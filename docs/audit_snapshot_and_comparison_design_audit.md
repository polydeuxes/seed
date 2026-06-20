# Audit Snapshot and Comparison Design Audit

## Status

Exploratory design audit.

This document captures an operational pressure discovered while repeatedly running Seed diagnostics and audits. It does not implement snapshot storage, define new ontology, or change diagnostic behavior.

Repository authority wins over this audit.

## Problem

Seed diagnostics and audits currently produce valuable point-in-time output, but the output is usually transient.

Operators run commands such as:

```bash
seed --ownership-discrepancies --json > ownership.json
seed --knowledge-reachability-audit --knowledge-reachability-audit-json > reachability.json
seed --observation-inventory --json > observations.json
seed --diagnostic-inventory --json
seed --diagnostic-shape-audit --json
```

Those files are only preserved if the operator remembers to redirect and save them.

When a later change affects observations, diagnostics, ownership inference, capability needs, or reachability, the before state may be gone.

That prevents Seed from answering:

```text
What changed?
Which audit rows appeared?
Which audit rows disappeared?
Did a new observation improve ownership diagnostics?
Did a commit introduce new observation predicates?
Did capability needs decrease after adding an observation?
```

The operator is currently performing this comparison manually.

## Observed examples

Recent work exposed this repeatedly:

- `ownership.json` was not saved before local listener observations were added, so before/after comparison became manual or impossible.
- `reachability.json` was saved manually and later used to identify candidate-kind noise, visibility-only rows, and tokenization pressure.
- Observation inventory output showed listener predicates were absent before local listener observations were added.
- Diagnostic inventory and diagnostic shape audit created visibility surfaces, but their outputs are still transient unless manually captured.
- Git commits and PRs contain important context for why audit output changed, but audit output is not currently tied to commit identity.

## Current operator workflow

```text
run diagnostic or audit
redirect JSON manually
remember where it was saved
make a code or observation change
rerun diagnostic or audit
manually compare files
manually inspect git history
manually infer what changed
```

This is fragile and easy to forget.

## Design pressure

Seed is gaining operational diagnostics that are intended to guide future action.

If those diagnostics are not saved with enough context to compare across time, Seed cannot use its own audit history.

This creates pressure for a first-class audit snapshot surface.

## Candidate operational model

A snapshot command could run or ingest selected audit outputs and save them under a stable local artifact directory.

Example commands:

```bash
seed --audit-snapshot ownership_discrepancies
seed --audit-snapshot observation_inventory
seed --audit-snapshot diagnostic_inventory
seed --audit-snapshot diagnostic_shape_audit
seed --audit-snapshot knowledge_reachability
```

Possible output location:

```text
.audit/seed/YYYY-MM-DDTHHMMSSZ/
  metadata.json
  ownership_discrepancies.json
  observation_inventory.json
  diagnostic_inventory.json
  diagnostic_shape_audit.json
  knowledge_reachability.json
  git.json
```

The exact location is intentionally undecided.

## Snapshot metadata

A snapshot should preserve enough context to explain why output changed later.

Potential metadata:

```text
timestamp
command
arguments
seed database path or identifier
seed database event count or latest event id
repository branch
repository commit
git dirty status
changed files
Seed projection version
snapshot format version
```

Git metadata is important because many audit changes are caused by code changes, not cluster changes.

## Comparison surface

A comparison command could compare two saved snapshots.

Example:

```bash
seed --audit-compare latest previous --kind ownership_discrepancies
seed --audit-compare latest previous --kind observation_inventory
```

Potential comparison questions:

```text
Which rows were added?
Which rows were removed?
Which rows changed confidence?
Which conflicts resolved?
Which capability needs appeared or disappeared?
Which observation predicates appeared?
Which diagnostics changed shape?
Which candidate kinds changed reachability?
```

## Boundary questions

The repository needs an implementation decision before this becomes code.

Open questions:

```text
Are audit snapshots repository artifacts, local runtime artifacts, event-ledger events, or diagnostic facts?
Should snapshots ever be committed to git?
Should snapshots be ignored by git by default?
Should snapshots be tied to workspace id, database path, or repository commit?
Should snapshot comparison be generic JSON diff or diagnostic-specific comparison?
Should snapshots be created by running diagnostics or by capturing already-produced JSON?
Should recording diagnostic facts and saving audit snapshots remain separate mechanisms?
```

## Suggested boundary

Initial implementation should probably treat snapshots as local operational artifacts, not repository knowledge and not cluster truth.

A conservative first boundary:

```text
.audit/seed/ is local artifact storage.
Snapshots are not facts.
Snapshots are not diagnostic-run facts.
Snapshots do not change cluster state.
Snapshots can include diagnostic JSON and git metadata.
Comparison reads snapshots and reports differences.
```

If this path is chosen, `.audit/` should likely be gitignored unless the operator explicitly wants to preserve a snapshot as a fixture.

## Relationship to diagnostic facts

Diagnostic-run-scoped facts remain useful for queryable diagnostic findings inside Seed.

Audit snapshots solve a different problem:

```text
diagnostic facts
  answer: what findings has Seed recorded?

audit snapshots
  answer: what did this audit output look like at a point in time?
```

They should not be collapsed by default.

## Relationship to git visibility

Snapshot metadata should include git context because audit output often changes when code changes.

Potential `git.json` fields:

```json
{
  "branch": "main",
  "commit": "...",
  "dirty": false,
  "changed_files": []
}
```

A later comparison could say:

```text
observation_inventory changed
new predicates: listening_socket, listener_port, listener_protocol
between commits: <old> -> <new>
changed files: seed_runtime/local_host_observations.py, predicate catalog tests
```

That would let Seed connect operational visibility changes to repository changes.

## Non-goals

Do not use this design to:

```text
create ontology
promote audit rows into facts
replace diagnostic-run recording
make snapshots cluster truth
build a general database migration system
write another reconciliation branch
```

## Implementation sketch

A future implementation could start small:

1. Add `seed --audit-snapshot <kind>` for one or two existing JSON-capable diagnostics.
2. Save JSON output plus `metadata.json` under `.audit/seed/<timestamp>/`.
3. Add `.audit/` to `.gitignore` unless repository policy says otherwise.
4. Add `seed --audit-snapshots` to list saved snapshots.
5. Add `seed --audit-compare <a> <b> --kind observation_inventory` for one structured comparison.
6. Extend only after a real before/after workflow proves useful.

Good first comparison target:

```text
observation_inventory
```

because it has stable provider/predicate/family summaries and directly supports the question:

```text
What new observation visibility did this change add?
```

Good second target:

```text
ownership_discrepancies
```

because it can show whether new observations reduce `insufficient_evidence` or change capability needs.

## Acceptance shape for future work

A future implementation should let an operator run:

```bash
seed --audit-snapshot observation_inventory
# make a change
seed --audit-snapshot observation_inventory
seed --audit-compare latest previous --kind observation_inventory
```

and receive a clear answer about what changed without manually saving JSON files.

## Current conclusion

Seed needs a way to preserve and compare its own audit outputs.

This should be treated as an operational memory and comparison surface, not as new cluster knowledge.

The immediate value is reducing operator memory burden and allowing Seed to participate in its own before/after validation loop.