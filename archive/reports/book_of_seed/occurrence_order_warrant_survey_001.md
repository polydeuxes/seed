# Occurrence order: is it implementable, and is it already implemented?

## 1. Executive

The question: are occurrence-warranted acts and claims implementable, and is
that the right path?

**Yes, and the reason is stronger than "it could be built" — the pattern is
already running, and so is the specific slice proposed as the first one to
build.**

The proposed first slice was to recover end-to-end: *E2 precedes E3 in Seed's
witnessed session order*. **The evidence capable of supporting that claim** is
already produced and already consumed on every console cycle — the claim itself
is not. An ordered list is evidence of order; it is not the proposition by
identity, and this report keeps that distinction because the campaign has
enforced it everywhere else:

```text
project_operator_session_standing   replays this session's events in append
                                    order, appending each to
                                    consumed_event_ids                (produced)

form_operator_presentation          standing_evidence_ids =
                                    list(session_standing[
                                      "consumed_event_ids"])          (consumed)
                                    source = as_of_event_id
```

Both are live. The ordered list is recorded into the
`operator.presentation.formed` event as `session_standing_evidence_ids`, and
the boundary marker as `session_standing_as_of_event_id`.

**So the first slice is not a build.** The material is carried; what is absent
is the bounded warranted claim and its stated strength. §3.

**The check that mattered.** A producer must not be built without an
already-warranted consumer. Here the consumer exists, is live, and already
consumes the exact material. The check passes — which is why this is worth
saying rather than assuming.

## 2. Why the path is right

`05.Testimony:10` supplies the design principle, and it is a constraint on
implementation rather than an encouragement:

> A Claim is the semantic proposition carried by testimony, observations,
> evidence payloads, fact artifacts, relationships, projections, explanations,
> documentation, or consumer assertions. **The Book does not currently
> recognize a separate durable `Claim` artifact as the universal subject of
> knowledge**; claim-centricity means the proposition is not identical to any
> one storage object and **must keep its source, scope, interpretation,
> support, confidence, conflict, and authority limits as it moves through
> different artifacts and standings**.

That is exactly the `_dimensions` payload pattern the runtime already uses: the
proposition travels with its limits attached. It is also a direct prohibition
on the obvious wrong turn — a `Claim` class, a claim registry, a claim
pipeline. The campaign has spent thirteen reports establishing that naming a
noun does not create a subject; here active law says so about this specific
noun in advance.

The same reading applies to `Observation`. It is real where an
observation-producing Responsibility exists. It is not a wrapper for every
occurrence.

## 3. What is actually missing

Not machinery. The order is carried as an ordered Python list, and its warrant
is nowhere stated.

```text
carried        consumed_event_ids, in ledger append order
  (evidence)     → recorded as session_standing_evidence_ids

not produced   the bounded claim "E2 precedes E3 in Seed's witnessed
  (the claim)    append order", with its strength stated and its limit
                 stated — that it claims no production, reliance, or
                 response
```

The distinction matters and is not pedantry. `05.Testimony:10` requires the
proposition to keep "its source, scope, interpretation, support, confidence,
conflict, and authority limits as it moves through different artifacts and
standings." A list index carries none of those. The evidence exists; the claim
does not.

`06.Events:47` says both halves precisely:

> Ledger order is the append sequence a projector replays [...] Chronology is
> not causation: causal or correlation fields can preserve local linkage
> evidence, but earlier time or earlier append position does not by itself
> prove production, reliance, or response.

The first half is a warrant. The second is its limit. The runtime currently
carries the material for the first and states neither.

Compare with what the same runtime does elsewhere. The presentation formation
act states its own limit in its own record:

```text
authority_warrant = "formation occurrence only; establishes no selection,
                     warrant, goal, or response treatment"
```

The ordering claim has no equivalent. That is the asymmetry, and it is small,
concrete, and answerable — unlike "what is the first lawful act."

## 4. The property worth preserving

Stated in active law's own words rather than a new phrase. The proposed
formulation was *"warrant propagates as Evidence, not as conclusion strength."*
The idea is right; the phrasing is a coinage — `warrant propagates`,
`propagates as evidence`, and `conclusion strength` return zero occurrences in
active law.

The established form is `05.Testimony:24`:

> A recorded claim, diagnostic finding, or evidence record may be consumed as
> attributed testimony or premise-relative input for an exact declared act.
> That consumption [...] does not establish the testified content as fact,
> prove the source producer occurred, or **strengthen standing merely through
> repetition or copied lineage**.

A downstream act consumes upstream Standing as evidence for its own
determination. It does not inherit the upstream's strength, and it does not
gain strength by citing lineage. Which is why call order cannot supply warrant:
running after a warranted act transfers nothing.

## 5. What this does not establish

That the four ingress acts stay inside their stated Authority. That question is
open from `#2349` and is not answered here.

That stating the order's warrant is the right next slice rather than merely a
small and available one. It is concrete and its consumer exists; whether it is
the most useful next thing is a judgement this report does not make.

That the projection is a lawful occurrence. `project_operator_session_standing`
runs every cycle and produces the ordered list. `06.Events:10` provides for a
responsible projection occurrence producing projected material, and
`06.Events` separately holds that `projected material != current constitutional
standing`. Whether this projection meets that clause is unexamined, and it
matters, because the ordering claim would rest on it.

That any of this requires the dormant goal chain. It does not, and #2348's
finding stands: that chain's gating input is fixture-only.

## 6. Method note

The cardboard-city check — never build a producer without an already-warranted
consumer — was run before assessing the proposal, and it changed the answer
rather than confirming it. The expected outcome was either "build it" or "no
consumer, don't." The actual outcome was neither: **the producer and consumer
both already exist, and what is absent is the stated warrant of what passes
between them.**

That is a third possibility worth keeping. Asking "who consumes this" can
return "something already does," and when it does, the remaining work is
usually much smaller than the proposal that prompted the question.
