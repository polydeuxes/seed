# Repository Observation Richness Audit

## Status

Investigation only. This document does not implement repository-observation richness, add MCP integration, extend source observation, modify source navigation, change relationship extraction, alter projection behavior, or introduce an external AST/ASG provider.

## Audit question

```text
What source-structure observations would materially increase repository understanding?
```

This audit begins from Seed repository-understanding needs, not from AST capability. The question is not what a parser can emit. The question is which preserved observations would make Seed better at answering operator questions about its own repository while preserving authority boundaries.

## Files inspected

Implementation and tests inspected:

- `seed_runtime/observation_sources.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/observations.py`
- `seed_runtime/knowledge/self_model_alignment.py`
- `tests/test_observation_sources.py`
- `tests/test_repository_observation.py`
- `tests/test_relationship_observation.py`
- `tests/test_source_navigation.py`
- `tests/test_seed_local_script.py`
- `tests/test_self_model_acquisition_pipeline.py`

Repository authority documents inspected:

- `docs/repository_observation_characterization.md`
- `docs/repository_observation_design.md`
- `docs/repository_observation_frontier.md`
- `docs/repository_observation_source_design.md`
- `docs/repository_observation_implementation_inventory_audit.md`
- `docs/repository_observation_external_tooling_audit.md`
- `docs/source_definitions_and_entrypoint_observation_reconciliation.md`
- `docs/source_observation_queryability_audit.md`
- `docs/source_observation_duplicate_fact_audit.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_query_surface_design_audit.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/source_navigation_practical_validation_audit.md`
- `docs/relationship_observation_v0_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/relationship_frontier.md`
- `docs/claim_support_frontier.md`
- `docs/repository_reconciliation_frontier.md`
- `docs/repository_reconciliation_v1_frontier.md`
- `docs/knowledge_navigation_layers_frontier.md`

## Current preserved repository observations

### Inventory summary

| Preserved observation type | What is observed | What becomes evidence | What becomes fact support | Current consumers / surfaces |
| --- | --- | --- | --- | --- |
| Python import relationship | A Python module syntactically imports a module or name. | The relationship evidence text, subject module, predicate `imports`, object value, source path, repository root, source metadata, and observation metadata become evidence through normal observation ingestion. | A `FactSupport` group keyed by subject module, predicate `imports`, value, and dimensions such as `path`; repeated ingestion should accumulate supporting fact IDs rather than require duplicate visible facts. | `--observe-repository-source` acquisition path, `--current-facts`, `--fact-support`, `--why-fact`, relationship/current fact filters, and source navigation over preserved `imports`. |
| Python definition relationship | A Python module syntactically defines a top-level function, async function, or class. | The relationship evidence text includes definition kind and line range; ordinary observation evidence preserves subject module, predicate `defines`, object value, source path, metadata, and confidence. | A `FactSupport` group keyed by subject module, predicate `defines`, fully qualified symbol object, and `path`. | `--observe-repository-source`, `--current-facts`, `--fact-support`, `--why-fact`, source-navigation definition lookup, and documentation/repository reconciliation checks. |
| Method artifact fact in fixture-level repository observation | A caller-provided Python class directly defines a method. | This path returns `RepositoryArtifactFact` records, not ordinary runtime observations; the record includes artifact kind `method`, path, symbol, and `parent_symbol`. | It does not currently travel through the general observation/evidence/fact-support pipeline unless caller-specific reconciliation uses the artifact facts. | Fixture-level self-model alignment and structure-claim reconciliation tests. It is repository-observation capability evidence but not the current repository-source observation stream. |
| Module/file artifact fact in fixture-level repository observation | A supplied source path exists as a module/file; parse failure still preserves a module/file fact. | A `RepositoryArtifactFact` record with artifact kind `module`, path, and optional parse-failed text. | Not ordinary `FactSupport` unless explicitly converted by a caller; used as supplied artifact support in reconciliation. | Fixture-level repository artifact reconciliation and tests. |
| Class/function/import artifact facts in fixture-level repository observation | A supplied Python source text contains top-level classes, functions, async functions, and imports. | `RepositoryArtifactFact` records with artifact kind `class`, `function`, or `import`, plus path and symbol. | Not ordinary fact support by default. | Self-model alignment and repository characterization tests. |
| Documentation navigation relationships | Explicit documentation front matter can define document/domain/concept relationships such as `depends_on`, `related_to`, `belongs_to_domain`, and `defines`. | Relationship evidence text and explicit authored metadata become relationship facts when extracted. | When converted to observations by documentation observation, support can be preserved as ordinary evidence-backed facts. | Documentation observation, knowledge navigation, and documentation relationship reconciliation surfaces. This is repository-derived but not source-code structure. |

### Current implementation shape

Current repository source observation is intentionally narrow:

```text
repository root
    -> allowlisted Python files under seed_runtime and tests by default
    -> read source text
    -> extract static import relationships
    -> extract top-level definition relationships
    -> convert each relationship into ordinary Observation records
    -> ObservationIngestor creates evidence and observed facts
    -> State projects fact support
    -> current facts / fact support / source navigation consume support
```

The repository-source observer is therefore a source relationship collector, not a complete repository model. It does not scan every repository artifact by default, does not preserve nested definitions as ordinary source observations, does not resolve symbols across files, does not infer runtime behavior, and does not treat AST output as architectural authority.

### What each current preserved observation means

#### `imports`

- **Observed:** static import syntax in Python source files.
- **Evidence:** the source module imported a module/name; evidence includes source path and relationship text.
- **Fact support:** current support can answer that module `A` imports value `B` with support and path dimensions.
- **Consumed by:** current facts, fact support, why-fact, relationship filters, source-navigation imports, and repository/documentation reconciliation as weak dependency evidence.
- **Boundary:** imports do not prove calls, use, reachability, behavior, ownership, validation, emission, registration, or architectural authority.

#### `defines`

- **Observed:** top-level Python class/function/async-function declarations in the repository-source observation stream; fixture-level extraction also observes direct class methods as artifact facts.
- **Evidence:** definition kind, fully qualified symbol, source path, and line range for relationship facts.
- **Fact support:** current support can answer which module defines a fully qualified symbol and where.
- **Consumed by:** current facts, fact support, source navigation, documentation/repository alignment, and structure/existence claim reconciliation.
- **Boundary:** definitions do not prove invocation, entrypoint reachability, behavior ownership beyond the declaration location, correctness, or capability authority.

#### Repository artifact facts outside the observation stream

`extract_repository_artifact_facts()` preserves module/file, class, function, method, and import artifact facts from caller-provided Python text. This is important because it proves Seed already has some native extraction ability for method containment, but the current repository-source acquisition path does not preserve those richer artifact facts as ordinary observations. The gap is therefore partly preservation/ontology, not merely AST construction.

## Current repository-understanding capabilities

Seed can currently answer narrow questions such as:

- What modules import this module/name, if the query matches preserved import support?
- What module defines this top-level class or function?
- What definitions or imports are preserved for a known module or path?
- What evidence supports an `imports` or `defines` fact?
- Does a documentation existence/structure claim have artifact support in fixture-level reconciliation?

Seed cannot reliably answer richer implementation questions such as:

- Where is this behavior entered from an operator command?
- Who calls this function or method?
- Which implementation units use this symbol after importing it?
- Which class implements a protocol or overrides a superclass method?
- Which module exports this symbol for package-level consumption?
- Which source artifact contains nested functions, methods, classes, constants, decorators, or registrations?
- What is the cross-file dependency path from an operator surface to a behavior?
- Which repository packages, modules, tests, and scripts form an implementation area?

## Candidate missing observations

The candidates below are evaluated by repository-understanding value, not parser availability.

Provider independence values:

- **A native extraction:** Seed can reasonably produce the observation with bounded native code.
- **B external AST/ASG provider:** best produced by a richer provider because scope, language semantics, resolution, or maintenance burden is high.
- **C either:** the desired observation is independent of mechanism; either native or external extraction can supply source material if Seed owns normalization and promotion.

### Candidate evaluation matrix

| Candidate observation | Operator question unlocked | Richer surface | Classification | Understanding value | Duplication risk | Provider independence |
| --- | --- | --- | --- | --- | --- | --- |
| Nested definitions and class methods as ordinary `defines` observations with containing scope | What methods does this class define? Where is this nested helper declared? | Source navigation, current facts, structure claim support | Observation -> evidence -> fact support; may also support `contains` relationship | High. It turns definition ownership from top-level only into actual implementation-unit ownership. | Low to medium. Fixture artifact facts already include methods, but they are not preserved in the main observation stream. | C either. Native Python extraction already partly exists; external provider could generalize. |
| `contains` / `contained_by` scope relationships | What does this class/module contain? What contains this method/function? | Source navigation, relationship views, claim support | Relationship fact and navigation material; eligible for fact support if narrowly syntactic | High. It is the missing bridge between files, modules, classes, methods, and nested definitions. | Medium. Some containment is implicit in fully qualified symbols and `parent_symbol`; explicit edges reduce ambiguity but can duplicate path/symbol conventions. | C either. Native for Python scope trees; external for multi-language and richer scopes. |
| Definition metadata: kind, signature, decorators, base classes, line range | What kind of thing is this symbol? What parameters shape this implementation surface? Is this a CLI option decorator/registration-like definition? | Source navigation detail, fact support detail, documentation reconciliation | Evidence metadata first; selected normalized fields may become facts or relationships | High for navigation and claim support; especially line ranges and containing scope. | Low if treated as evidence metadata rather than many noisy facts. | C either. Native for bounded Python metadata; external for broad language support. |
| Entrypoint / operator-surface declarations | Where is `--state-build` exposed? What source declaration creates this command surface? | Source navigation, operator surface mapping, implementation audit | Relationship/fact if declaration is explicit; otherwise candidate observation requiring guardrails | High. Prior docs identify entrypoints as reachability knowledge distinct from definitions/imports. | Low. Current imports/defines cannot answer reachability. | C either, but Seed-specific adapters may be needed for CLI/framework conventions. |
| Registrations / route/table/decorator bindings | Where is this handler registered? What command/route/capability maps to this implementation? | Source navigation, relationship views, operator action tracing | Relationship observation with conservative evidence; not behavior proof | High when explicit. It connects definitions to surfaces without claiming execution. | Low to medium. Can be confused with calls or reachability if overpromoted. | C either. Native for Seed-specific tables/decorators; external can identify syntax but not Seed semantics alone. |
| Calls / called_by | Who calls this function? What functions does this function call? | Source navigation, relationship graph, implementation audits | Relationship observation with strong guardrails; fact support if syntactic/static call target is clear; source-navigation-only when unresolved | High but risky. It answers behavior adjacency and next-hop navigation, not runtime execution. | Low duplication; current imports are much weaker. | C either. Native for bounded Python call AST; external/ASG better for resolution and cross-language accuracy. |
| Symbol references / referenced_by / usage sites | Where is this symbol used, not just imported or defined? | Source navigation, impact analysis, refactoring support | Mostly source-navigation and evidence material; facts only for clearly resolved static references | High. It answers impact and inspection questions that imports/defines cannot. | Low. Imports are not usage. | B or C. Simple textual/native AST references are possible; robust resolution favors external provider. |
| Cross-file reference resolution | Which definition does this reference actually point to? | Source navigation, relationship graph, support explanations | Relationship/evidence with confidence and resolver provenance | High. It turns local syntax into repository understanding. | Low. Existing facts do not resolve imports to local definitions. | B for robust ASG; C for bounded native Python/package resolution. |
| Import alias and relative import resolution | What local module/symbol does this import refer to? | Source navigation imports, dependency graph | Evidence metadata or normalized relationship object; can support `imports` refinement | Medium-high. Current import objects can be ambiguous (`alias.name` for from-imports). | Medium. It enriches existing imports rather than adds a wholly new observation. | C either. Native bounded resolver is feasible; external provider may reduce maintenance. |
| Exports / package public API | What does this package expose? Is this symbol intentionally public? | Source navigation, package relationship views | Observation/evidence for explicit `__all__`, re-export imports, package init exports; not authority for API stability unless documented | Medium-high for package understanding. | Medium. Re-export imports partially appear as imports but not as export intent. | C either. Native for Python `__all__` and `__init__`; external for broader languages. |
| Inherits / base class relationships | What class extends this class? What base classes shape this implementation? | Relationship views, class navigation, claim support | Relationship observation/fact when syntactic base is explicit | Medium-high. Helpful for structure and polymorphism, but not behavior by itself. | Low. Current `defines` ignores bases. | C either. Native Python class bases are straightforward; external helps resolution. |
| Implements protocol/interface | Which class implements this protocol/interface? | Relationship views, capability/contract audits | Often candidate/inferred relationship unless explicit language construct exists | Medium. Valuable in typed/interface-heavy code; risky in Python unless explicit inheritance or registration. | Low. Existing facts cannot answer this. | B or C. Native for explicit inheritance; robust structural typing likely external or type-checker provider. |
| Overrides | Which subclass method overrides a superclass method? | Relationship views, behavior-adjacent navigation | Relationship observation requiring inheritance + method matching; likely lower-confidence or provider-specific | Medium. Useful for class-heavy areas, but requires resolution. | Low. Not duplicated. | B preferred; C possible for bounded native Python. |
| Module/package relationships | Which package contains this module? Which modules are tests/scripts/runtime? | Repository overview, source navigation, state summary | Observation/fact for file/package/module existence and containment | High for repository orientation. Current source observer skips many artifact existence facts. | Medium. Some module identity is implicit in relationship subjects; explicit package/module facts reduce hidden assumptions. | A or C. Native filesystem/package extraction is enough; external AST not necessary. |
| Test-to-target relationships | Which tests exercise or reference this implementation unit? | Source navigation, impact analysis, verification planning | Relationship/navigation material; fact only when explicit import/reference supports it | Medium-high for development workflow. | Low. Current imports can show test imports but not target relationship intent. | C either. Native heuristics from imports/naming; external references improve quality. |
| Data/read/write/store/emits relationships | Where are facts/events persisted, emitted, read, or projected? | Architecture audits, behavior trace surfaces | Relationship candidates with strict domain-specific adapters; not generic AST facts alone | High for Seed architecture, but not first source-richness step because semantics are domain-specific. | Low. Current imports/defines cannot answer it. | C either, but Seed-specific semantic mapping is required regardless of provider. |
| Dependency/module graph | What modules depend on this module? What dependency clusters exist? | Relationship views, repository overview, source navigation | Derived relationship/read model from `imports` plus resolution; not necessarily new observation if based on existing import facts | Medium. Useful, but much is derivable after import resolution. | High if stored as duplicate facts without adding resolution. | C either; native graph over existing facts may suffice. |
| Complexity/control-flow/data-flow metrics | Which functions are complex or risky? What data flows into this value? | Audit prioritization, quality dashboards | Mostly analysis output/candidate evidence, not foundational observation | Low to medium for repository understanding; high risk of tool-driven scope creep. | Low duplication but high authority risk. | B external preferred if ever desired; not a near-term Seed-native priority. |

## Questions unlocked by high-value candidates

### 1. Containment and richer definitions

Unlocked questions:

- What methods does `Runtime` define?
- What functions/classes are inside this module?
- Where is this nested helper located?
- Which source artifact owns this symbol's declaration?

Surfaces enriched:

- source navigation can show module -> class -> method hierarchy;
- fact support can explain declaration ownership with line ranges;
- documentation structure claims can be supported by ordinary observations rather than fixture-only artifact facts.

Recommended classification:

- `defines` remains a fact-level structural relationship;
- `contains` can be either an explicit relationship fact or source-navigation projection derived from definitions with containing scope;
- line range, definition kind, and signature should initially be evidence metadata unless Seed defines canonical fact predicates for them.

### 2. Entrypoints and registrations

Unlocked questions:

- Where is an operator command, route, capability, or handler exposed?
- How can an operator reach this implementation surface?
- What source declaration connects a user-facing name to an implementation symbol?

Surfaces enriched:

- source navigation;
- operator-surface audits;
- current repository-understanding claims about reachability.

Recommended classification:

- explicit entrypoint declarations are relationship observations;
- framework- or convention-derived registrations should begin as source-navigation evidence/candidate material until promotion rules are defined;
- they must not collapse into capability ownership or runtime execution claims.

### 3. Calls and references

Unlocked questions:

- Who calls this function?
- What downstream implementation should I inspect next?
- If this symbol changes, what source locations are likely affected?
- Which modules use an imported symbol after importing it?

Surfaces enriched:

- source navigation;
- impact analysis;
- repository relationship views;
- implementation audit chains.

Recommended classification:

- static syntactic call sites can be preserved as relationship observations when target identity is local and clear;
- unresolved call names and broad references should be source-navigation-only or evidence/candidate material until resolution confidence is explicit;
- `called_by` should likely be a read-model inversion of `calls`, not a separately observed fact.

### 4. Cross-file resolution and import normalization

Unlocked questions:

- Which local file defines the symbol imported here?
- Is this dependency internal, external, package-local, or standard-library-like?
- What path should I open after seeing an import?

Surfaces enriched:

- source navigation imports become actionable;
- relationship graph becomes less string-based;
- current facts can distinguish raw import syntax from resolved repository dependency edges.

Recommended classification:

- preserve raw import syntax as current `imports` evidence;
- add resolved dependency/reference relationships only with resolver provenance and confidence;
- inverse dependency views should be read-model projections rather than duplicate observations.

### 5. Module/package/artifact existence and containment

Unlocked questions:

- What repository artifacts exist in the observed scope?
- Which package contains this module?
- Which files are tests, scripts, docs, catalogs, source modules, or configuration?

Surfaces enriched:

- repository overview;
- source navigation path/module lookup;
- documentation/repository reconciliation;
- state summary when source artifacts become navigable entities.

Recommended classification:

- direct filesystem/package observations are ordinary observations/facts;
- package/module containment is structural relationship material;
- external AST/ASG is unnecessary for basic file/package existence.

## Observation classification guidance

| Desired material | Best initial classification | Rationale |
| --- | --- | --- |
| Raw import syntax | Existing observation/evidence/fact | Already implemented and safe if not overread. |
| Top-level definitions | Existing observation/evidence/fact | Already implemented; should remain structural. |
| Method/nested definitions | Observation/evidence/fact | Same kind of structural declaration as top-level definitions; current non-preservation is a real gap. |
| Line ranges, signatures, decorators | Evidence metadata first | Useful for navigation, but many metadata fields would create noisy facts if promoted wholesale. |
| Containment hierarchy | Relationship fact or source-navigation projection | High navigation value; exact storage should avoid duplicating fully qualified symbol semantics. |
| Entrypoints/registrations | Relationship observation or candidate material | High value, but framework-specific and must not prove runtime execution. |
| Calls | Relationship observation when resolved; candidate/navigation material otherwise | Useful but behavior-adjacent and easy to overstate. |
| Called-by | Read-model inversion of calls | Do not observe both directions unless independent evidence exists. |
| References/referenced-by | Navigation/evidence first; facts only for resolved references | High volume and ambiguity favor cautious preservation. |
| Inherits | Relationship observation/fact for syntactic bases | Structural and useful; not behavior. |
| Implements/overrides | Candidate or relationship with resolver provenance | Usually needs inheritance/type resolution. |
| Exports/re-exports | Observation/evidence/fact for explicit syntax | Adds package API understanding beyond imports. |
| Module/package/file existence | Observation/evidence/fact | Direct repository structure; not AST-dependent. |
| Dependency graph / depended-by | Derived read model from imports/resolution | Avoid duplicating base observations. |
| Data-flow/control-flow metrics | Analysis/candidate material | Not foundational repository observation; high tool-driven scope risk. |

## Provider independence analysis

The desired observations are mostly provider-independent. Seed should define the normalized observation contract first, then decide extraction mechanism.

### Native extraction is enough for

- file/module/package existence;
- Python top-level and nested definitions;
- Python method containment;
- Python class bases as raw `inherits` edges;
- explicit Python `__all__` exports;
- simple import alias and relative import normalization;
- Seed-specific CLI table or argparse declaration observations, if adapters remain bounded.

### External AST/ASG provider may be appropriate for

- robust cross-file symbol resolution;
- multi-language parsing;
- reference indexing at repository scale;
- call graph extraction with scope resolution;
- override and implementation analysis;
- incremental indexing/caching;
- richer language-specific semantics.

### Either mechanism can produce

- calls/called-by source material;
- references/referenced-by source material;
- containment relationships;
- inheritance relationships;
- exports and re-exports;
- test-target relationships;
- module dependency graphs.

The mechanism should not determine authority. External provider output would still be source material that Seed wraps as observations with provider identity, version, configuration, path, confidence, and promotion boundaries.

## High-value candidates

1. **Preserve method/nested definitions and containing scope as ordinary source observations.**
   - This directly closes the gap between current top-level `defines` and actual implementation structure.
   - It reuses existing structural semantics.
   - It does not require external tooling before proving value.

2. **Add explicit containment/source hierarchy for module -> class -> method/function.**
   - This makes source navigation substantially richer without claiming behavior.
   - It can be a relationship fact or derived source-navigation projection; this classification should be investigated before implementation.

3. **Preserve entrypoint and registration declarations with strict guardrails.**
   - Prior source-navigation authority says reachability knowledge is distinct from imports and definitions.
   - This unlocks operator questions about commands and exposed surfaces.

4. **Resolve imports to repository-local definitions/dependencies where confidence is explicit.**
   - This makes existing import observations actionable rather than string-only.
   - It can be native and bounded at first, then external-provider-backed later if needed.

5. **Preserve calls/references as behavior-adjacent navigation material, not execution proof.**
   - This would materially improve implementation navigation and impact analysis.
   - The first investigation should define confidence, target identity, and promotion rules before collection.

6. **Add module/package/file existence and package containment observations if repository overview remains a goal.**
   - Repository characterization originally called for artifact existence/classification.
   - Current source observation preserves relationships found inside files but not a full observed repository artifact inventory.

## Low-value or defer candidates

- **Control-flow and data-flow metrics:** useful for analysis but not foundational repository understanding; likely tool-driven rather than Seed-need-driven.
- **Full semantic ASG as a fact source:** too broad before Seed defines accepted observation types and promotion rules.
- **`called_by` / `referenced_by` as independently stored observations:** better as read-model inversions of `calls` and `references` unless separately observed.
- **Broad `implements` in Python by structural typing:** high inference risk unless explicit inheritance/registration supports it.
- **Package dependency graph as duplicated facts:** valuable as a view, but much should derive from import observations plus resolution.

## Non-conclusions

This audit does not conclude that Seed should add MCP integration.

This audit does not conclude that Seed should replace native source observation.

This audit does not conclude that external AST/ASG providers are unnecessary.

This audit does not conclude that calls, references, implementations, overrides, or data-flow should be promoted as facts by default.

This audit does not select a schema, command, provider, extraction library, cache strategy, or indexing architecture.

This audit does not expand repository-source observation implementation.

## Recommended next investigation

Before implementation, perform a focused **source-structure observation contract reconciliation** that answers:

1. For method/nested definitions, should Seed preserve them as expanded `defines` facts, `contains` relationships, or both?
2. What exact evidence payload is required for source-structure observations: source path, line range, containing scope, raw syntax kind, resolver identity, provider version, confidence, and parse diagnostics?
3. Which relationship kinds are eligible for immediate fact promotion and which remain source-navigation-only or candidate material?
4. What is the canonical distinction between raw syntax observations and resolved repository relationships?
5. Which operator questions should source navigation answer first: symbol ownership, class/method containment, entrypoint reachability, callers/references, or package dependency paths?
6. What minimum native extraction should remain even if an external provider is later added?
7. What provider-independent test fixtures should validate the observation contract before choosing native extraction or external AST/ASG providers?

Recommended sequence:

```text
repository needs
    -> observation contract
    -> promotion and navigation boundaries
    -> native/external extraction decision
```

not:

```text
AST/ASG capability
    -> dumped structures
    -> retrofit Seed meaning later
```

## Recommendation

Seed should next define and validate a provider-independent source-structure observation contract. The most valuable missing repository observations are not exotic AST outputs; they are preserved implementation structure that operators already ask about: nested definitions, containment, entrypoints/registrations, resolved imports, and cautious calls/references.

Native extraction is sufficient to investigate the first two high-value gaps. External AST/ASG providers should remain optional future providers for cross-file resolution, large reference indexes, call graphs, multi-language support, and override/implementation analysis after Seed decides which observations it actually wants to preserve.
