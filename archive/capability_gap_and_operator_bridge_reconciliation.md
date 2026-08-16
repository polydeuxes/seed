# Capability Gap And Operator Bridge Reconciliation

## Purpose

This document captures a recurring pattern observed across implementation work, repository audits, operator trials, and tool usage.

The finding is:

```text
A missing capability is not a reasoning problem.
```

## Recurring Failure Mode

Systems often react to a missing capability by attempting additional reasoning.

Pattern:

```text
Need
    ↓
Reason harder
```

This frequently produces approximation, compensation, or speculation.

## Preferred Pattern

```text
Need
    ↓
Identify capability gap
    ↓
Surface limitation
    ↓
Bridge capability gap
```

## Examples

### Relationship Reconciliation

Behavior-oriented reconciliation appeared to require additional reasoning.

The actual blocker was:

```text
Missing relationship evidence.
```

The solution became:

```text
RelationshipFact
```

rather than stronger inference.

### Utility Requests

Questions involving weather, time, arithmetic, or conversion often appear reasoning-oriented.

The real requirement is usually:

```text
Deterministic utility capability.
```

### Observation Requests

Requests involving users, packages, services, or firewall rules often appear to require intelligence.

The actual blocker is often:

```text
Observation capability.
```

## Operator Bridge

Sometimes two capabilities exist independently but cannot be connected.

Example shape:

```text
Capability A

Capability B

No transfer path between them.
```

The resulting failure is not necessarily a missing endpoint.

It may be a missing bridge.

## Capability Gap Signals

Strong indicators of a capability gap:

```text
Repeated compensation
Repeated manual workarounds
Repeated explanation of limitations
Repeated operator intervention
```

## Non-Goals

This finding does not imply:

```text
Every gap deserves automation.
Every bridge should be built.
```

The goal is visibility.

## Current Conclusion

A recurring architectural lesson is:

```text
Missing capability should be surfaced
before compensation is attempted.
```

Naming the gap is often more valuable than hiding it.
