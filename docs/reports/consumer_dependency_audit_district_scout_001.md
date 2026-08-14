# Consumer Dependency Audit District Scout 001

## Scope and rule compliance

This was a read-only district scout for the consumer dependency audit district, starting from the live app surface behind `seed --consumer-audit`. No implementation files were changed. No test files were changed. This is a scout report, not a slice report.

The stopped Frontier Pressure Admission neighborhoods were respected: no work continued in `seed_runtime/pressure_audit.py`, no Slice 063 was created, and the exhausted pressure-audit neighborhoods from Slice 035, Slice 051, District Scout 004, and Outward Scout 005 were not mined for new local pressure-audit recovery.

Prior Frontier Pressure Admission boundaries were avoided, including pressure-audit candidate admission, pressure-audit consumer-predicate source fan-out, orphaned/fragile predicate pressure evidence payloads, orphaned/fragile pressure scoring, positive-finding refusal, and orphaned/fragile item-set selection. In particular, Slice 037 is treated as downstream pressure-audit fan-out from a single `build_consumer_audit(root)` call, not as ownership of consumer-audit internals.

## Current app evidence

Commands inspected:

```text
python scripts/seed_local.py --pressure-audit --json | python -m json.tool | head -100
python scripts/seed_local.py --consumer-audit --json | python -m json.tool | head -120
```

Current pressure-audit output still recommends `seed --consumer-audit` for two live pressures:

- `Orphaned Predicates`, score `26`, recommended command `seed --consumer-audit`.
- `Fragile Predicates`, score `13`, recommended command `seed --consumer-audit`.

The public consumer-audit app path is implementation-backed: the CLI flag is registered as `--consumer-audit`, and the command builds `build_consumer_audit(predicate_filter=args.predicate, diagnostic_filter=args.diagnostic)` before printing JSON or human-readable output.

## Implementation evidence map

Consumer dependency audit currently lives in `seed_runtime/consumer_dependency_audit.py`.

Key implementation evidence:

- `ConsumerAuditItem` owns item identity, kind, consumers, count/orphan/highlight derived properties, and per-item JSON fields.
- `ConsumerAudit` owns the tuple of items, metadata, summary counts, and top-level JSON fields.
- `CONSUMER_PATHS` declares consumer groups and source files scanned for implementation mentions.
- `build_consumer_audit(...)` reads sources once, conditionally produces observation-predicate items when `diagnostic_filter is None`, conditionally produces diagnostic items when `predicate_filter is None`, sorts the combined items by `(kind, item)`, and constructs metadata.
- `_audit_item(...)` owns per-item consumer matching by resolving lookup terms and scanning consumer source groups.
- `_consumer_lookup_terms(...)` owns exact lookup-term construction, including canonical predicate mappings from `predicate_catalog/core.json`.
- `_mentions_any_item(...)` owns low-level string-form expansion and source membership checks.
- `consumer_audit_json(...)` and `format_consumer_audit(...)` expose public JSON and human-readable output.

Existing tests already cover consumer discovery fixtures, orphan detection, multi-consumer counts, diagnostic filtering, empty behavior, canonical predicate mapping without prefix matching, listener predicate diagnostic consumers, JSON shape, and human output. That means several nearby responsibilities are already protected, even when not separately owned by helper boundaries.

## Inspected neighborhoods

### 1. Observation-predicate audit item production

Classification: **A. Strong implementation-backed next slice**

Current evidence: `build_consumer_audit(...)` directly performs observation inventory collection and appends `ConsumerAuditItem(kind="observation_predicate")` rows inline when `diagnostic_filter is None`.

Still-compressed responsibility: yes. The producer responsibility combines observation inventory access, predicate-filter handoff, item kind assignment, and append-loop construction inside the top-level build orchestration.

Implementation-backed: yes. It emits concrete public audit rows consumed by JSON/human output and downstream pressure-audit categories.

Distinct from prior Frontier Pressure Admission work: yes. Slice 037 recovered pressure-audit's single source collection/fan-out into pressure candidates. This candidate is inside consumer-audit item-family production and does not touch pressure-audit fan-out, orphaned/fragile selection, scoring, refusal, or evidence payload ownership.

Distinct from prior consumer-audit work: likely yes. Tests protect behavior, but no separate observation-predicate item-family producer exists in `seed_runtime/consumer_dependency_audit.py`.

Compatibility preservation: likely straightforward if extracted as a helper returning observation-predicate `ConsumerAuditItem` rows and preserving source reuse, filters, tuple/list ordering after final sort, schema, CLI, diagnostic behavior, and read-only behavior.

Independence: **Independent**. It remains valid even if diagnostic item production and matching are not recovered.

Confidence: **High**.

Why not a re-slice: it is upstream of pressure-audit categories and does not alter or split the pressure-audit candidate helpers recovered by prior Frontier Pressure Admission slices.

Why not merely a name: it produces actual audit rows with public `kind`, `item`, `consumers`, `consumer_count`, `orphaned`, and `highlight` fields.

### 2. Diagnostic audit item production

Classification: **B. Possible but needs caution**

Current evidence: `build_consumer_audit(...)` directly enumerates `DIAGNOSTIC_INVENTORY`, applies `diagnostic_filter`, and appends `ConsumerAuditItem(kind="diagnostic")` rows inline when `predicate_filter is None`.

Still-compressed responsibility: yes. Diagnostic inventory enumeration, diagnostic filtering, item kind assignment, and row construction are mixed into top-level orchestration.

Implementation-backed: yes. It emits concrete public `kind="diagnostic"` consumer-audit rows and is covered by diagnostic-filter tests.

Distinct from prior Frontier Pressure Admission work: yes. Frontier Pressure Admission pressure categories currently consume only `kind == "observation_predicate"` rows for orphaned and fragile pressure. Diagnostic row production inside consumer-audit is not pressure-audit fan-out, item-set selection, scoring, refusal, or pressure evidence payload ownership.

Distinct from prior consumer-audit work: likely yes. The behavior is tested, but no separate diagnostic item-family producer exists.

Compatibility preservation: likely straightforward if extracted after or alongside observation item production; must preserve `predicate_filter is None` gating, `diagnostic_filter` semantics, final sorting, JSON/human schema, and read-only behavior.

Independence: **Independent**, but weaker than candidate 1 because it shares the same top-level build orchestration and final aggregation. It remains valid if candidate 1 is not recovered, provided the extraction is limited to diagnostic rows only.

Confidence: **Medium-High**.

Why not a re-slice: it does not overlap the prior predicate-pressure work and does not rework downstream pressure-audit consumers.

Why not merely a name: it produces actual public diagnostic audit items, including concrete consumers and derived counts.

### 3. Per-item source-consumer matching

Classification: **B. Possible but needs caution**

Current evidence: `_audit_item(...)` resolves lookup terms, scans each consumer source group from `_read_sources(...)`, applies `_mentions_any_item(...)`, and returns a `ConsumerAuditItem` with matched consumer group names.

Still-compressed responsibility: partially. The helper already exists, so the boundary is not absent. However, lookup-term construction and source-consumer matching are still coupled in one per-item builder.

Implementation-backed: yes. Existing fixture tests prove implementation source mentions become consumer groups, orphaned items remain empty, multi-consumer counts work, canonical mappings are honored, and listener predicates are credited to diagnostics.

Distinct from prior Frontier Pressure Admission work: yes. This is upstream consumer-audit matching, not pressure-audit admission or pressure category selection.

Distinct from prior consumer-audit work: caution. `_audit_item(...)`, `_consumer_lookup_terms(...)`, and `_mentions_any_item(...)` already separate some responsibilities. A slice here could easily become a re-slice or cosmetic refactor unless it recovers a narrowly defined matching boundary such as `matched_consumer_groups(...)` while preserving existing lookup-term and string-form responsibilities.

Compatibility preservation: possible but higher risk. Must preserve exact consumer order from `CONSUMER_PATHS`, exact lookup-term expansion, source read behavior, schema, and all existing tests.

Independence: **Sequential**. It should be reassessed after one item-family producer slice because extracting item-family production may clarify whether matching needs any further ownership recovery.

Confidence: **Medium**.

Why not a re-slice: a valid future slice would need to recover only the matching responsibility inside consumer-audit, not the already separated canonical lookup-term helper or pressure-audit use of matched rows.

Why not merely a name: the matching result determines the concrete `consumers` tuple, `consumer_count`, orphan status, highlight, and downstream pressure eligibility.

### 4. Lookup-term construction

Classification: **C. Already separated / likely re-slice**

Current evidence: `_consumer_lookup_terms(...)` already owns exact lookup-term construction and canonical predicate mappings. Tests already prove canonical mapping is used without broad prefix matching.

Still-compressed responsibility: no strong evidence. The boundary is already represented by a dedicated helper and direct tests.

Independence: **Invalid** for immediate recovery.

Confidence: **High** that this should not be the next slice.

Why not a re-slice: attempting to recover it now would likely rename or reshuffle an existing ownership helper rather than recover a compressed boundary.

Why not merely a name: the implementation is real, but already separated.

### 5. Metadata, sorting/aggregation, and public output

Classification: **C/D. Already separated or cosmetic only**

Current evidence: final sorting and metadata construction are inline in `build_consumer_audit(...)`; summary and JSON are owned by `ConsumerAudit`; human formatting is owned by `format_consumer_audit(...)`.

Still-compressed responsibility: weak. Sorting and metadata are small final assembly details. Public JSON and human output already have explicit functions and dataclass methods.

Implementation-backed: yes, but mostly presentation/aggregation rather than a clear ownership boundary.

Independence: **Invalid** for the next slice.

Confidence: **Medium-High**.

Why not a re-slice: extracting summary, JSON, or human formatting would duplicate already separated methods/functions.

Why not merely a name: while output is concrete, the remaining inline pieces are not strong enough as an ownership-recovery slice; they are more likely cleanup.

## Candidate queue and independence answers

How many recoverable candidates currently exist? **2 safe candidates, plus 1 cautionary sequential candidate.**

| Rank | Candidate | Classification | Confidence | Still valid without the others? | Not a re-slice | Not merely a name |
| --- | --- | --- | --- | --- | --- | --- |
| A | Observation-predicate audit item production | Independent | High | Yes | Lives inside consumer-audit item-family production, not pressure-audit fan-out or pressure candidate selection | Emits concrete public `observation_predicate` audit rows and downstream pressure input |
| B | Diagnostic audit item production | Independent | Medium-High | Yes | Diagnostic rows are not prior predicate-pressure ownership and not Slice 037 fan-out | Emits concrete public `diagnostic` audit rows with consumers and counts |
| B | Per-item source-consumer matching | Sequential | Medium | Maybe, but should be reassessed after an item-family slice | Would need to avoid existing `_consumer_lookup_terms(...)` and `_mentions_any_item(...)` boundaries | Determines concrete consumer groups, counts, orphan status, and pressure eligibility |
| C | Lookup-term construction | Invalid / already separated | High | Not applicable | Existing helper and tests already own it | Real behavior, but not compressed |
| C/D | Sorting, metadata, JSON, and human output | Invalid / cosmetic or already separated | Medium-High | Not applicable | Existing dataclass methods/functions already own most output shape | Concrete output, but not a strong ownership-recovery boundary |

## Batch efficiency gate

Result: **Protection batch**, not an efficiency batch.

- Recoverable candidates currently safe enough: **2**.
- Candidate 1 and candidate 2 are independent and can be recovered as a guarded two-slice protection batch if the next command is allowed to batch.
- Candidate 3 is not safe enough for the same batch. It is sequential and should be reassessed after item-family producer extraction.
- Because only two safe candidates exist, batching would protect correctness by keeping sibling item-family boundaries aligned, but it does **not** save command count compared to older one-slice prompting.

Recommended batch size if batching is chosen: **2**.

Recommended next command: perform a guarded consumer dependency audit protection batch recovering:

1. observation-predicate audit item production; and
2. diagnostic audit item production.

The batch must preserve public CLI, JSON, human-readable output, diagnostic inventory/shape-audit visibility, event-ledger non-mutation, read-only behavior, filter semantics, item sorting, metadata, and all existing consumer dependency audit tests.

If avoiding protection batching, the single strongest next slice is **observation-predicate audit item production**.

## Risk of re-slicing prior work

Risk is **low-to-medium** for the two item-family candidates because both are inside `seed_runtime/consumer_dependency_audit.py`, while the avoided prior Frontier Pressure Admission slices live in pressure-audit candidate admission, pressure-audit consumer fan-out, predicate pressure item selection, evidence payloads, scoring, and refusal. The risk rises if a future command drifts back into `seed_runtime/pressure_audit.py` or tries to recover orphaned/fragile predicate pressure behavior from consumer-audit rows.

Risk is **medium-high** for per-item matching because `_audit_item(...)`, `_consumer_lookup_terms(...)`, and `_mentions_any_item(...)` already expose helper boundaries. Any matching slice must define a genuinely compressed responsibility rather than rename existing helpers.

Risk is **high** for lookup-term construction and output formatting because those neighborhoods are already separated or presentation-only.

## Explicit file-change statement

No implementation files were changed. No test files were changed. The only intended repository change is this scout report markdown file: `consumer_dependency_audit_district_scout_001.md`.

## Scout report commit hash

Commit hash: recorded in the git commit that adds this report.
