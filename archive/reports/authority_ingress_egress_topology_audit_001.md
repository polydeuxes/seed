# Authority-Bearing Ingress / Egress Topology Audit 001

## 1. Bounded question

Are the special operator-input pipeline and the shell/process-output pipeline inverse directions of one constitutional authority boundary, with shell serving as one concrete realization of Seed-authority egress rather than as a tool Seed possesses?

## 2. Fixed distinctions preserved

This audit preserves the requested distinctions: ordinary observation is not operator authority-bearing input; operator claim is not operator instruction; operator instruction is not granted authority; granted authority is bounded; Seed-native intended movement is not ordinary observation; reachability is not selected realization; selection is not warrant; warrant is not authorization; authorized invocation is not emitted movement; emitted movement is not successful behavior; external behavior is not admitted Seed knowledge; shell is not Bash, not executable inventory, not capability, and not every external mechanism; external mechanism is not constitutional owner; and boundary translation is not internal constitutional transformation.

## 3. Methodology

I inspected implementation bodies and direct consumers, not symbol names alone. Read-only probes covered operator inquiry, observations, candidate realization, reachability, registry, validation/policy, execution, result recording, and evidence admission. The proving request was: “Search this repository for files containing story or stories.” The ordinary-observation control was: “/bin/bash exists at path /bin/bash.” The internal-only control was the candidate-realization-to-capability-reachability projection.

## 4. Inspected owners

- `seed_runtime.bounded_constitutional_question`: explicit operator inquiry to bounded constitutional question.
- `seed_runtime.constitutional_pipeline`: ordered read-only constitutional pipeline handoff.
- `seed_runtime.observations`: ordinary observation ingestion and fact promotion.
- `seed_runtime.repository_observation`: current read-only repository observation provider that uses subprocess internally for git.
- `seed_runtime.representation_grammar_recovery`: internal grammar recovery projection.
- `seed_runtime.candidate_operational_realization`: candidate operational realization projection.
- `seed_runtime.capability_reachability_projection`: demand-level reachability projection.
- `seed_runtime.registry`, `seed_runtime.models.ToolSpec`: registry/catalog metadata.
- `seed_runtime.tool_validation`, `seed_runtime.tool_execution_policy`, `seed_runtime.policy`: selected registered-operation validation and policy authorization.
- `seed_runtime.execution`: registered-operation realization, event recording, and post-execution evidence extraction.
- `seed_runtime.fact_extraction`: tool result evidence admission.
- Relevant tests under `tests/` for guardrails and counterevidence.

## 5. Current operator-ingress topology

`BoundedConstitutionalQuestion` is the explicit owner closest to operator ingress. Its module declares that it owns only the `Operator Inquiry -> BoundedConstitutionalQuestion` boundary, preserves caller inputs as evidence/testimony, and does not create authority, truth, capability, view selection, event-ledger writes, or mutation. Its artifact preserves exact inquiry text, provenance, bounded question, constitutional intent, scope status, uncertainty, unknowns, caller-supplied fields, and a testimony status stating that operator testimony is evidence, not established fact.

For the proving request, current explicit inputs would have to be supplied as separate fields:

- `operator_inquiry`: exact external sentence.
- `inquiry_provenance`: attribution such as `operator:<session>`.
- `bounded_question`: `identify repository files whose contents contain the bounded lexical alternatives story or stories`.
- `constitutional_intent`: read-only repository search.
- `scope_status`: current repository, read-only.
- `unknowns`/`uncertainty`: ambiguities such as lexical boundary policy.

Current code does **not** perform natural-language interpretation from the operator sentence to these fields. CLI parsing supplies explicit fields, and bounded-question production preserves them. Therefore CLI parsing and constitutional operator-input interpretation are not a complete separated pair: parsing exists, bounded-question preservation exists, but the interpreter that binds authority, scope, instruction/claim separation, and demand from raw operator text is missing or manual.

Exact responsibility making operator input constitutionally different from ordinary observation: it can carry an attributed request/permission/policy input that asks Seed to move, while ordinary observation reports a source-state claim that may become evidence/fact. The current bounded-question owner preserves this testimony boundary and refuses ordinary fact promotion.

## 6. Ordinary-observation control

Ordinary observations enter through `ObservationIngestor`. It appends `observation.observed`, converts the observation to provenance evidence, and may append `fact.observed` or `fact.inferred`. Thus `/bin/bash exists at path /bin/bash` establishes at most an attributed external observation/evidence/fact about mechanism existence if ingested through that path.

That is distinct from `operator says: use /bin/bash`, which is an instruction/request and not proof that `/bin/bash` exists. It is also distinct from `operator authorizes: execute a bounded local read-only process`, which is a possible authority grant and still not proof that `/bin/bash` exists. Current code partially preserves this distinction: observations and bounded operator inquiry have separate artifacts, but there is no full operator-authority artifact that binds “use” and “authorize” separately.

## 7. Current outward-movement topology

The modern projection road has an internal handoff sequence:

`ExaminationProbeRequest`/`OperationalRealizationHandoff` -> `CandidateOperationalRealizationSet` -> `CapabilityReachabilityProjection` -> `FutureOperationalRealizationSelectionHandoff`.

`CandidateOperationalRealizationSet` consumes observations, attributed claims, contracts, recovered grammars, behavioral observations, comparisons, and bases to produce possible candidates. It explicitly says candidates are not ranked or selected, mechanism existence is not reachability, grammar declarations are not behavioral competency, authority availability differs from policy authorization, and no registered-operation concept is required.

`CapabilityReachabilityProjection` consumes candidates and says reachability is not selection, mechanical reachability differs from dependency availability, authority availability, and policy authorization, and the artifact does not authorize, schedule, execute, or create pending actions.

The first current artifact on the outward path after a bounded demand is normally a handoff/probe request naming the exact capability demand and representation requirements. The first missing outward owner is after reachability: there is a future selection handoff, but no established owner for selecting a realization, warranting reliance, translating it into an exact process request, and handing it to authorization.

## 8. Shell/process boundary analysis

There is no general shell/process constitutional boundary owner. Current concrete process usage appears in specific providers, e.g. repository observation calls `subprocess.run([git, *args], cwd=cwd, text=True, capture_output=True, check=False)` and reads return code/stdout. That provider owns a bounded git observation implementation, not general Seed egress.

The legacy/current `ToolExecutor` owns registered-tool execution: validate registered operation and policy, append start/failure/completion events, load a registered callable, invoke it, validate output schema, then record and extract evidence. It does not expose argv, stdin, cwd, environment, executable resolution, timeout, cancellation, network/filesystem constraints, user identity, privilege, or general effect accounting as a constitutional local-process request. Shell therefore currently owns no complete egress boundary; process invocation is scattered beneath specific implementation owners or callable implementations.

Classification of shell/process responsibilities in current evidence:

- argv/cwd/stdout/return code: process-boundary implementation inside `repository_observation` for git only.
- stdin/environment/executable resolution/timeout/cancellation/effects/filesystem/network/user/privilege: not explicit in a shared boundary owner.
- authorization: policy service for registered operations, not process-boundary enforcement.
- result recording: `ToolExecutor` events and `FactExtractionService` evidence for registered tools; repository observation returns a typed observation object without ledger writes.
- admission: ordinary observation ingestion or tool-output evidence extraction depending on path.

Answer: shell is not the constitutional egress owner in current code. It is either absent as a general owner or compressed inside mechanism-specific code; a lawful topology would make it consume an already authorized egress request.

## 9. Shell-versus-Bash analysis

Current implementation does not establish Bash as the shell boundary. `/bin/bash` can be represented as a mechanism observation, an invocation contract, and a recovered grammar target. Bash belongs beyond the Seed egress boundary as one external language/executable ecosystem. A lawful road would be `SeedAuthorityEgress -> local process boundary -> /bin/bash`. Current code avoids “shell owns Bash grammar” in the newer realization/reachability projections, but older registered-operation vocabulary can still compress implementation binding, policy action, and execution.

## 10. Realization analysis

Current candidate/reachability code uses realization mainly as “candidate possible manner of satisfying a demand,” with explicit non-selection. `CandidateOperationalRealization` includes mechanism, contract, recovered grammar, accepted/produced representations, standings, basis, provenance, unknowns, conflicts, and selected=false in formatting. It does not include concrete argv/process request, authorization decision, pending action, or execution. `ToolExecutor._realize_registered_operation`, however, uses “realize” to mean executing a registered callable and validating output. Therefore the repository uses several realization meanings: the newer projection meaning is candidate manner; the legacy execution meaning is actual callable execution.

An abstract transformation is concretely realized only when a chosen manner has been translated into an exact external representation and emitted/executed. The current candidate projection is not that point. Concrete representation construction is missing between selection/warrant and egress, so it is not yet cleanly owned.

## 11. Warrant analysis

Warrant-like evidence is distributed across candidate standings, behavior comparisons, representation compatibility, method compatibility, dependency standings, authority standings, and reachability conclusion reason. The closest existing artifact to a warrant is `CapabilityReachabilityProjection`, because it aggregates whether at least one candidate supports the full exact demand under current mechanism, grammar, behavior, representation, method, dependency, and authority state. But it explicitly does not select or authorize and does not answer why Seed may rely on the selected realization preserving exact meaning across the concrete representations. Therefore selected-realization warrant is distinct and missing/compressed.

Warrant is distinct from authorization. Warrant asks whether the selected realization preserves the demanded meaning. Authorization asks whether this concrete invocation may be performed now under authority, policy, risk, scope, and effect constraints.

## 12. Authorization analysis

Current authorization for registered operations is established by `ToolExecutionPolicyService`: operation existence/status/input schema are validated first, then `PolicyGate` evaluates risk/approval/scope. `PolicyGate` allows L1 by default as “low-risk read-only action” unless an action-risk table blocks unknown actions; higher risk requires confirmation/approval or is blocked.

Before Seed may emit a concrete request across a local process boundary, the missing lawful road would require: bounded demand, selected realization, warrant, exact external representation, effect constraints, operator/standing authority scope, environmental availability, and constitutional authorization decision. Current code only establishes this for registered-tool calls in a legacy/catalog path, not for general local process egress.

## 13. Effect-constraint analysis

Effect constraints are compressed. `BoundedConstitutionalQuestion` has `read_only=True`, no ledger writes, and no mutation. `CandidateOperationalRealization` has dependency and authority standings but not detailed process effects. `PolicyGate` uses risk class and approval, but does not prove arbitrary commands are read-only. `RepositoryObservation` is a specific read-only provider but enforces only by hard-coded git commands and no mutation flags. Missing explicit constraints include filesystem scope, network prohibition, privilege prohibition, environment mutation prohibition, process count, timeout, output size, and allowed executable identity as first-class authorization/enforcement inputs.

## 14. Result-ingress topology

For registered tools, the first return artifact is the callable output dict, then `tool.call.completed` event, then `evidence.observed` with `kind=tool.output`. Recording and admission are distinct: `ToolExecutor._record_completed_tool_call` records completed execution without extracting knowledge; `_extract_post_execution_knowledge` separately calls `FactExtractionService.observe_tool_result`. The generic fact extractor records output as evidence only and intentionally does not infer facts.

For direct repository observation, subprocess stdout/status are implementation details converted into a `RepositoryObservation`; it does not enter through the generic `ObservationIngestor` unless a caller separately ingests an `Observation`. Successful exit status establishes only process completion under that provider’s checks, not demanded semantic success. Behavior comparison is owned in the candidate-realization path by `BehaviorComparison`, not by process execution itself.

## 15. Tool-registry analysis

| Registry material | Recovered responsibility |
| --- | --- |
| capability labels | claimed transformation relevance / candidate enumeration input |
| implementation binding | mechanism identity or callable binding |
| input/output schema | declared invocation contract |
| status | registration/executable-status claim in validation |
| examples | attributed examples/comparison material, not proof |
| policy action | authorization input |
| visibility | packaging/exposure policy |
| lookup by capability | candidate enumeration; can become hidden selection if direct consumer treats first/only result as chosen |

Registration currently implies existence in the catalog, status if `registered`, declared schemas, policy-action binding, and import/callable identity. In the legacy execution road, selected tool name plus validation plus policy can imply executable invocation. It does not by itself prove mechanism exists on disk, grammar recovered, behavioral compatibility, reachability, warrant, or authorization. Hidden implications remain where registry lookup by capability is used as operational candidate/selection material and where `risk_class=L1` plus policy default functions as standing read-only authorization.

## 16. Registry counterfactual

If `/bin/bash` is registered, that adds catalog identity, optional capability labels, declared schemas/contracts, implementation binding, policy action, status, visibility, version/provenance if present, and examples. If separately `/bin/bash` was observed, contract known, bounded Bash grammar recovered, behavior comparisons support the exact fragment, dependencies/authority available, demand reachable, realization selected, reliance warranted, and concrete request authorized, registration adds only implementation inventory/package exposure and references. Lawful residue is `ImplementationInventory`: identity, binding/location, declared contract references, namespace, version, provenance, and observed availability references.

## 17. Translation-versus-transformation classification

- Operator prose -> Seed-native demand: boundary translation plus authority binding; currently manual/partial.
- Candidate grammars -> grammar recovery: internal constitutional transformation.
- Candidate realizations -> capability reachability: internal constitutional transformation.
- Seed-native demand -> Bash/argv/process representation: outward boundary translation; owner missing.
- Process request -> external process behavior: external behavior; shared owner missing.
- stdout/stderr/status -> Seed result artifact: inward result translation; partial in registered-tool and repository-observation paths.
- Result artifact -> evidence/fact: knowledge admission; distinct in tool result and ordinary observation paths.

## 18. Future-egress-boundary analysis

Repository evidence supports a shared responsibility for outward authority-bearing movement because current projections explicitly separate reachability, selection, authorization, execution, and tool/provider concepts, and tests forbid collapsing candidates into execution decisions. However, evidence does not show an existing owner named `SeedAuthorityEgress`. A general abstraction is warranted as a recovered responsibility only if bounded to the shared handoff: selected/warranted realization plus authority/effect constraints to a concrete boundary request. Shell/local process should be one boundary realization, not the canonical constitutional owner.

## 19. Complete repository-search trace

| Arrow | Producer | Artifact | Consumer | Current status | Authority significance | Role | Owner exists? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Operator expression -> operator authority ingress | external operator / CLI | raw sentence | bounded-question producer | partial | may carry instruction/permission | inward translation | missing full ingress owner |
| authority ingress -> bounded constitutional demand | caller/manual parser | explicit `BoundedConstitutionalQuestion` fields | constitutional pipeline | partial | scope and testimony preserved, authority not fully bound | authority binding + translation | partial |
| demand -> grammar recovery/reuse | examination/projection inputs | representation grammar recovery inputs | grammar recovery | partial | none if internal only | internal transformation | established for grammar, not for search prose |
| grammar -> candidate operational realizations | probe handoff | `CandidateOperationalRealizationSet` | reachability | established | authority availability recorded, not policy authorization | internal transformation | established |
| candidates -> capability reachability | candidate set + future handoff | `CapabilityReachabilityProjection` | future selection | established | reachability distinct from authorization | internal transformation | established |
| reachability -> realization selection | reachability projection | `FutureOperationalRealizationSelectionHandoff` | missing selector | partial/missing | choosing one manner | internal/egress boundary | missing |
| selection -> warrant | missing selector | missing warrant | concrete translation | missing | reliance on exact meaning | warrant projection | missing |
| warrant -> concrete external representation | missing warrant | missing process request/Bash argv | authorization | missing | binds exact effectful request | outward translation | missing |
| representation -> authorization | missing request | missing authorization decision | process boundary | missing for general process | permission to emit now | authorization | missing/legacy registered-tool only |
| authorization -> local process egress | missing authorization | subprocess/callable invocation | external mechanism | compressed | should enforce scope/effects | boundary egress | missing/shared not established |
| egress -> external behavior | process implementation | process behavior | result capture | partial/scattered | no knowledge yet | external behavior | implementation-specific |
| behavior -> result observation ingress | process/callable | stdout/stderr/status or output dict | result recorder | partial | attribution only | inward result translation | partial |
| result -> comparison | result artifact | behavior comparison | reachability/candidate evidence | partial | supports/refutes warrant | internal transformation | established only as supplied comparison |
| result -> State/explanation | recorder/extractor | event/evidence/fact or answer | state projector/operator | partial | admission distinct from recording | recording/admission | partial |

## 20. Ownership matrix

| Responsibility | Current producer | Current artifact | Current consumer | Direction | Current status | Missing or compressed owner |
| --- | --- | --- | --- | --- | --- | --- |
| exact operator expression | CLI/caller | `operator_inquiry` | bounded question | ingress | established | raw-expression interpreter missing |
| operator attribution | CLI/caller | `inquiry_provenance` | bounded question/pipeline | ingress | partial | operator identity binding |
| operator authority grant | implicit/manual | none/fields | downstream manual reasoning | ingress | missing | authority-grant artifact |
| operator scope/constraints | CLI/caller | `scope_status`, uncertainty, fields | bounded question | ingress | partial | scope/constraint binder |
| constitutional interpretation | caller/manual | `bounded_question`, `constitutional_intent` | pipeline | ingress/internal | partial | natural-language interpreter |
| bounded capability demand | probe/request builders | capability identity/reference | candidate projections | internal | established for examination path | demand builder for repo search |
| candidate realization | projection inputs | `CandidateOperationalRealizationSet` | reachability | internal | established | none |
| capability reachability | reachability projection | `CapabilityReachabilityProjection` | future selection | internal | established | none |
| realization selection | none/future handoff only | `FutureOperationalRealizationSelectionHandoff` | missing | internal | missing | selection owner |
| realization warrant/reliance | standings/reasons partial | no selected warrant | missing | internal/egress | missing | operational realization warrant |
| outward representation translation | none | none | authorization/process | egress | missing | selected-to-concrete request translator |
| concrete egress request | ToolExecutor args in legacy path | tool name + args | policy/executor | egress | compressed | general egress request |
| constitutional authorization | policy service for tools | `PolicyDecision` | ToolExecutor | egress | partial | general egress authorization |
| process-boundary enforcement | subprocess/callable code | invocation | external process/callable | egress | compressed | local process boundary owner |
| external behavior | OS/callable | behavior/output | capture | external | partial | effect account |
| result capture | subprocess/callable | stdout/output/return code | recorder/provider | ingress | partial | general result artifact |
| result observation | extractor/provider | evidence or observation object | state/admission | ingress | partial | result-observation ingress |
| behavior comparison | supplied comparison | `BehaviorComparison` | candidate projection | internal | partial | comparison generation owner |
| recording | ToolExecutor/ObservationIngestor | events | state projector | internal | established | none for direct process effects |
| knowledge admission | FactExtraction/ObservationIngestor | evidence/fact events | state | internal | established/partial | semantic fact mapping for results intentionally absent |
| implementation inventory | registry/toolkit manifest | `ToolSpec` | validation/recommendation | support | compressed | purified inventory after warrant separation |

## 21. Exact first mismatch

The first mismatch is that ingress has a bounded-question artifact preserving operator testimony and scope fields, while egress stops at reachability/future-selection handoff and lacks an owner that takes a reachable candidate, selects it, warrants reliance, translates it into concrete external representation, and hands it to authorization. The earliest missing producer is an operational realization warrant/selection-to-egress producer; the earliest missing artifact is a selected-realization warrant or handoff to concrete egress translation.

## 22. Strongest supporting evidence

- Bounded question explicitly refuses observation/fact promotion, capability discovery, authority creation, ledger writes, and mutation.
- Candidate realization explicitly refuses ranking/selection and separates mechanism existence, grammar declaration, behavioral support, authority availability, and registered-operation concepts.
- Reachability explicitly refuses selection, authorization, scheduling, execution, pending actions, and tool/provider concepts.
- Tool execution policy explicitly separates registered-operation validation from policy authorization.
- Tool execution explicitly separates execution recording from post-execution evidence extraction.

## 23. Strongest counterevidence

- `ToolExecutor` is an existing owner labelled `registered_tool_execution` and performs validation, policy, realization, recording, and evidence extraction in one operational road.
- `PolicyGate` can authorize L1 read-only actions from manifest risk class, so a context-free standing authorization exists for some registered operations.
- `repository_observation` directly uses subprocess and return codes lawfully for a read-only observation provider, which weakens the claim that all process egress needs a new general owner before any process use.
- `OperationSelectionResult` already names selected registered operations for call-tool decisions, so selection is not entirely absent in the old road.
- Registry tests and capability verification invariants characterize `ToolSpec.capabilities` as inert discovery metadata in newer slices, so the registry is not primarily warrant in all contexts.
- Result material from tools already follows an evidence pipeline, though not the ordinary `ObservationIngestor` pipeline.

## 24. Supported conclusions

1. Operator input is not ordinary observation because it may carry attributed instruction, bounded permission, and policy/scope material; current code preserves it as testimony rather than fact.
2. Current operator authority ingress owns exact inquiry preservation and provenance/scope testimony, but not full identity, authority-grant, or instruction/claim separation.
3. Seed-originated external movement requires inverse responsibilities: demand preservation, representation translation, effect constraints, warrant, authorization, egress, and result ingress.
4. Shell is not the egress owner; current code has specific subprocess/callable implementations and legacy registered-tool execution.
5. The old registry mixes implementation inventory with standing validation/authorization inputs and potential context-free warrant-like implications.
6. Lawful implementation inventory remains after separation: identity, location/binding, declared contracts, namespace, version/status/provenance, visibility, and observed availability references.
7. Current realization meaning is split: candidate possible manner in newer projections, actual callable execution in `ToolExecutor`.
8. The first missing owner is operational realization warrant / selected-realization-to-concrete-egress handoff.

## 25. Unsupported conclusions

- That the operator and Seed are equivalent authorities.
- That shell owns Bash grammar.
- That registration alone proves reachability, warrant, or authorization.
- That successful exit status proves demanded success.
- That every internal projection is egress.
- That a broad registry removal is warranted.
- That one existing owner already unifies both ingress and egress directions.

## 26. Boundary-symmetry classification

B. Operator ingress and Seed egress are inverse directions of one authority-bearing constitutional boundary family.

## 27. Shell-role classification

5. Shell currently compresses egress, authorization, execution, and result-ingress responsibilities.

## 28. Registry classification

II. The registry mixes implementation inventory with context-free operational warrant.

## 29. Realization classification

δ. The repository uses several distinct lawful realization meanings.

## 30. First-missing-boundary classification

d. Operational realization warrant is missing.

## 31. Exact next bounded boundary

Responsibility to recover: operational realization warrant for one selected reachable realization before concrete egress translation.

Current missing/compressed owner: reachability conclusion plus legacy tool validation/policy/execution.

Producer: future realization selection owner consuming `CapabilityReachabilityProjection.future_selection_handoff` and the selected candidate.

Input artifacts: bounded demand reference, selected candidate, recovered grammar/contract references, behavior comparisons, authority/dependency standings, effect constraints, provenance, unknowns/conflicts.

Output artifact or handoff: `OperationalRealizationWarrant` or equivalent selected-realization reliance handoff.

Immediate consumer: concrete egress representation translator / authorization decision.

Manual responsibility eliminated: ad hoc human assumption that a supported reachable candidate preserves exact demanded meaning when translated outward.

Compatibility treatment: keep registry and `ToolExecutor` compatibility as legacy registered-operation execution; do not remove registry fields.

Explicit exclusions: no source/test/registry/policy/execution changes in this audit; no broad egress framework; no shell implementation; no authorization rewrite.

## 32. Implementation-warrant decision

One bounded implementation slice is warranted.

## 33. Files changed

- `authority_ingress_egress_topology_audit_001.md` only.

## 34. Probes executed

- `find .. -name AGENTS.md -print`
- `cat AGENTS.md`
- `git status --short`
- `rg -n "operator.*input|operator.*authority|authority.*operator|inquiry.orientation|bounded.*question|operator.*request|operator.*instruction|operator.*claim" seed_runtime tests scripts campaigns || true`
- `rg -n "shell|subprocess|Popen|run_process|stdout|stderr|exit_status|returncode|cwd|environment|argv|stdin" seed_runtime tests scripts || true`
- `rg -n "CandidateOperationalRealization|CapabilityReachabilityProjection|OperationalRealizationSelection|realization|realized" seed_runtime tests || true`
- `rg -n "class ToolRegistry|ToolSpec|registered.operation|policy_action|subprocess|Popen|execution" seed_runtime scripts tests | head -300`
- `rg -n "Observation\(|Evidence\(|Fact\(|fact_extraction|tool.call.completed|stdout|stderr|returncode" seed_runtime tests | head -200`
- `rg -n "external material|Testimony|claim|instruction|operator" seed_runtime tests | head -200`
- `sed` inspections of the implementation files listed in methodology.
- `pytest -q tests/test_constitutional_pipeline.py tests/test_candidate_operational_realization.py tests/test_capability_reachability_projection.py tests/test_registry.py tests/test_tool_execution_policy.py tests/test_execution_proposals.py tests/test_observation_permission.py` -> 72 passed.

## 35. Confidence statement

Confidence is moderate-high for the audited bounded question. The evidence is strong that newer constitutional projections separate candidate realization and reachability from selection, authorization, and execution, and that operator inquiry is not ordinary observation. Confidence is lower on future naming because no existing general `SeedAuthorityEgress` owner is present; the conclusion is about recovered responsibility, not an already implemented abstraction.
