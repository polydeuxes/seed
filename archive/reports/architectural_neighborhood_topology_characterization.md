# Architectural Neighborhood Topology Characterization

## Status

This is a characterization of implementation-backed adjacency among already recovered neighborhoods. It does not recover new architecture, introduce districts, layers, phases, engines, pipelines, or a universal city model.

Repository authority wins. Prose from prior reports is used only where it points back to implementation, tests, or app surfaces.

## Evidence reviewed

Primary evidence reviewed:

- `representation_transformation_discipline_investigation.md`, especially the implementation evidence list, producer/consumer relationships, recurring transitions, and preserved/removed information matrix.
- `question_bounded_work_invocation_investigation.md`, especially the bounded ask path, responsibility characterization, counterexamples, and supported/unsupported conclusions.
- `bounded_inquiry_recovery_characterization.md`, especially app-surface commands and reductions from broad possibility to bounded repository questions.
- `pressure_audit_smallest_owner_investigation.md`, especially repeated pressure builder sequence and pressure-row assembly.
- `pressure_visibility_evidence_classification_boundary_investigation.md`, especially the pressure evidence/classification boundary and its methodology-vs-implementation limit.
- `constitutional_interpretation_characterization.md`, especially observation-to-fact, candidate-to-readiness-supported, observation-agreement-to-grammar-observation, and bounded interpretation stops.
- `docs/implementation_relationship_grammar_investigation.md`, especially relationship inventory, relationship matrix, producer/consumer tables, subsystem relationship graph, implicit relationship findings, and negative limits.
- Implementation files listed by those reports, including `seed_runtime/observations.py`, `seed_runtime/evidence.py`, `seed_runtime/facts.py`, `seed_runtime/state.py`, `seed_runtime/explanations.py`, `seed_runtime/context.py`, `seed_runtime/inquiry_orientation.py`, `seed_runtime/operational_story.py`, `seed_runtime/question_surface_inventory.py`, `seed_runtime/diagnostic_inventory.py`, `seed_runtime/diagnostic_shape_audit.py`, and `scripts/seed_local.py`.

Commands used in this investigation:

```bash
pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' -g '!__pycache__' | sort && git status --short
cat AGENTS.md && git status --short && rg -n "Observation|Possible Observation|Inquiry Orientation|Pressure Evidence|Responsibility Evaluation|Question Family|Question Surface Inventory|Bounded Inquiry|Bounded Ask|Supporting Evidence|Answer Composition|Diagnostic Inventory|Diagnostic Shape Audit|Grammar Observation|Observation Agreement|Provider Translation|Transition Families|Implementation Readiness|Local Recovery|Constitutional Recovery|Candidate|Admission" -S .
rg --files | sed -n '1,200p'
rg -n "diagnostic_inventory|diagnostic-shape-audit|QuestionFamily|BoundedAsk|Admission|Candidate|PressureItem|SupportingEvidence|Reason|Answer Composition|ObservationAgreement|GrammarObservation|provider translation|implementation readiness|constitutional recovery|local recovery" seed_runtime tests docs *.md -S
sed -n '1,220p' representation_transformation_discipline_investigation.md
sed -n '1,180p' constitutional_interpretation_characterization.md
sed -n '1,170p' docs/implementation_relationship_grammar_investigation.md
sed -n '1,180p' question_bounded_work_invocation_investigation.md
sed -n '1,160p' bounded_inquiry_recovery_characterization.md
sed -n '180,360p' question_bounded_work_invocation_investigation.md
sed -n '1,180p' pressure_audit_smallest_owner_investigation.md
sed -n '1,150p' pressure_visibility_evidence_classification_boundary_investigation.md
sed -n '1,140p' docs/implementation_relationship_grammar_investigation.md
```

## Neighborhood survey

| Neighborhood | Constitutional / local purpose currently earned | Immediate implementation-backed neighbors | Relationship type | Methodological-only neighbors | Explicitly rejected neighbors / ownership refusals | Relative position | Preserves / consumes / produces / observes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Observation | Canonical observed claim shape and ingestion-facing boundary. | Provider/source-local records, Evidence, Fact, State projection. | Source adapters produce observations; ingestor produces evidence and optional facts; projector replays observation events. | Broad “observation execution” vocabulary is weaker than source/adaptation/ingestion. | Observation does not automatically become fact; source adapters do not own ledger/projection internals. | After provider/source records; before Evidence/Fact/State. | Preserves observed subject/predicate/value/provenance; produces evidence/fact events through ingestion. |
| Possible Observation | Candidate or not-yet-promoted observation possibility. | Candidate Request, Bounded Inquiry, Provider Translation, Observation Source gaps. | Mostly implementation-adjacent when candidate requests or adapter gaps preserve possible meanings before routing/promotion. | Strongly methodological in many reports. | Does not become knowledge, fact, routing, or architecture without implemented evidence. | Before Observation or Inquiry; often independent. | Preserves possibility; observes gaps; rarely produces canonical output directly. |
| Inquiry Orientation | Read-only orientation from inquiry note plus projected state matches. | State, FactSupport, RelatedMaterial, Answer Composition, Rendering. | `build_inquiry_orientation` collects evidence, composes answer/reason/support/boundary/limitations, then formats. | Orientation as a broad constitutional movement remains methodological unless tied to this surface. | Rejects semantic intent, planning, routing, ownership, importance, action recommendations, and mutation. | Beside projected state and answer composition; after inquiry note preservation. | Consumes State/note; produces orientation view; observes related material. |
| Pressure | Ranking/visibility of current repository operational pressure. | Existing audits, Pressure Evidence, Pressure Classification, Candidate/Selection Path, Operational Story. | Pressure audit reads audit surfaces, scores positive rows, emits pressure items. | Methodological pressure characterization is broader than current implementation. | Pressure does not authorize recovery, ranking beyond local row score, planning, implementation, or mutation. | After audit evidence; before selection/operational explanation. | Consumes audit outputs; produces pressure items; preserves reasons/evidence. |
| Pressure Evidence | Material supporting or limiting pressure claims. | Pressure, Pressure Classification, Diagnostic rows, Unknowns. | Evidence fields in read-only diagnostics and pressure rows. | Evidence/classification split is characterized as methodology/reporting, not a recovered implementation owner. | Evidence alone does not classify, prioritize, or authorize a slice. | Before classification; beside Pressure. | Preserves material and provenance. |
| Responsibility | Naming an owner, answer responsibility, or local boundary. | Question Family, Diagnostic Inventory, Implementation Trait, Responsibility Evaluation, Answer Composition. | Inventory rows and relationship grammar expose `answer_responsibility`, owner/boundary fields, and consumers. | Responsibility recovery as a family is documented across reports. | No universal responsibility graph; distributed across surfaces. | Beside most surfaces; often before evaluation. | Observes and names ownership; preserves boundaries. |
| Responsibility Evaluation | Determining whether candidate responsibility is supported. | Responsibility, Evidence, Pressure Classification, Implementation Readiness. | Implemented indirectly through reports/tests rather than one runtime evaluator. | Mostly methodological. | Does not promote merely because vocabulary recurs. | After evidence; before recovery/readiness. | Consumes evidence; produces bounded status/stop. |
| Question Family | Exact registered bounded question identity. | Question Surface Inventory, Bounded Ask, Answer Surface, Diagnostic Inventory. | Inventory rows register family/surface/responsibility/boundary and bounded status. | Free-form question understanding is not implementation-backed. | Unknown families and free-text ask routing are rejected; family membership does not imply executable ask. | Before bounded ask; beside diagnostic visibility. | Preserves known question identity; produces inventory rows/status. |
| Question Surface Inventory | Static read-only registry of question family relationships. | Question Family, Bounded Ask, Diagnostic Inventory, Diagnostic Shape Audit. | Builds rows, maps diagnostic relationship, exposes bounded ask findings. | None needed for its current role. | Does not execute diagnostics or dispatch arbitrary questions. | Before bounded ask and question explanations. | Produces registry rows; observes static implementation maps. |
| Bounded Inquiry | Reduction of broad possibility to bounded repository investigation. | Question Family, Bounded Ask, Inquiry Artifacts, Implementation Readiness. | App surfaces expose inventory, artifacts, definitions, and explanations; reports reduce broad questions. | Mostly recovery methodology, not a runtime planner. | No universal promoter, no workflow engine, no automatic implementation authority. | Before bounded ask or recovery decisions. | Consumes possibility/pressure; produces bounded question. |
| Bounded Ask | Exact `ask --question-family` compatibility path to existing surfaces. | Question Family, Required Args, Dispatch, Answer Surface. | `bounded_status_for_question_family`, dispatch maps, required arg maps, CLI helper, tests. | None for the narrow CLI behavior. | Not a generic router, semantic classifier, planner, or universal dispatcher. | After Question Family; before selected direct surface. | Consumes registered family/args; produces CLI namespace mutation to an existing surface. |
| Dispatch | Existing-surface selection after eligibility. | Bounded Ask, Answer Surface, Rendering. | CLI helper sets direct surface flag; direct surface branch executes. | Broader dispatch vocabulary unsupported. | Dispatch != answer composition; dispatch != execution engine. | After eligibility; before surface-local build/format. | Consumes eligibility; delegates to surface. |
| Evidence | Provenance/source payload representation. | Observation, Fact, FactSupport, Explanation, Reasoning Path. | Observation ingestion and tool extraction produce evidence; state/explanations consume evidence ids. | “Evidence” as every support material is broader in reports. | Evidence does not necessarily produce fact; generic tool extraction intentionally does not infer facts. | After observation/tool event; before fact support/explanation. | Preserves provenance; supports claims. |
| Supporting Evidence | Bounded support payload for answer or selection. | Evidence, Reason, Answer Composition, Operational Story, Selection Path. | Operational story and selection/reasoning audits expose supporting evidence separately from reason/outcome. | Some answer-like surfaces are only surface-specific. | Supporting Evidence != Boundary; Reason != Supporting Evidence. | Beside reason; before answer handoff. | Preserves support; does not own conclusion. |
| Reason | Local explanation of why a bounded outcome/answer follows. | Supporting Evidence, Answer Composition, Selection/Reasoning Path. | Operational story payloads and selection path payloads separate reason from evidence/outcome. | General reasoning engine unsupported. | Reason does not own raw support, evidence acquisition, or mutation. | Between support and final answer/output. | Consumes support; produces explanation text/fields. |
| Answer Composition | Surface-local assembly of bounded answer, reason, support, boundary, limitations. | Supporting Evidence, Reason, Boundary, Rendering, Question Family. | Operational Story, Inquiry Orientation, question-family explanation, ExplanationBuilder. | Not every answer-like surface proves the same boundary. | Answer Composition != Rendering; does not create truth or execute operations. | After evidence collection; before JSON/formatter. | Consumes support/reason/boundary; produces view/object. |
| Compatibility | Preserving public behavior while local boundaries are separated. | Dispatch, Answer Composition, Existing CLI surfaces, Public dataclasses. | Bounded ask maps to existing direct surfaces; slice reports keep public objects stable while adding private payloads. | Compatibility as a global law is broader than evidence. | Compatibility does not justify new machinery. | Between recovered boundary and public output. | Preserves external shape. |
| Projection | Event-ledger to projected State/read models. | Observation/Evidence/Fact events, State, FactSupport, Explanation, Diagnostic consumers. | StateProjector applies events and finalizes derived supports, relationships, conflicts. | Projection as constitutional metaphor unsupported beyond implemented projection. | Projection does not rewrite event ledger; projected state is not universal architecture. | After events; before views/audits/explanations. | Consumes events/facts; produces State/support/read models. |
| Candidate | Possible status before admission/verification/selection. | Admission, Verification Evidence, Selection Path, Candidate Request. | Candidate capability/readiness and selection path preserve candidates and non-selected alternatives. | Candidate as generic philosophical status is broader. | Candidate != verified, selected, command, capability, execution decision, or truth. | Before Admission/Selection/Verification. | Preserves possibility and alternatives. |
| Admission | Local rule allowing candidate to enter stronger status. | Candidate, Evidence, Verification/Readiness, Implementation Readiness. | Candidate-to-verified/readiness-supported paths are evidence-gated and family-local. | Mostly methodological except specific capability/readiness surfaces. | No universal admission owner or promoter. | After candidate evidence; before verified/supported state. | Consumes evidence; produces permitted status or refusal. |
| Diagnostic Inventory | Registry of diagnostic/operational surfaces and record/mutation/source contracts. | Diagnostic Shape Audit, Question Surface Inventory, Projected Consumers. | Declares source use, JSON/record support, record scope, event-ledger and cluster mutation boundaries. | None for current registry behavior. | Inventory declares; it does not itself validate all implementation shape. | Before Shape Audit; beside question inventory. | Produces declarations; preserves operational contracts. |
| Diagnostic Shape Audit | Declared-vs-observed/static spec checker for diagnostic shapes. | Diagnostic Inventory, Implementation Specs, Tests. | Consumes diagnostic declarations/specs and reports consistency/warnings/mismatches. | None for current audit. | Shape audit does not execute every target surface as a semantic authority. | After Diagnostic Inventory. | Consumes declarations/specs; produces audit rows. |
| Grammar Observation | Recurrence observation over agreement shapes, not semantic truth. | Observation Agreement, Relationship/Grammar evidence, Candidate agreement. | Emits recurring relation-shape observations only after repeated agreement shape. | Grammar as architecture is not promoted. | Rejects semantic interpretation and architectural truth. | After candidate agreement. | Observes recurrence; preserves shape, not truth. |
| Observation Agreement | Candidate agreement between independent streams. | Evidence streams, Grammar Observation. | Emits candidate agreement when supplied streams share exact evidence equality. | Broader agreement methodology remains outside implementation. | Candidate agreement is not semantic/architectural truth. | Before Grammar Observation. | Observes equality; produces candidate agreement. |
| Provider Translation | Adapting provider/source-native representation to Seed representation. | Provider-native payloads, Source adapters, Observation, Provider contract gaps. | Some adapters decode into observations or structural records; not uniformly staged. | Provider language contract recovery is only partially supported. | Provider translation does not own observation truth, facts, or capability verification. | Before Observation; sometimes compressed with source adapter. | Consumes provider-native payloads; produces observations/records. |
| Transition Families | Local movement types with different authority changes. | Observation→Evidence→Fact, Candidate→Admission, Question→Bounded Ask, Inventory→Shape Audit. | Reports and implementation show several distinct transitions. | A universal transition model is methodological/unsupported. | No one generic constitutional movement. | Cross-cutting; family-local. | Characterizes changes; does not merge them. |
| Implementation Readiness | Evidence-gated permission to implement smallest behavior-preserving change. | Pressure, Responsibility Evaluation, Admission, Tests. | Characterized by convergence of boundary, owner/corridor, necessity, small change, preservation surface. | Mostly methodology, except tests/app surfaces can prove readiness conditions. | Recurrence, vocabulary, pressure, or excitement alone do not authorize implementation. | After recovery/evaluation; before code change. | Consumes evidence; produces readiness/refusal. |
| Local Recovery | Recovering implementation-local owner/boundary. | Pressure Evidence, Responsibility Evaluation, Compatibility, Tests. | Slice reports recover local owners from concrete code/tests. | Broader recovery doctrine methodological. | Does not imply constitutional architecture. | After evidence/classification; before/within implementation slice. | Consumes local evidence; produces bounded owner or stop. |
| Constitutional Recovery | Naming higher-level recurring law only when repeatedly supported. | Local Recovery, Transition Families, Negative Authority, Methodology. | Reports cautiously characterize constitutional interpretation/promotion limits. | Frequently methodological; not runtime implementation. | No universal graph, flow, promoter, or architecture family. | After repeated local recoveries. | Observes recurrence; preserves limits. |

## Street survey

Implementation-backed recurring streets currently earned:

1. **Provider/source-local representation ↔ Observation**
   - Repeats through source adapters and observation sources.
   - Often compressed: provider decoding, identity choice, predicate choice, and observation construction are not uniformly staged.

2. **Observation ↔ Evidence**
   - Strong direct street through `ObservationIngestor.observation_to_evidence(...)`.
   - Preserves provenance/source payload; does not create current truth by itself.

3. **Observation + Evidence ↔ Fact**
   - Strong but conditional street through `ObservationIngestor.observation_to_fact(...)`.
   - Fact promotion may be suppressed; therefore the street is not mandatory for every observation.

4. **Fact ↔ FactSupport / Supporting Evidence**
   - Strong projection street through fact support projection and support-consuming views.
   - It aggregates support and intentionally collapses some measurements to current samples.

5. **Supporting Evidence ↔ Reason**
   - Strong in answer-composition surfaces with separate support and reasoning payloads.
   - Not proven as a universal answer surface pattern.

6. **Reason ↔ Answer Composition**
   - Strong in Operational Story, Inquiry Orientation, question-family explanation, and representative selection/reasoning outputs.
   - Terminates at view/object construction, then delegates to rendering.

7. **Question Family ↔ Question Surface Inventory**
   - Strong registry street. Question family identity is static/exact, not inferred from free text.

8. **Question Family ↔ Bounded Ask**
   - Strong exact-family eligibility street through bounded status maps and CLI validation.
   - Not every registered family dispatches.

9. **Bounded Ask ↔ Dispatch ↔ Existing Surface**
   - Strong compatibility street. Dispatch selects existing direct surface behavior rather than owning answer composition.

10. **Diagnostic Inventory ↔ Diagnostic Shape Audit**
    - Strong governance street. Inventory declares diagnostic shape and record/mutation/source contracts; shape audit checks declared-vs-spec behavior.

11. **Pressure Evidence ↔ Pressure Classification**
    - Supported as a methodology/reporting street; implementation evidence is currently read-only fields and reports, not a separate recovered owner.

12. **Pressure ↔ Selection / Operational Story**
    - Supported locally: pressure audit candidates feed selection path and operational story focus.

13. **Candidate ↔ Admission / Verification / Readiness**
    - Supported family-locally. Candidate may become verified/readiness-supported only through specific evidence-gated rules.

14. **Observation Agreement ↔ Grammar Observation**
    - Supported locally in knowledge surfaces. Candidate agreement may feed grammar recurrence; neither becomes semantic architectural truth.

15. **Projection ↔ Explanation / Views / Audits**
    - Strong recurring street. Projected state and supports are consumed by explanations, views, diagnostic consumers, and operational surfaces.

Streets requested by the task that are not fully direct:

- **Pressure ↔ Orientation**: supported indirectly at most. Pressure can trigger bounded inquiry/orientation methodologically, but current implementation evidence is stronger for Pressure ↔ Selection/Operational Story and Inquiry Orientation ↔ State/RelatedMaterial.
- **Possible Observation ↔ Question**: supported weakly through candidate request/bounded inquiry methodology, not as a uniform implementation street.
- **Evidence ↔ Supporting Evidence**: supported when answer surfaces wrap evidence/support into answer-local supporting evidence payloads; not all evidence becomes supporting evidence.

## Bridge survey

Recurring intermediate neighborhoods:

| Pair asked about | Direct? | Recurring intermediate boundary | Current finding |
| --- | --- | --- | --- |
| Provider-native payload ↔ Fact | Usually no. | Observation and Evidence. | Provider data should not be treated as fact without observation/ingestion or another explicit fact-production path. |
| Observation ↔ Projected answer | No. | Evidence, Fact, Projection/FactSupport, Answer Composition. | Observation is upstream material; answer surfaces consume projected/support representations. |
| Question Family ↔ Answer Composition | Usually no. | Bounded Ask / Dispatch / selected surface. | Family identity selects or explains a surface; composition is surface-local. |
| Diagnostic Inventory ↔ Shape Audit result | Yes, but through implementation specs. | Implementation Specs. | Shape audit compares inventory declarations to specs/observed fields. |
| Pressure Evidence ↔ Implementation Readiness | No. | Pressure Classification, Responsibility Evaluation, Local Recovery. | Evidence must be classified and localized before readiness can be considered. |
| Candidate ↔ Verified / supported | No universal direct street. | Admission / verification evidence / family-local criteria. | Candidate status is preserved until a specific admission surface permits movement. |
| Supporting Evidence ↔ Final rendered answer | No. | Reason, boundary/limitations, Answer Composition, Rendering. | Support alone is not the answer. |
| Observation Agreement ↔ Architecture truth | No. | Grammar Observation still does not promote to semantic truth. | The path terminates before architecture truth. |
| Bounded Inquiry ↔ Implementation | No. | Implementation Readiness and tests/preservation surface. | A bounded investigation can terminate without implementation. |
| Projection ↔ Cluster mutation | No. | Diagnostic/operational boundary. | Projection produces read models; mutation authority is separately declared/refused. |

## Isolation survey

Neighborhoods that repeatedly remain isolated or family-local:

- **Diagnostic Inventory / Diagnostic Shape Audit** are tightly coupled to operational-surface governance. They touch question inventory and projected consumers, but their strongest recurrence is within diagnostic visibility and record/mutation contracts.
- **Observation Agreement / Grammar Observation** remain knowledge/grammar-family local. They deliberately stop before semantic or architectural truth.
- **Provider Translation** is often adapter-local and compressed. It neighbors Observation, but does not recur as a fully separated universal translation owner.
- **Execution Status / Runtime Trace** appear in relationship grammar as operational/runtime visibility neighborhoods, not as central participants in the architecture-recovery neighborhoods surveyed here.
- **Question Surface Inventory / Bounded Ask** are locally strong around exact question-family invocation, but reject broad free-text routing.
- **Pressure Evidence / Pressure Classification** are recurring in methodology and reporting; implementation ownership remains weaker than the pressure audit row-building surface.

Neighborhoods that appear globally or near-globally:

- **Evidence/support** appears across observation ingestion, fact support, explanations, reasoning/selection paths, capability/readiness, diagnostics, and reports.
- **Authority/boundary/refusal** appears across question inventory, diagnostic inventory, shape audit, operational story, inquiry orientation, projection, candidate admission, and constitutional reports.
- **Compatibility** appears as a repeated local concern when recovered boundaries preserve existing public outputs.

Neighborhoods not shown to directly interact:

- Observation Agreement does not directly interact with Bounded Ask.
- Provider Translation does not directly interact with Diagnostic Shape Audit except through broader diagnostic/source visibility if a surface is registered.
- Pressure Audit does not directly own Inquiry Orientation.
- Question Family does not directly own Observation ingestion.
- Diagnostic Inventory does not directly promote Candidate to Admission.

## Recurring local topology

The repository has earned local topology, not a universal architectural graph.

### 1. Evidence/support corridor

Recurring corridor:

```text
Observation / Event / Source material
  -> Evidence
  -> Fact or support projection when permitted
  -> Supporting Evidence
  -> Reason
  -> Bounded Answer / Explanation
```

This corridor is repeatedly implementation-backed, but it is not mandatory at every step. Tool result extraction may stop at Evidence. Observation may be recorded without fact promotion. Answer surfaces may consume projected support rather than raw evidence.

### 2. Question-to-surface chokepoint

Recurring chokepoint:

```text
Question Family
  -> Question Surface Inventory
  -> Bounded Ask eligibility / required args
  -> Dispatch to existing surface
```

The chokepoint rejects unknown families, free-text ask routing, diagnostic-only families, not-dispatchable families, and bad parameter counts. This is a real local topology: exact registration controls bounded invocation.

### 3. Diagnostic governance paired neighborhood

Recurring pair:

```text
Diagnostic Inventory
  <-> Diagnostic Shape Audit
```

This is one of the strongest recovered local pairs. Inventory declares operational shape, record scope, ledger/mutation boundaries, and source use; shape audit checks declared shape against specs. The pair also bridges to question-surface visibility when question inventory is registered as a diagnostic surface.

### 4. Candidate-admission gated cul-de-sac

Recurring pattern:

```text
Candidate
  -> Admission / verification / readiness criteria
  -> stronger status OR stop
```

Candidate does not freely flow into verified, selected, implemented, or true. Many candidate paths terminate as unsupported, unknown, not selected, insufficient evidence, or future frontier.

### 5. Projection as bridge, not city center

Projection bridges event/fact storage to State, FactSupport, explanations, current-fact views, and audits. It is important and recurring, but the evidence does not make it a universal city center. Projection does not own provider translation, bounded ask, pressure classification, diagnostic shape contracts, or candidate admission.

### 6. Answer-composition cul-de-sacs

Answer composition repeatedly terminates local evidence/reason/support into a bounded view, then hands off to rendering. It preserves support and boundary; it does not infer new truth, execute operations, or mutate the cluster.

### 7. Authority/boundary as repeated guardrail

Authority/boundary appears across many neighborhoods. It functions less like a single hub and more like a recurring curb: every neighborhood declares what it cannot own. This is topology by refusal.

## Negative authority

Implementation-backed evidence rejects the following overclaims:

### Rejected: every neighborhood touches every other neighborhood

The implementation shows explicit local relationships, not complete connectivity. Question family inventory touches bounded ask and diagnostics; observation ingestion touches evidence/facts/projection; grammar observation touches agreement; pressure audit touches audits/selection/story. Many pairs have no direct implementation street.

### Rejected: one universal architectural graph

The strongest relationship report says relationships are exposed across subsystems with stable recurring structure, but no single canonical relationship vocabulary or shared relationship schema is introduced. Responsibility is distributed across docs/inventories rather than a shared graph object.

### Rejected: one universal constitutional flow

Transition-family evidence repeatedly separates observation promotion, candidate admission, question invocation, diagnostic governance, projection, implementation readiness, and methodology earning. The repository supports family-local transitions, not one constitutional movement.

### Rejected: all neighborhoods belong to one family

Diagnostic governance, question invocation, observation/evidence/fact projection, pressure visibility, grammar agreement, provider translation, candidate admission, and answer composition remain distinct. They recur beside one another, often through bridges, but they do not merge.

### Rejected: presentation vocabulary automatically becomes knowledge

Repository instructions and knowledge-reachability discipline reject promoting presentation labels into preserved/projected knowledge without implementation evidence.

## Locality

| Topology | Current locality |
| --- | --- |
| Observation -> Evidence -> optional Fact -> Projection | Implementation-local and cross-family recurring. |
| FactSupport / Supporting Evidence -> Reason -> Answer Composition | Cross-family recurring in representative surfaces; not universal. |
| Question Family -> Inventory -> Bounded Ask -> Dispatch | Implementation-local and family-local to question/ask surfaces. |
| Diagnostic Inventory -> Diagnostic Shape Audit | Implementation-local and operational-governance local. |
| Candidate -> Admission / Verification / Readiness | Cross-family recurring, but admission rules remain family-local. |
| Pressure Evidence -> Pressure Classification -> Recovery/Readiness | Mostly methodological/reporting; pressure audit row assembly is implementation-local. |
| Observation Agreement -> Grammar Observation | Implementation-local to knowledge/grammar surfaces. |
| Provider Translation -> Observation | Implementation-local but uneven/compressed across adapters. |
| Authority/boundary/refusal | Cross-family recurring and partly constitutional as a guardrail, but not a single service. |
| Universal city topology | Unknown/unsupported/rejected. |

## Typed unknowns

- **Missing streets:** Some requested streets, especially Pressure ↔ Orientation and Possible Observation ↔ Question, are not yet strongly implemented as direct streets.
- **Incomplete neighborhoods:** Provider Translation is uneven; some providers use implementation-local records, while others compress decoding and observation construction.
- **Hidden intermediate owners:** Bounded ask runtime validation and dispatch are still compressed in one CLI helper. Pressure row assembly had repeated local variables before later slices but not always a separate owner.
- **Future districts:** Relationship grammar exposes stable structural patterns, but a shared relationship schema or global graph is not currently earned.
- **Neighborhoods awaiting implementation:** Some methodology-backed neighborhoods, such as Responsibility Evaluation and Pressure Classification, lack a single implementation owner.
- **Apparent topology not yet supported:** Broad orientation, universal transition, universal admission, generic dispatch, semantic question routing, and global architecture remain unsupported.
- **Directness unknowns:** Some answer-like surfaces may have support/reason/composition boundaries, but current evidence supports this strongly only in representative recovered surfaces.
- **Authority unknowns:** Inventory rows expose boundaries, but not every boundary is dynamically enforced by a separate authority validator.

## Smallest truthful answer

The repository has already earned this local topology:

```text
Evidence-bearing material repeatedly enters bounded local corridors.

Some corridors promote observations into evidence/facts/projection.
Some corridors register exact questions and dispatch only to existing bounded surfaces.
Some corridors declare diagnostic shape and audit that declaration.
Some corridors preserve candidates until family-local admission permits or refuses movement.
Some corridors compose bounded answers from support, reason, boundary, and limitations.

These corridors recur.
They do not merge into one universal graph, flow, layer, city, engine, or architecture.
```

The strongest topology is therefore **recurring local corridors with guarded chokepoints and explicit termination boundaries**.

What has been earned is not a city plan. It is a set of lawful streets, recurring bridges, and repeated refusals to connect where authority is absent.

## Lawful termination

This characterization stops at implementation-backed adjacency. It does not recommend implementation, recover a new ownership slice, introduce new diagnostics, add a CLI surface, or promote methodology into runtime architecture.

No diagnostic, audit, probe, view, operational CLI flag, or recordable output was added or modified by this document.

## Remaining questions

1. Does Pressure ↔ Orientation become implementation-backed if future surfaces explicitly connect pressure rows to inquiry orientation rather than selection/story?
2. Should Bounded Ask validation/dispatch remain compatibility compression, or will future implementation pressure justify a separate bounded invocation object?
3. Will Provider Translation become a recurring explicit neighborhood across adapters, or remain source-local compression?
4. Can Responsibility Evaluation become implementation-backed without inventing a universal responsibility evaluator?
5. Will relationship grammar remain distributed across inventories/audits, or will implementation eventually earn a shared relationship schema?
6. Which answer-like surfaces lack explicit support/reason/boundary/composition separation?
7. Where should candidate admission stay family-local, and where are family-local criteria still hidden?

## Confidence

- **High confidence** in Observation ↔ Evidence ↔ optional Fact ↔ Projection, Question Family ↔ Inventory ↔ Bounded Ask ↔ Dispatch, and Diagnostic Inventory ↔ Diagnostic Shape Audit.
- **High confidence** that universal graph/flow/family claims are not supported.
- **Medium confidence** in cross-family Evidence/Supporting Evidence/Reason/Answer Composition recurrence, because it is strong in representative surfaces but not proven uniformly.
- **Medium confidence** in Candidate ↔ Admission recurrence, because the pattern is repeated but admission criteria remain family-local.
- **Low-to-medium confidence** in direct Pressure ↔ Orientation and Possible Observation ↔ Question streets; current evidence supports adjacent methodological relationships more than direct implementation streets.
