# Knowledge Reachability Slice 006 — Table and human formatting

## District consistency gate

- Active district verified: **Knowledge Reachability**.
- Latest relevant completed slice verified: **`knowledge_reachability_slice_005.md`**, after prior verification of `knowledge_reachability_slice_003.md`, `knowledge_reachability_slice_004.md`, and `knowledge_reachability_district_scout_001.md`.
- Post-Slice-005 reassessment inspected `seed_runtime/knowledge_reachability.py` and `format_knowledge_reachability_table(...)`.
- Branch and local files did not point to another active district. Unrelated district reports were not used as authority.

## Selected boundary

Table/human formatting.

## Reassessment result

After Slices 004 and 005, `format_knowledge_reachability_table(...)` still contained one narrow implementation-local ownership boundary: constructing the existing human-readable Knowledge Reachability table and metadata sections. This is not metadata value production, JSON payload construction, candidate admission, index construction, row evaluation, diagnostic registration, CLI dispatch, Source Navigation, Question Surface Inventory, or bounded ask dispatch. Compatibility can be preserved without schema or behavior changes.

## Implementation evidence

The formatter owned headers, stage-to-attribute mapping, yes/no rendering, column width calculation, timing/candidate/kind/loss metadata sections, truncation guard text, and final table composition.

## Before

`format_knowledge_reachability_table(...)` directly owned the full table and human-readable metadata rendering body.

## After

`_knowledge_reachability_table_output(...)` owns construction of the existing human-readable table output. The public `format_knowledge_reachability_table(...)` remains as the compatibility entry point and delegates unchanged behavior.

## Recovered producer

`_knowledge_reachability_table_output(...)`.

## Recovered artifact/helper

The helper returns the existing human-readable table string, with or without metadata sections depending on whether metadata is supplied.

## Recovered consumer

`format_knowledge_reachability_table(...)` consumes the helper result as the public API. Existing CLI human output continues to use the public formatter path.

## Compatibility preserved

No.

Headers, stage-to-attribute mapping, yes/no rendering, column widths, timing metadata section, candidate metadata section, candidate-kind metadata section, loss-stage metadata section, truncation guard text, final table composition, CLI-like human output, diagnostic-shape expectations, read-only metadata, and event-ledger non-mutation are preserved.

## Files changed

- `seed_runtime/knowledge_reachability.py`
- `tests/test_knowledge_reachability.py`
- `knowledge_reachability_slice_006.md`

## LOC changed

Slice 006 implementation/test diff before this report: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py` changed with 75 insertions and 0 deletions.

## Tests executed

- `pytest -q tests/test_knowledge_reachability.py` — passed.

Focused coverage proves headers, stage-to-attribute mapping through stage columns, yes/no rendering, column widths, timing metadata section, candidate metadata section, candidate-kind metadata section, loss-stage metadata section, truncation guard text, final human-readable table composition, CLI-like human output, diagnostic-shape-compatible table availability, read-only metadata, and event-ledger non-mutation.

## Remaining compressed responsibilities

No further Knowledge Reachability implementation-local ownership boundary was directly evident without broad scouting after recovering metadata assembly, JSON payload construction, and table/human formatting. Diagnostic registration, CLI dispatch, Source Navigation, Question Surface Inventory, bounded ask dispatch, progress/deadline behavior, candidate admission, index construction, and row evaluation remain out of scope or already recovered.

## Required questions

1. **What responsibility was previously compressed?** Human-readable Knowledge Reachability table and metadata-section formatting.
2. **Which implementation-local ownership boundary became directly observable?** Formatting of completed Knowledge Reachability rows and metadata into the public table string.
3. **What producer now owns the recovered responsibility?** `_knowledge_reachability_table_output(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The helper carries the boundary and returns the existing human-readable table string.
5. **Who consumes it?** `format_knowledge_reachability_table(...)` and existing public/CLI callers through that function.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Knowledge Reachability district?** It only formats Knowledge Reachability rows and metadata.
8. **How is this distinct from Knowledge Reachability Slice 001 candidate admission?** It does not discover, filter, cap, or admit candidates; it formats completed rows and metadata.
9. **How is this distinct from Knowledge Reachability Slice 002 staged index construction?** It does not build or inspect indexes; it only formats existing metadata values.
10. **How is this distinct from Knowledge Reachability Slice 003 row evaluation?** It does not evaluate candidate flags or first-loss rows; it renders existing row fields.
11. **How is this distinct from prior Operational Graph slices?** It does not compose graph evidence, nodes, edges, confidence tiers, aggregate filtering, examples, or graph summary payloads.
12. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify emitters or build attribution rows/items.
13. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect emitted outputs, derive relationship status, or assemble emitted-item audit rows.
14. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate or diagnostic item families or matched consumer groups.
15. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, fan out pressure sources, score pressure, or produce pressure evidence payloads.
16. **How does this avoid Source Navigation direct work?** It only renders already completed Knowledge Reachability fields and does not query or format Source Navigation surfaces.
17. **How does this avoid Question Surface Inventory and bounded ask work?** It does not touch inventory, dispatch, bounded ask matching, or question routes; it only preserves human output.
18. **How does this preserve Knowledge Reachability JSON and table output?** Table output is delegated to a helper with the same formatting; JSON output is untouched.
19. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No diagnostic surface, registration, shape spec, CLI flag, or recordable output was added or changed.
20. **How does this preserve read-only and event-ledger behavior?** The helper consumes in-memory rows/metadata only; tests assert ledger event count remains unchanged.
21. **How is this distinct from any earlier slice in this batch?** Slice 004 owns metadata value assembly, Slice 005 owns JSON payload construction, and this slice owns human/table formatting.

## District boundary compliance

The slice remains local to Knowledge Reachability table/human formatting. It avoids metadata value production, JSON payload construction, candidate admission, index construction, row evaluation, diagnostic registration, CLI dispatch, Source Navigation direct work, Question Surface Inventory, bounded ask work, event-ledger mutation, and prior districts.
