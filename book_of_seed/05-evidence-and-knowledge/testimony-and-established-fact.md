# Testimony and Established Fact

## Constitutional subject
The boundary between a source's claim or diagnostic finding and a fact with established standing in Seed.

## Core question
Which source, support, reconciliation, and promotion conditions establish a fact?

## Bounded resolution
A Claim is the semantic proposition carried by testimony, observations, evidence payloads, fact artifacts, relationships, projections, explanations, documentation, or consumer assertions. The Book does not currently recognize a separate durable `Claim` artifact as the universal subject of knowledge; claim-centricity means the proposition is not identical to any one storage object and must keep its source, scope, interpretation, support, confidence, conflict, and authority limits as it moves through different artifacts and standings. Claim expression, claim interpretation, normalization, support, establishment, current selection, and verification are distinct boundaries.

Normalization canonicalizes an interpreted claim into Seed's subject, predicate, value, dimensions, time, source, and provenance vocabulary so it can be compared, supported, projected, contradicted, or explained. Normalization does not create a new constitutional subject by itself, does not prove the interpreted claim, does not supply support, and does not require a `NormalizedClaim` class or schema.

A Fact has two safe meanings that must not be collapsed. As implementation vocabulary, a `Fact` artifact is a normalized fact-shaped representation with fields such as subject, predicate, value, dimensions, source type, confidence, timestamps, inference links, and evidence references. As constitutional vocabulary, a Fact is an established, evidence-backed, normalized, scoped claim whose standing does not exceed its producing evidence, source authority, and production boundary. A Fact is not objective truth, universal truth, selected current state, verified state, or proof that every support reference is resolved. A Fact artifact does not prove its own Fact standing; constructor availability, schema validity, replay, view visibility, or ledger presence may preserve or reconstruct an assertion but do not by themselves show that the establishing boundary occurred.

Fact standing requires claim-appropriate evidence support, normalization, scope preservation, source or producer authority sufficient for the claim strength, and conflict awareness at the boundary where the claim is established or later consumed. A Fact emission warrants that bounded standing for the proposition itself; it does not warrant universal truth, present applicability, verification, or operational permission unless those stronger standings are separately established and disclosed. A surface that exposes normalized claim material, Fact artifacts, FactSupport, or current selected rows without warranting establishment is a fact-shaped inventory or projected support View, not a constitutional FactView in the strong standing-bearing sense. One Observation may support a bounded Fact when the Fact asserts no more than the source-relative observation can support, such as that the source reported the predicate/value at the preserved time, vantage, dimensions, confidence, and expiry limit. Broader claims, live-state claims, authority-heavy claims, verification claims, or claims that erase the source-relative boundary require stronger producer evidence, corroboration, method-specific verification, or consumer-local standing as appropriate. Contradiction, staleness, expiry, historical supersession, or loss of current selection does not delete a Fact's preserved standing or provenance; it changes later confidence, conflict, projection, current-standing, or verification determinations.

The current repository compresses Observation intake, Evidence construction, claim-field normalization, optional Fact artifact construction, and fact event emission in `ObservationIngestor`. The Book recognizes that compression as implementation testimony, not as a universal constitutional rule. It is constitutionally safe for weak source-relative observed Facts when scope and claim strength are preserved. Whether each producer, predicate, source, or stronger observation-to-Fact path establishes broader Fact standing remains Unknown until producer-specific evidence proves the boundary. A consumer may use testimony as a source-relative or premise-relative input for a new local assertion, but coherence checks and copied lineage fields do not turn testimony into established fact or prove the testifying producer occurred.


## Addressable boundaries for support-binding witnesses

### 05.Testimony.A — Premise-relative testimony without fact standing
A recorded claim, diagnostic finding, or evidence record may be consumed as attributed testimony or premise-relative input for a bounded examination. That consumption preserves attribution, source-relative limits, conflicts, and uncertainty; it does not establish the testified content as fact, prove the source producer occurred, or strengthen standing merely through repetition or copied lineage.


### 05.Testimony.B — Operational measurement production
An operational measurement is bounded testimony about the observed behavior of a particular operation instance under declared conditions and measurement method. The measurement-production responsibility produces that operation-instance testimony; recording is only one possible later preservation boundary. A measurement may identify operation, instance scope, phase, duration or resource behavior, clock or method, input scale, cache condition, environment or authority context, completion condition, and observation time as needed by its consumer, but no implementation must possess every dimension. Measuring a projection, cache lookup, query, rendering, observation collection, read-model construction, fact-index construction, diagnostic comparison, external realization, or other bounded operation does not make it execution by measurement alone. Diagnostic rendering may expose measurement testimony, but diagnostic rendering != measurement production and diagnostic rendering != measurement preservation. A measurement occurrence may exist transiently without ever becoming a recorded measurement; that does not make the measurement unreal and does not automatically make preservation mandatory. Measurement occurrence != recorded measurement, and recording measurement testimony != producing measurement testimony.

### 05.Testimony.C — Runtime/resource observation production
Operation-instance measurement and ambient runtime/resource observation are not identical. Operation-instance measurement attributes behavior to a scoped operation instance. Ordinary runtime/resource observation is testimony about a process or runtime condition at an observed time, such as process resident memory, thread count, process runtime duration, database size, or ledger size, without necessarily attributing the value to one bounded operation instance. Runtime/resource observation may be produced through ordinary observation grammar and may exist without a recording boundary. Runtime/resource observation is not an operational baseline by identity and may support an operational measurement or baseline only through an explicit attribution and establishment boundary; recording is not its producer merely because a recorded observation can survive process exit.

### 05.Testimony.D — Operational baseline, comparison, deviation, and transition establishment
An operational baseline is retained, scoped, evidence-supported understanding of ordinary operational behavior under declared conditions. Baseline establishment consumes sufficient measurement testimony, attributed runtime/resource observations where authorized, scope, context, temporal evidence, comparison method, conflicts, and uncertainty; baseline recording may preserve the resulting standing but does not establish ordinary behavior merely by retaining samples or a summary. An operational baseline is not a database table, raw timing history, retained measurement series, recorded summary, average, threshold, fixed artifact, runtime/resource observation, or predicted future duration by identity. It must preserve enough context to prevent comparison across constitutionally different subjects, such as cache hit and cache miss, full rebuild and incremental replay, fact-view inventory construction and subject/predicate selection, small and large inputs, or distinct environment and authority conditions. A comparison consumes an applicable baseline or other authorized comparison boundary and a measurement within a declared purpose and scope; comparison occurrence != recorded comparison. A tolerance or comparison boundary requires bounded authority: the baseline applied, the operation and conditions covered, the purpose of comparison, permitted variation, and the method by which that boundary was established. Difference from one prior sample is not material deviation. Material deviation recognition is an establishment decision that a difference is constitutionally material within the comparison authority; deviation recognition != deviation recording, and a recorded difference does not establish material deviation. A material deviation preserves enough measurement and comparison context to retain the challenge to prior understanding, including operation, applicable baseline or comparison standing, context, observed difference, comparison authority and purpose, and remaining uncertainty; it is not automatically an operation failure, lost capability, cause, or consequence. A baseline transition is evidence-supported establishment that ordinary operational behavior materially changed from one bounded regime to another; baseline transition establishment is distinct from transition recording, and baseline transition establishment != transition recording. One unusual sample is insufficient, and repeated samples are not sufficient merely by count without scope, conditions, comparison method, evidence sufficiency, conflict awareness, and temporal standing.

## Important distinctions
- operational measurement != recording
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
- ExecutionStatus cadence != operation timing testimony
- execution status != operational measurement
- claim expression != claim interpretation
- claim interpretation != normalization
- normalization != support
- support != establishment automatically
- Fact artifact != Fact standing
- Fact standing != selected current standing
- reliance on testimony occurrence != reliance on testified proposition
- reliance on Fact standing != reliance on current applicability
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

## Temporal standing amendment 001

Temporal standing is the bounded warrant that a claim, artifact, support group, projection, verification, or consumer use is temporally interpretable for a declared purpose without collapsing different time relations. It asks which time a claim describes, which time supports it, when a record or artifact was produced or preserved if that is evidenced, when standing was established if that boundary is evidenced, what interval or expiry affects present-facing use, and which later consumer time supplies reliance or applicability judgment.

Claim expression may assert an occurrence at a time, a condition during an interval, a source report at a time, a desired state, a historical assertion, a present-facing assertion, or a timeless/durable relation. Normalization must preserve temporal material whenever it is part of claim identity, dimensions, support scope, provenance, predicate semantics, or source-relative limitation. The required location is claim-family and predicate specific; the Book does not impose a universal one-timestamp Claim grammar.

`observed_at` safely means only the observation-time testimony supplied or inherited at the producing boundary. Depending on the producer, it may represent source sample time, collection time, adapter time, caller-supplied time, or import time. It does not by itself establish source occurrence time, Seed receipt time, ledger recording time, normalization time, Fact-establishment time, projection time, consumer uptake time, or lawful reliance time.

Evidence produced from an Observation inherits the Observation's temporal testimony and may preserve expiry as payload/support material; it does not gain an independent receipt or recording time unless the containing event or producer records one. A Fact artifact's `observed_at` is support or described-claim time carried into fact-shaped material, not an independent `established_at`. Fact standing may be established by a responsible boundary even when no independent establishment timestamp is stored, but the time of establishment remains compressed with artifact/event/support evidence or Unknown unless specifically evidenced.

Expiry removes only the temporal standing named by its producer or by the consuming projection rule. In the current Fact support projection it removes default current-support eligibility after the expiry comparison, and `include_expired=True` can reopen preserved material. Expiry, staleness, contradiction, supersession, or loss of current selection does not delete the ledger record, make the historical testimony false, or prove historical invalidity. Latest support is the greatest observed support time selected by a support rule; it is not current enough, sufficiently fresh, authoritative, verified, or lawfully applicable without projection and consumer-local judgment.

## Sensing, remembering, trajectory, and learning amendment 001

Sensing is production of bounded testimony about an environment, operation, or condition through a declared acquisition and interpretation boundary. External provider material is not an Observation; an Observation is Seed-native testimony formed after acquisition and interpretation, not environment truth, not recording, not current standing, and not learning. Activity visibility, including ExecutionStatus-style status emission, is not a sensing result, operational measurement, capability testimony, gap standing, interaction outcome, or learning.

Remembering is preservation of sufficient testimony or standing for later lawful recovery. It may preserve raw testimony, bounded history, rebuildable standing, or compressed established understanding, but sensing is not remembering, remembering is not current projection, projection pruning is not ledger erasure, retained history is not learning, and non-rebuildable material is not preservation-required by identity.

Observation history is not trajectory or transition standing. Retaining `up at t1`, `down at t2`, and `up at t3` does not establish outage, recovery, flapping, trajectory, trend, transition, consequence, cause, or changed ordinary behavior without a separate examination boundary that preserves scope, comparison method, temporal standing, conflicts, and uncertainty. Trajectory establishment may later revise condition, gap, capability, or expectation standing, but repeated observations do not perform that establishment by count alone.

Learning establishment is an evidence-supported revision of retained understanding because prior observations, comparisons, probes, measurements, or interactions warranted a new bounded standing. Its dependency must remain recoverable as prior testimony or standing, bounded examination or comparison, and revised standing. Learning may concern environment condition, trajectory, insufficiency, gap, capability, reachability, dependency, authority, representation compatibility, resource feasibility, expectation, or strategy standing. Retained history is not learning, changed stored data is not learning, a new current value is not learning, trajectory is not learning automatically, an interaction episode is not learning automatically, gap revision is not learning automatically, capability revision is not learning automatically, baseline formation is not learning automatically, and learning is not model training by identity.

Adaptive reliance is later lawful consumption of revised gap, capability, or learned standing by a consumer whose inquiry, selection, or movement is constrained by that standing. Learning establishment is not learning consumption, learning is not adaptive reliance, changed selection is not learning automatically, changed selection is not lawful adaptation automatically, and current inputs changing does not prove prior learning was consumed. A later consumer should expose which revised standing it consumed, which prior evidence supports that standing, which need, gap, or capability demand it applies to, what decision or movement it constrained, what warrant permitted reliance, and what uncertainty or conflicts remain. The consumer may rely on sufficiently established standing with preserved provenance and need not consume every raw historical episode directly.

Causal standing remains distinct and stronger than sequence, association, gap reduction, or capability revision. Movement followed by outcome does not establish that the movement caused the outcome. Interaction-linked learning may preserve bounded association without claiming cause; causal standing requires its own establishment boundary appropriate to the intervention identity, before/after binding, alternative-cause examination, temporal relation, outcome criteria, counterevidence, repeatability, scope, and uncertainty.

ObservationIngestor's current compressed road from Observation to evidence-linked Fact-shaped artifact does not independently establish Fact standing, current standing, verified standing, trajectory standing, gap standing, capability standing, or learning standing. Those remain later, separately warranted boundaries.

## Constrained movement evidence correction 001

Sensing produces testimony that may support later evidentiary movement; it is not advancement, establishment, admission, comparison, current projection, inquiry continuation, or permission to rely by identity. External material may be acquired and interpreted into Observation testimony, but Observation produced is not testimony admitted, not standing revised, and not movement opened. Later admission, examination, comparison, establishment, current projection, and inquiry-continuation movements must consume the Observation only within preserved source, method, scope, temporal, conflict, authority, and uncertainty limits.

Remembering preserves recoverability across time. It may preserve sufficient testimony or standing so later reliance, revision, explanation, or movement can recover its constitutive warrant. Remembering does not perform later reliance, preservation is not establishment, record survival does not automatically keep movement warranted, and evidence that cannot be lawfully recovered may leave later reliance, revision, explanation, or movement unavailable or Unknown.

Trajectory establishment may be understood, where warranted, as constrained movement from occurrence history to bounded temporal understanding. Retained history is not trajectory establishment, count increased is not temporal understanding moved, and trajectory standing is not causal standing. Trajectory establishment must consume applicable series identity, temporal authority, scope, comparison method, continuity, missing testimony, conflict, sufficiency, transition vocabulary, and uncertainty before it can revise condition, expectation, gap, capability, or inquiry standing.

Learning establishment may be understood as constrained constitutional movement in retained understanding when prior standing, admitted prior evidence, bounded examination or comparison, sufficiency, and warrant establish revised bounded standing. Learning establishment is not storage mutation, projection replacement, a new current value, model training by identity, a universal Learning object, or adaptive reliance. Learning may concern condition, trajectory, insufficiency, gap, capability, reachability, dependency, authority, representation compatibility, resource feasibility, expectation, or strategy standing only within the subject, evidence, authority, scope, and limits preserved by the establishment boundary.

Adaptive reliance is later movement constrained by the result of earlier movement in understanding. It may constrain inquiry continuation, candidate consideration, selection, handoff, stopping, resource allocation, or explanation only when a consumer exposes the relied-upon standing, applicable warrant, purpose, scope, and remaining Unknowns. Revised standing exists does not mean later movement occurred, later selection changed does not prove learned standing was consumed, and adaptive reliance is not automatic execution.

Causal establishment may be understood as constrained movement from sequence or association toward bounded intervention standing. Association standing is not causal standing, interaction-linked learning is not causal proof, repeated association is not causal proof, and gap reduction or capability revision does not establish causation automatically. Causal standing requires its own intervention, before/after, alternative-cause, temporal, criteria, counterevidence, repeatability, scope, and uncertainty examination before it may warrant later intervention, explanation, selection, or stopping beyond what association alone permits.
