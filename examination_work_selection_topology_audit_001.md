# Examination Work Selection Topology Audit 001

## 1. Bounded question

Given an immutable `ExaminationFrontier` whose candidate work was derived by Seed, what existing owner—or smallest missing owner—may select one eligible work item for conversion into a bounded probe request while preserving methodological constraints, inquiry purpose, selection reason, authorization boundaries, and all non-selected alternatives?

Second question: how does this frontier-movement selector differ from the existing methodological selector governing internal grammar, external grammar, and fidelity?

## 2. Settled orientation

Tested hypothesis:

- Methodological selector governs the lawful manner of examination.
- Examination-work selector governs movement through an already lawful examination frontier.

Repository evidence refines this: the implementation-backed selector closest to internal/external grammar/fidelity is `select_constitutional_views(...)`, but it does not actually select grammar or examination method. It selects registered constitutional read-model view names by exact caller-declared selection keys and capability keys. The examination-work selector is absent.

## 3. Governing distinctions

The audit preserved the requested distinctions: methodological orientation is not campaign traversal; lawful method is not next work item; technically compatible work is not necessarily methodologically applicable work; applicable work is not currently eligible work; eligible work is not selected work; selected work is not authorized execution; selection reason is not semantic truth; inquiry goal is not a selection algorithm; policy is not special operator identity; fidelity is not a priority score; external grammar applicability is not provider permission; internal grammar availability is not sufficiency; non-selected is not rejected; no selection is not campaign completion; and work selection is not probe-request construction.

## 4. Methodology

Read-only implementation audit only. Searches were used to locate relevant owners, then implementation bodies and tests were inspected. No candidate work, probe, scheduler, executor, campaign traversal, knowledge admission, or authorization action was executed.

Commands/probes executed:

```bash
find .. -name AGENTS.md -print
cat AGENTS.md
rg -n "methodolog|internal grammar|external grammar|fidelity|orientation|applicability" seed_runtime campaigns tests *.md
rg -n "CandidateExaminationWork|ExaminationFrontier|eligible|selected|non.selected|selection reason" seed_runtime campaigns tests *.md
rg -n "selection path|candidate set|work dispatch|operation selection|policy authorization|probe request" seed_runtime campaigns tests *.md
rg -n "class .*Method|Methodological|internal_grammar|external_grammar|fidelity|CandidateExaminationWork|ExaminationFrontier|candidate_examination|examination_frontier|selection_path|bounded_work|operation selection|capability selection|policy authorization|probe" seed_runtime tests campaigns --glob '*.py'
sed -n '1,220p' seed_runtime/candidate_examination_work.py
sed -n '1,220p' seed_runtime/examination_frontier.py
sed -n '1,220p' seed_runtime/candidate_external_grammar.py
sed -n '1,240p' seed_runtime/constitutional_view_selection.py
sed -n '1,380p' seed_runtime/selection_path_audit.py
sed -n '1,700p' seed_runtime/question_surface_inventory.py
sed -n '1,240p' seed_runtime/tool_validation.py
sed -n '1,240p' seed_runtime/tool_execution_policy.py
sed -n '1,160p' seed_runtime/bounded_constitutional_question.py
sed -n '1,220p' tests/test_candidate_examination_work.py
sed -n '1,240p' tests/test_examination_frontier.py
```

## 5. Inspected implementation owners

- `produce_bounded_constitutional_question(...)` in `seed_runtime/bounded_constitutional_question.py`.
- `project_constitutional_question(...)`, `project_constitutional_capabilities(...)`, and `select_constitutional_views(...)` in `seed_runtime/constitutional_view_selection.py`.
- `assemble_candidate_external_grammar_set(...)` in `seed_runtime/candidate_external_grammar.py`.
- `project_candidate_examination_work(...)` in `seed_runtime/candidate_examination_work.py`.
- `project_examination_frontier(...)` in `seed_runtime/examination_frontier.py`.
- `build_selection_path_audit(...)` and payload helpers in `seed_runtime/selection_path_audit.py`.
- bounded work eligibility/selection/dispatch request helpers in `seed_runtime/question_surface_inventory.py`.
- `ToolValidationService.select_operation(...)` and `ToolExecutionPolicyService` in `seed_runtime/tool_validation.py` and `seed_runtime/tool_execution_policy.py`.
- Representative tests for candidate work, frontier, constitutional view selection, bounded dispatch, external grammar, and policy.

## 6. Current road

Implementation-backed road verified:

```text
explicit bounded corpus members
+
known representation visibility
+
visible work contracts
→ CandidateExaminationWorkSet
→ ExaminationFrontier
```

Evidence:

- Candidate work is derived from explicit corpus membership, representation visibility, and visible contracts.
- Candidate records preserve compatibility observations, missing prerequisites, capability availability, provenance, and Unknowns.
- Candidate records explicitly are not selected, eligible, authorized, scheduled, or executed.
- Frontier owns classification into eligible, examined, blocked, unsupported, deferred, failed, conflict, and Unknown.
- Frontier explicitly is not a scheduler, queue, priority ranking, or campaign completion verdict.
- Tests show free-form `candidate_work_names` do not generate ordering and that mixed-corpus structural/surface/acquisition work is derived from contract visibility rather than manual prose names.
- Examination resolution and next-work selection remain outside the implemented road.

## 7. Methodological-selector analysis

Actual implementation-backed selector: `select_constitutional_views(...)`.

- Producer: `select_constitutional_views(...)`.
- Input artifact: `ConstitutionalQuestionProjection` plus tuple of `ConstitutionalCapabilityProjection`.
- Output artifact: `SelectedConstitutionalViews`.
- Immediate consumer: constitutional view composition request construction (`constitutional_view_composition_request(...)`) and constitutional view composition path.
- Exact selection dimensions: exact intersection between caller-declared selection keys on the bounded question and capability keys projected from registered constitutional read-model views.
- Fidelity role: fidelity is an implementation-supported capability key exposed by `ConstitutionalFidelityView` and selectable as a constitutional view dimension. It is not an examination method, priority score, or frontier-movement rule in this implementation.
- Output form: selected registered view names plus uncertainty and read-only boundary metadata. It is orientation/view applicability, not execution permission.
- Operation selection: no. It selects read-model views, not operations, probes, providers, or work items.
- What it refuses: semantic inference, capability discovery, mutation, persistence, event-ledger writes, registration repair, constitutional authority creation, and composition ownership.

It does not select internal grammar or external grammar as examination methods. `CandidateExternalGrammarSet` preserves caller-supplied structural hypotheses and refuses selection, verification, translator readiness, and capability establishment.

## 8. Existing selection-owner inventory

| Owner | Input | Selection basis | Output | Non-selected preservation | Authorization semantics | Reuse status |
| ----- | ----- | --------------- | ------ | ------------------------- | ----------------------- | ------------ |
| Constitutional view selection | `ConstitutionalQuestionProjection` + `ConstitutionalCapabilityProjection` | Exact declared selection keys intersect exact capability keys | `SelectedConstitutionalViews` | Unsupported keys become uncertainty; non-selected registered views are not fully snapshotted | Read-only; no execution permission | constitutional precedent |
| Selection path audit | State-derived pressures + target | Implemented focus or pressure-category target matching | `SelectionPathAudit` | Preserves candidates, non-selected candidates, factors, evidence, Unknowns | Diagnostic read-only only | diagnostic-only |
| Candidate external grammar preservation | Caller-supplied candidate grammar input | No selection; duplicate validation only | `CandidateExternalGrammarSet` | Preserves candidates, alternatives, support/contradiction, Unknowns | No translator readiness or capability permission | wrong selection dimension |
| Candidate examination work projection | Corpus members + representation visibility + contracts | Technical/visibility compatibility by representation and contract availability | `CandidateExaminationWorkSet` | Preserves emitted candidates, exclusions, missing prerequisites, Unknowns | Not eligible/authorized/scheduled/executed | implementation precedent |
| Examination frontier classification | Bounded inquiry + corpus members + candidate work + status evidence | Compatibility, authorization status, existing results, blockers, deferrals, failures, Unknowns | `ExaminationFrontier` | Preserves every supplied work item with classification | Eligible still not selected/authorized/executed | implementation precedent |
| Bounded work dispatch selection | Exact question family eligibility | Static map-backed surface selection after permitted eligibility | `BoundedWorkSelectionResult` | No candidate frontier alternatives; map-level non-selection not represented | Dispatch selection, not policy authorization | wrong selection dimension |
| Operation selection | Operation name from already-formed call-tool decision | Registry/state lookup of named operation | `OperationSelectionResult` | No alternative providers or capabilities | Validation precursor; no policy authorization | wrong selection dimension |
| Tool policy authorization | Validated registered operation call + state | Policy gate decision | `ToolExecutionPolicyResult` | Non-allow policy retained, but not frontier alternatives | Authority-bearing and unsafe for selection | authority-bearing and unsafe |
| Capability projection/selection in constitutional view selection | Registered read-model contracts/views | Capability keys exposed by immutable views | Capability projections / selected view names | Unsupported keys only | Read-only | constitutional precedent |

No inspected owner can directly consume `ExaminationFrontier` and produce a lawful selected frontier work item while preserving methodological constraints and all alternatives.

## 9. Selector-dimension analysis

The methodological selector and examination-work selector act on different dimensions.

- Existing methodological-like selection: bounded question material/declared keys plus registered view capability projections to select a lawful constitutional view/orientation artifact.
- Missing examination selection: frontier plus inquiry/policy to choose next lawful movement among eligible work items.

They are not the same selector at different resolutions. Repository evidence supports separate orthogonal selectors with a missing implementation handoff.

## 10. Selector-relationship analysis

Relationship: orthogonal but missing handoff.

They can compete only if a future owner lets methodology decide item priority or lets frontier selection decide method applicability. Existing code avoids that conflict because constitutional view selection has no frontier input and frontier classification has no methodological orientation input.

## 11. Handoff-location analysis

Possible handoffs and current support:

1. `methodological orientation → work-contract applicability → CandidateExaminationWorkSet`: not implemented. This is the earliest required handoff if technically compatible contracts can be methodologically inapplicable.
2. `CandidateExaminationWorkSet + methodological orientation → ExaminationFrontier`: not implemented. Frontier consumes candidate work and status evidence, not methodological applicability.
3. `ExaminationFrontier + methodological orientation → work selection`: not implemented. This would prevent selecting an unlawful method only if method applicability is carried or recomputed here.
4. `selected work + methodological orientation → probe request`: not implemented and too late to prevent unlawful candidates from appearing as frontier-eligible.

Earliest required handoff: methodological applicability must constrain contract applicability before or during candidate work generation. Existing adapter from candidate work to frontier has no methodological fields, so applying methodology only at final selection would allow unlawful but technically compatible work to enter the frontier as eligible.

## 12. Examination-resolution analysis

Current supplier of examination resolution: campaign author / caller testimony, not a typed implementation artifact.

Candidate bases:

- Answer bounded inquiry: partially represented as bounded question prose; not algorithmic.
- Continue deep examination beyond first sufficiency: raw caller/campaign policy if present; not typed.
- Satisfy prerequisites before dependent work: represented indirectly through missing prerequisites/blockers, but no ordering selector.
- Apply every compatible projection: not implemented as policy; would be caller/campaign traversal.
- Maximize bounded corpus coverage: not implemented as policy.
- Continue current artifact through next layer: possible to infer from representation chains, but not typed.
- Retry failed-but-eligible work: frontier can mark failed and eligible together; no policy selects retry.
- Resolve blocking dependency: blockers are represented; no dependency-resolution policy.
- Honor explicitly selected work identity: no frontier work selector accepts such identity.

A typed examination-resolution/policy handoff is absent. Turning these into numeric priority would be improper unless the policy artifact explicitly authorizes that scoring basis.

## 13. Goal-versus-orientation answer

Yes, with repository refinement: the existing methodological-like selector is orientation/read-model-view-key based, while the missing examination selector is frontier-movement/policy-realization based. “Goal-based” alone is too imprecise because current bounded inquiry fields preserve purpose as caller testimony but do not encode an executable selection rule. The implementation-backed missing dimension is examination resolution or policy over a frontier, including inquiry satisfaction, prerequisite ordering, corpus movement, and refusal to select when policy is Unknown.

## 14. Candidate-applicability analysis

`CandidateExaminationWorkSet` currently enumerates technically/visibility-compatible work, not methodologically lawful work.

Answers:

- Can a technically compatible external grammar contract appear without methodological applicability? Yes. Contracts are matched on representation kind, availability, and optional member ids; no methodological applicability field is checked.
- Can a fidelity requirement alter or exclude a candidate? Not currently. Fidelity is not consumed by candidate projection.
- Can one candidate require attributed testimony while another can produce mechanical projection? The schema can distinguish work kind/contract convention/capability, but it lacks typed attribution or claim-type applicability constraints.
- Is methodological applicability already represented in contract visibility? Insufficiently. Contracts carry ids, capability, work kind, accepted and produced representations, convention, availability, applicable member ids, provenance, and unknowns; not method constraints.
- Is a new candidate-work schema field required, or can an adapter preserve compatibility? An adapter could preserve compatibility by projecting methodological applicability into contract visibility/provenance/unknowns before candidate work, but a typed field may become necessary if selection must distinguish technical compatibility from methodological applicability.
- Would applying methodology only at selection time allow unlawful candidates into the frontier? Yes, if the frontier continues to classify technical compatibility and authorization as eligible without method applicability.

## 15. Policy-artifact analysis

No typed artifact currently carries all of:

```text
inquiry identity
examination resolution
methodological constraints
frontier identity
eligible candidate identities
prerequisite relationships
selection rule or basis
unknowns
```

The first missing owner is examination-policy projection, not eligible-work selection. Policy projection should not be collapsed into item selection because selection needs an already lawful basis for choosing among multiple eligible items and for refusing selection.

## 16. Selection-result analysis

Smallest lawful future selector output likely needs:

- selection identity;
- frontier identity;
- inquiry identity;
- selected work item or explicit no-selection;
- selection basis/policy reference;
- selection reason;
- methodological constraints applied or applicability reference;
- all non-selected eligible items;
- blocked/unsupported/deferred/failed/Unknown items unchanged or referenced;
- selection Unknowns;
- read-only, no-event, no-mutation guarantees.

Zero selected items must be lawful when no work is eligible, policy is Unknown, tied items lack a lawful tie-break, or methodological applicability is unresolved.

## 17. Non-selected preservation

Existing selection-path audit preserves non-selected candidates and reasons for its pressure/focus domain. Candidate external grammar preserves alternatives. Examination frontier preserves all classified work items. No existing examination selection artifact snapshots non-selected eligible frontier work because no such selector exists.

Future selection should snapshot the relevant eligible alternatives and selection-specific non-selection reasons while leaving the frontier as source of truth for full classification state.

## 18. Authorization boundary

A future selector may establish only “selected for probe-request construction.” It must not authorize network access, approve external providers, execute tools, create pending actions, bypass tool policy, or mark work examined. The immediate consumer should be a bounded probe-request generator, not an executor.

## 19. Proving trace

Existing mixed-corpus proving case: `tests/test_candidate_examination_work.py::test_mixed_corpus_proving_and_no_prose_or_comparison_invention` plus `tests/test_examination_frontier.py::test_mixed_corpus_demonstration_and_compatibility_boundaries`.

Trace:

1. Bounded inquiry: produced by `produce_bounded_constitutional_question(...)` in tests as caller-preserved bounded question.
2. Methodological orientation: no explicit handoff into candidate work/frontier. Constitutional view selection can select fidelity/process/governance views elsewhere, but this trace does not compose it.
3. Candidate work: `project_candidate_examination_work(...)` derives structural, surface-feature, and acquisition candidate work from member representations and contracts.
4. Frontier classification: `project_examination_frontier(...)` classifies existing completed structural/surface work as examined, website acquisition as blocked, prose interpretation as Unknown, comparison as unsupported.
5. Examination resolution/policy: supplied by test/campaign author arrangement, not typed.
6. Possible selection: absent. No owner selects one eligible frontier item.
7. Future probe request: absent.

Current campaign-author-supplied step: examination resolution / next-work decision and any manual decision that a particular work item should become a probe request.

## 20. Topology table

| Stage | Producer | Artifact | Consumer | Current owner | Missing handoff |
| ----- | -------- | -------- | -------- | ------------- | --------------- |
| bounded inquiry | `produce_bounded_constitutional_question(...)` | `BoundedConstitutionalQuestion` | constitutional question projection; frontier projection | present | None for inquiry preservation |
| methodological orientation | `project_constitutional_question(...)` + `project_constitutional_capabilities(...)` + `select_constitutional_views(...)` | `SelectedConstitutionalViews` | constitutional composition | partially present for read-model views | No handoff to examination contracts/candidates/frontier |
| contract applicability | caller-visible contracts; `ExaminationWorkContract` | contract visibility | candidate work projection | technical visibility only | Methodological applicability projection absent |
| candidate work generation | `project_candidate_examination_work(...)` | `CandidateExaminationWorkSet` | frontier adapter / caller | present | Method constraints absent |
| frontier classification | `project_examination_frontier(...)` | `ExaminationFrontier` | operators/diagnostic consumers | present | No policy/method handoff to selection |
| examination resolution/policy | campaign author/caller prose | none typed | none | absent | Typed policy projection absent |
| eligible-work selection | none | none | none | absent | Selector absent after policy |
| non-selected preservation | frontier; selection-path precedent | frontier work items / selection audit in other domain | future selector would consume/snapshot | partially present as precedent | Selection-specific alternatives snapshot absent |
| probe-request generation | none found for frontier work | none | executor/policy validation in future | absent | Selected-work to bounded probe request absent |
| authorization | `ToolExecutionPolicyService` for tools | `ToolExecutionPolicyResult` | callers | present for registered operations | Must remain after probe construction, not inside selection |
| execution | existing execution paths/tools | operation results/events where applicable | runtime consumers | out of scope | Not part of selection |

## 21. Current campaign-author responsibility

The campaign author currently supplies the examination-resolution and next-work decision outside the implemented road: deciding which eligible or possible work item should move toward a probe request, why that item advances the bounded inquiry, and what happens to non-selected alternatives.

## 22. Strongest supporting evidence

- Candidate work boundary notes explicitly say candidate records are not selected, eligible, authorized, scheduled, or executed.
- Frontier boundary notes explicitly say eligible work is not selected, authorized, or executed and the frontier is not scheduler/queue/priority/campaign completion.
- Candidate projection code uses representation-kind matching, contract availability, and member ids; it does not consume methodological orientation.
- Frontier classification code uses compatibility, authorization status, results, blockers, deferrals, failures, and Unknowns; it does not consume methodological orientation or policy.
- Bounded work dispatch selection is map-backed for exact question families, not frontier work.
- Tool operation selection starts from an already-selected operation name and refuses capability/provider recommendation ownership.
- Tool policy authorization is separate from validation and execution, supporting the required authorization boundary.

## 23. Strongest counterevidence

- Constitutional view selection already demonstrates a deterministic selector from bounded question projection plus capability projections to selected views, including fidelity; this is a precedent for composition.
- Selection path audit already preserves selected value, candidate set, selection factors, non-selected candidates, evidence, outcome, and Unknowns; mechanically it resembles the desired visibility artifact.
- Bounded work selection already composes eligibility, selected dispatch surface, selected surface value, and dispatch request construction for exact question families.
- Frontier classification already handles prerequisites/blockers, failed-but-eligible combinations, and eligibility, so a simple deterministic order over eligible items might be tempting.
- Candidate contracts include `applicable_member_ids`, `work_kind`, convention, provenance, and unknowns, which may be enough for some applicability testimony without a new schema field.
- Campaign traversal may intentionally remain external if repository policy requires human choice for next work.
- Probe-request generation might be the practical missing owner if a caller already knows the work item identity.
- Current frontier may be insufficient for lawful selection because it lacks explicit dependency graph, inquiry satisfaction criteria, methodological applicability, and policy.
- The methodological selector and examination selector could overlap in a future design if “fidelity” were incorrectly treated as a work-item priority rather than a constraint/key.

## 24. Supported conclusions

1. The actual implementation-backed methodological-like selector is constitutional view selection.
2. It selects registered constitutional view names by exact key/capability intersection.
3. Fidelity is a selectable read-model capability/view key, not an examination priority or frontier movement method.
4. Candidate examination work is technically/visibility compatible work, not methodologically lawful work.
5. Frontier owns classification, not next-work choice.
6. Examination resolution/policy is absent as a typed artifact.
7. Eligible-work selection is also absent, but should follow policy projection.
8. Future selection must preserve alternatives and may return no item.
9. Authorization must remain downstream of probe request validation/policy, not inside selection.

## 25. Unsupported conclusions

- That internal grammar, external grammar, and fidelity exist as mature runtime methodological dimensions for examination work.
- That existing selection-path audit can directly consume an `ExaminationFrontier`.
- That candidate contracts already carry all methodological applicability.
- That all eligible work may be dispatched independently.
- That a deterministic prerequisite order is sufficient.
- That one selected item is always required.
- That probe-request generation alone can safely recover the missing boundary without policy projection.

## 26. Primary classification

C. Methodological orientation exists, but examination-policy projection is the first missing owner.

## 27. Selector-relationship classification

3. The selectors are orthogonal, but their implementation handoff is missing.

## 28. First-missing-boundary classification

II. Examination-resolution or policy projection is the first missing boundary.

## 29. Exact next bounded boundary

Recovered responsibility: project typed examination resolution/policy from bounded inquiry/caller testimony plus methodological constraints and frontier identity, without selecting a work item.

Producer: a future examination-policy projection owner.

Input artifacts: bounded inquiry, methodological orientation/applicability reference, immutable `ExaminationFrontier`, caller-supplied resolution testimony if any.

Output artifact: typed examination policy projection carrying inquiry identity, frontier identity, eligible candidate identities or references, prerequisite/dependency testimony, selection rule/basis, constraints, and Unknowns.

Immediate consumer: future eligible-work selector.

Exact bounded question: what lawful basis, if any, exists for choosing among eligible frontier work items for this bounded inquiry?

Manual responsibility eliminated: campaign author prose deciding or implying the next-work policy before item selection.

Explicit exclusions: no item selection, no probe request construction, no authorization, no execution, no examined marking, no priority scoring unless explicitly represented as policy testimony.

## 30. Implementation-warrant decision

One bounded implementation slice is warranted.

- Recovered responsibility: examination-policy projection.
- Producer: future examination-policy projection function/module.
- Input artifacts: bounded inquiry, methodological orientation/applicability reference, `ExaminationFrontier`, explicit caller policy/resolution testimony.
- Output artifact: typed examination policy projection.
- Immediate consumer: future eligible-work selector.
- Exact bounded question: what lawful selection basis applies to this frontier without choosing an item?
- Manual responsibility eliminated: campaign-author/manual prose handoff for examination resolution.
- Explicit exclusions: no work selection; no probe request; no authorization; no execution; no queue; no scheduler; no campaign completion; no knowledge admission.

## 31. Files changed

- `examination_work_selection_topology_audit_001.md` only.

## 32. Probes executed

See Section 4. All probes were read-only source inspections/searches, plus required diff guardrail commands before commit.

## 33. Confidence statement

Confidence is moderate-high for the immediate ownership seam because implementation bodies and direct tests support the current road and missing handoffs. Confidence is lower for final schema shape because the audit did not implement or exercise a policy projection and repository evidence leaves methodological applicability fields unresolved.

## Required questions answered

1. Actual methodological selector: constitutional view selection, specifically `select_constitutional_views(...)` with its question/capability projections.
2. Exact dimension: exact declared selection keys to exact registered view capability keys.
3. It selects registered constitutional view names; fidelity appears as a view capability key, not internal/external grammar method selection.
4. Fidelity is a selectable read-model view/capability key in that selector; for examination work it would be a constraint or orientation input, not a method/priority in current code.
5. Methodological selection does not currently constrain candidate work generation.
6. It does not constrain frontier classification.
7. It does not constrain work selection because work selection is absent.
8. They are orthogonal.
9. Exact handoff is missing; earliest required is methodological applicability into contract applicability/candidate generation, followed by policy into eligible-work selection.
10. They could compete only in a faulty future design that lets method orientation choose item priority or frontier selection choose lawful method.
11. Examination resolution is currently supplied by campaign author/caller prose/test arrangement.
12. The bounded inquiry can preserve deep-examination prose as testimony but cannot express it as typed executable policy.
13. No typed examination policy exists.
14. Prerequisite relationships can create lawful ordering in principle; current code preserves missing prerequisites/blockers but does not order work.
15. Corpus-coverage policy could create lawful selection only if typed as policy; it is not currently implemented.
16. A selector cannot lawfully choose merely because one item is eligible unless policy says sole eligibility is sufficient.
17. Yes, selection must preserve every non-selected alternative relevant to the selection.
18. Yes, selection can lawfully return no selected item.
19. A typed policy/applicability boundary prevents methodological applicability from becoming priority.
20. Methodological applicability handoff before selection prevents frontier selection from choosing an unlawful method.
21. First missing owner is examination-policy projection.
22. Smallest future handoff: examination-policy projection producer → typed policy artifact → eligible-work selector.
23. It eliminates campaign-author manual responsibility for implicit examination resolution/next-work basis.
24. One bounded implementation slice is warranted.
