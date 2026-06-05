# Seed Architecture

Seed follows this boundary-oriented flow:

```text
Input -> Events -> State -> Context -> Decision -> Policy -> Execution -> Events
```

The knowledge explanation flow is:

```text
Events -> projected State -> Evidence Graph -> Fact explanations
```

- **EventLedger** is the historical source of truth. It is append-only and records what happened.
- **ProjectionStore** caches projection snapshots derived from EventLedger data. It is an optimization, not source-of-truth persistence.
- **State** is the current projected world model: facts, observations, relationships, entity types, requirements/goals, capabilities/tool needs, registered tools, and graph issues.
- **State Views** are read-only representations of projected State. They answer what Seed currently knows without reading raw events directly.
- **Evidence Graph** is a read-only explanation layer derived from projected State. It links Evidence records to Facts so Seed can explain why a fact exists, which projected evidence supports it, and which facts remain unsupported.
- **RuntimeLoop** coordinates one execution request.
- **DecisionJournal** records why a runtime decision was made and what happened afterward.
- **RuntimeTrace** reconstructs one runtime run for audit/explanation without replaying execution.

State Views and the Evidence Graph are projections and are not second state stores. They do not append events, invoke the RuntimeLoop, call a DecisionProvider, evaluate policy, execute tools, run shell commands, mutate hosts, perform network calls, call LLMs, or create separate persistence layers.

Evidence Graph v1 keeps the model intentionally small: projected evidence nodes support, contradict, mention, or derive from facts, with `supports` as the initial relationship emitted for fact evidence. Facts should become explainable through linked evidence rather than existing as unsupported assertions; unsupported facts are still shown explicitly so operators can identify knowledge gaps.
