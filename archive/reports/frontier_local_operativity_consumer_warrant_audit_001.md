# Frontier-local operativity consumer warrant audit 001

## Boundary of this investigation

This is one bounded, read-only investigation of the consumer-local warrant required before preserved frontier-boundary testimony may contribute to frontier-local operativity. It examines only the implemented responsibility that produces the `BoundedInquiryFrontier` operative relation from one selected inquiry need and one preserved `InquiryFrontierBoundaryTestimony` artifact.

It does not design an admission layer, warrant engine, ownership registry, clause lifecycle, standing service, or universal frontier architecture. It does not inspect the whole frontier pipeline.

## Book expectation applied

The applicable Book expectation is claim-relative and consumer-local: weaker, attributed, or unowned upstream testimony may sometimes be considered and relied upon premise-relatively, but only where the consumer possesses warrant sufficient for the exact narrower assertion it produces. The current Book-side recovery also preserves that frontier identity is conjunctive: the exact need or uncertainty, source and provenance, current movement or consumer-local boundary, scope, available evidence territory, sufficiency and stopping conditions, Unknowns, conflicts, and negative authority must remain bounded rather than inferred from wording, order, labels, stale evidence, unavailable evidence, or selected-need standing alone.

For this audit, the expected lawful pattern is therefore:

```text
source-relative preserved testimony
+ preserved ownership/source limits
+ consumer-local identity/coherence/coverage checks
→ bounded premise-relative frontier-local operative relation
```

The forbidden shortcut is:

```text
Book permits local reliance
→ every consumed coordinate is faithfully warranted
```

## Exact consumer assertion

The exact consumer is `assemble_bounded_inquiry_frontier(...)` in `seed_runtime/bounded_inquiry_frontier.py`.

The exact local assertion it can produce is not "this clause is intrinsically true" or "this clause has producer-owned standing." The assertion is narrower:

```text
for this selected inquiry need artifact and this preserved testimony artifact,
this preserved clause is operative for this exact bounded frontier assembly
```

The produced artifact exposes that assertion through `operative_clause_refs`, with the overall frontier state set to `established`, `missing_required_clause_family`, `material_binding_conflict`, or `not_selected_inquiry_need`.

The consumer explicitly does not create stronger standing: it remains read-only; it does not invent scope, admit evidence, formulate a question, open inquiry, select sources or observations, authorize access, start execution, start recording, write the event ledger, mutate the cluster, or know the result.

## Prior consumer standing

The consumer's prior standing is limited to receiving two typed artifacts:

1. an `AdvancementNeedConsiderationSelection`; and
2. an `InquiryFrontierBoundaryTestimony`.

The testimony preservation responsibility binds clauses to the selected need when a selected inquiry reference exists, copies clause coordinates as supplied, and records ownership basis as `stage_producer_lineage`, `adapter_lineage`, or `unowned` from lineage-field presence. It does not assemble the frontier or verify the truth of the copied coordinates.

The frontier consumer therefore begins with typed, preserved, source-relative testimony plus selected-need fields. It does not begin with verified clause truth, verified producer occurrence, or universal admission standing.

## Witness path recovered independently

```text
Book expectation
→ claim-relative warrant required for local reliance

frontier consumer responsibility
→ assemble one read-only bounded inquiry frontier from a selected need plus preserved testimony

inputs and validations actually consumed
→ selected state, inquiry family, selected-reference identity equality, native projection equality, native lineage equality, need-set equality, selection-id equality, goal identity equality, horizon equality, clause_standing, family_disposition, evidence_currency, evidence_availability, scope_disposition for scope clauses, required-family coverage, explicit conflicts

exact assertion produced
→ operative clause references and frontier state for this assembly only

classification
→ mixed: identity and operative coverage are consumer-local checks; the clause-coordinate values mostly remain supplied testimony rather than independently established by this consumer
```

## Identity warrant

### What the consumer verifies

The assembler refuses or conflicts when the selection is not selected, when no selected reference exists, when the selected reference is not `family == "inquiry"`, or when testimony fields disagree with the selected reference across:

- selected inquiry need identity;
- native projection identity;
- native lineage;
- need-set identity;
- selected-need selection identity;
- goal identity;
- horizon identity.

The testimony preservation step also derives `source_testimony_ref`, `bounded_uncertainty_component_ref`, and `repository_world_subject_ref` from `ref.native_lineage` and carries them into each clause.

### What this warrants

Classification: **A for local identity coherence; D/F for producer occurrence or lineage truth.**

The consumer independently establishes that the selected-need artifact and preserved-testimony artifact cohere for this assembly boundary. That warrants local identity binding for the frontier relation.

It does not prove testimony truth, native-lineage provenance, source-testimony occurrence, component occurrence, subject truth, or intrinsic clause standing. Matching fabricated fields could satisfy the equality checks, so identity coherence cannot be promoted into producer occurrence.

## Clause-standing warrant

### What the consumer verifies

The operative predicate requires:

```text
clause.clause_standing == "established"
```

The consumer rejects stronger/non-establishing values for operativity: `unsupported`, `unknown`, `conflicting`, and `unclassified` do not become operative. Explicit `conflicting` standing also becomes a material conflict and prevents frontier establishment.

### What this warrants

Classification: **D for intrinsic clause standing; B for narrower premise-relative operative use when other local checks pass.**

The consumer does not independently verify why `clause_standing` is established. The preservation producer copies the supplied value. The frontier consumer reads that value and uses it as an operative predicate.

What is warranted locally is only the conditional assertion:

```text
given preserved testimony that carries clause_standing == established,
and given the consumer's other identity/conflict/coverage checks,
this clause may count as operative for this bounded frontier assembly
```

The repository evidence does not show that this consumer requires producer-backed standing or verifies the establishment basis. Rejecting weaker values prevents over-inclusion, but it is not positive warrant that the accepted `established` value was lawfully established upstream.

## Family warrant

### What the consumer verifies

The operative predicate requires:

```text
clause.family_disposition == "inquiry"
```

The frontier as a whole requires operative coverage of all four required clause families:

- `included_excluded_inquiry_scope`;
- `eligible_ineligible_evidence_territory`;
- `sufficient_resolution_conditions`;
- `lawful_stopping_conditions`.

`mixed` and `adjacent_family` clauses are preserved but non-operative.

### What this warrants

Classification: **B/D.**

The consumer locally verifies exact enum equality and required-family coverage among clauses that pass the operative predicate. This warrants only consumer-local family coherence for the assembly.

It does not independently establish an inquiry-family classifier, family owner, or repository-owned relation proving that the clause belongs to the inquiry frontier family. The family disposition is supplied testimony copied by preservation and consumed by the assembler. Therefore `family_disposition == inquiry` supports a narrower premise-relative operative relation, not intrinsic inquiry-family standing.

## Scope warrant

### What the consumer verifies

For the `included_excluded_inquiry_scope` clause family, the operative predicate additionally requires:

```text
clause.scope_disposition == "included"
```

A scope value of `conflicting` becomes a material conflict. A scope value of `outside_current_scope` is preserved and listed in `out_of_scope_clause_refs`, but it is non-operative.

### What this warrants

Classification: **B/D, with A only for local refusal/coherence.**

The consumer checks the supplied scope disposition only for the scope clause family. It does not independently establish who owns the scope, what prior standing places the clause inside it, or whether goal-horizon scope is inquiry scope. The testimony boundary notes explicitly separate goal-horizon scope from inquiry scope.

Thus identity binding alone is not sufficient scope warrant. The local positive warrant is narrower: where preserved testimony supplies `scope_disposition == included` for an inquiry-family established scope clause, and identity/conflict checks pass, the clause can be operative for this assembly. The intrinsic inclusion standing remains supplied testimony rather than independently verified by this consumer.

## Currency warrant

### What the consumer verifies

The operative predicate refuses only:

```text
evidence_currency == "conflicting"
```

It does not refuse `stale` or `unknown` currency. Tests show stale clauses can remain preserved and listed as stale while a frontier remains established if required current/available clauses also satisfy coverage.

### What this warrants

Classification: **F/D for stale or unknown as sufficient operativity; A only for conflict refusal.**

The implementation clearly treats `conflicting` currency as disqualifying. It clearly preserves stale testimony as visible/non-erased. However, it does not check `evidence_currency == current` for operativity. Therefore the repository does not support a conclusion that this consumer has positive currentness warrant for every operative clause.

Separate determinations:

- stale testimony may remain visible: **supported**;
- stale testimony may remain relevant or preserved: **supported as preservation/listing, not as truth**;
- stale testimony may satisfy required-family operativity: **implementation permits it if other predicate values pass, but the consumer-local warrant for that sufficiency is Unknown/insufficient in the inspected evidence**.

Currency matters relative to the current bounded frontier assembly and its available evidence territory. The consumer preserves stale/unknown coordinates but does not establish that stale/unknown currency is sufficient for frontier establishment.

## Availability warrant

### What the consumer verifies

The operative predicate refuses only:

```text
evidence_availability == "conflicting"
```

It does not refuse `unavailable` or `unknown` availability. Tests show unavailable clauses can remain preserved and listed as unavailable while a frontier remains established if required clauses otherwise cover the required families.

### What this warrants

Classification: **F/D for unavailable or unknown as sufficient operativity; A only for conflict refusal.**

Availability is not independently verified by this consumer. The preservation module copies the supplied availability value and explicitly does not authorize access, select sources, or select observations.

Separate determinations:

- available to whom: **Unknown from this consumer**;
- available when: **Unknown except as supplied coordinate**;
- available for what act: **not for source selection, observation selection, access authorization, execution, or recording**;
- unavailable testimony may describe a boundary: **supported by preservation/listing**;
- unavailable testimony may satisfy the frontier's available-evidence-territory requirement: **implementation may allow it, but positive consumer-local warrant is insufficient/Unknown**.

Availability is not applicability, admission, consumption, or sufficient support.

## Unowned limitation

Classification: **B for permitted consideration under preserved negative limit; not A/C for ownership.**

The testimony preservation responsibility marks a clause `unowned` when neither producer lineage nor adapter lineage is present. The frontier assembler does not consult `ownership_basis` when deciding operative coherence. Therefore unowned testimony is not unusable testimony in the current implementation.

However, `unowned` is only a negative limit. It supplies no positive support. The lawful implementation-supported movement is:

```text
preserved source-relative clause testimony
+ preserved unowned limitation where lineage is absent
+ consumer-local identity/coherence/coverage checks
→ bounded premise-relative operative relation
```

The forbidden movement remains unsupported:

```text
unowned status
→ warrant
```

## Operative-clause warrant

Classification: **mixed A/B/D/F by coordinate.**

A clause becomes operative for this consumer only when the consumer sees:

```text
clause_standing == established
family_disposition == inquiry
evidence_currency != conflicting
evidence_availability != conflicting
and, for included_excluded_inquiry_scope, scope_disposition == included
```

The consumer-local warrant is strongest for:

- exact selected-need/testimony identity coherence;
- refusal when the selection is not a selected inquiry need;
- refusal on explicit identity or coordinate conflicts;
- required-family coverage among locally operative clauses;
- negative boundaries that the result is read-only and non-mutating.

The consumer-local warrant is weaker or insufficient for:

- the truth or upstream establishment basis of `clause_standing == established`;
- the classification basis behind `family_disposition == inquiry`;
- the scope owner and prior standing behind `scope_disposition == included`;
- positive currentness for stale/unknown currency;
- positive availability for unavailable/unknown availability;
- producer occurrence or owner-backed lineage.

## Whole-frontier establishment warrant

Consumer-local operativity warrant is not identical to whole-frontier establishment warrant.

The whole frontier reaches `frontier_state == "established"` only when:

1. the selected need is selected, present, and inquiry-family;
2. testimony identity bindings match the selected reference;
3. no material identity or explicit coordinate conflicts are present; and
4. every required clause family appears among locally operative clauses.

One operative clause does not warrant the whole frontier. Conversely, complete family coverage does not warrant reliance upon every preserved clause, because non-operative clauses remain preserved as unsupported, unknown, mixed, adjacent-family, stale, unavailable, or out of scope.

## Lawful asymmetries

- Producer ownership is not consumer-local warrant.
- Consumer-local warrant is not producer ownership.
- Unowned testimony can be considered, but unowned status is not support.
- Identity coherence can warrant local binding without proving testimony truth.
- Required-family coverage can warrant local frontier establishment without proving intrinsic clause standing.
- Preserved stale or unavailable testimony can remain visible without satisfying a positive current/available evidence requirement.
- `frontier_state == established` is not inquiry opening, source selection, observation selection, access authorization, execution, recording, mutation, or result knowledge.

## Possible crossings

The first unsupported or insufficiently warranted movement appears at positive reliance on supplied clause-coordinate values as established standing rather than as premise-relative testimony.

Potential crossings by coordinate:

- **Clause-standing:** the consumer consumes `clause_standing == established` but does not verify the establishment basis. If the produced assertion is read as intrinsic clause standing, this crosses. If read as premise-relative operative use, it is bounded but depends on preserving the testimony limit.
- **Family:** the consumer consumes `family_disposition == inquiry` without independently establishing classification warrant. Intrinsic inquiry-family standing would cross; local family-coherence use is narrower.
- **Scope:** the consumer consumes `scope_disposition == included` without establishing scope ownership or prior inclusion standing. Intrinsic scope standing would cross; local predicate use is narrower.
- **Currency:** because only `conflicting` is refused, stale or unknown testimony can satisfy the predicate. Positive currentness warrant is unsupported.
- **Availability:** because only `conflicting` is refused, unavailable or unknown testimony can satisfy the predicate. Positive availability warrant is unsupported.

No crossing is found merely because the assembler compresses several predicate checks into `_is_operatively_coherent(...)`. The crossing risk appears only if the resulting operative relation is interpreted as stronger than the local predicate and preserved testimony limits support.

## Remaining Unknowns

- Whether an upstream stage or adapter actually verifies clause standing before creating `FrontierBoundaryClauseInput`.
- Whether any repository-owned relation establishes inquiry-family disposition for a clause beyond supplied field value.
- Who owns the inquiry scope and what prior standing places a specific clause inside it.
- Whether stale testimony is intentionally allowed to satisfy required-family operativity or whether the predicate should require `current`.
- Whether unavailable testimony is intentionally allowed to satisfy required-family operativity or whether the predicate should require `available`.
- Whether direct construction in tests is only a permissive fixture pattern or represents intended runtime inputs.
- Whether complete frontier establishment requires positive current and available evidence territory beyond the current local predicate.

## Required determinations

### What permits consideration?

Preserved testimony for one exact selected inquiry need permits consideration when the selected need is a selected inquiry reference and the testimony carries the selected need, native projection, native lineage, need set, goal, horizon, component, and subject bindings. Unowned clauses remain eligible for consideration only as preserved testimony with a negative ownership limit.

### What permits local reliance?

Local reliance is permitted only by the assembler's claim-relative checks: selected inquiry gate, identity equality between selected reference and testimony, absence of material conflicts, and operative predicate satisfaction for the clause. This is premise-relative reliance on supplied clause coordinates, not verification of coordinate truth.

### What permits operative projection?

Operative projection is permitted by the local operative predicate plus identity/conflict conditions:

```text
clause_standing == established
family_disposition == inquiry
evidence_currency != conflicting
evidence_availability != conflicting
scope_disposition == included for the scope clause family
matching selected-need/testimony identity
no material conflicts
```

This permits `operative_clause_refs` only within the resulting `BoundedInquiryFrontier` artifact.

### What permits complete frontier establishment?

Complete frontier establishment requires the operative projection above to cover all four required clause families, with no material identity or coordinate conflict and with a selected inquiry need. Complete establishment remains read-only frontier-coherence standing. It is not authority to open inquiry, select evidence, access sources, execute, record, mutate, or declare a result known.

## Bounded answer

> What exact consumer-local warrant permits preserved frontier-boundary testimony to contribute to a frontier-local operative relation, and which coordinates remain insufficient or Unknown?

The exact consumer-local warrant is the `BoundedInquiryFrontier` assembler's selected-inquiry gate, selected-reference/testimony identity equality checks, explicit conflict refusal, and local operative predicate over preserved clause coordinates, followed by required-family coverage for whole-frontier establishment. That warrant permits only a bounded premise-relative assertion that a preserved clause contributes to this exact frontier assembly's operative relation.

Identity coherence, explicit conflict refusal, required-family coverage, and negative read-only/non-mutating boundaries are independently established by the consumer. Clause standing, inquiry-family disposition, included-scope disposition, positive currentness, and positive availability are not independently established by this consumer; they remain supplied attributed or unowned testimony, insufficient for intrinsic clause standing and Unknown or insufficient as positive current/available evidence-territory warrant where the implementation only rejects conflicts.
