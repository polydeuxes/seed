# Evidence Strength And Claim Strength Reconciliation

## Purpose

Recent reconciliation work repeatedly exposed the same failure pattern.

The pattern is not necessarily missing evidence.

It is often a mismatch between:

```text
Evidence Strength
```

and:

```text
Claim Strength
```

## Central Finding

A claim may be technically related to available evidence while still exceeding what that evidence justifies.

A useful question is therefore:

```text
Does the strength of the claim match the strength of the support?
```

## Examples

### Relationship Evidence

Evidence:

```text
Import relationship observed.
```

Supported claim:

```text
X imports Y.
```

Escalated claim:

```text
X calls Y.
X owns Y.
X depends on Y behaviorally.
```

The additional claim strength is not supported by the available evidence.

### Behavioral Evidence

Evidence:

```text
Behavior observed.
```

Supported claim:

```text
Behavior exists.
```

Escalated claim:

```text
Ownership proven.
```

Ownership requires additional evidence.

### Capability Evidence

Evidence:

```text
Capability A exists.
Capability B exists.
```

Supported claim:

```text
A exists.
B exists.
```

Escalated claim:

```text
A and B compose.
```

A bridge may be required.

### Visibility Evidence

Evidence:

```text
Partial artifact visible.
```

Supported claim:

```text
Visible portion understood.
```

Escalated claim:

```text
Whole artifact replacement justified.
```

## Claim Escalation

A recurring pattern is:

```text
Evidence
        ↓
Supported Claim
        ↓
Additional Inference
        ↓
Stronger Claim
```

The strongest claim is not always justified.

## Relationship To Supported Ground

Supported ground recognition asks:

```text
Am I leaving supported ground?
```

Evidence strength and claim strength asks:

```text
Has the claim become stronger than the support?
```

The findings are closely related.

## Candidate Warning Signals

Examples:

```text
Claim scope expands.

Evidence type changes.

Inference chain length increases.

Ownership appears.

Authority appears.

Behavior appears without behavior evidence.
```

These signals suggest potential claim escalation.

## Non-Goals

This finding does not prohibit inference.

Reasoning remains useful.

The goal is proportionality between support and conclusion.

## Current Conclusion

A useful architectural guardrail is:

```text
Claim strength should not exceed evidence strength without explicitly acknowledging the gap.
```

Many unsupported conclusions can be understood as claim escalation beyond available support.
