# Goal Consideration Candidate Resolution Slice 001

## Boundary

```text
GoalOrientationInventory
+
attributed candidate testimony naming a goal_establishment_id
→ GoalConsiderationCandidateResolution
```

This boundary compares attributed testimony with one visible bounded-goal inventory snapshot. It can establish that the testimony resolves to exactly one visible goal identity.

It does not select that goal, determine that the goal should receive present consideration, establish priority, originate advancement, classify a need, or open inquiry.

## Resolved state

A candidate identity resolves only when:

- the testimony names one exact `goal_establishment_id`;
- all exact testimony agrees on that identity;
- exactly one visible bounded-goal record carries that identity.

The result preserves the candidate-set fingerprint, testimony and source references, the resolved goal identity and source, all visible candidates, Unknowns, and conflicts.

## Preserved unresolved states

- no candidate testimony;
- missing identity;
- ambiguity;
- conflict;
- inventory mismatch.

Pressure records and Null dimensions do not become bounded-goal candidates.

## Negative authority

```text
candidate identity resolved
!= Seed-owned goal selection
!= constitutional focus
!= priority
!= advancement
!= inquiry applicability
```

The bounded advancement horizon may consume the resolved identity to check that its supplied goal artifact is the same artifact. That consumption does not strengthen candidate resolution into selection standing.
