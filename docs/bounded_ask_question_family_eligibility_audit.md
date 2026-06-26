# Bounded Ask Question-Family Eligibility Audit

This reconciliation is observational. It reviews only the current question-surface inventory, existing inquiry/read-only surfaces, CLI registration, surface arguments, JSON output paths, and human formatters. It does not recommend routing, planning, semantic matching, conversation, operator prose interpretation, embeddings, or parameter inference.

Repository authority wins: the current bounded `ask` model is treated as exact Question Family selection followed by deterministic dispatch to an existing surface. Eligibility below means the current implementation can already participate in that bounded model without adding new architecture.

## Scope and implementation evidence

Reviewed implementation:

- `seed_runtime/question_surface_inventory.py` for the static Question Family inventory and its JSON/human formatters.
- `scripts/seed_local.py` for CLI registrations, argument arity, JSON gates, and dispatch handlers.
- Existing surface modules imported by `scripts/seed_local.py` for build/JSON/formatter ownership as referenced by CLI dispatch.

Key implementation facts:

- The inventory is static and returns 17 rows from `build_question_surface_inventory()`.
- The CLI registers every inventory row's current `surface_flag` except that bounded `ask` itself is not present as a CLI surface in the reviewed implementation.
- Generic `--json` is allowed for most inventory rows, but `knowledge reachability` uses the surface-specific `--knowledge-reachability-audit-json` flag and `source navigation` / `inquiry orientation` do not expose JSON in the reviewed CLI path.
- Human formatter support exists for all reviewed surfaces through the CLI dispatch path.

## Classification vocabulary

- `eligible_now`: exact Question Family dispatch can invoke the existing surface with no required family-specific parameters, with current JSON and human output support.
- `eligible_with_parameters`: exact Question Family dispatch can invoke the existing surface only if the operator supplies explicit required parameters; no inference or defaults are recommended here.
- `diagnostic_only`: the row describes diagnostic registry/shape surfaces rather than a bounded inquiry answer surface for `ask` validation.
- `not_dispatchable`: the inventory row points at a surface that lacks a required ask-participation characteristic in current implementation, such as JSON output, despite having a CLI path.
- `unsupported`: no current implementation-backed CLI dispatch surface exists. No current row falls in this category.

## Reconciliation table

| Question Family | Classification | Dispatch target | Required parameters | JSON support | Formatter support | Bounded ask eligibility | Implementation rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| operational pressure | `eligible_now` | `--ops-brief` -> `build_ops_brief(...)` | none beyond common app state options | yes, generic `--json` prints `brief.to_json_dict()` | yes, `format_ops_brief(...)` | immediately eligible | CLI registers a no-argument read-only `--ops-brief`; dispatch builds the brief and chooses JSON or formatter output. |
| current operational explanation | `eligible_now` | `--operational-story` -> `build_operational_story(...)` | none beyond common app state options | yes, generic `--json` via `operational_story_json(...)` | yes, `format_operational_story(...)` | immediately eligible | CLI registers a no-argument story view and dispatches deterministically to existing JSON/human output. |
| derivation explanation | `eligible_with_parameters` | `--reasoning-path DOMAIN SUBJECT` -> `build_reasoning_path_audit(...)` | explicit `DOMAIN`, explicit `SUBJECT` | yes, generic `--json` via `reasoning_path_audit_json(...)` | yes, `format_reasoning_path_audit(...)` | eligible only when parameters are supplied exactly | CLI registration uses `nargs=2`; inventory notes that domain and subject are required and not inferred. |
| selection explanation | `eligible_with_parameters` | `--selection-path TARGET` -> `build_selection_path_audit(...)` | explicit `TARGET` | yes, generic `--json` via `selection_path_audit_json(...)` | yes, `format_selection_path_audit(...)` | eligible only when target is supplied exactly | CLI registration requires a target argument; inventory notes target inference is outside scope. |
| knowledge reachability | `eligible_now` | `--knowledge-reachability-audit` -> `build_knowledge_reachability_audit_result(...)` | none; optional family, subject, kind, limit, all, max-seconds, debug filters exist | yes, but via `--knowledge-reachability-audit-json`, not generic `--json` | yes, `format_knowledge_reachability_table(...)` | immediately eligible with surface-specific JSON flag | CLI registers a no-argument audit plus optional filters; dispatch renders JSON through the surface-specific JSON flag or human table otherwise. |
| capability pressure | `eligible_now` | `--capability-needs` -> `build_capability_needs(...)` | none; optional `--subject` and `--diagnostic` filters exist | yes, generic `--json` via `capability_needs_json(...)` | yes, `format_capability_needs(...)` | immediately eligible | CLI registers a no-argument capability-needs surface with optional filters and deterministic JSON/human output. |
| ownership ambiguity | `eligible_now` | `--ownership-discrepancies` -> `build_ownership_discrepancies(...)` | none; optional `--subject`; optional `--record` is outside ask | yes, generic `--json` via `ownership_discrepancies_json(...)` | yes, `format_ownership_discrepancies(...)` | immediately eligible for non-recording use | Inventory row describes default non-recording use; CLI read path works without subject and renders JSON/human output. |
| observation domain coverage | `eligible_now` | `--observation-domains [DOMAIN]` -> `build_observation_domains(...)` | none; optional explicit `DOMAIN`; omitted argument renders all domains | yes, generic `--json` via `observation_domains_json(...)` | yes, `format_observation_domains(...)` | immediately eligible for all-domain form | CLI uses optional argument with `const="__all__"`, so the current surface already has a deterministic all-domain invocation. |
| observation permission state | `eligible_now` | `--observation-permission [DOMAIN]` -> `build_observation_permission(...)` | none; optional explicit `DOMAIN`; omitted argument renders all domains | yes, generic `--json` via `observation_permission_json(...)` | yes, `format_observation_permission(...)` | immediately eligible for all-domain form | CLI uses optional argument with `const="__all__"`, so the current surface already has a deterministic all-domain invocation. |
| authority-constrained container ownership | `eligible_now` | `--container-ownership-authority` -> `evaluate_container_ownership_authority_slice(...)` | none beyond common app state options | yes, generic `--json` via `container_ownership_authority_json(...)` | yes, `format_container_ownership_authority(...)` | immediately eligible | CLI registers a no-argument constrained-authority evaluator and dispatches to existing JSON/human output. |
| authority-constrained service ownership | `eligible_now` | `--service-ownership-authority` -> `evaluate_service_ownership_authority_slice(...)` | none beyond common app state options | yes, generic `--json` via `service_ownership_authority_json(...)` | yes, `format_service_ownership_authority(...)` | immediately eligible | CLI registers a no-argument constrained-authority evaluator and dispatches to existing JSON/human output. |
| listener endpoint reachability | `eligible_now` | `--listener-endpoint-authority` -> `evaluate_listener_endpoint_authority_slice(...)` | none beyond common app state options | yes, generic `--json` via `listener_endpoint_authority_json(...)` | yes, `format_listener_endpoint_authority(...)` | immediately eligible | CLI registers a no-argument constrained-authority evaluator and dispatches to existing JSON/human output. |
| surface inventory | `diagnostic_only` | `--diagnostic-inventory` -> `diagnostic_inventory_json()` / `format_diagnostic_inventory()` | none | yes, generic `--json` | yes | not an ask validation target | The inventory row explicitly points to the diagnostic registry, not the question-family inventory; it is diagnostic visibility rather than an inquiry-answer surface. |
| surface shape validation | `diagnostic_only` | `--diagnostic-shape-audit` -> `build_diagnostic_shape_audit()` | none; optional mismatch/status filters exist | yes, generic `--json` via `diagnostic_shape_audit_json(...)` | yes, `format_diagnostic_shape_audit(...)` | not an ask validation target | This checks diagnostic declarations against implementation shape and does not execute target inquiry surfaces. |
| source definition/import lookup | `not_dispatchable` | `--source-navigation QUERY` -> `build_source_navigation(...)` | explicit `QUERY` | no reviewed CLI JSON path | yes, `format_source_navigation(...)` | not eligible today | CLI registration requires `QUERY`, and the JSON gate does not include `--source-navigation`; the dispatch path prints only the human formatter. |
| inquiry orientation | `not_dispatchable` | `--inquiry-orientation [NOTE_ID]` -> `build_inquiry_orientation(...)` | latest note by omission or explicit `NOTE_ID`; current note storage must contain a selected note | no reviewed CLI JSON path | yes, `format_inquiry_orientation(...)` | not eligible today | CLI supports latest or explicit note selection, but the JSON gate does not include `--inquiry-orientation`; missing note returns an error rather than a deterministic answer payload. |
| projection shape visibility | `eligible_now` | `--projection-shape` -> `build_projection_shape()` | none | yes, generic `--json` via `projection_shape_json(...)` | yes, `format_projection_shape(...)` | immediately eligible | CLI registers a no-argument read-only implementation-backed view and dispatches to existing JSON/human output. |

## Classification counts

| Classification | Count |
| --- | ---: |
| `eligible_now` | 11 |
| `eligible_with_parameters` | 2 |
| `diagnostic_only` | 2 |
| `not_dispatchable` | 2 |
| `unsupported` | 0 |

## Answers to required questions

### 1. Classification for every current Question Family

The classification is shown in the reconciliation table above. In short, 11 of 17 rows are immediately eligible, 2 require explicit parameters, 2 are diagnostic-only, and 2 are not dispatchable for bounded ask today because they lack current JSON support and/or a stable deterministic answer payload in the reviewed CLI path.

### 2. Immediately eligible families: dispatch target, arguments, JSON, formatter, parity

The immediately eligible families are:

1. `operational pressure`
2. `current operational explanation`
3. `knowledge reachability`
4. `capability pressure`
5. `ownership ambiguity`
6. `observation domain coverage`
7. `observation permission state`
8. `authority-constrained container ownership`
9. `authority-constrained service ownership`
10. `listener endpoint reachability`
11. `projection shape visibility`

All immediately eligible rows share deterministic dispatch to one existing CLI surface, no required family-specific argument, an existing human formatter, and existing JSON output. Expected output parity is implementation-backed by the CLI dispatch pattern: the same built result object is passed either to a JSON adapter or to the human formatter, except `knowledge reachability`, where the same `result.rows` and `result.metadata` are rendered via a surface-specific JSON flag or the table formatter.


### 3. Parameter-only eligible families

Only these inventory rows require explicit parameters while otherwise having JSON and formatter support:

- `derivation explanation`: requires explicit `DOMAIN` and explicit `SUBJECT`.
- `selection explanation`: requires explicit `TARGET`.

No inference, defaults, or recommendations are introduced.

### 4. Smallest reason each non-immediately eligible family does not participate today

- `derivation explanation`: requires explicit domain and subject.
- `selection explanation`: requires explicit target.
- `surface inventory`: diagnostic inventory only.
- `surface shape validation`: diagnostic shape validation only.
- `source definition/import lookup`: requires explicit query and lacks reviewed JSON support.
- `inquiry orientation`: depends on selected existing note/latest note availability and lacks reviewed JSON support.

### 5. Possible inventory misclassifications after bounded ask

Implementation-backed inconsistencies to note, without redesign:

- `source definition/import lookup` is listed as a Question Family with a surface, but its current CLI path has no JSON output. If bounded ask requires JSON/human parity, this row is overstated as ask-ready.
- `inquiry orientation` is listed as a Question Family, but current CLI output is human-only and depends on note-store state. It is a valid existing surface, but not currently ask-ready under the same bounded output characteristics as the immediately eligible families.
- `knowledge reachability` supports JSON through `--knowledge-reachability-audit-json`, while most other eligible rows use generic `--json`. This is not a functional blocker, but it is an implementation-shape inconsistency for any exact dispatcher that expects one JSON mechanism.
- `observation domain coverage` and `observation permission state` are inventory notes saying they accept explicit domain or all domains. The CLI confirms omission maps deterministically to all-domain output, so these rows should be treated as `eligible_now`, not parameter-required.

### 6. Common characteristics of `eligible_now` families

All `eligible_now` families share these implementation-backed traits:

- A single existing surface flag in the inventory.
- CLI registration for that flag.
- No required Question-Family-specific parameters.
- Deterministic dispatch in `scripts/seed_local.py` to a specific builder/evaluator.
- Existing human formatter.
- Existing JSON rendering path.
- Read-only or default non-recording behavior for the reviewed invocation.

### 7. Currently ineligible families that could become eligible without forbidden architecture

These conclusions stay within deterministic exact dispatch and do not require routing, planning, semantic matching, or parameter inference:

- `derivation explanation` can participate when an operator supplies exact `DOMAIN` and `SUBJECT`. No new architecture is required for exact argument forwarding.
- `selection explanation` can participate when an operator supplies exact `TARGET`. No new architecture is required for exact argument forwarding.
- `source definition/import lookup` could participate if an operator supplies exact `QUERY` and the existing source-navigation result obtains JSON output support. Exact argument forwarding would not require inference, but JSON support would be an implementation change.
- `inquiry orientation` could participate if the ask form either requires an exact `NOTE_ID` or intentionally accepts the existing latest-note selector, and the surface obtains JSON output support. This does not require semantic routing, but it would require implementation work and a clear deterministic note-selection boundary.
- `surface inventory` and `surface shape validation` should remain diagnostic-only for first bounded ask validation because they validate visibility/shape, not ordinary inquiry-answer participation.

### 8. Exactly two recommended manual operator validation targets

Recommended first targets:

1. `authority-constrained service ownership`
   - Simple: no required parameters.
   - Fully bounded: one inventory row, one surface flag, one evaluator, JSON and human output.
   - Architecturally representative: it exercises a current inquiry/authority evaluator rather than a generic registry or diagnostic list.

2. `listener endpoint reachability`
   - Simple: no required parameters.
   - Fully bounded: one inventory row, one surface flag, one evaluator, JSON and human output.
   - Architecturally representative: it validates that another constrained-authority inquiry surface can participate in the same exact-dispatch model without expanding ask.

`operational pressure` is also simple, but it is a composed summary. The two authority surfaces are better first validation targets because they are bounded inquiry evaluators with clearer answer responsibility and less risk of confusing summary composition with routing.

## Report

### Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules' && git status --short
cat AGENTS.md && rg "question_surface_inventory|Question Family|diagnostic-inventory|ask" -n .
sed -n '1,320p' seed_runtime/question_surface_inventory.py && sed -n '1,260p' seed_runtime/cli.py
rg "argparse|ArgumentParser|def main|--ops-brief|--service-ownership|ask" -n seed_runtime seed.py tests | head -200
rg --files | rg 'seed_local|__main__|bin|cli' && sed -n '1,260p' seed_local.py
sed -n '1,340p' scripts/seed_local.py
sed -n '340,760p' scripts/seed_local.py
rg "ops-brief|operational-story|reasoning-path|selection-path|knowledge-reachability|capability-needs|ownership-discrepancies|observation-domains|observation-permission|container-ownership-authority|service-ownership-authority|listener-endpoint-authority|diagnostic-inventory|diagnostic-shape-audit|source-navigation|inquiry-orientation|projection-shape|question-surface|ask" -n scripts/seed_local.py
sed -n '1160,1265p' scripts/seed_local.py && sed -n '1338,1490p' scripts/seed_local.py && sed -n '1785,1935p' scripts/seed_local.py && sed -n '2045,2075p' scripts/seed_local.py
rg "args\.(ops_brief|operational_story|reasoning_path|selection_path|knowledge_reachability_audit|capability_needs|ownership_discrepancies|observation_domains|observation_permission|container_ownership_authority|service_ownership_authority|listener_endpoint_authority|diagnostic_inventory|question_surface_inventory|diagnostic_shape_audit|source_navigation|inquiry_orientation|projection_shape)" -n scripts/seed_local.py
sed -n '2110,2395p' scripts/seed_local.py && sed -n '6150,6500p' scripts/seed_local.py && sed -n '6670,6805p' scripts/seed_local.py && sed -n '6988,7008p' scripts/seed_local.py
python scripts/seed_local.py --question-surface-inventory --json >/tmp/qsi.json && python - <<'PY'
import json
rows=json.load(open('/tmp/qsi.json'))
print(len(rows))
print('\n'.join(r['question_family']+' -> '+r['surface_flag'] for r in rows))
PY
python scripts/seed_local.py --service-ownership-authority --json >/tmp/soa.json
python scripts/seed_local.py --ops-brief --json >/tmp/ops.json
python scripts/seed_local.py --diagnostic-shape-audit --json >/tmp/shape.json
```

### Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_ops_brief.py`

### Files changed

- `docs/bounded_ask_question_family_eligibility_audit.md`

### LOC changed

- Added 216 lines in `docs/bounded_ask_question_family_eligibility_audit.md`.

### Tests run

No product code changed. Validation used the app's existing JSON surfaces:

- `python scripts/seed_local.py --question-surface-inventory --json`
- `python scripts/seed_local.py --service-ownership-authority --json`
- `python scripts/seed_local.py --ops-brief --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`

### Classification counts

- `eligible_now`: 11
- `eligible_with_parameters`: 2
- `diagnostic_only`: 2
- `not_dispatchable`: 2
- `unsupported`: 0

### Recommended manual validation targets

- `authority-constrained service ownership`
- `listener endpoint reachability`
