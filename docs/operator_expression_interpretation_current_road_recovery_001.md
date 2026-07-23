# Operator-expression interpretation current-road recovery 001

## Scope and method

This is a report-only current-road recovery for `seed_runtime/operator_expression_interpretation.py`. It does not edit production code, tests, fixtures, package exports, CLI behavior, APIs, events, projections, persistence, the Book, existing reports, or repository structure beyond this report.

Minimum required searches were run against `seed_runtime scripts tests book_of_seed docs`, followed by narrower searches for actual callers and immediately visible producers/consumers.

## Current implementation inventory

`seed_runtime/operator_expression_interpretation.py` owns these artifacts and helpers:

- `AttributedOperatorExpression`: preserves exact and normalized operator material, input/source channel, workspace/session/operator refs, provenance, received scope context, uncertainty, unknowns, and read-only/no-ledger/no-mutation flags.
- `attribute_operator_expression(...)`: normalizes whitespace, stable-hashes the attribution payload, and returns `AttributedOperatorExpression`.
- `SourceSpan`: records a component label, exact text, and start/end offsets.
- `CandidateInterpretation`: stores interpretation candidate fields: expression form, inquiry/request kind, relation/focus, subject/object/scope expressions, requested movement class, authority-bearing expressions, stated effect constraints, evidence/unknown/presentation preferences, temporal expressions, and source spans.
- `FutureOperatorAuthorityScopeBindingHandoff`: copies selected interpretation fields for a possible later authority/scope binding; it is created only when interpretation state is `interpreted`.
- `OperatorExpressionInterpretationProjection`: the returned projection, including input refs, mechanism/contract refs, interpretation state/reason, parsed fields, alternatives, unresolved references, unsupported residual spans, known loss, supporting/provenance/unknown/conflict material, and the optional future handoff.
- `_stable(...)`, `_refs(...)`, and `_spans(...)`: identity, tuple normalization, and lexical span helpers.
- `_parse(...)`: hard-coded lexical/expression parsing over normalized operator text and recovered grammar `supported_structures`.
- `interpret_operator_expression(...)`: validates that the selected recovered grammar belongs to the recovery projection; parses the attributed expression under that grammar; merges Unknown/conflict/known-loss/supporting/provenance material; optionally creates a future handoff; returns `OperatorExpressionInterpretationProjection`.
- `operator_expression_interpretation_json(...)` and `format_operator_expression_interpretation(...)`: JSON and formatter surfaces only.

### Hard-coded interpretation states and reasons

The file declares states `interpreted`, `ambiguous`, `unsupported`, `unknown`, and `conflict`. `_parse(...)` currently creates these reason strings:

- `bounded movement request interpreted without authority binding`
- `operator-stated constraint preserved without proving realization`
- `coordination or multi-clause structure is outside the recovered grammar boundary`
- `reference expression is unresolved`
- `referent required for blocker interpretation is unresolved`
- `multiple bounded interpretations remain possible`
- `one bounded interpretation is supported`
- `prediction request form is outside the recovered grammar boundary`
- `imperative/request form has unresolved target or action`
- `bounded positive evidence places expression outside recovered grammar`
- `grammar was not recovered`
- `conflicting interpretation material is preserved`

### Fields parsed or inferred from operator text

The parser directly infers or fills these fields from lexical matches in `expr.normalized_text`/`expr.exact_text`:

- `expression_form`
- `inquiry_or_request_kind`
- `relation_or_focus_expressions`
- `subject_expressions`
- `object_expressions` only by preservation as an empty tuple in current rules
- `scope_expressions`
- `requested_movement_class`
- `authority_bearing_expressions`
- `operator_stated_effect_constraints`
- `evidence_support_preference`
- `unknown_limitation_preference`
- `presentation_preference`
- `temporal_expressions`
- `alternative_interpretations`
- `unresolved_references`
- `unsupported_residual_spans`
- `source_span_bindings`

`interpretation_mechanism_ref`, `invocation_contract_ref`, `lexical_support_refs`, `domain_vocabulary_refs`, `supporting_references`, `provenance`, `unknowns`, and `conflicts` are caller-supplied, not discovered by the interpreter.

## Immediate producer recovery

### `AttributedOperatorExpression` producers

| file/function | invoked by current production code? | exact standing established | caller-supplied? | tests only demonstrated caller? |
|---|---:|---|---:|---:|
| `seed_runtime/operator_expression_interpretation.py::attribute_operator_expression(...)` | No current non-test caller found. | Preserves exact text, normalized whitespace text, source/input channel, workspace/session/operator refs, provenance, received scope context, uncertainty, unknowns, and read-only/no-ledger/no-mutation flags; does not establish meaning, authority, grammar applicability, or occurrence in a downstream road. | Yes: all substantive source/context fields are parameters except normalized text and stable id. | Yes. |
| Direct dataclass construction in tests | No. | Constructs artifact-shaped values without producer occurrence. | Yes. | Yes. |
| Package export in `seed_runtime/__init__.py` | No invocation. | Importability only. | N/A. | N/A. |

### `RepresentationGrammarRecoveryProjection` and `RecoveredRepresentationGrammar` producers

| file/function | invoked by current production code? | exact standing established | caller-supplied? | tests only demonstrated caller? |
|---|---:|---|---:|---:|
| `seed_runtime/representation_grammar_recovery.py::recover_representation_grammars(...)` | No current non-test caller immediately visible except package export/importability. | Produces a recovery projection and recovered grammar records from candidate grammar material, recovery material, comparisons, lexical support, unknowns, and conflicts. | Yes: all source/candidate/comparison/recovery/lexical material is caller-supplied. | Yes for the interpreter road. |
| Direct fixtures/tests selecting `rec.recovered_grammars[0]` | No. | Test-created grammar availability for tests only. | Yes. | Yes. |
| Package export in `seed_runtime/__init__.py` | No invocation. | Importability only. | N/A. | N/A. |

### `interpretation_mechanism_ref` and `invocation_contract_ref` sources

| source | invoked by current production code? | exact standing established | caller-supplied? | tests only demonstrated caller? |
|---|---:|---|---:|---:|
| `interpret_operator_expression(..., interpretation_mechanism_ref=...)` keyword | No current non-test call found. | A string copied into projection identity and field; no mechanism registry or proof is checked. | Yes. | Yes. |
| `interpret_operator_expression(..., invocation_contract_ref=...)` keyword | No current non-test call found. | A string copied into projection identity and field; no invocation contract registry or proof is checked. | Yes. | Yes. |
| Test constants such as `MECH` and `contract_id` | No. | Test-local labels only. | Yes. | Yes. |

## Immediate consumer recovery

### `OperatorExpressionInterpretationProjection` consumers

| file/function | exact fields consumed | standing assumed | other producer? | production-active? | test-only? | constructible-only? | unreachable? |
|---|---|---|---:|---:|---:|---:|---:|
| `seed_runtime/operator_expression_interpretation.py::operator_expression_interpretation_json(...)` | full `to_json_dict()` | Artifact has `to_json_dict`; no semantic standing strengthened. | Directly constructible projection. | No current non-test invocation found. | Yes. | Yes. | No, importable. |
| `seed_runtime/operator_expression_interpretation.py::format_operator_expression_interpretation(...)` | projection id, expression ref, state/reason, form/kind/focus/scope, authority language, constraints, presentation preference, operational flags, alternatives, unresolved, unsupported, provenance, unknowns, conflicts, boundary notes | Display only; formatter is not downstream constitutional consumer. | Directly constructible projection. | No current non-test invocation found. | Yes. | Yes. | No, importable. |
| `seed_runtime/operator_authority_scope_binding.py::bind_operator_authority_scope(...)` | projection id, attributed expression ref, inquiry kind, requested movement class, scope expressions, authority-bearing expressions, stated constraints, presentation preference, provenance, unknowns, conflicts | Assumes interpretation artifact fields are suitable ingress for authority/scope binding after handoff/expression/context consistency checks; it does not prove interpreter occurrence. | No independent non-interpreter projection producer found; tests can construct projection-shaped values. | No current non-test invocation found. | Yes. | Yes. | No, importable. |
| `seed_runtime/bounded_operator_goal_establishment.py::establish_bounded_operator_goal_from_interpretation(...)` | artifact type, projection id, attributed expression ref, interpretation state, relation/focus, subject/object/scope, unresolved lexical/references, unsupported spans, provenance, stated constraints, unknowns, alternatives, conflicts, known loss | Treats interpreted orientation as bounded goal-orientation evidence; does not require authority/scope binding. | Direct construction possible; no active non-test producer found. | No current non-test invocation found. | Yes. | Yes. | No, importable. |
| `seed_runtime/bounded_operator_goal_establishment.py::establish_bounded_operator_goal_from_authority_scope_binding(...)` | projection id, attributed expression ref, relation/focus, subject/object, state, unresolved references, lexical bindings, unsupported spans, conflicts, known loss, alternatives, full JSON snapshot | Requires matching binding and expression; consumes interpretation as part of permitted authority/scope material. | Only manual/direct construction or interpreter road found. | No current non-test invocation found. | Yes. | Yes. | No, importable. |
| Tests | many fields | Test expectations only. | Test construction/helpers. | No. | Yes. | No. | No. |
| Package exports | symbol only | Importability only. | N/A. | No invocation. | No. | Yes. | No. |

### `FutureOperatorAuthorityScopeBindingHandoff` consumers

| file/function | exact fields consumed | standing assumed | other producer? | production-active? | test-only? | constructible-only? | unreachable? |
|---|---|---|---:|---:|---:|---:|---:|
| `seed_runtime/operator_authority_scope_binding.py::bind_operator_authority_scope(...)` | interpretation id, attributed expression ref, operator ref, workspace ref, session ref | Uses the handoff only for identity/session/workspace consistency checks against interpretation, expression, operator identity, and workspace/session/scope contexts. The rest of the handoff fields are not consumed by the binder. | The interpreter is the only non-test implementation producer found; tests obtain it from interpreter helper. Direct dataclass construction remains possible. | No current non-test invocation found. | Yes. | Yes. | No, importable. |
| `OperatorExpressionInterpretationProjection.to_json_dict()` | full handoff JSON if present | Serialization only. | Interpreter/direct construction. | No current non-test invocation found. | Yes. | Yes. | No. |
| Tests | identity fields through binder and non-null assertions | Test road only. | Test helper through interpreter. | No. | Yes. | No. | No. |
| Package exports | symbol only | Importability only. | N/A. | No invocation. | No. | Yes. | No. |

## Authority/scope boundary answers

1. `FutureOperatorAuthorityScopeBindingHandoff` is the only implementation producer of the handoff shape found outside tests, but no current non-test invocation road constructs it.
2. No production entry point was found constructing the handoff.
3. Authority/scope artifacts are consumed by current functions and renderers, but no current production invocation road was found.
4. Deletion of the interpreter would leave `bind_operator_authority_scope(...)` without its only implementation handoff producer, while direct construction/importability would remain possible until separately deleted.
5. Yes. Tests manually create or route artifacts that production never produces in the current road: interpreter projections, handoffs, authority/scope bindings, bounded-goal inputs, and explanation/rendering inputs.

## Goal-establishment boundary

| function | current producers | current consumers | classification |
|---|---|---|---|
| `establish_bounded_operator_goal_from_interpretation(...)` | Accepts caller-supplied `OperatorExpressionInterpretationProjection`; tests manually construct it. No current non-test interpreter invocation found. | Tests and downstream need-projection tests. Package export. | production-constructible but not invoked |
| `establish_bounded_operator_goal_from_authority_scope_binding(...)` | Accepts caller-supplied `OperatorAuthorityScopeBindingProjection`, matching interpretation, and expression; tests manually construct or produce these through test helpers. No current non-test binder invocation found. | Tests. Package export. | production-constructible but not invoked |
| `establish_bounded_operator_goal_from_admitted_interpretation(...)` | Accepts `DownstreamInterpretationAdmission`, a separate downstream interpretation admission road. | Tests, Book mentions, package export. | independently active through another producer, but production invocation was not established in this recovery; classification for this interpreter road: production-constructible but not invoked |

Interpreter-dependent goal-establishment functions are `establish_bounded_operator_goal_from_interpretation(...)` and `establish_bounded_operator_goal_from_authority_scope_binding(...)`. The admitted-interpretation function does not depend on the operator-expression interpreter road.

## Shared-explanation boundary

`MinimumLawfulAdvancementExplanation` is produced by `seed_runtime/operator_authority_scope_binding.py::explain_minimum_lawful_advancement(...)` from `OperatorAuthorityScopeBindingProjection`. It is consumed by:

- `minimum_lawful_advancement_explanation_json(...)` and `format_minimum_lawful_advancement_explanation(...)` in the same module.
- `seed_runtime/shared_explanation_rendering_projection.py::project_shared_explanation_rendering(...)`, which registers acceptance by `isinstance(explanation, MinimumLawfulAdvancementExplanation)` and projects shared display fields.
- `shared_explanation_rendering_json(...)` and `format_shared_explanation_rendering(...)` for display.
- Tests.

No current production occurrence of the interpretation → authority/scope → explanation → shared-rendering road was found. Rendering registration and membership registration prove constructibility/importability, not production occurrence. Because the explanation producer consumes an authority/scope binding, and the only implementation handoff producer for that binding is the interpreter, the explanation artifacts are downstream compatibility structure for this road unless an independent authority/scope producer is later recovered.

## Representation-grammar recovery boundary

Operator-expression interpretation is a current implementation consumer of `RepresentationGrammarRecoveryProjection` and `RecoveredRepresentationGrammar` because `interpret_operator_expression(...)` validates and reads both. However, no current non-test invocation of that consumer was found.

Immediately visible other current non-test consumers from direct search are:

- `seed_runtime/representation_grammar_recovery.py` internal JSON/formatting/producer code.
- `seed_runtime/__init__.py` package exports/imports.

Tests are the demonstrated active callers. This report does not infer broader constitutional standing for representation-grammar recovery.

## Artifact matrix

| artifact or function | producer | input standing | produced standing | consumer | activity classification | foreign-grammar pressure | independent constitutional warrant | candidate later treatment | strongest Unknown |
|---|---|---|---|---|---|---|---|---|---|
| `AttributedOperatorExpression` | `attribute_operator_expression(...)`; direct construction | Caller-supplied exact text/context | Attributed text preservation, not meaning | interpreter, binder, goal from binding, tests | production-constructible but not invoked | Yes: external operator text | Not established here | delete with interpreter if no independent review preserves it | Whether any undiscovered production plugin imports it dynamically |
| `SourceSpan` | `_spans(...)`; direct construction | Lexical substring matches | Component offsets/testimony | candidate/projection/handoff/format/JSON | production-constructible but not invoked | Yes | No independent warrant found | delete with interpreter unless another owner needs it | Dynamic consumers not found by search |
| `CandidateInterpretation` | `_parse(...)`; direct construction | Hard-coded lexical parses | Candidate testimony | projection alternatives/fields/tests | production-constructible but not invoked | Yes | No independent warrant found | delete with interpreter | Whether alternative interpretation has external users |
| `OperatorExpressionInterpretationProjection` | `interpret_operator_expression(...)`; direct construction | Attributed expression + recovered grammar + caller refs | Interpretation testimony with boundaries | binder, goal establishment, format/JSON, tests | production-constructible but not invoked | Yes | No active non-test warrant found | delete with interpreter if no independent road recovered | Dynamic/API consumers outside search |
| `FutureOperatorAuthorityScopeBindingHandoff` | `interpret_operator_expression(...)`; direct construction | Interpreted candidate + identity refs | Future handoff-shaped testimony, not occurrence | binder identity checks, JSON/tests | production-constructible but not invoked | Yes | No active non-test warrant found | delete with interpreter/binder district | Whether future field is consumed externally |
| `interpret_operator_expression(...)` | module function | Caller supplies expression, recovery projection, grammar, mechanism, contract | Parses and packages testimony; maybe future handoff | tests; constructible import | production-constructible but not invoked | High | No active non-test warrant found | delete | Dynamic production invocation not found |
| `operator_expression_interpretation_json(...)` | module function | Projection object | Dict serialization | tests/constructible callers | production-constructible but not invoked | Low | Formatter/serialization only | delete with projection unless external API preserves it | External API stability expectations |
| `format_operator_expression_interpretation(...)` | module function | Projection object | Presentation text | tests/constructible callers | production-constructible but not invoked | Low | Formatter only | delete with projection unless external API preserves it | CLI dynamic use not found |
| `bind_operator_authority_scope(...)` | authority/scope module | Interpretation + future handoff + contexts | Authority/scope binding projection | goal from binding, explanation, format/JSON/tests | production-constructible but not invoked | Medium | Not established independently | preserve for independent review or delete with road if no independent producer | Whether non-interpreter producers exist outside visible search |
| `MinimumLawfulAdvancementExplanation` | `explain_minimum_lawful_advancement(...)` | Authority/scope binding | Stage-owned explanation | shared rendering/format/JSON/tests | production-constructible but not invoked | Low | Depends on binding road in this recovery | preserve for independent review with authority/scope district | Whether other binding producers exist |

## Road matrix

| producer | handoff or artifact | consumer | non-test occurrence evidence | test-only evidence | standing preserved | standing strengthened by consumer | classification |
|---|---|---|---|---|---|---|---|
| `attribute_operator_expression(...)` | `AttributedOperatorExpression` | `interpret_operator_expression(...)` | None found | `tests/test_operator_expression_interpretation.py`, `tests/test_operator_authority_scope_binding.py` | Exact/normalized text and context | No; parser adds testimony only | test-only |
| `recover_representation_grammars(...)` | `RepresentationGrammarRecoveryProjection` / `RecoveredRepresentationGrammar` | `interpret_operator_expression(...)` | None found | interpreter tests | Recovered grammar records | Interpreter treats selected grammar as parsing boundary | test-only |
| caller keyword | `interpretation_mechanism_ref` | `interpret_operator_expression(...)` | None found | test constants | String label | No validation | test-only |
| caller keyword | `invocation_contract_ref` | `interpret_operator_expression(...)` | None found | test constants | String label | No validation | test-only |
| `interpret_operator_expression(...)` | `OperatorExpressionInterpretationProjection` | `bind_operator_authority_scope(...)` | None found | authority/scope tests | Interpretation testimony | Binder relies on movement/scope/authority-shaped fields for permission decision | test-only |
| `interpret_operator_expression(...)` | `FutureOperatorAuthorityScopeBindingHandoff` | `bind_operator_authority_scope(...)` | None found | authority/scope tests | Future handoff-shaped identity/context | Binder checks identity consistency only | test-only |
| `bind_operator_authority_scope(...)` | `OperatorAuthorityScopeBindingProjection` | `establish_bounded_operator_goal_from_authority_scope_binding(...)` | None found | bounded goal tests manually construct binding | Permission/refusal testimony | Goal establishment relies on permitted binding to orient goal | test-only |
| `bind_operator_authority_scope(...)` | `OperatorAuthorityScopeBindingProjection` | `explain_minimum_lawful_advancement(...)` | None found | authority/scope and rendering tests | Binding state/reason/unknown/conflict | Explanation derives first missing boundary | test-only |
| `explain_minimum_lawful_advancement(...)` | `MinimumLawfulAdvancementExplanation` | `project_shared_explanation_rendering(...)` | None found | shared rendering tests | Stage-owned explanation fields | Shared rendering only displays stage-owned material | test-only |
| Direct projection construction | `OperatorExpressionInterpretationProjection` | `establish_bounded_operator_goal_from_interpretation(...)` | None found | multiple need/goal tests | Artifact-shaped interpretation | Goal function treats it as orientation evidence | test-only |

## Candidate deletion matrix

| implementation file or symbol | depends exclusively on interpreter road | has independent producer | has independent consumer | mechanical deletion dependency | later treatment |
|---|---:|---:|---:|---|---|
| `seed_runtime/operator_expression_interpretation.py` | Yes | No active non-test producer found | No active non-test consumer found | Exports/tests/binder/goal imports | delete with interpreter |
| `AttributedOperatorExpression` | Yes in current road | No active non-test producer found | Binder/goal consume but no active road | Binder and goal signatures/imports | delete with interpreter |
| `SourceSpan` | Yes | No | No active independent consumer | Candidate/projection/handoff fields | delete with interpreter |
| `CandidateInterpretation` | Yes | No | No active independent consumer | Projection alternatives/tests | delete with interpreter |
| `OperatorExpressionInterpretationProjection` | Yes | Direct construction only | Binder/goal/format/tests constructible | Binder and goal signatures/imports | delete with interpreter |
| `FutureOperatorAuthorityScopeBindingHandoff` | Yes | No active independent producer | Binder constructible consumer | Binder signature/import/tests | delete with interpreter |
| `attribute_operator_expression(...)` | Yes | N/A | Tests/interpreter road only | Tests/exports | delete with interpreter |
| `interpret_operator_expression(...)` | Yes | N/A | Tests only | Tests/exports | delete with interpreter |
| `operator_expression_interpretation_json(...)` | Yes | N/A | Formatter/API constructible only | Exports/tests if any | delete with interpreter |
| `format_operator_expression_interpretation(...)` | Yes | N/A | Formatter/API constructible only | Exports/tests if any | delete with interpreter |
| `seed_runtime/operator_authority_scope_binding.py::bind_operator_authority_scope(...)` | Depends on interpreter projection + handoff | No independent handoff producer found | Goal/explanation constructible | Imports interpreter classes | preserve for independent review |
| `OperatorAuthorityScopeBindingProjection` | Road depends on interpreter, but class could be direct-constructed | Direct construction only | Goal/explanation/tests | Goal/explanation signatures | preserve for independent review |
| `MinimumLawfulAdvancementExplanation` and producer/renderers | Depends on authority/scope binding road | Binding direct construction only | Shared rendering/tests | Rendering import/type check | preserve for independent review |
| `establish_bounded_operator_goal_from_interpretation(...)` | Yes for live meaning | Direct projection construction only | Tests/exports | Import of projection class | delete with interpreter or preserve only if independent interpretation producer is recovered: Unknown |
| `establish_bounded_operator_goal_from_authority_scope_binding(...)` | Indirectly, through binding road | Binding direct construction only | Tests/exports | Imports binding/projection classes | preserve for independent review |
| `establish_bounded_operator_goal_from_admitted_interpretation(...)` | No | `DownstreamInterpretationAdmission` road | Tests/Book mentions | Separate imports/types | preserve for independent review |

## Fidelity examination

| possible crossing | producer actually establishes | consumer relies upon | classification |
|---|---|---|---|
| operator text → operator meaning | Attribute function preserves text and normalized text only; parser produces bounded testimony. | Goal-from-interpretation treats interpreted fields as bounded orientation evidence. | not reached in production |
| recovered grammar → applicable grammar | Grammar recovery artifact is supplied by caller; interpreter checks grammar belongs to projection and candidate was recovered. | Parser uses `supported_structures` as applicable parsing boundary. | not reached in production |
| lexical match → constitutional subject | `_parse(...)` extracts focus/scope/subject expressions by regex/string matching. | Goal functions use those expressions as orientation/scope material. | not reached in production |
| imperative form → requested movement | `_parse(...)` labels active scan/inspection/prediction/run forms. | Binder maps requested movement to activity class and authority class. | not reached in production |
| authority-shaped words → authority relevance | `_parse(...)` copies phrases such as `Run an active scan` or `Inspect` as authority-bearing expressions. | Binder uses non-empty authority-bearing expressions when deciding source refs/additional authority. | not reached in production |
| effect language → effect constraint | `_parse(...)` preserves clauses like `do not modify anything`. | Binder treats constraints as conflict inputs; goal preserves them. | not reached in production |
| interpretation result → authorized downstream handoff | Interpreter creates a future handoff only for `interpreted`; boundary notes say it does not establish authority or authorize. | Binder requires handoff identity consistency before binding. | not reached in production |
| constructed handoff → handoff occurrence | Construction creates an object field; no event/record/provenance of handoff occurrence is established. | Binder only sees object fields. | not reached in production |

No live production crossing was recovered. In constructible/test roads, the strongest fidelity pressure is that consumers can rely on stronger standing than the interpreter produces: e.g., binder and goal-establishment can consume lexical interpretation testimony as if it were sufficient ingress evidence when manually constructed. That is not proven production contamination because no production invocation was found.

## Documentation and historical-only matches

Book matches and prior reports are historical/documentation references, not current roads. They include `book_of_seed/attributed_operator_expression_active_road_fidelity_recovery_001.md`, `book_of_seed/constitutional_occurrence_evidence_survey_007.md`, `book_of_seed/constitutional_evidence_uptake_runtime_frontier_investigation_001.md`, and scattered Book lens/constructor mentions. This operation did not edit or hash historical reports.

## Smallest coherent later deletion district

The smallest coherent implementation district visible for later deletion, without inventing replacement architecture, is:

- `seed_runtime/operator_expression_interpretation.py` in full:
  - `AttributedOperatorExpression`
  - `attribute_operator_expression(...)`
  - `SourceSpan`
  - `CandidateInterpretation`
  - `OperatorExpressionInterpretationProjection`
  - `FutureOperatorAuthorityScopeBindingHandoff`
  - `interpret_operator_expression(...)`
  - `operator_expression_interpretation_json(...)`
  - `format_operator_expression_interpretation(...)`
  - helpers/constants/parser states/reasons.
- Package exports/imports for those exact symbols.
- Tests that only prove construction or behavior of that road.
- Downstream signatures/imports that exclusively require the interpreter projection/handoff would need separate deletion review, especially authority/scope binding and goal-from-interpretation.

What must remain outside that deletion district unless independently reviewed:

- `seed_runtime/representation_grammar_recovery.py`, because it has its own producer and tests; this report only recovers that the interpreter is not its only immediately visible constructible consumer.
- `establish_bounded_operator_goal_from_admitted_interpretation(...)` and the downstream interpretation admission road.
- General bounded goal establishment artifacts not exclusively tied to operator-expression interpretation.
- Shared explanation rendering infrastructure unless the authority/scope explanation district is separately deleted.
- Book files and existing reports.

No replacement interpreter, adapter, ingress envelope, movement classifier, authority-expression artifact, source-span model, or grammar application boundary is warranted by this recovery.

## Required direct answers

1. **What current non-test producer invokes `interpret_operator_expression(...)`?** None found.
2. **What current non-test producer constructs `AttributedOperatorExpression` for that road?** None found; only `attribute_operator_expression(...)` exists as constructible implementation producer, and tests demonstrate it.
3. **What current non-test producer supplies recovered grammar?** None found for this road; `recover_representation_grammars(...)` is the constructible producer and tests demonstrate it.
4. **Who supplies `interpretation_mechanism_ref`?** The caller of `interpret_operator_expression(...)`; in demonstrated calls, tests supply string constants.
5. **Who supplies `invocation_contract_ref`?** The caller of `interpret_operator_expression(...)`; in demonstrated calls, tests supply string constants.
6. **Is the interpreter production-active, constructible-only, test-only, or Unknown?** `test-only` for demonstrated occurrence; `production-constructible but not invoked` for importable implementation. Under the required exact classification for recovered roads: `test-only`.
7. **What exact act does the interpreter perform?** It validates grammar membership, applies hard-coded lexical parsing to normalized operator text under supported-structure labels, merges caller/recovery/expression unknowns and conflicts, creates a stable projection id, and returns interpretation testimony plus an optional future authority/scope handoff.
8. **Which fields are parsed or inferred from operator text?** `expression_form`, `inquiry_or_request_kind`, relation/focus, subject, scope, requested movement class, authority-bearing expressions, stated effect constraints, evidence/unknown/presentation preferences, temporal expressions, alternatives, unresolved references, unsupported spans, and source spans. Current rules do not populate object expressions except as the empty default.
9. **Does it establish meaning or only produce interpretation testimony?** Only interpretation testimony bounded by its notes; it does not establish authority, resolved Seed entities, a bounded constitutional question, execution, scheduling, events, or cluster mutation.
10. **Does any consumer rely on stronger standing than the interpreter produces?** In constructible/test roads, yes: binder and goal functions can treat interpreted lexical fields as ingress for authority/scope or goal orientation. No production occurrence was found.
11. **Is `FutureOperatorAuthorityScopeBindingHandoff` produced in a current production road?** No current production road found.
12. **Is that handoff consumed in a current production road?** No current production road found.
13. **Does handoff construction establish handoff occurrence?** No. It creates a field/object; it does not record occurrence.
14. **Does `operator_authority_scope_binding.py` have any independent producer?** No independent handoff producer was found. The binding projection itself can be directly constructed in tests, but that is not an implementation producer occurrence.
15. **Which authority/scope artifacts would become producerless if the interpreter were deleted?** `FutureOperatorAuthorityScopeBindingHandoff` would lose its only implementation producer. `bind_operator_authority_scope(...)` would lose the only found implementation handoff/projection ingress road. `OperatorAuthorityScopeBindingProjection` would have no found production road, though direct construction would remain until deleted.
16. **Which goal-establishment functions depend exclusively on this road?** `establish_bounded_operator_goal_from_interpretation(...)` depends directly on `OperatorExpressionInterpretationProjection`. `establish_bounded_operator_goal_from_authority_scope_binding(...)` depends indirectly through `OperatorAuthorityScopeBindingProjection` and matching interpreter artifacts.
17. **Which goal-establishment functions have independent producers?** `establish_bounded_operator_goal_from_admitted_interpretation(...)` has the separate `DownstreamInterpretationAdmission` input road. Broader production activity was not established here.
18. **Which shared-explanation artifacts depend exclusively on this road?** `MinimumLawfulAdvancementExplanation` and `SharedExplanationRenderingProjection` for that explanation depend on `OperatorAuthorityScopeBindingProjection`; with no independent binding producer found, they are downstream of this road in current evidence, but should be preserved for independent authority/scope review before deletion.
19. **Does the interpreter provide the only current consumer of representation-grammar recovery?** No. Representation-grammar recovery has its own format/JSON/export/tests; the interpreter is the only immediately visible non-test implementation consumer outside that module, but it is not production-invoked.
20. **Which tests manually create roads that production does not?** `tests/test_operator_expression_interpretation.py`, `tests/test_operator_authority_scope_binding.py`, `tests/test_bounded_operator_goal_establishment.py`, `tests/test_bounded_advancement_horizon.py`, `tests/test_authority_need_projection.py`, `tests/test_clarification_need_projection.py`, `tests/test_operational_realization_need_projection.py`, `tests/test_inquiry_need_projection.py`, and `tests/test_shared_explanation_rendering_projection.py` manually construct or route interpretation/authority/goal/explanation artifacts without a current production producer road.
21. **Which documentation or Book matches are historical rather than current?** Prior Book reports and lenses matching these names are historical/documentation-only: especially `book_of_seed/attributed_operator_expression_active_road_fidelity_recovery_001.md`, `book_of_seed/constitutional_occurrence_evidence_survey_007.md`, `book_of_seed/constitutional_evidence_uptake_runtime_frontier_investigation_001.md`, and Book lens/constructor references.
22. **What is the smallest coherent later deletion district?** The whole `seed_runtime/operator_expression_interpretation.py` file, its package exports, and tests exclusively proving that road; then separately review authority/scope binding, goal-from-interpretation, and explanation compatibility structures.
23. **What must remain outside that deletion district?** Representation-grammar recovery, admitted-interpretation goal establishment, unrelated bounded-goal establishment machinery, shared rendering infrastructure unless separately reviewed, Book files, and existing reports.
24. **Is any replacement architecture warranted?** No.
25. **Where must this report stop?** At current-road recovery and candidate deletion district identification. It must not delete, rename, archive, adapt, redesign, restore historical versions, hash historical reports, or create replacement architecture.
