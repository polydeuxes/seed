# Source Navigation Slice 001 — Source-navigation match-set assembly

## District consistency gate

- Active district verified: **Source Navigation**.
- Latest local district scout verified: **`source_navigation_district_scout_001.md`**.
- Handoff source verified: **`knowledge_reachability_outward_scout_003.md`**.
- Completed source district verified: **Knowledge Reachability**.
- No local report, summary, branch state, or inspected file pointed to a different active district for this slice.
- Knowledge Reachability reports were used only for the consistency gate/handoff identity, not as authority for Source Navigation internals.

## Selected boundary

Selected boundary: **source-navigation match-set assembly**.

The recovered responsibility is to collect Source Navigation rows matching an already prepared query, separate those matched rows into sorted definitions and sorted imports, and select sorted dependency mentions while preserving existing lookup semantics, sorting, public view fields, JSON output, human formatting, CLI behavior, and read-only behavior.

This was not a stop result because the responsibility was still compressed inside `_compose_source_navigation(...)` before the change and was directly supported by current implementation evidence.

## Implementation evidence

- `_prepare_source_navigation_query(...)` already owns external query normalization and source-row preparation, returning `_PreparedSourceNavigationQuery` with `normalized_query` and `source_rows` only.
- Before this slice, `_compose_source_navigation(...)` directly performed match collection, definition/import separation, sorting, dependency mention selection, bounded lookup detection, explanation assembly, and `SourceNavigationView` assembly in one function.
- `_matches(...)` already owns definition/import matching semantics for query, subject, path, qualified symbol, and short symbol lookup.
- `_dependency_mentions(...)` already owns import dependency mention predicate semantics.
- `_row_sort_key(...)` already owns row ordering.
- `SourceNavigationView`, `source_navigation_json(...)`, and `format_source_navigation(...)` remained public assembly/serialization/formatting consumers and were not moved or broadened.

## Before

`_compose_source_navigation(...)` consumed `_PreparedSourceNavigationQuery` and locally:

1. copied `normalized_query` and `source_rows`;
2. built `matched` via `_matches(...)`;
3. split and sorted definitions;
4. split and sorted imports;
5. selected and sorted dependency mentions via `_dependency_mentions(...)`;
6. calculated bounded lookup status;
7. assembled definition, dependency, support, and non-claim explanations;
8. assembled the public `SourceNavigationView`.

The match-set assembly responsibility was implementation-backed but not directly observable as its own handoff.

## After

- Added private `_SourceNavigationMatchSet` as the local artifact for match-set assembly.
- Added private `_assemble_source_navigation_match_set(...)` as the producer that consumes `_PreparedSourceNavigationQuery`, preserves `_matches(...)`, `_dependency_mentions(...)`, and `_row_sort_key(...)`, and returns sorted `definitions`, sorted `imports`, and sorted `dependency_mentions`.
- Kept `_compose_source_navigation(...)` responsible for bounded lookup detection, explanation assembly, and public `SourceNavigationView` assembly.

## Recovered producer

`_assemble_source_navigation_match_set(...)` now owns the recovered match-set assembly responsibility.

## Recovered artifact/helper

`_SourceNavigationMatchSet` is the private handoff artifact carrying:

- `definitions`;
- `imports`;
- `dependency_mentions`.

It does not carry explanation objects, public view metadata, JSON payloads, formatter text, CLI dispatch details, query preparation policy, or diagnostic registration data.

## Recovered consumer

`_compose_source_navigation(...)` consumes `_SourceNavigationMatchSet` and continues to assemble the public `SourceNavigationView` using the same explanation helpers and bounded rendering behavior.

## Compatibility preserved

Did any compatibility boundary change? **No.**

No public function signature changed. No public dataclass field changed. No CLI flag changed. No JSON key changed. No human formatter text changed intentionally. No event-ledger or mutation boundary changed.

## Files changed

- `seed_runtime/source_navigation.py`
- `tests/test_source_navigation.py`
- `source_navigation_slice_001.md`

## LOC changed

Implementation/test diff before this report showed:

- `seed_runtime/source_navigation.py`: 50 changed lines in diff, with 25 net new helper/artifact lines and local composition replacement.
- `tests/test_source_navigation.py`: 105 changed lines in diff, adding focused match-set/read-only coverage and a test fixture ledger hook.
- `source_navigation_slice_001.md`: new slice report.

## Tests executed

- `pytest -q tests/test_source_navigation.py` — passed, 32 tests.
- `python scripts/seed_local.py --observe-repository-source . --source-navigation state_summary` — passed and rendered the Source Navigation app output.

## Remaining compressed responsibilities directly evident without broad scouting

Inside `_compose_source_navigation(...)`, bounded path/module lookup detection and explanation/public-view assembly remain local to composition. Those were intentionally not recovered in this slice because bounded lookup policy must be reassessed after this slice lands and explanation/public-view assembly was out of scope.

## Required questions

1. **What responsibility was previously compressed?** Collecting matched Source Navigation rows from prepared rows, separating matched rows into definitions/imports, sorting them, and selecting dependency mentions.

2. **Which implementation-local ownership boundary became directly observable?** The source-navigation match-set assembly boundary between prepared query intake and public SourceNavigationView/explanation assembly.

3. **What producer now owns the recovered responsibility?** `_assemble_source_navigation_match_set(...)`.

4. **What artifact or helper carries the recovered boundary, if any?** `_SourceNavigationMatchSet` carries sorted `definitions`, sorted `imports`, and sorted `dependency_mentions`.

5. **Who consumes it?** `_compose_source_navigation(...)` consumes it.

6. **Did any compatibility boundary change?** **No.**

7. **How does this stay inside the Source Navigation district?** The change is confined to `seed_runtime/source_navigation.py`, Source Navigation tests, and this Source Navigation slice report. It only reorganizes Source Navigation source-fact lookup composition.

8. **How is this distinct from external query preparation?** `_prepare_source_navigation_query(...)` still strips the external query and prepares `SourceNavigationRow` objects from state fact supports. The new helper accepts that prepared handoff and does not normalize external input or read `State`.

9. **How is this distinct from FactSupport row preparation?** `_row_from_support(...)` still converts `FactSupport` into `SourceNavigationRow`. The new helper operates only on already prepared rows.

10. **How is this distinct from `_matches(...)` predicate internals?** The new helper calls `_matches(...)` unchanged. It does not alter matching conditions for subject, path, definition value, or final segment.

11. **How is this distinct from `_dependency_mentions(...)` predicate internals?** The new helper calls `_dependency_mentions(...)` unchanged. It does not alter import-only dependency mention logic.

12. **How is this distinct from bounded source-navigation lookup policy?** Bounded detection remains in `_compose_source_navigation(...)` and formatter behavior remains in existing formatting helpers. The new helper does not decide bounded rendering or bounded metadata visibility.

13. **How is this distinct from definition/dependency/support/non-claim explanation assembly?** Explanation helpers remain unchanged and are still called by `_compose_source_navigation(...)` after match-set assembly.

14. **How is this distinct from SourceNavigationView public assembly?** `_compose_source_navigation(...)` still constructs `SourceNavigationView`. `_SourceNavigationMatchSet` is private and carries only internal row groups.

15. **How is this distinct from Source Navigation JSON and human formatting?** `source_navigation_json(...)` and `format_source_navigation(...)` are unchanged. Tests compare composed/public JSON and human output to prove preservation.

16. **How is this distinct from Knowledge Reachability Slices 001 through 006?** It does not discover Knowledge Reachability candidates, build Knowledge Reachability indexes, evaluate Knowledge Reachability rows, assemble Knowledge Reachability metadata, build Knowledge Reachability JSON, or format Knowledge Reachability tables/human output.

17. **How is this distinct from prior Operational Graph slices?** It does not build graph nodes/edges, merge duplicate edges, filter confidence, produce confidence tiers, or assemble graph summary payloads.

18. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify unknown emitters, collect implementation evidence for emitters, or construct known/unknown emitter attribution rows.

19. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect scan results, derive emitted-output relationship status, produce unknown-emitter rows, produce scanned emitted-item rows, or assemble emitter/consumer audit output.

20. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate audit item families, diagnostic audit item families, or matched consumer groups.

21. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, fan out consumer-predicate sources, own pressure evidence payloads, score pressure findings, refuse positive findings, or select pressure item sets.

22. **How does this avoid Question Surface Inventory, bounded ask, and Inquiry Orientation work?** It touches no question-family registry, bounded ask dispatch, or inquiry-orientation note/material logic. It only rearranges private Source Navigation row grouping.

23. **How does this preserve Source Navigation JSON and human output?** The JSON serializer and human formatter are unchanged, and focused tests assert `_compose_source_navigation(...)` output remains identical to `build_source_navigation(...)` for JSON and formatted text.

24. **How does this preserve read-only and event-ledger behavior?** The new helper consumes in-memory prepared rows and returns a frozen private match-set. It does not inspect files, parse source, append events, or mutate state; tests assert source navigation leaves projected state and event ledger entries unchanged.

## District boundary compliance

This slice remains inside Source Navigation. It does not modify Knowledge Reachability, Operational Graph, Emitter Attribution Audit, Emitter/Consumer Audit, Consumer Dependency Audit, Pressure Audit, Question Surface Inventory, bounded ask dispatch, Inquiry Orientation, diagnostic inventory registration, diagnostic-shape registration, JSON serialization, human formatting, or CLI dispatch.

## Distinctions summary

- **External query preparation:** unchanged and still owned by `_prepare_source_navigation_query(...)`.
- **Predicate helpers:** unchanged and still owned by `_matches(...)` and `_dependency_mentions(...)`.
- **Bounded lookup policy:** unchanged and still evaluated outside the new helper.
- **Explanation assembly:** unchanged and still owned by existing explanation helpers called by `_compose_source_navigation(...)`.
- **Public view assembly:** unchanged and still owned by `_compose_source_navigation(...)`.
- **JSON and formatting:** unchanged and still owned by `source_navigation_json(...)` and `format_source_navigation(...)`.
- **Knowledge Reachability work:** untouched.
- **Operational Graph work:** untouched.
- **Emitter Attribution Audit work:** untouched.
- **Emitter/Consumer Audit work:** untouched.
- **Consumer Dependency Audit work:** untouched.
- **Frontier Pressure Admission work:** untouched.
- **Question Surface Inventory, bounded ask, Inquiry Orientation:** untouched.
