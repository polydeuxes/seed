# Goal Inquiry Consideration Selection Slice 001

This slice adds one read-only `GoalInquiryConsiderationSelection` boundary.

## Boundary

```text
GoalOrientationInventory
+
GoalFocusEvidence(exact goal_establishment_id)
-> GoalInquiryConsiderationSelection
```

The owner consumes only explicit focus evidence that names exact bounded-goal identities. It does not resolve prose, labels, dimension names, topic similarity, pressure records, or inventory uniqueness.

## Lawful selected state

A selection is produced only when exactly one visible `bounded_goal` candidate in the inventory has the named `goal_establishment_id`. The result preserves:

- the visible inventory candidate-set fingerprint;
- focus evidence references;
- focus provenance references;
- the selected goal identity and source reference;
- every non-selected visible goal unchanged.

## Preserved non-selected states

The implementation preserves, without repair:

- no focus evidence;
- missing goal identity;
- ambiguity;
- conflicting exact identities;
- inventory mismatch when a named identity is not a visible bounded-goal candidate.

`Null` dimensions and pressure records are not selectable bounded goals in this boundary.

## Non-authority

`GoalInquiryConsiderationSelection` is read-only. It does not prioritize, activate goals, require inquiry, open inquiry, move a frontier, authorize work, start execution, start recording, write the event ledger, or mutate the cluster.

Goal inquiry consideration selection slice complete.
