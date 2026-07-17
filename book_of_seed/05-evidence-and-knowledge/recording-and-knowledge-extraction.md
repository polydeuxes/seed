# Recording and Knowledge Extraction

## Constitutional subject
The boundary between preserving events or diagnostic output and deriving knowledge from recorded material.

## Core question
Which explicit process may extract, reconcile, and establish knowledge from a record?

## Bounded resolution
Recording creates a retrievable representation of attributable events and findings within the preservation horizon supplied by the recorder. Knowledge extraction is a separate process with normalization, evidence, reconciliation, and standing rules; diagnostic recording should remain scoped to its diagnostic run unless explicitly promoted.


## Addressable boundaries for recorded-change witnesses

### 05.Recording.A — Recorded assertion standing
A recording boundary may create retrievable assertion-bearing material within its declared preservation horizon. The produced standing is that a record exists and preserves an attributed assertion. The permitted reliance is examination of that recorded assertion as recorded material. The forbidden inference is that the represented external occurrence, current lawful state, or factual truth has been established merely because the record exists.

### 05.Recording.B — Diagnostic or examination-scoped recording
When recorded material is admitted only for diagnostic or examination purposes, consumers must preserve the scoped subject of that recording unless a separate promotion or establishment boundary supplies additional standing. The produced effect is bounded availability for examination, not mutation of cluster truth or universal state.

## Important distinctions
- act occurrence != recording occurrence
- record exists != recorded assertion true automatically
- extraction occurrence != original execution occurrence
- recording != knowledge extraction
- event ledger write != cluster mutation
- retrievable record != established fact
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
