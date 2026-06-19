# State Summary CLI Boundary Audit

## Purpose

This audit reviews the current boundary between State Summary semantics and CLI rendering.

The immediate trigger was a small State Summary output fix:

```text
availability unknown counting
compact top-entity alias rendering
```

Those fixes were appropriate in-place because they corrected current operator-visible output.

The remaining question is architectural:

```text
Which State Summary responsibilities belong in scripts/seed_local.py,
and which should move to runtime/read-model code before the surface grows?
```

## Current Context

State Summary has become one of the clearest operator overview surfaces.

Recent audits classify it as:

```text
repository overview / knowledge inventory
```

It currently summarizes:

```text
entity count
fact count
durable fact count
measurement current sample count
conflicts
stale facts
graph issues
observation sources
top entities
availability
filesystems
```

As Seed adds more observations, State Summary will likely want to summarize more domains.

Examples:

```text
packages
users
services
containers
firewall rules
scheduled jobs
capabilities
purpose
hardware inventory
```

If the summary semantics remain in the CLI, `scripts/seed_local.py` risks becoming a second read-model authority.

## Central Finding

```text
CLI rendering
        ≠
State Summary semantics
```

The CLI may render State Summary.

It should not own the meaning of State Summary.

## Current Boundary Smell

The current CLI contains logic that is more than terminal formatting.

Examples:

```text
which facts count as durable versus measurement
which entities participate in top entity summary
how availability is counted
how aliases are summarized
how filesystem measurements are paired
whether relationship count is included
```

These are semantic aggregation decisions.

They define what the repository overview means.

That is broader than rendering.

## What The CLI Should Own

`scripts/seed_local.py` should own:

```text
argument parsing
command dispatch
terminal formatting
plain-text layout
JSON serialization choices for CLI output
error messages for CLI misuse
```

Examples:

```text
--state-build flag handling
printing headings
indentation
line ordering for display
compact text formatting
```

These are presentation concerns.

## What Runtime / Read-Model Helpers Should Own

A runtime/read-model helper should own State Summary aggregation semantics.

Candidate module names:

```text
seed_runtime/state_summary_views.py
seed_runtime/state_summary.py
```

The exact name is less important than the ownership boundary.

The helper should own:

```text
entity participation
fact category counts
durable versus measurement categorization
availability summary semantics
top entity summary data
observation source accounting
filesystem summary data
relationship count inclusion
future domain summary inputs
```

These are not terminal-formatting choices.

They are read-model choices.

## Candidate Shape

A future shape could be:

```text
seed_runtime/state_summary_views.py
    StateSummaryView
    TopEntitySummary
    AvailabilitySummary
    FilesystemSummary
    build_operator_state_summary(state, ...)

scripts/seed_local.py
    calls build_operator_state_summary(state)
    formats StateSummaryView for terminal output
```

This preserves:

```text
runtime/read-model helper
    owns summary meaning

CLI
    owns display
```

## Why Not Move Immediately Before Fixing Output

The recent availability and alias fixes were intentionally done first.

Reason:

```text
Fix behavior before moving behavior.
```

A refactor before correction would risk hiding a semantic bug inside a file move.

The safer sequence is:

```text
1. Correct current behavior with characterization tests.
2. Audit ownership boundary.
3. Move semantics without changing behavior.
```

## Refactor Guardrails

A future State Summary boundary refactor should preserve behavior.

It should not introduce new semantics.

It should not expand State Summary.

It should not change availability meaning.

It should not change alias resolution.

It should not add observation, provider calls, probing, Runtime behavior, or ToolExecutor behavior.

The refactor should be mechanically verifiable by existing characterization tests.

## Availability-Specific Guardrail

Availability semantics are especially important because prior audit work established:

```text
local observation does not imply availability_status = up
missing availability evidence projects as unknown
availability_status must be evidence-backed and scoped
endpoint availability must not become host availability through alias flattening
```

A moved State Summary helper must preserve those rules.

The CLI should only render the resulting availability summary.

It should not decide what availability means.

## Alias-Specific Guardrail

Top-entity aliases in State Summary should remain compact.

State Summary may report:

```text
alias count
```

It should not inline all alias evidence.

Raw aliases remain owned by:

```text
Current Facts
Fact Support
```

A moved helper may compute alias counts.

The CLI may decide exact text such as:

```text
aliases: 39
```

but should not own alias evidence semantics.

## Tests For A Refactor

A semantics move should rely on existing characterization tests and add focused tests if needed.

Important cases:

```text
State Summary counts remain unchanged.
Top entity alias output remains compact.
Missing availability evidence counts as unknown.
Explicit up/down availability counts correctly.
Endpoint availability does not make host availability up.
Observation source counts remain deterministic.
Filesystem summaries remain deterministic.
CLI output remains stable.
```

If the refactor changes output, it is no longer only a boundary move.

## Non-Goals

This audit does not require immediate implementation.

It does not require changing State Summary output.

It does not require adding new summary sections.

It does not require renaming the CLI command.

It does not change Current Facts, Fact Support, Impact, or Integrity Summary.

It does not define final module names.

It does not introduce a new projection.

## Current Conclusion

State Summary has grown from a simple CLI report into a meaningful repository overview surface.

That means its aggregation semantics should not remain owned by the CLI indefinitely.

The next safe architectural step is likely:

```text
move State Summary semantic aggregation into a runtime/read-model helper
```

while preserving:

```text
scripts/seed_local.py
    owns terminal rendering only
```

This should be a behavior-preserving refactor after the current output fixes are characterized and green.