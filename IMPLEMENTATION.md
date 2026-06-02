# Seed Prototype Implementation Status

This branch turns the seed blueprint into a runnable Python prototype. It completes the first runtime loop and builder milestones from the build plan while keeping the implementation dependency-light and testable.

## Completed capabilities

- Runtime domain dataclasses for events, state objects, tools, tool needs, decisions, approvals, and policy decisions.
- In-memory and SQLite event ledgers with deterministic state projection.
- Toolkit manifest loading, tool registry, minimal JSON-schema validation, policy gating, and safe dynamic tool execution.
- Context composition and a fake-model runtime loop that can answer, ask questions, request tools, or call tools.
- Tool Need service with open-need deduplication and status-change events.
- Builder candidate generation, candidate validation with bounded candidate-test execution, and registration flow for validated toolkits.
- Strict JSON model-decision parser and a dependency-light API shell for future web framework adapters.

## Deliberate constraints

- Generated toolkit manifests are JSON documents stored as `toolkit.yaml`; this keeps the loader dependency-free while leaving room for a YAML adapter later.
- The executor only runs registered Python callables after schema validation and policy evaluation; it does not provide arbitrary shell execution.
- The builder emits untrusted stubs and validation reports rather than treating generated code as automatically safe.
- The API module is a framework-neutral shell, not a production HTTP server.

## Suggested next steps

1. Add a real model adapter behind `ParsedDecisionModel`.
2. Add deeper candidate sandboxing beyond bounded pytest execution and static import checks.
3. Add generated toolkit versioning and artifact copy/registration into `toolkits/generated`.
4. Add a proper HTTP adapter once endpoint semantics stabilize.
5. Expand policy tables from risk-class defaults into workspace-specific configuration.
