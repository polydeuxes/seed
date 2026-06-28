# Observation Agreement Architectural Position Audit

## selected architectural question

Where does `Observation Agreement` sit in the recovered observation architecture, and which recovered capability should consume it?

Bounded answer: implementation evidence supports `Observation Agreement` as a downstream evidence supplier between independent observation streams and `Grammar Observation`:

```text
Structure Observation
↓
Relationship Observation
↓
Observation Agreement
↓
Grammar Observation
```

This ordering is not a strict universal layer cake for all Seed responsibilities. It is the best-supported ordering for the recovered observation stack when the question is limited to structure evidence, relationship evidence, agreement between independent observation streams, and grammar visibility as recurring implementation relation shape.

This audit does not implement Observation Agreement, add observers, change CLI behavior, change JSON/schema/event/ledger behavior, recover grammar, recover responsibility, stabilize lexicon, or create diagnostic surfaces.

## implementation evidence

### Structure Observation produces bounded structural evidence

`structure_observation_substrate_responsibility_audit.md` establishes `Structure Observation` as the broader read-only structural-observation responsibility behind substrate-specific implementations. The documented boundary rejects prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, event-ledger writes, and repository mutation.

The same audit records that documentation structure produces document-local structural records, including explicit architectural relation observations with `left_term`, `relation`, `right_term`, `source_path`, `line_number`, and `evidence`. These are structural line matches, not grammar, responsibility, dependency, ownership, or lexicon.

Repository artifact observation is another structure stream. It emits implementation-side repository artifact facts from supplied Python text while rejecting file scanning, repository imports, LLM use, claim reconciliation, runtime integration, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation.

Implementation consequence: Structure Observation and its substrate implementations naturally **produce evidence**. They do not naturally consume multiple observation streams to judge agreement, and they do not own grammar.

### Repository Artifact Observation produces implementation-side structure evidence

`cross_substrate_structural_coincidence_audit.md` identifies `RepositoryArtifactObservationAdapter` beneath Structure Observation and records that it emits `RepositoryArtifactFact` records for modules, top-level classes, top-level functions, async functions, direct class methods, and imports. Its facts include artifact kind, path, symbol, and parent symbol.

The same audit treats answer-composition and operational-responsibility implementation objects as observable implementation structures. Examples include separated answer/reason payloads, selection result/lineage payloads, and execution recording/post-execution extraction methods. Those facts are candidate implementation-side evidence only; they do not prove architectural truth.

Implementation consequence: Repository Artifact Observation is a producer of implementation structure evidence for agreement. It is not the agreement layer and is not a grammar consumer.

### Documentation Structure produces documentation-side structure evidence

Documentation Structure emits explicit structural observations from Markdown mechanics and line-shaped relation forms. The cross-substrate audit records that tests prove forms such as `A != B`, `A owns B`, `A produces B`, `A consumes B`, and `A hands off to B`, while rejecting prose-like, modal, list-item, and fenced-code counterexamples.

Implementation consequence: Documentation Structure naturally supplies an independent observation stream that can agree or fail to agree with implementation-side structures. It should not be collapsed into grammar because its own boundary is narrower: it observes surface relation forms with provenance.

### Relationship Observation produces relationship evidence across observed structures

`relationship_observation_architectural_position_audit.md` establishes Relationship Observation as a substrate-independent companion capability that extracts relationship evidence over structural inputs and already-observed structures. It emits `RelationshipFact` records with `relationship_kind`, `subject`, `object`, `path`, and `evidence` from documentation navigation metadata, Python import syntax, and Python definition syntax.

Relationship Observation explicitly rejects stronger claims. Import relationships are dependency/name-availability evidence only, not behavior, calls, routes, boundaries, or ownership. Definition relationships are declaration evidence only, not invocation, behavior, reachability, capability authority, or runtime ownership. Documentation navigation relationships consume metadata already observed elsewhere rather than parsing documentation prose.

Implementation consequence: Relationship Observation is still a **producer** in this stack. It produces relationship evidence that can participate in agreement; it is not a terminal architecture observer, and it does not own grammar or responsibility recovery.

### Cross-substrate coincidence already identifies a downstream comparative slot

`cross_substrate_structural_coincidence_audit.md` concluded that a bounded downstream capability could consume Documentation Structure, Repository Artifact Observation, and Relationship Observation without replacing them. It would own candidate correspondence records between already-observed documentation relations and already-observed repository structures.

The audit explicitly says the capability would be downstream and comparative, not a parser, grammar interpreter, responsibility recovery mechanism, architecture inference engine, lexicon stabilizer, semantic inference layer, public CLI, JSON schema, event, ledger writer, or cluster mutation path.

Implementation consequence: the recovered architecture already contains a natural slot between evidence-producing observations and higher interpretation: a read-only agreement/correspondence layer over independently produced observations.

### Observation Agreement classifies the comparative slot more generally

`observation_agreement_classification_audit.md` concludes that the durable capability candidate is broader than `Cross-Substrate Structural Coincidence`. Its defining characteristic is independent observation agreement, not substrate pairing.

It defines `Observation Agreement` as read-only preservation of candidate agreement between independent observation streams where each stream already produced bounded evidence for the same structural pattern, without promoting the agreement to truth, grammar, responsibility, lexicon, semantics, or mutation.

Its owned boundary includes stream independence, candidate agreement records, non-promotion, stream extensibility, and provenance preservation. That boundary is exactly the consumer-of-multiple-evidence-streams role in the observation stack.

Implementation consequence: Observation Agreement naturally consumes Structure Observation and Relationship Observation outputs. It supplies stronger, provenance-preserving evidence to later interpretation surfaces, but it is not terminal.

### Grammar Observation consumes recurring implementation relation shape

`implementation_grammar_visibility_audit.md` answers that Seed can observe grammar directly from implementation evidence if grammar is treated as recurring implementation relation shape rather than a new engine, observer, registry, or vocabulary authority.

The grammar audit identifies recurring forms such as `A != B`, `A owns B`, `A produces B`, `A consumes B`, `A hands off to B`, `A preserves B`, `A bounds B`, `A derives B`, `A selects B`, `A explains B`, `A observes B`, and `A does not own B`. It also rejects treating grammar as an owner, a universal layer relationship, a vocabulary authority, or an automatic conclusion from attractive prose distinctions.

Implementation consequence: Grammar Observation needs evidence of recurring relation shape and must avoid unsupported promotion. Independent agreements are a stronger input than raw observations because they preserve convergence and provenance while still refusing truth, responsibility, and lexicon authority.

### Responsibility family evidence rejects a universal layer cake

`implementation_responsibility_family_stack_audit.md` warns that implementation evidence supports a composition graph with compatibility handoffs, not a strict universal layer cake. It also says families can be orthogonal: visibility does not execute, answer composition does not own underlying facts, inquiry lineage does not own answer correctness, and observation-derived capability does not own runtime operation realization.

Implementation consequence: the proposed observation ordering should not be generalized into a universal architecture for every Seed family. It is supported for the observation-to-grammar path only.

## producer capabilities

The recovered capabilities that naturally produce evidence are:

1. **Structure Observation** — produces bounded structural observations through substrate-specific implementations and preserves evidence without grammar, responsibility, lexicon, mutation, or truth promotion.
2. **Documentation Structure** — produces documentation-side structural records and explicit line-shaped architectural relation observations with source provenance.
3. **Repository Artifact Observation** — produces implementation-side artifact facts from supplied source text.
4. **Relationship Observation** — produces relationship facts across documentation navigation metadata, Python imports, and Python definitions while rejecting behavior, ownership, reachability, and authority claims.
5. **Responsibility family slices/audits** — produce implementation evidence for recurring owner/producer/consumer/handoff/boundary shapes, but only after implementation-backed boundaries exist.

These capabilities are evidence producers because their implementation boundaries are read-only, provenance-preserving, and non-promotional.

## consumer capabilities

The recovered capability that naturally consumes multiple evidence streams is **Observation Agreement**.

Observation Agreement is the first layer whose recovered responsibility is not to observe one substrate or one relation family. Its role is to consume independently produced structural and relationship evidence, preserve candidate convergence, retain provenance, and keep the result below architectural truth, grammar, responsibility, lexicon, and mutation.

The recovered capability that should consume Observation Agreement is **Grammar Observation**.

Grammar Observation asks whether recurring implementation relation shapes are observable. It is stronger when it consumes independent agreements because agreement records can demonstrate that multiple bounded observation streams support the same relation shape while preserving where each side came from and what each side does not prove.

## supported layering

The implementation-supported ordering for this bounded observation stack is:

```text
Structure Observation
↓
Relationship Observation
↓
Observation Agreement
↓
Grammar Observation
```

More precisely:

```text
Documentation Structure ┐
Repository Artifact Observation ├─ Structure Observation evidence
other structural adapters ┘

Relationship Observation ─ relationship evidence over structures and metadata

Structure evidence + relationship evidence
↓
Observation Agreement
↓
candidate agreements with provenance and non-promotion boundaries
↓
Grammar Observation
↓
recurring relation-shape visibility, still not grammar engine / truth / responsibility / lexicon
```

This layering is supported because Structure Observation and Relationship Observation are producers, Observation Agreement is the multi-stream evidence consumer, and Grammar Observation is the later visibility capability that benefits from already-correlated evidence.

## unsupported layering

The following orderings are not supported by current implementation evidence:

### Observation Agreement as terminal observer

Unsupported. Observation Agreement preserves candidate convergence. Existing audits explicitly state it may supply evidence useful to later bounded audits and grammar visibility, but it does not prove architectural truth. Treating it as terminal would overstate its authority and stop before the recovered grammar-visibility question.

### Grammar Observation before Observation Agreement

Partially possible as a manual audit method, but weaker as architecture. The grammar audit did inspect raw implementation evidence directly; however, the recovered observation stack now has a candidate agreement layer that can preserve independent convergence before grammar visibility consumes it. Bypassing agreement would lose the explicit independence/provenance/non-promotion record.

### Responsibility Recovery consuming Observation Agreement directly as its primary input

Unsupported as the selected position. Responsibility recovery requires implementation-backed ownership boundaries, compatibility behavior, tests, and family roles. Observation Agreement may supply evidence to a later responsibility audit, but agreement alone does not recover owner boundaries or family completion.

### Family Recovery consuming Observation Agreement directly as its primary input

Unsupported as the selected position. Family recovery depends on repeated implementation slices and completion evidence. Agreement can identify candidate recurring shapes, but family recovery requires stronger implementation-backed owner/composer/validator/executor/presenter/recorder relationships.

### No consumer

Unsupported. If Observation Agreement has no downstream consumer, its architectural value is reduced to a report-local coincidence record. Existing grammar visibility evidence creates a natural downstream consumer that needs recurring relation-shape evidence without semantic promotion.

## counterexamples

### Evidence that Grammar can inspect raw observations directly

The grammar visibility audit did observe grammar directly from completed implementation slices and representative modules. This is evidence that Grammar Observation does not strictly require an implemented Observation Agreement layer to exist in order for a human audit to identify recurring relation shapes.

However, this is not evidence that raw observations are the stronger architectural input. The audit also warns against creating a grammar owner, grammar engine, vocabulary authority, or universal layer relationship. Observation Agreement would preserve independent convergence before grammar visibility consumes it, reducing the risk that grammar is inferred from a single raw stream or attractive prose label.

### Evidence that Observation Agreement is not yet implemented

`observation_agreement_classification_audit.md` gives medium-high confidence because no Observation Agreement implementation, record type, matching algorithm, diagnostic surface, or test suite exists yet. Therefore this report cannot claim the stack is implemented as code. It can only position the bounded candidate capability using implementation evidence from existing producers and audits.

### Evidence that Observation Agreement could duplicate Structure Observation

Structure Observation already produces structural records and evidence. If Observation Agreement parsed substrates, emitted structural facts, or owned documentation/code extraction, it would duplicate Structure Observation. Existing audits avoid that duplication by requiring agreement to consume already-observed records and preserve candidate convergence only.

### Evidence that Observation Agreement could duplicate Relationship Observation

Relationship Observation already emits `RelationshipFact` records and owns relationship-specific extraction invariants. If Observation Agreement emitted import, definition, navigation, dependency, or documentation relationship facts, it would duplicate Relationship Observation. Existing audits avoid that duplication by requiring agreement to compare independent evidence streams, not extract relationship facts.

### Evidence that Observation Agreement adds no architectural value

The strongest pressure against agreement is that the grammar audit can already inspect implementation evidence and that cross-substrate coincidence is not yet implemented. But the cross-substrate and classification audits identify a missing comparative responsibility: preserving where independent observation streams converge without promoting that convergence. That record is not produced by Structure Observation or Relationship Observation today. Therefore agreement adds value as provenance-preserving convergence evidence.

## recommended architectural position

Observation Agreement should be positioned as a **non-terminal evidence supplier** between observation producers and Grammar Observation.

Its architectural responsibility should be:

```text
consume bounded structural and relationship evidence from independent observation streams;
preserve candidate agreement and provenance;
refuse truth, grammar, responsibility, lexicon, semantic alignment, event, ledger, repository, runtime, or cluster mutation;
supply agreement evidence to Grammar Observation and later bounded audits.
```

The best-supported downstream consumer is **Grammar Observation**, not Responsibility Recovery, Family Recovery, or none.

Responsibility Recovery and Family Recovery may later consume grammar-visible or agreement-supported evidence as part of stronger implementation-backed audits, but current evidence does not support making them the direct primary consumers of Observation Agreement.

## future implementation boundary

If implementation is later requested, the boundary should remain narrower than grammar and responsibility recovery:

1. Consume supplied observation records only.
2. Do not parse Markdown, Python, runtime state, diagnostics, tests, or event logs directly.
3. Do not introduce CLI, JSON, schema, diagnostic inventory, shape-audit, event, or ledger behavior unless explicitly scoped in a future implementation task.
4. Preserve source paths, line numbers, symbols, relationship kinds, evidence strings, and stream identity.
5. Emit candidate agreement records only.
6. Make non-promotion explicit: not truth, not grammar, not responsibility, not lexicon, not semantic alignment, not cluster state.
7. Treat Grammar Observation as the natural downstream consumer for recurring relation-shape visibility.

## confidence

**Medium-high.**

Confidence is high that Structure Observation, Repository Artifact Observation, Documentation Structure, and Relationship Observation naturally produce bounded evidence and should not own agreement, grammar, responsibility, or lexicon. Confidence is high that Observation Agreement is the natural multi-stream consumer. Confidence is medium-high, not high, for the final placement before Grammar Observation because Observation Agreement is still a candidate capability without implementation, record type, matching algorithm, CLI, or tests.

## acceptance answer

Observation Agreement belongs after independent evidence producers and before Grammar Observation.

Structure Observation, Documentation Structure, Repository Artifact Observation, and Relationship Observation produce the evidence for it. Observation Agreement consumes those streams, preserves candidate agreement and provenance, and refuses promotion to truth, grammar, responsibility, lexicon, or mutation.

Grammar Observation should consume Observation Agreement because Grammar Observation is about recurring relation-shape visibility. Independent agreement records are a stronger and safer input than raw observations alone: they preserve convergence across streams while keeping the non-promotion boundaries explicit. Raw observations can still be inspected during audits, but bypassing Observation Agreement weakens the recovered architecture by losing a dedicated independence, provenance, and candidate-convergence boundary.
