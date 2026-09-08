# Seed Competency Roadmap for Repository-Neutral Review

## 1. Executive summary

Seed is not yet implementation-backed as an autonomous repository-neutral reviewer. It is, however, implementation-backed as a disciplined evidence-first review **curriculum**: it can acquire bounded competencies in an order that preserves repository authority, separates observation from mutation, and refuses unsupported architectural promotion.

The current frontier supports this progression:

```text
Orientation
  -> Evidence visibility
  -> Surface/question routing
  -> Authority interpretation
  -> Responsibility evaluation
  -> Bounded answer explanation
  -> Repository-neutral review readiness
```

This roadmap intentionally treats the expected areas (`Orientation`, `Visibility`, `Interpretation`, `Understanding`, `Evaluation`, `Explanation`) as candidate competencies, not architectural objects. Implementation evidence supports keeping most of them, but renaming and splitting them to avoid overclaiming:

| Candidate area | Roadmap decision | Reason |
| --- | --- | --- |
| Orientation | Keep as **Target Orientation** | Existing inquiry surfaces require explicit target identity and reject semantic intent recovery. |
| Visibility | Keep and narrow as **Evidence Visibility** | Repository and diagnostic surfaces expose read-only evidence, but do not create truth. |
| Interpretation | Keep and narrow as **Authority Interpretation** | Seed can interpret boundaries, shape, and negative authority; it cannot interpret arbitrary semantics. |
| Understanding | Rename to **Bounded Responsibility Understanding** | “Understanding” is too broad unless tied to implementation-backed responsibility evidence. |
| Evaluation | Keep as **Responsibility Evaluation** | Existing investigations repeatedly evaluate sufficiency, counterexamples, compatibility, and stopping. |
| Explanation | Keep and narrow as **Bounded Answer Explanation** | Explanation exists as deterministic composition from projected support and answer surfaces, not a generalized explanation engine. |

The final competency, **Repository-Neutral Review Readiness**, is not a new subsystem. It is the integrated ability to apply the prior competencies to an unfamiliar repository while refusing autonomous review, repository import automation, semantic free-text reasoning, universal representation, universal grammar, unsupported identity recovery, and unsupported responsibility recovery.

## 2. Current implementation frontier

The strongest current implementation frontier is methodological rather than a runnable general reviewer. Existing evidence says repository-neutral program review is supported as a bounded evidence-first human investigation shape, not as an implemented capability. That investigation explicitly distinguishes the supported methodology from autonomous debugging, repository import, code generation, implementation planning, and review-engine behavior.

Implementation-backed support already exists for:

- **Read-only repository state observation.** `GitRepositoryObservationProvider` observes arbitrary git-backed paths and records repository path, VCS, head commit, branch, dirty state, status availability, and non-mutation flags.
- **Read-only Python source relationship observation.** `RepositorySourceObservationSource` scans configured include roots, extracts Python import and definition relationship facts, and emits observations with source-path evidence and repository-root metadata.
- **Bounded question-family identity and dispatch.** `question_surface_inventory.py` maps exact question families to answer surfaces, required parameters, bounded dispatch statuses, diagnostic relationships, and authority boundaries.
- **Diagnostic visibility boundaries.** Diagnostic inventory rows explicitly record whether surfaces support recording, write the event ledger, mutate cluster state, and are read-only or operational.
- **Deterministic projected-state explanations.** `ExplanationBuilder` explains current, ambiguous, or absent projected beliefs from `State` fact support; it does not invent missing facts or resolve unsupported semantics.
- **Completed recovered responsibility families.** Existing family audits classify Operational Responsibility, Execution Visibility, Observation-Derived Capability, Answer Composition, and Inquiry Lineage as implementation-backed families for Seed-specific recovered chains.

Current implementation does **not** support:

- autonomous repository review;
- general program-purpose extraction;
- arbitrary intended-responsibility recovery;
- semantic free-text reasoning over unfamiliar repositories;
- repository import automation;
- universal Representation, Grammar, Artifact, provider pipeline, Question abstraction, or explanation subsystem;
- using Seed-specific responsibility families as another repository's architecture.

## 3. Dependency graph of competencies

```text
C1 Target Orientation
  answers: What bounded review target has been supplied?
  |
  v
C2 Evidence Visibility
  answers: What read-only implementation evidence is observable?
  |
  v
C3 Surface/Question Routing
  answers: Which bounded surface can answer this exact question?
  |
  v
C4 Authority Interpretation
  answers: What may this evidence authorize, and what must it refuse?
  |
  v
C5 Bounded Responsibility Understanding
  answers: What bounded work appears to be owned by implementation evidence?
  |
  v
C6 Responsibility Evaluation
  answers: Is the claimed responsibility supported, contradicted, or insufficiently visible?
  |
  v
C7 Bounded Answer Explanation
  answers: What justified answer can be composed from the evaluated evidence?
  |
  v
C8 Repository-Neutral Review Readiness
  answers: Can Seed perform a disciplined, evidence-first review of an unfamiliar repository without overclaiming authority?
```

Dependencies are deliberately conservative. Visibility before interpretation prevents vocabulary from becoming knowledge. Authority interpretation before responsibility understanding prevents observed labels from becoming ownership. Evaluation before explanation prevents answer surfaces from substituting for evidence.

## 4. Competency-by-competency analysis

### C1. Target Orientation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Target Orientation |
| Bounded question it answers | What exact repository, concern, target, or question family has the operator supplied? |
| Bounded work performed | Preserve supplied review target identity; normalize only implementation-backed parameters; distinguish operator prose from facts, goals, requirements, ownership, intent, commands, or next actions. |
| Prerequisite competencies | None. This is the entry competency. |
| Implementation evidence already supporting it | Repository-neutral review investigation requires explicit purpose or target rather than autonomous inference. Inquiry identity evidence says question-family registration, dispatch, source-navigation query identity, selection target identity, reasoning-path subject/domain, and inquiry note identity are different implementation shapes rather than one universal identity. |
| Implementation evidence still missing | No general repository-purpose extractor; no stable review-target input model for arbitrary repositories; no implementation-backed conversion from arbitrary prose to target responsibilities. |
| Authority intentionally excluded | Operator intent inference; semantic subject recovery; automatic ownership recovery; natural-language routing beyond exact registered identities; treating note text as cluster truth. |
| Proceed criteria | The review has an explicit repository path and bounded target/question/concern, or an exact implementation-backed question family with required surface arguments. |
| Stop criteria | The only input is vague prose requiring intent inference, arbitrary subject discovery, or unsupported responsibility recovery. |
| Implementation readiness | **Partially ready.** Ready for explicit targets and exact question families; not ready for autonomous orientation over unfamiliar repositories. |

### C2. Evidence Visibility

| Field | Roadmap finding |
| --- | --- |
| Competency name | Evidence Visibility |
| Bounded question it answers | What implementation evidence can Seed observe read-only, and what is invisible? |
| Bounded work performed | Collect or enumerate repository state, source relationships, diagnostics, read models, inventory rows, and test-backed surfaces without mutating repository or cluster truth. Preserve unknowns and visibility gaps as findings. |
| Prerequisite competencies | C1 Target Orientation. |
| Implementation evidence already supporting it | `RepositoryObservation` carries read-only repository metadata and non-mutation flags. `GitRepositoryObservationProvider` observes arbitrary git work trees without writes. `RepositorySourceObservationSource` extracts Python import/definition observations from configured include roots. Diagnostic inventory rows and tests preserve read-only, ledger, record, and mutation boundaries. |
| Implementation evidence still missing | Language-neutral source observation; build/test/runtime evidence collection for arbitrary repositories; documentation-claim observation outside Seed's existing corpus; generalized evidence intake for non-Python repositories. |
| Authority intentionally excluded | Mutating the target repository; importing repositories automatically; executing build or runtime actions without an operational authority; promoting diagnostic-only findings to cluster truth. |
| Proceed criteria | Relevant read-only evidence exists and its source, scope, and mutation boundary are explicit. |
| Stop criteria | Required evidence is invisible, unavailable, language/runtime-specific without support, or would require mutation/execution not authorized by current surfaces. |
| Implementation readiness | **Ready for narrow read-only evidence; incomplete for repository-neutral review.** |

### C3. Surface/Question Routing

| Field | Roadmap finding |
| --- | --- |
| Competency name | Surface/Question Routing |
| Bounded question it answers | Which bounded implemented surface, if any, is allowed to answer this exact question? |
| Bounded work performed | Match exact question-family identity to inventory rows, dispatch maps, required arguments, diagnostic-only status, and formatter/surface metadata. Refuse unregistered question families. |
| Prerequisite competencies | C1 Target Orientation and C2 Evidence Visibility. |
| Implementation evidence already supporting it | `QuestionSurfaceInventoryRow` records question family, example questions, answering surface, CLI flag, answer responsibility, authority boundary, bounded ask status, dispatch surface, required args, formatter, diagnostic inventory relationship, shape-spec relationship, and relationship status. Bounded ask maps exact registered families to dispatch surfaces and parameters. |
| Implementation evidence still missing | A repository-neutral question-surface inventory for arbitrary target repositories; implemented mapping from repository-neutral review questions to evidence surfaces; dispatch surfaces that consume non-Seed repository evidence uniformly. |
| Authority intentionally excluded | Natural-language question understanding; universal Question abstraction; dispatch to unregistered surfaces; automatic creation of review surfaces. |
| Proceed criteria | The question maps to a registered exact family or a manually bounded review question with known evidence surfaces and arguments. |
| Stop criteria | The question requires unregistered routing, semantic paraphrase matching, or creating a new abstraction to make the question answerable. |
| Implementation readiness | **Ready inside Seed's bounded ask system; not yet repository-neutral.** |

### C4. Authority Interpretation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Authority Interpretation |
| Bounded question it answers | What does the observed evidence authorize Seed to conclude, and what must remain excluded? |
| Bounded work performed | Interpret read-only, event-ledger, mutation, diagnostic, compatibility, and answer-boundary fields. Separate observed evidence, diagnostic records, projected facts, operator prose, execution authority, and cluster mutation. |
| Prerequisite competencies | C2 Evidence Visibility and C3 Surface/Question Routing. |
| Implementation evidence already supporting it | Repository observation and many audit surfaces carry `writes_event_ledger=false` and `mutates_cluster=false`. Diagnostic inventory records whether surfaces support recording, write the event ledger, or mutate cluster state. Repository-neutral review evidence identifies implementation authority, visibility sufficiency, authority boundaries, and negative ownership as neutral methodology concepts. |
| Implementation evidence still missing | A repository-neutral authority schema for arbitrary repositories; target-repository compatibility authority recovery; target-specific mutation/operational authority discovery. |
| Authority intentionally excluded | Treating read-only observation as permission to change code; treating event-ledger writes as cluster mutation; treating diagnostic findings as target truth; inferring compatibility contracts without implementation evidence. |
| Proceed criteria | Each conclusion names the authority-bearing source and its excluded authority. |
| Stop criteria | The next conclusion would require mutating, authorizing, executing, or promoting evidence beyond the source boundary. |
| Implementation readiness | **Strong for Seed surfaces; partial for unfamiliar repositories.** |

### C5. Bounded Responsibility Understanding

| Field | Roadmap finding |
| --- | --- |
| Competency name | Bounded Responsibility Understanding |
| Bounded question it answers | What bounded work does implementation evidence show is owned, consumed, produced, and explicitly not owned? |
| Bounded work performed | Recover candidate responsibility only from code, tests, records, interfaces, handoffs, diagnostics, reports, or compatibility constraints. Preserve consumed inputs, produced outputs, handoff boundaries, and negative authority. |
| Prerequisite competencies | C4 Authority Interpretation. |
| Implementation evidence already supporting it | Family stack evidence recovers Seed responsibility families by owned work, consumed artifacts, produced artifacts, upstream/downstream handoffs, orthogonal responsibilities, and shared compatibility boundaries. Repository-neutral investigation generalizes responsibility review as a methodology only when authority evidence exists. |
| Implementation evidence still missing | General arbitrary-repository responsibility recovery; target-specific intended-responsibility sources; semantic matching between names and implementation duties; evidence model for non-Seed responsibility families. |
| Authority intentionally excluded | Universal responsibility ontology; unsupported ownership recovery; using Seed's family names as another repository's architecture; promoting presentation vocabulary into knowledge. |
| Proceed criteria | A candidate responsibility has implementation-backed owner, inputs, outputs, boundaries, excluded authority, compatibility expectations, and counterexamples. |
| Stop criteria | The candidate depends on preferred vocabulary, architectural nouns, human memory, inferred intent, or Seed-specific families without target evidence. |
| Implementation readiness | **Methodologically ready; not automated or repository-neutral as machinery.** |

### C6. Responsibility Evaluation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Responsibility Evaluation |
| Bounded question it answers | Is the claimed bounded responsibility supported, contradicted, incomplete, or insufficiently visible? |
| Bounded work performed | Compare claimed responsibility to observed implementation evidence; evaluate sufficiency, counterexamples, compatibility preservation, authority boundaries, missing visibility, proceed/stop conditions, and confidence. |
| Prerequisite competencies | C5 Bounded Responsibility Understanding. |
| Implementation evidence already supporting it | Repository-neutral investigation identifies evidence sufficiency, counterexamples, confidence, bounded recommendations, and explicit stopping as repository-neutral methodology concepts. Family audits repeatedly distinguish supported handoffs from plausible but unproven universal flows. |
| Implementation evidence still missing | A generalized evaluator that consumes repository-neutral evidence and target-specific claimed responsibilities; test-backed review result schemas; target-repository compatibility-break evaluation. |
| Authority intentionally excluded | Autonomous review judgment; broad redesign; implementation planning; repository-specific fixes without target evidence; declaring mismatch when visibility is merely absent. |
| Proceed criteria | Evidence supports a clear supported/unsupported/insufficient classification and a bounded next review posture. |
| Stop criteria | Evaluation would require semantic reasoning, hidden intent, executing unsupported tooling, or treating missing evidence as failure. |
| Implementation readiness | **Ready as investigation discipline; not yet an implemented review evaluator.** |

### C7. Bounded Answer Explanation

| Field | Roadmap finding |
| --- | --- |
| Competency name | Bounded Answer Explanation |
| Bounded question it answers | What answer can Seed justify from evaluated evidence, with support, boundary, limitations, and unknowns? |
| Bounded work performed | Compose answer material from existing authorities; cite support; preserve limitations and unknowns; explain current/ambiguous/no-current-belief states for projected facts; avoid creating new truth. |
| Prerequisite competencies | C6 Responsibility Evaluation. |
| Implementation evidence already supporting it | `ExplanationBuilder` builds deterministic explanations entirely from projected `State` support and separates current beliefs, competing beliefs, conflicts, and no-current-belief status. Answer Composition family evidence shows bounded answers separate material, reasoning, support, boundary, and limitations while preserving public compatibility. |
| Implementation evidence still missing | Repository-neutral answer objects; explanation composition over arbitrary repository evidence; review-specific answer schemas; evidence citations across non-Seed target sources. |
| Authority intentionally excluded | Generalized explanation engine; semantic free-text reasoning; creating facts from explanation text; resolving ambiguity without evidence; universal explanation ontology. |
| Proceed criteria | Answer can be assembled from evaluated evidence with explicit support, authority boundary, limitations, and stop/proceed posture. |
| Stop criteria | Answer would need unsupported semantic synthesis, hidden facts, target mutation, or explanation machinery beyond existing support. |
| Implementation readiness | **Ready for Seed projected-state and bounded answer surfaces; partial for repository-neutral review.** |

### C8. Repository-Neutral Review Readiness

| Field | Roadmap finding |
| --- | --- |
| Competency name | Repository-Neutral Review Readiness |
| Bounded question it answers | Can Seed perform a disciplined, repository-neutral, evidence-first review of an unfamiliar repository without overclaiming? |
| Bounded work performed | Integrate explicit orientation, read-only evidence visibility, registered surface routing, authority interpretation, responsibility understanding, evaluation, and bounded explanation into a review answer that may conclude support, contradiction, insufficient evidence, or stop. |
| Prerequisite competencies | C1 through C7. |
| Implementation evidence already supporting it | Existing repository-neutral review investigation says the methodology is supported, not the implemented capability. Repository observation and source observation provide narrow neutral evidence. Responsibility and answer family audits provide Seed-specific examples of the discipline. |
| Implementation evidence still missing | Implemented repository-neutral review input model; target-repository responsibility-source intake; language/runtime-neutral evidence adapters; review result schema; tests proving review over a non-Seed fixture repository; diagnostic inventory/shape coverage if exposed as a CLI diagnostic. |
| Authority intentionally excluded | Autonomous reviewer; planner; repository importer; semantic review engine; ownership recovery engine; universal representation/grammar/artifact/provider/question/explanation abstractions. |
| Proceed criteria | A non-Seed fixture can be reviewed from explicit target + read-only evidence + target-specific authority sources, producing a bounded answer that refuses unsupported claims. |
| Stop criteria | Review requires the missing competencies above or collapses into a backlog, implementation plan, ownership recovery, or abstraction proposal. |
| Implementation readiness | **Not ready as an implemented capability. Ready only as the acquisition target.** |

## 5. Existing implementation support

### Strong support

1. **Read-only repository observation.** The repository observer is intentionally generic over arbitrary git-backed paths and includes explicit non-mutation flags.
2. **Source relationship observation.** Python import and definition extraction provides an implementation-backed way to see some structure in a configured repository root.
3. **Question-family inventory.** Exact question family rows prevent free-form semantic routing from masquerading as implementation-backed inquiry.
4. **Diagnostic inventory and shape checks.** Operational visibility rules require surfaces to be registered and audited for record, ledger, and mutation behavior.
5. **Authority-boundary discipline.** Current reports and tests repeatedly preserve `writes_event_ledger=false` and `mutates_cluster=false` for read-only diagnostics and observations.
6. **Responsibility-family evidence discipline.** Completed family audits show how to recover bounded work from implementation evidence while preserving orthogonal responsibilities and handoff boundaries.
7. **Answer and explanation discipline.** Existing explanation and answer-composition surfaces explain projected support and limitations rather than inventing truth.

### Medium support

1. **Repository-neutral methodology.** The methodology is well recovered, but remains mostly a report/investigation discipline.
2. **Responsibility evaluation.** Seed can evaluate Seed responsibilities with strong evidence, but arbitrary-repository evaluation requires target-specific authority sources.
3. **Inquiry lineage and explanation.** Lineage exists in bounded surfaces, but family vocabulary remains less stable and should not be generalized prematurely.

### Weak or absent support

1. **Autonomous target orientation.** No implementation extracts general program purpose or intended responsibilities from arbitrary repositories.
2. **Language-neutral implementation evidence.** Current source observation is Python/import/definition oriented.
3. **Repository-neutral review surface.** No test-backed CLI/report currently integrates all competencies against a non-Seed repository fixture.
4. **General semantic understanding.** Existing surfaces use exact identities, deterministic matching, and projected evidence; they do not perform free-text semantic reasoning.

## 6. Missing implementation evidence

Before repository-neutral review can be considered implementation-backed, Seed would need evidence for the following, in competency order:

1. **Target orientation evidence:** an explicit review target model that preserves supplied repository path, target concern, and excluded intent inference.
2. **Visibility evidence:** read-only evidence adapters broad enough for the review target, plus tests proving non-mutation boundaries.
3. **Routing evidence:** a review question/surface registry that maps exact repository-neutral review questions to implemented evidence consumers.
4. **Authority evidence:** a schema that records source authority, mutation boundaries, compatibility boundaries, and diagnostic/run scope for target-repository evidence.
5. **Responsibility-understanding evidence:** target-specific responsibility candidates sourced from implementation-backed artifacts, not inferred architectural nouns.
6. **Evaluation evidence:** a result shape and tests proving supported/unsupported/insufficient classifications without treating missing visibility as failure.
7. **Explanation evidence:** a review answer surface that composes support, counterexamples, authority boundary, limitations, and stop/proceed posture.
8. **Integration evidence:** a non-Seed fixture repository reviewed end-to-end with expected bounded refusal behavior.

If any of these become diagnostic, audit, probe, view, operational CLI flag, or recordable output, the diagnostic inventory and shape-audit obligations apply before the surface can count as visible.

## 7. Recommended competency acquisition order

1. **Target Orientation** — Seed must first learn to preserve the supplied review target and refuse hidden intent recovery.
2. **Evidence Visibility** — Seed then needs enough read-only evidence to know what it can and cannot see.
3. **Surface/Question Routing** — Seed must route only exact, registered bounded questions to implemented surfaces.
4. **Authority Interpretation** — Seed must learn what observed evidence can authorize before naming responsibility.
5. **Bounded Responsibility Understanding** — Seed can then identify bounded work only where authority evidence supports it.
6. **Responsibility Evaluation** — Seed can compare claims to evidence and classify support, contradiction, or insufficiency.
7. **Bounded Answer Explanation** — Seed can compose justified review answers with support, boundaries, limitations, and stopping.
8. **Repository-Neutral Review Readiness** — Only after the previous competencies are implementation-backed should Seed claim repository-neutral review capability.

This order follows the recovered discipline:

```text
Responsibilities own bounded work.
Questions determine which bounded work must be performed.
Answers are justified results of that work.
```

The order starts with questions/targets because the current implementation cannot responsibly recover arbitrary intended work without an explicit target. It reaches responsibilities only after evidence and authority are visible. It reaches answers only after evaluation.

## 8. Explicit stopping boundaries

Seed must stop rather than proceed when a review would require any of the following:

- autonomous review or planner behavior;
- repository import automation;
- semantic free-text reasoning as authority;
- universal Representation, Grammar, Artifact, provider pipeline, Question, or explanation abstractions;
- unsupported identity recovery;
- unsupported responsibility or ownership recovery;
- treating Seed-specific responsibility families as target-repository architecture;
- treating diagnostic findings as cluster truth;
- mutating a repository or executing target tooling without an implemented operational authority;
- declaring mismatch where evidence is merely invisible;
- promoting presentation vocabulary into preserved or projected knowledge without implementation evidence;
- producing an implementation plan, backlog, or ownership-recovery proposal instead of a competency-bounded review answer.

## 9. Long-term competencies separated from current implementation readiness

These are plausible future competencies, but they are **not** current readiness claims:

1. **Target-purpose recovery from authoritative artifacts.** A future Seed may learn to recover intended purpose from READMEs, package metadata, tests, schemas, or docs, but only if those sources are authority-classified and counterexample-tested.
2. **Language-neutral structural evidence.** A future Seed may support multiple language adapters, but each adapter must remain provider-local rather than implying a universal grammar.
3. **Target-specific responsibility-source intake.** A future Seed may accept responsibility candidates from target tests, docs, schemas, or APIs, but must preserve source authority and excluded authority.
4. **Review result schema.** A future Seed may produce structured repository-neutral review answers, but only after support, boundary, limitations, and stop/proceed criteria are test-backed.
5. **Cross-repository fixture evaluation.** A future Seed should prove the review discipline against non-Seed fixture repositories, including expected refusals.
6. **Compatibility authority recovery.** A future Seed may evaluate compatibility expectations for a target repository, but must recover those expectations from target evidence rather than impose Seed's compatibility norms.

## 10. Open questions

1. What should count as an authority-bearing intended-responsibility source in an unfamiliar repository: tests, docs, API schemas, package metadata, examples, issue templates, or only executable contracts?
2. Should repository-neutral review begin with a human-supplied responsibility claim, a human-supplied question family, or a constrained target-purpose artifact?
3. Which evidence adapters are necessary before review is meaningfully repository-neutral rather than Python/Seed-adjacent?
4. How should Seed represent insufficient visibility without encouraging implementation recommendations?
5. What minimal non-Seed fixture would prove the competency chain without creating a review engine prematurely?
6. How should review answer citations refer to target repository files while preserving the difference between target evidence and Seed evidence?
7. If a review surface becomes recordable, should all repository-neutral findings be scoped under `diagnostic_run:<id>` by default?
8. What tests would prove that Seed refuses unsupported identity and responsibility recovery under tempting vocabulary overlap?
9. Can bounded review recommendations remain proceed/stop/insufficient-evidence, or is a fourth state needed for “evidence belongs to another authority”? 
10. Where should compatibility expectations come from when a target repository has code and tests but weak documentation?
