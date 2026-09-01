# Candidate physiology census 001

## Boundary

This is an investigation report. It changes no Book clause, Witness Grammar,
runtime occurrence, reader, current coordinate, or test.

The census begins at `712fa652`. It asks whether the Candidate physiology
declared by `01.Source.E`, `01.Source.E.1`, and `04.Compare.C` has a live exact
Witness after the authored Candidate enumeration road was removed.

The three classifications used here are:

- **live exact Witness** — a recorded occurrence and exact reader establish the
  coordinate now;
- **Book-only** — the Book and Witness Grammar declare the coordinate, but no
  live occurrence establishes it;
- **structural vacancy** — a later coordinate requires the distinction, but no
  live road supplies its subject or occurrence.

Shared words do not join roads. Generic Applicability, Admission,
Participation, Act, Yield, or Compare physiology elsewhere does not establish a
Candidate-specific occurrence.

## Active runtime census

The active runtime contains no Candidate occurrence name, producer, reader,
subject-to-Act binding, Applicability result, Admission relation,
Participation relation, Act occurrence, Yield, result, completeness boundary,
or Compare consumer.

Its only constitutional-looking Candidate surface is the current-coordinate
accumulator `candidate_result_occurrences` in
`seed_runtime/operator_current_coordinates.py`:

```text
initialize {}
take the prior mapping when prior coordinates are supplied
return the mapping
```

No active branch adds an occurrence to that mapping. No runtime test addresses
the mapping. The coordinate therefore provides no live exact Candidate Witness.
It is an empty carried slot, not a Candidate result.

Other lowercase `candidate` locals in active runtime are ordinary Python names
for values being searched or selected. They establish no Candidate grammar by
sharing the spelling.

## Book and Witness Grammar census

| Candidate coordinate | Classification | Exact current testimony |
| --- | --- | --- |
| Candidate subject | Book-only | `01.Source.E.1` declares one exact subject required by one exact Candidate rule; no runtime subject occurrence exists. |
| Candidate subject-to-Act binding | structural vacancy | The Book requires the exact rule, subject boundary, required subject, and Candidate Act to be exact together; no Candidate binding occurrence exists. |
| Candidate Applicability | structural vacancy | The Book requires Applicability for each required subject; no Candidate-specific Applicability binding, Act, or result exists. |
| Candidate Admission | Book-only and conditional | `01.Source.E.1` and `04.Compare.C` require exact Admission where applicable; no Admission occurrence is related to a Candidate. |
| Candidate Participation | structural vacancy | The Book requires the Candidate subject to participate in the exact Candidate or Compare Act occurrence; no such relation occurrence exists. |
| Candidate Act occurrence | structural vacancy | Witness Grammar declares `Candidate`; no runtime Candidate Act occurrence exists. |
| Candidate Yield | structural vacancy | The Book declares `Candidate Act occurrence --Yield--> exact Candidate result`; no exact Candidate Act exists from which this Yield could proceed. |
| Candidate result | structural vacancy | Witness Grammar declares `exact_Candidate_result`; no producer or exact reader exists. |
| Candidate completeness boundary | Book-only | The exact rule and subject boundary are declared as the completeness boundary; no runtime boundary carries Candidate results. |
| Candidate consumption by `04.Compare.C` | structural vacancy | The Book requires an exact Candidate result in current coordinates; no runtime Compare road consumes one. |

No row is a live exact Witness.

## Historical control

The absence is deliberate rather than an incomplete repository search.

`3638df8f` removed
`seed_runtime/candidate_results_from_exact_result_assertions.py` and its tests
under the finding that its two enumeration rules were authored:

```text
every exact source Assertion
every distinct ordered source Assertion pair
```

That commit retained the constitutional statement that an exact Candidate rule,
subject boundary, and required subjects must already be exact. It did not
establish a replacement rule or producer.

`8fdd2cb4` subsequently removed the stale Candidate identity reservations from
the Ledger. Thus neither the deleted producer nor its identity mechanics remain
live testimony.

## Smallest exact finding

```text
Candidate constitutional grammar              declared
Candidate live physiology                      absent
candidate_result_occurrences current slot      empty and never populated
```

The empty current-coordinate slot cannot make Candidate live. Conversely, the
absence of a live Witness does not by itself disprove the Book distinction. The
Book currently describes a structural vacancy whose antecedent exact Candidate
rule and required subjects have not been recovered.

## Cleanup frontier

The next falsifiable subtraction is the empty
`candidate_result_occurrences` current-coordinate accumulator:

```text
remove initialization
remove prior-coordinate carry
remove returned coordinate

ask whether any live exact reader, occurrence, replay, or refusal loses a
coordinate
```

If nothing loses a coordinate, delete the slot without replacing it. That
cleanup must not be described as deleting Candidate from the Book and must not
manufacture a Candidate producer, rule, binding, or Compare road.

