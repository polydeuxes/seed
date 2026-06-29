# Inquiry Anchor Dependency-Head Investigation

## Scope

This bounded investigation reviews implementation evidence for a recurring dependency-center role across inquiry-like surfaces. `Inquiry Anchor` is only a working name in this report. The investigation does not recover ownership, rename vocabulary, add runtime behavior, change parsing, or promote an ontology.

The reviewed question is not whether the repository has one semantic concept named `subject`. The reviewed question is whether different implementation identities repeatedly occupy the same ordering role:

```text
inquiry / surface request
-> established organizing identity
-> evidence selection or validation
-> reasoning / lineage assembly
-> answer composition / rendering
```

## Implementation evidence reviewed

### Question Surface Inventory

`seed_runtime/question_surface_inventory.py` statically maps `question_family` values to answering surfaces. The dispatch map includes entries for operational pressure, current operational explanation, derivation explanation, selection explanation, knowledge reachability, capability pressure, ownership ambiguity, observation domains, observation permissions, authority-constrained ownership surfaces, listener endpoint reachability, and projection shape visibility.

Evidence:

- `BOUNDED_ASK_DISPATCH_SURFACES` uses exact `question_family` strings as the organizing dispatch identity and maps them to surface names.
- `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` declares that `derivation explanation` requires `domain` and `subject`, and `selection explanation` requires `target`.
- `bounded_status_for_question_family()` determines whether a family is eligible now, eligible with parameters, diagnostic-only, or not dispatchable before dispatch occurs.
- Inventory rows for derivation and selection explicitly state that required values are not inferred.

Implementation implication: question-family identity is an organizing identity for bounded ask dispatch, but it is not a general subject ontology. Some families require additional surface-local identities before evidence selection can proceed.

### Bounded ask dispatch

`scripts/seed_local.py` validates the bounded ask shape before routing to a surface. It rejects `--question-family` outside exact `ask --question-family <exact-question-family>` usage, rejects unknown families, derives eligibility, enforces required explicit surface args, and only then sets the target surface argument on the parsed namespace.

Evidence:

- Missing `--question-family` under `ask` is rejected before routing.
- Unknown families are rejected against `build_question_surface_inventory()`.
- Parameterized families must provide exactly the configured number of explicit operator-provided values.
- For parameterized families, the provided values become the existing surface argument (`reasoning_path` receives `(domain, subject)`; `selection_path` receives `target`) before the normal surface implementation runs.

Implementation implication: dispatch validation happens before reasoning. The organizing identity may be `question_family`, but for parameterized answers it is insufficient alone; it hands off to `domain`/`subject` or `target` as the downstream dependency head.

### Reasoning Path

`seed_runtime/reasoning_path_audit.py` exposes `ReasoningPathAudit(domain, subject, ...)` and `build_reasoning_path_audit(state, domain, subject, ...)`. The builder gathers implemented evidence surfaces and then filters or relates them using the already-supplied `subject` and `domain`.

Evidence:

- The audit object carries `domain` and `subject` as first-class output fields.
- The builder signature requires `domain` and `subject` before it can execute.
- Ownership discrepancy rows are selected by `_matches(subject, row.subject, row.conflict)` and by matching `subject` against diagnostic capability-need records.
- Capability need consumers are selected by matching `subject` against capability names, subjects, and diagnostics.
- Pressure consumers are selected by `subject` or by `domain` matching pressure category.
- Story impact is selected by `subject` appearing in operational-story JSON or `domain` matching story focus.
- Only after those selections does the implementation create conclusion and lineage payloads and hand them to `_reasoning_path_from_payloads()`.

Implementation implication: Reasoning Path strongly supports the dependency-center pattern. Reasoning does not discover the identity; it assumes `domain` and `subject` already exist, and evidence selection branches from them.

### Selection Path

`seed_runtime/selection_path_audit.py` exposes `SelectionPathAudit(target, selected, ...)` and `build_selection_path_audit(state, target, ...)`. The builder normalizes the already-provided `target`, compares it to implemented selection surfaces, and either builds a selection lineage from pressure/story evidence or returns an explicit unknown result.

Evidence:

- The audit object carries `target` as the first output field.
- The builder signature requires `target` before it can execute.
- `target` is normalized before evidence branches.
- Recognized targets (`current_focus`, `primary_pressure`, story focus, or pressure category matches) determine which selection path is built.
- Unknown targets still return a candidate set, but the result is `selected="unknown"`, `selection_factors=["unknown"]`, and an explicit unknown reason: no implementation-backed selection evidence was discovered for the target.

Implementation implication: Selection Path supports the role pattern while also supplying a counterexample boundary. Evidence selection is not fully absent for unknown targets because candidates can still be listed, but subject-specific selection reasoning is explicitly unavailable when the organizing `target` is not recognized.

### Reference Selection

`seed_runtime/reference_selection.py` exposes `ReferenceSelection(domain, question, selected_reference, ...)` and `build_reference_selection(repo_root, domain)`. It branches first on `domain`; only `history` is implementation-backed.

Evidence:

- The output carries `domain` and `question` before selected reference, rationale, alternatives, boundary, and limitations.
- Non-`history` domains return an unsupported-domain result with unknown reference and a limitation that only `history` is currently implementation-backed.
- The `history` branch builds comparison references from impact and snapshot-policy audits.
- Rendering is downstream of the already-built selection object.

Implementation implication: Reference Selection supports the dependency-center pattern for a `domain` identity. It also limits the claim: unsupported domains prove that not every identity value leads to reasoning; validation/branching can stop the reasoning path.

### Inquiry Orientation

`seed_runtime/inquiry_orientation.py` records and selects `InquiryNoteRecord` values, then builds `InquiryOrientationView` from an already-selected note. It explicitly constrains matches to deterministic lexical overlap and does not treat the note as intent, concern, ownership, recommendation, command, or semantic interpretation.

Evidence:

- `record_inquiry_note()` validates that raw notes are non-empty before preservation.
- `select_inquiry_note()` returns either a specific note id or the latest recorded note; `build_inquiry_orientation()` receives an `InquiryNoteRecord`, not arbitrary unresolved text.
- `_compose_architectural_orientation_answer()` calls `_collect_architectural_orientation_evidence()` before composing answer material.
- `_collect_architectural_orientation_evidence()` tokenizes `note.raw_note` and uses those tokens to select fact and source-navigation matches.
- Formatting is downstream of the view and renders related material, support, uncertainty, and authority boundary.

Implementation implication: Inquiry Orientation supports the ordering pattern but not semantic subject resolution. The organizing identity is the preserved note (and derived lexical token set), not a parsed ontology.

### Source Navigation

`seed_runtime/source_navigation.py` exposes source navigation around a `query`. It uses projected source facts only, normalizes the query, matches rows against the query, and returns bounded explanations with non-claim boundaries.

Evidence:

- The module-level boundary says it reads preserved repository source facts and does not inspect files, parse source, ingest observations, or infer behavior/reachability/ownership.
- `SourceNavigationView` carries `query` ahead of definitions, imports, repository artifact explanations, support, and non-claims.
- `build_source_navigation(state, query)` normalizes `query`, builds support rows, and filters matches using `_matches(row, normalized_query)`.

Implementation implication: Source Navigation supports an implementation role where `query` is the dependency head for evidence selection, while explicitly rejecting semantic expansion beyond projected source-fact matches.

### Operational Story and Answer Composition

`seed_runtime/operational_story.py` is not a direct subject-resolution surface. It composes current operational evidence from pressure, capability, privilege, correlation, impact, and investigation-path surfaces. Its organizing center is the primary pressure/focus selected from pressure audit output.

Evidence:

- `build_operational_story()` builds pressure, capability, privilege, correlation, impact, and investigation-path inputs; then `primary = pressure_audit.pressures[0] if pressure_audit.pressures else None` becomes the focus input.
- `_domain_for(primary)` selects the investigation path domain from that primary pressure.
- `_compose_operational_story_payloads()` separates answer, reasoning, supporting evidence, boundary, and limitations.
- The public `OperationalStory` is assembled only after these payloads exist.

Implementation implication: Operational Story supports the downstream composition half of the pattern. It has an organizing focus, but that focus is selected by existing operational evidence rather than supplied by an inquiry. This is evidence for a dependency-center role in answer composition, not for a general inquiry-anchor owner.

## Recurring ordering patterns

The strongest repeated ordering is:

1. **Validate or establish a surface-local identity.** Examples: exact `question_family`, explicit `domain`/`subject`, explicit `target`, explicit `domain`, selected `InquiryNoteRecord`, normalized `query`, selected `primary` pressure/focus.
2. **Branch or filter evidence from that identity.** Examples: bounded ask maps family to surface; Reasoning Path filters discrepancies, capability needs, pressure, privilege, and story by subject/domain; Selection Path normalizes target before selecting implemented path; Reference Selection branches on domain; Inquiry Orientation tokenizes the note before matching facts/source navigation; Source Navigation filters projected source rows by query.
3. **Assemble reasoning/lineage after evidence is selected.** Examples: Reasoning Path constructs conclusion and lineage payloads after subject/domain filtering; Selection Path constructs result/lineage payloads after target matching; Reference Selection constructs choice/lineage payloads after domain branching; Inquiry Orientation collects evidence before composing the answer.
4. **Compose/render answer downstream.** Formatters operate on already-built audit/view objects. Operational Story and Inquiry Orientation explicitly separate answer material from evidence/reasoning/boundary/limitations before rendering.

## Recurring dependency patterns

The recurring invariant appears to be about **role**, not shared ontology:

| Surface | Identity occupying the role | What depends on it | Evidence of boundary |
| --- | --- | --- | --- |
| Question Surface Inventory / bounded ask | `question_family` | Dispatch surface, eligibility, required args, presentation vs raw surface | Exact family validation; unknown/non-dispatchable families rejected |
| Reasoning Path | `domain` + `subject` | Evidence filtering, derived conclusions, consumers, story impact | Subject/domain required as inputs; no inference in inventory |
| Selection Path | `target` | Selection branch, selected result, candidate lineage, unknown result | Unknown target produces explicit unknown reasoning |
| Reference Selection | `domain` | Supported-domain branch, selected reference, rationale, alternatives | Only `history` is implementation-backed |
| Inquiry Orientation | selected `InquiryNoteRecord` and token set from `raw_note` | Related material matching, support, uncertainty | Lexical overlap only; no intent/ownership/recommendation claims |
| Source Navigation | `query` | Projected source fact matching and bounded explanations | Source-fact lookup only; no runtime/semantic claims |
| Operational Story | primary pressure/focus | Investigation path domain, focus, support, answer payload | Focus comes from existing pressure evidence, not inquiry parsing |

These identities are not interchangeable. `question_family`, `subject`, `target`, `domain`, `query`, `note`, and `focus` have different meanings and different validation rules. What recurs is the architectural role: a value is established before subject-specific evidence selection and reasoning begin.

## Counterexamples and limits

### No single ontology is implemented

The implementation does not collapse `question_family`, `subject`, `target`, `domain`, `query`, `note`, and `focus` into one model. Required arguments and inventory notes explicitly preserve distributed identities. Therefore the evidence does not support introducing or assuming a unified inquiry-identity ontology.

### Some surfaces are static registrations, not dynamic resolution

Question Surface Inventory registers known families and maps them to surfaces. It does not parse arbitrary prose into a subject. Bounded ask requires exact `ask --question-family <exact-question-family>` shape and rejects unknown families.

### Some reasoning stops when the identity is unsupported

Reference Selection returns unsupported-domain results outside `history`. Selection Path returns unknown selection logic for unrecognized targets. These are counterexamples to any claim that an organizing identity always guarantees reasoning.

### Evidence selection can happen before final answer composition but after broad surface audits

Reasoning Path builds broad upstream surfaces (`ownership_discrepancies`, `capability_needs`, `pressure_audit`, `privilege_discovery`, `operational_story`) before filtering their outputs by subject/domain. This means the invariant is not "all data collection waits for the identity." The stronger supported invariant is narrower: subject-specific evidence selection and reasoning depend on the identity.

### Operational Story is not inquiry-subject acquisition

Operational Story has a focus/primary pressure, but it is selected from operational audit outputs. It supports the answer-composition side of a dependency-center role, not a general inquiry-anchor recovery responsibility.

## Answers to central questions

### 1. Does implementation consistently exhibit an organizing inquiry identity before reasoning begins?

**Mostly yes for the reviewed inquiry-like surfaces, with scope limits.** Reasoning Path, Selection Path, Reference Selection, Inquiry Orientation, Source Navigation, and bounded ask all require an established identity before surface-specific reasoning or selection can proceed. The identity is not always supplied the same way: it may be an exact `question_family`, explicit `domain`/`subject`, explicit `target`, a selected note, a `query`, or a primary operational focus.

The implementation evidence does **not** support the stronger claim that a single shared identity object exists, or that all broad upstream audits wait for that identity.

### 2. Where is the strongest implementation evidence?

The strongest evidence is in three places:

1. **Bounded ask dispatch**: exact `question_family` validation and parameter enforcement occur before surface routing.
2. **Reasoning Path**: `domain` and `subject` are required inputs, and evidence/consumers/story impact are selected by those values before conclusion and lineage payloads are assembled.
3. **Selection Path / Reference Selection**: `target` and `domain` are validated or branched on before implemented reasoning; unsupported values produce explicit unknown/unsupported outputs rather than inferred reasoning.

### 3. Is the recurring invariant one of role rather than ontology?

**Yes.** The recurring invariant is role-shaped: an implementation value becomes the dependency head for subsequent evidence selection, reasoning, and answer composition. The values occupying the role are different concepts with different rules. Treating them as one ontology would exceed implementation evidence.

### 4. Which implementation concepts occupy this role?

Supported role occupants in the reviewed implementation are:

- `question_family` for bounded ask dispatch and question-surface presentation.
- `domain` + `subject` for Reasoning Path derivation explanation.
- `target` for Selection Path selection explanation.
- `domain` for Reference Selection.
- selected `InquiryNoteRecord` / `raw_note` token set for Inquiry Orientation.
- `query` for Source Navigation.
- primary pressure/focus for Operational Story answer composition.

### 5. Does implementation evidence support beginning a bounded investigation into this recurring dependency-center responsibility?

**Yes, with a narrow scope.** The implementation repeatedly requires an established identity before subject-specific evidence selection and reasoning. That recurrence is strong enough to justify a bounded investigation into the dependency-center role as a recoverable architectural invariant.

The next investigation should not recover ownership yet, rename vocabulary, implement parsing, or introduce a shared ontology. It should instead inventory where this role is compressed into dispatch, surface arguments, validators, branch functions, evidence filters, and answer-composition payloads.

## Supported conclusions

- The repository repeatedly uses an established value as an organizing center before surface-specific reasoning begins.
- The recurrence is primarily about **ordering and dependency role**, not about a common semantic identity.
- Multiple implementation concepts occupy the role: `question_family`, `domain`, `subject`, `target`, `query`, note identity/token set, and operational focus.
- Validation or bounded branching commonly precedes reasoning: exact family checks, required surface arg checks, supported-domain checks, recognized-target checks, non-empty note checks, and query normalization.
- Answer composition is downstream of selected evidence/lineage in the strongest reviewed surfaces.

## Unsupported conclusions

- Unsupported: Seed has a single `Inquiry Anchor` model or ontology.
- Unsupported: `subject` is the universal organizing identity.
- Unsupported: bounded ask performs semantic parsing of arbitrary operator questions.
- Unsupported: Inquiry Orientation discovers operator intent, concern, ownership, or recommended action.
- Unsupported: Reference Selection supports arbitrary domains.
- Unsupported: beginning a runtime implementation or ownership recovery is justified by this investigation alone.

## Confidence

**Medium-high** for the role-level recurrence across reviewed surfaces.

Confidence is high that Reasoning Path, Selection Path, Reference Selection, Inquiry Orientation, Source Navigation, and bounded ask exhibit identity-before-reasoning ordering. Confidence is lower for calling the role a distinct recoverable responsibility because current implementation keeps the role distributed across inventory rows, CLI dispatch, surface arguments, local filters, and answer-composition payloads.

## Recommended next action

Begin a bounded follow-up investigation into the recurring dependency-center role, using a neutral working label such as `inquiry dependency head` or continuing with `Inquiry Anchor` only as a temporary name. The follow-up should:

1. Inventory every surface where an identity value gates evidence selection or reasoning.
2. Separate identity acquisition, validation, evidence selection, reasoning, and answer composition in implementation evidence.
3. Preserve current vocabulary and explicit-input boundaries.
4. Look for additional counterexamples where reasoning proceeds without an organizing identity or where several identities remain co-equal.
5. Avoid ownership recovery, runtime changes, parser changes, grammar changes, ontology changes, and behavior changes.

## Acceptance answer

Yes, the repository repeatedly requires an organizing identity before subject-specific reasoning begins in the reviewed surfaces. The strongest evidence is not that the same identity exists everywhere, but that different implementation concepts repeatedly perform the same dependency-center role. The recurrence is therefore about architectural role and ordering, not about what the identity ontologically is. Implementation evidence justifies treating that role as a candidate recoverable architectural invariant for a future bounded investigation, but not as a basis for implementation changes or ownership recovery now.
