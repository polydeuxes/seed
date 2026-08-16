# Constitutional Evidence Consumer District Survey 001

## completed evidence consumed

This survey consumes the completed constitutional uptake frontier investigation and the applicability/admission/consumption projection as settled grammar. It does not reinvestigate the grammar that material applicable to a consumer, material admitted to a consumer, and material consumed by a consumer are distinct. It also treats constitutional uptake as responsibility-local: uptake begins only when a consumer gives upstream material bounded constitutional use or produces a consumer-local assertion materially dependent on that material.

Implementation evidence reviewed for the runtime district included:

- `seed_runtime/evidence.py`
- `seed_runtime/observations.py`
- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/confidence.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/context_views.py`
- `seed_runtime/explanations.py`
- `seed_runtime/correlation_audit.py`
- `seed_runtime/closed_choice_selection_binding.py`
- `tests/test_observation_sources.py`
- `tests/test_runtime_loop.py`
- `tests/test_knowledge_reachability.py`

Application surfaces used for orientation, not as sole authority, were:

```text
python -m scripts.seed_local --projected-state-consumers
python -m scripts.seed_local --consumer-audit
```

## bounded survey question

Where does an actual Seed `Evidence` artifact, preserved evidence record, evidence observation, or resolved evidence reference first cross from available represented material into consumer-local applicability, admission, and use for each serious consuming responsibility in the current runtime district?

The survey remains bounded to runtime Evidence consumers. It does not implement a recovery slice, central evidence router, universal admission engine, mandatory evidence pipeline, or Book repetition.

## Evidence boundary used

Included material had to be one of:

- canonical `Evidence` objects stored or replayed as evidence records;
- observation-derived evidence records;
- `Fact.evidence_ids` whose represented material is resolved against `State.evidence`, or whose absence is explicitly represented as a compressed reference;
- bounded fact-support artifacts that carry preserved fact lineage;
- testimony objects explicitly carrying evidence standing.

Rejected as sufficient by itself:

- arbitrary fields named `evidence`;
- prose source text;
- fact rows with no evidence lineage;
- rendered summaries of evidence;
- provenance strings without a resolved evidence material boundary;
- support IDs whose material is never resolved;
- tests that merely construct values;
- comments or reports using generic evidence vocabulary.

## implementation neighborhoods inspected

The serious neighborhoods found by implementation evidence are:

1. Observation ingestion and fact establishment.
2. State projection and fact-support/current-belief establishment.
3. Evidence graph construction.
4. Confidence and contradiction projection.
5. Decision context selection.
6. Explanation/why views.
7. Diagnostic correlation/consumer exposure.
8. Closed-choice selection binding and inquiry-like testimony surfaces.

The app-facing projected-state and consumer audits confirmed broad projected-state, diagnostic, and view consumers, but they do not by themselves prove constitutional Evidence uptake; they are orientation only.

## candidate relationships rejected

- Diagnostic inventory rows are not Evidence consumption merely because they declare surfaces, flags, record support, or mutation boundaries.
- `--projected-state-consumers` output is transport/exposure of consumer names and source classes, not proof that each consumer admits Evidence material.
- `consumer_audit` dependency rows expose reuse and orphaning relationships; they do not resolve evidence material into admission or use.
- `Fact.evidence_ids` alone are not treated as resolved Evidence consumption unless the consumer resolves them through `State.evidence` or explicitly preserves the missing reference compression.
- `ContextFact.evidence_count` is a summary count, not an Evidence artifact.
- Explanation prose such as “Seed believes this fact because ...” is presentation over support, not producer occurrence.
- Inquiry and selection tests that construct `NeedFocusEvidence`, `EvidenceSnapshotReference`, or support text were excluded unless the implementation explicitly carries evidence standing or validates evidence-bearing coordinates.

## per-neighborhood topology

### 1. Observation ingestion and fact establishment

**Classification:** mature uptake neighborhood.

**Fidelity:** faithful within scope.

**Responsibility-local purpose:** convert a canonical `Observation` into a preserved `Evidence` record and, unless bounded suppression applies, into an observed `Fact` whose evidence lineage points to that evidence.

**Upstream Evidence material:** `ObservationIngestor.observation_to_evidence(...)` produces an `Evidence` object with `source`, `kind`, `observed_at`, payload coordinates, and confidence copied from the observation. The ingestor then passes that actual object to `observation_to_fact(...)`, which creates a `Fact` with `evidence_ids=[evidence.id]`.

**Producer/preservation boundary:** `ingest_many(...)` emits `observation.observed`, `evidence.observed`, and optional `fact.observed`/`fact.inferred` events in the same batch. This is both producer and preservation boundary.

**Consumer boundary:** `observation_to_fact(...)` is the first fact-establishment consumer. It consumes the newly produced Evidence artifact by identity, not by prose.

**Applicability:** bounded by the observation-to-fact responsibility. The material coordinates required are observation subject, predicate, value, dimensions, source type, observed time, confidence, and suppression metadata. The fact-establishment consumer validates confidence range through `Observation.__init__`, preserves metadata in Evidence payload, and recognizes a bounded suppression case through `_should_suppress_fact_promotion(...)`.

**Admission:** admission occurs when `observation_to_fact(...)` accepts the generated Evidence object as support for a Fact. If suppression applies, evidence is preserved and fact admission/use is refused.

**Consumption:** actual use occurs when the Fact is produced with `evidence_ids=[evidence.id]`; downstream standing is an observed or inferred Fact, not a direct promotion of Evidence into truth.

**Coordinates validated:** identity (`evidence.id`), content (subject/predicate/value/dimensions), provenance/source (`source_type`, metadata, observed_at), standing (`kind="observation"`, confidence), occurrence/preservation (events), bounded responsibility (fact establishment), scope (workspace id). Authority is source-type/confidence-bounded rather than inherited as truth.

**Coordinates compressed or absent:** conflict is not evaluated here; it belongs downstream. Admission is implemented in the conversion boundary rather than as a named admission object.

**Refusal/Unknown/conflict behavior:** bounded refusal is visible in Prometheus `node_uname_info` OS suppression: Evidence is recorded but fact promotion is suppressed. Unknown is preserved by absence of a Fact rather than repaired. Conflict is absent here by responsibility.

**Authority and scope:** authority remains observation/fact-support authority only; no cluster mutation authority is created.

**Producer occurrence:** producer occurrence is preserved as observation/evidence event occurrence and observed_at, but the consumer does not inherit producer occurrence as its own occurrence beyond the recorded fact event.

**Tests/diagnostics:** `tests/test_observation_sources.py` proves provider/imported observation evidence payload preservation and suppression without fact promotion; `tests/test_runtime_loop.py` proves tool output evidence projection.

### 2. State projection and fact-support/current-belief establishment

**Classification:** mature uptake neighborhood.

**Fidelity:** faithful within scope.

**Responsibility-local purpose:** replay preserved evidence and fact events into `State`, then establish bounded `FactSupport`, current samples, aggregate support, aliases, conflicts, graph issues, and current fact views without rewriting event authority.

**Upstream Evidence material:** preserved `evidence.observed` event payloads become `State.evidence`; `Fact.evidence_ids` remain lineage; `FactSupport` consumes facts and their evidence-linked lineage through supporting fact IDs.

**Producer/preservation boundary:** `StateProjector` decodes `evidence.observed` events into `Evidence` objects stored in `state.evidence`, and `fact.observed`/`fact.inferred` events into facts.

**Consumer boundary:** `_project_fact_supports(...)`, `State.get_fact_supports(...)`, alias resolution, relationship projection, and conflict projection consume facts that carry evidence lineage. The first admission for current-belief support is grouping non-expired facts into a `FactSupport` record.

**Applicability:** material applicability is predicate/subject/value/dimension/local-expiry bounded. Measurement predicates are applicable to current-sample support; durable predicates are applicable to aggregate support. Expired facts are inapplicable to default support unless `include_expired=True`.

**Admission:** admission occurs when non-expired facts are grouped into support rows and either aggregated or selected as current sample. Measurement admission is latest-sample admission; durable admission is aggregate admission.

**Consumption:** use occurs in producing `FactSupport` rows with supporting fact IDs, source types, confidence, observed/latest timestamps, expiry, predicate semantics, and support kind. Downstream standing is current-belief support, not Evidence truth.

**Coordinates validated:** identity (fact IDs and support keys), content (subject/predicate/value/dimensions), responsibility (support projection), scope (subject and dimensions; alias-resolved methods where requested), occurrence (observed/latest timestamps), standing (confidence/source types), preservation (supporting fact IDs).

**Coordinates compressed or absent:** Evidence object resolution is not required for `_project_fact_supports(...)`; it admits fact lineage, not canonical Evidence payloads. Authority remains compressed into source type/confidence and catalog semantics.

**Refusal/Unknown/conflict behavior:** expired facts can be refused; measurement history is not aggregated as durable truth; ties and ambiguity are preserved through no single best support and conflict structures rather than repaired.

**Authority and scope:** support projection does not mutate events or facts. It scopes by subject, predicate, dimensions, and predicate semantics.

**Producer occurrence:** support records preserve source fact occurrence times without treating the producer occurrence as consumer occurrence; support has its own observed/latest range.

**Tests/diagnostics:** observation source tests cover aggregation/current-sample support counts, duplicate support, and suppressed fact projection.

### 3. Evidence graph construction

**Classification:** compressed uptake neighborhood.

**Fidelity:** faithful within scope.

**Responsibility-local purpose:** expose a read-only graph view linking facts to evidence nodes and support links for downstream contradiction, confidence, context, and explanation consumers.

**Upstream Evidence material:** resolved `State.evidence` entries referenced by `Fact.evidence_ids`; unresolved fact evidence IDs are represented as `_node_from_fact_reference(...)`; fact-support-derived supporting facts can bring their evidence IDs into the view; inferred facts with no evidence but a source fact can produce a projection node.

**Producer/preservation boundary:** projected `State` is the producer/preservation boundary. Evidence Graph does not persist a separate database.

**Consumer boundary:** `_nodes_for_fact(...)` is the first crossing: a fact's evidence IDs are resolved against `State.evidence` when possible, otherwise compressed into a fact-reference node.

**Applicability:** applicability is fact-local: only evidence IDs attached to the target fact or to supporting facts selected by matching `FactSupport` are applicable to that graph view. This is not generic evidence availability.

**Admission:** admission is compressed into graph node construction. If the ID resolves to an `Evidence`, the node receives type, summary, source event/run, confidence, and created_at from that Evidence. If unresolved, the graph admits a weaker represented reference node rather than rejecting or claiming resolution.

**Consumption:** use occurs when the graph emits `EvidenceNode`, `EvidenceLink(relationship="supports")`, and `FactEvidenceView` records. Downstream standing is graph support visibility.

**Coordinates validated:** resolved identity, content summary, evidence kind/source type, confidence, created_at, source event/run when payload supports it, relationship target fact.

**Coordinates compressed:** applicability collapsed into node/link construction; admission collapsed into view construction; unresolved evidence references are admitted as represented fact-reference nodes with compressed standing; relationship vocabulary is fixed to support links, not a full authority analysis.

**Refusal/Unknown/conflict behavior:** unsupported facts produce an explanation that projected State has the fact but no linked supporting evidence. Unresolved references are not repaired; they are represented as weaker nodes. Conflict is absent here and delegated downstream.

**Authority and scope:** read-only graph support authority only. It does not claim truth, resolve conflicts, execute tools, call providers, mutate facts, or persist a parallel store.

**Producer occurrence:** source event/run are derived from Evidence payload keys where available; otherwise source_event_id falls back to the evidence id. Producer occurrence is represented, sometimes compressed, not consumer occurrence.

**Tests/diagnostics:** evidence graph behavior is exercised indirectly through context, confidence, contradiction, unsupported-fact, and runtime-loop tests.

### 4. Confidence and contradiction projection

**Classification:** compressed uptake neighborhood.

**Fidelity:** faithful within scope.

**Responsibility-local purpose:** derive read-only contradiction and confidence records from projected facts and the Evidence Graph.

**Upstream Evidence material:** `FactEvidenceView` objects from the graph; each view may contain resolved Evidence nodes, compressed fact-reference nodes, and supporting event IDs.

**Producer/preservation boundary:** Evidence Graph and projected State are the producer boundary.

**Consumer boundary:** `build_contradictions(...)` maps `graph.fact_evidence` into `evidence_by_fact_id`; `build_fact_confidences(...)` maps the same graph views into support counts and supporting event IDs.

**Applicability:** contradiction applicability is exact subject/predicate with exclusive predicate membership. Confidence applicability is per projected Fact. Evidence material is applicable only as support count/supporting event lineage for that fact.

**Admission:** admission is compressed: confidence admits support by count, not by inspecting each Evidence coordinate; contradiction admits attached evidence views for conflicting fact IDs.

**Consumption:** confidence consumes support counts to compute confidence, unsupported flags, reasons, and contradiction penalties. Contradiction consumes attached evidence views to preserve evidence_by_fact_id and supporting event IDs for conflict visibility.

**Coordinates validated:** fact identity, subject, predicate, value, exclusive predicate scope for contradictions, support count, contradiction count, supporting event lineage.

**Coordinates compressed:** Evidence content, authority, occurrence, and scope are inherited through `FactEvidenceView`; admission is collapsed into count/evidence-view presence; evidence standing is not revalidated locally.

**Refusal/Unknown/conflict behavior:** unsupported can remain unsupported; explicit confidence without linked evidence is stated as such; contradictions reduce confidence and preserve reasons without resolving truth.

**Authority and scope:** read-only projection authority. Confidence estimates support strength; contradiction reports conflict. Neither mutates facts nor promotes admitted evidence to truth.

**Producer occurrence:** supporting event IDs are carried forward; producer occurrence is not recast as confidence occurrence.

**Tests/diagnostics:** tests around unsupported facts, contradictions, confidence facts, and decision context expose this relation.

### 5. Decision context selection

**Classification:** compressed uptake neighborhood.

**Fidelity:** faithful within scope.

**Responsibility-local purpose:** build a deterministic provider context from State, Evidence Graph, contradictions, and confidence aggregation while excluding unsupported facts by default and preserving contradiction flags.

**Upstream Evidence material:** `FactConfidence.support_count` and `supporting_event_ids` derived from graph views, not raw Evidence objects. The represented Evidence material has already been consumed by Evidence Graph and Confidence.

**Producer/preservation boundary:** confidence aggregation, contradiction detection, and evidence graph are upstream producers.

**Consumer boundary:** `select_context_facts(...)` admits or refuses facts into `ContextFact` based on unsupported status and `include_unsupported`.

**Applicability:** applicability is decision-context bounded: a fact-confidence row is applicable if it represents a fact available to context selection and either is supported or the caller explicitly includes unsupported facts.

**Admission:** admission is the selected `ContextFact` row. Unsupported facts are refused by default.

**Consumption:** use occurs when selected facts become provider-context facts with confidence, contradiction flag, and evidence count.

**Coordinates validated:** fact identity, subject, predicate, object, confidence, contradiction flag, support count, context inclusion option.

**Coordinates compressed:** actual Evidence identities and source events are compressed to `evidence_count`; admission consumes confidence rows rather than Evidence objects; authority and occurrence details are not materially needed for this surface's minimal context purpose but are hidden.

**Refusal/Unknown/conflict behavior:** unsupported is refused by default; contradicted facts are retained and marked; unsupported can be intentionally included by option.

**Authority and scope:** context authority is provider-context composition only. It does not assert truth or mutate State.

**Producer occurrence:** occurrence is absent from `ContextFact`; no producer occurrence is inherited.

**Tests/diagnostics:** decision-context tests expose supported/unsupported and contradiction behavior.

### 6. Explanation / why views

**Classification:** mature uptake neighborhood.

**Fidelity:** faithful within scope.

**Responsibility-local purpose:** answer why a current or ambiguous belief appears by traversing projected support, evidence IDs, source types, conflicts, inferred source facts, and alias resolution.

**Upstream Evidence material:** `FactSupport.supporting_fact_ids`; each supporting Fact's `evidence_ids`; optional recursive `source_fact_id`; `FactConflict` where present.

**Producer/preservation boundary:** projected State and support/conflict projections.

**Consumer boundary:** `ExplanationBuilder._explain_support(...)` resolves supporting facts and collects sorted evidence IDs from those facts. `_explain_fact(...)` recursively preserves source fact and inference rule lineage.

**Applicability:** support rows for the queried subject/predicate are applicable. Multi-valued predicates admit all supports; single-valued predicates use best support when unique and preserve competing supports/conflict when not unique.

**Admission:** admission occurs when support rows are turned into `BeliefExplanation` objects and their facts into `FactExplanation` objects. Expired facts are refused in `_explain_support(...)`.

**Consumption:** use occurs in producing `Explanation` standing: current, ambiguous, or no_current_belief with current/competing beliefs, evidence IDs, source types, recursive facts, conflict, and entity-resolution path.

**Coordinates validated:** query responsibility and predicate, support identity, fact identity, evidence IDs, source type, observed time, confidence, inference rule/source fact lineage, alias-resolution path, conflict status.

**Coordinates compressed or absent:** it does not resolve Evidence payloads itself; it consumes evidence IDs from admitted facts. That is acceptable within why-view scope because its local purpose is explanation over projected provenance, not evidence-payload auditing.

**Refusal/Unknown/conflict behavior:** no support returns no_current_belief; ambiguous supports remain competing beliefs; conflict is preserved; expired facts are excluded from support explanation.

**Authority and scope:** explanation authority is explanatory/provenance authority only. It does not convert explanation into truth or producer occurrence.

**Producer occurrence:** observed_at and recursive source_fact_id are preserved; explanation occurrence is separate from source occurrence.

**Tests/diagnostics:** `--why`, `--why-fact`, fact-support, contradiction, and explanation tests expose this consumer.

### 7. Diagnostic correlation / consumer exposure

**Classification:** transport / exposure only.

**Fidelity:** not classified under Fidelity because no mature/compressed/unfaithful uptake is established.

**Responsibility-local purpose:** expose read-only diagnostic relationships among operational evidence, consumers, pressure, and projected-state surfaces.

**Upstream Evidence material:** diagnostic rows often contain `evidence_present` dictionaries, implementation-source observations, inventory declarations, or consumer dependency rows. Some are evidence-shaped, but many are not canonical Evidence artifacts or resolved evidence records.

**Producer/preservation boundary:** repository files, static registries, projected-state consumers, and diagnostic inventories.

**Consumer boundary:** correlation and consumer audit builders render findings, counts, and lists. They do not give actual Seed Evidence artifacts bounded constitutional use.

**Applicability/admission/consumption:** absent for actual Evidence uptake. The boundary stores, formats, links, and exposes availability. It may identify disconnects, but it does not admit an Evidence artifact into a downstream truth/support standing.

**Coordinates represented:** diagnostic item identity, source class, consumer names, read-only/no-record/no-mutation boundaries, counts.

**Coordinates absent:** resolved Evidence identity/content/standing, consumer-local Evidence admission, Evidence-backed downstream assertion.

**Refusal/Unknown/conflict behavior:** diagnostics can report orphaned, mismatch, warning, or unknown states, but those are diagnostic statuses, not Evidence admission results.

**Authority and scope:** read-only diagnostic authority. No cluster mutation and no truth promotion.

**Producer occurrence:** absent or diagnostic-run scoped where recordable diagnostics apply.

**Tests/diagnostics:** `python -m scripts.seed_local --projected-state-consumers` and `python -m scripts.seed_local --consumer-audit` expose this transport-only district.

### 8. Closed-choice selection binding and testimony-like inquiry surfaces

**Classification:** Unknown for actual Evidence district uptake.

**Fidelity:** Unknown.

**Responsibility-local purpose:** bind closed-choice selection, unknowns, conflicts, and unsupported evidence references; inquiry tests also preserve focus/testimony references and evidence territory distinctions.

**Upstream Evidence material:** fields such as `unsupported_selection_evidence`, `unknown_selection_evidence`, `conflicting_selection_evidence`, `NeedFocusEvidence.evidence_ref`, and `EvidenceSnapshotReference` can explicitly carry evidence standing or evidence-reference vocabulary.

**Producer/preservation boundary:** local selection/testimony constructors and tests.

**Consumer boundary:** selection binding composes unsupported, unknown, and conflicting evidence references into refusal/selection results; inquiry testimony tests distinguish visible evidence refs from eligible evidence territory refs.

**Applicability/admission/consumption:** repository evidence proves preservation of evidence-reference distinctions and refusal categories, but in the inspected implementation it does not prove that represented references are resolved to actual Evidence material before admission or use. Therefore actual Evidence uptake remains Unknown rather than counted as mature or compressed.

**Coordinates represented:** reference identity, unsupported/unknown/conflict category, selection reason, visible versus eligible territory, family disposition, evidence currency/availability.

**Coordinates missing for this survey:** resolved Evidence material, producer occurrence of the referenced evidence, local admission boundary from resolved evidence to selection standing.

**Refusal/Unknown/conflict behavior:** strong representation of refusal/Unknown/conflict vocabulary exists. Actual Evidence conflict handling cannot be proven without resolved material.

**Authority and scope:** local selection/testimony scope is represented; evidence authority remains Unknown.

**Producer occurrence:** unknown for actual Evidence because references are not resolved in the inspected relationship.

**Tests/diagnostics:** tests prove reference and testimony distinctions, including visible evidence not automatically becoming eligible territory, but not resolved Evidence consumption.

## per-neighborhood coordinate analysis

| neighborhood | materially required coordinates | validated | preserved as testimony/representation | compressed/missing |
| --- | --- | --- | --- | --- |
| Observation ingestion / fact establishment | identity, content, provenance, standing, responsibility, scope, occurrence | observation confidence, content, dimensions, source type, workspace, evidence id | metadata and event payload | conflict absent by scope; admission named only by conversion |
| State projection / fact support | identity, content, responsibility, scope, occurrence, standing | non-expiry, predicate semantics, subject/predicate/value/dimensions grouping | supporting fact IDs, source types, timestamps | canonical Evidence payload resolution not needed locally; authority compressed |
| Evidence graph | identity, content summary, standing, provenance, occurrence | resolved Evidence entries where present | unresolved references as fact-reference nodes | applicability/admission collapsed into node construction |
| Confidence / contradiction | identity, content, conflict scope, support count | exclusive predicate, subject/predicate/value grouping, support count | supporting event IDs, reasons | Evidence coordinates compressed to graph view/count |
| Decision context | identity, confidence, contradiction, support count, selection scope | unsupported exclusion by default, contradiction flag retained | evidence_count | Evidence identities/source occurrence hidden |
| Explanation / why | query responsibility, fact/support identity, evidence IDs, source, occurrence, inference lineage, conflict | support selection, expired refusal, recursive source fact traversal, alias path | evidence IDs and conflicts | Evidence payloads not resolved by explanation itself |
| Diagnostic exposure | diagnostic identity, source class, consumer names | read-only/no-mutation declarations | evidence_present dictionaries | actual Evidence uptake absent |
| Closed-choice/testimony | reference identity, unknown/conflict/refusal category, local scope | category preservation | focus/testimony/evidence territory refs | actual Evidence resolution Unknown |

## applicability findings

- Observation ingestion has a bounded applicability boundary: observation-shaped material becomes applicable to fact establishment only when it can produce a valid Evidence object and is not in the suppressed fact-promotion case.
- Fact support has predicate/expiry/subject/dimension applicability and treats measurement predicates differently from durable predicates.
- Evidence Graph has fact-local applicability: only evidence linked through a target fact or supporting fact is applicable to that view.
- Confidence and contradiction have per-fact and exact exclusive-predicate applicability, respectively.
- Decision context has context-selection applicability and refuses unsupported facts by default.
- Explanation has query-bounded support applicability.
- Diagnostic and closed-choice/testimony surfaces either expose availability or preserve references without proving resolved Evidence applicability.

## admission findings

- First clear Evidence admission into fact establishment occurs at `observation_to_fact(observation, evidence)`.
- First support admission occurs in `_project_fact_supports(...)` when non-expired facts are admitted into aggregate/current-sample support.
- First graph admission occurs in `_nodes_for_fact(...)`, but it is compressed because applicability/admission/use coincide with node construction.
- Confidence admission is compressed into support-count consumption.
- Decision-context admission occurs when `select_context_facts(...)` emits a `ContextFact` and refuses unsupported facts unless explicitly included.
- Explanation admission occurs when support rows and facts become `BeliefExplanation` and `FactExplanation` records.
- Diagnostic exposure has no actual Evidence admission.
- Closed-choice/testimony admission of actual Evidence remains Unknown because references are not proven resolved.

## consumption findings

- Observation ingestion consumes Evidence by creating downstream Fact evidence lineage.
- State projection consumes evidence-linked facts by creating support/current-belief standings.
- Evidence Graph consumes resolved or compressed references by creating nodes, support links, and fact evidence views.
- Confidence consumes graph support to compute support strength, unsupported status, reasons, and contradiction penalties.
- Contradiction consumes graph evidence views to preserve conflict lineage.
- Decision context consumes confidence/context selection to produce provider-facing context facts.
- Explanation consumes support and evidence IDs to produce why-standing.
- Diagnostics expose availability and dependency but do not consume Evidence constitutionally.

## classifications

| neighborhood | classification | exact compression if any |
| --- | --- | --- |
| Observation ingestion / fact establishment | mature uptake neighborhood | admission implemented as conversion boundary |
| State projection / fact support | mature uptake neighborhood | canonical Evidence payload not resolved for support because fact lineage is sufficient for support purpose |
| Evidence Graph | compressed uptake neighborhood | applicability collapsed into admission; admission collapsed into node/view construction; unresolved Evidence references become weaker represented nodes |
| Confidence / contradiction | compressed uptake neighborhood | Evidence standing compressed into graph support count/view presence |
| Decision context | compressed uptake neighborhood | Evidence identities compressed to evidence_count; admission consumes confidence rows |
| Explanation / why | mature uptake neighborhood | Evidence payload not resolved locally, but evidence ID lineage is sufficient for why-scope |
| Diagnostic correlation / consumer exposure | transport / exposure only | no uptake |
| Closed-choice/testimony references | Unknown | resolved material and admission boundary missing |

## Fidelity findings

| neighborhood | Fidelity |
| --- | --- |
| Observation ingestion / fact establishment | faithful within scope |
| State projection / fact support | faithful within scope |
| Evidence Graph | faithful within scope |
| Confidence / contradiction | faithful within scope |
| Decision context | faithful within scope |
| Explanation / why | faithful within scope |
| Diagnostic correlation / consumer exposure | not applicable: transport/exposure only |
| Closed-choice/testimony references | Unknown |

No inspected compressed neighborhood is classified as unfaithful merely for compression. The compression becomes constitutionally significant only if a downstream surface overclaims hidden Evidence identity, authority, occurrence, or scope. Current evidence does not prove that overclaim for the compressed neighborhoods inspected.

## authority and scope findings

- Observation ingestion keeps authority bounded to observation/fact support; it records Evidence and optionally Facts without cluster mutation authority.
- State projection keeps authority bounded to projected support/current-belief views; it does not rewrite ledger authority.
- Evidence Graph declares read-only graph support; it does not persist a parallel truth system.
- Confidence and contradiction estimate support/conflict but do not resolve truth.
- Decision context provides provider-facing context with support counts and contradiction flags, not Evidence truth.
- Explanation provides explanatory standing, not producer occurrence or truth promotion.
- Diagnostic exposure is read-only diagnostic authority.
- Closed-choice/testimony surfaces preserve local reference categories but actual Evidence authority remains Unknown.

## producer-occurrence findings

- Observation ingestion preserves observation/evidence/fact event occurrence and observed_at, while distinguishing evidence event and fact event boundaries.
- Fact support creates its own support occurrence range (`observed_at`, `latest_observed_at`) from source facts rather than inheriting one producer occurrence.
- Evidence Graph carries source event/run IDs where payloads provide them and otherwise falls back to compressed IDs.
- Confidence and contradiction carry supporting event IDs but do not claim occurrence authority.
- Decision context drops occurrence details; this is acceptable for its minimal context row shape but makes occurrence unavailable there.
- Explanation preserves observed_at and recursive source_fact lineage but does not convert explanation into producer occurrence.
- Diagnostic exposure and testimony reference surfaces do not prove producer occurrence for actual Evidence material.

## refusal, conflict, and Unknown findings

- Refusal is strongest in observation ingestion (suppressed fact promotion), fact support (expired facts and measurement current-sample handling), decision context (unsupported excluded by default), and explanation (no_current_belief/ambiguous).
- Conflict is strongest in contradiction/confidence/explanation, where contradictions are reported, confidence is reduced, and competing beliefs remain visible.
- Unknown is preserved in unsupported facts, no_current_belief explanations, diagnostic unknown statuses, and the unresolved actual-Evidence status of closed-choice/testimony references.
- No inspected consumer repairs Unknown into truth.

## downstream standings

- Observation ingestion produces preserved Evidence records and evidence-linked Facts.
- State projection produces `FactSupport`, current belief support, alias/entity/relationship projections, conflicts, and graph issues.
- Evidence Graph produces `EvidenceNode`, `EvidenceLink`, `FactEvidenceView`, and summary standings.
- Confidence produces `FactConfidence` and confidence summaries.
- Contradiction produces `Contradiction` and contradiction summaries.
- Decision context produces `DecisionContextView` and selected `ContextFact` standings.
- Explanation produces `Explanation`, `BeliefExplanation`, and `FactExplanation` standings.
- Diagnostics produce diagnostic findings, inventory/dependency rows, and rendered output, not Evidence-backed truth.

## cross-neighborhood comparison

### strongest mature reference neighborhood

Observation ingestion and fact establishment is the strongest mature reference neighborhood. It has a concrete canonical Evidence artifact, a clear preservation event, a bounded consumer, explicit refusal behavior, and a downstream Fact standing that remains evidence-linked rather than truth-by-availability.

Explanation/why is also mature, but it is downstream of fact support and consumes evidence IDs through projected support rather than resolving canonical Evidence payloads itself. It is an excellent witness for preserving ambiguity, conflicts, inference lineage, and explanatory scope.

### strongest compressed neighborhood

Evidence Graph is the strongest compressed neighborhood. It performs real bounded use and is central to later confidence, contradiction, context, and explanation surfaces, but its first crossing compresses applicability, admission, and use into node/view construction. It also preserves unresolved evidence references as weaker represented nodes rather than excluding or repairing them.

### clearest transport-only neighborhood

Diagnostic correlation/consumer exposure is the clearest transport-only neighborhood. It stores, formats, indexes, and exposes diagnostic/consumer relationships, but the inspected boundary does not admit actual Evidence artifacts into bounded constitutional use.

### unfaithful neighborhoods, if any

None were proven. No inspected consumer was shown to invent evidence standing, treat availability as admission, treat admission as truth, expand authority, erase scope, ignore material conflicts, repair Unknown, inherit producer occurrence, or promote Evidence directly into stronger standing without a consumer act.

### most important preserved Unknown

The most important preserved Unknown is closed-choice/testimony evidence references. The implementation preserves sophisticated reference, Unknown, conflict, unsupported, visible, and eligible-territory distinctions, but this survey cannot prove that those references are resolved actual Evidence material before local admission and use.

## Book projection decision

No Book update is made. PR 1821 already projected the applicability/admission/consumption distinction. This district survey recovers implementation topology, compressions, and candidate frontiers, but it does not recover a genuinely missing constitutional relation that cannot already be expressed through the completed grammar. Implementation names, classes, functions, event kinds, tables, and schemas remain external grammar.

## one smallest lawful implementation frontier

Selected frontier for later work:

```text
Evidence Graph
+
collapsed applicability/admission at unresolved or resolved evidence-node construction
+
observable consumer-local result: FactEvidenceView/EvidenceNode standing that distinguishes resolved admitted Evidence from represented unresolved reference
```

Why this is the smallest lawful frontier:

- Completed uptake grammar already distinguishes applicability, admission, and consumption.
- Actual topology shows Evidence Graph is the first compressed crossing used by multiple serious downstream consumers.
- Local Fidelity pressure is concrete: downstream confidence/context/explanation can only see graph-produced support count/view standing, so the graph is the smallest place where resolved Evidence admission versus represented reference can become observable without building a universal router.
- The mature observation-ingestion neighborhood witnesses what resolved Evidence identity and bounded refusal look like; it should inform, not be selected as, the frontier.

No implementation begins in this survey.

## later implementation pressure

A later implementation slice, if authorized, should stay local to Evidence Graph and avoid a universal Evidence router. The smallest observable improvement would be to separate graph-local applicability/admission status from node construction for one case, likely by preserving whether a node came from:

1. resolved `State.evidence[evidence_id]`;
2. unresolved `Fact.evidence_ids` represented as a weaker reference;
3. projection/source-fact fallback.

The observable result should be visible in the graph-local output and downstream tests without changing runtime fact truth, context truth, or explanation authority.

## preserved Unknowns

- Whether closed-choice selection binding resolves actual Evidence material before using evidence references.
- Whether inquiry testimony evidence references have a runtime resolver outside the inspected files.
- Whether any operational diagnostic `evidence_present` field ever crosses from diagnostic availability into actual Evidence admission; current inspected behavior says transport/exposure only.
- Whether future Book-facing surfaces should mention resolved-reference admission; current survey says no Book update.
- Whether Evidence Graph should refuse unresolved evidence references or continue preserving weaker represented nodes; this is a later implementation question, not resolved here.
