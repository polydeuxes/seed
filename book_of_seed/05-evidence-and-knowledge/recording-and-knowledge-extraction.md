# Recording and Knowledge Extraction

## Constitutional subject
The boundary between preserving events or diagnostic output and deriving knowledge from recorded material.

## Core question
Which explicit process may extract, reconcile, and establish knowledge from a record?

## Initial resolution
Recording preserves attributable events and findings. Knowledge extraction is a separate process with normalization, evidence, reconciliation, and standing rules; diagnostic recording should remain scoped to its diagnostic run unless explicitly promoted.

## Important distinctions
- act occurrence != recording occurrence
- record exists != recorded assertion true automatically
- extraction occurrence != original execution occurrence
- recording != knowledge extraction
- event ledger write != cluster mutation
- durable record != established fact

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
