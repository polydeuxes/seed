# Composition, Artifact, and presentation: constitutional status recovery 001

## 1. Executive

Three subjects, three different verdicts. The fan-out was run before any of
them, and it predicted all three.

```text
composition     10 occurrences,  3 files, 0 positive clauses    cat
presentation    45 occurrences,  6 files, 0 act/standing clause bundling defect
artifact        87 occurrences, 18 files, definition + chapter  established
```

**`Composition` does not name a constitutional subject**, and active law does
not merely omit it — it warns against the exact reification. §2.

**`Artifact` is established**, and the suspicion against it does not survive
contact with the corpus. Chapter 01 is titled *Constitutional Kinds and
Artifact Standing*, its core question is "what establishes an artifact's
standing," and `01.Kinds:10` defines it outright. §3 also separates two
different things that share the word.

**`presentation` is not a cat, but the one-word `Presentation` bundles two
things active law explicitly keeps apart.** That is the answer to the question
that prompted this: the difference between representation and presentation is
that active law states `representation formation != emission`, twice, and
`Presentation` names both at once. §4.

## 2. Composition is a cat

Ten occurrences across three files. No `Composition act`, `formation`,
`producer`, `responsibility`, `occurrence`, or `standing` clause exists. But
the decisive evidence is positive rather than absent.

**It appears in a verb list.** `01.Lenses:10`:

> A lens consumes existing material and **exposes, selects, projects, or
> composes** a bounded representation without changing the standing of the
> represented source material.

Four verbs describing what a lens does in forming a bounded representation. No
one would recover an `Exposure Responsibility` or a `Projection-of-a-View
Responsibility` from the neighbouring verbs in that same sentence, and the cat
rule applies identically to the third one.

**Active law explicitly warns against the reification.** `01.Lenses:53` lists,
among things not to do:

> Treating the pipeline's **projection-selection-composition call order as a
> universal constitutional sequence**; each component is explicitly read-only
> and locally bounded.

This is unusual and worth marking: the corpus anticipated this exact error and
recorded it. The warning is about the *call order*, and it lands on the same
material — an implementation's decomposition read as constitutional structure.

**The remaining uses are non-equivalences, a filename, and the unrecovered
node.**

```text
01.Lenses:27   read-only representation selection or composition
               != assertion-preserving Uptake by itself
01.Lenses:34   composition compatibility != general selection standing
01.Lenses:47   `seed_runtime/constitutional_view_composition.py`
04.Question:26 "may constrain lens applicability, selection, composition"
04.Question:40 "applicability, selection, and composition of lawful
               internal means"  — the node #2344 found names nothing
```

`ConstitutionalViewComposition` in the runtime does not rescue it.
Implementation naming is testimony about what developers built, not recovery of
a constitutional act — the same reading applied to `examination_work_selection.py`
at #2343.

So: **composition is an ordinary description of how representation formation
forms a particular representation.** It answers "how was this one formed," not
"what occurred."

## 3. Artifact is established — the suspicion does not carry

`artifact` appears 87 times across 18 active-law files, has a home chapter
named for it, and carries a definition:

```text
01.Kinds  chapter title    "Constitutional Kinds and Artifact Standing"
01.Kinds:7  core question  "Which kinds are constitutionally recognized, and
                            what establishes an artifact's standing as one
                            of them?"
01.Kinds:10 definition     "An artifact is a preserved representation or
                            record whose fields carry an assertion made by
                            another responsibility."
```

That is the strongest profile of any term tested in this campaign. It is not a
cat, and no further test is needed to say so.

**But two different things share the word, and only one of them is this.** The
suspicion against Artifact rests on #844's admission that its `Artifact` was
"only an architectural characterization, not a first-class runtime object."
That is true and it is about a *different* Artifact:

```text
#844's Artifact      a node between answer composition and presentation,
                     owning "consumer-specific organization"

01.Kinds:10's        a preserved representation or record whose fields
artifact             carry another responsibility's assertion
```

The first may well be a cat. Nothing here defends it, and it was never
recovered. The second is established law and is untouched by the first's
failure. Sharing a word does not transfer a defect — the same reading that kept
`Inquiry` alive at #2343 when `Examination` was cut from its own chapter.

## 4. representation, emission, and what `Presentation` bundles

Active law's terms, with their counts:

```text
representation   129 occurrences, 17 files   defined, with an act
emission          40 occurrences, 11 files   defined, distinct occurrence
presentation      45 occurrences,  6 files   no act or standing clause
Presentation       1 occurrence               mid-sentence, 08.Communication:45
```

The distinction is stated, and stated twice:

```text
08.Communication:39   "Representation formation is not emission occurrence.
                       A representation may exist without being emitted."
08.Communication:92   representation formation != emission
```

And `08.Communication:10` gives the act: "Seed may form a bounded
representation from exact source material for a declared purpose."

**Where `presentation` does appear substantively, it is a qualifier, not a
subject.** The two recurring forms are `presentation purpose`
(`03.Prerequisite:110`, "eligibility for one presentation purpose") and
`presented alternative` — and the second settles the ownership question,
because `03.Prerequisite:111` says who forms it:

> a **responsible representation occurrence** forms a presented alternative

The representation occurrence is the act. "Presented" is the resulting
property. So:

```text
representation formation    the act                        established
bounded representation      the formed thing               established
emission                    the separate occurrence        established
presentation                ordinary description of the emission;
                            adjectivally, presentation purpose and
                            presented alternative
```

**The defect is bundling, not vocabulary.** `Presentation` as a single word
names formation and emission together, and active law separates them twice.
Anything reasoning about "the Presentation" is reasoning about two occurrences
at once, which is why it has been simultaneously central and hard to place as a
responsibility.

**The runtime is already structurally correct**, which is worth saying plainly
because it means no rework follows from this. `form_operator_presentation()`
and `emit_operator_presentation()` are already two occurrences, recorded
separately as `presentation.formed` and `presentation.emitted`. The split
active law requires is implemented. Only the name bundles.

## 5. What this does not establish

That `presentation` should be removed. It is ordinary English for what an
emission does, used that way throughout active law, and it passes the deletion
test in neither direction — this report proposes no edit.

That `Presentation C` must be renamed. The runtime already keeps the two
occurrences apart; whether the name should change is a separate decision with
its own costs, and it is not made here.

That the old pipeline's remaining nodes are settled. `Answer` was dissolved at
#2345 and `composition` here. `#844`'s `Artifact` node is untested — §3
declines to defend it while establishing that the constitutional kind is
unaffected either way.

That `View` and `representation` are distinct. `01.Lenses:63` makes a View "a
bounded representation formed for a consumer purpose from source material under
a declared method," which reads as a View being a kind of representation rather
than a separate upstream stage. That is a real question raised by the wording
and it is not resolved here.

## 6. Method note

The fan-out caught a counting error that would have inverted a verdict.

```text
grep -oi "presentation"    181 occurrences   WRONG
grep -oiE "\bpresentation\b"  45 occurrences  correct
```

**`presentation` is a substring of `representation`.** The contaminated figure
made `presentation` look more established than `representation` itself, and it
had already been published — #2345 stated "lowercase `presentation` appears 180
times." The naive 181 decomposes exactly as:

```text
representation     129
presentation        45
representations      5
representational     2
                   ---
                   181
```

That figure is corrected in #2345.

The same class of error as `## Core question` at #2344 and `Direct answer` at
#2345, and the third counting defect in four reports. The pattern is now clear
enough to state as a rule: **a census is only as good as its word boundaries
and its buckets.** Count with `\b`, then read every occurrence rather than
trusting the count.
