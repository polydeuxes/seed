# Repository Self Observation Reconciliation

## Scope

This reconciliation asks whether Seed should treat its own repository as a
future knowledge-acquisition domain.

It is documentation only. It does not implement repository scanning, repository
indexing, repository mutation, repository repair, repository management,
repository execution, self-modification, capability execution, tool execution,
`Runtime` integration, `ToolExecutor` integration, provider integration, network
probing, shell execution, subprocess execution, sudo requirements, or
LLM-generated facts.

The current architectural direction remains the Local Observation Roadmap
Reconciliation: enrich Seed through the existing
`Observation -> Evidence -> Fact -> Projection` path and keep observation,
inference, verification, and execution separate.

## Files inspected

Minimum requested sources inspected:

- `README.md`
- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/invariants.md`
- `docs/state.md`
- `docs/reasoning_roadmap.md`
- `docs/knowledge_acquisition_status.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/capability_extension_methodology.md`
- `docs/self_observation_audit.md`

Additional relevant sources inspected:

- `docs/local_observation_roadmap_reconciliation.md`

## Current state

Seed's core documentation already defines a knowledge-first architecture:
observations become evidence-backed facts, projected state becomes explainable,
and capability handling remains downstream of knowledge. The architecture docs
also state that projection views are read-only and must not execute operations,
call providers, run shell commands, mutate hosts, call LLMs, or become separate
state stores.

Seed has already completed several local observation slices that answer what can
be learned from local host evidence. Those slices preserve a recurring boundary:
observation is not management. Observing host identity, mounts, resources,
storage topology, or listening ports does not imply availability, reachability,
health, ownership, orchestration, or permission to act.

The repository now has a parallel knowledge gap. Seed knows increasingly rich
host-local facts, but its projected knowledge does not yet describe Seed itself:
its predicates, entity types, relationships, capabilities, operations,
implementations, providers, tests, invariants, canonical documents, generated
documents, roadmap items, or architecture metadata.

## Existing repository-local knowledge

Repository-local knowledge already exists in several forms, but it is not yet
ordinary Seed knowledge.

| Knowledge area | Current repository form | Current visibility |
| --- | --- | --- |
| Architecture ownership | `__seed_arch__` metadata, architecture docs, invariants | Visible to humans and generated architecture artifacts; not projected as facts |
| Runtime boundaries | `docs/invariants.md`, `docs/architecture.md`, generated graph | Visible as docs/tests/artifacts; not queryable as evidence-backed repository facts |
| Predicate vocabulary | `PredicateCatalog` and related catalog documentation | Visible through catalog mechanisms; not observed as repository self-facts |
| Entity type vocabulary | entity type catalog and rule inventory docs | Visible as metadata; not modeled as repository facts about Seed |
| Relationship vocabulary | relationship catalog and rule inventory docs | Visible as metadata; not modeled as repository facts about Seed |
| Capability metadata | `CapabilityCatalog`, capability docs, capability methodology | Visible as inert metadata and methodology; not self-observed repository structure |
| Registered operations | `ToolRegistry` concepts and runtime docs | Visible as executable inventory boundary; must not be conflated with observation |
| Tests and invariant checks | test modules and invariant docs | Visible to developers/CI; not represented as facts with evidence |
| Canonical documents | promoted docs and reconciliation docs | Visible by convention; no generated canonical documentation index |
| Roadmap items | roadmap and reconciliation docs | Visible in documentation; not projected as roadmap entities or facts |
| Generated documents | architecture generated artifacts | Visible as files; no generated-document entity model or freshness facts |

The strongest existing self-observation asset remains the architecture generator
and generated graph described in `docs/self_observation_audit.md`: a static,
source-attributed architecture artifact with nodes, edges, owners, layers, and
route labels. It is close to repository observation in shape, but it currently
emits documentation artifacts rather than `Observation`, `Evidence`, `Fact`, or
projected relationship records.

## Repository-local knowledge currently visible

Seed can currently inspect or expose repository-local knowledge through
non-observation channels:

- committed documentation;
- generated architecture artifacts;
- source metadata embedded in selected runtime classes;
- deterministic catalog inventories;
- invariant tests and architecture generator tests;
- roadmap and audit documents.

This visibility is useful but fragmented. It supports human review and CI drift
checks, not first-class answers from projected state such as:

- "Which evidence supports `ToolExecutor` as execution owner?"
- "Which document states that `request_tool` must not execute?"
- "Which generated edge says `Runtime.call_tool` reaches `ToolExecutor`?"
- "Which canonical documents define the current knowledge-acquisition frontier?"

## Repository-local knowledge currently invisible

The following knowledge is effectively invisible to Seed's canonical knowledge
path today:

- repository source files as observation subjects;
- architecture graph nodes as entities;
- graph edges as projected relationships;
- owner labels as evidence-backed facts;
- route labels as evidence-backed relationships;
- invariant statements as expected facts or documentation facts;
- documentation pages as canonical, generated, historical, or audit entities;
- tests as evidence that an invariant is checked rather than evidence that the
  invariant is true;
- predicate, entity type, relationship, inference, and capability catalog entries
  as repository-local facts about Seed's knowledge model;
- roadmap items as knowledge-acquisition entities with status and boundaries;
- generated artifacts as generated-document entities with provenance.

The invisibility is architectural, not accidental. Seed lacks repository source
contracts, repository predicates, repository entity types, repository
relationship types, source-confidence rules, and a projection design for turning
repository evidence into ordinary state.

## Architectural fit

Repository self-observation is a meaningful future knowledge-acquisition domain
because it can follow the same shape as host-local observation without becoming
self-management:

```text
Repository-local read-only source
-> Observation
-> Evidence
-> Fact
-> Relationship / Entity Type
-> Projection
-> Explanation / Query
```

Potential examples:

| Repository evidence | Possible fact or relationship | Boundary |
| --- | --- | --- |
| Generated graph node for `ToolExecutor` | `ToolExecutor architecture_owner registered_tool_execution` | Ownership fact only; not execution |
| Generated graph edge from `Runtime` to `ToolExecutor` | `Runtime routes_to ToolExecutor` with route `call_tool` | Route description only; not route invocation |
| Invariant documentation | `docs/invariants.md documents call_tool_only_path` | Documentation fact only; not enforcement |
| Predicate catalog entry | `PredicateCatalog defines predicate hostname` | Catalog structure only; not new predicate creation |
| Test file containing invariant checks | `tests/test_architecture_invariants.py checks invariant runtime_loop_absent` | Test inventory only; not verification of runtime state |
| Roadmap document section | `reasoning_roadmap contains self_observation future_direction` | Roadmap metadata only; not implementation authorization |

The domain fits best when repository facts are treated as descriptive,
source-attributed claims about committed artifacts. They should support
explanation and inventory, not runtime behavior.

## Potential future self-observation domains

Future repository self-observation could naturally include the following domains
if each domain receives explicit source, predicate, relationship, provenance, and
boundary design before implementation.

| Domain | Fit | Notes |
| --- | --- | --- |
| Predicates | Strong | Observe predicate catalog entries and mapping declarations as repository metadata. Do not add or infer predicates automatically. |
| Entity types | Strong | Observe entity type catalog entries and documentation references. Do not mutate the catalog. |
| Relationships | Strong | Observe relationship catalog entries and generated architecture edges. Do not infer operational reachability. |
| Capabilities | Strong with guardrails | Observe capability metadata as inert catalog knowledge. Do not verify, execute, or recommend providers merely from repository presence. |
| Operations | Moderate with strict boundaries | Observe registered-operation definitions or contracts as inventory. Do not execute or treat presence as availability. |
| Implementations | Moderate | Observe source-backed components, class metadata, and layers. Do not make quality, health, or correctness claims without separate evidence. |
| Providers | Moderate with strict boundaries | Observe provider recommendation metadata only. Do not contact providers or assert availability. |
| Tests | Strong as inventory | Observe test files, named checks, or invariant coverage. Do not treat a test's existence as proof that architecture is correct. |
| Invariants | Strong | Observe invariant statements and expected architecture boundaries. Enforcement remains separate tests or future checks. |
| Canonical documents | Strong | Observe canonical documentation pages and promoted reconciliation docs. Do not rewrite or promote documents automatically. |
| Generated documents | Strong | Observe generated artifacts, generator provenance, and declared generated status. Do not regenerate as part of observation. |
| Roadmap items | Strong | Observe roadmap items, non-goals, and recommended next steps. Do not convert roadmap items into execution plans. |
| Architecture metadata | Strong | Observe `__seed_arch__` nodes, layers, owners, routes, and edges. Do not turn metadata into active routing. |

## Boundaries to preserve

Repository self-observation must preserve the same boundary language used by
local observation:

- observing repository structure must not imply repository modification;
- observing architecture must not imply architecture mutation;
- observing invariants must not imply invariant enforcement;
- observing tests must not imply successful verification;
- observing capabilities must not imply capability execution;
- observing operations must not imply operation availability;
- observing providers must not imply provider reachability or integration;
- observing generated artifacts must not imply regeneration;
- observing roadmap items must not imply orchestration or scheduling;
- observing implementation metadata must not imply implementation correctness;
- observing documentation must not imply automatic canonicalization;
- observing drift must not imply self-repair.

A future repository observation model must remain:

- read-only;
- evidence-backed;
- projection-backed;
- knowledge-first;
- deterministic where possible;
- source-attributed;
- separate from inference, verification, execution, provider interaction, and
  mutation.

## Existing documentation that already touches this concept

Existing documents already provide strong conceptual coverage:

- `README.md` defines the knowledge-first flow and separates capability handling
  from execution.
- `docs/architecture.md` defines Runtime, ToolExecutor, projected State,
  Evidence Graph, and projection-view boundaries.
- `docs/architecture_principles.md` defines ownership, externalization,
  logic-first, and execution-boundary principles.
- `docs/invariants.md` states runtime, execution, projection, capability,
  observation, and verification invariants.
- `docs/reasoning_roadmap.md` already has a self-observation section that
  describes repository AST observations flowing to facts and relationships while
  forbidding self-mutation.
- `docs/self_observation_audit.md` inventories current repository knowledge
  assets and identifies missing concepts.
- `docs/local_observation_roadmap_reconciliation.md` supplies the currently
  accepted pattern for read-only local knowledge acquisition.
- `docs/knowledge_classification_vocabulary.md` classifies knowledge by
  identity, configuration, topology, description, and state without changing
  runtime behavior.
- `docs/capability_extension_methodology.md` provides the gap-to-narrowest-fact
  review process that repository self-observation should follow.

## Ownership considerations

Repository self-observation should have a future owner distinct from runtime,
execution, provider, and catalog mutation ownership.

Recommended ownership model:

| Concern | Future owner shape | Must not own |
| --- | --- | --- |
| Repository source reading | A read-only repository observation source, if later approved | Runtime routing, execution, mutation, shell commands |
| Repository evidence normalization | Observation ingestion / explicitly named repository normalizer | Predicate invention at runtime, provider calls |
| Repository fact projection | Existing StateProjector path after ledger-backed facts exist | Event creation outside ingestion, enforcement |
| Repository architecture metadata | Architecture metadata/generator conventions | Runtime behavior or operation execution |
| Repository documentation inventory | Documentation inventory design, likely generated/read-only | Canonicalization, promotion, rewriting |
| Repository invariant inventory | Invariant docs/tests and future read-only reports | Auto-repair or enforcement beyond explicit tests |
| Capability metadata about Seed | Existing CapabilityCatalog as inert metadata | Verification, provider reachability, execution |

`Runtime` should not own repository observation. `ToolExecutor` should not own
repository observation. `EventLedger` should continue to own append-only events
if repository observations are later ingested. `ProjectionStore` should continue
to own cached projected-state snapshots, not repository scans. The ownership
question should be answered before any implementation is proposed.

## Knowledge-classification fit

The existing knowledge classification vocabulary can be extended conceptually to
repository knowledge without changing projection behavior.

| Repository knowledge class | Analogy | Examples | Caution |
| --- | --- | --- | --- |
| Repository identity | Identity | repository name, generated artifact identity, canonical document identity | Identity does not imply ownership by Seed over mutation. |
| Repository configuration | Configuration | catalog entries, invariant declarations, route metadata, owner labels | Configuration does not imply availability or correctness. |
| Repository topology | Topology | files define classes, components route to services, documents contain sections | Topology does not imply reachability, execution, or management. |
| Repository description | Description | implementation summaries, layers, component summaries | Description does not imply quality, health, or supportability. |
| Repository state | State | generated artifact freshness, test inventory status, roadmap status | State is volatile and must not imply verification or execution. |

This fit is documentation-only. It does not add freshness behavior, scheduling,
context composition, repository scanning, projection changes, or runtime changes.

## Capability-methodology fit

Repository self-observation fits the Capability Extension Methodology if it is
framed as a missing reasoning capability rather than a desired tool.

| Methodology step | Repository self-observation interpretation |
| --- | --- |
| Capability gap | Seed cannot answer first-class questions about its own repository knowledge model. |
| Required question | What repository fact is needed, such as which component owns a behavior or which document states an invariant? |
| Narrowest fact | Use a precise repository fact such as `ToolExecutor architecture_owner registered_tool_execution`. |
| Least-privileged source | Prefer committed generated artifacts, docs, catalogs, or static metadata. |
| Read-only observation | Read only the selected source; do not run commands, mutate files, contact providers, or execute tools. |
| Evidence | Preserve file, line, artifact, generator, and source-payload provenance. |
| Fact | Project only what the evidence directly supports. |
| Inference | Keep ownership reasoning, drift analysis, and coverage conclusions separate from observation. |
| User query | Explain repository facts with evidence and boundaries. |

This means repository self-observation should start with a tiny, source-backed
fact vocabulary rather than a broad repository index.

## Roadmap implications

Repository self-observation is a meaningful future Knowledge Acquisition domain,
but it should not displace the current Local Observation Roadmap Reconciliation
or pull Seed into Reasoning Expansion, Execution Expansion, Provider Expansion,
or Runtime Expansion.

Recommended roadmap placement:

1. Keep the current host-local observation roadmap as the active sequence.
2. Add Repository Self Observation as a future knowledge-acquisition domain after
   the existing local observation direction remains stable.
3. Treat the first step as documentation/design only, not implementation.
4. Require explicit vocabulary design before any observation source exists:
   repository source type, repository predicates, repository entity types,
   repository relationships, provenance rules, and non-goal tests.
5. Require any future implementation to prove that repository observation does
   not touch `Runtime`, `ToolExecutor`, provider integration, shell execution,
   subprocess execution, network probing, or mutation.

## Recommended smallest next step

The smallest safe next step is a **Repository Observation Source Design**
document, not code.

That design should define only:

1. the narrow initial question Seed should answer about itself;
2. the minimal read-only repository source, likely the generated architecture
   graph or a small explicitly named documentation artifact;
3. the minimal repository entity types;
4. the minimal repository predicates;
5. the minimal repository relationships;
6. evidence provenance rules using file path, line number, generated artifact,
   and source payload boundaries;
7. explicit non-goals stating no scanning implementation, no mutation, no
   execution, no provider interaction, no Runtime integration, no ToolExecutor
   integration, no LLM-generated facts, and no self-repair.

A good first design target would be one question:

> What evidence says which component owns a named architecture behavior?

A deliberately narrow answer could use existing generated architecture metadata
to describe owner labels for a small set of components, without indexing the
whole repository and without changing runtime behavior.

## Reconciliation finding

Repository self-observation is architecturally meaningful, but only as a future
read-only knowledge-acquisition domain. Seed should be able to learn facts about
its own repository for explanation and inventory in the same way it learns facts
about the local host: from bounded evidence, through explicit facts, into
projection, with strict boundaries around what the facts do not imply.

The correct framing is:

```text
Seed observes repository evidence to explain what Seed knows about itself.
```

The incorrect framings are:

```text
Seed modifies itself.
Seed repairs itself.
Seed manages its repository.
Seed executes capabilities because it observed them.
Seed verifies architecture because it observed tests or invariants.
Seed routes runtime behavior from repository metadata.
```

Therefore, Repository Self Observation should be recognized as a future
Knowledge Acquisition domain, with ownership and vocabulary designed before any
implementation and with documentation-only status for this phase.
