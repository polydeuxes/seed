---
doc_type: reconciliation
status: implementation-backed finding
scope: bounded inquiry identity, bounded inquiry state, authority-aware ownership slices, claim-state comparison
---

# Bounded inquiry identity/state reconciliation

## Central answer

Current implementation evidence supports a narrow distinction between bounded inquiry identity and bounded inquiry state.

The two reviewed authority slices preserve inquiry identity through stable bounded-inquiry fields:

```text
desired_observation
current_strategy
required_observations
required_authority
read-only boundary discipline
```

The same slices expose current inquiry state through fields that legitimately vary when authority or observation reachability varies:

```text
available_authority
reachable_observations
blocked_observations
remaining_observations
strategy_status
outcome
blocking_boundary
uncertainty
remaining_uncertainty
```

The strongest supported statement is:

```text
For the current container-ownership and service-ownership authority slices,
the bounded inquiry preserves its implemented identity while its current state changes.
```

This report does not propose an inquiry state machine, runtime, planner, workflow, conversation engine, generic state framework, or shared base class.

## Files inspected

Required implementation and tests:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`

Supporting documents and implementation inspected where useful:

- `docs/current_strategy_bounded_inquiry_reconciliation.md`
- `docs/inquiry_shapes_emerged_reconciliation.md`
- `docs/inquiry_state_reasoning_reconciliation.md`
- `docs/knowledge_change_and_revision_reconciliation.md`
- `seed_runtime/knowledge/self_model_alignment.py`
- `tests/test_self_model_alignment.py`
- `tests/test_existence_claim_reconciliation.py`
- `tests/test_structure_claim_reconciliation.py`

## 1. Stable fields during the lifetime of the bounded inquiry

### Container ownership

The container slice fixes its inquiry identity in module-level constants and returns those constants through a frozen result dataclass:

- `DESIRED_OBSERVATION = "container ownership"`.
- `CONTAINER_OBSERVATIONS = ("container_inventory", "container_port_mapping")`.
- `CURRENT_STRATEGY = "container_runtime_observation"`.
- `BLOCKING_BOUNDARY = "docker_or_root_container_runtime_authority_unavailable"`.

The evaluator computes `required_observations` by filtering the fixed container observation set through the existing `container_runtime` domain mapping, and computes `required_authority` from privilege guidance for those required observations. Under the current implementation, that means the inquiry remains about container ownership, uses container-runtime observation, and requires the same container-runtime observations and Docker/root authority class.

Tests assert the stable identity fields directly: `desired_observation == "container ownership"`, `current_strategy == "container_runtime_observation"`, required observations include `container_inventory` and `container_port_mapping`, and both required authority entries are `docker_group_or_root`.

### Service ownership

The service slice similarly fixes its inquiry identity in module-level constants and returns them through a frozen result dataclass:

- `DESIRED_OBSERVATION = "service ownership"`.
- `SERVICE_OBSERVATIONS` includes listener, listener-process, systemd-unit, and container-runtime observations.
- `CURRENT_STRATEGY = "composite_local_service_attribution_observation"`.
- `BLOCKING_BOUNDARY = "docker_or_root_container_runtime_authority_unavailable"`.

The evaluator derives `required_observations` from the bounded service observation set and existing capability-needs/domain evidence, then derives `required_authority` per observation. The resulting inquiry remains service ownership using one composite local service attribution strategy; authority changes do not replace that strategy.

Tests assert the stable identity fields directly: `desired_observation == "service ownership"`, `current_strategy == "composite_local_service_attribution_observation"`, local listener/systemd observations remain required local-passive evidence, and container observations remain Docker/root dependent.

### Stable identity conclusion

Implementation supports these as stable bounded-inquiry identity fields for the reviewed slices:

| Field | Why it is identity-like in current implementation |
| --- | --- |
| `desired_observation` | Fixed by module constant and asserted by tests. |
| `current_strategy` | Fixed by module constant and returned directly; recent reconciliation already found it is determined by the bounded inquiry, not selected among alternatives. |
| `required_observations` | Determined from the bounded inquiry's implemented observation set and repository mappings, not from current authority availability. |
| `required_authority` | Determined from required observations and privilege guidance, not from whether that authority is available now. |
| `boundary` | Both slices remain read-only diagnostics with no records, event-ledger writes, cluster mutation, provider acquisition, permission creation, or observation execution. |

`required_observations` and `required_authority` are stable only within the current implemented bounded inquiry and repository mappings. They are not eternal ontology claims; a code change or repository-authority change could change them.

## 2. Fields that legitimately change as authority or observation availability changes

### Authority-driven variable state

Both evaluators normalize the supplied profile into `available_authority`. That field is current state because the supplied profile is the authority decision source for the diagnostic, and tests change it to prove different outcomes.

Container ownership demonstrates authority-driven changes:

- With `root=unavailable` and `docker_socket_read=unavailable`, the outcome is `blocked`, `strategy_status` mirrors `blocked`, `remaining_observations` are both required container observations, and `blocking_boundary` is present.
- When `docker_socket_read` is changed to `available`, the same inquiry and strategy remain in place, but `outcome` changes to `unknown`, `strategy_status` mirrors `unknown`, `blocking_boundary` is absent, and JSON omits `blocking_boundary`.

Service ownership demonstrates authority-driven changes with a richer current-state shape:

- Under the constrained profile, local observations are reachable, container observations are blocked, `outcome` is `partially_reachable`, `remaining_observations == blocked_observations`, and the Docker/root blocking boundary is present.
- When `docker_socket_read` is changed to `available`, blocked and remaining observations become empty, `blocking_boundary` is absent, and the outcome becomes `reachable` in the direct evaluator test.

### Observation-availability-driven variable state

The service implementation exposes observation state explicitly with `reachable_observations` and `blocked_observations`. Reachability changes as current authority allows or blocks each required observation:

- `tcp_listen_inventory` and `systemd_unit_inventory` are reachable when local passive authority is available.
- `listener_process_inventory` is reachable when privilege guidance says `partial_non_root` and local passive authority is available.
- Container-runtime observations are blocked when their required authority is `docker_group_or_root` and both root and Docker socket read are unavailable.

The container implementation does not expose a separate `reachable_observations` field, but it still exposes current observation state through `remaining_observations`, `outcome`, `strategy_status`, and `blocking_boundary`.

### Variable state conclusion

Implementation supports these as current inquiry-state fields for the reviewed slices:

| Field | Why it is state-like in current implementation |
| --- | --- |
| `available_authority` | Copied from the supplied profile; tests vary the profile. |
| `reachable_observations` | Service slice computes it from required observations, required authority, and current profile. |
| `blocked_observations` | Service slice computes it from required observations, required authority, and current profile. |
| `remaining_observations` | Container uses all required observations when blocked; service uses blocked observations. |
| `outcome` | Computed from current reachability/blockage. |
| `strategy_status` | Assigned from current `outcome`. |
| `blocking_boundary` | Present only when the current profile blocks Docker/root container-runtime evidence. |
| `uncertainty` / `remaining_uncertainty` | Built from current implementation evidence and unobserved/unevaluated boundaries; tests assert equality in the current slices. |

## 3. Does implementation distinguish identity from current state?

Yes, narrowly and structurally.

The distinction is not implemented as a named `InquiryIdentity` class and `InquiryState` class. It is not a state machine. But it is more than conceptual prose because the dataclasses and evaluators separate fields with different behavior:

- identity-like fields are fixed by constants or bounded observation definitions and do not change when tests vary the authority profile;
- state-like fields are recomputed from the current profile and current reachability;
- tests intentionally vary authority while asserting the same desired observation, current strategy, and required authority remain in place.

The distinction is therefore implementation-backed as a shape and behavior, not as a separately named abstraction.

## 4. Can the statement be supported?

```text
The bounded inquiry
preserves its identity
while its current state
changes.
```

Supported with bounded wording:

```text
For the current container-ownership and service-ownership authority slices,
the bounded inquiry preserves its implemented identity while its current state changes.
```

Support:

- changing Docker socket authority in container ownership changes outcome and blocking boundary, not desired observation or current strategy;
- changing Docker socket authority in service ownership changes reachable/blocked/remaining observations and outcome, not desired observation or current strategy;
- tests assert these behaviors directly.

Unsupported broadening:

- all future inquiries behave this way;
- inquiry identity is a general persisted object;
- inquiry state has lifecycle transitions;
- Seed has an inquiry state machine.

## 5. Do authority changes modify the inquiry, the strategy, or only inquiry state?

In the reviewed implementation, authority changes modify only inquiry state.

Authority changes modify:

- `available_authority`;
- `reachable_observations` and `blocked_observations` where exposed;
- `remaining_observations`;
- `outcome`;
- `strategy_status`;
- `blocking_boundary`.

Authority changes do not modify:

- `desired_observation`;
- `current_strategy`;
- the bounded required-observation set;
- per-observation required authority mapping.

The strongest evidence is the pair of tests that set `docker_socket_read` to `available`: both slices keep the same strategy label and authority semantics while current outcome/blockage fields change.

## 6. Do observation changes modify the inquiry, the strategy, or only inquiry state?

Within the current implementation, observation availability changes modify inquiry state, not the inquiry or strategy.

For service ownership, observation availability is represented by `reachable_observations` and `blocked_observations`, derived from required observations plus current authority. The composite strategy remains `composite_local_service_attribution_observation` whether the container-runtime portion is blocked or not. The bounded inquiry remains `service ownership`.

For container ownership, blocked observation availability is represented through `remaining_observations`, `outcome`, and `blocking_boundary`. The strategy remains `container_runtime_observation`.

The implementation does not show an observation becoming available and thereby selecting a new strategy. It shows the current state of the existing strategy changing.

## 7. Relationship to existing claim-state implementation

There is a genuine architectural similarity, but only at the level of stable subject plus variable reconciliation outcome.

### Claim implementation evidence

`seed_runtime/knowledge/self_model_alignment.py` defines immutable records:

- `DocumentationClaim` preserves claim content, family, source path, and optional source heading.
- `RepositoryArtifactFact` preserves supplied repository artifact evidence.
- `AlignmentRecord` preserves the same `claim`, matched artifact facts, an `outcome`, a `rule_id`, and a `reason`.

`reconcile_claims()` applies deterministic rules and returns an `AlignmentRecord` per supplied claim. The claim object is preserved inside the result while outcome varies according to supplied artifact facts and rule applicability. For example, ownership, existence, structure, rejected-concept, and frontier rules can return `supported`, `missing_support`, `potential_conflict`, or `not_evaluable` without rewriting the claim content.

This is structurally similar to the inquiry slices:

```text
stable claim content + current artifact evidence -> alignment outcome/reason
stable inquiry identity + current authority/reachability -> inquiry outcome/uncertainty
```

### Limits of the similarity

The similarity is not a shared implementation:

- claim reconciliation uses `DocumentationClaim`, `RepositoryArtifactFact`, and `AlignmentRecord`;
- bounded inquiry slices use separate authority-slice dataclasses;
- claim outcomes reconcile documentation claims against repository artifact facts;
- inquiry outcomes expose current reachability and authority state for a diagnostic inquiry.

Therefore the architectural similarity is implementation-backed in shape, not in shared code or shared lifecycle machinery.

## 8. Does the distinction exist?

```text
Claim state
    reconciles reality.

Inquiry state
    preserves Seed's current frame.
```

Current implementation partially supports this distinction if narrowed.

Supported:

- Claim alignment state reconciles supplied documentation claims against supplied repository artifact facts and returns an outcome, rule, and reason. This is a reconciliation of a claim against evidence in the self-model fixture boundary.
- Inquiry state preserves Seed's current bounded frame for the authority question: desired observation, current strategy, required observations, required authority, available authority, current outcome, uncertainty, and read-only boundary.

Not supported as written:

- `reconciles reality` is too broad for the implemented claim path. The self-model alignment module explicitly reconciles supplied fixture records; it does not inspect the repository, project runtime state, or establish direct reality truth.
- `preserves Seed's current frame` is accurate as a description of the authority slices, but not yet a named repository primitive or generic runtime object.

Safer implementation-backed wording:

```text
Claim alignment state reconciles a preserved claim against supplied evidence.
Bounded inquiry state preserves the current evidence-backed frame of a bounded authority inquiry.
```

## Strongest supporting evidence

1. Both authority slices define stable desired-observation and current-strategy constants.
2. Both authority slices compute current state from a supplied authority profile.
3. Tests vary Docker socket authority and prove outcomes/boundaries change while strategy labels remain stable.
4. Service ownership explicitly separates `reachable_observations`, `blocked_observations`, and `remaining_observations` from fixed desired observation and current strategy.
5. Both slices keep read-only diagnostic boundaries and prove no state/event/approval mutation.
6. Claim alignment preserves `DocumentationClaim` inside `AlignmentRecord` while outcome/reason vary from reconciliation rules and supplied facts.

## Strongest contradictory evidence

1. There is no named `InquiryIdentity` or `InquiryState` implementation.
2. The authority-slice dataclasses combine stable and variable fields in one result object.
3. `required_observations` can be derived from current repository state in service ownership via capability needs, so it is stable only as part of the bounded implemented inquiry, not as a timeless identity field.
4. `current_strategy` uses the word `current`, which could imply selection or temporal transition, but implementation shows a fixed label rather than a selected strategy.
5. Claim alignment is fixture-level and evidence-reconciliation oriented; inquiry state is diagnostic/current-frame oriented. The similarity is structural, not a single architecture implemented through shared types.

## Acceptance answers

### What remains stable during a bounded inquiry?

In the reviewed implementations: desired observation, current strategy, bounded required-observation semantics, required authority semantics, and read-only/non-mutating boundary discipline.

### What is allowed to change?

Available authority, reachability/blockage, remaining observations, outcome, strategy status, blocking boundary, and uncertainty are allowed to change as current authority and observation availability change.

### Does current implementation already distinguish inquiry identity from inquiry state?

Yes, as implementation behavior and output shape. No, not as a separately named abstraction or state machine.

### Is the similarity to claim-state architecture implementation-backed or merely conceptual?

It is implementation-backed as a structural similarity: stable subject/identity plus variable reconciliation outcome. It is not implementation-backed as shared code, shared lifecycle, or a generic state framework.

## Recommended next bounded implementation question

```text
When authority is newly supplied for a previously blocked observation,
which existing inquiry-state fields should change in the same diagnostic output,
and which stable inquiry-identity fields must remain unchanged?
```

This question stays bounded to the existing authority-slice behavior and avoids proposing a state machine or generic framework.

## Report metadata

Files changed:

- `docs/bounded_inquiry_identity_state_reconciliation.md`

LOC changed:

- `docs/bounded_inquiry_identity_state_reconciliation.md`: 342 lines added.

Tests run:

```text
pytest -q tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_self_model_alignment.py tests/test_existence_claim_reconciliation.py tests/test_structure_claim_reconciliation.py
```
