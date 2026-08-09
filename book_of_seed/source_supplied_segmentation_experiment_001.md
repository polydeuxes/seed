# Source-supplied segmentation: experiment 001

Findings only. No runtime or Book amendment. Nothing was built.

**This is experimental physiology, not constitutional archaeology.** It does not
ask what active law authorizes. It asks one empirical question about a corpus
file:

```text
what Evidence could produce
    [A noun] [is] [a word]
as three distinct coordinates,
without a developer choosing the boundaries?
```

The proposed shape is not tested for lawfulness here, and nothing in the recent
archaeology showed the shape to be wrong — only that the Book has not finished
describing it.

## 1. Result

**For `corpus/grammar_goold_brown.txt`, the source supplies the segmentation.**

Every boundary in the three-coordinate shape is obtainable from measurements
`01.External:28` already permits — exact equality, count, recurrence, prefix
occurrence, adjacency. None required knowing English, and none was chosen for
its meaning.

```text
step                              how obtained                 measured
recurring block header            exact equality + count       12 blocks
  "EXAMPLE PARSED."
source's own segment delimiter    recurrence                   161 entries
  _..._                                                        in those blocks
first coordinate                  the delimiter's contents     161
second coordinate                 recurrence in the position   141/161 = 88%
                                  immediately after it
third coordinate                  remainder                    boundary not
                                                               established
```

## 2. The decisive measurement

The pseudocode's `0:6`, `7:9`, `10:16` look like developer magic. For the second
boundary they are not.

Across the 161 entries that open with a source-delimited segment, the
representation occupying the position immediately after the delimiter was
**enumerated, not supplied**:

```text
  141x  'is'
    5x  'or'
    4x  '.'
    3x  'which'
    3x  ';'
    1x  'to'
```

Nothing asked for `is`. The measurement ranked what recurs in a position the
source's own delimiter defines, and one representation took 88% of it.

This is the difference from `recurrence_consumer_first_recovery_001`'s failure.
There, `"it keeps"` was chosen because a reader who knew English found it
interesting, and at corpus scale the ranking drowned in short common forms.
Here the source constrains the position first, and the recurrence inside that
position is decisive.

## 3. What the source actually supplies, exactly

The repeated form:

```text
_The_ is the definite article.
_Best_ is a common adjective, of the superlative degree; ...
_And_, is a conjunction.
_Most_ is an adverb.
```

**Only the first coordinate is delimited.** The second and third boundaries are
not marked by the source. The second is recoverable by §2's measurement. **The
third is not established** — its terminator was not recovered, and this
experiment does not supply one.

So the honest count is **two of three boundaries obtainable, one open**.

## 4. A declared rule is required, and it is disclosable

Brown's parsing entries also point at segments of the quoted example sentence.
Whether a delimited segment is a part of that sentence is measurable:

```text
rule                                        segments matched
byte-exact                                  80/312   (26%)
case-insensitive                           198/312   (63%)
case-insensitive, punctuation-trimmed      198/312   (63%)
```

Byte equality fails because the source capitalises a word at the head of its
entry — `Patient`, `Ox`, `Submits` — where the sentence has it lowercase.

**This is not a hidden assumption.** `01.External:28` requires a recurrence
assertion to disclose "the rule by which equivalence or sameness was
determined". Case-insensitivity is exactly such a rule, and stating it is the
clause's own requirement rather than a workaround.

## 5. The delimiter is dual-purpose, and the measurement separates the uses

The 37% that never match are a different kind of thing:

```text
   14x  'the, an'
   13x  'to be, to act'
    6x  'ing, d'
    3x  'When? How long? How soon?'
```

Those are quoted inside Brown's *definitions*, not segments of the example.

**The substring test separates the two uses without interpreting either.** A
delimited representation that is a part of the nearby quoted representation is
one kind of occurrence; one that is not is another. No semantics distinguishes
them; a measurement does.

## 6. What this does not establish

**That the three-coordinate shape is lawful.** Untouched. `#2382` and `#2384`
recorded that no clause licenses occupancy of `the relation assertion`, and
nothing here changes that.

**That any of it means anything.** Nothing establishes what `is` means, what
`The` means, that Brown's classification is true, or that the three
representations stand in any relation. `01.Standing.D` refuses relation standing
to co-presence, and this produces co-presence.

**That the anchors were not chosen.** `EXAMPLE PARSED.` and `_..._` were picked
by a reader. Both are enumerable — the relation observer surfaced `OBS. 1` and
this source's citation prefix without being told — but that enumeration was not
re-run here to derive them. The claim is that they *are* enumerable, not that
this experiment enumerated them.

**That it generalises.** These are Brown's parsing exercises, an unusually
regular section of an unusually regular book. Ordinary prose was not tested,
and `"A noun is a word"` as free-standing text was not tested.

**That 161 entries is a corpus.** Twelve blocks in one file.

**That the third coordinate is obtainable.** §3 records it as open.

**That anything was built.** No competency, no segmenter, no runtime change.
These are measurements over a preserved file, reported.

## 7. What it does establish

One thing, and it is the thing that was in question:

```text
the segmentation problem is not necessarily a developer problem
```

For at least one real source, the boundaries the pseudocode hard-codes are
recoverable from the source's own repeated structure, under a disclosable
equivalence rule, using only findings active law already permits a declared
measurement to produce.

That does not make the shape lawful. It removes the objection that the shape
could only ever be reached by a developer choosing it.
