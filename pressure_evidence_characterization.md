# Pressure Evidence Characterization

## Executive answer

Repository evidence supports a bounded **Pressure Evidence** characterization, but not a recovered implementation ownership today.

The recurring implementation-backed answer is:

```text
Before Seed can classify architectural pressure,
Seed may use observable implementation facts:

- concrete owners/corridors carrying multiple visible responsibilities;
- explicit evidence streams, payloads, report shapes, diagnostic rows, counts, and measurements;
- compatibility handoffs and compatibility residue;
- completion-audit residuals and stop points;
- manually reconstructed producer -> artifact -> consumer chains;
- negative observations, unknowns, unsupported domains, and evidence gaps.
```

Pressure Evidence begins when a concrete subject and observable repository material exist. It stops before saying the material is architectural pressure, before assigning pressure status, before choosing a recovery, and before changing implementation.

The repository demonstrates many local evidence responsibilities and multiple pressure-adjacent surfaces, especially `pressure_audit` and State-Build Cache Debug evidence production. It does **not** yet demonstrate one recurring compressed implementation owner named or equivalent to `Pressure Evidence`. Current recurrence remains a methodology/reporting pattern plus local evidence carriers.

Recommendation:

```text
Insufficient implementation evidence for Pressure Evidence ownership recovery.
Pressure Evidence is implementation-backed as a characterization boundary only.
```

Repository authority wins.

## Implementation reviewed

Primary implementation and tests reviewed:

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- State-Build Cache Debug implementation evidence described by the slice family and completion audit.
- Classification implementation evidence summarized by `classification_responsibility_characterization.md`.

Primary reports and investigations reviewed:

- `architectural_pressure_methodology_characterization.md`
- `pressure_visibility_competency_frontier.md`
- `pressure_visibility_evidence_classification_boundary_investigation.md`
- `classification_responsibility_characterization.md`
- `docs/repository_pressure_inventory.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/pressure_source_observation.md`
- `docs/pressure_transformation_investigation.md`
- State-Build Cache Debug slices and completion audit.
- Recent completion audits, negative investigations, responsibility-recovery readiness reports, and frontier reports found through repository search.

Commands used:

```bash
rg --files -g 'AGENTS.md' -g '*.md' -g '*.py' | head -200
rg -n "architectural_pressure|pressure_visibility|classification_responsibility|repository_pressure|pressure_source|pressure_transformation|completion audit|negative" *.md seed_runtime tests | head -200
rg -n "repeated manual|manual reconstruction|ownership reassignment|mixed authority|compatibility|corridor|completion-audit|residue|targeting|payload|decomposition|Pressure Evidence|Pressure Classification|evidence" architectural_pressure_methodology_characterization.md pressure_visibility_competency_frontier.md pressure_visibility_evidence_classification_boundary_investigation.md classification_responsibility_characterization.md docs/repository_pressure_inventory.md docs/pressure_visibility_and_preservation_observation.md docs/pressure_source_observation.md docs/pressure_transformation_investigation.md *completion_audit.md *slice*.md | head -300
rg -n "def _state_build_cache_debug|class _StateBuildCacheDebug|PressureAudit|pressure" seed_runtime tests docs *.md | head -200
sed -n '1,220p' seed_runtime/pressure_audit.py
sed -n '1,220p' tests/test_pressure_audit.py
sed -n '1,220p' pressure_visibility_evidence_classification_boundary_investigation.md
sed -n '1,220p' classification_responsibility_characterization.md
sed -n '1,240p' state_build_cache_debug_family_completion_audit.md
```

## Recurring observations

### 1. Observed material is preserved before pressure conclusion

`PressureItem` contains `evidence`, `score`, `reason`, and `recommended_command` as separate fields. `build_pressure_audit()` explicitly ranks operational pressure without planning, recording, or mutating state. The strongest direct implementation observation is that observed rows/counts are carried separately from the reason that interprets them as pressure-bearing.

Implementation-backed examples:

- Diagnostic Shape evidence records mismatch, warning, and unknown counts before the reason says those visibility rows are inconsistent.
- Ownership Attribution evidence records service/storage ambiguities, conflict counts, and dominant conflict before the reason says unresolved ownership rows create pressure.
- Capability evidence records frequency, affected subjects, and affected diagnostics before the reason names missing observation capability.
- Orphaned/Fragile Predicate evidence records consumer-audit predicate facts before the reason names no-consumer or single-consumer pressure.

This is Pressure Evidence only up to the observed rows/counts. `score`, `reason`, category ranking, and recommended inspection are pressure-audit classification/presentation choices.

### 2. Evidence production is often local and responsibility-specific

The State-Build Cache Debug family is the clearest implementation-backed evidence-production chain. Its completion audit identifies explicit local artifacts for cache evidence, projection evidence, read-model evidence, timing evidence, evidence assembly, final evidence, report payload, compatibility report, and presentation.

This demonstrates an evidence responsibility pattern, but it is not generic Pressure Evidence. It is State-Build Cache Debug evidence production.

### 3. Manual reconstruction recurs before classification

Several investigations reconstruct producer -> artifact -> consumer chains from code, tests, and prior slices before assigning pressure status. The State-Build Cache Debug completion audit reconstructs the chain from `_state_build_cache_debug_evidence_from_args(...)` through stream artifacts, assembly, final evidence, report payload, compatibility report, and formatter. The pressure/classification boundary investigation reconstructs evidence bundles before identifying classification authority.

This manual reconstruction is implementation-backed as operator methodology. It is not yet implemented as a reusable repository surface.

### 4. Completion audits preserve residual evidence

Completion audits repeatedly preserve remaining pressure as evidence while refusing same-family continuation when the residue belongs elsewhere. State-Build Cache Debug classifies remaining concerns as compatibility/report pressure, presentation pressure, or broader orchestration pressure rather than evidence-production pressure. Read-Model Ownership and Projection Influence Lineage are repeatedly cited as examples where completion leaves adjacent cache, timing, invalidation, selection, or downstream pressure outside the completed family.

These residuals are Pressure Evidence inputs for future inquiries only after the audit identifies concrete owners and boundaries. They are not themselves authorization to implement recovery.

### 5. Negative observations are evidence

Unsupported domains, unknown targets, absent support, ambiguity, and insufficient evidence are repeatedly preserved rather than inferred through. The evidence/classification boundary investigation explicitly treats unknowns, unsupported domains, operator-pressure-only findings, and residuals as evidence that may limit a pressure claim. Classification characterization likewise says Classification begins after the subject and evidence already exist and stops before evidence production, authority, rendering, navigation, selection, reasoning, mutation, or ownership recovery.

Negative observations therefore belong to Pressure Evidence until the report says what they authorize or do not authorize.

## Implementation-backed evidence

The following candidate observations are implementation-backed:

| Candidate observation | Status | Evidence basis | Current owner |
| --- | --- | --- | --- |
| Diagnostic rows/counts that precede pressure reasoning | Supported | `PressureItem.evidence`; `_diagnostic_shape_pressure`, `_ownership_pressure`, `_capability_pressure`, `_orphaned_predicate_pressure`, `_fragile_predicate_pressure`; pressure-audit tests asserting evidence fields. | `seed_runtime/pressure_audit.py` local pressure audit builders. |
| Evidence/reason separation | Supported | `PressureItem` field split and tests asserting category, score, evidence, reason-visible rendering, and JSON evidence. | Pressure Audit output shape. |
| Read-only diagnostic boundary | Supported | `build_pressure_audit()` docstring and empty-state test proving no event-ledger writes. | Pressure Audit diagnostic surface. |
| Multiple evidence streams before report payload | Supported | State-Build Cache Debug slices and completion audit identify cache, projection, read-model, and timing evidence artifacts before assembly and report payload. | State-Build Cache Debug evidence-production family. |
| Compatibility handoff concentration | Supported | State-Build Cache Debug completion audit separates evidence artifact, report payload, compatibility report, and formatter; remaining report/formatter pressure is downstream. | State-Build Cache Debug report/presentation owners, not evidence production. |
| Completion-audit residue | Supported | Completion audits preserve remaining pressure and stop when it belongs to another family. | Completion-audit methodology; specific family audits. |
| Counterexamples / unsupported / unknown as evidence | Supported | Pressure boundary and classification reports preserve unsupported/unknown/insufficient evidence and assign stop authority to classification. | Investigation methodology and local diagnostic/audit surfaces. |
| Repeated recovery targeting | Partly supported | Slices repeatedly target one compressed implementation-local boundary and stop; responsibility-readiness reports describe this as criteria. | Human-scoped recovery methodology, not an automatic owner. |
| Hidden ownership transitions | Partly supported | Slices recover hidden handoffs such as evidence collection -> stream artifact -> assembly -> report payload. | Local slice families. |
| Repeated implementation-local payload introduction | Supported in slices | State-Build Cache Debug and Timing Visibility introduce implementation-local payload/evidence classes while preserving compatibility. | Local family owners. |
| Repeated compatibility-preserving decomposition | Supported | Multiple slices and completion audits explicitly preserve public behavior while separating local owners. | Slice methodology and local implementation owners. |

## Observations currently reconstructed manually

The following are not currently first-class Pressure Evidence implementation surfaces; they are reconstructed by the operator/report author:

1. **Cross-family pressure-evidence inventory.** The repository has `pressure_audit` and many local audits, but no implemented `PressureEvidence` inventory that lists all observable facts available for future pressure visibility.
2. **Manual producer -> artifact -> consumer chains across historical slices.** State-Build Cache Debug's chain is visible in its completion audit, but recovering the same shape across unrelated families still requires reading slice reports, code, and tests.
3. **Ownership reassignment history.** Reports describe where remaining pressure moved, but there is no executable history table assigning each residual to a new owner.
4. **Compatibility residue across families.** Completion audits preserve compatibility residue in prose; no general implementation surface lists compatibility residue as pressure evidence.
5. **Evidence that supports multiple future pressure inquiries.** Diagnostic rows, completion-audit residuals, and local evidence artifacts can support multiple inquiries, but this reuse is manual unless an existing audit consumes them directly.
6. **Distinguishing architectural intuition from implementation-backed evidence.** The repository enforces this through report discipline and negative conclusions, not through a generalized runtime checker.

## Candidate evidence evaluation

### Repeated manual reconstruction

Implementation-backed as investigation practice. It appears in completion audits and boundary investigations that reconstruct chains from implementation evidence before reaching a conclusion. It is not implemented as an automatic repository feature.

### Repeated ownership reassignment

Partly supported. Completion audits and recovery-readiness reports repeatedly state that remaining pressure belongs to another family. The reassignment is a classification/stop outcome, not Pressure Evidence itself. Pressure Evidence owns the observed remaining owner/corridor and residue; Classification owns the reassignment conclusion.

### Mixed authority

Supported as a pressure-relevant observation when concrete surfaces combine evidence, reason, recommendation, compatibility, presentation, or mutation boundaries. `PressureItem` packages evidence, score, reason, and recommendation together, but the fields remain separable. Diagnostic inventory/shape-audit rules also show authority is tracked separately from diagnostic content.

### Compatibility handoff concentration

Supported. State-Build Cache Debug demonstrates evidence artifact -> report payload -> compatibility report -> formatter handoffs. The evidence side stops before compatibility report/presentation pressure.

### Repeated implementation corridor crossings

Supported only when a concrete corridor is named. Examples include `_state_build_cache_debug_evidence_from_args(...)` crossing collection, stream production, assembly, and downstream reporting before slices separated the chain. Generic corridor-crossing claims remain unsupported without code/test/report references.

### Multiple independently recoverable responsibilities

Supported locally. State-Build Cache Debug recovered cache, projection, read-model, timing, assembly, evidence artifact, report payload, compatibility report, and presentation boundaries. Timing Visibility and Structure Observation show similar local separations. This supports evidence-rich recovery methodology, not a generic Pressure Evidence owner.

### Completion-audit residue

Supported. Residue is an important Pressure Evidence source when tied to concrete owner names, stop points, and counterexamples.

### Repeated recovery targeting

Supported as methodology. It is not enough by itself to prove a new ownership.

### Hidden ownership transitions

Supported when a slice exposes a previously hidden handoff. State-Build Cache Debug's stream and payload artifacts are examples.

### Repeated implementation-local payload introduction

Supported in recent slices. Payload/evidence dataclasses introduce local boundaries without changing public behavior. This is evidence of localized responsibility recovery, not proof that all such payloads belong to Pressure Evidence.

### Repeated compatibility-preserving decomposition

Strongly supported as recovery methodology. Pressure Evidence may observe that decomposition happened and that compatibility was preserved. Pressure Classification decides whether remaining pressure exists.

## Counterexamples

### Pressure classification without observable evidence

No strong implementation-backed example was found. The repository's pressure audit builds categories from existing diagnostic shape, ownership discrepancy, capability need, and consumer-audit surfaces. Methodology reports repeatedly insist on implementation evidence before pressure classification. Classification may occur without **newly generated** evidence, but it still classifies already-preserved evidence.

### Pressure evidence that never contributes to pressure visibility

Counterexamples exist. Many evidence surfaces are native to other families and may never become pressure evidence: structure observations, relationship facts, timing measurements, read-model evidence, and diagnostic rows can support local reports without being used by Pressure Visibility. They become Pressure Evidence only when a pressure inquiry uses them to answer what observable implementation facts exist.

### Pressure evidence that belongs to another family

Strong counterexamples exist. State-Build Cache Debug evidence streams belong to State-Build Cache Debug, not generic Pressure Evidence. Classification surfaces belong to Classification-local diagnostics. Selection Path preserves pressure candidates and non-selected candidates, but candidate ordering and selection factors belong to Selection Path. Reasoning Path keeps derivation evidence, consumers, story impact, and unknowns as reasoning-path material, not pressure evidence.

### Evidence and classification packaged together

`PressureItem` packages evidence, score, reason, and recommendation together. This weakens any ownership-recovery claim that the implementation already separates Pressure Evidence and Pressure Classification as independent code owners. It supports a field-level characterization boundary, not a recovered owner.

### Adjacent pressure alone

Completion audits repeatedly leave adjacent pressure. Adjacent pressure alone does not justify implementation or ownership recovery. It must first be supported by concrete implementation compression in the target family.

## Supported conclusions

1. **Pressure Evidence is observable material with provenance.** It includes implementation owners/corridors, evidence streams, diagnostic rows, counts, measurements, support gaps, unknowns, counterexamples, and completion-audit residue.
2. **Pressure Evidence begins after the subject and observable implementation material exist.** It does not begin from vocabulary, intuition, or desired competency shape.
3. **Pressure Evidence stops at an evidence bundle.** It does not decide that the evidence proves architectural pressure, insufficient evidence, adjacent pressure, frontier pressure, or recovery readiness.
4. **Classification begins after Pressure Evidence.** Classification assigns pressure status, authority limits, stop outcomes, and recommendation boundaries over existing evidence.
5. **Many evidence observations can support multiple future pressure inquiries.** Diagnostic rows, ownership conflicts, capability gaps, consumer-audit rows, completion-audit residuals, and compatibility residue can be reused, but current reuse is mostly local or manual.
6. **The repository already has implementation-backed evidence producers.** It does not yet have a recurring compressed implementation owner specifically responsible for Pressure Evidence across Pressure Visibility.
7. **The strongest current ownership evidence remains local.** State-Build Cache Debug evidence production is recovered as its own family; Pressure Audit is a local read-only diagnostic; Classification is local deterministic status assignment over existing evidence.

## Unsupported conclusions

The following conclusions are not supported by repository evidence:

- Pressure Evidence should be implemented now.
- Pressure Evidence should be a framework, score, schema, diagnostic, runtime behavior, or CLI surface.
- Pressure Evidence owns pressure classification, pressure scoring, recovery selection, automatic slicing, navigation, rendering, or authority.
- Any repeated pressure vocabulary proves repository knowledge.
- Completion-audit residue automatically becomes a frontier, next slice, or recovery target.
- Operator pain alone establishes implementation pressure or root cause.
- Local evidence classes in State-Build Cache Debug prove a generic Pressure Evidence owner.
- `PressureItem.evidence` proves evidence and classification are already independent implementation owners.

## Direct answers

### 1. What recurring implementation observations constitute Pressure Evidence?

Observable facts with provenance: diagnostic counts/rows, ownership conflicts, capability gaps, orphaned/fragile consumer rows, local evidence streams, implementation-local payloads, measurements, compatibility handoffs, producer/consumer chains, completion-audit residuals, unknowns, unsupported domains, and counterexamples.

### 2. Which observations are implementation-backed?

Strongly backed: pressure-audit evidence fields, pressure-audit read-only behavior, State-Build Cache Debug evidence stream chain, compatibility-preserving payload/report handoffs, and completion-audit residual/stop patterns. Partly backed: cross-family ownership reassignment history and repeated recovery targeting, because those are preserved in reports rather than implemented as a shared surface.

### 3. Which observations are currently reconstructed manually?

Cross-family pressure-evidence inventories, producer -> artifact -> consumer chains outside local completion audits, ownership reassignment history, compatibility residue across families, multi-inquiry reuse potential, and the distinction between implementation-backed observations and architectural intuition.

### 4. Where does Pressure Evidence begin?

Pressure Evidence begins when a bounded subject and observable implementation material already exist: code, tests, diagnostics, audit rows, measurements, report artifacts, compatibility constraints, completion-audit residuals, or explicit negative observations.

### 5. Where does Pressure Evidence stop?

Pressure Evidence stops at the preserved evidence bundle: what was observed, where it came from, what shape it has, and what is absent/unknown. It stops before pressure status, scoring meaning, authority limitation, recovery recommendation, ownership recovery, scheduling, runtime change, schema change, or behavior change.

### 6. Is there sufficient recurring implementation evidence to justify recovering a bounded Pressure Evidence ownership?

```text
Insufficient implementation evidence.
```

There is sufficient evidence to keep Pressure Evidence as a characterization boundary and a future investigation target. There is not sufficient evidence to recover a generic Pressure Evidence owner today because the implementation evidence remains distributed across local owners and methodology reports, and the central pressure surface still packages evidence with score/reason/recommendation.

## Confidence

Confidence: **medium-high** for the boundary characterization. The evidence/classification distinction is explicitly supported by the pressure boundary investigation, classification characterization, pressure-audit implementation, tests, and recent evidence-production slices.

Confidence: **medium** for the ownership-recovery recommendation. The pattern is recurring, but current proof is mostly distributed across local implementation families and human-authored completion audits. That is enough to reject ownership recovery now, but future slices could make a compressed Pressure Evidence owner visible.

## Recommendation

Do not recover Pressure Evidence ownership now.

Preserve this bounded characterization:

```text
Pressure Evidence observes and preserves implementation facts.
Pressure Classification decides what those facts authorize Seed to claim.
```

If future work returns to Pressure Visibility, it should first find a concrete compressed implementation owner where evidence gathering for pressure inquiries is repeated, local, compatibility-constrained, and separable from classification. Until then, Pressure Evidence remains methodology backed by implementation examples, not a recovered implementation responsibility.
