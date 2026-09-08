# Seed Decision and Context Grammar Topology Review 001

## 1. Bounded questions

This review asks whether Seed contains a genuine general decision responsibility, or whether lawful movement is produced through bounded selection, admission, sufficiency, warrant, authorization, composition, and stopping disciplines. It also asks whether Seed consumes general context, or instead consumes typed, bounded artifacts whose scope, provenance, authority, and uncertainty are explicit.

## 2. Governing orientation tested

Operator orientation tested, but not assumed as fact:

- Seed does not globally decide; Seed selects under constitutional constraints.
- Ambient model context is not the same as typed bounded Seed artifacts.
- LLMs are external grammar and have no internal constitutional standing inside Seed.

## 3. Methodology

I ran the required read-only searches, inspected implementation bodies and callers in the likely neighborhoods, sampled tests and CLI construction, and treated documentation strings and module docstrings as repository testimony rather than automatically authoritative fact. Classification was based on producer/artifact/consumer behavior, not on vocabulary alone.

## 4. Inspected implementation neighborhoods

- `seed_runtime/models.py`
- `seed_runtime/context.py`
- `seed_runtime/model_client.py`
- `seed_runtime/runtime.py`
- `seed_runtime/decisions.py`
- `seed_runtime/intent_classifier.py`
- `seed_runtime/evaluations.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/context_views.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/frontier_pressure_admission.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/decision_journal.py`
- `seed_runtime/state.py`
- `scripts/seed_local.py`
- relevant tests under `tests/`

## 5. Inspected documentation testimony

The strongest testimony is in code-level documentation:

- `seed_runtime/runtime.py` says Runtime records user input and refuses to route model-produced Decisions as Seed authority.
- `seed_runtime/context.py` describes compact context packets for model decisions.
- `seed_runtime/model_client.py` renders `DecisionInputPacket` into prompts and parses strict JSON model decisions.
- `seed_runtime/constitutional_view_selection.py` states Selection consumes deterministic question and capability projections, exact-compares them, preserves unsupported uncertainty, and emits immutable selection artifacts.
- `seed_runtime/context_views.py` says Context Views are deterministic read-only projections and do not call LLMs, append events, mutate State, execute runtime behavior, or persist a context store.
- `seed_runtime/tool_validation.py` explicitly separates operation selection from recommendation/provider choice.
- `seed_runtime/tool_execution_policy.py` explicitly separates registered operation validation from policy authorization.
- `seed_runtime/decision_journal.py` records decision audit records but does not own a mutable store.

## 6. Classification criteria

- **A. LLM-agent decision grammar**: broad material is given to a general chooser that produces the next runtime movement.
- **B. Seed-native bounded selection**: typed candidates are filtered or selected through explicit constraints.
- **C. Seed-native admission or sufficiency discipline**: evidence/testimony/reliance/movement is admitted or found sufficient without choosing the next action globally.
- **D. Local bounded adjudication**: an already-specified subject is allowed, blocked, validated, made eligible/ineligible, or requires approval.
- **E. LLM prompt context**: broad packet exists to inform an LLM/general chooser.
- **F. Typed bounded Seed artifact**: explicit producer, immutable scope/provenance/uncertainty/authority, specific consumer.
- **G. Descriptive or incidental vocabulary**: local naming without architectural ownership.
- **H. Unsupported ambiguity**: evidence does not safely establish the responsibility.

## 7. Occurrence inventory

| Occurrence | Classification | Evidence-backed rationale |
|---|---:|---|
| `DecisionKind` / `Decision` in `models.py` | A | Union of `answer`, `ask_question`, `call_tool`, `request_tool`, plans, patches, and `refuse`; this is heterogeneous next-step grammar. |
| `DecisionInputPacket` / `DecisionInputComposer` | E | Broad packet of input, goals, entities, facts, tools, needs, schema, evidence, retry prompt, and budget; consumed by prompt renderers and decision producers. |
| `render_decision_prompt`, `DecisionPromptModelClient`, `ParsedDecisionProducer`, `StrictJSONDecisionParser` | A/E | Turns packet into model instruction to choose exactly one decision and parses model-authored JSON. |
| `DecisionValidator` | D | Validates already-formed model-shaped Decisions; does not choose Seed movement. |
| `Runtime` decision-producer boundary | D / counter-testimony against A | Runtime is now an input boundary that refuses model Decisions as authority. |
| `StaticDecisionProducer` | A residue / G compatibility | Legacy inert test helper; calling `decide` raises unsupported authority error. |
| `IntentClassification`, `DecisionBuilder`, `IntentDecisionProducer` | A residue | Compact intent grammar is converted into the same general `Decision` union. Deterministic fallback is non-LLM counterevidence, but artifact remains model-shaped next-step grammar. |
| `DecisionEvaluator` | A test/evaluation harness | Evaluates DecisionProducer behavior against golden cases, not Seed-native movement. |
| `PolicyDecision` | D | Local policy adjudication for a selected operation: allow/block/require confirmation/approval. |
| `ToolExecutionPolicyResult` | D | Combines operation validation and policy adjudication; caller routes result. |
| `OperationSelectionResult` / `select_operation` | B/D | Resolves one already named registered operation; explicitly does not rank providers or recommendations. |
| `context_selection.py` ordering/budget helpers | B/E support | Selects and orders items for prompt/context budget, not constitutional movement. |
| `DecisionContextView` / `ContextFact` / `ContextIssue` / `ContextRequirement` / `ContextCapability` | F | Deterministic read-only projections from State/evidence/contradictions/confidence for specific consumers; no LLM/provider/mutation path. |
| `constitutional_view_selection.py` projections and `SelectedConstitutionalViews` | B/F | Deterministic exact-key selection from bounded question and capability projections; preserves Unknown/unsupported keys. |
| `constitutional_pipeline.py` | B/F | Typed bounded stages: bounded question, projection, capability projection, selection, composition, provenance explanation. |
| `reference_selection.py` | B/F | Read-only implementation-selected comparison reference with alternatives, limitations, authority boundary. |
| `selection_path_audit.py` | B/F | Diagnostic selection visibility with candidate sets, non-selected items, unknowns, lineage, evidence. |
| `frontier_pressure_admission.py` | C/F | Admission discipline for pressure artifacts, not global next-action choice. |
| `inquiry_artifacts.py` / `inquiry_orientation.py` | C/F | Bounded inquiry/orientation artifacts preserve scope, provenance, unknowns, and limits. |
| `DecisionJournal` / `DecisionRecord` | G/F | Audit/event vocabulary around historic decisions; records context hash and outcomes, not current authority. |
| Generic local `context` function parameters | G | Many are ordinary parameter names. Only architecturally meaningful contexts were classified above. |

## 8. Producer / artifact / consumer table

| Producer | Artifact | Consumer | Trigger | Owns | Explicitly refuses | Selects? | Creates authority? | Controls movement? | Provenance? | Unknown? | Read-only? | Ledger? | Mutates cluster/projected state? | Independent non-LLM producer? | Independent non-LLM consumer? |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `DecisionInputComposer.compose` | `DecisionInputPacket` | prompt clients, decision producers, evaluators | user input + projected State + registry | prompt bundle assembly | durable authority | no | no | only by later producer | partial via facts/evidence | no explicit Unknown channel | yes as object | no | no | yes | mostly no; deterministic tests/evaluators inspect it |
| LLM text + parser | `Decision` | legacy producers/evaluators/validators | model completion | next-step grammar | constitutional authority in Runtime | yes, heterogeneous action kind | no after excision | no after excision | reason only | no structured Unknown | data-only | no | no | no |
| `DecisionBuilder` | `Decision` | `IntentDecisionProducer` callers/evaluators | intent classification | translate compact intent into Decision | independent Seed authority | yes, among union kinds | no | no after Runtime excision | reason only | no | data-only | no | no | yes, but grammar remains general |
| `Runtime.handle_user_message` | `RuntimeResponse(kind=unsupported)` + ledger event | caller and event ledger | user message | input record + explicit stop | model-produced Decision authority | no | no | yes, stops movement | event causation | reason preserved | no, writes ledger | yes | no cluster mutation | yes | yes |
| `DecisionValidator` | `ValidationResult` | tests/legacy callers | existing `Decision` | shape validation | movement/authority | no | no | no | errors only | no | yes | no | no | yes | yes |
| `PolicyGate` via `ToolExecutionPolicyService` | `PolicyDecision` | tool execution policy callers | selected valid operation | policy allow/block/approval adjudication | execution and event writes | no | applies existing policy authority | gates execution eligibility | reason/risk | no Unknown outcome | yes | no | no | yes | yes |
| `ToolValidationService.select_operation` | `OperationSelectionResult` | validation/policy services | operation name | operation lookup | provider ranking/recommendation | bounded single-name resolution | no | only validation path | errors | absence as rejected | yes | no | no | yes | yes |
| `build_decision_context_view` | `DecisionContextView` | CLI/view renderers/tests | projected State | read-only knowledge view | runtime/LLM/policy/execution/mutation | selects facts through confidence filters | no | no | State-derived | unsupported counts, contradictions | yes | no | no | yes | yes |
| `produce_bounded_constitutional_question` + projectors | `ConstitutionalQuestionProjection` | view selection | explicit bounded inquiry fields | projection of selection keys | semantic inference/discovery | no | no | no | bounded id/provenance upstream | uncertainty and unknowns | yes | no | no | yes | yes |
| `project_constitutional_capabilities` | capability projections | view selection | contracts/registrations/views | available capability keys | authoring knowledge/repair | no | no | no | registration name | Unknown compatibility | yes | no | no | yes | yes |
| `select_constitutional_views` | `SelectedConstitutionalViews` | composition request builder/pipeline/diagnostics | question + capability projections | exact-key bounded selection | semantic reasoning/raw question consumption/mutation | yes | no | controls composition inputs only | bounded question id | unsupported keys/empty selection | yes | no | no | yes | yes |
| `build_constitutional_view_composition` | composition artifact | pipeline/renderers | selected view names/request | bounded composition | mutation/ledger/provider calls | no | no | no | contributing views | preserved unknowns/refusals | yes | no | no | yes | yes |
| `build_reference_selection` | `ReferenceSelection` | CLI/diagnostic renderers | domain | comparison reference choice | baseline authority/mutation | yes | no | no | alternatives/limitations | unsupported domain unknown | yes | no | no | yes | yes |
| admission builders | admission artifacts | diagnostics/pipelines | typed inputs | admissibility/sufficiency | next-action choice | no | no | may block reliance | provenance | Unknown/unsupported preserved | yes | no | no | yes | yes |
| `DecisionJournal.append_record` | `decision.recorded` event | ledger/read-only traces | completed/historic run | audit record | mutable store/authority | no | no | no | context hash/run id | outcome errors | no | yes | projected by replay only | yes | yes |

## 9. Decision-oriented topology

Current implemented paths involving general `Decision` or decision producers:

```text
DecisionInputComposer
  -> DecisionInputPacket
  -> render_decision_prompt / IntentPromptModelClient
  -> external model text or compact intent
  -> StrictJSONDecisionParser / StrictJSONIntentParser
  -> Decision / IntentClassification
  -> DecisionBuilder optionally builds Decision
  -> DecisionValidator / evaluator / legacy tests
```

Runtime path now diverges:

```text
Runtime.handle_user_message
  -> append input.user_message
  -> append runtime.decision_authority_unsupported
  -> RuntimeResponse(kind="unsupported")
```

No inspected current Runtime path routes `Decision.kind` to answer, tool execution, tool request, patch, plan, or refusal authority.

## 10. Selection-oriented topology

Recurring Seed-native selection paths:

```text
BoundedConstitutionalQuestion
  -> ConstitutionalQuestionProjection(selection_keys, uncertainty, unknowns)
  + ConstitutionalCapabilityProjection(capability_keys, compatibility_answer)
  -> select_constitutional_views(exact key comparison)
  -> SelectedConstitutionalViews(selected names, unsupported uncertainty, read-only boundaries)
  -> ConstitutionalViewCompositionRequest
  -> composition artifact(preserved unknowns/refusals)
```

```text
registered operation name
  -> ToolValidationService.select_operation
  -> OperationSelectionResult(selected operation | rejected absence)
  -> schema/status validation
  -> ToolExecutionPolicyService policy adjudication
```

```text
repository/domain inputs
  -> ReferenceSelection(candidate/alternative reference testimony)
  -> selected reference + limitations + authority boundary
```

```text
state/story/frontier inputs
  -> selection_path_audit
  -> selected target/category/focus + candidates + non-selected + evidence + unknowns
```

These selectors generally consume already-produced candidates or explicit keys. They do not discover broad possibilities or invent unbounded next actions.

## 11. Context-oriented topology

Broad prompt context topology:

```text
State + Event + ToolRegistry
  -> DecisionInputComposer
  -> DecisionInputPacket(current input, goals, entities, facts, tools, tool needs, evidence, schema, retry/budget)
  -> render_decision_prompt / intent prompt
  -> model or model-shaped producer
```

Read-only view context topology:

```text
State + EvidenceGraph + Contradictions + Confidence
  -> build_decision_context_view
  -> DecisionContextView(facts/issues/requirements/capabilities/summary)
  -> CLI/view renderers/tests
```

Audit hash context topology:

```text
provider-visible context-like object
  -> context_hash_payload/context_hash
  -> DecisionRecord.context_hash
  -> decision.recorded event
```

## 12. Typed-artifact topology

Representative typed artifacts replacing ambient context:

```text
operator inquiry fields
  -> BoundedConstitutionalQuestion(scope, provenance, unknowns, uncertainty, read-only flags)
  -> ConstitutionalQuestionProjection(selection keys only)
```

```text
read-model contracts + immutable constitutional views
  -> ConstitutionalCapabilityProjection(registered view, exact capability keys, compatibility)
  -> SelectedConstitutionalViews
```

```text
SelectedConstitutionalViews
  -> ConstitutionalViewCompositionRequest
  -> ConstitutionalViewCompositionArtifact(contributors, preserved unknowns/refusals)
```

```text
State knowledge layers
  -> DecisionContextView(typed facts/issues/requirements/capabilities and counts)
```

```text
reference-selection domain
  -> ReferenceSelection(selected reference, alternatives, authority boundary, limitations)
```

## 13. Vocabulary collision topology

```text
Decision
├── model-authored general next-step choice: Decision, DecisionKind, ParsedDecisionProducer
├── compact-intent-to-general-choice compatibility: IntentDecisionProducer, DecisionBuilder
├── local policy adjudication: PolicyDecision
├── audit record vocabulary: DecisionRecord, DecisionJournal
└── incidental validation/evaluation vocabulary: DecisionValidator, DecisionEvaluator
```

```text
Context
├── LLM prompt packet: DecisionInputPacket, DecisionInputComposer, model_client context parameter
├── deterministic read-only knowledge view: DecisionContextView and ContextFact/Issue/Requirement/Capability
├── prompt-budget/order support: context_selection.py and ContextBudget
├── audit hash of provider-visible material: decision_journal.context_hash_payload
├── repository/history prose in diagnostics: history brief/snapshot audit/reference selection
└── incidental function argument names
```

```text
Selection
├── constitutional exact-key view selection
├── operation-name registry resolution
├── reference selection for comparison baselines
├── selection-path diagnostics preserving candidates/non-selected/unknowns
└── incidental list filtering in tests and diagnostics
```

## 14. Independent testimony for `Decision`

Evidence for general Decision as LLM-agent grammar:

- `DecisionKind` is a heterogeneous union of answer, question, tool call, tool request, action plan, handoff plan, state patch, and refusal.
- `render_decision_prompt` tells a model to choose exactly one decision for the runtime.
- `StrictJSONDecisionParser` parses raw model text into `Decision`.
- `ParsedDecisionProducer` is an adapter around a text-generating model client.
- `DecisionInputComposer` exists to create input packets for model decisions.

Evidence against current Seed-native authority:

- Runtime explicitly ignores provided decision producers, stores `decision_producer = None`, and returns unsupported for free-text input.
- `StaticDecisionProducer.decide` raises that model-shaped Decisions are not Seed authority.

## 15. Independent testimony for `Context`

Evidence for prompt context:

- `DecisionInputPacket` contains broad current input, active goal, entities, facts, tools, open tool needs, schema, evidence, retry prompt, and budget trace.
- Prompt rendering omits some runtime details but still creates broad material for a model chooser.

Evidence for bounded Seed-native context:

- `DecisionContextView` is deterministic, read-only, State/evidence/confidence-derived, and has typed sub-artifacts.
- Constitutional projections and pipeline artifacts carry bounded IDs, exact keys, uncertainty/unknowns, read-only flags, ledger flags, and mutation flags.

## 16. Independent testimony for `Selection`

Selection has multiple implementation-backed bounded meanings:

- Constitutional view selection consumes explicit selection keys and capability keys, performs exact comparison, preserves unsupported keys, and emits `SelectedConstitutionalViews`.
- Operation selection resolves one already named registered operation and rejects absence.
- Reference selection returns a selected comparison reference with alternatives and limitations.
- Selection path audit exposes candidate set, non-selected alternatives, evidence, factors, lineage, and unknowns.

## 17. Strongest counterevidence

- `DecisionBuilder` and `IntentDecisionProducer` can create general `Decision` artifacts without an LLM if deterministic fallback or a non-LLM classifier is used. This is real non-LLM production of the artifact, but it produces the same heterogeneous next-step union and Runtime no longer grants it authority.
- `DecisionContextView` uses `Decision` and `Context` vocabulary but is a deterministic read-only typed projection. Therefore a blanket claim that all Context vocabulary is LLM prompt grammar would be false.
- `PolicyDecision` is legitimate local vocabulary; it cannot be deleted merely because general `Decision` is unsupported.
- Some selection support is used to prepare prompt packets (`context_selection.py`), so not every selector is constitutional movement grammar.

## 18. Preserved Unknowns

- I did not prove every historic or compatibility test no longer references routed Decisions; tests contain legacy scaffolding.
- I did not classify every local variable named `context`; only architecturally significant types/services/public surfaces were reviewed.
- Some documentation may describe obsolete architecture and remains testimony, not conclusive current behavior.
- The long-term intended replacement for free-text runtime movement is not fully established by current implementation.

## 19. Supported conclusions

1. Seed does not currently have an implementation-backed general decision owner in Runtime.
2. Non-LLM code can create the general `Decision` artifact through intent fallback/builder paths, but this does not establish constitutional authority.
3. No inspected current non-LLM runtime consumer requires `Decision` for lawful movement.
4. General `Decision` is a union of unrelated movement forms.
5. Its shape encodes LLM-agent grammar.
6. Legitimate local `Decision` terms include `PolicyDecision`, `DecisionRecord`, and validation/evaluation compatibility vocabulary.
7. Those local artifacts would remain valid if the general `Decision` artifact disappeared, provided references were renamed or decoupled carefully.
8. `PolicyDecision` is better characterized as bounded policy adjudication.
9. Seed explicitly uses Selection in constitutional view selection, operation selection, reference selection, and selection-path diagnostics.
10. Selectors consume explicit names, keys, projections, registered capabilities, candidate sets, and diagnostic inputs.
11. Selectors generally do not invent candidates; they select or preserve absence from already-produced inputs.
12. Selectors apply existing authority constraints; they do not create authority.
13. Selection preserves absence, unsupported outcomes, refusal, and Unknown in multiple places.
14. Selection is the dominant implemented lawful movement grammar for constitutional/read-only paths, but not every runtime capability has been rebuilt on it.
15. `DecisionInputPacket` contains a broad prompt bundle.
16. `DecisionInputComposer` produces it.
17. Model clients, decision producers, prompt renderers, evaluators, and tests consume it.
18. It has no clear lawful consumer other than LLM/model-oriented chooser and compatibility/evaluation code.
19. Its content is an ambient prompt bundle, not a single explicit constitutional artifact.
20. Genuinely bounded context artifacts include `DecisionContextView`, constitutional projections, bounded inquiry artifacts, reference selections, and diagnostic selection artifacts.
21. Prompt/classification/retry contexts include `DecisionInputPacket`, intent prompt context, and model-client context parameters.
22. Some typed Seed artifacts are hidden behind generic `Context` vocabulary, especially `DecisionContextView`.
23. A global `Decision -> Selection` rename would be inaccurate.
24. A global `Context -> Artifact` rename would be inaccurate.
25. General `Decision`, `DecisionInputPacket`, prompt decision producer names, and intent-to-decision compatibility names are candidates for removal or boundary-specific replacement, not blind rename.
26. `PolicyDecision`, `DecisionContextView` until renamed carefully, `ReferenceSelection`, `SelectedConstitutionalViews`, `OperationSelectionResult`, and admission/sufficiency terms should remain because they represent distinct local responsibilities.

## 20. Unsupported conclusions

- It is not supported that every use of `context` is prompt grammar.
- It is not supported that every use of `decision` should be excised.
- It is not supported that Selection alone currently implements all future runtime movement for free-text input.
- It is not supported that deterministic intent fallback makes the general `Decision` artifact Seed-native; it only proves a non-LLM producer exists.

## 21. Exact recommended next slice

The smallest next implementation slice should target **inert runtime compatibility and intent-to-decision production**, specifically documenting or isolating the remaining compatibility producers that can still create general `Decision` objects without Runtime authority. This is smaller and safer than a global rename. It should prove that `IntentDecisionProducer`/`DecisionBuilder` are compatibility/model grammar boundaries or replace their output with a more explicit unsupported/intent artifact before touching `PolicyDecision` or typed context views.

## 22. Explicit implementation-warrant decision

**B. General Decision is unsupported, but some Context responsibilities are independently Seed-native.**

Rationale: general `Decision` no longer has Runtime authority and is model-shaped grammar, while `DecisionContextView` and constitutional/inquiry/provenance artifacts demonstrate independently bounded, typed, read-only Context responsibilities.

## 23. Files changed

- Added `seed_decision_context_grammar_topology_review_001.md`.
- No production files changed.
- No test files changed.

## 24. Probes or tests executed

Read-only probes executed:

```bash
rg -n "class .*Decision|DecisionKind|DecisionProducer|DecisionInput|DecisionContext|PolicyDecision|OperationSelectionResult" seed_runtime scripts tests
rg -n "\bselect|\bselection|\badmit|\badmission|\bsufficien|\bwarrant|\bauthoriz|\brefus|\bstop" seed_runtime tests
rg -n "\bcontext\b|Context" seed_runtime scripts tests
rg -n "Decision|decision context|context packet|Selection|PolicyDecision|DecisionInputPacket|DecisionProducer" *.md docs seed_runtime
sed -n focused inspections of the implementation neighborhoods listed above
```

No tests were required to validate behavior because this was a review-only artifact. Diff guardrail commands were run before commit as requested.

## 25. Confidence statement

Confidence is high for the current Runtime and prompt/Decision boundary classification, high for the bounded constitutional Selection topology, and medium-high for repository-wide vocabulary collision coverage. Confidence is intentionally lower for exhaustive historical/compatibility test implications because the task explicitly avoided broad implementation changes and a blind classification of every local `context` variable.
