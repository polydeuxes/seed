# Operational Realization Topology Audit 001

## 1. Bounded question

Given one bound `ExaminationProbeRequest`, can Seed's existing capability, provider, tool-registry, and registered-operation owners project zero or more candidate operational realizations without selecting, authorizing, or executing one--or is a distinct composition owner missing?

Answer: the inspected implementation has separate owners for capability requests/projections, advisory provider recommendations, registered operation inventory, named-operation validation, policy authorization, and concrete proposal generation. It does not have an owner that composes one probe request plus State into a candidate provider/tool/registered-operation realization set.

## 2. Working distinctions

The audit tested these as orientation, not as repository ontology:

- capability: a requested or projected transformation/result, with verification status and reachability evidence kept separate.
- tool: a concrete registered operation record in current `ToolSpec` vocabulary; the registry calls these tools but architecture comments identify the owner as a registered-operation catalog.
- provider: an advisory source/runtime/backend recommendation, not necessarily a registered tool and not selected by recommendation.
- registered operation: one exact callable boundary exposed by a toolkit/registry and resolvable by operation name.

Preserved distinctions: registered tool is not projected capability; projected capability is not selected provider; selected provider is not selected operation; registered operation is not a valid operation call; valid operation call is not policy authorization; policy authorization is not execution; candidate realization is not selected realization; representation compatibility is not methodological compatibility; methodological compatibility is not operational realizability; tool availability is not operation reachability; operation reachability is not operation permission; provider recommendation is not provider selection; deterministic enumeration is not lawful selection.

## 3. Methodology

Read-only probes and implementation inspection were used. The audit did not change source, tests, campaigns, diagnostics, policies, registries, action plans, execution proposals, or execution internals. It inspected only the requested neighborhoods: probe handoff, capability inventory/projection, tool needs and capability resolution, provider recommendation, registry, operation selection/validation, execution proposal boundary, and direct tests.

Commands/probes executed are listed in section 32.

## 4. Inspected owners

- `seed_runtime/examination_probe_request.py`: `ExaminationProbeRequest`, `OperationalRealizationHandoff`, binding checks, formatting.
- `tests/test_examination_probe_request.py`: direct proof that bound requests preserve identities/constraints and omit provider/tool/operation/execution fields.
- `seed_runtime/capability_inventory.py`: State-derived read-only capability verification inventory.
- `seed_runtime/single_capability_state_projection.py`: one-capability read-only composition of requested needs, catalog metadata, provider recommendations, registered operation associations, evidence, inventory status, and Unknowns.
- `seed_runtime/capability_catalog.py`: static capability metadata and advisory provider/handoff recommendations.
- `seed_runtime/tool_recommendations.py` and `seed_runtime/recommendation_ranker.py`: ranked provider recommendation for an existing `ToolNeed` and current State.
- `seed_runtime/tool_needs.py`: `ToolNeedService` and read-only capability resolution payload.
- `seed_runtime/registry.py`: toolkit manifest loading, `ToolRegistry`, model-visible operation listing, capability mapping.
- `seed_runtime/tool_validation.py`: named operation selection and registered-tool input/output schema validation.
- `seed_runtime/tool_execution_policy.py`: selected registered operation validation followed by policy authorization.
- `seed_runtime/execution_proposals.py`: legacy/experimental concrete-call proposal from accepted `ActionPlan` and State.
- Direct tests: `tests/test_tool_recommendations.py`, `tests/test_tool_validation.py`, `tests/test_capability_inventory.py`, `tests/test_single_capability_state_projection.py`.

## 5. Current probe-request handoff

Implementation-backed road verified:

```text
ExaminationWorkSelection
-> FutureProbeRequestHandoff
-> ExaminationProbeRequest
-> OperationalRealizationHandoff
```

`bind_examination_probe_request` requires matching selection, handoff, frontier, work set, and method applicability; verifies inquiry reference equality; verifies artifact identity/hash; verifies candidate work identity; verifies contract/capability consistency; rejects non-applicable or conflicting method applicability; then returns a read-only bound request with no event-ledger write and no cluster mutation.

The bound request preserves:

- inquiry identity through `inquiry_reference` and handoff `inquiry_identity`.
- exact artifact identity/version/hash through `artifact_identity` and `artifact_hash`.
- selected candidate-work identity via `selected_work_reference` and `candidate_work_reference`.
- work-contract identity via `work_contract_reference`.
- capability identity via `capability_identity`.
- input/output representations via `required_input_representation` and `requested_output_representation`.
- method applicability via `method_reference` and `method_applicability_reference`.
- fidelity, attribution, and claim-treatment constraints.
- selection reason.
- provenance and Unknowns.

The `OperationalRealizationHandoff` intentionally narrows the request to: probe request ID, inquiry identity, artifact identity/hash, work contract, capability identity, required input representation, requested output representation, method-constraint reference, and read-only/no-ledger/no-mutation flags. It does not include selected provider, selected tool, selected registered operation, operation arguments, execution proposal, policy authorization, pending-action state, or execution state.

Direct tests confirm the JSON/handoff omits provider/tool/operation/authorization/pending/execution vocabulary and remains read-only.

## 6. Capability ownership analysis

Capability is represented by several distinct artifacts and stages, not one concept:

| Neighborhood | Capability meaning | Producer | Evidence/status | Direct consumers | Exclusions |
| --- | --- | --- | --- | --- | --- |
| Probe request | Required capability for selected examination work | `bind_examination_probe_request` | Bound from candidate work and method applicability | Future operational realization handoff | No provider/tool/operation/arguments/authorization/execution |
| Tool need | Caller/requested missing capability | `ToolNeedService.create_from_decision` | Demand only | provider recommendation, capability resolution, State projection | Demand does not prove availability |
| Capability catalog | Known capability metadata | catalog YAML / `CapabilityCatalog` | Static metadata and advisory recommendations | recommendation/ranking, tool need resolution, single capability projection | Does not execute or verify |
| Capability inventory | State-derived verification belief | `build_capability_inventory(state)` | `verified`, `unverified`, `stale`, `provider_reported`, `unknown`; union of registered tool capability labels, ToolNeeds, and capability verification facts | inventory CLI/tests, single capability projection | Does not verify, select, authorize, or execute |
| Registered operation contract | Capability labels on `ToolSpec` | toolkit manifests and registry/state | Contract metadata only | registry lookup, inventory universe, capability resolution | Not admitted knowledge and not current reachability |
| Single capability projection | Read-only composition for one normalized capability string | `build_single_capability_state_projection` | requested, catalog-known, advisory providers, registered operation associations, candidate evidence, verification status, Unknowns | CLI/reporting | Explicitly no provider/operation selection, no verification, no authorization/execution |

Answer: capability is a caller request, static catalog metadata, State-derived projection, verification subject, and operation-contract label through separate artifacts. The repository deliberately separates these stages.

## 7. Tool ownership analysis

The registry owner stores toolkit packages and `ToolSpec` records. In code, `ToolSpec` fields include toolkit ID, operation name, summary, input schema, output schema, policy action, implementation, status, visibility, risk class, capabilities, and examples. `ToolRegistry` exposes tools by exact name and lists tools for a capability by matching normalized `ToolSpec.capabilities`.

Tool identity in current code is mostly `ToolSpec.name`; provider identity is not a first-class field on `ToolSpec`. Toolkit identity (`toolkit_id`) is distinct from the registered operation name. Registration can be static/dynamic in memory from manifests or programmatic `Toolkit` construction and can be projected into State through events. Status and visibility decide model visibility; they do not prove dependency availability, provider availability, operation permission, or execution success.

A registered tool/operation establishes only possible operation metadata: name, toolkit package, schemas, policy action, implementation string, visibility/status, and declared capability labels. It provides evidence toward capability inventory as contract metadata but does not establish current capability reachability.

## 8. Provider ownership analysis

Provider has multiple implementation-backed meanings:

- Catalog/recommendation provider: `CapabilityRecommendation.provider` identifies a suggested provider/source for a capability; recommendations are advisory and unselected.
- Ranked recommendation provider: `RankedRecommendation.provider` is scored against current State by recommendation ranking.
- Handoff provider: catalog recommendation can carry backend type/operation for external handoff candidates.
- Action plan provider: legacy `ActionPlan.provider` names a proposed plan provider.
- Execution proposal provider: `ExecutionProposal.provider` is copied from an accepted action plan.
- Observation provider/source type: elsewhere in State/evidence, provider can mean observation source type; this audit did not treat observation providers as operational realizations.

Provider is distinct from tool in recommendation and action/proposal neighborhoods: catalog recommendations name providers without requiring registered `ToolSpec` records, while registry records operations without provider fields. One provider can plausibly expose multiple operations via catalog metadata or action/proposal conventions, but current registry does not model provider-to-many-tools directly. Multiple providers can be recommended for one capability; recommendation preserves non-selected alternatives and ranks them. Provider recommendation requires a formed `ToolNeed`; it does not consume an `ExaminationProbeRequest` directly.

## 9. Registered-operation ownership analysis

Registered operation identity is `ToolSpec.name`, indexed by `ToolRegistry`. Relationship to toolkit/provider:

- toolkit relation: `ToolSpec.toolkit_id` points to containing toolkit.
- provider relation: absent in registry; providers appear in catalog/recommendation/action-plan neighborhoods.
- capability relation: `ToolSpec.capabilities` labels operation contract associations.

Operation selection currently consumes an already named operation string from a `call_tool` decision. It resolves registry then optional State tools by exact name. It does not rank alternatives, consume capability identity as a starting point, inspect provider recommendations, compare representations, or evaluate methodological constraints.

Operation validation checks existence, registered status, and input schema. Output schema validation exists separately. The policy service separates validation from authorization and only evaluates policy after a selected operation call is valid.

Answer: current registered-operation selection cannot begin from an abstract capability request; it starts from an already named operation.

## 10. Existing capability-to-provider road

Implemented road for tool needs:

```text
request_tool Decision
-> ToolNeed
-> catalog provider recommendations ranked against State
-> ToolNeedService.resolve_capability
-> read-only capability_resolution payload
```

Stages:

| Stage | Producer | Artifact | Consumer |
| --- | --- | --- | --- |
| Request missing capability | decision producer | `Decision(kind="request_tool", tool_need={...})` | `ToolNeedService.create_from_decision` |
| Persist/request need | `ToolNeedService` | `ToolNeed` event/State object | recommendation service, capability resolution |
| Static recommendations | `CapabilityCatalog` | `CapabilityRecommendation` list | ranking/resolution |
| Ranked provider recommendations | `ToolRecommendationService` / ranker | `RankedRecommendation` list | runtime response, resolution payload |
| Registered operation candidates | `ToolRegistry.list_tools_for_capability` | visible `ToolSpec` payloads | capability resolution payload |
| Handoff candidates | catalog recommendations with backend/operation | provider/backend/operation metadata | runtime response |

What causes candidates to appear:

- Provider recommendations appear when the catalog has an entry for `ToolNeed.capability` and ranking runs.
- Registered operations appear when `ToolRegistry` has model-visible registered tools whose `capabilities` include the requested capability.
- Handoff candidates appear when catalog recommendations include backend type or operation metadata.

Multiple provider recommendations are preserved in ranked order. The ranking does not lawfully select one provider. Artifact identity, artifact hash, input/output representation, work-contract identity, method applicability, fidelity constraints, attribution constraints, and claim-treatment constraints are not part of `ToolNeed`/provider recommendation inputs. Methodological constraints therefore do not survive this road except as unstructured text if manually encoded in summaries, which would misclassify them.

## 11. Probe-request compatibility matrix

| Required information | Probe handoff provides it | Existing owner requires it | Existing owner can derive it | Missing handoff |
| --- | ---: | ---: | ---: | --- |
| probe-request identity | yes | no current owner | no | none in handoff; missing consumer |
| inquiry identity | yes | no current capability/provider/registry owner | no | none in handoff; missing consumer |
| artifact identity/version | yes | no current tool-need/provider/registry owner | no | none in handoff; missing consumer |
| capability identity | yes | capability inventory/projection and registry capability lookup can consume normalized string | yes, through adapter | `ToolNeed` object if using tool-need road |
| work-contract identity | yes | no current capability/provider/registry owner | no | none in handoff; missing consumer |
| required input representation | yes | no current owner | no | representation compatibility owner |
| requested output representation | yes | no current owner | no | representation compatibility owner |
| methodological-constraint reference | yes | no current owner beyond probe binding | no | constraint compatibility owner |
| fidelity constraints | no in narrow handoff; yes in full probe request | no current provider/tool/operation owner | no | if only handoff consumed, these are missing |
| attribution constraints | no in narrow handoff; yes in full probe request | no current provider/tool/operation owner | no | if only handoff consumed, these are missing |
| claim-treatment constraints | no in narrow handoff; yes in full probe request | no current provider/tool/operation owner | no | if only handoff consumed, these are missing |
| current capability status | no | inventory/projection produces it from State | yes from State/projection | needs State/projection input |
| provider candidates | no | provider recommendation produces from ToolNeed/catalog/State | only via adapted ToolNeed lacking artifact/constraints | candidate composition artifact |
| tool candidates | no | registry produces by capability string | yes via capability string | candidate composition artifact |
| registered-operation candidates | no | registry/capability resolution produces by capability | yes by capability only | candidate composition artifact |
| required operation arguments | no | operation validation/execution proposal requires arguments | no | later argument construction |
| authority requirements | no | registry has policy action/risk; policy later needs State | partial | candidate should surface requirements, not authorize |
| provenance | no in narrow handoff; yes in full probe request | no current owner | no | candidate composition provenance |

First exact mismatch: `OperationalRealizationHandoff.capability_identity` is only a string plus artifact/representation/method reference, while existing provider recommendation starts from a `ToolNeed` (`id`, `name`, `summary`, `capability`, `reason`, optional desired inputs/outputs) and existing registry lookup returns operations by capability without preserving artifact identity, representation requirements, method constraints, or provenance. A narrow adapter can expose the capability string, but it cannot compose provider/tool/operation candidates with probe-specific compatibility without taking on new responsibility.

## 12. Tool-versus-capability reconciliation

Implementation evidence supports orthogonal dimensions with inconsistent naming:

- Capability can be requested (`ToolNeed`), catalog-known (`CapabilityCatalog`), State-projected (`CapabilityInventoryEntry`), or operation-contract metadata (`ToolSpec.capabilities`).
- Tool/registered operation is concrete registry metadata (`ToolSpec`) with schemas/policy action/implementation/status/visibility.
- Provider is advisory/ranked/legacy proposal metadata and not a field of registry operations.

One tool can support several capabilities because `ToolSpec.capabilities` is a list. One capability can have several provider/tool realizations because a catalog entry can hold multiple provider recommendations and a registry can list multiple tools for the same capability. Current code does not reconcile those into candidate realizations.

## 13. Shell/Bash classification test

No shell/Bash concepts were added. Under current repository evidence, the orientation is coherent with caveats:

| Example | Current-evidence classification | Caveat |
| --- | --- | --- |
| local command execution | capability or requested transformation | only if represented as ToolNeed/catalog/inventory/ToolSpec capability label |
| shell adapter | toolkit/tool mechanism | current registry would represent callable boundaries as `ToolSpec`, not a separate adapter ontology |
| `/bin/bash` | provider/runtime/dependency | current registry has no provider/runtime field; dependency availability would need State/evidence outside ToolSpec |
| Bash-language competency | separate grammar/capability knowledge | no inspected owner maps grammar competency to operational realization |
| `shell.run` | registered operation name | if registered as `ToolSpec.name`; validation starts from this exact name |

Repository vocabulary agrees that exact callables are registered operations, capability labels are separate metadata, and provider/runtime is not currently modeled inside the registry. It differs by calling registered operation records "tools" in model names.

## 14. State-projection analysis

Current State can establish or expose:

- registered tools/operations from projected tool registration events.
- capability verification facts and freshness/staleness through capability inventory.
- ToolNeeds as requested demand.
- provider-reported capability state when `capability_verified` support uses provider-reported values.
- registered operation status/visibility if `ToolSpec` is present in State.
- facts that recommendation ranking may use to prefer providers (for example runtime facts).

Current State/projections do not by themselves prove:

- provider availability as selected operational runtime.
- dependency availability for a registered operation unless separately represented by facts/preconditions.
- artifact representation presence, except in examination artifacts outside capability/tool State projections.
- authority reachable; policy authorization remains downstream.
- operation permission; validation and policy are separate.
- capability currently reachable as operationally executable; inventory explicitly separates registered operation contract metadata from admitted capability knowledge and verification.

Operational-realization enumeration should consume existing capability/tool projections rather than bypassing them, and should use State only through those owners plus any explicitly needed current-State facts. It should not treat registered mechanism as currently reachable capability.

## 15. Realization-constraint compatibility

Existing provider/tool records cannot express probe methodological constraints in a structured way. Registry schemas can express operation argument shape and output JSON shape, not artifact representation compatibility, exact material preservation, provider attribution, no semantic promotion, span preservation, raw-byte fidelity, or claim-treatment constraints. Putting those into operation arguments would misclassify request constraints as call parameters and would lose compatibility provenance.

A separate realization-constraint compatibility result is needed if candidates are to preserve why an operation/provider/tool is compatible, incompatible, or Unknown with respect to representation and methodology. Incompatible candidates should remain preserved as candidates with compatibility status when the question is enumeration and traceability; omitting them would hide why no lawful realization exists.

## 16. Multiple-realization behavior

Lawful candidate enumeration behavior should be:

- capability has no provider: produce zero provider-backed candidates or a no-provider Unknown/blocker, not a selected fallback.
- provider has no matching registered operation: preserve provider recommendation and missing operation relation separately.
- several providers realize same capability: preserve all ranked/advisory alternatives, selected false.
- one tool exposes several matching operations: preserve all matching operation records, selected false.
- provider stale/unavailable: preserve status evidence and Unknown/unavailable marker.
- operation arguments cannot yet be formed: preserve candidate with argument requirements Unknown, not invalid execution.
- authority unavailable: preserve authority requirement/downstream authorization Unknown; do not authorize.
- methodological constraints incompatible: preserve incompatibility reason.
- representation compatibility Unknown: preserve Unknown rather than omit.

The stage must preserve zero or more candidates and Unknowns, and must not arbitrarily select one.

## 17. Execution-proposal boundary

Current `ExecutionProposal` requires an `ActionPlan`, provider, tool name, concrete tool arguments, fingerprint, risk class, and preconditions that make a plan ready. It is explicitly experimental and outside the core path; it is not executable by itself and never grants authorization.

The evidence supports a future road shaped like:

```text
ExaminationProbeRequest
-> CandidateOperationalRealizationSet
-> OperationalRealizationSelection
-> concrete ExecutionProposal or equivalent downstream concrete-call proposal
```

Existing action-plan/proposal artifacts are constitutional/implementation precedent for keeping concrete calls downstream, but they do not cover candidate realization enumeration for probe requests.

## 18. Baseline tool-validation failures

`pytest -q tests/test_tool_validation.py` is not green on this commit. Observed result: 4 failed, 5 passed.

Failures reproduced:

1. `test_runtime_still_rejects_unknown_tool_during_decision_validation`: expected `response.kind == "invalid_decision"`; observed `"unsupported"`.
2. `test_runtime_still_rejects_invalid_input_schema_before_execution`: expected `"invalid_decision"`; observed `"unsupported"`.
3. `test_runtime_still_rejects_unregistered_tool_status_before_execution`: test attempted `runtime.tool_intent_guard.validate`, but `Runtime` has no `tool_intent_guard` attribute.
4. `test_runtime_still_rejects_invalid_output_schema_after_start`: expected `"tool_failed"`; observed `"unsupported"`.

Interpretation: shared `ToolValidationService` unit boundaries pass in the same file, and the failing cases are runtime integration expectation mismatches/drift around current unsupported runtime behavior and removed/changed `tool_intent_guard`. They do not prove the registry/operation-selection owner is unusable for read-only enumeration, but they reduce confidence in reusing the runtime execution path as evidence. This seam should not claim tool-validation road is green.

## 19. Direct composition trace

Using the bound request shape from `tests/test_examination_probe_request.py` scenario:

```text
OperationalRealizationHandoff(
  probe_request_id=..., inquiry_identity=..., artifact_identity="artifact", artifact_hash="h",
  work_contract_reference="struct", capability_identity="cap-struct",
  required_input_representation="exact_text",
  requested_output_representation="structural_projection",
  method_constraint_reference={...}
)
```

Trace attempt:

1. First existing owner that can consume any part: capability inventory/projection or registry can consume the normalized `capability_identity` string; provider recommendation cannot consume the handoff directly because it expects `ToolNeed`.
2. First required adapter: handoff capability string to either a synthetic `ToolNeed` for provider recommendation/capability resolution or direct `capability_name` for `SingleCapabilityStateProjection`/registry lookup.
3. First genuinely missing responsibility: composition of the probe reference, capability status, provider recommendations, tool/operation candidates, representation compatibility, methodological compatibility, authority requirements, argument requirements, provenance, and Unknowns into candidate realizations.
4. First field/artifact mismatch: provider recommendation requires `ToolNeed` and loses artifact identity, exact representations, method reference, constraints, and provenance; registry lookup returns tools by capability without provider relation or representation/method compatibility.
5. Existing owners cannot be composed without transferring new responsibility into the adapter. If the adapter merely creates a `ToolNeed`, it loses probe constraints; if it preserves them and correlates providers/tools/operations, it becomes the missing candidate-realization composition owner.

## 20. Exact first mismatch

The first exact mismatch is between `OperationalRealizationHandoff` and the `ToolNeed`-centered provider recommendation/capability resolution road: the handoff has `probe_request_id`, `inquiry_identity`, artifact identity/hash, work contract, representation requirements, and method reference, but provider recommendation consumes a `ToolNeed` with capability/name/summary/reason and no artifact/method/representation constraint slots. Direct registry lookup can use only the capability string and therefore cannot preserve the rest of the handoff.

## 21. Ownership matrix

| Responsibility | Producer | Artifact | Consumer | Current status | Reuse status | Missing handoff |
| --- | --- | --- | --- | --- | --- | --- |
| required capability preservation | probe binding | `ExaminationProbeRequest` / `OperationalRealizationHandoff` | future realization owner | implemented | directly reusable | none |
| capability-state projection | capability inventory / single capability projection | `CapabilityInventoryEntry`, `SingleCapabilityStateProjection` | CLI/reporting/future owner | implemented read-only | reusable through narrow adapter | probe-to-capability string normalization |
| provider inventory | capability catalog | `CapabilityRecommendation` | ranking/resolution | static advisory | implementation precedent | probe-specific constraints |
| provider recommendation | recommendation service/ranker | `RankedRecommendation` list | runtime request_tool response | implemented for `ToolNeed` | reusable through narrow adapter for advisory providers only | ToolNeed adapter; artifact/constraints absent |
| tool registration | toolkit manifest / registry | `Toolkit`, `ToolSpec` | registry/state/validation | implemented | directly reusable as operation inventory | provider relation absent |
| operation registration | registry | `ToolSpec` indexed by name/capability | selection/validation/resolution | implemented | directly reusable | no probe compatibility |
| operation selection | `ToolValidationService.select_operation` | `OperationSelectionResult` | validation/runtime | implemented for named operation | wrong responsibility for candidates | selected operation name |
| operation validation | validation service / policy service | `ToolValidationResult`, `RegisteredOperationValidationResult` | policy/execution path | implemented but runtime tests failing | reusable after selection/arguments | operation name and args |
| representation compatibility | none in inspected owners | absent | future realization owner | absent | absent | accepted/produced representation result |
| methodological-constraint compatibility | method applicability only pre-probe; no realization check | absent | future realization owner | absent | absent | constraint compatibility status |
| candidate realization enumeration | none | absent | future selection owner | absent | absent | `CandidateOperationalRealizationSet` or equivalent |
| realization selection | none | absent | execution proposal / action plan | absent | absent | selected candidate artifact |
| argument construction | execution proposal special case | `tool_arguments` | execution proposal/validation | legacy/specialized | legacy/specialized | concrete args |
| execution proposal | `ExecutionProposalService` | `ExecutionProposal` | downstream policy/execution side path | experimental outside core | constitutional precedent | selected provider/tool/operation + args |
| policy authorization | `ToolExecutionPolicyService` / `PolicyGate` | `PolicyDecision`, `ToolExecutionPolicyResult` | execution path | implemented downstream | authority-bearing and downstream | valid selected operation call |
| execution | runtime/tool executor | tool call events/results | runtime | implemented elsewhere | authority-bearing and downstream | authorization and concrete call |

## 22. Strongest supporting evidence

- `OperationalRealizationHandoff` preserves capability and representation fields but no provider/tool/operation/args/authorization/execution fields.
- Capability inventory explicitly separates admitted capability knowledge, registered operation contract metadata, and requested capabilities, and states that registered operation contract metadata does not verify existence/select/authorize execution.
- Single capability projection explicitly marks provider recommendations advisory, registered operations as contract associations, and no provider/operation selection/authorization/execution.
- Tool need capability resolution explicitly separates catalog provider recommendations/handoff candidates from registry-derived registered operation candidates and does not execute/authorize/mutate.
- Registry can list multiple registered operation records for a capability, but no provider relation or representation/method compatibility exists there.
- Operation selection explicitly resolves a single already selected operation name and does not choose providers or rank recommendations.
- Policy service explicitly separates valid operation call from authorization.
- Execution proposal is concrete and downstream, requiring action plan and tool arguments.

## 23. Strongest counterevidence

- `ToolNeedService.resolve_capability` already returns a read-only payload containing known capability, registered operations, provider recommendations, and handoff candidates. This is close to part of a candidate realization surface.
- `SingleCapabilityStateProjection` already composes requested demand, catalog known status, provider recommendations, registered operation associations, evidence, verification status, and Unknowns for one capability string.
- `ToolRegistry.list_tools_for_capability` can enumerate registered operation candidates directly by capability.
- `CapabilityRecommendation` may include `backend_type` and `operation`, giving a limited provider-to-operation hint.
- `ExecutionProposal` is abstract enough to carry provider, tool name, and arguments, suggesting a downstream target once selection/arguments exist.

Why counterevidence does not win: these artifacts either start from `ToolNeed`/capability string rather than a probe request, lack artifact/representation/method constraints, lack provider-tool-operation correlation, or are downstream concrete selected-call artifacts. Using an adapter that fills these gaps would transfer candidate-realization responsibility into the adapter.

## 24. Supported conclusions

1. Capability has separate requested, catalog-known, projected verification, and operation-contract meanings.
2. A registered tool/operation proves metadata and possible operation contract only, not reachability or authorization.
3. Provider recommendation is advisory and preserves alternatives.
4. Provider recommendation cannot consume `ExaminationProbeRequest` directly.
5. Operation selection starts from an already named operation.
6. Operation validation checks existence/status/input schema, not representation or methodology.
7. Candidate realization enumeration is absent as a distinct owner.
8. A bounded implementation slice is warranted for one missing composition owner, not for selection, authorization, execution, or proposal redesign.

## 25. Unsupported conclusions

- It is unsupported to claim existing owners already compose probe requests into candidate realizations.
- It is unsupported to treat provider recommendation as provider selection.
- It is unsupported to treat a registered tool as a currently reachable capability.
- It is unsupported to treat operation reachability as operation permission.
- It is unsupported to put methodological/fidelity/attribution constraints into operation arguments.
- It is unsupported to use current runtime execution behavior as green validation evidence because `tests/test_tool_validation.py` has reproducible failures.
- It is unsupported to add shell/Bash concepts to repository knowledge from the classification example alone.

## 26. Primary classification

C. Capability, provider, tool, and operation owners exist separately, but a candidate-realization composition owner is missing.

## 27. Tool/capability relationship classification

4. Capability and tool meanings vary by neighborhood and are not yet coherently reconciled.

## 28. First-missing-boundary classification

II. Capability/provider/tool candidate composition is the first missing boundary.

## 29. Exact next bounded boundary

Recovered responsibility: enumerate zero or more candidate operational realizations for one bound probe request without selection, authorization, execution, or argument construction beyond argument-shape visibility.

Producer: a new read-only candidate-realization composition owner.

Input artifacts: `ExaminationProbeRequest` or full probe plus `OperationalRealizationHandoff`, current State, existing capability inventory/projection, capability catalog/provider recommendations, tool registry registered-operation inventory, and method/representation constraints already preserved by the probe.

Output artifact: `CandidateOperationalRealizationSet` or equivalent read-only record with probe reference, capability identity, provider/tool/registered-operation candidate correlations, representation compatibility, methodological compatibility, availability/status evidence, authority requirements, argument requirements, provenance, and Unknowns.

Immediate consumer: later operational-realization selection owner.

Exact bounded question: for this probe, what provider/tool/registered-operation candidates may realize the requested capability and constraints, with statuses and Unknowns, without choosing one?

Manual responsibility eliminated: campaign author no longer manually correlates capability status, provider recommendation, tool registry entries, registered operation names, representation/method constraints, and Unknowns before selection.

Explicit exclusions: no provider selection, no operation selection, no operation arguments beyond requirements/feasibility, no policy authorization, no pending action, no execution proposal construction, no execution, no mutation, no ledger writes.

## 30. Implementation-warrant decision

One bounded implementation slice is warranted.

## 31. Files changed

- `operational_realization_topology_audit_001.md` only.

## 32. Probes executed

```bash
pwd && find .. -name AGENTS.md -print && git status --short
cat AGENTS.md && git status --short
rg -n "CapabilityInventory|capability inventory|CapabilityProjection|capability_id|tool need|required capability" seed_runtime tests
rg -n "provider recommendation|ProviderRecommendation|provider_id|provider" seed_runtime tests
rg -n "ToolRegistry|registered tool|registered operation|operation_id|operation_name" seed_runtime tests
rg -n "select_operation|OperationSelection|validate.*operation|tool_intent_guard" seed_runtime tests
rg -n "ExaminationProbeRequest|OperationalRealizationHandoff" seed_runtime tests
sed -n '1,260p' seed_runtime/capability_inventory.py
sed -n '1,240p' seed_runtime/single_capability_state_projection.py
sed -n '1,230p' seed_runtime/capability_catalog.py
sed -n '1,220p' seed_runtime/tool_needs.py
sed -n '1,200p' seed_runtime/registry.py
sed -n '1,230p' seed_runtime/models.py
sed -n '1,220p' seed_runtime/tool_validation.py
sed -n '1,230p' seed_runtime/tool_execution_policy.py
sed -n '1,210p' seed_runtime/execution_proposals.py
pytest -q tests/test_tool_validation.py
sed -n '1,140p' tests/test_examination_probe_request.py
sed -n '1,470p' tests/test_tool_recommendations.py
sed -n '1,280p' tests/test_tool_validation.py
sed -n '1,130p' tests/test_capability_inventory.py
sed -n '1,240p' tests/test_single_capability_state_projection.py
nl -ba seed_runtime/examination_probe_request.py | sed -n '31,84p'
nl -ba seed_runtime/capability_inventory.py | sed -n '99,187p'
nl -ba seed_runtime/single_capability_state_projection.py | sed -n '20,75p;84,153p'
nl -ba seed_runtime/tool_needs.py | sed -n '72,119p'
nl -ba seed_runtime/registry.py | sed -n '18,83p;91,134p'
nl -ba seed_runtime/tool_validation.py | sed -n '34,116p'
nl -ba seed_runtime/tool_execution_policy.py | sed -n '22,70p;137,205p'
nl -ba seed_runtime/execution_proposals.py | sed -n '16,75p'
```

## 33. Confidence statement

Confidence: high for the primary topology classification because multiple direct implementation owners explicitly preserve the same boundaries: advisory provider recommendations, registered-operation contract associations, named-operation selection, validation before policy, and downstream execution proposal. Confidence is moderate on provider/tool multiplicity because provider is not modeled in the registry and must be inferred from catalog/recommendation/action-plan neighborhoods. Confidence is reduced for runtime execution reuse because `tests/test_tool_validation.py` has reproducible failures, but those failures do not invalidate the read-only enumeration conclusion.
