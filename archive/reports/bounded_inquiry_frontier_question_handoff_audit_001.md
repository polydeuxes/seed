# Bounded Inquiry Frontier Question Handoff Audit 001

## Scope

This audit determines the smallest lawful handoff:

```text
BoundedInquiryFrontier
→ BoundedConstitutionalQuestion
```

It audits the existing bounded-question owner before introducing any new question artifact. It does not implement a new runtime path, formulate a live question instance, open inquiry, select evidence, authorize observation, execute investigation, record findings, write the event ledger, or mutate state.

## Repository evidence reviewed

- `seed_runtime/bounded_inquiry_frontier.py`
- `seed_runtime/bounded_constitutional_question.py`
- `tests/test_bounded_constitutional_question.py`
- `tests/test_bounded_constitutional_question_formulation.py`
- `tests/test_bounded_inquiry_frontier.py`
- `bounded_constitutional_question_formulation_slice_001.md`
- `bounded_inquiry_frontier_slice_001.md`
- `inquiry_frontier_boundary_testimony_audit_001.md`
- `bounded_inquiry_frontier_audit_001.md`

## Existing bounded-question owner

The current owner is `seed_runtime.bounded_constitutional_question.BoundedConstitutionalQuestion`, produced by `produce_bounded_constitutional_question(...)` and, for operator ingress, by `formulate_bounded_constitutional_question(...)`.

The module states its boundary directly: it owns only `Operator Inquiry -> BoundedConstitutionalQuestion`. It preserves explicit caller inputs as evidence/testimony and refuses view projection, capability discovery, authority selection, ledger writes, and cluster mutation.

The artifact currently requires these canonical question fields:

1. `bounded_question_id`.
2. `operator_inquiry`.
3. `inquiry_provenance`.
4. `bounded_question`.
5. `constitutional_intent`.
6. `scope_status`.
7. `uncertainty`.
8. `unknowns`.
9. optional `caller_supplied_fields`.
10. fixed testimony and read-only boundary fields.
11. fixed read-only, no-ledger, no-mutation flags.

The deterministic producer accepts only explicit caller inputs for the same substantive fields. It derives identity from the exact payload unless an id is supplied. That means the existing owner can preserve a question-shaped handoff, but only after a producer has supplied explicit `operator_inquiry`, `bounded_question`, `constitutional_intent`, `scope_status`, uncertainty, Unknowns, provenance, and caller-supplied fields. The owner does not itself know how to read a `BoundedInquiryFrontier`.

## Existing frontier owner

The existing frontier owner is `seed_runtime.bounded_inquiry_frontier.BoundedInquiryFrontier`, assembled by `assemble_bounded_inquiry_frontier(...)` from one selected inquiry need and matching frontier-boundary testimony.

Its module boundary states that it consumes one exact selected inquiry need plus preserved frontier-boundary testimony, and only determines whether already supplied boundary clauses coherently establish a bounded inquiry frontier. It explicitly does not invent scope, admit evidence, formulate a question, open inquiry, authorize, execute, record, write the event ledger, or mutate state.

A frontier is established only when:

1. the selected need is actually selected;
2. the selected reference exists and is an inquiry family reference;
3. selection/testimony identity bindings match;
4. no material binding conflict exists;
5. required clause families are operatively coherent:
   - included/excluded inquiry scope;
   - eligible/ineligible evidence territory;
   - sufficient-resolution conditions;
   - lawful stopping conditions.

The frontier preserves lineage, bounded uncertainty component reference, repository/world subject reference, operative and preserved clause references, missing required families, conflict references, unsupported/unknown/mixed/adjacent/stale/unavailable/out-of-scope clause references, all clauses, and negative authority flags proving it does not formulate a question or open inquiry.

## Can `BoundedConstitutionalQuestion` consume frontier-derived testimony directly?

No.

The existing bounded-question producer consumes explicit caller-oriented question fields, not a `BoundedInquiryFrontier`. The operator-ingress formulation path consumes operator expression interpretation plus authority/scope binding and a future bounded-question handoff. No reviewed function accepts a frontier, validates frontier state, converts operative clauses into question fields, or proves structural equivalence between frontier and question.

Directly passing frontier-derived testimony into `produce_bounded_constitutional_question(...)` would be technically possible only by a caller manually choosing strings for `operator_inquiry`, `bounded_question`, `constitutional_intent`, `scope_status`, `uncertainty`, `unknowns`, and `caller_supplied_fields`. That manual call would not prove:

- one frontier became one question;
- the frontier was established;
- all frontier scope/evidence/sufficiency/stopping boundaries were preserved;
- unknown/conflicting/incomplete frontiers were refused;
- eligible evidence territory was preserved as territory rather than selected evidence;
- question wording did not broaden, narrow, or reinterpret frontier authority.

Therefore, the existing owner can receive a final canonical question artifact, but cannot lawfully consume frontier-derived testimony directly without an adapter/handoff producer.

## Smallest missing adapter or handoff artifact

The smallest missing responsibility is a read-only adapter that consumes exactly one established `BoundedInquiryFrontier` and produces exactly one existing `BoundedConstitutionalQuestion` by delegation to `produce_bounded_constitutional_question(...)`.

A new question artifact is not warranted. The repository already has the canonical question artifact. The missing piece is a frontier-to-question handoff producer, not another question owner.

A minimal adapter should own only this transition:

```text
established BoundedInquiryFrontier
→ explicit BoundedConstitutionalQuestion producer inputs
→ existing BoundedConstitutionalQuestion
```

It should not own inquiry selection, frontier assembly, evidence selection, source selection, observation selection, access authorization, inquiry opening, investigation execution, result judgment, recording, ledger writes, or state mutation.

## Required structural equivalence proof

The adapter must prove equivalence by deterministic field preservation, not by semantic similarity. The proof should be conjunctive.

### Identity and lineage

- `frontier.frontier_id` must be preserved in `inquiry_provenance` or `caller_supplied_fields`.
- `selected_need_selection_id`, `selected_need_reference_id`, `native_projection_id`, `native_lineage`, `need_set_id`, `selected_goal_id`, `horizon_id`, `testimony_id`, and `source_testimony_ref` must be preserved as caller-supplied or provenance fields.
- The resulting `bounded_question_id` must be deterministic over the frontier-derived payload.

### Uncertainty component

- `bounded_uncertainty_component_ref` must be preserved.
- Any `unknown_clause_refs`, `unsupported_clause_refs`, `stale_clause_refs`, `unavailable_clause_refs`, and non-material unresolved testimony must appear in `unknowns` or `uncertainty` without becoming resolved.
- Any conflict reference must refuse the handoff rather than become a weaker Unknown.

### Repository/world subject

- `repository_world_subject_ref` must be preserved exactly.
- No additional subject may be inferred from wording or clause text.

### Included and excluded scope

- Operative included scope clauses must be represented in `scope_status` or structured caller fields.
- Out-of-scope and excluded boundary clauses must remain excluded boundary material.
- The adapter must not widen included scope by summarizing several clauses into broader prose.
- The adapter must not narrow scope by omitting an operative included clause.

### Eligible evidence territory

- Eligible evidence territory clauses must be preserved as eligible territory only.
- Ineligible or out-of-scope territory must remain ineligible or excluded.
- No evidence item, source, observation, file, host, service, corpus member, or runtime entity may be selected by the adapter.

### Sufficient-resolution conditions

- Operative sufficient-resolution clauses must be preserved as conditions for resolution.
- They must not be treated as satisfied.

### Lawful stopping conditions

- Operative lawful stopping clauses must be preserved as stopping conditions.
- They must not be treated as inquiry completion.

### Unknowns and conflicts

- Unsupported, unknown, stale, unavailable, mixed, adjacent-family, and out-of-scope clause refs must remain visible.
- Material conflicts must refuse handoff.
- Missing required clause families must refuse handoff.

## Refusal rules

The adapter must refuse with a deterministic formulation error, or a narrower frontier-question handoff error if introduced, when any of the following is true:

1. `frontier.frontier_state != "established"`.
2. `frontier.missing_required_clause_families` is non-empty.
3. `frontier.material_conflict_clause_refs` is non-empty.
4. `frontier.selected_need_reference_id` is absent.
5. `frontier.bounded_uncertainty_component_ref` is absent.
6. `frontier.repository_world_subject_ref` is absent.
7. any required operative clause family cannot be mapped one-to-one into the question payload.
8. the mapping would require interpreting clause prose to infer a new subject, new scope, selected evidence, or a new stopping condition.
9. the mapping would merge adjacent uncertainties or split one frontier into multiple questions.
10. the mapping would omit preserved Unknowns, stale evidence, unavailable evidence, excluded scope, or ineligible territory.

Incomplete, ambiguous, conflicting, non-established, or identity-mismatched frontiers are therefore not question inputs. They remain frontier artifacts with refusal evidence.

## Is one implementation slice warranted?

Yes, if Seed needs the handoff to become executable.

The slice should be smaller than constitutional pipeline redesign and smaller than inquiry execution. It should add one read-only frontier-to-existing-question adapter, plus tests proving:

- an established frontier delegates to `produce_bounded_constitutional_question(...)` and returns a `BoundedConstitutionalQuestion`;
- frontier id, selection id, need reference id, lineage, uncertainty component, repository/world subject, scope clauses, eligible evidence territory, sufficient-resolution conditions, stopping conditions, Unknowns, and non-operative clause refs are preserved;
- non-established, missing-required-family, conflicting, ambiguous, incomplete, and identity-broken frontiers are refused;
- the resulting question remains read-only, does not write the event ledger, and does not mutate cluster state;
- the adapter does not set or imply inquiry opening, evidence selection, observation selection, source selection, access authorization, execution, recording, or result knowledge.

No diagnostic, audit CLI, probe, view, operational flag, or recordable output is required by this audit document itself. If the later slice adds a public diagnostic or CLI surface, it must update diagnostic inventory, diagnostic shape-audit specs, and the corresponding tests.

## Smallest missing responsibility

The smallest missing responsibility is:

> Given one established `BoundedInquiryFrontier`, deterministically prepare explicit `produce_bounded_constitutional_question(...)` inputs that preserve the frontier's identity, lineage, uncertainty component, repository/world subject, included/excluded scope, eligible/ineligible evidence territory, sufficient-resolution conditions, lawful stopping conditions, Unknowns, and non-operative testimony, while refusing ambiguous, conflicting, incomplete, or non-established frontiers and without opening inquiry, selecting evidence, authorizing access, executing, recording, writing the event ledger, or mutating state.

This responsibility is an adapter responsibility, not a new constitutional-question artifact responsibility.

## Exact next bounded question

What is the minimal read-only frontier-to-existing-question adapter that consumes one established `BoundedInquiryFrontier`, refuses non-established, ambiguous, conflicting, incomplete, or identity-broken frontiers, and delegates to `produce_bounded_constitutional_question(...)` to produce exactly one `BoundedConstitutionalQuestion` preserving the frontier's inquiry-need and lineage identity, uncertainty component, repository/world subject, included and excluded scope, eligible evidence territory, sufficient-resolution conditions, lawful stopping conditions, Unknowns, conflicts, and non-operative testimony without broadening, narrowing, reinterpreting, selecting evidence, opening inquiry, authorizing observation, executing investigation, recording output, writing the event ledger, or mutating state?

Bounded inquiry frontier question handoff audit complete.
