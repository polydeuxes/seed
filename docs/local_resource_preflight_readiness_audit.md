# Local Resource Preflight Readiness Audit

## Purpose

This document audits whether Seed currently has enough local, provider-independent resource information to implement a safe local preflight check before high-volume acquisition work.

This is a documentation-only implementation-readiness audit.

No code was changed.

No schema was changed.

No runtime behavior was changed.

No tests were changed.

No ontology definitions were changed.

No provider acquisition behavior was changed.

## Scope

This audit is scoped to local resource readiness for Seed itself.

The motivating question is:

```text
Do we already have enough local RAM, disk, and database-path information to implement a safe preflight check before acquisition?
```

The focus is local-only:

```text
local RAM
local DB filesystem free/total
local DB file size
local DB WAL size
```

Prometheus is intentionally out of scope for preflight dependency.

Prometheus may later provide provider observations about hosts, but it should not be required to decide whether Seed itself has enough local room to perform provider acquisition.

## Non-goals

This audit does not propose:

* Prometheus dependency for preflight
* provider-backed preflight
* new ontology
* new schemas
* new provider acquisition behavior
* new fact promotion behavior
* resource-capacity claims about remote hosts
* execution approval logic
* observation-cost accounting for every observation
* modeling every observation side effect

## Reviewed implementation surfaces

### `scripts/seed_local.py`

The local CLI already exposes:

* `--db` for selecting a SQLite event ledger path
* `--observe-local-host` for local read-only discovery intake
* `--observe-prometheus` for provider intake
* `--state-build` and other read-only projected views

The CLI path distinguishes local host observation from Prometheus observation, but there is no dedicated `--preflight` or equivalent local resource readiness command.

The `--observe-prometheus` flag is a provider acquisition path and should not be used as a dependency for checking whether acquisition is safe.

### `seed_runtime/observation_sources.py`

`LocalHostObservationSource` already performs local read-only collection using Python standard library APIs and local files. Its metadata explicitly marks local-only behavior and absence of shell execution, subprocess execution, privilege escalation, network probes, and network connections.

It currently emits local observations including:

```text
local_observation_status
os
architecture
disk_total_bytes
disk_free_bytes
cpu_count
memory_total_bytes
```

The root disk observations are currently based on:

```text
shutil.disk_usage("/")
```

The memory total observation is currently based on:

```text
/proc/meminfo MemTotal
```

The source does not currently emit:

```text
memory_available_bytes
local_db_path_free_bytes
local_db_path_total_bytes
local_db_file_size_bytes
local_db_wal_size_bytes
local_process_rss_bytes
local_tmp_free_bytes
```

### `predicate_catalog/core.json`

The predicate catalog currently defines `memory_total_bytes` as a durable fact.

It also defines `disk_total_bytes` and `disk_free_bytes` as local host predicates indirectly evidenced by the existing local host source behavior, but root disk observations are not sufficient for DB-path preflight if the selected DB path resides on a different filesystem.

There is no existing canonical predicate for:

```text
memory_available_bytes
db_path_free_bytes
db_path_total_bytes
db_file_size_bytes
db_wal_size_bytes
```

A first implementation slice does not necessarily need to add canonical predicates if the preflight is presented as a local runtime check rather than persisted observation.

### Tests

Existing tests cover `LocalHostObservationSource` as local read-only collection.

Relevant test behavior includes:

* local host collection does not execute shell commands
* local host collection does not require network calls
* local host collection emits `disk_total_bytes`, `disk_free_bytes`, `cpu_count`, and other host description observations
* local host collection does not assert availability or network reachability merely because local observation succeeded

The existing tests are a strong foundation for a local preflight implementation because they already enforce local-only, read-only, no-network behavior.

## Current state

Seed already has partial local resource observation support:

```text
memory_total_bytes
root disk_total_bytes
root disk_free_bytes
```

Seed does not yet have the minimum information needed for a reliable local preflight:

```text
memory_available_bytes
DB-path filesystem free/total
DB file size
DB WAL size
```

Root filesystem free space is not enough if the selected DB path is elsewhere.

Memory total is not enough to determine whether the current process has room to perform a high-volume acquisition.

DB file size and WAL size are important because acquisition cost is often local write amplification rather than only incoming observation count.

## Boundary finding

The relevant boundary is:

```text
local runtime preflight
        !=
provider observation
```

A preflight check may inspect local operating conditions because it is the safety boundary before provider acquisition.

A preflight check should not require the provider acquisition it is gating.

For example:

```text
Seed may inspect local RAM, DB path free space, DB file size, and WAL size before querying Prometheus.

Seed should not need Prometheus data to decide whether it is safe to query Prometheus.
```

This is a runtime bootstrap concern, not a new ontology plane.

## Why Prometheus is not the starting point

Prometheus can observe many useful host resource facts, but it is optional provider input.

Starting preflight with Prometheus would invert the dependency:

```text
provider acquisition
        ↓
decide whether provider acquisition is safe
```

That is the wrong direction for this specific readiness check.

The correct implementation ordering is:

```text
Seed process starts
        ↓
local resource preflight
        ↓
safe enough to acquire?
        ↓
provider acquisition may begin
```

Prometheus data may later enrich monitoring, state summary, or remote-host resource awareness, but it is not a prerequisite for local preflight.

## Required local resource fields

The smallest useful local preflight surface should inspect:

```text
memory_available_bytes
memory_total_bytes
db_path_free_bytes
db_path_total_bytes
db_file_size_bytes
db_wal_size_bytes
```

### Memory

`memory_total_bytes` already exists through `/proc/meminfo` `MemTotal` when local host observation runs.

`memory_available_bytes` does not currently exist.

A local-only implementation can derive it from `/proc/meminfo` `MemAvailable` on Linux.

Fallback behavior should be explicit if `MemAvailable` is unavailable.

Do not substitute `MemFree` silently as equivalent to available memory unless the code labels the downgrade, because free memory and available memory differ materially on Linux.

### DB path free/total

`disk_free_bytes` and `disk_total_bytes` currently reflect `/` from `shutil.disk_usage("/")`.

Preflight needs the filesystem containing the selected DB path, not necessarily `/`.

The implementation should compute disk usage for:

```text
Path(args.db).resolve().parent
```

or the effective DB path parent if no `--db` is supplied and an in-memory ledger is being used.

If no persistent DB path exists, preflight should report that DB-path file growth is not applicable rather than inventing a path.

### DB file size

The DB file size can be inspected with local filesystem metadata.

If the DB file does not exist yet, size should be `0` with an explicit status such as:

```text
db_file_exists: false
```

This should not be treated as failure by itself.

### DB WAL size

SQLite WAL files commonly appear next to the database as:

```text
<db>.sqlite-wal
```

The preflight should inspect the WAL path if a DB path exists.

If the WAL file is absent, WAL size should be `0` with an explicit status such as:

```text
db_wal_exists: false
```

This should not be treated as failure by itself.

## Existing implementation support

Seed already has several useful implementation pieces:

```text
--db CLI path
LocalHostObservationSource
read-only local-file conventions
stdlib-only local collection
no-network local collection tests
predicate catalog support for memory_total_bytes
root disk usage collection
```

These support a small implementation slice, but not a complete preflight yet.

The missing piece is a local runtime preflight utility or CLI surface that checks DB-path and memory conditions directly before acquisition.

## Recommended implementation slice

Implement a local-only preflight command first.

Suggested CLI shape:

```text
python scripts/seed_local.py --db .seed-local.sqlite --preflight
```

Suggested output shape:

```text
preflight:
  memory:
    available: <bytes>
    total: <bytes>
    status: ok|warning|error
  db path:
    path: .seed-local.sqlite
    filesystem_free: <bytes>
    filesystem_total: <bytes>
    db_size: <bytes>
    wal_size: <bytes>
    status: ok|warning|error
```

This command should not:

* query Prometheus
* append events
* ingest observations
* project state
* require a model
* require network access
* execute shell commands

It should use local Python and local filesystem/proc inspection only.

## Later implementation slice

After a standalone preflight exists, provider acquisition commands may optionally call it before large acquisition.

For example:

```text
seed --observe-prometheus URL
```

could run local preflight first, then continue, warn, or refuse based on thresholds.

That should be a later slice, because the first slice should prove the local-only readiness surface independently.

## Thresholds

This audit does not define final thresholds.

A first implementation can use conservative defaults and make them visible.

Potential threshold inputs:

```text
minimum_memory_available_bytes
minimum_db_path_free_bytes
maximum_db_wal_size_bytes
```

The first implementation may also report observations without failing if the repository is not ready to enforce gates yet.

If enforcement is added, it should be explicit and test-covered.

## What should not be persisted yet

Do not immediately promote preflight results into durable facts unless a separate design establishes why they belong in the knowledge model.

Preflight is initially a local runtime readiness check.

Persisting it as observations may be useful later, but that would raise additional questions:

* whether preflight status is evidence
* whether it belongs in the event ledger
* whether it should expire immediately
* whether it should appear in state summary
* whether it should participate in issue generation

Those questions are intentionally out of scope.

## Direct answers

### Do we have RAM details yet?

Partially.

Seed currently has `memory_total_bytes` through local host observation, but not `memory_available_bytes`.

`memory_total_bytes` is insufficient for preflight because capacity to proceed depends on available memory, not total installed memory.

### Do we have disk details yet?

Partially.

Seed currently has root filesystem `disk_total_bytes` and `disk_free_bytes` from local host observation.

That is insufficient for preflight because the selected DB path may live on a different filesystem.

### Do we have DB file size details yet?

No.

No audited implementation surface currently reports DB file size.

### Do we have DB WAL size details yet?

No.

No audited implementation surface currently reports SQLite WAL size.

### Is Prometheus required for this?

No.

Prometheus must not be a dependency for local preflight.

Prometheus may later supply provider observations about hosts, but local preflight must be provider-independent.

### Do we have enough to implement a safe first slice?

Yes.

The first safe slice is not full provider gating.

The first safe slice is a standalone, local-only `--preflight` style command that inspects memory available, DB path free space, DB size, and WAL size without ingesting observations or querying providers.

### Should this become an architectural invariant now?

No.

The current finding is implementation-readiness shaped.

It should be kept as a runtime bootstrap/preflight concern unless repeated failures across acquisition sources force a broader architectural reconciliation.

## Recommended next Codex prompt shape

```text
Pull latest main first.

Task: implement a local-only preflight command.

Read docs/local_resource_preflight_readiness_audit.md before changing code.

Do not query Prometheus.
Do not ingest observations.
Do not append events.
Do not project state.
Do not require a model.
Do not execute shell commands.

Implement local checks for:

- memory_available_bytes
- memory_total_bytes
- db_path_free_bytes
- db_path_total_bytes
- db_file_size_bytes
- db_wal_size_bytes

Use Python stdlib and local proc/filesystem inspection only.

Add tests proving:

- no provider acquisition occurs
- no events are appended
- DB path free/total is based on the selected DB path parent, not hardcoded /
- missing DB file reports size 0 and exists false
- missing WAL reports size 0 and exists false
- memory available is parsed from /proc/meminfo when present
- Prometheus is not required

Report files changed, LOC changed, tests run, and exact behavior added.
```

## Summary

Seed is ready for a local-only preflight implementation slice.

The slice should begin with local RAM and DB-path capacity checks.

Prometheus should not be involved.

Local preflight is a runtime safety/readiness boundary before provider acquisition, not provider observation and not a new ontology concept.
