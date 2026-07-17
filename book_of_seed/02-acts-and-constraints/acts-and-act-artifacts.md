# Acts and Act Artifacts

## Constitutional subject
The classification of acts and the artifacts that report, propose, or preserve them.

## Core question
What establishes that an act occurred rather than that an act-shaped artifact exists?

## Bounded resolution
An act is a bounded responsibility at which something constitutionally occurs: a choice is made, material is admitted, standing is established, or an operation is performed. It consumes the subject plus the warrant and conditions appropriate to that occurrence and produces or preserves an attributed result. An act artifact reports or preserves that assertion; constructing it does not prove the act. Occurrence must be evidenced by the responsible validated function and, for operational acts, the execution or recording boundary.

## Important distinctions
- act != artifact describing an act
- classification of language != occurrence of the classified act
- proposal != occurrence
- intent classification != performance

## Representative repository anchors
- `seed_runtime/input_inspector.py::InputAct`
- `seed_runtime/advancement_need_consideration_selection.py::select_advancement_need_for_consideration`
- `seed_runtime/execution_proposals.py::ExecutionProposal`
- `seed_runtime/execution.py::ToolExecutor.execute`

## Counterexamples or failure modes
- Treating an execution proposal as evidence that a tool ran.
- Treating classified operator language as the requested act itself.
- Treating direct construction of a selection result as evidence that exact focus evidence was validated.

## Related chapters
- [Constraints, policy, and preconditions](constraints-policy-and-preconditions.md)
- [Execution and recording](../07-operational-realization/execution-and-recording.md)
- [Recording and knowledge extraction](../05-evidence-and-knowledge/recording-and-knowledge-extraction.md)
