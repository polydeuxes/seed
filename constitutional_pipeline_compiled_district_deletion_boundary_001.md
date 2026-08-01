# Constitutional-pipeline compiled district deletion boundary 001

## Recovery boundary and verdict

This is one report-only recovery against merged `main` at `a895027` (PR 2136). It asks only whether the current constitutional-pipeline district has an independently warranted current producer, consumer, or constitutional responsibility. It does not design a replacement road and does not recover operator ingress, common grammar, BOGE, advancement, Gap/Demand, inquiry admission, evidence competency, method applicability, probes, findings, Hurricane, Eye, or federation.

**Verdict.** The working characterization is confirmed for the pipeline proper: the caller supplies question wording, intent, scope, uncertainty/Unknown labels, and internal selection tokens; developers supply the three categories, exact capability tokens, static payloads, and the selection/composition topology; the implementation copies, type-checks, exact-matches, rebuilds, aggregates, and renders. No completed stage consumes projected `State`, current evidence, active Book text, repository file contents, a responsible question-formation occurrence, applicability evidence, or an examination finding. The diagnostic, registrations, CLI surfaces, documentation, and tests form visibility and support around that same closed district.

There is one narrow falsification of “delete every named artifact”: `BoundedConstitutionalQuestion` is also the concrete input type used by the separately registered `--examination-frontier` road and by the method-applicability and examination-policy modules. The active frontier CLI constructs it from JSON and consumes `bounded_question_id`, `inquiry_provenance`, and `bounded_question`. That is an exact non-district runtime consumer, not merely an import. This report therefore preserves the type and those fields as an implementation compatibility input under their existing consumer; it does **not** infer that the type has internal-question standing, and it does not preserve the named producer, pipeline renderers, or unused fields on that basis. The exclusions prevent a redesign of those examination modules here.

No other independently active producer, consumer, responsibility, cache, publication road, or unrelated read model was found. Another report is not required. The next lawful action is one demolition PR deleting the developer-compiled district while retaining the minimal examination-frontier input compatibility and general read-model/diagnostic infrastructure.

## Method and evidence classes

The recovery searched every Python definition and call of the named classes/functions, every flag, diagnostic inventory and shape registration, read-model contract/registration, test, README/guide reference, and repository report name. Results were classified as:

* **production call** — an executable call on a non-test road;
* **test call** — a call below `tests/` only;
* **import only** — no credit unless the object is instantiated, called, or read;
* **registration visibility** — metadata naming a builder/renderer, not consumption of its constitutional content;
* **diagnostic visibility** — observation of the implementation surface, not independent warrant;
* **documentation reference** — claims or instructions, not a runtime caller;
* **historical testimony** — implementation reports retained as evidence of past work, not active necessity.

The named producer `produce_bounded_constitutional_question(...)` has zero production calls. `ConstitutionalPipelineRequest(...)` also has zero production constructions. The imports of pipeline request/invocation in `scripts/seed_local.py` are unused after PR 2136: both pipeline flags immediately produce parser errors. The diagnostic can invoke the pipeline only when another Python caller supplies a request, and all such current constructions are tests. This is district self-consumption, not ingress.

## Recovery A — exact producer/consumer graph

| Subject / function | Definition | Producer | Production calls and consumers | Test-only consumers | Other references | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `BoundedConstitutionalQuestion` | `seed_runtime/bounded_constitutional_question.py` | constructor; named helper below | `examination_frontier.input_from_json_dict` constructs it; frontier, method applicability, and policy projection type-check/read it; pipeline request carries it | bounded-question, pipeline/projection, candidate-work/frontier/applicability/policy tests | inventory/CLI prose names it | mixed district/examination compatibility type; retain minimally |
| `produce_bounded_constitutional_question` | same | explicit caller values only | none | bounded-question, question/capability projection, candidate examination, frontier/applicability/policy | historical reports | delete; constructor success is not production occurrence |
| bounded-question JSON/human renderers | same | render the object | none outside district | bounded-question tests | none independently | delete with district |
| `ConstitutionalPipelineRequest` | `seed_runtime/constitutional_pipeline.py` | callers | no production constructor; diagnostic accepts it | pipeline, diagnostic, wiring, provenance, public-surface tests | unused CLI import | delete |
| `invoke_constitutional_pipeline` / `ConstitutionalPipelineResult` | same | request only | diagnostic wrapper invokes it; no independently produced request | pipeline family tests | shape-audit metadata; unused CLI import | district-only cycle; delete |
| provenance explanation | same | completed pipeline result | pipeline JSON/human renderer | provenance/public tests | historical report | renderer-local explanation; delete |
| pipeline JSON/human renderers | same | completed pipeline result | none; CLI positive branch is gone | pipeline/public tests | shape/inventory | delete |
| `ConstitutionalQuestionProjection` / `project_constitutional_question` | `seed_runtime/constitutional_view_selection.py` | bounded question | pipeline only | question/capability projection tests | historical reports | compiled routing projection; delete |
| `ConstitutionalCapabilityProjection` / `project_constitutional_capabilities` | same | contracts, registrations, static builders | pipeline only | capability projection tests | historical reports | compiled routing projection; delete |
| `SelectedConstitutionalViews` / `select_constitutional_views` | same | the two projections | composition-request adapter only | selection/projection tests | historical reports | exact-token matcher; delete |
| selection-to-composition adapter | same | selected names/id/uncertainty | pipeline only | selection tests | none independently | delete |
| Process view, builder, formatters | `seed_runtime/constitutional_process_view.py` | zero-input static builder | standalone CLI, capability projection, composition | process/capability/composition tests | diagnostic/read-model registrations, docs/reports | active presentation but no independent constitutional act; delete |
| Governance view, builder, formatters | `seed_runtime/constitutional_governance_view.py` | zero-input static builder | standalone CLI, capability projection, composition | governance/capability/composition tests | diagnostic/read-model registrations, docs/reports | active presentation but no independent constitutional act; delete |
| Fidelity view, builder, formatters | `seed_runtime/constitutional_fidelity_view.py` | zero-input static builder | standalone CLI, capability projection, composition | fidelity/capability/composition tests | diagnostic/read-model registrations, docs/reports | active presentation but no bounded comparison; delete |
| composition request/artifact/build/render | `seed_runtime/constitutional_view_composition.py` | CLI explicit names or Selection | standalone composition CLI and pipeline | composition/selection tests | diagnostic/read-model metadata, docs/reports | district aggregation; delete |
| pipeline diagnostic and stage wrappers | `seed_runtime/constitutional_pipeline_diagnostic.py` | request or completed pipeline result | wrapper calls pipeline; refusal-only CLI never calls wrapper | diagnostic tests | inventory/shape metadata | observes district only; delete |
| pipeline-specific contracts/registrations | `seed_runtime/read_model_ownership.py` | static tuple expansion | registration flag validation, Selection, Composition | ownership/capability/pipeline tests | CLI/parser and diagnostics | district-local entries; delete entries, retain machinery |

### Exact edges

```text
caller/test-created BoundedConstitutionalQuestion
  -> ConstitutionalPipelineRequest
  -> project_constitutional_question
       caller_supplied_fields[selection_key*] -> exact selection_keys
  -> project_constitutional_capabilities
       constitutional contracts -> registrations -> zero-input static builders
       Python artifact type + nonempty tuple -> process/governance/fidelity key
  -> select_constitutional_views
       exact intersection(question keys, capability keys) -> registered names
  -> selected_constitutional_views_to_composition_request
  -> build_constitutional_view_composition
       rebuild each named zero-input view -> serialize -> aggregate payload fields
  -> ConstitutionalPipelineResult
  -> provenance explanation -> pipeline JSON/human renderer
  -> optional pipeline diagnostic -> stage JSON/human renderer
```

The only edge leaving that graph is:

```text
--examination-frontier JSON
  -> examination_frontier.input_from_json_dict
  -> BoundedConstitutionalQuestion(**bounded_inquiry)
  -> project_examination_frontier
  -> reads bounded_question_id, inquiry_provenance, bounded_question
```

Method-applicability and policy functions additionally accept/type-check the same class and read its identifier/provenance/question. Their present production ingress was not recovered further because those districts are explicitly excluded, but their executable use is enough to prevent deletion of the class by name in the demolition PR.

## Recovery B — `BoundedConstitutionalQuestion`

### Table 2 — Field ownership

| Field | Supplied or derived | Actual source | Actual consumer | Independent standing | Disposition |
| --- | --- | --- | --- | --- | --- |
| `bounded_question_id` | caller-supplied or hash-derived | caller values, with no projected evidence | pipeline stages; frontier, method applicability, policy projection | identity coordinate only; no question standing | retain minimally for external examination compatibility |
| `operator_inquiry` | supplied | caller prose | pipeline render/provenance only | attributed testimony label only | delete from retained minimal input unless excluded consumers' JSON compatibility requires whole current schema |
| `inquiry_provenance` | supplied | caller string | pipeline render/provenance; frontier and method applicability | represented provenance, not verified production | retain minimally |
| `bounded_question` | supplied | caller wording | pipeline renderer (projection does not read content); frontier and method applicability | caller-authored question-shaped material, not Seed formation | retain minimally as external input text |
| `constitutional_intent` | supplied | caller label | pipeline renderer only | none established | delete with district |
| `scope_status` | supplied | caller label | pipeline renderer only | none established | delete with district |
| `uncertainty` | supplied | caller labels | Question Projection copies it; renderers | attributed labels only | delete with district unless retained temporarily for JSON compatibility |
| `unknowns` | supplied | caller labels | Question Projection prefixes `unknown:`; renderers | does not establish constitutional Unknown standing | delete with district unless retained temporarily for JSON compatibility |
| `caller_supplied_fields` | supplied map, sorted/stringified | caller | Question Projection extracts `selection_key` names/values | routing coordinates only | delete |
| `testimony_status` | static default | developer | renderers/provenance only | assertion about boundary, not produced validation | delete |
| `read_only_boundaries` | static default | developer | Selection handoff/renderers only | implementation declarations only | delete |

The booleans `read_only`, `writes_event_ledger`, and `mutates_cluster`, although omitted from the requested field list, are static constructor defaults copied/aggregated only by the district. They do not turn the object into a diagnostic occurrence and should not be used as preservation grounds.

### Direct B answers

1. **Active non-test named producer? No.** Every call to `produce_bounded_constitutional_question(...)` is in tests.
2. **Active non-district consumer? Yes, narrowly.** The examination-frontier input/CLI road constructs and reads the class; method-applicability and policy code also consume it.
3. **Any projected field? No.** The identifier is a hash of caller values; every semantic label comes from caller or developer default.
4. **Any field establishes named standing? No.** Names/defaults preserve representations only.
5. **Responsible formation validation? No.** Consumers check type, identity correspondence, or use text coordinates; none validates Seed-owned formation inputs such as evidence demand, authority limits, or lawful stop.
6. **Would deletion remove an active capability?** Deleting the class outright would break `--examination-frontier`; deleting its named producer and district-only fields/uses removes no active ingress, inquiry, examination, or result occurrence. Preserve minimal compatibility in the demolition implementation.
7. **Independently worth preserving?** Only the three fields actually read by excluded examination consumers and the construction compatibility they currently require. This is implementation compatibility, not endorsement of the class name or standing.

Classification: a **mixed caller-authored external-characterization/routing object**, used by the compiled district and as an input container by an external examination road. It is not a faithful Seed-formed internal question.

## Recovery C — projections

### Question Projection

It reads the bounded-question identifier, `uncertainty`, `unknowns`, and `caller_supplied_fields`. It copies identity and uncertainty; prefixes each caller Unknown with `unknown:`; extracts values from the exact field name `selection_key` or key suffix `selection_key:<token>`; and discards the actual question, inquiry, provenance, intent, scope, testimony status, and boundaries. It sees no question content, evidence, goal, subject, Book grammar, or applicability testimony. Its only production consumer is exact-key Selection inside the pipeline. **Classification: compiled routing projection.**

### Capability Projection

“Capability” means: a registered name has one of three Python artifact types whose developer-authored payload contains a nonempty tuple (`stages`, `relationships`, or `classifications`). The corresponding hard-coded token is `process`, `governance`, or `fidelity`. It is representational availability, not an operational competency, applicable method, or current occurrence. Keys come from artifact type and non-emptiness, not evidence. Contracts/registrations are consumed independently only as CLI/diagnostic metadata for the same static views; no other road uses a projected capability. **Classification: compiled routing projection.**

Neither projection strengthens source standing lawfully; neither has an external consumer.

## Recovery D — exact-key Selection

`select_constitutional_views(...)` consumes only a tuple of question tokens/uncertainty/flags and tuples of registered names, capability tokens, compatibility strings, and flags. It does not inspect evidence or question content; establish applicability; select an examination method or constitutional subject; rank, reason, or validate scope. It intersects caller-supplied tokens with developer-supplied tokens and returns matching registered names, copied/added uncertainty, and an aggregate compatibility string. Only the composition-request adapter/pipeline consumes the result. Deletion removes no selection capability elsewhere in Seed. Determinism and tests do not change this verdict.

## Recovery E — static views

| View | Builder input | Runtime material read | What it actually is | Non-test consumers | Independent consumer outside district | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| Process | none | no State, Book, files, question, subject, scope, or occurrence | static developer-authored stages and strings naming historical reports | standalone renderer, capability projection, composition | none; standalone CLI is presentation of this payload | delete |
| Governance | none | no State, Book, files, question, subject, scope, or occurrence | static developer-authored relationships and strings naming historical reports | standalone renderer, capability projection, composition | none | delete |
| Fidelity | none | no State, Book, files, question, witness, seam, expectation, scope, or occurrence | static developer-authored summary/classifications wrapping one historical report name | standalone renderer, capability projection, composition | none; it performs no bounded comparison | delete |

Their source-file evidence tuples are strings; builders do not open or validate those reports. Process is not a current process projection. Governance is not current governance examination. Fidelity is not a finding because it compares neither constitutional grammar nor expectation against an implementation witness. Each is district-local operator presentation scaffolding even though each has a positive standalone CLI renderer.

## Recovery F — composition and explanation

Composition validates requested names against the district contract/builder maps, then **rebuilds** each static view, serializes it, and concatenates/deduplicates selected payload fields. It does not compare views with each other, a view with a question, evidence with Book grammar, or anything with current State. It resolves no conflict; establishes no finding, answer, reliance, or bounded result; and never reads the question beyond preserving an optional identifier. Its only consumers are its own renderer/JSON serializer, the pipeline result, diagnostic wrappers around that result, the standalone district CLI, and tests.

* **Composition request:** explicit names, purpose label, output-format label, optional ID and copied uncertainty/boundaries; district-local routing DTO.
* **Composition artifact:** rebuilt static payloads plus concatenated strings and static boundary claims; district-local aggregate.
* **Provenance explanation:** derives token matches and stage summaries from an already completed result; it explains mechanics only and performs no constitutional act.
* **JSON/human renderers:** representations of district artifacts, not independent consumers.
* **Diagnostic stage wrappers:** copy fields/flags from the same result; diagnostic visibility, not a capability.

## Recovery G — registrations and ownership

### Table 3 — Registration disposition

| Registration/contract | Builder | Consumers | Shared or district-local | Deletion effect | Disposition |
| --- | --- | --- | --- | --- | --- |
| `constitutional_process` | static Process builder | CLI flag collection, capability projection, composition, inventory/shape, tests | district-local entry in shared registry | removes only Process surface/key | delete with district |
| `constitutional_governance` | static Governance builder | same | district-local | removes only Governance surface/key | delete with district |
| `constitutional_fidelity` | static Fidelity builder | same | district-local | removes only Fidelity surface/key | delete with district |
| `ConstitutionalReadModelContract`, helper, tuple | string metadata for the three above | district only plus tests | district-local contract layer | no unrelated cache/publication effect | delete with district |
| `ReadModelViewRegistration` and generic registration helpers | many shared read-model builders | parser validation and unrelated read-model tests/roads | shared | deletion would affect state/current observation/requirement/capability/issue registrations | retain shared infrastructure |
| nonconstitutional entries in `READ_MODEL_VIEW_REGISTRATIONS` | state/current views | `scripts/seed_local.py`, tests | shared/independent | unrelated flags and metadata would break | retain independent entries |
| construction/cache identity, lookup, publication machinery in `read_model_ownership.py` | generic read-model functions | State/read-model/cache consumers | shared | unrelated runtime/cache behavior would break | retain shared infrastructure |

No constitutional registration is used by cache lookup/publication or another repository road. The shared registry mechanism is not a warrant for its three district entries.

## Recovery H — CLI, diagnostics, documentation, and tests

The two pipeline flags have no positive behavior: each immediately calls `parser.error`. Their associated raw-field arguments are now orphaned district inputs. Removing the flags removes no lawful refusal required by another road; absence of an unsupported flag supplies the ordinary parser boundary without claiming a pipeline API exists.

The three standalone view flags and composition flag do render positive output, but only the static district payloads. They are visibility for dead code, not independent constitutional capability. Inventory and shape entries observe precisely these district surfaces and must be removed in the demolition PR under the operational visibility contract. None records; all declare no event-ledger writes and no cluster mutation.

### Table 4 — test and documentation disposition

| Path | What it protects/describes | Current or historical | Shared dependency | Demolition disposition |
| --- | --- | --- | --- | --- |
| `tests/constitutional_pipeline_test_support.py` | pipeline fixture construction | pipeline-only | none | delete |
| `tests/test_bounded_constitutional_question.py` | producer/renderers | pipeline-only | none; excluded examination tests separately cover their input use | delete |
| `tests/test_constitutional_question_projection.py` | caller-token projection | pipeline-only | none | delete |
| `tests/test_constitutional_capability_projection.py` | static type-to-token projection/selection | pipeline-only | none | delete |
| `tests/test_constitutional_view_selection.py` | exact-key Selection/adapter | pipeline-only | none | delete |
| `tests/test_constitutional_process_view.py` | static Process payload/CLI | pipeline-only | none | delete |
| `tests/test_constitutional_governance_view.py` | static Governance payload/CLI | pipeline-only | none | delete |
| `tests/test_constitutional_fidelity_view.py` | static Fidelity payload/CLI | pipeline-only | none | delete |
| `tests/test_constitutional_view_composition.py` | static aggregation/CLI | pipeline-only | none | delete |
| `tests/test_constitutional_pipeline.py` | orchestration/result/rendering | pipeline-only | none | delete |
| `tests/test_constitutional_pipeline_diagnostic.py` | diagnostic wrappers and refusal flag | pipeline-only | none | delete |
| `tests/test_constitutional_pipeline_integration_wiring.py` | duplicate end-to-end wiring | pipeline-only | none | delete |
| `tests/test_constitutional_pipeline_provenance_explanation.py` | explanation/rendering | pipeline-only | none | delete |
| `tests/test_constitutional_pipeline_public_surface.py` | duplicate API/refusal behavior | pipeline-only | none | delete |
| `tests/test_diagnostic_inventory.py` | shared inventory including district rows | current shared suite | many diagnostics | edit only: remove district expectations |
| `tests/test_diagnostic_shape_audit.py` | shared shape audit including district specs | current shared suite | many diagnostics | edit only: remove district expectations |
| `tests/test_read_model_ownership.py` | shared registry plus district contracts | current shared suite | shared machinery | edit only: remove district-specific assertions, retain shared tests |
| `tests/test_question_surface_inventory.py` | PR 2136 absence/refusal assertions | current but pipeline-specific assertions | broader inventory suite | edit only: remove obsolete flag assertion; retain absence protection if it remains meaningful without the flag |
| `tests/test_candidate_examination_work.py`, `tests/test_examination_frontier.py`, `tests/test_examination_method_applicability.py`, `tests/test_examination_policy_projection.py` | excluded examination districts using the type/producer as fixture | current outside district | exact non-district dependency | do not delete; adapt only as forced by minimal retained input boundary |
| `constitutional_pipeline_operations.md` | active operator/API guide and docs index target | active documentation | none | delete |
| `docs/README.md` | link to operations guide | active index | shared document | edit only: remove pipeline link |
| `constitutional_pipeline_operational_documentation_001.md` | implementation report containing obsolete commands | historical testimony despite its title | none | retain historical; do not treat commands as active guidance |
| root `*constitutional*pipeline*`, bounded-question, projection, selection, composition, view, diagnostic, contract implementation/recovery reports | past implementation/recovery testimony | historical | none | retain as historical testimony |
| `book_of_seed/constitutional_view_composition_consumer_recovery_001.md` and `book_of_seed/constitutional_view_composition_package_standing_repair_001.md` | historical recovery testimony | historical Book-area report, not active clause | none | retain unchanged |

Historical reports should remain because deletion does not erase implementation history. Active operator instructions must not remain linked or presented as usable. No historical report is a production consumer.

## Active Book constraints used

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
| --- | --- | --- | --- |
| caller question-shaped material is not an internal question; formation is Seed-owned | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, “Question standing” paragraph 1 and “External grammar cannot inject…” paragraph | rejects standing claimed from caller fields | does not demand a replacement implementation in demolition |
| implementation family/dispatch taxonomy is not constitutional grammar/applicability | same file, “External grammar cannot inject…” paragraph | exact tokens/registrations remain realization coordinates | does not make all implementation routing unlawful |
| missing realization does not transfer formation to operator; public ask may be compatibility/diagnostic only | same file, “Seed-owned question formation” final paragraph | prevents preserving caller-owned formation as substitute | does not require this disconnected pipeline to exist |
| constructor/type success does not prove producer occurrence or standing | `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`, first substantive paragraph | distinguishes the dataclass/helper from responsible formation | does not forbid retaining a compatibility input type |
| artifact shape does not supply warrant | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, first substantive paragraph | typed artifacts/default claims do not establish standing | does not infer the artifact is false |
| view availability is not consumer applicability/uptake/reliance | `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`, availability paragraph | registrations/static views do not prove applicable competency | does not deny representation can be useful when independently consumed |
| projection/compression cannot strengthen inputs or erase required standing | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, lossless-purpose paragraph | copied tokens/labels remain at caller standing | does not require every projection to preserve every field |
| Fidelity finding requires bounded grammar/expectation/witness comparison | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, Fidelity paragraph | static Fidelity classifications are not a finding | does not recover a new Fidelity implementation |
| downstream reliance requires preserved bounded warrant | `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`, reliance paragraph | composition/rendering cannot invent reliance | does not prove no future consumer could rely lawfully |

Book grammar constrains claims; it is not used here to preserve code lacking a current responsibility.

## Table 1 — component disposition

| Component | Active producer | Non-test consumer | Independent consumer outside district | Constitutional act | Deletion effect | Proposed disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `BoundedConstitutionalQuestion` minimal input shape | frontier JSON constructor | frontier/applicability/policy | yes, examination frontier exactly | none established; compatibility representation | outright deletion breaks active frontier CLI | retain independent component |
| named bounded-question producer and district-only fields/renderers | none | pipeline only | no | no responsible formation | none outside tests/district | delete with district |
| pipeline request/result/invocation | none externally | diagnostic/renderers | no | ordered calls only | removes no ingress/result road | delete |
| Question Projection | pipeline | Selection | no | copies routing tokens | none | delete |
| Capability Projection | pipeline | Selection | no | maps types to tokens | none | delete |
| Selection | pipeline | Composition adapter | no | exact token comparison only | none elsewhere | delete |
| Process view | zero-input builder/CLI | CLI/projection/composition | no independent content consumer | no process occurrence | removes static surface | delete |
| Governance view | zero-input builder/CLI | CLI/projection/composition | no | no governance examination | removes static surface | delete |
| Fidelity view | zero-input builder/CLI | CLI/projection/composition | no | no bounded comparison/finding | removes static surface | delete |
| composition request/artifact/builders | explicit CLI/Selection | renderers/pipeline | no | rebuild/aggregate only | removes static composition | delete |
| provenance explanation/renderers/serializers | result | CLI/tests | no | representation only | removes district output | delete |
| pipeline diagnostic | API wrapper only | refusal CLI does not invoke | no | district observation only | removes visibility for district | delete |
| constitutional contracts/registrations/specs | static declarations | district CLI/diagnostics | no | availability metadata only | removes only district metadata | delete with district |
| generic read-model registry/cache/construction machinery | active shared runtime | unrelated State/read models | yes | implementation infrastructure | unrelated roads break if removed | retain shared infrastructure |
| generic diagnostic inventory/shape mechanisms | active shared CLI | all diagnostics | yes | operational visibility infrastructure | unrelated diagnostics break | retain shared infrastructure |
| historical implementation reports | past authors | readers only | n/a | testimony only | history would be erased | historical report only |

## Mutual-support test

Apply simultaneous deletion, not file-by-file charity:

* Pipeline needs Question Projection; Projection exists for Selection; Selection exists for Composition; Composition rebuilds views; views are registered for capability tokens and Composition; diagnostics observe those stages; tests assert the cycle; active documentation describes it. Removing that whole strongly connected support district leaves no external pipeline request producer or result consumer broken.
* The three standalone view CLI calls are outward edges only in the presentation sense: they display zero-input static developer payloads. They do not cause a current constitutional occurrence or feed another independent road. They fall with the district.
* The read-model and diagnostic **mechanisms** have many outside consumers and survive; only individual district registrations/specs fall.
* The one genuine crossing edge is the examination-frontier road's construction/read of `BoundedConstitutionalQuestion`. Preserve the minimum compatible input boundary while removing pipeline ownership and standing claims. This crossing does not preserve the producer because the active road calls the dataclass constructor directly.

**Result:** if every component whose only consumers are inside the district is removed simultaneously, no independently active producer, consumer, or constitutional responsibility breaks. With the minimal question-shaped compatibility retained, simultaneous deletion does not remove a real current Seed capability.

## Required direct verdicts

1. **Is `BoundedConstitutionalQuestion` consumed outside this district?** Yes: exact executable examination consumers exist, including active `--examination-frontier` JSON construction/use.
2. **Is its named producer called outside tests?** No.
3. **Does it preserve a Seed-formed internal question?** No; it preserves caller-authored fields without a Seed-owned formation occurrence.
4. **Is it a mixed external-characterization/routing object?** Yes.
5. **Does Question Projection project evidence-derived question standing?** No.
6. **Does Capability Projection project real applicable competencies?** No; it projects static artifact availability/type tokens.
7. **Does Selection perform anything beyond exact token matching?** No, apart from uncertainty/flag aggregation.
8. **Does any static view consume current question or evidence material?** No.
9. **Does any static view perform Process, Governance, or Fidelity examination?** No.
10. **Does Composition produce a finding or bounded result?** No; it aggregates static payloads.
11. **Does the diagnostic expose an independent capability?** No.
12. **Do refusal-only CLI flags serve any current positive road?** No.
13. **Are any pipeline registrations independently used?** No; only the shared registration mechanism is.
14. **Are any pipeline artifacts required by unrelated runtime code?** Only the `BoundedConstitutionalQuestion` compatibility type/three read fields used by excluded examination code.
15. **Would simultaneous deletion break a real current Seed capability?** Not if that minimal compatibility is preserved; outright deletion of the class would break examination frontier.
16. **What shared infrastructure must survive?** Generic read-model registration/construction/cache/publication machinery; generic diagnostic inventory/shape audit; unrelated CLI/parser/read models; the minimal examination input compatibility.
17. **What exact paths should be deleted next?** Listed in the manifest below.
18. **What historical reports should remain?** All existing implementation/recovery/audit reports, including pipeline operational implementation testimony and Book-area historical reports.
19. **What active documentation should be deleted/corrected?** Delete `constitutional_pipeline_operations.md`; remove its link from `docs/README.md`.
20. **Is another report required before demolition?** No.
21. **Single next lawful action?** One demolition PR deleting the compiled district while preserving independently consumed shared/minimal compatibility infrastructure.

## Exact deletion manifest for the next PR

Every path below exists at this recovery commit.

### Delete together

```text
seed_runtime/constitutional_pipeline.py
seed_runtime/constitutional_pipeline_diagnostic.py
seed_runtime/constitutional_view_selection.py
seed_runtime/constitutional_view_composition.py
seed_runtime/constitutional_process_view.py
seed_runtime/constitutional_governance_view.py
seed_runtime/constitutional_fidelity_view.py

tests/constitutional_pipeline_test_support.py
tests/test_bounded_constitutional_question.py
tests/test_constitutional_capability_projection.py
tests/test_constitutional_fidelity_view.py
tests/test_constitutional_governance_view.py
tests/test_constitutional_pipeline.py
tests/test_constitutional_pipeline_diagnostic.py
tests/test_constitutional_pipeline_integration_wiring.py
tests/test_constitutional_pipeline_provenance_explanation.py
tests/test_constitutional_pipeline_public_surface.py
tests/test_constitutional_process_view.py
tests/test_constitutional_question_projection.py
tests/test_constitutional_view_composition.py
tests/test_constitutional_view_selection.py

constitutional_pipeline_operations.md
```

### Edit as part of that same demolition

```text
seed_runtime/bounded_constitutional_question.py
  remove the uncalled named producer and pipeline-only renderers/fields;
  preserve only construction and fields required by excluded examination consumers,
  with no internal-question standing claim

seed_runtime/read_model_ownership.py
  remove ConstitutionalReadModelContract, constitutional contract tuple/helper,
  and the three constitutional registrations; preserve all generic machinery and
  nonconstitutional registrations

scripts/seed_local.py
  remove district imports, parser flags/arguments, JSON eligibility, flag validation,
  refusal branches, and positive static-view/composition branches

seed_runtime/diagnostic_inventory.py
  remove constitutional_process, constitutional_governance,
  constitutional_fidelity, constitutional_pipeline,
  constitutional_pipeline_diagnostic, and constitutional_view_composition entries

seed_runtime/diagnostic_shape_audit.py
  remove the matching six implementation specs

tests/test_diagnostic_inventory.py
tests/test_diagnostic_shape_audit.py
tests/test_read_model_ownership.py
tests/test_question_surface_inventory.py
  remove only district expectations; retain shared verification and PR-2136
  namespace-absence coverage where still applicable

docs/README.md
  remove the active constitutional-pipeline operations link

tests/test_candidate_examination_work.py
tests/test_examination_frontier.py
tests/test_examination_method_applicability.py
tests/test_examination_policy_projection.py
  change fixture construction only if required by narrowing the retained compatibility
  type; do not redesign or recover those excluded districts
```

Before demolition, re-run exact-reference search after edits so imports/strings do not point at deleted modules. Run the mandatory diagnostic inventory/shape tests because registrations are being removed.

### Preserve because independently consumed

```text
seed_runtime/read_model_ownership.py
  generic ReadModelViewRegistration and registration helpers
  nonconstitutional READ_MODEL_VIEW_REGISTRATIONS entries
  construction, dependency identity, cache lookup, and publication machinery

seed_runtime/diagnostic_inventory.py
seed_runtime/diagnostic_shape_audit.py
  generic mechanisms and every unrelated entry/spec

seed_runtime/bounded_constitutional_question.py
  only the minimal examination-consumed construction compatibility and
  bounded_question_id, inquiry_provenance, bounded_question fields (or an equivalent
  no-standing compatibility shape implemented without changing excluded behavior)

scripts/seed_local.py
docs/README.md
shared test modules named above
  all unrelated behavior/content
```

### Preserve as historical testimony only

```text
all existing root and book_of_seed implementation, slice, investigation,
characterization, recovery, readiness, campaign, integration, diagnostic,
operational-documentation, and deletion reports concerning this district,
including constitutional_pipeline_operational_documentation_001.md
```

Their historical status must not be represented as active operator guidance; the sole active linked guide is deleted/corrected above.

### Remaining Unknown

```text
none requiring a follow-up report
```

The exact minimal code shape retained for excluded examination consumers is a demolition implementation choice bounded by their already-observed field reads; it is not an unresolved responsibility and must not grow into replacement architecture.

### Next action

```text
one demolition PR: delete the developer-compiled constitutional-pipeline district
while preserving only independently consumed shared infrastructure and the minimal
existing examination-input compatibility; do not implement a replacement question road
```

## Validation checklist

* Exactly this one report is changed in this recovery.
* All current Python call sites, CLI strings, registrations, diagnostic specs, tests, documentation links, and historical report references were searched.
* Test calls and production calls are counted separately.
* Unused CLI imports after PR 2136 are not counted as consumers.
* Diagnostics, renderers, serializers, registrations, docs, and tests are not treated as independent constitutional responsibility.
* Circular district references are evaluated as one simultaneous deletion set.
* Generic read-model/diagnostic infrastructure is separated from district entries.
* Historical testimony is separated from the one active operator guide/index link.
* Every path proposed for deletion exists now.
* Every retained implementation component above has an exact current consumer; historical reports are retained only as testimony.
* No replacement architecture is proposed.
