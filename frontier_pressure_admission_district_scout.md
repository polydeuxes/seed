# Frontier Pressure Admission District Scout

## Scope and method

This is a read-only district scout of nearby Frontier Pressure Admission neighborhoods. No implementation files, tests, slice files, schemas, CLI surfaces, event-ledger behavior, diagnostics, or read-only boundaries were changed.

The scout started from the most recent Frontier Pressure Admission slice, Slice 052, then moved outward through adjacent implementation neighborhoods in `seed_runtime/pressure_audit.py`. The app was used in read-only mode with:

- `python scripts/seed_local.py --pressure-audit --json`
- `python scripts/seed_local.py --consumer-audit --json`
- `python scripts/seed_local.py --capability-needs --json`
- `python scripts/seed_local.py --ownership-discrepancies --json`

Current app evidence showed pressure only from consumer predicates: `Orphaned Predicates` scored 26 and `Fragile Predicates` scored 13. Capability needs and ownership discrepancies returned empty JSON arrays in this checkout.

## Stop markers respected

- Slice 035 stopped the immediate `selection_path_audit` neighborhood. This scout did not inspect or propose work in `seed_runtime/selection_path_audit.py`.
- Slice 051 stopped the immediate diagnostic-shape pressure candidate-construction pocket. This scout did not propose extracting diagnostic-shape category, reason, recommended-command, or candidate construction literals.
- Slice 052 recovered ownership-discrepancy pressure score production. This scout treats `_ownership_pressure_score(rows)` as prior work and does not recommend re-slicing it.

## Candidate rankings

### A. Strong implementation-backed next slice

#### Capability pressure score production

**Neighborhood inspected:** `_capability_pressure(state)` in `seed_runtime/pressure_audit.py`.

**Evidence summary:** The function builds capability-needs entries, computes `score = sum(len(entry.subjects) for entry in entries)`, uses that score for non-positive refusal, then reuses the same score in the candidate reason and candidate record. Adjacent prior work already separated capability evidence payload assembly into `_capability_pressure_evidence(entries)`, leaving score production still inline.

**Scout questions:**

1. **Still-compressed responsibility?** Yes. Capability pressure score production from existing capability-needs entries is compressed with entry collection, refusal, top-entry selection, reason text, command text, evidence helper consumption, and candidate construction.
2. **Implementation evidence?** Yes. The inline score is consumed by both the refusal guard and the public candidate reason/score.
3. **Distinct from prior slices?** Yes. Slice 040 recovered capability evidence payload assembly, not capability score production. Slice 052 recovered ownership score production, not capability score production.
4. **Outside stopped neighborhoods?** Yes. It is outside `selection_path_audit` and outside the stopped diagnostic-shape candidate-construction pocket.
5. **Would recovery require behavior, schema, CLI, JSON, diagnostic, event-ledger, or read-only-boundary changes?** No. A lawful slice would be a compatibility-preserving helper extraction plus focused test coverage, preserving the same score integer and output.
6. **Next move?** Slice.

**Rank:** A. Strong implementation-backed next slice.

### B. Possible but needs caution

#### Capability pressure positive-finding refusal

**Neighborhood inspected:** `_capability_pressure(state)` immediately after score production.

**Evidence summary:** The function refuses candidate construction when `score <= 0`. This resembles the recovered diagnostic-shape positive-finding refusal, but in the capability neighborhood the score production itself remains the nearer compressed responsibility. Recovering refusal first could skip over the stronger adjacent score boundary.

**Scout questions:**

1. **Still-compressed responsibility?** Yes, but it is less immediate than the score producer.
2. **Implementation evidence?** Yes. `if score <= 0: return None` directly controls candidate construction.
3. **Distinct from prior slices?** Mostly. Slice 050 recovered diagnostic-shape refusal, not capability refusal.
4. **Outside stopped neighborhoods?** Yes.
5. **Would recovery require behavior, schema, CLI, JSON, diagnostic, event-ledger, or read-only-boundary changes?** No if limited to a compatibility-preserving predicate helper and tests.
6. **Next move?** Move outward only after capability score production is recovered or explicitly stopped.

**Rank:** B. Possible but needs caution.

#### Orphaned predicate pressure score production / non-empty refusal

**Neighborhood inspected:** `_orphaned_predicate_pressure(audit)`.

**Evidence summary:** The function selects orphaned observation-predicate consumer-audit items, refuses empty selections, and constructs a pressure candidate with `score=len(items)`. The app currently reports 26 orphaned predicates, confirming this neighborhood is active in the current checkout. However, Slice 041 already recovered orphaned-predicate pressure evidence payload assembly, and this neighborhood is close to consumer-predicate pressure work from Slice 037.

**Scout questions:**

1. **Still-compressed responsibility?** Yes. Item selection, empty refusal, score derivation, reason text, command text, evidence helper consumption, and candidate construction remain together.
2. **Implementation evidence?** Yes. `items` are selected from `audit.items`; `if not items` refuses; `len(items)` becomes the public pressure score.
3. **Distinct from prior slices?** Potentially, if narrowed to score production or refusal. It must not re-slice Slice 037 consumer-predicate fan-out or Slice 041 evidence payload assembly.
4. **Outside stopped neighborhoods?** Yes.
5. **Would recovery require behavior, schema, CLI, JSON, diagnostic, event-ledger, or read-only-boundary changes?** No if limited to helper extraction with identical output.
6. **Next move?** Move outward after capability scoring/refusal is exhausted; not the immediate next slice.

**Rank:** B. Possible but needs caution.

#### Fragile predicate pressure score production / non-empty refusal

**Neighborhood inspected:** `_fragile_predicate_pressure(audit)`.

**Evidence summary:** The function selects single-consumer observation-predicate items, refuses empty selections, and constructs a pressure candidate with `score=len(items)`. The app currently reports 13 fragile predicates, confirming active current pressure. However, Slice 042 already recovered fragile-predicate evidence payload assembly, and this sits close to the same consumer-predicate fan-out recovered by Slice 037.

**Scout questions:**

1. **Still-compressed responsibility?** Yes. Item selection, empty refusal, score derivation, reason text, command text, evidence helper consumption, and candidate construction remain together.
2. **Implementation evidence?** Yes. `items` are selected from `audit.items`; `if not items` refuses; `len(items)` becomes the public pressure score.
3. **Distinct from prior slices?** Potentially, if narrowed to score production or refusal and not evidence/fan-out.
4. **Outside stopped neighborhoods?** Yes.
5. **Would recovery require behavior, schema, CLI, JSON, diagnostic, event-ledger, or read-only-boundary changes?** No if limited to helper extraction with identical output.
6. **Next move?** Move outward after capability scoring/refusal and orphaned-predicate adjacency are exhausted.

**Rank:** B. Possible but needs caution.

### C. Already separated / likely re-slice

#### Ownership pressure score production

**Neighborhood inspected:** `_ownership_pressure(state)` and `_ownership_pressure_score(rows)`.

**Evidence summary:** Slice 052 already recovered ownership-discrepancy pressure score production from selected conflicted ownership rows. The current code consumes `_ownership_pressure_score(rows)` and tests exercise the helper. Further work on the same score would be a re-slice.

**Scout questions:**

1. **Still-compressed responsibility?** Not for score production. Other ownership candidate fields remain, but immediate scoring is already separated.
2. **Implementation evidence?** Yes, but it supports prior completed work rather than a new slice.
3. **Distinct from prior slices?** No for score production.
4. **Outside stopped neighborhoods?** Yes.
5. **Would recovery require behavior, schema, CLI, JSON, diagnostic, event-ledger, or read-only-boundary changes?** A score rework should not be attempted; it risks churn.
6. **Next move?** Move outward.

**Rank:** C. Already separated / likely re-slice.

#### Diagnostic-shape pressure candidate construction

**Neighborhood inspected:** `_diagnostic_shape_pressure(root)` only as a stop-marker boundary, not as a new candidate.

**Evidence summary:** Slice 051 already stopped this immediate pocket. Extracting the remaining category/reason/recommended-command fields would be naming or presentation-field movement rather than a distinct implementation-local ownership boundary.

**Scout questions:**

1. **Still-compressed responsibility?** Only unchanged candidate construction fields remain.
2. **Implementation evidence?** Evidence exists for construction, but not for a narrower lawful producer/consumer boundary.
3. **Distinct from prior slices?** No. This is the stopped Slice 051 pocket.
4. **Outside stopped neighborhoods?** No.
5. **Would recovery require behavior, schema, CLI, JSON, diagnostic, event-ledger, or read-only-boundary changes?** It should not be recovered; even compatibility-preserving extraction would violate the stop marker absent stronger repository evidence.
6. **Next move?** Stop for this pocket; move outward.

**Rank:** E. Stop.

## Candidate boundaries found

1. **Recommended:** capability pressure score production from existing capability-needs entries.
2. **Secondary after recommended target:** capability pressure positive-finding refusal.
3. **Later possible:** orphaned-predicate score production or refusal, with care not to re-slice consumer-predicate fan-out or evidence payload.
4. **Later possible:** fragile-predicate score production or refusal, with the same caution.

## Rejected candidates and why

- **Diagnostic-shape candidate fields:** rejected because Slice 051 explicitly stopped the immediate diagnostic-shape candidate-construction pocket.
- **Ownership score:** rejected because Slice 052 already recovered this exact boundary.
- **Generic pressure candidate metadata extraction:** rejected as cosmetic unless a specific producer/consumer boundary is directly evidenced by implementation use.
- **Pressure audit route orchestration:** rejected as too broad; the existing candidate list in `build_pressure_audit(...)` does not itself show a smaller lawful ownership boundary that should precede the capability score target.
- **Selection-path work:** rejected because Slice 035 stopped the immediate `selection_path_audit` neighborhood and no compatibility-preserving call-site requirement was found.

## Recommended next slice target

The next lawful implementation slice should begin at **capability pressure score production inside `_capability_pressure(state)`**.

The narrow target would be a compatibility-preserving helper that owns only the integer score currently computed as `sum(len(entry.subjects) for entry in entries)`, consumed by `_capability_pressure(state)` exactly as before. The likely focused test would prove that the helper returns the same subject-occurrence count for representative `CapabilityNeedEntry` rows and zero for an empty list.

This target is the strongest because it is adjacent to the most recent outward movement from ownership scoring, directly mirrors the now-separated ownership score boundary without re-slicing it, and remains distinct from prior capability evidence work.

## Risk of re-slicing prior work

- **Low** if the next slice is limited to capability score production.
- **Medium** if it touches capability evidence payload fields, because Slice 040 already recovered `_capability_pressure_evidence(entries)`.
- **Medium** if it moves into orphaned/fragile predicates before capability scoring is exhausted, because Slices 037, 041, and 042 already recovered nearby consumer-predicate fan-out and evidence boundaries.
- **High** if it returns to diagnostic-shape candidate construction or selection-path audit, because those are stopped neighborhoods.

## Whether the next command should slice or stop

The next command should **slice**, not stop, if it targets capability pressure score production and preserves all public behavior.

A stop would be appropriate only if the next investigation refuses to touch capability scoring and instead remains in the stopped diagnostic-shape pocket, reopens selection-path audit, or cannot keep the slice distinct from previously recovered evidence and scoring helpers.
