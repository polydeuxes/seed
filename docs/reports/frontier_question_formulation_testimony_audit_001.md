# Frontier Question Formulation Testimony Audit 001

## Scope

This audit determines the lawful bridge:

```text
BoundedInquiryFrontier
+
stage-owned question-formulation testimony
→ BoundedConstitutionalQuestion
```

It does not create another question artifact. It does not formulate a live runtime question instance, select evidence, open inquiry, authorize observation, execute, record, write the event ledger, or mutate state.

## Repository evidence reviewed

- `seed_runtime/bounded_inquiry_frontier.py`
- `seed_runtime/inquiry_frontier_boundary_testimony.py`
- `seed_runtime/bounded_constitutional_question.py`
- `tests/test_bounded_inquiry_frontier.py`
- `tests/test_bounded_constitutional_question.py`
- `tests/test_bounded_constitutional_question_formulation.py`
- `bounded_inquiry_frontier_question_handoff_audit_001.md`

## Existing lawful owners

### Frontier owner

`BoundedInquiryFrontier` is the existing owner for assembling one selected inquiry need plus preserved frontier-boundary testimony into an established or refused frontier. Its own boundary is explicit: it assembles only from already-preserved boundary testimony and does not formulate a question, open inquiry, select sources or observations, authorize access, start execution, start recording, write the event ledger, mutate the cluster, or know the result.

The frontier owner therefore may not itself produce the question expression. It can supply only the established frontier and its preserved clauses as input to a separate formulation responsibility.

### Boundary-testimony owner

`InquiryFrontierBoundaryTestimony` is the existing owner for preserving stage-owned clauses for one exact selected inquiry need. Its clause records preserve producer lineage, adapter lineage, source lineage, evidence classes, provenance roles, already-visible evidence refs, eligible evidence territory refs, standing, scope disposition, evidence currency, evidence availability, and family disposition.

This owner may lawfully provide the testimony basis for a later formulation owner, but it also does not formulate a question.

### Canonical question owner

`BoundedConstitutionalQuestion` is the canonical question artifact. `produce_bounded_constitutional_question(...)` can receive explicit question fields and preserve them as one immutable bounded constitutional question. The operator-ingress formulation path, `formulate_bounded_constitutional_question(...)`, is lawful only for the existing operator expression / interpretation / authority-scope-binding handoff. It does not accept a `BoundedInquiryFrontier`.

The canonical question owner may receive the final frontier-derived question payload, but it is not by itself the lawful grammar owner for frontier-to-question equivalence.

## Determination: lawful formulation owner

No existing implemented owner may currently express one `BoundedInquiryFrontier` as one structurally equivalent `BoundedConstitutionalQuestion`.

The lawful owner must be a small read-only frontier-question formulation testimony producer. It should sit between the established frontier and the existing canonical question producer:

```text
established BoundedInquiryFrontier
+ explicit stage-owned frontier-question formulation testimony
→ explicit produce_bounded_constitutional_question(...) inputs
→ BoundedConstitutionalQuestion
```

This is not a second constitutional-question artifact. It is a testimony and adapter responsibility that proves the canonical question payload is structurally equivalent to one established frontier before delegating to the existing canonical question producer.

## Required formulation testimony

The testimony must be explicit and conjunctive. It must preserve the following four expressions separately:

1. **Question expression testimony**: the exact bounded question string to pass to `bounded_question`, plus a deterministic explanation that every operative frontier clause is represented exactly once and no clause was interpreted into broader or narrower wording.
2. **Constitutional-intent testimony**: the exact intent string to pass to `constitutional_intent`, derived only from the frontier's selected inquiry need and clause families, not from new semantic interpretation.
3. **Uncertainty-expression testimony**: the exact uncertainty and Unknown entries to pass to `uncertainty` and `unknowns`, including unsupported, unknown, stale, unavailable, mixed, adjacent-family, out-of-scope, and non-operative clause references without resolving them.
4. **Scope-status expression testimony**: the exact scope-status string and structured caller fields preserving included scope, excluded scope, eligible evidence territory, ineligible or out-of-scope territory, sufficient-resolution conditions, and lawful stopping conditions.

The testimony must also preserve these negative statements:

- question formulation is not scope expansion;
- question formulation is not scope narrowing;
- question formulation is not uncertainty reinterpretation;
- eligible evidence territory is not selected evidence;
- sufficient-resolution conditions are not satisfied results;
- lawful stopping conditions are not completed inquiry;
- one frontier produces at most one canonical question.

## Frontier clause mapping into canonical question fields

Every operative frontier clause must map into canonical question fields by reference and content, not by similarity.

| Frontier material | Canonical question field(s) | Required preservation rule |
| --- | --- | --- |
| `frontier_id` | `inquiry_provenance`; `caller_supplied_fields` | Preserve exact frontier identity as the source frontier. |
| `selected_need_selection_id` | `inquiry_provenance`; `caller_supplied_fields` | Preserve exact selected-need selection identity. |
| `selected_need_reference_id` | `inquiry_provenance`; `caller_supplied_fields` | Preserve exact selected inquiry need; absence refuses formulation. |
| `native_projection_id` and `native_lineage` | `inquiry_provenance`; `caller_supplied_fields` | Preserve native source lineage without rewriting it as fact. |
| `need_set_id`, `selected_goal_id`, `horizon_id` | `caller_supplied_fields` | Preserve inquiry-need context and horizon separately from question text. |
| `testimony_id` and `source_testimony_ref` | `inquiry_provenance`; `caller_supplied_fields` | Preserve boundary-testimony lineage. |
| `bounded_uncertainty_component_ref` | `uncertainty`; `caller_supplied_fields` | Preserve uncertainty component identity; absence refuses formulation. |
| `repository_world_subject_ref` | `bounded_question`; `scope_status`; `caller_supplied_fields` | Preserve exact subject reference; do not infer another subject from prose. |
| Operative `included_excluded_inquiry_scope` clauses | `bounded_question`; `scope_status`; `caller_supplied_fields` | Include every operative included/excluded scope clause exactly once; no omission, broadening, or narrowing. |
| Operative `eligible_ineligible_evidence_territory` clauses | `scope_status`; `caller_supplied_fields`; possibly `uncertainty` for non-operative territory | Preserve as evidence territory only; do not select sources, evidence, observations, files, hosts, services, or runtime entities. |
| Operative `sufficient_resolution_conditions` clauses | `constitutional_intent`; `scope_status`; `caller_supplied_fields` | Preserve as conditions for resolution; do not mark satisfied. |
| Operative `lawful_stopping_conditions` clauses | `scope_status`; `caller_supplied_fields` | Preserve as stopping conditions; do not mark inquiry complete. |
| `unknown_clause_refs` | `unknowns`; `caller_supplied_fields` | Preserve Unknowns as Unknowns. |
| `unsupported_clause_refs`, `stale_clause_refs`, `unavailable_clause_refs`, `mixed_clause_refs`, `adjacent_family_clause_refs`, `out_of_scope_clause_refs`, `non_operative_clause_refs` | `uncertainty`; `caller_supplied_fields` | Preserve non-operative or unresolved material without converting it into operative scope. |
| `material_conflict_clause_refs` and required-family gaps | Refusal, not question fields | Conflicts or missing required families refuse formulation. |
| All `clauses` | `caller_supplied_fields` or a structured testimony record referenced from `inquiry_provenance` | Preserve complete clause inventory so structural equivalence is auditable. |

The bounded question string itself should be a compact expression of the frontier, not a transcript of the original operator inquiry. Structural equivalence is proven by the mapping testimony and structured caller fields, not by preserving frontier metadata alone.

## Lineage preservation

The formulation testimony must preserve producer, grammar, frontier, selected-need, and original operator lineage as distinct entries.

Minimum lineage fields:

- `frontier_question_formulation_testimony_id`;
- `formulation_owner_ref`;
- `formulation_grammar_ref` or `formulation_convention`;
- `frontier_ref`;
- `frontier_testimony_ref`;
- `selected_need_selection_id`;
- `selected_need_reference_id`;
- `native_projection_id`;
- `native_lineage`;
- `source_testimony_ref`;
- `bounded_uncertainty_component_ref`;
- `repository_world_subject_ref`;
- clause-level `producer_ref` and `producer_lineage`;
- clause-level `adapter_ref` and `adapter_lineage` where present;
- original operator ingress reference, if present in upstream native lineage or source testimony.

Original operator lineage must not be collapsed into `operator_inquiry` when the question is frontier-derived. The canonical question should preserve the operator inquiry as original ingress testimony, while the bounded question text should preserve the frontier-derived formulation.

## Ingress-provenance extension

Yes. The existing `BoundedConstitutionalQuestion` warrants a small ingress-provenance extension before frontier-derived questions become executable.

Current fields can encode provenance as strings, but they do not type the ingress lane. That is sufficient for direct operator ingress, but insufficient to keep frontier-derived ingress distinct without relying on ad hoc string conventions.

The smallest extension is one optional structured ingress-provenance field on the existing artifact, not a new question artifact. Suggested shape:

```text
ingress_provenance = {
  ingress_kind: "direct_operator" | "frontier_derived",
  original_operator_inquiry: <text or ref>,
  frontier_ref: <frontier id or absent>,
  formulation_testimony_ref: <testimony id or absent>,
  formulation_grammar_ref: <grammar/convention id>,
  selected_need_reference_id: <ref or absent>,
  source_lineage: (<refs...>)
}
```

For backward compatibility, direct operator questions may default to `ingress_kind=direct_operator` when the field is absent. Frontier-derived questions must set `ingress_kind=frontier_derived` and preserve both original operator lineage and the frontier formulation lineage.

## Direct operator ingress remains distinct

Direct operator ingress remains:

```text
AttributedOperatorExpression
→ OperatorExpressionInterpretationProjection
→ OperatorAuthorityScopeBindingProjection
→ formulate_bounded_constitutional_question(...)
→ BoundedConstitutionalQuestion
```

Frontier-derived ingress should be:

```text
BoundedInquiryFrontier
+ FrontierQuestionFormulationTestimony
→ produce_bounded_constitutional_question(...)
→ BoundedConstitutionalQuestion
```

The distinction is not the final artifact. The distinction is the ingress lane and provenance:

- direct operator ingress preserves the operator inquiry as the immediate source of the formulated question;
- frontier-derived ingress preserves the operator inquiry as upstream lineage, while the immediate source is one established frontier plus stage-owned formulation testimony;
- frontier-derived `bounded_question` must not be verbatim operator inquiry unless the formulation testimony proves exact structural equivalence without loss or expansion;
- direct operator questions need not carry `frontier_ref`; frontier-derived questions must carry it.

## Refusal rules

The formulation owner must refuse, deterministically and read-only, when any condition below is true:

1. `frontier.frontier_state != "established"`.
2. `frontier.missing_required_clause_families` is non-empty.
3. `frontier.material_conflict_clause_refs` is non-empty.
4. `frontier.selected_need_reference_id` is absent.
5. `frontier.bounded_uncertainty_component_ref` is absent.
6. `frontier.repository_world_subject_ref` is absent.
7. Required operative clause families are absent, duplicated in a way that cannot map one-to-one, or structurally nonequivalent to the proposed question payload.
8. The proposed question omits an operative frontier clause.
9. The proposed question broadens scope, narrows scope, changes eligible evidence territory into selected evidence, treats sufficient-resolution conditions as satisfied, or treats stopping conditions as completion.
10. The proposed question merges adjacent uncertainties, splits one frontier into multiple questions, or combines multiple frontiers.
11. The proposed formulation depends on interpreting clause prose to invent subjects, evidence, observations, authority, or results.
12. Original operator lineage cannot be preserved separately from frontier-derived formulation lineage.

Ambiguous, conflicting, incomplete, or structurally nonequivalent formulations are therefore not malformed questions. They are refused formulation attempts.

## Is one read-only implementation slice warranted?

Yes, but only one small slice is warranted.

The warranted slice should add a read-only frontier-question formulation testimony producer and adapter that:

- accepts exactly one established `BoundedInquiryFrontier`;
- accepts or constructs explicit stage-owned formulation testimony;
- validates one-to-one structural equivalence between operative frontier clauses and canonical question fields;
- delegates to `produce_bounded_constitutional_question(...)`;
- returns the existing `BoundedConstitutionalQuestion`;
- preserves typed ingress provenance distinguishing direct operator ingress from frontier-derived ingress;
- refuses non-established, conflicting, incomplete, ambiguous, or nonequivalent frontiers;
- writes no event ledger and mutates no cluster state.

No diagnostic, audit CLI, probe, view, operational flag, or recordable output is required by this audit document itself. If the implementation slice exposes a diagnostic or recordable output, the diagnostic inventory and shape-audit responsibilities apply.

## Smallest missing responsibility

The smallest missing responsibility is:

> Given one established `BoundedInquiryFrontier` and explicit stage-owned frontier-question formulation testimony, prove that every operative frontier clause maps exactly once into the existing `BoundedConstitutionalQuestion` fields, preserve frontier-derived ingress separately from original direct operator inquiry, refuse ambiguity/conflict/incompletion/nonequivalence, and delegate to `produce_bounded_constitutional_question(...)` without opening inquiry, selecting evidence, authorizing observation, executing, recording, writing the event ledger, or mutating state.

## Exact next bounded question

What is the minimal read-only frontier-question formulation testimony producer that consumes one established `BoundedInquiryFrontier`, preserves producer, grammar, frontier, selected-need, original operator, uncertainty, subject, scope, evidence-territory, sufficient-resolution, and lawful-stopping lineage, proves one-to-one structural equivalence to the existing `BoundedConstitutionalQuestion` fields, distinguishes frontier-derived ingress from direct operator ingress with a small typed provenance extension, refuses ambiguous/conflicting/incomplete/nonequivalent formulations, and delegates to `produce_bounded_constitutional_question(...)` without broadening, narrowing, reinterpreting uncertainty, selecting evidence, opening inquiry, authorizing observation, executing, recording, writing the event ledger, or mutating state?

Frontier question formulation testimony audit complete.
