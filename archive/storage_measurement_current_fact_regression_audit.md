# Storage Measurement Current-Fact Regression Audit

## Status

Audit only. No implementation changes were made.

## Scope

This audit investigated the observed runtime behavior where the operator State Summary still reports a high measurement-current-sample count, while direct filesystem `--current-facts` queries for a subject/predicate return no facts, and top entities now render endpoint rows with `facts: 1`.

Inspected implementation surfaces:

- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`
- `scripts/seed_local.py`

Inspected recent implementation line:

- `9054e5cf3a4a5f2d37623c90ecd4e0bbc7affcec` / PR #336: cluster mount grouping projection
- `c0d04120a1141c0bf2d0baba686a444a12a8f789` / PR #337: shared storage candidate projection
- `93682ba231a699b70eca5cd12c6107a11be53b73` / PR #338: storage topology ambiguity projection
- `b5af462f7feed371669ac53689cdc5acbe821250` / PR #343: state-summary top-entity ranking by durable facts

The handoff short SHA `3e35b14` did not resolve in repository lookup during this audit. The matching repository-authoritative commit for "Fix state summary top entity ranking" is `b5af462f7feed371669ac53689cdc5acbe821250`.

## Finding

The observed behavior is a combination of:

1. expected top-entity ranking behavior from PR #343,
2. misleading State Summary rendering terminology for per-entity `facts: X`, and
3. a current-fact query visibility gap for dimensioned filesystem measurements.

It is not evidence that filesystem measurement facts were deleted by the storage topology projection commits.

## Trace

### Observation

`state_summary()` computes `current_measurements` directly from non-expired measurement predicates in `state.facts`.

### Interpretation

The `measurement current samples: 910` number means the projected state still contains 910 non-expired measurement facts.

### Evidence

`state_summary()` builds:

```python
current_measurements = [
    fact
    for fact in state.facts.values()
    if is_measurement_predicate(fact.predicate) and not is_fact_expired(fact)
]
```

and renders:

```python
"measurement_current_sample_count": len(current_measurements)
```

### Claim

A high `measurement current samples` count is direct evidence of measurement presence in projected state. It is not derived from entity ranking and is not derived from `--current-facts` CLI output.

---

### Observation

The explicit storage projection `_storage_projection(state)` reads filesystem measurements from `current_measurements`, filters for `filesystem_free_bytes` and `filesystem_total_bytes`, and requires a `mountpoint` dimension.

### Interpretation

Filesystem projection remains measurement-backed and projection-only. It does not promote ownership, storage identity, or topology facts.

### Evidence

The storage projection constructs filesystem rows only from measurement facts:

```python
for fact in current_measurements:
    if fact.predicate not in {"filesystem_free_bytes", "filesystem_total_bytes"}:
        continue
    mountpoint = fact.dimensions.get("mountpoint")
    if mountpoint is None:
        continue
```

### Claim

Filesystem measurements still exist when `measurement_current_sample_count` is high. If explicit storage projection is queried, filesystem rows can still be reconstructed from those current measurements when matching free/total samples and mountpoint dimensions are present.

---

### Observation

`State.get_current_facts(subject, predicate)` delegates through predicate-cardinality support selection. For predicates not treated as multi by the predicate catalog, it calls `get_best_fact(subject, predicate, dimensions=None)` and returns no rows if no unambiguous best support exists.

### Interpretation

A query like:

```bash
seed --current-facts 192.168.254.100:9100 filesystem_free_bytes
```

is an unqualified subject/predicate query. Filesystem measurements are dimensioned by mountpoint/device/fstype. Without dimensions, the direct current-facts surface can fail to choose a single current value even while dimensioned measurements exist.

### Evidence

`get_current_facts()` returns all supports only for predicates known as multi. Otherwise it asks for one best fact:

```python
if not self.predicate_catalog.is_multi(predicate):
    best = self.get_best_fact(...)
    return [best] if best is not None else []
```

The PR #343 regression test proves the dimension-qualified path works:

```python
state.get_best_fact(
    "192.168.254.116:9100",
    "filesystem_free_bytes",
    dimensions={...},
).value == 1000
```

### Claim

The current-facts symptom is a measurement visibility/query-shape issue, not a disappearance-of-facts issue. Existing tests prove dimension-qualified lookup, but they do not prove unqualified CLI `--current-facts SUBJECT filesystem_free_bytes` returns all dimensioned samples.

---

### Observation

PR #343 changed top-entity prominence to count only durable facts while still discovering aliases/entities from all facts.

### Interpretation

Endpoints with many filesystem measurement facts no longer rank highly from measurement volume. Endpoints with one durable endpoint fact can render with `facts: 1`.

### Evidence

The ranking change increments `entity_fact_counts` only from `durable_facts`:

```python
for fact in durable_facts:
    canonical = state.alias_resolver.canonical(fact.subject_id)
    entity_fact_counts[canonical] += 1
```

The same PR changed the CLI expectation from:

```text
host-up (aliases: 1 total; facts: 6)
```

to:

```text
host-up (aliases: 1 total; facts: 3)
```

### Claim

The top-entity collapse is expected behavior from PR #343. The regression is not the durable-only ranking itself. The regression is that the rendered field still says `facts: X`, even though `X` now means durable ranking evidence, not total projected facts for that entity.

## Direct answers

### 1. Do filesystem facts still exist?

Yes, when projected state reports measurement current samples and explicit storage projection can reconstruct filesystem rows from current measurement facts. The inspected storage projection commits preserve filesystem measurement facts and use them as projection input.

### 2. Do filesystem measurements still exist?

Yes. `measurement_current_sample_count` is computed directly from non-expired measurement facts in `state.facts`.

### 3. Why does `measurement current samples: 910` remain high?

Because the count is independent of top-entity ranking and direct current-facts rendering. It counts non-expired measurement facts present in projected state.

### 4. Why does `seed --current-facts SUBJECT filesystem_free_bytes` return no facts?

Because the CLI calls `State.get_current_facts(subject, predicate)` without dimensions. Dimensioned filesystem measurements can require dimensions, or a predicate-catalog/multi-value path, to be visible as multiple current samples. The inspected regression test proves dimension-qualified `get_best_fact()` works, not that unqualified `--current-facts` lists every dimensioned filesystem sample.

### 5. Why did top entities collapse to `facts: 1` for endpoints?

Because PR #343 changed top-entity ranking evidence to durable facts only. Measurement volume no longer contributes to endpoint prominence.

### 6. Is the ranking commit behaving as intended?

Yes for the ranking algorithm. It is behaving as intended by ranking with durable evidence instead of measurement volume.

No for operator terminology. The displayed `facts: X` label now communicates the wrong thing because it looks like total fact count but actually reflects durable ranking evidence.

### 7. Is displayed `facts: X` actually durable ranking evidence?

Yes. The current implementation stores durable ranking evidence under `top_entities[].fact_count`, and `format_state_summary()` renders it as `facts: X`.

### 8. Which commit introduced the observed behavior?

For top-entity collapse and `facts: X` changing meaning: `b5af462f7feed371669ac53689cdc5acbe821250` / PR #343.

For default State Summary no longer rendering storage/filesystem detail: PR #342 separated explicit `storage_state_projection(state)` from the default operator `state_summary(state)` surface.

For unqualified filesystem current-facts returning no rows: no inspected storage-topology commit introduced this directly. The behavior follows from existing current-fact query semantics plus dimensioned filesystem measurements. The smallest safe repair should add an explicit regression test before changing code.

## Root cause

The root cause is semantic surface drift:

- Top-entity ranking changed from total facts to durable ranking evidence.
- The output label remained `facts`.
- Direct current-facts lookup remains subject/predicate-oriented, while filesystem measurements are dimensioned measurement samples.

## Affected surfaces

- `state_summary().top_entities[].fact_count`
- `scripts/seed_local.py::format_state_summary()` rendering of `facts: X`
- `seed --current-facts SUBJECT filesystem_free_bytes` and `filesystem_total_bytes` when called without dimensions
- operator interpretation of endpoint prominence after PR #343

## Unaffected surfaces

- Measurement retention in `state.facts`
- `measurement_current_sample_count`
- Availability current fact lookup for endpoint-scoped `availability_status`
- Storage projection inputs
- Cluster mount groups
- Shared storage candidates
- Storage topology ambiguities
- Candidate/fact boundary
- Ambiguity/fact boundary
- Ownership/storage-identity boundaries

## Smallest safe repair

Do not revert durable-only ranking.

Recommended minimal repair:

1. Rename the top-entity summary field from `fact_count` to `durable_fact_count` or `ranking_fact_count`.
2. Render top entities as one of:

```text
ranking facts: X
```

or:

```text
durable facts: X
```

3. Add a regression test proving that an endpoint can have many measurement facts while the top-entity rendered label does not imply total facts.
4. Add a separate current-facts regression test for dimensioned filesystem measurements:
   - unqualified `--current-facts SUBJECT filesystem_free_bytes` behavior is documented and intentional, or
   - unqualified filesystem current-facts lists all current dimensioned samples.
5. If changing current-facts behavior, prefer a measurement-aware/multi-support listing path over special-casing filesystem predicates in CLI rendering.

## Non-goals

- No topology inference.
- No ownership inference.
- No shared-storage fact promotion.
- No ambiguity-to-issue promotion.
- No change to measurement retention.
- No change to Prometheus acquisition.
- No code changes in this audit.
