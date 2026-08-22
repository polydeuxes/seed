# Measurement-result Candidate activation investigation 001

## Question

Why does the ordinary `!cat` road stop after its carried Measurement results
when Candidate production already consumes Measurement, Compare, and Candidate
result coordinates?

This investigation changes no Book, grammar, console, Measurement, Candidate,
or Compare behavior.

## Corrected finding

The prior disposition oriented the next road too quickly toward Candidate.
Repository tests already demonstrate a narrower association road:

```text
exact material
↓
byte-pair count Measurement
↓
recurrence Assertion where exact count exceeds 1
↓
exact recurrent-pair subject
↓
position premise concerning that exact pair
↓
Compare against occurrences in later exact material
```

Candidate does not own that narrowing. Commit `6ccdc256` explicitly corrected
the recurrent-pair carrier from `ExactMaterialPairCandidate` to
`ExactRecurrentMaterialPairSubject`. The finding yielded by Measurement is
already the exact subject. Calling it a Candidate had inserted a needless
constitutional position.

The exact-result Candidate road is separate. It was added afterward. Its
current Book clause, runtime, and tests deliberately make every carried source
Assertion and every distinct ordered source-Assertion pair a required subject.
Its Applicability result then records `applicable` for every required subject.
There is no hidden recurrence or comparison determination inside that module.

Therefore:

```text
carried Measurement results
!=
immediate activation of the exact-result Candidate Cartesian road
```

The position-result reader refusal and the eager ordered-pair construction
remain real facts about that separate Candidate road. They are not the first
blockers in the ordinary corpus experiment because the tests do not establish
that road as the next consumer.

## 1. The recurrent-pair tests provide the first demonstrated narrowing

`tests/test_material_pair_investigation.py` begins with a larger material
population but admits only pair material already established as recurrent by
the exact pair Measurement.

The source reader in `scripts/material_pair_investigation.py` accepts only
Assertions satisfying all of these coordinates:

```text
result = recurrence
exact two-byte representation
exact count-Assertion support
exact pair-Measurement result occurrence
exact source occurrence population
exact completeness boundary
exact Locality
```

The next subject reader then requires at least two exact adjacent premise
occurrences of that same yielded pair. Mere adjacency does not pass.

`test_recurrence_not_adjacency_alone_warrants_one_pair_subject` proves the
boundary directly:

```text
material b"ab"
+ pair material b"ab"
→ no recurrent-pair subject

material b"abxxab"
+ recurrence Assertion for b"ab"
→ exact recurrent-pair subject with two premise occurrences
```

`test_recurrence_and_position_premise_of_pair_discriminate_fresh_material`
then takes that exact pair subject into another source occurrence. It records
the exact current occurrences and distinguishes the position relations that
match the premise from those that differ. The later source material is not
part of the premise source population.

The same refusal exists in the durable Measurement road.
`test_one_same_boundary_pair_subject_set_requires_exact_distinct_recurrence_subjects`
proves that
`measure_positions_for_recurrent_byte_pair_assertions(...)` accepts exact
recurrence Assertion references and refuses the supporting count Assertion as
the subject.

The subject population is therefore bounded by an already yielded
Measurement distinction:

```text
all adjacent positions available in exact material
↓ pair count Measurement
observed exact pair counts
↓ count > 1
recurrence Assertions
↓ exact recurrence reference and support
recurrent-pair subjects
```

No general Candidate enumeration performs that work.

## 2. Compare tests demonstrate nontrivial Applicability

The current `04.Compare.B` tests provide the clearest active witness that
Applicability is not a ceremonial `applicable` label.

`test_every_current_compare_assignment_records_one_separate_applicability_result`
creates two exact ordered-path results and two exact recorded-pair comparison
results. Current Standing therefore exposes four possible path/comparison
subjects.

The exact Applicability determination in
`comparison_of_ordered_relation_path_with_recorded_pair_findings.py` requires:

```text
every pair carried by the path has a matching pair finding
+
the path source occurrence is the comparison's added source occurrence
```

The four results are:

```text
applicable
inapplicable
inapplicable
applicable
```

`test_only_applicable_current_compare_results_record_participation_and_act_evidence`
then proves that only the two applicable subjects receive Participation and a
Compare Act occurrence. The two inapplicable results address no Act
occurrence. `test_another_source_occurrence_is_inapplicable_and_cannot_participate`
independently proves the same source-occurrence refusal.

This is the demonstrated distinction:

```text
possible subject position
↓ exact Applicability Act and result
applicable or inapplicable
↓ only when applicable
Participation
↓
Compare Act occurrence
```

## 3. The sixteen-Book material tests already contain the association wheel

The material-witness tests preserve a longer recursive road over the same
sixteen 300-line windows:

```text
exact Book material
↓ byte and byte-pair Measurements
exact observed byte and pair references
↓ compiled invocations
exact returned coordinates for each function
↓ Admission
groups of material carrying the same returned coordinates
↓ exact added-position Act occurrences
new exact results
↓ Compare
↓ later Admission and later Acts
```

That road does not begin from every Assertion in the ledger. It begins from
the exact measured byte and observed byte-pair references. Compiled invocation
results establish further exact distinctions, and Admission preserves the
groups sharing those returned coordinates. Later added-position Acts consume
the admitted result references.

The historical naming makes the correction especially direct. Commit
`952cce37` called the produced three-byte material `candidates`. Commit
`1ad72ef9` decomposed that noun into:

```text
exact source material reference
+ exact added material reference
+ exact position
↓ AddedPosition Act occurrence
exact result material
```

The current road retains the exact source references, Act occurrences,
results, compiled invocation distinctions, Admission, Compare, and recursive
later work. It does not require a Candidate wrapper for the material result.

The `measured_book_pairs` fixture currently stops through an explicit stale
Witness-Material refusal sentence, so this investigation does not claim the
whole fixture is live after the recent Witness Locality correction. Its tests
and runtime functions nevertheless preserve the demonstrated association
road, and its history explains the Candidate wording the operator recalled.

## 4. The exact-result Candidate road is different

Commit `c962a5c2` introduced unary Candidate Standing from every exact result
Assertion through a supplied ledger boundary. Its Applicability result was
already constructed as:

```python
"finding": "applicable"
```

Commit `07625cad` added the distinct ordered-pair Candidate Responsibility and
required every ordered source-Assertion pair except self-pairs.

The present replacement module preserves that decision:

```text
source Assertion references through B = N

unary required subjects        = N
ordered-pair required subjects = N × (N - 1)

every required subject
→ Applicability result = applicable
→ Participation
→ Candidate Act
→ Candidate result
```

`test_ordered_pair_responsibility_requires_each_distinct_ordered_pair` pins
the exact `N × (N - 1)` population and yields every member. The behavior is
therefore not an accidental loop introduced by the independent-result rewrite.
It is carried by active `01.Source.E.1`, machine grammar, runtime, and tests.

The exact-result Candidate road did not replace an internal discriminator.
It declared a different Responsibility whose required population was already
the complete unary and ordered-pair population. Its Applicability Act currently
has no work left except to restate that every predeclared required subject is
applicable.

Using that module as the automatic continuation after any Measurement result
would nevertheless bypass the narrower demonstrated association road.

## 5. Corpus scale through the demonstrated pair distinction

The exact 218,058-byte corpus contains:

| coordinate | population |
|---|---:|
| bytes | 218,058 |
| adjacent positions | 218,057 |
| observed exact two-byte values | 2,708 |
| observed exact two-byte values with count greater than 1 | 2,162 |

The first two counts are the live observation. The latter two were calculated
from the same byte-for-byte corpus value using the pair Measurement rule.

That gives the scale difference exposed by the tests:

```text
global exact-result Candidate source read
→ 218,984 source Assertion references
→ 47,953,773,272 ordered Candidate subjects

demonstrated pair road
→ 2,708 exact observed pair counts
→ 2,162 exact recurrence Assertions
→ recurrent-pair subjects and later exact comparisons
```

This comparison does not prove every recurrent pair must immediately proceed.
It proves that the repository already has an exact result distinction that
prevents raw position co-presence from becoming an all-Assertion Candidate
product.

## 6. Correct stopping boundary

Do not connect exact-result Candidate production to the console here.

Do not fix its position-result reader merely to make the corpus enter that
road. Do not make its ordered-pair construction lazy merely to stream the
forty-eight-billion population. Those changes would optimize a continuation
that the current experiment has not established.

The next live seam is earlier and narrower:

```text
ordinary !cat first acquisition
↓ exact-byte Measurement result
↓
operator console records no byte-pair Measurement when pair_premise is None
↓
STOP
```

The console already records the byte-pair Measurement after an earlier pair
premise exists, while focused tests record that Measurement directly from one
exact-byte Measurement and then admit only recurrence Assertions to the
recurrent-pair subject road.

The next question is therefore not how to activate Candidate. It is whether
the tested byte-pair Measurement Responsibility is readable at the first exact
material boundary, and why the live console currently conditions that
Measurement on an already carried pair premise belonging to a later Compare.

Preserve:

```text
pair Measurement
!= pair Compare

recurrence Assertion
!= Candidate

possible Compare subject
!= applicable Compare subject

carried result availability
!= immediate exact-result Candidate activation
```

## Validation

Focused current witnesses:

```text
tests/test_material_pair_investigation.py::
  test_recurrence_not_adjacency_alone_warrants_one_pair_subject

tests/test_material_pair_investigation.py::
  test_recurrence_and_position_premise_of_pair_discriminate_fresh_material

tests/test_candidate_results_from_exact_result_assertions.py::
  test_ordered_pair_responsibility_requires_each_distinct_ordered_pair

tests/test_comparison_of_ordered_relation_path_with_recorded_pair_findings.py::
  test_every_current_compare_assignment_records_one_separate_applicability_result

tests/test_comparison_of_ordered_relation_path_with_recorded_pair_findings.py::
  test_only_applicable_current_compare_results_record_participation_and_act_evidence

tests/test_comparison_of_ordered_relation_path_with_recorded_pair_findings.py::
  test_another_source_occurrence_is_inapplicable_and_cannot_participate
```

Result: `6 passed`.
