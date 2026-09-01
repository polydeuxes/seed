# Prometheus Endpoint Top Entity Boundary Audit

## Purpose

This audit examines why the default operator state summary is dominated by Prometheus scrape-target endpoint identifiers such as `192.168.254.116:9100`.

It is a documentation-only implementation audit.

It does not change code, schemas, projections, observations, facts, relationships, tests, runtime behavior, or storage.

## Trigger

After the default filesystem and storage-topology rendering leak was removed from state-summary output, the remaining default summary still showed endpoint-shaped subjects as top entities:

```text
192.168.254.116:9100 (aliases: 0 total; facts: 111)
192.168.254.202:9100 (aliases: 0 total; facts: 97)
192.0.2.200:9100 (aliases: 0 total; facts: 90)
```

This suggests a separate boundary issue from the storage-detail rendering leak.

## Central Finding

The current top-entities output appears to expose a Prometheus endpoint identity / promotion / ranking boundary issue.

The summary renderer is likely reporting the projected state faithfully. The upstream issue is that Prometheus scrape-target endpoint subjects accumulate many facts and therefore rank as the most significant entities.

The likely boundary chain is:

```text
Prometheus sample
        ↓
instance label
        ↓
endpoint subject
        ↓
facts attached to endpoint
        ↓
state_summary top_entities ranks by fact count
        ↓
endpoint identifiers dominate default operator summary
```

This is not the same class of issue as the previous storage leak.

The storage leak was a presentation-surface violation.

This issue is likely an identity/promotion/ranking boundary violation.

## Evidence

### Prometheus Emits Endpoint Subjects Directly

`PrometheusObservationSource._observations_from_query()` reads the Prometheus `instance` label and uses it as the observation subject for `up`, `endpoint_role`, `os`, `filesystem_avail_bytes`, and `filesystem_size_bytes` observations.

Examples from `seed_runtime/observation_sources.py`:

```python
instance = metric.get("instance")
...
self._observation(observed_at, instance, "endpoint_role", job.strip(), metadata)
self._observation(observed_at, instance, "up", _prometheus_int(sample_value), metadata)
...
self._observation(observed_at, instance, "filesystem_avail_bytes", ...)
self._observation(observed_at, instance, "filesystem_size_bytes", ...)
```

The code comments correctly note that non-`node_uname_info` metrics remain endpoint-scoped and do not participate in endpoint alias normalization. However, those endpoint-scoped observations still become subjects with many facts.

### Endpoint Alias Boundary Is Preserved

`AliasResolver` explicitly avoids aliasing endpoint and non-endpoint identities together.

```python
if _crosses_endpoint_identity_boundary(fact.subject_id, alias):
    continue
```

This is good. It prevents endpoint identity from being collapsed into host identity through alias resolution.

The remaining issue is not endpoint-host alias collapse. The issue is endpoint subjects becoming highly ranked default summary entities.

### State Summary Ranks By Fact Count

`state_summary()` builds `top_entities` from canonical subjects and fact counts across projected facts and known entities.

The relevant behavior is:

```text
for fact in state.facts.values():
    canonical = state.alias_resolver.canonical(fact.subject_id)
    entity_fact_counts[canonical] += 1
...
top_entities = sorted(entity_aliases, key=(-fact_count, name))[:limit]
```

Because endpoint-scoped Prometheus facts retain endpoint subjects, high-volume endpoint subjects naturally dominate top-entity ranking.

## Boundary Analysis

### What Is Correct

The Prometheus `instance` label is a valid observation subject for endpoint-scoped observations.

The code preserves endpoint-host alias separation.

Endpoint-scoped facts should remain queryable and explainable.

The default summary should not pretend endpoint measurements are host identity facts.

### What Is Wrong Or Suspect

The default operator summary currently treats high fact-count endpoint subjects as top entities without distinguishing endpoint-scoped measurement subjects from operator-meaningful entities.

This makes the default top-entities section communicate scrape targets as if they were the most important entities in the system.

That is misleading even if the underlying facts are preserved correctly.

## Likely Failure Class

This is likely not:

```text
endpoint identity collapsed into host identity
```

It is more likely:

```text
endpoint-scoped measurement subjects are allowed to dominate a default operator-facing entity ranking
```

That can happen even while endpoint-host alias boundaries are preserved.

## Architecture Boundary

Prometheus `instance` should be interpreted as a scrape-target endpoint identifier unless stronger host identity evidence is available.

Default state summary should distinguish:

```text
operator-meaningful entity
        !=
Prometheus scrape target endpoint
```

and:

```text
fact volume
        !=
operator relevance
```

Top-entity ranking should not simply reward high-volume measurement endpoints.

## Questions For Follow-Up Implementation Audit

1. Should default `top_entities` exclude endpoint-shaped subjects by default?

2. Should endpoint-shaped subjects appear in a separate `top endpoints` or `scrape targets` section instead?

3. Should `top_entities` rank durable/non-measurement facts only?

4. Should endpoint-scoped measurement facts count toward endpoint detail views but not default entity ranking?

5. Should host entities be promoted only from stronger identity observations such as inventory, local host identity, or `node_uname_info` with stable nodename metadata?

6. Should the state summary expose entity type when ranking entities so endpoints are visible as endpoints rather than implied hosts?

## Candidate Fix Directions

The safest implementation direction is likely presentation-side first:

```text
Default top_entities should not be dominated by endpoint-scoped measurement subjects.
```

Possible surgical fixes:

- rank top entities using durable facts only;
- exclude endpoint-shaped subjects from default `top_entities`;
- split endpoint-shaped subjects into an explicit endpoint/scrape-target section;
- include entity type and suppress endpoint types from the default operator entity ranking;
- preserve exact endpoint facts for explicit endpoint detail views.

Avoid fixes that:

- alias endpoints to hosts without stronger identity evidence;
- delete endpoint-scoped facts;
- promote scrape targets into hosts;
- hide provenance;
- treat fact count as operator relevance.

## Recommended Next Step

Perform a surgical implementation audit of `state_summary()` top-entity construction.

Focus on whether default top entities should use:

```text
durable facts only
```

or:

```text
non-endpoint subjects only
```

or a combination of both.

Do not change Prometheus observation preservation before deciding the state-summary contract.

## Files Inspected

- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`

## Non-Goals

This audit does not recommend deleting endpoint facts.

This audit does not recommend aliasing endpoint subjects to host subjects.

This audit does not recommend changing Prometheus ingestion semantics as an immediate fix.

This audit does not define a full endpoint detail projection.

## Invariants

- Prometheus instance labels are endpoint identifiers unless stronger evidence supports another interpretation.
- Endpoint identity must remain distinct from host identity.
- Fact volume is not operator relevance.
- Default top-entity summaries should not be dominated by endpoint-scoped measurement subjects.
- Endpoint facts should remain available for explicit endpoint or scrape-target detail views.
- Presentation ranking should not perform identity promotion.
