# Question graph pass 088 — Book comparison and projection decision

## Decision

A small Book projection is warranted. Existing clauses already preserve most nodes and edges compositionally, but the Book does not directly preserve the present-facing graph distinctions among Question Shape, Survey Warrant Family, QuestionFamily, individual bounded question, typed Unknown constraints, Inquiry Need/frontier separation, family/instance boundaries, and completion/retirement as one readable question-graph relation set. Adding a constrained graph section to `04-inquiry-and-examination/questions-and-inquiry.md` is the smallest truthful projection. It avoids a new Book chapter and avoids creating a universal question engine.

## Coverage classification by neighborhood

| Neighborhood | Book coverage before projection | Decision |
| --- | --- | --- |
| Expression → pressure → possible inquiry → admitted movement | Direct/compositional through External Grammar, question origination, frontier, admission, refusal, stopping. | No new ingress clause needed. |
| Bounded goal/current position → Inquiry Need | Partially preserved by goals/needs/frontiers, but graph distinction between Inquiry Need and question is under-projected. | Project distinction in question graph section. |
| Typed Unknown → question/evidence/stop constraints | Compositional through Unknown/evidence/stop clauses; typed Unknown versus public generic unknowns under-projected in question graph. | Project non-collapse and constraint relation. |
| Question Shape ↔ Survey Warrant Family ↔ QuestionFamily | Partially preserved by kind-label/no-ontology and question clauses; current relation/refusal boundaries under-projected. | Project relation/refusal boundaries. |
| QuestionFamily ↔ individual bounded question | Partially preserved by question/answer boundary; current family/instance and pipeline special-case conflict under-projected. | Project family/instance boundary. |
| Inquiry Need → bounded inquiry frontier | Direct in inquiry-frontiers; no universal formulation boundary already present. | Cross-reference in graph section. |
| Individual bounded question → examination frontier/method/policy/selection/probe | Direct in examination chapters. | No new examination clause needed beyond graph cross-reference. |
| Finding/answer/sufficiency/completion/retirement | Direct/compositional in evidence/stopping; family-local answer responsibility and completion/retirement distinction under-projected in question graph. | Project non-collapse boundary. |
| Bounded result → representation → delivery → response/new pressure | Direct through `08.Handoff.C` and stopping/refusal clauses. | No new egress clause needed. |
| Receipt/understanding/reliance/correction/reopening | Preserved negatively by handoff/refusal/stopping. | No new clause; graph section references negative boundary. |

## Clause-by-clause comparison

- `01.Standing.A` already blocks reachable artifacts from promotion to admission, reliance, truth, event ledger writes, or mutation. Adequate for reachability edges.
- `01.Standing.B` already blocks class names, inventory rows, and report kinds from ontology closure. Adequate for not promoting implementation names; insufficient alone for the shape/warrant/family relation because those are question-specific.
- `01.External.A/B/C` already cover external expression, addressability, translation, and limit-preserving consumption. Adequate for ingress and re-entry.
- `01.Lenses/views/roads` already distinguishes lens, road, uptake, handoff, adjacency, and sequence. Adequate for edge-class discipline.
- `04.Question.A/B` cover question standing and origination; they do not explicitly preserve Question Shape / Survey Warrant Family / QuestionFamily / individual bounded question as separate resolutions.
- `04.Frontier.A/B/C` cover frontier membership, exclusions, lawful inactivity, and missing/unknown/conflict. Adequate for frontier membership versus selection/execution; graph cross-reference helpful.
- `04.Examination.A/B/C` cover applicability, selection, probe, output, findings, lawful inactivity, and cross-examination. Adequate.
- `05` evidence and knowledge chapters cover testimony, fact establishment, provenance, recording, Unknowns, and no silent knowledge. Adequate for output/finding/knowledge boundaries.
- `06` state/projection chapters cover result/state/projection non-promotion. Adequate for projection and result standing.
- `07.Realization.B` covers seam-specific Fidelity and realization. Adequate for implementation realization edges.
- `08.Handoff.C` covers egress representation and delivery boundaries. Adequate.
- `08.Stopping` covers local stops/completion but question graph should explicitly state completion is not retirement.

## No-change decisions

No dedicated `constitutional question graph` Book chapter is warranted because that would risk stabilizing a canonical topology. No implementation file should change because the task is recovery/projection, not runtime design. No diagnostic inventory or shape-audit update is required because no diagnostic surface, CLI flag, audit, recordable output, or operational surface is added.

## Book projection performed

Projection: add `04.Question.C — Question graph relations are plural and non-collapsing` to `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`.

The clause states source standing, target standing, crossing evidence/warrant, non-crossing evidence, lawful refusals/stops, and non-collapse boundaries. It uses present-facing language and avoids Python class names, CLI flags, tests, PR numbers, pass chronology, and speculative machinery.
