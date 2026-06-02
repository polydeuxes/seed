# Seed Prototype Implementation Status

This branch turns the seed blueprint into a runnable Python prototype. It completes the first runtime loop and builder milestones from the build plan while keeping the implementation dependency-light and testable.

## Completed capabilities

- Runtime domain dataclasses for events, state objects, tools, tool needs, decisions, approvals, and policy decisions.
- In-memory and SQLite event ledgers with deterministic state projection.
- Toolkit manifest loading, tool registry, minimal JSON-schema validation, policy gating, and safe dynamic tool execution.
- Context composition and a fake-model runtime loop that can answer, ask questions, request tools, or call tools.
- Tool Need service with open-need deduplication and status-change events.
- Builder candidate generation, candidate validation, and registration flow for validated toolkits.
- Strict JSON model-decision parser and a dependency-light API shell for future web framework adapters.
- A harmless generated-style `host_notes` toolkit that mutates only Seed's own event ledger.
- A golden-case decision evaluation harness for checking model outputs against expected decision kind/tool/tool-need contracts.

## Deliberate constraints

- Toolkit manifests are JSON documents stored as `toolkit.yaml`; this keeps the loader dependency-free while leaving room for a YAML adapter later.
- The executor only runs registered Python callables after schema validation and policy evaluation; it does not provide arbitrary shell execution.
- The builder emits untrusted stubs and validation reports rather than treating generated code as automatically safe.
- The generated-style `host_notes` toolkit is checked in as a demo artifact; it proves the safe registration/execution path without remote infrastructure.
- The API module is a framework-neutral shell, not a production HTTP server.

## Suggested next steps

1. Add a real model adapter behind `ParsedDecisionModel` and run it through `DecisionEvaluator` cases.
2. Add candidate sandboxing/timeouts beyond the current import and pytest checks.
3. Add generated toolkit versioning and artifact copy/registration into `toolkits/generated`.
4. Add a proper HTTP adapter once endpoint semantics stabilize.
5. Expand policy tables from risk-class defaults into workspace-specific configuration.
