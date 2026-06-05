# State and State Views

Seed's State layer turns append-only EventLedger data into a current world model.

## Terms

- **EventLedger**: historical source of truth.
- **ProjectionStore**: cached projection snapshots.
- **State**: current world model produced by the state projector.
- **State Views**: read-only projection views over State.

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

## CLI

The read-only CLI views are:

- `--current-facts`
- `--current-observations`
- `--current-requirements`
- `--current-capabilities`
- `--current-issues`
- `--state-summary`

The commands load projected State, use `ProjectionStore` cache when available, and render plain text. They never append events, invoke runtime behavior, call providers, evaluate policy, execute tools, run shell commands, mutate hosts, or make network calls.
