# Operational Realization Selection Slice 001

1. **Recovered responsibility:** Seed now selects zero or one supported operational realization for one exact reachable capability demand under an explicit policy, while preserving lawful refusal.
2. **Producer:** `select_operational_realization(...)`.
3. **Input artifacts:** `CapabilityReachabilityProjection`, matching `FutureOperationalRealizationSelectionHandoff`, matching `CandidateOperationalRealizationSet`, and `OperationalRealizationSelectionPolicy`.
4. **Selection-policy artifact:** `OperationalRealizationSelectionPolicy`, immutable and read-only; it can express exact-candidate, sole-supported-candidate, select-none, insufficient, and projected-dimension constraint policies.
5. **Output artifact:** `OperationalRealizationSelection`.
6. **Future warrant handoff:** `FutureOperationalRealizationWarrantHandoff`, emitted only for exactly one selected candidate and containing no warrant conclusion or invocation material.
7. **Selection-state model:** `selected`, `no_selection`, and `conflict`.
8. **Reachability gate:** non-`reachable` reachability states always produce no selection and preserve the reachability reason.
9. **Eligible-candidate rules:** eligibility is limited to supporting candidate references present in the reachability projection and matching candidate set; no candidate standing is recomputed.
10. **Exact-candidate policy:** selects only when the required candidate is an eligible supporting candidate.
11. **Sole-supported-candidate policy:** selects only when exactly one supporting candidate exists.
12. **Constraint-policy treatment:** filters only already-projected candidate dimensions: mechanism reference, representation pair, methodology standing, authority standing, and dependency standing.
13. **No-default-policy rule:** no policy or insufficient policy returns `no_selection` with `policy insufficient`.
14. **Selected treatment:** selected output preserves the selected candidate reference and all alternatives without warranting reliance.
15. **No-selection treatment:** no selected candidate is synthesized; bounded reasons distinguish insufficient policy, reachability gate, select-none, missing required candidate, no match, and tie.
16. **Conflict treatment:** incompatible required candidate identities produce `conflict` and no future warrant handoff.
17. **Tie treatment:** unresolved ties are preserved as no selection and are not resolved by ordering, lexical identity, registration order, or provider rank.
18. **Non-selected alternative preservation:** all supporting candidates not selected remain preserved as non-selected supporting candidates.
19. **Non-selected reasons:** reasons include alternative candidate, unresolved tie, selection-policy chose none, not-required candidate, and policy constraint not satisfied.
20. **Authority-related policy treatment:** policy may filter on projected authority standing, but selection never authorizes.
21. **Internal-versus-external treatment:** internal and external candidates use the same artifact; neither is preferred absent explicit policy.
22. **Deterministic identity:** selection identity is stable over demand, reachability, handoff, candidate-set, policy, eligible identities, selected/no-selection state, reasons, conflicts, and convention; timestamps and UUIDs are not used.
23. **Repository-search result:** two supported repository-search candidates with no policy produce no selection; exact policy selects one and preserves the other.
24. **Bash single-candidate result:** one Bash-representable candidate can be selected under the explicit sole-supported-candidate policy.
25. **Bash multiple-candidate result:** multiple Bash-representable candidates remain unresolved without a distinguishing policy.
26. **Internal-producer result:** deterministic internal producer candidates fit the same selection artifact and require no registry membership.
27. **Non-reachable results:** blocked, unsupported, unknown, and conflict reachability states cannot be overridden by policy.
28. **Policy-selects-none result:** explicit select-none policy returns no selection even when reachable.
29. **Invalid required-candidate result:** missing or non-eligible required candidates return no selection and do not cause fallback selection.
30. **Legacy selection precedent:** examination-work selection supplied the nearest precedent for bounded immutable selection, alternatives, ties, and future handoff; legacy operation selection was not modified.
31. **Warrant exclusion:** selection does not warrant reliance.
32. **Outward-translation exclusion:** selection does not build Bash, argv, stdin, cwd, environment, or process request material.
33. **Authorization exclusion:** selection does not authorize, schedule, propose, or execute.
34. **Caller-supplied inputs:** callers supply the projected reachability, handoff, candidate set, and explicit policy; raw realization material is not resupplied.
35. **Seed-owned selection responsibility:** Seed validates the handoff, applies the policy, selects zero or one, and preserves topology.
36. **Manual responsibility eliminated:** campaign authors no longer manually pick from supporting realizations or risk collapsing reachability, selection, and warrant.
37. **Read-only guarantees:** `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false` are preserved.
38. **Boundary notes:** output states that selection is not warrant, ordering is not policy, non-selected support remains support, and no tool/provider/toolkit/registered-operation concept is required.
39. **Compatibility answer:** No. This slice did not change any existing compatibility boundary.
40. **Files changed:** `seed_runtime/operational_realization_selection.py`, `seed_runtime/__init__.py`, `tests/test_operational_realization_selection.py`, and this report.
41. **LOC delta:** See `git diff --stat` and `git diff --numstat`.
42. **Tests executed:** focused selection tests plus compatibility tests listed in the final response.
43. **Baseline failures:** none observed in executed tests.
44. **Remaining roads:** `OperationalRealizationSelection → OperationalRealizationWarrant`; `OperationalRealizationWarrant → BoundedEgressTranslation`; `BoundedEgressTranslation → ConstitutionalAuthorization`; `ConstitutionalAuthorization → AuthorizedLocalProcessRequest → LocalProcessBoundary`; `ExternalBehavior → ResultObservationIngress → Comparison → Recording → KnowledgeAdmission`.
45. **Exact next bounded question:** Given one `OperationalRealizationSelection` containing exactly one selected realization for an exact bounded demand, what smallest owner may project whether Seed may rely upon that selection as preserving the demanded meaning across its representation grammar, invocation contract, behavioral support, dependency state, authority state, provenance, Unknowns, and conflicts without constructing an external request, authorizing, or executing it?
