# Repository Artifact / Runtime Artifact Characterization

## Executive answer

Repository evidence is sufficient to recognize a stable distinction between **repository artifacts** and **runtime artifacts**.

The repository does **not** support the rule that every mature artifact must eventually become runtime implementation. It repeatedly preserves mature documentation families because they own repository competencies: orientation, vocabulary, boundary reasoning, status, roadmap sequencing, decision provenance, historical findings, negative findings, investigation record, pressure preservation, and safe handoff of architectural context.

The strongest supported answer is:

```text
mature repository artifact
    -> may remain a durable repository competency surface
    -> may inform implementation
    -> does not thereby become runtime behavior
```

This is not a preference for documentation over implementation. It is the repository's current authority model. Seed's runtime owns observation intake, evidence, facts, projections, read-only views, capability-gap recommendation, event ledgers, and bounded runtime routing. Repository artifacts own architectural memory, navigation, currentness, vocabulary, historical proof, and boundary discipline where those responsibilities are about humans or future work recognizing what the repository has already learned.

If Seed eventually reads prose, the reviewed evidence indicates that ownership does **not** automatically move from repository artifact to runtime implementation. Prose-reading would create a new consumer and observation path over documentation artifacts. It would not make documentation an executable instruction stream, runtime governance engine, or automatic source of architectural truth.

## Repository evidence reviewed

Representative evidence included:

- `README.md`, especially the repository orientation, scope, ownership, non-ownership, and authority model sections.
- `IMPLEMENTATION.md`, especially the implemented runtime scope, non-execution boundary, legacy artifact quarantine, and explicit delegation of execution.
- `docs/seed.md`, especially the constitutional architecture paths and warnings against sequence overclaiming.
- `docs/ontology.md`, especially the claim-centric vocabulary, core boundaries, and relationship to implementation.
- `docs/README.md`, especially the documentation map and routing role.
- `docs/documentation_authority_reconciliation.md`, especially document-family authority assignments.
- `docs/documentation_lifecycle_reconciliation.md`, especially lifecycle roles and the duplicate-authority problem.
- `docs/architectural_status_and_next_frontier.md`, especially active frontier ownership, paused work, and non-goals.
- `docs/architectural_findings_preservation.md`, especially preservation responsibility, completed audit memory, and negative findings.
- `docs/documentation_prose_as_language_bearing_source_reconciliation.md`, especially the future prose-reading boundary.
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`, especially language as observation rather than truth, authority, or execution.
- `docs/work_recognition_reality_audit.md`, as an example of mature documentation explicitly bounded as audit, not runtime proposal.
- Runtime-facing implementation summaries in `IMPLEMENTATION.md` and the repository layout description in `README.md`.

## Recurring distinction

The recurring distinction is not merely "docs versus code." It is a responsibility boundary:

| Artifact kind | Primary responsibility | Authority form | Non-authority |
| --- | --- | --- | --- |
| Repository artifact | Preserve, route, explain, reconcile, audit, characterize, sequence, or hand off repository knowledge. | Documentation-scoped authority: orientation, vocabulary, lifecycle, status, finding preservation, scoped decision provenance, observed evidence. | Does not execute, mutate runtime state, project environmental facts, or write ledger truth by default. |
| Runtime artifact | Implement Seed behavior over observations, evidence, claims, facts, projections, views, capability gaps, policy metadata, and bounded operator responses. | Implementation-backed behavior and tested runtime invariants. | Does not absorb all architectural memory, all documentation vocabulary, all future work, or all mature prose. |

This boundary appears in several forms:

1. `README.md` separates the current implementation directories from `docs/`, and describes `docs/` as architectural thesis, navigation, reconciliations, vocabularies, audits, and status documents rather than runtime modules.
2. `docs/README.md` says it is a documentation navigation authority and a map, not an encyclopedia.
3. `docs/documentation_authority_reconciliation.md` assigns different authority forms to README, maps, canonical architecture documents, status/frontier documents, roadmap documents, reconciliations, vocabularies, audits, inventories, and generated references.
4. `docs/documentation_lifecycle_reconciliation.md` says the problem is duplicate authority, not lack of prose, and proposes lifecycle roles rather than a runtime document database or governance subsystem.
5. `docs/architectural_findings_preservation.md` says preservation itself is an owned responsibility and that non-implementation conclusions are architecture knowledge, not incomplete work.
6. `IMPLEMENTATION.md` describes the runtime as knowledge/handoff-oriented and explicitly says Seed is no longer being documented as an internal executor or workflow engine.

## Repository-owned responsibilities

### 1. Constitutional thesis and invariants

`docs/seed.md` owns the concise constitutional statement of Seed's claim-centric architecture. Its architecture paths are explicitly conceptual, not rigid runtime pipelines. The responsibility is to preserve the shape and boundary of the architecture so implementation and future reasoning do not overclaim sequence, causality, authority, or execution.

This responsibility is documentation-owned because it governs interpretation of many surfaces. A runtime module can realize parts of the thesis, but no single runtime module owns the repository's constitutional answer to what Seed is.

### 2. Stable vocabulary and boundary reference

`docs/ontology.md` owns concise vocabulary and boundaries. It explicitly says it is not a schema, storage model, runtime design, or reconciliation argument. It also states that implementation may realize, serialize, cache, expose, or test concepts, but implementation vocabulary does not define the ontology exhaustively.

That is direct evidence against "ontology maturity means schema/runtime ownership." The ontology can be mature and implementation-independent at the same time.

### 3. Navigation and answer routing

`README.md` and `docs/README.md` own orientation and routing. They tell readers where to start, which documents own which concerns, and where current status and canonical references live.

Navigation remains repository-owned because it supports human and future-agent consumption of repository knowledge. It is not a runtime behavior unless a later implementation explicitly builds a navigation consumer. Even then, the map's authority would remain scoped to routing unless superseded by repository process.

### 4. Documentation authority and lifecycle control

`docs/documentation_authority_reconciliation.md` and `docs/documentation_lifecycle_reconciliation.md` own distinctions among canonical, active, reference, historical, superseded, archived, and deprecated documentation roles. They address duplicate authority, preservation, supersession, and safe archival.

These responsibilities are not runtime-owned because the problem is repository authority hygiene: preventing old or overlapping documents from appearing equally current. The lifecycle reconciliation explicitly excludes production code, tests, runtime behavior, event schemas, projection schemas, providers, policy behavior, acquisition logic, generated artifacts, and a runtime document database.

### 5. Current status, roadmap, and frontier ownership

`docs/architectural_status_and_next_frontier.md` owns current architectural status and active frontier. Roadmap documents own sequencing and backlog context. Frontiers preserve unresolved pressure and not-yet-reconciled inquiry.

This is intentionally not a planner. The status/frontier document explicitly says paused work should not become runtime, ToolExecutor integration, planners, workflow engines, projection mutation, truth arbitration, provider calls, execution, verification, refresh, repair, or language-as-truth by default.

### 6. Completed findings, negative findings, and audit memory

`docs/architectural_findings_preservation.md` owns preservation of completed findings, negative findings, rejected concepts, deferred concepts, and durable historical conclusions. It states that implementation not justified is a valid outcome and should be recorded as architecture knowledge, not incomplete work.

This is one of the strongest counterweights to the operator's implicit expectation. Mature audit conclusions often terminate in preservation, not implementation. Their purpose is to prevent rediscovery and architecture drift.

### 7. Investigations, gap analyses, slice reports, pressure artifacts, and methodology reconciliations

The representative investigation/audit family repeatedly uses metadata and scope language such as documentation-only, audit-only, observation-only, not runtime proposal, not schema proposal, not implementation proposal, and no runtime changes. For example, `docs/work_recognition_reality_audit.md` explicitly says it is an observational audit only and not a reconciliation, frontier, taxonomy, runtime, schema, classifier, or implementation proposal.

These artifacts preserve evidence, pressure, reconstruction, uncertainty, and bounded conclusions. Their maturity means they are better at their repository responsibility, not that they are queued for automatic implementation.

## Runtime-owned responsibilities

The runtime-owned side is also well evidenced.

`README.md` says Seed currently owns the knowledge path around scoped observation intake, evidence preservation, claim normalization, fact support, relationship and entity-type projection, contradiction/confidence/staleness/graph-issue characterization, read-only state/support/explanation surfaces, and capability-gap resolution as downstream recommendation.

`IMPLEMENTATION.md` lists implemented runtime capabilities: event ledgers, deterministic state projection, observation pipelines, facts/evidence, projection store, read-only ingestion examples, operator queries, capability catalog, recommendation ranking, policy metadata, and runtime loop behavior.

It also marks boundaries:

- Seed does not execute host commands.
- Seed does not own internal workflow execution.
- Seed does not schedule jobs, retry work, handle secrets, or replace external executors.
- ActionPlans and HandoffPlans are retained only as quarantined legacy/experimental or side-path artifacts, and remain non-executable.
- Execution remains delegated to external providers.

Thus runtime artifacts own implementation-backed behavior. They do not own every mature repository artifact, nor do they receive automatic authority from documentation maturity.

## Why documentation-owned responsibilities are not implementation-owned

The repository gives several recurring reasons.

### Reason 1: Their outputs are authority, orientation, provenance, or preservation, not runtime state

A documentation map routes. A status document owns currentness. A preservation document preserves historical findings. An audit records observed evidence and scope. A frontier preserves unsettled pressure. These outputs support repository competency but do not require event appends, projection mutation, fact promotion, provider calls, or execution.

### Reason 2: Mature negative findings intentionally block implementation drift

`docs/architectural_findings_preservation.md` preserves repeated rejections of engines, universal formatters, runtime integration, ToolExecutor integration, and parallel truth systems. The maturity of those findings makes implementation less justified, not more justified.

### Reason 3: Documentation authority is scoped by role

`docs/documentation_authority_reconciliation.md` explicitly separates navigation authority, orientation authority, canonical architecture authority, state authority, preservation authority, status/frontier authority, roadmap authority, scoped reconciliation authority, vocabulary authority, and audit/characterization authority. A runtime owner would collapse those roles unless a concrete implementation need and ownership boundary existed.

### Reason 4: Repository prose is language-bearing evidence, not executable authority

`docs/documentation_prose_as_language_bearing_source_reconciliation.md` directly answers the future prose-reading case: documentation can be observed, cited, interpreted, compared, routed, accepted, rejected, superseded, scoped, or preserved. It does not become an executable command path by being prose.

### Reason 5: Implementation evidence remains the authority for implemented behavior

The repository repeatedly warns that presentation vocabulary or documentation language does not automatically become repository knowledge or runtime truth. Runtime behavior must be implementation-backed. Documentation can support claims about what the repository says; it does not by itself prove observed runtime state.

## Consumer analysis

### Consumers today

Current consumers include:

- **Human operators and contributors**, who use README, docs maps, status/frontier documents, roadmaps, ontology, and reconciliations to decide what question is already answered and what work is safe.
- **Automated coding agents**, because `AGENTS.md`, README routing, documentation maps, scoped audits, and preservation documents constrain future changes.
- **Implementation work**, because runtime changes are expected to consult reconciliation chains and boundary documents before changing projection semantics, source authority, or capability behavior.
- **Documentation maintenance**, because lifecycle and authority documents prevent duplicate authority and route currentness to owning surfaces.
- **Future investigations**, because frontiers, pressure artifacts, gap analyses, and slice reports preserve uncertainty and prior evidence.

### Consumers in the future

Future consumers may include:

- **Seed repository-observation or prose-observation paths**, if implemented, consuming documentation as language-bearing repository evidence.
- **Generated documentation or wiki projections**, if bounded by existing documentation authority and lifecycle rules.
- **Future agents or handoff processes**, consuming maps, current work position, frontiers, continuation, and preservation artifacts as activation support.
- **Runtime explanation or source-navigation surfaces**, if they cite repository evidence without converting documentation into truth or execution.

The future consumer set can expand without changing ownership. A new consumer does not imply that the consumed artifact becomes runtime-owned.

## Counterexamples searched

The investigation actively searched for evidence that mature artifacts must eventually become runtime implementation, that documentation is only temporary scaffolding, or that repository artifacts lose purpose once implementation exists.

### Counterexample class 1: Mature artifact eventually becoming runtime

Some implementation exists after earlier architectural work. `IMPLEMENTATION.md` shows many concepts have runtime realization: evidence, facts, projection, event ledgers, observation pipelines, catalogs, capability recommendations, and read-only query surfaces.

However, this is not evidence that every mature artifact must become runtime. The same implementation summary preserves non-executable handoff boundaries, quarantines legacy plans, and delegates actual execution. `docs/ontology.md` explicitly allows implementation to realize concepts without making implementation vocabulary exhaustive of ontology.

Conclusion: partial implementation of selected responsibilities exists, but no general rule of inevitable promotion was found.

### Counterexample class 2: Documentation only as temporary scaffolding

No sufficient evidence was found. The opposite is stronger: documentation lifecycle states include reference, historical, superseded, archived, and deprecated records retained for provenance. `docs/architectural_findings_preservation.md` says completed audit sequences should be recorded as settled architectural memory, not open implementation backlog.

Conclusion: repository evidence rejects the idea that documentation is merely temporary scaffolding.

### Counterexample class 3: Repository artifacts losing purpose after implementation exists

No sufficient evidence was found. Implementation can coexist with repository artifacts that own vocabulary, boundary reasoning, provenance, negative findings, and currentness. `README.md` still routes boundary-sensitive architecture work through foundational reconciliation chains even though runtime implementation exists.

Conclusion: implementation does not erase repository artifact purpose.

### Counterexample class 4: Documentation prose becoming executable when Seed can read it

No sufficient evidence was found. The prose-as-source reconciliation explicitly distinguishes documentation artifacts from executable commands. Natural-language reconciliation treats language as observation and interpretation as candidate derivation, not verification, authority, command execution, or policy.

Conclusion: prose-reading would add observation/interpretation consumption, not automatic ownership transfer.

## Supported conclusions

1. **Yes, the repository has recovered a distinction between repository artifacts and runtime artifacts.** The distinction is responsibility-based: repository artifacts preserve, route, reconcile, audit, characterize, sequence, and constrain; runtime artifacts implement observation, evidence, projection, read-only views, capability recommendation, policy metadata, and bounded response behavior.

2. **Many responsibilities intentionally remain documentation-owned.** These include constitutional thesis, ontology vocabulary, documentation navigation, authority/lifecycle roles, current status/frontier, roadmap sequencing, findings preservation, negative findings, investigations, gap analyses, pressure preservation, slice reports, and methodology reconciliation.

3. **Those responsibilities are not implementation-owned because their purpose is repository competency support.** They guide humans, agents, and future implementation work; preserve provenance and uncertainty; avoid duplicate authority; and prevent repeated architecture drift. They do not require runtime mutation, event-ledger writes, provider execution, projection changes, or command routing.

4. **Current consumers are humans, agents, documentation maintainers, implementation workers, and future investigations.** The repository already treats maps, status, preservation records, reconciliations, and frontiers as consumed surfaces.

5. **Future consumers may include Seed itself if prose/repository observation is implemented.** That would not automatically transfer artifact ownership. It would make documentation a source artifact observed under source, authority, and interpretation boundaries.

6. **If Seed eventually reads prose, ownership changes only if a later, implementation-backed repository decision changes ownership.** Prose-reading itself changes consumption, not constitutional ownership.

7. **The constitutional boundary is:**

```text
repository support preserves and constrains architectural knowledge;
runtime execution implements bounded behavior over observations, evidence,
claims, projections, policies, recommendations, and responses;
repository prose does not become runtime authority merely by being mature,
current, imperative, or readable.
```

8. **There is sufficient evidence to recognize the distinction as a stable architectural principle**, with one caveat: the exact term pair "Repository Artifact / Runtime Artifact" is not yet established as canonical vocabulary in the reviewed files. The principle is strongly present; the label is newly characterized here.

## Unsupported conclusions

The investigation does **not** support these conclusions:

- Every mature repository artifact should become runtime implementation.
- Constitution, ontology, roadmap, frontiers, audits, investigations, or slice reports are incomplete until executable.
- Documentation should be moved into runtime, executed as markdown, interpreted as governance, or duplicated into a planner.
- Runtime should become the default home for architectural memory, boundary reasoning, negative findings, or roadmap currentness.
- Prose-reading would make documentation an operator command stream.
- Presentation vocabulary alone is repository knowledge or runtime truth.
- Repository artifacts lose purpose when corresponding implementation exists.

## Confidence

**High** that the repository already distinguishes repository competency artifacts from runtime behavior artifacts.

**High** that Constitution, Ontology, Roadmap, Frontiers, Completion Audits, Implementation Audits, Investigations, Gap Analyses, Slice Reports, Current Work Position, pressure artifacts, and methodology reconciliations can remain durable repository artifacts without being implementation backlog.

**Medium-high** that "Repository Artifact / Runtime Artifact" is a useful name for the distinction. The pattern is well supported, but the label itself is a characterization introduced by this document rather than a pre-existing canonical ontology term.

**Low** support for any claim that all mature artifacts eventually become runtime. Selected concepts can become implementation when a bounded responsibility requires it, but repository evidence rejects automatic promotion.
