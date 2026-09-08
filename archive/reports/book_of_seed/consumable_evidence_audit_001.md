# Is the separation result consumable? audit 001

Findings only. No runtime or Book amendment.

## Executive

The question: does Seed hold consumable Evidence for **both** of these, such
that a responsible comparison could consume them together?

```text
1  ordered material separates from shuffled material on one source
   and not another                                          (#2396)

2  one coordinate of its own measuring was observed with a
   single value across 3,226 occurrences                    (#2397)
```

**Only the second.** The first is not recorded anywhere Seed can reach.

```text                                     recorded as an  reachable by
                                            event?          a consumer?
self-survey of measured positions           yes             yes
ordered-vs-shuffled separation              no              no
```

So the join a reader makes between them — *what I can distinguish may depend on
a coordinate of my own measuring that has never varied* — is available to the
experimenter and to nothing else. **The hand is still in the loop, and this is
where it is.**

## 1. Where each result lives

**[runtime witness]** `operator.measurement.self_survey_recorded` is an event
kind. A survey is appended to the ledger, names its subject, carries its
equivalence rule and counting scope, and can be read back by anything that
reads the ledger.

**[runtime witness]** Nothing records a comparison between ordered and shuffled
material. Searching the committed Python for any form of `shuffl` returns two
occurrences, both prose inside docstrings describing `#2396`. No event kind, no
payload field, and no function carries the comparison or its result.

**[historical testimony]** `#2396`'s result exists in exactly two places: the
report `source_swap_experiment_001.md`, and a scratch script that built a fresh
ledger per run and discarded it. The shuffled runs' own findings were recorded
into ledgers that no longer exist.

## 2. Why that is the load-bearing gap

`#2397` gave Seed a record of its own measuring. That was the harder half, and
it works.

But an invariant is not interesting on its own. `displacement` being recorded
with one value is a fact about bookkeeping until it is set beside a fact about
consequences — that the same measuring distinguishes ordered from shuffled
material on one source and not another. **The consequence is the half that is
missing.**

```text
what Seed can consume        what a reader consumed
self-survey                  self-survey
                             + #2396's separation table
                             + the observation that all five forms
                               measure one position away
                             -> a suspicion about why
```

Two of those three inputs are the reader's.

## 3. What would have to be recorded

Not proposed, only stated, because naming what is missing is not the same as
warranting it:

```text
a measurement whose subject is a source under a stated arrangement
a measurement whose subject is the same source under a destroyed
  arrangement, recorded as such rather than as a different source
both preserved in one reachable place
```

The last is the part the current experiments never do. Each control run built
its own ledger, and a comparison cannot consume findings that were discarded
when the process exited. `05.Testimony:27` lets a bounded comparison consume
preserved findings; it cannot consume a table in a report.

**[inference]** The shuffled material is also not currently anything Seed
received. It was produced by a script, not preserved as ingress, so even its
findings would have no recorded provenance tying them to the ordered material
they are a control for.

## 4. What this does not establish

**That the comparison should be recorded.** This audit locates a gap. Whether
an act should consume both findings, and whose act it would be, is not
recovered here, and `01.Kinds:32` still requires a responsible occurrence for
any relation between them.

**That recording it would produce the join.** Preserving two findings in one
place makes a comparison possible. It does not make the comparison, and it
establishes nothing about what a comparison would find.

**That `#2396`'s result is unsound.** It is measured and controlled. It is
simply not held anywhere Seed can reach.

**That the self-survey is Standing.** It is measurement evidence about Seed's
own occurrences. An earlier summary of `#2397` said "Seed's Standing now
contains", which overstated it: the record establishes nothing beyond the
survey assertion, and the PR itself says so.

**That this is the only remaining hand.** It is the one visible from here.
`#2391` records that material extent, field division, and the measurement
family are still supplied.
