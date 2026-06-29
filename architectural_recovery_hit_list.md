# Architectural Recovery Hit List

## Scope

This is a bounded implementation audit. It identifies candidate architectural
recoveries that are already visible in repository implementation evidence. It is
not a roadmap, design document, priority plan, or promise to implement every
candidate.

The selection rule is intentionally conservative:

- implementation evidence exists;
- ownership appears compressed;
- behavior already exists;
- compatibility can likely be preserved;
- bounded recovery appears feasible.

Candidates are rejected when they require greenfield architecture, a major
redesign, a new runtime model, large compatibility changes, LLM interpretation,
or future speculation. Repository authority wins.

## Evidence base reviewed

This audit used implementation-backed artifacts rather than preferred terms:

- completed recovery slices for Operational Responsibility, Execution Visibility,
  Observation-Derived Capability, Answer Composition, Inquiry Lineage, Structure
  Observation, Relationship Observation, and Observation Agreement;
- completed implementation audits including grammar visibility, responsibility
  family inventory, responsibility family stack, observation agreement
  classification, cross-substrate structural coincidence, and answer composition
  family completion;
- implementation modules that already expose bounded records, payloads,
  diagnostics, observers, compatibility handoffs, and read-only boundaries;
- tests that prove current observer, diagnostic, inquiry, projection, and
  agreement-adjacent surfaces.

The recurring implementation principle observed across these artifacts remains:

```text
Each recovered capability can create
observable conditions that make
adjacent recovery possible.
```

## Selection ordering

Candidates are ordered by strength of implementation evidence, not by interest or
preferred implementation sequence.

Evidence strength considers:

1. number of independent implementation surfaces showing the same pressure;
2. whether current behavior already exists behind compressed ownership;
3. presence of compatibility-preserving handoff patterns;
4. test coverage around the current behavior;
5. whether prior audits already bounded unsupported interpretations.

## High-confidence recoveries

### 1. Grammar Observation

**Implementation evidence**

- `implementation_grammar_visibility_audit.md` finds recurring implementation
  relation shapes across completed families, especially `A != B`, `A owns B`,
  `A produces B`, `A consumes B`, `A hands off to B`, `A preserves B`,
  `A bounds B`, `A derives B`, `A selects B`, `A explains B`, `A observes B`,
  and `A does not own B`.
- `seed_runtime/documentation_structure.py` already observes narrow explicit
  documentation relation records with left term, relation, right term, source
  path, line number, and evidence.
- `tests/test_documentation_structure.py` proves explicit relation-shaped forms
  are observed while prose-like, modal, list-item, and fenced-code examples are
  rejected.
- Completed slices repeatedly separate implementation-local payloads before
  compatibility handoff, which makes grammar observable as relation shape rather
  than vocabulary preference.

**Why it appears recoverable**

Grammar-like evidence already exists as observed relation shape. The compressed
responsibility is that grammar visibility is currently distributed across
Documentation Structure, implementation audits, and manually reviewed recovery
slices. A bounded recovery could preserve observed grammar forms without
becoming a grammar engine, lexicon authority, or prose interpreter.

**Expected ownership boundary**

Grammar Observation would own read-only observation of implementation-backed
relation shapes and their provenance. It would not own grammar interpretation,
responsibility recovery, semantic alignment, vocabulary stabilization, runtime
mutation, event-ledger writes, or cluster truth.

**Estimated implementation size**

Small to medium. The likely recovery shape is an internal observer or audit over
already-observed records and existing implementation artifacts, plus tests. A
public CLI or JSON surface would be a separate operational-surface task and is
not implied by this audit.

**Compatibility considerations**

High compatibility if implemented as an additive, read-only internal/audit layer
that consumes existing records and preserves existing public shapes. Risk rises
if it tries to reinterpret prose, rename relation vocabulary, or canonicalize
terms.

**Blocking dependencies**

- Existing documentation relation records must remain narrow and provenance-rich.
- Repository artifact and relationship observations should remain independent
  sources.
- Any diagnostic exposure would need diagnostic inventory and shape-audit updates.

**Confidence**

High. The recurring implementation grammar is already repeatedly documented and
backed by concrete record shapes and tests.

### 2. Observation Agreement implementation

**Implementation evidence**

- `observation_agreement_classification_audit.md` identifies Observation
  Agreement as read-only preservation of candidate agreement between independent
  observation streams.
- `cross_substrate_structural_coincidence_audit.md` shows a concrete narrower
  instance: documentation relation observations can coincide with repository
  artifact observations and relationship facts.
- `seed_runtime/knowledge/observation_agreement.py` already exists, as do
  `tests/test_observation_agreement.py`, showing the repository has begun to
  encode agreement-adjacent behavior.
- Structure Observation, Repository Artifact Observation, Documentation
  Structure, and Relationship Observation already preserve independent evidence
  streams with provenance and non-promotion boundaries.

**Why it appears recoverable**

Agreement behavior is conceptually bounded and already has source streams. The
compressed responsibility is that agreement is partly present as classification,
partly present in a narrower cross-substrate audit, and partly present in code.
A recovery could make the implementation owner explicit while preserving the
non-truth boundary.

**Expected ownership boundary**

Observation Agreement would own candidate agreement records between independent
observation streams. It would not parse raw substrates, decide architectural
truth, infer grammar, recover responsibility, stabilize lexicon, write ledger
facts, mutate repository state, or mutate cluster state.

**Estimated implementation size**

Small to medium, depending on how much of the existing
`observation_agreement.py` surface already matches the audited boundary. The
smallest safe slice would be internal record ownership and tests over supplied
records.

**Compatibility considerations**

Compatibility risk is low if existing observation records remain inputs and
agreement records are additive/read-only. Risk is medium if agreement output is
made public before diagnostic inventory, shape-audit, and record-scope contracts
are updated.

**Blocking dependencies**

- Independent observation streams must remain provenance-preserving.
- Agreement records must retain non-promotion language.
- If exposed diagnostically, diagnostic inventory and shape audit must be updated.

**Confidence**

High. Multiple audits already converge on the same boundary, and code/tests for
agreement exist.

### 3. Cross-substrate agreement records

**Implementation evidence**

- `cross_substrate_structural_coincidence_audit.md` identifies a minimal
  documentation-relation plus repository-artifact plus relationship-fact model.
- Documentation Structure already emits explicit relation records.
- Repository Artifact Observation already emits module/class/function/method and
  import facts from supplied Python source text.
- Relationship Observation already emits shared `RelationshipFact` records from
  documentation navigation metadata, Python import syntax, and Python definition
  syntax.

**Why it appears recoverable**

The behavior already exists as separate observable streams. The compressed
responsibility is the absence of a first-class candidate correspondence record
that preserves that independently observed convergence without promoting it to
truth.

**Expected ownership boundary**

Cross-substrate agreement records would own candidate correspondence between
already-observed documentation-side and implementation-side evidence. They would
not own substrate parsing, semantic equivalence, documentation truth,
implementation truth, architecture inference, responsibility recovery, or
lexicon stabilization.

**Estimated implementation size**

Small. A bounded implementation could operate over supplied records and return
read-only candidate correspondence records with provenance.

**Compatibility considerations**

Low risk if additive and internal/test-only. Compatibility risk increases if the
records are surfaced through CLI/JSON without the required diagnostic inventory
and shape-audit contracts.

**Blocking dependencies**

- Observation Agreement boundary should remain settled.
- Documentation, repository artifact, and relationship records must preserve
  source path, line number where available, symbols, relation text, and evidence.

**Confidence**

High. This is the most concrete instance of Observation Agreement and has the
clearest bounded record shape.

### 4. Projection influence lineage

**Implementation evidence**

- `inquiry_lineage_family_vocabulary_audit.md` includes projection products,
  influence edges, and non-influence edges among result/lineage material.
- `seed_runtime/projection_shape.py`, `seed_runtime/projection_store.py`,
  `seed_runtime/projected_state_consumers.py`, and related tests already expose
  projection shape, storage, and consumer relationships.
- Inquiry Lineage slices repeatedly recover result-like material as distinct from
  the lineage frame that explains how it was selected, derived, compared,
  bounded, or left incomplete.

**Why it appears recoverable**

Projection behavior already exists, and lineage pressure has already been
recovered in nearby inquiry surfaces. The compressed responsibility appears to be
that projection outputs and projection influence evidence are still mixed across
shape/store/consumer surfaces rather than owned as a bounded lineage record.

**Expected ownership boundary**

Projection influence lineage would own how a projection result was influenced by
inputs, consumers, evidence paths, and non-influencing alternatives. It would not
own projection computation, state truth, event replay, storage mutation, or
presentation rendering.

**Estimated implementation size**

Medium. The likely slice would separate implementation-local projection result
payloads from influence-lineage payloads before compatibility handoff, mirroring
completed Inquiry Lineage recoveries.

**Compatibility considerations**

Medium-low risk if private payloads preserve existing projection shapes. Risk is
higher if public projection JSON, event semantics, or state schema are changed.
Those changes are not justified by this audit.

**Blocking dependencies**

- Existing projection compatibility objects must be preserved.
- The implementation must avoid treating presentation labels such as projection
  cache as preserved knowledge unless proven by implementation evidence.

**Confidence**

High. The lineage grammar is mature, and projection surfaces already exist, but
this specific boundary is not yet as explicitly recovered as selection,
derivation, or reference lineage.

### 5. Read-model ownership recovery

**Implementation evidence**

- `seed_runtime/state_views.py`, `seed_runtime/state_summary_views.py`,
  `seed_runtime/context_views.py`, `seed_runtime/projection_shape.py`, and
  `seed_runtime/projected_state_consumers.py` already expose multiple read-side
  views over state/projection material.
- Tests exist for state views, state summary views, context views, projection
  shape, state projection, and projected-state consumers.
- Completed Execution Visibility and Answer Composition work repeatedly preserves
  compatibility objects while moving ownership into implementation-local payloads
  or builders.

**Why it appears recoverable**

Read behavior exists in several surfaces, but ownership appears compressed
between projected state, read-model construction, consumer-specific formatting,
and answer/presentation surfaces. The recovery candidate is the read-model owner,
not a new state model.

**Expected ownership boundary**

Read-model ownership would own construction of read-only, consumer-safe state
views from already-projected or already-observed state. It would not own event
application, ledger truth, cluster mutation, projection computation, or final
presentation text.

**Estimated implementation size**

Medium. Likely requires private read-model payloads and tests around existing
view builders while preserving public dataclasses and renderers.

**Compatibility considerations**

Medium-low if recovered behind current view APIs. High if it changes state schema
or public JSON; those changes are explicitly outside this audit.

**Blocking dependencies**

- Projection compatibility boundaries must remain stable.
- Presentation ownership must remain distinct from read-model ownership.

**Confidence**

High. The behavior is broad and tested, and ownership compression is visible, but
the exact minimal slice needs a focused implementation audit before coding.

## Medium-confidence recoveries

### 6. Projection agreement

**Implementation evidence**

- Observation Agreement already has a bounded candidate-agreement classification.
- Projection shape, projected-state consumers, and knowledge reachability/cache
  tests already observe projection-related outputs.
- Cross-substrate agreement shows how independent streams can converge without
  becoming truth.

**Why it appears recoverable**

Projection outputs can likely be compared against independent observations,
diagnostics, tests, or documentation structures as candidate agreement. The
compressed responsibility is that projection agreement currently lacks a bounded
record distinct from projection computation and observation agreement in general.

**Expected ownership boundary**

Projection agreement would own candidate agreement between projection-derived
records and independently observed records. It would not own projection truth,
state mutation, event replay, semantic alignment, or responsibility recovery.

**Estimated implementation size**

Medium. It likely depends on first clarifying Observation Agreement implementation
and projection influence lineage boundaries.

**Compatibility considerations**

Medium. Safe as an additive read-only agreement record; risky if used to validate
or mutate projected state.

**Blocking dependencies**

- Observation Agreement implementation boundary.
- Stable projection provenance sufficient to compare independent streams.

**Confidence**

Medium-high. Evidence is strong for the components, but the exact agreement
surface is less directly proven than cross-substrate agreement.

### 7. Evidence provenance recovery

**Implementation evidence**

- Many records already carry evidence/provenance fields, including documentation
  relation records, repository artifact facts, relationship facts, verification
  evidence, reasoning path evidence, selection path evidence, reference selection
  rationale, and inquiry artifacts.
- `seed_runtime/evidence.py`, `seed_runtime/evidence_graph.py`,
  `seed_runtime/verification_evidence.py`, and their tests already preserve
  evidence-related behavior.
- Observation Agreement and grammar visibility both require provenance
  preservation to remain non-promotional.

**Why it appears recoverable**

Evidence behavior exists in many places, but provenance ownership appears
compressed across record-specific fields. A bounded recovery could identify the
owner of provenance preservation and handoff without redesigning every evidence
record.

**Expected ownership boundary**

Evidence provenance recovery would own preservation of where a claim, relation,
selection, observation, or agreement came from. It would not own claim truth,
fact admission, semantic interpretation, event-ledger writes, or cluster state.

**Estimated implementation size**

Medium. The safest recovery would begin with a narrow internal provenance record
or helper used by one or two surfaces, not a global schema rewrite.

**Compatibility considerations**

Medium. Compatibility can likely be preserved through adapters or private
payloads. Risk becomes high if existing evidence fields are renamed or public
schemas are normalized globally.

**Blocking dependencies**

- A specific first surface must be selected by implementation evidence, not by
  conceptual preference.
- Existing public evidence fields must remain stable.

**Confidence**

Medium-high. Provenance is everywhere, but the repository has not yet proven one
universal provenance owner.

### 8. Responsibility Recovery

**Implementation evidence**

- Responsibility-family inventory and stack audits already classify completed,
  ready, additional-recovery, and insufficient-evidence families.
- Completed slices show recurring owner/composer/validator/executor/presenter/
  recorder boundaries.
- Grammar visibility can observe relation shape, and Observation Agreement can
  preserve convergent observations, both of which can feed responsibility review.

**Why it appears recoverable**

Responsibility recovery already happens through bounded implementation slices,
but the mechanics remain mostly manual and audit-shaped. The compressed
responsibility is the absence of an implementation owner for preserving candidate
responsibility-recovery evidence without deciding truth.

**Expected ownership boundary**

Responsibility Recovery would own candidate recovery evidence and boundary
classification from implementation artifacts. It would not own architectural
truth, implementation priority, roadmap creation, LLM interpretation, or automatic
promotion of presentation vocabulary.

**Estimated implementation size**

Medium to large. A safe first slice would be narrow and evidence-preserving, not
a general recovery engine.

**Compatibility considerations**

Medium. Additive audit records are low risk; automatic classification or public
surfaces would require careful diagnostic and shape-audit contracts.

**Blocking dependencies**

- Grammar Observation should remain non-promotional.
- Observation Agreement should remain distinct from responsibility recovery.
- Presentation vocabulary must not be promoted without knowledge-reachability
  evidence.

**Confidence**

Medium. The repository clearly performs this work, but a bounded implementation
owner is harder to recover safely than the lower-level observation/agreement
records.

### 9. Documentation drift observation

**Implementation evidence**

- Documentation Structure already observes documentation mechanics and explicit
  relation-shaped records.
- Repository Artifact Observation and Relationship Observation can independently
  observe implementation structures and relationships.
- Cross-substrate structural coincidence already frames documentation and
  implementation alignment as candidate correspondence, not truth.

**Why it appears recoverable**

Drift can be treated as a read-only observation that documentation-side records
and implementation-side records no longer show expected candidate agreement. The
compressed responsibility is currently split between documentation observation,
repository observation, and agreement audits.

**Expected ownership boundary**

Documentation drift observation would own candidate documentation/implementation
mismatch records with provenance and uncertainty. It would not own documentation
rewrites, implementation changes, semantic equivalence, lexicon authority, or
architectural truth.

**Estimated implementation size**

Medium. It likely depends on cross-substrate agreement records first.

**Compatibility considerations**

Low to medium if additive and read-only. Risk increases if drift findings are
attached directly to cluster/runtime truth or used to mutate docs automatically.

**Blocking dependencies**

- Cross-substrate agreement records or equivalent candidate correspondence.
- Provenance retention for both documentation and implementation streams.

**Confidence**

Medium. Evidence supports it, but drift requires a prior agreement baseline or
explicit expected-correspondence source.

### 10. Implementation drift observation

**Implementation evidence**

- Repository Artifact Observation, Relationship Observation, diagnostic shape
  audit, diagnostic inventory, and many tests already observe implementation
  structure and surface conformance.
- Completed visibility work separates declarations from conformance checks.
- Existing shape-audit behavior already distinguishes expected diagnostic shapes
  from actual implementation output.

**Why it appears recoverable**

Implementation drift appears as an adjacent generalization of existing shape and
conformance checks. The compressed responsibility is that drift detection is
currently surface-specific rather than owned as implementation drift observation.

**Expected ownership boundary**

Implementation drift observation would own read-only mismatch observations
between expected implementation surfaces and currently observed implementation
artifacts. It would not own code changes, schema changes, runtime mutation,
semantic inference, or architectural truth.

**Estimated implementation size**

Medium. A narrow first slice could be built around one existing conformance
family rather than a repository-wide drift engine.

**Compatibility considerations**

Medium. Safe if read-only and additive; risky if it changes diagnostic outputs or
turns every drift into a failing operational contract.

**Blocking dependencies**

- Clear expected-surface source for the first slice.
- Diagnostic inventory and shape-audit updates if exposed diagnostically.

**Confidence**

Medium. Surface-specific behavior exists; repository-wide ownership is not yet
proven.

### 11. Coverage observation

**Implementation evidence**

- `seed_runtime/classification_coverage.py`, `seed_runtime/observation_inventory.py`,
  `seed_runtime/capability_inventory.py`, `seed_runtime/diagnostic_inventory.py`,
  and associated tests already compute inventory/coverage-like surfaces.
- Responsibility-family inventory audits classify maturity and gaps using
  implementation evidence.
- Diagnostic inventory already treats visibility of surfaces as a first-class
  operational concern.

**Why it appears recoverable**

Coverage behavior exists, but responsibility is split across classification,
observation, capability, diagnostic, and audit-specific inventories. A recovery
could bound coverage observation as a read-only inventory of what evidence/surface
families are covered and what remains unobserved.

**Expected ownership boundary**

Coverage observation would own read-only coverage records over existing surfaces,
inputs, and tests. It would not own capability admission, architectural truth,
roadmap priority, or implementation selection.

**Estimated implementation size**

Medium. Existing inventory patterns make the shape feasible, but the first scope
must be narrow.

**Compatibility considerations**

Medium-low if additive. Public diagnostic exposure requires the standard
inventory and shape-audit updates.

**Blocking dependencies**

- Decide first covered domain using implementation evidence.
- Preserve distinction between coverage observation and coverage enforcement.

**Confidence**

Medium. Existing inventory surfaces are strong, but coverage ownership could
become too broad without a bounded first slice.

### 12. Presentation ownership recovery

**Implementation evidence**

- Answer Composition separates answer construction from rendering in operational
  story and inquiry orientation.
- `format_operational_story(...)` and `format_inquiry_orientation(...)` render
  compatibility objects without owning selection, reasoning, or boundary
  construction.
- AGENTS instructions explicitly warn that presentation vocabulary is not
automatically knowledge.

**Why it appears recoverable**

Presentation behavior exists and has been separated from answer composition in
some surfaces. Ownership remains compressed across renderers, compatibility
objects, answer composition, and presentation labels.

**Expected ownership boundary**

Presentation ownership would own formatting and operator-facing presentation of
already-composed compatibility objects. It would not own answer selection,
reasoning, evidence truth, knowledge promotion, or presentation-vocabulary
stabilization.

**Estimated implementation size**

Medium. A narrow recovery could start with a completed Answer Composition surface
and preserve current output exactly.

**Compatibility considerations**

Medium. High sensitivity to output snapshots/text expectations. Public output
must remain compatible unless explicitly changed.

**Blocking dependencies**

- A specific formatter must be selected as first slice.
- Knowledge reachability evidence must be used before preserving presentation
  vocabulary as repository knowledge.

**Confidence**

Medium. The boundary is visible in completed surfaces, but broader presentation
ownership is not yet as mature as answer composition itself.

## Speculative recoveries

Speculative does not mean unsupported. It means implementation evidence exists,
but the current boundary is not yet strong enough to justify immediate bounded
implementation without another focused audit.

### 13. Architectural consistency observation

**Implementation evidence**

- Architecture conformance audit, component audit, diagnostic shape audit,
  question surface inventory, relationship observation, and grammar visibility
  all observe pieces of consistency or conformance.
- Tests exist for architecture conformance, component audit, diagnostic shape
  audit, relationship observation, and question surface inventory.

**Why it appears recoverable**

Consistency pressure is visible across conformance and observation surfaces.
However, an architectural consistency observer could easily overreach into
truth-claims or preferred architecture unless carefully bounded.

**Expected ownership boundary**

Architectural consistency observation would own read-only candidate consistency
or inconsistency records between already-authoritative implementation surfaces.
It would not own architectural truth, roadmap decisions, semantic interpretation,
or automatic remediation.

**Estimated implementation size**

Medium to large. Needs a focused audit to identify the smallest safe consistency
pair.

**Compatibility considerations**

Medium-high. The risk is not technical compatibility alone; it is authority
creep. Any diagnostic exposure also triggers inventory and shape-audit work.

**Blocking dependencies**

- More explicit agreement/provenance boundaries.
- A narrow first consistency domain.

**Confidence**

Speculative-medium. Evidence exists, but ownership is not yet bounded enough.

### 14. Architectural consistency versus drift separation

**Implementation evidence**

- Drift-like evidence appears in documentation/implementation agreement,
  diagnostic shape audit, and architecture conformance audit.
- Consistency-like evidence appears in architecture conformance, invariant tests,
  and relationship observation.

**Why it appears recoverable**

The repository may eventually need to separate “surfaces disagree” from “surface
violates a required architecture rule.” Current evidence hints at that boundary,
but most surfaces still use domain-specific language.

**Expected ownership boundary**

This recovery would own the distinction between candidate drift observations and
required consistency/conformance findings. It would not own either domain's raw
observation or remediation.

**Estimated implementation size**

Medium.

**Compatibility considerations**

Medium-high because it could affect audit language and failure semantics if not
kept internal/read-only.

**Blocking dependencies**

- Documentation drift or implementation drift observation should be recovered
  first.
- Conformance surfaces must remain distinct from observation surfaces.

**Confidence**

Speculative-medium.

### 15. Repository artifact observation acquisition workflow

**Implementation evidence**

- Repository Artifact Observation can parse supplied Python source text and emit
  bounded implementation facts.
- Prior responsibility-family inventory classifies repository observation
  acquisition as requiring additional recovery because adapter evidence exists
  but acquisition workflow ownership is not stabilized.

**Why it appears recoverable**

The adapter behavior exists, but traversal, filtering, ingestion, command/query
surface, and compatibility boundaries remain compressed or absent.

**Expected ownership boundary**

An acquisition workflow would own how repository files are selected and supplied
to existing observation adapters. It would not own repository artifact record
semantics, relationship facts, responsibility recovery, event mutation, or
cluster truth.

**Estimated implementation size**

Medium to large.

**Compatibility considerations**

Medium-high because a workflow may become an operational surface, which would
require diagnostic inventory, shape-audit, and possibly CLI/API contracts if
exposed.

**Blocking dependencies**

- Clear operational surface decision.
- Diagnostic visibility contract if exposed.
- Filtering and traversal boundary that avoids broad repository authority claims.

**Confidence**

Speculative-medium. The adapter is real; the workflow boundary is not yet proven.

### 16. Capability-to-operation compatibility handoff recovery

**Implementation evidence**

- Observation-Derived Capability completed slices distinguish observed evidence,
  capability verification, promotion readiness, capability inventory, and
  executable operation contract.
- Operational Responsibility owns registered operation recommendation,
  selection, validation, policy authorization, execution, recording, and
  post-execution extraction.
- Capability inventory intentionally unions admitted capability knowledge,
  requested capability needs, and registered operation contract labels.

**Why it appears recoverable**

The handoff between observed/read-only capability knowledge and executable
operation metadata is visible, but it may not yet have a first-class recovered
owner.

**Expected ownership boundary**

This handoff would own compatibility translation between capability inventory
context and executable operation contract labels. It would not own capability
truth, operation execution, policy authorization, or promotion/admission.

**Estimated implementation size**

Medium.

**Compatibility considerations**

Medium. Safe if it preserves existing recommendation/selection behavior; risky if
it changes operation ranking or capability admission semantics.

**Blocking dependencies**

- A focused audit of current capability inventory to operation selection paths.
- Preserve separation between read-only inventory and executable contract.

**Confidence**

Speculative-medium. The boundary is visible, but adjacent completed families may
already cover enough that a separate owner could be unnecessary.

### 17. Unified provenance-backed recovery backlog

**Implementation evidence**

- This hit list, responsibility-family inventory, grammar visibility,
  observation agreement, and recoverability audits all preserve candidate
  recovery opportunities.
- The repository repeatedly distinguishes candidate evidence from roadmap or
  implementation promise.

**Why it appears recoverable**

The repository now has multiple audit documents functioning as candidate
recovery memory. However, implementing a backlog-like artifact risks becoming a
roadmap or planning system, which is explicitly outside several prior audit
scopes.

**Expected ownership boundary**

A provenance-backed recovery backlog would own durable candidate evidence records
for recoverable architecture. It would not own priority, scheduling, commitment,
roadmap, or implementation order.

**Estimated implementation size**

Medium.

**Compatibility considerations**

Medium-high because this can easily become process architecture rather than
implementation recovery. It should remain document/audit-backed unless future
implementation evidence justifies a record type.

**Blocking dependencies**

- Evidence provenance recovery.
- Clear non-roadmap boundary.

**Confidence**

Speculative-low to medium. The repository has earned this document, but not yet a
runtime or schema-backed backlog capability.

## Rejected or deferred prompts

The following prompts were considered but not admitted as high- or
medium-confidence recoveries in their broad form:

- **LLM interpretation of candidate architecture**: rejected. Current evidence
  supports deterministic, implementation-backed observation and audits, not LLM
  semantic inference.
- **Global schema normalization for evidence/provenance/agreement**: deferred.
  Compatibility risk is too high without a bounded first surface.
- **Automatic roadmap generation**: rejected. This document is a candidate
  recovery inventory, not a plan or promise.
- **Public CLI/JSON diagnostic exposure for every candidate**: rejected. Any new
  operational surface would require the diagnostic inventory and shape-audit
  contract and is outside this audit.
- **Presentation vocabulary promotion**: rejected unless proven through
  implementation evidence such as knowledge reachability. Presentation labels are
  not automatically repository knowledge.

## Summary answer

If development stopped today, the most visible recoverable architecture already
waiting inside the implementation is the observation layer around relation shape,
agreement, provenance, projection lineage, and read-model ownership.

The repository has especially strong evidence for recovering:

1. Grammar Observation as non-promotional relation-shape observation;
2. Observation Agreement as candidate agreement between independent streams;
3. Cross-substrate agreement records as the first concrete agreement instance;
4. Projection influence lineage as an Inquiry Lineage-adjacent recovery;
5. Read-model ownership as a compatibility-preserving boundary around existing
   state/projection views.

The repository has medium evidence for projection agreement, evidence provenance,
responsibility recovery, drift observation, coverage observation, and
presentation ownership. It has speculative but visible evidence for broader
architectural consistency, acquisition workflow, capability-to-operation handoff,
and a provenance-backed recovery backlog.

None of these candidates should be treated as a required implementation order.
They are candidate recoveries: places where existing behavior, compressed
ownership, compatibility-preserving patterns, and bounded evidence suggest that
architecture is already present and waiting to be uncovered.
