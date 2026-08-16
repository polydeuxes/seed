# Existence Claim Reconciliation

## Purpose

This document reconciles the intended semantics for Repository Reconciliation v1's first implementation slice: explicit existence-claim reconciliation.

It is documentation-only. It does not modify production code, tests, runtime behavior, repository observation, documentation observation, tool execution, event storage, projection behavior, or package exports.

The goal is to define a small, safe claim family that can be implemented before ownership reconciliation is generalized.

## Motivation

`docs/repository_reconciliation_v1_frontier.md` argues that ownership claims should not be generalized by symbol existence alone.

These two claims are different:

```text
ToolExecutor exists.
```

```text
ToolExecutor owns registered-operation execution.
```

The first can be supported by direct repository artifact facts such as class or module facts. The second requires stronger behavioral or boundary evidence.

Existence claims are therefore the safest next reconciliation slice.

## Claim Family

Add a future claim family named:

```text
existence
```

An existence claim asserts that a named repository artifact exists or that a named artifact defines another named artifact.

This family should be narrower than ownership, boundary, status, or frontier claims.

## Supported Claim Forms

The first implementation should support only explicit forms.

### `X exists.`

Meaning:

```text
The claim asserts that an artifact named X exists in the supplied repository artifact facts.
```

Examples:

```text
ToolExecutor exists.
ProjectionStore exists.
Runtime exists.
```

Expected evidence:

- a `RepositoryArtifactFact` whose `symbol` is `X`; or
- a conservatively equivalent artifact fact where the symbol/fact/path directly mentions `X` according to the implementation's existing matching rules.

Preferred evidence kinds:

- `class`;
- `function`;
- `module`;
- `import` only when the claim is explicitly about an import or dependency.

### `X defines Y.`

Meaning:

```text
The claim asserts that artifact X defines or contains artifact Y.
```

Examples:

```text
Runtime defines handle_user_message.
ToolExecutor defines execute.
```

Expected evidence:

- an artifact fact for `X`;
- an artifact fact for `Y`; and
- both artifact facts originate from the same supplied source path.

Same path is the complete support boundary for this existence rule. Do not infer AST containment, method ownership, class-member relationships, behavior, or structure from this form. It only says both named definitions exist within the same supplied artifact path.

## Outcome Semantics

Use the existing alignment outcomes:

```text
supported
missing_support
potential_conflict
not_evaluable
```

Do not add new outcomes for this slice.

### `supported`

Use `supported` when:

```text
The existence claim pattern is recognized,
and the supplied artifact facts contain the required artifact evidence.
```

Examples:

| Claim | Supplied artifact facts | Outcome |
| --- | --- | --- |
| `ToolExecutor exists.` | class fact with `symbol="ToolExecutor"` | `supported` |
| `Runtime defines handle_user_message.` | class fact `Runtime` and function fact `handle_user_message` from the same source path | `supported` |

### `missing_support`

Use `missing_support` when:

```text
The existence claim pattern is recognized,
and the supplied artifact facts do not contain the required artifact evidence.
```

Examples:

| Claim | Supplied artifact facts | Outcome |
| --- | --- | --- |
| `MagicExecutor exists.` | class fact `ToolExecutor` only | `missing_support` |
| `Runtime defines handle_user_message.` | class fact `Runtime` only | `missing_support` |
| `Runtime defines handle_user_message.` | class fact `Runtime` and function fact `handle_user_message` from different source paths | `missing_support` |

This means only that support is missing from the supplied artifact facts. It does not prove repository-wide absence unless repository-wide acquisition is explicitly in scope.

### `not_evaluable`

Use `not_evaluable` when:

```text
The claim does not match a supported existence pattern.
```

Examples:

```text
ToolExecutor appears important.
Runtime probably has a user-message path.
Execution capability is present.
```

These may be meaningful prose, but they are not explicit v1 existence claims.

### `potential_conflict`

Existence claims usually should not produce `potential_conflict` in the first slice.

A possible future use might be a negative existence claim such as:

```text
ResponseEngine does not exist.
```

But negative existence claims are out of scope for the first implementation.

## Existence vs Ownership

This distinction must remain sharp.

```text
ToolExecutor exists.
```

can be supported by a class fact.

```text
ToolExecutor owns registered-operation execution.
```

cannot be fully supported by class existence alone.

Ownership may require:

- existence evidence;
- structural evidence;
- behavioral evidence;
- boundary evidence;
- tests or invariants;
- absence of competing owners under an explicit acquisition scope.

Existence reconciliation must not upgrade itself into ownership reconciliation.

## Existence vs Import

An import fact can show that code references a symbol or dependency.

It does not necessarily show that Seed defines that symbol locally.

For example:

```python
from seed_runtime.execution import ToolExecutor
```

supports a claim like:

```text
This module imports ToolExecutor.
```

more directly than:

```text
ToolExecutor exists.
```

The first implementation may choose to match imports conservatively, but it should avoid claiming local definition support from imports unless the rule states that imported symbols count as artifact existence within the supplied artifact facts.

## Extraction Boundary

Documentation Observation may need to extract explicit existence claims as `claim_family="existence"`.

It should extract only clear, explicit forms such as:

```text
ToolExecutor exists.
Runtime defines handle_user_message.
```

It should not extract vague prose such as:

```text
Seed has many runtime components.
The repository includes useful helpers.
Runtime is important.
```

Repository Observation already emits artifact facts such as:

```text
module
class
function
import
```

Existence reconciliation should consume those facts. It should not perform AST parsing, file IO, repository scanning, or source inspection itself.

## Recommended Initial Tests

The first implementation should be fixture-only.

Suggested tests:

1. `ToolExecutor exists.` plus class `ToolExecutor` produces `supported`.
2. `MagicExecutor exists.` plus class `ToolExecutor` produces `missing_support`.
3. `Runtime defines handle_user_message.` plus class `Runtime` and function `handle_user_message` from the same source path produces `supported`.
4. `Runtime defines handle_user_message.` plus class `Runtime` and function `handle_user_message` from different source paths produces `missing_support`.
5. `Runtime defines handle_user_message.` plus only class `Runtime` produces `missing_support`.
6. Vague existence-like prose is either not extracted or becomes `not_evaluable`, depending on extractor boundary.
7. Existing ownership claims still use ownership semantics and are not reclassified as existence claims.
8. No runtime, tool execution, event ledger, projection store, repository scanning, file reads, or LLM behavior is introduced.

## Non-Goals

This slice does not implement:

- ownership generalization;
- negative existence claims;
- repository-wide absence proofs;
- behavior inference;
- route authority inference;
- confidence scoring;
- graph construction;
- runtime integration;
- repository scanning;
- file reads;
- LLM extraction.

## Future Work

After explicit existence claims are stable, future reconciliation may consider:

- negative existence claims;
- local definition vs imported reference distinctions;
- module-qualified claims;
- same-source containment semantics for `X defines Y`;
- existence support across multiple supplied artifact scopes;
- stronger ownership support profiles.

Those should be added deliberately and documented before implementation.

## Documentation-Only Status

This document defines intended existence-claim reconciliation semantics only. It does not modify production code, tests, reconciliation behavior, acquisition behavior, runtime behavior, tool execution, event storage, projection behavior, package exports, or local CLI behavior.
