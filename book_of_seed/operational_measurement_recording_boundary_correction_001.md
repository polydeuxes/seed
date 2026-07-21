# Operational Measurement Recording Boundary Correction 001

## Status
Accepted canonical correction. This correction does not invalidate PR 1895's preservation rule or PR 1896's execution correction.

## Central Finding
Producing operational measurement testimony is not constitutionally identical to recording it. Operational measurement testimony may exist transiently without a recording boundary. Recording a set of measurements does not establish an operational baseline. Recording a difference does not establish material deviation. Recording repeated measurements does not establish a baseline transition. Recording may preserve already established measurement, baseline, deviation, or transition standing within its declared preservation horizon and standing limits.

## Canonical clauses examined
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`, especially 05.Recording.A-F.
- `07-operational-realization/execution-and-recording.md`, especially 07.Execution.A-B.
- `06-state-and-projection/projection-and-current-state.md`, especially rebuildability and prior invocation reconstruction.

## Repository witnesses examined
Current repository testimony includes projection build diagnostics, observation ingestion diagnostics, state cache status, runtime observation sources, execution status, current-selection timing, state-build cache timing, fact-index timing, event-ledger recording grammar, evidence extraction grammar, examination grammar, projection grammar, and temporal-standing grammar.

## PR 1895 findings preserved
PR 1895's preservation rule remains valid: Seed need not preserve every operational measurement; non-rebuildable is not preservation-required; Seed must preserve sufficient evidence or compressed standing to retain materially sufficient operational understanding; ordinary samples may be discarded when their loss does not alter or erase that understanding; material deviation must preserve sufficient measurement and comparison context; and a lawful baseline transition may preserve the prior baseline, transition standing, new baseline, and sufficient evidence without retaining every raw sample.

## PR 1896 findings preserved
PR 1896's topology correction remains valid: bounded operation is not execution; operational measurement is not execution; operation-instance measurement is not ambient runtime/resource observation; and current repository evidence does not restore the stale `ToolExecutor` execution ontology.

## Remaining ownership compression
The remaining compression was that the operational-measurement district sat under recording in a way that could be read as making recording the producer or owner of measurement testimony, baseline standing, deviation recognition, and baseline transition standing. The correction separates production, establishment, rendering, and preservation while allowing the recording chapter to keep preservation and record-existence grammar.

## Measurement-production standing
Operational measurement is bounded testimony about the observed behavior of a particular operation instance under declared conditions and measurement method. The measurement-production responsibility produces that testimony. The operation itself, operation result, execution, execution recording, diagnostic rendering, durable preservation, baseline establishment, future prediction, failure, capability loss, and permission to act are distinct. A measurement may exist transiently without ever being durably recorded.

## Runtime/resource observation production standing
Runtime/resource observations may be produced through ordinary observation grammar. They are not operation-instance measurements by identity and may later support operation attribution, baseline examination, or deviation analysis only through explicit evidence and establishment boundaries. Recording is not their producer merely because recorded observations can survive process exit.

## Baseline-establishment standing
An operational baseline is retained, scoped, evidence-supported understanding of ordinary operational behavior under declared conditions. Baseline establishment may consume measurement testimony, explicitly attributed runtime/resource observations, scope, context, temporal evidence, comparison method, conflicts, and uncertainty. Retained measurement series is not an operational baseline; recorded summary is not established ordinary behavior; baseline recording is not baseline establishment.

## Comparison and deviation standing
A comparison consumes an applicable baseline or other authorized comparison boundary and a measurement within a declared purpose and scope. Comparison is not recording, and comparison occurrence is not recorded comparison. Difference is not material deviation. Material deviation recognition is distinct from deviation recording; storage of a difference does not decide constitutional materiality.

## Baseline-transition standing
Baseline transition establishment is distinct from transition recording. One unusual sample is not changed ordinary behavior, and repeated samples by count alone do not establish baseline transition. A transition recorder may preserve the prior baseline, transition standing, new baseline, and sufficient supporting evidence after lawful establishment.

## Recording and preservation responsibility
Recording may preserve attributed testimony or already established standing within its declared preservation horizon. Recording does not create the upstream measurement, comparison authority, baseline standing, deviation standing, or transition standing merely by storing their representation. Record existence proves record existence, not that recorded standing was lawfully established.

## Canonical clauses amended
- `05.Recording.C` now names operational measurement production and separates production from recording, diagnostic rendering, and preservation.
- `05.Recording.D` now states runtime/resource observation production may occur through ordinary observation grammar without recording ownership.
- `05.Recording.E` now separates baseline establishment, comparison occurrence, deviation recognition, and transition establishment from their recorded forms.
- `05.Recording.F` now states preservation decision is not standing-establishment decision and record existence is not lawful establishment.

## Concordance corrections
The concordance points operational measurement, runtime/resource observation, operational baseline, material deviation, and baseline transition to the recording/evidence chapter as the current canonical address while describing production or establishment responsibility rather than equating those concepts with recording, recorded summaries, recorded differences, or stored timing histories.

## What remains absent in implementation
No operational timing baseline is implemented. No tolerance comparison is implemented. No deviation artifact is implemented. No baseline-transition artifact is implemented. No timing-based lawful-movement consumer is implemented.

## What remains Unknown
It remains Unknown which future operational consumers, if any, will require retained operational baselines; which comparison authority form would be warranted; which raw measurements would be materially necessary; where a future measurement producer or store would live; and which implementation surface should preserve deviation or transition testimony if later authorized.
