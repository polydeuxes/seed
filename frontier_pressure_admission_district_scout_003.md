# Frontier Pressure Admission District Scout 003

## Read-only scout scope

This scout inspected nearby Frontier Pressure Admission implementation neighborhoods after Slice 060. It is read-only with respect to implementation and tests.

No implementation files were changed. No test files were changed. No slice report was created. This file is the only intended repository change.

## Commands used

```bash
pwd && rg --files -g 'AGENTS.md' -g '!.*' .. /workspace 2>/dev/null | head -50 && git status --short
cat AGENTS.md && git status --short && rg -n "ownership_pressure|selection_path_audit|diagnostic-shape|diagnostic_shape|pressure|Frontier|admission|conflicted_rows|has_findings" . -g '!*.pyc'
rg --files seed_runtime tests | rg 'pressure|diagnostic|selection|ownership|capability|predicate|ops'
sed -n '1,260p' seed_runtime/pressure_audit.py && sed -n '1,260p' tests/test_pressure_audit.py
sed -n '260,620p' seed_runtime/pressure_audit.py && sed -n '260,620p' tests/test_pressure_audit.py
sed -n '1,220p' frontier_pressure_admission_district_scout_002.md 2>/dev/null || true
python scripts/seed_local.py --pressure-audit --json | python -m json.tool | head -120
python scripts/seed_local.py --diagnostic-shape-audit --json | python -m json.tool | head -80
sed -n '1,180p' frontier_pressure_admission_slice_059.md; sed -n '1,180p' frontier_pressure_admission_slice_060.md
nl -ba seed_runtime/pressure_audit.py | sed -n '1,360p'
nl -ba tests/test_pressure_audit.py | sed -n '1,420p'
rg -n "diagnostic_shape_audit_root|consumer-predicate|orphaned-predicate|fragile-predicate|audit root|summary" frontier_pressure_admission_slice_0*.md
```

## Current app evidence

Running the current app command:

```bash
python scripts/seed_local.py --pressure-audit --json
```

succeeded. The current audit output contains two pressure categories:

1. `Orphaned Predicates`, score `26`, recommended command `seed --consumer-audit`.
2. `Fragile Predicates`, score `13`, recommended command `seed --consumer-audit`.

The app output does not currently show diagnostic-shape, ownership-attribution, or capability pressure. That matters because the live pressure signal still points at consumer-audit-derived predicate pressure, while the most recent implementation campaign consumed several nearby predicate-pressure score/refusal boundaries already.

The diagnostic shape audit command also ran successfully in JSON mode, and the visible initial rows were consistent. This scout did not use that as a reason to reopen diagnostic-shape candidate construction, because Slice 051 explicitly stopped the immediate diagnostic-shape pressure candidate-construction pocket.

## Stop markers respected

### Slice 035

`selection_path_audit` neighborhood exhausted.

This scout did not inspect `seed_runtime/selection_path_audit.py` as a next-slice target and does not propose new selection-path work. Any future selection-path change should be only a compatibility-preserving call-site update with direct implementation evidence.

### Slice 051

Immediate diagnostic-shape pressure candidate-construction pocket exhausted.

This scout did not propose extracting diagnostic-shape candidate literals, reason text, command text, or candidate-field assembly. Prior slices already separated diagnostic-shape audit root selection, summary production, score production, positive-finding refusal, and evidence projection; candidate construction remains stopped.

## Recently consumed boundaries

The following boundaries were treated as consumed and unavailable:

- capability pressure score production;
- capability pressure positive-finding refusal;
- orphaned-predicate pressure score production;
- orphaned-predicate positive-finding refusal;
- fragile-predicate pressure score production;
- fragile-predicate positive-finding refusal;
- ownership-pressure positive-finding refusal;
- ownership-discrepancy conflicted-row selection.

The current implementation confirms helpers now exist for the recently consumed ownership boundaries: `_ownership_pressure_conflicted_rows(state)` and `_ownership_pressure_has_findings(score)` are imported and tested in `tests/test_pressure_audit.py`, and `_ownership_pressure(state)` consumes those helpers before unchanged candidate construction.

## Inspected neighborhoods

### 1. Ownership-pressure candidate construction remainder

Rank: **C. Already separated / likely re-slice**

After Slice 060, `_ownership_pressure(state)` consumes `_ownership_pressure_conflicted_rows(state)`, `_ownership_pressure_score(rows)`, `_ownership_pressure_has_findings(score)`, and `_ownership_pressure_evidence(rows)`. The remaining inline material is the `_PressureItemCandidate` shell: category `Ownership Attribution`, reason text, recommended inspection command, and passing through the already-produced score/evidence.

This is implementation evidence, but it is not a strong next boundary. The prior nearby slices already separated the row source, score, refusal predicate, and evidence payload. Extracting category/reason/command assembly now would look like candidate-field movement, not a distinct producer/consumer responsibility. It also resembles the stopped diagnostic-shape candidate-construction pocket from Slice 051.

Decision: do not slice next.

### 2. Capability-pressure candidate construction remainder

Rank: **C. Already separated / likely re-slice**

`_capability_pressure(state)` already delegates score production to `_capability_pressure_score(entries)`, non-positive refusal to `_capability_pressure_has_findings(score)`, and evidence payload production to `_capability_pressure_evidence(entries)`. The remaining inline responsibilities are fetching capability needs, selecting `top = entries[0]` after the finding check, and assembling the candidate reason/command shell.

The top-need expression is directly present, but it is only used to interpolate the reason string after candidate admission. It does not currently feed a separate downstream consumer beyond reason text. Because the score/refusal/evidence boundaries are already consumed and because candidate text extraction is high-risk cosmetic movement, this neighborhood should not be the immediate next slice.

Decision: do not slice next.

### 3. Consumer-predicate item filtering in orphaned and fragile producers

Rank: **B. Possible but needs caution**

`_orphaned_predicate_pressure(audit)` still filters `audit.items` inline for rows where `item.kind == "observation_predicate" and item.orphaned`. `_fragile_predicate_pressure(audit)` still filters `audit.items` inline for rows where `item.kind == "observation_predicate" and item.consumer_count == 1`.

This is a real implementation-local responsibility: each filtered item set is consumed by the category's positive-finding refusal, score producer, evidence producer, and candidate construction. It is distinct from the recently consumed score/refusal boundaries because item filtering is upstream of those helpers. It is also distinct from Slice 037's consumer-predicate source admission because Slice 037 owns building one `ConsumerAudit` and fanning it out, not category-specific row selection inside each producer.

However, this area is adjacent to the recently consumed orphaned/fragile predicate score and refusal slices, and the app's current pressure output is dominated by these same categories. The risk is re-slicing by symmetry if the next command merely repeats the same pattern without proving the upstream row-selection handoff. If selected, it should be a deliberately narrow single slice or a two-slice batch only for the two category-specific filters.

Decision: viable but cautious.

### 4. Consumer-predicate candidate construction fields

Rank: **C/D. Already separated / cosmetic only**

After filtering, refusal, scoring, and evidence helpers, the orphaned and fragile producers still assemble category labels, reason strings, and `seed --consumer-audit` recommended commands inline.

Although these fields affect public output, they are candidate construction rather than a separated producer/consumer boundary. Extracting them would likely be cosmetic and would risk changing schema/CLI presentation without meaningful ownership recovery. It is weaker than item filtering because reason/command literals have no independent downstream consumer.

Decision: reject.

### 5. Pressure-audit top-level orchestration and admission

Rank: **C. Already separated / likely re-slice**

`build_pressure_audit(...)` still constructs the repository root and passes diagnostic-shape, ownership, capability, and consumer-predicate candidate slots to `_admitted_pressure_items(...)`. `_admitted_pressure_items(...)` already owns absent/non-positive candidate filtering, candidate conversion, and score/category ordering.

This top-level source orchestration is implementation-backed, but the producer responsibilities have already been separated at the source level. Reworking it now would likely re-slice Slice 036 admission or Slice 037 consumer-predicate source fan-out rather than recover new local ownership.

Decision: reject.

## Candidate boundaries found

| Rank | Candidate | Implementation evidence | Distinct from prior recovered slices? | Safe behavior-preserving recovery? | Scout decision |
| --- | --- | --- | --- | --- | --- |
| B | Orphaned-predicate item-set selection | Inline filter over `audit.items` for observation predicates with `item.orphaned`, then consumed by refusal, score, evidence, and candidate construction. | Yes: not score, not positive-finding refusal, not evidence payload, not single-audit fan-out. | Likely yes if helper preserves exact predicate and order. | Possible next single slice or first half of cautious two-slice batch. |
| B | Fragile-predicate item-set selection | Inline filter over `audit.items` for observation predicates with `consumer_count == 1`, then consumed by refusal, score, evidence, and candidate construction. | Yes: not score, not positive-finding refusal, not evidence payload, not single-audit fan-out. | Likely yes if helper preserves exact predicate and order. | Possible paired slice only if batching is accepted. |
| C | Ownership candidate shell | `_ownership_pressure(state)` still assembles category/reason/command after separated row, score, refusal, and evidence helpers. | Mostly distinct but too close to candidate-field extraction. | Technically yes, but likely cosmetic. | Do not take. |
| C | Capability top-need/reason shell | `_capability_pressure(state)` selects `top = entries[0]` only for reason text after score/refusal. | Distinct from score/refusal/evidence but weak. | Technically yes, but likely cosmetic. | Do not take. |
| C/D | Consumer-predicate reason/command/category fields | Orphaned/fragile candidate literals remain inline. | Distinct from score/refusal but not a strong ownership boundary. | Could preserve behavior, but unnecessary risk. | Reject. |
| C | Pressure-audit builder orchestration | `build_pressure_audit(...)` sequences source producers and admission. | Mostly already recovered by source/admission slices. | Would preserve behavior, but likely re-slice. | Reject. |

## Rejected candidates and why

### Ownership-pressure score/refusal/row selection

Rejected as unavailable. Slices 052, 059, and 060 already recovered ownership score production, positive-finding refusal, and conflicted-row selection. Reopening these under new names would re-slice prior work.

### Capability score/refusal/evidence

Rejected as unavailable. Capability score and refusal were recently consumed, and capability evidence was already separated earlier. The remaining top-need use is only reason-text construction, so it lacks a strong independent consumer.

### Diagnostic-shape pressure construction

Rejected because Slice 051 stopped the immediate diagnostic-shape candidate-construction pocket. Diagnostic-shape audit-root, summary, score, positive-finding refusal, and evidence boundaries are already separated.

### Selection-path audit

Rejected because Slice 035 stopped the neighborhood, and this scout found no compatibility-preserving call-site update that would require reopening it.

### Formatting and display

Rejected because pressure-audit display responsibilities are already separated into item-section, mapping, collection, and scalar display helpers. Further movement would be presentation cleanup rather than Frontier Pressure Admission recovery.

## Recommended next command

Recommended next move: **perform a cautious single slice** for **orphaned-predicate item-set selection inside `_orphaned_predicate_pressure(audit)`**, or move outward if the operator wants to avoid the consumer-predicate neighborhood because of high re-slice risk.

A safe single-slice command should recover only the existing orphaned item filter into a helper such as `_orphaned_predicate_pressure_items(audit)` and prove that it preserves:

- the exact `item.kind == "observation_predicate" and item.orphaned` predicate;
- item order;
- public JSON shape;
- human-readable output;
- CLI behavior;
- diagnostic inventory and shape-audit status;
- event-ledger read-only behavior;
- absence of cluster mutation.

The command should explicitly avoid score, positive-finding refusal, evidence payload, reason text, command literals, and candidate construction.

## Whether batching is safe

Batching is **possible but not strongly recommended**.

A two-slice batch could be safe only if it is strictly limited to the two parallel category-specific item-set selection boundaries:

1. orphaned-predicate item-set selection;
2. fragile-predicate item-set selection.

These two filters have separate predicates and separate downstream candidate producers, so they can be recovered independently without changing output. But the re-slice risk is higher than in Scout 002 because the campaign just consumed the orphaned/fragile score and refusal queue, and current app output still highlights those categories.

Recommended batch size if batching is accepted: **2**.

Recommended safer default: **1**.

## Risk of re-slicing prior work

Risk is **medium to high** if the next command stays in `seed_runtime/pressure_audit.py` without a very narrow target.

High-risk re-slice areas:

- ownership row selection/refusal/score/evidence, because Slices 039, 052, 059, and 060 already separated them;
- orphaned/fragile score and positive-finding refusal, because Slices 055 through 058 consumed them;
- diagnostic-shape candidate construction, because Slice 051 stopped it;
- selection-path audit, because Slice 035 stopped it;
- top-level pressure admission/order, because earlier slices already separated candidate admission and source fan-out.

The only nearby candidate that still looks implementation-backed is upstream item-set selection in the consumer-predicate producers. Even there, the next command should name the exact input and output boundary rather than the pressure category generally.

## Final scout statement

No implementation files were changed. No test files were changed. No slice report was created. This scout report is the only repository file intentionally added.
