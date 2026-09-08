# Operational Measurement Responsibility Topology Correction 001

## Status
Accepted as a bounded canonical Book correction after PR 1897.

## Central Finding
Operational measurement production, runtime/resource observation production, operational-standing establishment, preservation decision, recording, and rendering are distinct constitutional responsibilities. Recording does not produce operational measurement testimony and does not establish baseline, deviation, or transition standing. Recording may preserve already produced testimony or already established standing within its declared preservation horizon and standing limits.

## Canonical clauses examined
- `05-evidence-and-knowledge/testimony-and-established-fact.md`
- `05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `04-inquiry-and-examination/examination-methods-and-probes.md`
- `06-state-and-projection/projection-and-current-state.md`
- `07-operational-realization/execution-and-recording.md`
- `book_of_seed/concordance.md`

## Repository witnesses examined
- `ProjectionBuildDiagnostics`
- `ObservationIngestionDiagnostics`
- `SeedRuntimeObservationSource`
- `StateCacheStatus`
- current-selection timing
- state-build cache timing
- fact-index timing
- `ExecutionStatus`
- `EventLedger`

Implementation locations are witnesses, not automatic constitutional owners.

## PR 1895 findings preserved
PR 1895's preservation rule remains valid. Seed need not preserve every operational measurement. Non-rebuildable is not preservation-required. Seed must preserve sufficient evidence or compressed standing to retain materially sufficient operational understanding. Ordinary samples may be discarded when their loss does not alter or erase that understanding. Material deviations require sufficient measurement and comparison context. Lawful baseline transitions may preserve prior baseline, transition standing, new baseline, and sufficient evidence without permanently retaining every raw sample.

## PR 1896 findings preserved
PR 1896's execution correction remains valid. Bounded operation is not execution by identity. Operational measurement is not execution by identity. Operation-instance measurement is not ambient runtime/resource observation. This correction does not reintroduce `ToolExecutor.execute(...)` as a current canonical execution realization.

## PR 1897 findings preserved
PR 1897's semantic distinctions remain valid. Measurement production is not recording. Baseline establishment is not baseline recording. Comparison is not recording. Deviation recognition is not deviation recording. Baseline transition establishment is not transition recording. Preservation decision is not standing-establishment decision.

## Remaining structural compression
After PR 1897, the prose denied recording ownership but the canonical addresses `05.Recording.C`, `05.Recording.D`, and `05.Recording.E` still placed measurement production, runtime/resource observation production, and operational-standing establishment under Recording. That heading made readers negate the structure by prose. This correction removes that structural compression.

## Measurement-production responsibility
Measurement production lawfully belongs with testimony production and establishment grammar. It creates bounded operation-instance testimony that a particular operation instance, under declared conditions, was measured by a declared method and exhibited described behavior. It is distinct from the operation itself, operation result, execution, execution record, diagnostic rendering, recording, baseline establishment, future prediction, failure, capability loss, and permission to act. Measurement occurrence may exist transiently without being recorded.

## Runtime/resource-observation production responsibility
Runtime/resource observation production lawfully belongs with testimony and ordinary observation grammar. Process resident memory, thread count, process runtime duration, database size, and ledger size are observations about a process or runtime condition at an observed time. They are not operation-instance measurements by identity. They may later support operation attribution or operational-standing establishment only through explicit evidence and establishment boundaries.

## Operational-standing establishment responsibility
Operational baseline establishment, comparison authority and occurrence, material-deviation recognition, and baseline-transition establishment lawfully belong with standing-producing testimony and fact-establishment grammar. A retained measurement series is not an operational baseline. A recorded summary is not established ordinary behavior. A difference is not material deviation. A recorded difference is not material-deviation recognition. Repeated recorded samples are not a baseline transition. Record existence is not proof that recorded standing was lawfully established.

## Preservation-decision responsibility
Preservation decision remains a recording and preservation responsibility. It decides what evidence or compressed standing must survive within a declared preservation horizon so Seed retains materially sufficient operational understanding. It does not itself establish baseline, deviation, or transition standing.

## Recording responsibility
Recording may preserve attributed measurement testimony, runtime/resource observation testimony, already established baseline standing, already established deviation standing, and already established transition standing. Recording does not produce or establish those things merely by retaining a representation.

## Canonical ownership recovered
The recovered topology is:

```text
bounded operation or ambient runtime condition
        ↓
measurement or observation production
        ↓
attributed testimony
        ↓
examination / comparison / reconciliation
        ↓
possible baseline, deviation, or transition establishment
        ↓
preservation decision
        ↓
optional recording
```

The smallest lawful placement is:

- measurement production: `05.Testimony.B`
- runtime/resource observation production: `05.Testimony.C`
- baseline, comparison, deviation, and transition establishment: `05.Testimony.D`
- preservation decision: `05.Recording.C`
- recording: `05.Recording.A`, `05.Recording.B`, and `05.Recording.D`

## Execution residue examined
`EventLedger` and `ExecutionStatus` remain lawful representative anchors for execution recording and status-display boundaries. The concordance alias `execution = tool call` and execution counterexamples referring to `execution-request event` and `tool output` were unsupported residues from the deleted internal execution road and were removed or generalized. This correction does not invent a replacement execution producer.

## Concordance corrections
The concordance now indexes operational measurement, runtime/resource observation, operational baseline, material deviation, and baseline transition to `Testimony and established fact` rather than to `Recording and knowledge extraction`. It no longer implies that recording owns measurement production, establishes baselines, recognizes material deviations, establishes baseline transitions, equates execution with tool calls, or equates runtime/resource observation with operation-instance measurement.

## What remains absent in implementation
No operational timing baseline is implemented. No tolerance comparison is implemented. No material-deviation artifact is implemented. No baseline-transition artifact is implemented. No timing-based lawful-movement consumer is implemented.

## What remains Unknown
It remains Unknown which future producer, storage form, comparison authority, tolerance configuration, telemetry framework, performance policy, or timing-based consumer, if any, will be added. Canonical grammar does not create implementation.

## Required conclusions
Does recording produce operational measurement testimony? No.

Does recording a measurement series establish an operational baseline? No.

Does recording a difference establish material deviation? No.

Does recording repeated samples establish a baseline transition? No.

May recording preserve already produced testimony or already established standing? Yes, within its declared preservation horizon and standing limits.

Does the recording chapter currently provide a constitutionally honest structural home for measurement production and operational-standing establishment? No. The recovered topology places those responsibilities under testimony and establishment grammar, while recording retains preservation and record-standing responsibilities.

Does this correction invalidate PR 1895's preservation rule, PR 1896's execution correction, or PR 1897's semantic distinctions? No.

Are baseline, tolerance, deviation, transition, or timing-driven consumers now implemented? No.
