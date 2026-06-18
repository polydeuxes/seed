# Input Act Vocabulary

## Purpose

This document defines first-class vocabulary for describing what kind of thing a user said before Seed chooses what to do next. It is documentation-only and does not change runtime behavior, tests, routing, validation, policy, tool execution, event storage, or projection behavior.

The motivation comes from `docs/input_inspection_reconciliation.md`: Seed already has a real input-inspection and decision-routing path, but its current vocabulary is mostly output-shaped or route-shaped. Seed needs stable words for user input acts before any future code changes preserve those acts explicitly.

## Central Distinction

`InputAct` answers:

> What kind of thing did the user say?

`DecisionKind` answers:

> What should Seed do next?

These are related, but they are not the same thing.

**InputAct != DecisionKind.**

An input act classifies the user's utterance as input. A decision kind classifies Seed's next runtime behavior after context composition, model or classifier decision-making, validation, guard checks, policy, and capability constraints. The same input act can lead to different decision kinds depending on evidence, policy, available tools, missing capabilities, ambiguity, and safety. Conversely, the same decision kind can be an appropriate response to several different input acts.

For example, `Install Docker on example_host_b.` is a `command_request` because the user is asking for an action. Its possible downstream `DecisionKind` may be `request_tool`, `propose_action_plan`, `call_tool`, or `refuse` depending on capability, policy, and validation. The input act should not pre-authorize execution.

## Why Existing Vocabulary Is Insufficient

Current terms such as:

- `answer`;
- `ask_question`;
- `call_tool`;
- `request_tool`;
- `refuse`;
- `echo`;
- `missing_tool`;
- `clarify`.

mostly describe output, routing, compact intent, or decision behavior. They say what Seed should emit or route toward, not what kind of user input was received.

That creates ambiguity:

- A factual question, a correction acknowledgment, and a casual thanks may all route to `answer`, but they are different kinds of user input.
- A user-provided observation may need acknowledgment, clarification, evidence handling, or future state update logic, but it is not itself an `answer`.
- A documentation claim may require claim support checks or clarification, but it is not the same thing as a command.
- A command request may become `request_tool`, `call_tool`, `propose_action_plan`, or `refuse`, but it remains a command request as input.

The gap is therefore not missing routing vocabulary. The gap is missing input-act vocabulary that can be preserved before Seed chooses a route.

## Initial Vocabulary

### `operator_query`

#### Definition

An `operator_query` is a user question asking Seed to explain, summarize, compare, inspect, or report what Seed knows, believes, can infer, or can do. The user is primarily seeking information, not directly requesting an external side effect.

#### Examples

- `What does Seed know about ProjectionStore?`
- `Why did Seed choose request_tool instead of call_tool?`
- `Can Seed explain the capability boundary here?`

#### Likely downstream handling

Likely downstream handling is to answer from existing context, ask a clarifying question when the query is ambiguous, or request a missing capability if the query requires unavailable external/current inspection.

#### What it is not

- It is not a `command_request` merely because it mentions a tool, host, file, or subsystem.
- It is not a `documentation_claim` unless the user is asserting what documentation says.
- It is not a `user_observation` unless the user is reporting a fact about the world.

#### Relationship to existing `DecisionKind` values

An `operator_query` often maps to `answer`. It may map to `ask_question` when clarification is needed, `request_tool` when the query requires unavailable capability, or `refuse` if answering would violate policy. The input act does not guarantee any specific route.

### `command_request`

#### Definition

A `command_request` is a user request for Seed to perform, initiate, plan, change, install, run, execute, configure, inspect externally, or otherwise cause an action. The distinguishing feature is that the user wants Seed to do something beyond merely answering.

#### Examples

- `Install Docker on example_host_b.`
- `Check whether web_service is listening on port 8096.`
- `Create a state patch for the corrected host mapping.`

#### Likely downstream handling

Likely downstream handling is capability and policy evaluation, followed by a safe route such as requesting a missing tool, proposing an action plan, calling an available tool, asking for clarification, or refusing.

#### What it is not

- It is not automatically executable.
- It is not a bypass around validation, tool guards, policy gates, pending-action gates, or registered-tool boundaries.
- It is not the correct label for every sentence that mentions infrastructure or operations.
- It is not the same as `request_tool`; `request_tool` is one possible runtime decision when Seed lacks an available capability.

#### Relationship to existing `DecisionKind` values

A `command_request` may map to `request_tool`, `propose_action_plan`, `call_tool`, or `refuse` depending on policy and capability. It may also map to `ask_question` if the requested action is underspecified. It should never imply direct `ToolExecutor` access without the existing `call_tool` route and guard/validation path.

### `user_observation`

#### Definition

A `user_observation` is a user-provided report about the world, environment, repository, system state, or operational situation. The user is contributing information rather than asking a question or issuing a command.

#### Examples

- `web_service is running on example_host_b.`
- `The local Docker daemon is down.`
- `The repository has no docs check configured.`

#### Likely downstream handling

Likely downstream handling is acknowledgment, clarification, reconciliation with existing context, evidence/caveat handling, or future observation intake if an implementation adds one. Seed may answer directly or ask a question when the observation is ambiguous, unsupported, or conflicts with existing knowledge.

#### What it is not

- It is not an external observation made by Seed.
- It is not a `command_request` unless the user asks Seed to verify, change, or act on the observation.
- It is not a documentation claim unless the observation specifically asserts what documentation says.
- It is not automatically a durable fact without whatever future validation, evidence, or state-update path is explicitly implemented.

#### Relationship to existing `DecisionKind` values

A `user_observation` may map to `answer` for acknowledgment or explanation. It may map to `ask_question` if Seed needs clarification. A future implementation may route it toward explicit observation intake, but this document does not add that behavior.

### `documentation_claim`

#### Definition

A `documentation_claim` is a user assertion about what a document, README, audit, comment, design note, or other text says. It is specifically about a documented claim rather than directly about the external world.

#### Examples

- `README says ToolExecutor owns execution.`
- `The audit says Runtime is the canonical route owner.`
- `docs/invariants.md says request_tool does not execute.`

#### Likely downstream handling

Likely downstream handling is to compare the claim against available documentation, answer with support or caveats, ask where the claim appears, or request capability if the relevant document cannot be inspected. It may also feed future claim-support or documentation-observation workflows.

#### What it is not

- It is not necessarily true just because the user phrases it as a documentation claim.
- It is not a `user_observation` about runtime state unless the claim is separately verified against the system.
- It is not a `command_request` unless the user asks Seed to update, verify, rewrite, or act on the documentation.

#### Relationship to existing `DecisionKind` values

A `documentation_claim` may map to `answer` when Seed can evaluate or contextualize the claim. It may map to `ask_question` when the referenced document or claim is ambiguous. It may map to `request_tool` if documentation access requires unavailable capability, or `refuse` if policy prevents the requested handling.

### `correction`

#### Definition

A `correction` is a user statement that revises, negates, or supersedes previous information, an earlier assistant answer, a stored assumption, or a current conversational premise.

#### Examples

- `No, example_host_b is not the web_service host anymore.`
- `Actually, the port is 8097, not 8096.`
- `Correction: the README does not say ToolExecutor owns every action.`

#### Likely downstream handling

Likely downstream handling is acknowledgment, conflict identification, clarification, caveated answer, or future correction intake if an implementation adds one. Corrections often require preserving both the corrected claim and the target of the correction.

#### What it is not

- It is not automatically a state mutation.
- It is not automatically more authoritative than existing evidence.
- It is not merely a casual answer just because it starts conversationally.
- It is not a command unless the user asks Seed to apply, record, patch, or propagate the correction.

#### Relationship to existing `DecisionKind` values

A `correction` may map to `answer` for acknowledgment or explanation, `ask_question` when the correction target is unclear, `propose_state_patch` if a future or existing route explicitly proposes a state change, or `refuse` if the requested correction handling is unsafe or disallowed. The correction itself should not bypass validation or policy.

### `casual_answer`

#### Definition

A `casual_answer` is conversational user input that acknowledges, thanks, confirms, declines, or otherwise continues the interaction without introducing a substantive new query, command, observation, documentation claim, or correction.

#### Examples

- `Thanks, that makes sense.`
- `Okay.`
- `Yes, that's fine.`

#### Likely downstream handling

Likely downstream handling is a brief conversational answer, acknowledgment, or no-op-like response. If the casual answer resolves a previous clarification question, Seed may use the surrounding context to continue the prior task safely.

#### What it is not

- It is not automatically an authorization for a pending side effect.
- It is not a `command_request` unless the user clearly requests an action.
- It is not a `correction` unless it revises prior information.
- It is not an `operator_query` unless it asks a question.

#### Relationship to existing `DecisionKind` values

A `casual_answer` usually maps to `answer`. It may map to `ask_question` if the conversational context remains ambiguous. It must not be treated as implicit approval to execute tools or bypass pending-action policy.

## Example Mapping Table

| User text | InputAct | Possible `DecisionKind` |
| --- | --- | --- |
| `What does Seed know about ProjectionStore?` | `operator_query` | `answer` |
| `web_service is running on example_host_b.` | `user_observation` | `answer` or `ask_question` |
| `README says ToolExecutor owns execution.` | `documentation_claim` | `answer` or `ask_question` |
| `No, example_host_b is not the web_service host anymore.` | `correction` | `answer` or `ask_question` |
| `Install Docker on example_host_b.` | `command_request` | `request_tool`, `propose_action_plan`, `call_tool`, or `refuse` depending on policy and capability |
| `Thanks, that makes sense.` | `casual_answer` | `answer` |

The table is illustrative, not a routing specification. The `InputAct` column describes the user input. The `DecisionKind` column describes possible downstream runtime choices after existing decision, validation, guard, policy, and capability logic.

## Relationship To Existing Input Inspection

`docs/input_inspection_reconciliation.md` documents that Seed already has an input-inspection and routing path:

```text
raw user text
  -> intent decision
  -> validation
  -> guard
  -> runtime route
```

This vocabulary should extend that existing input-inspection vocabulary rather than replace `Runtime` routing. In particular:

- `Runtime.handle_user_message` remains the canonical intake and routing entry point.
- `Runtime._route` remains the runtime route owner for validated decisions.
- `DecisionKind`, `Decision`, `IntentDecisionModel`, `TextIntentClassifier`, `IntentPromptModelClient`, `StrictJSONIntentParser`, `DecisionBuilder`, deterministic fallback, normalization, `DecisionValidator`, `ToolIntentGuard`, `ContextComposer`, and `scripts/seed_local.py` remain existing components of the current path.
- Input-act vocabulary should give Seed words for the user utterance before output/routing decisions are made.
- Input-act vocabulary should not turn natural language into LLM-only routing, policy bypass, or direct tool execution.

## Future Implementation Boundary

A future implementation should likely add an immutable input-inspection record that preserves an input act classification alongside the raw user text. This document does not require that implementation.

A possible future shape is:

```text
InputInspection:
  raw_text: str
  input_act: InputAct
  confidence or certainty field: optional/future
  reason: str
  source: local_classifier | prompt_model | fallback
```

This shape is future-facing and documentation-only. It is not implemented by this task. If implemented later, it should remain narrow, immutable, auditable, and subordinate to existing validation, guard, policy, capability, and runtime-route boundaries.

## Rejected Solutions

This vocabulary does not recommend or introduce:

- requiring robotic prefixes such as `seed, I have a question`;
- adding `InputEngine`, `ConversationEngine`, `CommandEngine`, or a new `RuntimeLoop`;
- rewriting `Runtime`;
- changing `ToolExecutor`, `EventLedger`, or `ProjectionStore`;
- bypassing `DecisionValidator`;
- bypassing `ToolIntentGuard`;
- bypassing policy, pending-action, capability, or registered-tool boundaries;
- treating all natural language as `command_request`;
- treating all non-commands as `answer`;
- using LLM-only classification with no deterministic fallback;
- making `request_tool` executable;
- allowing an input act to pre-authorize `call_tool`.

## Documentation-Only Status

This document defines vocabulary only. It does not modify runtime behavior, tests, route ownership, validation rules, guard behavior, policy behavior, tool execution, event ledger behavior, projection behavior, or local CLI behavior.
