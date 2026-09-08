# Active Witness And Documentation Truth Cleanup 001

## Scope and negative authority

This bounded pass cleaned active implementation witness and active non-Book documentation after PR 1918 removed the pure foreign planning/control shell. The operation did not perform the later full Book contamination lint.

No database compatibility obligation was preserved for deleted planning, handoff, proposal, authorization, or pending-action artifacts.

This operation corrected active witness claims. It did not perform a repository-wide Book contamination lint.

Negative authority preserved:

- deleted implementation equals absent implementation;
- historical possibility does not create a current compatibility obligation;
- a historical database could have existed does not require reserving dead artifact IDs;
- no replacement runtime flow, policy route, execution route, compatibility prefix registry, migration, adapter, or tombstone registry was introduced.

## Dead ID reservations removed

Removed the deleted artifact-family payload ID reservations from `SQLiteEventLedger._PERSISTED_ID_PREFIXES`:

- `plan`;
- `handoff`;
- `auth`.

No additional dead persisted-prefix reservation was found in `seed_runtime/events.py`.

## Surviving ID prefixes and current owners

The surviving persisted payload ID prefixes are:

| Prefix | Current owner / responsibility |
| --- | --- |
| `obs` | General observation records, including local script observation payloads. |
| `obs_local_host` | Local host observation source records. |
| `evd` | Evidence records created by state patch ingestion. |
| `evd_obs` | Evidence records derived by observation ingestion. |
| `fact` | Fact records created by state patch ingestion and current fact fixtures. |
| `fact_obs` | Fact records derived by observation ingestion and persisted observation projection. |
| `need` | Current ToolNeed / capability-gap records and capability inventory state. |

## Dead imports removed

Removed dead `models.py` imports made obsolete by PR 1918 residue:

- `new_id`;
- `normalize_field_name`.

Inspected and retained currently used imports:

- `reject_secret_fields` for event payload secret-field rejection;
- `Any` for model payload/schema field types;
- `Literal` for actor/status/risk/backend type literals;
- `Field` for default factories.

## Active documents examined

Examined at minimum:

- `docs/architecture.md`;
- `docs/invariants.md`;
- `docs/archive/original_book_of_seed/01-architecture.md`;
- `docs/archive/original_book_of_seed/03-runtime-loop.md`;
- `docs/input_source_authority_reconciliation.md`;
- current README/documentation search results returned by the required `rg` command.

Additional stale active or active-looking documents with current-tense route language were marked historical/stale rather than rewritten into replacement architecture:

- `docs/input_act_vocabulary.md`;
- `docs/input_act_decision_bridge.md`;
- `docs/function_blocks.md`;
- `docs/architecture_visualization_phase1.md`;
- `docs/relationship_fact_reconciliation.md`;
- `docs/gap_classification_reconciliation.md`;
- `docs/conclusion_taxonomy_reconciliation.md`;
- `docs/runtime_decision_reconciliation.md`;
- `docs/pending_action_lifecycle_inventory.md`.

## Stale current claims removed or corrected

Removed or corrected active claims that current Seed canonically routes through Runtime/RuntimeLoop, Context-to-Decision-to-Policy-to-Execution, request-tool/call-tool runtime decisions, ActionPlan, HandoffPlan, ExecutionProposal, ExecutionAuthorization, PendingAction, ToolkitCandidate, or builder-candidate workflow.

Specific corrections included:

- `docs/architecture.md` no longer presents `Input -> Events -> State -> Context -> Decision -> Policy -> Execution -> Events` as current architecture.
- `docs/architecture.md` no longer claims Runtime is the canonical input boundary.
- `docs/architecture.md` no longer claims RuntimeLoop is a deprecated active comparison point.
- `docs/invariants.md` no longer contains a Runtime invariants section claiming Runtime is canonical or request_tool is current.
- `docs/invariants.md` no longer retains compatibility clauses for ActionPlan, HandoffPlan, ExecutionProposal, or ExecutionAuthorization.
- At the time, root `01-architecture.md` was reduced toward current bounded event/projection/observation/evidence/fact/view/diagnostic/capability-testimony responsibilities, but PR 1919 left an overstrong active `ToolRegistry` ownership claim that was corrected by the later active architecture/domain document truth correction operation.
- At the time, root `03-runtime-loop.md` was converted to a historical placeholder, not an active RuntimeLoop instruction document.
- `docs/canonical_documentation_reconciliation.md` was corrected where it described `docs/architecture.md` as actively identifying Runtime as canonical.

## Historical documents preserved

Historical testimony, audits, reconciliations, inventories, and quoted former architecture were preserved rather than mechanically term-deleted. Surviving search hits were classified as historical testimony, audit/reconciliation records, quoted former architecture, test names/fixtures for unrelated current responsibilities, or ordinary unrelated language unless a file was corrected above.

Examples of preserved historical/audit families include runtime parity inventories, capability/execution boundary reconciliations, source authority reconciliation, conclusion taxonomy reconciliation, and pending-action lifecycle inventory after being marked or maintained as historical/stale rather than active current instruction.

## Minimal Book references touched, if any

Only this required Book report was added during PR 1919. The later active architecture/domain document truth correction operation amended this report because PR 1919's completion conclusion was overstrong. No Book-wide vocabulary lint was performed.

## Tests added or updated

Added focused tests proving:

- dead persisted ID prefix reservations are absent and the current prefix tuple is exact;
- active invariant documentation no longer preserves deleted Runtime/request-tool/planning/handoff/proposal/authorization compatibility clauses;
- active architecture documentation no longer claims Runtime is canonical or presents the deleted Context/Decision/Policy/Execution pipeline.

## Verification

Commands run:

```bash
rg -n \
'Runtime is canonical|Runtime is the canonical|RuntimeLoop|Context -> Decision|Decision -> Policy|Policy -> Execution|request_tool|call_tool|ActionPlan|HandoffPlan|ExecutionProposal|ExecutionAuthorization|PendingAction|ToolkitCandidate|seed-builder-v1|--preconditions|--handoff|--accept-plan|--approve-plan|--reject-plan|--supersede-plan' \
docs README* 01-architecture.md 03-runtime-loop.md
```

Classification: surviving results are historical/stale banners, historical testimony, audit/reconciliation records, quoted former architecture, or unrelated non-deleted vocabulary in tests/documentation. Active documents corrected in this pass no longer assert the deleted roads as current.

```bash
rg -n \
'"plan"|"handoff"|"auth"|plan_|handoff_|auth_' \
seed_runtime/events.py tests
```

Classification: `seed_runtime/events.py` has no dead persisted-prefix reservation for `plan`, `handoff`, or `auth`; surviving test hits are assertions that those prefixes are absent, ordinary unrelated field/value examples, or unrelated non-planning uses of words such as handoff/auth.

Other verification:

- `python -m compileall -q seed_runtime scripts` passed.
- `python scripts/seed_local.py --help` passed.
- `git diff --check` passed after removing the trailing blank line.
- Focused tests passed: `pytest -q tests/test_events.py tests/test_persistence.py tests/test_state_projector.py tests/test_projection_store.py tests/test_capability_verification_invariants.py tests/test_seed_local_script.py::test_parser_no_longer_exposes_generic_http_or_model_selection`.
- Full suite passed: `pytest -q` reported `2017 passed in 418.09s (0:06:58)`.

## Remaining mixed residue

Mixed boundary families were intentionally left unchanged:

- `Actor`;
- `ToolNeed`;
- `ToolNeedStatus`;
- `ToolSpec`;
- `Toolkit`;
- `Approval`;
- `RiskClass`;
- `HandoffBackendType`;
- `CapabilityCatalog`;
- `CapabilityRecommendation` and provider recommendation surfaces.

Current invariant statements about those families may remain only as descriptions of current behavior and not as final ownership canonization.

## Boundary reserved for the later Book lint

The next operation is reserved for a full Book contamination lint over `book_of_seed/` and any Book-referenced canonical vocabulary. This pass did not inspect, classify, or rewrite the Book corpus beyond adding this report.

## Lawful stopping point

This PR 1919 operation stopped after removing deleted ID reservations, dead imports, stale active architecture/invariant claims, and selected directly active stale documentation anchors. Its conclusion that active documentation was complete was overstrong: additional active contamination remained in then-root `01-architecture.md` and `02-domain-model.md` and was corrected later. It did not invent replacement architecture, did not create migrations or compatibility mechanisms, did not rename mixed models, and did not perform Book-wide lint.

## Final direct answers

1. Was the `plan` persisted-ID reservation deleted? Yes.
2. Was the `handoff` persisted-ID reservation deleted? Yes.
3. Was the `auth` persisted-ID reservation deleted? Yes.
4. Did any replacement compatibility or migration mechanism get introduced? No.
5. Which persisted-ID prefixes remain? `obs`, `obs_local_host`, `evd`, `evd_obs`, `fact`, `fact_obs`, and `need`.
6. What current artifact or responsibility warrants each surviving prefix? `obs` is general observation payload identity; `obs_local_host` is local-host observation identity; `evd` is state-patch evidence identity; `evd_obs` is observation-ingestion evidence identity; `fact` is state-patch fact identity; `fact_obs` is observation-ingestion fact identity; `need` is ToolNeed/capability-gap identity.
7. Were dead `models.py` imports removed? Yes: `new_id` and `normalize_field_name`.
8. Which active architecture claims were removed? Runtime as canonical boundary/coordinator, RuntimeLoop as active deprecated comparator, Context/Decision/Policy/Execution as current pipeline, and active planning/handoff/current runtime-decision route claims.
9. Which active invariant claims were removed? Runtime canonicality, request_tool current behavior, and retained compatibility clauses for ActionPlan, HandoffPlan, ExecutionProposal, and ExecutionAuthorization.
10. Does any active document still claim `Runtime` is canonical? No.
11. Does any active document still present `Context -> Decision -> Policy -> Execution` as current architecture? No.
12. Does any active document still claim `request_tool` is current? No.
13. Does any active document still permit retention of `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, or `ExecutionAuthorization`? No.
14. Which historical documents were preserved? Historical/audit/reconciliation/inventory documents surfaced by search were preserved, including RuntimeLoop-era, source-authority, input-act, architecture-visualization, relationship-fact, gap-classification, conclusion-taxonomy, runtime-decision, and pending-action records.
15. Were any historical reports rewritten merely because their implementation was deleted? No; active-looking stale anchors were marked historical/stale or minimally corrected, but historical testimony was not mechanically purged.
16. Were mixed `ToolNeed`, `ToolSpec`, `Approval`, `RiskClass`, recommendation, provider, backend, or Actor surfaces changed? No.
17. Was a new architecture invented? No.
18. What active-documentation residue remains? PR 1919 incorrectly concluded that no known active document still asserted deleted roads as current. Later inspection found additional active contamination in `docs/archive/original_book_of_seed/01-architecture.md` and `docs/archive/original_book_of_seed/02-domain-model.md`; the active architecture/domain document truth correction operation completed that bounded correction. Historical/stale documents still contain preserved former vocabulary by design.
19. What exact scope is reserved for the next Book contamination lint? A repository-wide Book-focused contamination lint over `book_of_seed/` and Book-referenced canonical claims, including historical/current classification beyond this single added report.
20. Where must this operation stop? It stops at active witness and active documentation truth cleanup, leaving historical testimony, mixed-boundary recovery, and Book-wide contamination lint for later operations.
## Later archival conclusion after PR 1920

The numbered root documents were subsequently classified together as the
formative original Seed corpus and archived as historical testimony.

Their active-document corrections were bounded intermediate repairs, not a
final decision that the family should remain a second active canon.

Sequence preserved: PR 1919 corrected implementation residue and selected
active docs; PR 1920 corrected additional numbered active claims; the later
original numbered Seed corpus archival operation recovered the numbered
family's proper standing as one historical corpus.
