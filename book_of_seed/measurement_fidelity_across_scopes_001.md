# Fidelity across independently bounded scopes: experiment 003

Findings only. No runtime or Book amendment. Uses `#2389` unchanged.

## Executive

The question was not whether a percentage rises with more material. It was:

```text
does the same representation recur as the strongest occupant
across independently preserved scopes?
```

**Yes. Twelve of twelve.**

```text
scope                       occurrences  positions  strongest  share
parsing region 0                    400         33       'is'    52%
parsing region 1                    400         29       'is'    83%
parsing region 2                    400         28       'is'    39%
parsing region 3                    400         37       'is'    76%
parsing region 4                    400         35       'is'    71%
parsing region 5                    400         24       'is'    79%
parsing region 6                    400         22       'is'    59%
parsing region 7                    400         22       'is'    55%
parsing region 8                    400         22       'is'    41%
parsing region 9                    400         20       'is'    55%
parsing region 10                   400         19       'is'    47%
parsing region 11                   400         70       'is'    81%

PROSE CONTROL                       400         18        '.'    28%
```

**The share is unstable and the occupant is not.** 39% to 83%, median 57.
Twelve scopes, one occupant, no exceptions.

**The control differs.** Ordinary prose under the identical declared
measurement yields a different occupant at a much weaker share. So the finding
is a property of the material measured, not of the measurement.

**Thirteen findings are preserved in the ledger**, each carrying its own
counting scope, so they can be compared later without any of them losing what
it stood on.

## 1. Method

Each region was fed through the operator console as its own session, so the
material measured is preserved ingress the session actually recorded. One
declared measurement, unchanged across all thirteen scopes:

```text
representation measured   the first representation following a
                          source-delimited opening segment
equivalence rule          byte-for-byte equality; no normalization
counting scope            stated per region
```

Regions were bounded by the recurring block header, taking 400 lines from each,
which is why occurrence counts are identical and position counts are not: a
region admits as many measured positions as it happens to contain.

No result was discarded. The control was chosen before the parsing scopes were
run, not after.

## 2. Why this is better evidence than one high number

`#2386` reported 88.1% over a hand-chosen span. That number is not repeated
here and should not be sought.

```text
one scope at 88%          strong reading, unknown reliability
twelve scopes at 39-83%   weaker readings, repeated independently
```

The second is worth more. A single share can be produced by choosing a span
that flatters it. Twelve independently bounded scopes agreeing on the occupant
cannot, and the disagreement about the *share* is itself informative — it
varies with how much non-parsing material a 400-line window happens to admit,
which is exactly the noise `#2387` predicted a region-bounded aperture would
let in.

**No finding was strengthened by this.** Each remains a count in its own scope.
What repeated across scopes is agreement, and agreement between preserved
findings is what `05.Testimony:27` lets a bounded comparison consume — while
preserving each input's confidence and standing rather than merging them.

## 3. The control is the load-bearing part

Without it, twelve agreeing scopes could be an artifact of the measurement.
With it:

```text
parsing regions      strongest 'is'   39-83%
ordinary prose       strongest '.'       28%
```

Same measurement, same equivalence rule, same corpus, same console path. The
occupant changes and the concentration collapses.

**[inference]** That is evidence the measurement is reporting something about
the parsing regions rather than about itself. It is not evidence that `is`
means anything, that the parsing regions are grammar, or that `.` means
anything in prose.

## 4. What this does not establish

**That anything means anything.** No finding here establishes what `is` is,
what any delimited segment is, or that the three representations stand in a
relation. `01.Standing.D` refuses relation standing to co-presence, and every
finding reports co-presence.

**That the aperture was recovered.** `occupant_of` is still supplied by the
caller, and the regions were bounded by a header a reader chose. `#2386` and
`#2389` both record this, and it is unchanged. This experiment increased the
evidence behind a finding; it did not make the finding self-starting.

**That agreement is warrant.** Twelve scopes agreeing is twelve preserved
findings that agree. `01.Kinds:32` still requires a responsible occurrence for
any relation warrant, and nothing here performs one.

**That the shares are comparable.** They range over a factor of two across
samples of 19 to 70 positions. No claim is made that the variation is
explained, and small-sample behaviour was not analysed.

**That twelve regions is a corpus.** One file, one author, one unusually
regular section of it.

**That the control is sufficient.** One prose region. A second control might
behave differently, and none was run.

**That anything new was built.** `#2389` unchanged; this is its first use at
more than one scope.

## 5. What it does establish

```text
the occupant is stable under independent bounding
the share is not
the measurement distinguishes the parsing regions from prose
```

That is the fidelity question answered for this source. It leaves the autonomy
question exactly where `#2387` left it: whether a recorded finding can supply
the aperture for the next measurement without a reader choosing it.
