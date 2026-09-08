# Question → Bounded Work Invocation Investigation

## Scope

This is a bounded implementation investigation only. It does not implement ownership recovery, planners, workflow engines, task graphs, routing frameworks, generic dispatchers, behavior changes, CLI changes, schema changes, ledger changes, or projection changes.

The investigation asks how the current repository answers:

```text
A question has arrived.
Which bounded work is permitted to execute?
```

Repository authority is the implementation, tests, and existing diagnostic/report artifacts reviewed below.

## Implementation evidence reviewed

### Primary implementation surfaces

- `seed_runtime/question_surface_inventory.py`
  - `BOUNDED_ASK_DISPATCH_SURFACES`
  - `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`
  - `BOUNDED_ASK_DIAGNOSTIC_ONLY_FAMILIES`
  - `BOUNDED_ASK_ARG_VALUES`
  - `bounded_status_for_question_family(...)`
  - `bounded_ask_inventory_findings(...)`
  - `QuestionSurfaceInventoryRow`
  - `build_question_surface_inventory(...)`
  - `build_question_family_definition(...)`
  - `build_composed_question_family_explanation(...)`
- `scripts/seed_local.py`
  - CLI arguments for `ask`, `--question-family`, `--surface-args`, and `--presentation`
  - `apply_bounded_ask_dispatch(...)`
  - direct rendering branches for question inventory, family definition, and family explanation
- `tests/test_question_surface_inventory.py`
  - bounded ask unknown-family rejection
  - bounded ask free-text rejection
  - parameter-required family validation
  - direct-surface equivalence tests for `knowledge reachability`, `derivation explanation`, and `selection explanation`
  - diagnostic-only and not-dispatchable rejection tests
  - QuestionFamily definition and composed explanation guardrail tests
- `seed_runtime/operational_story.py`
  - implementation-local answer, reasoning, supporting-evidence, boundary, and limitations payloads
  - `build_operational_story(...)`
  - `_compose_operational_story_payloads(...)`
  - `format_operational_story(...)`
- `seed_runtime/inquiry_orientation.py`
  - inquiry-note selection and orientation building
  - `_collect_architectural_orientation_evidence(...)`
  - `_compose_architectural_orientation_answer(...)`
  - `format_inquiry_orientation(...)`
- `seed_runtime/diagnostic_inventory.py`
  - diagnostic registry row for `question_surface_inventory`
- `seed_runtime/diagnostic_shape_audit.py`
  - implementation specs for diagnostic/operational surfaces, including `operational_story`

### Existing reports used as secondary evidence

- `methodology_as_inquiry_subject_investigation.md`
- `docs/inquiry_surface_classes_observation.md`
- `repository_dependency_ordering_invariant_investigation.md`
- `dependency_transformation_invariant_investigation.md`
- `answer_composition_family_completion_audit.md`

### Commands run

```bash
rg -n "bounded ask|QuestionFamily|question surface|question registration|question eligibility|Inquiry Orientation|Answer Composition|diagnostic-inventory|diagnostic-shape-audit|question" . -g '!**/.git/**'
sed -n '1,620p' seed_runtime/question_surface_inventory.py
rg -n "bounded_ask|ask|question_family|question_families|BOUNDED_ASK|question_surface_inventory" scripts/seed_local.py seed_runtime tests -g '*.py'
sed -n '920,1000p' scripts/seed_local.py
sed -n '2201,2290p' scripts/seed_local.py
sed -n '6880,6970p' scripts/seed_local.py
sed -n '430,705p' tests/test_question_surface_inventory.py
rg -n "AnswerComposition|answer composition|build_.*answer|format_.*answer|composition_source|operational_story|inquiry_orientation" seed_runtime tests -g '*.py'
sed -n '1,220p' seed_runtime/operational_story.py
sed -n '1,200p' seed_runtime/inquiry_orientation.py
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Recurring implementation patterns

### 1. Question-family registration is static and explicit

Known question families are registered as `QuestionSurfaceInventoryRow` values in `build_question_surface_inventory(...)`. Each row carries:

- `question_family`
- example questions
- answering surface
- CLI flag
- answer responsibility
- authority boundary
- notes

The rows are then enriched with bounded ask status, dispatch surface, required surface args, formatter name, implementation reason, canonical diagnostic surface, diagnostic inventory relationship, diagnostic shape-audit relationship, and relationship status.

This is implementation evidence that Question Family identity is not inferred from free text at runtime. The inventory is the current registration owner for known question families.

### 2. Bounded work eligibility is derived from separate bounded ask maps

`bounded_status_for_question_family(...)` derives eligibility from three implementation structures:

- `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` → `eligible_with_parameters`
- `BOUNDED_ASK_DISPATCH_SURFACES` → `eligible_now`
- `BOUNDED_ASK_DIAGNOSTIC_ONLY_FAMILIES` → `diagnostic_only`
- otherwise → `not_dispatchable`

This is stronger than a purely presentational inventory because the same status is consumed by `apply_bounded_ask_dispatch(...)` before any surface flag is set.

### 3. Bounded work selection is a map from exact QuestionFamily to existing surface flag behavior

`BOUNDED_ASK_DISPATCH_SURFACES` maps exact question-family names to existing implementation surfaces such as:

- `operational pressure` → `ops_brief`
- `current operational explanation` → `operational_story`
- `knowledge reachability` → `knowledge_reachability_audit`
- `derivation explanation` → `reasoning_path`
- `selection explanation` → `selection_path`
- authority and observation question families → their existing bounded surfaces

`apply_bounded_ask_dispatch(...)` does not execute a new generic work unit. It mutates parsed CLI args so the existing direct surface branch executes later. This is compatibility-style dispatch to existing surfaces, not a standalone work-execution owner.

### 4. Required-argument validation is explicit for parameterized families

`BOUNDED_ASK_REQUIRED_SURFACE_ARGS` lists required surface arguments for `derivation explanation` and `selection explanation`. `apply_bounded_ask_dispatch(...)` requires exactly that number of operator-provided values and forwards them unchanged to the direct surface flag.

Tests preserve this behavior by proving missing, too few, and too many parameter values fail, and by proving bounded ask output equals direct surface output for `reasoning_path` and `selection_path`.

### 5. Eligibility and dispatch are adjacent but not identical

The code first resolves inventory membership, then computes `eligibility`, then rejects inappropriate combinations, then sets a surface-specific CLI attribute. This supports a boundary:

```text
Question lookup / eligibility check != direct answer-surface execution
```

However, lookup, eligibility validation, required-argument validation, presentation override, and dispatch mutation all live inside `apply_bounded_ask_dispatch(...)`. The implementation separates the data structures more than it separates the runtime owner.

### 6. Question Family is distinct from Answer Surface

Inventory rows preserve both `question_family` and `surface`. Some registered families are executable through bounded ask; others are diagnostic-only or not-dispatchable. Examples:

- `surface inventory` and `surface shape validation` are registered question families but diagnostic-only.
- `source definition/import lookup` and `inquiry orientation` are registered question families but not dispatchable by bounded ask.
- `knowledge reachability` has a question family whose dispatch surface is `knowledge_reachability_audit`, with a canonical diagnostic alias back to `knowledge_reachability`.

This supports:

```text
Question Family != Answer Surface
```

### 7. Dispatch is distinct from answer composition in representative surfaces

Bounded ask dispatch only selects an existing surface. Answer composition happens inside the selected surface.

`operational_story` is the strongest representative evidence. It gathers existing audits, then `_compose_operational_story_payloads(...)` creates separate implementation-local answer, reasoning, supporting evidence, boundary, and limitations payloads before constructing `OperationalStory`; rendering is handled separately by `format_operational_story(...)`.

`inquiry_orientation` also separates evidence collection from answer composition and rendering: `_collect_architectural_orientation_evidence(...)` collects deterministic matches, `_compose_architectural_orientation_answer(...)` composes answer/reason/support/boundary/limitations, and `format_inquiry_orientation(...)` renders the view.

This supports:

```text
Dispatch != Answer Composition
Answer Composition != Rendering
```

for these representative surfaces. It does not prove every inquiry-like surface has the same internal answer composition boundary.

### 8. Diagnostic visibility checks question-bounded-work relationships

The question surface inventory is itself registered as a diagnostic surface, and tests preserve its visibility through diagnostic inventory and shape audit. `bounded_ask_inventory_findings(...)` checks inventory rows against bounded ask maps, including duplicate families and orphaned mappings.

This shows the repository treats question-family registration and bounded ask relationships as operationally visible, not merely as hidden CLI behavior.

## Recovered implementation relationships

### Current bounded ask path

The implementation-backed path is:

```text
CLI tokens: ask --question-family <exact family> [--surface-args ...] [--presentation]
  ↓
question-family inventory membership check
  ↓
bounded_status_for_question_family(family)
  ↓
required argument validation / diagnostic-only rejection / not-dispatchable rejection
  ↓
optional QuestionFamily presentation explanation
  ↓
set existing direct surface argument on argparse namespace
  ↓
existing direct surface build/json/format branch executes
  ↓
surface-local answer composition, if that surface has an explicit composition boundary
  ↓
surface-local rendering or JSON serialization
```

### Responsibility characterization

| Responsibility | Current owner | Explicit or compressed? | Evidence |
| --- | --- | --- | --- |
| question registration | `build_question_surface_inventory(...)` rows | explicit | static inventory rows with family, surface, responsibility, boundary |
| question lookup | `apply_bounded_ask_dispatch(...)` membership check against built inventory | compressed with dispatch path | unknown family rejected before dispatch |
| question-family resolution | exact `--question-family` value only | explicit but narrow | no free-text classification for bounded ask |
| required argument validation | `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` plus `apply_bounded_ask_dispatch(...)` | explicit data, compressed runtime validation | parameterized families require exact arg count |
| authority / eligibility validation | `bounded_status_for_question_family(...)`; rejection logic in `apply_bounded_ask_dispatch(...)`; row `authority_boundary` | partially explicit | eligibility statuses explicit; authority boundary declarative, not a separate enforcing module |
| bounded work selection | `BOUNDED_ASK_DISPATCH_SURFACES` | explicit data, compatibility-style execution handoff | exact family maps to existing surface flag |
| dispatch | `apply_bounded_ask_dispatch(...)` mutates CLI args | compressed | lookup, eligibility, validation, presentation, and dispatch mutation share one function |
| answer composition | selected surface implementation | explicit in `operational_story` and `inquiry_orientation`; surface-specific elsewhere | implementation-local payload classes / compose functions in representative surfaces |
| presentation / rendering | selected surface `format_*` or `*_json` branches in CLI | explicit per surface, not generic | direct branch prints JSON or formatter output |

## Counterexamples and compression

### Counterexample: bounded ask is not a generic question router

The bounded ask path rejects unknown question families and rejects free-text ask routing. It requires an exact registered family. Therefore, the repository does not contain a general natural-language question router for bounded work invocation.

### Counterexample: registered QuestionFamily does not imply executable bounded ask

`surface inventory` and `surface shape validation` are diagnostic-only. `source definition/import lookup` and `inquiry orientation` are not dispatchable by bounded ask. Thus, QuestionFamily membership alone does not authorize execution.

### Counterexample: authority boundary is mostly declarative at selection time

Inventory rows carry `authority_boundary`, and selected surfaces often encode boundary fields, but bounded ask eligibility does not evaluate dynamic authority conditions. The bounded ask owner decides only whether the existing registered surface may be invoked through the bounded ask compatibility path. Dynamic or domain-specific authority remains inside the answer surface or its underlying audit implementation.

### Counterexample: dispatch and validation remain compressed in one CLI helper

`apply_bounded_ask_dispatch(...)` owns all of the following in one function:

```text
message shape validation
question family lookup
eligibility check
required argument validation
presentation override
surface flag mutation
JSON compatibility special-case for knowledge reachability
```

This is the strongest recurring compressed boundary for the requested family. The supporting data maps are explicit, but the runtime owner is compressed.

### Compatibility-code assessment

The apparent compression is partly compatibility code. Bounded ask does not create new execution machinery; it maps an exact question family to an already existing direct CLI surface. Tests verify bounded ask outputs match direct-surface outputs. That means the compressed runtime helper is currently a compatibility presenter/selector over existing surfaces, not a new independently owned dispatcher.

However, the recurring pressure is not absent. The inventory, eligibility maps, required-args map, diagnostic-only/not-dispatchable states, relationship checks, and tests all repeatedly express the same decision:

```text
Given this exact QuestionFamily, is bounded ask permitted to invoke an existing bounded surface, and with what arguments?
```

## Answers to central questions

### 1. Does the repository currently contain a recurring Question → Bounded Work Invocation responsibility?

Yes, with a bounded scope.

The recurring implementation responsibility is not a planner, workflow engine, generic dispatcher, or free-text router. It is an exact QuestionFamily-to-existing-surface invocation responsibility for the bounded `ask --question-family` path. It answers whether a registered question family is eligible for bounded ask, whether required operator arguments are present, and which existing surface flag should be activated.

The owner is not fully separated as a named responsibility module. It is split between explicit inventory/maps in `seed_runtime/question_surface_inventory.py` and compressed runtime orchestration in `scripts/seed_local.py::apply_bounded_ask_dispatch(...)`.

### 2. Where is the strongest implementation evidence?

Strongest evidence:

1. `BOUNDED_ASK_DISPATCH_SURFACES`, because it explicitly maps question families to bounded work surfaces.
2. `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`, because it proves some questions require validated surface parameters before invocation is permitted.
3. `bounded_status_for_question_family(...)`, because it makes eligibility a derived implementation status rather than a prose-only claim.
4. `apply_bounded_ask_dispatch(...)`, because it operationalizes lookup, eligibility, rejection, parameter validation, presentation override, and surface selection.
5. `tests/test_question_surface_inventory.py`, because it proves the bounded ask path rejects unknown, diagnostic-only, not-dispatchable, and incorrectly parameterized families, and proves eligible bounded ask surfaces match direct surface outputs.
6. Diagnostic inventory and shape-audit tests, because they preserve visibility of question-surface inventory and bounded ask relationship findings.

### 3. Which responsibilities are already explicit?

Already explicit:

- Question-family registration as inventory rows.
- QuestionFamily-to-surface relationship as row fields.
- Bounded ask dispatch eligibility statuses.
- Required surface-argument names and exact argument-count validation for parameterized families.
- Diagnostic-only and not-dispatchable statuses.
- Bounded work selection as exact family-to-surface map.
- QuestionFamily definition/explanation presentation from existing fields.
- Representative answer composition boundaries in `operational_story` and `inquiry_orientation`.
- Rendering/serialization as selected surface-specific formatter/json functions.
- Diagnostic visibility for question surface inventory.

### 4. Which responsibilities remain compressed?

Compressed responsibilities:

- Question lookup, eligibility validation, required-argument validation, presentation override, dispatch mutation, and compatibility JSON special-casing are all in `apply_bounded_ask_dispatch(...)`.
- Authority validation is partly declarative. Inventory rows expose boundaries, but bounded ask does not have a separate authority validator beyond eligibility status and surface-specific behavior.
- Dispatch is implemented as CLI argparse mutation rather than an explicit bounded-work invocation object or decision result.
- Answer composition is explicit only in representative surfaces; other answer-like surfaces remain surface-specific.
- Question-family registration and bounded ask eligibility live in the same inventory module, so the boundary between family registration and invocation eligibility is explicit in data but not fully owned by separate runtime responsibilities.

### 5. Is the next ownership family supported by implementation evidence?

Yes, but only as a narrow ownership family:

```text
QuestionFamily bounded invocation eligibility / existing-surface selection
```

The earliest recurring compressed boundary is:

```text
question lookup + eligibility validation + required argument validation + existing-surface selection
```

This boundary currently lives primarily in `apply_bounded_ask_dispatch(...)`, with its data source in `seed_runtime/question_surface_inventory.py`.

The evidence does not support ownership recovery for a planner, workflow engine, task graph, generic router, generic dispatcher, semantic question classifier, or behavior-changing CLI redesign.

## Supported conclusions

- The repository already distinguishes `QuestionFamily` from answer surface in inventory rows and bounded status enrichment.
- Bounded ask currently requires exact `QuestionFamily` identity; it does not infer families from free text.
- Eligibility is not the same as dispatch: diagnostic-only and not-dispatchable families are registered but rejected by bounded ask.
- Dispatch is not answer composition: bounded ask selects an existing surface; surface-local implementations compose the answer.
- Answer composition is not rendering in representative recovered surfaces (`operational_story`, `inquiry_orientation`).
- The current owner of the invocation decision is compressed across `question_surface_inventory.py` data and `apply_bounded_ask_dispatch(...)` control flow.
- The strongest justified next slice, if ownership recovery is later requested, would be narrow and implementation-preserving: extract or clarify the bounded ask eligibility/selection boundary without changing CLI behavior or surface outputs.

## Unsupported conclusions

- Unsupported: the repository has a generic question router.
- Unsupported: bounded ask should classify arbitrary natural-language questions.
- Unsupported: every QuestionFamily is executable.
- Unsupported: eligibility performs dynamic authority enforcement for every family.
- Unsupported: answer composition is uniformly implemented across all answer-like surfaces.
- Unsupported: a planner, workflow engine, task graph, routing framework, or generic dispatcher is justified by this evidence.
- Unsupported: architectural vocabulary alone should be promoted into knowledge without existing implementation evidence.

## Confidence

High confidence that a recurring exact QuestionFamily-to-existing-surface bounded invocation responsibility exists, because it is represented in executable maps, a status function, CLI dispatch behavior, and tests.

High confidence that the responsibility is currently compressed rather than fully separated, because the runtime decision path is concentrated in one CLI helper.

Medium confidence on the recommended first ownership slice, because the recurring boundary is clear but the current compression is partly intentional compatibility code over existing direct surfaces.

Low confidence for any broader routing or workflow claim, because the implementation explicitly rejects unknown and free-text bounded ask routing.

## Recommended first ownership slice, if later justified

If ownership recovery is explicitly requested later, the first slice should be the smallest implementation-backed boundary:

```text
QuestionFamily bounded invocation eligibility and existing-surface selection
```

The slice should preserve current behavior and should not introduce semantic routing. It would be justified only to make the existing compressed decision object or function explicit:

```text
exact question family
+ bounded status
+ required surface args
+ selected existing surface
+ rejection reason
```

It should not change CLI shape, schemas, ledgers, projections, answer surfaces, or diagnostic outputs unless a future task explicitly requests those changes and updates diagnostic inventory and shape-audit tests under the repository visibility contract.
