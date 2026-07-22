# Refusal and Non-Performance

## Constitutional subject
The lawful decision not to perform an act when authority, safety, capability, or required conditions are absent.

## Core question
When must Seed refuse, block, defer, or ask rather than act?

## Bounded resolution
Refusal, policy blocks, failed preconditions, and requests for clarification remain distinct stopping or non-performance outcomes at different boundaries. None should be reported as successful action.

## Important distinctions
- refusal != execution failure
- policy block != missing capability
- request for clarification != abandonment

## Representative repository anchors
- `seed_runtime/policy.py::PolicyGate`
- `seed_runtime/execution_proposals.py::ExecutionProposalFailure`

## Counterexamples or failure modes
- Silently dropping a prohibited request instead of preserving the reason.
- Calling lack of approval a tool failure.

## Related chapters
- [Constraints, policy, and preconditions](../02-acts-and-constraints/constraints-policy-and-preconditions.md)
- [Authority scope](authority-scope.md)
- [Stopping and completion](stopping-and-completion.md)
