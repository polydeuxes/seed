---
doc_type: observation
status: exploratory
domain: diagnostic result self-observation
defines:
  - diagnostic result self-observation boundary
  - recorded diagnostic result orientation boundary
depends_on:
  - source_navigation_entity_typing_graph_issue_audit.md
  - documentation_metadata_surface_observation.md
  - observable_domain_consumer_activity_observation.md
related:
  - self_observation_reconciliation.md
  - repository_observation_source_design.md
  - graph_issue_orientation_audit.md
  - projection_integrity_summary_characterization.md
introduced_by: classification coverage diagnostic discussion 2026-06-19
---

# Diagnostic Result Self-Observation

## Status

Exploratory observation only.

This document records an implementation-adjacent observation about diagnostic output, recording, and later operator inspection.

It does not propose a diagnostic framework, ontology, runtime concept, planner, recommendation mechanism, or automatic remediation path. Repository authority remains with the cited implementation, observation, projection, and integrity documents in their own scopes.

## Context

Recent work around graph issues and entity classification coverage exposed a practical distinction.

An operator can directly run a diagnostic and inspect terminal output:

```text
operator
    -> direct diagnostic run
    -> immediate output
```

Seed can also record the diagnostic result as evidence:

```text
diagnostic run
    -> observed diagnostic result
    -> projected diagnostic facts
    -> later inspection through Seed
```

Those are related but not identical activities.

The direct diagnostic output is useful for immediate inspection. The recorded diagnostic result is useful because it gives Seed a durable, provenance-bearing account of what was observed at a projection boundary.

## Candidate Observation

A diagnostic result can become self-observation evidence when recording is explicit.

Safe shape:

```text
diagnostic ran
    -> diagnostic result observed
    -> result facts projected
    -> later read surfaces summarize or compare those facts
```

This differs from treating a diagnostic result as permanent truth.

A recorded diagnostic result may say:

```text
classification coverage diagnostic ran
unknown entities = N
graph issues involving unknown endpoints = N
projection version = v1
last event id = evt_...
observed_at = ...
```

It does not say:

```text
unknown entities are wrong
a fix is required
relationship authority is incorrect
classification should be promoted
```

## Operator Direct Test Versus Seed-Recorded Result

The operator-facing terminal command answers:

```text
What does this diagnostic report right now?
```

A recorded diagnostic result lets Seed later answer richer questions:

```text
What diagnostic ran?
When did it run?
Against which projection?
What event boundary did it inspect?
What counts were observed?
What categories dominated?
Was the result recorded or only inspected?
What changed compared with a prior recorded run?
```

This is the richer environment gained by ingesting the result. Seed can preserve diagnostic provenance, projection identity, event boundary, observed counts, dominant categories, and later deltas between recorded runs.

## Useful Recorded Details

Useful diagnostic-result facts include:

```text
diagnostic_name
observed_at
projection_version
last_event_id
command
entity_count
classified_entity_count
unknown_entity_count
unknown_entity_percentage
graph_issue_count
unknown_subject_graph_issue_count
unknown_object_graph_issue_count
both_unknown_graph_issue_count
concrete_type_mismatch_graph_issue_count
top_unknown_predicates
top_unknown_relationships
top_unknown_sources
```

Where the diagnostic supports comparison over time, later surfaces may derive:

```text
previous_unknown_entity_count
delta_unknown_entity_count
previous_graph_issue_count
delta_graph_issue_count
unchanged / improved / worsened trend labels
```

Those comparisons are read-side interpretations over recorded diagnostic results. They should preserve the underlying run identifiers, timestamps, projection versions, and event ids.

## Orientation Boundary

The operator orientation can be described narrowly when the evidence supports it.

For the classification coverage work, a safe orientation statement is:

```text
The operator is investigating whether current graph issues are dominated by
relationship-authority failures or by endpoint-classification visibility gaps.
```

Current evidence includes graph issue output where relationship endpoints were reported as:

```text
expected=document actual=unknown
expected=concept actual=unknown
```

That supports orienting the diagnostic toward classification coverage.

It does not support claiming that the operator intends to redesign ontology, fix relationship authority, promote new classifications, or treat unknown entities as inherently wrong.

## Inspection And Recording Boundary

Default diagnostic execution should remain inspection-only unless implementation explicitly records it.

Safe command boundary:

```text
seed --classification-coverage
    -> inspect current projected State
    -> no mutation
    -> no observations appended
```

Explicit recording boundary:

```text
seed --classification-coverage --record
    -> inspect current projected State
    -> append self-observation evidence for the diagnostic result
```

This preserves the distinction between looking at a surface and adding new evidence to Seed.

The same pattern may apply to other diagnostics:

```text
seed --graph-issue-summary
    -> inspect

seed --graph-issue-summary --record
    -> record graph issue inventory as self-observation evidence
```

The pattern should not be generalized into a framework from this observation alone.

## Supported Observations

Supported observations:

1. Direct diagnostic output and recorded diagnostic evidence are distinct activities.
2. Recorded diagnostic results can give Seed richer later answers than terminal output alone.
3. Useful richness comes from provenance, projection boundary, event boundary, observed counts, categories, and comparison between runs.
4. Recording must be explicit to avoid turning every inspection into mutation.
5. Operator orientation can be described narrowly from current evidence without asserting intent, priority, recommendation, or remediation.
6. Classification coverage diagnostics are a concrete self-observation surface because they inspect Seed's projected State and graph issue inventory.

## Unsupported Observations

Unsupported observations:

1. A diagnostic result is permanent truth.
2. A diagnostic result implies a fix.
3. Unknown entity counts imply incorrect entities.
4. Graph issue counts imply relationship-authority failure.
5. Recording should happen automatically for every diagnostic inspection.
6. Operator orientation authorizes implementation priority or next-safe-move selection.
7. This observation establishes a diagnostic framework or ontology.

## Preserved Uncertainty

This observation does not determine which diagnostics should support `--record`.

It also does not determine the exact fact vocabulary for diagnostic-result observations. That vocabulary should follow implementation and predicate-catalog conventions where implemented.

The safest current reading is:

```text
diagnostic inspection
    !=
self-observation recording
```

and:

```text
recorded diagnostic result
    ==
provenance-bearing evidence about what a diagnostic observed at a projection boundary
```

not:

```text
recorded diagnostic result
    ==
truth, recommendation, remediation, or architecture authority
```
