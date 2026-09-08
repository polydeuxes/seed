# Entity Impact Drilldown Reconciliation

## Purpose

This document reconciles the role of `--impact` as Seed accumulates more observed local-host facts and future entity evidence.

The motivating concern is that an impact view can become unreadable if it tries to include every relevant detail directly in the overview.

## Central Finding

```text
A useful impact view should not expand endlessly.
```

An impact view should summarize what matters and route the operator to focused drilldowns.

## Current Context

Local-host impact currently includes sections such as:

```text
identity
local network configuration
mounts
storage topology
listening endpoints
endpoint availability by role
groups/dependencies/dependents
conflicts
graph issues
```

Recent work improved mount rendering by collapsing noisy mount groups while preserving raw evidence in `--current-facts`.

However, future observation areas are likely to add more sections.

Examples:

```text
packages
capabilities
purpose
services
users
firewall rules
scheduled jobs
containers
systemd units
hardware inventory
```

If all of this is placed directly into the default impact output, the operator view will become another evidence dump.

## View Boundary

The established read-surface boundary remains:

```text
--current-facts
    raw scoped evidence / grep surface

--fact-support
    provenance / justification surface

--impact
    operator interpretation surface
```

The new distinction is:

```text
impact overview
    ≠
impact drilldown
```

## Proposed Shape

A better long-term shape is:

```text
--impact ENTITY
    overview / landing page

--impact ENTITY --section mounts
    focused mount interpretation

--impact ENTITY --section network
    focused network interpretation

--impact ENTITY --section storage
    focused storage interpretation

--impact ENTITY --section listeners
    focused listener interpretation
```

Future sections may include:

```text
--impact ENTITY --section packages
--impact ENTITY --section capabilities
--impact ENTITY --section purpose
--impact ENTITY --section services
--impact ENTITY --section users
--impact ENTITY --section firewall
```

## Operator Flow

A useful operator flow is:

```text
overview
        ↓
focused drilldown
        ↓
raw facts / support evidence
```

Example:

```text
--impact node
        ↓
--impact node --section network
        ↓
--current-facts node ip_address
        ↓
--fact-support node ip_address
```

Each surface answers a different question.

## What The Overview Should Own

The overview should answer:

```text
What is this entity?
What are the most important observed domains?
What high-level risks or gaps are visible?
Where should the operator drill down?
```

The overview may include compact summaries such as:

```text
mounts: 8 operator-relevant, 45 collapsed system/docker mounts
network: primary eno1, loopback, 28 virtual/container/vpn collapsed
listeners: 52 endpoints observed
storage: 14 devices, 10 partitions, 7 mounted block-device relationships
```

The overview should avoid long exhaustive listings.

## What Drilldowns Should Own

Drilldowns should answer:

```text
What matters within this domain?
```

Examples:

```text
mount drilldown
    visible mounts plus collapsed group counts

network drilldown
    primary/loopback/vpn/container interface details

storage drilldown
    devices, partitions, mount relationships

listener drilldown
    listening endpoints and non-inference guardrails
```

Drilldowns may be more verbose than the overview, but still remain interpretation surfaces.

Raw evidence remains in `--current-facts`.

## Relationship To CLI Boundary Audits

This finding reinforces the local CLI boundary audits.

As impact grows, the risk increases that `scripts/seed_local.py` becomes the owner of impact semantics.

Long-term, impact composition may need a runtime-owned read model such as:

```text
seed_runtime/impact_views.py
```

or local-host-specific runtime view helpers.

The CLI should not own the meaning of each section.

It should render the selected view.

## Non-Goals

This document does not require immediate implementation.

It does not require changing current `--impact` output immediately.

It does not require removing details from existing drilldown-like sections until a section mechanism exists.

It does not change `--current-facts` or `--fact-support`.

## Future Implementation Guidance

If implementing drilldowns, prompts should explicitly preserve boundaries:

```text
--impact ENTITY remains the overview.
--impact ENTITY --section SECTION provides focused interpretation.
--current-facts remains raw scoped evidence.
--fact-support remains provenance.
Runtime read-model helpers own section composition.
CLI owns argument parsing and terminal rendering.
```

Tests should distinguish:

```text
overview output
section output
evidence output
support output
```

## Current Conclusion

Seed should treat `--impact` as an operator landing page, not as an infinitely expanding report.

As new observation domains arrive, the correct path is likely:

```text
overview summary
        +
section drilldowns
        +
raw evidence navigation
```

rather than adding every new fact family directly to the default impact output.
