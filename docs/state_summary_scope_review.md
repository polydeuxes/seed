# State Summary Scope Review

## Purpose

This is an architectural review of State Summary responsibility, scope, and authority.
It does not redesign implementation, remove output, add output, rename commands, or introduce a dashboard or node-specific operational view.

The review question is:

```text
What should State Summary actually be responsible for,
and what should belong in separate lenses/views instead?
```

## Files inspected

Primary implementation surfaces:

- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `scripts/seed_local.py`
- `seed_runtime/projection_store.py`

Primary tests inspected:

- `tests/test_state_summary_views.py`
- `tests/test_state_views.py`
- `tests/test_seed_local_script.py`
- `tests/test_projection_store.py`
- `tests/test_relationship_catalog.py`
- `tests/test_graph_validation.py`
- `tests/test_candidate_requests.py`

Related documentation inspected:

- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_cli_boundary_audit.md`
- `docs/state_summary_filesystem_projection_boundary_audit.md`
- `docs/state_summary_top_entity_selection_audit.md`
- `docs/state_summary_endpoint_prominence_audit.md`
- `docs/state_summary_empty_operator_kind_buckets_audit.md`
- `docs/storage_measurement_current_fact_regression_audit.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/response_vocabulary.md`
- `docs/state.md`

## Current implementation shape

There are currently two State Summary-related summary layers.

### Compact projected world-model summary

`seed_runtime/state_views.py::build_state_summary(state)` returns a compact read-only `StateSummary` with counts for facts, observations, requirements, capabilities, issues, plus projection identity fields (`last_event_id` and `projection_version`). This is the closest existing implementation to a narrow summary of projected State itself.

It answers:

```text
What is the size and projection identity of the projected world model?
```

### Operator State Summary

`seed_runtime/state_summary_views.py::state_summary(state)` returns a richer dictionary described in code as a concise operator summary using only projected State. It includes counts, integrity signals, observation-source counts, top entities by kind, availability by scope, legacy top-entity and availability fields, and optionally relationship count.

It answers several questions at once:

```text
How large is State?
What integrity warnings exist?
What observation sources contributed?
Which entities look prominent?
What availability statuses are visible by scope?
```

The CLI path in `scripts/seed_local.py` couples both layers: `projected_state_summary_from_args(...)` loads or builds the projected State, builds both `build_state_summary(state)` and `state_summary(state)`, stores both in a dependent state-summary snapshot, and `format_state_summary(...)` renders the operator summary.

## What State Summary currently renders

The terminal State Summary currently renders these sections from the operator summary:

| Rendered section | Current source field(s) | Why it exists today | State itself or lens over State? |
|---|---|---|---|
| Entity count | `entity_count` | Repository-wide cardinality of canonical entities participating in the projected summary. | Mostly State itself, although canonicalization and participation rules are summary-specific. |
| Fact count | `fact_count` | Total projected fact volume. | State itself. |
| Optional relationship count | `relationship_count` | Relationship catalog tests require optional relationship cardinality without changing default output. | State itself. |
| Durable fact count | `durable_fact_count` | Separates durable knowledge from measurement current samples after measurement-retention work. | State itself, with domain semantics about fact lifecycle. |
| Measurement current samples | `measurement_current_sample_count` | Shows retained current measurement sample volume without exposing full history. | State itself/projection health. |
| Conflict count | `conflict_count` | Indicates projected fact conflict volume. | State integrity. Could also belong in Projection Integrity Summary. |
| Stale fact count | `stale_fact_count` | Indicates facts requiring freshness attention. | State integrity with operational-attention implications. |
| Graph issues | warning/error counts | Indicates graph validation issues in projected State. | State integrity. Could also belong in Projection Integrity Summary. |
| Observation sources | `observation_source_counts` | Accounts for observation provenance/source distribution. | State itself/provenance inventory. |
| Top entities by kind: hosts/services/storage | `top_entities_by_kind` rows | Gives compact, operator-friendly prominence/inventory rows with alias and durable-fact counts. | Lens over State. Ranking, kind buckets, and limits are view choices. |
| Top entities by kind: endpoints | endpoint availability count object | Preserves endpoint visibility without rendering endpoint names as prominent entities. | Lens over State; partly operational visibility. |
| Availability by scope | `availability_by_scope` | Separates endpoint scrape availability from host and service availability after endpoint-boundary audits. | Lens over State; availability is a projected fact count, not runtime health authority. |
| Legacy top entities | `top_entities` | Backward-compatible field retained for older callers. | Lens over State and compatibility surface. |
| Legacy availability | `availability` | Backward-compatible all-entity availability counts. | Lens over State and compatibility surface. |

## What is State Summary?

Repository evidence supports this definition:

```text
State Summary is a deterministic, read-only summary of the projected State/read model.
```

A narrower authority statement would be:

```text
State Summary should describe the shape, identity, and integrity-adjacent accounting of projected State.
It should not be the default authority for every operator interpretation of State.
```

The compact `build_state_summary(state)` already embodies the narrowest version of this idea: counts and projection identity. The richer operator summary extends beyond that by selecting prominent entities, grouping entity kinds, separating availability scopes, and preserving compatibility fields.

## What is State Summary not?

State Summary should not be treated as:

- a HomeOps dashboard;
- a node dashboard;
- a runtime health checker;
- an operational attention queue;
- a recommendation engine;
- a storage-topology authority;
- an ownership/topology inference surface;
- the only or canonical way operators interact with State.

The existing implementation already contains several boundary comments and tests enforcing parts of this non-authority, especially around endpoint identity, filesystem/storage interpretation, and availability scope. The concern is that those guardrails live inside a surface whose name still invites broad operator-dashboard interpretation.

## Sections that appear to describe State itself

These sections are closest to projected-State description:

- projection identity: `last_event_id`, `projection_version` in the compact `StateSummary`;
- fact count;
- observation count in the compact `StateSummary`;
- requirement count in the compact `StateSummary`;
- capability count in the compact `StateSummary`;
- issue count in the compact `StateSummary`;
- entity count;
- optional relationship count;
- durable fact count;
- measurement current sample count;
- observation source counts;
- fact support count when using the lower-level state-view count behavior;
- graph issue, conflict, and stale-fact counts when framed as integrity accounting rather than action priority.

These are mostly cardinality, provenance, lifecycle, or projection-integrity facts about the read model.

## Sections that appear to describe a lens over State

These sections are not raw State shape; they are useful views/lenses built from State:

- top entities by kind;
- endpoint visibility summarized without endpoint names;
- host/service/storage prominence buckets;
- alias counts rendered beside top entities;
- availability by scope;
- legacy all-entity availability;
- filesystem shape summaries and storage topology candidates in the storage projection helper;
- shared-storage candidates and storage-topology ambiguities;
- any operator-relevant mount filtering, mount display priority, or bounded detail selection.

These sections may be valuable, but their semantics are view choices: they rank, classify, suppress, group, or interpret State for an operator purpose.

## Sections that appear overloaded

### Top entities

Top entities are the clearest overloaded section. They are derived from projected facts, but the output is a prominence/ranking lens. Recent repository history already narrowed endpoint prominence by ranking durable facts only and rendering endpoint totals without names. That history is evidence that the section is trying to answer operator-attention questions rather than only State-shape questions.

### Availability

Availability is represented as projected facts, but its summary can be misread as live health. The current scoped availability output is safer than the old all-entity rollup, but it still belongs naturally to an availability/operational-status lens unless explicitly framed as projected availability-fact accounting.

### Graph issues, conflicts, and stale facts

These are legitimate State integrity counts. They become overloaded when State Summary is read as an operational priority surface. Projection Integrity Summary is already a more natural authority for integrity drilldown and caveats.

### Storage and filesystem interpretation

The current default operator summary excludes storage detail projection keys, while the same module still owns an explicit `storage_state_projection(state)` helper with filesystem shape, cluster mount visibility, shared-storage candidates, and topology ambiguity summaries. This is strong evidence that storage interpretation is a separate lens over State, not core State Summary responsibility.

### Observation source counts

Observation source accounting describes State provenance, but it is under-specified as operator information. It says how observations entered State, not what the operator should do with them. A provenance/observation lens may eventually explain this better than the generic State Summary.

## Candidate State-vs-lens distinction

A useful architectural distinction is:

```text
one deterministic projected State
    supports
many deterministic read-only lenses over State
```

Under that distinction, State Summary should be one lens with narrow authority, not the umbrella surface for all operator views.

### Candidate State Summary responsibility

State Summary should primarily summarize:

- projection identity and boundary (`last_event_id`, `projection_version`);
- State cardinality (entities, facts, observations, relationships, requirements, capabilities);
- fact lifecycle accounting (durable facts versus current measurement samples);
- support/provenance accounting when needed (fact support count, observation source counts);
- projection-integrity accounting at a count level (conflicts, stale facts, graph issue counts), with drilldown delegated elsewhere;
- build/cache status only as execution/projection metadata, not as domain interpretation.

### Candidate separate lenses/views

Natural future lenses suggested by current repository evidence:

1. **Projection Health / Integrity lens**
   - conflicts;
   - contradictions;
   - graph issues;
   - stale facts;
   - unsupported facts;
   - refresh recommendations;
   - cache/projection freshness;
   - drilldown links to existing integrity, contradiction, evidence, and graph-issue views.

2. **Knowledge Inventory lens**
   - learned hosts, services, endpoints, storage subjects, capabilities, requirements;
   - counts by entity type;
   - alias/canonicalization inventory;
   - durable knowledge versus measurement sample accounting.

3. **Operational Availability lens**
   - host availability facts;
   - service availability facts;
   - endpoint scrape availability facts;
   - explicit caveat that these are projected availability observations, not live probes.

4. **Entity Prominence / Navigation lens**
   - top entities;
   - ranking basis;
   - aliases;
   - fact/support counts;
   - drilldown targets.

5. **Observation / Provenance lens**
   - observation source counts;
   - source-type semantics;
   - evidence and fact-support navigation.

6. **Storage Projection lens**
   - filesystems;
   - mount visibility;
   - shared-storage candidates;
   - storage-topology ambiguities;
   - explicit non-authority over ownership, identity, and topology truth.

These lenses should remain deterministic read-only projections unless separate repository authority later says otherwise.

## Major findings

1. **State Summary has two meanings today.** The repository has a compact `StateSummary` read model and a richer operator summary. They are built and cached together in the CLI path, which reinforces the perception that operator overview is the same thing as State Summary.

2. **The compact summary is closest to projected-State authority.** Its counts and projection identity fields stay close to State shape and projection boundary.

3. **The operator summary mixes State accounting with operator lenses.** Counts such as fact count and measurement current sample count describe State; top entities and availability scopes are lenses over State.

4. **Recent boundary work already points away from a dashboard interpretation.** Endpoint prominence, filesystem projection, storage ambiguity, and availability scope work all reduced accidental operational interpretation without removing the output.

5. **State construction is coupled to State Summary as a default operator entry point.** `--state-summary` builds State and both summary layers, then persists a dependent summary snapshot. This is appropriate for performance, but architecturally it can make State Summary look like the canonical way to consume State.

6. **A State-vs-lens split is the natural next architectural vocabulary.** One deterministic State can support multiple read-only deterministic lenses. State Summary can then narrow to State shape/projection accounting while other lenses own operational, inventory, prominence, provenance, and storage interpretations.

## Non-findings / boundaries preserved

This review does not recommend immediate implementation changes.

It does not recommend removing current State Summary fields.

It does not recommend adding dashboards, node views, operational runtime behavior, probes, recommendations, or HomeOps-specific views.

It does not rename commands or alter CLI output.

## Conclusion

State Summary should primarily be responsible for describing projected State itself: projection identity, cardinality, lifecycle counts, provenance accounting, and count-level integrity signals.

Sections that rank, classify, interpret, prioritize, or present domain-specific operator meaning should be recognized as lenses over State. Some of those lenses already exist implicitly inside State Summary. Future work can separate authority without changing behavior first: document the State-vs-lens boundary, preserve deterministic read-only behavior, and only then consider implementation refactors under repository authority.
