# Uptake-Dimension Characterization Pass 005

## Repository state examined

- `git rev-parse HEAD`: `f9b2516cbe28298adef330df70087f34074acc60`.
- `git status --short`: empty before this pass changed Book files.
- PR 1746 is present as `f9b2516 Add consumer uptake topology pass (#1746)`.
- `book_of_seed/consumer_uptake_topology_pass_004.md` exists and was treated as testimony, not controlling implementation evidence.

## Primary relationships compared

This pass reused the Pass 004 relationships without expanding into a repository-wide inventory:

1. Relationship A: `SelectedConstitutionalViews` -> `selected_constitutional_views_to_composition_request(...)` -> `ConstitutionalViewCompositionRequest` -> `build_constitutional_view_composition(...)`.
2. Relationship B: `AdvancementNeedConsiderationSelection` -> `preserve_inquiry_frontier_boundary_testimony(...)` -> `InquiryFrontierBoundaryTestimony`.
3. Relationship C: `AdvancementNeedConsiderationSelection` + `InquiryFrontierBoundaryTestimony` -> `assemble_bounded_inquiry_frontier(...)` -> `BoundedInquiryFrontier`.
4. Relationship D: `ConstitutionalPipelineResult` -> `explain_constitutional_pipeline_provenance(...)` -> `ConstitutionalPipelineProvenanceExplanation`.

## Per-relationship dimensional matrix

| Relationship | upstream assertion relation | consumer constraints | consumer act | consumer assertion | standing effect | handoff structure | producer occurrence proved? |
|---|---|---|---|---|---|---|---|
| A | The adapter treats `SelectedConstitutionalViews.selected_view_names` as selected values and narrows the artifact to a request. Composition consumes the resulting request as explicit registered view names, not as proof that the selection act occurred. | Registration and buildability are enforced by `build_constitutional_view_composition(...)`; the adapter itself performs no identity or lineage validation. The constraint belongs to composition's act, not to the adapter's value transport. | Request formation by the adapter, followed by read-only composition of explicitly requested registered views. | The request asserts these registered view names are requested for this composition purpose; the composition artifact asserts a bounded explanation composed from registered views. It re-expresses selected names for a new purpose and does not preserve the full selection assertion. | Consumer request and composition artifact receive standing when produced by their responsible constructors/consumer. Upstream selection standing is not newly established. | Selected fields -> typed request -> composition artifact. | No. Direct construction of a request can bypass the selection producer. |
| B | The selected inquiry reference is adopted only for selected-subject standing when selection state, selected reference, and inquiry family agree; otherwise no selected inquiry subject is preserved. Boundary clauses are treated as testimony with ownership/lineage classifications. | Standing check on selected state, selected reference presence, and inquiry family. Clause ownership is classified from producer or adapter lineage, but not fully re-proven. | Testimony preservation and selected-standing preservation for frontier-boundary use. | The testimony asserts that boundary clauses and selected-inquiry identifiers were preserved for one exact selected inquiry need under the frontier-testimony purpose. It depends on the selected reference as testimony and selected standing. | Testimony receives standing as preserved testimony. The selected subject is referenced/preserved, not re-established. | Full selected artifact plus clause inputs; selected identity fields, native lineage snapshot, visible evidence refs, and testimony bundle cross into the testimony artifact. | No. It does not independently prove the original focus evidence or selection act. |
| C | The assembler consumes selected need and testimony as independently supplied artifacts and compares their identities/lineage. It does not adopt testimony alone and does not re-establish the selected need. | Identity matching, lineage matching, standing checks, required clause-family sufficiency, operative coherence, and conflict refusal. These are consumer constraints governing frontier assembly. | Sufficiency judgment and establishment of a bounded inquiry frontier when constraints hold; refusal states otherwise. | The frontier asserts that this selected inquiry need has an established, missing, conflicting, or not-selected frontier state under supplied testimony. When established, the subject is a new downstream frontier, not the upstream selected need or testimony. | New downstream subject receives standing only when frontier state is established. Testimony and selected need retain their own prior standing. | Multiple independently supplied artifacts: selected artifact plus testimony bundle with identity references and lineage snapshot. | No. Coherence success validates agreement for the frontier boundary; it does not re-run or prove upstream producers. |
| D | The explanation reads preserved stage artifacts and their fields as source material. It adopts values for an explanation, but does not adopt every stage assertion as newly established truth. | Result shape and artifact availability; matched-key reconstruction; read-only, event-ledger, and mutation flags are aggregated from stage artifacts. No independent verification, semantic matching, persistence, or mutation occurs. | Explanation construction/projection over one completed pipeline result. | The explanation asserts why the completed result selected these views, what was unsupported or unknown, and which contributors/unknowns/refusals were present. It is a consumer-local explanation assertion. | Explanation artifact receives standing as an explanation if produced by the function. Upstream stages are not re-established. | Full completed pipeline result; selected fields from each stage; identity references and stage flag aggregation. | No. The function explains existing artifacts and explicitly does not perform stages or verification. |

## Concepts that combine within one boundary

- Relationship A combines assertion narrowing, typed request handoff, request formation, and later registration/buildability constraints. That combination shows that handoff representation, relationship-to-upstream-material, consumer act, and consumer constraint are not sibling kinds.
- Relationship B combines partial assertion adoption for selected-subject standing, purpose-limited testimony preservation, and standing checks.
- Relationship C combines coherence revalidation, sufficiency judgment, conflict refusal, and new downstream establishment in one consumer boundary.
- Relationship D combines value adoption for explanation, projection/explanation construction, and a new explanation assertion without re-establishing upstream stages.

## Relationship modes supported

Repository evidence supports these relationship modes in the bounded survey:

- assertion adoption for a declared purpose, as in selected inquiry standing preserved into boundary testimony;
- assertion narrowing, as in selected view names narrowed into a composition request;
- testimony-dependent use, as in frontier assembly depending on boundary testimony;
- value use for explanation, as in provenance explanation reading stage artifacts;
- non-uptake value transport, where the adapter merely constructs a typed request before a consumer gives that request constitutional use.

## Consumer constraints supported

Supported constraints include registration, buildability, identity matching, lineage matching, selected-state standing checks, family applicability, operative sufficiency, conflict refusal, and purpose limitation. These constraints govern consumer acts. They are not themselves consumer acts, standing effects, handoff structures, or proof that upstream producer occurrences happened.

## Consumer acts supported

Supported acts include request formation, composition, testimony preservation, selected-standing preservation, sufficiency judgment, new downstream subject establishment, and explanation construction/projection. Ordinary dataclass construction or field reading is not enough to classify an act without an assertion-bearing boundary.

## Standing effects supported

Supported standing effects include consumer request standing, testimony standing, new downstream frontier standing, and explanation standing. The evidence does not show re-standing of the upstream selected need, re-standing of all pipeline stages, or general standing for typed values merely because an adapter transported them.

## Handoff structures supported

Supported handoff structures include selected fields, typed requests, identity references, lineage snapshots, testimony bundles, full upstream artifacts, and multiple independently supplied artifacts. Handoff structure is representation, not constitutional relationship by itself.

## Constitutional-uptake boundary result

The bounded evidence supports the hypothesis with a refinement: constitutional uptake occurs when a consumer gives upstream material bounded constitutional use or standing, or makes an assertion whose warrant materially depends on that material. Reading fields, passing typed values, or building a typed request is not automatically uptake. In Relationship A, the adapter participates in the larger boundary, but uptake resides where the request is used by composition under registration/buildability constraints and where the resulting assertion depends on the requested view names. In Relationship B, uptake resides in purpose-limited preservation of selected inquiry standing into testimony. In Relationship C, uptake resides in the assembler's identity/lineage/sufficiency use of selected need and testimony to establish or refuse a frontier. In Relationship D, uptake resides in the explanation function's source-dependent explanation assertion.

## Constitutional-road definition result

The current definition is retained with dimensional clarification: a constitutional road is assertion-preserving uptake in which a consumer relies on a producer assertion for a declared purpose and validates the identities and invariants material to that use. Assertion adoption is the relationship mode that can define roads. Constraints such as registration, buildability, identity matching, and sufficiency remain separate dimensions that may be required for local road sufficiency. Consumer acts such as composition or explanation construction do not become roads unless they preserve an upstream assertion under bounded validation.

## Re-establishment terminology result

`re-establishment` is demoted and removed as a top-level concordance entry. Relationship C establishes a new `BoundedInquiryFrontier`; it does not establish the selected need or testimony again. The existing term `establishment` is sufficient when paired with `new downstream subject` or `consumer-local/downstream frontier` in prose. No new durable top-level term is required.

## Explanation-projection classification result

`explanation projection` is demoted from top-level durable concordance status. The implemented responsibility is best classified as an explanation-construction/projection act that produces a consumer-local explanation assertion from one completed pipeline result. It may be described in chapter prose, but the dedicated function and dataclass do not prove a distinct constitutional uptake kind.

## Concordance entries retained

Retained entries relevant to this pass:

- `constitutional road`;
- `constitutional uptake`;
- `lens`;
- `artifact`;
- `act`;
- `constraint`;
- `handoff`;
- `testimony`;
- `evidence`.

## Concordance entries removed or demoted

Removed as top-level concordance entries because they name dimensions, implementation behaviors, or purpose-bound effects rather than durable sibling constitutional kinds:

- `assertion narrowing`;
- `coherence revalidation`;
- `re-establishment`;
- `explanation projection`;
- `typed request handoff`.

These phrases may still appear in Book prose where they describe a relationship mode, constraint, act, or handoff structure.

## Claims contradicted

- The claim that all Pass 004 uptake terms are distinct sibling constitutional kinds is contradicted by Relationships A, C, and D, where several terms combine inside one boundary.
- The claim that typed request handoff is constitutional uptake by itself is contradicted by Relationship A's adapter, which forwards selected names without validating producer occurrence.
- The claim that coherence validation re-proves the upstream assertion is contradicted by Relationship C, where identity/lineage comparison is only a frontier-assembly constraint.
- The claim that Relationship C performs re-establishment of the same subject is contradicted because it establishes a new `BoundedInquiryFrontier` subject.
- The claim that explanation projection is durable merely because it has a dedicated dataclass and function is contradicted by Relationship D's bounded reporting/explanation responsibility.

## Claims remaining unresolved

- `[UNRESOLVED]` Whether other repository relationships support additional relationship modes outside these four bounded relationships.
- `[UNRESOLVED]` Whether explanation construction should eventually have subfamilies beyond the pipeline provenance explanation.
- `[UNRESOLVED]` Whether every adapter in the repository only transports values or whether some adapters own an assertion-bearing uptake boundary.
- `[UNRESOLVED]` Which other implemented producer-consumer pairs satisfy constitutional-road sufficiency.

## Book chapters updated

- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`: revised constitutional uptake as dimensional grammar and clarified constitutional roads as the assertion-preserving subfamily.
- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`: clarified that relationship modes, acts, constraints, handoff structures, and standing effects are not automatically durable kinds.
- `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`: replaced re-establishment phrasing with new downstream establishment and separated consumer acts from constraints.
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`: demoted explanation projection to an explanation-construction/projection act rather than a durable uptake kind.
- `book_of_seed/08-authority-communication-and-stopping/communication-and-handoff.md`: clarified typed request handoff and adapter participation as representation/transport unless a consumer gives bounded constitutional use.
- `book_of_seed/concordance.md`: removed premature top-level entries for assertion narrowing, coherence revalidation, re-establishment, explanation projection, and typed request handoff.

## Bounded resolution

uptake topology contains both kinds and orthogonal dimensions

Book of Seed uptake-dimension characterization pass 005 complete.
