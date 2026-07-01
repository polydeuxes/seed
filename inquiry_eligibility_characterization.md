# Inquiry Eligibility Characterization

## Executive answer

Yes, the repository demonstrates a recurring competency that operates before Methodological Selection, but the most repository-faithful name is **Inquiry Eligibility**, not a broad selection method, planner, or priority engine.

The responsibility is bounded:

```text
candidate inquiry / attractive architectural idea
        ↓
repository observation and prior-work reload
        ↓
evidence-strength check against claim-strength / boundary being proposed
        ↓
reject, defer, preserve as open/unsupported, or narrowly authorize
        ↓
only then can selection/path explanation operate on an eligible surface
```

This competency is not primarily choosing the next inquiry. It determines whether an inquiry, boundary, family, vocabulary, or implementation direction has been constitutionally earned by repository evidence. Its positive output is narrow authorization: a bounded inquiry may proceed only to the extent supported. Its negative output is equally important: `Insufficient implementation evidence.`

The evidence is sufficient to recognize a stable discipline, but not sufficient to claim a separately implemented runtime subsystem named `InquiryEligibility`. The competency is presently distributed across constitutional claim rules, inquiry/documentation artifacts, selection-path unknown handling, recovery investigations, completion audits, and architectural vocabulary preservation.

## Repository evidence reviewed

This characterization reviewed implementation-backed and documentation-backed evidence from:

- `docs/seed.md` for constitutional claims about observations, evidence, justified claims, promotion, projections, and authority.
- `docs/evidence_strength_and_claim_strength_reconciliation.md` for the recurring rule that claims must not exceed support.
- `repository_dependency_ordering_invariant_investigation.md` for assessment, justification, admission, identity, and evidence-before-selection/execution ordering.
- `methodology_as_inquiry_subject_investigation.md` for methodology-as-subject boundaries, explicit registration limits, and rejection of inferred subjects/subsystems.
- `selection_path_answer_composition_completion_audit.md` and `seed_runtime/selection_path_audit.py` for what Methodological/Selection Path actually owns: candidate ordering, selection factors, non-selected candidates, unknown selection targets, and outcome explanation.
- `seed_runtime/inquiry_artifacts.py` for repository-visible inquiry artifacts, including `supported_conclusion`, `unsupported_conclusion`, `open_question`, read-only boundaries, and explicit refusal to infer inquiry movement or planning.
- `docs/architectural_findings_vocabulary.md` for the preserved vocabulary of accepted findings, rejected concepts, deferred concepts, open questions, current frontiers, and architectural lessons.
- Representative reports ending in or preserving `Insufficient implementation evidence`, including `inquiry_lineage_slice_001.md`, `inquiry_lineage_slice_004.md`, `projection_diagnostics_slice_002.md`, and `state_build_cache_debug_slice_002.md`.

The app was also exercised to inspect repository-visible inquiry surfaces rather than relying only on prose:

```text
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --inquiry-artifacts --json
python scripts/seed_local.py --selection-path current_focus --json
```

These commands confirmed that the repository exposes bounded question-family inventory, inquiry-artifact visibility, and selection-path visibility as read-only surfaces.

## Recurring behavioral pattern

The repeated behavior is not immediate selection. The repeated behavior is eligibility filtering.

### Pattern observed

```text
1. A candidate framing appears interesting.
2. The repository is searched for implementation evidence, prior work, tests, and preserved findings.
3. The candidate claim is compared with the strength and type of evidence.
4. If the claim exceeds evidence, the repository rejects, defers, narrows, or preserves a null conclusion.
5. If the claim is supported, only the supported slice is authorized.
6. Selection, roadmap, frontier, pressure, or completion language may then describe the remaining eligible work.
```

### Evidence that this pattern is recurring

`docs/evidence_strength_and_claim_strength_reconciliation.md` states the central guardrail directly: a claim can be related to evidence while still exceeding what the evidence justifies, and the useful question is whether claim strength matches support strength. That document gives escalation warning signals such as scope expansion, evidence-type changes, inference-chain growth, ownership appearing, authority appearing, and behavior appearing without behavior evidence.

`repository_dependency_ordering_invariant_investigation.md` generalizes the same structure across implementation families: established evidence or identity appears before narrower reasoning; verification, admission, or agreement appears before presentation or downstream use; construction appears before publication; and assessment or justification appears before selection/execution.

`methodology_as_inquiry_subject_investigation.md` applies this discipline to methodology itself. It finds that methodology-oriented inquiry is plausible in shape, but explicitly refuses to infer an implemented question family or new subsystem merely from recurring methodology reports.

`selection_path_answer_composition_completion_audit.md` shows the boundary from the other side: Selection Path owns candidate ordering, selection factors, candidate lineage, non-selected explanations, unsupported-target unknowns, and outcome explanation. It does not own the prior constitutional decision that a candidate inquiry has enough evidence to be eligible.

`seed_runtime/inquiry_artifacts.py` keeps supported and unsupported conclusions visible but bounded. It classifies `supported_conclusion` and `unsupported_conclusion` as document-visible, and its boundary refuses recording, event-ledger writes, cluster mutation, inquiry-graph creation, pressure-transformation inference, workflow, and planning.

## What distinguishes interesting from justified?

An idea is **interesting** when it has conceptual appeal, recurring vocabulary, or apparent explanatory usefulness.

An idea is **justified** only when repository evidence supports the specific strength of the claim being made.

The repository repeatedly rejects escalation from:

- observed relationship to ownership;
- recurring vocabulary to stable ontology;
- document shape to runtime artifact;
- local handoff grammar to shared abstraction;
- presentation label to preserved knowledge;
- visibility surface to mutation authority;
- current frontier to selected implementation;
- candidate family to recovered owner.

The criterion is not novelty, elegance, or usefulness. The criterion is proportionality between support and conclusion.

## Constitutional authority

Inquiry Eligibility derives authority from core Seed rules, not from preference.

`docs/seed.md` says Seed begins with observation, accumulates evidence, normalizes justified claims, connects justified relationships, selects explainable projections, and escalates to the operator when authority is required. It also states that facts are justified claims, that a single observation may justify a scoped fact only when it does not exceed the observation's scope, and that promotion should preserve the rule: promote only what the evidence supports.

The same constitutional document says projections select and communicate preserved knowledge but do not become authority over truth or action. That matters here: selection surfaces can explain selected knowledge, but selection visibility does not override whether the underlying inquiry has been earned.

Therefore the constitutional authority of Inquiry Eligibility is:

```text
Preserve broadly.
Promote carefully.
Explain provenance.
Do not let claim strength exceed evidence strength.
Do not let projection or presentation become truth authority.
```

It may reject a candidate inquiry when the inquiry would require unsupported claim promotion, unsupported ownership, unsupported implementation authority, or unsupported vocabulary stabilization.

## Relationship to Methodological Selection

Methodological Selection and Inquiry Eligibility are adjacent but different.

### Inquiry Eligibility

Owns:

- whether a candidate inquiry has sufficient repository evidence to be pursued at the claimed strength;
- whether a proposed boundary is supported, unsupported, deferred, or open;
- whether attractive vocabulary is only presentation or is repository knowledge;
- whether a proposed implementation direction is constitutionally earned;
- whether the result should be a null conclusion such as `Insufficient implementation evidence.`

It operates before selection because it determines the candidate set that selection is allowed to consider.

### Methodological Selection / Selection Path

Owns:

- candidate ordering once an implemented candidate set exists;
- selection factors;
- candidate lineage;
- non-selected candidate explanation;
- unsupported selection-target unknowns;
- selected outcome explanation.

The implementation in `seed_runtime/selection_path_audit.py` demonstrates this. It normalizes a target, builds pressure and operational-story evidence, returns pressure-based selection for implemented targets, and returns `unknown` when no implementation-backed selection evidence exists. `_from_pressure_selection(...)` orders pressure candidates by score and category, records selection factors, builds candidate rows, and explains non-selected candidates.

That is selection explanation, not constitutional eligibility.

### Boundary

Inquiry Eligibility can say:

```text
No candidate has earned investigation at this claim strength.
```

Selection Path can say:

```text
Given this implemented selection surface and candidates, this candidate sorted first; the others did not.
```

The repository evidence supports this ordering:

```text
eligibility / justification / admission / assessment
        ↓
selection / explanation / non-selected alternatives
```

## Comparison with adjacent competencies

| Adjacent surface | Relationship to Inquiry Eligibility |
| --- | --- |
| Constitution | Source of authority: observations before evidence, justified claims, promote only what evidence supports, projections are not truth authority. |
| Investigation | Common work mode that applies eligibility: searches evidence, tests candidate boundaries, preserves supported and unsupported conclusions. |
| Implementation Audit | Strong evidence source for eligibility because it checks actual code, tests, diagnostics, and implemented boundaries. |
| Completion Audit | Uses eligibility to stop work when remaining pressure belongs elsewhere or lacks implementation-backed continuation evidence. |
| Roadmap | Consumes eligible/deferred/frontier findings; does not by itself make an unsupported inquiry justified. |
| Frontier | Preserves next meaningful attention after eligibility and status work; priority does not equal constitutional authorization. |
| Pressure | May supply candidate pressure, but pressure alone does not justify a boundary or implementation family. |
| Current Work Position | Can orient continuation, but presentation/continuation vocabulary is not automatically preserved knowledge. |
| Slice | A bounded implementation-backed investigation unit; eligibility determines whether a slice is justified and how narrow it must be. |
| Methodological Selection | Operates after an implemented or justified candidate set exists; explains ordering, non-selection, unknowns, and selected outcome. |

## Counterexamples and limits

### Counterexample considered: immediate selection without rejection

Selection Path does implement immediate ordering for current pressure candidates when the target is implemented. The code selects the first pressure item after pressure audit ordering. However, this is not a counterexample to Inquiry Eligibility because it occurs inside an already implemented selection surface and still returns `unknown` for unsupported targets.

### Counterexample considered: Methodological Selection already owns eligibility

`selection_path_answer_composition_completion_audit.md` says the remaining Selection Path responsibility is candidate ordering, factors, lineage, non-selected candidate explanation, unsupported target unknowns, and outcome explanation. It does not claim ownership of constitutional evidence sufficiency. The strongest supported conclusion is that Selection Path owns local selection explanation, while eligibility is broader and upstream.

### Counterexample considered: no recurring rejection discipline

The repository contains too many preserved rejection and insufficiency patterns for this to hold. `docs/architectural_findings_vocabulary.md` treats rejected concepts as useful findings because they prevent rediscovery and scope creep. It also distinguishes rejected concepts from deferred concepts, open questions, and frontiers.

### Counterexample considered: `Insufficient implementation evidence` is merely wording

The phrase is report wording, but the behavior behind it is not merely wording. It recurs where reports stop rather than overclaim: inquiry-lineage slices preserve insufficient evidence for precise family naming or stronger generalization; projection diagnostics reject narrower owner vocabulary when evidence only supports a broader payload; state-build cache debug preserves insufficiency rather than inventing a stronger family. The phrase marks a completed eligibility check whose negative result is constitutionally meaningful.

### Limit

There is not sufficient evidence to claim a standalone implementation owner, CLI surface, diagnostic surface, or runtime artifact named `Inquiry Eligibility`. Recognizing the competency should not trigger a planner, ranking system, autonomous scheduler, selection algorithm, or implementation strategy.

## Supported conclusions

1. A recurring competency exists before Methodological Selection.
2. The best bounded name is **Inquiry Eligibility**.
3. Its responsibility is to determine whether a candidate inquiry, boundary, vocabulary, family, or implementation direction has been constitutionally earned by repository evidence.
4. It rejects inquiries when evidence is insufficient, claim strength exceeds evidence strength, authority would be promoted without support, vocabulary is only presentational, or a proposed owner/subsystem is inferred from recurring shape rather than implementation evidence.
5. It authorizes inquiries only narrowly: the authorized inquiry may proceed only at the strength, scope, and boundary supported by repository evidence.
6. Its constitutional authority comes from Seed's observation/evidence/justified-claim rules, careful promotion, provenance explanation, and projection-not-authority boundary.
7. It differs from Methodological Selection because selection explains ordering among eligible or implemented candidates; eligibility determines whether candidates have earned consideration at all.
8. When a report concludes `Insufficient implementation evidence.`, the completed bounded work is an eligibility assessment that successfully prevented unsupported promotion.
9. There is sufficient repository evidence to recognize a stable distributed competency, but not an implemented subsystem.

## Unsupported conclusions

Current repository evidence does not support concluding that:

- `Inquiry Eligibility` is already an implemented runtime module or public question family;
- Methodological Selection should be replaced;
- a new planner, ranking engine, priority engine, autonomous scheduler, or selection algorithm is justified;
- every rejection belongs to one central owner;
- every future inquiry must explicitly name Inquiry Eligibility before proceeding;
- recurring report wording alone proves architecture;
- pressure, roadmap, frontier, or current-work-position language can authorize an inquiry without implementation evidence;
- presentation vocabulary should be promoted into preserved knowledge without a separate evidence check.

## Confidence

**Moderate-high** for the existence of a stable distributed eligibility discipline.

The confidence is high that the repository repeatedly rejects unsupported claim escalation and places assessment/justification/admission before selection in multiple surfaces. The confidence is lower for naming because the repository does not currently implement a first-class `InquiryEligibility` module, question family, or diagnostic surface. The safest characterization is therefore:

```text
Inquiry Eligibility is a stable repository discipline and recurring responsibility pattern,
not yet a separately implemented subsystem.
```
