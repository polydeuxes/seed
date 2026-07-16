# Authority Scope

## Constitutional subject
The origin, binding, extent, and non-transferability of authority across Seed's boundaries.

## Core question
What grants authority for a bounded goal or act, and how is that authority prevented from expanding in transit?

## Initial resolution
Operator expressions and explicit approvals may contribute authority only after interpretation and scope binding. Internal models, selections, records, and provider handoffs cannot create or enlarge that authority.

## Important distinctions
- operator request != unbounded authority
- scope binding != approval for every act in scope
- internal recommendation != authority grant

## Representative repository anchors
- `seed_runtime/operator_authority_scope_binding.py`
- `seed_runtime/policy.py::PolicyGate`
- `tests/test_internal_llm_authority_excision.py`

## Counterexamples or failure modes
- Allowing inferred intent to widen target or impact.
- Treating a recorded approval identifier as transferable authority.

## Related chapters
- [Construction and establishment](../03-goals-and-advancement/construction-and-establishment.md)
- [Selection and authorization](../03-goals-and-advancement/selection-and-authorization.md)
- [Communication and handoff](communication-and-handoff.md)
