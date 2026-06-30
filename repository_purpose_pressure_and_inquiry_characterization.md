# Repository Purpose, Values, Pressure, and Inquiry Characterization

## Executive answer

Seed already separates **Pressure** and **Inquiry** in implementation-backed surfaces, and it expresses stable repository **Values** strongly through reconciliations, completion audits, and authority boundaries. It expresses **Purpose** more weakly and mostly methodologically: Seed is consistently directed toward a claim-centric, evidence-preserving, boundary-preserving repository that performs bounded implementation cleanup and inquiry when concrete unanswered questions remain, but the repository does not expose a single implementation-backed `Purpose` owner equivalent to `PressureAudit` or `QuestionSurfaceInventoryRow`.

The recovered architectural relationship is:

```text
Purpose: stable direction for what kind of repository Seed is becoming
  -> evidence-backed, claim-centric, boundary-preserving, humble, locally recoverable

Values: invariant constraints that must be preserved while work changes
  -> evidence support, provenance, compatibility, read-only/mutation boundaries,
     authority humility, claim/fact/projection distinctions

Pressure: current operational or architectural attention signal
  -> what deserves inspection now, ranked from existing visibility surfaces

Inquiry: bounded work/question surface
  -> exact question-family selection, eligibility, dispatch to an answering surface,
     or documentation-only investigation when implementation evidence is insufficient
```

Pressure **informs** inquiry; it does not replace Purpose and does not automatically command implementation. Inquiry performs bounded work because a concrete unanswered question, implementation compression, visibility gap, or operator-facing uncertainty remains under repository authority. The current implementation-backed selector for executable inquiry is exact `QuestionFamily` dispatch through the question surface inventory. The current methodological selector for future investigation is a concrete operator question that is important, recurring, and unanswered by existing documents or surfaces.

Recommendation on a new family: **Insufficient implementation evidence.** The repository has enough evidence for a characterization report, but not enough recurring implementation ownership to justify a new architectural family named Purpose, Values, or Purpose/Pressure/Inquiry.

## Evidence reviewed

### Implementation-backed pressure evidence

- `seed_runtime/pressure_audit.py` defines `PressureItem`, `_PressureItemCandidate`, and `PressureAudit`, then ranks pressure from existing diagnostic shape, ownership, capability, orphaned predicate, and fragile predicate visibility surfaces.
- `seed --pressure-audit --json` currently returns bounded pressure items containing `category`, `score`, `evidence`, `reason`, and `recommended_command`.
- `docs/repository_pressure_inventory.md` characterizes pressure inventory as recurring unresolved repository pressure and explicitly rejects roadmap, future-state vision, strategy, autonomous-agent design, and grand-framework authority.
- `architectural_pressure_methodology_characterization.md` defines pressure as implementation responsibility plurality compressed inside an owner or corridor with insufficient boundary visibility.

### Implementation-backed inquiry evidence

- `seed_runtime/question_surface_inventory.py` defines bounded ask dispatch maps, bounded statuses, selection results, dispatch requests, and `QuestionSurfaceInventoryRow` rows with answer responsibility and authority boundaries.
- `docs/inquiry_presentation_answer_implementation_audit.md` recovers the current executable path: `ask --question-family <exact QuestionFamily>` selects an exact family, validates bounded status and required arguments, sets the mapped CLI surface flag, and terminates at the existing answering surface.
- `seed_runtime/inquiry_orientation.py` preserves inquiry notes as read-only operator prose and limits orientation to deterministic lexical overlap; it explicitly refuses to treat the note as fact, goal, requirement, authorization, command, intent, recommendation, or next safe move.
- `bounded_question_discipline_investigation.md` finds bounded question discipline across implementation surfaces and emphasizes narrow answers, explicit boundaries, and exact inquiry dispatch.

### Methodology and frontier evidence

- `docs/architectural_status_and_next_frontier.md` owns current architectural status, active frontier, and priorities; it classifies many recent inquiry/attention/current-work-position/active-edge documents as exploratory and not implementation-ready.
- `docs/future_frontiers.md` preserves candidate frontiers but states that presence on the list does not imply priority, sequencing, implementation readiness, or canonical ontology.
- `docs/current_work_position_frontier.md` and `docs/active_edge_frontier.md` explore what keeps work continuous or pulls work forward, while rejecting planners, schedulers, prioritizers, workflow engines, attention systems, schemas, runtimes, and implementation behavior.
- Completion-audit and family reports reviewed through the pressure methodology show that completed families stop when same-family compressed ownership is gone and remaining pressure is adjacent, unsupported, residual, or frontier.

## Purpose characterization

### Supported characterization

Seed's repository purpose is not implemented as a first-class runtime object, schema, diagnostic record, or CLI surface. It is nevertheless methodologically visible as stable direction:

```text
Seed is trying to become a repository that preserves evidence-backed knowledge,
keeps authority boundaries explicit, supports bounded inquiry and recovery,
and improves through narrow compatibility-preserving implementation work.
```

Evidence:

- The architectural status document says Seed's major conceptual reconciliation is complete enough to keep active implementation attention on bounded cleanup rather than recursive architecture audits.
- Its current priority is bounded implementation work over concrete observation/projection problems, beginning with Prometheus boundary issues.
- Its architectural status table classifies the foundational ontology as claim-centric and stable, while many newer inquiry/attention/current-position/active-edge concepts remain exploratory and not implementation-ready.
- Its future-investigation rule says to start future investigations only when a concrete operator question is important, recurring, and unanswered by existing documents or surfaces.

### Boundary

Purpose is **not** the current top pressure, not the active inquiry, and not the future frontier list. Pressure can change without changing the repository's direction. Inquiry can change without changing the repository's direction. The current documentation does not support a new autonomous motivation, goal planner, reward system, or agent architecture.

### Implementation backing

Purpose is **methodology-backed**, not implementation-backed as a discrete owner. There is no `PurposeAudit`, `RepositoryPurpose`, `PurposeItem`, or executable `--purpose` surface found in the reviewed evidence. Purpose is inferred from stable cross-document constraints and current architectural routing, not from a single implementation surface.

## Values characterization

### Supported characterization

Values are the repository properties that remain constant while pressures and inquiries change. The strongest values recovered from evidence are:

1. **Repository authority wins.** Implementation behavior, tests, executable surfaces, and repository-visible documents outrank preference.
2. **Evidence and provenance must be preserved.** Observation, evidence, claim, fact, relationship, projection, and support boundaries must remain visible.
3. **Compatibility preservation matters.** Recovery changes should preserve public behavior while separating local owners or handoffs.
4. **Authority humility matters.** Projection is not authority; import is not verification; visibility is not existence; prediction is not observation; handoff is not architecture authority.
5. **Read-only diagnostics must not mutate cluster truth.** Diagnostic and inquiry surfaces repeatedly declare no recording, no event-ledger writes, and no cluster mutation unless intentionally recorded under a diagnostic scope.
6. **Exploratory vocabulary is not automatically architecture.** Current-work-position, active-edge, selection, attention, inquiry frontier, and similar labels remain exploratory until reconciled or implemented.

### Implementation backing

Values are partly implementation-backed and partly methodological.

Implementation-backed examples include `QuestionSurfaceInventoryRow.authority_boundary` fields for read-only/mutation boundaries and pressure audit code that ranks existing visibility surfaces without planning, recording, or mutating state. Tests around diagnostic inventory, question surface inventory, projection shape, inquiry orientation, and authority-aware surfaces preserve these boundaries.

Methodological examples include broad architectural humility statements in status/frontier documents and family completion audits. They are stable and recurring, but not all values have a single runtime owner.

## Pressure characterization

### Where pressure begins

Pressure begins when existing repository evidence shows that something currently deserves attention. Implementation-backed pressure begins at the pressure audit builder: it aggregates existing visibility surfaces and converts local candidates into `PressureItem`s with bounded category, score, evidence, reason, and recommended inspection command.

The pressure methodology broadens this beyond the live CLI surface: architectural pressure begins when one owner or corridor carries multiple behaviorally real responsibilities whose boundary, authority, compatibility contract, or stopping point is not independently visible enough for safe local change.

### Where pressure stops

Pressure stops at **attention and inspection**, not at purpose, planning, mutation, or automatic inquiry execution. The pressure audit recommends inspection commands; it does not mutate state or select a next implementation. Completion-audit methodology says pressure is eliminated for a bounded family when same-family compressed owners are gone, public behavior is preserved, tests/audits preserve the boundary, counterexamples fail, and remaining pressure is classified as adjacent, unsupported, historical, residual, or frontier.

### Does pressure drive inquiry or inform inquiry?

Pressure informs inquiry. It can supply evidence that an unanswered question matters, but it does not by itself authorize a new family, runtime behavior, or next slice. `docs/repository_pressure_inventory.md` explicitly says the pressure inventory is not a roadmap, architecture, future-state vision, strategy, autonomous-agent design, maturity model, ontology, or grand framework. `docs/architectural_status_and_next_frontier.md` likewise treats characterized frontiers as inputs to future inquiry, not canonical architecture or implementation-ready by default.

## Inquiry characterization

### Where inquiry begins

Executable inquiry begins with exact bounded selection, not free-text purpose interpretation. The current path is:

```text
ask --question-family <exact QuestionFamily>
  -> inventory lookup
  -> bounded status / required argument validation
  -> mapped dispatch surface selection
  -> existing answering surface formatter or JSON handler
```

The question surface inventory owns the subject-to-answering-surface relationship through fields such as question family, surface, surface flag, answer responsibility, authority boundary, bounded status, dispatch surface, required arguments, diagnostic registrations, and relationship status.

Documentation inquiry begins when a concrete unanswered operator question is important, recurring, and not already answered by existing documents or surfaces.

### Where inquiry stops

Executable inquiry currently stops at dispatch to an existing answer surface. The inquiry presentation audit found that bounded inquiry does not yet select newer subject-specific presentation-composed explanation surfaces; it terminates at the raw mapped surface.

Inquiry Orientation stops even narrower: it preserves operator prose and related material, but it does not promote the note into intent, fact, ownership, recommendation, runtime instruction, or next safe move.

### What currently selects the next inquiry?

There are two selectors:

1. **Executable selector:** exact `QuestionFamily` and bounded ask maps select the answering surface.
2. **Methodological selector:** current architectural routing selects future investigation only when a concrete operator question is important, recurring, and unanswered by existing documents or surfaces.

Pressure is one input into the methodological selector. Current architectural status, reconciled values, implementation evidence, completion audits, and unsupported-conclusion boundaries also constrain selection.

## Counterexamples reviewed

### Pressure acting as repository purpose

Counterexample evidence was sought in pressure audit, pressure inventory, operational brief, status/frontier documents, and pressure methodology. The evidence does **not** support pressure as purpose. The pressure audit ranks current operational pressures and recommends inspection commands. The pressure inventory explicitly denies roadmap, architecture, future-state vision, strategy, autonomous-agent design, maturity model, ontology, and grand-framework status. Pressure therefore informs what deserves attention; it does not define why Seed improves.

### Inquiry acting as repository purpose

Counterexample evidence was sought in inquiry frontier, inquiry presentation audit, question surface inventory, inquiry orientation, and bounded question discipline. The evidence does **not** support inquiry as purpose. Inquiry is bounded dispatch, read-only orientation, or exploratory frontier work. It is not a universal repository objective, planner, or semantic purpose interpreter.

### Values changing because pressure changes

No implementation-backed evidence was found that values change because pressure changes. Pressure outputs can change category and score, but read-only boundaries, evidence/provenance preservation, compatibility preservation, and authority humility remain stable constraints across surfaces and family completion reports.

### No stable repository direction exists

This counterexample is not supported. The repository has stable direction through architectural status, claim-centric ontology, preservation boundaries, and repeated bounded-cleanup routing. However, the direction is not implemented as a separate Purpose component.

## Supported conclusions

1. **The repository already distinguishes Pressure and Inquiry implementation-backed.** Pressure has `PressureAudit` and pressure item records; Inquiry has exact `QuestionFamily` inventory, eligibility, selection, and dispatch surfaces.
2. **The repository already distinguishes Values methodologically and partially in implementation.** Authority boundaries, read-only/no-mutation constraints, evidence preservation, and compatibility-preserving recovery recur across code, tests, audits, and status documents.
3. **Purpose exists as stable methodology, not as a first-class implementation owner.** It is visible in architectural status and recurring constraints: claim-centric knowledge, evidence/provenance preservation, boundary humility, and bounded implementation cleanup.
4. **Pressure begins at evidence-backed attention signals and stops before purpose or autonomous action.** It recommends inspection and frames unresolved compression; it does not authorize mutation or select an architecture by itself.
5. **Inquiry begins at bounded question/work selection and stops at the selected answer surface or documented unsupported boundary.** Inquiry does not infer free-text purpose or operator intent.
6. **Pressure informs Inquiry; it does not drive Inquiry unilaterally.** Inquiry selection also depends on exact dispatch eligibility, architectural status, concrete unanswered operator questions, completion-audit evidence, and value constraints.
7. **Stable across completed families:** compatibility preservation, public behavior preservation, explicit owners/handoffs, tests or audits for recovered boundaries, same-family stopping conditions, and classification of residual pressure as adjacent/unsupported/frontier.
8. **No new architectural family is implementation-backed by this characterization.** The recurring relationship is important, but current evidence supports a report and future bounded inquiry only, not a new family.

## Unsupported conclusions

The reviewed repository evidence does not support these claims:

- Seed has a first-class implemented Repository Purpose component.
- Pressure is repository purpose.
- Inquiry is repository purpose.
- Pressure automatically selects or executes the next inquiry.
- Values change when pressure scores change.
- A motivation engine, goal planner, autonomous planner, reward system, agent architecture, runtime redesign, schema change, or behavior change is justified.
- Current-work-position, active-edge, selection, attention, or inquiry-frontier vocabulary is implementation-ready by default.
- A new architectural family is justified solely because Purpose/Values/Pressure/Inquiry can be characterized.

## Confidence

- **High** that Pressure and Inquiry are distinct implementation-backed responsibilities.
- **High** that pressure informs rather than commands inquiry.
- **Medium-high** that repository Values are stable across completed families and current surfaces.
- **Medium** that Purpose is accurately characterized as stable methodological direction rather than an implemented component.
- **Low** that a new implementation family is currently justified.

## Recommendation on new family

**Insufficient implementation evidence.**

Do not open a new architectural family for Purpose, Values, or Purpose/Pressure/Inquiry unless future work finds recurring implementation ownership rather than recurring architectural philosophy. The smallest repository-backed result of this investigation is this characterization report.
