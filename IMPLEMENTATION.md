# Seed Prototype Implementation Status

This branch turns the seed blueprint into a runnable Python prototype. The current priority is the boring Session 8 MVP loop: append input, project state, compose context, accept a fake-model Decision, validate it, run the core echo tool or record a Tool Need, append the result event, and project state again in tests. Builder and generated-tool work should stay behind that checkpoint.

## Completed capabilities

- Runtime domain dataclasses for events, state objects, tools, tool needs, decisions, approvals, and policy decisions.
- In-memory and SQLite event ledgers with deterministic state projection.
- Toolkit manifest loading, tool registry, minimal JSON-schema validation, policy gating, and safe dynamic tool execution.
- Context composition and a fake-model runtime loop that can answer, ask questions, request tools, or call tools.
- Tool Need service with open-need deduplication and status-change events.
- Strict JSON model-decision parser and a dependency-light API shell for future web framework adapters.
- Builder candidate generation exists as a later milestone, but it is deliberately not part of the runtime MVP loop.

## Deliberate constraints

- Generated toolkit manifests are JSON documents stored as `toolkit.yaml`; this keeps the loader dependency-free while leaving room for a YAML adapter later.
- The executor only runs registered Python callables after schema validation and policy evaluation; it does not provide arbitrary shell execution.
- The builder emits untrusted stubs and validation reports rather than treating generated code as automatically safe.
- The API module is a framework-neutral shell, not a production HTTP server.

## Suggested next steps

1. Keep Session 8 tests green while extending only the fake-model runtime loop.
2. Add a real model adapter behind `ParsedDecisionModel` only after the fake loop remains stable.
3. Add deeper candidate sandboxing beyond bounded pytest execution and static import checks before promoting builder output.
4. Add generated toolkit versioning and artifact copy/registration into `toolkits/generated` after builder safety hardening.
5. Add a proper HTTP adapter once endpoint semantics stabilize.
6. Expand policy tables from risk-class defaults into workspace-specific configuration.
