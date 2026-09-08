> **Historical/stale after PR 1918.** This document is preserved as historical testimony only. Its Runtime, RuntimeLoop, Decision, Policy, Execution, ActionPlan, HandoffPlan, ExecutionProposal, ExecutionAuthorization, PendingAction, request_tool, call_tool, and builder-candidate language is not current architecture or operator instruction.

# Input Act Decision Bridge

## Purpose


The goal is to preserve the distinction introduced by `docs/input_act_vocabulary.md` while making the next design boundary explicit:

```text
InputAct
        ↓
        ↓
existing decision, validation, guard, policy, and routing path remains authoritative
```

## Core Rule

`InputAct` is advisory.


An input act describes what kind of user utterance Seed received. It should help the classifier, prompt, future inspection records, and tests preserve the user's act before routing. It must not execute tools, authorize side effects, bypass policy, or replace decision validation.


Therefore:

```text
```

and:

```text
```

## Existing Runtime Vocabulary

`seed_runtime/models.py` currently defines these runtime decision kinds:

| --- | --- |
| `answer` | Return direct answer text. |
| `ask_question` | Ask the user for missing information. |
| `call_tool` | Execute a visible registered tool through the canonical guarded runtime path. |
| `request_tool` | Record/request a missing capability or tool need. |
| `propose_action_plan` | Legacy/experimental text-only plan side path. |
| `propose_handoff_plan` | Legacy/experimental handoff-plan side path. |
| `propose_state_patch` | Runtime-supported state-patch side path. |
| `refuse` | Return a refusal reason. |

`docs/input_inspection_reconciliation.md` also documents that the context-advertised model schema is currently narrower than the full domain vocabulary and advertises only `answer`, `ask_question`, `call_tool`, `request_tool`, and `refuse` to the composed decision context.

This bridge document does not change that split.

## Bridge Table

| --- | --- | --- |
| `operator_query` | `answer`, `ask_question`, `request_tool`, `refuse` | The user is asking for information. Seed may answer, clarify, request unavailable capability, or refuse. |
| `command_request` | `ask_question`, `request_tool`, `propose_action_plan`, `call_tool`, `refuse` | The user is asking Seed to do something. Capability, policy, validation, and guard checks determine whether anything can proceed. |
| `user_observation` | `answer`, `ask_question`, `propose_state_patch`, `refuse` | The user is contributing an observation. Seed may acknowledge, clarify, possibly propose a state patch through an existing explicit path, or refuse unsafe handling. |
| `documentation_claim` | `answer`, `ask_question`, `request_tool`, `refuse` | The user is asserting what a document says. Seed may evaluate, clarify, request document access/capability, or refuse. |
| `correction` | `answer`, `ask_question`, `propose_state_patch`, `refuse` | The user is revising prior information. Seed may acknowledge, clarify the correction target, propose an explicit state patch where supported, or refuse unsafe handling. |
| `casual_answer` | `answer`, `ask_question`, `refuse` | The user is continuing conversationally. Seed may acknowledge, ask for clarity if context requires it, or refuse if the input asks for unsafe implicit behavior. |

The table is intentionally permissive rather than prescriptive. It describes allowed or plausible decision families, not a deterministic route map.

## InputAct-Specific Guidance

### `operator_query`

An `operator_query` normally supports `answer` because the user is asking Seed to explain or report something.

It may support `ask_question` when the target is ambiguous, `request_tool` when answering requires unavailable inspection or current external data, or `refuse` when policy prevents answering.

It should not bias directly toward `call_tool` merely because the query mentions a tool, host, repository file, package, service, or command.

### `command_request`

A `command_request` is the only initial input act in this vocabulary that naturally points toward action-oriented decisions.

It may support `request_tool` when a capability is missing, `propose_action_plan` when a text-only plan is appropriate, `call_tool` when a visible registered tool is valid and guarded, `ask_question` when the command is underspecified, or `refuse` when policy blocks the action.


### `user_observation`

A `user_observation` normally supports `answer` for acknowledgment or explanation.

It may support `ask_question` when the observation is ambiguous or conflicts with known context. It may support `propose_state_patch` only through the existing explicit state-patch path when the implementation and policy allow that kind of proposal.

It should not be treated as automatically durable knowledge. It is user-provided input, not direct observation by Seed.

### `documentation_claim`

A `documentation_claim` normally supports `answer` when Seed can evaluate, contextualize, or caveat the claim.

It may support `ask_question` when the document, quote, or source is ambiguous. It may support `request_tool` when the relevant documentation cannot be inspected with available capability.

It should not be treated as proof that the documentation claim is true. Documentation claims are candidates for support/reconciliation, not facts by default.

### `correction`

A `correction` normally supports `answer` for acknowledgment or explanation.

It may support `ask_question` when the correction target is unclear. It may support `propose_state_patch` where an explicit state-patch proposal path exists and the correction is suitable for that path.

It should not automatically mutate state, supersede stronger evidence, or become implicit approval for a side effect.

### `casual_answer`

A `casual_answer` normally supports `answer` as a short acknowledgment.

It may support `ask_question` if the surrounding conversation still requires clarification. It may support `refuse` if the casual response attempts to smuggle authorization or unsafe behavior through ambiguous language.

It must not be treated as implicit approval to execute a tool or commit a pending action unless a separate approval path explicitly recognizes it.

## Non-Deterministic Relationship

The bridge is many-to-many:

```text
```

Examples:

| --- | --- | --- | --- |
| `What does Seed know about ProjectionStore?` | `operator_query` | `answer` | The user wants an explanation/report. |
| `Which host runs web_service?` | `operator_query` | `ask_question` | Clarification may be needed if multiple workspaces or sources exist. |
| `Can you check whether web_service is listening?` | `command_request` | `request_tool` | The request asks for external/current inspection and may require missing capability. |
| `Install Docker on example_host_b.` | `command_request` | `propose_action_plan`, `request_tool`, `call_tool`, or `refuse` | The route depends on capability, policy, and guard checks. |
| `web_service is running on example_host_b.` | `user_observation` | `answer` | Seed can acknowledge or explain evidence requirements. |
| `README says ToolExecutor owns execution.` | `documentation_claim` | `answer` | Seed can discuss or evaluate the claim. |
| `No, example_host_b is not the web_service host anymore.` | `correction` | `ask_question` | Seed may need to know what replaced it or what record is being corrected. |
| `Thanks, that makes sense.` | `casual_answer` | `answer` | A brief acknowledgment is sufficient. |

## Relationship To Existing Input Inspection

This bridge extends the documentation model established by:

- `docs/input_inspection_reconciliation.md`
- `docs/input_act_vocabulary.md`

It does not replace the current path:

```text
raw user text
  -> Runtime.handle_user_message
  -> input.user_message event
  -> context composition
  -> decision model / compact classifier / fallback
  -> validation
  -> Runtime._route
```

Instead, it defines how a future `InputInspection` record or classifier helper could preserve input-act metadata before the existing decision pipeline chooses and validates a route.

## Future Implementation Boundary

A later implementation may add a small deterministic helper such as:

```text
```

If added, that helper should be advisory only. It should not:

- execute tools;
- authorize side effects;
- bypass validation;
- bypass policy or approval gates;
- rewrite `Runtime`;
- make `request_tool` executable.


## Rejected Interpretations

This bridge rejects:

- treating `InputAct` as a runtime route;
- treating `InputAct` as an execution permission;
- treating `command_request` as automatic `call_tool`;
- treating `casual_answer` as implicit approval;
- treating `user_observation` as a durable fact;
- treating `documentation_claim` as verified truth;
- adding `InputEngine`, `ConversationEngine`, `CommandEngine`, or a new `RuntimeLoop`;
- adding LLM-only routing with no deterministic fallback;
- bypassing existing validation, guard, policy, capability, or execution boundaries.

## Documentation-Only Status

