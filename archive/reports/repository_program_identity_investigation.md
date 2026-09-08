# Repository / Program Identity Investigation

## Scope

This is a bounded implementation investigation into whether current Seed implementation distinguishes the identities named in the prompt:

```text
repository
program
language corpus
implementation
runtime artifact
responsibility-bearing system
```

The investigation is read-only with respect to implementation behavior. It does not recover ownership, import a repository, redesign observation, add probes, or introduce automation.

## Implementation evidence reviewed

- `seed_runtime/repository_observation.py`: repository-state observation model and git-backed provider.
- `seed_runtime/observation_sources.py`: observation source protocol, repository-source intake, and CLI ingestion path support.
- `seed_runtime/knowledge/relationship_observation.py`: Python import/definition relationship extraction and stated boundaries.
- `seed_runtime/observations.py`: canonical observation and ingestion/promotion path.
- `seed_runtime/inquiry_orientation.py`: inquiry note preservation and lexical related-material orientation boundary.
- `scripts/seed_local.py`: CLI flags for repository observation, repository-source observation, and bounded ask dispatch.
- Tests covering repository-state observation, repository-source observation, relationship observation, inquiry orientation, and CLI ingestion.
- Existing investigation `repository_neutral_program_review_investigation.md` as implementation-backed prior review context, especially its limits around repository observation and program-purpose recovery.

## Recovered implementation identities

### Repository state identity

`RepositoryObservation` is the strongest explicit repository-state identity. Its fields are repository path, VCS, head commit, branch, dirty state, untracked/modified/staged counts, remote presence, status availability, a reason for unavailable status, and explicit read-only flags. `GitRepositoryObservationProvider.observe()` resolves the provided path, verifies it is inside a git work tree, runs git status commands, and returns that repository-state record.

This identity is a git working-tree/status identity. It is not a program identity, source corpus identity, runtime identity, or responsibility identity.

### Repository source observation identity

`RepositorySourceObservationSource` is a read-only source adapter named `repository_source`. It accepts a `repository_root` plus include roots, discovers allowlisted Python files, reads their text, extracts Python import and definition relationship facts, and emits `Observation` records with `source_path`, `relationship_family`, and `repository_root` metadata.

This identity is a repository-root-scoped Python source relationship observation. It observes selected Python files under configured roots. It is narrower than a repository and narrower than a program.

### Language-corpus / language-adapter identity

`relationship_observation.py` defines `RelationshipFact` as a language-neutral relationship evidence record, but the implemented source adapters are Python-specific: static `import` / `from ... import ...` extraction and top-level class/function/async-function definition extraction from caller-provided source text.

This gives implementation evidence for a limited language implementation identity: static Python syntax relationships. It does not provide evidence of a general language corpus identity across all repository languages.

### Observation identity

`Observation` is the canonical external observation shape: id, source type, observed timestamp, subject, predicate, value, confidence, metadata, dimensions, and optional expiry. `ObservationIngestor` converts observations into evidence events and, unless suppressed, facts. This is an evidence/provenance identity, not a repository/program/runtime/responsibility identity.

### Runtime artifact identity

The reviewed surfaces do contain runtime-observation implementation elsewhere in `observation_sources.py`, such as `SeedRuntimeObservationSource`, which observes the current Seed runtime process and emits local process observations. However, repository-source observation does not identify executable entrypoints, execute code, load modules, prove calls, prove reachability, or prove behavior. Tests for repository-source observation explicitly assert absence of `calls` and `entrypoints` facts.

Therefore executable/runtime identity exists in Seed as a separate kind of observation for Seed's current process, but it is not derived from repository observation or repository-source observation.

### Inquiry identity

Inquiry surfaces are explicit but not semantic program recovery. `InquiryNoteRecord` preserves raw operator prose outside the event ledger. `build_inquiry_orientation()` performs deterministic lexical overlap against projected material and source navigation. Its authority boundary says the note is not a fact, goal, requirement, authorization, command, runtime instruction, ownership claim, intent, recommendation, or next safe move.

Bounded ask dispatch is also exact: `ask --question-family` maps an exact registered question-family identifier to existing surfaces and rejects unknown families or missing required surface arguments. That is an inquiry dispatch identity, not repository/program discovery.

### Responsibility-bearing identity

No reviewed implementation defines a general repository-program-responsibility object or automatically recovers responsibilities from repository state, source layout, imports, definitions, or inquiry notes. The closest current implementation-backed responsibility evidence is negative: relationship extraction explicitly says imports do not prove ownership, definition relationships do not prove runtime ownership, and inquiry orientation rejects ownership and intent inference.

Existing responsibility investigations evaluate Seed-native recovered responsibility families, but that is not evidence that an unfamiliar repository has a recovered responsibility-bearing system identity.

## Explicit implementation distinctions

### Repository state is distinct from cluster/runtime mutation

Repository-state observation carries `writes_event_ledger=False` and `mutates_cluster=False`; the CLI JSON test verifies those flags and verifies the git `HEAD` is unchanged before and after `--observe-repository`. This is an explicit boundary between read-only repository-state observation and mutation.

### Repository state is distinct from repository source relationships

`--observe-repository` reports git status metadata only. `--observe-repository-source` is a separate CLI flag described as read-only repository source intake for allowlisted Python files, emitting only imports and defines observations. These are separate implementation surfaces.

### Repository source relationships are distinct from behavior

Repository-source tests assert emitted facts are limited to `imports` and `defines`, and that no `calls` or `entrypoints` facts are produced. `relationship_observation.py` also states import relationships do not prove behavior, calls, routes, boundaries, or ownership; definition relationships do not prove invocation, behavior, reachability, capability authority, or runtime ownership.

### Language adapter is distinct from language-neutral relationship record

`RelationshipFact` is language-neutral, but the implemented extraction functions are named and documented as Python import and Python definition adapters. The current implementation therefore separates a generic record shape from a Python-specific adapter, while not implementing a general language-corpus model.

### Inquiry is distinct from semantic interpretation and responsibility recovery

Inquiry orientation preserves operator prose and lexical related material without promoting it to facts, requirements, intent, ownership, recommendations, or runtime instructions. Bounded ask dispatch requires exact question-family identifiers. This distinguishes inquiry presentation/dispatch from repository-program interpretation.

### Runtime observation is distinct from repository source observation

`SeedRuntimeObservationSource` is a separate observation source for the current process. Repository-source observation reads files and extracts syntax relationships; it does not execute repository code or observe process behavior.

## Implementation compressions

### Repository and program remain compressed or absent at the program boundary

Implementation evidence identifies git repository state and selected Python source relationships. It does not identify a first-class `Program`, program manifest, program boundary, product boundary, service boundary, build target, entrypoint set, testable unit, deployed unit, or intended purpose for an arbitrary repository.

The result is not that repository equals program in implementation. The safer finding is that `program` is mostly absent as an implementation identity, so repository observations may be discussed as program-review input without implementation evidence that they identify a program.

### Language corpus remains compressed into allowlisted Python source observation

The repository-source implementation observes Python files under include roots. It does not discover all languages, classify a multi-language corpus, identify generated/vendor/test/source roles beyond allowlisted roots and excluded paths, or relate language corpus identity to program identity.

### Implementation remains compressed into static source relationships

The current repository-source evidence is implementation-backed, but it is limited to static import and definition relationships. It does not identify semantic implementation responsibilities, architectural roles, behavioral contracts, routes, APIs, data flow, or execution paths.

### Runtime/executable behavior is not recovered from repository observation

Runtime observation exists for the current Seed process, but repository observation and repository-source observation do not identify executable behavior. Static imports and definitions are explicitly not behavior or reachability evidence.

### Responsibility-bearing system is not recovered from repository observation

Responsibility-bearing structure remains unsupported for unfamiliar repositories. Current evidence can support statements such as "module X imports Y" or "module X defines class Z"; it cannot support "module X owns responsibility R" without additional implementation evidence.

## Counterexamples investigated

### Repository treated as program

No reviewed code explicitly names a git repository as a program. The stronger counterexample is documentation/report language around repository-neutral program review that uses repository observation as review input. The implementation itself only exposes repository state and source relationships, so the compression is in absent program identity rather than an explicit `repository == program` assignment.

### Source tree treated as runtime

Repository-source observation does not emit `calls` or `entrypoints`; tests assert those are absent. The relationship adapter states it does not prove runtime reachability and never integrates with runtime/tool execution. This counterexample was rejected by implementation evidence.

### Imports treated as responsibilities

Rejected by implementation evidence. Import extraction says imports are dependency/name-availability evidence only and do not prove ownership. Tests only assert `imports` facts, not responsibility facts.

### Language treated as architecture

Partially rejected. The Python adapter does not claim architecture. However, the absence of a separate language-corpus identity means a reviewer could overread Python import/definition relationships as architecture unless the boundary text is preserved.

### Repository metadata treated as implementation semantics

Rejected for the repository-state implementation itself: the observed fields are VCS/status metadata. No reviewed code maps branch, commit, dirty state, or remote presence to program purpose or implementation responsibility.

## Answers to central questions

### 1. What implementation entity does Repository Observation actually observe?

Repository Observation observes a local git-backed working-tree/status entity: path, VCS, `HEAD`, branch, dirty state, untracked/modified/staged counts, remote presence, status availability, and unavailable reason. It does not observe program purpose, source semantics, runtime behavior, or responsibilities.

### 2. Does implementation distinguish repository from program?

Only negatively. It has an explicit repository-state identity, but no corresponding explicit program identity. Because there is no first-class implementation evidence for `Program`, the repository/program boundary remains implementation-compressed or underimplemented. The code does not prove repository equals program; it also does not prove how a program is identified inside or across repositories.

### 3. Does implementation distinguish program from language implementation?

No explicit program identity exists, while a Python static relationship adapter does exist. Therefore implementation distinguishes Python language relationships from repository state, but it does not distinguish program from language implementation because `program` is not implemented as a separate identity.

### 4. Does implementation distinguish language implementation from executable behavior?

Yes for the reviewed repository-source path. Static Python imports/definitions are explicitly bounded away from behavior, calls, invocation, reachability, capability authority, runtime ownership, and runtime/tool execution. Runtime process observation exists as a separate source, not as an inference from source syntax.

### 5. Does implementation distinguish executable behavior from recovered responsibilities?

Partly, but mostly by absence and negative boundaries. Execution/runtime observations and operational responsibility families exist elsewhere for Seed-native behavior, while repository-source relationships explicitly do not prove ownership or responsibility. There is no general recovered-responsibility identity for unfamiliar repository programs.

### 6. Which boundaries are already explicit?

- Repository-state observation vs mutation/event-ledger/cluster mutation.
- Repository-state observation vs repository-source observation.
- Static Python source relationships vs calls, behavior, runtime reachability, and runtime ownership.
- Language-neutral relationship record vs Python-specific extraction adapter.
- Inquiry note/lexical orientation vs facts, semantic interpretation, ownership, intent, recommendations, and commands.
- Exact question-family dispatch vs natural-language inquiry routing.

### 7. Which remain implementation-compressed?

- Repository vs program.
- Program vs language corpus.
- Language corpus vs complete implementation identity.
- Static implementation relationships vs executable behavior for arbitrary repositories.
- Executable behavior vs responsibility-bearing system for unfamiliar repositories.
- Repository metadata/source relationships vs program purpose.

## Supported conclusions

1. Seed currently knows how to observe a repository as git state.
2. Seed currently knows how to observe a bounded Python source subset as import/definition relationships.
3. Seed explicitly refuses to treat imports/definitions as behavior, reachability, ownership, capability authority, or responsibilities.
4. Seed has some runtime observation identity for its own current process, but repository observation does not produce runtime artifact identity.
5. Seed has inquiry surfaces and Seed-native responsibility investigations, but no implementation evidence that repository observation identifies an unfamiliar repository's program or responsibility-bearing system.

## Unsupported conclusions

- That a repository is equivalent to a program.
- That a source tree is equivalent to a runtime artifact.
- That Python imports identify responsibilities.
- That Python definitions identify executable behavior or ownership.
- That repository metadata identifies implementation semantics or program purpose.
- That Seed can honestly perform fully autonomous responsibility recovery for an unfamiliar repository from current repository observation alone.

## Confidence

High confidence for the observed implementation boundaries around repository state, Python imports/definitions, mutation flags, and lexical inquiry boundaries, because these are encoded in code and tests.

Medium confidence for the broader conclusion that `program` is absent rather than merely named elsewhere, because this investigation reviewed the requested surfaces and broad search results but did not exhaustively inspect every historical Markdown report.

Low confidence for any claim about future repository-neutral program review capability, because the prompt explicitly forbids new probes, ownership recovery, repository import, or redesign.

## Acceptance answer

Before Seed can honestly review an unfamiliar repository as a program, current implementation evidence shows it knows only some of what it is observing:

- It knows when it is observing git repository state.
- It knows when it is observing selected Python source syntax relationships.
- It knows those static relationships are not runtime behavior and not responsibilities.
- It does not yet know, in implementation-backed terms, what the repository's program is.
- It does not yet know how a language corpus maps to a program.
- It does not yet know how repository source maps to executable/runtime artifacts for arbitrary repositories.
- It does not yet know how executable artifacts map to a responsibility-bearing system for unfamiliar repositories.

Therefore the concepts remain materially implementation-compressed at the `repository -> program -> language corpus -> runtime artifact -> responsibility-bearing system` chain. The first distinction to recover should be the repository/program boundary, because without an implementation-backed program identity, later distinctions risk treating repository state or source syntax as program purpose, executable behavior, or responsibility evidence.

## Recommended next action

Do not recover ownership yet. Do not import repositories or add probes yet. The next bounded investigation should recover only the implementation evidence Seed would require to identify a `program` boundary separately from a git repository and from a Python source corpus. If that evidence is absent, stop with "insufficient implementation evidence" rather than promoting repository observation into program identity.
