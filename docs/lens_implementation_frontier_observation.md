---
doc_type: observation
status: exploratory
domain: lens implementation frontier
related:
  - lens_catalog_observation.md
  - state_summary_scope_review.md
  - inquiry_note_orientation_probe_plan.md
  - inquiry_note_orientation_surface_reachability_observation.md
  - operator_pressure_as_evidence_observation.md
  - projection_integrity_summary_characterization.md
  - projection_integrity_drilldown_characterization.md
  - source_navigation_surface_reconciliation.md
---

# Lens Implementation Frontier Observation

## Purpose

Recent repository work produced a lens catalog. The repository now appears to
contain this architectural shape:

```text
one deterministic State
    ->
many possible lenses
```

The question for this observation is no longer:

```text
What is a lens?
```

The question is:

```text
Which candidate lenses appear closest to an implementation frontier, and why?
```

This document is exploratory only. It does not implement lenses, alter CLI
behavior, create dashboards, modify Inquiry Orientation, redesign State Summary,
recommend V2 implementation, introduce semantic retrieval, or introduce LLM
interpretation.

## Reading And Authority Boundary

Required and primary reading:

- `docs/lens_catalog_observation.md`
- `docs/state_summary_scope_review.md`
- `docs/inquiry_note_orientation_probe_plan.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/operator_pressure_as_evidence_observation.md`
- requested `docs/lens_view_architecture_audit.md` was searched for but is not
  present in this repository snapshot

Related implementation and documentation inspected as evidence:

- `seed_runtime/integrity_summary.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/source_navigation.py`
- `scripts/seed_local.py`
- related tests and documentation found by repository search

Repository authority remains with existing code, tests, and scoped documents.
This observation classifies implementation-frontier evidence only.

## Frontier Classification Legend

```text
conceptual
    named or described in documentation, but no distinct implementation surface

partially implemented
    some deterministic read model, helper, command, formatter, or tests already
    embody part of the lens, but boundaries or lens ownership remain mixed

implemented
    a distinct read-only surface exists with command/rendering/tests and explicit
    authority boundaries close to the candidate lens
```

"Implemented" here does not mean complete, ideal, or recommended. It only means
the repository already has a recognizably separate surface for that lens-shaped
question.

## Cross-Cutting Findings

### Candidate Lenses Already Partially Exist

The strongest partial or complete surfaces are:

- **Projection Health / Integrity**: has a separate `ProjectionIntegritySummary`,
  builder, CLI flag, formatter, caveats, and links to drilldown commands. It is
  the clearest implemented lens-shaped surface.
- **Storage Projection**: has an explicit `storage_state_projection(state)`
  helper and storage-specific projection machinery, but default State Summary is
  deliberately guarded against becoming a storage detail surface.
- **Entity Navigation / Prominence**: top-entity ranking, entity-kind buckets,
  aliases, durable-fact ranking, and endpoint suppression exist inside operator
  State Summary, so the lens exists implicitly rather than separately.
- **Operational Availability**: availability-by-scope exists inside operator
  State Summary, with host/service/endpoint boundaries, but no separate
  availability lens surface is visible.
- **Observation / Provenance**: observation source counts and fact support
  surfaces exist, and Inquiry Orientation can traverse fact support, but there is
  no single provenance lens.
- **Source / Knowledge Navigation**: source navigation is implemented as a
  bounded read-only view over preserved source facts.
- **Inquiry Orientation**: Inquiry Orientation V1 is implemented as an isolated
  probe and read-only orientation view over preserved note evidence plus
  projected State/source-navigation matches.
- **Node Detail**: node-impact/detail-style formatting exists in CLI helper code,
  especially around canonical entity impact, endpoint availability, storage
  topology, identity, listener, and local-network caveats. It does not appear to
  be a clean general lens module.

### Candidate Lenses With No Clear Implementation

The clearest no-implementation or mostly-conceptual candidates are:

- **HomeOps Dashboard**: repository documents repeatedly use dashboard language
  as a boundary, not as an implemented surface. No dashboard should be inferred
  from State Summary.
- **Knowledge Inventory** as a standalone lens: inventory pieces exist in State
  Summary and capability inventory/integrity code, but no dedicated general
  knowledge-inventory surface appears to own learned hosts, services, endpoints,
  storage, aliases, requirements, and capabilities together.
- **A general lens framework**: the repository has deterministic read-only views,
  but no common lens registry, lens composition architecture, or lens-view
  abstraction was found.

### Operator Value Signals

Repository evidence suggests operator value is strongest where a lens answers a
felt operator pressure without over-promoting pressure into implementation
authority:

1. **Projection Health / Integrity**: directly helps operators ask what might
   need investigation by aggregating unsupported facts, conflicts,
   contradictions, graph issues, stale facts, refresh recommendations, and
   capability evidence status.
2. **Entity Navigation / Prominence**: helps operators understand why some
   entities appear prominent, and recent endpoint/top-entity boundary work shows
   that prominence can otherwise mislead operator attention.
3. **Operational Availability**: operators naturally care about availability,
   but the repository repeatedly warns that projected availability facts are not
   live probes or health authority.
4. **Inquiry Orientation**: explicitly addresses the gap between available
   knowledge and activated work, but V1 evidence shows strong reachability for
   runtime entities and weak reachability for repository concepts.
5. **Storage Projection**: valuable where filesystem/topology facts confuse
   operators, but repository documents and tests emphasize the need for strong
   caveats.

### Repository-Readiness Signals

Repository readiness appears strongest where read-only State projections,
formatters, commands, and caveats already exist:

1. **Projection Health / Integrity**: strongest readiness; already separately
   surfaced.
2. **Source / Knowledge Navigation**: strong readiness for source facts; weaker
   if broadened to all knowledge navigation.
3. **Storage Projection**: strong projection helpers and caveats; weaker public
   surface separation.
4. **Operational Availability**: scoped counts exist; needs separate authority if
   moved out of State Summary.
5. **Entity Navigation / Prominence**: ranking exists; needs separate ownership
   if extracted from State Summary.
6. **Inquiry Orientation**: implemented as V1 probe; generalization remains
   unresolved because reachable surfaces are limited.

## Lens Inventory Review

### Projection Health / Integrity

- **Current status:** implemented as a summary lens; broader drilldown family is
  partially implemented.
- **Existing commands/surfaces:** `--integrity-summary` in CLI; formatter prints
  unsupported facts, fact conflicts, contradictions, graph issues, stale facts,
  refresh recommendations, capability counts, caveats, projection version, and
  last event. It points to existing drilldown commands such as unsupported facts,
  fact conflicts, contradictions, graph issues, stale facts, stale refreshes, and
  capability status.
- **Authority boundaries:** read-only; aggregates existing projected integrity
  signals only; does not create facts or evidence, execute runtime behavior,
  call providers, verify capabilities, refresh stale facts, resolve
  contradictions, or mutate projected State.
- **Implementation prerequisites:** mostly present for summary-level operation;
  richer implementation would depend on existing drilldown surfaces retaining
  source semantics and avoiding repair/execution authority.
- **Relationship to operator workflows:** high value for investigation triage.
  It converts scattered integrity signals into a bounded overview without
  claiming truth, correctness, health, repair, or recommendation authority.
- **Blocked by missing architecture:** not strongly blocked for summary use;
  broader composition with other lenses would need an explicit lens architecture.
- **Blocked by missing State projections:** not strongly blocked for current
  counts; any deeper provenance or priority view may require more structured
  support/provenance projections.

### Knowledge Inventory

- **Current status:** partially implemented in fragments; no standalone lens.
- **Existing commands/surfaces:** compact State Summary counts facts,
  observations, requirements, capabilities, issues, projection identity; operator
  State Summary counts entities, facts, durable facts, current measurements,
  observation sources, and top entities by kind. Capability inventory also feeds
  integrity summary capability counts.
- **Authority boundaries:** should describe what the projected read model knows
  or preserves, not what matters most, what is true outside the projection, or
  what work should occur.
- **Implementation prerequisites:** a dedicated inventory lens would need to own
  buckets across hosts, services, endpoints, storage, aliases, requirements,
  capabilities, relationships, and lifecycle counts rather than inheriting mixed
  State Summary semantics.
- **Relationship to operator workflows:** useful for orientation and coverage
  questions: "what does Seed know about this environment?" Current evidence is
  broad but scattered.
- **Blocked by missing architecture:** moderately blocked by the lack of a
  general lens boundary/registry and by State Summary owning several inventory
  fragments.
- **Blocked by missing State projections:** partly blocked where inventory wants
  consistent entity typing, alias/canonicalization, and relationship/lifecycle
  projections across domains.

### Observation / Provenance

- **Current status:** partially implemented in fragments.
- **Existing commands/surfaces:** observation source counts in State Summary;
  fact support and why/explanation surfaces; Inquiry Orientation matches against
  `state.fact_supports`; source navigation exposes representative support ids
  for preserved source facts.
- **Authority boundaries:** provenance explains support paths and observation
  sources. It must not become truth authority, semantic interpretation, or a
  claim that unsupported material is false.
- **Implementation prerequisites:** a standalone lens would need a coherent way
  to group observations, source types, support ids, representative facts,
  unsupported facts, and evidence strength without duplicating integrity summary.
- **Relationship to operator workflows:** high value for audit/explanation:
  "why is this in State?" and "where did this come from?"
- **Blocked by missing architecture:** moderately blocked by overlap with
  Projection Integrity, Source Navigation, and explanations.
- **Blocked by missing State projections:** likely blocked where support and
  provenance need consistent projected rows beyond current counts and support
  records.

### Operational Availability

- **Current status:** partially implemented inside State Summary.
- **Existing commands/surfaces:** `availability_by_scope` separates endpoint
  scrape availability, host availability, and service availability; legacy
  availability remains for compatibility. CLI rendering prints scoped
  availability inside State Summary.
- **Authority boundaries:** projected availability facts are not live health,
  reachability, provider verification, or runtime probe results.
- **Implementation prerequisites:** separate ownership for availability grouping,
  caveats, and display if it leaves State Summary; preservation of endpoint vs
  host/service scope boundaries.
- **Relationship to operator workflows:** strong operational value because
  availability status is an obvious operator question, but it is also high-risk
  because it can be misread as live health.
- **Blocked by missing architecture:** lightly to moderately blocked; the data is
  present, but a separate lens boundary would reduce State Summary overload.
- **Blocked by missing State projections:** not strongly blocked for count-level
  status; stronger views may need clearer projected freshness, source, and
  measurement-age fields.

### Entity Navigation / Prominence

- **Current status:** partially implemented inside State Summary.
- **Existing commands/surfaces:** `top_entities_by_kind`, legacy `top_entities`,
  durable-fact ranking, alias counts, entity-kind classification, endpoint
  visibility as aggregate counts rather than endpoint-name prominence.
- **Authority boundaries:** ranking is a presentation choice, not proof of
  importance, relevance, ownership, or active work. Endpoint suppression shows
  the repository already treats prominence as a potentially misleading lens.
- **Implementation prerequisites:** a separate navigation/prominence lens would
  need explicit ranking basis, caveats, and drilldown targets.
- **Relationship to operator workflows:** strong value for "where should I look?"
  and "why is this entity prominent?" It is also where operator attention can be
  most distorted by measurement volume.
- **Blocked by missing architecture:** moderately blocked by State Summary
  ownership and lack of generic entity-detail/navigation composition.
- **Blocked by missing State projections:** partly blocked by entity typing,
  alias/canonicalization, and support-count projections.

### Storage Projection

- **Current status:** partially implemented; explicit projection helper exists.
- **Existing commands/surfaces:** `storage_state_projection(state)` exposes an
  explicit storage/filesystem topology projection surface. State Summary helper
  code computes filesystem shape, cluster mount visibility, shared-storage
  candidates, topology ambiguities, and summary counts. Tests and formatter
  boundaries prevent storage detail from leaking into default State Summary.
- **Authority boundaries:** storage projection candidates are not ownership,
  storage identity, shared-storage facts, health, availability, filesystem
  health, or resolved topology.
- **Implementation prerequisites:** if elevated as a lens, it needs a dedicated
  operator surface that keeps candidate/ambiguity caveats visible and avoids
  dashboard or node-topology authority.
- **Relationship to operator workflows:** valuable when filesystem rows and
  cluster-mount patterns create confusion, especially in HomeOps-style settings.
- **Blocked by missing architecture:** lightly blocked at helper level; more
  blocked at operator-surface level because default State Summary explicitly
  rejects storage detail.
- **Blocked by missing State projections:** partly blocked where topology truth,
  ownership, identity, and relationship projections are intentionally absent or
  not authoritative.

### HomeOps Dashboard

- **Current status:** conceptual / not implemented.
- **Existing commands/surfaces:** none identified as a dashboard. State Summary,
  availability, storage, and integrity surfaces contain dashboard-like fragments
  but are explicitly bounded away from dashboard authority.
- **Authority boundaries:** a dashboard would risk combining availability,
  storage, integrity, prominence, and attention signals into operational meaning.
  Existing documents explicitly warn that State Summary is not a HomeOps
  dashboard, node dashboard, runtime health checker, or operational attention
  queue.
- **Implementation prerequisites:** would require a separate dashboard authority,
  composition rules, panel caveats, and probably architectural work not present
  now.
- **Relationship to operator workflows:** potentially high value, but also the
  highest risk of collapsing many lenses into one over-authoritative surface.
- **Blocked by missing architecture:** strongly blocked by missing lens
  composition and dashboard authority.
- **Blocked by missing State projections:** likely blocked by missing live-health
  and topology authority if interpreted operationally; existing projected State
  cannot supply those meanings.

### Node Detail

- **Current status:** partially implemented as CLI/entity-impact formatting, not
  as a clean standalone lens.
- **Existing commands/surfaces:** CLI helper code formats canonical entity
  impact-style sections including availability status, endpoint availability by
  role, storage topology, listener/local-network caveats, mount facts, storage
  facts, and identity facts. The code repeatedly states what is not inferred.
- **Authority boundaries:** node detail must not infer availability,
  reachability, ownership, health, filesystem health, or topology truth from
  listener, mount, storage, identity, or network facts.
- **Implementation prerequisites:** a clean node-detail lens would need a module
  boundary and State projections that distinguish node identity, endpoints,
  storage, local network, and support paths without creating a dashboard.
- **Relationship to operator workflows:** useful for targeted investigation of a
  single host/node. It is less broad than HomeOps Dashboard and more concrete
  than generic entity prominence.
- **Blocked by missing architecture:** moderately blocked by mixed CLI helper
  ownership and lack of dedicated lens module.
- **Blocked by missing State projections:** partly blocked by authority-preserved
  topology, ownership, and health projections.

### Inquiry Orientation

- **Current status:** implemented as V1 probe; unresolved as a general lens
  pattern.
- **Existing commands/surfaces:** `--record-inquiry-note` stores raw inquiry
  notes in an isolated JSONL probe store; `--inquiry-orientation` renders a
  bounded orientation view. Runtime code builds lexical matches from fact support
  and source navigation.
- **Authority boundaries:** the note is preserved operator prose, not fact,
  claim, goal, tool need, requirement, capability, decision, proposal, plan,
  authorization, command, runtime instruction, or intent. Matches are
  deterministic lexical overlaps and do not assert importance, ownership,
  concern, recommended action, or next safe move.
- **Implementation prerequisites:** further classification would require knowing
  which surfaces participate and why repository concepts are weakly reachable.
  This observation does not propose that work.
- **Relationship to operator workflows:** high value for orientation around
  operator pressure and raw inquiry evidence. Current observed behavior favors
  runtime entities and weakly reaches repository concepts.
- **Blocked by missing architecture:** blocked as a general pattern by unresolved
  surface composition and reachability boundaries.
- **Blocked by missing State projections:** likely blocked where repository
  concepts, frontiers, active edges, and documentation concepts are not projected
  into participating surfaces.

### Source / Knowledge Navigation

- **Current status:** source navigation implemented; broader knowledge navigation
  partially implemented/conceptual.
- **Existing commands/surfaces:** `build_source_navigation(state, query)` and
  `format_source_navigation(view)` provide a bounded read-only view over
  preserved `imports` and `defines` facts. Inquiry Orientation reuses source
  navigation for token matches.
- **Authority boundaries:** source navigation does not inspect files, parse
  source, ingest observations, infer behavior, infer reachability, or infer
  ownership. It navigates preserved facts only.
- **Implementation prerequisites:** broader knowledge navigation would need
  support for non-source concepts, documentation concepts, observations,
  frontiers, and relationship paths without semantic retrieval.
- **Relationship to operator workflows:** valuable for code/source lookup and for
  keeping navigation tied to preserved support.
- **Blocked by missing architecture:** source-fact navigation is not strongly
  blocked; broader knowledge navigation is blocked by missing concept-surface
  architecture.
- **Blocked by missing State projections:** broader knowledge navigation is
  blocked by missing projections for repository/documentation concepts and
  concept-to-support relations.

## Implementation Frontier Classification

### Smallest Architectural Risk

The smallest architectural-risk frontier appears to be lenses whose read-only
surfaces already exist and whose authority boundaries are explicit:

1. **Projection Health / Integrity**: already has a distinct module, dataclass,
   builder, caveats, CLI flag, formatter, and links to existing drilldowns.
2. **Source Navigation**: already has a distinct module and bounded read-only
   behavior over preserved source facts.
3. **Storage Projection**: has explicit projection helpers and caveats, but its
   default State Summary exclusion means any operator-facing separation would
   need careful boundary handling.

This is classification only, not an implementation recommendation.

### Greatest Operator Value

The greatest operator-value candidates appear to be:

1. **Projection Health / Integrity**, because it answers investigation-readiness
   questions using existing integrity evidence.
2. **Entity Navigation / Prominence**, because it shapes operator attention and
   already required endpoint/prominence boundary corrections.
3. **Operational Availability**, because operators naturally ask availability
   questions, while repository boundaries show high risk of live-health
   misinterpretation.
4. **Inquiry Orientation**, because it preserves operator pressure and helps
   orient around it, but V1 reachability remains uneven.
5. **Storage Projection**, because storage/topology ambiguity can be operator
   painful and evidence-sensitive.

This is classification only, not prioritization authority.

### Best Exercise Of State-vs-Lens Distinction

The lenses that most naturally exercise the new distinction are:

- **Entity Navigation / Prominence**: same State facts can produce raw entity
  counts, durable-fact prominence, endpoint visibility, and alias display. The
  ranking is visibly lens-specific.
- **Operational Availability**: same projected availability facts can be counted
  as State facts or presented as availability by scope; the latter is a lens and
  not live health.
- **Storage Projection**: same filesystem facts can be raw measurements,
  candidate shared-storage interpretations, or node-relevant display rows. The
  caveats demonstrate lens authority limits.
- **Inquiry Orientation**: same State/source-navigation material becomes related
  material only through a preserved raw note and lexical match rules, showing a
  viewpoint over State rather than new State.

## Inquiry Orientation V1 Classification

Inquiry Orientation V1 currently appears best classified as:

```text
prototype lens
```

It has a real implementation and a separate operator surface, so it is more than
conceptual. It is also explicitly a probe: inquiry notes are stored outside the
event ledger, matching is deterministic lexical overlap, and authority language
states that the note is preserved evidence rather than intent, goal, command,
plan, or recommendation. The reachability observation reports that runtime
entities participate, repository concepts participate weakly or not at all, and
additional query variation stopped producing substantially new observations.

It is not yet strong evidence for a **general lens pattern**, because V1
participates through a narrow set of surfaces: projected fact support and source
navigation. It may contain **special-case lens** behavior because it is organized
around raw operator prose, isolated note storage, and lexical overlap rather than
a normal State-only query. The current evidence therefore supports "prototype
lens" with unresolved generality.

## State Summary Classification

State Summary appears to be converging toward something broader than a pure
Projection Health lens, while also shedding several lens-like responsibilities
from its center.

Evidence:

- The compact State Summary in `state_views` is closest to projected-State
  accounting: facts, observations, requirements, capabilities, issues,
  projection version, and last event.
- The richer operator State Summary mixes State-shape accounting with integrity
  counts, observation source counts, top-entity prominence, endpoint visibility,
  availability by scope, and compatibility fields.
- Integrity counts inside State Summary overlap naturally with Projection Health
  / Integrity, but the implemented Projection Integrity Summary already owns a
  broader integrity overview with unsupported facts, conflicts, contradictions,
  graph issues, stale facts, refresh recommendations, and capability evidence
  status.
- Top entities, availability, storage projection, and source/provenance concerns
  are lens-like but not all integrity-like.

Classification:

```text
State Summary naturally converges toward a narrow State/accounting summary plus
integrity-adjacent counts, not toward becoming only a Projection Health lens.
```

Projection Health is a strong neighboring lens and may absorb or contextualize
integrity material, but State Summary remains broader where it describes
projection identity, cardinality, lifecycle counts, observation source counts,
and compatibility-level operator overview. This is an observation about current
shape, not a redesign proposal.

## Candidate Frontier Lenses

Candidate frontier lenses, classified by current evidence:

| Candidate lens | Status | Small architectural risk | Operator value | Repository evidence |
|---|---|---:|---:|---:|
| Projection Health / Integrity | implemented summary / partial family | high | high | high |
| Source / Knowledge Navigation | source implemented, knowledge partial | high for source | medium | high for source |
| Storage Projection | partially implemented | medium | medium-high | high |
| Operational Availability | partially implemented | medium | high | medium-high |
| Entity Navigation / Prominence | partially implemented | medium | high | medium-high |
| Observation / Provenance | partially implemented | medium-low | high | medium |
| Inquiry Orientation | prototype implemented | medium-low | high | medium |
| Knowledge Inventory | fragmented partial | medium-low | medium-high | medium |
| Node Detail | fragmented partial | medium-low | medium-high | medium |
| HomeOps Dashboard | conceptual | low | potentially high | low as implementation |

## Non-Findings

This observation does not find that any lens should be implemented next.

It does not find that State Summary should be redesigned, narrowed, renamed, or
split now.

It does not find that Inquiry Orientation should be generalized, optimized,
extended with semantic retrieval, or treated as a V2 plan.

It does not find that dashboard composition is currently authorized.

## Conclusion

The implementation frontier is uneven. Projection Health / Integrity is the
clearest implemented lens-shaped surface. Source Navigation is a strong bounded
navigation lens over source facts. Storage Projection, Operational Availability,
and Entity Navigation / Prominence are already present as deterministic
read-only view logic but remain mixed into State Summary or CLI helper surfaces.
Inquiry Orientation V1 is a real prototype lens with unresolved generality.
HomeOps Dashboard remains conceptual and architecturally blocked.

The strongest repository pattern is not a single next lens. It is the repeated
need to preserve this distinction:

```text
projected State says what is preserved
lens says how a bounded operator question views it
```
