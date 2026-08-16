# Agent Instructions

These instructions apply to automated agents and future coding sessions working in this repository.

## Operational visibility contract

Visibility is part of the work, not a follow-up.

If a change adds or modifies any diagnostic, audit, probe, view, operational CLI flag, or recordable output:

- Update the diagnostic inventory registry.
- Update the diagnostic shape-audit implementation specs.
- Add or update tests proving the surface appears in `seed --diagnostic-inventory`.
- Add or update tests proving the surface is checked by `seed --diagnostic-shape-audit`.
- If it supports `--record`, prove `record_scope=diagnostic_run` unless intentionally different.
- If it writes the event ledger, prove `mutates_cluster=false` unless intentionally operational.
- Run `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`.

New operational surfaces should not be invisible.

## Diagnostic recording boundary

Diagnostic findings must not silently become cluster truth.

When recording diagnostic output:

- Prefer `diagnostic_run:<id>` scoped subjects.
- Do not attach diagnostic-only findings directly to hosts, services, filesystems, or runtime entities unless the task explicitly changes that boundary.
- Distinguish event-ledger writes from cluster mutation.
- Preserve `mutates_cluster=false` for read-only diagnostics.

## Presentation vocabulary is not automatically knowledge

Do not assume presentation vocabulary is repository knowledge.

Terms such as:

- continuation
- current work position
- source navigation
- active edge
- storage topology
- state build
- projection cache

may exist only as visibility or presentation labels.

Use implementation evidence, such as `seed --knowledge-reachability-audit`, before promoting presentation vocabulary into preserved or projected knowledge.

## Work style

Prefer code and tests over papers.

When the task is operational:

- Identify the failing command, behavior, or visibility gap.
- Make the smallest implementation-backed change.
- Add tests that preserve the behavior.
- Avoid creating new conceptual documents unless explicitly requested.

Repository authority wins over these instructions when implementation evidence disagrees.
