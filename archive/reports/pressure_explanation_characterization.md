# Pressure Explanation Characterization

## Executive answer

The implementation does **not** currently expose a dedicated Pressure Explanation owner that turns Pressure evidence into one qualitative explanation chain for each pressure item.

Pressure itself already performs a bounded amount of explanation work: each category-specific pressure builder selects upstream diagnostic evidence, computes a score, writes a short `reason`, and points to a recommended inspection command. That work is implementation-visible, not merely presentation.

However, the broader chain an operator asks for — why this pressure exists, which evidence contributes, which diagnostics participate, which architectural boundary is compressed, and which recovery direction naturally follows — is still composed across multiple surfaces. The closest recurring owner is **reasoning-path / operational-story composition**, not `pressure_audit.py` alone. Those surfaces reuse pressure output plus ownership discrepancies, capability needs, privilege discovery, correlation, impact, and investigation-path inputs, but they do not provide a pressure-item-specific explanation boundary.

Therefore the supported conclusion is:

> Pressure evidence and short pressure reason are currently compressed inside category-specific pressure candidate builders. A recurring explanation-composition behavior exists in `reasoning_path_audit.py` and `operational_story.py`, but the implementation does not yet demonstrate exactly one bounded Pressure Explanation owner separated from Pressure Evidence.

## Implementation evidence reviewed

Implementation files reviewed:

- `seed_runtime/pressure_audit.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/consumer_dependency_audit.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/diagnostic_inventory.py`
- `scripts/seed_local.py`

Tests reviewed:

- `tests/test_pressure_audit.py`
- `tests/test_reasoning_path_audit.py`
- `tests/test_operational_story.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

Repository characterization/audit artifacts reviewed:

- `pressure_audit_slice_001.md`
- `pressure_evidence_characterization.md`
- `pressure_audit_responsibility_characterization.md`
- `pressure_audit_smallest_owner_investigation.md`
- `pressure_visibility_evidence_classification_boundary_investigation.md`
- selected pressure-related files under `docs/`

App commands used during the audit:

```bash
python scripts/seed_local.py --pressure-audit --json
python scripts/seed_local.py --reasoning-path capability listener_process_inventory --json
```

## Current pressure explanation path

### 1. Pressure audit owns pressure item construction

`build_pressure_audit()` gathers candidates from five category-specific builders:

- diagnostic shape;
- ownership attribution;
- capability;
- orphaned predicates;
- fragile predicates.

Each candidate becomes a public `PressureItem` with the same fields:

- `category`;
- `score`;
- `evidence`;
- `reason`;
- `recommended_command`.

This means current Pressure output is not raw evidence only. It already contains a short implementation-authored reason per category.

### 2. Category builders combine scoring, evidence selection, reason text, and next inspection

Each pressure category constructs four responsibilities together:

1. select upstream diagnostic or implementation evidence;
2. compute score;
3. compose a short reason sentence;
4. choose the recommended command.

Examples:

- Diagnostic Shape pressure reads `build_diagnostic_shape_audit()`, summarizes it, scores mismatches/warnings/unknowns, emits count evidence, and writes the reason about visibility-contract rows not being consistent.
- Ownership Attribution pressure reads `build_ownership_discrepancies()`, counts conflict kinds, emits dominant conflict evidence, and writes the reason about unresolved ownership rows.
- Capability pressure reads `build_capability_needs()`, counts subject occurrences, emits capability frequency, affected subjects, and affected diagnostics, and writes the reason about missing observation capability and top need.
- Orphaned and Fragile Predicate pressure both read `build_consumer_audit()`, filter observation predicates, emit predicate lists/counts, and write reasons about absent or single implementation consumers.

This is recurring implementation behavior, but it is repeated per category rather than centralized as a pressure explanation boundary.

### 3. Formatting is presentation-only for existing fields

`format_pressure_audit()` renders the fields already present on each `PressureItem`. It does not derive additional explanation chains. It prints evidence key/value pairs, the prebuilt reason, and the recommended inspection command.

Therefore Pressure explanation sentences are not merely formatting. They are constructed before rendering, inside pressure item construction.

### 4. Broader explanation chains are composed outside pressure audit

The implementation has two nearby composition surfaces:

- `reasoning_path_audit.py` builds derivation paths from ownership discrepancies, capability needs, pressure audit, privilege discovery, and operational story.
- `operational_story.py` builds a broad current story from pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path.

These surfaces demonstrate recurring explanation-composition behavior, but their ownership is broader than Pressure. They are not a separated `Pressure Explanation` owner for each pressure category.

## Evidence-chain characterization

### Capability pressure chain

Capability pressure starts with `build_capability_needs(state)`.

`build_capability_needs()` derives needs from two places:

1. current `build_ownership_discrepancies()` rows via `diagnostic_capability_need_records(row)`;
2. recorded diagnostic facts scoped to `diagnostic_run:*` whose predicate is `diagnostic_capability_need`.

The ownership discrepancy implementation contains a conflict-to-capability mapping. For example, a service `owner_not_observed` conflict maps to listener/process/container-related evidence needs. That is where the underlying “missing observation capability” chain originates for current capability pressure.

Pressure then compresses these entries into:

- total subject occurrence score;
- capability need frequency;
- affected subjects;
- affected diagnostics;
- short reason naming missing observation capability and top need.

The qualitative operator chain is therefore implementation-backed but distributed:

```text
ownership discrepancy row
→ conflict class
→ diagnostic capability need record
→ capability need entry
→ capability pressure item
→ optional reasoning path / operational story consumer
```

### Ownership pressure chain

Ownership pressure starts with `build_ownership_discrepancies(state)`. The pressure audit filters rows with `row.conflict`, counts kinds and conflict classes, and emits dominant conflict evidence.

The row itself already contains `reason`, `evidence_count`, `conflict`, and evidence refs. Pressure does not preserve row-level reasoning in full; it compresses row reasoning into aggregate counts and one pressure-level reason.

### Consumer predicate pressure chain

Orphaned and fragile predicate pressures start with `build_consumer_audit(root)`. Consumer audit discovers observation predicates and diagnostics from inventories, then scans implementation source mentions through declared consumer path groups.

Pressure filters consumer audit items to observation predicates and compresses them into counts and predicate lists. The architectural boundary — no implementation consumer, or only one implementation consumer — is represented as `orphaned` / `consumer_count == 1` in the consumer audit item, then summarized by pressure.

### Diagnostic shape pressure chain

Diagnostic Shape pressure starts with `build_diagnostic_shape_audit()` and `summarize_diagnostic_shape_audit()`. Pressure compresses mismatches, warnings, and unknowns into a score and reason.

This category is independently built and does not share the capability/ownership/consumer chain.

## Recurring implementation ownership

### What recurs

A recurring construction pattern exists:

```text
upstream diagnostic evidence
→ pressure category filter/aggregation
→ score
→ evidence dict
→ reason sentence
→ recommended command
```

The owner of that pattern is `seed_runtime/pressure_audit.py`, specifically the category-specific `_..._pressure()` builder functions and `_PressureItemCandidate` handoff.

### What does not recur as a separate owner

No implementation-visible object currently owns:

```text
PressureItem evidence
→ qualitative pressure explanation chain
```

as a separated responsibility.

The recurring pressure builders own evidence, score, reason, and recommendation together. The broader explanatory surfaces (`reasoning_path_audit.py`, `operational_story.py`) compose explanation material across many surfaces, but neither is bounded to Pressure Explanation as an extracted owner.

## Comparison against presentation

Explanation is **both implementation and presentation**, with different boundaries:

- Implementation: `PressureItem.reason` is constructed in the pressure category builders, and `OperationalStory` / `ReasoningPathAudit` construct structured reason/evidence/consumer/story fields before rendering.
- Presentation: `format_pressure_audit()`, `format_operational_story()`, and `format_reasoning_path_audit()` render already-built structures into text.

The pressure reason sentence is implementation-visible because it appears in JSON as well as text output. The longer coherent architectural story is only partially implementation-visible and remains assembled by combining multiple surfaces.

## Counterexamples reviewed

### Counterexample: pressure explanation already separated from pressure evidence

Not supported.

`PressureItem` stores `evidence` and `reason` as separate fields, but the builders construct both in the same category functions. There is no separate pressure explanation builder that consumes pressure evidence after candidate construction.

### Counterexample: each pressure category builds explanations independently

Supported.

Each category-specific `_..._pressure()` function builds its own reason sentence and evidence dictionary. This is strong evidence against a single existing Pressure Explanation owner.

### Counterexample: no recurring explanation compression

Not supported.

There is recurring compression: all pressure categories compress upstream evidence into a score/evidence/reason/recommended-command candidate. `reasoning_path_audit.py` and `operational_story.py` also repeatedly compose structured explanation material from existing surfaces.

### Counterexample: a single recurring owner already constructs complete pressure explanations

Not supported.

`pressure_audit.py` constructs short reasons, not full explanation chains. `reasoning_path_audit.py` constructs derivation paths, but only when given a domain and subject; it is not the pressure audit’s per-item explanation owner. `operational_story.py` constructs a broad story focused on primary pressure, but it is not bounded to explaining every pressure item.

## Supported conclusions

1. **A recurring Pressure Explanation responsibility exists only in compressed form.**  
   The recurring responsibility is pressure candidate construction: upstream evidence is selected, scored, summarized, given a reason sentence, and assigned a recommended command.

2. **The implementation does not currently expose a separated Pressure Explanation owner.**  
   Evidence and explanation are colocated in category builders, while broader explanation composition lives in general story/path surfaces.

3. **Explanation chains are currently constructed in multiple places.**  
   Short pressure explanations are constructed in `pressure_audit.py`; derivation-style explanations are constructed in `reasoning_path_audit.py`; broad operational explanations are constructed in `operational_story.py`.

4. **The evidence feeding capability pressure is implementation-visible.**  
   Ownership discrepancy conflicts feed diagnostic capability need records, which feed capability needs, which feed pressure.

5. **The operator still manually composes the complete qualitative chain for a specific pressure report.**  
   The pieces are available, but the Pressure surface does not provide one coherent “why” chain per pressure item.

6. **Recovering a boundary could improve qualitative pressure visibility without changing quantitative behavior.**  
   Because scores already come from existing builders, a future extraction that only reuses existing evidence/reason material could preserve scores while making the qualitative chain visible. This is a characterization, not a recommendation to implement it here.

## Unsupported conclusions

The implementation evidence does **not** support claiming that:

- Pressure already has a complete separated explanation generator.
- Pressure explanation should be LLM-generated.
- Pressure needs new categories.
- Pressure should plan recovery automatically.
- Any architectural boundary should be promoted beyond what current diagnostics already expose.
- There is already exactly one bounded owner for complete Pressure Explanation.

## Confidence

**Medium-high.**

The pressure category builders, capability need derivation, reasoning path audit, and operational story implementation provide enough evidence to characterize the current compression. Confidence is not “high” for recovering exactly one owner because the implementation shows at least three nearby composition sites and no existing pressure-item-specific explanation boundary.

## Acceptance answer

Pressure currently tells the operator **where** pressure exists and provides short implementation-built reasons.

The implementation can partially explain **why** pressure exists through existing diagnostic and story/path surfaces, especially for Capability pressure:

```text
ownership discrepancy
→ diagnostic capability need
→ capability need
→ capability pressure
→ reasoning path / operational story
```

But the Pressure surface itself does not yet expose that as one coherent pressure explanation chain. The operator still manually composes the complete qualitative chain from multiple implementation surfaces.

There is recurring compressed responsibility in `pressure_audit.py` around pressure candidate construction. There is also recurring broader explanation composition in `reasoning_path_audit.py` and `operational_story.py`. The implementation evidence is sufficient to say a boundary is compressed, but **not** sufficient to say that exactly one already-separated bounded Pressure Explanation owner exists today.
