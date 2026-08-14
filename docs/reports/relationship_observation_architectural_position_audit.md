# Relationship Observation Architectural Position Audit

## selected architectural question

Is `Relationship Observation` another substrate adapter beneath `Structure Observation`, or is it a substrate-independent companion capability that extracts relationship evidence across already-observed structures?

## implementation evidence

### Relationship Observation module boundary

`seed_runtime/knowledge/relationship_observation.py` describes `RelationshipFact` as a language-neutral relationship evidence record and describes Python import extraction as only the first adapter that emits that record. The module-level boundary also states that import relationships are dependency/name-availability evidence only, definition relationships are syntactic declaration evidence only, and the module does not read files, scan repositories, import repository modules, use LLMs, reconcile claims, build graphs, or integrate with runtime/tool execution.

The shared record is:

- `relationship_kind`
- `subject`
- `object`
- `path`
- `evidence`

The module emits the same record type from distinct relationship extractors:

- `documentation_navigation_relationship_facts(...)`
- `extract_python_import_relationship_facts(...)`
- `extract_python_definition_relationship_facts(...)`
- the compatibility wrapper `extract_relationship_facts(...)`

### Documentation navigation relationships use observed documentation metadata

Documentation navigation relationships do not parse markdown prose inside Relationship Observation. The documentation observation module observes front matter into `DocumentationMetadataObservation`, then passes the already-observed metadata fields into `documentation_navigation_relationship_facts(...)`.

That relationship helper explicitly says the caller supplies metadata already observed from YAML front matter and that it only maps explicit metadata fields to relationship facts using stable document, domain, and concept identities. This means the relationship layer owns conversion from observed navigation metadata into relationship facts, not documentation structural observation itself.

### Python import and definition relationships parse caller-provided Python text

The Python import and definition extractors parse caller-provided source text with `ast.parse(...)` and return an empty relationship list on invalid Python. They only inspect top-level import/definition syntax and emit `RelationshipFact` records.

Their documented boundaries are relationship-specific:

- import extraction emits only `imports` relationships from static Python import syntax.
- definition extraction emits only `defines` relationships for top-level Python function, async function, and class declarations.
- definition relationships are declaration evidence only, not call, behavior, reachability, capability authority, or runtime ownership claims.

### Compatibility wrapper is intentionally narrow

`extract_relationship_facts(...)` is explicitly not a general relationship extractor. It remains a compatibility wrapper for the v0 Python import relationship adapter and delegates to `extract_python_import_relationship_facts(...)`.

### Structure Observation owner boundary

`seed_runtime/structure_observation.py` defines `Structure Observation` as an implementation-local, substrate-independent owner for read-only structural extraction. Its boundary states that it does not own substrate parsing, grammar interpretation, responsibility recovery, lexicon stabilization, event ledger writes, repository mutation, or cluster mutation.

The same module says substrate adapters keep ownership of their parsing, record schemas, traversal, and compatibility surfaces. Current tests assert this owner string and boundary behavior.

### Recovered substrate adapter contrast

`RepositoryArtifactObservationAdapterBoundary` explicitly declares `parent_owner = STRUCTURE_OBSERVATION_OWNER`, `adapter_owner = "Repository Artifact Observation Adapter"`, Python parsing, module/class/function/method observation, repository artifact record construction, and the read-only/no-mutation boundary.

Relationship Observation does not currently expose an equivalent boundary object that declares itself as a `Structure Observation` adapter. Instead, it exposes relationship-specific constants, a shared relationship record, and multiple relationship extractors.

## current ownership

Relationship Observation currently owns relationship evidence record construction and relationship-specific extraction invariants. Its implementation-owned record is `RelationshipFact`, and its relationship kinds include `imports`, `depends_on`, `related_to`, `belongs_to_domain`, and `defines`.

It owns the following implementation responsibilities:

1. normalize relationship subjects and objects for supported relationship families;
2. emit a shared relationship record shape across documentation and Python relationship families;
3. preserve evidence text for each emitted relationship;
4. maintain bounded relationship semantics, especially by avoiding behavior, ownership, call, reachability, authority, graph, and runtime claims;
5. preserve compatibility for the v0 import-only `extract_relationship_facts(...)` wrapper.

It does not currently own repository traversal, file reading, event-ledger writes, cluster mutation, documentation front-matter observation, repository artifact facts, responsibility recovery, or lexicon stabilization.

## substrate analysis

Relationship Observation currently observes multiple structural domains rather than one substrate:

- Python import relationships from Python source syntax.
- Python definition relationships from Python source syntax.
- Documentation navigation relationships from documentation metadata observed elsewhere.

The implementation evidence against a single-substrate adapter interpretation is stronger than the evidence for it:

- all emitted records share `RelationshipFact` instead of separate substrate-specific records;
- documentation navigation relationships consume already-observed metadata rather than owning documentation parsing;
- Python import and definition extractors emit relationship semantics, not repository artifact facts;
- tests require isolation from runtime components and file reads;
- tests assert relationship facts are not documentation claims, repository artifact facts, or alignment records;
- relationship observation contains relationship-family invariants such as no call relationships, no ownership claims, and no runtime authority claims.

Evidence that could superficially support the substrate-adapter hypothesis is limited:

- the module docstring still calls Python import extraction the first adapter;
- Python import and definition extractors perform Python AST parsing over caller-provided text;
- `Structure Observation` documentation text mentions relationship extraction among substrate adapters.

However, repository implementation authority shows that the actual module has expanded beyond a single Python import adapter and now uses a shared relationship model across Python and documentation navigation domains.

## relationship to Structure Observation

Relationship Observation is structurally adjacent to `Structure Observation`, but the implementation does not establish it as another recovered substrate adapter.

The best-supported current position is:

> Relationship Observation is a substrate-independent companion capability beneath or alongside Structure Observation that extracts relationship evidence over structural inputs and already-observed structures.

This position fits the current code better than treating it as a substrate adapter because Relationship Observation does not own one substrate's structural extraction boundary. It owns relationship evidence construction across multiple structural domains.

## supported conclusions

1. **Relationship Observation owns relationship extraction, not general structural extraction.**
   It emits relationship-specific evidence records and explicitly avoids behavior, ownership, reachability, authority, graph-building, and runtime claims.

2. **Relationship Observation observes multiple substrates/domains.**
   It emits relationship facts from Python import syntax, Python definition syntax, and documentation navigation metadata.

3. **Relationship Observation owns relationship extraction over structures or structural inputs.**
   Documentation navigation facts are produced from metadata already observed by documentation observation. Python relationships are produced from caller-provided source text and bounded to import/definition relationships.

4. **Relationship Observation is not currently another recovered Structure Observation substrate adapter.**
   Unlike `Repository Artifact Observation Adapter`, it has no adapter boundary declaring a `Structure Observation` parent and a substrate-specific adapter owner.

5. **Recovering it as a substrate adapter would weaken the recovered ownership.**
   It would force a multi-domain relationship capability into a single-substrate shape, obscure the shared `RelationshipFact` model, and blur the distinction between structural extraction and relationship evidence extraction.

6. **The existing compatibility boundary is meaningful and should be preserved.**
   `extract_relationship_facts(...)` must remain the v0 import-only compatibility wrapper unless an explicit compatibility change is requested.

## unsupported conclusions

The current implementation does not support these conclusions:

- Relationship Observation is only a documentation adapter.
- Relationship Observation is only a Python source adapter.
- Relationship Observation owns repository traversal or source discovery.
- Relationship Observation owns documentation front-matter parsing.
- Relationship Observation owns repository artifact observation.
- Relationship Observation proves behavior, calls, routes, ownership, runtime reachability, capability authority, or graph-level truth.
- Relationship Observation should be renamed or recovered as an adapter as part of this audit.

## compatibility boundaries

Current compatibility boundaries that depend on the existing implementation include:

- `RelationshipFact` as the shared record shape for relationship evidence.
- `extract_python_import_relationship_facts(...)` emitting `imports` relationships from static Python import syntax.
- `extract_python_definition_relationship_facts(...)` emitting `defines` relationships for top-level Python function, async function, and class declarations only.
- `documentation_navigation_relationship_facts(...)` mapping explicit navigation metadata to `depends_on`, `related_to`, `belongs_to_domain`, and `defines` relationships.
- `extract_relationship_facts(...)` remaining a compatibility wrapper for Python import relationships only.
- `extract_documentation_navigation_relationship_facts(...)` in documentation observation using front-matter observation before delegating relationship record construction.
- `RepositorySourceObservationSource.collect()` combining Python import and definition relationship facts into observations with relationship metadata.
- Tests enforcing no file reads, no runtime module loading, parse-failure behavior, deterministic documentation navigation observation, no call relationship emission, no ownership claims, and isolation from documentation claims/repository artifact facts/alignment records.

## recommended next implementation step

Do not recover Relationship Observation as a substrate adapter now.

The smallest implementation-backed next step, if further work is requested, is to add an explicit relationship-observation boundary object or tests documenting its existing companion-capability role without changing public JSON, CLI, schema, event, ledger, grammar, lexicon, or naming surfaces. That future step should preserve `extract_relationship_facts(...)` as the narrow compatibility wrapper and should keep documentation metadata observation outside Relationship Observation.

## confidence

High.

The conclusion is based on direct implementation boundaries, shared record shape, multiple relationship extractors, delegation paths from documentation observation and repository source observation, and tests that enforce relationship-specific invariants. The main caveat is that some comments still use the word `adapter` for the initial Python import extractor, but current implementation evidence shows a broader relationship capability rather than a single recovered substrate adapter.
