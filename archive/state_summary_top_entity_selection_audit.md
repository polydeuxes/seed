# State Summary Top Entity Selection Audit

## Purpose

This audit examines how the default operator `top entities` section is selected and why Prometheus scrape-target endpoints dominate it.

It is a documentation-only implementation audit.

It does not change code, schemas, projections, observations, facts, tests, runtime behavior, or storage.

## Trigger

After filesystem and storage-topology details were removed from the default state summary, the summary became compact but still listed endpoint-shaped Prometheus scrape targets as the highest-ranked entities:

```text
192.168.254.116:9100 (aliases: 0 total; facts: 111)
192.168.254.202:9100 (aliases: 0 total; facts: 97)
192.0.2.200:9100 (aliases: 0 total; facts: 90)
```

The previous Prometheus endpoint audit identified that endpoint-scoped facts can dominate the default summary. This audit narrows the question to `state_summary()` top-entity selection.

## Central Finding

The default top-entities ranking is currently fact-volume driven.

`state_summary()` counts every projected fact by canonical subject and sorts entities by descending fact count. That means high-volume measurement subjects, especially Prometheus endpoint subjects, naturally dominate the default operator-facing top-entity section.

The relevant behavior is:

```python
for fact in state.facts.values():
    canonical = state.alias_resolver.canonical(fact.subject_id)
    entity_aliases[canonical].update(state.alias_resolver.resolve(fact.subject_id))
    entity_fact_counts[canonical] += 1
```

and:

```python
top_entities = [
    ...
    for canonical in sorted(
        entity_aliases, key=lambda name: (-entity_fact_counts[name], name)
    )[:top_entity_limit]
]
```

This means:

```text
fact volume
        ↓
ranking weight
        ↓
operator-visible top entity
```

That is the likely boundary violation.

## Boundary Finding

Fact volume is not operator relevance.

A subject with many current measurement facts is not necessarily the most meaningful default operator entity.

Prometheus endpoints are legitimate endpoint-scoped subjects, but they should not automatically dominate the default top-entity ranking merely because they carry many measurements.

The default summary should not imply:

```text
highest fact count
        ==
most important entity
```

## Evidence

### `state_summary()` Uses All Facts For Top-Entity Ranking

`seed_runtime/state_summary_views.py` builds `current_measurements` and `durable_facts` separately, but `top_entities` uses `state.facts.values()` as its source rather than durable facts or operator-relevant entity types.

This is important because Prometheus filesystem and scrape metrics are current measurements and can produce many facts per endpoint.

### Endpoint Subjects Are Preserved Correctly Upstream

The Prometheus source emits endpoint-scoped observations using the Prometheus `instance` label as the observation subject for endpoint role, `up`, and filesystem metrics. This is acceptable as an observation boundary.

The alias resolver also prevents endpoint-host alias collapse by refusing aliases that cross endpoint identity shape boundaries.

Therefore, the immediate default summary problem does not require changing Prometheus ingestion or endpoint preservation.

### The Summary Surface Converts Measurement Volume Into Prominence

The problem appears when the default operator summary turns raw fact count into top-entity prominence.

This is a presentation/ranking boundary issue first.

It may still reveal deeper identity or promotion work later, but the immediate observable leak is:

```text
endpoint-scoped measurements
        retained as endpoint facts
        counted as ordinary entity facts
        ranked above operator-meaningful entities
```

## What Is Correct

- Endpoint-scoped Prometheus observations should remain preserved.
- Endpoint facts should remain queryable by endpoint detail or scrape-target views.
- Endpoint-host alias boundaries should remain protected.
- Measurement facts should continue to contribute to measurement counts and explicit detail surfaces.

## What Is Incorrect Or Suspect

- Default `top_entities` treats all facts as equal ranking evidence.
- Measurement-heavy endpoint subjects dominate default operator summary.
- The top-entity label does not distinguish endpoints, hosts, services, or other entity types.
- The default operator summary communicates high-volume scrape targets as if they were the primary entities of interest.

## Candidate Fix Directions

The safest implementation fix should adjust top-entity selection, not Prometheus ingestion.

Candidate approaches:

1. Rank top entities using durable facts only.

   This removes high-volume current measurements from top-entity scoring while preserving measurement counts elsewhere.

2. Exclude endpoint-shaped subjects from default `top_entities`.

   This prevents scrape targets from appearing as default top entities unless explicitly requested.

3. Split endpoints into a separate explicit surface.

   For example:

   ```text
   scrape targets:
       up: N
       down: N
       unknown: N
   ```

   or a future endpoint detail view.

4. Include entity type and rank only operator-meaningful types.

   This likely requires stronger type projection and may be less surgical.

5. Combine durable-only ranking with endpoint exclusion.

   This is likely the safest short-term default-summary behavior.

## Recommended Surgical Implementation Direction

Start with a minimal default-summary fix:

```text
Top entities should not be ranked by measurement fact volume.
```

Prefer using durable facts for `entity_fact_counts` in the default `top_entities` ranking.

Also consider excluding endpoint-shaped subjects from default top entities if durable endpoint facts still dominate.

Do not change Prometheus ingestion as the first fix.

Do not alias endpoints to hosts to make the top-entity section look better.

Do not delete endpoint facts.

Do not hide endpoint state from explicit endpoint or availability surfaces.

## Tests To Add Or Update

Add tests for default state summary that prove:

- measurement-heavy endpoint subjects do not dominate `top_entities`;
- durable facts are used for top-entity ranking, if that implementation path is chosen;
- endpoint facts remain preserved and queryable;
- availability counts still work;
- measurement current sample count still includes measurements.

Possible test shape:

```text
Given:
    endpoint A has many measurement facts
    host B has fewer durable facts

Default top_entities should prefer host B over endpoint A,
or should exclude endpoint A from default top_entities,
depending on selected implementation.
```

## Non-Goals

This audit does not recommend changing Prometheus observation subjects.

This audit does not recommend collapsing endpoint identity into host identity.

This audit does not recommend removing measurement facts.

This audit does not recommend removing endpoint availability facts.

This audit does not define the final endpoint detail projection.

## Files Inspected

- `seed_runtime/state_summary_views.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/state.py`

## Invariants

- Fact volume is not operator relevance.
- Measurement volume should not dominate default entity prominence.
- Endpoint identity remains distinct from host identity.
- Endpoint-scoped facts should remain preserved for explicit endpoint views.
- Default top-entity ranking should reflect operator-relevant entity prominence, not raw metric cardinality.
- Presentation ranking must not perform identity promotion.

## Next Safe Move

Perform a surgical implementation patch to `state_summary()` top-entity construction.

Scope the patch to default summary ranking.

Do not modify Prometheus ingestion unless tests prove the ranking fix cannot satisfy the operator summary boundary.
