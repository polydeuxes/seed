# Question Family Artifact Reconciliation

## Scope

This reconciliation asks whether the repository has already implemented **Question Families** as observable repository artifacts independent of CLI surfaces. It remains observational: it does not propose `ask`, routing, planner behavior, semantic search, embeddings, conversation runtime, or natural-language interpretation.

Repository authority for this report comes from implementation directly involved in `question_surface_inventory`, existing inquiry/authority surfaces, diagnostic inventory, diagnostic shape audit, CLI registration, and authority evaluators.

## Executive answer

**Yes, with a narrow boundary.** Question Families have become observable repository artifacts as rows in the static `question_surface_inventory` implementation. The artifact is implementation-backed because it is a dataclass-backed registry, rendered by a CLI surface, included in diagnostic inventory, covered by diagnostic shape audit, and tested for field shape, read-only diagnostic behavior, and non-router boundaries.

**No, not as an operational router or evaluator.** Current implementation does not route operator questions by family, does not infer intent, does not choose commands, and does not make Question Family membership executable beyond static inventory observation.

## 1. Implementation-backed Question Family properties

| Property | Implementation-backed? | Evidence | Conclusion | Confidence |
|---|---:|---|---|---:|
| Family identifier | Yes | `QuestionSurfaceInventoryRow.question_family`; every row supplies a string value. | The family identifier is a first-class row field. | High |
| Example questions | Yes | `example_questions` is a tuple field converted to JSON lists; tests require non-empty examples for all rows. | Examples are observable metadata, not routing input. | High |
| Bounded inquiry | Partly, through answer responsibility and authority-bound surfaces | Rows bind families to a named surface and answer responsibility; authority evaluators expose bounded desired observations, required observations, authority, outcome, uncertainty, and boundaries. | The inventory binds families to bounded answering responsibilities, but does not model bounded inquiry as a separate field named `bounded_inquiry`. | Medium |
| CLI surface | Yes | `surface` and `surface_flag` are fields; rows include direct flags such as `--container-ownership-authority`. | CLI surface is explicitly mapped from each family row. | High |
| Responsibility | Yes | `answer_responsibility` is a row field and rendered in human output. | A Question Family owns answer-responsibility metadata. | High |
| Authority boundary | Yes | `authority_boundary` is a row field; diagnostic inventory records the question inventory as read-only/no-record/no-ledger/no-mutation. | Boundary is explicit, static, and observable. | High |
| Notes | Yes | `notes` is a row field and JSON output field; tests check anti-router notes by searching rendered row content. | Notes preserve limitations such as no routing or no inference. | High |

## 2. Presentation, documentation, implementation artifact, operational artifact

| Classification | Current status | Evidence | Confidence |
|---|---|---|---:|
| Presentation | Yes, but not only presentation. Human formatting renders families, surfaces, responsibility, and boundaries. | `format_question_surface_inventory` formats the static rows. | High |
| Documentation | Partly. The inventory has explanatory row notes and examples, but the authoritative binding is code, not prose docs. | The row registry lives in `seed_runtime/question_surface_inventory.py`, not only under `docs/`. | High |
| Implementation artifact | Yes. It is a dataclass-backed build function with JSON conversion and tests. | `QuestionSurfaceInventoryRow`, `build_question_surface_inventory`, `question_surface_inventory_json`, and tests. | High |
| Operational artifact | Narrowly yes. It is exposed through `seed --question-surface-inventory`, registered in diagnostic inventory, and shape-audited. It remains read-only and non-mutating. | CLI registration, diagnostic inventory entry, and shape audit spec. | High |

## 3. Relationship cardinality between families and CLI surfaces

Current implementation demonstrates a **one-row-to-one-surface mapping** in the static inventory:

- 17 question-family rows were observed from `python scripts/seed_local.py --question-surface-inventory --json`.
- All `question_family` values were unique.
- All `surface` values were unique.
- All `surface_flag` values were unique.
- No duplicate surfaces were observed.

Therefore, under current implementation evidence:

| Question | Current answer | Confidence |
|---|---|---:|
| Can two CLI surfaces answer the same Question Family? | Not in the current inventory. No duplicate family rows were observed and each row has one surface/flag. | High for current inventory; low for design intent beyond current implementation. |
| Can one CLI surface answer multiple Question Families? | Not in the current inventory. No duplicate surface or flag values were observed. | High for current inventory; low for design intent beyond current implementation. |

This is an observation about the current registry, not a claim that the implementation forbids future many-to-one or one-to-many mappings. There is no validator enforcing cardinality beyond current test expectations and static row content.

## 4. Separation of Question Family, Bounded Inquiry, and CLI Surface

Current implementation distinguishes these concepts, but not all at equal strength.

| Layer | Separate implementation evidence | Coupling still present | Confidence |
|---|---|---|---:|
| Question Family | `question_family` is a field in the question-surface row. | It exists only inside rows that also include surface mapping. | High |
| Bounded Inquiry | Authority evaluators and inquiry surfaces expose bounded desired observations, required observations, outcomes, uncertainties, and boundaries. Inventory rows expose `answer_responsibility`. | The inventory does not have a distinct `bounded_inquiry` identifier field; bounded inquiry is represented by responsibility/surface behavior, not a separate registry key. | Medium |
| CLI Surface | `surface` and `surface_flag` are explicit fields and CLI registration invokes the inventory surface directly. | Every implemented family row currently names exactly one CLI surface. | High |

Conclusion: the repository distinguishes `Question Family -> answering responsibility/inquiry surface -> CLI Surface`, but the middle layer is not fully independent in the `question_surface_inventory` schema because there is no standalone bounded-inquiry identifier field.

## 5. Effect of removing Question Families

| Loss type | Would removal cause it? | Support | Confidence |
|---|---:|---|---:|
| Implementation loss | Yes. Removing Question Families would remove a dataclass field, static row data, JSON output shape, formatter content, CLI behavior, and tests. | The registry and tests require `question_family`. | High |
| Observable capability loss | Yes. `seed --question-surface-inventory` would no longer expose family membership, example-question coverage, or family-to-surface mappings. | CLI JSON output currently exposes 17 rows with family fields. | High |
| Documentation loss | Yes. Examples, notes, responsibilities, and boundaries would no longer document the mapping in implementation-backed inventory output. | Row metadata provides implemented explanatory content. | High |

The loss would be all three, while still not removing the underlying diagnostic surfaces themselves.

## 6. Observability of Question Families

| Observable characteristic | Already implementation-backed? | Evidence | Confidence |
|---|---:|---|---:|
| Membership | Yes | Static inventory rows enumerate families. | High |
| Coverage | Partly | Rows cover known answering surfaces represented in the inventory; diagnostic inventory separately lists 44 diagnostic surfaces. There is no implemented completeness proof that every possible surface or inquiry is represented. | Medium |
| Recurrence | Partly | Family rows are stable static entries and can be repeatedly rendered; no recurrence metric exists. | Medium |
| Uniqueness | Observed yes | Current JSON output has unique family, surface, and flag values. No explicit uniqueness validator was found. | Medium |
| Mapping completeness | Partly | Each row has family, examples, surface, flag, responsibility, boundary, and notes. Completeness against all repository surfaces is not enforced. | Medium |
| Unused families | Not directly | No observer was found that proves whether a family is unused, because the registry is not a router and does not track invocations. | High |
| Duplicate mappings | Observed absent, not enforced | Current rows have no duplicate surfaces/families/flags; tests do not assert uniqueness. | Medium |

## 7. What kind of property is Question Family?

| Candidate | Supported? | Evidence | Confidence |
|---|---|---|---:|
| Property of the operator | No. Example questions are operator-like prompts, but there is no operator state, intent model, or question classification runtime. | CLI rejects free-text question arguments for the inventory. | High |
| Property of inquiries | Partly. Families group answer responsibilities that point to bounded inquiry-like surfaces. | Family rows map to surfaces whose implementations expose bounded observations, authority, uncertainty, and outcomes. | Medium |
| Repository artifact | Yes. Families are committed code data rendered and audited by repository-owned CLI/diagnostic surfaces. | Static registry, CLI, diagnostic inventory, shape audit, tests. | High |
| Something else | Yes: a static indexing/mapping artifact. | Notes explicitly say rows are inventory only and not routing. | High |

A Question Family currently owns **static answer-responsibility classification**: it names a family, gives example questions, identifies the existing surface that answers it, and states the read-only authority boundary. It does not own routing, execution, command choice, operator intent, or truth promotion.

## 8. Has the repository earned `Operator Question -> Question Family -> Bounded Inquiry`?

The repository has earned a **partial architectural layer**:

```text
Question Family
↓
answer responsibility / bounded inquiry surface
↓
CLI Surface
```

It has **not** earned an operational layer that starts with arbitrary operator questions. Strong evidence:

- The inventory is static and read-only.
- The inventory rejects free-text question arguments.
- Tests assert it is not a router or recommender.
- Row notes repeatedly state that the inventory does not infer required arguments, targets, or intent.

Strongest supporting evidence for the layer:

1. Families are implementation fields, not just prose.
2. Families are observable through CLI JSON and human output.
3. The diagnostic registry declares the surface and its no-record/no-mutation behavior.
4. The diagnostic shape audit checks the implementation declaration.
5. Authority evaluators implement bounded inquiries with desired observations, required observations, authority, outcomes, uncertainty, and non-mutation boundaries.

Strongest contradictory evidence:

1. The inventory schema does not include a standalone `bounded_inquiry` field.
2. Every current family row is coupled to exactly one CLI surface/flag.
3. No implementation routes an operator question to a family.
4. No implementation tracks family usage, unused families, or duplicate mappings as first-class audit findings.
5. The `question_surface_inventory` surface itself is a diagnostic inventory row and not a general question layer runtime.

Final conclusion: **Question Families are already observable repository artifacts, but their operational responsibility is static classification and answer-surface accountability, not routing or interpretation.** The repository has earned `Question Family -> Bounded Inquiry` as a narrow implementation-backed mapping layer, but not `Operator Question -> Question Family` as an operational layer independent of CLI presentation.

## Commands executed

```bash
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' .. /workspace 2>/dev/null | head -50 && git status --short
cat AGENTS.md && rg -n "question_surface_inventory|diagnostic-inventory|diagnostic-shape-audit|knowledge-reachability|Question Family|question family|bounded inquiry|authority" .
rg --files | rg 'question_surface_inventory|diagnostic_inventory|diagnostic_shape_audit|seed_local.py|authority.*\.py|inquiry'
sed -n '1,240p' seed_runtime/question_surface_inventory.py && sed -n '1,180p' tests/test_question_surface_inventory.py && rg -n "question_surface_inventory|diagnostic_inventory|diagnostic_shape_audit|container_ownership_authority|service_ownership_authority|listener_endpoint_authority" scripts/seed_local.py seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py
sed -n '240,360p' seed_runtime/question_surface_inventory.py; sed -n '660,710p' seed_runtime/diagnostic_inventory.py; sed -n '600,618p' seed_runtime/diagnostic_shape_audit.py; sed -n '2360,2395p' scripts/seed_local.py; sed -n '6212,6226p' scripts/seed_local.py
python scripts/seed_local.py --question-surface-inventory --json > /tmp/qsi.json && python - <<'PY'
import json,collections
rows=json.load(open('/tmp/qsi.json'))
print('rows',len(rows))
print('fields',sorted(rows[0]))
print('families_unique', len({r['question_family'] for r in rows})==len(rows))
print('surfaces_unique', len({r['surface'] for r in rows})==len(rows))
print('flags_unique', len({r['surface_flag'] for r in rows})==len(rows))
print('empty_examples', [r['question_family'] for r in rows if not r['example_questions']])
print('duplicate_surfaces', [k for k,v in collections.Counter(r['surface'] for r in rows).items() if v>1])
PY
python scripts/seed_local.py --diagnostic-inventory --json > /tmp/di.json
python scripts/seed_local.py --diagnostic-shape-audit --json > /tmp/dsa.json
python - <<'PY'
import json
for path,name in [('/tmp/di.json','inventory'),('/tmp/dsa.json','shape')]:
 data=json.load(open(path));
 print(name, 'rows', len(data))
 print([r for r in data if r.get('name')=='question_surface_inventory' or r.get('diagnostic')=='question_surface_inventory'][:3])
PY
sed -n '1,220p' seed_runtime/container_ownership_authority.py; sed -n '1,220p' seed_runtime/service_ownership_authority.py; sed -n '1,180p' seed_runtime/listener_endpoint_authority.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`

## Files changed

- `docs/question_family_artifact_reconciliation.md`

## LOC changed

- Added 199 lines.

## Tests run

```bash
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Recommended bounded implementation slice

None. This task was observational and explicitly bounded away from implementation recommendations. The current repository-backed answer is that Question Families are observable static inventory artifacts with answer-responsibility ownership, not routers or natural-language interpretation surfaces.
