# Constitutional state-language and evidence-shape/root survey 001

## 0. Scope, method, and evidence rule

This first recovery pass surveyed repository-owned uses of `state` language across code, tests, diagnostics, Book clauses, reports, schemas, comments, function/class/module names, fields, and filenames. The survey treated repository artifacts as testimony about mechanics only. It did not treat identifiers, dataclasses, tests, recurring names, or implementation existence as constitutional authority.

Mechanical survey result: a case-insensitive repository scan for word and identifier forms containing `state` found **25,579 literal occurrences in 1,666 files**: 18,629 in Markdown, 6,869 in Python, 30 in JSON, 20 in DOT, 20 in Mermaid, 5 in SQL, 5 in YAML, and 1 in YML. The highest-density owned areas are `scripts/seed_local.py`, projection tests, observation-source tests, `seed_runtime/projection_store.py`, Seed Book architecture clauses, `seed_runtime/state.py`, diagnostic inventory surfaces, state view tests, capability inventory, knowledge reachability, and prior recovery reports.

This report groups usages by recovered meaning rather than by spelling alone. Literal external fields and third-party grammar are preserved separately. No code is renamed here.

## 1. Repository-wide usage families grouped by recovered meaning

### Family A — Projected world model / current projected knowledge

- **Literal occurrence and owner:** `State`, `StateProjector`, `seed_runtime/state.py`, `state_views`, `ProjectionStore` state snapshots, `--current-*`, `--state-build`, Book phrases including “current projected world model derived from the EventLedger.” Representative owners: `docs/archive/original_book_of_seed/01-architecture.md`, `seed_runtime/state.py`, `seed_runtime/state_views.py`, `seed_runtime/projection_store.py`, projection and view tests.
- **Subject whose state is asserted:** Seed's reconstructible world-model projection for a workspace: entities, observations, facts, fact supports, conflicts, aliases, relationships, goals, pending actions, approvals, registered operations, tool needs, and related indexes.
- **Mechanical producer:** `EventLedger` replay through `StateProjector.apply()` and `finalize()`, optionally loaded/saved via `ProjectionStore` snapshots.
- **Evidence consumed:** append-only event records, observations, facts, predicate/entity/relationship catalogs, inference catalog rules, and projection cache metadata when compatible.
- **Consumer:** state views, context views, diagnostics, CLI surfaces, capability inventory, fact indexes, graph validation, contradiction/confidence layers, tests, and compatibility API paths.
- **Temporal resolution:** current-at-projection time, usually resolved by last event and projection build time; measurements may keep recent samples rather than durable aggregation.
- **Persistence resolution:** durable authority remains ledger history; `State` is reconstructible projection; `ProjectionStore` is cached projection and not source truth.
- **Constrains movement:** yes, but only as projected knowledge available to consumers. It can constrain context selection, diagnostics, current-belief display, and validation checks, while not authorizing execution by itself.
- **Meaning claimed:** projection, current belief, condition of known material, and reconstructible outcome of replay.
- **Constitutional warrant found:** strongest warrant is the architecture distinction between ledger history, projection cache, projected world model, and read-only views. Prior recovery reports also classify projection as inspectability rather than original authority.
- **Fidelity finding:** **compressed meanings**. Within core projection code it is mostly faithful within scope, but the single word `state` compresses projected knowledge, projection output, cache payload, current belief, and object-container mechanics.
- **Candidate Seed-native meaning, if warranted:** `projected knowledge`, `current projected knowledge`, `projection`, `projected condition`, or `reconstructible projection` depending on local surface.

### Family B — Projection cache / snapshot lifecycle / freshness

- **Literal occurrence and owner:** `ProjectionStore`, `ProjectionSnapshot.state_payload`, `STATE_PROJECTION_NAME`, `STATE_PROJECTION_VERSION`, `--rebuild-state-cache`, `--state-cache-status`, `state-build` cache debug diagnostics, cache freshness tests and reports.
- **Subject whose state is asserted:** cached projection material for a workspace and derived read-model snapshots that depend on a compatible state snapshot.
- **Mechanical producer:** projection store save/load/clear operations and CLI cache-status/build paths.
- **Evidence consumed:** projection version, last event id, last event created-at timestamp, serialized projection payload, derived snapshot dependency metadata.
- **Consumer:** CLI cache status/build rendering, read-model construction paths, tests around stale/missing/compatible cache behavior.
- **Temporal resolution:** freshness relative to last ledger event and projection version.
- **Persistence resolution:** persisted cache, but subordinate to ledger and rebuildable.
- **Constrains movement:** yes for cache reuse and rebuild decisions; no for constitutional truth.
- **Meaning claimed:** freshness, cache availability, projection lifecycle posture.
- **Constitutional warrant found:** architecture clauses identify `ProjectionStore` as cached current world-model snapshots that never become source of truth.
- **Fidelity finding:** **faithful within scope** where cache subordination is explicit; **compressed meanings** where `state` is used as both projection name and freshness label.
- **Candidate Seed-native meaning, if warranted:** `projection cache`, `projection snapshot`, `cache freshness`, `projection build`.

### Family C — Read-only views and diagnostic/operator presentation surfaces

- **Literal occurrence and owner:** `State Views`, `StateSummary`, `state_summary_views`, `state-build`, diagnostic inventory entries, diagnostic shape-audit specs/tests, current facts/observations/requirements/capabilities/issues flags, `--diagnostic-inventory` and `--diagnostic-shape-audit` expectations.
- **Subject whose state is asserted:** a presentation surface over already-projected material, often a summary of counts, facts, observations, capabilities, or cache/build metrics.
- **Mechanical producer:** view builders and CLI renderers that consume `State` or snapshots.
- **Evidence consumed:** already projected `State`, snapshot metadata, diagnostic registry/spec records.
- **Consumer:** operators, tests, diagnostic inventory and shape audit.
- **Temporal resolution:** current view at render/build time; diagnostic records may preserve a diagnostic run scope.
- **Persistence resolution:** mostly transient rendering; diagnostic inventory/specs are repository-owned durable descriptions; recorded diagnostic output, where present, should be scoped as diagnostic run material.
- **Constrains movement:** yes for visibility and audit expectations; it does not authorize mutation.
- **Meaning claimed:** presentation posture, visible condition, inventory presence, diagnostic outcome, not root knowledge authority.
- **Constitutional warrant found:** operational visibility contract and architecture read-only boundaries.
- **Fidelity finding:** **faithful within scope** when read-only and non-mutation boundaries are explicit; **compressed meanings** where `StateSummary` means both projected summary data and CLI diagnostic surface.
- **Candidate Seed-native meaning, if warranted:** `projection view`, `read-only projection view`, `diagnostic surface`, `summary projection`.

### Family D — Fact support, current belief, contradiction, confidence, and freshness condition

- **Literal occurrence and owner:** `get_best_fact`, FactSupport aggregation language, stale facts, current facts, confidence/contradiction tests, `CapabilityVerificationState` values such as `verified`, `unverified`, `stale`, `provider_reported`, `unknown`.
- **Subject whose state is asserted:** a fact value, capability, predicate support, evidence support set, or unresolved/expired condition.
- **Mechanical producer:** fact support aggregation, predicate cardinality handling, expiry checks, contradiction detection, capability inventory.
- **Evidence consumed:** supporting/conflicting facts, source confidence, source type, observed timestamps, expiry policy, predicate catalog cardinality.
- **Consumer:** context views, current facts CLI, capability inventory, recommendation/inspection surfaces, tests.
- **Temporal resolution:** current belief relative to non-expired facts and latest observations; stale is time-relative.
- **Persistence resolution:** evidence/facts in ledger; support and current-belief projections rebuildable; capability inventory entries transient presentation.
- **Constrains movement:** yes for what is shown or considered supported; no independent execution authority.
- **Meaning claimed:** standing (`verified`), condition (`stale`, `unknown`), current belief, support outcome, conflict posture.
- **Constitutional warrant found:** architecture's fact support aggregation and typed unknown preservation.
- **Fidelity finding:** **compressed meanings** because `state` covers standing, condition, freshness, and unresolvedness. Capability inventory is also pressured by external capability/tool grammar.
- **Candidate Seed-native meaning, if warranted:** `support standing`, `freshness condition`, `current belief`, `unresolved condition`, `verification standing`.

### Family E — Lifecycle/status/posture fields for goals, needs, decisions, executions, approvals, and actions

- **Literal occurrence and owner:** `status`/state-like fields in `ToolNeed`, `Goal`, `PendingAction`, `ExecutionStatus`, execution proposals, decisions, approval and pending action tests; Book and reports that say active/open/unresolved/completed/blocked.
- **Subject whose state is asserted:** a lifecycle object or request artifact.
- **Mechanical producer:** event application, service methods, execution status measurement, policy/validation results, tests.
- **Evidence consumed:** lifecycle events, decision payloads, policy decisions, execution reports, progress observations.
- **Consumer:** runtime services, CLI/API presentation, diagnostics, tests, context composition.
- **Temporal resolution:** current lifecycle posture after replay or event update.
- **Persistence resolution:** event history durable; projected object posture rebuildable; some transient measurement records.
- **Constrains movement:** yes, often directly: open vs resolved needs, pending vs completed actions, blocked vs allowed policy results affect lawful continuation/presentation.
- **Meaning claimed:** posture, phase, status, condition, outcome.
- **Constitutional warrant found:** partial. Movement constraints are mechanically real, but constitutional standing varies by local object and question.
- **Fidelity finding:** **Unknown** for many local fields until each lifecycle grammar is recovered; **compressed meanings** where one word hides phase, posture, and authority outcome.
- **Candidate Seed-native meaning, if warranted:** `lifecycle posture`, `request posture`, `execution outcome`, `approval posture`; not warranted universally.

### Family F — Unknown preservation and unresolved conditions

- **Literal occurrence and owner:** typed unknown reports and code, `unknown` enum values in capability inventory, membership evidence, reachability, diagnostic/admission surfaces, Book language around Unknown and uncommitted subjects.
- **Subject whose state is asserted:** unresolved claims, missing support, unsupported relationships, uncertain membership, insufficient evidence, boundary unknowns.
- **Mechanical producer:** typed unknown preservation helpers, local classifiers, audit/admission projections, capability/reachability/membership producers.
- **Evidence consumed:** absence of required support, explicit missing references, conflict references, unsupported evidence boundaries.
- **Consumer:** reports, diagnostics, context/admission surfaces, tests.
- **Temporal resolution:** unresolved at the local inquiry/projection time.
- **Persistence resolution:** sometimes durable report text, sometimes transient projection field, sometimes rebuildable from inputs.
- **Constrains movement:** yes by stopping unsupported promotion or requiring bounded follow-up inquiry.
- **Meaning claimed:** unresolved condition, not a fact.
- **Constitutional warrant found:** strong in typed unknown characterization and operational instructions.
- **Fidelity finding:** **faithful within scope** where Unknown is preserved and typed; **compressed meanings** where raw `unknown` appears as a catch-all enum without local question evidence.
- **Candidate Seed-native meaning, if warranted:** `typed unresolved condition`, `Unknown`, `support absence preserved as Unknown`.

### Family G — Membership, admission, eligibility, applicability, and reachability result states

- **Literal occurrence and owner:** shared explanation membership evidence states (`belongs`, `does_not_belong`, `unknown`, `conflict`), interpretation applicability, representation grammar applicability, downstream admission, capability reachability partitions (`supporting`, `blocked`, `unsupported`, `unknown`, `conflicting`).
- **Subject whose state is asserted:** candidate membership, applicability, admission, reachability, or eligibility relative to a bounded inquiry/request.
- **Mechanical producer:** local projection/classification functions consuming bounded references and explicit evidence.
- **Evidence consumed:** bounded inquiry identity, source identity, lineage references, positive/incompatible/missing references, same-bounded-input checks, conflict references.
- **Consumer:** shared explanation, admission, reachability, and diagnostic tests/surfaces.
- **Temporal resolution:** result at the local classification act.
- **Persistence resolution:** usually transient projection record and tests; some report text durable.
- **Constrains movement:** yes for admission, membership, and reachability, but not as universal authority.
- **Meaning claimed:** local classification outcome or standing relative to a question.
- **Constitutional warrant found:** local warrant exists in reports/tests that explicitly bound membership/admission/reachability and deny selection/execution authority.
- **Fidelity finding:** **faithful within scope** locally; **compressed meanings** if called simply `state` without question and responsibility names.
- **Candidate Seed-native meaning, if warranted:** `membership classification`, `admission standing`, `applicability standing`, `reachability posture`.

### Family H — External provider or third-party literal fields

- **Literal occurrence and owner:** systemd active/sub/unit-file state, Kubernetes/pod/container state-like payloads where present, Git status/branch state, HTTP/JSON provider field names, YAML/JSON fixture keys, externally quoted command output, Book/provider examples.
- **Subject whose state is asserted:** external resource condition as named by that provider.
- **Mechanical producer:** external command/API/parser output and Seed source adapters.
- **Evidence consumed:** provider row/field text, command stdout, imported fixture.
- **Consumer:** source adapters, observation normalizers, tests, reports.
- **Temporal resolution:** external observation time.
- **Persistence resolution:** raw observation/evidence may be durable; provider vocabulary remains quoted or mapped evidence, not Seed grammar.
- **Constrains movement:** only as evidence after a Seed responsibility recognizes relevance/sufficiency.
- **Meaning claimed:** legacy/external grammar; provider condition.
- **Constitutional warrant found:** warrant only to preserve testimony and map into observations; no warrant to adopt provider vocabulary as Seed-native.
- **Fidelity finding:** **legacy external grammar**. Likely neutralize by quotation/boundary preservation rather than translate into Seed constitutional terms.
- **Candidate Seed-native meaning, if warranted:** `provider-reported condition` or quoted external field; no Seed-native replacement for literal field names.

### Family I — LLM-agent, tool, ToolNeed, ToolExecutor, capability-catalog, and registered-operation vocabulary

- **Literal occurrence and owner:** `ToolNeed`, `ToolExecutor`, `ToolRegistry`, registered operations, capability catalog, recommendation ranker, provider/handoff candidates, builder/toolkit reports and tests.
- **Subject whose state is asserted:** a capability gap, registered operation catalog entry, recommendation, operation candidate, or execution authorization path.
- **Mechanical producer:** runtime services, catalog lookup, registry lookup, validation, policy, tests.
- **Evidence consumed:** decision payloads, catalog metadata, registered specs, validation/policy results, projected needs.
- **Consumer:** runtime request handling, capability resolution payloads, CLI/API/tests.
- **Temporal resolution:** current catalog/registry/projection view at request time.
- **Persistence resolution:** catalog/registry may be configured/imported; needs/events may be durable; recommendations often transient.
- **Constrains movement:** yes mechanically, especially because only registered operations may execute after validation/policy; but this is precisely a fidelity pressure area.
- **Meaning claimed:** availability, capability gap, registered-operation candidate, execution boundary.
- **Constitutional warrant found:** only boundary warrant: these terms are treated as compatibility/external/LLM-agent vocabulary and must not be promoted as Seed-native without independent authority.
- **Fidelity finding:** **legacy external grammar** and **fidelity red flag**. Mechanics must be recorded accurately; grammar should not be constitutionalized.
- **Candidate Seed-native meaning, if warranted:** none yet beyond neutral descriptions such as `capability gap request`, `registered operation metadata`, `execution boundary record`.

### Family J — “State machine,” “state transition,” and architectural metaphor

- **Literal occurrence and owner:** Book opening: “state engine / distributed state machine,” high-level flow `Input -> Events -> State -> Context`, Event Ledger storing “state transitions,” reports comparing Seed to organisms/courts/science and separating current state from governing constraints.
- **Subject whose state is asserted:** Seed architecture as a whole, or event-ledger change semantics.
- **Mechanical producer:** documentation, not a single implementation boundary.
- **Evidence consumed:** broad architecture description and implementation recurrence.
- **Consumer:** readers, architectural conformance tests, recovery reports.
- **Temporal resolution:** architectural statement, not local projection time.
- **Persistence resolution:** durable docs.
- **Constrains movement:** yes as orientation, but risky if treated as universal model.
- **Meaning claimed:** metaphor/model, transition/outcome, architecture shorthand.
- **Constitutional warrant found:** weak for constitutional grammar; repository instructions explicitly warn that presentation vocabulary is not automatically knowledge.
- **Fidelity finding:** **compressed meanings** and possible **unfaithful boundary crossing** if used to make all Seed movement a state-machine concept.
- **Candidate Seed-native meaning, if warranted:** none universally. Local occurrences may become `projection`, `event outcome`, or `movement record` only after local warrant.

### Family K — Python/local implementation mechanics and compatibility identifiers

- **Literal occurrence and owner:** module filenames (`state.py`, `state_patches.py`), dataclasses, function arguments named `state`, local variables, test fixture names, serialized keys, compatibility API names.
- **Subject whose state is asserted:** often no constitutional subject; frequently an object instance, dictionary, fixture, or compatibility key.
- **Mechanical producer:** ordinary Python implementation and tests.
- **Evidence consumed:** local object graph or fixture data.
- **Consumer:** code paths and tests.
- **Temporal resolution:** call-local or test-local.
- **Persistence resolution:** none unless serialized or event-backed.
- **Constrains movement:** only mechanically.
- **Meaning claimed:** implementation container, compatibility object, fixture label.
- **Constitutional warrant found:** none from naming alone.
- **Fidelity finding:** **compatibility-only** or **Unknown**. Do not rename until the surrounding constitutional meaning is recovered.
- **Candidate Seed-native meaning, if warranted:** no automatic replacement.

## 2. First-pass material → shape → responsibility → question → produced meaning map

### Road 1 — Ledger events to current projected knowledge

- **Available material:** event ledger records, observations, facts, catalogs, inference rules, workspace identity, event order.
- **Candidate coordinates and relations:** subject/predicate/value triples; observation/evidence provenance; source confidence; predicate cardinality; entity type constraints; relationship definitions; event ids; timestamps.
- **Missing/conflicting material:** conflicting single-valued facts, unknown entity types, expired facts, unsupported relationships, absent observations.
- **Typed Unknowns preserved:** unknown type, graph validation issues, fact conflicts, unsupported or stale support.
- **Recognized evidence shape:** replayable event history plus catalog-governed evidence/fact graph.
- **Bounded responsibility:** State projection / knowledge projection.
- **Applicable local question:** “What projected knowledge is reconstructible from durable event history for this workspace now?”
- **Determination act:** replay events, apply known event types, finalize indexes/support/relationships/conflicts.
- **Produced meaning:** current projected knowledge and current-belief support; not original truth authority.
- **Persistence/projection behavior:** durable ledger; rebuildable projection; optional cache.

Before recognition, there were only event records and catalogs. The responsibility contributed ordering, application rules, cardinality interpretation, conflict preservation, and derived indexes. Those recognized relations made the current-knowledge question applicable.

### Road 2 — Projection cache freshness to cache posture

- **Available material:** saved projection snapshot, projection version, last event id, last event created timestamp, current ledger head, requested workspace/version.
- **Coordinates/relations:** snapshot workspace matches request; version matches; snapshot last event matches ledger head; dependent summary/index snapshots name their source projection version and last event id.
- **Absences/conflicts:** missing snapshot; version mismatch; stale last event id; incompatible dependent snapshot.
- **Recognized evidence shape:** cache compatibility/freshness evidence.
- **Bounded responsibility:** ProjectionStore/cache consumer.
- **Applicable local question:** “Can this cached projection be reused for this workspace/version/head?”
- **Determination act:** load, compare version/head metadata, reuse or rebuild.
- **Produced meaning:** cache availability/freshness posture, not knowledge standing.
- **Persistence/projection behavior:** persisted cache remains subordinate and replaceable.

Here evidence availability is not relevance unless identity/version/head coordinates match; relevance is not authority because ledger remains source.

### Road 3 — Fact support to support standing/current belief

- **Available material:** fact events, support facts, source evidence, confidence, observed_at/expires_at, predicate cardinality.
- **Coordinates/relations:** same subject+predicate+value grouping; conflicting values for single-valued predicates; freshness window; source strength; inferred vs observed support.
- **Absences/conflicts:** no support for a value, expired support, contradictory support, inferred-only support.
- **Recognized evidence shape:** support aggregate with conflict/freshness coordinates.
- **Bounded responsibility:** Fact support/current-belief projection.
- **Applicable local question:** “Which value is currently best supported, and what remains conflicted or stale?”
- **Determination act:** aggregate support, apply expiry/cardinality/confidence rules, select representative current belief where supported.
- **Produced meaning:** support standing, current belief, conflict posture, stale condition.
- **Persistence/projection behavior:** facts/evidence durable; support/current belief rebuildable.

This road shows result fields do not automatically equal constitutional standing: `verified`, `stale`, or `unknown` become standings/conditions only when tied to local support rules and question.

### Road 4 — Capability inventory to verification standing and availability presentation

- **Available material:** projected ToolNeeds, registered operation specs, `capability_verified` fact supports, requested capability names.
- **Coordinates/relations:** admitted capability facts vs executable operation contract metadata vs requested gaps; expiry; fact support; provider-reported vs verified values.
- **Absences/conflicts:** missing verification facts, stale verification, operation metadata without capability admission, requested need without proof.
- **Recognized evidence shape:** separated inventory sources plus support/freshness classification.
- **Bounded responsibility:** capability inventory presentation.
- **Applicable local question:** “What capability labels are visible in inventory and what verification standing do projected facts support?”
- **Determination act:** union inventory sources without collapsing ownership, classify each entry.
- **Produced meaning:** verification standing or freshness condition for presentation; operation metadata availability remains separate.
- **Persistence/projection behavior:** transient inventory built from projection; facts/events durable; operation metadata configured/registered.

This is a fidelity-pressure road: `ToolNeed` and registered-operation vocabulary is mechanical and compatibility-bound, not Seed-native grammar.

### Road 5 — Shared explanation membership to local classification outcome

- **Available material:** bounded inquiry reference, bounded demand, candidate projection/source identity, preserved lineage evidence, positive/incompatible/missing references.
- **Coordinates/relations:** same bounded inquiry identity; target lineage references; incompatible lineage references; missing lineage references; duplicate source identity.
- **Absences/conflicts:** missing lineage produces unknown; positive plus incompatible produces conflict.
- **Recognized evidence shape:** membership evidence set relative to one bounded inquiry/demand/candidate.
- **Bounded responsibility:** shared explanation membership evidence projection.
- **Applicable local question:** “Does this candidate belong to this bounded demand's membership evidence set?”
- **Determination act:** classify as belongs/does_not_belong/unknown/conflict from supplied references only.
- **Produced meaning:** membership classification outcome, not semantic relevance, ranking, selection, or authority.
- **Persistence/projection behavior:** projected record/test output; no event ledger mutation or cluster mutation.

This road proves material arrangement is not recognized evidence shape: shared wording or artifact fields are not enough; lineage references become relevant only for the membership responsibility.

### Road 6 — Admission/applicability/reachability to local standing

- **Available material:** local question form, candidate artifact, bounded context, required references, conflict/unknown references, same-input identity checks.
- **Coordinates/relations:** candidate-to-question fit; demand identity; responsibility-local exclusions; conflict references; evidence sufficiency.
- **Absences/conflicts:** candidate outside bounded input, unsupported evidence, conflict, no positive support.
- **Recognized evidence shape:** admission/applicability/reachability evidence relative to a local question.
- **Bounded responsibility:** interpretation applicability, downstream admission, capability reachability, representation grammar applicability, or neighboring classifier.
- **Applicable local question:** “Is this candidate applicable/admitted/reachable for this bounded question?”
- **Determination act:** local classifier returns admitted/applicable/supporting/blocked/unsupported/unknown/conflicting.
- **Produced meaning:** local standing or posture.
- **Persistence/projection behavior:** mostly transient/reconstructible; sometimes diagnostic/report durable.

This road supports shared recognition pressure across responsibility families, but not a universal schema. The recurring grammar is question-relative evidence recognition.

### Road 7 — External provider rows to provider-reported condition

- **Available material:** command/API output rows with provider fields such as active/sub/unit-file state or git status.
- **Coordinates/relations:** provider identity, subject id, field name, raw value, observation time, parser/source boundary.
- **Absences/conflicts:** missing field, parser mismatch, provider-specific unknown value, source unavailable.
- **Recognized evidence shape:** provider testimony preserved as observation material.
- **Bounded responsibility:** source adapter / observation normalizer.
- **Applicable local question:** “What did this provider report about this subject at observation time?”
- **Determination act:** parse/preserve raw values, map where catalog-supported, avoid execution/mutation.
- **Produced meaning:** provider-reported condition; not Seed constitutional state.
- **Persistence/projection behavior:** observation/evidence may be durable; provider vocabulary remains external.

This road distinguishes evidence availability from relevance and relevance from authority.

### Road 8 — Lifecycle objects to posture/outcome/phase

- **Available material:** creation/update events for goals, needs, pending actions, approvals, decisions, execution reports.
- **Coordinates/relations:** object identity; causation event; status value; actor; policy/validation result; timestamps.
- **Absences/conflicts:** missing update, contradictory status events, stale pending work, policy denial.
- **Recognized evidence shape:** lifecycle history for one object under one service boundary.
- **Bounded responsibility:** object-local lifecycle projector/service.
- **Applicable local question:** “What is this object’s current posture/outcome/phase after recognized lifecycle evidence?”
- **Determination act:** apply lifecycle event/order rules.
- **Produced meaning:** lifecycle posture, execution outcome, approval condition, phase.
- **Persistence/projection behavior:** events durable; posture rebuildable.

This road remains partly Unknown because each object’s lifecycle grammar needs local constitutional recovery.

## 3. Warranted Seed-native replacements already supported

These replacements are warranted as meanings, not as immediate code edits:

1. `State` meaning current world model derived from the event ledger → **current projected knowledge** / **projected knowledge**.
2. `StateProjector` meaning replay/finalize responsibility → **projection builder** or **knowledge projector**.
3. `State Views` → **read-only projection views**.
4. `ProjectionStore` `state` cache language → **projection cache** / **projection snapshot**.
5. `state-cache-status` → **projection cache freshness/status**.
6. `state-build` where diagnostic → **projection build diagnostic**.
7. Fact/capability `stale` state → **freshness condition**.
8. Capability `verified/unverified/provider_reported/unknown` state → **verification standing** or **support condition**, with provider-reported kept separate.
9. Membership `belongs/does_not_belong/unknown/conflict` state → **membership classification**.
10. Admission/applicability result `state` → **local standing** or **applicability standing** when the bounded question is explicit.
11. External provider `state` fields → **quoted provider-reported condition**; preserve literal field names separately.

## 4. Unknown usages that must not be renamed yet

- Local variables and arguments named `state` where the subject is merely an implementation object and no constitutional responsibility has been recovered.
- Most lifecycle/status fields on goals, actions, approvals, decisions, execution records, and pending work until their local question and authority boundary are recovered individually.
- Historical reports using “constitutional inquiry state,” “identity state,” “access state,” “working-state activation,” “current work position,” or “state build” as presentation vocabulary without implementation-backed knowledge-reachability evidence.
- Architecture-level “distributed state machine” and “state transition” metaphors where no local evidence shape/responsibility/question is named.
- Compatibility tests and serialized fields that preserve API shape but do not testify to Seed-native meaning.
- Generated or fixture keys where provenance as Seed-owned, external, or compatibility-only is unclear.

## 5. Legacy external-grammar usages likely requiring neutralization rather than translation

- Provider fields such as systemd unit active/sub/unit-file `state`.
- Git branch/status/working-tree state phrases when quoting git porcelain or branch orientation.
- Kubernetes/container/runtime state values where present as imported/provider vocabulary.
- LLM-agent/tool ecosystem vocabulary: `tool`, `ToolNeed`, `ToolExecutor`, `ToolRegistry`, capability catalog as execution affordance, registered operation candidates, provider/handoff recommendations.
- JSON/YAML fixture fields copied from external systems.
- Compatibility API names whose primary obligation is preserving external caller shape.

Neutralization means boundary-preserving phrasing such as “provider-reported field,” “registered-operation metadata,” “compatibility field,” or “quoted external value,” not constitutional translation.

## 6. Contradictions and compressions hidden by one word

1. **Ledger authority vs projection output:** `State` can be rebuilt from ledger history, but the word often implies durable truth. Ledger is the durable authority; projection is reconstructible inspectability.
2. **Projection vs cache:** `state` names both the current projected knowledge object and reusable cache snapshots, hiding the difference between meaning and storage convenience.
3. **Current belief vs fact truth:** `current state` can mean best-supported belief, but multiple values and conflicts may remain preserved.
4. **Standing vs condition:** `verified`, `unverified`, `stale`, and `unknown` are not one kind. They include support standing, absence/insufficiency, freshness condition, and unresolved condition.
5. **Posture vs authority:** open/pending/blocked/resolved lifecycle values constrain movement locally, but do not automatically authorize or deny execution outside their boundary.
6. **Availability vs capability proof:** registered operations and catalog entries can make something visible or callable under policy, but do not prove Seed-native capability standing.
7. **Provider condition vs Seed meaning:** external `state` fields are evidence material until a Seed responsibility recognizes relevance and sufficiency.
8. **Presentation label vs preserved knowledge:** reports and diagnostics sometimes use `state` as a visibility label; operational instructions warn not to promote such labels without implementation evidence.
9. **Architecture metaphor vs local grammar:** “distributed state machine” compresses many local responsibilities and should not become a universal constitutional model.

## 7. Smallest repository-supported answers

### What distinct meanings are currently compressed beneath “state”?

At least these meanings are compressed: current projected knowledge; projection build output; projection cache snapshot; cache freshness; read-only projection view; fact support/current belief; contradiction/conflict posture; freshness condition; typed unresolved condition; membership/admission/applicability/reachability standing; lifecycle posture; execution outcome; provider-reported condition; compatibility field; implementation object; architecture metaphor; and LLM-agent/tool external grammar.

### What portion of an evidence shape exists before responsibility-local recognition?

Before recognition, repository evidence supports only available material: artifacts, rows, events, fields, names, timestamps, values, references, raw provider testimony, catalog entries, and absences/conflicts as encountered. Some coordinates and relations are physically present, but they are not yet constitutional evidence shape. The shape begins only when a bounded responsibility identifies which coordinates matter for a local question.

### What does the bounded responsibility contribute to the recognized shape?

The bounded responsibility contributes relevance selection, admissible coordinate resolution, relation typing, sufficiency thresholds, exclusion boundaries, Unknown/conflict preservation, temporal/freshness interpretation, and the local authority limit for what the recognition can produce. It does not turn all available material into evidence, all relevant material into sufficient proof, or all sufficient support into universal authority.

### How does a recognized shape make one local question applicable?

A recognized shape makes a local question applicable by assembling enough responsibility-relative coordinates to ask that question lawfully: for example, same workspace/version/head makes cache reuse askable; subject+predicate+value support with cardinality makes current-belief askable; bounded inquiry plus lineage references makes membership askable; provider row plus observation boundary makes provider-reported condition askable. Without the recognized relation set, the question is either premature, different, or Unknown.

### Which former “state” meanings are standings, conditions, postures, outcomes, phases, projections, freshness claims, or legacy grammar?

- **Standings:** verification standing, membership standing/classification, admission/applicability standing, support standing.
- **Conditions:** stale, unknown, unsupported, conflicted, provider-reported condition.
- **Postures:** open, pending, blocked, resolved lifecycle posture; reachability posture.
- **Outcomes:** policy result, execution result, classifier result, projection build result.
- **Phases:** lifecycle phases for goals/needs/actions/execution where locally warranted.
- **Projections:** current projected knowledge, projection views, summary projections, fact indexes, context views.
- **Freshness claims:** stale fact, cache freshness, latest observation/current sample.
- **Legacy grammar:** provider `state` fields; git/systemd/runtime state vocabulary; LLM-agent/tool vocabulary; compatibility API keys.

### Can the word `state` be completely removed without first recovering additional constitutional distinctions?

No. The word cannot be faithfully removed in one mechanical sweep. Some meanings already have warrant for Seed-native replacements, especially projected knowledge, projection views, projection cache, freshness condition, verification standing, and provider-reported condition. But many usages remain compatibility-only, local lifecycle posture, implementation container names, architecture metaphor, or unresolved report vocabulary. Removing `state` completely before recovering these distinctions would risk erasing Unknowns, translating legacy external grammar into false Seed grammar, or inventing a universal model the repository does not warrant.

## 8. First-pass finding on recognition grammar/root

Repository evidence supports a **recurring responsibility-local recognition grammar**, not a universal root registry or single state model. The recurring grammar is:

```text
available material
→ responsibility-selected relevant coordinates and relations
→ preserved absences/conflicts/Unknowns
→ recognized evidence shape
→ local question becomes applicable
→ bounded determination act
→ produced standing, condition, posture, outcome, phase, projection, or freshness claim
```

The same pattern recurs across projection, cache freshness, fact support, capability inventory, membership evidence, admission/applicability/reachability, provider observations, and lifecycle posture. However, the repository does not yet prove one recognition grammar per responsibility, one per question form, or a universal shared grammar. The smallest supported answer is: **shared constitutional pressure with local mechanisms and local warrants**.

