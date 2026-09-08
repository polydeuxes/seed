# Hybrid testimony pass 077 — State snapshot boundary-origin implementation

## Selected seam

State projection snapshot boundary testimony origin at the Python–SQLite boundary, with synchronized source-origin checks for the state-summary cache.

## Testimony sources examined

Passes 075 and 076 examined Python producer construction, dataclass defaults, SQLite INSERT values, schema defaults, ALTER TABLE migration defaults, legacy rows, in-memory stores, direct/admin rows, rebuild/rewrite paths, summary derivation, and rehydration.

## Before and after jurisdiction split

Before: SQLite preserved boundary values; Python compared value equality. Migration compatibility defaults could become indistinguishable from producer-recorded occurrence.

After: SQLite preserves `boundary_testimony_origin` on projection rows and `boundary_testimony_origin` / `source_boundary_testimony_origin` on summary rows. Python admits only bounded origins: `producer_recorded` and `migration_inferred_compatibility`.

## Standing answers

- Producer-recorded standing: current Python save paths write `producer_recorded` by dataclass default and explicit INSERT.
- Compatibility-inferred standing: ALTER migration writes `migration_inferred_compatibility`; it is eligible only as compatibility standing.
- Consumer-owned decision: Python eligibility predicates and the SQLite summary load query decide cache uptake.
- Lawful acceptance: current producer rows and migrated compatibility rows may be cache inputs when all other boundary limits match.
- Lawful rejection: administratively supplied or unknown origins produce cache miss/rebuild, even when text values match.
- Migration answer: migration preserves compatibility testimony; it does not invent historical producer occurrence.
- Rebuild answer: rebuild produces a newly saved producer-recorded snapshot without appending ledger events.
- Occurrence answer: persistence occurrence remains snapshot preservation only; projection occurrence and ledger fact occurrence remain distinct.

## Schema changes

`projection_snapshots` gains `boundary_testimony_origin`. `state_summary_snapshots` gains `boundary_testimony_origin` and `source_boundary_testimony_origin`. CREATE TABLE defaults are `producer_recorded` for current saves; ALTER migration defaults are `migration_inferred_compatibility` for legacy rows.

## Python changes

`ProjectionSnapshotBoundary` and `SummarySnapshotBoundary` carry origin fields. Eligibility functions accept producer-recorded and migration-inferred origins only. Summary SQLite loading requires the summary source origin to match the state projection origin.

## Compatibility answer

Legacy compatibility remains explicit and observable in tests. It is accepted for bounded cache reuse but does not become producer occurrence.

## Tests executed

Focused tests prove new producer origin, legacy migration distinction, matching strings not proving producer occurrence, bounded eligibility, explicit compatibility, miss/rebuild on insufficient origin, no false ledger append, no cluster mutation flag, persistence/projection distinction, current cache hits, legacy observable behavior, summary synchronization, and no derived-index mutation.

## Remaining pressure

Remaining provenance compression includes in-memory default origin ambiguity for administrative constructors. Remaining derived-index pressure is unchanged and deliberately paused. Remaining diagnostic pressure is limited because no diagnostic surface was added. Cross-realization Unknowns remain for complete owner maps, production witness-to-runtime consumption, and universal provenance envelopes.

## Superseded by correction 078–079

Passes 078–079 supersede this pass's compatibility-reuse claims. The `boundary_testimony_origin` / `source_boundary_testimony_origin` machinery and `migration_inferred_compatibility` reuse answer were based on an unsupported obligation to reuse legacy cache rows. The corrected implementation treats legacy cache rows as rebuildable projections: database migration remains safe, but migrated legacy rows are invalidated by unverified standing and rebuilt from ledger evidence rather than accepted as compatibility inputs.
