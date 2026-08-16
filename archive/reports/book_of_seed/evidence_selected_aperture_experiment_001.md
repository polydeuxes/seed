# Evidence-selected measurement apertures: experiment 004

Findings only. No Book amendment. `#2389`'s measurement mechanism is used
unchanged; nothing new was built.

## Executive

The question:

```text
can a recorded finding supply the aperture for a later measurement
without a reader choosing the range, delimiter, representation,
or expected occupant?
```

**Three of those four hands come off. One does not.**

```text
delimiter           removed -- none is used
representation      removed -- candidates are enumerated from the material
expected occupant   removed -- the downstream occupant is enumerated
range               still chosen -- the material's extent and how the field
                    is divided remain reader-supplied
```

**The evidence differentiates candidate apertures on its own.** Of 180
candidates measurable in every scope, **13 produced a downstream finding that
agreed across all eight independently bounded scopes**. The other 167 did not.
No threshold was applied; the discriminator is agreement across scopes, which
is what `#2390` found is the signal that survives.

**And the discrimination does not depend on a tokenization rule.** Repeating the
experiment over character n-grams, with no whitespace convention at all, still
separates stable candidates from unstable ones.

Nothing here establishes meaning, grammar, relation, or truth.

## 1. Method

Material: 4,000 contiguous lines of the grammar corpus, taken **outside** the
parsing regions `#2386` and `#2390` used, fed through the operator console as
one session. 4,000 preserved ingress occurrences.

No parsing region, delimiter, representation, or expected occupant was supplied.

```text
1  divide the preserved occurrences into 8 equal consecutive scopes
2  candidates = every representation measurable in every scope
      not a threshold on interest; a requirement for comparability
3  for each candidate, in each scope independently:
      which representation most often occupies the position after it?
4  a candidate's stability = how many scopes returned the same answer
```

Step 3 is adjacency, one of the six findings `01.External:28` permits a
declared measurement to produce.

## 2. Result: the evidence separates the candidates

```text
stability     obs   candidate boundary -> downstream occupant
     100%    1913           'of' -> 'the'
     100%     755           'in' -> 'the'
     100%     470         'that' -> 'the'
     100%     323           'it' -> 'is'
     100%     294           'by' -> 'the'
     100%     256         'have' -> 'been'
     100%     240          'for' -> 'the'
     100%     221         'from' -> 'the'
     100%     153          'may' -> 'be'
     100%     133          'has' -> 'been'
     100%      79           'It' -> 'is'
     100%      25    'according' -> 'to'
     100%      21        'seems' -> 'to'
      88%    1103          'and' -> 'the'
      88%     120         'what' -> 'is'
      88%      98          'can' -> 'be'

13 of 180 candidates reached agreement across all 8 scopes.
```

**[inference]** The material discriminates. 167 candidates were measurable
everywhere and produced no stable downstream finding; 13 did. A reader supplied
neither list.

**One incidental observation, recorded because it was not sought.** `is`
reappears here — `'it' -> 'is'`, `'It' -> 'is'` — from a completely different
aperture, in ordinary prose rather than parsing exercises, with no delimiter
involved. `#2390`'s finding and this one share an occupant and share no method.
That is corroboration between independent measurements, and it is **not**
evidence that `is` means anything.

## 3. The tokenization rule is not load-bearing

Splitting on whitespace is an English convention, so §1 step 2 was a reader
choice. Repeating the whole procedure over character n-grams removes it
entirely:

```text
n-gram   candidates   fully stable across 8 scopes   strongest
  2            487                            165    ' t' -> 'h'
  3          1,583                            495    ' th' -> 'e'
  4          2,095                            678    ' the' -> ' '
```

**[inference]** The separation of stable from unstable candidates survives with
no notion of a word. Whatever the physiology is measuring, it is not an artifact
of a segmentation rule someone supplied.

## 4. What still requires reader choice

Stated exactly, because this is the point of the investigation:

```text
still chosen                     why it is a choice
the material's extent            4,000 lines beginning at an arbitrary offset
how the field is divided         8 scopes; the count is arbitrary, though
                                 the contents of each are not
the measurement family           adjacency, and at what granularity

no longer chosen
which representation to measure  enumerated from the material
which occupant to expect         enumerated from the material
any delimiter                    none is used
any threshold                    stability is agreement, not a cutoff
any grammatical category         none appears anywhere
```

**[inference]** The remaining choices are about *where to look and at what
resolution*. None of them names a representation, an occupant, or a boundary.
That is a different kind of choice from the one `#2386` and `#2390` recorded,
where a reader supplied `EXAMPLE PARSED.` and the delimiter itself.

**[Unknown]** Whether the extent and the division can themselves be
evidence-selected. Nothing here attempts it.

## 5. What this does not establish

**That any of it means anything.** `01.Standing.D` refuses relation standing to
co-presence. Every finding above reports which representation follows which,
and that is co-presence.

**That stability is warrant.** `01.Kinds:32` requires a responsible occurrence
for any relation warrant. Agreement across scopes is agreement between preserved
findings, and `05.Testimony:27` lets a comparison consume such findings while
preserving each one's confidence and standing — not merge them into a stronger
one.

**That the 13 are a discovery about English.** They are counts under a stated
measurement in a stated scope. That a reader recognises them as English
collocations is the reader's knowledge, not Seed's.

**That the physiology was recorded here.** The candidates were enumerated and
compared in a scratch run. `#2389` is the mechanism that would preserve each
finding with its premise; this experiment did not record 180 findings, and the
loop is therefore demonstrated but not preserved.

**That eight scopes is enough.** One division of one body of one file.

**That the unstable 167 are uninformative.** They were not examined. A candidate
whose downstream finding varies may be reporting something real about variation.

**That anything was built.** `#2389` unchanged.

## 6. What it does establish

```text
a recorded finding can supply the aperture for a later measurement
without a reader naming the representation, the occupant, or a delimiter

the material differentiates candidate apertures on its own,
by downstream agreement across independently bounded scopes

that differentiation does not depend on a segmentation rule
```

What remains reader-supplied is extent and resolution — where to look and how
finely — not what to look for.
