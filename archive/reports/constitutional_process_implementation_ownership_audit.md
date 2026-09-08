# Constitutional Process Implementation Ownership Audit

Repository authority wins.

## Boundary

This is exactly one bounded implementation ownership audit. It starts from the implementation named in the task and inspects only implementation immediately corresponding to the four candidate pressures preserved by `constitutional_implementation_topology_comparison.md`.

This audit does not implement the constitutional process, does not recover a general Recovery owner, Question Grammar engine, Cross-Examination engine, Completion Audit engine, global Stop owner, framework, registry, planner, scheduler, or workflow, and does not recover an implementation slice because topology pressure alone exists.

## Implementation inspected

Primary implementation inspected:

- `constitutional_implementation_topology_comparison.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`

Focused implementation evidence followed from those files:

- `tests/test_question_surface_inventory.py`
- `tests/test_inquiry_orientation.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

App visibility checked:

```text
python scripts/seed_local.py --question-surface-inventory
python scripts/seed_local.py --diagnostic-inventory
python scripts/seed_local.py --diagnostic-shape-audit
```

Test visibility checked:

```text
pytest -q tests/test_question_surface_inventory.py tests/test_inquiry_orientation.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Audit method

Each candidate pressure was assessed independently against the same questions:

1. What implementation currently owns the responsibility?
2. Is an adjacent compressed responsibility directly observable?
3. Is a producer, artifact/helper, and consumer visible?
4. Would recovery reduce ownership compression?
5. Or would it merely wrap, rename, or relocate already-owned behavior?

Classification vocabulary is limited to:

```text
Recoverable
Already lawfully owned
Needs additional implementation visibility
```

## Pressure 1: Question construction / admission

### Current owner

Exact question-family admission is owned by `seed_runtime/question_surface_inventory.py`:

- `_lookup_exact_question_family` accepts only inventory-backed exact `QuestionFamily` text and rejects unknown text.
- `_prepare_question_family_eligibility_input` prepares admitted exact question-family text for bounded eligibility only.
- `_bounded_work_eligibility_for_prepared_question_family` classifies the admitted family for bounded work eligibility.
- `scripts/seed_local.py` consumes these helpers in `apply_bounded_ask_dispatch` before any selected surface dispatch.

### Adjacent compressed responsibility directly observable?

No directly recoverable construction responsibility is observable before exact lookup. The observable implementation boundary is exact inventory admission, not construction. Operator prose that does not supply `ask --question-family <exact-question-family>` is refused by CLI compatibility rather than transformed into a constructed family.

### Producer, artifact/helper, and consumer visible?

For admission, yes:

- Producer: `_lookup_exact_question_family` / `_prepare_question_family_eligibility_input`.
- Artifact/helper: `ExactQuestionFamilyLookupResult` and `_QuestionFamilyEligibilityInput`.
- Consumer: `_bounded_work_eligibility_for_prepared_question_family` and `apply_bounded_ask_dispatch`.

For question construction before admission, no. There is no implementation-backed producer that constructs a question family from free text, no construction artifact, and no consumer that relies on constructed output.

### Would recovery reduce ownership compression?

Not with current evidence. Adding a construction boundary would either infer a grammar/construction responsibility that the implementation intentionally does not expose or wrap exact lookup with a renamed step.

### Wrap, rename, or relocate risk

High. Any recovered construction owner would merely rename existing exact lookup/preparation behavior or introduce forbidden Question Grammar-like behavior without implementation evidence.

### Classification

```text
Already lawfully owned
```

The exact admission chain is already lawfully owned. The distinct construction responsibility remains unsupported by implementation evidence rather than immediately recoverable.

## Pressure 2: Recovery / selected surfaces

### Current owner

Recovery-like answering is owned by selected existing answering or diagnostic surfaces, with bounded ask owning only selection and dispatch handoff:

- `BOUNDED_ASK_DISPATCH_SURFACES` maps exact question families to existing surfaces.
- `bounded_work_selected_dispatch_surface_for_eligibility` selects the dispatch surface after eligibility.
- `bounded_work_selected_surface_value_for_eligibility` prepares the surface value.
- `bounded_work_selection_for_question_family` combines selected surface and value.
- `bounded_work_dispatch_request_for_selection` prepares an invocation request.
- `execute_bounded_work_dispatch`, `apply_bounded_work_dispatch_result`, and message-clearing helpers preserve CLI compatibility.
- The downstream selected surfaces own their own answer/audit production.

### Adjacent compressed responsibility directly observable?

A handoff is directly observable between admitted eligible work and selected dispatch. However, the repository already exposes narrow implementation-local ownership boundaries for selected surface identity, selected surface value, dispatch request construction, namespace update, result production, post-dispatch compatibility, and message clearing.

The remaining recovery pressure is semantic: selected surfaces perform their own answer/audit work. There is no implementation evidence of a shared recovery artifact between eligibility and all answering surfaces.

### Producer, artifact/helper, and consumer visible?

For dispatch handoff, yes:

- Producer: `bounded_work_selection_for_question_family` and `bounded_work_dispatch_request_for_selection`.
- Artifact/helper: `BoundedWorkSelectionResult` and `BoundedWorkDispatchRequest`.
- Consumer: `execute_bounded_work_dispatch` and CLI downstream rendering.

For a distinct recovery boundary, no:

- There is no shared recovered-work artifact consumed by all selected answer or diagnostic surfaces.
- The selected surface itself is the recovery/answer owner.

### Would recovery reduce ownership compression?

Not as a bounded implementation-local slice under current evidence. The immediately adjacent dispatch boundaries are already decompressed. A new Recovery owner would either centralize semantics currently owned by selected surfaces or wrap `BoundedWorkDispatchRequest` with a broader name.

### Wrap, rename, or relocate risk

High. Recovering a general or shared recovery owner would violate the task constraints and would not preserve the local ownership demonstrated by existing selected surfaces.

### Classification

```text
Already lawfully owned
```

The implementation-local handoff from admitted work to selected surfaces is already lawfully owned. The broader Recovery pressure needs constitutional or future implementation visibility before any new boundary is recoverable, but it is not directly recoverable here.

## Pressure 3: Cross-Examination / Completion Audit

### Current owner

Diagnostic comparison and completion-like status classification are owned by `seed_runtime/diagnostic_shape_audit.py` and by inventory consistency checks:

- `DiagnosticImplementationSpec` declares expected implementation shape for diagnostics.
- `build_diagnostic_shape_audit` compares diagnostic inventory declarations with observed implementation shape.
- `DiagnosticShapeAuditRow` carries per-field declared/observed/status output.
- `DiagnosticShapeAuditSummary` carries aggregate completion-like counts.
- `bounded_ask_inventory_findings` checks question-surface inventory consistency against bounded ask maps.
- Diagnostic inventory and shape-audit tests prove the diagnostic surfaces remain visible and checked.

### Adjacent compressed responsibility directly observable?

No distinct Cross-Examination owner or distinct Completion Audit owner is directly observable outside audit-local behavior. The observable implementation is a diagnostic shape audit: compare declared shape with observed shape and classify status. Completion-like status is a field of the audit result, not a separate downstream owner.

### Producer, artifact/helper, and consumer visible?

For audit-local comparison, yes:

- Producer: `build_diagnostic_shape_audit`.
- Artifact/helper: `DiagnosticShapeAuditRow` and `DiagnosticShapeAuditSummary`.
- Consumer: `format_diagnostic_shape_audit`, `diagnostic_shape_audit_json`, and CLI flags.

For separate Cross-Examination and Completion Audit responsibilities, no:

- There is no separate cross-examination artifact consumed by a completion classifier.
- There is no separate completion audit producer that consumes cross-examined findings across implementation surfaces.

### Would recovery reduce ownership compression?

No. Splitting diagnostic shape comparison into Cross-Examination and Completion Audit wrappers would merely rename parts of one lawful audit-local implementation. It would not expose a repository-backed producer/artifact/consumer boundary that currently exists but is compressed.

### Wrap, rename, or relocate risk

High. A recovered split would impose constitutional vocabulary on audit-local implementation without evidence.

### Classification

```text
Already lawfully owned
```

Diagnostic shape comparison and status reporting are already lawfully owned as one audit-local responsibility.

## Pressure 4: Lawful Stop

### Current owner

Stop/refusal behavior is distributed among local owners:

- CLI compatibility in `scripts/seed_local.py` rejects invalid `ask`, `--question-family`, `--surface-args`, and `--presentation` combinations.
- `_lookup_exact_question_family` rejects unknown exact question families before eligibility.
- `_bounded_work_eligibility_for_prepared_question_family` classifies non-dispatchable and diagnostic-only families.
- `bounded_work_refusal_for_eligibility` produces refusal messages for non-permitted bounded work.
- `bounded_work_surface_args_for_eligibility` rejects missing, extra, or invalid surface args for parameterized surfaces.
- Inquiry orientation owns read-only authority and uncertainty text through `AUTHORITY_BOUNDARY`, `UNCERTAINTY_WITH_MATCHES`, and `UNCERTAINTY_WITHOUT_MATCHES`.
- Message-clearing helpers preserve post-handoff CLI compatibility.

### Adjacent compressed responsibility directly observable?

Multiple stop points are observable, but they are intentionally local to the owner that knows the stopping condition. One refusal boundary after bounded eligibility is already directly observable through `BoundedWorkRefusalResult`. Other stops remain parser compatibility, exact admission failure, parameter validation, orientation uncertainty, and post-dispatch message clearing.

### Producer, artifact/helper, and consumer visible?

For local bounded-work refusal, yes:

- Producer: `bounded_work_refusal_for_eligibility`.
- Artifact/helper: `BoundedWorkRefusalResult`.
- Consumer: `apply_bounded_ask_dispatch`, which passes the message to `parser.error`.

For one global lawful stop owner, no:

- There is no common stop artifact consumed by parser errors, inquiry orientation rendering, dispatch compatibility, and downstream surfaces.
- Stop conditions are tied to their local owners and compatibility boundaries.

### Would recovery reduce ownership compression?

No. A global stop owner would centralize unrelated parser, admission, eligibility, argument, read-only, and compatibility responsibilities. A narrower recovery after bounded eligibility is already present as `BoundedWorkRefusalResult`.

### Wrap, rename, or relocate risk

High. Recovery would either duplicate the existing bounded refusal helper or relocate local stop behavior away from the implementation that has the evidence to refuse.

### Classification

```text
Already lawfully owned
```

Lawful Stop remains lawfully distributed among local implementation owners. The directly observable bounded-work refusal slice has already been decompressed.

## Selected pressure

No pressure selected for implementation recovery.

Repository evidence shows local ownership boundaries already exist for exact admission, bounded eligibility, selected dispatch handoff, bounded refusal, diagnostic shape audit, and inquiry orientation. The remaining candidate pressures are topology pressure only or already lawfully owned in local implementation. Recovering another boundary in this audit would wrap, rename, relocate, or over-centralize already-owned behavior.

## Readiness classification

| Pressure | Classification |
| --- | --- |
| Question construction / admission | Already lawfully owned |
| Recovery / selected surfaces | Already lawfully owned |
| Cross-Examination / Completion Audit | Already lawfully owned |
| Lawful Stop | Already lawfully owned |

Overall readiness:

```text
No implementation recovery selected
```

No `constitutional_process_implementation_slice_001.md` is produced because no pressure is classified `Recoverable` in this audit.

## Preserved Unknowns

- Whether future implementation should introduce question construction before exact `QuestionFamily` admission remains Unknown.
- Whether future bounded ask should require inquiry orientation before selected dispatch remains Unknown.
- Whether a shared implementation Recovery artifact should ever exist between bounded eligibility and selected answering surfaces remains Unknown.
- Whether diagnostic comparison and completion thresholds should ever become distinct implementation-visible responsibilities remains Unknown.
- Whether stop/refusal surfaces should ever be inventoried independently across CLI, admission, orientation, dispatch, and downstream surfaces remains Unknown.
- Whether constitutional vocabulary should map to broader implementation stages remains Unknown unless future implementation evidence creates producer/artifact/consumer boundaries.

## Confidence

- **High confidence** that exact `QuestionFamily` admission and bounded eligibility are implementation-backed and already locally owned.
- **High confidence** that bounded dispatch handoff has existing local producer/artifact/consumer boundaries.
- **High confidence** that diagnostic shape comparison and status classification are audit-local behavior rather than separate Cross-Examination and Completion Audit owners.
- **High confidence** that the bounded-work refusal helper already owns one local refusal boundary after eligibility.
- **Medium confidence** that no additional implementation-local ownership boundary is recoverable without changing compatibility, because this audit stayed intentionally bounded to the requested implementation path.
