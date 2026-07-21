# Execution and Recording

## Constitutional subject
The performance of an authorized execution and the separate preservation of what happened.

## Core question
What proves execution occurred, and what exactly may the resulting record claim?

## Bounded resolution
Execution is a warranted performance boundary for an authorized act or externally realized operation with observable or recordable result/refusal standing. It is not a local implementation function call, ordinary projection, read-model construction, diagnostic comparison, rendering, cache lookup, measurement, or execution-status display by identity. A bounded operation may be measured, completed, refused, recorded, rendered, projected, or externally realized without becoming execution merely by consuming time or resources; whether a particular bounded operation is execution depends on the applicable act, authority, realization, and occurrence grammar. Recording preserves an assertion about occurrence, lineage, and output within its preservation horizon; it does not retroactively authorize the act, independently verify external effects, or automatically extract knowledge from the result.

## Addressable boundaries for execution

### 07.Execution.A — Execution, operation, and result standing
Performing bounded work, externally realizing an act, executing an authorized act, preserving operation testimony, producing an operation result, and recording an execution are separate responsibilities. Execution may involve bounded invocation, external mechanism realization, occurrence evidence, and result or completion testimony, but those features do not make every bounded Seed-internal computation an execution. Projection, cache lookup, query selection, fact-index construction, observation collection, read-model construction, rendering, examination, comparison, ingress, and egress retain their own constitutional kinds unless a separate warranted execution boundary is established.

### 07.Execution.B — Execution recording boundary
An execution record is testimony that an execution boundary reported an occurrence, refusal, completion, failure, result, or lineage under its declared preservation horizon. It is not the execution occurrence itself, not the operation result by identity, not independent verification of external effect, and not knowledge extraction. A result returned or displayed by a boundary can be evidence for later examination only within its preserved source, authority, scope, and uncertainty.

## Important distinctions
- bounded operation != execution
- performing bounded work != externally realizing an act
- execution != local implementation function call
- execution != ordinary projection
- execution != read-model construction
- execution != diagnostic comparison
- execution != rendering
- execution != cache lookup
- execution != measurement itself
- proposal != authorization != invocation != completed execution != recorded execution
- execution result != execution record
- provider response != independently verified external effect
- execution != recording
- successful result != established fact
- recorded authorization reference != authority grant

## Representative repository anchors
- `seed_runtime/events.py::EventLedger`
- `seed_runtime/execution_status.py`

## Counterexamples or failure modes
- Treating a requested execution or operation request record as a successful result.
- Promoting returned output directly into state because it was recorded.
- Calling every measured projection, cache lookup, query, or rendering operation execution because it has timing testimony.

## Related chapters
- [Acts and act artifacts](../02-acts-and-constraints/acts-and-act-artifacts.md)
- [Recording and knowledge extraction](../05-evidence-and-knowledge/recording-and-knowledge-extraction.md)
- [Refusal and non-performance](../08-authority-communication-and-stopping/refusal-and-non-performance.md)
