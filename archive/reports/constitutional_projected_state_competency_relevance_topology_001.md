# Constitutional Projected-State Competency Relevance Topology 001

## Scope

This investigation asks what the repository currently reconstructs into Seed's live projected state, which bounded responsibilities can recognize the reconstructed conditions as locally relevant, and where Seed instead uses direct transient artifact handoffs without first recording or projecting them.

It does not design a scheduler, subscription mechanism, event bus, competency registry, universal state schema, or next implementation seam. It treats repository implementation, tests, and refusal boundaries as authority.

## Smallest topology recovered

Seed does not currently expose one global projection that gives every responsibility universal standing over every constitutional condition. The implementation shows several partially overlapping surfaces:

| Surface | Classification | Repository support | Boundary |
| --- | --- | --- | --- |
| Append-only ledger entries | canonical event history | `EventLedger.append` creates `Event` records and stores them by id/workspace; `SQLiteEventLedger` persists the same public API in SQLite. | Event availability is historical input, not automatic truth, action, or consumer relevance. |
| `State` rebuilt by `StateProjector` | current projection | `StateProjector.project` starts a workspace `State`, replays ledger events, and finalizes derived indexes. | Projection availability is not consumer uptake and does not establish universal standing. |
| `State` collections and finalized helper fields | current projection plus derived indexes | `State` contains entities, facts, observations, evidence, goals, tool needs, approvals, authorizations, pending actions, plans, tools, graph issues, aliases, supports, conflicts, and type assertions. | Projected condition is not canonical history; these coordinates are replay results. |
| Projection snapshots | disposable cache/read model | `project_state_with_cache` may load/save snapshots keyed by workspace, projection name/version, and last event id. | Cache freshness is not authority independent of ledger events. |
| `DerivedFactIndex` | derived index | `build_fact_index` builds reusable facts-by-subject/predicate lookup from already-projected `State`. | It is not event authority, projection authority, fact mutation, observation creation, or a view cache. |
| `CapabilityCatalog` and registry/capability resolution payloads | consumer-local lens / read-only catalog lens | `ToolNeedService.resolve_capability` reads a `ToolNeed`, `CapabilityCatalog`, registry, and recommendations to return resolution metadata. | Catalog recommendations and registered operations do not execute, authorize actions, or mutate catalog/registry state. |
| Goal selection, inquiry-need, downstream admission, bounded-goal establishment artifacts | transient artifacts / consumer-local lenses | These dataclasses preserve `read_only`, `writes_event_ledger=False`, and `mutates_cluster=False` boundaries. | Direct live uptake may be lawful inside exact consumer/purpose boundaries but is not cross-tick recognition. |

## Road A: recorded tool-need event to projection-mediated relevance

```text
recorded event
→ projected open tool-need condition
→ tool-need/capability-resolution responsibility recognizes relevance
```

| Required recovery field | Repository-supported recovery |
| --- | --- |
| Source event | `ToolNeedService.create_from_decision` records `tool_need.created` after checking the current projection for an existing open need. |
| Artifact or recorded assertion | The event payload contains serialized `ToolNeed` with normalized `name`, `capability`, summary, reason, requester causation id, risk hint, and desired inputs/outputs. |
| Projection owner | `StateProjector` owns replay into `State`. Its `apply` branch for `tool_need.created` reconstructs a `ToolNeed` and stores it in `state.tool_needs`; `tool_need.status_changed` updates projected status. |
| Projected coordinates and standings | Projected coordinates include `ToolNeed.id`, workspace, normalized name/capability, summary, requested-by event id, risk hints, desired IO, and status. The relevant standing is open/closed status as exposed by projected-state helpers such as open tool needs. |
| Projection scope and freshness | Scope is workspace-local: `StateProjector.project(workspace_id)` uses `ledger.list_events(workspace_id)`. Freshness is at `State.last_event_id`, or the cache status' `current_last_event_id` when `project_state_with_cache` is used. |
| Consumer or responsibility locality | `ToolNeedService` owns capability-gap creation and read-only capability resolution for `request_tool` decisions, not all goals or actions. |
| Local question made applicable | On creation: “does this workspace already have an open need with this normalized name or capability?” On resolution: “what known catalog providers, handoff candidates, and registered visible operations may satisfy this exact need?” |
| Consumer validation before uptake | Creation validates through projection deduplication before recording another event. Resolution validates by looking up the specific need capability in `CapabilityCatalog` and visible registry operations only. |
| Authority and purpose boundary | The service records tool-need events but `resolve_capability` explicitly does not execute tools, authorize actions, create pending actions, or mutate registry/catalog state. |
| Resulting standing | A new missing-capability condition can become projected in `state.tool_needs`; later resolution can return advisory capability metadata. |
| Whether another event is recorded | Creation records `tool_need.created`; status changes record `tool_need.status_changed`; read-only resolution records no event. |
| Remains transient, hidden, Unknown, unreconstructible | Provider recommendations supplied as live arguments to `resolve_capability` are transient unless separately preserved. Catalog/registry contents are read from their owners rather than reconstructed from the tool-need event. No universal competency action is implied. |

Observed surface classifications: `tool_need.created` is canonical event history; `state.tool_needs` is current projection; open-need lookup is a consumer-local lens over projected state; capability resolution payload is a consumer-local transient/read-only lens.

## Road B: recorded fact events to projected facts and derived index relevance

```text
recorded event
→ projected fact condition and supports
→ fact-index/read-model responsibility recognizes lookup relevance
```

| Required recovery field | Repository-supported recovery |
| --- | --- |
| Source event | Ledger events of kind `fact.observed` or `fact.inferred`. |
| Artifact or recorded assertion | The event payload normalizes into a `Fact`; inferred facts are marked `inferred=True` and `source_type="inferred"`, while observed facts are kept non-inferred unless source metadata says otherwise. |
| Projection owner | `StateProjector.apply` decodes fact events into `state.facts`; finalization derives observed/inferred fact collections, supports, conflicts, relationship/type indexes, and graph validation outputs. |
| Projected coordinates and standings | Projected coordinates include fact id, subject, predicate, value, confidence/source fields, expiry/measurement status, observed vs inferred status, supports, conflicts, and current lookup ordering. Standing is current projected fact availability, not objective truth. |
| Projection scope and freshness | Workspace replay position is `last_event_id`. Cache freshness is accepted only when snapshot `last_event_id` matches current ledger latest event id or when safe incremental replay applies. |
| Consumer or responsibility locality | `DerivedFactIndex` owns reusable fact lookups by subject/predicate from an already-projected `State`. It is a read-model owner, not the fact projector or event owner. |
| Local question made applicable | “For this already-projected state, which current facts answer this exact subject/predicate lookup?” |
| Consumer validation before uptake | The index is constructed from `read_model_construction_inputs(state)`, uses `visible_state`, records dependency identity on state projection version and last event id, and lookup returns only fact ids still present in the supplied `State`, excluding expired facts by default. |
| Authority and purpose boundary | `fact_index.py` states the index is a cacheable derived read model and is not event authority, projection authority, fact mutation, observation creation, or a view cache. |
| Resulting standing | The index grants faster consumer-local lookup standing over facts already admitted to projected state. It does not promote facts to canonical truth. |
| Whether another event is recorded | Building/loading/publishing the fact index records no ledger event; it may save a derived-index snapshot in the projection store. |
| Remains transient, hidden, Unknown, unreconstructible | Exact progress/status emission during index work is transient unless captured. If ledger events remain, the index is reconstructible; if a snapshot is lost, history is not lost. |

Observed surface classifications: `fact.observed`/`fact.inferred` are canonical event history; `state.facts`, observed/inferred facts, supports, conflicts, and graph issues are current projection/derived projection indexes; `DerivedFactIndex` is a derived index and cacheable read model.

## Road C: projection cache as disposable current-state materialization

```text
recorded events
→ projected State snapshot
→ later projector/cache caller recognizes freshness and reuses or rebuilds
```

| Required recovery field | Repository-supported recovery |
| --- | --- |
| Source event | All workspace ledger events up to a latest event id. |
| Artifact or recorded assertion | A `ProjectionSnapshot` stores projection identity/version, `last_event_id`, latest event timestamp, serialized state payload, and created time. |
| Projection owner | `StateProjector` owns the `State`; `ProjectionStore` owns cached projected-state snapshots; `project_state_with_cache` coordinates reuse. |
| Projected coordinates and standings | The coordinates are whatever `State` carried at `last_event_id`; the cache status carries `cache_hit`, projection version, snapshot/current last event ids, incremental replay flag, and events applied. |
| Projection scope and freshness | Scope is workspace plus projection name/version. Freshness requires snapshot `last_event_id == current_last_event_id` for a hit, or compatible incremental replay after the snapshot. Cache eligibility also requires `mutates_cluster is False`. |
| Consumer or responsibility locality | The locality is projector/cache caller locality, not every bounded responsibility. A later consumer may receive the returned `State`, but the snapshot owner only accelerates materialization. |
| Local question made applicable | “Can this exact projection/version/workspace snapshot stand in for replay, or must events be replayed?” |
| Consumer validation before uptake | The cache path checks load errors, cache eligibility, payload materialization, projection identity/version, snapshot event position, current ledger event position, and incremental-replay compatibility. |
| Authority and purpose boundary | `project_from_state` states event history remains authority when a validated snapshot is reused. |
| Resulting standing | A returned `State` has current projected-state standing at the accepted ledger position; the snapshot itself has disposable cache standing. |
| Whether another event is recorded | Saving a snapshot does not append a ledger event. |
| Remains transient, hidden, Unknown, unreconstructible | Cache status and progress status may be transient. Losing the cache should not destroy history if ledger events remain. Exact prior build timings are not canonical projection truth. |

Observed surface classifications: ledger rows are canonical event history; `State` is current projection; `ProjectionSnapshot` is disposable cache/read model; `StateCacheStatus` is transient/status artifact.

## Road D: direct goal-focus selection to inquiry-need projection without ledger mediation

```text
producer returns transient artifact
→ exact consumer validates and uses it directly
```

| Required recovery field | Repository-supported recovery |
| --- | --- |
| Transient producer | `select_goal_for_inquiry_consideration`. |
| Artifact or recorded assertion | `GoalInquiryConsiderationSelection` records candidate-set identity, focus evidence refs/provenance, selection state, selected goal identity/source if exactly supported, non-selected goals, ambiguity/missing/mismatch refs, unknowns, conflicts, and boundary booleans. |
| Projection owner, if any | No ledger projector owns this artifact. It is a read-only selection artifact. `project_inquiry_need` later uses it as one direct input. |
| Projected coordinates and standings | Selection standings include `selected`, `no_focus_evidence`, `missing_goal_identity`, `ambiguous`, `conflict`, and `inventory_mismatch`. Inquiry projection standings include `established`, `unsupported`, `unknown`, `conflicting`, `excluded_family`, and `unclassified`. |
| Projection scope and freshness | Selection freshness is tied to the exact `GoalOrientationInventory` candidate-set hash and explicit focus evidence. Inquiry projection freshness is tied to the supplied selection id, goal establishment id, horizon id, and horizon evidence refs. It is not cross-tick state freshness. |
| Consumer or responsibility locality | The consumer is `project_inquiry_need`, whose purpose is only read-only inquiry-need projection from explicit repository/world uncertainty testimony. |
| Local question made applicable | “Does explicit focus evidence select one visible bounded goal, and does component-bounded repository/world uncertainty testimony establish an inquiry need for that selected goal and horizon?” |
| Consumer validation before uptake | Selection refuses absent, missing, ambiguous, conflicting, or inventory-mismatched focus evidence. Inquiry projection rejects testimony through identity checks on selection, goal, horizon, evidence refs, uncertainty family, stage ownership, component boundedness, repository/world subject, materiality, and mixed/non-inquiry material. |
| Authority and purpose boundary | Selection states selected-for-inquiry-consideration is not activation, inquiry required/opened, frontier movement, work authorization, execution, recording, or mutation. Inquiry projection says established inquiry need is not inquiry opened, question selected, observation authorized, action selected, sufficiency judged, execution, recording, event-ledger writing, or cluster mutation. |
| Resulting standing | The direct result may classify inquiry-need testimony for the exact supplied context. It does not create projected `State` and does not authorize movement. |
| Whether another event is recorded | No event is recorded by either producer. |
| Remains transient, hidden, Unknown, unreconstructible | The selection and projection are reconstructible only if the inventory, focus evidence, goal, horizon, and testimony remain available. Generic Unknowns and unrelated observations do not become inquiry evidence. |

Observed surface classifications: selection artifact is transient artifact/consumer-local lens; inquiry-need projection is a consumer-local transient read model; no canonical event history or shared `State` road exists here unless inputs are separately recorded.

## Road E: direct downstream admission to bounded-goal establishment

```text
producer returns transient consumer-local admission
→ exact bounded-goal consumer validates and uses it directly
```

| Required recovery field | Repository-supported recovery |
| --- | --- |
| Transient producer | `admit_downstream_interpretation`. |
| Artifact or recorded assertion | `DownstreamInterpretationAdmission` carries selection result id, applicability projection id, selected candidate ref/object, exact consumer/purpose refs and labels, admission evidence, outcome, admitted flags, refusals, unknowns, conflicts, provenance, and read-only boundary flags. |
| Projection owner, if any | No ledger-backed `StateProjector` owner. The admission consumes an `InterpretationApplicabilityProjection` and is then directly consumed by `establish_bounded_operator_goal_from_admitted_interpretation`. |
| Projected coordinates and standings | Applicability is distinct from admission. Admission standings include admitted, unadmitted, conflict, unknown, and applicable-but-unadmitted reasons. Bounded-goal standings include `established`, `provisional`, and `refused` with sufficiency state. |
| Projection scope and freshness | Scope is the exact tuple of selection result, applicability projection, selected candidate, consumer ref, and purpose ref. Freshness is live artifact freshness, not ledger position. |
| Consumer or responsibility locality | The downstream admission is local to exactly one consumer and purpose. Bounded-goal establishment accepts it only for `consumer:bounded-operator-goal-establishment` and `purpose:bounded-operator-goal-establishment`. |
| Local question made applicable | Admission asks whether an applicable selected interpretation has explicit admission evidence for this exact consumer/purpose. Bounded-goal establishment asks whether that admitted meaning can supply bounded operator-goal orientation without reinterpreting/reselecting/recomputing upstream material. |
| Consumer validation before uptake | Admission rejects mismatched applicability/selection ids, foreign evidence, non-applicable projections, conflicts, unknowns, refusals, and missing explicit admission evidence. Bounded-goal establishment validates artifact type, consumer/purpose refs, admission/projection/selection identity, admitted outcome, applicability, unknowns, conflicts, and selected meaning identity. |
| Authority and purpose boundary | Admission says applicable is not admitted, admission is not transferable authority, and admission stops before goal establishment, correction, inquiry movement, authorization, execution, presentation, recording, event-ledger writes, state mutation, or cluster mutation. Goal establishment from admission consumes carried snapshots and explicitly does not reinterpret source material, regenerate warrants, reselect candidates, recompute applicability, or recompute admission. |
| Resulting standing | A bounded goal may become established or provisional as a direct live artifact. It is not a recorded `goal.created` event and not projected into shared `State` unless another owner records it. |
| Whether another event is recorded | No event is recorded by admission or this bounded-goal establishment path. |
| Remains transient, hidden, Unknown, unreconstructible | Admission evidence and selected meaning snapshots remain local artifacts unless separately preserved. Another consumer cannot inherit the admission. Cross-tick recognition is unavailable without persisted inputs or a later ledger event. |

Observed surface classifications: applicability/admission/goal-establishment artifacts are transient artifacts and consumer-local lenses; the carried selected-meaning snapshot is a transient artifact snapshot; no current shared `State` surface is created.

## Quiet classification of requested possibilities

| Possibility | Current repository support | Classification |
| --- | --- | --- |
| One shared `State` | Supported as a workspace projection class rebuilt by `StateProjector`. | current projection, not universal standing |
| Multiple bounded projections | Supported by many read-only projection artifacts and projection/read-model owners, e.g. inquiry need, applicability, authority/scope, fact index, projection snapshots. | multiple bounded projections/read models |
| Consumer-specific lenses | Supported by downstream admission, tool-need service resolution, capability catalog lookups, and fact-index lookups. | consumer-local lenses |
| Derived indexes | Supported by `DerivedFactIndex` and `State` finalized indexes. | derived indexes |
| Read models | Supported by projection snapshots, derived-index snapshots, summaries, and read-model ownership helpers. | disposable cache/read model unless specified otherwise |
| Direct artifact roads | Supported by goal selection → inquiry projection and admission → bounded-goal establishment. | transient artifact roads |
| Projection-mediated roads | Supported by event ledger → `StateProjector` → service/index/diagnostic consumers. | canonical history to current projection to bounded recognition |
| Universal competency relevance | Not supported. No implementation evidence shows every event/projection is relevant to every responsibility. | Unknown / unsupported |

## Distinctions preserved by implementation evidence

- Event availability is not competency relevance: `ToolNeedService` cares about open tool needs; `DerivedFactIndex` cares about fact lookup; admission/goal establishment never consult the ledger.
- Projection availability is not consumer uptake: a `State` may contain many collections, but each consumer performs local validation before relying on a slice.
- Projected condition is not canonical history: `State` can be rebuilt or cached; ledger events remain the replay authority.
- Shared `State` is not universal standing: `State` contains many dimensions but does not authorize all movement or answer every local question.
- Lens is not road: a lookup/index/admission lens shapes what a consumer sees; it does not by itself create a replay path or action path.
- Direct live uptake is not cross-tick recognition: direct artifacts can be consumed immediately and then vanish unless preserved.
- Relevance is not required action: even established inquiry need or open tool need does not itself open inquiry, execute a tool, or mutate a cluster.
- Current condition is not authority to move: projected authorizations may mark execution proposals executable in one branch, while other projected facts/needs only make local questions answerable.

## Smallest repository-supported answers

### What constitutes Seed's live projected present?

The smallest implementation-backed live projected present is a workspace `State` rebuilt by `StateProjector` from append-only ledger events, finalized with local derived indexes, optionally materialized through a cache whose eligibility and freshness are tied to projection identity/version and ledger `last_event_id`. Direct read-only projection artifacts outside `State` are live local presents only for their exact consumers and inputs, not shared projected state.

### Which dimensions and standings survive projection?

The shared `State` projection preserves event-derived coordinates for entities, observations, evidence, facts, goals, tool needs, approvals, execution authorizations/proposals, pending actions, action plans, handoff plans, tools, relationships, aliases, type assertions, fact supports/conflicts, and graph issues. Standings that survive include observed vs inferred facts, current fact support/conflict/expiry lookup, tool-need status, authorization executability when matching and unexpired, pending/action-plan statuses, graph validation issues, and current entity-type assertions. Direct artifact standings such as admission outcome or inquiry-need classification survive only as live artifacts unless separately recorded or recomputable from preserved inputs.

### Which bounded responsibilities can presently recognize that condition?

Recognizers are local: `ToolNeedService` recognizes open projected tool needs for deduplication and capability-gap resolution; `DerivedFactIndex` recognizes projected fact supports for subject/predicate lookup; projection-cache callers recognize snapshot freshness; diagnostics and audits recognize their own projected-state slices; bounded-goal establishment recognizes exact consumer-local admission artifacts; inquiry-need projection recognizes exact selected-goal/horizon/testimony artifacts. The repository does not show one competency that recognizes every projected condition as relevant.

### How does a projected condition make a local question applicable?

A projected condition makes a local question applicable only when a bounded consumer has an implementation path that reads that coordinate and validates its own boundary. An open tool need makes deduplication and capability resolution applicable; projected fact supports make fact-index lookup applicable; cache metadata makes cache-hit or incremental-replay questions applicable; projected graph/fact/type collections make diagnostics applicable. The condition does not require action and does not confer authority beyond that consumer's purpose.

### When is direct transient uptake used instead?

Direct transient uptake is used when one producer returns an artifact that the exact next consumer can validate and use without cross-tick recognition: goal-focus selection into inquiry-need projection, downstream interpretation admission into bounded-goal establishment, closed-choice or interpretation artifacts into bounded-goal establishment, and read-only capability resolution metadata. These roads preserve consumer identity, purpose, provenance, refusals, unknowns, and no-record/no-mutation boundaries instead of writing ledger events.

### Where does current implementation still fail to connect event history, projected condition, and bounded responsibility?

The implementation does not connect every constitutional artifact to event history, every event-derived condition to a responsible consumer, or every consumer-local admission/selection to cross-tick projected recognition. Goal inquiry selection, inquiry-need projection, downstream admission, and bounded-goal establishment can remain outside canonical history. Capability-catalog recommendations and registry views are not reconstructed from tool-need events. Projection snapshots and fact indexes are disposable read models, not authority. Universal competency relevance, global projection exposure, and transferable standing remain unsupported or Unknown.
