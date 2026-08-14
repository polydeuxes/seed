# Shared Explanation Membership-to-Presentation Admission Topology Audit 001

## Bounded question

Does `membership_state == belongs` in `SharedExplanationMembershipEvidenceSet` directly admit a shared explanation rendering projection to later presentation sequencing, or does Seed require a separate bounded presentation-eligibility responsibility?

## Executive finding

`membership_state == belongs` does **not** directly admit a rendering projection to later presentation sequencing.

Repository evidence supports this topology:

```text
SharedExplanationRenderingProjection
  -> SharedExplanationMembershipEvidenceProjection
  -> SharedExplanationMembershipEvidenceSet
  -> missing separate presentation-eligibility/admission boundary
  -> later sequencing/composition/ranking/rendering owners, if implemented
```

The current membership owner answers only whether explicit preserved lineage ties a candidate rendering projection to one bounded inquiry or demand. It does not select, rank, deduplicate, sequence, compose, authorize, execute, create handoffs, or mutate state. The set owner mechanically partitions already-produced membership states and preserves duplicate occurrences; it also refuses completeness claims. Therefore a projection may belong to the inquiry while still not being admitted to this presentation.

## Evidence reviewed

### Shared rendering projection

`SharedExplanationRenderingProjection` is a read-only display projection over exactly one stage-owned explanation. Its `single_explanation_boundary` says it does not compare, aggregate, order, or compose explanations. Its `rendering_boundary` says shared field names are display labels only and constitutional meaning remains with the source stage.

This makes rendering projection a common presentation-compatible shape, not presentation admission.

### Membership evidence projection

`project_shared_explanation_membership_evidence(...)` consumes one bounded inquiry reference, one rendering projection, and explicit preserved lineage evidence. Its docstring forbids lookup and semantic membership inference from shared wording, source state, stage, or explanation text.

Its states are limited to:

```text
belongs
does_not_belong
unknown
conflict
```

Its output has `evidence_input_boundary` and `non_selection_boundary`. The non-selection boundary expressly says it produces one per-candidate evidence result only and does not select, rank, deduplicate, sequence, compose, authorize, execute, create handoffs, or mutate state.

Tests preserve the required distinctions:

- matching explicit inquiry lineage produces `belongs`;
- positive lineage to another incompatible inquiry can produce `does_not_belong`;
- missing lineage remains `unknown`, not non-membership;
- matching lineage plus incompatible references produces `conflict`;
- duplicate source identities remain visible and are not deduplicated;
- shared state wording or stage does not establish membership;
- the projection writes no events, mutates no cluster, and exposes no selected candidate.

### Membership evidence set

`build_shared_explanation_membership_evidence_set(...)` consumes one bounded inquiry reference and supplied membership evidence records. It validates the inquiry and demand references, then partitions the supplied records mechanically by membership state.

Its `completeness_claim` is explicitly `none; supplied collection only`. Its `non_selection_boundary` says it does not select rendering projections, rank, sequence, compose, deduplicate, infer semantic relevance, fabricate missing Unknowns, create handoffs, authorize, execute, write events, or mutate.

Tests show that:

- the set preserves every supplied result;
- duplicate candidate and source-identity occurrences remain visible;
- state partitions are mechanical over existing states only;
- empty and partial collections fabricate no Unknowns;
- the set exposes no `selected_rendering_projections` field.

The set therefore preserves membership evidence and collection visibility, not admission.

### Constitutional view selection precedent

Constitutional view selection is a separate implemented selection boundary. It consumes deterministic question and capability projections, performs exact key comparison, preserves unsupported uncertainty, and outputs registered view names. Its boundaries explicitly refuse raw question consumption, immutable view consumption, semantic reasoning, ranking, heuristics, planning, orchestration, evidence discovery, constitutional recovery, repository mutation, event-ledger writes, and cluster mutation.

This precedent matters because it shows that when Seed admits a view-like projection to composition, the admission/selection responsibility is explicit and bounded. Selection is not silently inherited from projection membership or renderability.

### Constitutional composition precedent

The selected constitutional views adapter wires a selection artifact into a composition request. Composition receives `requested_views`; it is not handed all compatible or belonging projections by default. Existing tests prove selected registered views wire directly into composition, while unsupported keys remain uncertainty.

This supports the distinction:

```text
projection can be compatible or related
!= selected/requested/admitted for this composition
```

### Question-family eligibility precedent

Question surface inventory and bounded ask dispatch distinguish an exact known family from bounded dispatch eligibility. A family can be known, diagnostic-only, eligible with parameters, eligible now, or not dispatchable. Exact inventory presence is not the same as execution or answer composition.

This is adjacent precedent for the same shape of responsibility: repository-visible membership/registration is weaker than presentation or dispatch admission.

## Required distinctions preserved

### `belongs to inquiry != admitted to this presentation`

`belongs` means explicit positive lineage ties the candidate to the bounded inquiry or demand. It does not mean the candidate has been admitted under a requested presentation purpose, output format, budget, requested role, conflict policy, duplicate policy, audience, stage policy, or composition contract.

### `not admitted != does_not_belong`

A belonging projection can fail admission for presentation-local reasons without becoming a non-member. Examples of lawful non-admission reasons include:

- presentation purpose excludes that explanation role;
- requested presentation asks for summary only, not supporting-stage detail;
- output format or budget cannot include all belonging projections;
- conflict policy preserves conflict visibility but withholds conflict-bearing projections from sequencing;
- duplicate policy admits one representative while keeping duplicate occurrences visible;
- downstream composition contract accepts only certain registered projection kinds;
- required admission evidence is Unknown.

None of those facts prove that the projection does not belong to the inquiry.

### `admitted to sequencing != first in encounter order`

Admission would only mean the projection is eligible to enter a later sequencing/composition owner. It would not decide first position, encounter order, rank, priority, grouping, deduplication, or narrative order. Sequencing is a downstream responsibility.

### `presentation selection != ranking blockers`

Admission can decide whether a projection may participate in the requested presentation. Ranking blockers decide whether relative order or priority can be computed. A projection could be admitted with ranking Unknown, or not admitted for presentation-local reasons while ranking evidence remains irrelevant.

## Who owns presentation admission?

No current implementation owner lawfully owns shared-explanation presentation admission.

The closest existing owners are intentionally narrower:

| Owner | Owns | Does not own |
| --- | --- | --- |
| `SharedExplanationRenderingProjection` | single explanation display-compatible projection | comparison, aggregation, ordering, composition, admission |
| `SharedExplanationMembershipEvidenceProjection` | per-candidate inquiry membership evidence from explicit lineage | selection, ranking, sequencing, composition, deduplication, admission |
| `SharedExplanationMembershipEvidenceSet` | supplied collection preservation and state partitions | selecting/admitting rendering projections, completeness, semantic relevance, deduplication |
| Constitutional View Selection | registered constitutional view selection by exact keys | shared explanation projection admission |
| Constitutional View Composition | composition of explicitly requested/selected registered constitutional views | shared explanation eligibility over membership evidence sets |
| Question-family eligibility/dispatch | exact question family eligibility and dispatch to existing surfaces | shared explanation presentation admission |

Therefore, if Seed needs to move from membership evidence to presentation sequencing, the lawful owner would be a new bounded presentation-eligibility/admission responsibility, not the existing membership set.

## Does a separate eligibility boundary exist?

As an implemented artifact: **No.** No inspected shared-explanation artifact has fields such as admitted projection refs, admission state, requested presentation purpose, requested explanation roles, output budget, admission reasons, non-admitted belonging refs, ranking-blocker separation, or sequencing handoff.

As an architectural requirement before sequencing: **Yes.** The boundary is required by existing negative evidence. Membership objects explicitly refuse selection, ranking, sequencing, composition, and deduplication. Constitutional selection precedent shows admission must be explicit when presentation/composition consumes selected items.

## What evidence may lawfully affect admission?

A future presentation-admission owner may lawfully consume only bounded, preserved evidence relevant to this presentation request. Based on current repository patterns, lawful inputs include:

1. The `SharedExplanationMembershipEvidenceSet`, including all membership states, reasons, Unknowns, conflicts, duplicate occurrence records, collection-partial status, and completeness claim.
2. The bounded inquiry and bounded demand references.
3. An explicit requested-presentation artifact or equivalent local request, including purpose, audience/surface, output format, requested explanation roles, and any budget or scope constraints.
4. Source-stage preservation metadata already carried by rendering projections: source artifact owner, explanation type, source state/reason, preserved Unknowns, preserved conflicts, prohibited downstream movement, explanation boundary, and stage-owned material.
5. Registered presentation/composition capability constraints, if such constraints already exist in the consuming surface.
6. Explicit policy for conflict treatment, Unknown treatment, duplicate treatment, supporting-stage inclusion, and non-selected visibility.

Evidence that may not lawfully affect admission without a separate owner includes semantic similarity of wording, unstated source-stage assumptions, raw explanation text inference, ranking heuristics, authorization/execution concerns, or treating presentation vocabulary as repository knowledge.

## Handling non-members, Unknowns, conflicts, duplicates, and belonging-but-unadmitted projections

A lawful admission boundary must preserve visibility as follows:

| Case | Visibility rule |
| --- | --- |
| `does_not_belong` | Remain visible as non-member membership evidence. Do not admit as a member, and do not use non-admission to create new non-membership. |
| `unknown` | Remain visible as Unknown membership evidence. Do not coerce Unknown to `does_not_belong`; do not fabricate missing Unknowns beyond supplied evidence. |
| `conflict` | Remain visible with conflicting references. Admission may be blocked, allowed with caveat, or routed to a conflict section only if explicit presentation policy says so. |
| Duplicate candidate/source identities | Preserve occurrences and duplicate refs. Deduplication, if any, must be separate from admission and must leave duplicate visibility. |
| `belongs` but not admitted | Remain visible as belonging-but-unadmitted with an admission reason, without changing membership state. |
| Collection partial/empty | Preserve collection-partial and no-completeness-claim facts. Do not treat absence from the supplied set as non-membership or non-admission unless the presentation request explicitly scopes the supplied universe. |

## Supporting-stage preservation and explanation roles

Rendering projections preserve source-stage owned material and boundaries. Membership evidence preserves whether explicit lineage ties that rendered projection to the inquiry. Neither owner decides whether a presentation asked for that role.

A future admission owner must distinguish at least:

```text
source explanation role preserved by stage
!= role requested for this presentation
!= eligible for presentation sequencing
```

For example, an explanation may belong to the inquiry as supporting-stage preservation while the requested presentation admits only a constitutional process overview. That non-admission would be presentation-local, not a membership denial.

## Requested presentation and constitutional view selection

Existing constitutional selection shows a strong pattern: requested presentation or view selection must be explicit and deterministic enough for a bounded owner. Selection consumes projected keys and capability projections; composition consumes selected names. It does not infer requested views from all available constitutional material.

Shared explanation presentation admission should follow that discipline if implemented. It should not use `belongs_results` as an implicit selected list.

## Unknowns, conflicts, and duplicates do not become ranking blockers by default

Membership Unknowns, conflicts, and duplicates are admission evidence and visibility obligations. They are not automatically sequencing/ranking blockers. A future owner must separately say whether each condition:

- blocks admission;
- admits with caveat;
- admits to a special section;
- remains visible only in non-admitted evidence;
- requires downstream sequencing to preserve a ranking Unknown.

Without that explicit policy, the safe current conclusion is no admission.

## Is one implementation slice warranted?

Yes, one narrow implementation slice is warranted **if and only if** Seed needs to hand shared explanation rendering projections from membership evidence into a requested presentation sequence.

The slice should be limited to a read-only admission artifact, for example `SharedExplanationPresentationEligibilitySet`, that:

- consumes one `SharedExplanationMembershipEvidenceSet` and one explicit requested-presentation reference;
- preserves `belongs`, `does_not_belong`, `unknown`, and `conflict` partitions unchanged;
- emits admitted projection references, non-admitted belonging projection references, and admission Unknowns/conflicts;
- records admission reasons without changing membership states;
- preserves duplicate occurrence visibility without deduplicating;
- does not sequence, rank, compose, authorize, execute, mutate state, or write events;
- keeps `admitted_to_sequencing` distinct from encounter order and ranking.

No implementation should be done in this audit.

## Exact next bounded question

```text
For one explicit requested shared-explanation presentation, which membership-belonging rendering projections are eligible to enter presentation sequencing, with non-admitted belonging projections, Unknowns, conflicts, duplicates, and non-members preserved, without sequencing, ranking, composition, deduplication, authorization, execution, event-ledger writes, or cluster mutation?
```

## Conclusion

`membership_state == belongs` is necessary evidence for presentation admission only if a future presentation-admission policy requires membership, but it is not sufficient and does not itself admit a projection to sequencing.

The repository currently has membership preservation and membership-set visibility, not shared-explanation presentation admission. The first missing responsibility is a bounded read-only presentation eligibility/admission owner that consumes membership evidence plus an explicit requested-presentation boundary and preserves all non-admitted and uncertain material without changing membership truth.

Shared explanation membership-to-presentation admission topology audit complete.
