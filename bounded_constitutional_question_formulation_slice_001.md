# Bounded Constitutional Question Formulation Slice 001

## 1. Recovered responsibility

This slice recovers exactly one missing responsibility: given one permitted `OperatorAuthorityScopeBindingProjection` for one exact interpreted operator expression, Seed formulates one existing canonical `BoundedConstitutionalQuestion` for the constitutional inquiry pipeline.

The recovered road is:

```text
AttributedOperatorExpression
→ OperatorExpressionInterpretationProjection
→ OperatorAuthorityScopeBindingProjection
→ BoundedConstitutionalQuestion
```

This completes the artifact-level free-form ingress road. It does not yet connect the public REPL to that road.

```text
ingress road implemented
!= REPL routing changed
```

## 2. Existing canonical bounded-question owner

The existing canonical owner remains `BoundedConstitutionalQuestion` in `seed_runtime/bounded_constitutional_question.py`, produced by `produce_bounded_constitutional_question(...)`. The new formulation path delegates final artifact construction to that producer and does not create a competing constitutional-inquiry artifact.

## 3. Producer or adapter

Added `formulate_bounded_constitutional_question(...)` as a narrow additive adapter. It validates the ingress artifacts, deterministically formulates bounded-question fields, then invokes `produce_bounded_constitutional_question(...)`.

## 4. Input artifacts

The producer consumes only the smallest immutable upstream artifacts required for formulation:

- one `AttributedOperatorExpression`;
- one `OperatorExpressionInterpretationProjection`;
- one `OperatorAuthorityScopeBindingProjection`;
- the matching `FutureBoundedConstitutionalQuestionHandoff`;
- the handoff grammar/applicability references only as provenance;
- formulation convention identity;
- upstream provenance, known loss, Unknowns, conflicts, constraints, presentation preference, and scope status.

It does not consume raw operator prose as the sole semantic input, reinterpret the expression, reopen grammar recovery, reopen applicability, or rebind authority/scope.

## 5. Output artifact

The output is the existing `BoundedConstitutionalQuestion`.

## 6. Optional downstream context handoff

No optional downstream handoff was warranted. Presentation preference, constraints, excluded scope, and provenance fit in existing bounded-question fields without creating another inquiry artifact.

## 7. Deterministic validation

Validation fails deterministically via `BoundedConstitutionalQuestionFormulationError` when:

- binding state is not `permitted`;
- future handoff is absent or does not belong to the binding projection;
- binding, interpretation, expression, operator, workspace, session, kind, activity, requested scope, permitted scope, excluded scope, constraints, presentation preference, or provenance references mismatch.

Mismatches are not repaired.

## 8. Exact operator-inquiry treatment

`operator_inquiry` is the exact `AttributedOperatorExpression.exact_text`. It remains distinct from the Seed-derived bounded question.

## 9. Direct-versus-derived provenance

Direct operator-supplied material is limited to exact expression text, requested scope expression text, operator-stated effect constraints, presentation preference, and excluded original scope text when preserved upstream. Seed-derived bounded question, constitutional intent, and bound scope are not labeled as direct operator testimony.

## 10. Bounded-question formulation convention

The explicit convention is `bounded_constitutional_question_formulation_v1`. It maps interpreted request kind and activity class into stable question forms for identify, explain, support, unknowns, limitations, passive observation, active network observation, privileged observation, and external movement.

## 11. Constitutional-intent treatment

Constitutional intent is Seed-derived from interpreted request kind and activity class. Constitutional-read inquiries examine current constitutional State, support, limitations, or Unknowns. Movement requests ask for lawful constitutional movement without authorization or execution.

## 12. Scope-status treatment

`scope_status` preserves permitted, requested, excluded, and unresolved scope references in one deterministic string.

## 13. Permitted-scope treatment

The formulated question is bounded to `permitted_scope_refs` only.

## 14. Excluded-scope treatment

Excluded scope is preserved in `scope_status`, uncertainty, and caller-supplied context when present. It is not silently dropped.

## 15. Partial-scope treatment

Partial scope formulates only over permitted scope while preserving excluded original scope. The original request is not rewritten as fully permitted.

## 16. Uncertainty treatment

Uncertainty preserves expression uncertainty, unresolved lexical bindings, unresolved references, known loss, unresolved scope, excluded scope, conflicts, handoff known loss, and formulation-specific Unknowns.

## 17. Unknown treatment

Unknowns preserve upstream expression, interpretation, authority/scope binding, and handoff Unknowns.

## 18. Known-loss treatment

Known loss is carried into uncertainty from interpretation and handoff material.

## 19. Caller-supplied-field treatment

Caller-supplied fields contain only direct operator or operator-stated material: exact expression, requested scope expression text, constraints, presentation preference, and excluded original scope context.

## 20. Operator-stated-constraint treatment

Constraints such as no modification are preserved as downstream requirements. They are not proof that any realization is read-only.

## 21. Presentation-preference treatment

Presentation preference remains separate from inquiry meaning. JSON preference does not alter bounded question text, constitutional intent, or renderer selection.

## 22. Information-inquiry formulation

Information inquiries formulate identify-oriented bounded constitutional questions, e.g. identifying ownership relation or state within bound scope.

## 23. Explanation formulation

Explanation inquiries formulate questions about current constitutional limitations, support boundaries, and Unknowns. No limitation, authority, or ownership views are selected.

## 24. Support formulation

Support inquiries formulate questions identifying bounded support and provenance. They do not retrieve or rank evidence.

## 25. Unknowns formulation

Unknowns inquiries formulate questions identifying unresolved constitutional material. They do not calculate Unknowns during formulation.

## 26. Limitation formulation

Limitation inquiries preserve unresolved focus or referent uncertainty instead of inventing a target.

## 27. Passive-observation-request formulation

Passive observation requests formulate next-lawful-movement questions for the bound scope under operator-stated constraints. They do not select filesystem, git, grep, traversal, or another mechanism.

## 28. Active-network-request formulation

Active-network requests formulate a constitutional-road question for the permitted network-active request. They do not select scanners, authorize packets, project reachability, or execute.

## 29. Privileged-request formulation

Privileged requests formulate next-lawful-movement questions for privileged inspection. They do not establish root availability, sudo availability, or privileged reachability.

## 30. No-selection-key rule

The formulator emits no `selection_key`, `question_family`, diagnostic name, view name, capability name, surface args, or dispatch surface.

## 31. Immediate-consumer compatibility

The resulting `BoundedConstitutionalQuestion` remains consumable by `project_constitutional_question(...)`. Question projection behavior is unchanged.

## 32. Structured CLI compatibility

The existing structured `produce_bounded_constitutional_question(...)` path is unchanged. Structured CLI fields remain compatible.

## 33. Current REPL compatibility

`Runtime.handle_user_message`, `LocalSeedApp.run`, and `run_shell` are unchanged. Free-text REPL routing remains unsupported for this slice.

## 34. Caller-supplied inputs

Caller-supplied inputs are preserved only when upstream artifacts identify them as operator expression, requested scope expression, operator-stated constraint, or presentation preference.

## 35. Seed-owned formulation responsibility

Seed now owns deterministic bounded-question formulation from already-projected semantic material after authority/scope permission.

## 36. Manual responsibility eliminated

Before:

```text
operator or campaign author:
- interprets the expression;
- binds authority and scope;
- manually rewrites the permitted request
  into operator_inquiry, bounded_question,
  constitutional_intent, scope_status,
  uncertainty, Unknowns, and caller fields;
- risks mislabeling Seed-derived material
  as direct operator testimony;
- risks silently narrowing scope;
- risks embedding question-family or view selection
  inside the bounded question.
```

After:

```text
Seed:
- validates one permitted authority/scope handoff;
- preserves the exact attributed operator inquiry;
- formulates one deterministic Seed-native
  bounded constitutional question;
- preserves direct-versus-derived provenance;
- preserves permitted, excluded, and unresolved scope;
- preserves constraints, uncertainty,
  known loss, and Unknowns;
- produces the existing canonical
  BoundedConstitutionalQuestion;
- performs no decomposition, selection,
  evidence retrieval, authorization, or execution.
```

## 37. Read-only guarantees

Formulation and rendering preserve:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

They append no ledger entries, mutate no State or cluster, produce no observations/evidence/facts, authorize no movement, and execute nothing.

## 38. Boundary notes

- This artifact is the canonical constitutional inquiry formulated from one permitted operator request.
- The exact operator expression remains distinct from the Seed-derived bounded question.
- Ingress permission allows the request to be formulated; it does not establish capability reachability or authorize a realization.
- Bound scope is preserved without silently broadening or narrowing the original requested scope.
- Operator-stated constraints remain downstream requirements; they are not proof that a realization satisfies them.
- Presentation preference remains distinct from constitutional inquiry meaning.
- This artifact does not select question families, diagnostics, views, capabilities, or realizations.
- This artifact does not retrieve evidence, authorize movement, observe, emit, or execute.
- No tool, provider, model-decision, or registered-operation concept is required.

## 39. Compatibility answer

Did this slice change any existing compatibility boundary?

No.

## 40. Files changed

- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/__init__.py`
- `tests/test_bounded_constitutional_question_formulation.py`
- `bounded_constitutional_question_formulation_slice_001.md`

## 41. LOC delta

Recorded with `git diff --numstat` before commit.

## 42. Tests executed

Focused and compatibility commands executed:

```bash
pytest -q tests/test_bounded_constitutional_question_formulation.py
pytest -q tests/test_bounded_constitutional_question_formulation.py tests/test_bounded_constitutional_question.py tests/test_constitutional_pipeline.py tests/test_operator_expression_interpretation.py tests/test_operator_authority_scope_binding.py
pytest -q tests/test_constitutional_view_selection.py tests/test_constitutional_capability_projection.py tests/test_representation_grammar_recovery.py tests/test_representation_grammar_applicability.py tests/test_runtime_loop.py tests/test_cli_trace.py tests/test_seed_local_script.py tests/test_registry.py tests/test_policy.py tests/test_pending_actions.py tests/test_execution.py tests/test_execution_proposals.py tests/test_events.py tests/test_event_batching.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_public_exports.py
pytest -q
```

## 43. Full-suite baseline result

Full suite result: `57 failed, 2061 passed in 345.54s`. The failures are unrelated baseline failures concentrated in runtime decision routing, generated architecture stability, observation inventory and utilization, consumer dependency audit, Seed-local CLI, State patches, tool intent, tool recommendations, tool validation, and related API/evaluation paths. These were not repaired.

## 44. Completed ingress road

This slice completes the artifact-level free-form ingress road:

```text
AttributedOperatorExpression
→ OperatorExpressionInterpretationProjection
→ OperatorAuthorityScopeBindingProjection
→ BoundedConstitutionalQuestion
```

It does not yet connect the public REPL to that road.

## 45. Deferred inquiry/view road

The following remains deferred and unresolved:

```text
BoundedConstitutionalQuestion
→ semantic inquiry decomposition
→ capability projection
→ constitutional view selection
→ broader dynamic constitutional composition
```

The current exact-key question projection remains unchanged.

## 46. Next access-topology audit question

> Across repository, filesystem, service, network, internet, privileged-local, and peer-Seed boundaries, what is the constitutional unit of access: a target, a permission, a mechanism, a path, or one exact subject–activity–target–scope relationship under current authority and State; and which existing artifacts currently compress access observation, access authority, environmental reachability, credentials, effect constraints, and realization-specific authorization?

This audit must determine whether the next missing owners are equivalent to:

```text
CandidateAccessPathSet
→ AccessReachabilityProjection
```

without presuming those names or implementing an access registry.
