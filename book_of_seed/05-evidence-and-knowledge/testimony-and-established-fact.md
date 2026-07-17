# Testimony and Established Fact

## Constitutional subject
The boundary between a source's claim or diagnostic finding and a fact with established standing in Seed.

## Core question
Which source, support, reconciliation, and promotion conditions establish a fact?

## Bounded resolution
Observations and specialized testimony preserve attributed claims. Fact standing requires explicit ingestion, support, normalization, and conflict-aware establishment rather than direct attachment of a finding to cluster truth. A consumer may use testimony as a source-relative or premise-relative input for a new local assertion, but coherence checks and copied lineage fields do not turn testimony into established fact or prove the testifying producer occurred.

## Important distinctions
- observer-held occurrence evidence != preserved occurrence evidence
- recorded testimony != established fact automatically
- testimony != established fact
- observation != belief
- diagnostic finding != cluster truth

## Representative repository anchors
- `seed_runtime/observations.py::ObservationIngestor`
- `seed_runtime/evidence.py::Evidence`
- `seed_runtime/facts.py::Fact`

## Counterexamples or failure modes
- Recording diagnostic-only findings directly against runtime entities.
- Treating repeated testimony as independent corroboration without source analysis.

## Related chapters
- [Evidence, provenance, and explanation](evidence-provenance-and-explanation.md)
- [Recording and knowledge extraction](recording-and-knowledge-extraction.md)
- [Questions and inquiry](../04-inquiry-and-examination/questions-and-inquiry.md)
