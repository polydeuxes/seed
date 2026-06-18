# Graph Issue Orientation Audit

## Scope

This is an orientation-only audit. It does not fix graph issues, redesign graph issues, suppress graph issues, change graph issue generation, create projections, create views, create dashboards, or implement solutions.

The prompt-provided runtime count was:

```text
graph issues: 1839 warnings
graph issues: 0 errors
```

That count is not reproducible from this checkout alone because no persisted event ledger or state database containing those 1839 projected issues is present in the repository workspace. The default local projection in this checkout currently reports `0 warnings, 0 errors`.

This audit therefore records:

- the graph issue types the repository can construct;
- where issue construction occurs;
- what trigger conditions exist;
- which surfaces count or render graph issues;
- what data is still required to compute the exact 1839-warning distribution.

## Files inspected

- `seed_runtime/state.py`
  - `GraphValidationIssue` model
  - projection finalization
  - catalog relationship projection
  - `GraphValidator.validate`
  - `GraphValidator._check_side`
  - `GraphValidator._issue`
- `seed_runtime/facts.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `relationship_catalog/core.json`
- `entity_type_catalog/core.json`
- `tests/test_graph_validation.py`
- `tests/test_state_summary_views.py`
- `tests/test_seed_local_script.py`

Note: this checkout does not contain `seed_runtime/relationships.py`; relationship models and projection logic are in `seed_runtime/state.py`, and catalog loading is in `seed_runtime/relationship_catalog.py`.

## What produces graph issues

Graph issues are produced during state projection finalization.

The finalization order is:

1. catalog relationship projection;
2. entity type assertion projection;
3. graph issue construction via `GraphValidator(...).validate(state)`.

`GraphValidator.validate` iterates over `state.relationships`, skips relationships not found in the relationship catalog, skips identity relationships, and checks subject/object entity types against the relationship catalog definition.

If either side fails validation, the validator creates one `GraphValidationIssue` per unique:

```text
subject, relationship, object, severity, reason
```

Duplicate projected edges with the same key are collapsed into one issue while preserving all contributing relationship IDs and source fact IDs.

## Graph issue model

`GraphValidationIssue` contains:

- `id`
- `severity`
- `subject`
- `relationship`
- `object`
- `relationship_ids`
- `source_fact_ids`
- `reason`
- `hint`
- `expected_subject_types`
- `actual_subject_types`
- `expected_object_types`
- `actual_object_types`

## Graph issue construction surfaces

| Surface | Location | Role |
| --- | --- | --- |
| `GraphValidationIssue` | `seed_runtime/state.py` | Issue dataclass/model. |
| `StateProjector.project` finalization | `seed_runtime/state.py` | Calls graph issue construction. |
| `GraphValidator.validate` | `seed_runtime/state.py` | Iterates projected catalog relationships and aggregates issue instances. |
| `GraphValidator._check_side` | `seed_runtime/state.py` | Determines warning/error trigger conditions. |
| `GraphValidator._issue` | `seed_runtime/state.py` | Creates deterministic issue IDs and optional hints. |
| `build_operator_state_summary` | `seed_runtime/state_summary_views.py` | Counts graph issues, warnings, and errors. |
| `build_issue_view` | `seed_runtime/state_views.py` | Converts graph issues into issue views. |

## Trigger conditions

| Trigger family | Severity | Trigger condition |
| --- | --- | --- |
| Unknown expected catalog type | warning | The relationship catalog expects an entity type that is absent from the entity type catalog. |
| Unknown actual entity type | warning | The subject or object currently resolves to exactly `['unknown']`. |
| Ambiguous actual entity type | warning or error | The subject or object has multiple current types. If independent evidence proves one wrong type, this can become an error; otherwise it is a warning. |
| Wrong known actual entity type | error | The subject or object has one known type and it does not match the catalog expectation. |

Identity relationships do not produce graph issues because validation skips relationships whose catalog kind is `identity`.

## Relationship categories that can feed graph issues

| Relationship | Derived from predicate(s) | Subject expected | Object expected | Validation behavior |
| --- | --- | --- | --- | --- |
| `member_of` | `group` | `host` | `group` | Validated. |
| `alias_of` | `alias`, `hostname`, `ip_address`, `ansible_host` | `entity` | `entity` | Skipped because it is an identity relationship. |
| `monitored_by` | `prometheus_instance` | `host` | `monitoring_system` | Validated; unknown subject gets a dedicated hint. |
| `provides` | `provides`, `endpoint_role` | `entity` | `capability` | Subject bypasses validation because expected type is `entity`; object can validate. |
| `runs_on` | `host`, `runs_on` | `service` | `host` | Validated. |
| `depends_on` | `depends_on` | `document` | `document` | Validated; can warn because `document` is not in the inspected entity type catalog. |
| `related_to` | `related` | `document` | `document` | Validated; can warn because `document` is not in the inspected entity type catalog. |
| `belongs_to_domain` | `domain` | `document` | `domain` | Validated; can warn because `document` and `domain` are not in the inspected entity type catalog. |
| `defines` | `defines` | `document` | `concept` | Validated; can warn because `document` and `concept` are not in the inspected entity type catalog. |

## Graph Issues by Type

### Actual projected count in this checkout

| Type | Count | Severity |
| --- | ---: | --- |
| No graph issues in default projected state | 0 | n/a |

### Constructible issue categories discovered

| Type | Count in checkout default state | Severity |
| --- | ---: | --- |
| `{side} expects unknown catalog type {expected}` | 0 | warning |
| `{side} type is unknown; expected {expected}` | 0 | warning |
| `{side} type is ambiguous (...); expected {expected}` | 0 | warning |
| `{side} type is {actual}; expected {expected}` | 0 | error |

The exact distribution of the prompt-provided `1839 warnings` cannot be computed from this checkout because the underlying issue instances are absent.

## Issue type inventory

### Unknown expected catalog type

- **Issue Type:** `{side} expects unknown catalog type {expected}`
- **Count:** 0 in the default checkout projection; unknown for the external 1839-warning runtime set.
- **Severity:** warning
- **Construction location:** `GraphValidator._check_side`
- **Trigger condition:** relationship catalog references an expected entity type not present in the entity type catalog.
- **Example instance category:** `depends_on`, `related_to`, `belongs_to_domain`, and `defines` can trigger this when facts project those relationships and the expected types are absent from the entity type catalog.

### Unknown actual entity type

- **Issue Type:** `{side} type is unknown; expected {expected}`
- **Count:** 0 in the default checkout projection; unknown for the external 1839-warning runtime set.
- **Severity:** warning
- **Construction location:** `GraphValidator._check_side`
- **Trigger condition:** the actual subject or object type list is exactly `['unknown']`.
- **Example instances from tests:**
  - `mystery member_of servers`
  - `mystery monitored_by prometheus`
  - duplicate `example_host monitored_by prometheus` source facts collapse into one warning

### Ambiguous actual entity type

- **Issue Type:** `{side} type is ambiguous (...); expected {expected}`
- **Count:** 0 in the default checkout projection; unknown for the external 1839-warning runtime set.
- **Severity:** warning unless independent evidence proves a single wrong type.
- **Construction location:** `GraphValidator._check_side`
- **Trigger condition:** the actual subject or object has multiple current types and validation cannot reduce that ambiguity to a concrete wrong type.
- **Example instance category:** multi-typed entities participating in catalog relationships where the expected type is one of several possible current types.

### Wrong known actual entity type

- **Issue Type:** `{side} type is {actual}; expected {expected}`
- **Count:** 0 in the default checkout projection. The prompt states the external runtime set has 0 errors, so this category is not expected to contribute to the 1839 warning count.
- **Severity:** error
- **Construction location:** `GraphValidator._check_side`
- **Trigger condition:** the actual subject or object has one known type that does not match the catalog expected type.
- **Example instance from tests:** `workers runs_on node`, where `runs_on` expects a `service` subject but the subject has group evidence.

## Severity breakdown

### Default checkout projection

| Severity | Count |
| --- | ---: |
| warning | 0 |
| error | 0 |

### Prompt-provided runtime count

| Severity | Count |
| --- | ---: |
| warning | 1839 |
| error | 0 |

This prompt-provided count was not reproducible from repository data available in the workspace.

## Top 10 graph issue categories

### Default checkout projection

| Rank | Category | Count | Severity |
| ---: | --- | ---: | --- |
| 1 | No graph issues in default projected state | 0 | n/a |

### Prompt-provided 1839-warning set

Not computable from this checkout without the event ledger/state DB that produced those 1839 warnings.

## Percentage by category

### Default checkout projection

There are zero graph issues, so category percentages are not meaningful.

### Prompt-provided 1839-warning set

Not computable from this checkout without the issue instances.

## Concentration analysis

The code has a concentrated generator shape:

- one graph issue generator: `GraphValidator.validate`;
- four trigger families;
- a small finite relationship catalog;
- deduplication by subject, relationship, object, severity, and reason.

This means a large warning count is structurally more likely to be a few issue families repeated across many subjects/objects than many independent issue generators.

However, the exact concentration of the 1839-warning runtime set cannot be proven without the underlying projected `state.graph_issues` list.

## Ties to requested domains

| Domain | Tied to graph issues? | Orientation |
| --- | --- | --- |
| facts | Yes | Facts project catalog relationships, and graph issues preserve source fact IDs. |
| relationships | Yes | Graph validation iterates `state.relationships`. |
| aliases | Mostly no direct issue | `alias_of` is identity and identity relationships are skipped. |
| entity typing | Yes | Actual current entity types are compared to catalog expected types. |
| catalog projections | Yes | Catalog relationship projection feeds graph validation. |
| availability | Indirect/no direct issue found | `availability_status` is not a relationship-catalog predicate in the inspected catalog. |
| storage projections | No direct issue found | Inspected storage/filesystem predicates are not relationship-catalog predicates in the inspected catalog. |

## Categories that appear noisy

- Repeated unknown actual type warnings can become high-volume orientation noise when many projected relationships involve entities without inventory/type evidence.
- Repeated `monitored_by` warnings are partially de-noised by aggregation: duplicate source facts for the same subject/object/reason collapse into one issue.

## Categories that appear meaningful

- Unknown expected catalog type warnings appear meaningful because they indicate catalog vocabulary mismatch.
- Ambiguous type warnings appear meaningful because entity typing is unresolved.
- Wrong known type errors are meaningful because they indicate concrete type mismatch.
- Unknown actual type warnings are meaningful as missing type evidence, but may dominate volume when inventory evidence is sparse.

## What is actually producing the warnings

Within repository code, warnings are produced only by `GraphValidator._check_side` when:

1. a relationship catalog expected type is unknown to the entity type catalog;
2. a subject or object type is unknown;
3. a subject or object type is ambiguous and not independently proven wrong.

For the prompt-provided `1839 warnings`, the exact producer distribution cannot be determined from this checkout because the projected issue instances are not present.

## Data required to complete exact 1839-warning inventory

To compute the exact requested inventory, the audit needs the event ledger or persisted projection state that produced:

```text
graph issues: 1839 warnings, 0 errors
```

With that data, the deterministic grouping should be:

```text
severity, relationship, reason
```

and examples should be sampled directly from matching `GraphValidationIssue` objects.

## Files changed

- `docs/graph_issue_orientation_audit.md`

## LOC changed

Documentation-only addition.
