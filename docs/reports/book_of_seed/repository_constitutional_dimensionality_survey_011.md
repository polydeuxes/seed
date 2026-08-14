# Repository Constitutional Dimensionality Survey 011

## Repository state examined

- Survey operation: repository survey and constitutional orientation, not a SQLite witness slice, Python refactor, Book-wide rewrite, final ontology, type system, programming language, universal schema, or proof of exact dimensionality.
- Recorded `git rev-parse HEAD`: `9005fe7444f696aacecdc5d710403003d5076329`.
- Recorded `git status --short`: empty output; the checkout was clean before this survey file was created.
- PR 1753 is present in the surveyed checkout: `8df2688 Add SQLite witness support binding slice 002 (#1753)` appears in the local first-parent-visible history immediately below HEAD.
- Recent constitutional recovery artifacts verified present:
  - `book_of_seed/realization_independence_audit_008.md`
  - `book_of_seed/eye_competency_composition_locality_characterization_009.md`
  - `book_of_seed/sqlite_constitutional_witness_slice_001.md`
  - `book_of_seed/sqlite_constitutional_witness_slice_002.md`
- Current Book of Seed structure located in eight numbered districts:
  - `book_of_seed/01-grammar-and-standing/`
  - `book_of_seed/02-acts-and-constraints/`
  - `book_of_seed/03-goals-and-advancement/`
  - `book_of_seed/04-inquiry-and-examination/`
  - `book_of_seed/05-evidence-and-knowledge/`
  - `book_of_seed/06-state-and-projection/`
  - `book_of_seed/07-operational-realization/`
  - `book_of_seed/08-authority-communication-and-stopping/`
- SQLite witness district located at `witnesses/sqlite_constitutional_witness_slice_001/` with `schema.sql`, `fixtures.sql`, `verify.sql`, `README.md`, and `run_verification.sh`.
- SQLite-Seed Grammar Friction Characterization 010 is available at `book_of_seed/sqlite_seed_grammar_friction_characterization_010.md` and is treated as evidence.

## Scope and evidence method

This survey used repository-supported constitutional distinctions first, then stable Book clauses, repeated investigations, Python realization evidence, SQLite witness evidence, and orientation artifacts. It did not inventory every class, table, function, diagnostic, or Book clause. It selected examples that test recurrence, independent variation, local expansion, and realization compression.

Evidence districts inspected include all eight Book districts, the constitutional reports for foundational kinds, selection topology, selection-road sufficiency, consumer uptake, uptake standing, occurrence evidence, realization independence, Eye/competency locality, SQLite Slice 001, SQLite Slice 002, and SQLite-Seed grammar friction 010. Representative implementation evidence was read from runtime modules and tests concerned with events, evidence, facts, observations, authority, execution, inquiry, selection, projection, recording, and diagnostics.

## Classification vocabulary used

The survey uses the required vocabulary as follows:

- **macro dimension**: recurring constitutional coordinate family answering a broad question across districts.
- **local dimension**: bounded coordinate family that becomes visible under a local question but should not be universalized.
- **coordinate**: a representable constitutional variable inside a macro or local dimension.
- **axis or coordinate value**: one possible value or posture on a coordinate.
- **standing**: lawful posture or admissibility/reliance condition, sometimes a macro family and sometimes a local judgment.
- **relation**: comparison, applicability, binding, mismatch, or dependency among dimension-bearing subjects.
- **operator**: transformation that evaluates, selects, projects, constrains, records, or moves material across dimensions.
- **act**: responsible occurrence or proposed occurrence that may alter or preserve coordinates.
- **constraint**: rule, precondition, policy, prohibition, or requirement limiting lawful coordinate transitions.
- **projection or lens**: view that exposes, selects, or recomposes material without automatically establishing upstream truth.
- **composition**: bounded assembly of multiple materials or standings into a new consumer-local result.
- **movement topology**: lawful transition structure among subjects, acts, standings, responsibilities, and scopes.
- **metaphor or orientation vocabulary**: presentation language that may help orient but is not established as Seed knowledge by naming alone.
- **implementation mechanism**: field, table, class, function, method, view, query, enum, exception, or storage feature carrying some current realization.
- **unresolved**: insufficient evidence or contradicted evidence prevents stable classification.

## Candidate macro dimensions

### 1. Subject / identity

- **Classification**: macro dimension.
- **Constitutional question answered**: Which subject, representation, occurrence, producer, source, consumer, assertion, competency, projection, or record is this?
- **What may vary**: subject identity, representation identity, assertion identity, source identity, consumer identity, producer boundary identity, event identity, projection identity, local key identity, and join/reference identity.
- **What remains invariant**: identity distinguishes reference targets without itself establishing truth, occurrence, authority, or standing.
- **Book districts**: Book I separates artifact representation from standing and producer occurrence; Book II separates act artifact from act; Book III separates selected need/candidate from movement; Book IV requires question/inquiry identity; Book V separates evidence, testimony, fact, source, and provenance identities; Book VI separates event, fact, entity, state, and projection; Book VII separates proposal, execution, result, and record; Book VIII separates operator request, handoff, authority, and consumer.
- **Implementation districts**: Python dataclasses and ledgers carry event IDs, subject IDs, source IDs, capability IDs, projection references, selected names, producer references, and diagnostic run IDs. SQLite carries row primary keys and textual IDs for changes, evidence, provenance, competencies, sources, and Book traceability.
- **Interactions**: identity interacts with provenance, standing, authority, responsibility, occurrence, locality, and content.
- **Recurrence across realizations**: strong. Python object identity and SQLite row identity both compress Seed-native identity distinctions.
- **Counterevidence**: local IDs are sometimes merely implementation keys; row uniqueness or object construction does not establish constitutional subject identity.
- **Confidence**: high.

### 2. Assertion / content

- **Classification**: macro dimension.
- **Constitutional question answered**: What is being asserted, claimed, selected, explained, recorded, projected, or tested?
- **What may vary**: assertion text, claim family, observable subject, result content, explanation reason, selected candidate, refusal reason, event payload, diagnostic finding, query result, and projection content.
- **What remains invariant**: content can be represented without fact standing, verified provenance, authority, or occurrence truth.
- **Book districts**: Book I distinguishes representation from standing; Book II distinguishes proposal/intent/classification from performance; Book III distinguishes need descriptions from movement; Book IV distinguishes question-shaped text from inquiry; Book V distinguishes testimony and evidence from established fact; Book VI distinguishes event assertion from fact/state; Book VII distinguishes provider response from verified effect; Book VIII distinguishes communication from establishment.
- **Implementation districts**: observation records, evidence records, event payloads, fact extraction, inquiry results, execution results, projection results, diagnostics, and SQLite assertion rows.
- **Interactions**: content is bound by source/provenance, scope/locality, authority/warrant, responsibility, and standing.
- **Recurrence across realizations**: strong. Python return values and SQLite query results both carry content while not establishing all constitutional standings.
- **Counterevidence**: content is sometimes inseparable from local type or record fields in implementation, so not every field is a separate coordinate.
- **Confidence**: high.

### 3. Standing

- **Classification**: macro dimension with local standing-coordinate families; also produces local standings and values.
- **Constitutional question answered**: What lawful posture, admissibility, reliance permission, truth status, verification status, or movement permission does this material have for this bounded use?
- **What may vary**: standing kind, reason, admissibility, reliance permission, movement permission, truth status, verification status, unknown reason, refusal reason, and forbidden inference.
- **What remains invariant**: standing is not the artifact, field, content, source, or event itself.
- **Book districts**: all eight Books repeatedly distinguish artifact, act, evidence, projection, warrant, authority, communication, and stopping from their standings.
- **Implementation districts**: status enums/strings, validation results, audit outputs, event/fact separation, capability standing, projection cache freshness, execution status, diagnostic flags, and SQLite standing columns/views.
- **Interactions**: standing is affected by provenance, authority, scope, responsibility, occurrence, and content; it constrains reliance and movement.
- **Recurrence across realizations**: very strong. Python uses dataclass fields, booleans, enums, exceptions, and result objects; SQLite uses status strings, CHECK constraints, CASE views, and audit queries.
- **Counterevidence**: standing may be too cross-cutting to behave like a simple peer dimension; it often attaches to subjects and relations rather than existing as a single global axis.
- **Confidence**: high as a macro family; medium as one simple dimension.

### 4. Source / provenance

- **Classification**: macro dimension with strong local coordinate systems.
- **Constitutional question answered**: From what source, context, lineage, producer, or evidence basis does this claim derive, and how far is that lineage applicable or verified?
- **What may vary**: reference presence, referenced material existence, source identity, source context, attribution, represented lineage, lineage applicability, internal coherence, independent verification, verified causation, producer occurrence, and support independence.
- **What remains invariant**: provenance representation does not automatically establish truth, causation, independence, producer occurrence, or applicability.
- **Book districts**: Book I producer occurrence and construction; Book IV examination requirements; Book V evidence/provenance/explanation; Book VI events/facts/state; Book VII warrants/execution results; Book VIII handoff and authority boundaries.
- **Implementation districts**: evidence source references, observation sources, fact support, explanation lineage, event metadata, selection basis, projection lineage, SQLite provenance tables and support-binding views.
- **Interactions**: provenance affects standing, content admissibility, authority, locality, occurrence, and responsibility.
- **Recurrence across realizations**: strong. Python in-process references and lineage fields compress several Seed distinctions; SQLite text/foreign references do the same unless compensated.
- **Counterevidence**: source identity, evidence support, producer occurrence, and independent verification vary independently, so provenance is not one scalar axis.
- **Confidence**: high as macro family; high that local expansion is required.

### 5. Responsibility

- **Classification**: macro dimension.
- **Constitutional question answered**: Who or what boundary is responsible for producing, checking, selecting, recording, projecting, refusing, or relying on a claim or act?
- **What may vary**: responsibility family, responsible subject, producer boundary, consumer boundary, examiner, recorder, operator, owner, adapter participation, and cluster mutation responsibility.
- **What remains invariant**: responsibility is not identical to authority, implementation ownership, source, identity, or occurrence evidence.
- **Book districts**: Book I constructors and production authority; Book II acts and artifacts; Book IV bounded examination responsibility; Book V testimony/fact ingestion; Book VI ownership discrepancy; Book VII execution/recording; Book VIII authority and handoff.
- **Implementation districts**: capability/executor boundaries, event ledgers, diagnostic record scopes, fact extraction responsibility, selection consumers, SQLite competency rows with responsibility family/subject.
- **Interactions**: responsibility constrains acts, authority, occurrence claims, provenance interpretation, and standing assignment.
- **Recurrence across realizations**: strong in Python; explicit in SQLite witness competency/evidence rows.
- **Counterevidence**: some responsibility-locality distinctions remain partly unresolved; implementation ownership can be mistaken for constitutional responsibility.
- **Confidence**: high.

### 6. Authority / warrant

- **Classification**: macro dimension.
- **Constitutional question answered**: What grants permission or warrant for a bounded act, reliance, selection, execution, movement, projection, or refusal?
- **What may vary**: authority origin, authority zone, scope binding, operator approval, policy allowance, warrant basis, precondition satisfaction, and authority mismatch/block.
- **What remains invariant**: authority is not generated by internal recommendation, selection, record existence, handoff, or provider response.
- **Book districts**: Book III selection and authorization; Book IV examination applicability; Book VII warrants/proposals/execution; Book VIII authority scope/refusal; Book V testimony/fact standing.
- **Implementation districts**: authority scope binding, authorization references, execution proposal checks, policy/precondition audits, diagnostic mutation flags, SQLite authority zones.
- **Interactions**: authority constrains movement, execution, reliance, recording, communication, and fact establishment; it interacts with source, responsibility, scope, and standing.
- **Recurrence across realizations**: strong. Python authorization objects/references and SQLite authority_zone columns both compress constitutional warrant unless bounded by Book clauses and tests.
- **Counterevidence**: warrant, approval, authority zone, and policy satisfaction can differ; authority is a family, not one Boolean.
- **Confidence**: high.

### 7. Scope / locality

- **Classification**: macro dimension with multiple local dimensions.
- **Constitutional question answered**: Within what bounded family, subject, authority zone, inquiry, source context, preservation horizon, organism, host/process, consumer, or purpose is a claim or act meaningful?
- **What may vary**: subject locality, responsibility locality, authority locality, evidence/provenance locality, inquiry locality, observation-context locality, organism locality, host/process locality, consumer locality, preservation horizon, and purpose scope.
- **What remains invariant**: locality bounds a claim but does not itself establish truth, occurrence, authority, or consumer uptake.
- **Book districts**: all Books use bounds, scope, local purpose, horizon, exact candidate sets, authority zones, and consumer-local standing.
- **Implementation districts**: operator authority scope binding, bounded examinations, local observations, projection replay scopes, diagnostic run scope, SQLite `local_observation` and authority zones, test fixtures that preserve local admissibility.
- **Interactions**: scope bounds identity, authority, responsibility, provenance applicability, standing, movement, and preservation.
- **Recurrence across realizations**: strong, especially after Eye/competency locality and SQLite friction reports.
- **Counterevidence**: several locality branches remain unresolved or orientation-only; not every local label is a constitutional locality coordinate.
- **Confidence**: high as macro family; medium for individual branches not repeatedly tested.

### 8. Occurrence / preservation

- **Classification**: macro dimension family, probably two tightly related local families rather than one scalar dimension.
- **Constitutional question answered**: Did a responsible act, branch, recording, construction, external effect, extraction, or uptake occur, and what evidence or preserved record exists for that occurrence?
- **What may vary**: boundary invocation, assertion-bearing branch occurrence, result construction, external effect, recording occurrence, preserved record, persistent record, producer occurrence, observer-held occurrence evidence, preserved occurrence evidence, knowledge extraction occurrence, and consumer uptake occurrence.
- **What remains invariant**: representation existence, object construction, row insertion, or view evaluation does not automatically prove responsible occurrence or truth.
- **Book districts**: Book I construction/production; Book II act occurrence; Book V recording/knowledge; Book VI event recording; Book VII execution/recording; Book VIII communication/uptake.
- **Implementation districts**: event ledgers, execution traces, recording APIs, projection caches, diagnostic record scopes, SQLite fixture creation and status columns.
- **Interactions**: occurrence affects standing, provenance, responsibility, preservation, authority, and movement; preservation affects future admissibility without proving represented truth.
- **Recurrence across realizations**: strong. Python calls and SQLite transactions/builds both compress occurrence distinctions.
- **Counterevidence**: occurrence and preservation can vary independently; a record may exist without occurrence truth, and occurrence evidence may exist without durable preservation.
- **Confidence**: high for family; medium on whether it should remain one macro family or split into two.

## Candidate dimension inventory

| Candidate name | Classification | Macro parent | Constitutional question | Independent variables | Known coordinate values or standings | Local expansions | Recurring districts | Python witness | SQLite witness | Book support | Counterevidence | Confidence | Remaining falsification question |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Subject / identity | macro dimension | self | Which constitutional subject or representation is this? | subject, representation, assertion, source, occurrence, projection, consumer IDs | same/different, selected/non-selected, duplicate, coherent/incoherent | representation, subject, assertion, occurrence, source, responsibility, projection identity | Books I-VIII, selection, uptake, occurrence, SQLite | object IDs, dataclass fields, event IDs | primary keys and text refs | artifact/act/event/fact/projection distinctions | implementation IDs may be mere keys | high | When does a local key become constitutional subject identity? |
| Assertion / content | macro dimension | self | What claim, question, result, or finding is represented? | text, payload, claim family, result content, explanation | recorded claim, testimony, finding, result, projection | observable subject, claim family, assertion text, result content | Books I-VIII | payloads, observations, facts, diagnostics | recorded change assertions, query results | testimony != fact; event != fact | fields are not automatically coordinates | high | Which content differences alter constitutional judgment rather than representation detail? |
| Standing | macro dimension / standing family | self | What lawful posture does it have? | admissibility, reliance, truth, verification, movement permission, reason | established, not established, unknown, permitted, blocked, refused | standing kind, reason, consumer-relative reliance, truth/verification, forbidden inference | Books I-VIII, uptake, SQLite | enums, result statuses, validation outcomes | status columns, CASE-derived postures | standing repeated throughout Book | may attach to relations rather than act as one axis | high family / medium scalar | Is standing one macro dimension or a coordinate family attached to all subjects? |
| Source / provenance | macro dimension | self | What source, context, lineage, and support apply? | source identity, material existence, attribution, lineage, applicability, verification, causation | missing, dangling, represented, verified, conflicting, applicable | source identity, lineage representation, applicability, independent verification, producer occurrence | Books I, IV-VII, reports 006-010 | evidence references, lineage/explanation fields | provenance table, support binding view | evidence/provenance clauses | multiple variables independent | high | Should producer occurrence remain inside provenance or occurrence family? |
| Responsibility | macro dimension | self | Which responsible boundary owns production/checking/reliance? | family, subject, producer, examiner, recorder, consumer | responsible, consumer-local, owner-bound, not owned | responsibility locality, producer boundary, consumer boundary | Books I-II, IV-VIII | executors, recorders, diagnostic scopes | competency responsibility fields | constructors/acts/recording clauses | implementation ownership != responsibility | high | How many responsibility localities are constitutionally established? |
| Authority / warrant | macro dimension | self | What permits or warrants this act/reliance? | origin, zone, approval, policy, precondition, warrant basis | authorized, blocked, mismatch, insufficient, scoped | authority zone, scope binding, warrant reason, precondition | Books III-IV, VII-VIII | operator authority binding, execution proposal | authority_zone columns and blocked postures | authority scope and warrant chapters | authority not same as selection or record | high | How far can authority be represented without an explicit grant event? |
| Scope / locality | macro dimension | self | Where and for what bounded purpose does this hold? | subject, authority zone, inquiry, source context, consumer, host, horizon | local, external, bounded, outside scope, purpose-limited | subject, responsibility, authority, inquiry, observation-context, preservation, organism, host/process locality | Books I-VIII, report 009, SQLite | replay scopes, local observations, diagnostic runs | local_observation, external_admin, bounded competencies | boundedness throughout Book | local labels can be mere presentation | high family / medium branches | Which locality branches vary independently across more than one district? |
| Occurrence / preservation | macro dimension family | self or split | What happened, and what record/evidence persists? | invocation, branch, result, external effect, recording, preservation, uptake | occurred, not established, recorded, preserved, persistent, observer-held | act, producer, branch, result, recording, record, knowledge extraction, uptake occurrence | Books I-II, V-VII, reports 007-010 | calls, event ledger, execution records | row existence, status, witness build | occurrence survey and recording clauses | occurrence and preservation can split | high family / medium unity | Should preservation become separate macro dimension? |
| Act | act / operator | occurrence, responsibility, authority | What responsible performance changes or preserves coordinates? | performer, input, output, occurrence, authority | proposed, invoked, completed, failed, refused | execution, recording, selection, examination, communication | Books II, III, IV, VII, VIII | method calls and executor calls | statement execution not constitutional act | act != artifact | same act type operates over dimensions | high not dimension | Can any act property vary independently enough to be a dimension rather than kind? |
| Constraint | constraint / operator | authority, standing, scope | What limits lawful transitions? | policy, precondition, prohibition, requirement | passed, blocked, required, forbidden | schema checks, policy, preconditions | Books II, VII-VIII | validations, precondition audits | CHECK constraints, CASE guards | act != constraint | constraint can limit several dimensions | high not dimension | When is a constraint record also evidence? |
| Road / handoff / uptake | movement topology / relation | identity, standing, authority, scope | How does material move between producer/artifact/consumer/purpose? | producer, artifact, consumer, purpose, warrant, scope | sufficient, insufficient, adopted, refused, consumer-local | selection road, uptake standing, communication handoff | Books I, III, VIII, passes 003-006 | adapter handoff, selection consumers | not directly modeled except joins/prose | road != lens; handoff != execution | requires many other coordinates | high topology | Which road facts deserve durable representation? |
| Lens / projection | projection or lens / operator | content, standing, occurrence | What does a view expose or recompose? | selected inputs, projection rules, replay scope, freshness | view, cache, projection, stale/current | view availability, current state, projection lineage | Books I and VI; SQLite 010 | StateProjector, projection store | SQL views | projection != establishment | view evaluation != occurrence | high not peer dimension | When does projected content become new assertion? |
| Composition | composition / operator | identity, content, standing | How are materials assembled into a consumer-local whole? | contributors, coherence, duplicate handling, admissibility | coherent, conflict, duplicate preserved | competency composition, explanation composition | uptake and locality reports; Book VIII | composition result objects | join topology and views | composition != adjacency | not independent without inputs | medium-high | Which composition standings should be preserved? |
| Movement | movement topology | standing, authority, scope, occurrence | What lawful transition occurs? | from/to posture, authority, responsibility, preserved record | opened, blocked, completed, stopped, refused | advancement, execution, reliance, projection use | Books III, VII-VIII | execution/goal advancement flows | view permission postures | orientation != movement | movement is transition, not axis | high topology | Can movement be represented without sequence assumptions? |

## Macro-dimensional map

```text
Supported macro-dimensional families

identity ─┬─ content/assertion ─┬─ standing
          │                     │
          │                     ├─ source/provenance
          │                     │
          │                     ├─ responsibility
          │                     │
          │                     ├─ authority/warrant
          │                     │
          │                     ├─ scope/locality
          │                     │
          │                     └─ occurrence/preservation
          │
          └─ participates in every relation that must avoid confusing
             representation identity with subject, producer, occurrence,
             source, or projection identity.

Major operators and topology over these families

acts: perform or attempt coordinate-changing/preserving occurrences.
constraints: limit permissible transitions or reliance.
roads/handoffs/uptake: relate producer, artifact, consumer, purpose, warrant,
standing, scope, and preservation.
lenses/projections: expose or recompose selected coordinates without automatically
changing upstream standing.
composition: assembles bounded inputs into consumer-local results.
movement topology: lawful transition structure among standings and scopes.
```

Unresolved boundaries: standing may be a macro family or a cross-cutting local coordinate system; occurrence and preservation may split into two macro families; producer occurrence may belong both to provenance and occurrence; locality branches are not all equally established; some Book chapter organization mixes dimensions, kinds, and operators.

## Local coordinate systems

### Subject / identity local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Representation identity | supported | identity | content, standing | same fields can have different producer occurrence | Book I, SQLite, Python dataclasses | object identity, row PK | may be mistaken for constitutional subject | reveals internal identity structure |
| Subject identity | supported | identity | scope, responsibility | same assertion can concern different subjects | Book IV/V, SQLite claims | subject fields/text IDs | subject binding hidden in payload | reveals internal structure |
| Assertion identity | supported | identity | content, provenance | same subject/provenance can have different claims | Book V/VI, SQLite changes | event IDs/change IDs | assertion conflated with record | reveals internal structure |
| Occurrence identity | supported | identity + occurrence | responsibility, preservation | same representation can lack producer occurrence | occurrence survey, uptake reports | call context, event IDs | object construction misread as occurrence | bridges identity and occurrence |
| Source identity | supported | identity + provenance | evidence, standing | same content can have different source | Book V, SQLite evidence | source fields | source independence lost | reveals provenance structure |
| Responsibility identity | supported | identity + responsibility | authority, act | same source can differ from responsible producer | Book I/II/VII | executor/owner fields | owner conflated with implementation module | reveals responsibility structure |
| Projection identity | supported | identity + projection | state, scope | same upstream records can produce different views | Book VI | projection refs/cache keys | view mistaken for source | reveals projection topology |

### Assertion / content local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Claim family | supported | content | responsibility, scope | same subject may have different families | SQLite competency/change family, Book V | strings/enums | family hidden in prose | reveals content binding needs |
| Assertion text/payload | supported | content | standing, provenance | same text can have different standing/source | events, diagnostics, testimony | payload dicts, text columns | text mistaken for fact | reveals representation/content split |
| Observable subject | supported | content + identity | evidence, locality | evidence may bind or fail to bind subject | Book IV/V, SQLite | subject fields | unknown binding concealed | reveals local evidence content |
| Result content | supported | content | occurrence, standing | result can exist without verified effect | Book VII, Python execution | return values/results | result mistaken for effect | reveals output/effect distinction |
| Explanation reason | supported | content + provenance | standing | same claim can have different reasons | Book V, tests, SQLite standing_reason | reason fields | reason collapsed to status | reveals explanation topology |

### Standing local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Standing kind | supported | standing | all | testimony vs fact vs permission can vary with same content | Books I-VIII | enums/status strings | single Boolean admissibility | reveals family complexity |
| Standing reason | supported | standing | provenance, authority, scope | same posture can have different reasons | SQLite, diagnostics, refusal | strings/result fields | why is lost | reveals explanatory coordinate |
| Consumer-relative admissibility | supported | standing | uptake, scope, authority | one consumer may adopt local assertion while upstream remains weaker | uptake reports | consumer result objects | consumer-local reliance universalized | reveals uptake topology |
| Reliance permitted | supported | standing | authority, source | evidence can be premise-relative but not fact | Book V, SQLite | statuses | testimony becomes truth | reveals reliance coordinate |
| Movement permitted | supported | standing | authority, scope | selection standing can lack authorization | Book III/VII | authorization checks | selected implies authorized | reveals movement coordinate |
| Truth status | supported | standing + content | evidence, provenance | record existence can coexist with not_established truth | Book V/VI, SQLite | truth status columns | record becomes fact | reveals truth/record split |
| Verification status | supported | standing + provenance | occurrence | represented lineage can be unverified | SQLite Slice 002 | verification fields | represented provenance overpromoted | reveals provenance-local standing |
| Unknown reason | supported | standing | evidence/provenance | unknown can preserve rather than fail | Book IV, SQLite | unknown_* statuses | unknown collapsed into false | reveals lawful inactivity |
| Forbidden inference | supported | standing/constraint | all | local permission forbids broader facts | SQLite, diagnostics | forbidden text/status | scope leakage | reveals guardrail topology |

### Source / provenance local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Reference presence | supported | provenance | identity | reference can exist while target missing | SQLite dangling refs | text refs | names treated as material | reveals reference/material split |
| Referenced material existence | supported | provenance | preservation | target row may be absent/present | SQLite | joins/FKs | dangling hidden | reveals material boundary |
| Source attribution | supported | provenance | responsibility | same material can be attributed to different source | Book V | source fields | source context erased | reveals attribution coordinate |
| Source context | supported | provenance + locality | scope | same source in different context differs | observations, SQLite fixture_run | context fields | context globalized | reveals locality branch |
| Lineage representation | supported | provenance | standing | lineage represented but not verified | reports 006/010 | lineage fields | represented treated as verified | reveals local standing |
| Lineage applicability | supported | provenance relation | content, scope | provenance can exist but not apply to claim/evidence | SQLite applicability statuses | applies_to fields | source overapplied | relation over coordinate |
| Internal coherence | supported | provenance/standing | content | conflicting lineage preserved | SQLite case q | conflict statuses | conflict collapsed by COALESCE | reveals coherence coordinate |
| Independent verification | supported | provenance/standing | occurrence | represented lineage can be verified or not | SQLite | verification_status | verification omitted | reveals stronger standing |
| Verified causation | unresolved | provenance + occurrence | responsibility | not represented enough as positive current standing | reports 006/010 | mostly absent | causation invented | unresolved boundary |
| Producer occurrence | supported as neighboring occurrence | occurrence/provenance | responsibility | live return can differ from constructed artifact | occurrence/uptake reports | call context, status | provenance conflated with occurrence | likely bridges families |

### Responsibility local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Responsibility family | supported | responsibility | content, scope | same subject may belong to different family | SQLite competency rows | family strings | family hidden in class | reveals local jurisdiction |
| Responsibility subject | supported | responsibility | identity, locality | same family can apply to different subject | SQLite/Book IV | subject fields | wrong subject admitted | reveals subject locality |
| Producer boundary | supported | responsibility + occurrence | provenance | artifact can exist without producer occurrence | Book I/II, reports | functions/methods | construction mistaken for production | reveals occurrence bridge |
| Consumer boundary | supported | responsibility + standing | uptake | consumer may establish local assertion | uptake reports | consumer assembly functions | uptake universalized | reveals relation topology |
| Recorder boundary | supported | responsibility + preservation | occurrence | recording act differs from recorded event | Book V/VI/VII | ledger append | record existence overclaims truth | reveals preservation branch |
| Diagnostic responsibility | supported implementation/book by AGENTS | responsibility + scope | standing | diagnostic finding not cluster truth | tests/diagnostic surfaces | diagnostic_run scopes | findings mutate truth | reveals operational boundary |
| Organism/Eye locality | supported but bounded | responsibility/locality | competency | Eye composition has local competence | report 009 | competency assemblers | organism universalized | reveals local branch |

### Authority / warrant local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Authority origin | supported | authority | source, responsibility | same request can lack grant | Book VIII | approval/request fields | request becomes authority | reveals origin coordinate |
| Authority zone | supported | authority + locality | scope | local vs external zone blocks same evidence | SQLite | authority_zone | zone erased | reveals locality structure |
| Scope binding | supported | authority/scope | standing | scope binding not approval for all acts | Book VIII | operator_authority_scope_binding | scope treated as blanket approval | bridges scope/authority |
| Warrant basis | supported | authority/provenance | evidence | mechanism fitness not operator authority | Book VII | warrant objects/results | fitness overpromoted | reveals basis coordinate |
| Preconditions/policy | supported as constraint relation | authority | act | passing constraint not complete authority | Book II/VII | validators | check == permission | relation/operator, not dimension |
| Authority mismatch/block | standing/relation | authority | standing | same content can be blocked by zone | SQLite | lawful_posture | mismatch treated as missing evidence | reveals relation coordinate |

### Scope / locality local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Responsibility locality | supported | scope + responsibility | authority | same claim within/outside family subject | Book IV, SQLite | responsibility_family/subject | all responsibilities global | reveals internal structure |
| Subject locality | supported | scope + identity | content | evidence can be irrelevant to subject | SQLite cases | observable_subject | subject drift | reveals content binding |
| Authority locality | supported | scope + authority | standing | local observation vs external admin blocks | Book VIII, SQLite | authority_zone | permission expands | reveals authority-scope coupling |
| Evidence/provenance locality | supported | scope + provenance | standing | source context and applicability vary | Book V, SQLite | context/applicability fields | support overapplied | reveals provenance local system |
| Inquiry locality | supported | scope + inquiry | content | question surface may not open inquiry | Book IV | inquiry/frontier objects | visibility becomes execution | reveals activation context |
| Observation-context locality | supported | scope + provenance | occurrence | observer-held evidence may not be preserved | Book V/007 | observation source/context | observation universalized | reveals evidence boundary |
| Preservation-horizon locality | supported bounded | scope + preservation | occurrence | process-local vs persisted record differ | 008, Book V/VI | event ledger/store | durability hidden | reveals preservation structure |
| Organism locality | supported bounded | scope + responsibility | competency | Eye/local competency not universal organism | 009 | composition objects | local organism universalized | reveals special branch |
| Host/process locality | supported implementation-only to bounded | scope + realization | occurrence | process return differs from persisted row | 008/010 | in-process refs/SQLite DB | host artifact becomes constitutional grammar | reveals realization compression |

### Occurrence / preservation local coordinates

| Local coordinate | Status | Parent | Neighboring dimensions | Independent variation | Recurrence | Host-language carrier | Local-only loss | Macro effect |
|---|---|---|---|---|---|---|---|---|
| Act occurrence | supported | occurrence | responsibility, authority | act may occur without every claimed effect | Book II/VII | executor call/events | result overclaims | reveals act boundary |
| Producer boundary occurrence | supported | occurrence + provenance | responsibility | live producer return vs direct construction | reports 006/008 | call context | artifact proves producer | reveals provenance bridge |
| Assertion-bearing branch occurrence | supported | occurrence + content | standing | branch may occur without external effect | Book II | code path/events | result construction conflated | reveals internal act structure |
| Result construction | supported | occurrence + content | identity | object may be constructed separately | Book I/II | dataclass ctor | construction as occurrence | reveals representation split |
| External effect | supported | occurrence | authority, evidence | provider response != independently verified effect | Book VII | tool result | response as fact | reveals verification need |
| Recording occurrence | supported | occurrence + preservation | responsibility | event record differs from act | Book V/VI/VII | ledger append | record as event truth | reveals recording boundary |
| Preserved record | supported | preservation | standing | record exists without truth | Book VI/SQLite | ledgers/rows | row == truth | reveals preservation coordinate |
| Persistent record | supported bounded | preservation | scope | process-local vs SQLite-backed | 008 | SQLiteEventLedger | durability over/understated | reveals horizon coordinate |
| Knowledge extraction occurrence | supported bounded | occurrence + standing | evidence | extraction not automatic fact truth | Book V | fact extraction functions | extraction hidden | reveals establishment path |
| Consumer uptake occurrence | supported bounded | occurrence + uptake | standing | consumer adoption may occur without upstream truth | reports 004-006 | consumer assembly | uptake as universal truth | reveals movement topology |

## Dimension independence results

- **Same assertion, different standing**: event and testimony records may carry a claim while fact standing remains absent or bounded; SQLite recorded changes can remain `not_established` while still supporting bounded examination.
- **Same evidence, different consumer authority**: evidence about the same family/subject can be local-observation admissible and external-admin blocked by authority-zone mismatch.
- **Same subject, different provenance**: recorded assertions and evidence can reference different provenance material; the SQLite conflict case preserves disagreement instead of allowing `COALESCE` to decide constitutional precedence.
- **Same provenance, different applicability**: represented provenance material can exist while applicability to the specific change or evidence remains unknown or mismatched.
- **Same representation, different occurrence standing**: direct construction of an artifact with identical fields lacks the live producer occurrence standing available from a witnessed owner return.
- **Same record, different preservation horizon**: process-local in-memory records, SQLite ledgers, and Book-preserved clauses differ in durability without changing the represented content.
- **Same selection artifact, different authorization standing**: selection can narrow candidates without granting execution or movement authority.
- **Same projection content, different source standing**: a view or cache can expose current understanding without becoming a constitutional source.

Falsification result: recurrence does not automatically prove independence. Some candidates, such as authority block and lawful posture, are better classified as standing/relation values inside authority and standing rather than separate macro dimensions. Acts, constraints, roads, lenses, projections, and movement failed as peer-dimension candidates because they require and operate over several dimensions.

## Cross-district recurrence results

| Macro family | Book recurrence | Investigation recurrence | Python realization | SQLite realization | Diagnostic/operator-facing recurrence | Strength |
|---|---|---|---|---|---|---|
| Identity | Books I-VIII | selection, uptake, occurrence, realization, SQLite | IDs, refs, dataclass objects, event IDs | row PKs/text IDs | diagnostic subjects/runs | strong |
| Content/assertion | Books I-VIII | testimony, support binding, grammar friction | payloads, result objects, fact claims | assertion text, query results | findings and reports | strong |
| Standing | Books I-VIII | uptake standing, occurrence, SQLite | status fields, validation results | standing CASE columns/status strings | pass/fail/warning, forbidden inferences | very strong |
| Source/provenance | Books I, IV-VII | uptake, realization, SQLite slices, friction | source and lineage fields | provenance refs/material/applicability | evidence reports | strong |
| Responsibility | Books I-II, IV-VIII | occurrence, realization, Eye locality | producer/consumer/executor boundaries | competency responsibility family/subject | diagnostic record scopes | strong |
| Authority/warrant | Books III-IV, VII-VIII | selection road, SQLite, realization | authority binding and proposals | authority_zone and blocked postures | mutates_cluster/record scope | strong |
| Scope/locality | Books I-VIII | Eye locality, SQLite friction | replay scope, local observations | local_observation/external_admin | diagnostic_run scope | strong |
| Occurrence/preservation | Books I-II, V-VII | occurrence survey, realization, SQLite friction | calls, ledgers, execution records | row existence/status/build scripts | recordable diagnostics | strong family |

## Variable activation profiles

Seed does not use one fixed-dimensional structure everywhere. It uses context-dependent dimensional activation: different subjects require different coordinates to be active, latent, irrelevant, unknown, or supplied by relation to another artifact.

Legend: **A** active, **L** latent, **I** irrelevant for the bounded question, **U** unknown/preserved as unknown, **R** supplied by relation to another artifact.

| Subject or process | Identity | Content | Standing | Provenance | Responsibility | Authority | Scope/locality | Occurrence/preservation | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Raw observation | A | A | L/U | A | R | L | A | U/R | Observer-held evidence may exist before preserved occurrence evidence. |
| Recorded assertion | A | A | A | R/U | R | L/U | A | A | Recording occurrence and assertion truth remain separate. |
| Evidence-bearing material | A | A | A | A | R | R/U | A | R | Evidence can support bounded examination without fact standing. |
| Bounded examination result | A | A | A | A/R | A | A | A | U/R | Lawful inactivity can be positive result; examination occurrence may remain unrecorded. |
| Selected capability/candidate | A | A | A | R | R | L/U | A | R/U | Selection standing does not authorize execution. |
| Authorized operation | A | A/R | A | R | A | A | A | L | Authority active before occurrence. |
| Execution result | A | A | A | R/U | A | A/R | A | A | Provider response does not verify external effect. |
| Recorded execution | A | A | A | A/R | A | A/R | A | A | Record preserves assertion of execution, not every represented effect. |
| Extracted knowledge/fact | A | A | A | A | A/R | R | A | A/R | Requires ingestion/support/normalization/conflict-aware establishment. |
| Projected current state | A | A | A | R | R | R/U | A | R | Projection exposes replayed understanding; not a new constitutional source. |

## Local expansion case studies

### Locality

- **Original coarse concept**: bounded/local scope.
- **Bounded question applying pressure**: Why can material be relevant for one competency, subject, authority zone, consumer, or host realization but not another?
- **Local coordinates recovered**: responsibility locality, subject locality, authority locality, evidence/provenance locality, inquiry locality, observation-context locality, preservation-horizon locality, organism locality, host/process locality.
- **Coordinates contradicted or unresolved**: host/process locality is implementation-evident but not constitutional destiny; organism locality is bounded to Eye/competency evidence; not every local label is a constitutional coordinate.
- **Implementation compression discovered**: Python object/module boundaries and SQLite text fields/authority zones can look like locality while omitting consumer purpose and preservation horizon.
- **Book grammar recovered**: boundedness is distributed across authority scope, examination, testimony, projection, and communication rather than one locality chapter.
- **Remaining topology question**: Which locality branches should be represented explicitly when material crosses producer-consumer boundaries?

### Provenance

- **Original coarse concept**: source/provenance.
- **Bounded question applying pressure**: Does a named reference, represented lineage, or source row establish support, verification, applicability, or producer occurrence?
- **Local coordinates recovered**: reference presence, referenced material existence, source attribution, source context, lineage representation, lineage applicability, internal coherence, independent verification, producer occurrence.
- **Coordinates contradicted or unresolved**: verified causation is not positively established by current SQLite witness; producer occurrence bridges provenance and occurrence rather than belonging solely to one.
- **Implementation compression discovered**: Python references and SQLite text/foreign references both collapse reference, material, applicability, verification, and causation unless compensated.
- **Book grammar recovered**: evidence identifies source/context; explanations expose reasons/conflicts; represented provenance does not become verified provenance.
- **Remaining topology question**: How should future records preserve disagreement between assertion-level and evidence-level provenance without imposing universal precedence?

### Identity

- **Original coarse concept**: identity.
- **Bounded question applying pressure**: Does object identity, row identity, selected name, source identity, or event identity identify the same constitutional subject?
- **Local coordinates recovered**: representation identity, subject identity, assertion identity, occurrence identity, source identity, responsibility identity, projection identity.
- **Coordinates contradicted or unresolved**: row identity and object identity are not constitutional identity by themselves; future multi-claim records may need assertion identity separate from change ID.
- **Implementation compression discovered**: Python object identity and SQLite row identity provide uniqueness but can hide producer, occurrence, subject, source, and projection distinctions.
- **Book grammar recovered**: artifact representation, act artifact, event, fact, projection, and authority grant are separate constitutional subjects.
- **Remaining topology question**: When does a local implementation key become a durable constitutional reference rather than an internal representation key?

### Standing

- **Original coarse concept**: status or establishedness.
- **Bounded question applying pressure**: What can a downstream consumer lawfully rely on when upstream producer occurrence, truth, or provenance is weaker?
- **Local coordinates recovered**: standing kind, standing reason, consumer-relative admissibility, reliance permission, movement permission, truth status, verification status, unknown reason, forbidden inference.
- **Coordinates contradicted or unresolved**: a universal standing enum is not supported; standing may be a macro family attached to every subject/relation rather than one peer dimension.
- **Implementation compression discovered**: booleans, enums, exceptions, CHECK constraints, and CASE results compress reasons and forbidden inferences unless explicit fields preserve them.
- **Book grammar recovered**: consumer-local establishment can coexist with weaker upstream standing; testimony and fact standing differ; lawful inactivity is positive.
- **Remaining topology question**: Which standing coordinates should be preserved generically, and which remain local to diagnostic, examination, or uptake surfaces?

### Occurrence

- **Original coarse concept**: happened/recorded.
- **Bounded question applying pressure**: Does representation existence, successful return, row insertion, or view evaluation prove a responsible act or external effect occurred?
- **Local coordinates recovered**: act occurrence, producer boundary occurrence, assertion-bearing branch occurrence, result construction, external effect, recording occurrence, preserved record, persistent record, knowledge extraction occurrence, consumer uptake occurrence.
- **Coordinates contradicted or unresolved**: occurrence and preservation are coupled but independently variable; view evaluation and query availability are not occurrence or uptake.
- **Implementation compression discovered**: Python method calls and SQLite statement/view evaluation compress call occurrence, responsible branch, result construction, record preservation, and consumer receipt.
- **Book grammar recovered**: boundary invocation, result construction, recording, external effect, and fact establishment are distinct.
- **Remaining topology question**: Whether occurrence/preservation should remain one macro family or split into occurrence and preservation macro families.

## Acts and constraints dimensional role

- **Act** is classified as an act/operator over dimensions, not a peer macro dimension. An act may change or preserve identity-bound records, standing, occurrence evidence, content, projection outputs, or authority posture. The same act type can operate across different dimensions: selection narrows identity/content candidates, recording changes preservation, execution produces occurrence/result records, examination changes standing/reason visibility, and communication changes handoff topology.
- **Constraint** is classified as constraint/operator. Constraints consume proposed acts or contexts and produce permission, prohibition, requirement, or condition. They limit coordinate transitions but are not themselves the dimension being limited. A single authority dimension can constrain execution, recording, projection reliance, fact establishment, and handoff. A single constraint can touch authority, scope, standing, provenance, and responsibility.
- **Movement** is classified as movement topology. Movement is lawful transition through constitutional state or standing. It depends on identity, scope, authority, responsibility, standing, occurrence, and preservation. It is not a universal sequence and not a peer coordinate.

## Roads, handoffs, and uptake dimensional role

Roads, handoffs, and uptake are best classified as movement topology and relations between dimension-bearing subjects. A road requires producer, artifact, consumer, purpose, warrant, authority, standing, scope, and often preservation. Consumer uptake can create local standing transitions without proving upstream truth or producer occurrence. Selection-road sufficiency and uptake reports support road/topology treatment rather than a separate road dimension.

Important preserved distinctions:

- selection artifact != act of selection
- selection standing != authorization standing
- consumer accepts artifact type != consumer lawfully relies on every assertion
- communication != establishment
- handoff != execution
- adapter participation != adapter owns uptake automatically

## Lenses / projections dimensional role

Lenses and projections are projection/lens operators. They select, expose, or recompose coordinates and may derive new assertion-bearing outputs. They do not automatically change upstream standing, establish truth, prove occurrence, or create authority. Projection can produce a current-state view with scope, freshness, and lineage, but the view/cache is not a new constitutional source of law.

Important preserved distinctions:

- lens != road
- projection != establishment
- view availability != occurrence
- composition != adjacency
- read model != underlying record
- cache freshness != truth

## Standing dimensional characterization

Standing is supported as a recurrent macro family, but not as a simple scalar dimension. It behaves as a coordinate family attached to constitutional subjects and relations. The strongest supported local coordinates are standing kind, standing reason, consumer-relative admissibility, reliance permission, movement permission, truth status, verification status, unknown reason, and forbidden inference.

Standing varies independently from content, identity, source, authority, and occurrence. The same claim can be recorded testimony, premise-relative input, consumer-local established result, or not-established fact. The same artifact can be locally accepted for a typed request while forbidden from broader reliance. The same provenance can be represented but not verified. The same execution result can be completed but not independently verify external effect.

Therefore standing is counted as one macro-dimensional family only with the warning that it is cross-cutting and locally activated.

## Occurrence / preservation characterization

Occurrence and preservation are supported as a recurrent macro family with unresolved internal split. Occurrence asks what happened at a responsible boundary. Preservation asks what record or evidence persists. They interact constantly but can vary independently:

- representation existence != responsible production
- record existence != represented occurrence truth
- observer-held occurrence evidence != preserved occurrence evidence
- live producer return != direct construction with identical fields
- view evaluation != recorded examination occurrence
- query result != consumer uptake
- batch or transaction != constitutional act

The bounded answer is that occurrence/preservation is a strong macro family for this survey, but future work may lawfully split it into occurrence and preservation if repository evidence demands finer macro separation.

## Host-language compression matrix

| Macro family | Python representation mechanism | SQLite representation mechanism | Python expresses naturally | SQLite expresses naturally | Python compresses | SQLite compresses | Compensating grammar | Book clause preserving distinction | Same deficit? |
|---|---|---|---|---|---|---|---|---|---|
| Identity | object identity, dataclasses, IDs, references | row PKs, text IDs, FKs/joins | in-process reference and object construction | unique rows and join keys | subject vs representation vs producer occurrence | row identity vs constitutional subject/occurrence | explicit IDs, type-specific refs, duplicate preservation | artifact/act/event/fact/projection separations | yes, via object vs row identity |
| Content/assertion | payloads, return values, result objects | assertion rows, query results, view columns | rich structured return values | deterministic relation/query content | return value vs effect/truth | query result vs fact/uptake | status/reason fields and forbidden inferences | testimony != fact; projection != source | yes, return/query result compression |
| Standing | enums, booleans, validation results, exceptions | CHECK constraints, status columns, CASE views | local validation and result postures | constrained strings and deterministic posture derivation | reason and scope behind status | mechanical validity vs constitutional standing | explicit standing_reason, unknown statuses, forbidden inference | standing is not artifact field | yes, status compression |
| Source/provenance | in-process refs, source fields, lineage objects | text references, optional FKs, LEFT JOIN, COALESCE | direct object linkage | reference storage and joins | reference vs material vs verified lineage | reference presence vs material/applicability/verification | separate provenance material, applicability, conflict preservation | evidence/provenance/explanation clauses | yes, references compress provenance |
| Responsibility | owner methods, executors, recorders, consumers | responsibility_family/subject columns | callable ownership and call context | explicit competency boundaries | module/callable ownership vs responsibility | row family/subject vs producer/consumer boundary | producer/consumer clauses, diagnostic scopes | constructors and production authority; acts | yes, host owner compresses responsibility |
| Authority/warrant | authority binding objects, proposal checks | authority_zone, CASE blocking | procedural checks before calls | zone equality/mismatch | approval, warrant, policy, precondition | zone string vs grant/warrant | authority scope binding, blocked postures | authority scope and warrant chapters | yes, authorization compressed into local checks |
| Scope/locality | replay scope, local observations, function context | local_observation/external_admin strings, DB fixture scope | process/request-local context | bounded fixture domains | process locality vs constitutional locality | column value vs purpose/consumer/horizon | bounded clauses, purpose fields, record_scope | bounded examination and authority scope | yes, local context compressed |
| Occurrence/preservation | method call, constructor, event ledger append, SQLiteEventLedger | INSERTs, database build, view evaluation, persisted rows | call occurrence and in-memory causality | durable row persistence and deterministic views | call vs branch vs result vs record | row/view/transaction vs act/uptake | event records, occurrence statuses, verification scripts | acts, recording, events/facts/state | yes, host execution compresses occurrence |

## Shared Python-SQLite dimensional deficits

| Pair tested | Supported shared deficit? | Finding |
|---|---:|---|
| Python object identity vs SQLite row identity | yes | Both naturally establish host identity but not constitutional subject, standing, source, or occurrence identity. |
| Python `None` vs SQLite `NULL` | partial | Both can represent absence/unknown mechanically; Seed unknown requires a bounded standing reason. SQLite 010 explicitly refuses a universal absence taxonomy. Python evidence is broad but not identical. |
| Method call vs SQL view evaluation | yes | Both can be mistaken for constitutional occurrence; method call has stronger occurrence context than view availability, but neither automatically proves all represented claims. |
| Constructor validation vs CHECK constraints | yes | Both mechanically validate shape/values and can reject malformed representation; neither supplies full producer authority, refusal reason, or constitutional standing. |
| Call topology vs join topology | yes | Both express host relations that can be mistaken for constitutional road, lineage, or causation. Explicit applicability and responsibility are needed. |
| Return value vs query result | yes | Both carry content without independently establishing truth, external effect, or consumer uptake. |
| In-process reference vs foreign/text reference | yes | Both collapse reference presence, target existence, applicability, and verification unless separated. |
| Batch or transaction vs constitutional act | yes | Both provide host execution grouping but not one constitutional act unless responsible occurrence, authority, scope, and record are represented. |
| Exception vs rejected statement | partial | Both can indicate mechanical failure/block; constitutional refusal requires bounded reason, authority/policy context, and non-performance standing. |

Hypothesis E is supported at the family level with caution: Python and SQLite independently compress many of the same Seed-native distinctions, but not always in exactly analogous ways. The survey does not claim a one-to-one host-language equivalence.

## Candidate Seed-native dimensions

Strongly supported candidate Seed-native macro-dimensional families:

1. subject / identity
2. assertion / content
3. standing
4. source / provenance
5. responsibility
6. authority / warrant
7. scope / locality
8. occurrence / preservation

Candidate families requiring caution or split pressure:

- standing may be cross-cutting rather than one peer axis;
- occurrence / preservation may split under future pressure;
- source / provenance includes producer occurrence only as a neighboring bridge, not as a simple subfield;
- scope / locality contains many local coordinate systems, not all equally established.

Candidates rejected as peer macro dimensions in this survey:

- act: act/operator over coordinates;
- constraint: constraint/operator limiting transitions;
- road/handoff/uptake: movement topology and consumer-relative relation;
- lens/projection: projection/lens operator;
- composition: bounded assembly/operator;
- movement: topology of lawful transition;
- authority blocked, unknown preserved, selected, established, verified: standings or values rather than dimensions;
- table columns, class attributes, primary keys, enum names: implementation mechanisms unless supported by constitutional distinctions.

## Hypothesis testing and falsification

### Hypothesis A — approximately eight macro dimensions

Supported with bounded confidence. The repository currently exhibits approximately eight recurrent macro-dimensional families. The model is useful, but not exact: standing is cross-cutting, occurrence/preservation may split, and several candidates are topology/operators rather than dimensions.

### Hypothesis B — locally expanding dimensionality

Supported. Locality, provenance, identity, standing, and occurrence all unfold into bounded coordinate systems under local questions. The expansion is evidence-controlled, not universal schema expansion.

### Hypothesis C — variable dimensional activation

Supported. Raw observations, recorded assertions, evidence, examination results, selected capabilities, authorized operations, execution results, recorded executions, extracted knowledge, and projections activate different coordinates. Seed does not currently use one fixed-dimensional structure everywhere.

### Hypothesis D — relational and transformational topology

Mostly supported. Acts, constraints, roads, handoffs, uptake, lenses, projections, composition, and movement operate over dimensions or relate dimension-bearing subjects. They should not be casually counted as peer dimensions. Projection may derive new assertion-bearing outputs, but that does not make projection itself a macro dimension.

### Hypothesis E — shared host-language dimensional deficit

Supported with caution. Python and SQLite independently compress identity, standing, provenance, authority, locality, occurrence, and content distinctions. The deficits recur, but analogies must remain bounded because Python call context and SQLite relational evaluation differ.

### Falsification burdens recorded

- **Every candidate macro dimension varies independently**: partially falsified; authority-blocked, selected, verified, and established are better treated as standings/values under larger families.
- **Every local distinction belongs to one parent dimension**: falsified; producer occurrence, consumer uptake, and authority scope bridge neighboring dimensions.
- **Acts and constraints are operators rather than dimensions**: supported, not falsified by current evidence.
- **Roads are topology rather than dimensions**: supported.
- **Standing is one macro dimension**: supported only as a macro family; falsified as a simple scalar.
- **Occurrence and preservation form one family**: supported for this survey but split pressure remains unresolved.
- **Python and SQLite compress the same dimensions**: supported at family level; exact equivalence falsified.
- **Local dimensional expansion is reusable outside the district discovered**: partially supported; provenance/locality/standing recur broadly, but host/process and organism locality remain bounded.

## Codex local-to-global orientation rule

Future Codex investigations should use this bounded operating rule:

> Investigate one local constitutional boundary at a time. For every recovered distinction, project it back into its parent macro family, neighboring dimensions, and city-level topology. Preserve local surgical precision without converting local implementation structure into universal constitutional grammar. Preserve global constitutional orientation without allowing a macro map to prescribe the seam before repository evidence is examined. Classify acts, constraints, roads, lenses, projections, composition, standings, values, relations, and implementation fields before calling them dimensions.

This rule preserves both local resolution and global orientation. It also protects against two recurring errors: expanding local fixture structure into a universal schema, and using global dimension maps to erase locally meaningful unknowns, consumer-relative standings, or host-language deficits.

## Book implications

- The dimensional survey should remain an orientation artifact for now.
- No new “dimension” Book should be created.
- The eight Book districts already approximate major constitutional districts but do not map one-to-one to dimensions. They mix dimensions, operators, kinds, relations, and movement topology.
- A small Book clause for local-to-global projection may eventually be useful, but this survey did not make a canonical Book change because the current evidence is better preserved as an orientation report rather than a realization-independent constitutional law.
- Book chapter organization should not be reorganized by this survey.

## Claims supported

- Seed currently exhibits approximately eight recurrent macro-dimensional families.
- Macro families unfold into local coordinate systems under bounded constitutional questions.
- Standing is recurrent and cross-cutting, not a simple linear scale.
- Provenance unfolds into reference, material, attribution, applicability, verification, coherence, and occurrence-adjacent questions.
- Locality unfolds into responsibility, subject, authority, inquiry, evidence/provenance, observation-context, preservation-horizon, organism, and host/process branches with varying confidence.
- Identity unfolds beyond object/row identity into subject, assertion, occurrence, source, responsibility, and projection identities.
- Occurrence/preservation has many local coordinates and is not proved by representation existence.
- Acts, constraints, roads, lenses, projections, composition, and movement operate over or among dimensions.
- Python and SQLite independently compress many Seed-native dimensions.

## Claims contradicted

- A field, class attribute, table column, row key, enum, or status string is automatically a constitutional coordinate.
- Book chapter equals dimension.
- Selection equals authorization.
- Projection equals establishment.
- View availability equals occurrence.
- Construction equals producer occurrence.
- Record existence equals represented truth.
- Reference presence equals referenced material existence or applicability.
- Represented provenance equals verified provenance or verified causation.
- Consumer uptake proves upstream truth automatically.
- Movement is a universal pipeline.
- Local expansion implies infinite or universal dimensionality.

## Claims remaining unresolved

- Whether occurrence and preservation should be split into two macro dimensions.
- Whether standing should be represented as a peer macro family or as a coordinate family attached to all subjects and relations.
- Which locality branches deserve stable Book-level names beyond the current bounded reports.
- Whether producer occurrence belongs primarily to provenance, occurrence, responsibility, or a bridge relation.
- How future implementations should represent consumer uptake occurrence without overpromoting local reliance.
- Whether a general bounded competency declaration should become a canonical Book kind.
- Which standing vocabularies should become durable enums and which remain local posture strings.

## Estimated macro-dimension count

The repository supports **approximately eight recurrent macro-dimensional families**:

1. subject / identity
2. assertion / content
3. standing
4. source / provenance
5. responsibility
6. authority / warrant
7. scope / locality
8. occurrence / preservation

This count is approximate and bounded. It is not a mathematical proof, a final ontology, a universal schema, or a prescription for implementation fields.

## Estimated recurring local-coordinate count

Evidence supports **roughly sixty recurring or boundedly supported local coordinates** across the eight families if coordinates are counted conservatively from the local systems above. That number is intentionally approximate because some coordinates bridge families, some are values or standings, and some are implementation-only or unresolved. The stronger result is nested dimensionality, not exact cardinality.

## Files changed

- Created `book_of_seed/repository_constitutional_dimensionality_survey_011.md`.

## Verification or validation performed

- `git rev-parse HEAD`
- `git status --short`
- `git log --oneline --decorate -n 20`
- `find book_of_seed -maxdepth 2 -type f | sort`
- `find witnesses -maxdepth 3 -type f | sort`
- `rg` searches over Book, runtime, tests, and witness districts for PR 1753 and dimensional evidence.
- `bash witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh`
- `python -m pytest -q tests/test_documentation_structure.py`

## Bounded resolution

Seed currently exhibits approximately eight recurrent macro-dimensional families, each unfolding into locally activated coordinates. The repository also supports nested dimensionality but not an exact dimensional count. Several apparent dimensions are better classified as standings, values, acts, constraints, relations, operators, projections, composition, or movement topology. The report remains an orientation artifact, not a final ontology.
