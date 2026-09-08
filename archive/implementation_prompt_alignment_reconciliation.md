# Implementation Prompt Alignment Reconciliation

## Purpose

This document preserves findings about implementation prompts discovered during operator review and Codex-assisted development.

The motivating observation was that a technically correct implementation can still violate architectural intent when alignment remains implicit.

## Central Finding

```text
Implicit alignment is not an instruction.
```

Human reviewers often assume shared architectural context.

Implementation agents operate primarily from the literal prompt and the explicit scope provided.

If a boundary is not stated, it should not be assumed to be protected.

## Example

A request to:

```text
Clean impact mount rendering.
```

appears straightforward.

However, without explicit ownership guidance, an implementation may reasonably place:

```text
filesystem taxonomy
classification policy
collapse policy
```

inside the CLI because those concepts are nearby to the rendering code.

The resulting implementation can satisfy the requested behavior while violating architectural boundaries.

## Finding: Intent Is Not Alignment

A useful distinction:

```text
Intent
    ≠
Alignment
```

Intent describes:

```text
What should change.
```

Alignment describes:

```text
What must remain true.
```

Both are required.

## Finding: Scope Is Not Boundary

A useful distinction:

```text
Scope
    ≠
Boundary
```

Scope describes:

```text
Which files and behaviors may be modified.
```

Boundary describes:

```text
Which responsibilities must remain separated.
```

A prompt can have a correct scope while still permitting boundary violations.

## Recommended Prompt Structure

Implementation prompts should explicitly include:

```text
Goal
Context
Required Change
Boundary / Ownership
Tests
Non-Goals
```

## Boundary / Ownership Section

The most important addition is:

```text
Boundary / Ownership
```

Example:

```text
seed_runtime/local_host_mounts.py
    owns mount classification policy

scripts/seed_local.py
    owns CLI rendering
```

and:

```text
Do not place filesystem taxonomy in scripts/seed_local.py.
```

This converts an assumed architectural rule into an explicit requirement.

## Finding: Update Requests Must Be Explicit

A second observation emerged during review.

Implementation agents frequently treat unspecified artifacts as out of scope.

Examples:

```text
PR descriptions
comments
docstrings
test descriptions
```

If updates are desired, the prompt should explicitly require them.

Example:

```text
Update:
- code
- tests
- comments/docstrings
- PR description
```

rather than assuming those updates will occur automatically.

## Finding: Nearby Code Attracts Responsibility

A recurring implementation pattern is:

```text
Behavior lives here.
Therefore policy is added here.
```

This is natural but dangerous.

Without explicit boundaries:

```text
CLI scripts
views
API handlers
controllers
```

tend to accumulate:

```text
classification
categorization
domain policy
business rules
```

because they are closest to the requested change.

## Operator Lesson

A useful operator question is:

```text
What incorrect implementation would still satisfy the literal request?
```

The answer often reveals missing alignment instructions.

## Relationship To Existing Findings

This document reinforces:

```text
Surface Authority Before Implementation
Evidence ≠ Interpretation
Audit Before Implementation
Boundary Preservation
```

The common theme is:

```text
Architectural intent should be made explicit before implementation begins.
```

## Current Conclusion

A correct implementation prompt should specify not only:

```text
What change is desired.
```

but also:

```text
What ownership boundaries must be preserved.
What artifacts must be updated.
What responsibilities must not move.
```

When alignment remains implicit, an implementation may satisfy the request while still violating the architecture.
