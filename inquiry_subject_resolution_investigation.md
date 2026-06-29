# Inquiry Subject Resolution Investigation

## Scope

This bounded investigation asks whether the current implementation contains a recurring responsibility for turning an inquiry into something subject-specific before evidence selection and answer composition begin. It does not evaluate natural-language understanding, planners, semantic interpretation, or new runtime orchestration.

## Implementation evidence reviewed

- `seed_runtime/question_surface_inventory.py` static question-family registry, bounded ask maps, required surface arguments, inventory rows, and inventory enrichment.
- `scripts/seed_local.py` bounded `ask --question-family` dispatch, CLI argument declarations, and direct calls into answer surfaces.
- `seed_runtime/inquiry_orientation.py` inquiry-note recording and read-only orientation.
- `seed_runtime/reasoning_path_audit.py` derivation-path surface.
- `seed_runtime/selection_path_audit.py` selection-path surface.
- `seed_runtime/reference_selection.py` reference-selection surface.
- `seed_runtime/operational_story.py` answer composition for current operational explanation.
- `seed_runtime/capability_inventory.py` current capability inventory presentation.
- `seed_runtime/state.py` projection-influence lineage and replay-selection boundary comments.
- Tests around question-surface dispatch, reasoning path, selection path, reference selection, inquiry orientation, capability inventory, operational story, current facts, and projection behavior were considered through their implementation targets and explicit assertions where relevant.

## Recurring implementation patterns

### 1. Public bounded inquiry starts from exact question-family identity

The strongest recurring implementation-backed identity for an answerable inquiry subject is the static `QuestionSurfaceInventoryRow`. Rows bind a `question_family` to example questions, an answering `surface`, CLI `surface_flag`, `answer_responsibility`, `authority_boundary`, bounded dispatch status, required arguments, diagnostic relationships, and implementation reason.

`build_question_surface_inventory()` is deterministic and static. It does not recover a subject from free text. It declares known families such as operational pressure, current operational explanation, derivation explanation, selection explanation, knowledge reachability, capability pressure, ownership ambiguity, observation domains, authority-constrained ownership, source navigation, inquiry orientation, and projection shape visibility.

This means the implementation has a recurring *registered question-family identity* boundary. It is not yet a general subject-resolution engine.

### 2. Bounded ask dispatch validates exact family strings and maps to existing surfaces

`apply_bounded_ask_dispatch()` is the implementation bridge from `ask --question-family <exact-question-family>` to existing answer surfaces. It requires the literal `ask` command shape, checks the family against `build_question_surface_inventory()`, derives bounded eligibility, rejects unknown or non-dispatchable families, and then sets the target surface argument on the parsed CLI namespace.

This is a repeatable routing boundary, but the resolved object is an exact, operator-supplied `QuestionFamily` string. Dispatch does not parse the question text into a subject. It maps a pre-registered family to an existing surface.

### 3. Subject-like values are often explicit operator-provided surface parameters

Some answer surfaces require additional subject or target values before their evidence selection can begin:

- `derivation explanation` requires `domain` and `subject`.
- `selection explanation` requires `target`.
- `source definition/import lookup` requires a query argument, but is not currently bounded-ask dispatchable.
- `inquiry orientation` requires a recorded note id or latest note, but the note is not classified into intent or subject.
- `reference_selection` requires a `domain` and only implements `history` as a supported domain.

The bounded ask implementation preserves this boundary explicitly: required surface arguments are forwarded unchanged as operator-provided values. Missing or extra values cause parser errors rather than inference.

### 4. Surface-local evidence selection begins after a subject, target, domain, note, or query is already supplied

The neighboring surfaces show subject-specific or target-specific work after input identity is known:

- `build_reasoning_path_audit(state, domain, subject, ...)` filters ownership discrepancies, capability need records, pressure, privilege, and operational story information by the already-supplied subject. It explains derivation; it does not discover the subject.
- `build_selection_path_audit(state, target, ...)` normalizes the already-supplied target and compares it against implemented selection surfaces such as current focus, primary pressure, story focus, and pressure categories. It explains selection; it does not infer the target from a natural-language inquiry.
- `build_reference_selection(repo_root, domain)` branches on the already-supplied domain and returns an unsupported-domain result for anything other than `history`. It chooses comparison references only after domain selection.
- `build_inquiry_orientation(state, note)` tokenizes the already-recorded note and performs deterministic lexical overlap against projected fact supports and source navigation. It orients related material; it explicitly refuses semantic interpretation, intent, ownership, recommended action, or next safe move.

The recurring evidence is therefore: identity comes in first; evidence selection follows.

### 5. Answer composition is downstream of already-selected evidence

`operational_story` and `inquiry_orientation` show implementation-local answer-payload objects before rendering. These are answer-composition boundaries, not subject-acquisition boundaries. They assemble focus, pressure, evidence, limitations, support, and authority boundaries from existing surfaces after the surface has already been chosen.

`question_surface_inventory` also exposes `QuestionFamilyDefinition` and `ComposedQuestionFamilyExplanation`, which explain the existing family row for presentation. They do not create new question-family identity.

### 6. Projection, current facts, and capability inventory own neighboring knowledge/read-model behavior, not inquiry subject acquisition

`State.current_facts()` owns current projected fact selection under predicate cardinality. `state._recover_projection_influence_lineage()` composes affected-scope and affected-projection evidence for events but explicitly does not select replay targets, compute projections, invalidate caches, persist snapshots, or expose a runtime surface. `capability_inventory` separates admitted capability facts, executable operation contract labels, and requested capabilities before presentation.

These areas identify or present existing projected knowledge. They do not determine what an inquiry is about.

## Counterexamples and limiting evidence

### Subjects are often operator-provided

The clearest counterexample to a recurring independent subject-resolution responsibility is the explicit parameter requirement in bounded ask and the direct CLI surfaces. `derivation explanation` requires exactly two explicit values (`domain`, `subject`), while `selection explanation` requires exactly one explicit `target`. The inventory notes say these values are not inferred.

### Some subjects are static question-family rows rather than dynamically resolved subjects

Question families are registered by editing the static inventory. Unknown families are rejected or reported as unknown; they are not inferred from prose, recovered responsibilities, or related artifacts. This means question-family identity is implemented as a registry boundary, not a recurring discovery capability.

### Some subject/domain choices are hard-coded inside individual surfaces

`reference_selection` supports only the `history` domain and returns an unsupported-domain result for other values. `selection_path` recognizes implemented target names such as `current_focus`, `primary_pressure`, story focus, and pressure categories. These are local surface rules, not a shared subject-resolution owner.

### Inquiry Orientation is related-material discovery, not subject resolution

Inquiry Orientation is the closest implementation to accepting arbitrary operator prose, but it records raw notes and uses lexical overlap only after receiving the note. Its authority boundary explicitly prevents treating matches as semantic interpretation, operator intent, ownership, concern, recommended action, or next safe move. That is evidence against calling it a subject-resolution responsibility.

### Question families do not currently own all subject identity

Question families own high-level answerable family identity, but parameterized families still require separate surface-local identity (`domain`, `subject`, `target`). Therefore the implementation cannot safely be summarized as "QuestionFamily already resolves the subject." It resolves only the answer family.

## Supported conclusions

### 1. Does the repository currently contain a recurring Inquiry Subject Resolution responsibility?

Partly, but not as a separate owner.

The implementation contains recurring fragments of inquiry subject acquisition:

- exact question-family registration and validation;
- bounded ask mapping from family to existing answer surface;
- explicit operator-provided subject, target, domain, query, or note parameters;
- surface-local normalization or matching after those parameters are present.

However, there is insufficient evidence for a distinct recurring responsibility that generally turns an inquiry question into a subject before subject-specific reasoning begins. Subject acquisition is still distributed across question-family inventory, CLI dispatch, required surface args, and individual surfaces.

### 2. If yes, where is the strongest implementation evidence?

The strongest evidence is the combination of:

1. `QuestionSurfaceInventoryRow` and `build_question_surface_inventory()` as the static answer-family identity registry;
2. `BOUNDED_ASK_DISPATCH_SURFACES` and `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` as the bounded dispatch/required-argument contract;
3. `apply_bounded_ask_dispatch()` as the exact-family validation and mapping adapter;
4. parameterized surfaces such as `reasoning_path`, `selection_path`, and `reference_selection`, which begin evidence selection only after subject/target/domain input is already supplied.

This supports an emerging implementation concern around inquiry subject/target/domain identity, but the concern is compressed rather than separately owned.

### 3. Which implementation responsibilities currently appear compressed?

The following responsibilities appear compressed together:

- **Question-family registration and answerable-subject identity** are compressed in `question_surface_inventory.py` rows.
- **Bounded ask dispatch and subject/target argument forwarding** are compressed in `scripts/seed_local.py` parser handling and `apply_bounded_ask_dispatch()`.
- **Surface-specific subject normalization and evidence filtering** are compressed inside answer surfaces such as `reasoning_path_audit`, `selection_path_audit`, and `reference_selection`.
- **Related-material discovery and answer composition** are compressed in Inquiry Orientation after a note is provided.
- **Question-family explanation and presentation** are compressed with inventory row fields rather than a separate subject model.

### 4. Which adjacent responsibilities already own neighboring behavior?

- **Question Surface Inventory** owns known question-family rows, eligibility status, required-arg visibility, diagnostic relationships, and implementation reasons.
- **Bounded ask dispatch** owns exact-family validation and compatibility mapping to existing surfaces.
- **Reasoning Path** owns derivation evidence for a supplied domain and subject.
- **Selection Path** owns selection explanation for a supplied target.
- **Reference Selection** owns comparison-reference choice for a supplied supported domain.
- **Inquiry Orientation** owns note recording and lexical related-material orientation for a supplied inquiry note.
- **Operational Story / Answer Composition** owns bounded answer assembly after evidence surfaces are already selected.
- **Projection/current facts/capability inventory** own projected knowledge, current fact visibility, admitted capability state, and presentation, not inquiry subject acquisition.

### 5. Does implementation evidence support beginning an Inquiry Subject Resolution responsibility family?

Yes, cautiously, as an investigation or characterization family rather than an implementation change.

Implementation evidence supports beginning a responsibility-family investigation because subject/target/domain acquisition recurs across multiple surfaces, but it is currently distributed and sometimes hard-coded. The next family should be named only after more evidence is recovered; `Inquiry Subject Resolution` is a plausible working label, not repository-proven vocabulary.

The evidence does **not** support implementing semantic parsing, planner behavior, ownership recovery, new question families, or automated subject inference now. A future implementation step would need first to preserve the current explicit-input boundaries and prove which subject identities are registry-owned, operator-provided, or surface-local.

## Unsupported conclusions

- Unsupported: Seed currently understands natural-language questions and resolves semantic subjects from prose.
- Unsupported: Inquiry Orientation already performs semantic subject discovery.
- Unsupported: Question Families alone own complete subject identity for all answering surfaces.
- Unsupported: Reasoning Path or Selection Path should be generalized into a universal subject resolver.
- Unsupported: Projection influence, current facts, capability inventory, or answer composition determine what an inquiry is about.
- Unsupported: A new architecture should be implemented now.

## Confidence

Medium-high confidence that subject acquisition is currently distributed across existing implementation owners.

Medium confidence that a recurring concern is emerging, because multiple surfaces share the pattern `operator/registry supplies identity -> surface selects evidence -> answer composition renders`. The confidence is not high enough to claim a separate implemented responsibility owner, because the code still uses explicit parameters, static rows, and surface-local rules.

## Recommended next action

Do not implement runtime behavior yet.

Recommended next bounded action: produce a small subject-acquisition inventory that classifies each known question family and answer surface by how its subject identity is obtained:

- static question-family identity;
- explicit operator-provided `subject`, `target`, `domain`, `query`, or note id;
- surface-local normalization or hard-coded supported domains;
- no subject parameter;
- not dispatchable.

That inventory should remain read-only and evidence-only. If later converted into a diagnostic or CLI surface, the operational visibility contract requires diagnostic inventory, shape-audit specs, and tests.

## Acceptance answer

Before Seed can determine what knowledge is required, the current implementation usually determines what the inquiry is about by requiring an exact registered question family and, for parameterized surfaces, explicit operator-provided subject/target/domain/query/note identity. Subject-specific evidence selection begins only after those identities exist.

A recurring concern is emerging, but it is not yet a separate implementation owner. Subject acquisition remains distributed across Question Surface Inventory, bounded ask dispatch, CLI parameters, and surface-local rules.
