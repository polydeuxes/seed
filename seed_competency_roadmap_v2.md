# Seed Competency Roadmap v2 for Repository-Neutral Review

## 1. Executive summary

This v2 roadmap preserves `seed_competency_roadmap.md` as prior work and revises only the competency sequence. The revision is narrower and more evidence-first: Seed should not begin from architectural nouns, ownership labels, or review ambitions. It should acquire bounded competencies in the order required to ask an evidence-bearing question, find authority-bearing evidence, interpret what that evidence can and cannot support, recover bounded work only where implementation evidence permits, evaluate responsibility claims, and compose a bounded review answer.

The implementation-backed sequence is:

```text
Target Orientation
  -> Evidence Visibility
  -> Evidence Interpretation
  -> Inquiry Navigation
  -> Bounded Work Recovery
  -> Responsibility Evaluation
  -> Bounded Answer Composition
  -> Repository-Neutral Review
```

The candidate sequence is accepted with three important refinements:

1. **Evidence Interpretation replaces Authority Interpretation.** Authority is real, but current implementation evidence shows a broader discipline: evidence must be interpreted by provenance, visibility, compatibility, grammar/non-promotion boundary, fact-support shape, diagnostic/run scope, event-ledger authority, and mutation authority. Authority is one interpreted dimension, not the whole competency.
2. **Inquiry Navigation is inserted before Bounded Work Recovery.** Current inquiry evidence does not support planner behavior, but it does support a bounded ability to choose the next evidence-bearing question or authority-bearing surface and to stop when no implemented surface can answer.
3. **Bounded Work Recovery replaces Bounded Responsibility Understanding.** The safer implementation-backed order is work first, responsibility second. Seed should identify bounded performed work from evidence, then recover responsibility only when the work has stable owner, inputs, outputs, exclusions, handoffs, and tests. This is not ownership recovery by default.

The final capability, **Repository-Neutral Review**, remains an acquisition target, not a current implementation claim. Existing evidence supports the discipline, not an autonomous reviewer, planner, repository importer, semantic review engine, universal representation pipeline, universal grammar abstraction, generalized explanation engine, or code-modification agent.

## 2. Relationship to `seed_competency_roadmap.md`

The v1 roadmap remains preserved prior work. It established a conservative competency curriculum:

```text
Target Orientation
  -> Evidence Visibility
  -> Surface/Question Routing
  -> Authority Interpretation
  -> Bounded Responsibility Understanding
  -> Responsibility Evaluation
  -> Bounded Answer Explanation
  -> Repository-Neutral Review Readiness
```

V2 keeps v1's core discipline: explicit targets precede evidence, visibility precedes interpretation, interpretation precedes responsibility claims, evaluation precedes answer composition, and repository-neutral review is not yet implemented as an autonomous capability.

V2 changes the sequence where recent investigations sharpened the boundary:

| V1 element | V2 decision | Why |
| --- | --- | --- |
| Surface/Question Routing | Folded into **Inquiry Navigation** | Exact dispatch is necessary evidence, but the broader competency is bounded navigation across exact ask dispatch, inquiry orientation, source navigation, and stop conditions. |
| Authority Interpretation | Renamed to **Evidence Interpretation** | Authority is too narrow; implementation evidence also requires provenance, visibility, compatibility, grammar/non-promotion boundary, observation/evidence/fact shape, fact support, diagnostic scope, and ledger/mutation distinctions. |
| Bounded Responsibility Understanding | Renamed to **Bounded Work Recovery** | The implementation-backed entry is bounded work performed by code/tests/surfaces, not a responsibility noun. Responsibility is recovered only after work evidence is stable. |
| Bounded Answer Explanation | Renamed to **Bounded Answer Composition** | The answer-family evidence is local composition from support, boundaries, limitations, and unknowns; it is not a generalized explanation engine. |
| Repository-Neutral Review Readiness | Renamed to **Repository-Neutral Review** | The competency target is review behavior, but the readiness assessment remains: current implementation is not yet an end-to-end neutral reviewer. |

V2 does not overwrite v1 and does not introduce implementation changes, ownership recovery, new architectural abstractions, or a proposal for repository import automation.

## 3. Revised dependency graph

```text
C1 Target Orientation
  answers: What exact review target or bounded question has been supplied?
  |
  v
C2 Evidence Visibility
  answers: What implementation evidence is observable, read-only, and in scope?
  |
  v
C3 Evidence Interpretation
  answers: What does the visible evidence mean within provenance, shape, authority, compatibility, and non-promotion boundaries?
  |
  v
C4 Inquiry Navigation
  answers: What is the next evidence-bearing question or authority-bearing surface, and when must inquiry stop?
  |
  v
C5 Bounded Work Recovery
  answers: What bounded work is actually performed by implementation evidence before naming responsibility?
  |
  v
C6 Responsibility Evaluation
  answers: Is a responsibility claim supported, contradicted, incomplete, or insufficiently visible?
  |
  v
C7 Bounded Answer Composition
  answers: What review answer can be composed from evaluated evidence, support, boundary, limitations, and unknowns?
  |
  v
C8 Repository-Neutral Review
  answers: Can Seed perform disciplined, evidence-first review of an unfamiliar repository without overclaiming?
```

The order is intentionally conservative:

- **Target Orientation before Evidence Visibility** prevents Seed from observing without a bounded review target.
- **Evidence Visibility before Evidence Interpretation** prevents invisible evidence and presentation vocabulary from becoming knowledge.
- **Evidence Interpretation before Inquiry Navigation** ensures the next question is chosen from interpreted evidence boundaries, not from planner intent.
- **Inquiry Navigation before Bounded Work Recovery** prevents Seed from naming work before it knows which evidence-bearing surface can answer the next bounded question.
- **Bounded Work Recovery before Responsibility Evaluation** prevents responsibility nouns from driving the review.
- **Responsibility Evaluation before Bounded Answer Composition** prevents answers from substituting for evidence.
- **Bounded Answer Composition before Repository-Neutral Review** keeps review output bounded, cited, and refusal-capable.

## 4. Competency-by-competency analysis

### C1. Target Orientation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Target Orientation |
| Bounded question it answers | What exact repository, review target, concern, question family, subject, query, target, domain, or note has the operator supplied? |
| Bounded work performed | Preserve explicit operator-supplied identity; distinguish repository path, question family, surface arguments, source-navigation query, inquiry note, reasoning subject/domain, and selection target; reject conversion of vague prose into facts, goals, requirements, ownership, commands, or next actions. |
| Prerequisite competencies | None. This is the entry competency. |
| Implementation evidence already supporting it | Exact bounded ask requires `ask --question-family <exact-question-family>` and exact surface-argument counts; inquiry identity investigations show different identity shapes for `question_family`, `subject`, `target`, `domain`, `query`, and `note`; Inquiry Orientation preserves notes as prose rather than truth. |
| Implementation evidence still missing | No general program-purpose extractor; no stable review-target schema for arbitrary repositories; no implementation-backed conversion from arbitrary prose into intended responsibilities; no automated subject discovery for neutral review. |
| Authority intentionally excluded | Operator-intent inference; semantic free-text routing; unsupported identity recovery; automatic ownership or responsibility recovery; treating note text as facts, goals, requirements, or commands. |
| Proceed criteria | The review has an explicit repository path plus a bounded target/question/concern, or an exact implemented question family with required arguments. |
| Stop criteria | The only input is vague intent, architectural vocabulary, or a request that requires Seed to infer a target responsibility without implementation-backed identity. |
| Implementation readiness | **Partially ready.** Strong for explicit identities inside Seed inquiry surfaces; not ready for autonomous orientation over unfamiliar repositories. |

### C2. Evidence Visibility

| Field | Roadmap finding |
| --- | --- |
| Competency name | Evidence Visibility |
| Bounded question it answers | What implementation evidence is observable, in scope, provenance-preserved, and read-only; what evidence is invisible or unavailable? |
| Bounded work performed | Enumerate or collect visible repository metadata, source relationships, diagnostic surfaces, inventory rows, projected state, fact support, explanation/read-model material, and existing investigation evidence without mutating repository or cluster truth. Preserve visibility gaps as gaps. |
| Prerequisite competencies | C1 Target Orientation. |
| Implementation evidence already supporting it | Repository observation is read-only and records repository path, VCS, head, branch, dirty state, status availability, and non-mutation flags; source observation extracts Python import/definition relationships from configured roots; diagnostic inventory and shape-audit surfaces preserve record, ledger, read-only, and mutation boundaries; documentation structure observation preserves structural visibility while refusing prose interpretation and responsibility recovery. |
| Implementation evidence still missing | Language-neutral source observation; target build/test/runtime evidence collection under explicit authority; documentation-claim observation beyond structural metrics; evidence adapters for non-Python repositories; end-to-end non-Seed fixture review evidence. |
| Authority intentionally excluded | Repository import automation; file mutation; target tooling execution without operational authority; event-ledger writes unless the surface declares them; cluster mutation; promotion of diagnostic-only output into target truth. |
| Proceed criteria | Relevant evidence is visible, scoped, and carries provenance plus read/record/ledger/mutation boundaries. |
| Stop criteria | Required evidence is invisible, unavailable, unsupported by current adapters, or would require mutation/execution outside implemented authority. |
| Implementation readiness | **Ready for narrow read-only evidence; incomplete for repository-neutral review.** |

### C3. Evidence Interpretation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Evidence Interpretation |
| Bounded question it answers | What does visible evidence authorize, exclude, support, contradict, or leave unknown when interpreted by provenance, visibility, compatibility, grammar, evidence shape, diagnostic scope, fact support, and mutation boundary? |
| Bounded work performed | Interpret evidence without semantic free-text reasoning: distinguish observation, evidence, projected fact, fact support, explanation, diagnostic output, recordable run output, event-ledger authority, cluster mutation, compatibility evidence, grammar observation, presentation vocabulary, and repository knowledge. |
| Prerequisite competencies | C2 Evidence Visibility. |
| Implementation evidence already supporting it | Promotion investigations distinguish observation from fact support, candidate from verification, diagnostic recording from cluster mutation, and presentation vocabulary from reachable knowledge; Grammar Observation and Observation Agreement explicitly refuse semantic interpretation, architectural truth, responsibility recovery, family recovery, event writes, ledger writes, and mutation; `ExplanationBuilder` consumes projected fact support and conflicts rather than creating facts; diagnostic inventory records record scope, event-ledger writes, mutation behavior, and read-only status. |
| Implementation evidence still missing | A neutral authority/provenance schema for arbitrary target repositories; target-specific compatibility authority recovery; review-specific evidence-shape classification across languages and artifacts; tests proving interpretation refusals on non-Seed fixture evidence. |
| Authority intentionally excluded | Semantic free-text reasoning; treating README prose, labels, or presentation terms as knowledge without evidence; treating diagnostic output as cluster truth; treating grammar observations as responsibility recovery; treating read-only observation as permission to modify code. |
| Proceed criteria | Each candidate conclusion names the evidence type, provenance, support shape, authority boundary, excluded authority, and visible counterexamples or unknowns. |
| Stop criteria | The next conclusion would require semantic interpretation, hidden intent, unsupported promotion, mutation, or authority beyond the evidence source. |
| Implementation readiness | **Strong for Seed surfaces; partial for unfamiliar repositories.** |

**Required distinction:** Evidence Interpretation is not semantic free-text reasoning. It is bounded interpretation of implementation evidence shapes and authority boundaries.

### C4. Inquiry Navigation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Inquiry Navigation |
| Bounded question it answers | Given interpreted evidence, what is the next evidence-bearing question or authority-bearing surface, and when is there no supported next step? |
| Bounded work performed | Navigate only among bounded implemented surfaces: exact question-family dispatch, inquiry orientation, source navigation, reasoning/selection path surfaces, diagnostic inventory/shape-audit surfaces, fact-support/explanation surfaces, and existing investigations. Determine the next question needed to expose evidence, not a plan of action. Stop when no implemented surface can answer. |
| Prerequisite competencies | C1 Target Orientation, C2 Evidence Visibility, and C3 Evidence Interpretation. |
| Implementation evidence already supporting it | Bounded ask dispatch validates exact registered question families, rejects unknown or non-dispatchable families, enforces required argument counts, and forwards explicit values unchanged; Inquiry Orientation deterministically finds lexical overlap between preserved notes and projected material while refusing intent, planning, routing, ownership, and next-move authority; Source Navigation performs syntactic lookup over projected source fact supports and carries non-claims against semantic relevance; question-surface inventory exposes authority boundaries and diagnostic relationships. |
| Implementation evidence still missing | No implemented planner; no natural-language routing; no repository-neutral inquiry controller; no automated next-question engine; no target-repository question inventory; no proof that Seed can navigate an unfamiliar repository's evidence surfaces without human-bounded questions. |
| Authority intentionally excluded | Planner behavior; autonomous review; semantic question understanding; creation of new question families; direct dispatch from recovered responsibilities; routing from grammar observations; recommendations about next safe moves. |
| Proceed criteria | A next bounded question maps to an implemented surface, exact dispatch row, syntactic source lookup, or existing evidence artifact, and its output can refine visibility or interpretation. |
| Stop criteria | The next step would require planning, unregistered routing, semantic paraphrase matching, a new abstraction, repository import automation, or unsupported responsibility recovery. |
| Implementation readiness | **Ready as bounded manual navigation across Seed surfaces; not ready as planner or repository-neutral autonomous navigation.** |

**Required distinction:** Inquiry Navigation is not planner behavior. It chooses a next evidence-bearing question or stops; it does not decide work to perform, generate implementation plans, or authorize actions.

### C5. Bounded Work Recovery

| Field | Roadmap finding |
| --- | --- |
| Competency name | Bounded Work Recovery |
| Bounded question it answers | What bounded work is actually performed by code, tests, records, reports, diagnostics, or handoffs before any responsibility noun is accepted? |
| Bounded work performed | Recover implementation-backed work units from evidence: consumed inputs, produced outputs, validation, compatibility preservation, handoffs, exclusions, negative authority, tests, and counterexamples. Name responsibility only after work boundaries are stable. |
| Prerequisite competencies | C4 Inquiry Navigation. |
| Implementation evidence already supporting it | Slice investigations repeatedly recover exactly one implementation-local boundary from observed work and stop; responsibility audits recover work from code paths, record shapes, tests, and handoffs; state-build cache-debug investigations distinguish evidence collection, visibility payload, projection diagnostic payload, timing, orchestration, and presentation; source/documentation/grammar observations explicitly refuse responsibility recovery where only structural observations exist. |
| Implementation evidence still missing | General arbitrary-repository bounded-work recovery; target-specific intended-work authority; semantic matching between repository vocabulary and implemented duties; responsibility evidence model for non-Seed projects; tests proving work-first recovery against a non-Seed fixture. |
| Authority intentionally excluded | Ownership recovery by default; unsupported responsibility recovery; treating architectural nouns as work; treating Seed-specific responsibility families as universal; recovering identity or responsibility from grammar/structure observations alone. |
| Proceed criteria | A candidate work unit has evidence-backed inputs, outputs, local owner or locus, boundary, excluded authority, compatibility expectations, and tests or observed behavior. |
| Stop criteria | The candidate begins from a noun, label, README claim, presentation vocabulary, grammar shape, or Seed family name without implementation evidence of performed work. |
| Implementation readiness | **Methodologically ready; not automated or repository-neutral as machinery.** |

**Required distinction:** Bounded Work Recovery is not ownership recovery by default. It may support later responsibility evaluation, but only after performed work is evidenced.

### C6. Responsibility Evaluation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Responsibility Evaluation |
| Bounded question it answers | Is a responsibility claim supported, contradicted, incomplete, compressed into another owner, or insufficiently visible? |
| Bounded work performed | Compare recovered bounded work to a responsibility claim; evaluate sufficiency, counterexamples, compatibility, handoff preservation, negative ownership, diagnostic visibility, missing evidence, confidence, proceed criteria, and stop criteria. |
| Prerequisite competencies | C5 Bounded Work Recovery. |
| Implementation evidence already supporting it | Responsibility and family audits repeatedly distinguish supported work from plausible but unimplemented abstractions; slice evaluation readiness identifies negative ownership clauses and missing evaluator implementation; question-family boundary audits reject direct ResponsibilityRecovery-to-Inquiry dispatch; repository-neutral methodology distinguishes supported, contradicted, and insufficient evidence. |
| Implementation evidence still missing | No implemented slice-evaluation command, registry, inquiry surface, or automated evaluator; no generalized evaluator over arbitrary target evidence; no test-backed review result schema; no target-specific compatibility-break evaluator. |
| Authority intentionally excluded | Autonomous review judgment; broad redesign; implementation planning; declaring mismatch from absent visibility alone; upgrading compressed work into a first-class responsibility without evidence; treating target-specific responsibility families as universal. |
| Proceed criteria | Evidence supports a clear classification with counterexamples, missing evidence, authority boundaries, and confidence. |
| Stop criteria | Evaluation would require hidden intent, semantic reasoning, unsupported target tooling execution, or ownership recovery beyond bounded work evidence. |
| Implementation readiness | **Ready as investigation discipline; not yet an implemented review evaluator.** |

### C7. Bounded Answer Composition

| Field | Roadmap finding |
| --- | --- |
| Competency name | Bounded Answer Composition |
| Bounded question it answers | What answer can Seed compose from evaluated evidence while preserving support, boundary, limitations, unknowns, and refusal conditions? |
| Bounded work performed | Compose a review answer from evidence-backed material, reasoning, citations/support, boundaries, limitations, unknowns, confidence, proceed criteria, and stop criteria. Preserve ambiguity and insufficient evidence instead of filling gaps. |
| Prerequisite competencies | C6 Responsibility Evaluation. |
| Implementation evidence already supporting it | Answer Composition evidence separates answer material, reasoning, supporting evidence, boundary, and limitations; Operational Story and Inquiry Orientation produce read-only answer/view records; `ExplanationBuilder` explains current, ambiguous, or absent projected beliefs from fact support and conflicts; question-family explanation composes static inventory fields for presentation without creating families or authority. |
| Implementation evidence still missing | Repository-neutral answer object; review-specific result schema; citation model over target repositories; tests proving bounded refusal and insufficient-evidence answers over non-Seed evidence; composition across arbitrary evidence adapters. |
| Authority intentionally excluded | Generalized explanation engine; semantic free-text synthesis; creating facts from answer text; resolving ambiguity without evidence; producing implementation plans, ownership recovery, or code modifications. |
| Proceed criteria | The answer can cite or identify support, name authority boundaries, state limitations/unknowns, and preserve stop/proceed posture without inventing facts. |
| Stop criteria | The answer would require unsupported semantic synthesis, hidden facts, autonomous recommendations, target mutation, or a new explanation abstraction. |
| Implementation readiness | **Ready for Seed projected-state and bounded answer surfaces; partial for repository-neutral review.** |

### C8. Repository-Neutral Review

| Field | Roadmap finding |
| --- | --- |
| Competency name | Repository-Neutral Review |
| Bounded question it answers | Can Seed review an unfamiliar repository in a disciplined, evidence-first, repository-neutral way without overclaiming authority or modifying code? |
| Bounded work performed | Integrate explicit target orientation, evidence visibility, evidence interpretation, inquiry navigation, bounded work recovery, responsibility evaluation, and bounded answer composition into a review answer that can conclude supported, contradicted, insufficiently visible, out of scope, or stopped. |
| Prerequisite competencies | C1 through C7. |
| Implementation evidence already supporting it | Existing repository-neutral review investigations support the methodology; read-only repository and Python source observation provide narrow neutral evidence; diagnostic governance preserves visibility and mutation boundaries; responsibility and answer-family audits demonstrate Seed-specific examples of disciplined review. |
| Implementation evidence still missing | End-to-end repository-neutral review surface; non-Seed fixture tests; language/runtime-neutral evidence adapters or scoped adapter declarations; target-responsibility source intake; review result schema; diagnostic inventory and shape-audit coverage if exposed as a diagnostic/audit/probe/view/CLI surface; proof that review does not become a planner, importer, debugger, or code modifier. |
| Authority intentionally excluded | Autonomous debugging; code modification; planner behavior; repository import automation; semantic review engine; universal representation pipeline; universal grammar abstraction; generalized explanation engine; unsupported identity/responsibility/ownership recovery. |
| Proceed criteria | A non-Seed fixture can be reviewed from explicit target plus read-only evidence and target-specific authority sources, producing bounded supported/contradicted/insufficient/stopped answers with refusals preserved. |
| Stop criteria | Review requires missing competencies, unimplemented adapters, semantic reasoning, mutation, implementation planning, ownership recovery, or new architectural abstractions. |
| Implementation readiness | **Not ready as an implemented capability. Ready only as the ordered acquisition target.** |

**Required distinction:** Repository-Neutral Review is not autonomous debugging or code modification.

## 5. Changes from v1 and why

### 5.1 Authority Interpretation broadened to Evidence Interpretation

V1 correctly identified authority boundaries as central, but recent evidence shows authority is only one dimension of interpretation. Seed must also interpret:

- provenance and source locality;
- visibility versus invisibility;
- observation versus evidence versus projected fact;
- fact support and conflict shape;
- diagnostic inventory and shape-audit status;
- event-ledger writes versus cluster mutation;
- compatibility preservation;
- grammar and observation non-promotion boundaries;
- presentation vocabulary versus repository knowledge.

This change is implementation-backed by promotion, grammar-observation, diagnostic, representation-transition, fact-support, and explanation evidence. It remains tentative only in the repository-neutral setting because arbitrary target repositories do not yet have a general interpretation schema.

### 5.2 Inquiry Navigation inserted before Bounded Work Recovery

V1 had Surface/Question Routing before Authority Interpretation. V2 separates the exact-routing evidence from the broader competency. Exact dispatch remains necessary, but recent inquiry investigations show several bounded navigation surfaces:

- exact `ask --question-family` dispatch;
- question-surface inventory;
- Inquiry Orientation lexical related-material matching;
- Source Navigation syntactic lookup over projected source facts;
- Reasoning/Selection Path parameterized surfaces;
- diagnostic inventory and shape-audit surfaces.

This supports a competency that determines the next evidence-bearing question or authority-bearing surface. It does **not** support planner behavior, autonomous next-action generation, semantic routing, or review automation.

### 5.3 Bounded Responsibility Understanding changed to Bounded Work Recovery

V1's wording still risked starting from responsibility nouns. V2 starts from performed work. This change is implementation-backed by slice investigations that recover exactly one implementation-local boundary, by audits that reject grammar/structure observation as responsibility recovery, and by responsibility-to-inquiry audits that reject direct dispatch from recovered responsibilities.

The change remains tentative as an automated competency: Seed can apply the discipline in investigations, but it does not yet have a general arbitrary-repository work-recovery engine.

### 5.4 Bounded Answer Explanation changed to Bounded Answer Composition

V1's “Explanation” wording could overstate a generalized explanation engine. V2 uses “Composition” because current answer surfaces compose bounded outputs from already interpreted and evaluated evidence. `ExplanationBuilder` is strong evidence for projected-state explanation, but repository-neutral review needs a broader answer composition discipline rather than a universal explanation abstraction.

### 5.5 Repository-Neutral Review Readiness shortened to Repository-Neutral Review

The final competency is still not a current implementation claim. The rename clarifies the target behavior while preserving readiness limits. Seed can currently describe the acquisition path; it cannot yet claim an implemented repository-neutral review surface.

## 6. Existing implementation support

### Strong support

1. **Exact inquiry/ask dispatch.** Bounded ask uses exact question-family identity, exact argument counts, static dispatch maps, and refusal of unknown or unsupported families.
2. **Inquiry orientation.** Inquiry notes are preserved as operator prose and matched only by deterministic lexical overlap against projected material, with explicit refusal of intent, planning, ownership, commands, requirements, and next-move authority.
3. **Source navigation.** Source-navigation query identity is syntactic lookup over projected source fact supports, not semantic relevance or responsibility inference.
4. **Diagnostic and visibility surfaces.** Diagnostic inventory and shape-audit governance expose read-only, recordable, event-ledger, mutation, and shape-spec boundaries.
5. **Observation/evidence/fact boundaries.** State projection, promotion investigations, grammar observation, observation agreement, fact support, and explanation surfaces preserve non-promotion boundaries.
6. **Fact support and explanation.** `ExplanationBuilder` consumes projected fact support, facts, conflicts, and evidence ids to produce current/ambiguous/no-current-belief explanations without creating truth.
7. **Responsibility recovery discipline inside Seed.** Existing slices and audits recover implementation-local work boundaries from code/tests/records and stop at unsupported ownership claims.
8. **Representation discipline.** The implementation has multiple concrete representations and transitions, but rejects one universal `Representation` pipeline.
9. **Bounded-question discipline.** Existing answer surfaces show a recurring pattern: bounded question -> bounded work -> bounded answer -> next responsibility, while refusing broader adjacent questions.

### Medium support

1. **Responsibility evaluation readiness.** The discipline is visible in reports and slices, but there is no implemented generic evaluator.
2. **Slice evaluation readiness.** Investigations identify what evaluation would require, but no slice-evaluation command, registry, inquiry surface, or automated evaluator exists.
3. **Repository-neutral methodology.** Prior investigations support evidence-first neutral review as a methodology, not as an implemented review engine.
4. **Python source observation.** Repository source evidence exists for Python import/definition relationships but is not language-neutral.

### Weak or absent support

1. **Autonomous review.** No implementation supports autonomous repository-neutral review.
2. **Planner behavior.** Inquiry surfaces do not plan or recommend next safe moves.
3. **Repository import automation.** Existing evidence observation is read-only and scoped; it does not import repositories as review subjects automatically.
4. **Semantic free-text reasoning.** Current surfaces rely on exact identifiers, syntactic matching, lexical overlap, and projected support rather than general semantic reasoning.
5. **Universal abstractions.** Universal representation, grammar, explanation, provider, artifact, question, or responsibility pipelines are repeatedly rejected by implementation evidence.

## 7. Missing implementation evidence

Before Seed can claim implemented repository-neutral review, it needs evidence in dependency order:

1. **Target Orientation evidence:** a review target model preserving repository path, bounded question/concern, supplied authority source, and excluded intent inference.
2. **Evidence Visibility evidence:** read-only evidence adapters broad enough for the target and tests proving no mutation, no unintended event-ledger writes, and scoped provenance.
3. **Evidence Interpretation evidence:** a review evidence-shape model distinguishing observation, evidence, fact, support, diagnostic output, compatibility evidence, authority, and unknowns across target repositories.
4. **Inquiry Navigation evidence:** a bounded next-question/surface selection mechanism that is not a planner, uses exact/implemented surfaces, and stops on unsupported questions.
5. **Bounded Work Recovery evidence:** work-first recovery over target evidence, including inputs, outputs, owner/locus, handoffs, exclusions, and counterexamples before responsibility naming.
6. **Responsibility Evaluation evidence:** a result shape and tests for supported, contradicted, incomplete, compressed, insufficient, and stopped classifications.
7. **Bounded Answer Composition evidence:** a repository-neutral answer object with support/citations, boundaries, limitations, confidence, unknowns, and refusal posture.
8. **Integration evidence:** non-Seed fixture review proving bounded success and bounded refusal without planner behavior, repository import automation, semantic free-text reasoning, ownership recovery, or code modification.
9. **Diagnostic governance evidence if exposed:** if any review surface becomes a diagnostic, audit, probe, view, operational CLI flag, or recordable output, diagnostic inventory and diagnostic shape-audit implementation specs and tests must cover it.

## 8. Recommended competency acquisition order

1. **Target Orientation** — learn to preserve explicit target identity and refuse hidden intent recovery.
2. **Evidence Visibility** — learn to expose read-only evidence and visibility gaps with provenance and mutation boundaries.
3. **Evidence Interpretation** — learn to interpret evidence shape, support, authority, compatibility, diagnostic scope, and non-promotion boundaries without semantic free-text reasoning.
4. **Inquiry Navigation** — learn to choose the next evidence-bearing question or authority-bearing surface, or stop, without becoming a planner.
5. **Bounded Work Recovery** — learn to recover bounded performed work from implementation evidence before accepting responsibility names.
6. **Responsibility Evaluation** — learn to classify claims against recovered work and counterexamples.
7. **Bounded Answer Composition** — learn to compose supported review answers with boundaries, limitations, unknowns, and explicit refusal.
8. **Repository-Neutral Review** — integrate the prior competencies against non-Seed repositories while preserving repository authority and non-mutation.

The recommended order differs from v1 primarily by moving from **authority-only interpretation** to **evidence interpretation**, inserting **inquiry navigation**, and changing **responsibility understanding** into **work-first recovery**.

## 9. Explicit stopping boundaries

Seed must stop rather than proceed when a review would require:

- autonomous review;
- planner behavior;
- autonomous debugging;
- code modification;
- repository import automation;
- semantic free-text reasoning as authority;
- generalized explanation engines;
- universal representation pipelines;
- universal grammar abstractions;
- universal provider/artifact/question abstractions;
- unsupported identity recovery;
- unsupported responsibility recovery;
- ownership recovery by default;
- treating Seed-specific responsibility families as universal;
- treating presentation vocabulary as repository knowledge;
- treating grammar observations as responsibility or family recovery;
- treating diagnostic findings as cluster truth;
- treating event-ledger writes as cluster mutation or read-only observation as mutation authority;
- mutating a target repository or executing target tooling without implemented operational authority;
- declaring failure where evidence is merely invisible;
- producing a backlog, implementation plan, migration plan, recovery plan, or abstraction proposal instead of a bounded review answer.

These stops are not optional safeguards; they are part of the competency sequence. A disciplined review must be able to answer “insufficient evidence” or “unsupported by current surfaces” without filling the gap.

## 10. Long-term competencies separated from current readiness

The following are plausible future competencies, but they are not current implementation readiness claims:

1. **Target-purpose recovery from classified authority sources.** Future work may recover intended purpose from tests, schemas, docs, examples, package metadata, or API contracts, but only with source authority classification and counterexample tests.
2. **Language-neutral structural evidence.** Future adapters may broaden source observation beyond Python, but each adapter should remain provider-local rather than implying universal grammar.
3. **Repository-neutral evidence-shape registry.** A future registry could classify target evidence types, support shapes, mutation boundaries, and compatibility authority, but it must not become a universal representation pipeline.
4. **Bounded inquiry navigator.** A future navigator could suggest the next implemented evidence-bearing question, but it must remain non-planning, non-autonomous, and refusal-capable.
5. **Work-first recovery fixture suite.** Future tests should prove bounded work recovery on non-Seed fixture repositories before responsibility naming.
6. **Review result schema.** A future schema could represent supported, contradicted, incomplete, compressed, insufficient, and stopped findings with support and boundaries.
7. **Cross-repository compatibility evidence.** Future review may evaluate compatibility expectations, but only when those expectations are recovered from target evidence rather than imposed from Seed.
8. **Recordable review diagnostics.** If review becomes recordable, findings should default to diagnostic-run scope and preserve `mutates_cluster=false` unless intentionally operational.

## 11. Open questions

1. What minimal target model is enough for repository-neutral review: repository path plus bounded question, repository path plus responsibility claim, or repository path plus authority-bearing artifact?
2. Which target artifacts can carry intended-responsibility authority: tests, schemas, public APIs, package metadata, examples, READMEs, issue templates, or only executable contracts?
3. How should Seed represent evidence that belongs to another authority rather than being simply supported or unsupported?
4. What non-Seed fixture repository would prove the full competency chain without creating a premature review engine?
5. How should a bounded inquiry navigator expose “next evidence-bearing question” while proving it is not planner behavior?
6. What is the smallest evidence-shape vocabulary that distinguishes observation, evidence, fact, support, diagnostic output, compatibility claim, and unknown without creating a universal representation abstraction?
7. How should review answers cite target repository files while preserving the difference between target evidence and Seed implementation evidence?
8. What tests would prove that lexical overlap, syntactic source navigation, and exact dispatch do not become semantic free-text reasoning?
9. What tests would prove that bounded work recovery does not become ownership recovery by default?
10. If a repository-neutral review surface becomes diagnostic or recordable, what inventory and shape-audit rows are required before it can count as visible?

## 12. Acceptance answer

If Seed were a new engineer, it would need to acquire these bounded competencies in order:

```text
Target Orientation
Evidence Visibility
Evidence Interpretation
Inquiry Navigation
Bounded Work Recovery
Responsibility Evaluation
Bounded Answer Composition
Repository-Neutral Review
```

What changed from v1:

- **Authority Interpretation** became **Evidence Interpretation** because implementation evidence supports a broader interpretation boundary than authority alone.
- **Inquiry Navigation** was inserted because exact dispatch, inquiry orientation, source navigation, and diagnostic/source surfaces show bounded next-question behavior without planner authority.
- **Bounded Responsibility Understanding** became **Bounded Work Recovery** because repository authority supports recovering performed work before accepting responsibility nouns.
- **Bounded Answer Explanation** became **Bounded Answer Composition** because current answer surfaces compose bounded outputs rather than implement a generalized explanation engine.

Which changes are implementation-backed:

- Exact inquiry/ask dispatch, question-surface inventory, Inquiry Orientation, Source Navigation, diagnostic visibility, observation/evidence/fact boundaries, fact support, explanation, grammar non-promotion, representation-transition discipline, slice investigations, responsibility boundary audits, and bounded-question investigations all support the revised sequence.

Which remain tentative:

- The sequence as a repository-neutral implemented capability remains tentative until Seed has non-Seed fixture tests, target evidence adapters, review result schemas, bounded inquiry navigation that is not planning, work-first recovery over target evidence, and diagnostic governance for any exposed review surface.
