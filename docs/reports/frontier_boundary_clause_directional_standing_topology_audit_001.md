# Frontier Boundary Clause Directional Standing Topology Audit 001

## Scope and bounded starting point

This is one bounded, read-only investigation of directional standing topology around frontier-boundary clauses. It does not implement anything, propose a universal clause lifecycle, design an admission engine, assign a centralized owner, or infer what Seed should contain from an implementation absence.

The investigation starts with one explicitly preserved frontier-boundary clause whose producer or adapter ownership is not established by lineage:

```text
FrontierBoundaryClauseInput(
  clause_ref="clause:payload-owned",
  clause_family="included_excluded_inquiry_scope",
  producer_ref="",
  producer_lineage=(),
  adapter_ref="",
  adapter_lineage=(),
  caller_asserts_ownership=True
)
```

The repository's focused test names this case `clause:payload-owned` and proves that a caller payload flag cannot create ownership. The preserved clause becomes `ownership_basis == "unowned"` and appears in `InquiryFrontierBoundaryTestimony.unowned_clause_refs`.

## Governing constitutional grammar

The governing distinctions are treated directionally, not statically:

```text
visible clause
!= owned clause

owned clause
!= admitted clause

admitted clause
!= operative clause

operative clause
!= frontier established
```

The adjacent repository grammar also forbids these reverse promotions:

```text
consumer admission
!= retroactive producer ownership

frontier operativity
!= proof of upstream ownership

frontier requirement
!= automatic admission

frontier establishment
!= proof that every visible clause was operative
```

The local testimony slice states the ownership rule asymmetrically: ownership is derived only from stage producer lineage or adapter lineage, and clauses without producer lineage or adapter lineage are preserved as unowned rather than upgraded. The implementation carries that grammar in `_ownership(...)`: producer reference plus producer lineage yields `stage_producer_lineage`; adapter reference plus adapter lineage yields `adapter_lineage`; otherwise the clause is `unowned`. A caller assertion is not consumed by that function.

## Initial clause standing

### Prior standing

```text
explicitly preserved frontier-boundary clause testimony
+
producer/adapter ownership unrecognized
```

More precisely, the clause is visible and preserved inside `InquiryFrontierBoundaryTestimony`, but its ownership basis is `unowned`.

### Responsible preserving act

The responsible act is `preserve_inquiry_frontier_boundary_testimony(...)`. For a selected inquiry need, it copies each input clause into an `InquiryFrontierBoundaryClause`, binds it to the selected need, native projection, native lineage, need set, selected goal, horizon, source testimony, uncertainty component, subject, producer or adapter fields, source lineage, evidence classes, provenance roles, separate standing dimensions, and the computed `ownership_basis`.

### Required evidence or warrant

For ownership, the required warrant is one of:

```text
producer_ref + producer_lineage
```

or:

```text
adapter_ref + adapter_lineage
```

The bounded example has neither. Its `caller_asserts_ownership=True` field is intentionally insufficient.

### Preserved prior history

The prior history remains preserved as unowned testimony. The testimony artifact retains the clause reference, family, text, selected-need binding, native lineage, source/evidence/provenance fields, clause standing, scope disposition, evidence currency, evidence availability, and family disposition. It also preserves the unowned status separately in `unowned_clause_refs`.

### Forbidden reverse inference

The existence of the clause in preserved testimony does not prove producer ownership, adapter ownership, admission, operativity, or frontier establishment.

## 1. Independent producer and ownership witness

### Who produces the clause testimony?

The immediate producer of the preserved artifact is the testimony preservation owner, `preserve_inquiry_frontier_boundary_testimony(...)`. The clause input may name a stage producer or adapter, but the selected bounded clause names neither with lineage.

### What exact assertion does the producer make?

For the bounded clause, the preservation owner asserts only this:

```text
the clause was preserved for the exact selected inquiry need,
and its ownership basis is unowned
```

It does not assert that the caller's payload flag makes the clause owned.

### What evidence establishes producer or adapter ownership?

Repository evidence establishes producer or adapter ownership only through lineage:

```text
producer_ref and producer_lineage
```

or:

```text
adapter_ref and adapter_lineage
```

The test `test_ownership_cannot_be_asserted_through_payload_flags` cross-examines the negative case and the adapter-positive case in the same witness. The payload-owned clause remains `unowned`; the adapter-owned clause becomes `adapter_lineage`.

### Can ownership be established after initial preservation?

Unknown for this bounded road. The implementation can preserve a different clause input with adapter lineage as `adapter_lineage`, and the slice says ownership is derived from stage producer lineage or adapter lineage. However, the inspected implementation does not provide a later attribution transition that revises the already preserved clause, attaches new standing to that same clause, or emits a new attributed artifact after the initial preservation.

### If later ownership testimony appears, what happens?

Unknown. Repository evidence supports only this narrower statement:

```text
newly supplied clause input with producer/adapter lineage
→ preserved as stage_producer_lineage or adapter_lineage
```

It does not prove that later testimony revises the original clause, retroactively owns it, attaches a new standing to it, or creates a successor artifact.

## 2. Independent consumer-local admission witness

### Which consumer first considers the clause?

The first downstream consumer inspected here is `assemble_bounded_inquiry_frontier(...)`, which consumes one selected inquiry need plus one `InquiryFrontierBoundaryTestimony` artifact.

### What standing does that consumer actually require?

The assembler requires selected-need/testimony identity coherence, no material binding conflict, and operative coherent clauses for the four required clause families:

```text
included_excluded_inquiry_scope
eligible_ineligible_evidence_territory
sufficient_resolution_conditions
lawful_stopping_conditions
```

For an individual clause to be operatively coherent, `_is_operatively_coherent(...)` requires:

```text
clause_standing == "established"
family_disposition == "inquiry"
evidence_currency != "conflicting"
evidence_availability != "conflicting"
if included_excluded_inquiry_scope: scope_disposition == "included"
```

The consumer-local rule does not check `ownership_basis`.

### May it admit testimony whose upstream ownership is unrecognized, conflicting, or Unknown?

For unrecognized ownership, yes, in the limited sense that `assemble_bounded_inquiry_frontier(...)` may consume preserved testimony containing an unowned clause. The implementation has no ownership-basis gate in `_is_operatively_coherent(...)`, and the frontier assembler carries preserved clauses into the returned frontier.

For conflicting ownership specifically, Unknown. The implemented ownership basis enum has `stage_producer_lineage`, `adapter_lineage`, and `unowned`; it does not encode `conflicting` ownership as an ownership standing. Conflict can exist in clause standing, scope disposition, evidence currency, or evidence availability, and those conflicts block establishment as material binding conflicts, but that is not a recovered ownership-conflict transition.

### If admission is possible, what exact local reliance is permitted?

The consumer-local reliance permitted by the inspected implementation is narrower than upstream ownership:

```text
preserved testimony may be considered for frontier-local operative coherence
```

If the unowned clause also has established clause standing, inquiry family disposition, non-conflicting evidence currency and availability, and the required scope disposition for the scope family, the assembler may count it as operative for family completeness.

### What stronger upstream standing remains explicitly absent?

Producer or adapter ownership remains absent. Admission into the assembler's local coherence check does not rewrite the clause's `ownership_basis`, remove the clause from `unowned_clause_refs`, create producer lineage, create adapter lineage, or repair producer history.

## 3. Independent frontier-local operativity witness

### What owner determines that a clause is operative for one exact frontier-boundary family?

The bounded frontier assembler owns the frontier-local operativity determination through `_is_operatively_coherent(...)` and `assemble_bounded_inquiry_frontier(...)`.

### What standing does it consume?

It consumes preserved `InquiryFrontierBoundaryClause` records from `InquiryFrontierBoundaryTestimony`. It consumes separate dimensions rather than ownership standing:

```text
clause_standing
scope_disposition
evidence_currency
evidence_availability
family_disposition
clause_family
```

### What evidence or comparison performs that transition?

The transition from preserved clause testimony to frontier-local operative standing is performed by comparison against `_is_operatively_coherent(...)`:

- non-`established` clause standings are non-operative;
- non-`inquiry` family dispositions are non-operative;
- conflicting evidence currency or availability is non-operative and also material conflict;
- included/excluded inquiry-scope clauses are operative only when `scope_disposition == "included"`;
- other required families need no scope-included check.

The assembler then compares the resulting operative family set with `REQUIRED_CLAUSE_FAMILIES` to decide whether family completeness is present.

### Does operativity depend upon producer ownership, consumer admission, family coherence, explicit adapter testimony, or another repository-owned act?

Repository evidence supports this bounded answer:

```text
operativity depends on frontier-local coherence checks over preserved testimony
```

It does not depend on producer ownership or explicit adapter testimony in the current implementation. It does depend on the assembler's consumer-local act of consuming the preserved testimony and classifying operative clauses. Family coherence is required. The exact selected-need/testimony identity checks are also required for frontier establishment, but they are not ownership checks.

## Cross-examination

### Producer witness versus admission witness

The producer/ownership witness preserves the selected bounded clause as `unowned`. The admission witness does not repair that standing. The assembler can consume the preserved clause without consulting `ownership_basis`, but that is consumer-local reliance only.

Result:

```text
consumer admission
!= retroactive producer ownership
```

### Admission witness versus operativity witness

The admission witness supports consideration of preserved testimony. The operativity witness is stronger and narrower: only clauses satisfying `_is_operatively_coherent(...)` become operative. A visible or preserved unowned clause with `unsupported`, `unknown`, `mixed`, `adjacent_family`, `outside_current_scope`, or explicit conflict does not become operative merely by being present.

Result:

```text
admitted/preserved clause
!= operative clause
```

### Operativity witness versus frontier establishment

Operativity for one clause is not the whole frontier. Frontier establishment requires no material binding conflict and operative coverage for all four required families. Tests prove non-operative clauses can remain preserved while the frontier is established by other operative clauses. Therefore frontier establishment does not prove that every visible clause was operative.

Result:

```text
operative clause
!= frontier established

frontier established
!= every visible clause was operative
```

## Directional movement recovered

### Prior standing

```text
visible and preserved frontier-boundary clause testimony
with ownership_basis == "unowned"
```

### Responsible act

```text
bounded frontier assembler consumes preserved testimony
and applies frontier-local operative coherence checks
```

### Required evidence or warrant

For the first lawful movement out of unowned preserved testimony, repository evidence requires:

```text
selected inquiry need remains selected
selected-need/testimony identity is coherent
clause_standing == "established"
family_disposition == "inquiry"
evidence_currency is not "conflicting"
evidence_availability is not "conflicting"
if clause_family == "included_excluded_inquiry_scope":
  scope_disposition == "included"
```

For contribution to establishment, the frontier also requires operative coverage of all four required families and absence of material binding conflict. That later completeness check is not needed to characterize the first movement, except to keep operativity distinct from establishment.

### Direction of movement

```text
unowned preserved clause testimony
→ bounded consumer-local consideration/admission by assembler
→ frontier-local operative standing if coherence checks pass
```

The first movement is not from unowned to owned. It is from unowned preserved testimony into bounded consumer-local consideration by the frontier assembler. In the inspected implementation, if the clause also satisfies the assembler's coherence checks, that same consumer-owned process may classify it as operative without upstream ownership being resolved.

### Resulting standing

The resulting standing is:

```text
consumer-admitted preserved testimony,
and possibly frontier-local operative clause testimony
```

Only the latter applies when the clause satisfies `_is_operatively_coherent(...)`.

### Preserved prior history

The preserved prior history remains:

```text
ownership_basis == "unowned"
clause_ref remains in unowned_clause_refs
producer lineage remains absent
adapter lineage remains absent
```

The assembler's reliance does not revise those fields.

### Forbidden reverse inference

From consumer admission or frontier-local operativity, it is forbidden to infer:

- producer ownership;
- adapter ownership;
- valid caller ownership assertion;
- later ownership testimony;
- that unowned clauses are always operative;
- that all visible clauses contributed to frontier establishment;
- that frontier establishment proves every preserved clause was operative.

## Lawful asymmetries

The repository supports these bounded asymmetries:

1. A clause can be preserved and visible while remaining unowned.
2. Producer/adapter ownership requires lineage; payload assertion is insufficient.
3. The frontier assembler can consume preserved testimony without first upgrading ownership.
4. Frontier-local operativity is decided by local coherence dimensions, not by `ownership_basis`.
5. Operativity can be established while upstream ownership remains unresolved.
6. Non-operative preserved clauses can coexist with an established frontier when other clauses supply required operative family coverage.
7. Explicit clause conflicts block establishment, but lack of ownership is not implemented as an establishment-blocking conflict.

## Possibility selection

The maximum movement warranted by repository evidence is closest to possibility B:

```text
B.
unowned testimony
→ bounded consumer-local admission
→ operative standing may later be established
while upstream ownership remains unresolved
```

A small correction is necessary: in the inspected implementation, consumer-local consideration and frontier-local operativity may occur in the same assembler act. The movement is still directional and asymmetric because the assembler's local operative classification does not repair upstream ownership.

## Remaining Unknowns

- Whether a later producer or adapter ownership testimony can attach to an already preserved unowned clause without rewriting it remains Unknown.
- Whether a new attributed successor artifact is the lawful way to represent later ownership remains Unknown.
- Whether ownership conflict has a dedicated standing outside clause standing, scope disposition, evidence currency, or evidence availability remains Unknown.
- Whether constitutional grammar outside the inspected inquiry frontier road would require ownership as a precondition for operativity remains Unknown.
- Whether stale or unavailable but otherwise established testimony should always remain operative for required-family establishment remains Unknown in adjacent audit evidence; this investigation does not rely on that stronger claim.

## Bounded conclusion

What is the first repository-supported constitutional movement available from unowned frontier-boundary clause testimony?

```text
Unowned preserved frontier-boundary clause testimony may first move into bounded consumer-local consideration by the bounded frontier assembler. If, and only if, the preserved clause independently satisfies the assembler's frontier-local coherence checks, it may receive frontier-local operative standing while its upstream producer or adapter ownership remains unresolved and preserved as unowned.
```
