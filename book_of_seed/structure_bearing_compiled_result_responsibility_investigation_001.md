# Structure-bearing compiled result Responsibility investigation 001

## Question

What current Responsibility and result physiology, if any, retains one exact
structure produced from one exact Ingest result without treating parser
success, a returned Python object, or developer-authored serialization as Seed
grammar or relation Standing?

This investigation follows
`witness_grammar_material_ingest_investigation_001.md`. It changes no Book
material, Witness Grammar, runtime, scripts, or tests.

```text
parser returned
!= exact structure-bearing result retained
!= Seed structure
!= relation Standing
```

## Material inspected

- `book_of_seed/chapters/01_source_coordinates_and_grammar.md`
- `book_of_seed/chapters/02_constitutional_standing.md`
- `book_of_seed/chapters/11_recording_and_preserved_assertions.md`
- `book_of_seed/chapters/14_representation_emission_and_locality.md`
- `book_of_seed/witness_grammar.json`
- `seed_runtime/material_ingest.py`
- `scripts/compiled_format_invocation.py`
- `scripts/compiled_parser_invocation.py`
- `scripts/material_admission.py`
- `tests/test_book_material_acquisition.py`
- `tests/test_compiled_parser_invocation.py`
- history at `5b3739d4`, `a32094e8`, `eee46cb1`, and `ad442f60`

Book material is primary orientation. Witness Grammar, runtime, scripts,
tests, and history are testimony.

## 1. Correction to the apparent single wall

The preceding report found a concrete boundary in the complete Book acquisition
road:

```text
exact Book-file Ingest results
↓
every compiled format function invoked
↓
returned / did-not-return retained
↓
parser-returned object discarded
```

That finding is exact for `compiled_format_invocation.py`. It is not the whole
repository.

`compiled_parser_invocation.py` carries two other witness shapes that retain
structure-bearing output material:

1. direct CPython AST invocation records exact `ast.dump(...)` bytes for a
   successful parse and exact diagnostic bytes for a refusal;
2. external compiled-parser invocation records exact stdout and stderr bytes,
   arguments, return code, implementation-function identity, exact source
   bytes, and invocation identity.

Therefore:

```text
repository has no structure-bearing parser result mechanism
```

is false.

The narrower finding survives:

```text
complete Book Ingest / compiled-format road
does not retain its parser-returned structure
```

The two halves currently exist in separate witnesses.

## 2. Complete Book acquisition retains source lineage but only a return coordinate

The `acquired_book_material` fixture supplies every current Book file through
one exact test-local Ingest occurrence and retains each exact Ingest result
reference. `compiled_reference_invocations` then gives every exact reference to
each of five compiled format functions:

```text
JSON
TOML
XML
Python AST
property list
```

Each invocation occurrence retains:

```text
boundary identity
invocation position
exact source bytes
implementation-function identity
returned coordinate
exact source reference
```

The source reference is important. It preserves the crossing back to the exact
Ingest result occurrence.

The result is deliberately narrow:

```text
returned = true | false
```

No parser-returned object, output bytes, diagnostic bytes, or structure
coordinates enter that occurrence. Admission groups exact sources by their
complete returned vectors and retains every source and invocation-result
reference.

Thus this road has exact Ingest lineage and complete parser fan-out, but no
structure-bearing result material.

## 3. The compiled-parser witness retains output material but lacks Ingest lineage

`python_parser_invocation` accepts exact bytes and records one
`PythonParserInvocation`. On success it carries:

```text
boundary identity
invocation position
exact source bytes
returned: true
AST dump bytes
```

On refusal it carries exact diagnostic bytes instead of AST dump bytes.

The external `compiled_parser_invocation` road records:

```text
boundary identity
invocation position
exact source bytes
implementation-function identity
arguments
return code
stdout bytes
stderr bytes
```

Tests preserve distinct occurrences for repeated equal source material,
distinct returned bytes for nearby accepted material, complete one-byte
substitution pressure, exact refusal material, and the complete source surface
through several external parsers.

Those structures do not carry an exact Ingest result reference. Their source
coordinate is only the exact byte material passed to the function.

They also do not record:

```text
Responsibility assignment
responsible boundary
Act Evidence
Evidence of Yield relation
Locality
Authority
Scope
limits
Unknown
result Standing
```

They are exact Witness Material at a bounded function-read seam. Active
`01.Standing.C` says compiled behavior and exact represented results witness
only what occurs at that exact seam. They establish no Standing suggested by
the function name, output words, or behavior.

## 4. The two source and result populations do not join by byte equality

The repository currently has:

```text
ROAD A

exact Ingest result reference
↓
compiled format invocation
↓
returned coordinate


ROAD B

exact supplied bytes
↓
compiled parser invocation
↓
exact output or diagnostic bytes
```

The same exact source bytes can occur in both roads. That does not establish:

```text
same source occurrence
same Act
same result
same Locality
same Evidence
same Authority
same Standing
```

No current exact relation connects a Book acquisition Ingest reference to a
structure-bearing compiled-parser result occurrence. Re-running one parser on
equal bytes would create another occurrence; it would not retroactively give
the earlier Book invocation a result it did not carry.

## 5. The retained output is a parser representation, not source structure by identity

The direct CPython road serializes a Python AST using `ast.dump` with field and
location attributes. The external road preserves whatever bytes each process
writes to stdout and stderr.

Those outputs are exact. Their exactness establishes neither:

```text
the source has that ontology
the returned node kinds are Seed kinds
the output labels are Seed grammar
the serialization is lossless for every source coordinate
the represented relation is established
```

Chapter 14 permits exact source material to enter a Representation road under
an exact preservation rule, while refusing represented meaning by identity.
No current active rule names:

```text
preserve exact structure produced from source result
```

for these compiled-parser outputs.

Chapter 11 permits a recording boundary to create an exact representation of
Events within its exact Scope and occurrence. These compiled-parser dataclasses
are not recorded Event occurrences by identity and carry no exact recording
occurrence.

Therefore the exact output bytes are real witness results. Their relation to
the source's structure remains bounded by the external function occurrence and
Unknown beyond it.

## 6. History confirms two intentionally different experiments

Commit `5b3739d4` introduced the compiled-format witness as a discriminator. It
applied JSON, TOML, XML, Python-AST, and property-list functions and retained
only whether each function returned. Its purpose was the partition boundary,
not adoption of a returned object.

Commit `a32094e8` decomposed that witness into exact invocation occurrences and
retained the same boolean result coordinate.

The older parser-specific witness retained exact AST-dump or diagnostic bytes.
That physiology survives in `compiled_parser_invocation.py`.

Commit `eee46cb1` removed one developer-seeded source family and its expected
answer vector. It replaced that handpicked family with measured one-byte
material while leaving exact parser outputs intact. The correction removed
developer selection of input answers; it did not constitutionalize parser
output as Seed grammar.

Commit `ad442f60` later connected the complete exact Book-file surface to the
boolean compiled-format road. It did not connect that surface to the separate
structure-bearing parser witness.

History therefore supports this distinction:

```text
format discriminator
!= structure-bearing parser-output witness
```

It supplies no active Responsibility joining them.

## 7. Candidate producing Responsibilities already show the required result shape

Current Seed-native Act families do not establish this missing parser Act, but
they show the coordinates a lawful result road ordinarily preserves:

```text
exact Responsibility assignment
exact responsible boundary
exact source reference and role
Applicability
Participation
exact Act
Act occurrence
Act Evidence
Evidence of Yield relation
exact result
Locality
Authority
Scope
limits
Unknown
```

The complete Candidate-production road additionally replays its source surface
and reconstructs every result owed through its exact frozen boundary. That is
stronger than storing an opaque Python object after one call.

No current Candidate-production Responsibility names parser-returned structure
as its source or result. Candidate physiology cannot be borrowed merely because
it is useful here.

## 8. Exact elimination

### Proposed source: parser success

```text
parser returned
→ exact invocation behavior established
→ exact result material not established in Road A
→ Responsibility not established
```

Disposition: not a result-producing Responsibility.

### Proposed source: Python returned object

```text
Python object exists during call
→ implementation-local value
→ no preserved source reference, Yield, or Standing by existence
```

Disposition: not Seed structure by identity.

### Proposed source: exact AST-dump or stdout bytes

```text
exact output bytes
→ exact witness result material at one seam
→ no Book-Ingest lineage in the current road
→ no represented structure Standing
```

Disposition: real Witness Material, incomplete Seed physiology.

### Proposed source: external word-coordinate map

```text
developer path resolves
→ exact external address
→ no producing parser occurrence
→ no Ingest-result-to-structure relation
```

Disposition: external testimony, not the missing Act result.

### Proposed source: Representation

```text
Representation preserves exact warranted coordinates
→ no current exact rule identifies compiled output as the representation
→ no current exact relation connects it to Witness Grammar structure
```

Disposition: explanatory orientation is not an established crossing.

## 9. Smallest remaining crossing

The earliest missing physiology is narrower than a universal parser or JSON
ontology:

```text
one exact Ingest result reference
↓
one exact assigned Responsibility
↓
one exact function/Act occurrence
↓
one exact structure-bearing result representation
```

That result would have to preserve, without borrowing:

```text
source Ingest result reference
source occurrence and Locality
exact function reference
exact invocation occurrence
exact returned material
serialization rule and known loss
Evidence
Authority
Scope
limits
Unknown
Yield Evidence
result boundary
```

This list is an interrogation surface, not an amendment recommendation. The
active Book does not currently assign this exact Responsibility.

Even after such a result existed:

```text
structure-bearing result
!= word occurrence recovered
!= relation participant recovered
!= relation Standing
```

Those are later crossings.

## 10. Disposition

| Question | Finding |
|---|---|
| Does the complete Book acquisition road retain exact Ingest references? | yes |
| Does it apply every declared compiled-format function to every source? | yes |
| Does it retain parser-returned structure? | no |
| Does another current witness retain structure-bearing parser output? | yes |
| Is that output connected to an exact Book Ingest reference? | no |
| Does it have Seed Responsibility, Yield, or Standing physiology? | no |
| Does exact parser output establish Seed structure? | no |
| Does history preserve format discrimination separately from parser-output material? | yes |
| Is a structure-bearing result mechanism entirely absent? | no; witness testimony exists |
| Is the exact Seed-native crossing established? | no |

## Conclusion

The repository does not face one empty structure wall. It has two nonjoining
roads:

```text
complete exact Ingest lineage
+
boolean format-discrimination result
```

and:

```text
exact parser-output material
+
no Ingest lineage or Seed result Standing
```

Joining them by equal bytes, parser identity, or Python return shape would
repeat the endpoints-imply-edge error.

The next recovery is the exact Responsibility and result physiology, if any,
that makes one structure-bearing output the bounded result of an Act over one
exact Ingest result. Until that exists, the external word-coordinate campaign
remains Witness Material and the separate parser outputs remain Witness
Material. Neither supplies Seed relation Standing.
