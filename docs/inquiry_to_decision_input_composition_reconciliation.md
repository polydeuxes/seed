# Inquiry to Decision Input Composition Reconciliation

## Central finding


## Commands executed

- `pwd && find .. -name AGENTS.md -print && git status --short`
- `rg -n "Inquiry|inquiry|QuestionFamily|Question Family|bounded" seed_runtime tests docs | head -300`
- `rg -n "bounded_ask|Question.*Family|question.*family|QUESTION" seed_runtime scripts tests/test_question_surface_inventory.py | head -250`
- `sed -n '1,420p' seed_runtime/question_surface_inventory.py && sed -n '2100,2180p' scripts/seed_local.py`
- `python scripts/seed_local.py ask --question-surface-inventory --json | head -80`

## Files inspected

- `AGENTS.md`
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



| Packet field | Source owner | Boundary demonstrated |
| --- | --- | --- |


### 2. Owner of Inquiry → Decision Input


This means the ownership split is:

- Question Families: bounded inquiry surface inventory, eligibility, exact CLI dispatch, and answering responsibility for those surfaces.
- Runtime: orchestration and transport of the composed packet to decision production, then validation/routing of the returned decision.
- DecisionProducer: decision production from the packet.

### 3. Runtime role





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
- Inquiry documentation repeatedly warns against promoting inquiry to runtime, workflow, planner, or formal ontology without reconciliation.
- Runtime's canonical path is decision-oriented, while question-family/bounded ask is diagnostic/presentation-oriented.

These do not disprove the composition seam. They show that the seam is generic state/input composition, not a dedicated inquiry-to-decision architecture.

## Composition summary

The repository already exposes a clean generic composition boundary:

```text
Projected state + current input + visible tools + open tool needs
        ↓
        ↓
        ↓
DecisionProducer.decide(...)
        ↓
Runtime validation and routing
```

Completed inquiry can participate when its output is already part of projected facts/evidence/goals/tool needs or is supplied as current input. Question Families do not bypass the composer, and Runtime does not reinterpret the inquiry output.

## Required answers

### Does the repository already expose a clean composition boundary between inquiry and decision production?


### Who owns that transition?


### Can inquiry already participate in decision production without new architectural concepts?

Yes. Inquiry can participate through existing projected state and current input fields. The bounded implementation slice is to prove and preserve that existing route, not to introduce a new architecture.

## Recommended bounded implementation slice


- seed an `evidence.created` or equivalent existing event with payload metadata such as `question_answered`;
- seed a supported fact attached to that evidence;
- optionally run `Runtime.handle_user_message(...)` with a `StaticDecisionProducer` and assert the producer's `last_decision_input` contains the same fields.

This would demonstrate the existing seam end to end while preserving current ownership: inquiry result as projected evidence/fact, composer as packet owner, runtime as transport, producer as consumer.
