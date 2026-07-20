# Bounded Inquiry to Decision Mapping Reconciliation

## Scope

This reconciliation is observational. It inspects only the current implementation surfaces for `Decision`, `DecisionProducer`, `DecisionValidator`, canonical Runtime routing, `request_tool`, `ask_question`, `call_tool`, `answer`, and `refuse`, plus the current inquiry-style implementations `container_ownership_authority`, `service_ownership_authority`, and `privilege_discovery` for comparison.

It does not introduce planning, an inquiry engine, a new Runtime, or new `Decision` kinds.

## Executive answer

A bounded inquiry can produce an existing `Decision` today if it implements the existing `DecisionProducer.decide(decision_input) -> Decision` protocol and returns a `Decision` that satisfies `DecisionValidator`. Runtime already accepts any object with that protocol shape, validates the returned `Decision`, applies the existing tool-intent guard, and routes valid decisions through existing response, tool-need, tool-execution, state-patch, or refusal branches.

The current `Decision` vocabulary is sufficient for the observed inquiry-driven runtime bridge for these bounded outcomes:

| Bounded inquiry outcome | Existing `Decision` mapping | Support status |
| --- | --- | --- |
| final bounded answer | `answer` | supported |
| ambiguous / needs operator clarification | `ask_question` | supported |
| additional observation requires unavailable capability or authority-backed capability acquisition | `request_tool` | supported as capability-gap recording, not execution |
| existing visible registered operation can satisfy already-determined work | `call_tool` | supported as execution boundary |
| unsafe / prohibited / intentionally non-actionable outcome | `refuse` | supported |
| partially reachable inquiry state | usually `answer`; optionally `request_tool` for blocked remainder | supported only by composition in an inquiry producer, not as a distinct `Decision` kind |
| unknown inquiry state | `answer`, `ask_question`, or `request_tool` depending on whether unknown is reportable, ambiguous, or capability-limited | supported only by inquiry-owned interpretation, not as a distinct `Decision` kind |
| blocked by missing authority | `request_tool` when expressed as missing capability/authority need; `answer` when only reporting the boundary | partially supported; no authority-specific `Decision` kind exists or is needed by current runtime |

The smallest implementation-backed bridge is:

```text
one bounded inquiry adapter implementing DecisionProducer
↓
evaluate an existing inquiry slice
↓
return one existing Decision kind
↓
Runtime validation and routing
↓
existing response / ToolNeedService / ToolExecutor behavior
```

The repository already supports that shape. What does not yet exist is a committed adapter that calls one of these inquiry evaluators and converts its result into a `Decision`.

## 1. What bounded outcomes can an inquiry currently reach?

### `container_ownership_authority`

`evaluate_container_ownership_authority_slice` computes:

- `blocked`, when required container observations are Docker/root-dependent and both root and Docker socket authority are unavailable.
- `unknown`, otherwise.

The result also preserves `remaining_observations`, `remaining_uncertainty`, and an optional `blocking_boundary`. Its boundary declares read-only behavior, no recording, no event-ledger writes, no cluster mutation, no provider acquisition, no permission creation, and no observation execution.

Implementation-backed outcomes:

| Outcome | Evidence |
| --- | --- |
| blocked | Docker/root-required observations with unavailable root and Docker socket authority produce `outcome = "blocked"`. |
| unknown | All non-blocked cases fall back to `"unknown"`. |
| additional authority required | The blocking boundary is `docker_or_root_container_runtime_authority_unavailable`; remaining observations are the required Docker/root observations. |
| additional observation required | `remaining_observations` carries the required observations when blocked. |
| visibility-only / non-mutating boundary | The result boundary marks recording and mutation false. |

### `service_ownership_authority`

`evaluate_service_ownership_authority_slice` computes:

- `partially_reachable`, when some required observations are reachable and some are blocked.
- `reachable`, when required observations are reachable and none are blocked.
- `blocked`, when observations are blocked and none are reachable.
- `unknown`, when neither reachable nor blocked observations are found.

The result carries reachable observations, blocked observations, blocked-observation details, remaining observations, uncertainty, and an optional Docker/root blocking boundary. Its boundary is likewise read-only, non-recording, non-mutating, and non-executing.

Implementation-backed outcomes:

| Outcome | Evidence |
| --- | --- |
| partially reachable | `reachable and blocked` yields `"partially_reachable"`. |
| reachable | reachable observations with no blocked observations yield `"reachable"`. |
| blocked | blocked observations with no reachable observations yield `"blocked"`. |
| unknown | no reachable or blocked observations yield `"unknown"`. |
| additional authority required | Docker/root container-runtime blockage is exposed through `blocking_boundary`. |
| additional observation required | `remaining_observations` is the blocked observation tuple. |

### `privilege_discovery`

`build_privilege_discovery` produces visibility-only capability guidance for current capability needs. It does not produce a single inquiry `outcome` field, but each `PrivilegeDiscoveryCapability` exposes:

- `access_level`, such as `partial_non_root`, `docker_group_or_root`, `root`, `local_passive`, or `unknown`.
- `implementation_evidence`, such as `registered`, `not_registered`, or `unknown`.
- `guidance_status`, such as `registered` or `unknown`.
- `limiting_reason`, including `missing_authority`, `missing_implementation_evidence`, `missing_guidance`, or `none`.
- `suggested_next_step` and explanatory notes.

Implementation-backed outcomes:

| Outcome | Evidence |
| --- | --- |
| additional authority required | `root`, `docker_group_or_root`, and `unknown` access can lead to `limiting_reason = "missing_authority"`. |
| missing implementation evidence | `implementation_evidence = "not_registered"` leads to `missing_implementation_evidence`. |
| unknown guidance | unknown guidance status leads to `missing_guidance`. |
| no limiting reason | local/passive or otherwise supported guidance can yield `none`. |
| visibility-only / non-mutating boundary | The audit has `mutates_cluster = False` and `writes_event_ledger = False`. |

## 2. What existing `Decision` kinds already correspond to those outcomes?

### `answer`

`answer` corresponds to a bounded inquiry that can report its computed result without needing clarification, capability acquisition, or execution. `DecisionValidator` requires only `decision.answer`; Runtime records `response.answer` and returns an answer response.

This can express:

- final bounded answer;
- blocked-but-reportable boundary;
- partially reachable summary;
- unknown-but-reportable summary.

It does not execute observations or acquire authority.

### `ask_question`

`ask_question` corresponds to a bounded inquiry that cannot decide the next valid response because operator input is ambiguous or missing. `DecisionValidator` requires `decision.question`; Runtime records `response.question` and returns a question response.

This can express:

- ambiguous subject;
- missing selection among known alternatives;
- insufficient operator-provided authority profile when the inquiry requires the operator to state or choose authority.

It is not a capability-acquisition or execution path.

### `request_tool`

`request_tool` corresponds to a bounded inquiry that identifies a missing capability or capability-like need. `DecisionValidator` requires a `tool_need` with valid `name`, `summary`, and `capability`. Runtime routes it to `ToolNeedService.create_from_decision`, computes recommendations and read-only capability resolution, and returns a `tool_need` response. Architecture invariant tests assert that this path records a capability need without invoking the tool executor.

This can express:

- additional observation required when the missing observation is represented as a capability need;
- missing capability;
- authority-bound observation need when encoded as a capability gap, such as Docker/root-backed container-runtime visibility.

It does not itself execute the observation, authorize permission, mutate the cluster, or call a registered operation.

### `call_tool`

`call_tool` corresponds to already-determined work using a visible registered tool. `DecisionValidator` requires `tool_name` and validates input against the registry and state through `ToolValidationService`. Runtime then calls `ToolExecutor.execute`; tests assert this is the branch that invokes the tool executor.

This can express:

- an inquiry deciding that an existing registered operation can satisfy the next observation or action;
- execution of already-determined work after validation and guard checks.

It should not be used for missing authority, missing capability, or speculative planning.

### `refuse`

`refuse` corresponds to a bounded inquiry that determines the requested output or action should not proceed. `DecisionValidator` requires a non-empty reason; Runtime records `response.refusal` and returns a refusal response.

This can express:

- unsafe request;
- prohibited execution;
- boundary-preserving refusal to promote presentation vocabulary or unsupported inference into knowledge.

## 3. Does every inquiry outcome naturally map to an existing Decision?

For the reviewed implementation, yes for runtime purposes, with two caveats.

Supported mappings:

| Inquiry outcome | Natural existing mapping |
| --- | --- |
| answer / reachable | `answer` |
| blocked and reportable | `answer` |
| blocked and needs unavailable capability | `request_tool` |
| partially reachable and reportable | `answer` |
| partially reachable with blocked remainder worth recording | `request_tool` for the blocked remainder, or `answer` summarizing both parts |
| unknown and reportable | `answer` |
| unknown due to ambiguous input | `ask_question` |
| unknown due to missing observation capability | `request_tool` |
| additional authority required | `request_tool` if modeled as a capability need; otherwise `answer` or `ask_question` |
| additional observation required | `request_tool` for unavailable capability, `call_tool` for visible registered capability, or `answer` if only reporting |
| unsafe / forbidden | `refuse` |

Implementation-backed gaps:

1. No current adapter maps an inquiry result object into a `Decision`. Runtime supports the protocol, but the reviewed inquiry functions currently return slice/audit dataclasses rather than `Decision` objects.
2. Partial reachability and unknown are inquiry-state distinctions, not runtime `Decision` kinds. They must be represented inside an `answer` body, a `tool_need` payload, or a question/refusal reason.
3. Authority-specific requests have no separate `Decision` kind. Current support is through `request_tool` as a `ToolNeed` capability gap or through plain `answer`/`ask_question` reporting.

No new `Decision` kind is required by the current implementation evidence.

## 4. What does `request_tool` currently represent?

`request_tool` currently represents a missing capability / capability need, with optional resolution metadata. It can carry additional-observation needs when those needs are expressed as capabilities, but it is not a generic observation executor and not a direct authority grant.

Implementation support:

- `DecisionValidator` validates `request_tool` by requiring `tool_need.name`, `tool_need.summary`, and `tool_need.capability`.
- `ToolNeedService` is explicitly summarized as owning capability-gap creation and read-only capability resolution for `request_tool` decisions.
- Runtime routes `request_tool` to `ToolNeedService`, recommendations, and capability resolution, returning `kind="tool_need"`.
- `ToolNeedService.resolve_capability` documents that it does not execute tools, authorize actions, create pending actions, or mutate registry/catalog state.
- Architecture tests assert `request_tool` records capability need without calling `ToolExecutor`.

So the most precise answer is:

```text
request_tool = explicit capability-gap / ToolNeed recording path
```

It may represent additional observation required only when the missing observation is represented as a capability need.

## 5. Would a bounded inquiry be capable of producing a valid Decision today without modifying Runtime?

Yes.

Runtime depends on a `DecisionProducer` protocol with only `decide(decision_input) -> Decision`. `StaticDecisionProducer` proves that the producer can be any object returning a `Decision`. Tests build Runtime with custom producer objects and static decisions. Once such a producer returns a valid `Decision`, canonical Runtime validates and routes it.

The missing piece is not Runtime support. It is an inquiry adapter that owns the inquiry-specific mapping from inquiry result state to one `Decision` object.

## 6. Does Runtime already provide everything required once a Decision exists?

Yes, for the existing decision vocabulary.

Once a decision exists, Runtime already provides:

1. input event recording;
2. state projection;
3. decision input composition;
4. decision production call;
5. proposed-decision event recording;
6. decision validation;
7. tool-intent guard validation;
8. routing for `answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, and `refuse`;
9. invalid-decision parse/validation retry handling;
10. response, tool-need, execution, state-patch, or refusal event paths according to branch.

The central runtime seam is already:

```text
Reasoning / producer
↓
Decision
↓
Runtime validation and routing
↓
Execution or response owner service
```

## 7. If an inquiry produced a Decision, what responsibility remains outside the inquiry?

The inquiry should own only the bounded question and deterministic local reasoning needed to choose a proposed `Decision`.

Responsibilities that remain outside the inquiry:

| Responsibility | Current owner |
| --- | --- |
| decision shape validation | `DecisionValidator` |
| registered tool input/schema validation | `DecisionValidator` via `ToolValidationService` |
| tool-intent guard | `Runtime` via `ToolIntentGuard` |
| runtime routing | `Runtime._route` |
| capability-gap persistence and capability resolution | `ToolNeedService` plus recommendation/catalog/registry helpers |
| registered operation execution | `ToolExecutor` through the `call_tool` branch only |
| response/refusal/question event recording | `Runtime` |
| tool-need event recording | `ToolNeedService` |
| state projection before decision | `StateProjector` |
| context composition | `DecisionInputComposer` |
| policy and execution checks for tools | existing execution/policy services behind `ToolExecutor` and validation paths |

## 8. Smallest implementation-backed demonstration

The smallest demonstration that the repository already supports is:

```text
one inquiry adapter implementing DecisionProducer
↓
call evaluate_service_ownership_authority_slice or evaluate_container_ownership_authority_slice
↓
map the result to one of:
  - Decision(kind="answer", ...)
  - Decision(kind="ask_question", ...)
  - Decision(kind="request_tool", tool_need={...})
  - Decision(kind="call_tool", tool_name=..., tool_arguments={...})
  - Decision(kind="refuse", ...)
↓
pass that producer to current Runtime
↓
Runtime validates and routes through existing branches
```

A particularly small bounded slice would use `container_ownership_authority`:

- constrained profile returns `outcome="blocked"` with Docker/root remaining observations;
- inquiry adapter returns `Decision(kind="request_tool", tool_need={"name": "container_runtime_visibility", "summary": "Provide Docker or root-backed read-only container runtime visibility", "capability": "container_inventory"})` or an `answer` reporting the blocked boundary;
- existing Runtime records `model.decision.proposed`;
- `DecisionValidator` validates the `tool_need`;
- `Runtime` routes to `ToolNeedService`;
- `ToolNeedService` records `tool_need.created` and returns read-only capability resolution.

This would prove the bridge without changing Runtime or adding a new `Decision` kind.

## Recommended bounded implementation slice

Do not implement a planner, inquiry engine, decision engine, new runtime, new `Decision` kind, or execution redesign.

The bounded slice, if later requested, is only:

```text
InquiryDecisionProducer for one existing inquiry
```

Constraints:

- implement the existing `DecisionProducer` protocol;
- call one existing inquiry evaluator;
- map exactly one implementation-backed result to exactly one current `Decision` kind;
- rely on current `DecisionValidator`, `Runtime`, `ToolNeedService`, and `ToolExecutor` boundaries;
- test with canonical Runtime that the produced decision validates and routes through the existing branch.

## Commands executed

```text
pwd
rg --files -g 'AGENTS.md' -g '!**/.git/**'
find .. -name AGENTS.md -print
cat AGENTS.md
git status --short
rg "class Decision|DecisionKind|DecisionProducer|DecisionValidator|request_tool|ask_question|call_tool|refuse|def answer|container_ownership_authority|service_ownership_authority|privilege_discovery" -n .
sed -n '1,220p' seed_runtime/models.py
sed -n '1,220p' seed_runtime/decisions.py
sed -n '1,380p' seed_runtime/runtime.py
sed -n '380,520p' seed_runtime/runtime.py
sed -n '1,260p' seed_runtime/tool_needs.py
sed -n '1,260p' seed_runtime/container_ownership_authority.py
sed -n '1,520p' seed_runtime/service_ownership_authority.py
sed -n '1,420p' seed_runtime/privilege_discovery.py
sed -n '1,240p' tests/test_architecture_invariants.py
sed -n '1,230p' tests/test_runtime_loop.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/models.py`
- `seed_runtime/decisions.py`
- `seed_runtime/runtime.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/privilege_discovery.py`
- `tests/test_architecture_invariants.py`
- `tests/test_runtime_loop.py`

## Files changed

- `docs/bounded_inquiry_decision_mapping_reconciliation.md`

## LOC changed

One documentation file was added. The report contains the implementation-backed reconciliation only and does not alter runtime code, diagnostics, registries, shape-audit specs, or tests.

## Tests run

No tests were required for this documentation-only reconciliation. No runtime, diagnostic, audit, CLI, or recordable output behavior was changed.
