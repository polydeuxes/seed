# Recording and Knowledge Extraction

## Constitutional subject
The boundary between preserving events or diagnostic output and deriving knowledge from recorded material.

## Core question
Which bounded responsibility may examine recorded material, and what standing, if any, may it establish?

## Bounded resolution
A recording boundary may create a retrievable representation of attributed events or findings within the preservation horizon supplied by the recorder. Examination or extraction from recorded material is a separate constitutional responsibility with its own evidence, reconciliation, and standing limits; successful extraction does not itself establish knowledge. Diagnostic recording should remain scoped to its diagnostic run unless a separate establishment boundary supplies additional standing.


## Addressable boundaries for recorded-change witnesses

### 05.Recording.A — Recorded assertion standing
A recording boundary may create retrievable assertion-bearing material within its declared preservation horizon. The produced standing is that a record exists and preserves an attributed assertion. The permitted reliance is examination of that recorded assertion as recorded material. The forbidden inference is that the represented external occurrence, current lawful state, factual truth, renewed occurrence, or consumer receipt has been established merely because the record exists or remains retrievable.

### 05.Recording.B — Diagnostic or examination-scoped recording
When recorded material is admitted only for diagnostic or examination purposes, consumers must preserve the scoped subject of that recording unless a separate establishment boundary supplies additional standing. The produced effect is bounded availability for examination, not mutation of cluster truth, universal state, reliance, or receipt.

## Important distinctions
- act occurrence != recording occurrence
- record exists != recorded assertion true automatically
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
