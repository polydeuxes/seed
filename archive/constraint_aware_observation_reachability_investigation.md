# Constraint-Aware Observation Reachability Investigation

## Current capability-under-constraint question

The mission is **capability under constraint**. The goal is to help Seed answer what remains observable when authority is denied.

The missing operator question is not primarily:

```text
How do we expose relationship chains?
```

It is:

```text
Given denied or unavailable authority, what observation paths remain reachable?
```

A relationship-chain view may explain why a capability matters, but reachability under constraint must also know the current authority state, the authority each observation path requires, the observation evidence still available, and the reason a path is unreachable.

## Scenario tested

Explicit constraint profile used for this investigation:

| Authority / observation class | Scenario state |
| --- | --- |
| `root` | `unavailable` |
| `docker` | `unavailable` |
| `network_active` | `unauthorized` |
| `external_provider_query` | `allowed` or `unknown` |
| `local_passive` | `allowed` |

Required operational targets:

| Target | Constraint-aware expectation |
| --- | --- |
| local listener visibility | Local passive listener evidence may remain reachable, but process/owner attribution may be partial without root or privileged process visibility. |
| service ownership attribution | Partially reachable when listener/service evidence exists; still may leave `owner_not_observed` without listener-process or container evidence. |
| container runtime visibility | Unreachable when both Docker and root are unavailable unless another provider exists. |
| container inventory | Unreachable under Docker/root denial for Docker-backed inventory. |
| container port mapping | Unreachable under Docker/root denial for Docker-backed port mapping. |
| neighbor table / passive local network evidence | Reachable if local passive reads are allowed; no active probing implied. |
| active network probing | Blocked because `network_active` is unauthorized. |

## Current surfaces inspected

Implementation and tests inspected:

- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/observation_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_privilege_discovery.py`
- `tests/test_observation_domains.py`
- `tests/test_observation_permission.py`
- `tests/test_capability_relationship.py`
- `tests/test_observation_inventory.py`
- `tests/test_diagnostic_inventory.py`

Supporting documents inspected:

- `docs/observation_relationship_visibility_gap_investigation.md`
- `docs/observation_relationship_chain_requirements.md`
- `docs/observation_domain_permission_authority_reuse_investigation.md`

## What Seed can currently answer

### 1. Current capability pressure

Seed can derive capability pressure from ownership discrepancies. `ownership_discrepancies` maps ownership conflicts to candidate capabilities such as `listener_process_inventory`, `container_inventory`, and `container_port_mapping`; `capability_needs` aggregates those records by capability, subjects, diagnostics, and needed evidence.

This supports answers such as:

```text
Which missing capabilities are currently pressured by owner attribution gaps?
```

### 2. Domain visibility without constraint propagation

Seed can classify observation domains from inventory evidence and capability pressure. `observation_domains` maps `listener_process_inventory` to `local_listeners`, maps `container_inventory` and `container_port_mapping` to `container_runtime`, and classifies domains as `observed`, `partially_observed`, `unobserved`, or `unknown` based on provider families and pressure.

This partially supports answers such as:

```text
Is container_runtime currently unobserved?
Is local_listeners partially observed?
```

### 3. Permission status for selected observation activities

Seed can report permission state for selected observation activities: `neighbor_table_read`, `traffic_capture`, `active_network_probe`, `docker_socket_read`, and `external_provider_query`. The surface distinguishes `granted`, `requires_operator_expression`, `denied`, and `unknown`, but in current implementation it primarily derives reusable grants from approvals and otherwise reports `requires_operator_expression` for known domains.

This partially supports answers such as:

```text
Does Seed have reusable approval for active_network_probe or docker_socket_read?
```

### 4. Access guidance for capabilities

Seed can report implementation-backed access guidance for capability needs. `privilege_discovery` says `listener_process_inventory` is `partial_non_root`, while `container_inventory` and `container_port_mapping` require `docker_group_or_root`.

This supports answers such as:

```text
What access class is associated with container_inventory?
```

### 5. Capability/access/benefit co-location

Seed can co-locate capability pressure, access guidance, and operational benefit through `capability_relationship`. This is the strongest existing surface for explaining why a capability matters, but it leaves attainability and expectation as `unknown`.

This partially supports answers such as:

```text
Why does container_inventory matter operationally?
```

## What Seed cannot currently answer

### 1. Can Seed currently represent an authorization/constraint profile?

**No, not as the scenario requires.**

Seed can represent approvals and selected observation permission states, but there is no first-class read-model input or stored diagnostic shape for a profile such as:

```text
root denied
docker denied
network_active denied
local_passive allowed
external_provider_query unknown
```

`observation_permission` can show whether a reusable approval is observed for known observation activities. It does not accept or synthesize a multi-authority constraint profile containing denied/unavailable root, Docker, and network-active authority.

### 2. Can Seed currently propagate that profile across observation capabilities?

**No.**

Seed has pieces of the propagation path:

```text
container_inventory -> docker_group_or_root
container_inventory -> container_runtime
docker_socket_read -> local_privileged
active_network_probe -> network_active
```

But no current surface evaluates:

```text
root unavailable + docker unavailable => container_inventory unreachable
network_active unauthorized => active_network_probe blocked
local_passive allowed => neighbor_table_read reachable
```

The current implementation can show access context and permission context separately; it does not compute reachability outcomes.

### 3. Can Seed distinguish the required unobserved states?

**Only partially.**

| Required distinction | Current support | Gap |
| --- | --- | --- |
| unobserved because no provider exists | Partial. `observation_inventory` exposes provider/predicate/family existence, and `observation_domains` can say no container observation family is observed. | No explicit reachability reason category `no_provider`. |
| unobserved because required authority is denied | Not supported. | No profile propagation from denied root/Docker/network-active authority to observation paths. |
| partially observed because local passive evidence exists | Partial. `observation_domains` can classify `local_listeners` as `partially_observed` when listener evidence and pressure coexist. | It does not tie the classification to `local_passive=allowed` or enumerate remaining reachable paths. |
| blocked because authorization is missing | Partial. `observation_permission` reports `requires_operator_expression` when approval is absent. | It does not mark affected capabilities as blocked, and does not distinguish denied/unavailable from not-yet-expressed authorization. |
| unknown because repository evidence is insufficient | Partial. Unknown domain handling exists in `observation_domains` and `observation_permission`. | Unknown is not applied as a reachability outcome across capabilities. |

### 4. Can Seed answer inverse operator questions?

**No, not reliably.**

Current surfaces can help manually reconstruct partial answers, but Seed cannot directly answer:

- `Why is container_runtime still unobserved?`
- `Why does owner_not_observed remain?`
- `What observation path is blocked?`
- `What remains observable without Docker?`
- `What would become observable if Docker authorization were granted?`

The reason is that these are inverse reachability questions, not only relationship visibility questions. They require a model that joins:

```text
current constraint profile
+ observation path requirements
+ provider availability
+ permission state
+ domain evidence
+ capability pressure
=> reachable / partially_reachable / unreachable / blocked / unknown
```

## Reachability gaps by required target

| Target | Current answer | Missing reachability answer under scenario |
| --- | --- | --- |
| local listener visibility | Domain can be `partially_observed`; listener process inventory has `partial_non_root` guidance. | Which local-passive listener observations remain reachable without root, and which owner-attribution edges remain unreachable. |
| service ownership attribution | `owner_not_observed` can create capability needs. | Whether remaining unresolved ownership is due to denied authority, absent provider, partial evidence, or insufficient repository evidence. |
| container runtime visibility | `container_runtime` can be `unobserved` with container capability pressure. | Explicit statement that Docker/root-denied scenario makes Docker-backed runtime paths unreachable. |
| container inventory | Capability access guidance says `docker_group_or_root`. | Direct propagation from Docker/root unavailable to `unreachable`. |
| container port mapping | Capability access guidance says `docker_group_or_root`. | Direct propagation from Docker/root unavailable to `unreachable`. |
| neighbor table / passive local network evidence | Permission class maps `neighbor_table_read` to `local_passive`. | Direct answer that this remains reachable when `local_passive=allowed`, provided a provider exists or provider status is known. |
| active network probing | Permission class maps `active_network_probe` to `network_active`. | Direct answer that it is blocked because `network_active=unauthorized`. |

## Distinction between relationship visibility and reachability reasoning

The previous relationship visibility work correctly identified that relationships are fragmented across surfaces. The relationship-chain proposal would solve part of the problem: it would make capability, domain, permission-activity, and operational-benefit links easier to inspect.

However, **the previous relationship-chain proposal does not by itself solve the actual mission**. It only solves part of it.

The mission requires Seed to answer what remains observable when authority is denied. That requires reachability classification, not merely chain visibility. A chain like:

```text
container_inventory -> container_runtime -> docker_socket_read -> local_privileged
```

still does not answer:

```text
Given docker=unavailable and root=unavailable, is container_inventory reachable?
```

unless Seed also has a constraint profile and a reachability evaluator that can classify the path.

## Candidate implementation targets

| Candidate | Fit for mission | Risk / limitation | Assessment |
| --- | --- | --- | --- |
| Extend `observation_domains` with reachability classification | Good domain-level home for `observed`, `partially_observed`, `unreachable`, `blocked`, and `unknown`. | Could overload a domain visibility surface with authority state unless profile input is explicit and narrow. | Plausible if kept domain-scoped and read-only. |
| Extend `privilege_discovery` with denied/unavailable inputs | Good fit for root/Docker access constraints tied to capability guidance. | Privilege is not the same as observation permission; network-active authorization and local-passive reachability do not fit cleanly. | Useful ingredient, not sufficient alone. |
| Add a narrow `observation_reachability` read model | Best fit for the operator question. It can join profile, provider/domain evidence, capability pressure, access guidance, and permission activity without mutating cluster state. | New diagnostic surface requires inventory and shape-audit work if exposed as CLI. Must avoid becoming planning/authorization system. | Recommended smallest conceptual target. |
| Extend `capability_relationship` only after reachability exists | Good presentation target once reachability rows exist. | If extended first, it repeats the previous chain-first error and still cannot classify denied authority outcomes. | Defer until reachability classification exists. |
| Reuse `observation_permission` as authority-state input | Good source for observation activity approval state and class vocabulary. | Current surface does not model root/Docker availability and does not accept denied/unavailable scenario inputs. | Reuse as input, not as the whole answer. |
| Do nothing yet; document missing model first | Safe and consistent with this task. | Does not improve runtime answers. | Appropriate for this investigation; next slice should be implementation-backed. |

## Recommended smallest next slice

Add a narrow read-only reachability model before expanding relationship-chain output.

Proposed smallest implementation requirement:

```text
Given an explicit constraint profile, classify supported observation paths as:
reachable
partially_reachable
unreachable_authority_unavailable
blocked_authorization_missing
no_provider
unknown
```

Initial supported paths should be deliberately small and implementation-backed:

| Observation path | Required authority / evidence | Scenario outcome |
| --- | --- | --- |
| `local_listener_visibility` | local passive listener provider/evidence; root optional for full process ownership | `partially_reachable` when local passive allowed but root unavailable. |
| `listener_process_inventory` | non-root partial; root/privileged process visibility for full attribution | `partially_reachable` or `unreachable_authority_unavailable` for full attribution. |
| `container_inventory` | Docker socket/group or root-equivalent visibility | `unreachable_authority_unavailable`. |
| `container_port_mapping` | Docker socket/group or root-equivalent visibility | `unreachable_authority_unavailable`. |
| `neighbor_table_read` | `local_passive` allowed plus provider support | `reachable` or `unknown` if provider evidence is absent/insufficient. |
| `active_network_probe` | `network_active` authorization | `blocked_authorization_missing`. |
| `external_provider_query` | external provider permission allowed/unknown plus provider configuration | `reachable` or `unknown`, depending on repository evidence. |

This can begin as an internal helper plus focused tests. If exposed as a CLI diagnostic, it must be registered in diagnostic inventory and diagnostic shape audit, and tests must prove read-only boundaries.

## Files likely touched

If implemented later, likely files:

- `seed_runtime/observation_reachability.py` for the narrow read model.
- `seed_runtime/observation_domains.py` only if domain output consumes reachability classifications.
- `seed_runtime/privilege_discovery.py` only if denied/unavailable profile inputs are added there.
- `seed_runtime/observation_permission.py` only if reusable permission state is exposed as structured input to reachability.
- `seed_runtime/capability_relationship.py` only after reachability rows exist and need operator-facing explanation.
- `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py` if a new or changed diagnostic surface is exposed.
- Tests under `tests/test_observation_reachability.py` or focused existing test files.

## Tests required

If the next slice exposes a diagnostic surface, required tests:

- Constraint profile can represent `root=unavailable`, `docker=unavailable`, `network_active=unauthorized`, `external_provider_query=unknown|allowed`, and `local_passive=allowed`.
- `container_inventory` is classified as unreachable when Docker and root are unavailable.
- `container_port_mapping` is classified as unreachable when Docker and root are unavailable.
- `active_network_probe` is classified as blocked when `network_active` is unauthorized.
- `neighbor_table_read` remains reachable or explicitly unknown under `local_passive=allowed`, depending on provider evidence.
- Local listener visibility is partial when non-root/local-passive evidence remains but root-dependent attribution is unavailable.
- `owner_not_observed` can be traced to remaining blocked/unreachable/partial observation paths without attaching diagnostic findings to service or runtime entities as cluster truth.
- Diagnostic inventory includes the surface.
- Diagnostic shape audit checks the surface.
- Read-only boundaries remain `writes_event_ledger=false` and `mutates_cluster=false` unless recording is explicitly added later.

Per repository visibility contract, run:

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

and add/run the focused reachability tests if implementation occurs.

## Risks

- Reintroducing a generic relationship-chain feature before modeling reachability would miss the mission.
- Treating `requires_operator_expression` as the same as `denied` would blur authorization states.
- Treating Docker/root unavailability as a permanent fact about the cluster would violate the diagnostic recording boundary.
- A broad authorization/enforcement mechanism would exceed scope.
- Active network probing must not be performed to prove reachability.
- Docker probing and root probing must not be performed to prove the denied/unavailable scenario.
- Provider absence, authority denial, and insufficient repository evidence must remain distinct.

## Non-goals

- No new ontology.
- No generic relationship catalog.
- No planning system.
- No authorization enforcement.
- No approval mechanism.
- No observation provider.
- No root probing.
- No Docker probing.
- No network probing.
- No cluster mutation.
- No diagnostic facts attached directly to operational entities as cluster truth.
- No broad answer-formatting work.

## Rollback path

This investigation only adds documentation. Rollback is removing this file.

For the future implementation slice, rollback should be straightforward if it remains a read-only helper or diagnostic:

- Remove `observation_reachability` helper/CLI.
- Remove diagnostic inventory and shape-audit entries.
- Remove focused tests.
- Leave existing `observation_domains`, `observation_permission`, `privilege_discovery`, `capability_needs`, `capability_relationship`, and `ownership_discrepancies` behavior unchanged.

## Report

### Files inspected

See [Current surfaces inspected](#current-surfaces-inspected).

### Files changed

- `docs/constraint_aware_observation_reachability_investigation.md`

### LOC changed

- Documentation-only addition: 367 lines at creation time.

### Tests run

- `python -m pytest -q tests/test_observation_domains.py tests/test_observation_permission.py tests/test_privilege_discovery.py tests/test_capability_relationship.py tests/test_observation_inventory.py`
- `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

### Recommended next step

Implement a narrow, read-only `observation_reachability` model that accepts an explicit constraint profile and classifies the small supported observation paths above. Only after that exists should `capability_relationship` or relationship-chain output be extended to explain the reachability result.
