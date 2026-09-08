# Observer Capability Freshness Characterization

## Executive Answer

Seed currently has recurring implementation evidence for **state freshness**, **projection/cache freshness**, and **fact/evidence freshness**. It also has recurring implementation evidence for **bounded observation capability**: repository observers, structure observers, provider/discovery observation sources, capability inventories, and verification inspections.

However, the implementation evidence reviewed does **not** show a stable runtime distinction between:

```text
artifact changed
```

and

```text
observer changed
```

for previously observed repository artifacts.

Today, Seed knows when projected state has become stale relative to the event ledger, projection version, state projection version, state last event id, and fact expiry. It does not appear to know that an unchanged artifact deserves another observation pass merely because the observer has learned a new extraction capability.

The strongest supported answer is:

```text
Insufficient implementation evidence.
```

More precisely: there is sufficient evidence to characterize the existing freshness owners, and sufficient evidence to say that observer capability is represented as read-only collector/adapter/capability-inspection behavior. There is not sufficient implementation evidence that Seed already treats observer capability evolution as a freshness/invalidation input for unchanged artifacts.

## Implementation Evidence Reviewed

### Runtime projection and state freshness

- `StateProjector` owns rebuilding inspectable state from append-only ledger events. Its architecture metadata names the owner as `state_projection`, says it reads `EventLedger`, and says it produces projected `State`.
- `StateProjector.project_from_state()` states that event history remains the authority when applying ledger events to a projected state, including the incremental projection path.
- `ProjectionBuildDiagnostics` is explicitly optional and non-authoritative timing metadata for projected-state construction.
- `ProjectionStore` owns reusable projected-state snapshots, not event history. The store declares that snapshots are used when stale and that it loads/saves projected snapshots.
- `project_with_cache()` treats a cache hit as valid when the snapshot's `last_event_id` equals the current ledger `last_event_id` and the projection version matches the load request. Dependent read-model/index caches are keyed by state projection version and state last event id.

### Fact, observation, and evidence freshness

- `Observation` preserves source type, observed time, subject, predicate, value, confidence, metadata, dimensions, and optional expiry.
- `ObservationIngestor` records one observation as an `observation.observed` event, an `evidence.observed` event, and optionally a promoted fact event.
- Evidence created from an observation preserves observation id, source type, subject, predicate, value, metadata, dimensions, and `expires_at` in its payload.
- Fact freshness is implemented through optional `expires_at`; `is_fact_expired()` uses that timestamp and current time.
- `State.get_stale_facts()` returns facts that no longer influence projected state because of expiry, and `State.get_stale_fact_refresh_recommendations()` maps expired fact predicates to refresh capabilities.

### Repository and structure observation

- `RepositoryObservation` records repository-level git state including head commit, branch, dirty status, status availability, and mutation flags. It does not record observer capability identity or observer extraction version.
- `RepositoryArtifactObservationAdapter` extracts structural Python artifact facts from caller-provided text. Its boundary says it is read-only, structural, evidence-preserving, Python parsing, and not responsible for interpretation, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, or cluster mutation.
- The repository source observation source scans allowlisted Python roots and emits relationship observations for extracted imports and definitions. Its observation metadata includes `source_name`, `source_path`, evidence, relationship family, and repository root, but not observer capability version or extraction capability inventory.
- `StructureObservationBoundary` is a recurring owner for read-only structural extraction and non-interpretation. It owns a boundary, not a freshness lifecycle for changed observer capabilities.

### Provider/capability evidence

- Capability inventory is derived from projected registered tools, tool needs, and `capability_verified` facts. Missing verification facts produce `unverified`; expired verification facts produce `stale`.
- Capability inspection surfaces are read-only. The implementation audit records that capability candidate, verification, and promotion-readiness surfaces are not execution authority and that stale capability status comes from expired verification facts.
- This is capability status/fact freshness evidence, not evidence that provider or observer upgrades requalify unchanged repository artifacts for observation.

### Recovery and architectural reports

- `docs/current_implementation_audit_execution_observation_projection_cache_capability.md` explicitly characterizes projection caches as derived from event ledgers, dependent snapshots as keyed by projection version and state last event id, and cache invalidation sufficiency across all schema/semantic evolution as inferred but not proven.
- The same audit characterizes capability surfaces as read-only inspection derived from projected facts and existing evidence, not as execution authority or an observer-evolution trigger.
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md` distinguishes observation/evidence freshness, refresh need, recommendation, decision, command, and observation execution; it is documentation-only and does not introduce runtime semantics.

## Current Freshness Model

The current implementation-backed freshness model has three strong forms.

### 1. Projection/cache freshness

Responsibility belongs to projection cache and state projection code.

Authority is the event ledger plus projection version metadata. A state snapshot is reusable when it matches the requested projection version and ledger `last_event_id`. Dependent summary/index snapshots also have to match state projection version and state last event id.

Invalidation trigger is event-ledger movement, projection-version mismatch, invalid snapshot materialization, or related cache compatibility checks. The reviewed implementation did not show artifact mtime, artifact hash, observer version, or observer capability inventory as a projection-cache freshness key.

Consumers are state views, summary read models, fact indexes, diagnostics, and app surfaces that consume projected state.

Current owner: `StateProjector`, `ProjectionStore`, and dependent read-model/index cache helpers.

### 2. Fact/evidence freshness

Responsibility belongs to facts, fact support, and state freshness helpers.

Authority is the observation/fact timestamp and optional `expires_at`. A fact becomes stale when `is_fact_expired()` says the optional expiry timestamp has passed.

Invalidation trigger is time passing beyond `expires_at`, not artifact modification and not observer evolution.

Consumers include state queries, stale fact refresh recommendations, capability inventory stale verification status, and views that include or exclude expired facts.

Current owner: `seed_runtime.facts`, `State.get_stale_facts()`, `State.get_stale_fact_refresh_recommendations()`, and capability inventory logic for expired `capability_verified` facts.

### 3. Repository status freshness / artifact change visibility

Responsibility belongs to repository observation providers and source observation adapters.

Authority is the current repository/git status or the caller-provided source text at collection time. Repository state observation can report head commit and dirty/modified/staged/untracked counts. Source observation reads current files when collection is invoked and emits observations.

Invalidation trigger is not modeled as a durable artifact freshness lifecycle in the reviewed implementation. The app can observe current repository status, and collection can rescan files, but the reviewed code does not show a durable per-artifact freshness record keyed by source artifact identity and previous observation capability.

Consumers include repository-observation output, source-observation ingestion, observation inventory/diff flows, and downstream state projection after observations are recorded.

Current owner: `RepositoryObservationProvider`, `RepositorySourceObservationSource`, and repository artifact/relationship extraction helpers.

## Artifact Freshness Characterization

The repository has several artifact-adjacent signals:

- Git head/branch/dirty counts for repository state.
- Source path metadata on repository source observations.
- `dimensions={"path": relationship.path}` for repository relationship observations.
- Current source text parsing during explicit collection.
- Projection/cache freshness tied to ledger event identity after observations have been recorded.

These signals support the statement that Seed can observe repository state and source-derived facts. They do not support the stronger statement that Seed has a durable per-artifact freshness owner that can compare artifact identity/content against prior observation capability.

For unchanged artifacts, the reviewed implementation evidence shows no recurring durable field such as:

- observer id/version attached to prior artifact observations;
- extraction capability inventory attached to prior artifact observations;
- per-artifact observed-with metadata used for eligibility decisions;
- artifact observation completeness marker;
- provider upgrade event that targets old artifacts for re-observation.

Because those are not visible in the reviewed implementation, artifact freshness should be characterized narrowly: current repository/file observations can be collected, and resulting events update projected state; projection/cache freshness then follows the ledger. Artifact freshness as a persisted re-observation eligibility model is not established.

## Observer Capability Characterization

Observer capability exists as behavior and boundary metadata, not as a stable freshness dimension.

Implementation evidence includes:

- `ObservationSource` requires a source name, source type, and `collect()` method.
- `RepositorySourceObservationSource` has a stable `name` and emits metadata including `source_name`, path, evidence, relationship family, and repository root.
- `RepositoryArtifactObservationAdapterBoundary` records what the adapter does and does not own, including Python parsing, module/class/function/method/import observation, read-only behavior, and non-mutation.
- `StructureObservationBoundary` centralizes read-only structural-extraction vocabulary.
- Capability inventory and verification inspection represent operational capability status from projected facts and local evidence.

These surfaces identify current observer behavior and boundaries. They do not show observer capability as independently versioned runtime state, nor do they show a capability-evolution event that invalidates prior artifact observations.

## Comparison Between Artifact Freshness and Observer Capability Freshness

| Concept | Responsibility | Authority | Invalidation / staleness trigger | Consumer | Current implementation owner |
| --- | --- | --- | --- | --- | --- |
| Artifact Freshness | Narrowly: repository/git status and current source collection; not a durable artifact re-observation lifecycle | Current git status, current file text when collected, and subsequent ledger events | Explicit collection or repository/file changes visible to observer; no reviewed durable per-artifact stale marker | Repository observation output, observation ingestion, projected state | `RepositoryObservationProvider`, `RepositorySourceObservationSource`, repository extraction helpers |
| State Freshness | Build current inspectable state from events | Append-only event ledger | Replay over ledger events; event history remains authority | Runtime views, facts, relationships, summaries | `StateProjector` |
| Projection Freshness | Reusable snapshots of derived state | Projection version plus ledger `last_event_id`; dependent caches also use state projection version and state last event id | Version mismatch, ledger movement, invalid snapshot, full/incremental replay conditions | State cache users, summary read models, fact index | `ProjectionStore`, `project_with_cache()` |
| Observer Capability | Current collector/adapter behavior and read-only boundaries | Code implementation, source names, boundary dataclasses, capability/fact inventories | No reviewed freshness trigger for observer improvement; capability verification can be stale only through expired facts | Observation collection, structure/repository observation, capability inspection | `ObservationSource`, `RepositoryArtifactObservationAdapter`, `StructureObservationBoundary`, capability inventory/verification modules |
| Observation Provenance | Preserve source-attributed reported evidence | Observation fields, evidence payload, event ledger | New observations produce new events; optional fact expiry affects currentness | Evidence/fact projection, explanations, inventory/diff flows | `Observation`, `ObservationIngestor`, `Evidence`, event ledger |
| Repository Observation | Read-only repository status and source-derived structure/relationships | Git command output, caller-provided text, allowlisted source files | Explicit observation run; repository status may differ, but reviewed code does not persist observer-capability freshness | Diagnostics/app output and observation ingestion | `GitRepositoryObservationProvider`, `RepositorySourceObservationSource`, repository knowledge helpers |
| Provider Capability | Candidate/verification/inventory status | Projected package facts, registered tools, tool needs, `capability_verified` facts, local PATH metadata | Missing verification is `unverified`; expired verification fact is `stale` | Capability inventory, verification inspection, promotion readiness | `capability_inventory`, `capability_verification`, candidate/promotion-readiness modules |

## Counterexamples Reviewed

### Counterexample: artifact timestamp alone already solves observer evolution

Not supported by reviewed implementation evidence.

The repository source observer reads current files and repository observation reports git status, but the reviewed code does not show artifact timestamp/hash/commit identity joined with observer capability metadata to decide whether an unchanged artifact deserves re-observation after observer improvement.

### Counterexample: provider upgrades already trigger artifact re-observation

Not supported by reviewed implementation evidence.

Provider/capability surfaces represent candidates, verification evidence, inventory status, and stale verification facts. They do not show provider upgrade events that invalidate repository artifact observations or trigger re-observation eligibility for unchanged artifacts.

### Counterexample: existing observer metadata already tracks capability evolution

Partially supported only as static/boundary metadata; not supported as freshness/invalidation metadata.

Observation metadata records `source_name`, `source_path`, evidence, relationship family, and repository root. Adapter boundary objects record supported extraction types. These are useful provenance and boundary facts, but the reviewed implementation does not show them being versioned, compared against old observations, or used to mark prior observations incomplete.

### Counterexample: no recurring distinction between artifact freshness and observer freshness

Supported.

The implementation repeatedly distinguishes event/projection/fact freshness from read-only observation boundaries, but reviewed code and reports do not show a recurring owner that names observer capability freshness as a separate lifecycle. The current recurring distinctions are ledger/projection freshness, fact expiry, repository observation, structure observation, and capability verification status.

## Supported Conclusions

1. **Seed distinguishes state/projection freshness from observation/fact freshness.** Projection caches use event identity and version metadata; fact freshness uses optional expiry timestamps.

2. **Seed distinguishes observation provenance from projected claims.** Observation ingestion records observation events, evidence events, and optional fact events while preserving source metadata.

3. **Seed has bounded observer capability surfaces.** Repository, source, structure, and capability observers have explicit read-only boundaries and source metadata.

4. **Seed does not currently show implementation evidence that unchanged artifacts become stale because observer capability improved.** No reviewed implementation owner compares prior artifact observations against current observer extraction capability.

5. **If an observer gains new extraction capability, the runtime currently appears to know only if new observations are explicitly collected and ingested.** Once new observations are written to the ledger, normal state/projection freshness handles them. Before that collection, the reviewed implementation does not show an automatic or explicit eligibility signal for unchanged artifacts.

6. **Observer capability is currently owned by collector/adapter implementations and capability inspection surfaces, not by a freshness lifecycle.** Structure observation owns the shared read-only boundary; repository/source adapters own extraction behavior; capability inventory owns provider/verification status derived from facts.

7. **Artifact freshness is currently owned narrowly by repository/git observation, explicit source collection, and downstream ledger/projection freshness.** It is not shown as a durable artifact-observed-with-capability model.

## Unsupported Conclusions

The reviewed implementation does not support concluding that Seed already has:

- observer epochs;
- observer capability versions;
- automatic rescanning or background reprocessing;
- provider upgrade events that target old artifact observations;
- a durable incomplete-observation marker for unchanged artifacts;
- artifact observation eligibility caused by extraction-capability evolution;
- a stable owner bridging artifact freshness and observer capability freshness.

## Answers to the Recovery Questions

### 1. Does the repository already distinguish artifact freshness from observer capability freshness?

No stable implementation distinction was found. The repository distinguishes projection/event freshness, fact expiry freshness, repository observation, structure observation, and capability verification status. It does not show a recurring implementation owner for observer capability freshness over unchanged artifacts.

### 2. What implementation evidence supports that conclusion?

The evidence is negative and comparative: projection freshness keys on event id and projection version; fact freshness keys on `expires_at`; repository observations preserve git/source metadata; observer boundaries describe read-only extraction behavior. None of the reviewed owners compare prior artifact observations with current observer capabilities.

### 3. If an observer gains new extraction capability, how would the runtime currently know previously observed artifacts deserve another pass?

Based on reviewed implementation evidence, it would not know as a distinct runtime freshness condition. It would know only after an explicit observation run produces new observation/evidence/fact events; then normal ledger-driven projection freshness applies.

### 4. Who currently owns observer capability?

Current observer capability is distributed across source/adapter implementations and capability inspection surfaces:

- `ObservationSource` protocol and individual source classes own collection behavior.
- `RepositorySourceObservationSource` owns repository source relationship collection.
- `RepositoryArtifactObservationAdapter` owns deterministic Python artifact structural extraction from caller-provided text.
- `StructureObservationBoundary` owns the shared read-only structural extraction boundary.
- Capability inventory/verification modules own operational capability status derived from existing projected facts and local evidence.

### 5. Who currently owns artifact freshness?

Narrowly, repository observation providers and source observation sources own current repository/file observation, while projection/state owners handle freshness after observations become events. A durable per-artifact freshness owner was not found.

### 6. Does any recurring implementation owner already bridge these responsibilities?

No recurring bridge was found. Structure Observation bridges read-only structural extraction across substrates, and observation ingestion bridges observations into evidence/facts/events. Neither was found to bridge artifact freshness with observer capability evolution.

### 7. Is there sufficient implementation evidence to recognize a stable architectural boundary?

For the existing boundaries, yes: state/projection freshness, fact freshness, observation provenance, repository observation, structure observation, and provider capability status are all implementation-visible.

For **observer capability freshness of unchanged artifacts**, the answer is:

```text
Insufficient implementation evidence.
```

## Confidence

Confidence: **medium-high**.

Reason: the reviewed implementation and recovery reports repeatedly expose the existing freshness owners and their triggers. The absence of observer-capability freshness is supported by multiple negative comparisons across projection caching, fact expiry, repository/source observation metadata, structure observer boundaries, and capability verification status. Confidence is not absolute because the repository is large, but the searched terms and reviewed implementation areas match the requested investigation scope.
