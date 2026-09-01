# Documentation ↔ Code Agreement Investigation

## Scope and method

This is a bounded implementation investigation of whether Seed currently contains a recurring implementation responsibility for Documentation ↔ Code Agreement. It does not implement ownership recovery, runtime surfaces, diagnostics, grammar changes, observation changes, documentation generation, or compatibility changes.

Implementation evidence reviewed:

- `seed_runtime/knowledge/documentation_observation.py` and `tests/test_documentation_observation.py`
- `seed_runtime/documentation_structure.py` and `tests/test_documentation_structure.py`
- `seed_runtime/knowledge/relationship_observation.py` and `tests/test_relationship_observation.py`
- `seed_runtime/knowledge/observation_agreement.py` and `tests/test_observation_agreement.py`
- `seed_runtime/knowledge/grammar_observation.py` and `tests/test_grammar_observation.py`
- `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py`
- Prior investigation and reconciliation reports found by repository search around documentation structure, documentation observation, observation agreement, grammar observation, cross-substrate coincidence, and the architectural hit list.

Commands used for evidence recovery:

```sh
rg -n "Observation Agreement|Grammar Observation|documentation index|documentation recurrence|documentation structure|question-family|diagnostic documentation|responsibility-family|architectural investigation|implementation audit|agreement|documentation" -S . --glob '!**/.git/**'
rg -n "documentation agreement|documentation.*code|code.*documentation|verified against documentation|derived from implementation|unsupported documentation|supported documentation|documentation authority|documentation confidence|documentation provenance|Agreement Result|Documentation Agreement" seed_runtime tests docs *.md -S
sed -n '1,240p' seed_runtime/knowledge/documentation_observation.py
sed -n '1,260p' seed_runtime/documentation_structure.py
sed -n '1,220p' seed_runtime/knowledge/observation_agreement.py
sed -n '1,220p' seed_runtime/knowledge/grammar_observation.py
sed -n '1,220p' seed_runtime/knowledge/relationship_observation.py
sed -n '1,260p' tests/test_documentation_observation.py
sed -n '1,760p' tests/test_documentation_structure.py
sed -n '1,220p' tests/test_observation_agreement.py
sed -n '1,220p' tests/test_grammar_observation.py
```

## Executive answer

The repository does **not** currently contain sufficient recurring implementation evidence for a standalone Documentation ↔ Code Agreement responsibility family.

It does contain implementation-backed adjacent responsibilities:

1. Documentation Observation extracts a narrow set of documentation claims and front-matter navigation metadata from caller-provided text.
2. Documentation Structure observes mechanical Markdown/documentation structure, recurrence, drilldown, membership, links, code fences, and raw architectural relation line forms.
3. Relationship Observation converts documentation navigation metadata and Python syntax into `RelationshipFact` records.
4. Observation Agreement consumes already-observed records from documentation, repository artifacts, and relationship facts and emits candidate agreement records.
5. Grammar Observation consumes Observation Agreement records and emits recurring relation-shape observations.

Those are enough to show an implementation pathway resembling:

```text
Documentation/Repository/Relationship observations
↓
Observation Agreement
↓
Candidate agreement record
↓
Grammar Observation or future consumers
```

They are **not** enough to show a recurring, mature owner specifically shaped as:

```text
Implementation
↓
Documentation Agreement
↓
Agreement Result
↓
Consumer
```

The implementation-backed equivalent currently belongs to Observation Agreement, not to a Documentation ↔ Code Agreement owner.

## Implementation evidence reviewed

### Documentation Observation

`seed_runtime/knowledge/documentation_observation.py` is a deterministic helper module. Its module boundary says it works only on caller-provided text, does not read files, does not inspect the repository, does not use LLMs, and parses only simple Markdown headings/lines plus YAML front matter. Its claim extraction recognizes ownership, rejected concept, frontier, existence, and one explicit structure-claim family. It returns `DocumentationClaim` records with claim text, family, source path, and source heading.

Important evidence:

- `extract_documentation_claims(source_path, text)` tracks headings, skips fenced code blocks, normalizes simple lines, and recognizes only narrow claim families.
- `observe_documentation_metadata(source_path, text)` observes only supported YAML front-matter keys: `doc_type`, `status`, `domain`, `defines`, `depends_on`, and `related`.
- `extract_documentation_navigation_relationship_facts(source_path, text)` delegates observed front matter into relationship facts.
- Tests prove code fences are ignored, narrative non-claim prose is ignored, body front matter-like content is ignored for navigation metadata, and front-matter relationships are deterministic.

This is documentation-derived observation, not documentation-code agreement. It does not compare documentation to implementation, does not verify code against documentation, and does not produce agreement/disagreement results.

### Documentation Structure and recurrence tooling

`seed_runtime/documentation_structure.py` is the strongest implementation around documentation indexing, structure, recurrence, drilldown, and membership. It reads top-level `docs/*.md`, produces `DocumentationStructureRecord` values, and exposes structure-oriented reports. Its declared boundary is explicitly read-only and negative: no prose interpretation, no grammar interpretation, no responsibility recovery, no lexicon stabilization, no claim extraction, no authority inference, no shape inference, no event ledger writes, and no repository mutation.

Implemented structures include:

- document metrics: lines, bytes, blank/nonblank lines, trailing newline, empty document;
- front-matter presence and key names, not front-matter values;
- heading outlines and sections;
- links and broken local doc-link counts;
- fenced code-block structure without contents;
- raw architectural relation observations;
- recurrence reports for section labels, front-matter keys, heading depths, code-fence languages, skeleton signatures, common/missing sections, and outliers;
- exact section-label drilldown and membership reports.

Tests assert these outputs exclude hidden prose, claim text, link text semantics, code-block contents, purpose inference, authority inference, shape inference, and repository mutation.

This is substantial documentation structural analysis and recurrence detection. It is not documentation-code agreement. It does not observe implementation artifacts, compare documents to implementation, decide support/unsupported status for documentation claims, or emit agreement/disagreement records scoped specifically to documentation vs code.

### Relationship Observation

`seed_runtime/knowledge/relationship_observation.py` implements a substrate-neutral `RelationshipFact` record and multiple bounded adapters:

- documentation navigation metadata becomes `depends_on`, `related_to`, `belongs_to_domain`, and `defines` relationship facts;
- static Python imports become `imports` relationship facts;
- top-level Python declarations become `defines` relationship facts.

The documentation navigation helper explicitly states that it does not read files, inspect prose, infer concepts, or reconcile the documentation graph with repository relationships. Python import and definition extraction are syntactic evidence only; they do not prove behavior, calls, routes, boundaries, ownership, reachability, or capability authority.

This provides a shared record shape (`RelationshipFact`) that could feed future agreement. But the current implementation does not compare documentation relationship facts with Python relationship facts as a documentation-code agreement owner.

### Observation Agreement

`seed_runtime/knowledge/observation_agreement.py` is the strongest implemented agreement evidence. It consumes supplied `DocumentationArchitecturalRelationRecord`, `RepositoryArtifactFact`, and `RelationshipFact` sequences and emits `ObservationAgreementRecord` values.

Its implemented responsibility includes:

- consuming supplied observation records;
- preserving candidate agreement;
- preserving provenance;
- preserving observation independence;
- emitting candidate agreement records;
- rejecting promotion to architectural truth, grammar ownership, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, runtime mutation, event writes, ledger writes, repository mutation, and cluster mutation.

The implemented rule is intentionally small: two or more independent observation streams agree only when their supplied evidence text is exactly the same after trimming whitespace. Tests prove exact evidence matching across documentation architectural relations, repository artifact facts, and relationship facts; tests also prove no agreement is emitted for semantically similar but non-identical evidence.

This is an implementation-backed agreement owner, but it is broader and narrower than Documentation ↔ Code Agreement at the same time:

- broader because it can compare any supported independent observation streams, not only documentation and code;
- narrower because it only preserves exact-evidence candidate agreement and does not verify documentation claims against code behavior or authority.

### Grammar Observation

`seed_runtime/knowledge/grammar_observation.py` consumes only `ObservationAgreementRecord` values. It emits `GrammarObservationRecord` values for recurring relation shapes such as `term != term` when at least two supplied agreement records share the same syntactic shape.

Its boundary explicitly rejects grammar promotion, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, capability promotion, mutation, event writes, ledger writes, repository mutation, and cluster mutation.

This means recurrence exists after Observation Agreement, but recurrence is shape recurrence over agreement records. It is not documentation-code agreement recurrence.

### Diagnostic inventory and shape audit

`seed_runtime/diagnostic_inventory.py` registers `documentation_structure` as an operator diagnostic. The registry description identifies mechanical documentation metrics and structural observation without parsing code contents, interpreting prose, extracting claims, inferring authority, inferring shapes, promoting ontology, writing events, or mutating the repository. The shape audit contains the corresponding documentation-structure diagnostic shape expectations.

This proves documentation structure is visible as a diagnostic surface. It does not prove a Documentation ↔ Code Agreement diagnostic or runtime surface exists.

## Recurring implementation patterns

### Pattern 1: Bounded observation before interpretation

Documentation Observation, Documentation Structure, Relationship Observation, Observation Agreement, and Grammar Observation all preserve narrow inputs and reject stronger claims. The recurring design pattern is:

```text
bounded extraction
↓
evidence/provenance preservation
↓
explicit non-promotion boundary
↓
optional downstream interpretation by another bounded owner
```

This pattern supports future agreement work, but it does not itself establish Documentation ↔ Code Agreement ownership.

### Pattern 2: Documentation can produce observation records

Documentation contributes several record families:

- `DocumentationClaim` from narrow claim extraction;
- `DocumentationMetadataObservation` from front matter;
- `RelationshipFact` from front-matter navigation metadata;
- `DocumentationStructureRecord` and related structural records;
- `DocumentationArchitecturalRelationRecord` from raw relation-line forms.

These are documentation observations. They are not verified documentation conclusions.

### Pattern 3: Code/repository evidence exists, but agreement is generic

Code/repository-side evidence appears through `RepositoryArtifactFact` and Python relationship facts. Observation Agreement can compare these with documentation-side evidence if callers supply identical evidence text from independent streams. But there is no dedicated implementation path that says: extract documentation claim, extract implementation fact, compare them, assign support/disagreement/confidence/authority, then route the result to a consumer.

### Pattern 4: Recurrence detection is structural, not semantic

Documentation Structure recurrence detects repeated section labels, front-matter keys, heading depths, code-fence languages, skeletons, common missing sections, and outliers. Grammar Observation detects repeated syntactic relation shapes over agreement records. Neither implementation detects recurring documentation-code agreement semantics.

### Pattern 5: Reports often describe agreement pressure, but reports are not owners

Several reports mention documentation/code agreement, cross-substrate coincidence, documentation authority, documentation observation, repository observation, and hit-list candidates. These are investigation artifacts and architectural pressure records. They do not add runtime owners, records, APIs, or tests proving Documentation ↔ Code Agreement as an implemented responsibility.

## Counterexamples and negative evidence

### Counterexample 1: Documentation agreement exists only as reports or candidate pressure

The architectural hit list contains documentation ↔ code agreement language and possible future work. Prior audits discuss cross-substrate structural coincidence and observation agreement. Those documents are useful evidence of architectural pressure, but they are not implementation owners. No dedicated `documentation_code_agreement.py`, agreement result record, consumer API, diagnostic, or test suite currently exists.

### Counterexample 2: Existing agreement belongs to Observation Agreement

The implemented agreement owner is `Observation Agreement`. It consumes documentation architectural relations, repository artifact facts, and relationship facts, then emits candidate agreement. Its name, boundary, tests, and input/output records are not documentation-code-specific. Therefore, the current agreement evidence is already sufficiently explained by Observation Agreement.

### Counterexample 3: Documentation Structure explicitly refuses agreement semantics

Documentation Structure has extensive indexing and recurrence machinery, but its boundary rejects prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, ledger writes, and mutation. Its tests actively prove hidden claims and semantic text do not appear in outputs. That is evidence against treating Documentation Structure as a documentation-code agreement owner.

### Counterexample 4: Documentation Observation extracts claims but does not verify them

Documentation Observation can extract a small set of documentation claims, but it does not inspect implementation, compare claim text to code, evaluate support, emit disagreement, compute confidence, or consume authority rules. That is claim extraction, not agreement.

### Counterexample 5: Relationship Observation normalizes relationship records but refuses reconciliation

Relationship Observation can produce relationship facts from both documentation metadata and Python syntax. However, documentation metadata extraction explicitly does not reconcile the documentation graph with repository relationships, and Python relationship extraction refuses behavioral or ownership conclusions. The common record shape is a prerequisite, not an agreement responsibility.

### Counterexample 6: No implemented agreement result consumed by another owner

Observation Agreement records are consumed by Grammar Observation, but no implementation consumes a documentation-code agreement result as a support/disagreement/confidence/authority decision. There is no recurring result type with fields such as documentation claim, code evidence, agreement status, disagreement status, authority, confidence, provenance, and consumer decision.

## Supported conclusions

### 1. Does the repository currently contain a recurring Documentation ↔ Code Agreement responsibility?

No, not as a standalone responsibility family. The repository contains adjacent implemented responsibilities and one generic agreement owner, but not a recurring Documentation ↔ Code Agreement owner.

Supported implementation evidence:

- Documentation Observation extracts bounded documentation claims and metadata from caller-provided text only.
- Documentation Structure observes Markdown structure and recurrence, not claim truth or implementation agreement.
- Relationship Observation emits relationship facts from documentation metadata and Python syntax but explicitly avoids reconciliation and stronger claims.
- Observation Agreement emits generic candidate agreement records over supplied independent observation streams using exact evidence equality.
- Grammar Observation consumes Observation Agreement records and observes recurring relation shapes, not documentation-code semantics.

### 2. If yes, where is the strongest implementation evidence?

Because the answer is no for a standalone family, the strongest adjacent evidence is `seed_runtime/knowledge/observation_agreement.py` plus `tests/test_observation_agreement.py`.

That pair proves an implemented, provenance-preserving, non-promoting candidate-agreement owner. It can compare documentation-side and repository/code-side supplied records, but only under the generic Observation Agreement boundary.

The strongest documentation tooling evidence is `seed_runtime/documentation_structure.py` plus `tests/test_documentation_structure.py`, which proves documentation indexing, structure, recurrence, drilldown, and membership. That is not agreement ownership.

### 3. Which implementation responsibilities appear compressed?

The following responsibilities appear compressed or adjacent enough to be confused with Documentation ↔ Code Agreement:

1. **Observation Agreement vs Documentation ↔ Code Agreement.** Observation Agreement can compare documentation and repository streams, but its implementation is generic candidate agreement over exact evidence text.
2. **Documentation Structure vs Documentation Agreement.** Documentation Structure owns rich structural analysis and recurrence, but it explicitly rejects prose interpretation, claim extraction, authority inference, and shape promotion.
3. **Documentation Observation vs Documentation Verification.** Documentation Observation extracts claims and metadata, but it does not validate those claims against implementation.
4. **Relationship Observation vs Reconciliation.** Relationship Observation creates a common relationship fact shape from documentation metadata and Python syntax, but it does not compare or reconcile the two.
5. **Reports vs runtime owners.** Architectural reports preserve pressure and prior conclusions, but they are not implementation responsibilities unless code, records, and tests support them.

### 4. Which implementation responsibilities are already sufficiently explicit?

These responsibilities are sufficiently explicit in implementation:

1. **Documentation Structure**: mechanical Markdown/documentation structure, recurrence, drilldown, membership, and diagnostic visibility.
2. **Documentation Observation**: narrow documentation claim extraction and front-matter metadata observation from caller-provided text.
3. **Relationship Observation**: shared `RelationshipFact` record plus bounded documentation-navigation and Python syntax adapters.
4. **Observation Agreement**: candidate agreement across supplied independent observation streams with provenance and non-promotion.
5. **Grammar Observation**: recurring relation-shape observation over Observation Agreement records.
6. **Diagnostic inventory/shape audit for documentation structure**: documentation-structure surface registration and shape checks.

### 5. Does implementation evidence support beginning a Documentation ↔ Code Agreement responsibility family?

Not yet.

Implementation evidence supports keeping Documentation ↔ Code Agreement on the architectural hit list as a candidate pressure, but not beginning bounded responsibility-family recovery now. The missing implementation evidence is too central:

- no dedicated agreement result record for documentation-code comparison;
- no implemented comparator from `DocumentationClaim` to repository/code facts;
- no recurring consumer that relies on documentation-code agreement results;
- no support/disagreement/confidence/authority fields or rules specific to documentation-code alignment;
- no tests proving supported documentation conclusions, unsupported documentation conclusions, documentation disagreement, documentation provenance, or documentation authority against code;
- no diagnostic or internal API proving this surface exists independently from Observation Agreement.

## Unsupported conclusions

The following conclusions are not supported by current implementation evidence:

- Documentation ↔ Code Agreement is an implemented responsibility family.
- Documentation Structure owns documentation-code agreement.
- Documentation Observation validates documentation against implementation.
- Relationship Observation reconciles documentation metadata with source-code relationships.
- Observation Agreement should be renamed or treated as Documentation ↔ Code Agreement.
- Documentation recurrence implies documentation-code agreement recurrence.
- Architectural reports alone prove a runtime or internal implementation owner.
- Current implementation can classify documentation conclusions as supported or unsupported against code.
- Current implementation computes documentation agreement confidence or documentation authority against implementation.

## Confidence

**Confidence: medium-high.**

Reasons for confidence:

- The relevant implementation modules have explicit boundaries and tests that reject promotion beyond observation, structure, relationship extraction, candidate agreement, and grammar-shape recurrence.
- Repository search found documentation-code agreement as architectural pressure and report language, not as a dedicated implemented owner.
- The strongest implemented agreement owner is clearly named and tested as Observation Agreement, not Documentation ↔ Code Agreement.

Reasons confidence is not absolute:

- The repository contains many documentation-only reconciliations and investigation reports, and some may mention documentation-code alignment in ways not exhaustively semantically reviewed.
- A future integration path may already be partially latent through shared records (`DocumentationClaim`, `RepositoryArtifactFact`, `RelationshipFact`, and `ObservationAgreementRecord`), but latent composability is not current responsibility ownership.

## Recommended next action

Do **not** begin Documentation ↔ Code Agreement responsibility-family recovery yet.

Recommended bounded next action:

1. Preserve this candidate as **insufficient implementation evidence** in the architectural hit-list context.
2. If future work is requested, first perform a narrower implementation audit of actual consumers that ask whether documentation claims are supported by implementation.
3. Only begin a responsibility family if implementation evidence appears for all of the following:
   - a recurring comparator between documentation claims/relations and implementation facts;
   - an agreement/disagreement result record with provenance;
   - a consumer that uses that result;
   - tests preserving supported and unsupported documentation conclusions;
   - explicit boundary rules distinguishing documentation authority from implementation authority;
   - non-promotion and mutation boundaries compatible with Observation Agreement and Grammar Observation.

Until then, repository authority supports this answer:

```text
Documentation ↔ Code Agreement is a plausible architectural candidate,
but current implementation evidence is insufficient for bounded responsibility-family recovery.
Existing agreement evidence belongs to Observation Agreement.
Existing documentation analysis evidence belongs to Documentation Observation and Documentation Structure.
```
