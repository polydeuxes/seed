# Implementation Authority Concept Recovery Investigation

## Scope

This is a recovery report, not a proposal. It searches current implementation,
tests, and existing repository documents for authority concepts that are already
backed by code, CLI surfaces, registries, or executable tests. It does not add a
new authority framework, registry, ontology, capability model, permission model,
or execution redesign.

The evidence base includes direct source review and broad repository searches for
`authority`, `permission`, `credential`, `execution`, `provider`, `observer`,
`projection`, `ownership`, `container`, `service`, `network`, `runtime`,
`cluster`, `local`, `remote`, and related relationship words.

## Implementation-backed authority concepts currently present

### Registered-operation execution authority

`ToolExecutor` is the clearest implementation-backed execution authority. It is
not broad shell authority. It is a constrained path that requires a registered
operation, validates it, evaluates policy, records tool-call events, and only then
executes the registered handler. Its architecture metadata explicitly names the
owner as `registered_tool_execution`, the layer as `execution`, and the required
edges to `ToolRegistry`, `StateProjector`, `EventLedger`, and
`RegisteredOperation`.

Recovered concept: **registered operation authority**. A tool call has execution
authority only when it is known to the registry, passes validation, and is allowed
by policy.

### Policy/risk approval authority

`PolicyGate` implements permission outcomes over tool policy actions. The gate
can block unknown actions, allow approved actions, allow low-risk read-only
operations, require confirmation, require approval, or block critical actions by
default. This is not credential authority and not provider authority; it is a
risk-and-approval decision over a `ToolSpec.policy_action` in projected state.

Recovered concept: **policy decision authority**. Policy is represented as an
execution prerequisite with status values: `allow`, `block`,
`require_confirmation`, and `require_approval`.

### Pending-action approval authority

`ToolExecutor.resume_approved_tool_call` recovers a separate authority concept:
approval is durable pending-action state, and only pending actions with status
`approved` may be resumed. This decomposes approval from initial validation and
from the actual tool handler execution.

Recovered concept: **resume authority for approved pending actions**. Approval is
a prerequisite for replaying a stored tool call, not a general grant.

### Diagnostic visibility and mutation-boundary authority

`DiagnosticInventoryEntry` declares whether each diagnostic uses projected state,
uses repository files, supports JSON, supports recording, emits diagnostic facts,
emits cluster facts, writes the event ledger, mutates the cluster, or reads
diagnostic facts. `DiagnosticShapeAudit` separately checks implementation shape
against that declaration using implementation specs and marker scans.

Recovered concept: **diagnostic surface authority**. Visibility is represented as
an inventory declaration plus shape audit. Recording authority is bounded by
`record_scope`; mutation authority is bounded by `mutates_cluster` and ledger
fields.

### Diagnostic-run recording authority

Several diagnostic entries that record output use `record_scope="diagnostic_run"`,
emit diagnostic facts, write the ledger, and keep `emits_cluster_facts=false` and
`mutates_cluster=false`. This is an implementation-backed boundary between
recording diagnostic output and mutating cluster truth.

Recovered concept: **diagnostic recording authority**. Diagnostic event writes are
allowed only as diagnostic-scoped records unless a surface intentionally declares
a different shape.

### Container ownership observation authority

`container_ownership_authority` is a narrow read-only evaluator. It distinguishes
`root`, `docker_socket_read`, `active_network_probe`, `local_passive`, and
`external_provider_query`; maps container inventory and port mapping to
`docker_group_or_root`; and returns `blocked` when root and Docker-socket read are
unavailable. Its boundary explicitly forbids recording, event-ledger writes,
cluster mutation, provider acquisition, permission creation, and executing an
observation.

Recovered concept: **container runtime observation authority**. Container
ownership is not inferred from the word Docker alone; the implementation asks
which observation is needed and which authority key can support it.

### Service ownership observation authority

`service_ownership_authority` decomposes service ownership into required
observations: TCP listen inventory, listener process inventory, systemd unit
inventory, container inventory, and container port mapping. It separately reports
reachable observations, blocked observations, blocked details, outcome, remaining
observations, and uncertainty. It uses implementation evidence from observation
inventory/domains, privilege discovery, ownership discrepancies, and capability
needs.

Recovered concept: **composite service attribution authority**. Service ownership
authority is not one permission. It composes local passive listener evidence,
process inventory, systemd evidence, and container runtime evidence, each with
separate authority requirements.

### Listener endpoint observation authority

`listener_endpoint_authority` exposes local listener endpoint authority as a
read-only slice requiring local passive authority for protocol, address, port, and
local socket-table evidence. Its boundary excludes process ownership, service
ownership, application ownership, container ownership, health, responsiveness,
external accessibility, DNS validity, remote network reachability, causality, and
intent.

Recovered concept: **local endpoint observation authority**. Listener endpoint
authority reaches only protocol/address/port evidence, not ownership or
availability.

### Observation-permission classes

The authority-slice implementations consult `observation_permission` and
`privilege_discovery` to map observation classes or capability names to required
privilege such as local passive observation or Docker-group/root access. This
makes observation prerequisites explicit without converting them into execution
rights.

Recovered concept: **observation prerequisite authority**. Observation authority
is represented as requirements for evidence acquisition, not as permission to
mutate.

### Provider/handoff authority boundary

Repository architecture and implementation documents consistently preserve the
external-provider boundary: Seed may recommend or hand off, but external
providers own credentials, retries, schedules, long-running jobs, and real host
automation. Handoff metadata does not imply Seed execution, credential
availability, provider trust, or operation registration.

Recovered concept: **external provider execution authority**. Provider authority
is outside Seed's core runtime, while Seed owns metadata, recommendations,
capability gaps, and audit records.

### Projection and context-view non-authority

Projection and context views are explicitly read-only representations over
projected state. They do not append events, mutate state, invoke providers,
evaluate policy, execute operation implementations, run shell commands, or make
network calls. This is implementation-backed negative authority.

Recovered concept: **projection visibility without execution authority**.
Projection can answer what is currently believed or selected, but it does not
become authority to execute or mutate.

### Repository/documentation navigation authority

The README declares a documentation maintenance authority model and points to a
documentation navigation authority. This is backed mainly by documentation and
navigation surfaces, not by execution code. It is therefore an implementation-adjacent
authority concept, weaker than execution or diagnostic authority but still
present as repository-maintenance authority.

Recovered concept: **documentation/navigation authority**. It routes repository
maintenance and discovery, but it is not runtime execution authority.

## Broad concepts already decomposed

### `authority`

The repository already decomposes authority into at least these separate
responsibilities:

- registered operation authority;
- policy/risk decision authority;
- pending-action resume approval;
- diagnostic visibility and recording authority;
- diagnostic mutation boundary;
- local passive observation authority;
- privileged Docker/root observation authority;
- active network probe authorization;
- external provider query/ownership boundary;
- projection/context visibility without execution authority;
- documentation/navigation authority.

No single implementation object owns all of these.

### `execution`

Execution decomposes into registry membership, validation, policy, event recording,
registered handler dispatch, pending approval, and external-provider delegation.
The implementation rejects compression of execution into "the runtime can run
things".

### `root`

`root` is not modeled as universal authority. In the ownership authority slices it
is one status key inside a constrained profile and is paired with
`docker_socket_read`. The container and service evaluators can report a
Docker/root-specific blocking boundary while still allowing local passive endpoint
or listener observations.

### `docker`

Docker is not one authority. Existing implementation separates Docker socket read,
Docker group/root authority, container inventory, container port mapping,
container ownership pressure, and the broader container runtime domain.

### `service`

Service ownership decomposes into listener endpoint facts, listener process
inventory, systemd unit inventory, container inventory, container port mapping,
ownership discrepancies, and capability needs. Listener endpoint authority
explicitly refuses to infer service ownership.

### `network`

Network-like authority decomposes into local passive socket-table evidence,
active network probing, external accessibility, DNS validity, and remote network
reachability. Listener endpoint authority supports only local TCP/UDP endpoint
inventory and excludes the rest.

### `provider`

Provider decomposes into recommendation/handoff metadata, external execution
backend, credential/secret boundary, provider result evidence, and absence of
Seed-owned retries/scheduling/lifecycle.

## Recurring authority responsibilities

The following recurring dimensions are supported by implementation evidence:

| Candidate dimension | Status | Implementation-backed characterization |
| --- | --- | --- |
| Observation authority | Supported | Authority slices declare required observations, required authority, available authority, reachable/blocked observations, and uncertainty. |
| Execution authority | Supported | `ToolExecutor` executes only registered tools after validation and policy; provider execution is external. |
| Mutation authority | Supported | Diagnostic inventory declares `mutates_cluster`; diagnostic shape audit checks mutation markers; read-only authority slices set mutation false. |
| Provider authority | Supported | External providers own real host automation, credentials, retries, schedules, and long-running jobs; Seed owns recommendations and evidence ingestion. |
| Projection authority | Rejected as execution authority; supported as visibility boundary | Projection exposes selected/current knowledge but is explicitly non-mutating and non-executing. |
| Selection authority | Partially supported | Context views and projection select visible/current facts, but this is selection for visibility/decision context, not permission or execution authority. |
| Ownership authority | Supported in narrow slices | Container, service, and listener endpoint authority surfaces recover ownership/attribution boundaries, especially what cannot be inferred. |
| Visibility authority | Supported | Diagnostic inventory, diagnostic shape audit, state views, context views, and documentation navigation expose what can be inspected. |
| Credential authority | Supported only as external boundary | Seed consistently refuses to store or request raw credentials; credentials remain provider-side resources. |
| Recording authority | Supported | Diagnostic recording is scoped to diagnostic runs and separated from cluster mutation. |

## Consistency across subsystems

Authority is consistent at the highest boundary: Seed repeatedly separates
knowledge/projection/recommendation from execution/mutation/credentials.
However, authority is not represented through one uniform model.

Implementation families use different representations:

- execution uses `ToolSpec`, registry validation, `PolicyGate`, events, and
  pending actions;
- diagnostics use static inventory declarations and shape-audit specs;
- observation/ownership slices use authority profiles, required observations,
  reachable/blocked observations, and explicit negative boundaries;
- provider/handoff boundaries are mostly in architecture documents, capability
  metadata, and recommendation language;
- projection/context visibility is represented as read-only views and negative
  execution claims;
- documentation navigation authority is represented by documentation routing and
  repository-maintenance guidance.

Conclusion: the repository has a consistent boundary posture but not a single
consistent authority schema.

## Compressed terminology that hides implementation structure

Supported compressed terms:

- **authority** hides policy, execution, observation, recording, mutation,
  provider, projection, and navigation responsibilities.
- **execution** hides registered dispatch, validation, policy, pending approval,
  event recording, and external provider delegation.
- **root** hides a specific privileged-observation status rather than global
  permission.
- **docker** hides Docker socket read, Docker group/root privilege, container
  runtime observations, container inventory, port mapping, and ownership pressure.
- **service** hides endpoint evidence, process evidence, systemd evidence,
  container evidence, ownership discrepancy, and attribution uncertainty.
- **network** hides local passive socket observation, active probing, external
  accessibility, DNS validity, and remote reachability.
- **provider** hides metadata recommendation, handoff target, credential boundary,
  external execution, result evidence, and lifecycle ownership.

Unsupported or weakly supported compressed terms:

- **operator authority** appears in documents and examples, but current code
  evidence reviewed here mainly represents approvals/pending actions and policy
  state, not a broad operator-authority subsystem.
- **repository authority** is a work-style/documentation principle, not a runtime
  authority implementation.
- **projection authority** should not be promoted beyond visibility/selection;
  repository evidence repeatedly says projection is not execution authority.

## Recurring authority relationships

The implementation repeatedly demonstrates these relationships:

- **requires**: `ToolExecutor` requires a registered operation; authority slices
  require observations and required authority; policy requires approval or
  confirmation for risk classes.
- **provides**: local passive authority provides listener endpoint observation;
  Docker/root authority provides container runtime observations when available;
  external providers provide execution outside Seed.
- **blocks**: policy blocks unknown/critical actions; unavailable Docker/root
  authority blocks container runtime observation; unauthorized active network
  probing remains out of scope.
- **permits/allows**: policy allows low-risk read-only actions and approved
  actions; authority profiles allow reachable observations.
- **records**: execution records tool-call events; diagnostic recording records
  diagnostic facts under diagnostic scope.
- **limits**: diagnostic inventory limits record scope and mutation; listener
  endpoint authority limits conclusions to local endpoint facts; context views
  limit providers to selected projected facts.
- **delegates**: provider boundary delegates actual execution, credentials,
  retries, schedules, and job lifecycle to external providers.
- **consumes**: Tool execution consumes registry specs, state, policy, and
  validation; authority slices consume observation inventory/domains, privilege
  discovery, ownership discrepancies, and capability needs as evidence.

## How authority is exposed

Current implementation exposes authority as multiple shapes:

- **status**: `allow`, `block`, `require_confirmation`, `require_approval`,
  `approved`, `blocked`, `reachable`, `partially_reachable`, `unknown`.
- **relationship**: requires registered operation, required observation,
  required authority, reachable/blocked observation, provider boundary.
- **boundary**: read-only flags, no recording, no provider acquisition, no
  permission creation, no event write, no cluster mutation, no ownership
  inference.
- **capability**: capability needs, observation capabilities, registered
  operations, and provider/handoff recommendations.
- **execution prerequisite**: registry membership, validation, policy decision,
  approval/pending-action status.
- **observation prerequisite**: local passive access, Docker socket/root access,
  lack of active probe authorization, external-provider query uncertainty.

## Counterexamples and contradictions

- The word `authority` appears in many investigations and conceptual documents;
  those usages are not implementation-backed unless tied to code, registry
  entries, CLI surfaces, or tests.
- Projection is repeatedly visible and central, but implementation contradicts
  treating projection as execution or mutation authority.
- Documentation/navigation authority is real for repository maintenance but is
  not equivalent to runtime or provider authority.
- Operator authority is under-specified in implementation compared with policy
  decisions and pending-action approvals.
- Provider authority is strongly represented as a boundary but less uniformly
  represented as executable code because real execution is intentionally outside
  Seed.
- Authority is not consistently represented across subsystems as a single object
  or schema; each subsystem uses the representation that fits its boundary.

## Supported conclusions

1. Existing implementation already contains multiple authority concepts; the
   repository has not compressed authority into one model.
2. The strongest implementation-backed authority classes are registered execution,
   policy decision, diagnostic recording/mutation boundary, observation
   prerequisite, ownership/attribution boundary, provider boundary, and projection
   non-authority.
3. Broad terms such as `root`, `docker`, `service`, `network`, `provider`, and
   `execution` already decompose into narrower responsibilities.
4. Authority is consistently conservative across subsystem boundaries: read-only
   surfaces do not become mutation authority, projections do not become execution
   authority, recommendations do not become provider execution, and diagnostics do
   not become cluster truth.
5. Authority is inconsistently shaped across implementations; this is a recovery
   finding, not a defect by itself.

## Unsupported conclusions

- There is no evidence for a single canonical authority ontology in the current
  implementation.
- There is no evidence that root or Docker access grants global authority.
- There is no evidence that service endpoint observation grants service ownership.
- There is no evidence that projection/cache/context visibility grants execution,
  mutation, or credential authority.
- There is no evidence that Seed owns provider credentials, retry loops,
  schedules, or long-running job lifecycle.
- There is no evidence that diagnostic recording should attach diagnostic-only
  findings directly to hosts, services, filesystems, or runtime entities.

## Recommended next investigation

The next recovery step should be an implementation-only comparison of all
surfaces that emit authority-like status values. Start with `ToolExecutor`,
`PolicyGate`, `PendingActionService`, diagnostic inventory/shape audit,
`container_ownership_authority`, `service_ownership_authority`,
`listener_endpoint_authority`, observation permission/privilege discovery, and
capability/provider recommendation code. The question should be narrow:

> Which status vocabularies are implementation-backed, where are they consumed,
> and which of them are only presentation labels?

This would preserve the current recovery boundary while avoiding a new authority
framework or taxonomy proposal.
