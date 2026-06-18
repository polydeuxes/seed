# Operator Navigation Reconciliation

## Purpose

This audit reviews how operators move between Seed read surfaces.

The triggering observation is that recent audits repeatedly found that useful information already existed, but operators were not naturally guided to it.

The question is:

```text
How does an operator discover
what to look at next?
```

This is a navigation question rather than an acquisition question.

## Background

Recent authority audits produced a progressively clearer surface model:

```text
State Summary
    repository overview

Impact Overview
    entity overview

Impact Section
    entity domain drilldown

Current Facts
    evidence inspection

Fact Support
    provenance
```

Each surface answers a different question.

The remaining challenge is helping operators move between them.

## Central Finding

```text
A useful read surface should not only answer a question.

It should suggest the next question.
```

A surface that requires the operator to already know the rest of the system is difficult to discover.

A surface that naturally points toward deeper inspection is easier to learn.

## Observed Pattern

Several recent investigations followed the same shape:

```text
Unexpected output
        ↓
Audit
        ↓
Information already existed
        ↓
Navigation was weak
```

Examples include:

```text
Current Facts dimensions
Mount interpretation
Integrity inventories
Entity impact information
```

The issue was often not missing information.

The issue was discovering where the information lived.

## Navigation Hierarchy

The current hierarchy naturally forms a ladder:

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

Each step increases detail.

Each step narrows scope.

## Surface Questions

### State Summary

Primary question:

```text
What exists in the repository?
```

Potential next questions:

```text
What matters about this entity?
What integrity concern should I investigate?
```

Natural navigation targets:

```text
Impact
Integrity Summary
Capability Status
Entity-specific views
```

State Summary should help operators discover meaningful entities and investigation directions.

It should not require operators to already know what to inspect.

## Impact Overview

Primary question:

```text
What matters about this entity?
```

Potential next questions:

```text
Which domain deserves investigation?
Which concern should I inspect further?
```

Natural navigation targets:

```text
Impact Sections
Current Facts
Integrity Surfaces
```

Impact should function as a landing page.

Its role is not only summarization.

Its role is directional guidance.

## Impact Section

Primary question:

```text
What matters within this domain?
```

Potential next questions:

```text
What was actually observed?
What evidence supports this interpretation?
```

Natural navigation targets:

```text
Current Facts
Fact Support
```

A section should stop before becoming a raw evidence inventory.

Its purpose is focused interpretation.

## Current Facts

Primary question:

```text
What was observed?
```

Potential next questions:

```text
Where did this fact come from?
Why does this fact exist?
```

Natural navigation target:

```text
Fact Support
```

Current Facts should remain evidence-oriented.

However evidence becomes easier to trust when provenance is discoverable.

## Fact Support

Primary question:

```text
Why should I believe this fact?
```

Fact Support is the end of the investigation chain.

It owns provenance.

Further navigation is generally unnecessary.

## Navigation Authority

A useful distinction:

```text
Navigation
        ≠
Ownership
```

A surface may recommend another surface.

That does not transfer authority.

Example:

```text
Impact
    may point to Current Facts

Current Facts
    still owns evidence
```

Likewise:

```text
Current Facts
    may point to Fact Support

Fact Support
    still owns provenance
```

Navigation should reinforce boundaries rather than blur them.

## Candidate Navigation Rules

A simple working model:

```text
Every surface should answer:

    What am I looking at?

and

    What should I inspect next?
```

The answer may be explicit or implicit.

The important property is discoverability.

## Future Navigation Hints

Possible future implementations could include:

```text
See:
    --impact example_host

See:
    --impact example_host --section network

See:
    --current-facts example_host interface

See:
    --fact-support example_host interface
```

These are examples rather than implementation requirements.

The audit concerns authority and operator flow.

Not output formatting.

## Relationship To Existing Audits

This audit complements:

```text
State Summary Authority
Impact Overview Authority
Impact Drilldown Reconciliation
CLI Responsibility Boundary
Integrity Navigation
```

Those audits establish:

```text
What each surface owns
```

This audit establishes:

```text
How operators move between surfaces
```

## Non-Goals

This document does not require implementation.

It does not require adding navigation hints immediately.

It does not define command syntax.

It does not alter ownership boundaries.

It does not create new read models.

It does not redefine any existing surface.

## Future Implementation Guidance

If navigation hints are added, prompts should preserve:

```text
Navigation does not change authority.

State Summary remains repository overview.
Impact remains entity overview.
Impact Sections remain domain interpretation.
Current Facts remain evidence.
Fact Support remains provenance.
```

Tests should verify:

```text
Navigation hints are deterministic.
Navigation hints reference valid surfaces.
Navigation hints do not duplicate owned information.
Navigation hints do not change surface authority.
```

## Current Conclusion

Seed's read surfaces are becoming increasingly well-defined.

The next operator-experience opportunity is likely not additional information.

It is helping operators discover existing information.

The intended navigation path is:

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

Each surface should answer its own question while helping the operator discover the next one.