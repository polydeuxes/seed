# Manual Observation Invocation Permission Investigation

## Purpose

This investigation distinguishes manual operator invocation from reusable Seed
observation-domain permission without implementing permission storage, new CLI
behavior, observation behavior, policies, runtime autonomy, or authority models.

The motivating ambiguity is:

```text
operator manually ran a command
  != operator granted Seed reusable autonomous permission
```

but also:

```text
operator manually ran a command
  may be sufficient operator expression for that single invocation
```

Repository authority wins. This document therefore treats existing implemented
models, event flows, and boundary documents as evidence, and it avoids promoting
candidate CLI syntax into implemented behavior.

## Existing Manual Invocation Authority Evidence

### Current CLI and runtime input preserve invocation as input, not permission

The local CLI defaults to `workspace_id="local"` and `session_id="local"`, and
`LocalSeedApp.run(text)` sends text into `Runtime.handle_user_message` according
to the input-source authority reconciliation. That means the local manual path is
preserved as a user-message interaction in a local scope, not as an approval
record, authenticated principal, or durable permission grant.

`Runtime.handle_user_message` appends an `input.user_message` event with
`payload={"text": text}`, `actor="user"`, `workspace_id`, and `session_id`, then
projects state, composes context, obtains a model decision, validates it, applies
the tool-intent guard for tool calls, and routes the result.

Existing evidence supports this conclusion:

- `Actor` contains coarse event-author labels such as `user`, `model`, `system`,
  `tool`, `builder`, and `approver`; it is not an authenticated principal model.
- `Event` stores `kind`, `workspace_id`, `actor`, `payload`, `session_id`,
  `causation_id`, and `correlation_id`, but not transport, OS user, TTY,
  authenticated principal, source trust, authorization scope, or manual/autonomous
  invocation mode.
- The input-source authority reconciliation explicitly says runtime user-message
  intake records raw text with `actor="user"`, workspace, and session, while it
  does not preserve channel, transport, authenticated principal, authentication
  strength, source trust, modality, device identity, or authorization scope.
- The principal-identity reconciliation explicitly says runtime input is not a
  claimed or authenticated principal surface.

Therefore the repository currently distinguishes manual input from approval only
negatively: manual CLI/user input has an input event shape, while approval has a
separate approval event/model shape. There is no current first-class
`manual_operator_invocation` event, source envelope, or invocation-authorization
record.

### Manual invocation can be a one-execution operator expression conceptually

Repository evidence does not forbid treating a direct manual CLI invocation as
operator expression for the command being run now. The CLI already has many
read-only diagnostic and observation-style flags whose use is interpreted by the
process as a request to perform that action now. For ordinary manual use, forcing
an additional `--approve-once` flag for the same foreground command would add
operator burden without adding current repository-backed authentication or
principal proof.

However, because the event ledger currently records only coarse actor/input
metadata, that one-execution expression should be understood as process-local and
invocation-local unless a future implementation records it explicitly. It is not
current durable approval evidence.

## Existing Approval Evidence

### Approval model

`Approval` is already a durable permission-shaped model with:

```text
id
action
scope
approved_by
expires_at
constraints
```

The domain model describes approval as a durable permission decision for a
specific action, scope, and actor. Policy documentation says approvals are scoped
and expiring, and should not be broad unless intentionally designed.

`State.has_approval(action, scope)` searches projected approvals by exact action,
optional exact scope, and expiry. `PolicyGate.evaluate(...)` allows a matching
approval before applying risk-class defaults. That is the strongest existing
pattern for reusable bounded permission.

### Pending action lifecycle

`PendingActionService.create_tool_call(...)` emits `pending_action.created` for a
tool call that must not execute yet. `mark_approved(...)` emits
`pending_action.approved` with `actor="approver"`, but this is a pending-action
status transition, not creation of a reusable `Approval` grant. Existing
inventory documentation already preserves that distinction: a durable
`approval.granted` can satisfy later policy checks, while
`pending_action.approved` does not create an `Approval` model.

### Execution authorization is not a current authority foundation

`ExecutionAuthorization` exists, but repository authority repeatedly marks it as
legacy/experimental, non-core, secret-free metadata that must not be treated as
permission for Seed to execute anything. It should not be reused as the basis for
observation-domain permission without an explicit reintroduction design.

### Observation-domain visibility is read-only and not authorization

The current `observation_domains` report is a visibility surface derived from
existing evidence. Its boundary says `read_only=true`, `writes_event_ledger=false`,
and `mutates_cluster=false`. It classifies coverage/gaps; it does not authorize
new observation collection or future autonomous invocation.

## Recommended Conceptual Distinctions

The repository should keep these concepts separate:

| Concept | Meaning | Current repository support | Recommended use |
| --- | --- | --- | --- |
| Manual operator invocation | A foreground command was run by the operator now. | Partially implied by CLI/process context; not first-class in event models. | May authorize only that foreground invocation when command semantics are manual. |
| One-time approval for this invocation | An explicit approval grant for one specific invocation. | Not first-class for observation domains; closest analog is pending-action approval for tool calls. | Optional future concept only if Seed needs auditable one-shot grants separate from process invocation. |
| Standing approval for future Seed autonomous invocation | Reusable bounded permission for action/scope/constraints until expiry. | Strongly analogous to `Approval(action, scope, approved_by, expires_at, constraints)`. | Must be recorded separately from observation events and manual command invocation. |
| Unknown authorization state | No evidence of manual foreground expression, one-time grant, or reusable approval. | Supported by absence of relevant records, but no observation-permission model exists. | Report as unknown/requires operator expression, not as denied. |
| Denied authorization | A policy or authority decision refused the action. | Policy outcomes include `block`; no observation-domain denial model exists. | Only report denied when there is explicit denial/block evidence. |

These distinctions preserve the requested boundaries:

```text
permission event != observation event
manual command invocation != standing autonomous authorization
operator expression != authenticated authority proof
capability availability != observation authorization
observation authorization != execution authorization
```

## Supported CLI Semantics

The following semantics are supportable as conceptual future behavior because
they align with existing repository boundaries:

### `seed --observe-neighbors`

A manual foreground invocation can mean:

```text
run this observation now because the operator invoked it
```

It should not mean:

```text
Seed may run this observation domain later without asking
```

If surfaced, status should be explicit:

```text
Observation Permission:
  invocation_authorized_by: manual_operator_invocation
  reusable_seed_permission: not_granted
  future_autonomous_invocation: requires_operator_expression
```

or in prose:

```text
Command invoked manually by operator.
This authorizes this invocation only.
No standing Seed permission was granted.
```

### `seed --approve-observation neighbor_table_read --scope local_host --until ...`

This is conceptually distinct from running an observation. It would create a
bounded reusable approval and need an approval-shaped record, probably following
`Approval(action, scope, approved_by, expires_at, constraints)`. It should not
silently run the observation unless command semantics explicitly say it does.

### `seed --observe-neighbors --use-existing-approval`

This is useful as a future autonomous/runtime-like path because it says the
invocation should be authorized only by an existing reusable approval. If no
matching approval exists, it should fail or report requires operator expression,
rather than falling back to manual invocation semantics silently.

### `seed --observation-permission neighbor_table_read`

This is useful as a reporting surface. It should distinguish at least:

- reusable approval present;
- reusable approval absent;
- denied/block evidence present;
- unknown because no permission model/record exists;
- current command was manually invoked, if the reporting is in the context of an
  observation command run.

## Unsupported CLI Semantics

The following semantics are not supported by current repository evidence and
should not be claimed without implementation:

- Manual invocation creates `Approval` automatically.
- Manual invocation updates durable permission storage.
- `actor="user"` proves an authenticated operator identity.
- `actor="approver"` proves a named authenticated approver without separate
  grant metadata.
- Observation-domain capability availability means authorization to observe.
- Read-only observation-domain visibility means permission to perform sensitive
  network, process, Docker, or external API observation.
- `ExecutionAuthorization` is a current reusable permission mechanism.
- Absence of approval means explicit denial; it is usually unknown or requires
  operator expression unless policy has explicit block evidence.

## Risks Of Over-Authorizing

The main over-authorization risk is treating a manual command as reusable Seed
authority. That would convert:

```text
run this now because I typed it
```

into:

```text
Seed may run this later without asking
```

which conflicts with current approval scoping, expiry, and authority-boundary
documents. It would also blur observation events with permission events and could
make sensitive domains such as traffic capture, Docker socket reads, root process
visibility, active probing, and external API queries appear authorized merely
because they were once run manually.

A second risk is treating `actor="user"` as an authenticated operator proof. The
repository currently says actor is event-author vocabulary, not principal proof.
If standing approvals eventually require identity, they need explicit grant
metadata such as `approved_by` plus a future source/identity boundary, not a raw
input actor alone.

A third risk is using legacy `ExecutionAuthorization` as a shortcut. Repository
authority says it is non-core and not permission for Seed to execute anything.

## Risks Of Over-Burdening The Operator

The main operator-burden risk is requiring redundant explicit approval for every
ordinary foreground manual observation command even when the operator typed the
command in order to run it now. That would make manual diagnostics awkward while
providing little additional evidence under current implementation, because Seed
still lacks authenticated source envelopes and observation-domain permission
storage.

A balanced future surface should therefore allow direct manual invocation for
this execution only, while making reusable permission an explicit separate act.
The operator burden should appear only at the point where Seed needs reusable,
autonomous, background, scheduled, or delegated permission.

## Supported Conclusions

1. **When an operator manually invokes a sensitive observation command, that can
   be treated as sufficient operator expression for that invocation only** if the
   command is explicitly a foreground manual command. Current repository evidence
   supports this as a CLI semantic, not as a durable permission record.
2. **Manual invocation does not grant future Seed permission.** Existing input
   and actor metadata are not approval records, authenticated principals, or
   reusable grants.
3. **Approval should be separate from observation.** The existing `Approval`
   model is permission-shaped, while observation-domain visibility is read-only
   coverage/gap reporting and observation events should not double as grants.
4. **Standing observation-domain permission should follow the existing approval
   pattern if implemented later:** action/domain, scope, approved-by identity,
   expiry, and constraints.
5. **Permission status after manual invocation should surface both halves:** the
   invocation was manually authorized for this run, and reusable Seed permission
   remains not granted or unknown.
6. **Unknown and denied should remain distinct.** Lack of an approval record is
   not the same as explicit denial unless policy/block evidence exists.

## Unsupported Conclusions

This investigation does not support concluding that:

- Seed already has first-class observation-domain authorization.
- Seed already records manual invocation authority as a distinct event.
- Seed can authenticate the operator from `actor="user"`, workspace, session, or
  local CLI defaults.
- A single manual observation run should create standing permission.
- A future autonomous runtime can reuse manual invocation evidence as durable
  permission.
- Observation authorization is the same as execution authorization, capability
  availability, or observation-source provenance.

## Open Questions

- If one-time approval needs durable auditability, should it be a distinct
  invocation-scoped approval record, a constrained `Approval`, or a separate
  `operator_expression` event?
- What source envelope or authentication boundary is required before
  `approved_by` can be more than a string supplied at a CLI/API boundary?
- Should future observation-domain permission actions be named by domain
  (`neighbor_table_read`) or by concrete collector/provider operation?
- How should denial/revocation be represented for observation domains, given that
  current `Approval` has expiry but no general revocation model in this
  investigation?
- Should manual foreground commands record a non-permission audit event such as
  `observation.invocation_requested` if observation collection later becomes
  recordable?
- How should `--record` observation commands preserve `record_scope=diagnostic_run`
  and `mutates_cluster=false` while also reporting invocation-only permission?

## Answer To Acceptance Questions

### When an operator manually invokes a sensitive observation command, does that authorize the invocation?

Conceptually yes for that one foreground invocation, if the command's semantics
are manual and immediate. Current repository evidence supports this only as a
CLI/process semantic; it is not currently stored as a first-class permission
record.

### Does it grant future Seed permission?

No. Manual invocation does not create `Approval`, does not prove an authenticated
principal, does not create `ExecutionAuthorization`, and does not grant future
autonomous permission.

### Should approval be separate from observation?

Yes. Existing approval and observation surfaces are different: `Approval` is a
scoped, expiring permission-shaped model, while observation-domain visibility is
read-only evidence/coverage reporting. Observation events or reports should not
silently become approval grants.

### How should Seed surface the distinction?

A future surface should say, in machine-readable or prose form:

```text
invocation_authorized_by: manual_operator_invocation
reusable_seed_permission: not_granted
future_autonomous_invocation: requires_operator_expression
```

when a foreground manual command was run without a matching reusable approval. If
there is no current manual invocation context and no permission record, the
status should be `unknown` or `requires_operator_expression`, not implicitly
allowed or denied.
