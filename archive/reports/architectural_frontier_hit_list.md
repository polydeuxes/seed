# Architectural Frontier Hit List

## 1. Executive summary

Seed's current frontier supports disciplined movement toward bounded repository-neutral review, but only through small evidence-backed investigations and slices. The next work should not review an unfamiliar repository yet. It should clarify the minimum inputs and transformations that a future review would need without promoting repository, source tree, imports, provider payloads, observations, or diagnostics into broader authority than the implementation currently grants.

The practical heuristic remains:

```text
What bounded work
does this responsibility perform?
```

Applied to repository-neutral review, the next frontier is not a universal review engine. It is a sequence of narrow clarifications around:

1. what counts as a review target without treating a repository as a program;
2. what evidence may be decoded from provider/source structures without inferring responsibility;
3. what internal review input shape can compose already-observed evidence without becoming generic `Representation`, `Grammar`, or `Artifact`;
4. what visibility is sufficient to evaluate one bounded responsibility mismatch;
5. where Seed must stop because authority, identity, behavior, or intent is not implementation-backed.

The recommended first three moves are:

1. **Program/service identity input boundary investigation**.
2. **Repository-neutral review input packet slice**.
3. **Provider decoding boundary audit**.

These moves preserve the existing frontier: external grammars, internal grammars, artifact flow, bounded transformations, local composition, and representation discipline. They move toward bounded repository-neutral review by clarifying review inputs and evidence boundaries, not by implementing autonomous review.

## 2. Current frontier

### 2.1 What is currently supported

Recent investigations support a bounded evidence-first methodology, not implemented autonomous review. The supported chain is:

```text
explicit review target or candidate responsibility
↓
authority-bearing intended-responsibility evidence
↓
read-only observed implementation evidence
↓
visibility / authority / compatibility evaluation
↓
proceed / stop / insufficient evidence
```

Implementation-backed support includes:

- Repository observation identifies git working-tree/status evidence, not program identity or responsibility-bearing system identity.
- Repository source observation currently observes allowlisted Python import and definition relationships under configured roots, not calls, behavior, entrypoints, ownership, or runtime capability.
- Observation providers already convert provider/source structures into Seed `Observation` records, but provider responsibilities differ by source and include provider-specific decoding in some cases.
- Relationship extraction exposes bounded Python syntax evidence and explicitly refuses behavior, routes, ownership, capability authority, and runtime ownership.
- Representation-transformation discipline exists as local bounded transformations between existing implementation records, not as a universal representation pipeline.
- Expression composition exists through concrete surfaces such as evidence, fact supports, fact views, inquiry orientation, operational story, and question-family explanations, not through a generalized explanation subsystem.
- Slice and responsibility recovery readiness support evaluating proposed work against implementation compression, upstream fulfilled work, boundary-crossing artifacts, excluded authority, compatibility expectations, counterexamples, and explicit stopping.
- Repository-neutral program review is supported as a human-scoped methodology, not as implemented machinery.

### 2.2 Frontier pressure

The next pressure is to determine what bounded work Seed must clarify before a future repository-neutral review can be evaluated. The pressure is not to import repositories, discover program purpose, infer ownership, or recommend code changes. The pressure is to clarify:

- how a review target is represented without conflating repository, program, service, runtime artifact, source corpus, and responsibility-bearing system;
- how provider/source payloads become observations without unbounded interpretation;
- how candidate responsibilities become review inputs without automatic recovery;
- how internal evidence packets preserve provenance, negative authority, and insufficient evidence;
- how local composition can produce a bounded review evaluation without a universal provider pipeline or explanation subsystem.

## 3. Things explicitly not to do

Do not start with any of the following:

- introduce generic `Representation`;
- introduce generic `Grammar`;
- introduce generic `Artifact`;
- introduce a universal provider pipeline;
- introduce autonomous review;
- introduce planner behavior;
- introduce repository import automation;
- infer program purpose from prose without implementation-backed authority;
- treat repository identity as program identity;
- treat Python imports, definitions, packages, file layout, or names as responsibilities;
- treat diagnostics, observations, or inquiry notes as cluster truth;
- promote Seed's recovered responsibility families into another repository's architecture;
- turn methodology into an implementation plan for arbitrary repositories;
- recommend code changes to a target repository before intended responsibility and observed implementation evidence are both available;
- widen source observation into behavior, call graph, entrypoint, route, ownership, or capability inference without a separate evidence-backed slice;
- make compatibility breaks part of review authority before compatibility evidence is separately recovered.

## 4. Ranked hit list

| Rank | Candidate | Type | Why this rank |
| ---: | --- | --- | --- |
| 1 | Program/service identity input boundary | investigation | Repository-neutral review needs a review target, but existing evidence explicitly separates repository, source relationships, runtime observation, inquiry note, and responsibility identity. |
| 2 | Repository-neutral review input packet | slice | Once target identity boundaries are clear, Seed needs a minimal local composition input shape for review evidence without creating generic representation or review automation. |
| 3 | Provider decoding boundary | audit | Review inputs depend on provider-decoded evidence. Current providers mix acquisition and interpretation differently, so the boundary must be inventoried before relying on provider observations. |
| 4 | External grammar to observation grammar compatibility | investigation | External structures must become Seed observations through bounded decoding, not through a universal grammar abstraction. |
| 5 | Candidate responsibility evidence gate | slice | Future review needs a gate that preserves candidate responsibility, intended evidence, observed evidence, and excluded authority before evaluation. |
| 6 | Visibility sufficiency checklist for one bounded review concern | slice | Review must distinguish mismatch from insufficient visibility using existing diagnostics/evidence patterns. |
| 7 | Repository-source relationship non-authority regression | audit | Python imports/definitions must remain syntax evidence only as review pressure increases. |
| 8 | Local composition explanation boundary | investigation | Review output will need composed explanation, but existing evidence rejects a generalized explanation subsystem. |
| 9 | Bounded transformation trace between review inputs and evaluation rows | slice | A later review evaluation needs auditable transformation trace without generic representation or artifact abstractions. |
| 10 | Stop: autonomous repository-neutral review command | stop | Current evidence does not support autonomous review, repository import, program-purpose inference, or implementation recommendations. |

## 5. Candidate-by-candidate evaluation

### 5.1 Program/service identity input boundary

- **Type:** investigation.
- **Why it is next:** Repository-neutral review cannot start until Seed can say what the review target is without collapsing repository, program, source corpus, runtime artifact, service, and responsibility-bearing system into one identity.
- **What bounded work is being clarified:** Distinguish the bounded work of carrying an operator-supplied review target from the unsupported work of discovering program purpose or responsibility identity.
- **Upstream fulfilled work:** Repository/program identity investigation already recovered explicit distinctions among repository state, repository source relationships, language adapter evidence, observation identity, runtime artifact observation, inquiry identity, and absent general responsibility-bearing identity. Repository-neutral review investigation already requires an explicit review target or purpose.
- **Explicit evidence that would cross the boundary:** A report mapping existing implementation records and fields that may participate in review target identity: repository path/status, repository root/include roots, source path, observation subject, runtime process observation, inquiry note target text, question-family arguments, and candidate responsibility identifiers. Evidence crosses only when tied to implementation fields, tests, or CLI surfaces.
- **Authority intentionally not assumed:** Program purpose, service boundary, runtime entrypoint, ownership, responsibility, operator intent, repository import authority, execution authority, and mutation authority.
- **Compatibility expectation:** No behavior change. Existing repository observation, repository-source observation, inquiry orientation, and ask dispatch semantics remain unchanged.
- **Proceed criteria:** The investigation identifies a minimal set of existing fields that can safely name a review target and enumerates target identities that must remain unsupported.
- **Stop criteria:** Evidence shows only repository/source identities are available and no safe review-target carrier exists beyond operator prose and existing arguments.
- **Insufficient evidence criteria:** The candidate target requires service/runtime identity or program purpose not present in code, tests, diagnostics, records, or explicit operator-supplied scope.

### 5.2 Repository-neutral review input packet

- **Type:** slice.
- **Why it is next:** Once review target boundaries are clarified, Seed needs a minimal local composition object that can hold review inputs without implementing review, generic representation, or repository import.
- **What bounded work is being clarified:** Preserve a bounded packet of review target, candidate responsibility, intended-responsibility evidence references, observed implementation evidence references, visibility caveats, authority exclusions, and compatibility expectations.
- **Upstream fulfilled work:** Slice evaluation readiness and responsibility recovery readiness already establish packet-like evaluation criteria: upstream fulfilled work, owner/adjacent surface, boundary-crossing artifact, excluded authority, compatibility, counterexamples, and proceed/stop/insufficient evidence. Program review readiness already supports human-scoped review evaluation in principle.
- **Explicit evidence that would cross the boundary:** A dataclass or report row, if later implemented, containing only references to existing evidence IDs/paths/surfaces and explicit negative authority fields. No interpretation beyond preserving supplied/recovered references.
- **Authority intentionally not assumed:** No autonomous selection of candidate responsibilities, no repository scan, no semantic parser, no review verdict, no implementation recommendation, no fact promotion.
- **Compatibility expectation:** Additive only. If implemented later, it should not alter observation ingestion, fact promotion, diagnostics, question-family dispatch, or existing reports.
- **Proceed criteria:** A minimal input shape can be specified using existing evidence categories and negative authority without introducing generic `Representation`, `Grammar`, or `Artifact`.
- **Stop criteria:** The slice requires automatic target discovery, source interpretation, or review judgment.
- **Insufficient evidence criteria:** Existing evidence cannot identify stable references for intended evidence, observed evidence, or authority exclusions.

### 5.3 Provider decoding boundary

- **Type:** audit.
- **Why it is next:** Repository-neutral review will consume observations, but current providers vary in how much acquisition, decoding, and structural interpretation they perform.
- **What bounded work is being clarified:** Inventory which providers decode external structures into Seed observations, which interpretation decisions happen inside providers, which happen in helpers, and which happen downstream through normalization, ingestion, and projection.
- **Upstream fulfilled work:** Observation provider structure identity and provider representation-to-observation investigations already show that `ObservationSource.collect()` returns Seed observations, Prometheus performs metric-specific interpretation, local-host observation mixes several read-only interpretations, repository source delegates Python syntax extraction to helpers, and capability candidates are downstream rather than provider-verified capabilities.
- **Explicit evidence that would cross the boundary:** Provider-by-provider table of acquired input, decoding step, emitted observation predicates, metadata authority markers, downstream normalization/ingestion behavior, and explicit non-authority flags.
- **Authority intentionally not assumed:** Universal provider pipeline, common provider grammar, capability proof, service identity, endpoint health, program intent, and ownership.
- **Compatibility expectation:** No behavior change. Audit only. Existing provider outputs and diagnostic inventory remain unchanged unless a later separate slice changes an operational surface.
- **Proceed criteria:** Audit can distinguish provider-specific decoding from downstream observation/fact behavior using implementation evidence.
- **Stop criteria:** The audit starts proposing provider refactors or common abstractions.
- **Insufficient evidence criteria:** Provider metadata does not expose enough authority markers to determine what interpretation occurred.

### 5.4 External grammar to observation grammar compatibility

- **Type:** investigation.
- **Why it is next:** Review input depends on external grammars becoming observations without a generic grammar abstraction.
- **What bounded work is being clarified:** Identify the existing external grammar surfaces and how each maps into Seed observation grammar: Prometheus JSON/vector samples, dpkg status text, systemd output, git status, Python syntax, local `/proc`/platform structures, and inquiry note text.
- **Upstream fulfilled work:** Provider grammar to observation grammar and provider representation-to-observation investigations already establish that Seed has local grammar translations, not one universal grammar.
- **Explicit evidence that would cross the boundary:** A compatibility matrix listing external structure, decoder, emitted predicates/subjects/metadata, negative authority, and tests or reports that prove the mapping.
- **Authority intentionally not assumed:** Generic `Grammar`, generic artifact flow, semantic meaning of arbitrary prose, service health, responsibility identity, or program behavior.
- **Compatibility expectation:** All existing observation shapes remain compatible; no new predicates are introduced by the investigation.
- **Proceed criteria:** Existing mappings can be documented as bounded local translations with explicit authority limits.
- **Stop criteria:** A mapping requires interpreting arbitrary repository-specific grammar not implemented today.
- **Insufficient evidence criteria:** No tests or implementation evidence demonstrate the translation boundary for a candidate external structure.

### 5.5 Candidate responsibility evidence gate

- **Type:** slice.
- **Why it is next:** A future review must not evaluate a responsibility unless the candidate responsibility and both intended/observed evidence are present with authority limits.
- **What bounded work is being clarified:** Gate a candidate review concern into `proceed`, `stop`, or `insufficient evidence` before any review evaluation.
- **Upstream fulfilled work:** Responsibility recovery readiness already supports evaluating proposed responsibility recoveries against implementation evidence, upstream work, existing owners, boundary artifacts, excluded authority, compatibility, and stopping criteria.
- **Explicit evidence that would cross the boundary:** A row-level decision that records candidate responsibility text, supplied target identity, intended evidence references, observed evidence references, upstream fulfilled work, excluded authority, and compatibility expectation.
- **Authority intentionally not assumed:** Recovery of responsibilities from repository contents, ownership discovery, semantic interpretation, fix recommendation, or planner behavior.
- **Compatibility expectation:** Additive evaluator or report-only slice. It must not mutate cluster truth, promote diagnostics, or alter existing observations.
- **Proceed criteria:** Candidate has explicit target, at least one intended-responsibility authority surface, at least one observed implementation evidence surface, and explicit negative authority.
- **Stop criteria:** Candidate requires unsupported program purpose, autonomous ownership recovery, implementation recommendation, or compatibility break authority.
- **Insufficient evidence criteria:** Candidate has only prose, naming resemblance, imports, file layout, or diagnostics without intended responsibility evidence.

### 5.6 Visibility sufficiency checklist for one bounded review concern

- **Type:** slice.
- **Why it is next:** Repository-neutral review must distinguish implementation mismatch from insufficient observability.
- **What bounded work is being clarified:** Produce a checklist for one review concern that asks whether the target has enough evidence surfaces to support evaluation: code, tests, public surface, event/payload/schema, diagnostic, read-only observation, compatibility contract, or explicit absence.
- **Upstream fulfilled work:** Program review readiness and repository-neutral review investigation both treat visibility sufficiency as a first-class review result. Diagnostic inventory and shape-audit practices show how operational surfaces remain visible when added, though this slice should not add diagnostics unless separately justified.
- **Explicit evidence that would cross the boundary:** A bounded checklist result attached to a candidate responsibility input packet, not to cluster truth.
- **Authority intentionally not assumed:** That lack of evidence means defect, that diagnostics are truth, or that visibility gaps authorize implementation changes.
- **Compatibility expectation:** Report-only unless later implemented as an additive read-only surface. If implemented as diagnostic output, the operational visibility contract applies.
- **Proceed criteria:** Checklist can classify a candidate concern as reviewable, not reviewable, or visibility-insufficient using existing evidence types.
- **Stop criteria:** The checklist becomes a generic quality framework or review score.
- **Insufficient evidence criteria:** Evidence needed to decide visibility is itself unavailable or repository-specific without implementation support.

### 5.7 Repository-source relationship non-authority regression

- **Type:** audit.
- **Why it is next:** As review pressure increases, Python import/definition observations are likely to be over-read as architecture or responsibility evidence.
- **What bounded work is being clarified:** Preserve the boundary that repository-source relationships prove only syntax/name-availability/declaration evidence, not behavior, runtime reachability, service boundaries, ownership, or responsibility.
- **Upstream fulfilled work:** Repository/program identity and observation provider structure investigations explicitly recover this negative authority. Existing repository-source tests assert no calls or entrypoints are emitted.
- **Explicit evidence that would cross the boundary:** Audit rows or tests confirming repository-source observations remain limited to imports/defines and carry metadata boundaries where implemented.
- **Authority intentionally not assumed:** Calls, routes, runtime behavior, entrypoints, service identity, capability authority, ownership, or responsibility.
- **Compatibility expectation:** Existing repository-source outputs stay stable; no new behavior facts are introduced.
- **Proceed criteria:** Audit confirms current implementation and tests protect non-authority boundaries.
- **Stop criteria:** Proposed work attempts to use imports/definitions as responsibility proof.
- **Insufficient evidence criteria:** Metadata/test coverage is insufficient to prove consumers cannot over-promote relationship observations.

### 5.8 Local composition explanation boundary

- **Type:** investigation.
- **Why it is next:** A future review result must compose evidence into a human-readable explanation, but existing evidence rejects a generalized explanation subsystem.
- **What bounded work is being clarified:** Identify the local composition pattern that can explain one candidate review evaluation from existing evidence references, caveats, counterexamples, and stopping criteria.
- **Upstream fulfilled work:** Expression composition explanation investigation shows multiple expression-like sources and concrete composition surfaces, while rejecting a universal `Expression` abstraction or generalized explanation owner.
- **Explicit evidence that would cross the boundary:** A mapping from existing composition surfaces to a possible review evaluation report shape: identity, evidence references, support, caveats, negative authority, and proceed/stop/insufficient evidence.
- **Authority intentionally not assumed:** General explanation subsystem, semantic explanation, program-purpose inference, or recommendation authority.
- **Compatibility expectation:** No change to existing answer, inquiry, operational story, or fact explanation surfaces.
- **Proceed criteria:** Investigation identifies a local report composition shape consistent with existing answer-composition boundaries.
- **Stop criteria:** Work requires a universal explanation layer or new architectural vocabulary.
- **Insufficient evidence criteria:** Existing composition surfaces cannot support review output without inventing new authority.

### 5.9 Bounded transformation trace between review inputs and evaluation rows

- **Type:** slice.
- **Why it is next:** Review evaluation will need auditable transformation from input packet to evaluation rows, but representation discipline rejects universal transformations.
- **What bounded work is being clarified:** Trace a local transformation from review input packet to candidate evaluation row, preserving source references and negative authority.
- **Upstream fulfilled work:** Representation transformation discipline investigation found bounded local transformations among existing records and rejected one-input/one-output or universal representation laws. Slice evaluation readiness supplies the row criteria.
- **Explicit evidence that would cross the boundary:** A trace showing input field, transformation function or report rule, output field, preserved evidence reference, and excluded authority.
- **Authority intentionally not assumed:** Generic transformation law, generic representation, artifact abstraction, autonomous evaluation, or hidden fact promotion.
- **Compatibility expectation:** Additive and read-only. No impact on observation ingestion, state projection, or existing diagnostics.
- **Proceed criteria:** A trace can be implemented or specified for one candidate without generalizing beyond local review evaluation.
- **Stop criteria:** Work tries to define a universal transformation pipeline.
- **Insufficient evidence criteria:** The candidate input packet itself lacks sufficient references to trace.

### 5.10 Stop: autonomous repository-neutral review command

- **Type:** stop.
- **Why it is next:** It is the tempting wrong move. Current evidence supports methodology and readiness investigations, not a command that reviews arbitrary repositories.
- **What bounded work is being clarified:** The stop boundary itself: Seed must not jump from frontier reports to autonomous review machinery.
- **Upstream fulfilled work:** Repository-neutral program review investigation, program review readiness, slice evaluation readiness, and responsibility recovery readiness all reject autonomous review, planning, ownership recovery, semantic interpretation, automatic confidence, and implementation recommendations.
- **Explicit evidence that would cross the boundary:** None today. Required evidence would include safe review-target identity, intended-responsibility authority, observed implementation coverage beyond narrow Python relationships, visibility sufficiency, compatibility recovery, and bounded recommendation authority.
- **Authority intentionally not assumed:** Repository import, program-purpose inference, autonomous responsibility recovery, automatic review verdict, planner behavior, code changes, execution, or mutation.
- **Compatibility expectation:** Do not implement.
- **Proceed criteria:** Not met.
- **Stop criteria:** Current state.
- **Insufficient evidence criteria:** Also current state, if framed as a proposal rather than a stop.

## 6. Recommended first three moves

### Move 1: Program/service identity input boundary investigation

Start here because every later review concern needs a target. The investigation should produce a narrow map of what Seed can safely name today and what must remain unsupported. It should avoid implementation and should not create a new identity abstraction.

Expected output: a report that says which existing fields can participate in review target identity and which identities require explicit operator scope or separate implementation evidence.

### Move 2: Repository-neutral review input packet slice

After target boundaries are explicit, define the smallest additive input shape for a future review evaluation. This should preserve references and caveats, not evaluate or recommend. It should be local to review evaluation readiness and must not become generic `Representation` or `Artifact`.

Expected output: a later separate slice, if justified, that records review target, candidate responsibility, intended evidence, observed evidence, visibility caveats, excluded authority, and compatibility expectation.

### Move 3: Provider decoding boundary audit

Before review evaluation consumes observations, audit what observations already mean and where interpretation occurred. This protects review from treating provider output as raw truth or as responsibility evidence.

Expected output: provider/source decoding inventory with negative authority and downstream handoff boundaries.

## 7. Stopping criteria

Stop a candidate when any of the following is required:

- inferring program purpose from repository layout, prose, package names, imports, definitions, or naming resemblance;
- treating repository identity as program/service/responsibility identity;
- promoting inquiry notes, diagnostics, observations, or review findings into facts or cluster truth;
- using Python imports/definitions as calls, behavior, entrypoints, routes, ownership, capability authority, or responsibility proof;
- introducing generic `Representation`, `Grammar`, or `Artifact`;
- introducing universal provider, transformation, explanation, or review pipelines;
- implementing autonomous repository review, repository import, planning, or code modification;
- recommending implementation changes without intended responsibility evidence and observed implementation evidence;
- changing operational diagnostic surfaces without inventory, shape-audit specs, tests, record scope proof where relevant, and event-ledger mutation proof where relevant;
- relying on Seed-specific responsibility families as if they are another repository's architecture;
- approving compatibility breaks without separately recovered compatibility authority.

Stop with **insufficient evidence** rather than failure when the candidate has a plausible pressure but lacks implementation-backed target identity, intended responsibility authority, observed implementation evidence, visibility sufficiency, or compatibility expectation.

## 8. Open questions

1. What existing field or record is the safest carrier for a repository-neutral review target: operator-supplied target text, repository path, source root, observation subject, or a new local review-input row?
2. Can intended-responsibility evidence be supplied entirely by an operator while preserving the boundary that operator prose is not automatically truth?
3. What is the smallest observed-implementation evidence set that can support one bounded review concern without broad source understanding?
4. Which provider outputs already carry enough negative authority metadata for review consumption, and which only have negative authority in prose/tests?
5. Should review input packets cite evidence IDs, file paths, diagnostic row identifiers, observation subjects, or all of these depending on source?
6. Can visibility sufficiency be evaluated as a report-only checklist before any diagnostic surface exists?
7. What compatibility evidence is required for an unfamiliar repository when no Seed-like diagnostic or test corpus is available?
8. How should Seed preserve `insufficient evidence` as a first-class result without turning it into a recommendation to add visibility?
9. What local composition surface, if any, should render a bounded review evaluation without creating a generalized explanation subsystem?
10. Where is the boundary between repository-neutral review methodology and Seed-specific inquiry/answer surfaces?
