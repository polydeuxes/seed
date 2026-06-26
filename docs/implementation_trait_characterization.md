# Implementation Trait Characterization

## Implementation summary

This investigation used Seed's existing visibility surfaces rather than direct architectural inference. The surfaces inspected were:

- `projected_state_consumers`
- `diagnostic_inventory`
- `question_surface_inventory`
- `operational_surface_inventory`

The exposed traits form a coherent implementation vocabulary for the currently visible surfaces. They describe four recurring implementation concerns:

1. **Evidence source** — where a surface obtains implementation information.
2. **Operational boundary** — what a surface is allowed to do while answering or recording.
3. **Dispatchability** — whether and how a question family participates in bounded ask dispatch.
4. **Implementation capability** — support or classification facts about the surface itself.

No new trait categories are required to characterize the recurring implementation-backed traits observed in these four surfaces.

## Complete trait inventory

| Trait | Exposed by | Concern | Implementation-backed meaning |
|---|---|---|---|
| `uses_projected_state` | `projected_state_consumers`, `diagnostic_inventory` | evidence source | The surface reads projected state, as declared by diagnostic inventory and copied into projected-state consumer rows. |
| `uses_repo_files` | `projected_state_consumers`, `diagnostic_inventory` | evidence source | The surface reads repository files, as declared by diagnostic inventory and copied into projected-state consumer rows. |
| `uses_static_inventory` | `projected_state_consumers` | evidence source | The surface obtains information from static registry/row data for known inventory-like surfaces. |
| `uses_live_observation` | `projected_state_consumers` | evidence source | The surface obtains information from the existing live observation collection surface. |
| `uses_event_ledger` | `projected_state_consumers` | evidence source | The surface obtains information from event-ledger-backed history or policy audit surfaces. |
| `uses_runtime_input` | `projected_state_consumers` | evidence source | The surface obtains information from existing inquiry/runtime input surfaces. |
| `read_only` | `projected_state_consumers.boundary`, question inventory authority text | operational boundary | The surfaced operation is observational and does not perform mutation. |
| `records` | `projected_state_consumers.boundary` | operational boundary | Whether the consumer row itself records output; current projected-state consumer rows declare `false`. |
| `supports_record` | `diagnostic_inventory` | operational boundary / capability | Whether the diagnostic CLI surface supports `--record`; when true, `record_scope` supplies the recording boundary. |
| `record_scope` | `diagnostic_inventory` | operational boundary | The subject scope for diagnostic recording, currently `none` or `diagnostic_run`. |
| `writes_event_ledger` | `projected_state_consumers.boundary`, `diagnostic_inventory` | operational boundary | Whether the surface writes to the event ledger. Diagnostic inventory has true values only for recordable diagnostic fact surfaces observed in this run. |
| `mutates_cluster` | `projected_state_consumers.boundary`, `diagnostic_inventory` | operational boundary | Whether the surface mutates cluster truth; all inspected diagnostic entries currently report `false`. |
| `executes_observation` | `projected_state_consumers.boundary` | operational boundary | Whether the surface performs observation execution; current projected-state consumer rows declare `false`. |
| `permission_creation` | `projected_state_consumers.boundary` and authority surfaces' JSON vocabulary | operational boundary | Whether the operation creates permissions; current projected-state consumer boundary declares `false`. |
| `provider_acquisition` | `projected_state_consumers.boundary` and authority surfaces' JSON vocabulary | operational boundary | Whether the operation acquires a provider; current projected-state consumer boundary declares `false`. |
| `bounded_status` | `question_surface_inventory` | dispatchability | Derived from bounded ask maps as `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`. |
| `dispatch_surface` | `question_surface_inventory` | dispatchability | The implementation surface selected by bounded ask maps for a dispatchable question family. |
| `required_surface_args` | `question_surface_inventory` | dispatchability | Required arguments that must be supplied before bounded dispatch can invoke parameterized surfaces. |
| `supports_json` | `diagnostic_inventory` | implementation capability | Whether the diagnostic surface supports JSON output. |
| `json_support` | `question_surface_inventory` | implementation capability | Whether the answering surface has JSON support according to the question inventory row. |
| `json_capable` | `operational_surface_inventory` | implementation capability | Whether an argparse-discovered operational flag has JSON-capable companion support from registered diagnostic flags. |
| `registered` | `operational_surface_inventory` | implementation capability | Whether an argparse-discovered operational flag is present in diagnostic inventory registration. |
| `category` | `operational_surface_inventory` | implementation capability | Keyword-derived implementation classification for discovered operational flags, such as audit, observation, inventory, analysis, diagnostic, debug, or view. |
| `consumer_kind` | `projected_state_consumers` | implementation capability | Static grouping of surfaces as diagnostic, inquiry, inventory, runtime, observation, projection, or unknown. |
| `emits_diagnostic_facts` | `diagnostic_inventory` | implementation capability / boundary-adjacent output | Whether the diagnostic emits diagnostic facts. It describes output capability, while the recording boundary remains represented by `supports_record`, `record_scope`, and `writes_event_ledger`. |
| `emits_cluster_facts` | `diagnostic_inventory` | implementation capability / boundary-adjacent output | Whether the diagnostic emits cluster facts; all observed entries report `false`. |
| `reads_diagnostic_facts` | `diagnostic_inventory` | evidence source | Whether the diagnostic reads diagnostic fact output. This is an evidence-source trait even though it refers to diagnostic facts rather than projected state or files. |
| `evidence` | `operational_surface_inventory` | evidence source | The implementation basis for discovering the operational surface; observed value is `argparse`. |

## Comparison table

| Surface | Traits it exposes | Counts observed | What those traits characterize |
|---|---|---:|---|
| `projected_state_consumers` | source booleans, `boundary`, `consumer_kind` | 47 rows; projected state 20, repo files 23, static inventory 6, live observation 1, event ledger 2, runtime input 1 | Evidence-source consumption and a uniform read-only/no-record/no-mutation boundary for the inventory itself. |
| `diagnostic_inventory` | projected-state/file use, JSON/record support, record scope, emitted/read fact flags, event-ledger writes, mutation boundary | 47 rows; JSON support 42, record support 2, event-ledger writes 2, cluster mutation 0, diagnostic-fact reads 12 | Public diagnostic operational contract and diagnostic source/output behavior. |
| `question_surface_inventory` | bounded status, dispatch surface, required args, JSON support, answer responsibility and authority text | 17 rows; 11 eligible now, 2 eligible with parameters, 2 diagnostic only, 2 not dispatchable | Static question-family inventory plus bounded-dispatch participation. |
| `operational_surface_inventory` | category, registered, JSON-capable, evidence | 96 discovered surfaces; 46 registered, 41 JSON-capable | Argparse-discovered CLI visibility surface classification and registration coverage. |

## Recurring implementation concerns

### Evidence source

The evidence-source traits consistently describe where implementation information comes from:

- `uses_projected_state` and `uses_repo_files` are part of `DiagnosticInventoryEntry` and are copied directly into `ProjectedConsumerRow`.
- `uses_static_inventory`, `uses_live_observation`, `uses_event_ledger`, and `uses_runtime_input` are computed in `build_projected_state_consumers()` from fixed surface-name sets and rendered as `sources` by `format_projected_state_consumers()`.
- `reads_diagnostic_facts` in diagnostic inventory also describes an input source: diagnostic fact records.
- `evidence` in operational surface inventory reports the discovery basis; currently operational surfaces are discovered from argparse declarations.

### Operational boundary

Boundary traits consistently describe allowed behavior rather than information source:

- `projected_state_consumers` has a fixed `BOUNDARY` with `read_only=true` and `records`, `writes_event_ledger`, `mutates_cluster`, `executes_observation`, `provider_acquisition`, and `permission_creation` all `false`.
- `diagnostic_inventory` declares `supports_record`, `record_scope`, `writes_event_ledger`, and `mutates_cluster` per diagnostic surface.
- The observed diagnostic inventory has `mutates_cluster=false` for every entry, while only two surfaces support recording and write the event ledger.

### Dispatchability

Dispatch traits consistently describe bounded ask participation rather than diagnostic behavior:

- `BOUNDED_ASK_DISPATCH_SURFACES` maps question families to dispatch surfaces.
- `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` marks the parameterized cases.
- `bounded_status_for_question_family()` derives `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable` from those maps.
- `QuestionSurfaceInventoryRow` serializes `bounded_status`, `dispatch_surface`, and `required_surface_args` for visibility.

### Capability

Capability traits describe implementation support or classification rather than source, boundary, or dispatch:

- JSON support/capability appears as `supports_json`, `json_support`, and `json_capable` in different surface inventories.
- `registered` describes diagnostic-inventory registration coverage for argparse-discovered flags.
- `category` classifies operational CLI flags by implementation keyword rules.
- `consumer_kind` groups projected-state consumer rows by static surface sets.
- `emits_diagnostic_facts` and `emits_cluster_facts` describe output capability. They are boundary-adjacent, but the mutating/recording boundary is separately represented by `record_scope`, `writes_event_ledger`, and `mutates_cluster`.

## Implementation-backed inconsistencies

No recurring trait was observed serving multiple unrelated purposes across these surfaces. There are naming differences for similar JSON capability traits (`supports_json`, `json_support`, and `json_capable`), but each occurrence still describes JSON output support/capability for the surface that exposes it.

The only boundary-adjacent ambiguity is `supports_record`: it is both a capability flag and part of the operational recording boundary. Current implementation resolves that by pairing it with `record_scope` and `writes_event_ledger`, so it does not require a new concern category.

`emits_diagnostic_facts` and `emits_cluster_facts` describe output capability, not evidence source. They also help interpret operational consequences, but they do not themselves state mutation or ledger behavior; those are represented by separate boundary traits.

## Required question answers

1. The traits that describe evidence source are `uses_projected_state`, `uses_repo_files`, `uses_static_inventory`, `uses_live_observation`, `uses_event_ledger`, `uses_runtime_input`, `reads_diagnostic_facts`, and `evidence`. They consistently describe where implementation obtains or discovers information.
2. The traits that describe operational boundary are `read_only`, `records`, `supports_record`, `record_scope`, `writes_event_ledger`, `mutates_cluster`, `executes_observation`, `permission_creation`, and `provider_acquisition`. They consistently describe behavior limits rather than evidence.
3. The dispatchability traits are `bounded_status`, `dispatch_surface`, and `required_surface_args`. They consistently describe bounded ask eligibility and invocation requirements.
4. Recurring implementation-backed capability traits are `supports_json`, `json_support`, `json_capable`, `registered`, `category`, `consumer_kind`, `emits_diagnostic_facts`, and `emits_cluster_facts`.
5. No currently exposed recurring trait was observed serving multiple unrelated purposes. `supports_record` is both capability-like and boundary-relevant, but only in the single recurring concern of recording boundary.
6. The current surfaces collectively expose a coherent implementation vocabulary: source, boundary, dispatch, and capability traits recur across independent visibility surfaces.
7. Every currently exposed implementation trait observed in the four requested surfaces can be placed into evidence source, boundary, dispatch, or capability without inventing additional architectural concepts.

## Commands executed

```text
pwd && find .. -name AGENTS.md -print && git status --short
cat AGENTS.md && rg -n "projected_state_consumers|diagnostic_inventory|question_surface_inventory|operational_surface_inventory|uses_projected_state|bounded_status|permission_creation" .
python scripts/seed_local.py --projected-state-consumers --json > /tmp/psc.json
python scripts/seed_local.py --diagnostic-inventory --json > /tmp/di.json
python scripts/seed_local.py --question-surface-inventory --json > /tmp/qsi.json
python scripts/seed_local.py --operational-surface-inventory --json > /tmp/osi.json
python scripts/seed_local.py --operational-surface-inventory | head -80
sed -n '1,220p' seed_runtime/projected_state_consumers.py
sed -n '1,80p' seed_runtime/diagnostic_inventory.py
sed -n '1,130p' seed_runtime/question_surface_inventory.py
sed -n '1,260p' seed_runtime/operational_surface_inventory.py
python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_question_surface_inventory.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/projected_state_consumers.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/operational_surface_inventory.py`
- Seed JSON output from `/tmp/psc.json`, `/tmp/di.json`, `/tmp/qsi.json`, and `/tmp/osi.json`

## Files changed

- `docs/implementation_trait_characterization.md`

## LOC changed

- Added 159 lines.

## Tests run

```text
python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_question_surface_inventory.py
```

Result: passed.

## Conclusion

The current visibility surfaces already expose enough implementation-backed evidence to support a coherent implementation vocabulary for the currently recurring traits. Additional visibility is not required before concluding that the exposed traits fit the recurring concerns of evidence source, operational boundary, dispatchability, and implementation capability.
