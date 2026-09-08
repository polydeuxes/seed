# Pressure Visibility Evidence / Classification Boundary Investigation

## Executive answer

Repository evidence supports a bounded distinction between **Pressure Evidence** and **Pressure Classification**, but not enough recurring implementation compression to justify a new ownership recovery.

The supported boundary is:

```text
Pressure Evidence
= observed, repository-visible material that answers "what did I observe?"

Pressure Classification
= cautious interpretation of that material that answers "what may Seed conclude?"
```

The current recovered Pressure Visibility methodology already separates those functions in reports, observations, and read-only diagnostics. Evidence is gathered as operator reports, measurements, implementation owners/corridors, diagnostic rows, support gaps, unknowns, residuals, and completion-audit findings. Classification then names whether the evidence supports apparent implementation pressure, insufficient evidence, adjacent pressure, residual pressure, frontier pressure, unsupported conclusion, or authority limit.

However, this distinction is presently a **methodology/reporting boundary**, not an implementation ownership boundary. The recurring implementation evidence shows read-only surfaces already carry evidence fields, reasons, limitations, authority boundaries, and stop states. It does not show a repeated compressed implementation owner where evidence gathering and pressure classification must be recovered as separate responsibilities now.

Therefore the recommendation is:

```text
Do not recover ownership.
Pressure Evidence != Pressure Classification is supported as a characterization boundary.
Insufficient implementation evidence for a separate ownership recovery.
```

Repository authority wins.

## Methodology reviewed

This investigation reviewed the prompt-listed methodology and nearby implementation-backed reports:

- `architectural_pressure_methodology_characterization.md`
- `pressure_visibility_competency_frontier.md`
- `recovery_to_frontier_promotion_characterization.md`
- `docs/repository_pressure_inventory.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/pressure_source_observation.md`
- `docs/operator_pressure_as_evidence_observation.md`
- `docs/architectural_recovery_methodology_characterization.md`
- family completion-audit patterns referenced by those documents
- negative investigations and stop/insufficient-evidence reports referenced by those documents
- current implementation surfaces around `pressure_audit`, diagnostic shape audit, and reference-selection unknown/unsupported handling

The reviewed methodology consistently begins from implementation or observation evidence, then separately restricts what can be concluded from it. That separation appears most clearly in the repeated pattern:

```text
implementation evidence first
↓
classification of pressure / authority / residual / insufficient evidence
↓
stop unless separate recovery authority exists
```

## Implementation evidence reviewed

### Pressure audit implementation

`seed_runtime/pressure_audit.py` is an implemented read-only diagnostic that aggregates existing surfaces. It defines `PressureItem` with both an `evidence` payload and a `reason`, then `build_pressure_audit()` ranks operational pressure without planning, recording, or mutating state. This is implementation evidence that observation material and interpretive reason are distinct fields inside an existing pressure surface.

The pressure audit also shows classification-like output is currently local and bounded: diagnostic shape pressure is emitted only when mismatches, warnings, or unknowns produce a positive score; ownership pressure is emitted only when ownership discrepancies have conflicts; capability pressure is emitted only when capability needs exist. Evidence can be counted and carried separately from the reason string that explains why the rows are pressure-bearing.

### Diagnostic inventory / shape-audit implementation

`seed_runtime/diagnostic_shape_audit.py` registers `pressure_audit` as a diagnostic implementation spec. The same file tracks record scope and mutation fields for diagnostic surfaces. That is implementation evidence that read-only diagnostic authority is already checked separately from the content of any diagnostic result.

This matters for the evidence/classification boundary because authority does not belong to raw pressure evidence. Authority is a separate boundary/shape property: a diagnostic can expose pressure-bearing evidence while still being non-mutating and not a recovery authorization.

### Reference-selection unsupported-domain implementation

`seed_runtime/reference_selection.py` returns an explicit `unknown` selected reference for unsupported domains, with rationale and limitations explaining the boundary. This is a concrete counterexample to classification by inference: when implementation evidence does not expose supported candidate alternatives for a domain, the result is unknown/unsupported rather than an invented conclusion.

### Methodology documents as implementation-adjacent evidence

The pressure methodology and frontier reports repeatedly cite completed slices, completion audits, tests, and diagnostic/read-only surfaces. They are not runtime code, but the repository treats them as implementation-backed methodology evidence when they derive claims from code, tests, and completed recovery families. This investigation treats them as equal evidence only where they preserve implementation or methodology authority, and not as independent architecture preference.

## Evidence responsibilities

Pressure Evidence answers:

```text
What did Seed observe?
```

The supported evidence responsibilities are:

1. **Preserve observed material without overclaiming.** Evidence may include overloaded owners/corridors, report/dataclass shapes, inventory aggregators, cache/build corridors, projection paths, event corridors, diagnostic rows, measurements, operator reports, support gaps, unknowns, residual completion-audit findings, and repeated manual reconstruction.
2. **Preserve source and scope.** Evidence must remain tied to the implementation owner, command, diagnostic, report, document, measurement, or observed situation that produced it.
3. **Preserve negative observations.** Unsupported domains, unknown targets, insufficient evidence, absence, ambiguity, and operator-pressure-only findings are still evidence about what the repository can and cannot support.
4. **Avoid conclusion authority.** Evidence can say what was observed; it does not by itself say the root cause, implementation direction, priority, ownership recovery, or architectural boundary.
5. **Support later classification.** Evidence must be rich enough that a later classification can explain why it is pressure-bearing, insufficient, adjacent, unsupported, residual, or frontier.

### What constitutes Pressure Evidence?

Pressure Evidence is repository-visible material that can support or limit a pressure claim. The strongest implementation-backed forms are:

- one owner or corridor carrying behaviorally real multiple responsibilities;
- hidden boundary, authority, compatibility, or stopping-point evidence;
- repeated manual reconstruction tied to a concrete owner or corridor;
- completion-audit residuals and counterexamples;
- operator pressure after localization through measurement or repository evidence;
- diagnostic rows, counts, mismatches, unknowns, capability needs, ownership conflicts, or consumer-audit rows;
- support gaps, missing observations, contradictions, staleness, activation failures, navigation failures, unknowns, and ambiguities when they matter to continuation, explanation, selection, or operator answering.

Pressure Evidence can exist without pressure classification. Examples include operator pain before instrumentation, preserved facts without current pressure, raw diagnostic row counts before reason/pressure explanation, unknown or ambiguous material before a supported conclusion, and completion-audit residuals before frontier classification.

## Classification responsibilities

Pressure Classification answers:

```text
Given that evidence, what may Seed legitimately conclude?
```

The supported classification responsibilities are:

1. **Apply the recovered pressure definition.** Classification determines whether evidence shows behaviorally real responsibility plurality compressed in one owner/corridor with insufficient independent boundary visibility.
2. **Name the supported pressure status.** Supported statuses include apparent implementation pressure, insufficient evidence, adjacent pressure, residual pressure, frontier pressure, historical pressure, orphaned pressure, unsupported conclusion, unknown, or authority limit.
3. **Distinguish pressure kinds.** Classification separates implementation pressure from operator pressure, inquiry pressure, frontier pressure, residual pressure, debug/timing pressure, presentation vocabulary, and ordinary incompleteness.
4. **Preserve authority limits.** Classification says what Seed cannot infer: root cause from operator pain alone, recovery from pressure alone, priority from impact alone, architecture from vocabulary, or implementation from frontier status.
5. **Own stop outcomes.** Classification owns `insufficient evidence`, `unsupported`, `unknown`, `already recovered`, `belongs to another family`, and `stop` as legitimate terminal conclusions.

### What constitutes Pressure Classification?

Pressure Classification is the interpretive act that maps pressure evidence to a bounded conclusion. It includes:

- deciding that evidence is **apparent implementation pressure**;
- deciding evidence is **operator-pressure-only** until localized;
- deciding that residual pressure is **adjacent** rather than same-family;
- deciding that lack of implementation authority is **insufficient evidence**;
- deciding unsupported identities should return **unknown** rather than be inferred;
- deciding a remaining recurring future need is a **frontier candidate** rather than an implementation-ready slice;
- deciding the report must **stop** before recovery, ranking, planning, or implementation.

Pressure Classification can exist without new evidence only when it reclassifies, audits, or interprets already-preserved evidence. Completion audits and recovery-to-frontier characterization do this: they classify remaining pressure after reviewing completed slices and existing residuals. That is not evidence-free classification; it is classification without newly generated evidence.

## Boundary between evidence and classification

The boundary occurs at the transition from:

```text
observed material and provenance
```

to:

```text
permitted conclusion and authority statement
```

In the current Pressure Visibility flow, the boundary is between the **evidence bundle** and **bounded classification**:

```text
Implementation owner/corridor
↓
Pressure observation
↓
Evidence bundle        ← Pressure Evidence ends here
↓
Pressure classification ← Pressure Classification begins here
↓
Authority boundary / human review / stop
```

A practical rule:

- If the statement answers **"what was seen, where, and with what support?"**, it belongs to Pressure Evidence.
- If the statement answers **"what does that allow Seed to claim, refuse, or stop on?"**, it belongs to Pressure Classification.

Examples:

| Statement | Responsibility |
| --- | --- |
| `seed --state-build` was slow on a cold path. | Evidence |
| Instrumentation measured replay/build and relationship-refresh costs. | Evidence |
| The implementation target localized to repeated relationship projection during fact-event replay. | Classification over evidence |
| Operator pain is pressure signal, not root-cause authority. | Classification / authority limit |
| `PressureItem.evidence` contains counts or row summaries. | Evidence |
| `PressureItem.reason` explains why those counts are pressure-bearing. | Classification |
| Unsupported reference-selection domain returns `unknown`. | Classification / stop |
| The unsupported-domain rationale and limitation are preserved. | Evidence for the classification boundary |

## Authority boundary

Authority changes when Seed moves from observed material to a permitted conclusion. Evidence does not carry implementation authority by itself. Classification owns the authority boundary because classification determines what the evidence authorizes and what it does not.

The authority boundary is supported by these repository patterns:

- Operator reports orient attention but do not authorize root cause or implementation direction.
- Pressure Visibility may classify apparent pressure but must stop before recovery, ranking, scheduling, or implementation.
- Recovery stops when no same-family implementation compression remains, when evidence is insufficient, or when pressure belongs to another family.
- Unsupported targets/domains return `unknown`, `unsupported`, `stop`, or `insufficient evidence` rather than inferred answers.
- Diagnostic surfaces preserve record scope and mutation boundaries separately from diagnostic content.

### Which responsibility owns authority limitation?

**Pressure Classification owns authority limitation.** Evidence can contain authority-relevant facts, such as record scope, mutation flags, source provenance, unknown status, unsupported domain, or diagnostic counts. But the act of saying "this evidence does not authorize recovery," "this is insufficient," or "this must stop" is classification.

### Which responsibility owns `insufficient evidence`?

**Pressure Classification owns `insufficient evidence`.** The evidence responsibility preserves what exists and what is missing. Classification determines that the missing or weak evidence is insufficient for the proposed claim.

### Which responsibility owns `apparent implementation pressure`?

**Pressure Classification owns `apparent implementation pressure`.** Evidence owns the observed owner/corridor, compressed responsibilities, hidden handoff, diagnostic rows, or measurements. Classification determines whether that evidence satisfies the recovered pressure definition strongly enough to call it apparent implementation pressure.

### Which responsibility owns the explicit stop condition?

**Pressure Classification owns the explicit stop condition.** The stop condition is a conclusion about authority: stop because evidence is insufficient, stop because the pressure is adjacent, stop because the current family is complete, stop because the target is unsupported, or stop because further work would require recovery/implementation authority.

## Counterexamples

### Evidence and classification appear intentionally adjacent

`seed_runtime/pressure_audit.py` keeps `PressureItem.evidence`, `score`, `reason`, and `recommended_command` in one output item. This could suggest evidence and classification are intentionally packaged together for operator use. However, the fields remain separable: evidence carries observed row summaries/counts, while reason and score interpret them. The counterexample weakens a claim for separate implementation owners, but not the characterization boundary.

### Classification without newly generated evidence

Completion audits and recovery-to-frontier characterization classify already-existing slice reports and residuals. They do not always create new measurements or runtime rows. This is classification without new evidence generation, but not classification without evidence. It depends on previously preserved implementation and methodology evidence.

### Evidence that intentionally refuses classification

Operator pressure before instrumentation is evidence that refuses root-cause classification. The operator report that the state-build path was slow was real pressure evidence, but repository methodology says it was not sufficient diagnosis. The classification remained withheld until instrumentation and repository evidence localized the implementation target.

Unsupported reference-selection domains also refuse classification into a selected concrete reference. The implementation returns `unknown`, a rationale, and limitations instead of inferring a candidate from unsupported evidence.

### Evidence and classification intentionally inseparable?

No strong repository evidence shows they are intentionally inseparable as responsibilities. Existing surfaces package evidence and reasons together for usability, but the methodology repeatedly distinguishes observation/evidence from supported claim/authority. The strongest conclusion is packaging adjacency, not inseparability.

### Classification without observable evidence?

No supported example was found. Repository methodology repeatedly rejects inference from vocabulary, operator pain alone, unsupported identities, broad frontiers, or missing abstractions. Apparent classification without evidence is treated as unsupported, unknown, or insufficient evidence.

## Supported conclusions

1. **Pressure Evidence is distinct from Pressure Classification as a methodology boundary.** Evidence answers what was observed; classification answers what Seed may conclude.
2. **Evidence can exist without pressure classification.** Operator pain, raw diagnostic rows, unknowns, missing support, and preserved residuals may be evidence before they are classified.
3. **Classification can occur without new evidence generation, but not without evidence.** Completion audits and characterization reports classify existing implementation evidence and residuals.
4. **Authority limitation belongs to classification.** Evidence preserves source/scope; classification states supported conclusions, non-authority, and stop conditions.
5. **`insufficient evidence` belongs to classification.** Missing or weak evidence is observed by evidence responsibility, but insufficiency is a conclusion.
6. **`apparent implementation pressure` belongs to classification.** The compressed owner/corridor and observed signals are evidence; apparent pressure is the permitted conclusion.
7. **The explicit stop condition belongs to classification.** Stop is an authority conclusion, not a raw observation.
8. **Current repository evidence supports characterization, not ownership recovery.** There is not enough recurring implementation compression showing evidence gathering and pressure classification must become separate code owners.

## Unsupported conclusions

The repository evidence does **not** support concluding that:

- Pressure Visibility should be implemented now;
- a new diagnostic, schema, runtime behavior, scoring system, ranking system, or workflow should be added;
- Pressure Evidence and Pressure Classification are separate implementation ownership families today;
- classification may proceed without observable evidence;
- operator pain authorizes root cause or implementation direction;
- residual pressure automatically becomes a frontier or next slice;
- presentation vocabulary proves repository knowledge;
- pressure evidence automatically authorizes Architectural Recovery.

## Answers to the recovery questions

### What constitutes Pressure Evidence?

Pressure Evidence is repository-visible observed material with provenance: implementation owners/corridors, compressed responsibilities, hidden handoffs, diagnostic rows, measurements, operator reports, support gaps, unknowns, residual audit findings, and counterexamples that can support or limit a pressure claim.

### What constitutes Pressure Classification?

Pressure Classification is the bounded interpretation of that evidence into a permitted conclusion: apparent implementation pressure, insufficient evidence, adjacent/residual/frontier pressure, unsupported, unknown, authority limit, or stop.

### Can evidence exist without pressure classification?

Yes. Operator pain before instrumentation, raw audit rows, observed unknowns, support gaps, preserved residuals, and absent evidence can exist before classification determines what they support.

### Can pressure classification exist without new evidence?

Yes, but only by classifying already-preserved evidence. Completion audits and methodology characterizations classify existing slice/report evidence without necessarily producing new runtime observations. Classification without any observable evidence is unsupported.

### Where does authority change?

Authority changes when Seed moves from evidence bundle to classification. Evidence can show what was observed; classification decides what can be claimed and where Seed must refuse, limit, or stop.

### Which responsibility owns `insufficient evidence`?

Pressure Classification owns it.

### Which responsibility owns `apparent implementation pressure`?

Pressure Classification owns it.

### Which responsibility owns the explicit stop condition?

Pressure Classification owns it.

## Confidence

Confidence is **high** that the methodology distinguishes observation/evidence from permitted conclusion/authority. Multiple documents and implemented surfaces preserve evidence, reason, limitations, unknown/unsupported status, and stop conditions separately.

Confidence is **medium-high** that Pressure Evidence and Pressure Classification are useful names for this characterization boundary. The behavior is repository-supported, although this exact naming is a characterization produced by this investigation.

Confidence is **low** that a separate ownership recovery is justified now. Current implementation packages evidence and reason together in read-only surfaces without showing recurring harmful compression that requires a new owner split.

## Recommendation on ownership recovery

Do **not** recover ownership now.

The repository demonstrates a recurring methodological boundary:

```text
Pressure Evidence != Pressure Classification
```

But it does not demonstrate a recurring compressed implementation responsibility requiring ownership recovery. The correct conclusion is:

```text
Supported as implementation characterization.
Insufficient implementation evidence for ownership recovery.
```

Repository authority wins.
