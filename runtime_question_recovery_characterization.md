# Runtime Question Recovery Characterization

## Executive answer

Repository evidence is sufficient to recognize a stable architectural pattern:

```text
mature recovery usually terminates as a runtime-owned question or answer surface,
not as a new durable runtime object that stores the recovered concept forever.
```

The repository does **not** support an absolute rule that Seed always asks instead of remembering. Seed has durable runtime artifacts: event ledgers, evidence, facts, projections, catalogs, state, runtime responses, diagnostic inventory rows, and explicit `QuestionFamily` inventory rows. But those artifacts are justified when they own implementation behavior, projected knowledge, source authority, diagnostic contracts, or public invocation identity.

For the recurring recoveries named in the prompt, the stronger pattern is Path B:

```text
Recovery
  -> New runtime question / answer surface
  -> Answer composed from existing artifacts
```

rather than Path A:

```text
Recovery
  -> New runtime artifact
  -> Stored forever
```

The strongest implementation-backed formulation is:

```text
When Seed discovers a recurring competency,
it normally makes the answerable boundary explicit:
question family, diagnostic surface, audit, explanation, or bounded read model.
It introduces new durable runtime artifacts only when the implementation needs
state, provenance, registry identity, dispatch identity, catalog data, or a
mutation/recording boundary that cannot be composed from existing artifacts.
```

`Methodology Observation`, `Architectural Consequence`, and `Recovery Result` are therefore better characterized, on current evidence, as candidate inquiry surfaces or report sections. Current repository evidence does not justify treating them as new runtime-owned persisted entities.

## Repository evidence reviewed

### Primary implementation evidence

- `README.md` describes Seed as maintaining evidence-backed answers to bounded questions by asking responsible subsystems. It separates Inquiry, Subjects, Responsibilities, Implementations, Answer Composition, Presentation, Authority, Evidence, and Contradictions.
- `README.md` defines the current runtime ownership path as observation intake, evidence preservation, claim normalization, projections, read-only state/impact/support/explanation surfaces, and capability-gap recommendation.
- `README.md` also says Seed is not a planner, workflow engine, reasoning engine, orchestration framework, autonomous execution platform, provider-availability proof system, or host mutation/repair system.
- `seed_runtime/runtime.py` identifies runtime orchestration as routing validated model decisions to owner services without owning their behavior.
- `seed_runtime/question_surface_inventory.py` implements a static inventory of question families and answering surfaces, exact bounded-ask dispatch maps, required argument maps, diagnostic-only family markers, and status derivation.
- `seed_runtime/diagnostic_inventory.py` implements durable diagnostic surface metadata including flags, JSON support, record support, record scope, ledger writing, and cluster-mutation boundaries.

### Primary recovery reports and audits reviewed

Representative repository reports reviewed include:

- `question_family_registration_boundary_audit.md`
- `answer_composition_projection_navigation_audit.md`
- `repository_artifact_runtime_artifact_characterization.md`
- `responsibility_to_inquiry_boundary_audit.md`
- `question_surface_inventory` implementation evidence in `seed_runtime/question_surface_inventory.py`
- `inquiry_eligibility_characterization.md`
- `operator_methodological_selection_characterization.md`
- `pressure_audit_smallest_owner_investigation.md`
- `pressure_audit_responsibility_characterization.md`
- `read_model_ownership_family_completion_audit.md`
- `timing_visibility_current_facts_completion_audit.md`
- `classification_responsibility_characterization.md`
- `projection_diagnostics_family_completion_audit.md`
- `inquiry_note_artifact_characterization.md`
- `question_bounded_work_invocation_investigation.md`
- `bounded_question_discipline_investigation.md`
- `methodology_as_inquiry_subject_investigation.md`
- `translation_surfaces_pattern_investigation.md`
- `docs/understanding_visibility_existing_surface_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`

This was a representative bounded investigation, not a full census of every Markdown file.

## Runtime artifact analysis

### What currently becomes a runtime artifact

A new runtime artifact is justified when implementation evidence needs one of these durable roles:

1. **Observed input or event provenance.** Runtime events and ledgers are durable because Seed receives user input, records decisions/responses, and projects current state from event history.
2. **Evidence and claims.** Evidence, facts, relationships, confidence, contradictions, staleness, and graph issues become runtime artifacts because Seed's claim-centric architecture depends on provenance-backed state.
3. **Projection and read-model state.** Projections and read-only views are runtime artifacts when they expose current composed knowledge or operational state from evidence.
4. **Catalog or registry identity.** Capability catalogs, predicate catalogs, entity type catalogs, relationship catalogs, diagnostic inventory rows, and question-family inventory rows are durable when exact identity, compatibility, or invocation behavior depends on them.
5. **Dispatch or CLI contract.** Exact question family names, diagnostic flags, required surface args, and bounded ask dispatch mappings become implementation artifacts when the CLI needs deterministic acceptance, rejection, or routing.
6. **Recording boundary.** Diagnostic inventory entries become durable because they define whether a surface supports recording, writes the event ledger, and mutates cluster state.

These are real counterweights to a simplistic “questions only” reading. Seed does remember some things. It remembers observations, evidence, facts, projections, catalogs, registered question surfaces, diagnostics, and event history when those are implementation-owned responsibilities.

### What does not automatically become a runtime artifact

Repository evidence rejects automatic promotion from recurring language or recovered concepts into runtime objects. The clearest examples are:

- A recovered family does not become public inquiry identity until it is explicitly represented in `QuestionSurfaceInventoryRow` and bounded ask maps.
- Grammar observation and observation agreement boundaries reject direct promotion into family recovery, responsibility recovery, semantic truth, repository mutation, or cluster mutation.
- Mature repository artifacts can remain documentation-owned responsibilities rather than runtime behavior.
- Presentation vocabulary is not automatically knowledge, and repository instructions require implementation evidence before promoting terms into preserved/projected knowledge.

Therefore recurrence alone is insufficient. A recurring phrase such as `Recovery Result` or `Architectural Consequence` may indicate an inquiry need, but it does not itself prove a runtime owner, schema, store, cache, or persistent family.

## Runtime question analysis

### The repeated path

The repeated mature path in the reviewed recoveries is:

```text
recurring pressure or responsibility
  -> bounded question family / diagnostic / audit / explanation
  -> composed answer from existing state, evidence, code, docs, registries, or diagnostics
  -> explicit boundary, uncertainty, and non-authority
```

This appears across the representative recoveries:

| Recovery area | Tempting artifact reading | Mature implementation-backed reading |
| --- | --- | --- |
| Question Family | Store recovered families automatically | Exact static `QuestionFamily` rows plus bounded ask eligibility and existing answer surfaces |
| Answer Composition | Store composed answers as new truth | Separate answer/result, reason, support, lineage, limitation payloads while preserving public compatibility |
| Pressure | Introduce a generic pressure object/owner | Use pressure audit/brief surfaces to ask what current pressure is and why |
| Ownership | Promote ownership as a universal primitive | Ask bounded authority/ownership questions where implementation supports them |
| Capability Needs | Store needs as new planning truth | Compose read-only capability-gap/recommendation answers from projected knowledge and catalogs |
| Selection Path | Store selection result as durable methodology | Expose why a current selection occurred from candidates, factors, evidence, and unknowns |
| Reachability | Store reachability as knowledge truth | Audit what knowledge is reachable across projected/repository/inquiry/rendered surfaces |
| Current Facts | Store presentation rows as authority | Render current projected facts while preserving projection/source authority boundaries |
| Inquiry Artifacts | Make inquiry artifacts runtime ontology | Classify artifact visibility, evidence, and limitations as bounded visibility answers |
| Question Surface Inventory | Auto-discover question surfaces | Maintain explicit static inventory rows and map-backed dispatch status |
| Inquiry Eligibility | Make eligibility a planning engine | Ask whether exact bounded work may execute under current maps and args |
| Methodological Selection | Store methodology as an owner | Characterize selection as inquiry subject or explanation surface when evidence supports it |

The important distinction is not “no code changes.” Some of these surfaces are implemented code. The distinction is that the implemented artifact usually owns **the question contract and composition boundary**, not a newly persisted conceptual object corresponding to every recovered noun.

### Why asking is preferred over remembering in mature recoveries

The preference is architectural, not stylistic:

1. **Authority remains with existing evidence.** If an answer can be composed from event history, state, repository files, catalogs, diagnostic registries, or code structure, storing another truth copy would create duplicate authority.
2. **Uncertainty remains visible.** Many surfaces preserve unknowns, unsupported targets, non-selected candidates, limitations, and boundary strings rather than filling gaps with durable claims.
3. **Non-promotion boundaries remain intact.** Recurrence, grammar, presentation labels, and methodological observations are not promoted into runtime truth without explicit implementation backing.
4. **Compatibility stays bounded.** Question-family rows and dispatch maps make public answerability exact and testable, rather than letting recovered vocabulary mutate runtime capability.
5. **Diagnostic surfaces remain read-only by default.** Diagnostic inventory requires record scope and mutation metadata, preserving the line between diagnostic output and cluster truth.

## Comparative analysis

### Path A: recovery -> new runtime artifact -> stored forever

Path A is supported only under stricter conditions. It appears when Seed needs durable implementation state or exact registry identity. Examples include:

- event ledger records;
- evidence and facts;
- projected state and read models;
- catalog entries;
- diagnostic inventory rows;
- question surface inventory rows;
- bounded ask dispatch maps;
- CLI flags and recordability contracts.

Path A is not supported merely because a recovery names a recurring behavior, methodology, consequence, result, pressure, or family.

### Path B: recovery -> new runtime question -> answer composed from existing artifacts

Path B is the more common mature path in the reviewed architectural recoveries. It appears when Seed needs operator-facing clarity, diagnostic visibility, explanation, boundary preservation, or answer composition without creating duplicate source-of-truth state.

The evidence is especially strong for question families, answer composition, selection path, pressure, reachability, current facts, diagnostic inventory/shape surfaces, and artifact/runtime distinction reports.

## Counterexamples and limits

### Counterexample 1: Question families are durable runtime artifacts

Accepted. `QuestionFamily` identity is a durable implementation artifact once encoded in the static inventory and dispatch maps. But this counterexample supports the boundary rather than defeating it: the repository does not automatically recover question families from recurring prose. It registers exact answerable identities explicitly and maps them to existing answering surfaces.

### Counterexample 2: Diagnostic inventory is a durable runtime artifact

Accepted. Diagnostic inventory entries persist diagnostic contracts. They are justified because operational surfaces must disclose flags, recordability, ledger writes, JSON support, and cluster mutation boundaries. This is a runtime artifact introduced to govern visibility of questions and diagnostics, not a generic store for every recovered methodology observation.

### Counterexample 3: Evidence, facts, projections, and catalogs are durable runtime artifacts

Accepted. Seed's core claim-centric runtime requires durable evidence and projected knowledge artifacts. This means the constitutional preference is not “never remember.” The preference is “remember observations/evidence/claims/registries when ownership requires it; ask bounded questions over them when composition is sufficient.”

### Counterexample 4: Some answer surfaces have code-local payload objects

Accepted. Answer-composition slices introduce or refine payload classes. These are implementation artifacts. But their role is to separate result, reason, support, lineage, and limitations for public compatibility; they do not make every answer a new stored truth family.

### Counterexample 5: Repository artifacts are durable

Accepted. Documentation itself is durable repository memory. But prior characterization distinguishes repository artifacts from runtime artifacts. A mature report can remain a repository artifact that informs future work without becoming runtime-owned state.

## Supported conclusions

1. **When architectural recovery succeeds, what usually becomes runtime?**

   Usually the bounded question/answer contract becomes runtime: a diagnostic surface, audit, read-only view, question-family inventory row, bounded ask dispatch mapping, explanation surface, or answer-composition boundary. The recovered noun itself usually does not become a new durable runtime entity unless implementation ownership requires durable state or exact registry identity.

2. **Does the repository more commonly recover artifacts or questions?**

   In the reviewed architectural recovery reports, it more commonly recovers questions: “What pressure is active?”, “Who owns this answer?”, “What capability is needed?”, “Why was this selected?”, “What is reachable?”, “What facts are current?”, “Which surface answers this family?”, and “Is this inquiry eligible?”

3. **What implementation evidence supports that conclusion?**

   The clearest implementation evidence is the static question surface inventory and bounded ask maps, the diagnostic inventory, read-only diagnostic boundaries, runtime orchestration routing to owner services, and README's bounded-question framing. These show explicit answerability, routing, and diagnostic contracts rather than automatic concept persistence.

4. **When is a new runtime artifact actually justified?**

   A new runtime artifact is justified when Seed needs durable observations, evidence, facts, projections, catalogs, registry identity, exact dispatch identity, compatibility behavior, event history, diagnostic metadata, recordability metadata, or a mutation boundary that cannot safely be recomposed from existing artifacts.

5. **When is a new runtime question sufficient?**

   A new runtime question is sufficient when the answer can be composed from existing state, evidence, catalogs, diagnostics, code, docs, or registries while preserving authority, uncertainty, and boundaries. It is especially sufficient for pressure, ownership, capability needs, selection, reachability, current-fact visibility, inquiry eligibility, artifact visibility, and methodology characterization.

6. **Do Recovery Results, Methodology Observations, and Architectural Consequences naturally become runtime artifacts?**

   No. Current evidence supports treating them as inquiry/report surfaces or answer sections unless a concrete implementation owner, persistence need, dispatch contract, or registry identity is recovered. They may be important repository artifacts, but repository importance is not runtime ownership.

7. **Does the repository demonstrate a constitutional preference for remembering or asking?**

   The repository demonstrates a preference for **asking over duplicate remembering**, not for asking over all memory. Seed remembers observations, evidence, facts, projections, catalogs, diagnostic contracts, and registered question identities. It asks bounded questions over those artifacts instead of storing every recovered architectural interpretation as new truth.

8. **Is there sufficient repository evidence to recognize this as a stable architectural pattern?**

   Yes, with moderate-to-high confidence. The pattern is stable across the reviewed representative recoveries and is supported by implementation boundaries. It should not be overextended into a prohibition on new runtime artifacts.

## Unsupported conclusions

The investigation does **not** support these stronger claims:

- Seed never introduces new runtime artifacts.
- All runtime artifacts are mistakes.
- All architectural reports should become question families.
- Methodology should become a runtime engine.
- Question families should be auto-created from recurring prose.
- Diagnostic findings should become cluster truth.
- Presentation vocabulary is sufficient evidence for preserved knowledge.
- The repository has proven a universal law covering every future recovery.

## Confidence

**Moderate-high confidence** in the main characterization: mature recoveries usually terminate as bounded inquiry/answer surfaces composed from existing artifacts.

**High confidence** that automatic promotion from recurring prose into runtime artifacts is unsupported by current implementation evidence.

**High confidence** that Seed nevertheless has justified durable runtime artifacts for evidence, facts, projections, catalogs, diagnostics, and registered question identities.

**Medium confidence** on the exact boundary for future `Methodology Observation`, `Architectural Consequence`, and `Recovery Result` surfaces because current evidence supports inquiry/report characterization, but a future concrete implementation could justify a narrower artifact if it proved ownership, state, registry, or dispatch requirements.

## Acceptance answer

When Seed discovers a new recurring competency, current repository evidence says it should first ask:

```text
Can this be answered as a bounded question composed from existing repository/runtime artifacts,
with authority, uncertainty, and non-promotion boundaries preserved?
```

If yes, Seed should gain the question or answer surface rather than a new stored object.

Seed should remember a new runtime artifact only when the competency requires durable state, provenance, registry identity, dispatch compatibility, diagnostic contract metadata, or mutation/recording boundaries that cannot be represented by composition over existing artifacts.

The reviewed recoveries support the skeptical answer that we have often been tempted to turn inquiries into objects, while the repository has repeatedly earned the narrower pattern of turning them into bounded questions.
