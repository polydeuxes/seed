# Methodology as Inquiry Subject Investigation

## Scope

This investigation asks whether architectural recovery methodology should become another Inquiry subject rather than a new Inquiry subsystem.

This is an investigation only. It does not implement new inquiry behavior, new question families, new inquiry owners, methodology automation, architectural recovery automation, planners, prompts, runtime surfaces, or ownership recovery.

Repository authority wins. Conclusions below use implementation evidence, tests, and implementation-backed reports rather than architectural preference.

## Implementation evidence reviewed

### Runtime inquiry and question-family implementation

- `seed_runtime/question_surface_inventory.py` defines static `QuestionFamily` inventory rows with example questions, answering surface, CLI flag, answer responsibility, authority boundary, bounded dispatch status, diagnostic inventory relationship, diagnostic shape-audit relationship, relationship status, implementation reason, and unknown-family behavior.
- `seed_runtime/question_surface_inventory.py` maps bounded ask families to exact existing surfaces in `BOUNDED_ASK_DISPATCH_SURFACES` and marks parameterized families in `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`.
- `seed_runtime/question_surface_inventory.py` exposes `build_question_family_definition(...)` and `build_composed_question_family_explanation(...)`, which answer identity, responsibility, boundary, dispatch, and diagnostic-relationship questions for a known family and return explicit `unknown` status for unregistered families.
- `seed_runtime/inquiry_orientation.py` records inquiry notes in an isolated JSONL probe store and builds a read-only `InquiryOrientationView` from an `InquiryNoteRecord` plus projected state.
- `seed_runtime/inquiry_orientation.py` has an implementation-local `_ArchitecturalOrientationAnswer` with `answer`, `reason`, `support`, `boundary`, and `limitations` before compatibility handoff into the public `InquiryOrientationView`.
- `seed_runtime/inquiry_orientation.py` selects related material by deterministic lexical overlap against projected fact supports and source-navigation matches, and its authority boundary explicitly forbids treating the note as a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, ownership assertion, intent, concern, recommended action, or next safe move.
- `seed_runtime/inquiry_artifacts.py` exposes repository-visible inquiry artifacts with classifications, evidence, limitations, and a read-only boundary that forbids recording, event-ledger writes, cluster mutation, inquiry-graph creation, pressure-transformation inference, and workflow/planning behavior.
- `scripts/seed_local.py` exposes the implemented app surfaces used for this investigation: `--question-surface-inventory`, `--question-family-definition`, `--question-family-explanation`, and `--inquiry-artifacts`.
- `tests/test_question_surface_inventory.py`, `tests/test_inquiry_orientation.py`, and `tests/test_inquiry_artifacts.py` preserve the current question-family, orientation, and inquiry-artifact behavior.

### Implementation-backed reports and audits

- `question_family_registration_boundary_audit.md` concludes that a new known `QuestionFamily` currently exists only through a static implementation edit to `build_question_surface_inventory()` and, when executable through bounded ask, corresponding dispatch-map entries.
- `question_family_registration_boundary_audit.md` concludes that recovered families are not public inquiry subjects by default; current inquiry will not answer them unless they are represented in Question Surface Inventory and bounded ask maps where applicable.
- `answer_composition_family_completion_audit.md` concludes that Answer Composition is a reusable architectural layer for current projected responsibility, strongest in `operational_story` and `inquiry_orientation`, while other inquiry surfaces remain surface-specific or compressed.
- `architectural_inquiry_orientation_surface_audit.md` concludes that Seed can partially derive architectural self-orientation from repository artifacts for known responsibility-family slices, but no dedicated runtime/CLI surface derives the answer automatically today.
- `architectural_orientation_answer_composition_audit.md` concludes that architectural orientation fits the existing bounded answer pattern: answer, reason, support, boundary, and limitations.
- `architectural_recovery_methodology_characterization.md` characterizes the demonstrated recovery methodology as implementation evidence -> one compressed owner -> compatibility-preserving local handoff -> focused tests/audits -> repeat while same-family evidence remains -> completion audit -> stop on ownership change.
- `architectural_recovery_methodology_characterization.md` also warns that recurring vocabulary, similar output shapes, private dataclasses, and read-only flags are insufficient proof of a shared abstraction.
- `evidence_contract_family_investigation.md` finds repeated implementation-local evidence handoffs across independent families, but explicitly rejects immediate shared abstraction, vocabulary migration, or implementation recovery.
- `inquiry_lineage_family_vocabulary_audit.md` and related inquiry-lineage slices show inquiry-result interpretability, selection rationale, alternatives, limitations, authority, and confidence as recurring inquiry-facing concerns, but not a universal runtime inquiry graph.

### App surfaces exercised during this investigation

The following repository app commands were run to inspect implemented Inquiry surfaces rather than relying only on prose reports:

```text
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --inquiry-artifacts --json
python scripts/seed_local.py --question-family-definition "inquiry orientation" --json
python scripts/seed_local.py --question-family-explanation "derivation explanation" --json
```

The command outputs confirmed that the app exposes question-family inventory, inquiry artifact visibility, known-family definitions, composed family explanations, bounded statuses, answer responsibilities, authority boundaries, implementation reasons, and unknown/registration boundaries through existing surfaces.

## Supporting evidence

### Bounded inquiry subjects already exist

The current Inquiry architecture is organized around bounded subjects represented as exact question-family rows. Each row binds a question family to example questions, a responsible answering surface, a CLI flag, an answer responsibility, an authority boundary, implementation reason, and diagnostic relationship metadata.

This supports methodology-oriented inquiry in principle because architectural recovery methodology can be treated as a bounded subject if and only if a repository-backed question family is explicitly registered with a responsible surface and authority boundary. The architecture does not require question subjects to be runtime-only: existing families include operational pressure, derivation explanation, selection explanation, knowledge reachability, source definition/import lookup, inquiry orientation, projection shape visibility, and surface shape validation.

However, bounded subject support is static and explicit. The implementation does not auto-promote a methodology topic into a question family.

### Subject registration is explicit, not inferred

The strongest counterweight to overclaiming is the registration boundary. `build_question_surface_inventory()` is the current source of known question-family identity. `build_question_family_definition(...)` returns a structured `unknown` response when no inventory row exists. Bounded ask dispatch is controlled by exact dispatch maps and required-argument maps.

Therefore, architectural recovery methodology is not already an answerable public Inquiry subject merely because methodology reports exist. It could become one only through an explicit future implementation step that registers a question family and responsible read-only answering surface. That step would be an implementation decision, not a new inquiry subsystem by itself.

### Existing answer composition matches methodology questions

Methodology questions listed in the task ask for evidence, strongest compressed responsibility, continuation/stop conditions, contradictions, unsupported conclusions, completion-audit stopping reasons, and confidence. Existing Inquiry and answer surfaces already support much of this shape:

- derivation explanation asks which evidence supports a conclusion;
- selection explanation asks why a conclusion or candidate was selected and which alternatives were considered;
- inquiry orientation relates a preserved inquiry note to projected fact supports and source-navigation matches while preserving uncertainty and authority limits;
- inquiry artifacts expose supported/unsupported conclusion as document-visible artifacts with explicit limitations;
- architectural orientation and operational story demonstrate answer/reason/support/boundary/limitations composition;
- methodology characterization and completion audits already use counterexamples, supported conclusions, unsupported conclusions, confidence, and recommended next action sections.

This is strong evidence that methodology-oriented questions fit the existing answer-composition grammar. It is weaker evidence for immediate runtime capability because there is no implemented methodology subject surface.

### Authority boundaries are already first-class in inquiry answers

Existing question-family rows include authority boundaries. Inquiry orientation has a detailed boundary preventing preserved prose and lexical matches from becoming facts, ownership, operator intent, recommended actions, or next safe moves. Inquiry artifacts have a boundary forbidding recording, event-ledger writes, cluster mutation, inquiry-graph creation, pressure-transformation inference, workflow behavior, and planning behavior.

That is directly relevant to architectural recovery methodology because methodology inquiry would have to avoid turning diagnostic findings or recovery hypotheses into cluster truth, ownership truth, plans, prompts, or automation. Existing Inquiry already contains the boundary vocabulary and read-only posture needed for that discipline.

### Limitations and unsupported conclusions are already represented, but unevenly

Inquiry artifacts classify `supported_conclusion` and `unsupported_conclusion` as document-visible rather than fully implemented runtime artifacts. Answer Composition completion says several surfaces carry bounded answers but not all are projected into a five-part implementation-local answer object. Architectural inquiry orientation says confidence and next inquiry are derivable from artifacts but not automatically surfaced today.

This means methodology inquiry can use current Inquiry concepts, but a future implementation would need to be honest about which conclusions are document-derived, which are implementation-derived, and which are unsupported.

### Confidence is supported as evidence-scope confidence, not as a generic calculator

Architectural orientation and methodology reports already use confidence based on evidence strength, implemented slice chains, tests, and unresolved compression scope. Current implementation does not expose a general confidence calculator for methodology questions. Therefore, confidence can be part of a methodology answer shape, but the repository does not yet support automated confidence computation for architectural recovery methodology.

## Counterexamples and limits

### Methodology is not currently registered as a QuestionFamily

No reviewed implementation row registers `architectural recovery methodology` or `methodology inquiry` as a known question family. There is no bounded ask dispatch mapping for the central methodology questions. Unknown question families are deliberately reported as unknown rather than inferred.

This is the main reason the answer cannot be: "architectural recovery is already an Inquiry subject." It is not.

### Existing Inquiry does not recover methodology ownership automatically

The implementation can expose known question-family definitions, inquiry orientation, inquiry artifacts, derivation paths, and selection paths. It does not parse methodology reports, detect compressed responsibility, compute strongest owner, evaluate whether a family should continue, or automate architectural recovery.

That limitation is compatible with the task's prohibition. It also means methodology-oriented Inquiry would initially need to compose existing repository evidence, not implement recovery automation.

### Inquiry artifact implementation explicitly refuses several tempting generalizations

`inquiry_artifacts` keeps supported and unsupported conclusions as document-visible artifacts and says there is no repository implementation currently modeling supported inquiry conclusions as generalized artifacts. It also refuses inquiry-graph creation, pressure-transformation inference, and workflow/planning behavior.

Those constraints argue against a new subsystem that tries to model all methodology movement, planning, or recovery state. They support a narrower subject-oriented read-only answer, if any future step is taken.

### Answer Composition is reusable, but not universal

Answer Composition is complete as a reusable architectural layer with representative implementations, not as a universal conversion of every inquiry surface. `reasoning_path`, `selection_path`, `reference_selection`, and `inquiry_artifacts` remain surface-specific or compressed. A methodology subject should not assume all existing surfaces expose identical fields or a shared answer payload.

### Evidence Contract investigation rejects shared abstraction from recurring handoff grammar

The repeated evidence-handoff grammar is real, but the investigation explicitly rejects immediate shared abstraction or vocabulary migration. This directly prevents concluding that methodology inquiry requires a new cross-cutting Evidence Contract subsystem. It also prevents concluding that repeated methodology sections alone justify a new architecture.

### Architectural inquiry orientation was only partially supported

The prior architectural inquiry orientation audit concluded that Seed can derive a bounded architectural self-orientation answer from existing artifacts for known families, but cannot do so automatically through a dedicated runtime/CLI surface today. That is a useful precedent and a limit: methodology inquiry is naturally shaped like Inquiry, but current implementation remains document/app-surface-assisted rather than fully implemented.

## Answers to central questions

### 1. Can the existing Inquiry architecture naturally inquire about architectural recovery methodology?

Yes, with an important boundary: the existing Inquiry architecture appears expressive enough to inquire about architectural recovery methodology as a bounded subject, but that subject is not currently registered or automatically answerable.

The evidence supports expressiveness because existing Inquiry already has bounded subjects, explicit subject registration, answer responsibility, authority boundaries, answer composition, evidence support, limitations, unknown-family behavior, derivation explanation, selection explanation, inquiry orientation, inquiry artifacts, and diagnostic relationships.

The evidence does not support implementing a new inquiry engine or subsystem for methodology. It also does not support saying methodology inquiry already exists as a public question family.

### 2. If yes, what implementation evidence supports that conclusion?

Supporting evidence:

1. Question families are static bounded subjects with responsible surfaces, boundaries, dispatch status, required args, diagnostic relationships, implementation reasons, and unknown-family behavior.
2. Existing question families already include non-runtime-only subjects such as knowledge reachability, derivation explanation, selection explanation, source definition/import lookup, inquiry orientation, projection shape visibility, surface inventory, and surface shape validation.
3. Inquiry orientation composes a bounded answer with answer, reason, support, boundary, and limitations from repository/projected evidence while preserving a strict authority boundary.
4. Inquiry artifacts expose inquiry-relevant concepts such as boundary, pressure, finding, supported conclusion, unsupported conclusion, open question, and gap with evidence and limitations.
5. Answer Composition has representative implementation-backed reuse across Operational Story and Architectural Orientation and identifies other bounded inquiry surfaces that already carry similar material.
6. Architectural recovery methodology characterization already produces the same investigation answer shape requested here: implementation evidence reviewed, recurring patterns, counterexamples, supported conclusions, unsupported conclusions, confidence, and recommendations.
7. Evidence Contract investigation shows repeated bounded handoff grammar but rejects a new shared abstraction, aligning with subject-oriented inquiry rather than subsystem creation.

### 3. If not, what implementation capabilities are missing?

The answer is not a full "no," but current implementation is missing capabilities required for methodology to be a public Inquiry subject:

- no registered methodology question family;
- no responsible methodology answering surface;
- no bounded ask dispatch for methodology questions;
- no implementation that composes methodology evidence from recovery reports into a stable answer;
- no automated methodology confidence calculation;
- no implemented support/contradiction scanner for recovery conclusions;
- no tests preserving methodology answers through `--question-surface-inventory`, bounded ask, diagnostic inventory, or shape audit;
- no explicit record of which methodology questions are supported, unsupported, or parameterized.

These are missing subject/surface capabilities, not evidence for a fundamentally different Inquiry architecture.

### 4. Would architectural recovery become merely another Inquiry subject, or require a fundamentally different inquiry architecture?

Repository evidence supports: architectural recovery methodology would most naturally become another bounded Inquiry subject, not a fundamentally different inquiry architecture.

Reasons:

- Existing Inquiry already answers bounded subjects through registered surfaces and explicit boundaries.
- Existing answer composition already supports evidence, reason, support, boundary, limitations, and compatibility handoff.
- Existing inquiry artifact visibility already warns against creating workflow, planning, inquiry-graph, or pressure-transformation behavior.
- Existing methodology characterization is a repository process that can be questioned about evidence, support, contradiction, stopping point, unsupported conclusions, and confidence without changing the Inquiry architecture.
- Existing registration boundaries show that the smallest future move would be subject/surface registration and composition, not a new subsystem.

The only reason to consider a new subsystem would be if future implementation evidence shows methodology questions require behavior outside current Inquiry: recovery automation, ownership recovery execution, planning, workflow state, semantic inference beyond repository evidence, or a shared evidence-contract abstraction. Current evidence rejects or does not support those capabilities.

### 5. What is the smallest implementation step, if any, supported by repository evidence?

No implementation step is taken in this investigation.

If future work is authorized, the smallest repository-supported step would be a read-only methodology inquiry subject investigation-to-surface slice, not a subsystem. That slice would need to:

1. define the exact bounded question family and examples;
2. choose or implement one read-only answering surface that composes existing methodology/recovery artifacts;
3. preserve authority boundaries and avoid recovery automation;
4. expose answer, reason, support, boundary, limitations, unsupported conclusions, and confidence only where evidence supports them;
5. add inventory/dispatch/diagnostic shape tests if a runtime/diagnostic surface is added;
6. preserve the current rule that unknown families remain unknown until explicitly registered.

The smallest non-runtime step would be to keep methodology as documentation-only and use existing app surfaces (`--question-surface-inventory`, `--question-family-definition`, `--question-family-explanation`, `--inquiry-artifacts`) to inspect whether a future subject is justified. Because this task forbids implementation, this report stops at that conclusion.

## Supported conclusions

1. Existing Inquiry architecture is expressive enough, in shape, to handle architectural recovery methodology as a bounded Inquiry subject.
2. Architectural recovery methodology is not currently a registered public Inquiry subject.
3. Current evidence supports subject-oriented future work more strongly than subsystem-oriented future work.
4. A fundamentally new inquiry architecture is not supported by current implementation evidence.
5. Existing answer-composition and inquiry-artifact boundaries are directly relevant to methodology questions about evidence, contradiction, unsupported conclusions, limitations, authority, and confidence.
6. Static registration and exact dispatch are important compatibility and authority boundaries; methodology must not be inferred into existence from prose or recurring vocabulary.
7. Current implementation supports read-only, evidence-composing methodology inquiry better than automation, ownership recovery, planning, prompts, or workflow behavior.

## Unsupported conclusions

Current repository evidence does not support concluding that:

- architectural recovery methodology is already an implemented question family;
- methodology questions can already be asked through bounded ask dispatch;
- a new Inquiry subsystem should be created;
- a new inquiry engine is required;
- recovery ownership should be automated;
- methodology conclusions should become cluster truth;
- unsupported methodology conclusions are runtime artifacts;
- confidence can be computed automatically for methodology questions today;
- recurring report sections or vocabulary alone prove a reusable implementation abstraction;
- Evidence Contract should become a shared abstraction as part of this work;
- architectural recovery should recover ownership as part of this investigation.

## Confidence

**High confidence** that existing Inquiry architecture has the right conceptual and implementation shape for methodology-oriented inquiry: bounded subjects, explicit registration, answer responsibility, authority boundaries, evidence support, limitations, unknown-family behavior, and answer composition are all present.

**High confidence** that methodology is not currently a registered Inquiry subject, because question-family identity is static and explicit and no methodology row or dispatch mapping was found.

**Medium confidence** that a future read-only methodology inquiry subject would be the smallest appropriate implementation direction, because the shape is strongly supported but the exact surface and tests are not implemented.

**Low confidence** that methodology questions require a new Inquiry subsystem, because current counterexamples argue against automation, generalized inquiry graphs, workflow/planning behavior, and shared cross-family abstractions.

## Recommended next action

Do not implement a new Inquiry subsystem.

If future work is approved, treat architectural recovery methodology as a candidate bounded Inquiry subject and first perform the smallest implementation-backed registration/surface design slice. That slice should remain read-only, compose existing repository evidence, preserve unsupported conclusions and confidence limits, and add the required inventory, dispatch, diagnostic-shape, and tests only if it creates a runtime surface.

Until that work is authorized, keep architectural recovery methodology as repository-visible documentation that can be inspected through existing Inquiry-adjacent app surfaces rather than promoted automatically.

## Final answer

Architectural recovery is not currently a new inquiry system and is not currently an implemented Inquiry subject.

Repository evidence supports that, if architectural recovery methodology becomes queryable, it should become another bounded Inquiry subject before anyone considers a new Inquiry subsystem. The existing Inquiry architecture already has the necessary shape: bounded subjects, static registration, answer responsibility, evidence support, authority boundaries, limitations, unknown-family refusal, and answer composition. What is missing is not a fundamentally different architecture; what is missing is explicit registration and a read-only answering surface for methodology questions.
