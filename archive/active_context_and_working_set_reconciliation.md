# Active Context And Working Set Reconciliation

## Purpose

Recent discussions exposed a distinction that appears increasingly important.

The distinction is:

```text
Knowledge
    ≠
Active Context
```

A system may possess a large amount of knowledge while only a small portion is relevant to the current situation.

## Observation

Human operators rarely carry all known information in active thought.

Instead they maintain a small working set.

Example:

```text
Leave for work.

Need keys.
Need badge.
Need lunch.
Need to take out trash.
```

The operator does not mentally load the entire house.

The operator maintains a checklist of what currently matters.

## Knowledge Versus Context

Knowledge answers:

```text
What is true?
```

Context answers:

```text
What is important right now?
```

These are related but distinct questions.

## Dynamic Context

Active context changes through observation.

Example:

```text
Leave for work.
        ↓
Observe full trash can.
        ↓
Trash becomes relevant.
        ↓
Take out trash.
        ↓
Remove from active context.
```

The working set is continuously updated.

## Candidate Working Set Model

```text
Current Goal

Current Object

Current Frontier

Recent Observations

Relevant Guardrails

Open Tasks
```

This working set is much smaller than total repository knowledge.

## Relationship To Applicability

The Finding Applicability Index asks:

```text
When is a finding useful?
```

Active context asks:

```text
Which useful findings belong in the working set right now?
```

Applicability and context are therefore complementary.

## Relationship To Context Anchor Drift

A recurring failure mode is:

```text
Active object changes.
```

Example:

```text
Seed
        ↓
Host
```

The answer may remain technically correct while no longer serving the current objective.

Maintaining active context helps prevent this drift.

## Relationship To Supported Ground

Supported ground recognition helps determine:

```text
What conclusions are justified?
```

Active context helps determine:

```text
What information should currently influence decisions?
```

## Why This Matters

Many systems are optimized around memory.

However useful behavior often depends more on maintaining the correct working set.

A system with extensive knowledge may still perform poorly if the wrong information is active.

## Non-Goals

This finding does not replace:

```text
Memory
Knowledge acquisition
Evidence storage
```

Instead it focuses on selecting the subset of information that currently matters.

## Current Conclusion

A useful system requires more than knowledge.

It requires a mechanism for maintaining an active checklist.

One possible framing is:

```text
Knowledge tells the system what is true.

Context tells the system what matters right now.
```

Many recent findings can be interpreted as attempts to improve management of that active working set.
