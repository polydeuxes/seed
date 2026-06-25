---
doc_type: reconciliation
status: implementation-backed finding
scope: container ownership authority, service ownership authority, emergent inquiry shapes
---

# Inquiry shapes emerged reconciliation

## Central answer

After two authority-aware implementations, Seed has implementation-backed evidence for one stable inquiry-state discipline and two naturally different inquiry shapes.

What stayed the same:

```text
desired observation
current strategy
required observations
required authority
available authority
strategy status
remaining observations
uncertainty
remaining uncertainty
boundary
```

What changed naturally:

```text
strategy shape
reachability shape
observation composition
authority composition
```

The strongest supported statement is:

```text
The inquiry-state discipline remained stable.
The inquiry shape varied naturally.
```

This report does not recommend a generalized implementation, shared interface, base class, planner, presentation framework, conversation runtime, or inquiry framework. It preserves only what the two implementations already show.

## Files inspected

Required implementation files:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`

Reconciliation documents inspected where useful:

- `docs/container_ownership_authority_minimal_slice_findings.md`
- `docs/service_ownership_authority_reuse_findings.md`
- `docs/bounded_inquiry_subsystem_collaboration_reconciliation.md`
- `docs/presentation_conversation_responsibility_reconciliation.md`

## 1. Implementation-backed inquiry shapes now present

### Single-strategy inquiry: container ownership

`container ownership` is implemented as a single container-runtime strategy.

Implementation evidence:

- The desired observation is fixed to `container ownership`.
- The current strategy is fixed to `container_runtime_observation`.
- The required observations are limited to `container_inventory` and `container_port_mapping` when both map to the `container_runtime` domain.
- Both observations are evaluated against the same required authority class, `docker_group_or_root`.
- Under the constrained profile, the strategy reports `blocked`.

This shape is single-strategy because the evaluator has one named strategy and one authority class governing all required observations. The implementation does not branch into independent local, systemd, listener, provider, or network sub-strategies.

### Composite inquiry: service ownership

`service ownership` is implemented as a composite local service attribution strategy.

Implementation evidence:

- The desired observation is fixed to `service ownership`.
- The current strategy is fixed to `composite_local_service_attribution_observation`.
- The required observations include local listener evidence, listener-process evidence, systemd-unit evidence, and container-runtime evidence.
- Required authority differs by observation: local listener and systemd evidence are local-passive, listener process evidence is partial non-root under local passive authority, and container-runtime observations remain Docker/root dependent.
- Under the constrained profile, the strategy reports `partially_reachable`.

This shape is composite because the evaluator holds multiple observation families together in one service-ownership answer and distinguishes reachable local evidence from blocked container-runtime evidence.

## 2. Implementation-backed reachability shapes now present

### Fully blocked

The container ownership slice demonstrates a fully blocked reachability shape under the constrained profile.

Evidence:

- `root` is unavailable.
- `docker_socket_read` is unavailable.
- Both required observations require `docker_group_or_root`.
- `outcome` and `strategy_status` are `blocked`.
- `remaining_observations` are the same required observations.
- A Docker/root blocking boundary is emitted.

No reachable observation subset is exposed for container ownership because the single strategy depends entirely on Docker/root container-runtime authority.

### Partially reachable

The service ownership slice demonstrates a partially reachable reachability shape under the same constrained profile.

Evidence:

- Local listener, listener-process, and systemd observations are reachable.
- Container inventory and container port mapping are blocked.
- `outcome` and `strategy_status` are `partially_reachable`.
- `remaining_observations` equal `blocked_observations`.
- The same Docker/root blocking boundary is emitted for the blocked container-runtime portion.

No broader reachability shapes should be inferred from these two examples. Current implementation evidence supports only the fully blocked and partially reachable shapes described above.

## 3. Inquiry-state fields stable across both implementations

The following fields are implementation-backed in both dataclasses, JSON shapes, and tests:

| Stable field | Container ownership evidence | Service ownership evidence |
| --- | --- | --- |
| `desired_observation` | Fixed to `container ownership`. | Fixed to `service ownership`. |
| `current_strategy` | `container_runtime_observation`. | `composite_local_service_attribution_observation`. |
| `required_observations` | Container inventory and container port mapping. | Listener, listener-process, systemd, and container-runtime observations. |
| `required_authority` | Per-observation Docker/root guidance. | Per-observation local-passive, partial-non-root, and Docker/root guidance. |
| `available_authority` | Normalized constrained profile keys. | Same normalized constrained profile keys. |
| `outcome` | `blocked` under constrained profile. | `partially_reachable` under constrained profile. |
| `strategy_status` | Mirrors `outcome`. | Mirrors `outcome`. |
| `remaining_observations` | Same as all required observations when blocked. | Same as blocked observations when partially reachable. |
| `uncertainty` | Preserves unknown provider/local-passive insufficiency/profile-authority notes. | Preserves inventory/domain/authority-boundary notes. |
| `remaining_uncertainty` | Equals `uncertainty`. | Equals `uncertainty`. |
| `blocking_boundary` | Present when Docker/root container-runtime authority is unavailable. | Present when Docker/root container-runtime authority blocks the container portion. |
| `boundary` | Read-only, no records, no event-ledger write, no cluster mutation, no provider acquisition, no permission creation, no observation execution. | Same boundary discipline. |

The stable fields are not merely prose similarities. They are returned by both implementations and asserted by both test suites.

## 4. Parts that naturally differed

### Strategy shape differed architecturally

Container ownership is a single-strategy inquiry. Service ownership is a composite inquiry. This difference is architectural in the narrow observational sense because it follows from the desired observation and required evidence shape:

- Container ownership currently needs only container-runtime observations in the implemented slice.
- Service ownership currently needs a local service attribution composition: listener, process, systemd, and container-runtime observations.

This report does not convert that difference into a taxonomy. It records that the two implemented inquiries have different shapes.

### Reachability differed architecturally

Container ownership is fully blocked under the constrained profile. Service ownership is partially reachable under the same profile.

This is architectural in the narrow observational sense because the difference comes from implementation-backed authority composition:

- Container ownership required observations all need Docker/root authority.
- Service ownership includes local-passive and partial-non-root evidence in addition to Docker/root-dependent container evidence.

### Observation composition differed architecturally

Container ownership uses two container-runtime observations. Service ownership uses five observations spanning local listener, process, systemd, and container-runtime evidence.

This is not a presentation difference. It is encoded in implementation constants and preserved in JSON/tests.

### Authority composition differed architecturally

Container ownership has one effective required authority class for all required observations: `docker_group_or_root`.

Service ownership has mixed authority requirements: `local_passive`, `partial_non_root`, and `docker_group_or_root`.

This difference is implementation-backed because each evaluator maps required observations to authority before reachability is determined.

### Formatting details differed implementation-specifically

The human CLI sections differ slightly because service ownership displays reachable and remaining observation state, while container ownership displays remaining work after execution status. That is an implementation-specific rendering difference, not evidence for a new architecture.

## 5. Did either implementation require new subsystems, authority domains, frameworks, or presentation frameworks?

No.

Neither implementation required:

```text
new subsystem
new authority domain
new inquiry framework
new presentation framework
planner
conversation runtime
```

Implementation evidence:

- Both evaluators are narrow read-only authority slices.
- Both reuse existing authority/profile vocabulary: `root`, `docker_socket_read`, `active_network_probe`, `local_passive`, and `external_provider_query`.
- Both reuse existing privilege guidance rather than adding a new authority domain.
- Both expose CLI/JSON diagnostics through existing diagnostic inventory and shape-audit mechanisms.
- Both preserve read-only boundary flags and prove no state, approval, event-ledger, provider-acquisition, permission-creation, or observation-execution behavior.

The service slice expanded the observation composition, not the authority domain model.

## 6. Is the stability/variation statement supported?

Yes, with the repository-bound wording below:

```text
The inquiry-state discipline remained stable.
The inquiry shape varied naturally.
```

Supported meaning:

- Both implementations preserve a bounded current answer: desired observation, strategy, required observations, required authority, available authority, status, remaining observations, uncertainty, and boundary.
- Container ownership naturally became a single-strategy/fully-blocked inquiry.
- Service ownership naturally became a composite/partially-reachable inquiry.
- The variation appeared without adding a generic inquiry runtime, planner, presentation framework, or new authority domain.

Unsupported meaning:

- These two implementations do not prove a complete taxonomy of inquiries.
- These two implementations do not prove that a shared interface, base class, or generalized runtime should be introduced.
- These two implementations do not prove every future authority-aware inquiry will fit these shapes.

## 7. Recurring implementation pressures in both slices

Only implementation-backed recurring pressures are listed here.

### Supplied authority profile must remain authoritative

Both slices evaluate reachability from the supplied constrained profile instead of inferring permission from existing approvals or creating authority.

### Docker/root container-runtime boundary recurs

Both slices encounter the same Docker/root boundary for `container_inventory` and `container_port_mapping`.

### Read-only diagnostics must not become cluster truth

Both slices preserve the same non-mutating boundary:

```text
read_only=true
records=false
writes_event_ledger=false
mutates_cluster=false
provider_acquisition=false
permission_creation=false
executes_observation=false
```

### Remaining observations are preserved instead of hidden

Both slices keep unperformed observations visible:

- Container ownership keeps all required observations as remaining when fully blocked.
- Service ownership keeps only blocked observations as remaining when partially reachable.

### Uncertainty remains explicit

Both slices preserve `uncertainty` and `remaining_uncertainty` instead of converting uncertainty into inferred ownership truth.

## Strongest supporting evidence

1. Both implementations expose the same core inquiry-state fields in their dataclasses and JSON payloads.
2. Both test suites assert desired observation, current strategy, strategy status, remaining observations, uncertainty preservation, and non-mutating boundary behavior.
3. The container implementation proves a single-strategy shape because all required observations are container-runtime observations requiring Docker/root authority.
4. The service implementation proves a composite shape because one bounded desired observation combines listener, process, systemd, and container-runtime observations.
5. The same constrained authority profile yields different reachability outcomes, showing that reachability follows observation/authority composition rather than a hard-coded universal answer.
6. Diagnostic inventory and shape-audit tests cover both surfaces without adding a new diagnostic framework.

## Strongest contradictory or limiting evidence

1. There are only two implementation-backed examples. That is enough to recognize recurrence, but not enough to define broader architectural patterns.
2. The recurring state discipline is currently duplicated in two narrow evaluators, not held by a generalized runtime object.
3. Service ownership has fields that container ownership does not need, such as `reachable_observations` and `blocked_observations`; container ownership has no explicit reachable subset because its constrained result is fully blocked.
4. The current examples are both ownership-oriented authority slices, so they do not prove that non-ownership inquiries will preserve the same field set.
5. The documents reviewed warn against promoting presentation vocabulary or collaboration language into implementation truth without source evidence.

## Have recurring inquiry shapes begun to appear?

Yes, but only modestly.

The two slices are not unrelated implementations. They independently preserve the same inquiry-state discipline and both respect the same authority/profile/boundary pressures. They also differ in meaningful implementation-backed ways: one is single-strategy and fully blocked; the other is composite and partially reachable.

The current evidence supports this cautious conclusion:

```text
Implementation has begun revealing recurring inquiry-state discipline
and at least two naturally different inquiry shapes.
```

It does not support this stronger conclusion:

```text
Seed now has enough evidence to define a generalized inquiry architecture.
```

## Are we ready to continue implementing?

Yes. The repository is ready to continue implementing bounded authority-aware inquiry slices.

No additional framework work is needed before continuing. Additional examples would be valuable before recognizing broader architectural patterns, especially examples outside ownership or examples with different authority mixtures. The next implementation should remain a bounded slice that preserves discovered state fields and lets the shape emerge from implementation.

## Recommended next implementation slice

Recommended next implementation slice:

```text
storage/filesystem ownership or local runtime ownership under constrained authority
```

Reason:

- It remains close to the active mission: what Seed can learn without root, Docker, or network probing.
- It is likely to exercise local-passive versus privileged filesystem/process evidence without inventing a new framework.
- It can test whether the stable inquiry-state discipline survives outside the container/service ownership pair.

This is a recommendation for the next bounded implementation target only, not a recommendation to generalize or introduce shared infrastructure.

## Files changed

- `docs/inquiry_shapes_emerged_reconciliation.md`

## LOC changed

- Added one report file, 334 lines.

## Tests run

- `pytest -q tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py`
