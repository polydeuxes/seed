# Events, Facts, and Standing

## Constitutional subject
The roles of recorded events, established facts, relationships, projected material, and bounded current constitutional standing.

## Core question
From which recorded material and established facts may a responsible projection act expose support for a current lawful condition or current constitutional standing, and what authority remains absent?

## Bounded resolution
A responsible recording occurrence may preserve, as an Event, attributed testimony that an occurrence or other claim was asserted; Event preservation does not establish the asserted occurrence as true. A responsible Fact-producing or Fact-establishing occurrence may produce material with bounded Fact standing. Fact-shaped material may otherwise exist without established Fact standing, and its original standing must be recovered from provenance and production-occurrence Evidence. A responsible projection occurrence may consume bounded recorded material under declared projection rules and produce projected material. Projected material is not current standing by identity, and current standing is not a constitutional Standing object. A responsible bounded exact Act may use projected material only under its exact subject, evidence, warrant, scope, authority, confidence, freshness, conflict, expiry, and Unknown limits. Contradicted, stale, expired, historical, unselected, or superseded Facts may remain preserved fact material while losing current selection or receiving weaker confidence for an exact Act. Recording, Fact production or establishment, projection, and act-local standing remain distinct without requiring a universal ordering among them.


## Addressable boundaries for current constitutional standing

### 06.Standing.A — Constitutional reality is bounded repository-governed standing, not objective reality
Append-only records, established facts, projected material, and current lawful condition may support a bounded current constitutional standing within the applicable Seed, workspace, corpus, question, authority, projection rule, confidence limit, and Unknown boundary. Support becomes current standing only through the responsible bounded act that consumes the material under the required evidence, warrant, constraints, and preserved limits. That standing is repository-governed and inspectable; it is not projected material by identity, a constitutional Standing object, objective reality, complete memory, universal shared truth, mandatory convergence, verification of every recorded assertion, conflict resolution by existence alone, or an oracle about conditions outside preserved evidence and authority.

### 06.Standing.B — Occurrence locality is a carried boundary coordinate
Occurrences preserved within one workspace may carry a bounded locality coordinate, and consuming acts preserve that locality where applicable, in the sense `01.Standing.E.1` already requires applicability to preserve as scope and locality and as exact Act context. Same workspace does not mean same locality, and same locality does not mean same occurrence.

Workspace is a boundary of standing, not merely another locality label. Addressability of material or Evidence from one workspace does not make it applicable within another. Cross-workspace consumption requires a separately warranted responsible occurrence that preserves the source and destination workspace, purpose, authority, scope, provenance, Unknowns, and surviving limits applicable to that movement. Where no such warrant is available, the proposed cross-workspace use is refused or remains Unknown; the material or Evidence is not thereby false or unfaithful. This clause does not establish the owner, Act, or representation of a future cross-workspace movement.

Within one workspace, a Seed may make one exact preserved Assertion available in another locality through a responsible movement occurrence. The movement preserves the source Assertion occurrence, Assertion identity, source and destination locality, Scope, Evidence, Authority, Standing, Unknowns, and surviving limits. It establishes only availability of that same Assertion in the destination locality: it does not copy or strengthen the Assertion, revise its Standing, establish applicability, demand another Act, or authorize a workspace crossing. The Assertion's identity remains unchanged while its locality occurrences remain distinct.

Chronology alone does not establish locality. Occurrences carrying one locality need not be contiguous in any recorded order, and position within a preserved sequence establishes neither membership nor exclusion.

Where a responsible act consumes material distinguished by locality, it preserves the applicable locality of what it consumed. Where that act records material under a distinct locality, the consumed and produced locality coordinates remain distinct, so that material the act produced is not later consumed as material it was given.

This establishes no further standing. A locality is not a constitutional subject, does not own or perform an act, does not carry standing of its own, and does not establish a lifetime, container, coordinator, current context, or ordering authority. Locality requires no separate locality responsible occurrence or producing act; a carried locality value remains bounded by the warrant of the occurrence or act that carries it. `session_id` is a current implementation witness for this coordinate and is not its constitutional definition.

## Important distinctions
- event != explanation
- event recording != required for every constitutional occurrence
- event != fact
- fact != entity
- Fact artifact != Fact standing
- Fact standing != current constitutional standing
- current constitutional standing != verified standing
- replay input != projected material
- projected material != current constitutional standing
- current lawful condition != recorded history
- constitutional standing != objective reality

## Representative repository anchors
- `seed_runtime/models.py::Event`
- `seed_runtime/facts.py::Fact`
- `seed_runtime/condition.py::Standing projection boundary`

## Counterexamples or failure modes
- Reading an event payload as current lawful condition without projection and a responsible standing boundary.
- Treating a relationship assertion as an observed fact without provenance.

## Related chapters
- [Recording and knowledge extraction](../05-evidence-and-knowledge/recording-and-knowledge-extraction.md)
- [Projection and current standing](projection-and-current-standing.md)
- [Testimony and established fact](../05-evidence-and-knowledge/testimony-and-established-fact.md)

## Temporal preservation, replay, and projection amendment 001

Event timestamp and ledger order are distinct. Ledger order is the append sequence a projector replays; event timestamp is event-carried metadata that may be supplied out of sequence. Chronology is not causation: causal or correlation fields can preserve local linkage evidence, but earlier time or earlier append position does not by itself prove production, reliance, or response.

Projection may select, aggregate, rank, suppress, or characterize preserved material under its projection rule. Projection does not create upstream source time, Fact-establishment time, recording time, verification time, or exact Act uptake time. A cached projection snapshot's `created_at` is projection-local snapshot time, `last_event_id` is an as-of boundary by ledger append sequence, and `last_event_created_at` is only a timestamp clue from the last input event. Direct projection without a cached snapshot may not expose an independent projection creation time.

Current selection is projection-local unless and until a responsible exact Act uses it under a bounded purpose. Non-expired material is eligible under the local expiry rule; it does not automatically satisfy an exact Act requirement. Latest measurement sample selection chooses the greatest observed sample under predicate semantics; it is not recurrence, warranted freshness for an exact Act purpose, or durable present applicability. Repeated durable support can strengthen or preserve support without creating indefinite currentness unless a predicate- and exact Act-warranted rule says so.
