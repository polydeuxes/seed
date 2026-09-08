# Artifact Kind / Answer Composition Audit

## Scope

This is a bounded architectural audit. It does not implement an artifact registry, artifact framework, base artifact class, renderer, template engine, schema change, CLI change, projection slice, or runtime behavior. It characterizes what the current repository already supports through implementation evidence.

## Executive answer

The repository already supports reading explanations, capability handoffs, operational briefs, investigation reports, projection slice reports, architectural audits, and human summaries as **artifact kinds** produced after an implementation-backed inquiry has yielded a bounded answer.

That support is architectural characterization, not a new runtime object. Current code and reports repeatedly separate:

```text
Implementation evidence
-> question / inquiry surface
-> bounded answer composition
-> consumer-specific artifact organization
-> presentation / rendering
```

The strongest implementation evidence is not a generic `Artifact` class. It is the repeated pattern that builders collect evidence, compose answer payloads or result payloads, preserve lineage/boundary/limitations, and only then hand those materials to a public report/view/explanation/handoff shape or formatter.

Therefore, **explanation is not supported as a unique architectural object**. It is currently an implemented artifact kind: a deterministic, human-readable/provenance-oriented artifact derived from projected fact support for a `why` question. Other output families differ mainly by purpose, consumer, structure, required fields, and boundary wording rather than by ownership of inquiry itself.

## Candidate artifact kinds

| Candidate artifact kind | Existing output examples | Underlying inquiry | Answer source | Artifact purpose | Intended consumer | Presentation | Implementation evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Explanation | `ExplanationBuilder.why(...)` result | Why does the projected state currently support this subject/predicate value? | Projected `State` fact supports, conflicts, facts, entity aliases | Explain current/ambiguous/no-current belief with recursive provenance | Human/operator or caller asking why | `Explanation`, `BeliefExplanation`, `FactExplanation` data shape; renderer may be external | `ExplanationBuilder` builds entirely from projected state and separates current/competing beliefs for future query modes. |
| Capability Handoff | `HandoffPlanService.create_handoff_plan(...)` | What non-executable provider handoff can be described for an accepted action plan? | Accepted `ActionPlan`, capability catalog recommendation, projected state target hints | Carry non-secret, non-executable execution boundary to an external provider/operator | External provider/operator or follow-on executor outside Seed | `HandoffPlan` model plus optional event ledger record | Handoff planning explicitly does not execute, approve, authorize, register tools, ask for credentials, or manage provider jobs. |
| Operational Brief | `OperationalStory` | What is the current operational story from existing diagnostic surfaces? | Pressure audit, capability needs, privilege discovery, correlation audit, impact audit, investigation path audit | Organize current focus, pressure, capabilities, constraints, gaps, impact, changes, outcomes, path, unknowns, and boundary | Operator needing a brief | JSON dict or formatted CLI/report surface | `build_operational_story` composes read-only current operational evidence without planning, recording, or mutation, with implementation-local answer/reason/support/boundary/limitation payloads. |
| Investigation Report | Reasoning/selection/investigation path audits; repository `*_investigation.md` reports | How was a conclusion, selection, vocabulary recovery, or implementation characterization derived? | Implemented diagnostic surfaces, repository files, projected state, prior implementation records | Preserve evidence, intermediate conclusions, consumers, unknowns, supported/unsupported conclusions | Developer/operator reviewing inquiry lineage | Markdown report or audit JSON/text | Reasoning path audit separates derived conclusions from derivation lineage before compatibility handoff. |
| Projection Slice Report | `*_slice_*.md` reports, projection shape visibility | What implementation slice changed or what projection stage shape is visible? | Code/test diffs, projection stage declarations, diagnostics, tests | Record implementation-backed slice boundary, compatibility impact, tests, and next edges | Maintainer reviewing incremental architecture recovery | Markdown report; projection shape JSON/text elsewhere | Projection shape stages expose consumes/produces/influences/does-not-influence/authority boundary; slice docs preserve implementation diff/test evidence. |
| Architectural Audit | `*_audit.md` reports and architecture conformance audit | What responsibility boundary or architectural relation is supported by repository evidence? | Code, tests, diagnostic surfaces, docs, operational graph | Characterize supported and unsupported conclusions without changing truth | Maintainer/architect | Markdown audit or audit surface JSON/text | Architecture conformance audit reads architecture references and operational graph evidence, classifies realization, and remains read-only. |
| Human Summary | State summary, inquiry orientation view, source navigation/context views | What bounded information should be shown to a human without promoting presentation vocabulary to knowledge? | Projected state, source navigation, lexical overlap evidence, summary aggregation | Organize information for human orientation or inspection | Human operator/developer | Text sections and JSON dicts | State summary marks filesystem classification as presentation taxonomy only; inquiry orientation composes answer material before rendering and warns that lexical overlap is not semantic interpretation. |

## Shared inquiry ownership

The repository evidence supports shared inquiry ownership at the level of collecting implementation evidence and answering a bounded question, but it does **not** support a single universal inquiry runtime object.

Repeated owners are surface-specific:

- `ExplanationBuilder` owns why-query answer construction over projected state, not fact creation or authority resolution.
- `build_operational_story` owns a read-only operational story view assembled from existing visibility surfaces, not planning, recording, or mutation.
- `build_reasoning_path_audit` owns derivation-path visibility from implemented diagnostic surfaces, not creation of the underlying conclusions as cluster truth.
- `build_selection_path_audit` owns selection trace visibility, not new selection authority.
- `HandoffPlanService` owns non-executable handoff boundary description from an accepted action plan, not execution.
- `build_inquiry_orientation` owns bounded orientation for preserved notes, not note interpretation as facts, goals, requirements, or workflow movement.

This means the repository already allows multiple artifacts to share the same **inquiry pattern**:

```text
collect implementation evidence
answer a bounded question
preserve lineage / boundary / limitations
shape for a consumer
render or serialize
```

But it does not yet implement, and this audit does not recommend immediately implementing, a generic inquiry mechanism or artifact mechanism.

## Shared answer composition

Answer composition is already visible as a responsibility distinct from evidence collection and presentation.

Implementation examples:

1. **Architectural orientation.** `_collect_architectural_orientation_evidence(...)` collects related material from projected facts and source navigation. `_compose_architectural_orientation_answer(...)` then builds an answer with answer material, reason, support, boundary, and limitations before `format_inquiry_orientation(...)` renders text sections.
2. **Operational story.** `build_operational_story(...)` gathers pressure, capability needs, privilege discovery, correlation, impact, and investigation path inputs. `_compose_operational_story_payloads(...)` separates answer, reasoning, support, boundary, and limitations before `OperationalStory` is constructed.
3. **Reasoning path audit.** `build_reasoning_path_audit(...)` collects evidence, intermediate conclusions, derived conclusions, consumers, story impact, and unknowns, then separates `_DerivedConclusionPayload` from `_DerivationLineagePayload` before returning `ReasoningPathAudit`.
4. **Selection path audit.** `build_selection_path_audit(...)` separates `_SelectionResultPayload` from `_SelectionLineagePayload` before constructing `SelectionPathAudit`.
5. **Explanation.** `ExplanationBuilder.why(...)` collects fact supports/conflicts and returns an `Explanation` whose status and current/competing beliefs are separate from the recursive fact explanations used as support.

These are not identical implementations, but the architectural relationship is consistent: answer composition owns the bounded answer and its support frame; it does not own the final consumer-specific organization in every case, and it does not own presentation vocabulary as repository truth.

## Artifact-specific composition

The artifacts differ primarily in artifact-kind concerns:

- **Purpose.** Explanation explains why a belief is current or ambiguous; a handoff describes a provider boundary; an operational brief summarizes current operational pressure; an investigation report preserves derivation; a projection slice report records implementation slice impact; an architectural audit classifies supported conclusions; a human summary orients a person.
- **Consumer.** Some artifacts target operators, some maintainers, some external providers, some future implementation work.
- **Structure.** Explanation requires status/current beliefs/competing beliefs/conflicts. Handoff requires provider/backend/operation/target/policy/secret boundary/executable flag. Operational story requires focus/pressure/capabilities/constraints/impact/path/unknowns/boundary. Audits require evidence/conclusions/unknowns/boundary. Summaries require selected display categories and explicit presentation boundaries.
- **Required fields.** The required fields come from the consumer and purpose, not from a different inquiry owner.

This supports treating `Explanation`, `Capability Handoff`, `Operational Brief`, `Investigation Report`, `Projection Slice Report`, `Architectural Audit`, and `Human Summary` as artifact kinds derived from answer composition.

## Presentation boundaries

Presentation remains downstream from artifact composition and must not silently become knowledge.

Repository evidence repeatedly enforces this boundary:

- `format_inquiry_orientation(...)` renders inquiry-orientation sections after answer composition; its authority boundary says the note is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction.
- State summary filesystem categories are explicitly presentation taxonomy and do not assert ownership, shared storage identity, or topology truth.
- Inquiry artifact visibility states that findings, supported conclusions, unsupported conclusions, and open questions may be visible as outputs/documents without becoming a generalized runtime artifact model.
- Diagnostic and audit outputs often include `records_facts=false`, `writes_event_ledger=false`, and `mutates_cluster=false` boundaries.

Thus the supported chain is:

```text
Answer Composition owns bounded answer.
Artifact Composition owns consumer-specific organization.
Presentation owns rendering/serialization labels.
Repository truth remains with implementation evidence, projection, event replay, and explicit mutation paths.
```

## Counterexamples and exclusions

Some repository outputs genuinely require different mechanisms and remain outside artifact composition:

1. **Runtime mutation.** Runtime decision routing, state patches, event appends, pending actions, approvals, and execution authorization are not artifact composition. They can produce records that later become evidence, but the mutation itself is operational behavior.
2. **Event recording.** Event ledger writes are durable state history, not a presentation artifact. Handoff creation may append an event when a ledger is supplied, but that is a record of handoff-plan creation, not artifact rendering.
3. **Execution.** Registered operation execution belongs to execution services and policy boundaries, not to artifact composition. Handoff plans explicitly remain non-executable.
4. **Projection.** Projection stages consume event ledger and facts to produce projected read models, aliases, supports, relationships, and graph issues. Artifact composition may read projections but does not own projection authority.
5. **State evolution.** Anything that changes cluster truth, projected truth, event truth, or persistent repository truth is outside artifact composition unless an explicit implementation path says otherwise.

These counterexamples prevent over-generalization. Artifact composition can describe, summarize, explain, or hand off bounded answers. It cannot replace mutation, execution, projection, or state-evolution mechanisms.

## Supported conclusions

1. The repository already supports `Artifact` as a first-class **architectural characterization** derived from answer composition, even though it does not implement a first-class artifact runtime object.
2. Explanation is one artifact kind among many, not a special architectural object.
3. Capability handoffs, operational briefs, investigation reports, projection slice reports, architectural audits, and human summaries share an evidence/question/answer path more than they share a concrete schema.
4. Differences among those outputs are primarily artifact purpose, consumer, structure, required fields, presentation, and boundary language.
5. Answer composition should own bounded answers, support, reason, boundary, and limitations.
6. Artifact composition should own consumer-specific organization and required fields without changing repository truth.
7. Presentation should own rendering and labels, and those labels should not become repository knowledge without implementation evidence.
8. Runtime mutation, event recording, execution, projection, and state evolution remain outside artifact composition.

## Unsupported conclusions

1. Unsupported: the repository has a generic artifact registry, framework, base class, schema, or renderer.
2. Unsupported: all outputs should be normalized into one concrete artifact model now.
3. Unsupported: explanation should replace answer composition as the architectural center.
4. Unsupported: presentation vocabulary alone is sufficient to create repository knowledge.
5. Unsupported: handoff artifacts are executable or authorize execution.
6. Unsupported: diagnostic findings, open questions, or supported/unsupported conclusions are already modeled as generalized runtime inquiry artifacts.
7. Unsupported: projection slices, runtime state changes, event recording, or execution can be recovered as mere artifact composition.

## Answers to explicit questions

### Is explanation a special architectural object, or one artifact kind among many?

Explanation is one artifact kind among many. Its implementation is real and specific, but its architectural role is not unique: it organizes a bounded answer and support frame for a why-query consumer. Other repository outputs do the same for different consumers and purposes.

### Does the repository already support `Artifact` as a first-class architectural characterization derived from Answer Composition?

Yes, as an architectural characterization. The repository already contains multiple implementation-backed outputs that can be characterized as artifact kinds produced after answer composition. No repository evidence supports a generic runtime artifact framework or registry.

### Should future capability handoffs, briefs, reports, and explanations be recovered as artifact kinds rather than independent architectural responsibilities?

Yes, when the output is read-only or boundary-descriptive and differs mainly by purpose, consumer, structure, required fields, or presentation. Future recovery should first classify the output as an artifact kind derived from answer composition before introducing a new architectural responsibility. New responsibility should be introduced only when implementation evidence shows a different mechanism such as mutation, execution, projection, recording, or state evolution.

## Relationship between Answer Composition, Artifact, and Presentation

```text
Answer Composition
  owns: bounded answer, reason, support, boundary, limitations
  does not own: consumer-specific report shape as a universal schema, rendering labels, mutation

Artifact
  owns: consumer-specific organization of an already bounded answer
  examples: explanation, handoff, brief, report, audit, summary
  does not own: repository truth, projection authority, event recording, execution

Presentation
  owns: text/JSON/CLI/Markdown rendering and labels
  does not own: knowledge promotion, architectural truth, state mutation
```

This relationship further simplifies the architectural model because it avoids treating every human-facing output as an independent architectural responsibility.

## Recommended next implementation step

Do not implement an artifact framework yet.

The next smallest implementation-backed step should be a **single compatibility-preserving refactor in one existing output builder** where answer payload and artifact-shaping payload are still compressed. A good candidate is a diagnostic or audit builder that already has tests and public shape-audit coverage. The refactor should:

1. introduce private implementation-local payloads only;
2. separate bounded answer material from artifact-specific organization;
3. preserve public JSON/text/CLI behavior exactly;
4. update or add tests proving the unchanged public surface; and
5. run the relevant diagnostic inventory and diagnostic shape-audit tests if a diagnostic surface is touched.

This would continue recovering the architecture through implementation evidence without adding a registry, framework, schema, or runtime artifact abstraction.
