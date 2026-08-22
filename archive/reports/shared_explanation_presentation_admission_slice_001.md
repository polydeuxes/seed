# Shared Explanation Presentation Admission Slice 001

This slice adds one bounded read-only responsibility:

```text
SharedExplanationMembershipEvidenceSet
+
one explicit requested-presentation boundary
+
explicit presentation-local admission evidence
->
SharedExplanationPresentationAdmission
```

The implementation admits only already-`belongs` membership evidence results to later
presentation sequencing for the requested presentation. Belonging to the inquiry remains
distinct from admission to this presentation: a belonging result may remain unadmitted
with a preserved non-admission reason without becoming `does_not_belong`.

The slice intentionally does not sequence, rank, deduplicate, compose a view, reinterpret
membership, invent missing projections, authorize, execute, write events, or mutate
cluster state. `admitted_to_sequencing` is an admission marker for a later sequencing
responsibility and is not equivalent to first encounter order.

Implementation evidence:

- `seed_runtime/shared_explanation_presentation_admission.py` defines
  `RequestedPresentationBoundary`, `PresentationAdmissionEvidence`, and
  `SharedExplanationPresentationAdmission`.
- `admit_shared_explanation_presentation(...)` enforces one evidence-set inquiry/demand,
  one requested presentation boundary, and presentation-matched admission evidence.
- Focused tests in `tests/test_shared_explanation_presentation_admission.py` prove
  presentation-local admission, preserved non-admission reasons, unchanged membership
  partitions, visible Unknown/conflict/duplicate occurrences, and absence of sequencing
  or composition.
