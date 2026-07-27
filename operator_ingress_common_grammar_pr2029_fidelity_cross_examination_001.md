# Operator-ingress common-grammar PR 2029 Fidelity cross-examination 001

## 1. Boundary, authority, and governing answer

This is one bounded, report-only cross-examination of merged PR 2029
(`ca8371f`) against the canonical Book at current `main`. It changes no Book,
implementation, test, root documentation other than this report, `docs/`, prior
report, CLI behavior, event, ledger, State, projector, or runtime wiring.

The controlling grammar is the Book's already-established eight-dimensional
characterization of an exact subject or relation:

1. **identity**;
2. **content**;
3. **standing**;
4. **source / provenance**;
5. **responsibility**;
6. **authority / warrant**;
7. **scope / locality**; and
8. **occurrence / preservation**.

These are constitutional dimensions, not fields required on a universal class
and not phases of a protocol. This report applies them exactly. It does not
recover, rename, reduce, or replace them.

**Governing answer:** PR 2029 preserves several correct local distinctions, but
does **not** faithfully project operator bootstrap through the eight dimensions.
Its proposed implementation makes a library-owned attempt aggregate the center
of the road, encodes absence of warrant as repeated negative booleans, elects
not to record the very occurrences needed for recurrence and currentness, has
no production shell caller, and fixes a one-retry application policy that the
Book explicitly leaves policy-dependent. The proposal is therefore a bespoke
protocol state machine specification around a useful exact-set binder, not a
production-connected dimensional projection.

The defect is not that PR 2029 failed to invent enough dataclasses. The defect
is that it substituted compiled structures for produced, recorded evidence and
then asked those structures to own presentation, currentness, replay,
supersession, treatment meaning, stopping, and policy. A frozen value returned
to an arbitrary caller can describe those claims; it cannot witness the real
shell occurrences, make them durable, or project their current standing.

## 2. Canonical findings applied before implementation inspection

The Book fixes the following cross-examination rules.

* An act occurrence requires its competent production boundary. Artifact
  construction and downstream validation do not prove the upstream occurrence.
* Event production and event recording are separate. Not every constitutional
  occurrence must be recorded, but durable comparison cannot be projected from
  evidence deliberately discarded at process-local return.
* A ledger event is an immutable record that an assertion was made. Recording
  does not make its payload Fact standing, constitutional truth, current
  standing, operator authority, or cluster truth.
* Projection is a rebuildable, purpose-bounded view over recorded evidence.
  Durable evidence can remain while a presentation, attempt, response, or
  treatment loses current standing through consumption or supersession.
* Exact-set binding establishes membership or nonmembership only within the
  exact presented set. It does not interpret an unsupported response.
* Repeated obstruction is scoped recurrence evidence. It may warrant Demand
  examination; it neither establishes a Demand nor assigns its family.
* A Demand, even if separately established, does not select or authorize
  acquisition.
* Treatment selection and treatment execution are separate acts. Affirmative
  selection neither authorizes nor begins acquisition. Negative selection does
  not establish stopping.
* Common-grammar work is prerequisite movement before possible BOGE. BOGE
  remains operator-origin; Seed may not manufacture a Seed-origin bootstrap
  goal.
* Retry is optional, bounded, separately evidenced, and policy-dependent. The
  Book specifies no count.

## 3. Evidence-key for the matrices

Every dimensional cell below states all seven required judgments in this
compact order:

`E` exact evidence; `P` producer responsibility; `Prov` provenance; `L` what
may be ledger-recorded; `Cur` active standing in the current projection; `U`
what remains Unknown; `¬` what does not follow.

“May record” means a competent recorder may preserve the produced assertion;
it is not a claim that storage produced the occurrence. “Current” means a
projector's bounded, conflict-aware standing, never mutation of cluster truth.

## 4. Eight-dimensional matrices for every bootstrap occurrence

### 4.1 Operator-ingress occurrence

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** interaction id, ingress occurrence id, ordinal, and captured-subject ref. **P:** real shell ingress adapter. **Prov:** adapter/channel and session correlation. **L:** ids and correlation may be recorded. **Cur:** preserved ingress is current for examination until consumed, abandoned, or superseded. **U:** identity of a human behind the channel. **¬:** attribution does not prove authority, intent, or a goal. |
| content | **E:** exact value at the owned capture boundary, or distinct EOF outcome; decoding and framing loss named. **P:** shell capture. **Prov:** bytes/decoder when retained, otherwise explicitly post-framing text. **L:** exact captured value and known loss, subject to existing secret rejection. **Cur:** original preserved material available for later re-entry. **U:** meaning and original bytes when not retained. **¬:** no trimming, tokenization, interpretation, or affirmative/negative meaning follows. |
| standing | **E:** source-attributed operator-ingress testimony. **P:** competent ingress producer. **Prov:** production event plus adapter identity. **L:** the producer assertion may be preserved. **Cur:** ingress occurrence standing, not BOGE standing. **U:** interpretability for BOGE. **¬:** a dataclass named `OperatorIngressOccurrence` is not standing. |
| source / provenance | **E:** `source_kind=operator`, channel, capture time/order, session/correlation, known loss. **P:** adapter. **Prov:** direct capture boundary. **L:** all available lineage. **Cur:** source attribution with unresolved identity. **U:** operator identity and upstream transport details not observed. **¬:** `operator` does not grant operator authority. |
| responsibility | **E:** shell adapter accepted the free-form occurrence. **P:** real runnable shell path, not a test or arbitrary library caller. **Prov:** invocation and emitted event lineage. **L:** producer/adapter/version. **Cur:** ingress producer remains attributable. **U:** downstream interpretation owner. **¬:** binder or projector cannot retroactively become ingress producer. |
| authority / warrant | **E:** warrant only to preserve attributed ingress for bounded examination. **P:** ingress boundary plus recording policy. **Prov:** declared channel contract. **L:** scope and limits. **Cur:** available, not authorized movement. **U:** intent, requested action, interpretation, BOGE eligibility. **¬:** capture is not admission, Demand, authority, or execution. |
| scope / locality | **E:** one workspace/session/interaction/channel occurrence. **P:** ingress adapter. **Prov:** scoped ids. **L:** exact locality. **Cur:** only that interaction. **U:** relation to other interactions absent evidence. **¬:** no global bootstrap or shared grammar. |
| occurrence / preservation | **E:** actual read completed or EOF occurred. **P:** shell read boundary; recorder separately appends. **Prov:** occurrence id linked to event id and append order. **L:** occurrence assertion. **Cur:** durable unconsumed/superseded status derived by projection. **U:** delivery before capture and future use. **¬:** an in-memory constructor or capture string alone is not a production witness. |

### 4.2 Probe-production occurrence

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** probe-production occurrence id, probe kind/version, semantic-set identity, ingress ref. **P:** bounded probe producer invoked by shell orchestration. **Prov:** ingress and producer version. **L:** production assertion and set representation refs. **Cur:** one current produced probe eligible for presentation. **U:** whether it will be emitted. **¬:** content identity is not presentation occurrence identity. |
| content | **E:** canonical two treatments and their bounded selection effects, plus local tokens/labels as representation. **P:** application producer. **Prov:** Book-constrained producer version. **L:** exact immutable set and representation fingerprint. **Cur:** exact set applicable to this probe. **U:** shared understanding of labels. **¬:** labels are not constitutional vocabulary or goal meanings. |
| standing | **E:** competent production of a bounded communication probe. **P:** producer boundary. **Prov:** validated preserved ingress and interpretation-unavailable condition. **L:** produced-probe event. **Cur:** probe available, not yet presented. **U:** operator receipt. **¬:** construction does not prove emission, acquisition applicability, or BOGE. |
| source / provenance | **E:** ingress ref, producer/version, semantic members, representation derivation. **P:** producer. **Prov:** causal link to ingress. **L:** lineage and known loss. **Cur:** source-attributed derived probe. **U:** external grammar. **¬:** application authorship does not make labels Book law. |
| responsibility | **E:** probe producer selected this bounded probe form. **P:** application producer; shell calls it. **Prov:** code/version and invocation event. **L:** producer responsibility. **Cur:** ownership remains with producer. **U:** response and stopping owners. **¬:** `PresentedClosedChoiceSet` or tests are not the application producer. |
| authority / warrant | **E:** warrant to ask only the canonical bounded treatment question. **P:** probe producer. **Prov:** preserved ingress plus unavailable interpretation. **L:** warrant inputs/limits. **Cur:** eligible for bounded emission. **U:** acquisition authority. **¬:** probe production does not select a treatment or authorize movement. |
| scope / locality | **E:** one interaction and one attempt purpose. **P:** producer. **Prov:** exact ingress/attempt refs. **L:** locality. **Cur:** only within that interaction. **U:** applicability elsewhere. **¬:** no generic dialogue controller. |
| occurrence / preservation | **E:** producer invocation successfully emitted a production artifact/event. **P:** producer; recorder separately. **Prov:** event causation from ingress. **L:** durable production assertion. **Cur:** latest unsuperseded eligible probe production. **U:** presentation occurrence until emitted. **¬:** deterministic construction in a test is not production. |

### 4.3 Presentation occurrence

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** presentation occurrence id distinct from set/probe id, attempt id, exact fingerprint. **P:** shell output/emission boundary. **Prov:** produced probe and concrete output channel. **L:** presentation assertion. **Cur:** latest emitted, response-eligible presentation. **U:** receipt/comprehension. **¬:** `presentation_ref` supplied by a caller is not occurrence proof. |
| content | **E:** exact bytes/text actually offered, option encodings, ordering, prompt, rendering loss. **P:** renderer plus emitter. **Prov:** semantic set and render version. **L:** exact representation or lossless ref/hash with retained basis. **Cur:** representation against which response can bind. **U:** what operator perceived. **¬:** render return does not prove transport or receipt. |
| standing | **E:** an emission occurrence, separately from representation formation. **P:** real output adapter. **Prov:** successful write evidence. **L:** emitted-presentation event. **Cur:** open/current only under response-window policy. **U:** delivery and reliance. **¬:** formatting is not emission. |
| source / provenance | **E:** producer probe, renderer, output channel, emission result. **P:** emitter. **Prov:** causal chain ingress→probe→presentation. **L:** chain and conflicts. **Cur:** exact current presentation lineage. **U:** downstream display transformations. **¬:** identical content does not make two emissions one occurrence. |
| responsibility | **E:** renderer formed representation; emitter performed output. **P:** separate owners where implementation separates them. **Prov:** both boundaries. **L:** respective assertions. **Cur:** emitter owns occurrence claim. **U:** operator response owner. **¬:** a mixed presentation object must not collapse formation and emission. |
| authority / warrant | **E:** authority only to emit bounded probe in declared interaction. **P:** shell orchestration/emitter. **Prov:** current produced probe. **L:** scope and stop limits. **Cur:** may accept a response. **U:** response meaning. **¬:** emission grants no acquisition, goal, or operator authority. |
| scope / locality | **E:** interaction, attempt, channel, set fingerprint. **P:** emitter. **Prov:** scoped links. **L:** locality. **Cur:** exact attempt only. **U:** other clients or channels. **¬:** same token from another presentation cannot bind. |
| occurrence / preservation | **E:** actual output write outcome and ordinal/time. **P:** shell emitter; recorder separately. **Prov:** event/append link. **L:** successful/failed emission assertion. **Cur:** currentness projected from later response, close, or supersession events. **U:** receipt. **¬:** library-only renderer is fake-only scaffolding for occurrence. |

### 4.4 Operator-response occurrence

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** response occurrence id, source/channel, interaction, exact presentation and attempt refs. **P:** shell input adapter. **Prov:** next bounded capture tied to current presentation. **L:** response event. **Cur:** unconsumed response candidate. **U:** human identity. **¬:** `OperatorSelectionTokenCapture` alone is not response occurrence proof. |
| content | **E:** exact token at owned boundary or distinct EOF, with framing/decoding loss. **P:** capture adapter. **Prov:** capture method. **L:** exact material and limits subject to secret policy. **Cur:** material available for binding. **U:** unsupported meaning/intent/treatment. **¬:** empty text is not EOF and near-match is not normalization permission. |
| standing | **E:** attributed response to one presentation. **P:** response producer. **Prov:** exact occurrence linkage without defeating Unknown/conflict. **L:** occurrence assertion. **Cur:** response is pending, consumed, stale, or conflicted by projection. **U:** semantic meaning before binding. **¬:** response existence is not receipt proof or treatment selection. |
| source / provenance | **E:** channel, source attribution, presentation fingerprint/ref, capture refs. **P:** adapter. **Prov:** direct response capture. **L:** lineage. **Cur:** source-scoped candidate. **U:** off-channel causes. **¬:** matching text from a different channel/presentation does not qualify. |
| responsibility | **E:** shell captured; binder later compares. **P:** adapter for occurrence, binder for membership. **Prov:** two distinct events/acts. **L:** capture independently of binding. **Cur:** responsibilities remain distinct. **U:** interpretation owner for unsupported text. **¬:** binder cannot manufacture response provenance. |
| authority / warrant | **E:** warrant to preserve and submit exact response to this set. **P:** capture/orchestrator. **Prov:** current presentation. **L:** bounded warrant. **Cur:** binding-eligible only if current and uncompromised. **U:** authority for selected treatment. **¬:** source attribution does not itself authorize anything. |
| scope / locality | **E:** one interaction/presentation/attempt/capture. **P:** capture adapter. **Prov:** exact refs. **L:** locality. **Cur:** cannot migrate to another identical set. **U:** broader preference. **¬:** token reuse is not consent elsewhere. |
| occurrence / preservation | **E:** actual read/EOF occurrence. **P:** shell capture; recorder separately. **Prov:** causal/correlation ids and append order. **L:** occurrence even before consumption. **Cur:** consumption/supersession projected from later evidence. **U:** future retry. **¬:** caller-authored response dataclass is not a real production occurrence. |

### 4.5 Exact-set binding / nonmembership occurrence

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** binding occurrence/id over exact presentation fingerprint and response id. **P:** exact binder consumer after lineage/currentness checks. **Prov:** presentation plus response. **L:** binding result event. **Cur:** current binding only while its inputs remain applicable. **U:** response meaning when nonmember. **¬:** binding id is not treatment-selection id. |
| content | **E:** exact member option ref or exact nonmembership; Unknown/conflict preserved. **P:** `bind_closed_choice_selection`. **Prov:** supplied closed set and token capture. **L:** comparison inputs/result. **Cur:** membership evidence usable by treatment selector. **U:** unsupported meaning, intent, requested treatment. **¬:** label, prefix, whitespace, case, or semantic similarity cannot bind. |
| standing | **E:** bounded comparison finding. **P:** binder under competent caller preconditions. **Prov:** exact-set fingerprint and capture. **L:** read-only act result may still be recorded. **Cur:** current comparison finding, not constitutional truth. **U:** any proposition beyond membership. **¬:** nonmembership is neither negative selection nor refusal. |
| source / provenance | **E:** response, presentation, set, capture, binder convention. **P:** binder. **Prov:** full input lineage. **L:** result plus lineage. **Cur:** traceable comparison evidence. **U:** provenance gaps explicitly defeat binding. **¬:** a matching token cannot cure wrong occurrence identity. |
| responsibility | **E:** binder performs exact membership only. **P:** existing binder. **Prov:** deterministic function plus competent invocation. **L:** its assertion. **Cur:** binder owns no treatment meaning. **U:** treatment selector. **¬:** binder is not response producer, projector, stop owner, or BOGE adapter. |
| authority / warrant | **E:** authority limited to exact comparison. **P:** binder. **Prov:** validated current inputs. **L:** limits. **Cur:** may feed only the declared probe selector. **U:** acquisition/stopping authority. **¬:** bound is not goal, admission, execution, or authority. |
| scope / locality | **E:** one exact set representation and response occurrence. **P:** binder. **Prov:** fingerprint and refs. **L:** scope. **Cur:** local to probe purpose. **U:** equivalence to other sets. **¬:** byte-identical sets do not merge occurrences. |
| occurrence / preservation | **E:** binder was actually invoked after checks. **P:** production orchestrator/binder; recorder separately. **Prov:** binding event caused by response. **L:** comparison assertion. **Cur:** can be invalidated for active use by supersession without deleting history. **U:** later use. **¬:** pure function availability is not invocation evidence. |

### 4.6 Acquisition-treatment selection occurrence

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** selection occurrence/id, exact affirmative member, binding and treatment refs. **P:** probe-specific selection act. **Prov:** current exact-member binding. **L:** selection event. **Cur:** acquisition treatment selected for this interaction. **U:** method/provider/scope. **¬:** a monolithic result id need not duplicate every upstream object. |
| content | **E:** only `bounded acquisition treatment selected`. **P:** selector. **Prov:** immutable option-to-treatment mapping. **L:** positive selection assertion plus limits. **Cur:** selected treatment awaiting separate applicability/selection/authority/admission. **U:** all acquisition realization details. **¬:** not authorized, begun, successful, shared grammar, Demand, or BOGE. |
| standing | **E:** selection-act standing. **P:** responsible selector. **Prov:** binding and mapping warrant. **L:** event preserves selection. **Cur:** positive standing; negative standings arise from absent later warrants, not copied `false` fields. **U:** whether movement will be admitted. **¬:** `acquisition_authorized=false` is not required evidence of absent authority. |
| source / provenance | **E:** ingress→probe→presentation→response→binding lineage. **P:** selector. **Prov:** event refs rather than embedded duplicates. **L:** lineage. **Cur:** attributable selected treatment. **U:** later candidate evidence. **¬:** presented label cannot supply semantic identity. |
| responsibility | **E:** selector chose treatment; later owners remain separate. **P:** probe selection consumer. **Prov:** selector version. **L:** producer. **Cur:** selection responsibility visible. **U:** acquisition owners. **¬:** selector must not execute treatment. |
| authority / warrant | **E:** exact affirmative binding warrants this selection only. **P:** selector. **Prov:** canonical mapping. **L:** narrow warrant. **Cur:** selection, no authority. **U:** authority and admission. **¬:** no Demand, acquisition, goal, or cluster mutation authority. |
| scope / locality | **E:** one interaction and preserved ingress prerequisite. **P:** selector. **Prov:** scoped lineage. **L:** locality. **Cur:** local selected treatment. **U:** grammar extent needed. **¬:** no global learning program. |
| occurrence / preservation | **E:** actual selector invocation. **P:** production caller; recorder separately. **Prov:** event caused by binding. **L:** durable selection event. **Cur:** may remain pending or be superseded/consumed under later rules. **U:** treatment execution. **¬:** returned `OperatorCommonGrammarProbeSelectionResult` alone is not durable/current. |

### 4.7 Local-stop-treatment selection and stopping occurrences

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** distinct selection id and, only after consumption, distinct stop occurrence/id with cause lineage. **P:** selector then stopping consumer. **Prov:** negative binding then accepted current selection (or separately typed EOF). **L:** two events where both acts occur. **Cur:** selected-before-stop, stopped-after-stop. **U:** general operator preference. **¬:** one `OperatorIngressBoundedStop` must not erase the two acts. |
| content | **E:** local-stop treatment selected; later bounded interaction stop established. **P:** respective owners. **Prov:** exact negative member or EOF-specific cause. **L:** each assertion and linkage. **Cur:** interaction closed after stop. **U:** response meaning beyond local treatment. **¬:** neither is general refusal; EOF is not a negative token. |
| standing | **E:** selection standing and separate stopping standing. **P:** selector/stopping consumer. **Prov:** validated handoff. **L:** event artifacts. **Cur:** only the latter establishes current stopped posture. **U:** future new interaction. **¬:** negative selection alone is not stopping. |
| source / provenance | **E:** full occurrence lineage and separate producer ids. **P:** both owners. **Prov:** causal links. **L:** links without embedding a compiled aggregate. **Cur:** explainable stop cause. **U:** unobserved operator intent. **¬:** causal linkage is not interpretation. |
| responsibility | **E:** selector selects; stop owner validates and stops. **P:** separate boundaries. **Prov:** invocation records. **L:** producer responsibility. **Cur:** no mixed ownership. **U:** none beyond declared owners. **¬:** attempt aggregate is not a substitute for either occurrence. |
| authority / warrant | **E:** negative member warrants selection; current exact selection warrants bounded stopping. **P:** each consumer. **Prov:** guarded inputs. **L:** limits. **Cur:** authority exhausted at local interaction stop. **U:** broader refusal/abandonment. **¬:** no cluster mutation, goal completion, or acquisition decision. |
| scope / locality | **E:** exact interaction/attempt; EOF cause scoped likewise. **P:** stop owner. **Prov:** refs. **L:** scope. **Cur:** closes only this interaction. **U:** other ingress. **¬:** not a global Seed stop. |
| occurrence / preservation | **E:** actual selection invocation and actual stop-consumer invocation. **P:** production road. **Prov:** two ledger assertions in order. **L:** both may be recorded; cluster remains unchanged. **Cur:** projection derives closed/current status. **U:** external receipt. **¬:** `writes_event_ledger=false` cannot support durable stop/currentness history. |

### 4.8 Repeated obstruction, retry, currentness, and supersession occurrences

| Dimension | Cross-examination cell |
| --- | --- |
| identity | **E:** each obstruction finding, policy decision, retry probe/presentation/response, and supersession relation has its own id; recurrence comparison has another. **P:** binder, policy selector, occurrence producers, projector/comparator. **Prov:** ordered lineage. **L:** distinct assertions, not necessarily one event. **Cur:** exact current attempt and scoped recurrence view. **U:** future retry count. **¬:** `OperatorCommonGrammarProbeAttempt` is not all these subjects by identity. |
| content | **E:** nonmembership/Unknown/conflict per attempt; policy-selected retry/stop; `supersedes` relation; recurrence comparison over eligible evidence. **P:** dimension-local owners. **Prov:** recorded events and rules. **L:** inputs/results/limits. **Cur:** latest unsuperseded attempt plus obstruction history. **U:** response meanings and Demand family. **¬:** repeated tokens do not become meaning. |
| standing | **E:** historical occurrence standing survives while active standing changes; recurrence is a derived finding. **P:** event producers and projector/comparator. **Prov:** durable evidence. **L:** occurrence and relation assertions. **Cur:** only projection-selected attempt is response-eligible. **U:** Demand establishment. **¬:** aggregation is not occurrence, Demand, or authority. |
| source / provenance | **E:** complete attempt chain, policy version/input, event order, presentation/response/binding refs. **P:** recorder/projector preserve. **Prov:** ledger sequence plus explicit causal refs; timestamp alone is insufficient. **L:** chain and conflicts. **Cur:** replayable provenance. **U:** causation where not asserted. **¬:** temporal order alone does not prove retry relation. |
| responsibility | **E:** policy selects whether another retry is admitted; producer creates it; projector computes active attempt; recurrence examiner compares. **P:** separate owners. **Prov:** respective artifacts/events. **L:** responsibility per assertion. **Cur:** no attempt object owns policy and projection together. **U:** Demand establisher remains missing. **¬:** application convenience does not transfer constitutional responsibility. |
| authority / warrant | **E:** bounded policy authorizes at most the selected next occurrence, if any; recurrence may warrant Demand examination. **P:** policy/recurrence consumers. **Prov:** policy authority and eligible history. **L:** decisions and limits. **Cur:** next retry allowed or stopped. **U:** whether Demand exists and its family. **¬:** no fixed one-retry authority, automatic Demand, acquisition authority, or Seed goal. |
| scope / locality | **E:** one interaction, declared retry policy, time/as-of boundary, obstruction predicate. **P:** policy/projector. **Prov:** scope fields. **L:** exact locality. **Cur:** scoped currentness and recurrence only. **U:** equivalence across interactions. **¬:** recurrence is not a universal bootstrap condition. |
| occurrence / preservation | **E:** separately recorded attempts, responses, findings, retry decisions, supersession relations; projection is rebuildable. **P:** producers/recorder/projector. **Prov:** event ids and projection rule/as-of. **L:** durable evidence; projection snapshot need not be canonical. **Cur:** derived current attempt and recurrence standing. **U:** discarded occurrences cannot be recovered. **¬:** immutable in-memory aggregate cannot prove durable recurrence, replay, or supersession. |

## 5. Adjudication of PR 2029's proposed artifacts and assertions

| PR 2029 proposal | Category | Fidelity conclusion |
| --- | --- | --- |
| `OperatorIngressOccurrence` | **fake-only scaffolding as proposed**; potentially faithful event artifact | Its fields are useful only when a real free-form shell adapter produces the occurrence and a recorder preserves it. Arbitrary construction is not ingress evidence. |
| `OperatorCommonGrammarProbePresentationOccurrence` | **mixed object** | It may preserve representation formation, but it must not claim emission. Real emitter evidence is a separate occurrence/event, and currentness belongs in projection. |
| `OperatorProbeResponseOccurrence` | **fake-only scaffolding as proposed**; potentially faithful event artifact | It becomes faithful only when produced by the response-reading shell boundary against an emitted presentation. |
| `OperatorCommonGrammarProbeAttempt` | **duplicated compiled structure and mixed object** | It collapses occurrences, retry relation, policy, consumption, currentness, and supersession. Those claims belong to event evidence, relation evidence, policy selection, and projection. |
| `OperatorCommonGrammarProbeSelectionResult` | **mixed object** | A narrow positive treatment-selection event is faithful. Embedding the whole road and negative-authority booleans duplicates upstream evidence and absent downstream warrant. |
| `OperatorIngressBoundedStop` | **faithful event artifact only if competently produced** | A separate stop consumer is correct, but the artifact must record its own occurrence; it is not current closed standing until projection applies it. |
| negative-authority booleans | **duplicated compiled structures** | `false` copies do not establish why authority, Demand, BOGE, execution, or mutation is absent. Projection must expose positive standing, explicit Unknown/conflict/refusal, scope, and missing warrants. |
| `writes_event_ledger=false` | **incorrect application boundary** | Correct for the pure binder itself, incorrect for a production bootstrap road whose occurrences must support currentness, supersession, recurrence, and later Demand examination. Event recording still does not mutate cluster truth. |
| `mutates_projected_state=false` | **category error if read as projection prohibition** | Producers should not directly mutate projected State. The `StateProjector` must nevertheless derive a current bootstrap view by replaying recorded evidence. Projection is not producer mutation. |
| library-only implementation/no shell caller | **fake-only scaffolding** | Tests can witness value behavior, never real ingress, emission, response, or stop occurrences. A runnable production caller is mandatory. |
| fixed one-retry policy | **unwarranted application policy** | No existing canonical authority fixes one retry. Policy may select zero, one, or more within a bounded rule; the selection and each occurrence must be separately evidenced. |

The existing `ClosedChoiceSelectionBinding` and
`bind_closed_choice_selection` survive as faithful, read-only membership
machinery within their exact scope. Their current negative booleans are legacy
boundary disclosures, not a template for a new monolithic protocol result.

## 6. Exact PR 2029 conclusions that survive

1. Preserve exact ingress at the owned capture boundary, name framing/decoding
   loss, and distinguish EOF from empty text.
2. Keep semantic-set identity, represented set identity, and presentation
   occurrence identity distinct.
3. Reuse exact token membership with no trimming, case folding, aliases, label
   matching, prefix matching, integer conversion, or interpretation.
4. Preserve exact-set nonmembership while response meaning, intent, and
   requested treatment remain Unknown.
5. Map a bound member by immutable semantic identity, never its presentation
   label.
6. Keep acquisition-treatment selection separate from applicability,
   mechanism selection, authority, admission, execution, success, common
   grammar, Demand, and BOGE.
7. Keep local-stop-treatment selection separate from a competent stopping act;
   treat EOF as a distinct stopping cause, not a negative token.
8. Reject stale, replayed, mismatched-presentation, mismatched-set, conflicted,
   and provenance-defeated responses before semantic treatment selection.
9. Ensure communication-probe bindings cannot enter the current unsafe
   closed-choice-to-BOGE adapter merely because a token bound.
10. Keep BOGE operator-origin and require preserved ingress to re-enter
    interpretation, warrant, applicability, admission, and BOGE after adequate
    grammar exists.
11. Preserve `mutates_cluster=false` throughout this read-only bootstrap.

## 7. Exact PR 2029 conclusions that must be rejected

1. Reject “application-owned fixed two-treatment probe around the binder” as a
   sufficient vertical slice when no real shell owns ingress and emission.
2. Reject library invocation as implementation witness for any claimed shell
   occurrence.
3. Reject keeping all artifacts only as returned in-memory values. That makes
   recurrence, replay, currentness, and supersession non-durable assertions.
4. Reject `writes_event_ledger=false` for the whole road. Preserve the
   distinction: the binder need not write; a separate recorder records produced
   occurrence/event artifacts.
5. Reject `mutates_projected_state=false` as a reason not to project. Producers
   do not mutate State; replay derives a bounded current view.
6. Reject `OperatorCommonGrammarProbeAttempt` as owner of old/new attempts,
   retry policy, supersession, and currentness.
7. Reject a result object containing `acquisition_authorized=false`,
   `acquisition_begun=false`, `BOGE=false`, `Demand=false`, ledger false, State
   false, and cluster false as dimensional proof. Except where an existing API
   requires compatibility fields, absence of those standings follows from
   missing warrant or explicit Unknown/conflict/scope.
8. Reject a fixed “at most one retry” as the smallest faithful policy. The
   canonical count is unspecified.
9. Reject the claim that adding event kinds or projections would falsely turn
   ephemeral communication into cluster truth. Ledger evidence is not cluster
   truth, and projected current standing is not State-object truth by identity.
10. Reject “implementation-ready” with a seven-file library/test patch that
    explicitly omits the only real producer caller, recorder, and projector.
11. Reject hardening BOGE by adding semantic effect/consumer metadata to every
    generic closed-choice option unless the smallest goal-specific admission
    gate can consume a separately produced eligible selection artifact. Generic
    representation should not become a universal constitutional envelope.

## 8. Corrected minimal production-connected topology

```text
real free-form shell ingress
-> competent ingress occurrence/event production
-> EventLedger / SQLiteEventLedger recording
-> bootstrap projector derives preserved-ingress current standing
-> bounded probe production
-> representation formation
-> real shell emission and presentation occurrence/event
-> event-ledger recording
-> projector derives the current response-eligible presentation
-> real shell response capture and response occurrence/event
-> event-ledger recording
-> exact occurrence/set/currentness validation
-> existing bind_closed_choice_selection
-> binding finding/event recording
-> probe-specific treatment-selection act/event
-> event-ledger recording
-> projector derives selected treatment and current interaction posture
-> negative: separate stop consumer/event -> projection closes interaction
-> unsupported: policy-local retry examination/selection
-> if admitted, fresh separately produced probe/presentation/response events
-> explicit supersession relation/event -> updated current projection
-> recurrence/obstruction comparison over eligible durable evidence
-> possible Demand examination (not automatic establishment)
```

No claim requires every arrow to be one event. In particular, representation
formation is not emission; binding is not treatment selection; policy selection
is not retry execution; selection is not stopping; projection is not event
production; and Demand examination is not Demand establishment.

The shell may keep orchestration small: read one ingress, append the produced
event, replay/project, emit only a currently eligible probe, append emission and
response events, then call narrow consumers. It must not become a global
session controller or interpreter.

## 9. Existing ledger and projector machinery that must be reused

* `seed_runtime.events.EventLedger.append` and `append_many` already preserve
  process-local append order, ids, actor, workspace, session, causation, and
  correlation.
* `seed_runtime.events.SQLiteEventLedger` supplies the existing durable form
  for a shell invoked with a database.
* `seed_runtime.models.Event` supplies the generic immutable record envelope;
  event payload secret rejection remains applicable.
* `seed_runtime.state.StateProjector.project` and `project_from_state` already
  replay workspace-scoped ledger order and expose an as-of event boundary.
* `StateProjector.apply` remains the event-kind dispatch boundary. It must gain
  narrow bootstrap handlers rather than receive direct producer mutations.
* Existing projection publication, replay, and projection-store machinery may
  rebuild/cache the view; a cache snapshot must not become occurrence evidence.
* `PresentedClosedChoiceSet`, `OperatorSelectionTokenCapture`, and
  `bind_closed_choice_selection` remain the exact representation/comparison
  seam after production and currentness validation.
* `establish_bounded_operator_goal_from_admitted_interpretation` remains the
  lawful interpreted-ingress BOGE road. The direct generic closed-choice BOGE
  adapter must refuse probe selection artifacts.

## 10. Only genuinely missing implementation pieces

1. A real free-form bootstrap mode/caller in `scripts/seed_local.py` with
   explicit workspace/session/channel framing and exact capture-loss behavior.
2. Narrow produced event payloads for ingress capture/EOF, probe production,
   presentation emission, response capture/EOF, binding finding, treatment
   selection, stop, retry-policy decision, and supersession. Some adjacent
   assertions may share an event only when producer, occurrence, and warrant
   truly coincide.
3. A small recorder/orchestrator that appends already-produced event artifacts;
   it must not infer their truth while recording.
4. A bootstrap projection/read model preserving the eight dimensions,
   Unknowns/conflicts, history refs, current attempt/presentation/response,
   consumption, stopping, and supersession.
5. A fixed two-treatment probe producer and real renderer/emitter split.
6. Response production plus exact lineage/currentness validation around the
   existing binder.
7. Two narrow treatment-selection outputs and a separate local-stop consumer;
   no omnibus negative booleans.
8. A bounded retry-policy seam whose configured/selected count is evidence,
   not constitutional law, and a recurrence comparator that can orient Demand
   examination without establishing Demand.
9. A BOGE eligibility gate that admits only goal-specific, competently produced
   selection/admission evidence and refuses communication-probe treatment
   selections.
10. Production-connected tests covering shell ingress/emission/response,
    ledger preservation, replay/currentness/supersession, exact binding,
    asymmetric treatment/stop behavior, configurable bounded retry, recurrence
    without Demand, BOGE isolation, and no cluster mutation.

No acquisition provider, grammar learner, Demand establisher, Seed-origin goal,
cluster mutation, general dialogue engine, or interpretation of unsupported
material belongs in this corrected slice.

## 11. Corrected anticipated files and LOC range

| File | Smallest faithful anticipated change | LOC range |
| --- | --- | ---: |
| `scripts/seed_local.py` | explicit real free-form bootstrap caller and narrow stdin/stdout adapter | 55–90 |
| `seed_runtime/operator_ingress_common_grammar.py` | event payload producers, fixed probe representation, response validation, narrow treatment selections, policy seam | 190–260 |
| `seed_runtime/operator_ingress_stopping.py` | separate local-stop/EOF consumer and event production | 35–60 |
| `seed_runtime/operator_ingress_projection.py` | eight-dimensional bootstrap view and replay reducers/currentness rules | 140–210 |
| `seed_runtime/state.py` | dispatch bootstrap event kinds into the dedicated reducer/view | 20–40 |
| `seed_runtime/bounded_operator_goal_establishment.py` | refuse probe treatment selection; require goal-eligible evidence | 15–30 |
| `seed_runtime/__init__.py` | bounded exports | 10–20 |
| `tests/test_operator_ingress_common_grammar.py` | exact local producer/consumer asymmetry and Unknown boundaries | 130–190 |
| `tests/test_operator_ingress_bootstrap_cli.py` | real caller, output, EOF, recording, retry policy | 130–200 |
| `tests/test_operator_ingress_projection.py` | replay, currentness, consumption, supersession, recurrence, no Demand/cluster mutation | 150–220 |
| `tests/test_bounded_operator_goal_establishment.py` | communication-probe refusal and lawful goal fixture | 20–40 |
| **Total** | **eleven anticipated files** | **895–1,360** |

This range is deliberately larger than PR 2029's library-only estimate because
production occurrence, recording, and projection are part of fidelity, not
optional later wiring. It remains bounded: it reuses the generic event envelope,
both ledgers, projector replay, exact closed-choice binder, and existing BOGE
road rather than creating a protocol framework.

## 12. Implementation / no-implementation verdict

**Verdict: no implementation from PR 2029's proposed topology.** PR 2029 is a
useful local artifact inventory and preserves the exact-set and treatment
asymmetries listed in section 6, but its proposed slice must not be implemented
as written. It has no competent production caller, rejects required durable
evidence and dimensional projection, duplicates absent authority as booleans,
and constitutionalizes an unsupported retry count.

Implementation may proceed only as the corrected production-connected slice in
sections 8–11: event producers do not become recorders, records do not become
truth, projectors do not manufacture occurrences, current views do not erase
history, treatment selection does not execute treatment, recurrence does not
establish Demand, Demand does not confer authority, common-grammar prerequisite
movement does not become BOGE, and BOGE never becomes Seed-origin.

This report is **404 LOC**.
