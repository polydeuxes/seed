# Supported Ground Recognition Reconciliation

## Purpose

This document captures a recurring architectural finding.

The finding is not primarily about evidence acquisition.

It is about recognizing the boundary of justified conclusions.

## Central Question

A common question is:

```text
What does the system know?
```

A more useful question may be:

```text
What is currently justified?
```

These are not equivalent.

## Observation

A system may possess information, capabilities, observations, or partial evidence.

The existence of those elements does not automatically justify stronger conclusions.

## Examples

### Relationship Evidence

Supported:

```text
Import relationship observed.
```

Unsupported:

```text
Behavior proven.
Ownership proven.
```

### Capability Evidence

Supported:

```text
Capability A exists.
Capability B exists.
```

Unsupported:

```text
Capability bridge exists.
```

### Visibility Evidence

Supported:

```text
Partial artifact visible.
```

Unsupported:

```text
Whole artifact replacement justified.
```

### Context Evidence

Supported:

```text
Current discussion concerns Seed.
```

Unsupported:

```text
Host-level answers satisfy the request.
```

## Leaving Supported Ground

A recurring failure mode is:

```text
Supported observation
        ↓
Additional inference
        ↓
Unsupported conclusion
```

The transition often occurs gradually.

The system may not explicitly recognize that it has crossed a boundary.

## Candidate Warning Signals

Potential indicators include:

```text
Inference chain length increases.

Claim strength increases.

Evidence type changes.

Requested scope exceeds visible scope.

A capability bridge is assumed.

The active object changes.
```

These signals do not necessarily indicate error.

They indicate increased distance from directly supported evidence.

## Relationship To Boundary Preservation

Boundary preservation focuses on maintaining distinctions.

Supported ground recognition focuses on recognizing when those distinctions are being crossed.

The two findings are complementary.

## Relationship To Evidence Architecture

Evidence architecture answers:

```text
How does Seed know something?
```

Supported ground recognition answers:

```text
How does Seed recognize that it is moving beyond what its evidence currently supports?
```

## Non-Goals

This finding does not imply:

```text
Avoid inference.
Avoid reasoning.
Avoid synthesis.
```

The goal is not elimination of reasoning.

The goal is awareness of support boundaries.

## Current Conclusion

One of the most useful future capabilities may be:

```text
Recognize when a conclusion is leaving supported ground.
```

A system that can identify the edge of its support may avoid many forms of unsupported reasoning without requiring additional intelligence.
