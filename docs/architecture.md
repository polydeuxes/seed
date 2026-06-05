# Seed Architecture

Seed follows this boundary-oriented flow:

```text
Input -> Events -> State -> Context -> Decision -> Policy -> Execution -> Events
```

- **EventLedger** is the historical source of truth. It is append-only and records what happened.
- **ProjectionStore** caches projection snapshots derived from EventLedger data. It is an optimization, not source-of-truth persistence.
- **State** is the current projected world model: facts, observations, relationships, entity types, requirements/goals, capabilities/tool needs, registered tools, and graph issues.
- **State Views** are read-only representations of projected State. They answer what Seed currently knows without reading raw events directly.
- **RuntimeLoop** coordinates one execution request.
- **DecisionJournal** records why a runtime decision was made and what happened afterward.
- **RuntimeTrace** reconstructs one runtime run for audit/explanation without replaying execution.

State Views are projections and are not a second state store. They do not append events, invoke the RuntimeLoop, call a DecisionProvider, evaluate policy, execute tools, run shell commands, mutate hosts, or perform network calls.
