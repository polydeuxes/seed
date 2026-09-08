# Inquiry Need Projection Audit 001

## Question

Determine what evidence lawfully establishes that unresolved repository, world, observation, or support knowledge prevents advancement across one exact bounded horizon:

```text
BoundedAdvancementHorizon
+
stage-owned repository/world uncertainty evidence
→ InquiryNeedProjection
```

Repository authority wins. This audit does not generate questions, establish an inquiry frontier, request authority, select observations or realizations, judge sufficiency, authorize, execute, record, write the event ledger, or mutate state.

## Guardrails preserved

```text
unknown fact
!= inquiry need automatically

missing evidence
!= inquiry need automatically

repository/world uncertainty
!= horizon-material uncertainty automatically

inquiry need established
!= inquiry opened
!= question selected
!= observation authorized
```

A lawful inquiry-need projection must establish more than unresolvedness. It must show that a stage-owned repository/world, observation, or support uncertainty is material to crossing the exact `BoundedAdvancementHorizon` for the selected bounded goal. Absent downstream artifacts, generic Unknowns, stale evidence, unresolved goal fields, missing implementation, and generic repository/world uncertainty remain preserved but do not automatically become inquiry need.

## Evidence reviewed

- `seed_runtime/bounded_advancement_horizon.py`
- `tests/test_bounded_advancement_horizon.py`
- `seed_runtime/bounded_operator_goal_establishment.py`
- `seed_runtime/goal_inquiry_consideration_selection.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/repository_observation.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/knowledge/observation_agreement.py`
- `seed_runtime/facts.py`
- `docs/state.md`
- `clarification_need_projection_audit_001.md`
- `goal_advancement_need_evidence_topology_audit_001.md`
- `operator_clarification_competency_assessment_audit.md`
- `docs/gap_classification_reconciliation.md`
- `docs/observation_interpretation_and_reality_reconciliation.md`

## Existing bounded-horizon boundary

`BoundedAdvancementHorizon` is the required binding input, not the need owner. Its implementation preserves one selected goal, the matching bounded goal artifact, the present movement boundary, included and excluded scope, evidence snapshots, stale and unavailable evidence references, relevant and excluded need families, Unknowns, conflicts, and explicit non-action flags.

The horizon implementation explicitly names the need-classification fields that it refuses to populate:

```text
clarification_need
inquiry_need
authority_need
operational_realization_need
sufficient_for_now
selected_next_action
```

It also carries boundary notes stating that the horizon is not need classification or sufficiency judgment, that included need family means potentially relevant rather than need existence, and that the horizon does not open inquiry, authorize, execute, record, or mutate state.

Therefore a lawful `InquiryNeedProjection` may consume the horizon for exact selected-goal and movement-boundary binding, but it may not treat the horizon's own Unknowns, conflicts, stale evidence, unavailable evidence, or relevant-family listing as established inquiry need.

## Which existing stage-owned artifacts may testify to repository/world uncertainty?

### Primary inquiry-family testimony

The strongest existing testimony sources are stage-owned artifacts whose responsibility is repository/world observation, knowledge extraction, support, or inquiry-artifact visibility.

| Artifact or owner | What it may testify | Boundary for this audit |
| --- | --- | --- |
| `EvidenceSnapshotReference` inside `BoundedAdvancementHorizon` | A named evidence reference, snapshot reference, evidence state, and notes at the current horizon. | Binds evidence quality to a horizon but does not classify need. |
| `stale_evidence_refs` and `unavailable_evidence_refs` on `BoundedAdvancementHorizon` | Evidence quality problems preserved for the current horizon. | May support `unknown` or `unsupported`; establishes inquiry need only when a stage owner says the missing/stale evidence is horizon-material. |
| `seed_runtime/repository_observation.py` `RepositoryObservation` | Repository path, VCS, head commit, branch, dirty state, changed counts, remote presence, and whether status is available. | Repository-state observation; not a question, authority request, or realization selector. |
| `seed_runtime/knowledge/repository_observation.py` | Deterministic repository artifact facts extracted from caller-provided source text. | Testifies to repository artifact structure only inside its adapter boundary. |
| `seed_runtime/knowledge/documentation_observation.py` | Documentation claims from caller-provided markdown/text. | Documentation testimony, not implementation truth by itself. |
| `seed_runtime/knowledge/relationship_observation.py` | Explicit relationship facts supplied to the relationship observation owner. | Relationship testimony from explicit input, not repository scanning or semantic inference. |
| `seed_runtime/knowledge/observation_agreement.py` | Agreement or disagreement among documentation, repository, and relationship observations. | Support/agreement testimony; does not mutate ledgers or promote truth automatically. |
| `seed_runtime/facts.py` and projected state documentation | Event-derived facts, support summaries, unsupported facts, confidence, contradiction, and current projected state. | Support and current-world model testimony; confidence is not truth and unsupported facts are not automatic inquiry need. |
| `seed_runtime/inquiry_artifacts.py` | Visibility of unknown, boundary, pressure, finding, supported conclusion, unsupported conclusion, open question, and gap artifacts. | Visibility testimony only; explicitly not inquiry movement, graph creation, pressure transformation, workflow, or planning. |

### Secondary binding testimony

`GoalInquiryConsiderationSelection` and `BoundedOperatorGoalEstablishment` may supply the selected goal identity, source reference, ingress lineage, goal scope, unresolved scope, sufficiency conditions, stop conditions, Unknowns, ambiguities, conflicts, and known loss. For inquiry need, these fields are not enough by themselves. They become relevant only when the unresolved component concerns repository/world knowledge rather than operator meaning, authority, or realization and when another stage-owned owner binds that component to the horizon.

### Non-testimony for inquiry need

The following do not lawfully establish inquiry need by themselves:

- a generic `unknowns` field;
- a stale evidence reference without horizon-materiality evidence;
- an unavailable evidence reference without a stage-owned explanation of what advancement it blocks;
- an unresolved goal field that concerns operator meaning;
- pressure, concern, or presentation vocabulary;
- an unsupported conclusion with no selected-goal and horizon binding;
- a missing implementation route;
- absence of an inquiry, question, observation, realization, answer, test, or diagnostic artifact.

## What binds testimony to the selected goal and horizon?

A lawful `InquiryNeedProjection` must preserve all of the following bindings before it can emit `established` for inquiry need:

1. **Selection binding.** `GoalInquiryConsiderationSelection.selection_state` is `selected` and names exactly one `selected_goal_establishment_id`.
2. **Goal artifact match.** The selected goal id matches the consumed `BoundedOperatorGoalEstablishment.goal_establishment_id`.
3. **Horizon binding.** `BoundedAdvancementHorizon.horizon_state` is `bounded`, names the same selected goal, and has a non-empty `present_movement_boundary`.
4. **Family coverage.** Inquiry is potentially relevant for the horizon or at least not explicitly excluded. If inquiry is explicitly excluded, inquiry standing is `excluded_family`.
5. **Stage-owned uncertainty evidence.** The uncertainty comes from an owner allowed to testify about repository/world, observation, or support standing.
6. **Subject binding.** The uncertainty names or references a repository/world subject, observation target, support relationship, evidence snapshot, fact, claim, source, or agreement comparison that participates in the selected goal's current boundary.
7. **Materiality binding.** A stage-owned record or explicit projection input ties the unresolved subject to the horizon's `present_movement_boundary`, included scope, current-state bounds, evidence snapshot refs, sufficiency/stop condition, or current bounded movement.
8. **Family separation.** Clarification, authority, and realization components are excluded or preserved separately rather than collapsed into inquiry need.

The binding rule is intentionally strict: repository/world uncertainty is inquiry-family material only when it is materially required for crossing the current bounded horizon. Otherwise it remains a preserved Unknown, unsupported item, stale evidence note, unavailable evidence note, or adjacent-family component.

## Boundary between inquiry need and adjacent families

### Inquiry need

Inquiry need concerns unresolved repository/world, observation, or support knowledge that blocks advancement across the exact horizon. Examples that may establish inquiry need if horizon-materiality is explicit:

- a repository fact required by the present movement boundary is unknown, contradicted, or unsupported;
- a documentation claim must be compared with repository implementation before the selected goal can advance;
- an observation source is unavailable for a fact that the horizon explicitly requires;
- evidence snapshots disagree about a support relationship that the current movement boundary depends on;
- current repository state is unavailable where the horizon's current-state bounds require it.

### Operator clarification

Operator clarification concerns unresolved operator-owned meaning, acceptance, scope, constraints, or stop conditions. The existing clarification audit identifies `BoundedOperatorGoalEstablishment` as the primary testimony owner for this family. If the missing piece is what the operator meant, accepted, or intended for this selected goal, the component belongs to clarification, not inquiry.

### Authority deficiency

Authority deficiency concerns whether Seed is allowed, authorized, or adopted to rely on, observe, mutate, use a provider, cross a boundary, or proceed. A missing authority grant or adoption decision is not inquiry need merely because it is unresolved. It may block action, but its owner is authority/adoption/policy, not repository/world knowledge projection.

### Operational-realization deficiency

Operational-realization deficiency concerns whether an implementation mechanism, invocation contract, grammar, dependency, representation, method, or behavior exists and can realize a capability. Candidate-realization surfaces preserve supported, unsupported, unknown, and conflict standings for mechanisms. No known realization, missing mechanism evidence, unavailable dependency, or representation incompatibility is not inquiry need unless the immediate horizon is specifically to know a repository/world fact rather than to select or execute a mechanism.

### Generic Unknown

Generic Unknown is the lawful preservation result when the subject, owner, family, currentness, or materiality cannot be established. Unknown is not false, not failure, not action pressure, and not inquiry need. It may later become inquiry-family evidence if a stage-owned artifact binds it to a selected goal and horizon.

## Standing preservation

A read-only projection should preserve item-level standing independently from any next action:

| Standing | Meaning | Required preservation |
| --- | --- | --- |
| `established` | Stage-owned repository/world, observation, or support uncertainty is bound to the selected goal and material to crossing this horizon. | Preserve the evidence refs, materiality refs, subject, horizon id, and excluded adjacent components; do not open inquiry or select a question. |
| `unsupported` | Uncertainty exists, but evidence does not establish inquiry-family ownership or horizon materiality. | Preserve why the item failed binding without converting it to generic need. |
| `unknown` | Current evidence is unavailable, stale, incomplete, or insufficient to determine family ownership or materiality. | Preserve evidence-quality limits and refuse promotion. |
| `conflicting` | Stage-owned evidence conflicts about subject, currentness, support, family ownership, selected-goal binding, or materiality. | Preserve conflict; do not choose a winner or establish need. |
| `excluded_family` | Inquiry family is explicitly excluded by the horizon or the item belongs to clarification, authority, or realization only. | Preserve the family exclusion and reason. |

These standings are not lifecycle states. `established` means only that inquiry need exists for the horizon. It does not mean inquiry opened, question selected, observation authorized, support judged sufficient, realization selected, or work authorized.

## Mixed-component separation

One unresolved item may contain multiple components. The projection must split rather than collapse them.

Example:

```text
"Use the current storage topology to decide whether the migration path is safe."
```

Possible components:

- operator clarification: what the operator means by `storage topology` or `safe` if those are operator-owned criteria;
- inquiry: what the repository currently implements or observes as storage topology;
- authority: whether Seed is authorized to inspect a host, external system, provider, or protected file;
- realization: whether a mechanism exists to perform the required observation or comparison.

A lawful projection may establish inquiry need only for the repository/world knowledge component that is materially bound to the horizon. The other components must be preserved separately as clarification, authority, realization, unknown, conflicting, unsupported, or excluded-family material.

## Does an existing owner already perform this projection?

No reviewed owner already performs `InquiryNeedProjection`.

Adjacent owners exist, but each stops earlier or belongs to another family:

- `GoalInquiryConsiderationSelection` selects one visible bounded goal for inquiry consideration from exact focus evidence, while refusing inquiry opening, authority, execution, recording, event-ledger writes, and mutation.
- `BoundedOperatorGoalEstablishment` establishes or refuses a bounded goal and preserves unresolved scope, Unknowns, ambiguities, conflicts, lineage, sufficiency conditions, and stop conditions, while refusing inquiry opening, resource observation, work authorization, execution, recording, satisfaction judgment, event-ledger writes, and mutation.
- `BoundedAdvancementHorizon` binds the selected goal to a present movement boundary and preserves potential need-family coverage, evidence quality, Unknowns, and conflicts, while explicitly refusing need classification and sufficiency judgment.
- Repository and knowledge observation owners testify to repository/documentation/relationship facts and observation agreement, but they do not consume a selected goal plus horizon to project a need.
- `InquiryArtifactVisibility` exposes inquiry artifact categories and limitations, but its boundary refuses inquiry movement, inquiry graph creation, pressure transformation, workflow, and planning.
- Clarification projection audit recovers a clarification-family boundary, not inquiry-family repository/world knowledge projection.
- Authority and operational-realization owners preserve their own standings and must not be imported into inquiry need by analogy.

## Smallest missing responsibility

The smallest missing responsibility is a read-only `InquiryNeedProjection` owner that consumes:

```text
GoalInquiryConsiderationSelection(selected)
+
matching BoundedOperatorGoalEstablishment
+
BoundedAdvancementHorizon(bounded)
+
explicit stage-owned repository/world uncertainty evidence refs
```

and emits only:

- selected-goal id and source binding;
- horizon id and present movement boundary;
- uncertainty items considered;
- item subject and source owner;
- item family classification or exclusion;
- item standing: `established`, `unsupported`, `unknown`, `conflicting`, or `excluded_family`;
- materiality refs tying established items to the present movement boundary, current-state bounds, evidence snapshot refs, included scope, sufficiency/stop conditions, or current bounded movement;
- separated clarification, authority, and realization components;
- read-only/non-action flags.

It must not infer inquiry need from absent downstream artifacts, generic Unknowns, stale evidence, unresolved goal fields, missing implementation, pressure vocabulary, missing authority, missing realization, or the mere fact that inquiry would be useful.

## Is one read-only implementation slice warranted?

Yes, one narrow read-only implementation slice is warranted if Seed needs the boundary to become executable after `BoundedAdvancementHorizon` and the clarification-family projection audit. The slice should be smaller than inquiry opening, question selection, observation selection, or a full goal-advancement need set.

A minimal slice would add:

- an explicit `InquiryNeedEvidenceRef` input record with fields such as `evidence_ref`, `source_artifact_ref`, `source_owner`, `subject_ref`, `uncertainty_kind`, `family_hint`, `materiality_ref`, `material_to_horizon`, `standing_hint`, and `excluded_components`;
- an `InquiryNeedProjection` dataclass with selected-goal id, horizon id, item standings, materiality refs, separated adjacent-family components, Unknowns, conflicts, and boundary flags;
- validation that selection, goal, and horizon identities match;
- validation that `established` requires inquiry-family ownership and materiality to the current horizon;
- preservation of `unsupported`, `unknown`, `conflicting`, and `excluded_family` without promotion;
- tests proving generic unknowns, missing evidence, stale evidence, repository uncertainty, excluded inquiry family, authority gaps, realization gaps, and mixed clarification/inquiry components do not overclassify;
- tests proving no inquiry opening, question selection, observation authorization, sufficiency judgment, realization selection, authority request, execution, recording, event-ledger write, or cluster mutation.

Because this would be a library/read-model artifact rather than a public diagnostic CLI surface, it need not update diagnostic inventory or diagnostic shape-audit registries unless a diagnostic surface is added.

## Exact next bounded question

```text
What is the minimal read-only `InquiryNeedProjection` artifact that consumes one selected `GoalInquiryConsiderationSelection`, one matching `BoundedOperatorGoalEstablishment`, one bounded `BoundedAdvancementHorizon`, and explicit stage-owned repository/world uncertainty evidence refs, preserves `established`, `unsupported`, `unknown`, `conflicting`, and `excluded_family` standings without opening inquiry, selecting a question, authorizing observation, requesting authority, selecting realization, judging sufficiency, recording, or mutating state, and refuses to classify operator clarification, authority deficiency, operational-realization deficiency, generic Unknown, stale evidence, missing implementation, or absent downstream artifacts as inquiry need?
```

## Conclusion

Inquiry need is lawfully established only when stage-owned repository/world, observation, or support uncertainty is explicitly bound to one selected bounded goal and is material to crossing one exact `BoundedAdvancementHorizon`. Unknown facts, missing evidence, stale evidence, repository/world uncertainty, and unsupported conclusions remain non-promoted unless an owning artifact supplies horizon-materiality evidence.

No reviewed owner currently performs this projection. The smallest missing responsibility is a read-only preservation and standing projection for horizon-material repository/world uncertainty, with explicit separation from operator clarification, authority deficiency, operational-realization deficiency, and generic Unknown.

Inquiry need projection audit complete.
