# Temporal Standing and View Disclosure Amendment 001

## Status

Canonical amendment record. This record documents the cross-examination that amended the Book; it is not an independent source of constitutional authority apart from the clauses amended below.

## Book clauses examined

- `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `01-grammar-and-standing/constructors-and-production-authority.md`
- `01-grammar-and-standing/lenses-views-and-roads.md`
- `02-acts-and-constraints/acts-and-act-artifacts.md`
- `02-acts-and-constraints/selection-artifacts-and-selection-acts.md`
- `04-inquiry-and-examination/examination-methods-and-probes.md`
- `05-evidence-and-knowledge/testimony-and-established-fact.md`
- `05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `06-state-and-projection/events-facts-and-state.md`
- `06-state-and-projection/projection-and-current-state.md`
- `08-authority-communication-and-stopping/authority-scope.md`
- `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `concordance.md`
- `unresolved.md`

## Historical doctrine examined

- `docs/temporal_reasoning_audit.md` first established the broad non-equivalence of event time, observation time, recording, expiry, replay, staleness, and current use.
- `docs/event_and_change_reconciliation.md` independently anchored append-only event history and change projection, including the distinction between recorded event material and current state.
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md` first made freshness and refresh purpose-relative rather than truth-relative.
- `docs/knowledge_maintenance_reconciliation.md` repeated and operationalized stale/refresh distinctions; it was corroborating, not first authority.
- `docs/claim_strength_and_assertion_semantics_reconciliation.md` first tied claim strength to assertion semantics, blocking automatic promotion from source report to live-state claim.
- `docs/operator_interface_and_projection_authority_reconciliation.md`, `docs/view_authority_and_surface_responsibility_reconciliation.md`, and `docs/read_model_inventory_and_authority_reconciliation.md` anchored View authority and surface responsibility without making every View a current-standing surface.
- `docs/explainability_contract_characterization.md` anchored provenance and explanation as reasons/exposure, not establishment.

## Repository witnesses examined

- `seed_runtime/events.py`: `EventLedger.list()` returns append order; append and batch append store event objects without reordering by event timestamp.
- `seed_runtime/models.py`: Event timestamp is event-carried metadata and can be supplied on externally constructed events.
- `seed_runtime/observations.py`: `Observation.observed_at` is caller/producer-supplied observation testimony; conversion to `Evidence` and `Fact` copies it and optional expiry forward.
- `seed_runtime/evidence.py`: `Evidence.observed_at` records evidence time but, through the ingestion path, inherits Observation time.
- `seed_runtime/facts.py`: `Fact.observed_at`, optional `expires_at`, `FactSupport.observed_at`, `latest_observed_at`, `expired`, `expires_at`, and support kind/semantics preserve support and expiry material, not establishment time.
- `seed_runtime/state.py`: current fact getters and support projection filter expiry by default, reopen expired material with `include_expired=True`, aggregate durable support, and choose measurement current samples by greatest observed time.
- `seed_runtime/state_views.py`: public `ObservationView` exposes `observation_id`, `observation_type`, `summary`, and `supporting_event_ids`; public `FactView` exposes `fact_id`, `subject`, `predicate`, `object`, `confidence`, `dimensions`, and `supporting_event_ids` only.
- `seed_runtime/projection_store.py`: `ProjectionSnapshot.created_at`, `last_event_id`, and `last_event_created_at` distinguish snapshot time, ledger append boundary, and event-carried timestamp clue.
- `seed_runtime/evidence_graph.py`, `seed_runtime/confidence.py`, `seed_runtime/contradictions.py`, and `seed_runtime/explanations.py`: evidence/confidence/contradiction/explanation surfaces expose support, conflict, confidence, and sometimes support-window times, but do not establish upstream truth or consumer reliance.
- Focused tests in `tests/test_temporal_characterization.py`, `tests/test_state_views.py`, `tests/test_evidence_graph.py`, `tests/test_confidence.py`, `tests/test_contradictions.py`, and `tests/test_explanations.py` preserve these implementation behaviors.

## PR 1889 claims accepted

- Seed preserves ledger append sequence separately from event timestamp.
- Observation, Evidence, Fact, support aggregation, projection snapshot, expiry, and consumer applicability are materially different temporal relations.
- `observed_at` is not a universal source occurrence, receipt, recording, normalization, establishment, projection, or consumption time.
- Expired and stale material remains historically preserved and may remain explainable or reopenable.
- Latest support or latest measurement sample is not sufficient to prove current applicability.
- Projection snapshot time is local to projection/cache formation and is not source time.
- Verification remains method-, scope-, and time-bounded.
- Egress and returned testimony require distinct temporal boundaries that the current producer does not yet resolve.

## PR 1889 claims corrected or rejected

- The recovery report's field inventory is inaccurate for the current public `FactView`: it claimed public exposure of `observed_at`, `latest_observed_at`, `expires_at`, and `expired`; the current dataclass exposes none of those fields.
- The same report is overbroad where it treats `FactView` as a temporal disclosure surface. The builder consumes `FactSupport` temporal evidence for projection and selection, but the public View shape does not disclose support-window or expiry distinctions.
- The report is overbroad if read to imply `ObservationView` exposes observation time or expiry. The current dataclass exposes neither.
- These errors do not require rewriting the historical report. It remains testimony with this amendment explicitly recording the inaccurate witness and superseding it for canonical grammar.

## Canonical clauses amended

- `01-grammar-and-standing/lenses-views-and-roads.md` now distinguishes View selection responsibility, assertion responsibility, and temporal disclosure responsibility.
- `05-evidence-and-knowledge/testimony-and-established-fact.md` now defines temporal standing, `observed_at`, normalization preservation, Fact support time, Fact-establishment-time absence, expiry, staleness, and latest-support limits.
- `06-state-and-projection/events-facts-and-state.md` now distinguishes event timestamp, ledger order, chronology, causation, projection-local selection, snapshot time, and current selection.
- `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md` now preserves consumer-local temporal applicability and non-inheritance across egress/returned testimony.
- `concordance.md` now indexes temporal standing and temporal disclosure.

## Clauses preserved

- Artifact shape still does not establish constitutional standing.
- Constructors and replay still do not prove producer occurrence or establishment.
- Views and lenses still expose bounded representations without strengthening upstream material by identity.
- Projection still does not become constitutional source law.
- Fact artifact, Fact standing, current standing, and verification standing remain distinct.
- Consumer uptake remains local and may preserve Unknown or refusal.

## Missing temporal grammar recovered

The missing grammar was not a new lifecycle object. It was the rule that temporal evidence, temporal selection, temporal standing, temporal disclosure, provenance navigation, projection-local selection, and consumer applicability are separate responsibilities. A boundary may consume one temporal relation without asserting it; may assert a compact result without duplicating every upstream timestamp; and must disclose every temporal distinction that defines the standing it claims.

## Boundary answers

| Boundary | Canonical answer |
| --- | --- |
| Claim expression | A claim may express occurrence, interval condition, source report, desired state, historical assertion, present-facing assertion, or durable relation. No universal one-timestamp claim grammar is warranted. |
| Normalization | Temporal material must be preserved where it is part of claim identity, dimensions, support scope, provenance, predicate semantics, or source-relative limitation. The required location is predicate- and claim-family-specific. |
| Observation and Evidence | `observed_at` is producer-supplied observation-time testimony with producer-specific meaning. Evidence inherits it through the observed ingestion path and does not gain receipt or recording time by copying it. |
| Fact artifact and Fact standing | A Fact artifact carries support/described-claim time. Fact standing may be established without an independent stored `established_at`, but that establishment time remains Unknown unless evidenced by the producer/event boundary. |
| Support aggregation | Durable support aggregation preserves earliest and latest support times; measurement support selects the greatest observed sample as a current sample. Neither earliest nor latest automatically creates validity start, currentness, or freshness sufficiency. |
| Projection | Projection replays ledger append order and may select current material under rules. Snapshot `created_at` is projection-local; `last_event_id` is append-sequence as-of boundary; projection may select but not create upstream temporal standing. |
| Consumer uptake | Consumers judge purpose fit, freshness threshold, expiry meaning, conflict tolerance, authority, scope, verification duration, and reliance time locally. Different consumers may lawfully disagree on applicability. |
| Verification | Verification remains bounded by method, target, scope, evidence, and time. Its historical occurrence or testimony can remain preserved after current verification applicability ages out. |
| Egress and returned testimony | Requirement, request, emission, receipt, realization, response, ingress, and new Observation times do not inherit from one another without recorded producer evidence. |

## Subject table

| subject | prior Book wording | ambiguity | repository witness | amended wording | remaining limit |
| --- | --- | --- | --- | --- | --- |
| `observed_at` | Observation and Fact chapters treated support time as preserved testimony but did not fully define its safe meaning. | Could be read as source occurrence, receipt, recording, or establishment time. | `ObservationIngestor` copies `Observation.observed_at` into `Evidence` and `Fact`. | It is only producer-supplied observation-time testimony, with producer-specific meaning. | Producer-specific semantics may remain Unknown. |
| event timestamp | Events were immutable records with timestamps. | Could be confused with append order or source occurrence. | `EventLedger` stores externally supplied Event objects in append order. | Event timestamp is event-carried metadata, distinct from ledger order. | Clock source and external occurrence may be Unknown. |
| ledger order | Projection replay was recognized. | Append sequence could be mistaken for chronology or causation. | Temporal tests prove out-of-order event timestamps do not reorder projection. | Ledger order is replay input sequence, not causation or source chronology. | Cross-ledger order remains Unknown. |
| Fact support time | Fact standing wording preserved support but not all temporal roles. | Support time could be read as validity start or establishment. | `FactSupport.observed_at` and `latest_observed_at` derive from supporting fact observation times. | Support times bound support evidence; earliest is not automatically validity start. | Predicate-specific validity remains unresolved. |
| Fact-establishment time | Fact chapter said Fact artifact does not prove standing. | Absence of `established_at` could erase establishment or collapse it into `observed_at`. | `Fact` has no `established_at`; establishment is compressed with producer/event/support evidence. | Fact standing may have a production boundary even when its timestamp is absent or Unknown. | Which producers establish broader standing remains unresolved. |
| expiry | Expiry was recognized as stale/current filtering. | Could be read as deletion, falsity, or historical invalidity. | State filters expired facts by default and reopens them with `include_expired=True`. | Expiry removes only named current-support eligibility or local temporal permission. | Purpose-specific expiry semantics may differ. |
| `latest_observed_at` | Recovery report treated it as view-visible. | Could be read as current enough. | `FactSupport` has it; public `FactView` does not. | Latest support is selection evidence, not freshness sufficiency or public FactView disclosure. | Future repair may expose, explain, split, or narrow assertions. |
| freshness | Historical docs discussed refresh and staleness. | Could be upstream, projection-local, or consumer-local only. | Expiry is implemented; no universal freshness threshold exists. | Freshness is mixed: source/support evidence, projection rules, and consumer purpose all may matter. | General freshness policy remains predicate/purpose-specific. |
| current standing | Projection docs named current lawful condition. | Current projected material could be treated as constitutional standing. | Current getters select support; Views expose compact material. | Current standing requires responsible boundary preserving evidence, authority, freshness, conflicts, expiry, and Unknowns. | Which current Views satisfy this remains a later repair question. |
| projection time | Projection store exposes snapshot created time. | Could be mistaken for source or consumption time. | `ProjectionSnapshot.created_at` and `last_event_id` are separate fields. | Snapshot time is projection-local and as-of boundary is ledger append sequence. | Direct projections may not expose creation time. |
| consumer applicability | Uptake chapter already local. | Temporal applicability was not explicit. | No general consumer uptake time is recorded. | Consumers newly judge purpose fit, freshness, expiry, conflict, authority, scope, and reliance time. | Consumer uptake recording remains sparse. |
| temporal selection | Selection grammar existed. | Selecting by time could be mistaken for asserting time. | Builders consume support times and expiry without exposing them in `FactView`. | Temporal selection is builder use of temporal evidence, separate from asserted standing. | View-specific contracts must declare assertion strength. |
| temporal disclosure | Projection losslessness existed generally. | It did not say which temporal details must be direct. | Current FactView and ObservationView omit material upstream temporal fields. | A View must disclose temporal distinctions constitutive of its own asserted standing; other details may remain navigable. | Future Views may choose fields, split surfaces, or narrowed assertions. |
| `ObservationView` | Projection chapter said it exposes source-attributed observation testimony and supporting ids. | Could imply sufficient testimony-time or current representation. | Dataclass exposes id, type, summary, supporting ids only. | It is an observation navigation index/source-attributed testimony surface, not currentness, expiry, verification, or full time disclosure. | Whether an operator-facing testimony View needs more disclosure is unresolved. |
| `FactView` | Projection chapter called it projected normalized fact/support material and sometimes current fact view. | Could imply current-standing disclosure. | Dataclass exposes no observed/latest/expiry/as-of fields. | It is compact projected normalized fact/support inventory; not a complete current-standing View by itself. | Later repair must decide whether to narrow assertion, expose, split, or explain. |

## Compactness versus loss

- Lawful compact representation: omits upstream timestamps that do not define the View's own claim and keeps supporting ids or provenance paths sufficient for audit.
- Lossy but honest navigation index: omits constitutive upstream details because it refuses currentness, verification, expiry, or reliance standing and signals that stronger judgment requires reopening provenance.
- Insufficient disclosure: asserts currentness, non-expiry, freshness, as-of selection, or verification applicability while hiding the boundary that makes that assertion interpretable.
- Misleading assertion: lets consumers read preserved material, latest support, non-expiry, or View visibility as lawful reliance without a declared temporal method, scope, boundary, and Unknowns.

## View contracts recovered

`ObservationView` is authorized to assert that projected Observation material exists in a compact navigation form: observation identity, source type, summary, and supporting ids. It is not authorized, in its current public shape, to assert observed-time standing, expiry interpretation, current applicability, verification, or sufficient testimony representation.

`FactView` is authorized to assert compact projected normalized fact/support inventory material selected by the state-view builder. It is not authorized, in its current public shape, to assert Fact-establishment time, public support-window disclosure, non-expiry, freshness sufficiency, projection as-of boundary, or consumer applicability. Describing it as "current projected claims" is only safe if "current" is read as internal projection/support selection, not as disclosed current constitutional standing for reliance.

## Why broader amendment was not warranted

The current Book already had the seams needed: artifact standing, lenses/views/roads, testimony and Fact standing, state/projection, and handoff/uptake. The repository did not warrant a new global temporal lifecycle, `TemporalStanding` object, validity interval model, new View fields, renamed fields, or implementation repair. The missing constitutional work was to clarify boundaries and disclosure contracts in the existing chapters.

## Unresolved questions

- Which current public Views fail the amended temporal assertion and disclosure contracts, and what is the smallest repository-warranted repair for each?
- Which producers, predicates, and source families establish broader Fact standing beyond weak source-relative observed claims?
- Which claim families require temporal material in dimensions, predicate semantics, support scope, or provenance during normalization?
- Which verification surfaces should disclose aging, expiry, method scope, or reliance limits directly rather than only through provenance?
- Which egress producer, if any, records requirement, request, emission, external receipt, realization, response, ingress, and new Observation times?
