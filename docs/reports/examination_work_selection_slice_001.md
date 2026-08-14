# Examination Work Selection Slice 001

1. **Recovered responsibility**: Apply one supplied, applicable examination policy to its immutable `ExaminationFrontier` and select zero or one eligible work item while preserving the reason and non-selected alternatives.
2. **Producer**: `select_examination_work(frontier, policy, handoff)`.
3. **Input artifacts**: `ExaminationFrontier`, `ExaminationPolicyProjection`, and `ExaminationPolicySelectorHandoff`.
4. **Output artifact**: `ExaminationWorkSelection`, with `FutureProbeRequestHandoff` only when exactly one item is selected.
5. **Selection identity**: deterministic SHA-256 identity over frontier id, policy projection id, normalized handoff contents, selected/no-selection state, selected work reference, selection reason, and `examination_work_selection_v1` convention.
6. **Supported policy realization**: only existing policy kinds are realized: `explicit_work_identity`, `prerequisite_first`, `all_eligible_no_order`, and `no_selection`.
7. **Selection-state model**: `selected`, `no_selection`, `unknown`, `conflict`, and deterministic construction failure for invalid mismatched handoff/frontier/policy identities.
8. **Explicit-work behavior**: selects the named work only when the policy is applicable, sufficient, the named work exists, remains frontier-eligible, is not policy-excluded, and no no-selection boundary applies; otherwise returns zero selection with a policy-grounded reason.
9. **Prerequisite-first behavior**: uses only prerequisite references already preserved by the policy projection/handoff; exactly one eligible in-scope item may be selected, while unresolved prerequisite ties produce no selection.
10. **All-eligible-no-order behavior**: does not invent order; multiple eligible items produce no selection, while a sufficient sole eligible in-scope item may be selected.
11. **No-selection behavior**: always produces zero selected work references and preserves the explicit no-selection basis.
12. **Failed-but-eligible behavior**: failed remains an orthogonal frontier facet; failed-but-eligible work can be selected only by a policy that otherwise permits it, and failure alone does not prioritize it.
13. **Tie treatment**: only the policy-projected tie treatment is honored; lexical, insertion, hash, path, id, and arbitrary first-item tie-breaks are not used.
14. **Selection reason**: selected and no-selection artifacts carry deterministic, bounded reasons grounded in the policy realization.
15. **Non-selected preservation**: eligible alternatives are preserved as non-selected records with reasons; they are not rejected and their frontier classification remains owned by `ExaminationFrontier`.
16. **Frontier relationship**: the selector reads frontier classifications and references; it does not mutate or revise the frontier.
17. **Policy relationship**: the selector realizes an already projected policy; it does not create, alter, or duplicate policy projection ownership.
18. **Method-applicability relationship**: method constraints remain referenced through the policy projection for future handoff; methodological applicability remains owned upstream.
19. **Future probe-request handoff**: the narrow read-only handoff contains selection identity, inquiry/frontier/policy references, selected work reference, selection reason, and method-constraint reference; it constructs no probe request.
20. **Read-only guarantees**: `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`; no pending actions, execution, authorization, Observations, Evidence, or Facts are created.
21. **Boundary notes**: the artifact states that it applies existing policy, selects at most one item, does not authorize/schedule/execute/examine, preserves non-selected alternatives, treats no-selection as lawful but not campaign completion, uses no arbitrary tie-break, keeps frontier and method ownership upstream, and is not runtime Evidence or Fact.
22. **Compatibility answer**: No. This slice did not change any existing compatibility boundary.
23. **Files changed**: `seed_runtime/examination_work_selection.py`, `tests/test_examination_work_selection.py`, and `examination_work_selection_slice_001.md`.
24. **LOC delta**: +136 implementation lines, +122 focused test lines, +34 report lines before commit-time stat normalization.
25. **Tests executed**: `python -m pytest -q tests/test_examination_work_selection.py`; `python -m pytest -q tests/test_examination_work_selection.py tests/test_examination_policy_projection.py`; `python -m pytest -q tests/test_examination_work_selection.py tests/test_candidate_examination_work.py tests/test_examination_method_applicability.py tests/test_examination_frontier.py tests/test_examination_policy_projection.py tests/test_execution_proposals.py`.
26. **Remaining missing roads**: `ExaminationWorkSelection -> bounded probe request`; `bounded probe request -> operation/provider realization`; `realized probe -> policy authorization`; `authorized probe -> execution`; `execution result -> result recording -> frontier revision`.
27. **Exact next bounded question**: Given an `ExaminationWorkSelection` containing exactly one selected frontier work item, what smallest owner may construct a bounded probe request that preserves inquiry identity, artifact identity, work-contract identity, methodological constraints, selection reason, and the distinction between requested operation and authorized execution?

## Manual handoff eliminated

Before, a campaign author read the policy/frontier, chose work, explained the choice, remembered non-selected alternatives, and decided when no lawful selection existed. After this slice, Seed validates the handoff, applies the policy without inventing a tie-break, selects zero or one eligible item, preserves the selection reason and non-selected alternatives, and emits the future probe-request handoff only for a selected item.
