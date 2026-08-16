# Inquiry Orientation Answer Presentation Current Road Recovery 001

This is one bounded, report-only current-road recovery of `seed_runtime/inquiry_orientation.py` on current merged `main` after PR 1942. It changes no production code, tests, fixtures, CLI behavior, persistence, events, exports, Book chapters, or existing reports.

## Governing question

What exact producer -> artifact -> consumer road currently exists from preserved inquiry note through evidence collection, answer composition, View assembly, and rendering, and what constitutional responsibilities or compressions does that road demonstrate relative to the frontier -> Question -> Answer -> presentation -> rendering topology recovered by PR 1942?

## Classification vocabulary

Findings use these labels: `faithful within scope`, `compressed but separable`, `compatibility-only`, `foreign crossing`, `absent`, and `Unknown`.

## 1. Exact current road

```text
record_inquiry_note(...)
  -> InquiryNoteRecord
  -> _prepare_inquiry_orientation_composition(...)
  -> _InquiryOrientationCompositionRequest
  -> _collect_inquiry_orientation_evidence(...)
  -> _InquiryOrientationEvidence
  -> _prepare_inquiry_orientation_selected_material(...)
  -> _InquiryOrientationSelectedMaterial
  -> _prepare_inquiry_orientation_answer_payload(...)
  -> _InquiryOrientationAnswerPayload
  -> _assemble_inquiry_orientation_answer_artifact(...)
  -> _InquiryOrientationAnswer
  -> build_inquiry_orientation(...)
  -> InquiryOrientationView
  -> format_inquiry_orientation(...)
  -> formatted output string
  -> CLI print / knowledge-reachability internal surface scan
```

The active CLI road is:

```text
scripts.seed_local --record-inquiry-note TEXT
  -> record_inquiry_note(...)
  -> isolated JSONL record

scripts.seed_local --inquiry-orientation [NOTE_ID]
  -> select_inquiry_note(...)
  -> build_inquiry_orientation(projected_state_from_args(args), note)
  -> format_inquiry_orientation(...)
  -> print(...)
```

The road is production-active as module code, CLI-active through `scripts.seed_local`, test-active through `tests/test_inquiry_orientation.py`, and internally constructible through direct helper calls. The private dataclass crossings are implementation-local and test-constructible; the public operational entry points are `record_inquiry_note`, `select_inquiry_note`, `build_inquiry_orientation`, and `format_inquiry_orientation`.

## 2. Producer -> artifact -> consumer table

| Crossing | Exact producer | Consumed standing | Produced artifact or relation | Identity/provenance preserved | Evidence or warrant used | Consumer | Scope and authority limits | Forbidden reverse inference | Active status | Classification |
|---|---|---|---|---|---|---|---|---|---|---|
| Raw operator prose -> preserved note | `record_inquiry_note` | Non-empty raw operator prose plus optional workspace/session/time | `InquiryNoteRecord` appended as JSONL | `note_id`, exact `raw_note`, UTC `recorded_at`, `source`, optional `workspace_id`, optional `session_id` | Non-empty validation and caller-provided/store-provided metadata | `load_inquiry_notes`, `select_inquiry_note`, tests, CLI orientation | Store is isolated outside event ledger; note is not fact/claim/goal/authorization/command/instruction | Preserved prose is not interpreted operator intent, cluster truth, requirement, authorization, or next action | production-active, CLI-active, test-active | faithful within scope |
| Preserved note -> composition request | `_prepare_inquiry_orientation_composition` | One `InquiryNoteRecord` | `_InquiryOrientationCompositionRequest(note, note_tokens)` | Full note object retained; derived token set adds no new provenance identity | `_note_tokens(note.raw_note)` case-normalized regex tokens of length >= 3 | `_compose_inquiry_orientation_answer`, tests | Tokenization prepares lexical orientation only; no rendering, state query, semantic interpretation, or question standing | Token overlap vocabulary is not semantic interpretation or constitutional Question formulation | production-active via build, test-active, constructible-only as private helper | faithful within scope |
| Composition request -> collected evidence | `_collect_inquiry_orientation_evidence` | Projected `State` plus request tokens | `_InquiryOrientationEvidence(related_material)` | Related-material rows preserve material type, label, surface, support, why-related, surface family; request note identity is not carried in evidence artifact | `_fact_matches` over `state.fact_supports`; `_source_navigation_matches` over `build_source_navigation(state, token)` | `_prepare_inquiry_orientation_selected_material`, tests | Collection is deterministic lexical overlap against projected read models/source-navigation; it does not admit evidence to a constitutional question | Collected material is not admitted evidence; source-navigation/fact matches do not establish relevance, importance, ownership, concern, or intent | production-active via build, test-active, constructible-only as private helper | compressed but separable |
| Collected evidence -> selected material | `_prepare_inquiry_orientation_selected_material` via `_select_inquiry_orientation_related_material` and `_prepare_inquiry_orientation_support` | `_InquiryOrientationEvidence` | `_InquiryOrientationSelectedMaterial(related_material, support)` | Related-material rows and support strings are preserved; note identity remains absent | Sort/dedupe by related-material keys and cap at `_MAX_RELATED_ITEMS` | `_prepare_inquiry_orientation_answer`, tests | Selection is bounded slice/cap and support preservation; no semantic admission or Answer standing | Selected material is not constitutional Answer standing and is not proof that material is important or sufficient | production-active via build, test-active, constructible-only as private helper | faithful within scope for bounded selection; absent as admission |
| Selected material -> answer payload | `_prepare_inquiry_orientation_answer_payload` | `_InquiryOrientationSelectedMaterial` | `_InquiryOrientationAnswerPayload` with `answer`, `reason`, `support`, `boundary`, `limitations` | Carries selected rows and support strings; carries boundary/limitation text; still no note id, question id, admitted-evidence id, sufficiency, conflict, or Unknown structure | Reason selector states deterministic lexical overlaps; boundary selector returns fixed authority boundary; limitation selector switches on whether selected material exists | `_assemble_inquiry_orientation_answer_artifact`, tests | Prepares fields only; no rendering or transport change; no constitutional derivation | Answer-shaped payload is not automatically constitutional Answer | production-active via build, test-active, constructible-only as private helper | compatibility-only / compressed but separable |
| Answer payload -> local answer artifact | `_assemble_inquiry_orientation_answer_artifact` | `_InquiryOrientationAnswerPayload` | `_InquiryOrientationAnswer` | Copies answer rows, reason, support, boundary, limitations exactly | Dataclass assembly from prepared fields | `build_inquiry_orientation` through `_prepare_inquiry_orientation_answer` and `_compose_inquiry_orientation_answer`, tests | Local artifact is explicitly implementation-local answer composition before rendering | `_InquiryOrientationAnswer` name does not prove bounded constitutional Answer standing | production-active via build, test-active, constructible-only as private helper | compatibility-only |
| Local answer -> View | `build_inquiry_orientation` | Projected `State` and `InquiryNoteRecord`; internally consumes `_InquiryOrientationAnswer` | `InquiryOrientationView(note, related_material, uncertainty, authority_boundary)` | Restores full note identity/provenance into View; maps answer rows, limitations, boundary; drops answer reason/support list except support embedded in related rows | Internal composition road result | `format_inquiry_orientation`, CLI, knowledge-reachability scan, tests | View assembly adapts local answer material to public orientation view; it does not render or emit by itself | View is not rendering, presentation admission, or constitutional Answer | production-active, CLI-active, test-active | compressed but separable |
| View -> formatted output | `format_inquiry_orientation` | `InquiryOrientationView` | Plain text string with sections: inquiry note, potentially related material, support/why related, uncertainty, authority boundary | Renders raw note, selected rows, why-related/support strings, uncertainty, authority boundary; no separate render identity/provenance artifact | Direct deterministic text formatting | CLI `print`; internal knowledge-reachability `_inquiry_surfaces`; tests | Rendering is text formatting only; it does not emit until a caller prints/uses it and does not mutate state | Rendering is not emission, and rendering does not strengthen source standing | production-active, CLI-active, test-active | faithful within scope for formatting; absent as constitutional rendering artifact |
| Formatted output -> outward use | CLI `print`; `_inquiry_surfaces` in knowledge reachability | Output string | Terminal emission or internal surface string list | CLI preserves text only; knowledge reachability uses presence/absence of deterministic related material string | CLI dispatch and internal scan | User/operator or knowledge-reachability audit internals | CLI emission is operational output, not delivery/receipt/uptake/reliance; knowledge-reachability scan is not inquiry-orientation consumer standing | Emitted/read string is not proof of constitutional Answer or presentation fidelity | CLI-active; internal active | foreign crossing / compatibility-only |

## 3. Standing carried at every crossing

1. `InquiryNoteRecord` carries preserved operator ingress: exact raw prose, note id, timestamp, source, workspace id, and session id. It carries no fact, claim, goal, requirement, capability, decision, plan, authorization, command, runtime instruction, or Question standing.
2. `_InquiryOrientationCompositionRequest` carries the full note plus deterministic lexical tokens. It preserves operator ingress identity by retaining `note`; it does not preserve a separate derivation id for tokenization and does not formulate a Question.
3. `_InquiryOrientationEvidence` carries collected `RelatedMaterial` only. It drops note identity and request tokens. Its standing is collected lexical material from projected state/source-navigation, not admitted evidence.
4. `_InquiryOrientationSelectedMaterial` carries selected related material plus support strings. It does not carry the note, boundary, limitations, or reason. Its standing is bounded selected material, not Answer standing.
5. `_InquiryOrientationAnswerPayload` carries answer-shaped fields: related material under `answer`, reason string, support strings, boundary, and limitations. Its standing is prepared local composition fields, not a constitutional Answer.
6. `_InquiryOrientationAnswer` copies the payload into an implementation-local answer composition artifact. It preserves support, boundary, limitations, and related rows but does not carry note id, question id, admitted-evidence identity, derivation identity, sufficiency, conflicts, Unknowns as structured standing, or lawful next movement.
7. `InquiryOrientationView` carries public view standing: note, related material, uncertainty, authority boundary. It does not carry the local answer's `reason` field or top-level support list, and it is not itself rendering or emission.
8. Formatted output carries rendered text sections. It has no independent rendering artifact identity, no emission occurrence identity, and no outward Fidelity finding.

## 4. Active entry points and current consumers

- `record_inquiry_note` is active through `--record-inquiry-note`; it appends the raw note and prints only the note id.
- `select_inquiry_note` is active through `--inquiry-orientation`, selecting either latest note or requested note id.
- `build_inquiry_orientation` is active through CLI orientation, through knowledge-reachability's internal inquiry surface scan, and through tests.
- `format_inquiry_orientation` is active through CLI `print`, knowledge-reachability's internal string scan, and tests.
- Private helpers and private dataclasses are production-active by being called from `build_inquiry_orientation`, but external use is constructible-only/test-only because they are implementation-local.

## 5. Constitutional acts actually performed

| Responsibility prompt | Current implementation result | Classification |
|---|---|---|
| operator ingress preservation | Exact raw prose and minimal provenance are preserved outside the event ledger. | faithful within scope |
| Question standing | No bounded Question producer is present; tokenization is not question formulation. | absent |
| evidence collection | Projected fact supports and source-navigation matches are collected by deterministic lexical overlap. | faithful within scope |
| evidence admission | No question-relative admission boundary is implemented; selected material is a slice, not admitted evidence. | absent |
| Answer standing | `_InquiryOrientationAnswer` is local answer-shaped composition material, not enough for constitutional Answer standing. | compatibility-only |
| presentation relevance | The module labels material as potentially related and provides `why_related`; relevance is lexical and explicitly uncertain. | compressed but separable |
| presentation admission | No admitted-to-presentation artifact or admission warrant exists. | absent |
| sequencing | Sort/dedupe/cap create deterministic order, but no constitutional encounter sequencing. | compatibility-only |
| composition | Local composition assembles selected rows, supports, reason, boundary, and limitations. | compressed but separable |
| View projection | `build_inquiry_orientation` projects local composition into `InquiryOrientationView`. | faithful within scope |
| rendering | `format_inquiry_orientation` renders text sections. | faithful within scope for text formatting |
| emission | CLI `print` emits operational text; the module itself only formats. | foreign crossing / compatibility-only |

## 6. Cross-examination of named materials

- **Raw operator prose:** preserved as `raw_note`; not interpreted as fact, intent, concern, recommendation, command, or safe move.
- **Deterministic lexical overlap:** `_note_tokens`, `_overlap`, `_fact_matches`, and `_source_navigation_matches` provide lexical matching only. Lexical match is not semantic interpretation.
- **Projected State material:** `state.fact_supports` and source-navigation views are read-model inputs. Projected material may be collected; collection is not admission.
- **Support strings:** support is preserved in each `RelatedMaterial` and copied into selected material, payload, and local answer. The public View keeps support inside related rows but drops the local answer's separate support list.
- **Authority boundary:** fixed boundary text refuses fact/claim/goal/tool/requirement/capability/decision/proposal/plan/authorization/command/instruction standing and refuses importance, ownership, intent, concern, recommended action, and next-safe-move assertions.
- **Limitations:** limitation text distinguishes match and no-match cases but remains string-level uncertainty, not structured Unknown/conflict/sufficiency standing.
- **Selected related material:** deduped/capped related rows are selected for the orientation view; selected material is not Answer standing.
- **Answer composition:** composition prepares answer-shaped local material from selected related material and fixed selector strings; it has no question identity or admitted evidence boundary.
- **InquiryOrientationView:** the View is a public carrier of note, related material, uncertainty, and authority boundary; it collapses answer material into a prebuilt View rather than performing independent presentation admission/relevance/sequencing responsibilities.
- **Text formatting:** formatting renders View fields into required V1 sections. Formatting is not emission until called by CLI print or another consumer.

## 7. Compressed or bypassed boundaries

| Boundary | Current road behavior | Classification |
|---|---|---|
| Frontier -> Question | Not present in this module. | absent |
| Preserved note -> Question | Bypassed; preserved note becomes tokenized composition request, not Question standing. | absent |
| Question + admitted evidence -> Answer | Bypassed; no Question, no admission, no constitutional Answer. | absent |
| Collected material -> admitted evidence | Compressed into selected material by sort/dedupe/cap only; no admission artifact. | compressed but separable |
| Selected material -> Answer-shaped payload | Implemented as local field preparation; constitutional Answer standing remains absent. | compatibility-only |
| Answer -> presentation candidate | Bypassed; `_InquiryOrientationAnswer` is mapped directly into View fields. | absent |
| Presentation relevance/admission/sequencing/composition | Relevance is lexical `why_related`; admission and encounter sequencing are absent; composition is local answer/View assembly. | compressed but separable / absent |
| View -> rendering | Implemented by formatter but without separate rendering identity/provenance artifact. | faithful within scope / compatibility-only |
| Rendering -> emission | Outside module; CLI print emits text operationally. | foreign crossing |

## 8. Fidelity assessment against PR 1942

PR 1942 recovered missing crossings in the broader topology:

```text
BoundedInquiryFrontier -> Question
Question + admitted evidence -> Answer
Answer/derivation -> presentation candidate
presentation -> rendering
```

Against that topology, this module:

- **Implements:** preserved operator ingress; deterministic evidence collection from projected read models; bounded selected-material slicing; local answer-shaped field assembly; View projection; text formatting.
- **Partially witnesses:** answer composition pressure, support preservation, authority-boundary preservation, limitation preservation, presentation-relevance pressure through `why_related`, and renderable public View pressure.
- **Bypasses:** frontier-to-Question; preserved note-to-Question; Question-plus-admitted-evidence-to-Answer; Answer-to-presentation-candidate.
- **Compresses:** collected material vs selected material vs local answer-shaped material; local answer vs View; View vs formatted rendering. These are separable in code but not constitutional standing crossings.
- **Does not address:** constitutional Question standing, evidence admission, constitutional Answer standing, presentation admission, encounter sequencing, outward Fidelity, delivery, receipt, uptake, reliance, or responsibility/authority transition.

Central fidelity finding: `_InquiryOrientationAnswer` preserves enough standing to qualify as a bounded implementation-local orientation answer material artifact, but not enough to qualify as a bounded constitutional Answer. `InquiryOrientationView` performs View projection by collapsing local answer material and the preserved note into the prebuilt View shape; it does not independently perform constitutional presentation admission, sequencing, or rendering-as-standing responsibilities. Rendering is performed later by `format_inquiry_orientation` as plain text formatting.

## 9. Strongest Unknowns

1. Whether a future or deleted producer was intended to connect `InquiryNoteRecord` to constitutional Question standing is Unknown from this module and was not surveyed repository-wide.
2. Whether any other answer-shaped surface in the repository preserves full Question/admitted-evidence/Answer standing remains outside this bounded inquiry.
3. Whether the CLI output has an externally compared Fidelity relation to the View is Unknown; no local fidelity-comparison producer exists here.
4. Whether knowledge-reachability's internal use of formatted inquiry orientation should be treated as a constitutional consumer is Unknown; current evidence supports only an internal read-model surface scan.
5. Whether the separate support list dropped between `_InquiryOrientationAnswer` and `InquiryOrientationView` matters constitutionally is Unknown; row-level support survives in `RelatedMaterial`.

## 10. Smallest next honest inquiry

Inspect exactly one active caller outside `seed_runtime/inquiry_orientation.py` and ask whether it consumes `InquiryOrientationView` or formatted inquiry-orientation output as constitutional Answer/presentation standing, or only as operational orientation text. The smallest target is `seed_runtime/knowledge_reachability.py::_inquiry_surfaces`, because it builds and formats inquiry orientation internally but appears to use the result only as a surface-presence signal.

## Checks performed

- `pwd && find .. -name AGENTS.md -print && git status --short --branch`
- `cat AGENTS.md && git branch --show-current && git log --oneline -5`
- `sed -n '1,260p' seed_runtime/inquiry_orientation.py && sed -n '260,620p' seed_runtime/inquiry_orientation.py`
- `rg -n "InquiryOrientation|inquiry_orientation|record-inquiry-note|format_inquiry_orientation|build_inquiry_orientation|diagnostic-inventory|diagnostic-shape-audit" .`
- `rg -n "build_inquiry_orientation|format_inquiry_orientation|record_inquiry_note|select_inquiry_note|--inquiry-orientation|--record-inquiry-note" seed_runtime scripts tests docs/frontier_question_answer_presentation_connection_recovery_001.md -S`
- `sed -n '1600,1680p' scripts/seed_local.py && sed -n '6630,6685p' scripts/seed_local.py && sed -n '880,920p' seed_runtime/knowledge_reachability.py && sed -n '1,640p' tests/test_inquiry_orientation.py`
- `sed -n '1,220p' docs/frontier_question_answer_presentation_connection_recovery_001.md && sed -n '960,1020p' seed_runtime/question_surface_inventory.py`
- `nl -ba seed_runtime/inquiry_orientation.py | sed -n '1,390p'`
- `nl -ba scripts/seed_local.py | sed -n '1630,1680p;6640,6685p'`
- `nl -ba seed_runtime/knowledge_reachability.py | sed -n '895,910p'`
- `nl -ba docs/frontier_question_answer_presentation_connection_recovery_001.md | sed -n '50,130p'`
- `git diff --check`
