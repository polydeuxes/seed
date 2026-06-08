# Documentation Boundary Enforcement Reconciliation

## 1. Purpose and scope

This document is a documentation-only audit of whether Seed's major
architectural documentation surfaces currently respect the authority boundaries
established by the documentation lifecycle and documentation authority audits.

It answers this narrow question:

```text
Do the documents currently stay within their assigned authority boundaries?
```

This audit does not ask who should own each answer. That ownership model is
already established by `docs/documentation_lifecycle_reconciliation.md` and
`docs/documentation_authority_reconciliation.md`. This document checks present
behavior against that model.

In scope:

- inspecting high-traffic navigation, map, preservation, status, roadmap,
  lifecycle, authority, characterization, vocabulary, and reconciliation
  documents;
- identifying documents that answer questions owned elsewhere;
- distinguishing harmless overlap from ambiguity-producing overlap;
- identifying restatements that should become references;
- recommending smallest boundary corrections.

Out of scope:

- redesigning Seed's documentation system;
- creating new document categories;
- archiving, moving, deleting, or renaming documents;
- introducing generated documentation;
- changing lifecycle definitions or authority definitions;
- changing production code, tests, runtime behavior, event schemas,
  projections, providers, acquisition logic, policy behavior, or execution
  behavior;
- proposing new architecture.

## 2. Documents inspected

Primary documents inspected:

- `docs/README.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_findings_preservation.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/reasoning_roadmap.md`
- `docs/documentation_lifecycle_reconciliation.md`
- `docs/documentation_authority_reconciliation.md`

Additional major authority-adjacent documents inspected or sampled:

- `docs/canonical_documentation_reconciliation.md`
- `docs/documentation_architecture_audit.md`
- `docs/architectural_findings_characterization.md`
- `docs/architectural_findings_vocabulary.md`
- `docs/architectural_findings_reconciliation.md`
- `docs/roadmap_reconciliation.md`
- `docs/roadmap_and_methodology_reconciliation.md`
- `docs/backlog_and_status_reconciliation.md`
- `docs/knowledge_acquisition_status.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_representation_map.md`
- `docs/knowledge_representation_reconciliation.md`
- representative scoped `*_characterization.md`, `*_vocabulary.md`,
  `*_audit.md`, `*_inventory.md`, `*_frontier.md`, and
  `*_reconciliation.md` documents.

## 3. Authority model reviewed

This audit uses the authority model established by
`docs/documentation_authority_reconciliation.md`:

| Authority role | Owner |
| --- | --- |
| Navigation authority | `docs/README.md` |
| Orientation/map authority | `docs/architectural_knowledge_map.md` |
| Preservation authority | `docs/architectural_findings_preservation.md` |
| Status/frontier authority | `docs/architectural_status_and_next_frontier.md` |
| Roadmap authority | `docs/reasoning_roadmap.md` |
| Lifecycle-role authority | `docs/documentation_lifecycle_reconciliation.md` |
| Decision-provenance authority | scoped `*_reconciliation.md` documents |
| Vocabulary authority | scoped `*_vocabulary.md` documents |
| Characterization authority | scoped `*_characterization.md`, `*_audit.md`, and `*_inventory.md` documents |
| Canonical architecture authority | `docs/architecture.md` plus scoped canonical documents |
| State/knowledge semantics authority | `docs/state.md` and scoped lifecycle/knowledge documents |
| Invariant authority | `docs/invariants.md` |
| Generated-reference authority | generated files within generation scope only |

The key reference-vs-authority rule is:

```text
A document may point to an answer owned elsewhere, but should not restate that
answer in enough detail that readers can treat the restatement as current,
canonical, or final.
```

## 4. Boundary-compliant documents

The following documents mostly respect their assigned boundaries today.

| Document | Authority responsibility | Compliance assessment | Notes |
| --- | --- | --- | --- |
| `docs/documentation_authority_reconciliation.md` | Define which existing surfaces own which answers. | Compliant. | It directly owns authority analysis and explicitly rejects becoming a new architecture system. |
| `docs/documentation_lifecycle_reconciliation.md` | Define lifecycle roles, archival/supersession vocabulary, and metadata expectations. | Mostly compliant. | It overreaches only where it names current canonical sets and archive candidates in detail; those details should be treated as lifecycle examples, not active content authority. |
| Scoped `*_vocabulary.md` documents | Define terms for their own concern. | Mostly compliant. | Sampled vocabulary documents generally define scoped language rather than global status. |
| Scoped `*_characterization.md`, `*_audit.md`, and `*_inventory.md` documents | Preserve observed behavior, evidence, inventories, and characterization. | Mostly compliant. | These documents become ambiguous only when older observations are read as superseding later reconciliations. The lifecycle model already handles that by requiring metadata and replacement links. |
| Scoped `*_reconciliation.md` documents | Preserve rationale and decisions for a specific concern. | Mostly compliant. | Older broad reconciliation documents overlap with newer global lifecycle/status documents, but this is usually a lifecycle-labeling issue rather than a content-authority failure. |
| `docs/knowledge_acquisition_status.md` | Status board for acquisition slices. | Compliant within its scope. | It owns acquisition-slice status more specifically than broad roadmap/status documents. Broad documents should reference it for acquisition slice details. |

## 5. Boundary violations

### 5.1 `docs/README.md`

Authority responsibility:

- Own navigation and entry orientation.
- Tell readers where to start and what to read next.

Current behavior:

- Provides recommended reading order, which is appropriate.
- Summarizes architectural concerns, current frontiers, important findings,
  rejected concepts, and recurring lessons.

Authority violations:

- It answers some status questions by naming active frontiers such as Users,
  Groups, Package, and Systemd Observation.
- It answers preservation/rejection questions by listing rejected concepts.
- It answers concern-specific finding questions by including important findings
  for Knowledge Selection, Response, and Architectural Findings.
- It restates recurring architectural lessons that are better owned by
  preservation and scoped reconciliations.

Duplicated authority:

- Rejected concepts duplicate `docs/architectural_findings_preservation.md`,
  scoped reconciliation documents, and `docs/architectural_knowledge_map.md`.
- Current frontier bullets duplicate `docs/architectural_status_and_next_frontier.md`,
  `docs/reasoning_roadmap.md`, and `docs/knowledge_acquisition_status.md`.
- Concern findings duplicate scoped characterization/reconciliation documents.

Recommended boundary correction:

- Keep the reading order and entry-point list.
- Replace substantive finding, frontier, and rejected-concept lists with compact
  references to the owning documents.
- Add explicit wording that `docs/README.md` owns navigation only and does not
  own status, preservation, roadmap, canonicality, or rejection rationale.

### 5.2 `docs/architectural_knowledge_map.md`

Authority responsibility:

- Own orientation and concern mapping.
- Route readers to canonical, status, preservation, roadmap, vocabulary, and
  reconciliation authorities.

Current behavior:

- Correctly states that it is not a source of truth, registry, inventory,
  runtime model, governance process, or replacement for canonical documents.
- Provides concern map and document links, which is appropriate.
- Also includes a status overview, major findings, rejected concepts, current
  frontier, documentation maintenance frontier, recurring architectural lessons,
  and recommended reading order.

Authority violations:

- It answers current-status questions through its status overview and current
  frontier sections.
- It answers preservation questions through major findings, recurring lessons,
  and repository-wide rejected concepts.
- It answers roadmap/frontier questions through priority lists and acquisition
  frontier language.
- It answers navigation questions already owned by `docs/README.md` through a
  recommended reading order.
- It uses canonical-document classification language that can be read as content
  authority rather than route guidance.

Duplicated authority:

- Status/frontier duplicates `docs/architectural_status_and_next_frontier.md`.
- Acquisition priorities duplicate `docs/knowledge_acquisition_status.md` and
  `docs/reasoning_roadmap.md`.
- Rejected concepts duplicate `docs/architectural_findings_preservation.md` and
  scoped reconciliations.
- Reading order duplicates `docs/README.md`.
- Canonical-document classification overlaps lifecycle/authority documents.

Recommended boundary correction:

- Keep the map structure and concern-to-document routing.
- Convert status, frontier, rejected concept, and recurring lesson sections into
  shorter pointers to their authority documents.
- Keep only enough summary text to orient a reader before following links.
- Strengthen the existing disclaimer by naming the authorities it references:
  status/frontier, preservation, roadmap, lifecycle, vocabulary, reconciliation,
  and canonical architecture.

### 5.3 `docs/architectural_findings_preservation.md`

Authority responsibility:

- Preserve completed findings, negative findings, rejected concepts, deferred
  concepts, and durable lessons from completed audit chains.
- Keep settled architecture knowledge discoverable.

Current behavior:

- Strongly preserves completed findings, negative findings, rejected concepts,
  and audit-chain outcomes.
- Also includes current frontier language, acquisition readiness, recommended
  documentation updates, and near-term candidate ordering.

Authority violations:

- It answers current-frontier questions by naming Knowledge Acquisition
  expansion and immediate candidates.
- It answers roadmap/backlog questions by ranking next acquisition candidates
  and documentation updates.
- It can be mistaken for a status page when it describes completed audit chains
  as settled status.

Duplicated authority:

- Current frontier duplicates `docs/architectural_status_and_next_frontier.md`.
- Future sequencing duplicates `docs/reasoning_roadmap.md` and
  `docs/knowledge_acquisition_status.md`.
- Documentation maintenance recommendations overlap
  `docs/documentation_lifecycle_reconciliation.md` and
  `docs/documentation_authority_reconciliation.md`.

Recommended boundary correction:

- Keep preserved findings and negative findings intact.
- Change current-frontier statements into historical handoff context, with a
  reference to `docs/architectural_status_and_next_frontier.md` for currentness.
- Change candidate ordering into preserved rationale or references to roadmap and
  acquisition status documents.

### 5.4 `docs/architectural_status_and_next_frontier.md`

Authority responsibility:

- Own current architectural status and active frontier.
- Summarize completed audit chains only as context for current status.

Current behavior:

- Clearly acts as the status/frontier surface.
- Also contains major architectural findings, negative findings worth preserving,
  backlog prioritization recommendations, documentation maintenance
  opportunities, rejection criteria for new audit chains, and rationale for why
  Knowledge Acquisition expansion is the recommended frontier.

Authority violations:

- It partially answers preservation questions through major findings and
  negative findings.
- It partially answers roadmap questions through backlog prioritization and
  future investigation categories.
- It partially answers methodology/governance questions through rejection
  criteria for new audit chains.

Duplicated authority:

- Major and negative findings duplicate
  `docs/architectural_findings_preservation.md`.
- Backlog and sequencing language duplicates `docs/reasoning_roadmap.md`,
  `docs/roadmap_reconciliation.md`, and `docs/backlog_and_status_reconciliation.md`.
- Documentation maintenance opportunities duplicate lifecycle and authority
  reconciliation concerns.

Recommended boundary correction:

- Keep current status, active frontier, and why that frontier is current.
- Reference preservation for durable findings and rejected concepts.
- Reference roadmap/acquisition status for sequencing beyond the current
  frontier.
- Reframe rejection criteria as status-context guidance or reference the
  preservation/authority documents that own settled negative findings.

### 5.5 `docs/reasoning_roadmap.md`

Authority responsibility:

- Own roadmap sequencing, future work, backlog context, and historical evolution
  of planned reasoning-system work.

Current behavior:

- Provides roadmap triage, concern-level future directions, missing pieces,
  non-goals, and smallest safe next implementations.
- Also includes canonical runtime ownership statements, current repo support,
  implemented status, and completed-audit conclusions.

Authority violations:

- It answers current architecture ownership questions by restating Runtime,
  ToolExecutor, ProjectionStore, and EventLedger authority.
- It answers current status questions by marking items implemented, complete,
  paused, or not justified.
- It answers preservation questions by restating completed audit-program
  findings and rejected directions.

Duplicated authority:

- Runtime and ownership statements duplicate `docs/architecture.md`,
  `docs/invariants.md`, and generated architecture outputs.
- Implemented/current status duplicates `docs/architectural_status_and_next_frontier.md`
  and scoped status documents.
- Completed-audit findings duplicate `docs/architectural_findings_preservation.md`
  and scoped reconciliations.

Recommended boundary correction:

- Keep sequencing, future-work framing, and backlog context.
- Convert canonical runtime ownership assertions into references to architecture
  and invariant documents.
- Convert current status assertions into references to status/frontier and scoped
  status documents.
- Preserve historical evolution but avoid presenting roadmap history as the
  current board.

### 5.6 `docs/documentation_lifecycle_reconciliation.md`

Authority responsibility:

- Own lifecycle roles, archival/supersession vocabulary, provenance metadata,
  and safe archival rules.

Current behavior:

- Defines lifecycle states and metadata expectations.
- Also lists current canonical documents, active documents, archive candidates,
  and documents that may be superseded.

Authority violations:

- It can answer current canonical-set and archive-candidate questions in a way
  that overlaps `docs/documentation_authority_reconciliation.md`,
  `docs/canonical_documentation_reconciliation.md`, README/map navigation, and
  scoped authority documents.

Duplicated authority:

- Canonical-set lists overlap canonical documentation reconciliation and
  authority reconciliation.
- Archive-candidate lists overlap older broad canonical documentation and
  documentation architecture audits.

Recommended boundary correction:

- Keep lifecycle vocabulary and rules.
- Treat document lists as examples or first-pass candidates unless another
  document explicitly adopts them.
- Reference authority reconciliation for ownership and scoped documents for
  current content.

### 5.7 `docs/canonical_documentation_reconciliation.md`

Authority responsibility:

- Preserve a prior canonical/generated/roadmap/status/historical/archive-candidate
  reconciliation.

Current behavior:

- Classifies many documents and recommends a lifecycle register or index.
- Its canonical set predates the later lifecycle and authority reconciliations.

Authority violations:

- It risks redefining canonicality and lifecycle classification after newer
  lifecycle/authority work has established more precise boundaries.

Duplicated authority:

- Canonical-set and lifecycle-role language duplicates
  `docs/documentation_lifecycle_reconciliation.md` and
  `docs/documentation_authority_reconciliation.md`.

Recommended boundary correction:

- Treat as decision provenance and historical classification input.
- Reference lifecycle and authority reconciliations for current lifecycle and
  ownership language.

### 5.8 Older roadmap/status/backlog reconciliation documents

Documents:

- `docs/roadmap_reconciliation.md`
- `docs/roadmap_and_methodology_reconciliation.md`
- `docs/backlog_and_status_reconciliation.md`

Authority responsibility:

- Preserve scoped historical rationale for roadmap, methodology, backlog, and
  handoff decisions.

Current behavior:

- They contain useful provenance but also include status/backlog claims that can
  look current.

Authority violations:

- They can answer current roadmap/status questions now owned by
  `docs/reasoning_roadmap.md`, `docs/architectural_status_and_next_frontier.md`,
  and scoped status documents.

Duplicated authority:

- Current status, next frontier, backlog classification, and methodology
  sequencing overlap newer roadmap/status/lifecycle surfaces.

Recommended boundary correction:

- Treat as scoped decision provenance.
- Add references or lifecycle notes in future cleanup so readers go to current
  roadmap/status documents for currentness.

## 6. Duplicate-authority findings

| Duplicate area | Documents involved | Current risk | Preferred owner |
| --- | --- | --- | --- |
| Reading order/navigation | `docs/README.md`, `docs/architectural_knowledge_map.md` | Low to medium. Two entry points can diverge. | `docs/README.md` |
| Concern orientation | `docs/README.md`, `docs/architectural_knowledge_map.md` | Low. Helpful orientation if compact. | `docs/architectural_knowledge_map.md` |
| Current frontier | `docs/architectural_knowledge_map.md`, `docs/architectural_findings_preservation.md`, `docs/architectural_status_and_next_frontier.md`, `docs/reasoning_roadmap.md`, `docs/knowledge_acquisition_status.md` | High. Readers may not know which frontier is current. | `docs/architectural_status_and_next_frontier.md`, with acquisition detail in `docs/knowledge_acquisition_status.md` |
| Acquisition candidate ordering | README, map, preservation, status/frontier, roadmap, acquisition status | High. Candidate priority can drift across five surfaces. | `docs/architectural_status_and_next_frontier.md` for active frontier; `docs/knowledge_acquisition_status.md` for slice status; `docs/reasoning_roadmap.md` for sequencing context |
| Rejected concepts | README, map, preservation, status/frontier, scoped reconciliations | High. Rejection lists can become inconsistent and lose rationale. | `docs/architectural_findings_preservation.md` for consolidated preservation; scoped reconciliations for rationale |
| Completed audit findings | preservation, status/frontier, roadmap, map, scoped audits/reconciliations | Medium to high. Summaries can diverge from preserved findings. | `docs/architectural_findings_preservation.md` plus scoped source chains |
| Canonical document lists | map, lifecycle, authority, canonical documentation reconciliation, README | Medium. Classification lists can diverge. | lifecycle/authority documents for role definitions; scoped canonical docs for content |
| Runtime ownership assertions | roadmap, status, preservation, architecture, invariants | Medium. Repeated non-goals are useful but can stale. | `docs/architecture.md` and `docs/invariants.md` |
| Documentation maintenance recommendations | preservation, status/frontier, lifecycle, authority | Medium. Cleanup priority can look like competing roadmaps. | lifecycle for lifecycle rules; authority for boundary rules; status/frontier for current maintenance opportunities |
| Vocabulary definitions | scoped vocabularies, maps, roadmaps, reconciliations | Low to medium. Short restatements are useful, but full definitions should not drift. | scoped `*_vocabulary.md` documents |

## 7. Reference-vs-restatement findings

Content that should remain as short reference:

- README references to map, preservation, status/frontier, roadmap, and concern
  documents.
- Map references to canonical documents, vocabularies, reconciliations, status,
  preservation, and roadmap.
- Preservation references to active frontier and future acquisition sequencing.
- Status/frontier references to completed findings and rejected concepts.
- Roadmap references to current runtime ownership and settled audit conclusions.
- Lifecycle references to canonical sets, active documents, and archive
  candidates.

Content that currently reads too much like restatement:

- README's rejected-concept list and concern-level important findings.
- Knowledge map's status overview, current frontier, repository-wide rejected
  concepts, recurring lessons, and reading order.
- Preservation's current frontier and acquisition candidate ranking.
- Status/frontier's major findings, negative findings, backlog categories, and
  audit-chain rejection criteria.
- Roadmap's implemented/current-status statements and canonical runtime owner
  assertions.
- Lifecycle's detailed current canonical and archive-candidate lists.

Safe restatement pattern:

```text
One sentence of context + link to the authority.
```

Unsafe restatement pattern:

```text
A complete list, priority order, rationale, or final label that a reader could
use without opening the authority document.
```

## 8. Highest-value cleanup opportunities

### 1. Convert repeated current-frontier statements into references

Highest value because currentness changes faster than preserved findings. The
same Knowledge Acquisition frontier appears across README, map, preservation,
status/frontier, roadmap, and acquisition status. The smallest cleanup is to make
`docs/architectural_status_and_next_frontier.md` the only broad current-frontier
answer and make other documents reference it.

### 2. Centralize rejected-concept summaries by reference

Rejected concepts appear in multiple visible surfaces. The consolidated list
should be preserved in `docs/architectural_findings_preservation.md`; scoped
reconciliations should own rationale. README and map should link rather than
carry long lists.

### 3. Reduce the knowledge map to map-level summaries

The map has the broadest authority sprawl. It is already explicitly
non-authoritative, so cleanup does not require a conceptual change. Replace full
status/frontier/rejection/restatement sections with route guidance.

### 4. Make README navigation-only in practice

README is high-traffic. Removing substantive status, rejection, and finding
claims from README would immediately reduce duplicate entry-point authority.

### 5. Add boundary notes to preservation, status/frontier, and roadmap

Each document is useful and mostly correctly scoped. A compact boundary note near
the top would prevent readers from treating preservation as status, status as
preservation, or roadmap as the current board.

### 6. Treat older broad reconciliation documents as provenance

Older roadmap/status/canonical documentation reconciliations should not be
rewritten into current authorities. Future cleanup should add references or
lifecycle notes that direct readers to the newer authority/lifecycle/status
surfaces.

## 9. Non-goals

This boundary audit does not recommend:

- changing Seed architecture;
- adding or removing runtime behavior;
- changing tests;
- changing schemas;
- changing projections;
- changing providers;
- changing acquisition behavior;
- changing policy behavior;
- changing lifecycle definitions;
- changing authority definitions;
- creating new document categories;
- moving or archiving documents;
- deleting historical records;
- generating documentation;
- creating a registry, database, governance process, or new documentation
  system.

## 10. Rejected solutions

Rejected solution: make the knowledge map the global authority.

Reason rejected: the map already says it is not a source of truth. Making it the
global authority would collapse navigation, status, preservation, roadmap,
canonicality, vocabulary, and reconciliation into one document.

Rejected solution: make README the broad summary authority.

Reason rejected: README should be stable orientation. If it owns rejected
concepts, frontiers, findings, and reading order, it becomes a second map, second
status board, and second preservation surface.

Rejected solution: make preservation own current frontier.

Reason rejected: preservation answers what was learned and why it matters.
Currentness belongs to status/frontier documents.

Rejected solution: make roadmap own current status.

Reason rejected: roadmap explains sequencing and evolution. It may use current
status as input, but it should not be the current board.

Rejected solution: solve overlap by archiving documents now.

Reason rejected: the problem is authority ambiguity, not document existence.
Archival without metadata and references would risk losing provenance.

Rejected solution: create a new documentation category or generated index.

Reason rejected: the established authority model is already sufficient. The
smallest useful cleanup is replacing restatements with references in existing
surfaces.

## 11. Direct answer

### 1. Does README act only as navigation/orientation?

No. `docs/README.md` is primarily navigational, but it also restates current
frontiers, rejected concepts, concern findings, and recurring lessons. Those
answers are owned by status/frontier, preservation, scoped reconciliations, and
vocabulary/characterization documents.

### 2. Does the knowledge map act only as a map?

No. It declares the correct boundary, but then provides status overview,
frontier, rejected-concept, recurring-lesson, and reading-order content. Its
intent is map-like; its content currently exceeds map authority.

### 3. Does findings preservation act only as preservation?

Mostly, but not completely. It strongly owns preservation, but current frontier,
acquisition readiness, recommended documentation updates, and candidate ordering
bleed into status and roadmap authority.

### 4. Does status/frontier act only as status/frontier?

Mostly, but not completely. It correctly owns current status and active frontier,
but also restates preservation findings, negative findings, backlog categories,
and audit-chain rejection criteria.

### 5. Does roadmap act only as roadmap/evolution?

Mostly, but not completely. It owns roadmap and evolution, but restates current
architecture ownership, implementation status, completed-audit conclusions, and
non-goals owned by architecture, invariants, status/frontier, and preservation
surfaces.

### 6. Which documents currently answer questions owned elsewhere?

- `docs/README.md` answers status, rejection, finding, and lesson questions.
- `docs/architectural_knowledge_map.md` answers status, frontier, rejection,
  preservation, canonicality, and reading-order questions.
- `docs/architectural_findings_preservation.md` answers current-frontier and
  roadmap-sequencing questions.
- `docs/architectural_status_and_next_frontier.md` answers preservation,
  roadmap, and methodology-gating questions.
- `docs/reasoning_roadmap.md` answers current-status, current-architecture, and
  preservation questions.
- `docs/documentation_lifecycle_reconciliation.md` answers some canonical-set
  and archive-candidate questions beyond pure lifecycle vocabulary.
- `docs/canonical_documentation_reconciliation.md` answers lifecycle and
  canonicality questions now better owned by newer lifecycle/authority work.
- Older roadmap/status/backlog reconciliations answer currentness questions now
  owned by current status and roadmap documents.

### 7. Which documents duplicate information owned by another authority?

Highest duplication appears in:

- current frontier and acquisition candidate ordering;
- rejected concepts;
- completed audit findings;
- canonical document classification;
- roadmap/status/backlog labels;
- runtime ownership and non-goal assertions;
- documentation maintenance recommendations.

### 8. Which documents should replace content with references?

- README should replace rejected concepts, current frontier, concern findings,
  and recurring lessons with references.
- Knowledge map should replace detailed status/frontier/rejection/lesson content
  with references.
- Preservation should replace current frontier and candidate ordering with
  references.
- Status/frontier should replace detailed preserved findings and rejected lists
  with references.
- Roadmap should replace current ownership/status restatements with references.
- Lifecycle should replace or qualify detailed current document lists as examples
  and reference authority documents for ownership.
- Older broad reconciliation documents should reference current lifecycle,
  authority, roadmap, and status surfaces.

### 9. Which overlaps are harmless?

Harmless overlaps:

- one-sentence context summaries before links;
- repeated high-level concern names such as Acquisition, Integrity, Selection,
  and Response;
- short non-goal reminders that prevent unsafe implementation drift;
- cross-links among README, map, preservation, status, and roadmap;
- scoped vocabulary terms repeated briefly for readability;
- historical documents retaining their original claims as provenance when newer
  authority is clear.

### 10. Which overlaps create ambiguity?

Ambiguity-producing overlaps:

- multiple current-frontier statements;
- multiple rejected-concept lists;
- multiple canonical-document classifications;
- roadmap documents that look like current status boards;
- preservation documents that look like active backlog boards;
- map sections that look like authoritative status or rejection summaries;
- README sections that look like final architecture findings rather than entry
  orientation.

### 11. Which overlaps create maintenance burden?

Maintenance burden is highest where facts change or lists expand:

- acquisition candidate priority lists;
- implemented/planned/deferred status labels;
- rejected concept lists;
- canonical document lists;
- archive/supersession candidates;
- documentation maintenance opportunity lists;
- repeated runtime ownership/non-goal assertions.

### 12. Which overlaps are the highest-value cleanup targets?

Highest-value targets:

1. current-frontier duplication across README, map, preservation, status,
   roadmap, and acquisition status;
2. rejected-concept duplication across README, map, preservation, status, and
   scoped reconciliations;
3. knowledge map sections that restate status, frontier, rejection, and reading
   order;
4. README sections that restate substantive findings instead of routing;
5. roadmap current-status and architecture-owner restatements;
6. lifecycle/canonical-document lists that can be read as competing current
   authority.

## Closing answers

### Which documents currently violate authority boundaries?

The documents with meaningful boundary violations are:

- `docs/README.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_findings_preservation.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/reasoning_roadmap.md`
- `docs/documentation_lifecycle_reconciliation.md`
- `docs/canonical_documentation_reconciliation.md`
- older roadmap/status/backlog reconciliation documents, especially
  `docs/roadmap_reconciliation.md`,
  `docs/roadmap_and_methodology_reconciliation.md`, and
  `docs/backlog_and_status_reconciliation.md`

The strongest violations are in `docs/architectural_knowledge_map.md` and
`docs/README.md` because they are high-traffic entry surfaces and repeat answers
owned elsewhere.

### Which violations matter most?

The most important violations are the ones that can make readers act on stale or
competing guidance:

1. current frontier and acquisition priority duplication;
2. rejected-concept duplication without scoped rationale;
3. map-as-status and README-as-summary behavior;
4. roadmap-as-current-status behavior;
5. lifecycle/canonical-set lists that compete with newer authority boundaries.

### What is the smallest cleanup that would produce the largest reduction in documentation ambiguity?

The smallest high-impact cleanup is:

1. add explicit authority-boundary notes to README, the knowledge map,
   preservation, status/frontier, and roadmap;
2. make `docs/README.md` navigation-only by replacing substantive finding,
   frontier, and rejected-concept lists with links;
3. make `docs/architectural_knowledge_map.md` map-only by replacing detailed
   status, frontier, rejected-concept, recurring-lesson, and reading-order
   sections with references;
4. route current frontier to `docs/architectural_status_and_next_frontier.md`,
   durable findings/rejections to `docs/architectural_findings_preservation.md`,
   future sequencing to `docs/reasoning_roadmap.md`, and acquisition slice status
   to `docs/knowledge_acquisition_status.md`.

That cleanup does not require new categories, moves, archival, generated docs, or
architecture changes. It only enforces the authority model already established.
