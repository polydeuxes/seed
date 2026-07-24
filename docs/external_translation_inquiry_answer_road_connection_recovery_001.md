# External Translation Inquiry Answer Road Connection Recovery 001

This is one bounded, report-only constitutional road-connection recovery on current merged `main` after PR 1944. It changes no production code, tests, fixtures, CLI behavior, persistence, events, exports, canonical Book chapters, or existing reports.

## Governing question

Does all externally supplied material first cross an external-translation boundary, after which translated world material, operator inquiry, testimony, correction, movement requests, and other material may lawfully enter different Seed-native competency roads -- and what exact producer -> standing -> consumer connections currently exist or remain absent from translated operator inquiry through bounded Answer, presentation, rendering, and optional preservation?

## Classification vocabulary

Findings use: `evidenced`, `partially evidenced`, `compatibility-only`, `compressed`, `absent`, and `Unknown`.

## Witnesses inspected

Repository searches were bounded to external grammar/translation, inquiry, Answer, presentation, rendering, retention/preservation, Demand, Observation/Evidence, competency, diagnostic, and federation terms across `docs`, `book_of_seed`, `seed_runtime`, and `tests`. Principal witnesses were:

- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`
- `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`
- `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `docs/operational_realization_external_grammar_recovery_001.md`
- `docs/frontier_question_answer_presentation_connection_recovery_001.md`
- `docs/inquiry_orientation_answer_presentation_current_road_recovery_001.md`
- `docs/ephemeral_read_only_inquiry_constitutional_boundary_recovery_001.md`
- `docs/cross_seed_provenance_and_federation_reconciliation.md`
- `seed_runtime/external_material_testimony_binding.py`
- `seed_runtime/external_material_structural_projection.py`
- `seed_runtime/candidate_external_grammar.py`
- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/shared_explanation_membership_evidence_projection.py`
- `seed_runtime/shared_explanation_membership_evidence_set.py`
- `seed_runtime/shared_explanation_presentation_admission.py`
- `seed_runtime/shared_explanation_encounter_sequencing.py`
- `seed_runtime/shared_explanation_bounded_composition.py`
- `seed_runtime/shared_explanation_rendering_projection.py`

PR 1942, PR 1943, and PR 1944 reports are treated as immutable testimony, not canonical amendments.

## 1. Current external-translation topology

The strongest evidenced external-material road is local and preservation-first:

```text
externally supplied material
-> source identity / representation manifest
-> selected artifact identity, hash, bounds, Unknowns
-> validated testimony reference binding
-> mechanical structural projection where requested
-> candidate external-grammar hypotheses where supplied
-> possible later Seed-native consumer
```

Implementation evidence supports discrete producers:

| Producer | Produced artifact or relation | Standing | Consumer currently evidenced |
|---|---|---|---|
| `ExternalMaterialManifest.from_json_dict` / caller-supplied manifest records | source, selected artifact, annotation, unknown records | `evidenced` source and representation preservation input | testimony-binding validator and structural projection request |
| `validate_external_material_testimony_bindings` | `ExternalMaterialTestimonyBindingSet` with valid reference spans | `evidenced` referential integrity only | external-grammar/candidate testimony consumers by reference |
| `project_external_material_structure` | line and nonblank-region projection | `evidenced` mechanical representation projection | diagnostic/translation investigations and candidate grammar work |
| `assemble_candidate_external_grammar_set` | caller-supplied candidate grammar hypotheses | `evidenced` as hypotheses, not truth or translator capability | human/operator/report review and diagnostics |

This topology preserves exact material identity and reference integrity before interpretation. It does not by itself prove semantic translation, Seed-native constitutional admission, Observation, Evidence, Question, Demand, or Answer standing.

## 2. Exact classification: universal or local external translation

Classification: `partially evidenced` / `compressed` for "external translation as universal crossing"; `evidenced` for several local external-translation roads.

Current Book grammar says external and constitutional grammar differ and that external material must not inject native constitutional standing merely because its wording has a familiar shape. Current question grammar specifically says question-shaped external material is testimony, not an internal constitutional question, and requires bounded translation before Seed-owned internal inquiry. That supports a broad constitutional discipline: external wording must cross a boundary before Seed-native standing is claimed.

However, the implementation does not expose one universal crossing artifact or registry that every external input must traverse. Instead, the repository contains local roads: external material testimony binding, mechanical structural projection, candidate grammar preservation, bounded constitutional question production from explicit caller fields, inquiry-note orientation, Observation ingestion, Demand/authority boundaries, and request-shaped representation grammar. Therefore:

```text
external translation as discipline: evidenced
external translation as single universal implementation crossing: absent
all external inputs become one standing after translation: absent
several local external-translation roads: evidenced
```

Forbidden reverse inference: because a road accepts external material, the road does not prove that all external material has crossed that same road, or that external material has become Seed-native truth.

## 3. Road matrix for translated material by standing

| Translated material standing | Smallest lawful road | Current status | Protected non-inference |
|---|---|---|---|
| world material | attributed source/representation -> possible testimony binding -> possible Observation/Evidence road | `partially evidenced`; source and binding are evidenced, semantic Observation/Evidence admission is road-local | external text != Observation; valid span != support; Evidence-shaped material != admitted Evidence |
| operator inquiry | attributed inquiry material -> bounded interpretation/preparation -> relevant read-only competencies -> bounded answer material -> presentation/view -> rendering -> emission | `partially evidenced` for inquiry-note road; `compatibility-only` for constitutional Answer standing | external query != Observation; translated query != asserted fact; query interpretation != admission |
| operator testimony or correction | attributed expression -> constitutional ingress/admission -> possible durable testimony/correction/Question/Facts | `compatibility-only` in reports and Book grammar; no universal implementation path recovered here | testimony != fact; correction offered != correction established |
| request for movement | request-shaped representation -> Demand/authority/selection boundaries -> possible movement | `partially evidenced` as local Demand/authority grammar; absent as automatic consequence of wording | request wording != authority; movement request != movement selected or completed |
| provider/adapter result | provider output -> attributed external testimony/result -> local comparison/admission/reliance if warranted | `compatibility-only` from representation/federation grammar and adapter capabilities | provider capability != constitutional competency; provider response != local truth |
| diagnostic output | diagnostic run scoped output -> optional record as diagnostic_run subject | `evidenced` in diagnostic inventory discipline, outside this report's change | diagnostic finding != cluster truth |

## 4. Current inquiry -> competency -> Answer road

The smallest evidenced current read-only inquiry road is the inquiry-note orientation road recovered by PR 1943/1944 testimony and implementation:

```text
client/operator text
-> record_inquiry_note(... raw_note ...)
-> InquiryNoteRecord(note_id, raw_note, recorded_at, source, workspace_id, session_id)
-> build_inquiry_orientation(projected State, note)
-> _prepare_inquiry_orientation_composition(note)
-> lexical tokens
-> _collect_inquiry_orientation_evidence(projected State, request)
-> projected fact-support/source-navigation matches
-> _prepare_inquiry_orientation_selected_material
-> _InquiryOrientationAnswer
-> InquiryOrientationView
-> format_inquiry_orientation
-> CLI print / external emission by the local shell
```

Classification by crossing:

| Crossing | Source standing | Producer | Consumed material | Warrant | Produced standing | Identity/provenance | Scope/authority/time | Consumer | Occurrence/preservation status | Forbidden reverse inference | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw query -> record | client/session inquiry material | `record_inquiry_note` | raw note, workspace/session ids | explicit `--record-inquiry-note`; non-empty validation | `InquiryNoteRecord` | note id, raw note, UTC timestamp, source, workspace/session | local JSONL store; read-only authority boundary | selection/orientation builder | persisted outside event ledger | query retained != query admitted | `evidenced` |
| record -> composition request | preserved inquiry-note material | `_prepare_inquiry_orientation_composition` | raw note | deterministic tokenization | implementation-local composition request | note object retained | lexical only; no semantic interpretation | answer composition | ephemeral computation | query interpretation != admission | `evidenced` |
| composition -> evidence selection | projected-State read model | `_collect_inquiry_orientation_evidence` | note tokens and projected State | deterministic lexical overlap | related material candidates | labels, support strings, surface family | current projected State only | selected-material preparer | ephemeral computation | selected material != admitted evidence | `evidenced` |
| selected material -> answer-shaped payload | implementation-local selected material | `_prepare_inquiry_orientation_answer` and helpers | selected related material/support | local deterministic composition | `_InquiryOrientationAnswer` | support and boundary strings | read-only, no providers/tools/events/mutation | `InquiryOrientationView` | ephemeral computation | Answer-shaped payload != durable Answer | `evidenced` for local result; `compatibility-only` for constitutional Answer |
| answer -> view/presentation | implementation-local answer | `build_inquiry_orientation` | answer fields | dataclass assembly | `InquiryOrientationView` | note plus related material | no presentation-admission artifact | formatter | ephemeral view | view != canonical presentation | `evidenced` operationally; `compressed` constitutionally |
| view -> rendering | view | `format_inquiry_orientation` | view fields | formatter | text rendering | visible fields preserve boundaries | display-only | CLI print/API caller | occurrence depends on caller surface | rendering != emission/receipt | `evidenced` |
| rendering -> emission | rendered text | `scripts.seed_local` CLI print path | formatted response | process stdout | emitted representation candidate | shell process context | no proof of delivery/receipt/uptake | external operator/client | emission only | emission != reliance | `partially evidenced` |

This road consumes translated inquiry standing only in a limited sense: the record has client/session inquiry-note standing plus explicit negative authority text. It mostly consumes raw client material and lexical query material. It does not consume an already-durable constitutional Question. It also does not establish a general constitutional Answer object.

## 5. Exact missing connections

The following connections remain absent or only compatibility-supported:

1. A universal external-translation crossing used by every external input: `absent`.
2. A current producer that converts translated operator inquiry into durable Seed-owned bounded Question standing as part of the inquiry-note road: `absent`.
3. A current producer that connects `InquiryNoteRecord` or `_InquiryOrientationAnswer` to an independently evidenced constitutional `Answer` standing: `absent`.
4. A general Answer registry, Answer subject, or Answer artifact preserving inquiry identity, bounded Question identity, support, derivation, Unknowns, conflicts, limitations, sufficiency, occurrence, durability, and permitted downstream movement: `absent`.
5. A producer connecting answer-shaped payloads into the surviving `SharedExplanation*` presentation admission, sequencing, bounded composition, and rendering road: `absent`.
6. A crossing proving presentation candidate -> rendering -> emission -> delivery -> receipt -> interpretation -> uptake -> reliance: all after emission are `absent` unless separately evidenced.
7. A retention-selection boundary for automatically preserving read-only inquiry as client history, research backlog, operator testimony, durable constitutional Question, or learned answer: `absent` in the current inquiry road.
8. A federation implementation path for query emission, foreign Seed response, local comparison, admission, and reliance: `absent`; topology compatibility only.

## 6. Presentation and rendering connection topology

Two presentation families are visible and must not be collapsed.

### Inquiry-orientation presentation/rendering

```text
implementation-local answer material
-> InquiryOrientationView
-> format_inquiry_orientation
-> process stdout / caller response
```

This is operationally evidenced. Its presentation candidate preserves the inquiry note, related material, uncertainty, and authority boundary, but it does not preserve all requested constitutional coordinates as structured fields. It is therefore `compressed` as constitutional presentation and `evidenced` as a bounded local View/rendering.

### Shared-explanation presentation/rendering

```text
stage-owned explanation / membership evidence
-> membership evidence projection or set
-> presentation-local admission
-> encounter sequencing
-> bounded composition
-> rendering projection over one stage-owned explanation
```

Surviving shared-explanation artifacts evidence important distinctions:

```text
belongs != admitted
admitted != sequenced
sequenced != composed
composed != rendered
rendered != emitted
```

They are not canonical realizations of every Seed presentation. They are local artifacts over shared explanation membership and stage-owned explanations. Their existence is strong evidence that presentation responsibilities can preserve source identity, bounded inquiry refs, demand refs, admission evidence, Unknowns, conflicts, non-admission, and read-only/non-mutation boundaries. They do not evidence a completed upstream Answer-to-presentation candidate road, and they do not evidence external emission or consumer uptake.

Can presentation consume both durable constitutional inquiry and interaction-local read-only inquiry? Classification: `compatibility-only` / `partially evidenced`. Book communication grammar permits bounded representation of source material without strengthening standing, so both durable and interaction-local sources can be represented if their source standing, authority, scope, Unknowns, and limits survive. Current implementation evidences a local read-only view and separate durable-ish shared-explanation inquiry refs, but no common presentation boundary that accepts both.

Minimum source standing a presentation candidate must preserve:

```text
inquiry identity or interaction identity;
answer/result identity;
durability and occurrence standing;
scope and authority;
evidence/support basis;
Unknowns, conflicts, limitations, refusals;
consumer locality;
permitted and prohibited downstream movement;
negative authority that rendering and emission do not strengthen standing.
```

## 7. Occurrence and preservation distinctions

The current repository supports this stronger distinction than "durable inquiry only":

```text
constitutional standing != durable standing
constitutional act != event
interaction-local Question or Answer != durable Question or Answer
```

PR 1944's claim that Seed-owned Question formation belongs primarily to durable inquiry remains valid testimony for the durable road, but it is not the strongest universal distinction. The Book says bounded translation and Seed-owned question formation are constitutional requirements, while implementation shows read-only artifacts can preserve explicit caller inputs, Unknowns, no-ledger writes, and no mutation. Therefore a read-only interaction may be constitutionally bounded without becoming durable. Whether a particular temporary computation has constitutional Question or Answer standing remains `Unknown` unless the boundary explicitly preserves the required identity, provenance, scope, authority, evidence demand/support, Unknowns, occurrence, and lawful stop limits.

Protected distinctions:

- `external query != Observation`
- `translated query != asserted fact`
- `query interpretation != admission`
- `competency invocation != durable learning`
- `Answer produced != Answer preserved`
- `presentation != rendering`
- `rendering != emission`
- `emission != delivery, receipt, interpretation, uptake, or reliance`

## 8. Optional retention branch and ownership

The lawful optional preservation branch is separate:

```text
interaction-local query
-> retention candidate
-> declared retention purpose
-> authority and scope
-> explicit selection or policy
-> preserved material with declared standing
```

Possible preserved standings must remain distinct:

| Preserved standing | Owner / authority | Current evidence | Non-collapse |
|---|---|---|---|
| client/session history | client shell, adapter, or explicit local store | inquiry-note JSONL store preserves note/session/workspace when flag used | session history != Seed memory |
| research backlog | operator or governance policy | `Unknown` in this inquiry road | interesting query != backlog item |
| future inquiry candidate | Seed/operator selection boundary | `compatibility-only` from inquiry grammar | candidate != opened inquiry |
| operator testimony | constitutional ingress boundary | `compatibility-only` | testimony != fact |
| durable constitutional Question | Seed-owned question producer with preserved fields | `partially evidenced` in `produce_bounded_constitutional_question`, absent from inquiry-note road | durable Question != answer learned |
| learned answer or established fact | evidence/admission/learning boundary | `absent` from read-only inquiry road | answer preserved != answer learned |

Current evidence permits explicit caller persistence through `--record-inquiry-note` and explicit caller-supplied bounded-question fields through `produce_bounded_constitutional_question`. It does not evidence automatic family-local retention, Seed-owned nomination authorization, or an operator-established retention policy applied to this query road. `Seed nominates retention != retention authorized`; no nomination road was recovered.

## 9. Narrow federation compatibility finding

Classification: `compatibility-only`.

Existing federation testimony supports this grammar:

```text
Seed A bounded inquiry
-> external query emission
-> Seed B receives attributed material through its own external boundary
-> Seed B produces bounded response or warrant testimony
-> Seed A receives attributed external testimony
-> Seed A performs local comparison, admission, reliance, or refusal if warranted
```

No implementation path was recovered for federated query dispatch or Answer import. The compatible grammar is evidence-transfer, not truth-transfer:

```text
foreign Seed Answer != local truth
foreign warrant != local warrant automatically
agreement != fact
federated recurrence != authority
```

## 10. Producer -> artifact/relation -> consumer evidence

| Producer | Artifact/relation | Consumer | Classification |
|---|---|---|---|
| `validate_external_material_testimony_bindings` | valid material span binding only | candidate external grammar/testimony references | `evidenced` |
| `project_external_material_structure` | mechanical line/region projection | structural diagnostics and external grammar inquiries | `evidenced` |
| `assemble_candidate_external_grammar_set` | candidate grammar hypothesis set | reports/diagnostics/operator review | `evidenced` |
| `produce_bounded_constitutional_question` | bounded question from explicit caller fields | formatter/JSON/caller | `evidenced` locally; `absent` as inquiry-note consumer |
| `record_inquiry_note` | persisted inquiry-note record | `select_inquiry_note`, `build_inquiry_orientation` | `evidenced` |
| `_compose_inquiry_orientation_answer` | implementation-local answer-shaped result | `InquiryOrientationView` | `evidenced` local result; `compatibility-only` constitutional Answer |
| `build_inquiry_orientation` | `InquiryOrientationView` | `format_inquiry_orientation` | `evidenced` |
| `format_inquiry_orientation` | rendered text | CLI stdout/caller | `evidenced` rendering; `partially evidenced` emission |
| `admit_shared_explanation_presentation` | presentation-local admission | encounter sequencing | `evidenced` for shared-explanation family |
| `project_shared_explanation_rendering` | rendering projection for one stage-owned explanation | formatter | `compressed`; generic function rejects unknown explanation types |

## 11. Contradictions among Book grammar, reports, and implementation

1. Book question grammar emphasizes Seed-owned internal Question formation after bounded translation. Implementation's `BoundedConstitutionalQuestion` preserves explicit caller-supplied fields and refuses natural-language classification, authority creation, event writes, and durable knowledge creation. This is not a direct contradiction, but it is a compression: current implementation can preserve caller-shaped bounded fields without proving Seed has performed a full constitutional question-forming act.
2. PR 1944 testimony emphasizes durable inquiry as the primary home of Seed-owned Question formation. Current implementation and Book communication grammar support read-only bounded constitutional discipline without event or mutation. The stronger distinction is occurrence/durability, not constitutional/non-constitutional.
3. Inquiry orientation uses words such as "preserved operator prose" and `_InquiryOrientationAnswer`, but its authority boundary says the note is not fact, goal, authorization, command, or instruction, and the answer is implementation-local. The names overstate constitutional standing if read as durable inquiry or Answer.
4. Shared-explanation artifacts evidence membership, admission, sequencing, composition, and rendering boundaries, but PR/report vocabulary sometimes invites a presentation pipeline reading. Current evidence does not connect those artifacts to inquiry-note answers or universal presentation.
5. External-grammar reports support broad translation discipline, while implementation exposes local external-material artifacts. The universal crossing remains conceptual discipline, not a single implemented gate.

## 12. Strongest Unknowns

1. Whether the repository intends to recognize interaction-local constitutional Answer standing as a named standing without durability.
2. Whether any existing durable inquiry road, outside the bounded witnesses inspected here, connects translated operator inquiry to Answer standing through internal competencies.
3. Which producer, if any, is responsible for turning an answer-shaped local competency result into a presentation candidate with all constitutional coordinates preserved.
4. Whether presentation responsibilities are intended to have one common boundary over durable and interaction-local inquiries or remain family-local.
5. Whether operator-established retention policy exists anywhere outside explicit caller persistence surfaces.
6. Whether learned external-grammar competency can be invoked by read-only inquiry roads without preservation, and what standing its outputs would have.
7. Whether provider/adapter capability outputs can ever be Answer material directly, or only external testimony for local comparison.
8. Whether federated query response is intended to be a bounded Answer exchange, warrant testimony exchange, or ordinary external testimony import.

## 13. Smallest next honest road-connection inquiry

The smallest next honest inquiry is not implementation design. It is a bounded evidence recovery of one concrete road:

```text
Does any current producer consume a translated operator inquiry or bounded constitutional Question and produce an Answer-standing artifact -- distinct from a View, local result, diagnostic output, or presentation candidate -- while preserving inquiry identity, provenance, authority, scope, support, Unknowns, occurrence standing, durability standing, and downstream movement limits?
```

That inquiry should inspect only current Answer-shaped producers and tests, classify each as Answer standing, answer-shaped payload, View, local competency result, diagnostic output, or presentation candidate, and stop before recommending architecture.
