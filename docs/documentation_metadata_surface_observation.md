---
doc_type: observation
status: exploratory
domain: documentation observation
defines:
  - documentation metadata surface
  - documentation metadata fact boundary
depends_on:
  - documentation_observation_design.md
  - documentation_observation_frontier.md
  - defines_relationship_reconciliation_audit.md
related:
  - observation_surface_and_blind_spot_audit.md
  - documentation_observation_characterization.md
  - documentation_observation_v0_implementation_characterization.md
introduced_by: implementation-frontier investigation 2026-06-19
---

# Documentation Metadata Surface Observation

## Status And Boundary

Observation only.

This document records whether authored documentation metadata is an observable repository surface.

It does not interpret document prose, classify prose meaning, evaluate document correctness, promote prose claims into facts, create embeddings, propose architecture, or change implementation.

## Repository Evidence

Repository documentation currently contains YAML-like front matter in many Markdown files. The front matter convention visibly uses these fields:

```text
doc_type
status
domain
defines
depends_on
related
introduced_by
```

A repository scan of `docs/**/*.md` on 2026-06-19 observed:

```text
total markdown documents: 384
documents with opening front matter: 115
documents without opening front matter: 269
```

Observed front matter keys and counts:

```text
status: 114
domain: 89
doc_type: 86
related: 82
defines: 50
depends_on: 49
scope: 27
created: 26
introduced_by: 26
authority: 11
title: 10
related_documents: 2
source_plan: 1
```

Among documents that have front matter, commonly missing candidate metadata fields were:

```text
introduced_by missing from 89
depends_on missing from 66
defines missing from 65
related missing from 33
doc_type missing from 29
domain missing from 26
status missing from 1
```

Examples of repository-supported metadata fields appear in `docs/index.md`, including `doc_type`, `status`, `domain`, `defines`, `depends_on`, and `related`.

Examples of older or un-metadataed documentation also remain: `docs/README.md`, `docs/architectural_knowledge_map.md`, `docs/documentation_authority_reconciliation.md`, and `docs/defines_relationship_reconciliation_audit.md` do not begin with front matter.

## Implementation Evidence

`seed_runtime/knowledge/documentation_observation.py` contains deterministic documentation observation helpers that operate on caller-provided text only.

The implementation explicitly separates two paths:

```text
extract_documentation_claims(...)
observe_documentation_metadata(...)
extract_documentation_navigation_relationship_facts(...)
```

Implementation comments and docstrings state that navigation metadata observation parses only YAML front matter and does not read files, inspect the repository, use LLMs, or integrate with runtime/tool execution.

The implementation-supported metadata key set is:

```text
doc_type
status
domain
defines
depends_on
related
```

The list-valued metadata key set is:

```text
defines
depends_on
related
```

`observe_documentation_metadata(...)` returns structural fields:

```text
source_path
has_front_matter
doc_type
status
domain
defines
depends_on
related
```

`extract_documentation_navigation_relationship_facts(...)` emits relationship facts only from front matter. It emits no relationship facts for documents without front matter.

`relationship_catalog/core.json` contains repository relationship support for documentation metadata-derived relationships:

```text
depends_on: document -> document, derived_from_predicates [depends_on]
related_to: document -> document, derived_from_predicates [related]
belongs_to_domain: document -> domain, derived_from_predicates [domain]
defines: document -> concept, derived_from_predicates [defines]
```

`predicate_catalog/core.json` includes `defines` as a durable, multi-valued string predicate.

Tests preserve the boundary that documentation navigation metadata is front matter only, deterministic, caller-text-only, and body prose is ignored for navigation metadata.

## Supported Observations

Supported structural observations include:

```text
document exists
document has opening front matter
document lacks opening front matter
document has supported metadata key
document lacks supported metadata key
document metadata status value
document metadata doc_type value
document metadata domain value
document metadata defines value
document metadata depends_on value
document metadata related value
document metadata reference resolves to a repository path
document metadata reference does not resolve to a repository path
```

Supported relationship observations include:

```text
document belongs_to_domain domain

document defines concept

document depends_on document

document related_to document
```

These observations are structural metadata facts. They do not require interpreting document prose.

## Unsupported Observations

Unsupported observations include:

```text
document prose claim is true
document prose claim is current
document prose claim is authoritative because it appears in prose
document prose implies an architecture relationship
document prose defines a concept unless front matter says so
missing metadata means the document has no prose relevance
missing metadata means the document is obsolete
metadata dependency means the dependency is correct
metadata status means implementation behavior matches the status
```

Unsupported implementation observations include:

```text
introduced_by is parsed by the current documentation metadata observer
scope is parsed by the current documentation metadata observer
created is parsed by the current documentation metadata observer
authority is parsed by the current documentation metadata observer
title is parsed by the current documentation metadata observer
repository-wide documentation metadata ingestion is exposed as a CLI observation source
metadata reference existence validation is currently emitted as a graph issue
```

## Documentation Structure Versus Documentation Prose

Supported distinction:

```text
document metadata fact
    !=
document prose claim
```

Example supported metadata fact shape:

```text
docs/foo.md status active
```

Example unsupported prose-claim fact shape unless separately evaluated by a prose-claim pathway:

```text
docs/foo.md claims RuntimeLoop uses DecisionContextView
```

A metadata field can be observed as authored structure. A prose sentence remains prose unless a separate deterministic claim extractor or support rule evaluates it within its own boundary.

## Preserved Uncertainty

The repository contains both documents with metadata and documents without metadata.

The repository convention appears broader than current implementation support: repository front matter uses `introduced_by`, `scope`, `created`, `authority`, `title`, `related_documents`, and `source_plan`, while current documentation metadata observation supports only `doc_type`, `status`, `domain`, `defines`, `depends_on`, and `related`.

The existence of metadata does not establish document correctness.

The absence of metadata does not establish document irrelevance.

The current implementation supports structural observation from caller-provided text; this document does not claim an implemented repository-wide documentation scanner or validator.
