# Architectural Recovery Hit List

## Scope

This document is a bounded implementation audit of the strongest remaining
architectural recovery opportunities visible in the current repository. It is not
a roadmap, implementation plan, redesign proposal, or request to invent new
ontology. Repository authority wins.

A candidate is included only when implementation evidence already shows:

- existing behavior;
- compressed ownership;
- clear compatibility preservation path;
- bounded recovery surface;
- observable recurring implementation pattern.

A candidate is rejected or deferred when it primarily requires new architecture,
runtime redesign, future speculation, LLM interpretation, a major compatibility
migration, or greenfield implementation.

## Evidence Base Reviewed

The audit reviewed the current recovery corpus and implementation surfaces,
including completed recovery slices, implementation characterization reports,
ownership recovery reports, answer composition slices, inquiry lineage slices,
grammar observation, observation agreement, structure observation,
responsibility recovery, artifact composition investigations, provider contract
investigations, question family investigations, execution visibility,
operational responsibility, incremental replay ownership recovery,
documentation structure investigations, diagnostic inventory, and diagnostic
shape audit.

Recurring repository pattern:

```text
implementation-local evidence -> bounded compatibility handoff ->
read-only/recorded visibility -> explicit non-ownership boundary
```

That pattern is stronger evidence than vocabulary recurrence alone.

## Selection Ordering

The ordering below reflects implementation evidence strength, not desirability.
Ready candidates have enough implementation pressure for a bounded ownership or
boundary recovery. Medium/deferred candidates may be real, but current evidence
is not yet strong enough to justify recovery without another implementation audit.

---

## Ready Now

### 1. Projection Influence Lineage

**Type:** ownership recovery; boundary recovery; behavior characterization.

**Summary**

Projection and replay behavior now expose enough implementation-local evidence to
recover a lineage boundary around how projection results were influenced, without
changing projection computation, cache behavior, or read-model output.

**Current implementation owner(s)**

- `seed_runtime.state` owns event replay, affected-projection visibility, full
  projection finalization, and compatibility-preserving replay target selection.
- `seed_runtime.projection_store` owns projection snapshot/cache persistence and
  dependent summary/index snapshot compatibility.
- `seed_runtime.projection_shape`, `seed_runtime.projected_state_consumers`, and
  state/read-view modules own consumer-visible projection/read shapes.

**Compressed responsibility**

Influence evidence is currently mixed through replay diagnostics, affected-scope
recovery, projection cache load/save behavior, summary/index snapshot dependency
checks, and consumer descriptions. The repository can describe that a projection
was rebuilt, cached, or dependent on state projection versions, but the lineage
record that explains influence remains compressed across those owners.

**Implementation evidence**

- `seed_runtime/state.py` names affected projection recovery as descriptive and
  explicitly says it does not mark projections dirty, schedule work, change cache
  invalidation, or optimize projection execution.
- `seed_runtime/state.py` preserves affected projections as input evidence while
  continuing to use full event replay and full projection finalization.
- `seed_runtime/projection_store.py` persists state projection snapshots and
  dependent summary/index snapshots keyed by projection version and state
  projection version, proving compatibility-preserving dependency checks already
  exist.
- Incremental replay ownership slices show pre-optimization replay evidence was
  recovered without changing the replay execution path.

**Expected recovery**

Recover a read-only projection influence lineage owner that preserves:

- influencing input/event scope;
- derived projection surfaces named by current implementation;
- replay target selection evidence;
- cache/dependent snapshot compatibility evidence;
- explicit non-influence where the implementation kept full replay/finalization.

It must not own projection computation, event replay, projection storage,
projection truth, cache invalidation, read-model construction, presentation, or
cluster mutation.

**Estimated implementation size**

Medium. A safe slice would introduce implementation-local lineage records around
existing replay/projection compatibility paths and tests proving current behavior
is preserved.

**Compatibility risk**

Medium-low if implemented behind existing projection/replay APIs and outputs.
High if it changes state schemas, cache semantics, replay narrowing, or public
JSON. Those are outside this recovery.

**Blocking dependencies**

- Preserve full replay/finalization semantics unless a separate future behavior
  task changes them.
- Avoid promoting presentation labels such as “projection cache” into repository
  knowledge without implementation evidence.

**Confidence**

High.

**Why now**

The repository has already recovered incremental replay ownership boundaries.
Projection influence lineage is the strongest adjacent boundary still compressed
inside implementation behavior rather than vocabulary.

---

### 2. Read-Model Ownership Recovery

**Type:** ownership recovery; boundary recovery.

**Summary**

The repository has multiple read-side views over projected state. Construction of
consumer-safe read models is visible but still compressed between state
projection, projection storage, context/state views, consumer descriptions, and
answer/presentation surfaces.

**Current implementation owner(s)**

- `seed_runtime.state_views` and `seed_runtime.state_summary_views` expose
  read-only state/summary views.
- `seed_runtime.context_views` exposes context-oriented views.
- `seed_runtime.projection_shape` and `seed_runtime.projected_state_consumers`
  describe projection shapes and consumers.
- `seed_runtime.projection_store` stores read-compatible projection snapshots and
  dependent summary/index snapshots.

**Compressed responsibility**

Read models are built in several modules according to consumer need. The common
owner of “construct a read-only compatibility view from projected state” is not
explicitly recovered.

**Implementation evidence**

- Tests exercise state views, state summary views, context views, projection
  shape, projected-state consumers, and state projection behavior.
- `tests/test_state_views.py` includes a guard that CLI state-view commands do
  not invoke runtime providers, policy, or tools.
- `tests/test_projected_state_consumers.py` proves projected-state consumer
  boundaries include no provider acquisition.
- `seed_runtime/projection_store.py` serializes enough state to serve read-only
  projection CLI output and validates dependent read-model snapshots against the
  underlying state projection version.

**Expected recovery**

Recover read-model ownership as the boundary that constructs read-only,
consumer-safe views from already-projected state or already-observed records.

It must not own event application, ledger truth, projection computation,
provider/tool invocation, runtime policy, answer composition, or final
presentation language.

**Estimated implementation size**

Medium. Likely one focused read surface first, with private payloads/adapters that
preserve existing public dataclasses and output.

**Compatibility risk**

Medium-low behind current APIs; high if state schema or CLI/JSON output changes.

**Blocking dependencies**

- Projection compatibility boundaries must remain stable.
- Presentation ownership must remain separate.

**Confidence**

High.

**Why now**

Behavior is broad, tested, and explicitly read-only. The recovery is ownership
clarification, not new runtime behavior.

---

### 3. Documentation ↔ Code Agreement Observation

**Type:** boundary recovery; implementation audit; compatibility characterization.

**Summary**

The repository has independent documentation-structure, repository-artifact, and
relationship observations. Cross-substrate agreement is the strongest concrete
instance of Observation Agreement still waiting for a bounded recovered owner.

**Current implementation owner(s)**

- Documentation structure observation owns explicit documentation relation
  records.
- Repository artifact observation owns implementation artifact facts from source.
- Relationship observation owns relationship facts from documentation navigation
  metadata and Python syntax.
- Observation Agreement owns or begins to own candidate agreement between
  independent observations.

**Compressed responsibility**

Candidate agreement between documentation-side and code-side evidence is still
mostly document/audit-shaped. The first-class record preserving “these
independent streams appear to correspond” is not consistently owned.

**Implementation evidence**

- Documentation structure tests prove narrow explicit relation-shaped forms are
  observed while prose-like or fenced examples are rejected.
- Observation Agreement tests build candidate agreements from independent
  documentation relation records, repository artifact facts, and relationship
  facts.
- Cross-substrate structural coincidence audit identifies documentation relation
  observations, repository artifact observations, and relationship facts as the
  minimal coincidence model.

**Expected recovery**

Recover read-only documentation ↔ code agreement records with provenance on both
sides. The records should preserve correspondence without promoting it to
architecture truth.

They must not own raw parsing, semantic equivalence, responsibility recovery,
lexicon stabilization, documentation rewrites, implementation mutation, or
cluster truth.

**Estimated implementation size**

Small to medium. The first slice can operate over supplied records and preserve
existing public shapes.

**Compatibility risk**

Low if internal/additive; medium if exposed through CLI or JSON because the
operational visibility contract would require diagnostic inventory and shape-audit updates.

**Blocking dependencies**

- Independent observation streams must retain provenance.
- Observation Agreement must remain non-promotional.

**Confidence**

High.

**Why now**

This is narrower and more implementation-backed than generic architectural
consistency or drift. It is the safest agreement boundary to recover next.

---

### 4. Evidence Contract Family

**Type:** ownership recovery; compatibility characterization.

**Summary**

Evidence/provenance fields recur across observations, inquiry lineage, answer
composition, capability verification, agreement, and diagnostics. A bounded
Evidence Contract recovery can clarify preservation and handoff of evidence
without creating a universal evidence schema.

**Current implementation owner(s)**

- `seed_runtime.evidence`, `seed_runtime.evidence_graph`, and
  `seed_runtime.verification_evidence` own evidence-specific behavior.
- Observation, agreement, inquiry, answer, capability, and diagnostic modules own
  domain-specific evidence fields.

**Compressed responsibility**

Each family preserves evidence locally, but the compatibility contract for “what
must survive handoff as evidence” is distributed across many record types.

**Implementation evidence**

- Observation records preserve source path, line/evidence, artifact kind, or
  relationship source.
- Inquiry Lineage slices preserve selection, derivation, reference, and open-gap
  evidence separately from conclusions.
- Answer Composition slices preserve reasoning/support context before rendering.
- Capability verification and inventory tests preserve verification source/state
  distinctions including provider-reported state.
- Diagnostic inventory and shape audit preserve expected output shape and record
  boundaries.

**Expected recovery**

Recover a narrow evidence contract that states what evidence handoffs preserve:
source, subject, observed relation/fact, scope, confidence/status where present,
and non-promotion boundary.

It must not own claim truth, fact admission, global schema normalization,
semantic interpretation, event-ledger writes, or cluster mutation.

**Estimated implementation size**

Medium. Start with one or two families and adapters; do not rewrite all evidence
records.

**Compatibility risk**

Medium. Low if additive/private; high if public fields are renamed or normalized
across the repository.

**Blocking dependencies**

- Select first surface by implementation pressure, not conceptual neatness.
- Preserve existing public evidence fields.

**Confidence**

Medium-high.

**Why now**

The pattern is recurring and implementation-backed. The recovery should be
bounded because a universal schema is not yet earned.

---

### 5. QuestionFamily Admission Characterization

**Type:** compatibility characterization; behavior characterization.

**Summary**

Question-family dispatch and admission behavior appears sufficiently visible for
a characterization slice that documents and tests what is admitted, rejected, and
preserved at compatibility boundaries.

**Current implementation owner(s)**

- Question-family registration/dispatch modules and tests.
- Inquiry artifact and inquiry orientation surfaces that classify artifact
  visibility and boundary behavior.

**Compressed responsibility**

Admission rules, dispatch compatibility, and inquiry artifact classification are
close but not fully separated as a stable boundary.

**Implementation evidence**

- `question_family_registration_boundary_audit.md` identifies the registration
  boundary.
- Question surface and inquiry artifact tests prove conservative classifications
  and diagnostic inventory/shape-audit registration for inquiry artifacts.
- Answer Composition and Inquiry Lineage slices show dispatch results should not
  own reasoning, evidence truth, or presentation vocabulary.

**Expected recovery**

Characterize QuestionFamily admission as the compatibility boundary deciding
whether a question shape is registered/handled, with conservative fallback for
visible-but-not-owned artifacts.

It must not own answer quality, LLM behavior, architectural truth, or future
question ontology.

**Estimated implementation size**

Small to medium, primarily characterization/tests unless gaps are found.

**Compatibility risk**

Medium because question dispatch can affect user-visible behavior. Safe if it
preserves existing fallback/output shapes.

**Blocking dependencies**

- Keep admission separate from answer composition and inquiry lineage.
- Any new diagnostic surface must update diagnostic inventory and shape audit.

**Confidence**

Medium-high.

**Why now**

The repository has enough completed answer/inquiry work to characterize
admission without inventing a new question ontology.

---

## Needs More Evidence

### 6. Family Recovery

**Summary**

The repository repeatedly uses “family” to group recovered responsibilities, but
an implementation owner for Family Recovery risks becoming vocabulary-first.

**Implementation evidence**

Responsibility-family inventory/stack audits classify completed and candidate
families; completed slices show repeated owner/boundary/handoff patterns.

**Expected recovery**

Eventually, a read-only family-recovery evidence record could preserve why a set
of slices belongs together.

**Confidence**

Medium.

**Why not yet**

Current evidence supports family as audit organization more than runtime or
implementation ownership. Recover narrower candidates first.

---

### 7. Artifact Composition Implementation

**Summary**

Artifact composition has characterization evidence, but ownership boundaries
between artifact kind, artifact composition, inquiry artifacts, and answer
composition remain insufficiently separated for immediate recovery.

**Implementation evidence**

Artifact kind answer-composition audit, inquiry artifact CLI/tests, and artifact
composition investigations show visible behavior.

**Expected recovery**

A bounded artifact composition owner would assemble already-observed artifacts
into compatibility-preserving inquiry/answer artifacts.

**Confidence**

Medium.

**Why not yet**

Current behavior may still be adequately owned by Inquiry Lineage and Answer
Composition. More implementation evidence is needed before adding a separate
owner.

---

### 8. Artifact Kind Implementation

**Summary**

Artifact kinds are visible as classifications and compatibility labels, but the
repository has not yet proven that kind assignment needs an independent owner.

**Implementation evidence**

Artifact kind audits, inquiry artifact classifications, diagnostic inventories,
and repository artifact observations all use kind-like distinctions.

**Expected recovery**

A future characterization could distinguish artifact-kind classification from
artifact composition and presentation.

**Confidence**

Medium-low.

**Why not yet**

Kind labels are recurring, but could remain local compatibility vocabulary unless
more cross-surface implementation pressure appears.

---

### 9. Provider Contract Implementation

**Summary**

Provider contract behavior is visible in operation recommendations, capability
inventory, provider-reported verification state, and non-executable handoff
plans. A full provider contract owner is plausible but not yet safely bounded.

**Implementation evidence**

- Recommendation/ranker tests preserve provider choice and reasoning.
- Capability inventory distinguishes provider-reported state from verified and
  unverified states.
- Handoff plans explicitly create non-executable provider handoffs and avoid
  approving, authorizing, registering tools, or managing provider jobs.
- State/read-view tests guard against provider acquisition in read-only surfaces.

**Expected recovery**

A compatibility-preserving provider contract owner could describe provider
metadata and handoff boundaries without executing providers.

**Confidence**

Medium.

**Why not yet**

Operational Responsibility and Observation-Derived Capability already recovered
large adjacent boundaries. More focused evidence is needed to avoid duplicating
those owners.

---

### 10. Capability Handoff Implementation

**Summary**

Capability-to-operation handoff is visible, but may already be sufficiently
covered by Observation-Derived Capability plus Operational Responsibility.

**Implementation evidence**

Capability inventory unions admitted capability knowledge, requested capability
needs, and registered operation contract labels; operational recommendation,
selection, authorization, execution, recording, and post-execution extraction are
already recovered.

**Expected recovery**

If needed, recover only the compatibility translation between read-only
capability inventory context and executable operation contract labels.

**Confidence**

Medium.

**Why not yet**

A separate owner may be unnecessary. Do not recover unless implementation shows
handoff logic is compressed enough to cause ambiguity or duplicated behavior.

---

### 11. Observation Agreement Evolution

**Summary**

Observation Agreement exists, and cross-substrate agreement is ready. Evolution
of agreement over time is not yet sufficiently evidenced.

**Implementation evidence**

Agreement tests preserve candidate agreement among independent streams;
projection/replay code has versioned snapshots and event ids.

**Expected recovery**

Eventually, agreement evolution could preserve how candidate agreements appear,
change, or disappear across versions/snapshots.

**Confidence**

Medium-low.

**Why not yet**

The repository has stronger evidence for static candidate agreement than for
agreement-history ownership.

---

### 12. Grammar Evolution

**Summary**

Grammar Observation is already substantially recovered as relation-shape
observation. Evolution of grammar forms is not yet independently proven.

**Implementation evidence**

Documentation structure and grammar audits identify relation shapes, but current
tests emphasize narrow admission/rejection rather than historical grammar change.

**Expected recovery**

A future grammar-evolution owner could preserve when relation-shape forms are
added, deprecated, or remain unsupported.

**Confidence**

Low-medium.

**Why not yet**

Recovering evolution now would mostly extrapolate from static grammar evidence.

---

### 13. Cross-Substrate Observation

**Summary**

Cross-substrate agreement is ready; broader cross-substrate observation is not.

**Implementation evidence**

Documentation relation records, repository artifact facts, and relationship
facts independently observe different substrates.

**Expected recovery**

A future owner might coordinate acquisition of observations across substrates.

**Confidence**

Medium-low.

**Why not yet**

Agreement between existing streams is bounded. Owning observation across all
substrates would imply acquisition/traversal responsibilities not yet recovered.

---

### 14. Documentation Drift Observation

**Summary**

Documentation drift is plausible after documentation ↔ code agreement is
recovered, but it currently lacks a stable expected-correspondence baseline.

**Implementation evidence**

Documentation structure, repository artifact observation, relationship
observation, and cross-substrate audits expose possible match/mismatch evidence.

**Expected recovery**

Read-only candidate documentation/implementation mismatch records with
provenance and uncertainty.

**Confidence**

Medium.

**Why not yet**

Drift requires an agreement baseline or explicit expected correspondence. Recover
agreement first.

---

### 15. Implementation Drift Observation

**Summary**

Implementation drift is visible in diagnostic shape audit, diagnostic inventory,
architecture conformance, and surface-specific tests, but the general drift owner
is not yet bounded.

**Implementation evidence**

Diagnostic shape audit compares expected diagnostic shapes to actual output;
architecture/component audits and tests check conformance-like behavior.

**Expected recovery**

Read-only mismatch observations between expected implementation surfaces and
currently observed implementation artifacts.

**Confidence**

Medium.

**Why not yet**

Surface-specific checks are real. Repository-wide drift observation could become
too broad unless a narrow first domain is selected.

---

### 16. Architectural Consistency Observation

**Summary**

Architectural consistency pressure is visible but high-risk because it can easily
become architectural truth enforcement rather than observation.

**Implementation evidence**

Architecture conformance audits, invariant tests, diagnostic shape audit,
relationship observation, and grammar visibility all observe consistency-like
conditions.

**Expected recovery**

Candidate consistency/inconsistency records between already-authoritative
implementation surfaces.

**Confidence**

Low-medium.

**Why not yet**

The authority boundary is not yet safe. Recover agreement, evidence contracts,
and drift observation first.

---

### 17. Coverage Observation

**Summary**

Coverage-like behavior exists in classification, observation, capability, and
diagnostic inventories. A general Coverage Observation owner is plausible but
currently too broad.

**Implementation evidence**

Classification coverage, observation inventory, capability inventory, diagnostic
inventory, and responsibility-family audits all compute inventory/gap-like
surfaces.

**Expected recovery**

Read-only coverage records over existing surfaces, inputs, and tests.

**Confidence**

Medium.

**Why not yet**

Coverage must remain observation, not enforcement or priority. A first domain is
needed.

---

### 18. Operational Artifact Specialization

**Summary**

Operational artifacts exist in diagnostics, handoff plans, snapshots, and CLI
outputs, but specialization may already be local to those surfaces.

**Implementation evidence**

Diagnostic inventory/shape audit, snapshot artifact tests, handoff plans, and
operational responsibility slices preserve operational boundaries.

**Expected recovery**

A future characterization could distinguish operational artifacts from inquiry,
answer, evidence, and projection artifacts.

**Confidence**

Low-medium.

**Why not yet**

Current evidence supports local operational boundaries more than a distinct
architectural family.

---

## Behavior Work (ownership already recovered)

These areas have recovered ownership boundaries sufficient to enable behavior
work. Additional ownership slices should not be started unless new implementation
evidence exposes compressed responsibility.

### Observation Chain

**Summary**

Structure Observation, Relationship Observation, Observation Agreement, and
Grammar Observation collectively recovered the observation chain from raw
substrate evidence to candidate agreement and relation-shape visibility.

**Implementation evidence**

Completed structure, relationship, grammar, and agreement slices/audits identify
narrow observers, provenance preservation, and non-promotion boundaries.

**Expected recovery**

No new ownership recovery by default. Behavior work may add specific observers,
records, tests, or compatibility handoffs within already recovered boundaries.

**Confidence**

High.

**Why now / why not**

Further ownership recovery would likely rename known boundaries unless a new
substrate or compressed behavior appears.

---

### Answer Composition

**Summary**

Answer Composition has enough recovered ownership around composing supported
answers from selected reasoning/evidence/artifacts while leaving rendering and
truth ownership elsewhere.

**Implementation evidence**

Answer composition slices and audits repeatedly separate answer construction,
support context, compatibility objects, and presentation rendering.

**Expected recovery**

Behavior work can improve supported answer shapes or tests. Do not add more
ownership slices without new evidence.

**Confidence**

High.

**Why now / why not**

Additional ownership recovery would likely become vocabulary-first because the
main composition boundary is already implementation-backed.

---

### Inquiry Lineage

**Summary**

Inquiry Lineage has recovered boundaries around selection, derivation,
reference, unsupported/open outcomes, and lineage explanation separate from final
answers.

**Implementation evidence**

Inquiry lineage slices and family vocabulary audits preserve lineage material as
separate from result-like payloads and presentation.

**Expected recovery**

Behavior work can add lineage capture for new surfaces. Avoid another general
ownership slice unless a new compressed lineage owner appears.

**Confidence**

High.

**Why now / why not**

The repository has a mature lineage grammar. More abstract ownership work would
mostly restate it.

---

### Pre-Optimization Replay Ownership

**Summary**

Incremental replay recovery established that affected-scope evidence can be
observed while execution remains full event replay and full projection
finalization.

**Implementation evidence**

Incremental state replay slices and `seed_runtime.state` preserve descriptive
affected projection recovery without altering scheduling, dirty marking, cache
invalidation, or replay optimization.

**Expected recovery**

Behavior work may later optimize replay, but ownership recovery for the
pre-optimization boundary is complete.

**Confidence**

High.

**Why now / why not**

Further ownership recovery here would confuse behavior changes with already
recovered non-optimization boundaries.

---

### Structure Observation

**Summary**

Structure Observation is sufficiently recovered as bounded observation of
implementation/documentation structure with provenance and no architectural truth
promotion.

**Implementation evidence**

Structure observation slices, substrate responsibility audit, repository artifact
observation tests, and documentation structure tests all preserve narrow
observed structures.

**Expected recovery**

Behavior work may add new structures or substrate adapters. Do not start another
general Structure Observation ownership slice without new evidence.

**Confidence**

High.

**Why now / why not**

The boundary is already concrete. More ownership recovery would likely promote
presentation vocabulary or duplicate existing observers.

---

### Execution Visibility

**Summary**

Execution Visibility has recovered the boundary around exposing execution phases,
status, and diagnostic-compatible visibility without owning execution itself.

**Implementation evidence**

Execution visibility slices, projection/replay status phases, diagnostic
inventory, and diagnostic shape audit show recurring visibility contracts.

**Expected recovery**

Behavior work can add new visible phases only with diagnostic inventory and
shape-audit updates when exposed.

**Confidence**

High.

**Why now / why not**

Ownership is clear. New work should be surface-specific behavior, not another
visibility recovery family.

---

### Operational Responsibility

**Summary**

Operational Responsibility has recovered registered operation recommendation,
selection, validation, authorization, execution, recording, and post-execution
extraction boundaries.

**Implementation evidence**

Operational responsibility slices, recommendation/ranker tests, operation
contract surfaces, and handoff boundaries preserve the operational chain.

**Expected recovery**

Behavior work can add operations or improve validation within existing owners.

**Confidence**

High.

**Why now / why not**

Another ownership slice should wait for new compressed operational behavior;
provider/capability handoff candidates should not duplicate completed ownership.

---

## Do Not Pursue Yet

### Presentation Ownership Recovery

**Summary**

Presentation behavior exists, but the repository explicitly warns that
presentation vocabulary is not automatically knowledge.

**Implementation evidence**

Answer Composition already separates composition from rendering in several
surfaces; AGENTS instructions require implementation evidence before promoting
presentation labels such as continuation, current work position, source
navigation, active edge, storage topology, state build, or projection cache.

**Expected recovery**

A future presentation owner could format already-composed compatibility objects.

**Confidence**

Medium-low.

**Why not**

Pursuing this now risks promoting presentation vocabulary. Wait for stronger
implementation evidence that formatting ownership is compressed enough to matter.

---

### Read-Model Architecture Redesign

**Summary**

Read-model ownership recovery is ready; read-model redesign is not.

**Implementation evidence**

Existing read views and projection snapshots already work and are tested.

**Expected recovery**

No redesign. Preserve current read APIs while recovering ownership if pursued.

**Confidence**

High rejection.

**Why not**

The candidate is ownership clarification, not a new state/read architecture.

---

### Global Evidence/Provenance Schema Normalization

**Summary**

Evidence Contract recovery is plausible; repository-wide schema normalization is
not yet earned.

**Implementation evidence**

Evidence fields recur, but they are domain-specific and compatibility-sensitive.

**Expected recovery**

No global schema rewrite.

**Confidence**

High rejection.

**Why not**

Would create compatibility risk and new architecture beyond current evidence.

---

### Automatic Architectural Roadmap or Recovery Engine

**Summary**

This document is a frontier inventory, not a planning engine.

**Implementation evidence**

Recoverability audits preserve candidates, confidence, and boundaries, but do not
commit implementation order.

**Expected recovery**

None now.

**Confidence**

High rejection.

**Why not**

The task explicitly rejects roadmap/planning behavior, and implementation does
not justify a runtime recovery engine.

---

### LLM-Based Architecture Inference

**Summary**

Repository recovery depends on deterministic implementation evidence, not model
interpretation.

**Implementation evidence**

Completed slices consistently prefer code, tests, records, and diagnostics over
semantic speculation.

**Expected recovery**

None.

**Confidence**

High rejection.

**Why not**

This would violate repository authority and introduce non-deterministic
architecture claims.

---

### New Ontology for Family / Artifact / Presentation Terms

**Summary**

Family, artifact, and presentation terms recur, but broad ontology work is not
implementation-backed enough.

**Implementation evidence**

Some terms are classification labels or audit organization rather than preserved
runtime knowledge.

**Expected recovery**

None until implementation requires it.

**Confidence**

High rejection for now.

**Why not**

Would be vocabulary-first rather than implementation-first.

---

## Completed Areas That Should Not Receive More Ownership Slices Without New Evidence

The following families appear sufficiently recovered:

1. **Observation chain** — narrow observers, provenance, and non-promotion
   boundaries are established. More ownership recovery would likely restate
   existing structure/relationship/grammar/agreement roles.
2. **Answer Composition** — composition, support context, compatibility handoff,
   and rendering separation are already implementation-backed.
3. **Inquiry Lineage** — selection, derivation, reference, unsupported/open
   outcomes, and lineage explanation are mature enough for behavior work.
4. **Pre-optimization replay ownership** — affected-scope evidence is preserved
   while full replay/finalization remains the execution path.
5. **Structure Observation** — bounded substrate observation is concrete and
   tested.
6. **Execution Visibility** — visibility owns execution/status exposure, not
   execution behavior.
7. **Operational Responsibility** — operation recommendation through recording is
   sufficiently recovered; adjacent provider/capability candidates must avoid
   duplicating it.

Further ownership recovery in these areas should require new implementation
evidence: a new compressed owner, repeated duplicated behavior, a compatibility
handoff not already covered, or a tested surface that existing boundaries cannot
explain.

---

## Current Architectural Frontier

If repository development paused today, the architectural work that has already
earned the right to exist is the implementation-backed recovery layer around:

- bounded observation of structure, relationships, grammar shapes, and candidate
  agreement;
- answer composition and inquiry lineage as separate from presentation and truth;
- execution visibility and operational responsibility as separate from execution
  ownership and provider acquisition;
- pre-optimization replay visibility that preserves affected-scope evidence
  without changing replay behavior;
- read-only diagnostics that must remain visible through diagnostic inventory and
  diagnostic shape audit when exposed.

The strongest remaining ownership recoveries are:

1. Projection Influence Lineage;
2. Read-Model Ownership Recovery;
3. Documentation ↔ Code Agreement Observation;
4. Evidence Contract Family;
5. QuestionFamily Admission Characterization.

These candidates are ready because implementation already shows behavior,
compressed ownership, compatibility-preserving patterns, and bounded recovery
surfaces.

Work that still requires additional implementation evidence includes Family
Recovery, Artifact Composition, Artifact Kind, Provider Contract, Capability
Handoff, Observation Agreement Evolution, Grammar Evolution, Cross-Substrate
Observation, Documentation Drift, Implementation Drift, Architectural
Consistency, Coverage Observation, and Operational Artifact Specialization. These
may become real recoveries, but they should wait for narrower evidence or a
specific compressed implementation owner.

Work that should intentionally remain undiscovered for now includes presentation
vocabulary promotion, read-model redesign, global evidence schema normalization,
automatic roadmap generation, LLM-based architectural inference, and new ontology
for recurring labels. Those would be vocabulary-first or architecture-first
unless future implementation naturally exposes them.

The frontier is therefore:

```text
Recover the next ownership boundary only where current implementation
already behaves as if that owner exists.

Do behavior work where ownership is already recovered.

Leave vocabulary, ontology, redesign, and future-planning claims
undiscovered until repository behavior forces them into view.
```
