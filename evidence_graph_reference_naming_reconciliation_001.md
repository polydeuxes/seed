# Evidence Graph Reference Naming Reconciliation 001

## Naming pressure

PR 1823 established the Evidence Graph admission boundary: a represented unresolved reference is not the same thing as resolved admitted Evidence. Once that boundary became implementation-backed, names that blurred reference visibility with admitted Evidence, or that overloaded one field for two fact roles, stopped being harmless.

## Misleading names found

| Before name | Pressure |
| --- | --- |
| `EvidenceReference` | Looked like a universal Evidence artifact instead of a graph-local represented reference. |
| `ReferenceStanding` | Looked like a universal reference standing instead of the Evidence Graph's local reference standing vocabulary. |
| `FactEvidenceView.represented_references` | Did not identify that the represented references are graph-local and separate from admitted `evidence`. |
| `EvidenceReference.source_fact_id` | Was overloaded: unresolved references used it for the fact carrying the unresolved evidence ID, while derivation references used it for the upstream source fact. |
| `_evidence_for_fact(...)` | Implied every returned item was Evidence, though it returned both admitted Evidence nodes and represented non-evidence references. |
| `find_evidence_for_fact(...)` | Public query helper implied only Evidence, though returned fact views containing Evidence Graph material, including represented graph references. |

## Constitutional roles distinguished

The reconciliation separates these roles mechanically:

1. **Referencing fact**: the fact that carries or contributes the graph-local reference.
2. **Source fact**: the upstream source fact named by a derivation relation.
3. **Admitted Evidence**: resolved Evidence nodes admitted into graph support links.
4. **Represented graph reference**: visible graph-local material for unresolved evidence IDs or derivation source-fact references that must not be counted as admitted Evidence.

## Before and after names

| Before | After | Role now named |
| --- | --- | --- |
| `EvidenceReference` | `EvidenceGraphReference` | Graph-local represented reference, not a universal Evidence kind. |
| `ReferenceStanding` | `EvidenceGraphReferenceStanding` | Graph-local reference standing vocabulary. |
| `FactEvidenceView.represented_references` | `FactEvidenceView.represented_graph_references` | References represented by the Evidence Graph, separate from admitted Evidence nodes. |
| unresolved-reference `source_fact_id` | `referencing_fact_id` | The fact carrying the unresolved evidence reference. |
| derivation-reference `source_fact_id` | `source_fact_id` | The actual upstream source fact named by the derivation relation. |
| `_evidence_for_fact(...)` | `_evidence_graph_material_for_fact(...)` | Helper returns mixed Evidence Graph material: admitted Evidence nodes plus represented graph references. |
| `find_evidence_for_fact(...)` | `find_evidence_graph_material_for_fact(...)` | Query returns Evidence Graph fact-material views, not only Evidence-backed material. |

## Why each rename is now mature rather than premature

- The admission boundary is implemented: unresolved references are visible but do not create Evidence nodes or support links.
- Derivation references are visible without becoming admitted Evidence support.
- The overloaded fact field had two live meanings in implementation, so keeping one mechanical name hid a constitutional distinction.
- Downstream support counting depends on admitted `evidence`, not represented references, so graph-local reference names can be made explicit without reopening admission behavior.

## Compatibility treatment

No compatibility aliases were added. These names were introduced by the recent Evidence Graph admission work and repository search did not show an established external consumer that required retaining the misleading names. The change intentionally updates in-repository call sites and tests rather than preserving speculative aliases.

## Files changed

- `seed_runtime/evidence_graph.py`
- `scripts/seed_local.py`
- `tests/test_evidence_graph.py`
- `tests/test_contradictions.py`
- `docs/state.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/audit/context_knowledge_consolidation.md`
- `evidence_graph_admission_fidelity_slice_001.md`
- `evidence_graph_reference_naming_reconciliation_001.md`

## Tests executed

```text
pytest -q tests/test_evidence_graph.py tests/test_confidence.py tests/test_contradictions.py tests/test_context_views.py
```

Result: passed.

## Preserved behavior

- Resolved Evidence admission remains separate from unresolved or derivation references.
- Unresolved-reference visibility remains present.
- Derivation-reference visibility remains present.
- Evidence support links are still created only for resolved Evidence nodes.
- Confidence support counts continue to count admitted Evidence nodes only.
- Contradiction lineage still avoids inventing supporting event IDs from unresolved references.
- Decision-context behavior remains covered by the unchanged context-view test suite.
- Ordering remains deterministic.
- Evidence Graph and CLI view construction remain read-only.
- JSON/dataclass serialization remains lawfully compatible with the updated in-repository dataclass names and fields; no stale alias fields were added.

## Remaining naming Unknowns

- Broader documentation still uses long-established names such as `FactEvidenceView` and `EvidenceGraph`; this task did not reopen those names because the requested district was the PR 1823 graph-local reference/admission artifact set.
- Historical audit documents may contain conceptual uses of `source_fact_id` for non-Evidence-Graph fact and relationship provenance. Those are outside this reconciliation because they refer to existing fact/projection models rather than the graph-local reference record.
- The Evidence Graph CLI presentation does not currently print represented graph references. This reconciliation did not add a new visible output surface because runtime behavior and surface area were intentionally preserved.
