# Execution Status Emission And Consumption Reconciliation

## Purpose

This reconciliation continues the work from:

- execution_status_and_operator_feedback_reconciliation.md

The prior reconciliation established:

```text
Execution
        ↓
Execution Status
        ↓
Operator Feedback
        ↓
Renderer
```

This reconciliation investigates a deeper question:

```text
Where does execution status come from?

Who emits it?

Who consumes it?
```

## Central Finding

Execution status should be emitted by work-producing boundaries and consumed by interested observers.

The architecture should not be:

```text
CLI asks execution what is happening
```

nor:

```text
Audio asks execution what is happening
```

The architecture should be:

```text
Execution
        ↓
Status Emission
        ↓
Status Stream
        ↓
Status Consumers
        ↓
Renderers
```

## The Producer Boundary

Execution status originates where work occurs.

Examples:

```text
Observation Collection
Claim Import
Reconciliation
Projection
Verification
Execution
Federation
```

These activities are uniquely positioned to know:

```text
phase
start
completion
failure
partial progress
```

Therefore:

```text
Renderer
    !=
Status Producer
```

## The Consumer Boundary

Consumers observe execution status.

Consumers do not create execution status.

Examples:

```text
CLI
Audio
Web UI
Mobile UI
Notifications
Future Agents
```

A consumer may:

```text
display
summarize
announce
ignore
aggregate
```

without altering the underlying execution state.

## Why Direct Renderer Coupling Fails

If execution is coupled directly to CLI:

```text
Execution
        ↓
print()
```

then:

```text
Audio cannot reuse it.
UI cannot reuse it.
Notifications cannot reuse it.
```

The execution layer becomes presentation-aware.

This violates established boundaries.

## Status Events

A useful shape is:

```text
Execution Activity
        ↓
Status Event
```

Examples:

```text
phase_started
phase_completed
phase_failed
progress_updated
waiting
```

These are not knowledge events.

They are activity visibility events.

## Status Events Are Not Ledger Events

A critical distinction:

```text
Execution Status Event
        !=
Knowledge/Event Ledger Event
```

Ledger events preserve historical knowledge.

Execution status preserves current activity visibility.

Therefore execution status should not automatically enter:

```text
observation history
knowledge history
fact history
relationship history
```

unless a separate audit or operational history capability explicitly requires it.

## Ephemeral By Default

Execution status is naturally ephemeral.

Examples:

```text
Writing observations 100/243
```

becomes irrelevant once execution completes.

The architecture should assume:

```text
Status
    is transient by default
```

and only persist it when a separate requirement exists.

## Relationship To Handoffs

Execution status resembles handoff working-state information.

However:

```text
Execution Status
    explains active work

Working State
    explains continuation context
```

These should not collapse.

## Relationship To Observations

Execution status should not become an observation source.

Examples:

```text
Collecting packages...
```

is not package evidence.

```text
Reading /etc/hosts...
```

is not hosts-file evidence.

The distinction remains:

```text
Activity
    !=
Observed Reality
```

## Relationship To Audio

Future audio support was a motivating factor.

Audio should consume status.

Examples:

```text
Still working.
```

```text
Collecting local host observations.
```

```text
Observation collection completed.
```

Audio should not implement independent progress tracking.

## Relationship To Federation

Federated execution may emit status.

Examples:

```text
Remote Seed importing claims.
Remote Seed reconciling.
Remote Seed projecting.
```

Status provenance should remain preserved.

Consumers should know:

```text
which execution source emitted the status
```

without promoting status into knowledge.

## Architectural Invariants

```text
Execution Status != Observation
Execution Status != Evidence
Execution Status != Claim
Execution Status != Fact
Execution Status != Projection
Execution Status != Knowledge

Status Producer != Status Consumer
Renderer != Producer
Renderer != Execution

Activity != Reality
Status != Authority
Status != Proof

Status Stream != Ledger
Status Event != Ledger Event
```

## Implementation Implications

If implementation occurs later, preferred direction is:

```text
Execution Boundary
        emits
Status Events

Consumers
        subscribe
```

rather than:

```text
Execution
        prints directly
```

or:

```text
Renderer
        polls internal execution state
```

This preserves renderer independence.

## Final Finding

Execution status should be emitted by work-producing boundaries and consumed by renderer-independent status consumers.

The architectural unit is not CLI progress.

The architectural unit is a transient execution-status stream.

CLI, audio, UI, notifications, federation surfaces, and future agents should all consume the same emitted execution status while preserving the boundary between activity visibility and knowledge preservation.
