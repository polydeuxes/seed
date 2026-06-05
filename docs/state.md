# State, State Views, and Evidence Graph

Seed's State layer turns append-only EventLedger data into a current world model.

## Terms

- **EventLedger**: historical source of truth.
- **ProjectionStore**: cached projection snapshots.
- **State**: current world model produced by the state projector.
- **State Views**: read-only projection views over State.
- **Evidence Graph**: read-only explanation layer over projected State that links evidence to facts.

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

The commands load projected State, use `ProjectionStore` cache when available, and render plain text. They never append events, invoke runtime behavior, call providers, evaluate policy, execute tools, run shell commands, mutate hosts, make network calls, or call LLMs.
