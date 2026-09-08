# Authority Need Projection Slice 001

Implemented one read-only `AuthorityNeedProjection` from explicit component-bounded `AuthorityRequirementTestimony` and `AuthorityStandingTestimony` tied to one selected goal, one bounded advancement horizon, one bounded authority component, one required authority class, one applicable scope, and horizon-material evidence.

The projection preserves requirement standing, authority standing, scope applicability, and horizon materiality as separate dimensions. It classifies only exact joined testimony and leaves failed identity, evidence, component, authority-class, scope, ownership, or materiality joins unclassified.

Conclusion matrix:

| Requirement | Authority standing | Authority need conclusion |
| --- | --- | --- |
| required | unavailable | established |
| required | available | unsupported |
| required | unknown | unknown |
| required | conflicting | conflicting |
| required | outside_current_scope | outside_current_scope |
| not_required | any | unsupported |
| unknown | any | unknown |
| conflicting | any | conflicting |

Guardrails preserved: no authority request, source selection, grant, scope expansion, authorization, realization selection, execution, recording, event-ledger write, or cluster mutation occurs.
