# Test Suite Contamination and Failure Recovery 001

## Scope

This is one bounded, report-only recovery on current merged `main` after PR 1932.  No production code, tests, fixtures, documentation families other than this report, Book content, CI configuration, package exports, CLI behavior, or repository structure were changed.

The governing distinction for this pass is that the present suite result is evidence about current executable tests only.  A green local run does not prove the suite is uncontaminated, and a reported red history across prior PRs does not prove current production regressions.

Repository head inspected:

```text
bf15ba0 Archive removed PR 1932 docs (#1932)
0a01e62 Excise conversational input classifier (#1931)
eb5cda7 Correct Fidelity production ownership (#1930)
fd0adf3 Excise Book VII operational topic collection (#1929)
68443aa Add internal external grammar recovery report (#1928)
```

Active standing witnesses used for this pass include:

- `docs/architecture_principles.md`, which says current core is state reasoning, capability reasoning, knowledge projection, and explanation, and that `RuntimeLoop`, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` are not current-core architecture.
- `docs/archive/original_book_of_seed/03-runtime-loop.md`, which says the original runtime-loop chapter is historical testimony only and must not preserve compatibility obligations for deleted planning, handoff, proposal, authorization, pending-action, or builder-candidate roads.
- current tests and producers under `tests/` and `seed_runtime/`.

## Current Suite Result

Local Python runtime result:

```text
pytest -q
2017 passed in 454.17s (0:07:34)
```

Collection result:

```text
pytest --collect-only -q
2017 tests collected in 2.10s
```

Recovered counts from the two local commands:

```text
total collected: 2017
passed: 2017
failed: 0
errors during collection: 0
skipped: 0
xfailed: 0
xpassed: 0
```

Complete failure summary preservation: there was no local failure summary because the suite passed.

GitHub Actions inspection: not recoverable in this checkout.  `gh run list --limit 10 --json ...` failed with `/bin/bash: line 1: gh: command not found`, and this repository checkout has no configured Git remote (`git remote -v` returned no remotes).  Therefore Python 3.11 / 3.12 CI job logs could not be inspected from local repository metadata during this bounded operation.

CI distinction status:

```text
shared failures: none observed locally; CI unavailable
version-specific failures: unknown; CI unavailable
including Python 3.11: unknown; CI unavailable
including Python 3.12: unknown; CI unavailable
environment-only failures: unknown; CI unavailable
collection failures: none observed locally
assertion failures: none observed locally
```

## Exact Failure Ledger

No failing or erroring tests were recovered from current merged `main` in the local available Python runtime.

Because there were no failures, no failing test has a missing symbol/path/content ledger entry, and no failure receives classifications A-H.  The appropriate current disposition for the empty failure ledger is `preserve` for the fact of the green local result, not for every passing test's architecture.

## Failure Families

No current local failure families were recovered.

Important negative findings:

- No collection failures were observed.
- No assertion failures were observed.
- No import-time failures were observed.
- The reported history that the suite remained red for approximately the last 100 PRs is not reproduced at current head in this runtime.  That history remains relevant as background testimony, but it is not an active failure ledger for this checkout.

## Passing Contamination Ledger

The following passing tests or coherent families are high-confidence contamination candidates or mixed-standing families.  They should not be treated as ordinary faithful coverage merely because they pass.

### 1. Candidate operational realization and future-handoff chain

- tests:
  - `tests/test_candidate_operational_realization.py`
  - `tests/test_capability_reachability_projection.py`
  - `tests/test_operational_realization_warrant.py`
  - related `operational_realization*` and `capability_reachability*` tests found by search.
- protected structure:
  - `OperationalRealizationHandoff`, candidate operational realization sets, reachability projections, selection handoffs, warrant handoffs, and future egress translation handoffs.
  - Tests explicitly protect future handoff fields and absence of `execution_proposal`, `pending_action`, argv/stdin/cwd/environment, and authorization vocabulary.
- why passing is not evidence of fidelity:
  - The tests prove constructibility and internal shape stability of a staged operational-realization pipeline.  They do not by themselves prove that the staged future-handoff/warrant chain has current constitutional standing or a production consumer.
  - `tests/test_operational_realization_warrant.py` constructs synthetic fixtures with `source:fixture`, `internal:repo_search`, `/bin/search*`, and future handoff objects; that can protect a fixture road rather than a runtime road.
- current standing:
  - Mixed.  Active architecture still includes capability reasoning and provider/handoff recommendations, but current architecture also warns that old planning/handoff/proposal/authorization roads are not current-core.  The active witness supports capability-gap reasoning; it does not automatically support every future handoff and warrant seam in this family.
- historical witness:
  - These files entered at `8bffc1e Recover selection producer acts (#1831)`.  PRs after that deleted or quarantined adjacent execution/proposal/tool corridors, including `8724503 Excise Seed-owned tool execution corridor (#1882)`, `b943e2d Excise execution proposal authorization island (#1915)`, and `0a01e62 Excise conversational input classifier (#1931)`.
- likely disposition:
  - `split_mixed_test` for tests that combine real capability reasoning with future-handoff scaffolding.
  - `rewrite_to_current_witness` only where the existing current witness is capability reasoning / provider recommendation in `docs/architecture_principles.md` and active `seed_runtime` consumers.
  - `delete_as_stale` or `delete_with_excised_family` for pure future-handoff seams that lack a current consumer after history inspection.

### 2. Candidate request and candidate route preservation surfaces

- tests:
  - `tests/test_candidate_requests.py::test_state_summary_input_preserves_high_confidence_state_summary_candidate`
  - `tests/test_candidate_requests.py::test_generic_summary_input_preserves_multiple_summary_candidates`
  - `tests/test_candidate_requests.py::test_ambiguous_summary_preserves_ambiguity_instead_of_selecting_one`
  - `tests/test_candidate_requests.py::test_candidate_request_inspection_does_not_perform_downstream_authority_steps`
  - `tests/test_candidate_requests.py::test_candidate_requests_cli_is_read_only_and_does_not_build_runtime`
  - `tests/test_candidate_requests.py::test_state_summary_input_preserves_routed_state_summary_candidate`
  - `tests/test_candidate_requests.py::test_generic_summary_input_preserves_multiple_routed_candidates`
  - `tests/test_candidate_requests.py::test_ambiguity_survives_candidate_routing`
  - `tests/test_candidate_requests.py::test_candidate_routing_does_not_perform_downstream_authority_steps`
- protected structure:
  - Conversational candidate request inspection, candidate route preservation, label-to-route surfaces, and read-only CLI outputs.
- why passing is not evidence of fidelity:
  - These tests preserve summary-intent candidates and routed candidates after PR 1931 excised the conversational input classifier.  The family is careful to say it does not execute, select capability, or build runtime, but it still protects a conversational-classification/routing-adjacent surface.
- current standing:
  - Mixed to contaminated.  Read-only diagnostics can be current if listed in diagnostic inventory and shape audit.  However, the request/route naming and summary candidate mapping look like surviving scaffolding around excised conversational application architecture unless a current diagnostic or consumer proves otherwise.
- historical witness:
  - `git log -- tests/test_candidate_requests.py` shows the file was touched by `5d0f034 Excise generic conversational application district (#1912)`, `398b539 Restore independent excision test witness (#1883)`, `8724503 Excise Seed-owned tool execution corridor (#1882)`, and originally by `8bffc1e Recover selection producer acts (#1831)`.
- likely disposition:
  - `split_mixed_test` if the CLI is a registered diagnostic with shape-audit standing.
  - `delete_with_excised_family` for candidate-routing responsibilities that survive only as anti-execution scaffolding after classifier/router excision.

### 3. Knowledge reachability audit fixture vocabulary

- tests:
  - `tests/test_knowledge_reachability.py::test_reachability_detects_first_loss_at_projection_for_preserved_only_concept`
  - `tests/test_knowledge_reachability.py::test_reachability_integration_fixture_finds_distinct_loss_stages`
  - related table/json tests that include presentation labels such as `source navigation`, `current work position`, `storage topology`, `state build`, and `projection-cache`.
- protected structure:
  - A diagnostic that distinguishes preserved, projected, read-model, and rendered reachability stages and classifies presentation labels.
- why passing is not evidence of fidelity:
  - The family intentionally uses presentation labels and fixture documents to prove that visibility vocabulary is not automatically knowledge.  Passing proves the guardrail exists, not that those labels are active repository ontology.
- current standing:
  - Mostly faithful diagnostic guardrail, but with contamination risk if later maintainers treat the fixture terms as active requirements.  The user-provided AGENTS.md explicitly names these terms as presentation labels requiring implementation evidence before promotion.
- historical witness:
  - `git log -- tests/test_knowledge_reachability.py` shows `0a01e62 Excise conversational input classifier (#1931)` and `8bffc1e Recover selection producer acts (#1831)`.
- likely disposition:
  - `preserve` for the audit's boundary behavior.
  - `rewrite_to_current_witness` if fixture terms become mistaken for production concepts; current witness is the diagnostic's classification of presentation labels, not the labels themselves.

### 4. Legacy decision vocabulary compatibility tests and reports

- tests:
  - No current `tests/test_runtime_loop.py` exists in this checkout, but `docs/legacy_decision_vocabulary_reconciliation.md` records prior tests preserving `DecisionModel`, `FakeDecisionModel`, `ContextComposer`, `ContextPacket`, and `last_context` compatibility.
  - Search still finds model/decision/context vocabulary in current docs and implementation surfaces.
- protected structure:
  - Compatibility aliases and serialized/event vocabulary from the model-decision era.
- why passing is not evidence of fidelity:
  - Compatibility aliases can be intentional for a window, but compatibility is not responsibility.  Tests that assert alias existence without a current public consumer can freeze deleted architecture.
- current standing:
  - Historical/mixed.  The reconciliation document itself says some aliases were intentionally retained, but also frames them as compatibility surfaces and future cleanup candidates rather than preferred architecture.
- historical witness:
  - The reconciliation was added at `8bffc1e Recover selection producer acts (#1831)` and later touched by excision commits including `cdf5109 Excise internal model decision residue (#1869)`, `a443c63 Delete model client decision prompt stack (#1875)`, `1c9e619 Delete withdrawn model context pipeline (#1879)`, and `77ba23d Archive original numbered Seed corpus (#1921)`.
- likely disposition:
  - `rewrite_to_current_witness` for tests that protect current serialized public compatibility with explicit consumers.
  - `delete_as_stale` for alias-only tests after the compatibility window closes or if no consumer is found.

### 5. Excision-witness tests for deleted runtime roads

- tests:
  - `tests/test_events.py::test_sqlite_persisted_id_prefixes_exclude_deleted_planning_artifacts`
  - `tests/test_capability_verification_invariants.py::test_active_invariants_do_not_preserve_deleted_runtime_roads`
  - `tests/test_capability_verification_invariants.py::test_active_architecture_doc_does_not_claim_deleted_runtime_pipeline`
  - `tests/test_constitutional_pipeline_*::test_cli_raw_pipeline_ingress_is_removed`
- protected structure:
  - Negative witnesses proving deleted roads remain absent from active docs, events, and CLI surfaces.
- why passing is not evidence of fidelity:
  - These tests are currently useful as deletion witnesses, but they can become contaminated if they require exact names of every deleted artifact forever, or if they turn excision history into active architecture.
- current standing:
  - Mostly faithful for now because active architecture explicitly says the deleted roads are not current-core.  The risk is over-specific stale enumeration.
- historical witness:
  - `tests/test_events.py` was touched by `b943e2d Excise execution proposal authorization island (#1915)` and `4c905af Clean active witness and stale runtime docs (#1919)`.  `tests/test_capability_verification_invariants.py` was touched by `8724503`, `1883`, `1884`, `1919`, `1920`, and `1921` cleanup/archive commits.
- likely disposition:
  - `preserve` while they protect active absence boundaries.
  - `rewrite_to_current_witness` if they become a stale deleted-name catalog rather than checking the current architecture document and inventory surfaces.

## Faithful Test Families

The following important surviving families appear to protect real current responsibilities and should not be swept away merely because the repository has a red-suite history or carries old vocabulary.

- Diagnostic inventory and shape audit tests: these protect the operational visibility contract and should remain authoritative for diagnostic surfaces.
- Knowledge reachability audit tests: despite risky fixture vocabulary, the family directly protects the distinction between preservation, projection, read model, rendering, and presentation labels.
- State projector, state views, temporal characterization, relationship catalog, evidence/fact, observation ingestion, and source navigation tests: these align with the active core loop from Observation through Evidence, Fact, State Projection, Explanation, and capability reasoning.
- Capability inventory, capability candidates, capability promotion readiness, and provider/catalog tests: these align with capability reasoning and provider/handoff recommendations, provided they do not reintroduce execution/proposal/authorization roads.
- Negative excision/invariant tests that prove removed runtime roads are absent from active architecture and CLI surfaces: these should remain until a smaller current witness replaces exact historical-name assertions.

## Unknowns

- CI Python 3.11 and 3.12 results could not be inspected because the GitHub CLI is unavailable and this checkout has no remote configured.  Shared vs version-specific CI failures therefore remain unknown.
- A comprehensive per-test passing contamination classification was not attempted; this pass reports only high-confidence families with meaningful evidence.
- Some mixed families may have active consumers in `seed_runtime` that warrant narrower preservation.  Before deletion, use `rg`, `git log -S`, `git log -G`, and direct consumer inspection for the exact class/function under consideration.
- The absence of current failures means the requested per-failure classifications cannot be populated without inventing failures.  They are intentionally empty.

## Recommended Cleanup Order

1. Preserve the green local suite result as current evidence, and do not delete tests merely because they are old or because prior PRs reportedly had red suites.
2. First isolate pure compatibility aliases and deleted-name catalogs from tests that protect current serialized public behavior.  Delete only alias-only tests with no current consumer.
3. Split operational-realization / reachability / warrant tests into current capability-reasoning witnesses versus future-handoff scaffolding witnesses.  Keep current capability reasoning; delete or rewrite pure future-handoff seams that lack current consumers.
4. Review candidate request/route tests against diagnostic inventory and shape audit.  Preserve registered read-only diagnostics; delete candidate-routing scaffolding that only survives as a residue of excised conversational classifier architecture.
5. Keep knowledge reachability tests, but prevent fixture presentation labels from becoming active ontology.  If needed, rewrite fixture terms to explicitly assert `presentation_label` standing.
6. Keep negative excision tests while deleted runtime roads remain a live absence boundary.  Later, reduce exact historical enumerations to current architecture/inventory witnesses.
7. Only after these separations, remove stale tests in small families.  Do not propose or create replacement architecture to save contaminated tests.

## Central Finding

Current merged `main` after PR 1932 is locally green: `2017 passed`, `2017 collected`, with no local failures or collection errors.  The actionable contamination is therefore in passing tests, not in a current failing ledger.  The highest-risk passing families are mixed tests around operational-realization/future-handoff scaffolding, candidate request/route preservation after conversational classifier excision, and compatibility aliases or deleted-name witnesses that can freeze excised architecture.  Faithful witnesses still exist and should be protected: diagnostic inventory/shape audit, knowledge reachability as a guardrail, state/evidence/projection/explanation behavior, capability reasoning, and current negative tests proving deleted runtime roads remain absent.
