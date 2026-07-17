# Consumer-Uptake Topology Pass 004

## Repository state examined

- `git rev-parse HEAD`: `58ded871f9a528c1bd1a8154ca3f98891fbe1068`.
- `git status --short`: no output before this pass began.
- PR 1745 is present in the surveyed checkout: `git log --oneline --decorate -5` shows `58ded87 (HEAD -> work) Add selection road sufficiency pass 003 (#1745)`.
- `book_of_seed/selection_road_sufficiency_pass_003.md` exists.

## Relationships compared

This pass compared four bounded relationships:

1. `select_constitutional_views(...)` -> `SelectedConstitutionalViews` -> `selected_constitutional_views_to_composition_request(...)` -> `ConstitutionalViewCompositionRequest` -> `build_constitutional_view_composition(...)`.
2. `select_advancement_need_for_consideration(...)` -> `AdvancementNeedConsiderationSelection` -> `preserve_inquiry_frontier_boundary_testimony(...)`.
3. `InquiryFrontierBoundaryTestimony` -> `assemble_bounded_inquiry_frontier(...)` -> `BoundedInquiryFrontier`.
4. `ConstitutionalPipelineResult` -> `explain_constitutional_pipeline_provenance(...)` -> `ConstitutionalPipelineProvenanceExplanation`.

## Relationship A: constitutional view selection to composition

### Producer

`select_constitutional_views(...)` consumes a `ConstitutionalQuestionProjection` and capability projections. It selects registered view names by exact intersection between `question_projection.selection_keys` and each `capability.capability_keys`, preserves unsupported selection keys as uncertainty, and returns `SelectedConstitutionalViews` with read-only and non-mutating boundaries.

### Producer assertion

The produced artifact asserts only that, for one bounded question projection and the supplied capability projections, these registered view names matched exact deterministic selection keys. It also preserves unsupported-key uncertainty, derives a narrow compatibility answer, and records that no raw question, semantic reasoning, ranking, planning, orchestration, evidence discovery, repository mutation, event-ledger write, or cluster mutation occurred.

### Transported artifact and adapter

`SelectedConstitutionalViews` preserves the bounded question ID, selected view names, uncertainty, compatibility answer, and boundary flags. The adapter `selected_constitutional_views_to_composition_request(...)` reads only `artifact.selected_view_names` and caller-supplied composition purpose / output format. It constructs `ConstitutionalViewCompositionRequest` by forwarding those names as explicit requested views.

### Consumer

`build_constitutional_view_composition(...)` consumes `ConstitutionalViewCompositionRequest`, builds a local contract map from registered constitutional read-model contracts, checks that every requested name is registered and buildable, builds the requested views, correlates existing evidence/unknowns/refusals, and produces `ConstitutionalViewCompositionArtifact`.

### Consumer validations

Composition validates registered-name admissibility and buildability. It refuses unsupported requested view names with `ValueError`. It does not validate the bounded question ID, exact-key comparison occurrence, unsupported-key uncertainty, capability-projection universe, or producer identity.

### Consumer assertion

Composition asserts a new bounded explanation composed from explicitly requested registered constitutional views. Its assertion is not that exact-key selection occurred; it is that the requested registered views were composed read-only into one bounded composition artifact.

### Material preserved and discarded

Preserved material: selected registered view names, composition purpose, output format, resulting contributing view payloads, existing evidence, unknowns, refusals, and read-only/non-mutating boundaries.

Discarded material at the adapter/composition boundary: bounded question ID, selection uncertainty, compatibility answer from selection except insofar as the selected names drive composition, capability projection keys, unsupported requested selection keys, and the exact-key selection basis.

### Characterization

Relationship A supports assertion narrowing plus a new request assertion. The adapter narrows `SelectedConstitutionalViews` to `selected_view_names` and creates an explicit composition request. Composition treats those names as requested registered views, not as proof of a lawful exact-key selection act. The same narrowed value could lawfully come from another producer: `constitutional_view_composition_request(...)` can be constructed directly with explicit requested views. Narrowing does not make the original selection assertion false, but it breaks any claim that composition alone accepts the full producer assertion.

### First unsupported inference

The first unsupported inference is: selected names suitable for composition prove exact-key selection occurrence for a particular bounded question. They do not. Composition proves local registration/buildability and composition of requested views only.

## Relationship B: selected need to frontier testimony

### Producer

`select_advancement_need_for_consideration(...)` consumes an `AdvancementNeedReferenceSet` and focus evidence. It derives a stable selection ID, handles missing, conflicting, ambiguous, mismatched, absent, duplicate, or non-selectable evidence states, and returns a selected state only when exact focus evidence names one visible selectable reference with matching need-set, prior selection, goal, horizon, family, native projection, and native lineage.

### Producer assertion

In the selected state, `AdvancementNeedConsiderationSelection` asserts that one exact visible advancement-need reference has selected-subject standing for consideration within the reference set, need set, selected goal, and horizon. It also preserves visible and non-selected references, focus/provenance refs, unknowns, and conflicts.

### Transported artifact and adapter

`preserve_inquiry_frontier_boundary_testimony(...)` is the consumer of the selected-need artifact and boundary clauses. It is not merely a copier. If the selected reference is absent or not in the `inquiry` family, it returns testimony with no selected inquiry subject. If the reference is a selected inquiry need, it preserves selected-reference identity, native projection and lineage, need-set/selection/goal/horizon bindings, lineage-derived source testimony/component/subject refs, visible evidence refs, and per-clause standing/scope/evidence/family dispositions.

### Consumer validations

The testimony boundary validates selected state, selected-reference presence, and inquiry family. It then binds each clause to the selected reference's identity and lineage. It does not rerun focus-evidence matching against the original reference set.

### Consumer assertion

`InquiryFrontierBoundaryTestimony` asserts preserved boundary testimony for one exact selected inquiry need when the selected-reference standing is present and family is inquiry. It does not establish the frontier, open inquiry, execute examination, or prove that focus evidence was lawfully consumed by the selection producer.

### Material preserved and discarded

Preserved material: selected reference ID, native projection ID, native lineage, need-set ID, selected-need selection ID, selected-goal ID, horizon ID, source testimony/component/subject refs, visible evidence refs, clause refs, clause standing, scope disposition, evidence currency/availability, family disposition, producer/adapter/source lineage, and unowned clause refs.

Discarded or not rechecked: original focus evidence comparison, exact visible-reference search, non-selected references as a full candidate snapshot, and proof that `select_advancement_need_for_consideration(...)` occurred.

### Characterization

Relationship B supports assertion adoption for selected-subject standing plus bounded consumer-side filtering/re-expression. The consumer accepts the upstream selected reference as standing material only when selected state, selected reference, and inquiry family agree. It re-expresses that standing as boundary testimony under the frontier-testimony purpose. This is not full re-establishment of the selected need, because the testimony function does not independently prove focus evidence or the original candidate-set selection act.

### First unsupported inference

The first unsupported inference is: selected need identity coherent in testimony proves that focus evidence was lawfully consumed by the selection producer. It does not. It proves consumer-local selected-inquiry coherence for testimony preservation.

## Relationship C: testimony to bounded inquiry frontier

### Producer

`preserve_inquiry_frontier_boundary_testimony(...)` produces `InquiryFrontierBoundaryTestimony`, preserving selected-inquiry identity and clauses.

### Producer assertion

The testimony artifact asserts boundary testimony for one selected inquiry need, or explicitly records that no selected inquiry subject exists. It preserves clauses and their standing/scope/evidence/family dispositions.

### Consumer

`assemble_bounded_inquiry_frontier(...)` consumes both the selected need and the testimony. It does not rely on testimony alone.

### Consumer validations

Frontier assembly checks:

- selected-need state is `selected` and selected reference exists;
- selected reference is an inquiry-family reference;
- testimony selected-reference ID, native projection ID, native lineage, need-set ID, selected-need selection ID, selected-goal ID, and horizon ID match the selected reference;
- operative clauses are established, inquiry-family, non-conflicting in evidence currency/availability, and within included scope where required;
- every required clause family is present in operative testimony;
- material conflicts are absent.

Refusal states include `not_selected_inquiry_need`, `material_binding_conflict`, and `missing_required_clause_family` before `established` is reached.

### Consumer assertion

When established, `BoundedInquiryFrontier` asserts a new frontier subject: a bounded set of operative inquiry-boundary clauses for the selected inquiry need, with missing/conflict/non-operative/unsupported/unknown/conflicting/stale/unavailable/out-of-scope preservation. It also preserves selected-need and testimony identifiers and lineage.

### Material preserved and discarded

Preserved material: selected-need selection ID, selected need reference ID, native projection and lineage, need-set ID, selected-goal ID, horizon ID, testimony ID, source testimony/component/subject refs, operative clause refs, preserved clause refs, non-operative refs, conflict/missing/unsupported/unknown and other diagnostic clause refs, and full clauses.

Discarded or not proven: producer occurrence for the selected-need act, producer occurrence for testimony preservation, original focus evidence, whether inquiry has been opened or executed, and whether examination has occurred.

### Characterization

Relationship C supports coherence revalidation plus re-establishment. Frontier assembly relies on testimony, independently compares testimony identity against the selected need, judges sufficiency through required operative clause families and conflict checks, and establishes a new frontier subject when those local conditions hold. Coherence success validates only identity and invariant agreement for the frontier boundary; it is not re-execution of the producer act.

### First unsupported inference

The first unsupported inference is: frontier established proves inquiry opened or executed. It does not. The frontier is a bounded subject ready for inquiry-boundary use; it is not an execution record.

## Relationship D: pipeline result to provenance explanation

### Producer

`invoke_constitutional_pipeline(...)` owns ordered invocation of established bounded question input, question projection, capability projection, selection, composition-request adaptation, and composition. It returns `ConstitutionalPipelineResult` preserving each stage artifact.

### Producer assertion

`ConstitutionalPipelineResult` asserts that these stage artifacts exist together as the result of one deterministic pipeline invocation. It preserves bounded question, question projection, capability projection, selection, composition request, and composition.

### Consumer

`explain_constitutional_pipeline_provenance(...)` consumes one completed `ConstitutionalPipelineResult`. It explicitly performs no pipeline stages, capability discovery, semantic matching, persistence, event-ledger write, or cluster mutation.

### Consumer validations and reconstruction

The explanation recomputes projected relationships from preserved artifacts: question keys, capability keys by view, flat capability keys, matched keys, unsupported keys, unknown capabilities, empty-selection explanation, composition contributors, unknowns, refusals, and combined read-only / ledger / mutation flags. It does not execute projection, selection, or composition; it reconstructs the reason trace from completed artifacts.

### Consumer assertion

`ConstitutionalPipelineProvenanceExplanation` asserts an explanation of why the completed pipeline artifacts produced the selected views and composition contributors. It reports existing typed handoffs only. It does not establish upstream stage occurrence outside the supplied result, and it does not make the explanation a substitute for producer warrant.

### Material preserved and discarded

Preserved/projected material: bounded question ID, inquiry provenance, operator inquiry testimony, question selection keys, available capability keys, matched keys, unsupported keys, selected views, unselected/unavailable reasons, selection uncertainty, empty-selection explanation, composition contributors, unknowns/refusals, and aggregate read-only/ledger/mutation flags.

Discarded or not proven: full internal stage bodies, external proof that an arbitrary `ConstitutionalPipelineResult` was returned by `invoke_constitutional_pipeline(...)`, semantic bestness, capability discovery, and upstream establishment beyond the supplied artifacts.

### Characterization

Relationship D supports explanation projection and consumer-local explanatory assertion. It adopts stage artifacts as source material for explanation but does not adopt every stage assertion as newly established truth. It reconstructs relationships among preserved artifacts and establishes an explanation assertion under its own warrant: faithful reading of one completed result.

### First unsupported inference

The first unsupported inference is: explanation equals upstream establishment. It does not. Explanation reports and projects existing typed handoffs; it is not proof that a producer boundary occurred unless the caller also has warrant for the supplied result's production.

## Direct-construction implications

Direct construction remains decisive for uptake characterization:

- A directly constructed `SelectedConstitutionalViews` can feed the adapter and composition if its selected names are registered and buildable. This proves composition-local admissibility, not exact-key selection occurrence.
- A directly constructed `AdvancementNeedConsiderationSelection` can satisfy testimony and frontier identity checks if internally coherent and inquiry-family. Later consumers revalidate coherence but do not prove original focus evidence was lawfully consumed.
- A directly constructed `InquiryFrontierBoundaryTestimony` can be refused by frontier assembly when identity or required clause sufficiency fails. If internally coherent and sufficient, assembly establishes a frontier under its own local warrant without proving testimony producer occurrence.
- A directly constructed `ConstitutionalPipelineResult` can be explained because the explanation reads the supplied artifacts. That explanation is warranted as a projection over the supplied result, not as proof that `invoke_constitutional_pipeline(...)` ran.

## Live owner findings

`seed_runtime/constitutional_pipeline.py` is a live higher owner for the constitutional view path. `invoke_constitutional_pipeline(...)` preserves bounded question, question projection, capability projection, selection, composition request, and composition in one `ConstitutionalPipelineResult`. Therefore the pipeline owner can own an assertion-preserving relationship across projection, selection, adapter, and composition more strongly than composition alone. Composition alone owns only explicit requested registered-view composition.

No equivalent single live owner was found in the selected-need frontier path during this bounded review. The live functions are adjacent producers/consumers: selection, testimony preservation, and frontier assembly. Frontier assembly strengthens the boundary by consuming both selected need and testimony, but that is not the same as a higher orchestration owner that proves the original selection producer occurred.

## Uptake kinds supported

### Assertion adoption

Supported narrowly by Relationship B. The testimony consumer accepts selected-subject standing as material only if selected state, selected reference, and inquiry family are present. The exact adopted assertion is selected inquiry-need standing for testimony preservation. Stable identity: selected reference, native projection/lineage, need set, selection, goal, and horizon. Unsupported inference: focus-evidence selection occurrence.

### Assertion narrowing

Supported by Relationship A. The adapter extracts selected registered view names from a richer selection artifact and creates an explicit composition request. Discarded information includes bounded question ID, unsupported-key uncertainty, compatibility answer, and selection basis. The narrowed value can lawfully come from another producer through a direct composition request. Narrowing breaks reliance on the full selection assertion but does not invalidate the narrowed handoff.

### Coherence revalidation

Supported by Relationships B and C, especially C. Consumers compare upstream assertions against other bounded material and refuse on identity or invariant conflict. Success validates coherence, not producer occurrence. It can preserve upstream standing for a new local purpose, and in the frontier case it also contributes to new consumer-local standing.

### Re-establishment

Supported by Relationship C. Frontier assembly uses selected need and testimony as input, performs identity and sufficiency judgment, and establishes `BoundedInquiryFrontier` as a new constitutional subject when local conditions hold. Upstream selected-need and testimony claims remain inputs/testimony for the frontier boundary; they are not automatically re-proven.

### Explanation projection

Repository evidence requires an additional uptake kind. Relationship D is not adequately described as simple adoption, narrowing, coherence revalidation, or re-establishment of upstream subjects. It projects and reconstructs relationships among preserved stage artifacts and establishes an explanation assertion under its own warrant. Explanation projection is durable because the runtime has a dedicated `ConstitutionalPipelineProvenanceExplanation` type and function with explicit boundaries.

### Typed value transport / adapter handoff

Repository evidence also requires distinguishing mechanical typed transport from constitutional-road uptake. The selection-to-composition adapter performs typed value transport and request creation; it is not by itself a constitutional road. It may participate in a larger road when owned by a live pipeline invocation.

## Uptake kinds contradicted or limited

- Full assertion adoption is contradicted for Relationship A: composition does not adopt the full exact-key selection assertion.
- Re-establishment is contradicted for Relationship B: testimony preservation re-expresses and preserves selected-inquiry boundary testimony but does not independently establish the selected need.
- Producer-occurrence validation is contradicted for Relationships A, B, C, and D when only direct artifacts are supplied.
- Projection as automatic re-establishment is contradicted for Relationship D: provenance explanation reports and reconstructs; it does not re-establish upstream pipeline stages.
- Adapter as automatic constitutional road is contradicted by Relationship A: the adapter copies selected names into a request with no validation of the original producer act.

## Constitutional-road definition result

The current singular road definition is too narrow if it requires every lawful producer-to-consumer relationship to be one in which the consumer accepts the producer's assertion for a declared purpose. Repository evidence shows several lawful uptake boundaries:

- full or partial assertion adoption;
- assertion narrowing into a new request;
- coherence revalidation against independently supplied material;
- re-establishment of a new subject under consumer warrant;
- explanation projection over preserved artifacts;
- typed value transport that may support but does not itself constitute a road.

The durable concept supported by repository evidence is broader constitutional uptake: a warranted consumer boundary that receives upstream material and either adopts, narrows, revalidates, projects, transports, or re-establishes a bounded assertion under local conditions. Constitutional roads remain a subfamily: assertion-preserving producer-to-consumer uptake where the consumer relies on the producer assertion for a declared purpose and validates needed identities/invariants. Some adapters and projections are lawful uptake without being roads by themselves.

## Additional kinds discovered

- **Explanation projection:** an explanation consumes preserved artifacts, reconstructs relationships, and produces an explanation assertion without performing or proving the upstream acts.
- **Typed request handoff:** an adapter extracts bounded values and creates a consumer request. It may be warranted as value transport/request formation while not warranting full assertion uptake.

## Claims remaining unresolved

- Whether a future selected-need live owner should preserve selection, testimony, and frontier assembly in one result is unresolved; no such owner was established in this bounded review.
- Whether every existing adapter should be classified as typed request handoff or road participant is unresolved by scope control; no repository-wide handoff inventory was conducted.
- Whether producer occurrence should be encoded in artifacts is unresolved and intentionally not implemented.
- Whether explanation projection should have subfamilies beyond pipeline provenance is unresolved.

## Book chapters updated

- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`: road definition narrowed to assertion-preserving uptake, and constitutional uptake added as broader grammar.
- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`: direct construction clarified as insufficient for producer occurrence even when consumer-local coherence succeeds.
- `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`: consumer validation distinguished from act occurrence.
- `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md`: selection-to-consumer uptake split into adoption, narrowing, and coherence revalidation.
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`: explanation projection distinguished from upstream establishment.
- `book_of_seed/08-authority-communication-and-stopping/communication-and-handoff.md`: typed value transport and adapter handoff distinguished from constitutional roads.
- `book_of_seed/concordance.md`: durable uptake, assertion narrowing, coherence revalidation, re-establishment, explanation projection, and typed request handoff entries added.

## Bounded resolution

constitutional uptake is broader than constitutional roads

Book of Seed consumer-uptake topology pass 004 complete.
