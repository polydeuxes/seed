# Execution Status And Operator Feedback Reconciliation

## Purpose

This reconciliation defines the architectural boundary between execution status, operator feedback, observations, evidence, claims, projections, and knowledge.

The motivating event was an operator running:

```text
seed --observe-local-host
```

with no visible feedback for an extended period. The operator could not determine whether Seed was:

- collecting observations;
- writing events;
- projecting state;
- stalled;
- or completed.

The operator interrupted execution during event persistence.

The question is not how the CLI should display progress.

The question is:

```text
How should Seed communicate work-in-progress?
```

across CLI, UI, API, notifications, and future audio interfaces.

## Central Finding

Execution visibility is a first-class architectural concern.

The correct abstraction is not:

```text
CLI progress
```

The correct abstraction is:

```text
Execution Status
        ↓
Operator Feedback
```

Different interfaces may render the same execution status differently.

## Core Distinctions

Execution Status answers:

```text
What work is currently occurring?
```

Operator Feedback answers:

```text
What should be communicated to the operator about that work?
```

These are distinct from:

```text
Observation
Evidence
Claim
Fact
Relationship
Projection
Audit
History
Knowledge
```

## What Execution Status Is Not

Execution status is not:

```text
an observation
an evidence record
an event ledger fact
an audit trail
knowledge
proof
state summary
projection authority
```

Execution status exists to communicate activity, not truth.

## Architectural Shape

Preferred architecture:

```text
Execution
        ↓
Execution Status
        ↓
Operator Feedback
        ↓
Renderer
```

Example renderers:

```text
CLI
Audio
Web UI
Mobile UI
Notifications
```

## Renderer Independence

The same status should be renderable as:

CLI:

```text
Writing observations 100/243
```

Audio:

```text
Still working. Writing observations.
```

UI:

```text
[########----] 100/243
```

Therefore:

```text
Feedback Renderer
        !=
Execution Status
```

## Execution Phases

Execution status may describe phases such as:

```text
Collecting Observations
Importing Claims
Reconciling
Projecting
Persisting
Capability Inventory
Verification
Execution
```

These are execution activities.

They are not facts.

## Progress

Progress is a possible property of execution status.

Examples:

```text
phase
current
completed
remaining
estimated_total
rate
start_time
elapsed
```

Progress is optional.

Execution status may exist even when progress cannot be calculated.

## Availability, Consumption, Activation Analogy

Previous reconciliations established:

```text
Handoff Available
    != Handoff Consumed
    != Handoff Activated
    != Handoff Compliance
```

Execution visibility follows a similar pattern:

```text
Work Exists
    != Status Exists
    != Feedback Rendered
    != Operator Acknowledged
```

The presence of work does not imply the operator can see it.

## Relationship To Knowledge

Execution status should not be promoted into knowledge.

Examples:

```text
Collecting packages...
```

is not a package fact.

```text
Writing observations...
```

is not evidence.

```text
Reconciling state...
```

is not a reconciliation result.

Execution status communicates activity.

Knowledge communicates preserved understanding.

## Relationship To Auditing

Execution status may support debugging.

Execution status is not itself an audit.

Audits explain:

```text
what happened
why it happened
what was discovered
```

Execution status explains:

```text
what is happening right now
```

## Audio Implications

Future audio interfaces should not implement independent progress logic.

Audio should consume execution status.

Examples:

```text
Collecting local host observations.
```

```text
Still working.
```

```text
Observation collection completed.
```

Audio therefore becomes a renderer.

Not a source of execution state.

## API Implications

Future APIs should expose execution status independently from projections.

The operator should not need to inspect state summaries to determine whether work is running.

## CLI Implications

CLI output should be a rendering of execution status.

The CLI should not need custom logic for every execution path.

## Architectural Invariants

```text
Execution Status != Observation
Execution Status != Evidence
Execution Status != Claim
Execution Status != Fact
Execution Status != Projection
Execution Status != Audit
Execution Status != Knowledge

Renderer != Status
Audio != Status
CLI != Status
UI != Status

Work Exists != Feedback Visible
Progress != Truth
Status != Authority
```

## Non-Goals

This reconciliation does not:

- prescribe a status schema;
- prescribe a transport;
- prescribe a renderer;
- prescribe CLI implementation;
- prescribe audio implementation;
- prescribe UI implementation;
- modify runtime behavior.

## Final Finding

Seed should model execution visibility through execution status rather than interface-specific progress reporting.

Execution status is a renderer-independent representation of ongoing work.

CLI, UI, notifications, and future audio interfaces should consume the same execution status and render it appropriately.

This preserves the boundary between activity and knowledge while allowing operators to understand what Seed is doing without coupling visibility to any specific interface.
