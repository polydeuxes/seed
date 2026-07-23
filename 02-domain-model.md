# 02 Domain Model

This is an active, bounded domain witness for the implementation that exists now.
It is not a universal runtime, registry, executor, policy-routing, planning,
handoff, pending-action, builder-candidate, generated-toolkit, provider-handoff,
or model-visible operation-routing architecture.

Absent implementation owners are not current domain kinds. Historical names from
former design roads are not preserved here as legacy, quarantined, experimental,
or non-executable current objects.

## Current standing

Seed's currently evidenced domain centers on append-only events, observations,
evidence-backed facts, projected state, relationships, provenance, read-only
views and diagnostics, capability testimony, and provider recommendation
metadata where implementation exists.

Mixed implementation families such as `ToolNeed`, `ToolSpec`, `Toolkit`,
`Approval`, `RiskClass`, `CapabilityCatalog`, and recommendation models remain
implementation witnesses with unresolved Fidelity standing. This document does
not validate them as final Seed-owned kinds.

## Core objects

### Event

An immutable record of something that happened. Events are the historical source
for projection; recording a diagnostic run or observation is not the same as
making a diagnostic-only finding cluster truth.

### Observation

A bounded record of observed input. Observations can come from local development
surfaces, provider reports, fixtures, imports, or operator statements. They are
not execution instructions.

### Evidence

Immutable material derived from observations or accepted imports that may support
facts. Evidence preserves source, observation time, payload, and provenance. It
is not itself a projected current belief.

### Fact

A projected claim about a subject, predicate, and value, with confidence,
freshness, and provenance. Facts may be observed, imported, or deterministically
inferred from other facts. They remain tied to evidence and source events.

### FactSupport

A rebuildable projection that groups supporting facts for the same subject,
predicate, and value. FactSupport is not appended as authoritative truth; it is
rebuilt from facts and evidence.

### FactConflict

A projected conflict between incompatible current fact values. Conflicts preserve
which facts, evidence, source types, confidence, and observation times produced
the disagreement.

### Entity

A projected thing Seed knows about, such as a host, service, repository,
environment, filesystem, endpoint, account, or other observed subject. Entity
identity and aliases must preserve provenance rather than hide source-specific
names.

### Relationship

A projected edge between entities, derived from facts or observations. Relationship
projection supports topology and reachability views without creating a second
source of truth.

### State projection

`ProjectionStore` caches current world-model snapshots rebuilt from the event
ledger. Projected state includes current facts, fact support, conflicts,
measurements, identity and alias indexes, entity types, relationships, graph
validation issues, and explanation inputs. The cache is deterministic and
rebuildable; it is not the source of truth.

### Capability testimony

Capability-related records currently serve as testimony about gaps, known or
reported capabilities, verification status, and availability boundaries where the
implementation exposes those surfaces. Catalog or recommendation presence does
not prove availability, verification, or execution permission.

### Provider recommendation testimony

Provider recommendation and ranking surfaces may describe possible external
providers or metadata. They are testimony and recommendation views, not Seed-owned
provider execution grammar, credential ownership, retry logic, scheduling, or job
lifecycle.

## Boundaries

Seed owns evidence-to-fact projection, provenance, conflict visibility, read-only
state views, diagnostics, and bounded capability/recommendation testimony where
backed by code.

Seed does not own arbitrary command execution, shell mutation, secret handling,
credential prompts, provider job lifecycle, workflow execution, replacement
operation registry, replacement runtime, replacement policy gate, replacement
action plan, or replacement handoff model.
