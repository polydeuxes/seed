# Consumer Dependency Audit District Scout 002

## Scope and read-only statement

This scout reassessed the current Consumer Dependency Audit district after Consumer Dependency Audit Slices 001 and 002. It was read-only with respect to implementation and tests: no implementation files were changed, no test files were changed, and no slice report or PR metadata was created. The only intended repository change is this scout report: `consumer_dependency_audit_district_scout_002.md`.

Scout report commit hash: `c23f90551d21d0b92cf64006dd9f029bdfca7b8f`.

## Commands and current app evidence

Commands run during the scout:

- `cat AGENTS.md`
- `rg "consumer dependency|consumer_dependency|_audit_item|_consumer_lookup_terms|_mentions_any_item|ConsumerAuditItem" -n .`
- `sed -n '1,340p' seed_runtime/consumer_dependency_audit.py`
- `sed -n '1,260p' tests/test_consumer_dependency_audit.py`
- `python scripts/seed_local.py --consumer-audit --format json | head -c 4000` (invalid flag; confirmed the app uses `--json`, not `--format json`)
- `python scripts/seed_local.py --consumer-audit --json`
- `python scripts/seed_local.py --consumer-audit --predicate filesystem_avail_bytes --json`
- `python scripts/seed_local.py --consumer-audit --diagnostic ownership_discrepancies --json`
- `git status --short`

Current app evidence from `python scripts/seed_local.py --consumer-audit --json`:

- Summary: `items_scanned=128`, `orphaned_items=27`, `single_consumer_items=13`, `multi_consumer_items=88`.
- Metadata discovery says observation predicates come from observation inventory, diagnostics from diagnostic inventory, and consumers from implementation source mentions.
- Metadata consumer evidence lists five source-consumer groups: `projection_builders`, `read_models`, `diagnostics`, `state_build`, and `views`.

Current focused diagnostic-filter evidence from `python scripts/seed_local.py --consumer-audit --diagnostic ownership_discrepancies --json`:

- One `diagnostic` item is emitted for `ownership_discrepancies`.
- Consumers are `diagnostics`, `state_build`, and `views`.
- The item is not orphaned and is highlighted as `widely used`.

Current focused predicate-filter evidence from `python scripts/seed_local.py --consumer-audit --predicate filesystem_avail_bytes --json`:

- The current app returned zero items for this predicate in this checkout state.
- This did not support any new ownership boundary by itself; it only confirmed filter behavior can produce an empty item set.

## Recently consumed Consumer Dependency Audit boundaries

The following boundaries are already recovered and unavailable for this scout:

1. Observation-predicate audit item-family production via `_observation_predicate_audit_items(...)`.
2. Diagnostic audit item-family production via `_diagnostic_audit_items(...)`.

These are treated as consumed work and are not proposed again under alternate labels.

## Prior Frontier Pressure Admission boundaries and stopped neighborhoods respected

This scout avoided re-slicing prior Frontier Pressure Admission work, including:

- pressure-audit candidate admission;
- consumer-predicate source fan-out from pressure-audit;
- orphaned-predicate and fragile-predicate pressure evidence payload ownership;
- orphaned-predicate and fragile-predicate pressure score production;
- orphaned-predicate and fragile-predicate positive-finding refusal;
- orphaned-predicate and fragile-predicate item-set selection.

The scout also respected stopped or exhausted neighborhoods:

- Slice 035: `selection_path_audit` neighborhood exhausted.
- Slice 051: immediate diagnostic-shape pressure candidate-construction pocket exhausted.
- District Scout 004: immediate post-Slice-062 pressure-audit neighborhood exhausted for safe local recovery.
- Outward Scout 005: Frontier Pressure Admission pressure-audit district has zero immediate recoverable candidates.

No candidate below lives in pressure-audit fan-out or pressure candidate admission. All accepted or rejected neighborhoods are evaluated inside `seed_runtime/consumer_dependency_audit.py` and its public `seed --consumer-audit` surface.

## Inspected consumer-audit neighborhoods

### 1. Per-item source-consumer matching in `_audit_item(...)`

Implementation evidence:

- `_audit_item(...)` receives an item, kind, source groups, and repo root.
- It asks `_consumer_lookup_terms(...)` for lookup terms.
- It iterates each consumer source group from `_read_sources(...)`.
- It calls `_mentions_any_item(files.values(), aliases)` for each group.
- It builds a tuple of matched consumer group names and constructs `ConsumerAuditItem(item=item, kind=kind, consumers=tuple(consumers))`.

Assessment:

This is a current, implementation-backed compressed responsibility. Lookup-term ownership and low-level mention expansion are already separate helpers, but the group-level matching responsibility remains inside `_audit_item(...)`: consume `sources` and lookup terms, emit ordered matched consumer group names for the item. A compatibility-preserving slice could recover a helper such as matched-consumer-group construction without changing schema, CLI, JSON, human output, event-ledger behavior, read-only behavior, or item ordering.

Classification: **Independent**.

Confidence: **High**.

Rank: **A. Strong implementation-backed next slice**.

Why it is not a re-slice: it does not recover observation-predicate item-family production or diagnostic item-family production; it also does not recover `_consumer_lookup_terms(...)` or `_mentions_any_item(...)`. It isolates the still-inline producer/consumer handoff between per-item lookup terms and `ConsumerAuditItem.consumers`.

Why it is not merely a name: the current implementation performs concrete source group iteration and produces public JSON/human-visible consumer group values, counts, orphan status, and highlights.

Would it still be valid without other candidates? **Yes**. It can be recovered alone by preserving `_audit_item(...)` as the item constructor and moving only matched consumer group production behind a helper.

### 2. Lookup-term handoff and alias construction in `_consumer_lookup_terms(...)`

Implementation evidence:

- `_consumer_lookup_terms(...)` already exists.
- It owns exact predicate terms, catalog lookup from `predicate_catalog/core.json`, canonical predicate mapping, and returns a `frozenset`.
- Tests already protect canonical predicate consumer matching behavior.

Assessment:

This neighborhood is already separated. There may be future behavior work if matching semantics are wrong, but this scout found no compressed implementation-local ownership boundary distinct from the existing helper. Splitting catalog lookup from base term creation would be cosmetic unless new implementation evidence shows separate producer/consumer pressure.

Classification: **Invalid**.

Confidence: **High**.

Rank: **C. Already separated / likely re-slice**.

Why rejected: re-slicing `_consumer_lookup_terms(...)` would rename or subdivide existing helper ownership rather than recover a still-compressed boundary.

### 3. Low-level source membership and string-form expansion in `_mentions_any_item(...)`

Implementation evidence:

- `_mentions_any_item(...)` already exists.
- It expands each lookup item into raw, JSON-quoted, `repr`, and hyphenated forms.
- It checks whether any expanded needle appears in any source string.

Assessment:

This neighborhood is already separated from `_audit_item(...)`. It is distinct from item-family production, but it is not a new recoverable ownership boundary because the helper already owns low-level mention matching. Further extraction of needle expansion from source scanning would be cosmetic without recurrence or implementation evidence of separate consumers.

Classification: **Invalid**.

Confidence: **High**.

Rank: **C. Already separated / likely re-slice**.

Why rejected: the responsibility is already owned by `_mentions_any_item(...)`; splitting it now would likely be a cosmetic re-slice.

### 4. Source file scanning in `_read_sources(...)` and `_read(...)`

Implementation evidence:

- `CONSUMER_PATHS` declares named consumer groups and their file paths.
- `_read_sources(root)` converts those paths into a nested dictionary of consumer group to file path to text.
- `_read(path)` reads text or returns an empty string when the path does not exist.
- `build_consumer_audit(...)` calls `_read_sources(repo_root)` once and passes sources to both recovered item-family producers.

Assessment:

Source file scanning is already separated into `_read_sources(...)` and `_read(...)`. The app evidence confirms consumer evidence metadata exposes the same consumer groups. A future slice could adjust behavior if missing files or consumer path metadata require a change, but this scout found no still-compressed local ownership boundary. The declaration-to-read conversion is cohesive and already a helper.

Classification: **Invalid**.

Confidence: **High**.

Rank: **C. Already separated / likely re-slice**.

Why rejected: existing helper boundaries already separate source scanning from item-family production and per-item matching.

### 5. Final audit sorting, metadata, summary, JSON, and human output

Implementation evidence:

- `build_consumer_audit(...)` still owns orchestration, final sorting by `(item.kind, item.item)`, and metadata construction.
- `ConsumerAudit.summary` derives counts from items.
- `ConsumerAudit.to_json_dict()` owns public JSON envelope shape.
- `ConsumerAuditItem.to_json_dict()` owns per-item public JSON fields.
- `format_consumer_audit(...)` owns human-readable output.

Assessment:

This neighborhood is public-output-adjacent, but it is not a safe implementation-local ownership slice for the next command. Sorting and metadata are orchestration details in `build_consumer_audit(...)`; summary/JSON/human output are already separate methods/functions. Extracting metadata production alone would be cosmetic. Extracting output rendering would be a risky public surface refactor without a compressed producer/consumer handoff. No app evidence showed a distinct local ownership seam that needs recovery.

Classification: **Invalid**.

Confidence: **Medium**.

Rank: **D. Cosmetic only**.

Why rejected: this is either already separated public serialization/rendering or orchestration glue, not one compressed implementation-local responsibility.

## Candidate boundaries found

### Candidate 1: matched consumer group construction for a single audit item

Boundary statement:

Recover the group-level matching responsibility currently inline in `_audit_item(...)`: consume source groups and resolved lookup terms, produce the ordered tuple/list of consumer group names that mention the item.

Producer/consumer relationship:

- Producer: candidate matched-consumer-group helper would produce matched group names from `sources` and aliases.
- Consumer: `_audit_item(...)` would consume the matched group names to construct `ConsumerAuditItem`.

Classification: **Independent**.

Confidence: **High**.

Rank: **A. Strong implementation-backed next slice**.

Compatibility notes:

- Preserve source group iteration order from `CONSUMER_PATHS`.
- Preserve `_consumer_lookup_terms(...)` and `_mentions_any_item(...)` behavior.
- Preserve `ConsumerAuditItem` construction and all derived public fields.
- Preserve CLI, JSON, human output, diagnostic inventory/shape-audit visibility, event-ledger non-mutation, read-only behavior, filters, sorting, and metadata.

Why not a re-slice:

- It is not observation-predicate or diagnostic item-family production.
- It is not pressure-audit fan-out from Slice 037.
- It is not lookup-term construction or low-level mention matching, both of which already have helpers.

Why not merely a name:

- The current implementation has executable behavior: it loops over concrete source groups, tests file contents, and emits concrete consumer group names consumed by public output and pressure-adjacent audits.

Would it still be valid if other proposed candidates were not recovered?

- **Yes**. It is the only safe candidate found and does not depend on any other proposed work.

## Rejected candidates and why

| Candidate | Classification | Confidence | Rank | Reason rejected |
| --- | --- | --- | --- | --- |
| Lookup-term construction split | Invalid | High | C | `_consumer_lookup_terms(...)` already owns this boundary; splitting catalog mapping or base terms would be a re-slice/cosmetic subdivision. |
| Low-level mention matching split | Invalid | High | C | `_mentions_any_item(...)` already owns string-form expansion and source membership checks. |
| Source file scanning split | Invalid | High | C | `_read_sources(...)` and `_read(...)` already separate source loading from matching and item production. |
| ConsumerAuditItem JSON/derived properties | Invalid | Medium | C/D | Per-item schema and derived properties are already owned by the dataclass methods/properties; no compressed handoff found. |
| Final sorting and metadata extraction | Invalid | Medium | D | Sorting/metadata remain orchestration glue; extracting them would not recover a distinct implementation-backed ownership boundary. |
| Public human-readable formatter extraction | Invalid | Medium | D | `format_consumer_audit(...)` already owns human rendering; further extraction would be cosmetic and public-output risky. |

## Candidate independence answer

How many recoverable candidates currently exist?

**1**

For each candidate:

1. **Matched consumer group construction for a single audit item**
   - Classification: **Independent**.
   - Confidence: **High**.
   - Why it is not a re-slice: it is not either consumed item-family producer, not existing lookup-term construction, not existing low-level mention matching, and not prior pressure-audit Slice 037 fan-out.
   - Why it is not merely a name: it corresponds to the current loop that converts source groups plus aliases into public consumer group names and all downstream count/orphan/highlight effects.
   - Valid without other candidates: **Yes**.

Fewer than three implementation-backed candidates are supported. Only one candidate is safe.

## Batch Efficiency Gate

Next move classification: **Single-slice target**.

This is **not** an efficiency batch because three recoverable candidates do not exist. It is **not** a protection batch because two recoverable candidates do not exist. Running a batch is not worth it for speed or process protection in this district right now; it would increase the risk of cosmetic extraction or re-slicing prior work.

Recommended batch size: **1**.

## Recommended next command

Perform one guarded Consumer Dependency Audit slice recovering matched consumer group construction for a single audit item from `_audit_item(...)` while preserving behavior exactly.

Suggested slice constraint:

- Do not change `_consumer_lookup_terms(...)` semantics.
- Do not change `_mentions_any_item(...)` semantics.
- Do not change `_observation_predicate_audit_items(...)` or `_diagnostic_audit_items(...)` except for compatibility-preserving call flow if unavoidable.
- Add/update focused tests proving matched consumer group construction preserves source group ordering, exact consumers, orphan behavior, and public JSON/human output through `build_consumer_audit(...)`.

## Risk of re-slicing prior work

Risk is **medium** if the next command is not tightly scoped, because `_audit_item(...)`, `_consumer_lookup_terms(...)`, and `_mentions_any_item(...)` are adjacent and already named. The safe boundary is only the still-inline group-level matching responsibility inside `_audit_item(...)`. Any attempt to rework item-family production, pressure-audit fan-out, lookup-term mapping, mention expansion, output schemas, or final metadata would risk re-slicing consumed or already-separated work.

## Final scout conclusion

The Consumer Dependency Audit district has exactly one nearby implementation-backed recoverable candidate after Slices 001 and 002: matched consumer group construction for a single audit item. The next command should be a single slice, not a batch. If that slice lands, the district should be reassessed before proposing further local work; based on this scout, remaining nearby neighborhoods are already separated, cosmetic, or likely re-slices.
