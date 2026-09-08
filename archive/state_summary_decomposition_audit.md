# State Summary Decomposition Audit

## Scope

This audit classifies the currently rendered State Summary output by repository authority. It does not propose destinations, new commands, dashboards, HomeOps surfaces, Lens frameworks, View frameworks, or implementation changes.

## Files inspected

- `seed_runtime/state_summary_views.py`
- `scripts/seed_local.py`
- `tests/test_state_summary_views.py`
- `tests/test_seed_local_script.py`
- `docs/state_summary_scope_review.md`

## Rendered sections discovered

The CLI `--state-build` path renders two State Summary-related layers together:

1. Compact `StateSummary`, rendered by `format_state_view_summary(...)`.
2. Operator State Summary, rendered by `format_state_summary(...)`.

### Compact State Summary sections

- Facts
- Observations
- Requirements
- Capabilities
- Issues
- Projection Version
- Last Event

### Operator State Summary sections

- entities
- facts
- optional relationships
- durable facts
- measurement current samples
- conflicts
- stale facts
- graph issues
- observation sources
- top entities by kind
  - hosts
  - services
  - endpoints
  - storage
- legacy top entities fallback
- availability by scope
  - endpoint_scrape_availability
  - host_availability
  - service_availability
- legacy availability fallback

## Section classification

| Section | Purpose | KEEP / MOVE / UNCERTAIN | Evidence |
| ------- | ------- | ----------------------- | -------- |
| Compact `State Summary` heading | Names the compact projected world-model summary. | KEEP | `format_state_view_summary(...)` renders the compact heading, and `docs/state_summary_scope_review.md` identifies compact `StateSummary` as the closest existing narrow summary of projected State itself. |
| Compact `Facts` | State cardinality: total facts in the compact State View summary. | KEEP | Rendered from `summary.facts_count`; the scope review lists fact count as closest to projected-State description. |
| Compact `Observations` | Observation cardinality in the projected State View. | KEEP | Rendered from `summary.observations_count`; the scope review lists observation count in compact `StateSummary` as State-itself accounting. |
| Compact `Requirements` | Requirement cardinality in the projected State View. | KEEP | Rendered from `summary.requirements_count`; the scope review lists requirement count in compact `StateSummary` as State-itself accounting. |
| Compact `Capabilities` | Capability cardinality in the projected State View. | KEEP | Rendered from `summary.capabilities_count`; the scope review lists capability count in compact `StateSummary` as State-itself accounting. |
| Compact `Issues` | Issue cardinality in the projected State View. | KEEP | Rendered from `summary.issues_count`; the scope review lists issue count in compact `StateSummary` as State-itself accounting. |
| Compact `Projection Version` | Projection identity and boundary metadata. | KEEP | Rendered from `summary.projection_version`; the scope review lists projection identity as State Summary responsibility. |
| Compact `Last Event` | Projection identity and boundary metadata showing the last event included. | KEEP | Rendered from `summary.last_event_id`; the scope review lists projection identity as State Summary responsibility. |
| Operator `State summary` heading | Names the richer operator summary rendered after compact State Summary. | KEEP | `format_state_summary(...)` renders this heading for concise terminal inspection of projected State. |
| `entities` | Cardinality of canonical entities participating in the projected operator summary. | KEEP | Built from `len(entity_aliases)` as `entity_count`; the scope review classifies entity count as mostly State itself. |
| `facts` | Total projected fact volume. | KEEP | Built from `len(state.facts)` as `fact_count`; the scope review classifies fact count as State itself. |
| Optional `relationships` | Optional relationship cardinality. | KEEP | Built from `len(state.relationships)` only when requested; the scope review classifies optional relationship count as State itself. |
| `durable facts` | Fact lifecycle accounting for non-measurement facts. | KEEP | Built by excluding measurement predicates; the scope review treats durable fact count as State itself with lifecycle semantics. |
| `measurement current samples` | Fact lifecycle/projection-health accounting for non-expired current measurements. | KEEP | Built from non-expired measurement predicates; the scope review lists measurement current sample count as projected-State description. |
| `conflicts` | Count-level integrity accounting for fact conflicts. | KEEP | Built from `len(state.fact_conflicts)`; the scope review treats conflict count as State integrity accounting when not used as action priority. |
| `stale facts` | Count-level integrity and lifecycle accounting for stale facts. | KEEP | Built from `len(state.get_stale_facts())`; the scope review treats stale fact count as State integrity accounting when not used as action priority. |
| `graph issues` | Count-level projection integrity accounting split into warnings and errors. | KEEP | Built from graph issue warning/error counts; the scope review treats graph issue counts as State integrity accounting when not used as action priority. |
| `observation sources` | Observation provenance/source accounting. | KEEP | Built from observation `source_type` counts; the scope review lists observation source counts under State-itself accounting while noting they are under-specified as operator information. |
| `top entities by kind: hosts` | Operator-facing entity prominence/navigation bucket for hosts, using ranked durable-fact counts and alias counts. | MOVE | Built by ranking entities and grouping by classified kind; the scope review classifies top entities, host/service/storage prominence buckets, and alias counts as lenses over State. |
| `top entities by kind: services` | Operator-facing entity prominence/navigation bucket for services. | MOVE | Built by the same ranked, kind-classified top-entity machinery; the scope review identifies top entities as a prominence/ranking lens. |
| `top entities by kind: endpoints` | Endpoint visibility/availability count object that suppresses endpoint names. | MOVE | Rendered as endpoint total/up/down/unknown counts; tests assert endpoint counts render without endpoint names; the scope review classifies endpoint visibility summarized without names as a lens over State. |
| `top entities by kind: storage` | Operator-facing entity prominence/navigation bucket for storage entities. | MOVE | Rendered in the top-entities-by-kind loop; the scope review classifies storage prominence buckets as a lens over State. |
| Legacy `top entities` fallback | Backward-compatible undifferentiated operator-prominence list. | MOVE | The implementation calls it a legacy compatibility field and explicitly scopes it around operator prominence. |
| `availability by scope: endpoint_scrape_availability` | Scoped availability interpretation for scrape endpoints. | MOVE | Built by mapping endpoint entities to endpoint scrape availability; the scope review says availability by scope is a lens over State and can be misread as live health. |
| `availability by scope: host_availability` | Scoped availability interpretation for hosts. | MOVE | Built by mapping host entities to host availability; the scope review identifies availability by scope as a lens over State. |
| `availability by scope: service_availability` | Scoped availability interpretation for services. | MOVE | Built by mapping service entities to service availability; the scope review identifies availability by scope as operational-status interpretation unless framed only as projected availability-fact accounting. |
| Legacy `availability` fallback | Backward-compatible all-entity availability rollup. | MOVE | The implementation calls it a legacy compatibility field with historical all-entity semantics; the scope review classifies legacy all-entity availability as a lens over State. |

## KEEP sections

- Compact `Facts`
- Compact `Observations`
- Compact `Requirements`
- Compact `Capabilities`
- Compact `Issues`
- Compact `Projection Version`
- Compact `Last Event`
- Operator `entities`
- Operator `facts`
- Optional operator `relationships`
- Operator `durable facts`
- Operator `measurement current samples`
- Operator `conflicts`
- Operator `stale facts`
- Operator `graph issues`
- Operator `observation sources`

## MOVE sections

- `top entities by kind: hosts`
- `top entities by kind: services`
- `top entities by kind: endpoints`
- `top entities by kind: storage`
- Legacy `top entities`
- `availability by scope: endpoint_scrape_availability`
- `availability by scope: host_availability`
- `availability by scope: service_availability`
- Legacy `availability`

## UNCERTAIN sections

None.

Repository authority is sufficient to classify every currently rendered section as either State/projection accounting or lens/operator interpretation.

## Additional analysis

### Question 1: If every MOVE section were removed, what would State Summary contain?

It would contain only projected-State identity, cardinality, lifecycle, provenance, and count-level integrity accounting:

- compact facts, observations, requirements, capabilities, and issues;
- compact projection version and last event;
- operator entity count;
- operator fact count;
- optional relationship count;
- durable fact count;
- measurement current sample count;
- conflict count;
- stale fact count;
- graph issue warning/error counts;
- observation source counts.

It would not contain entity prominence, entity-kind navigation buckets, endpoint visibility summarization, scoped availability interpretation, or legacy compatibility rollups.

### Question 2: Would the remaining output still function as a coherent State View?

Yes.

The remaining output would still function as a coherent State View because it would continue to describe projected State shape, projection identity, lifecycle accounting, provenance accounting, and integrity-adjacent counts. That matches the repository-supported narrow State Summary definition.

### Question 3: Which MOVE sections contribute the largest amount of operator-facing interpretation?

1. `top entities by kind`
   - ranks entities;
   - classifies them into host/service/endpoint/storage buckets;
   - limits rendered rows;
   - renders alias counts and durable-fact counts;
   - suppresses endpoint names in favor of endpoint totals.

2. `availability by scope`
   - maps classified entities to endpoint, host, and service availability scopes;
   - interprets projected `availability_status` facts as up/down/unknown buckets;
   - can be misread as runtime health if not carefully framed.

3. Legacy `top entities` and legacy `availability`
   - preserve older compatibility surfaces that still carry operator-prominence and all-entity availability interpretation.

### Question 4: Which sections appear to be the original source of HomeOps-style behavior?

Repository evidence points to:

1. `top entities` / `top entities by kind`
   - the scope review identifies top entities as the clearest overloaded section;
   - the implementation uses operator-prominence language;
   - tests ensure endpoint measurement volume does not make scrape endpoints look prominent.

2. `availability by scope` / legacy `availability`
   - the scope review warns availability can be misread as live health;
   - tests enforce endpoint scrape availability boundaries from host availability.

3. Storage/filesystem interpretation is related HomeOps-style behavior, but it is not currently rendered in default State Summary.
   - default State Summary explicitly excludes storage/filesystem detail;
   - tests reject storage detail, topology groups, shared-storage candidates, and topology ambiguities from default State Summary output.

## Required report

- files inspected: `seed_runtime/state_summary_views.py`, `scripts/seed_local.py`, `tests/test_state_summary_views.py`, `tests/test_seed_local_script.py`, `docs/state_summary_scope_review.md`
- rendered sections discovered: compact State Summary sections plus operator State Summary sections listed above
- KEEP sections: listed above
- MOVE sections: listed above
- UNCERTAIN sections: none
- largest interpretation-heavy sections: `top entities by kind`, `availability by scope`, legacy `top entities`, legacy `availability`
- coherent State View remains after removal: yes
- files changed: `docs/state_summary_decomposition_audit.md`
- LOC changed: 194 added
