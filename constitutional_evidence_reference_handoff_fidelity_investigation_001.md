# Constitutional Evidence Reference Handoff Fidelity Investigation 001

## Completed grammar consumed

This investigation consumes as completed grammar and witness evidence:

- `book_of_seed/applicability_admission_consumption_projection_001.md`
- `constitutional_evidence_selection_inquiry_fidelity_investigation_001.md`
- `constitutional_evidence_consumer_district_survey_001.md`
- `evidence_graph_admission_fidelity_slice_001.md`

The controlling grammar is:

```text
available != applicable != admitted != consumed
reference != resolved Evidence
upstream admission != downstream admission
producer output standing != consumer-local admission standing
```

Admission is responsibility-local. This report therefore keeps producer-side establishment separate from consumer-side admission, and it does not use downstream behavior to repair upstream standing or upstream naming to excuse downstream admission.

## Strict separation of investigations

- **Pass A** examines only producer-side witness for artifacts later presented to selection and inquiry.
- **Pass B** examines only consumer-side witness inside selection, inquiry-need projection, frontier-boundary testimony preservation, and frontier assembly.
- **Pass C** compares the independently recovered sides only after Pass A and Pass B.

The report clearly distinguishes:

```text
Evidence reference identity
!=
established evidence-reference standing
!=
downstream admission of that standing
!=
downstream consumption
```

## Pass A - independent upstream investigation

### Bounded upstream question

What upstream responsibility, applicability boundary, admission act, and consumption act establish the standing of the artifact later supplied downstream?

### Upstream witness map

| Upstream material | Producer responsibility and bounded purpose | Applicability | Admission / refusal / Unknown / conflict | Producer consumption | Produced reference or testimony standing |
| --- | --- | --- | --- | --- | --- |
| Native advancement-need projection items presented through an `AdvancementNeedReferenceSet` | Expose one read-only reference per supplied native item without changing native need meaning. | Binds only need set, family, native projection, and family-local native lineage. | Established native bucket and standing become selectable; non-established/unknown/conflicting/excluded/unclassified buckets remain visible but non-selectable; duplicate lineage becomes conflict. | The producer reads supplied projection bucket membership, native lineage, native standing, evidence references, and evidence-quality fields. | Visible advancement-need reference; selectable only when bucket is `established` and native standing is `established`; not resolved Evidence. |
| `EvidenceSnapshotReference` entries in a bounded advancement horizon | Preserve current advancement boundary for one exact selected goal, including supplied evidence snapshot references. | Horizon applicability is selected-goal identity plus present movement boundary; snapshot entries are preserved after the horizon itself is bounded. | Horizon refuses on unresolved selection, goal mismatch, non-established goal, missing movement boundary, or excluded family lacking reason; snapshot entries are otherwise preserved with their supplied state. | The producer consumes caller-supplied snapshot references only as boundary coordinates and deduped stale/unavailable reference lists. | Horizon-local evidence snapshot reference standing; reference identity and snapshot identity are preserved, not resolved Evidence admission. |
| `RepositoryWorldUncertaintyTestimony` into `InquiryNeedProjection` | Project inquiry-need standings from explicit component-bounded repository/world uncertainty testimony without opening inquiry. | Selection, goal, horizon, horizon evidence-reference membership, repository-world family, stage ownership, component boundedness, subject identity, and materiality to current movement. | Mismatches become unclassified reasons; excluded inquiry family becomes `excluded_family`; otherwise supplied standing is preserved into established/unsupported/unknown/conflicting buckets. | The producer consumes testimony coordinates and horizon evidence-reference membership to produce projection items and projection evidence reference set. | Inquiry-need projection item testimony standing; preserves `evidence_ref`, freshness, availability, and unclassified reason; not resolved Evidence. |
| `FrontierBoundaryClauseInput` into `InquiryFrontierBoundaryTestimony` | Preserve unordered stage-owned or adapter-owned frontier-boundary clauses for one exact selected inquiry need. | Applicable only when the selected need is selected and is an inquiry reference; clause ownership is recognized from producer lineage or adapter lineage. | Unowned clauses are preserved as unowned references; caller assertion alone does not establish ownership; non-inquiry or unselected need produces no selected inquiry boundary standing. | The producer consumes selected inquiry reference identity, native lineage, and clause fields including visible evidence refs, eligible territory refs, provenance roles, source lineage, and producer/adapter lineage. | Preserved frontier-boundary testimony with owned/unowned clause standing and separate visible evidence refs versus eligible territory refs. |

### Upstream applicability, admission, consumption, and resulting standing

#### 1. Advancement-need reference production

- **Applicability:** Native items are applicable to reference production only through the supplied need set, family, native projection, and family-local lineage. Standing, bucket, evidence quality, and selectability are metadata, not reference identity.
- **Admission:** The producer admits an advancement-need reference as selectable only when its native bucket is `established` and native standing is `established`. Duplicate native lineage is preserved as conflict and non-selectable. Unknown/conflicting/non-established native standings remain visible but are not admitted as selectable.
- **Consumption:** The producer consumes supplied projection items to construct `AdvancementNeedReference` objects and a read-only `AdvancementNeedReferenceSet`.
- **Resulting standing:** Lawfully produced reference standing, not canonical Evidence standing. The artifact is not caller-constructed at the downstream seam, but its `evidence_refs` remain preserved reference strings.
- **Fidelity:** **faithful within scope** for reference production; **Unknown** for actual resolved Evidence uptake.

#### 2. Horizon evidence snapshot reference production

- **Applicability:** Evidence snapshot references are applicable only inside a horizon that first satisfies selected-goal identity, established goal artifact, and present movement boundary requirements.
- **Admission:** The horizon admits the supplied snapshot references as boundary references when the horizon is bounded; stale and unavailable reference lists are preserved separately. It does not admit resolved Evidence.
- **Consumption:** The producer consumes provided `EvidenceSnapshotReference` entries into horizon state and stable identity payload.
- **Resulting standing:** Horizon-local evidence-reference availability/currentness standing. A preserved `evidence_ref` is not evidence-reference admission standing for any later consumer by itself.
- **Fidelity:** **faithful within scope** for boundary preservation; **Unknown** for producer occurrence and actual Evidence resolution.

#### 3. Inquiry-need testimony production

- **Applicability:** Repository/world uncertainty testimony is applicable only when selection, goal, horizon, evidence-reference membership, family, ownership, bounded component, subject, and materiality coordinates match.
- **Admission:** Matching testimony is admitted into the standing bucket supplied by the testimony, unless inquiry is explicitly excluded; mismatches are refused from classified standing and preserved as unclassified reasons.
- **Consumption:** The producer consumes testimony and horizon evidence-reference membership to produce `InquiryNeedProjectionItem` records.
- **Resulting standing:** Producer-local inquiry-need testimony standing. The `evidence_ref` has membership standing in the horizon reference set, not resolved Evidence standing.
- **Fidelity:** **faithful within scope** for testimony classification and refusal preservation; **Unknown** for actual Evidence admission.

#### 4. Frontier-boundary testimony production

- **Applicability:** Clause preservation is applicable only for one exact selected inquiry need. Ownership is proven by producer lineage or adapter lineage, not by a caller assertion.
- **Admission:** Owned and unowned clause status is preserved. Clause standing, scope disposition, evidence currency, evidence availability, and family disposition are copied as clause-local standing; the testimony producer does not assemble a frontier.
- **Consumption:** The producer consumes selected inquiry reference coordinates and clause input fields to emit `InquiryFrontierBoundaryClause` records.
- **Resulting standing:** Preserved boundary testimony standing. Already visible evidence references and eligible evidence territory references remain separate coordinate families.
- **Fidelity:** **faithful within scope** for boundary testimony preservation and ownership treatment; **Unknown** for resolved Evidence standing.

### Independent upstream Fidelity result

**faithful within scope** for lawful production of references and testimony standings. The upstream witnesses establish responsibility-local standings for reference production, horizon snapshot preservation, inquiry-need testimony projection, and frontier-boundary testimony preservation. They do not establish actual resolved Evidence standing for downstream selection or inquiry, and they do not prove producer occurrence from `evidence_ref` field shape.

## Pass B - independent downstream investigation

### Bounded downstream question

What downstream responsibility, applicability boundary, admission act, and consumption act govern the supplied artifact inside selection or inquiry?

### Downstream witness map

| Presented artifact | Consumer responsibility and bounded purpose | Applicability | Admission / refusal / Unknown / conflict | Consumer consumption | Selection / inquiry / frontier standing |
| --- | --- | --- | --- | --- | --- |
| `NeedFocusEvidence` supplied to advancement-need consideration selection | Select one advancement need for consideration from exact focus evidence naming an exact visible reference. | Requires exact reference state, one named reference, matching need set, selection, goal, horizon, family, native projection, and native lineage. | Missing, Unknown, ambiguous, conflict, absent reference, duplicate lineage, non-selectable, and mismatch states are preserved as distinct selection states. | Consumes focus evidence only to choose one exact selectable reference or preserve refusal/conflict/Unknown. | Selected advancement-need reference standing; does not resolve `evidence_ref` to Evidence. |
| `RepositoryWorldUncertaintyTestimony` supplied to inquiry-need projection | Classify explicit repository/world uncertainty as inquiry need for current selection/goal/horizon. | Requires local identity matches and `evidence_ref` membership in horizon evidence snapshot refs; validates family, owning stage, component boundedness, subject, and materiality. | Mismatches become unclassified; Unknown/conflicting/unsupported standings remain separate buckets; excluded inquiry family preserved. | Consumes testimony coordinates to produce inquiry-need projection items. | Inquiry-need standing; `evidence_ref` membership is checked, but resolved Evidence is not required. |
| `FrontierBoundaryClauseInput` supplied to boundary testimony preservation | Preserve boundary clauses for one exact selected inquiry need. | Requires selected inquiry need; preserves clause ownership only when producer or adapter lineage is present. | Unowned clauses remain visible as unowned; no frontier assembled; no source or observation selected. | Consumes clause input fields into preserved clause records. | Boundary testimony standing; visible evidence refs and eligible territory refs remain distinct. |
| `InquiryFrontierBoundaryTestimony` supplied to bounded frontier assembly | Assemble a read-only frontier only from already preserved boundary testimony for one exact selected inquiry need. | Requires selected-need/testimony identity match and operative coherence of required clause families. | Identity conflicts and explicit clause conflicts become material conflicts; unsupported/unknown/stale/unavailable/out-of-scope/mixed/adjacent clauses are preserved as non-operative/refusal coordinates. | Consumes preserved clauses to determine operative clauses, missing required families, conflicts, and frontier state. | Bounded inquiry frontier standing; does not invent evidence admission, formulate question, open inquiry, authorize, execute, record, or mutate. |

### Downstream applicability, admission, consumption, and resulting standing

#### 1. Advancement-need consideration selection

- **Applicability required/revalidated:** The consumer revalidates reference identity, need set, selection, goal, horizon, family, native projection, and native lineage. It also requires the selected upstream reference to be visible, unique, not conflicted, and selectable.
- **Admission:** The consumer admits one exact selectable advancement-need reference into selected-reference standing. It refuses or preserves Unknown/conflict states when focus evidence is absent, missing, Unknown, ambiguous, conflicting, mismatched, absent, duplicate, or non-selectable.
- **Consumption:** It consumes focus evidence and the visible reference set to produce `AdvancementNeedConsiderationSelection`.
- **Resulting standing:** Selection-for-consideration standing over a reference. It does not consume actual resolved Evidence and does not use `evidence_ref` as Evidence.
- **Fidelity:** **faithful within scope** for reference selection; **Unknown** for actual Evidence admission.

#### 2. Inquiry-need projection as downstream consumer

- **Applicability required/revalidated:** The consumer validates selection identity, goal identity, horizon identity, `evidence_ref` membership in horizon snapshot references, repository/world uncertainty family, stage ownership, component boundedness, repository/world subject, and materiality.
- **Admission:** It admits testimony into inquiry-need standing buckets only after those local checks. It preserves unsupported, unknown, conflicting, excluded-family, and unclassified reasons without repair.
- **Consumption:** It consumes the supplied testimony as testimony, not as resolved Evidence.
- **Resulting standing:** Inquiry-need projection standing. Downstream validates `evidence_ref` membership but does not validate snapshot identity, source payload, source occurrence, authority of the evidence producer, or canonical Evidence existence.
- **Fidelity:** **faithful within scope** for component-bounded inquiry testimony; **Unknown** for resolved Evidence.

#### 3. Frontier-boundary testimony preservation as downstream consumer

- **Applicability required/revalidated:** The consumer validates that the selected need is selected and belongs to the inquiry family. It does not revalidate clause content as sufficient for frontier; it preserves clause standing and ownership coordinates.
- **Admission:** It admits clause records into preserved testimony only as boundary testimony. Ownership requires producer lineage or adapter lineage; caller assertion is ignored for ownership.
- **Consumption:** It consumes clause inputs into preserved boundary testimony.
- **Resulting standing:** Preserved testimony standing, including unowned clause refs and separate already-visible evidence refs versus eligible evidence territory refs.
- **Fidelity:** **faithful within scope** for preservation; **Unknown** for clause truth and resolved Evidence admission.

#### 4. Bounded inquiry frontier assembly as downstream consumer

- **Applicability required/revalidated:** The consumer revalidates selected-need/testimony identity, required clause families, clause standing, inquiry family disposition, evidence conflict flags, availability/currency conflict flags, and included scope for scope clauses.
- **Admission:** It admits only operatively coherent clauses into operative frontier use. Non-established, non-inquiry, conflicting, stale, unavailable, unknown, unsupported, adjacent, mixed, and out-of-scope clauses remain preserved as non-operative or conflict coordinates.
- **Consumption:** It consumes preserved boundary testimony to establish or refuse bounded frontier standing.
- **Resulting standing:** Bounded inquiry frontier standing. The frontier explicitly does not invent evidence admission.
- **Fidelity:** **faithful within scope** for frontier assembly; **Unknown** for actual Evidence use.

### Independent downstream Fidelity result

**faithful within scope** for consumer-local admission of references, testimony, and clauses. Downstream consumers revalidate responsibility-local coordinates and preserve refusal, conflict, and Unknown states. They do not require canonical `Evidence` resolution, and no downstream witness proves actual Evidence admission into selection or inquiry.

## Pass C - cross-examination

### Cross-examination matrix

| Handoff | Same artifact admitted downstream? | Does upstream establish every coordinate downstream relies upon? | Does downstream revalidate only local coordinates? | Silent stronger inheritance? | Classification | Fidelity outcome |
| --- | --- | --- | --- | --- | --- | --- |
| Advancement-need reference set -> `NeedFocusEvidence` selection | Not exactly. Downstream admits a caller-supplied focus artifact that names an upstream reference, then matches it against the reference set. | Partly. Upstream establishes reference identity/selectability; the focus artifact itself is caller-supplied and not producer-emitted by the reference producer. | Yes for reference identity and selectability. | No stronger Evidence standing inherited; focus source/evidence refs are provenance only. | **lawful asymmetry** with caller-constructed representation risk preserved | faithful within scope |
| Horizon `EvidenceSnapshotReference` -> inquiry testimony `evidence_ref` membership | Same reference identifier, not same resolved Evidence artifact. | Partly. Upstream preserves `evidence_ref` and snapshot state; downstream relies only on `evidence_ref` membership, not snapshot identity or resolved Evidence. | Yes, but compressed: membership only. | No resolved Evidence standing inherited; snapshot authority and occurrence remain Unknown. | **lawful asymmetry** | faithful within scope; Unknown for Evidence |
| Inquiry-need projection item -> advancement-need reference set -> selected inquiry reference -> frontier-boundary testimony | Same selected reference identity is preserved through projection/reference/selection into testimony. | Mostly for identity, family, native lineage, and evidence refs; clause ownership and clause standing are new downstream/caller supplied coordinates. | Yes for selected inquiry identity; clause ownership is local to boundary testimony preservation. | No Evidence standing inherited; clause truth is not inferred from selected need. | **exact lawful handoff** for selected reference identity; **lawful asymmetry** for clause-local standing | faithful within scope |
| Frontier-boundary testimony -> bounded inquiry frontier | Same preserved clause artifacts are consumed by frontier assembly. | Yes for preserved clause fields; frontier adds operative coherence requirements. | Yes; it revalidates frontier-local required families and operative coherence. | No; non-operative/refusal coordinates are preserved. | **exact lawful handoff** for clause artifacts; no duplicated admission | faithful within scope |
| Evidence references throughout selection/inquiry -> resolved Evidence | No. The artifact is an identifier/reference, not a resolved `Evidence` record. | No upstream examined here establishes canonical Evidence occurrence for these references. | Downstream does not revalidate canonical Evidence; it also does not claim it does. | No current stronger standing claim in these witnesses; actual Evidence remains Unknown. | **Unknown** rather than standing gap, because downstream does not require canonical Evidence for this scope | Unknown for Evidence, faithful for references |

### Coordinate-by-coordinate handoff comparison

| Coordinate | Upstream output standing | Downstream expected input/admission standing | Comparison |
| --- | --- | --- | --- |
| Evidence reference identity | Preserved as strings in `evidence_refs`, `EvidenceSnapshotReference.evidence_ref`, and testimony `evidence_ref`. | Matched by exact reference ID for selection focus or by membership in horizon evidence refs for inquiry testimony. | Preserved as identity only; reference identity is not Evidence standing. |
| Established evidence-reference standing | Selectability or membership can be established locally; horizon snapshot state can be `current`, `stale`, or other supplied state. | Selection admits selectable references; inquiry projection admits testimony only if `evidence_ref` is in horizon refs; frontier separates visible refs from eligible territory refs. | Lawful compression where downstream needs membership, not full snapshot standing. |
| Downstream admission of that standing | Not owned upstream. | Consumer-local: selected-reference standing, inquiry-need bucket, boundary-testimony preservation, or operative frontier clause. | Responsibility-local admission preserved. |
| Downstream consumption | Not owned upstream. | Consumed to produce selection, inquiry projection, boundary testimony, or frontier state. | No upstream/downstream symmetry assumed. |
| Identity | Producer identity includes need set/family/projection/lineage or horizon/selection/goal. | Consumers revalidate exact local identity coordinates. | Faithful within scope. |
| Provenance | Source refs, native lineage, source lineage, producer lineage, adapter lineage are preserved where supplied. | Downstream preserves provenance and uses producer/adapter lineage for ownership, not caller assertion. | Faithful within scope; producer occurrence remains separate. |
| Purpose | Upstream purposes are reference exposure, horizon preservation, inquiry-need projection, boundary testimony preservation. | Downstream purposes are selection-for-consideration, inquiry need classification, boundary testimony preservation, frontier assembly. | Lawful asymmetry; purposes are not merged. |
| Scope | Upstream scope is need set/horizon/present movement boundary and clause scope disposition. | Downstream revalidates selected need/horizon and frontier included scope for operative scope clauses. | Faithful within scope. |
| Authority | Upstream artifacts are read-only and deny execution/recording/mutation. | Downstream consumers also deny opening inquiry or operational movement except bounded frontier standing. | Preserved; no authority expansion. |
| Occurrence | Actual producer occurrence for Evidence is Unknown; source/provenance references are preserved. | Downstream does not infer occurrence from IDs and does not require canonical Evidence. | Faithful within scope with preserved Unknown. |
| Preservation | References, unknowns, conflicts, unclassified reasons, and non-operative clause lists are preserved. | Downstream carries these as refusal/conflict/Unknown coordinates. | Faithful within scope. |
| Standing | Upstream standing is reference/testimony/clause-local. | Downstream standing is consumer-local selection/inquiry/frontier standing. | Lawful asymmetry. |

### Lawful asymmetries

- Upstream may lawfully produce a selectable advancement-need reference while downstream separately requires focus evidence naming that reference.
- Horizon evidence references may lawfully be sufficient for inquiry-testimony membership without becoming canonical Evidence.
- Boundary testimony may lawfully add clause-local ownership and standing coordinates that were not produced by the selected inquiry reference.
- Frontier assembly may lawfully admit only a subset of preserved clauses as operative while preserving the rest as non-operative, unsupported, unknown, conflicting, stale, unavailable, out-of-scope, mixed, or adjacent.

### Gaps, mismatches, or duplicated admission

- **Caller-constructed representation risk:** `NeedFocusEvidence` is not shown as produced by the advancement-need reference producer. The handoff is lawful only because downstream treats it as focus evidence and revalidates it against visible references; it is not proof of upstream producer output standing.
- **Canonical Evidence Unknown:** Neither side resolves `evidence_ref` or `focus_evidence_refs` to canonical `Evidence` for selection/inquiry. This is not a correction target in this investigation because downstream does not require canonical Evidence for the bounded responsibilities examined.
- **Snapshot compression:** Inquiry projection checks `evidence_ref` membership but not `snapshot_ref` or evidence snapshot state. This is lawful asymmetry if the consumer requires only membership; it would become a standing gap only if future behavior relies on snapshot state, currentness, source occurrence, or producer authority.
- **No duplicated admission found:** Producer reference standing and downstream selected-reference/frontier admission standing are separate acts. The frontier consumes preserved clauses after boundary testimony preservation; it does not repeat producer ownership admission except through frontier-local operative coherence.

### Preserved refusal, conflict, and Unknown

- Focus evidence absence, missing identity, Unknown, ambiguity, conflict, absent references, duplicate lineage, and non-selectable references remain explicit selection states.
- Inquiry testimony mismatches remain unclassified reasons; unsupported, unknown, conflicting, and excluded-family buckets remain separate.
- Boundary testimony preserves unowned clause references rather than repairing ownership through caller assertion.
- Frontier assembly preserves missing required clause families, material binding conflicts, unsupported clauses, unknown clauses, conflicting clauses, mixed clauses, adjacent-family clauses, stale clauses, unavailable clauses, and out-of-scope clauses.
- Actual canonical Evidence occurrence and admission remain **Unknown** for these handoffs.

### Authority and producer-occurrence treatment

Authority remains bounded and read-only across all examined handoffs. The witnesses deny inquiry opening, authorization, execution, recording, event-ledger writes, and cluster mutation at the reference-set, selection, inquiry-projection, testimony-preservation, and frontier-assembly boundaries.

Producer occurrence is not inferred from payload shape, `evidence_ref`, `focus_evidence_refs`, `already_visible_evidence_refs`, or `eligible_evidence_territory_refs`. Producer lineage and adapter lineage can establish clause ownership for testimony preservation, but that ownership is not Evidence occurrence and does not make a reference resolved Evidence.

### Does either side mistake an evidence identifier for resolved or admitted Evidence?

No current selected/inquiry/frontier witness examined here treats an evidence identifier as resolved canonical Evidence. The handoffs preserve reference identity, membership, evidence-quality labels, visible references, and eligible territory references without claiming resolved Evidence admission. The earlier Evidence Graph repair remains the actual-Evidence frontier: unresolved references must not count as admitted evidence support.

### Overall handoff classification

- Advancement-need reference to focus selection: **lawful asymmetry**, with caller-constructed representation risk preserved.
- Horizon evidence reference to inquiry testimony: **lawful asymmetry**, with snapshot/currentness compression and canonical Evidence Unknown preserved.
- Selected inquiry reference to boundary testimony: **exact lawful handoff** for selected reference identity; **lawful asymmetry** for newly supplied clause standing and ownership.
- Boundary testimony to bounded frontier: **exact lawful handoff** for clause artifacts, with frontier-local operative admission.
- Reference identifier to resolved Evidence: **Unknown**; no current downstream reliance requires resolution and no current witness proves resolution.

## Book projection decision

No Book update is warranted. The completed grammar already expresses the needed constitutional relations: availability, applicability, admission, and consumption are distinct; reference is not resolved Evidence; upstream admission is not downstream admission; and producer output standing is not consumer-local admission standing. The implementation witness fits inside that grammar and exposes no constitutional relation that the current grammar cannot express.

## Smallest lawful implementation frontier, if warranted

No implementation correction is warranted in this investigation. The smallest future frontier, only if a future task makes downstream selection or inquiry rely on Evidence currentness, source occurrence, producer authority, or resolved Evidence content, would be to add a responsibility-local check at that specific consumer boundary. This report does not prescribe classes, fields, routers, resolvers, admission engines, or pipelines.

## Focused tests run

The focused read-only witness checks were:

```text
pytest -q tests/test_advancement_need_reference_set.py tests/test_advancement_need_consideration_selection.py tests/test_inquiry_need_projection.py tests/test_inquiry_frontier_boundary_testimony.py tests/test_bounded_inquiry_frontier.py
```

Result: `25 passed in 2.00s`.
