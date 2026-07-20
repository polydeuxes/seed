# Decision Model And Context Naming Audit

## Scope

This report audits whether `DecisionModel`, `ContextComposer`, `ContextPacket`, and related `context` naming should be renamed before deeper inquiry/runtime integration. It is intentionally limited to naming and responsibility alignment. It does not implement renames, change runtime behavior, change the decision schema, introduce planning, introduce inquiry runtime, or alter execution.

## Files Inspected

Required files inspected:

- `seed_runtime/runtime.py`
- `seed_runtime/models.py`
- `seed_runtime/decisions.py`
- `tests/test_runtime_loop.py`
- `tests/test_execution.py`
- `tests/test_policy.py`
- `tests/test_execution_proposals.py`

Additional directly relevant implementation and docs inspected for blast radius:

- `scripts/seed_local.py`
- `tests/test_context.py`
- `tests/test_context_budget.py`
- `tests/test_model_client.py`
- `tests/test_model_clients.py`
- `tests/test_architecture_invariants.py`
- `tests/test_tool_recommendations.py`
- `tests/test_state_patches.py`
- `tests/test_capability_catalog.py`
- `tests/test_evidence_facts.py`
- `tests/test_fact_extraction.py`
- `tests/test_tool_validation.py`
- `docs/audit/context_knowledge_consolidation.md`
- `docs/runtime_runtime_loop_responsibility_audit.md`
- `docs/response_reconciliation.md`
- `docs/natural_language_execution_path_inventory_audit.md`

Repository-wide searches run:

- `rg -n "DecisionModel|ContextComposer|Context\b|context\b|decide\(context\)" . -g '!*.pyc'`
- `rg -n "DecisionModel|ContextComposer|ContextPacket|decide\(context\)|def decide\(|context_composer|last_context|Decision Context|decision-context" seed_runtime tests scripts docs -g '*.py' -g '*.md'`

## Current Responsibility

### `DecisionModel`


Implementation evidence:

- `FakeDecisionModel` stores the last input packet and returns a preconfigured `Decision`, proving the seam can be deterministic and non-LLM.
- `Runtime.handle_user_message` appends input, projects state, composes a packet, calls `self.model.decide(...)`, records `model.decision.proposed`, validates the returned `Decision`, and routes only after validation.

Answer to Question 1: `DecisionModel` owns only production of a proposed `Decision` from the current decision input packet. It does not own decision truth, runtime authority, routing, validation, execution, or policy.

Answer to Question 2: the name is partly stale. The seam is now generic enough to be implemented by deterministic fakes, local chat clients, parsed prompt clients, and intent classifiers. However, several implementations remain explicitly model/LLM-shaped, including prompt rendering and local chat model adapters. The safest implementation-backed reading is therefore: generic decision producer seam with legacy/model-backed implementations still present.

### `ContextComposer`

`ContextComposer` currently composes a compact `ContextPacket` from:

- workspace/session identifiers;
- the current input event payload;
- a single budget-selected active goal;
- budget-selected entities;
- budget-selected facts, with selected evidence attached only when that evidence survived the same budget pass;
- visible registered tools from `ToolRegistry` with schemas, policy actions, and risk classes;
- budget-selected open tool needs;
- a compact decision schema listing accepted decision kinds for the packet;
- budget-selected evidence;
- optional retry prompt metadata attached by `Runtime` through dataclass replacement;
- a context budget trace.

Answer to Question 3: `ContextComposer` composes a deterministic, budgeted, provider-facing decision input packet from projected runtime state, current input, visible tool inventory, open tool needs, selected evidence/facts/entities/goals, and schema metadata. It is not a general inquiry engine.

Answer to Question 4: `context` is mostly structured operational state, not a free-form prompt blob, at the `ContextPacket` boundary. The packet is a typed dataclass with structured sections and deterministic budget metadata. The stale part is that downstream model clients still render the structured packet into prompts, and retry metadata uses prompt-oriented wording such as `retry_prompt` and instructions for JSON-only output.

## Stale Vocabulary

### Stale or Partly Stale

| Current name | Assessment | Why |
| --- | --- | --- |
| `DecisionModel` | Partly stale | It implies the producer is a model, but runtime only requires a `decide(ContextPacket) -> Decision` protocol. Deterministic and intent-classifier implementations already satisfy the same seam. |
| `FakeDecisionModel` | Stale if the seam is renamed | It is a test decision source, not a fake model in any required architectural sense. |
| `ContextComposer` | Partly stale but less urgent | It accurately composes context, but `Context` can imply prompt/input blob or an old context-engine framing. The implementation composes bounded decision input from projected operational state. |
| `ContextPacket` | Partly stale | It is structured and budgeted, but `Context` alone is broad and collides with `ToolContext`, `DecisionContextView`, `RuntimeContext`, docs, and many presentation surfaces. |
| `context` parameter in `decide(context)` | Partly stale | It is structured decision input, not necessarily an LLM prompt, but prompt clients still consume it. |
| `retry_prompt` | More stale than `ContextComposer` | Runtime retry metadata is currently embedded in the packet under a prompt-specific name even though the runtime needs a retry instruction/advice section, not necessarily a prompt. |

### Not Stale Enough To Rename Alone

`Decision`, `Runtime`, `Policy`, `Registry`, and `Execution` still align with implementation and should not be renamed as part of this slice.

## Recommended Names

### Recommended Implementation-Backed Replacements

| Current | Recommended | Rationale |
| --- | --- | --- |
| `DecisionModel` | `DecisionProducer` | Most precise minimal name. It produces proposed `Decision` objects without claiming planning, inquiry, reasoning, orchestration, or LLM ownership. |
| `FakeDecisionModel` | `StaticDecisionProducer` or `FakeDecisionProducer` | `StaticDecisionProducer` best describes test behavior. `FakeDecisionProducer` is a low-friction alias during transition. |
| `context` parameter in producer protocol | `decision_input` | Avoids implying a prompt blob while keeping the method signature semantics obvious. |
| `retry_prompt` | Later: `retry_instruction` or `retry_feedback` | This is implementation-backed, but changing it touches packet schema/tests and should be a separate compatibility-aware slice. |

### Candidate Evaluation

| Candidate | Verdict | Reason |
| --- | --- | --- |
| `DecisionProducer` | Prefer | Minimal, implementation-backed, neutral about source. |
| `DecisionSource` | Acceptable alias only | Indicates origin, but less active than the `decide(...)` behavior and may blur source vs producer. |
| `DecisionProposer` | Acceptable but slightly weaker | Captures proposed-decision status, but sounds like a higher-level proposal subsystem and overlaps with execution proposals. |
| `RuntimeInputComposer` | Not preferred | Too broad; the packet is not all runtime input, only decision-producer input. |
| `OperationalStateComposer` | Not preferred | Overclaims: composer includes current input, tool inventory, schema, and budget trace, not complete operational state. |
| `Planner`, `ReasoningEngine`, `InquiryEngine`, `AutonomousOrchestrator` | Reject | The implementation does not support these responsibilities. |


## Blast Radius

### Runtime And Core Modules

A rename would likely touch:

- `seed_runtime/runtime.py`: protocol, fake/static implementation, constructor type, `self.model` naming if desired, local variables `context`/`retry_context`, retry helper signatures, and `context_composer` property if renamed.
- `scripts/seed_local.py`: app wiring imports, app fields, local runtime wrappers, CLI app construction.

### Tests

At minimum, test imports and helper classes would be touched in:

- `tests/test_runtime_loop.py`
- `tests/test_context.py`
- `tests/test_context_budget.py`
- `tests/test_model_client.py`
- `tests/test_model_clients.py`
- `tests/test_architecture_invariants.py`
- `tests/test_tool_recommendations.py`
- `tests/test_state_patches.py`
- `tests/test_capability_catalog.py`
- `tests/test_evidence_facts.py`
- `tests/test_fact_extraction.py`
- `tests/test_tool_validation.py`

The required review files `tests/test_execution.py`, `tests/test_policy.py`, and `tests/test_execution_proposals.py` are not primary rename blast-radius files for `DecisionModel`/`ContextComposer`; they are useful boundary checks because execution and policy should remain unaffected.

### Docs

Docs contain many references to `ContextComposer`, `ContextPacket`, `DecisionModel`, and context vocabulary. A full doc rename is large and should not be bundled with code aliases. The implementation slice should update only docs that describe current public APIs or architecture invariants. Historical audits can remain as historical references unless they are actively misleading.

Answer to Question 5: the rename touches runtime protocol/composer modules, provider/model-client adapters, intent/evaluation wiring, CLI app construction, and a broad but manageable set of tests. Execution, policy, and execution proposal implementation should not change.

## Safe Rename Order

1. Add compatibility names without behavior changes:
   - introduce `DecisionProducer = DecisionModel` or define `DecisionProducer` as the new protocol and retain `DecisionModel` as an alias;
   - introduce `StaticDecisionProducer` while retaining `FakeDecisionModel` as an alias.
3. Update tests to prefer the new names and add explicit compatibility tests proving old imports still work temporarily.
4. Update only current API/architecture docs that would otherwise misstate the seam. Leave historical audits alone unless refreshed.
5. In a later release/slice, deprecate old names with clear removal criteria after inquiry/runtime integration consumes the new names.
6. Consider a separate packet-field cleanup for `retry_prompt` -> `retry_instruction`/`retry_feedback`; do not mix that field/schema change into the class/protocol rename unless compatibility wrappers are in place.

## Compatibility Plan

Temporary aliases should remain because references are broad and some docs already distinguish legacy `ContextPacket`/`ContextComposer` from newer `RuntimeContext`/`RuntimeLoopContextComposer` paths.

Recommended aliases:

- `DecisionModel` remains an alias for `DecisionProducer` for at least one integration cycle.
- `FakeDecisionModel` remains an alias or subclass of `StaticDecisionProducer` until tests and external imports settle.

Avoid changing serialized packet field names in the first slice. In particular, keep `current_input`, `active_goal`, `open_tool_needs`, `decision_schema`, `context_budget`, and `retry_prompt` stable until a separate compatibility decision is made.

Answer to Question 8: compatibility aliases should remain temporarily for all public/semi-public names: `DecisionModel`, `FakeDecisionModel`, `ContextComposer`, and `ContextPacket`. The old aliases should be low-risk because they preserve imports and behavior while allowing new code to use better vocabulary.

## Tests Required

A rename implementation slice should run at least:

- `pytest -q tests/test_execution.py tests/test_policy.py tests/test_execution_proposals.py` as non-regression boundary checks proving execution/policy/proposal behavior was not changed.

If any diagnostic or audit surface is modified during a future implementation, also run:

- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

No diagnostic surfaces are modified by this report.

## Recommended Implementation Slice

The smallest safe implementation-backed slice is:

1. Introduce new names and aliases only.
3. Leave packet fields and event names unchanged.
5. Add alias/import tests.
6. Run the targeted tests listed above.

## Should This Happen Before Inquiry/Runtime Integration?


Do not rename toward inquiry-specific terms yet. The current implementation supports bounded decision input and proposed decision production; it does not yet support a planner, inquiry engine, reasoning engine, or autonomous orchestrator.

## Non-Goals

This audit does not recommend:

- changing `Decision` schema;
- changing event names such as `model.decision.proposed` in the same slice;
- changing runtime routing;
- changing validation, policy, or execution behavior;
- introducing a planner;
- introducing inquiry runtime;
- promoting presentation vocabulary into knowledge;
- changing `ContextPacket` serialized field names in the first rename slice;
- removing old names immediately.

## Acceptance Criteria Answers

### Are `DecisionModel` and `ContextComposer` stale names?

Yes, partly. `DecisionModel` is the more stale name because the protocol is now a generic proposed-decision producer seam, even though model-backed implementations still exist. `ContextComposer` is less stale but still broad; it composes structured decision input, not arbitrary context or an inquiry engine.

### What are the safest implementation-backed replacement names?

- `DecisionModel` -> `DecisionProducer`
- `FakeDecisionModel` -> `StaticDecisionProducer` with `FakeDecisionModel` retained temporarily
- `decide(context)` parameter -> `decide(decision_input)`

### Should the rename happen before deeper inquiry integration?

Yes. It should happen before deeper inquiry/runtime integration, but only as a small compatibility-preserving rename with aliases and no behavior/schema changes. That prevents the inquiry work from inheriting LLM-shaped or prompt-shaped vocabulary while avoiding premature claims about planners or inquiry engines.

## Files Changed

- `docs/decision_model_context_naming_audit.md`

## LOC Changed

This report adds one documentation file. The exact changed line count should be taken from `git diff --stat` for the commit that includes this report.

## Tests Run

No runtime behavior changed. Documentation-only validation and repository inspection commands were run; see the final response for exact commands and status.
