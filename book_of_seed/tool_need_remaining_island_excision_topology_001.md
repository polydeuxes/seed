# ToolNeed Remaining-Island Excision Topology 001

## Boundary, witnesses, and finding

This is one bounded, report-only recovery at merged-main commit `65bbfae` (PR
1987). It creates only this report. It does not change implementation, tests,
fixtures, schemas, serialization, exports, commands, events, projections, canonical
Book chapters, earlier reports, or archived testimony. The active Book is the
constitutional grammar witness; current code is mechanical testimony; PR 1986's
report is immutable characterization testimony; and PR 1987 proves that the
consumerless `ToolNeedService` district and its false registered-operation rule
entry were independently removable.

**Answer.** No independently warranted constitutional responsibility found in
the repository requires the surviving `ToolNeed` artifact by identity. The
island is a producerless compatibility carrier with several read-only satellites
attached to independently useful capability, projection, inventory, summary, and
diagnostic responsibilities. Those responsibilities generally remain coherent
without their ToolNeed branches. Absence of a producer is not by itself deletion
warrant; the actual excision pressure is the recovered dependency topology:
remove presentation/correlation adapters first, then counts and the lifecycle
filter, then snapshot/projection compatibility, then event replay and affected
scope, and only then the collection, status alias, model, and package export.

Repository searches confirm the fixed post-1987 boundary: `seed_runtime/tool_needs.py`,
`ToolNeedService`, `resolve_capability`, and `set_status` are deleted; no current
source imports them. PR 1987 also removed
`capability_resolution.registered_operation_candidates`. The remaining rule
inventory wording is catalog-derived recommendation metadata, not the deleted
false registered-operation entry.

No finding below promotes request vocabulary into Need, Gap, Demand, Capability,
selection, authorization, movement, generation, validation, registration,
refusal, or satisfaction. Public constructibility, replayability, projection,
and test fixtures are different kinds of testimony.

## I. Current surviving island

### Topology 1 — current road

```text
current responsible ToolNeed creator -------------------------------- ABSENT
current responsible ToolNeed event emitter --------------------------- ABSENT

arbitrary Python caller -> ToolNeed(...) (constructibility only) ------+
generic/manual ledger input -> tool_need.created ----------------------+-> StateProjector
old/current event replay -> recognized creation/status event ----------+      |
snapshot payload -> state_from_payload --------------------------------+      |
                                                                               v
                                  State.tool_needs[id] = latest ToolNeed
                                      |         |             |
                         open status filter     |             +-> snapshot write
                                                |
        +--------------------+------------------+--------------------+
        v                    v                  v                    v
 capability view       capability inventory   single-capability   state summary
 id/name/status/        capability string      projection           count
 request-event id             |               full matching needs
                              v                     |
                        integrity summary            v
                        capability counts       CLI text / JSON

ToolNeed argument -> CapabilityCatalog.recommend_for -> recommendations
ToolNeed + State -> ToolRecommendationService -> string-based ranker -> ranked list
catalog entries -> rule inventory ToolNeed.capability condition -> CLI/JSON
```

The only current ingresses are (1) arbitrary direct construction, including via
the package export, (2) caller-supplied generic ledger events subsequently
recognized by replay, and (3) snapshot reconstruction. None identifies a current
production owner. `StateProjector` is ingestion/replay, not production; the
generic ability of `EventLedger.append(kind: str, ...)` is not a ToolNeed event
producer.

### Producer and occurrence inventory

| Occurrence | Classification | Non-test owner? | Result / boundary |
| --- | --- | ---: | --- |
| `ToolNeed(...)` in model definition/import clients | direct construction | no production construction found | In-memory caller-authored object only. |
| `tool_need.created` in `StateProjector.apply` | event ingestion/replay | no emitter | Reconstructs and overwrites current dictionary entry. |
| `tool_need.status_changed` in `StateProjector.apply` | event ingestion/replay | no emitter | Replaces status only when an object already exists. |
| `_recover_affected_scope` branches | replay/cache locality metadata | no | Names collection and identity; produces no artifact/event. |
| `state_from_payload(..., ToolNeed)` | snapshot reconstruction | no | Rebuilds cached current objects. |
| tests constructing objects/appending creation events | test fixture | no | Distributed compatibility testimony. |
| PR 1986 and older reports | historical testimony | no | Locators/characterization only. |
| `ToolNeedService` roads | deleted historical implementation | no | PR 1987 removed service and its only intended status emitter. |

No example or production fixture outside tests was found constructing or storing a
ToolNeed. No production append of either event kind was found.

### Creation-event road

`payload.get("tool_need", payload)` chooses a nested mapping when the key exists,
otherwise the entire flat payload. `ToolNeed(**data)` requires `id`, `name`,
`summary`, `capability`, and `reason`. It defaults `workspace_id="default"`,
`status="proposed"`, `requested_by_event_id=None`, `risk_hint=None`, and both
desired lists empty. Recognized supplied optional fields survive. Model-extra
behavior governs unknown fields (current reconstruction does not create a new
coordinate for them); event-envelope actor, timestamp, causation, correlation,
session, and event ID are ignored by this model branch.

The payload's `workspace_id`, not the event envelope, binds the object, and no
equality check exists. The event's workspace controls which ledger stream is
replayed. Artifact identity is caller-supplied `id`; event identity is not adopted
and `requested_by_event_id` is not derived. Assignment is
`state.tool_needs[need.id] = need`, so duplicate IDs silently overwrite the
projected current value in replay order. Missing required data, malformed model
data, or invalid status raises model/key validation through replay rather than
being locally caught. A malformed nested `tool_need` value likewise fails model
construction. A valid event changes inventory/view/projection/summary outputs and
snapshot shape through the new current entry.

Affected scope for either event is collection `tool_needs`; creation identity is
nested/flat `id`, while status identity falls back to `tool_need_id`. Missing
identity can yield a scope whose identity is `None`; the metadata supplies cache
locality, not semantic authority.

### Status-event road

The status branch requires `payload["tool_need_id"]`; absence raises `KeyError`.
If the ID is unknown, replay silently does nothing. If present, it rebuilds a full
`ToolNeed` from the current object's attributes plus `payload["status"]`.
`ToolNeedStatus`/model validation rejects values outside the eight literals.
Every recognized predecessor can mechanically be replaced by every valid status:
there is no transition graph.

The event ledger preserves event history and envelope, but the projected object
preserves only latest status. The current object carries no before-status,
transition reason, transition evidence/authority, actor, event ID, time, or
causation. `requested_by_event_id` remains creation-payload testimony and is not
changed. Thus the only consumer-visible consequences are latest-status display,
the `registered`/`rejected` terminal filter, full-object serialization, and
snapshot replacement. There is no current runtime operation that changes a
ToolNeed because no current production emitter remains.

## II. Complete direct-consumer inventory

| Consumer | Material consumed | Exact local act | Output / standing | Independent responsibility | Other inputs | Branch classification |
| --- | --- | --- | --- | --- | --- | --- |
| `StateProjector.apply` creation | recognized full payload | construct, key by `id`, overwrite | current representation | generic event projection | all other event families | replay compatibility only |
| `StateProjector.apply` status | ID/status + current full object | lookup and latest replacement | current status representation | generic event projection | all other event families | replay compatibility only |
| `_recover_affected_scope` | event kind and ID | collection/identity metadata | incremental replay locality | generic scoped projection | other event branches | optional compatibility branch |
| `State.tool_needs` | full objects | dictionary storage | projected collection | generic current State | many independent collections | compatibility carrier |
| `State.open_tool_needs` | full collection; `status` | exclude `registered`,`rejected` | full-object list | none beyond local lifecycle filter found | none | producerless satellite |
| projection serializer | full dictionary/objects | `to_plain` | snapshot field | generic snapshot persistence | every State field | serialization-only branch |
| projection loader | full serialized objects | `_model_dict` | reconstructed dictionary | generic snapshot reconstruction | every State field | snapshot compatibility branch |
| projection shape | field name | declares collection | shape metadata | generic projection-shape description | other State collections | compatibility-only |
| capability view | `id`, `capability`, `status`, `requested_by_event_id`; `name` only sort | emit `CapabilityView` | capability-labeled presentation | capability view remains for ToolSpecs | tools | presentation/correlation branch |
| state summary | collection length | add to `len(tools)` | `capabilities_count` | compact state summary | facts/goals/tools/issues | count-only, strengthening |
| capability inventory | every `capability` string | union into universe | often `unverified` entry absent fact | evidence/contract capability inventory | ToolSpecs, verification facts/support | optional input branch; stronger wording |
| integrity summary | inventory entries transitively | count verification states | capability-state counts | integrity aggregation | facts/evidence/issues | transitive optional branch |
| catalog adapter | `capability` only | normalized `get`, copy list | recommendations | catalog exact-string lookup is independent | catalog entries | ToolNeed-specific adapter |
| `ToolRecommendationService` | `capability` only; identity as parameter type | catalog adapter then rank | transient ranked recommendations | generic ranker/catalog are independent | State runtime/platform/provider facts | ToolNeed-specific adapter |
| recommendation ranker | capability string, not object | capability labels reasoning; score from recommendations/State | transient ordered records | independent generic ranking | providers, tools, entities, facts, risk/default order | no direct ToolNeed dependency |
| single-capability projection | normalized `capability`, `id` sort, then full objects | correlate and serialize `requested` | request list/count, “demand artifact(s)” | independent correlation of catalog, operations, evidence, inventory | protected owner artifacts | optional presentation branch |
| diagnostic inventory | diagnostic name/metadata only | register projection command | discoverability | independent registry | other diagnostics | transitive to ToolNeed branch only |
| diagnostic shape audit | module/build/format/JSON functions | shape/read-only checks | audit result | independent audit | projection surface | transitive to ToolNeed branch only |
| rule inventory | literal wording `ToolNeed.capability`; catalog entries | produce conditions per catalog entry | rule report/CLI JSON | catalog-rule inventory | catalog | presentation-only ToolNeed wording |
| CLI state/capability views | derived view/count | format | operator text/JSON | generic operator representation | view objects | transitive |
| CLI capability inventory/integrity | derived inventory/counts | format | operator text/JSON | generic diagnostics | inventory | transitive |
| CLI single capability | projected object | format / `to_plain` | count and full JSON | independent multi-source diagnostic | catalog/evidence/tools | transitive ToolNeed branch |
| package `__init__` | class symbol | re-export | import constructibility | package API aggregation | many exports | compatibility-only |

`inquiry_orientation`, capability-relationship, and privilege-discovery production
logic do not consume ToolNeeds; their tests compare empty/open collections solely
to prove unrelated operations do not mutate them. They are test-only satellites,
not production consumers. There is no current `seed_runtime/state_summary.py`
ToolNeed reference; current filenames are `state_views.py`,
`integrity_summary.py`, and `state_summary_views.py` (the latter has no direct
ToolNeed coordinate). There is no current `recommendation_ranker.py` object read.

## III. Consumer asymmetry

### `open_tool_needs`

The property performs exactly:

```text
State.tool_needs.values()
 -> status not in {"registered", "rejected"}
 -> list of complete objects in dictionary iteration order
```

No non-test caller was found. Tests call it once to demonstrate replay and in two
unrelated read-only invariance checks. Nothing uses it for movement, selection,
authorization, work, constitutional Need openness, or closure. Removing it would
remove an implementation-local lifecycle filter, not an independent responsibility.

### Capability view

The branch sorts on `capability`, `name`, `id` and emits `id` as capability ID,
`capability` as name, latest `status`, and optional `requested_by_event_id` as a
supporting event. It does not emit summary/reason/risk/I/O/workspace/full object.
The shared view also independently represents `ToolSpec` records, so the view is
meaningful without ToolNeeds. Its ToolNeed branch mixes request correlation,
status presentation, and generic provenance display and is removable independently.

### Capability inventory and integrity

ToolNeed capability strings join three distinct sources: ToolSpec-declared
operation-contract labels, evidence-supported `capability_verified` subjects, and
requested strings. Catalog-declared capabilities are not added by this inventory.
The source distinction disappears in output. With no support fact, a ToolNeed-only
string becomes `state="unverified"` with reason “no capability_verified fact is
present”; this wording strengthens “requested string” into an apparent capability
requiring verification. It does not say “missing” or “demanded,” but “unresolved
needs” in helper prose and `unverified` imply stronger standing than the input.
Downstream integrity counts do not distinguish source. Removing requested strings
leaves a coherent inventory over operation-contract metadata and admitted
verification subjects; integrity remains coherent with changed counts.

### Catalog adapter and recommendation ranking

`CapabilityCatalog.get(capability: str)` already supplies normalized exact-string
lookup. `recommend_for(tool_need)` uses only `tool_need.capability`, adds no act
beyond get-and-copy, and its output is not durably preserved. Its direct callers
are tests and `ToolRecommendationService`. That service likewise consumes only
the string and forwards it to the generic ranker. The ranker never reads
`State.tool_needs`: presence of projected ToolNeeds does **not** change scores.
Scores derive from registered-provider names, runtime/platform facts, lower risk,
and catalog ordering. The ranker's independent responsibility exists without
ToolNeed; the service/catalog overloads are identity-specific optional adapters.
Rank increase is not candidate/provider selection, Capability, or authorization.

### Single-capability projection

The ToolNeed branch matches normalized capability, sorts by `id`, stores full
objects in `requested`, serializes every field in JSON, and emits only their count
in text: `requested: N demand artifact(s)`. Its boundary note also says
`requested_state_proves_demand_only`. That language strengthens caller-authored
request testimony into Demand, although no bounded necessity is established.
The projection remains coherent over catalog membership/recommendations,
ToolSpec contract associations, candidate evidence, verification evidence,
inventory status/freshness, and Unknowns without this branch. The diagnostic
inventory and shape audit require the overall registered surface and read-only
shape, not ToolNeed identity as an independently justified coordinate.

### Summaries, diagnostics, and rule inventory

`StateSummary.capabilities_count` counts ToolNeeds plus tools and therefore treats
each carrier as a capability count. The CLI prints that count. Integrity summary
counts ToolNeed-origin inventory states transitively. The single-capability
diagnostic emits the full `requested` JSON and count-only text; its registry and
shape audit assert discoverability/functions/read-only metadata. None establishes
Need or Capability standing. Removing each ToolNeed coordinate preserves the
summary/diagnostic responsibility with a narrower input/output shape.

Rule inventory independently reports catalog rules, but conditions currently say
`ToolNeed.capability is ...`. After service deletion this wording has no live rule
producer and is a presentation-only satellite; catalog entries and
`CapabilityRecommendation` remain protected.

## IV. Consumer dependency and satellite graphs

### Topology 2 — every direct and transitive `State.tool_needs` consumer

```text
State.tool_needs
 +-> open_tool_needs -> tests proving replay/non-mutation
 +-> build_capability_view -> CLI text/JSON and StateSummary comparison tests
 +-> build_state_summary -> CLI/operator summary + summary cache representation
 +-> _requested_capabilities -> capability inventory
 |                              +-> CLI inventory
 |                              +-> integrity summary -> CLI integrity
 |                              +-> single-capability verification state/freshness
 +-> single-capability requested correlation
 |      +-> projection dataclass -> JSON full objects
 |      +-> formatter -> “demand artifact(s)” count
 |      +-> diagnostic inventory / diagnostic shape audit / CLI
 +-> state_to_payload -> projection snapshot persistence

StateProjector event branches -> State.tool_needs (producer of projection only)
state_from_payload ------------> State.tool_needs (snapshot reconstruction only)
projection_shape --------------> declares its shape (metadata, not value read)
```

Catalog and recommendation adapters consume a `ToolNeed` argument directly but
are not downstream of `State.tool_needs`; no current production caller connects
the projected collection to them. Rule inventory references its type vocabulary
but not the collection.

### Topology 3 — responsibility-only graph

```text
event replay locality -> current-state projection -> cache persistence

operation-contract metadata ----+
evidence-admitted subjects ------+-> capability inventory -> integrity counts

catalog metadata -> exact-string recommendation lookup -> optional ranking
runtime/platform/provider facts --------------------------^

catalog + operation contracts + candidate/evidence owners
 -> one-string read-only diagnostic -> operator text/JSON

projected facts/goals/tools/issues -> compact state views/summaries -> operator output
diagnostic registry -> discoverability and shape/read-only audit
```

Every responsibility in this graph can exist without a request-shaped artifact.
This report does not redesign its inputs or outputs.

### Topology 4 — satellites

```text
generic projector/persistence -------- [ToolNeed event/field/model branches]
capability view ----------------------- [ToolNeed-to-CapabilityView adapter]
capability inventory ------------------ [requested-string universe input]
integrity summary --------------------- [counts caused by that input]
catalog lookup ------------------------ [ToolNeed-typed get adapter]
generic recommendation ranking -------- [ToolRecommendationService adapter]
single-capability diagnostic ---------- [requested/full-object/count branch]
state summary ------------------------- [ToolNeed count addend]
catalog rule inventory ---------------- [ToolNeed condition wording]
package API --------------------------- [ToolNeed export]
tests --------------------------------- [construct/replay/preserve branches]
```

### Topology 5 — circular-preservation graph

```text
ToolNeed -> capability-view branch -> “consumer exists” -> ToolNeed
ToolNeed -> requested inventory input -> inventory coverage -> ToolNeed
ToolNeed -> projected collection -> snapshot field -> replayability -> ToolNeed
ToolNeed -> package export -> tests construct export/model -> compatibility -> ToolNeed
ToolNeed -> single-capability request branch -> diagnostic shape tests -> ToolNeed
```

These loops show compatibility preservation, not independent constitutional
warrant. They are insufficient alone to prove deletion safe as an external API
matter, which remains Unknown outside repository evidence.

## V. Field-to-consumer matrix

| Field | Direct consumers after PR 1987 | Exact-field need? | Consumer works without branch? | Excision burden |
| --- | --- | ---: | ---: | --- |
| `id` | projector key; status lookup indirectly; capability view ID; single projection sort | yes locally | yes | remove adapters before model |
| `workspace_id` | full snapshot/JSON only | no semantic read | yes | serialization-only |
| `name` | capability-view sort; full snapshot/JSON | only deterministic sort | yes | presentation/serialization |
| `summary` | full snapshot/JSON only | no | yes | serialization-only |
| `capability` | view; inventory; catalog adapter/service; single projection; rule wording | yes | yes, except adapter becomes empty | highest consumer-branch burden |
| `reason` | full snapshot/JSON only | no | yes | serialization-only |
| `requested_by_event_id` | capability view provenance; full snapshot/JSON | yes locally | yes | presentation/provenance branch |
| `risk_hint` | full snapshot/JSON only | no | yes | serialization-only |
| `status` | open filter; status replay; capability view; full snapshot/JSON | yes locally | yes | lifecycle/display compatibility |
| `desired_inputs` | full snapshot/JSON only | no | yes | serialization-only |
| `desired_outputs` | full snapshot/JSON only | no | yes | serialization-only |

Only `id`, `name`, `capability`, `requested_by_event_id`, and `status` have direct
non-serialization reads. Workspace, summary, reason, risk hint, and desired I/O
survive solely because full-object event/snapshot/single-projection serialization
carries them.

## VI. Status-use matrix

| Status | Explicit branch consumer | Generic display | Open/closed consequence | Other consequence | Excision burden |
| --- | --- | ---: | --- | --- | --- |
| `proposed` | model default only | yes | open | validation/serialization | alias/model compatibility |
| `accepted` | none | yes | open | validation/serialization | display-only |
| `generating` | none | yes | open | validation/serialization | display-only |
| `generated` | none | yes | open | validation/serialization | display-only |
| `validating` | none | yes | open | validation/serialization | display-only |
| `validated` | none | yes | open | validation/serialization | display-only |
| `registered` | `open_tool_needs` terminal set | yes | excluded | ToolSpecs separately display same word | filter + display |
| `rejected` | `open_tool_needs` terminal set | yes | excluded | none | filter + display |

The five intermediate values have no branch behavior beyond accepting,
serializing, and displaying a value; `proposed` additionally defaults. Exactly
`registered` and `rejected` mechanically matter by excluding the object from the
otherwise unused `open_tool_needs` list. Neither causes registration, refusal,
satisfaction, or any other state transition.

## VII. Event, projection, persistence, fixtures, and exposure

### Event/projection compatibility matrix

| Surface | Producer | Consumer | Checked-in fixture | Absence tolerated? | Unrelated effect if removed | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `tool_need.created` | none | projector/scope | tests append | yes; replay has no required event | remove one recognized branch only | replay/test compatibility |
| `tool_need.status_changed` | none | projector/scope | no append found | yes | remove one recognized branch only | replay compatibility only |
| `State.tool_needs` | replay/snapshot loader | listed branches | direct test objects | default empty | State shape changes | active read-only compatibility road |
| `open_tool_needs` | collection property | tests only | test assertions | yes | none in production | test-preserved/consumerless |
| snapshot field | serializer | loader | tests cover general snapshot, no nonempty checked-in snapshot | loader defaults missing to `{}` | schema/cache shape only | snapshot compatibility |
| affected scope | event kinds | incremental projection machinery | scope unit test | absence of events tolerated | only those event invalidations | replay compatibility |
| projection-shape declaration | static metadata | shape/audit machinery | shape tests | runtime State defaults without events | declared shape changes | compatibility metadata |

Replay tolerates complete absence of both events and produces an empty collection.
Removing the ToolNeed branch need not change unrelated event application, but an
implementation operation would need coordinated tests/version handling rather
than pretending each lower layer is already consumerless.

### Snapshot and fixture burden matrix

| Evidence | Nonempty ToolNeed? | What it proves | What it cannot prove |
| --- | ---: | --- | --- |
| `state_to_payload` | possible | writes dictionary under `tool_needs`, full recognized fields | an external deployment exists |
| `state_from_payload` | possible | `_model_dict(payload, "tool_needs", ToolNeed)`; missing field becomes empty | unknown-field or external migration contract |
| projection version checks | generic | mismatched stored projection versions trigger existing invalidation/replay policy | ToolNeed-specific version promise |
| checked-in non-test JSON/YAML snapshot/fixture search | none found | no repository-local persisted nonempty burden | external absence |
| distributed Python tests | yes, ephemeral | current model/replay/view/inventory/diagnostic compatibility | production occurrence |
| old reports | historical examples | immutable testimony | active fixture/contract |

Snapshot output always includes `tool_needs`, even empty. Loading an absent key
returns `{}`. Unknown top-level fields are ignored by this loader; object unknown
fields follow the model compatibility behavior. The snapshot carries its generic
`projection_version`; there is no ToolNeed-specific snapshot version. No external
database or migration burden is evidenced, and none is inferred.

### Package/API exposure matrix

| Surface | Internal importer/caller | Documentation | CLI/API | Tests | Standing |
| --- | --- | --- | --- | --- | --- |
| `seed_runtime.models.ToolNeed` | projector/store/catalog/single projection/service adapter | implementation and reports | objects appear transitively in diagnostic JSON | many distributed tests | internal compatibility model |
| `from seed_runtime import ToolNeed` | no non-test internal importer found | package `__all__`; no active user guide promise found | Python import only | architecture/export coverage may enumerate package surface | constructibility compatibility, not producer |
| `ToolNeedStatus` | model annotation | no package export | no independent CLI/API | status fixtures indirectly | internal type alias |
| events | projector only | historical reports | generic ledger can accept strings; no dedicated command/API | creation replay tests | producerless replay compatibility |

The root export is a mechanically public symbol but repository evidence does not
show documented supported use or a production authority. Unsupported external
direct consumers remain Unknown and were not audited.

## VIII. Satellite, circular, terminology, and standing ledgers

### Satellite versus independent-responsibility matrix

| District | Would exist without ToolNeed? | Classification | Coherent without branch? |
| --- | ---: | --- | ---: |
| projector/persistence | yes | generic support with compatibility branch | yes |
| capability view | yes, for ToolSpecs | independent consumer + removable branch | yes |
| capability inventory | yes, facts/ToolSpecs | independent consumer + optional input | yes |
| integrity summary | yes | independent transitive consumer | yes |
| catalog | yes | independent catalog + typed adapter | yes |
| ranker | yes | independent; receives only string transitively | yes |
| `ToolRecommendationService` | no evidenced role beyond ToolNeed adapter | producerless satellite | removing whole adapter is coherent after caller check |
| single-capability projection | yes, many owners | independent diagnostic + removable branch | yes |
| state summary | yes | independent + count-only branch | yes |
| rule inventory | yes, catalog rules | independent + stale type wording | yes |
| `open_tool_needs` | no independent caller/act | ToolNeed-only satellite | yes |
| package export/tests | no substantive responsibility | compatibility/test satellites | n/a |

### Circular-preservation ledger

| Argument | Circle | Independent evidence | Finding |
| --- | --- | --- | --- |
| Keep model because view reads it | model creates view branch; branch exists for model | view also represents ToolSpecs | circle does not preserve branch |
| Keep model because inventory counts it | model supplies requested universe; helper exists to ingest it | facts/ToolSpecs independently warrant inventory | optional branch only |
| Keep model because snapshots serialize it | projection creates snapshot field; loader restores projection | generic snapshots independently warranted | compatibility burden, circular constitutionally |
| Keep model because tests construct it | compatibility surface prompts fixtures; fixtures preserve surface | no production occurrence | test-only support |
| Keep status because open filter uses it | status family creates filter; filter has no production caller | none | pure satellite loop |
| Keep requested diagnostic because audit checks it | diagnostic branch creates shape; audit preserves declared branch | diagnostic independently warranted | remove branch and update its declarations/tests together |

### Active terminology ledger

Repository-wide searches used all required spellings. Results are classified by
context rather than by filename alone.

| Term/location family | Classification | Standing effect |
| --- | --- | --- |
| `ToolNeed`, `tool_need`, `tool_needs`, events in runtime | implementation reference | none beyond mechanics |
| capability inventory “ToolNeeds”, “requested”, “unresolved needs” | implementation/operator strengthening | request string can appear as unverified capability |
| single projection `requested` and “demand artifact(s)” | operator-facing strengthening | strongest unwarranted Demand wording |
| boundary note `requested_state_proves_demand_only` | operator-facing strengthening/negative qualifier | still calls request state Demand |
| capability view/status/count | implementation/operator presentation | Capability-label strengthening |
| rule condition `ToolNeed.capability` | stale implementation wording | catalog recommendation condition only |
| tests named need/requested/status | test description | compatibility only |
| PR 1986 and other numbered reports | historical testimony | immutable, not active law |
| canonical Book Need/Gap/Demand/Capability English | Book law or generic constitutional grammar | does not name/require implementation object |
| unrelated generic “tool need” prose | generic English/historical locator | no implementation dependency |

No canonical Book chapter was found requiring `ToolNeed` by implementation
identity. Book discussions of Need, Gap, Demand, and Capability impose distinctions
rather than providing automatic standing to a similarly named object.

### Capability / Gap / Demand / Unknown ledger

| Pressure/claim | Exact evidence | Classification | Consequence |
| --- | --- | --- | --- |
| Runtime can construct/replay/serialize artifact | model/projector/store | implementation ability | compatibility exists; not Capability |
| Request string enters inventory | `need.capability` union | excision + editorial pressure | optional universe input; not Gap/Demand |
| Missing producer | exhaustive non-test search | excision pressure | motivates topology recovery only |
| No `capability_verified` fact for requested string | inventory assigns unverified | evidence absence | not constitutional incompatibility/Gap |
| Catalog match/recommendations | exact normalized string metadata | implementation ability | not Capability/selection |
| `demand artifact(s)` text | formatter count | editorial pressure | overstates request testimony |
| Old event/snapshot acceptance | projector/store | compatibility pressure | local compatibility burden |
| Need/Gap/Demand/Capability standing | no establishing owner/act found | Unknown/absent current evidence | no constitutional preservation warrant |
| External stored events/snapshots/import clients | not in repository | Unknown | cannot claim zero external burden |

There is no present evidence of an incompatibility against a declared reference
condition and scoped consequence, so no Gap is established. There is no bounded
necessary transformation, so no Demand is established. There is no admitted
ability/standing produced by ToolNeed consumers, so no constitutional Capability
is established. The pressure is faithful excision and local compatibility cleanup,
not a Demand to invent a replacement.

## IX. Artifact/event disposition and deletion topology

### Candidate disposition matrix

| Candidate | Current disposition | Why / prerequisite |
| --- | --- | --- |
| capability-view branch | coherent immediate excision candidate | independent view remains; remove tests/output expectations |
| inventory requested-string branch | coherent immediate excision candidate | independent sources remain; update transitive counts/tests |
| catalog `recommend_for(ToolNeed)` | coherent immediate excision candidate | `get(str)` exists; direct tests/service adapter affected |
| ranker ToolNeed branch | preserve (none exists) | ranker is already string-based/independent |
| `ToolRecommendationService` | producerless compatibility support | remove with/after catalog adapter; no callers found |
| single-capability requested branch | coherent immediate excision candidate | projection remains coherent; coordinate/wording/tests/audit shape affected |
| state-summary coordinate | coherent immediate excision candidate | delete ToolNeed count addend, preserve summary |
| integrity/diagnostic coordinates | independent responsibility with removable branch | inventory/projection branches first |
| rule-inventory wording | presentation-only | can be narrowed without deleting catalog rules |
| `open_tool_needs` | coherent immediate excision candidate | no production callers; test-only reads |
| snapshot serialization/reconstruction | requires earlier consumer removal | then retain only if replay compatibility chosen |
| projection shape | requires earlier consumer removal | coordinate tracks collection |
| affected-scope handling | requires event-branch removal together | otherwise incremental replay expects scope |
| `tool_need.status_changed` | producerless compatibility support | projection/open/status display currently consume |
| `tool_need.created` | producerless compatibility support | projection and fixtures currently consume |
| `State.tool_needs` | requires earlier consumer/rematerialization removal | central carrier until all branches gone |
| `ToolNeedStatus` | requires earlier consumer removal | model/status replay/filter/display validate it |
| `ToolNeed` model | requires earlier consumer removal | projector/store/adapters/export/tests import it |
| package export | requires model/client removal | constructibility compatibility only |
| distributed tests/fixtures | test-only support | update only with the surface each test preserves |

### Topology 6 — evidenced excision dependency graph

```text
Layer 1: leaf presentation/correlation adapters
  capability view branch
  capability inventory requested input (+ integrity effects)
  catalog ToolNeed overload + ToolRecommendationService adapter
  single-capability requested branch
  state-summary count addend
  rule-inventory ToolNeed wording
          |
          v
Layer 2: lifecycle/test-only leaf
  open_tool_needs
          |
          v
Layer 3: generic compatibility attachments
  snapshot write/read field + projection-shape declaration
          |
          v
Layer 4: replay compatibility
  status_changed and created apply branches + affected-scope branches
          |
          v
Layer 5: carrier
  State.tool_needs
          |
          v
Layer 6: representation compatibility
  ToolNeedStatus -> ToolNeed -> package export

At every layer: update only distributed tests/fixtures that preserve that layer.
```

Layer 1 items are mutually separable; this is a dependency order, not a demand
for one large patch. Layer 2 is also immediately coherent alone. Layers 3–6 should
not precede consumers: removing persistence while retaining projected consumers
would split replay/snapshot behavior; removing events while retaining a collection
would leave snapshot/direct-construction-only state; removing the collection
before branches would break them; removing model/status/export first breaks every
upper branch. Once Layers 1–2 are gone, projection support has no production
semantic consumer other than persistence/replay of itself. Removing Layer 3 makes
the events replay-only without snapshot cache support; removing Layer 4 makes the
collection consumerless; removing Layer 5 makes model/status/export test/API-only.

### Deletion dependency matrix

| Layer | Current dependents | Independent responsibility preserved | Tests affected | Coherent alone? | What becomes consumerless |
| --- | --- | --- | --- | ---: | --- |
| view branch | CLI/view | ToolSpec capability view | state-view/CLI | yes | that adapter |
| inventory branch | inventory/integrity/single projection | fact/contract inventory and integrity | inventory/integrity/CLI | yes | requested-source helper |
| catalog/service adapters | service/tests | catalog entries/get/ranker | catalog | yes together | ToolRecommendationService |
| single projection branch | JSON/text/diagnostic audits | all other one-string sources | projection/CLI/diagnostic | yes | requested coordinate |
| summary/rule wording | CLI | generic summary/catalog rules | view/rule/CLI | yes | type-specific wording/count |
| open filter | tests | State itself | projector/invariance | yes | property |
| snapshot/shape | store/audits | generic store/shape | projection store/shape | after leaf removal | projected persistence branch |
| event/scope | projector/tests | generic replay/scope | projector | after persistence choice | collection production road |
| collection | model/store imports/tests | generic State | distributed | after all reads | model/status |
| status/model/export | imports/tests | package and other models | exports/distributed | last | complete island |

**Immediate bounded candidate.** The smallest single coherent implementation
excision evidenced is `State.open_tool_needs` plus only its ToolNeed-specific test
assertions: it has no non-test consumer and removes no independent responsibility.
An equally leaf-like documentation correction exists in rule-inventory wording,
but that is presentation narrowing rather than topology excision. This report
does not implement either.

**Smallest next honest operation.** Perform one implementation-backed deletion of
`State.open_tool_needs` and its test-only assertions, re-search callers, run the
focused projector/invariance suite, and stop. Do not combine that operation with
model/event/projection deletion or replacement design.

## X. Negative authority and protected neighbors

### Topology 7 — negative-authority graph

```text
caller-authored ToolNeed / producerless event
   -X-> constitutional Need
   -X-> evidenced Gap
   -X-> bounded capability Demand
   -X-> constitutional Capability standing
   -X-> candidate or provider selection
   -X-> authorization
   -X-> movement or work
   -X-> generation / validation / registration acts
   -X-> refusal
   -X-> satisfaction or closure

status labels -> display/filter only
catalog recommendations -> advisory metadata only
rank scores -> ordering only
projection -> accepted current representation only
```

Protected neighboring districts are not deletion candidates here:
`CapabilityCatalog` entries, `CapabilityRecommendation`, `ToolSpec`, `Toolkit`,
capability candidates, capability promotion readiness, verification evidence,
registered-operation indexing, Capability standing, Need/Gap/Demand families,
`BoundedOperatorGoalEstablishment`, `BoundedAdvancementHorizon`, `ExecutionStatus`,
`Approval`, and `RiskClass`. A typed ToolNeed adapter inside them may be removed
without prejudging the neighbor.

## XI. Candidate next-operation matrix

| Candidate operation | Requirement | Present incompatibility/consequence | Pressure | Verdict |
| --- | --- | --- | --- | --- |
| delete `open_tool_needs` only | no independent caller depends on it | only tests/invariance tuple change | excision | smallest honest next operation |
| remove rule wording only | catalog rule must not imply deleted service | output wording changes | editorial/excision | coherent, but not deepest topology step |
| remove capability-view branch | preserve ToolSpec views | ToolNeed rows disappear | excision | coherent bounded follow-up |
| remove inventory branch | preserve fact/contract universe | ToolNeed-only entries/counts disappear | excision/editorial | coherent with transitive tests |
| remove single projection branch | preserve diagnostic's other sources | requested JSON/count disappears | excision/editorial | coherent with registry/shape tests updated |
| remove snapshot/events now | compatibility policy decision | old local payload/event support disappears | compatibility | not first; consumers remain |
| remove model/export now | every importer/consumer must be gone | immediate breakage across island | cleanup only if premature | requires earlier layers |
| invent replacement open/Need schema | none in task | would create new responsibility | unsupported | prohibited |

## XII. Direct answers

1. **Current production owner creates ToolNeed?** No.
2. **Current production owner emits either event?** No.
3. **Exact ingress?** Arbitrary constructor/package import, manually supplied
   generic ledger events recognized at replay, and snapshot payload reconstruction.
4. **Direct `State.tool_needs` readers?** `open_tool_needs`, capability view,
   state summary, capability inventory, single-capability projection, snapshot
   serialization; projector/status replay and loader write it; projection shape
   names it.
5. **Transitive-only consumers?** Integrity summary, CLI formatters/JSON, summary
   cache/operator views, diagnostic inventory/shape audit, and associated tests.
6. **Independent responsibilities?** Generic projection/persistence, capability
   view for ToolSpecs, evidence/contract inventory, integrity summary, catalog,
   generic ranker, multi-source single-capability diagnostic, state summary,
   rule inventory, diagnostic registry/audit.
7. **Satellites?** Every ToolNeed-specific branch listed in Topology 4, especially
   open filter, typed catalog/service adapters, requested projection branch, and export/tests.
8. **Coherent without branch?** All independent consumers above.
9. **Exist solely because ToolNeed exists?** `open_tool_needs`, the typed catalog
   overload, `ToolRecommendationService` as currently evidenced, model/status/export,
   event/snapshot branches, and ToolNeed-specific tests.
10. **Direct semantic fields?** `id`, `name` (sort only), `capability`,
    `requested_by_event_id`, and `status`.
11. **Serialization-only fields?** `workspace_id`, `summary`, `reason`, `risk_hint`,
    `desired_inputs`, `desired_outputs`.
12. **Explicit status branches?** Only `registered` and `rejected`; `proposed` is a default.
13. **Intermediate status use beyond display?** No; validation/serialization only.
14. **`registered` behavior?** Exclusion from `open_tool_needs`.
15. **`rejected` behavior?** The same exclusion.
16. **Constitutional Need?** No.
17. **Gap?** No.
18. **Capability Demand?** No; only strengthening language.
19. **Capability standing?** No; strings/correlation/inventory rows do not establish it.
20. **Catalog adapter needs full object?** No, only `capability`; `get(str)` exists.
21. **Ranker needs ToolNeed identity?** No; it receives a string and never reads collection presence.
22. **Inventory requires strings?** Its independent fact/ToolSpec responsibility does not.
23. **Capability view coherent without them?** Yes, with ToolSpec rows.
24. **Single projection coherent?** Yes, with its other independent owner inputs.
25. **Strengthening wording?** “unresolved needs,” `unverified` for request-only
    strings, capability counts/views, `requested_state_proves_demand_only`, and
    especially “demand artifact(s).”
26. **Checked-in persisted fixture requires compatibility?** No non-test nonempty
    snapshot/fixture found; ephemeral distributed tests do.
27. **External persistence burden evidenced?** No; Unknown externally.
28. **Export documented supported contract?** No active guide promise found;
    package export itself proves only public constructibility.
29. **Events active production or replay compatibility?** Replay/test compatibility only.
30. **Would presentation/correlation removal make projection consumerless?** Yes,
    except snapshot/replay compatibility preserving itself.
31. **Would projection removal make events consumerless?** Yes.
32. **Would events/projection removal make model/status/export consumerless?** Yes,
    after typed catalog/service adapters and tests are also removed.
33. **Exact order?** Leaf consumer adapters -> open filter -> snapshot/shape ->
    event/scope replay -> collection -> status/model/export, with tests per layer.
34. **Immediate coherent excision?** Yes: `open_tool_needs` plus its test assertions.
35. **Smallest next operation?** That single bounded deletion and focused validation.
36. **Unknowns?** External imports, persisted databases/events/snapshots, unsupported
    direct consumers, deployment compatibility policy, and whether maintainers
    intentionally choose replay longevity despite absent constitutional warrant.

## Validation record and stopping point

The recovery used repository-wide `rg` searches over production, scripts, tests,
fixtures, active Book, and reports for constructors, both event kinds, collection
and snapshot fields, status literals, package exports, service names, and every
required vocabulary spelling. Focused tests cover construction/catalog adapters,
event replay and open filtering, projection persistence/shape, views, inventory,
ranking, single-capability projection, integrity/summary output, diagnostic
inventory/shape, rule inventory, CLI/JSON, and package/import behavior. The exact
commands and results are recorded in the change's final response.

The recovery stops here. It does not delete, rename, repair, replace, migrate, or
reopen any implementation district and does not characterize `ExecutionStatus`.
