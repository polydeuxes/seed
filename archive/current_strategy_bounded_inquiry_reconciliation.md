---
doc_type: reconciliation
status: implementation-backed finding
scope: current_strategy, bounded inquiry authority slices
---

# Current strategy bounded inquiry reconciliation

## Central answer

Seed currently does not choose a strategy in the two authority-aware inquiry slices reviewed here.

The repository demonstrates that the bounded inquiry already determines the exposed strategy:

- `container ownership` returns `current_strategy=container_runtime_observation` because the container-ownership slice is bounded to container-runtime observations.
- `service ownership` returns `current_strategy=composite_local_service_attribution_observation` because the service-ownership slice is bounded to a composite local service attribution observation set.

This report does not propose a strategy engine, strategy planner, strategy runtime, alternative strategy implementation, generic inquiry framework, or future selection behavior.

## Files inspected

Required implementation and test files:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`

Recent reconciliation documents inspected where useful:

- `docs/inquiry_shapes_emerged_reconciliation.md`
- `docs/service_ownership_authority_reuse_findings.md`
- `docs/container_ownership_authority_minimal_slice_findings.md`

## 1. What `current_strategy` currently represents

Implementation-only meaning:

```text
current_strategy names the single implemented observation strategy for the bounded inquiry currently being evaluated.
```

In the container-ownership slice, `CURRENT_STRATEGY` is a module constant set to `container_runtime_observation`. The evaluator returns that constant directly in `ContainerOwnershipAuthoritySlice.current_strategy`.

In the service-ownership slice, `CURRENT_STRATEGY` is a module constant set to `composite_local_service_attribution_observation`. The evaluator returns that constant directly in `ServiceOwnershipAuthoritySlice.current_strategy`.

In both implementations, `strategy_status` is not a separate strategy-selection state. It is assigned from the computed `outcome`.

Therefore, `current_strategy` currently represents the strategy label already embedded in the bounded evaluator, not a selected winner among alternatives.

## 2. Chosen strategy or intrinsic bounded-inquiry strategy?

The strategy is intrinsic to the bounded inquiry in the current implementation.

Container ownership:

- The desired observation is fixed as `container ownership`.
- The required observations are fixed to the container-runtime observation set: `container_inventory` and `container_port_mapping`, filtered only by the existing container-runtime domain mapping.
- The returned `current_strategy` is always the fixed `CURRENT_STRATEGY` constant.
- The evaluator varies the outcome based on authority availability, not by choosing another strategy.

Service ownership:

- The desired observation is fixed as `service ownership`.
- The required observations are derived from the bounded service observation set: listener, listener-process, systemd-unit, and container-runtime observations.
- The returned `current_strategy` is always the fixed `CURRENT_STRATEGY` constant.
- The evaluator varies reachability and outcome based on observation authority, not by choosing another strategy.

The current behavior is therefore:

```text
bounded inquiry -> fixed implemented strategy label -> authority/reachability outcome
```

not:

```text
bounded inquiry -> candidate strategies -> selection/comparison/ranking/fallback -> current strategy
```

## 3. Does either implementation evaluate multiple candidate strategies?

No.

Neither implementation contains a candidate strategy collection, strategy scorer, strategy comparator, strategy ranking, strategy fallback branch, or strategy-selection loop.

The container slice evaluates one container-runtime observation path.

The service slice evaluates one composite local service attribution path. Although that path contains multiple observations and mixed authority requirements, those observations are components of one implemented composite strategy. They are not competing strategies.

## 4. Is this statement implementation-backed?

```text
The bounded inquiry determines the strategy.
```

Supported, for the two reviewed implementations.

The implementation-backed wording should remain narrow:

```text
For the current container-ownership and service-ownership authority slices, the bounded inquiry determines the exposed current_strategy.
```

Support:

- Container ownership is bounded to container-runtime evidence and exposes `container_runtime_observation`.
- Service ownership is bounded to composite local service attribution evidence and exposes `composite_local_service_attribution_observation`.
- Both evaluators return a constant strategy label for their inquiry.
- Tests assert the fixed strategy labels for direct evaluator results and CLI/JSON output.

This statement should not be widened into a claim that every possible future inquiry can only have one strategy.

## 5. Can a bounded inquiry possess only one valid strategy?

Supported only for the current two implemented bounded inquiries.

The current repository demonstrates two bounded inquiries that each possess one implementation-backed strategy:

- `container ownership` has one valid implemented strategy in this slice: `container_runtime_observation`.
- `service ownership` has one valid implemented strategy in this slice: `composite_local_service_attribution_observation`.

The repository does not demonstrate, and this report does not claim, that every future bounded inquiry must possess only one valid strategy.

The strongest implementation-backed answer is:

```text
A bounded inquiry can possess only one valid implementation-backed strategy in the current repository evidence.
```

## 6. Evidence for selection, comparison, ranking, or fallback

The current repository contains no implementation evidence in these two slices for:

```text
strategy selection
strategy comparison
strategy ranking
strategy fallback
```

Observed behavior instead:

- Authority availability changes `outcome`, `reachable_observations`, `blocked_observations`, `remaining_observations`, and `blocking_boundary`.
- Authority availability does not change `current_strategy`.
- Missing Docker/root authority blocks or partially blocks the current strategy; it does not select an alternate strategy.
- Local-passive service evidence makes part of the composite service strategy reachable; it does not become a separate fallback strategy.

## 7. Compatibility of the vocabulary with a possible future multi-strategy inquiry

The current vocabulary would remain semantically compatible with a future implementation where a bounded inquiry had multiple implementation-backed strategies, because `current_strategy` is a neutral label for the strategy currently being reported.

That compatibility is vocabulary-level only. The repository currently has no implementation-backed strategy-selection behavior. If a future implementation ever had multiple implementation-backed strategies, additional evidence would be needed to explain how `current_strategy` became current.

This report makes no recommendation to add such behavior.

## Supported implementation

### Container ownership

The container implementation fixes:

- desired observation: `container ownership`
- strategy: `container_runtime_observation`
- observations: `container_inventory`, `container_port_mapping`
- authority requirement: `docker_group_or_root` for both observations
- constrained-profile outcome: `blocked`

The authority profile determines whether the fixed strategy is blocked or unknown; it does not determine a different strategy.

### Service ownership

The service implementation fixes:

- desired observation: `service ownership`
- strategy: `composite_local_service_attribution_observation`
- observations: `tcp_listen_inventory`, `listener_process_inventory`, `systemd_unit_inventory`, `container_inventory`, `container_port_mapping`
- authority requirements: local-passive, partial-non-root, and Docker/root-dependent requirements
- constrained-profile outcome: `partially_reachable`

The authority profile determines which observations inside the fixed composite strategy are reachable or blocked; it does not determine a different strategy.

## Unsupported behavior

Unsupported by current implementation:

- choosing among candidate strategies
- comparing strategies
- ranking strategies
- falling back from one strategy to another
- treating local-passive service evidence as an alternate strategy
- treating Docker/root failure as a trigger for strategy replacement
- interpreting `current_strategy` as a decision product

## Strongest supporting evidence

1. Both modules define exactly one `CURRENT_STRATEGY` constant.
2. Both evaluators return that constant directly as `current_strategy`.
3. Both evaluators compute `strategy_status` from `outcome`, not from selection metadata.
4. Container ownership has one observation family and one effective authority class, so blocked Docker/root authority blocks the single current strategy.
5. Service ownership has mixed observations and mixed authority classes, but they are assembled into one composite strategy and reported as one `current_strategy`.
6. Tests assert the fixed strategy labels in direct evaluator output, JSON output, and human CLI output.
7. Recent reconciliation already distinguishes a stable inquiry-state discipline from naturally varying inquiry shapes, without introducing a planner, framework, or generalized inquiry runtime.

## Strongest contradictory evidence

The strongest possible contradictory evidence is naming, not behavior:

- The field name `current_strategy` could sound like a selected current item from a larger set.
- The service strategy is called `composite`, and its internal observations have different reachability states.

Current implementation resolves both points narrowly:

- No larger candidate set exists in the reviewed implementations.
- Composite service observations are components of one strategy, not competing strategies.
- The strategy label remains fixed while reachability and outcome vary.

## Acceptance answers

### Does Seed currently choose a strategy, or does the inquiry already define it?

For the reviewed implementations, the inquiry already defines it. Seed does not currently choose among multiple strategies.

### Have we discovered strategy selection, or simply named the strategy already embedded in the implementation?

The repository has simply named the strategy already embedded in each bounded implementation.

### Should `current_strategy` be interpreted as a decision or as a property of the bounded inquiry?

In the current repository evidence, `current_strategy` should be interpreted as a property of the bounded inquiry, not as a decision.

## Files changed

- `docs/current_strategy_bounded_inquiry_reconciliation.md`

## LOC changed

- Added one documentation file, 250 lines.

## Tests run

- `pytest -q tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py`

## Recommended next bounded implementation question

```text
When authority availability changes, which inquiry-state fields are allowed to change while current_strategy remains stable?
```

This question stays bounded to current implementation behavior and does not require strategy selection, a planner, or a generic inquiry framework.
