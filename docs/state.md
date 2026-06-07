# State, State Views, Evidence Graph, and Confidence

Seed's State layer turns append-only EventLedger data into a current world model.

## Terms

- **EventLedger**: historical source of truth.
- **ProjectionStore**: cached projection snapshots.
- **State**: current world model produced by the state projector.
- **State Views**: read-only projection views over State.
- **Evidence Graph**: read-only explanation layer over projected State that links evidence to facts.
- **Contradiction Detection**: read-only projection view over projected facts and evidence that reports conservative conflicts without resolving them.
- **Confidence Aggregation**: read-only projection view over projected facts, evidence, and contradictions that estimates support strength without deciding truth.


## Current-State Temporal Semantics

`docs/state.md` is the canonical home for State temporal semantics. Seed's
State layer answers latest-current questions from projected state; it does not
provide a supported as-of event, as-of timestamp, belief timeline, why-then, or
semantic what-changed API.

Projection order is ledger append order. In-memory ledgers return events in the
order they were appended, and SQLite-backed ledgers return events in row
insertion order. Event timestamps, observation timestamps, evidence timestamps,
fact timestamps, support timestamps, projection snapshot timestamps, and
evidence graph timestamps are provenance, freshness, expiry, or cache metadata;
they do not determine projection replay order and they do not create a
projection-as-of-time query.

A projected `State` is the latest current world model after replaying all events
for the workspace and building derived indexes. Current fact selection is
projection logic over that latest projected state, using predicate semantics,
support, confidence, inferred/observed status, observation timestamps, and fact
IDs as deterministic tie-breakers where the existing query path does so. This is
not a general temporal reasoner.

Durable facts are retained in projected state unless they are expired or absent
from replay. For durable single-cardinality predicates, competing current values
can remain retained and conflicting rather than being automatically deleted,
superseded, rewritten, or resolved. For durable multi-cardinality predicates,
multiple values can remain current without being conflicts solely because more
than one value exists.

Measurement predicates have latest-current semantics. By default, projected
measurement state exposes only the latest current sample for the
subject/predicate/dimensions series, selected by `Fact.observed_at` plus fact ID.
A bounded `measurement_history_limit` can retain additional samples for
debug/read-only history, but that history is not durable truth arbitration and
does not make older samples current.

Fact expiry is a read-time current-state boundary. Expired facts remain stored in
projected `State.facts`, but default support, current-belief, and conflict
queries exclude them. Stale fact listing and refresh recommendations are
deterministic read views over expiry metadata; they do not mutate facts, lower
stored confidence, append refresh events, or call providers.

`ProjectionStore` owns latest-current projection snapshots only. A cached
snapshot is valid when it matches the latest event ID and projection identity; it
is invalidated by latest event ID mismatch rather than timestamp comparison. It
does not store historical projection snapshots as an as-of API and does not own
EventLedger history.

## State Views v1

`seed_runtime/state_views.py` exposes:

- `FactView`
- `ObservationView`
- `RequirementView`
- `CapabilityView`
- `IssueView`
- `StateSummary`

These views answer:

- What does Seed currently know?
- What facts exist?
- What requirements exist?
- What capabilities exist?
- What issues exist?

They use existing projected State structures and do not duplicate storage or create a secondary persistence system.

## Evidence Graph v1

`seed_runtime/evidence_graph.py` exposes read-only builders:

- `build_evidence_graph(state)`
- `build_fact_evidence_view(state, fact_id)`
- `build_evidence_summary(state)`
- `find_evidence_for_fact(state, subject, predicate, object=None)`

The Evidence Graph is derived from projected `State`, especially existing `Fact`, `FactSupport`, and `Evidence` records. It prefers projected State as its source and does not create a mutable evidence database. The flow is:

```text
Events -> projected State -> Evidence Graph -> Fact explanations
```

Evidence Graph v1 models:

- **EvidenceNode**: projected evidence metadata such as type, summary, source event/run IDs, confidence, and creation time.
- **EvidenceLink**: deterministic relationships from evidence to facts. The initial emitted relationship is `supports`.
- **FactEvidenceView**: a fact plus confidence, supporting evidence, supporting event IDs, and a plain-text explanation.
- **EvidenceSummary**: counts for evidence nodes, linked facts, unsupported facts, average confidence, projection version, and last event.

Facts without linked evidence are counted and rendered as unsupported. This makes unsupported assertions visible without mutating State or inventing a new persistence layer.

## Conflict and Contradiction Semantics

`docs/state.md` is the canonical home for State conflict semantics. Seed has
several read-only disagreement surfaces, not a unified truth-arbitration engine.
Facts are ledger-derived projected records, and contradictory later facts do not
rewrite, delete, or supersede older facts.

### Projection-level `FactConflict`

`FactConflict` is the projected-state conflict model for disagreements among
facts for one resolved subject, predicate, and dimensions scope. It records the
resolved subject, predicate, dimensions, observed values, optional winning value,
optional best fact ID, conflicting fact IDs, and a reason.

`StateProjector` derives `state.fact_conflicts` after replaying events, resolving
aliases, retaining measurement history, projecting inferred facts, projecting
fact supports, projecting relationships/types, and validating graph issues.
`State.get_fact_conflicts()` returns cached projected conflicts by default and
can recompute with expired facts included when requested.

Projection-level fact conflicts are created for non-expired facts unless
`include_expired=True`, non-measurement predicates, non-multi-cardinality
predicates, the same alias-canonical subject, predicate, and dimensions, and more
than one distinct value. If an unambiguous best fact can be selected,
`winning_value` and `best_fact_id` report it while `conflicting_fact_ids` points
to facts with other values. If no unambiguous best support exists, all grouped
facts are conflicting and the winning fields remain empty.

Multi-cardinality predicates intentionally preserve multiple values and do not
report those values as conflicts solely because multiple values exist.
Measurement predicates use latest-current sample semantics and treat prior
retained samples as history rather than durable disagreement. Descriptive local
substrate facts such as `kernel_release`, `kernel_version`, `cpu_model`,
`cpu_count`, and `memory_total_bytes` are durable facts: they can change after
upgrades or resizing, but they are not volatile availability, health,
performance, or memory-pressure measurements.

### Standalone `Contradiction` view

`seed_runtime/contradictions.py` exposes read-only builders:

- `build_contradictions(state, evidence_graph=None, exclusive_predicates=None)`
- `build_contradiction_summary(state, contradictions=None)`
- `find_contradictions_for_fact(state, fact_id, evidence_graph=None)`

The standalone contradiction view is derived from projected `State` facts and,
when supplied, the read-only `EvidenceGraph`. The flow is:

```text
Events -> projected State -> Evidence Graph -> Contradiction Detection
```

Contradiction Detection v1 starts with a conservative built-in exclusive
predicate set: `status`, `runs_on`, `located_on`, `ip`, `hostname`, `enabled`,
`available`, and `version`. It reports `Contradiction` records for exact
subject/predicate groups that have different values for an exclusive predicate.
It groups by exact `fact.subject_id`, does not use predicate-catalog
cardinality, ignores duplicate identical facts, ignores non-exclusive predicates
by default, and accepts caller-supplied exclusive predicates for future
extension.

Contradictions include the subject, predicate, conflicting fact IDs, values,
severity, reason, optional evidence by fact ID, supporting event IDs, last event,
and projection version. They are not resolutions: Seed does not choose a winner,
aggregate confidence, rewrite facts, delete facts, append events, call providers,
evaluate policy, execute operation implementations, run shell commands, mutate
hosts, make network calls, or call LLMs. The preferred failure mode is a false
negative rather than a noisy false positive.

### Graph validation issues

`GraphValidationIssue` is a graph-read-model issue, not a fact truth decision.
Graph validation reports suspicious or invalid relationship endpoints and type
mismatches as deterministic warnings/errors. It does not remove relationships,
alter entity types, rewrite aliases, block state projection, or resolve the
source facts that produced the issue.

### Explanation and confidence boundaries

`ExplanationBuilder.why(subject, predicate)` can expose current beliefs,
ambiguous values, competing beliefs, and an attached matching `FactConflict` for
single-cardinality predicates. For multi-cardinality predicates, it returns all
supports as current beliefs and does not attach conflict metadata solely because
multiple values exist. Seed has no explicit `why_not()` API and no negative
belief model.

Confidence penalties are limited to the separate read-only confidence projection.
Confidence Aggregation may apply a deterministic contradiction penalty to its own
`FactConfidence` records, but it does not change `Fact.confidence`,
`FactSupport.confidence`, projected current-belief selection, EventLedger data,
or State projection behavior.

Conflict lifecycle terms are intentionally narrow. `stale` is expiry/read-time
filtering; `superseded` exists for `ActionPlan` status events, not for facts,
supports, evidence, or conflicts; `disputed` is not a first-class state; and
`uncertain` is represented through confidence values, ambiguity, unsupported
reasons, unknown types, or no-current-belief statuses rather than a separate
fact/support/conflict lifecycle.

## Confidence Aggregation v1

`seed_runtime/confidence.py` exposes read-only builders:

- `build_fact_confidences(state, evidence_graph=None, contradictions=None)`
- `build_fact_confidence(state, fact_id, evidence_graph=None, contradictions=None)`
- `build_confidence_summary(state, fact_confidences=None)`
- `find_fact_confidence(state, subject, predicate, object=None, evidence_graph=None, contradictions=None)`

Confidence Aggregation is derived from projected `State`, the read-only `EvidenceGraph`, and read-only `Contradiction Detection`. The flow is:

```text
Events -> projected State -> Evidence Graph -> Contradiction Detection -> Confidence Aggregation
```

Confidence is support estimation, not truth. It does not resolve contradictions, choose winners, rewrite facts, delete unsupported facts, append events, invoke runtime behavior, call providers, evaluate policy, execute operation implementations, run shell commands, mutate hosts, make network calls, call LLMs, or persist a separate confidence database.

Confidence Aggregation v1 models:

- **FactConfidence**: one fact plus confidence, support count, contradiction count, unsupported/contradicted flags, reasons, and supporting event IDs.
- **ConfidenceSummary**: aggregate fact counts, support buckets, contradicted count, average confidence, projection version, and last event.

Scoring is intentionally simple and deterministic for v1:

- no evidence gives `0.0` unless the fact has explicit projected confidence
- one evidence node gives at least `0.50`
- two or more evidence nodes give at least `0.75`
- explicit projected fact confidence is preserved when higher than evidence-derived confidence
- contradicted facts are not resolved, but receive a deterministic confidence penalty
- confidence is clamped to `[0.0, 1.0]`

With State Views, Evidence Graph, Contradiction Detection, and Confidence Aggregation together, Seed can distinguish:

- unsupported facts
- weakly supported facts
- strongly supported facts
- contradicted facts

## CLI

The read-only CLI views are:

- `--current-facts`
- `--current-observations`
- `--current-requirements`
- `--current-capabilities`
- `--current-issues`
- `--state-summary`
- `--evidence`
- `--why-fact SUBJECT PREDICATE [OBJECT]`
- `--unsupported-facts`
- `--contradictions`
- `--confidence`
- `--confidence-fact SUBJECT PREDICATE [OBJECT]`

The commands load projected State, use `ProjectionStore` cache when available, and render plain text. They never append events, invoke runtime behavior, call providers, evaluate policy, execute operation implementations, run shell commands, mutate hosts, make network calls, or call LLMs.
