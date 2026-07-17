# Constitutional Bounded Question Road Standing Audit 001

## Question audited

This audit asks what constitutional standing the existing bounded constitutional question road actually has:

```text
produce_bounded_constitutional_question()
→ project_constitutional_question()
→ select_constitutional_views()
→ selected_constitutional_views_to_composition_request()
→ build_constitutional_view_composition()
```

The audit treats existing reports as testimony and evidence locators, not as authority. Repository implementation, callers, tests, and history control.

## Executive finding

The road has implementation standing as a deterministic, read-only, explicit-field construction and registered-view composition path. It does not have demonstrated standing as a live bounded-goal-relative constitutional question origination road.

The supported road begins only after a caller already supplies a `BoundedConstitutionalQuestion` or explicit fields from which one is constructed. The constructor preserves those values, assigns deterministic identity, and refuses promotion to fact, durable knowledge, constitutional authority, repository truth, view selection, event-ledger write, or cluster mutation. Projection then carries only exact caller-declared selection keys. Selection matches those keys against locally projected registered-view capability keys. The adapter converts selected registered view names into a composition request. Composition validates registered names, builds existing registered constitutional read-model views, correlates existing evidence, and preserves Unknowns/refusals.

That proves artifact validity and downstream consumer validity for an explicit supplied object. It does not prove constructor validity as question origination, input authority, bounded-goal identity, current position, completed-work lineage, unresolved pressure recovery, evidence territory recovery, remaining-authority recovery, lawful stop-condition recovery, complete circulation realization, or constitutional standing of the question's origin.

## History and introduction evidence

`produce_bounded_constitutional_question()` was introduced by commit `15a0417` (`Implement bounded constitutional question producer (#1603)`), which added the implementation report, runtime module, and tests. The implementation itself states that the module preserves explicitly supplied `BoundedConstitutionalQuestion` fields and explicit caller inputs as evidence/testimony, while refusing projection, capability discovery, authority selection, ledger writes, and cluster mutation.

Subsequent history narrows rather than expands origination standing:

- `fc5e78b` added constitutional view selection before the bounded-question producer road was complete.
- `85d80bf`, `eb9806a`, `1aec61b`, and `6c33272` added capability projection, pipeline invocation, provenance explanation, and CLI exposure.
- `8bba96c` added a bounded-question formulation adapter, but later repository evidence shows operator-ingress question origination was removed.
- `7bd2325` deleted raw constitutional pipeline question origination. Current code requires `ConstitutionalPipelineRequest` to consume one already-established `BoundedConstitutionalQuestion` and current CLI error paths reject raw pipeline question fields.
- `7bd2325` and related tests confirm the public pipeline no longer exposes a raw constructor path as pipeline origination.
- `faa0fb9` recovered selection-to-composition handoff behavior, not live question origination.

Historical standing is therefore: the producer was introduced to construct and preserve an explicit bounded-question artifact for a deterministic read-only path. Later repository history removed or narrowed raw/operator origination surfaces instead of proving them constitutionally valid.

## Callers and surface classification

### Production/runtime paths

- `ConstitutionalPipelineRequest` consumes an already-established `BoundedConstitutionalQuestion`; it no longer accepts raw operator-inquiry, bounded-question, or scope fields. This is a production API consumer of a supplied artifact, not a producer of bounded-goal-relative questions.
- `invoke_constitutional_pipeline()` invokes projection, capability projection, selection, adapter, and composition in order over the supplied bounded question. It is an ordered handoff runner, not an originator.
- `constitutional_pipeline_diagnostic.py` wraps the same pipeline request/result for diagnostic reporting. It depends on a request already containing the bounded question.
- `scripts/seed_local.py` imports the pipeline but current CLI paths for `--constitutional-pipeline` and `--constitutional-pipeline-diagnostic` reject raw question fields and instruct API use with an already-established `BoundedConstitutionalQuestion`. The CLI surface is therefore not a live raw question origination route.

### Tests

Tests directly construct bounded questions for deterministic behavior, projection, selection, pipeline, examination, and policy scenarios. Those test calls are construction scaffolding and implementation witnesses. They prove preservation, identity stability, exact key projection, read-only flags, non-mutation, unsupported-key uncertainty, and composition success/failure. They do not prove lawful origination from a bounded goal.

### Demonstrations and reports

Reports and demonstrations describe or exercise the road, but they are not authority. They can locate evidence and testify to intended boundaries. Where they claim complete circulation or constitutional path realization, the current audit treats those claims as unsupported unless implementation establishes the required high-resolution origin inputs.

### Adapters/scaffolding

`selected_constitutional_views_to_composition_request()` is a narrow adapter. It has valid standing as handoff wiring from a selected-views artifact to a composition request. It is not an independent constitutional judgment and does not establish origination.

## Field establishment analysis

### Fields Seed establishes

Seed establishes only implementation-local properties that it computes or fixes:

- `bounded_question_id` when absent, by stable hash of the explicit supplied payload.
- tuple normalization of `uncertainty`, `unknowns`, and `caller_supplied_fields`.
- default `testimony_status` saying operator testimony is evidence, not established fact.
- default read-only boundary text.
- `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False` for the bounded-question artifact.
- `ConstitutionalQuestionProjection.selection_keys` by reading exact caller-supplied fields named `selection_key` or `selection_key:<key>`.
- projection uncertainty by forwarding supplied uncertainty and prefixing supplied Unknowns.
- capability keys from registered implementation-backed read-model views: process, governance, fidelity.
- selected registered view names by exact set intersection between question keys and capability keys.
- unsupported selection-key uncertainty and no-match uncertainty.
- composition request fields from selected view names plus purpose/output-format defaults.
- composition artifact contents from registered builders, their JSON payloads, existing evidence, Unknowns, refusals, and compatibility answers.

### Fields the caller merely asserts

The caller asserts the semantically important input fields:

- `operator_inquiry`.
- `inquiry_provenance`.
- `bounded_question`.
- `constitutional_intent`.
- `scope_status`.
- supplied `uncertainty`.
- supplied `unknowns`.
- supplied `caller_supplied_fields`, including selection-key fields.
- supplied `bounded_question_id`, when provided.
- any claim that the bounded question comes from a bounded goal, current constitutional position, completed work, unresolved pressure, available evidence, preserved Unknowns, remaining authority, or lawful stop conditions.

Seed preserves those assertions but does not validate them as constitutional origin.

## Validation standing

### Validations that establish local standing

- Dataclass shape and immutability establish artifact stability, not origin.
- Deterministic ID computation establishes repeatable identity for the supplied payload, not lawful question source.
- Exact selection-key extraction establishes no semantic inference from question text.
- Exact capability-key projection establishes registered-view availability from implementation-backed builders.
- Exact selection matching establishes deterministic local admission into registered view composition.
- Composition validates requested names against registered constitutional read-model contracts and the local builder map.
- Read-only/non-ledger/non-cluster flags and tests establish operational non-mutation boundaries.

### Validations that only preserve supplied shape

- Required constructor arguments ensure a caller supplies strings; they do not prove that those strings are true, authorized, goal-relative, or constitutionally originated.
- `scope_status="bounded"` in tests or examples is caller testimony; the constructor does not recover or verify the actual boundary.
- `constitutional_intent` is accepted as text; no implementation establishes intent from repository authority.
- `inquiry_provenance` is accepted as text; no implementation validates the provenance chain.
- `unknowns` and `uncertainty` are carried, not audited for completeness.
- `caller_supplied_fields` are sorted and stringified, not authorized.

## `selection_keys` standing

`selection_keys` are caller-authored routing instructions, not recovered evidence demand.

The projection function extracts keys only from `caller_supplied_fields` whose field name is `selection_key` or starts with `selection_key:`. It does not read the bounded question text for evidence needs, recover pressure, inspect current work, derive constitutional method, discover territory, or infer evidence demand. Tests prove that without explicit selection-key fields, projection emits an empty key tuple even when natural-language strings might suggest process or compatibility. Unsupported keys become preserved uncertainty.

Therefore, `selection_keys` have standing as exact caller-declared local composition routing keys. They do not have standing as recovered evidence demand from a bounded-goal state.

## Artifact type: question, composition request, or mixed object

`BoundedConstitutionalQuestion` is named and shaped as a constitutional question artifact, but its supported standing is narrower: it is an immutable, provenance-preserving explicit testimony artifact with a deterministic identity and read-only boundary declarations. It is not proven to be a constitutionally originated question.

`ConstitutionalQuestionProjection` is a selection input derived from the bounded-question artifact's caller-supplied fields. It is not the question itself and not a recovered inquiry representation.

`SelectedConstitutionalViews` is an admitted local movement artifact for registered constitutional views. It is not a question and not a composition result.

`ConstitutionalViewCompositionRequest` is a composition request. It owns explicit registered-view selection, purpose, output format, and optional upstream selection limits. It is not a question-origin artifact.

`ConstitutionalViewCompositionArtifact` is a bounded explanation composed from requested registered views. It is not question origination.

The end-to-end result is mixed only in the sense that the pipeline result bundles all stage artifacts. The stages remain separable. Bundling does not convert caller-supplied testimony into originated constitutional standing.

## Projection and selection consumption standing

Projection consumes only artifact shape and exact caller-supplied selection fields. It does not consume established question standing because no implementation proves the bounded question's origin.

Selection consumes only `ConstitutionalQuestionProjection` and capability projections. It does not consume raw question text, operator testimony, completed work, unresolved pressure, evidence territory, authority, or stop conditions. Its judgment is local exact-key admission into registered read-model view names. It is independently useful downstream only when the selection keys are already lawful and meaningful for the caller's purpose.

## Missing high-resolution inputs

The road lacks implementation-backed recovery or validation of:

- bounded-goal identity;
- current constitutional position;
- completed work;
- unresolved pressure;
- available evidence territory;
- preserved Unknowns as a complete set rather than caller-supplied entries;
- remaining authority;
- negative authority and forbidden moves;
- lawful stop conditions;
- relation between earlier operator testimony and present bounded-goal ancestry;
- proof that the immediate source is a live bounded goal rather than a direct caller assertion;
- proof that the bounded question is the right next constitutional pressure after extended work;
- proof that `selection_keys` correspond to evidence demand instead of routing preference;
- proof that an empty selection means lawful inactivity rather than missing origination data.

## Live goal-relative producer finding

No live goal-relative producer for the audited road was found in current implementation. Current production pipeline code requires a preexisting `BoundedConstitutionalQuestion`. The CLI rejects raw constitutional pipeline fields. Tests and helpers manufacture bounded questions directly for controlled assertions. Reports mention possible or desired formulation paths, but current repository implementation does not establish a producer that consumes bounded-goal state plus current position, completed work, unresolved pressure, evidence, preserved Unknowns, authority, and stop conditions to originate the question.

## Classification by element

| Element | Classification | Supported standing | Unsupported assumption |
|---|---|---|---|
| `produce_bounded_constitutional_question()` | implementation witness only; construction/test scaffolding when called directly | deterministic explicit-field artifact constructor/preserver; stable ID; read-only/no-ledger/no-cluster declarations | lawful constitutional question origination; bounded-goal-relative source; validation of caller semantics |
| `BoundedConstitutionalQuestion` artifact | constitutionally established only as preserved testimony artifact; not established as originated question | immutable shape carrying explicit fields, uncertainty, Unknowns, caller fields, testimony boundary, and non-mutation flags | that the question is constitutionally valid because constructed |
| `project_constitutional_question()` | unsupported projection from local machinery as to origin; implementation witness for exact key projection | carries ID, exact caller-declared selection keys, uncertainty/Unknowns; refuses semantic inference | that projection consumes established question standing or recovered evidence demand |
| `ConstitutionalQuestionProjection` | implementation witness only | local selection input with exact keys and uncertainty | full possible-inquiry translation |
| `project_constitutional_capabilities()` | constitutionally established as implementation-backed capability projection for registered views | projects capability keys from registered read-model builders | general capability discovery or authority recovery |
| `select_constitutional_views()` | independently valid downstream consumer | deterministic exact-key matching to registered view names; preserves unsupported uncertainty; read-only | semantic inquiry admission; evidence demand recovery; method selection beyond registered views |
| `SelectedConstitutionalViews` | independently valid downstream handoff artifact | selected registered view names plus uncertainty and non-mutation boundaries | proof selected views answer the bounded constitutional question |
| `selected_constitutional_views_to_composition_request()` | independently valid downstream adapter | converts selected names and selection limits into composition request fields | independent constitutional judgment or examination eligibility beyond wiring |
| `ConstitutionalViewCompositionRequest` | independently valid downstream request | explicit registered-view request, purpose, format, optional bounded ID and uncertainty | question standing or origin |
| `build_constitutional_view_composition()` | independently valid downstream consumer | validates registered names; builds registered views; correlates existing evidence; preserves Unknowns/refusals; read-only | source-independent truth formation; resolution of unsupported origin |
| `ConstitutionalViewCompositionArtifact` | independently valid bounded explanation artifact | composed registered read-model evidence and preserved uncertainty/refusals | complete constitutional circulation realization |
| `invoke_constitutional_pipeline()` | implementation witness only for ordered handoff; independently useful runner after lawful input exists | deterministic stage invocation over supplied bounded question | origination, current-position recovery, or authority validation |
| Existing tests | construction/test scaffolding and implementation witnesses | preservation, deterministic construction, exact projection, selection, read-only behavior, composition | lawful constitutional origination |
| Existing reports | testimony/evidence locators | locate history and intended boundaries | authority for standing |

## Distinctions required by this audit

- Artifact validity is present for the explicit constructed dataclass object.
- Constructor validity is present only as deterministic explicit-field preservation.
- Input authority is not established beyond caller assertion.
- Question origination is not established.
- Downstream consumer validity survives for registered-view selection, adapter wiring, and composition.
- Complete circulation realization is not established because the origin and high-resolution bounded-goal inputs are missing.

## Surviving components

The following components remain useful without unsupported origin claims:

1. The explicit bounded-question constructor can preserve supplied testimony and boundaries for inspection.
2. Question projection can expose exact caller-declared selection keys without semantic inference.
3. Capability projection can report registered view capability keys from implementation-backed read models.
4. Selection can perform deterministic exact-key routing to registered views and preserve unsupported uncertainty.
5. The adapter can pass selected registered views into composition without broadening authority.
6. Composition can build bounded explanations from explicitly requested registered constitutional views while preserving Unknowns/refusals and non-mutation boundaries.
7. Pipeline invocation can run the above stages for an already lawful `BoundedConstitutionalQuestion` supplied by some other established producer.

## Supported standing of the road

The supported standing is:

> A read-only, deterministic, implementation-local road that takes an explicitly supplied bounded-question artifact or explicit question fields, preserves them as testimony, projects only exact caller-declared selection keys, routes those keys to registered constitutional read-model views by exact matching, and composes explicitly selected registered views into a bounded explanation without mutation.

The road is not:

- a bridge from bounded-goal state to constitutional question;
- a live current-position question originator;
- an evidence-demand recoverer;
- an authority validator;
- a lawful-stop-condition validator;
- a complete constitutional circulation realization;
- proof that operator ancestry remains the constitutional source after extended bounded-goal work.

## Exact stopping boundary

Stop at the boundary where a caller asks this road to treat a supplied `BoundedConstitutionalQuestion`, `selection_keys`, or pipeline request as constitutionally originated. The implementation may preserve and route the artifact, but it must not claim origin, bounded-goal standing, recovered pressure, recovered evidence demand, remaining authority, or lawful stop completeness unless a separate implementation-backed live goal-relative producer establishes those facts.

Downstream use may continue only as explicit registered-view consumption over supplied inputs, with unsupported origin preserved as Unknown rather than silently converted into constitutional standing.

Bounded constitutional question road standing audit 001 complete.
