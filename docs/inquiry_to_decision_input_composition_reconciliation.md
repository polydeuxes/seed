# Inquiry to Decision Input Composition Reconciliation

## Central finding

Yes: the repository already exposes a bounded composition seam between inquiry and decision production, but the seam is not an inquiry-specific runtime. The implementation-backed owner of the transition into a `DecisionInputPacket` is `DecisionInputComposer`. Question-family/bounded-inquiry surfaces own their own read-only answering and dispatch eligibility. Runtime transports the composed packet to a `DecisionProducer` and later routes the validated decision. Decision production consumes the packet; it does not own inquiry or rebuild bounded-inquiry answers.

## Commands executed

- `pwd && find .. -name AGENTS.md -print && git status --short`
- `cat AGENTS.md && rg -n "DecisionInputComposer|DecisionInputPacket|DecisionProducer|bounded inquiry|Question Families|QuestionFamily|decision adapter|runtime routing|Runtime" .`
- `sed -n '1,180p' seed_runtime/context.py && sed -n '1,430p' seed_runtime/runtime.py`
- `rg -n "Inquiry|inquiry|QuestionFamily|Question Family|bounded" seed_runtime tests docs | head -300`
- `rg -n "bounded_ask|Question.*Family|question.*family|QUESTION" seed_runtime scripts tests/test_question_surface_inventory.py | head -250`
- `sed -n '1,420p' seed_runtime/question_surface_inventory.py && sed -n '2100,2180p' scripts/seed_local.py`
- `python scripts/seed_local.py ask --question-surface-inventory --json | head -80`

## Files inspected

- `AGENTS.md`
- `seed_runtime/context.py`
- `seed_runtime/runtime.py`
- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `seed_runtime/models.py`
- `seed_runtime/state.py`
- `seed_runtime/observation_sources.py`
- `tests/test_question_surface_inventory.py`
- Supporting search hits in `docs/architecture.md`, `docs/architectural_status_and_next_frontier.md`, and inquiry-related documentation.

## Files changed

- `docs/inquiry_to_decision_input_composition_reconciliation.md`

## LOC changed

- Added one documentation report file.

## Implementation observations

### 1. Current inquiry output contributing to `DecisionInputPacket`

Current inquiry output can contribute to `DecisionInputPacket` when it has become implementation-backed projected state or current input. The direct packet fields are:

| Packet field | Source owner | Boundary demonstrated |
| --- | --- | --- |
| `current_input` | Runtime records `input.user_message`; `DecisionInputComposer` includes the input event payload | Operator inquiry text can enter the packet as input, but not as interpreted inquiry state. |
| `active_goal` | State projection owns goals; `DecisionInputComposer` selects the active goal | Goal `open_questions` can be present because prompt rendering includes them from `active_goal`. |
| `facts` | State projection owns facts; `DecisionInputComposer` orders/budgets facts | Completed observation/inquiry-derived facts can become decision input as facts. |
| `evidence` | State projection owns evidence; `DecisionInputComposer` orders/budgets evidence | Observation-source question metadata can be carried as evidence payload, including `question_answered`, but composer does not reason over it. |
| `open_tool_needs` | ToolNeed projection/service owns tool needs; `DecisionInputComposer` selects open needs | Prior decisions or recorded needs can influence later decision input. |
| `tools` | Tool registry owns registered visible tools; `DecisionInputComposer` lists visible tool specs | Tool availability is composed into decision input separately from inquiry. |
| `decision_schema` | `DecisionInputComposer` owns allowed decision kind exposure | Decision shape constraints are composed, not inferred from inquiry. |
| `context_budget` | `ContextBudget` selection trace owned by context selection/composer | Selection visibility is included as composition trace. |

There is no implementation evidence that bounded question-family surface output is directly injected into `DecisionInputPacket` as a first-class `inquiry_result` field. Instead, completed inquiry participates only through existing boundaries: current input, projected goals/facts/evidence/tool needs, and selected context.

### 2. Owner of Inquiry → Decision Input

The transition owner is `DecisionInputComposer` for packet construction. Runtime owns when composition happens, because it records input, projects state, invokes `compose`, and passes the result to `DecisionProducer`. Question Families own bounded inquiry surface eligibility and dispatch to exact answering surfaces, but they do not own `DecisionInputPacket`. DecisionProducer owns decision production from an already-built packet and does not own composition.

This means the ownership split is:

- Question Families: bounded inquiry surface inventory, eligibility, exact CLI dispatch, and answering responsibility for those surfaces.
- DecisionInputComposer: decision-input construction from current input, projected state, registry, context budget, and schema.
- Runtime: orchestration and transport of the composed packet to decision production, then validation/routing of the returned decision.
- DecisionProducer: decision production from the packet.

### 3. Runtime role

Runtime does not interpret inquiry in the observed path. Runtime appends the user input event, projects state, asks `DecisionInputComposer` to compose the packet, calls `decision_producer.decide(packet)`, validates, applies a tool-intent guard, and routes validated decisions to response, tool-need, tool-execution, state-patch, or refusal branches. Its own architecture metadata describes it as routing validated model decisions to owner services without owning their behavior.

Runtime can add retry prompts to the already composed `DecisionInputPacket` after parse, schema, validation, or intent failures. That is correction context for decision production, not inquiry interpretation.

### 4. DecisionInputComposer role

`DecisionInputComposer` performs composition and selection, not reasoning. Its implementation orders goals, entities, facts, evidence, and tool needs; asks `ContextBudget` to select sections; serializes selected dataclasses; attaches selected evidence to selected facts; lists visible tools; and emits the decision schema and context-budget trace. It does not call question-family surfaces, run bounded inquiries, infer conclusions, produce decisions, execute tools, or mutate state.

### 5. Inquiry reasoning duplication during decision production

No direct duplication was found in the canonical decision path. Decision prompt rendering summarizes packet content for a model decision: current input, relevant state summary, visible tools, open tool needs, allowed decision shapes, and optional retry prompts. Rendering excludes runtime bookkeeping and tool implementation details. It does not re-run question-family dispatch or bounded inquiry evaluators.

The strongest caveat is that a model-backed `DecisionProducer` may reason over the packet text to choose a decision. That is decision reasoning over composed inputs, not duplicated implementation-backed bounded-inquiry reasoning. The implementation-backed code does not duplicate inquiry evaluators during production.

### 6. Can completed inquiry become decision input without new architecture?

Yes, if completed inquiry is represented through existing implementation-backed state/input boundaries. The cleanest existing routes are:

1. preserved/projected facts and evidence;
2. goal `open_questions` or related goal context;
3. recorded/open tool needs;
4. operator current input;
5. evidence payload metadata such as `question_answered` from observation sources.

No new planner, scheduler, agent loop, autonomous reasoning runtime, or decision-engine redesign is required for those routes. The repository already has the packet boundary and producer protocol needed for composed state to participate in decision production.

### 7. Strongest contradictory evidence

The strongest contradictory evidence is intentional independence:

- Question-family inventory maps bounded ask surfaces to read-only exact diagnostics and states many boundaries as no recording, no event-ledger writes, no mutation, no routing, or not dispatchable.
- `apply_bounded_ask_dispatch` maps `ask --question-family` to CLI diagnostic/read-only surfaces, not to Runtime or `DecisionInputComposer`.
- Inquiry documentation repeatedly warns against promoting inquiry to runtime, workflow, planner, or formal ontology without reconciliation.
- `DecisionInputPacket` has no explicit `inquiry_result`, `question_family_result`, or `bounded_inquiry_result` field.
- Runtime's canonical path is decision-oriented, while question-family/bounded ask is diagnostic/presentation-oriented.

These do not disprove the composition seam. They show that the seam is generic state/input composition, not a dedicated inquiry-to-decision architecture.

## Composition summary

The repository already exposes a clean generic composition boundary:

```text
Projected state + current input + visible tools + open tool needs
        ↓
DecisionInputComposer.compose(...)
        ↓
DecisionInputPacket
        ↓
DecisionProducer.decide(...)
        ↓
Runtime validation and routing
```

Completed inquiry can participate when its output is already part of projected facts/evidence/goals/tool needs or is supplied as current input. Question Families do not bypass the composer, and Runtime does not reinterpret the inquiry output.

## Required answers

### Does the repository already expose a clean composition boundary between inquiry and decision production?

Yes, with an important qualifier: the boundary is not named as an inquiry-specific seam. It is the existing `DecisionInputComposer` → `DecisionInputPacket` boundary. It is clean because packet construction is isolated from decision production, and decision producers receive a single composed input object.

### Who owns that transition?

`DecisionInputComposer` owns construction of decision input. Runtime owns invoking that construction in the user-message path and transporting the resulting packet to `DecisionProducer`. Question Families own bounded inquiry surfaces and dispatch eligibility, not the packet boundary. DecisionProducer owns production of a decision from the packet, not the Inquiry → Decision Input transition.

### Can inquiry already participate in decision production without new architectural concepts?

Yes. Inquiry can participate through existing projected state and current input fields. The bounded implementation slice is to prove and preserve that existing route, not to introduce a new architecture.

## Recommended bounded implementation slice

Add a focused test that creates an inquiry-shaped completed result as existing projected state, composes a `DecisionInputPacket`, and asserts that the result appears in the relevant packet fields and rendered decision prompt. The test should not add runtime redesign or new concepts. A good slice would be:

- seed an `evidence.created` or equivalent existing event with payload metadata such as `question_answered`;
- seed a supported fact attached to that evidence;
- run `DecisionInputComposer.compose(...)` directly;
- assert that `DecisionInputPacket.facts`, `DecisionInputPacket.evidence`, and rendered prompt state summary include the expected content;
- optionally run `Runtime.handle_user_message(...)` with a `StaticDecisionProducer` and assert the producer's `last_decision_input` contains the same fields.

This would demonstrate the existing seam end to end while preserving current ownership: inquiry result as projected evidence/fact, composer as packet owner, runtime as transport, producer as consumer.
