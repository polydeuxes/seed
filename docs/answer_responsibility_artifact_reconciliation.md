# Answer Responsibility artifact reconciliation

## Scope and method

This reconciliation is observational. It reviews only the implementation directly involved in `question_surface_inventory`, the authority evaluators, existing inquiry surfaces, diagnostic inventory, diagnostic shape audit, and runtime decision responsibility boundaries. Repository authority wins over prior vocabulary.

Commands executed:

```text
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short
cat AGENTS.md && rg -n "question_surface_inventory|Answer Responsibility|answer responsibility|authority evaluator|diagnostic inventory|diagnostic-shape|shape audit|inquiry|responsibil" -S .
sed -n '1,240p' seed_runtime/question_surface_inventory.py
sed -n '1,220p' tests/test_question_surface_inventory.py
rg -n "QuestionSurface|answer_responsibility|desired_observation|authority_boundary|bounded_scope|execution_target|question_family" seed_runtime tests docs -S
sed -n '240,280p' seed_runtime/question_surface_inventory.py
sed -n '1,220p' seed_runtime/container_ownership_authority.py
sed -n '1,180p' seed_runtime/service_ownership_authority.py
sed -n '1,150p' seed_runtime/listener_endpoint_authority.py
rg -n "question_surface_inventory|container_ownership_authority|service_ownership_authority|listener_endpoint_authority|inquiry_artifacts|inquiry_orientation" seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py seed_runtime/inquiry_artifacts.py seed_runtime/inquiry_orientation.py seed_runtime/runtime.py seed_runtime/runtime_loop.py
sed -n '110,165p' seed_runtime/diagnostic_inventory.py
sed -n '670,708p' seed_runtime/diagnostic_inventory.py
sed -n '148,182p' seed_runtime/diagnostic_shape_audit.py
sed -n '600,622p' seed_runtime/diagnostic_shape_audit.py
sed -n '1,170p' seed_runtime/inquiry_artifacts.py
sed -n '1,180p' seed_runtime/inquiry_orientation.py
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --container-ownership-authority --json
python scripts/seed_local.py --service-ownership-authority --json
python scripts/seed_local.py --listener-endpoint-authority --json
python scripts/seed_local.py --inquiry-artifacts --json
python scripts/seed_local.py --diagnostic-inventory --json
pytest -q tests/test_question_surface_inventory.py tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_listener_endpoint_authority.py tests/test_inquiry_artifacts.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Files inspected:

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `seed_runtime/container_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `tests/test_listener_endpoint_authority.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/inquiry_artifacts.py`
- `tests/test_inquiry_artifacts.py`
- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `scripts/seed_local.py`
- Supporting documentation only where search showed direct prior reconciliations involving answer responsibility or question-family artifacts.

Files changed: this report only, `docs/answer_responsibility_artifact_reconciliation.md`.

LOC changed: one new documentation file.

## Short answer

Answer Responsibility is implementation-backed, but only as static row metadata inside the question-surface inventory. It is not currently an independent repository artifact with its own identifier, registry, evaluator, CLI surface, lifecycle, or runtime ownership. Its actual responsibility is to name, per Question Family row, what an existing answering surface is expected to answer.

The repository has earned this narrower chain:

```text
Question Family
↓
answer_responsibility field on the QuestionSurfaceInventoryRow
↓
existing Seed surface / authority evaluator / inquiry surface
```

It has not yet earned Answer Responsibility as a separate architectural layer between Question Family and Bounded Inquiry.

Confidence: high for the static-metadata conclusion; medium-high for rejecting independent-layer status, because absence evidence is drawn from the directly reviewed implementation set rather than from every repository file.

## 1. Implementation-backed properties currently belonging to Answer Responsibility

| Property | Current support | Conclusion | Confidence |
| --- | --- | --- | --- |
| identifier | No independent identifier. The only implementation field is `answer_responsibility: str` inside `QuestionSurfaceInventoryRow`; no separate responsibility id, name field, registry key, or dataclass exists. | Not independently supported. Responsibility text is identifiable only by its string value in a question-family row. | High |
| owner | The row owns the field: each `QuestionSurfaceInventoryRow` contains `question_family`, `surface`, `surface_flag`, `answer_responsibility`, `authority_boundary`, and `notes`. | Answer Responsibility is owned by Question Surface Inventory rows, and practically by the Question Family mapping. | High |
| desired observation | Authority evaluators own `DESIRED_OBSERVATION` constants and `desired_observation` result fields, but the question-surface responsibility strings are separate prose. | Desired observation is implementation-backed in bounded authority evaluators, not in Answer Responsibility itself. | High |
| authority boundary | The question-surface row has an adjacent `authority_boundary` field, and authority evaluators have boundary dictionaries. | Boundary is associated with the row/surface/evaluator, not part of a separate responsibility artifact. | High |
| bounded scope | Some responsibility strings are bounded by their mapped surface and notes; authority evaluators expose concrete required observations and boundary fields. | Boundedness is implementation-backed at the surface/evaluator level; Answer Responsibility inherits this context but does not independently encode scope. | Medium-high |
| execution target | Question-surface rows map to one `surface` and one `surface_flag`; the responsibility string does not execute and is not selected by a runtime. | Execution target belongs to the inventory row's surface mapping, not to Answer Responsibility as a separate object. | High |
| notes | Notes are a sibling row field. The formatter renders responsibility and boundary, but not notes. | Notes constrain the row; they are not Answer Responsibility properties. | High |

## 2. Current type of Answer Responsibility

| Classification | Supported? | Evidence and conclusion | Confidence |
| --- | --- | --- | --- |
| metadata | Yes. | `answer_responsibility` is a static string field in `QuestionSurfaceInventoryRow`, serialized to JSON, and rendered as `responsibility:` in the formatter. Tests assert the JSON field exists. | High |
| implementation artifact | Partly. | It is code-backed as a dataclass field and static inventory value. It is not independently artifact-backed as its own class, registry, shape audit subject, or CLI surface. | High |
| operational artifact | No, except indirectly through surfaces. | Diagnostic inventory declares `question_surface_inventory` itself read-only, non-recording, no event-ledger writes, no cluster mutation, no projected-state use. The responsibility field does not perform operations. | High |
| presentation | Yes. | The formatter presents each responsibility line in human output. This is observable presentation backed by static data. | High |
| documentation | Not primarily. | Documentation discusses answer responsibility, but the authoritative current implementation evidence is the dataclass field and inventory rows. Removing docs would not remove the field; removing the field would change CLI/JSON behavior. | Medium-high |

## 3. Relationship: Question Family ↓ Answer Responsibility

Current implementation demonstrates one Question Family row owns one Answer Responsibility string.

Evidence:

- `QuestionSurfaceInventoryRow` declares both `question_family` and `answer_responsibility` as fields in the same frozen dataclass.
- `build_question_surface_inventory()` constructs 17 rows. In the observed CLI JSON output, there were 17 unique `question_family` values and 17 unique `answer_responsibility` strings, with no duplicate responsibility strings.
- Tests require the JSON output to include `question_family` and `answer_responsibility`, and they assert the inventory is not a router or recommender.

What current implementation does not demonstrate:

- It does not demonstrate a shareable responsibility object across multiple Question Families.
- It does not demonstrate responsibility reuse, responsibility membership, or responsibility ownership outside a row.
- It does not prove that multiple Question Families cannot share one responsibility in the future; it only shows no current shared responsibility strings in the static rows.

Conclusion: one current inventory row maps one Question Family to one Answer Responsibility string. The implementation does not yet demonstrate an independent many-to-one or shared responsibility artifact.

Confidence: high.

## 4. Relationship: Answer Responsibility ↓ Bounded Inquiry

The current implementation cannot distinguish responsibility ownership of inquiry from inquiry ownership of responsibility.

Evidence supporting bounded inquiry surfaces:

- The authority evaluators expose bounded inquiry-like result shapes: `desired_observation`, required observations, required authority, available authority, outcome, uncertainty, and read-only/no-record/no-ledger/no-mutation boundary fields.
- `inquiry_orientation` preserves raw inquiry notes and renders deterministic related material with an explicit authority boundary, but it states the note is not a fact, goal, requirement, decision, proposal, plan, command, or runtime instruction.
- `inquiry_artifacts` classifies inquiry artifacts and explicitly refuses inquiry graph creation, pressure transformation inference, workflow, or planning behavior.

Contradictory / limiting evidence:

- `QuestionSurfaceInventoryRow` has no `bounded_inquiry` field.
- Authority evaluator classes do not carry `answer_responsibility` fields.
- Inquiry surfaces do not point back to an Answer Responsibility object.
- Diagnostic shape audit registers surfaces, not responsibilities.

Conclusion: bounded inquiry behavior exists in specific surfaces/evaluators, but Answer Responsibility does not own Bounded Inquiry, and Bounded Inquiry does not own Answer Responsibility. Their relationship is mediated by the question-surface inventory row's surface mapping.

Confidence: medium-high.

## 5. Effect of removing Answer Responsibility

| Loss type | Would occur? | Support | Confidence |
| --- | --- | --- | --- |
| implementation loss | Yes. | Removing `answer_responsibility` would alter the dataclass, JSON conversion, static row construction, formatter, and tests requiring the field. | High |
| observable capability loss | Yes, but narrow. | `seed --question-surface-inventory --json` would no longer expose the responsibility field, and human output would no longer render `responsibility:` lines. This is a visibility/capability loss for the inventory surface, not loss of authority evaluator behavior. | High |
| documentation loss | Yes if docs are also removed, but not required for implementation loss. | Existing reconciliation docs discuss answer responsibility. The implementation-backed loss is independent of those docs. | Medium |
| all three | Potentially, if the term is removed from both code and docs. | Code removal alone produces implementation and observable capability loss; complete repository removal would also remove documentation vocabulary. | Medium |

## 6. Can Answer Responsibilities themselves be observed?

| Observable characteristic | Already implementation-backed? | Conclusion | Confidence |
| --- | --- | --- | --- |
| membership | Partly. | Membership of responsibility strings in question-surface rows is observable via `--question-surface-inventory --json`. There is no separate responsibility membership registry. | High |
| coverage | Partly. | Coverage can be inferred as rows with responsibility strings mapped to surfaces, but no implementation computes responsibility coverage as its own metric. | Medium |
| recurrence | Weakly. | Recurrence of string values can be externally counted from JSON output. The repository does not implement recurrence analysis for responsibilities. | Medium |
| uniqueness | Weakly and externally. | The observed current rows had unique responsibility strings, but tests do not assert responsibility uniqueness. | Medium |
| shared inquiries | No. | No implementation links responsibilities to reusable inquiry objects or shared inquiry membership. | High |
| unused responsibilities | No. | Static rows always bind responsibility strings to surfaces; no independent responsibility pool exists where unused entries could be detected. | High |
| duplicate responsibilities | No built-in check. | Duplicates could be counted externally, but no test or audit currently proves duplicate detection. | High |

Conclusion: Answer Responsibilities are observable as static field values in one diagnostic surface. They are not observable as first-class objects with implemented membership, coverage, recurrence, uniqueness, sharing, unused, or duplicate audits.

Confidence: high.

## 7. What concept does Answer Responsibility currently appear to be?

| Candidate concept | Conclusion | Support | Contradictory evidence | Confidence |
| --- | --- | --- | --- | --- |
| property of Question Families | Strongest current fit. | The field exists only inside rows that also declare `question_family`; tests require both fields in the row JSON. | The responsibility text often describes the mapped surface rather than the family in isolation. | High |
| property of inquiries | Not currently. | Inquiry surfaces and authority evaluators do not include `answer_responsibility`; they use `desired_observation`, boundaries, uncertainty, and related material. | Some responsibility strings describe bounded evaluator behavior, so they semantically summarize inquiry-like surfaces. | Medium-high |
| repository artifact | Partly, but not independent. | The field is code-backed, serialized, rendered, and tested. | There is no responsibility class, registry, audit spec, identifier, CLI, or runtime consumer. | High |
| another concept | Surface responsibility label. | The field names what an existing surface answers for a question-family row. | Prior docs may use architectural language more strongly than current code supports. | Medium-high |

Strongest contradictory evidence against “merely prose”: the field is not only documentation; it is a dataclass field, present in JSON output, rendered by CLI, registered through the diagnostic inventory surface, and covered by tests.

Strongest contradictory evidence against “independent artifact”: there is no object or registry for Answer Responsibilities separate from `QuestionSurfaceInventoryRow`, and no evaluator or inquiry consumes responsibility records.

## 8. Has the repository earned `Question Family ↓ Answer Responsibility ↓ Bounded Inquiry`?

Not as an independent architectural layer.

Earned:

```text
Question Family row
↓
answer_responsibility metadata
↓
surface / CLI flag with bounded behavior where that surface implements one
```

Not earned:

```text
Question Family
↓
independent Answer Responsibility artifact
↓
Bounded Inquiry artifact
```

Reasons:

1. Answer Responsibility has no independent identity.
2. Answer Responsibility has no independent registry apart from question-surface rows.
3. Answer Responsibility has no lifecycle or audit surface of its own.
4. Bounded inquiry behavior is implemented by concrete surfaces/evaluators, not by responsibility records.
5. Diagnostic inventory and diagnostic shape audit validate diagnostic surfaces, including question-surface inventory, but do not validate responsibility objects.
6. Runtime decision responsibilities are separate coordinator responsibilities and do not consume question-family responsibility metadata.

Confidence: high.

## Strongest supporting evidence

- Static implementation: `QuestionSurfaceInventoryRow` explicitly includes `answer_responsibility`, and `build_question_surface_inventory()` populates it for every known question-family row.
- Observable CLI/JSON: `question_surface_inventory_json()` serializes the field; `format_question_surface_inventory()` renders it as `responsibility:`.
- Tests: `tests/test_question_surface_inventory.py` requires the JSON field and proves the inventory is read-only/static and not a router/recommender.
- Diagnostic visibility: `diagnostic_inventory` registers `question_surface_inventory` as a read-only JSON-capable surface with no record support, no ledger writes, no projected-state use, and no cluster mutation.
- Shape audit: `diagnostic_shape_audit` maps `question_surface_inventory` to its module, build function, formatter, JSON function, and CLI flag.
- Authority evaluator contrast: container, service, and listener endpoint authority evaluators independently implement desired observations, required observations, authority requirements, outcomes, uncertainty, and boundaries without using an `answer_responsibility` field.

## Strongest contradictory evidence

- Answer Responsibility is not merely documentation because it is executable repository data rendered by a CLI and asserted by tests.
- Answer Responsibility is not an operational executor because the diagnostic inventory marks the inventory surface as read-only/non-recording/non-mutating, and responsibility values are not consumed by runtime decision paths.
- Answer Responsibility is not an independent artifact because no reviewed implementation provides a responsibility id, class, registry, shape audit row, owner relation, bounded-inquiry relation, duplicate audit, unused audit, or runtime consumer.
- Bounded inquiries exist, but their implementation vocabulary is `desired_observation`, required observations, authority, outcome, uncertainty, and boundary; this is adjacent to but not owned by Answer Responsibility.

## Final answers

### Has Answer Responsibility already become an implementation-backed repository artifact?

Yes, but only in a bounded sense: it is an implementation-backed field on the question-surface inventory artifact. No, if “artifact” means an independent architectural artifact with its own identity and lifecycle.

Confidence: high.

### What responsibility does Answer Responsibility actually own?

It owns the static description of what the mapped answering surface is responsible for answering for that Question Family row. It does not own routing, execution, inquiry construction, desired-observation evaluation, recording, event-ledger mutation, or cluster mutation.

Confidence: high.

### Has the repository already earned `Question Family ↓ Answer Responsibility ↓ Bounded Inquiry`?

No, not as a three-layer architecture. The repository has earned a weaker implementation-backed pattern: Question Family rows carry answer-responsibility metadata and point to existing bounded surfaces. Answer Responsibility has not become an independent layer between Question Family and Bounded Inquiry.

Confidence: high.

## Tests run

- `pytest -q tests/test_question_surface_inventory.py tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_listener_endpoint_authority.py tests/test_inquiry_artifacts.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Recommended bounded implementation slice

No implementation recommendation is made for `ask`, routing, planners, conversation runtime, LLM interpretation, a generic responsibility framework, or new inquiry architecture.

If future work is requested, the bounded slice should remain observational: add a read-only test or audit that proves the current question-surface inventory's responsibility field remains static, non-routing, and tied to rows rather than creating or recommending a new responsibility abstraction.
