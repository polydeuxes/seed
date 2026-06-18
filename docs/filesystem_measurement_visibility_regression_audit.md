# Filesystem Measurement Visibility Regression Audit

## Purpose

This audit investigates a reported regression after the storage-topology projection work and the default top-entity ranking change.

It is a documentation-only implementation audit.

It does not change code, schemas, projections, observations, facts, tests, runtime behavior, or storage.

## Trigger

A runtime state summary reported high measurement preservation:

```text
measurement current samples: 910
```

But targeted current-fact queries returned no filesystem facts:

```bash
seed --current-facts 192.168.254.100:9100 filesystem_free_bytes
seed --current-facts 192.168.254.100:9100 filesystem_total_bytes
```

while availability remained visible:

```bash
seed --current-facts 192.168.254.100:9100 availability_status
```

The same runtime output showed default `top entities` collapsed from measurement-heavy endpoint counts such as:

```text
192.168.254.116:9100 (facts: 111)
```

to endpoint rows with durable-ranking counts such as:

```text
10.0.0.1:8080 (facts: 1)
```

## Scope

Files inspected:

- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`
- `scripts/seed_local.py`
- `predicate_catalog/core.json`
- PRs / commits corresponding to recent storage-topology and ranking work:
  - PR 336: cluster mount grouping projection
  - PR 337: shared storage candidate projection
  - PR 338: storage topology ambiguity projection
  - PR 343: durable-only top-entity ranking

The short SHA `3e35b14` from the handoff did not resolve through the GitHub connector on `polydeuxes/seed`. The matching repository authority for the described change is PR 343, merge commit `9ef6bd455b829477d9570f4e9cf2dd4dfbcd2bc4`, head commit `b5af462f7feed371669ac53689cdc5acbe821250`.

## Central Finding

The observed behavior is a combination of two separate implementation effects:

```text
state summary top_entities facts:X
        = durable ranking evidence
        != total entity facts
```

and:

```text
seed --current-facts SUBJECT filesystem_* without dimensions
        asks for one unambiguous current filesystem support
        but filesystem measurements are dimensioned by mount/device/fstype
        and filesystem predicates are cataloged as single-cardinality
        so multiple equally current dimension groups can produce no selected fact
```

Filesystem measurements still exist in projected state. The storage projections read them directly from `state.facts`, not through `--current-facts` rendering.

## Evidence Before Claim

### Observation: Measurement Count Remains High

`state_summary()` computes current measurements directly from projected facts:

```python
current_measurements = [
    fact
    for fact in state.facts.values()
    if is_measurement_predicate(fact.predicate) and not is_fact_expired(fact)
]
```

It then reports:

```python
"measurement_current_sample_count": len(current_measurements)
```

Interpretation: a high `measurement current samples` count means measurement facts remain in `state.facts` and are not expired. It does not depend on `--current-facts SUBJECT PREDICATE` query success.

Claim: `measurement current samples: 910` is not evidence of a rendering lie. It is evidence that current measurement facts remain projected.

### Observation: Storage Projection Reads Filesystem Measurements Directly

`_storage_projection()` filters `state.facts.values()` for non-expired measurement predicates, then selects only `filesystem_free_bytes` and `filesystem_total_bytes`. It groups by canonical subject, mountpoint, and full dimensions key:

```python
current_measurements = [
    fact
    for fact in state.facts.values()
    if is_measurement_predicate(fact.predicate) and not is_fact_expired(fact)
]

filesystems: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(dict)
for fact in current_measurements:
    if fact.predicate not in {"filesystem_free_bytes", "filesystem_total_bytes"}:
        continue
    mountpoint = fact.dimensions.get("mountpoint")
    if mountpoint is None:
        continue
    canonical = state.alias_resolver.canonical(fact.subject_id)
    dimensions_key = json.dumps(
        fact.dimensions, sort_keys=True, separators=(",", ":")
    )
    key = (canonical, mountpoint, dimensions_key)
```

Interpretation: filesystem projection does not require `get_current_facts()` to return a fact for a subject/predicate-only query. It reads retained measurement facts directly.

Claim: storage topology projections can remain correct even when `seed --current-facts SUBJECT filesystem_free_bytes` returns no facts.

### Observation: Measurement History Retention Preserves Dimensioned Series

`StateProjector.project()` applies `_retain_projected_measurement_history()` after alias construction and again after inferred facts. Measurement retention keys by projection subject, predicate, and dimensions:

```python
key = (
    subject_key(fact),
    fact.predicate,
    _dimensions_key(fact.dimensions),
)
```

Interpretation: each filesystem mount/device/fstype dimension group remains a separate measurement series.

Claim: there is no evidence in the inspected code that recent storage-topology projections delete filesystem facts.

### Observation: Filesystem Predicates Are Cataloged As Single Cardinality

`predicate_catalog/core.json` defines:

```json
{
  "predicate": "filesystem_free_bytes",
  "kind": "measurement",
  "value_type": "integer",
  "cardinality": "single"
},
{
  "predicate": "filesystem_total_bytes",
  "kind": "measurement",
  "value_type": "integer",
  "cardinality": "single"
}
```

Interpretation: `State.get_current_facts()` treats filesystem predicates as single-value current beliefs unless dimensions are supplied or the predicate is changed to multi-cardinality.

Claim: this is the proximate cause of subject/predicate-only `--current-facts` returning no filesystem rows when multiple dimension groups exist.

### Observation: `get_current_facts()` Falls Back To `get_best_fact()` For Non-Multi Predicates

`State.get_current_facts()` checks predicate cardinality:

```python
if not self.predicate_catalog.is_multi(predicate):
    best = self.get_best_fact(...)
    return [best] if best is not None else []
```

For filesystem predicates, `is_multi()` is false.

Interpretation: `--current-facts SUBJECT filesystem_free_bytes` does not enumerate all current filesystem rows. It asks for one best current fact.

Claim: the CLI help text says current-facts prints all projected Fact views, but the implementation returns only one best fact for single-cardinality predicates.

### Observation: Best Fact Selection Is Ambiguity-Sensitive

`get_best_fact()` calls `get_fact_support()`, and `get_fact_support()` calls `_select_unambiguous_best_support()`.

That selector returns `None` when multiple supports tie for the best support key:

```python
if len(top_supports) != 1:
    return None
```

Measurement support tie keys use latest observation time, confidence, and supporting-fact count:

```python
if support.predicate_semantics == "measurement":
    return (
        support.latest_observed_at,
        support.confidence,
        len(support.supporting_fact_ids),
    )
```

Interpretation: multiple filesystem mount rows for the same subject and predicate can produce multiple dimensioned supports. Without a dimensions filter, if those supports tie, the selector returns `None`.

Claim: `seed --current-facts SUBJECT filesystem_free_bytes` returning no facts is best explained as current-fact query ambiguity across dimensioned filesystem supports, not missing measurement data.

### Observation: Availability Is Single-Dimension And Remains Queryable

`availability_status` is also cataloged as a single-cardinality measurement, but it has no filesystem-style mount dimensions in the common Prometheus endpoint case.

Interpretation: a subject/predicate availability query normally has one support group and therefore remains unambiguous.

Claim: availability returning `up` while filesystem facts return none is consistent with the support-selection path.

### Observation: Top Entity Ranking Now Counts Durable Facts Only

Current `state_summary()` builds aliases from all facts, but increments `entity_fact_counts` only from `durable_facts`:

```python
for fact in state.facts.values():
    canonical = state.alias_resolver.canonical(fact.subject_id)
    entity_aliases[canonical].update(state.alias_resolver.resolve(fact.subject_id))
# Default top-entity prominence is based on durable facts only.
# Current measurement volume must remain queryable and counted elsewhere,
# but should not make scrape-target endpoints look operator-prominent.
for fact in durable_facts:
    canonical = state.alias_resolver.canonical(fact.subject_id)
    entity_fact_counts[canonical] += 1
```

The rendered `fact_count` field uses that same `entity_fact_counts` value:

```python
"fact_count": entity_fact_counts[canonical]
```

Interpretation: top-entity `facts: X` no longer means total facts for the entity. It means durable facts contributing to ranking prominence.

Claim: the `facts: 1` collapse is expected from PR 343, but the label is now semantically misleading.

## Direct Answers

### 1. Do filesystem facts still exist?

Yes, based on the inspected implementation path. `_storage_projection()` reads current filesystem measurements directly from `state.facts.values()` and the high measurement count confirms current measurement facts remain projected.

### 2. Do filesystem measurements still exist?

Yes. `measurement_current_sample_count` is derived from non-expired measurement facts in `state.facts`.

### 3. Why does `measurement current samples: 910` remain high?

Because it counts all non-expired measurement facts retained in projected state, independent of whether a subject/predicate-only `--current-facts` query can choose one unambiguous support.

### 4. Why does `seed --current-facts SUBJECT filesystem_free_bytes` return no facts?

Because filesystem predicates are cataloged as `single`, so `get_current_facts()` delegates to `get_best_fact()`. Without dimensions, multiple mount/device/fstype support groups may tie. `_select_unambiguous_best_support()` returns `None` on ties, so the CLI renders `no current facts`.

### 5. Why did top entities collapse to `facts: 1` for endpoints?

Because PR 343 changed top-entity ranking counts from all facts to durable facts only. Measurement facts still populate aliases and measurement counts, but no longer increment `top_entities[].fact_count`.

### 6. Is 3e35b14 behaving as intended?

The short SHA did not resolve in repository authority. The matching repository change, PR 343, is behaving as intended for ranking: measurement volume no longer drives top-entity prominence. However, it introduced or exposed a rendering-label ambiguity because `facts: X` now displays durable ranking evidence, not total entity facts.

### 7. Is displayed `facts: X` actually showing durable ranking evidence?

Yes. In current `state_summary()`, `top_entities[].fact_count` is populated from `entity_fact_counts`, and that counter is incremented only by `durable_facts`.

### 8. Which commit introduced the observed behavior?

For the top-entity `facts: X` collapse, repository authority points to PR 343, merge commit `9ef6bd455b829477d9570f4e9cf2dd4dfbcd2bc4`, titled `Rank state-summary top entities by durable facts (ignore measurement volume)`.

For the `--current-facts SUBJECT filesystem_*` no-facts behavior, the proximate implementation path is not PR 343. It comes from the combination of:

```text
filesystem predicates cataloged as single-cardinality
        +
get_current_facts() delegating non-multi predicates to get_best_fact()
        +
get_best_fact() requiring an unambiguous best support
        +
dimensioned filesystem measurements creating multiple support groups
```

The exact introducing commit for that path was not isolated in this audit, but it predates the durable-ranking PR because PR 343's own regression test uses `get_best_fact(..., dimensions={...})`, not subject/predicate-only `get_current_facts()`.

## Classification

```text
rendering regression: yes, for top_entities facts:X label semantics
projection regression: not shown
current-fact regression: yes/suspect, for dimensioned filesystem measurement visibility through subject/predicate-only CLI
measurement visibility regression: yes, on the CLI query surface only
entity ranking regression: no, PR 343 intentionally changed ranking semantics
subject association regression: not shown by inspected code
expected behavior from recent changes: yes, for durable-only top-entity counts
```

## Root Cause

Root cause 1:

```text
top_entities[].fact_count field name retained
        after value changed from total fact count
        to durable-only ranking evidence
```

Root cause 2:

```text
filesystem measurements are dimensioned multi-row measurements
        but filesystem_free_bytes/filesystem_total_bytes are cataloged as single-cardinality predicates
        and current-facts without dimensions requires one unambiguous best support
```

## Affected Surfaces

- `seed --state-summary` top entities: `facts: X` label now means durable ranking count.
- `seed --current-facts SUBJECT filesystem_free_bytes` without dimensions: can return no facts even when measurement facts exist.
- `seed --current-facts SUBJECT filesystem_total_bytes` without dimensions: same ambiguity risk.
- Operator interpretation of endpoint prominence: improved ranking, but label ambiguity can mislead audit/debug work.

## Unaffected Surfaces

- Measurement retention in projected `state.facts`.
- `measurement_current_sample_count`.
- Storage projection surfaces built from current measurement facts.
- Cluster mount grouping projection.
- Shared storage candidate projection.
- Storage topology ambiguity projection.
- Availability queries where one unambiguous support exists.
- Endpoint-host identity boundary.

## Smallest Safe Repair

Do not change ingestion.

Do not collapse endpoint subjects into hosts.

Do not delete or hide filesystem measurements.

Smallest repair A:

```text
Rename/render top entity facts field as durable facts or ranking facts.
```

For example:

```text
example_host (aliases: 0 total; durable facts: 3)
```

or:

```text
example_host (aliases: 0 total; ranking facts: 3)
```

Smallest repair B:

```text
Make current-facts dimension-aware for filesystem measurements.
```

Safe implementation options:

1. Mark `filesystem_free_bytes` and `filesystem_total_bytes` as `multi` in the predicate catalog if multiple current dimensioned values are allowed for one subject.
2. Add a filesystem-specific current-facts path that enumerates all current supports across dimensions when no dimensions filter is provided.
3. Add CLI flags for dimension filters and make subject/predicate-only ambiguity explicit instead of rendering `no current facts`.

The most direct semantic repair is option 1 if the intended meaning is:

```text
one current filesystem_free_bytes value per subject + mount/device/fstype dimensions
```

## Tests To Add Before Repair

Add regression coverage proving:

- a subject with two filesystem mountpoints returns both current filesystem facts from `state.get_current_facts(subject, "filesystem_free_bytes")`, or returns an explicit ambiguity message if enumeration is not desired;
- `--current-facts SUBJECT filesystem_free_bytes` does not print `no current facts` when current dimensioned filesystem facts exist;
- `--state-summary` top-entity rendering does not label durable ranking evidence as total facts;
- storage projections still use only measurement facts and do not promote ownership, identity, or topology truth.

## Non-Goals

This audit does not recommend changing Prometheus observation subjects.

This audit does not recommend collapsing endpoint identity into host identity.

This audit does not recommend promoting shared storage candidates to facts.

This audit does not recommend treating storage ambiguities as issues.

This audit does not implement fixes.

## Invariants

- Measurement is not ownership.
- Mount visibility is not storage identity.
- Candidate is not fact.
- Ambiguity is not truth.
- Ambiguity is not issue.
- Durable ranking evidence is not total fact count.
- Subject/predicate-only current-fact absence is not proof that dimensioned measurement facts are absent.
