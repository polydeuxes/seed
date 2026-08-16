# Knowledge Reachability Inquiry Discipline Reconciliation

## Command outputs reviewed

Captured observable behavior before inspecting implementation by running:

```bash
python scripts/seed_local.py --knowledge-reachability-audit > /tmp/kr.txt
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json > /tmp/kr.json
```

The local container does not expose a `seed` executable on `PATH`, so the repository CLI entrypoint was invoked through `python scripts/seed_local.py`.

Observed text output shape:

- Title: `Knowledge Reachability Audit`.
- Timing sections for `load_state`, `discover_candidates`, `build_indexes`, `evaluate`, `render`, and index subphases.
- Candidate counts: `raw_seen: 126`, `used: 115`, `limit: 500`, `evaluated: 115`, `skipped: 0`.
- Candidate kinds: `presentation_label: 51`, `relationship_label: 1`, `repository_concept: 2`, `runtime_value: 2`, `unknown: 59`.
- Loss stages: `not_preserved: 115`.
- A row table with `Family`, `Kind`, `Candidate`, `Preserved`, `Projected`, `Read Model`, `Inquiry Orientation`, `Rendered`, and `First Loss`.

Observed JSON output shape:

- Top-level object with `metadata` and `rows`.
- `metadata` includes algorithmic counters, cache state, candidate counts, candidate kind counts, candidate sources, indexes, loss stage counts, scan counts, timing, truncation state, limit, max seconds, and reason.
- `rows` contains the same per-candidate fields as the human table: `family`, `candidate_kind`, `candidate`, `preserved`, `projected`, `read_model`, `inquiry_orientation`, `rendered`, and `first_loss`.

## Files inspected

- `seed_runtime/knowledge_reachability.py`
- `scripts/seed_local.py`
- `tests/test_knowledge_reachability.py`
- `tests/test_knowledge_reachability_cache.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Reconciliation

### 1. Bounded implementation-backed question

The diagnostic answers this bounded question:

> For discovered candidate strings, are the strings reachable in preserved event payload/kind terms, projected state terms, read-model terms, inquiry-orientation terms, and rendered visibility, and what is the first loss stage?

This is backed by the row schema, which stores only family, candidate kind, candidate string, five booleans, and first loss. The builder discovers candidates, builds indexes, evaluates each candidate against those indexes, and appends one row per evaluated candidate.

The diagnostic does **not** answer whether a concept is architecturally important, should be promoted to knowledge, or should be redesigned. Candidate families and kinds are local classifications used to bound and summarize the audit, not proof of broader repository intent.

### 2. Reasoning that exists before presentation

Implementation-backed reasoning exists before either CLI formatter runs:

- **Projection loading:** the audit projects ledger state once through `StateProjector(ledger).project(workspace_id)` and also lists workspace events.
- **Candidate discovery:** candidates are discovered from default seeds, event payloads, projected state, source-navigation terms, `docs/`, and `seed_runtime/`, with source budgets, global limits, subject filtering, family filtering, and candidate-kind filtering.
- **Index construction:** `_build_indexes` constructs preserved, projected, read-model, and inquiry term indexes.
- **Reachability computation:** `_candidate_flags_from_indexes` computes the stage booleans for each candidate from the indexes.
- **Aggregation:** metadata records timings, candidate counts, candidate-kind counts, loss-stage counts, algorithmic counters, candidate sources, scan counts, cache state, and index timings.
- **Boundaries:** limits, `--all`, subject selection, family selection, candidate-kind selection, and max-second truncation bound the diagnostic before rendering.

### 3. Human CLI output versus JSON output versus implementation

The human CLI output does not introduce separate knowledge. It projects already-computed rows and metadata.

The CLI first builds `result = build_knowledge_reachability_audit_result(...)`. After ledger cleanup, it chooses JSON rendering when `--knowledge-reachability-audit-json` is set, otherwise it calls the text table formatter. Both branches consume `result.rows` and `result.metadata`.

The text formatter turns row fields into labels, yes/no strings, and a width-padded table. The JSON formatter serializes the same rows with `asdict(row)` and attaches serialized metadata.

The only observed CLI distinction is projection form:

- Text output converts booleans into `yes`/`no`, adds section labels, and orders columns for people.
- JSON output preserves booleans and metadata fields for machine use.

### 4. Where reasoning terminates

Reasoning terminates at `KnowledgeReachabilityAuditResult`:

- `rows` contain computed per-candidate audit facts.
- `metadata` contains computed summary, timing, count, source, scan, cache, truncation, and boundary information.

After the result object is returned, the remaining work is serialization or formatting. The `render` timer phase is present but does not compute additional rows or metadata.

### 5. Where presentation begins

Presentation begins at `format_knowledge_reachability_table` and `knowledge_reachability_json`, and at the CLI branch that chooses which formatter to call.

The text formatter supplies human labels (`Knowledge Reachability Audit`, `Timing`, `Candidates`, `Candidate Kinds`, `Loss Stages`), converts booleans with `_yes`, lays out columns, and optionally prints truncation. The JSON formatter serializes dataclasses and adds compatibility aliases in metadata (`timing`, `candidates`).

### 6. Composition or local reasoning

The diagnostic has one local responsibility: evaluate candidate-string reachability across a fixed sequence of local surfaces.

It does compose inputs from existing repository subsystems and surfaces:

- event ledger events,
- state projection,
- state facts, observations, entities, relationships, and fact supports,
- source-navigation-like terms derived from fact supports with `defines` and `imports`,
- inquiry orientation output,
- repository files under `docs/` and `seed_runtime/`.

However, it owns the candidate discovery, tokenization, term index construction, membership checks, first-loss classification, and metadata aggregation locally. It is not a generic inquiry framework and does not delegate a planning or reasoning engine.

### 7. Implementation loss or observable capability loss if removed

Removing this subsystem would cause **observable capability loss** and **implementation loss**.

Observable capability loss:

- The CLI branch for `--knowledge-reachability-audit` would lose its builder and both rendering paths.
- The observed human report and JSON object would disappear.
- Diagnostic inventory and shape-audit entries would refer to a missing implementation-backed diagnostic.

Implementation loss:

- Candidate discovery across default seeds, event payloads, projected state, source-navigation terms, docs, and runtime modules would disappear.
- The local reachability indexes and first-loss computation would disappear.
- Metadata describing candidate counts, loss stages, scan counts, algorithmic counters, and truncation would disappear.

The responsibility that would disappear is:

> A bounded read-only diagnostic that turns discovered repository/runtime candidate strings into stage-by-stage reachability rows and summary metadata across preserved, projected, read-model, inquiry-orientation, and rendered surfaces.

### 8. Relationship to the recent earned inquiry discipline

The diagnostic strengthens the recent discipline in a narrow, implementation-backed way:

- It computes reasoning before presentation.
- The human CLI and JSON output project already-computed rows and metadata.
- It keeps a bounded responsibility seam: candidate-string reachability and first-loss classification.
- It treats presentation labels as candidates to be tested, not automatically as preserved knowledge.

It is also an **independent diagnostic shape**, not simply another authority-aware inquiry:

- Its candidate source includes default seeds and repository file names, so candidate inclusion can originate from diagnostic vocabulary and file structure rather than earned domain knowledge.
- Its membership checks are lexical term containment, not semantic authority assessment.
- Inquiry orientation is one indexed surface inside the audit, not the audit's organizing engine.
- The `rendered` flag is computed as `read_model or inquiry`, so rendered visibility is a local Boolean derivation rather than evidence that a separate renderer introduced or validated knowledge.

Strongest supporting evidence:

- The audit returns computed rows and metadata before the CLI chooses text or JSON rendering.
- Tests assert the same stage columns and JSON fields from the builder output.
- Diagnostic inventory classifies the surface as read-only, JSON-capable, repo-file-using, not event-ledger-writing, and non-mutating.

Strongest contradictory evidence:

- Candidate discovery starts from hard-coded presentation-oriented default seeds such as `source navigation`, `current work position`, `active edge`, `continuation`, `inquiry orientation`, `state build`, and `projection cache`.
- Candidate families and kinds are heuristic string classifiers.
- Read-model and rendered reachability are derived from local surfaces and booleans, not from a separate general presentation authority.

## Acceptance answers

### Does knowledge reachability already compute reasoning before presentation?

Yes. It computes state projection, candidate discovery, indexes, reachability booleans, first-loss rows, and summary metadata before formatting text or JSON.

### Is this another example of the inquiry discipline, or an independent diagnostic shape?

It is an independent diagnostic shape that is consistent with the inquiry discipline in its most important boundary: reasoning is computed before presentation. It is not itself an authority-aware inquiry framework; it is a bounded lexical reachability audit over implementation surfaces.

### What responsibility would disappear if this subsystem were removed?

The repository would lose the bounded read-only responsibility for discovering candidate strings and reporting where each one is or is not reachable across preserved, projected, read-model, inquiry-orientation, and rendered diagnostic surfaces.

## Files changed

- `docs/knowledge_reachability_inquiry_discipline_reconciliation.md`

## LOC changed

- Added one report file, 186 lines.

## Tests run

```bash
python scripts/seed_local.py --knowledge-reachability-audit > /tmp/kr.txt
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json > /tmp/kr.json
pytest -q tests/test_knowledge_reachability.py tests/test_knowledge_reachability_cache.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Recommended bounded implementation slice

No redesign is recommended. If implementation work is requested later, the bounded slice should be only to preserve or clarify the existing observable diagnostic contract with tests: builder rows and metadata first, formatter projection second, and diagnostic inventory/shape-audit coverage unchanged.
