# Measurement-population Candidate Responsibility activation investigation 001

## Question

Why do the established sixteen-book Measurement results produce no Candidate
Responsibility, Candidate Applicability, or Candidate occurrence on the live
operator road?

This investigation changes no Book, grammar, runtime, test, Measurement,
Candidate, or Compare behavior.

## Disposition

The live road does not stop at Candidate Applicability. It stops before current
Standing exposes an exact Candidate Responsibility branch; correspondingly,
the runtime carries no durable Candidate Responsibility record:

```text
current Standing carries exact Measurement results
↓
no Candidate Responsibility branch
↓
no required Candidate subject-to-Act position
↓
no Candidate Applicability
no Participation
no Candidate Act
no Candidate result
STOP
```

The current exact-result Candidate module is not a continuation discovered
from current Standing. Its public entry points require a caller to supply a
ledger-wide append boundary and recording Locality, record both Candidate
Responsibilities explicitly, and then request Candidate results explicitly.
The live console imports or invokes none of those entry points.

Measurement availability therefore does not currently expose the Candidate
Responsibility declared by `01.Source.E.1`.

## Active clause and runtime entry disagree

Active `01.Source.E` begins from current Standing carrying an exact addressed
source result. `01.Source.E.1` then gives the Candidate Responsibility an exact
bounded source-Assertion population.

The runtime constructor has no current-Standing coordinate and no exact
addressed-result coordinate:

```text
record_one_source_candidate_responsibility(
    ledger,
    source_append_boundary,
    recording_locality_identity,
)

record_ordered_pair_candidate_responsibility(
    ledger,
    source_append_boundary,
    recording_locality_identity,
)
```

It reads every Measurement, Compare, and Candidate result carried through the
supplied ledger boundary across every Locality. The caller also chooses the
Locality in which the runtime Responsibility record is written.

The resulting runtime direction is:

```text
caller-supplied global ledger boundary
+ caller-supplied recording Locality
↓
record Candidate Responsibility
↓
construct its subject population
↓
Candidate Applicability
```

That is not the active clause direction:

```text
exact current Standing
+ exact addressed source result
↓
exact Candidate Responsibility branch
```

No current function establishes that second direction.

## Existing tests create the runtime record themselves

`tests/test_candidate_results_from_exact_result_assertions.py` does not begin
from the ordinary console. Its `_one_source_responsibility(...)` helper:

```text
records exact material
records an exact-byte Measurement directly
freezes ledger.append_boundary()
calls record_one_source_candidate_responsibility(...)
```

Every Candidate lifecycle test begins after that explicit constructor call.
The tests prove Candidate behavior after the Responsibility exists. They do not
prove that current Standing exposes the Responsibility or that the console can
recover it.

The predecessor Candidate implementation was likewise called directly from
tests and the calculator Witness. Repository history contains no exact-result
Candidate constructor call from `operator_console.py`.

The `tatatata` history does not supply the missing Candidate activation.
Commit `6f894d6d` directly recorded ordered paths of adjacent pair relations in
the byte-pair Measurement result. Commit `75dc6b16` reverted that implementation.
The current replacement separates recurrence, recurrent-pair position
Measurement, and shared-position Measurement. That history establishes the
recursive pair road; it contains no exact-result Candidate Responsibility
constructor and no current-Standing-to-Candidate continuation.

## The live Measurement result shape is presently unreadable

A second independent stop appears if the current constructor is manually
applied to a ledger produced by the ordinary console.

The Candidate source reader handles a generic `assertions` dictionary before
its specialized position-result branch. A position-coordinate Measurement
result carries an aggregate addressed-position account at `assertions`; that
account is not itself an Assertion address. The generic reader therefore
refuses before the specialized reader can expose the exact addressed position
references:

```text
ordinary b"tatatata" Witness road
↓
60 durable events and complete Measurement results
↓
source_assertion_references_through_boundary(...)
↓
ValueError:
Candidate production requires one exact Assertion carried by a result
```

The Candidate tests create only an exact-byte Measurement result in their
common source helper. They do not place the ordinary position-coordinate result
before the source reader, so the mismatch is not exercised there.

Correcting this reader alone would not establish live activation. It would
only permit the caller-created, ledger-wide Candidate Responsibilities to see
the live result population.

## The supplied boundary is much broader than an addressed result

For observation only, the position-result reader was corrected in process
without changing repository files. The exact sixteen-book ledger then carries
these Candidate source-reference populations:

| carried Measurement result coordinate | source references |
|---|---:|
| position-coordinate results | 218,131 |
| exact-byte results | 578 |
| byte-pair results | 9,742 |
| Locality occurrence-position result | 21 |
| complete population | 228,472 |

Under the current Candidate rules this becomes:

```text
unary required subjects         228,472
ordered required subjects        52,199,226,312
```

This population is not produced by the live console; it is the consequence of
manually supplying the complete ledger boundary to the Candidate constructor.
It demonstrates why connecting that constructor after Measurement would not be
a neutral continuation from an exact addressed result.

## Applicability cannot discover the Responsibility

Candidate Applicability occurs only inside
`_record_candidate_result_for_subject(...)`, after:

```text
Candidate Responsibility already recorded
↓
required subject already constructed
↓
Applicability Responsibility and Act
↓
Applicability result
```

The result is currently fixed to:

```python
"finding": "applicable"
```

Applicability therefore performs no upstream discovery of Candidate
Responsibilities and cannot explain why the Measurement population should
activate either Candidate road. It only restates the subject-to-Act position
already constructed under the caller-created Responsibility.

The module also records no Candidate Admission occurrence. Active
`01.Source.E.1` and machine grammar retain exact Admission prior to
Participation where that boundary requires it. The present lifecycle proceeds
directly from Applicability to Participation. This mismatch is downstream of
the missing Responsibility branch, but it prevents the current module from
being treated as a complete live implementation of the active clause.

## Performance observation

The ordinary console completed the sixteen-book acquisition and Measurement
road in 11.76 seconds during this investigation.

The existing Candidate source reader, with only the position-result ordering
corrected in process, exceeded 90 seconds before producing its reference tuple
and was interrupted. No Candidate Responsibility or Candidate result had been
recorded. A direct count over the already validated Measurement result
coordinates produced the exact 228,472 population without constructing the
ledger-wide reference objects.

The nested read explains the unbounded delay:

```text
references_to_recorded_position_coordinates_of_byte_pair_occurrences(...)
→ reads and validates the position result
→ enumerates every addressed position reference

for each reference:
    _recorded_position_assertion_coordinates_for_locality_movement(...)
    → reads and validates the complete position result again
    → scans from the first position until its Assertion address matches
```

For `N` addressed positions, the second phase repeats complete-result reading
`N` times and performs approximately `N * (N + 1) / 2` position comparisons.
Measured scaling confirms the quadratic reconstruction:

| addressed position references | source-read time |
|---:|---:|
| 63 | 0.128 s |
| 127 | 0.368 s |
| 255 | 1.220 s |
| 511 | 4.403 s |
| 1,023 | 16.626 s |

A 511-reference profile recorded:

```text
complete profile time                                      8.217 s
_recorded_position_assertion_coordinates... calls             511
complete _read_result calls                                   511
bounded Standing replay calls                                 511
_assertion_identity calls                                 131,327
canonical JSON/hash operations                            395,003
```

The dominant cumulative costs were 6.379 seconds in Assertion-address
calculation, 4.141 seconds in canonicalization, 3.930 seconds in `json.dumps`,
and 1.241 seconds in repeated bounded Standing replay.

The corpus has 218,057 stdout positions. The current nested read implies about
23,774,754,710 Assertion-address calculations and 71,324,700,244 canonical
JSON/hash operations. Extrapolation from the measured curve is approximately
8.7 days. This reconstructs coordinates the first enumeration already
recovered.

The expanded source-reference objects also retain approximately 1,042 bytes
per reference and reached about 1,296 bytes per reference during the bounded
memory probe. At the stdout position population alone, that projects to about
227 MB retained and 283 MB peak before the global ordering/deduplication
structures and the public API's second deep copy.

This is a source-read bottleneck, not the reason Candidate is absent from the
live road. The live road never calls the reader.

## Exact stop

The current stop is:

```text
exact current Standing
├── position-coordinate Measurement results
├── exact-byte Measurement results
├── pair count Assertions
└── recurrence Assertions

required next coordinate:
exact Candidate Responsibility branch for an exact addressed source result

established:
Candidate law and direct Candidate constructors

not established:
current Standing → exact Candidate Responsibility branch
```

Do not connect the global-boundary constructors to the console. Do not correct
the position reader merely to expose 52,199,226,312 ordered subjects. Do not
make Candidate Applicability discover Responsibilities. Do not optimize the
reader as a substitute for the missing exact Standing/result boundary.

The next investigation must orient how an exact Candidate Responsibility is a
branch of current Standing carrying an exact addressed source result, without
recreating Assignment, caller choice, or a global ledger population.
