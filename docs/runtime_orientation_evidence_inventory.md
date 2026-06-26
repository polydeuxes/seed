# Runtime Orientation Evidence Inventory

This implementation investigation audits existing repository evidence for a bounded read-only runtime-orientation surface. It does not implement `seed --runtime-orientation`, design runtime behavior, introduce runtime state, reconcile documents, or infer values that current implementation does not preserve.

## Implementation summary

Current implementation preserves a strong static surface registry and relationship inventory, but it does not preserve a live execution context object that identifies the currently executing work. The implementation-backed evidence is therefore sufficient for a bounded read-only view over registered surfaces and their declared relationships, but not sufficient to truthfully report live fields such as current owner, current mode, active runtime input, or runtime context.

The implementation evidence used here came from:

- `python scripts/seed_local.py --question-surface-inventory --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
- `python scripts/seed_local.py --projected-state-consumers --json`
- `python scripts/seed_local.py --implementation-trait-characterization --json`
- `python scripts/seed_local.py --operational-surface-inventory --json`
- CLI dispatch code for bounded `ask --question-family`.
- Existing inquiry-orientation implementation and tests.

Observed inventory sizes from those commands:

| Evidence source | Rows / surfaces observed | Relevant implementation-backed meaning |
| --- | ---: | --- |
| Question Surface Inventory | 17 rows | Question-family registrations, answering surface metadata, bounded status, dispatch surface, diagnostic relationships, answer responsibility, authority boundary. |
| Diagnostic Inventory | 48 rows | Diagnostic surface declarations, CLI flags, evidence-source booleans, record/ledger/mutation boundaries, descriptions. |
| Diagnostic Shape Audit | 432 rows | Static audit comparing declared diagnostic behavior shape with observed implementation shape; all observed rows were `consistent`. |
| Projected State Consumers | 48 rows | Surface source-consumer characterization and read-only boundary metadata built from diagnostic inventory plus static classification sets. |
| Implementation Trait Characterization | 32 trait items and non-trait metadata items | Characterizes recurring fields as evidence-source, operational-boundary, dispatchability, or implementation-capability traits; leaves some inventory relationship names unclassified. |
| Operational Surface Inventory | 96 surfaces | Argparse-discovered operational surface flags with categories, registration state, JSON capability, and argparse evidence. |

## Supported runtime-orientation fields

Supported means the implementation already preserves the field as registered/static surface evidence. It does not mean the implementation can determine the field for currently executing work.

| Candidate field | Support status | Implementation-backed evidence |
| --- | --- | --- |
| `current_surface` | Partially supported as registered `surface`, not as current execution state. | Question Surface Inventory rows preserve `surface`; Operational Surface Inventory preserves discovered CLI flag names. No live current-surface state was found. |
| `current_question_family` | Partially supported as registered `question_family`, not as current execution state. | Question Surface Inventory rows preserve exact `question_family` values; bounded ask dispatch validates an operator-provided family against inventory families. |
| `dispatch_surface` | Supported for Question Surface Inventory rows. | Question Surface Inventory enrichment fills `dispatch_surface` from bounded ask mappings. |
| `canonical_diagnostic_surface` | Supported for Question Surface Inventory rows. | Question Surface Inventory enrichment computes canonical diagnostic aliases for declared/dispatch surfaces. |
| `diagnostic_inventory_name` | Supported for Question Surface Inventory rows when a canonical surface exists in Diagnostic Inventory. | Enrichment checks canonical surface names against Diagnostic Inventory names. |
| `diagnostic_shape_spec_name` | Supported for Question Surface Inventory rows when a canonical surface exists in Diagnostic Shape Audit specs. | Enrichment checks canonical surface names against implementation shape specs. |
| `implementation_responsibility` | Supported only as static `answer_responsibility` metadata for Question Surface Inventory rows. | The registry preserves human-readable responsibility text per question-family row. It does not preserve responsibility for currently executing work. |
| `evidence_source` | Supported as surface characteristics, not as current inquiry evidence source. | Diagnostic Inventory exposes booleans such as `uses_projected_state`, `uses_repo_files`, and `reads_diagnostic_facts`; Projected State Consumers adds `uses_static_inventory`, `uses_live_observation`, `uses_event_ledger`, and `uses_runtime_input`; Implementation Trait Characterization classifies these as `evidence_source`. |
| `operational_boundary` | Supported as surface metadata, not as current execution boundary state. | Diagnostic Inventory preserves record, ledger, and mutation fields; Projected State Consumers preserves read-only boundary fields; Implementation Trait Characterization classifies those as `operational_boundary`. |
| `relationship_status` | Supported for Question Surface Inventory rows. | Question Surface Inventory enrichment marks rows as `connected`, `missing_diagnostic_inventory`, `missing_diagnostic_shape_spec`, or `not_dispatchable` depending on registry/spec relationships. |

## Unsupported runtime-orientation fields

Unsupported means current implementation evidence does not preserve a truthful value for the field, and this investigation does not infer one.

| Candidate field | Why unsupported by current implementation evidence |
| --- | --- |
| `current_mode` | No preserved runtime-mode field or live execution context was found. Existing categories such as `consumer_kind` and operational surface `category` classify registered surfaces, not live mode during execution. |
| `current_owner` | No owner field, owner registry, active-work owner binding, session owner binding, or runtime-work ownership record was found in the inspected implementation evidence. |
| `active_runtime_input` | Inquiry notes preserve raw note text for `--record-inquiry-note`, and bounded ask consumes operator-provided question families/surface args, but no general active runtime input field is preserved for executing work. |
| `runtime_context` | No runtime context object was found that ties together current surface, current question family, current owner, active input, mode, evidence source, and operational boundary during execution. |

## Implementation-backed evidence table

| Question | Answer from implementation evidence |
| --- | --- |
| 1. Which candidate fields are already implementation-backed? | Registered/static support exists for `current_surface` as `surface`, `current_question_family` as `question_family`, `dispatch_surface`, `canonical_diagnostic_surface`, `diagnostic_inventory_name`, `diagnostic_shape_spec_name`, static `implementation_responsibility` via `answer_responsibility`, surface-level `evidence_source`, surface-level `operational_boundary`, and `relationship_status`. |
| 2. Which candidate fields are not currently implementation-backed? | Live `current_mode`, `current_owner`, general `active_runtime_input`, and integrated `runtime_context` are unsupported. Live/current interpretations of `current_surface`, `current_question_family`, `implementation_responsibility`, `evidence_source`, and `operational_boundary` are also unsupported. |
| 3. Can current implementation determine current surface during execution? | No. It exposes registered implementation surfaces. Question Surface Inventory preserves `surface`; Operational Surface Inventory discovers argparse flags; bounded ask sets the target argparse destination after an exact family is supplied. None of these preserve a live current-surface record for arbitrary execution. |
| 4. Can current implementation determine current Question Family during execution? | No general runtime determination exists. It exposes static Question Family registrations and bounded ask validates an explicit `--question-family` value against those registrations. It does not classify free-form runtime work into a current family. |
| 5. Can current implementation determine implementation responsibility for currently executing work? | No. It preserves static `answer_responsibility` metadata for inventory rows. That metadata is not bound to a live current work item unless the caller explicitly selects a registered row. |
| 6. Can current implementation determine current evidence source for an executing inquiry? | No. It exposes evidence-source characteristics for registered surfaces. Diagnostic Inventory and Projected State Consumers declare which evidence classes a surface consumes, but there is no current inquiry execution record selecting one or more actual evidence sources. |
| 7. Can current implementation determine current operational boundary for an executing inquiry? | No. It exposes boundary metadata associated with registered surfaces. Diagnostic Inventory and Projected State Consumers preserve read/record/ledger/mutation boundaries, but no live inquiry boundary context is preserved. |
| 8. Can current implementation determine current owner of runtime work? | No. Missing evidence: an owner field in inventories, a runtime-work record, an owner/session/work binding, and any current execution context that records ownership. Do not infer ownership from surface names, categories, or responsibility metadata. |
| 9. Can current implementation determine current runtime mode? | No. Supported implementation-backed classifications include static operational surface categories (`audit`, `observation`, `view`, `inventory`, `analysis`, `diagnostic`, `debug`) and projected consumer kinds (`diagnostic`, `inventory`, `inquiry`, `observation`, `projection`). These are not live runtime modes such as `request_response`, `diagnostic_surface`, `observation_collection`, or `projection_build`. No candidate runtime-mode value is preserved as current. |
| 10. What is the smallest truthful runtime-orientation view the repository could currently expose using only existing evidence? | A read-only registered-surface orientation view could truthfully expose: selected/registered surface name; Question Family when the selected surface has a Question Surface Inventory row; dispatch surface; canonical diagnostic surface; diagnostic inventory name; diagnostic shape spec name; static answer responsibility; static evidence-source traits; static operational-boundary traits; relationship status; CLI flag/category/registration/JSON capability when available. It could not truthfully expose current owner, current runtime mode, active runtime input, or an integrated runtime context. |

## Implementation-backed gaps

The repository does not currently preserve these facts as implementation-backed runtime evidence:

- A live current-surface record for the command being executed.
- A live current Question Family classification for the command being executed.
- A runtime-work owner or owner-binding field.
- A runtime-mode field with values such as `request_response`, `diagnostic_surface`, `observation_collection`, `projection_build`, or `unknown`.
- A general active-runtime-input record.
- A runtime context object that binds current surface, family, input, owner, mode, evidence source, and operational boundary.
- A current evidence-source selection for an executing inquiry.
- A current operational-boundary selection for an executing inquiry.

## Files inspected

Implementation files inspected:

- `scripts/seed_local.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projected_state_consumers.py`
- `seed_runtime/implementation_trait_characterization.py`
- `seed_runtime/operational_surface_inventory.py`
- `seed_runtime/inquiry_orientation.py`

Test files inspected:

- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- `tests/test_projected_state_consumers.py`
- `tests/test_implementation_trait_characterization.py`
- `tests/test_operational_surface_inventory.py`
- `tests/test_inquiry_orientation.py`

Prior observation document inspected as supporting context, not authority over implementation:

- `docs/inquiry_surface_classes_observation.md`

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules' && git status --short`
- `cat AGENTS.md && rg -n "Question Surface Inventory|diagnostic-inventory|diagnostic-shape-audit|Projected State Consumers|Implementation Trait|Operational Surface|question-family|inquiry|orientation|responsibility|evidence_source|operational_boundary" -S .`
- `python scripts/seed_local.py --question-surface-inventory --json > /tmp/qsi.json`
- `python scripts/seed_local.py --diagnostic-inventory --json > /tmp/di.json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json > /tmp/dsa.json`
- `python scripts/seed_local.py --projected-state-consumers --json > /tmp/psc.json`
- `python scripts/seed_local.py --implementation-trait-characterization --json > /tmp/itc.json`
- `python scripts/seed_local.py --operational-surface-inventory --json > /tmp/osi.json`
- `python` JSON inspection snippets over `/tmp/qsi.json`, `/tmp/di.json`, `/tmp/dsa.json`, `/tmp/psc.json`, `/tmp/itc.json`, and `/tmp/osi.json`
- `rg -n "QUESTION_SURFACE|QuestionSurface|DIAGNOSTIC_INVENTORY|DiagnosticInventory|SHAPE|IMPLEMENTATION_TRAIT|projected_state_consumers|BOUND_ASK|_QUESTION_FAMILY|inquiry_orientation|record_inquiry_note|def _handle_bounded_ask" seed_runtime scripts/seed_local.py tests/test_inquiry_orientation.py tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`
- `sed` inspections of the implementation files listed above
- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_projected_state_consumers.py tests/test_implementation_trait_characterization.py tests/test_operational_surface_inventory.py tests/test_inquiry_orientation.py`

## Files changed

- `docs/runtime_orientation_evidence_inventory.md`

## LOC changed

- Added 143 lines in `docs/runtime_orientation_evidence_inventory.md`.

## Tests run

- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_projected_state_consumers.py tests/test_implementation_trait_characterization.py tests/test_operational_surface_inventory.py tests/test_inquiry_orientation.py`

## Conclusion

The repository currently preserves sufficient implementation-backed evidence for a first bounded read-only registered-surface orientation view, but not for a live runtime-orientation view that claims current owner, current runtime mode, active runtime input, or integrated runtime context. Any truthful first surface would need to remain bounded to existing registered implementation evidence rather than live execution state.
