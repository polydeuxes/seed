# Operator Authority / Scope Binding Slice 001

## 1. Recovered responsibility
Seed now owns one read-only ingress binding responsibility: given one interpreted operator expression, bind the interpreted request to established operator identity, authority class, session/workspace authority, and exact scope.

## 2. Producer
`bind_operator_authority_scope(...)` produces `OperatorAuthorityScopeBindingProjection`.

## 3. Input artifacts
Inputs are one `OperatorExpressionInterpretationProjection`, its matching `FutureOperatorAuthorityScopeBindingHandoff`, the matching `AttributedOperatorExpression`, `OperatorIdentityContext`, `WorkspaceSessionAuthorityContext`, and `ScopeBindingContext`.

## 4. Output artifact
`OperatorAuthorityScopeBindingProjection` preserves interpretation and expression references, operator identity reference, workspace/session references, activity class, requested/resolved/permitted/excluded/unresolved scope, authority-bearing expressions, authority source references, required authority, constraints, state, reason, Unknowns, conflicts, and read-only flags.

## 5. Future bounded-question handoff
No future bounded-question handoff is emitted. A permitted binding stops at authority/scope preservation and does not contain a bounded question, constitutional intent conclusion, selection key, diagnostic/view identity, realization, authorization, pending action, or execution material.

## 6. Binding-state model
The state model is `permitted`, `blocked`, `unknown`, and `conflict`.

## 7. Interpretation-handoff validation
The producer deterministically rejects mismatched interpretation, attributed expression, operator, workspace, and required session contexts.

## 8. Operator identity treatment
Actor attribution is separate from verified identity. `operator_ref` must match the interpretation handoff and expression. Authority must be supplied by the bounded identity context; attribution alone does not grant authority.

## 9. Workspace/session treatment
Workspace references must match the expression, handoff, workspace/session authority context, and scope-binding context. Session references must match when the session authority context requires them.

## 10. Activity-class treatment
The producer maps the existing interpreted movement class or interpreted inquiry kind to the smallest supported activity class and does not reinterpret raw prose.

## 11. Requested-scope treatment
Requested scope expressions are copied from the interpretation projection and retained separately from resolved and permitted scope.

## 12. Scope resolution
Scope resolution is supplied by `ScopeBindingContext`; the producer does not invent entity resolution.

## 13. Permitted-scope treatment
Permitted scope is the resolved scope that is also in the workspace/session authority boundary.

## 14. Excluded-scope treatment
Resolved scope outside permitted authority, or inside prohibited scope, is preserved as excluded scope.

## 15. Unresolved-scope treatment
Unresolved requested scope prevents a permitted binding and is preserved as Unknown binding material.

## 16. Partial-scope treatment
Partial scope is preserved by retaining permitted and excluded scope separately. The projection does not silently narrow the original request.

## 17. Authority-bearing-language treatment
Authority-bearing expressions are preserved as operator-stated material, not automatic authority grants.

## 18. Standing-authority treatment
Standing authority is accepted only when supplied through bounded identity/session authority classes and authority-source references.

## 19. Explicit-grant treatment
An explicit bounded operator grant may contribute only when the operator identity context lists the exact grantable authority class and authority-bearing language is present.

## 20. Ingress-versus-environmental-authority distinction
The binding only answers whether the operator may request the activity in scope. It does not prove root availability, dependency availability, mechanism availability, or reachability.

## 21. Ingress-versus-realization-authorization distinction
The binding does not authorize a concrete realization and does not project warrant, selection, realization-specific authorization, or execution.

## 22. Operator-stated-constraint treatment
Operator constraints are preserved as downstream requirements; they do not prove future implementation effects.

## 23. Constraint-conflict treatment
Known request/constraint contradictions produce `conflict` rather than clause-order resolution.

## 24. Permitted treatment
`permitted` means the interpreted request is constitutionally receivable as an operator request within the bound scope.

## 25. Blocked treatment
`blocked` is used when positive authority/scope evidence establishes the request cannot advance.

## 26. Unknown treatment
`unknown` is used when permission or bounded denial cannot be established.

## 27. Conflict treatment
`conflict` is used when preserved authority, scope, or constraint material is incompatible.

## 28. Deterministic identity
Projection identity is stable over interpretation, expression, operator identity, workspace/session context, activity, scope sets, authority material, constraints, provenance, Unknowns, conflicts, state, reason, and convention. Input ordering is normalized.

## 29. Read-only inquiry result
A storage ownership inquiry over node115 is permitted when standing constitutional-read authority over node115 is supplied.

## 30. Existing-State explanation result
Existing-State explanation inquiries remain constitutional-read activity and do not authorize observation.

## 31. Passive repository-observation result
Passive repository inspection is permitted when local passive observation authority over the repository scope is supplied, and no-modification constraints are preserved.

## 32. Active network-observation result
Active network observation is blocked when network-active authority is absent or explicitly not granted.

## 33. Unknown network-authority result
Unresolved network-active authority produces `unknown`, not permission.

## 34. Privileged-observation result
Privileged observation is non-permitted unless the exact privileged authority class and scope are established; ingress permission would still not prove root availability.

## 35. Presentation-only result
JSON presentation preference passes through unchanged and does not select a renderer.

## 36. Unresolved-scope result
Unresolved required scope cannot become permitted.

## 37. Scope-exceeds-authority result
Scope outside authority is blocked or preserved as excluded without silent narrowing.

## 38. Conflicting-scope result
Conflicting scope bindings produce `conflict`.

## 39. Authority-expression result
Authority-bearing language alone does not create authority. A recognized operator with grantable exact authority may contribute an explicit bounded grant.

## 40. Operator-identity mismatch result
Operator mismatch fails deterministically.

## 41. Session/workspace mismatch result
Workspace and required session mismatches fail deterministically.

## 42. Current REPL compatibility
No REPL routing was changed.

## 43. Structured CLI compatibility
No CLI flags or structured caller behavior were changed.

## 44. Caller-supplied inputs
Structured callers may continue to supply bounded-question fields directly; this slice does not make free-form interpretation mandatory.

## 45. Seed-owned authority/scope responsibility
Seed now owns the narrow interpretation-to-ingress-authority/scope projection.

## 46. Manual responsibility eliminated
Seed validates one exact interpretation handoff, binds identity/session/workspace, binds activity to authority, limits exact permitted scope, preserves exclusions and Unknowns, preserves constraints, and emits a future handoff only for permitted bindings.

## 47. Read-only guarantees
The producer and renderers are read-only, write no event ledger entries, mutate no cluster state, create no observations/evidence/facts, and execute nothing.

## 48. Boundary notes
Boundary notes preserve ingress-only authority, authority-language limits, scope limits, identity limits, constraint limits, no bounded question production, and no realization/execution authority.

## 49. Compatibility answer
No.

## 50. Files changed
- `seed_runtime/operator_authority_scope_binding.py`
- `seed_runtime/__init__.py`
- `tests/test_operator_authority_scope_binding.py`
- `operator_authority_scope_binding_slice_001.md`

## 51. LOC delta
Recorded by `git diff --stat` and `git diff --numstat` before commit.

## 52. Tests executed
Focused operator-authority/scope tests and compatibility tests were executed. Full suite was executed and baseline failures were recorded.

## 53. Full-suite baseline result
The full suite still has unrelated baseline failures; this slice did not repair those unrelated failures.

## 54. Remaining roads
- `OperatorAuthorityScopeBindingProjection -> BoundedConstitutionalQuestion`
- `BoundedConstitutionalQuestion -> inquiry decomposition -> capability projection -> constitutional view selection`
- `SelectedConstitutionalViews -> broader dynamic constitutional composition`
- `BoundedConstitutionalResult -> OperatorPresentationTranslation -> OperatorFacingEgress`

## 55. Exact next bounded question
Given one permitted `OperatorAuthorityScopeBindingProjection` for one exact interpreted operator expression, what smallest owner may formulate the explicit bounded question, constitutional intent, scope status, uncertainty, Unknowns, caller-supplied fields, and downstream inquiry handoff required by `BoundedConstitutionalQuestion` without decomposing the inquiry, selecting question families or views, retrieving evidence, authorizing movement, or executing anything?
