# Book Standing and Contamination Topology 001

## Scope and negative authority

This is one bounded, report-only Book of Seed standing and contamination topology recovery on the current merged `main` after PR 1921. It creates this report only. It does not modify production code, tests, CLI behavior, events, projections, active documentation, archived documentation, or existing Book files.

This inquiry does not authorize Book edits, vocabulary purges, historical rewrites, movement of files, replacement constitutional vocabulary, universal metadata, or implementation changes. Term occurrence is not treated as active constitutional claim. Historical report is not treated as governing clause. Quoted former witness is not treated as present ownership. Deleted implementation does not mean every historical reference must disappear.

## Post-1921 corpus boundary

PR 1921 establishes three standings for this inquiry:

```text
docs/archive/original_book_of_seed/  formative historical corpus
book_of_seed/                        constitutional corpus requiring Fidelity review
current implementation               present witness
```

The original numbered corpus is historical and is not a second active canon. The current `book_of_seed/` directory is the Book territory being recovered, but placement under that directory does not itself prove current constitutional authority.

## Method

The required searches were run as candidate generators only:

```bash
find book_of_seed -type f -name '*.md' | sort
rg -n 'canonical|current|governs|amends|supersedes|corrects|replaces|withdraws|excises|historical|former witness|no longer|must not|should not' book_of_seed
rg -n 'Runtime|RuntimeLoop|RuntimeResponse|SeedAPI|Decision|DecisionProvider|DecisionContextView|context composer|context budget|PolicyDecision|PolicyGate|request_tool|call_tool|ActionPlan|HandoffPlan|PendingAction|ExecutionProposal|ExecutionAuthorization|ToolkitCandidate|seed-builder-v1|model_visible|provider execution|provider handoff|subagent|user message|free-text' book_of_seed
rg -n 'seed_runtime/[A-Za-z0-9_./-]+|scripts/seed_local\.py|--[a-z0-9-]+|[A-Za-z_][A-Za-z0-9_]*\(' book_of_seed
```

I then inspected the nearby headings, status clauses, amended-clause lists, preservation language, and current-implementation language before classifying material. The recurrent dimensional field used as orientation was subject/identity, assertion/content, standing, source/provenance, responsibility, authority/warrant, scope/locality, and occurrence/preservation. This report does not promote that field into a universal schema.

## Book tree and document families

The complete tree contains 99 Markdown files: 8 numbered chapter directories with 28 thematic chapter files and 8 chapter indexes, plus the root `README.md`, `concordance.md`, `unresolved.md`, and 60 root-level reports or records.

Recovered families:

- **Numbered chapter directories**: `01-grammar-and-standing` through `08-authority-communication-and-stopping`.
- **Active thematic chapters**: chapter files with `Constitutional subject`, `Core question`, `Bounded resolution`, distinctions, anchors, counterexamples, and related chapters.
- **Active amendments**: root records declaring canonical amendment status and naming amended clauses; some chapter files also contain embedded amendment/correction clauses.
- **Recoveries, surveys, audits, reviews, characterizations, reconciliations, topologies, corrections, cleanups, repairs, and witness slices**: mostly bounded testimony or current implementation testimony, not independent governing clauses unless they explicitly amend chapter text or concordance entries.
- **Excision/deletion reports**: historical excision records preserving what was removed and what residue remains.
- **Navigation surfaces**: root `README.md`, chapter `README.md` files, `concordance.md`, and `unresolved.md`.

## Authority and standing mechanism

The strongest current authority mechanism is **explicit but incomplete and inconsistent**:

1. The numbered chapter files present the clearest active constitutional chapter form.
2. Root amendment records with `Canonical amendment record` status and explicit amended-clause lists govern only through the clauses they amend, not as independent free-standing constitutional authority.
3. Embedded amendment/correction sections inside chapter files appear governing because they are already placed inside active chapter text.
4. The concordance indexes terms but does not reliably distinguish canonical terms from report testimony or unresolved districts.
5. Root reports may contain current testimony, corrections, or findings, but most explicitly remain report-only, bounded, or historical.

Unknown remains: the repository lacks one explicit Book-standing rule that says exactly which root reports are governing, preserved testimony, superseded, or navigational. As a result, later corrections often coexist with earlier claims rather than visibly superseding them.

## Document-standing inventory

Compact full inventory follows. `Anchors` and `contamination` are family-level summaries, not exhaustive term lists.

| path | title | primary standing | secondary standing | declared scope | authority evidence | counter-evidence | current implementation anchors | supersession relationship | contamination relevance | candidate treatment | strongest Unknown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `book_of_seed/01-grammar-and-standing/README.md` | Book I: Grammar and Standing | index / navigation | chapter index | Book I links | chapter placement | no clauses | none | ordinary navigation | none | preserve | whether index has authority beyond navigation |
| `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` | Constitutional Kinds and Artifact Standing | active constitutional chapter | amended by later view/fact clauses | artifact standing | chapter form | broad anchors are examples | dataclasses/exports generally | amended by fact/view/temporal records | guards against contamination | preserve, add standing notes later if needed | precise root-report effect |
| `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md` | Constructors and Production Authority | active constitutional chapter | amended orientation | construction vs occurrence | chapter form | implementation anchor examples | helper/constructor names | cited by amendments | low | preserve | none material |
| `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md` | External and Constitutional Grammar | active constitutional chapter | governing refusal | external grammar boundary | chapter form | provider wording may be abstract | provider/API grammar | orientation for contamination reports | high, protective | preserve | application to mixed provider metadata |
| `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md` | Lenses, Views, and Constitutional Roads | active constitutional chapter | embedded amendments | views, roads, uptake | chapter form plus embedded amendment | contains handoff word as distinction | `FactView`, views | amended by view/temporal records | medium: handoff/view grammar | preserve; later clarify view/handoff standing | whether all embedded clauses have equal force |
| `book_of_seed/02-acts-and-constraints/README.md` | Book II: Acts and Constraints | index / navigation | chapter index | Book II links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md` | Acts and Act Artifacts | active constitutional chapter | governing distinction | acts/artifacts | chapter form | anchors examples only | events/artifacts | cited by reports | low | preserve | none material |
| `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md` | Constraints, Policy, and Preconditions | active constitutional chapter | mixed contamination candidate | policy/preconditions | chapter form | title retains deleted-road terms | policy/precondition anchors | later planning excisions correct shell | high | later bounded correction | how much policy grammar remains faithful |
| `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md` | Selection Artifacts and Acts of Selection | active constitutional chapter | amended by selection reports | selection | chapter form | selection not authorization clause may be overread | selection services | cited by selection recoveries | medium | preserve; clarify ToolRecommendation pressure | recommendation standing |
| `book_of_seed/03-goals-and-advancement/README.md` | Book III: Goals and Advancement | index / navigation | chapter index | goals links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/03-goals-and-advancement/construction-and-establishment.md` | Construction and Establishment | active constitutional chapter | goal standing | goal establishment | chapter form | no detailed mixed family | goal constructors | cited by goal reports | low | preserve | relation to Session/Goal implementation |
| `book_of_seed/03-goals-and-advancement/needs-and-opened-movement.md` | Needs and Opened Movement | active constitutional chapter | embedded amendments | needs/gaps | chapter form | ToolNeed family may pressure interpretation | ToolNeed/gap | amended by sensing-gap amendment | medium | clarify ToolNeed standing | whether ToolNeed is Seed-owned need or prototype residue |
| `book_of_seed/03-goals-and-advancement/orientation-and-movement.md` | Orientation and Movement | active constitutional chapter | embedded correction | movement | chapter form | uses runtime as example/refusal | state/cache/runtime words | corrected by constrained movement reports | medium | preserve; avoid runtime purge | movement vs execution boundary |
| `book_of_seed/03-goals-and-advancement/selection-and-authorization.md` | Selection and Authorization | active constitutional chapter | contamination candidate | authorization refusal | chapter form | anchors authority binding; approval words | `operator_authority_scope_binding.py` | cited by approval/recommendation reports | high | later clarify Approval/RiskClass | approval standing |
| `book_of_seed/04-inquiry-and-examination/README.md` | Book IV: Inquiry and Examination | index / navigation | chapter index | inquiry links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md` | Examination Methods and Probes | active constitutional chapter | probe grammar | probes | chapter form | implementation probes not all constitutional | diagnostics/probes | cited by audits | low | preserve | diagnostic/report standing interaction |
| `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md` | Inquiry Frontiers | active constitutional chapter | amended by frontier clarification | frontiers | chapter form | frontier implementation partly pipeline-shaped | inquiry frontier services | corrected by frontier reports | low/medium | preserve | exact frontier authority after amendments |
| `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md` | Questions and Inquiry | active constitutional chapter | operator-expression boundary | questions | chapter form | mentions operator ask/prompt | question projection | cited by two-cycle and operator reports | medium | preserve | user/operator vocabulary boundary |
| `book_of_seed/05-evidence-and-knowledge/README.md` | Book V: Evidence and Knowledge | index / navigation | chapter index | evidence links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md` | Evidence, Provenance, and Explanation | active constitutional chapter | governing evidence | evidence/provenance | chapter form | no complete supersession map | evidence graph | amended by evidence repair | low | preserve | exact repair force |
| `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md` | Recording and Knowledge Extraction | active constitutional chapter | negative authority | recording/knowledge | chapter form | recording words may be confused with occurrence | ledger/projection | cited by operational corrections | medium | preserve | diagnostic recording boundary interaction |
| `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md` | Testimony and Established Fact | active constitutional chapter | amended fact/temporal clauses | testimony/fact | chapter form | FactView pressure | FactSupport/FactView | amended by fact/temporal/view amendments | low/medium | preserve | Fact standing producers unresolved |
| `book_of_seed/06-state-and-projection/README.md` | Book VI: State and Projection | index / navigation | chapter index | state links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/06-state-and-projection/events-facts-and-state.md` | Events, Facts, and State | active constitutional chapter | event/projection boundary | state | chapter form | may include legacy event kinds | Event/State | corrected by measurement reports | medium | preserve; mark stale anchors later | legacy events standing |
| `book_of_seed/06-state-and-projection/ownership-discrepancy-and-residue.md` | Ownership, Discrepancy, and Residue | active constitutional chapter | residue grammar | ownership/residue | chapter form | can preserve foreign subject while refusing | residue | cited by excisions | medium | preserve | whether residue is descriptive or corrective |
| `book_of_seed/06-state-and-projection/projection-and-current-state.md` | Projection and Current State | active constitutional chapter | current-state negative authority | projection/current | chapter form | current implementation anchors age quickly | State/projections | amended by view/temporal docs | low/medium | preserve | current-facing View standing |
| `book_of_seed/07-operational-realization/README.md` | Book VII: Operational Realization | index / navigation | chapter index | operational links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/07-operational-realization/execution-and-recording.md` | Execution and Recording | active constitutional chapter | active contamination candidate | execution | chapter form | title and clauses likely preserve execution ownership grammar | execution/status events | corrected by excision/measurement records | high | district correction | execution vs recording boundary |
| `book_of_seed/07-operational-realization/operational-realization-and-capability.md` | Operational Realization and Capability | active constitutional chapter | mixed capability candidate | capability | chapter form | capability/provider grammar mixed | CapabilityCatalog/recommendations | corrected by egress/planning reports | high | district correction | capability ownership boundaries |
| `book_of_seed/07-operational-realization/warrants-and-execution-proposals.md` | Warrants and Execution Proposals | active constitutional chapter | active contamination candidate | warrants/proposals | chapter form | `ExecutionProposal` deleted or excised | ExecutionProposal references | execution proposal excision | high | district correction | whether any warrant grammar survives title |
| `book_of_seed/08-authority-communication-and-stopping/README.md` | Book VIII: Authority, Communication, and Stopping | index / navigation | chapter index | authority links | chapter placement | no clauses | none | ordinary navigation | none | preserve | navigation authority |
| `book_of_seed/08-authority-communication-and-stopping/authority-scope.md` | Authority Scope | active constitutional chapter | approval/refusal boundary | authority | chapter form | Approval/RiskClass unresolved | authority binding | cited by amendments | medium | clarify Approval/RiskClass | operator authority interface |
| `book_of_seed/08-authority-communication-and-stopping/communication-and-handoff.md` | Communication and Handoff | active constitutional chapter | active contamination candidate | handoff | chapter form | handoff provider realization deleted/mixed | HandoffPlan/communication | egress recovery and planning excision | high | district correction | faithful handoff vs provider realization |
| `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md` | Refusal and Non-Performance | active constitutional chapter | corrected after conversational deletion | refusal | chapter form; deletion report says Decision anchor removed | prior refusal-as-Decision history | refusal anchors | generic conversational excision | medium | preserve; check stale clauses | remaining foreign subject disclaimers |
| `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md` | Stopping and Completion | active constitutional chapter | completion | stopping | chapter form | sparse realization grammar | Goal/Session status | cited by warrant recovery | low/medium | preserve | ExecutionStatus relation |
| `book_of_seed/README.md` | Book of Seed | index / navigation | root overview | Book layout | navigation | not enough standing labels | none | ordinary navigation | possible navigation defect | later update with standing map | whether it promotes reports |
| `book_of_seed/concordance.md` | Concordance | index / concordance / navigation | possible authority index | term index | canonical-looking index | does not consistently distinguish reports | many term anchors | amended by amendments | high navigation effect | district correction | whether inclusion canonizes |
| `book_of_seed/unresolved.md` | Cross-Cutting Unresolved Questions | unresolved question ledger | navigation | open questions | explicit `[UNRESOLVED]` | may omit superseded questions | none | ordinary citation | mixed-family pressure | preserve and later reconcile | completeness |
| `book_of_seed/claim_normalization_and_fact_standing_amendment_001.md` | Claim Normalization and Fact Standing Amendment 001 | active constitutional amendment | bounded amendment record | fact/claim | canonical amendment status | not independent authority beyond clauses | FactSupport, facts | amends chapters/concordance | low | preserve | exact supersession extent |
| `book_of_seed/temporal_standing_and_view_disclosure_amendment_001.md` | Temporal Standing and View Disclosure Amendment 001 | active constitutional amendment | bounded amendment record | temporal/view | canonical amendment status | not independent authority beyond clauses | FactView/current views | amends chapters/concordance | low/medium | preserve | all amended clauses updated? |
| `book_of_seed/view_emission_warrant_and_reliance_amendment_001.md` | View Emission, Warrant, and Reliance Amendment 001 | active constitutional amendment | bounded amendment record | view reliance | canonical amendment status | not independent authority beyond clauses | `scripts/seed_local.py` view commands | amends view/fact/authority clauses | medium | preserve | operator surface repair completion |
| `book_of_seed/sensing_gap_capability_and_learning_amendment_001.md` | Sensing, Gap, Capability, and Learning Amendment 001 | active constitutional amendment | bounded amendment record | sensing/gap/capability | amendment filename and clauses | capability family still mixed | capability/gap/sensing | amends need/capability areas | medium/high | preserve; later capability correction | ToolNeed/capability force |
| `book_of_seed/operational_measurement_baseline_and_preservation_amendment_001.md` | Operational Measurement, Baseline, and Preservation Amendment 001 | active constitutional amendment | bounded amendment record | measurement/baseline | amendment status | timing/status still mixed | diagnostics/timing/status | amends operational measurement | medium | preserve; later status correction | ExecutionStatus treatment |
| `book_of_seed/generic_conversational_application_district_excision_001.md` | Generic Conversational Application District Excision 001 | historical excision record | current residue testimony | conversational Runtime deletion | explicit PR 1912 deletion | not a chapter | deleted `RuntimeResponse`, `SeedAPI`, shell | preserves/corrects older claims | high, negative | preserve; do not cleanse | whether all active chapters reflect it |
| `book_of_seed/remaining_agent_runtime_schema_deletion_topology_001.md` | Remaining agent/runtime schema deletion topology 001 | historical excision record | current deletion topology | agent/runtime schema deletion | explicit deletion topology | not a chapter | Actor/runtime schema | corrects residual runtime claims | high | preserve | Actor standing |
| `book_of_seed/pure_foreign_planning_control_shell_excision_001.md` | Pure foreign planning/control shell excision 001 | historical excision record | current residue testimony | planning/control shell | explicit deleted list | not a chapter | ActionPlan, HandoffPlan, PolicyDecision, PendingAction | corrects planning shell claims | high | preserve | mixed survivors |
| `book_of_seed/execution_proposal_authorization_island_excision_001.md` | Execution proposal / authorization island excision 001 | historical excision record | correction testimony | proposal/authorization island | excision title/status | not chapter | ExecutionProposal/Authorization | corrects operational chapters | high | preserve | chapter title remains |
| Root recoveries/surveys/audits/reviews/reconciliations/topologies not named above | 56 root report files | historical recovery / investigation / audit or inventory record | bounded current implementation testimony where declared | local to requested pass | report titles/status/methods | root placement and present tense do not canonize | numerous anchors | ordinary citation/orientation unless explicit amendment | varies | preserve; add standing notes only later | exact edge for each report |

The row above is compact for the 56 non-amendment, non-excision root reports; the complete path list for those reports is: `active_architecture_domain_document_truth_correction_001.md`, `active_witness_and_documentation_truth_cleanup_001.md`, `advancement_need_focus_formation_recovery_001.md`, `agentic_planning_tool_prototype_contamination_recovery_001.md`, `applicability_admission_consumption_projection_001.md`, `asymmetrical_antecedent_to_first_seed_movement_review_001.md`, `attributed_operator_expression_active_road_fidelity_recovery_001.md`, `book_fidelity_repair_state_and_restrained_movement_001.md`, `bootstrap_capability_external_grammar_and_structured_communication_review_001.md`, `characterization_pass_001.md`, `claim_normalization_and_fact_standing_recovery_001.md`, `constitutional_evidence_relevance_and_competency_survey_001.md`, `constitutional_evidence_uptake_runtime_frontier_investigation_001.md`, `constitutional_grammar_contamination_reconciliation_001.md`, `constitutional_grammar_recoverability_survey_001.md`, `constitutional_occurrence_evidence_survey_007.md`, `constitutional_projection_compression_recovery_001.md`, `constitutional_view_composition_consumer_recovery_001.md`, `constitutional_view_composition_package_standing_repair_001.md`, `constrained_movement_implementation_readiness_recovery_001.md`, `constrained_movement_sensing_gap_capability_learning_correction_001.md`, `consumer_uptake_topology_pass_004.md`, `demand_establishment_boundary_review_001.md`, `evidence_and_knowledge_external_grammar_fidelity_repair_002.md`, `external_grammar_promotion_and_relation_compression_repair_001.md`, `eye_competency_composition_locality_characterization_009.md`, `focus_consideration_selection_constitutional_recovery_001.md`, `frontier_clause_testimony_to_reliance_fidelity_recovery_001.md`, `frontier_required_family_warrant_clarification_001.md`, `getting_off_null_constitutional_transition_review_001.md`, `goal_to_question_connection_survey_001.md`, `inquiry_cross_examination_warrant_reliance_reconciliation_012.md`, `mature_constitutional_grammar_review_013.md`, `operational_measurement_recording_boundary_correction_001.md`, `operational_measurement_responsibility_topology_correction_001.md`, `operational_measurement_topology_correction_001.md`, `operational_timing_and_preservation_recovery_001.md`, `operator_emission_surface_classification_and_split_recovery_001.md`, `original_numbered_seed_corpus_archival_001.md`, `post_tool_corridor_directional_topology_recovery_001.md`, `reality_exposed_demand_gap_and_baseline_review_001.md`, `realization_independence_audit_008.md`, `realization_language_compression_orientation_001.md`, `realization_language_standing_compression_bounded_search_002.md`, `realization_language_standing_compression_survey_001.md`, `repository_constitutional_dimensionality_survey_011.md`, `seed_egress_external_realization_grammar_recovery_001.md`, `selection_act_classification_recovery_001.md`, `selection_producer_recovery_001.md`, `selection_road_sufficiency_pass_003.md`, `selection_topology_pass_002.md`, `selection_warrant_observability_district_survey_001.md`, `sensing_experience_and_learning_topology_recovery_001.md`, `sqlite_constitutional_witness_slice_001.md`, `sqlite_constitutional_witness_slice_002.md`, `sqlite_seed_grammar_friction_characterization_010.md`, `temporal_standing_and_relation_recovery_001.md`, `two_cycle_constitutional_bootstrap_recovery_001.md`, `uptake_dimension_characterization_pass_005.md`, `uptake_standing_characterization_pass_006.md`, and `warrant_realization_asymmetry_fidelity_recovery_001.md`.

## Chapter-level topology

| chapter | current governing center | amendments | historical testimony | active contamination | internal contradiction | navigation defect | strongest Unknown |
|---|---|---|---|---|---|---|---|
| `01-grammar-and-standing` | standing, constructors, external grammar, lenses/views/roads | view, temporal, fact amendments | view/composition recoveries | handoff/view wording can be overread | low; generally protective | README does not list all amendments | force of embedded amendment sections |
| `02-acts-and-constraints` | act/artifact, constraints, selection | constrained movement corrections | selection/tool contamination reports | policy/precondition grammar | policy title and shell excision tension | README only thematic | faithful policy standing |
| `03-goals-and-advancement` | goal construction, needs, movement, selection/authorization | gap/capability/learning clauses | goal/need/focus recoveries | ToolNeed, authorization, movement-as-execution pressure | need/gap vs ToolNeed lifecycle | README omits amendment map | Session/Goal current standing |
| `04-inquiry-and-examination` | questions, inquiry frontiers, probes | frontier clauses | question/frontier investigations | operator/user prompt boundary | low | README omits bounded report standing | normal internal questioning scope |
| `05-evidence-and-knowledge` | testimony, facts, provenance, recording | fact, temporal, view amendments | evidence relevance/uptake reports | runtime-frontier investigation title historical | recording vs occurrence pressure | README omits amendments | current Fact producer scope |
| `06-state-and-projection` | events/facts/state, projection/current, ownership/residue | temporal/view/measurement corrections | SQLite/projection reports | legacy event/model anchors possible | projection currentness vs View amendment | README omits amendment map | legacy event standing |
| `07-operational-realization` | capability, warrants, execution/recording | measurement/capability amendments | realization audits, egress recovery | execution proposal, provider realization, capability/toolkit | high: deleted proposal/authorization/handoff districts remain in active chapter titles | README promotes chapter without warning | how to preserve realization grammar without execution corridor |
| `08-authority-communication-and-stopping` | authority scope, communication/handoff, refusal, stopping | view/temporal corrections; PR 1912 refusal cleanup | handoff/excision/recovery reports | handoff/provider, approval, Decision residue | medium/high: communication vs HandoffPlan deletion | README omits excision context | Approval/RiskClass/operator boundary |

Chapter syntheses and root reports partly agree: the chapter files preserve mature distinctions, while root reports recover corrections and deletions. They do not fully agree in navigation because the active chapter table of contents does not expose which later amendments or excisions now constrain each chapter.

## Supersession and amendment graph

| earlier document | later document | relationship | scope of correction | explicit or inferred | does earlier text still appear governing | candidate treatment |
|---|---|---|---|---|---|---|
| `01-grammar.../lenses-views-and-roads.md` | `view_emission_warrant_and_reliance_amendment_001.md` | explicit bounded amendment | View emission, warrant, reliance | explicit | yes, with embedded/recorded amendments | preserve; later add clear standing markers |
| `05-evidence.../testimony-and-established-fact.md` | `claim_normalization_and_fact_standing_amendment_001.md` | explicit bounded amendment | claim normalization and Fact standing | explicit | yes | preserve |
| `05-evidence.../testimony-and-established-fact.md` | `temporal_standing_and_view_disclosure_amendment_001.md` | explicit bounded amendment | temporal standing and disclosure | explicit | yes | preserve |
| `concordance.md` | fact/view/temporal amendments | explicit index correction | indexes added/updated | explicit | yes; indexing may still over-promote | navigation district |
| `08.../refusal-and-non-performance.md` | `generic_conversational_application_district_excision_001.md` | explicit correction by deletion testimony | refusal no longer canonizes `Decision`/`ExecutionProposalFailure` | explicit in excision report | chapter appears governing but corrected | verify/remediate stale phrases later |
| `07.../warrants-and-execution-proposals.md` | `execution_proposal_authorization_island_excision_001.md` | explicit correction/excision | proposal/authorization island | explicit from title/content | yes by title and chapter placement | correction district |
| `08.../communication-and-handoff.md` | `seed_egress_external_realization_grammar_recovery_001.md` | explicit/inferred bounded correction | HandoffPlan as legacy external-provider boundary | explicit for HandoffPlan, inferred for chapter | yes | correction district |
| `02.../constraints-policy-and-preconditions.md` | `pure_foreign_planning_control_shell_excision_001.md` | explicit correction/excision | PolicyGate/PolicyDecision/preconditions shell | explicit for implementation shell | yes | correction district |
| `03.../needs-and-opened-movement.md` | `sensing_gap_capability_and_learning_amendment_001.md` | explicit bounded amendment | need/gap/capability learning | explicit | yes | clarify ToolNeed separately |
| `07.../operational-realization-and-capability.md` | `sensing_gap_capability_and_learning_amendment_001.md` and egress recovery | bounded amendment plus recovery | capability/gap and provider realization | explicit/inferred | yes | correction district |
| historical original corpus | `original_numbered_seed_corpus_archival_001.md` | historical preservation, not supersession inside Book | formative corpus archived | explicit | no as active canon | preserve historical boundary |
| many root reports | later correction reports | ordinary citation/orientation unless status says amendment | local findings | mostly inferred | often yes | do not treat citation as supersession |

Earlier clauses that still appear governing after correction: the active chapter files in Books II, VII, and VIII whose titles and bounded resolutions still use policy, preconditions, execution proposals, execution recording, and handoff without visible chapter-level standing markers for post-excision limits.

## Active implementation-anchor recovery

| Book document | anchor | anchor type | current existence | current Fidelity standing | historical or active use | candidate treatment |
|---|---|---|---|---|---|---|
| `generic_conversational_application_district_excision_001.md` | `RuntimeResponse`, `SeedAPI`, `Runtime.handle_user_message`, HTTP/shell/free-text road | class/API/CLI/event road | deleted by report testimony | deleted present witness | historical/excision | preserve report; remove active claims elsewhere |
| `remaining_agent_runtime_schema_deletion_topology_001.md` | generic `Runtime`, agent/runtime schema | schema/service grammar | deleted or residue only | deleted present witness | excision testimony | preserve |
| `pure_foreign_planning_control_shell_excision_001.md` | `ActionPlan`, `HandoffPlan`, `PolicyDecision`, `PolicyGate`, `PendingAction`, `ToolkitCandidate`, `seed-builder-v1`, `model_visible` | models/services/fields | many deleted, some mixed survivors | deleted shell; mixed residue | excision testimony | preserve; correct active chapter pressure |
| `seed_egress_external_realization_grammar_recovery_001.md` | `HandoffPlan`, `HandoffPlanService.create_handoff_plan(...)`, `--handoff`, `backend_type`, `operation`, provider metadata | model/service/CLI/fields | live or recently live according to report | mixed/foreign realization compression | bounded recovery testimony | correction district |
| `07-operational-realization/warrants-and-execution-proposals.md` | `ExecutionProposal` grammar | domain kind/title | deleted/excised | stale active anchor if governing | active-looking chapter | correct later |
| `07-operational-realization/execution-and-recording.md` | execution/status/recording grammar | chapter claim | mixed: recording live, execution corridor deleted | mixed | active-looking chapter | correct later |
| `02-acts.../constraints-policy-and-preconditions.md` | policy/preconditions | chapter claim | mixed/deleted shell | mixed/stale | active-looking chapter | correct later |
| `03.../needs-and-opened-movement.md` | `ToolNeed`, need/gap/capability | model/service vocabulary | live mixed | unresolved | active chapter plus reports | clarify standing |
| `07.../operational-realization-and-capability.md` | CapabilityCatalog, CapabilityRecommendation, ToolRecommendationService, RecommendationRanker | service/model | live mixed | unresolved recommendation/testimony | active chapter plus reports | clarify standing |
| `08.../authority-scope.md` | Approval, RiskClass, operator authority | model/field grammar | live mixed | unresolved | active chapter | clarify standing |
| measurement amendment/corrections | `ExecutionStatus`, timing/cadence, diagnostics | model/diagnostic fields | live mixed | current testimony not baseline by itself | report/amendment | clarify status standing |
| SQLite witness slices | SQLite tables/queries | implementation witness | live if implementation keeps SQLite | bounded testimony | historical/current testimony | preserve |

Burden applied: a live target is faithful only if there is a current Seed-owned producer, constitutional act, artifact with bounded standing, and current Seed-owned consumer. Many mixed anchors fail or leave Unknowns at one of those points.

## Deleted-road contamination topology

| document | claim summary | deleted or mixed grammar involved | claim standing | current implementation evidence | later correction or amendment | historical value | correction candidate | confidence | strongest Unknown |
|---|---|---|---|---|---|---|---|---|---|
| `07-operational-realization/warrants-and-execution-proposals.md` | execution proposal vocabulary appears as active chapter subject | ExecutionProposal/authorization island | potentially active constitutional claim | deleted/excised | execution proposal excision | shows former warrant attempt | yes | high | whether title alone is treated as governing |
| `07-operational-realization/execution-and-recording.md` | execution grammar appears paired with recording | execution corridor, ExecutionStatus | active/mixed | corridor deleted; status/timing mixed | measurement corrections | preserves recording distinction | yes | high | exact faithful replacement boundary not authorized here |
| `08-authority.../communication-and-handoff.md` | handoff may read as Seed-owned egress/provider realization | HandoffPlan/provider handoff | active/mixed | HandoffPlan district reported legacy/mixed | egress recovery | preserves communication boundary | yes | high | current live callers after PR 1921 |
| `02-acts.../constraints-policy-and-preconditions.md` | policy/preconditions can read as policy-gate architecture | PolicyDecision/PolicyGate/preconditions | active/mixed | planning shell deleted | pure shell excision | preserves constraint distinction | yes | high | faithful policy terminology |
| `03.../selection-and-authorization.md` | approval/authorization may pressure execution authority | Approval/RiskClass/authorization | active/mixed | live fields possibly remain | planning/proposal excisions | preserves selection!=authorization | yes | medium | approval constitutional standing |
| `07.../operational-realization-and-capability.md` | capability/recommendation/provider wording can exceed testimony | CapabilityRecommendation/provider metadata | active/mixed | live mixed catalog services | sensing amendment and egress recovery | preserves capability testimony | yes | medium/high | which producers/consumers are faithful |
| root excision reports | deleted terms occur in tables/lists | Runtime, Decision, ActionPlan, etc. | excision testimony | documents describe deletion | themselves are corrections | essential former witness | no vocabulary purge | high | none |
| root historical recoveries/investigations | terms occur while reconstructing past roads | agent/model/runtime/user/handoff | historical recovery testimony | report-only status common | later excisions | essential evolution evidence | no purge | high | standing markers may be absent |

Active conversational/runtime grammar remaining actively canonical appears limited after PR 1912: the excision report says the refusal chapter was cleaned, but active chapter navigation and any generic `runtime` wording in movement/state/operation chapters may still be overread without standing markers. Active model-decision grammar is mostly excision testimony; `PolicyDecision` remains mixed residue rather than validated Seed architecture. Planning/policy/readiness/handoff grammar remains more visibly active in Books II, VII, and VIII.

## Mixed-family standing topology

| family | Book characterization | classification | false preservation pressure |
|---|---|---|---|
| Actor | appears in runtime/deletion topology and operator/user/model discussions | contradictory or unresolved | actor labels can preserve conversational grammar if treated as Seed owners |
| Workspace | not materially recovered in inspected standing mechanisms | not materially addressed | low, except if Session/Goal boundaries import it |
| Session | goal/stopping/status adjacency | Unknown | may import conversational lifecycle |
| Goal | active chapter subject with current implementation anchors | provisionally preserved | lower; needs producer/consumer standing |
| ToolNeed / ToolNeedStatus / ToolNeedService | need/capability lifecycle adjacent to deleted request_tool road | explicitly unresolved/mixed | high: can preserve request-tool planning road |
| ToolSpec / Toolkit | capability/tool vocabulary, model_visible residue | unresolved/mixed | high: model-facing visibility can preserve LLM tool corridor |
| Approval / RiskClass | authority and risk metadata, not execution authority by itself | provisionally preserved but unresolved | medium/high: approval can be mistaken for authority |
| CapabilityCatalog / CapabilityRecommendation / ToolRecommendationService / RecommendationRanker | capability testimony/recommendation surfaces | unresolved/mixed | high: recommendation can be mistaken for selection/provider realization |
| HandoffBackendType / backend_type / operation / provider metadata | egress recovery shows foreign realization compression | contradictory/mixed | high: external provider ownership grammar |
| `model_visible` | model-facing tool vocabulary after model-decision deletion | unresolved/mixed | high: preserves deleted LLM corridor label |
| `policy_action` | policy-routing residue | unresolved/mixed | medium/high |
| ExecutionStatus / progress/status emission / timing/cadence | operational measurement testimony, not baseline/movement by itself | provisionally preserved/mixed | medium: can recreate execution lifecycle |

This operation does not decide final implementation disposition. The false preservation pressure is strongest where active chapters use broad constitutional language around a family that excision reports classify as deleted shell or unresolved residue.

## Negative-authority analysis

Recovered genuine negative authority:

- construction is not occurrence or standing;
- selection is not authorization;
- recommendation is not selection;
- approval is not authority or execution;
- recording is not occurrence;
- projection is not truth/current fact by identity;
- provider metadata is not provider trust, execution, receipt, or realization;
- handoff construction is not external delivery;
- movement is not mutation or method call;
- diagnostic/measurement output is not cluster mutation or baseline by identity.

Negative clauses that can accidentally preserve foreign subjects: policy/precondition clauses that keep PolicyGate-shaped subject matter; handoff clauses that keep provider/backend/operation/target fields as if external realization were Seed-owned; execution-recording clauses that keep an execution lifecycle subject while refusing to execute; capability/recommendation clauses that keep provider/tool route grammar while refusing selection. These are correction candidates because foreign architecture with careful refusals is not automatically faithful constitutional artifact.

## Concordance and navigation analysis

`concordance.md`, the root `README.md`, chapter `README.md` files, and `unresolved.md` are navigation/index surfaces, not reliable authority resolvers. Defects:

- They do not consistently distinguish active chapters, canonical amendments, report-only recoveries, historical investigations, excision records, and unresolved ledgers.
- Concordance inclusion can visually promote a term without stating whether the source is a governing clause, an amendment, a recovery, or an excision record.
- Chapter indexes omit later root-level amendments/excisions that currently constrain chapter interpretation.
- `unresolved.md` lists open questions but does not by itself map superseded questions or mixed-family residue after PRs 1912-1921.
- Navigation therefore creates duplicate constitutional centers: numbered chapters appear governing, root amendments appear governing, and report conclusions can look governing when cited densely.

No navigation file is corrected here.

## Candidate correction districts

| district | root claim | governing documents | affected chapters | later corrections already present | implementation anchors | historical testimony to preserve | smallest coherent correction | prerequisites | what must not be rewritten | likely order |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Standing/navigation map | Book placement implies authority | README/concordance/chapter READMEs | all | PR 1921 boundary | none | all reports | add standing markers/navigation distinctions | none | reports/history | 1 |
| 2. Execution proposal and authorization island | active chapter still names proposal/authorization | Book VII, Book VIII | 07,08 | execution proposal excision | ExecutionProposal, ExecutionAuthorization | excision record | bounded amendment/supersession note | district 1 | excision testimony | 2 |
| 3. Planning/policy/preconditions shell | constraints/policy terms imply PolicyGate road | Book II, III, VII | 02,03,07 | pure shell excision | PolicyDecision, PolicyGate, ActionPlan | planning excision report | correct active policy/precondition clauses | district 1 | historical prototype tables | 3 |
| 4. Handoff/provider realization | handoff means provider realization | Book VIII, VII | 08,07 | egress recovery | HandoffPlan, backend_type, operation | egress recovery | distinguish communication/egress from provider realization | districts 1-3 | former witness | 4 |
| 5. Capability/tool/recommendation families | recommendation/capability becomes selection/route | Book VII, III | 07,03 | sensing amendment, generic excision | ToolNeed, ToolSpec, Toolkit, CapabilityRecommendation | capability reports | classify Seed-owned testimony vs unresolved residue | districts 1,3 | useful capability distinctions | 5 |
| 6. Approval/RiskClass | approval metadata becomes authority | Book VIII, III | 08,03 | proposal/planning excisions | Approval, RiskClass | excisions | bounded approval standing amendment | districts 2-3 | refusal clauses | 6 |
| 7. Status/timing/execution cadence | status/timing recreates execution lifecycle | Book VII, VI | 07,06 | measurement amendments | ExecutionStatus, timing diagnostics | measurement reports | clarify measurement/status testimony | district 2 | operational measurement history | 7 |
| 8. Negative disclaimers retaining foreign subjects | refusal clauses preserve the subject they deny | Books II,VII,VIII | 02,07,08 | multiple excisions | policy/handoff/execution fields | historical refusals | separate genuine negative authority from foreign subject retention | districts 2-7 | negative examples | 8 |
| 9. Supersession notes | later corrections coexist invisibly | all | all | amendments/excisions | none | superseded claims | add bounded supersession markers | district 1 | earlier clauses needed for evolution | 9 |
| 10. Historical report misuse | report conclusions used as canon | root reports | all | PR 1921 boundary | many | all historical testimony | mark reports as testimony/orientation | district 1 | reports | 10 |

## Candidate correction-order matrix

| sequence | district | root defect | documents affected | historical testimony preserved | prerequisite | why coherent | replacement prohibited |
|---|---|---|---|---|---|---|---|
| 1 | standing/navigation map | no explicit authority resolver | README, concordance, chapter READMEs, unresolved | all | none | prevents accidental canonization before clause edits | no new Book structure/ontology |
| 2 | execution proposal/authorization | active stale domain kind | Book VII/VIII clauses | proposal excision | standing map | removes deleted-road active anchor | no vocabulary purge |
| 3 | planning/policy/preconditions | deleted shell remains as active grammar | Book II/III/VII | planning excision | standing map | separates constraints from PolicyGate road | no replacement policy architecture |
| 4 | handoff/provider realization | Seed handoff confused with external realization | Book VIII/VII | egress recovery | 2-3 | provider grammar depends on planning/execution cleanup | no egress ontology |
| 5 | capability/tool/recommendation | mixed residues canonized | Book VII/III | capability histories | 3-4 | preserves useful testimony while refusing routing | no tool-corridor revival |
| 6 | approval/risk | metadata becomes authority | Book VIII/III | refusal/excision histories | 2-5 | approval depends on execution and capability boundaries | no approval engine |
| 7 | status/timing | measurement becomes execution lifecycle | Book VII/VI | measurement reports | 2 | isolates diagnostics/measurement | no operational baseline invention |
| 8 | negative disclaimers | foreign subject retained by refusal | Books II/VII/VIII | negative examples | 2-7 | cleanup after subjects are bounded | no cleansing of examples |
| 9 | supersession notes | corrections invisible | all corrected chapters | superseded claims | 1-8 | records topology without flattening history | no universal metadata mandate |
| 10 | historical report misuse | testimony read as canon | root reports/navigation | reports | 1 | finalizes standing | no historical rewrites |

## Historical testimony preservation rules

Later corrections must preserve historical recovery reports, excision reports, investigations, audits, reconciliations, quoted former witness, and superseded claims needed to understand repository evolution. Corrections may add explicit standing markers or bounded supersession notes, but should not rewrite history into apparent foresight. They must not cleanse vocabulary merely for visual consistency.

## Unknowns

- Whether a repository-level rule exists outside `book_of_seed/` that defines Book authority; this report did not alter scope to invent one.
- Whether all live implementation anchors after PR 1921 match the report testimony; this was a Book topology recovery, not a code audit.
- Whether `concordance.md` inclusion is intended as canonical recognition or navigational indexing.
- Whether active chapter titles themselves carry authority when their body has later corrections.
- Exact standing of Actor, Session, Workspace, ToolNeed, ToolSpec, Toolkit, Approval, RiskClass, provider metadata, ExecutionStatus, and timing/cadence families.
- Which historical report conclusions are being consumed operationally by future agents as active authority.

## Smallest coherent next correction

The smallest coherent next correction is not to edit contaminated terms. It is a bounded Book-standing/navigation correction that states, without inventing a new structure, which surfaces are active chapters, which are canonical amendments, which are report-only testimony, which are excision records, and how bounded amendments constrain earlier chapter clauses. That correction should update navigation/concordance standing before attempting semantic clause edits.

## Lawful stopping point

This inquiry stops at topology recovery. It does not perform Book edits, implementation edits, vocabulary deletion, canon redesign, or final disposition of mixed families. The lawful output is this single report.

## Final direct answers

1. **What currently constitutes the Book of Seed?** `book_of_seed/` is the constitutional corpus requiring Fidelity review, containing active chapters, amendments, reports, excisions, navigation, and unresolved ledgers.
2. **Does every file under `book_of_seed/` exercise constitutional authority?** No.
3. **What document families exist inside the Book?** Numbered chapters, canonical thematic chapters, amendments, recoveries, investigations, characterizations, reconciliations, audits, surveys, topologies, excision reports, corrections, operational slices, inventories, concordance/indexes, unresolved ledgers, historical summaries, and implementation-specific reports.
4. **What makes a Book document canonical or governing today?** Strongest evidence is numbered chapter placement with chapter form, explicit canonical amendment status, or embedded amendment text inside a chapter.
5. **Is that authority mechanism explicit, implicit, inconsistent, or Unknown?** Explicit in places, implicit and inconsistent overall.
6. **Which files are active constitutional chapters?** The 28 non-README files inside numbered chapter directories.
7. **Which files are active amendments?** `claim_normalization_and_fact_standing_amendment_001.md`, `temporal_standing_and_view_disclosure_amendment_001.md`, `view_emission_warrant_and_reliance_amendment_001.md`, `sensing_gap_capability_and_learning_amendment_001.md`, and `operational_measurement_baseline_and_preservation_amendment_001.md`, plus embedded amendment/correction sections in chapter files.
8. **Which files are historical recovery or investigation testimony?** Root files named `*_recovery_*.md` or `*_investigation_*.md`, subject to local status; examples include agentic planning, temporal standing, frontier reliance, egress grammar, and runtime frontier investigations.
9. **Which files are excision records?** `generic_conversational_application_district_excision_001.md`, `remaining_agent_runtime_schema_deletion_topology_001.md`, `pure_foreign_planning_control_shell_excision_001.md`, and `execution_proposal_authorization_island_excision_001.md`.
10. **Which files are mixed or Unknown?** Several root reports without explicit amendment/excision status, witness slices, orientations, bounded searches, and current-testimony reports are mixed or Unknown; see inventory.
11. **How are amendments and corrections currently represented?** As root amendment records, embedded chapter clauses, correction reports, and concordance updates.
12. **Do later corrections actually supersede earlier clauses?** Sometimes boundedly; often they coexist without visible complete supersession.
13. **Which earlier clauses still appear governing after correction?** Books II, VII, and VIII clauses around policy/preconditions, execution proposals, execution/recording, handoff, capability, and authorization.
14. **Where does deleted conversational/runtime grammar remain actively canonical?** Mostly not active after PR 1912, but generic runtime words in state/movement/operation areas require standing markers to prevent overreading.
15. **Where does deleted model-decision grammar remain actively canonical?** Universal `Decision` appears primarily historical/excision; `PolicyDecision` remains mixed residue in policy districts.
16. **Where does deleted planning/policy/readiness/handoff grammar remain actively canonical?** Books II, VII, and VIII, especially constraints-policy-preconditions, execution proposals, operational realization, and communication-handoff.
17. **Where does provider-realization or execution grammar remain actively canonical?** Book VII operational realization/execution chapters and Book VIII communication-handoff.
18. **Which occurrences are honest historical testimony and must remain?** Excision reports, recoveries, investigations, audits, reconciliations, quoted former witness, and superseded claims preserving evolution.
19. **Which negative disclaimers preserve foreign architecture instead of removing it?** Policy/precondition, handoff/provider/backend/operation, execution-recording, and capability/recommendation refusals when they retain the foreign subject as Seed-owned.
20. **Which active implementation anchors point to deleted artifacts?** ExecutionProposal, ExecutionAuthorization island, generic Runtime/RuntimeResponse/SeedAPI, ActionPlan shell, PolicyGate/PolicyDecision shell parts, PendingAction/tool-call road, ToolkitCandidate/builder lifecycle, and generic HTTP/shell free-text road.
21. **Which active anchors point to live but unresolved mixed artifacts?** ToolNeed, ToolSpec, Toolkit, Approval, RiskClass, CapabilityCatalog, CapabilityRecommendation, RecommendationRanker, Handoff metadata, provider metadata, ExecutionStatus, timing/cadence.
22. **How does the Book characterize Actor?** Unresolved/mixed, mostly in runtime/agent/operator/model residue rather than clean active constitutional ownership.
23. **How does the Book characterize ToolNeed?** Need/capability testimony adjacent to deleted request-tool planning road; unresolved mixed family.
24. **How does the Book characterize ToolSpec and Toolkit?** Capability/tool metadata with `model_visible` residue; unresolved mixed family.
25. **How does the Book characterize Approval and RiskClass?** Risk/approval metadata and refusal distinctions, not execution authority by itself; unresolved/provisionally preserved.
26. **How does the Book characterize capability/provider recommendations?** Useful testimony/recommendation surfaces that must not be equated with selection, provider trust, or realization; mixed.
27. **How does the Book characterize ExecutionStatus and timing?** Operational measurement/status testimony, not baseline, movement, or execution lifecycle by identity; mixed.
28. **Which chapters contain internal contradictions?** Most visible contradictions are Books II, VII, and VIII; Books III and VI have mixed-family tensions.
29. **Does the concordance accurately reflect governing standing?** Not reliably.
30. **Does `unresolved.md` distinguish open questions from superseded questions?** Not sufficiently.
31. **Are historical reports being used as active authority?** They can be visually used that way because navigation lacks standing markers; this report does not prove specific operational reliance.
32. **What coherent correction districts are visible?** Standing/navigation, execution proposal/authorization, planning/policy/preconditions, handoff/provider realization, capability/tool/recommendation, approval/risk, status/timing, foreign-subject disclaimers, supersession notes, and historical-report misuse.
33. **In what order should those districts later be corrected?** Navigation/standing first, then execution proposal, planning/policy, handoff/provider, capability/tool, approval/risk, status/timing, negative disclaimers, supersession notes, and historical-report misuse.
34. **What is the smallest coherent next correction?** Add bounded standing/navigation and supersession markers; do not edit vocabulary first.
35. **What historical testimony must that correction preserve?** All recovery, excision, investigation, audit, reconciliation, quoted former witness, and superseded-evolution testimony.
36. **Does the Book require a new structure before correction?** No.
37. **Does the Book require a vocabulary purge?** No.
38. **Was any existing Book file modified?** No; only this new report was created.
39. **What are the strongest remaining Unknowns?** Authority mechanism completeness, concordance force, live implementation fidelity of mixed anchors, and final standings of Actor/Session/Workspace/ToolNeed/ToolSpec/Toolkit/Approval/RiskClass/provider metadata/ExecutionStatus.
40. **Where must this inquiry stop?** At report-only topology recovery, before Book edits, code edits, replacement architecture, or final mixed-family disposition.
