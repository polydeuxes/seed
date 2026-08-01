# Static constitutional-pipeline deletion 001

## Bounded implementation result

This change deletes the developer-compiled static constitutional-pipeline district recovered by PR 2138. It does not build a replacement pipeline, question entrance, orchestrator, examination CLI, competency, applicability mechanism, policy mechanism, executor, or result-return road.

## Before and after topology

Before:

```text
caller-authored question-shaped artifact
        ├── static constitutional pipeline demonstration
        └── examination-related consumers
```

The deleted branch copied caller question fields and routing tokens into projections, intersected exact tokens with developer-defined capability keys, selected developer-authored Process, Governance, and Fidelity payloads, statically composed them, and wrapped the composition in pipeline, provenance, diagnostic, JSON, and human output.

After:

```text
caller-authored question-shaped artifact
        └── examination-related consumers held out for separate recovery

static constitutional pipeline:
        deleted
```

## Exact deletion manifest

Runtime modules deleted:

- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_view_composition.py`
- `seed_runtime/constitutional_process_view.py`
- `seed_runtime/constitutional_governance_view.py`
- `seed_runtime/constitutional_fidelity_view.py`

Repository-wide consumer searches confirmed that every production consumer of these modules belonged to the same district. No examination module imported any deleted module or component.

CLI flags deleted from `scripts/seed_local.py` are `--constitutional-pipeline`, `--constitutional-pipeline-diagnostic`, `--constitutional-process`, `--constitutional-governance`, `--constitutional-fidelity`, and `--constitutional-view-composition`. District-only input arguments deleted are `--operator-inquiry`, `--inquiry-provenance`, `--bounded-question`, `--constitutional-intent`, `--scope-status`, `--selection-key`, `--pipeline-uncertainty`, `--pipeline-unknown`, and `--composition-purpose`. Their imports, parser declarations, JSON allow-list references, dispatch/rendering branches, and refusal branches were deleted. The deleted flags now fail as unknown arguments and are not redirected.

Diagnostic inventory entries and matching shape-audit implementation specifications deleted are `constitutional_pipeline`, `constitutional_pipeline_diagnostic`, `constitutional_process`, `constitutional_governance`, `constitutional_fidelity`, and `constitutional_view_composition`. General inventory/audit machinery and `examination_frontier` remain.

Read-model ownership cleanup deleted the district-owned `ConstitutionalReadModelContract`, `constitutional_read_model_registration`, and `CONSTITUTIONAL_READ_MODEL_CONTRACTS` machinery, plus registrations for `constitutional_process`, `constitutional_governance`, and `constitutional_fidelity`. Shared read-model registration and construction infrastructure remains.

Static-only tests and fixtures deleted:

- `tests/constitutional_pipeline_test_support.py`
- `tests/test_constitutional_capability_projection.py`
- `tests/test_constitutional_fidelity_view.py`
- `tests/test_constitutional_governance_view.py`
- `tests/test_constitutional_pipeline.py`
- `tests/test_constitutional_pipeline_diagnostic.py`
- `tests/test_constitutional_pipeline_integration_wiring.py`
- `tests/test_constitutional_pipeline_provenance_explanation.py`
- `tests/test_constitutional_pipeline_public_surface.py`
- `tests/test_constitutional_process_view.py`
- `tests/test_constitutional_question_projection.py`
- `tests/test_constitutional_view_composition.py`
- `tests/test_constitutional_view_selection.py`

District-only registration assertions were removed from `tests/test_read_model_ownership.py`. Focused absence tests now prove parser, diagnostic, shape-audit, and registration cleanup while proving only continued availability—not standing or fidelity—of held-out imports.

The active operator guide `constitutional_pipeline_operations.md` was deleted and its active `docs/README.md` navigation entry removed. Numbered implementation, campaign, audit, compatibility, and recovery reports are retained as historical testimony. In particular, `bounded_constitutional_question_complete_topology_recovery_001.md` remains the controlling recovery report. Historical testimony is not active operator documentation.

## Preserved and held-out boundary

`seed_runtime/bounded_constitutional_question.py` and its tests are unchanged. `BoundedConstitutionalQuestion`, `produce_bounded_constitutional_question(...)`, and all current fields remain unchanged because examination modules consume the artifact; their disposition remains unresolved.

The following examination implementation files and their tests, diagnostics, formatters, schemas, and documentation are unchanged:

- `seed_runtime/examination_frontier.py`
- `seed_runtime/candidate_examination_work.py`
- `seed_runtime/examination_method_applicability.py`
- `seed_runtime/examination_policy_projection.py`
- `seed_runtime/examination_work_selection.py`
- `seed_runtime/examination_probe_request.py`

The examination artifacts were excluded from this deletion because they fall outside the independently proven static-pipeline district. This exclusion is not a finding that they are faithful, necessary, evidence-derived, reachable end-to-end, or worthy of permanent retention.

Import and repository-wide symbol searches prove no examination module depended on a deleted component. The patch adds no replacement pipeline or question entrance and makes no examination implementation change. No malformed external-input behavior is frozen in a new test.

## Required distinctions

- held out from one deletion != constitutionally preserved
- implemented Python API != active runtime demand
- test coverage != independent consumer
- CLI presence != lawful responsibility
- registration != constitutional warrant
- static view != examination
- exact token matching != applicability
- composition != comparison or finding
- request construction != execution
- absence of an executor != authorization to invent one
- deleting fake code != implementing real code
- historical testimony != active operator documentation

## Remaining contaminated examination-road boundary

The final boundary remains unresolved: `ExaminationFrontier` is operator-reachable but begins with raw JSON construction; method applicability, policy, and selection are implemented and callable without a recovered CLI or runtime ingress; and probe request remains a representation endpoint with no recovered executor or result-return road. The next independent recovery concerns examination ingress, reachability, supplied standing, and the malformed external-input boundary.
