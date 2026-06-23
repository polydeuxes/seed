# Observation-Domain Permission Authority Reuse Investigation

## Purpose and boundary

This investigation asks whether existing repository authority mechanisms could support future observation-domain permission questions.

This is investigation only.

It does not implement new permission systems, authority systems, policy rules, configuration mechanisms, runtime behavior, observation behavior, or event shapes.

Repository authority wins.

## Central finding

Repository evidence supports reuse of several existing authority-bearing concepts for observation-domain permission, but not as-is.

The strongest supported answer is:

```text
existing authority mechanisms can partially support observation-domain permission
```

but:

```text
observation-domain authorization is not currently first-class
```

and:

```text
observation permission must remain distinct from capability availability
```

Repository authority does not currently justify a separate permission subsystem.

Repository authority also does not support pretending the existing action/execution authorization model already answers observation-domain permission.

The likely future shape, if needed, is reuse of existing authority vocabulary patterns:

```text
action/scope/approved_by/expires_at/constraints

policy outcome vocabulary

operator expression through event ledger records

read-only boundary invariants
```

with a narrower observation-domain target.

## Core distinction

The important distinction is:

```text
capability availability
    !=
observation authorization
```

Examples:

```text
listener_process_inventory
    may be useful
    may be attainable
    may be unavailable
```

while:

```text
network exploration
    may be useful
    may be technically attainable
    may still be unauthorized
```

These are different questions.

Capability relationship asks:

```text
what capability pressure, access context, attainability, and expectation are visible?
```

Observation permission asks:

```text
has the operator authorized this observation domain under this scope?
```

Repository authority wins.

## Existing authority mechanisms

### Event authorship

The repository has `Actor` vocabulary:

```text
user
model
system
tool
builder
approver
```

Current meaning:

```text
event authorship category
```

Not:

```text
authenticated principal
```

This is useful for recording operator expression but insufficient for proving authority.

### Workspace/session/correlation scope

Events carry:

```text
workspace_id
session_id
causation_id
correlation_id
```

These support scoping and traceability.

They do not prove identity or permission.

### Policy outcome vocabulary

Existing policy outcomes include:

```text
allow
block
require_confirmation
require_approval
```

This is directly analogous to observation permission status.

However existing `PolicyGate` applies to tool policy actions, not observation domains.

### Tool risk vocabulary

Existing tool specs include:

```text
policy_action
risk_class
```

This supports risk/approval reasoning for registered tool calls.

It does not directly classify observation domains such as:

```text
neighbor_table_read
traffic_capture
active_network_probing
```

### Approval model

Existing `Approval` includes:

```text
action
scope
approved_by
expires_at
constraints
```

This is the strongest reusable authority-bearing shape.

It already models:

```text
what was approved
where it applies
who approved it
when it expires
what constraints apply
```

Observation-domain permission could plausibly reuse that pattern.

But current approvals are action-oriented and policy-gate oriented.

### Pending action model

`PendingAction` includes:

```text
action
tool_name
arguments
scope
status
created_from_event_id
causation_id
```

and statuses:

```text
pending
approved
completed
cancelled
```

This is useful as an approval lifecycle pattern.

It is currently tied to tool calls awaiting human approval or confirmation.

### Action plan lifecycle

Action plans support:

```text
proposed
accepted
rejected
superseded
```

and explicit plan approval.

Important boundary:

```text
plan approval is not execution authorization
```

This is a strong precedent for not collapsing:

```text
operator likes the idea
```

into:

```text
operator authorized observation
```

### Execution authorization

Existing `ExecutionAuthorization` records secret-free, short-lived grant metadata for a concrete execution proposal:

```text
execution_proposal_id
action_plan_id
tool_name
arguments_fingerprint
granted_by
expires_at
interactive_prompt
ssh_agent
sudo_timestamp
external_vault_token_ref
secret_seen_by_seed=false
```

Important boundary:

```text
legacy/experimental
non-core
concrete proposal scoped
not generic runtime authority
```

It is a useful analogy.

It should not be reused uncritically for observation domains.

## Existing operator-expression mechanisms

Repository-visible operator expression currently appears through:

```text
input.user_message events
actor=user
workspace/session scope
action_plan.accepted
action_plan.rejected
action_plan.approved
pending_action.approved
execution_authorization.granted
```

But generic user-message input lacks first-class source authority metadata.

Current gaps include:

```text
authenticated principal
claimed principal
authorization scope
source trust
channel
transport
modality
device identity
```

Therefore operator expression exists, but source authority is weak.

This matters for observation-domain permission because:

```text
operator said something
    !=
operator authorized this observation domain
```

unless the repository preserves the expression as an approval-like scoped record.

## Existing observation-domain mechanisms

`observation_domains.py` already exposes read-only observation-domain visibility.

Current domain entries include:

```text
domain
classification
gap_type
pressure
evidence
```

Current mapped domains include:

```text
local_listeners
container_runtime
```

Current classifications include:

```text
observed
partially_observed
unobserved
unknown
```

Current gap types include:

```text
missing_evidence_inside_observed_domain
missing_observation_domain
unknown
```

This is visibility, not permission.

The surface boundary is:

```text
read_only=true
writes_event_ledger=false
mutates_cluster=false
```

Therefore observation domains already exist as visibility objects, but not as authorization objects.

## Existing capability mechanisms

`capability_relationship.py` exposes:

```text
capability
current_access
operational_benefit
pressure
attainability
expectation
reasoning
known_limitations
```

It intentionally reports:

```text
attainability=unknown
expectation=unknown
```

and states that capability pressure is visibility context, not acquisition guidance.

This is important.

Capability relationship can say:

```text
useful
unknown
not acquisition guidance
```

It cannot say:

```text
operator authorized network scan
```

## Existing privilege mechanisms

`privilege_discovery.py` exposes capability privilege guidance such as:

```text
partial_non_root
docker_group_or_root
available
root
unknown
```

It includes explicit caution such as:

```text
requires root visibility; do not collect until explicitly authorized
```

This is the closest existing bridge between access capability and permission.

But it still remains guidance about privilege/access, not a stored authorization decision.

## Relevant invariants

Existing repository invariants already preserve many boundaries directly relevant to observation-domain permission:

```text
Observation must not imply execution.
Observation must not imply availability.
Observation must not imply management.
Write access must not be required for observation.
Prefer least-privileged observation sources.
Observation must not claim more than the selected source directly supports.
Read-only observation must remain separate from mutation, provider calls, and registered-operation execution.
Observing a local network segment must not imply neighbor existence, subnet occupancy, gateway reachability, or scanning.
```

These invariants strongly support the new distinction:

```text
technical ability to observe
    !=
permission to observe
```

## Observation-domain examples reviewed

Examples only:

```text
network_scan
traffic_capture
neighbor_table_read
docker_socket_read
root_process_visibility
external_api_query
```

### `neighbor_table_read`

Likely characteristics:

```text
may be non-root
may be passive/local
may reveal nearby devices
may still require operator authorization
```

Existing authority structures could represent it as:

```text
action=observation_domain.neighbor_table_read
scope=host/local-network
approved_by=operator
constraints={read_only:true, no_active_probe:true}
```

But this is not implemented.

### `traffic_capture`

Likely characteristics:

```text
sensitive
may require elevated privileges
may collect third-party/private traffic
```

Existing approval/authorization patterns are relevant, but current capability/privilege surfaces are insufficient.

This likely needs explicit authorization semantics if ever supported.

### `active_network_probing`

Likely characteristics:

```text
not merely observation
can affect remote systems
can cross social/legal/operator boundaries
```

Existing policy outcomes are analogous.

But active probing may not fit read-only observation even if it is used for discovery.

### `docker_socket_read`

Likely characteristics:

```text
may be read-only intent
but docker socket access is often root-equivalent
```

Existing privilege guidance already marks container inventory as docker-group-or-root.

Observation permission would still need a separate operator authorization decision.

### `root_process_visibility`

Likely characteristics:

```text
requires elevated process visibility
may expose sensitive command lines/environments
```

Existing privilege discovery can identify root requirement.

It cannot authorize it.

### `external_api_query`

Likely characteristics:

```text
may not need root
may involve external disclosure
may require account/API/provider scope
```

Existing tool policy and approvals are closer here, but observation-source permission remains separate from capability presence.

## Evidence supporting reuse

Existing repository authority mechanisms already include the ingredients needed for future observation-domain permission:

```text
append-only events
actor categories
workspace/session/correlation scope
PolicyOutcome vocabulary
Approval(action, scope, approved_by, expires_at, constraints)
PendingAction lifecycle
ExecutionAuthorization-style short-lived grants
risk_class and policy_action patterns
read-only invariants
least-privileged observation invariants
```

The strongest reusable concept is:

```text
Approval(action, scope, approved_by, expires_at, constraints)
```

Observation-domain permission could be modeled as a scoped approval target without creating a fundamentally new permission philosophy.

## Evidence arguing against simple reuse

Existing authority mechanisms are not enough as-is.

Reasons:

```text
Approval is currently action/policy oriented, not observation-domain oriented.
ExecutionAuthorization is legacy/experimental and concrete-proposal scoped.
PendingAction is tool-call oriented.
PolicyGate evaluates ToolSpec.policy_action, not observation domain.
Actor is not authenticated principal.
Workspace/session are not authority.
Observation source metadata is provenance, not permission.
Capability relationship does not encode operator authorization.
Privilege discovery gives guidance, not permission state.
```

Therefore reuse is plausible at the pattern/vocabulary level, but not currently implemented as behavior.

## Authority-bearing concepts already present

Existing concepts analogous to the requested vocabulary:

```text
authority source
    -> approved_by / granted_by / actor / source_type, with caveats

approval source
    -> Approval.approved_by

authorization scope
    -> Approval.scope / PendingAction.scope / input-envelope docs authorization_scope

operator expression
    -> input.user_message / action_plan lifecycle events / pending_action.approved

allowed
    -> PolicyOutcome.allow

denied
    -> PolicyOutcome.block / action_plan.rejected

unknown
    -> absence of matching approval or explicit authority metadata; observation_domains unknown classification
```

But these are not equivalent.

The repository must preserve their current boundaries.

## Supported conclusions

1. Existing repository mechanisms can partially support future observation-domain permission.
2. A fundamentally separate permission subsystem is not currently justified by repository evidence.
3. Existing `Approval(action, scope, approved_by, expires_at, constraints)` is the strongest reusable authority-bearing shape.
4. Existing policy outcome vocabulary is reusable as status vocabulary.
5. Existing input source authority work already identified the relevant gap: source/authority metadata is not first-class for generic input.
6. Capability availability and observation authorization must remain separate.
7. Observation-domain visibility exists today, but observation-domain permission does not.
8. Privilege discovery can identify access/privilege boundaries, but it cannot grant permission.
9. Existing invariants strongly support least-privileged observation and prohibit observation from implying execution, availability, management, or scanning.
10. Any future observation-domain permission should likely reuse authority patterns, not bypass them.

## Unsupported conclusions

- Observation-domain authorization is currently implemented.
- Existing capability relationship answers permission questions.
- Existing privilege discovery authorizes privileged observation.
- Actor `user` proves operator authorization.
- Workspace/session scope proves authority.
- Observation source metadata proves permission.
- ExecutionAuthorization should be promoted into a general observation-permission model.
- Active network probing is read-only merely because it is used for observation.
- Technical attainability implies authorization.

## Open questions

- What is the minimal observation-domain permission record, if one is ever needed?
- Should observation-domain permission reuse `Approval.action` and `Approval.scope`, or require a clearer non-execution target name?
- How should operator denial be represented for an observation domain?
- Should permission states be `allowed`, `denied`, `unknown`, `requires_confirmation`, and `requires_approval`, matching existing policy outcomes?
- How should time-bounded permission be represented for passive versus active observation?
- Can observation permission remain a read-model over existing events rather than a new subsystem?
- How should permission differ for passive local reads, privileged local reads, external API reads, and active network probes?

## Acceptance answer

### If Seed eventually needs observation-domain permission, can existing authority mechanisms support it?

Partially yes.

Existing mechanisms provide reusable authority-bearing patterns:

```text
approval source
scope
constraints
expiry
policy outcomes
operator lifecycle events
read-only invariants
least-privilege invariants
```

The strongest candidate for reuse is the approval shape:

```text
Approval(action, scope, approved_by, expires_at, constraints)
```

applied to observation-domain targets rather than tool execution targets.

### Or would observation authorization require fundamentally new authority concepts?

Repository evidence does not currently justify fundamentally new authority concepts.

It does suggest a missing target/scope distinction:

```text
observation domain permission
```

is not currently the same as:

```text
tool approval
execution authorization
capability availability
privilege visibility
operator input
```

Therefore the likely future need is a narrow extension or reuse of existing authority patterns, not a separate permission subsystem.
