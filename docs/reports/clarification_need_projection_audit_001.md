# Clarification Need Projection Audit 001

## Question

Determine what stage-owned evidence lawfully establishes that unresolved operator meaning prevents advancement across the current horizon:

```text
BoundedAdvancementHorizon
+
goal-owned operator-meaning evidence
→ ClarificationNeedProjection
```

Repository authority wins. This audit does not classify inquiry, authority, or operational-realization needs. It does not generate clarification questions, judge sufficiency, select a next action, authorize movement, execute, record, write the event ledger, or mutate state.

## Guardrails preserved

```text
unresolved material
!= clarification need

ambiguity
!= operator-owned ambiguity automatically

missing information
!= clarification need automatically

clarification need established
!= clarification requested
!= wording selected
!= inquiry opened
```

A lawful clarification projection must preserve operator-owned uncertainty only where an owning artifact already establishes that the uncertainty concerns operator meaning for the exact selected goal and current horizon. It must not convert repository/world unknowns, authority gaps, mechanism gaps, missing downstream artifacts, or generic unresolved material into clarification need.

## Evidence reviewed

- `seed_runtime/bounded_advancement_horizon.py`
- `tests/test_bounded_advancement_horizon.py`
- `seed_runtime/bounded_operator_goal_establishment.py`
- `seed_runtime/goal_inquiry_consideration_selection.py`
- `goal_advancement_need_evidence_topology_audit_001.md`
- `bounded_advancement_horizon_slice_001.md`

## Existing boundary now available

The repository now has a read-only `BoundedAdvancementHorizon` implementation. It preserves one selected goal identity, matching goal artifact identity, present movement boundary, scope bounds, evidence snapshots, relevant and excluded need-family coverage, Unknowns, conflicts, stale evidence, and unavailable evidence. Its boundary notes explicitly say the horizon is not need classification or sufficiency judgment, and that the horizon does not open inquiry, authorize, execute, record, or mutate state.

The tests prove the horizon requires a selected `GoalInquiryConsiderationSelection` and matching `BoundedOperatorGoalEstablishment`, preserves the present movement boundary and current bounds, preserves potential need-family coverage without classifying a need, carries stale/unavailable/Unknown/conflicting evidence, and exposes no action, authority, execution, recording, event-ledger, mutation, or sufficiency side effects.

Therefore the horizon can bind a projection to one selected bounded goal and current movement boundary, but it cannot itself establish clarification need. Its own `unknowns`, `conflicts`, stale evidence, or unavailable evidence are evidence-quality material, not clarification-family standing.

## Which existing artifacts may testify to operator-owned uncertainty?

### Primary testimony: `BoundedOperatorGoalEstablishment`

`BoundedOperatorGoalEstablishment` is the primary existing artifact that may testify to operator-owned uncertainty because it owns bounded operator goal establishment from lawful ingress evidence. The fields that may contain operator-owned uncertainty are:

- `establishment_state` and `establishment_reason`, when the state is provisional or refused because bounded operator orientation is not resolved;
- `intended_outcome` and `outcome_resolution`, when the goal's intended operator outcome is absent, only provisionally interpreted, or not supported by ingress;
- `known_scope` and `unresolved_scope`, when the unresolved scope concerns operator-facing goal boundary rather than repository facts;
- `sufficiency_conditions`, `sufficiency_state`, and `stop_conditions`, when the operator's acceptance, completion, or stop meaning is missing or unclear;
- `operator_acceptance_provenance`, when the current boundary requires provenance for accepted operator meaning and that provenance is absent or insufficient;
- `operator_constraints`, when stated operator constraints cannot be interpreted as movement boundaries;
- `unknowns`, `ambiguities`, `conflicts`, and `known_loss`, only when the owning context shows the unresolved matter belongs to operator meaning rather than repository/world investigation.

These fields may testify; they do not automatically establish clarification need. The projection must distinguish the field carrier from the family ownership of the uncertainty.

### Secondary testimony: `GoalInquiryConsiderationSelection`

`GoalInquiryConsiderationSelection` may testify to focus/selection-boundary uncertainty through `missing_identity_evidence_refs`, `ambiguous_goal_refs`, `unknowns`, and `conflicts`. That testimony can support a refusal or non-coverage for projection if exact selected-goal binding is not available.

Once the selection is in `selected` state and the horizon matches the goal artifact, selection-boundary uncertainty is not a license to reinterpret the goal. It remains selection evidence, not clarification need about the already selected goal, unless an owner explicitly binds it to the selected goal's operator meaning.

### Horizon testimony: `BoundedAdvancementHorizon`

`BoundedAdvancementHorizon` may testify to binding and coverage, not operator meaning. It contributes:

- exact selected-goal binding;
- matching goal artifact binding;
- `horizon_id`;
- `present_movement_boundary`;
- included/excluded scope;
- evidence snapshot refs and evidence quality;
- potentially relevant and explicitly excluded need families.

Its Unknowns and conflicts may show that projection coverage is unknown or conflicting. They do not alone establish clarification need because the horizon explicitly refuses need classification and sufficiency judgment.

## Evidence that binds uncertainty to the selected goal and horizon

A lawful `ClarificationNeedProjection` needs all of the following before it may say operator-owned uncertainty prevents advancement across the current horizon:

1. **Selection binding:** the `GoalInquiryConsiderationSelection.selection_state` is `selected`, with exactly one `selected_goal_establishment_id`.
2. **Goal artifact match:** the selected goal id equals `BoundedOperatorGoalEstablishment.goal_establishment_id`.
3. **Horizon binding:** the `BoundedAdvancementHorizon.horizon_state` is `bounded`, names the same selected goal id, and has a non-empty `present_movement_boundary`.
4. **Family coverage:** the horizon includes clarification as a potentially relevant need family or otherwise does not exclude clarification. If clarification is explicitly excluded, the projection standing for this horizon is `excluded_family`, not established clarification need.
5. **Owned operator-meaning evidence:** a stage-owned field on `BoundedOperatorGoalEstablishment`, or a stage-owned upstream record preserved by that artifact, identifies unresolved operator meaning, scope, acceptance, stop, constraint, ambiguity, conflict, or known loss as material to the current movement boundary.
6. **Materiality to advancement:** evidence links the unresolved operator-owned item to the horizon's `present_movement_boundary`, included scope, sufficiency/stop condition, accepted meaning, or current bounded movement. Generic uncertainty without this link is unsupported for clarification projection.
7. **Non-inquiry exclusion:** the unresolved item is not merely repository/world unknown, source evidence deficiency, observation gap, authority standing, or operational-realization gap. If it contains such components, those components must remain separate from the clarification component.

## Standing vocabulary

A projection should preserve standing separately from requested action. The following standings are sufficient for this boundary:

| Standing | Meaning | Lawful output implication |
| --- | --- | --- |
| `established` | Current bounded evidence shows unresolved operator-owned meaning is material to crossing this horizon. | Clarification need exists for this horizon; no question wording or request is selected. |
| `unsupported` | Some unresolved material exists, but evidence does not bind it to operator-owned meaning and the current horizon. | No clarification need is established from that item. |
| `unknown` | Evidence quality or ownership is unavailable, stale, or insufficient to determine whether the item is operator-owned or horizon-material. | Projection coverage is unknown; do not infer need. |
| `conflicting` | Stage-owned evidence conflicts about whether the uncertainty is operator-owned, material, current, or in scope. | Preserve conflict; do not collapse to established need. |
| `excluded_family` | Clarification family is out of scope for this horizon by explicit horizon exclusion or family boundary. | Do not classify the item as clarification need for this horizon. |

The standing names are not next-action states. `established` does not mean clarification was requested, wording was selected, inquiry was opened, or movement was authorized.

## Operator-owned uncertainty versus repository/world uncertainty

### Clarification need side

Operator-owned uncertainty may become clarification need when the unresolved item is about what the operator meant or accepted for this goal and when that unresolved operator meaning is material to the current boundary. Examples include:

- the selected goal's intended outcome is provisional because the operator expression admits multiple goal meanings;
- a scope phrase in the operator expression is unresolved and the horizon's movement boundary would cross that scope;
- sufficiency or stop conditions depend on operator acceptance that is absent or ambiguous;
- a stated operator constraint is preserved but cannot be interpreted enough to know the allowed movement boundary;
- known loss in ingress evidence removed operator wording required for the horizon.

### Inquiry need side

Repository/world uncertainty remains inquiry-family material when the unresolved item concerns facts, observations, support, source truth, current repository state, external world state, or evidence conflicts after the goal meaning is sufficiently bounded. Examples include:

- the operator meaning is clear, but repository evidence is missing;
- a source file, runtime fact, observation, or test result is unknown;
- two repository observations conflict;
- downstream support, reachability, or projection evidence is stale or unavailable;
- the question is whether a claim about the repository/world is true.

The same surface field, such as `unknowns` or `unresolved_scope`, may carry either family. The lawful distinction is not the field name; it is the owner, provenance, subject, and binding to the horizon.

## May one unresolved item contain both clarification and inquiry components?

Yes. One unresolved item may contain both components when the operator-facing phrase and repository/world fact are entangled. For example, “use the current storage topology” may require clarification of what the operator means by “storage topology” and inquiry into what the repository currently implements under that term.

The projection must split components rather than force one family label. The operator-meaning component may receive clarification standing if bound to the selected goal and horizon. The repository/world component must remain inquiry-family material and is outside this audit's classification scope.

## Does an existing owner already perform this projection?

No reviewed owner already performs `ClarificationNeedProjection`.

Adjacent owners exist:

- `BoundedOperatorGoalEstablishment` preserves bounded goal meaning and unresolved goal-owned evidence, but it does not project horizon-bound clarification need.
- `GoalInquiryConsiderationSelection` selects one visible bounded goal from exact focus evidence, but it refuses to require or open inquiry and does not classify clarification need.
- `BoundedAdvancementHorizon` binds a selected goal to a present movement boundary and preserves evidence quality, but it explicitly refuses need classification and sufficiency judgment.
- `goal_advancement_need_evidence_topology_audit_001.md` identifies clarification-family topology at the need-set level, but does not implement or own a specific clarification projection from goal-owned operator-meaning evidence.

## Smallest missing responsibility

The smallest missing responsibility is a read-only `ClarificationNeedProjection` owner that consumes:

```text
GoalInquiryConsiderationSelection(selected)
+
matching BoundedOperatorGoalEstablishment
+
BoundedAdvancementHorizon(bounded)
+
goal-owned operator-meaning evidence refs
```

and emits only:

- selected goal and horizon binding;
- the operator-owned uncertainty item refs considered;
- standing per item: `established`, `unsupported`, `unknown`, `conflicting`, or `excluded_family`;
- materiality evidence tying established items to the present movement boundary;
- excluded inquiry/authority/operational-realization components when present;
- non-authority, non-action, non-recording, non-mutation flags.

It must not infer clarification need from absent evidence, generic ambiguity, generic unresolved material, unknown repository facts, missing implementation route, downstream silence, or operator-visible wording alone.

## Is one read-only implementation slice warranted?

Yes, one narrow read-only implementation slice is warranted if Seed needs this projection to become executable after the now-implemented `BoundedAdvancementHorizon`. The slice should be smaller than a full `GoalAdvancementNeedSet` and should not introduce a diagnostic CLI surface unless explicitly requested.

A minimal slice would add:

- a `ClarificationNeedEvidenceRef` or equivalent input record declaring item subject, owner, family hint, materiality ref, and source artifact ref;
- a `ClarificationNeedProjection` dataclass with selected-goal id, horizon id, item standings, excluded components, and boundary flags;
- validation that selection, goal, and horizon identities match;
- validation that `established` requires an operator-meaning owner and materiality to the current horizon;
- tests proving unresolved material, generic ambiguity, missing repository information, excluded family, and mixed clarification/inquiry components are preserved without overclassification;
- tests proving no inquiry opening, wording selection, action selection, authorization, execution, recording, event-ledger write, or cluster mutation.

Because this would be a library artifact rather than a new diagnostic/audit CLI surface, the diagnostic inventory and diagnostic shape-audit registry do not need changes unless a public diagnostic surface is added.

## Exact next bounded question

```text
What is the minimal read-only `ClarificationNeedProjection` artifact that consumes one selected `GoalInquiryConsiderationSelection`, one matching `BoundedOperatorGoalEstablishment`, one bounded `BoundedAdvancementHorizon`, and explicit goal-owned operator-meaning evidence refs, preserves `established`, `unsupported`, `unknown`, `conflicting`, and `excluded_family` standings without requesting clarification or opening inquiry, and refuses to classify repository/world uncertainty, authority gaps, or operational-realization gaps as clarification need?
```

## Conclusion

Stage-owned clarification evidence must come primarily from `BoundedOperatorGoalEstablishment` fields and preserved upstream operator-meaning evidence, with `GoalInquiryConsiderationSelection` and `BoundedAdvancementHorizon` supplying exact selected-goal and horizon binding. The lawful boundary is not unresolvedness, ambiguity, or missing information. It is unresolved operator-owned meaning that is materially bound to the exact selected goal and current movement horizon.

The repository does not currently show an owner that performs this projection. The smallest missing responsibility is a read-only preservation and standing projection for goal-owned operator-meaning uncertainty, not an inquiry classifier, sufficiency judge, clarification requester, question writer, planner, authority requester, realization selector, executor, recorder, or state mutator.

Clarification need projection audit complete.
