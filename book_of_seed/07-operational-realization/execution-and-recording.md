# Execution and Recording

## Constitutional subject
The performance of an authorized operation and the separate preservation of what happened.

## Core question
What proves execution occurred, and what exactly may the resulting record claim?

## Bounded resolution
Execution is the bounded operation-performance and result boundary. In the current repository it is commonly realized by `ToolExecutor.execute(...)` invoking registered Python callables and emitting started/completed/failed events. Constitutionally, the requirement is a warranted execution boundary with observable or recordable result standing, not a local Python call topology. Recording preserves an assertion about occurrence, lineage, and output within its preservation horizon; it does not retroactively authorize the act, independently verify external effects, or automatically extract knowledge from the result. Operational measurement is a distinct form of operation testimony: a bounded operation instance, under known conditions, was measured by a declared method and exhibited described operational behavior. A measurement may identify operation, instance scope, phase, duration or resource behavior, clock or method, input scale, cache condition, environment or authority context, completion condition, and observation time as needed by its consumer, but no implementation must possess every dimension. The measurement does not by itself establish ordinary behavior, predicted future duration, capability availability, correctness, failure, material degradation, or permission to act.

## Addressable boundaries for operational measurement

### 07.Execution.A — Operation, measurement, and retained operational understanding
Performing an operation, measuring that operation, preserving operation testimony, summarizing ordinary operational behavior, comparing a measurement, recognizing a material deviation, establishing changed ordinary behavior, and using operational understanding in later movement are separate responsibilities. A later movement consumer may use retained operational understanding only through the same bounded standing, authority, sufficiency, admissibility, and consumer-responsibility grammar that governs other evidence; operational evidence does not independently authorize movement.

### 07.Execution.B — Operational baseline, comparison, deviation, and transition
An operational baseline is retained, scoped, evidence-supported understanding of ordinary operational behavior under declared conditions. It is not a database table, raw timing history, average, threshold, fixed artifact, or predicted future duration by identity. It must preserve enough context to prevent comparison across constitutionally different subjects, such as cache hit and cache miss, full rebuild and incremental replay, fact-view inventory construction and subject/predicate selection, small and large inputs, or distinct environment and authority conditions. A tolerance or comparison boundary requires bounded authority: the baseline applied, the operation and conditions covered, the purpose of comparison, permitted variation, and the method by which that boundary was established. Difference from one prior sample is not material deviation. A material deviation preserves enough measurement and comparison context to retain the challenge to prior understanding, including operation, applicable baseline or comparison standing, context, observed difference, comparison authority and purpose, and remaining uncertainty; it is not automatically an operation failure, lost capability, cause, or consequence. A baseline transition is evidence-supported establishment that ordinary operational behavior materially changed from one bounded regime to another; one unusual sample is insufficient, and repeated samples are not sufficient merely by count without scope, conditions, comparison method, evidence sufficiency, conflict awareness, and temporal standing.

### 07.Execution.C — Preservation and discard of operational measurements
Seed need not preserve every operational measurement. Non-rebuildable is not equal to preservation-required: a raw measurement that cannot be reconstructed after process exit is preserved only when discarding it would erase material evidence or understanding of reality not otherwise retained. Seed must preserve sufficient evidence or compressed standing to retain its materially sufficient understanding of operational reality. A measurement within an established tolerance may be discarded when its loss does not alter or erase that understanding. A material deviation must preserve sufficient measurement and comparison context to retain the challenge to prior understanding. When changed ordinary behavior is lawfully established, Seed may preserve the prior baseline, transition standing, new baseline, and sufficient supporting evidence without permanently retaining every contributing raw measurement.

## Important distinctions
- proposal != authorization != invocation != completed execution != recorded execution
- execution result != execution record
- provider response != independently verified external effect
- execution != recording
- operation measurement != operational baseline
- operational baseline != predicted future duration
- difference from one sample != material deviation
- deviation != operation failure
- deviation != capability loss
- one unusual sample != changed ordinary behavior
- non-rebuildable != preservation-required
- ExecutionStatus cadence != operation timing testimony
- successful result != established fact
- recorded authorization reference != authority grant

## Representative repository anchors
- `seed_runtime/execution.py::ToolExecutor`
- `seed_runtime/events.py::EventLedger`
- `seed_runtime/execution_status.py`

## Counterexamples or failure modes
- Treating an execution-request event as a successful result.
- Promoting tool output directly into state because it was recorded.

## Related chapters
- [Acts and act artifacts](../02-acts-and-constraints/acts-and-act-artifacts.md)
- [Recording and knowledge extraction](../05-evidence-and-knowledge/recording-and-knowledge-extraction.md)
- [Refusal and non-performance](../08-authority-communication-and-stopping/refusal-and-non-performance.md)
