# Read-Model Ownership Slice 001

## Selected architectural boundary

**Published projected state handoff into read-model construction.**

Projection publication stops when finalized `State` becomes consumer-visible projected state. Read-model construction begins when read-model builders accept that visible `State` as their construction input. This slice made that handoff explicit with `ReadModelConstructionInputs`, an identity-preserving implementation-local boundary.

## Implementation evidence

- Projection publication already returns the same finalized `State` as `visible_state`; publication is explicitly not replay, cache invalidation, storage, CLI, JSON, events, or read-model semantics.
- State summary construction reads an already-built `State` to count projected facts, observations, goals, tool needs, tools, graph issues, last event, and projection version.
- Fact index construction reads an already-built `State` through `fact_supports`, `get_current_facts`, and `last_event_id` to build a cacheable derived index.
- Fact index cache lookup is keyed by the published state's projection version and last event id, then either returns a cached derived read model or builds one from the same state.

## Before

Projection publication and read-model construction were adjacent but compressed:

- publication returned a visible `State`;
- `build_state_summary` immediately treated its `State` parameter as read-model input;
- `build_fact_index` and `load_or_build_fact_index` immediately treated their `State` parameter as both cache dependency evidence and construction input.

The behavior was correct, but the ownership boundary between visible projected state and derived read-model construction was only implicit in helper signatures and comments.

## After

`ReadModelConstructionInputs` now names the construction-side input boundary. The helper `read_model_construction_inputs(state)` wraps the already-published projected state without copying, filtering, refreshing, mutating, or republishing it.

State summary construction and fact index construction now start by recovering this construction input boundary, then continue using the same visible `State` object and the same existing read-model logic.

## Boundary made explicit

Projection Publication **does not** own read-model construction.

Read-model construction starts at an identity-preserving handoff from visible projected state into the read-model builder. The recovered boundary owns only the construction inputs for derived read models. It does not own:

- projection replay;
- projection execution;
- projection finalization;
- projection publication;
- cache invalidation;
- rendering;
- CLI;
- scheduling;
- persistence.

## Compatibility preserved

No compatibility boundary changed.

- Projection publication behavior is unchanged.
- Read-model semantics are unchanged.
- Cache behavior is unchanged.
- Summary contents are unchanged.
- Fact index contents are unchanged.
- CLI, JSON, events, ledger replay, and persistence are unchanged.
- No runtime surface was introduced.

## Questions answered from implementation evidence

1. **Where were projection publication and read-model construction previously mixed?**

   They were mixed at the call boundary where read-model builders accepted the same `State` object produced by projection publication without an explicit construction-side handoff. The clearest recurring examples were state summary construction and fact index construction/cache lookup.

2. **Which recovered architectural boundary became more explicit?**

   The identity-preserving handoff from visible projected state into read-model construction inputs.

3. **How does the implementation now better reflect the recovered architecture?**

   Read-model builders now first recover `ReadModelConstructionInputs` from the visible state before constructing the summary or fact index. This makes the post-publication construction start point observable while leaving all builder logic and projection publication untouched.

4. **Did implementation evidence suggest a more precise responsibility name than "Read-Model Construction"?**

   Yes: **Read-Model Construction Inputs**. The recovered slice is narrower than full read-model construction; it represents the published-state handoff into builders, not construction algorithms, caching, persistence, rendering, or invalidation.

5. **Did any compatibility boundary change?**

   No.

## Files changed

- `seed_runtime/read_model_ownership.py` — added the implementation-local construction input boundary.
- `seed_runtime/state_views.py` — state summary construction now starts from read-model construction inputs.
- `seed_runtime/fact_index.py` — fact index cache lookup/build now starts from read-model construction inputs.
- `tests/test_state_views.py` — added proof that state summary construction begins from the recovered input boundary.
- `tests/test_fact_index.py` — added proof that fact index construction begins from the recovered input boundary.
- `read_model_ownership_slice_001.md` — this report.

## LOC changed

At report time, `git diff --stat` showed:

```text
read_model_ownership_slice_001.md    | 129 +++++++++++++++++++++++++++++++++++
seed_runtime/fact_index.py           |  22 ++++--
seed_runtime/read_model_ownership.py |  33 +++++++++
seed_runtime/state_views.py          |  17 +++--
tests/test_fact_index.py             |  19 ++++++
tests/test_state_views.py            |  19 ++++++
6 files changed, 227 insertions(+), 12 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_state_views.py tests/test_fact_index.py
```

Result: `29 passed`.

## Remaining compressed read-model ownership responsibilities

This slice intentionally stops after one boundary. Remaining implementation pressure still appears around:

- broader read-model construction algorithms beyond the initial input handoff;
- state summary cache ownership and debug visibility;
- fact index cache ownership versus construction ownership;
- inquiry view construction ownership;
- diagnostic view construction ownership;
- current-facts read paths that can use either state methods or derived fact index read models;
- dependent cache metadata ownership.

These are not changed here.

## Observations about emerging family vocabulary

The implementation evidence supports **Read-Model Ownership** as the family name, but this slice's most precise local term is **Read-Model Construction Inputs**. The vocabulary should remain implementation-backed and narrow: presentation terms should not be promoted into repository knowledge unless future implementation evidence supports them.
