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


### 05.Recording.C — Preservation and discard of operational measurements
Seed need not preserve every operational measurement. Non-rebuildable is not equal to preservation-required: a raw measurement that cannot be reconstructed after process exit is preserved only when discarding it would erase material evidence or understanding of reality not otherwise retained. Seed must preserve sufficient evidence or compressed standing to retain its materially sufficient understanding of operational reality. Preservation decision != standing-establishment decision: recording may preserve attributed testimony or already established standing, but record exists != recorded standing was lawfully established. A measurement within an established tolerance may be discarded when its loss does not alter or erase that understanding. A material deviation must preserve sufficient measurement and comparison context to retain the challenge to prior understanding. When changed ordinary behavior is lawfully established, Seed may preserve the prior baseline, transition standing, new baseline, and sufficient supporting evidence without permanently retaining every contributing raw measurement.

### 05.Recording.D — Recording operational testimony and standing
Recording may preserve already produced measurement testimony and already produced runtime/resource observation testimony within its declared preservation horizon and standing limits. Recording may preserve already established baseline standing, deviation standing, or transition standing. It does not produce the testimony, establish ordinary behavior, perform comparison, recognize material deviation, establish baseline transition, or create authority for future prediction merely by storing a representation. Recording a measurement series does not establish an operational baseline. Recording a difference does not establish material deviation. Recording repeated samples does not establish a baseline transition.



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
- [Acts and act artifacts](../02-acts-and-constraints/acts-and-act-artifacts.md)
