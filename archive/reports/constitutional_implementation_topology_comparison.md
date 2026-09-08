# Constitutional Implementation Topology Comparison

Repository authority wins.

## Boundary

This is exactly one Constitutional Implementation Topology Comparison.

It compares the already recovered constitutional process topology against implementation directly corresponding to question-family admission, bounded ask dispatch, inquiry orientation, and implementation-local visibility/recovery surfaces. It does not recover implementation ownership, redesign implementation, redesign constitutional topology, invent implementation stages, infer implementation behavior from constitutional theory, or infer constitutional theory from implementation convenience.

Implementation evidence determines implementation topology. Constitutional evidence determines constitutional topology. Neither redefines the other.

## App visibility used

The app was used only for bounded implementation visibility:

```text
python scripts/seed_local.py --question-surface-inventory
```

The app exposed current implementation-backed question families, bounded ask eligibility, dispatch surfaces, diagnostic relationships, responsibilities, and authority boundaries. This comparison uses that output as implementation visibility only; it does not treat app presentation vocabulary as constitutional knowledge.

## Constitutional authority used

The completed constitutional comparison authority is `constitutional_process_reconciliation.md`.

That artifact recovered the following bounded recurring constitutional process pattern:

```text
Pressure
    ↓
Lawful Question
    ↓
Orientation
    ↓
Recovery
    ↓
Cross-Examination
    ↓
Completion Audit
    ↓
Lawful Stop
```

It also preserved unresolved pressure around question construction versus question admission, admission before Orientation, Orientation before Recovery, cross-examination thresholds, and completion thresholds.

## Implementation evidence reviewed

Review stayed inside implementation directly corresponding to the already recovered process:

- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/inquiry_orientation.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_shape_audit.py`

The comparison also used the app output from `python scripts/seed_local.py --question-surface-inventory` to confirm the implementation-exposed surface topology.

## Implementation topology observed

Current implementation topology is not a single constitutional process owner. It is a set of implementation-local and compatibility surfaces around exact question-family selection, bounded work eligibility, dispatch to existing surfaces, and read-only inquiry orientation.

Observed implementation sequence for bounded `ask --question-family` work:

```text
operator text / CLI pressure
    ↓
exact QuestionFamily lookup
    ↓
prepared QuestionFamily eligibility input
    ↓
bounded work eligibility
    ↓
surface-argument validation or refusal
    ↓
selected dispatch surface / selected surface value
    ↓
dispatch request
    ↓
CLI namespace update / existing surface execution handoff
    ↓
post-dispatch compatibility handling
    ↓
message clear / downstream surface rendering
```

Observed implementation sequence for inquiry orientation:

```text
recorded inquiry note
    ↓
orientation composition request with lexical tokens
    ↓
orientation evidence collection from projected facts and source navigation
    ↓
selected related material and preserved supports
    ↓
answer payload / answer artifact assembly
    ↓
InquiryOrientationView rendering
```

Observed implementation sequence for diagnostic/shape visibility:

```text
diagnostic inventory declaration
    ↓
diagnostic implementation spec
    ↓
static implementation observation
    ↓
shape-audit row comparison
```

These implementation sequences are local implementation topology only. They are not constitutional topology.

## Stage-by-stage comparison

| Constitutional movement | Corresponding implementation responsibility? | Current implementation owner | Ownership assessment | Comparison |
| --- | --- | --- | --- | --- |
| Pressure | Yes, partially. CLI/operator input appears as `ask`, `--question-family`, recorded inquiry notes, and operational-pressure question family visibility. | `scripts/seed_local.py` argument handling; `QuestionSurfaceInventoryRow` for `operational pressure`; `record_inquiry_note` for inquiry notes. | Locally owned for CLI/input preservation; not independently constitutional. | Implementation accepts or preserves pressure-like input, but does not own constitutional pressure as a separate responsibility. |
| Lawful Question | Yes. Exact QuestionFamily lookup, preparation, bounded eligibility, refusal, and surface-argument validation decide whether exact inventory-backed work may proceed. | `seed_runtime/question_surface_inventory.py`. | Independently owned within implementation-local bounded ask topology, with compatibility handoff to CLI. | Implementation has a clear local admission/eligibility chain for exact QuestionFamily work. It is narrower than constitutional Question Grammar because it admits exact inventory-backed families, not arbitrary constitutional questions. |
| Orientation | Yes. Inquiry orientation has a dedicated read-only view builder and formatter for recorded inquiry notes. | `seed_runtime/inquiry_orientation.py`; CLI entry in `scripts/seed_local.py`. | Independently owned for inquiry-note orientation; locally owned for read-only lexical orientation only. | Implementation preserves orientation as a separate surface, but only for recorded inquiry notes and projected/read-model lexical material. |
| Recovery | Yes, partially and indirectly. Bounded ask dispatch selects existing surfaces such as reasoning path, selection path, knowledge reachability, and other audits that recover implementation-backed visibility. | Existing dispatch target surfaces selected by `bounded_work_selection_for_question_family`; diagnostic specs in `seed_runtime/diagnostic_shape_audit.py`. | Compressed/orchestration-owned by selected diagnostic surfaces and bounded ask dispatch; no single recovery owner in the compared implementation. | Implementation does not expose a general Recovery owner corresponding to constitutional Recovery. Recovery-like work is carried by the specific selected surface. |
| Cross-Examination | Yes, partially. Diagnostic shape audit compares declared diagnostic shape with observed implementation shape; question-family inventory exposes diagnostic relationship status. | `seed_runtime/diagnostic_shape_audit.py`; enrichment in `build_question_surface_inventory`. | Compatibility/local audit owned, not constitutional Cross-Examination ownership. | Implementation has comparison/audit surfaces, but no evidence of a general post-recovery cross-examination stage for every recovered responsibility. |
| Completion Audit | Yes, partially. Shape audit rows produce status comparisons, inventory findings validate question-surface rows, and downstream surfaces can render final reports. | `build_diagnostic_shape_audit`; `bounded_ask_inventory_findings`; downstream diagnostic formatters. | Compressed into diagnostic/audit surfaces; no independent completion-audit owner for the constitutional chain. | Implementation can audit bounded implementation completeness for specific surfaces, but completion is surface-local rather than a global constitutional Completion Audit stage. |
| Lawful Stop | Yes. Parser errors, refusal messages, non-dispatchable statuses, read-only authority boundaries, no-match uncertainty, and message clearing stop bounded work. | `bounded_work_refusal_for_eligibility`; `argparse` errors in `scripts/seed_local.py`; inquiry-orientation uncertainty/authority boundary. | Locally owned and compatibility owned. | Implementation preserves stop/refusal behavior, but stop is distributed across admission, CLI compatibility, orientation uncertainty, and downstream surfaces. |

## Implementation ownership assessment

### Independently owned responsibilities

- **Exact QuestionFamily lookup and admission.** `_lookup_exact_question_family` admits only inventory-backed exact question families and rejects unknown families.
- **Prepared eligibility handoff.** `_prepare_question_family_eligibility_input` narrows admitted text for bounded eligibility and explicitly excludes dispatch selection, presentation, rendering, surface arguments, and mutation.
- **Bounded work eligibility.** `_bounded_work_eligibility_for_prepared_question_family` classifies eligible, parameterized, diagnostic-only, and non-dispatchable work.
- **Inquiry-note orientation.** `build_inquiry_orientation` and its internal composition chain own read-only orientation over preserved notes and projected/read-model lexical supports.

### Locally owned responsibilities

- **Surface-argument validation.** `bounded_work_surface_args_for_eligibility` is local to already eligible bounded work.
- **Selected dispatch surface and selected value.** `bounded_work_selected_dispatch_surface_for_eligibility` and `bounded_work_selected_surface_value_for_eligibility` locally prepare selected bounded work.
- **Inquiry-orientation evidence selection, answer payload, and rendering.** These are local to `seed_runtime/inquiry_orientation.py` and do not claim broader recovery ownership.

### Compatibility-owned responsibilities

- **CLI namespace mutation for dispatch.** `apply_bounded_work_dispatch_namespace_update` applies an already selected surface value to the CLI namespace as compatibility with existing surfaces.
- **Post-dispatch JSON compatibility.** `apply_bounded_work_dispatch_result` preserves a special knowledge-reachability JSON handoff.
- **Presentation handoff and message clearing.** Presentation and dispatch clear `args.message` after handoff to prevent free-text ask from continuing.
- **Question-family diagnostic relationship enrichment.** Inventory rows connect to diagnostic inventory and shape specs where possible, but this is compatibility between surfaces rather than constitutional ownership.

### Compressed responsibilities

- **Recovery is compressed into selected answering/diagnostic surfaces.** Bounded ask dispatch selects existing surfaces; the dispatch layer does not independently own recovery semantics.
- **Cross-Examination and Completion Audit are compressed into diagnostic shape/inventory audit surfaces when the implementation question is about diagnostic surface shape.** There is no evidence of a universal implementation stage that cross-examines every recovered responsibility before completion.
- **Lawful Stop is distributed across exact lookup, eligibility refusal, parser errors, read-only authority boundaries, and no-match uncertainty.** It is preserved as behavior, but not independently owned as one implementation stage.

## Identified compressions

### Compression 1: Recovery into selected surfaces

1. **Constitutional responsibilities compressed:** Recovery, and sometimes the answer-production portion following Orientation.
2. **Implementation owner presently carrying them:** Selected dispatch target surfaces named by `BOUNDED_ASK_DISPATCH_SURFACES`, reached through `bounded_work_selection_for_question_family` and `execute_bounded_work_dispatch`.
3. **Compression type:** Orchestration compression. Bounded ask orchestrates existing surfaces rather than owning a general Recovery responsibility.
4. **Future implementation recovery justified?** Repository evidence justifies preserving this as a future implementation-recovery pressure only. Do not recover it here.
5. **Pressure only:** Whether implementation should expose a distinct recovery boundary between eligibility/orientation and selected answering surfaces.

### Compression 2: Cross-Examination and Completion Audit into diagnostics

1. **Constitutional responsibilities compressed:** Cross-Examination and Completion Audit for implementation-surface visibility.
2. **Implementation owner presently carrying them:** `seed_runtime/diagnostic_shape_audit.py` and `bounded_ask_inventory_findings` for surface inventory consistency.
3. **Compression type:** Implementation-local audit compression, with compatibility to diagnostic inventory declarations.
4. **Future implementation recovery justified?** Repository evidence justifies preserving pressure around whether post-recovery cross-examination and completion thresholds need implementation-visible separation. Do not recover it here.
5. **Pressure only:** Whether implementation should distinguish shape comparison, cross-examination threshold, and completion threshold as separate implementation responsibilities.

### Compression 3: Lawful Stop across admission, CLI, and read-only boundaries

1. **Constitutional responsibilities compressed:** Lawful Stop is distributed across Lawful Question refusal, orientation uncertainty, CLI parser refusal, and compatibility message clearing.
2. **Implementation owner presently carrying them:** `_lookup_exact_question_family`, `_bounded_work_eligibility_for_prepared_question_family`, `bounded_work_refusal_for_eligibility`, `_handle_question_family_dispatch`, `format_inquiry_orientation`, and inquiry-orientation boundary constants.
3. **Compression type:** Implementation-local and compatibility compression.
4. **Future implementation recovery justified?** Repository evidence justifies only preserving pressure around whether stop boundaries should become separately visible in implementation topology. Do not recover it here.
5. **Pressure only:** Whether implementation stop/refusal boundaries should be independently inventoried for bounded inquiry work.

### Compression 4: Question construction into exact admission

1. **Constitutional responsibilities compressed:** Question construction pressure and Question admission are not separately exposed for bounded ask; exact text must already match a known QuestionFamily.
2. **Implementation owner presently carrying them:** `_lookup_exact_question_family` and `_prepare_question_family_eligibility_input`.
3. **Compression type:** Implementation-local compression.
4. **Future implementation recovery justified?** Repository evidence justifies preserving pressure because implementation supports exact inventory admission but not a separate construction owner. Do not recover it here.
5. **Pressure only:** Whether question construction before exact QuestionFamily admission needs implementation evidence beyond current exact-match lookup.

## Compatibility boundaries

- Bounded ask maps exact QuestionFamily identifiers to existing CLI surfaces rather than replacing those surfaces.
- Diagnostic-only question families are visible in inventory but are refused as bounded ask inquiry-answer surfaces.
- Diagnostic relationship status connects question-family rows to diagnostic inventory and diagnostic shape specs when current implementation supports that relationship.
- Knowledge reachability uses a canonical diagnostic-surface alias to preserve compatibility between bounded ask dispatch naming and diagnostic registry naming.
- CLI namespace updates and message clearing are compatibility mechanics, not constitutional movements.

## Orchestration boundaries

- `scripts/seed_local.py` orchestrates `ask --question-family` by lookup, eligibility, optional argument validation, presentation handoff, selected dispatch, post-dispatch compatibility handling, and stop/refusal.
- `seed_runtime/question_surface_inventory.py` owns bounded ask selection artifacts but repeatedly limits each function to a narrow local handoff.
- `seed_runtime/inquiry_orientation.py` orchestrates note tokenization, evidence collection, selection, answer payload preparation, and rendering while preserving read-only boundaries.
- `seed_runtime/diagnostic_shape_audit.py` orchestrates declared-vs-observed implementation shape comparison without executing target surfaces.

## Constitutional fidelity

### 1. Does implementation preserve the recovered constitutional topology?

Partially. Implementation preserves recognizable corresponding responsibilities for pressure, lawful question/admission, orientation, recovery-like answering surfaces, comparison/audit, completion-like status reporting, and lawful stop/refusal. However, implementation does not preserve the recovered constitutional topology as independently owned implementation stages.

### 2. Where does implementation diverge?

- Lawful Question is implemented as exact inventory-backed QuestionFamily admission, not as the full constitutional Question Grammar discipline.
- Orientation is implemented as a specific inquiry-note orientation probe, not a general prerequisite for every bounded ask dispatch.
- Recovery is carried by selected existing diagnostic/answer surfaces rather than a distinct implementation Recovery owner.
- Cross-Examination and Completion Audit appear as specific audit surfaces and inventory consistency checks, not as universal stages following every recovery.
- Lawful Stop is distributed across parser errors, local refusals, no-match uncertainty, authority boundaries, and compatibility message clearing.

### 3. Are any constitutional stages absent?

No constitutional stage is entirely absent as an implementation-corresponding responsibility, but Recovery, Cross-Examination, Completion Audit, and Lawful Stop are not independently owned across the compared implementation topology. They are present only as surface-local, audit-local, orchestration-local, or compatibility-local behavior.

### 4. Are any implementation stages constitutionally unsupported?

Yes, as implementation mechanics only:

- CLI namespace update.
- Message clearing after dispatch or presentation handoff.
- Canonical diagnostic-surface aliasing.
- JSON compatibility toggling for knowledge reachability.
- Exact inventory row enrichment with diagnostic relationship metadata.

These are implementation-compatible mechanics. They do not claim constitutional-stage status.

## Preserved Unknowns

- Whether implementation should ever expose a distinct implementation Recovery owner remains Unknown.
- Whether bounded ask should require inquiry orientation before selected dispatch remains Unknown.
- Whether cross-examination thresholds should become implementation-visible beyond diagnostic shape/inventory audits remains Unknown.
- Whether completion thresholds should become implementation-visible beyond surface-local audit completion remains Unknown.
- Whether lawful stop should be independently inventoried for bounded inquiry work remains Unknown.
- Whether question construction before exact QuestionFamily admission has a distinct implementation responsibility remains Unknown.
- Whether the exact QuestionFamily admission surface is sufficient for future constitutional Question Grammar implementation remains Unknown.

## Readiness

```text
Ready for implementation recovery
```

This classification means only that implementation-local ownership compression is visible enough to support a future bounded implementation recovery inquiry. It does not perform that recovery.

## Confidence

- **High confidence** that exact QuestionFamily admission, bounded eligibility, bounded dispatch selection, and inquiry-note orientation are implementation-backed responsibilities.
- **High confidence** that implementation does not currently expose a single owner for the entire recovered constitutional process.
- **Medium-high confidence** that Recovery is compressed into selected answering/diagnostic surfaces.
- **Medium confidence** that Cross-Examination and Completion Audit are compressed into diagnostic/audit surfaces rather than independently owned implementation stages.
- **Medium confidence** that Lawful Stop is distributed across admission, CLI compatibility, orientation uncertainty, and read-only authority boundaries.
- **Low confidence** for any claim about how these pressures should be recovered in future implementation work, because this comparison intentionally does not recover implementation ownership.

Constitutional implementation topology comparison complete.
