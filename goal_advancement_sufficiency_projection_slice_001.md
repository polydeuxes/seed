# Goal Advancement Sufficiency Projection Slice 001

This slice adds one read-only `GoalAdvancementSufficiencyProjection` over one exact `GoalAdvancementNeedSet` and one exact `AdvancementNeedFamilyCoverageSet`.

## Boundary

The projection consumes only standings already emitted by native need-family owners and coverage-family owners. It does not reinterpret stale or unavailable evidence, discover new needs, rank needs, select movement, route work, open inquiry, request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.

## Conclusions

The projection emits exactly one bounded conclusion:

- `conflicting`
- `insufficient_for_now`
- `unknown`
- `sufficient_for_now`

`Sufficient_for_now` is limited to the selected goal and bounded advancement horizon. It is not permanent goal satisfaction, next movement selection, movement authorization, execution, or recording.

`Insufficient_for_now` means at least one included family preserved an established unresolved native need. It is not global blockage, priority, selected resolution, or routing.

## Rule implemented

1. Material identity, scope, native-need, or coverage conflict yields `conflicting`.
2. Otherwise, any established unresolved native need yields `insufficient_for_now`.
3. Otherwise, any included family with absent native projection, unknown native standing, partial/unknown coverage, or unresolved binding yields `unknown`.
4. Otherwise, complete included-family coverage with no established, unknown, or conflicting native need, plus explicit non-conflicting reasons for excluded families, yields `sufficient_for_now`.

Established insufficiency is intentionally decisive over unrelated Unknowns, while Unknown reasons remain preserved in the unordered reason set.

## Preservation

Family reasons are a `frozenset`, so multiple established needs and coexisting Unknowns remain unordered. Coverage gaps are represented as Unknown sufficiency reasons and are not promoted into native advancement needs.
