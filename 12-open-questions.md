# 12 Open Questions

These are decisions to make while building the new repo.

## Product questions

1. Is Seed primarily local-first, hosted, or hybrid?
2. Should generated toolkits be shared between workspaces?
3. Is the first user a developer/operator or an end-user?
4. Should the system optimize for infrastructure ops first or generic personal/work tools?
5. What is the first demo scenario?

## Model questions

1. Which small model should be the design target?
2. Does the runtime model need native tool calling, or only structured JSON decisions?
3. When should the system escalate to a stronger model?
4. Should builder use a different model than runtime?
5. How are model prompts/versioned context templates evaluated?

## Runtime questions

1. Is event sourcing required from day one, or can append-only rows plus projections be enough?
2. Should state projections be rebuilt on demand or materialized?
3. What is the minimum API surface?
4. How should sessions and goals be linked?
5. How much of the context packet should be persisted?

## Tooling questions

1. What is the minimum valid toolkit?
2. Should toolkit manifests be YAML or JSON?
3. Should operation implementations be Python-only at first?
4. Should tools receive `ToolContext` as first arg?
5. How are dependencies declared and installed?
6. Can a toolkit include multiple risk classes?
7. How are tool versions selected in context?

## Builder questions

1. Is generation synchronous or queued?
2. Does the builder write directly to repo files or artifact storage?
3. Does builder open PRs for generated toolkits?
4. What validation is mandatory before registration?
5. Can generated toolkits modify existing toolkits?
6. Should generated mutating tools be disabled by default?

## Policy questions

1. Are policy rules static files, database rows, or code?
2. What is the default for unknown policy actions?
3. How granular are approvals?
4. Can approvals be delegated?
5. How are approvals revoked?
6. Are generated tools assigned higher default risk?

## Safety questions

1. What sandbox is used for generated code?
2. Are network calls allowed from generated code?
3. Are subprocesses ever allowed from generated code?
4. How are secrets exposed to tools?
5. How are logs redacted?
6. What is the maximum execution time for tools?

## Data questions

1. What database should be used first?
2. How are artifacts stored?
3. How are large tool outputs summarized?
4. How are stale facts expired?
5. How are conflicting facts represented?

## UX questions

1. How does Seed explain that a tool is missing?
2. How does it show Tool Need progress?
3. How does it ask for approval?
4. How does it explain generated toolkit risk?
5. How does a user disable a generated tool?

## Recommended initial answers

If you want to move fast:

```text
Runtime: local FastAPI or CLI
Database: SQLite
Toolkit manifest: YAML
Tool implementations: Python
Runtime model: swappable interface, fake model first
Builder model: manual/template first, stronger model later
Tool execution: in-process for core tools, sandbox later
Generated mutating tools: disabled or approval-required by default
Unknown policy action: approval-required or blocked
Context persistence: store full packet for early debugging
First demo: host_notes, then ssh_access plan
```
