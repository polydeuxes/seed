# Python–SQLite correction pass 079 — Legacy cache invalidation

Pass 079 consumes pass 078.

## Before / after responsibility split

Before: SQLite preserved boundary values plus testimony-origin columns. Migration supplied `migration_inferred_compatibility`; Python accepted both producer-recorded and migrated-origin rows as cache inputs.

After: SQLite preserves only the boundary values needed for cache standing and consumer limits. Current `CREATE TABLE` paths write current bounded defaults. `ALTER TABLE` migration for legacy cache tables marks missing boundary standing as `legacy_unverified_*`, making those rows safe cache misses. Python rebuilds from the event ledger and overwrites the disposable cache with current bounded standing.

## Deleted assumptions

- Legacy cache reuse is not required.
- Migrated default values do not need an origin taxonomy.
- Summary source-origin synchronization is unnecessary when legacy rows are invalidated instead of reused.
- Admin/migration/producers do not need a universal origin envelope for rebuildable cache rows.

## Compatibility answer

Database opening and schema migration remain compatible. Reuse of old cache rows is not preserved. Legacy projection and summary rows are disposable and may be invalidated safely; rebuilding does not append events, create facts, create observations, or mutate cluster state.

## Tests

Tests now prove that legacy projection rows migrate to unverified standing and are rebuilt rather than reused, that legacy summary rows miss instead of being accepted as compatibility inputs, and that current producer-written rows still hit when their bounded cache limits match.

## Remaining Unknowns

The event payload JSON and state snapshot payload still compress many dimensions. Complete read-model owner maps remain incomplete. This pass does not redesign projection storage or declare the Python–SQLite realization complete.
