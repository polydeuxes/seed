# Cross-Substrate Structural Coincidence Audit

## Selected architectural question

Can the repository observe structural coincidences between documentation and implementation without performing grammar, responsibility recovery, lexicon stabilization, LLM interpretation, semantic inference, runtime mutation, or architectural truth claims?

Bounded answer: **yes, as a read-only observation-derived capability candidate, if it owns only candidate correspondence records between already-observed documentation relations and already-observed repository structures.** The evidence supports `Cross-Substrate Structural Coincidence` as an observational capability, not as grammar interpretation, responsibility recovery, architecture inference, or lexicon stabilization.

## Implementation evidence

### Structure Observation already owns substrate-independent read-only structure extraction

`seed_runtime/structure_observation.py` names `Structure Observation` as the substrate-independent owner for read-only structural extraction, evidence preservation, non-interpretation, and adapter boundaries. Its boundary explicitly rejects content interpretation, substrate parsing ownership, grammar ownership, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation.

This is direct evidence that a downstream capability may consume structural observations without becoming the substrate parser or interpreting content.

### Repository Artifact Observation already emits implementation structure facts

`seed_runtime/knowledge/repository_observation.py` implements `RepositoryArtifactObservationAdapter` beneath `Structure Observation`. It parses caller-provided Python text and emits `RepositoryArtifactFact` records for modules, top-level classes, top-level functions, async functions, direct class methods, and imports. Its docstring and adapter boundary reject repository scanning, imports, LLMs, claim reconciliation, runtime integration, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation.

`seed_runtime/knowledge/self_model_alignment.py` defines `RepositoryArtifactFact` with `fact`, `artifact_kind`, `path`, `symbol`, and optional `parent_symbol`. This is enough to observe candidate implementation-side structures such as `_OperationalStoryAnswerPayload`, `_OperationalStoryReasoningPayload`, `_SelectionResultPayload`, `_SelectionLineagePayload`, `_record_completed_tool_call`, and `_extract_post_execution_knowledge` when their source text is supplied.

### Documentation Structure already emits explicit structural relation observations

`seed_runtime/documentation_structure.py` defines `DocumentationArchitecturalRelationRecord` with `left_term`, `relation`, `right_term`, `source_path`, `line_number`, and `evidence`. `observe_markdown_document()` stores `architectural_relation_observations` in each `DocumentationStructureRecord` by calling `_architectural_relation_observations(...)`.

The relation extractor is intentionally narrow. It skips headings, list items, block quotes, tables, and fenced code content, then records only explicit line-shaped relation forms. Tests prove it observes relation forms such as `A != B`, `A owns B`, `A produces B`, `A consumes B`, and `A hands off to B`, while rejecting prose-like, modal, list-item, and fenced-code counterexamples.

This provides a documentation-side structural stream. It does not need to become grammar recovery because the existing implementation records explicit surface forms with evidence.

### Relationship Observation already emits relation facts without behavior claims

`seed_runtime/knowledge/relationship_observation.py` defines `RelationshipFact` and bounded adapters for documentation navigation relationships, Python import relationships, and Python definition relationships. Its module docstring states that import relationships are dependency/name-availability evidence only and do not prove behavior, calls, routes, boundaries, or ownership. Definition relationships are declaration evidence only and do not prove invocation, behavior, reachability, capability authority, or runtime ownership.

This supplies a second relation-oriented observation stream that can be consumed by a coincidence capability without replacing either `Structure Observation` or `Relationship Observation`.

### Answer Composition examples independently expose implementation structures

`seed_runtime/operational_story.py` separates `_OperationalStoryAnswerPayload` from `_OperationalStoryReasoningPayload`, then maps those implementation-local payloads back into the public `OperationalStory` compatibility object. Its boundary payload remains read-only and rejects fact recording, event-ledger writes, and cluster mutation.

`seed_runtime/selection_path_audit.py` separately defines `_SelectionResultPayload` and `_SelectionLineagePayload`, and `_selection_path_from_payloads(...)` maps those payloads into the public `SelectionPathAudit` compatibility object. The public audit boundary remains read-only and rejects recording, event-ledger writes, and cluster mutation.

These are implementation-side structures. They are not the same as documentation observations such as `Answer != Reason` or `Selection Result != Selection Lineage`; however, they are observable as candidate structures that may coincide with documentation-side relation observations.

### Operational Responsibility example exposes a structural split

`seed_runtime/execution.py` records completed execution through `_record_completed_tool_call(...)`, then hands the durable completion event to `_extract_post_execution_knowledge(...)`. The first method records `tool.call.completed`; the second calls `FactExtractionService.observe_tool_result(...)`.

This supports the candidate example `Execution Recording != Post Execution Extraction` as a possible structural coincidence only if documentation separately supplies the relation observation and repository-artifact observation separately supplies the methods.

## Observable inputs

A bounded coincidence capability could consume these already-existing inputs:

1. `DocumentationStructureRecord.architectural_relation_observations`, especially `DocumentationArchitecturalRelationRecord(left_term, relation, right_term, source_path, line_number, evidence)`.
2. `RepositoryArtifactFact` records, especially `artifact_kind`, `path`, `symbol`, `parent_symbol`, and evidence text.
3. `RelationshipFact` records where useful, especially `relationship_kind`, `subject`, `object`, `path`, and `evidence`.
4. Existing source paths and evidence strings as provenance.

It should not read runtime state, mutate the event ledger, write cluster truth, create public JSON/schema changes, or stabilize a repository-wide lexicon.

## Candidate coincidence model

A minimal model could own only:

```text
candidate documentation relation
↓
candidate implementation structures
↓
candidate correspondence
```

A candidate record could be implementation-local and read-only, for example:

```text
Documentation relation:
  left_term="Answer"
  relation="!="
  right_term="Reason"
  evidence="Answer != Reason"

Implementation candidates:
  symbol="_OperationalStoryAnswerPayload"
  artifact_kind="class"
  path="seed_runtime/operational_story.py"

  symbol="_OperationalStoryReasoningPayload"
  artifact_kind="class"
  path="seed_runtime/operational_story.py"

Candidate correspondence:
  relation_shape="pairwise structural distinction"
  support="documentation relation and two implementation artifact facts are both observed"
  authority="candidate observation only"
```

The capability would own **coincidence observation**: preserving the fact that a documentation relation and implementation structures appear to form a structurally similar pair. It would not own the claim that documentation and implementation mean the same thing, that the architecture is correct, that a responsibility has been recovered, or that terms have entered a stable lexicon.

## Supported conclusions

1. **The repository already exposes enough observable information to detect documentation/implementation structural coincidences.** Documentation relation observations provide explicit left/relation/right structures with provenance. Repository artifact facts provide implementation symbols and paths. Relationship facts provide bounded relation evidence. These streams are independently observable.

2. **The candidate capability would own coincidence observation, not grammar interpretation.** Existing boundaries explicitly reject grammar ownership, content interpretation, responsibility recovery, and lexicon stabilization. A coincidence capability can preserve candidate pairs/triples using already-observed records rather than parsing grammar or interpreting prose.

3. **Coincidence observation would consume Structure Observation and Relationship Observation without replacing either.** Structure Observation remains responsible for read-only structural extraction and substrate adapter boundaries. Documentation Structure and Repository Artifact Observation remain substrate adapters. Relationship Observation remains responsible for relationship facts. Cross-Substrate Structural Coincidence would be downstream and comparative.

4. **The capability could improve architectural recovery while preserving repository authority.** It would make visible cases where independent observation streams converge, such as documentation distinguishing `Answer` from `Reason` while implementation exposes separate answer and reasoning payloads. This improves recovery by surfacing candidates for human or later implementation review, while preserving authority through evidence, provenance, and non-truth wording.

5. **The legitimate first-class capability is observational and bounded.** The strongest supported name is `Cross-Substrate Structural Coincidence`, not `Cross-Substrate Semantic Alignment`, `Responsibility Recovery`, `Grammar Recovery`, `Architecture Inference`, or `Lexicon Stabilization`.

## Unsupported conclusions

The evidence does **not** support claiming that:

1. `Answer != Reason` in documentation and `_OperationalStoryAnswerPayload` / `_OperationalStoryReasoningPayload` in implementation are necessarily the same architectural truth.
2. Documentation terms define implementation responsibilities.
3. Implementation symbol names stabilize documentation vocabulary.
4. Coincidence detection proves ownership, behavior, invocation, reachability, family completion, or architectural authority.
5. Relationship observations prove behavior, calls, routes, boundaries, or ownership.
6. Repository artifact facts alone prove responsibility.
7. A public CLI, JSON schema, diagnostic inventory item, event, ledger write, or cluster mutation is justified by this audit.

## Evidence against stronger interpretations

Several implementation boundaries reject stronger interpretations:

- `StructureObservationBoundary` explicitly sets `interprets_content=False`, `owns_grammar=False`, `owns_responsibility_recovery=False`, and `owns_lexicon=False`.
- `RepositoryArtifactObservationAdapterBoundary` rejects responsibility recovery and lexicon ownership, and the extractor states that it does not reconcile claims or use LLMs.
- `Relationship Observation` states that import and definition relationships do not prove behavior, calls, routes, boundaries, ownership, invocation, reachability, capability authority, or runtime ownership.
- Documentation architectural relation tests reject prose-like, modal, list-item, and fenced-code examples, proving the documentation stream is a narrow surface-form observer rather than general prose interpretation.
- Answer Composition implementation maps private payloads back into stable public compatibility objects, so private structural separation is implementation evidence but not public schema authority.

These are counterexamples to treating coincidence detection as grammar, responsibility recovery, lexicon stabilization, semantic inference, or architecture truth.

## Compatibility boundaries

A future implementation must preserve these boundaries:

1. **Read-only only.** No event-ledger writes, repository mutation, runtime mutation, cluster mutation, or fact recording as cluster truth.
2. **No public surface changes unless explicitly scoped later.** This audit does not justify CLI changes, JSON changes, schema changes, diagnostic inventory changes, or shape-audit changes.
3. **No grammar recovery.** Use already-observed relation records and artifact facts; do not introduce a grammar for prose.
4. **No responsibility recovery.** Candidate correspondence must not claim ownership or responsibility.
5. **No lexicon stabilization.** Matching labels or symbol fragments are candidate evidence only, not repository vocabulary authority.
6. **No LLM or semantic inference.** Correspondence should be deterministic and evidence-preserving.
7. **Do not replace existing streams.** Documentation Structure, Repository Artifact Observation, and Relationship Observation remain independent sources.
8. **Preserve provenance.** Every candidate coincidence must retain source paths, line numbers where available, symbols, relation text, and evidence strings.
9. **Preserve uncertainty.** Output language should use `candidate`, `observed coincidence`, `documentation-side`, `implementation-side`, and `not architectural truth` style boundaries.

## Recommended next implementation step

If implementation is approved later, the smallest safe next step is an internal, test-only coincidence observer over supplied records:

```text
observe_cross_substrate_structural_coincidences(
    documentation_relations: Sequence[DocumentationArchitecturalRelationRecord],
    repository_facts: Sequence[RepositoryArtifactFact],
    relationship_facts: Sequence[RelationshipFact] = (),
) -> tuple[CrossSubstrateStructuralCoincidence, ...]
```

Initial matching should be deliberately conservative and deterministic:

- consume only supplied records;
- produce candidate records only;
- retain all evidence/provenance;
- make no CLI/JSON/schema/event/ledger changes;
- include boundary fields rejecting grammar, responsibility recovery, lexicon stabilization, semantic inference, and architectural truth;
- test examples such as `Answer != Reason` versus `_OperationalStoryAnswerPayload` / `_OperationalStoryReasoningPayload`, while also testing counterexamples where only one side is present or where relation terms require semantic inference.

## Confidence

**Medium-high.** The repository has strong evidence for the required raw materials and boundaries: documentation relation observations, repository artifact facts, relationship facts, and explicit non-interpretation contracts. Confidence is not `high` because the exact coincidence matching rule is not yet implemented and must be proven with tests before becoming a first-class implementation capability. The supported conclusion is therefore limited to natural repository support for a bounded read-only capability candidate, not proof that the capability already exists.
