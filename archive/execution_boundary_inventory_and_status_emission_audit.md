# Execution Boundary Inventory And Status Emission Audit

## Purpose

This audit follows:

- execution_status_and_operator_feedback_reconciliation.md
- execution_status_emission_and_consumption_reconciliation.md

Those reconciliations established that execution status should be emitted by work-producing boundaries and consumed by renderer-independent consumers.

This audit investigates the next implementation-facing question:

```text
What execution boundaries should emit status?
```

## Central Finding

Status should not be emitted by renderers.

Status should not be emitted by observations.

Status should not be emitted by projections.

Status should be emitted by execution boundaries that perform meaningful work.

## Candidate Execution Boundaries

The following categories appear to be natural status producers:

```text
Observation Collection
Observation Ingestion
Evidence Construction
Claim Import
Federation Import
Reconciliation
Projection Construction
Capability Inventory
Verification
Command Execution
Action Execution
```

These activities have:

```text
start
progress
completion
failure
```

and therefore can responsibly emit execution status.

## Observation Collection

Example:

```text
Collecting local host observations
```

Possible emissions:

```text
collection_started
collection_progress
collection_completed
collection_failed
```

## Observation Ingestion

Example:

```text
Appending observations to ledger
```

This boundary is especially relevant because the motivating interruption occurred during event persistence.

## Reconciliation

Examples:

```text
Identity Reconciliation
Relationship Reconciliation
Corroboration
```

Long-running reconciliation should be visible.

## Projection Construction

Examples:

```text
State Summary
Impact View
Capability Inventory
```

Projection work may be significant enough to warrant status visibility.

## Federation

Examples:

```text
Importing foreign claims
Importing foreign evidence
Synchronizing remote state
```

Federation status should preserve source provenance.

## Capability Inventory

Capability determination may become expensive as the system grows.

Capability inventory is therefore a likely status producer.

## Verification

Verification may involve:

```text
provider access
ssh
future APIs
```

Status visibility should exist independently of result visibility.

## Command And Action Execution

Examples:

```text
install package
restart service
apply configuration
```

Execution status is likely most important here because operators care about:

```text
started
running
waiting
completed
failed
```

## Non-Producers

The following should not become status producers merely because they exist:

```text
facts
claims
relationships
observations
projections
renderers
```

Status follows work.

Not knowledge.

## Recommended Status Lifecycle

A minimal lifecycle appears sufficient:

```text
started
progress
completed
failed
```

Additional states may emerge later.

## Architectural Invariants

```text
Execution Boundary != Renderer
Execution Boundary != Projection
Execution Boundary != Observation

Status Producer != Status Consumer

Work Produces Status
Knowledge Does Not Produce Status

Status Emission != Status Rendering
Status Event != Ledger Event
```

## Implementation Implications

Before implementing status infrastructure, identify execution boundaries.

The implementation target should not be:

```text
add progress bar
```

The implementation target should be:

```text
identify producers
identify consumers
identify emission points
```

Only after those boundaries are known should transport and rendering decisions be made.

## Final Finding

The next safe implementation step is not renderer work.

The next safe implementation step is execution-boundary discovery.

Seed should identify which work-producing boundaries emit status and which consumers render it. Once those boundaries are known, CLI, audio, UI, notification, and federation visibility can all share the same execution-status architecture.
