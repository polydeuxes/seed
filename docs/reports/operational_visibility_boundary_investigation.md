# Operational Visibility Boundary Investigation

## Scope

This is an investigation-only report. It does not recover implementation, introduce slices, propose a framework, alter runtime behavior, or authorize a neighboring construction campaign.

The bounded question is:

```text
Does Operational Visibility presently contain
one recurring implementation-local ownership
boundary that remains compressed?
```

## Answer

No. Current implementation evidence does **not** expose exactly one recurring implementation-local Operational Visibility ownership boundary worthy of future recovery.

The bridge from External Orientation into Operational Visibility is real and implementation-backed, but it reveals **multiple possible local footings**, not exactly one lawful footing. The strongest recurring pressure is the adjacency between implementation-discovered operational surfaces, surface classification, diagnostic registration, shape-audit checking, and coverage presentation. However, that pressure is not singular: it appears as several adjacent ownership candidates that would need a separate authorization decision before any recovery.

## Bridge characterization

### What responsibilities now belong to External Orientation?

External Orientation now owns the narrow edge where externally supplied or externally declared material is admitted into a bounded implementation owner. Its completed family includes:

- exact external QuestionFamily text admitted into bounded-work eligibility;
- CLI/parser surface material prepared for operational surface classification;
- diagnostic declarations prepared for diagnostic inventory composition;
- source-navigation and inquiry-orientation intake boundaries already recovered by the prior campaign.

The implementation shows this ending point directly. `_QuestionFamilyEligibilityInput` is explicitly limited to carrying exact QuestionFamily text after inventory admission and explicitly does not own dispatch selection, presentation, rendering, surface arguments, or public result shape. `_prepare_question_family_eligibility_input(...)` validates exact inventory membership and returns only that narrow handoff. `【F:seed_runtime/question_surface_inventory.py†L66-L95】`

The operational-surface side has the same External Orientation end: `_CliSurfaceClassificationInput` prepares parser-derived material consumed by classification, and `build_operational_surface_classification_audit(...)` consumes that prepared material before emitting the established audit shape. `【F:seed_runtime/operational_surface_inventory.py†L119-L130】` `【F:seed_runtime/operational_surface_inventory.py†L195-L216】`

Diagnostic inventory composition also sits at the recovered end of External Orientation: `_DiagnosticInventoryCompositionInput` is only prepared diagnostic declarations for inventory composition, while the later formatting and JSON composition are diagnostic visibility outputs. `【F:seed_runtime/diagnostic_inventory.py†L35-L41】` `【F:seed_runtime/diagnostic_inventory.py†L1090-L1100】`

### What responsibilities first belong to Operational Visibility?

Operational Visibility first becomes observable when the implementation asks visibility questions about operational surfaces rather than merely admitting external material. The first visible responsibilities are:

1. discovering operational CLI surfaces from `argparse` declarations;
2. classifying discovered CLI elements as primary surfaces, filters, modifiers, debug, manual input, legacy, or unknown;
3. comparing discovered surfaces to diagnostic inventory registration;
4. rendering that coverage status as an operational visibility output.

`build_operational_surface_inventory(...)` discovers operational surfaces from public long options, skips auxiliaries, categorizes by operational keywords, and records whether each surface is registered and JSON-capable. `【F:seed_runtime/operational_surface_inventory.py†L169-L192】`

`VisibilityCoverageAudit` owns coverage counts and unregistered-surface views over surfaces plus classifications, and `build_visibility_coverage_audit(...)` composes discovery and classification outputs into one coverage audit. `【F:seed_runtime/operational_surface_inventory.py†L132-L166】` `【F:seed_runtime/operational_surface_inventory.py†L219-L231】`

The CLI makes these Operational Visibility surfaces observable as distinct app flags: `--operational-surface-inventory`, `--visibility-coverage-audit`, and `--operational-surface-classification-audit`. `【F:scripts/seed_local.py†L1402-L1416】`

### Where is the constitutional footing between them?

The constitutional footing is the handoff from prepared external/parser material into implementation-local visibility judgments.

External Orientation ends at the prepared handoff artifact. Operational Visibility begins when implementation evidence is discovered, classified, registered/unregistered, shape-checked, or presented as coverage. The footing is therefore:

```text
External Orientation:
  prepare/admit external or declared material

Operational Visibility:
  decide what operational surfaces are visible,
  how they are classified,
  whether they are registered,
  whether their declared shape matches implementation,
  and how coverage is presented
```

This footing is lawful because the implementation keeps the admission helpers narrow and because the visibility outputs are separately registered as diagnostic/operational surfaces. The diagnostic inventory registry declares operational surface inventory, visibility coverage audit, and operational surface classification audit as read-only surfaces with JSON support and no record, ledger, or cluster mutation behavior. `【F:seed_runtime/diagnostic_inventory.py†L232-L260】` `【F:seed_runtime/diagnostic_inventory.py†L262-L276】`

## Implementation evidence

### Operational surface discovery and coverage

Operational surface discovery is already implementation-backed: the inventory scans `argparse` public long options, filters auxiliary flags, maps operational keywords to categories, and records registration/JSON visibility from diagnostic entries. `【F:seed_runtime/operational_surface_inventory.py†L15-L37】` `【F:seed_runtime/operational_surface_inventory.py†L169-L192】`

Coverage presentation is also implementation-backed: `format_visibility_coverage_audit(...)` renders discovered, registered, and unregistered counts, then reports each missing registration as invisible to diagnostic inventory. `【F:seed_runtime/operational_surface_inventory.py†L311-L357】`

Running the app exposed the current shape of that pressure: `python scripts/seed_local.py --visibility-coverage-audit` reported 99 discovered surfaces, 49 registered surfaces, and 50 unregistered surfaces, split across primary, debug, filter, modifier, manual-input, and legacy classes. This supports dense Operational Visibility pressure, but it does not isolate exactly one ownership boundary.

### Diagnostic registry and shape audit

Diagnostic inventory owns declared diagnostic/test-like operational surface shape: flags, projected-state use, repo-file use, JSON support, record support, record scope, diagnostic/cluster fact emission, event-ledger writes, cluster mutation, diagnostic-fact reads, and descriptions. `【F:seed_runtime/diagnostic_inventory.py†L11-L32】`

Diagnostic shape audit owns static checking of declared fields against implementation evidence. Its audited fields include record support, JSON support, record scope, fact emission, event-ledger writes, diagnostic-fact reads, repo-file use, projected-state use, and cluster mutation. `【F:seed_runtime/diagnostic_shape_audit.py†L21-L31】`

The shape-audit specs separately register the operational visibility surfaces as implementation specs for operational surface inventory, visibility coverage audit, and operational surface classification audit. `【F:seed_runtime/diagnostic_shape_audit.py†L280-L297】`

`build_diagnostic_shape_audit(...)` then reads `scripts/seed_local.py`, observes each diagnostic implementation against its spec, and produces row-level consistency/mismatch/unknown status for every audited field. `【F:seed_runtime/diagnostic_shape_audit.py†L711-L737】`

### Question and bounded-ask surfaces are counterexamples, not ownership evidence

Question eligibility and bounded ask are adjacent, but they remain recovered External Orientation / bounded ask responsibilities rather than Operational Visibility ownership. The implementation explicitly limits question-family preparation to exact inventory-backed admission and excludes dispatch selection, presentation, rendering, surface arguments, and runtime mutation. `【F:seed_runtime/question_surface_inventory.py†L78-L95】`

The app-level bounded ask dispatcher then validates CLI usage, prepares eligibility input, evaluates bounded status, validates parameter count, optionally routes presentation, and dispatches through existing surface selection/execution helpers. That is CLI orchestration and bounded ask dispatch, not Operational Visibility ownership. `【F:scripts/seed_local.py†L2202-L2285】`

## Constitutional footing

Operational Visibility has constitutional footing only where implementation evidence is already visible:

- the app exposes operational visibility flags in `scripts/seed_local.py`; `【F:scripts/seed_local.py†L1402-L1416】`
- the diagnostic inventory declares those surfaces with read-only shape; `【F:seed_runtime/diagnostic_inventory.py†L232-L276】`
- the shape-audit implementation specs include those same surfaces; `【F:seed_runtime/diagnostic_shape_audit.py†L280-L297】`
- the operational surface inventory implementation discovers, classifies, and presents visibility coverage from parser and registry evidence. `【F:seed_runtime/operational_surface_inventory.py†L169-L231】`

That footing supports a bridge, not a campaign. The implementation evidence says Operational Visibility is observable. It does not say exactly one recovery boundary is ready.

## Recurring implementation pressures

The investigation found these recurring pressures:

1. **Discovery/classification/coverage adjacency.** Operational surface discovery, classification, registration comparison, and coverage presentation are tightly adjacent in `seed_runtime/operational_surface_inventory.py`. `【F:seed_runtime/operational_surface_inventory.py†L169-L231】`
2. **Registry/spec dual declaration.** Operational visibility surfaces must appear in both `DIAGNOSTIC_INVENTORY` and `IMPLEMENTATION_SPECS`, preserving the operational visibility contract. `【F:seed_runtime/diagnostic_inventory.py†L232-L276】` `【F:seed_runtime/diagnostic_shape_audit.py†L280-L297】`
3. **Shape audit as visibility enforcement.** Diagnostic shape audit checks declared registry facts against implementation markers across a fixed set of operational fields. `【F:seed_runtime/diagnostic_shape_audit.py†L21-L31】` `【F:seed_runtime/diagnostic_shape_audit.py†L711-L737】`
4. **Coverage presentation from classification output.** Visibility coverage reuses both discovered surfaces and classification rows to explain missing registration impact. `【F:seed_runtime/operational_surface_inventory.py†L132-L166】` `【F:seed_runtime/operational_surface_inventory.py†L311-L357】`

These are real pressures, but they are plural.

## Implementation-local candidates

The following candidates are visible but **not authorized**:

1. `Operational Surface Discovery != Operational Surface Classification`
   - Evidence: discovery builds `OperationalSurface` rows from parser actions, while classification prepares `_CliSurfaceClassificationInput` and classifies all CLI elements. `【F:seed_runtime/operational_surface_inventory.py†L169-L216】`

2. `Operational Surface Classification != Visibility Coverage Composition`
   - Evidence: classification emits `OperationalSurfaceClassificationAudit`, while coverage composes inventory and classification into discovered/registered/unregistered counts and missing-registration impact. `【F:seed_runtime/operational_surface_inventory.py†L195-L231】` `【F:seed_runtime/operational_surface_inventory.py†L311-L357】`

3. `Diagnostic Registry Declaration != Diagnostic Shape Audit Spec`
   - Evidence: registry entries declare read-only operational surface shapes, while shape-audit specs separately identify implementation modules/functions/flags. `【F:seed_runtime/diagnostic_inventory.py†L232-L276】` `【F:seed_runtime/diagnostic_shape_audit.py†L280-L297】`

4. `Operational Visibility Surface != Question-Family Presentation`
   - Evidence: question-surface inventory includes diagnostic-only and presentation-adjacent families, while bounded ask eligibility keeps question admission and dispatch separate from visibility surface ownership. `【F:seed_runtime/question_surface_inventory.py†L54-L63】` `【F:seed_runtime/question_surface_inventory.py†L165-L180】`

Because at least these four candidates are visible, the answer to “exactly one recurring implementation-local ownership boundary” is no.

## Answers to required questions

### 1. Where does External Orientation constitutionally end?

External Orientation constitutionally ends at narrow prepared handoffs from external/operator/parser/declaration material into existing bounded owners. Examples include `_QuestionFamilyEligibilityInput`, `_CliSurfaceClassificationInput`, and `_DiagnosticInventoryCompositionInput`. `【F:seed_runtime/question_surface_inventory.py†L66-L95】` `【F:seed_runtime/operational_surface_inventory.py†L119-L130】` `【F:seed_runtime/diagnostic_inventory.py†L35-L41】`

### 2. Where does Operational Visibility first become observable?

Operational Visibility first becomes observable at implementation-backed visibility outputs: operational surface inventory, visibility coverage audit, and operational surface classification audit. These are exposed by the CLI, declared in the diagnostic registry, checked by diagnostic shape specs, and implemented in `seed_runtime/operational_surface_inventory.py`. `【F:scripts/seed_local.py†L1402-L1416】` `【F:seed_runtime/diagnostic_inventory.py†L232-L276】` `【F:seed_runtime/diagnostic_shape_audit.py†L280-L297】` `【F:seed_runtime/operational_surface_inventory.py†L169-L231】`

### 3. Is there exactly one recurring implementation-local ownership boundary presently compressed?

No.

Implementation evidence exposes multiple adjacent pressures, not exactly one recurring implementation-local ownership boundary.

### 4. Did implementation evidence expose multiple possible recoveries?

Yes. The possible recoveries are listed without recommendation:

- Operational Surface Discovery vs. Operational Surface Classification;
- Operational Surface Classification vs. Visibility Coverage Composition;
- Diagnostic Registry Declaration vs. Diagnostic Shape Audit Spec;
- Operational Visibility Surface vs. Question-Family Presentation.

None is authorized by this investigation.

### 5. Did any existing campaign appear incomplete?

No.

The External Orientation completion audit already identified Operational Visibility as a bridge and preserved it as unknown rather than recovering it. This investigation did not find implementation evidence that invalidates that completion stance.

## Preserved unknowns

- Whether Operational Visibility deserves a future campaign at all remains unknown.
- If a future campaign is authorized, which of the visible candidates should become the first recovery footing remains unknown.
- Whether diagnostic registry/spec dual maintenance is a visibility ownership boundary or merely a contract enforcement pattern remains unknown.
- Whether unregistered operational surfaces represent intentional non-diagnostic CLI behavior, inventory debt, or classification overreach remains unknown.
- Whether question-family presentation belongs near Operational Visibility remains unknown and is not promoted by this report.

## Neighboring families

Neighboring families visible but not crossed:

- External Orientation, already completed;
- Diagnostic Visibility / Diagnostic Shape Audit;
- Question Eligibility / Bounded Ask;
- Source Navigation;
- Projection Diagnostics;
- Operational Responsibility;
- Observation / Pressure visibility.

The counterexamples named in the task remain outside Operational Visibility ownership unless future implementation evidence proves otherwise: CLI parsing, orientation preparation, question eligibility, diagnostic inventory composition, and source navigation composition.

## Confidence

Confidence: **medium-high**.

Reason: the implementation evidence is direct for the bridge and for multiple adjacent candidates. Confidence is not “high” because this was intentionally scout-mode and did not perform a full Operational Visibility family characterization.

## Acceptance answer

The bridge from External Orientation to Operational Visibility has revealed **multiple possible footings**, not exactly one lawful footing and not none.

No implementation recovery is authorized by this investigation.
