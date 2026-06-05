# Context / Explanation / Knowledge Consolidation Audit

## Scope and conclusion

This audit covers the current Seed context, explanation, evidence, observation,
fact, confidence, contradiction, state-view, and runtime-trace paths. It found
several intentionally distinct read-only views over the same canonical projected
`State`, plus two provider-facing context shapes that were ambiguous:

- `seed_runtime.context.ContextPacket` / `ContextComposer`, used by the older
  `Runtime` path.
- `seed_runtime.runtime_loop.RuntimeContext`, used by `RuntimeLoop` v1.
- `seed_runtime.context_views.DecisionContextView`, introduced as the knowledge
  boundary intended for future decision providers.

Low-risk consolidation implemented here: `RuntimeLoop` now includes an explicit
`DecisionContextView` inside `RuntimeContext`. This preserves existing runtime
behavior, keeps `State` available for compatibility, and removes ambiguity about
whether RuntimeLoop providers can consume the canonical decision-ready knowledge
view.

No providers, views, ingestion paths, CLI commands, shell execution, network
execution, or runtime safety boundaries were added.

## Canonical component map

### Event and projection backbone

| Canonical concept | Component(s) | Role |
| --- | --- | --- |
| Append-only facts of record | `EventLedger`, `SQLiteEventLedger` in `seed_runtime.events` | Durable event source. Knowledge and runtime trace views read from this rather than mutating separate stores. |
| Projected world model | `State`, `StateProjector` in `seed_runtime.state` | Canonical in-memory projection for entities, observations, evidence, facts, support groups, relationships, requirements, capabilities, issues, conflicts, and inferred facts. |
| Projection cache | `ProjectionStore`, `project_state_with_cache` in `seed_runtime.projection_store` | Optional cache of projected `State`; not a separate source of truth. |
| Read-only current-state slices | `seed_runtime.state_views` | Canonical operator-facing state summaries for current facts, observations, requirements, capabilities, issues, and counts. |

### Context

| Concept | Component(s) | Canonical status |
| --- | --- | --- |
| Legacy compact provider packet | `ContextPacket`, `ContextComposer` in `seed_runtime.context` | Existing provider-facing shape for the older `Runtime` path. Keep for compatibility. It composes current input, active goal, entities, facts with selected evidence, visible tools, open tool needs, schema, and budget trace. |
| RuntimeLoop provider context | `RuntimeContext` in `seed_runtime.runtime_loop` | Canonical provider input for `RuntimeLoop` v1. It now contains `workspace_id`, `run_id`, raw projected `state`, current input, visible tools, and the explicit `decision_context`. |
| Decision-ready knowledge view | `DecisionContextView` in `seed_runtime.context_views` | Canonical knowledge boundary for decision-making. It is a deterministic read-only projection from `State` plus Evidence Graph, Contradiction Detection, and Confidence Aggregation. It should not be folded into `State` because it is a selected provider view, not durable world state. |
| Context selection / budget | `seed_runtime.context_selection`, `seed_runtime.context_budget` | Support code for `ContextComposer`; not a competing knowledge model. |

Decision: `RuntimeLoop` should consume / expose `DecisionContextView` directly as
part of `RuntimeContext`. `DecisionContextView` should not be folded into
`RuntimeContext` as raw fields or into `State`; doing so would blur the boundary
between canonical world projection and provider-facing selection.

### Evidence, observations, and facts

| Canonical concept | Component(s) | Role |
| --- | --- | --- |
| External observation | `Observation` in `seed_runtime.observations` | Canonical normalized observation payload: subject, predicate, value, source type, time, confidence, metadata, dimensions, optional expiry. |
| Observation ingestion path | `ObservationIngestor` in `seed_runtime.observations` | Appends `observation.observed`, derived `evidence.observed`, and derived `fact.observed` events. |
| Raw input inspection | `InputInspector`, observation sources, observation normalizers | File/provider input classification and normalization before observations. These are ingestion helpers, not separate state. |
| Provenance record | `Evidence` in `seed_runtime.evidence` | Canonical immutable support payload for one or more facts. |
| Projected claim | `Fact` in `seed_runtime.facts` | Canonical interpreted claim with `evidence_ids`, source type, confidence, observed time, optional expiry, and optional inference provenance. |
| Aggregated support | `FactSupport` in `seed_runtime.facts`, projected by `State` | Canonical support grouping by subject + predicate + value (+ dimensions). |
| Tool-output evidence only | `FactExtractionService` in `seed_runtime.fact_extraction` | Older compatible extractor for `tool.call.completed` that records evidence without inferring facts. Not a separate fact engine. |
| Evidence graph | `seed_runtime.evidence_graph` | Read-only graph/view over `State.evidence` and `State.facts`; not a duplicate evidence store. |

Decision: Evidence Graph duplicates some traversal questions answered by
`ExplanationBuilder`, but it does not duplicate persistence or ingestion. Keep it
as a read-only provenance index and CLI view; use `Evidence`/`Fact`/`FactSupport`
as canonical data.

### Explanation / why

| CLI / component | Backing code | Status |
| --- | --- | --- |
| `--why ENTITY PREDICATE` | `ExplanationBuilder.why` in `seed_runtime.explanations` | Canonical belief explanation over current and competing projected `FactSupport`; includes recursive inferred-fact provenance. Keep distinct. |
| `--why-fact SUBJECT PREDICATE [OBJECT]` | `find_evidence_for_fact` / `FactEvidenceView` in `seed_runtime.evidence_graph` | Evidence-centric fact provenance view. Overlaps with `--why` but answers a narrower fact/evidence question. Keep, document as evidence graph explanation rather than separate engine. |
| `--evidence` | `build_evidence_graph`, `build_evidence_summary` | Whole-graph provenance summary. Keep distinct from belief explanation. |
| `--trace-run RUN_ID` | `RuntimeTraceReader` / `RuntimeTrace` | Runtime event reconstruction. Not a knowledge explanation engine. Keep distinct. |
| `--why-run RUN_ID` | `RuntimeTrace` summary formatter | Human summary of the same runtime trace. Keep distinct from `--why`; it explains a runtime decision, not a projected belief. |
| `--confidence`, `--confidence-fact` | `seed_runtime.confidence` | Confidence aggregation view over facts/evidence/contradictions. Keep as diagnostic view. |
| `--contradictions` | `seed_runtime.contradictions` | Contradiction detection view. Keep as diagnostic view and `DecisionContextView` input. |

Decision: There are multiple explanation views, but not multiple explanation
engines for the same boundary. `ExplanationBuilder` explains projected beliefs;
Evidence Graph explains fact provenance; RuntimeTrace explains run-time decision
history. The only confusing overlap is naming (`--why` vs `--why-fact` vs
`--why-run`), and the commands should remain distinct to preserve behavior.

## Duplicate / overlapping concepts

1. **Provider context shapes**
   - Overlap: `ContextPacket` and `RuntimeContext` both describe provider input.
   - Consolidation: `RuntimeLoop.RuntimeContext` now embeds the canonical
     `DecisionContextView` while retaining existing fields. `ContextComposer`
     remains for the older `Runtime` path.

2. **Fact provenance explanations**
   - Overlap: `ExplanationBuilder` and Evidence Graph can both surface evidence
     ids and supporting events.
   - Consolidation recommendation: keep both for now; treat Evidence Graph as a
     provenance index and `ExplanationBuilder` as current-belief explanation.
     Future work can adapt `ExplanationBuilder` to optionally reuse
     `FactEvidenceView` for evidence formatting, but no behavior should be
     removed without tests.

3. **State views vs DecisionContextView**
   - Overlap: both project read-only slices from `State`.
   - Consolidation recommendation: keep `State Views` as operator/read-model
     slices and `DecisionContextView` as selected provider-facing knowledge.
     `DecisionContextView` may reuse state views for requirements/capabilities,
     as it already does.

4. **Observation and evidence terminology**
   - Overlap: `Observation` is converted into `Evidence`; some tool outputs are
     represented directly as `Evidence` by `FactExtractionService`.
   - Consolidation recommendation: keep both event paths. Canonical normalized
     IN data should go through `ObservationIngestor`; legacy/direct tool output
     may remain evidence-only until an explicit fact mapping exists.

## Recommended consolidation plan

### Keep

- `State` / `StateProjector` as canonical projected world model.
- `Observation`, `Evidence`, `Fact`, `FactSupport`, `FactConflict` as canonical
  knowledge models.
- `EvidenceGraph`, `Contradictions`, `Confidence`, and `State Views` as
  read-only projections over `State`.
- `DecisionContextView` as the canonical provider-facing knowledge view.
- `RuntimeTrace` as the canonical read-only RuntimeLoop run reconstruction.
- Existing CLI commands, because they answer distinct operator questions.

### Merge / adapt

- `RuntimeLoop.RuntimeContext` should include `DecisionContextView` explicitly
  and should be the RuntimeLoop provider boundary. This has been implemented.
- Future providers should prefer `context.decision_context` for knowledge
  selection and use `context.state` only as a compatibility escape hatch.
- If the older `Runtime` path remains active, consider adding a
  `DecisionContextView` to `ContextPacket` in a later compatibility-focused
  change, but only with tests because that packet uses context budgeting.

### Delete

No deletion is recommended in this audit. The overlapping modules are read-only
views or compatibility layers, not duplicate stores or behavior that can be
safely removed under the current test coverage.

## CLI surface and recommended boundaries

| CLI flag | Keep? | Boundary |
| --- | --- | --- |
| `--why` | Yes | Belief explanation for current/ambiguous/no-current projected support. |
| `--why-fact` | Yes | Evidence Graph explanation for a fact query. |
| `--why-run` | Yes | Human RuntimeTrace summary for a RuntimeLoop run. |
| `--trace-run` | Yes | Detailed RuntimeTrace event listing. |
| `--current-facts` | Yes | State View for all facts, with legacy subject/predicate query behavior preserved. |
| `--current-observations` | Yes | State View for projected observations. |
| `--current-requirements` | Yes | State View for requirements. |
| `--current-capabilities` | Yes | State View for capabilities. |
| `--current-issues` | Yes | State View for projected issues. |
| `--evidence` | Yes | Whole Evidence Graph summary. |
| `--unsupported-facts` | Yes | Evidence Graph diagnostic for facts with no linked evidence. |
| `--contradictions` | Yes | Contradiction Detection diagnostic. |
| `--confidence` | Yes | Confidence Aggregation summary. |
| `--confidence-fact` | Yes | Confidence details for a fact query. |
| `--decision-context` | Yes | Exact provider-facing `DecisionContextView` JSON. |
| `--fact-support`, `--best-fact`, `--fact-conflicts` | Yes | Older fact-support/current-belief diagnostics that should remain for compatibility. |

## Files involved

### Context and runtime

- `seed_runtime/context.py`
- `seed_runtime/context_views.py`
- `seed_runtime/context_budget.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/runtime.py`
- `seed_runtime/runtime_loop.py`
- `seed_runtime/decision_journal.py`

### Explanation and trace

- `seed_runtime/explanations.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/runtime_trace.py`
- `scripts/seed_local.py`

### Evidence / observation / facts

- `seed_runtime/observations.py`
- `seed_runtime/evidence.py`
- `seed_runtime/facts.py`
- `seed_runtime/fact_extraction.py`
- `seed_runtime/input_inspector.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/predicate_normalizers.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/confidence.py`
- `seed_runtime/contradictions.py`

### Tests covering the boundary

- `tests/test_context.py`
- `tests/test_context_views.py`
- `tests/test_runtime_loop.py`
- `tests/test_runtime_trace.py`
- `tests/test_evidence_graph.py`
- `tests/test_explanations.py`
- `tests/test_state_views.py`
