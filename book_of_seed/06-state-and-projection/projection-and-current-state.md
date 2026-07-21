# Projection and Current State

## Constitutional subject
The derivation of projected material, current lawful condition, and possible current constitutional standing from constitutional records and repository evidence.

## Core question
Which projected material may support a question-facing current lawful condition or current constitutional standing, and how are scope, freshness, lineage, authority limits, and Unknowns exposed?

## Bounded resolution
Projected material is a recoverable view shaped by replay scope and projection rules. It may support current understanding, a current lawful condition, or bounded current constitutional standing only through a responsible consumer boundary that preserves evidence, warrant, authority, freshness, confidence, conflicts, expiry, mutation limits, and Unknowns. ObservationView exposes source-attributed observation testimony and its supporting ids; it does not assert promotion, current selection, verification, or Fact standing. A true FactView exposes a proposition with bounded Fact standing, not merely any projected support or fact-shaped material. The current implementation named `FactView` exposes projected normalized fact/support material, usually from `FactSupport` and sometimes from raw fact-shaped rows for fallback callers; this is an implementation inventory that may contain lawfully established Fact material but does not itself prove establishment, current applicability, universal truth, verified state, or exhaustive history. PR 1890 was therefore correct to recover the current implementation surface as compact projected normalized fact/support inventory, but overbroad if that phrase is treated as the constitutional definition of a FactView. A current-facing Fact View is a further standing-bearing emission that warrants present applicability under a declared projection, scope, purpose, as-of boundary, freshness/expiry treatment, conflict treatment, and Unknowns. A view or cache does not become a new constitutional source of law, and projection is not standing by identity.

## Addressable boundaries for implementation visibility

### 06.Projection.A — Projection and diagnostic visibility boundary
A projection, read model, diagnostic, audit, or inventory surface may expose bounded operational or constitutional visibility only within its recorded scope, inputs, freshness, shape, and mutation boundary. Its existence and output may be used as evidence that the bounded surface exists or reported what it reported, and projected material may support a later bounded standing determination, but neither existence nor output is source truth, Book law, complete corpus coverage, implementation readiness, ownership assignment, current constitutional standing, or cluster mutation authority by identity. Diagnostic or audit records remain diagnostic-scope findings unless a separate warranted act promotes a claim through the applicable evidence, authority, and standing boundaries.

### 06.Projection.B — Purpose-relative lossless projection and package standing
A projection, view, package, set, or handoff is lossless for a declared bounded consumer purpose only when its responsible formation preserves the distinctions needed for that consumer to recover the exact bounded standing it may rely on without reopening the producer, inventing missing standing, strengthening the upstream claim, or erasing surviving limits. Such compression need not duplicate every upstream implementation detail, but it must not collapse formation standing, contents, cardinality, availability, completeness, Unknowns, conflicts, refusals, known loss, negative authority, or aggregate judgment where those distinctions are required by the declared purpose. Empty contents, unavailable input, incomplete input, Unknown input, conflicting input, omitted material, null representation, no testimony, and negative testimony remain distinct unless a local warranted rule intentionally relates them. Aggregation over supplied contents produces only a bounded judgment over those contents and does not by itself establish that the input package existed, was complete, was available, or carried negative authority.


### 06.Projection.C — Rebuildability and prior invocation boundary
A derived artifact need not be preserved when the understanding it carries can be faithfully rebuilt from retained evidence. Projection snapshots are generally rebuildable from ledger-supported evidence; summary snapshots are generally rebuildable from projected State; fact-index snapshots are generally rebuildable from projected State. Rebuildability is bounded by the retained evidence, projection rules, and declared purpose, and does not mean rerunning an operation reconstructs a prior operation instance. Rebuildable projection is not prior invocation reconstruction. The elapsed duration of one invocation and the cache condition at that historical invocation may be irrecoverable after process exit even when current condition can be reconstructed or the operation can be rerun.

## Important distinctions
- projection != constitutional source
- projected material != current constitutional standing
- input artifact kind != View kind automatically
- projected FactSupport != FactView automatically
- FactView != current-facing Fact View
- ObservationView != FactView
- FactView != Fact establishment boundary
- read model != underlying record
- cache freshness != truth
- visibility != uptake
- diagnostic finding != cluster mutation
- implementation visibility != implementation authority
- rebuildable derived artifact != required retained artifact
- rebuildable projection != prior invocation reconstruction
- reconstructable current condition != irrecoverable historical invocation

## Representative repository anchors
- `seed_runtime/state.py::ProjectionBuildDiagnostics`
- `seed_runtime/projection_store.py`
- `seed_runtime/read_model_ownership.py`

## Counterexamples or failure modes
- Treating a generated topology as durable grammar.
- Preserving a stale projection because its presentation is stable.
- Collapsing projected material into current constitutional standing because replay completed.

## Related chapters
- [Lenses, views, and constitutional roads](../01-grammar-and-standing/lenses-views-and-roads.md)
- [Events, facts, and state](events-facts-and-state.md)
- [Ownership, discrepancy, and residue](ownership-discrepancy-and-residue.md)
