# Eligible Evidence Territory Reference Warrant Provenance Audit 001

## Bounded target

Exact family assertion investigated: `eligible_ineligible_evidence_territory`.

Bounded consumer question: what standing does one non-empty `eligible_evidence_territory_refs` value carry before this exact family contributes positive support toward required-family frontier establishment?

This is a read-only investigation of current repository behavior. It does not propose an implementation, add a predicate, design a registry, or continue into the other three required frontier families.

## Repository witnesses used

- `FrontierBoundaryClauseInput` exposes caller-supplied producer, adapter, source/provenance, visible-evidence, eligible-territory, standing, currency, availability, and family-disposition fields. It does not define a territory registry, territory object, evidence-territory admission relation, or inquiry-specific eligibility proof.
- `preserve_inquiry_frontier_boundary_testimony(...)` preserves clauses for one selected inquiry need and copies the eligible territory refs and other caller-supplied testimony into immutable boundary testimony.
- `assemble_bounded_inquiry_frontier(...)` consumes preserved testimony and mechanically recognizes a non-empty `eligible_evidence_territory_refs` tuple as the family-local positive condition for `eligible_ineligible_evidence_territory`, after checking only selected-testimony identity at the testimony level, standing/family-disposition conflicts, explicit `conflicting` currency/availability, and family-specific scope/territory tuple presence.
- Existing tests prove the PR 1856 distinction: family label and positive coordinates with empty territory refs remain preserved but non-operative.
- A focused read-only probe, run without changing tests, characterized unavailable, unknown, stale, unknown-currency, no-source, and empty-ref cases.

## 1. Territory producer witness

### Upstream reference traced

The directly recoverable upstream territory reference is the test-supplied value `("territory:repo-world",)` in `_required_clauses()` for the `eligible_ineligible_evidence_territory` clause.

### Who creates or selects the reference

The concrete repository witness creates the reference in the test helper `_required_clauses()`. The helper calls `_clause(...)` with `eligible_evidence_territory_refs=("territory:repo-world",)`. `_clause(...)` then constructs `FrontierBoundaryClauseInput` with default producer testimony naming `producer_ref="stage:frontier-boundary"`, producer lineage, source lineage, evidence classes, provenance roles, `clause_standing="established"`, `evidence_currency="current"`, `evidence_availability="available"`, and `family_disposition="inquiry"`.

The constructor of `FrontierBoundaryClauseInput` is therefore not treated as the constitutional producer. It is a payload shape. The only producer occurrence preserved by current evidence is the caller-supplied `producer_ref`/`producer_lineage` tuple, and in the test fixture that tuple names `stage:frontier-boundary`.

### What subject the reference identifies

The literal territory reference identifies only the string subject `territory:repo-world` in current code. No repository witness resolves that string to a territory entity, repository-world identity object, access state, temporal state, owner, or current frontier boundary object. The selected inquiry need itself binds to a native source-testimony/component/subject lineage, but the territory ref is not independently resolved against that lineage.

### What evidence supports its eligibility

Current evidence supports only attributed caller testimony:

- the family label is `eligible_ineligible_evidence_territory`;
- the tuple is non-empty;
- `_clause(...)` supplies `clause_standing="established"`, `family_disposition="inquiry"`, `evidence_currency="current"`, `evidence_availability="available"`, `source_lineage`, `evidence_classes`, and `provenance_roles`;
- preservation copies these fields;
- the consumer recognizes tuple non-emptiness for this family.

No upstream implementation evidence was found that derives territory eligibility from source material, validates the territory against an inquiry need, or proves the tuple's referent is actually eligible evidence territory.

### Inquiry need, component, subject, goal, and horizon binding

Preservation binds each preserved clause to the selected inquiry need's `reference_id`, `native_projection_id`, `native_lineage`, `need_set_id`, `selection_id`, `goal_establishment_id`, `horizon_id`, `source_testimony_ref`, bounded uncertainty component, and repository-world subject. This is clause-level binding created by preservation from the selected need. It is not a recovered proof that the territory ref itself belongs to that need, component, subject, goal, or horizon.

### Producer responsibility and limits

The preserved producer witness owns only stage-producer lineage when both `producer_ref` and `producer_lineage` are present. `_ownership(...)` classifies such a clause as `stage_producer_lineage`; it classifies adapter lineage separately; otherwise the clause is unowned. The test fixture proves payload ownership flags alone do not create ownership.

The producer/adaptor occurrence is preserved, but current code does not make the producer own eligibility, availability, or currency as a validated relation. Those dimensions remain copied clause testimony unless a consumer explicitly validates them.

## 2. Preservation witness

`preserve_inquiry_frontier_boundary_testimony(...)` does the following with the investigated fields:

| Dimension | Current preservation behavior |
| --- | --- |
| `eligible_evidence_territory_refs` | Copies `tuple(item.eligible_evidence_territory_refs)` into `InquiryFrontierBoundaryClause`. |
| `already_visible_evidence_refs` | Copies `tuple(item.already_visible_evidence_refs)` into each clause and separately preserves selected-need visible refs at testimony level. |
| `source_lineage` | Copies `tuple(item.source_lineage)`. |
| `evidence_classes` | Copies `tuple(item.evidence_classes)`. |
| `provenance_roles` | Copies `tuple(item.provenance_roles)`. |
| producer lineage | Copies `producer_ref` and `producer_lineage`; classifies `ownership_basis` as `stage_producer_lineage` only when both are non-empty. |
| adapter lineage | Copies `adapter_ref` and `adapter_lineage`; classifies `ownership_basis` as `adapter_lineage` only when no producer lineage exists and both adapter fields are non-empty. |
| currency | Copies `item.evidence_currency`. |
| availability | Copies `item.evidence_availability`. |

Preservation derives selected-need binding for the preserved clause artifact from the selected inquiry reference. Preservation does not derive, validate, or attribute an independent territory-eligibility relation. It mostly copies caller testimony, with a narrow preservation-local ownership-basis classification.

Preservation also explicitly remains read-only and non-operational: it does not assemble a frontier, formulate a question, open inquiry, authorize access, execute, start recording, write the event ledger, mutate cluster state, select sources, select observations, or judge collective sufficiency.

## 3. Frontier-consumer witness

### Validated before counting the family

`assemble_bounded_inquiry_frontier(...)` validates these things before determining required-family coverage:

1. Selection/testimony identity at the testimony level: selected state, selected reference existence, and agreement among selected-need reference id, native projection, native lineage, need set, selection id, goal id, and horizon id.
2. Clause operativity through `_is_operatively_coherent(...)`:
   - `clause_standing == "established"`;
   - `family_disposition == "inquiry"`;
   - currency and availability are not `"conflicting"`;
   - included-scope clauses have `scope_disposition == "included"`;
   - `eligible_ineligible_evidence_territory` clauses have `bool(clause.eligible_evidence_territory_refs)`.
3. Required-family coverage by set membership of operative clause families.
4. Material conflict if selected/testimony identity conflicts or if any clause has `clause_standing`, `scope_disposition`, `evidence_currency`, or `evidence_availability` equal to `"conflicting"`.

### Absent consumer checks

Current consumer code does not verify that:

- a territory ref belongs to the selected inquiry need;
- a territory ref is bound to the same component and subject;
- a territory ref is supported by preserved source evidence;
- a territory is currently available;
- a territory is current for this assembly;
- a territory is eligible rather than merely visible;
- a territory is within the frontier boundary;
- a territory is sufficient for this family assertion beyond tuple non-emptiness and the copied positive clause coordinates;
- `already_visible_evidence_refs` can substitute for `eligible_evidence_territory_refs`.

These are recorded as absent checks, not automatic defects.

## Directional recovery

Maximum repository-supported movement currently recovered:

```text
caller/stage-supplied boundary-clause testimony
→ copied producer or adapter lineage ownership basis for the clause artifact
→ preservation-level binding of the clause artifact to selected inquiry need/native lineage/goal/horizon
→ copied currency and availability testimony
→ copied source/provenance testimony
→ consumer-local checks for established standing, inquiry family disposition, non-conflicting currency/availability, and non-empty eligible territory refs
→ positive required-family support for eligible_ineligible_evidence_territory
```

Unsupported movement begins when the non-empty territory tuple is treated as establishing any of these independent relations: territory identity, actual eligible territory, selected-need-specific territory relation, current availability, current currency, admitted evidence, or warranted reliance beyond family-local tuple presence.

## Special discriminating cases

A focused read-only probe constructed the four required clauses and varied only the evidence-territory clause.

| Case | Current result | Classification |
| --- | --- | --- |
| non-empty ref + available + current | `frontier_state=established`; evidence clause operative | Family-local positive support when all copied positive coordinates are present. |
| non-empty ref + unavailable | `frontier_state=established`; evidence clause operative; `unavailable_clause_refs` records the clause | Unsupported promotion if read as available/current eligible territory; lawful but non-establishing testimony if read only as preserved unavailable testimony; current consumer still gives family-local positive support. |
| non-empty ref + unknown availability | `frontier_state=established`; evidence clause operative | Family-local positive support despite unknown availability; no availability establishment. |
| non-empty ref + stale | `frontier_state=established`; evidence clause operative; `stale_clause_refs` records the clause | Family-local positive support despite stale currency; no current-territory establishment. |
| non-empty ref + unknown currency | `frontier_state=established`; evidence clause operative | Family-local positive support despite unknown currency; no current-territory establishment. |
| non-empty ref + `conflicting` availability | `frontier_state=material_binding_conflict`; evidence clause non-operative; family missing | Consumer-locally blocked by explicit conflict. |
| non-empty ref unrelated to selected need | Unknown from direct repository evidence; no field-level relation exists for the consumer to check | Insufficient. The consumer validates testimony-level selected-need identity, not per-territory selected-need relation. |
| visible evidence refs without eligible territory refs | Preserved but non-operative for this family | Existing tests prove visible refs and positive coordinates do not repair empty eligible territory refs. |
| eligible territory refs without source lineage/evidence basis | `frontier_state=established`; evidence clause operative in focused probe | Mechanical recognition; source/provenance support is not required by the consumer. |
| empty refs with otherwise positive coordinates | `frontier_state=missing_required_clause_family`; clause preserved non-operative | PR 1856 distinction preserved. |

## Warrant dimensions

| Dimension | Standing | Basis |
| --- | --- | --- |
| reference identity | Mechanically recognized | A string tuple is copied and `bool(...)` is checked; no referent resolution. |
| territory eligibility | Preserved attributed testimony / insufficient | Family label plus tuple and standing are preserved; no independent eligibility derivation or validation. |
| selected-need binding | Preserved attributed testimony for the clause artifact; insufficient for the territory ref itself | Preservation binds the clause to the selected need; consumer checks testimony-level identity, not territory-level relation. |
| component and subject binding | Preserved attributed testimony for the clause artifact; insufficient for the territory ref itself | Clause receives selected native lineage/component/subject; tuple is not resolved against them. |
| frontier-boundary binding | Mechanically recognized / insufficient | Consumer treats non-empty tuple as within this family's operative condition; no boundary containment check. |
| source and provenance support | Preserved unowned or attributed testimony depending on producer/adapter fields; insufficient as validation | Source lineage, evidence classes, and provenance roles are copied and can be absent while the consumer still counts the family. |
| currency | Preserved unowned testimony; consumer-locally blocks only `conflicting` | `stale` and `unknown` are recorded but still operative in current consumer behavior. |
| availability | Preserved unowned testimony; consumer-locally blocks only `conflicting` | `unavailable` and `unknown` are recorded but still operative in current consumer behavior. |
| conflict handling | Consumer-locally validated for explicit `conflicting` values | Explicit conflict creates material binding conflict and prevents establishment. |
| consumer-local reliance purpose | Mechanically recognized | Reliance is limited to required-family coverage for `eligible_ineligible_evidence_territory`, not evidence admission, source selection, observation selection, inquiry execution, or result knowledge. |

## Lawful asymmetries

- Visible evidence and eligible evidence territory are intentionally separate. `already_visible_evidence_refs` can be preserved without making the family operative.
- Empty eligible territory refs with otherwise positive coordinates are preserved but non-operative.
- Explicit `conflicting` currency or availability is materially blocking.
- `stale`, `unavailable`, and `unknown` are not materially blocking in current consumer logic even though they are recorded in the frontier output.
- Producer/adapter lineage can provide clause-artifact ownership basis without proving territory eligibility, availability, or currency.

## Book fidelity test

Book claim-relative warrant expectation plus the recovered producer, preservation, and consumer witnesses yields a mixed implementation crossing.

Faithful relation:

- The implementation faithfully preserves the distinction between visible evidence refs and eligible territory refs.
- It faithfully prevents family-label-only or positive-coordinate-only clauses with empty eligible territory refs from contributing operative coverage.
- It faithfully preserves explicit unavailable/stale markers in output fields rather than erasing them.
- It faithfully blocks explicit `conflicting` currency/availability.

Implementation crossing:

- A non-empty `eligible_evidence_territory_refs` tuple can contribute positive family support even when availability is `unavailable` or `unknown`.
- A non-empty tuple can contribute positive family support even when currency is `stale` or `unknown`.
- A non-empty tuple can contribute positive family support without source lineage, evidence classes, or provenance roles.
- A non-empty tuple can contribute positive family support without consumer validation that the territory belongs to the selected need, component, subject, or frontier boundary.

Unknown:

- Whether any upstream, non-test stage exists that independently establishes claim-relative eligible-territory warrant before constructing these inputs.
- Whether different future territory refs are intended to carry different standings.
- Whether the current family-local positive support is an intentional limited reliance on caller testimony or an accidental promotion from tuple presence.

## First unsupported movement

The first unsupported movement is:

```text
preserved non-empty territory reference
→ repository-supported claim-relative eligible territory warrant
```

The implementation-supported movement is narrower:

```text
preserved non-empty territory reference
→ consumer-local positive support for this family, provided clause_standing is established, family_disposition is inquiry, and currency/availability are not explicitly conflicting
```

That narrower movement is real current behavior. It is not, by itself, evidence-territory identity establishment, availability establishment, currency establishment, selected-need applicability, source admission, or frontier-wide warrant.

## Remaining Unknowns

- No direct repository witness was found for a territory producer that validates `territory:repo-world` as eligible for a particular inquiry need.
- No direct repository witness was found for a territory ownership layer or provenance relation that makes the tuple sufficient as evidence basis.
- No direct repository witness was found for a consumer check that ties individual territory refs to selected need, component, subject, goal, horizon, boundary, availability, or currency.
- No direct repository witness was found distinguishing different territory-reference classes or standings.

## Bounded answer

What standing does a non-empty `eligible_evidence_territory_refs` value actually carry, and what additional claim-relative movement—if any—is required before it may contribute positive support toward required-family frontier establishment?

A non-empty `eligible_evidence_territory_refs` value currently carries mechanically recognized, preserved caller/stage testimony that a territory reference was supplied for the `eligible_ineligible_evidence_territory` family. In the current consumer, that non-empty tuple is sufficient for family-local positive support when the clause also has `clause_standing="established"`, `family_disposition="inquiry"`, and no explicitly `conflicting` currency or availability. It does not independently establish territory identity, eligibility for the selected inquiry need, component/subject/frontier binding, source or provenance support, currentness, availability, admissibility, or whole-frontier warrant. Additional claim-relative movement would be required for those stronger readings: producer-supported or otherwise validated territory eligibility, selected-need/component/subject/frontier binding, source/provenance basis, and availability/currency standing. Current implementation does not require that additional movement before counting the family locally; therefore the bounded outcome is mixed, primarily **D** for mechanically supplied references that the consumer treats as sufficient family-local warrant, with **B** only if the result is read narrowly as limited attributed boundary testimony rather than established eligible-territory warrant.
