# Local CLI Responsibility Boundary Audit

## Purpose

This audit reviews `scripts/seed_local.py` after the local-host mount rendering work exposed a responsibility-boundary risk.

The triggering concern was that mount filesystem taxonomy and collapse policy initially landed directly in the CLI script.

That specific issue was corrected by moving mount classification policy into `seed_runtime/local_host_mounts.py`.

This audit asks whether the local CLI is still at risk of becoming a second domain system.

## Central Question

```text
What should scripts/seed_local.py own?
```

Working answer:

```text
Argument parsing
Local orchestration
Read-model dispatch
CLI formatting
```

It should not own:

```text
Domain taxonomy
Classification policy
Projection semantics
Evidence semantics
Capability policy
Runtime behavior
```

## Current Observed Shape

`scripts/seed_local.py` is a large local operator entry point.

It currently owns several categories of behavior:

```text
CLI argument parsing
Local app construction
Development seeding helpers
Observation-source orchestration
Projected state loading/cache access
Read-model formatting
Impact view composition
HTTP shim behavior
```

This is not automatically wrong.

A local CLI can own orchestration and rendering.

The risk is when rendering logic starts accumulating domain policy.

## Boundary That Was Successfully Restored

Mount classification policy no longer belongs to the CLI.

The corrected boundary is:

```text
seed_runtime/local_host_mounts.py
    owns mount classification and operator-impact grouping policy

scripts/seed_local.py
    owns text rendering of already-classified mount impact output
```

This is the correct direction.

## Acceptable CLI Responsibilities

The following responsibilities appear appropriate for the CLI:

```text
Parsing flags
Validating mutually exclusive command combinations
Opening the selected ledger/cache
Calling runtime/read-model services
Formatting terminal text
Choosing which formatter to invoke for a requested command
```

These are local operator concerns rather than domain authority.

## Potential Responsibility Leaks

## 1. Impact View Composition

`format_entity_impact(...)` still directly chooses impact sections and predicate families.

Examples:

```text
identity predicates
mount predicates
storage predicates
listener predicates
network predicates
```

This may be acceptable as CLI view composition for now.

However, if impact grows further, the responsibility may belong in a runtime read-model module such as:

```text
seed_runtime/impact_views.py
```

or local-host-specific view modules.

Risk:

```text
The CLI becomes the owner of what an entity impact view means.
```

## 2. Network Impact Grouping

The CLI currently owns some network impact grouping behavior, including interface role display, visible/collapsed interface groups, address grouping, and DNS resolver formatting.

This resembles the mount issue.

It may be acceptable as formatting while small.

If the network grouping rules grow, they should move into runtime-owned local-host network view helpers.

Possible future module:

```text
seed_runtime/local_host_networks.py
```

Boundary to preserve:

```text
Runtime helper owns local-host network classification/grouping policy.
CLI owns terminal rendering.
```

## 3. State Summary Composition

`state_summary(...)` builds a concise operator summary directly in the CLI script.

It calculates entity counts, fact counts, durable/current measurement counts, top entities, availability counts, and filesystem summaries.

This is not pure string formatting.

It is read-model composition.

If used beyond the CLI, it should move into runtime read-model code.

Possible future module:

```text
seed_runtime/state_summary.py
```

or an extension of existing state view modules.

## 4. Event Summary Semantics

The CLI owns compact event-summary text such as extracting subject/predicate from observation and fact events.

This is probably acceptable as debug formatting.

If event summaries become used by other surfaces, move them into runtime-owned event view helpers.

## 5. Development Seeding Helpers

The CLI still owns dev-only fact/observation/provider seed helpers.

This appears acceptable because the helpers are explicitly local-development entry points.

However, they should remain clearly labeled as CLI/dev shims and should not become canonical ingestion APIs.

## Non-Issues Observed

The following do not currently look like boundary problems:

```text
Argument parser construction
Mutually exclusive CLI command validation
Opening/closing SQLite ledgers and projection stores
Calling existing read-model builders
Plain terminal formatting for already-computed views
```

These are expected CLI responsibilities.

## Recommended Next Work

Do not immediately split everything.

The next safe step is documentation and characterization.

Recommended sequence:

```text
1. Preserve this audit.
2. Avoid adding new domain classification policy to scripts/seed_local.py.
3. When touching network impact, state summary, or impact composition, first ask whether the rule belongs in runtime read-model code.
4. Add tests that make ownership boundaries explicit when new helpers are moved.
```

Potential future implementation candidates:

```text
Move network impact classification helpers to seed_runtime/local_host_networks.py.
Move state_summary composition to runtime read-model code.
Move entity impact view composition into seed_runtime/impact_views.py if it continues to grow.
```

## Current Conclusion

`scripts/seed_local.py` is currently doing too much, but not everything it does is wrong.

The immediate architectural risk is not file size alone.

The risk is domain authority accumulating in the CLI.

The mount fix restored one boundary.

Future changes should preserve the rule:

```text
CLI renders.
Runtime owns domain classification and read-model authority.
```
