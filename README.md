# Seed System

Seed is a claim-centric, knowledge-oriented runtime: it receives observations, preserves evidence, normalizes supportable claims, projects explainable state, and answers questions about what it knows and why.

For Seed's concise architectural thesis and constitutional statement, read [`docs/seed.md`](docs/seed.md). For concise vocabulary, read [`docs/ontology.md`](docs/ontology.md). This README is only the repository orientation surface; the documentation map lives in [`docs/README.md`](docs/README.md).

## What Is Seed?

Seed transforms bounded observations into evidence-backed projected knowledge claims. Its center is the supportable claim: facts are normalized claim forms, relationships are normalized connection claims, and projections communicate selected knowledge rather than becoming authority.

Natural language can be treated as observation of communicative acts. It may strongly support claims about what a speaker requested, asserted, forbade, or prioritized while remaining weak or irrelevant as direct support for what is true in the environment. LLMs and other interpreters may derive candidate meaning from language, but they are not architectural authority.

Seed does not begin with truth. It begins with observation, records provenance, normalizes justified claims, connects justified relationships, and selects explainable projections.

## What Does Seed Own?

Seed currently owns the knowledge path around:

* observation intake from scoped sources;
* evidence preservation and provenance;
* claim normalization, fact support, and support aggregation;
* relationship and entity-type projection;
* contradiction, confidence, staleness, and graph-issue characterization;
* read-only state, impact, support, and explanation surfaces;
* capability-gap resolution as downstream recommendation over projected knowledge.

The current implementation is primarily Python and includes:

* `seed_runtime/` — runtime domain models, projection, observations, evidence, state views, policy, capability inventory, recommendations, and supporting services;
* `tests/` — executable coverage for the implemented behavior and architecture invariants;
* `docs/` — architectural thesis, navigation, reconciliations, vocabularies, audits, and status documents;
* `capability_catalog/`, `predicate_catalog/`, `relationship_catalog/`, and `entity_type_catalog/` — checked-in catalog data used by the runtime;
* `scripts/` and `toolkits/` — local scripts and toolkit examples around the runtime boundary.

## What Does Seed Not Own?

Seed is not:

* a planner;
* a workflow engine;
* a reasoning engine;
* an orchestration framework;
* an autonomous execution platform;
* a provider-availability proof system;
* a host mutation or repair system.

Capability handling is downstream of projected knowledge. A capability gap can become a registered-operation candidate or provider recommendation, but that does not imply execution, verification, availability, host mutation, planning, or workflow orchestration.

## Where Do I Start?

For a new contributor, use this short path:

1. [`README.md`](README.md) — repository orientation and current scope.
2. [`docs/seed.md`](docs/seed.md) — concise architectural thesis / constitutional statement.
3. [`docs/ontology.md`](docs/ontology.md) — concise architectural vocabulary and boundaries.
4. [`docs/README.md`](docs/README.md) — documentation navigation map.
5. [`docs/architectural_status_and_next_frontier.md`](docs/architectural_status_and_next_frontier.md) — current status and active frontier.
6. [`docs/architectural_knowledge_map.md`](docs/architectural_knowledge_map.md) — concern map and routing to owning documents.

If you are doing boundary-sensitive architecture work, follow the foundational reconciliation chain from [`docs/README.md`](docs/README.md) and the ontology audit in [`docs/foundational_ontology_reconciliation.md`](docs/foundational_ontology_reconciliation.md) rather than rediscovering or duplicating those findings. Handoff boundaries and continuation alignment are routed from the documentation map and knowledge map. Natural language, attribution, federation, learning, contradiction discovery, and future-claim boundaries have been reconciled and should be treated as stable references for bounded implementation work.

## Current Status

The current active frontier is a return from conceptual reconciliation to bounded implementation work, especially concrete Prometheus observation and projection cleanup. Current status and priority ownership live in [`docs/architectural_status_and_next_frontier.md`](docs/architectural_status_and_next_frontier.md), not in this README.

Documentation maintenance should keep authority boundaries clear and reduce duplication. The authority model for this repository is:

```text
README.md
    repository orientation

docs/seed.md
    concise architectural thesis / constitutional statement

docs/README.md
    documentation navigation authority

docs/ontology.md
    concise architectural vocabulary

reconciliation documents
    architectural case law / boundary reasoning
```

## Running Checks

Install the project in an environment with Python 3.11 or newer and `pydantic` available, then run:

```bash
python -m pytest
```

Use targeted tests while working on a bounded area, and run the full suite before relying on behavior changes.
