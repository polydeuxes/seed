# Repository Observation External Tooling Audit

## Status

Audit only. This document does not implement changes, add MCP integration, remove Seed source observation, expand source observation, change predicates, change promotion rules, or change projected State behavior.

## Audit question

Should Seed rely on external tools for repository observation richness?

Comparison target:

```text
Seed native repository-source observation
```

versus external AST/ASG tooling such as:

```text
ast-mcp-server
```

as a possible observation source provider.

## Operator pressure

The operator pressure being audited is:

```text
Seed's repository observation is immature and incomplete.
External AST/ASG tools may provide richer source structure.
Maybe Seed should consume those richer observations instead of rebuilding AST/ASG capability internally.
```

This pressure is evidence that the current observation surface may be insufficient. It is not authority and is not a conclusion.

## Evidence inspected

Repository evidence inspected:

- `seed_runtime/observation_sources.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/source_navigation.py`
- `scripts/seed_local.py`
- `docs/repository_observation_frontier.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/repository_observation_implementation_inventory_audit.md`
- relevant tests discovered by repository search, especially repository observation, relationship observation, source navigation, and CLI tests

External material inspected:

- Public GitHub/search-result README claims for `angrysky56/ast-mcp-server`.
- Public package/index summaries for the same tool where they repeat the claimed feature set.

Those public claims describe `ast-mcp-server` as an MCP server that provides code-structure and semantic-analysis capabilities through ASTs and ASGs; claims include parsing code into ASTs, generating ASGs, code structure and complexity analysis, multi-language support, incremental parsing, scope handling, AST diffing, and caching. These claims are comparison material only. This audit did not validate implementation correctness, output schema stability, completeness, security, or fitness for Seed authority.

## Current Seed source-observation shape

Seed currently has a narrow repository source observer, not a general repository understanding engine.

`RepositorySourceObservationSource` is a read-only repository source adapter for imports and defines observations. It scans allowlisted Python files below configured include roots, reads each file, extracts import and definition relationship facts, and converts those relationships into ordinary `Observation` records with source path, evidence text, relationship family, repository root, and path dimension metadata.

The extraction layer is intentionally bounded:

- it uses Python `ast.parse` over caller-supplied text;
- it extracts static top-level Python imports;
- it extracts top-level Python function, async function, and class declarations;
- syntax errors produce no relationships rather than authority claims;
- it does not read files itself;
- it does not scan repositories itself;
- it does not import repository modules;
- it does not build a source graph;
- it does not reconcile claims;
- it does not infer behavior, reachability, routes, capability ownership, or runtime authority.

The CLI exposes this as `--observe-repository-source PATH`, described as read-only repository source intake for allowlisted Python files that emits only imports and defines observations. Source navigation is a separate read-only view over preserved imports/defines facts; it explicitly does not inspect repository files, parse source, or append events.

## Layer distinction

| Layer | Current Seed shape | Seed responsibility? | Safe delegation? | Notes |
| --- | --- | --- | --- | --- |
| Source parsing | Minimal Python `ast.parse` for imports/defines | Partly, for native baseline | Yes, for richer language parsing | Parsing can be delegated when output remains source material. |
| AST / ASG construction | Not a general internal capability | No, except minimal baseline needs | Yes | External tools are strongest here. |
| Source graph extraction | Very limited imports/defines relationships | Seed owns normalized graph meaning | Partly | Tools may propose edges; Seed must define accepted edge semantics. |
| Observation generation | Seed-owned `Observation` records | Yes | No, except as raw provider payload | External output should be wrapped into Seed observations, not replace them. |
| Normalization | Seed-owned predicate/entity/path normalization | Yes | No | Normalization is part of Seed's authority boundary. |
| Evidence preservation | Seed-owned metadata, dimensions, support, evidence graph | Yes | No | Provider payload should be preserved as evidence/provenance, not treated as truth. |
| Fact / relationship promotion | Seed-owned promotion rules | Yes | No | External output cannot self-promote to Seed facts. |
| Projected State | Seed-owned projection | Yes | No | State is the selected Seed view over promoted facts/support. |
| Source-navigation views | Seed-owned read-only projection/view | Yes | Mostly no | External data may enrich inputs, but view semantics remain Seed-owned. |

## Direct answers

### 1. What does Seed's current repository-source observation preserve?

It preserves a narrow set of static Python source relationships:

- module imports symbol/module;
- module defines top-level class;
- module defines top-level function;
- module defines top-level async function;
- source path as a dimension;
- evidence text such as `subject imports name` or `subject defines function name at path:line-range`;
- source metadata identifying repository source collection.

It also preserves the fact that these are observations from a discovery source rather than repository truth by themselves.

### 2. What source-structure richness is missing today?

Missing richness includes at least:

- nested class/function/method definitions;
- class-to-method containment;
- call relationships;
- decorator relationships;
- inheritance/base-class relationships;
- assignment and exported-symbol relationships;
- import alias resolution and relative import resolution beyond preserving the imported name;
- module/package/file existence facts for the full repository;
- non-Python language parsing;
- test-target relationships;
- entrypoint detection;
- config/catalog/schema-specific structure;
- control-flow, data-flow, and semantic-scope relationships;
- cross-file symbol resolution;
- source graph indexes and query surfaces beyond imports/defines source navigation;
- explicit uncertainty and parser-diagnostic preservation for unsupported files.

### 3. Is the missing work primarily parsing/AST/ASG construction, or Seed-specific normalization and authority preservation?

It is both, but the architectural blocker is Seed-specific normalization and authority preservation.

External AST/ASG tooling can plausibly reduce parsing and raw structural extraction work. However, Seed's hard problem is not merely obtaining a richer tree. Seed must decide which provider records become observations, which observations are normalized into canonical predicates, which relationships are promotable, what provenance is retained, how contradictions or parser disagreement are handled, and how the resulting facts project into State and source-navigation views.

Therefore, the missing work is not primarily "get an AST." The missing Seed work is to define the repository observation ontology, evidence contract, normalization rules, promotion rules, and projection boundaries for richer source facts.

### 4. Would an external AST/ASG tool reduce code Seed should maintain?

Potentially yes, but only in the parsing and raw extraction layers.

An external tool could reduce Seed-maintained code for:

- multi-language parsers;
- incremental parsing;
- raw AST creation;
- ASG construction;
- language-specific scope extraction;
- complexity metrics;
- AST diffing;
- parser caching.

It would not remove Seed-maintained code for:

- source-provider trust boundaries;
- observation wrapping;
- predicate normalization;
- evidence and provenance preservation;
- relationship promotion;
- projected State;
- source-navigation semantics;
- contradiction handling;
- provider-version compatibility;
- native minimal baseline observation.

### 5. What risks appear if Seed relies on an external tool?

Risks include:

- authority leakage, where external AST/ASG output is accidentally treated as fact;
- MCP availability becoming a prerequisite for basic repository observation;
- provider schema instability;
- opaque or changing language semantics;
- dependency, packaging, parser-build, and runtime-environment complexity;
- cross-version drift between provider output and Seed normalization;
- large observation volume and projection performance pressure;
- over-rich output causing premature fact promotion;
- false confidence from labels such as "semantic graph";
- unsupported-language or parse-error blind spots being hidden;
- security and trust concerns from invoking a separate tool over repository contents;
- loss of a minimal explainable baseline if native observation is replaced.

### 6. What risks appear if Seed builds all AST/ASG richness natively?

Risks include:

- high maintenance cost across languages;
- reimplementing existing parser and static-analysis ecosystems;
- slow expansion of repository observation richness;
- large test burden for language semantics;
- distraction from Seed's core responsibility: evidence-backed knowledge, normalization, projection, and authority boundaries;
- inconsistent quality if native parsers are shallow but presented as comprehensive;
- pressure to promote weak syntactic edges into stronger semantic claims;
- performance and caching work becoming a separate platform project inside Seed.

### 7. Can external AST/ASG output be treated as an observation source without becoming authority?

Yes, if Seed treats it as provider source material only.

A safe model is:

```text
external AST/ASG provider output
    -> raw provider payload preserved with provider identity/version/config
    -> Seed observation records
    -> Seed normalization
    -> Seed promotion rules
    -> Seed facts/relationships only where allowed
    -> projected State and source-navigation views
```

The provider may say "this looks like a call edge" or "this symbol belongs to this scope." Seed must still decide whether that is an observation, whether it maps to a canonical predicate, what evidence supports it, and whether it is eligible for projection.

### 8. What boundary should exist between external source tools and Seed facts?

The boundary should be:

```text
External tools produce source observations or raw source-structure material.
Seed produces normalized facts, relationship facts, support, and projected State.
```

External provider output should carry:

- provider name;
- provider version;
- provider configuration;
- source repository identity/path;
- file path;
- language;
- parser diagnostics;
- source span/line range where available;
- raw provider node/edge kind;
- raw provider confidence/uncertainty if available;
- normalized candidate predicate, if Seed maps it;
- explicit non-authoritative status before promotion.

Seed facts should exist only after Seed-owned normalization and promotion. External output should never bypass Seed's event ledger, evidence graph, predicate catalog, or projector.

### 9. What predicates/relationships would be candidates for richer source observation?

Candidate richer predicates/relationships include:

| Candidate relationship | Meaning | Promotion caution |
| --- | --- | --- |
| `contains_path` | repository/path containment | Low semantic risk, high volume. |
| `path_has_kind` | file kind such as source, test, doc, config | Needs deterministic classification rules. |
| `defines` | module/file defines symbol | Existing predicate; should be refined by symbol kind/span. |
| `defines_method` | class defines method | Requires containment and class identity. |
| `contains_symbol` | scope contains nested symbol | Must not imply ownership beyond declaration location. |
| `imports` | module/file imports dependency/name | Existing predicate; alias and relative imports need careful metadata. |
| `exports` | module exposes symbol | Language-specific; avoid inferring public API too broadly. |
| `inherits_from` | class derives from base | Static syntax evidence only, not behavior. |
| `decorated_by` | function/class has decorator | Syntax evidence only. |
| `calls` | function/method body contains call expression | Does not prove runtime execution. |
| `references_symbol` | code references name/symbol | Requires scope-resolution caveats. |
| `registers_handler` | code registers handler/route/capability | Should require domain-specific extraction and conservative promotion. |
| `entrypoint_declares` | script/config declares entrypoint | Needs config-specific evidence. |
| `test_targets` | test appears to target module/symbol | Heuristic unless explicit import/name support exists. |
| `config_defines` | config/catalog defines key/object | Schema-aware, not generic AST. |

These are candidates, not schema decisions.

### 10. Should Seed keep a minimal native source observer even if an external provider is added?

Yes.

Seed should keep a minimal native source observer as a trusted baseline because it is:

- local;
- deterministic;
- explainable;
- dependency-light;
- sufficient for basic imports/defines navigation;
- useful when external providers are unavailable;
- a regression oracle for provider output;
- a guard against turning external tooling into authority.

Keeping the baseline does not require Seed to rebuild full AST/ASG capability internally.

## External AST/ASG capability comparison

Public `ast-mcp-server` claims make it a plausible comparison target for the lower source-analysis layers:

- AST parsing;
- ASG generation;
- code structure analysis;
- complexity analysis;
- multiple languages;
- incremental parsing;
- scope handling;
- AST diffing;
- caching;
- MCP-client integration.

Those claimed capabilities address real gaps in Seed's current native source observer. They do not address Seed's authority needs by themselves.

The comparison is therefore asymmetric:

```text
ast-mcp-server strength:
    parse/source-structure richness

Seed required strength:
    evidence-backed observation, normalization, promotion, projection, authority boundaries
```

An AST/ASG provider may provide richer raw edges. It cannot decide what Seed believes.

## What Seed should own

Seed should own:

- repository observation contract;
- provider adapter boundary;
- observation record shape;
- source identity and path normalization;
- predicate vocabulary;
- relationship semantics;
- evidence retention requirements;
- support aggregation;
- promotion rules;
- confidence/uncertainty interpretation;
- contradiction handling;
- projected State;
- source-navigation views;
- operator-facing explanation of what is observed versus inferred;
- minimal native baseline observer.

## What external tools may provide

External tools may safely provide:

- raw AST nodes;
- ASG nodes/edges;
- parser diagnostics;
- source spans;
- language identification;
- symbol/scope candidates;
- call/reference/inheritance/decorator candidates;
- complexity metrics as observations;
- AST diffs as observations;
- caching/incremental parsing as provider implementation details.

They should not provide Seed facts directly.

## Risks

### If replacing Seed native source observation

Replacing Seed native observation with external AST/ASG tooling would create the highest authority risk. Seed would lose a minimal, inspectable baseline and could make basic repository observation dependent on MCP availability, provider health, provider schemas, and provider interpretation.

This conflicts with the explicit boundary that external AST/ASG output is observation source material, not repository truth.

### If keeping only current native observation

Keeping only current native observation avoids dependency and authority leakage, but leaves Seed with immature source richness. It would continue to miss method containment, calls, inheritance, decorators, entrypoints, package/file inventory, multi-language source, and richer navigation evidence.

### If adding external provider beside native baseline

Adding an external provider beside the native baseline introduces adapter complexity, duplicate/conflicting observations, volume control, and schema-version management. However, those are Seed's normal evidence-boundary problems and can be handled if the provider output is explicitly non-authoritative.

## Candidate integration boundary

This audit does not propose implementation, but the safe boundary would look like:

```text
Repository files
    -> Seed native minimal observer
        -> Seed observations for baseline imports/defines

Repository files
    -> optional external AST/ASG provider
        -> raw provider source-structure payload
        -> Seed provider adapter
        -> Seed observations with provider provenance
        -> Seed-owned normalization
        -> Seed-owned fact/relationship promotion
        -> Seed-owned State projection
        -> Seed-owned navigation views
```

Important constraints:

- external output is never written directly as a fact;
- provider node/edge kinds are not canonical predicates;
- Seed records provider identity/version/config;
- Seed preserves file path and source span evidence;
- unsupported files and parse failures are observable diagnostics, not invisible absence;
- source-navigation views should state whether rows come from native baseline, external provider, or both;
- richer predicates should be introduced only after Seed defines their semantics and promotion rules.

## Recommendation or deferred decision

Recommended outcome: **C with D-style gating**.

```text
Keep Seed native source observation as a minimal trusted baseline,
and optionally add external AST/ASG tooling as a richer provider only after
richer-source observation requirements are clearer.
```

Do not choose B. Replacing Seed native observation with external tooling would collapse the authority boundary and remove the minimal baseline.

Do not choose A as a permanent position unless Seed deliberately accepts the cost of native AST/ASG expansion. Extending native observation is useful for the smallest well-defined relationships, but full AST/ASG richness is not obviously Seed's core maintenance burden.

The immediate decision should be deferred for implementation purposes until Seed defines:

- a richer source observation contract;
- accepted predicates and relationships;
- evidence requirements per relationship;
- provider provenance requirements;
- conflict behavior when native and external observations disagree;
- projection and navigation behavior for richer relationships;
- volume and performance limits.

## Non-conclusions

This audit does not conclude that:

- `ast-mcp-server` is correct;
- `ast-mcp-server` is the right provider;
- MCP should be integrated now;
- Seed should remove native repository-source observation;
- Seed should expand source observation immediately;
- external ASG edges are facts;
- call graphs prove runtime behavior;
- imports prove ownership;
- definitions prove capability authority;
- richer source structure should bypass Seed normalization, evidence, promotion, or projection.

## Major findings

1. Seed's current repository-source observation preserves useful but narrow imports/defines evidence.
2. Missing richness includes AST/ASG-scale structure, but the more important Seed work is canonical normalization, evidence preservation, and promotion boundaries.
3. External AST/ASG tooling can reduce parser and raw extraction maintenance, but cannot own Seed facts or projected State.
4. External source tools can be observation providers if their output is kept non-authoritative and wrapped in Seed-owned provenance.
5. Seed should keep the minimal native observer even if a richer external provider is later added.
