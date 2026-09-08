# Operational Measurement Topology Correction 001

## Status
Accepted as a bounded Book correction after PR 1895.

## Central Finding
Operational measurement is bounded operation-instance testimony and preservation grammar. It is not constitutionally identical to execution, execution record, operation result, diagnostic rendering, or ambient runtime/resource observation. PR 1895's preservation rule remains valid, but its placement under execution was overbroad because current repository testimony does not support treating every measured bounded Seed operation as execution.

## Canonical clauses examined
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `06-state-and-projection/projection-and-current-state.md`
- `07-operational-realization/execution-and-recording.md`
- `07-operational-realization/operational-realization-and-capability.md`
- `07-operational-realization/warrants-and-execution-proposals.md`
- `02-acts-and-constraints/acts-and-act-artifacts.md`
- `01-grammar-and-standing/external-and-constitutional-grammar.md`
- `concordance.md`

## Repository witnesses examined
Current implementation testimony includes `ProjectionBuildDiagnostics`, `ObservationIngestionDiagnostics`, `StateCacheStatus`, `SeedRuntimeObservationSource`, `ExecutionStatus`, current-selection timing, state-build cache timing, and fact-index timing. These witness isolated timings, cache-status testimony, projection and ingestion phase measurements, runtime/resource observations, and transient execution-status visibility. They do not witness an implemented operational baseline, tolerance comparison, deviation artifact, baseline-transition artifact, or timing-based lawful-movement consumer.

## PR 1895 findings preserved
PR 1895 correctly preserved that Seed need not preserve every operational measurement; non-rebuildable is not preservation-required; Seed must preserve sufficient evidence or compressed standing to retain materially sufficient operational understanding; ordinary samples may be discarded when their loss does not alter or erase that understanding; material deviation must preserve sufficient measurement and comparison context; and a baseline transition may preserve prior baseline, transition standing, new baseline, and sufficient evidence without retaining every raw sample.

## PR 1895 topology qualified or corrected
PR 1895 placed useful preservation grammar under `07-operational-realization/execution-and-recording.md`. This correction qualifies that placement: operational measurement may apply to execution, but it also may apply to projection, cache lookup, read-model construction, fact-index construction, observation collection, query selection, rendering, external realization, examination, comparison, ingress, egress, or another bounded operation. The canonical home for the cross-kind measurement and preservation grammar is now recording/testimony, with execution retaining only execution-specific occurrence and recording grammar.

## Bounded operation standing
The Book does not warrant turning operation into an unbounded universal bucket. Bounded operation remains a family resemblance across scoped performances of work whose subject, boundary, conditions, result, refusal, completion, or standing must be recovered from the local constitutional kind: act, movement, operation, realization, projection, examination, formation, comparison, rendering, ingress, or egress. Is every bounded Seed operation an execution? Not as a constitutional identity; execution is one possible bounded operation standing when the act, authority, realization, and occurrence grammar warrant it.

## Execution standing
Execution is a warranted performance boundary for an authorized act or externally realized operation with observable or recordable result/refusal standing. It is not a local implementation function call, ordinary projection, read-model construction, diagnostic comparison, rendering, cache lookup, measurement, or execution-status display by identity. Does measuring a projection, cache lookup, query, or rendering operation make it an execution? No, not by measurement alone. Does current repository evidence support the canonical claim that Seed commonly executes registered Python callables through `ToolExecutor.execute(...)`? No.

## Operational measurement standing
Operational measurement is bounded testimony about the observed behavior of a particular operation instance under declared conditions and measurement method. Is operational measurement constitutionally identical to execution? No. It is also not an execution record, operation result, ordinary behavior, future prediction, failure, capability loss, or permission to act by identity.

## Ordinary runtime/resource observation standing
Ordinary runtime/resource observation is testimony about a process or runtime condition at an observed time, such as process resident memory, thread count, process runtime duration, database size, or ledger size. Is ordinary runtime/resource observation identical to an operation-instance measurement? No. A runtime/resource observation may later support an operational measurement or baseline only through explicit attribution and establishment.

## Corrected preservation ownership
Operational measurement preservation belongs to retained testimony or compressed standing under recording/evidence grammar. Diagnostic rendering, CLI output, metrics display, or operator capture may expose measurement testimony but do not own or decide Seed preservation.

## Canonical clauses amended
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md` now owns operational measurement, runtime/resource observation, baseline, comparison, deviation, transition, and preservation/discard clauses.
- `07-operational-realization/execution-and-recording.md` now distinguishes execution from bounded operation, measurement, projection, cache lookup, rendering, diagnostic comparison, and local implementation calls.
- `concordance.md` now indexes operational measurement and baseline grammar under Evidence and Knowledge and removes runtime/resource observation as an alias of operational measurement.

## Stale implementation testimony removed
The canonical execution chapter no longer claims that current Seed commonly realizes execution through `ToolExecutor.execute(...)` invoking registered Python callables, and no longer lists `seed_runtime/execution.py::ToolExecutor` as representative current repository authority.

## Concordance corrections
The concordance no longer implies operational measurement equals execution and no longer aliases runtime/resource observation to operation-instance timing. Runtime/resource observation is indexed separately as observation testimony that may support measurement or baseline only through explicit attribution and establishment.

## What remains absent in implementation
No operational timing baseline is implemented. No tolerance comparison is implemented. No deviation artifact is implemented. No baseline-transition artifact is implemented. No timing-based lawful-movement consumer is implemented.

## What remains Unknown
This correction does not decide every possible future boundary where a bounded operation might also be an execution. It does not select a future measurement store, baseline artifact, tolerance policy, telemetry framework, performance policy, automatic comparison mechanism, or timing-based selector. It does not invalidate PR 1895's preservation rule.
