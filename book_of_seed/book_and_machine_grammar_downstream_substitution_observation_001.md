# Book and machine-grammar downstream substitution observation 001

## Question

The preceding substitution observation changed exact local material and asked
five serialization functions whether their returned coordinates recurred. It
stopped at that immediate result. This observation asks a different question:

```text
exact source-addressed substitution
↓
preserve both resulting production populations
↓
continue each population through already-demonstrated structural recurrence
↓
compare their later consequence structure
```

The experiment changes no Book chapter, witness grammar, runtime, or test. It
records no Seed occurrence. It is an observer gauntlet, not the ABCDEF fanout
experiment.

## Reproducible observer

The reusable observer is:

```text
scripts/observe_book_grammar_downstream_substitutions.py
```

The active Book and Fidelity grammar are read as raw bytes. JSON is not parsed
and no grammar name, relation name, heading, expected literal, or expected joint
participates in discovery. JSON is used only to emit the frozen observer
artifact.

The source populations can be bounded independently:

```text
.venv/bin/python scripts/observe_book_grammar_downstream_substitutions.py book
.venv/bin/python scripts/observe_book_grammar_downstream_substitutions.py grammar
```

## Exact source boundary

```text
Book
├── book_of_seed/README.md
└── twelve active chapter files, each retained as an independent source

machine grammar
└── book_of_seed/witness_grammar.json
```

Reports, archive material, Rosetta, tests, and admission inventories are
excluded.

| population | source count | bytes |
|---|---:|---:|
| Book | 13 | 24,881 |
| machine grammar | 1 | 12,885 |

Independent Book files are never concatenated. A recurrence population and its
later consequences remain inside the exact file that supplied them.

## Blind calculation

For each exact source, the observer reconstructs the demonstrated incremental
surface used by variable-extent recurrence:

```text
adjacent source coordinates
↓
complete internal same-content/difference surface
↓
exact recurrence with exact producing source positions
↓
extend by the next source-order coordinate
↓
retain only recurrent complete surfaces
↓
repeat until recurrence stops
```

Within each recurrent complete surface, exact material productions that recur
are retained separately. Every pair of distinct recurrent materials is then
examined without choosing an English or grammar role.

For exact materials `A` and `B`, the observer finds their first and final
differing byte coordinates. It algebraically addresses every three-part split
for which the complete differing interval lies inside exactly the first,
middle, or final part. The remaining two parts must be exact. This yields every
source-addressed occupant substitution at that bounded surface without testing
every possible split against every other split.

The exact producing positions for `A` and `B` then continue independently
through later variable extents. At each later extent the observer records:

- whether each production population still yields recurrent structure;
- whether both yield the same set of internal structural result kinds;
- whether both yield the same structural result kinds and occurrence counts.

The observer does not infer that Yield completes current Standing. It records
only that yielded exact results remain available to the consequence calculation.

## Exact complete-result divergence

The corresponding-coordinate material Measurement adds an important
distinction. Every pair examined here contains distinct exact materials. At the
first recurrent bound, corresponding-coordinate Measurement records the
literal byte carried at every role. At least the substituted coordinate differs
by construction.

Therefore:

```text
substitution A → B
↓
complete exact yielded result population differs immediately
```

This does not prevent the structural result kinds, their counts, or later
structural consequences from remaining the same. Attempting to rebuild and
hash corresponding literal results at every later extent was redundant: exact
complete-result equality is already refused at the first changed coordinate.

The experiment consequently preserves three separate observations:

```text
both production populations continue

same internal structural result kinds continue

same internal structural result kinds and counts continue
```

It does not compress any of those into exact equality of the yielded worlds.

## Frozen artifacts and timing

| population | artifact | bytes | structural digest | exact file digest | wall seconds |
|---|---|---:|---|---|---:|
| Book | `/tmp/seed_book_grammar_joint_downstream_blind_book.json` | 23,402,693 | `e1c561000b43a4505d54eb85ba6059d356aa33ca34899afb1ff788591cacf1d7` | `984abeb530e987557d300107ad3845afd9fb824e2fd6a3719d270027772d4b5a` | 13.771 |
| machine grammar | `/tmp/seed_book_grammar_joint_downstream_blind_grammar.json` | 13,774,460 | `e083ecef0854bbe073a41af7668817aa97d6152f3fc406e9607ef7f17af2f503` | `f2d5e585f8651bf233660a5b323a352d8601ceaf190d94e7958c2ac73b270deb` | 45.715 |

Each independently bounded leg remains below the minute siren.

An earlier observer draft serialized every corresponding-coordinate finding
population to canonical JSON at every later extent. That draft pushed the
grammar leg beyond sixty seconds. The work was redundant for the reason above.
Removing that reconstruction reduced the Book leg from 27.483 seconds to
13.771 seconds and allowed the grammar leg to complete in 45.715 seconds. The
source-addressed split and consequence populations are unchanged.

## Population results

| population | addressed split surfaces | recurrent production pairs | addressed substitution edges |
|---|---:|---:|---:|
| Book | 39,810 | 37,514 | 133,123 |
| machine grammar | 261,229 | 64,548 | 1,209,674 |

The machine grammar has fewer bytes but far more addressable split surfaces.
Its repeated serialized coordinate families supply many distinct material
productions with the same internal structure.

Maximum later rungs observed:

| population | both continue | same structural kinds | same kinds and counts | exact complete results |
|---|---:|---:|---:|---:|
| Book | 57 | 16 | 16 | 0 |
| machine grammar | 194 | 25 | 24 | 0 |

The zero in the final column is a required consequence of substituting exact
material, not a failure to continue.

### Book edge distribution

| later rungs | both continue | same structural kinds | same kinds and counts |
|---|---:|---:|---:|
| 0 | 0 | 0 | 84,099 |
| 1 | 14,708 | 54,871 | 21,459 |
| 2 | 18,626 | 36,359 | 13,164 |
| 3–5 | 43,493 | 36,773 | 12,452 |
| 6–10 | 35,612 | 4,943 | 1,877 |
| 11–25 | 18,752 | 177 | 72 |
| 26+ | 1,932 | 0 | 0 |

### Machine-grammar edge distribution

| later rungs | both continue | same structural kinds | same kinds and counts |
|---|---:|---:|---:|
| 0 | 0 | 0 | 937,763 |
| 1 | 37,305 | 383,968 | 80,262 |
| 2 | 49,666 | 242,021 | 48,513 |
| 3–5 | 166,839 | 363,147 | 73,304 |
| 6–10 | 270,997 | 170,749 | 49,150 |
| 11–25 | 365,616 | 49,789 | 20,682 |
| 26+ | 319,251 | 0 | 0 |

The broad distinction is now observable:

```text
both changed productions keep recurring
!=
their later structural result kinds remain the same
!=
their later structural result populations remain the same size
```

## Blind survivors

The strongest machine-grammar survivors are serialized coordinate-family
siblings. Representative exact substitutions include:

```text
Standing.A  ↔ Standing.D
Standing.D.1 ↔ Standing.D.2
Standing.A  ↔ Standing.B
Standing.A  ↔ Standing.C
```

Several preserve the same structural kinds and counts for 24 later extents.
This is a real representation-level joint: substituting a coordinate member
inside the repeated JSON shape leaves a long serialized consequence intact.
It does not establish that the substituted coordinate has the same
constitutional physiology.

The strongest Book survivors are dominated by newline/indentation families,
punctuation, capitalization, and morphological fragments. Representative
families include changed letters before the same newline indentation, case
changes inside `Supplied`, and changed prefixes before shared `Act occurrence`
material.

These are honest false survivors near the desired joints. Downstream structural
recurrence alone does not eliminate them.

## Post-hoc answer-key inspection

Only after both blind artifacts were frozen were active grammar names used as
an answer key.

Exact complete material appeared among source-derived substitution pressure in
both Book and machine grammar for:

```text
Act
Locality
Yield
relation
result
subject
```

The machine grammar additionally exposed exact complete material for:

```text
Responsibility
Standing
```

No exact complete pressure span was found for `Candidate`, `Carriage`,
`Participation`, or `Support` in this calculation, although shorter fragments
can occur.

This is material addressability only:

```text
exact bytes spell `Yield`
!=
exact material occupies the Yield relation position
!=
a Yield relation occurrence exists
```

The observer recovered representation pressure around several active names. It
did not recover the active relation-Assertion anatomy:

```text
first subject
exact relation content
second subject
```

Nor did it establish Participation, Carriage, Yield, Locality, or Support as a
relation occurrence from the blind split surfaces.

## What substitution several rungs downstream establishes

The preceding five-parser experiment stopped before the result was allowed to
participate in later work. This observer establishes that the omission mattered:

```text
local substitutions indistinguishable at their immediate equality surface
↓
later recurrence consequence
↓
many diverge after a small number of extents
```

Substitution followed by consequence is therefore more discriminating than
substitution followed by an immediate survival check.

It still does not identify Seed's constitutional joints. The independent Act
used here is structural recurrence. That Act bears on repeated source shape;
it does not bear on whether three exact occupants are the first subject,
relation content, and second subject of a relation Assertion.

## Current Standing correction pressure

The active Book accurately refuses the stronger claims:

```text
result existence
→ Standing for that result

Yield
→ later Standing occurrence
```

The observer requires neither claim.

The active Book also contains exact specializations in which current Standing
carries a result and another Responsibility becomes addressable from that
result. `01.Source.D.2`, Candidate work, and `04.Compare.C` already use that
shape. What the general rendering does not state as plainly is:

```text
exact result yielded under a Responsibility branch of current Standing
↓
exact result coordinates remain carried by that current branch
↓
another exact Responsibility may address those coordinates

!=
Standing for the result

!=
later Standing

!=
completion of the yielding Responsibility or its sibling subjects
```

The headings and prose foreground `Later Standing`. Read too literally, that
omission makes later Standing appear to be a prerequisite for every downstream
uptake. The demonstrated specializations show otherwise.

This is Book amendment pressure, not a missing constitutional district. A
future narrow amendment can make the current-Standing carriage explicit while
preserving the refusals above. The observer does not manufacture branch
completion to cross that omission.

## Stopping boundary

The current observer can continue exact source production populations through
structural recurrence because those subjects are already addressable from
exact source coordinates.

It stops here:

```text
exact recurrent bounded production populations
↓
exact source-addressed occupant substitutions
↓
later structural recurrence consequences
↓
many substitutions diverge; some representation siblings remain coherent
↓
no responsible occurrence assigns the three occupants to
first subject / exact relation content / second subject
↓
STOP
```

No current Responsibility makes the blind local split a constitutional joint.
Without that relation-bearing Act, propagating farther would merely measure
more serialization, punctuation, and morphology.

The useful recovery is narrower:

```text
substitute
↓
let both exact results continue
↓
later consequence discriminates many surfaces
```

That pressure is real. It becomes constitutional joint evidence only when the
independent downstream Responsibility bears on the exact relation anatomy being
tested.
