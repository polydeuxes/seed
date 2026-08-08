# Examination as discriminating witness for formation and production

## 1. Executive

The probe: rather than census `formation` again, use the one composite act
active law actually decomposed — `Examination`, removed at #2210 — and read
what it decomposed *into*.

**Two findings, and the second answers the question directly.**

**Examination decomposed into four already-established acts, none of which is
formation or production.** Each replacement names a different act, and each of
those acts carries its own result:

```text
before #2210                          after #2210
─────────────────────────────────────────────────────────────────────
duplicate every examination      →    duplicate every applicability
                                      determination
for examination, comparison, …   →    for comparison, …   (deleted outright)
attempting to examine the        →    attempting consumer-local
  preserved ingress                   interpretation
separately responsible           →    separately responsible
  examination                         establishment
```

Seventy-two `examin*` occurrences were removed across the commit and **zero
were added**. No replacement anywhere in that commit introduced `formation` or
`production` to carry a result-producing step that Examination had been
carrying.

**Active law already has the general category, and Examination was a kind of
it.** This is the direct answer. The clause read:

> A responsible **examination or other kind-specific production occurrence**
> may preserve a bounded **Unknown** finding …

and became:

> A responsible **kind-specific production occurrence** may preserve a bounded
> **Unknown** finding …

Examination was listed as one *kind* of production occurrence. Removing the
kind left the general category standing and covering the ground. Nothing had to
be invented to replace it, because the category was already there.

## 2. Why this answers the assigned question

The question was whether `formation` preserves any distinction not already
carried by producer, act, occurrence, production, and the resulting
representation.

`01.Kinds:69` supplies the grammar that makes a separate node unnecessary:

```text
responsible kind-specific production occurrence
```

That is a general form with a slot. The specific act names the kind;
`production occurrence` names what it is. On this reading:

```text
Examination      was    a kind-specific production occurrence   (removed)
comparison       is     a kind-specific production occurrence
determination    is     a kind-specific production occurrence
establishment    is     a kind-specific production occurrence
forming a representation
                 would be a kind-specific production occurrence
```

`formation` does not need to be a coordinate between the act and its result,
because the act *is* the production occurrence and the result is what it
produces. Inserting `formation` would add a node the grammar already has a slot
for.

The same clause family appears twice more as "kind-specific production **or
establishment** boundary", so the general form is not a single stray phrase.

## 3. What the decompression shows about composites generally

Each of the four replacements is a *different* act. Examination was not one act
under a wrong name; it was four acts under one word.

```text
applicability determination      whether this input applies here
comparison                       what two preserved things exhibit
consumer-local interpretation    what this material means to this consumer
establishment                    whether the bounded thing now holds
```

And none of those four required a companion production step to be named
separately. `determination`, `interpretation`, and `establishment` each carry
their result in the act name; `comparison` produces a finding without a
`comparison formation` beside it.

The concordance's own retired `examination` row recorded its related concepts
as **"relevance, applicability, testimony"** — consistent with the
decomposition, and containing no production or formation term.

## 4. What this does not establish

**That `formation` and `production` mark the same distinction.** They may not.
`production` bears on whether something came into existence; the earlier report
was corrected for compressing them. This probe shows only that the one real
decompression in the corpus needed neither `formation` as a node nor a separate
production step beside the named acts.

**That `formation` should be removed from active law.** It appears 45 times,
overwhelmingly as ordinary English describing what a responsible occurrence
does. Nothing here proposes deleting it, and `06.Representation.A` is a
separate question.

**That every composite decomposes this way.** One decompression is one witness.
Examination is the strongest available because it is the only composite act
active law has actually taken apart, but a single case does not establish a
general rule about composites.

**That `kind-specific production occurrence` is a recovered constitutional act
family.** It is a phrase appearing four times in one file. Whether it names a
family with an owner, or is ordinary grammar for "whatever occurrence produced
this kind of thing", is untested. That question matters, because §2 rests on
it, and this report does not settle it.

**Anything about `rendering` or `emission`.** Settled separately at #2357 and
untouched here.

## 5. Method note

The probe answered in three commands what a vocabulary census could not answer
at all, because it asked a different kind of question: not *how is this word
written*, but *when the Book actually removed a composite, what did it reach
for*.

The discriminating property was that #2210 is a real decompression with a
known before and after. Removed and added text can be paired, and the pairing
is evidence about what the corpus considered equivalent — which no count of the
current text can supply.

One check kept the finding honest. `formation` and `production` do appear in
#2210's added lines, which initially looked like they might be Examination
replacements. Reading them showed all are unrelated context from the same
commit, which also removed `Work` and relocated `Policy`. The claim required
checking that the additions were in the same sentences as the removals, not
merely in the same commit.
