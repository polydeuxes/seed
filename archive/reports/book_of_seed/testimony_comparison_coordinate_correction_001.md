# Correcting the universal coordinate requirement in 05.Testimony.E

Book amended narrowly. No runtime amendment. One clause, one sentence boundary.

## The correction

```diff
- ... and forbidden inferences. It may produce bounded relation standing ...
+ ... and forbidden inferences as that input carries them, but no input must
+ possess every coordinate. Preserving forbids erasing or strengthening what an
+ input carries; it does not supply what an input lacks, and no input acquires a
+ coordinate by being compared. It may produce bounded relation standing ...
```

**Nothing was removed.** All ten coordinates remain named. What is removed is
the assertion that every preserved testimony or finding possesses each of them.

## Why this wording

**[measured]** The qualifier is the Book's own idiom, not new grammar.
`05.Testimony.B:33`, two clauses away in the same chapter:

> A measurement may identify operation, instance scope, phase, duration or
> resource behavior, clock or method, input scale, cache condition, environment
> or authority context, completion condition, and observation time as needed by
> its consumer, **but no implementation must possess every dimension.**

**[inference]** The chapter already knew how to name a coordinate list without
requiring every member of it. `E` was the clause that did not, and it is the one
that arrived by relocation.

## What the protective purpose required

`#2418` established the requirement as unwarranted. It did not establish that
the clause had no work to do, and the second added sentence is that work stated
positively rather than left implied:

```text
  forbidden    erasing what an input carries
  forbidden    strengthening what an input carries
  not implied  that a comparison supplies what an input lacks
  not implied  that being compared confers a coordinate
```

**[inference]** "Strengthening" is stated because the original protection was
one-directional. `:29` already forbids comparison establishing truth, warrant or
corroboration, but nothing said a comparison may not return an input with a
firmer coordinate than it arrived with. Under the old universal reading that gap
was hidden, because an absent coordinate was not contemplated at all.

## What was deliberately not done

**No coordinate was deleted.** `confidence` remains named. `#2418` found it real
and provider-owned under `01.External:15`, and an input that *is* attributed
external testimony may well carry one. The defect was universality, not the
word.

**No other clause was touched.** `05.Testimony:24`'s four-coordinate consumption
is unchanged, and the contrast `#2418` recorded between `:24` and `:27` now
reads as two consumption boundaries with different obligations rather than as a
contradiction.

**No runtime was amended**, per the correction's scope.

## Known stale quotation, not repaired here

**[measured]** `seed_runtime/preserved_material_measurement.py:25-27` quotes the
clause as it stood:

> `05.Testimony:27` permits exactly that: a bounded comparison may consume
> preserved findings "only while preserving each input's attribution,
> provenance, support basis, subject, scope, authority, confidence or
> uncertainty, Unknowns, standing, and forbidden inferences".

The quoted words are all still present, and the quotation now stops immediately
before the qualifier that changes their force. That is a partial quotation of an
amended clause, and it is the defect this session records as its most frequent —
a correction that does not reach every place asserting the old claim.

It is **left in place** because this correction's scope excludes runtime. It
should be repaired in whatever change next touches that module, and it is
recorded here so the omission is deliberate rather than forgotten.

## What this does not establish

**That layer C may now be built.** One blocker is removed. Whether the smallest
bounded testimony Compare is warranted, what instantiates it, and what it
records are unanswered, and `#2416` holds: the owner is local to each
instantiated comparison and never universal.

**That the remaining nine coordinates are warranted universally.** Only
`confidence or uncertainty` was cat-tested. The other nine were carried by the
measurement findings without difficulty, which is evidence that they are
available, not that active law requires them of every input.

**That the relocated clause is now sound in every respect.** `#2418` traced its
origin to cross-examination grammar in an excised contaminated chapter. One
requirement in it was tested and corrected. The rest of the relocation was not
re-examined.
