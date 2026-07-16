# Acts and Act Artifacts

## Constitutional subject
The classification of acts and the artifacts that report, propose, or preserve them.

## Core question
What establishes that an act occurred rather than that an act-shaped artifact exists?

## Initial resolution
Seed distinguishes input acts and executable operations from artifacts describing them. Occurrence requires execution or another appropriate event boundary, not merely construction of a proposal.

## Important distinctions
- act != artifact describing an act
- proposal != occurrence
- intent classification != performance

## Representative repository anchors
- `seed_runtime/input_inspector.py::InputAct`
- `seed_runtime/execution_proposals.py::ExecutionProposal`
- `seed_runtime/execution.py::ToolCallResult`

## Counterexamples or failure modes
- Treating an execution proposal as evidence that a tool ran.
- Treating classified operator language as the requested act itself.

## Related chapters
- [Constraints, policy, and preconditions](constraints-policy-and-preconditions.md)
- [Execution and recording](../07-operational-realization/execution-and-recording.md)
- [Recording and knowledge extraction](../05-evidence-and-knowledge/recording-and-knowledge-extraction.md)
