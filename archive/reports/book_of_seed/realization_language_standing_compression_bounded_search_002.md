# Realization-language standing-compression bounded search 002

## Constitutional grammar consumed

Current Book grammar is the constitutional authority for this pass.

- `01.External.A-C` says realization, persistence, serialization, provider, and programming-language grammar remain external grammar unless translated with source, scope, uncertainty, limits, negative authority, Unknowns, and refusal conditions preserved.
- `06.Projection.A-B` says projection, diagnostics, read models, packages, sets, and handoffs support bounded visibility or standing only through the responsible consumer boundary, and only when the distinctions needed by that declared consumer purpose survive. Empty contents, unavailable input, incomplete input, Unknown input, no testimony, and negative testimony remain distinct unless a local warranted rule intentionally relates them.
- `07.Realization.A-B` says lawful realization need not mirror constitutional vocabulary structurally, but a Fidelity determination must examine one realization boundary for erasure, invention, mutation, or relocation of authority and classify the result as faithful within scope, unfaithful boundary crossing, or Unknown.

Operational discipline used here:

```text
constitutional grammar
→ repository-selected candidate
→ independent producer recovery
→ independent consumer recovery
→ road cross-examination
→ faithful asymmetry / unfaithful crossing / Unknown
```

Negative authority: this pass does not create a universal package abstraction, result/status type, truthiness framework, realization-language taxonomy, cache framework, subprocess-result framework, or repository-wide default-handling cleanup. It does not treat language mechanics as constitutional grammar and does not repair representation collisions unless an existing consumer relies on the erased distinction.

## Bounded search territory

Repository evidence selected a bounded territory rather than a single road:

1. the prior realization-language survey's remaining strongest unresolved road after the repaired Constitutional View Composition crossing;
2. roads already cited by current Book representative anchors or existing tests as projection, diagnostic, repository-observation, or external-grammar surfaces;
3. implementation paths where the previous pass left either `possible crossing`, `next bounded question`, or `representation collision without evidenced consumer consequence`;
4. existing consumers reachable by direct imports, callers, JSON/human formatters, CLI wrappers, diagnostic inventory/shape-audit specs, and tests.

The bounded territory intentionally excludes broad repository-wide searches for every `None`, default, empty list, SQL miss, subprocess call, or truthiness expression. Prior survey evidence already rejected that universalization, and current Book grammar requires consumer-purpose reliance before classifying a compression as unfaithful.

## Candidate roads examined in order

### 1. Constitutional View Composition package-standing road

**Why repository evidence selected it:** The previous realization-language survey identified this as the strongest lossy crossing because an empty compatibility contribution package and a populated all-negative package both produced scalar `No.`. A later local repair artifact and tests now exist for that exact road, so it is the first coherence check before selecting new territory.

**Producer standing:** `build_constitutional_view_composition(...)` forms one compatibility contribution per successfully built requested view, after validating requested view names against registered contracts and local builders. The repair artifact records that empty requested views produce known zero contribution cardinality, not failed construction and not negative compatibility testimony.

**Consumer standing:** `ConstitutionalViewCompositionArtifact`, JSON rendering, human rendering, pipeline transport, and tests consume a scalar compatibility answer plus preserved requested view identity, contributing views, Unknowns, refusals, read-only flags, event-ledger flags, and mutation flags.

**Realization-language compression:** Python `all(...)` previously allowed vacuous truth over an empty list. Current implementation guards the aggregate with non-empty compatibility answers before returning `No.`.

**Consumer reliance:** Consumers render and transport `compatibility_answer`; tests now witness that empty requested views render and serialize `Unknown.`, while populated all-`No.` compositions remain `No.`.

**Fidelity classification:** **faithful after existing repair**. The prior unfaithful crossing is not current unresolved work because the local aggregate now preserves empty-package standing for the consumer-visible scalar.

**Reason for continuing:** A faithful repaired road does not exhaust the bounded territory. The search returned to repository evidence and selected the strongest remaining unresolved candidate from the prior survey.

### 2. Repository Observation Git testimony road

**Why repository evidence selected it:** The prior survey left `_git_text(...) -> None` as `possible crossing — consumer not yet recovered`. Repository dependencies show the coherent local road: `GitRepositoryObservationProvider.observe(...)` produces `RepositoryObservation`; `repository_observation_json(...)`, `format_repository_observation(...)`, CLI `--observe-repository`, `history_brief`, and `snapshot_policy_audit` consume it; tests cover clean, dirty, unavailable, CLI JSON, and snapshot-policy consumption.

**Independent producer recovery:** The producer first checks `shutil.which(...)` and reports `git executable is unavailable` without calling Git. It then uses `_git_ok(... rev-parse --is-inside-work-tree)` to classify non-affirmation as `path is not a git work tree`. After work-tree admission, it asks for head, branch, remote, and porcelain status. If head or status is unavailable, it produces `repository_status_available=False` with reason `git status is unavailable` and `repository_vcs="git"`. If successful, it counts staged, modified, and untracked lines, sets `repository_dirty=bool(status.strip())`, and preserves `writes_event_ledger=False` and `mutates_cluster=False`.

**Independent consumer recovery:** JSON serialization exposes the dataclass fields without reinterpreting them. Human formatting prints `status available: yes/no`, a reason when present, and `unknown` for unavailable value fields. Snapshot policy consumes only `repository_status_available`, `reason`, `repository_head_commit`, and `repository_dirty`: missing context becomes `repository_context_health="missing"`; available clean context becomes `healthy`; available dirty or incomplete context becomes `partial`; repository status label is `unknown`, `dirty`, or `clean`. Existing tests assert missing Git context remains distinct from snapshot-comparison availability.

**Realization-language compression:** `_git_text(...)` collapses subprocess `OSError`, `ValueError`, and nonzero Git return codes into `None`. `_git_ok(...)` then interprets `None` only as not affirmative for work-tree admission. Later head/status lookup also turns `None` into an unavailable observation with a bounded reason.

**Consumer reliance:** No recovered consumer treats `None` as a negative repository fact such as clean, no remote, no changes, no branch, no VCS, or no snapshot comparability. Consumers rely on `repository_status_available` and `reason` for availability, and on `repository_dirty` only after status is available. The dirty/clean distinction is produced only from successful porcelain status. Snapshot policy explicitly allows comparable snapshots while repository context is missing.

**Road cross-examination:** The producer has richer native subprocess detail than the consumer needs. The road compresses failure-kind detail but does not strengthen it into negative repository standing. Unavailable Git, not-a-work-tree, and status unavailable are distinct enough for current consumers. Branch absence and remote absence after successful Git commands are narrowed locally to optional branch/remote presentation; no consumer relies on them as constitutional absence.

**Fidelity classification:** **faithful asymmetry** for current consumers. The subprocess result is richer than the repository-observation package, but current consumers require safe availability/non-affirmation and successful dirty counts, not exception taxonomy or stderr.

**Reason for continuing:** This resolves the prior Unknown within the bounded road but does not establish a repairable crossing. The search continued to the next strongest representation-collision road with an explicit consumer question.

### 3. External Material Structural Projection to Surface Feature road

**Why repository evidence selected it:** The prior survey recorded omitted unknown-list fields and explicitly empty unknown-list fields colliding in JSON rehydration without consumer consequence, and asked whether any downstream audit treats empty unknowns as complete no-unknown testimony. Repository dependencies show a coherent producer/consumer road: `ExternalMaterialStructuralProjection` JSON can be rehydrated by `structural_projection_from_json_dict(...)`; `project_external_material_surface_features(...)` consumes the structural projection; JSON/human formatters, diagnostic inventory, diagnostic shape audit, examination-frontier work references, and tests consume the resulting surface-feature projection.

**Independent producer recovery:** `project_external_material_structure(...)` validates manifest/source/artifact/hash/encoding/exact text/line counts/character counts before projecting mechanical lines and nonblank regions. It carries request-level unknowns as `projection_unknowns`; generated line and region unknowns are empty because the mechanical producer currently has no line- or region-local Unknown testimony to preserve.

**Independent consumer recovery:** `structural_projection_from_json_dict(...)` requires structural artifact type, required identity/hash/encoding fields, line list, nonblank region list, required region `line_ids`, and required mechanical fields. It defaults omitted `projection_unknowns`, line `unknowns`, and region `unknowns` to empty lists. `project_external_material_surface_features(...)` validates duplicate line ids, duplicate region ids, region line counts, known region line ids, deterministic region line order, and line character counts before projecting measurements. Feature JSON carries unknowns when present. Human formatting presents mechanical feature measurements and boundary notes, not an audited no-unknown claim.

**Realization-language compression:** JSON omission and explicit empty unknown arrays both rehydrate to `()`. Python tuple emptiness then travels through line, region, and projection features.

**Consumer reliance:** The surface-feature consumer relies on mechanical identity, line/region coordinate coherence, counts, ordering, and read-only/no-mutation boundaries. It does not use empty unknown tuples as proof that the upstream structural producer audited all possible Unknowns absent. Tests prove mechanical preservation, omission of raw text from surface features, invalid reference/order refusal, diagnostic inventory presence, shape-audit consistency, and campaign feature counts; they do not assert `unknowns == ()` as negative testimony.

**Road cross-examination:** Required structural fields are strict while optional Unknown-list fields are legacy-tolerant. Unknowns supplied by the producer are preserved when present; omitted unknown fields are not promoted to audited absence. The consumer package narrows to mechanical surface measurement and refuses semantic interpretation. Therefore representation collision exists, but consumer consequence is not recovered.

**Fidelity classification:** **representation collision without consumer consequence**. Current consumer standing does not require omitted-vs-explicit-empty Unknown-list distinction.

**Reason for continuing:** This road does not establish a repairable crossing. The search continued to a projection/cache diagnostic road because it is Book-representative, test-covered, and remained a smaller possible follow-up in the prior survey.

### 4. State-build cache-debug empty-ledger and miss-status road

**Why repository evidence selected it:** The prior survey recorded a possible follow-up around empty-ledger snapshot equality if future diagnostics strengthen currentness claims. The Book names projection/cache freshness as a representative projection boundary, and repository diagnostics expose cache-debug status in CLI/test surfaces.

**Independent producer recovery:** `_state_build_cache_debug_evidence_from_args(...)` builds diagnostic evidence from projection-store availability, cache eligibility, latest event id, summary-snapshot lookup, state-snapshot lookup, cached event ids, and notes. It sets unavailable or skipped states explicitly when the store is absent or ineligible. It computes `current_last_event_id=None` for an empty ledger and classifies summary/state cache status as `hit`, `miss`, `skipped`, or `unavailable`.

**Independent consumer recovery:** CLI formatting and JSON consume the diagnostic evidence as cache visibility. Existing tests around `--state-build-cache-debug` and projection-store cache behavior check hit/miss/skipped/unavailable statuses, cached/current event ids, read-only behavior, and no event-ledger mutation. Cache rebuild consumers treat non-hit as a reason to materialize, not as constitutional nonexistence.

**Realization-language compression:** Multiple non-hit causes can become `miss`; empty ledger current event identity is represented as `None`; a snapshot with nullable `last_event_id=None` can match empty-ledger currentness.

**Consumer reliance:** Current consumers rely on `hit` only as cache eligibility for the exact current ledger frontier represented by nullable last-event identity. They do not claim that `None` means unavailable, incomplete, no testimony, or negative truth. The diagnostic reports current and cached event ids separately, alongside status and notes.

**Road cross-examination:** The road distinguishes unavailable/skipped from miss/hit where the diagnostic purpose needs it. It lawfully narrows stale/absent/mismatched non-hit causes to `miss` for rebuild-oriented use. Empty-ledger `None` is a faithful identity coordinate for no last event in this cache frontier, not Unknown by itself.

**Fidelity classification:** **faithful asymmetry** for current diagnostic and cache consumers.

**Reason for continuing:** No unfaithful crossing was established. This also exhausted the strongest unresolved roads left by prior survey evidence within the selected territory.

## Affected coherent surfaces reviewed

- Constitutional View Composition artifact, JSON renderer, human renderer, pipeline transport, pipeline diagnostic, and focused tests.
- Repository observation provider, JSON/human formatters, CLI JSON path, history-brief import path, snapshot-policy audit health/status consumers, and focused tests.
- External material structural projection, structural JSON rehydration, surface-feature projection, JSON/human formatters, diagnostic inventory/shape-audit rows, examination-frontier work references, and focused tests.
- State-build cache-debug diagnostic evidence, CLI JSON/human surfaces, projection-store cache consumers, and focused tests.

No new operational surface, diagnostic flag, audit, CLI output, event-ledger write, or cluster mutation behavior was added by this investigation artifact.

## Tests recovered from repository evidence

The repository-selected checks for this bounded no-repair pass are:

```text
pytest -q tests/test_constitutional_view_composition.py tests/test_constitutional_pipeline.py
pytest -q tests/test_repository_observation.py
pytest -q tests/test_external_material_surface_feature_projection.py tests/test_external_material_structural_projection.py
pytest -q tests/test_seed_local_script.py -k state_summary_cache_debug
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

The diagnostic inventory/shape-audit tests are included because one examined road consumes existing diagnostic inventory and shape-audit surfaces, not because this artifact adds a diagnostic surface.

## Compatibility preservation

No production implementation changes are selected. Existing compatibility preserved by current repository evidence:

- empty Constitutional View Composition packages remain `Unknown.` while populated all-`No.` packages remain `No.`;
- repository observation remains read-only and non-mutating, and unavailable repository context does not erase snapshot comparability;
- external material surface features remain mechanical, read-only, non-semantic, and preserve supplied Unknowns without treating omitted Unknown fields as audited absence;
- cache-debug remains read-only, preserves unavailable/skipped/hit/miss status coordinates, and does not mutate the event ledger or cluster.

## Negative authority

This pass does not establish that:

- every subprocess failure collapse requires a result object;
- every omitted JSON field must be distinct from an explicit empty field;
- every cache miss needs a miss-cause taxonomy;
- every nullable event id is Unknown;
- every consumer needs producer occurrence or full producer package richness;
- generated diagnostics, views, or caches are source truth;
- representation collision alone is constitutional loss;
- the Book needs revision.

## Remaining Unknowns

- Whether future repository-observation consumers will need Git stderr, return code, or exception-kind detail remains Unknown.
- Whether a future external-material consumer will treat empty `unknowns` as audited no-Unknown testimony remains Unknown; current consumers do not.
- Whether future state-build diagnostics will explain distinct miss causes beyond rebuild eligibility remains Unknown.
- Whether future composition families outside Constitutional View Composition require different aggregation package standing remains Unknown.

## Stopping warrant

The bounded search territory is sufficiently examined for this pass because repository evidence selected and resolved the prior strongest repaired road, the prior strongest unresolved possible crossing, the explicit representation-collision consumer question, and the remaining cache-debug follow-up road. Each examined road recovered producer standing, consumer standing, realization-language compression, and consumer reliance through existing implementation, formatters, CLI/diagnostic surfaces, and tests.

No actual, current, repairable Fidelity crossing was established. The only previously established crossing in this territory, Constitutional View Composition empty-package aggregation, is already repaired and tested. The remaining examined roads show faithful asymmetry or representation collision without current consumer consequence. Under the user's termination rule, the territory is therefore exhausted enough to warrant stopping without implementation changes.
