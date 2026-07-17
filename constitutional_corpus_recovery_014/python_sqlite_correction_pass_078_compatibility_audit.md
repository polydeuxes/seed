# Python–SQLite correction pass 078 — Compatibility assumption audit

Repository authority wins. This pass changes no code.

## Finding

The prior origin machinery was justified by an unsupported obligation: that legacy projection-cache rows migrated from older SQLite schemas must remain reusable cache inputs. Repository evidence establishes safe database opening, schema migration, bounded cache rebuilding, and non-mutating read-model behavior. It does not establish reuse of old cache rows as an obligation.

## Compatibility obligation classification

| Claimed obligation | Classification | Evidence / answer |
| --- | --- | --- |
| SQLite databases with older projection-cache tables should still open. | repository-established | Existing migration helpers and persistence tests require schema evolution not to make the database unusable. |
| Current producer-written state projection cache rows may be reused when projection version, event horizon, payload materialization, standing, consumer limit, and non-mutation checks match. | repository-established | `project_state_with_cache` and projection-store tests prove cache hit, miss, stale, corrupt, and rebuild behavior. |
| Current producer-written summary rows may be reused only when tied to a bounded source state projection. | repository-established | Pass 073/074 implementation and tests establish source-limit checking for summary cache consumption. |
| Legacy cache rows must remain reusable after adding boundary columns. | unsupported | Cache rows are rebuildable projections. No repository or user instruction names old cache reuse as required. |
| Legacy migrated rows need compatibility standing distinct from producer standing. | implementation convenience | This was introduced to support legacy reuse; without that unsupported reuse requirement, origin standing is unnecessary. |
| Matching boundary strings from direct/admin rows must be rejected because they lack producer origin. | unsupported as a cache-reuse requirement | Matching strings alone do not prove occurrence, but cache eligibility only needs bounded current-row limits for rebuildable cache use; it must not be promoted to producer occurrence. |
| Legacy rows must be safely invalidated and rebuilt without ledger append or cluster mutation. | repository-established by boundary principles and user-required here | The objective says projections are rebuildable and asks not to preserve unsupported compatibility behavior. |
| Boundary columns preserving derived standing, occurrence kind, consumer limit, and `mutates_cluster=false` remain required. | repository-established | Pass 071/074 evidence prevents row existence from becoming truth, occurrence, or mutation authority. |
| Derived-index rows may be consumed from any matching state version/event row regardless of source boundary. | unsupported | They are downstream read models and cannot strengthen an invalid source projection. |

## Authoritative and disposable data

Authoritative durable data is the append-only event ledger and its event payloads as recorded occurrences. Python projection output, state-summary rows, derived-index rows, and projection snapshots are disposable/rebuildable read-model cache artifacts. SQLite preservation of a cache row evidences cache preservation only, not fact truth, projection occurrence, or cluster mutation.

## Unsupported dependencies identified

Unsupported legacy-reuse assumptions affected: `boundary_testimony_origin`, `migration_inferred_compatibility`, summary source-origin synchronization, tests asserting legacy compatibility reuse, and reports claiming migrated cache rows are eligible compatibility inputs. These should be removed or corrected. Boundary value checks should remain; legacy rows should be safely invalidated by incompatible migration defaults and rebuilt from the ledger when needed.
