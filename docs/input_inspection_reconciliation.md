# Input Inspection Reconciliation

## Purpose

This audit documents Seed's existing input-inspection, intent-classification, and decision-routing structure without changing runtime behavior. The motivating question is whether the current system already lets users speak naturally, for example `seed, I have a question`, without requiring robotic command-prefix syntax.

The answer is mixed:

- Seed already has a real input-inspection path: raw text is recorded, composed into decision context, classified or decided, validated, guarded, and routed.
- The current vocabulary is decision/action oriented, not conversational-act oriented.
- The current implementation can support natural text when the classifier or deterministic fallback maps it into existing labels, but it does not explicitly model operator query, command/task request, observation, documentation claim, correction, or casual answer as first-class input categories.

## Existing Surfaces

### Runtime input and route surfaces

- `Runtime.handle_user_message` is the canonical intake for user text. It appends an `input.user_message` event, projects state, composes context, asks the configured model for a `Decision`, records `model.decision.proposed`, validates, applies the tool-intent guard, and routes the valid decision.
  - Code: `seed_runtime/runtime.py`.
- `Runtime._route` maps valid decisions to response surfaces or owner services:
  - `answer` -> `response.answer` event and `RuntimeResponse(kind="answer")`.
  - `ask_question` -> `response.question` event and `RuntimeResponse(kind="question")`.
  - `request_tool` -> `ToolNeedService` plus capability resolution/recommendations and `RuntimeResponse(kind="tool_need")`.
  - `call_tool` -> `ToolExecutor.execute` and the executor's result.
  - `propose_state_patch` -> `StatePatchService.apply`.
  - `refuse` -> `response.refusal` event and `RuntimeResponse(kind="refusal")`.

### Decision model and compact intent surfaces

- `DecisionKind` in `seed_runtime/models.py` contains the runtime decision vocabulary.
- `Decision` stores the selected `kind`, `reason`, and kind-specific fields such as `answer`, `question`, `tool_name`, `tool_arguments`, `tool_need`, and `state_patch`.
- `IntentDecisionProducer` adapts compact intent classification into full runtime `Decision` objects.
- `TextIntentClassifier` wraps an `IntentPromptModelClient` and parses strict JSON into an `IntentClassification`.
- `IntentPromptModelClient` renders a provider-neutral intent prompt and delegates completion to a text transport.
- `StrictJSONIntentParser` only accepts JSON objects containing `intent`, `reason`, and optional object-valued `arguments`.
- `DecisionBuilder` maps compact intent labels into full `Decision` kinds.

### Deterministic fallback and normalization surfaces

- `deterministic_intent_fallback` handles high-confidence local cases before calling a classifier:
  - `echo ...` -> compact `echo` intent.
  - inputs matching missing-tool patterns are left for classifier/fallback missing-tool handling.
  - informational patterns such as `what is ...`, `who is ...`, `explain ...`, and `define ...` become compact `answer` intents.
- `_normalize_classification_for_input` prevents certain unsafe/incorrect compact labels from surviving:
  - if missing-tool patterns match but the classifier returned `answer`, it rewrites to `missing_tool`.
  - if an informational pattern was classified as `missing_tool` and no missing-tool pattern matched, it rewrites to `answer`.

### Validation and guard surfaces

- `DecisionValidator` validates required fields for `answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, and `refuse`.
- `ToolIntentGuard` adds deterministic checks for `call_tool` decisions:
  - non-`call_tool` decisions pass through.
  - the tool must be visible to the model.
  - the built-in `echo` tool must only be called when input starts with `echo ` and the argument must exactly match the text after that prefix.
- Runtime retries invalid parsed decisions, invalid decisions, and intent-rejected tool calls through retry context instead of bypassing validation.

### Context-composition surfaces

- `DecisionInputComposer.compose` includes the current input event payload, active goal, entities, recent facts, recent evidence, visible tools, open tool needs, a decision schema, and context-budget trace in a `DecisionInputPacket`.
- The context decision schema currently advertises only `answer`, `ask_question`, `call_tool`, `request_tool`, and `refuse` to the composed context, even though the broader `DecisionKind` type also includes proposal/state-patch legacy or side-path kinds.
- `build_intent_prompt` narrows compact classifier output to `echo`, `answer`, `missing_tool`, `clarify`, and `refuse` and includes guidance for general informational questions, visible tools, missing capabilities, external/current information, actions, and observations of the world.

### Local CLI intent path

- `scripts/seed_local.py` constructs the local app with `DecisionInputComposer`, `IntentPromptModelClient.for_endpoint`, `TextIntentClassifier`, `IntentDecisionProducer`, `DecisionValidator`, `ToolExecutor`, `ToolNeedService`, and canonical `Runtime`.
- One-shot CLI messages are joined into a single string and passed through `LocalSeedApp.run`, which calls `Runtime.handle_user_message`.
- The CLI description explicitly says it runs Seed locally with Ollama `/api/generate` intent classification.

### Documentation surfaces already present

- `docs/invariants.md` states that `Runtime` is canonical, `request_tool` records/resolves a capability gap and does not execute, and `call_tool` is the only `Runtime` path to `ToolExecutor`.
- `docs/function_blocks.md` draws the execution boundary from `DecisionValidator` to runtime branches and states that only `call_tool` may enter `ToolExecutor`.
- `docs/response_vocabulary.md` maps runtime `answer`, `ask_question`, `refuse`, `tool_need`, `tool_result`, invalid-decision, and state-update responses into response categories.
- `docs/state_patch_inventory.md` already summarizes the `Runtime.handle_user_message` validation/routing sequence.

## Current Vocabulary

### Runtime decision vocabulary

`DecisionKind` currently includes:

| Decision kind | Current meaning in code |
| --- | --- |
| `answer` | Return direct answer text. |
| `ask_question` | Ask the user for missing information. |
| `call_tool` | Execute a visible registered tool through `ToolExecutor`. |
| `request_tool` | Record a missing capability/tool need and return capability-resolution metadata. |
| `propose_action_plan` | Legacy/experimental text-only side-path vocabulary in the domain model; not part of the composed decision schema. |
| `propose_handoff_plan` | Legacy/experimental handoff-plan side-path vocabulary in the domain model; not part of the composed decision schema. |
| `propose_state_patch` | Runtime-supported state-patch side path in `Runtime._route`, but not advertised by the current composed decision schema. |
| `refuse` | Return a refusal reason. |

### Context-advertised decision vocabulary

`DecisionInputComposer` currently advertises this narrower schema to model context:

- `answer`
- `ask_question`
- `call_tool`
- `request_tool`
- `refuse`

### Compact intent vocabulary

The intent-classifier path currently uses compact labels:

| Compact label | Built runtime decision |
| --- | --- |
| `echo` | `call_tool` with `tool_name="echo"`. |
| `answer` | `answer`. |
| `missing_tool` | `request_tool`. |
| `clarify` | `ask_question`. |
| `refuse` | `refuse`. |

### Response vocabulary reached by this path

The route can produce at least these response kinds:

- `answer`
- `question`
- `tool_need`
- executor-provided tool-result kinds for `call_tool`
- `state_updated`
- `invalid_state_patch`
- `refusal`
- `invalid_decision`
- `unsupported`

## Current Flow

The existing code path is:

```text
raw user text
  -> Runtime.handle_user_message
  -> input.user_message event
  -> StateProjector.project
  -> DecisionInputComposer.compose(DecisionInputPacket)
  -> DecisionProducer.decide
     -> IntentDecisionProducer.decide for the local CLI path
        -> deterministic_intent_fallback, or TextIntentClassifier.classify
        -> IntentPromptModelClient.complete(build_intent_prompt(context))
        -> StrictJSONIntentParser.parse
        -> _normalize_classification_for_input
        -> DecisionBuilder.build
  -> model.decision.proposed event
  -> DecisionValidator.validate
  -> ToolIntentGuard.validate for call_tool intent constraints
  -> Runtime._route
     -> answer response, question response, ToolNeed/capability-resolution response,
        ToolExecutor execution, state-patch service, or refusal response
```

Important boundaries in this flow:

- `request_tool` is capability-gap intake, not execution.
- `call_tool` is the only canonical runtime path into `ToolExecutor`.
- `ToolIntentGuard` does not replace the classifier; it only applies deterministic checks to tool-call decisions.
- The prompt/classifier may choose labels, but routing remains constrained by `DecisionValidator`, `ToolIntentGuard`, `Runtime._route`, and policy/execution services downstream of `ToolExecutor`.

## What Already Works

- Seed already records raw user input as an event before model decision-making.
- Seed already composes a context packet that exposes current input, state, visible tools, and open tool needs to the decision path.
- Seed already has an intent-first local classifier path that asks for compact labels rather than full decision JSON.
- Seed already has deterministic fallback for simple `echo` input and simple informational questions.
- Seed already has a deterministic missing-tool bias for actions, lookups, external/current information, system/file/network operations, weather, Docker inspection, and observations of the world.
- Seed already separates missing capability requests from tool execution: `request_tool` records a `ToolNeed`, while only `call_tool` can reach `ToolExecutor`.
- Seed already rejects a schema-valid but intent-invalid `echo` tool call when the raw input does not start with `echo `.
- Seed already asks clarification questions through `clarify` -> `ask_question`.

## What Does Not Exist Yet

The current code does **not** expose first-class input categories for:

- operator query;
- command / task request;
- observation;
- documentation claim;
- correction;
- casual answer.

Some of these concepts can be approximated by current decision labels:

- operator query -> often `answer` or `ask_question`;
- command/task request -> often `call_tool`, `request_tool`, `propose_state_patch`, or `refuse` depending on capability and safety;
- observation -> currently biased toward `missing_tool` when it asks Seed to observe the world, but there is no dedicated observation-intake category for user-provided observations;
- documentation claim -> no dedicated claim-intake category in this path;
- correction -> no dedicated correction-intake category in this path;
- casual answer -> could become `answer` or `clarify` depending on classifier behavior, but it is not a first-class category.

Therefore, Seed can distinguish these cases only indirectly and inconsistently, through prompt behavior, regex heuristics, state context, and downstream decision validation. It cannot currently report or preserve the distinction as an explicit input-inspection result.

## Conversational Input Gap

Seed can accept natural text in the limited sense that `Runtime.handle_user_message` accepts arbitrary strings and the classifier prompt contains conversational guidance. There is no runtime requirement that the user type `echo`, `ask`, `answer`, or another command prefix for every interaction.

However, Seed does **not** yet have enough explicit input-inspection vocabulary to reliably understand meta-conversational openings such as:

```text
seed, I have a question
```

The smallest gap is **missing vocabulary plus under-documented existing behavior**, not a missing runtime loop.

More specifically:

1. **Missing vocabulary**: there is no first-class category for conversational setup, operator query, user-provided observation, documentation claim, correction, or casual answer.
2. **Classifier behavior is under-specified for conversational setup**: the prompt says to use `answer` for conversational replies or directly answerable questions, but it does not define how to treat prefaces like `I have a question`, user corrections, claims, or observations.
3. **Routing behavior mostly exists for the current vocabulary**: `answer`, `ask_question`, `request_tool`, `call_tool`, and `refuse` are routed, validated, and documented elsewhere.
4. **Observation/claim intake is missing from this path**: user-provided observations and documentation claims are not accepted as explicit input kinds before decision routing.
5. **Docs were incomplete for this exact reconciliation question**: existing docs document routing and response boundaries, but not the full relationship between input inspection, compact intent labels, decision kinds, and conversational naturalness.

## Ownership Boundaries

This audit preserves the current boundaries:

- `Runtime` remains the canonical route owner.
- `DecisionInputComposer` owns composition of current input and relevant state into `DecisionInputPacket`.
- `IntentDecisionProducer`, `TextIntentClassifier`, `IntentPromptModelClient`, `StrictJSONIntentParser`, and `DecisionBuilder` own the local compact-intent-to-decision adaptation path.
- `DecisionValidator` owns structured decision validation.
- `ToolIntentGuard` owns deterministic tool-call intent checks.
- `ToolNeedService` owns `request_tool` capability-gap creation and resolution support.
- `ToolExecutor` owns registered-operation execution only after a valid `call_tool` route.
- Policy gates and pending-action handling remain downstream execution boundaries and must not be bypassed.

## Rejected Solutions

This audit does not recommend or introduce:

- `InputEngine`;
- `ConversationEngine`;
- `CommandEngine`;
- a new `RuntimeLoop`;
- default `ToolExecutor` integration for `request_tool`;
- LLM-only routing;
- bypassing `DecisionValidator`, `ToolIntentGuard`, policy gates, pending-action gates, or registered-tool boundaries.

These would duplicate or bypass existing surfaces rather than addressing the smallest documented gap.

## Follow-up

See `docs/input_act_vocabulary.md` for the documentation-only first-class vocabulary that distinguishes user input acts from downstream `DecisionKind` routing decisions.

## Recommended Next Step

Add a small, explicit input-inspection vocabulary only if a future behavior change is approved. The likely next design task is to define how current compact intent labels should relate to user input acts such as operator query, task request, user-provided observation, documentation claim, correction, and casual answer.

The next implementation should remain narrow:

- do not replace `Runtime`;
- do not make `request_tool` executable;
- do not bypass validation or policy;
- do not add a broad engine;
- start by documenting or extending classifier guidance and preserving explicit input-act metadata only where it has a routed owner.

Until then, the correct documentation-level conclusion is:

> Seed has an input-inspection and decision-routing path, but it does not yet have first-class conversational/input-act categories. Natural conversational input is possible but not structurally guaranteed, and the main gap is vocabulary/classifier specification plus observation/claim/correction intake, not runtime routing.
