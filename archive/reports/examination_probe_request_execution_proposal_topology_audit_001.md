# Examination Probe Request / Execution Proposal Topology Audit 001

## 1. Bounded question

Can the existing execution-proposal owner lawfully consume a selected examination-work handoff, or is one distinct examination probe-request boundary missing between selection and execution proposal?

## 2. Governing distinctions

Preserved distinctions: selected work is not a requested probe; requested probe is not concrete operation realization; operation realization is not execution proposal; execution proposal is not registered-operation validation; validated operation is not policy authorization; authorized operation is not execution; selection reason is not operation arguments; work contract identity is not registered operation identity; methodological constraints are not execution policy; provider attribution requirement is not provider selection; probe request is not pending action; proposal is not permission.

## 3. Methodology

This was a read-only implementation-backed audit except for this report. I used focused ripgrep probes, then inspected implementation bodies and direct tests for `ExaminationWorkSelection`, `FutureProbeRequestHandoff`, `ExecutionProposalService`, action plans, registered-operation selection/validation, tool execution policy, and pending actions. I did not inspect or classify corpus discovery, candidate-generation correctness, methodological applicability correctness, selection correctness, campaign completion, the Eye, general grammar architecture, or execution internals beyond validation/policy boundaries.

## 4. Inspected owners

- `seed_runtime.examination_work_selection.select_examination_work` produces `ExaminationWorkSelection` and optional `FutureProbeRequestHandoff`.
- `seed_runtime.execution_proposals.ExecutionProposalService.create_proposal` produces `ExecutionProposal`.
- `seed_runtime.action_plans.ActionPlanService` produces and manages legacy `ActionPlan` lifecycle and grants execution authorization for an existing proposal.
- `seed_runtime.tool_validation.ToolValidationService.select_operation` resolves a single already-named registered operation.
- `seed_runtime.tool_execution_policy.ToolExecutionPolicyService` validates a selected registered operation call and then evaluates policy.
- `seed_runtime.pending_actions.PendingActionService.create_tool_call` creates pending tool-call records.

## 5. Current selection handoff

`FutureProbeRequestHandoff` preserves exactly: `selection_id`, `inquiry_reference`, `frontier_reference`, `policy_reference`, `selected_work_reference`, `selection_reason`, `method_constraint_reference`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.

It intentionally does not preserve or construct: operation/provider identity, registered operation identity, tool arguments, requested probe outcome as a first-class field, input or produced representation, artifact identity/hash/version, candidate-work record fields other than selected work reference, work-contract identity, exact fidelity/attribution/claim-treatment constraints, pending action identity, authorization, schedule, execution decision, or result destination. Selection boundary notes explicitly keep methodological applicability and constraints upstream and deny authorization, scheduling, execution, and marking work examined.

## 6. Execution-proposal analysis

The execution-proposal suite tests `ExecutionProposalService.create_proposal` and the `ExecutionProposal` artifact. The producer takes an `ActionPlan` and projected `State`; it first evaluates action-plan preconditions and then builds a concrete tool call only for `service_management/docker_container_lifecycle` by reading service host/container facts from `State`.

The output artifact contains `id`, `action_plan_id`, `provider`, `tool_name`, `tool_arguments`, `arguments_fingerprint`, `risk_class`, `authorized=False`, and `executable=False`. Its immediate consumers are projection/state storage, CLI authorization/precondition paths, and `ActionPlanService.grant_execution_authorization`, which binds authorization to an existing proposal id and copies only tool name and argument fingerprint.

The producer consumes an action plan with selected provider and capability, not a selected examination work item. It binds operation arguments. It preserves action-plan provenance through `action_plan_id`, but not inquiry or examination-selection provenance. It does not select among registered operations from a capability; it hard-codes/supports one provider/capability-to-tool-call builder. It does not create pending actions and does not authorize or execute. It explicitly refuses internal lifecycle, credentials, retries, scheduling, long-running jobs, approvals, execution authorizations, registration, and tool invocation.

## 7. Information-compatibility matrix

| Required information | Selection/handoff provides it | Proposal requires it | Existing owner can derive it | Missing owner |
| --- | ---: | ---: | ---: | --- |
| inquiry identity | Yes, as `inquiry_reference` | No | Not used | Probe-request binding |
| artifact identity/version | Indirectly only via frontier reference; not exact selected artifact fields | No for current docker proposal | No | Probe-request binding |
| candidate-work identity | Yes, as `selected_work_reference` to frontier work id, not full candidate record | No | No | Probe-request binding |
| work-contract identity | No | No | No | Probe-request binding from candidate/frontier/work-set context |
| requested outcome | No first-class field | No | No | Probe-request binding |
| required input representation | No | No | No | Probe-request binding |
| produced representation | No | No | No | Probe-request binding |
| methodological constraints | Only method-constraint reference | No | No | Probe-request binding/preservation |
| fidelity constraints | No | No | No | Probe-request binding/preservation |
| attribution constraints | No | No | No | Probe-request binding/preservation |
| claim-treatment constraints | No | No | No | Probe-request binding/preservation |
| capability identity | Indirectly only if frontier item is looked up | ActionPlan requires capability | No from handoff alone | Operational realization after probe request |
| provider identity | No | ActionPlan/proposal require provider | No | Operational realization |
| registered operation identity | No | Proposal requires `tool_name` | No | Operational realization-to-proposal construction |
| operation arguments | No | Proposal requires `tool_arguments` | No | Operational realization-to-proposal construction |
| selection reason | Yes | No | Could carry only if model extended, not current contract | Probe-request binding |
| provenance | Partial selection/inquiry/frontier/policy references | Only action-plan id/fingerprint | No | Probe-request binding plus realization provenance |

## 8. Work-contract-versus-operation analysis

`ExaminationWorkContract` identifies an abstract examination transformation/visibility contract: `contract_id`, `capability_id`, `work_kind`, accepted input representation, produced output representation, convention, availability, applicable members, provenance, and unknowns. Candidate work records copy contract identity and representation requirements. Frontier work items preserve `work_kind`, `capability_id`, `convention`, artifact identity/hash, classification, reasons, and unknowns.

The selected work contract cannot directly identify an executable operation. It is not a callable registered operation, not a provider selection, and not operation arguments. The missing realization boundary is therefore `selected work contract -> candidate operational realization`; policy authorization remains a later boundary and must not be conflated with this realization.

## 9. Probe-request responsibility analysis

A distinct examination probe request is warranted as the earliest owner of binding a selection to exact selected artifact identity/version, selected candidate-work/work-contract identity, requested examination outcome, required input representation, produced representation, methodological constraint references/constraints, fidelity/attribution/claim-treatment constraints, selection reason, and provenance while requesting capability realization without selecting provider or operation.

Those responsibilities are not already owned by `ExecutionProposal`: the current proposal is concrete-call shaped, action-plan based, provider/tool named, argument-bearing, and does not preserve inquiry, selected work, artifact, contract, or methodological constraints.

## 10. Execution-proposal responsibility analysis

The current execution proposal is a concrete proposal naming a provider, registered operation/tool name, and arguments, with a fingerprint and risk class. It is not executable by itself and is not permission, but it is already downstream of provider/tool/argument realization. Because it is concrete, some owner before it must translate an examination probe request into a lawful operational realization and then into an execution proposal. It cannot directly consume `FutureProbeRequestHandoff` with only a narrow adapter because the handoff lacks the action-plan input contract, provider/tool names, and operation arguments, and because adding those to an adapter would create realization responsibility.

## 11. Provider/tool-realization analysis

Capability recommendation and provider recommendation exist in the tool-need/action-plan road, but they do not consume examination work contracts. Registered operation selection resolves one already-named operation from a `call_tool` decision; it explicitly does not rank capability recommendations, inspect handoff metadata, or choose providers. Registered operation validation proves existence/status/input shape only. Tool execution policy authorizes a validated registered operation call but does not create pending actions or execute. Pending actions store already-formed tool calls awaiting approval.

No inspected owner can transform a selected examination-work contract into a proposed operational realization. The action-plan road can select provider from a tool need/recommendation, but the missing examination probe request is earlier because the selected handoff has not yet bound exact artifact/contract/request constraints into an abstract requested probe.

## 12. Methodological-constraint preservation

Fidelity, attribution, exact material/span identity, competing interpretation preservation, claim-treatment restrictions, no Fact/Evidence promotion, and downstream authorization requirements must survive in a request/preservation artifact before operation realization. The current execution proposal has no fields for opaque examination constraints, artifact identity, work contract identity, selection reason, or inquiry reference. Storing these as `tool_arguments` would misclassify methodological constraints as operation arguments; storing them as authorization/policy would misclassify methodology as execution policy.

## 13. No-realization behavior

When selected work has no provider, no registered operation, unformable arguments, unrepresentable methodological constraints, incomplete artifact identity, or multiple realizations without a lawful selector, the lawful result is an Unknown/insufficiency at the request/realization boundary. The road must not invent a provider, operation, pending action, authorization, or execution proposal.

## 14. Direct composition trace

Using the existing selected-work fixture from `tests/test_examination_work_selection.py`, selection can produce a handoff with `selection_id`, `inquiry_reference`, `frontier_reference`, policy projection reference/kind, selected frontier work id, selection reason, and method applicability reference. Calling the existing proposal producer requires `ExecutionProposalService.create_proposal(action_plan: ActionPlan, state: State, ...)`. The selected handoff is neither an `ActionPlan` nor a `State`, and it has no provider, capability in action-plan form, risk class, plan id, executable preconditions, tool name, or tool arguments.

## 15. Exact first mismatch

The first exact composition mismatch is the producer input contract: `ExecutionProposalService.create_proposal` requires an `ActionPlan`, while `FutureProbeRequestHandoff` supplies only selected-work references and reason. The first missing information inside that mismatch is a bounded requested-probe artifact that binds the selected work reference to exact artifact/work-contract/requested-outcome/representation/methodological constraints before any provider or operation realization.

## 16. Strongest supporting evidence

- `FutureProbeRequestHandoff` is reference-only and read-only; it lacks provider/tool/argument fields.
- `ExecutionProposal` is a concrete-call shape with `provider`, `tool_name`, `tool_arguments`, and `arguments_fingerprint`.
- `ExecutionProposalService` only builds a docker lifecycle concrete call from an action plan and service facts.
- `ToolValidationService.select_operation` starts from an already-selected operation name, not capability/work metadata.
- `ToolExecutionPolicyService` separates registered operation validation from policy authorization.
- `PendingActionService` creates pending records only for already-formed tool calls.
- `ExaminationWorkContract` preserves abstract capability/work/representation/convention, not registered operation identity.

## 17. Strongest counterevidence

- The execution-proposal module calls itself a concrete-call proposal that is not executable by itself, so it is not permission or execution and could theoretically be a handoff target after an adapter.
- It can append an `execution_proposal.created` event with an opaque serialized proposal payload and can reject secrets, so it already has some audit-like boundary behavior.
- It preserves `action_plan_id`, provider, risk class, fingerprint, and non-executable/unauthorized flags, which are useful provenance/control fields downstream.
- The action-plan road already has a provider/capability concept and precondition reporting, reducing the need to invent a separate generic execution-proposal abstraction.
- `ExecutionProposalFailure` already preserves insufficiency for precondition/tool-call failures in the action-plan road.

This counterevidence is not strong enough to classify the existing proposal as the requested-probe artifact because its implementation and tests require an action plan and concrete provider/tool/arguments rather than selected examination work and methodological constraints.

## 18. Supported conclusions

1. The current execution proposal represents a legacy/experimental concrete tool-call proposal for an accepted action-plan road, not a bounded examination probe request.
2. Its producer requires an `ActionPlan` and projected `State` with executable preconditions.
3. It does not already represent a bounded requested probe.
4. It names a concrete registered operation/tool.
5. It binds operation arguments and fingerprints them.
6. It preserves action-plan provenance, but not inquiry and examination-selection provenance.
7. It cannot currently preserve artifact identity and work-contract identity without schema changes or misuse of arguments.
8. It cannot currently preserve methodological constraints as first-class request constraints.
9. It cannot preserve fidelity/attribution constraints without treating them as operation arguments or unrelated policy metadata.
10. `FutureProbeRequestHandoff` cannot directly satisfy the execution-proposal input contract.
11. The first missing owner is selection-to-probe-request binding.
12. A distinct `ExaminationProbeRequest` artifact is warranted.
13. Such an artifact would not duplicate execution proposal because it would not choose provider, registered operation, or arguments.
14. Operational realization is also missing, but it is not first.
15. Provider or registered operation selection should be owned by an operational-realization owner after probe request, not by selection.
16. Selection cannot lawfully reach current execution proposal without operation realization.
17. When no operational realization exists, Unknown/insufficiency must be preserved.
18. When several realizations exist, Unknown/conflict/multiple-candidate insufficiency must be preserved unless a lawful selector exists.
19. Unknown must remain for artifact identity gaps, missing provider, missing operation, unformable arguments, unrepresentable constraints, and ambiguous realization.
20. The smallest producer/artifact/consumer handoff is `ExaminationProbeRequestProducer` consuming `ExaminationWorkSelection`/`FutureProbeRequestHandoff` plus referenced frontier/candidate-work context and producing `ExaminationProbeRequest` for an operational-realization consumer.
21. It would eliminate the manual campaign-author responsibility of translating a selected examination work item into a precise probe request with artifact, contract, representation, constraints, reason, and provenance.
22. One bounded implementation slice is warranted.

## 19. Unsupported conclusions

- That execution proposal should be redesigned during this audit.
- That a provider or registered operation should be selected by `ExaminationWorkSelection`.
- That methodological constraints should be encoded as `tool_arguments`.
- That a pending action should be created from selection.
- That policy authorization can substitute for probe request or operational realization.
- That every selected probe request will have one realizable provider or operation.
- That examination requests should become campaign-local only; no implementation evidence proves that boundary.

## 20. Primary classification

E. Both probe-request construction and operational realization remain missing, with probe request first.

## 21. Request/proposal relationship classification

3. They are distinct responsibilities and their handoff is missing.

## 22. First-missing-boundary classification

I. Selection-to-probe-request binding is the first missing boundary.

## 23. Exact next bounded boundary

Recover responsibility: bind one selected examination work handoff to a bounded requested examination probe without choosing provider, registered operation, operation arguments, pending action, authorization, or execution.

Producer: `ExaminationProbeRequestProducer`.

Input artifacts: `ExaminationWorkSelection`/`FutureProbeRequestHandoff`, the referenced `ExaminationFrontier` work item, and enough referenced candidate-work/work-contract context to recover artifact identity/hash, candidate-work id, work-contract id, requested outcome, required input representation, produced representation, method constraints, selection reason, and provenance.

Output artifact: `ExaminationProbeRequest`.

Immediate consumer: a future operational-realization owner that maps requested probe/capability/constraints to candidate provider/registered-operation realization or Unknown.

Exact bounded question: can one selected examination work item be bound into a non-operational requested probe preserving artifact, contract, representation, methodological constraints, selection reason, provenance, and Unknowns without choosing or validating a registered operation?

Manual responsibility eliminated: campaign authors no longer manually translate selected work references into exact probe requests and constraint bundles before realization.

Explicit exclusions: no provider selection, registered operation selection, argument construction, operation validation, policy authorization, pending action, execution, result ingestion, fact/evidence promotion, campaign completion, or diagnostics changes.

## 24. Implementation-warrant decision

One bounded implementation slice is warranted.

## 25. Files changed

- `examination_probe_request_execution_proposal_topology_audit_001.md` only.

## 26. Probes executed

- `pwd && find .. -name AGENTS.md -print && git status --short`
- `cat AGENTS.md && git status --short`
- `rg -n "ExecutionProposal|execution proposal|proposal_id|proposed operation|operation arguments" seed_runtime tests campaigns`
- `rg -n "FutureProbeRequestHandoff|ExaminationWorkSelection|selected_work|selection_reason" seed_runtime tests`
- `rg -n "select_operation|OperationSelection|provider recommendation|capability recommendation|registered operation" seed_runtime tests`
- `rg -n "ToolExecutionPolicy|pending action|authorize|validation|execute" seed_runtime tests`
- `sed -n '1,180p' seed_runtime/examination_work_selection.py`
- `sed -n '1,180p' seed_runtime/execution_proposals.py`
- `sed -n '1,260p' tests/test_execution_proposals.py`
- `sed -n '180,360p' seed_runtime/execution_proposals.py`
- `sed -n '1,260p' seed_runtime/action_plans.py`
- `rg -n "class ActionPlan|class Pending|execution_proposals|ExecutionAuthorization" seed_runtime/models.py seed_runtime/state.py seed_runtime/preconditions.py seed_runtime/pending_actions.py`
- `sed -n '120,170p' seed_runtime/models.py`
- `sed -n '220,315p' seed_runtime/models.py`
- `sed -n '1,230p' seed_runtime/tool_validation.py`
- `sed -n '1,230p' seed_runtime/tool_execution_policy.py`
- `sed -n '1,130p' seed_runtime/pending_actions.py`
- `rg -n "ExaminationWorkContract|work_contract|contract|capability_id|CandidateExaminationWork" seed_runtime tests | head -200`
- `sed -n '1,220p' seed_runtime/candidate_examination_work.py`
- `sed -n '1,180p' tests/test_examination_work_selection.py`

## 27. Confidence statement

Confidence: high for the immediate seam classification. The inspected implementation and tests consistently show a reference-only examination selection handoff, a concrete action-plan-based execution proposal, separate registered-operation validation and policy authorization, and no owner that binds selected examination work into a requested probe. Confidence is limited only by the audit scope: this report did not inspect unrelated campaign-local code or general external grammar architecture outside the requested seam.
