# Execution Status And Projection Pipeline Gap Audit

## Purpose

Recent testing showed that execution-status visibility improved, but the operator still encountered long silent phases during repository-source observation and state rebuilds.

This audit preserves the observed behavior before further implementation changes are attempted.

This is an audit.

It is not an implementation proposal, reconciliation, schema proposal, cache redesign, projection redesign, or performance fix.

## Triggering Observations

### Observation 1: Local host observation is verbose

The operator observed that local host observation emits useful status output.

This suggests some observation paths are properly threaded through the transient execution-status consumer.

### Observation 2: Repository-source observation is still silent

The operator observed that repository-source observation remains slow and emits little or no progress while work is occurring.

This suggests `--observe-repository-source` may not be using the same status path as `--observe-local-host`, or the long work inside that path does not emit progress.

This must be verified from implementation before patching.

### Observation 3: Incremental replay progress emits only boundary updates

Observed output:

```text
Incremental replay: 0 / 10668
Incremental replay: 10668 / 10668
```

The operator reported a long wait between those two lines.

This means either:

1. progress updates inside incremental replay are not firing as intended;
2. the expensive work is not actually inside the replay loop;
3. the expensive work happens after the replay loop completes.

The audit should not assume which one is true.

### Observation 4: Hold occurs after replay completion

Observed output during `seedstate` after repository observation:

```text
Loading state-summary cache...
State-summary cache: miss
Loading projection cache...
State cache: miss
Incremental replay: 0 / 10761
Incremental replay: 10761 / 10761
```

Then the process held after the final replay line.

This strongly indicates that at least one expensive phase occurs after the displayed incremental replay phase.

Candidates include, but are not limited to:

```text
finalize projected state
rebuild derived State structures
serialize State payload
save projection snapshot
build state-summary payload
save state-summary cache
build or invalidate derived indexes
```

These are hypotheses, not findings, until measured.

## Known Context

Recent work added:

```text
ExecutionStatusConsumer
CliExecutionStatusConsumer
bounded ProgressCadence helper
progress for projection replay
progress for incremental replay
progress for event writing
progress for fact index build
cache visibility for projection cache
cache visibility for state-summary cache
cache visibility for fact index cache
```

Despite that, user-visible behavior remains uneven across commands and phases.

## Boundary Finding

The key boundary remains:

```text
execution status
    !=
knowledge
    !=
events
    !=
observations
    !=
facts
    !=
projection authority
```

The issue is operator visibility and measurement, not knowledge semantics.

## Current Risk

The current risk is hen-pecking symptoms:

```text
silent phase observed
    ↓
add one status line
    ↓
another silent phase observed
    ↓
add another status line
```

That approach can spread status logic inconsistently and create a larger maintenance problem.

Before another fix, the repository needs an implementation audit of the full long-running command path.

## Required Investigation Areas

A follow-up implementation audit should identify the concrete phases and status coverage for:

```text
--observe-local-host
--observe-repository-source
--state-build / seedstate
--current-facts SUBJECT PREDICATE
--capability-candidates FILTER
--capability-verification FILTER
--capability-promotion-readiness FILTER
```

For each path, determine:

```text
which phases run
which phases emit status
which phases are silent
which phases can be long-running
which phases run on stdout vs stderr
which phases mutate caches
which phases mutate knowledge
```

## Required Measurement Questions

For slow incremental projection after repository observation, determine whether time is spent in:

```text
loading/deserializing snapshot
finding remaining events
applying remaining events
finalizing projected State
serializing State
saving projection snapshot
building dependent summary payload
saving summary cache
building derived index cache
other post-projection work
```

Do not infer the answer from status messages alone.

The final visible status line may not identify the slow phase.

## Desired Evidence

Before patching, collect evidence such as:

```text
cProfile output for the slow command
phase-level timing logs or instrumentation
exact status sequence for each command path
which functions receive status_consumer
which functions drop or fail to pass status_consumer
which loops use ProgressCadence
which expensive functions have no status boundary
```

## Non-Goals

This audit does not:

- propose new cache architecture;
- change projection semantics;
- change repository observation semantics;
- add new progress messages;
- add new indexes;
- modify execution status behavior;
- optimize performance;
- alter stdout/stderr behavior.

## Findings So Far

The repository currently has execution-status mechanisms and bounded progress cadence, but operator evidence shows incomplete coverage.

The strongest observed gap is not simply "incremental replay has no intermediate progress." The observed hold after:

```text
Incremental replay: 10761 / 10761
```

shows that post-replay work may be the true silent bottleneck.

Therefore the next work should be a concrete implementation audit with measurements, not another guessed status patch.

## Final Finding

Execution-status coverage is uneven across observation, projection, cache, and read-model paths.

The next safe step is to map the actual long-running pipeline phases and measure where time is spent before adding more status emissions or optimization patches.
