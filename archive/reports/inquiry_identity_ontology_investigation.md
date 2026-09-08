# Inquiry Identity Ontology Investigation

## Scope

This bounded investigation reviewed current implementation evidence around Question Families, Question Surface Inventory, Reasoning Path, Selection Path, Reference Selection, Inquiry Orientation, Operational Story, Architectural Orientation, Answer Composition, question registration, and bounded ask dispatch.

The question was whether implementation uses the word and role of `subject` as one architectural concept for everything an inquiry is "about", or whether multiple distinct implementation concepts are compressed behind that vocabulary.

No implementation behavior, ownership recovery, vocabulary, ontology, semantic parsing, runtime behavior, question-family behavior, or compatibility behavior was changed.

## Implementation evidence reviewed

### Question family and bounded ask registration

* `seed_runtime/question_surface_inventory.py` defines Question Families as exact inventory row identities with answering surfaces, flags, answer responsibilities, authority boundaries, bounded statuses, dispatch surfaces, and required surface arguments.
* The bounded ask dispatch map routes exact `question_family` strings to implementation surfaces. Only two families require operator-provided surface arguments: `derivation explanation` requires `domain` and `subject`; `selection explanation` requires `target`.
* `scripts/seed_local.py` enforces exact `ask --question-family <exact-question-family>` routing, rejects unknown families, rejects free-text `ask` without a family, rejects surface args unless the selected family requires them, and forwards explicit surface args unchanged to the mapped surface.

### Reasoning Path

* `seed_runtime/reasoning_path_audit.py` models `ReasoningPathAudit` with both `domain` and `subject` fields.
* `build_reasoning_path_audit(state, domain, subject, ...)` uses `subject` to match ownership-discrepancy rows, diagnostic capability records, capability-needs subjects/diagnostics, pressure text, privilege capability names, and serialized operational-story content.
* The same function uses `domain` differently: it is not normalized as a target, and it participates mainly in category/focus matching and report identity.
* The output separates evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundary.

### Selection Path

* `seed_runtime/selection_path_audit.py` models `SelectionPathAudit` with `target`, not `subject`.
* `build_selection_path_audit(state, target, ...)` normalizes the target using strip/lower/hyphen-space-to-underscore normalization, then routes special targets such as `current_focus` and `primary_pressure` and pressure-category matches.
* Selection output is organized around selected value, candidate set, selection factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundary.
* This is different from Reasoning Path: the identity drives selection-surface recognition and candidate ranking explanation rather than derivation matching through evidence and consumers.

### Reference Selection

* `seed_runtime/reference_selection.py` models `ReferenceSelection` with `domain` and `question`, not `subject` or `target`.
* `build_reference_selection(repo_root, domain)` only implements `domain == "history"`; unsupported domains return an unknown reference-selection answer with limitations.
* The selected reference is a comparison-reference object, with alternatives, selection rationale, limitations, and authority boundary. It is not a fact subject and not a selection target.

### Inquiry Orientation and Architectural Orientation / Answer Composition

* `seed_runtime/inquiry_orientation.py` models raw inquiry material as `InquiryNoteRecord` with `note_id`, `raw_note`, timestamp, source, workspace, and session.
* `record_inquiry_note` validates only non-empty note text and appends to an isolated JSONL probe store; the authority boundary says the note is operator prose, not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction.
* `build_inquiry_orientation(state, note)` composes related material by tokenizing the note and finding deterministic lexical overlaps with projected fact supports and source-navigation matches.
* Implementation-local `_ArchitecturalOrientationEvidence` and `_ArchitecturalOrientationAnswer` separate evidence collection from answer composition. They do not create a stable subject identity from note prose.
* Related fact-support matches label material by `support.subject`, but the inquiry's own identity remains the note record and lexical tokens, not a promoted repository subject.

### Source Navigation / query identity

* `seed_runtime/source_navigation.py` models repository source lookup as `SourceNavigationView(query=...)`.
* `build_source_navigation(state, query)` strips the query, then performs syntactic matches against source fact supports: exact module/path subject matches, path matches, definition values, final dotted segment matches, and dependency mentions.
* The same view also includes explicit non-claims that it does not infer calls, behavior, reachability, ownership authority, semantic relevance, or truth beyond source-navigation matches.
* `query` is therefore an operator lookup key over projected source facts, not the same lifecycle as fact `subject`, selection `target`, or note identity.

### Operational Story

* `seed_runtime/operational_story.py` builds an `OperationalStory` with `focus`, `pressure`, `supporting_evidence`, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and boundary.
* The implementation composes existing surfaces: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path.
* `focus` is derived from the primary pressure item, and capability display renders subject counts from capability needs. Operational Story does not require an operator-supplied `subject`, `target`, `domain`, `query`, or `note` identity.

## Recurring implementation patterns

1. **Explicit identity is required before bounded subject-specific surfaces run.** Bounded ask does not parse free text into a subject. It requires an exact `question_family`; parameterized families then require exact `--surface-args` counts and forward those values unchanged.
2. **Different surfaces require different identity shapes.** Reasoning Path requires `(domain, subject)`, Selection Path requires `target`, Reference Selection requires `domain`, Source Navigation requires `query`, and Inquiry Orientation requires a preserved `note` record.
3. **Identity validation is surface-specific.** Bounded ask validates family existence and parameter count; Reasoning Path does broad string matching; Selection Path normalizes and recognizes implemented selection targets; Reference Selection restricts domain choices to `history`; Inquiry Note recording validates non-empty prose only; Source Navigation strips and syntactically matches a query.
4. **Identity normalization is not shared.** Selection targets are normalized with lower/underscore conversion. Source-navigation queries are stripped. Inquiry notes are tokenized with a regex and minimum token length. Reasoning-path subjects are matched by case-insensitive helper checks rather than the selection target normalizer. Question families require exact registered strings.
5. **Identity participates in routing differently from evidence selection.** Question Family identity routes to surfaces. Selection target identity chooses whether a selection explanation is implemented. Reasoning subject/domain identity filters evidence and consumers. Query identity retrieves projected source rows. Note identity selects stored operator prose, while note tokens collect related material.

## Explicit distinctions already present

### `question_family`

A public answerable-family identity in the inventory and bounded ask dispatch path. It controls bounded eligibility, dispatch surface, required surface args, diagnostic relationship, and unknown-family rejection. It is not evidence subject identity.

### `subject`

At least two implementation meanings appear:

* fact/support/diagnostic subject: `FactSupport.subject`, ownership-discrepancy row subject, capability-need subjects, source-navigation row subject;
* Reasoning Path's operator-provided `subject`, used as a matching key across diagnostic rows, needs, pressure text, privilege names, and operational-story serialization.

Those meanings overlap in some surfaces, but implementation does not establish one stable repository-wide inquiry subject ontology.

### `target`

Selection Path target is an operator-provided selection-surface key. It is normalized for target matching and used to explain selected pressure/focus candidates. It is not treated like Reasoning Path's subject.

### `domain`

Domain is surface-specific. Reasoning Path accepts a domain alongside subject for derivation context and category/focus matching. Reference Selection accepts a domain but currently supports only `history`, where domain selects the comparison-reference implementation path.

### `query`

Source Navigation query is a lookup expression over projected source fact supports. It is stripped and matched syntactically against module/path/value/final-segment evidence and carries explicit non-claims against semantic promotion.

### `note`

Inquiry Orientation note identity is a preserved operator-prose record. The note is not converted into facts, goals, tool needs, decisions, runtime instructions, or stable subjects. Its text is tokenized only to find bounded lexical overlap.

### `reference`

Reference Selection's selected reference is a comparison artifact such as a previous comparable snapshot. It participates in selection rationale and alternative reference visibility, not fact attachment or subject-specific reasoning.

### `focus`

Operational Story's focus is derived from primary pressure and is composed as answer material. It is not an operator identity argument and not a fact subject.

## Counterexamples considered

### Evidence that could suggest one recurring architectural concept

* Many surfaces are answering something an operator is "about": a derivation subject, a selection target, a history domain, a source query, or a note.
* Reasoning Path can match its `subject` against several implementation values: row subjects, candidate capabilities, diagnostic conflicts, capability need subjects/diagnostics, pressure text, privilege capability names, and operational story content.
* Inquiry Orientation can discover related material whose label is a projected fact-support subject.
* Source Navigation rows have a `subject` even though the lookup input is called `query`.

These similarities show a recurring need for explicit inquiry anchoring, but they do not prove one architectural concept because validation, normalization, routing, output shape, and authority boundaries differ by surface.

### Evidence against identical treatment

* Bounded ask requires `domain, subject` for derivation explanation but `target` for selection explanation. The required args are explicitly different.
* Selection Path has a target normalizer and target-specific implemented-surface checks; Reasoning Path does not use that target normalization and instead filters derivation evidence.
* Reference Selection rejects unsupported domains and only implements `history`; it does not accept subject or target.
* Inquiry Orientation treats note prose as non-authoritative operator evidence and explicitly refuses fact/goal/tool/decision/runtime promotion.
* Source Navigation query carries non-claims against semantic relevance and uses source-fact syntactic matching.
* Operational Story composes current focus without an operator-provided subject.

## Supported conclusions

### 1. Does implementation use one architectural concept for inquiry identity, or several?

**Several distinct implementation concepts.** Current code has a recurring pattern of explicit inquiry anchoring, but the anchors are not one architectural concept in implementation. `question_family`, `subject`, `target`, `domain`, `query`, `note`, `reference`, and `focus` have distinct validation rules, normalization rules, routing roles, evidence-selection roles, output structures, and authority boundaries.

### 2. Where is the strongest implementation evidence?

The strongest evidence is the bounded ask registration and dispatch path plus the parameterized audit surfaces:

* `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` differentiates `derivation explanation` as `(domain, subject)` from `selection explanation` as `(target,)`.
* `apply_bounded_ask_dispatch` enforces exact question-family identity and exact surface-argument counts, then forwards parameters unchanged to the mapped surface.
* `build_reasoning_path_audit` uses `domain` and `subject` to collect derivation evidence, while `build_selection_path_audit` uses normalized `target` to explain selected pressure/focus candidates.

This is stronger than prose because it determines CLI acceptance, error behavior, dispatch target, and answer construction.

### 3. Which implementation concepts appear conflated?

The implementation vocabulary appears most conflated around `subject`:

* Fact/support subjects and source-navigation row subjects are projected knowledge/evidence identities.
* Reasoning Path's `subject` is an operator-provided derivation-matching key that may match row subjects, capability names, diagnostic conflicts, capability-need subjects/diagnostics, pressure text, privilege capability names, and serialized story content.
* Diagnostic inventory prose and prior investigation reports use `subject` as a general "thing this is about" label in places where current code may actually mean diagnostic row subject, capability-need affected subject, query key, or operator-supplied matching term.

`domain` is also overloaded between derivation context and reference-selection routing. `question` appears in Reference Selection as a report field but not as the same identity as Question Family registration.

### 4. Which distinctions are already explicit?

Explicit distinctions already exist for:

* Question Family registration and bounded dispatch eligibility.
* Parameterized derivation explanation requiring `domain` plus `subject`.
* Parameterized selection explanation requiring `target`.
* Reference Selection domain restriction to `history`.
* Inquiry note identity as preserved prose with a strict non-promotion authority boundary.
* Source Navigation query identity as syntactic lookup over projected source facts with explicit non-claims.
* Operational Story focus as composed answer material rather than supplied inquiry identity.

### 5. Does implementation evidence support treating "subject" as stable repository vocabulary?

**Only with scope qualifiers.** Implementation evidence supports `subject` as stable vocabulary in specific data structures such as facts, fact supports, source-navigation rows, ownership-discrepancy rows, capability-need subject sets, and Reasoning Path's parameter name. It does **not** support treating bare `subject` as a stable repository-wide ontology for every inquiry identity.

A safer implementation-backed phrasing is: current repository code has multiple inquiry-anchor shapes, one of which is called `subject` in several surfaces. Bare `subject` should not be promoted to a universal inquiry-identity concept without further implementation evidence.

## Unsupported conclusions

The current implementation evidence does **not** support concluding that:

* all inquiry "aboutness" identities are one architectural concept;
* `subject`, `target`, `domain`, `query`, and `note` are synonyms;
* inquiry notes should become fact subjects;
* selection targets should be renamed or normalized into subjects;
* Reference Selection domains should become subjects;
* Question Family registration is an inquiry-subject ontology;
* a distinct Inquiry Subject Resolution owner already exists.

## Confidence

**High** that current implementation distinguishes several concepts under inquiry "aboutness" vocabulary. The evidence is executable and structural: CLI arguments, dispatch maps, dataclass fields, validation paths, normalization helpers, and answer composition functions differ across surfaces.

**Medium** on the exact future boundary names. The implementation strongly shows distinct concepts, but it does not yet name a dedicated owner such as Inquiry Subject Resolution, nor does this investigation recover ownership.

## Recommended next action

Do not rename or recover ownership as part of this investigation.

Recommended next bounded action: create a small follow-up inventory of inquiry-anchor shapes from implementation evidence only, listing each surface's accepted identity fields, validation, normalization, routing role, evidence-selection role, output field, and non-claims. That would preserve the current distinctions without promoting `subject` into a universal ontology.

## Acceptance answer

When the repository says an inquiry is "about" something, it is **not always the same kind of thing** in current implementation. Multiple architectural concerns are compressed behind broad aboutness vocabulary, and the word `subject` is used for several specific implementation roles rather than one stable repository-wide inquiry identity concept.
