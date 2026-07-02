# Competency Interrogation 002

## Selected competency

**Repository Artifact Observation Adapter**.

This interrogation selects Repository Artifact Observation because it is implementation-backed, explicit enough to answer identity and boundary questions, and less constitutionally mature than Documentation Structure Adapter. It has an adapter boundary, tests, and downstream consumers, but it does not have a public diagnostic inventory or diagnostic shape-audit surface comparable to `documentation_structure`.

The selected competency is not a universal repository observer. It is the Python repository-artifact structure adapter implemented in `seed_runtime/knowledge/repository_observation.py`.

## Implementation evidence reviewed

Implementation evidence reviewed in this interrogation:

- `seed_runtime/knowledge/repository_observation.py`
  - module-level refusal to read files, scan repositories, import modules, use LLMs, reconcile claims, or integrate with runtime/tool execution;
  - `RepositoryArtifactObservationAdapterBoundary`;
  - `RepositoryArtifactObservationAdapter.extract()`;
  - public compatibility helper `extract_repository_artifact_facts()`;
  - module, class, function, async function, direct method, import, and parse-failure fact construction.
- `seed_runtime/structure_observation.py`
  - substrate-independent Structure Observation owner;
  - split between shared read-only structural extraction and adapter-owned parsing, record schemas, traversal, and compatibility surfaces.
- `seed_runtime/knowledge/self_model_alignment.py`
  - `RepositoryArtifactFact` record consumed by self-model alignment;
  - supplied-record reconciliation boundary.
- `seed_runtime/knowledge/observation_agreement.py`
  - downstream candidate-agreement consumer of repository artifact observations.
- `tests/test_structure_observation.py`
  - adapter boundary assertions;
  - public extractor delegation and returned fact-shape preservation.
- `tests/test_observation_agreement.py`
  - repository artifact facts consumed as one independent observation stream;
  - non-promotion boundary for candidate agreement.
- App command run for this interrogation:
  - `python - <<'PY' ... RepositoryArtifactObservationAdapter().extract(...) ... PY`

## Interrogation matrix

Legend:

- ✓ Answered by implementation
- ? Partially supported / unanswered but meaningful
- ○ Not applicable at current maturity
- ✗ Unsupported / unknown

Question level legend:

- **Core** — needed for truthful bounded use of the competency now.
- **Advanced** — useful for mature public or multi-consumer governance, but not always required for this adapter.
- **Evolutionary** — future split, simplification, or maturation question; absence is not automatically a failure.

### Identity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What worker/surface is being interrogated? | ✓ | `RepositoryArtifactObservationAdapter` and its public helper `extract_repository_artifact_facts()` are being interrogated. The surface observes caller-provided Python source text and emits `RepositoryArtifactFact` records. |
| Core | What competency does it exercise? | ✓ | It exercises substrate-local structural observation for Python repository artifacts under the broader Structure Observation boundary. |
| Core | What bounded responsibility does it own? | ✓ | It owns deterministic extraction of module/file, top-level class, top-level function, top-level async function, direct class method, and top-level import facts from caller-provided Python source text. |
| Core | What does it explicitly refuse to own? | ✓ | It refuses file reads, repository scans, module imports, LLM use, claim reconciliation, runtime/tool execution integration, content interpretation, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation. |
| Core | Does implementation support separating worker, competency, and responsibility? | ✓ | Yes. The worker is the adapter/helper surface, the competency is Python repository-artifact structural observation, and the responsibility is record construction from supplied text. |

### Constitutional Authority

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Who may invoke this worker? | ? | Internal code and tests may invoke `extract_repository_artifact_facts()` or instantiate `RepositoryArtifactObservationAdapter`. No CLI or diagnostic inventory invocation is implemented. |
| Core | Who may consume its artifacts? | ? | `self_model_alignment` can consume `RepositoryArtifactFact` records for supplied-record reconciliation, and `observation_agreement` can consume them as one independent stream. A complete consumer registry is absent. |
| Core | Who may trust this artifact, and only as what? | ✓ | Consumers may trust emitted records only as deterministic structural facts about supplied Python text: existence of a module/file path string, observed definitions/imports, or parse failure. They may not trust them as repository-wide truth, runtime reachability, ownership, behavior, architecture, priority, or operator intent. |
| Core | What constitutional authority permits it to participate? | ✓ | The adapter declares `parent_owner = Structure Observation`, and Structure Observation permits read-only structural extraction while leaving substrate parsing and record schemas to adapters. |
| Core | What constitutional constraints limit it? | ✓ | It must remain read-only, supplied-text-bound, structural, deterministic, non-interpretive, non-reconciling, non-runtime, non-ledger-writing, non-mutating, and adapter-local. |
| Advanced | What would be an unlawful expansion of responsibility? | ✓ | Reading files on its own, scanning the repository, importing modules, interpreting symbol meaning, inferring ownership/responsibility, reconciling documentation claims internally, writing facts to a ledger, mutating repository/cluster state, or presenting itself as a repository-wide implementation inventory would exceed its authority. |

### Evidence

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What evidence can this worker observe? | ✓ | It observes only the `source_path` string and caller-provided Python source text, parsed through Python AST when possible. |
| Core | What evidence can it preserve? | ✓ | It preserves fact text, artifact kind, path, symbol, and parent symbol in `RepositoryArtifactFact` records. Parse failure is preserved by returning only a module/file fact with parse-failure wording. |
| Core | What evidence can it not observe? | ✓ | It cannot observe actual filesystem existence, repository completeness, runtime imports, call behavior, nested functions beyond its implemented direct traversal, documentation claims, operator intent, architecture, ownership, or cluster truth. |
| Core | What evidence permits movement? | ✓ | Movement from text to facts is permitted by AST node evidence for top-level classes/functions/async functions/imports and direct class methods; syntax failure permits only the bounded module/file parse-failure fact. |
| Core | What evidence causes lawful stop? | ✓ | Syntax failure stops structural extraction after the module/file parse-failure fact. Unsupported AST forms, nested definitions, behavior, ownership, and semantic claims are simply not emitted. |

### Boundaries

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Where does this worker begin? | ✓ | It begins with a caller-supplied `source_path` and `text`. |
| Core | Where does it end? | ✓ | It ends at a list of `RepositoryArtifactFact` records. It does not persist, reconcile, dispatch, execute, or mutate. |
| Core | Which neighboring responsibilities does it deliberately avoid? | ✓ | It avoids generic Structure Observation ownership, documentation structure, relationship extraction, repository traversal, source navigation explanation, claim reconciliation, observation agreement, runtime execution, grammar, responsibility recovery, lexicon stabilization, event-ledger writing, repository mutation, and cluster mutation. |
| Advanced | Which recurring implementation evidence supports those boundaries? | ✓ | The module docstring, adapter boundary fields, extraction implementation, structure-observation parent boundary, shape-preservation tests, and observation-agreement non-promotion tests all repeat the boundary. |

### Artifact Handoff

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What artifact leaves this worker? | ✓ | A list of `RepositoryArtifactFact` records leaves the worker. |
| Core | What minimum orientation survives? | ✓ | Artifact kind, source path, symbol, optional parent symbol, and human-readable fact text survive. |
| Core | What provenance survives? | ? | Path strings and symbols survive. Line numbers, byte spans, AST node locations, parser version, observation time, and observer identity do not survive. |
| Core | Who may consume the artifact? | ? | Self-model alignment, observation agreement, tests, and any internal caller accepting supplied `RepositoryArtifactFact` records may consume it. Exhaustive consumer authority is not implemented. |
| Core | Who may trust this artifact, and only as what? | ✓ | Downstream consumers may trust it as adapter-produced structure evidence from supplied Python text only. They may not trust it as proof that the file currently exists on disk, that the symbol is reachable, that architecture agrees, or that a responsibility is owned. |
| Core | What information is intentionally excluded? | ✓ | File contents beyond selected structural facts, filesystem proof, call graph, behavior, ownership, documentation meaning, claim truth, line provenance, event-ledger record, repository mutation, and cluster mutation are excluded. |

### Unknown / Stop

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What can remain unknown? | ✓ | Whether the supplied path exists, whether the text is current, whether a symbol is used, what behavior it implements, who owns it, whether documentation claims are true, and whether a downstream consumer should act can all remain unknown. |
| Core | What unsupported conclusions are refused? | ✓ | A class fact does not prove responsibility. An import fact does not prove dependency authority. A module/file fact does not prove current repository existence. A parse-failure fact does not prove absence of artifacts. |
| Core | How does the competency stop honestly? | ✓ | It emits only supported structural facts, returns only a parse-failure module fact on syntax errors, and omits unsupported observations rather than guessing. |
| Advanced | Which unanswered questions reveal real gaps? | ? | Consumer completeness, diagnostic inventory/shape-audit visibility, line-level provenance, and public invocation/governance are real gaps if this adapter is expected to become a public operational diagnostic surface. |
| Evolutionary | Which unanswered questions are inappropriate for this maturity level? | ○ | A universal competency registry, planner authority, repository-wide scan contract, and implementation framework are inappropriate to demand from this adapter; the current surface is intentionally a supplied-text extractor. |

### Locality

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Why is this competency local? | ✓ | It is local because it is Python-source-specific, AST-based, supplied-text-bound, and emits a specific record type. |
| Core | Why has implementation rejected universal ownership? | ✓ | Structure Observation keeps substrate-independent boundaries separate and says adapters own parsing, record schemas, traversal, and compatibility surfaces. |
| Advanced | What would fail if this competency became universal? | ✓ | It would wrongly apply Python AST assumptions to Markdown, relationship evidence, repository state, runtime observations, documentation claims, and architectural truth. |

### Continuity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What public compatibility contract exists? | ? | The public helper `extract_repository_artifact_facts(source_path, text)` and `RepositoryArtifactFact` shape are tested. No CLI, JSON schema, diagnostic inventory entry, or shape-audit registration exists for this adapter. |
| Core | What internal implementation freedom remains? | ✓ | The adapter can change internal parsing mechanics if it preserves the tested helper behavior, record shape, read-only boundary, and non-interpretive constraints. |
| Core | What identity survives implementation evolution? | ✓ | Supplied-text Python repository-artifact structural extraction survives; repository scanning, runtime execution, semantic interpretation, and mutation remain outside identity. |
| Advanced | How is compatibility drift detected today? | ? | Unit tests detect boundary-field drift and fact-shape drift. There is no operational diagnostic inventory or diagnostic shape-audit check for this surface. |

### Self-Observation / Drift

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | How can this competency be audited? | ✓ | It can be audited by tests and direct invocation of the adapter/helper. |
| Advanced | How is drift detected today? | ? | Drift is detected through `tests/test_structure_observation.py` and downstream observation-agreement tests. There is no app-visible diagnostic surface to audit it independently. |
| Advanced | What diagnostic evidence already exists? | ✗ | No diagnostic inventory registration, CLI flag, record-scope declaration, event-ledger declaration, or diagnostic shape-audit spec was found for Repository Artifact Observation. |
| Advanced | What important self-observation remains absent? | ? | Public operational visibility, exhaustive consumer mapping, line-level provenance, currentness/freshness markers, and shape-audit coverage remain absent. |

### Evolution

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Evolutionary | Why did this competency emerge? | ? | Prior structure-observation slices characterize it as an existing implicit Python repository-artifact substrate adapter later named beneath Structure Observation. Code alone shows the current boundary, not full historical causality. |
| Evolutionary | What architectural pressure produced it? | ? | Evidence suggests pressure to separate structural code artifact evidence from documentation claims, relationship facts, responsibility recovery, and runtime execution. This is partly implementation-backed and partly repository-artifact-characterized. |
| Evolutionary | What future evidence could split it? | ✓ | Independent consumers or tests for imports, method definitions, parse-failure records, line provenance, source navigation, or repository-wide artifact inventories could justify smaller workers. |
| Evolutionary | What future evidence could simplify it? | ✓ | If consumers only require existence of symbols, import extraction or method extraction could remain adapter internals or be removed without creating a separate competency. |

## Recurring implementation evidence

Recurring evidence supports the same bounded conclusion:

1. **The module boundary is explicit.** Repository artifact observation works only on caller-provided Python source text and refuses file reads, repository scans, imports, LLM use, claim reconciliation, and runtime/tool execution integration.
2. **The adapter boundary is explicit but implementation-local.** It names Structure Observation as parent, names Repository Artifact Observation Adapter as adapter owner, and declares read-only structural extraction, evidence preservation, Python parsing, specific artifact observation, record construction, and non-mutation.
3. **The extraction path is tiny and deterministic.** The adapter emits a module/file fact, parses AST when possible, emits selected top-level and direct-method facts, and stops at a bounded parse-failure fact on syntax errors.
4. **The public helper preserves compatibility.** `extract_repository_artifact_facts()` delegates to the adapter, and tests assert the returned fact shape.
5. **Downstream consumers preserve non-promotion.** Observation Agreement can consume repository artifact facts as one independent stream, but its tests require candidate-only non-promotion rather than architectural truth.
6. **The app can exercise the adapter only indirectly/directly through Python invocation.** No CLI diagnostic surface was found, which makes this competency less mature than Documentation Structure.

## Constitutional observations

Repository Artifact Observation Adapter can answer a bounded constitutional oral examination:

- **What worker/surface is being interrogated?** The Python adapter/helper in `seed_runtime/knowledge/repository_observation.py`.
- **What competency does it exercise?** Python repository-artifact structural observation.
- **What bounded responsibility does it own?** Construction of `RepositoryArtifactFact` records from supplied source text.
- **What can Seed trust it for?** Seed can trust it for deterministic structural observations over the supplied text only.
- **What must Seed refuse to infer from it?** Seed must refuse repository-wide truth, current filesystem truth, ownership, responsibility, architecture, runtime behavior, priority, selection, claim truth, and mutation authority.
- **Who may trust this artifact, and only as what?** Internal consumers may trust it only as one bounded evidence stream, not as final agreement, documentation truth, or implementation authority.
- **Which gaps are real?** Diagnostic visibility, consumer completeness, line provenance, freshness/currentness, and shape-audit coverage are real if this surface is promoted toward operational visibility.
- **Which unknowns are merely maturity-inappropriate?** Universal registry, planner/coordinator authority, and repository-wide scanning are not appropriate demands for this adapter.

## Unsupported answers

The following answers remain unsupported or only partially supported:

- A complete list of all legitimate consumers of `RepositoryArtifactFact` records.
- A public CLI invocation contract for Repository Artifact Observation.
- Diagnostic inventory registration or diagnostic shape-audit coverage for this adapter.
- Line-number, byte-span, parser-version, observation-time, or observer-version provenance.
- Proof that the supplied `source_path` exists in the current repository.
- Proof that emitted symbols are reachable, behavioral, owned, architecturally significant, or responsibility-bearing.
- Full implementation-only history of why this adapter emerged.

### Unanswered question classification

| Unanswered / partial question | Classification | Why |
| --- | --- | --- |
| Complete consumer map | consumer gap | Known consumers exist, but no exhaustive consumer registry was found. |
| Public CLI / diagnostic invocation | implementation gap | The adapter exists, but no operational diagnostic surface is registered. |
| Diagnostic inventory and shape-audit coverage | drift gap | Unit tests exist, but operational drift governance comparable to Documentation Structure is absent. |
| Line/byte/parser/time provenance | handoff gap | Records preserve path/symbol/parent but not precise source locations or observation metadata. |
| Whether supplied path exists now | authority gap | The adapter receives a path string; it does not read the filesystem. |
| Whether symbol implies ownership or responsibility | authority gap | Boundary explicitly rejects responsibility recovery. |
| Whether artifact facts should drive work selection | frontier | No selection authority is implemented, and adding one would be a different competency. |
| Whether to create a universal registry or planner | presentation-only | The interrogation method does not justify a registry/framework, and the adapter does not need one to remain truthful. |

## Constitutional oral examination

If Seed were asked to explain Repository Artifact Observation Adapter, he could answer truthfully only in bounded terms.

| Answer class | Result |
| --- | --- |
| Unknown | Complete consumer map; source currentness; line-level provenance; full emergence history; whether future consumers need public operational visibility. |
| Unsupported | Any claim that the adapter scans the repository, proves current filesystem truth, imports code, observes runtime behavior, owns architecture, recovers responsibility, stabilizes lexicon, writes event-ledger truth, mutates repository state, or ranks/selects work. |
| Operator-only | The supplied `source_path` string and supplied `text` are invocation inputs, not independently verified repository truth. |
| Presentation vocabulary | Fact prose such as `Class X exists` or `Import Y exists` is record orientation over supplied text, not a constitutional ownership claim. |
| Implementation-backed | Read-only Python AST structural extraction from caller-provided text; module/file fact emission; selected class/function/async function/direct method/import facts; parse-failure bounded stop; `RepositoryArtifactFact` construction; no interpretation, responsibility recovery, lexicon ownership, ledger writes, repository mutation, or cluster mutation. |

## Lawful termination

**Boundary characterized; drift gap preserved.**

This is smaller and more precise than broad implementation recovery. The interrogation recovers an implementation-backed competency and its lawful trust boundary, but the repository does not support treating it as mature in the same way as Documentation Structure. Repository Artifact Observation Adapter has a named boundary, tested helper behavior, and downstream candidate-only consumption. It lacks public diagnostic inventory, diagnostic shape-audit registration, CLI visibility, exhaustive consumer mapping, and rich provenance.

The lawful stop is therefore not implementation recovery. No requested operational surface was changed, and the adapter already truthfully refuses overreach. The smallest lawful stop is to characterize the boundary and preserve the drift/visibility gap for a future task only if repository authority later requires operational promotion.

## Remaining questions

- Should Repository Artifact Observation ever become a public diagnostic surface, or is supplied-text internal extraction sufficient?
- If it becomes public, should it be registered in diagnostic inventory and diagnostic shape audit with explicit record scope and mutation declarations?
- Which downstream consumers actually depend on `RepositoryArtifactFact`, and do they all preserve the supplied-text/non-promotion boundary?
- Would line-level provenance materially improve handoff, or would it imply a larger source-navigation responsibility?
- Are import facts, method facts, and parse-failure facts still one adapter-local record family, or are any becoming independent competencies?

## Confidence

**High** for bounded identity, supplied-text locality, read-only extraction, parse-failure stop, record construction, and explicit refusals.

**Medium** for consumer and drift conclusions, because known consumers and tests exist but there is no exhaustive consumer registry or operational diagnostic governance.

**Low** for historical emergence and future split/simplification paths, because those answers depend partly on repository characterization artifacts rather than executable implementation alone.
