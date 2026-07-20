# Operator Investigation Workflow Reconciliation

## Purpose

Recent operator sessions exposed a recurring pain point.

The pain is often described as:

```text
What command should I run?
```

However deeper review suggests that this is not the actual architectural problem.

The command is only the current mechanism.

The underlying problem is:

```text
An operator notices a concern.

How do they know what evidence to gather next?
```

This document reconciles that distinction.

## Central Finding

Operators do not fundamentally need commands.

Operators need a reliable path from:

```text
Observed concern
        ↓
Required evidence
        ↓
Supported conclusion
```

The command is merely one possible transport mechanism.

## Observation

Many recent audits followed the same structure.

Examples:

```text
Current Facts ambiguity
Impact verbosity
State Summary overlap
Authority confusion
Navigation confusion
```

The workflow repeatedly became:

```text
Observe anomaly
        ↓
Determine needed evidence
        ↓
Gather evidence
        ↓
Compare surfaces
        ↓
Identify boundary
        ↓
Determine smallest correction
```

The specific commands varied.

The investigation pattern remained stable.

## Important Distinction

```text
Investigation Workflow
        ≠
Current Command Set
```

Commands may change.

Interfaces may change.

The workflow remains useful.

Example:

Today:

```text
Impact seems confusing
        ↓
Run State Summary
Run Impact
Run Current Facts
        ↓
Compare outputs
```

Future:

```text
Impact seems confusing
        ↓
Open overview inspector
Open drilldown
Open evidence view
        ↓
Compare outputs
```

The workflow survives even if the commands disappear.

## Relationship To Operator Pain

Operator Pain As Frontier Signal asks:

```text
What hurts right now?
```

Repeated sessions revealed:

```text
Need evidence.
Need the next inspection step.
Need the next audit.
Need the right command.
```

These requests appeared repeatedly.

This suggests a missing investigation capability rather than a reasoning deficiency.

## Relationship To Evidence Before Capability

The canonical pathway is:

```text
InputEnvelope
        ↓
InputAct
        ↓
Evidence
        ↓
Capability Selection
        ↓
Capability
        ↓
Response
```

Investigation workflow is therefore naturally evidence-oriented.

The goal is not:

```text
Which capability should run?
```

The goal is:

```text
What evidence is required
before capability selection is justified?
```

## Investigation Versus Diagnosis

Another useful distinction:

```text
Investigation
        ≠
Diagnosis
```

Diagnosis attempts to explain a problem.

Investigation attempts to determine:

```text
What evidence is needed?
```

Investigation therefore precedes diagnosis.

## Candidate Generic Workflow

Many successful audits appear to fit:

```text
Observe concern
        ↓
Identify active object
        ↓
Identify affected surface
        ↓
Determine required evidence
        ↓
Gather evidence
        ↓
Compare evidence and interpretation
        ↓
Locate boundary issue
        ↓
Determine smallest justified correction
```

This workflow is intentionally independent of implementation.

## Evidence Requirements

An investigation should be framed in terms of evidence needs.

Not command needs.

Example:

### Surface Confusion

Evidence required:

```text
Overview surface
Drilldown surface
Evidence surface
```

Current mechanism:

```text
State Summary
Impact
Current Facts
```

### Integrity Concern

Evidence required:

```text
Integrity summary
Affected facts
Supporting evidence
```

Current mechanism:

```text
Integrity Summary
Fact Support
```

### Capability Gap

Evidence required:

```text
Operator request
Available capability
Missing capability
```

Current mechanism may change.

The evidence requirement remains.

## Relationship To Active Context

The investigation workflow depends heavily on maintaining the correct working set.

Important items include:

```text
Current goal
Current object
Current concern
Recent observations
Relevant guardrails
Open questions
```

Without these anchors the investigation can drift.

Example:

```text
Seed concern
        ↓
Host concern
```

The answer may remain technically correct while addressing the wrong object.

## Relationship To Boundary Preservation

Many investigations eventually discover:

```text
Two things were treated as equivalent.
```

Examples:

```text
Evidence
        ≠
Interpretation

Overview
        ≠
Drilldown

Capability
        ≠
Evidence

Source
        ≠
Authority
```

Investigation therefore frequently becomes boundary identification.

## Relationship To Navigation

Operator Navigation asks:

```text
I am on a surface.
Where should I go next?
```

Investigation asks:

```text
I observed a concern.
What evidence do I need?
```

Navigation may support investigation.

The two concepts remain distinct.

## Future Capability Direction

A future system might support investigations through:

```text
CLI guidance
Interactive workflows
Investigation assistants
Automatic evidence collection
Guided audits
```

These are implementation possibilities.

They are not the architectural finding.

## Non-Goals

This document does not require:

```text
New commands
New CLI arguments
New read models
New evidence types
Immediate implementation
```

It does not claim current commands are incorrect.

It does not define a final operator interface.

## Current Conclusion

The recurring operator request:

```text
What command should I run?
```

appears to be a symptom.

The deeper requirement is:

```text
How do I move from observed concern
to the evidence required for a supported conclusion?
```

Commands, interfaces, and tooling may change.

The investigation workflow remains applicable.

The durable architectural concern is therefore:

```text
Evidence-guided investigation.
```

rather than:

```text
Command generation.
```
