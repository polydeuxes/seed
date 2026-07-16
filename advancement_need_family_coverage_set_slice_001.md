# Advancement Need Family Coverage Set Slice 001

This slice adds one read-only `AdvancementNeedFamilyCoverageSet` assembler for one exact `BoundedAdvancementHorizon`.

The assembler preserves, per clarification, inquiry, authority, and operational-realization family:

- selected goal and horizon identity;
- native need-projection identity;
- family-owned bounded candidate-space identity;
- covered component references;
- unexamined component references;
- explicitly excluded component references and reasons;
- evidence-snapshot binding;
- unknowns and conflicts.

It keeps scope disposition (`included`, `excluded`, `conflicting`) separate from coverage standing (`complete_for_horizon`, `partial`, `unknown`, `conflicting`, `not_evaluated`). Horizon-excluded families retain their explicit reason and remain `not_evaluated` rather than becoming complete.

Completion is only assembled when matching family-owned bounded candidate space testimony accounts for every included component, all component exclusions are explicitly reasoned, and no material coverage conflict is present. Supplied projections, empty candidate spaces, absent testimony, stale or unavailable testimony, successful tests, and absence of evidence do not imply completeness.

The assembler is not the candidate-space owner, need classifier, planner, authority selector, realization selector, router, recorder, event-ledger writer, or state mutator.
