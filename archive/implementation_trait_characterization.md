# Implementation Trait Characterization

## Implementation summary

`seed --implementation-trait-characterization` now preserves a distinction that is visible in the implementation-backed inventories:

- **Implementation traits** are recurring behavior/capability/source/dispatch fields that the implementation maps to an existing concern category.
- **Inventory metadata** are row identifiers, CLI labels, examples, notes, descriptions, and human-readable inventory explanations.
- **Grouping/container fields** hold trait-bearing subfields but are not themselves the trait being characterized.

The command still reports non-trait exposed fields, but it reports them under `non_trait_items` / `Exposed Non-Trait Fields` instead of classifying them as unclassified implementation traits.

No concern category was added. The existing concern categories remain:

1. `evidence_source`
2. `operational_boundary`
3. `dispatchability`
4. `implementation_capability`
5. `unclassified` for exposed fields that are not yet distinguished by implementation evidence

After this refinement, the current implementation-backed output has no remaining unclassified implementation traits.

## Implementation-backed qualification rule

A currently exposed value qualifies as an implementation trait when implementation evidence shows that it declares behavior, capability, source consumption, or dispatch participation for an exposed surface and the characterization registry maps it to one of the existing concern categories.

The implementation evidence used for this distinction is:

- `DiagnosticInventoryEntry` contains operational contract fields such as `uses_projected_state`, `uses_repo_files`, `supports_json`, `supports_record`, `record_scope`, `emits_diagnostic_facts`, `emits_cluster_facts`, `writes_event_ledger`, `mutates_cluster`, and `reads_diagnostic_facts`.
- `ProjectedConsumerRow` contains source-consumption traits and a `boundary` container; the container expands into recurring operational-boundary fields from `BOUNDARY`.
- `QuestionSurfaceInventoryRow` contains bounded-dispatch fields such as `bounded_status`, `dispatch_surface`, `required_surface_args`, and `json_support` alongside metadata such as examples, notes, and responsibility text.
- `OperationalSurface` contains argparse-discovered capability/classification fields such as `category`, `registered`, `json_capable`, and `evidence`.

## Currently characterized implementation traits

| Trait | Concern | Implementation-backed meaning |
|---|---|---|
| `uses_projected_state` | `evidence_source` | Declares whether a surface consumes projected state. |
| `uses_repo_files` | `evidence_source` | Declares whether a surface reads repository files or repository inventory evidence. |
| `uses_static_inventory` | `evidence_source` | Declares whether a surface consumes static registry or inventory row data. |
| `uses_live_observation` | `evidence_source` | Declares whether a surface depends on existing live observation collection evidence. |
| `uses_event_ledger` | `evidence_source` | Declares whether a surface depends on event-ledger evidence. |
| `uses_runtime_input` | `evidence_source` | Declares whether a surface depends on runtime inquiry input. |
| `reads_diagnostic_facts` | `evidence_source` | Declares whether a surface reads diagnostic facts. |
| `evidence` | `evidence_source` | Names the implementation evidence source for a discovered operational surface. |
| `read_only` | `operational_boundary` | Declares a no-mutation operational boundary. |
| `records` | `operational_boundary` | Declares whether the visibility surface records facts during this run. |
| `supports_record` | `operational_boundary` | Declares whether a surface has a record-capable mode. |
| `record_scope` | `operational_boundary` | Declares the subject scope used when recording is supported. |
| `writes_event_ledger` | `operational_boundary` | Declares whether a surface appends to the event ledger. |
| `mutates_cluster` | `operational_boundary` | Declares whether a surface mutates cluster truth/state. |
| `executes_observation` | `operational_boundary` | Declares whether a surface executes observation collection. |
| `permission_creation` | `operational_boundary` | Declares whether a surface creates permission state. |
| `provider_acquisition` | `operational_boundary` | Declares whether a surface acquires or invokes providers. |
| `bounded_status` | `dispatchability` | Declares bounded ask dispatch eligibility for a question family. |
| `dispatch_surface` | `dispatchability` | Declares the implementation dispatch surface for bounded ask. |
| `required_surface_args` | `dispatchability` | Declares required arguments for dispatchable bounded surfaces. |
| `supports_json` | `implementation_capability` | Declares whether a diagnostic surface supports JSON output. |
| `json_support` | `implementation_capability` | Declares whether a question surface supports JSON output. |
| `json_capable` | `implementation_capability` | Declares whether an operational CLI surface has JSON-capable visibility. |
| `registered` | `implementation_capability` | Declares whether a discovered operational surface is registered in diagnostic inventory. |
| `category` | `implementation_capability` | Declares the discovered operational surface category. |
| `consumer_kind` | `implementation_capability` | Declares the implementation-backed consumer kind. |
| `emits_diagnostic_facts` | `implementation_capability` | Declares whether a surface emits diagnostic facts. |
| `emits_cluster_facts` | `implementation_capability` | Declares whether a surface emits cluster facts. |

The requested validation examples remain classified: `uses_projected_state`, `writes_event_ledger`, `dispatch_surface`, and `supports_json` all remain in the trait item output.

## Inventory metadata

The following exposed fields are now reported as inventory metadata rather than implementation traits:

| Field | Evidence-backed reason |
|---|---|
| `name` | Inventory row identifier. |
| `surface` | Inventory row or answering surface identifier. |
| `cli_flags` | CLI exposure metadata for invoking the inventory row surface. |
| `surface_flag` | CLI exposure metadata for the answering surface. |
| `description` | Human-readable diagnostic inventory description. |
| `question_family` | Inventory row identifier for the question family. |
| `example_questions` | Human-readable inventory examples. |
| `answer_responsibility` | Human-readable inventory responsibility description. |
| `authority_boundary` | Human-readable authority description for the inventory row. |
| `notes` | Human-readable inventory/evidence notes. |
| `human_formatter` | Formatter metadata for the answering surface. |
| `implementation_reason` | Human-readable implementation explanation for the inventory row. |

These fields remain visible in `non_trait_items`; they are not silently discarded.

## Grouping/container fields

`boundary` is now reported as a grouping/container field. The implementation evidence is `ProjectedConsumerRow.boundary`, which contains the recurring operational-boundary fields declared in `BOUNDARY`: `read_only`, `records`, `writes_event_ledger`, `mutates_cluster`, `executes_observation`, `provider_acquisition`, and `permission_creation`.

The container remains visible in `non_trait_items`, while the contained boundary traits remain characterized as implementation traits.

## Before/after output examples

Before this change, metadata and containers appeared as unclassified traits. Example from the previous JSON output:

```json
{
  "concern_counts": {
    "dispatchability": 3,
    "evidence_source": 8,
    "implementation_capability": 8,
    "operational_boundary": 9,
    "unclassified": 13
  }
}
```

After this change:

```json
{
  "concern_counts": {
    "dispatchability": 3,
    "evidence_source": 8,
    "implementation_capability": 8,
    "operational_boundary": 9
  },
  "non_trait_counts": {
    "container_field": 1,
    "inventory_metadata": 12
  }
}
```

Before this change, entries such as `answer_responsibility`, `authority_boundary`, `boundary`, `cli_flags`, and `description` were emitted in `items` with `concern: unclassified`. After this change, those fields are absent from trait `items` and present in `non_trait_items` with either `inventory_metadata` or `container_field` classification.

## Remaining unclassified implementation traits

None in the current implementation-backed output.

This conclusion comes from the current JSON output: `concern_counts` contains no `unclassified` count, and a direct check of `items` where `concern == "unclassified"` returns an empty list.

## Files changed

- `seed_runtime/implementation_trait_characterization.py`
- `tests/test_implementation_trait_characterization.py`
- `docs/implementation_trait_characterization.md`

## Tests added or updated

Updated `tests/test_implementation_trait_characterization.py` to prove:

- metadata examples (`answer_responsibility`, `authority_boundary`, `cli_flags`, and `description`) are not emitted as implementation traits;
- metadata examples are preserved as `inventory_metadata` non-trait fields;
- `boundary` is preserved as a `container_field` non-trait field;
- the JSON output has no unclassified entries for the observed metadata/container examples;
- existing required implementation traits remain classified.

## Commands executed

```text
python scripts/seed_local.py --implementation-trait-characterization --json
python -m pytest -q tests/test_implementation_trait_characterization.py
python -m black seed_runtime/implementation_trait_characterization.py tests/test_implementation_trait_characterization.py
python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_implementation_trait_characterization.py
```

## LOC changed

At the time of this update, `git diff --stat` reports:

```text
 docs/implementation_trait_characterization.md      | 284 +++++++++++----------
 seed_runtime/implementation_trait_characterization.py | 155 ++++++++++-
 tests/test_implementation_trait_characterization.py  |  64 ++++-
 3 files changed, 351 insertions(+), 152 deletions(-)
```
