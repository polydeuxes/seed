# Question Family deterministic dispatch reconciliation

Date: 2026-06-26

## Verdict

The repository has already earned the first bounded deterministic Question Family dispatcher, provided the first implementation is limited to explicit `--question-family` lookup and dispatch to already-registered inquiry surfaces. The implementation evidence supports a presentation layer, not a new architectural layer.

A first bounded `seed ask --question-family service-ownership` would expose the existing relationship:

```text
Question Family -> existing surface flag -> existing evaluator/formatter/JSON output
```

It would not introduce routing, natural language interpretation, planning, semantic matching, or reasoning.

## Scope reviewed

Reviewed implementation directly involved in:

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py` CLI registration and command dispatch
- authority evaluator modules for existing bounded inquiry surfaces:
  - `seed_runtime/container_ownership_authority.py`
  - `seed_runtime/service_ownership_authority.py`
  - `seed_runtime/listener_endpoint_authority.py`

Supporting checks were limited to the current inventory and one representative dispatched inquiry surface.

## Answers

### 1. Does every Question Family already identify exactly one dispatch target?

Yes. `build_question_surface_inventory()` returns one static row per Question Family. Each row contains a `question_family`, `surface`, `surface_flag`, `answer_responsibility`, `authority_boundary`, and notes. The JSON adapter serializes those rows without adding routing logic.

A direct uniqueness check over the current implementation found:

- 17 Question Families.
- 17 unique `question_family` values.
- 17 unique `surface` values.
- 17 unique `surface_flag` values.
- 17 unique `answer_responsibility` values.

This supports exactly one declared dispatch target per current Question Family.

Caveat: some targets require additional explicit arguments, and the inventory says it does not infer those arguments. That caveat does not contradict deterministic dispatch for a bounded first slice such as `service-ownership`, whose target surface does not require an extra subject argument.

### 2. Would a deterministic dispatcher require repository knowledge beyond the current Question Surface Inventory?

For selecting the target surface: no. The inventory already contains the necessary mapping from Question Family to surface name and CLI flag.

For executing a selected surface: yes, but only ordinary existing CLI invocation knowledge is required. The dispatcher must reuse the same command implementation that `scripts/seed_local.py` already uses for the target flag. For the first bounded `service-ownership` slice, that means the dispatcher needs to call the existing projected-state builder, evaluator, JSON adapter, and formatter used by `--service-ownership-authority`.

No additional architectural knowledge, ontology, documentation routing, semantic index, or operator-intent model is required.

### 3. Would the dispatcher perform reasoning?

No. The dispatcher would perform:

```text
lookup -> dispatch
```

The inventory is static and read-only. The existing authority surface performs the domain evaluation after dispatch. The dispatcher itself would only select a row by exact Question Family id and invoke the corresponding existing branch.

### 4. Can the existing inquiry surface already produce the complete answer after dispatch?

For the first bounded `service-ownership` demonstration: yes.

`evaluate_service_ownership_authority_slice()` already returns the answer-bearing fields needed by the surface:

- desired observation
- required observations
- required authority
- available authority
- reachable observations
- blocked observations and details
- outcome
- current strategy and strategy status
- remaining observations
- uncertainty and remaining uncertainty
- blocking boundary
- read-only boundary flags

The existing JSON adapter and text formatter expose those fields. Therefore the dispatcher does not need to add authority, expectation sets, reasoning, boundaries, or uncertainty. Those are already owned by the existing inquiry surface.

### 5. Would `seed ask --question-family service-ownership` introduce a new architectural responsibility?

No, if bounded to exact Question Family ids and deterministic dispatch.

It would be another presentation of an existing repository relationship: the inventory row for authority-constrained service ownership points to `service_ownership_authority` and `--service-ownership-authority`; the CLI already registers that surface and dispatches to the evaluator/formatter/JSON output.

The new responsibility would be only presentation-level command shape: accepting `ask --question-family <id>`, resolving the id to one inventory row, and invoking the existing target surface. It would not become a router, planner, interpreter, or authority evaluator.

### 6. Implementation dependencies required for the first bounded `ask`

Required dependencies for the smallest bounded implementation:

1. Question Surface Inventory
   - Needed for exact Question Family id lookup and target surface metadata.
2. CLI parser
   - Needed to register a bounded `ask` command or equivalent `ask --question-family` argument form.
3. Deterministic dispatch table
   - Needed to map allowed inventory rows to existing in-process handlers. For the first slice, the table can contain only `service-ownership` / `authority-constrained service ownership` aliases if the implementation chooses a stable machine id.
4. Existing surface invocation
   - Needed to call the same logic currently used by `--service-ownership-authority`.
5. Projected state construction
   - Needed because the service ownership authority evaluator accepts `State`.
6. Authority profile
   - Needed because the existing evaluator accepts the constrained authority profile already used by the direct CLI surface.
7. Formatter
   - Needed for human output; already exists as `format_service_ownership_authority()`.
8. JSON output
   - Needed to preserve existing `--json` behavior; already exists as `service_ownership_authority_json()`.
9. Exclusivity validation
   - Needed so `ask` remains mutually exclusive with other lifecycle/read-only surfaces, matching current CLI command shape.
10. Tests
   - Needed to prove exact lookup, no inference, existing output parity, JSON parity, and diagnostic visibility if the new operational surface is registered.

### 7. Intentionally excluded from the first bounded implementation

The first bounded implementation should exclude:

- operator prose
- natural-language interpretation
- LLM interpretation
- semantic search
- embeddings
- fuzzy matching
- conversation
- planning
- recommendation
- automatic parameter inference
- documentation routing
- generic routing
- authority acquisition
- observation execution
- event-ledger writes
- cluster mutation

Repository evidence supports these exclusions because the Question Surface Inventory notes that it does not route operator questions or infer required arguments, while the authority evaluators explicitly use constrained profiles, do not acquire providers, do not create permissions, do not execute observations, do not record, do not write the event ledger, and do not mutate the cluster.

### 8. Remaining architectural gap after completing bounded `ask`

The immediate remaining gap would be coverage and parameterization, not architecture.

After the first bounded `service-ownership` demonstration, the repository would still need implementation-backed rules for which other Question Families are eligible for `ask`, especially rows whose target surfaces require explicit extra parameters such as domain, subject, target, query, note id, or domain filter. The current trajectory supports exact dispatch, but not inference of missing parameters.

## Minimal dispatch path

For the smallest demonstration:

```text
seed ask --question-family service-ownership
  -> exact Question Family lookup
  -> inventory row: authority-constrained service ownership
  -> surface_flag: --service-ownership-authority
  -> existing projected_state_from_args(args)
  -> evaluate_service_ownership_authority_slice(state, CONSTRAINED_AUTHORITY_PROFILE)
  -> service_ownership_authority_json(result) when --json is present
  -> format_service_ownership_authority(result) otherwise
```

This closes the loop from Question Family to existing inquiry without adding routing, natural language, or planning.

## Strongest supporting evidence

- The Question Surface Inventory is static, deterministic, read-only, and includes the exact target fields needed for dispatch.
- The current inventory has one unique surface and one unique flag for each Question Family.
- The CLI already registers `--question-surface-inventory` and the authority target surfaces.
- The CLI already dispatches `--service-ownership-authority` to the evaluator, JSON adapter, and formatter.
- The service ownership evaluator already owns authority, reachability, blocked work, uncertainty, and read-only boundary fields.
- The target evaluator boundary declares no recording, no event-ledger writes, no observation execution, no provider acquisition, no permission creation, and no cluster mutation.

## Strongest contradictory evidence

- `ask` does not yet exist in the CLI.
- The Question Surface Inventory explicitly says it does not route operator questions.
- Several inventory rows require explicit arguments that the inventory does not infer.
- The current `question_family` labels are human-readable strings, while the requested example uses a slug (`service-ownership`). A bounded implementation would need a stable exact id or a deliberately small alias table; that alias table must not become fuzzy matching.
- A new operational CLI surface would need diagnostic inventory and diagnostic shape-audit coverage under the repository operational visibility contract.

## Has the repository earned the first deterministic Question Family dispatcher?

Yes, for a bounded exact-id dispatcher that exposes only already implemented zero-extra-argument inquiry surfaces, with service ownership as the smallest initial demonstration.

No, for any broader dispatcher that interprets operator prose, infers missing parameters, searches semantically, plans, routes generically, or treats documentation structure as routing authority.

## Is `seed ask --question-family` a new architectural layer or presentation?

It would be presentation, not a new architectural layer, if implemented as exact lookup over Question Surface Inventory followed by invocation of the existing surface handler.

It would become a new architectural layer only if it claimed responsibility for intent interpretation, routing policy, parameter inference, planning, or answer construction.

## Smallest bounded implementation-backed demonstration

Recommended bounded implementation slice:

1. Add a CLI `ask` form that accepts only `--question-family service-ownership`.
2. Resolve that exact id to the existing inventory row for `authority-constrained service ownership`.
3. Invoke the same in-process code path as `--service-ownership-authority`.
4. Preserve `--json` output parity with `--service-ownership-authority --json`.
5. Preserve text output parity with `--service-ownership-authority` or add only an outer presentation heading that does not alter the underlying answer fields.
6. Register the new operational surface in diagnostic inventory and shape audit if the CLI surface is added.
7. Add tests proving:
   - exact `service-ownership` lookup succeeds;
   - unknown Question Family fails without fuzzy suggestions becoming matching authority;
   - `ask --question-family service-ownership --json` matches the existing service-ownership authority JSON payload;
   - the text path reaches the existing formatter;
   - diagnostic inventory and diagnostic shape audit include the new surface.

## Commands executed

```bash
pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' && git status --short
cat AGENTS.md && rg -n "question_surface_inventory|Question Surface|question-family|question_family|diagnostic-inventory|diagnostic-shape-audit|seed_local|surface_flag|answer_responsibility|authority|Expectation|reasoning" -S .
sed -n '1,240p' seed_runtime/question_surface_inventory.py
sed -n '1,260p' seed_runtime/service_ownership_authority.py
sed -n '1,220p' seed_runtime/container_ownership_authority.py
sed -n '1,220p' seed_runtime/listener_endpoint_authority.py
sed -n '220,520p' seed_runtime/question_surface_inventory.py
sed -n '220,520p' seed_runtime/service_ownership_authority.py
sed -n '220,520p' seed_runtime/container_ownership_authority.py
sed -n '1120,1260p' scripts/seed_local.py
sed -n '2140,2235p' scripts/seed_local.py
sed -n '6150,6230p' scripts/seed_local.py
python - <<'PY'
from seed_runtime.question_surface_inventory import build_question_surface_inventory
rows=build_question_surface_inventory()
print(len(rows))
for f in ('question_family','surface','surface_flag','answer_responsibility'):
 vals=[getattr(r,f) for r in rows]
 print(f, len(vals), len(set(vals)), [v for v in set(vals) if vals.count(v)>1])
PY
python scripts/seed_local.py --question-surface-inventory --json | head -60
python scripts/seed_local.py --service-ownership-authority --json | head -80
git diff --stat && git diff --numstat
pytest -q tests/test_question_surface_inventory.py tests/test_service_ownership_authority.py
git diff --cached --stat && git diff --cached --numstat
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `scripts/seed_local.py`

## Files changed

- `docs/ask_question_family_dispatch_reconciliation.md`

## LOC changed

- Added 262 lines.
- Removed 0 lines.

## Tests run

No code implementation was changed. The validation performed was read-only inspection plus deterministic inventory/CLI output checks listed above. The targeted pytest check passed: `pytest -q tests/test_question_surface_inventory.py tests/test_service_ownership_authority.py` reported 23 passed.
