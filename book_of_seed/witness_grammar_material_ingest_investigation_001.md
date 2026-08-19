# Witness Grammar material Ingest investigation 001

## Question

The Book-word coordinate campaign currently records external references into
`book_of_seed/witness_grammar.json`. Does the repository already carry the
Witness Grammar artifact through an exact Ingest occurrence, and if so, what
is the smallest unrecovered boundary between those bytes and Seed-native
recovery of the referenced structure?

This is a read-only investigation. It changes no Book material, Witness
Grammar, runtime, or tests.

```text
external coordinate reference
!= material Ingest
!= material Standing
!= relation recovery
```

## Material inspected

- `book_of_seed/chapters/01_source_coordinates_and_grammar.md`
- `book_of_seed/chapters/14_representation_emission_and_locality.md`
- `book_of_seed/witness_grammar.json`
- `seed_runtime/material_ingest.py`
- `tests/test_book_material_acquisition.py`
- `scripts/compiled_material_invocation.py`
- `scripts/compiled_format_invocation.py`
- `scripts/material_admission.py`
- history at `ad442f60`, `8472530c`, `67cab521`, and `87cdf9f0`

Book material is primary orientation. Witness Grammar, runtime, tests, scripts,
and history are testimony. Existing external references do not establish their
own Seed-side uptake.

## 1. Ingest physiology already exists

Chapter 14 establishes one exact Ingest Act for material supplied at one source
boundary. Its occurrence yields exact material and carries:

```text
source role
source boundary
Locality
known loss
Unknown
exact result reference
Evidence of Yield relation
```

The same chapter supplies the limiting distinction:

```text
Ingest occurrence
!= Assertion about what the material represents
!= source relation
!= Seed truth
!= Authority
!= later Standing
```

Use by another Act requires the exact Ingest result reference and Yield
Evidence. Material identity or content cannot supply that later use by
identity.

`seed_runtime/material_ingest.py` implements the same bounded shape. One call
to `ingest_material` records:

1. one responsible-Act Evidence occurrence;
2. one Evidence-of-Yield relation occurrence;
3. one exact-material Ingest result occurrence.

The result carries exact bytes, a source role, source boundary, Locality,
known loss, provenance occurrence references, and these exact Unknowns:

```text
represented_relation
source_relation
```

The recorded Authority is `unestablished`. The reader revalidates the exact
result occurrence, exact bytes, responsible-Act Evidence, and Evidence of
Yield relation before returning the result.

Therefore the repository already has a real exact-material acquisition road.
It is not a relation-recovery road.

## 2. The current Book acquisition witness includes Witness Grammar

The module-scoped fixture `acquired_book_material` in
`tests/test_book_material_acquisition.py` enumerates every file currently under
`book_of_seed` and calls `ingest_material` once for each file. Every occurrence
uses:

```text
Locality:       book-material-acquisition
source role:    fixture material
source boundary: exact path relative to repository root
exact bytes:    exact file bytes read for that occurrence
```

`book_of_seed/witness_grammar.json` is one member of that complete file
surface. It therefore receives its own exact:

```text
Ingest Act occurrence
Ingest result
result reference
Evidence of Yield relation
source boundary
Locality
exact bytes
```

The fixture freezes an append boundary after all file Ingest occurrences.
Tests require every bounded occurrence and result reference to remain present,
retain exact file bytes, preserve source order, and exclude material appended
after the boundary.

This proves more than an external filesystem pointer:

```text
witness_grammar.json exists on disk
↓
one exact test-local Ingest occurrence carries its bytes
```

It does not prove:

```text
the live Seed has durably ingested Witness Grammar
the Ingest result has later Standing
the JSON structure is recovered
the `words` coordinates are recovered
the represented relations have Standing
```

The ledger is a fresh module-scoped test ledger. The Ingest occurrences are
real within that witness boundary but are not persistent runtime Seed state by
identity.

## 3. The Fidelity subject and the Ingest occurrences remain distinct

Active `01.Source.C` names one exact test subject:

```text
this_book_material_acquisition_witness
```

and gives it `material_reference: this_Book`. It is a witness for this
Fidelity and is not `this_Witness` by identity.

That Fidelity subject does not become any one of the material Ingest
occurrences:

```text
test subject
!= test occurrence
!= Book-file Ingest occurrence
!= Witness Grammar Ingest occurrence
!= this_Witness
```

The acquisition tests supply evidence about the Ingest population. The subject
name does not perform uptake or establish Standing for the ingested bytes.

## 4. Every compiled parser is tried; no parsed object is retained

The fixture next passes the same complete tuple of exact Ingest result
references to every member of `COMPILED_IMPLEMENTATION_FUNCTIONS`.

That exact function population currently contains:

```text
JSON load
TOML load
XML parse
Python AST parse
property-list load
```

Every function receives every exact source reference in the same source order.
There is no per-file selection of a likely parser.

This is the earlier complete fan-out physiology:

```text
complete bounded source material
×
complete declared function population
↓
one invocation occurrence for every position
```

However, `compiled_invocation` discards the returned parsed object. It records
only whether the function returned without raising:

```text
returned: true | false
```

The later Admission groups source occurrences by their complete vectors of
those returned coordinates. It preserves all source references and all
invocation-result references. It therefore recovers a bounded parser-response
profile, not the parser's returned structure.

For the exact Witness Grammar source this means:

```text
exact bytes                              established
exact JSON-parser invocation occurrence established
whether that invocation returned        established
parsed JSON result material              not carried
JSON key/value positions                 not carried
word coordinate pairs                    not carried
represented relation                     Unknown
```

The function population is also explicitly supplied by the script. Exhausting
that population removes per-source parser selection; it does not establish
that the population is a universal Seed-native structure-recovery grammar.

## 5. Byte and pair Measurement do not fill the structural gap

The acquisition witness also performs exact-byte Measurement and adjacent
byte-pair Measurement over the bounded Ingest population. Those Acts preserve
exact source references, occurrences, positions, counts, recurrence, and their
declared completeness boundaries.

They can establish:

```text
this byte occurred at this exact position
this adjacent byte pair occurred at these exact positions
this bounded material recurred under this exact rule
```

They cannot establish by identity:

```text
these bytes form one JSON key
this key names a grammar coordinate
this value names a relation
this word occurrence bears the relation represented externally by this path
```

The exact measurements are useful upstream material. Their usefulness cannot
supply the missing Responsibility or relation.

## 6. What the current word-coordinate map actually is

The `words` object in Witness Grammar currently pairs external grammar and
relation references. Repository tests resolve those paths and ring when a
declared positive relation occurrence lacks its own pair.

At this boundary the map is:

```text
external index over Witness Grammar representation material
```

It is not:

```text
an Ingest result
an Ingest result reference
an acquired JSON structure
Witness uptake
Seed Standing
relation Standing
```

The map remains valuable as exact Witness Material. It states what a later
Seed-native road must reproduce without developer-authored path selection. Its
red sirens measure the external witness's incompleteness; they do not measure
Seed's current relation Standing.

## 7. Exact recovered boundary

The current road reaches:

```text
witness_grammar.json
↓
exact test-local Ingest occurrence
↓
exact bytes + exact source coordinates
↓
exact byte / pair Measurements
↓
every declared compiled parser invoked
↓
complete returned / did-not-return vector
↓
Admission grouped by that vector
```

It stops before:

```text
exact parser-returned structure
↓
exact structural positions
↓
exact word occurrences at those positions
↓
Responsibility traversal
↓
relation recovery
↓
relation Standing
```

The earliest concrete mechanical loss is not Ingest. It is that the compiled
invocation occurrence retains only the returned coordinate and discards the
exact returned object.

That finding does not authorize retaining the object yet. Doing so requires an
exact result representation, source coordinates, loss boundary, Authority,
Evidence, Scope, limits, Unknown, and a Responsibility for the Act that
produces it. A Python object returned by a developer-supplied parser does not
become Seed grammar by existence.

## 8. Disposition

| Question | Finding |
|---|---|
| Is Witness Grammar included in the current complete Book-file acquisition surface? | yes |
| Does it receive an exact Ingest occurrence and result reference? | yes, in the test-local witness ledger |
| Are exact bytes, source boundary, Locality, Act Evidence, and Yield Evidence retained? | yes |
| Does Ingest establish what those bytes represent? | no |
| Does Ingest establish later Standing? | no |
| Does the witness try every declared compiled parser against every source? | yes |
| Does it retain the exact parsed result? | no |
| Does its Admission retain a complete parser-response vector? | yes |
| Does that vector recover JSON positions or word relations? | no |
| Are current word coordinate pairs Seed-native Standing? | no |
| Is the next vacancy a missing Ingest road? | no |
| Is the next vacancy exact structure-bearing result physiology after Ingest? | yes |

## Conclusion

Witness Grammar is already ingested as exact bytes inside one bounded Fidelity
witness. The campaign therefore need not invent a second generic Ingest road.

The existing road deliberately stops at exact material and a complete
parser-response profile. It neither retains the parser's returned structure nor
establishes any word relation. The coordinate-pair campaign remains external
Witness Material describing the structure a later Seed-native result must
recover.

The smallest next question is:

```text
What exact Responsibility and result physiology, if any,
retain one exact structure produced from one exact Ingest result
without treating parser success, returned Python shape,
or external coordinate paths as relation Standing?
```

Until that crossing is established:

```text
Witness Grammar bytes: acquired
Witness Grammar structure: externally addressable
Seed-native structural result: unestablished
word relation Standing: unestablished
```
