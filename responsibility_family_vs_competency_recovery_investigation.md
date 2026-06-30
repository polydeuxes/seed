# Responsibility Family vs Competency Recovery Investigation

Repository authority wins. This investigation does not perform implementation slices, runtime changes, schema changes, CLI changes, vocabulary migration, roadmap redesign, new abstractions, or new architectural layers. It recovers the implementation-backed distinction already present in repository evidence.

## Executive answer

Implementation evidence distinguishes the two concepts this way:

- A **Responsibility Family** is a bounded ownership recovery unit: a sequence of recovered architectural boundaries that share an implementation ownership chain, can be projected through compatibility-preserving implementation slices, and reaches natural completion when the known boundaries in that chain have been made explicit.
- A **Competency** is a recurring bounded work discipline: a repeatable capability or review move that appears across multiple implementation owners, preserves common invariants, and terminates at its local boundary without requiring one shared implementation owner, class hierarchy, module hierarchy, runtime service, interface, or API.

They are therefore **orthogonal architectural concepts** in the current repository evidence:

- Responsibility families organize **where bounded ownership lives and how recovered boundaries are projected into implementation**.
- Competencies organize **what recurring bounded work Seed must be able to perform or preserve across owners**.

Evidence Interpretation is the decisive counterexample to collapsing them. The competency recovery investigation finds one Evidence Interpretation competency expressed through several owners, while also stating that the repository does not implement a generic Evidence Interpretation service or responsibility family. Conversely, Operational Responsibility, Execution Visibility, Observation-Derived Capability, and Answer Composition are responsibility families because repeated slices expose shared ownership chains and natural completion points.

## Evidence base reviewed

This report reviewed implementation-backed artifacts around:

- Operational Responsibility slices 001 through 006.
- Execution Visibility slices 001 through 005.
- Observation-Derived Capability slices 001 through 005.
- Answer Composition slices and family completion audit.
- Evidence Interpretation competency recovery investigation.
- Competency roadmap v1 and v2.
- Architectural projection lineage and slice methodology.
- Responsibility-family completion audits and inventory audits.
- Architectural inquiry orientation and responsibility-to-inquiry boundary investigations.

Prior reports are used only where they cite or summarize implementation evidence, tests, compatibility preservation, or explicit negative authority. Repository source and tests remain stronger authority than architectural prose.

## Implementation-backed definition: Responsibility Family

A **Responsibility Family** is an implementation-backed ownership family formed by multiple recovered architectural boundaries that belong to one coherent ownership chain.

The repository evidence supports these characteristics.

### 1. Shared ownership chain

Responsibility families are recovered from ownership seams, not labels. Operational Responsibility is a chain from capability recommendation through operation selection, validation, authorization, execution realization, execution recording, and post-execution knowledge extraction. Execution Visibility is a chain from status emission/consumption through timing, cache visibility, diagnostics, state-build visibility, and projection-cache diagnostics. Observation-Derived Capability is a chain from observed evidence through verification, promotion readiness, inventory, and executable operation contract separation.

The chain may cross files or classes, but the family is defined by the shared ownership problem being separated into bounded handoffs.

### 2. Recoverable implementation boundaries

A family is made of recovered boundaries such as:

```text
Capability Recommendation != Operation Selection
Status Emission != Status Consumption
Observed Evidence != Capability Verification
Repository Knowledge != Answer Composition != Rendering
```

The effective implementation unit is the recovered architectural boundary, not a class, module, subsystem, or directory.

### 3. Implementation slices

Families are projected by slices that make one already-recovered boundary explicit while preserving behavior and compatibility. The recurring slice pattern is:

```text
recover boundary
recover implementation evidence
identify compressed ownership
make one boundary explicit
preserve compatibility
stop
```

A responsibility family is therefore not merely a conceptual grouping. It is recoverable because the repository can point to completed slices, implementation changes, tests or generated architecture evidence, compatibility preservation, and adjacent compressed boundaries.

### 4. Natural completion

A responsibility family reaches a natural stopping point when every currently recovered boundary in that family has an implementation-backed slice and further work would require recovering new boundaries rather than projecting known ones.

Completion is not a manual status flag. It is an evidence condition: recovered boundaries have crossed the slice pattern, remaining gaps are explicitly outside the completed chain or future-family candidates, and compatibility was preserved.

### 5. Implementation-local ownership transitions

Responsibility-family evidence is strongest when it shows implementation-local transitions: selected operation resolution differs from provider recommendation; policy authorization differs from registered validation; status consumption differs from status emission; capability inventory differs from executable operation contract; answer composition differs from compatibility object handoff and rendering.

These transitions may live in adjacent functions, private dataclasses, services, or builder paths. The key evidence is the ownership handoff, not the syntax used to express it.

## Implementation-backed definition: Competency

A **Competency** is recurring bounded work and discipline that Seed needs across implementation owners. It is not necessarily one implementation owner.

The current roadmap and Evidence Interpretation recovery support these characteristics.

### 1. Recurring bounded work

Competencies are named by repeatable work, such as Target Orientation, Evidence Visibility, Evidence Interpretation, Inquiry Navigation, Bounded Work Recovery, Responsibility Evaluation, and Bounded Answer Composition.

For Evidence Interpretation, the repeatable work is visible-evidence consumption, deterministic repository rule application, interpreted output emission, provenance preservation, authority-boundary declaration, and termination before downstream authority.

### 2. Shared implementation discipline

A competency is unified by common discipline rather than one shared class. Evidence Interpretation appears in fact support selection, explanation building, capability inventory, verification inspection, promotion readiness, relationship catalog mapping, reasoning path audit, selection path audit, inquiry orientation, and operational story composition.

These owners share rules: consume visible evidence, preserve provenance, distinguish authority, avoid promotion, and stop before mutation, execution, or unsupported semantic inference.

### 3. Repeated invariants

Competencies preserve repeated invariants across owners. Evidence Interpretation repeatedly preserves:

- provenance and support;
- authority and non-promotion boundaries;
- read-only diagnostic or inquiry posture where applicable;
- explicit unknown/unsupported outcomes instead of forced conclusions;
- termination before execution, mutation, durable promotion, or final answer authority unless a separate owner performs that work.

The competency roadmap generalizes the same discipline: visibility precedes interpretation, interpretation precedes responsibility claims, bounded work precedes responsibility evaluation, and answer composition preserves support, boundaries, limitations, unknowns, and refusal conditions.

### 4. Cross-family recurrence

A competency can recur inside multiple responsibility families. Evidence Interpretation appears inside Observation-Derived Capability through verification, readiness, and inventory; inside Answer Composition through operational story and inquiry orientation answer material; inside visibility/audit surfaces through reasoning and selection path audits; and inside state/read-model support through fact support and explanation.

This recurrence is the reason Evidence Interpretation is implementation-backed as one competency but not currently implementation-backed as one responsibility family.

### 5. Termination discipline

Competencies are bounded by stop conditions. Evidence Interpretation stops before promotion, execution, mutation, policy approval, semantic intent recovery, or truth creation. Inquiry Navigation stops when no implemented surface can answer. Bounded Work Recovery stops when evidence begins from nouns, labels, or presentation vocabulary instead of performed work. Bounded Answer Composition stops rather than filling gaps without support.

### 6. Authority discipline

Competencies are heavily authority-shaped. They determine what evidence authorizes, excludes, supports, contradicts, or leaves unknown. This is broader than ownership: the same authority discipline can be required by many owners.

## Shared characteristics

Responsibility families and competencies share several repository-backed traits:

1. **Both are implementation-backed.** Neither should be accepted from preferred vocabulary or architectural preference alone.
2. **Both are boundary-oriented.** Families separate ownership boundaries; competencies preserve work/authority/termination boundaries.
3. **Both require negative authority.** They must state what they do not own, do not infer, do not mutate, or do not promote.
4. **Both preserve compatibility.** Families do this through slices; competencies do this by stopping before downstream authority and preserving existing surfaces.
5. **Both reject presentation vocabulary as automatic knowledge.** Labels do not become families or competencies without implementation evidence.

## Distinguishing characteristics

| Question | Responsibility Family | Competency |
| --- | --- | --- |
| Primary axis | Ownership and implementation boundary projection | Recurring bounded work and discipline |
| Evidence shape | Completed or candidate slices, owner handoffs, compatibility-preserving implementation changes, natural completion | Repeated invariants across owners, bounded work descriptions, authority and stop conditions |
| Unit of progress | One recovered architectural boundary made explicit | One repeatable capability/discipline preserved across contexts |
| Completion signal | Known recovered boundaries in the family have slices and remaining gaps are outside the chain | Roadmap readiness/proceed/stop conditions; may be methodological before being a runtime capability |
| Relation to owner | Requires stable or recoverable ownership chain | May intentionally span several owners |
| Relation to API/service | Does not require a shared API/service, but may have concrete owner seams | Does not require and may lack a shared API/service |
| Counterexample risk | Overclaiming all adjacent architecture complete | Collapsing a cross-cutting discipline into a premature generic owner |

## Relationship between them

### Can one competency span multiple responsibility families?

**Yes, implementation evidence supports this.** Evidence Interpretation spans multiple owners and family areas. It appears in capability verification/readiness/inventory, fact support and explanation, relationship catalog mapping, reasoning and selection audits, inquiry orientation, and operational story. The Evidence Interpretation report explicitly concludes that it is one competency expressed through several implementation families, not one single runtime owner.

### Can one responsibility family contribute to multiple competencies?

**Yes, but repository evidence supports this as contribution, not identity.** Answer Composition contributes to Bounded Answer Composition and also exercises Evidence Interpretation where it interprets material into answer/reason/support/boundary/limitations. Observation-Derived Capability contributes to Evidence Visibility, Evidence Interpretation, Bounded Work Recovery, and Responsibility Evaluation through observed evidence, verification, promotion-readiness, and inventory boundaries. Execution Visibility contributes to Evidence Visibility and Evidence Interpretation through diagnostic inventory, timing/cache/status distinctions, and read-only diagnostic boundaries. Operational Responsibility contributes to Bounded Work Recovery and Responsibility Evaluation through explicit operational handoffs and negative authority.

The relationship is many-to-many, but not because of a new taxonomy. It follows from observed implementation: ownership chains perform work that participates in more than one recurring competency discipline.

### Are they orthogonal architectural concepts?

**Yes, with a bounded meaning of orthogonal.** They are orthogonal because one axis asks which implementation owner or ownership chain owns a boundary, while the other asks what recurring bounded work discipline is being exercised. They are not unrelated: competencies are exercised by owners, and responsibility families may supply evidence for competencies. But neither axis reduces to the other.

## Dependency on hierarchy, layout, runtime service, interface, or API

Current evidence does **not** show that either concept depends on:

```text
class hierarchy
module hierarchy
directory layout
runtime service
shared interface
shared API
```

The projection methodology explicitly says implementation did not evolve class-by-class, module-by-module, or subsystem-by-subsystem; the effective unit was the recovered architectural boundary. The Evidence Interpretation investigation explicitly says there is no generic EvidenceInterpretation service and no current shared API or compatibility surface that would justify adding a generic implementation family.

Concrete code structures matter as evidence, but they are not the defining criterion. A private dataclass, function boundary, service method, diagnostic row, audit builder, catalog lookup, or test can all be evidence if it proves ownership, handoff, authority, support, or termination.

## Counterexamples reviewed

### Competency collapses into one owner

No reviewed evidence shows Evidence Interpretation collapsing into one current owner. The opposite is supported: the competency is distributed across several owners, and a generic owner is explicitly unsupported without a compression point, shared API, or compatibility surface.

A future competency could become one owner if implementation evidence later showed a real compression point. That is unsupported for Evidence Interpretation now.

### Responsibility family lacks bounded ownership

Candidate or adjacent areas sometimes lack bounded ownership and therefore remain future work rather than completed families. Repository Observation Acquisition has adapter evidence, but acquisition workflow ownership is not stabilized across traversal, filtering, ingestion, command, and query surfaces. Responsibility-Family Status Inquiry can be manually answered from evidence but lacks a dedicated runtime inquiry surface. Presentation-only orientation vocabulary has insufficient evidence when unsupported by implementation reachability.

These counterexamples reinforce the distinction: recurring interest or vocabulary is not enough for a responsibility family.

### Implementation slices do not align with a family

The slice methodology reports the opposite for completed families: slices aligned with recovered family boundaries. However, it also warns that not every architectural area is proven to decompose this way. Remaining compressed boundaries around pending actions, projection build diagnostics, fact-index cache timing, writable capability promotion/admission, and additional inquiry surfaces are valid adjacent work, not evidence that the completed family definition should stretch to include them.

### Recurring bounded work does not align with ownership

Evidence Interpretation is the clearest example. Its recurring bounded work appears across owners and does not align with one responsibility family. Inquiry Navigation also appears as bounded navigation across exact ask dispatch, inquiry orientation, source navigation, reasoning/selection path surfaces, diagnostic inventory/shape audit, and existing investigations rather than one runtime planner.

## Supported conclusions

Supported by implementation evidence:

1. Responsibility Family is an ownership/boundary-projection concept.
2. Competency is a recurring bounded-work and discipline concept.
3. Responsibility families are characterized by shared ownership chains, recoverable implementation boundaries, implementation slices, natural completion, and implementation-local ownership transitions.
4. Competencies are characterized by recurring bounded work, shared implementation discipline, repeated invariants, cross-owner recurrence, termination discipline, and authority discipline.
5. Neither concept currently depends on class hierarchy, module hierarchy, directory layout, runtime service, shared interface, or shared API.
6. A competency can span multiple responsibility families; Evidence Interpretation does so now.
7. A responsibility family can contribute to multiple competencies; the completed families do so through visibility, interpretation, bounded work recovery, evaluation, and answer composition disciplines.
8. Evidence Interpretation should remain a competency and review discipline unless a future concrete implementation compression point appears.
9. Repository authority supports orthogonality between the axes, not replacement of one by the other.

## Unsupported conclusions

Not supported by current implementation evidence:

1. Evidence Interpretation is one implemented responsibility family or generic runtime service.
2. Competencies should be implemented as shared base classes, registries, services, interfaces, or APIs.
3. Responsibility families should be reorganized around competency names.
4. The competency roadmap should be redesigned into a taxonomy of families.
5. Every recurring invariant indicates a new owner.
6. Every owner belongs to only one competency.
7. Every responsibility family contributes to every competency.
8. Every competency must span multiple responsibility families.
9. Presentation vocabulary such as continuation, current work position, active edge, or source navigation is architectural knowledge without reachability or implementation evidence.
10. The repository has an autonomous repository-neutral review engine, planner, semantic interpretation system, or generic responsibility evaluator.

## Recommended implications for the competency roadmap

1. **Keep Evidence Interpretation as a competency, not a new responsibility family.** Current evidence supports the roadmap v2 replacement of Authority Interpretation with Evidence Interpretation, but not a generic implementation owner.
2. **Keep Bounded Work Recovery before Responsibility Evaluation.** Responsibility-family evidence shows ownership should be recovered from performed work, handoffs, exclusions, and tests rather than from nouns.
3. **Use responsibility-family evidence as case material for competencies.** Completed families provide strong examples for Evidence Visibility, Evidence Interpretation, Bounded Work Recovery, Responsibility Evaluation, and Bounded Answer Composition.
4. **Do not redesign the roadmap into a taxonomy.** The distinction is already present: families organize implementation ownership; competencies organize recurring bounded disciplines.
5. **Continue requiring proceed/stop criteria.** Competencies should preserve stop conditions when evidence is invisible, unsupported, semantic-only, presentation-only, or authority-limited.
6. **Do not add shared abstractions prematurely.** A new service, API, registry, or interface would need concrete implementation compression evidence, compatibility surface evidence, and tests. Current evidence does not provide that for Evidence Interpretation.

## Final answer to acceptance questions

### What implementation evidence distinguishes Responsibility Families from Competencies?

Responsibility families are distinguished by ownership-chain evidence: recovered boundaries, compressed ownership, one-boundary slices, compatibility preservation, tests or generated architecture evidence, and natural completion. Competencies are distinguished by recurring bounded-work evidence: common invariants, authority boundaries, stop conditions, and repeated discipline across multiple owners without a required shared service.

### Are they orthogonal architectural concepts?

Yes. They are orthogonal axes in current evidence: ownership/boundary projection versus recurring bounded work/discipline. They interact, but neither reduces to the other.

### Can one competency span multiple responsibility families?

Yes. Evidence Interpretation spans fact support, explanation, capability verification/readiness/inventory, relationship catalog mapping, reasoning and selection audits, inquiry orientation, and operational story. The repository supports it as one competency expressed through several implementation families.

### Can one responsibility family contribute to multiple competencies?

Yes. Answer Composition, Observation-Derived Capability, Execution Visibility, and Operational Responsibility each participate in more than one roadmap competency because their implementation boundaries exercise visibility, interpretation, bounded work, evaluation, and answer-composition disciplines.

### What implementation evidence supports those answers?

The strongest support is the contrast between completed responsibility-family slice chains and the Evidence Interpretation competency recovery. The slice chains show family completion through ownership boundaries and natural stopping points. The Evidence Interpretation recovery shows one recurring competency distributed across multiple implementation owners and explicitly rejects a current generic owner, shared service, shared API, or new responsibility-family implementation.
