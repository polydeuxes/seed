# Knowledge Requirement Discovery Investigation

## Scope and method

This is a bounded implementation investigation. It does not implement ownership recovery, planning, orchestration, autonomous inquiry, runtime surfaces, compatibility behavior, or question-family changes.

The investigation reviewed implementation around inquiry, question families, inquiry orientation, answer composition, reference selection, selection path, reasoning path, current facts, state summary, operational story, capability inventory, projection influence, and read-model consumers. Repository authority wins over vocabulary preference.

The central question was whether Seed already has a recurring responsibility equivalent to:

```text
Question -> Required subject(s) -> Required knowledge -> Available knowledge -> Answer Composition
```

## Executive conclusion

Seed does **not** currently contain strong implementation evidence for a recurring, separately owned Knowledge Requirement Discovery responsibility.

The implementation does determine some prerequisite information before answering, but that decision is distributed across existing owners:

- question-family dispatch maps select an answering surface and sometimes require explicit operator parameters;
- individual answering surfaces select their own evidence and fallback behavior;
- read-model and diagnostic surfaces expose availability, reachability, consumers, or derivation after a surface has already been selected;
- model-decision context composition supplies recent/projected context broadly rather than deriving question-specific knowledge requirements.

The strongest emerging evidence is therefore not a recovered owner. It is repeated local compression: several surfaces contain small, implementation-specific versions of subject selection, evidence selection, availability checks, and fallback handling.

## Implementation evidence reviewed

### Bounded ask and Question Families

`question_surface_inventory.py` is the clearest implementation-backed question-family surface. It maps exact question-family names to answering surfaces, declares required surface arguments for only two families, and derives bounded ask eligibility from those maps.

Relevant evidence:

- `BOUNDED_ASK_DISPATCH_SURFACES` maps question families such as `operational pressure`, `current operational explanation`, `knowledge reachability`, `derivation explanation`, and `selection explanation` to concrete surfaces.
- `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` requires explicit `domain, subject` for `derivation explanation` and `target` for `selection explanation`.
- `bounded_status_for_question_family()` derives eligibility from those maps rather than from semantic interpretation of a free-form inquiry.
- inventory rows state that derivation and selection explanations require explicit arguments and do not infer them.

This is evidence for question-family-to-surface routing and parameter preconditions. It is **not** evidence for a generalized responsibility that discovers required knowledge. The implementation asks the operator to provide required subject/target values for the cases where subject selection would otherwise be needed.

`scripts/seed_local.py` confirms this boundary in the CLI dispatch path. `apply_bounded_ask_dispatch()` accepts only exact `ask --question-family ...` usage, rejects unknown families, enforces required argument counts, forwards explicit arguments to the target surface, and sets the corresponding diagnostic/inquiry flag. It does not parse the user's natural-language question to discover required subjects or evidence.

### Inquiry Orientation and Architectural Orientation

`inquiry_orientation.py` contains the strongest local evidence for question-dependent knowledge selection, but the selection is intentionally bounded to lexical overlap.

Relevant evidence:

- `_collect_architectural_orientation_evidence()` tokenizes the raw inquiry note and combines `_fact_matches()` with `_source_navigation_matches()`.
- `_fact_matches()` scans projected fact supports for token overlap against subject, predicate, value, and path dimensions.
- `_source_navigation_matches()` queries source navigation for each token and converts definitions/imports into related material.
- `_compose_architectural_orientation_answer()` separates evidence collection from answer composition, and the authority boundary explicitly states that matches are deterministic lexical overlaps only.

This is implementation evidence for **related-material discovery**, not for required-knowledge discovery. It answers “what already projected material overlaps this note?” rather than “what knowledge must exist to answer honestly?” Its fallback also says absence of matches does not prove unrelatedness.

### Reasoning Path

`reasoning_path_audit.py` builds a derivation path from implemented diagnostic surfaces for an explicit domain and subject.

Relevant evidence:

- `build_reasoning_path_audit()` requires `domain` and `subject` parameters.
- It builds or consumes ownership discrepancies, capability needs, pressure audit, privilege discovery, and operational story surfaces.
- It filters ownership discrepancy rows and diagnostic capability need records by subject match.
- It emits unknowns when no derivation evidence, conclusions, consumers, or story impact are found.

This is strong evidence for subject-dependent derivation explanation after the subject is known. It is not evidence that the implementation discovers the subject or required knowledge from the original question. The question-family inventory and CLI path require the subject to be operator-provided.

### Selection Path

`selection_path_audit.py` explains why an implemented operational conclusion was selected.

Relevant evidence:

- `build_selection_path_audit()` requires a `target` parameter.
- It normalizes that target, builds pressure audit and operational story, then checks whether the target matches current focus, primary pressure, or a pressure category.
- It reports candidates, factors, non-selected candidates, selected evidence, outcome, and unknowns.
- Its fallback for unrecognized targets states that the target is not an implemented selection surface.

This is evidence for selection explanation and candidate visibility. It is not evidence for knowledge-requirement discovery because the target is an input precondition, and the candidate set comes from pressure audit rather than from a generalized answer prerequisite model.

### Reference Selection

`reference_selection.py` exposes implementation-selected comparison references for a narrow domain.

Relevant evidence:

- `build_reference_selection()` supports only `domain == "history"`.
- Unsupported domains return `status: unknown` with limitations that only the history domain is implementation-backed.
- The history path selects previous comparable snapshots when impact audit exposes comparable pairs and records limitations.

This is evidence for a narrow reference-selection owner. It demonstrates a local version of required reference availability: historical comparison requires comparable snapshot pairs. It does not recur as generalized question-to-required-knowledge discovery.

### Operational Story and Answer Composition

`operational_story.py` separates answer payload, reasoning payload, supporting evidence, boundary, and limitations.

Relevant evidence:

- `build_operational_story()` composes pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit.
- `_compose_operational_story_payloads()` produces separate answer, reasoning, supporting evidence, boundary, and limitations payloads.
- Unknowns are emitted when pressure, capability needs, or impact evidence is absent.

This is evidence for answer composition over preselected surfaces. It is not evidence that Operational Story owns discovery of what knowledge is required by arbitrary inquiries. The required inputs are hard-coded by the story surface.

### Current Facts, State Summary, and Read Models

`state_views.py` and `state_summary_views.py` implement read-only current fact views and state summary aggregation.

Relevant evidence:

- `build_fact_view()` renders projected fact support when available and falls back to raw facts for tests and direct `State` construction.
- state summary helpers classify and aggregate current projected state for presentation, with explicit boundaries that classifications do not assert ownership, topology truth, or fact status.

These are read-model and presentation responsibilities. They expose available knowledge, but they do not decide what knowledge an inquiry requires.

`projected_state_consumers.py` inventories surfaces and source consumption from diagnostic inventory. It classifies consumers as diagnostic, inquiry, inventory, runtime, observation, projection, or unknown, and records whether surfaces use projected state, repo files, static inventory, live observation, event ledger, or runtime input. This is useful evidence about **who consumes what**, but it is not a runtime mechanism for question-specific knowledge prerequisite discovery.

### Capability Inventory

`capability_inventory.py` preserves a clear adjacent boundary: capability inventory consumes admitted capability facts, executable operation contract metadata, and requested capabilities.

Relevant evidence:

- `_CapabilityInventorySources` keeps admitted repository capability knowledge, executable operation contract metadata, and requested capabilities separate before inventory presentation.
- `build_capability_inventory()` derives verification state from `capability_verified` facts and returns no rows if the predicate is absent from the predicate catalog.
- Missing verification facts produce unverified entries; expired verification facts produce stale entries.

This is evidence for capability availability and verification-state interpretation, not for general knowledge-requirement discovery.

### Runtime decision input and answer routing

`context.py`, `decisions.py`, and `runtime.py` show that the runtime supports answering but does not implement question-specific knowledge requirements.

Relevant evidence:

- `DecisionInputComposer.compose()` sends current input, active goals, entities, recent facts, recent evidence, tools, and open tool needs through a budgeted context packet.
- `Runtime._route()` appends answer or question responses after a decision is already selected.

This is evidence for context packaging, decision validation, and routing. It is not evidence for a repository-owned process that determines the required knowledge before answer composition.

## Recurring implementation patterns

### Pattern 1: Exact question family selects an answering surface

Question Families currently choose the answering surface through exact string maps. This recurs in inventory, bounded ask eligibility, and CLI dispatch. It is implementation-backed and explicit, but it answers “which surface handles this family?” rather than “what knowledge is required?”

### Pattern 2: Some surfaces require explicit operator-provided subject/target arguments

Reasoning Path and Selection Path are the strongest counterexample to hidden discovery. The implementation requires operator-provided `domain, subject` or `target`, then explains derivation or selection. The responsibility for subject discovery is not implemented there.

### Pattern 3: Individual surfaces hard-code their own evidence inputs

Operational Story always composes pressure, capabilities, privilege, correlation, impact, and investigation path. Inquiry Orientation always uses lexical matches over fact supports and source navigation. Reference Selection only supports history and comparable snapshots. Capability Inventory always uses the capability verification predicate and inventory sources. These are recurring local prerequisites, but not a shared owner.

### Pattern 4: Surfaces expose unknowns and limitations when evidence is absent

Several surfaces preserve absence or unavailability:

- Inquiry Orientation distinguishes no deterministic related material from proof of unrelatedness.
- Reasoning Path emits `derivation` unknowns when no evidence is found.
- Selection Path emits unknowns for unsupported targets or missing pressure candidates.
- Reference Selection returns unsupported-domain or unavailable-reference limitations.
- Operational Story emits unknowns for missing pressure, capability needs, or impact.

This is evidence for honest fallback behavior. It does not prove a unified requirement-discovery responsibility.

### Pattern 5: Read-model consumers and reachability surfaces describe availability after the fact

Read-model consumer inventory and knowledge reachability can show where knowledge is visible or missing across surfaces. That is adjacent and useful, but it does not select required knowledge for a specific inquiry before answer composition.

## Counterexamples and negative evidence

### Knowledge requirements are often hard-coded inside individual surfaces

Operational Story, Capability Inventory, Reference Selection, Inquiry Orientation, Reasoning Path, and Selection Path each own their own prerequisite choices. These choices are not declared through a shared requirement-discovery interface.

### Question Families do not own knowledge discovery

Question Families own inventory rows, answer responsibility descriptions, bounded eligibility, dispatch-surface relationships, and a small number of required surface arguments. They do not infer subjects or evidence requirements from question text.

### Subject selection is not generally implemented

The strongest subject-dependent surfaces require explicit subject or target parameters. Where a free-form note is accepted, Inquiry Orientation uses lexical overlap and explicitly refuses semantic interpretation.

### Runtime answers can be produced from broad context without explicit prerequisites

The model-facing decision input contains recent facts and evidence selected by budget/freshness ordering, not a question-derived knowledge prerequisite set. Answer decisions are validated for answer presence, not for evidence sufficiency.

### Knowledge discovery does not recur as an owner

There are recurring pieces of behavior related to evidence selection, subject filtering, availability checks, and fallback, but they are distributed across unrelated owners. No reviewed implementation exposes a recurring `required knowledge`, `knowledge prerequisites`, `answer preconditions`, or equivalent boundary.

## Answers to central questions

### 1. Does the repository currently contain a recurring Knowledge Requirement Discovery responsibility?

No, not as a separately owned recurring implementation responsibility.

The implementation contains multiple local prerequisite decisions and availability checks, but they are compressed into question-family dispatch, individual surfaces, read-model consumers, and answer composition surfaces. The strongest implementation-backed statement is:

> Seed currently distributes knowledge requirement decisions across exact question-family dispatch, explicit operator-provided surface arguments, and surface-local evidence selection.

### 2. If yes, where is the strongest implementation evidence?

Because the conclusion is “not yet,” the strongest **near evidence** is:

1. Question Families: exact family-to-surface maps and required surface arguments.
2. Inquiry Orientation: lexical related-material discovery from projected fact supports and source navigation.
3. Reasoning Path: explicit-subject derivation evidence and unknown fallback.
4. Selection Path: explicit-target selection evidence and unsupported-target fallback.
5. Reference Selection: domain-limited reference availability for history.
6. Operational Story: hard-coded composition inputs and limitations payloads.

These are adjacent fragments, not a recovered responsibility.

### 3. Which implementation responsibilities currently appear compressed?

The following responsibilities appear compressed into existing owners:

- **Subject/target selection** is compressed into operator-provided `--surface-args`, lexical token matching, or target normalization.
- **Required evidence discovery** is compressed into individual surfaces' hard-coded source lists.
- **Knowledge availability checks** are compressed into per-surface unknowns, limitations, fallback branches, and read-model/reachability diagnostics.
- **Answer preconditions** are compressed into question-family eligibility, CLI argument validation, decision validation, and surface-specific fallbacks.
- **Read-model selection for answering** is compressed into bounded ask dispatch and each answering surface's implementation.

### 4. Which responsibilities already own adjacent behavior?

Adjacent owners already visible in implementation are:

- **Question Families / Bounded Ask Dispatch** own exact family identity, dispatch-surface mapping, bounded eligibility, and explicit required surface arguments.
- **Inquiry Orientation** owns read-only lexical related-material orientation for preserved notes.
- **Reference Selection** owns narrow implementation-selected comparison reference visibility for history.
- **Reasoning Path** owns explicit-subject derivation explanation from implemented diagnostic surfaces.
- **Selection Path** owns explicit-target selection explanation from pressure and operational story evidence.
- **Operational Story / Answer Composition** owns composition of selected operational surfaces into answer, reasoning, support, boundary, and limitations payloads.
- **Read-model construction and views** own current facts, state summary, capability inventory, and consumer/source visibility.
- **Runtime decision validation and routing** own structural decision validity and response emission after a decision is proposed.

### 5. Does implementation evidence support beginning a Knowledge Requirement Discovery responsibility family?

Yes, cautiously, but only as a future bounded recovery investigation if implementation pressure continues.

The evidence supports the existence of recurring pressure around question-dependent subject/evidence selection, but not the existence of a current owner. Beginning a responsibility family would be supported only if future work remains implementation-backed and starts from the compressed behaviors above. It should not introduce planners, orchestration, autonomous inquiry, semantic question interpretation, or runtime behavior changes.

The first implementation-backed question for future recovery would be narrow:

> Can Seed make explicit the already-existing handoff between an exact question family plus explicit surface arguments and the evidence sources that the selected answering surface already consumes?

That would preserve repository authority and avoid inventing unsupported architecture.

## Supported conclusions

- Seed has exact question-family dispatch, not general question interpretation.
- Some question families require explicit surface arguments, proving subject/target discovery is not generally implemented there.
- Inquiry Orientation performs deterministic lexical related-material discovery, not semantic required-knowledge discovery.
- Reasoning Path and Selection Path explain derivation/selection only after a subject or target is supplied.
- Operational Story composes hard-coded adjacent surfaces into answer payloads and limitations.
- Reference Selection has a narrow history-only reference availability rule.
- Read-model views expose available projected knowledge but do not determine inquiry-specific prerequisites.
- Runtime decision validation checks structural decision payloads, not evidence sufficiency.

## Unsupported conclusions

The reviewed implementation does not support claiming that:

- Seed has a general Knowledge Requirement Discovery owner today.
- Question Families infer required subjects or evidence from natural-language questions.
- Inquiry Orientation determines required knowledge rather than related material.
- Knowledge Reachability selects prerequisite knowledge for answering.
- Runtime answers are gated by explicit answer precondition evidence.
- Reference selection, reasoning path, and selection path form a unified requirement-discovery pipeline.

## Confidence

Confidence is **medium-high**.

The evidence is strong that no shared owner is visible in the reviewed implementation, and strong that adjacent fragments exist. Confidence is not absolute because the repository is large and additional local surfaces may contain similar prerequisite logic. However, the reviewed central surfaces consistently show distribution rather than unified ownership.

## Recommended next action

Do not implement ownership recovery now.

Recommended next action is documentation-only or audit-only:

1. Preserve this investigation as the bounded evidence record.
2. If future implementation pressure continues, perform a narrower follow-up audit of selected answering surfaces to inventory their existing hard-coded evidence inputs and fallback conditions.
3. Do not add planners, orchestration, autonomous inquiry, semantic question parsing, question-family changes, or runtime surfaces until implementation evidence shows a recurring compressed boundary that needs recovery.

## Acceptance answer

When Seed answers a question today, the implementation generally determines what must exist first by a combination of:

1. exact question-family dispatch to a known surface;
2. explicit operator-provided parameters where a subject or target is needed;
3. surface-local hard-coded evidence inputs;
4. per-surface unknowns, limitations, and fallback behavior;
5. broad runtime context packaging for model decisions where bounded ask is not involved.

A Knowledge Requirement Discovery responsibility is **emerging only as pressure**, not as an implementation owner. Today's implementation still distributes the decision across unrelated owners.
