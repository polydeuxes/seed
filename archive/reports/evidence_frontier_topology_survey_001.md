# Evidence Frontier Topology Survey 001

## Scope

This is a bounded, report-only topology survey of the constitutional area around:

```text
selected inquiry need
→ frontier-boundary testimony
→ bounded inquiry frontier
→ downstream inquiry movement
```

It uses the Book as constitutional grammar and implementation/tests as witness. It does not amend the Book, modify implementation, invent a wrapper, declare a fidelity crossing merely because ownership is unclear, collapse the area into the unavailable-only clause case, or expand into complete self-orientation or execution topology.

## Local constitutional graph

Legend:

- **Observed edge**: implementation or focused test directly shows the producer-consumer relation.
- **Book-warranted correspondence**: Book/prior constitutional reports provide grammar for the relation, but not necessarily live implementation ownership.
- **Implementation-local behavior**: live code behavior, possibly narrower than the constitutional grammar.
- **Inferred candidate edge**: plausible next responsibility supported by adjacent evidence but not implemented.
- **Unknown**: not recovered from repository evidence.

```text
RepositoryWorldUncertaintyTestimony / InquiryNeedProjection
→ inquiry need standing + evidence freshness/availability testimony
→ AdvancementNeedConsiderationSelection
→ selected inquiry need
→ InquiryFrontierBoundaryTestimony
→ preserved clause-level territory/currency/availability/scope/sufficiency/stop testimony
→ BoundedInquiryFrontier
→ established/refused frontier + preserved unavailable/stale/unknown/conflicting/non-operative refs
→ FrontierQuestionFormulationTestimony (missing / inferred candidate)
→ BoundedConstitutionalQuestion
→ downstream execution eligibility checks (partly outside this survey; executable operation remains separate ToolRegistry/ToolExecutor authority)
```

A narrower implementation-local graph is visible today:

```text
FrontierBoundaryClauseInput
→ InquiryFrontierBoundaryClause.evidence_availability
→ InquiryFrontierBoundaryTestimony.clauses
→ assemble_bounded_inquiry_frontier(...)
→ BoundedInquiryFrontier.unavailable_clause_refs / material_conflict_clause_refs / operative_clause_refs
```

## Recovered responsibilities and artifacts

| Responsibility | Producer | Artifact or testimony produced | Constitutional purpose | Standing entering | Standing established | Immediate consumer | Negative authority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Native inquiry-need projection | `InquiryNeedProjection` and its source `RepositoryWorldUncertaintyTestimony` in prior recovery | Native inquiry item with uncertainty component, repository/world subject, evidence ref, freshness, availability, materiality | Establish that a repository/world uncertainty is a horizon-material inquiry need without opening inquiry | Explicit component-bounded testimony | Inquiry-need item standing plus separated evidence freshness/availability | `AdvancementNeedConsiderationSelection`, later boundary testimony as cited provenance | Does not open inquiry, select a question, authorize observation, judge sufficiency, execute, record, write ledger, or mutate state |
| Exact selected inquiry need | `AdvancementNeedConsiderationSelection` | One selected advancement-need reference | Bind the frontier area to one exact visible inquiry need, not family order or wording | Need reference set + explicit focus evidence | `selection_state="selected"` for one inquiry-family reference, or refused selection | `preserve_inquiry_frontier_boundary_testimony(...)` and `assemble_bounded_inquiry_frontier(...)` | Does not create scope, evidence territory, sufficiency, stop conditions, authority, execution, or blocking standing |
| Frontier-boundary clause preservation | `preserve_inquiry_frontier_boundary_testimony(...)` consuming explicit `FrontierBoundaryClauseInput` | `InquiryFrontierBoundaryTestimony` and `InquiryFrontierBoundaryClause` records | Preserve unordered, stage-owned boundary clauses for one exact selected inquiry need | Selected inquiry need plus caller/stage-supplied clause fields | Clause-level family, standing, scope disposition, evidence currency, evidence availability, family disposition, lineage, ownership basis | `assemble_bounded_inquiry_frontier(...)` | Does not assemble frontier, formulate question, open inquiry, authorize access, execute, record, write ledger, mutate cluster, select sources, select observations, or judge collective sufficiency |
| Evidence availability testimony | Clause-producing stage or adapter before `FrontierBoundaryClauseInput`; implementation accepts supplied field | `evidence_availability` on each `InquiryFrontierBoundaryClause`: `available`, `unavailable`, `unknown`, or `conflicting` | Preserve whether the clause's evidence territory/testimony is presently available without collapsing into existence, reachability, access authority, blocking, stop, or sufficiency | Explicit clause payload with producer or adapter lineage where owned | Availability dimension on preserved testimony; unowned if no producer/adapter lineage | Boundary testimony and frontier assembler | The current preservation owner does not independently verify availability and does not authorize access or decide blocking |
| Evidence currency testimony | Same clause-producing stage or adapter before `FrontierBoundaryClauseInput` | `evidence_currency`: `current`, `stale`, `unknown`, or `conflicting` | Preserve currentness separately from availability and clause standing | Explicit clause payload | Currency dimension; stale refs surfaced by frontier | Boundary testimony and frontier assembler | Stale does not automatically mean stop, exclusion, refresh authorization, or non-establishment |
| Frontier establishment | `assemble_bounded_inquiry_frontier(...)` / `BoundedInquiryFrontier` | `BoundedInquiryFrontier` with `frontier_state`, operative refs, missing required families, conflicts, non-operative and preservation refs | Judge whether already-preserved clauses coherently establish a bounded inquiry frontier | Selected inquiry need + preserved boundary testimony | `established`, `missing_required_clause_family`, `material_binding_conflict`, or `not_selected_inquiry_need` | Future frontier-question formulation testimony; report/audit consumers | Does not invent scope, admit evidence, formulate question, open inquiry, select sources/observations, authorize access, execute, record, write ledger, mutate, or know result |
| Frontier-to-question formulation | No existing implemented owner; prior audit recovers a missing responsibility | Future formulation testimony plus existing `BoundedConstitutionalQuestion` | Convert one established frontier into one structurally equivalent bounded question without losing lineage | Established frontier plus explicit formulation testimony | Question artifact, if equivalence is proven; refusal otherwise | Constitutional pipeline / downstream inquiry surfaces | Must not broaden/narrow, select evidence, authorize observation, execute, record, write ledger, or mutate |
| Executable operation authority | Tool system, outside local frontier implementation | Registered `ToolSpec` operation executable through `ToolRegistry` and `ToolExecutor` | Distinguish conceptual need or question from callable operation | Separate registered operation and policy path | Executable operation eligibility, not established by frontier | Runtime tool execution path | Capability metadata, ToolNeed, ActionPlan, HandoffPlan, or frontier establishment is not executable authority |

## Evidence availability: producer and warrants

### Who produces `evidence_availability`?

Implementation-local answer: `InquiryFrontierBoundaryTestimony` preserves `evidence_availability`, but it does **not** originate or verify it. The immediate implementation producer is the caller/stage that creates `FrontierBoundaryClauseInput`; ownership is recognized only when the input carries `producer_ref` plus `producer_lineage`, or `adapter_ref` plus `adapter_lineage`. Otherwise the clause is preserved as `unowned`.

Book-warranted correspondence: prior boundary-testimony recovery says the native inquiry item may supply freshness and availability status, and that a lawful frontier-boundary clause requires explicit stage ownership, exact selected-need/native/subject/goal/horizon binding, and basis refs. Thus availability is best recovered as **imported clause-level testimony with ownership/provenance**, not as a judgment made by `BoundedInquiryFrontier`.

### What permits the producer to say available, unavailable, conflicting, or Unknown?

Observed implementation permits the values because `EvidenceAvailability` is a literal enum on `FrontierBoundaryClauseInput` and `InquiryFrontierBoundaryClause`. The preservation function copies the supplied value exactly. The frontier assembler reads that value only to reject `conflicting` as a material conflict, to require non-conflicting availability for operative coherence, and to collect `unavailable_clause_refs`.

Constitutionally, a producer may say:

- **available** when explicit stage-owned clause testimony says the evidence territory/testimony is available for this frontier boundary.
- **unavailable** when explicit stage-owned clause testimony says the territory/testimony is not presently available while preserving identity and nonexistence as a separate question.
- **conflicting** when availability testimony conflicts; the assembler treats this as a material binding conflict.
- **unknown** when the producer lacks enough owned testimony; the assembler preserves it as non-operative if it prevents operative coherence.

No reviewed implementation independently probes access, refreshes evidence, or proves reachability to derive these values.

### What kind of standing is availability?

Availability is not frontier-local establishment standing. It is not source selection, observation selection, access authorization, capability proof, or execution readiness. In the observed implementation it is a **clause-level evidence-condition dimension imported into frontier-boundary testimony**. In the frontier assembler it becomes a preservation/judgment input:

```text
available/unavailable/unknown/conflicting testimony
→ operative coherence or preserved non-operative/conflict/unavailable refs
```

Availability is adjacent to access/reachability, but not identical to either. `unavailable != nonexistent`, and `territory identified != evidence presently reachable` remain preserved distinctions.

## Producer-consumer edges

### Observed edges

```text
FrontierBoundaryClauseInput.evidence_availability
→ InquiryFrontierBoundaryClause.evidence_availability
→ BoundedInquiryFrontier.unavailable_clause_refs
```

```text
InquiryFrontierBoundaryClause.evidence_availability == "conflicting"
→ explicit_conflicts
→ material_conflict_clause_refs
→ frontier_state = "material_binding_conflict"
```

```text
InquiryFrontierBoundaryClause.evidence_availability == "unavailable"
+ clause_standing == "established"
+ family_disposition == "inquiry"
+ non-conflicting currency/availability
→ _is_operatively_coherent(...) can remain true
→ required family can contribute to frontier establishment
```

```text
InquiryFrontierBoundaryClause.evidence_currency == "stale"
→ BoundedInquiryFrontier.stale_clause_refs
```

```text
InquiryFrontierBoundaryClause.clause_standing == "unknown"
→ BoundedInquiryFrontier.unknown_clause_refs
→ non-operative if not operatively coherent
```

### Book-warranted correspondences

```text
native inquiry item / horizon / goal / observations / fact support
→ explicit stage-owned boundary clause testimony
→ frontier-boundary testimony
```

This correspondence is warranted only when exact binding, basis refs, and stage ownership are explicit. It is not automatic copying from horizon scope, evidence snapshots, or native subject.

```text
unavailable or stale testimony
→ possible lawful stopping condition
```

This is warranted only if a lawful-stopping clause says so. Stale or unavailable evidence does not automatically create a stop condition.

### Implementation-local behavior

`BoundedInquiryFrontier` constitutionally judges coherence of preserved clauses. It does not judge factual availability in the world. It preserves unavailable refs and treats conflicting availability as material conflict, but it does not transform unavailable into blocking, refresh, access need, observation need, or lawful inactivity.

### Inferred candidate edges

```text
established BoundedInquiryFrontier
→ frontier-question formulation testimony
→ BoundedConstitutionalQuestion
```

This edge is recovered as missing in prior audits. It is the strongest candidate immediate consumer path after frontier establishment, but it is not implemented.

```text
unavailable evidence territory
→ access need / observation need / refresh requirement / lawful stop
```

This is candidate-only unless a separate owner consumes the unavailable testimony and explicitly produces one of those standings.

### Unknowns

No observed owner consumes `unavailable_clause_refs` and produces a named `blocking_standing`, `access_need`, `observation_need`, `refresh_required`, `insufficiency`, `lawful_stopping`, or `lawful_inactivity` artifact.

## Standing transitions

| Entering standing | Responsibility | Established standing | Transition class | Notes |
| --- | --- | --- | --- | --- |
| Exact selected inquiry need absent or non-inquiry | `preserve_inquiry_frontier_boundary_testimony(...)` | Testimony with no selected inquiry binding and possible unowned refs | Observed | This does not create frontier territory. |
| Exact selected inquiry need + explicit owned clauses | `preserve_inquiry_frontier_boundary_testimony(...)` | Preserved boundary testimony | Observed | Preservation, not frontier establishment. |
| Clause availability `available` | `assemble_bounded_inquiry_frontier(...)` | May be operative if other coherence predicates pass | Observed | Availability alone is insufficient. |
| Clause availability `unavailable` | `assemble_bounded_inquiry_frontier(...)` | Preserved in `unavailable_clause_refs`; may still be operative if established/inquiry/non-conflicting | Observed / implementation-local | Unavailable is not automatically blocking or non-establishment. |
| Clause availability `conflicting` | `assemble_bounded_inquiry_frontier(...)` | Material binding conflict | Observed | Conflicting availability defeats frontier establishment. |
| Clause availability `unknown` | `assemble_bounded_inquiry_frontier(...)` | Non-operative for coherence; possible missing required family if no other operative family clause exists | Observed | Unknown does not become unavailability or nonexistence. |
| Clause currency `stale` | `assemble_bounded_inquiry_frontier(...)` | Preserved in `stale_clause_refs`; non-operative because coherence requires non-conflicting but does not reject stale | Observed | Stale does not itself authorize refresh. |
| Required clause family absent from operative clauses | `assemble_bounded_inquiry_frontier(...)` | `missing_required_clause_family` | Observed | Insufficient current boundary, not proof frontier territory does not exist. |
| Four required coherent families + no material conflict | `assemble_bounded_inquiry_frontier(...)` | `frontier_state="established"` | Observed | Established frontier is still not inquiry executable. |
| Established frontier | Missing frontier-question formulation owner | Unknown / candidate question production | Inferred candidate | Prior audits require explicit formulation testimony before canonical question. |
| Bounded question | Downstream executable inquiry | Unknown locally; tool execution requires separate registered operation authority | Book/architecture correspondence | `frontier established != inquiry executable`. |

## Who consumes unavailable standing?

Observed consumers:

1. `assemble_bounded_inquiry_frontier(...)` consumes clause availability to collect `unavailable_clause_refs`.
2. `_is_operatively_coherent(...)` consumes availability only to reject `conflicting`; it does not reject `unavailable`.
3. Tests consume frontier output to prove unavailable refs are preserved and do not automatically replace clause standing.

Not observed:

- no blocking owner;
- no access-need owner;
- no observation-need owner;
- no refresh-requirement owner;
- no sufficiency owner consuming unavailable refs from the frontier;
- no lawful-inactivity owner.

## Transformations not recovered

Within the surveyed local area, no implemented responsibility transforms unavailable testimony into:

- blocking standing;
- access need;
- observation need;
- refresh requirement;
- insufficiency;
- lawful stopping;
- lawful inactivity.

Book/prior-report grammar permits unavailable evidence to support lawful stopping only when explicit lawful-stopping testimony says so. That is a separate clause responsibility, not an automatic effect of the availability dimension.

## Does `BoundedInquiryFrontier` preserve or judge availability?

It does both, but at different levels:

- It **preserves** availability by carrying complete clauses and collecting `unavailable_clause_refs`.
- It **judges coherence** by treating `evidence_availability == "conflicting"` as a material conflict and by requiring non-conflicting availability for operative coherence.
- It does **not** judge whether evidence is truly reachable, whether access is authorized, whether refresh is required, whether inquiry is blocked, or whether the inquiry may execute.

Thus the frontier assembler constitutionally judges boundary coherence, not availability truth.

## Standing required after frontier establishment before executable inquiry

The local recovered path requires at least one missing bridge before canonical inquiry execution:

```text
frontier_state="established"
→ explicit frontier-question formulation testimony
→ BoundedConstitutionalQuestion
→ separate downstream eligibility/dispatch authority
```

A frontier is not executable merely because it is established. Before an inquiry may become executable, repository evidence requires a canonical bounded question or equivalent downstream inquiry artifact, and executable tool movement still requires a separately registered operation and policy/executor path where tooling is involved. Access required is not access authorized.

## Places where one artifact carries multiple independent dimensions

`InquiryFrontierBoundaryClause` carries at least these independent dimensions:

- territory identity: `clause_family`, `eligible_evidence_territory_refs`, `already_visible_evidence_refs`, `source_lineage`;
- availability: `evidence_availability`;
- currency: `evidence_currency`;
- clause legal standing: `clause_standing`;
- scope relation: `scope_disposition`;
- family relation: `family_disposition`;
- ownership/provenance: `producer_ref`, `producer_lineage`, `adapter_ref`, `adapter_lineage`, `ownership_basis`.

`BoundedInquiryFrontier` also carries multiple independent dimensions:

- establishment state: `frontier_state`;
- operative coherence: `operative_clause_refs`;
- preserved total testimony: `preserved_clause_refs` and `clauses`;
- unresolved/refused dimensions: `missing_required_clause_families`, `material_conflict_clause_refs`, `unsupported_clause_refs`, `unknown_clause_refs`, `conflicting_clause_refs`;
- quality/availability dimensions: `stale_clause_refs`, `unavailable_clause_refs`;
- scope/family adjacency dimensions: `out_of_scope_clause_refs`, `mixed_clause_refs`, `adjacent_family_clause_refs`;
- negative authority flags: no scope invention, evidence admission, access authorization, execution, recording, ledger write, mutation, or result knowledge.

This proves the surveyed distinctions must not be collapsed:

```text
territory identified != evidence presently reachable
unavailable != nonexistent
preserved availability != blocking standing
frontier established != inquiry executable
access required != access authorized
insufficient current evidence != frontier absent
```

## Ownership gaps

1. The actual availability producer is not implemented as a dedicated verifier. Current code preserves caller/stage-supplied testimony and ownership lineage.
2. No owner derives availability from access probes, reachability checks, capability inventory, refresh state, or source authorization.
3. No owner consumes frontier `unavailable_clause_refs` into blocking, access need, observation need, refresh-required standing, insufficiency, lawful stopping, or lawful inactivity.
4. No implemented frontier-to-question formulation testimony owner exists.
5. No local downstream owner proves that an established frontier has all prerequisites for executable inquiry.
6. No current artifact distinguishes unavailable because source identity is known but access is missing, unavailable because refresh is needed, unavailable because capability is absent, or unavailable because reachability failed.

## Fidelity judgments

- **No fidelity crossing** is warranted merely because availability ownership is incomplete. The implementation is explicit that boundary testimony preserves supplied availability and that frontier assembly judges only clause coherence.
- **No crossing** is warranted for preserving unavailable evidence territory inside an established frontier. The implementation and tests show unavailable is an independent dimension and does not automatically defeat establishment.
- **Potential under-specification, not crossing**: the minimal case where the sole required evidence-territory clause is established but unavailable remains a local implementation convention unless more focused constitutional grammar or tests make that case explicit.
- **Crossing would occur** if a downstream responsibility treated `unavailable_clause_refs` as access authorization, refresh authorization, evidence nonexistence, or lawful stop without explicit stage-owned testimony. No such implemented crossing was observed.

## Remaining Unknowns

- Which concrete stage, if any, should own verified evidence availability rather than preserving supplied testimony.
- Whether availability should eventually split into access, reachability, capability, freshness/refreshability, source existence, and authorization dimensions.
- Whether unavailable evidence territory should ever be sufficient as the sole operative evidence-territory family for frontier establishment, or only preserved beside available territory.
- What artifact should consume unavailable testimony and produce blocking standing, access need, observation need, refresh-required standing, insufficiency, lawful stopping, or lawful inactivity.
- Whether the future frontier-question formulation owner must reject established frontiers with unavailable operative evidence territory or merely preserve that condition into the canonical question.
- What exact downstream checks make an inquiry executable after a bounded question exists.

## Single most dominating next inquiry

What is the minimal read-only post-frontier eligibility responsibility that consumes one established `BoundedInquiryFrontier` plus its preserved availability/currency/territory clauses, distinguishes unavailable from access-required, refresh-required, observation-required, insufficient, and lawful-stop standings, and either produces explicit frontier-question formulation eligibility or a named non-executable refusal without authorizing access, selecting observations, refreshing evidence, executing inquiry, recording, writing the event ledger, or mutating cluster state?
