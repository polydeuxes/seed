# Observation Versus Mutation Reconciliation

## Purpose

This document captures a recurring distinction that repeatedly simplified architecture, capability design, risk classification, and operator workflows.

The distinction is:

```text
Observation
    ≠
Mutation
```

## Observation

Observation answers:

```text
What is true?
What exists?
What changed?
What was observed?
```

Examples:

```text
List users.
List packages.
List services.
List firewall rules.
Read configuration.
Observe process state.
```

## Mutation

Mutation answers:

```text
Change something.
Create something.
Delete something.
Modify something.
```

Examples:

```text
Add user.
Install package.
Restart service.
Open firewall port.
Delete files.
Modify configuration.
```

## Architectural Finding

Many requests appear similar at the language level.

Examples:

```text
List users.
Add user.

List firewall rules.
Change firewall rules.

List services.
Restart service.
```

Despite similar wording, they belong to different risk classes.

## Why The Distinction Matters

Observation often permits:

```text
Read-only execution
Lower risk
Evidence acquisition
```

Mutation often requires:

```text
Policy evaluation
Approval
Rollback consideration
Risk classification
```

## Repeated Appearance

This distinction emerged repeatedly across:

```text
Homelab observation planning
Tool generation discussions
Capability proposals
Approval-path discussions
Safety reviews
```

## Relationship To Evidence

Observation frequently produces:

```text
Facts
Evidence
Observations
```

Mutation frequently produces:

```text
Actions
Side effects
State changes
```

The two should not be conflated.

## Non-Goals

This finding does not prohibit mutation.

It simply recommends that mutation be recognized explicitly.

## Current Conclusion

One of the simplest useful classifications available to Seed is:

```text
Observation
or
Mutation
```

This distinction consistently reduces ambiguity and improves safety boundaries.
