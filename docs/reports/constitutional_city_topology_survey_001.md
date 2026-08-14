# Constitutional City Topology Survey 001

## Scope and evidence basis

This survey began from the constitutional grammar supplied by the operator, then reviewed live repository roads rather than treating any existing pipeline diagram as authoritative. Evidence was taken from production modules, CLI ingress, public APIs, dataclass fields, validation checks, event creation, and downstream consumption. Tests and prior audit reports were used only as locating aids when useful, not as constitutional proof.

Reviewed implementation districts include `scripts/seed_local.py`, `seed_runtime/runtime.py`, `seed_runtime/api.py`, `seed_runtime/bounded_constitutional_question.py`, `seed_runtime/constitutional_pipeline.py`, ingress and goal-establishment modules, inquiry/frontier modules, view projection/composition modules, operational-realization modules, execution/recording modules, diagnostics, event storage, and related selection/projection surfaces.

## 1. Constitutional grammar recovered

The smallest source-neutral grammar supported across the repository is:

```text
external material
→ representation translation
→ bounded constitutional meaning
→ authority and scope
→ bounded objective
→ present-state evaluation
→ warranted constitutional movement
→ result preservation
→ external translation
```

The repository does not implement this as one universal linear pipeline. It implements several partial roads, optional entrances, read-only lenses, constructors, and operational roads that overlap the grammar without proving every transition.

### Separated grammar responsibilities

| Grammar element | Repository-supported meaning | Confirmed boundaries |
|---|---|---|
| translation | Preserve or normalize external/operator material into typed artifacts. | `attribute_operator_expression` normalizes exact operator text but does not establish authority or bounded questions. Candidate external-grammar and external-material projections are diagnostic/structural roads, not universal ingress. |
| meaning | Interpret attributed expression under a recovered/applicable grammar. | `OperatorExpressionInterpretationProjection` may classify expression form, request kind, scope expressions, constraints, unknowns, conflicts, and a future handoff. It explicitly does not authorize, schedule, emit, execute, or produce a bounded constitutional question. |
| goal | Establish bounded operator orientation from lawful ingress artifacts. | `BoundedOperatorGoalEstablishment` can be produced from closed-choice binding, interpretation, authority/scope binding, or downstream admission. It separates goal establishment from inquiry opening, resource observation, authorization, execution, recording, and satisfaction. |
| evaluation | Evaluate present known state against bounded goal/horizon, inquiry testimony, capability reachability, frontier evidence, policy, or diagnostics. | Implemented as several conditional projections and selections; no universal present-state evaluator is proved. |
| need | Preserve specific need families only when required typed evidence is supplied. | Inquiry, clarification, authority, and operational-realization need surfaces require explicit testimony/handoffs. Generic unknowns do not automatically establish a need. |
| movement | Select or execute only through roads with required warrant. | Read-only selections are not movement authorization. Registered tool execution is a separate operational road gated by registry validation and policy. |
| result | Preserve execution or diagnostic outputs as events or read-only artifacts. | Event recording is distinct from execution and fact extraction. Diagnostic records are scoped separately when declared. |
| recording | Append events or diagnostic facts. | `EventLedger.append` records runtime events; diagnostic inventory distinguishes `record_scope=diagnostic_run` from cluster facts. |
| external expression | Format or render artifacts for humans/JSON/CLI/API. | Formatters and composition views are lenses unless they are part of a specific road with a consuming destination. |

## 2. Start-to-finish live road inventory

### Road A: free-text runtime ingress to bounded stop

| Field | Finding |
|---|---|
| source | `SeedAPI.post_user_message` and `Runtime.handle_user_message`. |
| producer | `Runtime.handle_user_message`. |
| destination | `RuntimeResponse(kind="unsupported")` plus ledger events `input.user_message` and `runtime.decision_authority_unsupported`. |
| destination assertion | Free-text input was recorded, and no Seed-owned runtime decision authority exists for routing it. |
| required warrant | Only receipt of text and absence of configured internal runtime decision authority. |
| actual producer evidence | The method appends the exact text as an input event, appends an unsupported-authority event, discards any supplied decision producer by setting `self.decision_producer = None`, and returns unsupported. |
| decisive caller-controlled inputs | `workspace_id`, `session_id`, `text`. Caller cannot manufacture a successful movement from this road. |
| consumers | API clients and tests can consume the response and event ledger. No live movement consumer requires a routed decision. |
| alternate paths | CLI flags, direct constructors, diagnostic/projection commands, and registered tool execution bypass free-text runtime routing. |
| classification | branch: bounded stop/refusal path. |
| unproven points | No live producer proves free-text external interrogative form becomes internal inquiry. No universal runtime decision path exists. |

### Road B: attributed operator expression to interpretation

| Field | Finding |
|---|---|
| source | Raw operator text supplied to `attribute_operator_expression`; recovered grammar and applicability supplied to `interpret_operator_expression`. |
| producer | `attribute_operator_expression` and `interpret_operator_expression`. |
| destination | `AttributedOperatorExpression`; `OperatorExpressionInterpretationProjection`; optional `FutureOperatorAuthorityScopeBindingHandoff`. |
| destination assertion | Exact text has been attributed; expression has been interpreted under one bounded grammar with explicit state, components, unresolved spans, unknowns, and conflicts. |
| required warrant | Exact text plus a recovered grammar and applicability context sufficient for deterministic pattern matching. |
| actual producer evidence | Text normalization, stable identity payloads, pattern matching, grammar supported-structure checks, provenance, unknown/conflict fields. |
| decisive caller-controlled inputs | Exact text, operator/workspace/session refs, provenance, grammar object, applicability projection, candidate interpretation fields indirectly through supplied grammar evidence. |
| consumers | Authority/scope binding consumes the interpretation and its future handoff; bounded goal establishment can consume interpretation directly. |
| alternate paths | Closed-choice selection, downstream admission, and direct bounded-question constructors bypass expression interpretation. |
| classification | optional entrance into meaning/orientation; conditional branch toward authority/scope binding. |
| unproven points | Interpretation does not prove authority, selected question family, bounded constitutional question, authorization, or execution. Caller-provided context remains testimony unless checked downstream. |

### Road C: interpretation to authority/scope binding

| Field | Finding |
|---|---|
| source | `OperatorExpressionInterpretationProjection`, `FutureOperatorAuthorityScopeBindingHandoff`, attributed expression, operator identity context, workspace/session authority context, scope binding context. |
| producer | `bind_operator_authority_scope`. |
| destination | `OperatorAuthorityScopeBindingProjection`. |
| destination assertion | A requested activity and requested scope are classified as permitted, blocked, unknown, or conflict relative to supplied authority/scope evidence. |
| required warrant | Identity consistency across interpretation, expression, operator, workspace, session, requested scope resolution, permitted/prohibited scope refs, and authority classes. |
| actual producer evidence | Explicit mismatch checks for handoff, expression, operator, workspace, session; activity mapping; resolved/permitted/excluded/unresolved scope calculations; authority-class comparison; constraint conflict checks. |
| decisive caller-controlled inputs | Operator identity authority classes, workspace permitted/prohibited scope refs, scope-binding mappings, unknowns/conflicts, and supporting refs are caller-supplied structures. |
| consumers | `establish_bounded_operator_goal_from_authority_scope_binding`; `explain_minimum_lawful_advancement`; diagnostics/tests. |
| alternate paths | Goal establishment can bypass authority/scope by consuming closed-choice, interpretation, or downstream admission. Operational execution has its own registry/policy road. |
| classification | branch: authority movement/evaluation. It is legitimate conditionally, not universal. |
| unproven points | A `permitted` binding is not a bounded question, selected realization, authorization to execute, recording, or knowledge extraction. Caller can influence authority outcome through context objects; the function validates consistency, not independent real-world authority ownership. |

### Road D: closed-choice binding to bounded operator goal

| Field | Finding |
|---|---|
| source | `ClosedChoiceSelectionBinding`. |
| producer | `establish_bounded_operator_goal_from_closed_choice`. |
| destination | `BoundedOperatorGoalEstablishment`. |
| destination assertion | A closed-choice selection supplies bounded operator orientation, either established/provisional/refused depending on binding state and sufficiency conditions. |
| required warrant | Artifact type must be `ClosedChoiceSelectionBinding`; binding must be `bound` with a bound option ref for orientation. |
| actual producer evidence | Binding state, bound option ref/label, exact choice set fingerprint, token capture ref, unknown/unsupported/conflicting selection evidence. |
| decisive caller-controlled inputs | The binding artifact fields and optional sufficiency/stop/unresolved/known-loss/correction fields. |
| consumers | Advancement horizon and need/evaluation surfaces can consume bounded goal establishment. |
| alternate paths | Interpretation, authority/scope binding, and downstream admission can also establish bounded operator goal. |
| classification | optional entrance/constitutional road for bounded objective only when binding evidence is valid. |
| unproven points | Goal establishment is not inquiry opened, resources observed, constraints enforced, work authorized, execution started, recording started, or satisfaction judged. |

### Road E: interpreted expression to bounded operator goal

| Field | Finding |
|---|---|
| source | `OperatorExpressionInterpretationProjection`. |
| producer | `establish_bounded_operator_goal_from_interpretation`. |
| destination | `BoundedOperatorGoalEstablishment`. |
| destination assertion | Interpreted expression components supply bounded orientation, provisional unless sufficiency conditions are supplied and unknowns are absent. |
| required warrant | Interpretation artifact type must match; interpretation state must be `interpreted`; orientation expressions must be present. |
| actual producer evidence | Relation/focus/subject/object/scope expressions, unresolved lexical/references/residual spans, operator-stated constraints, unknowns/conflicts. |
| decisive caller-controlled inputs | Interpretation artifact contents and optional sufficiency/stop conditions. |
| consumers | Advancement and need surfaces. |
| alternate paths | Closed choice, authority/scope binding, downstream admission. |
| classification | optional entrance/constructor-adjacent road: it establishes orientation from interpreted components, not full constitutional movement. |
| unproven points | The producer does not re-run grammar recovery, authority binding, or selection; caller can pass a constructed interpretation dataclass if type/fields satisfy checks. |

### Road F: authority/scope binding to bounded operator goal

| Field | Finding |
|---|---|
| source | `OperatorAuthorityScopeBindingProjection`. |
| producer | `establish_bounded_operator_goal_from_authority_scope_binding`. |
| destination | `BoundedOperatorGoalEstablishment`. |
| destination assertion | A permitted authority/scope binding can supply bounded operator orientation; non-permitted states refuse or preserve unresolved boundaries. |
| required warrant | Authority/scope binding artifact type and binding state/reason evidence. |
| actual producer evidence | Binding state, requested activity, requested/resolved/permitted/excluded/unresolved scopes, authority sources, constraints, unknowns/conflicts. |
| decisive caller-controlled inputs | Upstream authority/scope context remains decisive. |
| consumers | Advancement/evaluation surfaces. |
| alternate paths | Other goal-establishment entrants. |
| classification | branch: authority-conditioned optional entrance to goal orientation. |
| unproven points | A permitted authority/scope projection does not select work, authorize execution, or prove external permission beyond supplied authority contexts. |

### Road G: explicit bounded constitutional question constructor to view pipeline

| Field | Finding |
|---|---|
| source | Caller supplies all bounded question fields to `produce_bounded_constitutional_question` or constructs `BoundedConstitutionalQuestion`. |
| producer | `produce_bounded_constitutional_question`; `ConstitutionalPipelineRequest`; `invoke_constitutional_pipeline`. |
| destination | `BoundedConstitutionalQuestion`, then `ConstitutionalQuestionProjection`, `ConstitutionalCapabilityProjection`, `SelectedConstitutionalViews`, `ConstitutionalViewCompositionArtifact`. |
| destination assertion | Explicit caller-supplied bounded fields are preserved; selection keys are exact caller-declared fields; registered read-model capability keys are projected; exact key matches select view names; requested views are composed into a bounded explanation. |
| required warrant | For bounded question: none beyond explicit fields. For selection: exact `selection_key`/`selection_key:*` matching projected capability keys. For composition: selected names must be registered constitutional read models. |
| actual producer evidence | Caller fields; read-model contracts and registrations; immutable view builders; exact key matching; registered builders; read-only boundary flags. |
| decisive caller-controlled inputs | `operator_inquiry`, `bounded_question`, `constitutional_intent`, `scope_status`, `unknowns`, `uncertainty`, `caller_supplied_fields`, capability registrations/builders in pipeline request, composition purpose/output format. |
| consumers | Pipeline result, provenance explanation, CLI/API tests and formatters. |
| alternate paths | Direct `build_constitutional_view_composition` can bypass question projection and selection by accepting explicit requested views. Individual constitutional views can be built directly. |
| classification | constructor plus selection surface plus lens. The pipeline is live and deterministic, but not a universal constitutional road from external material to movement. |
| unproven points | Bounded question fields are not independently established facts; selection keys are caller-supplied; selected views are view names, not movement authorization; composition is explanation, not knowledge extraction or execution. |

### Road H: direct constitutional view composition

| Field | Finding |
|---|---|
| source | `constitutional_view_composition_request(requested_views=...)`. |
| producer | `build_constitutional_view_composition`. |
| destination | `ConstitutionalViewCompositionArtifact`. |
| destination assertion | Explicitly requested registered constitutional read-model views were composed read-only. |
| required warrant | Requested view names must be in read-model contracts and builder map. |
| actual producer evidence | Contract lookup, builder execution, JSON renderers, evidence/unknown/refusal aggregation. |
| decisive caller-controlled inputs | Requested view names, purpose label, output format. |
| consumers | CLI surface and pipeline adapter. |
| alternate paths | Pipeline selection can produce composition request; individual views can be rendered directly. |
| classification | lens/optional entrance, not movement gate. |
| unproven points | Does not discover evidence, resolve unknowns, establish authority, plan, record, or mutate. |

### Road I: bounded goal/horizon/need projections

| Field | Finding |
|---|---|
| source | `BoundedOperatorGoalEstablishment`, `BoundedAdvancementHorizon`, and explicit testimony objects such as `RepositoryWorldUncertaintyTestimony`. |
| producer | Goal/horizon/need projection modules including `inquiry_need_projection`, `clarification_need_projection`, `authority_need_projection`, `operational_realization_need_projection`, and related consideration-selection modules. |
| destination | Need projection artifacts partitioning established/unsupported/unknown/conflicting/excluded/unclassified material. |
| destination assertion | A specific need family is established or not only from component-bounded testimony matching selection, goal, horizon, and evidence identities. |
| required warrant | Identity matches; owning stage; component-bounded material; family-specific subject; materiality to present movement boundary; no excluded family conflict. |
| actual producer evidence | Explicit testimony dataclasses, identity comparisons, stage ownership booleans, family fields, evidence freshness/availability, boundary flags. |
| decisive caller-controlled inputs | Testimony dataclass fields, horizon evidence refs, selection/goal/horizon identities, family/status fields. |
| consumers | Consideration/selection/audit surfaces and CLI diagnostics. |
| alternate paths | Operational execution does not require these need projections; view composition does not require them. |
| classification | conditional branches and selection surfaces. |
| unproven points | Need established is not movement opened, question selected, observation authorized, action selected, sufficiency judged, execution, recording, event-ledger writing, or cluster mutation. |

### Road J: inquiry frontier and examination

| Field | Finding |
|---|---|
| source | `BoundedConstitutionalQuestion` plus caller-supplied corpus members and candidate work. |
| producer | `project_examination_frontier`. |
| destination | `ExaminationFrontier` with work-item classifications. |
| destination assertion | Supplied corpus/work visibility was classified as eligible, examined, blocked, unsupported, deferred, failed, unknown, or conflict. |
| required warrant | Structurally valid bounded inquiry, corpus id, unique corpus members/work ids, candidate work references known corpus members, compatibility/authorization/status evidence consistent. |
| actual producer evidence | Caller-supplied corpus/work/result references, compatibility status, authorization status, blockers, deferral, failure references, result-state matching. |
| decisive caller-controlled inputs | All corpus, work, status, blocker, failure, authorization, and prior-result fields. |
| consumers | CLI diagnostic/projection surfaces and tests. |
| alternate paths | Inquiry need can exist without frontier; operational tool execution bypasses frontier; view pipeline bypasses frontier. |
| classification | lens/conditional branch for inquiry frontier visibility, not scheduler or movement gate. |
| unproven points | Frontier does not discover corpus members, select/authorize/execute eligible work, judge completion, or extract knowledge. |

### Road K: capability demand to operational realization selection

| Field | Finding |
|---|---|
| source | Candidate operational realization set, capability reachability projection, future selection handoff, optional selection policy. |
| producer | `select_operational_realization`. |
| destination | `OperationalRealizationSelection` and optional `FutureOperationalRealizationWarrantHandoff` when one candidate is selected. |
| destination assertion | Zero or one supported realization was selected according to policy from eligible supporting candidates. |
| required warrant | Handoff/projection/candidate-set identity matches; candidate standings match reachability partitions; policy constraints identify zero/one candidate. |
| actual producer evidence | Validation of handoff/projection/candidate-set identities, candidate standings, reachability state, policy kind, exact candidate or constraints. |
| decisive caller-controlled inputs | Candidate set fields, reachability projection, future handoff, selection policy fields. |
| consumers | Operational-realization warrant modules, CLI/tests. |
| alternate paths | Registered tool execution does not consume this selection; direct tool executor uses registry/policy. |
| classification | selection surface. Conditional road only for operational-realization analysis, not universal execution. |
| unproven points | Selection does not warrant reliance, construct invocation, translate representations, authorize, schedule, or execute. Caller can manufacture much of the candidate/policy evidence if constructors are accessible. |

### Road L: registered tool execution

| Field | Finding |
|---|---|
| source | `ToolExecutor.execute` with `tool_name`, `arguments`, workspace/session/scope. |
| producer | `ToolExecutionPolicyService`, `ToolValidationService`, `PolicyGate`, `ToolExecutor._execute_allowed_tool_call`, registered callable loaded by registry. |
| destination | `ToolCallResult`; ledger events `tool.call.started`, `tool.call.completed`/`tool.call.failed`/policy events; optional pending action; post-execution facts. |
| destination assertion | A registered tool call was validated, policy-allowed or blocked/approval-required, optionally executed, recorded, and then facts extracted from completed event. |
| required warrant | Registered tool, valid input schema/status, policy `allow` for execution, callable import succeeds, output schema validates. |
| actual producer evidence | Registry `require`, validation result, policy decision, event append, callable execution, output validation, completed event, fact extraction service. |
| decisive caller-controlled inputs | Workspace/session/tool name/arguments/scope; approval resume id. Registry and policy configuration are not caller fields in the execute call, but may be configured externally. |
| consumers | State projector, fact extraction, pending actions, API/CLI/toolkit callers. |
| alternate paths | Runtime free-text no longer routes to executor. Diagnostics and view pipelines do not require executor. |
| classification | constitutional road for operational realization when registry and policy warrant are present. |
| unproven points | This road does not consume constitutional view selection or operational-realization selection artifacts; execution result recording is distinct from knowledge extraction; fact extraction may promote only what its service recognizes. |

### Road M: event recording to projected state/facts

| Field | Finding |
|---|---|
| source | `EventLedger.append`, `append_many`, `extend`, SQLite compatibility ledger. |
| producer | Event ledger and services that append events. |
| destination | Stored `Event` objects read by `StateProjector`, fact extraction, diagnostics, history/status surfaces. |
| destination assertion | An event with unique id, kind, workspace, actor, payload, session/causation/correlation was stored append-only. |
| required warrant | Unique event id and execution authorization validation for applicable event kinds. |
| actual producer evidence | ID generation/reservation, duplicate checks, in-memory lists/maps, SQLite persistence compatibility. |
| decisive caller-controlled inputs | Event kind, workspace id, payload, actor, session/causation/correlation, or fully pre-built Event for `append_many/extend`. |
| consumers | State projector, execution status, fact extraction, diagnostics. |
| alternate paths | Read-only projections can bypass ledger; diagnostic records may use diagnostic-run scoped subjects. |
| classification | result preservation/recording road. |
| unproven points | Recording is not automatically constitutional knowledge extraction; caller-supplied payload fields are not testimony ownership unless downstream extraction validates them. |

### Road N: diagnostics, inventories, audits, orientation surfaces

| Field | Finding |
|---|---|
| source | CLI flags and direct diagnostic builders. |
| producer | `diagnostic_inventory`, `diagnostic_shape_audit`, operational surface inventory, question surface inventory, knowledge reachability, audits, and many read-only view builders. |
| destination | Diagnostic inventory entries, shape audit rows/summaries, formatted/JSON diagnostic outputs, optional diagnostic records. |
| destination assertion | A diagnostic/read-only surface is declared, checked, formatted, or recorded under its declared boundary. |
| required warrant | Static registry entry and implementation spec for inventory/shape audit; declared support for JSON/recording/ledger/mutation fields. |
| actual producer evidence | `DiagnosticInventoryEntry` fields, implementation specs, static marker scans, format/json/build function declarations. |
| decisive caller-controlled inputs | Diagnostic name/filters/status flags/json flags/record flags and some diagnostic input JSON. |
| consumers | CLI, tests, operators. |
| alternate paths | Diagnostics are not required by runtime execution or constitutional view selection except as visibility/audit obligations. |
| classification | lens/scaffolding/read-only projection, with diagnostic recording as a bounded recording road. |
| unproven points | Inventory presence does not prove constitutional movement; shape-audit consistency does not prove semantic legitimacy of the diagnosed surface. |

## 3. City topology

### Constitutional trunk supported by evidence

```text
external material
  ├─ Runtime free text → input event → unsupported bounded stop
  ├─ Attributed operator expression → interpretation → [optional authority/scope binding]
  ├─ Closed-choice binding → bounded operator goal
  ├─ Explicit bounded-question constructor → read-only question/capability/view pipeline
  └─ Registered tool call request → validation/policy → execution → recording → fact extraction
```

### Conditional branches

```text
interpretation + identity/scope/authority contexts
→ authority/scope binding
→ optional bounded operator goal establishment

bounded goal + horizon + family-specific testimony
→ clarification/inquiry/authority/operational-realization need projection
→ consideration/selection/audit surfaces

bounded question + supplied corpus/work visibility
→ examination frontier lens
```

### Optional entrances

- Closed-choice binding can establish bounded operator goal without free-text interpretation.
- Interpreted expression can establish bounded operator goal without authority/scope binding.
- Authority/scope binding can establish bounded operator goal when available.
- Explicit bounded-question constructors can enter the read-only view pipeline without proving upstream translation/meaning/goal.
- Direct view composition can bypass question projection and selection by accepting explicit registered view names.
- Registered tool execution can be invoked directly through executor/API/CLI roads without constitutional view selection.

### Lenses

- Constitutional process/governance/fidelity views.
- Constitutional view composition.
- Pipeline provenance explanation.
- Examination frontier.
- Diagnostic inventory and diagnostic shape audit.
- Question/capability/source/navigation/knowledge reachability and similar orientation inventories.

### Selection surfaces

- Closed-choice selection binding.
- Constitutional view selection by exact selection key.
- Goal inquiry consideration selection and advancement need selection surfaces.
- Operational realization selection by policy over explicit candidates.
- Recommendation/ranking surfaces where present are bounded choices, not authorization.

### Constructors

- `produce_bounded_constitutional_question`.
- `constitutional_view_composition_request`.
- Static policy constructors such as `OperationalRealizationSelectionPolicy.exact_candidate`, `.sole_supported_candidate`, `.select_none`, `.constraints`.
- Dataclass constructors for testimony, contexts, candidates, corpus members, and projected artifacts where not protected by producer validation.

### Scaffolding

- Static decision producer retained as inert compatibility residue.
- Prior architecture/audit markdown files.
- Tests that assert expected behavior.
- Generated/diagnostic inventories as visibility support.

### Dead or invalid roads observed

- Free-text `DecisionProducer.decide -> Runtime._route` is explicitly removed/unsupported; supplying a decision producer cannot restore movement.
- Any claim that constitutional view selection authorizes execution is unsupported by live consumers.
- Any claim that diagnostic inventory/shape audit is a constitutional movement gate is unsupported; these are read-only visibility surfaces.

### Unproven junctions

- `[UNPROVEN]` Bounded operator goal → bounded constitutional question. Multiple goal artifacts exist, but the reviewed live code does not prove a universal producer that converts established goal into bounded constitutional question with constitutional ownership.
- `[UNPROVEN]` Inquiry need established → inquiry opened. Need projections preserve that inquiry has not opened.
- `[UNPROVEN]` Operational realization selection → registered tool invocation. The executor uses registry and policy, not the selection artifact.
- `[UNPROVEN]` Diagnostic recording → cluster knowledge. Diagnostic boundaries preserve diagnostic-run scope unless intentionally different.

## 4. Universal-road claims falsified

| Structure | Treated-as claim falsified | Evidence-supported role |
|---|---|---|
| `ConstitutionalPipelineRequest` / `invoke_constitutional_pipeline` | Universal Seed pipeline from operator request to constitutional movement. | Deterministic read-only adapter over an already-established bounded question and view selection/composition. |
| `BoundedConstitutionalQuestion` | Established internal inquiry/goal. | Constructor-preserved caller-supplied fields and testimony boundary. |
| `ConstitutionalQuestionProjection` | Semantic question understanding. | Exact caller-declared selection-key projection. |
| `SelectedConstitutionalViews` | Universal selection of what Seed should do. | Exact selection surface over registered read-model capability keys. |
| `ConstitutionalViewCompositionArtifact` | Result of constitutional movement. | Bounded explanation lens over explicitly requested views. |
| `ExaminationFrontier` | Scheduler or inquiry gate. | Read-only classification of supplied corpus/work visibility. |
| Need projections | Movement opened. | Conditional evaluation of explicit family-specific testimony; movement flags remain false. |
| Operational realization selection | Execution authorization/invocation. | Selection surface producing optional future warrant handoff, not execution. |
| Diagnostic inventory/shape audit | Constitutional gates. | Read-only visibility/audit lenses. |
| Runtime decision producer | Live decision authority. | Compatibility residue; unsupported and not consumed. |

## 5. Missing origination authority

Artifacts lawfully consumed downstream but lacking a proven live constitutional producer in the reviewed road set:

1. `BoundedConstitutionalQuestion` as an established constitutional question. The constructor preserves explicit caller fields; no live upstream producer proves translation → meaning → authority/scope → bounded objective → bounded question ownership.
2. `ClosedChoiceSelectionBinding` as a constitutionally owned selection. Goal establishment consumes it, but the survey did not prove universal origination authority for the binding.
3. `OperatorIdentityContext`, `WorkspaceSessionAuthorityContext`, and `ScopeBindingContext` as independent authority testimony. Authority/scope binding validates consistency, but caller-supplied authority fields remain decisive.
4. `RepositoryWorldUncertaintyTestimony` and related need-family testimony. Need projections consume them lawfully, but live origination authority for testimony ownership is not proved.
5. `BoundedAdvancementHorizon` as universal present-state evaluation. Need projections consume it, but no universal road from goal to horizon was established in this survey.
6. `CandidateOperationalRealizationSet`, `CapabilityReachabilityProjection`, and `FutureOperationalRealizationSelectionHandoff` as operational candidate truth. Selection validates identity and partitions but does not prove independent origination for every supplied candidate/reachability assertion.
7. Corpus/work/result references for `ExaminationFrontier`. The frontier validates structure and internal consistency, not discovery/ownership.
8. Event payload assertions passed to `EventLedger.append` or `append_many`; recording uniqueness is proved, payload truth is downstream-specific.

## 6. Caller-controlled constitutional assertions

Production surfaces where callers can manufacture or strongly influence claims by constructing dataclasses or supplying fields:

| Surface | Manufacturable claim | Boundary consequence |
|---|---|---|
| `produce_bounded_constitutional_question` / `BoundedConstitutionalQuestion` | `bounded`, `constitutional_intent`, `scope_status`, selection keys, unknowns/uncertainty. | Preserved as caller testimony, not established fact. |
| `ConstitutionalPipelineRequest` | Capability contracts/registrations/builders and composition purpose. | Pipeline can be made to see alternate capability evidence; still read-only. |
| `constitutional_view_composition_request` | Requested registered views and purpose. | Composition proves explicit request, not selection warrant. |
| `attribute_operator_expression` | Operator/workspace/session/provenance context. | Attribution preserves caller context unless downstream identity checks compare it. |
| `OperatorExpressionInterpretationProjection` dataclass construction | `interpreted`, request kind, scope, constraints, future handoff. | Direct dataclass construction can bypass producer parsing unless consumers validate specific identity/field invariants. |
| Authority context dataclasses | Authority classes, permitted/prohibited scopes, restrictions, sources. | Binding outcome is highly dependent on supplied context. |
| `ClosedChoiceSelectionBinding` | `bound`, selected option, unsupported/unknown/conflict evidence. | Goal establishment checks state/type but relies on supplied binding evidence. |
| Bounded goal establishment options | Sufficiency/stop conditions, unresolved scope, known loss. | `established` vs `provisional` can depend on caller-supplied sufficiency conditions. |
| Need testimony dataclasses | `established`, `unsupported`, `unknown`, family, owning stage, materiality. | Projection classifies supplied testimony; origination authority remains unproven. |
| `CorpusMember`, `CandidateWork`, `WorkResultReference` | eligible/examined/blocked/unsupported/deferred/failed status evidence. | Frontier validates consistency but does not discover truth. |
| `OperationalRealizationSelectionPolicy` | exact candidate, select none, sole supported, constraints. | Selection can be driven by caller policy over supplied candidates. |
| `EventLedger.append` / `append_many` | event kind/payload assertions, actor/session/correlation. | Recording proves storage, not payload truth or constitutional knowledge. |
| Diagnostic CLI inputs and JSON files | Surface-specific observations, filters, diagnostic record requests. | Diagnostic outputs are lenses/records scoped by declared boundaries. |

## 7. Naming mismatches

| Name | Implemented responsibility | Mismatch/consequence |
|---|---|---|
| `ConstitutionalPipeline` | Ordered invocation from already-supplied bounded question to read-only view composition. | Name can imply universal constitutional road; implementation is a deterministic adapter/lens pipeline. |
| `BoundedConstitutionalQuestion` | Immutable carrier of explicit caller-supplied fields. | Name can imply question is constitutionally established; constructor boundary says no natural-language classification or authority creation. |
| `ConstitutionalQuestionProjection` | Exact selection-key carrier. | Name can imply semantic question projection; actual projection reads caller-supplied selection fields only. |
| `ConstitutionalCapabilityProjection` | Read-model capability-key projection from view builders/contracts. | Name can imply operational capability discovery; actual scope is constitutional read-model compatibility keys. |
| `SelectedConstitutionalViews` | Exact-match selected view names. | Name can imply constitutional movement selection; actual selection is among registered read-only views. |
| `ConstitutionalViewCompositionArtifact` | Bounded explanation from requested views. | Name can imply composition of constitutional meaning; it composes read-model renderings without resolving unknowns. |
| `FutureOperatorAuthorityScopeBindingHandoff` | Carrier generated from interpretation for possible binding. | Name correctly signals future use, but can be mistaken as authority itself. |
| `OperatorAuthorityScopeBindingProjection` | Evaluation against supplied authority/scope contexts. | Name can imply actual authority binding; implementation validates supplied contexts and preserves states. |
| `BoundedOperatorGoalEstablishment` | Orientation artifact from specified ingress. | Name can imply objective fully selected/authorized; boundary flags deny inquiry/opening/execution/recording. |
| `InquiryNeedProjection` | Partitions explicit repository/world uncertainty testimony. | Name can imply inquiry opened; flags say `opens_inquiry=False`. |
| `ExaminationFrontier` | Read-only classification of supplied corpus/work visibility. | Name can imply active frontier/scheduler; boundary notes deny discovery, scheduling, queueing, completion verdict. |
| `OperationalRealizationSelection` | Policy selection of zero/one candidate. | Name can imply realization occurs; boundary says no invocation, authorization, scheduling, or execution. |
| `EventLedger` | Append-only event storage. | Name can imply historical truth; implementation records payloads and separates extraction. |
| `DiagnosticShapeAudit` | Static declaration/spec consistency check. | Name can imply semantic diagnostic validity; implementation observes markers and inventory fields. |

## 8. Confirmed city map

```text
[External operator/API/CLI material]
  ├─ Runtime.handle_user_message
  │    → input.user_message event
  │    → runtime.decision_authority_unsupported event
  │    → bounded unsupported response
  │
  ├─ attribute_operator_expression
  │    → AttributedOperatorExpression
  │    → interpret_operator_expression
  │       → OperatorExpressionInterpretationProjection
  │       ├─ bind_operator_authority_scope
  │       │    → OperatorAuthorityScopeBindingProjection
  │       │    → [optional] BoundedOperatorGoalEstablishment
  │       └─ establish_bounded_operator_goal_from_interpretation
  │            → BoundedOperatorGoalEstablishment
  │
  ├─ ClosedChoiceSelectionBinding [origin UNPROVEN]
  │    → establish_bounded_operator_goal_from_closed_choice
  │    → BoundedOperatorGoalEstablishment
  │
  ├─ BoundedOperatorGoalEstablishment
  │    → BoundedAdvancementHorizon [universal origin/transition UNPROVEN]
  │    → family-specific testimony projections
  │       → clarification/inquiry/authority/operational-realization need surfaces
  │       → selection/audit lenses
  │
  ├─ BoundedConstitutionalQuestion constructor
  │    → project_constitutional_question
  │    → select_constitutional_views + project_constitutional_capabilities
  │    → selected_constitutional_views_to_composition_request
  │    → build_constitutional_view_composition
  │    → bounded explanation lens
  │
  ├─ BoundedConstitutionalQuestion + supplied corpus/work
  │    → project_examination_frontier
  │    → frontier lens
  │
  ├─ CandidateOperationalRealizationSet + reachability + handoff + policy
  │    → select_operational_realization
  │    → optional FutureOperationalRealizationWarrantHandoff
  │    → [UNPROVEN junction to registered tool execution]
  │
  └─ ToolExecutor.execute
       → registry/status/input validation
       → policy decision
       ├─ block/approval-required → policy event + optional pending action
       └─ allow → tool.call.started → registered callable → output validation
                → tool.call.completed/tool.call.failed
                → fact extraction from completed event
```

Unresolved gaps are intentionally left as `[UNPROVEN]`; no adapter, handoff, or missing artifact is proposed.

## 9. Orientation corrections

| Prior orientation assumption | Status | Correction |
|---|---|---|
| Seed has one constitutional pipeline from ingress to answer. | too linear / contradicted | Live roads are multiple partial roads; the named pipeline is read-only view composition over an already supplied bounded question. |
| External interrogative form becomes internal inquiry. | unproven | Runtime records and stops; interpretation preserves request kind but does not open inquiry. |
| Bounded question means goal established. | contradicted | Bounded question constructor preserves caller-supplied fields; separate goal establishment artifacts exist. |
| Goal established implies advancement need. | contradicted | Goal establishment flags deny advancement/inquiry/execution; need projections require explicit family testimony and horizon identities. |
| Need established opens movement. | contradicted | Need projection flags preserve no inquiry opened, no action selected, no authorization, no execution, no recording. |
| View selection is universal selection. | based on a lens mistaken for a road | It selects among registered constitutional read-model views by exact keys. |
| Capability projection discovers operational capabilities. | too universal | Constitutional capability projection exposes read-model keys; operational capability catalogs/registered tools are separate roads. |
| Operational realization selection authorizes execution. | contradicted/unproven junction | Selection explicitly does not authorize/schedule/execute; executor uses registry and policy directly. |
| Diagnostic inventory and shape audit gate movement. | lens mistaken for road | They declare/check visibility surfaces; they do not authorize constitutional movement. |
| Event recording equals knowledge extraction. | contradicted | Executor records completed events, then separately calls fact extraction; ledger append alone stores payloads. |
| Mature/public artifacts are constitutional roads. | contradicted | Many public dataclasses are constructors, lenses, or scaffolding without origination authority. |

Constitutional city topology survey complete.
