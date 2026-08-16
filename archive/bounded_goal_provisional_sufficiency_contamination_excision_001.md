# Bounded goal provisional/sufficiency contamination excision 001

## Deleted district

This excision removes the goal-local split that treated lawful non-refused ingress with empty caller-supplied sufficiency conditions as `provisional` and lawful non-refused ingress with nonempty caller-supplied sufficiency conditions as `established`.

## Constitutional warrant for deletion

Current canonical grammar distinguishes construction from establishment, but it warrants bounded operator goal standing through admitted or lawfully bound operator meaning, scope, provenance, boundedness, and a responsible local establishment act. It does not warrant `ProvisionalBoundedGoal`, caller-supplied sufficiency tuple promotion, tuple absence downgrade, or a mirrored `sufficiency_state` as constitutional standing.

## Production changes

`BoundedOperatorGoalEstablishment` no longer carries `sufficiency_conditions` or `sufficiency_state`. The closed-choice and admitted-interpretation producers no longer accept caller-supplied `sufficiency_conditions`, no longer include sufficiency tuples in stable identity payloads, and no longer emit `provisional` for otherwise lawful ingress. Passing ingress now emits the surviving truthful `established` bounded-goal standing; failing ingress still emits local `refused` standing.

## Tests deleted or rewritten

Focused bounded-goal tests were rewritten so they no longer supply sufficiency tuples to establish standing. New assertions prove tuple absence still establishes lawful closed-choice and admitted-interpretation ingress, tuple presence is rejected rather than promoted, serialized runtime output contains no `sufficiency_conditions` or `sufficiency_state`, and runtime goal output contains no `provisional` standing.

## Surviving bounded-goal establishment road

The surviving road is lawful `ClosedChoiceSelectionBinding` ingress or exact `DownstreamInterpretationAdmission` ingress plus bound/admitted operator meaning, known scope where available, preserved provenance and lineage, bounded local validation, and the negative-authority/read-only flags already carried by the artifact.

## Surviving refusal behavior

Closed-choice ingress remains refused when no bound option supports bounded orientation. Admitted-interpretation ingress remains refused for consumer or purpose mismatch, selection/projection/candidate identity mismatch, unadmitted interpretation, inapplicable projection, unknown upstream lineage, conflicting upstream lineage, or missing selected meaning identity.

## Consumer compatibility changes

No replacement horizon taxonomy was introduced. Direct consumers continue to consume the surviving bounded-goal establishment testimony and still refuse `establishment_state == "refused"`; there is no longer a `provisional` non-refused state for them to accept as compatibility vocabulary.

## Remaining uses of provisional

Active runtime production under `seed_runtime/` has no remaining `provisional` occurrence. Focused tests mention `provisional` only to prove it is absent from runtime goal output. Other surviving occurrences are historical reports, Book/report testimony outside this narrow runtime split, or independent English use unrelated to the deleted goal-local standing switch.

## Remaining uses of sufficiency_conditions

Active runtime production under `seed_runtime/` has no remaining `sufficiency_conditions` occurrence. Focused tests mention `sufficiency_conditions` only to prove the removed caller argument is rejected and the serialized fields are absent. Other surviving occurrences are historical reports or audit testimony about the removed or unrelated sufficiency vocabulary.

## Remaining uses of sufficiency_state

Active runtime production under `seed_runtime/` has no remaining `sufficiency_state` occurrence. Focused tests mention `sufficiency_state` only to prove the serialized field is absent. Other surviving occurrences are historical reports or audit testimony.

## Book amendments

The active construction/establishment chapter was amended only to state that the Book does not recognize caller-supplied sufficiency tuple presence or absence as a separate provisional/established bounded-goal standing split.

## Reports left unchanged

Historical reports and archived/audit testimony were not edited to remove chronology-preserving references to the deleted split.

## Checks performed

- `pytest -q tests/test_bounded_operator_goal_establishment.py`
- `pytest -q tests/test_bounded_operator_goal_establishment.py tests/test_bounded_advancement_horizon.py tests/test_clarification_need_projection.py tests/test_inquiry_need_projection.py tests/test_authority_need_projection.py tests/test_operational_realization_need_projection.py`
- `rg "provisional|sufficiency_conditions|sufficiency_state" -n .`
- `git diff --check`

## Strongest Unknowns

Whether historical Book-adjacent reports should eventually be superseded by a broader canonical reconciliation remains outside this bounded excision. No new sufficiency subsystem, acceptance stage, construction artifact, or horizon characterization is proposed here.
