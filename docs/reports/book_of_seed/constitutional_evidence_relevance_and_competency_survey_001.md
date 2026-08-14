# Constitutional Evidence Relevance and Competency Survey 001

## Repository state examined

- Survey operation: repository-supported orientation about how new or changed evidence becomes locally relevant; not an architecture proposal, scheduler design, universal pipeline, central inquiry engine, ownership plan, or implementation seam selection.
- Orientation source: `book_of_seed/repository_constitutional_dimensionality_survey_011.md`, used as high-resolution orientation only, not as a prescribed architecture.
- Recorded `git rev-parse HEAD`: `9005fe7444f696aacecdc5d710403003d5076329`.
- The checkout already contains constitutional Book clauses and SQLite witness material for bounded examination, evidence/provenance support binding, recorded assertion standing, authority scope, consumer uptake, occurrence evidence, and Eye/competency locality.

## Method and resolution discipline

This survey begins with the recovered macro-dimensional families:

```text
identity
content
standing
provenance
responsibility
authority
scope
occurrence / preservation
```

The families are treated as coordinate families, not as a mandatory sequence. A responsibility locality is admitted only where repository evidence shows a bounded producer or consumer question, material it may recognize, local validation requirements, lawful acts, refusal or Unknown behavior, and an output that later consumers may or may not accept.

The survey keeps two resolutions at once:

- **High resolution**: constitutional grammar, external grammar, fidelity, dimensions, standing, authority, acts, and constraints.
- **Local resolution**: exact producer, artifact, consumer, validation, refusal, test, and occurrence evidence.

The recurring cycle is therefore descriptive, not prescriptive:

```text
new or changed evidence becomes available
→ local responsibilities evaluate relevance
→ zero or more responsibilities accept it
→ each accepted locality applies its own bounded question and acts
→ new evidence or standing is produced
→ later consumers may independently evaluate that output
```

The repository does not support inference of a road from adjacency, shared fields, constructibility, rendering, or availability. Three crossings remain especially burdened:

- **producer occurrence**: did the asserted producer boundary occur, and what evidence travels?
- **consumer uptake**: did a later consumer give upstream material bounded constitutional use?
- **authority scope**: did the material and act remain within a bounded warrant?

## Repository-supported locality map

| Locality or bounded competency | Responsibility performed | Evidence it can recognize | Coordinates required for relevance | Applicable local question | Authority and scope required | Acts it may perform | Refusal, Unknown, and lawful inactivity | Output or standing-bearing artifact | Producer occurrence evidence | Consumers that may accept output | Consumer uptake validation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Recording boundary for assertions | Preserve attributable assertion-bearing material inside a declared horizon. | Event, diagnostic, examination, or change assertion material offered to a recorder. | Record identity, assertion content, attribution, preservation horizon, scoped subject where diagnostic/examination-scoped, and record/fact separation. | "May this boundary preserve this assertion as retrievable recorded material?" | Recorder's declared preservation horizon and any diagnostic or examination scope; event-ledger writes remain distinct from cluster mutation. | Create a retrievable record; preserve a record existence standing; make material available for bounded examination. | Refuses over-inference by preserving `not_established` truth posture; diagnostic/examination-scoped material remains bounded availability, not cluster truth. Unknown remains where the record lacks stronger support. | Recorded assertion, event, diagnostic record, or examination-scoped record; standing is record-exists / preserves-attributed-assertion. | Recording occurrence is established by retrievable ledger or record storage when preservation succeeds; it does not establish the represented external occurrence. | Bounded examination, support-binding, fact extraction, projection, explanation, diagnostics, and later uptake boundaries. | Consumers validate identity, scope, attribution, record status, preservation horizon, and forbidden inference before use; they must not treat record existence as truth or authority. |
| Bounded examination competency | Decide whether recorded material is relevant enough for further examination inside a declared responsibility. | Recorded constitutional-change assertion or similar recorded material. | Responsibility family, responsibility subject, subject binding, evidence requirement, provenance requirement, authority zone, and available support standings. | "Is this recorded material relevant to this responsibility, with enough support and authority to permit further examination?" | Local responsibility and subject plus exact authority boundary; no selection, execution, mutation, truth establishment, or required action follows. | Evaluate relevance; preserve lawful inactivity reasons; preserve Unknown; produce bounded permission for further examination. | `lawful_inactivity_irrelevant`, `lawful_inactivity_insufficient_evidence`, `lawful_inactivity_insufficient_provenance`, dangling-reference inactivity, authority-blocked inactivity, support-mismatch inactivity, or `unknown_preserved`. | `competency_change_examination` posture and reason; strongest positive result is `bounded_permission_for_further_examination`. | Producer occurrence is fixture/query occurrence only unless a running boundary records its examination; CROSS JOIN rows are calculated pairs, not dispatch or awakening. | Later examinations, support-binding consumers, diagnostic/audit summaries, and Book surveys may cite the posture as bounded witness evidence. | Consumers validate competency identity, local family/subject match, evidence/provenance support posture, authority-zone match, assertion truth boundary, and forbidden inference. |
| Evidence support-binding consumer | Determine whether evidence-shaped material is applicable represented support for a bounded examination. | Evidence reference plus represented evidence material and possibly provenance material. | Evidence identity versus existence, source attribution, evidence kind, source identity/context, responsibility family, observable subject, supported claim id, authority zone, preservation horizon, confidence label, and provenance relation. | "Does this evidence-shaped material satisfy this competency's bounded evidence requirement for this recorded assertion?" | Same responsibility, subject, claim, and authority zone required by the competency; no universal evidence admission. | Bind evidence to assertion for bounded examination; classify missing, dangling, unknown, mismatch, or applicable support. | Missing reference, dangling reference, unknown subject/claim binding, authority mismatch, source-context Unknown, or support mismatch produce inactivity or Unknown downstream. | `support_binding_examination.evidence_standing`, especially `applicable_represented_evidence`; it is represented support, not fact standing. | Evidence row existence proves material is represented in the witness, not collection occurrence or producer occurrence. | Bounded examination, provenance applicability, cross-examination, explanation, and later reliability/reliance consumers. | Consumers validate material existence, subject/claim match, authority match, source context, provenance relation, confidence/uncertainty, and forbidden inference against truth or independent corroboration. |
| Provenance representation and applicability consumer | Determine whether represented lineage can contribute to bounded support. | Provenance reference, represented provenance material, and its relation to assertion or evidence. | Provenance identity versus existence, source attribution/context, applies-to assertion/evidence, authority zone, lineage status, verification status, producer occurrence status. | "Is represented provenance applicable to this assertion or evidence, and what lineage standing may be used?" | Bounded requirement of the consuming examination; authority zone must match where required. | Bind provenance; classify independent verification boundary; preserve represented-not-verified lineage; preserve conflicts. | Missing/dangling provenance, unknown applicability, authority mismatch, internal conflict, conflicting references, or unverified provenance preserve inactivity or Unknown where appropriate. | `provenance_standing`, `provenance_verification_boundary`, and `producer_occurrence_boundary`; represented lineage may support further examination without stronger proof. | The witness explicitly preserves `producer_occurrence_not_established`; copied causation IDs, strings, and internally coherent lineage are not occurrence seals. | Evidence support-binding, bounded examination, explanations, reliance checks, and cross-examination. | Consumers validate existence, applicability to the exact assertion/support material, authority, internal coherence, verification status, and explicit producer-occurrence boundary. |
| Knowledge extraction from tool-result events | Convert a completed-tool-result-shaped event into evidence without inferring facts. | Source event with event kind `tool.call.completed` or legacy `tool.result`, tool name, output payload, timestamp, and ledger append ability. | Source event identity, event kind, tool name, output, timestamp, causation id, workspace/event context, and confidence. | "May this completed tool-result event be observed as evidence?" | Extraction boundary authority to append evidence; source event is treated as testimony about tool output, not verified external effect. | Create `Evidence` with source `tool:<name>`, kind `tool.output`, observed time from source event, output payload, confidence; append `evidence.observed` caused by the source event. | Non-tool or incomplete events are not accepted; extraction does not infer facts, prove external effects, or verify original execution occurrence. | `FactExtractionResult` and `evidence.observed` event; standing is evidence observation, not fact. | Extraction occurrence is proven by the appended `evidence.observed` event; original tool execution occurrence remains only as source-event testimony unless separately trusted. | Evidence consumers, fact-establishment boundaries, explanations, projections, and diagnostics. | Consumers validate source event kind/tool name, causation, evidence event presence, payload boundary, confidence, and fact/occurrence forbidden inference. |
| Fact establishment or state projection consumer | Separate recorded events/evidence from facts and projected state. | Events, evidence observations, fact support, or existing facts. | Event identity, fact identity, subject/entity identity, support, source/provenance, event kind, state/projection scope, and standing. | "Does this material establish a fact or merely support a projection/explanation under bounded support?" | Fact or projection-specific warrant; projection availability does not create upstream truth. | Establish facts only under support rules; project current state from accepted facts/events; expose cache or view content with freshness/scope boundaries. | Unsupported material remains evidence/testimony; projection may be stale, partial, Unknown, or view-only; record existence is not fact. | Fact record, state projection, projection cache entry, or explanation-support material. | Fact/projector invocation may be locally observed; durable occurrence requires records; event source occurrence remains separately burdened. | Explanations, operational views, question surfaces, audits, and later reliance consumers. | Consumers validate fact support, event/fact separation, projection scope, freshness, lineage, and that view evaluation is not producer occurrence. |
| Consumer uptake / road sufficiency boundary | Give upstream material bounded constitutional use for a declared purpose, or refuse. | Selected artifacts, testimony bundles, composition requests, completed pipeline results, stage artifacts, identity references, and lineage snapshots. | Producer artifact identity, consumer purpose, selected state, selected reference, family applicability, registration/buildability, identity match, lineage match, sufficiency, conflicts, and purpose limit. | "May this consumer use this upstream assertion for this bounded purpose, and what downstream assertion or standing results?" | Consumer-local warrant; authority does not expand in transit; handoff representation alone is insufficient. | Form requests, compose views, preserve testimony, preserve selected-standing for a purpose, judge sufficiency, establish a new downstream frontier, or construct an explanation. | Refuse on not-selected state, missing/mismatched identity, lineage mismatch, insufficient clauses, conflict, unsupported family, or purpose mismatch; Unknowns are preserved rather than repaired. | Consumer-local request standing, testimony standing, downstream frontier standing, composition artifact, or explanation assertion. | Successful consumer validation does not prove upstream producer occurrence; direct construction can bypass producer. Occurrence travels only if represented and accepted. | Downstream frontier assemblers, explanations, display/composition surfaces, selection-road audits, and later reliance boundaries. | Consumers validate exactly the invariants material to use: registration/buildability, selected-state standing, identity/lineage agreement, clause sufficiency, conflict posture, purpose scope, and forbidden inference. |
| Authority-scope / bounded reliance consumer | Prevent warranted content, records, selections, or admissions from expanding authority or standing. | Operator expressions, approvals, warrants, selections, internal recommendations, records, provider handoffs, examination outputs, admission findings. | Authority origin, scope binding, role/purpose, evidence/provenance, source boundary, confidence/Unknowns, negative authority, and requested act. | "May this downstream act or reliance proceed within the preserved warrant without strengthening it?" | Explicit bounded authority; internal records and provider handoffs cannot create or enlarge authority. | Permit bounded reliance, admit participation for the next bounded posture, stop at the warrant boundary, or refuse/non-perform. | Authority mismatch or insufficiency yields lawful stop/refusal; analytical competence does not become adjudicative authority; Unknown authority remains Unknown. | Bounded reliance or admission posture, refusal reason, non-performance record, or authority-bound result. | Authority records prove only represented warrant material unless grant occurrence is separately preserved and accepted. | Execution boundaries, examination consumers, reliance consumers, communication/handoff, diagnostics. | Consumers validate origin, scope, role, purpose, negative authority, preserved Unknowns, and that reliance does not mutate truth, implementation authority, or universal permission. |
| Cross-examination / comparison responsibility | Compare independently preserved testimony or findings without erasing source locality. | Two or more independently preserved testimony/finding artifacts. | Attribution, provenance, support basis, subject, scope, authority, confidence/uncertainty, Unknowns, standing, and forbidden inference for each input. | "What comparison standing is permitted between these inputs without source-local erasure?" | Comparison boundary authority only; comparison does not become truth, reliance warrant, source independence, reconciliation, or implementation permission. | Produce bounded comparison standing: agreement, disagreement, contradiction, conflict, refinement, insufficiency, or Unknown. | Unknown, insufficient, conflicted, or outside-scope inputs remain preserved as such; apparent agreement does not authorize stronger standing. | Comparison finding with source-local standings retained. | Comparison occurrence travels only if the comparison output is preserved; input producer occurrence remains separate. | Later examinations, explanations, reliability reviews, and bounded reliance consumers. | Consumers validate source-local attribution/provenance/support for each input, comparison authority, confidence/Unknown preservation, and forbidden inference against causation or reconciliation. |

## How evidence becomes locally relevant

Evidence becomes locally relevant only when a local responsibility can bind its shape to that responsibility's coordinates. The SQLite witness makes this explicit: a recorded change assertion is not presented to one universal processor. Instead, every calculated competency/change pair is examined against local responsibility family, subject, authority zone, evidence requirement, and provenance requirement. The result may be bounded permission, lawful inactivity, or Unknown. A row pair or query availability is not dispatch, notification, or producer occurrence.

At high resolution, the macro families participate as follows:

- **Identity** distinguishes recorded assertion, evidence row, provenance row, competency, producer attribution, consumer artifact, and later output identity.
- **Content** supplies the assertion text, evidence payload, provenance lineage, event payload, request, or explanation claim.
- **Standing** determines whether content is recorded, applicable support, represented lineage, bounded permission, Unknown, refused, testimony, fact, projection, or explanation.
- **Provenance** binds source attribution/context, lineage applicability, verification, and producer occurrence boundaries.
- **Responsibility** selects the local question: recorder, examiner, support binder, extractor, projector, consumer, authority checker, or comparer.
- **Authority** constrains the act and prevents admission or reliance from expanding into execution, mutation, truth, or universal permission.
- **Scope** bounds responsibility subject, source context, diagnostic run, preservation horizon, purpose, inquiry, authority zone, consumer, and projection.
- **Occurrence/preservation** distinguishes acted occurrence, recording occurrence, extraction occurrence, producer occurrence, external effect, durable record, and later uptake occurrence.

At local resolution, relevance is therefore not intrinsic to evidence. It arises when a bounded responsibility can ask one of its own shape-governed questions:

```text
recording: may this assertion be preserved as a scoped record?
examination: is this recorded material relevant enough for further examination?
evidence binding: does this evidence material satisfy this local support requirement?
provenance binding: does this lineage apply, and with what verification/occurrence boundary?
extraction: may this completed-tool-result-shaped event be converted into evidence?
fact/projection: may this material establish fact or only project/view/explain bounded content?
uptake/road: may this consumer use that upstream assertion for this declared purpose?
authority/reliance: may reliance or action proceed without warrant expansion?
comparison: what standing follows from comparing source-local preserved materials?
```

## Cross-family boundary findings

### Producer occurrence

Producer occurrence remains a crossing, not a default inheritance. Repository evidence supports separate layers: boundary invocation, assertion-bearing branch occurrence, result construction, external effect, recording occurrence, knowledge extraction occurrence, and consumer uptake occurrence. Representation existence, row insertion, object construction, selected fields, source attribution, or copied causation identifiers do not prove that the represented producer boundary occurred. Durable occurrence evidence must itself travel as a record, event, evidence, testimony, or other accepted artifact.

### Consumer uptake

Consumer uptake occurs only where the consumer gives upstream material bounded constitutional use or standing for a purpose, or produces a downstream assertion materially dependent on it. Typed request formation, field reading, handoff, rendering, adjacency, and constructibility are insufficient. Each consumer validates only the invariants material to its own use; a successful local validation does not re-establish the upstream artifact or prove its producer occurred.

### Authority scope

Authority does not travel merely because evidence, a record, or a provider handoff travels. A local responsibility requires authority for its own act and must preserve negative authority, confidence limits, Unknowns, and purpose scope. Admission into a next bounded posture is not ratification, mutation authority, implementation authority, adjudicative authority, or reusable approval.

## Disconnectedness and branching supported by evidence

The repository evidence supports several independent or branching localities rather than one universal sequence:

- Recording can create retrievable assertion material without examination, fact extraction, or truth establishment.
- Bounded examination can treat material as relevant for further examination, inactive, or Unknown without selecting, executing, mutating, or requiring action.
- Evidence and provenance support binding can produce applicable represented support or lineage standing without proving fact, independent corroboration, causation, or producer occurrence.
- Knowledge extraction can create evidence from completed-tool-result-shaped events without proving original tool execution or external effects.
- Consumer uptake can create a new downstream frontier, testimony standing, composition, request standing, or explanation assertion without re-standing upstream material.
- Authority-scope checking can lawfully stop even when content is available, coherent, or useful.
- Cross-examination can compare preserved materials without reconciling them or promoting agreement into truth.

No repository evidence requires a central inquiry engine, scheduler, universal competency registry, single Eye-owned observation pipeline, or prescribed topology. The witness `CROSS JOIN` demonstrates deterministic side-by-side examination pairs only; it does not awaken competencies or establish runtime dispatch.

## Smallest repository-supported account

Evidence becomes locally relevant when a bounded responsibility can bind available material to the coordinates required by that responsibility: identity, content, standing, provenance, responsibility, authority, scope, and occurrence/preservation. The bounded responsibilities currently supported include recording, bounded examination, evidence support binding, provenance applicability, knowledge extraction, fact/projection consumption, consumer uptake, authority-scope reliance, and cross-examination.

Applicable questions arise from evidence shape, not from a universal sequence. A completed-tool-result-shaped event can trigger an extraction question; a recorded-change assertion can trigger bounded relevance; an evidence reference can trigger support binding; a provenance reference can trigger applicability and verification boundary checks; a selected artifact or testimony bundle can trigger consumer-local uptake questions; a warrant can trigger bounded reliance questions; multiple preserved findings can trigger comparison questions.

Each responsibility may produce only its local output: record existence, bounded permission for further examination, applicable represented support, represented lineage standing, evidence observation, fact/projection/explanation material, consumer-local downstream standing, bounded reliance/admission/refusal, or comparison standing. These outputs become available to later consumers only as artifacts or preserved evidence with their own standing; later consumers must independently validate material identity, local scope, authority, provenance, standing, producer-occurrence evidence, and forbidden inferences before uptake.

The crossings that remain Unknown are the exact runtime set of all responsibility localities outside the surveyed anchors; which producer occurrence proofs intentionally travel across every production boundary; which adapters own assertion-bearing uptake rather than mere transport; whether all comparison subfamilies share the same standings; and which locality branches, if any, should split from the current macro families in future repository-supported surveys. This survey does not select a next implementation seam.
