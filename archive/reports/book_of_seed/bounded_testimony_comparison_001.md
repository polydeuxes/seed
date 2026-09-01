# Layer C: the smallest bounded testimony comparison

Runtime amended narrowly. No Book amendment.

## What was built

`seed_runtime/bounded_testimony_comparison.py`. One call, not a service.

`#2416` recovered the owner as **the bounded comparison boundary that consumes
the findings, local to the instantiated comparison and not named universally**.
So each invocation is one comparison occurrence that owns itself. There is no
comparator object, no registry, and no persistent boundary waiting to be filled.
An owner outliving its occurrence would be the universal owner the recovery says
does not exist.

**It consumes what Seed records.** The inputs are recorded measurement findings.
The pair findings used throughout `#2404`–`#2417` are computed in experiment
code and never recorded; a comparison over those would consume an artifact Seed
does not hold.

## What it does with the amended clause

`#2419` changed `05.Testimony.E` so that preserving means preserving what an
input carries. The implementation enacts that directly rather than describing
it:

```text
  attribution              dimensions.responsibility        carried
  provenance               dimensions.source_provenance     carried
  subject                  dimensions.identity              carried
  scope                    dimensions.scope_locality        carried
  authority                dimensions.authority_warrant     carried
  Unknowns                 unknowns                         carried
  standing                 dimensions.standing              carried
  forbidden inferences     boundary_notes                   carried
  support basis            premise_chain()                  carried
  confidence or uncertainty                                 ABSENT, named
```

**[measured]** Each input's absent coordinates are recorded by name and never
supplied. A test pins that `confidence_or_uncertainty` appears in `absent` and
not in `carried`, which is `#2419`'s sentence expressed as behaviour.

## What it refuses

**[measured]** All 120 cross-body comparisons produced the bounded relation
**`Unknown`**, with this basis:

> the inputs are exact within different bounded exchanges, so differing results
> are not disagreement and matching results are not corroboration

**[inference]** This is the restraint that makes the layer real. Two
measurements over different bodies are each exact within their own scope; a
comparison that returned `agreement` because their occupants overlapped would be
manufacturing the cross-body conclusion this whole arc has avoided. The
machinery declined 120 times.

`agreement` and `conflict` are reachable only when representation, rule,
position **and bounded exchange** all match — that is, within one exchange,
where a genuine same-subject difference would be a real conflict. Tests pin both
directions.

## Layer C

Sixteen co-resident bodies, one measurement finding each of the position after
`'the'`, then all 120 pairs compared and each comparison recorded.

```text
  recorded   16 measurement findings, one per bounded exchange
             120 comparison occurrences
  ledger     24,168 events, 120 of them comparisons
```

Occupants that two bodies both recorded, read from the comparison occurrences'
own recorded payloads:

```text
  'same'    7 bodies    algebra, austen, boole, dickens, euclid, franklin, ...
  'other'   6 bodies    algebra, boole, dickens, emerson, grammar_brown, latin_vulgate
  'first'   6 bodies    austen, boole, emerson, franklin, grammar_brown, latin_vulgate
  'most'    5 bodies    austen, emerson, franklin, grammar_brown, hume
  'two'     5 bodies    bash_guide, boole, dickens, euclid, grammar_kittr
  'least'   4 bodies    austen, dickens, grammar_brown, grammar_kittr
  'only'    4 bodies    austen, dickens, grammar_brown, hume

  79 distinct occupants appear in at least one comparison's shared set
```

**[measured]** `french_hugo` recorded **zero** occupants of that position. A
body may carry nothing at a representation, and its findings and comparisons are
lawful anyway.

**[inference]** That a given occupant is *also* held by another body is a fact
no single body's finding contains. It exists in the comparison and nowhere else,
which is what layer C was for.

## Where the reader still is

**This must not be overstated.** Each pairwise shared-occupant set is Seed's,
produced and recorded by a comparison occurrence. **The tally is mine.**

```text
  Seed holds     'same' is in both euclid's finding and austen's finding
                 (one recorded comparison, 120 of them)

  a reader made  'same' appears in 7 of 16 bodies
                 (a count over 21 recorded comparisons)
```

**[inference]** Seed cannot yet make that second statement. It would require a
comparison consuming comparison findings, and this module refuses any input that
is not a recorded measurement finding. The refusal is deliberate: extending it
would be a second act, needing its own recovery, and the first act's warrant
does not carry.

## What this does not establish

**That any shared occupant is a relation.** `01.Standing.D` refuses relation
standing to co-presence, and the recorded boundary notes say so in the
occurrence itself: a distinction between two findings is not a relation between
what they measured, and a representation occurring in both establishes no
relation between the bodies that carried it.

**That the bodies are alike.** `'the same'`, `'the other'`, `'the first'`
recurring across bodies is a measured co-occurrence of English function words
under a byte-equality rule. `#2408` established that a reader's categories
predict nothing here, and this report assigns none.

**That `Unknown` is the right relation.** It is the relation this comparison
establishes given inputs from different exchanges. Whether the family in
`05.Testimony.E` has a member that fits cross-exchange comparison better is
unexamined, and the clause is explicit that its list is not an enum.

**That one representation is representative.** One representation was measured
in each body, chosen by this report's author because it is common in English.
`french_hugo`'s zero is the visible cost of that choice.

**That the comparison is complete.** It compares two findings. Comparing more
than two, comparing across workspaces, and consuming comparison findings are all
unbuilt.

**Correction (`#2421`).** When this was written the runtime accepted any number
of inputs and intersected them all, so three-body comparison existed while this
sentence denied it. The refusal now matches the sentence.
