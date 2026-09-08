# Knowledge Reachability Slice 005 — JSON payload construction

## District consistency gate

- Active district verified: **Knowledge Reachability**.
- Latest relevant completed slice verified: **`knowledge_reachability_slice_004.md`**, after prior verification of `knowledge_reachability_slice_003.md` and `knowledge_reachability_district_scout_001.md`.
- Post-Slice-004 reassessment inspected `seed_runtime/knowledge_reachability.py` and `knowledge_reachability_json(...)`.
- Branch and local files did not point to another active district. Unrelated district reports were not used as authority.

## Selected boundary

JSON payload construction.

## Reassessment result

After Slice 004, `knowledge_reachability_json(...)` still contained one narrow implementation-local ownership boundary: converting completed rows and completed metadata into the existing public JSON-compatible payload. This is not metadata value production, candidate admission, index construction, row evaluation, table formatting, diagnostic registration, CLI dispatch, Source Navigation, Question Surface Inventory, or bounded ask dispatch. Compatibility can be preserved without schema or behavior changes.

## Implementation evidence

The JSON function converted rows with `asdict(row)`, converted metadata with `asdict(metadata)`, added compatibility aliases `timing` and `candidates`, preserved the `load state/cache` timing alias, and returned either row-only or metadata-plus-rows shapes.

## Before

`knowledge_reachability_json(...)` directly owned row dictionary construction, metadata dictionary construction, compatibility aliases, and return-shape branching.

## After

`_knowledge_reachability_json_payload(...)` owns construction of the existing JSON-compatible payload. The public `knowledge_reachability_json(...)` remains as the compatibility entry point and delegates unchanged behavior.

## Recovered producer

`_knowledge_reachability_json_payload(...)`.

## Recovered artifact/helper

The helper returns the existing JSON-compatible artifact: either `list[dict[str, Any]]` for row-only output or `{"metadata": ..., "rows": ...}` when metadata is provided.

## Recovered consumer

`knowledge_reachability_json(...)` consumes the helper result as the public API. CLI JSON behavior and bounded ask compatibility continue to use the public API path.

## Compatibility preserved

No.

Row dictionaries, metadata dictionary keys, `timing` compatibility alias, `candidates` compatibility alias, row-only return shape, metadata-plus-rows return shape, CLI-like JSON behavior, diagnostic-shape expectations, read-only metadata, and event-ledger non-mutation are preserved.

## Files changed

- `seed_runtime/knowledge_reachability.py`
- `tests/test_knowledge_reachability.py`
- `knowledge_reachability_slice_005.md`

## LOC changed

Slice 005 implementation/test diff before this report: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py` changed with 86 insertions and 0 deletions.

## Tests executed

- `pytest -q tests/test_knowledge_reachability.py` — passed.

Focused coverage proves row dictionary construction, metadata dictionary construction, `timing` alias, `load state/cache` alias, `candidates` alias, row-only return shape, metadata-plus-rows return shape, CLI-like JSON serialization behavior, diagnostic-shape-compatible metadata keys, read-only metadata, and event-ledger non-mutation.

## Remaining compressed responsibilities

After this slice, direct implementation evidence still shows `format_knowledge_reachability_table(...)` owns table/human formatting. It requires reassessment before recovery because it is a sequential medium-confidence candidate.

## Required questions

1. **What responsibility was previously compressed?** Knowledge Reachability JSON-compatible payload construction from completed rows and metadata.
2. **Which implementation-local ownership boundary became directly observable?** Row/metadata dictionary serialization and compatibility alias assembly for Knowledge Reachability JSON output.
3. **What producer now owns the recovered responsibility?** `_knowledge_reachability_json_payload(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The helper carries the boundary and returns the existing JSON-compatible row-only or metadata-plus-rows payload.
5. **Who consumes it?** `knowledge_reachability_json(...)` and existing public/CLI callers through that function.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Knowledge Reachability district?** It only serializes Knowledge Reachability rows and metadata.
8. **How is this distinct from Knowledge Reachability Slice 001 candidate admission?** It does not discover, filter, cap, or admit candidates; it serializes completed rows and metadata.
9. **How is this distinct from Knowledge Reachability Slice 002 staged index construction?** It does not build or inspect indexes; it serializes already completed metadata fields.
10. **How is this distinct from Knowledge Reachability Slice 003 row evaluation?** It does not evaluate candidate flags or first-loss rows; it converts existing row objects to dictionaries.
11. **How is this distinct from prior Operational Graph slices?** It does not compose graph evidence, nodes, edges, confidence tiers, aggregate filtering, examples, or graph summary payloads.
12. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify emitters or build attribution rows/items.
13. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect emitted outputs, derive relationship status, or assemble emitted-item audit rows.
14. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate or diagnostic item families or matched consumer groups.
15. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, fan out pressure sources, score pressure, or produce pressure evidence payloads.
16. **How does this avoid Source Navigation direct work?** It serializes already completed Knowledge Reachability payloads and does not query or format Source Navigation.
17. **How does this avoid Question Surface Inventory and bounded ask work?** It does not touch inventory, dispatch, bounded ask matching, or question routes; it only preserves the JSON shape they can consume.
18. **How does this preserve Knowledge Reachability JSON and table output?** JSON output is delegated to a helper with the same payload construction; table output is untouched.
19. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No diagnostic surface, registration, shape spec, CLI flag, or recordable output was added or changed.
20. **How does this preserve read-only and event-ledger behavior?** The helper consumes in-memory rows/metadata only; tests assert ledger event count remains unchanged.
21. **How is this distinct from any earlier slice in this batch?** Slice 004 owns metadata value assembly; this slice owns JSON serialization of already completed rows and metadata.

## District boundary compliance

The slice remains local to Knowledge Reachability JSON payload construction. It avoids metadata value production, candidate admission, index construction, row evaluation, table formatting, diagnostic registration, CLI dispatch, Source Navigation direct work, Question Surface Inventory, bounded ask work, event-ledger mutation, and prior districts.
