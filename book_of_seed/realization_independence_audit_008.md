# Realization-Independence Audit 008

## Repository state examined

- `git rev-parse HEAD`: `850044cf1b1da7976d7960884a1bd0337e9e8f90`.
- `git status --short` before the audit: no output.
- PR 1749 is present in the surveyed checkout as `850044c (HEAD -> work) Add constitutional occurrence evidence survey 007 (#1749)`.
- `book_of_seed/constitutional_occurrence_evidence_survey_007.md` exists.

Repository implementation evidence controls claims about the current Seed realization. It does not, by itself, control claims about every lawful Seed realization.

## Book claims audited

Audited the durable claims in:

- `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `01-grammar-and-standing/constructors-and-production-authority.md`
- `01-grammar-and-standing/lenses-views-and-roads.md`
- `02-acts-and-constraints/acts-and-act-artifacts.md`
- `03-goals-and-advancement/construction-and-establishment.md`
- `04-inquiry-and-examination/inquiry-frontiers.md`
- `05-evidence-and-knowledge/testimony-and-established-fact.md`
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `06-state-and-projection/events-facts-and-state.md`
- `07-operational-realization/execution-and-recording.md`

The audit focused on claims strengthened by occurrence-evidence work: act versus artifact, responsible production versus representation construction, observer-held occurrence evidence versus preserved occurrence evidence, recording occurrence versus truth of recorded assertion, execution result versus execution record, and knowledge extraction versus original execution occurrence.

## Implementation witnesses examined

Representative witnesses examined only as needed:

- `seed_runtime/events.py::EventLedger` and `SQLiteEventLedger`
- `seed_runtime/models.py::Event`
- `seed_runtime/execution.py::ToolExecutor.execute` and related allowed-call recording paths
- `seed_runtime/fact_extraction.py::FactExtractionService.observe_tool_result`
- Book-cited establishment and selection anchors where audited chapters used construction-bypass examples

These witnesses show that the current repository can realize the audited distinctions through Python functions and methods, model construction, exceptions and returns, event payloads, stable identifiers, causation/correlation fields, in-memory records, and SQLite-backed persistence. They do not make those mechanisms constitutional requirements.

## Current-realization versus invariant matrix

| Concept | Constitutional invariant | Current repository witness | Implementation-specific mechanism | Silent dependency risk | Corrected language required? | Non-dependency guardrail |
| --- | --- | --- | --- | --- | --- | --- |
| responsible boundary | A constitutional occurrence requires a responsibility-bearing producer boundary with the relevant warrant, validation, and asserted transition. | Establishment, selection, execution, and extraction routines validate inputs and then assert results. | Python functions or methods. | Equating act occurrence with Python invocation. | Yes. | A lawful realization may use another authorized operation boundary if it preserves validation and assertion responsibility. |
| representation construction | A representation that can exist without responsible production is insufficient by itself to prove that production occurred. | Direct construction of goal-, selection-, event-, or evidence-shaped models can produce fields without the producer boundary. | Dataclass/model/public constructor construction. | Treating direct Python instantiation as the constitutional problem rather than one witness of it. | Yes. | Any representation system with separable construction and responsible production carries the same burden. |
| act artifact | An artifact may report or preserve an act assertion without proving the act occurred. | Execution proposals, act-shaped models, and selection artifacts can exist apart from execution or selection boundaries. | Python objects with act-shaped fields. | Treating artifact class identity as act standing. | Partly. | Standing depends on production or establishment warrant, not artifact shape alone. |
| observer testimony | A witness to a responsible-boundary occurrence may have occurrence evidence not preserved in the artifact. | A caller may observe return or refusal inside an execution context. | Return value, raised exception, same call context. | Making stack presence or object-return history constitutional. | Yes. | The invariant is witnessed occurrence versus preserved evidence; the witness form is realization-specific. |
| recording | Recording proves that a record was made and may preserve an assertion; it does not prove the truth of every recorded assertion. | `EventLedger.append` creates event objects and indexes them by id/workspace. | In-memory append method. | Equating recording with `EventLedger.append(...)`. | Yes. | Recording is any warranted creation of retrievable assertion-bearing material within a declared preservation horizon. |
| persistent recording | Persistence requires preservation beyond the local process horizon claimed by the recorder. | `SQLiteEventLedger` stores events in a SQLite database and can list/get rows later. | SQLite table and relational row storage. | Equating persistence with SQLite or calling in-memory history durable. | Yes. | SQLite is a witness of cross-runtime storage, not the constitutional meaning of persistence. |
| producer attribution | Represented producer lineage is an assertion needing warrant; it is not verified production by itself. | Event payloads and causation/correlation fields carry producer and lineage references. | String ids and event fields. | Treating lineage fields as occurrence seals. | No broad rewrite; existing distinctions mostly hold. | Stable identifiers and references support explanation but do not independently verify causation or production. |
| execution occurrence | Execution requires a warranted performance boundary and result/refusal standing. | `ToolExecutor.execute` validates registration/policy, records started/completed/failed events, validates output, and returns structured results. | Registered Python callables, return values, exceptions. | Equating execution with local callable invocation. | Yes. | Remote, subprocess, message-driven, hardware, or distributed execution can satisfy the grammar only if the warranted boundary and result evidence remain visible. |
| external effect | A provider response or successful local result does not independently verify the external world effect it claims. | Tool output can be recorded and extracted as evidence without automatic fact promotion. | Tool output payloads and `tool.call.completed`. | Treating successful result as established fact or verified external effect. | No broad rewrite. | External-effect standing requires additional evidence or verification appropriate to the claim. |
| knowledge extraction | Extraction admits source material under an extraction warrant and creates a new attributed evidence/knowledge assertion; it is not the original execution. | `FactExtractionService.observe_tool_result` accepts completed-result events and appends `evidence.observed`. | Service class, event kind strings, Evidence model. | Requiring the current service/event names as constitutional extraction. | No broad rewrite; audit notes guardrail. | The durable distinction is source admission + extraction warrant + new attributed assertion, not a mandatory class or event name. |

## Python dependency findings

Some Book language risked promoting the current Python realization into constitutional grammar. The phrase that occurrence must be evidenced by a "responsible validated function" was too narrow. The invariant is a responsible validated production boundary. Python functions and methods remain useful repository witnesses because they show validation, refusal, assertion production, result construction, and side effects in one inspectable place. They are not the definition of constitutional act occurrence.

The constructor chapter also risked making "producer function" the universal subject. It now speaks of the named producer boundary while retaining the current repository's function/method anchors.

## Representation-construction dependency findings

The current repository demonstrates construction bypass through public model construction and pre-built event insertion. The invariant exposed by those paths is not "dataclasses are dangerous" or "Python constructors are constitutionally suspect." The invariant is that representation existence can be achieved without the responsible production occurrence, so later consumers need a warrant if their assertion depends on that occurrence.

The audited chapters mostly preserved this invariant. Existing direct-construction examples remain useful because they are concrete failure modes in this repository.

## Live-call-context findings

Pass 006/007 language around live return was directionally correct but too tied to the local call context. A live return does not have universal constitutional standing as an object-return history. The invariant is witnessed responsible-boundary occurrence: an observer may have immediate-context evidence that the responsible boundary occurred, while the returned artifact may not preserve that evidence for later consumers.

Corrected language now uses witnessed return and observer-held occurrence standing rather than treating Python return semantics as constitutional.

## Recording and persistence findings

`EventLedger` is a process-local append-only ledger. It records events and permits later retrieval while that ledger instance and process-local state remain available. `SQLiteEventLedger` witnesses a stronger preservation horizon by storing events in SQLite. These witnesses support distinctions among record creation, later retrievability, process-lifetime preservation, cross-runtime persistence, attribution, causal reference, and recorded assertion.

The audited Book language contained one overly broad "Recording preserves" claim and one "durable record" phrase that collapsed preservation horizons. Those were corrected to say that recording creates retrievable representations within the recorder's preservation horizon and that a retrievable record is not an established fact. A process-local record is not the same as a cross-restart persistent record.

## Execution realization findings

`ToolExecutor.execute(...)` witnesses the operational execution grammar through registration and policy validation, started/completed/failed events, return values, exception handling, and output-schema validation. The constitutional invariant survives replacement by another execution realization only if the new realization preserves a warranted operation-performance boundary and result/refusal evidence.

The execution chapter now states that local Python call topology is a current witness, not a constitutional requirement. It also preserves the repository-grounded distinction that recording does not retroactively authorize execution, verify external effects, or automatically extract knowledge.

## Knowledge-extraction realization findings

`FactExtractionService.observe_tool_result(...)` supports the distinction between original execution and later extraction. It admits only completed-result event shapes, derives an attributed evidence payload, and appends a new evidence observation caused by the source event. The current class, event kind strings, `Evidence` model, and database representation are implementation witnesses.

The supported invariant is narrower: source material must be admitted for extraction under an extraction warrant, and extraction creates a new attributed knowledge/evidence assertion rather than proving the original execution occurrence. The repository currently supports evidence observation from tool results, not a universal extraction theory for every source.

## Silent dependencies corrected

Corrected silent dependencies in audited Book chapters:

- Python function as constitutional production boundary was replaced with responsible validated production boundary while preserving Python functions/methods as current witnesses.
- Live return as a universal standing category was replaced with witnessed return/observer-held occurrence standing.
- Recording as unqualified preservation was bounded to the preservation horizon supplied by the recorder.
- Durable record terminology was replaced with retrievable record and process-local versus cross-restart distinctions.
- Event language was clarified so events assert occurrences or other claims, rather than making every event an occurrence truth.
- Execution was reframed as operation-performance and result boundary, with `ToolExecutor.execute(...)` retained as current repository witness rather than mandatory topology.

## Implementation details retained as useful evidence

The audit retained repository anchors to Python functions, dataclasses/models, `EventLedger`, `SQLiteEventLedger`, event payloads, stable ids, causation/correlation references, `ToolExecutor.execute(...)`, and `FactExtractionService.observe_tool_result(...)`. These details are valuable representative anchors. Removing them would weaken the evidence burden and drift into implementation-free abstraction.

## Claims demoted to current-realization testimony

- "Responsible function proves occurrence" is demoted to current-realization testimony: current functions may witness a responsible boundary, but the invariant is not function-specific.
- "Live return carries stronger standing" is demoted to current-realization testimony: a caller may witness occurrence, but the universal distinction is observer-held occurrence evidence versus preserved occurrence evidence.
- "Persistent recording equals SQLite" is rejected as constitutional language; SQLite is a current persistence witness.
- "Event proves execution" is demoted: an event proves a recording/assertion occurrence, while execution truth depends on the warrant for the recorded assertion and any surrounding evidence.

## Cross-realization invariants recovered

- Act occurrence requires a responsibility-bearing boundary and cannot be inferred from an act-shaped artifact alone.
- Responsible production and representation construction are distinct.
- Observer-held occurrence evidence and preserved occurrence evidence are distinct.
- Recording occurrence and truth of recorded assertion are distinct.
- Execution result and execution record are distinct.
- Knowledge extraction and original execution occurrence are distinct.
- Represented provenance and verified production are distinct.
- Stable identifiers, causation references, serialization, and database storage can support evidence, but none is an occurrence seal by itself.

## Non-dependency guardrails recovered

- Python is not constitutionally required.
- Dataclasses, Pydantic models, and public constructors are not constitutionally required.
- In-process function calls and Python object identity are not constitutionally required.
- Exceptions and return values are not universal refusal or occurrence representations.
- `EventLedger` is not recording as a constitutional kind.
- SQLite is not persistence as a constitutional kind.
- Current event names are not the constitutional grammar of occurrence, execution, or extraction.
- Implementation replacement does not automatically replace the constitutional grammar, but a replacement must still demonstrate the same evidentiary distinctions.

## Claims contradicted

No audited Book claim was contradicted by implementation evidence in the strong sense of saying the opposite of what the repository does. The main findings were over-narrow phrasings that could accidentally constitutionalize current mechanisms.

## Claims remaining unresolved

- The repository supports process-local and SQLite-backed preservation horizons, but it does not establish a complete constitutional taxonomy for replicated, externally durable, or multi-party preservation.
- The repository supports tool-result evidence observation, but it does not establish a universal extraction process for every possible source material.
- The repository supports causation/correlation references as lineage fields, but not as verified causation seals.

## Book chapters updated

Updated narrowly:

- `01-grammar-and-standing/constructors-and-production-authority.md`
- `02-acts-and-constraints/acts-and-act-artifacts.md`
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `06-state-and-projection/events-facts-and-state.md`
- `07-operational-realization/execution-and-recording.md`

No implementation code was changed. No tests were added because the task was a Book audit and the corrections were documentation wording, not a diagnostic or runtime behavior change.

## Bounded resolution

Book grammar contains correct invariants but several silent implementation dependencies.

Book of Seed realization-independence audit 008 complete.
