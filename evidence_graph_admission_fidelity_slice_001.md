# Evidence Graph Admission Fidelity Slice 001

## completed evidence consumed

- `constitutional_evidence_consumer_district_survey_001.md` was consumed as completed evidence.
- PR 1822's selection of Evidence Graph as the smallest actual-Evidence uptake frontier was accepted without repeating the district survey.

## selected boundary

- Selected boundary: Evidence Graph local admission standing.
- Recovered distinction: a represented evidence reference is not the same as resolved admitted Evidence.
- Scope: `seed_runtime/evidence_graph.py` and immediate downstream consumers that materially rely on graph evidence standing.

## implementation evidence

- The graph producer previously created `EvidenceNode` objects for missing `Fact.evidence_ids` by synthesizing node material from the `Fact`.
- The graph producer also created `EvidenceLink(relationship="supports")` for every node returned for a fact.
- Confidence counted `len(FactEvidenceView.evidence)` as `support_count`.
- Contradiction lineage read `FactEvidenceView.supporting_event_ids` and had a fallback that could reuse unresolved fact evidence IDs as supporting event IDs.
- Decision context exposed confidence `support_count` as `evidence_count`.

## before

- Missing `State.evidence[evidence_id]` still became an `EvidenceNode`.
- Synthesized nodes received ordinary support links.
- Synthesized nodes increased graph evidence counts and downstream support counts.
- Missing evidence IDs could be rendered as supporting event IDs.

## unfaithful crossing

- An unresolved `Fact.evidence_ids` reference crossed from visible reference material into resolved admitted Evidence standing.
- That crossing made unresolved material eligible for ordinary support links, support counts, confidence uplift, context evidence counts, and support wording.

## recovered standings

| Material | Owner | Artifact or representation | Standing |
| --- | --- | --- | --- |
| Resolved `State.evidence[evidence_id]` | Evidence Graph | `EvidenceNode` plus ordinary `supports` link | Admitted evidence support |
| Missing `Fact.evidence_ids` entry | Evidence Graph | `EvidenceReference(standing="unresolved_evidence_reference")` | Visible unresolved reference only |
| Source-fact/projection fallback | Evidence Graph | `EvidenceReference(standing="derivation_reference")` | Visible derivation reference only |

## consumers

- Confidence now continues to count only admitted `FactEvidenceView.evidence` nodes.
- Unsupported status remains based on admitted evidence count, not represented unresolved references.
- Contradiction lineage now uses graph supporting event IDs only, avoiding fallback invention from unresolved IDs.
- Decision context continues to consume confidence `support_count`, so unresolved references produce `evidence_count=0` unless separate lawful support exists.
- Human fact explanations now distinguish represented references from resolved supporting evidence records.

## downstream reliance corrected

- `support_count`: unresolved references do not increment it.
- `unsupported`: a fact with only unresolved references remains unsupported when no explicit confidence or other admitted support exists.
- `evidence-derived confidence`: unresolved references do not raise it.
- `supporting event IDs`: unresolved references do not invent source-event occurrence.
- `contradiction lineage`: unresolved material remains visible through attached fact evidence views without becoming supporting event IDs.
- `decision-context evidence count`: unresolved references remain zero-count support.
- `explanation wording`: unresolved-only facts are not described as supported by evidence records.

## negative authority

- This slice does not build a universal evidence router.
- This slice does not create a central admission engine.
- This slice does not reopen applicability, admission, or consumption grammar.
- This slice does not repair missing Evidence by copying `Fact` coordinates into Evidence standing.
- This slice does not remove unresolved references merely to simplify counts.
- This slice does not select observation ingestion as the implementation frontier.

## Fidelity result

- before: unfaithful boundary crossing
- after: faithful within scope
- Reason: reference visibility is preserved without granting unresolved material resolved Evidence standing.

## compatibility treatment

- Resolved Evidence Graph behavior is preserved: resolved Evidence remains visible as `EvidenceNode`, receives ordinary support links, and remains available to confidence, contradiction, context, and explanation consumers.
- Ordering remains deterministic for nodes, links, and represented references.
- The projection remains read-only and does not add event-ledger writes, State mutation, provider execution, tool execution, or runtime behavior.
- Public shapes are additive where necessary: unresolved and derivation references are represented separately from admitted `evidence` nodes.
- False compatibility was not preserved for evidence counts, support wording, or source-event IDs derived only from unresolved references.

## tests executed

- `pytest -q tests/test_evidence_graph.py tests/test_confidence.py tests/test_contradictions.py tests/test_context_views.py`

## files changed

- `seed_runtime/evidence_graph.py`
- `seed_runtime/contradictions.py`
- `tests/test_evidence_graph.py`
- `tests/test_confidence.py`
- `tests/test_contradictions.py`
- `tests/test_context_views.py`
- `evidence_graph_admission_fidelity_slice_001.md`

## remaining compressed responsibilities

- The Evidence Graph still uses implementation-local graph standing rather than a universal admission engine.
- Consumers still rely on the graph-local distinction between admitted `evidence` nodes and represented references.
- Full Evidence applicability validation remains outside this slice.

## preserved Unknowns

- Missing Evidence material remains unknown and visible as an unresolved reference.
- Source-fact/projection fallback remains a weaker derivation reference unless separate resolved Evidence exists.
- The slice does not infer producer event occurrence from unresolved evidence IDs.
