# Bounded Constitutional Question Slice 001

This is exactly one implementation ownership audit. It determines whether repository evidence exposes one immediately adjacent implementation-local ownership boundary responsible only for producing the bounded constitutional question consumed by `ConstitutionalViewSelection`.

It does not implement that boundary, redesign constitutional admission, redesign Question Grammar, redesign Selection, redesign Composition, redesign CLI behavior, invent a reasoning engine, invent constitutional authority, or recover more than one ownership boundary.

Repository authority wins.

## Investigation scope

Reviewed implementation-local evidence was limited to:

- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Composition;
- Constitutional View Selection Slice 001;
- existing bounded-question and admission implementation immediately adjacent to those surfaces.

Expansion was limited to adjacent read-model registration, bounded ask / QuestionFamily admission evidence, CLI dispatch evidence, and tests where needed to confirm current ownership and compatibility behavior.

## Implementation evidence

### Constitutional Process View

`ConstitutionalProcessView` is an immutable read-only view over existing constitutional process evidence. It preserves `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.

Its process stages provide the strongest local evidence about bounded constitutional-question admission before later constitutional work:

- `Pressure` says possible questions appear as pressure without becoming command authority.
- `Lawful Question` says Question Grammar admits or refuses bounded inquiry under evidence, authority, unknown, stop, and confidence limits.
- `Orientation` receives an admitted inquiry question and locates lawful attention before recovery.
- `Recovery`, `Cross-Examination`, `Completion Audit`, and `Lawful Stop` are later stages that must not be pulled into question production.

The view therefore supports an upstream distinction between operator pressure and admitted bounded question, while preserving that admission/orientation/recovery are separate from later selection and composition responsibilities.

### Constitutional Governance View

`ConstitutionalGovernanceView` is an immutable read-only view over existing governance evidence. It preserves `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.

Its governance relationship named `Question Grammar governs later Process movement` says Question Grammar constrains and locally authorizes the Lawful Question stage while refusing to become Orientation or Recovery. Its explicit refusals include governance execution, governance ownership, constitutional recovery, implementation recovery, hierarchy, runtime governance, and repository mutation.

This evidence supports a bounded-question owner only if that owner remains before selection and refuses later governance, recovery, reasoning, orchestration, mutation, and authority creation.

### Constitutional Fidelity View

`ConstitutionalFidelityView` is an immutable read-only view over completed fidelity evidence. It preserves `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.

Its preserved Unknowns are directly adjacent to this audit:

- whether Asymmetrical Question Construction is a distinct constitutional responsibility or only pressure inside or adjacent to admission remains Unknown;
- whether future implementation should introduce question construction before exact `QuestionFamily` admission remains Unknown;
- whether bounded ask should ever require inquiry orientation before selected dispatch remains Unknown.

Its explicit refusals include constitutional recovery, implementation recovery, ownership recovery, implementation mutation, repository mutation, runtime evaluation, fidelity enforcement, architectural redesign, and projection recovery.

This evidence prevents overclaiming a broad constitutional construction engine. It supports at most one narrow implementation-local boundary that preserves inquiry, intent, boundedness, and uncertainty without resolving the larger Unknowns.

### Constitutional View Composition

`ConstitutionalViewCompositionRequest` accepts `requested_views`, `composition_purpose`, and `output_format`. Its docstring states that the request owns only explicit registered-view selection, purpose labeling, and output-format intent, and does not select views heuristically, discover evidence, reason at runtime, recover authority, plan, orchestrate, or mutate repository state.

`build_constitutional_view_composition(...)` validates requested names against `CONSTITUTIONAL_READ_MODEL_CONTRACTS` and its local builder map, builds only those requested view artifacts, correlates already-existing evidence, preserves Unknowns and refusals, and returns one immutable artifact with `compatibility_answer="No."` when all contributing views preserve that answer.

Composition therefore consumes a selection that has already happened. It does not own the bounded constitutional question and does not determine relevance.

### Constitutional View Selection Slice 001

`constitutional_view_selection_slice_001.md` recovered `ConstitutionalViewSelection` as the pre-composition ownership boundary. It established that selection sits after bounded-question intake and registered constitutional view metadata, and before `ConstitutionalViewCompositionRequest`.

The slice says selection may only accept one bounded constitutional question, inspect registered constitutional view metadata, determine which already registered views are relevant, preserve unsupported selection uncertainty, and produce one immutable `SelectedConstitutionalViews` artifact. It must refuse constitutional recovery, ownership recovery, implementation recovery, evidence discovery, evidence invention, runtime reasoning, planning, orchestration, composition, repository mutation, and authority creation.

This proves the consumer side for this audit: selection consumes a bounded constitutional question, but it does not produce that question.

### Read-model registration evidence

`ConstitutionalReadModelContract` records recurring implementation obligations for constitutional read-model views: producer, artifact/formatter, JSON renderer, CLI consumer, diagnostic declarations, and read-only boundaries. It explicitly refuses constructing views, rendering output, dispatching CLI requests, registering diagnostics, creating constitutional authority, creating implementation authority, or defining future constitutional view contents.

`CONSTITUTIONAL_READ_MODEL_CONTRACTS` currently registers exactly `constitutional_process`, `constitutional_governance`, and `constitutional_fidelity`. `constitutional_read_model_registration(contract)` converts each constitutional contract into the existing `ReadModelViewRegistration` shape, and `ReadModelViewRegistration` itself refuses construction, rendering, CLI dispatch, argument parsing, projection publication, ledger writes, cluster mutation, and constitutional-content declaration.

Registration therefore supplies metadata consumed by selection and composition, not bounded-question production.

### Existing bounded-question and admission implementation

The adjacent bounded ask / QuestionFamily implementation uses exact `QuestionFamily` rows rather than free-text constitutional inquiry production.

Implementation and tests show these adjacent responsibilities:

- exact QuestionFamily lookup is separate from eligibility and dispatch;
- unknown question-family text is rejected before eligibility for bounded work dispatch;
- eligibility classifies registered rows as eligible now, eligible with parameters, diagnostic-only, not dispatchable, or unsupported;
- selected bounded-work pieces and dispatch requests preserve exact registered question-family identity and selected CLI dispatch surfaces;
- question-family definition and explanation surfaces preserve unknown-family information as bounded presentation when no inventory row exists;
- the inventory is read-only, static, and not a router or recommender.

This is an existing admission/dispatch mechanism for registered public QuestionFamily rows. It does not produce the bounded constitutional question consumed by `ConstitutionalViewSelection`, and it does not translate an operator constitutional inquiry into a bounded constitutional-question artifact.

### CLI dispatch evidence

The CLI exposes `--constitutional-view-composition` as an explicit requested-view surface. The operator supplies registered constitutional view names; the CLI passes those names into `constitutional_view_composition_request(...)` and then into `build_constitutional_view_composition(...)`.

This confirms the current implementation starts composition after view relevance has already been selected, and after any bounded constitutional question has already been expressed outside the implementation.

## Current ownership

### 1. Who presently owns the bounded constitutional question consumed by `ConstitutionalViewSelection`?

No implementation-local component presently owns it.

Repository evidence shows adjacent owners only:

- Question Grammar / admission evidence owns lawful admission or refusal at the constitutional process level, not an implemented artifact producer for selection;
- bounded ask / QuestionFamily code owns exact registered public question-family lookup, eligibility, selected dispatch request construction, and presentation, not constitutional view-selection question production;
- `ConstitutionalViewSelection` owns selection from an already bounded constitutional question, not production of that question;
- `ConstitutionalViewComposition` owns composition after explicit registered-view selection, not question production.

Therefore the bounded constitutional question consumed by selection is presently supplied externally by the operator, caller, or prompt context.

### 2. Is bounded-question production currently compressed into the operator?

Yes.

The operator currently has to formulate the bounded constitutional question before any later selection could consume it. The repository has no immutable artifact that receives an operator constitutional inquiry and produces one bounded constitutional question for `ConstitutionalViewSelection`.

### 3. Is it compressed into CLI parsing?

No, not as an implemented bounded-question producer.

CLI parsing exposes existing flags and exact registered question-family arguments. For constitutional composition, CLI parsing accepts explicit view names, not an operator constitutional inquiry. For bounded ask, CLI parsing accepts exact `QuestionFamily` values and hands them to lookup/eligibility/dispatch machinery. Neither path produces the bounded constitutional question consumed by `ConstitutionalViewSelection`.

### 4. Is it compressed into prompt construction?

Yes, for prompt-driven usage.

When a prompt asks for constitutional explanation, the prompt or caller must already encode the constitutional inquiry as a bounded question before selection can operate. Repository evidence does not show a separate immutable bounded-question artifact produced between operator inquiry and selection.

### 5. Does repository evidence expose one immediately adjacent implementation-local ownership boundary?

Yes.

Repository evidence exposes exactly one immediately adjacent implementation-local ownership boundary: **BoundedConstitutionalQuestion**.

The evidence selects this boundary because:

1. Constitutional Process View distinguishes pressure from a lawful admitted question.
2. Constitutional Governance View says Question Grammar constrains and locally authorizes Lawful Question while refusing later Orientation or Recovery.
3. Constitutional Fidelity View preserves uncertainty about broader question construction and admission, preventing recovery of a larger engine.
4. Constitutional View Selection Slice 001 requires one bounded constitutional question as input and explicitly does not produce it.
5. Constitutional View Composition requires explicit selected views and does not determine relevance or question scope.
6. Existing bounded ask / QuestionFamily machinery admits exact registered public rows but does not produce the constitutional selection question artifact.

The missing adjacent responsibility is therefore not admission redesign, Question Grammar redesign, Selection redesign, Composition redesign, CLI redesign, planning, orchestration, runtime reasoning, evidence discovery, or authority creation. It is the narrower local responsibility for preserving one operator constitutional inquiry as one immutable bounded constitutional question artifact, including uncertainty where scope cannot be established.

## Selected ownership boundary

Selected boundary: `BoundedConstitutionalQuestion`.

This name is selected because repository evidence points to the artifact and ownership boundary immediately before selection: the bounded constitutional question itself. The selected boundary is narrower than `ConstitutionalInquiry` and narrower than `ConstitutionalQuestionRequest` because this slice cannot lawfully recover constitutional admission, inquiry orientation, request routing, planning, or a broader inquiry lifecycle.

## Before

Before this audit:

```text
Operator / prompt / caller
        ↓
Externally formulated bounded constitutional question
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
        ↓
Bounded Constitutional Explanation
```

The repository had recovered selection and implemented composition, but the question supplied to selection remained external to implementation-local ownership.

## After

After this audit, no code behavior changes. The recovered implementation-local boundary for a possible later slice is:

```text
Operator Inquiry
        ↓
BoundedConstitutionalQuestion
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
        ↓
Bounded Constitutional Explanation
```

This is ownership recovery only. `BoundedConstitutionalQuestion` is not implemented here.

## Recovered producer

Recovered producer: `bounded_constitutional_question_from_operator_inquiry(...)`.

If implemented later, the producer may only:

- receive one operator constitutional inquiry;
- preserve bounded scope;
- preserve constitutional intent;
- preserve uncertainty where scope cannot be established;
- produce one immutable bounded-question artifact.

It must explicitly refuse:

- constitutional recovery;
- ownership recovery;
- implementation recovery;
- evidence discovery;
- evidence invention;
- view selection;
- composition;
- planning;
- orchestration;
- runtime reasoning;
- repository mutation;
- authority creation.

## Recovered artifact/helper

Recovered artifact/helper: `BoundedConstitutionalQuestion`.

If implemented later, the immutable artifact may contain only fields needed to preserve the bounded question for selection, such as:

- the operator inquiry as received;
- the preserved bounded question text or bounded-question identity;
- constitutional intent as received or preserved;
- scope status;
- uncertainty notes when bounded scope cannot be established;
- read-only / non-mutating boundary flags.

It must not contain selected view names, composed view artifacts, recovered evidence, invented evidence, runtime reasoning traces, plans, orchestration state, repository mutations, implementation ownership claims, or constitutional authority claims.

## Recovered consumer

Recovered consumer: `ConstitutionalViewSelection`.

Selection remains the consumer because prior repository evidence recovered it as the boundary that accepts one bounded constitutional question, inspects already registered constitutional view metadata, and produces one immutable selected-view artifact. The new boundary stops before that selection act.

## Relationship to ConstitutionalViewSelection

Repository evidence supports the relationship:

```text
Operator Inquiry
        ↓
Bounded Constitutional Question
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
        ↓
Bounded Constitutional Explanation
```

Support is bounded:

- Process evidence supports pressure becoming lawful question only through constrained admission/refusal.
- Governance evidence supports Question Grammar constraining Lawful Question while refusing Orientation or Recovery.
- Fidelity evidence preserves Unknowns about broader question construction and bounded ask orientation, preventing a broader recovery.
- Selection evidence requires a bounded constitutional question before selection and refuses producing broader authority.
- Composition evidence consumes explicitly requested registered views after selection and refuses relevance determination.

The relationship is therefore supported as an implementation-local ownership sequence, not as an implemented runtime pipeline and not as constitutional authority.

## Compatibility

Expected compatibility answer:

```text id="e0m7pc"
No.
```

Compatibility is preserved because this slice changes only one audit document and does not modify:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Composition;
- Constitutional View Selection;
- CLI behavior;
- JSON output;
- human rendering;
- diagnostic inventory;
- diagnostic shape audit;
- tests;
- runtime compatibility.

## Files changed

- `bounded_constitutional_question_slice_001.md`

## LOC changed

- Added: 333 lines
- Removed: 0 lines
- Net: +333 lines

## Tests executed

- `pytest -q tests/test_constitutional_view_composition.py tests/test_question_surface_inventory.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining work before bounded constitutional inquiry

Before bounded constitutional inquiry can use this boundary, a future implementation slice would still need to:

1. implement `BoundedConstitutionalQuestion` as an immutable artifact without broadening authority;
2. implement the narrow producer from one operator constitutional inquiry to that artifact;
3. prove bounded scope and constitutional intent are preserved;
4. prove uncertainty is preserved where scope cannot be established;
5. prove the artifact can feed `ConstitutionalViewSelection` without selection owning question production;
6. prove the producer refuses recovery, discovery, invention, view selection, composition, planning, orchestration, runtime reasoning, mutation, and authority creation;
7. update diagnostic inventory and diagnostic shape audit only if the boundary becomes an exposed diagnostic, audit, probe, view, operational CLI flag, or recordable output;
8. leave admission redesign, autonomous attention, planning, orchestration, and the Eye as future work.

## Lawful stop

This slice identifies exactly one immediately adjacent implementation-local ownership boundary responsible only for producing the immutable bounded constitutional question consumed by `ConstitutionalViewSelection`. It preserves all existing implementation contracts and compatibility, separates bounded inquiry from selection, introduces no new authority, performs no runtime reasoning, and leaves admission, autonomous attention, planning, orchestration, and the Eye as future work.

Repository authority wins.
