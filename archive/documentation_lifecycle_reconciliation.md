# Documentation Lifecycle Reconciliation

## 1. Purpose and scope

This document is a documentation-only reconciliation for safe archival,
provenance preservation, and canonical document control in Seed.

It defines how Seed should distinguish active documentation from historical
records without deleting documents, losing findings, or creating another broad
architecture theory document.

In scope:

- identifying current canonical, navigation-only, preservation, active,
  superseded, historical, and archive-candidate documentation roles;
- proposing the smallest lifecycle vocabulary Seed needs;
- proposing required metadata for documents before archival or supersession;
- proposing safe archival and supersession rules;
- proposing a low-churn README/map maintenance rule;
- proposing a candidate next PR plan.

Out of scope:

- moving, deleting, renaming, or rewriting existing documents in this change;
- modifying production code, tests, runtime behavior, event schemas, projection
  schemas, providers, policy behavior, acquisition logic, or generated artifacts;
- deciding every document's final archive destination;
- creating a new architecture registry, runtime document database, or governance
  subsystem.

## 2. Current documentation problem

Seed's documentation has accumulated several overlapping document families:

- canonical architecture documents;
- navigation maps and reading-order documents;
- roadmap and status boards;
- vocabularies and methodologies;
- characterization, audit, inventory, and reconciliation chains;
- preservation and frontier handoffs;
- generated architecture artifacts;
- historical RuntimeLoop-era and quarantine records.

The risk is not that old documents exist. The risk is that old documents can
look equally authoritative to new readers after their conclusions have been
promoted or superseded. A reader can encounter multiple maps, roadmaps, status
summaries, and reconciliations that each sound current but were written for
different lifecycle roles.

The current failure mode is therefore **duplicate authority**, not lack of prose.
Seed needs lifecycle labels, provenance pointers, and supersession links before
it needs file moves.

## 3. Existing navigation/preservation surfaces

Seed already has several useful surfaces, but their responsibilities overlap:

| Surface | Current role | Lifecycle finding |
| --- | --- | --- |
| `docs/README.md` | Entry point and recommended reading order. | Should be navigation-only plus a small canonical-entry list; it should not duplicate volatile status tables. |
| `docs/architectural_knowledge_map.md` | Lightweight map of concerns, findings, rejected concepts, and frontiers. | Navigation/reference only; it explicitly should not become the source of truth. |
| `docs/architectural_findings_preservation.md` | Compact preservation of completed audit findings, negative findings, paused chains, and frontier handoff. | Historical-finding preservation surface; should remain active as a preservation/reference document. |
| `docs/architectural_status_and_next_frontier.md` | Current major-concern status and next-frontier reconciliation. | Active status/frontier document while Knowledge Acquisition expansion remains the frontier. |
| `docs/reasoning_roadmap.md` | Active roadmap and historical concern evolution. | Active roadmap, but should point to lifecycle metadata for completed/superseded chains instead of absorbing every detail. |
| `docs/documentation_architecture_audit.md` | Inventory and classification audit for documentation architecture. | Historical audit/reference; its durable rules should be promoted into lifecycle metadata before archival. |
| `docs/canonical_documentation_reconciliation.md` | Prior reconciliation of canonical/generated/roadmap/status/historical/archive-candidate categories. | Active reference for this lifecycle pass, then superseded by an adopted lifecycle index or metadata convention. |
| Recent `*_reconciliation.md` documents | Boundary-specific reconciliation records. | Usually active reference until their conclusions are promoted; then historical or superseded with provenance retained. |

These surfaces should not all compete to be the map. The README should route;
the architectural knowledge map should orient; preservation should keep settled
findings discoverable; status/roadmap documents should describe the current
frontier; reconciliation documents should preserve decision provenance.

## 4. Proposed document lifecycle states

Seed should use the smallest vocabulary that separates current authority,
reader navigation, historical evidence, and unsafe-to-delete provenance.

### Required states

| State | Meaning | May be canonical authority? | May be archived? |
| --- | --- | --- | --- |
| `canonical` | Defines Seed's current accepted architecture, ownership, invariants, state semantics, or vocabulary. | Yes. | No, unless replaced by another canonical document. |
| `active` | Mutable current-planning or current-status document. Examples: roadmap, status board, frontier handoff. | Sometimes, but only for current status, not durable architecture. | No, while active. |
| `reference` | Useful orientation, map, preservation, methodology, or background document that points to canonical sources. | No, unless explicitly scoped to vocabulary/methodology. | Only after replacement and link preservation. |
| `historical` | Preserves findings, audit evidence, design rationale, negative findings, rejected approaches, or old context. | No. | Already archival in meaning; file may remain in place. |
| `superseded` | Replaced by a newer document for current guidance while retained for provenance. | No. | Yes, after metadata is complete. |
| `archived` | Intentionally retained outside the active reading path for historical traceability. | No. | N/A; do not delete by default. |
| `deprecated` | Describes a concept, interface, or path that still exists but should not be used as current guidance. | No, except to document the deprecation itself. | Only after a current replacement explains the boundary. |

### Avoid additional states for now

Do not add separate states such as `draft`, `candidate`, `quarantined`,
`frontier`, `inventory`, `audit`, `map`, or `roadmap` as lifecycle states. Those
are document types or concerns, not lifecycle authority. Put them in `document_type`
or `owner_concern` metadata if needed.

## 5. Required provenance metadata

Before a document is archived, marked superseded, or removed from the active
reading path, it should carry a compact metadata header. YAML front matter is the
lowest-friction format because it is readable, diffable, and does not require a
new directory layout.

Required fields:

```yaml
---
status: canonical | active | reference | historical | superseded | archived | deprecated
owner_concern: knowledge_acquisition | knowledge_integrity | knowledge_selection | response | architectural_findings | documentation_lifecycle | runtime_architecture | capability | policy | other
created: YYYY-MM-DD
updated: YYYY-MM-DD
supersedes: []
superseded_by: []
related_documents: []
provenance:
  summary: "Why this document exists and what evidence or prior work it preserves."
  inspected_documents: []
  source_commits: []
archival_reason: null
canonical_replacement: null
---
```

Required before archival or supersession:

- `status` must be set to `superseded`, `historical`, `archived`, or
  `deprecated` as appropriate.
- `superseded_by` must name the current replacement when current guidance moved
  elsewhere.
- `canonical_replacement` must be set if the document previously made canonical
  claims.
- `archival_reason` must explain why it is safe to remove the document from the
  active reading path.
- `provenance.summary` must preserve what the document contributed.
- `related_documents` must include preservation, roadmap, status, or canonical
  documents that now carry its durable conclusions.

Optional fields for later, if useful:

- `document_type`: `map`, `roadmap`, `status`, `audit`, `reconciliation`,
  `characterization`, `vocabulary`, `methodology`, `inventory`, `generated`.
- `archive_batch`: an identifier for a later migration PR.
- `lineage_note`: short prose for complex supersession chains.

## 6. Safe archival rules

Archival means removing a document from the active reading path or moving it to
an archive directory in a later PR. It does not mean deletion.

Rules:

1. **No deletion by default.** Historical documents preserve evidence, rejected
   paths, negative findings, and why-not decisions.
2. **No archive without replacement for canonical claims.** If a document defines
   current architecture, ownership, invariants, vocabulary, status, or roadmap
   direction, those claims must be represented in a canonical, active, or
   reference replacement before archival.
3. **Archive after promotion, not before.** First promote durable conclusions to
   canonical/status/vocabulary/methodology surfaces; then mark the source as
   `superseded` or `historical`; then optionally move it.
4. **Preserve negative findings.** Rejected engines, parallel truth systems,
   Runtime/ToolExecutor overreach, and unjustified implementation findings must
   remain discoverable through a preservation or canonical boundary document.
5. **Preserve exact inventories until summarized.** Detailed audits and
   inventories can be archived only after their unique lists, edge cases, or
   quarantine rationale are represented elsewhere or explicitly declared no
   longer active.
6. **Generated artifacts are not archived manually.** Generated architecture
   outputs should be regenerated or removed only through the generation policy,
   not through documentation archival.
7. **Use two-step migration for moves.** First add lifecycle metadata in place;
   then, in a separate PR, move only documents with complete metadata and stable
   replacements.
8. **Keep links survivable.** If files move later, leave a stub or update every
   active link in README, maps, status, roadmap, and related documents.

## 7. Supersession rules

Supersession is a claim about current authority, not a claim that the older
document was wrong.

A document may declare `superseded` when:

- its durable conclusions were promoted to a canonical, active, vocabulary,
  methodology, or preservation surface;
- a newer reconciliation resolves the same concern more completely;
- its current-status claims are stale but its evidence remains useful;
- it describes a path Seed has deprecated or quarantined.

A supersession declaration must include:

- `superseded_by`: one or more replacement documents;
- `canonical_replacement`: the document that owns current authority, if any;
- `archival_reason`: why the old document should no longer be in the active
  reading path;
- a short top-of-document note visible without scanning the whole file.

Recommended top note:

```markdown
> Lifecycle note: This document is superseded for current guidance by
> `docs/example_replacement.md`. It is retained for provenance, historical
> findings, and decision traceability. Do not treat it as canonical unless a
> cited replacement points back to a specific section.
```

Supersession can be many-to-one or one-to-many. For example, a broad audit might
be superseded by `docs/architecture.md` for ownership, `docs/invariants.md` for
non-negotiable boundaries, and `docs/architectural_findings_preservation.md` for
negative findings.

## 8. Proposed directory or metadata strategy

Use metadata first. Do not move files yet.

Recommended strategy:

1. Add lifecycle metadata headers to high-value documents in place.
2. Add a compact lifecycle section to `docs/README.md` that explains the states
   and links to this reconciliation.
3. Add a small `docs/documentation_lifecycle_index.md` only if metadata alone
   proves insufficient for navigation. The index should be tabular and factual,
   not another architecture essay.
4. After one or more metadata passes, optionally create archive directories and
   move only well-labeled documents.

Potential directories for a later migration:

```text
docs/
  canonical/          # optional; only if Seed chooses to move canonical docs later
  reconciliations/    # optional; risky because many links already assume flat docs/
  history/            # optional; historical docs still relevant for provenance
  archive/            # optional; documents intentionally outside active reading path
```

Do not introduce these directories in the first lifecycle PR. The flat `docs/`
layout has many existing links, and moves would create churn before authority is
settled. Metadata headers are enough to start reducing documentation load.

If directories are introduced later, prefer:

- `docs/archive/` for documents intentionally removed from active reading;
- `docs/history/` only if Seed wants a distinction between historical records
  still commonly cited and colder archive records;
- no `docs/canonical/` move unless the project is willing to update all links and
  treat canonical files as a small curated set.

## 9. Minimal README/map maintenance rule

`docs/README.md` should avoid becoming stale by obeying a strict rule:

> The README lists only entry points and lifecycle policy, not the full state of
> every concern.

Required README behavior:

- link to the canonical entry set;
- link to the active roadmap/status/frontier documents;
- link to preservation/history surfaces;
- link to the lifecycle states and metadata convention;
- avoid embedding volatile status tables, detailed concern inventories, or long
  lists of completed audits;
- require any PR that adds or supersedes a broad map/status/roadmap/preservation
  document to update either the README's entry-point list or the document's own
  lifecycle metadata.

`docs/architectural_knowledge_map.md` should remain a map, not a registry. It
may list the current frame and high-level reading order, but canonical authority
must remain in the underlying documents.

## 10. Candidate next PR plan

Smallest safe next PR sequence:

1. Add lifecycle metadata headers to:
   - `docs/README.md` as `reference`;
   - `docs/architectural_knowledge_map.md` as `reference`;
   - `docs/architectural_findings_preservation.md` as `reference` or
     `historical` with active preservation role;
   - `docs/architectural_status_and_next_frontier.md` as `active`;
   - `docs/reasoning_roadmap.md` as `active`;
   - `docs/canonical_documentation_reconciliation.md` as `reference` or
     `superseded` by this lifecycle reconciliation after adoption;
   - `docs/documentation_architecture_audit.md` as `historical`.
2. Add a short lifecycle explanation and link to this document from
   `docs/README.md`.
3. Add top-of-document lifecycle notes to the safest superseded/historical
   candidates, without moving files.
4. Promote any unique current claims from archive candidates into canonical,
   active, vocabulary, methodology, or preservation surfaces.
5. In a later PR, optionally create `docs/archive/` and move only documents with
   complete metadata, replacement links, and updated inbound links.

First archive candidates after metadata and promotion checks:

- RuntimeLoop-era responsibility/quarantine records whose current conclusions
  are already represented in architecture/invariants/logic-model documents;
- older roadmap reconciliation/audit records whose active items are represented
  in `docs/reasoning_roadmap.md` and `docs/knowledge_acquisition_status.md`;
- completed audit records whose only remaining role is provenance and whose
  negative findings are represented in
  `docs/architectural_findings_preservation.md`.

## 11. Rejected solutions

Rejected for now:

- **Deleting old documents.** This would destroy provenance and make negative
  findings rediscoverable the hard way.
- **Moving many files immediately.** This would create link churn before Seed has
  lifecycle metadata and replacement pointers.
- **Creating a broad architecture registry.** Prior findings repeatedly reject
  parallel truth systems and architecture databases; documentation lifecycle can
  be handled with headers and small navigation rules.
- **Making `docs/README.md` a complete inventory.** It would go stale quickly and
  duplicate maps/status documents.
- **Treating every reconciliation as canonical forever.** Reconciliations are
  provenance records unless explicitly promoted into canonical architecture,
  active roadmap/status, vocabulary, methodology, or preservation surfaces.
- **Using directory location as the only authority signal.** Directories help
  browsing but do not preserve supersession, provenance, or replacements.
- **Adding many lifecycle states.** More states would increase load without
  solving duplicate authority.

## 12. Direct answer

### 1. Which documents are currently canonical?

Current canonical authority should be the smallest active set:

- root `README.md` for the top-level Seed thesis and entry orientation;
- `docs/architecture.md` for current architecture and ownership;
- `docs/architecture_principles.md` for current architecture direction, until
  overlap is consolidated;
- `docs/invariants.md` for non-negotiable architectural invariants;
- `docs/state.md` for projected state, evidence graph, contradiction, and
  confidence semantics;
- `docs/logic_model.md` for logic-layer model and drift guidance;
- `docs/function_blocks.md` for functional decomposition;
- active vocabularies and methodologies where scoped to their concern;
- generated architecture artifacts as generated, code-derived authority, not
  hand-authored canonical prose.

`docs/README.md` inside the docs directory should be treated as a navigation
entry point, not a canonical architecture source.

### 2. Which documents are navigation-only?

Navigation-only or navigation-first documents include:

- `docs/README.md`;
- `docs/architectural_knowledge_map.md`;
- any future lifecycle index;
- map/frontier documents when they point to underlying sources rather than own
  current authority.

### 3. Which documents preserve historical findings?

Historical-finding preservation is primarily carried by:

- `docs/architectural_findings_preservation.md`;
- `docs/architectural_findings_characterization.md`;
- `docs/architectural_findings_vocabulary.md`;
- `docs/architectural_findings_reconciliation.md`;
- completed `*_audit.md`, `*_inventory.md`, `*_characterization.md`, and
  `*_reconciliation.md` records after their conclusions are promoted.

### 4. Which documents are superseded by newer reconciliation work?

Likely superseded or ready to mark historical after promotion checks:

- older broad documentation audits by this lifecycle reconciliation for document
  lifecycle policy;
- older roadmap/status reconciliations by `docs/reasoning_roadmap.md`,
  `docs/architectural_status_and_next_frontier.md`, and
  `docs/architectural_findings_preservation.md` for current frontier framing;
- older boundary-specific audits when later vocabulary/reconciliation documents
  own the current terminology and decisions;
- RuntimeLoop-era planning/execution documents where current architecture,
  invariants, and logic-model documents already carry the active boundary.

Do not mark a document superseded merely because it is old. Mark it superseded
only when the replacement document is named and provenance is retained.

### 5. Which documents should remain active?

Remain active now:

- canonical architecture set listed above;
- `docs/reasoning_roadmap.md`;
- `docs/knowledge_acquisition_status.md`;
- `docs/architectural_status_and_next_frontier.md` while its frontier remains
  current;
- active vocabularies and methodologies;
- `docs/architectural_findings_preservation.md` as a preservation/reference
  surface;
- recent reconciliation documents until their durable conclusions are promoted
  or explicitly superseded.

### 6. Which documents can be archived safely?

A document can be archived safely only when:

- it has metadata;
- it has a named replacement for current claims;
- its unique findings are promoted or explicitly preserved;
- inbound links are updated or a stub remains;
- the archive action is separate from broad rewrites.

The first safe candidates are historical RuntimeLoop/quarantine records and
older roadmap/audit records whose current conclusions already exist in canonical
or active surfaces.

### 7. What metadata is required before archiving?

Required metadata: `status`, `owner_concern`, `created`, `updated`,
`supersedes`, `superseded_by`, `related_documents`, `provenance`,
`archival_reason`, and `canonical_replacement`.

### 8. How should archived docs preserve provenance?

Archived docs should preserve provenance by retaining original content,
recording why the document existed, linking to source and replacement documents,
recording supersession direction, preserving negative findings, and avoiding
silent deletion or unlinked file moves.

### 9. How should docs declare supersession?

Use both YAML metadata and a visible top-of-document lifecycle note. The note
should name the replacement, state that the old document is retained for
provenance, and warn readers not to treat it as current guidance except where a
replacement explicitly cites it.

### 10. How should docs/README.md avoid becoming stale again?

`docs/README.md` should only list entry points and lifecycle policy. It should
not contain broad status tables, full audit inventories, or detailed frontier
matrices. PRs that add or supersede broad maps/status/roadmaps must update either
README entry points or document metadata.

### 11. Should Seed use directories such as docs/canonical, docs/reconciliations, docs/archive, docs/history, or is a metadata header enough?

Metadata headers are enough for the first lifecycle pass. Directories can come
later, but only after documents have explicit status, replacement, and provenance
fields. If directories are introduced, start with `docs/archive/` for cold
historical records; avoid moving canonical files until link churn is justified.

### 12. What is the smallest documentation lifecycle vocabulary needed?

Use seven states:

- `canonical`
- `active`
- `reference`
- `historical`
- `superseded`
- `archived`
- `deprecated`

Do not add more lifecycle states until these fail.

## Closing answers

### What should become canonical now?

The canonical set should remain small: root `README.md`, `docs/architecture.md`,
`docs/architecture_principles.md`, `docs/invariants.md`, `docs/state.md`,
`docs/logic_model.md`, `docs/function_blocks.md`, scoped active vocabularies and
methodologies, and generated architecture outputs as generated authority.

This lifecycle reconciliation should become a **reference** document for
documentation lifecycle policy, not canonical architecture.

### What should be archived first?

Archive first only after metadata and promotion checks:

1. RuntimeLoop-era responsibility, planning, execution, and quarantine records
   whose current boundaries are already represented in canonical architecture;
2. older roadmap/status reconciliation records whose active items are already in
   `docs/reasoning_roadmap.md`, `docs/knowledge_acquisition_status.md`, or
   `docs/architectural_status_and_next_frontier.md`;
3. completed audit records whose unique negative findings are already preserved
   in `docs/architectural_findings_preservation.md`.

### What must never be archived without replacement?

Never archive without replacement:

- canonical architecture, invariant, state, logic-model, and function-block
  documents;
- active roadmap/status/frontier documents;
- active vocabularies and methodologies;
- generated architecture artifacts without updating the generation policy;
- preservation documents that retain negative findings, rejected concepts,
  paused chains, or provenance not represented elsewhere;
- any document that still owns a current boundary, owner, lifecycle rule,
  schema-adjacent semantic definition, or safety non-goal.
