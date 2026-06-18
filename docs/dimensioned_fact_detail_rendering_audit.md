# Dimensioned Fact Detail Rendering Audit

## Purpose

This audit reviews a rendering problem exposed by Local Users Observation v1.

The operator inspected group membership facts with:

```text
--current-facts example_host group_member
--fact-support example_host group_member
```

The output showed repeated values such as:

```text
value: user
value: user
value: user
```

The underlying facts are likely distinct because their dimensions differ, for example:

```text
groupname=sudo
username=user
gid=27
```

However the detail surfaces did not show those dimensions clearly enough.

## Central Finding

```text
For dimensioned facts, value alone is not always meaningful.
```

A fact's identity may depend on:

```text
subject
predicate
value
dimensions
```

If detail surfaces hide dimensions, distinct facts can appear duplicated or ambiguous.

## Current Trigger

The `group_member` predicate intentionally uses host-subject facts with dimensions.

Example:

```text
subject: example_host
predicate: group_member
value: user
dimensions:
    groupname: sudo
    gid: 27
    username: user
```

This preserves the local users audit boundary because it does not introduce User entities or relationship semantics.

But it also means dimensions carry critical meaning.

Rendering only:

```text
value: user
```

is insufficient.

## Scope

This is not a users observation bug.

This is a detail-surface rendering bug.

The user facts appear to exist.

The missing piece is readable dimension presentation in surfaces that claim to show evidence/detail.

## Surfaces Affected

### Current Facts

`--current-facts SUBJECT PREDICATE` should show dimensions when facts have dimensions.

Current Facts is an evidence inspection surface.

It should not hide fields required to distinguish facts.

### Fact Support

`--fact-support SUBJECT PREDICATE` should show dimensions for each supported fact or support group.

Fact Support owns provenance and justification.

When dimensions define the supported claim, provenance without dimensions is incomplete.

## Rendering Guidance

Acceptable compact shapes include:

```text
value: user (groupname=sudo, gid=27, username=user)
```

or:

```text
value: user
dimensions: gid=27, groupname=sudo, username=user
```

The exact formatting is less important than preserving deterministic, visible dimensions.

Dimension keys should be sorted for stable output.

## General Rule

Detail surfaces should render dimensions for any dimensioned fact.

This should not be special-cased to `group_member`.

Examples of future dimensioned facts may include:

```text
mount facts
filesystem facts
network interface facts
listening endpoint facts
package facts
user facts
group facts
```

The rule should be generic.

## Boundary With Aggregation

This audit does not require changing fact aggregation semantics.

It does not require changing fact identity.

It does not require changing support grouping.

It only requires that dimensioned facts remain distinguishable when rendered.

If multiple fact support records have the same value but different dimensions, they may remain separate.

They must not appear identical to the operator.

## Boundary With User Modeling

This audit does not reopen user observation design.

It does not require introducing User entities.

It does not require creating group membership relationships.

It does not require changing `group_member` value shape.

The current host-subject fact model remains acceptable.

The rendering must expose the dimensions that make that model readable.

## Non-Goals

This audit does not add new predicates.

It does not add new observations.

It does not change Local Users Observation v1.

It does not add user summaries to State Summary.

It does not add Impact user rendering.

It does not change availability, alias, or package semantics.

It does not change Runtime or ToolExecutor behavior.

## Recommended Small Fix

Update Current Facts and Fact Support formatting so dimensioned facts display their dimensions deterministically.

Likely requirements:

```text
- Render dimensions whenever fact.dimensions is non-empty.
- Sort dimension keys.
- Preserve existing output for dimensionless facts as much as possible.
- Add characterization tests using at least group_member-style fixture facts.
```

Expected improvement:

```text
Before:
    value: user
    value: user

After:
    value: user
    dimensions: gid=27, groupname=sudo, username=user

    value: user
    dimensions: gid=999, groupname=docker, username=user
```

## Current Conclusion

Dimensioned facts are valid and useful, but only if detail surfaces display their dimensions.

Local Users Observation v1 exposed the problem because group membership naturally repeats user names across different groups.

The right fix is not to redesign users.

The right fix is to make evidence/detail rendering honor dimensioned fact identity.