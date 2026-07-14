# Examination Method Applicability Projection Slice 001

## 1. Recovered responsibility
Recovered exactly one responsibility: project whether each existing technically compatible candidate examination work item has supplied methodology evidence establishing `applicable`, `inapplicable`, `unknown`, or `conflict`, and preserve fidelity, attribution, and claim-treatment constraints with that determination.

## 2. Producer
`project_examination_method_applicability(...)` is the producer.

## 3. Input artifacts
Inputs are the existing `BoundedConstitutionalQuestion`, existing `CandidateExaminationWorkSet`, and caller-supplied `ExaminationMethodApplicabilityTestimony` records.

## 4. Methodology-evidence convention
The testimony convention is narrow and explicit: inquiry reference, candidate or contract reference, artifact identity/hash reference, opaque method reference, applicability testimony, fidelity constraints, attribution constraints, claim-treatment constraints, supporting references, contradicting references, and unknowns.

## 5. Output artifact
The output is immutable read-only `ExaminationMethodApplicabilityProjection` with per-candidate applicability records, state buckets, projection unknowns, boundary notes, and read-only flags.

## 6. Applicability identity and ordering
Projection identity is deterministic over the bounded inquiry id, candidate-work-set id, convention, and ordered records. Candidate applicability records are ordered by `candidate_work_id`.

## 7. Applicable rule
A record is applicable only when matching testimony references the same inquiry, the same candidate or contract, and the same artifact version where supplied, explicitly states `applicable`, preserves constraints, and has no unresolved contradiction.

## 8. Inapplicable rule
A record is inapplicable only when explicit matching testimony states `inapplicable`. Capability unavailability, missing representation, provider authorization absence, and inactivity do not imply inapplicability.

## 9. Unknown rule
A record is Unknown when testimony is absent, mismatched, incomplete, or explicitly Unknown. Technical compatibility alone yields Unknown.

## 10. Conflict rule
A record is conflict when matching testimony supplies incompatible applicability states, incompatible required constraint sets, or contradicting references. Conflict records are also included in the Unknown bucket for handoff exclusion.

## 11. Fidelity treatment
Fidelity requirements remain tuple constraints on the candidate applicability record. They are not priority scores, separate work items, selected-work markers, or semantic conclusions.

## 12. Attribution treatment
Attribution requirements remain attached to the candidate applicability record. External/provider attribution does not authorize provider invocation.

## 13. Claim-treatment constraints
Claim-treatment constraints are preserved as explicit strings such as no promotion to Evidence or Fact and provider authorization remaining downstream.

## 14. Technical-compatibility distinction
`CandidateExaminationWorkSet` continues to own technical and representation compatibility. Method applicability is a separate projection over those existing candidate identities.

## 15. Frontier handoff
`ExaminationMethodApplicabilityProjection.to_frontier_candidate_work(...)` is the narrow handoff. It forwards only candidates that are both methodologically applicable and technically compatible to existing `ExaminationFrontier` classification.

## 16. Treatment of non-applicable alternatives
Inapplicable, Unknown, and conflict candidates remain preserved in the applicability artifact and are not forwarded as ordinary handoff work.

## 17. Mechanical structural proving result
Focused tests prove a compatible structural candidate plus explicit mechanical-method/fidelity testimony becomes applicable without claiming semantic understanding.

## 18. Surface-feature proving result
Focused tests include surface-feature compatible candidates and preserve structural-input/fidelity conventions without selecting or executing work.

## 19. External grammar decision
No universal internal/external grammar taxonomy was introduced. External-method applicability can be testified by opaque method key and can require attribution, exact span binding, alternatives/contradiction preservation, no Fact promotion, and downstream provider authorization.

## 20. Caller-supplied methodology evidence
Methodology evidence is caller supplied. Seed validates references and deterministically projects states; it does not discover methods or infer semantic applicability.

## 21. Seed-owned projection responsibility
Seed owns only deterministic projection from explicit inquiry + existing candidate work + explicit methodology testimony.

## 22. Manual handoff eliminated
The handoff no longer relies on a human manually remembering to remove Unknown or inapplicable method candidates before frontier classification.

## 23. Read-only guarantees
Projection and rendering are read-only: `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`. Tests check that no pending actions, provider/tool invocations, observations, runtime facts, selected work, or mutations are created.

## 24. Compatibility answer
Did this slice change any existing compatibility boundary? No.

## 25. Files changed
- `seed_runtime/examination_method_applicability.py`
- `tests/test_examination_method_applicability.py`
- `examination_method_applicability_projection_slice_001.md`

## 26. LOC delta
The final LOC delta is reported by `git diff --stat` and `git diff --numstat` before commit.

## 27. Tests executed
- `pytest -q tests/test_examination_method_applicability.py`
- `pytest -q tests/test_candidate_examination_work.py tests/test_examination_frontier.py tests/test_constitutional_view_selection.py tests/test_candidate_external_grammar.py`

## 28. Remaining missing roads
Leave unresolved:

```text
bounded inquiry
+
methodological applicability
+
ExaminationFrontier
→ examination-policy projection
```

```text
examination policy
+
eligible frontier work
→ selected work and preserved alternatives
```

```text
selected work
→ bounded probe request
```

```text
probe request
→ policy authorization
→ execution
```

```text
result
→ frontier revision
```

## 29. Exact next bounded question
Given an `ExaminationFrontier` whose candidate work is both technically compatible and methodologically applicable, what explicit examination resolution or policy governs lawful movement among its eligible work items without yet selecting one?
