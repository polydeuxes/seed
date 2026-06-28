# Structure Observation Substrate Responsibility Audit

## Selected architectural question

Is the current `Documentation Structure Probe` the architectural responsibility, or is it the documentation-substrate implementation of a broader `Structure Observation` responsibility?

This audit is bounded to implementation evidence. It does not rename surfaces, change CLI or JSON shapes, add runtime behavior, implement code observation, implement grammar interpretation, recover responsibility into code, or stabilize lexicon.

## Implementation evidence

### Documentation structure implementation

- `seed_runtime/documentation_structure.py` describes itself as read-only structural observation for repository Markdown documentation.
- Its main boundary text explicitly says it observes document structure only and excludes prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, event-ledger writes, and repository mutation.
- Its `DocumentationStructureRecord` stores document-local structural material: path, line/byte/blank/nonblank counts, trailing newline, front matter presence and keys, heading outline, section inventory, duplicate headings, link observations, code-block observations, architectural relation observations, and `structure_status`.
- `observe_documentation_structure()` observes only allowlisted top-level `docs/*.md` files, or one selected repo-relative `docs/*.md` file.
- `observe_markdown_document()` reads Markdown bytes, calculates mechanical metrics, observes front matter keys, code fences, headings, sections, links, and architectural relation forms, and returns a `DocumentationStructureRecord`.
- `documentation_structure_json()` preserves separate JSON modes for membership, drilldown, recurrence, and the default document-structure report.
- Recurrence, drilldown, membership, skeletons, common-section absence, and outlier rows are all derived from already observed documentation structure records.
- The architectural relation observations are record-shaped structural line matches with `left_term`, `relation`, `right_term`, `source_path`, `line_number`, and `evidence`; they are not emitted as `RelationshipFact` and are not interpreted as ownership, dependency, grammar, responsibility, or lexicon.

### Documentation structure CLI and diagnostic visibility

- `scripts/seed_local.py` exposes `--documentation-structure` as "observe read-only structural metadata for top-level repository Markdown docs".
- The same CLI surface exposes documentation-specific selection, detail, recurrence, drilldown, membership, and output-bound flags: `--document`, `--missing-front-matter`, `--missing-trailing-newline`, `--empty-sections`, `--sections`, `--links`, `--code-fences`, `--architectural-relations`, `--recurrence`, `--rare`, `--missing-common-sections`, `--outliers`, `--skeletons`, `--where`, `--membership`, `--limit`, `--top`, `--summary-only`, `--min-count`, and `--max-count`.
- The CLI constructs `DocumentationStructureOptions`, calls `observe_documentation_structure(REPO_ROOT, options, args.document)`, and then prints either `documentation_structure_json(report)` or `format_documentation_structure(report, options)`.
- Diagnostic inventory registers the surface as `documentation_structure`, not as `structure_observation`, and declares that it uses repository files, supports JSON, does not support record, has `record_scope="none"`, does not write the event ledger, and does not mutate the cluster.
- Diagnostic inventory description includes the expanded structural scope and explicitly says it operates over top-level repository docs without parsing code contents, interpreting prose, link text, grammar, responsibility, lexicon, extracting claims, inferring authority, inferring shapes, promoting ontology, writing events, or mutating the repository.
- Diagnostic shape audit has an implementation spec named `documentation_structure` with module path `seed_runtime/documentation_structure.py`, build function `observe_documentation_structure`, format function `format_documentation_structure`, JSON function `documentation_structure_json`, and the documentation-specific CLI flags.
- Tests assert the diagnostic inventory row, documentation-specific flag tuple, repo-file usage, JSON support, no record support, `record_scope="none"`, no event-ledger writes, and no cluster mutation.
- Tests assert the shape-audit surface checks `documentation_structure`.

### Relationship observation and repository/code artifact observation

- `seed_runtime/knowledge/relationship_observation.py` defines `RelationshipFact` as a language-neutral relationship evidence record.
- The same module says Python import extraction is the first adapter emitting that record, supports only caller-provided static Python import syntax, and never reads files, scans repositories, imports repository modules, uses LLMs, reconciles claims, builds graphs, or integrates with runtime/tool execution.
- `extract_python_import_relationship_facts()` parses caller-provided source text and emits `imports` relationship facts for top-level Python imports; invalid Python returns an empty list.
- `extract_python_definition_relationship_facts()` parses caller-provided source text and emits `defines` relationship facts for top-level functions, async functions, and classes; invalid Python returns an empty list.
- The relationship-observation module explicitly states imports are dependency/name-availability evidence only, not behavior, calls, routes, boundaries, or ownership; definition relationships are declaration evidence only, not invocation, behavior, reachability, capability authority, or runtime ownership.
- `extract_relationship_facts()` is a compatibility wrapper that delegates only to Python import relationship extraction and explicitly is not a general relationship extractor.
- `documentation_navigation_relationship_facts()` maps caller-supplied documentation front matter metadata into relationship facts without reading files, inspecting prose, inferring concepts, or reconciling graphs.
- `seed_runtime/knowledge/repository_observation.py` extracts structural repository artifact facts from caller-provided Python text. It always emits a module/file fact and, when parsing succeeds, emits class, function, async function, direct method, and import artifact facts. It never reads files, scans repositories, imports modules, uses LLMs, reconciles claims, or integrates with runtime/tool execution.
- Repository observation emits `RepositoryArtifactFact`; relationship observation emits `RelationshipFact`; documentation claim observation emits `DocumentationClaim`. Tests assert these record families remain isolated.
- Tests assert relationship observation does not load runtime components, does not read files, and does not emit call or ownership relationships.
- Tests assert repository observation does not emit documentation claims and documentation observation does not emit repository facts.

## Documentation-specific responsibilities

The current documentation structure probe owns the following documentation-substrate responsibilities:

1. **Markdown corpus selection.** It chooses top-level `docs/*.md` files and rejects selected documents outside top-level docs, non-Markdown paths, absolute paths, path traversal, and missing documents.
2. **Markdown mechanical metrics.** It counts lines, bytes, blank lines, nonblank lines, empty documents, trailing newline state, front matter presence, and front matter keys.
3. **Markdown heading and section structure.** It observes heading outlines, title heading presence, section inventory, section depth, skipped heading levels, duplicate heading labels, empty sections, and section skeleton signatures.
4. **Markdown link structure.** It observes raw Markdown link targets, relative-vs-external classification, under-docs classification, and local-doc broken-link counting.
5. **Markdown fenced-code-block structure.** It observes fence type, info string, language, line range, and closure state without parsing code contents.
6. **Documentation-specific recurrence.** It calculates recurrence over section labels, front matter keys, heading depths, code fence languages, link target classes, skeleton signatures, common missing sections, and structural outliers.
7. **Documentation-specific drilldown and membership.** It supports exact `section-label:<label>` occurrence drilldown and exact membership listing over the documentation corpus.
8. **Documentation-specific compatibility.** The public CLI flag, diagnostic inventory name, diagnostic shape-audit name, JSON keys, human text, test names, and option dataclasses all use documentation-specific vocabulary.

These are not generic structure-observation APIs today. They are implemented as documentation- and Markdown-specific code, names, records, options, CLI flags, and tests.

## Substrate-independent responsibilities

The following responsibilities appear substrate-independent in behavior, even though the concrete implementation is currently documentation-specific:

1. **Read-only observation of existing artifact structure.** Documentation structure and repository/code observation both inspect supplied or selected artifacts and produce bounded records without mutating the repository or cluster.
2. **Syntactic/mechanical extraction.** Documentation structure extracts headings, sections, links, code fences, and explicit relation-form lines; code/repository observation extracts AST-level module/class/function/method/import and import/definition relationships.
3. **Evidence preservation without promotion.** Documentation architectural relation observations preserve source path, line number, terms, relation token, and evidence text; relationship facts preserve relationship kind, subject, object, path, and evidence; repository artifact facts preserve artifact kind, path, symbol, parent symbol where applicable, and fact text.
4. **Boundary preservation.** Documentation structure excludes prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claims, authority, shape inference, event writes, and mutation. Relationship/code observation excludes behavior, calls, routes, ownership, runtime reachability, capability authority, file reads, repository scans, module imports, LLMs, reconciliation, graph building, and runtime/tool execution.
5. **Substrate adapters over structural records.** The documentation probe is effectively a Markdown/docs adapter. Python relationship and repository artifact observation are Python-source adapters. Each adapter exposes different record types, but the common pattern is structural observation of a substrate under strict non-interpretation boundaries.

These similarities support a broader responsibility candidate named `Structure Observation`, but the repository has not yet implemented a shared abstraction, registry, CLI surface, base record model, or migration path under that name.

## Relationship to code/repository artifact observation

The current code/repository artifact observer is plausibly another substrate-specific instance of the same broader responsibility, but not through a shared implementation abstraction.

Evidence supporting same broader responsibility:

- Both documentation structure and repository/code observation are read-only structural extraction surfaces.
- Both operate before grammar interpretation, responsibility recovery, lexicon stabilization, behavior inference, authority inference, and runtime execution.
- Both preserve observed structure with source/evidence boundaries.
- Both use deterministic parsing rather than LLM interpretation.
- Both have explicit tests preventing cross-boundary promotion: relationship facts are not documentation claims or repository artifact facts; repository facts are not documentation claims; documentation claims are not repository facts; code relationship observation does not emit call or ownership relationships.

Evidence against treating them as already unified:

- Documentation structure is a public diagnostic CLI surface with inventory and shape-audit declarations; repository/code artifact extraction is currently helper-level knowledge code exercised by tests, not a `--structure-observation` public surface.
- Documentation structure has a rich report model, recurrence report, drilldown report, membership report, human formatter, JSON formatter, diagnostic inventory row, and shape-audit spec. Repository/code observation has smaller extraction functions returning facts from caller-provided text.
- Documentation structure reads selected repository Markdown files; repository/code artifact extraction intentionally does not read files or scan repositories.
- Documentation architectural relation observations are stored as `DocumentationArchitecturalRelationRecord`, not as `RelationshipFact`; code import/definition relationships are `RelationshipFact` records.
- Documentation structure's recurrence and membership operations are corpus-level documentation features; code observation currently has no analogous recurrence, membership, skeleton, or corpus scan implementation.

Therefore, implementation evidence supports this conclusion: documentation structure probing and code/repository artifact observation are substrate-specific implementations of a broader structural-observation pattern, but the broader `Structure Observation` responsibility is not yet an implemented owner with its own API or compatibility surface.

## Compatibility surfaces

Compatibility currently depends on documentation-specific vocabulary in these places:

1. **CLI flags and help text.** `--documentation-structure` and its related flags are public operator vocabulary.
2. **Diagnostic inventory.** The registered diagnostic name is `documentation_structure`; its description names documentation structure, top-level repository docs, section labels, document metrics, front matter, Markdown links, fenced code blocks, and no code parsing.
3. **Diagnostic shape audit.** The implementation spec key and name are `documentation_structure`, pointing to documentation-structure functions and documentation-specific flags.
4. **JSON shapes.** Default output uses document-oriented keys such as `documents`, `summary`, `boundary`, `front_matter_keys`, `heading_outline`, `sections`, `link_observations`, `code_block_observations`, and `architectural_relation_observations`. Recurrence/drilldown/membership modes use documentation section labels and document counts.
5. **Human output.** Formatter output is organized around documentation structure, document rows, sections, links, code fences, recurrence, skeletons, architectural relations, drilldown, and membership.
6. **Python module/function names.** `seed_runtime.documentation_structure`, `observe_documentation_structure`, `DocumentationStructureRecord`, `DocumentationStructureOptions`, `format_documentation_structure`, and `documentation_structure_json` are documentation-specific names.
7. **Tests.** `tests/test_documentation_structure.py`, diagnostic inventory tests, and diagnostic shape-audit tests assert documentation-specific names and flag tuples.
8. **Existing docs/audits.** Multiple repository documents refer to `documentation structure` as an implemented diagnostic and visibility surface.

Any future migration would be mixed, not internal-only. Internals could potentially introduce a broader substrate abstraction without immediate public changes, but the current CLI, JSON, diagnostic inventory, shape-audit spec, tests, and docs create public and semi-public compatibility boundaries around the documentation-specific vocabulary.

## Supported conclusions

1. **The current probe owns read-only Markdown documentation structure observation.** It observes mechanical and structural Markdown/documentation properties and explicitly rejects grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, event-ledger writes, and mutation.
2. **Documentation is currently a substrate, not necessarily the whole responsibility.** The behavior resembles a substrate adapter over repository documentation artifacts: select substrate, parse structural forms, preserve bounded records, and avoid semantic promotion.
3. **Code/repository artifact observation shares the structural-observation pattern.** Python artifact and relationship extractors observe caller-provided source text, emit structural facts/relationship facts, and avoid runtime behavior, ownership, execution, graph building, and inference.
4. **The shared abstraction is implementation-backed as a pattern, not as a named owner.** There is no implemented `StructureObservation` class, CLI, diagnostic inventory row, shape-audit spec, common record protocol, or generic substrate registry.
5. **Documentation structure and code artifact observation are currently separate implementations with compatible boundaries.** They should be treated as separate compatibility surfaces until a future migration creates a tested shared owner.
6. **A rename would be mixed.** Internal refactoring could be staged, but public-facing names and JSON/diagnostic/CLI compatibility would need explicit preservation or migration because documentation-specific vocabulary is asserted in code, tests, and operator surfaces.

## Unsupported conclusions

1. **Unsupported: `Structure Observation` is already an implemented top-level responsibility.** The name is not present as a public owner or diagnostic surface with implementation authority comparable to `documentation_structure`.
2. **Unsupported: documentation architectural relation observations are grammar.** They are line-level structural relation-form observations and are not converted into grammar, responsibility, lexicon, ownership, dependency, or relationship facts by the documentation structure probe.
3. **Unsupported: code observation currently implements a repository-wide structure probe.** The repository/code artifact extractors work on caller-provided Python source text and intentionally do not read files or scan repositories.
4. **Unsupported: code observation owns execution, behavior, capability recovery, or runtime reachability.** Tests and module boundaries explicitly reject runtime loading, calls, ownership, behavior, and capability authority.
5. **Unsupported: documentation structure observation and code artifact observation can be renamed behind the scenes with no compatibility work.** Public CLI flags, diagnostic inventory, shape-audit specs, JSON keys, formatter output, and tests currently depend on documentation-specific vocabulary.

## Recommended next implementation slice

Do not rename yet.

The smallest safe next slice is an internal, non-public audit/test slice that characterizes the shared boundary without changing any CLI, schema, JSON, event, ledger, or runtime behavior:

1. Add no new user-facing surface.
2. Preserve `--documentation-structure`, `documentation_structure`, existing JSON keys, diagnostic inventory declarations, and shape-audit specs.
3. If implementation work is desired later, introduce an internal-only characterization test or small helper that compares existing documentation, repository artifact, and relationship observation boundaries under neutral terms such as read-only, substrate, structural extraction, evidence preservation, no inference, no runtime, and no mutation.
4. Only after that internal characterization is tested should a migration proposal decide whether to introduce a generic `StructureObservation` owner, substrate adapter registry, or compatibility alias.
5. If any future public diagnostic or CLI surface is added or renamed, update diagnostic inventory, diagnostic shape-audit specs, and tests according to the operational visibility contract.

## Confidence

High for the current documentation-structure responsibility and compatibility boundaries, because implementation, CLI, diagnostic inventory, shape-audit specs, and tests all directly assert them.

Medium-high for the broader substrate-specific interpretation, because the shared pattern is strongly present across documentation structure, relationship observation, and repository artifact extraction, but there is no implemented generic owner named `Structure Observation`.

Low for any claim about the final future architecture, because repository authority currently supports only the existing substrate-specific implementations and their bounded non-interpretation contracts.
