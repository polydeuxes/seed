# Constitutional-Pipeline Entrance and Bounded-Examination Fidelity Recovery 001

## Recovery boundary and verdict

This is one report-only recovery from merged `main` after PR 2134 (`7c72e31`). It changes no runtime, test, Book, Event, projection, schema, CLI, API, name, or persisted representation.

**Mixed verdict (Outcomes B, C, D, and F):** the implemented constitutional pipeline accepts a constructible, already-shaped `BoundedConstitutionalQuestion`, deterministically projects explicit caller coordinates and registered generic-view availability, selects by exact key equality, and composes the selected generic read models into a bounded explanation. It does **not** establish inquiry admission, examination eligibility, examination output, comparison/finding standing, or bounded-result standing. `produce_bounded_constitutional_question(...)` remains production code but has no recovered non-test caller. The admitted-inquiry-to-bounded-result movement is supported as constitutional grammar and described by corpus passes 051--056, but no exact runtime realization or explicit crossing into this pipeline was recovered. The relation between those movements is therefore **Unknown beyond broad, non-collapsing constitutional grammar**.

The pipeline does not recognize a claim's constitutional shape. It composes only registered views whose implementation keys exactly equal explicit caller-supplied keys. Availability is not applicability; exact-key compatibility is not semantic recognition; selection for composition is not constitutional focus; composition is not cross-examination.

## Evidence and method

### Current implementation and tests inspected

- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_view_composition.py`
- `seed_runtime/read_model_ownership.py`
- `seed_runtime/constitutional_process_view.py`
- `seed_runtime/constitutional_governance_view.py`
- `seed_runtime/constitutional_fidelity_view.py`
- `scripts/seed_local.py`
- `tests/test_bounded_constitutional_question.py`
- `tests/test_constitutional_question_projection.py`
- `tests/test_constitutional_capability_projection.py`
- `tests/test_constitutional_view_selection.py`
- `tests/test_constitutional_view_composition.py`
- `tests/test_constitutional_pipeline.py`
- `tests/test_constitutional_pipeline_provenance_explanation.py`

Searches separated production code from `tests/**`. They found zero non-test calls to `produce_bounded_constitutional_question(...)`. They found one non-test call to `invoke_constitutional_pipeline(...)`, inside `build_constitutional_pipeline_diagnostic(request)`, whose request must already contain the artifact. Direct pipeline calls otherwise occur in tests. `scripts/seed_local.py` still parses the historical flags but both constitutional-pipeline CLI branches now refuse raw fields and direct callers to the API.

### Active Book authority inspected

- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`
- `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`
- `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md`
- `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `book_of_seed/06-state-and-projection/projection-and-current-state.md`
- `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`
- `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md`
- `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md`

The requested historical `08.Handoff.A` is now active as `08.Communication.A`; the active Book explicitly says “handoff” is not a Seed-native primitive. The requested historical `07.Realization.B` was renamed and retained as `07.CapabilityMechanism.C`, as recorded by the active correction `book_of_seed/operational_realization_compression_constitutional_correction_001.md`. Neither old locator was silently treated as current authority.

### Corpus and history testimony inspected

- `constitutional_corpus_recovery_014/inquiry_frontier_pass_051_conjunctive_frontier_identity.md`
- `constitutional_corpus_recovery_014/inquiry_frontier_pass_052_possible_not_admitted_inquiry.md`
- `constitutional_corpus_recovery_014/inquiry_frontier_pass_053_lawful_stop_preserves_neighboring_inquiry.md`
- `constitutional_corpus_recovery_014/inquiry_pipeline_pass_054_admitted_inquiry_to_bounded_examination.md`
- `constitutional_corpus_recovery_014/inquiry_pipeline_pass_055_examination_to_comparison_finding.md`
- `constitutional_corpus_recovery_014/inquiry_pipeline_pass_056_scoped_finding_to_bounded_result.md`
- their stated Book-projection decisions
- `constitutional_pipeline_invocation_implementation_001.md` and `constitutional_pipeline_public_surface_implementation_001.md` as superseded historical implementation testimony
- `constitutional_pipeline_question_origination_deletion_slice_001.md` and current tests/code as the current ownership witness

PR 1607's original invocation account is superseded where PR 1734 (`7bd2325`, recovered by repository history testimony) removed raw question origination. Passes 051--056 are navigation and corpus testimony, not runtime evidence and not Book authority.

## Recovery A — `BoundedConstitutionalQuestion` standing

The frozen artifact fields are `bounded_question_id`, `operator_inquiry`, `inquiry_provenance`, `bounded_question`, `constitutional_intent`, `scope_status`, `uncertainty`, `unknowns`, sorted stringified `caller_supplied_fields`, `testimony_status`, `read_only_boundaries`, `read_only`, `writes_event_ledger`, and `mutates_cluster`.

`produce_bounded_constitutional_question(...)` converts iterable uncertainty/Unknown values to tuples, sorts and stringifies caller fields, and either preserves a caller-provided id or hashes all explicit identity-payload fields. It performs no non-emptiness, provenance, admission, applicability, authority, purpose, scope, or key validation. Its docstring calls its output a deterministic question produced from explicit caller inputs, but constructor/producer naming and return type do not themselves supply constitutional establishment authority.

1. **Direct construction and occurrence:** no. The dataclass accepts arbitrary shape-compatible values; active constructor grammar says construction does not prove a responsible production occurrence.
2. **Producer present:** yes, `produce_bounded_constitutional_question(...)` remains in production.
3. **Current non-test producer calls:** zero recovered.
4. **Evidence consumed:** caller-authored strings/iterables/dictionary only. They are preserved representations, not validated evidence packets.
5. **Admitted-inquiry artifact consumed:** no.
6. **Admission validation:** none.
7. **Operator testimony:** the exact inquiry string and provenance string are carried; the default testimony status refuses promotion to established fact.
8. **Identity versus standing:** it deterministically constructs an identity field and a question-shaped artifact. It does not prove responsible occurrence or independently establish constitutional question standing. The strongest current implementation claim is explicit-field preservation with negative authority.
9. **Examination request:** no request field or probe contract exists.
10. **Examination eligibility:** no relevance, admission, responsibility, subject-binding, or authority examination occurs.
11. **Meaning of `bounded`:** in this implementation it means caller-explicit content/scope/uncertainty/Unknown fields and enumerated negative boundaries. It is not proof that Book-required bounds were responsibly established.
12. **Purpose and scope source:** `constitutional_intent` and `scope_status` are supplied by the caller only.
13. **Selection keys:** supplied inside `caller_supplied_fields`; the producer neither derives nor selects them.
14. **Arbitrary keys:** yes. Arbitrary caller fields and arbitrary `selection_key` values are constructible.
15. **Refusals:** no language classification; no fact/verified-claim/authority/repository-truth/durable-knowledge/capability creation; no view selection or Question Projection; no recording, ledger write, or cluster mutation. It also does not establish admission, applicability, examination eligibility, finding, answer, reliance, or result standing.

Identity is stable over the producer's payload, not an occurrence seal. An explicit caller id bypasses even hash derivation. Both direct construction and JSON-to-constructor reconstruction can create shape-compatible artifacts; no hidden occurrence or producer token exists.

## Recovery B — Current entrance topology

`ConstitutionalPipelineRequest` requires exactly one `BoundedConstitutionalQuestion`-typed field by annotation and accepts optional contracts, registrations, no-argument view builders, composition purpose, and output format. Python dataclasses do not runtime-enforce annotations, but normal stage access requires the expected attributes. No `isinstance`, invariant, producer, signature, admission, provenance-warrant, or occurrence check is performed.

`invoke_constitutional_pipeline(...)` aliases `request.bounded_question`, projects it, projects capabilities, selects, adapts, composes, and returns every artifact. The same object identity is preserved in `result.bounded_question`; its string id is copied into projection, selection, composition request, provenance explanation, and rendering. This is identity carriage, not producer validation.

- A directly constructed or JSON-reconstructed instance can enter.
- Shape is operationally required; a responsible production occurrence is not.
- The pipeline cannot distinguish the named producer's return from an independently constructed equal artifact.
- It consumes no admission evidence, no admitted-inquiry artifact, no examination-purpose warrant, no present applicability evidence, and no inquiry provenance after the original artifact except provenance explanation/rendering.
- It establishes no new question standing; it accepts and reforms supplied fields.
- Raw CLI fields are refused. That proves only that the CLI no longer originates the question; it does not prove admission, responsible producer occurrence, or a lawful external entrance.
- No bounded-ask road was recovered constructing or supplying this artifact.
- The current public executable CLI has no successful pipeline entrance. Python/API construction is the operational entrance; the diagnostic is a non-test API consumer once handed a request. Tests are the only recovered callers that actually construct requests and invoke the pipeline directly.

The exact first unsupported crossing is therefore constructible question shape → pipeline acceptance as though “already-established”; production occurrence and establishment standing are not checked.

## Recovery C — Question Projection

`project_constitutional_question(...)` copies `bounded_question_id`; extracts exact keys from either `("selection_key", nonempty-value)` or field names beginning `selection_key:`; de-duplicates in encounter order; copies uncertainty; prefixes each source Unknown with `unknown: `; and propagates read/ledger/mutation flags.

It does not normalize prose, infer intent, read Book/Process/Governance/Fidelity content, inspect unrestricted question text, compare constitutional grammar, infer applicability, guess absent keys, remove unsupported keys, or strengthen standing. Unsupported keys remain until Selection labels them unsupported. It produces neither examination eligibility nor a finding. Its responsibility is a deterministic, lossy reform of explicit already-carried coordinates for the Selection consumer. Calling this “recognition” would be false.

## Recovery D — Capability Projection and Selection

Capability Projection iterates the configured read-model contracts, obtains supplied or mechanically derived registrations, invokes a no-argument builder by exact registered name, and maps artifact **type plus nonempty generic content** to one key: Process → `process`, Governance → `governance`, Fidelity → `fidelity`. With no builder/source it emits no keys and `compatibility_answer="Unknown."`. Registration availability, builder availability, generic content availability, and key exposure are separately visible; none proves question-relative applicability.

Selection consumes only the question projection and capability projections. It converts explicit keys to a set and uses set intersection/equality. It never sees question prose or a full view artifact. It does not infer neighbors, compare a claim with rules, prioritize, focus, establish examination eligibility, or select a goal. It selects registered view names for composition where exact keys match.

- **No key:** no selection; uncertainty says no registered view matched.
- **Unsupported key:** preserved as `unsupported selection key: ...`, plus no-match uncertainty when no view matched.
- **Unavailable capability evidence:** contributes no key and `Unknown.`; selection cannot match it. Selection does not add a capability-specific Unknown unless upstream question uncertainty already says so; provenance explanation later makes missing capability evidence visible for unsupported keys.
- **Selected-view standing:** exact-key-compatible registered view name selected for composition, with upstream uncertainty preserved. It is not semantic applicability, focus, goal selection, examination, warrant, authorization, or constitutional relevance.
- **Compatibility scalar:** `No.` when at least one selected capability contributes and all selected sources say `No.`; otherwise `Unknown.`. This scalar is existing view compatibility testimony, not a finding about the supplied question.

## Recovery E — Registered Process, Governance, and Fidelity views

All three are static, no-argument, immutable read models built from module constants. They do not read repository files, current runtime State, or active Book text at build time. Their payloads cite report filenames and emit pre-authored summaries, Unknowns, refusals, and `compatibility_answer="No."`. Selection's capability pass builds them once; Composition independently rebuilds selected views. The same output is reusable across unrelated questions because the question is never an input.

| Registered view | Producer and inputs | Source material/output | Claims, Unknowns, refusals | Consumer and authority limit |
| --- | --- | --- | --- | --- |
| `constitutional_process` | `build_constitutional_process_view()`; no inputs | Module constants citing reports; `ConstitutionalProcessView` with seven generic stages | Describes Pressure through Lawful Stop; preserves five topology/owner Unknowns; no explicit-refusal field | Capability Projection and Composition; static process read model/explanation source, not question-relative applicable-process finding |
| `constitutional_governance` | `build_constitutional_governance_view()`; no inputs | Module constants citing reports; `ConstitutionalGovernanceView` with five generic relationships | Generic governance relations, seven Unknowns, and refusals including governance execution/ownership/runtime governance | Capability Projection and Composition; static governance read model, not adjudication of the supplied claim |
| `constitutional_fidelity` | `build_constitutional_fidelity_view()`; no inputs | Module constant citing `constitutional_fidelity_characterization.md`; generic classifications/discipline | Generic Fidelity classifications, preserved Unknowns, and refusals including runtime evaluation | Capability Projection and Composition; static Fidelity read model, not a Book-expectation-to-current-question/witness comparison and not a Fidelity finding |

No builder receives question identity, content, scope, evidence, claim coordinates, or selection uncertainty. None compares a claim to a Book clause, produces a discrepancy/crossing, initiates inquiry, or establishes implementation authority. “Fidelity View” is not proof of a Fidelity examination; active Book grammar requires a bounded comparison of constitutional grammar, bounded expectation, and implementation witness under an examined seam. View standing here is generic read-model representation standing, weaker and differently purposed than examination or finding standing.

## Recovery F — View Composition

The adapter copies selected registered names, supplied composition label/format, question id, selection uncertainty, and selection boundaries into `ConstitutionalViewCompositionRequest`. Composition validates requested names against registrations/builders, rebuilds each generic view without the question, serializes it, concatenates/de-duplicates each payload's `composition` report filenames, prefixes and preserves Unknowns/refusals, and aggregates the existing compatibility answers.

Composition requires only a constructible request with explicit registered names. It does not reopen Selection, compare views with each other, compare a view with the question, resolve contradictions, cross-examine testimony, discover evidence, or produce a new constitutional assertion. Its `bounded_summary` explicitly says it composes requested read-model views into one bounded explanation without adding authority or resolving Unknowns.

`ConstitutionalViewCompositionArtifact` is therefore an implementation-local bounded explanation composition. It is not an answer, finding, scoped comparison, warranted result, or truth. The `compatibility_answer` is a mechanical aggregation of generic source scalars; it is not question-relative compatibility standing. A renderer or diagnostic may lawfully present/inspect it within this declared explanation boundary. No stronger reliance consumer was recovered.

## Recovery G — Admitted inquiry and bounded examination

The active Book distinguishes possible inquiry, bounded question, method applicability, selection, probe request, execution/output, comparison, finding, reliance, and result/emission. Corpus passes 051--056 describe one non-mandatory local movement with open owner maps and vocabulary. Current runtime searches found neighboring examination modules, but no exact `AdmittedInquiry` artifact/equivalent carrying this topology and no explicit consumption of such standing by the constitutional pipeline.

| Question | Current recovery |
| --- | --- |
| Active `AdmittedInquiry` artifact/equivalent | **Unknown / not recovered.** Generic phrases and neighboring local artifacts do not establish an exact equivalent. |
| Active admitted-inquiry producer | **Unknown / not recovered.** |
| Active bounded-examination artifact | Neighboring method-applicability, selection, and probe-request subjects exist, but no exact artifact implementing passes 054--056 for this pipeline was recovered. |
| Active comparison/finding artifact for this road | **Unknown / not recovered.** |
| Active bounded-result artifact for this road | **Unknown / not recovered.** Composition is not it. |
| Implemented owner map | None recovered. Absence does not warrant inventing one. |
| Admission evidence on `BoundedConstitutionalQuestion` | None. A caller may add an arbitrary field named `admission`, but it remains caller testimony and is ignored by the pipeline unless encoded as a selection key. |
| Examination eligibility consumed | No. |
| Examination output produced | No stage does so. |
| Comparison/finding standing produced | No stage does so. |
| Bounded result formed | No. |
| Explicit crossing/re-entry | None recovered. |

The two movements are neither proven identical nor proven independent. They share broad question/view/examination/Unknown/refusal grammar, while their exact artifact vocabulary, runtime owner map, entry relation, re-entry, and full topology remain Unknown. Described topology is not runtime realization; absence of a runtime owner is not proof that a new owner must be created.

## Required Book-authority table

Implementation facts above are implementation evidence, not Book conclusions. This table supplies the exact active authority for every constitutional conclusion used by this recovery.

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
| --- | --- | --- | --- |
| Question standing | `04-inquiry-and-examination/questions-and-inquiry.md`, `04.Question.A--E` | Bounded question identity/provenance/scope/evidence demand/authority/uncertainty/stop; Seed-owned formation; question is not answer | That this constructor performed the Seed-owned establishment act; admission, examination, answer |
| Inquiry admission | `01-grammar-and-standing/lenses-views-and-roads.md`, availability/applicability/admission/consumption resolution and `01.Uptake.A`; `08-authority-communication-and-stopping/authority-scope.md`, `08.Authority.B` | Admission is separate bounded participation and does not strengthen standing | Exact `AdmittedInquiry` artifact, producer, mandatory admission occurrence, runtime road |
| Bounded examination eligibility | `04-inquiry-and-examination/examination-methods-and-probes.md`, bounded resolution and `04.Examination.A--B` | Local relevance can permit examination; applicability is not selection; inactivity/Unknown are results | That key match is relevance, that the pipeline examines, universal stage order |
| Comparison/finding standing | `04-inquiry-and-examination/examination-methods-and-probes.md`, `04.Examination.C`; `01-grammar-and-standing/external-and-constitutional-grammar.md`, Fidelity production boundary | Preserved-input comparison can produce bounded agreement/conflict/refinement/Unknown; Fidelity requires actual bounded comparison | Truth/warrant/reliance; that composition performs comparison; that Fidelity view is a finding |
| Bounded result formation | `08-authority-communication-and-stopping/authority-scope.md`, `08.Authority.A`; `08-authority-communication-and-stopping/stopping-and-completion.md`, bounded stopping/completion clauses; `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, bounded-result emission resolution | Reliance, stop/completion, and emitted result remain purpose/scope/evidence/authority bounded | One canonical result artifact, truth, global completion, that composition is such a result |
| Explicit handoff | `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, resolution and `08.Communication.A` | “Handoff” must decompose; responsibility transition needs evidence and acceptance/establishment occurrence | That call adjacency or id carriage transitions responsibility; any pipeline/inquiry handoff |
| View selection | `01-grammar-and-standing/lenses-views-and-roads.md`, bounded resolution and distinctions; `04.Question.D` | Representation selection/composition is lens-like unless subject-selection standing is separately evidenced; question and lens applicability differ | Exact matching as semantic applicability, focus, goal selection, examination |
| Projection standing | `06-state-and-projection/projection-and-current-state.md`, projection/current-state bounded resolution; `01-grammar-and-standing/lenses-views-and-roads.md` | Faithful projection/view formation does not strengthen represented source | Admission, recognition, finding, answer, current applicability |
| Explanation standing | `05-evidence-and-knowledge/evidence-provenance-and-explanation.md`, explanation/evidence resolution and distinctions; `08.Authority.A` | Explanation can expose preserved support and limits for a bounded consumer; explanation is not establishment | Answer, truth, upstream producer occurrence, reliance beyond warrant |
| Unknown preservation | `04.Examination.B--C`; `08.Authority.A--B`; `08-authority-communication-and-stopping/refusal-and-non-performance.md`; `08-authority-communication-and-stopping/stopping-and-completion.md` | Unsupported/unbound material remains Unknown or a reasoned refusal/stop without standing expansion | That Unknown proves global absence or mandates implementation |
| Constructor/occurrence boundary | `01-grammar-and-standing/constructors-and-production-authority.md`, bounded resolution | Constructibility and consumer-local acceptance do not prove named producer occurrence or establishment | That producer name/return type grants authority |
| Constitutional road | `01-grammar-and-standing/lenses-views-and-roads.md`, bounded resolution | A road needs producer assertion plus consumer-purpose validation; adjacency/compatibility alone does not establish one | That pipeline order is a universal constitutional road |
| Fidelity realization comparison (historical `07.Realization.B`) | `01-grammar-and-standing/external-and-constitutional-grammar.md`, Fidelity production boundary; `operational_realization_compression_constitutional_correction_001.md`, retained `07.CapabilityMechanism.C` disposition | Bounded constitutional-expectation/implementation-witness comparison can produce scoped Fidelity standing | Runtime Fidelity engine, global certification, that static Fidelity View performed it |

For an exact active Book clause asserting that `BoundedConstitutionalQuestion` is identical to admitted inquiry, or that this pipeline must receive/perform the corpus's entire movement:

```text
classification:
    Unknown

finding:
    no exact active Book authority recovered
```

## Table 1 — Entrance producer/consumer inventory

| Subject or artifact | Producer | Production occurrence | Inputs | Standing produced | Current non-test callers | Consumer | Consumer act | First unsupported crossing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| operator inquiry | Operator/external source | Outside repository; exact occurrence Unknown | Operator words | Attributed testimony/pressure at most | Not applicable | BQ producer if called | Preserve explicit string | Testimony → internal question establishment |
| possible inquiry | Not recovered | Unknown | Pressure/uncertainty bundle in corpus | Possible, not admitted | None recovered | Admission boundary | Unknown | Possibility → admission |
| admitted inquiry | Not recovered | Unknown | Possible inquiry plus local authority evidence | Bounded participation | None recovered | Local examination boundary | Unknown | Admission → examination eligibility |
| `BoundedConstitutionalQuestion` | Public dataclass; named helper remains | Helper occurrence possible but no current non-test witness; direct construction possible | Caller strings/iterables/fields | Constructed identity and explicit-field preservation; constitutional establishment occurrence unproven | Producer: zero | Question Projection via pipeline/API | Reform supplied fields | Constructibility → accepted “already-established” standing |
| `ConstitutionalPipelineRequest` | Direct caller construction | API construction | BQ plus optional capability/composition inputs | Implementation-local invocation request shape | Diagnostic consumes one but does not originate it | `invoke_constitutional_pipeline` | Ordered calls | Request shape → question provenance/standing trusted |
| `ConstitutionalQuestionProjection` | `project_constitutional_question` | Each pipeline call | BQ id, caller fields, uncertainty/Unknowns, flags | Exact-key selection input | Pipeline | Selection | Exact-key input | Explicit coordinate → semantic applicability (not crossed) |
| `ConstitutionalCapabilityProjection` | `project_constitutional_capabilities` | Each pipeline call | contracts, registrations, no-arg builders | Generic registered capability-key availability | Pipeline | Selection | Exact-key input | Availability → applicability (not crossed) |
| `SelectedConstitutionalViews` | `select_constitutional_views` | Each pipeline call | two projections | Registered names compatible by exact key for composition | Pipeline | Composition adapter | Copy names/id/uncertainty | Compatibility → constitutional focus/examination |
| `ConstitutionalViewCompositionRequest` | adapter or direct helper | Each pipeline call/direct construction | selected names or caller names plus labels | Explicit composition request shape | Pipeline | Composition | Validate and build named views | Request → warranted comparison |
| `ConstitutionalViewCompositionArtifact` | `build_constitutional_view_composition` | Each pipeline call/direct CLI composition | explicit registered names; static views | Bounded explanation composition | Pipeline, explicit composition CLI | Rendering, diagnostic, provenance output | Present/inspect | Explanation → finding/answer/result |

## Table 2 — Movement comparison

| Movement | Book standing | Corpus testimony | Current implementation | Producer | Consumer | Relationship | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| question origination | Seed-owned bounded translation/forming act | Possible inquiry identity preserved | Helper only preserves caller fields; pipeline ownership removed | Exact responsible owner not recovered | BQ-shaped consumers | Not proven | Unknown runtime realization |
| question establishment | Requires identity/provenance/scope/evidence/authority/stop | Assumed before pass 054 | No validation/occurrence seal | Not recovered | Pipeline accepts shape | Unsupported entrance crossing | Mixed/Unknown |
| inquiry admission | Separate bounded participation | Pass 052 and 054 | No exact subject found | Not recovered | Not recovered | No crossing | Unknown runtime realization |
| examination eligibility | Relevance permits examination; not selection/execution | Pass 054 | Exact-key view selection is non-equivalent | Not recovered | Not recovered | Broad grammar only | Not implemented here |
| question projection | Lens/projection cannot strengthen source | Navigation only | Copies id/keys/uncertainty | Projection function | Selection | Direct typed call | Implemented local reform |
| capability projection | Availability distinct from applicability | Not the inquiry movement | Builds generic sources and type-derived keys | Capability function/builders | Selection | Direct typed call | Implemented availability projection |
| view selection | Representation selection unless stronger subject evidence | Not examination selection | Exact equality match | Selection function | Adapter | Direct typed call | Implemented composition selection |
| view construction | View formation from sources under method | Not examination output | Static no-arg generic views | Three builders | Capability/Composition | Rebuilt independently | Implemented generic read models |
| view composition | Lens-like bounded representation | Explanation is a possible result only with local authority | Aggregates selected static payloads | Composition function | Renderer/diagnostic | Direct typed call | Implemented explanation composition |
| comparison/finding | Preserved independent inputs and bounded comparison | Pass 055 | No question/view comparison | Not recovered | Not recovered | No crossing | Unknown runtime realization |
| bounded result | Local warrant/reliance/explanation/stop/completion act | Pass 056 | Composition lacks finding/warrant/result act | Not recovered | Not recovered | No crossing | Unknown runtime realization |

## Table 3 — Pipeline stage responsibility

| Stage | Input standing | Owned act | Output standing | What it preserves | What it refuses | What it does not establish |
| --- | --- | --- | --- | --- | --- | --- |
| `BoundedConstitutionalQuestion` | Caller representations | Immutable explicit-field construction | Question-shaped representation and stable id | Testimony, provenance string, content, intent/scope labels, uncertainty/Unknowns | Promotions, selection, recording/mutation | Responsible establishment, admission, eligibility, answer |
| Question Projection | Constructible BQ | Exact coordinate reform | Selection input | id, explicit keys, uncertainty/Unknowns, flags | Semantic inference, discovery, selection | Applicability, relevance, finding |
| Capability Projection | Contracts/registrations/static builders | Generic key exposure | Availability input | registration name, key, compatibility/flags | inference, registration repair, Selection | Question-relative applicability |
| Selection | Two projections | Exact equality match | Names selected for composition | id, upstream uncertainty, unsupported keys | raw prose, semantic reasoning, ranking/planning | focus, goal selection, examination eligibility |
| Composition adapter | Selection artifact | Field copying | Composition request | names, id, uncertainty, boundaries | heuristics/discovery | comparison request or result warrant |
| Composition | Explicit registered names | Rebuild, serialize, aggregate | Bounded explanation composition | contributors, evidence filenames, Unknowns/refusals | reasoning, discovery, authority, mutation | cross-examination, finding, answer, bounded result |
| Provenance explanation | Completed result | Report typed handoffs | Implementation-local provenance explanation | ids, keys, matches, uncertainty, contributor limits | all pipeline acts and verification | producer occurrence, semantic explanation, reliance |
| Rendering | Completed artifacts | Stable presentation | Human/JSON representation | represented stage fields | standing promotion | receipt, uptake, answer, truth |

## Table 4 — Conversation-gloss cross-check

| Term | Conversation use | Exact repository subject recovered | Exact active Book authority | Implementation owner | Classification |
| --- | --- | --- | --- | --- | --- |
| recognition | Characterizing a claim's constitutional shape | None in this pipeline; exact-key match only | No clause making exact matching recognition | None | conversation-only gloss |
| doubt | Reasoning posture | Uncertainty/Unknown fields are nearby but non-equivalent | Unknown/refusal clauses | Field-preservation owners only | nearby but non-equivalent repository term |
| challenge | Adversarial testing | `04.Examination.C` cross-examination is narrower | `04.Examination.C` | None in this pipeline | nearby but non-equivalent repository term |
| synthesis | Combining reasoning | Composition concatenates generic read models but does not synthesize claims | Lens/view grammar limits composition | Composition only | nearby but non-equivalent implementation-local behavior |
| focus | Current constitutional relevance/attention | No question-relative focus subject here | Question/lens applicability distinction | None | conversation-only gloss for this road |
| coherence application | Bringing all applicable distinctions to a claim | No such implemented act | Consumer-local coherence constraints in lens/uptake grammar do not create a universal act | None | conversation-only gloss / Unknown realization |

## Recovery H — “coherence necessarily applied”

**No.** The pipeline does not mechanically bring all applicable constitutional distinctions into contact with a supplied claim. It composes only exact registered generic views selected through explicit caller coordinates.

| Coordinate | Current standing |
| --- | --- |
| claim characterization | Not implemented by this road; caller-authored prose only |
| question establishment | Helper-shaped construction exists; responsible occurrence/entrance remains unproven |
| selection-key production | Explicit caller supply; projection extracts it |
| view availability | Implemented by contracts, registrations, builders, and capability keys |
| view applicability | Not examined |
| view selection | Exact-key names selected for composition |
| view construction | Static generic no-argument builders |
| view composition | Implemented bounded explanation aggregation |
| bounded examination | Not implemented in this road |
| comparison | Not implemented in this road |
| finding | Not produced |
| result | No bounded-result standing produced |

## Direct verdicts

1. **What produces a BQ?** A public dataclass can construct one; the named helper deterministically returns one from caller fields.
2. **Called outside tests?** The named helper has zero recovered non-test call sites.
3. **Consumes admitted inquiry?** No.
4. **Establishes occurrence?** No constitutionally warranted occurrence is represented; a live helper return witnesses only that call.
5. **Can direct construction bypass it?** Yes.
6. **Pipeline entry standing?** Operationally, a shape-compatible BQ object in `ConstitutionalPipelineRequest`; the docstring says already-established, but that standing is not verified.
7. **Verify establishment?** No.
8. **Consume admission evidence?** No.
9. **Question Projection adds?** A narrower exact-key/id/uncertainty selection representation; no stronger standing.
10. **Keys explicit or inferred?** Explicit caller coordinates only.
11. **Semantic recognition?** No.
12. **Applicability?** No.
13. **Focus?** No.
14. **Views consume question?** No.
15. **Examine claim?** No.
16. **Fidelity finding about question?** No.
17. **Composition comparison/cross-examination?** No.
18. **Bounded-result standing?** No.
19. **Composition artifact an answer?** No.
20. **A finding?** No.
21. **An explanation?** Yes: implementation-local bounded explanation composition.
22. **Exact admitted inquiry subject implemented?** Not recovered; Unknown.
23. **Exact bounded examination act implemented?** Not in this road; an equivalent end-to-end runtime act remains Unknown.
24. **Comparison/finding standing implemented?** Not in this road; exact runtime realization remains Unknown.
25. **Bounded result formation implemented?** Not in this road; exact runtime realization remains Unknown.
26. **Explicit inquiry-to-pipeline crossing?** None recovered.
27. **All applicable Book distinctions applied?** No.
28. **Only explicitly selected registered views?** Yes.
29. **Gloss without recovered standing?** Recognition, focus, synthesis-as-competency, doubt/skepticism owner, universal coherence application, intelligence, and “last inch”; challenge has only narrower non-equivalent cross-examination grammar.
30. **Exact Unknown relation?** Whether and how a responsibly admitted inquiry becomes a responsibly established BQ, examination-eligible artifact, or pipeline input; whether a neighboring runtime realizes examination/comparison/result and can re-enter this road.
31. **Implementation change warranted?** No implementation change is warranted by this recovery alone.
32. **Smallest next lawful action?** Stated once below.

## Single smallest next lawful action

**Recover inquiry-admission standing independently.**
