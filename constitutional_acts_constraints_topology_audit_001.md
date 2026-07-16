# Constitutional Acts and Constraints Topology Audit 001

## Survey boundary

Exact checkout surveyed before repository examination:

```text
git rev-parse HEAD
8772428fd8b8b788fe3104e07f4ab54be91f37b5

git status --short
<no output>
```

This audit is bounded to that checkout. It does not treat existing reports as authority except as locators. The conclusions below rely on production producers, production callers, function signatures, field provenance, validation, consumer assumptions, alternate paths, boundary flags, event creation, public construction surfaces, and unproven gaps.

## Smallest repository-supported topology

The smallest supported topology is not one universal constitutional pipeline. It is a set of typed roads and read-only representation surfaces:

```text
operator testimony / explicit caller fields
  -> bounded constitutional question artifact
  -> question projection
  -> deterministic view-name selection
  -> explicit composition request
  -> read-only constitutional view composition
```

This road is supported only where `invoke_constitutional_pipeline()` is called with a pre-established `BoundedConstitutionalQuestion`.

A separate event road exists:

```text
runtime input or observation ingestion
  -> append-only event ledger
  -> state projection / downstream read models
```

A separate observation road exists:

```text
Observation
  -> Evidence
  -> optional Fact
  -> event ledger batch
```

A separate grammar road exists:

```text
attributed operator expression
  -> recovered grammar applicability validation
  -> interpretation projection
  -> optional future authority/scope binding handoff
```

These roads can touch similar vocabulary but are not proven to be one mandatory constitutional sequence. `[UNPROVEN]` Universal order among translation, interpretation, binding, establishment, evaluation, selection, examination, realization, recording, projection, composition, and communication.

## Inventory of observed constitutional acts

| Candidate act | Observed structure | Classification | Consumes | Produces | Who consumes it | Checks | Preserves | Caller-controlled inputs | Movement or representation |
|---|---|---|---|---|---|---|---|---|---|
| Translation | `attribute_operator_expression()` normalizes exact operator text and assigns stable identity. | testimony / artifact constructor | exact text, representation, source channel, workspace/session/operator refs, provenance/scope/unknowns | `AttributedOperatorExpression` | `interpret_operator_expression()` | confidence-independent shape such as exact text normalization; no authority | exact text, normalized text, source channel, provenance, scope context, unknowns; read-only flags | text, channel, workspace/session/operator refs, provenance | representation only |
| Interpretation | `interpret_operator_expression()` validates grammar recovery/applicability references and parses bounded forms. | constitutional act / validation act | attributed expression, recovery projection, recovered grammar, applicability projection, mechanism/contract refs | `OperatorExpressionInterpretationProjection`; optional `FutureOperatorAuthorityScopeBindingHandoff` | possible future authority/scope binding; format/json surfaces | recovered grammar belongs to recovery projection; applicability references recovery and grammar; mechanism matches; applicability state | authority-bearing expressions as language only; operator constraints; unresolved references; unknowns/conflicts; read-only flags | mechanism refs, lexical/domain/support/provenance/unknown/conflict refs | representation; no execution |
| Binding | `closed_choice_selection_binding` binds captured token to exact presented choice set; interpretation can emit a future authority/scope binding handoff but does not bind authority. | constitutional act where closed choice token is bound; optional handoff elsewhere | presented closed choice set and selected token capture | `ClosedChoiceSelectionBinding` | downstream caller-specific consumers, not universal pipeline | choice set ref, option refs, unique tokens, supported token | local option meaning only; not authority/execution | presented set, capture token, reason | representation only |
| Establishment | `produce_bounded_constitutional_question()` establishes one bounded question only from explicit caller-supplied fields. | constitutional act / testimony-preserving artifact producer | operator inquiry, provenance, bounded question, constitutional intent, scope status, uncertainty, unknowns, caller fields | `BoundedConstitutionalQuestion` | `invoke_constitutional_pipeline()`, `project_constitutional_question()` | stable identity over supplied payload; tuple conversion | operator testimony as evidence, not fact; no truth/capability/view authority | all semantic fields and selection keys | representation; no mutation |
| Evaluation | `select_constitutional_views()` evaluates exact projected question keys against exact capability keys; observation ingestion evaluates whether fact promotion is suppressed. | constitutional act / judgment where present | projections or observation metadata | selected views, uncertainty, compatibility answer; or no Fact | composition adapter; event ledger | exact key intersection; unsupported-key accounting; suppression predicate | uncertainty, boundary flags | capability projections, question projection, metadata | representation except ingestion records events |
| Selection | `select_constitutional_views()` and `selected_constitutional_views_to_composition_request()`. | selection surface / constitutional act | question projection and capability projections | selected registered view names; composition request | `build_constitutional_view_composition()` | read-only/non-mutation flags; exact keys | unsupported keys; no raw question | projections and output format/purpose | representation only |
| Examination | Examination modules exist as production surfaces (for example candidate/examination policy/probe selection families), but no single universal topology was proven in this audit. | unproven / conditional branch | [UNPROVEN] varies by module | [UNPROVEN] varies by module | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] |
| Realization | Operational realization modules exist, but this audit found no universal required link from constitutional view selection or interpretation to realization. | unproven / conditional branch | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] | [UNPROVEN] |
| Recording | `EventLedger.append()` / `append_many()` and `ObservationIngestor.ingest_many()` record runtime events. | recording surface / constitutional act for preserved history | kind/workspace/payload/actor/session/causation/correlation or pre-built events | stored `Event`; event list; observation/evidence/fact events | `StateProjector`, owner services, event readers | duplicate event identity; execution authorization event validation; batch uniqueness | event order, workspace, causation/correlation, actor, payload | event kind/payload/actor/session/causation/correlation | movement: durable/in-memory or SQLite record |
| Projection | `project_constitutional_question()`, `project_constitutional_capabilities()`, and `StateProjector` projection. | constitutional act / lens depending surface | bounded question, read-model contracts/builders, or event ledger | projection artifacts or `State` | selection, read models, diagnostics | exact caller-declared keys; read-only flags; source contracts | identity, uncertainty, unknowns, compatibility, event-derived state | contracts, builders, state/projector inputs | representation; state projection computes derived state |
| Composition | `build_constitutional_view_composition()` composes explicitly requested registered views. | constitutional act / representation relationship | explicit composition request, registered view contracts/builders | `ConstitutionalViewCompositionArtifact` | pipeline result JSON/format/provenance explanation | requested view registration; unsupported requested view raises | contributing evidence, unknowns, explicit refusals, read-only boundaries | requested view names, purpose, output format | representation only |
| Communication | format/json functions render artifacts; runtime returns `RuntimeResponse`. | lens / communication surface | artifacts or runtime event ids | JSON-ready dicts, human text, response payload | CLI/tests/callers | mostly none beyond artifact shape | boundary flags and provenance fields | output format, renderer call | representation only |

## Inventory of observed constraints

| Constraint candidate | Observed evidence | Classification | Governs acts | Separate stage or orthogonal condition |
|---|---|---|---|---|
| Identity | Stable IDs from hashed bounded question/operator expression payloads; event IDs must be unique in ledger. | constraint | translation, establishment, recording | orthogonal condition; also created by constructors |
| Provenance | Bounded questions preserve inquiry provenance; observations become evidence payloads; events preserve causation/correlation. | constraint / testimony | establishment, interpretation, recording, projection | orthogonal condition preserved across acts |
| Authority | Interpretation refuses to treat authority-bearing language as grant; bounded questions refuse authority creation; runtime rejects model decision authority. | constraint / validation judgment | interpretation, establishment, runtime recording | orthogonal condition; sometimes an act of validation/refusal |
| Scope | Bounded question `scope_status`, interpreted `scope_expressions`, observation workspace, and event workspace. | constraint | establishment, interpretation, recording, projection | orthogonal condition |
| Warrant | Evidence IDs support Facts; constitutional composition correlates existing evidence but does not discover new evidence. | constraint | recording, projection, composition | orthogonal condition |
| Applicability | Interpretation validates grammar applicability references and state before parsing. | validation act / constraint | interpretation | separate validation step inside interpretation; not universal stage |
| Admissibility | Registered view composition rejects unsupported requested view names. | constraint / validation act | composition | orthogonal guard inside composition |
| Sufficiency | Selection records no match and unsupported keys; no universal sufficiency gate proven. | judgment / unproven as global constraint | selection | act-specific condition, not universal stage |
| Currentness | Observation/Facts carry `observed_at` and `expires_at`; state projection imports expiration helpers. | constraint | observation, fact projection | orthogonal condition; no universal constitutional stage proven |
| Availability | Missing capability builders produce `Unknown`; diagnostic/read surfaces expose availability-like fields in specific modules. | constraint / unproven as universal | capability projection, selection | conditional, representation-specific |
| Stopping | Unsupported/unknown states stop interpretation from handoff; unsupported selection keys stop view selection from composing those views. | constraint / branch condition | interpretation, selection | act-specific branch, not global stage |
| Read-only / mutation boundary | Many artifacts carry `read_only=True`, `writes_event_ledger=False`, `mutates_cluster=False`; recording surfaces write events; runtime records input but refuses decision authority. | constraint / boundary flag | establishment, projection, selection, composition, interpretation, recording, communication | orthogonal condition; also decisive classification evidence |

## Act-to-constraint incidence map

| Act | Identity | Provenance | Authority | Scope | Warrant | Applicability | Admissibility | Sufficiency | Currentness | Availability | Stopping | Read-only/mutation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Translation | yes | preserves | preserves/refuses authority | preserves | no | no | no | no | no | no | no | read-only |
| Interpretation | yes | preserves | checks/refuses grant | preserves | lexical/support refs | checks | no | parse sufficiency local | no | no | stops on unknown/unsupported/conflict | read-only |
| Binding | yes | preserves | explicitly not authority | local choice-set scope | no | no | token admissibility | local token match | no | no | unsupported token states | read-only |
| Establishment | stable ID | preserves | refuses creation | caller-provided status | no | no | no | no | no | no | no | read-only |
| Evaluation | artifact IDs | preserves uncertainty | no authority creation | projected input scope | compatibility evidence | no | no | exact-key match | no | capability absence as Unknown | no selected views branch | read-only |
| Selection | selected names | preserves bounded question id | no authority | projected input scope | capability keys | no | registered names later | exact-key match | no | missing capability keys | empty selection | read-only |
| Recording | event IDs | creates/preserves causation/correlation | actor and auth validation for execution events | workspace | event payload/evidence | no | event validation | no | timestamps in Event/Observation | no | duplicate IDs fail | writes ledger; mutation boundary depends surface |
| Projection | preserves IDs | preserves evidence/support | no new authority | workspace/state scope | evidence IDs/support | no | no | no | expiration helpers | no | replay assessment internally | usually read-only derived state |
| Composition | artifact identity by request content | preserves contributing evidence | refuses authority | requested views | correlates existing evidence | no | checks registered views | no | no | requested builders/contracts | unsupported request raises | read-only |
| Communication | no new identity | preserves rendered fields | no | no | no | no | no | no | no | no | no | read-only lens |

## Producer-to-consumer relationships

| Producer | Consumer | Relationship classification | Evidence summary |
|---|---|---|---|
| `produce_bounded_constitutional_question()` | `project_constitutional_question()` and `invoke_constitutional_pipeline()` | required sequence only inside constitutional pipeline invocation | pipeline request requires a `BoundedConstitutionalQuestion`; projection function signature consumes it |
| `project_constitutional_question()` | `select_constitutional_views()` | required sequence inside pipeline | selection signature consumes question projection, not raw question |
| `project_constitutional_capabilities()` | `select_constitutional_views()` | required sequence inside pipeline | selection consumes capability projections; builders can be caller-supplied |
| `select_constitutional_views()` | `selected_constitutional_views_to_composition_request()` | optional handoff / required inside pipeline helper | adapter consumes selected artifact to build request |
| `ConstitutionalViewCompositionRequest` | `build_constitutional_view_composition()` | required sequence for composition | composition function consumes explicit request |
| `ObservationIngestor.observation_to_evidence()` | `ObservationIngestor.observation_to_fact()` | conditional sequence | Fact production suppressed for specific metadata; evidence always produced for ingested observations |
| `ObservationIngestor.ingest_many()` | `EventLedger.append_many()` | required sequence for recording ingested observations | ingestor creates events then ledger stores batch |
| `EventLedger` | `StateProjector` | evidence dependency / projection relationship | ledger architecture declares feed to projector; projector imports/consumes ledger |
| `attribute_operator_expression()` | `interpret_operator_expression()` | required sequence for interpretation road | interpretation signature consumes attributed expression |
| `interpret_operator_expression()` | future authority/scope binding | optional handoff | handoff only exists when interpretation state is `interpreted`; no live binding consumer proven here |
| Direct dataclass construction | downstream format/json helpers | constructible bypass | construction proves artifact shape constructibility, not live producer authority |

## Confirmed branches and convergence points

- Composition converges selected registered view names into contributing view artifacts and correlated existing evidence, but only after explicit registered-view admission.
- Constitutional pipeline converges bounded question, question projection, capability projection, selection, composition request, and composition artifact into one result. This is an ordered invocation surface, not proof of universal constitutional order.
- Observation ingestion branches after evidence creation: fact production may be suppressed; observation and evidence events still record.
- Interpretation branches by applicability state, parse support, unknown references, conflicts, and unsupported residual spans. Only the `interpreted` branch emits a future authority/scope handoff.
- Runtime free-text input records `input.user_message` and a refusal event, then returns unsupported; it does not converge into model-routed movement.

## Lenses and optional entrances previously mistaken for roads

- Formatters and JSON renderers are communication lenses, not producers of constitutional authority.
- `constitutional_view_composition_request()` is a constructor for an explicit request, not selection evidence.
- `selected_constitutional_views_to_composition_request()` is a wiring adapter, not an independent constitutional judgment.
- Direct dataclass construction is constructibility, not live production authority.
- Capability view builders are optional entrances into capability projection; caller-supplied builders can substitute deterministic sources.
- Pipeline invocation is an optional composite entrance over already existing stages, not the source of bounded-question establishment.

## Mandatory-stage claims contradicted by bypass evidence

- Interpretation is not mandatory before bounded constitutional question establishment: bounded questions are produced from explicit caller fields, not from `OperatorExpressionInterpretationProjection`.
- Recording is not mandatory for bounded question, question projection, selection, or composition: these artifacts carry `writes_event_ledger=False`.
- Composition is not mandatory for recording or state projection: runtime input and observation ingestion write events without constitutional view composition.
- Selection is not mandatory for direct composition request construction: public request constructor can specify requested views directly, subject to composition admission checks.
- Fact production is not mandatory after observation: suppression metadata can yield observation/evidence events without a Fact.
- Model decision is not mandatory for runtime input: runtime explicitly records refusal rather than route model-produced decisions.

## Artifacts lacking proven origination authority

- `FutureOperatorAuthorityScopeBindingHandoff` has a live producer in interpretation, but no proven live authority/scope binding consumer recovered here. `[UNPROVEN]`
- Examination and operational realization artifacts are present as modules, but this audit did not prove their universal producer-to-consumer position relative to the constitutional pipeline. `[UNPROVEN]`
- Existing constitutional view artifacts are produced by builders, but their underlying constitutional legitimacy is not established by composition; composition only consumes registered read models. `[UNPROVEN]` for any stronger claim.
- Directly constructible dataclasses throughout the repository lack proven live origination authority unless a production function/caller path is identified. `[UNPROVEN]`

## Caller-controlled assertions

- Bounded question semantic fields, scope status, constitutional intent, uncertainty, unknowns, and selection keys are caller-controlled inputs to `produce_bounded_constitutional_question()`.
- Constitutional pipeline capability contracts, registrations, and builders can be supplied by the caller.
- Composition requested view names, purpose, and output format are caller-controlled, then constrained by registered-view admission.
- Event kind, payload, actor, workspace, session, causation, and correlation are caller-controlled at `EventLedger.append()` subject to ledger validation.
- Observation metadata can control fact promotion suppression in the Prometheus-specific path.
- Interpretation mechanism refs, invocation contract refs, lexical/domain/support refs, provenance, unknowns, and conflicts are caller-controlled inputs around the grammar/applicability artifacts.

## Answers to asymmetrical topology questions

1. Sequential proof requires a function signature plus production caller that consumes the prior artifact. The constitutional pipeline proves bounded question -> question projection -> selection -> composition request -> composition only inside `invoke_constitutional_pipeline()`.
2. Separate-stage proof appears where a named artifact/function consumes a previous artifact and produces a new artifact, such as question projection and selection. Constraints such as read-only, authority refusal, and provenance usually appear as fields/boundaries across multiple acts, so they are orthogonal unless implemented as a validation branch.
3. Many acts occur without proposed constraints: bounded question establishment occurs without interpretation applicability; composition occurs without recording; recording occurs without composition; runtime input recording occurs without selection.
4. Authority, provenance, scope, identity, and read-only/mutation boundaries govern multiple acts.
5. Formatters, JSON surfaces, request constructors, capability builders, and provenance explanations are lenses, constructors, or testimony-preserving explanations rather than roads.
6. Applicability, admissibility, sufficiency, and stopping often appear as acts of validation/admission/judgment inside interpretation, composition, and selection.
7. Confirmed roads are conditional or representation-specific. Universal roads are not proven.
8. Live bypasses include direct composition request construction bypassing selection, bounded question production bypassing interpretation, event recording bypassing constitutional composition, and observation recording bypassing Fact production.
9. Artifacts consumed downstream without proven live producer include future authority/scope binding consumers and some examination/realization positions in a global constitutional topology. `[UNPROVEN]`
10. Relationships among all candidate acts as a final canonical pipeline remain unproven. `[UNPROVEN]`

## Unresolved topology

- `[UNPROVEN]` Whether examination is a universal act or a family of conditional diagnostic/probe selection surfaces.
- `[UNPROVEN]` Whether realization follows selection, evaluation, warrant, authority, or a separate operational road in every live path.
- `[UNPROVEN]` Whether constraints such as sufficiency and availability should be promoted to standalone stages outside specific surfaces.
- `[UNPROVEN]` Whether constitutional view builders derive from a deeper live constitutional act road or are bounded read-model testimony.
- `[UNPROVEN]` Whether all recording surfaces are constitutional recording rather than operational event persistence in specific owners.
- `[UNPROVEN]` Whether projection publication internals in `StateProjector` establish a constitutional publication act or only an implementation-local projection step.

Constitutional acts and constraints topology audit complete.
