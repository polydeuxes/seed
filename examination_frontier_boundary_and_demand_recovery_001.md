# `ExaminationFrontier` boundary and demand recovery 001

## 1. Executive verdict

This is one bounded, report-only Fidelity recovery against merged `main` at
`5b40462` (PR 2147, **Delete unused bounded-question producer helper**). That
prerequisite is present. This change does not amend the Book, production code,
tests, schemas, CLI behavior, diagnostic registrations, exports, active
documentation, persisted data, or runtime behavior.

The exact surviving production road is:

```text
operator-selected JSON file
-> scripts/seed_local.py --examination-frontier
-> json.loads(...)
-> examination_frontier.input_from_json_dict(...)
-> BoundedConstitutionalQuestion(**bounded_inquiry)
-> CorpusMember.from_json_dict(...)
-> CandidateWork.from_json_dict(...)
-> WorkResultReference.from_json_dict(...)
-> project_examination_frontier(...)
-> ExaminationFrontier
-> examination_frontier_json(...) or format_examination_frontier(...)
-> stdout
```

There is no later production consumer. Repository-wide Python searches establish
that the direct unpack at `seed_runtime/examination_frontier.py:82` is the only
non-test in-repository construction of `BoundedConstitutionalQuestion`; the CLI is
the only non-test caller of the frontier loader, projector, serializer, and
formatter. No scheduler, selector, inquiry apparatus, examination method, probe,
evidence, comparison, finding, persistence, or subsequent invocation reads the
frontier or an individual classification.

The implementation performs a deterministic consistency check and status
projection over caller-supplied coordinates. It does not discover corpus or work,
inspect material, resolve capability or authority, load or inspect results, or
establish examination. Its booleans are mechanically derived from caller labels,
list presence, and exact coordinate equality. Determinism and validation give the
output repeatable representation shape, not independent constitutional standing.

Direct verdicts:

| Question | Verdict |
| --- | --- |
| operator reachability | **Present:** one JSON-file CLI branch with human/JSON stdout. |
| question standing | **Caller testimony only:** construction is direct dataclass unpack; only id, provenance string, and question text are consumed. |
| corpus standing | **Caller testimony only:** members are neither discovered nor read or verified. |
| candidate-work standing | **Caller testimony only, relationship-constrained:** work is neither derived, requested, selected, nor executed. |
| result standing | **Caller testimony only, coordinate-constrained:** no result artifact/content is loaded; `completed` is trusted text. |
| classification standing | **Mechanical status projection:** predicates over supplied labels/lists/references; not evidence-derived examination standing. |
| identity standing | **Stable coordinate hashes only:** neither occurrence nor provenance, responsibility, currentness, or standing. |
| consumer demand | **None independently recovered:** both rendering branches terminate at stdout. |
| diagnostic demand | **Visibility only:** registrations describe/audit the CLI surface but do not invoke or consume it. |
| `BoundedConstitutionalQuestion` demand | **None outside this district:** its serializer, formatter, tests, export, and historical/active prose do not supply a production consumer. |

**Independent-demand verdict:** no independently warranted responsibility would
disappear if this road and its now-exclusive bounded-question support were deleted.
What would disappear is a live operator-facing deterministic renderer/checker for
caller-authored campaign-status testimony. No in-repository consumer relies on its
output, and no independent producer establishes the input standing its frontier
name would require.

## 2. Evidence boundary and method

The recovery inspected, at minimum, `seed_runtime/examination_frontier.py`,
`seed_runtime/bounded_constitutional_question.py`, `scripts/seed_local.py`,
`seed_runtime/diagnostic_inventory.py`,
`seed_runtime/diagnostic_shape_audit.py`,
`tests/test_examination_frontier.py`, and
`tests/test_bounded_constitutional_question.py`. Repository-wide searches covered
every requested symbol and spelling, constructors, aliases, imports, field reads,
serializers, formatters, CLI parser/dispatch, diagnostic metadata, tests, active
operator prose, and historical reports. Generic `bounded_inquiry_ref` fields in
unrelated shared-explanation modules were inspected as lexical collisions, not
aliases of this artifact.

Evidence classes were kept separate:

* **Production execution:** only the CLI branch and frontier module.
* **CLI reachability:** parser flag, primary-action inclusion, dispatch, rendering.
* **API constructibility:** public module objects can be imported/called but no
  unobserved caller was inferred from that fact.
* **Diagnostic visibility:** inventory metadata and shape-source inspection.
* **Test-only construction:** dedicated tests directly construct all dataclasses.
* **Active operator documentation:** Book and `docs/` references are descriptions,
  not invocation or consumption.
* **Historical testimony:** reports and Git/PR records explain genesis/disposition,
  not current authority or demand.

Definitions were not counted as producers; serialization/formatting was not counted
as a substantive post-frontier consumer; tests, registrations, documentation, and
reports were not counted as production consumers. Bounded executable probes called
the public JSON boundary and CLI from `/tmp`; tracked-file status was compared, and
no probe input was written into the repository.

## 3. Complete producer/consumer graph

| Artifact/function | Definition / producer | Inputs and validation | Non-test / test-only callers | Consumer and fields consumed | Downstream / status |
| --- | --- | --- | --- | --- | --- |
| JSON input | operator-selected file; `Path.read_text` + `json.loads` | JSON syntax only before loader | CLI / CLI test | `input_from_json_dict` consumes three named top-level keys; other keys ignored | ephemeral invocation input; nonterminal |
| `BoundedConstitutionalQuestion` | dataclass; produced by `BoundedConstitutionalQuestion(**qd)` | Python signature only; no value/type/relationship validation | loader only / both dedicated test files | projector reads `bounded_question_id`, `inquiry_provenance`, `bounded_question` | copied inquiry reference and frontier-id input; nonterminal |
| `CorpusMember` | dataclass; `CorpusMember.from_json_dict` | three required nonempty strings; tuple-list element shape; optional scalars coerced with `str` | loader only / tests direct/loader | projector reads `member_id`, `artifact_identity`, `artifact_hash`; copies every field into output; sorter reads `member_id` | preserved caller member plus work coordinate; nonterminal |
| `WorkResultReference` | dataclass; `WorkResultReference.from_json_dict` nested in candidate loader | required ids/kind/state; optional coordinates coerced; provenance string tuple | candidate loader only / tests | projector reads five work coordinates, `result_state`, `result_id`; output copies all | examined/reason or mismatch refusal; nonterminal |
| `CandidateWork` | dataclass; `CandidateWork.from_json_dict` | required candidate/member/kind; optional scalar coercion; nested results and string tuples | loader only / tests direct/loader | projector reads all fields except candidate provenance; copies selected coordinates/status lists but omits candidate provenance and supplied status | work items/classifications; nonterminal |
| `FrontierClassification` | projector constructs one per work | developer predicate over supplied values | projector only / tests observe/direct accessibility | work-item JSON and human formatter; formatter reads true booleans | rendering only; nonterminal until stdout |
| `FrontierWorkItem` | projector constructs one per candidate | duplicate candidate/member link/result coordinate/capability condition | projector only / tests | frontier serializer copies all; formatter reads id, kind, member, classification, reasons | JSON/human stdout; no runtime consumer |
| `ExaminationFrontier` | `project_examination_frontier` | question `isinstance`, corpus id truthiness, duplicates, member links, compatible capability, result-coordinate equality | CLI only / tests | `examination_frontier_json` or `format_examination_frontier` | terminal stdout; terminal production artifact |
| JSON serializer | `examination_frontier_json` | no explicit type check; calls `to_json_dict` | CLI only / tests indirectly | `json.dumps` | stdout; terminal |
| human formatter | `format_examination_frontier` | no explicit type check; attribute reads | CLI only / tests | `print` | stdout; terminal |
| inventory entry | `DIAGNOSTIC_INVENTORY` row | static metadata | inventory CLI/tests, not frontier invocation | inventory rendering/audit reads metadata | visibility about surface; not a frontier consumer |
| shape spec | `DIAGNOSTIC_IMPLEMENTATION_SPECS` row | checks module/function/flag/markers and declared shape | shape-audit CLI/tests | audit rows | visibility consistency; not a frontier consumer |

Direct answers:

1. **Yes.** `input_from_json_dict(...)` is the only non-test producer of the
   complete argument tuple used by the sole non-test projector call.
2. **Yes.** `BoundedConstitutionalQuestion(**qd)` is the only in-repository
   non-test construction after PR 2147.
3. **No.** Nothing consumes `ExaminationFrontier` after either rendering branch.
4. **No.** No runtime road consumes an individual classification.
5. **No.** No scheduler, selector, inquiry apparatus, method, probe, evidence,
   comparison, or finding process consumes it.
6. **No.** Searches found no active event, cache, projection store, persisted shape,
   or later invocation referencing these `frontier_id`/`work_item_id` values.
7. **Yes.** The frontier is recalculated for one invocation and discarded after
   stdout.
8. **Yes.** Inventory and shape audit are visibility around the CLI surface.
9. **No.** No remaining module outside this frontier district consumes
   `BoundedConstitutionalQuestion`.
10. **Yes.** Deleting the frontier removes the only production demand for the
    question class; its serializer, formatter, tests, export, and active prose then
    have no independent runtime demand.

## 4. Input field ownership and standing

### 4.1 Bounded inquiry

All fields originate in `bounded_inquiry`. Required/defaulted below describes the
dataclass signature, not JSON semantic validation.

| Field | Required/default | Type/value/relationship validation | Standing before projection | Consumer / output effect |
| --- | --- | --- | --- | --- |
| `bounded_question_id` | required | none | caller value | copied to inquiry reference; enters `frontier_id` |
| `operator_inquiry` | required | none | caller value | ignored |
| `inquiry_provenance` | required | none | caller provenance label | copied to inquiry reference only |
| `bounded_question` | required | none | caller text | copied to inquiry reference only |
| `constitutional_intent` | required | none | caller label | ignored |
| `scope_status` | required | none | caller label | ignored |
| `uncertainty` | required | none; list is accepted despite tuple annotation | caller representation | ignored |
| `unknowns` | required | none | caller representation | ignored; does not make frontier unknown |
| `caller_supplied_fields` | default `()` | none | caller representation | ignored |
| `testimony_status` | developer string default, caller-overridable | none | negative developer declaration or caller text | ignored |
| `read_only_boundaries` | developer tuple default, caller-overridable | none | developer/caller declarations | ignored |
| `read_only` | developer `True`, caller-overridable | none | declaration, not verified property | ignored; output frontier independently defaults `True` |
| `writes_event_ledger` | developer `False`, caller-overridable | none | declaration, not effect evidence | ignored; output independently defaults `False` |
| `mutates_cluster` | developer `False`, caller-overridable | none | declaration, not effect evidence | ignored; output independently defaults `False` |

Thus exactly three question fields are consumed. Overrides of the three flags and
the testimony/boundary declarations do not affect identity, classification,
reasons, unknowns, output flags, or rendering. The actual effects were separately
verified in section 8; field names are not proof.

### 4.2 Corpus and members

`corpus_id` is required by `_req`; `corpus_label` defaults/coerces to `""`;
`members` defaults to empty; corpus `unknowns` defaults to empty and must be a
list/tuple of strings. Unknown top-level/corpus/member keys are ignored.

| Member field | Required/default; validation | Standing | Consumer / effect |
| --- | --- | --- | --- |
| `member_id` | required nonempty `str`; duplicate rejected | trusted caller id, uniqueness only | link key, sort key, work identity, copied |
| `substrate_kind` | required nonempty `str` | caller label | copied only |
| `artifact_identity` | required nonempty `str` | caller label | work identity and copied |
| `artifact_hash` | default `""`; arbitrary value coerced by `str(... or "")` | caller label, not calculated | result matching, work identity, copied |
| `material_reference` | default `""`; coerced | caller label | copied only |
| `scope_status` | default `in_scope`; coerced | caller assertion | copied only; no classification effect |
| `provenance` | default empty; list/tuple of strings | caller testimony | copied only |
| `authorization_testimony` | default empty; list/tuple of strings | caller testimony | copied only |
| `unknowns` | default empty; list/tuple of strings | caller testimony | copied only; no work/frontier unknown effect |

The frontier does **not** discover a member, read referenced material, verify
identity, calculate hashes, check references, establish scope/provenance, or
establish authorization. It preserves those supplied representations and uses
three coordinates mechanically.

### 4.3 Candidate work

| Field | Required/default; validation | Standing | Consumer / effect |
| --- | --- | --- | --- |
| `candidate_work_id` | required nonempty string; duplicate rejected | trusted caller occurrence label | copied and secondary sort key; omitted from `work_item_id` |
| `corpus_member_id` | required nonempty string; must equal a supplied member id | validated relationship to supplied set | selects member; copied |
| `work_kind` | required nonempty string | caller label | identity/result match/copied |
| `capability_id` | default empty, coerced; nonempty required only when compatibility is exactly `compatible` | caller label | identity/result match/copied |
| `convention` | default empty, coerced | caller label | identity/result match/copied |
| `compatibility_status` | default `unknown`, coerced | caller label | unsupported/unknown/eligible predicates |
| `authorization_status` | default `unknown`, coerced | caller label | unknown/eligible predicates |
| `existing_results` | default empty; iterable of result objects expected | caller references | coordinate checks, examined, reasons, copied |
| `blockers` | default empty string tuple | caller testimony | presence -> blocked/reason; copied |
| `deferral_testimony` | default empty string tuple | caller testimony | presence -> deferred/reason; copied |
| `failure_references` | default empty string tuple | caller testimony | presence -> failed/reason; copied |
| `supplied_status` | default empty, coerced | caller label | exact `eligible` may trigger conflict; not copied |
| `provenance` | default empty string tuple | caller testimony | ignored and not copied |
| `unknowns` | default empty string tuple | caller testimony | seeds work-item unknowns and affects eligibility |

The frontier does not discover/derive candidate work or a capability; check that a
capability exists; establish compatibility or authorization; observe blockers or
failures; establish deferral; select work; or request work. It tests supplied
relationships and labels only.

### 4.4 Existing results

| Field | Required/default; validation | Standing | Consumer / effect |
| --- | --- | --- | --- |
| `result_id` | required nonempty string | trusted caller id | reason and copied; not independently verified |
| `corpus_member_id` | required nonempty string | caller coordinate | exact match to selected member |
| `artifact_hash` | default empty, coerced | caller coordinate | exact match to member's supplied hash |
| `work_kind` | required nonempty string | caller coordinate | exact match to candidate |
| `capability_id` | default empty, coerced | caller coordinate | exact match to candidate |
| `convention` | default empty, coerced | caller coordinate | exact match to candidate |
| `result_state` | required nonempty string | caller label | exact `completed` sets examined |
| `provenance` | default empty string tuple | caller testimony | copied only |

The projector loads no result artifact, verifies no identifier/provenance/content,
and checks no successful examination. Exact equality of five supplied coordinates
plus caller text `result_state == "completed"` is not result verification.

## 5. Supplied-versus-derived output table

| Output field | Classification and exact source |
| --- | --- |
| `artifact_type` | developer-authored declaration, constant `ExaminationFrontier` |
| `frontier_id` | mechanically derived stable hash from supplied question id/corpus id and derived work ids plus developer convention |
| `inquiry_reference` | copied caller testimony: three question fields |
| `corpus_id`, `corpus_label` | copied/coerced caller testimony |
| `frontier_convention` | developer-authored constant/default |
| `corpus_members` | copied caller records, sorted mechanically; required/tuple shapes and duplicate ids validated |
| `work_item_id` | mechanically derived coordinate hash |
| work-item candidate/member/artifact/work/capability/convention fields | copied caller testimony after member-link validation |
| `classification.*` except `newly_eligible` | mechanically derived from caller testimony and relationship checks; not evidence-derived/runtime-observed |
| `newly_eligible` | developer-authored constant `unresolved_no_previous_frontier_input` |
| `reasons` | developer-authored messages selected mechanically; completed-result reason embeds caller result id |
| `existing_result_references`, blockers, deferrals, failures | copied caller testimony after listed shape/coordinate checks |
| work-item `unknowns` | copied candidate unknowns plus developer messages for unrecognized compatibility/authorization; conflict contributes boolean but not a new unknown string |
| `summary_counts` | mechanically counted classification booleans |
| `frontier_unknowns` | copied corpus-level caller strings |
| `boundary_notes` | developer-authored declarations/defaults |
| `read_only`, `writes_event_ledger`, `mutates_cluster` | developer defaults on output; not copied from question and not themselves runtime observation |

No output field is evidence-derived. Actual no-write/no-network effects are code-
and execution-observed, but the output booleans remain declarations.

Classification law:

| Classification | Caller trigger / constraint | Lawful local meaning | Does not mean |
| --- | --- | --- | --- |
| `eligible` | compatibility exactly `compatible`; authorization exactly `authorized` or `not_applicable`; capability nonempty; no matching completed result, blocker, unsupported label, deferral, or accumulated unknown; failure is not excluded | supplied labels satisfy developer predicate with no supplied disqualifier | lawful authorization, discovered/selected/requested/executable useful work |
| `examined` | at least one result has exact five-coordinate match and caller state `completed` | matching caller reference declares completion | result loaded, successful examination, content/claim understood or verified |
| `blocked` | nonempty caller blocker list | blocker testimony exists | blocker observed/current or work prohibited |
| `unsupported` | compatibility exactly `unsupported` | caller supplied that label | capability search or proof of absence |
| `deferred` | nonempty caller deferral list | deferral testimony exists | authorized/still-current deferral |
| `failed` | nonempty caller failure-reference list | failure testimony exists | failure inspected or eligibility excluded; it is orthogonal, so failed can be eligible |
| `unknown` | candidate unknowns, unrecognized compatibility/authorization, or supplied-eligible conflict | local input cannot satisfy unconflicted known predicate | epistemic survey of repository/world unknowns |
| `conflict` | supplied status exactly `eligible` while examined, unsupported, blocked, deferred, or unknown | one narrow label/predicate inconsistency | general contradiction detection; failures alone do not conflict |
| `newly_eligible` | no trigger; constant | previous frontier unavailable | any change or new occurrence |

`eligible`, `examined`, and `unsupported` mean nothing stronger than the precise
caller-testimony formulations in the governing question. `failed` is orthogonal to
eligibility. There is no previous-frontier input or comparison road.

## 6. Identity and relationship analysis

`_stable(prefix, payload)` canonicalizes JSON with sorted keys and compact
separators, hashes UTF-8 bytes using SHA-256, and prefixes the digest.

`_work_identity` includes: `corpus_id`, member `member_id`, `artifact_identity`,
`artifact_hash`, and candidate `work_kind`, `capability_id`, `convention`. It omits
candidate id, substrate kind, material reference, scope, all provenance and
authorization testimony, candidate compatibility/authorization/supplied status,
results, blockers, deferrals, failures, unknowns, and question.

`frontier_id` includes question `bounded_question_id`, `corpus_id`, the developer
frontier convention, and sorted `work_item_id` values. It omits question text and
provenance; corpus label/member-only records and all their omitted fields; candidate
ids; classifications; results; blockers; deferrals; failures; provenance;
unknowns; reasons; counts; and output flags.

Consequences:

1. Classification, blocker, failure, result, provenance, and unknown changes do not
   change `frontier_id` unless they also alter an included coordinate.
2. `work_item_id` identifies selected supplied coordinates, not candidate
   occurrence or verified work content.
3. Caller ids are trusted except local nonempty/uniqueness/link checks.
4. Hashing establishes repeatability for the serialized coordinate payload only;
   it establishes no occurrence, provenance, responsibility, standing, or
   currentness.
5. Two materially different frontiers can share an id—for example, identical
   coordinates with different candidate ids, statuses, results, failures,
   provenance, or unknowns.
6. Identical coordinates in separate invocations produce identical ids without
   proving the invocations are the same occurrence.

Identity stability is therefore distinct from constitutional standing.

## 7. Malformed-input matrix

The public Python boundary was probed without behavior changes. `ACCEPTED` means the
loader and, where necessary to exercise relationship checks, projector returned; it
does not mean the representation is semantically valid.

| Representative input | Observed result |
| --- | --- |
| top-level input is list | `AttributeError: 'list' object has no attribute 'get'` |
| missing `bounded_inquiry`; non-object bounded inquiry | `ExaminationFrontierError: bounded_inquiry is required` |
| missing required question field | `TypeError: BoundedConstitutionalQuestion.__init__() missing 1 required positional argument: 'bounded_question_id'` |
| extra question field | `TypeError: BoundedConstitutionalQuestion.__init__() got an unexpected keyword argument 'extra'` |
| blank required question string; wrong question scalar type | accepted |
| override question `read_only=false`, `writes_event_ledger=true`, or `mutates_cluster=true` | accepted; ignored by projection/output defaults |
| missing/non-object corpus | `ExaminationFrontierError: corpus is required` |
| missing or blank `corpus_id` | `ExaminationFrontierError: corpus_id is required` |
| `members` is integer | `TypeError: 'int' object is not iterable` |
| member element is integer | `AttributeError: 'int' object has no attribute 'get'` |
| missing/wrong-type `member_id` | `ExaminationFrontierError: member_id is required` |
| wrong optional member scalar (`artifact_hash=7`) | accepted after coercion to `"7"` |
| duplicate member id | `ExaminationFrontierError: duplicate_corpus_member_id` |
| `candidate_work` is integer | `TypeError: 'int' object is not iterable` |
| candidate element is integer | `AttributeError: 'int' object has no attribute 'get'` |
| missing candidate id | `ExaminationFrontierError: candidate_work_id is required` |
| wrong required candidate scalar (`work_kind=7`) | `ExaminationFrontierError: work_kind is required` |
| wrong optional candidate scalar (`compatibility_status=7`) | accepted after coercion |
| duplicate candidate id | `ExaminationFrontierError: duplicate_candidate_work_id` |
| unknown member link | `ExaminationFrontierError: unknown_corpus_member` |
| `existing_results` is integer | `TypeError: 'int' object is not iterable` |
| result element is integer | `AttributeError: 'int' object has no attribute 'get'` |
| missing result id | `ExaminationFrontierError: result_id is required` |
| wrong required result state scalar | `ExaminationFrontierError: result_state is required` |
| wrong/coerced or mismatched coordinate | `ExaminationFrontierError: existing_result_work_mismatch` |
| member provenance, candidate blockers, or candidate unknowns contain nonstrings | `ExaminationFrontierError: expected list of strings` |
| unexpected top-level field | accepted and ignored |
| malformed JSON text | `json.JSONDecodeError` at parser; CLI catches and emits argparse error, exit 2 |

Other exact boundary facts: missing `members` and `candidate_work` default to empty;
a mapping passed where a sequence is expected iterates keys and can yield raw
attribute errors; no JSON schema exists; dataclass annotations are not runtime
checks. The CLI catches `OSError`, `JSONDecodeError`, `ExaminationFrontierError`, and
`TypeError`, converting them to `parser.error(str(exc))` (usage/error on stderr,
exit 2). It does **not** catch `AttributeError`: a top-level JSON list emitted a
traceback and exit 1. Thus failures are mixed bounded refusals/raw Python behavior,
not one domain-bounded operator contract. These accidental raw exception types are
observations, not compatibility promises.

## 8. Operational-effects verification

Code inspection shows the invocation reads only the selected JSON file and imports
local Python modules. The frontier module uses dataclasses, JSON canonicalization,
sorting, and hashing. The CLI then prints. There is no Event-ledger import/call in
the district, projection-store/database/cache writer, repository writer, cluster
client, network library/call, material-reference read, capability invocation,
result loader, probe-request construction, persistence, or previous-frontier input.

Bounded human and JSON CLI executions completed while the test's and this recovery's
status checks showed no tracked-file mutation. Malformed probes also used `/tmp`.
Accordingly the observed road:

| Effect | Verdict |
| --- | --- |
| Event ledger write | no |
| projection store write | no |
| repository-file change | no (apart from this report authored by this PR) |
| cluster-state change | no code path |
| network access | no code path |
| referenced material read | no |
| capability execution | no |
| existing-result load | no |
| probe request creation | no |
| frontier persistence | no |
| prior-frontier comparison | no |

These are verified implementation effects, independent of caller-overridable
question flags and developer-authored frontier flags.

## 9. Independent-demand analysis

| Characterization | Supporting evidence | Contradicting evidence / required versus actual standing | Current consumer demand | Verdict |
| --- | --- | --- | --- | --- |
| real examination frontier | classifies named work and preserves reasons | requires established corpus/work/result standing and downstream movement; all are supplied and nothing moves | none after stdout | rejected |
| corpus visibility projection | preserves/sorts supplied member records | does not discover/read/verify visibility; standing is caller testimony | terminal only | accurate only as narrow supplied representation |
| candidate-work status projection | predicates over supplied candidates | neither candidates nor statuses are observed/established | terminal only | accurate narrow implementation description |
| caller-authored campaign-status renderer | caller supplies all substantive coordinates/status testimony; human/JSON render | output booleans/reasons are developer-derived, not literally copied | direct operator rendering demand only | best presentation characterization |
| deterministic consistency checker over supplied coordinates | duplicates, member links, result coordinates, and predicate conflicts checked | checks are narrow and omit semantic standing | direct operator invocation only | accurate implementation responsibility |
| diagnostic demonstration | inventory/shape entries and mixed-corpus test | CLI is runnable, not merely a test fixture | visibility only | partly accurate, not a consumer |
| useful bounded implementation support artifact | stable typed output and tests | no surviving staged code/import consumes it | none | no independently evidenced support demand |
| contaminated but independently demanded operator surface | operator can invoke it | no independent input producer or output consumer warrants frontier responsibility | none beyond self-display | rejected: reachability is not independent demand |
| disconnected district with no independent demand | sole raw-JSON producer, terminal endpoint, exclusive question dependency | it still works as renderer/checker | none | **established** |

The asymmetry matters: simplicity does not disqualify it; caller supply alone does
not contaminate it; live CLI and diagnostic registration do not warrant the stronger
responsibility. The decisive missing demand is a responsible producer/consumer
requiring this classification. Deletion would remove convenience rendering and
consistency checks, but no independently warranted current repository responsibility.

## 10. Remaining `BoundedConstitutionalQuestion` demand

| Use class | Exact remaining use | Demand verdict |
| --- | --- | --- |
| frontier production | import, direct JSON unpack construction, `isinstance`, three field reads | only production demand; internal to frontier district |
| tests | dedicated direct construction/serializer/formatter tests and frontier fixture | preservation evidence, not production demand |
| active export | package exports only `format_bounded_constitutional_question`, not the class/serializer | constructibility/convenience, no consumer |
| active-path Markdown search | matches are dated/audit/recovery reports under `book_of_seed/` and `docs/`; no current CLI guide/example was found | historical testimony, not active operator demand |
| historical reports | many reports and deleted-stage slice reports | historical testimony only |

Repository-wide Python searches found no other construction or consumer of the
class and no production call of `bounded_constitutional_question_json(...)` or
`format_bounded_constitutional_question(...)`. After frontier deletion, a single PR
should also delete `seed_runtime/bounded_constitutional_question.py`, its dedicated
tests, and active export. No active operator guide, example, or fixture advertising
this CLI/artifact was recovered, so there is no such file in the demolition set.
All matching dated/audit/recovery reports must remain unchanged. This report
performs none of those deletions.

## 11. Correct remote-history chronology

History is implementation testimony only. Current topology overrides original
intent. The environment has no configured Git remote, and the local history is
grafted: pre-2048 individual commits are not present. Consequently exact remote PR
titles, bodies, and per-PR changed-file lists for PRs 1636–1644 and 1936 could not be
independently retrieved. That is an environment retrieval limitation, not a claim
that those records are absent. The surviving reports supply the following bounded
chronology, but cannot substitute for unavailable exact remote metadata:

| PR | Available historical consequence/testimony | Exact remote metadata status |
| --- | --- | --- |
| 1636 | deep-corpus audit proposed the missing frontier responsibility | title/body/files Unknown: remote unavailable |
| 1637 | introduced `ExaminationFrontier`, projection, CLI, diagnostics, tests, and slice report | title/body/files Unknown: remote unavailable |
| 1638 | introduced candidate-work projection stage intended to feed frontier/later stages | title/body/files Unknown: remote unavailable |
| 1639 | introduced method-applicability testimony projection | title/body/files Unknown: remote unavailable |
| 1640 | introduced policy projection/handoff | title/body/files Unknown: remote unavailable |
| 1641 | introduced work selection/future-probe handoff | title/body/files Unknown: remote unavailable |
| 1642–1644 | completed downstream probe-binding/staged examination district described by surviving slice reports | individual mapping/title/body/files Unknown: remote unavailable |
| 1936 | removed the staged operational-realization continuation after probe request | title/body/files Unknown: remote unavailable |
| 2138 | **Recover complete bounded-question topology**; one report added | verified local commit `2baf3ab` and diff |
| 2139 | **Delete static constitutional-pipeline demonstration**; removed pipeline/views/CLI/diagnostics/tests while holding frontier for later recovery | verified local commit `ae12f3b` and diff |
| 2142 | **Recover examination topology and standing**; added one 544-line report | verified local commit `166cd0a` and diff |
| 2144 | **Delete disconnected examination staging chain**; deleted five runtime modules/five dedicated tests and adjusted Book/guard test; preserved frontier | verified local commit `0285181` and diff |
| 2147 | **Delete unused bounded-question producer helper**; removed named producer while retaining class/renderers/frontier direct loader | verified local commit `5b40462` and diff |

The current surviving consequence is narrower than the historical plan: PR 2144
removed every staged consumer, and PR 2147 left raw JSON unpack as the sole
production question construction. Neither former intent nor later holdout proves
present demand.

## 12. Exact Unknowns

1. Exact remote titles, bodies, changed-file lists, review discussion, and workflow
   results for PRs 1636–1644 and 1936 are Unknown because this checkout has no
   remote/repository locator and the grafted local history lacks those commits.
2. Any out-of-repository Python/API callers are Unknown; the in-repository graph is
   complete and no external compatibility claim is made.
3. Whether any operator has manually relied on CLI output is Unknown; no persisted
   reference or in-repository consumer records such reliance.
4. Whether supplied member/result/provenance references correspond to real current
   artifacts or occurrences is Unknown by construction; the road does not inspect
   them.
5. GitHub Actions status for the proposed PR is Unknown and is not claimed.

These Unknowns do not make the in-repository producer/consumer, standing,
classification, identity, or operational-effect findings uncertain.

## 13. One smallest lawful next action

**Delete the complete now-demandless frontier district in one PR.** The exact
demolition boundary is:

* delete `seed_runtime/examination_frontier.py`;
* delete `seed_runtime/bounded_constitutional_question.py`;
* delete `tests/test_examination_frontier.py` and
  `tests/test_bounded_constitutional_question.py`;
* remove `--examination-frontier` parser, primary-action, dispatch, imports, human
  formatter, and JSON wiring from `scripts/seed_local.py`;
* remove the `examination_frontier` diagnostic inventory registration and shape-
  audit implementation spec, and update their inventory/shape expectations;
* remove the bounded-question active package export;
* remove no operator documentation, example, or fixture: repository-wide searches
  recovered none independently active; and
* preserve all historical reports and audits unchanged.

This is one internally sharing disconnected district, so artificial leaf PRs would
not preserve independent consumers. The deletion must include visibility updates
and the required diagnostic inventory/shape-audit tests because the operational
surface would be removed. No replacement architecture or repair is proposed here.

Validation for this recovery included repository-wide requested-symbol searches,
constructor/caller searches, active documentation and historical-report searches,
Git log/diff inspection, direct malformed-boundary probes, caught and uncaught CLI
failure probes, the dedicated frontier/question tests, diagnostic inventory/shape
tests, compileall, diff whitespace checking, and an exact one-file change check.

Observed validation results:

| Command / probe | Result |
| --- | --- |
| `rg -n --hidden --glob '!.git/**' '<all requested symbols>' .` plus per-constructor/import/document searches | completed; 803 combined matches after adding this report, all production matches classified above |
| `PYTHONPATH=. python /tmp/probe_frontier.py` | completed; exact results recorded in section 7 |
| `python scripts/seed_local.py --examination-frontier /tmp/frontier_bad.json` and bounded list/element variants | malformed JSON and caught errors exited 2 via argparse; top-level list exited 1 with raw `AttributeError` traceback |
| `pytest -q tests/test_examination_frontier.py tests/test_bounded_constitutional_question.py` | 9 passed |
| `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` | 116 passed |
| `python -m compileall -q seed_runtime scripts` | passed with no output |
| `git diff --check` | passed with no output |
| `git status --short` / diff-name check | exactly this one new report |
