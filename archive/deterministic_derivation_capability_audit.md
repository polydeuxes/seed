# Deterministic Derivation Capability Audit

## Status

Investigation only. No derivations were implemented, no forecasting was introduced, no statistical models were introduced, and no dashboard output was added.

The audit finding is that Seed already preserves enough projected State to support a small deterministic derivation layer, but the first slice should be narrow and explicitly separated from forecasts, estimates, and planning.

## Audit question

Which useful derived values can be calculated from existing projected `State`, using only deterministic information already preserved?

The audit starts from facts Seed already possesses rather than from operator desires. Usefulness is evaluated only after input availability and determinism are established.

## Files inspected

Primary files inspected:

- `seed_runtime/state.py`
- `seed_runtime/facts.py`
- `seed_runtime/predicate_catalog.py`
- `seed_runtime/predicate_normalizers.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/inference_rules.py`
- `predicate_catalog/core.json`
- `inference_catalog/core.json`
- `entity_type_catalog/core.json`
- `relationship_catalog/core.json`
- `tests/test_fact_support_aggregation.py`
- `tests/test_state_summary_views.py`
- `tests/test_inference_catalog.py`
- `IMPLEMENTATION.md`
- `docs/archive/original_book_of_seed/03-runtime-loop.md`
- `docs/archive/original_book_of_seed/06-context-engine.md`
- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`
- Relevant `docs/` audits concerning projection, storage, response, and lifecycle boundaries.

## Existing measurement inventory

Seed's canonical predicate catalog already marks these predicates as measurements:

| Predicate | Value type | Cardinality | Notes |
| --- | --- | --- | --- |
| `availability_status` | enum: `up`, `down`, `unknown` | single | Canonical availability measurement. Prometheus `up` maps to it. |
| `filesystem_free_bytes` | integer | single | Canonical current free/available bytes measurement. Prometheus filesystem availability predicates map to it. |
| `filesystem_total_bytes` | integer | single | Canonical current filesystem size measurement. Prometheus filesystem size predicates map to it. |
| `health_status` | enum: `ok`, `degraded`, `unknown` | single | Measurement. Some values are inferable from availability. |
| `interface_operstate` | string | multi | Interface state measurement. |
| `local_observation_status` | enum: `observed` | single | Measurement representing local observation status. |

The legacy measurement predicate set in `seed_runtime/facts.py` additionally preserves raw/provider predicates while migration to canonical predicates continues:

- `up`
- `filesystem_avail_bytes`
- `filesystem_size_bytes`
- `disk_free_bytes`
- `disk_total_bytes`

Filesystem-specific inventory discovered:

- Raw Prometheus `node_filesystem_avail_bytes` and `filesystem_avail_bytes` normalize to `filesystem_free_bytes`.
- Raw Prometheus `node_filesystem_size_bytes` and `filesystem_size_bytes` normalize to `filesystem_total_bytes`.
- Filesystem measurements carry dimensions such as `mountpoint`, `device`, and `fstype` when provided by the source.
- `storage_state_projection` already joins `filesystem_free_bytes` and `filesystem_total_bytes` by canonical host, mountpoint, and full dimensions key, and emits complete filesystem rows with `host`, `mountpoint`, `free`, `total`, and optionally `fstype`.
- Storage projections already compute presentation-only filesystem categories, cluster mount visibility, shared-storage candidates, and storage topology ambiguities. These are projection-only interpretations, not facts, ownership assertions, identities, or topology truth.

State/projection inventory relevant to derivations:

- `State` contains raw facts, observed facts, inferred facts, observations, evidence, fact supports, fact conflicts, relationships, entity aliases, entity type assertions, graph issues, tool needs, plans, and other projected artifacts.
- Fact support aggregation groups claims by subject, predicate, value, and dimensions. Durable facts aggregate support; measurements represent current samples.
- Measurement projection keeps the latest current sample by default and can retain bounded recent measurement history for debugging when `measurement_history_limit` is configured.
- Entity aliases, entity relationships, entity type assertions, relationship graph traversal, graph validation issues, stale facts, current facts, and current best facts are already deterministic State read surfaces.
- Existing inference rules derive `managed_by` from `runtime` and `health_status` from `availability_status`.
- State summary views already compute deterministic counts and grouped views over current State, including availability counts by scope and storage projection summaries.

## Candidate deterministic derivations (Class A)

Class A candidates require only current projected State and deterministic formulas.

| Candidate | Inputs required | Inputs already exist? | Deterministic formula | Historical data required? | Assumptions required? | Potential consumer surfaces |
| --- | --- | --- | --- | --- | --- | --- |
| `filesystem_used_bytes` | Current `filesystem_total_bytes` and `filesystem_free_bytes` for same canonical subject and same filesystem dimensions. | Yes, when both measurements exist. `storage_state_projection` already joins complete rows. | `used_bytes = total_bytes - free_bytes`; valid only when `0 <= free <= total`. | No. | No, beyond rejecting invalid/incomplete rows. | Storage projection, current facts/lens, explanation, context selection. |
| `filesystem_used_percent` | Same as above. | Yes, when both measurements exist and total is positive. | `used_percent = ((total - free) / total) * 100`. | No. | No, if total is positive. | Storage projection, lens-only filesystem detail, possible derived fact later. |
| `filesystem_free_percent` | Same as above. | Yes, when both measurements exist and total is positive. | `free_percent = (free / total) * 100`. | No. | No, if total is positive. | Storage projection, lens-only filesystem detail, possible derived fact later. |
| Filesystem pressure band | Current deterministic used or free percent plus explicit thresholds. | Partially. Inputs exist; thresholds do not exist as repository facts or catalog policy. | Example formula would classify percent into bands. | No. | Yes unless thresholds are introduced as explicit policy/config. | Do not promote until threshold authority exists. |
| Availability counts | Current `availability_status` by projected entity/scope. | Yes. State summary already counts `up`, `down`, and `unknown` by endpoint, host, and service scope. | `count(status) / total scoped entities` for ratios; counts already exist. | No. | No for counts/ratios over current scope; scope classification is already bounded by state summary rules. | State summary, context, response, integrity. |
| Availability ratios | Availability counts and scoped total. | Yes. | `up_ratio = up / total`, `down_ratio = down / total`, `unknown_ratio = unknown / total`, with zero-total handling. | No. | No if scope is explicit. | State summary lens or derived summary value. |
| Fact age | `Fact.observed_at` and evaluation time. | Yes. | `age = now - observed_at` or `now - latest_observed_at` for support. | No. | Requires explicit `now` parameter for deterministic tests; no domain assumptions. | Integrity, stale-fact view, explanation, refresh recommendation context. |
| Observation age | `Observation.observed_at` and evaluation time. | Yes. | `age = now - observed_at`. | No. | Requires explicit `now` parameter. | Observation view, context freshness, explanation. |
| Support age / latest support age | `FactSupport.observed_at`, `FactSupport.latest_observed_at`, and evaluation time. | Yes. | `first_age = now - observed_at`; `latest_age = now - latest_observed_at`. | No. | Requires explicit `now` parameter. | Explanation, confidence/integrity, current facts. |
| Expiry remaining / expired flag | `expires_at` and evaluation time. | Yes. Expiry checks already exist. | `remaining = expires_at - now`; `expired = expires_at <= now`. | No. | Requires explicit `now` parameter. | Stale/integrity surfaces, context. |
| Current measurement count | Current measurement facts. | Yes. State summary already exposes `measurement_current_sample_count`. | Count unexpired facts whose predicate has measurement semantics. | No. | No. | State summary. |
| Durable fact count | Non-measurement facts. | Yes. State summary already exposes it. | Count facts not classified as measurements. | No. | No. | State summary. |
| Conflict ratios | `fact_conflicts`, fact/support counts. | Yes. | `conflict_ratio = conflict_count / fact_or_support_count`. | No. | Denominator choice must be explicit. | Integrity summary/lens. |
| Graph issue ratios | `graph_issues` and relationship/entity counts. | Yes. | Count by severity; optional ratio over relationships or entities. | No. | Denominator choice must be explicit. | Graph integrity summary/lens. |
| Entity type ambiguity count | Current entity type assertions. | Yes. | Count entities where strongest current types has length greater than one or only `unknown`. | No. | No if ambiguity definition matches existing `get_current_entity_types`. | Graph/integrity summary. |
| Relationship degree / dependency counts | Projected relationships. | Yes. | Count incoming/outgoing relationships by kind; transitive reachability already exists for dependencies/dependents. | No. | No for counts; usefulness depends on consumer. | Relationship views, impact analysis, context. |
| Support source diversity | `FactSupport.source_types`. | Yes. | Count distinct source types per support group. | No. | No. | Explanation, confidence/integrity. |
| Capability verification counts | `capability_verified` facts and capability views. | Yes for facts/status surfaces. | Count statuses by value. | No. | No if scoped to projected capability facts. | Capability inventory/integrity. |

### Filesystem Class A conclusion

Current facts support `used_bytes`, `used_percent`, and `free_percent` without introducing assumptions when the following are true:

1. a current `filesystem_free_bytes` measurement exists;
2. a current `filesystem_total_bytes` measurement exists;
3. both measurements refer to the same canonical subject and same filesystem dimensions/mountpoint; and
4. `total_bytes > 0` and `0 <= free_bytes <= total_bytes`.

`storage_state_projection` already proves the join shape exists by producing complete filesystem rows with `free` and `total`. A future implementation could calculate these values as projection-only fields in that storage lens first, before deciding whether they deserve durable derived facts.

Filesystem pressure indicators are not currently pure derivations unless their thresholds are explicitly provided by repository policy/config/catalog. The repository can deterministically calculate pressure inputs (`used_percent`, `free_percent`), but labels such as `warning`, `critical`, or `pressure` would otherwise smuggle in assumptions.

## Candidate historical deterministic derivations (Class B)

Class B candidates require historical measurements but no forecasting assumptions.

| Candidate | Inputs required | Inputs already exist? | Deterministic formula | Historical data required? | Assumptions required? | Potential consumer surfaces |
| --- | --- | --- | --- | --- | --- | --- |
| Filesystem free-bytes delta | Two or more retained filesystem free measurements for same subject/dimensions. | Partially. Projection defaults to latest measurement only; bounded history can be retained with `measurement_history_limit`. Event ledger still preserves events. | `delta = current_free - previous_free`. | Yes. | No, if both samples are explicit and ordered. | Debug/history lens; not current fact by default. |
| Filesystem used-bytes delta | Two or more retained total/free pairs, or used bytes calculated for each sample. | Partially, same history caveat. | `delta_used = current_used - previous_used`. | Yes. | No. | Storage history lens. |
| Filesystem change rate | Two or more samples with timestamps. | Partially. | `rate = delta_bytes / delta_seconds`. | Yes. | No for observed interval rate; no extrapolation. | Historical measurement lens. |
| Availability over observed samples | Historical `availability_status` samples. | Partially. Current State defaults to latest measurement; ledger/history can contain older samples. | `availability_ratio_observed = up_samples / total_samples` for retained interval. | Yes. | Requires explicit observation window, but no forecast assumption. | Historical availability lens. |
| Observation cadence | Multiple observations from same source/subject/predicate. | Partially. | Differences between consecutive `observed_at` values. | Yes. | No for observed cadence; future cadence prediction would be forecast. | Source integrity/debug. |
| Fact churn / support growth over time | Multiple fact/support samples or event history. | Partially. | Count changes or new support events per interval. | Yes. | Window must be explicit. | Integrity/history audit. |
| Relationship changes | Historical relationship-generating facts/events. | Partially through ledger; current State is current projection. | Set difference between relationship projections at two times/snapshots. | Yes. | No. | Topology audit/history. |

Class B values are deterministic if they only describe observed past intervals. They should not be promoted as forecasts. Their main architectural complication is that projected `State` is intentionally current-oriented for measurements, while event history or an explicit history lens is needed for interval calculations.

## Candidate forecasts / estimates (Class C)

Class C candidates require history plus extrapolation or other assumptions. They should be identified, not promoted into deterministic derivations.

| Candidate | Inputs required | Inputs already exist? | Why not Class A/B? | Assumptions required? | Potential future surface |
| --- | --- | --- | --- | --- | --- |
| `time_to_full` | Filesystem current free/used, historical change rate, and future continuation assumption. | Current inputs exist when filesystem total/free exists; history only partially exists via ledger/configured retention. | It predicts a future threshold crossing. | Assumes past rate continues, no cleanup, no workload shift, no capacity change. | Forecast module only, after explicit forecasting architecture. |
| Predicted exhaustion date | Same as `time_to_full`. | Same as above. | Future prediction. | Same as above. | Forecast module only. |
| Future availability | Historical availability samples and model/assumption. | Historical samples may exist; model does not. | Predicts future state. | Requires model or assumption. | Forecast module only. |
| Trend extrapolation | Historical measurements and extrapolation method. | Partially. | Extrapolates beyond observed interval. | Requires model/window assumptions. | Forecast module only. |
| Capacity planning recommendation | Derived metrics, forecasts, goals, and policy thresholds. | Not as deterministic facts. | Planning/recommendation, not derivation. | Requires goals, thresholds, operator policy, future assumptions. | Planning layer only. |

### `time_to_full` distinction

`time_to_full` is not a pure deterministic derivation from current projected State. Even with `used_bytes`, `used_percent`, and `free_percent`, `time_to_full` requires at least one of the following:

- historical measurements to compute an observed consumption rate; and
- an assumption that the observed rate continues into the future.

A past observed rate can be Class B. The future crossing time is Class C.

## High-value derivations

High-value candidates supported by repository evidence:

1. Filesystem `used_bytes`, `used_percent`, and `free_percent` as projection-only storage lens fields.
2. Availability ratios by existing explicit scope (`endpoint_scrape_availability`, `host_availability`, `service_availability`).
3. Fact/support/observation age and expiry remaining, with explicit `now` supplied by callers/tests.
4. Support source diversity and support age for explanation/integrity surfaces.
5. Relationship degree/dependency counts as relationship-view lens values.

Filesystem percent values are the strongest first slice because the repository already projects complete current filesystem rows and already treats storage topology interpretations as projection-only.

## Architectural fit analysis

### Inferred facts

Existing inferred facts are catalog-driven deterministic facts derived from observed facts. They are appropriate when the result is itself a claim Seed may explain as a fact, such as `runtime=docker -> managed_by=docker_container_lifecycle` or `availability_status=up -> health_status=ok`.

Numeric filesystem percentages could become inferred/derived facts later, but doing so immediately would increase fact vocabulary and conflict/support semantics. It would also require deciding predicate names, precision, rounding, dimensions, and whether derived numeric facts participate in conflict detection.

### Derived facts

A distinct `derived fact` concept could be useful if Seed wants to preserve deterministic formulas and source fact IDs without treating the output as direct observed/inferred semantic truth. However, the repository currently has `inferred=True`, `source_fact_id`, and `inference_rule_id`, not a separate derivation model.

A future derived-fact layer should be considered only after a lens-only prototype proves consumers need persistence or explanation as first-class facts.

### Fact supports

Fact supports already aggregate support and expose first/latest observation times, source types, confidence, dimensions, and measurement semantics. They are a good source for age, support diversity, and current-vs-expired characterization. They are not a good place to store filesystem used percent because support describes provenance for a claim, not arithmetic across two different predicates.

### Projection-only values

Projection-only values are the best fit for the first filesystem slice. `storage_state_projection` already joins free and total measurements into filesystem rows without creating new facts, relationships, ownership, or topology truth. Adding deterministic arithmetic there later would preserve the existing boundary.

### Lens-only calculations

Lens-only calculations are the safest initial architecture for values that help inspection but should not become facts yet. Examples: filesystem percentages, availability ratios, age displays, relationship degree counts, and support diversity counts.

### Existing architecture boundary

Seed documentation already distinguishes observed facts, inferred facts, supporting facts, conflicting facts, and current belief. It also describes State Views as deterministic read-only projections from `State`. This supports a narrow derivation capability as a read-only projection/lens concern before any forecasting or planning layer.

## Recommended first derivation slice

Recommended first implementation slice, when implementation is requested later:

1. Keep it lens/projection-only.
2. Add filesystem arithmetic to `storage_state_projection` rows only:
   - `used_bytes`
   - `used_percent`
   - `free_percent`
3. Use only rows already complete with `free` and `total`.
4. Do not emit pressure labels unless thresholds are explicitly introduced as repository-owned policy/config/catalog data.
5. Do not compute `time_to_full`.
6. Add tests proving:
   - calculations are deterministic;
   - invalid totals/free values are omitted or marked invalid without assumptions;
   - no new facts, relationships, ownership assertions, or forecasts are created.

Secondary later slices:

- Availability ratios in state summary.
- Fact/support/observation age in integrity/explanation lenses with explicit `now`.
- Historical deltas/rates only in an explicit history lens, not current State facts.

## Non-conclusions

This audit does not conclude that Seed should introduce forecasting.

This audit does not conclude that `time_to_full`, predicted exhaustion, future availability, trend extrapolation, or capacity planning are deterministic derivations.

This audit does not conclude that filesystem pressure labels are currently available without introducing threshold policy.

This audit does not conclude that storage candidates are facts, ownership assertions, shared-storage identities, or topology truth.

This audit does not implement any derivation layer.

## Summary answer

A small derivation layer is supported before forecasting or planning is considered, but it should initially be a read-only projection/lens layer. The strongest first candidate is filesystem arithmetic over already joined current measurements: `used_bytes`, `used_percent`, and `free_percent`. Historical deltas/rates are deterministic only over retained/event history. `time_to_full` and predicted exhaustion remain forecast-only because they require future-continuation assumptions.
