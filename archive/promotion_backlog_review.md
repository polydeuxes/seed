# Executive Summary

This Promotion Backlog Review treats the selected audit documents as possible
sources of still-unpromoted architectural knowledge, not as archive candidates.
No documents should be archived before their remaining unique knowledge is either
promoted into a clear canonical owner or explicitly marked historical by that
owner.

Overall finding: the repository's documentation issue is lifecycle lag, not lack
of documentation. The reviewed audits contain a mix of already-promoted
canonical knowledge, implementation-era details that can become historical after
validation, and several still-useful promotion candidates.

Conservative summary:

- `docs/temporal_reasoning_audit.md` still contains the most precise temporal
  semantics for event append order, timestamp roles, current-vs-historical fact
  semantics, measurement history, stale read-time behavior, and
  `ProjectionStore` cache boundaries. Some of this has been promoted to
  `docs/state.md`, `docs/invariants.md`, `docs/reasoning_roadmap.md`, and the
  explanation vocabulary, but not at the same operational precision.
- `docs/contradiction_handling_audit.md` still contains the fullest inventory of
  projected conflicts, standalone contradictions, graph issues, stale/expired
  conflict participation, and why/why-not coverage. `docs/state.md` owns the
  canonical contradiction view, but it does not yet own all contradiction
  lifecycle terms.
- `docs/self_observation_audit.md` remains mostly roadmap/design material. Its
  unique knowledge is the repository-as-observation-source model, candidate
  architecture predicates/relationships/entity types, self-observation safety
  boundaries, and the distinction between generated architecture artifacts and
  ledger-backed observations.
- `docs/local_network_observation_audit.md` has partly been overtaken by Local
  Network Observation v1 and `docs/knowledge_acquisition_status.md`, but it
  remains valuable for local-network negative space, required distinctions,
  least-privileged source boundaries, and deferred predicate rationale.

Recommendation: do not archive any reviewed audit immediately. First promote a
small set of high-priority semantics into canonical owner documents, especially
state semantics, capability extension methodology, knowledge acquisition status,
and a future repository self-observation design note.

# Temporal Audit Review

## Unique knowledge remaining

`docs/temporal_reasoning_audit.md` remains the richest description of Seed's
current temporal behavior. Unique or more precise content includes:

- Event listing and projection order are append order / row insertion order, not
  event timestamp order.
- Timestamps on observations, evidence, facts, support, approvals,
  authorizations, projection snapshots, and evidence graph nodes are provenance,
  expiry, or cache metadata; they are not a supported projection-as-of API.
- Current state means the latest projection after replaying all workspace events
  and building derived indexes.
- Current fact selection is projection logic over projected state, not a full
  temporal reasoner.
- Durable single-cardinality values can remain retained and conflicting rather
  than being automatically deleted, superseded, or resolved.
- Measurement facts retain only the latest current sample in default projected
  state, while a bounded `measurement_history_limit` can expose debug history.
- Expired facts remain stored in projected state but are excluded from default
  support/current/conflict queries; stale is a read-time expiry view plus
  deterministic refresh recommendations, not mutation or confidence decay.
- `ProjectionStore` stores latest-current snapshots only and invalidates by
  latest event id mismatch, not timestamp comparison.
- Missing temporal concepts are specific: as-of event projection, as-of timestamp
  projection, belief timelines, why-then explanations, and semantic what-changed
  timelines.

## Already promoted

Promoted, but at a higher level:

- `docs/state.md` owns the EventLedger -> projected State -> read-only views
  model and describes State as a current world model.
- `docs/state.md` owns read-only Evidence Graph, Contradiction Detection, and
  Confidence Aggregation boundaries.
- `docs/invariants.md` owns projection invariants such as EventLedger as source
  of truth, `StateProjector` as projection owner, and `ProjectionStore` as cache
  rather than event owner.
- `docs/reasoning_roadmap.md` owns temporal reasoning as a roadmap area and
  recognizes that current support is append-only events, projected current state,
  fact timestamps, expiry, and stale refresh recommendations.
- `docs/explanation_contract_vocabulary.md` owns temporal metadata as part of
  explanation vocabulary and keeps temporal explanations scoped to current-state
  explanations until as-of support exists.
- `docs/knowledge_classification_vocabulary.md` owns stability classes that help
  distinguish identity, configuration, topology, description, and state facts,
  but it does not own projection ordering semantics.

## Should be promoted

Promote the following before archival consideration:

1. To `docs/state.md`: precise current-vs-historical fact semantics, including
   append-order projection, timestamp non-ordering, durable retention,
   measurement latest-current behavior, stale read-time filtering, and the lack
   of as-of query support.
2. To `docs/invariants.md`: compact projection invariants for append-order
   replay, timestamp non-ordering, latest-current-only `ProjectionStore`, and
   stale facts not mutating stored facts.
3. To `docs/reasoning_roadmap.md`: missing temporal capabilities should be
   framed as roadmap items only after characterization remains pinned: as-of
   event projection, as-of timestamp projection, why-then explanations, and
   what-changed timelines.
4. To `docs/explanation_contract_vocabulary.md`: explanation temporal metadata
   should explicitly avoid implying as-of projection unless a future as-of model
   is added.

## Can safely become historical

After the above promotions are made, the implementation-era portions of the audit
can become historical, especially the detailed characterization-test status and
long file-inspection narrative. The audit should not be archived before the
canonical owners carry the precise temporal semantics.

# Contradiction Audit Review

## Unique knowledge remaining

`docs/contradiction_handling_audit.md` still contains more precise contradiction
semantics than the canonical documents. Unique or more detailed content includes:

- Seed has multiple conflict-like surfaces: projection-level `FactConflict`,
  standalone contradiction audits, graph validation issues, explanation conflict
  attachments, and confidence-view contradiction penalties.
- Single-cardinality durable predicates can produce ambiguous current belief
  when supports tie; Seed does not choose a winner.
- Multi-cardinality durable predicates and measurement predicates should not be
  treated as contradictory merely because multiple values exist.
- Expired facts are stale, excluded from default conflicts/current belief, and
  available only through explicit include-expired query paths.
- Superseded exists for `ActionPlan` status, not for facts, supports, evidence,
  or conflicts.
- Why coverage is partial: `why()` can explain belief and ambiguity, but there is
  no first-class `why_not()` API and no unified conflict-explanation API that
  merges all conflict surfaces.
- Missing lifecycle vocabulary includes disputed, superseded-for-facts,
  uncertain as a first-class state, and normalized competing evidence.

## Already promoted

Promoted, but more compactly:

- `docs/state.md` owns Contradiction Detection v1 as a read-only projection view
  derived from projected State and optional Evidence Graph.
- `docs/state.md` already states that contradictions are not resolutions, do not
  choose winners, and prefer false negatives over noisy false positives.
- `docs/invariants.md` owns the invariant that contradiction detection must be
  read-only and must not mutate facts, append events, execute operations, or call
  providers.
- `docs/explanation_contract_vocabulary.md` owns terms such as competing fact,
  conflict, why-not explanations, selection rationale, replacement rationale,
  stale rationale, and temporal metadata.
- `docs/reasoning_roadmap.md` owns contradiction handling as a roadmap area and
  keeps conflict resolution out of scope.

## Should be promoted

Promote the following before archival consideration:

1. To `docs/state.md`: distinguish `FactConflict`, standalone `Contradiction`,
   graph issues, explanation conflict attachments, and confidence penalties as
   separate read-only surfaces rather than one conflict engine.
2. To `docs/state.md`: document cardinality-specific contradiction behavior:
   single-cardinality durable conflicts, multi-cardinality non-conflicts, and
   measurement latest-current non-conflicts.
3. To `docs/explanation_contract_vocabulary.md`: promote the lack of a
   first-class `why_not()` API and the absence of a unified
   conflict-explanation API as explicit current boundaries/future work.
4. To `docs/invariants.md`: add concise invariants that conflicts do not imply
   truth arbitration, confidence penalties do not mutate fact confidence, and
   expired facts do not participate in default conflicts.

## Can become historical

After promotion, the audit's file inventory, characterization-test details, and
implementation inventory can become historical. The contradiction lifecycle
terms should not become historical until their canonical owner explicitly defines
or rejects them.

# Self Observation Audit Review

## Unique concepts remaining

`docs/self_observation_audit.md` is still the primary source for repository
self-observation as an architecture concept. Unique knowledge includes:

- The architecture generator is close to a repository observation source in
  shape, but it currently emits generated architecture artifacts rather than
  `Observation`, `Evidence`, `Fact`, or projected relationships.
- `__seed_arch__` metadata, generated architecture graph edges, invariants, and
  rule inventories can serve as source-attributed repository evidence.
- Repository information maps naturally to Seed concepts if treated as an
  external source payload: static scan result as observation, raw graph node/edge
  as evidence, stable derived claim as fact, architecture edge as relationship,
  and documentation invariant as expected fact or rule.
- Candidate repository entity types include repository, file, module, class,
  service, runtime component, catalog, generated artifact, invariant, rule
  inventory entry, capability, tool/operation, and architecture owner.
- Candidate architecture relationships include `contains`, `defines`,
  `has_owner`, `in_layer`, `routes_to`, `route_limited_to`, `records_event`,
  `reads_from`, `writes_to`, `projects_to`, `validates_with`, `requires`,
  `may_execute`, `may_suggest`, `documents`, and `expects_absence`.
- Missing repository vocabulary includes a repository source type, repository
  predicates, repository entity types, architecture relationship catalog entries,
  source confidence policy, unreachable-component semantics, and experimental
  component classification.
- Strong safety boundaries: self-observation must not become self-modification,
  autonomous refactoring, self-rewriting, runtime mutation, execution triggering,
  or auto-fixing architecture drift.

## Absorbed knowledge

Already absorbed into canonical or near-canonical documents:

- `README.md` and `docs/architecture.md` own the high-level architecture and
  component-boundary narrative.
- `docs/invariants.md` owns current runtime, execution, projection, capability,
  verification, and quarantine invariants.
- Generated architecture artifacts and architecture-visualization docs own the
  current graph output and ownership visualization.
- `docs/reasoning_roadmap.md` owns self-observation as a future reasoning area.
- `docs/knowledge_acquisition_status.md` owns the current local knowledge
  acquisition board, but it does not yet include repository self-observation as a
  planned acquisition slice.

## Roadmap material

The following remains roadmap/design material rather than canonical current
behavior:

- Repository observation source contract.
- Minimal architecture predicate vocabulary, such as `architecture_owner`,
  `architecture_layer`, `repository_presence`, and `architecture_route`.
- Minimal architecture entity types, such as `module`, `class`,
  `runtime_component`, `catalog`, `generated_artifact`, and `invariant`.
- Minimal architecture relationships, such as `defines`, `has_owner`,
  `routes_to`, `requires`, `records_event`, and `documents`.
- Read-only semantic drift reports that compare observed repository facts with
  expected invariants.
- Repository source confidence/provenance policy.

## Belongs elsewhere

- Canonical architecture ownership belongs in `docs/architecture.md`,
  `docs/architecture_principles.md`, and `docs/invariants.md`.
- Self-observation roadmap and smallest safe design steps belong in
  `docs/reasoning_roadmap.md` or a new repository self-observation design note.
- Knowledge acquisition tracking for repository observation belongs in
  `docs/knowledge_acquisition_status.md` once accepted as planned work.
- Predicate/entity/relationship vocabulary belongs in the relevant catalog docs
  or a dedicated architecture-observation vocabulary document, not in the audit.

# Local Network Observation Audit Review

## Unique observation methodology remaining

`docs/local_network_observation_audit.md` contains methodology detail that is
partly more precise than the current canonical documents:

- Local network configuration facts must be sourced from least-privileged,
  read-only local files and stdlib APIs.
- Missing files, permission errors, unsupported platforms, malformed lines, or
  unknown encodings should omit that specific observation rather than failing the
  whole local host observation.
- First implementation should avoid shell commands, subprocesses, third-party
  packages, DNS lookups, UDP source-address tricks, TCP sockets, ICMP pings, ARP
  probes, HTTP calls, and Prometheus calls.
- Interface existence, operational state, assigned IP, default route, DNS
  resolver configuration, local network segment, and neighbor reachability are
  separate facts or non-facts.
- `unknown` reachability should be rendered from missing scoped evidence, not
  emitted as a discovered local fact.
- Suggested future tests focus on deterministic local readers, missing-file
  tolerance, no subprocess, no network calls, dimensions, no availability
  inference, and impact output preserving unknown availability.

## Unique local-network boundaries remaining

The audit remains the strongest local-network negative-space document:

- Interface `operstate=up` must not become `availability_status=up`.
- Assigned `ip_address` must not become endpoint availability or reachability.
- `default_gateway` must not become gateway reachability or internet access.
- `dns_resolver`, `dns_resolver_stub`, and `dns_resolver_upstream` must not become
  DNS availability.
- `local_network_segment` must not become neighbor existence.
- Lack of a local fact must not become `down`.
- Availability remains separate and requires separate scoped evidence.
- Local Network Observation v1 does not add Runtime behavior, ToolExecutor
  behavior, scheduling, retries, orchestration, shell commands, subprocess
  execution, privilege escalation, network scans, DNS queries, pings, ARP probes,
  endpoint checks, Prometheus calls, or other network connections.

## Already promoted

Promoted content includes:

- `docs/capability_extension_methodology.md` owns the capability-gap to
  question/evidence/fact/projection methodology, least-privileged source rules,
  read-only observation rules, non-inference rules, and local-observation
  examples.
- `docs/knowledge_acquisition_status.md` records Local Network Observation as
  implemented and lists the next planned local observation slices.
- `docs/availability_vocabulary_audit.md` owns availability vs local
  observability and reachability vocabulary boundaries.
- Current observation documentation and catalogs now own the v1 predicate set and
  implementation status.

## Should be promoted

1. To `docs/capability_extension_methodology.md`: preserve the local-network
   required distinctions and negative-space examples as a general methodology
   pattern for future observations.
2. To `docs/knowledge_acquisition_status.md`: capture deferred local-network
   follow-ups such as listening ports, local network segment, and neighbor cache
   observation, with explicit no-probe boundaries.
3. To `docs/availability_vocabulary_audit.md` or a future availability canonical
   vocabulary: promote the rule that local configuration facts do not imply
   availability, reachability, health, DNS success, internet access, or provider
   visibility.
4. To current observation docs: keep v1 source boundaries and no-shell/no-network
   constraints canonical for Local Network Observation.

## Now historical

The pre-implementation predicate proposal and recommended-smallest-implementation
steps are historical where Local Network Observation v1 has already implemented
or superseded them. The boundary rationale, deferred-predicate rationale, and
negative-space rules should remain active until promoted.

# Promotion Inventory

| Source | Target | Knowledge | Priority | Status |
| --- | --- | --- | --- | --- |
| `temporal_reasoning_audit.md` | `docs/state.md` | Current state is latest projection after append-order replay, not timestamp-order replay. | High | Not promoted at full precision |
| `temporal_reasoning_audit.md` | `docs/state.md` | Timestamps are provenance/expiry/cache metadata, not projection-as-of semantics. | High | Partially promoted |
| `temporal_reasoning_audit.md` | `docs/state.md` | Durable facts are retained; old/conflicting values are not automatically deleted, superseded, or resolved. | High | Partially promoted |
| `temporal_reasoning_audit.md` | `docs/state.md` | Measurement predicates keep latest current sample by default while bounded debug history can be retained. | High | Not promoted at full precision |
| `temporal_reasoning_audit.md` | `docs/state.md` | Expired facts remain stored but are excluded from default support/current/conflict queries. | High | Partially promoted |
| `temporal_reasoning_audit.md` | `docs/invariants.md` | Staleness is a read-time expiry view and refresh recommendation path, not fact mutation or confidence degradation. | High | Not promoted at invariant precision |
| `temporal_reasoning_audit.md` | `docs/invariants.md` | `ProjectionStore` is latest-current cache only and invalidates by latest event id mismatch, not timestamps. | High | Partially promoted |
| `temporal_reasoning_audit.md` | `docs/reasoning_roadmap.md` | Missing temporal capabilities: as-of event/timestamp projection, belief timelines, why-then explanations, what-changed timelines. | Medium | Partially promoted |
| `temporal_reasoning_audit.md` | `docs/explanation_contract_vocabulary.md` | Explanation temporal metadata must not imply as-of support. | Medium | Partially promoted |
| `contradiction_handling_audit.md` | `docs/state.md` | Conflict-like surfaces are separate: `FactConflict`, standalone `Contradiction`, graph issue, explanation attachment, confidence penalty. | High | Not promoted at full precision |
| `contradiction_handling_audit.md` | `docs/state.md` | Single-cardinality durable conflicts can become ambiguous; multi-cardinality values and measurements are not conflicts merely by multiplicity. | High | Partially promoted |
| `contradiction_handling_audit.md` | `docs/state.md` | Expired facts are excluded from default conflicts/current belief and only included by explicit include-expired paths. | High | Partially promoted |
| `contradiction_handling_audit.md` | `docs/explanation_contract_vocabulary.md` | `why()` can expose ambiguity, but there is no first-class `why_not()` or unified conflict-explanation API. | Medium | Partially promoted |
| `contradiction_handling_audit.md` | `docs/invariants.md` | Contradiction penalties are read-only confidence-view effects and do not mutate facts or arbitrate truth. | High | Partially promoted |
| `contradiction_handling_audit.md` | `docs/reasoning_roadmap.md` | Missing lifecycle concepts: fact supersession, disputed, uncertain as first-class state, normalized competing evidence. | Medium | Partially promoted |
| `self_observation_audit.md` | `docs/reasoning_roadmap.md` | Repository self-observation should begin as a design document, not ingestion or runtime behavior. | High | Partially promoted |
| `self_observation_audit.md` | New repository self-observation design note | Repository scan result -> observation, graph node/edge -> evidence, stable claim -> fact, architecture edge -> relationship. | High | Not promoted |
| `self_observation_audit.md` | New architecture-observation vocabulary | Candidate predicates/entity types/relationships for architecture facts. | High | Not promoted |
| `self_observation_audit.md` | `docs/invariants.md` | Self-observation must not self-modify, self-rewrite, trigger execution, mutate runtime, or auto-fix drift. | High | Partially promoted |
| `self_observation_audit.md` | `docs/knowledge_acquisition_status.md` | Repository observation is not yet implemented and could be tracked as a planned documentation/design slice if accepted. | Medium | Not promoted |
| `local_network_observation_audit.md` | `docs/capability_extension_methodology.md` | Local observation pattern: tolerate missing local files, emit narrow facts only, preserve dimensions, no probe/no shell/no network. | High | Partially promoted |
| `local_network_observation_audit.md` | `docs/capability_extension_methodology.md` | Required distinctions among interface existence, operstate, IP assignment, route, resolver config, segment, and reachability. | High | Not promoted at full precision |
| `local_network_observation_audit.md` | `docs/availability_vocabulary_audit.md` | Local configuration facts never imply availability, reachability, DNS success, internet access, provider visibility, or host health. | High | Partially promoted |
| `local_network_observation_audit.md` | `docs/knowledge_acquisition_status.md` | Deferred local-network slices: local segment and neighbor cache/reachability vocabulary, with no-probe boundaries. | Medium | Partially promoted |
| `local_network_observation_audit.md` | Current observation docs/catalog docs | Local Network Observation v1 source boundaries and predicates should remain canonical after implementation. | Medium | Partially promoted |

# Archive Readiness Reassessment

| Document | Classification | Why |
| --- | --- | --- |
| `docs/temporal_reasoning_audit.md` | PROMOTE THEN ARCHIVE | It still contains high-priority temporal semantics not promoted at full precision, especially append-order projection, timestamp non-ordering, measurement history, stale read-time behavior, and `ProjectionStore` temporal boundaries. |
| `docs/contradiction_handling_audit.md` | PROMOTE THEN ARCHIVE | It still contains high-priority contradiction lifecycle detail across multiple conflict surfaces, cardinality behavior, stale participation, and explanation gaps. |
| `docs/self_observation_audit.md` | KEEP ACTIVE | It remains the active design source for repository self-observation. Much of its content is roadmap material rather than obsolete implementation history. |
| `docs/local_network_observation_audit.md` | PROMOTE THEN ARCHIVE | Parts are historical after Local Network Observation v1, but negative-space boundaries, source-safety methodology, and deferred predicate rationale should be promoted first. |

# Canonical Ownership Validation

| Topic | Canonical Owner | Clear? |
| --- | --- | --- |
| Temporal projection order | `docs/state.md` plus compact invariants in `docs/invariants.md` | Ambiguous until append-order/timestamp non-ordering is promoted |
| Current-vs-historical fact semantics | `docs/state.md` | Partially clear |
| Temporal roadmap/as-of queries | `docs/reasoning_roadmap.md` | Clear |
| Temporal explanation metadata | `docs/explanation_contract_vocabulary.md` | Partially clear |
| Staleness and expiry semantics | `docs/state.md` plus `docs/invariants.md` | Partially clear |
| `ProjectionStore` temporal role | `docs/state.md` plus `docs/invariants.md` | Partially clear |
| Contradiction detection v1 | `docs/state.md` | Clear for v1, incomplete for lifecycle detail |
| Contradiction invariants/non-resolution | `docs/invariants.md` | Clear |
| Why-not and unified conflict explanation vocabulary | `docs/explanation_contract_vocabulary.md` | Partially clear |
| Fact supersession/disputed/uncertain lifecycle | `docs/reasoning_roadmap.md` until accepted vocabulary exists | Ambiguous |
| Repository self-observation roadmap | `docs/reasoning_roadmap.md` or a new repository self-observation design note | Ambiguous |
| Architecture ownership facts | `docs/architecture.md`, `docs/architecture_principles.md`, and `docs/invariants.md` | Partially clear |
| Repository observation source contract | New repository self-observation design note | Not clear |
| Repository predicates/entity types/relationships | New architecture-observation vocabulary or catalog documentation | Not clear |
| Local observation methodology | `docs/capability_extension_methodology.md` | Clear |
| Local-network observation implementation status | `docs/knowledge_acquisition_status.md` plus current observation docs | Clear |
| Availability vs reachability vocabulary | `docs/availability_vocabulary_audit.md` until promoted to canonical vocabulary | Partially clear |
| Local-network deferred predicates | `docs/knowledge_acquisition_status.md` or future local-network design note | Partially clear |

# Risks

## Knowledge that could be lost

- Precise append-order-vs-timestamp projection semantics could be lost if the
  temporal audit is archived before promotion.
- Measurement latest-current and debug-history behavior could be mistaken for
  normal durable fact history without the audit.
- Stale fact behavior could be misread as mutation, confidence degradation, or
  event emission if not promoted as an invariant.
- The distinction among `FactConflict`, standalone contradictions, graph issues,
  explanation conflict attachments, and confidence penalties could collapse into
  an inaccurate single-conflict-engine mental model.
- Repository self-observation safety boundaries could be lost, increasing risk
  that future work jumps directly to ingestion, mutation, or self-repair.
- Local-network negative-space rules could be lost, especially the rule that
  local configuration is not availability or reachability evidence.

## Duplicate truth

- Temporal semantics currently live in both the temporal audit and several
  canonical documents, but at different levels of precision.
- Contradiction semantics live in the contradiction audit, `docs/state.md`, the
  explanation vocabulary, roadmap, and invariants.
- Local-network methodology lives in the local-network audit, capability
  extension methodology, availability vocabulary, and knowledge acquisition
  status.
- Architecture ownership lives in generated graph artifacts, README,
  architecture docs, invariants, and self-observation audit.

## Promotion gaps

- No canonical state section explicitly owns all current-vs-historical fact
  semantics.
- No canonical contradiction lifecycle section unifies current conflict surfaces
  without implying resolution.
- No canonical repository self-observation design document exists.
- No canonical architecture-observation vocabulary exists for repository-derived
  predicates, entity types, relationships, confidence policy, or provenance.
- Availability vocabulary is still audit-shaped, so its canonical ownership is
  less clear than methodology or state ownership.

## Premature archive risks

- Archiving `docs/temporal_reasoning_audit.md` now could remove the only precise
  temporal behavior inventory.
- Archiving `docs/contradiction_handling_audit.md` now could remove key
  lifecycle and cardinality boundaries.
- Archiving `docs/self_observation_audit.md` now would be premature because its
  main content is not historical; it is a pending design backlog.
- Archiving `docs/local_network_observation_audit.md` now could remove the
  negative-space rationale that prevents future local observation from becoming
  network probing or availability inference.

## Outdated audit content

- Local Network Observation v1 implementation makes some pre-implementation
  predicate proposal and implementation-step sections historical.
- Temporal and contradiction audits mention characterization status; those parts
  are less important than the semantic findings once canonical docs own the
  behavior.
- Self-observation remains explicitly non-implemented; it should not be mistaken
  for current system capability.

# Recommended Next Step

Do one small canonicalization pass before any archive planning:

1. Promote temporal current-vs-historical semantics into `docs/state.md` and add
   compact projection invariants to `docs/invariants.md`.
2. Promote contradiction lifecycle boundaries into `docs/state.md` and add any
   missing non-resolution invariants to `docs/invariants.md`.
3. Create or plan a repository self-observation design note that owns the
   repository observation source contract, architecture vocabulary, provenance,
   drift-report boundaries, and non-goals.
4. Promote local-network negative-space examples into
   `docs/capability_extension_methodology.md` and availability boundaries into
   the availability vocabulary owner.
5. Only after those promotions, reassess whether the reviewed audits should move
   from active audit documents to historical references.
