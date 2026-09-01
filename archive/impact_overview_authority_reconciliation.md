# Impact Overview Authority Reconciliation

## Purpose

This document reconciles the authority of the default entity impact surface.

The triggering concern is that `--impact ENTITY` is currently doing useful work, but it risks becoming too large as Seed begins collecting more fact families.

The question is:

```text
What belongs in the impact overview,
and what must be deferred to impact sections or evidence surfaces?
```

## Current Context

Recent audits established the following surface boundaries:

```text
State Summary
    repository overview / inventory

Impact
    entity overview

Impact Section
    entity drilldown

Current Facts
    evidence inspection

Fact Support
    provenance
```

The remaining ambiguity is the authority of the default impact surface.

If Seed later observes packages, users, firewall rules, systemd units, containers, scheduled jobs, capabilities, purpose, and hardware inventory, the default impact output cannot include every detail without becoming another evidence dump.

This is a volume pressure, not an intent change.

## Central Finding

```text
Impact overview should summarize entity significance.
```

It should not be a complete listing of everything known about the entity.

The overview should answer:

```text
What is this entity?
What important domains are known about it?
What risks, gaps, or unusual conditions are visible?
Where should the operator drill down next?
```

It should not answer:

```text
What is every observed fact?
What is every member of every domain?
What exact source produced this claim?
```

Those questions belong to section drilldowns, current facts, and fact support.

## Surface Contract

A stable working contract is:

```text
State Summary
    What exists in the repository?

Impact Overview
    What matters about this entity?

Impact Section
    What matters within this domain for this entity?

Current Facts
    What was observed?

Fact Support
    Where did it come from?
```

This preserves the operator path:

```text
repository overview
        ↓
entity overview
        ↓
entity domain drilldown
        ↓
raw evidence
        ↓
provenance
```

## What Impact Overview Owns

The default impact overview owns compact interpretation.

It may show:

```text
entity identity
entity type / role when known
high-level domain presence
compact counts
notable risks or gaps
integrity concerns relevant to the entity
recommended drilldown directions
```

Examples:

```text
mounts: 8 operator-relevant, 45 collapsed system/docker mounts
network: primary eno1, loopback present, 28 virtual/container/vpn interfaces collapsed
listeners: 52 endpoints observed
storage: 14 devices, 10 partitions, 7 mounted block-device relationships
users: observed, drilldown available
firewall: not observed
packages: not observed
```

These statements are summaries, not exhaustive inventories.

## What Impact Overview Should Avoid

The default impact overview should avoid:

```text
long mount listings
full interface inventories
full listener inventories
raw package lists
raw user lists
raw firewall rule listings
raw systemd unit listings
raw container inventories
source/provenance details
repeated evidence rows
```

These may be valid information, but they are not overview information.

## What Impact Sections Own

Impact sections own focused interpretation for one domain.

Examples:

```text
--impact ENTITY --section mounts
    visible mounts
    collapsed mount group counts
    operator-relevant mount interpretation

--impact ENTITY --section network
    primary interfaces
    loopback
    vpn/container/virtual groupings
    address interpretation

--impact ENTITY --section storage
    devices
    partitions
    mount relationships
    topology interpretation

--impact ENTITY --section listeners
    listening endpoints
    role grouping
    non-inference guardrails

--impact ENTITY --section users
    observed users
    privilege-relevant interpretation
    unknowns and caveats

--impact ENTITY --section firewall
    observed rules
    exposed/blocked interpretation
    unknowns and caveats
```

Sections may be more verbose than the overview, but they remain interpretation surfaces.

They still should not become raw evidence dumps.

## What Current Facts Owns

`--current-facts` owns raw scoped evidence.

It is allowed to be grep-friendly, verbose, and mechanically complete.

Examples:

```text
all observed mount facts
all observed interface facts
all observed listener facts
all observed package facts
all observed user facts
all observed firewall facts
```

Current Facts is the right place for completeness.

Impact Overview is the wrong place for completeness.

## What Fact Support Owns

`--fact-support` owns provenance and justification.

It answers:

```text
Which observation supports this fact?
What source produced it?
What evidence path led to it?
```

Impact Overview may indicate that evidence exists, but it should not inline provenance details by default.

## Detail Placement Table

| Information | Impact Overview | Impact Section | Current Facts | Fact Support |
| --- | --- | --- | --- | --- |
| Entity identity | yes | yes | yes | support when needed |
| Domain presence | yes | yes | yes | support when needed |
| Domain count | yes | yes | yes | support when needed |
| Mount summary | yes | yes | yes | support when needed |
| Full mount list | no | yes | yes | support when needed |
| Interface summary | yes | yes | yes | support when needed |
| Full interface list | no | yes | yes | support when needed |
| Listener summary | yes | yes | yes | support when needed |
| Full listener list | no | yes | yes | support when needed |
| Storage topology summary | yes | yes | yes | support when needed |
| Raw storage facts | no | no | yes | support when needed |
| Package summary | yes | yes | yes | support when needed |
| Raw package list | no | maybe | yes | support when needed |
| User summary | yes | yes | yes | support when needed |
| Raw user list | no | maybe | yes | support when needed |
| Firewall summary | yes | yes | yes | support when needed |
| Raw firewall rules | no | maybe | yes | support when needed |
| Provenance details | no | no | maybe | yes |

`maybe` means the section may include a curated or grouped version, but the raw complete version remains owned by Current Facts.

## Volume Pressure Does Not Change Intent

Seed currently collects a limited set of local-host facts.

As observation expands, the overview may need stricter summarization.

That does not change the authority of the surface.

The rule remains:

```text
More facts should create better summaries and better drilldowns,
not larger default overviews.
```

If a new fact family cannot fit into the overview without becoming noisy, the answer should be:

```text
add or improve a section
```

not:

```text
append the whole fact family to --impact ENTITY
```

## Boundary With CLI Responsibility

The CLI should not own impact meaning.

The long-term boundary should remain:

```text
runtime/read-model helper
    owns impact overview composition
    owns section composition
    owns domain policy

CLI
    owns arguments
    owns terminal rendering
```

A future implementation may introduce helpers such as:

```text
seed_runtime/impact_views.py
```

or local-host-specific read-model helpers.

The exact module name is less important than preserving the ownership boundary.

## Non-Goals

This document does not require immediate implementation.

It does not require adding `--section` immediately.

It does not require reducing current impact output before a section path exists.

It does not change Current Facts or Fact Support.

It does not define final output formatting.

It does not decide how much summarization is appropriate once additional fact families exist.

## Future Implementation Guidance

When implementation begins, prompts should explicitly preserve:

```text
--impact ENTITY remains the entity overview.
--impact ENTITY --section SECTION is the entity domain drilldown.
--current-facts remains raw scoped evidence.
--fact-support remains provenance.
Runtime/read-model helpers own semantic composition.
CLI owns argument parsing and terminal rendering.
```

Tests should verify at least:

```text
default impact does not expand full raw domain inventories
section output contains focused domain interpretation
current-facts still exposes raw evidence
fact-support still exposes provenance
unknown or unsupported sections fail clearly
```

## Current Conclusion

Impact Overview should remain an operator landing page for one entity.

Its authority is significance, not completeness.

As Seed observes more facts, the overview should become more selective, not more exhaustive.

The intended path is:

```text
State Summary
        ↓
Impact Overview
        ↓
Impact Section
        ↓
Current Facts
        ↓
Fact Support
```

This keeps the default impact surface useful while preserving drilldown and evidence paths for operators who need detail.
