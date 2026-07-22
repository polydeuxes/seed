# Seed Architecture

Seed documents its active architecture through bounded implementation witnesses rather than a universal runtime pipeline. Current implemented responsibilities include append-only event recording, state projection, observation, evidence, facts, relationships, read-only views, diagnostics, bounded inquiry, selection, and capability testimony where supported by code.

The canonical knowledge acquisition and selection relationship is documented in
[Knowledge Acquisition and Selection](knowledge_acquisition_and_selection.md):

```text
Observation -> Evidence -> Claim (Fact as normalized claim form) -> Projection
Projected Knowledge -> Context Composition -> Explanation -> Response
```

Knowledge Integrity sits between projected knowledge and selection as a
read-only characterization concern: it surfaces support, conflicts, confidence,
staleness, verification limits, graph issues, and source limitations so projected
knowledge can be interpreted safely before it is selected for context,
explanation, or response. The lifecycle relationship is summarized in
[Knowledge Lifecycle Reconciliation](knowledge_lifecycle_reconciliation.md), and
the integrity terminology is grounded in
[Knowledge Maintenance Reconciliation](knowledge_maintenance_reconciliation.md).

The knowledge explanation and verification flow is:

```text
Events -> projected State -> Evidence Graph -> Fact explanations
Events -> projected State -> Evidence Graph -> Contradiction Detection
Events -> projected State -> Evidence Graph -> Contradiction Detection -> Confidence Aggregation
```

- **EventLedger** is the authoritative historical event record. It is append-only and records what happened within Seed, without becoming a truth oracle about the world.
- **ProjectionStore** caches projection snapshots derived from EventLedger data. It is an optimization, not source-of-truth persistence.
- **State** is the current projected world model: facts, observations, relationships, entity types, requirements/goals, capabilities, ToolNeeds / capability gaps, and graph issues.
- **State Views** are read-only representations of projected State. They answer what Seed currently knows without reading raw events directly.
- **Evidence Graph** is a read-only explanation layer derived from projected State. It links Evidence records to Facts so Seed can explain why a fact exists, which projected evidence supports it, and which facts remain unsupported.
- **Contradiction Detection** is a read-only projection view derived from projected facts and the Evidence Graph. It reports conservative conflicts such as exclusive predicates with multiple values, includes evidence and supporting event IDs for each side, and never decides which fact is correct.
- **Confidence Aggregation** is a read-only projection view derived from projected State, Evidence Graph, and Contradiction Detection. It estimates support strength for each fact, but confidence is not truth and does not resolve contradictions.

State Views, the Evidence Graph, Contradiction Detection, and Confidence Aggregation are projections and are not second state stores. They do not append events, run shell commands, mutate hosts, perform network calls, call LLMs, or create separate persistence layers.

Evidence Graph v1 keeps the model intentionally small: projected evidence nodes support, contradict, mention, or derive from facts, with `supports` as the initial relationship emitted for fact evidence. Facts should become explainable through linked evidence rather than existing as unsupported assertions; unsupported facts are still shown explicitly so operators can identify knowledge gaps.

Contradiction Detection v1 is intentionally conservative. It starts with a small built-in set of exclusive predicates (`status`, `runs_on`, `located_on`, `ip`, `hostname`, `enabled`, `available`, and `version`) and reports only exact same-subject/same-predicate facts with different values. Contradictions are not resolutions: Seed can now distinguish unsupported facts, supported facts, and conflicting facts, but it does not rewrite, delete, rank, or resolve those facts automatically.

Confidence Aggregation v1 keeps scoring simple and deterministic. Evidence can raise a fact to weak support (`0.50`) or strong support (`0.75`), explicit fact confidence is preserved when higher, contradicted facts receive a deterministic penalty, and all confidence values are clamped to `[0.0, 1.0]`. This allows Seed to report unsupported, weakly supported, strongly supported, and contradicted facts, including facts that are contradicted but still better supported than alternatives, without treating confidence as automatic truth resolution.
