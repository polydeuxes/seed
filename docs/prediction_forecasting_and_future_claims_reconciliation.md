# Prediction, Forecasting, And Future Claims Reconciliation

## Purpose

This document performs a documentation-only reconciliation of prediction,
forecasting, future claims, expectations, projections of possible futures,
uncertainty, scenario generation, and future-oriented reasoning.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify
observations, evidence handling, claims, events, projections,
recommendations, decisions, authority systems, federation behavior, learning
behavior, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established that Seed is claim-centric, facts are
normalized claim forms, events preserve history, changes preserve transitions,
learning changes understanding without erasing history, contradiction existence
is distinct from contradiction discovery, recommendations are advisory,
decisions are distinct from commands, and goals remain operator-owned.

Seed now has architectural treatment for past knowledge, present selection,
historical preservation, contradiction handling, learning, reinterpretation,
recommendation relevance, and decision authority.

The remaining question is:

```text
How should Seed reason about claims concerning the future?
```

Examples:

```text
Disk will fill within 7 days.
Service outage risk is increasing.
This recommendation is likely to reduce downtime.
Host replacement will improve reliability.
This federation link may become stale.
Traffic is expected to increase next month.
```

## Central Finding

Future-oriented reasoning should remain claim-centric and support-preserving,
but it must not be mistaken for observation of the future.

The safest architectural definition is:

```text
A future claim is an evidence-backed, provenance-bearing claim about a possible,
expected, conditional, planned, or otherwise future state, event, transition,
consequence, or outcome, evaluated relative to an explicit time horizon and
support context.
```

A prediction is a future claim that asserts a possible or expected future state,
event, transition, or outcome. A forecast is a structured forecasting result that
may aggregate, compare, or summarize multiple future claims across time,
scenarios, assumptions, confidence levels, or models. A scenario is a coherent
possible-future frame used for reasoning, not a commitment and not necessarily a
prediction. A recommendation may rely on future claims, but the prediction ends
where advisory response selection begins. A plan records intended or selected
future action; it is not a future fact and not proof that the planned state will
occur.

The useful chain is:

```text
Observation / Evidence / Historical Claim
  -> Current-State Claim
  -> Trend / Causal / Assumption Support
  -> Future Claim
  -> Consequence
  -> Goal Relevance
  -> Recommendation
  -> Decision
  -> Plan / Command / Action
```

The shorter operational shorthand is:

```text
Observations preserve what was observed.
Historical claims preserve what was claimed about the past.
Current-state claims describe selected present understanding.
Future claims describe possible or expected later conditions.
Consequences explain what could result.
Recommendations advise what to consider.
Decisions select.
Plans intend.
Commands request execution.
Actions change reality.
```

Future claims remain revisable. If a prediction later fails, Seed should
preserve both the historical existence of the prediction and the historical
support that justified it at the time. The later outcome may weaken, contradict,
calibrate, or reinterpret the prediction, but it does not erase the fact that the
prediction existed, was supported by particular evidence, and was made under
particular assumptions.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/claim_support_characterization.md`
- `docs/claim_support_frontier.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/event_and_change_reconciliation.md`
- `docs/learning_and_knowledge_change_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/goal_relevance_and_recommendation_generation_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/cross_seed_provenance_and_federation_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/invariants.md`

## Boundary Summary

| Concept | Primary role | Answers | Must not become |
| --- | --- | --- | --- |
| Observation | Captures an input or external signal at an observation time | What was observed by this source? | Future fact, prediction, recommendation |
| Historical claim | Preserves a claim about a past state, event, or transition | What was claimed about the past? | Current selected truth, prediction |
| Current-state claim | Describes selected present understanding under support and freshness rules | What appears to be true now? | Live certainty, future guarantee |
| Future claim | Claims something about a possible later state, event, transition, consequence, or outcome | What may, is expected to, or is projected to happen? | Observation, commitment, plan, command |
| Prediction | Future claim asserting a possible or expected future condition | What is predicted under this support and horizon? | Observation, recommendation, decision |
| Forecast | Structured aggregation or time-indexed set of future claims | What future trajectory or distribution is forecast? | Commitment, plan, policy |
| Expectation | A stance that a future or current claim is anticipated, often from support, assumptions, or model output | What does Seed or an imported source expect? | Truth, confidence, trust, probability |
| Scenario | Coherent possible-future frame for reasoning under assumptions | What future case should be considered? | Prediction, commitment, selected plan |
| Consequence | Possible, inferred, projected, or observed outcome of a condition or action | What could result? | Recommendation, decision, goal |
| Recommendation | Advisory response connected to evidence and goal relevance | What should be considered? | Forecast, decision, command |
| Decision | Selection, rejection, deferral, or escalation of an option | What is chosen? | Prediction, execution result |
| Plan | Intended or organized future action or sequence | What is intended or scheduled? | Future fact, guarantee, observation |
| Commitment | Promise, obligation, or externally meaningful undertaking | What is obligated or promised? | Forecast, scenario, mere expectation |
| Uncertainty | Preserved incompleteness or spread in what is known, inferred, expected, or possible | What is not fully settled, bounded, or known? | Contradiction, ignorance, low confidence alone |

## 1. Future Claims

A future claim is a claim whose content concerns a state, event, transition,
condition, consequence, or outcome at a time later than the claim's evaluation
or assertion context.

A future claim should be understood through at least these conceptual fields,
even when no schema is being proposed here:

```text
subject / scope
future predicate or outcome
future horizon or time window
supporting observations, claims, models, and assumptions
uncertainty or confidence expression
provenance of the claim
claim creation or evaluation time
conditions under which the claim applies
```

Examples:

```text
Disk will fill within 7 days.
Traffic is expected to increase next month.
Federation link may become stale before the next synchronization.
Replacing the host is likely to improve reliability.
```

Future claims differ from observations because an observation records what a
source reported or measured at an observation time. Seed may observe that a
source made a prediction, but that observation is not itself an observation of
the predicted future state.

For example:

```text
Observation: model M reported "disk will fill within 7 days" at time T.
Future claim: disk will fill within 7 days after T.
```

The first is historical evidence about a report. The second is future-oriented
content supported by that report and any other evidence Seed chooses to preserve.

Future claims differ from historical claims because historical claims concern
past states, events, or transitions. They may be discovered later, revised later,
or contradicted later, but their target time is not future relative to the claim
context.

Future claims differ from current-state claims because current-state claims
select or express present understanding under freshness and support rules.
Current-state claims may support future claims, but they do not guarantee future
conditions.

## 2. Prediction

A prediction is a future claim that asserts a possible or expected future state,
event, transition, consequence, or outcome under stated or inferable support,
assumptions, and time horizon.

Prediction is therefore primarily a claim, not an observation, recommendation,
decision, command, or action.

Prediction may involve assessment and projection:

```text
Assessment: storage growth rate is high.
Projection: at this growth rate, remaining capacity crosses zero in 7 days.
Prediction: disk exhaustion is likely within 7 days.
```

The assessment interprets current or historical knowledge. The projection carries
a method or extrapolation over time. The prediction is the claim about the future
condition. The prediction may later support a recommendation, but it does not
itself advise action.

Prediction should remain explainable. A prediction should be able to answer:

```text
What was predicted?
For what time horizon?
From which observations and claims?
Under which assumptions?
With what uncertainty?
By which source, model, operator, or inference path?
What later outcome, if any, was observed?
```

A failed prediction does not invalidate the historical observations that
supported it. It may show that the model, assumptions, trend selection, causal
interpretation, or confidence expression were incomplete or wrong. The support
path remains historical evidence for why the prediction existed at the time.

## 3. Forecasting

Forecasting is the production, preservation, or communication of structured
future-oriented estimates or claims over a horizon.

Forecasting differs from prediction in scope and structure:

```text
Prediction: disk will fill within 7 days.
Forecast: remaining disk capacity by day for the next 14 days, with uncertainty.
```

A forecast may contain one prediction, many predictions, ranges, trajectories,
quantiles, model outputs, scenario comparisons, or time-indexed expected values.
It may aggregate multiple future claims into a coherent view.

Forecasting differs from estimation because estimation may concern past,
present, or future unknowns. A present estimate such as "current traffic is
approximately 10k requests per minute" is not necessarily a forecast. A forecast
is specifically future-oriented.

Forecasting differs from planning because planning organizes intended future
actions. Forecasting describes what may or is expected to happen under a support
context. A maintenance window plan is not a traffic forecast, although a traffic
forecast may influence the plan.

Forecasting differs from recommendation because forecasting answers what may
happen, while recommendation answers what should be considered in light of what
may happen and the operator's goals.

Forecasts are not commitments. A forecast may influence a commitment, and a
commitment may influence a forecast, but neither collapses into the other.

## 4. Expectation

An expectation is an anticipated claim stance: a source, model, operator, or
inference path anticipates a state, event, value, behavior, or outcome.

Expectation differs from prediction because expectation is the stance of
anticipation, while prediction is the future-oriented claim content. The sentence
"traffic is expected to increase next month" contains both an expectation stance
and a future claim about traffic.

Expectation differs from confidence because confidence expresses warrant or
strength of support for a claim. A source may expect a future condition with low
confidence, or may have high confidence that a weak expectation is the best
available expectation.

Expectation differs from trust because trust concerns the assessed reliability,
authority, or appropriateness of a source, model, process, or provenance path.
Seed may trust a source less while still preserving what that source expects.

Expectation differs from belief because belief is Seed's selected or asserted
stance about what is accepted in a context. A preserved expectation from an
external model does not automatically become Seed's belief.

Expectation differs from probability because probability is a quantitative or
formal expression over possible outcomes. Expectation may be qualitative:

```text
expected to increase
likely to degrade
may become stale
not expected to change
```

Expectation should not be treated as truth. It is a future-oriented or
anticipatory posture that requires support, provenance, and uncertainty.

## 5. Scenarios

A scenario is a coherent possible-future frame used to reason about outcomes
under a set of assumptions, conditions, or stresses.

Examples:

```text
best-case
worst-case
likely-case
failure-case
baseline-case
operator-assumption case
external-model case
```

Scenarios differ from predictions because a scenario need not assert that it
will occur. A scenario may be deliberately constructed to explore consequences,
bounds, sensitivity, risk, or preparedness.

For example:

```text
Scenario: worst-case traffic doubles while storage growth continues.
Prediction: traffic is likely to increase by 20% next month.
```

The scenario frames a possible case. The prediction asserts an expected future
condition. A likely-case scenario may contain predictions, but the scenario as a
whole remains a reasoning frame rather than a promise or commitment.

Scenarios are useful because they preserve alternatives without forcing a single
selected future. They allow Seed to distinguish:

```text
what is expected
what is possible
what is assumed for analysis
what would be severe if it happened
what the operator plans to do
```

Scenarios are not commitments. They do not authorize action, prove risk,
obligate operators, or convert possibilities into current facts.

## 6. Consequences And Future Claims

A consequence is an outcome that could, did, or may result from a condition,
action, event, or decision. Consequences can be historical, current, or future.
Future consequences are future claims when they concern possible later outcomes.

The recommendation relevance chain remains:

```text
Assessment
  -> Consequence
  -> Goal Relevance
  -> Recommendation
  -> Decision
  -> Command
  -> Action
```

A consequence differs from a prediction because consequence reasoning is
relational: it explains an outcome as resulting from a condition or action. A
prediction may simply assert a future state. Consequence reasoning adds the
"because of" or "would result in" structure.

Example:

```text
Prediction: disk exhaustion is likely within 7 days.
Consequence: disk exhaustion could cause write failures.
Recommendation: increase storage capacity or reduce write pressure.
Decision: approve capacity increase.
```

The future consequence supports goal relevance. It does not itself select a
response. The recommendation is the advisory response boundary. The decision is
the selection boundary.

Future consequences may be supported by causal claims, historical patterns,
operator assumptions, imported documentation, incident history, simulations,
external model output, or domain knowledge. The support path should remain
explainable and should not be hidden behind the recommendation.

## 7. Evidence And Support For Future Claims

Future claims require support and provenance. Because the future has not yet
been observed, support for future claims is indirect.

Support may include:

```text
observations
current-state claims
historical claims
trends
rates of change
historical patterns
causal claims
known mechanisms
operator assumptions
explicit scenario assumptions
imported knowledge
external model outputs
federated claims
policy or configuration constraints
planned actions, when treated only as intended inputs
```

Different support paths carry different meanings:

```text
Observation support: what was measured or reported?
Trend support: what direction or rate appears over time?
Pattern support: what has happened in similar past cases?
Causal support: why would this condition produce that outcome?
Assumption support: what is being assumed for analysis?
Model support: what model produced the claim and with what inputs?
Federated support: which external Seed or source supplied the claim?
Operator support: what did the operator assert, intend, or assume?
```

A future claim may be well supported without becoming certain. It may also be
unsupported, weakly supported, contradicted by other future claims, stale,
model-dependent, or assumption-dependent.

Support should remain explainable. At minimum, future-oriented reasoning should
preserve the distinction between:

```text
source reported a prediction
Seed inferred a prediction from evidence
operator supplied an assumption
external model generated a forecast
scenario assumed a condition for analysis
recommendation relied on a prediction
```

This distinction matters because provenance controls interpretation, authority,
trust, accountability, and later calibration.

## 8. Uncertainty

Uncertainty is the preserved incompleteness, boundedness, variability, or
contestability of a claim, inference, forecast, scenario, or decision-relevant
interpretation.

Uncertainty may arise from:

```text
future variability
limited observations
measurement noise
stale information
model limitations
unknown causal factors
ambiguous source language
competing support paths
operator assumptions
external dependency behavior
insufficient historical data
wide possible outcome ranges
```

Uncertainty differs from contradiction. Contradiction means claims cannot all be
true together under the same relevant scope, time, and interpretation.
Uncertainty means the available support does not fully settle the matter, even
if no direct contradiction is present.

Uncertainty differs from ignorance. Ignorance is absence or lack of relevant
knowledge. Uncertainty can exist even with substantial knowledge, such as a
well-supported forecast with a wide range of possible outcomes.

Uncertainty differs from ambiguity. Ambiguity concerns unclear meaning,
reference, scope, or interpretation. Uncertainty concerns unsettled state,
outcome, likelihood, or inference. Ambiguity can cause uncertainty, but they are
not identical.

Uncertainty differs from low confidence. Low confidence is one way to express a
weak claim posture. Uncertainty may be high even when confidence in the
forecasting process is high, for example when the process reliably reports a
wide outcome distribution.

Future reasoning should preserve uncertainty rather than collapse it into a
single apparently factual future. Qualitative uncertainty, quantitative ranges,
probabilities, confidence levels, assumptions, and scenario labels should remain
conceptually distinct.

## 9. Future Claims And Recommendations

Recommendations may rely on future claims, but they do not become forecasts.
Future claims answer what may happen. Recommendations answer what should be
considered in response to what may happen and why that response matters to an
operator-owned goal.

Example:

```text
Current-state claim: storage is 85% full.
Trend claim: storage usage is increasing by 2% per day.
Prediction: if growth continues, disk exhaustion is likely within 7 days.
Consequence: disk exhaustion could cause write failures and service degradation.
Goal relevance: service availability would be harmed.
Recommendation: increase storage capacity or reduce write pressure.
```

Prediction ends at the supported future-oriented assertion. Recommendation
begins when Seed crosses into advisory response generation tied to consequences,
goals, constraints, and alternatives.

A recommendation should not hide its predictive dependency. If a recommendation
is justified by a future claim, the explanation should expose that dependency:

```text
recommended because predicted consequence threatens goal
recommended despite uncertainty because severity is high
not recommended because prediction support is weak
alternative recommended because plan changes the forecast horizon
```

Recommendation authority remains advisory unless a separate decision,
authorization, command, or action boundary is crossed. A highly confident
prediction does not authorize action by itself.

## 10. Future Claims And Plans

A plan is an intended, scheduled, organized, or selected future action or
sequence of actions. A plan is not a prediction because it records intention or
organization, not occurrence.

Examples:

```text
Future claim: outage is expected tomorrow.
Plan: migrate service tomorrow.
Commitment: team has committed to completing migration by 18:00 UTC.
Prediction: migration is likely to reduce outage risk.
```

Plans may affect future claims. If a migration is planned, a forecast may use
that planned action as an assumption. But the plan remains an input or object of
reasoning, not proof that the future action will occur or succeed.

Plans are not future facts. A planned migration can be cancelled, fail, change
scope, be superseded by a decision, or execute differently from its description.
Seed should preserve the plan as a historical and current planning object while
separately preserving observations of execution and outcomes when they occur.

Plans differ from commitments. A plan may be internal, tentative, or exploratory.
A commitment expresses obligation, promise, or externally meaningful undertaking.
Neither should be collapsed into a forecast.

## 11. What Must Not Be Collapsed Together

The following distinctions are architectural boundaries:

| Distinction | Why it matters |
| --- | --- |
| Prediction != Observation | Seed may observe that a prediction was made, but it has not observed the future event. |
| Forecast != Commitment | A forecast describes possible or expected futures; a commitment records obligation or promise. |
| Scenario != Prediction | A scenario may be a reasoning frame without asserting that the scenario will occur. |
| Expectation != Truth | An expected outcome may fail, and the expectation still remains historically real. |
| Recommendation != Forecast | A recommendation advises consideration; a forecast describes possible future conditions. |
| Decision != Prediction | A decision selects an option; it does not prove the selected outcome will happen. |
| Plan != Future Fact | A plan records intention or organization, not future occurrence. |
| Confidence != Probability | Confidence is warrant or support posture; probability is an outcome measure or distribution. |
| Uncertainty != Contradiction | Uncertainty is unsettledness; contradiction is incompatibility among claims. |
| Consequence != Recommendation | A consequence explains what could result; a recommendation advises what to consider. |
| Assumption != Observation | An assumption frames reasoning; it is not measured reality. |
| Model output != Seed belief | Imported or generated output must be preserved with provenance before selection. |

These distinctions matter because future-oriented reasoning is high-risk for
category collapse. Without clear boundaries, Seed could accidentally treat a
forecast as authorization, a plan as accomplished reality, a scenario as a
prediction, or an expectation as truth.

## Non-Goals

This reconciliation does not require Seed to implement:

```text
prediction schemas
forecast schemas
scenario schemas
probability calculus
simulation engines
planning engines
recommendation generators
model calibration systems
runtime prediction behavior
automatic action selection
automatic goal adoption
automatic commitment tracking
new federation behavior
new learning behavior
```

It also does not require changing observation, evidence, claim, fact, event,
projection, recommendation, decision, authority, or test behavior.

Any future implementation proposal would need its own design and authority
review. This document only defines conceptual boundaries.

## Implementation Implications

Because this is a documentation-only reconciliation, the implementation
implications are constraints on interpretation rather than implementation tasks.

If future implementation work later addresses prediction or forecasting, it
should preserve these boundaries:

```text
future claims are claims, not observations
prediction records require support and provenance
forecast outputs should expose assumptions and horizons
scenarios should remain distinguishable from selected predictions
recommendations should expose predictive dependencies
plans should not be projected as future facts
uncertainty should remain visible
later outcomes should not erase historical predictions
```

The main architectural implication is negative: existing claim, support,
recommendation, decision, and planning concepts should not be reused in ways that
silently collapse future reasoning into present truth or execution authority.

## Architectural Invariants

The findings support the following architectural invariants:

1. Future claims are claims.
2. Predictions are not observations.
3. Forecasts are not commitments.
4. Scenarios are not promises.
5. Recommendations may rely on predictions.
6. Recommendations are not predictions.
7. Decisions are not predictions.
8. Plans are not future facts.
9. Commitments are not forecasts.
10. Expectations are not truth.
11. Confidence is not probability.
12. Uncertainty is not contradiction.
13. Assumptions are not observations.
14. Future reasoning should preserve uncertainty.
15. Future claims require support and provenance.
16. Prediction support should remain explainable.
17. A failed prediction does not invalidate its historical support.
18. A future claim becoming false does not erase its historical existence.
19. A scenario may contain predictions, but the scenario itself is a reasoning frame.
20. A plan may influence a forecast, but the plan does not prove the forecasted outcome.

## Conclusion

Seed should represent future-oriented reasoning as claim-centric,
provenance-bearing, support-preserving, and uncertainty-preserving.

The future should not be treated as observed merely because Seed can reason
about it. Predictions, forecasts, expectations, scenarios, consequences,
recommendations, plans, commitments, decisions, commands, and actions occupy
different architectural layers.

The governing boundary is:

```text
Future reasoning may describe, compare, support, and explain possible futures;
it must not silently convert possible futures into observed facts, commitments,
plans, recommendations, decisions, commands, or executed outcomes.
```

This preserves Seed's existing architectural posture: history remains preserved,
current understanding remains selected and explainable, learning can revise
interpretation without erasing prior claims, recommendations remain advisory,
decisions remain distinct from commands, goals remain operator-owned, and future
claims remain revisable claims rather than observations of reality.
