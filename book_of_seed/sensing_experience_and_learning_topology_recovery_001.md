# Sensing, Experience, and Learning Topology Recovery 001

## Status

Report-only investigation from merged `main` after PR 1898. No production code, tests, CLI behavior, persistence schema, projection schema, or canonical Book text was changed.

## Central Finding

Prometheus is not merely a monitoring surface. In current implementation it is a concrete external sensory translation path: a bounded Prometheus HTTP query set is fetched, provider JSON is validated, samples are decoded, provider-local shapes are semantically mapped, and Seed-native `Observation` objects are emitted for the existing observation-ingestion pipeline.

The reusable constitutional shape is narrower than a universal sensory framework: Seed already has a general `ObservationSource.collect() -> list[Observation]` boundary, a normalization boundary, an `Observation` to `Evidence` to `Fact` ingestion boundary, append-only event recording, and state projection. The Prometheus-specific parts remain query allowlisting, HTTP reach, Prometheus vector validation, sample decoding, metric-to-predicate interpretation, Prometheus metadata, sample time authority, and filesystem label dimensions.

Seed can remember repeated observations in the event ledger, and projection can retain a bounded recent measurement history when configured. However, projected current standing treats measurement predicates as latest current samples, not trajectories. Current repository evidence does not show an Experience artifact, an episode-equivalent standing, causal standing, or later movement selection that changes because an evidence-bearing prior episode was consumed.

## Repository witnesses examined

Primary implementation witnesses:

- `seed_runtime/observation_sources.py`: `ObservationSource`, `ObservationIngestionDiagnostics`, `PrometheusObservationSource`, `SAFE_QUERIES`, `_query(...)`, `_prometheus_decoded_sample(...)`, `_prometheus_observation_shapes(...)`, `_filesystem_dimensions(...)`, `ObservationCollectionService`.
- `seed_runtime/observations.py`: `Observation`, `ObservationIngestor`, `observation_to_evidence(...)`, `observation_to_fact(...)`, fact-promotion suppression for Prometheus `node_uname_info` OS observations.
- `seed_runtime/evidence.py`: `Evidence` payload model.
- `seed_runtime/facts.py`: `Fact`, `FactSupport`, `FactConflict`, measurement predicate classification.
- `seed_runtime/events.py`: `EventLedger`, `SQLiteEventLedger`, event correlation fields.
- `seed_runtime/state.py`: replay, projection publication, measurement-history retention, fact-support construction, current-fact selection, conflict projection, evidence/observation projection.
- `seed_runtime/models.py`: `Event`, legacy `ActionPlan`, legacy `HandoffPlan`, `PendingAction`, legacy `ExecutionAuthorization`.
- `seed_runtime/candidate_operational_realization.py`, `seed_runtime/capability_reachability_projection.py`, `seed_runtime/operational_realization_selection.py`, `seed_runtime/operator_authority_scope_binding.py`: candidate movement, reachability, selection, warrant handoff, and authority/scope witnesses.
- `seed_runtime/execution_status.py`: transient status family.
- Tests including `tests/test_fact_support_aggregation.py`, `tests/test_runtime_self_observation.py`, `tests/test_contradiction_characterization.py`, and `tests/test_temporal_characterization.py`.

Historical/report witnesses were used only as secondary context where they describe implemented boundaries and negative authority; implementation files above control the findings.

## Prometheus sensory road

### Question or query selection

`PrometheusObservationSource` accepts a base URL but does not accept arbitrary user PromQL. Its `SAFE_QUERIES` tuple is the current bounded question set: `up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`. `_query(...)` rejects any query outside that allowlist before external reach.

Boundary finding: **Present** for a Prometheus-specific bounded query set. Not universalized.

### External reach

For each allowlisted query, `_query(...)` constructs `api/v1/query?query=<metric>` and performs an HTTP `GET` with `Accept: application/json` and the configured timeout. The class docstring states it is read-only and uses fixed safe metric names.

Boundary finding: **Present** as Prometheus-specific HTTP reach. It does not imply Seed owns the external environment.

### Material receipt

`_query(...)` decodes the HTTP response body as JSON and requires a JSON object. It then requires `status == "success"`, `data.resultType == "vector"`, and `data.result` as a list.

Boundary finding: **Present** for provider response envelope validation.

### Provider-shape validation

`_prometheus_decoded_sample(...)` accepts only dict samples with dict `metric`, list `value` of length at least two, non-empty string `instance`, and parseable finite timestamp. Invalid samples are skipped by returning `None`.

Boundary finding: **Present** for Prometheus sample shape decoding. It is provider-specific.

### Signal decoding

A valid sample becomes `PrometheusDecodedSample(metric, instance, sample_timestamp, sample_timestamp_raw, sample_value)`. `_prometheus_sample_timestamp(...)` converts provider timestamp to UTC `datetime`; `_prometheus_int(...)` converts numeric sample strings to integers.

Boundary finding: **Present** for Prometheus signal decoding.

### Semantic interpretation

`_prometheus_observation_shapes(...)` maps query names to Seed-facing predicates:

- `up` may emit `endpoint_role` from the Prometheus `job` label and always emits `up` from the sample value.
- `node_uname_info` emits `os` after `_prometheus_os_from_uname(...)`, with fact promotion suppressed for endpoint subjects.
- `node_filesystem_avail_bytes` emits `filesystem_avail_bytes`.
- `node_filesystem_size_bytes` emits `filesystem_size_bytes`.

Boundary finding: **Present** but Prometheus-specific. This is where provider grammar becomes Seed predicate vocabulary.

### Observation production

`PrometheusObservationSource._observation(...)` creates `Observation(id="obs_prometheus...", source_type="provider", observed_at=<provider sample time>, subject, predicate, value, confidence=0.95, metadata, dimensions)`. Metadata preserves collector identity, Prometheus base URL, metric, labels, read-only HTTP method, provider sample timestamp, provider time authority, Seed collection time, Seed time authority, and current-instant temporal intent.

Boundary finding: **Present**. `Observation` is Seed-native testimony, not provider-native material and not environment truth.

### Normalization

`ObservationCollectionService.collect(...)` first calls `source.collect()`, then `_normalize_observation(...)`, which validates that collected items are `Observation` instances and that their `source_type` matches the source unless mixed types are explicitly allowed. It also adds `observation_source` metadata. If a normalization pipeline is configured, it projects current state and normalizes the observations against that state.

Boundary finding: **Present** and reusable across sources.

### Evidence construction

`ObservationIngestor.observation_to_evidence(...)` converts one `Observation` into `Evidence` with source `observation:<source_type>`, kind `observation`, the observation's `observed_at`, confidence, and a payload containing observation id, source type, subject, predicate, value, metadata, dimensions, and expiry.

Boundary finding: **Present** and reusable.

### Possible Fact-shaped production

`ObservationIngestor.observation_to_fact(...)` converts an observation/evidence pair into `Fact` with subject, predicate, value, dimensions, evidence id, source type, confidence, observed time, expiry, and inferred status. `_should_suppress_fact_promotion(...)` prevents Prometheus `node_uname_info` endpoint-scoped OS observations from becoming facts.

Boundary finding: **Present**. Fact production is not identical to experience; it is current knowledge projection material with evidence provenance.

### Recording

`ObservationIngestor.ingest_many(...)` builds, in order for each observation, `observation.observed`, `evidence.observed`, and optional `fact.observed` or `fact.inferred` events, then appends them via `EventLedger.append_many(...)`. It passes through optional `session_id`, `causation_id`, and `correlation_id`; when absent, evidence and fact events use observation/evidence IDs as causation defaults.

Boundary finding: **Present** for event recording. Correlation fields can preserve lineage hints, but they are not proof of realization or causation.

### Projection

`StateProjector` replays ledger events into `State.observations`, `State.evidence`, and `State.facts`, then finalizes derived indexes. Projection trims measurement facts to a configurable `measurement_history_limit`, builds `FactSupport`, selects current facts, and suppresses measurement predicates from conflict projection because retained measurement samples are history, not competing durable claims.

Boundary finding: **Present** for projection into current standing and bounded recent measurement retention. Not trajectory standing.

### Later consumption

Current-facing consumers call state helpers such as `get_current_facts(...)`, `get_best_fact(...)`, `get_fact_support(...)`, `get_fact_conflicts(...)`, stale fact refresh recommendations, capability inventory, and operational projections. These consume projected standing, not provider-native payloads.

Boundary finding: **Present** for current state consumption. Evidence of later movement selection consuming prior before/movement/after episodes is absent.

## Provider-specific vs reusable boundaries

| Boundary | Prometheus-specific | Reusable/existing Seed boundary |
|---|---:|---:|
| Safe question set | `SAFE_QUERIES` metric allowlist | General idea of bounded source collection is reusable but not universalized. |
| External reach | Prometheus HTTP `GET /api/v1/query` | Source adapters can perform bounded collection. |
| Provider envelope validation | Prometheus success/vector/result checks | Source-local validation pattern. |
| Sample decoding | Prometheus `metric`/`value`/`instance`/timestamp decoding | Source-local decoded-material boundary could be repeated by other providers. |
| Semantic interpretation | Prometheus metric-to-predicate mapping | General `Observation(subject, predicate, value, metadata, dimensions)` target. |
| Observation production | Prometheus IDs, provider confidence, provider metadata | `Observation` model is reusable. |
| Normalization | Endpoint alias exceptions and metadata shape partly Prometheus-aware | `ObservationCollectionService` and normalization pipeline are reusable. |
| Evidence construction | None except carried metadata | `ObservationIngestor.observation_to_evidence(...)` is reusable. |
| Fact production | Prometheus OS fact-promotion suppression | `observation_to_fact(...)` is reusable. |
| Recording | None except event metadata values | Event ledger is reusable. |
| Projection/current selection | Measurement predicates include Prometheus-style `up` and filesystem bytes | Projection mechanism is reusable for facts and measurements. |

## Repeated-sensing and temporal-retention findings

Seed can retain repeated observations at the event-ledger level. Every collected observation can produce an `observation.observed` event, an `evidence.observed` event, and often a fact event. `EventLedger` is append-only in memory; `SQLiteEventLedger` persists events to SQLite with timestamps and optional session/causation/correlation fields.

Projection is more selective. `StateProjector` defaults `measurement_history_limit` to `1`, requires it be at least one, and prunes measurement facts to the latest N per subject/predicate/dimensions series. Tests show that setting `measurement_history_limit=3` retains recent samples while `get_fact_support("svc_ssh", "up")` still points to the latest sample only. Tests also show availability/debug-history measurements can retain old and new values without fact conflicts, while current best fact is the newest sample.

Current retention by requested dimension:

- Multiple observations of the same subject/predicate: **Present in ledger**, **Partial in projected state** for measurements because the projection retains only latest N configured samples and default N is one.
- Source sample time: **Present** as `Observation.observed_at`, `Evidence.observed_at`, `Fact.observed_at`, and Prometheus metadata.
- Seed collection time: **Present** in Prometheus metadata as `seed_collected_at`.
- Provider time authority: **Present** in Prometheus metadata as `source_time_authority="prometheus"`.
- Collection time authority: **Present** in Prometheus metadata as `seed_collection_time_authority="seed_local_clock"`.
- Dimensions and labels: **Present**; Prometheus labels are preserved as metadata, and filesystem labels become dimensions.
- Contradictions: **Partial**. Durable fact conflicts are projected; measurement predicates are intentionally excluded from conflict projection.
- Supersession: **Partial**. Latest measurement support supersedes older measurement samples for current standing, but no explicit supersession artifact is created.
- Expiry: **Present** on observations/facts and in state helper handling, though Prometheus observations do not currently set expiry.
- Historical observations: **Present in ledger**, **Partial in projection** because measurement projection prunes retained samples.
- Current selection: **Present** through `FactSupport` and `get_current_facts(...)`.

A sequence such as service up at t1, down at t2, up at t3 can be stored as repeated observations/events and, with `measurement_history_limit >= 3`, can be recovered as three retained measurement facts. But current implementation does not promote it into trajectory, transition, outage, recovery, flap, or cause standing. It remains repeated testimony plus current-sample selection.

Required refusals:

- One observation is not observation history.
- Observation history is not trajectory understanding.
- Latest observation is not current truth; it is current projected standing from testimony.
- Repeated testimony is not independent corroboration when source identity and support identity do not establish independence.
- Change between observations is not cause of change.

## External sensing vs operational self-sensing

The recovered relation is a useful analogy with implemented overlap, not identity.

Prometheus observation is Seed sensing an external environment through a provider grammar. The signal source is Prometheus HTTP JSON; the observed subjects are endpoints, OS identity, and filesystems; temporal authority is provider sample time plus Seed collection time; labels and dimensions preserve provider series identity; recording proceeds through observation/evidence/fact events; projection produces current standing.

Operational measurement is Seed sensing the behavior of its own bounded operation. `ObservationIngestionDiagnostics` records source collection time, normalization time, event generation and ledger write time, totals, promoted fact count, and source counters. `ProjectionBuildDiagnostics` records projection phase timings and counters. `SeedRuntimeObservationSource` emits read-only discovery observations about Seed process memory, thread count, runtime duration, and storage sizes, marked `read_only`, `mutates_cluster=false`, `scheduler=false`, and `runtime_governance=false`; tests prove these observations flow through the same ingestion and projection path.

Shared grammar:

- bounded producer;
- observed subject;
- method-specific testimony;
- observed/collected time;
- read-only metadata where applicable;
- observation/evidence/fact recording when using the observation path;
- projection into state;
- later consumption as projected facts or diagnostics.

Distinct grammar:

- External sensing receives environment-native/provider-native material; operational measurement measures Seed's own phases, counters, process, and persistence files.
- Prometheus records provider sample time authority; operational timing diagnostics often use local monotonic/perf-counter phase timing and may remain diagnostic payloads rather than observations.
- `ExecutionStatus` exposes activity visibility but is not a measurement result, observation, experience, or learning.
- Operational measurement can describe bounded operation behavior; it does not by itself establish environment truth or experience.

Conclusion: both are instances of broader testimony-like practice only by analogy unless restricted to existing boundaries. The repository already has a general `Observation` ingestion grammar and separate diagnostic-measurement grammar; it does not yet name a universal testimony superclass that lawfully absorbs both.

## Sensing / remembering / experience / learning distinctions

### Sensing

Proposed definition: producing bounded testimony about an environment or operation.

Status: **Accepted narrowly**. External observation sources and runtime self-observation sources produce bounded `Observation` testimony. Diagnostic timing objects produce bounded operational-measurement testimony, but not always as `Observation` artifacts.

### Remembering

Proposed definition: retaining sufficient testimony or standing for later recovery.

Status: **Accepted narrowly**. The event ledger retains observation/evidence/fact events; SQLite can persist them across process exit. Projection retains current standing and, for measurements, bounded recent history according to `measurement_history_limit`. Remembering is not the same as sensing because collection can produce an observation before durable recording, and projection can forget pruned measurement samples even though the ledger retains events.

### Experience

Proposed definition: binding a prior situation, selected movement, realization testimony, resulting situation, and bounded outcome evaluation.

Status: **Absent as implemented artifact; Partial as separable ingredients**. Repository evidence contains observations, candidate operational realizations, selection artifacts, future handoffs, legacy handoff/authorization records, behavior observations/comparisons, event session/causation/correlation fields, impact comparisons, and current standing. It does not show a single evidence-bearing episode that binds before-state, selected movement, reported external realization, after-state, and declared outcome evaluation for later use.

### Learning

Proposed definition: changing later expectation, standing, or movement selection because of evidence from prior experience.

Status: **Absent**. The repository can change stored facts and current projections after new evidence. It can select an operational realization according to a policy and current candidate/reachability evidence. Current evidence does not show a later selector consuming preserved prior episodes and changing selection because of those episodes. Learning is not model training by identity; no model-training standing is required or present.

Direct tests:

- sensing != remembering: supported.
- remembering != experience: supported.
- observation history != experience: supported.
- experience != causal proof: supported by absence of causal artifact.
- repeated experience != learning automatically: supported; repeated observations do not drive selector change.
- changed stored data != changed later selection: supported.
- learning != model training by identity: supported as a negative boundary; no training framework is present.

## Movement and external-realization topology

Current repository evidence preserves external-realization asymmetry. Seed does not own a canonical internal executor.

Implemented or represented portions:

1. **Situation understanding**: projected `State`, facts, supports, conflicts, stale recommendations, and many read-only projections can provide bounded standing.
2. **Candidate movement / realization**: `CandidateOperationalRealizationSet` preserves candidate operational realizations, mechanism observations, invocation contracts, recovered grammar, behavioral observations, behavior comparisons, bases, standings, unknowns, and conflicts. It explicitly does not rank or select candidates.
3. **Reachability**: `CapabilityReachabilityProjection` consumes candidates and produces reachability plus future selection handoff; it does not select a realization.
4. **Selection**: `OperationalRealizationSelection` selects zero or one supported realization under a selection policy and may produce `FutureOperationalRealizationWarrantHandoff`. Its boundary notes say selection does not warrant reliance, construct invocation, translate external representation, authorize, schedule, or execute.
5. **Authority/scope**: `OperatorAuthorityScopeBindingProjection` can block or permit bounded downstream movement from operator expression and authority/scope material, but does not execute or grant authority beyond its scope.
6. **Representation grammar**: current review of representation grammar recovery is left to independent implementation evidence; no applicability-to-handoff owner is preserved here.
7. **Handoff/authorization residue**: `ActionPlan`, `HandoffPlan`, and `ExecutionAuthorization` are explicitly legacy/experimental/non-core or side-path compatibility artifacts. `HandoffPlan` records a boundary but does not execute, approve, assert trust, register a tool, retry, schedule, or manage jobs. `ExecutionAuthorization` is non-core secret-free grant metadata and must not be used to add internal execution lifecycle.
8. **Reported realization/result**: current repository evidence includes behavior observations/comparisons for candidate validation and generic evidence graph classification of tool results, but no canonical realization testimony artifact that binds an external mechanism's reported realization to before/after observations.

Therefore the lawful loop is only partially represented:

```text
Seed observes environment            Present
Seed forms bounded standing          Present
Seed selects/exposes possible move    Partial/Present for read-only operational-realization selection
Movement crosses handoff boundary     Partial as future handoffs and legacy handoff plans
External mechanism realizes it        Absent as Seed-owned implementation; not inferred
Seed receives new testimony           Present generally via observations/evidence
Seed compares resulting situation     Partial via impact/behavior comparisons, not episode-bound outcome attribution
```

## Before / movement / realization / after binding inventory

| Candidate | What it actually binds | Producer | Survives process exit | Proves occurrence | Supports temporal ordering | Supports attribution | Supports causal inference | Later selector consumes it |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `session_id` on `Event` | Events to a session label | Event producers/ingestors | Yes in SQLite ledger | No | Event timestamps/order only | Weak grouping | No | Not shown |
| `causation_id` on `Event` | Event to asserted cause/correlation id | Event producers/ingestors | Yes in SQLite ledger | No | Event order only | Partial lineage hint | No | Not shown |
| `correlation_id` on `Event` | Event to correlation group | Event producers/ingestors | Yes in SQLite ledger | No | Event order only | Weak grouping | No | Not shown |
| Observation/evidence/fact chain | Observation to Evidence to optional Fact | `ObservationIngestor` | Yes in ledger; projected state retains current/bounded history | Proves Seed recorded testimony, not environment truth | Uses observed/event timestamps | Attribution to source type/source metadata | No | Consumed by state and some projections |
| `FactSupport` | Current support group for subject/predicate/value/dimensions | State projection | Recomputable from ledger; persisted by projection store if used | No | Preserves observed/latest observed time | Evidence ids/source types | No | Yes, many current-state consumers |
| Measurement history limit | Recent N measurement facts per series in projection | State projection | Recomputable from ledger; projection may store | No | Yes for retained samples | Subject/predicate/dimensions | No | Current helpers select latest, not trajectory |
| `FactConflict` | Durable conflicting values | State projection | Recomputable; projection store can persist | No | Limited | Subject/predicate/dimensions | No | Current conflict consumers |
| `CandidateOperationalRealizationSet` | Candidate mechanisms and standings | `project_candidate_operational_realizations(...)` | As artifact only if caller records externally; dataclass itself read-only | No external occurrence | No episode order | Candidate-to-basis references | No | Reachability consumes it |
| `CapabilityReachabilityProjection` | Candidate set to reachability and future selection handoff | `project_capability_reachability(...)` | Artifact read-only | No | No episode order | Candidate/reachability lineage | No | Selection consumes it |
| `OperationalRealizationSelection` | Policy, reachability, candidate set, selected candidate | `select_operational_realization(...)` | Artifact read-only unless recorded by caller | No movement realization | No after-state order | Selection attribution to policy | No | Warrant handoff exists; no later learning consumer shown |
| `FutureOperationalRealizationWarrantHandoff` | Selected candidate for possible later warrant | Selection producer | Artifact read-only | No | No | Selection lineage | No | No canonical realization consumer shown |
| `HandoffPlan` | Legacy external-provider handoff boundary for an action plan | Legacy model/event producers | Yes if recorded | No; explicitly non-executable | Event order only | Handoff metadata | No | Not canonical Runtime |
| `ExecutionAuthorization` | Legacy secret-free authorization metadata | Legacy model/event producers | Yes if recorded | No realization | Expiry and event order | Grant metadata only | No | Not canonical Runtime |
| Behavior observation/comparison | Mechanism invocation behavior against reference | Candidate-realization projection inputs | Artifact-only unless recorded | Proves reported/observed behavior only under bounded test | Limited if timestamps/provenance supplied outside class | Mechanism id/input/result | No, comparison is not causation | Candidate projection consumes comparisons |
| Impact audit before/after snapshots | Comparable metrics before and after snapshots | `impact_audit` | Snapshot-dependent | No realization proof | Yes for snapshot comparison | Surface/metric comparison | No | Diagnostic/audit consumers, not movement selector |

No candidate currently binds all five required elements: prior situation, selected movement, reported realization, resulting situation, and outcome for a declared purpose.

## Causation boundary

The report explicitly refuses this equation:

```text
movement M was followed by outcome O
=
movement M caused outcome O
```

The strongest lawful assertion current evidence can support, when all separate records are present, is:

```text
under conditions C,
Seed had prior projected standing S1,
movement candidate M was selected or exposed under policy P,
a handoff or external report R was recorded,
and later observation O/S2 followed in ledger time or observed time,
with remaining uncertainty about whether M caused O/S2.
```

Stronger causal standing would require additional bounded evidence such as declared intervention identity, explicit before/after episode binding, external realization testimony with authority and scope, controlled or ruled-out alternative causes, temporal ordering accepted by the relevant domain, outcome criteria declared before evaluation, and a consumer that treats that evidence as causal only under stated limitations. This report does not prescribe a universal causal-learning implementation.

## Pong thought-experiment cross-examination

Pong is not repository authority. It is only a test of the recovered grammar.

- Seeing the ball: would correspond to a source decoding game-native state into observations such as ball position and velocity. Current Seed has the `Observation` target shape, but no Pong source or universal sensory framework.
- Remembering prior frames: the ledger could retain repeated observations, and projection could retain bounded recent measurement history if predicates were measurement predicates and the limit allowed it. That would still be frame history, not trajectory understanding.
- Moving the paddle: current Seed can represent candidate operational realizations and selection, but not a Seed-owned internal executor or game controller.
- Knowing the paddle moved: would require external realization testimony. Current Seed does not infer realization from proposal, selection, or handoff alone.
- Observing the next frame: current observation ingestion could record later testimony.
- Judging whether the rally continued: would require bounded outcome evaluation tied to a declared purpose. Current comparisons exist in separate audit/behavior domains but no general experience episode binds them here.
- Changing next movement because of prior evidence: absent unless a later selector consumes preserved evidence-bearing episode material; current selection policy does not show that dependency.

Thus the recovered grammar distinguishes seeing, remembering, moving, reported movement, after-observation, outcome evaluation, and learning, but only some pieces are implemented.

## Prometheus interaction cross-examination

Scenario:

```text
Prometheus reports service up = 0
Seed exposes or hands off a bounded recovery movement
external mechanism reports realization
Prometheus later reports service up = 1
```

Seed could lawfully preserve, using existing pieces:

- before observation: `Observation`, `Evidence`, `Fact`, ledger event(s), Prometheus sample time, Seed collection time, labels/dimensions;
- movement selection: `OperationalRealizationSelection` and future warrant handoff if candidate/reachability/policy evidence supports one;
- handoff: future handoff artifact or legacy `HandoffPlan` if used as side-path compatibility, without treating it as execution;
- reported realization: only as separate testimony/evidence if an external mechanism reports it; not inferred from selection;
- after observation: another Prometheus observation/evidence/fact chain;
- temporal relation: event order, event timestamps, observed_at timestamps, and optional session/causation/correlation IDs;
- declared outcome purpose: only if some artifact explicitly records it; not guaranteed by Prometheus or selection alone;
- remaining uncertainty: source reliability, independent realization verification, alternative causes, scrape timing, provider sample authority, and whether recovery movement caused the change.

Seed could not lawfully claim that the recovery movement caused `up` to become `1` merely because the later Prometheus sample changed. It also could not claim the movement was realized merely because it was selected or handed off.

## ExecutionStatus relevance and exclusion

`ExecutionStatus` is useful as a secondary witness for phase boundaries: collection, normalization, event generation, event persistence, projection replay, cache access, and index construction can emit renderer-independent progress/status payloads. `ObservationCollectionService`, `ObservationIngestor`, `EventLedger.append_many(...)`, and `StateProjector` use status consumers to expose operation progress.

But `ExecutionStatus` is transient, renderer-independent activity visibility. It does not own execution state. It is not operational measurement, not operation result, not environment observation, not experience, and not learning. `RecordingExecutionStatusConsumer` stores statuses in memory for tests/inspection only, and `CliExecutionStatusConsumer` renders feedback.

## Present / Partial / Absent / Unknown matrix

| Capability / boundary | Classification | Evidence-based reason |
|---|---|---|
| External sensory translation | Present | Prometheus and other observation sources translate source material to `Observation`. |
| Repeated observation retention | Partial | Ledger retains repeated events; projection prunes measurement history by configurable limit. |
| Temporal sequence recovery | Partial | Event order and observed timestamps exist; retained projected sequence depends on ledger access/history limit. |
| Trajectory or transition standing | Absent | No outage/recovery/flap/transition artifact found for repeated measurements. |
| Movement selection | Present | Operational realization selection can select zero or one supported candidate. |
| External realization handoff | Partial | Future handoffs and legacy handoff plans exist; no canonical executor/realization lifecycle. |
| Realization testimony | Partial | Behavior observations/comparisons and generic evidence can carry reports, but no canonical realization testimony bound to movement episode. |
| Before/after binding | Partial | Correlation/session/causation ids and snapshots can group/order, but no complete episode binding. |
| Outcome evaluation | Partial | Impact and behavior comparisons exist in bounded domains; no universal outcome for selected movement. |
| Experience standing | Absent | No artifact/equivalent binds prior situation, selected movement, realization, resulting situation, and outcome. |
| Causal standing | Absent | Temporal/correlation evidence does not establish cause. |
| Cross-experience comparison | Absent | No experience artifacts exist to compare. |
| Changed later movement from prior evidence | Absent | No selector shown consuming prior episodes to change movement selection. |
| Operational self-sensing | Present | Runtime self-observation and operational diagnostics measure Seed/process/projection behavior. |
| Activity status as sensing | Absent | `ExecutionStatus` is activity visibility, not sensing/measurement result. |

## Required distinctions tested

- External signal != `Observation`: provider JSON is decoded before `Observation` construction.
- `Observation` != environment truth: it is canonical testimony with confidence/provenance.
- Observation history != experience: history lacks movement, realization, outcome binding.
- Temporal succession != causation: event order/timestamps are not causal proof.
- Movement proposal != movement realization: candidate/selection/handoff boundaries explicitly stop before execution.
- Realization report != independently verified effect: a report would still need after-observation and attribution evidence.
- After-observation != result attribution automatically: later Prometheus `up=1` does not prove recovery movement caused it.
- Outcome evaluation != universal success: comparisons are bounded to declared dimensions/domains.
- Experience != `Fact` by identity: facts are subject/predicate/value claims with evidence, not episodes.
- Experience != learning automatically: even a repeated episode would not change selection unless a selector consumes it.
- Learning != retained history: history can be remembered without altering expectations or movement.
- Learning != baseline formation automatically: baselines/aggregates are not shown as movement-changing learning.
- Changed later selection != lawful learning unless the evidence-bearing dependency is preserved: no such dependency was found.
- External sensing != operational self-measurement: source, subject, method, and time authority differ.
- Activity status != either form of sensing: status is transient progress visibility.

## Required conclusions

1. **Is the Prometheus observer merely a monitoring surface?** No. It is an implemented external sensory translation path from bounded Prometheus provider material into Seed-native observations and projected facts. It remains only one provider-specific source, not a universal sensory framework.
2. **Which parts of its road are Prometheus-specific?** Safe metric names, HTTP API path, vector response validation, sample decoding, timestamp parsing, metric-to-predicate interpretation, Prometheus labels/metadata, provider time authority, and filesystem dimension extraction from Prometheus labels.
3. **Which parts express more general external sensory translation?** `ObservationSource.collect()`, `Observation`, collection service validation/normalization, evidence construction, optional fact production, event-ledger recording, and state projection.
4. **Does Seed currently retain repeated observations over time?** Yes in the ledger; partially in projected state because measurement retention is bounded and defaults to latest one.
5. **Does retained observation history currently become trajectory understanding?** No. Repeated samples remain testimony/history/current-sample support, not trajectory or transition standing.
6. **Can Seed presently bind a before-state, movement, reported realization, and after-state into one evidence-bearing episode?** No complete current artifact was found. Existing IDs and projections can preserve pieces but not the full episode.
7. **Does Seed currently possess an Experience artifact or equivalent standing?** No.
8. **Does Seed currently change later movement because of evidence from prior episodes?** No evidence found.
9. **Is operational measurement an inward analogue of external observation, and where does that analogy stop?** Yes as a bounded-testimony analogy: both can produce retained evidence about a bounded source/method/time. It stops at artifact identity and authority: operational diagnostics/status are not provider observations, not environment truth, not experience, and not learning.
10. **What is the smallest missing constitutional or implementation boundary between repeated sensing and learning?** The smallest missing boundary is not necessarily an `Experience` class. It is an evidence-bearing binding boundary that preserves, for one declared purpose and scope, prior situation, selected movement, reported external realization/refusal, resulting testimony, bounded outcome evaluation, uncertainty, and the fact that a later selector consumed that bound evidence when changing expectation, standing, or movement selection.

## Smallest coherent next step

If future work is admitted, the smallest coherent next step is a report or narrow projection audit that inventories existing event/session/causation/correlation, handoff, behavior-comparison, and impact-snapshot records for whether any current consumer preserves a declared before/movement/after dependency. It should remain read-only unless separately authorized, and it should not create a universal sensory framework, executor, Experience class, causal model, learner, or policy engine.

## One bounded unresolved question

When a future selector changes movement selection after new evidence appears, what exact preserved dependency must it expose to distinguish lawful learning from merely reading changed current state?
