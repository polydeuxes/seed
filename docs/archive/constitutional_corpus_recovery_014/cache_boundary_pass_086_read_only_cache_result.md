# Cache boundary pass 086 — Read-only cache result

## Consumed evidence

Pass 086 consumes `cache_boundary_pass_085_reality_audit.md`. The audit found that most cache-boundary strings described constitutional vocabulary without preventing a concrete repository-evidenced runtime failure. The supported cache-boundary machinery is narrower: schema validity, cache identity, version and event horizon matching, payload materialization, rebuild from the event ledger, ledger authority, and read-only cache admission through `mutates_cluster=false`.

## Removed unsupported machinery

Removed from projection, summary, and derived-index cache schemas, snapshot boundary dataclasses, SQLite save/load SQL, in-memory predicates, and focused tests:

- cache standing labels;
- producer-boundary labels;
- occurrence-evidence-kind labels;
- source standing labels;
- copied source producer/occurrence/consumer labels;
- summary and fact-index consumer-limit labels;
- report claims that these labels enforce cache authority.

These fields were not retained as compatibility metadata. Existing cache tables with the old columns are incompatible with the current cache schema and are reset through the existing drop-and-rebuild path.

## Preserved supported requirements

The implementation still preserves:

- projection, summary, and derived-index cache table schema validity;
- workspace/name/version identity;
- state projection version and last-event horizon for dependent caches;
- payload materialization and rebuild behavior;
- event-ledger authority for historical occurrence;
- no ledger append during cache hits, misses, schema resets, or dependent-cache rebuilds;
- read-only cache admission through `mutates_cluster=false` on projection, summary, and derived-index cache rows.

## Result

The evidence-supported result is a read-only cache boundary, not a high-resolution constitutional testimony cache. Cache rows are disposable read-model artifacts. They may be consumed when their schema, identity, version, event horizon, materialized payload, source state join, and non-mutating boundary are valid. They do not carry replacement metadata for constitutional standing, producer authority, occurrence evidence kind, source limits, or consumer authority.
