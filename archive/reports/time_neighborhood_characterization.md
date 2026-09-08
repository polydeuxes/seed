# Time Neighborhood Characterization

## Boundary

This is exactly one bounded Characterization of already surveyed Time evidence.
It does not perform another survey, recover new neighborhoods, recover bridges,
recover topology, recover ownership, recover scheduling, recover runtime behavior,
identify a Town Clock, identify central neighborhoods, infer architectural
importance, or recommend implementation.

Repository authority wins.

## Surveyed neighborhoods reviewed

The characterization reviews only the Time neighborhoods already visible in prior
survey and reconciliation evidence:

1. **Occurrence / external-reality time**
2. **Observation / collection time**
3. **Source sample / source-asserted time**
4. **Knowledge / justification time**
5. **Preservation / event-ledger time**
6. **Temporal claim / revision time**
7. **Diagnostic elapsed / phase timing**
8. **Progress cadence / status timing**
9. **Cache visibility time**

These labels are comparison handles for already surveyed evidence, not earned
repository identities.

## Comparative characterization

### 1. Occurrence / external-reality time

**Recurring distinguishing characteristics**

- Distinguished by referring to when the external condition happened, not when
  Seed observed, learned, preserved, sampled, rendered, or timed work.
- Recurs as usually unavailable directly to Seed.
- Recurs as something that may be inferred, asserted, bounded, or supported by
  evidence rather than copied from a universal field.
- Locally distinctive preserved unknown: for many changes, Seed does not know
  the exact occurrence instant.

**Comparative evidence supporting the distinction**

- Unlike observation time, occurrence time is not the collection/read/report
  moment.
- Unlike source sample time, it is not automatically the upstream source's sample
  timestamp.
- Unlike knowledge time, it is not when Seed became justified in using support.
- Unlike preservation time, it is not the event timestamp in Seed's append-only
  history.
- Unlike diagnostic elapsed timing, it is about external reality rather than
  measuring Seed's own diagnostic work.

**Confidence**

High that this neighborhood is distinct in the reviewed evidence, because the
prior reconciliations repeatedly preserve non-collapse between occurrence time
and every Seed-facing or source-facing timestamp.

**Preserved unknowns**

- Whether a specific occurrence has an exact recoverable instant remains unknown
  unless separate support establishes it.
- Whether future schemas should represent occurrence-time claims differently is
  outside this characterization.

### 2. Observation / collection time

**Recurring distinguishing characteristics**

- Distinguished by recording when a source, adapter, operator path, import path,
  or Seed collection action observed, sampled, read, reported, or accepted
  evidence.
- Recurs as evidence provenance, not occurrence authority.
- Locally distinctive behavior in prior evidence: local host collection and
  Prometheus collection use a Seed/client collection timestamp for observations;
  manual CLI observations use ingestion time; JSON imports may preserve supplied
  `observed_at` or use a default.

**Comparative evidence supporting the distinction**

- Compared with occurrence time, observation time can happen later than the
  external condition.
- Compared with source sample time, observation time may be Seed's collection
  clock rather than the upstream source clock.
- Compared with preservation time, observation time can precede ledger
  persistence.
- Compared with knowledge time, it is evidence collection/report timing, not the
  full justification boundary.

**Confidence**

High for the distinction from occurrence, source sample, and preservation time;
medium for exact boundaries with knowledge time because prior evidence describes
knowledge time as close to ingestion/evidence construction without collapsing it
into observation time.

**Preserved unknowns**

- Whether every observation path preserves clock provenance consistently remains
  unresolved in the prior evidence.
- Whether an observed timestamp was source-asserted, defaulted, normalized, or
  derived remains only partially distinguished in current surveyed evidence.

### 3. Source sample / source-asserted time

**Recurring distinguishing characteristics**

- Distinguished by being supplied by an upstream source for a sample or record.
- Recurs as a source temporal assertion with clock authority questions.
- Locally distinctive artifact: Prometheus vector results include a sample
  timestamp separate from the sample value.
- Locally distinctive preserved unknown/gap: surveyed Prometheus ingestion
  describes source sample timestamp loss where Seed substitutes collection time
  as observation time.

**Comparative evidence supporting the distinction**

- Compared with observation time, source sample time belongs to the upstream
  source's timestamped sample rather than Seed's collection moment.
- Compared with occurrence time, source sample time may support an occurrence
  claim but does not become the occurrence itself.
- Compared with preservation time, source sample time is not Seed ledger event
  persistence.
- Compared with temporal claims, it is support material rather than the supported
  claim over when an occurrence happened.

**Confidence**

High that source sample time is distinct from Seed collection and preservation
surfaces; medium on all concrete source families because prior evidence names
Prometheus most clearly and leaves broader source provenance partly unresolved.

**Preserved unknowns**

- The clock reliability, authority, and normalization status of source-provided
  timestamps remain unresolved unless separately recorded.
- Whether other source adapters preserve or discard analogous source sample
  timestamps is not concluded here.

### 4. Knowledge / justification time

**Recurring distinguishing characteristics**

- Distinguished by when Seed became justified in using particular support.
- Recurs as close to ingestion, evidence construction, approval, or import time,
  but not identical to external occurrence time.
- Locally distinctive behavior: it marks justified use rather than external
  change or ledger preservation.

**Comparative evidence supporting the distinction**

- Compared with observation time, knowledge time concerns Seed's entitlement to
  use support, not merely the sampling/read/report moment.
- Compared with preservation time, knowledge time is not simply append-only event
  recording.
- Compared with occurrence time, a condition may predate Seed's knowledge of it.
- Compared with temporal claim revision, knowledge time can change as support
  changes without implying that external reality changed again.

**Confidence**

Medium-high. The prior evidence repeatedly distinguishes knowledge time from
occurrence and preservation, while preserving some ambiguity around its exact
implementation boundary.

**Preserved unknowns**

- The exact current implementation boundary between observation, ingestion,
  evidence construction, approval, and knowledge time remains incompletely
  resolved in the reviewed evidence.

### 5. Preservation / event-ledger time

**Recurring distinguishing characteristics**

- Distinguished by when Seed records something in append-only history or the
  event ledger.
- Recurs in prior evidence as the meaning of `Event.timestamp` in the current
  implementation.
- Locally distinctive behavior: projection replay order is append order, while
  the event timestamp is preservation context rather than external occurrence
  authority.

**Comparative evidence supporting the distinction**

- Compared with occurrence time, preservation time records Seed's preservation
  act, not the external event's happening.
- Compared with observation time, it can occur after collection or acceptance.
- Compared with source sample time, it is Seed ledger context rather than source
  clock context.
- Compared with diagnostic timing, it is durable ledger context rather than a
  diagnostic elapsed measurement.

**Confidence**

High that preservation/event-ledger time is distinct from occurrence,
observation, and source sample time in the reviewed evidence.

**Preserved unknowns**

- Whether future event schemas should add richer temporal provenance is outside
  this characterization.
- This characterization does not inspect ledger behavior or recover runtime
  behavior.

### 6. Temporal claim / revision time

**Recurring distinguishing characteristics**

- Distinguished by being a supported statement about time, especially occurrence
  time, rather than a raw timestamp field.
- Recurs as revisable: Seed's supported understanding can narrow, widen,
  supersede, weaken, strengthen, or dispute a claim without moving reality.
- Locally distinctive artifact shape in prior evidence: exact timestamps,
  intervals, bounds, estimates, confidence, support, derivation method, source
  clock metadata, and revision/supersession are named as possible claim metadata,
  but the exact schema remains future work.

**Comparative evidence supporting the distinction**

- Compared with source sample time and observation time, a temporal claim uses
  support rather than simply equaling the support timestamp.
- Compared with occurrence time, the claim is Seed's supported understanding of
  occurrence, not the occurrence itself.
- Compared with knowledge time, revisions track changes in justified temporal
  understanding, not merely the moment Seed became justified to use support.
- Compared with preservation time, a claim may be preserved by an event, but the
  event is not the claim's external occurrence.

**Confidence**

Medium-high. The distinction is strong in prior reconciliations, but concrete
implementation shape remains explicitly unresolved.

**Preserved unknowns**

- The exact temporal-claim schema is future work in the surveyed evidence.
- Whether current repository artifacts should preserve temporal claims as new
  records is unsupported here.

### 7. Diagnostic elapsed / phase timing

**Recurring distinguishing characteristics**

- Distinguished by measuring Seed's own diagnostic or projection/cache/audit work
  in elapsed durations and named phases.
- Recurs through local timing structures rather than a shared timing
  architecture.
- Locally distinctive behaviors: projection diagnostics use local subphase
  timing; state-build and current-facts cache debug use local `timed(...)`
  closures; knowledge reachability uses its own timer; observation ingestion
  diagnostics report collection/normalization/write durations and rates.
- Locally distinctive artifact grammar: phase/name plus elapsed seconds recurs,
  but prior evidence explicitly rejects treating this as a repository-wide timing
  schema.

**Comparative evidence supporting the distinction**

- Compared with occurrence, observation, source sample, knowledge, and
  preservation time, diagnostic elapsed timing measures internal work duration,
  not temporal provenance of claims or evidence.
- Compared with progress cadence, it reports durations or phase timings rather
  than merely deciding when status should be emitted.
- Compared with cache visibility time, it measures elapsed path costs while cache
  status explains which path was taken.

**Confidence**

High that diagnostic elapsed timing is distinct from temporal provenance
neighborhoods; high that ownership has not converged according to prior timing
visibility audit evidence.

**Preserved unknowns**

- Whether timing work should ever converge into a shared framework is
  unsupported by surveyed evidence.
- Whether phase labels should be normalized is unsupported here.

### 8. Progress cadence / status timing

**Recurring distinguishing characteristics**

- Distinguished by using elapsed wall-clock intervals only to gate transient
  progress/status emission.
- Recurs as status visibility rather than duration reporting.
- Locally distinctive behavior: cadence decides whether enough time or item
  progress has passed to emit a status; status itself is renderer-independent and
  non-authoritative.

**Comparative evidence supporting the distinction**

- Compared with diagnostic elapsed timing, cadence does not report measured
  phase durations.
- Compared with preservation time, status cadence is transient visibility, not
  ledger persistence.
- Compared with observation or occurrence time, it does not describe external
  evidence or external reality.

**Confidence**

High that progress cadence is distinct from diagnostic duration reporting in the
surveyed timing evidence.

**Preserved unknowns**

- Whether any future status surfaces should include durations is not supported
  here.

### 9. Cache visibility time

**Recurring distinguishing characteristics**

- Distinguished by explaining cache path status, snapshot identity, hit/miss,
  incremental replay, and events applied rather than owning elapsed measurement
  globally.
- Recurs around state/projection/current-facts/knowledge reachability cache
  visibility as path explanation.
- Locally distinctive behavior: cache status explains the measured path, while
  elapsed measurement is usually caller-owned.

**Comparative evidence supporting the distinction**

- Compared with diagnostic elapsed timing, cache visibility explains which cache
  path occurred; it is not the duration itself.
- Compared with preservation time, cache visibility is diagnostic/path context,
  not append-only event recording.
- Compared with knowledge or occurrence time, cache visibility is not a temporal
  claim about external facts.

**Confidence**

Medium-high. Prior timing evidence strongly distinguishes cache status from
elapsed measurement, while cache visibility appears in several local diagnostic
forms rather than one converged owner.

**Preserved unknowns**

- Whether cache visibility should be further separated or normalized is outside
  this characterization.
- Whether all cache-related time labels share one stable vocabulary is
  unsupported.

## Unsupported conclusions preserved

The reviewed evidence does not support concluding that:

- the surveyed Time neighborhoods have earned stable repository identities;
- any Time neighborhood is central;
- any Time neighborhood is the Town Clock;
- a universal Time topology exists;
- a universal timing framework is warranted;
- source timestamps are occurrence time;
- observation timestamps are occurrence time;
- event timestamps are external occurrence time;
- temporal-claim revision means reality changed again;
- diagnostic phase timing is a repository-wide schema;
- cache status is elapsed-time measurement;
- progress cadence is diagnostic duration reporting;
- presentation labels should be promoted into preserved knowledge.

## Repository-wide characterization

What distinguishes each surveyed Time neighborhood from its neighboring
neighborhoods?

- **Occurrence / external-reality time** is distinguished by the external thing
  that happened; neighboring evidence, source, knowledge, preservation, and
  diagnostic times can support or contextualize it but do not equal it.
- **Observation / collection time** is distinguished by the act of observing,
  sampling, reading, reporting, collecting, or accepting evidence; it is
  provenance of observation, not occurrence, source authority, or ledger
  preservation.
- **Source sample / source-asserted time** is distinguished by upstream clock
  assertion; it may support claims but remains source-provided temporal
  evidence, not Seed collection time or external occurrence time by default.
- **Knowledge / justification time** is distinguished by Seed's justified use of
  support; it neighbors observation and preservation but is not reducible to
  either.
- **Preservation / event-ledger time** is distinguished by Seed's append-only
  recording act; it provides event context without becoming external occurrence
  authority.
- **Temporal claim / revision time** is distinguished by supported, revisable
  statements about time; it compares and organizes support without equating the
  claim with any one timestamp.
- **Diagnostic elapsed / phase timing** is distinguished by measuring internal
  work durations in local diagnostic paths; it is operational visibility, not
  temporal provenance.
- **Progress cadence / status timing** is distinguished by transient emission
  gating; it decides when status appears without reporting authoritative
  durations or external time claims.
- **Cache visibility time** is distinguished by path explanation around cache
  use; it contextualizes measured work without owning elapsed measurement or
  external temporal truth.

Characterization complete.
