# Frontier boundary clause operativity coordinate provenance audit 001

## Boundary of this investigation

This is a bounded, read-only recovery of the upstream standing establishment consumed by frontier-local operativity at the handoff:

```text
FrontierBoundaryClauseInput
→ InquiryFrontierBoundaryClause
→ BoundedInquiryFrontier operative relation
```

It does not design or recommend an admission layer, clause lifecycle, ownership registry, standing engine, or universal frontier architecture. It treats absence of an explicit producer as unresolved provenance rather than as a defect.

The governing correction is preserved:

```text
ownership_basis != frontier-local operativity
consumer-local evaluation != admission unless separately established
operative_clause_refs != intrinsic operativity added to the clause
```

The assembler consumes preserved testimony, evaluates local coherence, and projects operative or non-operative clause references in a downstream frontier artifact. It does not perform a separate admission act, repair upstream standing, establish clause ownership, or mutate preserved clauses.

## Witnesses inspected

Implementation witnesses:

- `seed_runtime/inquiry_frontier_boundary_testimony.py`
- `seed_runtime/bounded_inquiry_frontier.py`
- `tests/test_inquiry_frontier_boundary_testimony.py`
- `tests/test_bounded_inquiry_frontier.py`

Repository-audit witnesses used only as already-preserved interpretive context:

- `book_of_seed/uptake_standing_characterization_pass_006.md`
- `evidence_frontier_topology_survey_001.md`
- `inquiry_frontier_boundary_testimony_asymmetry_recovery_001.md`

## Shared implementation road

`FrontierBoundaryClauseInput` declares the five operative coordinates as caller-supplied fields with defaults:

```text
clause_standing = unclassified
scope_disposition = not_applicable
evidence_currency = unknown
evidence_availability = unknown
family_disposition = unclassified
```

`preserve_inquiry_frontier_boundary_testimony(...)` copies those values into `InquiryFrontierBoundaryClause` without re-deriving them. It separately assigns `ownership_basis` from the presence of producer lineage or adapter lineage. If neither is present, the preserved clause remains `unowned`.

`assemble_bounded_inquiry_frontier(...)` then treats a clause as operative when:

```text
clause_standing == established
family_disposition == inquiry
evidence_currency != conflicting
evidence_availability != conflicting
and, for included_excluded_inquiry_scope clauses only,
scope_disposition == included
```

It projects operative clause references, non-operative clause references, explicit conflict references, and dimension-specific reference lists into `BoundedInquiryFrontier`. It does not write back into `InquiryFrontierBoundaryClause`.

## Coordinate 1: clause standing

### Value set recovered

```text
established
unsupported
unknown
conflicting
unclassified
```

### Prior material or standing

The implementation-visible prior material is explicit clause payload supplied as `FrontierBoundaryClauseInput.clause_standing`. A clause may also carry `producer_ref` plus `producer_lineage`, `adapter_ref` plus `adapter_lineage`, source lineage, evidence classes, provenance roles, and evidence refs, but those fields do not cause the preservation function to verify or derive the standing value.

### Responsible producer or adapter act

The immediate implementation producer of the coordinate value is the caller or stage that constructs `FrontierBoundaryClauseInput`. A stronger producer is recognized only as attributed lineage when `producer_ref` and `producer_lineage` are present. An adapter is recognized only as attributed lineage when `adapter_ref` and `adapter_lineage` are present and producer lineage is absent.

The preservation owner classifies ownership basis from lineage-field presence. It does not prove that the named producer or adapter actually occurred.

### Required evidence or warrant

The implementation requires no independent evidence for `established`, `unsupported`, `unknown`, `conflicting`, or `unclassified` beyond the supplied enum value. Tests show payload flags cannot assert ownership without producer or adapter lineage, but they do not show that the clause-standing value itself is independently verified.

Thus the exact claim made by `established` at this layer is only:

```text
this preserved clause carries supplied testimony that its standing is established
```

If producer or adapter lineage is present, the claim is attributed to that producer or adapter lineage as preserved testimony. If not, it is unowned supplied testimony.

### Resulting coordinate testimony and preservation handoff

The preservation handoff copies `clause_standing` unchanged into `InquiryFrontierBoundaryClause`. It adds selected-need identity bindings and ownership-basis classification, but it does not add factual standing to the clause-standing claim.

### Frontier-local evaluation

The assembler inspects `clause_standing`. `established` is required for operative coherence. `unsupported`, `unknown`, and `unclassified` are preserved as non-operative when they fail that predicate. `conflicting` is both preserved and treated as a material binding conflict.

### Lawful asymmetry

A clause can be projected into `operative_clause_refs` only by satisfying the assembler predicate, but this projection does not prove the clause's producer standing or convert upstream unowned testimony into owned standing.

### Unsupported promotions

- `frontier_state="established"` does not prove that a clause-standing producer occurred.
- `clause_standing="established"` does not prove ownership.
- Later operativity must not be reverse-inferred into upstream clause truth.

### Outcome

C. Caller supplies explicit testimony; preservation owner preserves it as testimony; assembler lawfully evaluates it without stronger claims.

## Coordinate 2: family disposition

### Value set recovered

```text
inquiry
adjacent_family
mixed
unclassified
```

### Prior material or standing

The implementation-visible prior material is explicit `FrontierBoundaryClauseInput.family_disposition`. This is separate from `clause_family`, whose value identifies one of the four boundary clause families required by the frontier assembler.

### Responsible producer or adapter act

The immediate implementation producer is the caller or stage constructing `FrontierBoundaryClauseInput`. Producer or adapter lineage can be preserved, but no function derives family disposition from wording similarity, family labels, source lineage, or inquiry-need membership.

### Required evidence or warrant

No inspected implementation requires semantic or lexical evidence to classify a clause as `inquiry`, `adjacent_family`, `mixed`, or `unclassified`. The warrant is explicit supplied testimony, optionally attributed by producer or adapter lineage.

This prevents wording similarity from manufacturing family standing at the observed layer because no wording-similarity rule is implemented. It also means the implementation does not independently prove inquiry-family membership for the clause.

### Resulting coordinate testimony and preservation handoff

`family_disposition` is copied unchanged into `InquiryFrontierBoundaryClause` together with selected-need identity and ownership-basis fields.

### Frontier-local evaluation

The assembler requires `family_disposition == "inquiry"` for operative coherence. `mixed` and `adjacent_family` are collected in their own reference lists and, because they fail the operative predicate, appear as non-operative when otherwise preserved. `unclassified` also fails operative coherence, although it has no dedicated reference list except through `non_operative_clause_refs`.

### Lawful asymmetry

The assembler may require inquiry-family disposition for its own operative relation without proving that a stage-owned family classifier existed. `clause_family` names the kind of boundary clause; `family_disposition` remains the supplied relation of that clause to the inquiry family.

### Unsupported promotions

- `clause_family` must not be equated with established family disposition.
- `family_disposition="inquiry"` must not be inferred from later operative projection.
- Wording similarity must not be treated as family standing.

### Outcome

C. Caller supplies explicit testimony; preservation owner preserves it as testimony; assembler lawfully evaluates it without stronger claims.

## Coordinate 3: scope disposition

### Value set recovered

```text
included
excluded
outside_current_scope
conflicting
not_applicable
```

### Prior material or standing

The implementation-visible prior material is explicit `FrontierBoundaryClauseInput.scope_disposition`. The bounded scope being evaluated by the assembler is the frontier boundary for one exact selected inquiry need and matching boundary testimony, not automatically the goal horizon or a universal inquiry scope.

### Responsible producer or adapter act

The immediate implementation producer is the caller or stage constructing the clause input. Producer or adapter lineage can attribute the supplied scope relation, but preservation does not independently verify who owns the bounded scope or what prior act placed the clause inside or outside it.

### Required evidence or warrant

The preservation function requires a selected inquiry need before it preserves selected-path testimony, and the assembler requires identity agreement between selected need and testimony. Those checks bind the testimony to a selected inquiry need. They do not derive the scope disposition value.

The only implementation warrant for `included`, `excluded`, `outside_current_scope`, `conflicting`, or `not_applicable` is supplied coordinate testimony, optionally attributed by lineage.

### Resulting coordinate testimony and preservation handoff

`scope_disposition` is copied unchanged into `InquiryFrontierBoundaryClause`. Preservation also records selected-reference id, native projection id, native lineage, need set, selected-goal id, horizon id, uncertainty component, and repository/world subject refs.

### Frontier-local evaluation

The assembler inspects `scope_disposition` in two ways:

1. Any `scope_disposition == "conflicting"` becomes a material binding conflict.
2. For `included_excluded_inquiry_scope` clauses, operative coherence requires `scope_disposition == "included"`.

For non-scope clause families, `_is_operatively_coherent(...)` does not require included scope after the general conflict check. `outside_current_scope` is collected in `out_of_scope_clause_refs` and fails operativity when it is on the required scope-family clause because the scope-family special rule requires `included`.

### Lawful asymmetry

The assembler consumes an already-preserved scope relation for local coherence. It does not establish the bounded inquiry scope itself, does not invent scope, and does not make goal-horizon scope automatically equal inquiry scope.

### Unsupported promotions

- Goal-horizon scope must not be treated as inquiry scope automatically.
- A copied `included` value must not be promoted to proof that a scope owner performed the placement act.
- Frontier-local operativity must not be reverse-inferred into intrinsic scope inclusion.

### Outcome

C. Caller supplies explicit testimony; preservation owner preserves it as testimony; assembler lawfully evaluates it without stronger claims.

## Coordinate 4: evidence currency

### Value set recovered

```text
current
stale
unknown
conflicting
```

### Prior material or standing

The implementation-visible prior material is explicit `FrontierBoundaryClauseInput.evidence_currency`. Prior repository context distinguishes freshness/currency from availability, standing, sufficiency, stopping, and admission, but the current handoff does not independently calculate currentness relative to a clock, question, frontier, or reliance purpose.

### Responsible producer or adapter act

The immediate implementation producer is the caller or stage constructing the clause input. If producer or adapter lineage is present, preservation attributes the clause to that lineage. No inspected owner performs a temporal probe or freshness calculation at preservation or assembly time.

### Required evidence or warrant

No implementation evidence establishes a currentness warrant beyond the supplied coordinate. Therefore `current` is not a timeless property. At this handoff it means only that the clause carries supplied testimony of currency for the bounded act represented by the clause producer or caller.

### Resulting coordinate testimony and preservation handoff

`evidence_currency` is copied unchanged into `InquiryFrontierBoundaryClause`. Preservation adds identity binding to the selected inquiry need but does not refresh, verify, or timestamp the currency claim.

### Frontier-local evaluation

The assembler refuses `evidence_currency == "conflicting"` as a material binding conflict and excludes conflicting currency from operative coherence. It also records `stale_clause_refs`. It does not treat `stale` as automatically non-operative in the current implementation; stale clauses can still satisfy the operative predicate if other required coordinates pass.

### Lawful asymmetry

The assembler can use non-conflicting currency as a local coherence condition without establishing that the evidence remains current for all future frontiers or all reliance purposes.

### Unsupported promotions

- `current` must not be treated as indefinite currentness.
- Preserved currency testimony must not be promoted into refresh, access, sufficiency, or source-selection standing.
- Later frontier assembly must not be treated as an independent temporal currency judgment.

### Outcome

C, with a repository-noted Unknown about stale/unavailable operative strength. Caller supplies explicit currency testimony and preservation carries it; the assembler consumes it as a local conflict/non-conflict coordinate. The stronger rule that stale required-family testimony fully establishes required-family operativity remains not independently established by inspected grammar.

## Coordinate 5: evidence availability

### Value set recovered

```text
available
unavailable
unknown
conflicting
```

### Prior material or standing

The implementation-visible prior material is explicit `FrontierBoundaryClauseInput.evidence_availability`. Prior repository context distinguishes availability from applicability, admission, consumption, access authorization, source selection, observation selection, and execution.

### Responsible producer or adapter act

The immediate implementation producer is the caller or stage constructing the clause input. Producer or adapter lineage can be preserved as attribution, but neither preservation nor assembly independently probes reachability, access authority, admissibility, or consumability.

### Required evidence or warrant

No implementation evidence requires more than the supplied enum value. Therefore availability at this handoff means bounded clause testimony of availability to the producing/calling stage for its stated frontier-boundary purpose, not universal visibility, reachability, admissibility, or later consumption.

### Resulting coordinate testimony and preservation handoff

`evidence_availability` is copied unchanged into `InquiryFrontierBoundaryClause`. Already visible evidence refs and eligible evidence territory refs remain separate; visible evidence is not automatically eligible evidence territory.

### Frontier-local evaluation

The assembler refuses `evidence_availability == "conflicting"` as a material binding conflict and excludes conflicting availability from operative coherence. It records `unavailable_clause_refs`. It does not treat `unavailable` as automatically non-operative in the current implementation; unavailable clauses can still satisfy the operative predicate if other required coordinates pass.

### Lawful asymmetry

The assembler may consume availability as a local conflict/non-conflict coordinate without admitting evidence, selecting a source, authorizing access, or proving availability to a downstream executor.

### Unsupported promotions

- `available != applicable`.
- `applicable != admitted`.
- `admitted != consumed`.
- Preserved availability must not be reverse-inferred from operative projection.

### Outcome

C, with the same repository-noted Unknown about unavailable required-family operative strength. Caller supplies explicit availability testimony and preservation carries it; the assembler consumes it as a local conflict/non-conflict coordinate. The stronger rule that unavailable required-family testimony fully establishes required-family operativity remains not independently established by inspected grammar.

## Producer witness, consumer witness, and fidelity test

| Coordinate | Constitutional grammar | Directional expectation | Producer witness | Consumer witness | Result |
| --- | --- | --- | --- | --- | --- |
| `clause_standing` | Standing should come from a responsible producer, adapter, or bounded testimony; operativity must not imply ownership. | Preserve supplied standing and attribution; consume only within frontier-local predicate. | Caller/stage supplies value; producer/adapter lineage may attribute it; no occurrence proof. | Requires `established`; records unsupported/unknown/conflicting refs; conflict blocks. | Faithful handoff as C; no unsupported promotion if described as testimony. |
| `family_disposition` | Inquiry-family relation must not be manufactured by wording similarity or clause labels. | Preserve family-disposition testimony separately from `clause_family`; consume inquiry relation locally. | Caller/stage supplies value; lineage optional. | Requires `inquiry`; records mixed/adjacent refs. | Faithful handoff as C. |
| `scope_disposition` | Bounded inquiry scope is not automatically goal-horizon scope. | Preserve supplied scope relation for exact selected need; consume included/conflict locally. | Caller/stage supplies value; selected need binds testimony context but does not derive scope. | Scope-family operativity requires `included`; any conflicting scope blocks. | Faithful handoff as C. |
| `evidence_currency` | Currency is relative to time/purpose and is separate from availability and sufficiency. | Preserve supplied temporal testimony; consume conflict/non-conflict locally. | Caller/stage supplies value; no freshness probe found. | Conflicting blocks; stale refs are preserved; stale is not currently disqualifying. | C plus Unknown on stale operative strength. |
| `evidence_availability` | Availability is distinct from applicability, admission, consumption, and access authority. | Preserve supplied availability testimony; consume conflict/non-conflict locally. | Caller/stage supplies value; no reachability/access probe found. | Conflicting blocks; unavailable refs are preserved; unavailable is not currently disqualifying. | C plus Unknown on unavailable operative strength. |

No Fidelity frontier is established merely because the transition is compressed, because callers supply fields, because no dedicated producer class exists, or because the assembler trusts preserved testimony. A fidelity frontier would require constitutional grammar demanding a prior standing movement that the current witness fails to preserve. For these coordinates, the current witness preserves the supplied coordinate testimony and does not claim a stronger producer occurrence. The remaining Unknowns concern whether stale or unavailable testimony may supply required-family operativity, not whether the coordinates have hidden producer standing.

## Maximum warranted statement for the exact handoff

### What moves each operative coordinate into existence?

At this handoff, each coordinate first appears as explicit `FrontierBoundaryClauseInput` testimony supplied by the caller or upstream stage. Producer or adapter lineage, when present, attributes the clause to a recognized producer or adapter basis, but the implementation does not prove producer occurrence or derive the coordinate from upstream material.

### What standing does preservation add?

Preservation adds a read-only `InquiryFrontierBoundaryClause` bound to one exact selected inquiry need when the selected path is available. It copies the coordinates unchanged, preserves lineage and evidence refs, and classifies `ownership_basis` from producer or adapter lineage-field presence. It does not add clause truth, ownership, admission, scope establishment, family establishment, temporal currentness, availability verification, or operative standing.

### What standing does frontier evaluation add?

Frontier evaluation adds only consumer-local operative relation and frontier-state judgment: selected inquiry gate and identity binding passed, explicit material conflicts were absent, and operative clause references covered the required frontier families. It projects `operative_clause_refs` in the downstream `BoundedInquiryFrontier` artifact. It does not mutate the preserved clause or create intrinsic clause operativity.

### What remains merely attributed testimony?

The five coordinates remain attributed or unowned testimony according to their preserved producer/adapter lineage and ownership basis:

```text
clause_standing
family_disposition
scope_disposition
evidence_currency
evidence_availability
```

### Which prior standings survive unchanged?

Selected-need identity fields, native lineage, source testimony ref, uncertainty component ref, repository/world subject ref, clause refs, clause text, clause family, source lineage, evidence classes, provenance roles, visible evidence refs, eligible evidence territory refs, producer and adapter refs, and the five operative coordinates survive as copied testimony. Ownership basis survives as preservation-local classification from lineage-field presence.

### Which reverse inferences are forbidden?

- `operative_clause_refs` must not be read back as intrinsic operativity on `InquiryFrontierBoundaryClause`.
- `frontier_state="established"` must not be read back as clause ownership, producer occurrence, or verified upstream standing.
- `ownership_basis` must not be inferred from frontier-local operativity.
- `clause_family` must not be read as established `family_disposition`.
- Goal-horizon scope must not be read as inquiry scope automatically.
- Evidence availability must not be read as applicability, admission, source selection, observation selection, access authorization, execution readiness, or consumption.
- Evidence currency must not be read as timeless currentness.

## Remaining Unknowns

- Whether any upstream, stage-owned producer outside the inspected implementation currently establishes these coordinates before constructing `FrontierBoundaryClauseInput` remains Unknown.
- Whether adapter-produced coordinates have repository-enforced translation limits beyond preserved `adapter_ref` and `adapter_lineage` remains Unknown.
- Whether `stale` but otherwise established testimony should count as operative required-family support remains Unknown.
- Whether `unavailable` but otherwise established testimony should count as operative required-family support remains Unknown.
- Whether `current` and `available` are intended to be relative to the selected need, the frontier assembly time, a producer observation time, or a later reliance purpose remains unresolved by the implementation.

## Bounded answer

> What is the earliest repository-supported constitutional movement that establishes the coordinates later consumed by frontier-local operativity?

The earliest repository-supported movement for this exact handoff is explicit caller-or-stage testimony in `FrontierBoundaryClauseInput`, optionally attributed by producer or adapter lineage and then preserved unchanged in `InquiryFrontierBoundaryClause`; preservation adds selected-need binding and ownership-basis classification but not coordinate truth, and `BoundedInquiryFrontier` adds only a downstream, frontier-relative operative relation from those preserved coordinates. No stronger producer establishment is currently warranted by the inspected repository evidence.
