# Examination topology and standing recovery 001

## 1. Recovery boundary and verdict

This is one bounded, report-only recovery against merged `main` after PRs 2138 and
2139. It changes no implementation, test, Book clause, registration, schema,
persisted representation, existing report, or malformed-input behavior. The
recovery used repository-wide import, symbol, constructor, factory, CLI, diagnostic,
test, documentation, and history searches. Definitions are not counted as callers;
tests are not counted as production invocation; formatters and serializers are not
counted as constitutional consumers.

There is **not one coherent current examination road**. There are three adjacent
districts:

1. **District A is live but contaminated.** `--examination-frontier JSON_FILE`
   reconstructs a `BoundedConstitutionalQuestion` directly from caller JSON,
   reconstructs a separate corpus and candidate-work vocabulary, mechanically
   classifies supplied labels and references, and ends in JSON or human rendering.
   It is an operator-facing, read-only status-classification inventory. It neither
   discovers work nor establishes applicability, authorization, readiness, or a
   Seed-owned internal question.
2. **District B is production-callable but assembled only by tests in this
   repository.** Candidate projection matches caller-declared representations to
   caller-declared contracts; applicability organizes caller testimony; policy
   applies a developer-enumerated grammar to caller resolution testimony; selection
   mechanically filters classifications under that projected policy. No CLI,
   runtime orchestration, or independent non-test caller enters these stages.
3. **District C terminates at representation.** A test-built selection can be bound
   to `ExaminationProbeRequest` by exact identity checks and copied constraints.
   There is no recovered registered probe competency, executor, dispatcher, event,
   invocation, consumer, result artifact, or result-return road.

Thus the only operator-facing road ends at `ExaminationFrontier` rendering. Tests
manually continue across adjacent types, but production does not.

## 2. Method and complete reachability graph

### 2.1 Legend

```text
[O] operator-reachable edge       [I] production-invoked edge
[C] production-callable edge      [T] test-only edge
[D] diagnostic inventory/audit    [S] serializer/formatter edge
[H] historical planned edge       [X] no recovered consumer
```

### 2.2 Current graph

```text
external JSON file
  [O,I] Path.read_text -> json.loads
  [O,I] examination_frontier.input_from_json_dict
      |-- raw **bounded_inquiry (supplied constitutional labels enter here)
      |     -> BoundedConstitutionalQuestion (no value/formation validation)
      |-- corpus.members -> CorpusMember (caller inventory)
      `-- candidate_work -> CandidateWork
            (compatibility, authorization, status, results, blockers,
             deferrals and failures enter as caller testimony)
  [O,I] project_examination_frontier
      |-- consults no Evidence graph, State, repository corpus, registry or probe
      |-- exact completed-result tuple matching occurs here
      `-- ExaminationFrontier
            [S,O,I] examination_frontier_json -> CLI JSON -> terminal END
            [S,O,I] format_examination_frontier -> terminal END
            [D] inventory declaration + static shape audit (visibility, not calling)
            [T] manually passed into policy/selection/probe tests

direct Python / JSON-factory candidate district
  [C; T in repository] BoundedCorpusMember + RepresentationVisibility
        + ExaminationWorkContract
      -> project_candidate_examination_work
      -> CandidateExaminationWorkSet
         [S,T] JSON/formatter END
         [C,T] to_frontier_candidate_work -> CandidateWork
         [C,T] consumed by applicability and probe binder

direct Python testimony district
  [C; T in repository] BoundedConstitutionalQuestion
      + CandidateExaminationWorkSet
      + ExaminationMethodApplicabilityTestimony
      -> project_examination_method_applicability
      -> ExaminationMethodApplicabilityProjection
         [S,T] JSON/formatter END
         [C,T] to_frontier_candidate_work -> CandidateWork
         [C,T] policy projection / probe binder

  [T manual continuation] question + applicability + frontier
      + ExaminationResolutionTestimony (policy labels enter here)
      -> project_examination_policy
      -> ExaminationPolicyProjection
      -> to_selector_handoff
      [T] select_examination_work
      -> ExaminationWorkSelection (zero/one identity)
      -> FutureProbeRequestHandoff only when one is selected
      [T] bind_examination_probe_request
      -> ExaminationProbeRequest
         [S,T] JSON/formatter
         [X] no executor, dispatcher, emission, receiver, result, or return

[H] slice reports anticipated a selector/probe consumer; current code does not
    realize those planned edges.
```

Direct constructors, the candidate JSON factory, and all public projectors remain
importable production APIs, hence callable. Repository-wide searches found no
non-test call to candidate projection, applicability, policy, selection, or request
binding. `read_model_ownership.py` and `question_surface_inventory.py` contain no
examination registration or caller. Only the frontier appears in diagnostic
inventory/shape metadata; those diagnostics inspect declarations and static shape
and do not build a frontier.

## 3. Table 1 — Artifact reachability

| Artifact/function | Active producer | Active consumer | CLI reachable | Runtime invoked | Test only | End condition |
| --- | --- | --- | --- | --- | --- | --- |
| `BoundedConstitutionalQuestion` | Frontier JSON unpack; public helper/direct constructor; tests | Frontier reads 3 fields; applicability/policy read ID; tests/formatters | Yes, through raw frontier JSON | Yes, raw construction in frontier CLI | No | Mixed shared root/reference envelope |
| `input_from_json_dict` (frontier) | CLI; tests | CLI passes tuple to projector | Yes | Yes | No | Projector or parse failure |
| `CorpusMember`, `CandidateWork`, `WorkResultReference` | Frontier JSON/direct constructors | Frontier projector | Yes | Yes | No | Embedded in frontier/rendering |
| `project_examination_frontier` | CLI and tests/direct calls | Renderer/serializer; policy/selection only in tests | Yes | Yes | No | Operator road ends at rendering |
| `ExaminationFrontier` / item / classification | Frontier projector | CLI rendering; later test-built stages | Yes | Yes | No | No production constitutional consumer |
| Candidate JSON `input_from_json_dict` | Public API/tests | Candidate projector only when caller wires it | No | No | In-repository yes | Returns typed inputs, not work set |
| `project_candidate_examination_work` | Direct API/tests | Adapters/applicability/probe only in tests | No | No | In-repository yes | Callable work-set representation |
| `CandidateExaminationWorkSet` | Candidate projector/tests | Applicability, frontier adapter, probe binder in tests | No | No | In-repository yes | Serializer/formatter or manual chain |
| `ExaminationMethodApplicabilityTestimony` | Direct callers/tests | Applicability projector | No | No | In-repository yes | Supplied testimony |
| `project_examination_method_applicability` | Direct API/tests | Policy/probe and adapter in tests | No | No | In-repository yes | Test-supported organizer |
| `ExaminationMethodApplicabilityProjection` | Applicability projector | Policy/probe in tests; serializers | No | No | In-repository yes | No independent runtime demand |
| `ExaminationResolutionTestimony` | Direct callers/tests | Policy projector | No | No | In-repository yes | Supplied policy testimony |
| `project_examination_policy` | Direct API/tests | Selection through handoff in tests | No | No | In-repository yes | Developer-compiled organizer |
| `ExaminationPolicyProjection` / selector handoff | Policy projector | Selection in tests; serializers | No | No | In-repository yes | No independent consumer |
| `select_examination_work` | Direct API/tests | Probe binder in tests | No | No | In-repository yes | Zero/one identity + optional handoff |
| `ExaminationWorkSelection` | Selector | Probe binder in tests; serializers | No | No | In-repository yes | Mechanical filter result |
| `bind_examination_probe_request` | Direct API/tests | Serializer/formatter/tests | No | No | In-repository yes | Representation-only endpoint |
| `ExaminationProbeRequest` | Binder in tests | Serializer/formatter/tests | No | No | Yes in practice | No operational consumer |
| Frontier inventory/shape specs | Static registries | Inventory/audit CLI and tests inspect metadata | Diagnostic CLI only | Metadata is invoked; frontier is not | No | Visibility result only |

“Test only” here means in-repository practice, not that Python import is technically
restricted. The later functions are production-callable but have no recovered
production invocation.

## 4. Bounded-question examination use

| Consumer | Fields read | Why required | Standing assumed | Standing validated | Could a narrower reference satisfy it? |
| --- | --- | --- | --- | --- | --- |
| Frontier | `bounded_question_id`, `inquiry_provenance`, `bounded_question` | Stable frontier ID and displayed/copied inquiry reference | That the object is the bounded inquiry for this corpus/work | Only `isinstance`; no producer, occurrence, content, scope, or provenance validation | Yes: the exact three-field reference currently consumed |
| Applicability | `bounded_question_id` | Match testimony inquiry and form IDs/reference | That identity addresses the governing inquiry | Type check and string equality only | Yes: question identity |
| Policy | `bounded_question_id` | Match resolution testimony and copy identity | Same | Type check and string equality only | Yes: question identity |
| Selection/probe (indirect) | Copied `bounded_question_id` references | Cross-artifact identity consistency | That equal IDs share lawful question standing | Equality only | Yes: identity reference |

No examination stage consumes `operator_inquiry`, `constitutional_intent`,
`scope_status`, `uncertainty`, `unknowns`, or `caller_supplied_fields`. No stage
verifies how the artifact was produced or distinguishes helper construction from
raw JSON/dataclass construction. No stage needs the complete artifact. The object
is therefore a **mixed root**: complete question-shaped fields exist, while current
examination use is only an identity/reference envelope plus two display/provenance
strings. It does not function as a validated Seed-owned internal question.

## 5. JSON ingress and malformed-input boundary

### 5.1 Accepted current shape

The frontier loader expects a top-level mapping with:

```text
bounded_inquiry: kwargs accepted by BoundedConstitutionalQuestion
  required: bounded_question_id, operator_inquiry, inquiry_provenance,
            bounded_question, constitutional_intent, scope_status,
            uncertainty, unknowns
  optional/overrideable: caller_supplied_fields, testimony_status,
            read_only_boundaries, read_only, writes_event_ledger, mutates_cluster
corpus:
  corpus_id (required non-empty string), corpus_label (optional), unknowns (string list)
  members[]: member_id, substrate_kind, artifact_identity (required non-empty);
    optional artifact_hash, material_reference, scope_status, provenance,
    authorization_testimony, unknowns
candidate_work[]:
  candidate_work_id, corpus_member_id, work_kind (required non-empty);
  optional capability_id, convention, compatibility_status, authorization_status,
  existing_results[], blockers[], deferral_testimony[], failure_references[],
  supplied_status, provenance, unknowns
existing_results[]:
  result_id, corpus_member_id, work_kind, result_state (required non-empty);
  optional artifact_hash, capability_id, convention, provenance
```

The separate candidate-work factory expects `corpus.corpus_id`, `corpus.members[]`
as `BoundedCorpusMember` (including nested `representations[]`), and top-level
`contracts[]`; it ignores `candidate_work_names` after checking only that it is a
list/tuple. It is not used by the frontier CLI. Consequently the operator road does
**not** construct `CandidateExaminationWorkSet`; it constructs frontier
`CandidateWork` directly.

### 5.2 Table 4 — Malformed-input behavior

The following was observed by calling the current loader then projector. “Artifact”
means a final frontier; intermediate objects can exist before projector failures.

| Input case | Current behavior | Exception/result owner | Artifact obtained | Domain boundary quality |
| --- | --- | --- | --- | --- |
| Missing `bounded_inquiry` | `ExaminationFrontierError: bounded_inquiry is required` | Frontier loader | No | Domain-local |
| `bounded_inquiry` not object | Same | Frontier loader | No | Domain-local but conflates defect |
| Missing required question field | raw dataclass `TypeError` missing argument | Python constructor | No | Leaked implementation error (CLI happens to catch it) |
| Extra question field | raw dataclass `TypeError` unexpected keyword | Python constructor | No | Leaked implementation error (CLI catches) |
| Empty question identity | Frontier succeeds with empty copied ID | No rejection | Yes | Unguarded external crossing |
| Empty inquiry provenance | Frontier succeeds | No rejection | Yes | Unguarded |
| Empty question text | Frontier succeeds | No rejection | Yes | Unguarded |
| Wrong uncertainty type | Frontier succeeds because field is unread | No rejection | Yes | Unguarded |
| Wrong unknowns type | Frontier succeeds because field is unread | No rejection | Yes | Unguarded |
| Override `read_only=false` | Question is constructed; frontier remains independently read-only | Raw dataclass accepts | Yes | Caller can falsify question declaration |
| Override `writes_event_ledger=true` | Same | Raw dataclass accepts | Yes | Caller-authored operational declaration |
| Override `mutates_cluster=true` | Same | Raw dataclass accepts | Yes | Caller-authored operational declaration |
| Malformed corpus (not object) | `ExaminationFrontierError: corpus is required` | Frontier loader | No | Domain-local but conflates defect |
| Missing corpus ID | `ExaminationFrontierError: corpus_id is required` | Frontier loader | No | Domain-local |
| Unknown corpus member referenced by work | `ExaminationFrontierError: unknown_corpus_member` | Projector | No final frontier | Domain-local |
| Duplicate corpus member | `duplicate_corpus_member_id` | Projector | No final frontier | Domain-local |
| Duplicate candidate ID | `duplicate_candidate_work_id` | Projector | No final frontier | Domain-local |
| Malformed candidate member (`null`) | raw `AttributeError` from `.get` | Python implementation | No | Leaked and not caught by CLI's exception tuple |
| Candidate missing required identity | domain `candidate_work_id is required` | Candidate factory | No | Domain-local |
| Existing result tuple mismatches candidate/member/version | `existing_result_work_mismatch` | Projector | No final frontier | Domain-local identity validation |

Therefore malformed JSON behavior is **not domain-bounded**. Raw `TypeError` and
`AttributeError` are accidental implementation leakage and should not be frozen in
tests. This representation defect is separate from a well-formed but caller-authored
question characterization: schema repair alone cannot establish Seed-owned question
origination.

## 6. Candidate examination work

The candidate projector receives corpus members, their representation visibility,
and work contracts directly from callers. `work_kind`, `capability_id`, accepted and
produced representations, convention, availability, applicable member IDs, and
provenance all come from those contracts. It derives stable candidate/work-set IDs,
matches representation kind exactly, chooses the first matching representation,
and emits developer-enumerated observations: `compatible`,
`missing_required_representation`, `capability_unavailable`, `contract_unknown`, or
`representation_unknown`. It derives missing prerequisites from absence of a match.
It does not inspect artifact content, evidence, a capability registry, or an
execution occurrence.

The adapter weakens its richer observation to frontier compatibility `compatible`
or `unknown`, always supplies frontier authorization `unknown`, and carries no
results, blockers, deferrals, failures, or supplied eligible status. Conversely,
the CLI frontier accepts those latter fields directly from JSON. A result reference
proves only that a caller supplied a tuple; the frontier marks `examined` only when
that tuple exactly matches member ID, artifact hash, work kind, capability ID, and
convention and its supplied state equals `completed`. There is no result producer,
probe occurrence, authenticity, or present-question relevance check.

Field standing is:

* corpus/material/representation/contract data, statuses, provenance, results,
  blockers, deferrals, failures: **external testimony**;
* work/status/policy vocabularies and observation cases: **developer-defined
  grammar**;
* hash IDs: **derived identity**;
* exact tuple and representation-kind comparisons: **validated relationship** only
  for addressability/equality, not constitutional admission;
* missing representation/prerequisite and exclusions: **negative conditions**
  within supplied grammar;
* capability, work kind, convention and representation names: also
  **implementation routing**;
* actual producer occurrence, authority and independent applicability: **Unknown**.

Candidate work is not discovered from evidence or admitted by an examination
responsibility. Compatibility and authorization in the frontier are supplied;
candidate-projector compatibility is a mechanical declared-shape match. Candidate
identity carries no production occurrence. No active producer exists outside tests
and the unused public candidate JSON/API path, and the work set has no independent
consumer outside this adjacent chain.

## 7. Frontier classification mechanics

### Classification table

| Classification | Inputs used | Supplied or derived | Evidence consulted | Negative conditions | Downstream consequence |
| --- | --- | --- | --- | --- | --- |
| `eligible` | supplied compatibility=`compatible`; authorization=`authorized` or `not_applicable`; absence of examined/blocker/unsupported/deferral/unknown | Boolean mechanically derived from supplied testimony | None beyond supplied fields | Must lack examined, blocker, unsupported, deferral and Unknown; failure is notably not excluded | Render/count; test-only policy filtering |
| `examined` | matching result tuple with supplied `result_state=completed` | Exact-match boolean over supplied reference | No result body or occurrence | Exact member/hash/work/capability/convention tuple required | Render/count; later tests preserve ID |
| `blocked` | nonempty caller `blockers` | Supplied-presence boolean | None | None | May coexist; prevents eligible |
| `unsupported` | supplied compatibility=`unsupported` | Supplied-label equality | None | None | Prevents eligible |
| `deferred` | nonempty caller deferral testimony | Supplied-presence boolean | None | None | Prevents eligible |
| `failed` | nonempty caller failure references | Supplied-presence boolean | None | Does **not** prevent eligible | Orthogonal render/count |
| `unknown` | work unknowns, unrecognized compatibility/authorization, or conflict | Mechanical aggregation | None | Cleared only by accepted labels and no unknowns/conflict | Prevents eligible; later test policy excludes |
| `conflict` | supplied status=`eligible` while examined/unsupported/blocked/deferred/unknown | Developer-defined inconsistency predicate | None | Requires supplied eligible claim plus contrary local flags | Also makes unknown |
| `newly_eligible` | no previous frontier input exists | Constant string `unresolved_no_previous_frontier_input` | None | Never computed | Representation only |

Several flags can be true simultaneously (`failed` can even coexist with
`eligible`; blocked/deferred/failed/examined can overlap). The conjunction is an
implementation-local orthogonal-facet scheme, not recovered constitutional meaning.
“Eligible” means only permitted through the later developer filter if a caller/test
chooses to invoke it; there is no active consumer. It establishes neither method
applicability, authority, nor operational readiness. `unsupported` is supplied
compatibility text; `blocked` preserves caller strings rather than proving a lawful
stop; `examined` means exact completed-reference tuple match, not that a probe ran.

Beyond rendering and diagnostics that describe/check static surface shape, only
tests consume a frontier in later stages. “Frontier” overstates the present act if
read constitutionally; the exact current subject is a read-only caller-status
classification inventory. This report does not rename it.

## 8. Applicability, policy and selection

### 8.1 Method applicability

Testimony supplies inquiry, candidate/contract/artifact/version/method identities,
one of `applicable|inapplicable|unknown|conflict`, reason, three constraint families,
supporting/contradicting references, and Unknowns. The projector matches inquiry and
candidate address, artifact/version and optional contract identity. It aggregates
testimony, copies/combines constraints and references, treats contradictory states
or explicit contradiction as conflict, treats no testimony/mismatch as unknown,
and preserves incompatible candidate conditions. It consults no evidence or
competency and does not examine candidate-method relevance. Exact matching
establishes addressability only. The projection organizes—and labels as a result—
supplied applicability testimony; it does not derive stronger applicability
standing.

Its only downstream code consumers are policy and the probe binder, plus its
frontier adapter; all invocations are tests. It has no CLI, diagnostic entry,
runtime entrance, or independent producer. Deleting it would not change frontier
CLI behavior (although it is a shared typed dependency of the test-only later
district).

### 8.2 Examination policy

The accepted developer-enumerated policy kinds are
`explicit_work_identity`, `all_eligible_no_order`, `no_selection`, and
`prerequisite_first`; any other kind becomes Unknown. Callers choose `policy_kind`,
`policy_parameters`, tie treatment, prerequisite entries, continuation/resource
constraints, support/contradiction references, no-selection conditions and
Unknowns. The projector defaults missing tie treatment, derives all/in-scope and
eligible-in-scope IDs from the frontier plus applicability labels, and calculates
state/sufficiency using developer branches. “Sufficient for selection” means the
branch leaves a unique mechanically permitted item (or named eligible item), not
that external evidence warrants policy, authority, or selection.

The projection does not choose policy or authorize selection; it normalizes caller
resolution testimony through developer grammar. The grammar is not externally
compiled and no independent runtime producer exists. Its only substantive consumer
is selection in tests. Deletion would not affect the frontier CLI.

### 8.3 Work selection

Selection validates exact frontier/policy/handoff IDs and copied fields, considers
only policy-declared eligible scope whose frontier flag is true, and returns
`conflict`, `unknown`, `no_selection`, or at most one `selected` identity. Explicit
identity chooses its named eligible item. No-order and prerequisite-first select
only when exactly one remains; zero yields no selection; several yield no selection
without an invented tie-break. Unknown/conflict policy states remain unresolved.

It compares no evidence, establishes neither applicability nor authorization, and
does not choose among independently admitted candidates. It mechanically applies
caller-supplied policy to caller-classified work. Only tests invoke it, and only the
probe binder/tests consume its output. It is not recoverable as a constitutional
selection act without evidence of responsible candidate admission, evidence-derived
applicability, warranted policy/selection evidence, a responsible occurrence,
authority limits, and an active bounded consumer.

## 9. Probe-request endpoint

“Probe” refers only to the requested transformation represented by selected work:
produce the caller-contract's output representation from its input representation
for one artifact/version. The binder creates a stable request ID; binds question,
selection, frontier and policy references; exact candidate/member/artifact/version,
contract, capability, work kind and convention; copies method and fidelity,
attribution, claim-treatment, support/provenance/Unknown constraints; and constructs
a requested-outcome string. Its read-only/no-ledger/no-mutation declarations are
dataclass defaults. It declares no operational authority.

The binder performs substantial identity consistency validation, but identity
matching is not standing validation. Searches recovered no concrete probe
competency, registry entry, executor, dispatcher, CLI, diagnostic entry, event,
execution attempt, result artifact, return consumer, transport/emission, or
production caller. The request never leaves this representation boundary. Its only
consumers are its JSON serializer, human formatter and tests. It is therefore a
**representation-only endpoint**. Deleting it would remove no current operator
behavior.

## 10. Table 2 — Supplied versus derived standing

| Field/classification | Source | Validation | Derived act | Claimed standing | Supported standing |
| --- | --- | --- | --- | --- | --- |
| Question identity/provenance/text | Caller JSON or helper | Dataclass arity; later equality | Copied/reference-hashed | Bounded internal inquiry | Caller-authored question-shaped reference; mixed |
| Corpus/material/scope/authorization testimony | Caller | Required strings and member identity | Sorted/copied | Bounded corpus and authority | Inventory testimony only |
| Contract capability/work/convention/availability | Caller | Required strings, duplicate/member references | Exact representation-kind match | Available compatible examination work | Routing/contract testimony |
| Candidate IDs | Projector hash or caller frontier JSON | Duplicate and member reference | Stable hash in candidate projector/frontier item | Candidate examination identity | Derived implementation identity, no occurrence |
| Compatibility | Caller, or declared representation-kind match | Enumerated comparisons only | Observation/label | Compatibility | Supplied or mechanical shape compatibility |
| Authorization | Caller | Accepted strings only | Eligibility predicate | Authorization | Unsupported testimony; no authority boundary |
| Existing result / `examined` | Caller | Exact tuple match | Completed boolean | Prior examination | Matching caller result reference only |
| blockers/deferrals/failures | Caller | String-list shape | Presence booleans | Lawful stop/history | Preserved caller testimony |
| Frontier `eligible` | Developer predicate over caller labels | Mechanical conditions | Boolean conjunction | Eligibility/readiness | Local filter eligibility only |
| Frontier conflict/unknown/newly eligible | Developer grammar | Local comparisons | Aggregate/constant | Constitutional conflict/Unknown/change | Implementation classification; no previous frontier for change |
| Applicability | Caller testimony | Identity equality/conflict aggregation | Organized state | Method applicability | Addressed testimony, not evidence-derived finding |
| Method constraints | Caller testimony | Lists and identity association | Union/copy | Binding lawful constraints | Preserved caller constraints |
| Policy kind/parameters/tie/prerequisites | Caller within developer enum | Identity and branch checks | Normalized policy | Examination policy | Caller resolution testimony in compiled grammar |
| Policy sufficiency | Developer branch | Cardinality/state | Unique-item predicate | Sufficient policy | Mechanical sufficiency only |
| Selection | Developer filter | Exact handoff/identity checks | Zero/one choice | Constitutional selection | Implementation-local policy application |
| Probe request | Binder | Cross-artifact identity/version checks | Bound representation | Executable probe request | Representation only; no invocation/authority |

## 11. Table 3 — Stage classification

| Stage | Actual mechanical act | Evidence consulted | Independent demand | Constitutional classification | Disposition pressure |
| --- | --- | --- | --- | --- | --- |
| Raw question ingress | Dataclass reconstruction | Caller JSON only | Required by frontier CLI | mixed | decompose candidate |
| Candidate projection | Declared representation/contract matching | Caller testimony, no repository evidence | None outside adjacent tests/API | developer-compiled organizer | shared dependency |
| Frontier | Orthogonal status classification and exact result tuple matching | Caller-supplied references/labels only | Only operator-facing examination demand | live but contaminated projection | retain for separate repair |
| Applicability | Identity-match and aggregate testimony | Supplied references, not their evidence | None | developer-compiled organizer | shared dependency |
| Policy | Normalize testimony through four branch kinds | Frontier/applicability outputs, no warrant evidence | None | developer-compiled organizer | shared dependency |
| Selection | Validate handoff and filter to zero/one | Projected labels only | None | test-supported callable artifact | delete candidate |
| Probe request | Bind/copy identities and constraints | Neighbor representations only | None | representation-only endpoint | delete candidate |

No disposition is implemented. The independently bounded deletion district is the
probe-request endpoint—module, serializer/formatter and its tests/report—because it
has no operational consumer. Selection is adjacent pressure but is not combined
with that possible action here; applicability/candidate/policy are shared typed
dependencies and need a separately exact boundary before broader demolition.

## 12. Tests as implementation evidence

### Table 5 — Test support

| Test path | Stage | Behavior proved | Production reachability proved? | Stronger claim not supported |
| --- | --- | --- | --- | --- |
| `tests/test_bounded_constitutional_question.py` | Question helper/artifact | Determinism, preservation, rendering, negative operational defaults | No examination road | Seed-owned formation or consumer validation |
| `tests/test_candidate_examination_work.py` | Candidate projection | Constructor/factory invariants, deterministic shape matching, observations, adapter, serialization | No | Discovery, admission, capability reality |
| `tests/test_examination_frontier.py` | Frontier | Mechanical classifications, exact result tuple check, determinism, rendering, inventory/shape visibility and mixed flags | Yes only where explicit CLI tests invoke the flag; unit calls alone no | Evidence-derived eligibility, execution, applicability |
| `tests/test_examination_method_applicability.py` | Applicability | State aggregation, identity matching, constraints, deterministic adapter; manually constructs work set | No | Competency finding or runtime ingress |
| `tests/test_examination_policy_projection.py` | Policy | Four policy branches, Unknown/conflict/sufficiency, serialization; manually constructs prior stages | No | Policy choice, warrant, authority |
| `tests/test_examination_work_selection.py` | Selection | Exact handoff validation, ties, zero/one, preservation, determinism; manually builds frontier/applicability/policy | No | Responsible constitutional selection |
| `tests/test_examination_probe_request.py` | Probe binding | Full manual chain, identity/version refusal, constraints, serialization/formatting | No | Dispatcher, execution, emission, result return |
| `tests/test_static_constitutional_pipeline_deletion.py` | Holdout/visibility | Frontier module remains importable and registered after PR 2139 deletion | Only continued frontier surface | Permanent preservation or later-stage demand |

The probe test is the apparent end-to-end road: it manually constructs the question,
corpus/contracts, candidate set, applicability testimony, frontier, resolution
testimony, policy, selection and handoff before binding the request. That proves
composability, not production wiring. No test proves actual probe execution or
result return. Diagnostic tests prove visibility metadata, not runtime invocation.

## 13. Historical genesis (testimony, not authority)

The surviving slice reports identify their intended local sequence:

| Artifact | Historical testimony | Expected producer/consumer then | Current correction |
| --- | --- | --- | --- |
| Candidate set | Candidate-work projection slice | Caller corpus/contracts; direct frontier adapter | Still only API/tests; CLI bypasses it |
| Frontier | Frontier projection slice | Operator diagnostic; “future” selector/probe | CLI remains; future consumer not production-wired |
| Applicability | Applicability slice | Supplied testimony; downstream policy/probe | Only tests invoke it |
| Policy | Policy slice | Resolution testimony; handoff to future selector | Selector exists but only tests connect it |
| Selection | Selection slice | Apply policy; future probe handoff | Binder exists but only tests connect it |
| Probe request | Probe-binding slice | Selected work to exact request meaning | No executor/result road appeared |

Available repository history is grafted into the large commit labeled PR 2042, so
it does not independently expose each original introducing commit/PR. The slice
reports establish historical motivations only; exact individual introducing PR
numbers remain **Unknown in the available history**. PR 2138 recovered the shared
question/static-pipeline topology; PR 2139 deleted that static district while
explicitly holding these examination artifacts out for this separate recovery.
Neither holdout nor planned “future” consumer proves present demand. Current import
and call evidence controls the verdict.

## 14. Book constraints

The Book constrains claims but is not used to invent missing code.

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
| --- | --- | --- | --- |
| Raw caller question shape is not Seed-owned internal question | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, bounded resolution and 04.Question.B/E | Operator wording is testimony/pressure; internal formation is Seed-owned and bounded | Which missing producer should be built |
| Candidate carriage/matching does not establish production | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, 01.External.F | Producer/formation/provenance must remain attributed or Unknown | That no candidate can exist |
| Examination relevance requires explicit bound record material | `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`, 04.Examination.A/B | Applicability/relevance, movement and lawful inactivity remain distinct | Applicability from caller labels |
| Applicability, selection, request and execution are distinct | same path, bounded resolution and Important distinctions | Responsible selection/request/invocation are separate occurrences | A hidden executor |
| Identity resolution is not itself selection | `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md`, bounded resolution | Selection needs bounded candidates plus selection evidence/policy and owner validation | That this filter is a lawful selection act |
| Authorization labels/selection/request do not grant authority | `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`, Authorization boundary correction 001 | Authority needs responsible grant coordinates | Any authority from `authorized` text |
| Request formation is not invocation/result | `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, Request-shaped representation correction 001 | Formation, emission, receipt, invocation, performance and result are distinct | Execution from request-shaped names |
| Rendering does not strengthen or prove uptake | same path, 08.Communication.C | Representation/emission/receipt/reliance remain separate | A constitutional consumer from a formatter |

## 15. Direct verdicts

1. **One coherent road?** No; one live frontier road and a manually composable,
   uninvoked later district are adjacent, not wired.
2. **Only operator surface?** `seed --examination-frontier JSON_FILE` (with optional
   `--json`).
3. **Where does it end?** `ExaminationFrontier` JSON or human terminal output.
4. **Invokes applicability?** No.
5. **Invokes policy?** No.
6. **Invokes selection?** No.
7. **Invokes probe construction?** No.
8. **Later non-test callers?** None of candidate projection, applicability, policy,
   selection or probe binding; serializers/formatters are not substantive callers.
9. **Only production-callable?** All those public typed APIs are callable but
   uninvoked in repository production.
10. **Test-only in practice?** Candidate projection and its richer work set,
    applicability, policy, selection, and probe binding.
11. **Complete internal question?** No; it is a mixed root/reference envelope.
12. **Production standing validated?** No.
13. **Frontier eligibility evidence-derived?** No; it is a predicate over supplied
    labels/references.
14. **Supplied frontier classifications?** Compatibility/authorization/status and
    result/blocker/deferral/failure/unknown inputs are supplied; booleans are
    mechanically derived from them.
15. **Applicability derived?** No; supplied testimony is identity-matched and
    organized.
16. **Policy chosen by projection?** No; caller testimony chooses kind/parameters.
17. **Constitutional selection act?** Not established; it is a local filter.
18. **Probe reaches executor?** No.
19. **Result returns?** No.
20. **Frontier faithfully named?** Not constitutionally; current act is a supplied
    status-classification inventory. Name remains unchanged.
21. **Independent operator demand?** Frontier only.
22. **Independent non-test production demand?** Frontier loader/projector/renderers
    only; diagnostic metadata has separate visibility demand but does not invoke it.
23. **Only tests/neighbors?** Candidate work set, applicability projection, policy
    projection/handoff, selection/future handoff, probe request.
24. **Mixed artifacts?** `BoundedConstitutionalQuestion`, candidate work (derived
    identity plus supplied grammar), frontier, and policy projection.
25. **Developer-compiled grammar?** Candidate observations; frontier flags/conflict
    predicate; applicability state aggregation; four policy kinds and sufficiency;
    selection states/tie behavior; request state/convention.
26. **Unknowns?** Original individual introducing PR numbers in available grafted
    history; any out-of-repository Python callers; whether supplied references
    correspond to real evidence/results; intended future responsible producers and
    consumers. In-repository reachability and executor absence are not Unknown.
27. **Malformed JSON domain-bounded?** No.
28. **Freeze raw exceptions?** No.
29. **Independently deletable district?** The probe-request representation endpoint
    and its exclusive serializer/formatter/tests/report can be bounded independently;
    no disposition is implemented here.
30. **Separate recovery/repair?** Repair of the live frontier JSON/question
    origination boundary must be separate; shared candidate/applicability/policy
    dependencies need exact narrower recovery before broader deletion.
31. **Another broad report?** No; the graph and standing are conclusive enough for a
    bounded next change.
32. **Single next lawful action:** **delete one independently bounded
    representation-only district**—the probe-request endpoint—without combining
    repair or connecting the chain.

## 16. Completion statement

The operator can invoke only a raw-JSON-fed frontier classification and render it.
Production calls no later examination stage. Tests assemble every intermediate
artifact and terminate at a bound request representation. Evidence is not consulted
beyond caller-supplied references and exact implementation-local equality tests;
callers provide the constitutional-looking coordinates. The live mixed frontier
boundary requires separate repair, while the probe endpoint is independently
bounded deletion pressure. No implementation repair or disposition occurs in this
report.
