# Answer Support Chain Missing Relationship Investigation

## Implementation summary

This investigation attempted to connect existing implementation-backed visibility surfaces into a single answer-support chain for representative inquiry surfaces. The current implementation exposes:

- question-family rows with `surface`, `surface_flag`, `dispatch_surface`, JSON support, formatter metadata, responsibility text, and authority boundary;
- diagnostic inventory rows with CLI flags, evidence-source booleans, JSON/record support, ledger/mutation fields, and diagnostic-fact-read fields;
- diagnostic shape-audit specs with module paths plus build, format, JSON, and CLI implementation metadata;
- projected-state consumer rows derived from diagnostic inventory; and
- implementation-trait characterization over fields exposed by selected inventories.

The chain breaks at the same kind of relationship for the dispatchable representative answer surfaces: after a question-family row identifies the answering surface and bounded dispatch surface, the current visibility surfaces do not expose a normalized relation from that surface identifier to the diagnostic inventory row and diagnostic shape-audit implementation spec as one connected support edge. That relationship exists in implementation as independent registries keyed by surface/name and as CLI handlers, but it is not exposed as a normalized answer-support chain.

`implementation_trait_characterization` is different: it is registered in diagnostic inventory and diagnostic shape audit, and it appears as a projected-state consumer, but there is no question-surface-inventory row for it. Its chain therefore terminates before the question-family-to-answering-surface step.

## Implementation evidence inspected

### Question-surface inventory

`QuestionSurfaceInventoryRow` exposes question-family metadata, answering `surface`, `surface_flag`, `bounded_status`, `dispatch_surface`, required args, `json_support`, `human_formatter`, and `implementation_reason`. The bounded dispatch map includes `operational pressure -> ops_brief`, `knowledge reachability -> knowledge_reachability_audit`, and `authority-constrained service ownership -> service_ownership_authority`. It does not include `implementation_trait_characterization` as a question family.

Representative rows:

- `operational pressure` maps to `ops_brief` and `--ops-brief`.
- `knowledge reachability` maps to `knowledge_reachability` and `--knowledge-reachability-audit`.
- `authority-constrained service ownership` maps to `service_ownership_authority` and `--service-ownership-authority`.

### Diagnostic inventory

The diagnostic inventory independently declares rows for all four representative surface identifiers:

- `knowledge_reachability` with projected-state and repo-file use, JSON support, no record support, no event-ledger write, and no cluster mutation.
- `service_ownership_authority` with projected-state and repo-file use, JSON support, diagnostic-fact reads, no record support, no event-ledger write, and no cluster mutation.
- `ops_brief` with projected-state and repo-file use, JSON support, diagnostic-fact reads, no record support, no event-ledger write, and no cluster mutation.
- `implementation_trait_characterization` with JSON support, no projected-state/repo-file use, no record support, no event-ledger write, and no cluster mutation.

### Diagnostic shape audit

The shape-audit implementation specs independently declare implementation entry points for the same four representative surfaces:

- `knowledge_reachability`: `seed_runtime/knowledge_reachability.py`, `build_knowledge_reachability_audit_result`, `format_knowledge_reachability_table`, and `knowledge_reachability_json`.
- `service_ownership_authority`: `seed_runtime/service_ownership_authority.py`, `evaluate_service_ownership_authority_slice`, `format_service_ownership_authority`, and `service_ownership_authority_json`.
- `ops_brief`: `seed_runtime/ops_brief.py`, `build_ops_brief`, `format_ops_brief`, and `to_json_dict`.
- `implementation_trait_characterization`: `seed_runtime/implementation_trait_characterization.py`, `build_implementation_trait_characterization`, `format_implementation_trait_characterization`, and `implementation_trait_characterization_json`.

### Projected state consumers

Projected-state consumer rows are built by iterating diagnostic inventory entries, preserving the inventory `entry.name` as `surface`, copying `entry.cli_flags`, copying the inventory source-use booleans, and applying a common read-only/no-record/no-mutation boundary. This exposes consumer/source traits for diagnostic inventory surfaces, but it does not expose that a given question-family row is joined to the corresponding diagnostic inventory and shape-audit spec.

### Implementation trait characterization

Implementation-trait characterization classifies fields exposed by selected inventory dataclasses. It treats question-surface row fields such as `surface`, `surface_flag`, `human_formatter`, and `implementation_reason` as metadata/non-trait fields, while classifying recurring traits such as evidence sources, operational boundaries, dispatchability, and implementation capability. It therefore exposes trait meanings, not a per-surface relationship chain.

### CLI handlers

The CLI has independent handlers for the representative surfaces:

- `--service-ownership-authority` calls `evaluate_service_ownership_authority_slice(...)` and prints JSON or formatted output.
- `--question-surface-inventory` builds and renders the question-surface inventory.
- `--projected-state-consumers` builds and renders projected-state consumers.
- `--implementation-trait-characterization` builds and renders trait characterization.
- `--ops-brief` builds and renders an ops brief.
- `--knowledge-reachability-audit` builds and renders reachability audit rows.

These handlers prove the implementation entry points exist, but they do not expose a single normalized support edge from a question-family row to the diagnostic inventory row and shape-audit spec.

## Attempted relationship chains

### `service_ownership_authority`

Current supported chain:

```text
authority-constrained service ownership question family
↓
QuestionSurfaceInventoryRow.surface = service_ownership_authority
↓
QuestionSurfaceInventoryRow.surface_flag = --service-ownership-authority
↓
QuestionSurfaceInventoryRow.dispatch_surface = service_ownership_authority
↓
STOP: no exposed normalized edge from question-surface row / dispatch surface to the diagnostic inventory row and diagnostic shape-audit implementation spec
```

Independent implementation evidence after the stop:

```text
DiagnosticInventoryEntry.name = service_ownership_authority
↓
DiagnosticImplementationSpec.name = service_ownership_authority
↓
module_path = seed_runtime/service_ownership_authority.py
↓
build/format/json functions
↓
CLI handler calls evaluate_service_ownership_authority_slice(...) and renders JSON or human output
```

First missing implementation relationship: exposed `question_surface.surface` or `dispatch_surface` to `diagnostic_inventory.name` / `diagnostic_shape_audit.name` support edge.

### `knowledge_reachability`

Current supported chain:

```text
knowledge reachability question family
↓
QuestionSurfaceInventoryRow.surface = knowledge_reachability
↓
QuestionSurfaceInventoryRow.surface_flag = --knowledge-reachability-audit
↓
QuestionSurfaceInventoryRow.dispatch_surface = knowledge_reachability_audit
↓
STOP: dispatch_surface does not equal the diagnostic inventory/shape-audit surface name, and no exposed normalized alias edge connects knowledge_reachability_audit to knowledge_reachability
```

Independent implementation evidence after the stop:

```text
DiagnosticInventoryEntry.name = knowledge_reachability
↓
DiagnosticImplementationSpec.name = knowledge_reachability
↓
module_path = seed_runtime/knowledge_reachability.py
↓
build/format/json functions
↓
CLI handler calls build_knowledge_reachability_audit_result(...) and renders JSON or human output
```

First missing implementation relationship: exposed dispatch alias/support edge from `question_surface.dispatch_surface = knowledge_reachability_audit` to canonical diagnostic surface `knowledge_reachability`, then to diagnostic inventory and shape-audit rows.

### `ops_brief`

Current supported chain:

```text
operational pressure question family
↓
QuestionSurfaceInventoryRow.surface = ops_brief
↓
QuestionSurfaceInventoryRow.surface_flag = --ops-brief
↓
QuestionSurfaceInventoryRow.dispatch_surface = ops_brief
↓
STOP: no exposed normalized edge from question-surface row / dispatch surface to the diagnostic inventory row and diagnostic shape-audit implementation spec
```

Independent implementation evidence after the stop:

```text
DiagnosticInventoryEntry.name = ops_brief
↓
DiagnosticImplementationSpec.name = ops_brief
↓
module_path = seed_runtime/ops_brief.py
↓
build/format/json functions
↓
CLI handler calls build_ops_brief(...) and renders JSON or human output
```

First missing implementation relationship: exposed `question_surface.surface` or `dispatch_surface` to `diagnostic_inventory.name` / `diagnostic_shape_audit.name` support edge.

### `implementation_trait_characterization`

Current supported chain:

```text
STOP: no QuestionSurfaceInventoryRow has surface = implementation_trait_characterization
```

Independent implementation evidence after the stop:

```text
DiagnosticInventoryEntry.name = implementation_trait_characterization
↓
DiagnosticImplementationSpec.name = implementation_trait_characterization
↓
module_path = seed_runtime/implementation_trait_characterization.py
↓
build/format/json functions
↓
ProjectedConsumerRow.surface = implementation_trait_characterization
↓
CLI handler calls build_implementation_trait_characterization() and renders JSON or human output
```

First missing implementation relationship: question-family coverage for the implementation trait characterization surface. Unlike the other three representatives, this break occurs before the question-family-to-surface mapping, not after it.

## Recurring missing relationships

The recurring missing relationship across the dispatchable representative surfaces is:

```text
question-surface answering/dispatch surface
→
canonical diagnostic surface row
→
diagnostic shape-audit implementation spec
```

For `service_ownership_authority` and `ops_brief`, the relationship is mostly a same-key join that exists implicitly in implementation because `QuestionSurfaceInventoryRow.surface`, `DiagnosticInventoryEntry.name`, and `DiagnosticImplementationSpec.name` use the same identifier. For `knowledge_reachability`, the question row has `surface = knowledge_reachability` but `dispatch_surface = knowledge_reachability_audit`, so the chain also needs the existing alias/canonicalization to be exposed rather than inferred.

`implementation_trait_characterization` demonstrates an inconsistency: the surface is visible in diagnostic inventory, diagnostic shape audit, projected-state consumers, and its own CLI handler, but it is not a question-surface-inventory row. Therefore its first missing relationship is not the recurring support join; it is absent question-family coverage.

## Does the relationship not exist, or exist but not exposed?

For the three dispatchable representative answer surfaces, the relationship exists in implementation but is not exposed as one normalized chain:

- Question-surface inventory has answering surface names and dispatch metadata.
- Diagnostic inventory has matching canonical surface rows.
- Diagnostic shape audit has matching implementation specs.
- CLI handlers call the implementation functions.
- Projected-state consumers are already built by iterating diagnostic inventory rows.

The missing part is not new domain knowledge about the surfaces. It is exposed normalized linkage among already-existing identifiers and specs.

For `implementation_trait_characterization`, the question-family relationship does not currently exist in the question-surface inventory. Other implementation relationships for the surface do exist and are exposed independently.

## Highest-leverage next relationship

If exactly one implementation relationship were exposed next, the highest-leverage relationship supported by current implementation evidence would be:

```text
QuestionSurfaceInventoryRow.surface / dispatch_surface
→
canonical DiagnosticInventoryEntry.name
→
DiagnosticImplementationSpec.name
```

This would connect the greatest number of existing visibility surfaces because it joins question-surface inventory, bounded ask dispatch metadata, diagnostic inventory, diagnostic shape audit, projected-state consumers, implementation-trait characterization metadata, and CLI implementation entry points using identifiers that already exist.

This would primarily connect existing visibility. It would not require introducing fundamentally new implementation knowledge for the dispatchable representative surfaces. The only observed non-recurring gap is that `implementation_trait_characterization` lacks question-family coverage, so that surface would still need explicit question-inventory coverage before it could enter a question-family support chain.

## Implementation-backed inconsistencies

- `knowledge_reachability` uses `surface = knowledge_reachability` while bounded dispatch exposes `dispatch_surface = knowledge_reachability_audit`; diagnostic inventory and shape-audit specs use `knowledge_reachability` as the canonical name.
- `implementation_trait_characterization` is present in diagnostic inventory, diagnostic shape audit, projected-state consumers, and CLI handling, but not in question-surface inventory.
- Implementation-trait characterization classifies `surface` and `surface_flag` as metadata/non-trait fields rather than a relationship edge, so it cannot itself supply the missing per-surface support chain.

## Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!tests/.venv' && git status --short
cat AGENTS.md && rg -n "Question Surface Inventory|question.*inventory|diagnostic-inventory|diagnostic-shape-audit|Projected State Consumers|Implementation Trait Characterization|service_ownership_authority|knowledge_reachability|ops_brief|implementation_trait" -S .
sed -n '1,390p' seed_runtime/question_surface_inventory.py
sed -n '1,280p' seed_runtime/implementation_trait_characterization.py
sed -n '1,230p' seed_runtime/projected_state_consumers.py
sed -n '1,220p' seed_runtime/diagnostic_inventory.py
sed -n '80,190p' seed_runtime/diagnostic_shape_audit.py
sed -n '480,660p' seed_runtime/diagnostic_shape_audit.py
sed -n '6200,6930p' scripts/seed_local.py
python scripts/seed_local.py --question-surface-inventory --json > /tmp/q.json
python scripts/seed_local.py --diagnostic-inventory --json > /tmp/d.json
python scripts/seed_local.py --diagnostic-shape-audit --json > /tmp/s.json
python scripts/seed_local.py --projected-state-consumers --json > /tmp/p.json
python scripts/seed_local.py --implementation-trait-characterization --json > /tmp/t.json
python - <<'PY'
import json
for path,key in [('/tmp/q.json','surface'),('/tmp/d.json','name'),('/tmp/s.json','name'),('/tmp/p.json','surface')]:
 data=json.load(open(path));
 if isinstance(data,dict): data=data.get('items',data.get('rows',data))
 print(path)
 for n in ['service_ownership_authority','knowledge_reachability','ops_brief','implementation_trait_characterization']:
  rows=[r for r in data if r.get(key)==n or r.get('surface')==n]
  print(n, rows[:1])
PY
rg -n "name=\"(knowledge_reachability|service_ownership_authority|ops_brief|implementation_trait_characterization)\"|name: str|supports_json|mutates_cluster|reads_diagnostic_facts" seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py
```

## Files inspected

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projected_state_consumers.py`
- `seed_runtime/implementation_trait_characterization.py`

## Files changed

- `docs/answer_support_chain_missing_relationship.md`

## LOC changed

- Added 309 lines in `docs/answer_support_chain_missing_relationship.md`.

## Tests run

This was a read-only implementation investigation plus one documentation artifact. No production diagnostic surface, CLI flag, audit implementation, probe, or recordable output was changed, so diagnostic inventory/shape-audit tests were not required by the operational visibility contract.

Commands used as checks:

```text
python scripts/seed_local.py --question-surface-inventory --json > /tmp/q.json
python scripts/seed_local.py --diagnostic-inventory --json > /tmp/d.json
python scripts/seed_local.py --diagnostic-shape-audit --json > /tmp/s.json
python scripts/seed_local.py --projected-state-consumers --json > /tmp/p.json
python scripts/seed_local.py --implementation-trait-characterization --json > /tmp/t.json
```

The next implementation-backed visibility slice
most likely to connect existing support relationships is:

QuestionSurfaceInventoryRow.surface / dispatch_surface → canonical DiagnosticInventoryEntry.name → DiagnosticImplementationSpec.name
