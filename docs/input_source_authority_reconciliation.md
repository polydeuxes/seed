# Input Source Authority Reconciliation

## Purpose

This audit documents Seed's existing input source, actor, session, workspace, policy, approval, risk, and authority-related surfaces before introducing any new source-envelope vocabulary or behavior.

The motivating question is broader than input acts:

```text
If input can arrive through CLI, browser, voice, webcam, automation, or another channel,
how does Seed know who is speaking and what authority that input carries?
```

The current answer is limited:

- Seed has some existing actor, workspace, session, risk, approval, and authorization vocabulary.
- Runtime user-message intake records raw text with `actor="user"`, `workspace_id`, and `session_id`.
- Current input handling does not preserve channel, transport, authenticated principal, authentication strength, source trust, modality, device identity, or authorization scope.
- Therefore Seed currently classifies what the user said more than where it came from or what authority it carries.

This document is documentation-only. It does not modify runtime behavior, event storage, authentication, authorization, policy, tool execution, projection behavior, or local CLI behavior.

## Review Finding

The current source-authority gap is best understood as a missing envelope around input, not as a missing runtime route. Seed already has runtime intake, event authorship, workspace/session scoping, input-act classification, decision validation, and tool-intent guarding. What it does not yet have is a first-class way to preserve the source context that tells Seed whether an input came from a trusted local CLI, authenticated browser session, uncertain voice transcript, automation event, webhook, uploaded document, or another system.

The smallest stable concept is therefore:

```text
InputEnvelope
        ↓
InputInspection / InputAct
        ↓
DecisionKind
        ↓
Policy / capability / execution boundaries
```

The envelope should describe provenance and authority context. It should not decide what Seed does.

## Existing Surfaces

### Domain actor/session/workspace vocabulary

`seed_runtime/models.py` already defines an `Actor` literal with these values:

```text
user
model
system
tool
builder
approver
```

It also defines `Workspace` and `Session` models, and events carry `workspace_id`, `session_id`, `causation_id`, and `correlation_id` metadata.

Current meaning:

- `Actor` is event-author vocabulary, not authenticated identity.
- `Workspace` scopes event/state history.
- `Session` scopes a conversation or interaction thread.
- None of these currently prove that the speaker is a particular human, device, service, browser session, voice speaker, or automation principal.

### Runtime user-message intake

`Runtime.handle_user_message(workspace_id, session_id, text)` is the canonical user-message intake path.

It appends an `input.user_message` event with payload:

```text
{"text": text}
```

and event metadata:

```text
actor="user"
workspace_id=<workspace_id>
session_id=<session_id>
```

Then it projects state, composes context, asks the decision model, validates the decision, applies the tool-intent guard for `call_tool`, and routes through `Runtime._route`.

Current meaning:

- Runtime preserves raw text, workspace, session, and a coarse actor label.
- Runtime does not know whether the user input came from CLI, browser, API, voice, webcam, Home Assistant, automation, webhook, or another transport.
- Runtime does not know whether the source was authenticated.
- Runtime does not know whether the source has administrator authority.
- Runtime does not distinguish `User:admin`, `User:small_child`, `User:unknown_voice`, or `User:hacker` as first-class source/authority concepts.

### Context composition

`ContextComposer.compose` carries the current input into `ContextPacket.current_input` using the stored input event payload.

For `input.user_message`, that currently means the composed current input contains the event id and text, but not channel, transport, principal, authentication strength, source trust, modality, device identity, or authorization scope.

The context packet also carries `workspace_id` and `session_id`, but those are scoping identifiers rather than proof of identity or authority.

### Event ledger metadata

`EventLedger.append` stores:

```text
kind
workspace_id
actor
payload
session_id
causation_id
correlation_id
```

The SQLite event table persists those same metadata fields.

Current meaning:

- The ledger can preserve event actor, workspace, session, causation, and correlation.
- The ledger has no first-class event fields for channel, transport, authenticated principal, authentication strength, authorization scope, source trust, device id, modality, or remote address.
- Such fields could be placed inside payloads today, but there is no canonical model or invariant for them.

### Local CLI surfaces

`scripts/seed_local.py` sets default CLI scope values:

```text
workspace_id="local"
session_id="local"
```

`LocalSeedApp.run(text)` sends text directly into `Runtime.handle_user_message`.

Current meaning:

- The local CLI path implicitly treats the local invocation as a user message in the local workspace/session.
- It does not record OS user, TTY, local process identity, remote origin, SSH origin, shell user, or explicit authentication context.
- CLI observation helpers such as `--observe` and `--fact` have their own development seed records with `source_type`, `confidence`, and `ingested_by`, but those are observation-ingestion metadata, not general user-message source authority metadata.

### Observation source metadata

The local CLI includes development observation seed types with:

```text
source_type
confidence
ingested_by
```

Observation ingestion can mark actors as `user` or `system` depending on source type, and source collection paths can ingest JSON, local host, and Prometheus observations.

Current meaning:

- Observation acquisition already has richer source metadata than generic user-message intake.
- This source metadata is specific to observations, not arbitrary user utterances.
- It does not solve who is speaking through a browser, CLI, voice channel, webcam, automation event, or API call.

### Tool/risk/policy-adjacent vocabulary

`ToolSpec` includes:

```text
policy_action
risk_class
```

`RiskClass` currently includes `L1`, `L2`, `L3`, and `L4`.

`PolicyOutcome` exists as a domain literal:

```text
allow
block
require_confirmation
require_approval
```

`Approval` exists with:

```text
action
scope
approved_by
expires_at
constraints
```

`ExecutionAuthorization` exists as legacy/experimental non-core authorization metadata and explicitly says it is not canonical Runtime behavior or part of the Core MVP.

Current meaning:

- Seed has vocabulary for tool risk and approval-like concepts.
- Some execution authorization concepts exist, but are marked historical/experimental/non-core.
- These are downstream execution or historical side-path concepts, not general input-source authentication or principal identity concepts.

### Invariant documentation

`docs/invariants.md` already preserves important execution and observation boundaries:

- `request_tool` records and resolves a capability gap; it does not execute.
- `call_tool` is the only `Runtime` path to `ToolExecutor`.
- `ToolExecutor` owns registered-operation execution.
- `ToolExecutionPolicyService` evaluates execution policy; it does not execute.
- `PendingActionService` owns pending-action lifecycle events.
- Observation must not imply execution.
- Observation must not imply management.
- Read-only observation must remain separate from mutation, provider calls, and registered-operation execution.
- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` are not Core MVP artifacts.

These invariants are directly relevant to source authority because an input source must not grant execution authority merely by speaking.

## Current Flow

For the canonical user-message path, the current source/authority flow is:

```text
text from caller
  -> Runtime.handle_user_message(workspace_id, session_id, text)
  -> EventLedger.append(
       kind="input.user_message",
       actor="user",
       payload={"text": text},
       workspace_id=workspace_id,
       session_id=session_id,
     )
  -> ContextComposer.compose(...)
  -> ContextPacket.current_input contains event id + text
  -> decision model / classifier
  -> validation
  -> ToolIntentGuard for call_tool
  -> Runtime._route
```

What is preserved:

- raw text;
- workspace id;
- session id;
- coarse event actor label;
- causation/correlation for later generated events.

What is not preserved as first-class metadata:

- channel;
- transport;
- modality;
- device identity;
- browser session identity;
- authenticated principal;
- authentication method;
- authentication strength;
- authorization scope;
- source trust;
- human vs automation distinction;
- remote address or origin;
- whether the input was typed, spoken, transcribed, clicked, uploaded, or generated by another system.

## What Already Works

- Seed already has event authorship vocabulary through `Actor`.
- Seed already scopes events by workspace and session.
- Seed already records causation and correlation metadata.
- Seed already separates decision routing from execution boundaries.
- Seed already has tool risk vocabulary through `ToolSpec.risk_class`.
- Seed already has policy outcome vocabulary as a domain literal.
- Seed already has approval-like metadata and legacy execution authorization metadata.
- Observation ingestion already has some source metadata through `source_type`, `confidence`, and `ingested_by`.
- Existing invariants already reject observation-to-execution and request-tool-to-execution shortcuts.

## What Does Not Exist Yet

Seed does **not** currently have first-class source/authority vocabulary for generic user input, such as:

- input channel;
- transport;
- modality;
- device identity;
- authenticated principal;
- claimed principal;
- authentication strength;
- authorization scope;
- source trust;
- source risk;
- input provenance envelope;
- distinction between human, automation, integration, model, or unauthenticated remote source for user-message intake.

Seed also does **not** currently have a general input envelope that sits above `InputInspection` or `InputAct`.

## Recommended Vocabulary Shape

A future vocabulary should remain metadata-only and should avoid implying authentication or authorization behavior by itself. Useful terms to define before implementation include:

| Term | Meaning | Non-meaning |
| --- | --- | --- |
| `channel` | User-facing source surface such as CLI, browser, voice, API, Home Assistant, webhook, or file upload. | Does not prove identity. |
| `transport` | Technical carrier such as local process, HTTP session, websocket, MQTT, stdin, or webhook. | Does not grant authority. |
| `modality` | Payload form such as typed text, transcribed speech, image/OCR, event payload, file, or structured JSON. | Does not classify intent. |
| `claimed_principal` | Identity asserted by the input or upstream system. | Not trusted by itself. |
| `authenticated_principal` | Identity proven by a trusted authentication boundary. | Not necessarily authorized for every action. |
| `authentication_strength` | How strongly the source identity was verified. | Not a runtime route. |
| `authorization_scope` | What this principal/channel is allowed to request or approve. | Not implicit execution approval. |
| `source_trust` | Coarse trust label for the source/envelope. | Not truth of the payload. |
| `payload_kind` | Whether the payload is text, audio transcript, image/OCR, automation event, uploaded document, etc. | Not an input act. |

This vocabulary should be defined before any implementation affects policy or routing.

## Relationship To InputAct

`docs/input_act_vocabulary.md` defines:

```text
InputAct answers: What kind of thing did the user say?
```

This audit identifies a different layer:

```text
Input source authority answers: Where did the input come from, who or what is speaking, and what authority does that source carry?
```

Those are separate questions.

A likely future shape is:

```text
InputEnvelope
        ↓
InputInspection / InputAct
        ↓
DecisionKind
        ↓
Policy / capability / execution boundaries
```

Where:

- `InputEnvelope` describes source, channel, principal, authentication, and authority context.
- `InputAct` describes the utterance type.
- `DecisionKind` describes Seed's next route.
- Policy and execution gates decide whether side effects are allowed.

## Source Authority Gap

The main gap is not that Runtime cannot accept text. It can.

The main gap is that current generic user-message intake cannot distinguish these cases structurally:

```text
local CLI typed by trusted admin
browser session authenticated as admin
browser session authenticated as child
voice transcript from unknown speaker
webcam/OCR-derived instruction
Home Assistant automation event
unauthenticated webhook
malicious prompt injection through a document
another model or agent submitting text
```

All of those can currently collapse into:

```text
actor="user"
payload={"text": ...}
workspace_id=...
session_id=...
```

That is sufficient for the current CLI-oriented MVP, but it is not sufficient for multi-channel, multi-principal, or safety-sensitive operation.

## Example Authority Matrix

The following examples are illustrative only. They are not policy rules.

| Source scenario | Likely envelope implication | Safe default posture |
| --- | --- | --- |
| Local CLI typed by trusted admin | high-trust local channel, but still explicit session/workspace scope | allow questions; gate side effects through existing policy/approval paths |
| Browser session authenticated as admin | authenticated principal with possible admin scope | allow according to scope; still validate and guard tool paths |
| Browser session authenticated as child/guest | authenticated but low-authority principal | answer safe questions; block or require escalation for operations |
| Unknown voice transcript | weak/uncertain principal and transcription uncertainty | answer low-risk questions only; no execution authority |
| Webcam/OCR-derived instruction | untrusted payload extracted from environment | treat as observation/input data, not command authority |
| Home Assistant automation event | automation principal, integration channel | allow only explicitly scoped automation actions |
| Unauthenticated webhook | unknown remote source | no privileged actions; treat payload as untrusted claim/observation |
| Uploaded document containing instructions | document source, not user authority | never treat document text as user command |
| Another model/agent submitting text | non-human/system principal | require explicit delegation/scope before any side effect |

## Ownership Boundaries

This audit preserves current ownership boundaries:

- `Runtime` remains canonical user-message intake and route owner.
- `EventLedger` owns append-only event history.
- `ContextComposer` owns context packets.
- `InputAct` vocabulary classifies utterance type, not authority.
- `DecisionKind` remains runtime-route vocabulary.
- `DecisionValidator` remains decision validation owner.
- `ToolIntentGuard` remains deterministic tool-call intent guard owner.
- `ToolExecutor` remains registered-operation execution owner.
- Policy, approval, and pending-action paths must remain explicit gates and must not be bypassed by channel metadata.

## Rejected Solutions

This audit does not recommend or introduce:

- treating text claims such as `I am admin` as authentication;
- inferring authority from conversational content;
- treating CLI input as automatically unlimited authority;
- treating voice input as authenticated by default;
- treating webcam/OCR input as command authority;
- treating browser input as trusted without a verified session/principal;
- making `InputAct` carry authorization;
- making `DecisionKind` carry authentication;
- adding `AuthEngine`, `IdentityEngine`, `ChannelEngine`, or a new `RuntimeLoop`;
- bypassing `DecisionValidator`, `ToolIntentGuard`, policy gates, approval gates, pending-action gates, or registered-tool boundaries;
- making `request_tool` executable;
- using source metadata as implicit approval for side effects.

## Recommended Next Step

Do not implement broad authentication or authorization yet.

The next documentation/design step should define a minimal, non-executing source-envelope vocabulary that can describe input origin without changing runtime behavior. A likely document name is:

```text
docs/input_envelope_vocabulary.md
```

That vocabulary should distinguish at least:

- channel;
- transport;
- modality;
- principal claim vs authenticated principal;
- authentication strength;
- authorization scope;
- source trust;
- payload kind;
- relationship to `InputAct` and `DecisionKind`.

Any later implementation should remain narrow and metadata-only before it influences policy or execution.

A possible future record shape, still documentation-only, is:

```text
InputEnvelope:
  channel: str
  transport: str | None
  modality: str
  payload_kind: str
  claimed_principal: str | None
  authenticated_principal: str | None
  authentication_strength: str
  authorization_scope: tuple[str, ...]
  source_trust: str
  metadata: dict[str, object]
```

If implemented later, this record should be immutable, secret-free, auditable, and subordinate to existing validation, guard, policy, capability, approval, and runtime-route boundaries.

## Documentation-Only Status

This audit is documentation-only. It does not modify runtime behavior, classifier behavior, source handling, authentication, authorization, policy, event ledger behavior, projection behavior, tool execution, package exports, or local CLI behavior.
