# Prior Standing as a measurement premise: experiment 002

Findings only. No runtime or Book amendment. Nothing was built.

## Executive

The operator's hypothesis: a weakly-supported structure can be used as the
premise for the next measurement, and the next finding may be far stronger than
the premise that bounded it. *"If I take this structure with 40% confidence, I
find this structure with 88%."*

**Measured, and the ladder is real.** But it is **not monotonic**, and that is
the finding.

```text
aperture                                    strongest occupant   share  positions
0  no prior finding                                     'the'     3.0%   84,504
1  region bounded by a recurring block header         'which'     4.5%      738
2  position bounded by the source's delimiter            'is'    88.1%      160
```

**Narrowing is not what helps.** Rung 1 shrinks the material 114-fold and buys
1.5 percentage points. Rung 2 jumps to 88%.

The difference is what kind of prior finding you stand on:

```text
a finding that bounds a REGION      almost nothing follows
a finding that bounds a POSITION    the next measurement becomes decisive
```

**And active law already supplies the mechanism.** `05.Testimony:27` has a
bounded comparison consume preserved findings while preserving each input's
standing, confidence, and provenance. No new coordinate is required, which
matches curator's reading: prior Standing is an **input to the next
occurrence**, not a field inside the subject being discovered.

## 1. The measurement

Same question at three apertures — *what representation occupies this
position?* — with the only difference being what prior finding bounds it.

**Rung 0, no prior finding.** Every line's first representation, whole file.
Strongest occupant `'the'` at **3.0%** of 84,504 positions. This is the noise
floor, and it is the same floor the relation observer hit at corpus scale.

**Rung 1, standing on a region-bounding finding.** `EXAMPLE PARSED.` recurs 12
times; measure only inside those blocks. Strongest occupant `'which'` at
**4.5%** of 738 positions.

**Rung 2, standing on a position-bounding finding.** The source's own `_..._`
delimiter recurs across 161 entries in those blocks; measure the position
immediately after it. Strongest occupant `'is'` at **88.1%** of 160 positions.

## 2. Why rung 1 fails, and why it matters

Rung 1 is the intuitive move: find a regularity, narrow to it, measure again. It
removed 99.1% of the material and improved the signal by 1.5 points.

**A region tells you where to look. A position tells you what to look at.**
Inside the blocks the question is still *what starts a line*, which admits every
sentence Brown writes. After the delimiter the question is *what follows this
exact source-marked boundary*, which admits only what the source puts there.

So the hypothesis needs a qualification it did not originally carry: the premise
must constrain the **aperture of the next question**, not merely the volume of
material. A weak finding about *where* is worth little. A weak finding about
*structure* is worth a great deal.

**[inference]** This may be why the earlier recurrence work failed. It narrowed
by interest rather than by structure, and interest is a region.

## 3. Active law already carries the mechanism

**[active law]** `05.Testimony:27`:

> A bounded comparison may consume multiple independently preserved testimonies
> or **findings** only while preserving each input's attribution, provenance,
> support basis, subject, scope, authority, **confidence or uncertainty**,
> Unknowns, **standing**, and forbidden inferences.

Every element the hypothesis needs is in that sentence:

```text
requirement                              clause supplies it
a finding may be an input                "consume ... findings"
its weakness travels with it             "confidence or uncertainty"
its standing travels with it             "standing"
what it rested on travels with it        "provenance, support basis"
the result stays bounded                 "inside the comparison boundary"
```

**[inference]** So a 40%-supported structure being usable as a premise is not a
new permission. It is what consuming a finding already means, provided the
result preserves what it depended on.

**[inference]** And the collapse case is handled. If the premise fails later,
the finding built on it does not silently keep its authority, because
`05.Testimony:27` required its support basis to be preserved. The 88% is not
recorded as a fact about English. It is recorded as a finding under a stated
premise, in a stated region, by a stated rule.

## 4. Prior Standing is an input, not a coordinate

**[inference]** Adding `prior_standing` as a relation dimension would duplicate
into the subject something the consuming occurrence already carries. The shape
active law supports is:

```text
occurrence      a bounded comparison
consumes        preserved findings, each with its own standing and confidence
within          a stated scope and measurement rule
produces        bounded relation standing, inside the comparison boundary
```

The premise is not part of what is discovered. It is part of what did the
discovering, and `05.Testimony:27` requires it to be preserved as such.

## 5. What this does not establish

**That the ladder climbs further.** Three rungs on one file. Rung 3 — the third
segmentation boundary — was not attempted, and nothing here shows the pattern
continues.

**That a premise's weakness is quantified anywhere.** "40%" is the operator's
illustration. `05.Testimony:27` requires confidence or uncertainty to be
preserved; it does not establish a scale, and none is proposed.

**That 88% is a standing.** It is a count in a bounded region under a stated
rule. `01.Standing.D` still refuses relation standing to co-presence, and
nothing here establishes what `is` means or that Brown's classification is true.

**That the rungs were derived rather than chosen.** `EXAMPLE PARSED.` and
`_..._` were selected by a reader, as `#2386` also records. The ladder shows
what follows *given* those anchors; it does not show they would be found.

**That region-bounding findings are useless.** §2 shows one gave 1.5 points on
one file. A different region might do better, and the distinction between region
and position is drawn from three measurements.

**That anything was built.** Measurements over a preserved file, reported.

## 6. The next measurement this suggests

Not a bigger experiment. A smaller one:

```text
without being given `EXAMPLE PARSED.` or `_..._`,
does enumerating recurring structures surface a position-bounding
finding at all?
```

`#2386` records that the relation observer surfaced `OBS. 1` and this source's
citation prefix unprompted, so the ingredients exist. Whether an enumeration
reaches a *position*-bounding finding rather than a region-bounding one is the
question §2 makes load-bearing, and it is unanswered.
