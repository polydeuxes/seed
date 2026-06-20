# Pressure Audit Design Audit

## Status

Exploratory design audit.

This document captures an operational pressure discovered after adding multiple visibility and memory surfaces. It does not implement a pressure audit, create ontology, write facts, or change operational behavior.

Repository authority wins over this audit.

## Problem

Seed now has several useful visibility surfaces:

```text
observation inventory
observation utilization
consumer audit
diagnostic inventory
diagnostic shape audit
ownership discrepancies
capability needs
knowledge reachability
audit snapshots
audit compare
ops brief
```

These reduce the need to inspect source code manually.

However, the operator still has to decide which surfaced pressure matters most.

Current burden:

```text
read ops brief
read ownership discrepancies
read orphaned predicate list
read fragile predicate list
read capability needs
read shape audit
mentally rank what matters next
choose next implementation target
```

The system can now summarize pressures, but the prioritization burden still mostly lives in the operator.

## Observed examples

Recent `seed --ops-brief` output showed:

```text
Service ambiguities: 19
Orphaned predicates: 27
Fragile predicates: 7
Shape mismatches: 0
Top capability needs: none
```

The brief correctly summarized the state, but the operator still had to ask:

```text
Should we fix service ownership attribution?
Should we investigate orphaned predicates?
Should we address fragile predicates?
Should we build another observation?
```

Earlier examples showed similar burden:

- Candidate-kind noise in reachability required manual priority judgment.
- Ownership discrepancies exposed missing observations, but the operator chose which observation to add.
- Consumer audit exposed orphaned predicates, but the operator had to decide whether they were false or true orphans.
- Audit snapshots exposed changes, but the operator chose whether the change mattered.

## Design pressure

Seed needs a surface that ranks operational pressure using existing evidence.

This should not be autonomous planning.

The goal is not:

```text
Seed decides what to do and does it.
```

The goal is:

```text
Seed ranks current pressures and explains the evidence behind the ranking.
```

## Proposed surface

Potential command:

```bash
seed --pressure-audit
seed --pressure-audit --json
```

The pressure audit would aggregate existing surfaces and produce a ranked list.

Example output:

```text
Pressure Audit

1. Service ownership attribution
   Score: 19
   Evidence:
     service ambiguity rows: 19
     dominant conflict: owner_not_observed
   Suggested next inspection:
     seed --ownership-discrepancies

2. Orphaned observation predicates
   Score: 27
   Evidence:
     consumer audit orphaned predicates: 27
   Suggested next inspection:
     seed --consumer-audit --json

3. Fragile observation predicates
   Score: 7
   Evidence:
     single-consumer predicates: 7
   Suggested next inspection:
     seed --consumer-audit
```

## Relationship to ops brief

`seed --ops-brief` summarizes.

`seed --pressure-audit` should prioritize.

```text
ops brief
  answers:
    what is the current operational situation?

pressure audit
  answers:
    which pressure should be looked at first, and why?
```

The pressure audit may consume the same underlying data as ops brief, but the output should be ranking-oriented.

## Candidate inputs

Initial implementation could consume:

```text
ownership discrepancies
capability needs
consumer audit
observation utilization
diagnostic shape audit
audit snapshots / latest compare metadata
```

No new observations should be required.

No facts should be written.

No cluster mutation should occur.

## Candidate pressure categories

### Diagnostic shape pressure

High priority when mismatches are present because visibility contract drift undermines trust in other outputs.

Evidence:

```text
diagnostic shape mismatch count
warnings
unknowns
```

### Ownership pressure

High priority when ownership discrepancies contain many unresolved ambiguity rows.

Evidence:

```text
owner_not_observed
multiple_candidate_owners
consumer_mistaken_as_owner
mount_source_conflict
insufficient_evidence
```

### Capability pressure

High priority when many diagnostic rows request the same capability.

Evidence:

```text
capability need frequency
affected subjects
affected diagnostics
```

### Observation dead-zone pressure

High priority when collected observations have no implementation consumers.

Evidence:

```text
orphaned predicates
unused predicates
collected-only predicates
```

### Fragility pressure

Medium priority when important observations have only one implementation consumer.

Evidence:

```text
single-consumer predicates
widely used predicates
consumer counts
```

### Snapshot/change pressure

Useful when the latest snapshot comparison shows significant added/removed predicates or changed ownership rows.

Evidence:

```text
latest comparison availability
added rows
removed rows
changed conflicts
changed capability needs
```

## Scoring expectations

A simple score is enough for V1.

Possible scoring inputs:

```text
shape mismatches: high weight
ownership ambiguity rows: medium/high weight
capability need frequency: medium/high weight
orphaned predicates: medium weight
fragile predicates: lower weight
snapshot changes: contextual weight
```

The audit should expose the evidence and score components so the operator can disagree.

Avoid opaque ranking.

## Boundary

The pressure audit is operational triage.

It is not:

```text
autonomous planning
a task scheduler
a mutation engine
a fact generator
a replacement for diagnostics
```

It should read existing surfaces and produce a ranked pressure list.

## Relationship to operational memory

Audit snapshots preserve what happened.

Pressure audit ranks what currently needs attention.

These can complement each other:

```text
snapshot compare
  says what changed

pressure audit
  says whether that change creates pressure
```

A future version may use recent comparisons to raise or lower pressure.

## Initial implementation suggestion

A conservative first implementation should:

1. Run or reuse existing read-only surfaces.
2. Build pressure items from their summaries.
3. Rank by simple transparent scores.
4. Render human and JSON output.
5. Register the surface in diagnostic inventory and shape audit.
6. Add tests proving recommendations are evidence-backed.

Good V1 categories:

```text
diagnostic_shape
ownership
capability_needs
orphaned_predicates
fragile_predicates
```

Defer trend-aware pressure until audit snapshots have been used more.

## Non-goals

Do not use this audit to:

```text
execute fixes
open PRs
write facts
record diagnostic facts
create new ontology
invent new observation capabilities
replace ops brief
```

## Acceptance shape for future work

A future implementation should allow:

```bash
seed --pressure-audit
```

and produce a ranked, evidence-backed list of current operational pressures.

The operator should be able to answer:

```text
What should I inspect first?
Why is it ranked first?
Which existing command should I run next?
What evidence supports this priority?
```

without manually merging the outputs of every visibility surface.

## Current conclusion

The next burden to unload is prioritization.

Seed can increasingly see its own operational state. It should now begin ranking operational pressure from those visibility surfaces, while remaining read-only and non-autonomous.