# Recording and Knowledge Extraction

## Constitutional subject
The boundary between preserving events or diagnostic output and deriving knowledge from recorded material.

## Core question
Which bounded responsibility may examine recorded material, and what standing, if any, may it establish?

## Bounded resolution
A recording boundary may create a retrievable representation of attributed events, findings, testimony, or established standing within the preservation horizon supplied by the recorder. Examination or extraction from recorded material is a separate constitutional responsibility with its own evidence, reconciliation, and standing limits; successful extraction does not itself establish knowledge. Diagnostic recording should remain scoped to its diagnostic run unless a separate establishment boundary supplies additional standing. Diagnostic rendering, metrics output, CLI report text, and operator capture are not Seed preservation by identity; Seed preservation, when warranted, belongs to the retained testimony or compressed standing and not to the external surface that displayed it. Operational measurement production, operational understanding establishment, diagnostic rendering, and recording/preservation are separate responsibilities. Recording may preserve already produced measurement testimony or already established baseline, deviation, or transition standing; it does not produce the upstream measurement, comparison authority, baseline standing, deviation standing, or transition standing merely by storing a representation.


## Addressable boundaries for recorded-change witnesses

### 05.Recording.A — Recorded assertion standing
A recording boundary may create retrievable assertion-bearing material within its declared preservation horizon. The produced standing is that a record exists and preserves an attributed assertion. The permitted reliance is examination of that recorded assertion as recorded material. The forbidden inference is that the represented external occurrence, current lawful state, factual truth, renewed occurrence, or consumer receipt has been established merely because the record exists or remains retrievable.

### 05.Recording.B — Diagnostic or examination-scoped recording
When recorded material is admitted only for diagnostic or examination purposes, consumers must preserve the scoped subject of that recording unless a separate establishment boundary supplies additional standing. The produced effect is bounded availability for examination, not mutation of cluster truth, universal state, reliance, or receipt.


### 05.Recording.C — Operational measurement production
An operational measurement is bounded testimony about the observed behavior of a particular operation instance under declared conditions and measurement method. The measurement-production responsibility produces that operation-instance testimony; recording is only one possible later preservation boundary. A measurement may identify operation, instance scope, phase, duration or resource behavior, clock or method, input scale, cache condition, environment or authority context, completion condition, and observation time as needed by its consumer, but no implementation must possess every dimension. Measuring a projection, cache lookup, query, rendering, observation collection, read-model construction, fact-index construction, diagnostic comparison, external realization, or other bounded operation does not make it execution by measurement alone. Diagnostic rendering may expose measurement testimony, but diagnostic rendering != measurement production and diagnostic rendering != measurement preservation. A measurement occurrence may exist transiently without ever becoming a recorded measurement; that does not make the measurement unreal and does not automatically make preservation mandatory. Recording measurement testimony != producing measurement testimony.

### 05.Recording.D — Runtime/resource observation boundary
Operation-instance measurement and ambient runtime/resource observation are not identical. Operation-instance measurement attributes behavior to a scoped operation instance. Ordinary runtime/resource observation is testimony about a process or runtime condition at an observed time, such as process resident memory, thread count, process runtime duration, database size, or ledger size, without necessarily attributing the value to one bounded operation instance. Runtime/resource observation may be produced through ordinary observation grammar and may exist without a recording boundary. Runtime/resource observation is not an operational baseline by identity and may support an operational measurement or baseline only through an explicit attribution and establishment boundary; recording is not its producer merely because a recorded observation can survive process exit.

### 05.Recording.E — Operational baseline, comparison, deviation, and transition establishment
An operational baseline is retained, scoped, evidence-supported understanding of ordinary operational behavior under declared conditions. Baseline establishment consumes sufficient measurement testimony, attributed runtime/resource observations where authorized, scope, context, temporal evidence, comparison method, conflicts, and uncertainty; baseline recording may preserve the resulting standing but does not establish ordinary behavior merely by retaining samples or a summary. An operational baseline is not a database table, raw timing history, retained measurement series, recorded summary, average, threshold, fixed artifact, runtime/resource observation, or predicted future duration by identity. It must preserve enough context to prevent comparison across constitutionally different subjects, such as cache hit and cache miss, full rebuild and incremental replay, fact-view inventory construction and subject/predicate selection, small and large inputs, or distinct environment and authority conditions. A comparison consumes an applicable baseline or other authorized comparison boundary and a measurement within a declared purpose and scope; comparison occurrence != recorded comparison. A tolerance or comparison boundary requires bounded authority: the baseline applied, the operation and conditions covered, the purpose of comparison, permitted variation, and the method by which that boundary was established. Difference from one prior sample is not material deviation. Material deviation recognition is an establishment decision that a difference is constitutionally material within the comparison authority; deviation recognition != deviation recording, and a recorded difference does not establish material deviation. A material deviation preserves enough measurement and comparison context to retain the challenge to prior understanding, including operation, applicable baseline or comparison standing, context, observed difference, comparison authority and purpose, and remaining uncertainty; it is not automatically an operation failure, lost capability, cause, or consequence. A baseline transition is evidence-supported establishment that ordinary operational behavior materially changed from one bounded regime to another; baseline transition establishment is distinct from transition recording, and baseline transition establishment != transition recording. One unusual sample is insufficient, and repeated samples are not sufficient merely by count without scope, conditions, comparison method, evidence sufficiency, conflict awareness, and temporal standing.

### 05.Recording.F — Preservation and discard of operational measurements
Seed need not preserve every operational measurement. Non-rebuildable is not equal to preservation-required: a raw measurement that cannot be reconstructed after process exit is preserved only when discarding it would erase material evidence or understanding of reality not otherwise retained. Seed must preserve sufficient evidence or compressed standing to retain its materially sufficient understanding of operational reality. Preservation decision != standing-establishment decision: recording may preserve attributed testimony or already established standing, but record exists != recorded standing was lawfully established. A measurement within an established tolerance may be discarded when its loss does not alter or erase that understanding. A material deviation must preserve sufficient measurement and comparison context to retain the challenge to prior understanding. When changed ordinary behavior is lawfully established, Seed may preserve the prior baseline, transition standing, new baseline, and sufficient supporting evidence without permanently retaining every contributing raw measurement.

## Important distinctions
- diagnostic rendering != Seed-consumable knowledge
- diagnostic rendering != measurement ownership
- diagnostic rendering != measurement production
- diagnostic rendering != measurement preservation
- operational measurement != recording
- measurement occurrence != recorded measurement
- recording measurement testimony != producing measurement testimony
- operational measurement != execution
- operational measurement != execution record
- operational measurement != operation result
- operation-instance measurement != ambient runtime observation
- runtime/resource observation != operational baseline
- operation measurement != operational baseline
- baseline establishment != baseline recording
- retained measurement series != operational baseline
- recorded summary != established ordinary behavior
- operational baseline != predicted future duration
- comparison != recording
- comparison occurrence != recorded comparison
- difference from one sample != material deviation
- material deviation recognition != deviation recording
- deviation != operation failure
- deviation != capability loss
- one unusual sample != changed ordinary behavior
- baseline transition establishment != transition recording
- non-rebuildable != preservation-required
- ExecutionStatus cadence != operation timing testimony
- execution status != operational measurement
- operator capture != Seed preservation
- operator omission != permission for Seed to forget
- Seed preservation != obligation to expose every sample externally
- act occurrence != recording occurrence
- record exists != recorded assertion true automatically
- record exists != recorded standing lawfully established
- preservation decision != standing-establishment decision
- extraction occurrence != original execution occurrence
- recording != knowledge extraction
- event ledger write != cluster mutation
- retrievable record != established fact
- preservation != renewed occurrence
- retrieval or availability != receipt or reliance
- successful extraction != knowledge establishment
- process-local record != cross-restart persistent record

## Representative repository anchors
- `seed_runtime/events.py::EventLedger`
- `seed_runtime/observations.py::ObservationIngestor`
- `seed_runtime/fact_extraction.py`

## Counterexamples or failure modes
- Assuming all ledger payloads become facts during replay.
- Attaching diagnostic-only output directly to hosts or services.

## Related chapters
- [Testimony and established fact](testimony-and-established-fact.md)
- [Events, facts, and state](../06-state-and-projection/events-facts-and-state.md)
- [Execution and recording](../07-operational-realization/execution-and-recording.md)
