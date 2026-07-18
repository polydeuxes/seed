# Goal-Relative Inquiry Pressure Slice 001

This slice recovers exactly one implementation-local ownership boundary between an established bounded goal plus examined inquiry-need findings and later bounded-question formation.

## Selected ownership boundary

`recognize_goal_relative_inquiry_pressure(...)` owns goal-relative inquiry-pressure recognition. It consumes one `GoalInquiryConsiderationSelection`, one `BoundedOperatorGoalEstablishment`, one `BoundedAdvancementHorizon`, and one already-produced `InquiryNeedProjection`. It produces `GoalRelativeInquiryPressure`.

The owner is read-only. It does not inspect raw operator wording, open inquiry, formulate question wording, select a question, authorize observation, write the event ledger, mutate cluster state, or fabricate missing evidence.

## Adjacent implementation evidence

Adjacent upstream evidence already existed in the implementation:

- `BoundedOperatorGoalEstablishment` establishes bounded operator goals from admitted ingress artifacts, while preserving that goal establishment is not inquiry opening, recording, execution, or mutation.
- `GoalInquiryConsiderationSelection` selects exactly one visible bounded goal for inquiry consideration only from explicit focus evidence naming exact bounded-goal identities.
- `BoundedAdvancementHorizon` preserves the present movement boundary and evidence snapshot references for advancement consideration.
- `InquiryNeedProjection` classifies explicit component-bounded repository/world uncertainty testimony against that selected goal, horizon, and horizon evidence refs, while preserving inquiry standing separately from freshness and availability and refusing to select questions.
- `BoundedConstitutionalQuestion` remains the later question artifact consumed by constitutional selection and downstream inquiry work.

## Previous compressed responsibility

Before this slice, `InquiryNeedProjection` could preserve established, unknown, conflicting, unsupported, excluded, and unclassified inquiry-need items, but there was no explicit private handoff that said: this examined finding now creates lawful pressure relative to this established goal and horizon for possible bounded-question formation.

The nearest later producer, `produce_bounded_constitutional_question(...)`, accepted explicit caller fields. That public compatibility path preserved caller inputs but did not require an implementation-owned pressure artifact. The goal-relative recognition boundary was therefore implicit or externally supplied.

## Recovered producer

The recovered producer is `recognize_goal_relative_inquiry_pressure(...)` in `seed_runtime/inquiry_need_projection.py`.

It recognizes pressure only when:

1. the goal inquiry consideration selection is selected;
2. the selected goal identity matches the bounded goal establishment;
3. the inquiry-need projection names the same selection, goal, and horizon;
4. the projection contains at least one established, typed unknown, or conflicting inquiry-need item.

If those conditions fail, the artifact preserves `unsupported` or `unavailable` standing instead of inventing pressure.

## Recovered artifact

`GoalRelativeInquiryPressure` preserves:

- pressure identity;
- selection, goal, horizon, and source projection identity;
- source finding refs;
- examined evidence refs from the horizon;
- recognized standing;
- recognized pressure refs and kinds;
- why the finding matters relative to the goal;
- authority limits;
- provenance refs;
- Unknown and conflict refs;
- standing for possible question formation;
- read-only, no-event-ledger, and no-cluster-mutation boundaries.

It intentionally preserves `question_wording=None`. Pressure is not a bounded question.

## Consumer handoff

`produce_bounded_constitutional_question_from_inquiry_pressure(...)` in `seed_runtime/bounded_constitutional_question.py` is the consumer-side handoff. It forms a `BoundedConstitutionalQuestion` only from a pressure artifact with `standing_for_question_formation=True`, a pressure id, and no embedded question wording.

The caller still supplies bounded question wording, constitutional intent, and scope status. That remaining work is question formation, not pressure recognition.

## Compatibility preservation

The existing `produce_bounded_constitutional_question(...)` function is preserved for compatibility. The new pressure-based helper adds an implementation-local path without changing existing public constructor behavior or downstream consumers.

## Tests added

`tests/test_goal_relative_inquiry_pressure.py` proves:

- operator testimony alone does not produce a bounded question;
- an established goal without goal-relative evidence pressure does not automatically produce a question;
- examined evidence without an established bounded goal does not automatically produce goal-relative inquiry pressure;
- a typed Unknown or conflict may produce bounded inquiry pressure relative to the goal;
- the pressure artifact remains distinct from the resulting question;
- bounded-question formation consumes the pressure handoff rather than silently reconstructing it from raw caller fields;
- read-only inquiry orientation does not mutate cluster knowledge or fabricate missing evidence.

## Explicit answers

### Can operator testimony directly establish a constitutional question?

No. Operator testimony may contribute to upstream goal establishment or explicit caller-compatible fields, but the recovered pressure-based formation helper refuses raw testimony that lacks recognized goal-relative inquiry-pressure standing.

### What establishes the bounded goal?

The bounded goal is established by `BoundedOperatorGoalEstablishment` and selected for inquiry consideration by `GoalInquiryConsiderationSelection` when exact focus evidence names one visible bounded-goal identity.

### What examined evidence makes inquiry pressure lawful relative to that goal?

Inquiry pressure becomes lawful only from already examined `InquiryNeedProjection` items whose selection, goal, horizon, and evidence identities match the selected bounded goal and horizon evidence snapshot. Established, typed unknown, and conflicting inquiry-need items can create recognized pressure. Unsupported, excluded, unclassified, mismatched, or absent items do not.

### What owner recognizes that pressure?

`recognize_goal_relative_inquiry_pressure(...)` recognizes that pressure.

### What standing does the pressure artifact possess?

`GoalRelativeInquiryPressure` has recognized, unsupported, or unavailable standing. Only recognized pressure carries `standing_for_question_formation=True`.

### What remains for bounded-question formation?

Bounded-question formation must still supply lawful question wording, constitutional intent, and bounded scope status, and must produce the `BoundedConstitutionalQuestion`. It must not reconstruct pressure from raw operator wording or caller fields.

### Does the recovered boundary complete the second inquiry cycle?

No. This slice only pours the missing concrete between goal-relative evidence examination and bounded-question formation. It does not implement later question selection, examination, recursive execution, observation authorization, or cycle completion.

### What still remains Unknown?

It remains Unknown which later owner should select among multiple lawful bounded questions, how future examination work should be chosen from a pressure-formed question in this cycle, and whether broader constitutional question admission should replace or further constrain the compatibility constructor.

## Remaining compressed responsibilities

Remaining compressed responsibilities include broader constitutional question grammar/admission, multiple-pressure prioritization, bounded-question selection, examination request construction, recursive-cycle advancement, and any future public compatibility tightening around direct explicit bounded-question construction.
