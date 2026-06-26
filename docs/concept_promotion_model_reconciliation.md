# Concept Promotion Model Reconciliation

This reconciliation is observational. It asks whether current implementation history and current implementation demonstrate a repeatable progression by which new architectural concepts mature into repository artifacts. It does not recommend architecture governance, process, policy, or future methodology.

Repository authority wins. The strongest current answer is: **yes, a repeatable maturation pattern is visible, but it is not a formal promotion framework.** The repeated implementation-backed pattern is:

```text
language / reconciliation pressure
↓
bounded implementation evidence or existing implementation reuse
↓
read-only projection / inventory / audit surface
↓
tests and shape/inventory coverage
↓
possible artifact status
↓
runtime behavior only when an independent runtime owner already exists
```

The repository does **not** show that every concept must pass through a single uniform stage machine. It does show that implementation-backed concepts are usually exposed first through read-only diagnostic, inventory, or projection surfaces before they are treated as operational/runtime behavior.

## Commands executed

```bash
pwd && find .. -name AGENTS.md -print && git status --short
cat AGENTS.md && rg -n "Expectation Set|Question Famil|Documentation Structure|Answer Responsibility|Actionability|Runtime Responsibility|Seed Runtime Observations|promotion|projection|diagnostic-inventory|diagnostic-shape-audit" -S .
rg -n "class .*Expectation|ExpectationSet|expectation set|question surface|QuestionFamily|Question Family|Answer Responsibility|answer responsibility|runtime responsibility|Seed Runtime Observations|runtime observations|Documentation Structure|Actionability" seed_runtime scripts tests docs -S
python scripts/seed_local.py --help | sed -n '1,160p'; python scripts/seed_local.py --diagnostic-inventory --json | head -c 2000; echo
python scripts/seed_local.py --question-surface-inventory --json | python -m json.tool | sed -n '1,220p'
python scripts/seed_local.py --projection-shape --json | python -m json.tool | sed -n '1,120p'
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-family inquiry --knowledge-reachability-audit-json | python -m json.tool | sed -n '1,160p'
sed -n '1,220p' seed_runtime/question_surface_inventory.py
sed -n '1,220p' seed_runtime/diagnostic_inventory.py
sed -n '1,140p' seed_runtime/evaluations.py
rg -n "SeedRuntime|seed_runtime|runtime observation|process_thread|ObservationProvider|Runtime" seed_runtime tests/test_runtime_self_observation.py docs/runtime_self_observation_investigation.md docs/self_observation_ordinary_domain_reconciliation.md -S
sed -n '3140,3275p' seed_runtime/observation_sources.py
sed -n '1,120p' tests/test_runtime_self_observation.py
sed -n '1,130p' seed_runtime/projection_shape.py
sed -n '70,140p' seed_runtime/diagnostic_shape_audit.py
sed -n '590,625p' seed_runtime/diagnostic_shape_audit.py
rg -n "class SeedRuntimeObservationSource|class Runtime|owner|responsib|ToolNeed|ActionPlan|Execution|DecisionProducer|StateProjector" seed_runtime/observation_sources.py seed_runtime/runtime.py seed_runtime/models.py tests/test_runtime_responsibility* docs/runtime_responsibility* docs/*runtime*responsib* -S
sed -n '190,285p' seed_runtime/observation_sources.py
sed -n '37,120p' seed_runtime/runtime.py
sed -n '1,90p' seed_runtime/documentation_structure.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_runtime_self_observation.py tests/test_documentation_structure.py tests/test_question_surface_inventory.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/documentation_structure.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/evaluations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/runtime.py`
- `seed_runtime/models.py`
- `tests/test_runtime_self_observation.py`
- `tests/test_documentation_structure.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- Prior reconciliation docs located by ripgrep, especially expectation sets, question families, answer responsibility, current inquiry actionability, runtime responsibility, runtime self-observation, and ordinary self-observation reconciliations.

## Files changed

- `docs/concept_promotion_model_reconciliation.md`

## LOC changed

- Added 1 documentation file.
- Net change: report-only Markdown addition; no runtime code, schemas, projections, diagnostic registry entries, or tests changed.

## Concept maturity table

| Concept | Current maturity | Promotion evidence | Projection evidence | Artifact evidence | Runtime evidence | Strongest supporting evidence | Strongest contradictory evidence |
|---|---|---|---|---|---|---|---|
| Expectation Sets | Bounded implementation artifact in specific surfaces; not a generic runtime artifact. | Existing authority evaluators and eval harness encode expected observations/outcomes; prior reconciliation found no generic `ExpectationSet` registry. | Exposed indirectly through authority-slice JSON fields and question-family inventory rows. | `EvalExpectation` exists as a test/evaluation dataclass; bounded authority surfaces expose required observations and desired observations, but no repository-wide `ExpectationSet` artifact exists. | None as a runtime owner. Runtime consumes decisions, not expectation-set objects. | Implementation loss would occur if evaluator expected observations/outcomes were removed. | No generic `ExpectationSet` class, CLI, registry, lifecycle, or runtime consumer. |
| Question Families | Implementation artifact and read-only inventory artifact; presentation dispatch exists for exact `ask --question-family`. | Language became static inventory rows with family, surface, flag, examples, answer responsibility, boundary, and notes; later bounded ask dispatch uses exact lookup. | `--question-surface-inventory` renders JSON/human read-only rows. | `QuestionSurfaceInventoryRow` dataclass and deterministic `build_question_surface_inventory()`. | Presentation-layer dispatch only; rows explicitly say inventory does not infer or route natural-language operator intent. | Every row maps a question family to a surface flag and answer responsibility. | Not an operational router/evaluator; no natural-language classification authority and no fuzzy intent promotion. |
| Documentation Structure | Read-only implementation/projection artifact; not semantic knowledge or runtime artifact. | Documentation structure moved from prose concern to structural observer, recurrence/drilldown/membership surfaces, diagnostic inventory, shape audit, and tests. | `--documentation-structure` JSON/human output projects document metrics, recurrence, skeletons, and exact structural membership. | `DocumentationStructure*` dataclasses and observer/formatter/JSON functions. | None. It reads repo files and does not append events or mutate repo/runtime. | Boundary constants explicitly reject prose interpretation, claim extraction, shape inference, ontology promotion, event-ledger writes, and mutation. | The surface intentionally refuses semantic promotion; structure is not claim authority. |
| Answer Responsibility | Static implementation metadata attached to Question Family rows; not independent artifact. | Language became a row field in question-surface inventory and prior reconciliations audited whether it deserves independence. | Rendered by question-surface inventory. | Field in `QuestionSurfaceInventoryRow`; no separate id/class/registry. | None. Existing surfaces own execution/evaluation; answer-responsibility strings do not route. | Removing the row field would change inventory JSON/human output. | No independent lifecycle, tests, evaluator, runtime consumer, duplicate audit, or owner relation. |
| Actionability | Read-only projection/reconciliation concept over inquiry outputs; not implementation artifact as an independent object. | Prior actionability reconciliation found current fields such as blocked/remaining observations and limiting reasons can support a disposition projection. | Supported as possible non-persisted projection from existing inquiry slice payloads, not as a committed surface in reviewed implementation. | No independent `Actionability` artifact identified. | None. It is explicitly not scheduling, retry, notification, execution, authority acquisition, or event-ledger writing. | Existing inquiry fields can describe blocked/remaining observation and reason classes. | Strongest reason against promotion: duplicate responsibility/no independent implementation; actionable state is a projection of inquiry outputs. |
| Runtime Responsibility | Implementation-backed owner distinctions; no complete runtime-activity artifact. | Runtime responsibility moved from prose to owner metadata, service boundaries, event kinds, transient statuses, and reconciliation. | Diagnostic inventory and runtime traces can expose pieces; no single current-work projection exists. | `Runtime.__seed_arch__`, service classes, events, `ExecutionStatus` types. | Runtime exists, but as request/response orchestration and routing to owners, not as a continuous activity taxonomy. | Runtime routes validated decisions to owner services without owning their behavior. | No durable current activity owner/phase/run artifact; `idle`, `background-active`, and generic activity states are not implementation-backed. |
| Seed Runtime Observations | Runtime observation source and ordinary observation/fact/projection artifact. | Investigation identified a missing subject boundary; implementation added a read-only source that emits ordinary observations; tests prove ingestion and projection. | Observations become ordinary projected facts through existing event ledger and StateProjector. | `SeedRuntimeObservationSource` with process/thread/duration/storage predicates; observation inventory support; tests. | Not runtime governance or scheduler; it observes the current process and uses existing ingestion when callers collect it. | Tests prove deterministic read-only observations and ordinary event sequence to projection. | It does skip some intermediate read-only projection-only status: unlike many diagnostics, this became an observation provider whose data can be promoted to ordinary facts, but metadata keeps it local/read-only/non-governing. |

## Observed progressions for implementation artifacts

### Expectation Sets

Observed progression:

```text
surface-specific language about expected observations/outcomes
↓
bounded evaluator/test implementation
↓
rendered inquiry/audit fields
↓
observable artifact in those bounded surfaces only
```

The progression stops before a generic artifact. The strongest reason is missing generic implementation: no repository-wide expectation registry, no generic comparison API, and no runtime consumer.

### Question Families

Observed progression:

```text
operator question grouping language
↓
static question-surface inventory rows
↓
read-only inventory projection
↓
exact bounded ask presentation dispatch to existing surfaces
```

This is artifact promotion for static classification and surface accountability, not for natural-language intent routing.

### Documentation Structure

Observed progression:

```text
documentation organization concern
↓
mechanical structure observer
↓
read-only documentation-structure projection and recurrence/drilldown/membership views
↓
diagnostic inventory + shape-audit registration + tests
```

It becomes an operational visibility artifact while explicitly refusing semantic promotion.

### Answer Responsibility

Observed progression:

```text
language in investigations
↓
static metadata field on Question Family rows
↓
rendered inventory projection
```

It has not progressed into an independent artifact. The strongest reason is that responsibility is owned by existing surfaces and inventory rows; no separate implementation consumes it.

### Actionability

Observed progression:

```text
language in inquiry reconciliations
↓
existing inquiry output fields recognized as supporting a possible read-only disposition
```

It has not become an artifact. The strongest reason is that current actionable state is a projection of inquiry outputs and would duplicate bounded inquiry responsibility if made independent without new evidence.

### Runtime Responsibility

Observed progression:

```text
runtime responsibility language
↓
service boundaries, owner metadata, event kinds, and transient execution statuses
↓
read-only audit/reconciliation visibility over owners
```

It has not become a complete runtime-activity artifact. The strongest reason is absence of a durable/queryable current activity object with owner, phase, lifecycle, run id, and causation.

### Seed Runtime Observations

Observed progression:

```text
runtime self-observation investigation
↓
read-only observation source implementation
↓
ordinary observation ingestion
↓
event ledger facts/evidence
↓
projected state facts
```

This is the strongest example of a concept becoming an ordinary implementation artifact. It is also the strongest partial contradiction to a strict projection-before-artifact rule, because the implementation is an observation source, not only a projection. However, it remains read-only, local-only, and non-governing.

## Does the repository consistently prefer projection before runtime behavior?

Yes, for the investigated concepts that could have become operational behavior. The evidence is bounded rather than universal:

- Question Families became a static inventory and exact presentation dispatch, not an autonomous router.
- Documentation Structure became a read-only diagnostic/projection surface, not semantic documentation authority.
- Answer Responsibility became inventory metadata, not an executing layer.
- Actionability remains a possible read-only projection over inquiry outputs, not scheduling or retry behavior.
- Runtime Responsibility is visible through owner boundaries and reconciliation, but not as a continuous runtime state machine.
- Seed Runtime Observations became an observation source, but the source metadata and tests constrain it to read-only/local/non-governing behavior and ordinary ingestion/projection rather than runtime control.

Therefore, the current evidence supports: **read-only visibility usually precedes runtime behavior, and runtime behavior is withheld unless an independent runtime owner and tests already exist.**

## Does any investigated concept skip directly from idea to runtime artifact?

No strong direct skip is demonstrated. The closest case is **Seed Runtime Observations**, but it does not become runtime governance or scheduling. It becomes an observation provider whose outputs flow through existing observation, event, fact, and projection machinery. The concept therefore uses an existing runtime-adjacent pipeline rather than skipping to new runtime behavior.

## Can the progression itself be observed?

Partly yes. The following properties are already recoverable from repository evidence:

| Observable property | Recoverable? | Evidence source |
|---|---:|---|
| Promotion stage | Partly | Reconciliation docs, inventory rows, diagnostic inventory, current code/tests. |
| Implementation support | Yes | Dataclasses, build functions, observer/provider classes, runtime owner metadata, tests. |
| Projection support | Yes | CLI JSON/human projections such as diagnostic inventory, question-surface inventory, projection shape, documentation structure, and projected state facts. |
| Runtime support | Yes/No per concept | Runtime classes and event paths show support; absence is also observable when no owner/artifact exists. |
| Tests | Yes | Concept-specific tests plus diagnostic inventory and shape-audit tests. |
| Read-only boundary | Yes | Diagnostic inventory fields, shape audit specs, boundary constants, metadata such as `read_only`/`mutates_cluster=false`, and tests. |

The progression is observable as repository evidence, but not as a single first-class promotion-stage model.

## Strongest contradictory evidence

1. **Seed Runtime Observations** became an observation source and ordinary projected facts, not merely a read-only report. This differs from diagnostics that remain inventory/audit surfaces. The contradiction is limited because the source is explicitly read-only, local-only, non-scheduler, and non-governance.
2. **Legacy/experimental runtime side paths** in models and runtime code show artifacts such as action plans, handoff plans, execution proposals, and authorizations that exist in implementation even though current reconciliations treat them as non-core side paths. This weakens any simple claim that projection always precedes artifact existence.
3. **Evaluation expectation data** exists as test harness implementation (`EvalExpectation`) without becoming an operational projection surface. This shows implementation artifacts can exist inside test/evaluation infrastructure without promotion to runtime or diagnostic inventory.

## Acceptance criteria answers

### Has the repository already demonstrated a repeatable progression by which architectural concepts mature?

Yes, observationally. The repeated progression is not a formal policy, but repository evidence repeatedly favors implementation evidence, read-only visibility, shape/inventory/test coverage, and explicit non-mutation boundaries before treating a concept as architectural or operational.

### Is read-only projection consistently the stage immediately before artifact promotion?

Not strictly. Read-only projection is consistently favored before **runtime behavior**, but not always immediately before **artifact promotion**. Some artifacts first appear as implementation details or test/evaluation dataclasses before read-only exposure. For investigated operational concepts, however, promotion to operator-visible architectural status is usually mediated by read-only projection/inventory/audit surfaces.

### What implementation-backed evidence currently determines whether a concept earns promotion?

The recurring evidence is:

- a bounded implementation owner or existing implementation path;
- deterministic fields/schema rather than prose-only vocabulary;
- read-only projection/inventory/audit visibility;
- tests proving the surface appears and has expected boundaries;
- explicit authority/mutation boundaries;
- no duplicate responsibility with an existing owner;
- ordinary event/projection integration only when the concept is an observation/fact rather than diagnostic-only interpretation;
- absence of runtime promotion when observations, independent implementation, or durable lifecycle are missing.

## Recommended bounded implementation slice

None for this observational task. If a future implementation task is opened, the smallest implementation-backed slice would be to make promotion-stage visibility inspectable as a read-only diagnostic over existing evidence only. This report does not recommend adding that behavior now.
