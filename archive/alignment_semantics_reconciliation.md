# Alignment Semantics Reconciliation

## Purpose

This document reconciles the current meaning of Seed's fixture-level self-model alignment outcomes.

It is documentation-only. It does not modify reconciliation behavior, runtime behavior, tests, tool execution, event storage, projection behavior, repository observation, documentation observation, or package exports.

The immediate motivation is the first end-to-end fixture proof:

```text
Documentation text
        ↓
DocumentationClaim

Repository source text
        ↓
RepositoryArtifactFact

DocumentationClaim
+
RepositoryArtifactFact
        ↓
AlignmentRecord
```

Once that spine exists, the most important question becomes:

```text
What does each AlignmentRecord outcome actually mean?
```

## Current Outcome Vocabulary

The current fixture-level alignment vocabulary is:

```text
supported
missing_support
potential_conflict
not_evaluable
```

These are not truth values.

They are reconciliation outcomes for a supplied documentation claim against supplied repository artifact facts under the currently implemented v0 rules.

## Central Distinction

Alignment outcomes answer:

```text
Given this claim, these artifact facts, and these narrow rules,
what support relationship can v0 report?
```

They do not answer:

```text
Is this claim absolutely true?
```

or:

```text
Does the whole repository prove this claim?
```

or:

```text
Should Seed execute anything?
```

## Outcome Definitions

### `supported`

`supported` means:

```text
The v0 rule recognized the claim family and claim pattern,
and the supplied artifact facts satisfy the rule's support condition.
```

Examples:

- `ToolExecutor owns registered-operation execution.` is supported when supplied artifact facts mention `ToolExecutor`.
- `ProjectionStore owns cached projected-state snapshots.` is supported when supplied artifact facts mention `ProjectionStore`, `SQLiteProjectionStore`, or `InMemoryProjectionStore`.
- `ResponseEngine is rejected.` is supported when the rejected-concept rule recognizes the claim and no supplied artifact fact mentions `ResponseEngine`.
- `Users Observation is a current capability-growth priority.` is supported when the frontier rule recognizes the claim and no supplied artifact fact mentions the frontier as implemented.

`supported` does not mean:

- globally true;
- fully verified;
- semantically proven;
- supported by every relevant repository file;
- safe to act on;
- exempt from later contradiction.

### `missing_support`

`missing_support` means:

```text
The v0 rule recognized the claim family and claim pattern,
expected a supporting artifact fact,
and did not find one in the supplied artifact facts.
```

In current v0 semantics, this is used narrowly for known ownership subjects where the rule knows what artifact support should look like.

Examples:

- A `ProjectionStore` ownership claim with no supplied `ProjectionStore`, `SQLiteProjectionStore`, or `InMemoryProjectionStore` artifact fact.
- A `ToolExecutor` ownership claim with no supplied `ToolExecutor` artifact fact.

`missing_support` does not mean:

- the claim is false;
- the repository lacks support globally;
- the required artifact does not exist anywhere;
- the concept is rejected;
- the claim should become a conflict.

It only means the current supplied artifact facts did not satisfy a recognized support rule.

### `potential_conflict`

`potential_conflict` means:

```text
The v0 rule recognized the claim family and claim pattern,
and supplied artifact facts mention something that may conflict with the claim.
```

Examples:

- A rejected-concept claim such as `ResponseEngine is rejected.` with supplied artifact facts mentioning `ResponseEngine`.
- A frontier claim such as `Users Observation is a current capability-growth priority.` with supplied artifact facts matching the frontier implementation names recognized by the current rule.

`potential_conflict` does not mean:

- definite contradiction;
- semantic proof of disagreement;
- implementation is wrong;
- documentation is wrong;
- human review has completed.

It means the current rule found evidence worth inspecting because it may undermine the claim.

### `not_evaluable`

`not_evaluable` means:

```text
The claim cannot be evaluated by current v0 rules.
```

This may happen because:

- the claim family is unsupported;
- the claim text does not match a supported v0 pattern;
- the ownership subject is not one of the current explicit ownership rules;
- the rejected-concept text does not match the current rejected-concept pattern;
- the frontier text does not match the current frontier pattern.

Example:

- `MagicExecutor owns all execution.` is an ownership claim, but current v0 ownership reconciliation only knows explicit rules for `ProjectionStore` and `ToolExecutor`. Therefore it is `not_evaluable`, not `missing_support`.

`not_evaluable` does not mean:

- unsupported;
- false;
- missing from the repository;
- irrelevant;
- impossible to evaluate later.

It means the present rule set does not know how to evaluate the claim.

## Missing Support vs Not Evaluable

This distinction is important.

```text
missing_support
```

means:

```text
The rule knew what support should look like and did not find it.
```

```text
not_evaluable
```

means:

```text
The rule did not know how to evaluate this claim.
```

For example:

| Claim | Supplied artifacts | Current outcome | Reason |
| --- | --- | --- | --- |
| `ToolExecutor owns registered-operation execution.` | no `ToolExecutor` fact | `missing_support` | v0 knows the ToolExecutor ownership rule and expected a matching artifact. |
| `MagicExecutor owns all execution.` | no `MagicExecutor` fact | `not_evaluable` | v0 does not have a MagicExecutor ownership rule. |

The second case should not be called `missing_support` unless a future rule explicitly decides that all ownership claims are evaluable by symbol search.

## Potential Conflict vs Missing Support

This distinction is also important.

```text
missing_support
```

means expected support was absent.

```text
potential_conflict
```

means evidence appeared that may undermine the claim.

For rejected-concept claims:

```text
ResponseEngine is rejected.
```

- no `ResponseEngine` artifact mention -> `supported`
- `ResponseEngine` artifact mention -> `potential_conflict`

For ownership claims:

```text
ToolExecutor owns registered-operation execution.
```

- `ToolExecutor` artifact mention -> `supported`
- no `ToolExecutor` artifact mention -> `missing_support`

The two outcomes are not interchangeable.

## Frontier Semantics

Current frontier semantics are intentionally inverted compared with ownership support.

A frontier claim means something like:

```text
This capability is still a frontier / priority / not-yet-complete area.
```

Therefore:

- no matching implementation artifact -> `supported`
- matching implementation artifact -> `potential_conflict`

This does not mean implemented frontier work is bad. It means the documentation claim that the item is still a frontier may need review once matching artifacts appear.

Current v0 frontier matching is conservative. It recognizes explicit normalized forms such as:

```text
Users Observation
UsersObservation
users_observation
```

It does not automatically treat every plausible helper name, such as `observe_users`, as the frontier implementation unless reconciliation rules explicitly define that mapping.

## Rejected Concept Semantics

A rejected-concept claim means documentation says a concept should not exist or should not be introduced.

Current v0 behavior:

- no artifact fact mentions the rejected concept -> `supported`
- any artifact fact mentions the rejected concept -> `potential_conflict`
- text does not match the rejected-concept pattern -> `not_evaluable`

This is intentionally conservative.

A matching artifact fact does not prove the rejection was violated. It may be a historical reference, test fixture, documentation mention, or compatibility artifact. The correct v0 output is therefore `potential_conflict`, not definite conflict.

## Ownership Semantics

An ownership claim says a named component owns a responsibility.

Current v0 ownership support is explicit rather than general.

Supported ownership subjects currently include:

- `ProjectionStore`, supported by `ProjectionStore`, `SQLiteProjectionStore`, or `InMemoryProjectionStore` artifact facts.
- `ToolExecutor`, supported by `ToolExecutor` artifact facts.

Current v0 behavior:

- recognized ownership subject + matching artifact fact -> `supported`
- recognized ownership subject + no matching artifact fact -> `missing_support`
- unrecognized ownership subject -> `not_evaluable`

This prevents v0 from pretending it can evaluate arbitrary ownership claims.

## Non-Goals

Alignment outcomes are not:

- truth judgments;
- confidence scores;
- proof objects;
- graph conclusions;
- runtime decisions;
- policy decisions;
- execution permissions;
- repository-wide search results;
- human review results.

They are narrow records produced by deterministic reconciliation rules over supplied claim and artifact records.

## Future Semantics Boundary

Future work may add:

- more claim families;
- broader ownership rules;
- explicit contradiction outcomes;
- support strength;
- confidence or certainty metadata;
- human review state;
- repository-wide artifact acquisition;
- projection/read-model integration.

Those additions should not blur the current distinctions.

In particular:

- Do not turn `not_evaluable` into `missing_support` without an explicit rule that defines expected support.
- Do not turn `potential_conflict` into definite contradiction without stronger evidence semantics.
- Do not turn `supported` into truth.
- Do not treat lack of supplied artifacts as repository-wide absence unless repository-wide acquisition is explicitly in scope.

## Documentation-Only Status

This reconciliation documents current semantics only. It does not modify production code, tests, reconciliation rules, runtime behavior, repository observation, documentation observation, tool execution, event storage, projection behavior, or package exports.
