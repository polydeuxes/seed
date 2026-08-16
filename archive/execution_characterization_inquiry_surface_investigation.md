# Execution Characterization Inquiry Surface Investigation

This implementation investigation asks whether current Seed implementation already preserves enough execution evidence to answer “How did this inquiry surface execute?” for representative inquiry surfaces. It does not add a CLI surface, execution instrumentation, timers, or optimization work.

## Implementation summary

Current implementation preserves a partial, implementation-backed execution characterization. Most representative inquiry surfaces share the same CLI dispatch pattern: parse a flag, build or load `State` via `projected_state_from_args`, call a surface-specific builder, then render text or JSON. For persisted databases with the default predicate catalog and default measurement history limit, `projected_state_from_args` participates in the state projection cache; otherwise it performs direct projection replay.

Execution evidence is strongest for the shared projection/cache/snapshot layer and for explicit debug surfaces. It is weaker for arbitrary inquiry surfaces because most surfaces do not record or return their own cache status, projection path, formatter path, or elapsed phases. The repository can explain many execution relationships by composing CLI dispatch, projected-state loading, projection store behavior, builder code, formatter code, diagnostic inventories, and tests, but it does not currently expose one unified execution-characterization read model for arbitrary surfaces.

## Representative execution chains

| Question family | Answer surface | Implementation-backed execution path | Projection participation | Cache participation | Snapshot participation | Observed execution phases | Observed timing evidence | Boundary |
|---|---|---|---|---|---|---|---|---|
| Operational pressure | `ops_brief` / `--ops-brief` | CLI dispatch calls `build_ops_brief(projected_state_from_args(args), repo_root=REPO_ROOT)`, then JSON or text formatting. `build_ops_brief` composes observation inventory, observation utilization, consumer audit, ownership discrepancies, capability needs, diagnostic shape audit, diagnostic inventory count, and audit snapshot listing. | Yes. It consumes projected `State` for ownership discrepancies and capability needs. | Shared state projection cache may be used by `projected_state_from_args` when `--db` is present, no custom predicate catalog is supplied, and measurement history limit is default. | Lists audit snapshots as answer content. State projection snapshots may be loaded/saved by shared projection cache. | CLI dispatch, state load/projection, composed builders, render. | No surface-specific timing. Timing is only indirectly available from shared projection diagnostics/debug surfaces. | Read-only aggregation; no record or cluster mutation in builder. |
| Current operational explanation | `operational_story` / `--operational-story` | CLI dispatch calls `build_operational_story(projected_state_from_args(args), repo_root=REPO_ROOT)`, then `operational_story_json` or `format_operational_story`. Builder composes pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit. | Yes, through projected `State`. | Same shared state projection cache eligibility as other `projected_state_from_args` consumers. | State projection snapshot participation only through shared projection cache. | CLI dispatch, state load/projection, pressure/capability/privilege/correlation/impact/investigation builders, render. | No surface-specific timing. | Builder returns boundary fields: mode read-only view, no fact recording, no event ledger writes, no cluster mutation. |
| Knowledge reachability | `knowledge_reachability` / `--knowledge-reachability-audit` | CLI opens `EventLedger`, then calls `build_knowledge_reachability_audit_result`; implementation projects state directly with `StateProjector(ledger).project`, lists ledger events, discovers candidates, builds candidate/read-model surfaces, scores rows, and formats table or JSON. | Yes, but it directly projects state rather than using `projected_state_from_args`. | Metadata initializes state/summary/projection cache visibility as misses; implementation does not use `ProjectionStore` in the observed path. | No projection snapshot reuse or creation in current implementation path. | `load_state`, `discover_candidates`, read-model phases such as `read_model.current_facts`, `read_model.fact_support`, and `read_model.state_summary`, plus row evaluation phases captured by the reachability timer. | Yes. Reachability metadata contains phase timings and debug output can print cache visibility and counters. | Read-only audit surface in diagnostic inventory/shape audit; no cluster mutation. |
| Authority-constrained service ownership | `service_ownership_authority` / `--service-ownership-authority` | CLI dispatch loads projected state, calls `evaluate_service_ownership_authority_slice`, then renders JSON/text. Evaluator computes required service observations, authority requirements, reachable/blocked observations, discrepancy summaries, uncertainty, and blocking boundary. | Yes, through projected `State`. | Shared state projection cache may participate via `projected_state_from_args`. | State projection snapshot participation only through shared projection cache. | CLI dispatch, state load/projection, authority evaluation, render. | No surface-specific timing. | Evaluation docstring states the slice reads existing repository surfaces as implementation evidence. Diagnostic inventory and shape audit classify it as read-only/non-mutating. |
| Derivation explanation | `reasoning_path` / `--reasoning-path <domain> <subject>` | CLI dispatch loads projected state, calls `build_reasoning_path_audit`, then JSON/text formatting. Builder composes ownership discrepancies, capability needs, pressure audit, privilege discovery, and operational story, then filters evidence by subject/domain. | Yes, through projected `State`; also recursively calls operational story which composes additional builders. | Shared state projection cache may participate via `projected_state_from_args`. | State projection snapshot participation only through shared projection cache. | CLI dispatch, state load/projection, ownership/capability/pressure/privilege/story builders, filtering/selection, render. | No surface-specific timing. | Boundary says read-only reasoning audit: no fact recording, no event ledger writes, no cluster mutation. |
| Selection explanation | `selection_path` / `--selection-path <target>` | CLI dispatch loads projected state, calls `build_selection_path_audit`, then JSON/text formatting. Builder normalizes the target, builds pressure audit and operational story, and explains pressure ordering or an unknown target. | Yes, through projected `State`; also calls operational story. | Shared state projection cache may participate via `projected_state_from_args`. | State projection snapshot participation only through shared projection cache. | CLI dispatch, state load/projection, pressure audit, operational story, candidate ranking explanation, render. | No surface-specific timing. | Boundary says read-only selection audit: no fact recording, no event ledger writes, no cluster mutation. |
| Projection shape visibility | `projection_shape` / `--projection-shape` | CLI dispatch calls `build_projection_shape()` directly, then JSON/text formatting. The implementation returns static `PROJECTION_SHAPE_STAGES` and a boundary dictionary. | It describes projection stages but does not build projected `State` for the request. | None in the request path. | None in the request path. | CLI dispatch, static stage materialization, render. | No timing. | Boundary dictionary says read-only, no event ledger writes, no cluster mutation. |
| State-build cache debug | `state_build_cache_debug` / `--state-build-cache-debug` | Debug implementation opens projection store and ledger, lists events, checks summary snapshot, optionally checks state snapshot, constructs projector, calls `project_state_with_cache` or direct `projector.project`, builds `StateSummary` and operator summary, optionally saves summary snapshot, and renders debug report. | Yes. It explicitly invokes projection replay/build and records projection subphase diagnostics. | Yes. Summary cache, state cache, projection cache eligibility, cache statuses, and notes are part of the report. | Yes. It loads summary snapshots, loads state snapshots, reconstructs state snapshot payloads, and saves summary snapshots when eligible. | Projection store open, ledger open, event listing/current last event lookup, summary snapshot lookup/decode, state cache lookup/decode, projector construction, projection replay/build, fact-support construction, compact summary derivation, operator summary derivation, summary snapshot save, rendering, total runtime. | Yes. Report has timings plus projection replay/build subphase timings and structure counters. | Explicit docstring says it measures the state-build cache boundary without ingesting or executing tools. |
| Current-facts cache debug | `current_facts_cache_debug` / `--current-facts-cache-debug` | Debug implementation opens ledger/store, wraps store with `_TimingProjectionStore`, optionally seeds dev state for a query, constructs projector, uses `project_state_with_cache` when eligible, optionally loads/builds fact index, builds read model or query output, and renders timing report. | Yes. It either uses `project_state_with_cache` or full projection rebuild. | Yes. Reports state cache hit/miss/unavailable and, for subject/predicate queries, fact-index cache lookup/load and save through the wrapped store. | Yes when shared projection cache is eligible: snapshot load/save are timed; fact-index derived-index snapshots can load/save. | Ledger open, projection store open, state projector construction, cache load/save, state cache hit/incremental/full rebuild path, projection diagnostic timings, read-model build or fact-index build/load, query/filter + render, stdout/output time, total. | Yes. `CurrentFactsTimingReport` carries timings. | Read-only debug report; diagnostic inventory/shape audit classify it as non-mutating. |

## Recurring execution relationships

- **CLI dispatch to builder to formatter** recurs across `ops_brief`, `operational_story`, `service_ownership_authority`, `reasoning_path`, `selection_path`, `projection_shape`, and `knowledge_reachability`.
- **Projected `State` as shared input** recurs across `ops_brief`, `operational_story`, `service_ownership_authority`, `reasoning_path`, and `selection_path`; `knowledge_reachability` also projects state but uses its own direct path; `projection_shape` describes projection without building state.
- **Shared projection cache eligibility** recurs for surfaces using `projected_state_from_args`: persisted `--db`, no custom predicate catalog, default measurement-history limit.
- **ProjectionStore snapshot load/save and incremental replay** recur in the shared `project_state_with_cache` layer and are visible most clearly through state-build and current-facts debug surfaces.
- **Read model / formatter separation** recurs: builders return structured objects or dictionaries and formatters render text/JSON.

## Surface-specific execution relationships

- `ops_brief` uniquely includes audit snapshot listing and diagnostic inventory/shape summaries in the answer content.
- `operational_story` uniquely composes pressure, capabilities, privilege, correlation, impact, and investigation path into a narrative view.
- `knowledge_reachability` uniquely preserves candidate discovery, token/read-model phases, counters, cache visibility metadata, and timing metadata in the audit result.
- `service_ownership_authority` uniquely evaluates required authority for passive service ownership observations, reachable/blocked observations, uncertainty, and a blocking boundary.
- `reasoning_path` uniquely traces derivation from ownership discrepancies and capability needs into consumers and story impact for a subject/domain.
- `selection_path` uniquely explains pressure candidate ordering and why non-selected candidates did not win.
- `projection_shape` uniquely returns static implementation-backed projection stage metadata rather than consuming a projected state instance.
- `state_build_cache_debug` uniquely exposes summary snapshot behavior and projection/build structure counters.
- `current_facts_cache_debug` uniquely exposes fact-index derived-cache participation and current-facts query/render timing.

## Snapshot participation findings

- **Snapshot reuse:** `project_state_with_cache` loads a matching projection snapshot, materializes `State`, and returns a cache hit if the snapshot last event id equals the current last event id.
- **Snapshot creation:** after a cache miss/full rebuild or incremental replay, `_save_state_snapshot` saves a `ProjectionSnapshot` with workspace, projection name/version, last event id, serialized state payload, and creation timestamp.
- **Incremental replay:** if a snapshot can be materialized but is stale, has no inferred facts, and the remaining ledger events after the snapshot can be identified, `project_from_state` applies only remaining events and then saves a fresh snapshot.
- **Snapshot comparison:** the audit snapshot path can create, list, and compare audit snapshots; `ops_brief` reports whether a latest audit snapshot comparison is available. This is separate from projection-cache snapshot comparison.
- **Snapshot policy:** a dedicated `snapshot_policy_audit` module exists in the CLI import set, but this investigation did not find representative inquiry surfaces depending on it for their execution path.
- **Cache participation:** projection snapshots support shared state cache; summary snapshots support state-build read-model cache; derived index snapshots support fact-index cache used by current-facts query debug.

## Execution composition findings

The smallest truthful execution characterization Seed can currently provide for an arbitrary inquiry surface is:

1. the CLI flag and dispatch branch,
2. whether the branch uses `projected_state_from_args`, direct `StateProjector.project`, or no state projection,
3. the builder function called,
4. the formatter or JSON serializer called,
5. the shared projection-cache eligibility and possible cache path when `projected_state_from_args` is used,
6. any explicit boundary metadata exposed by the builder or diagnostic inventory/shape audit,
7. debug/timing details only when the surface itself is a debug/timing surface or when the shared projection debug surfaces are run separately.

Execution characterization is therefore **layered and composed**. The strongest layer is shared projection/cache/snapshot infrastructure; the next layer is CLI dispatch; the next layer is surface-specific builder composition; the final layer is formatter/rendering. Current implementation evidence supports this composition, but only explicit debug surfaces preserve timing and cache-path details as output.

## Implementation-backed gaps

- Most inquiry surfaces do not preserve per-run cache status, projection path, or timing in their own output.
- The diagnostic inventories record surfaces and shape expectations, but not a complete execution chain per surface.
- `knowledge_reachability` has rich internal timings, but it does not use the shared projection cache path in the observed implementation.
- `projection_shape` describes projection relationships statically; it does not characterize how a specific inquiry surface executed.
- Runtime trace is implemented as a read-only historical runtime-run view, but it is not composed into representative inquiry surface execution chains.
- Snapshot policy exists as a separate surface/module, but current representative execution paths do not use it to decide projection-cache behavior.

## Conclusion

Execution characterization appears to be an **emerging implementation-backed capability**, not yet a unified subsystem. The evidence is not too fragmented to answer a minimal form of “How did this inquiry surface execute?” because CLI dispatch, projected state loading, projection cache behavior, builder composition, formatter paths, and debug timing surfaces are all implementation-backed. However, the current implementation does not preserve one complete execution-characterization relationship for arbitrary inquiry surfaces. A future execution-characterization inquiry surface would primarily compose existing evidence for dispatch, projection/cache/snapshot behavior, builders, formatters, and boundaries, but would still need additional implementation knowledge to make per-surface execution chains complete and uniformly inspectable.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' .. /workspace 2>/dev/null | head -50 && git status --short`
- `rg -n "def main|argparse|ops-brief|operational-story|knowledge-reachability|service-ownership|reasoning-path|selection-path|projection-shape|state-build-cache|current-facts-cache|runtime-trace|diagnostic-inventory" seed_runtime tests -S`
- `rg --files | rg '(^|/)seed(_local)?(\.py)?$|cli|local' | head -50`
- `sed -n '1,220p' scripts/seed_local.py && sed -n '220,520p' scripts/seed_local.py && sed -n '520,900p' scripts/seed_local.py`
- `rg -n "def _load_state|def _state_from_args|def _state_build|def _current_facts|def main|add_argument\(.*ops|if args\.ops|operational_story|reasoning_path|selection_path|projection_shape|service_ownership|knowledge_reachability" scripts/seed_local.py`
- `sed -n '4800,5145p' scripts/seed_local.py && sed -n '6200,6680p' scripts/seed_local.py && sed -n '6860,6930p' scripts/seed_local.py`
- `sed -n '5145,5235p' scripts/seed_local.py && sed -n '536,820p' seed_runtime/projection_store.py && sed -n '330,380p' seed_runtime/knowledge_reachability.py && sed -n '690,725p' seed_runtime/knowledge_reachability.py`
- `rg -n "def projected_state_from_args|def fact_query_state|def _projection_store_from_args|def _can_use_state_cache|state-build-cache-debug|State Build Cache" scripts/seed_local.py seed_runtime/projection_store.py seed_runtime/state.py seed_runtime/projection_shape.py seed_runtime/ops_brief.py seed_runtime/operational_story.py seed_runtime/reasoning_path_audit.py seed_runtime/selection_path_audit.py seed_runtime/service_ownership_authority.py`
- `sed -n '2850,2995p' scripts/seed_local.py && sed -n '3250,3335p' scripts/seed_local.py && sed -n '1,220p' seed_runtime/projection_shape.py && sed -n '1,140p' seed_runtime/ops_brief.py && sed -n '1,140p' seed_runtime/operational_story.py`
- `sed -n '1,260p' seed_runtime/reasoning_path_audit.py && sed -n '1,220p' seed_runtime/selection_path_audit.py && sed -n '100,185p' seed_runtime/service_ownership_authority.py && sed -n '760,900p' seed_runtime/state.py`
- `sed -n '900,940p' seed_runtime/state.py && sed -n '3000,3250p' scripts/seed_local.py`
- `git diff --check && git status --short && nl -ba docs/execution_characterization_inquiry_surface_investigation.md | sed -n '1,160p'`

## Files inspected

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/state.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/ops_brief.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- Related tests discovered by ripgrep under `tests/`.

## Files changed

- `docs/execution_characterization_inquiry_surface_investigation.md`

## LOC changed

- Added 125 lines.

## Tests run

No tests were required for this documentation-only implementation investigation. No production code, CLI surface, diagnostic registry, diagnostic shape audit, or recordable output was changed.
