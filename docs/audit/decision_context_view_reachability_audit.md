---
doc_type: audit
status: active
domain: implementation reachability
defines:
  - DecisionContextView reachability findings
  - Context Views implementation usage boundary
depends_on:
  - ../seed_runtime/context_views.py
  - ../scripts/seed_local.py
  - ../tests/test_context_views.py
---

# DecisionContextView Reachability Audit

## Scope

This is an implementation reachability audit of `DecisionContextView` and
`seed_runtime/context_views.py`. It does not redesign context, rename symbols,
remove code, reconcile architecture, or propose a new framework.

Required repository-wide searches were run over `seed_runtime/`, `scripts/`,
`tests/`, and `docs/` for:

- `context_views`
- `DecisionContextView`
- `build_decision_context_view`
- `ContextFact`
- `ContextIssue`
- `ContextRequirement`
- `ContextCapability`
- `ContextSummary`
- `decision context`
- `Context Views`

## Files Inspected

- `seed_runtime/context_views.py`
- `scripts/seed_local.py`
- `tests/test_context_views.py`
- `tests/test_intent_classifier.py`
- `tests/test_runtime_loop.py`
- `docs/context_composition_reconciliation.md`
- `docs/capability_ownership_matrix.md`
- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_summary_characterization.md`
- `docs/response_reconciliation.md`
- `docs/runtime_parity_inventory.md`
- `docs/audit/context_knowledge_consolidation.md`

## Usage Found

### Imports

`DecisionContextView` is imported by:

- `scripts/seed_local.py`, where it types the CLI formatter for decision-context
  JSON output.
- `tests/test_runtime_loop.py`, with no further in-file reference found by the
  required symbol search.
- `tests/test_intent_classifier.py`, with no further in-file reference found by
  the required symbol search.

`build_decision_context_view` is imported by:

- `scripts/seed_local.py`, where the `--decision-context` command path calls it.
- `tests/test_context_views.py`, where unit and CLI tests call it.

`ContextFact`, `ContextIssue`, and `ContextSummary` are imported and used by
`tests/test_context_views.py` for expected values and summary assertions.

`ContextCapability`, `ContextFact`, `ContextIssue`, `ContextRequirement`,
`ContextSummary`, and `DecisionContextView` are imported by
`tests/test_intent_classifier.py`, but the required symbol search found no
non-import usage in that file.

### Calls

`build_decision_context_view` is called in production code only by the local CLI
`--decision-context` branch in `scripts/seed_local.py`.

`build_decision_context_view` is called in tests by `tests/test_context_views.py`.

No call to `build_decision_context_view` was found under `seed_runtime/` outside
`seed_runtime/context_views.py` itself.

### Dataclass Usage

Inside `seed_runtime/context_views.py`, the nested dataclasses are used to build
and type the projection:

- `DecisionContextView` contains lists of `ContextFact`, `ContextIssue`,
  `ContextRequirement`, and `ContextCapability`, plus `ContextSummary`.
- `select_context_facts(...)` returns `ContextFact` records.
- `build_context_summary(...)` returns `ContextSummary`.
- private helpers construct `ContextIssue`, `ContextRequirement`, and
  `ContextCapability` records.

Outside `seed_runtime/context_views.py`:

- `ContextFact` and `ContextSummary` are used directly in
  `tests/test_context_views.py` assertions.
- `ContextIssue` is imported by `tests/test_context_views.py`, but the required
  symbol search found no non-import usage in that file.
- `ContextRequirement` and `ContextCapability` had no non-import usage outside
  `seed_runtime/context_views.py`.

### CLI Usage

Context Views are reachable from the local CLI through `--decision-context`:
that branch builds a projected state, calls `build_decision_context_view(...)`,
and prints deterministic JSON using `format_decision_context_view(...)`.

## Usage Not Found

### RuntimeLoop

No current `seed_runtime/runtime_loop.py` file was present in the inspected tree,
and the required searches found no RuntimeLoop implementation call to
`build_decision_context_view` under `seed_runtime/`.

Current tests retain `tests/test_runtime_loop.py`, but that file imports
`DecisionContextView` without a non-import reference found by the required
symbol search. This does not establish current RuntimeLoop use.

### Decision Providers

No current decision-provider implementation under `seed_runtime/` imports or
calls `DecisionContextView` or `build_decision_context_view`.

`seed_runtime/context_views.py` docstrings describe the view as deterministic
DecisionProvider context, but the implementation reachability search found no
provider call path using it.

### CLI Commands Other Than `--decision-context`

No CLI use was found outside the `--decision-context` branch and its formatter in
`scripts/seed_local.py`.

### Only Tests

Context Views are not used only by tests: `scripts/seed_local.py` exposes them
through the `--decision-context` command path. However, the only non-test
reachable use found is CLI inspection output, not RuntimeLoop or provider
execution.

## Tests Covering It

`tests/test_context_views.py` covers:

- construction from projected state;
- deterministic fact ordering and summary counts;
- contradiction and graph issue projection into context issues;
- unsupported-fact exclusion and optional inclusion;
- read-only behavior that does not mutate state or execute runtime behavior;
- CLI `--decision-context` output and its no-runtime/provider/policy/tool
  boundary.

`tests/test_intent_classifier.py` currently asserts that the legacy context
packet prompt does not include `decision_context`. Its Context View imports are
not used by the current test body according to the required symbol search.

`tests/test_runtime_loop.py` imports `DecisionContextView`, but no non-import
usage was found by the required symbol search.

## Docs Claiming It

Documentation claims are mixed:

- `docs/context_composition_reconciliation.md`,
  `docs/selection_rationale_characterization.md`,
  `docs/selection_rationale_summary_characterization.md`, and
  `docs/response_reconciliation.md` accurately describe implemented projection
  behavior in `seed_runtime/context_views.py` at the level of facts, issues,
  requirements, capabilities, summaries, evidence, contradictions, and
  confidence-derived selection.
- `docs/capability_ownership_matrix.md`, `docs/runtime_parity_inventory.md`, and
  `docs/audit/context_knowledge_consolidation.md` claim or preserve RuntimeLoop
  embedding/provider-facing use. Those claims are stale relative to the current
  inspected implementation because no RuntimeLoop implementation file or
  provider call path was found.
- Docs that describe Context Views as read-only derived projections are
  implementation-backed.
- Docs that describe Context Views as currently consumed by RuntimeLoop or
  decision providers are not implementation-backed in the current tree.

## Supported Conclusion

`DecisionContextView` and `build_decision_context_view(...)` are implemented and
tested read-only projections. They are reachable from the current codebase
through the local CLI `--decision-context` inspection command and through tests.
The implementation builds deterministic decision-ready projection data from
projected `State` plus evidence graph, contradictions, confidence, requirements,
and capabilities without runtime/provider/tool/policy execution.

## Unsupported Conclusion

The current codebase does not support the conclusion that Context Views are used
by RuntimeLoop or by decision providers. Existing documentation that says
RuntimeLoop embeds `DecisionContextView` or that providers receive it is stale
with respect to the current implementation reachability findings.
