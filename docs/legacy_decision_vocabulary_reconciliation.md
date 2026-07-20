# Legacy decision vocabulary reconciliation

Date: 2026-06-25

## Scope and boundary

This is an observational audit after the compatibility rename from `DecisionModel`/`ContextComposer`/`ContextPacket`/`FakeDecisionModel` to `DecisionProducer`/`DecisionInputComposer`/`DecisionInputPacket`/`StaticDecisionProducer`. It does not remove aliases, rename events, rename serialized packet fields, rewrite historical documents, or change runtime behavior.

## Repository searches performed

Implementation and documentation searches were performed repository-wide with fixed-string `rg` for:

- `DecisionModel`
- `FakeDecisionModel`
- `ContextComposer`
- `ContextPacket`
- `last_context`
- `context_composer`
- `context_packet`
- `decide(context)`
- `context:`
- `model.decision`
- `retry_prompt`

The detailed occurrence inventory below is based on those searches plus targeted inspection of the implementation and tests that define or assert the compatibility surfaces.

## Active architectural vocabulary

The current runtime implementation defines `DecisionProducer.decide(decision_input: DecisionInputPacket) -> Decision`, `StaticDecisionProducer`, `DecisionInputPacket`, and `DecisionInputComposer`. `Runtime.__init__` accepts `decision_input_composer: DecisionInputComposer` and `model: DecisionProducer`; `Runtime.handle_user_message` composes a decision input packet and passes retry packets to `self.model.decide(...)`. The remaining `model` attribute and `model.decision.*` events are compatibility vocabulary rather than the preferred type vocabulary.

## Occurrence classification

### Compatibility aliases

| Occurrence | Files / lines | Classification | Support |
|---|---:|---|---|
| `DecisionModel = DecisionProducer` | `seed_runtime/runtime.py:391` | compatibility alias | Kept as former public decision producer name. |
| `FakeDecisionModel = StaticDecisionProducer` | `seed_runtime/runtime.py:392` | compatibility alias | Kept as former public static producer name. |
| `ContextPacket = DecisionInputPacket` | `seed_runtime/context.py:140` | compatibility alias | Kept as former public decision-input packet name. |
| `ContextComposer = DecisionInputComposer` | `seed_runtime/context.py:141` | compatibility alias | Kept as former public decision-input composer name. |

### Test compatibility

| Occurrence | Files / lines | Classification | Support |
|---|---:|---|---|
| `ContextComposer`, `ContextPacket` alias imports/assertions | `tests/test_runtime_loop.py:398-409` | test compatibility | Test proves legacy input imports remain aliases to preferred names. |
| `DecisionModel`, `FakeDecisionModel` alias imports/assertions and construction | `tests/test_runtime_loop.py:412-437` | test compatibility | Test proves legacy producer imports remain aliases and `last_context` compatibility still mirrors `last_decision_input`. |
| `model.decision.*` assertions | `tests/test_api.py:74`; `tests/test_runtime_loop.py:96-381`; `tests/test_seed_local_script.py:288,331,475`; `tests/test_state_patches.py:175,202`; `tests/test_tool_intent.py:50-90`; `tests/test_tool_recommendations.py:399`; `tests/test_tool_validation.py:126-218` | test compatibility | Tests preserve existing event vocabulary and should remain until event compatibility is intentionally changed. |
| `retry_prompt` assertions | `tests/test_model_client.py:165-178`; `tests/test_runtime_loop.py:243-356` | test compatibility | Tests preserve current retry metadata field and rendered correction section. |

### Active implementation

| Occurrence | Files / lines | Classification | Support |
|---|---:|---|---|
| `last_context` on `StaticDecisionProducer` | `seed_runtime/runtime.py:31,35` | active implementation | Runtime test helper stores both preferred `last_decision_input` and legacy `last_context`; this is active code, but the legacy member exists only for compatibility. |
| `context` local variables / annotations in runtime retry helpers | `seed_runtime/runtime.py:84,200,220,240` | active implementation | Local variable names still use generic `context` while the types are `DecisionInputPacket`; this is naming debt only, not a runtime behavior difference. |
| `runtime.py` constructor parameter `model: DecisionProducer` and `self.model.decide(...)` | `seed_runtime/runtime.py:68,83` | active implementation | Preferred type is `DecisionProducer`, but the member name remains model-centric. |

### Serialized/runtime schema

| Occurrence | Files / lines | Classification | Support |
|---|---:|---|---|
| `context_budget`, `current_input`, `open_tool_needs`, and similar `context:` search hits in serializers/journals | `seed_runtime/decision_journal.py:99,106`; `seed_runtime/history_brief.py:20`; `seed_runtime/snapshot_policy_audit.py:72` | serialized/runtime schema | These are runtime data shapes outside the compatibility rename target and should not be migrated in this slice. |

### Event vocabulary

| Occurrence | Files / lines | Classification | Support |
|---|---:|---|---|
| `model.decision.proposed` | `seed_runtime/runtime.py:56,116` | event vocabulary | Runtime emits the existing event name for proposed decisions. |
| `model.decision.parse_failed` | `seed_runtime/runtime.py:92` | event vocabulary | Runtime emits the existing event name for parse failures. |
| `model.decision.intent_rejected` | `seed_runtime/runtime.py:136` | event vocabulary | Runtime emits the existing event name for tool-intent rejection. |
| `model.decision.invalid` | `seed_runtime/runtime.py:156` | event vocabulary | Runtime emits the existing event name for validation failure. |
| `model.decision.*` in tests and current docs | files listed in the search output above | event vocabulary / test compatibility / current documentation | These document and test the emitted ledger vocabulary; they do not prove preferred architecture vocabulary. |

### Current documentation

Current documentation that describes live implementation still contains legacy terms and should be treated as current documentation, not implementation: `docs/runtime_parity_inventory.md`, `docs/input_inspection_reconciliation.md`, `docs/natural_language_execution_path_inventory_audit.md`, `docs/ask_question_refuse_inventory.md`, `docs/capability_ownership_matrix.md`, `docs/runtime_reassessment.md`, `docs/state_patch_inventory.md`, `docs/runtime_runtime_loop_responsibility_audit.md`, and generated architecture JSON. These documents frequently cite the legacy names while describing current runtime flows, aliases, or event streams.

### Historical documentation

Historical or planning documents preserve repository evidence and should not be rewritten for this slice: `03-runtime-loop.md`, `08-small-model-strategy.md`, `09-pseudocode.md`, `10-build-plan.md`, `11-naming.md`, `docs/decision_model_context_naming_audit.md`, `docs/runtime_decision_reconciliation.md`, and the older characterization/reconciliation/audit documents under `docs/` and `docs/audit/`. Their legacy vocabulary is historical evidence of the prior architecture and migration rationale.

### Intentional legacy compatibility


## Answers to required questions

### 1. Classification summary for every remaining occurrence

Every occurrence from the required searches falls into one of the categories above:

- active implementation: local `context`/`model` vocabulary in runtime, model-client, intent-classifier, and retry helpers; `last_context`; `retry_prompt` construction/rendering.
- test compatibility: alias, event-name, and retry-schema assertions under `tests/`.
- current documentation: current inventories/reconciliations that describe live runtime behavior.
- historical documentation: pseudocode, build-plan, naming-plan, and historical audit documents.
- serialized/runtime schema: packet fields and journal/snapshot context-shaped data.
- event vocabulary: `model.decision.*` strings emitted by `Runtime` and asserted by tests.

### 2. Occurrences that should migrate immediately

Safe immediate migrations are limited to internal variable/member names that do not alter public imports, event names, packet fields, or serialized shapes:

1. `Runtime.__init__(..., model: DecisionProducer)` / `self.model` can migrate to `decision_producer` / `self.decision_producer`, optionally keeping `self.model` as a temporary alias if external tests or integrations access it.
2. Local variables named `context` / `retry_context` in `Runtime.handle_user_message` and retry helper parameters can migrate to `decision_input` / `retry_decision_input` because the type is already `DecisionInputPacket`.
4. Current documentation that is not historical and not compatibility documentation can be updated opportunistically to say `DecisionProducer` / `DecisionInputPacket` first and legacy aliases second.

No cleanup is performed in this report.

### 3. Occurrences that should remain until a later compatibility window

The following should remain until an explicit compatibility window because implementation or tests prove consumers depend on them:

- `DecisionModel`, `FakeDecisionModel`, `ContextComposer`, and `ContextPacket` aliases.
- `StaticDecisionProducer.last_context`.
- `retry_prompt`, because it is a serialized `DecisionInputPacket` field and rendered by the model-client prompt path.
- `model.decision.*` event names, because runtime emits them and many tests assert them.

### 4. Occurrences that should never be migrated

Historical evidence should remain in historical documents and plans: `03-runtime-loop.md`, `08-small-model-strategy.md`, `09-pseudocode.md`, `10-build-plan.md`, `11-naming.md`, `docs/decision_model_context_naming_audit.md`, `docs/runtime_decision_reconciliation.md`, and older characterization/audit records. Rewriting those would erase the repository's evidence of how the rename was evaluated and why compatibility was retained.

### 5. Does active implementation still imply LLM ownership, prompt context, or model-centric architecture?

- LLM ownership: rejected. The active protocol is `DecisionProducer`, and `StaticDecisionProducer` plus intent adapters prove the producer can be deterministic or adapter-backed rather than an LLM owner.
- Model-centric architecture: partially supported. The preferred types shifted, but `Runtime` still stores the producer as `self.model`, emits `model.decision.*` events, and reports parse/validation messages as model decision failures.

### 6. Are current event names misleading?

The `model.decision.*` names are mildly misleading as architectural vocabulary because the implementation now accepts a `DecisionProducer`, not necessarily a model. They are best classified as implementation compatibility/event vocabulary, not preferred active architectural vocabulary. This report does not recommend renaming them in this slice.

### 7. Evaluation of `retry_prompt`

`retry_prompt` is both an active implementation concern and a compatibility concern. It is active because runtime retry helpers set it and the prompt renderer consumes it. It is compatibility because it is a serialized packet field and tested shape. It is a future cleanup candidate, but acceptable to keep now.

### 8. Migration inventory

#### Safe immediate migrations

- Internal runtime member/parameter/local names: `model` -> `decision_producer`, `context` -> `decision_input`, `retry_context` -> `retry_decision_input` where no public shape changes.
- Model-client parameter names from `context` to `decision_input`.
- Current, non-historical docs that describe live architecture can prefer new names while noting aliases.

#### Safe deferred migrations

- `last_context` -> `last_decision_input` only after alias tests and external compatibility window are updated.
- `retry_prompt` -> a neutral field such as retry feedback/instructions only with packet-field compatibility handling.
- Provider class aliases containing `DecisionModel` after import compatibility window.

#### Permanent compatibility

- Historical import aliases may remain indefinitely if the public API is intentionally stable.
- `model.decision.*` event names can remain as stable event vocabulary even though they are no longer preferred architecture vocabulary.

#### Historical preservation

- Historical plans, pseudocode, audits, generated architecture snapshots, and reconciliation documents should preserve the names they originally evaluated or observed.

## Findings

Legacy vocabulary still participates in active implementation through local/member names (`self.model`, `context` parameters), event names (`model.decision.*`), test-helper compatibility (`last_context`), and the serialized retry field (`retry_prompt`). The compatibility rename has shifted the core runtime's type vocabulary to `DecisionProducer` and `DecisionInputPacket`, but meaningful naming debt remains in the runtime boundary, prompt adapter, event vocabulary, and retry metadata.

## Recommended bounded implementation slice

A safe next slice would rename only internal runtime/model-client parameter and member names, add compatibility assignments only where needed, and update tests that inspect those internal names. It should explicitly exclude alias removal, event renames, serialized packet field renames, behavior changes, validation changes, policy changes, and inquiry behavior changes.

## Files inspected

- `seed_runtime/runtime.py`
- `seed_runtime/context.py`
- `tests/test_runtime_loop.py`
- `tests/test_model_client.py`
- Documentation files returned by the required repository-wide searches.

## Files changed

- `docs/legacy_decision_vocabulary_reconciliation.md`

## LOC changed

One documentation file was added. Runtime behavior, execution, validation, policy, inquiry behavior, aliases, events, and serialized schemas were not changed.
