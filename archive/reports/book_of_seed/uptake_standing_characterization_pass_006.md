# Uptake-Standing Characterization Pass 006

## Repository state examined

- `git rev-parse HEAD`: `24232f2b642bd1b4ca09b4c10fb78e08c0f7cd7a`.
- `git status --short`: no output at survey start.
- PR 1747 is present in the surveyed checkout as `24232f2 Characterize uptake dimensions pass 005 (#1747)`.
- `book_of_seed/uptake_dimension_characterization_pass_005.md` exists.

Repository evidence controls this pass. Names, state labels, Book language, and dataclass shape are treated as testimony unless supported by producer and consumer bodies.

## Primary relationships compared

1. `AdvancementNeedConsiderationSelection -> preserve_inquiry_frontier_boundary_testimony(...) -> InquiryFrontierBoundaryTestimony`.
2. `AdvancementNeedConsiderationSelection + InquiryFrontierBoundaryTestimony -> assemble_bounded_inquiry_frontier(...) -> BoundedInquiryFrontier`.
3. `ConstitutionalPipelineResult -> explain_constitutional_pipeline_provenance(...) -> ConstitutionalPipelineProvenanceExplanation`.
4. `invoke_constitutional_pipeline(...) -> ConstitutionalPipelineResult`.

## Consumer-standing matrices

### Relationship A: selected need to frontier testimony

| upstream material | standing assigned by consumer | evidence for that standing | consumer constraints | consumer assertion | assertion scope | new standing produced | upstream claims not inherited | producer occurrence established? | direct-construction consequence |
|---|---|---|---|---|---|---|---|---|---|
| selected need artifact | caller-supplied selected inquiry representation, with local field dependence | The testimony producer reads `selected_need.selection_state`, `selected_need.selected_reference`, and requires `ref.family == "inquiry"`; otherwise it returns a no-selected-inquiry testimony. | Must have selected state, selected reference, and inquiry family. | This testimony preserves clauses for the selected reference fields supplied on the artifact. | premise-relative and source-relative | boundary testimony for that exact supplied selected need | It does not prove `select_advancement_need_for_consideration(...)` ran, that focus evidence was validated, or that the selection assertion is true. | No. The consumer accepts fields; it does not call or verify the selector. | A directly constructed selected artifact with coherent fields can receive the same consumer treatment. |
| selected reference | internally coherent transported reference | The producer copies `reference_id`, `native_projection_id`, `native_lineage`, `need_set_id`, `selection_id`, `goal_establishment_id`, `horizon_id`, and evidence refs from `ref`. | `native_lineage` must unpack into three values on the selected path; otherwise construction fails mechanically. | The output records selected-reference identity and lineage as supplied. | source-relative | preserved identity binding inside testimony | Reference truth, source testimony truth, and native producer occurrence are not established. | No. | Direct construction can imitate copied identity fields. |
| selection state | mechanical gate value | Branch on `selection_state == "selected"`. | Non-selected state refuses selected-path preservation and yields null selected-need fields. | The testimony state is conditioned on the supplied selection-state value. | premise-relative | selected-path or no-selected-inquiry testimony | The gate does not prove why the state was selected. | No. | Direct construction of state value can pass the gate. |
| clause inputs | supplied premises whose clause standings are preserved | Loop constructs `InquiryFrontierBoundaryClause` from each `FrontierBoundaryClauseInput`, copying standing, dispositions, evidence currency, availability, lineage, and roles. | Ownership basis is locally classified from non-empty producer or adapter refs with lineage. | The producer preserves unordered stage-owned or unowned clauses for this selected need. | source-relative | attributed clause testimony | Clause truth, clause producer occurrence, and adapter occurrence are not proven. | No. | Directly supplied clause inputs are enough for preservation. |
| producer and adapter lineage | internally classified ownership representation | `_ownership` returns `stage_producer_lineage`, `adapter_lineage`, or `unowned` only from field presence. | Producer wins if both producer fields exist; adapter only if no producer ownership basis exists. | The clause has an ownership-basis label derived from supplied lineage fields. | source-relative | ownership-basis classification | Matching lineage fields are not lineage provenance established. | No. | Direct construction can imitate ownership basis. |

Smallest lawful assertion: given a supplied selected inquiry need artifact and supplied clauses, the function preserves boundary testimony bound to the selected-reference fields and locally classifies clause ownership from supplied lineage fields. It may not assert that the selector ran or that clause producers occurred.

### Relationship B: selected need and testimony to frontier

| upstream material | standing assigned by consumer | evidence for that standing | consumer constraints | consumer assertion | assertion scope | new standing produced | upstream claims not inherited | producer occurrence established? | direct-construction consequence |
|---|---|---|---|---|---|---|---|---|---|
| selected need | supplied identity premise and selected-inquiry gate | The assembler sets identity conflict from `selected_need.selection_state != "selected"` or missing selected reference, then compares testimony fields to the selected reference fields. | Selected state, selected reference, inquiry family, and identity equality across testimony and selected reference. | The frontier is assembled only if the supplied selected need and testimony identity bindings agree. | premise-relative | consumer-local frontier result | It does not prove the selected need was lawfully selected. | No. | A coherent directly constructed selection can satisfy the assembler. |
| testimony artifact | internally coherent bundle of preserved clauses and bindings | The assembler reads `testimony.clauses`, `testimony.testimony_id`, selected-need fields, lineage fields, and copied source refs. | Identity comparisons against selected reference; explicit conflict collection. | The testimony is usable when its material bindings match the selected need and clauses pass operative checks. | source-relative and premise-relative | frontier assembled from supplied testimony | It does not prove `preserve_inquiry_frontier_boundary_testimony(...)` ran. | No. | A directly constructed testimony can be accepted if coherent. |
| clauses | operative coherence candidates | `_is_operatively_coherent` requires `clause_standing == "established"`, `family_disposition == "inquiry"`, no conflicting evidence currency or availability, and included scope for the scope family. | All required clause families must appear among operative clauses; conflicts refuse establishment. | Operative clauses cover required frontier families without material conflict. | established for consumer-local operative coverage; source-relative as to clause claims | `frontier_state="established"` when coverage and bindings pass | Clause truth and clause producer occurrence are not inherited. | No. | Direct construction of clauses with matching fields and standings can produce an established frontier state. |
| identity and lineage bindings | internal agreement constraints | Comparisons check testimony selected-reference id, native projection id, native lineage, need set, selection id, selected goal id, and horizon id against selected reference. | Any mismatch yields `material_binding_conflict`. | Identity coherence is established for this assembly boundary. | established consumer-local coherence | coherent frontier identity binding | Stable identifiers and matching lineage fields do not establish lineage provenance. | No. | Matching fabricated fields pass; mismatches refuse. |

Smallest lawful assertion: given this selected need artifact and this testimony artifact, the supplied clauses coherently establish a bounded inquiry frontier only when required clause-family coverage and material bindings pass. The establishment is consumer-local and does not establish producer occurrence, selected-need truth, testimony truth, inquiry opening, execution, or result knowledge.

### Relationship C: pipeline result to provenance explanation

| upstream material | standing assigned by consumer | evidence for that standing | consumer constraints | consumer assertion | assertion scope | new standing produced | upstream claims not inherited | producer occurrence established? | direct-construction consequence |
|---|---|---|---|---|---|---|---|---|---|
| `ConstitutionalPipelineResult` | supplied artifact bundle | The explanation reads fields from `result` and states it performs no pipeline stages, discovery, semantic matching, persistence, event-ledger write, or mutation. | Dataclass shape and accessible fields; no owner seal or invocation proof. | Explanation reports relationships among existing supplied typed handoffs. | source-relative and premise-relative | provenance explanation artifact | It does not prove the result came from `invoke_constitutional_pipeline(...)`. | No. | Direct construction can receive the same explanation path. |
| question keys and capability keys | recomputed field relationship | It computes `matched_keys` and `unsupported_keys` by comparing `result.question_projection.selection_keys` to capability keys flattened from `result.capability_projection`. | Key equality only. | These question keys match or fail to match supplied projected capability keys. | established for this local comparison; source-relative to supplied artifacts | local explanation of key matching | It does not verify question keys correspond to the bounded question. | No. | Fabricated projections with chosen keys drive the same result. |
| selected views | copied selection assertion | It copies `result.selection.selected_view_names` and uncertainty. | No check that selected views follow from matched keys. | The supplied selection artifact says these views were selected. | source-relative | explanation preserves selection fields | It does not establish lawful selection occurrence. | No. | Directly constructed selection fields are explained as supplied. |
| composition request and contributors | copied composition output relationship | It copies contributing view names from `result.composition.contributing_views`, unknowns, and refusals; it does not read or compare `composition_request`. | No check that request follows from selected views or that contributors follow from the request. | The supplied composition artifact has these contributors, unknowns, and refusals. | source-relative | explanation of supplied composition fields | It does not prove composition request formation or composition occurrence. | No. | Direct construction can imitate completed fields. |
| read-only and mutation flags | aggregate mechanical values | It aggregates stage `read_only`, `writes_event_ledger`, and `mutates_cluster` booleans from supplied artifacts. | Boolean aggregation only. | The supplied stage artifacts collectively report these side-effect flags. | premise-relative | side-effect summary | It does not prove those stages occurred. | No. | Fabricated booleans alter the summary. |

Smallest lawful assertion: the explanation says why the supplied artifact fields relate under its local comparisons and copies. It is not an occurrence-relative explanation unless the caller separately knows the supplied result came from the live owner.

### Relationship D: live pipeline owner

| upstream material | standing assigned by consumer | evidence for that standing | consumer constraints | consumer assertion | assertion scope | new standing produced | upstream claims not inherited | producer occurrence established? | direct-construction consequence |
|---|---|---|---|---|---|---|---|---|---|
| pipeline request | caller-supplied premise plus already-established bounded question by request contract | `invoke_constitutional_pipeline` takes `ConstitutionalPipelineRequest`, assigns `bounded_question = request.bounded_question`, and uses request formatting and capability sources. | No validation in owner that the bounded question was produced by its responsible boundary; it relies on the supplied request. | This invocation uses the supplied request values. | premise-relative | live invocation context | It does not re-establish bounded-question provenance. | Owner occurrence yes for pipeline stages after call begins; upstream request assertions no. | Direct construction bypasses ordered invocation. |
| stage outputs | producer-established for this live call boundary | The owner calls `project_constitutional_question`, then `project_constitutional_capabilities`, then `select_constitutional_views`, then `selected_constitutional_views_to_composition_request`, then `build_constitutional_view_composition`, and returns all artifacts. | Ordered invocation is fixed by function body. | The returned result contains artifacts co-produced by this owner in that order from the request. | established for ordered invocation and artifact coexistence | live pipeline result | Stage internal assertion truth is only as strong as each stage body and supplied inputs. | Yes, when caller has the returned object from this function call. | A directly constructed identical instance has field equality but lacks live-owner occurrence standing. |
| artifact coexistence and producer attribution | established at live boundary, not represented in output type | Return statement packages the just-produced artifacts into `ConstitutionalPipelineResult`; output fields contain no seal distinguishing live return from direct construction. | Caller context must preserve live-return knowledge externally. | These artifacts coexisted in this invocation. | established in call context; not representable inside result | contextual live-result standing | Universal authority for arbitrary instances is not established. | Yes in the live call context only. | Direct construction can imitate fields but not call-context occurrence. |

Smallest lawful assertion: a result returned directly by the owner has stronger contextual standing than an arbitrarily constructed instance with identical fields. The owner establishes ordered invocation, artifact coexistence, and immediate producer attribution for the pipeline wrapper, while not independently proving every upstream request premise or embedding that distinction into `ConstitutionalPipelineResult`.

## Upstream standings supported

- Producer-established assertion is supported only when the consumer or observer has evidence of the responsible producer boundary occurrence. In this pass, live return from `invoke_constitutional_pipeline(...)` supports wrapper-stage occurrence and ordered invocation. Direct construction cannot imitate that call-context standing.
- Adopted assertion is supported as purpose-bounded uptake when a consumer accepts a field or artifact for an exact local purpose, such as the assembler accepting clause `clause_standing == "established"` as an operative criterion without proving the clause producer occurred.
- Testimony is supported where artifacts preserve attributed claims for later examination rather than fact, especially `InquiryFrontierBoundaryTestimony` and the pipeline explanation's explicit testimony boundary.
- Supplied premise is supported where functions condition outputs on caller-supplied artifacts: selected need and clauses for testimony preservation, selected need and testimony for frontier assembly, and pipeline result for provenance explanation.
- Internally coherent representation is supported where consumers compare fields for agreement: frontier assembly identity comparisons and required operative clause-family coverage.
- Mechanical value is supported where field values are transported or recomputed without adopting the larger upstream artifact assertion: pipeline key matching, copied composition contributors, and side-effect boolean aggregation.

## Upstream standings contradicted

- Type acceptance is not enough to prove producer occurrence.
- Matching lineage fields are not enough to prove lineage provenance.
- `frontier_state="established"` does not establish selected-need truth, testimony truth, inquiry opening, producer occurrence, execution, or result knowledge.
- `ConstitutionalPipelineProvenanceExplanation` does not, by itself, prove a verified pipeline occurrence.
- Directly constructed artifacts are not equivalent to live-produced artifacts on occurrence standing even when field values are identical.

## Consumer assertion scopes supported

More than one scope can apply on different axes.

- Source-relative: supported when outputs report what supplied artifacts contain, such as selected view names, contributing views, clause fields, and lineage fields.
- Premise-relative: supported when the result is lawful only given caller-supplied material, such as preserving testimony for a supplied selected need or assembling a frontier from supplied selected need plus testimony.
- Conditional: useful descriptively when a result depends on supplied identities and standings being valid, but the implementation more directly shows premise-relative and coherence-gated assertions.
- Provisional: useful descriptively where unresolved provenance remains, but not promoted as a durable kind by this pass.
- Established: supported only for exact consumer-local assertions whose warrant the body checks, such as frontier identity coherence, operative family coverage, local key matching, or live pipeline ordered invocation in call context.

## Live-producer versus direct-construction comparison

`invoke_constitutional_pipeline(...)` has stronger standing than direct construction because the owner performs the ordered stage calls and immediately packages their outputs. A direct `ConstitutionalPipelineResult(...)` with identical fields has the same shape and may satisfy downstream readers, but it lacks evidence that the owner invoked stages in order. The result type does not encode this distinction, so downstream functions that receive only a result instance cannot tell which path produced it.

## Provenance-explanation standing result

The audited claim was: `ConstitutionalPipelineProvenanceExplanation` explains why completed pipeline artifacts produced the selected views and composition contributors.

Implementation supports a narrower claim: the explanation reports why supplied artifact fields relate under local key comparisons and field copying. It computes question/capability key matches, preserves selected-view and composition fields, and aggregates side-effect flags. It does not check that question keys correspond to the bounded question, selected views follow from matched capability keys, the composition request follows from selected views, composition contributors follow from the request, or that the supplied result came from `invoke_constitutional_pipeline(...)`.

When called immediately on a live result returned by `invoke_constitutional_pipeline(...)`, external call context can add occurrence standing for the pipeline wrapper's ordered invocation. The explanation type itself cannot represent that stronger context.

## Frontier-establishment standing result

`frontier_state="established"` establishes only the assembler's local result: selected inquiry gate passed, selected-need/testimony bindings matched, no material conflict was detected, and operative clauses covered required clause families. The assembler body supports identity coherence, required clause-family coverage, and operative frontier standing from supplied clause standings and dispositions.

It does not establish producer occurrence, selected-need truth, testimony truth, source evidence truth, inquiry opening, authorization, execution, recording, event-ledger write, cluster mutation, or result knowledge. The hypothesis is therefore supported only in bounded form: given this selected-need artifact and this testimony artifact, the supplied clauses coherently establish a bounded inquiry frontier.

## Constitutional principle result

The candidate durable grammar is supported with one refinement:

A consumer may produce only the assertion warranted by both its own act and the standing it lawfully assigns to each upstream input. Coherence, construction, type acceptance, or field transport may warrant a source-relative, premise-relative, or consumer-local established result without proving upstream producer occurrence. A downstream subject may be established under consumer-local warrant while its upstream dependencies remain testimony, premises, or internally coherent representations.

The refinement is that inherited producer standing is not automatic: it depends on evidence of producer occurrence and on whether the consumer's assertion requires that occurrence.

## Durable Book grammar recovered

- Consumer-local establishment can coexist with weaker upstream standing.
- Assertion adoption is purpose-bounded and is not independent verification.
- Source-relative explanation is not occurrence-relative explanation.
- Internally coherent bundle is not lawfully produced bundle.
- Live owner return can carry contextual occurrence standing that the artifact type does not encode.
- Downstream standing may combine inherited warrant, adopted assertions, supplied premises, testimony, mechanical values, and consumer-local checks.

## Terms retained as descriptive only

- `source-relative`
- `premise-relative`
- `conditional`
- `provisional`
- `internally coherent representation`
- `mechanical value`

These are useful report vocabulary in this pass, but the evidence does not require promoting them to top-level concordance entries.

## Claims contradicted

- “Completed pipeline artifacts” does not mean verified pipeline occurrence when the explanation receives only a result instance.
- “Produced the selected views and composition contributors” is too strong for the explanation alone; selected views and contributors are copied from supplied artifacts, while only key matching is recomputed.
- “Established frontier” does not mean all upstream premises, lineage, or producers are established.
- “Stable identifier” does not mean verified lineage.
- “Function-produced artifact” does not make every arbitrary instance of the same type universally authoritative.

## Claims remaining unresolved

- Whether future consumers should represent occurrence standing explicitly is unresolved and out of scope.
- Whether clause `clause_standing="established"` is backed by a responsible clause producer is unresolved at this boundary.
- Whether the supplied bounded question in a pipeline request was itself produced by its responsible boundary is unresolved at `invoke_constitutional_pipeline(...)`.
- Whether a broader standing vocabulary should become a universal enum is unresolved and not supported by this local pass.

## Book chapters updated

- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
- `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`
- `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md`
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `book_of_seed/concordance.md` was reviewed but not updated; no new durable top-level concordance concept was supported.

## Bounded resolution

standing topology combines inherited and consumer-local warrant

Book of Seed uptake-standing characterization pass 006 complete.
