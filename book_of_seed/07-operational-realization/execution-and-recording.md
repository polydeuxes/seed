# Execution and Recording

## Constitutional subject
The performance of an authorized operation and the separate preservation of what happened.

## Core question
What proves execution occurred, and what exactly may the resulting record claim?

## Initial resolution
Execution is the bounded operation-performance and result boundary. In the current repository it is commonly realized by `ToolExecutor.execute(...)` invoking registered Python callables and emitting started/completed/failed events. Constitutionally, the requirement is a warranted execution boundary with observable or recordable result standing, not a local Python call topology. Recording preserves an assertion about occurrence, lineage, and output within its preservation horizon; it does not retroactively authorize the act, independently verify external effects, or automatically extract knowledge from the result.

## Important distinctions
- proposal != authorization != invocation != completed execution != recorded execution
- execution result != execution record
- provider response != independently verified external effect
- execution != recording
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
