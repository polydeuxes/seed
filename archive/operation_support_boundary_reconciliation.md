# Operation Support Boundary Reconciliation

## Purpose

Recent operator interactions exposed a recurring pattern.

Many failures were not caused by missing reasoning.

They were caused by missing support for the requested operation.

## Observation

A request may appear simple:

```text
Upload a file.
Generate commands.
Modify a document.
Answer a question.
```

However the operation may require prerequisites that are not currently available.

## Candidate Support Model

```text
Operation Request
        ↓
Active Object
        ↓
Required Evidence
        ↓
Available Evidence
        ↓
Capability Path
        ↓
Visibility Scope
        ↓
Risk / Approval
        ↓
Action or Refusal
```

## Active Object

The system should remain attached to the operator's active object.

Example:

```text
Exercise Seed.
```

is not equivalent to:

```text
Exercise the host operating system.
```

Changing the active object can produce technically correct but contextually incorrect answers.

## Evidence Sufficiency

A capability may exist while evidence remains insufficient.

Example:

```text
File replacement requested.
```

If the complete artifact is not visible, whole-file replacement may not be justified.

## Visibility Scope

Observed scope and requested scope may differ.

Example:

```text
Partial artifact visible.
Whole artifact replacement requested.
```

The operation exceeds available visibility.

## Capability Bridges

Two capabilities may exist independently.

```text
Capability A
Capability B
```

The required bridge between them may be absent.

The resulting failure is not necessarily a missing capability.

It may be a missing transfer path.

## Risk Acceptance

Operator risk acceptance does not create missing evidence.

```text
Risk accepted
```

is distinct from:

```text
Evidence sufficient
```

The two should not be conflated.

## Failure Pattern

Observed failure pattern:

```text
Missing support
        ↓
Reason harder
        ↓
Answer adjacent problem
```

Preferred pattern:

```text
Missing support
        ↓
Identify missing element
        ↓
Surface limitation
        ↓
Bridge or refuse
```

## Current Conclusion

A useful question is not merely:

```text
Can the system perform this operation?
```

but:

```text
Is the operation supported by the evidence,
visibility, bridges, and context currently available?
```
