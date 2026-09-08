# Disconnected Examination Staging Chain Deletion 001

## Disposition

This change deletes the complete disconnected examination staging district. Repository-wide producer and consumer searches classified the references as follows: the five runtime modules referenced one another inside the deletion district; the five dedicated tests manually assembled the stages; the static-pipeline deletion test was the only shared test reference; there was no active runtime consumer, CLI consumer, diagnostic consumer, registration, or package export; the Book of Seed chapter was the sole active documentation advertising the implementation; and all other Markdown matches were historical reports or unrelated uses of generic selection, policy, applicability, or probe vocabulary.

## Exact implementation deletion

The runtime modules deleted are:

- `seed_runtime/candidate_examination_work.py`
- `seed_runtime/examination_method_applicability.py`
- `seed_runtime/examination_policy_projection.py`
- `seed_runtime/examination_work_selection.py`
- `seed_runtime/examination_probe_request.py`

The classes deleted are `CandidateExaminationWorkError`, `RepresentationVisibility`, `BoundedCorpusMember`, `ExaminationWorkContract`, `CandidateExaminationWorkRecord`, `CandidateExaminationWorkSet`, `ExaminationMethodApplicabilityError`, `ExaminationMethodApplicabilityTestimony`, `CandidateMethodApplicabilityRecord`, `ExaminationMethodApplicabilityProjection`, `ExaminationPolicyProjectionError`, `ExaminationResolutionTestimony`, `ExaminationPolicySelectorHandoff`, `ExaminationPolicyProjection`, `ExaminationWorkSelectionError`, `NonSelectedEligibleWork`, `FutureProbeRequestHandoff`, `ExaminationWorkSelection`, `ExaminationProbeRequestError`, and `ExaminationProbeRequest`.

The public production, adapter, serialization, and formatting functions deleted are `project_candidate_examination_work`, `candidate_examination_work_json`, `format_candidate_examination_work`, candidate-work `input_from_json_dict`, `project_examination_method_applicability`, `examination_method_applicability_json`, `format_examination_method_applicability`, `project_examination_policy`, `examination_policy_projection_json`, `format_examination_policy_projection`, `select_examination_work`, `examination_work_selection_json`, `format_examination_work_selection`, `bind_examination_probe_request`, `examination_probe_request_json`, and `format_examination_probe_request`. Their private validation, tuple-normalization, stable-ID, handoff-ID, and selected-work helpers, constants, state grammars, boundary notes, adapters, and conventions were deleted with their owning modules.

In particular, both future-facing seams were deleted: `ExaminationPolicySelectorHandoff` and `FutureProbeRequestHandoff`. Neither a stranded selector input nor a handoff to the deleted probe binder remains.

## Tests and active surfaces

The dedicated test modules deleted are:

- `tests/test_candidate_examination_work.py`
- `tests/test_examination_method_applicability.py`
- `tests/test_examination_policy_projection.py`
- `tests/test_examination_work_selection.py`
- `tests/test_examination_probe_request.py`

`tests/test_static_constitutional_pipeline_deletion.py` was narrowed so its importability assertion covers only the intentionally held-out `BoundedConstitutionalQuestion` and `ExaminationFrontier`. It now also verifies that the five disconnected staging modules are absent. No other shared test required cleanup, and `tests/test_public_exports.py` does not exist in this checkout.

The deleted modules had no package exports, CLI flags or dispatch, active registration, diagnostic-inventory entry, diagnostic-shape specification, question-surface registration, or read-model-ownership entry, so none were removed from those surfaces. Searches of those surfaces confirm their continued absence. The `examination_frontier` diagnostic inventory and shape-audit registrations remain unchanged.

The active Book of Seed examination chapter no longer cites deleted runtime modules or presents their staged occurrences as current repository implementation. Historical reports remain intact, including:

- `deep_corpus_examination_capability_topology_audit_001.md`
- `candidate_examination_work_projection_slice_001.md`
- `examination_work_selection_topology_audit_001.md`
- `examination_method_applicability_projection_slice_001.md`
- `examination_policy_projection_slice_001.md`
- `examination_work_selection_slice_001.md`
- `examination_probe_request_execution_proposal_topology_audit_001.md`
- `examination_probe_request_binding_slice_001.md`
- `operational_realization_topology_audit_001.md`
- `representation_invocation_grammar_topology_audit_001.md`
- `examination_topology_and_standing_recovery_001.md`

Related implementation, topology, recovery, survey, and deletion reports found by the required searches were likewise retained as historical testimony.

## Historical chronology

Remote history supplies historical testimony, not constitutional authority:

```text
1636 through 1644:
    staged district constructed

1936:
    downstream operational-realization continuation deleted

2142:
    current topology proves the surviving chain is test-assembled
    and absent from the operator road

2143:
    disconnected staging chain deleted
```

## Before and after topology

Before:

```text
operator-reachable road:

external JSON
→ raw question construction
→ direct frontier CandidateWork construction
→ ExaminationFrontier
→ rendering


disconnected staged road:

caller corpus/contracts
→ CandidateExaminationWorkSet
→ supplied applicability testimony
→ MethodApplicabilityProjection
→ supplied resolution testimony
→ ExaminationPolicyProjection
→ WorkSelection
→ FutureProbeRequestHandoff
→ ExaminationProbeRequest
→ no operational consumer
```

After:

```text
operator-reachable road:

external JSON
→ raw question construction
→ direct frontier CandidateWork construction
→ ExaminationFrontier
→ rendering


disconnected staged road:

deleted
```

> The examination frontier was excluded from this deletion because it is the only current operator-reachable examination district. This exclusion is not a finding that the frontier is faithful, evidence-derived, properly named, constitutionally warranted, or worthy of permanent retention. Its raw JSON ingress and supplied-status grammar remain separate recovery subjects.

## Held boundaries and validation

`seed_runtime/examination_frontier.py` and `seed_runtime/bounded_constitutional_question.py` are unchanged. No malformed-input repair, raw JSON validation, new question producer, replacement adapter, compatibility wrapper, tombstone, or replacement examination chain was introduced. Existing raw `TypeError` or `AttributeError` behavior was neither changed nor frozen in a new test.

Focused tests: 207 passed, covering the held-out frontier and bounded question, deletion assertions, diagnostic inventory and shape audit, question-surface inventory, and read-model ownership. The requested `tests/test_public_exports.py` was omitted because it does not exist in this checkout.

Full suite: 1877 passed in 355.89 seconds.

The next unresolved district is the operator-facing frontier: raw external JSON ingress, caller-authored question origination, caller-supplied corpus and work classifications, the malformed-input boundary, and actual independent demand for the frontier. This change does not recover or repair that district.
