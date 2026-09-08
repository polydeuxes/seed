# Frontier Pressure Admission District Scout 002

## Read-only scout scope

This scout inspected nearby Frontier Pressure Admission implementation neighborhoods after Slice 058.

No implementation files were changed during the scout. No tests were changed during the scout. This report records the scout findings and next-command recommendation.

## Commands used

```bash
pwd && find .. -name AGENTS.md -print && git status --short && rg -n "Frontier Pressure|frontier pressure|pressure|admission|selection_path_audit|diagnostic-shape|diagnostic_shape|capability|orphaned|fragile" -S .
cat AGENTS.md && rg -n "frontier_pressure_admission_slice_0(5[3-8]|5[0-9]|3[0-9]|4[0-9])|Slice 058|Slice 057|pressure score|positive-finding refusal|pressure" frontier_pressure_admission_slice_*.md seed_runtime tests scripts/seed_local.py -S
sed -n '1,260p' seed_runtime/pressure_audit.py && sed -n '260,620p' seed_runtime/pressure_audit.py && sed -n '1,620p' tests/test_pressure_audit.py
python scripts/seed_local.py --pressure-audit --json
nl -ba seed_runtime/pressure_audit.py | sed -n '1,280p'
nl -ba tests/test_pressure_audit.py | sed -n '1,590p'
nl -ba scripts/seed_local.py | sed -n '1500,1535p;7360,7380p'
rg -n '"pressure_audit"|pressure_audit' seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py
nl -ba seed_runtime/diagnostic_inventory.py | sed -n '1138,1175p'
nl -ba seed_runtime/diagnostic_shape_audit.py | sed -n '618,636p'
nl -ba seed_runtime/pressure_audit.py | sed -n '270,360p'
rg -n "Recovered implementation-local ownership boundary|ownership pressure|Diagnostic Shape|admitted pressure|formatting|display evidence|consumer predicate" frontier_pressure_admission_slice_0*.md -S
```

## Current app evidence

Running the app with:

```bash
python scripts/seed_local.py --pressure-audit --json
```

succeeded and produced two current pressure categories:

1. `Orphaned Predicates`, score `26`.
2. `Fragile Predicates`, score `13`.

Current runtime pressure remains dominated by consumer-predicate findings, but the recently consumed queue already recovered the score and positive-finding refusal boundaries for those categories. Current app output alone therefore does not justify re-slicing orphaned/fragile score or refusal under new names.

The pressure-audit CLI surface is implementation-backed:

- `--pressure-audit` is registered as a CLI option in `scripts/seed_local.py`.
- The CLI branch builds the pressure audit, emits JSON when requested, otherwise emits human-readable output, and returns without recording or mutating through that branch.
- `pressure_audit` is registered in the diagnostic inventory as JSON-capable, non-recording, non-ledger-writing, and non-mutating.
- The diagnostic shape-audit spec covers the pressure-audit module, build/format/JSON functions, CLI flag, repo-file markers, and diagnostic-fact-read marker.

## Stop markers respected

### Slice 035

`selection_path_audit` neighborhood exhausted.

This scout did not propose new `selection_path_audit` work. The inspected current-code neighborhoods were in `seed_runtime/pressure_audit.py`, `scripts/seed_local.py`, diagnostic inventory, and diagnostic shape-audit registration.

### Slice 051

Immediate diagnostic-shape pressure candidate-construction pocket exhausted.

This scout did not propose extracting diagnostic-shape candidate fields, command literals, reason text, or metadata. The diagnostic-shape pressure source remains separated into summary, score, positive-finding refusal, evidence, and unchanged candidate construction.

## Recently consumed boundaries

The following boundaries were treated as already recovered and unavailable:

- capability pressure score production;
- capability pressure positive-finding refusal;
- orphaned-predicate pressure score production;
- orphaned-predicate positive-finding refusal;
- fragile-predicate pressure score production;
- fragile-predicate positive-finding refusal.

Current implementation confirms the helpers for capability, orphaned-predicate, and fragile-predicate score/refusal/evidence already exist. Those areas should not be re-sliced under new names.

## Inspected neighborhoods

### 1. Pressure-audit top-level source orchestration

`build_pressure_audit(...)` constructs the repository root, calls four pressure source producers, fans out consumer predicate pressures, and delegates candidate filtering/conversion/ordering to `_admitted_pressure_items(...)`.

Rank: **C. Already separated / likely re-slice**

The top-level orchestration is implementation-backed, but the visible responsibilities are already named at the source level:

- diagnostic shape pressure;
- ownership pressure;
- capability pressure;
- consumer predicate pressures;
- admitted pressure item production.

Slice 036 already recovered pressure candidate admission via `_admitted_pressure_items(...)`. Mining the outer builder now would likely re-slice orchestration rather than recover a new local ownership boundary.

Next move from this neighborhood: **stop locally; move to narrower source helpers.**

### 2. Ownership-pressure conflicted-row selection and non-positive refusal

`_ownership_pressure(state)` currently performs multiple local actions:

1. selects conflicted ownership discrepancy rows;
2. computes score through `_ownership_pressure_score(rows)`;
3. refuses non-positive score inline with `if score <= 0: return None`;
4. constructs the unchanged `Ownership Attribution` pressure candidate.

Score production and evidence aggregation are already separated:

- `_ownership_pressure_score(rows)` owns the score as `len(rows)`.
- `_ownership_pressure_evidence(rows)` owns service/storage ambiguity counts, conflict counts, and dominant conflict.

Rank: **A. Strong implementation-backed next slice** for ownership-pressure positive-finding refusal.

The strongest found boundary is **ownership-pressure positive-finding refusal**. The non-positive guard remains inline while the score helper is already separated. This mirrors already recovered positive-finding refusal patterns for diagnostic-shape, capability, orphaned-predicate, and fragile-predicate pressure, but it is distinct because it applies to ownership-discrepancy pressure rows and the `Ownership Attribution` candidate.

This candidate is distinct from prior slices:

- Slice 052 recovered ownership-discrepancy pressure score production, not non-positive refusal.
- Slice 039 recovered ownership pressure evidence payload aggregation, not refusal.
- Slices 053 through 058 recovered capability/orphaned/fragile score and refusal boundaries, not ownership refusal.

A helper such as `_ownership_pressure_has_findings(score)` would preserve:

- behavior: `score > 0` equivalent to current `score <= 0` refusal;
- schema: no JSON field changes;
- CLI: no flag changes;
- diagnostics: pressure-audit remains already registered;
- event ledger: no writes introduced;
- read-only boundary: unchanged read-only aggregation.

Next move from this neighborhood: **single slice or first item in a small batch.**

### 3. Ownership-pressure conflicted-row selection

`_ownership_pressure(state)` selects rows with `[row for row in build_ownership_discrepancies(state) if row.conflict]` before scoring and evidence production.

Rank: **B. Possible but needs caution**

There may be a still-compressed local responsibility: **ownership-pressure conflicted-row selection**.

The selected row set is consumed by:

- `_ownership_pressure_score(rows)`;
- `_ownership_pressure_evidence(rows)`;
- candidate reason/candidate construction.

This is implementation evidence, not only vocabulary. However, this candidate is weaker than ownership positive-finding refusal because it is very close to pressure-source audit-input filtering. It risks becoming a stylistic extraction unless framed narrowly as ownership pressure input-row selection and tested as behavior-preserving.

This candidate is distinct from prior slices:

- Not Slice 039: that recovered evidence aggregation from already-selected rows.
- Not Slice 052: that recovered score production from already-selected rows.
- Not Slices 053 through 058: those apply to capability/orphaned/fragile pressure.
- Not Slice 036: that recovered cross-candidate admission, not ownership row selection.

Next move from this neighborhood: **possible second slice in a batch; otherwise hold.**

### 4. Ownership-pressure candidate construction fields

After row selection, score, and refusal, `_ownership_pressure(state)` constructs the `_PressureItemCandidate` with:

- category `Ownership Attribution`;
- score;
- `_ownership_pressure_evidence(rows)`;
- reason text;
- recommended command `seed --ownership-discrepancies`.

Rank: **C. Already separated / likely re-slice**

The candidate construction itself is a direct implementation site, but Slice 051 already stopped the analogous immediate diagnostic-shape candidate-construction pocket because extracting candidate metadata or command literals would not recover a distinct producer/consumer boundary. The same caution applies here. Extracting ownership candidate field literals would likely be cosmetic or re-slice candidate construction, not ownership recovery.

Next move from this neighborhood: **reject for now.**

### 5. Consumer-predicate pressure item filtering

The consumer-predicate source fan-out is already separated into `_consumer_predicate_pressures(root)`, which builds one `ConsumerAudit` and returns orphaned and fragile candidate producers.

Inside the category producers:

- `_orphaned_predicate_pressure(audit)` filters audit items where `kind == "observation_predicate"` and `item.orphaned`.
- `_fragile_predicate_pressure(audit)` filters audit items where `kind == "observation_predicate"` and `consumer_count == 1`.

Score, evidence, and positive-finding refusal are already separated for both.

Rank: **B/C. Possible but high re-slice risk**

Category-specific item filtering is technically distinct from score/refusal, but it is immediately adjacent to the recently consumed orphaned/fragile predicate slices. Selecting it now would risk re-slicing by symmetry rather than implementation pressure.

Next move from this neighborhood: **reject for current batch; possible later outward move.**

## Candidate boundaries found

| Rank | Candidate | Evidence | Distinct from prior slices? | Safe recovery? | Scout decision |
| --- | --- | --- | --- | --- | --- |
| A | Ownership-pressure positive-finding refusal | Inline `if score <= 0: return None` after separated ownership score helper. | Yes. Slice 052 recovered score, Slice 039 recovered evidence, not refusal. | Yes, if helper preserves `score > 0` semantics. | Best next slice. |
| B | Ownership-pressure conflicted-row selection | Inline selection of `build_ownership_discrepancies(state)` rows with truthy `conflict`. | Yes, but adjacent to ownership source producer. | Yes, but caution against stylistic extraction. | Possible second slice in batch. |
| B/C | Consumer-predicate item filtering | Orphaned/fragile producers filter observation predicates inline. | Technically distinct from score/refusal, but very near recently consumed slices. | Behavior-preserving, but re-slice risk high. | Do not take next. |
| C | Pressure-audit top-level orchestration | `build_pressure_audit(...)` sequences existing sources and admission. | Mostly already separated by source helpers and Slice 036 admission. | Could preserve behavior, but likely re-slice. | Reject. |
| C/D | Ownership candidate construction fields | `_PressureItemCandidate(...)` literals and reason/command inside ownership producer. | Similar to stopped Slice 051 diagnostic-shape candidate pocket. | Could preserve behavior, but likely cosmetic. | Reject. |

## Rejected candidates and why

### Diagnostic-shape candidate construction

Rejected because Slice 051 explicitly stopped the immediate diagnostic-shape pressure candidate-construction pocket. The current diagnostic-shape candidate construction remains unchanged and should not be mined for field literals.

### Pressure-audit formatting

Rejected because Slices 043 through 046 already recovered mapping, collection, scalar display, and item-section formatting. Current display helpers are already separated.

### Consumer-predicate score/refusal/evidence rework

Rejected because Slices 055 through 058 consumed orphaned/fragile score and positive-finding refusal. Current helpers are already present and directly tested.

### Capability pressure score/refusal

Rejected because Slices 053 and 054 consumed these boundaries. Current helpers are already present and tested.

### Selection-path audit adjacency

Rejected because Slice 035 exhausted the neighborhood, and the scout did not find a compatibility-preserving call-site update that requires reopening it.

## Recommended next command

The next command should **perform a small batch of ownership-pressure slices**, starting with ownership-pressure positive-finding refusal.

Suggested scope:

```text
Recover implementation-local ownership boundaries in pressure_audit ownership-pressure neighborhood only:
1. ownership-pressure positive-finding refusal;
2. optionally, ownership-pressure conflicted-row selection if the first slice lands cleanly and direct tests prove unchanged behavior.

Do not touch selection_path_audit.
Do not touch diagnostic-shape candidate construction.
Do not re-slice capability, orphaned-predicate, or fragile-predicate score/refusal work.
Preserve CLI, JSON, diagnostics, event-ledger behavior, and read-only boundaries.
```

## Whether batching is safe

Batching is safe only in a small ownership-pressure batch.

Recommended batch size: **2 maximum**.

Safe batch:

1. **Ownership-pressure positive-finding refusal**: strong, implementation-backed.
2. **Ownership-pressure conflicted-row selection**: possible but should be included only if kept narrow and tested directly.

Do not include consumer-predicate filtering in this batch. It is too close to recently consumed orphaned/fragile predicate slices and raises re-slicing risk.

## Risk of re-slicing prior work

Overall risk: **moderate**.

- **Low risk** for ownership-pressure positive-finding refusal because score and evidence are already separated while refusal remains inline.
- **Moderate risk** for ownership conflicted-row selection because it is real but close to source-local filtering.
- **High risk** for consumer-predicate filtering because recent Slices 055 through 058 worked in that immediate neighborhood.
- **High risk** for any diagnostic-shape candidate field extraction because Slice 051 already stopped that pocket.
- **High risk** for formatting/display work because Slices 043 through 046 already recovered the visible formatting owners.

## Final scout decision

The next command should **perform a small batch of slices**, not produce a stop report and not move to a new adjacent neighborhood yet.

Recommended batch size: **1 to 2 slices**.

Best next slice: **ownership-pressure positive-finding refusal**.

Optional second slice: **ownership-pressure conflicted-row selection**, only if the next command explicitly permits a batch and preserves direct behavior with tests.
