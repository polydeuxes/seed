# Ordinary `!cat` sixteen-book recursive association observation 001

## Question

What does this Seed presently record when the sixteen exact 300-line corpus
windows cross through ordinary `!cat`, and where does stronger association
stop?

The run changes no Book, witness grammar, provider limit, corpus window, or
association rule. Two bounded-replay corrections found during the run are
separate runtime changes described below.

## Direct finding

All sixteen windows crossed the external Witness boundary byte-for-byte.
The complete unprofiled run finished in 19.59 seconds and recorded 726 events
in a 1,974,272-byte SQLite ledger.

The corpus did not reach its first Measurement pass:

```text
sixteen exact 300-line windows
↓
sixteen exact external `cat` output occurrences
↓
sixteen exact Witness material-acquisition results
↓
available in sixteen invocation Localities
↓
material-to-this-Seed Locality relation occurrences: 0
↓
Measurements concerning corpus material: 0
↓
Candidates: 0
↓
Compare results: 0
```

The association experiment therefore stops at exact Witness material
availability. It does not yet show a first atomic association pass, adjacent
association pass, ordered path, or association between paths.

## Exact material

The source is the same fixed population addressed by
`tests/book_material_test_witness.py`:

| position | source | first line | exact bytes |
|---:|---|---:|---:|
| 0 | `grammar_goold_brown.txt` | 6000 | 17,298 |
| 1 | `webster_dictionary.txt` | 6000 | 8,606 |
| 2 | `roget_thesaurus.txt` | 6000 | 19,412 |
| 3 | `grammar_kittredge.txt` | 6000 | 9,942 |
| 4 | `algebra_rivenburg.txt` | 1800 | 7,469 |
| 5 | `boole_laws_of_thought.tex` | 6000 | 12,521 |
| 6 | `euclid_elements.txt` | 6000 | 16,014 |
| 7 | `bash_abs_guide.txt` | 6000 | 7,334 |
| 8 | `cookbook_farmer.txt` | 6000 | 12,651 |
| 9 | `french_les_miserables.txt` | 6000 | 14,903 |
| 10 | `latin_vulgate.txt` | 6000 | 13,004 |
| 11 | `prose_austen_pride.txt` | 6000 | 16,276 |
| 12 | `prose_dickens_copperfield.txt` | 6000 | 14,996 |
| 13 | `prose_franklin_autobiog.txt` | 6000 | 17,352 |
| 14 | `prose_emerson_essays.txt` | 6000 | 19,364 |
| 15 | `prose_hume_enquiry.txt` | 6000 | 10,916 |
| | complete population | | **218,058** |

Every output acquisition matched its addressed window exactly.

## Invocation boundary

At this observation boundary, the active `!cat` road accepted one path
argument and its output boundary was 65,536 bytes. Concatenating the sixteen
windows into one file would have produced 218,058 bytes and crossed that
boundary with known loss. The later single-batch observation raised this
boundary and tested that distinct road directly.

The observation therefore used sixteen commands in one operator-console run:

```text
!cat window-0
!cat window-1
...
!cat window-15
```

This records sixteen operator command occurrences and sixteen invocation
Localities. Those command occurrences are additional subjects in the operator
Locality and affect the operator-side counts below. They must not be mistaken
for structures recovered from the corpus.

No claim is made that sixteen commands and a possible future exact batch road
have interchangeable histories. The present stop occurs before any corpus
Measurement in every invocation Locality, so no corpus association result is
available for such a comparison.

## Time and ledger growth

The first run exposed nonlinear rereading before the sixth host invocation.
It was cancelled after more than ten minutes. A bounded probe then measured:

| corpus windows addressed | profiled time before corrections | events |
|---:|---:|---:|
| 1 | 0.52 s | 51 |
| 2 | 1.39 s | 96 |
| 4 | 8.14 s | 186 |
| 8 | greater than 60 s; terminated | 237 durable rows before termination |

The partial eight-window ledger contained five completed invocations and the
sixth operator acquisition. Its timestamps show the delay before successive
host invocations growing approximately:

```text
0.28 s
0.63 s
1.58 s
4.72 s
14.30 s
greater than 37 s before the sixth invocation
```

The corpus bytes were not responsible for that delay. It occurred after each
operator command acquisition and before the corresponding host invocation,
inside declared Measurement over the operator Locality.

Two runtime corrections were made and pushed separately:

1. `7661b9f4` resolves already-recorded Measurement sources and exact O1
   Locality coordinates from the current validated bounded replay. It no
   longer reconstructs each prior Measurement lifecycle merely to discover
   the next source.
2. `5e893bb2` preserves the validated prior replay while advancing it over
   newly recorded occurrences. Incremental advance no longer clears that
   context and recursively reconstructs the earlier boundary.

The focused read and Measurement checks passed after each correction. Recorded
event populations and exact output matches remained unchanged.

| corpus windows addressed | profiled time after both corrections | events | ledger bytes |
|---:|---:|---:|---:|
| 4 | 2.87 s | 186 | 405,504 |
| 8 | 9.33 s | 366 | 835,584 |
| 16 | 34.00 s | 726 | 1,961,984 |

The final unprofiled sixteen-window run took **19.59 seconds** and recorded the
same 726 events. Its ledger file was 1,974,272 bytes after close; no WAL bytes
remained.

No `/dev/shm` path, retained derived state, or alternate event store was used.

## Remaining slow work

The sixteen-window profile still shows repeated durable-row decoding:

| active road | calls | cumulative time |
|---|---:|---:|
| declared Measurement after operator acquisition | 16 | 25.29 s |
| durable row to event | 99,862 | 20.81 s |
| JSON load for stored event material | 99,862 | 17.68 s |
| Locality event population reads | 161 | 11.08 s |
| exact-byte Measurement recording | 16 | 10.97 s |
| material acquisition result reads | 1,376 | 7.62 s |

The current experiment is now below the one-minute slow boundary, so no third
performance change was made. The remaining cost is nevertheless concentrated
in repeatedly decoding prior Locality rows while verifying new operator-side
Measurement work. It is not filesystem placement.

## Recorded populations

The unprofiled run recorded:

| population | count |
|---|---:|
| total ledger events | 726 |
| operator material-acquisition results | 16 |
| invocation Locality relations | 16 |
| Witness material-acquisition results | 48 |
| nonempty invocation output acquisitions | 16 |
| empty error acquisitions | 16 |
| empty completion acquisitions | 16 |
| operator command byte-pair position Measurement results | 16 |
| operator command exact-byte count Measurement results | 16 |
| operator Locality occurrence-position Measurement results | 16 |
| recorded Representation results | 65 |
| material-to-this-Seed Locality relations in invocation Localities | 0 |
| corpus Measurement results | 0 |
| Candidate results concerning corpus material | 0 |
| Compare results concerning corpus material | 0 |
| raw operator output bytes | 0 |

The three Measurement populations concern the sixteen `!cat` command
occurrences in the operator Locality. They are not findings about the Book
windows returned in the invocation Localities.

## Pass-by-pass observation

| pass | exact input | exact result |
|---|---|---|
| operator command acquisition | sixteen `!cat` commands | sixteen operator acquisitions and their declared Measurements |
| external invocation | sixteen addressed files | sixteen exact nonempty output occurrences |
| Witness acquisition | output, empty error, empty completion per invocation | 48 exact acquisition results |
| corpus Locality prerequisite | sixteen nonempty output acquisitions | no material-to-this-Seed Locality relation occurrence |
| corpus Measurement | no qualified corpus subject | no result |
| Candidate | no corpus Measurement result | no result |
| Compare | no Candidate | no result |
| stronger association | no prior association result | no result |

## Exact stop

```text
exact corpus bytes cross through ordinary `!cat`
↓
exact Witness acquisition in invocation Locality
↓
bounded replay availability
X
no exact material-to-this-Seed Locality relation occurrence
no corpus Measurement Responsibility becomes readable
no corpus finding can input a later pass
```

The run warrants neither fabricating the missing Locality relation nor adding a
recursive driver. It establishes that the complete corpus can now be observed
within the performance boundary and that the next lawful road remains the
already-identified Witness uptake boundary.
