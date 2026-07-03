# Constitutional permission bridge investigation

## Selected constitutional question

Does implementation evidence support a recurring constitutional bridge between evidence-producing physiology and behavior-producing physiology whose responsibility is preserving permission to proceed, rather than owning behavior itself?

## Implementation evidence reviewed

Implementation evidence reviewed:

- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `constitutional_self_governance_competency_investigation.md`
- `evidence_interpretation_competency_recovery_investigation.md`
- `responsibility_evaluation_competency_recovery_investigation.md`
- `observation_agreement_architectural_position_audit.md`
- `pressure_visibility_evidence_classification_boundary_investigation.md`
- `pressure_audit_smallest_owner_investigation.md`
- `question_bounded_work_invocation_investigation.md`
- `implementation_execution_grammar_recovery_investigation.md`
- `constitutional_physiology_behavior_architecture.md`

This report treats code as stronger evidence than prior characterization documents. Prior investigations are used only where they summarize implementation-backed boundaries that still match code evidence.

## Neighboring architectural neighborhoods

### Evidence-producing side

The evidence-producing side is not one neighborhood. Current implementation evidence supports at least these adjacent neighborhoods:

1. **Question-family / inquiry eligibility**
   - `bounded_status_for_question_family()` derives `eligible_with_parameters`, `eligible_now`, `diagnostic_only`, and `not_dispatchable` from implementation maps.
   - `BoundedWorkEligibilityResult` names this as an implementation-backed permission result for exact `QuestionFamily` invocation.
   - Unknown question families are explicitly represented with `unknown` status fields in question-family definition output, not silently treated as executable.

2. **Observation permission / authority visibility**
   - `ObservationPermissionDomain` separates `observation_class`, `permission_state`, `authority_evidence`, `reusable_permission`, and `future_autonomous_invocation`.
   - Its report boundary is read-only, does not write the event ledger, does not mutate the cluster, does not enforce permission, does not store approval, and does not create runtime autonomy.

3. **Observation-domain evidence / pressure visibility**
   - `ObservationDomainReport` is read-only and records `classification`, `gap_type`, pressure, and evidence for observation domains.
   - This neighborhood identifies observed, partially observed, or unobserved domains and the evidence pressure behind them, but does not itself perform runtime behavior.

4. **Reasoning-path / evidence interpretation visibility**
   - `ReasoningPathAudit` preserves evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and a read-only boundary.
   - The boundary explicitly says it records no facts, writes no event ledger, and does not mutate the cluster.

5. **Projection integrity / responsibility evaluation signals**
   - `ProjectionIntegritySummary` aggregates unsupported facts, conflicts, contradictions, graph issues, stale facts, recommendation counts, and capability states.
   - Its caveats preserve that integrity signals are not truth or correctness judgments and that refresh recommendations do not execute refresh or verification.

### Behavior-producing side

The behavior-producing side is also not one neighborhood. Implementation evidence supports these adjacent neighborhoods:

1. **Runtime decision routing**
   - `Runtime.__seed_arch__` says runtime routes validated model decisions to owner services without owning their behavior.
   - `_route()` turns validated decisions into answer, question, tool-need, registered tool call, state patch, refusal, or unsupported responses.

2. **Tool need / recommendation / capability resolution**
   - The `request_tool` branch records a tool need, computes provider recommendations, resolves capability, and returns metadata without invoking `ToolExecutor`.
   - This is behavior-adjacent because it produces operational response payloads, but it is not execution.

3. **Registered operation execution**
   - `ToolExecutor.__seed_arch__` owns `registered_tool_execution`, requires registered operations, evaluates policy, records tool-call events, invokes only registered implementations, and extracts post-execution knowledge only after a completed event.
   - This is the strongest implementation-backed execution neighborhood.

4. **Response behavior**
   - Runtime branches for `answer`, `ask_question`, and `refuse` append response events and return visible responses. These are behavior expressions, not permission determinations.

5. **State-patch mutation behavior**
   - Runtime has a `propose_state_patch` branch that applies a validated state patch or records rejection. This is mutation behavior, not permission grammar itself.

## Bridge responsibility

Implementation evidence supports a recurring narrow bridge responsibility:

> Preserve whether a bounded surface, question, observation domain, conclusion, recommendation, or operation may lawfully proceed to a next owner without pretending that this permission is itself planning, execution, routing, recommendation, or behavior selection.

The bridge owns constitutional permission-like decisions such as:

- whether bounded ask may execute now, execute after parameters, remain diagnostic-only, or remain not dispatchable;
- whether observation permission is granted, requires operator expression, denied, or unknown;
- whether an evidence path preserves unknowns instead of recording facts;
- whether an integrity signal is merely unsupported/stale/conflicted rather than false;
- whether a tool call is allowed, blocked, requires confirmation, or requires approval before registered execution.

The bridge does **not** own:

- planning;
- execution;
- runtime routing;
- provider recommendation;
- answer composition;
- semantic interpretation;
- behavior selection.

The strongest code evidence is negative as well as positive: bounded-work dispatch helpers explicitly say they do not decide lookup, eligibility, selection, evidence interpretation, answer composition, rendering, or semantic routing; runtime routing says it routes to owner services without owning their behavior; observation permission says it has no enforcement, approval storage, or runtime autonomy.

## Recurring handoff artifacts

Implementation evidence supports recurring handoff artifacts, but not a single universal schema.

Recurring shapes include:

- `eligible_now`
- `eligible_with_parameters`
- `diagnostic_only`
- `not_dispatchable`
- `unknown`
- `granted`
- `requires_operator_expression`
- `denied`
- `not_granted`
- `partially_observed`
- `observed`
- `unobserved`
- `missing_observation_domain`
- `missing_evidence_inside_observed_domain`
- `unsupported`
- `unverified`
- `stale`
- `provider_reported`
- `blocked`
- `require_confirmation`
- `require_approval`
- `completed`
- `failed`

These are not merely accidental local details, because they recur across independent surfaces that separate evidence, permission, and downstream action. They are also not yet a fully named constitutional grammar, because the implementation does not expose one shared `PermissionBridge` object, schema, CLI surface, or registry.

The smallest truthful classification is:

> The repository has recovered a recurring constitutional permission grammar pressure expressed through local implementation artifacts, not a stabilized first-class bridge identity.

## Neighbor boundary analysis

### Question Eligibility

Question Eligibility is the clearest bridge-adjacent implementation. It answers whether an exact registered question family may become bounded ask work. It does not own semantic routing or generic question answering. The artifact that crosses is a bounded eligibility result, not an answer.

### Observation Agreement / Observation Permission

Observation permission exposes whether an observation domain has reusable permission or needs operator expression. It is visibility only and explicitly not enforcement, approval storage, or runtime autonomy. The artifact that crosses is permission state and authority evidence, not an observation action.

### Pressure Visibility / Pressure Audit

Pressure surfaces expose missing evidence, capability pressure, ownership ambiguity, and domain gaps. They preserve pressure as diagnostic/evidential signal. The artifact that crosses is pressure classification or audit finding, not a command to repair the pressure.

### Responsibility Evaluation

Responsibility and integrity views distinguish unsupported, conflicted, stale, unknown, or candidate conditions from truth and repair. The artifact that crosses is responsibility/evidence status, not mutation.

### Behavior

Behavior receives constraints and may visibly answer, ask, refuse, record needs, call registered tools, or apply state patches. Behavior does not become proof that permission existed. Runtime only acts after decision validation and then delegates to owner services.

### Planning

Planning is not recovered as the owner of this bridge. Existing action-plan tests and recommendation paths may represent plans or handoff metadata elsewhere, but the permission artifacts reviewed here do not select plans. They preserve whether proceeding is lawful or blocked.

## Counterexamples

### Permission is not behavior

Observation permission reports are read-only, do not write the event ledger, do not mutate the cluster, and explicitly do not create runtime autonomy. Therefore permission-state visibility can exist without behavior.

Runtime response branches for `answer`, `ask_question`, and `refuse` are visible behavior events. They are separate from observation permission and bounded-work eligibility artifacts.

### Permission is not planning

Bounded-work eligibility decides `permitted` from exact implementation maps and required surface args. It does not create a plan, task graph, workflow, or route for arbitrary natural-language questions.

Projection integrity recommendations are inventory signals only. The implementation states that no refresh or verification is executed, which rejects interpreting recommendation pressure as a plan.

### Permission is not recommendation

The runtime `request_tool` branch can return provider recommendations and capability resolution without invoking `ToolExecutor`. Provider recommendation is metadata produced after a decision branch, while permission-like states such as eligible, diagnostic-only, unknown, require-operator-expression, blocked, or require-approval are gating/permission artifacts.

### Permission is not execution

`ToolExecutor` owns only registered tool execution after validation and policy checks. `request_tool` does not enter `ToolExecutor`; observation permission does not enforce permission; reasoning-path audit records no facts and performs no ledger mutation. These separate permission and evidence visibility from execution.

## Constitutional reliance

Future neighborhoods may lawfully rely on this recovered bridge pressure only in a narrow way.

They may rely on it to ask:

- Is this bounded question family eligible to proceed?
- Is this surface diagnostic-only or not dispatchable?
- Is this observation domain permission granted, unknown, or requiring operator expression?
- Is unknown preserved rather than promoted?
- Is a recommendation only a signal rather than execution?
- Is registered execution blocked, pending confirmation, pending approval, or allowed?

Future neighborhoods that may lawfully consume these artifacts include:

- Behavior, when deciding whether a visible response can honestly proceed.
- Execution, when preserving policy/registration/approval gates before registered operation invocation.
- Planning or coordination, if they treat these artifacts as constraints and not as plan selection.
- Future physiology, if it uses the artifacts as constitutional stop/proceed pressure and preserves unknowns.

They may **not** rely on this bridge as:

- a planner;
- a generic dispatcher;
- behavior selector;
- semantic router;
- recommendation ranker;
- approval store;
- execution engine;
- evidence-to-truth promoter;
- license to mutate cluster state;
- proof that a named constitutional bridge has already become stable repository knowledge.

## Lawful unknowns

The repository does not yet justify naming a stable first-class bridge as an implementation object. The recurring pressure is recovered; the stable identity is not.

Known unknowns:

- Whether future implementation should factor these local statuses into a shared artifact.
- Whether a shared artifact would improve visibility or over-compress distinct neighborhoods.
- Whether behavior, execution, planning, and coordination should consume the same permission status vocabulary or keep local grammars.
- Whether `permission to proceed` is the right stable name, or only the current investigation's best description of recurring pressure.

## Supported conclusions

Supported:

1. The repository contains repeated implementation-backed proceed/stop/unknown/blocked/diagnostic-only/eligibility artifacts.
2. These artifacts recur between evidence-producing surfaces and behavior-producing surfaces.
3. The recurring responsibility is narrower than planning, execution, routing, recommendation, or behavior selection.
4. The strongest current phrasing is constitutional permission to proceed, including permission to stop, preserve unknown, refuse, or remain diagnostic-only.
5. Evidence supports a bridge pressure or grammar, not a first-class bridge implementation.
6. Future behavior-producing neighborhoods may consume these artifacts only as constraints or handoff states.

## Unsupported conclusions

Unsupported:

1. The repository has internalized full Competency Interrogation methodology.
2. The repository has a named `constitutional permission bridge` implementation.
3. Eligibility, permission, or unknown status selects behavior.
4. Permission status is a planner.
5. Provider recommendation is execution or approval.
6. Diagnostic visibility mutates cluster truth.
7. All question families are executable.
8. Unknown means false, failed, or forbidden.
9. A generic semantic router is justified by the reviewed evidence.
10. A new schema, CLI surface, ledger event, or runtime behavior is justified by this investigation.

## Recommended next investigation

Investigate one narrow question without implementing anything:

> Across existing code paths, what minimum fields are actually needed for downstream owners to safely consume proceed/stop/unknown permission artifacts without collapsing them into behavior, planning, recommendation, or execution?

This should compare only existing artifacts and tests. It should not create a shared schema unless later implementation evidence requires one.

## Confidence

Medium-high confidence that recurring constitutional permission pressure has been recovered.

Low confidence that the bridge has earned a stable identity or should be named as a first-class architecture component.

The evidence is strongest for local implementation artifacts and boundary-preserving handoffs. It is weaker for any stronger architectural claim, because the repository currently keeps these decisions distributed across bounded surfaces rather than exposing a single bridge owner.
