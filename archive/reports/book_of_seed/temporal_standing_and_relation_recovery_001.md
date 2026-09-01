# Temporal Standing and Relation Recovery 001

## Status and scope

This is a report-only constitutional recovery. It does not amend the canonical Book, production code, schemas, timestamp fields, predicate behavior, projection behavior, or view behavior. Recovery and amendment records are treated here as testimony and amendment history; canonical force remains with the amended Book chapters.

## Sources inspected

### Canonical Book territory

Inspected the requested canonical chapters and nearby Book records:

- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
- `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`
- `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md`
- `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `book_of_seed/06-state-and-projection/events-facts-and-state.md`
- `book_of_seed/06-state-and-projection/projection-and-current-state.md`
- `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`
- `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md`
- `book_of_seed/concordance.md`
- `book_of_seed/unresolved.md`
- `book_of_seed/post_tool_corridor_directional_topology_recovery_001.md`
- `book_of_seed/claim_normalization_and_fact_standing_recovery_001.md`
- `book_of_seed/claim_normalization_and_fact_standing_amendment_001.md`

Book-level governing findings recovered:

- Artifact representation and constitutional standing are distinct; a normalized fact-shaped artifact may preserve a claim in Fact vocabulary without proving Fact standing.
- Constructor occurrence, act occurrence, consumer uptake, projection, and view formation are separately warranted boundaries.
- A lens or view faithfully exposes selected source material under method and scope; it does not change upstream standing or manufacture missing provenance, occurrence, or temporal dimensions.
- Material may be applicable, admitted, and consumed at separate consumer-local boundaries.
- Event ledger preservation and state projection are distinct from truth establishment, currentness, and consumer reliance.

### Historical temporal doctrine inspected

Inspected the requested historical documents:

- `docs/temporal_reasoning_audit.md`
- `docs/event_and_change_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`

Lineage characterization:

- The earliest focused temporal doctrine is `docs/temporal_reasoning_audit.md`; it established the main distinctions among event ordering, event timestamps, observation time, fact time, freshness, expiry, measurement selection, historical replay, and projection-cache limits.
- `docs/event_and_change_reconciliation.md` repeated and broadened the event/change distinction: append order and change records can preserve sequence and occurrence evidence without proving causal topology.
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md` and `docs/knowledge_maintenance_reconciliation.md` repeated and operationalized freshness/staleness as integrity and refresh concerns.
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`, `docs/corroboration_and_fact_promotion_reconciliation.md`, and `docs/fact_confidence_and_corroboration_reconciliation.md` repeated temporal support concerns while distinguishing claim strength, corroboration, and confidence from truth.
- `docs/evidence_trust_and_source_authority_reconciliation.md` preserved source authority/trust boundaries relevant to source time, but authority and trust do not make source time true.
- `docs/operator_interface_and_projection_authority_reconciliation.md` repeated projection time, current selection, and operator disclosure duties; it is projection-interface doctrine, not a producer amendment.
- `docs/knowledge_lifecycle_reconciliation.md` repeated a documentation-level lifecycle and explicitly warned against turning concern order into a runtime pipeline. Any language depending on an internal execution corridor or universal lifecycle remains only historical residue after the amended Fact-standing grammar.

### Current implementation witnesses inspected

Inspected the requested production files:

- `seed_runtime/events.py`
- `seed_runtime/observations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/evidence.py`
- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/confidence.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/explanations.py`
- `seed_runtime/predicate_catalog.py`

Focused temporal test witness inspected:

- `tests/test_temporal_characterization.py`

Other inspected test witnesses by targeted search included tests covering observation normalizers, relationship catalog projection, capability verification inspection, state views, evidence graph, confidence, contradictions, explanations, and downstream interpretation admission.

## Primary finding

Under the amended Book grammar, Seed currently supports several temporal standings, but it does not support one universal temporal sequence and does not record every requested time independently.

The repository currently preserves implementation evidence for:

1. ledger append sequence;
2. event timestamp;
3. observation/evidence/fact `observed_at` as copied or supplied observation time;
4. optional `expires_at` as expiry comparison input;
5. support-group earliest and latest observation times;
6. projection snapshot creation time and last input event boundary;
7. current-selection outputs derived by projection rules;
8. verification-like predicates and views in focused capability surfaces, with method/scope limits.

The repository does not generally preserve independent fields for source occurrence time, receipt time, translation time, normalized-at time, Fact-establishment time, projection-consumption time, external realization time, response-production time, or consumer reliance occurrence. These are Unknown unless a specific producer records them as payload metadata or event material.

## Required non-equivalences tested

| Non-equivalence | Recovery finding |
| --- | --- |
| `occurred_at != observed_at` | Supported constitutionally. Implementation usually has `observed_at`, not a generic occurrence timestamp. Event/act occurrence may be evidenced by a producer boundary or ledger event rather than by `observed_at`. |
| `observed_at != received_at` | Supported as a forbidden inference. No general `received_at` field exists for observations, evidence, or facts. |
| `received_at != recorded_at` | Supported. Receipt is not generally recorded; ledger append and event timestamp are recording-adjacent but not receipt. |
| `recorded_at != normalized_at` | Supported. Observation-to-evidence/fact conversion copies `observed_at`; no separate normalized-at is recorded. |
| `normalized_at != established_at` | Supported by amended Fact-standing grammar. Implementation compresses fact artifact production and support preservation; independent establishment time is absent. |
| `established_at != projected_at` | Supported. Projection snapshots have creation time and last event boundary; facts do not acquire establishment time from snapshots. |
| `projected_at != consumed_at` | Supported. Projection store records snapshot `created_at`; consumer uptake is generally not recorded. |
| `event timestamp != ledger order` | Directly tested: projection follows append order and out-of-order event timestamps do not reorder state. |
| `earlier != causal` | Supported by Book topology. Causation IDs and correlation IDs can preserve links, but chronology alone is insufficient. |
| `latest != current` | Partially implemented as unsafe. Measurement projection selects latest observed sample as current sample, but this is view/predicate policy, not universal current standing. |
| `fresh != sufficient` | Supported by authority/trust/consumer-local boundaries. Non-expired material may still lack scope, authority, trust, or purpose fit. |
| `stale != false` | Implemented. Expired/stale facts are retained and can be reopened with `include_expired=True`. |
| `expired != historically invalid` | Implemented. Expiry filters current support by default; it does not delete ledger or projected retained facts. |
| `preserved != currently applicable` | Implemented and constitutional. Ledger/preserved facts can outlive current selection. |
| `replayed now != occurred again` | Supported. State projector replays events into derived state; replay does not append new event occurrence. |
| `projection time != source time` | Supported. Projection snapshot creation time differs from observed/source time and last event created time. |
| `request time != external realization time` | Unresolved egress producer. Must not be inherited automatically. |
| `response time != ingress time` | Unresolved egress/return boundary. Must not be inherited automatically. |

## 1. Temporal vocabulary lineage

| term | governing source | original meaning | current implementation witness | constitutional standing | remaining ambiguity |
| --- | --- | --- | --- | --- | --- |
| occurrence | Canonical acts and constructors chapters; earliest temporal audit for event occurrence | A bounded act, condition, report, or crossing happened, distinct from an artifact saying so | Event append, producer return, causation/correlation IDs, observation event kinds | Constitutional only when evidenced by responsible boundary or preserved record | Many artifacts omit direct occurrence evidence |
| sequence | Canonical roads/lenses chapter; temporal audit | One material/act preceded another | `EventLedger.list()` returns append order; SQLite orders by rowid | Ledger sequence is preserved order, not causation | Cross-ledger and external sequence mostly Unknown |
| `observed_at` | Observation/evidence/fact implementation; temporal audit | Time the observation or producer testimony says it observed | `Observation`, `Evidence`, `Fact`, `FactSupport`, relationships | Implementation witness; constitutionally testimony time unless producer-specific evidence says more | Overloaded by producers; sometimes caller-supplied, collection time, source sample time, or imported time |
| recorded time | Event/recording doctrine | Time Seed preserved material | Event timestamp and append order; projection snapshot `created_at` | Partially recorded for events/snapshots | Observation/evidence/fact artifact recording time not independently represented except via containing event |
| event time | Event model and ledger doctrine | Timestamp carried by event | `Event.timestamp` default and SQLite `timestamp` column | Recording-adjacent event metadata, not ledger order | Can be externally constructed and out of append order |
| ledger order | Event ledger doctrine | Append order of preserved events | in-memory list order; SQLite rowid order | Explicit sequence for projection input | Not causal and not source chronology |
| Fact time | Fact model and fact-promotion doctrine | `observed_at` copied from observation into fact artifact | `Fact.observed_at` | Fact artifact testimony/support time; not independent establishment time | May describe sample/observation/import depending on producer |
| projection time | Projection doctrine and projection store | Time a projection snapshot was built/saved | `ProjectionSnapshot.created_at`; `last_event_id`; `last_event_created_at` | Projection-local boundary | Non-cached direct projections may not expose build time |
| current | State projection doctrine | Selected present-facing view under projection rules | `get_best_fact`, `get_current_facts`, current-support projection | Projection-local or consumer-local standing | Current enough for purpose remains consumer judgment |
| freshness | Observation refresh and knowledge maintenance doctrine | Support recent enough for purpose | `expires_at`, stale recommendations, include-expired filters | Consumer-relative integrity judgment, partially implemented by expiry | Freshness windows and source guarantees not generally modeled |
| staleness | Temporal audit and maintenance docs | Material no longer current enough or expired | `is_fact_expired`, `get_stale_facts` | Projection/integrity signal, not falsity | Stale due to age without `expires_at` often Unknown |
| expiry | Fact model and temporal tests | Optional timestamp after which fact is filtered from default current support | `Fact.expires_at`; `FactSupport.expired`; stale recommendations | Ends default current-support eligibility, not preservation | Whether it ends verification/current permission by purpose is not universal |
| latest | Measurement semantics and support projection | Chronologically greatest `observed_at` sample in a group | measurement support `current_sample`; `latest_observed_at` | Predicate/view-local selection evidence | Latest does not prove fresh, true, or sufficient |
| historical | Temporal audit and ledger doctrine | Preserved material remains recoverable after current applicability ends | append-only ledger, retained durable facts, include-expired reopening | Historical preservation standing | Historical validity interval is often unrepresented |
| verification time | Capability verification docs/tests and predicate facts | Method-, scope-, and time-specific confirmation | Verification records/predicates in capability surfaces | Verified standing is bounded and not universal truth | General independent verification timestamp is not part of Fact model |
| causation | Events and topology doctrine | One act produced or motivated another | `causation_id`, `correlation_id` fields on events | Explicit links may support causal inquiry; chronology alone does not | Semantics of links are local and not universal proof |

## 2. Temporal field inventory

| artifact or record | field | producer | literal implementation meaning | consumer usage | constitutional interpretation | unsafe inference |
| --- | --- | --- | --- | --- | --- | --- |
| `Event` | `timestamp` | Event constructor / ledger append / externally built event | Event-carried datetime | Stored, serialized, used as snapshot `last_event_created_at` | Event metadata; may witness recording or supplied event time | That ledger order follows timestamp; that source occurrence happened then |
| `Event` | append position / SQLite rowid | Ledger storage | Preservation order | Projection replay order | Explicit ledger sequence | Causation; external chronology |
| `Event` | `causation_id` | Caller/ingestor | Claimed causal parent id | Trace linkage | Link evidence requiring local interpretation | Chronology alone or ID presence proves causation truth |
| `Event` | `correlation_id` | Caller/ingestor | Claimed correlation group | Trace grouping | Association evidence | Production or causal dependency |
| `Observation` | `observed_at` | Observation source/caller | Supplied collection/testimony time | Copied to Evidence and Fact | Observation-time testimony | Receipt, source occurrence, recording, normalization, currentness |
| `Observation` | `expires_at` | Observation source/caller | Optional expiry copied forward | Fact expiry filtering later | Applicability/storage-lifetime clue for default current support | Historical invalidity after expiry |
| `Evidence` | `observed_at` | `ObservationIngestor.observation_to_evidence` or direct constructor | Copied observation `observed_at` | Evidence provenance display/support | Evidence testimony time inherited from observation | Evidence recording time or independent source time |
| `Fact` | `observed_at` | `ObservationIngestor.observation_to_fact`, direct constructor, inference code | Copied/supporting observation time or supplied fact time | Sorting, support aggregation, measurement latest selection, best-fact tie-break | Fact artifact's supported observation/sample time | Fact establishment time, current applicability, artifact production time |
| `Fact` | `expires_at` | Observation source/direct constructor | Optional expiry | Default support/conflict/current filtering and stale recommendations | Current-support eligibility boundary in implementation | Deletion, falsity, historical invalidity, universal permission end |
| `FactSupport` | `observed_at` | State support projection | Earliest support time for durable, selected sample time for measurement | Support views, evidence graph | Support-window lower bound or sample time | Establishment time for support group |
| `FactSupport` | `latest_observed_at` | State support projection | Latest support time or sample time | Support display/selection | Latest support evidence | Currentness, freshness sufficiency, consumer permission |
| `FactSupport` | `expired` | State support projection | Expiry state under now-comparison | Filtering/display | Projection-time expiry signal | Claim falsehood |
| `FactSupport` | `expires_at` | State support projection | For durable support, max expiry only if all supports expire; for measurement, sample expiry | Display/filtering | Group expiry clue | Universal standing end |
| `FactConflict` | none temporal | State conflict projection | Values and selected winner without times | Conflict views | Conflict relation lacks temporal scope | That conflicts are or are not temporal succession |
| `EntityRelationship` / alias / legacy relationship | `observed_at` | Relationship projection from fact | Copied fact observed time | Relationship provenance | Source fact observation time | Relationship establishment or current applicability |
| `ProjectionSnapshot` | `created_at` | Projection store | Snapshot creation/save time | Cache freshness/status | Projection-local build/recording time | Source time or consumer time |
| `ProjectionSnapshot` | `last_event_id` | Projection cache | Last event in input ledger order | Cache invalidation boundary | As-of event boundary by append sequence | Historical as-of API or source-time boundary |
| `ProjectionSnapshot` | `last_event_created_at` | Projection cache | Timestamp of last input event | Status/debug | Event-time clue | Append order or source chronology |
| `SummaryProjectionSnapshot` / derived index | `created_at` | Projection store | Snapshot/index creation time | Cache reuse | Projection-local recording time | Upstream claim time |
| `ObservationView` | no observed time | State view builder | Summary and supporting event IDs only | Public observation-facing view | View hides observation time unless support reopened | That summary is current or temporally scoped |
| `FactView` | `observed_at`, `latest_observed_at`, `expires_at`, `expired` | State view builder | Support-derived times and expiry | Public fact-facing view | View-local support temporal disclosure | Establishment time or universal currentness |

## 3. Temporal boundary table

| upstream subject | upstream temporal standing | boundary | required temporal evidence | temporal act or judgment | downstream temporal standing | what is preserved | what is reset or newly established | forbidden inference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| External material | Source may describe occurrence/sample/validity time | External material to ingress | Source payload, provenance, authority, receipt/translation evidence if available | Determine what the source claims and what Seed actually received | Ingress testimony with Unknowns | Source-provided temporal claims if copied into metadata/dimensions/payload | Seed receipt/translation standing if recorded | Receipt time substitutes for occurrence/source time |
| Ingress material | Received or imported representation | Ingress to Observation | Producer-specific collection/import rules | Observation production | Observation-time testimony | `observed_at`, payload metadata, dimensions, expiry | Observation artifact and event occurrence if ledger-recorded | `observed_at` has one universal meaning |
| Observation | Observation `observed_at` and optional expiry | Observation to Evidence | Observation identity/provenance | Preserve testimony as Evidence | Evidence support time inherited from observation | Observation id, source type, subject/predicate/value, metadata, expiry in payload | Evidence artifact id and ledger event if recorded | Evidence time is independent recording time |
| Observation/Evidence | Supported fact-shaped values | Observation to Fact artifact | Evidence id, observation confidence, source type | Normalize into fact-shaped artifact | Fact artifact with observed support time | Subject, predicate, value, dimensions, evidence ids, observed_at, expires_at | Fact artifact id; inferred flag | Fact artifact has Fact standing or current standing automatically |
| Claim | Semantic proposition | Claim normalization | Identity, scope, dimensions, predicate semantics, value representation | Canonical representation without standing | Normalized claim representation | Canonical subject/predicate/value/dimensions | Representation equality | Temporal scope omitted from normalization is safely recoverable later |
| Fact artifact | Normalized fact-shaped record with support links | Fact establishment | Valid support, scope, authority, conflict-aware boundary | Establish bounded Fact standing | Fact standing, if boundary is evidenced | Claim/support/provenance | Standing, if established | Artifact production time equals establishment time |
| Fact supports | Repeated observations over time | Support aggregation | Predicate semantics, grouping key, expiry, support facts | Aggregate durable support or choose measurement sample | Support standing for projection | Earliest/latest observed support, supporting ids | Confidence/support group | Latest equals current enough or best supported globally |
| Preserved facts/events | Historical event/fact material | Projection/View formation | Ledger order, projection method, filters, predicate catalog | Build current/historical-facing view | Projection-local current selection | Event/fact ids, selected support times | Projection snapshot `created_at` where cached | Projection time equals source or Fact time |
| View/projection | Projected material under method | Consumer uptake | Purpose, authority, freshness, expiry, conflict, scope | Applicability/admission/consumption judgment | Consumer-local temporal applicability | Support links may be reopened | Consumer standing, if recorded by consumer boundary | Public view fields prove lawful reliance |
| Verification evidence | Method/scope/time-limited verification result | Verification uptake | Verification method, target, observation/evidence time, freshness rules | Confirm or qualify claim for purpose | Verified standing | Verification support and scope | Verified status for method/scope/time | Verification remains current indefinitely |
| Requirement/request | Need or initiating view time | Egress/external return | Request formation/emission, external receipt/realization, response, ingress evidence | Preserve returned testimony as new ingress | New Observation/Testimony if recorded | Requirement/request links if represented | New observation boundary | Returned observation inherits initiating view/request time |

## 4. Temporal relation matrix

| relation | standing in repository |
| --- | --- |
| occurrence | Derived or explicit when a producer boundary/event is recorded; otherwise Unknown |
| sequence | Explicitly recorded for ledger append order; derived for causation/correlation; unsupported across external systems without evidence |
| source time | Historical doctrine only or payload-specific; not a universal field |
| observation time | Explicitly recorded as `observed_at`, but producer-specific and overloaded |
| receipt time | Unsupported generally; Unknown unless payload metadata records it |
| recording time | Explicit for events/snapshots via event timestamp/snapshot `created_at`; derived from append order; not independently stored for Observation/Evidence/Fact artifacts |
| normalization time | Unsupported generally; Unknown |
| Fact establishment time | Unsupported independently; compressed with artifact/event/support boundary or Unknown |
| projection time | Explicit for cached snapshots; derived/Unknown for direct projection objects unless diagnostics/status expose it |
| consumption time | Consumer-local and generally unrecorded; Unknown |
| applicability interval | Consumer-local/historical doctrine; partially represented by `expires_at` and dimensions; no general validity interval |
| freshness/staleness | Projection-local expiry comparison and consumer-local judgment; historical doctrine for broader freshness |
| expiry | Explicitly recorded as optional `expires_at`; interpretation is projection/current-support filtering unless a local boundary says more |
| preservation horizon | Explicit by append-only ledger and retained facts; projection measurement retention is limited but ledger remains |
| renewal | Derived; new evidence may add support, create new sample, or establish new current selection depending on predicate and boundary |
| causation | Explicit link fields exist, but causal proof is local; chronology alone unsupported |

## 5. Clock and ordering comparison

| clock/order | repository support | skew/absence/replay risk |
| --- | --- | --- |
| Source clock | Payload/metadata-specific only | Source time may be absent, ambiguous, untrusted, skewed, or collapsed into `observed_at` |
| Observer clock | `observed_at` from observation producers | May be caller-supplied, collection-time, import-time, adapter-time, or sample-time |
| Seed process clock | Used for defaults such as `datetime.now(timezone.utc)` in sources, events, expiry comparison, snapshots | Process clock skew changes event timestamps, observed defaults, snapshot `created_at`, and expiry status |
| Event timestamp | Event model field | Externally constructed events can carry timestamps out of append order |
| Ledger append order | In-memory list / SQLite rowid | Preserves Seed recording order but not causation or source chronology |
| Projection build time | Snapshot `created_at` where cached | Direct projections may lack public build time; replay now does not mean source recurrence |
| Consumer time | Consumer-local, generally unrecorded | Different consumers or calls may make different freshness/applicability judgments |
| External service time | Unresolved egress/ingress-specific | Request, external receipt, realization, response production, response receipt, and new ingress time must not be inherited automatically |

## 6. Temporal compression ledger

| compression | classification | recovery |
| --- | --- | --- |
| source time -> `observed_at` | Lossy compression / Unknown | Lawful only if producer explicitly defines observed time as source sample time; otherwise unsafe |
| observation time -> Evidence time | Lawful preservation plus implementation convenience | Evidence inherits observation time; no independent Evidence recording time |
| observation time -> Fact `observed_at` | Lawful preservation for one-observation fact artifact; lossy for establishment/currentness | Fact artifact carries support observation time, not establishment time |
| Fact production -> fact event recording | Implementation convenience / Unknown | Fact event records artifact in ledger; production time and event timestamp may be close but are not constitutionally identical |
| event replay -> projected State | Lawful derived projection | Replay derives state; it does not mean events occurred again |
| latest sample -> current View | Predicate/view-local implementation policy | Measurement projection selects latest observed sample; current enough remains not proven universally |
| `expires_at` -> stale/current judgment | Consumer-dependent projection convenience | Default support filters expired facts; historical preservation remains |
| verification occurrence -> verified predicate Fact | Historical residue / bounded implementation witness | Verification standing must remain method-, scope-, and time-specific; a predicate fact alone risks compression |

## 7. Preservation versus current applicability

- After staleness: the fact/event/evidence remains preserved; default current-support selection may exclude it, and refresh recommendations may point at it.
- After expiry: the Fact is retained in projected state and ledger, can be reopened with `include_expired=True`, and is not deleted or made historically false.
- After contradiction: support, evidence, and conflicting fact artifacts remain recoverable; contradiction views do not erase historical claims. Current selection may choose a winner under projection rules.
- After supersession: older durable facts can remain retained; measurement projection may retain only recent samples in `State.facts`, while the append-only ledger still preserves all samples.
- After loss of current selection: preserved material can remain support, history, or conflict material; it does not remain currently applicable merely because preserved.
- After verification ages out: method/scope/time-specific verification may remain historically true as a verification occurrence, but current verified standing is Unknown without renewed or still-applicable verification evidence.

## 8. Predicate-family assessment

| family | recovered temporal semantics | standing |
| --- | --- | --- |
| measurement predicates | Implementation class for volatile time-series samples. Projection keeps limited recent samples and support selects the greatest `observed_at` sample as `current_sample`. | Current implementation policy with predicate-catalog support; not a full constitutional temporal theory. |
| durable predicates | Implementation class for repeated observations that can aggregate support by subject/predicate/value/dimensions. Earliest and latest support times are exposed. | Current implementation policy; durable does not mean eternally current. |
| historical occurrence predicates | Supported only where specific predicates/events represent occurrences. No general family recovered in core predicate catalog. | Unknown/generalization unsupported. |
| declaration or intent predicates | Present in repository vocabulary through acts, requirements, plans, authority, and refusal records, but not as a temporal predicate family in fact projection. | Boundary-specific testimony; do not generalize. |
| verification predicates | Capability verification surfaces witness method/scope-limited verification; verified standing is not identical to current standing. | Bounded implementation witness and amended Book concept; temporal duration often underspecified. |
| relationship claims | Relationships project from facts and copy observed time from source fact. They may be durable or current depending on predicate semantics and consumer purpose. | Projection witness; not independent relationship establishment time. |

## 9. View assessment

| view/surface | temporal meaning exposed | temporal meaning hidden or unsafe |
| --- | --- | --- |
| `ObservationView` | Observation id/type, summary, supporting event ids | Does not expose `observed_at`, expiry, source time, receipt time, or projection time; consumer must reopen observation/event material |
| Evidence-facing views / evidence graph | Evidence support/provenance links and often observed/support ids | Evidence recording time and source time are not generally distinct |
| `FactView` | Support-derived `observed_at`, `latest_observed_at`, `expires_at`, `expired`, supporting ids | Fact establishment time, projection time, consumer applicability, and source/receipt distinctions |
| current-fact getters | Projection-selected current facts under predicate/cardinality/expiry rules | Current enough for purpose; source time; consumer reliance |
| conflict views | Conflicting values, winner, fact ids | Temporal scope of conflict; whether values are historical succession, different intervals, or true contradiction |
| confidence views | Confidence/support aggregation | Truth, freshness sufficiency, temporal applicability |
| explanations | Can trace supporting evidence/facts/conflicts | Cannot manufacture missing temporal provenance; explanation time is not source time |
| verification views | Verification status/support where implemented | General verification duration and current applicability remain boundary-specific |

## 10. Boundary-by-boundary cross-examination

### External material to ingress

Source time is payload-specific, not a constitutional default. Receipt time, translation time, external realization time, and response time are not generally represented. Translation may preserve original temporal claims only if the producer copies them into payload, metadata, dimensions, evidence, or a dedicated record. Receipt time cannot substitute for source occurrence time. If source time is absent, ambiguous, or untrusted, temporal source standing remains Unknown.

### Ingress to Observation

`Observation.observed_at` is producer-specific. Repository source observations set one observation time at source-object construction. Runtime process observations default to collection time during `collect()`. Imported or caller-created observations may provide their own value. Therefore `observed_at` may mean collection time, adapter time, caller-supplied time, or source/sample time depending on producer. Observation does not generally preserve a separate claim-described interval.

### Observation to Evidence

Evidence inherits Observation time in the ingestion path. Evidence preservation has its own ledger event when ingested, but the Evidence artifact does not have an independent recorded-at field. Evidence can remain historically valid after stale current-state use because expiry filtering acts later on projection support, not on the ledger or evidence artifact.

### Claim normalization

Normalization preserves subject/predicate/value/dimensions that the implementation carries. It does not preserve all temporal dimensions unless those dimensions are part of the representation. Two claims with identical subject/predicate/value but different source times, validity intervals, vantage points, or observation contexts can collapse into the same apparent representation if the producer does not encode those differences. The amended grammar requires this to remain normalization without standing.

### Fact artifact production or Fact establishment

`Fact.observed_at` describes the observation/support time copied into the fact artifact, not independent artifact production or Fact-establishment time. Current implementation does not record Fact-establishment time independently. One-observation Fact production inherits testimony time and support link, but does not prove current applicability. A Fact can retain historical artifact/support standing after expiry or contradiction; broader Fact standing after amendment requires the applicable support, scope, authority, and conflict-aware establishment boundary.

### Support aggregation

Repeated durable observations of the same value aggregate support and expose earliest/latest observed support. Measurement observations are not strengthened by repetition; projection selects the latest observed sample as the current sample for the group. `latest_observed_at` establishes chronological greatest support time within the group, not freshness sufficiency, best support globally, or current standing for a consumer. Old and new evidence can support different historical claims if predicate semantics and intervals allow it; current conflict detection does not always preserve enough interval/vantage information to decide.

### Projection and View formation

Projection's as-of boundary is chiefly last event in ledger append order; cached snapshots also record build `created_at` and last event created time. `FactView` exposes support times and expiry but not projection time or establishment time. `ObservationView` hides observation time. Default projection filters expired support but does not delete material; measurement retention prunes projected `State.facts` while ledger history remains. Responsible consumers may need to reopen supporting records.

### Consumer uptake

Upstream material becomes temporally applicable to a consumer only through consumer-local purpose, authority, freshness, expiry, conflict, scope, and confidence judgments. Two consumers can lawfully assign different current applicability to the same preserved Fact if their purposes, time of reliance, or freshness thresholds differ. Consumption occurrence is generally absent unless a specific consumer records an admission/use event.

### Verification

Verification confirms a claim only under a method, scope, and time-specific boundary. Newer contradictory evidence may qualify, supersede, or challenge current verified standing without erasing the historical fact that verification occurred. A verified historical claim can remain historically verified while no longer verified currently, unless local verification doctrine says otherwise.

### Egress and external return

The current egress producer remains unresolved. Requirement time, request formation time, request emission time, external receipt time, external realization time, response production time, response receipt time, ingress time, and new Observation time must remain distinct. Returned testimony must not inherit the initiating View's projection time, the requirement time, or request time automatically.

## 11. Temporal conflict recovery

Current conflict detection groups by subject/predicate/dimensions and distinguishes values, with optional expiry filtering and winner selection. It does not generally preserve explicit validity intervals, source vantage, or claim-described intervals. Therefore apparently incompatible claims may be:

- true temporal succession;
- historical change;
- stale/current disagreement;
- different intervals;
- different observation times;
- different vantage points;
- actual contradiction;
- Unknown.

The implementation has enough evidence to avoid treating expired material as current by default and enough evidence to select measurement latest samples. It does not have enough general evidence to classify every `value A at T1` / `value B at T2` pair as compatible or contradictory. Predicate semantics and applicability intervals matter, and many are absent.

## 12. Required conclusions

### What distinct temporal standings does the repository currently support?

Seed supports preserved ledger sequence, event timestamp standing, observation testimony time, evidence-inherited observation time, fact-artifact observed/support time, expiry-filtered projection eligibility, support-group earliest/latest observed time, projection snapshot time, historical preservation standing, and bounded verification standing where verification surfaces record it.

### Which times describe the external claim, observation, recording, Fact artifact, Fact establishment, projection, and consumption?

- External claim time: payload/metadata-specific or Unknown.
- Observation time: `Observation.observed_at`, producer-specific.
- Recording time: event timestamp and ledger append order for ledgered records; snapshot `created_at` for projections; otherwise Unknown.
- Fact artifact time: `Fact.observed_at`, usually inherited observation/support time.
- Fact establishment time: not independently recorded in the general Fact model.
- Projection time: snapshot `created_at` when cached; otherwise projection-local and often not exposed.
- Consumption time: generally unrecorded and consumer-local.

### Is `observed_at` overloaded across constitutional boundaries?

Yes. It is used on Observation, Evidence, Fact, FactSupport, and relationship projections. In the ingestion path it is copied from Observation to Evidence and Fact. Across producers it may denote caller-supplied time, collection time, adapter time, source/sample time, or imported testimony time. It must not be read as receipt, recording, normalization, establishment, projection, or consumption time.

### Does the repository record Fact-establishment time independently of Observation or event time?

No general independent Fact-establishment time was found. Establishment is either not represented, compressed into artifact/event/support production, or recoverable only through a specific establishment boundary outside the core Fact model.

### Is freshness an upstream property or a consumer-relative judgment?

Freshness is not solely upstream. `expires_at` is upstream/preserved input to expiry filtering, but freshness sufficiency is projection-local and consumer-relative because purpose, authority, scope, conflict, verification, and time of reliance determine whether material is current enough.

### What exactly expires when a Fact reaches `expires_at`?

In current implementation, default current-support eligibility expires. Expired facts are filtered from support and best/current fact getters by default and reported as stale facts for refresh recommendation. The fact artifact, ledger event, evidence support, and historical recoverability do not expire or disappear.

### Can contradicted, stale, expired, or superseded Facts retain historical Fact standing?

They can retain historical artifact/support standing and may retain bounded historical Fact standing if their establishment boundary was lawful for the historical claim. Contradiction, staleness, expiry, supersession, or loss of current selection does not by itself erase preserved historical standing. Current applicability is separate.

### Does `latest_observed_at` establish current standing?

No. It establishes the latest observed support time within the support group. For measurement predicates, projection uses latest observed sample as the current sample under implementation policy, but this does not prove freshness sufficiency or consumer applicability.

### Can two consumers lawfully assign different temporal applicability to the same preserved Fact?

Yes. The Book already distinguishes applicable, admitted, and consumed material as consumer-local standings. Different purposes, freshness thresholds, authority requirements, conflict tolerances, and reliance times can produce different lawful applicability judgments over the same preserved Fact.

### Which temporal relations are missing or Unknown?

General source occurrence time, receipt time, translation time, normalized-at time, independent Fact-establishment time, claim validity interval, external service request/realization/response times, projection-consumption time, consumer reliance occurrence, and general causal relation are missing or Unknown unless a specialized producer records them in payload or event material.

### Is the Book ready for a canonical temporal amendment?

Mostly yes, but the safest next action is a canonical Book temporal amendment that preserves Unknowns and producer-specific characterization rather than a schema repair. The amendment should not introduce new timestamp fields or a global lifecycle; it should state boundary law: which temporal standings may pass, which must be newly established, and which inferences are forbidden.

## Smallest warranted next step

Canonical Book temporal amendment is warranted. It should be bounded to temporal standing, applicability, preservation, currentness, and forbidden inheritance across Claim expression, normalization, Fact artifact production/establishment, projection, verification, egress/return, and consumer uptake. It should explicitly leave producer characterization and view repair as later implementation questions.

## Bounded next question

How must the Book be amended so that temporal standing, applicability, preservation, and currentness remain distinct across the recovered boundaries?
