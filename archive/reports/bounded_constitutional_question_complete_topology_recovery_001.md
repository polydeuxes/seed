# Complete `BoundedConstitutionalQuestion` topology recovery 001

## Recovery boundary and method

This is one report-only recovery against merged `main` after PR 2136. It changes no
runtime, test, Book, schema, registration, documentation, or persisted shape. The
superseded `constitutional_pipeline_compiled_district_deletion_boundary_001.md` is
deliberately absent: its pipeline-local premise was false.

Repository-wide searches covered the requested symbols, their definitions and call
sites, Python import edges, JSON loaders, CLI dispatch, diagnostic inventory and
shape specifications, question-surface inventory, tests and support fixtures,
operator material, reports, and history. In particular, searches for both
`BoundedConstitutionalQuestion(` and `produce_bounded_constitutional_question(`
separated production from tests. Import searches were repeated per deletion
candidate rather than treating a neighbor's import as independent demand.

Current implementation, not historical intent, controls the findings. History
shows the bounded-question and static pipeline artifacts were introduced together
in the shallow repository's surviving genesis commit `b3e4885`, while later reports
record the raw pipeline ingress removal and PR 2136 removes stale bounded-ask
ingress. The examination files share that surviving genesis in this checkout; this
is chronology testimony, not proof that their standing is lawful.

## Executive finding

`BoundedConstitutionalQuestion` is **not pipeline-local**. It is a shared, mixed,
construction-contaminated root. The static constitutional-pipeline branch consumes
caller-authored coordinates, exact tokens, and developer-authored static views; it
is a developer-compiled constitutional demonstration. Separately, three production
modules type-require the question: `examination_frontier`,
`examination_method_applicability`, and `examination_policy_projection`.

The examination branch is connected in code through request formation, but only
the frontier has a public CLI. Its classifications and later constitutional labels
are substantially supplied as operator/caller testimony. Method applicability
organizes supplied testimony. Policy projection interprets supplied testimony in a
developer-compiled four-kind grammar. Selection mechanically applies that policy,
and probe binding ends at a representation with no executor. Thus parts are live
but contaminated, parts are representation-only, and no stage is established here
as a faithful evidence-derived road.

## Complete dependency graph

```text
non-test construction
  named helper --direct construction, production-reachable API-->
    BoundedConstitutionalQuestion
  examination-frontier JSON loader --JSON reconstruction, CLI-reachable,
    production-reachable--> BoundedConstitutionalQuestion
  direct dataclass constructor --direct construction, production-reachable API-->
    BoundedConstitutionalQuestion

test construction
  test fixtures/helper calls --test-only--> BoundedConstitutionalQuestion
  constitutional_pipeline_test_support direct unpacking --test-only-->
    BoundedConstitutionalQuestion

BoundedConstitutionalQuestion
  --typed call, production-reachable-->
    ConstitutionalQuestionProjection
      --projection--> ConstitutionalCapabilityProjection
      --exact-key projection--> SelectedConstitutionalViews
        --> static ConstitutionalProcessView
        --> static ConstitutionalGovernanceView
        --> static ConstitutionalFidelityView
        --projection--> ConstitutionalViewCompositionRequest
        --projection--> ConstitutionalViewCompositionArtifact
        --> ConstitutionalPipelineResult
          --> provenance explanation / JSON / formatter
          --diagnostic-only--> ConstitutionalPipelineDiagnosticResult
          --refusal-only CLI flags--> --constitutional-pipeline and
                                      --constitutional-pipeline-diagnostic

BoundedConstitutionalQuestion
  --typed call, production-reachable, CLI-reachable through JSON-->
    ExaminationFrontier
      --identity reference/typed call--> ExaminationPolicyProjection
      --typed call--> ExaminationWorkSelection
      --typed call--> ExaminationProbeRequest
  --typed call, production-reachable-->
    ExaminationMethodApplicabilityProjection
      --identity reference/typed call--> ExaminationPolicyProjection
      --method-constraint reference--> ExaminationProbeRequest
  --typed call, production-reachable-->
    ExaminationPolicyProjection
      --projection--> ExaminationPolicySelectorHandoff
      --typed call--> ExaminationWorkSelection
        --projection--> FutureProbeRequestHandoff
        --typed call--> ExaminationProbeRequest
          --> JSON / formatter / tests
          -X- no production executor, result return, diagnostic, or CLI

CandidateExaminationWorkSet (independent explicit corpus/contract JSON model)
  --projection--> compatible CandidateWork rows
  --> ExaminationMethodApplicabilityProjection
  --> ExaminationProbeRequest identity/version/contract binding

historical reports --historical--> chronology/implementation testimony only
```

The raw transition is explicit: an operator-selected JSON file's
`bounded_inquiry` dictionary is unpacked directly into the internal dataclass. No
Seed-owned question-forming occurrence or prior occurrence reference is recovered
at that edge.

## Table 1 — Construction paths

| Producer/path | Source material | Validation | Occurrence evidence | Non-test reachability | Consumers | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| Direct dataclass call | Any Python caller's 15 fields | Python call binding only; dataclass does not validate values | None | Public import/API-reachable; no in-repository non-test call except helper and JSON unpack | All three examination consumers, selection projection, pipeline API | Raw caller-authored construction; mixed representation |
| Named helper | Explicit caller strings/iterables/map; optional caller ID | Stringifies iterable members and caller-field keys/values; sorts caller fields; no type, non-empty, provenance, scope, evidence-demand, authority, or stop validation | None; helper invocation is not recorded | Public API; pipeline request invokes it only when a typed question was not supplied, but current request requires the typed question | Pipeline and any API caller | Normalized caller-authored construction, not responsible question formation |
| Examination-frontier JSON loader | Operator-selected file, `bounded_inquiry` object | Requires object, then dataclass keyword binding; no helper or semantic validation | None; cannot distinguish new origination from reconstruction | `seed --examination-frontier FILE` | `project_examination_frontier` | Raw operator-authored construction; live contaminated ingress |
| Helper-internal constructor | Helper's normalized payload | Same dataclass binding; helper derives ID only when falsey/absent | None | Through helper | Same artifact consumers | Implementation construction detail, not another ingress |
| Test helper calls | Test-authored fields | Helper behavior only | Test occurrence only | No | Unit subjects | Test-only |
| Pipeline test-support unpack | Defaults plus test overrides | Dataclass keyword binding | Test occurrence only | No | Pipeline tests | Test-only direct construction |

There are **three public/non-test ways** to obtain the object at API resolution
(direct constructor, helper, JSON loader), but only **two in-repository non-test
constructor call sites** (helper internals and JSON unpack). Only the JSON loader is
currently operator-CLI reachable. The helper can derive a stable SHA-256 ID or
accept a caller ID. Direct construction and JSON unpack require and therefore
permit caller-supplied IDs. No path validates constitutional provenance, bounded
scope, evidence demand, authority, lawful stop, or a production occurrence.
Only the loader bypasses the named helper in non-test repository code. Consumers
cannot distinguish helper, direct, and JSON construction because no producer or
occurrence coordinate is carried. The three direct consumers check only
`isinstance`; downstream consumers compare copied identity references and artifact
relationships, not construction standing.

## Table 5 — Artifact field ownership

| Field | Source | Validation | Consumers | Independent standing | Likely owner/disposition |
| --- | --- | --- | --- | --- | --- |
| `bounded_question_id` | Caller, or helper hash of all caller fields | Required only by raw dataclass binding; no non-empty check | All three examination projectors; frontier/policy identity joins; static projection/selection/pipeline | Derived implementation identity when helper-derived; otherwise caller testimony; consumer-required reference | Preserve pending examination-road recovery; mixed |
| `operator_inquiry` | Caller | None; helper preserves value | Question projection, pipeline output/rendering only | Attributed external testimony | Pipeline-local consumption; raw testimony coordinate on artifact |
| `inquiry_provenance` | Caller | None | Frontier and method references; question projection/rendering | Claimed provenance, not validated provenance | Examination dependency and raw testimony coordinate |
| `bounded_question` | Caller | None | Frontier/method references; question projection, selection-key extraction indirectly through caller fields | Caller-authored constitutional characterization, not Seed-formed question | Preserve; mixed/contaminated |
| `constitutional_intent` | Caller | None | Static question projection and rendering | Caller-authored constitutional characterization | Pipeline-only consumption; field remains on shared artifact pending recovery |
| `scope_status` | Caller | None | Static projection/rendering; not examination frontier classification | Caller-authored constitutional characterization | Pipeline-only consumption; raw testimony coordinate |
| `uncertainty` | Caller iterable, helper stringifies elements | Container/element types not checked by dataclass; helper stringifies | Static question projection/selection and rendering | Attributed testimony/Unknown | Pipeline-only consumption currently |
| `unknowns` | Caller iterable, helper stringifies elements | As above | Static question projection/selection and rendering | Attributed external testimony, not typed Unknown establishment | Pipeline-only consumption currently |
| `caller_supplied_fields` | Caller map or tuple | Helper stringifies and sorts; direct path accepts any runtime value | Exact token extraction in static view selection; rendering | Implementation routing coordinate and pipeline-only contamination | Pipeline-local deletion of consumer; no independent consumer afterward |
| `testimony_status` | Dataclass default or raw caller override | None | Rendering/serialization; no examination decision | Negative-authority declaration | No independent decision consumer |
| `read_only_boundaries` | Developer default or raw override | None | Static projection/selection/composition and rendering | Negative-authority declaration; raw loader can replace it | Mixed / Unknown |
| `read_only` | Developer default or raw override | None | Static projection/selection and renderers | Representation flag, not occurrence proof | Mixed / Unknown |
| `writes_event_ledger` | Developer default or raw override | None | Static projection/selection and renderers | Negative operational declaration, not independently verified by constructor | Mixed / Unknown |
| `mutates_cluster` | Developer default or raw override | None | Static projection/selection and renderers | Negative operational declaration, not authority | Mixed / Unknown |

The artifact is not one coherent established constitutional subject. It combines
external testimony, caller-authored constitutional characterization, optionally
derived implementation identity, routing coordinates, and developer default
negative declarations. Across consumers it is best described as a **shared mixed
external-input envelope and implementation routing request with a contaminated
question-shaped root**. Fields may have different standing; no global promotion is
warranted.

## Table 2 — Complete production consumer inventory

| Consumer | Branch | Fields consumed | Standing required | Standing actually checked | Downstream consumer | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `project_constitutional_question` | Static | All question coordinates and flags | Already-established bounded question | `isinstance` only | capability projection, selection, pipeline result | Developer-compiled demonstration |
| `_selection_keys_from_bounded_question` | Static | `caller_supplied_fields` keys/values | Lawful selection coordinates | Exact values whose keys end in `selection_key`; no warrant | static selector | Pipeline-only contamination |
| `invoke_constitutional_pipeline` | Static | Whole artifact, projected fields | Established ingress | Request type and artifact type; no occurrence | result/explanation/diagnostic | Developer-compiled demonstration |
| `project_examination_frontier` | Examination | `bounded_question_id`, `inquiry_provenance`, `bounded_question` | Bounded inquiry identity/reference | `isinstance`; no formation/provenance standing | policy, selection, probe identity joins, CLI rendering | Live but contaminated |
| `project_examination_method_applicability` | Examination | same three fields | Bounded inquiry to which methodology applies | `isinstance`, exact ID matching and candidate/version matches | policy and probe request | Live testimony organizer; contaminated |
| `project_examination_policy` | Examination | `bounded_question_id` | Inquiry identity for resolution policy | `isinstance`, exact references; no question standing | selector handoff/work selection | Live but contaminated policy organizer |
| JSON/format renderers | Both | Serialized/copied fields | Representation only | Type assumptions | Operator/test output | Read-only projection surface |

No other production module imports the class or helper. Work selection and probe
request do not receive the root object; they consume identity-bearing projections.
That is indirect dependence, not a further direct artifact consumer.

## Branch A — static constitutional-pipeline branch

The current chain is implemented inside `constitutional_pipeline.py`,
`constitutional_view_selection.py`, `constitutional_view_composition.py`, and the
three static view modules. The prompt's separately named question- and
capability-projection files do not exist: both projection classes/functions live
in `constitutional_view_selection.py`.

The question projection copies caller-authored coordinates and flags; it consults
no State, Evidence, current repository observation, or Book material. Capability
projection consumes supplied `ConstitutionalCapabilitySource` records and uses
developer-known registration keys. Selection extracts exact tokens, including
caller fields named with `selection_key`; it does no semantic interpretation.
Process, Governance, and Fidelity builders return static developer-authored rows.
Composition packages selected static views. Pipeline result, provenance
explanation, diagnostic, JSON, and human rendering expose that package without a
constitutional effect outside the branch.

Therefore this branch meets the exact definition of **developer-compiled
constitutional demonstration**: developer categories, caller labels, no current
evidence or active Book examination, static summaries/routing, and no independent
constitutional effect. Internal dependency does not preserve an item.

## ExaminationFrontier input road

The only examination CLI flag is `--examination-frontier JSON_FILE`. The CLI reads
the operator-selected path with `Path(...).read_text()`, parses JSON, invokes
`input_from_json_dict`, projects, and prints JSON or text. Expected top-level keys
are:

* required `bounded_inquiry` object containing every non-default dataclass field:
  ID, operator inquiry, provenance, bounded question, intent, scope, uncertainty,
  and unknowns; defaulted artifact fields may be omitted;
* required `corpus` object with non-empty `corpus_id`, optional label/unknowns, and
  member list;
* optional `candidate_work` list.

Member identity, substrate kind, and artifact identity are non-empty strings.
Candidate ID/member/work kind are non-empty. Many optional values (`artifact_hash`,
material reference, scope, capability, convention, compatibility,
authorization, and supplied status) are merely `str(...)`-coerced. Tuple-like
testimony/reference fields require string lists/tuples. `BoundedConstitutionalQuestion(**qd)`
is directly reachable and does not call the helper. It may be either reconstruction
or origination; the implementation cannot tell. No occurrence or prior producer
reference is required.

The frontier consumes only question ID, alleged provenance, and alleged bounded
question text. A smaller inquiry-reference artifact could satisfy the mechanical
consumer. It does not need or verify the whole internal question. Work eligibility
is derived mechanically from supplied labels: `compatible`; authorization equal
to `authorized` or `not_applicable`; no matching completed result; and absence of
blockers, deferral testimony, unsupported status, and Unknowns. `supplied_status`
only triggers a conflict when `eligible` contradicts the other labels.
`capability_id` is required only after supplied compatibility says compatible.
Existing results count examined only when an exact tuple matches and
`result_state == completed`; blockers, deferrals, and failure references directly
produce the corresponding classifications. This is organized supplied testimony,
not evidence-derived constitutional eligibility.

## Table 3 — Examination-road stages

| Stage | Caller-supplied inputs | Derived outputs | Evidence consulted | Constitutional act claimed | Actual standing | Consumer |
| --- | --- | --- | --- | --- | --- | --- |
| Candidate work | Corpus members, representations, contracts, availability, applicability member IDs | Compatibility observation and stable candidate identities | Supplied visibility/contract testimony only | Candidate visibility | Mechanical candidates; availability is not applicability | applicability/frontier/probe binding |
| Frontier | Raw bounded inquiry, corpus, work labels, results/blockers/deferrals/failures | status booleans, counts, stable work/frontier IDs | No Evidence graph or State; supplied labels only | Eligibility/frontier classification | Live but contaminated testimony classification | policy, selection, CLI |
| Method applicability | Raw question, candidate set, applicability testimony | matched records, constraint unions, applicable/inapplicable/unknown/conflict sets | Supplied testimony/reference strings only | Method applicability | Testimony organizer, not evidence-derived applicability | policy, probe request |
| Policy | Raw question, frontier, applicability, resolution testimony | policy state/sufficiency/scope/exclusions/prerequisite rendering | Supplied testimony plus upstream supplied classifications | Resolution/selection policy | Developer-grammar organizer over contaminated inputs | work selection |
| Selection | Frontier, policy projection and exact handoff | zero/one selected ID, reasons, future handoff | No new evidence | Select examination work | Mechanical local selection; no authorization | probe binder |
| Probe request | Selection/handoff/frontier/work set/applicability | bound request and requested-outcome string | Identity/version/contract checks; no executor evidence | Request formation | Representation-only bound request | JSON/formatter/tests only |

### Method applicability answers

`ExaminationMethodApplicabilityTestimony` is constructed directly by callers/tests;
it has a JSON factory but no production JSON loader or CLI adapter uses that factory.
Applicability is supplied as one of four developer-defined states, not calculated
from evidence. A testimony targets an exact candidate ID or contract ID, and is
relevant only after exact inquiry, optional artifact identity, and optional version
matches. Exact ID matching establishes association, not methodological
applicability. Absence yields `unknown` plus `methodology_evidence_absent`.
Different non-Unknown labels, different constraint bundles, or contradicting
references yield conflict. Fidelity, attribution, claim-treatment constraints,
method references, supports, contradictions, and Unknowns are supplied; the
projection unions/sorts and classifies them.

`applicable_candidate_references` is treated as authoritative locally by policy's
eligible intersection, the adapter to frontier candidate work, and probe binding's
required applicable record. No Evidence graph or projected State participates.
This is a **supplied-applicability testimony organizer**, not faithful applicability
examination.

### Examination policy answers

Every resolution coordinate—`policy_kind`, `policy_parameters`, tie treatment,
candidate scope, prerequisite relations, no-selection conditions, continuation,
resource constraints, and supports—is supplied by
`ExaminationResolutionTestimony`. The projection validates references, conflicts,
and the four developer-compiled kinds (`explicit_work_identity`,
`all_eligible_no_order`, `prerequisite_first`, `no_selection`), then mechanically
computes scope and whether exactly one item remains.

`policy_sufficiency` means only sufficient for this selector to choose one work
identity. The downstream selector treats it as that generic uniqueness gate. The
projection neither selects nor authorizes work; it reshapes testimony into the
handoff consumed by `select_examination_work`. No projected evidence chooses a
policy. “Applicable,” “eligible,” and “sufficient” therefore have only local
implementation purposes, not stronger constitutional standing.

### Work selection and probe request answers

Selection chooses among frontier candidates derived from supplied compatibility,
authorization, and applicability testimony. It consumes caller-supplied policy,
and positive selection requires a sufficient applicable policy and exactly one
permitted candidate (or one explicit named eligible candidate). The candidate's
standing is only the upstream mechanical/supplied standing. Selection creates a
`FutureProbeRequestHandoff`; it does not authorize or execute.

Probe binding checks matching question/frontier/policy/selection/work-set,
candidate, artifact version, contract, capability, and applicable-method records.
It identifies a contract/capability string but explicitly contains no registered
operation, provider, tool, or arguments. Repository-wide consumers are its JSON
serializer, formatter, and tests. There is no executor, CLI, diagnostic, result
return, frontier update, or production performance. The chain stops at another
representation artifact and is not operational end to end.

## Public and diagnostic reachability

| Surface | Input | Produced artifact | Positive behavior | Refusal behavior | Next consumer | End-to-end result |
| --- | --- | --- | --- | --- | --- | --- |
| `--examination-frontier` | Operator JSON file | `ExaminationFrontier` | Prints projection | Loader/projection errors | None outside output | Read-only projection; live contaminated ingress |
| applicability API | Typed objects/testimony | applicability projection | Organizes supplied labels | Rejects invalid states/refs | policy/probe | Production-callable, no CLI |
| policy API | Typed projections/testimony | policy projection/handoff | Applies compiled grammar | Unknown/conflict/no selection | selector | Production-callable, no CLI |
| selection API | frontier/policy/handoff | selection/future handoff | Selects at most one | no-selection/unknown/conflict | probe binder | Production-callable, no CLI |
| probe API | five typed artifacts | probe request | Binds representation | rejects crossing mismatch/non-applicable method | None | Representation-only scaffold |
| `--constitutional-pipeline` | Raw legacy flags | none | None | always parser error | None | Refusal-only compatibility residue |
| `--constitutional-pipeline-diagnostic` | Raw legacy flags | none | None | always parser error | None | Refusal-only compatibility residue |
| typed pipeline API | established-object claim | pipeline result | static composition | typed/input invariant failures | renderer/diagnostic | Developer demonstration |
| pipeline diagnostic API | result/request | stage diagnostics | visibility only | typed/input failures | JSON/text | Developer diagnostic |
| diagnostic inventory/shape audit | registry/source inspection | inventory/audit rows | exposes frontier and two pipeline flags | reports shape mismatch | operator | Diagnostic visibility, not execution |
| question-surface inventory | static registry | family rows | exposes implementation family metadata | unknown family refusal | bounded ask dispatch | Does not form a question |
| active pipeline operator guide | prose/API examples | none | describes typed API/static output | documents CLI refusal | developer | Active documentation for demonstration |

There are no applicability, policy, selection, or probe CLI flags or diagnostic
inventory entries. Their tests prove constructors and validators, not operational
reachability. The examination frontier and pipeline entries are checked in both
diagnostic inventory and shape audit; this is visibility only.

## Table 4 — Static-pipeline deletion manifest

| Component/path | Independent consumer | Examination dependency | Shared infrastructure | Deletion effect | Disposition |
| --- | --- | --- | --- | --- | --- |
| `seed_runtime/constitutional_pipeline.py` | CLI refusal import wiring, diagnostic, tests | None | Uses shared serialization/read-model contracts | Removes static result/provenance API only | Delete next |
| `seed_runtime/constitutional_pipeline_diagnostic.py` | Pipeline CLI wiring/tests only | None | Serialization only | Removes pipeline diagnostic | Delete next |
| question and capability projections in `constitutional_view_selection.py` | Pipeline/tests only | None | None independently | Removes static copies/routing | Delete next with whole module |
| selection/composition adapter in `constitutional_view_selection.py` | Pipeline/tests only | None | Static view builders | Removes exact-token routing | Delete next |
| `seed_runtime/constitutional_view_composition.py` | Direct CLI view-composition surface/tests also exist | None | Read-model contracts | Affects a separately exposed static composition surface; include only with its CLI/registry/doc/test consumers | Delete next as demonstration district, after exact companion edits |
| three static view modules | Direct CLI flags, read-model ownership registrations, tests | None | Registration table references them | Removes static developer-authored views and registered contracts | Delete next with all registrations/surfaces/tests |
| pipeline provenance explanation/renderers/serializers | Pipeline neighbors only | None | Generic serializer remains | Removes pipeline-only presentation | Delete next |
| pipeline diagnostic inventory/shape specs | Registry entries only | None | General registries remain | Removes stale visibility rows | Delete next |
| refusal-only pipeline CLI flags and raw argument flags | Parser/tests/docs | None | General CLI remains | Removes compatibility residue | Delete next |
| `constitutional_pipeline_operations.md` and pipeline-only implementation reports/tests/fixtures | Human/test consumers only | None | None | Removes active guide and branch testimony/tests as selected by cleanup scope | Delete next; enumerate exact searched set in deletion PR |
| `seed_runtime/bounded_constitutional_question.py` | Three examination modules plus tests | Root of examination road | Serialization helper only | Breaks examination type checks and JSON loader | **Preserve** |
| examination modules/tests/frontier CLI/diagnostics | Live branch | Direct/indirect root dependence | Their own chain | Breaks separate branch | **Preserve** |
| general `read_model_ownership.py` | Many unrelated registrations | None from examination | Shared facility | Whole-file deletion breaks unrelated roads | Preserve file; remove only static registrations later |

No examination module imports any static-pipeline module. No unrelated production
module imports pipeline or selection. The three static view modules do have direct
CLI and read-model-registration consumers, but those consumers are members of the
same developer-compiled static district, not independent constitutional demand.
Deleting the bounded-question class is not part of this manifest. A deletion PR
must use repository-wide searches to enumerate exact tests/reports/docs and edit
shared files surgically; this report does not delete or silently pre-authorize an
unchecked wildcard list.

## Constitutional authority table

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
| --- | --- | --- | --- |
| External question material is not an internal question; formation remains Seed-owned | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, paragraphs 1–3 and negative equations | JSON/helper caller fields cannot establish internal formation | Does not prove no artifact exists |
| Constructor is not responsible production | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, first substantive paragraph | Shape and field names do not supply warrant/standing | Does not forbid representations |
| Missing formation occurrence stays Unknown | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, candidate production-standing paragraph | Consumer transport cannot relocate production | Does not infer a known producer is absent |
| Projection cannot strengthen source standing | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, opening and lossless-projection paragraphs | Static and examination projections retain source limits | Does not prohibit bounded projection |
| Testimony is not established fact/applicability | `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md`, support paragraph; `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`, opening clauses | Supplied positive labels need claim-relative warrant | Does not make testimony false |
| Availability, applicability, uptake, and standing differ | `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`, availability paragraph | Candidate availability does not establish applicability | Does not impose one universal stage order |
| Applicability is not selection; request is not execution | `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`, opening and negative equations | Examination-stage separations | Does not deny local responsible occurrences could exist |
| Selection/request does not grant authorization | `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`, authorization paragraph | No authority follows from these artifacts by identity | Does not decide an external authority not represented here |
| Representation formation is not invocation/performance | `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, request-formation paragraph | Probe object does not prove execution | Does not prove execution impossible elsewhere |
| Implementation labels/topology are not constitutional taxonomy/topology | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, taxonomy paragraph; `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`, uptake paragraph | Class names/import adjacency prove only implementation topology | Does not erase demonstrated typed edges |

Tests, reports, class names, docstrings, and PR history were not used as Book
authority.

## Precise classification and direct verdicts

1. **Pipeline-local?** No; it is a shared mixed root.
2. **Non-pipeline production consumers?** `examination_frontier.py`,
   `examination_method_applicability.py`, and `examination_policy_projection.py`.
3. **Non-test construction paths?** Direct public dataclass construction, helper
   construction, and examination-frontier JSON unpacking; two repository call sites.
4. **Operator-reachable construction?** The frontier JSON loader directly; public
   Python callers can also supply either constructor/helper inputs.
5. **Responsible helper formation?** Not established. It normalizes caller fields
   and optionally derives identity.
6. **Responsible loader formation?** No evidence; it raw-unpacks caller material.
7. **Can consumers distinguish paths?** No.
8. **Occurrence evidence carried?** No producer identity or occurrence coordinate.
9. **Does frontier need whole artifact?** No, mechanically.
10. **Frontier fields consumed?** ID, provenance string, bounded-question string.
11. **Eligibility basis?** Supplied statuses/testimony, mechanically combined; not
    preserved Evidence/State.
12. **Method applicability?** Organizes supplied applicability testimony.
13. **Policy?** Organizes supplied resolution testimony through compiled grammar.
14. **Real execution consumer after selection?** No; only probe-request binder.
15. **Probe request leads to execution?** No recovered path.
16. **Examination end-to-end operational?** No. Frontier CLI is live; typed middle
    stages connect; the chain stops before execution/result return.
17. **Live but contaminated stages?** JSON ingress, frontier, applicability, policy,
    and selection insofar as production-callable consumers use injected standing.
18. **Faithful stages?** None established. Mechanical identity/version validation is
    faithful only to representation consistency, not constitutional standing.
19. **Unknown?** Whether any out-of-repository API caller supplies responsibly
    produced questions/testimony; whether a responsible producer or executor exists
    beyond repository evidence; whether a smaller inquiry reference is intended.
20. **Static pipeline classification?** Developer-compiled demonstration.
21. **Static components with consumers outside pipeline?** The three views and
    composition have direct static CLI/read-model surfaces, all in the same static
    demonstration district; none is consumed by examination.
22. **Can static branch be deleted independently?** Yes, with all its own CLI,
    registrations, docs, tests, and shared-file rows removed surgically.
23. **Next deletion files?** The eight static runtime modules listed in Table 4
    (not nonexistent split projection modules), pipeline-only tests/support,
    pipeline/static-view CLI dispatch and flags, diagnostic rows/specs,
    read-model registrations, active pipeline operator guide, and pipeline-only
    reports selected by an exact consumer search.
24. **Explicit exclusions?** Bounded-question module/class/helper and tests needed by
    examination; every examination module/test; frontier CLI/diagnostics; general
    serialization, diagnostic, shape-audit, question-surface, and read-model files
    except exact static rows.
25. **Contamination after deletion?** Raw JSON question origination; absent producer
    occurrence; oversized root reference; caller-supplied compatibility,
    authorization, applicability, and policy standing; no executor/result return.
26. **Another broad report before deletion?** No. This repository-wide recovery is
    sufficient; the deletion PR still must perform exact local consumer checks.
27. **Single next lawful action?** Delete only the independently bounded static
    constitutional demonstration district, preserving the shared question and
    examination road.

## Remaining uncertainty discipline

No live consumer proves lawful standing. Typed requirements prove shape checks;
exact identity checks prove relation consistency only. The report does not decide
that externally supplied testimony is false, that no responsible occurrence exists
outside repository visibility, or that the examination design is globally fake.
It classifies only recovered stages and preserves stronger claims as Unknown.

delete next:
    the independently bounded static constitutional-pipeline demonstration district, including its eight runtime modules, exact CLI and registry rows, active operator guide, and pipeline-only tests and reports

preserve from that deletion:
    BoundedConstitutionalQuestion, its helper and examination-required tests, the complete examination branch, the examination-frontier CLI and diagnostics, and shared infrastructure except exact static registrations

recover afterward:
    the examination road's raw JSON origination, producer-occurrence standing, minimal inquiry-reference need, supplied eligibility/applicability/policy authority, and missing execution/result-return boundary

remaining Unknown:
    any responsible out-of-repository producer or consumer occurrence, any lawful external authority behind supplied testimony, any intended smaller inquiry reference, and any executor beyond current repository evidence

single next lawful action:
    delete only the independently bounded static constitutional-pipeline demonstration district while preserving the shared bounded question and examination road
