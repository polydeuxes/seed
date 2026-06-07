# Projection Integrity Drilldown Characterization

## Purpose

This document characterizes whether Seed can navigate from a Projection
Integrity Summary count to the underlying inventory that produced that count.
It is an audit of existing read models, views, and CLI surfaces. It is not an
implementation plan for a new CLI, subsystem, integrity engine, trust engine,
verification engine, refresh engine, planner, workflow engine, provider caller,
or LLM-generated reasoning layer.

The central finding is:

> A coherent **Projection Integrity Drilldown** surface is feasible almost
> entirely from existing structures. Most inventories already exist; the main
> gap is a single summary-to-inventory navigation convention that points each
> summary count at its existing read-only inventory.

Projection Integrity Summary can answer questions such as:

- `Unsupported facts: 12`
- `Fact conflicts: 3`
- `Contradictions: 3`
- `Graph issues: 4`
- `Stale facts: 2`
- `Refresh recommendations: 2`
- `Unverified capabilities: 8`

Projection Integrity Drilldowns ask the next operator question:

- Which 12 unsupported facts?
- Which 3 fact conflicts?
- Which 3 contradictions?
- Which 4 graph issues?
- Which 2 stale facts?
- Which 2 refresh recommendations?
- Which 8 unverified capabilities?

The repository already answers most of those questions through existing
projection-backed inventories. Composition and naming are the missing pieces, not
new execution behavior.

## Scope and non-goals

This characterization is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, `StateProjector`, runtime
routing, provider behavior, tool execution, orchestration, planning, fact
mutation, projection mutation, contradiction resolution, verification execution,
refresh execution, or LLM reasoning.

Integrity drilldowns are in scope only if they remain:

- **read-only**: derived from an already-built projected `State` and helper
  views;
- **projection-backed**: no new persistence, no alternate truth state, and no
  event appends;
- **evidence-backed**: provenance comes from facts/evidence already in projected
  state when evidence exists;
- **inventory-backed**: drilldowns list existing inventory records rather than
  inventing new judgments.

Integrity drilldowns must not become:

- `IntegrityEngine`
- `TrustEngine`
- `VerificationEngine`
- `RefreshEngine`
- `CapabilityExecutor`
- provider caller
- planner
- workflow engine
- agent loop
- parallel truth system
- LLM-generated trust system

Important distinctions preserved by this audit:

- Drilldown is not resolution.
- Inventory is not truth.
- Capability inventory is not verification execution.
- Refresh recommendation is not refresh execution.
- Contradiction inventory is not contradiction resolution.
- Graph issue inventory is not graph repair.
- Unsupported fact is not false.
- Unverified is not false.
- Unknown is not false.

## Files inspected

Required documents inspected:

- `docs/projection_integrity_summary_characterization.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/why_not_explanation_characterization.md`
- `docs/why_not_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/state.md`
- `docs/invariants.md`

Required runtime/read-model files inspected:

- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/facts.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/integrity_summary.py`
- `scripts/seed_local.py`

Relevant tests inspected:

- `tests/test_capability_inventory.py`
- `tests/test_contradictions.py`
- `tests/test_evidence_graph.py`
- `tests/test_fact_support_aggregation.py`
- `tests/test_graph_validation.py`
- `tests/test_integrity_summary.py`
- `tests/test_seed_local_script.py`
- `tests/test_state_views.py`
- `tests/test_temporal_characterization.py`

## Existing summary composition

`ProjectionIntegritySummary` is already a compact composition over existing
source signals. Its fields are counts for unsupported facts, fact conflicts,
contradictions, graph issues, stale facts, refresh recommendations, and
capability verification states.

The builder already accepts optional prebuilt source inventories for evidence
summary, fact conflicts, contradictions, graph issues, refresh recommendations,
and capability inventory. That is an architectural clue: the summary is already
intended to preserve source-view semantics rather than own a separate integrity
store.

However, the summary currently stores counts only. It does not include item IDs,
links, query names, or an embedded inventory payload. That is appropriate for a
summary, but it means the summary itself is not a direct drilldown object.

## Category findings

### Unsupported facts — Implemented

**Inventory exists:** yes. `unsupported_fact_views(state)` returns deterministic
`FactEvidenceView` records for facts that have no linked evidence in the Evidence
Graph.

**Builder exists:** yes. `build_evidence_graph(state)` creates fact evidence
views, and `build_evidence_summary(state)` counts unsupported facts.

**View exists:** yes. `FactEvidenceView` carries fact ID, subject, predicate,
object, confidence, evidence nodes, supporting event IDs, and an explanation.

**CLI exists:** yes. `--unsupported-facts` prints the unsupported-fact inventory.
`--evidence` prints the Evidence Graph summary and linked evidence list.
`--why-fact SUBJECT PREDICATE [OBJECT]` gives fact-level evidence explanation for
matching facts.

**Direct drilldown exists:** yes, but fragmented. Operators can go from
`Unsupported facts: N` to `--unsupported-facts` to list which facts are
unsupported, then use `--why-fact` for a specific subject/predicate/object. The
summary output itself does not print that navigation hint.

**Boundary:** unsupported means no linked evidence in the Evidence Graph view; it
is not false, contradicted, failed verification, or negative evidence.

### Fact conflicts — Implemented

**Inventory exists:** yes. `State.fact_conflicts` and
`State.get_fact_conflicts(include_expired=False)` expose projected
`FactConflict` records.

**Builder exists:** yes. Projection derives active fact conflicts, and
`get_fact_conflicts(include_expired=True)` can recompute with expired facts
included.

**View exists:** partially. `FactConflict` is an inventory model rather than a
`state_views.py` `*View` dataclass. It contains subject, predicate, dimensions,
values, winning value, best fact ID, conflicting fact IDs, and reason.

**CLI exists:** yes. `--fact-conflicts` prints active projected conflicts,
winning values, conflicting fact IDs, and expiry status; `--include-expired`
expands the query.

**Direct drilldown exists:** yes. The CLI inventory directly answers which
conflicts and which fact IDs are involved. Fact-level follow-up can use
`--fact-support`, `--best-fact`, `--current-facts`, `--why`, or `--why-fact`, but
there is no single conflict detail command by conflict ID.

**Boundary:** a fact conflict is a projection-level selection/disagreement signal
for facts. It is not contradiction resolution and does not prove the winning
value is globally true.

### Contradictions — Implemented

**Inventory exists:** yes. `build_contradictions(state, evidence_graph)` returns
read-only `Contradiction` records.

**Builder exists:** yes. The contradiction builder is intentionally conservative:
it groups exact subject/predicate facts, applies exclusive-predicate semantics,
and attaches evidence views when available.

**View exists:** yes. `Contradiction` includes a stable contradiction ID,
subject, predicate, fact IDs, values, severity, reason, evidence by fact ID, and
supporting event IDs.

**CLI exists:** yes. `--contradictions` prints summary counts, each
contradiction, values, fact IDs, evidence snippets, and supporting events.

**Direct drilldown exists:** yes. The contradiction inventory directly answers
which contradictions underlie the summary count. The module also has
`find_contradictions_for_fact(state, fact_id, evidence_graph)` for fact-centered
navigation, though the current CLI does not expose that helper directly.

**Boundary:** contradiction inventory is not contradiction resolution. It does
not rewrite facts, choose a truth, or merge with graph repair.

### Graph issues — Implemented

**Inventory exists:** yes. `State.graph_issues` and
`State.get_graph_issues(severity)` expose projected graph validation issues.

**Builder exists:** yes. Graph validation is part of state projection, and
`GraphValidator` emits deterministic `GraphValidationIssue` records for
suspicious or invalid graph edges.

**View exists:** yes. `build_issue_view(state)` creates compact `IssueView`
records with issue ID, summary, severity, and supporting event IDs. The native
`GraphValidationIssue` model carries more graph-specific detail such as subject,
relationship, object, expected/actual types, source fact IDs, relationship IDs,
severity, reason, and hint.

**CLI exists:** yes. `--graph-issues` prints graph validation issues and
`--severity warning|error` filters them. `--current-issues` exposes the generic
current Issue view. `--unhealthy --include-warnings` also surfaces graph errors
and optional warnings in an availability-oriented view.

**Direct drilldown exists:** yes. `--graph-issues` answers which graph issues are
present. The generic issue view is a lighter inventory and loses some native
graph detail, so `--graph-issues` is the better drilldown path.

**Boundary:** graph issue inventory is not graph repair and is not the same as a
fact conflict or contradiction.

### Stale facts — Implemented

**Inventory exists:** yes. `State.get_stale_facts()` returns expired projected
facts sorted deterministically.

**Builder exists:** yes. Staleness uses existing fact expiry semantics through
`Fact.expires_at` and `is_fact_expired(fact)`.

**View exists:** partially. Stale facts are returned as native `Fact` objects;
there is no dedicated `StaleFactView` dataclass. `FactSupport.expired` also
preserves expiry status for support-level queries.

**CLI exists:** yes. `--stale-facts` prints expired facts. `--include-expired`
can also affect fact support, best fact, current facts, and fact-conflicts query
surfaces.

**Direct drilldown exists:** yes. `--stale-facts` answers which stale facts
underlie the stale fact count, but it currently omits fact IDs. That makes it
sufficient for operator inspection by subject/predicate/value, but weaker for
ID-based navigation than `--fact-conflicts`, `--contradictions`, or capability
inventory.

**Boundary:** stale means expired or not current according to existing expiry
metadata. It is not false, deletion, confidence reduction, or a refresh action.

### Refresh recommendations — Implemented

**Inventory exists:** yes. `State.get_stale_fact_refresh_recommendations()`
returns `StaleFactRefreshRecommendation` records.

**Builder exists:** yes. Recommendations are deterministically derived from
stale facts and `recommended_capability_for_stale_fact(predicate)`.

**View exists:** yes as a domain model. Each recommendation carries fact ID,
subject, predicate, value, recommended capability, and reason. There is no
separate `state_views.py` view.

**CLI exists:** yes. `--stale-fact-refreshes` prints the recommendation
inventory.

**Direct drilldown exists:** yes. `--stale-fact-refreshes` answers which refresh
recommendations underlie the summary count and includes the stale fact ID.

**Boundary:** a refresh recommendation is not refresh execution, scheduling,
provider invocation, verification, or planning.

### Capability verification inventory — Implemented

**Inventory exists:** yes. `build_capability_inventory(state)` returns
`CapabilityInventoryEntry` records for the union of registered tool
capabilities, `ToolNeed` capabilities, and subjects of `capability_verified`
facts.

**Builder exists:** yes. The builder derives `verified`, `provider_reported`,
`stale`, `unverified`, and `unknown` from existing `capability_verified`
`FactSupport` records, expired support, and missing verification facts.

**View exists:** yes as capability inventory entries, with support summaries and
evidence summaries. There is also a generic `CapabilityView` in
`state_views.py`, but that view describes current capabilities/tool needs rather
than verification state.

**CLI exists:** yes. `--capability-status` prints deterministic JSON inventory
entries. `--current-capabilities` prints the generic capability view.

**Direct drilldown exists:** yes. `--capability-status` answers which
capabilities are verified, unverified, stale, provider-reported, or unknown, and
includes supporting fact/evidence information when present.

**Boundary:** capability inventory is not verification execution. A registered
operation, provider recommendation, catalog entry, or `verify_*` operation name
does not imply verification.

### Capability evidence/support summaries — Implemented

**Inventory exists:** yes inside `CapabilityInventoryEntry`. Verified,
provider-reported, stale, unverified-by-fact, and unknown-by-value entries can
include `supporting_facts`, `supporting_evidence`, and a
`CapabilitySupportSummary`.

**Builder exists:** yes. Capability evidence summaries reuse
`build_fact_evidence_view(state, fact.id)` rather than creating a parallel
evidence model.

**View exists:** yes. `CapabilityEvidenceSummary` carries evidence ID, type,
summary, confidence, and observation time. `CapabilitySupportSummary` carries
predicate, value, confidence, supporting fact IDs, source types, observation
times, expiry state, and expiry timestamp.

**CLI exists:** yes through `--capability-status` JSON.

**Direct drilldown exists:** partially. The JSON output contains the supporting
facts/evidence needed for drilldown. There is no capability-specific text
formatter or one-command jump from a capability entry to `--why-fact
CAPABILITY capability_verified`, but existing fact/evidence surfaces can answer
follow-up questions.

**Boundary:** support summary is an explanation of projected support, not proof
that a capability is executable now.

### Unknown capability status — Implemented

**Inventory exists:** yes. Capability inventory returns state `unknown` when a
`capability_verified` support value does not map to verified,
provider-reported, or unverified.

**Builder exists:** yes. `_state_from_value(value)` maps non-standard values to
`unknown`.

**View exists:** yes as a `CapabilityInventoryEntry` state, with support and
evidence details when the unknown state comes from a support record.

**CLI exists:** yes through `--capability-status` JSON.

**Direct drilldown exists:** yes. Operators can filter the JSON output for
`state == "unknown"`. The CLI does not currently provide a `--capability-status
--state unknown` filter, so navigation is present but not specialized.

**Boundary:** unknown is not false, failed verification, negative evidence, or
unavailability.

## Summary matrix

| Integrity signal | Status | Inventory exists? | Builder exists? | View exists? | CLI exists? | Direct drilldown exists? |
| --- | --- | --- | --- | --- | --- | --- |
| Unsupported facts | Implemented | Yes, `unsupported_fact_views` | Yes, Evidence Graph and Evidence Summary | Yes, `FactEvidenceView` | Yes, `--unsupported-facts`, `--evidence`, `--why-fact` | Yes, fragmented |
| Fact conflicts | Implemented | Yes, `State.get_fact_conflicts` | Yes, projection conflict builder | Partial, `FactConflict` domain model | Yes, `--fact-conflicts` | Yes |
| Contradictions | Implemented | Yes, `build_contradictions` | Yes | Yes, `Contradiction` | Yes, `--contradictions` | Yes |
| Graph issues | Implemented | Yes, `State.graph_issues` | Yes, graph validation projection | Yes, native issue plus `IssueView` | Yes, `--graph-issues`, `--current-issues` | Yes |
| Stale facts | Implemented | Yes, `State.get_stale_facts` | Yes, fact expiry semantics | Partial, native `Fact` only | Yes, `--stale-facts` | Yes, but weak ID display |
| Refresh recommendations | Implemented | Yes, `State.get_stale_fact_refresh_recommendations` | Yes, predicate-to-capability mapping | Yes, `StaleFactRefreshRecommendation` | Yes, `--stale-fact-refreshes` | Yes |
| Capability verification | Implemented | Yes, `build_capability_inventory` | Yes | Yes, `CapabilityInventoryEntry` | Yes, `--capability-status` | Yes |
| Capability evidence/support | Implemented | Yes, inside capability inventory | Yes, reuses fact evidence view | Yes, support/evidence summaries | Yes, `--capability-status` | Partially specialized |
| Unknown capability status | Implemented | Yes, capability inventory entries | Yes, value mapping | Yes, inventory state | Yes, `--capability-status` | Yes, but no state filter |

## Existing navigation paths

The repository already has practical navigation paths from summary counts to
inventory surfaces:

| Summary count | Existing drilldown path | Follow-up path |
| --- | --- | --- |
| Unsupported facts | `--unsupported-facts` | `--why-fact SUBJECT PREDICATE [OBJECT]`, `--evidence` |
| Fact conflicts | `--fact-conflicts` | `--fact-support SUBJECT PREDICATE`, `--best-fact SUBJECT PREDICATE`, `--why SUBJECT PREDICATE`, `--why-fact` |
| Contradictions | `--contradictions` | fact IDs in output can be followed through evidence/fact-support views |
| Graph issues | `--graph-issues`, optionally `--severity` | `--relationships`, `--entity-types`, `--current-issues` |
| Stale facts | `--stale-facts` | `--fact-support SUBJECT PREDICATE --include-expired` |
| Refresh recommendations | `--stale-fact-refreshes` | `--stale-facts`, `--capability-status` for recommended capability verification state |
| Verified/unverified/stale/provider-reported/unknown capabilities | `--capability-status` | `--why-fact CAPABILITY capability_verified`, `--current-capabilities` |

The main navigation gap is not missing inventory. It is that `--integrity-summary`
prints counts without naming the corresponding drilldown command or exposing a
structured map from count field to inventory query.

## Current read models and views

Existing read models relevant to drilldowns include:

- `EvidenceGraph`, `EvidenceSummary`, `FactEvidenceView`, and
  `unsupported_fact_views(state)` for evidence and unsupported-fact inventory.
- `FactSupport` for subject/predicate/value support groups.
- `FactConflict` for projection-level conflicting values.
- `Contradiction` and `ContradictionSummary` for conservative contradiction
  inventory and aggregate contradiction counts.
- `GraphValidationIssue` and `IssueView` for graph validation inventory.
- `Fact` plus expiry metadata for stale fact inventory.
- `StaleFactRefreshRecommendation` for refresh recommendation inventory.
- `CapabilityInventoryEntry`, `CapabilitySupportSummary`, and
  `CapabilityEvidenceSummary` for capability verification inventory.
- `StateSummary`, `FactView`, `ObservationView`, `RequirementView`,
  `CapabilityView`, and `IssueView` as generic current state views.
- `ProjectionIntegritySummary` for aggregate count composition.

The generic views are useful, but the best drilldowns usually come from the
source-specific inventory models because they preserve domain detail.

## What is only counts or implicit?

The only major count-only surface is the Projection Integrity Summary output
itself. Its source signals are mostly not count-only:

- Unsupported facts are count-only in `EvidenceSummary`, but inventory-backed by
  `unsupported_fact_views`.
- Contradictions are count-only in `ContradictionSummary`, but inventory-backed
  by `build_contradictions`.
- Capability counts are count-only in `ProjectionIntegritySummary`, but
  inventory-backed by `build_capability_inventory`.
- State summary graph counts are count-only in `state_summary(...)`, but
  inventory-backed by `State.get_graph_issues` and `build_issue_view`.

Partially implicit areas:

- Stale fact drilldown lists facts but omits fact IDs in the text formatter.
- Unknown capability status is present in JSON inventory but lacks a CLI state
  filter.
- Capability support/evidence details are present in JSON but not in a
  capability-specific text explanation surface.
- The summary does not advertise existing drilldown commands, so operators must
  already know the navigation vocabulary.

## Feasibility finding

A coherent integrity-drilldown surface is feasible from existing structures
without adding a new integrity engine or mutation behavior.

The minimal coherent model is a read-only map:

```text
summary field -> existing inventory builder -> existing CLI/read model -> caveat
```

No new source of truth is needed because each summary count already corresponds
to an existing inventory or near-inventory:

- `unsupported_fact_count` -> `unsupported_fact_views(state)`
- `fact_conflict_count` -> `state.get_fact_conflicts()`
- `contradiction_count` -> `build_contradictions(state)`
- `graph_issue_count` -> `state.get_graph_issues()` / `build_issue_view(state)`
- `stale_fact_count` -> `state.get_stale_facts()`
- `refresh_recommendation_count` ->
  `state.get_stale_fact_refresh_recommendations()`
- capability state counts -> `build_capability_inventory(state)` filtered by
  `entry.state`

This supports summary-to-inventory navigation while preserving source semantics.
The only category that would benefit from a small display improvement is stale
facts, where the existing CLI formatter does not show fact IDs even though the
native `Fact` inventory has IDs.

## Knowledge Integrity relationship

Projection Integrity Drilldowns are a Knowledge Integrity concern. They answer:

```text
Given an integrity signal in projected knowledge, which projected inventory
items explain that signal?
```

They do not decide whether Seed should trust, repair, execute, refresh, or
resolve anything. They expose already-derived integrity inventories so operators
can inspect support, provenance, conflicts, contradictions, graph issues,
staleness, refresh recommendations, and capability verification status.

This is consistent with existing Knowledge Integrity findings: the repository
already has integrity signals, and the missing piece has repeatedly been
composition and navigation rather than a new engine.

## Knowledge Selection relationship

Projection Integrity Drilldowns are adjacent to Knowledge Selection because
operators often drill down after a value was not selected, a capability was not
verified, or a current belief was ambiguous. Existing selection/explanation
surfaces already expose current beliefs, competing supported values, conflicts,
fact support, best facts, and evidence explanations.

The boundary is that drilldowns explain inventory and support; they do not select
answers for a response, choose a winning truth beyond existing projection
semantics, or invoke acquisition. Knowledge Selection may consume these views,
but drilldowns should not become selection policy.

## Complexity traps

Avoid these traps when thinking about future drilldown work:

1. **Turning navigation into resolution.** Listing contradictions must not choose
   truth or rewrite facts.
2. **Turning inventory into verification.** Capability inventory status must not
   execute tools, call providers, or treat catalog presence as proof.
3. **Turning refresh recommendations into refresh execution.** Recommended
   capability is a read-only hint, not a job, plan, or provider call.
4. **Collapsing distinct integrity signals.** Fact conflicts, contradictions,
   graph issues, unsupported facts, stale facts, and capability verification
   states have different semantics and should not be normalized into one generic
   truth score.
5. **Creating a parallel truth system.** Drilldowns should point at projected
   `State` structures, not maintain their own store.
6. **Using LLM reasoning as trust.** Drilldown text can explain existing
   records, but it must not create trust judgments that are not backed by
   projected evidence/inventory.
7. **Overfitting to CLI first.** The repository already has read models; any UI
   should preserve those source structures rather than inventing a CLI-only
   taxonomy.
8. **Mistaking absence for negative evidence.** Unsupported, unverified,
   unknown, stale, and not-believed are not false.

## Recommended smallest next step

Do not implement a new subsystem.

The smallest behavior-preserving next step is to document or add a read-only
navigation index for the existing Projection Integrity Summary fields:

- summary field name;
- human label;
- existing inventory builder/read model;
- existing CLI surface;
- caveat/boundary text.

If implemented later, this should be a small projection-backed map or formatter
adjacent to the existing summary, not a new engine. It should not append events,
mutate facts, execute verification, execute refresh, call providers, plan work,
or resolve contradictions.

A possible first documentation-only follow-up would be to add a short
"Drilldowns" section to the existing Projection Integrity Summary documentation
that maps each count to the already-existing inventory command listed above.

