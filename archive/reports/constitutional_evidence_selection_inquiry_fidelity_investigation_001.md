# Constitutional Evidence Selection/Inquiry Fidelity Investigation 001

## Completed grammar consumed

The completed constitutional evidence-uptake grammar led this investigation. The grammar used here is:

```text
available material
!=
applicable material
!=
admitted material
!=
consumed material
```

and:

```text
visibility != eligibility
reference != resolved Evidence
support association != reliance
consumer validation != producer occurrence
admission != truth
selection != authority for movement
```

Evidence relevance and uptake are responsibility-local. The consumer, not the producer vocabulary, determines which coordinates are material for the bounded purpose. Relevant coordinate families may include identity, content, standing, provenance, responsibility, authority, scope, and occurrence/preservation, but no universal schema is required.

## Bounded Fidelity question

Does current selection and inquiry machinery give actual resolved Evidence bounded constitutional use, or does it only preserve, transport, expose, or manipulate evidence references and evidence vocabulary?

## Expected constitutional relation

Where actual Evidence influences selection or inquiry, a faithful witness should preserve a recoverable equivalent of:

```text
resolved Evidence
+
bounded consumer responsibility
+
declared purpose
↓
consumer-local applicability
↓
applicable / inapplicable / Unknown / conflict
↓
consumer-local admission
↓
admitted / unadmitted / Unknown / conflict
↓
selection or inquiry consumer use
↓
new bounded consumer-local standing
```

The relation may be distributed or compressed, but the constitutional distinctions must remain recoverable.

## Implementation witness examined

The strongest bounded relationships found in the current selection and inquiry witness are:

1. `Evidence` canonical payload records.
2. Evidence Graph fact material resolution.
3. Advancement need reference projection.
4. Advancement need consideration selection by `NeedFocusEvidence`.
5. Inquiry need projection from repository/world uncertainty testimony.
6. Inquiry-frontier boundary testimony preservation.
7. Bounded inquiry frontier assembly.

The app implementation was treated as witness testimony. Terms such as `evidence_ref`, `already_visible_evidence_refs`, `eligible_evidence_territory_refs`, `focus_evidence_refs`, and `operative_clause_refs` were not accepted as actual Evidence merely because they use evidence vocabulary.

## Required comparison

| Distinction | Current witness finding | Fidelity result |
| --- | --- | --- |
| Reference preservation | Selection, need projection, reference projection, and frontier testimony preserve evidence-shaped identifiers and lineage coordinates. | faithful within scope |
| Evidence resolution | Evidence Graph resolves fact evidence IDs against projected `State.evidence`; selection/inquiry-frontier roads do not resolve those IDs to canonical `Evidence`. | Unknown |
| Applicability | Selection validates focus identity against the exact visible advancement need reference and its need set, selection, goal, horizon, family, native projection, and lineage. Inquiry projection validates testimony against selection/goal/horizon/evidence identity and local repository-world uncertainty dimensions. Frontier assembly tests clause coherence for required frontier families. | faithful within scope where implemented; Unknown for actual canonical Evidence applicability |
| Eligibility | Advancement need references separate visible from selectable; frontier testimony separates visible evidence references from eligible evidence territory. | faithful within scope |
| Admission | Selection admits only exact focus references into selected-reference standing; frontier assembly admits only operatively coherent boundary clauses into frontier establishment. No witness admits resolved canonical Evidence into selection/inquiry use. | faithful within scope for references/clauses; Unknown for actual Evidence |
| Selection use | Need consideration selection materially depends on exact focus-reference identity and selectable standing, not evidence presence or support counts. | faithful within scope |
| Inquiry use | Bounded frontier assembly materially depends on selected inquiry need identity plus coherent required boundary clauses; it does not execute inquiry. | faithful within scope |
| Movement authority | Selection and frontier assembly explicitly deny opening inquiry, authorizing access, starting execution, recording, event-ledger writes, and cluster mutation. | faithful within scope |

## Per-relationship Fidelity analysis

### 1. Canonical `Evidence` records

- **Consumer responsibility:** Preserve observed source payloads as provenance-backed support material for facts.
- **Bounded purpose:** Model a source payload that can support facts.
- **Upstream Evidence or reference:** Actual `Evidence` has `id`, `workspace_id`, `source`, `kind`, `observed_at`, `payload`, and `confidence`.
- **Resolution boundary:** The model itself is canonical material only when an instance is present; a string ID alone is not enough.
- **Applicability boundary:** Not established by the model. The model does not say which consumer purpose may use the Evidence.
- **Admission boundary:** Not established by the model.
- **Consumer act:** None inside the model.
- **Resulting standing:** Evidence record exists as source payload; no consumer-local admission standing is produced here.
- **Refusal / conflict / Unknown behavior:** Not owned here.
- **Authority and scope treatment:** Not expanded by the model.
- **Producer-occurrence treatment:** `observed_at`, `source`, and `kind` preserve occurrence/provenance coordinates for an actual record, but they do not make downstream use lawful.
- **Fidelity result:** **faithful within scope** as canonical record shape; **Unknown** as consumer-local uptake.

### 2. Evidence Graph fact material resolution

- **Consumer responsibility:** Build a deterministic read-only evidence graph from projected `State` for fact-evidence views.
- **Bounded purpose:** Resolve fact `evidence_ids` to `State.evidence` records when possible, otherwise preserve unresolved references.
- **Upstream Evidence or reference:** Fact evidence IDs and `State.evidence` canonical records.
- **Resolution boundary:** The graph resolves only when the evidence ID exists in `state.evidence`; missing IDs become `unresolved_evidence_reference` standing rather than Evidence.
- **Applicability boundary:** The graph associates resolved Evidence with fact support views, but it does not establish selection or inquiry applicability.
- **Admission boundary:** The graph creates support links and view explanations for facts; it does not admit that Evidence into advancement-need selection or inquiry-frontier use.
- **Consumer act:** Fact-evidence view construction and evidence graph link construction.
- **Resulting standing:** Read-only graph standing: resolved evidence node, evidence link, fact evidence view, or represented unresolved reference.
- **Refusal / conflict / Unknown behavior:** Missing evidence is preserved as an unresolved reference; unsupported facts explain that no resolved supporting evidence is linked.
- **Authority and scope treatment:** Graph derivation remains read-only and does not execute, persist a separate evidence DB, or mutate state.
- **Producer-occurrence treatment:** Resolved nodes carry source event/run and confidence when present; unresolved references do not invent occurrence.
- **Fidelity result:** **faithful within scope** for reference-versus-resolution. **Unknown** for selection/inquiry consumer use because this witness does not connect graph-resolved Evidence to the current selection or inquiry machinery.

### 3. Advancement need reference projection

- **Consumer responsibility:** Expose visible read-only references for native advancement-need projection items.
- **Bounded purpose:** Preserve one reference per native item with identity and metadata, without reclassifying or selecting.
- **Upstream Evidence or reference:** Native projection items may carry `evidence_ref` or `evidence_refs`; projection preserves them as reference strings and evidence-quality metadata.
- **Resolution boundary:** No canonical Evidence resolution occurs.
- **Applicability boundary:** Applicability is limited to reference identity for the advancement-need reference set: need set, family, native projection, and family-local lineage.
- **Admission boundary:** No Evidence is admitted. Selectability is derived from native bucket and standing, not from resolved Evidence.
- **Consumer act:** Reference projection.
- **Resulting standing:** Visible/selectable/non-selectable advancement need reference standing.
- **Refusal / conflict / Unknown behavior:** Duplicate native lineage becomes a conflict and non-selectable; non-established/unknown/conflicting buckets remain visible but non-selectable.
- **Authority and scope treatment:** The reference set explicitly does not select, prioritize, route, open inquiry, request authority, authorize work, execute, record, write ledger events, or mutate.
- **Producer-occurrence treatment:** Evidence quality metadata is preserved, but producer occurrence is not inferred from reference presence.
- **Fidelity result:** **faithful within scope** as reference preservation and visibility/eligibility separation. **Unknown** as actual Evidence uptake.

### 4. Advancement need consideration selection by `NeedFocusEvidence`

- **Consumer responsibility:** Select one advancement need for consideration from exact focus evidence naming exact visible advancement-need references.
- **Bounded purpose:** Convert exact focus-reference identity into one selected consideration reference if all local identity and selectability constraints hold.
- **Upstream Evidence or reference:** `NeedFocusEvidence` carries an `evidence_ref`, `source_ref`, expected selected reference identity, need-set identity, selection identity, goal/horizon identity, family, native projection, native lineage, evidence state, candidate references, unknowns, and conflicts.
- **Resolution boundary:** The consumer resolves a reference against `reference_set.references`; it does not resolve `evidence_ref` to canonical `Evidence`.
- **Applicability boundary:** Applicable focus requires exact reference state, one named ID, matching need set, selection, goal establishment, horizon, family, native projection, and native lineage.
- **Admission boundary:** Only an exact, matching, present, unique, non-conflicted, selectable reference is admitted into `selected_reference`.
- **Consumer act:** Selection for consideration.
- **Resulting standing:** `selection_state=selected` and bounded selected-reference standing, or a refusal state.
- **Refusal / conflict / Unknown behavior:** Missing evidence, missing identity, ambiguity, conflict, absent reference, duplicate lineage conflict, non-selectability, and reference mismatch all refuse selection rather than repairing the gap.
- **Authority and scope treatment:** The output explicitly refuses overclaim: it is not highest priority, primary blocker, resolution, next action, inquiry opened, authority requested, work authorized, execution, recording, ledger write, or mutation.
- **Producer-occurrence treatment:** `source_ref` and `evidence_ref` provenance references are preserved, but no canonical occurrence is invented.
- **Fidelity result:** **faithful within scope** for bounded reference-based selection. **Unknown** for actual resolved Evidence use because the selected consumer depends materially on resolved advancement-need reference identity, not canonical Evidence resolution.

### 5. Inquiry need projection from repository/world uncertainty testimony

- **Consumer responsibility:** Project inquiry-need standings from explicit component-bounded repository/world uncertainty testimony.
- **Bounded purpose:** Determine whether supplied testimony locally establishes, does not support, leaves unknown, conflicts, excludes, or fails to classify inquiry need standing for the current selection/goal/horizon boundary.
- **Upstream Evidence or reference:** Testimony carries `evidence_ref`, component and subject references, owning stage, standing, freshness, availability, and local materiality flags.
- **Resolution boundary:** The witness checks `evidence_ref` membership in the horizon evidence snapshot references; it does not resolve the ID to canonical `Evidence`.
- **Applicability boundary:** The testimony must match selection, goal, horizon, evidence identity, repository-world uncertainty family, stage ownership, component boundedness, repository/world subject, materiality to the present movement boundary, and non-mixed inquiry component.
- **Admission boundary:** Passing testimony is bucketed into local standing buckets, or excluded if the horizon excludes inquiry family. Failing testimony becomes unclassified with a specific reason.
- **Consumer act:** Inquiry-need projection.
- **Resulting standing:** Consumer-local inquiry need projection standing: established, unsupported, unknown, conflicting, excluded-family, or unclassified.
- **Refusal / conflict / Unknown behavior:** Identity mismatch, stale/absent/nonmaterial/mixed/non-owned conditions remain separate; unknown and conflicting standings remain typed rather than becoming selected inquiry.
- **Authority and scope treatment:** The projection does not open inquiry, select a question, authorize observation, select next action, judge sufficiency, execute, record, write the event ledger, or mutate cluster state.
- **Producer-occurrence treatment:** Evidence freshness and availability are preserved as testimony coordinates; occurrence is not proved by evidence reference membership alone.
- **Fidelity result:** **faithful within scope** for local testimony applicability/admission. **Unknown** for actual canonical Evidence uptake because membership in a horizon evidence snapshot is not Evidence resolution.

### 6. Inquiry-frontier boundary testimony preservation

- **Consumer responsibility:** Preserve unordered stage-owned frontier-boundary clauses for one exact selected inquiry need.
- **Bounded purpose:** Carry boundary clauses without assembling a frontier, formulating a question, opening inquiry, authorizing access, or judging collective sufficiency.
- **Upstream Evidence or reference:** Selected inquiry need reference and caller-supplied boundary clause inputs, including visible evidence references, eligible evidence territory references, provenance roles, source lineage, and producer/adapter lineage.
- **Resolution boundary:** No canonical Evidence resolution occurs. Visible evidence references are copied from the selected reference and clause input.
- **Applicability boundary:** Preservation requires an exact selected inquiry need; clause ownership is recognized only through producer lineage or adapter lineage, not caller assertion.
- **Admission boundary:** None for frontier establishment. The witness preserves clauses and their local dispositions; it does not make them operative.
- **Consumer act:** Testimony preservation.
- **Resulting standing:** Preserved boundary testimony for selected inquiry need, plus unowned-clause standing where lineage is absent.
- **Refusal / conflict / Unknown behavior:** Unsupported, unknown, conflicting, stale, unavailable, out-of-scope, mixed, and adjacent-family dispositions remain separate on clauses.
- **Authority and scope treatment:** The output explicitly denies frontier assembly, question formulation, inquiry opening, authorization, execution, recording, ledger writing, mutation, source selection, observation selection, and collective sufficiency judgment.
- **Producer-occurrence treatment:** Producer occurrence is not accepted from a payload flag; lineage is required for ownership basis.
- **Fidelity result:** **faithful within scope** as preservation, identity binding, and visibility/eligibility separation. **Unknown** as actual Evidence uptake.

### 7. Bounded inquiry frontier assembly

- **Consumer responsibility:** Assemble a read-only bounded inquiry frontier from one exact selected inquiry need plus preserved frontier-boundary testimony.
- **Bounded purpose:** Determine whether required boundary clause families coherently establish a frontier.
- **Upstream Evidence or reference:** Selected inquiry need, testimony identity, and boundary clauses. The clauses include evidence vocabulary and evidence-territory references, but the assembler consumes clause standing and dispositions rather than canonical Evidence records.
- **Resolution boundary:** It resolves selected need/testimony identity and operative clause coherence. It does not resolve canonical Evidence.
- **Applicability boundary:** Operative clauses must be established, inquiry-disposed, non-conflicting in evidence currency/availability, and, for scope clauses, included.
- **Admission boundary:** Coherent clauses are admitted as operative clause refs. Missing required families or material conflicts prevent frontier establishment.
- **Consumer act:** Frontier assembly.
- **Resulting standing:** `frontier_state=established`, `missing_required_clause_family`, `material_binding_conflict`, or `not_selected_inquiry_need`, with preserved/non-operative/unsupported/unknown/conflicting/mixed/adjacent/stale/unavailable/out-of-scope refs.
- **Refusal / conflict / Unknown behavior:** Missing family and material conflict are explicit; non-operative dispositions remain visible and non-operative.
- **Authority and scope treatment:** The output explicitly denies scope invention, evidence admission invention, question formulation, inquiry opening, source/observation selection, access authorization, execution, recording, ledger writing, mutation, and result knowledge.
- **Producer-occurrence treatment:** The assembler relies on preserved testimony identity and clause dispositions; it does not invent producer occurrence or resolve evidence occurrence.
- **Fidelity result:** **faithful within scope** for clause-based frontier establishment. **Unknown** for actual Evidence use because no canonical Evidence is resolved or admitted.

## Actual Evidence resolution findings

Actual canonical Evidence resolution is present in the Evidence Graph witness: fact evidence IDs are looked up in `State.evidence`, and missing IDs are preserved as unresolved evidence references. That is a faithful reference/resolution boundary.

The current selection and inquiry witnesses examined here do not show actual canonical Evidence resolution. They preserve and validate evidence-shaped references, source references, provenance lineages, standing labels, evidence freshness, evidence availability, and evidence territory references. Those are meaningful local coordinates, but they are not canonical Evidence resolution.

## Visibility versus eligibility findings

The implementation faithfully distinguishes visibility from eligibility in two strong places:

1. Advancement need references can be visible while not selectable; only established native records with established standing are selectable.
2. Inquiry-frontier boundary testimony keeps already visible evidence references separate from eligible evidence territory references, and explicitly says eligible territory is not source selection or observation selection.

No examined witness treats visibility alone as eligibility.

## Applicability and admission findings

Applicability exists locally for reference and clause consumers:

- Focus evidence is applicable only when it binds the exact reference, need set, selection, goal, horizon, family, native projection, and native lineage.
- Repository/world uncertainty testimony is applicable only when it matches local selection/goal/horizon/evidence identity and bounded inquiry dimensions.
- Frontier clauses are applicable to frontier establishment only when their clause family and dispositions satisfy the assembler's local coherence test.

Admission exists locally for references and clauses:

- Need consideration selection admits one selectable advancement need reference into selected-reference standing.
- Frontier assembly admits coherent required clauses into operative frontier standing.

Admission of actual resolved canonical Evidence into selection or inquiry use remains **Unknown** because the examined roads do not resolve `evidence_ref` values to `Evidence` records before use.

## Consumer-use findings

The material consumer uses observed are:

- Reference projection uses native projection items to produce visible/selectable advancement need references.
- Need consideration selection uses exact focus-reference identity and selectability to produce selected-reference standing.
- Inquiry need projection uses local testimony validation to produce inquiry-need standing buckets.
- Boundary testimony preservation uses selected inquiry need identity and lineage to preserve clauses.
- Frontier assembly uses selected inquiry need identity and operative clause coherence to produce frontier standing.

None of those acts is proven to materially depend on resolved canonical Evidence. They materially depend on references, standing labels, local identity coordinates, and clause dispositions.

## Resulting standings

The resulting bounded standings are:

- canonical Evidence record existence as source payload;
- resolved evidence node / unresolved evidence reference / fact-evidence view in Evidence Graph;
- visible/selectable/non-selectable advancement need reference;
- selected/no-focus/missing-identity/ambiguous/conflict/reference-mismatch/absent-reference/duplicate-lineage-conflict/non-selectable need consideration selection;
- established/unsupported/unknown/conflicting/excluded-family/unclassified inquiry need projection item;
- preserved inquiry-frontier boundary testimony and unowned clause references;
- established/missing-required-clause-family/material-binding-conflict/not-selected-inquiry-need bounded inquiry frontier.

Each standing is consumer-local. None is universal Evidence truth or movement authority.

## Authority and occurrence findings

The examined machinery repeatedly refuses authority expansion:

- Reference projection does not select, route, open inquiry, request authority, authorize work, execute, record, write the ledger, or mutate.
- Need consideration selection does not select a next action, open inquiry, request authority, authorize work, execute, record, write the ledger, or mutate.
- Inquiry need projection does not open inquiry, select a question, authorize observation, execute, record, write the ledger, or mutate.
- Boundary testimony does not assemble a frontier, formulate a question, open inquiry, authorize, execute, record, write the ledger, mutate, select sources, select observations, or judge collective sufficiency.
- Frontier assembly does not invent scope or evidence admission, formulate a question, open inquiry, select sources/observations, authorize access, execute, record, write the ledger, mutate, or know the result.

Producer occurrence is not silently inherited where the tests are strongest. Boundary clause ownership requires producer lineage or adapter lineage; a caller's ownership assertion flag cannot create ownership. Evidence Graph unresolved references do not become resolved Evidence.

## Refusal / conflict / Unknown findings

Refusal, conflict, and Unknown are preserved as first-class outcomes rather than repaired by adjacency:

- Need consideration selection preserves no-focus, missing identity, ambiguity, conflict, reference mismatch, absent reference, duplicate lineage conflict, and non-selectability.
- Inquiry need projection preserves unsupported, unknown, conflicting, excluded-family, and unclassified reasons.
- Boundary testimony preserves unsupported, unknown, conflicting, stale, unavailable, out-of-scope, mixed, adjacent-family, and unowned statuses.
- Frontier assembly preserves missing required clause families, material conflicts, non-operative clauses, unknown clauses, conflicting clauses, stale clauses, unavailable clauses, and out-of-scope clauses.
- Evidence Graph preserves unresolved evidence references instead of resolving them by name.

## Unfaithful crossings, if any

No unfaithful boundary crossing was established in the examined witness.

Specifically, the investigation did not find proof of:

- visible reference becoming eligible Evidence;
- unresolved reference becoming admitted Evidence;
- evidence presence becoming a selection warrant;
- support count becoming authority;
- selection becoming lawful movement;
- consumer-local admission becoming universal standing.

## Faithful witnesses, if any

Faithful witnesses within scope include:

1. Evidence Graph reference-versus-resolution behavior.
2. Advancement need reference visibility-versus-selectability behavior.
3. Need consideration selection's exact-reference and refusal behavior.
4. Inquiry need projection's local applicability checks and typed standing buckets.
5. Inquiry-frontier testimony's visible-evidence versus eligible-territory separation and producer-lineage ownership treatment.
6. Bounded inquiry frontier assembly's operative-clause admission, conflict preservation, and denial of movement authority.

## Preserved Unknowns

The main preserved Unknown is the bounded question itself: current selection and inquiry machinery is not proven to give actual resolved canonical Evidence bounded constitutional use. It is proven to preserve, transport, expose, validate, and consume evidence references, evidence vocabulary, local standing, and clause dispositions.

The relationship between Evidence Graph-resolved canonical Evidence and the selection/inquiry roads remains **Unknown**. The repository has a faithful resolver witness and faithful selection/inquiry witnesses, but this operation did not find a serious relationship where the latter consume the former as resolved Evidence under a declared local purpose and admission boundary.

## Book projection decision

No Book update is warranted.

The completed grammar already expresses the relation exposed by the witness: reference preservation, Evidence resolution, applicability, admission, consumer use, authority, and occurrence must remain distinct. The implementation witness does not expose a constitutional relation that the completed grammar cannot express. Adding repetitive uptake prose would risk over-projecting implementation vocabulary into Book grammar.

## Smallest lawful implementation frontier

The smallest Fidelity pressure exposed by the witness is an unresolved relationship that must remain **Unknown**:

> The current selection and inquiry witnesses have strong local reference and clause uptake, but they do not expose whether or where graph-resolved canonical `Evidence` is admitted into selection or inquiry consumer use for a declared bounded responsibility and purpose.

The lawful frontier is therefore not a universal Evidence resolver, admission engine, inquiry router, or selection pipeline. It is only this future observability question:

```text
For one existing selection or inquiry consumer, should there be an observable consumer-local standing that distinguishes
resolved canonical Evidence admitted for that purpose
from evidence references merely preserved or validated for identity?
```

This operation does not implement that frontier.
