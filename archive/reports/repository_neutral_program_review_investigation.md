# Repository-Neutral Program Review Investigation

## Scope

This is a bounded implementation investigation into whether recovered Seed architecture now supports **repository-neutral program review**: reviewing an unfamiliar repository by recovering intended responsibilities, comparing them with observed implementation, evaluating evidence and visibility, and recommending bounded next actions.

This is not self-modification, autonomous debugging, repository import, code generation, implementation planning, a review engine, or inquiry redesign. Repository authority wins. The investigation treats repository evidence as authoritative only when tied to implementation, tests, diagnostics, bounded inquiry surfaces, or completed investigations that themselves cite implementation evidence.

## Implementation evidence reviewed

Primary evidence reviewed:

- `responsibility_recovery_evaluation_readiness_investigation.md`
- `slice_evaluation_readiness_investigation.md`
- `responsibility_authority_frontier_reconciliation.md`
- `docs/architectural_recovery_methodology_characterization.md`
- `docs/answer_responsibility_implementation_characterization.md`
- `docs/answer_composition_family_completion_audit.md`
- `docs/answer_composition_slice_001.md` through answer-composition completion evidence referenced by the audit
- `docs/observation_relationship_implementation_evidence_investigation.md`
- `docs/repository_observation_v0_implementation_characterization.md`
- `docs/repository_observation_external_tooling_audit.md`
- `seed_runtime/repository_observation.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- Related tests named by the reviewed investigations, especially tests for repository observation, observation sources, inquiry orientation, diagnostic inventory, diagnostic shape audit, answer-like surfaces, component audit, and capability/recommendation boundaries.

The review looked for recurring implementation evidence involving intended responsibilities, observed implementation, visibility sufficiency, evidence acquisition, authority boundaries, responsibility boundaries, compatibility expectations, bounded recommendations, and explicit stopping. It also looked for counterexamples where the repository remains Seed-specific or where review would require semantic interpretation, tooling, or repository-specific knowledge not currently implemented.

## Central finding

Recovered implementation supports a **bounded repository-neutral review methodology as an evidence-first human investigation shape**, but it does **not** yet support an implemented repository-neutral review capability.

The strongest implementation-backed shape is:

```text
program or repository under review
↓
explicit review target / concern supplied by operator
↓
intended responsibilities recovered from implementation-backed authority surfaces
↓
observed implementation collected through read-only evidence surfaces
↓
visibility and authority boundaries evaluated
↓
evidence sufficiency / counterexamples / unknowns preserved
↓
bounded recommendation to proceed, stop, or investigate missing evidence
```

That shape is supported because completed investigations repeatedly evaluate candidate responsibilities against observed implementation evidence, authority boundaries, compatibility constraints, negative ownership, counterexamples, and stopping criteria. It is repository-neutral at the methodological level because the repeated evidence grammar is not inherently about Seed: bounded responsibility, authority-preserving handoff, evidence sufficiency, visibility, compatibility, and stopping can apply to any sufficiently observable program.

However, the implementation does not yet provide repository-neutral **review machinery**. Existing code can observe arbitrary repository state read-only and can observe Python definitions/imports from a configured repository root, but many recovered evaluation surfaces and question families remain Seed-specific because they consume Seed's projected state, Seed diagnostics, Seed responsibility families, Seed CLI surfaces, and Seed documentation corpus.

Therefore the answer is conditional:

```text
Repository-neutral program review is implementation-backed as a bounded methodology,
not as an autonomous or fully implemented capability.
```

## Repository-neutral methodology recovered from implementation evidence

### 1. Start from explicit purpose or target, not autonomous inference

Repository-neutral review requires a supplied program purpose, concern, or review target. Seed evidence supports this boundary: inquiry surfaces establish local identity first and then perform narrower work. The responsibility/authority reconciliation found that bounded ask dispatch validates exact question-family strings and forwards operator-provided values; it did not find a general semantic subject-resolution owner.

`QuestionSurfaceInventoryRow` encodes question family, surface, answer responsibility, authority boundary, bounded status, required arguments, and implementation reason. That is evidence for explicit bounded surface identity rather than automatic recovery of arbitrary intent.

Supported review consequence:

- A repository-neutral review may begin with an unfamiliar repository only if the review target or purpose is supplied or recoverable from implementation-backed artifacts.
- Current implementation does not support inferring the program's intended responsibilities from arbitrary prose or repository contents alone.

### 2. Recover intended responsibilities only when authority evidence exists

Recovered architecture supports intended-responsibility reasoning when it can point to existing owners, request/result boundaries, event handoffs, answer payloads, diagnostic rows, or tests. Responsibility Recovery Evaluation Readiness found that proposed recovery is strongest when it identifies fulfilled upstream work, an existing owner, concrete boundary-crossing evidence, excluded authority, compatibility preservation, and stopping criteria.

This generalizes beyond Seed as a review rule:

- Intended responsibility is not a preference or presentation label.
- It must be supported by an authority-bearing artifact: docs with implementation backing, code ownership boundary, interface, test, event, diagnostic declaration, record, schema, or explicitly preserved negative authority.

Limit:

- Existing recovered responsibility families are Seed's families. They are useful examples, but they are not a universal responsibility ontology for another repository.

### 3. Observe implementation through read-only evidence surfaces

Seed has repository-neutral observation primitives, but they are narrow.

`GitRepositoryObservationProvider` observes an arbitrary git-backed path without writes and returns repository path, VCS, head commit, branch, dirty state, untracked/modified/staged counts, remote presence, status availability, and read-only mutation flags. This supports repository-neutral repository-state observation.

`RepositorySourceObservationSource` accepts a repository root and include roots, discovers allowlisted Python source paths, extracts import and definition relationship facts, and emits observations with source path, evidence, relationship family, and repository root metadata. This supports read-only observed-implementation evidence for Python source structure when configured for a repository.

Supported review consequence:

- Seed can collect some repository-neutral implementation evidence from local repositories.
- The evidence currently covers repository state and Python import/definition relationships, not arbitrary language semantics, build systems, runtime behavior, tests, architectural intent, or domain-specific correctness.

### 4. Evaluate visibility sufficiency before judging responsibility match

Visibility sufficiency is a recovered cross-family concept. The methodology characterization and readiness investigations repeatedly reject vocabulary, diagram similarity, output-shape similarity, and boundary prose unless tied to executable code, tests, diagnostics, event behavior, payload shape, or compatibility-preserving handoffs.

Repository-neutral review consequence:

- If a repository lacks observable artifacts for a claimed responsibility, the supported conclusion is insufficient evidence, not mismatch.
- Visibility is part of the review result: the review may recommend adding bounded diagnostic/read-only visibility before recommending implementation changes.

### 5. Preserve authority boundaries and negative ownership

Authority boundary evidence is strong and recurring. Inquiry Orientation's authority boundary states that notes are read-only preserved operator prose, not facts, claims, goals, tool needs, requirements, capabilities, decisions, proposals, plans, authorizations, commands, runtime instructions, ownership, intent, recommended action, or next safe move. Repository Observation explicitly marks read-only observation fields with `writes_event_ledger=False` and `mutates_cluster=False`.

Repository-neutral review consequence:

- A review can compare intended and observed responsibilities without mutating the target repository or promoting diagnostic findings into cluster truth.
- Recommendations must not claim authority over implementation, runtime execution, repository mutation, or operator intent unless implementation evidence grants that authority.

### 6. Keep recommendations bounded

Answer Responsibility Implementation Characterization found strong answer surfaces are built from existing authorities, preserve unknowns/caveats/negative authority, perform answer shaping, and render an explicit boundary. Slice Evaluation and Responsibility Recovery Evaluation readiness both support only proceed / stop / insufficient-evidence recommendations for bounded proposed work.

Repository-neutral review consequence:

- Supported recommendations are bounded: proceed with a specific investigation or implementation-backed change, stop because evidence belongs elsewhere, or gather missing evidence.
- Unsupported recommendations include broad redesign, autonomous debugging, repository-specific fixes, or implementation plans for an unfamiliar program unless the repository's own evidence supports them.

### 7. Stop explicitly

Explicit stopping is a recovered invariant. Completed families stop when remaining pressure changes ownership family, lacks evidence, requires unsupported abstraction, requires compatibility breaks, or would promote vocabulary without implementation backing.

Repository-neutral review consequence:

- Reviewing an unfamiliar repository must be willing to stop with `unsupported`, `insufficient visibility`, or `additional recovered architecture required`.
- A review is not obligated to produce fixes.

## Concepts that are repository-neutral

The following recovered concepts are supported as repository-neutral methodology concepts because their evidence shape does not depend on Seed-specific domain semantics:

1. **Implementation authority first.** Reviews follow code, tests, diagnostics, event behavior, schemas, payloads, and public contracts rather than preferred vocabulary.
2. **Explicit intended responsibility.** Claimed purpose or responsibility needs authority-bearing evidence before it becomes review input.
3. **Observed implementation.** Read-only evidence collection can describe what implementation currently exposes.
4. **Visibility sufficiency.** Absence of observable support is a review finding distinct from implementation failure.
5. **Authority boundary.** The review must distinguish observation, event-ledger writes, repository mutation, cluster mutation, execution authority, and operator intent.
6. **Responsibility boundary.** Work is evaluated by who owns it, what it consumes, what it produces, and what it explicitly does not own.
7. **Compatibility preservation.** Existing public behavior and output shape are review constraints unless evidence supports breaking them.
8. **Evidence sufficiency and counterexamples.** Supported, unsupported, confidence, and counterexample sections are not report style only; they preserve the boundary between evidence and aspiration.
9. **Bounded recommendation.** The strongest supported recommendation type is proceed / stop / insufficient evidence / investigate missing visibility.
10. **Explicit stopping.** A review stops when the next claim would require a different authority, unsupported semantics, unavailable visibility, or implementation not yet recovered.

## Concepts that remain Seed-specific

The following concepts remain Seed-specific or only partially generalized:

1. **Seed responsibility families.** Operational Responsibility, Execution Visibility, Observation-Derived Capability, Projection Influence Lineage, Read-Model Ownership, Answer Composition, and Inquiry Lineage are recovered from Seed implementation and cannot be imposed as another repository's architecture.
2. **Question-family dispatch and inventory rows.** `question_family`, Seed CLI flags, answer responsibility strings, and diagnostic names are Seed's bounded inquiry surfaces, not a general review interface.
3. **Projected state and cluster truth.** Many answer and audit surfaces consume Seed's `State`, event ledger, projected read models, capability inventory, pressure audits, and diagnostic inventory.
4. **Seed documentation corpus.** Existing investigations rely on Seed's completed slice reports, family audits, and repository-local Markdown investigations.
5. **Python-specific repository source observation.** `RepositorySourceObservationSource` observes Python imports/definitions under configured include roots. It is not a language-neutral program understanding layer.
6. **Capability and operation vocabulary.** Tool needs, providers, capability promotion, and operation contracts are Seed runtime concepts and cannot automatically describe an arbitrary repository.
7. **Compatibility expectations for Seed surfaces.** CLI/JSON/event/cache/report compatibility expectations are implementation-backed for Seed surfaces; another repository's compatibility contracts must be recovered separately.
8. **Self-model and self-observation vocabulary.** Self-observation is treated in Seed as an ordinary domain in some investigations, but current executable surfaces are still built around Seed's own state and repository.

## Counterexamples and limits

### Current implementation does not infer program purpose

Repository-neutral review begins from program purpose, but the reviewed implementation does not provide a general program-purpose extractor. Inquiry Orientation explicitly performs deterministic lexical overlap and rejects semantic interpretation or operator-intent inference. Question surfaces require explicit identities or arguments. This is a major missing piece for fully independent unfamiliar-repository review.

### Current implementation does not recover arbitrary intended responsibilities

Responsibility recovery readiness supports evaluating proposed responsibility recovery against evidence. It does not implement autonomous ownership discovery or semantic interpretation of arbitrary proposals. An unfamiliar repository would still need a human or repository-native source to supply candidate responsibilities.

### Repository observation is narrow

Repository-state observation is arbitrary-path and read-only, but it only reports VCS/status metadata. Source observation is read-only but Python/import/definition oriented. It does not evaluate tests, build configuration, non-Python code, runtime behavior, API contracts, documentation claims, or operational behavior.

### Answer/recommendation surfaces are Seed-native

Strong answer surfaces compose Seed diagnostics and read models. They demonstrate a reusable answer-responsibility pattern, but they do not yet accept arbitrary repository evidence as their input universe.

### Recommendations without recovered intended responsibilities remain unsupported

The methodology does not support recommending changes to an unfamiliar repository merely because an implementation looks unusual. A mismatch requires both an intended responsibility and observed implementation evidence.

### Compatibility breaks remain unsupported

Completed recoveries preserve compatibility. The repository has not demonstrated how to evaluate or recommend a necessary compatibility break in Seed, much less in an unfamiliar repository.

## Answers to central questions

### 1. Does recovered implementation now support reviewing an unfamiliar repository using the same architectural methodology used for Seed?

**Partially yes, as a bounded evidence-first methodology; no, as an implemented general review capability.**

Supported:

- The methodology of explicit responsibility, observed implementation, visibility sufficiency, authority boundary, compatibility, evidence sufficiency, counterexamples, bounded recommendations, and stopping is recovered across multiple Seed families.
- Repository observation code can observe arbitrary local git repositories read-only and can collect Python definition/import observations from a configured repository root.

Unsupported:

- There is no implemented general program-purpose extractor.
- There is no implemented arbitrary-repository responsibility recovery engine.
- Existing answer and diagnostic surfaces largely consume Seed-specific state, diagnostics, and slice/family evidence.

### 2. Which recovered concepts are repository-neutral?

Repository-neutral concepts are: implementation authority first, intended responsibility as evidence-backed authority, observed implementation, visibility sufficiency, evidence acquisition, authority boundaries, responsibility boundaries, compatibility expectations, bounded recommendations, counterexample review, confidence, and explicit stopping.

They are neutral because they constrain how evidence is evaluated rather than prescribing Seed's specific architecture.

### 3. Which recovered concepts remain Seed-specific?

Seed-specific concepts include Seed's completed responsibility families, question-family inventory, projected state, diagnostic inventory names, event-ledger and cluster-truth semantics as currently implemented, capability/tool-provider vocabulary, Seed CLI/JSON compatibility surfaces, and Seed's documentation/investigation corpus.

Some of these may inspire repository-neutral review surfaces, but current implementation evidence does not support treating them as universal.

### 4. Would reviewing Seed itself simply become another instance of repository review?

**Methodologically, yes, if repository-neutral review is bounded to evidence-first review of observable program responsibilities.**

Seed already reviews itself through repository evidence, responsibility boundaries, authority boundaries, visibility checks, and bounded recommendations. Under a repository-neutral methodology, Seed would be a particularly observable target repository with unusually rich recovered architecture.

**Implementation-wise, not yet.** Existing self-review-like surfaces are coupled to Seed's projected state, diagnostics, event model, and investigations. Seed would become just another repository review target only after the review input model can accept repository-neutral evidence and recover target-specific responsibilities without relying on Seed-only surfaces.

### 5. Does implementation evidence support treating self-review as a consequence of repository-neutral review rather than as a special architectural capability?

**Yes as an architectural consequence; not yet as an implemented capability replacement.**

The evidence supports self-review as an instance of ordinary evidence-first review because the recovered methodology does not require self-modification or privileged self-knowledge. It requires observable responsibilities, authority, visibility, evidence, mismatches, bounded recommendations, and stopping.

But current implementation still uses Seed-specific surfaces to review Seed. Therefore implementation evidence supports the direction of treating self-review as a consequence, while also showing missing architecture before that consequence can replace Seed-specific review surfaces.

## Supported conclusions

1. Seed has recovered enough architecture to describe repository-neutral program review as a bounded evidence-first methodology.
2. The methodology is not tool-first. It begins with purpose/responsibility and then asks what implementation evidence, visibility, authority, and compatibility support or contradict it.
3. Seed can already observe some arbitrary repository facts read-only, especially git status metadata and Python import/definition relationships.
4. Strong review conclusions require intended responsibilities and observed implementation evidence; either one alone is insufficient.
5. Reviewing Seed can be understood as an instance of this methodology because Seed is an observable program with recovered responsibilities and authority boundaries.
6. Current implementation evidence supports bounded recommendations and explicit stopping, not autonomous repair or implementation planning.

## Unsupported conclusions

The reviewed implementation does not support concluding that:

1. Seed can autonomously review any unfamiliar repository today.
2. Seed can infer arbitrary program purpose from repository contents.
3. Seed can recover intended responsibilities for arbitrary languages, frameworks, or domains without human-supplied authority evidence.
4. Seed's responsibility families are universal architecture categories.
5. Seed-specific self-review surfaces can already be replaced by a repository-neutral review engine.
6. Broad redesign or debugging recommendations are supported for an unfamiliar repository without target-specific authority and evidence.
7. Compatibility-breaking recommendations are currently supported by recovered methodology.

## Confidence

**Moderate.**

Confidence is high that the recovered methodology is evidence-first, authority-bounded, visibility-aware, compatibility-preserving, and explicitly stoppable. This is supported across multiple completed investigations and implementation surfaces.

Confidence is moderate, not high, that the methodology is repository-neutral. The concepts are neutral, and repository observation supports arbitrary paths in limited ways, but the strongest executable review and answer surfaces are still Seed-specific. The conclusion therefore remains bounded: repository-neutral review is methodologically supported, while a general implemented capability is not.

## Recommended next action

Perform a bounded **repository-neutral review input model investigation**.

The investigation should not implement review. It should recover whether current code already has enough implementation evidence to define the minimum neutral inputs for program review, likely including:

- repository identity and observation boundary;
- supplied program purpose or review concern;
- intended responsibility evidence source;
- observed implementation evidence source;
- authority and mutation boundary;
- visibility sufficiency result;
- bounded recommendation status;
- explicit stopping reason.

The investigation should specifically avoid importing Seed responsibility families as universal categories. If implementation evidence is insufficient, it should stop with the missing architecture rather than designing a planner or review engine.

## Acceptance answer

If Seed can honestly review an unfamiliar repository using recovered responsibilities, authority, visibility, and evidence, then reviewing Seed itself becomes merely another application of the same evidence-first methodology rather than a special self-improvement capability.

Current implementation evidence supports that conclusion **as methodology**, because self-review does not require special authority beyond observable responsibilities, evidence, visibility, bounded recommendations, and stopping.

Current implementation evidence does **not** yet support that conclusion as a completed implementation capability. Missing implementation-backed architecture includes:

- a repository-neutral review input model;
- target-specific intended-responsibility evidence acquisition;
- broader observed-implementation adapters beyond git status and Python import/definition facts;
- review answer surfaces that consume arbitrary repository evidence rather than Seed projected state;
- explicit sufficiency/confidence rules for unfamiliar repositories;
- compatibility-boundary recovery for target repositories;
- a stopping/report shape that is neutral without losing Seed's authority discipline.

Until those are recovered, the honest conclusion is:

```text
Repository-neutral review is implementation-backed as a recovered methodology.
Additional recovered architecture is still required before it is an implemented capability.
```
