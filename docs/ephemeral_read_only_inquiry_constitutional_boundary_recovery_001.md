# Ephemeral Read-Only Inquiry Constitutional Boundary Recovery 001

This is one bounded, report-only constitutional boundary recovery of the inquiry-note side channel on current merged `main` after PR 1943. It changes no production code, tests, fixtures, CLI behavior, persistence, events, exports, canonical Book chapters, or existing reports.

## Governing question

Is the inquiry-note road a lawful read-only client inquiry against Seed's current projected standing, distinct from durable constitutional inquiry and ingress -- and if so, which responsibilities belong to the client, query boundary, Seed answering road, presentation, rendering, and any optional later crossing into the constitutional chain?

## Classification vocabulary

Findings use these labels: `faithful within scope`, `mixed standing`, `compatibility-only`, `foreign crossing`, `absent`, and `Unknown`.

## Scope and current witnesses inspected

Minimum implementation witnesses inspected:

- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/knowledge_reachability.py::_inquiry_surfaces`
- `scripts/seed_local.py`
- `tests/test_inquiry_orientation.py`

Current Book clauses inspected for operator ingress, questions and inquiry, State and projection, views, evidence and admission, representation and emission, consumer boundaries, recording and preservation, Unknown/refusal/stopping:

- `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`
- `book_of_seed/06-state-and-projection/projection-and-current-state.md`
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
- `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
- `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md`
- `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md`
- `book_of_seed/attributed_operator_expression_active_road_fidelity_recovery_001.md`

PR 1942's `docs/frontier_question_answer_presentation_connection_recovery_001.md` and PR 1943's `docs/inquiry_orientation_answer_presentation_current_road_recovery_001.md` were used as testimony only, not canonical authority.

## 1. Exact current side-channel road

The current side-channel road is:

```text
client/operator text supplied to scripts.seed_local
-> --record-inquiry-note TEXT
-> record_inquiry_note(store_path, raw_note, workspace_id, session_id)
-> isolated JSONL append of InquiryNoteRecord
-> --inquiry-orientation [NOTE_ID]
-> select_inquiry_note(store_path, note_id/latest)
-> projected_state_from_args(args)
-> build_inquiry_orientation(projected_state, note)
-> _prepare_inquiry_orientation_composition(note)
-> lexical note tokens
-> _collect_inquiry_orientation_evidence(projected_state, request)
-> _fact_matches(state.fact_supports, tokens)
-> _source_navigation_matches(build_source_navigation(state, token))
-> _prepare_inquiry_orientation_selected_material(evidence)
-> sort/dedupe/cap selected related material
-> _prepare_inquiry_orientation_answer_payload(selected_material)
-> _InquiryOrientationAnswer
-> InquiryOrientationView(note, related_material, uncertainty, authority_boundary)
-> format_inquiry_orientation(view)
-> CLI print formatted response
```

The implementation's module docstring states that inquiry notes are stored outside the event ledger and that rendering reads projected state without mutating it, appending events, calling providers, executing tools, or creating facts, goals, tool needs, decisions, proposals, or plans. That is evidence of intentional non-ledger, read-only posture, not evidence of absence of constitutional discipline.

Classification: `faithful within scope` as a bounded read-only inquiry road; `mixed standing` because the record function still says "operator prose remains preserved evidence for this probe only," while the recovered side-channel orientation is better read as client/session request material until a separate durable crossing occurs.

## 2. Durable-ingress versus ephemeral-inquiry topology

### Durable constitutional ingress or inquiry

```text
external material
-> admitted crossing
-> preserved occurrence or testimony
-> Observation / Evidence / standing
-> possible constitutional Question
-> examination
-> revised durable standing
```

Current Book question grammar says question-shaped external material is testimony, not an internal constitutional question; Seed may consume external/operator material when forming a bounded question, but the internal question-forming act is Seed-owned and must preserve identity, provenance, scope, evidence demand, authority limits, uncertainty, and lawful stop conditions. Current Book projection grammar also says diagnostic or projection output may be evidence that a bounded surface exists, but diagnostic findings remain diagnostic-scope unless a separate warranted act promotes a claim through applicable evidence, authority, and standing boundaries.

Durable ingress therefore requires an admitted crossing and a Seed-owned constitutional act. It may preserve testimony, form a bounded Question, conduct examination, and update durable standing only through explicit identity, provenance, scope, authority, evidence, Unknown, and stop boundaries.

### Ephemeral read-only inquiry

```text
client query
-> bounded interpretation or query preparation
-> read of existing projected State
-> bounded answer material
-> presentation
-> rendering
-> client response
```

This second topology can remain outside the event ledger and durable Seed history while lawfully constrained. The lawful constraint is not event preservation; it is boundary preservation: the query must not become Observation, testimony about reality, Fact, internal Question, admission, learning, authorization, or mutation by being asked; the answer must be limited to current projected standing and Unknowns; presentation/rendering/emission must not claim receipt, uptake, reliance, or durable transition.

Classification: ephemeral inquiry is `faithful within scope` when treated as a read-only client request to inspect current projected standing. Treating it as durable constitutional ingress without a crossing is a `foreign crossing`. Treating it as unconstrained because it is non-ledger is also a `foreign crossing`.

## 3. Responsibility and ownership matrix

| Responsibility | Recovered owner | Current evidence | Classification | Boundary protected |
|---|---|---|---|---|
| Raw query/session retention | client plus shell/communication adapter for session history; inquiry-note JSONL store only when `--record-inquiry-note` is explicitly used | CLI flag appends text to `.inquiry_notes.jsonl` or `--db`-derived store; record carries `workspace_id` and `session_id` | `mixed standing` | client session history != Seed memory; query persistence != event preservation |
| Query identity and correlation | ephemeral query boundary for `note_id`; shell/adapter for any broader client correlation | `InquiryNoteRecord` has `note_id`, timestamp, optional workspace/session | `faithful within scope` | correlation id != constitutional provenance by itself |
| Query interpretation | ephemeral query boundary | `_prepare_inquiry_orientation_composition` tokenizes raw note; overlap is deterministic lexical only | `faithful within scope` | query interpretation != admission; query subject != asserted fact |
| Scope and visibility authorization | shell/communication adapter plus ephemeral query boundary; Seed answering road must honor projected-State/workspace scope | CLI passes workspace/session; answer reads `projected_state_from_args(args)` | `compatibility-only` | request to inspect != authority to observe or learn |
| Current-State snapshot selection | Seed constitutional answering road, constrained by projection rules | `build_inquiry_orientation(projected_state_from_args(args), note)` consumes already projected State | `faithful within scope` | read-only answer computation != durable learning |
| Evidence or standing selection | Seed answering road for read-model selection only; constitutional ingress boundary for durable admission | `_fact_matches`, `_source_navigation_matches`, sort/dedupe/cap | `faithful within scope` for read-only selection; `absent` for admission | selected material != admitted evidence |
| Answer sufficiency and Unknowns | Seed answering road | Limitations distinguish lexical matches from no deterministic related material, but Unknowns are string limitations rather than structured constitutional Unknowns | `compatibility-only` | unanswerable query != authority to observe or learn |
| Presentation membership/admission | presentation boundary if durable presentation standing is required; current road only includes view field membership | `InquiryOrientationView` carries related material; no separate presentation admission artifact | `compatibility-only` / `absent` | material in view != admitted to constitutional presentation |
| Presentation sequencing/composition | current formatter and view assembly for display order; presentation boundary for constitutional sequencing | deterministic sorted/deduped/capped rows and section formatting | `compatibility-only` | display order != constitutional encounter sequencing |
| Rendering | renderer (`format_inquiry_orientation`) | formats plain text sections from the View | `faithful within scope` | rendering != emission |
| Response emission | shell/CLI communication adapter | `print(format_inquiry_orientation(...))` | `faithful within scope` operationally; `compatibility-only` constitutionally | emission != receipt, interpretation, uptake, or reliance |
| Optional conversion into testimony, Observation, or durable inquiry | constitutional ingress boundary only | no current conversion producer in this road | `absent` | query asked != transition authorized |

## 4. Standing of `InquiryNoteRecord`

`InquiryNoteRecord` currently carries:

```text
note_id
raw_note
recorded_at
source
workspace_id
session_id
```

Its fixed authority boundary text says the inquiry note is read-only and is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction. It also refuses importance, ownership, intent, concern, recommended action, and next-safe-move assertions.

Recovered standing: `mixed standing`.

- As PR 1943 implementation testimony, it carries preserved operator prose in an isolated probe store.
- Under the side-channel recovery, it more lawfully carries ephemeral request/client-session standing for a read-only current-State inquiry.
- It does not carry constitutional ingress standing, Observation standing, durable evidence standing, or constitutional Question standing automatically.
- It is not merely an implementation workaround because it preserves identity, timestamp, source, workspace/session references, and negative authority boundaries.
- It is not enough isolation to prove client session history is never Seed memory in all adapters, because this report inspected the local CLI side channel, not every external client transport.

`InquiryNoteRecord` therefore has `compatibility-only mixed standing`: a durable-ish local JSONL request record for a road whose lawful constitutional role is ephemeral read-only inquiry unless and until a separate ingress crossing is performed.

## 5. Event-ledger and persistence boundary

Storing inquiry notes outside the event ledger is mostly `faithful separation`, with an `incomplete isolation` Unknown.

Faithful separation:

- It prevents client query material from silently becoming event-ledger truth, Observation, Evidence, Fact, goal, plan, proposal, command, authorization, or durable constitutional Question.
- It preserves the distinction `query persistence != event preservation`.
- It lets a read-only answer be recomputed from current projected standing without asserting durable learning.

Incomplete isolation / Unknown:

- The JSONL store is still persistence. It may retain raw client/operator query material, note ids, timestamps, workspace ids, and session ids.
- That persistence belongs to the shell/ephemeral query boundary, not to the event ledger, but the current artifact name and docstring still use "preserved" and "operator prose" language.
- The report did not inspect every external transport or session-retention layer, so raw query/session retention outside this CLI store is `Unknown`.

Classification: `faithful within scope` for event-ledger separation; `mixed standing` for local persistence; `Unknown` for full client/session retention ecosystem.

## 6. Read-only Answer/presentation implications

Both durable Seed inquiry and ephemeral client requests may use similar Question, Answer, presentation, or rendering responsibilities without sharing occurrence and durability standing.

The shared responsibilities are shape responsibilities:

```text
identify the request
prepare bounded interpretation
select relevant current material
preserve support and limitations
answer Unknown rather than fabricate
present bounded material
render without strengthening standing
emit without claiming receipt/uptake/reliance
```

The durable road additionally requires constitutional occurrence responsibilities:

```text
admitted source crossing
Seed-owned internal Question formation
admitted evidence
examination standing
structured Unknown/conflict/sufficiency
lawful stop or movement standing
event/preservation boundary if durable change occurs
```

The inquiry-note road currently supplies answer-shaped material but not constitutional Answer standing. Its `_InquiryOrientationAnswer` is local answer material for a read-only side channel. Its `InquiryOrientationView` is a bounded view, and `format_inquiry_orientation` is rendering. None of these establishes receipt, interpretation, uptake, reliance, correction, or durable revision.

Classification: `faithful within scope` for read-only answer computation and rendering; `compatibility-only` for constitutional Answer/presentation standing.

## 7. Exact optional crossing into durable constitutional ingress

Before an ephemeral query can cause durable movement, there must be a distinct, explicit constitutional crossing. The crossing must preserve at least:

```text
identity: the query material or selected subset being offered, plus a new durable ingress/testimony/question id
scope: workspace, subject, temporal/as-of, permitted inquiry/examination bounds
provenance: client/operator/source/channel/session references and how they were established
authority: who/what is permitted to submit, observe, correct, authorize, or open inquiry
evidence demand: what existing or new evidence is being requested/admitted
standing target: testimony, Observation, Evidence, correction, bounded Question, request for authority, or stop
Unknowns/conflicts: what is not known, unsupported, contradicted, or refused
explicit act: submit, authorize observation, open durable inquiry, record correction, admit evidence, request authority, or stop
negative authority: what the act does not authorize
```

Protected distinctions:

- `query asked != transition authorized`
- `answer unavailable != observation authorized`
- `client selects offered movement != movement occurred`
- `query material reused != query material admitted`
- `suggested ingress != ingress occurred`
- `submit query material as testimony != establish testified content as fact`
- `open durable constitutional inquiry != answer it`
- `request authority != receive authority`
- `stop != erase neighboring Unknowns`

Current side-channel evidence contains no such crossing. Therefore optional durable transition is `absent` in this road, and any durable movement would require the constitutional ingress boundary to act separately.

## 8. Reassessment of `_inquiry_surfaces`

Current `_inquiry_surfaces(state)` builds one synthetic `InquiryNoteRecord` with `note_id="audit"`, `raw_note=" ".join(DEFAULT_SEEDS)`, and `recorded_at="1970-01-01T00:00:00Z"`. It formats `build_inquiry_orientation(state, note)`, then returns an empty list if the literal string `No deterministic related material` appears; otherwise it returns the entire formatted orientation string as an inquiry surface.

### Synthetic read-only diagnostic query

The synthetic record is a `synthetic read-only diagnostic query`, not fabricated constitutional testimony. It is not external material, not an operator statement about reality, not an Observation, not admitted Evidence, and not a constitutional Question. It is a diagnostic probe asking whether the inquiry-orientation read model can surface current projected material for default terms.

Classification: `faithful within scope` if documented as synthetic read-only diagnostic query; `foreign crossing` if treated as testimony or internal Question.

### Formatted presentation text reparsed as internal diagnostic signal

The function uses the formatted prose as an internal signal: if the rendered text lacks the no-match phrase, the whole formatted text is fed into the knowledge-reachability surface terms. That creates an inverted dependency risk:

```text
structured query result
-> formatting
-> literal prose search
-> internal reachability inference
```

This does not mutate cluster standing, but it makes an internal diagnostic inference depend on presentation wording rather than a structured result field. Under the recovered side-channel orientation, this is `compatibility-only`: acceptable as a bounded diagnostic witness to rendered surface reachability, but not faithful as proof that presentation prose is internal knowledge standing. If the wording changes, reachability classification can change without the structured orientation result changing.

Classification: synthetic query `faithful within scope`; formatted-text reparse `compatibility-only`; any inference that presentation text establishes internal standing is a `foreign crossing`.

## 9. Producer -> artifact/relation -> consumer evidence

| Producer | Artifact/relation | Consumer | Evidence | Classification |
|---|---|---|---|---|
| `scripts.seed_local` CLI parser | `--record-inquiry-note TEXT` option | CLI dispatch | Argument help says it appends raw operator prose to isolated inquiry-note probe store | `mixed standing` |
| `record_inquiry_note` | `InquiryNoteRecord` plus JSONL line | `load_inquiry_notes`, `select_inquiry_note`, tests | non-empty validation, note id, timestamp, workspace/session, source, JSONL append | `faithful within scope` for local retention |
| `select_inquiry_note` | latest or requested note | CLI orientation dispatch | loads JSONL and selects by id/latest | `faithful within scope` |
| `_prepare_inquiry_orientation_composition` | note plus lexical tokens | `_compose_inquiry_orientation_answer` | `_note_tokens(note.raw_note)` | `faithful within scope` |
| `_collect_inquiry_orientation_evidence` | related material from fact supports and source navigation | selected-material preparation | `_fact_matches` and `_source_navigation_matches` | `faithful within scope` for read-only selection; `absent` for admission |
| `_prepare_inquiry_orientation_selected_material` | bounded selected material and support strings | answer preparation | sort/dedupe/cap and support list | `faithful within scope` |
| `_prepare_inquiry_orientation_answer_payload` / `_assemble_inquiry_orientation_answer_artifact` | local answer-shaped material | `build_inquiry_orientation` | answer, reason, support, boundary, limitations | `compatibility-only` |
| `build_inquiry_orientation` | `InquiryOrientationView` | `format_inquiry_orientation`, tests, `_inquiry_surfaces` | view carries note, related material, uncertainty, authority boundary | `faithful within scope` as View |
| `format_inquiry_orientation` | formatted response text | CLI print, `_inquiry_surfaces`, tests | sections: inquiry note, related material, support/why related, uncertainty, authority boundary | `faithful within scope` for rendering; `compatibility-only` as internal diagnostic input |
| CLI `print` | terminal emission | client/operator | print call after build/format | `faithful within scope` operationally; no receipt/uptake/reliance standing |
| `_inquiry_surfaces` | rendered orientation string or empty list | knowledge-reachability term indexing | literal no-match phrase controls inclusion | `compatibility-only` |

## 10. Explicit Unknowns

1. Whether any non-CLI client adapter retains raw query/session material outside `.seed/inquiry_notes.jsonl` is `Unknown` from this bounded inspection.
2. Whether future or deleted code intended `InquiryNoteRecord` to become durable constitutional ingress is `Unknown`; current code does not perform that crossing.
3. Whether `workspace_id`/`session_id` values are verified identities, mere caller-supplied correlation labels, or adapter-derived references is `Unknown`; current inquiry-note code stores them without authority validation.
4. Whether every current consumer understands inquiry notes as ephemeral read-only requests rather than preserved operator testimony is `Unknown`; PR 1943 testimony still uses preserved-operator-prose vocabulary.
5. Whether structured Unknown/conflict/sufficiency standing should exist for read-only answers is `Unknown`; current road uses limitation strings only.
6. Whether knowledge-reachability intentionally tests rendered presentation reachability, structured inquiry-orientation result reachability, or both is `Unknown`; current implementation reparses formatted prose.
7. Whether a lawful future crossing should reuse raw query text, selected answer material, or a newly attributed operator expression is `Unknown`; this report does not recommend an architecture.

## 11. Smallest next honest inquiry

The smallest next honest inquiry is to inspect one actual boundary where a client/operator response after a read-only answer is received by Seed, and recover whether the response is retained as client session material, attributed testimony, an authorized observation request, a durable constitutional Question-opening act, a correction, a request for authority, or a lawful stop. That inquiry should preserve the same distinctions and should not recommend implementation, renaming, deletion, migration, or replacement architecture.

## Central finding

The inquiry-note side channel is lawfully recoverable as an ephemeral read-only client inquiry against current projected standing, distinct from durable constitutional ingress and durable Seed inquiry. Its constraints come from boundary preservation and negative authority, not from event-ledger writes. `InquiryNoteRecord` is currently mixed: it is a local persisted request/probe record carrying client-session-like material and preserved-prose vocabulary, but it does not by itself have constitutional ingress, Observation, Evidence, Fact, or Question standing. Durable movement requires a separate explicit constitutional crossing with identity, scope, provenance, authority, evidence demand, Unknown/refusal/stop treatment, and an explicit act.

## Checks performed

- `pwd && find .. -name AGENTS.md -print && git status --short --branch`
- `cat AGENTS.md && rg -n "inquiry|InquiryNote|operator ingress|questions|Question|State|projection|views|evidence|admission|representation|emission|consumer|Unknown|refusal|stopping|recording|preservation" seed_runtime/inquiry_orientation.py seed_runtime/knowledge_reachability.py scripts/seed_local.py tests/test_inquiry_orientation.py docs Book* . -g '!*.pyc' -g '!/.git/*'`
- `find . -maxdepth 3 -type f \( -name '*1942*' -o -name '*1943*' -o -iname '*book*' -o -path './docs/*' \) | sed 's#^./##' | head -200`
- `find docs -type f | rg '1942|1943|inquiry.*note|constitutional.*boundary'`
- `sed -n '1,260p' seed_runtime/inquiry_orientation.py; sed -n '880,920p' seed_runtime/knowledge_reachability.py; rg -n "record-inquiry|inquiry-note|inquiry" scripts/seed_local.py tests/test_inquiry_orientation.py`
- `sed -n '260,460p' seed_runtime/inquiry_orientation.py; sed -n '1630,1678p' scripts/seed_local.py; sed -n '6644,6680p' scripts/seed_local.py; find . -maxdepth 2 -type f | rg 'constitution|book|law|chapter|canonical'`
- `git log --oneline --decorate -20 && rg -n "PR 1942|PR 1943|1942|1943" docs . --glob '*.md'`
- `sed -n '1,220p' docs/inquiry_orientation_answer_presentation_current_road_recovery_001.md; sed -n '1,190p' docs/frontier_question_answer_presentation_connection_recovery_001.md`
- `find book_of_seed -maxdepth 2 -type f | sort | sed -n '1,120p'`
- `for f in book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md book_of_seed/06-state-and-projection/projection-and-current-state.md book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md book_of_seed/attributed_operator_expression_active_road_fidelity_recovery_001.md; do echo ===$f===; sed -n '1,180p' $f | head -160; done`
- `git diff --check`
