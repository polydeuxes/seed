# Inquiry Note Artifact Characterization

## Executive answer

An Inquiry Note is **not an Observation** in the implemented Seed runtime. It is an `InquiryNoteRecord`: an isolated JSONL-preserved copy of operator prose used as input to the bounded `InquiryOrientationView` read-only orientation surface.

Its implementation responsibility is exactly:

> Preserve raw operator prose with minimal provenance outside the event ledger, then allow Inquiry Orientation to use that preserved prose as a non-authoritative lexical query against already projected read models.

It owns **orientation**, not truth. It has no implemented authority to create observations, facts, claims, requirements, goals, recommendations, ownership, current facts, event-ledger entries, replay input, or claim support. The strongest repository evidence is negative: the module docstring, authority boundary, storage path, CLI flow, projector event handling, and tests all keep inquiry notes outside Seed's knowledge mutation path.

## Implementation evidence reviewed

Reviewed implementation surfaces:

- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/observations.py`
- `seed_runtime/facts.py`
- `seed_runtime/events.py`
- `seed_runtime/state.py`
- `scripts/seed_local.py`
- `tests/test_inquiry_orientation.py`
- `tests/test_inquiry_artifacts.py`
- focused repository searches for inquiry notes becoming observations, facts, event-ledger events, claim support, projections, or current facts

The core implementation states that inquiry notes are stored outside the event ledger and that rendering does not mutate projected state, append events, call providers, execute tools, or create facts, goals, tool needs, decisions, proposals, or plans. `AUTHORITY_BOUNDARY` then renders the stronger semantic boundary: an inquiry note is preserved operator prose, not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction; matches are deterministic lexical overlaps and do not assert importance, ownership, intent, concern, recommended action, or next safe move.

## Lifecycle

1. The CLI exposes `--record-inquiry-note TEXT` as a way to append raw operator prose to an isolated inquiry-note probe store.
2. `record_inquiry_note(...)` validates that the note is non-empty, constructs an `InquiryNoteRecord` with `inq_` id, raw note, timestamp, optional workspace/session ids, and fixed source string.
3. The note is serialized as one JSON object per line into the selected note store.
4. `load_inquiry_notes(...)` reads JSONL records back into `InquiryNoteRecord` values.
5. `select_inquiry_note(...)` selects either the latest note or an explicit id.
6. `build_inquiry_orientation(state, note)` consumes an existing projected `State` and a selected `InquiryNoteRecord`, composes related material, and returns an `InquiryOrientationView`.
7. `format_inquiry_orientation(...)` renders the preserved note, potentially related material, support/why-related text, uncertainty, and authority boundary.

There is no implemented lifecycle step that converts the note into an `Observation`, `Evidence`, `Fact`, `FactSupport`, claim, event, current fact, goal, recommendation, or replay unit.

## Storage

### Where is an Inquiry Note stored?

An Inquiry Note is stored in an isolated JSONL file, not the event ledger. `record_inquiry_note(...)` opens `store_path` in append mode and writes `_record_to_json(record)` as one JSON line. The CLI chooses that store as `<db>.inquiry_notes.jsonl` when `--db` is used, otherwise `.seed/inquiry_notes.jsonl` under the repository root.

### Does it survive replay?

Not as event-ledger replay. `StateProjector.project(...)` replays `ledger.list_events(workspace_id)` and applies known event kinds. Since inquiry notes are stored in a separate JSONL file and `record_inquiry_note(...)` does not append a ledger event, event replay cannot reconstruct inquiry notes. They survive only as long as the isolated JSONL store survives.

## Authority boundaries

### What authority does it possess?

An Inquiry Note has only input/orientation authority:

- preserve raw operator prose with minimal provenance;
- identify the note by id and timestamp;
- carry optional workspace/session labels;
- act as input to deterministic lexical matching over already projected fact supports and source-navigation matches;
- be rendered back to the operator in an Inquiry Orientation report.

### What authority does it explicitly not possess?

It explicitly lacks authority to be a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, importance assertion, ownership assertion, intent assertion, concern assertion, recommended action, or next safe move.

It also lacks implementation authority to mutate projected state, append events, call providers, execute tools, create facts, create goals, create tool needs, create decisions, create proposals, create plans, create observations, create evidence, create claim support, or affect replay.

## Comparison against Observation

An `Observation` is a canonical external observation with structured fields: `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, confidence, metadata, dimensions, and optional expiry. `ObservationIngestor.ingest_many(...)` turns observations into event-ledger entries: `observation.observed`, `evidence.observed`, and, unless promotion is suppressed, `fact.observed` or `fact.inferred`.

An Inquiry Note is different:

| Dimension | Observation | Inquiry Note |
| --- | --- | --- |
| Model | `Observation` | `InquiryNoteRecord` |
| Shape | subject/predicate/value observation | raw prose plus minimal provenance |
| Ingestion | `ObservationIngestor` | direct JSONL append |
| Ledger event | `observation.observed`, `evidence.observed`, optional fact event | none |
| Projection | projector stores observations from `observation.observed` events | not a `State` field and not replayed from events |
| Fact promotion | can become a `Fact` through observation-to-fact conversion | explicitly not a fact and no conversion path exists |
| Authority | external observation that may support facts | operator orientation prose only |

## Comparison against Event Ledger

The event ledger is append-only runtime history. `EventLedger.append(...)` constructs and stores `Event` records; `StateProjector` projects state by consuming ledger events. Observation ingestion uses ledger events to preserve observations, evidence, and facts.

Inquiry Note recording bypasses that path. It writes JSONL directly. The CLI branch for `--record-inquiry-note` calls `record_inquiry_note(...)`, prints the note id, and returns unless orientation was also requested. It does not call `EventLedger.append(...)` or `ObservationIngestor`.

Therefore an Inquiry Note does **not** create an Event and does **not** participate in event-ledger replay.

## Comparison against Claim Support

Fact support in Seed is projected from `Fact` records. `_project_fact_supports(...)` groups facts by subject, predicate, dimensions, and value, then emits `FactSupport` records whose `supporting_fact_ids`, source types, confidence, and observed times are derived from supporting facts.

Inquiry Orientation can display a string named `support`, but that is local answer support explaining why a piece of already projected material was lexically related. It is not `FactSupport`, not claim support, not evidence, and not a supporting fact id. The note is used to find overlaps against existing fact supports and source navigation; it does not become part of those supports.

## Comparison against Repository Observation

Repository observations in this codebase are implementation evidence or facts about repository artifacts that can be represented as observations/facts through existing observation/fact machinery. Inquiry Notes are not repository observations because they do not assert that any repository artifact has a subject/predicate/value state. They preserve what an operator wrote, and the implementation explicitly prevents that prose from becoming repository truth.

The nearest repository-visible inquiry artifact implementation, `seed_runtime/inquiry_artifacts.py`, is itself read-only and says its boundary has no recording, no event-ledger writes, no cluster mutation, no inquiry graph creation, no pressure transformation inference, and no workflow/planning behavior. That supports treating inquiry-note-related outputs as visibility/orientation rather than repository observations.

## Comparison against Answer Composition

Inquiry Orientation includes implementation-local `_ArchitecturalOrientationEvidence` and `_ArchitecturalOrientationAnswer` records before rendering. This means answer composition exists, but it is downstream of note preservation. The answer object carries related material, reason, support strings, boundary, and limitations; `InquiryOrientationView` then exposes the note, related material, uncertainty, and authority boundary.

Answer Composition may cite an Inquiry Note only in the narrow sense that `format_inquiry_orientation(...)` renders the preserved note and related material inside the Inquiry Orientation answer. There is no general implementation evidence that answer composition may cite Inquiry Notes as truth, facts, observations, claim support, or repository evidence outside this orientation surface.

## Who is permitted to read it?

Implemented readers are:

- `load_inquiry_notes(...)`, which reads the isolated JSONL store;
- `select_inquiry_note(...)`, which selects latest or explicit note id;
- the CLI `--inquiry-orientation` flow, which uses selected notes to render orientation;
- tests that load and select records.

There is no permission model beyond filesystem access and CLI invocation in the reviewed implementation.

## Who is permitted to mutate it?

The implemented mutator is `record_inquiry_note(...)`, exposed by CLI `--record-inquiry-note`, and its mutation is append-only at the JSONL file level. There is no update/delete/edit API for individual inquiry notes in the reviewed implementation. It is not mutated through the event ledger, the projector, observation ingestion, fact projection, or claim reconciliation.

## Counterexamples searched

### Inquiry Notes becoming observations

No implementation path was found. Counterevidence: `ObservationIngestor` requires an `Observation` and emits observation/evidence/fact events, while inquiry-note recording constructs `InquiryNoteRecord` and writes JSONL directly.

### Inquiry Notes creating event-ledger entries

No implementation path was found. Counterevidence: the inquiry orientation module says notes are stored outside the event ledger, and the CLI `--record-inquiry-note` path calls `record_inquiry_note(...)` rather than ledger append.

### Inquiry Notes participating in projection

No implementation path was found. Counterevidence: `State` has observations, evidence, facts, fact supports, goals, tools, and related projected collections, but no `inquiry_notes` field in the core dataclass; `StateProjector.project(...)` replays ledger events, not JSONL inquiry notes.

One knowledge-reachability helper uses a synthetic `InquiryNoteRecord` named `audit` to build an inquiry orientation string from default seeds, but that is a read-model audit query over existing state, not projection of recorded notes.

### Inquiry Notes becoming current facts

No implementation path was found. Current facts are projected from `Fact` records and `FactSupport`; inquiry notes do not produce facts or supporting fact ids.

### Inquiry Notes contributing claim support

No implementation path was found. The only inquiry-orientation support strings are explanatory strings for lexical relatedness in an answer view, not claim-support records or supporting evidence ids.

### Inquiry Notes being treated as repository truth

No implementation path was found. Counterevidence is the rendered authority boundary and tests checking that ownership/importance/next-safe-move language appears only as negated boundary language.

## Supported conclusions

1. **What implementation artifact is an Inquiry Note?**
   It is an `InquiryNoteRecord`: a frozen dataclass with `note_id`, `raw_note`, `recorded_at`, fixed `source`, and optional `workspace_id`/`session_id`, persisted as JSONL by `record_inquiry_note(...)`.

2. **What authority does it possess?**
   It can preserve operator prose and act as input to a read-only lexical orientation view over existing projected material.

3. **What authority does it explicitly not possess?**
   It cannot assert truth, mutate knowledge, become a fact/claim/observation/event, support a claim, establish intent/ownership/importance/concern, recommend action, or authorize next moves.

4. **How does it differ from an Observation?**
   An Observation is structured external subject/predicate/value input to the observation ingestion and event projection pipeline. An Inquiry Note is unstructured operator prose stored outside that pipeline.

5. **How does it differ from Claim Support?**
   Claim/fact support is derived from facts and supporting fact ids. Inquiry-note support strings only explain lexical relatedness inside one orientation answer.

6. **How does it differ from a repository Observation?**
   It does not observe a repository artifact or assert repository truth. It preserves operator context for orientation against existing repository/projected material.

7. **Is it implementation-visible as a distinct artifact family?**
   Yes, but boundedly: `InquiryNoteRecord`, isolated inquiry-note JSONL storage, `--record-inquiry-note`, `--inquiry-orientation`, and Inquiry Orientation tests make it distinct from observations/events/facts. The distinct family is not a generalized inquiry artifact or knowledge artifact; it is an inquiry-orientation input artifact.

8. **Is there sufficient implementation evidence to justify recovering exactly one bounded responsibility?**
   Yes. The recoverable responsibility is: **preserved operator-prose orientation input**. There is insufficient implementation evidence to recover broader ownership such as inquiry state, inquiry graph, planner state, claim evidence, or knowledge mutation.

## Unsupported conclusions

The reviewed implementation does not support concluding that an Inquiry Note is:

- an Observation;
- an Event;
- Evidence;
- a Fact;
- a current fact;
- Claim Support;
- a repository Observation;
- a requirement;
- a goal;
- ownership evidence;
- operator intent;
- a recommendation;
- a next safe move;
- durable replay input;
- a general inquiry graph node;
- a planner or workflow object.

## Confidence

High confidence for the negative boundary: the implementation directly stores notes outside the event ledger, renders explicit non-authority language, and tests that recording notes does not change projected runtime state.

Medium-high confidence for the positive characterization: the implementation clearly supports a distinct `InquiryNoteRecord`/JSONL/orientation-input path. The only reason this is not stated as broader architectural ownership is that repository evidence supports only the bounded Inquiry Orientation input role, not a generalized inquiry artifact architecture.
