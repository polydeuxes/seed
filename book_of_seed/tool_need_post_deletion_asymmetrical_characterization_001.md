# ToolNeed Post-Deletion Asymmetrical Characterization 001

## Boundary, method, and answer in brief

This is one bounded, report-only characterization of the surviving `ToolNeed`
district at merged-main commit `38b5681` (PR 1985). It changes no implementation,
test, fixture, schema, export, event, projection, CLI, canonical chapter, earlier
report, or archived testimony. Historical documents were used as locators only;
their former runtime-road conclusions were not imported as current facts.

The short answer is asymmetrical. A directly constructed `ToolNeed` currently has
only **immutable, schema-valid, capability-related request-shaped representation
standing supplied by its caller**. No surviving responsible production boundary
admits it as a constitutional Need, and the object lacks the responsible consumer,
bounded horizon/requirement, reference condition, evidence-backed incompatibility,
material consequence, authority, scope, time, and satisfaction/closure warrant
needed to establish Need, Gap, Demand, or Capability standing. This does not make
the representation invalid: its narrower request/candidate standing is useful to
current read-only correlation and presentation consumers. Its one object shape
compresses caller testimony, a catalog correlation key, provenance-shaped text,
interface wishes, lifecycle labels, and projected current representation.

The current roads are more uneven than the class suggests:

* production code contains **no creator** of a new `ToolNeed` and emits no
  `tool_need.created`; direct construction and creation-event recording occur in
  tests only;
* `resolve_capability` is a callable, transient, read-only four-component metadata
  composition, but has no current caller or downstream consumer;
* in the current Pydantic-backed runtime, `set_status` fails at
  `dataclasses.replace(need, ...)` because `ToolNeed` is not a dataclass. It thus
  returns no replacement and records no event. Even if that compatibility defect
  were absent, its code expresses unguarded caller-controlled replacement, not a
  warranted constitutional transition;
* projector support accepts test/external ledger testimony, reconstructs the full
  creation payload into one current object, and folds any later accepted status
  event into latest status only. It does not preserve transition reason, evidence,
  authority, actor-specific justification, or status history in `State.tool_needs`.

The active Book is the constitutional grammar witness: artifact representation is
not constitutional standing; constructability and public reachability are not
production authority; Need does not authorize movement; Gap needs a declared
reference and scoped evidence; capability demand is not Capability, selection, or
authorization; selection is not authorization; projection is not source or
standing; representation, emission, receipt, Uptake, reliance, authority transfer,
and realization remain separate; refusal remains distinct from failure and missing
capability. Relevant canonical chapters are:

* `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` and
  `constructors-and-production-authority.md`;
* `03-goals-and-advancement/needs-and-opened-movement.md`,
  `selection-and-authorization.md`, and `construction-and-establishment.md`;
* `05-evidence-and-knowledge/testimony-and-established-fact.md`,
  `evidence-provenance-and-explanation.md`, and
  `recording-and-knowledge-extraction.md`;
* `06-state-and-projection/events-facts-and-state.md` and
  `projection-and-current-state.md`;
* `08-authority-communication-and-stopping/authority-scope.md`,
  `refusal-and-non-performance.md`, and
  `representation-emission-and-consumer-boundaries.md`.

These clauses warrant an **Unknown** answer where the implementation supplies only
a suggestive name. They do not require a universal Need object or invalidate a
narrow compatibility representation.

## Constitutional coordinate discipline

The recovered coordinates are deliberately kept distinct:

| Coordinate | Meaning in this examination | Current `ToolNeed` evidence |
| --- | --- | --- |
| Responsibility | accountable producer or consumer boundary | arbitrary constructor/event caller; no admitted owner |
| Act | bounded occurrence that can establish or transform standing | construction, lookup/composition, attempted replacement, append, replay, render are separate acts |
| Standing | what an artifact may lawfully assert for a scope | caller-supplied request-shaped representation only |
| Representation | fields carrying another responsibility's assertions | the `ToolNeed` model and serialized payload |
| Event | recorded occurrence claim | generic creation testimony if appended; status claim only if append is reached |
| Projection | replay-built current representation | dictionary keyed by `ToolNeed.id`, latest status folded in |
| Consumer Uptake | evidenced local reliance by a consumer | field-level read-only correlation, filtering, counting, rendering; no receipt/Uptake occurrence recorded |
| Artifact field | one stored coordinate | may be copied, defaulted, or merely serialized; not a warrant |
| Status label | compatibility-constrained lifecycle word | type vocabulary on construction; no lawful transition graph |

## Road A — construction and recording

### Producer inventory

| Producer | Input material and responsibility | Supplied / derived / defaulted | Identity, workspace, provenance | Event and occurrence evidence |
| --- | --- | --- | --- | --- |
| Arbitrary Python caller of `ToolNeed(...)` | all required strings and any optional values; responsibility is not identified | caller supplies `id`, `name`, `summary`, `capability`, `reason`; may supply all others; model defaults workspace, status, provenance/risk, and lists | caller supplies identity and binding; neither is derived or checked | constructs only; no event |
| `StateProjector.apply`, creation branch | nested `payload.tool_need` or flat event payload from a ledger event | copies recognized payload values; model supplies omitted defaults; ignores unknown model fields | payload supplies `id` and `workspace_id`; event workspace selects replay but is not compared to artifact workspace | projects accepted ledger testimony; is not a creator/emitter |
| Projection snapshot loader | plain `tool_needs` dictionary from a projection snapshot | reconstructs recognized model fields | dictionary/object identity is deserialized; no new constitutional identity | snapshot reconstruction, not creation occurrence |
| Tests (`test_state_projector`, capability inventory, single-capability projection, state views, integrity summary) | hand-authored fixture values | fixture supplied plus model defaults | fixture-chosen IDs/workspaces/references | tests append `tool_need.created`; compatibility testimony only |

There is no production `ToolNeedService.create*`, runtime route, fixture/catalog
loader, CLI ingress, observation owner, serializer, or provider that creates a new
artifact. Repository-wide searches find creation-event appends only in tests.
Therefore: artifact constructible = yes; arbitrary event kind accepted by the
generic ledger = yes; creation event recorded in tests = yes; artifact projected =
yes; current non-test production occurrence witnessed = **no**.

The ledger accepts `kind: str`; it has no event-kind registry that validates
`tool_need.created`. The projector nevertheless recognizes that exact string.
No surviving production code appends it. When supplied, the creation event
preserves the ledger envelope (event identity, timestamp, actor, workspace and
optional session/causation/correlation) and the caller-provided payload. The
projector accepts either a whole nested `tool_need` mapping or a flat mapping and
requires enough recognized fields to construct a full model. Unknown artifact
fields do not survive model reconstruction. Event workspace determines inclusion
in a projected workspace, while payload `workspace_id` becomes the artifact
binding; equality is not checked. Creation-event identity does not become the
artifact ID, and `requested_by_event_id` is not automatically bound to it.

### Current implementation topology

```text
production creator: ABSENT
        X
arbitrary caller/test fixture -> ToolNeed construction (caller ID/workspace)
        X                    -> automatic creation-event recording: ABSENT
test/external generic append -> tool_need.created ledger testimony
                             -> projector recognizes nested or flat payload
                             -> State.tool_needs[id] = current ToolNeed
                             -> open/status/capability/read-model consumers

existing ToolNeed -> set_status -> FAILS before append in current runtime
                                   (intended code: status_changed -> latest status)
```

## Road B — capability resolution

`ToolNeedService.resolve_capability` takes one caller-provided representation, one
`CapabilityCatalog`, and optionally a list of arbitrary objects expected to have
`provider`, `score`, and `reasons`. It normalizes the need's `capability` only via
the catalog lookup and returns a fresh dictionary. It does not consult projected
State, registered `ToolSpec`s, policy, Approval, RiskClass, evidence, authority, or
the event ledger.

### Capability-resolution topology

```text
ToolNeed.capability -----------------------> normalized catalog lookup
CapabilityCatalog entry ------------------> known_capability boolean
                                      \----> recommendation records with backend/operation
                                             filtered into handoff-shaped metadata
caller-supplied ranked recommendations ----> provider/score/reasons copies

registered-operation owner/State --------X  (not an input)
                                         -> registered_operations = [] always

four transient components -> returned dict -> current consumers: NONE FOUND
                                              recording/emission: NONE
                                              status mutation: NONE
```

### Resolution-component matrix

| Component | Producer and input standing | Act / basis / scope | Authority and Unknowns | Consumer, preservation, standing effect |
| --- | --- | --- | --- | --- |
| `known_capability` | `_CapabilityResolution`; catalog membership for normalized `ToolNeed.capability` | boolean membership test in supplied catalog instance | metadata-presence testimony only; catalog freshness/completeness and constitutional Capability are Unknown | no caller found; transient; no status change |
| `registered_operations` | `_registered_operation_candidates` | unconditional empty list; it never reads State or ToolSpecs | no absence claim is warranted; reason is implementation stub/compatibility shape | no caller found; transient; stable returned key only |
| `provider_recommendations` | `_provider_recommendation_payload`; arbitrary caller list | copies `provider`, `score`, and `reasons`; does not filter/select | assumes attribute shape; origin, ranker occurrence, catalog relation, scope and authority are not preserved | no caller found; transient advisory representation; no selection |
| `handoff_candidates` | `_handoff_candidates`; recommendations on matched catalog entry | filters records whose `backend_type` is non-null or `operation` truthy, copies provider and present fields | external handoff-shaped metadata only; no recipient, emission, receipt, authority or realization evidence | no caller found; transient candidate metadata; no delivery/receipt/Uptake |

`registered_operations` is empty because its implementation literally returns
`[]`; `resolve_capability` has no State/Toolkit/ToolSpec input. Current evidence
supports **unimplemented compatibility field plus consumerless stable shape**,
not an intentional constitutional boundary and not a capability-absence finding.
The separate single-capability projection *does* correlate registered ToolSpec
contracts, proving such correlation has an independent owner, but that does not
retroactively populate or interpret this method.

Catalog membership != Capability standing. Provider recommendation != selection,
registered operation, authorization, or availability. Registered-operation
association != authorization. Handoff-shaped metadata != emission, delivery,
receipt, Uptake, responsibility transfer, authority transfer, or realization.
Read-only resolution != Need satisfaction, Gap closure, or status transition.
Nothing durably records a resolution invocation, payload, consumer receipt, or
consumer Uptake.

## Road C — status mutation and event recording

The signature accepts any caller holding the service, any `workspace_id`, any
`ToolNeed`, any runtime string, and optional causation ID. It does not verify that
the artifact exists in projected State, belongs to the supplied workspace, that
the caller has authority, or that the causation event exists. It declares neither
an allowed predecessor/successor graph nor warrant requirements.

In the current environment `ToolNeed` inherits Pydantic `BaseModel`, while the
method calls `dataclasses.replace`. Direct characterization with both `registered`
and an invalid `bogus` string raises `TypeError: replace() should be called on
dataclass instances`. The append is after that statement, so **the actual current
act is a failed replacement attempt**: no returned artifact and no event. There
are no dedicated current tests of this service.

The latent/intended code path remains worth characterizing without pretending it
occurs: were replacement supported by a different compatibility backend, it would
copy every field, substitute the caller string, then append
`tool_need.status_changed` with only `tool_need_id` and `status`, actor `system`,
supplied event workspace and causation ID. It contains no predecessor check,
evidence, reason, authority, request actor, transition identity, artifact workspace
check, or full artifact. Depending on compatibility validation, the Literal may
reject unknown strings while still permitting every pair among the eight known
labels. That is status replacement plus sparse lifecycle testimony production and
recording—not transition establishment or new constitutional standing.

The actor `system` is hard-coded compatibility vocabulary. It identifies neither
the calling responsibility nor evidence for a system-owned judgment, so factual
attribution remains Unknown. Status requested, type-compatible, event recorded,
transition warranted, and constitutional standing established are five distinct
claims; at present even replacement and recording are not reached.

## Road D — events, projection, and current State

### Event and projection matrix

| Event/surface | Accepted input | Reconstruction | Preservation and loss | Current claim |
| --- | --- | --- | --- | --- |
| `tool_need.created` | any ledger event with recognized string; nested whole artifact or flat mapping | constructs `ToolNeed`, applies defaults, stores by artifact `id` | known fields/current defaults survive; unknown fields lost; ledger envelope remains only in ledger; no identity/workspace/provenance validation | event says caller recorded payload; projection says a current representation was reconstructible |
| `tool_need.status_changed` | exact kind with `tool_need_id`, `status`; only acts if ID already projected | rebuilds current object from its fields with replaced status | event history remains in ledger; projected object keeps latest status only; orphan change silently has no artifact effect | accepted status testimony, not warrant |
| affected scope | either kind | collection `tool_needs`, identity from nested/flat ID or status ID | no semantic scope/authority | cache invalidation/replay locality only |
| projection snapshot | serialized entire `state.tool_needs` | `_model_dict(..., ToolNeed)` | recognized current fields only; status history and event linkage absent | cache representation, not source truth |
| `State.open_tool_needs` | current dictionary | list where status not in `{registered, rejected}` | loses no object fields but exposes no reason/order/history | implementation-local filtering convention |

Append-only status events can recover that certain payloads were recorded in
ledger order, including envelope actor/time/causation. `State.tool_needs` cannot
explain why the latest status exists, whether it followed a prior lawful status,
what evidence supported it, who actually decided it, or what authority applied.
A projected current status proves only latest recognized status representation
under replay rules. Projection can faithfully rebuild the model's **current
recognized shape** from a sufficient creation event plus changes, but not complete
historical provenance or constitutional standing.

`State.tool_needs` means an ID-indexed current compatibility projection of accepted
ToolNeed payload testimony. `open_tool_needs` means only “projected status string is
not `registered` and not `rejected`.” No active Book clause makes those the sole
terminal Need standings, and implementation enforces no lifecycle. The policy is
an implementation-local lifecycle/compatibility convention, not constitutional
Need openness, satisfaction, closure, or lawful terminality.

## Road E — public and operator-facing consumers

### Consumer inventory

| Consumer | Exact material reliance | Kind of consumption | Stronger act absent |
| --- | --- | --- | --- |
| `State.open_tool_needs` | `status`; returns full objects | filter | no transition/warrant/satisfaction |
| `build_capability_view` | `id`, `capability`, `status`, optional `requested_by_event_id` | sorts, forms status view and provenance-shaped ID list | no Capability establishment or provenance verification |
| `StateSummary` | count of `tool_needs` plus tools | count | no semantic field reliance |
| capability inventory | `capability` for every projected need (despite helper wording “unresolved”) | adds normalized/requested capability universe | no Gap/Demand/Capability proof |
| single-capability state projection | normalized `capability`, `id`, then full requested objects in JSON | correlates, sorts, serializes; CLI displays count as “demand artifact(s)” | no demand establishment, selection, verification, authorization or execution |
| capability catalog | `capability` | catalog recommendation lookup | no provider selection |
| `ToolRecommendationService` / ranker | `capability`; supplied State affects recommendation ranking | advisory ranking | no status change, registration, authorization, execution |
| projection store | every recognized field through generic serialization | snapshot serialize/deserialize | no semantic Uptake |
| rule inventory | method source and catalog entries, not an instance | documents capability-resolution rule surface | does not invoke resolution; its operation-candidate summary exceeds empty implementation |
| CLI `--single-capability-state` | projected matching objects and associated independent surfaces | operator display/JSON emission | emission does not prove receipt or Uptake |
| diagnostics/read-only capability relationship and privilege tests | snapshot/compare `open_tool_needs` to prove no mutation | boundary assertion | do not interpret fields |
| package export | `ToolNeed` symbol only | constructibility/reachability | no producer authority |

There is no current non-test consumer of `resolve_capability`'s dictionary, no CLI
that directly calls it, and no consumer that selects, authorizes, registers,
invokes, or externally realizes from it. `ToolNeedService`, `_CapabilityResolution`,
and `ToolNeedStatus` are not package exports. Tests preserve constructibility,
projection, catalog correlation, snapshot serialization, view shape, capability
inventory correlation, and read-only CLI behavior. Serialization/display is not
constitutional consumption; material filtering/correlation is the bounded local
reliance actually witnessed.

## Field-by-field characterization

All fields on ordinary construction are caller-supplied if present. “Defaulted”
below means model default, not a responsible derivation.

| Field | Producer | Source material | Copied/derived | Identity-bearing | Current consumers | Constitutional subject suggested | Stronger name implication | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | caller/payload | arbitrary string | copied, required | yes: State/scope key and status target | projector, snapshot, capability view, single-capability sorting | representation identity | stable Need identity | independently warranted representation identity; provenance under-specified |
| `workspace_id` | caller or `default` | arbitrary/default string | copied/defaulted | binding coordinate, not dictionary key | serialization/projection only | local scope | verified workspace membership | under-specified, serialized-only after replay; mismatch unchecked |
| `name` | caller | prose/slug-like string | copied | no | sort/view indirectly, serialization | presentation label | canonical subject name | faithful preservation but presentation-only |
| `summary` | caller | prose | copied | no | serialization/full requested JSON | representation summary | established requirement | serialized-only; under-specified |
| `capability` | caller | external/free string | copied; normalized only at consumers | no class identity, practical join key | catalog, ranker, inventory, views, single projection | requested desired ability / correlation vocabulary | missing constitutional Capability | mixed and compressed: catalog lookup key plus request vocabulary; no Capability standing |
| `reason` | caller | untyped prose | copied | no | serialization/full requested JSON only | attributed request rationale | Demand/Gap evidence or selection basis | under-specified, serialized-only; standing is plain caller prose |
| `requested_by_event_id` | caller/default null | optional arbitrary reference | copied/defaulted; never validated | no | capability view supporting-ID display; serialization | generic provenance hint | authoritative request/exposing event | overnamed/under-specified; proves only caller asserted a reference |
| `risk_hint` | caller/default null | optional prose | copied/defaulted | no | serialization/full requested JSON only | presentation hint | RiskClass/policy/authority input | consumerless residue except serialization; no risk standing |
| `status` | caller/default `proposed`; projector status payload | Literal-compatible label on construction | default/copy/latest fold | no, replacement retains ID | open filter, views, JSON/display | current lifecycle testimony | completed constitutional act | mixed/compressed compatibility coordinate |
| `desired_inputs` | caller/default empty | string wish list | copied/defaulted | no | serialization/full requested JSON only | capability/interface wishes | executable input schema/acceptance criterion | under-specified, serialized-only preference testimony |
| `desired_outputs` | caller/default empty | string wish list | copied/defaulted | no | serialization/full requested JSON only | capability/interface wishes | executable output schema/satisfaction evidence | under-specified, serialized-only preference testimony |

In current practice `capability` is primarily a free-string normalized correlation
and catalog lookup key. Its names/examples also suggest desired outcome ability and
mechanism/operation vocabulary; the object does not distinguish them, so the exact
constitutional subject remains an unresolved mixture. `reason` has caller-prose
standing only—not attributed Demand evidence, Gap evidence, producer rationale,
selection basis, or explanation warrant. `requested_by_event_id` proves only that
the caller supplied an optional string; the target can be any kind or absent, and
neither constructor nor consumers validate it. `risk_hint` feeds neither RiskClass,
policy nor authority. Desired inputs/outputs are caller-supplied wish lists; whether
they mean requirements, interface preferences, schema candidates, acceptance
conditions, expected evidence, or external grammar is Unknown. They are not
executable schemas or satisfaction criteria.

Fields with non-serialization semantic consumers are `id`, `capability`, `status`,
and (weakly) `requested_by_event_id`; `name` participates in deterministic sorting.
Workspace is used at construction/payload reconstruction but not checked as a
semantic binding. Summary, reason, risk hint, and desired lists are otherwise only
carried in full-object serialization/presentation.

## Status-by-status characterization

No exact producer currently succeeds through `set_status`; a constructor or
creation payload may directly supply any valid label, and a manually appended
status event may cause projector replacement. There is no implementation of
`proposed -> accepted -> generating -> generated -> validating -> validated ->
registered`, `any -> rejected`, or any other transition rule.

| Status | Exact producer | Warranting evidence / authority | Consumer reliance | Event occurrence | Implied act by name | Current standing |
| --- | --- | --- | --- | --- | --- | --- |
| `proposed` | constructor/payload or status event; default on model | none; caller controls | considered open; views/JSON | none automatically | candidate formation, external request, or unadmitted testimony | default compatibility label; meanings Unknown/compressed |
| `accepted` | same | none | open/view | only if manually appended; service currently fails | admission, operator acceptance, selection, authority, commitment | arbitrary current-label testimony; overstrong ambiguity |
| `generating` | same | none | open/view | same | builder/code generation in progress | imported workflow grammar; no occurrence evidence |
| `generated` | same | none | open/view | same | generation completed | imported workflow grammar; no artifact/result link |
| `validating` | same | none | open/view | same | structural, behavioral, Fidelity, safety, or authority review underway | compressed imported validation grammar; exact subject Unknown |
| `validated` | same | none | open/view | same | one of several verification/review completions | compressed/overnamed; no evidence, method or reviewer |
| `registered` | same | none | excluded from open; view | same | registry membership, availability, fitness, completion | implementation-local terminal label; no Capability or satisfaction standing |
| `rejected` | same | none | excluded from open; view | same | refusal/non-applicability/contradiction/failed validation/lack of authority/choice | compressed terminal label; cause and responsible refusal boundary absent |

Known-label moves are conceptually caller-controlled arbitrary replacement; there
are no partial guards beyond model Literal compatibility where construction occurs.
Current `set_status` cannot move even once due to the dataclass/Pydantic mismatch.
Tests do not preserve a transition sequence. Status recording, if a caller appends
an event directly, establishes only that the sparse status assertion was recorded;
it cannot warrant the transition or establish new constitutional standing.

The imported meanings are materially consumed only as an opaque status string and
the two-value terminal filter. No consumer performs generation, validation,
registration, refusal, selection, authorization, or external work based on a
specific intermediate label. `registered` establishes neither Capability standing
nor underlying Need satisfaction. `rejected` does not distinguish refusal from
failure, non-applicability, lack of evidence/authority, contradiction, or consumer
choice.

## Need / Gap / Demand / Capability cross-examination

| Constitutional family | Book requirement relevant here | Preserved by `ToolNeed` | Missing/Unknown | Disposition |
| --- | --- | --- | --- | --- |
| Need | bounded advancement requirement/horizon and responsible establishment; not movement | request-like name/summary/capability/reason | responsible consumer, exact requirement, horizon, establishment evidence, consequence, satisfaction | not established; candidate/request testimony at most |
| Gap | evidence-supported incompatibility/absence relative to exact reference and scope | capability string and caller reason may gesture at absence | reference condition, current condition evidence, comparison, scope, family, revision/closure | no Gap established; failed lookup would still be unknown catalog entry |
| Demand | bounded present transformation/outcome necessity supported from need/gap; not mechanism or authority | capability/desire vocabulary | necessity, temporal standing, subject, consequence, supporting Need/Gap, scope | no Demand established; CLI “demand artifact(s)” is presentation strengthening |
| Capability | evidenced ability of a subject under exact scope/limits | catalog join and recommendation metadata; ToolSpec correlation elsewhere | capable subject, evidence, ability, conditions, limits, freshness, availability/reachability | no Capability standing established |

The object preserves no exact responsible consumer, applicable requirement,
reference condition, current incompatibility evidence, material consequence,
authority, temporal standing, or satisfaction/closure criterion. It weakly preserves
caller-chosen scope via workspace and optional provenance-shaped reference, but
neither is validated. Therefore unknown catalog entry != Capability Gap; requested
mechanism != constitutional Need; desire for a tool != Demand; empty operation list
!= inability; recommendation != available Capability; `registered` != satisfied
Need.

## Identity and provenance matrix

| Question | Current evidence | Standing / limit |
| --- | --- | --- |
| Who supplies ID? | arbitrary constructor or creation-payload caller | no derivation or owner |
| Is identity derived? | no | stable representation key only |
| Does creation-event ID participate? | no | event occurrence and artifact identity remain separate |
| Does status replacement preserve it? | intended replacement copies ID; projector updates same key | same ID does not warrant same semantic standing |
| Can semantic fields change under one ID? | another creation event with same artifact ID overwrites projected object; snapshot input can differ | yes; no immutability across ledger testimony |
| Is workspace checked? | event workspace scopes replay; payload workspace becomes field; no equality check; service accepts another workspace | no lawful binding established |
| Is request reference checked? | no target existence, kind, workspace, or authority validation | optional claimed reference only |
| Is causation preserved? | status event can carry caller causation in envelope; creation has generic optional envelope causation | causation road is not reconstructed into current artifact |
| Is creation provenance preserved in object? | only optional caller field, not creation event automatically | complete historical provenance absent |

## Occurrence and durability matrix

| Coordinate | Transient | Recorded | Projected/rebuildable | Serialized/operator visible | Unknown or absent |
| --- | --- | --- | --- | --- | --- |
| direct ToolNeed construction | live object | no | only if separately appended/snapshotted | constructible/exported | production occurrence absent |
| `tool_need.created` occurrence | no after append | yes in ledger | current object rebuildable | ledger/persistence payload | non-test emitter absent |
| `tool_need.status_changed` occurrence | no after append | intended/manual append | latest status rebuildable | ledger event | service occurrence absent currently |
| projected latest ToolNeed | live/snapshot | source events separate | yes, recognized shape | state cache/views/CLI | constitutional standing absent |
| status history | ledger-resident | yes if events exist | not in current object | not shown by ToolNeed consumers | warrant/explanation absent |
| resolution payload | yes | no | recomputable from current inputs, not prior invocation | returned to hypothetical caller | invocation/receipt/Uptake absent |
| consumer receipt/Uptake | n/a | no | no | emission possible through CLI for separate projection | actual receipt/reliance Unknown |

## Responsibility-only topology

```text
caller supplies request-shaped testimony and representation identity
    -> schema construction
    -> [recording boundary absent in production]

separate recorder may preserve a creation assertion
    -> replay owner reconstructs a latest representation
    -> read-only consumers correlate, filter, count, serialize, or display it

request vocabulary + metadata catalog + advisory testimony
    -> membership result + copied advice + externally shaped route candidates
    -> [selection / authority / performance / Uptake absent]

caller asks for a lifecycle word replacement
    -> current mechanism failure
    -> [transition establishment and recording absent]
```

## Compression topology and ledger

```text
one object
  = identity + workspace hint + presentation + request rationale
  + capability correlation key + provenance hint + risk hint
  + interface wishes + opaque lifecycle testimony

one status
  = possible candidate/admission/work/generation/validation/registry/refusal words
  + projected latest representation + open/closed filter

one resolution dictionary
  = catalog membership + independent ranked advice
  + catalog route-shaped metadata + permanently empty operation slot

one latest projection
  = creation representation + folded status claims
  - transition history/warrant/explanation/authority
```

| Current carrier | Independently compressed responsibilities | Consequence |
| --- | --- | --- |
| `ToolNeed` | caller testimony preservation, candidate/request representation, capability-string correlation, lifecycle tracking | one class falsely invites one constitutional subject |
| `capability` | desired ability vocabulary, catalog key, operation/mechanism-like vocabulary | current consumers cannot recover which subject caller meant |
| `reason` | prose, possible source rationale, possible insufficiency claim | no attribution/evidence type or warranted role |
| desired lists | capability wishes, interface preferences, schema/acceptance-like vocabulary | serialized shape can look executable without being so |
| status field | candidate standing, workflow progress, review, registry, refusal | opaque latest word erases distinct acts and warrants |
| `set_status` | replacement, intended event production/recording, implied transition | implementation failure plus absent establishment boundary |
| `status_changed` payload | requested label and occurrence claim | omits before state, why, evidence and authority |
| current projection | historical append-only status testimony and current representation | latest value survives, explanation does not |
| `resolve_capability` | membership, recommendation transport, route candidates, operation slot | return adjacency can imply unified “resolution” without one result standing |
| `open_tool_needs` | lifecycle terminality and constitutional openness | implementation filter can be mistaken for Need closure |

Different responsibilities create decomposition **pressure**, not proof that new
objects should exist. Implementation shape remains Unknown.

## Negative-authority topology

```text
construction does NOT establish Need / Gap / Demand / Capability / authority
creation-event acceptance does NOT prove a responsible production road
catalog membership does NOT prove Capability
recommendation does NOT select a provider or mechanism
operation-shaped metadata does NOT register or authorize an operation
handoff-shaped metadata does NOT emit, deliver, transfer, or realize
resolution does NOT mutate status, record invocation, or satisfy anything
status label does NOT warrant a transition or named act
registered does NOT prove availability, fitness, Capability, or satisfaction
rejected does NOT establish a reasoned refusal
projection does NOT retain history explanation or establish current truth
open filtering does NOT establish constitutional openness or movement authority
CLI serialization/emission does NOT prove receipt, Uptake, or reliance
```

## Contamination ledger

Vocabulary resemblance alone is excluded. A finding requires active behavior,
producer, consumer, and strengthening.

| Suspected residue | Active field/behavior and producer | Current consumer | Semantic strengthening | Finding |
| --- | --- | --- | --- | --- |
| LLM tool-selection grammar | no `request_tool`/decision producer survives | none | none current | historical locator only, not current contamination proof |
| agent planning | `proposed`/`accepted` resemble planning | opaque status consumers only | open filter, no plan act | vocabulary residue; not materially planning |
| builder/code generation | generating/generated labels, caller/event supplied | open/view consumers | label can imply work occurrence without artifact evidence | active compressed lifecycle residue |
| tool registries | `registered`, empty operation result; caller/catalog composer | terminal filter and resolution shape | can imply membership/availability | active registry vocabulary compression; actual registry independent |
| provider routing | catalog and supplied provider recommendations | resolution has no consumer; separate recommendation ranker exists | advisory records remain unselected | active advisory behavior, bounded; not selection contamination |
| handoff/external realization | backend/operation candidate metadata from catalog | no resolution consumer | method name/payload can imply route; docstring negates execution | active external-shaped representation, no handoff act |
| approval/policy pipeline | risk hint/status words only | risk hint none; no approval input | none | resemblance/consumerless residue, not active policy behavior |
| model-visible affordances | no ToolNeed consumer exposes tools to a model | none | none | not evidenced in surviving district |
| generic request/call grammar | request-shaped fields remain; no producer/call road | read-only correlation/display | presentation calls them requested/demand | mixed compatibility residue, not current application route |

## Capability / Gap / Demand / Unknown ledger

| Pressure or absence | Responsible consumer / requirement / evidence / consequence | Classification |
| --- | --- | --- |
| direct construction works | type/serialization consumers accept model | implementation ability |
| catalog can correlate capability string | read-only metadata consumers; catalog membership evidence only | implementation ability, not constitutional Capability |
| single-capability projection correlates operations elsewhere | read-only inspection under exact normalized-string caveat | implementation ability; capability standing remains owner-dependent |
| no production creator | no identified consumer requires creation occurrence; no local operational failure shown | investigation pressure, not Gap/Demand |
| `set_status` TypeError | caller would require returned replacement/event, but no current caller or occurrence | implementation defect evidence; consumer consequence Unknown, so no constitutional Gap/Demand established |
| no transition guards/warrants | no current transition consumer/requirement established | conceptual/editorial and investigation pressure |
| empty resolution operations | no resolution consumer; method never receives operation registry | compatibility-only/consumerless residue; no inability claim |
| absent status reason/history in current State | ledger retains occurrences but no consumer requiring explanation identified | editorial/investigation pressure; no Gap automatically |
| unvalidated workspace/request reference | no responsible production consumer identified; mismatch mechanically possible | investigation pressure; constitutional consequence Unknown |
| CLI says “demand artifact(s)” | operator-facing formatter consumes request count but no demand establishment | presentation overstatement/editorial pressure |
| missing requirement/evidence/authority/scope/time | these prevent stronger classification | Unknown standing, not Gap or Demand by absence alone |
| any Capability standing in this district | no capable subject/evidence/scope/limits establishment | none established |
| any Gap standing in this district | no reference/evidence/comparison/scope establishment | none established |
| any Demand standing in this district | no present necessity establishment | none established |

## Candidate preservation and excision burden

| Piece | Current warrant / consumer burden | Candidate classification | What would be required before excision |
| --- | --- | --- | --- |
| `ToolNeed` artifact | projected/read-model/catalog/inventory/CLI/snapshot consumers and public constructibility | mixed and requires decomposition; preserve for now | consumer-by-consumer replacement or proof of no reliance; shape Unknown |
| `ToolNeedStatus` vocabulary | model validation, open filter, views/serialization | preserve but narrow; rename pressure only | recover compatibility expectations and terminal policy |
| `ToolNeedService` | no callers; houses two roads | mixed; delete-candidate pressure but not yet coherent excision | separate public/import compatibility and hidden caller search evidence |
| `resolve_capability(...)` | no callers; metadata logic and rule-inventory locator | consumerless residue / compatibility-only | confirm external API burden and rule inventory consequences |
| `_CapabilityResolution` | private, reachable only above | consumerless residue | same bounded confirmation |
| `set_status(...)` | no callers/tests; mechanically broken; latent event contract | delete-candidate pressure, current classification Unknown pending compatibility | establish whether external callers rely on method/event even though local road fails |
| `tool_need.created` | projector, scope/cache, tests, persisted-ledger compatibility | preserve but narrow; compatibility event | persistence census/migration burden and external append contracts |
| `tool_need.status_changed` | projector, scope/cache, latent service, persistence compatibility | preserve but narrow; compatibility event | persisted-event/external-producer evidence and replay impact |
| `State.tool_needs` | many read-only consumers and snapshot shape | preserve; mixed representation collection | independent consumer migration evidence |
| `State.open_tool_needs` | direct filters and mutation-boundary tests | preserve but narrow | recover public callers and replace local terminal convention |
| package export `ToolNeed` | public import/constructibility | compatibility-only but preserve | external compatibility evidence/versioned removal boundary |
| CLI/API surfaces | single-capability projection serializes/correlates ToolNeeds; no direct resolution API | preserve but narrow | operator contract and diagnostic visibility consequences |
| dedicated tests | no current `test_tool_needs.py`; distributed tests preserve projection/correlation | preserve distributed compatibility testimony | do not delete without affected-surface changes |

No bounded implementation excision is already warranted: the obvious no-caller
service seam is entangled with public-module compatibility, projector event
contracts, the rule inventory's claimed behavior, and possible persisted/external
events, while the artifact and State fields have active consumers. Responsibility
decomposition is warranted as a **characterization**, but implementation
decomposition shape remains Unknown. This report does not propose `CapabilityNeed`,
`NeedLifecycle`, `DemandResolution`, a registry, a workflow, or a transition engine.

## Direct answers

1. **Current constructors:** arbitrary direct model callers; creation-event replay
   in `StateProjector`; projection snapshot loading; and test fixtures. Only the
   first constructs without prior serialized testimony; none is a responsible
   production ingress.
2. **Non-test production occurrence:** none evidenced.
3. **Is `tool_need.created` emitted?** Not by surviving production code; tests append it.
4. **Creation-event preservation:** generic ledger envelope plus caller payload;
   replay recognizes nested/full or flat payload. It does not establish producer
   authority or bind event identity to artifact identity/provenance.
5. **New-object standing:** caller-supplied schema-valid request-shaped
   representation/candidate testimony only.
6. **Family:** mixed capability-related request representation; constitutional
   Need, Gap, Demand, mechanism request, and Capability request standing are each
   Unknown/not established. Mechanism-like readings are possible but unwarranted.
7. **Caller supplied:** all required fields and every optional field when present.
8. **Derived:** none. Workspace/status/nulls/empty lists may be defaulted; consumer
   normalization is not artifact derivation.
9. **Identity:** `id` is the State/status target key; `workspace_id` is a claimed
   binding coordinate. Creation-event ID and request reference do not produce identity.
10. **Non-serialization consumers:** `id`, `capability`, `status`, optional request
    reference, and `name` for sort; object count also contributes to summaries.
11. **`capability`:** current free-string catalog/correlation key with unresolved
    desired-ability/mechanism/operation vocabulary mixture.
12. **`reason`:** untyped caller prose only.
13. **Request event reference:** only that caller asserted an optional string; it
    proves no kind, occurrence, causation, request authority, or workspace relation.
14. **Risk hint:** not consumed as risk standing or authority input.
15. **Desired I/O:** caller wish lists; exact requirement/schema/preference meaning
    Unknown, with preference testimony the narrowest warranted reading.
16. **Resolution act:** transient read-only catalog membership, recommendation
    copying, catalog recommendation filtering, and an empty compatibility slot.
17. **Standing change:** none.
18. **Empty operations:** implementation returns `[]` and has no registry input;
    best classified unimplemented, consumerless compatibility shape.
19. **Provider standing:** copied advisory, unselected representation; independently
    supplied ranked material is not proven catalog testimony.
20. **Handoff candidates:** filtered external route-shaped catalog metadata only.
21. **Resolution selection/authority/realization:** none; no current consumer exists.
22. **`set_status` act:** currently a failed replacement attempt; latent code would
    be caller-controlled replacement plus sparse event append.
23. **Transition validation:** absent; current method fails before transition.
24. **Arbitrary moves:** no move works in the present backend. Latent logic permits
    every pair of type-compatible labels with no predecessor guard.
25. **Status warrant:** none of the eight preserves evidence or authority.
26. **Recording and standing:** sparse recording would not establish warrant or
    constitutional transition standing.
27. **History in projection:** no; only ledger retains event sequence.
28. **Projected status proof:** latest recognized status testimony under replay only.
29. **Open meaning:** current status is not exactly `registered` or `rejected`.
30. **Terminal policy:** implementation-local lifecycle/compatibility convention.
31. **Imported labels:** proposed/accepted import candidate/planning/admission;
    generating/generated builder workflow; validating/validated review/verification;
    registered registry; rejected refusal/choice.
32. **Material consumption:** opaque display for all and open/closed filtering for
    registered/rejected only; none of the named acts is performed.
33. **Registered -> Capability:** no.
34. **Registered -> satisfaction:** no.
35. **Rejected causes:** not distinguished.
36. **One coherent subject:** no exact single constitutional subject is warranted;
    it is one mixed compatibility representation.
37. **Compressed responsibilities:** testimony/candidate representation, identity,
    scope hint, capability correlation, rationale/provenance/risk/interface wishes,
    workflow/current-state labels, event testimony, and latest projection.
38. **Independently warranted:** representation identity, immutable constructibility,
    generic recording/replay compatibility, capability-string correlation,
    read-only catalog advice, snapshot/view serialization, and local status filtering.
39. **Compatibility/serialization only:** most prose/risk/interface fields;
    resolution operation slot; package export; lifecycle semantics beyond filtering;
    service roads have no local consumers.
40. **Capability standing:** none.
41. **Gap:** none.
42. **Demand:** none; presentation calls it demand without establishment.
43. **Unknowns:** original/request producer, responsible consumer, exact subject of
    capability/reason/I/O, requirement/reference/evidence/consequence, authority,
    time/scope, satisfaction, lifecycle acts, external API/persisted-event reliance,
    receipt/Uptake, and proper decomposition shape.
44. **Bounded excision now:** no coherent safe implementation excision is established.
45. **Decomposition:** responsibility distinctions warrant decomposition pressure;
    implementation form remains Unknown.
46. **Smallest next honest operation:** perform one bounded **external and persisted
    compatibility occurrence audit** of the no-local-caller service/event seam:
    determine whether any supported external caller or existing ledger depends on
    `ToolNeedService`, its status event, or resolution payload. Stop at evidence;
    do not design replacements or change behavior.

## Protected neighbors and stop

`CapabilityCatalog` remains independent read-only metadata testimony; capability
inventory remains its own current-state interpretation; provider recommendations
remain advisory; `ToolSpec`/`Toolkit` and registered-operation indexing remain
contract/registry neighbors; Approval/RiskClass remain independent authority/risk
districts; `HandoffBackendType` remains external-shaped metadata; ExecutionStatus
is not characterized; Demand-family projections, `BoundedOperatorGoalEstablishment`,
and `BoundedAdvancementHorizon` retain their own standing. No conclusion here
prejudges, modifies, or supplies a design for any of them.

The stopping rule is met. The current surviving district is characterized, and no
production implementation, lifecycle, event payload, projection, CLI, Book clause,
or protected neighbor is amended.

## Reproduction and validation record

Repository searches covered all requested names plus constructor/event append,
snapshot, view, inventory, recommendation, rule-inventory, CLI, package-export,
diagnostic, fixture, and documentation occurrences. Mechanical characterization
also directly exercised valid and invalid `set_status` requests and a creation
payload whose event workspace, artifact workspace, and unknown field differed.
Focused tests covered catalog, events, State replay, projection persistence/shape,
capability inventory and recommendations, capability/state views, single-capability
CLI/JSON, diagnostics, and CLI behavior. Final repository checks confirmed this
report is the only changed path.
