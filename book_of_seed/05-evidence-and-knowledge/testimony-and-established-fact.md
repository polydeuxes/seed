# Testimony and Established Fact

## Constitutional subject
The boundary between a source's claim or diagnostic finding and a fact with established standing in Seed.

## Core question
Which source, support, reconciliation, and promotion conditions establish a fact?

## Bounded resolution
A Claim is the semantic proposition carried by testimony, observations, evidence payloads, fact artifacts, relationships, projections, explanations, documentation, or consumer assertions. The Book does not currently recognize a separate durable `Claim` artifact as the universal subject of knowledge; claim-centricity means the proposition is not identical to any one storage object and must keep its source, scope, interpretation, support, confidence, conflict, and authority limits as it moves through different artifacts and standings. Claim expression, claim interpretation, normalization, support, establishment, current selection, and verification are distinct boundaries.

Normalization canonicalizes an interpreted claim into Seed's subject, predicate, value, dimensions, time, source, and provenance vocabulary so it can be compared, supported, projected, contradicted, or explained. Normalization does not create a new constitutional subject by itself, does not prove the interpreted claim, does not supply support, and does not require a `NormalizedClaim` class or schema.

A Fact has two safe meanings that must not be collapsed. As implementation vocabulary, a `Fact` artifact is a normalized fact-shaped representation with fields such as subject, predicate, value, dimensions, source type, confidence, timestamps, inference links, and evidence references. As constitutional vocabulary, a Fact is an established, evidence-backed, normalized, scoped claim whose standing does not exceed its producing evidence, source authority, and production boundary. A Fact is not objective truth, universal truth, selected current state, verified state, or proof that every support reference is resolved. A Fact artifact does not prove its own Fact standing; constructor availability, schema validity, replay, view visibility, or ledger presence may preserve or reconstruct an assertion but do not by themselves show that the establishing boundary occurred.

Fact standing requires claim-appropriate evidence support, normalization, scope preservation, source or producer authority sufficient for the claim strength, and conflict awareness at the boundary where the claim is established or later consumed. One Observation may support a bounded Fact when the Fact asserts no more than the source-relative observation can support, such as that the source reported the predicate/value at the preserved time, vantage, dimensions, confidence, and expiry limit. Broader claims, live-state claims, authority-heavy claims, verification claims, or claims that erase the source-relative boundary require stronger producer evidence, corroboration, method-specific verification, or consumer-local standing as appropriate. Contradiction, staleness, expiry, historical supersession, or loss of current selection does not delete a Fact's preserved standing or provenance; it changes later confidence, conflict, projection, current-standing, or verification determinations.

The current repository compresses Observation intake, Evidence construction, claim-field normalization, optional Fact artifact construction, and fact event emission in `ObservationIngestor`. The Book recognizes that compression as implementation testimony, not as a universal constitutional rule. It is constitutionally safe for weak source-relative observed Facts when scope and claim strength are preserved. Whether each producer, predicate, source, or stronger observation-to-Fact path establishes broader Fact standing remains Unknown until producer-specific evidence proves the boundary. A consumer may use testimony as a source-relative or premise-relative input for a new local assertion, but coherence checks and copied lineage fields do not turn testimony into established fact or prove the testifying producer occurred.


## Addressable boundaries for support-binding witnesses

### 05.Testimony.A — Premise-relative testimony without fact standing
A recorded claim, diagnostic finding, or evidence record may be consumed as attributed testimony or premise-relative input for a bounded examination. That consumption preserves attribution, source-relative limits, conflicts, and uncertainty; it does not establish the testified content as fact, prove the source producer occurred, or strengthen standing merely through repetition or copied lineage.

## Important distinctions
- claim expression != claim interpretation
- claim interpretation != normalization
- normalization != support
- support != establishment automatically
- Fact artifact != Fact standing
- Fact standing != selected current standing
- selected standing != verified standing
- verification != universal truth
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
