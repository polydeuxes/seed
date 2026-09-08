# Competency Interrogation 001

## Selected competency

**Documentation Structure Adapter**.

This interrogation selects Documentation Structure because it is implementation-backed, public-surface visible, tested through diagnostic inventory and diagnostic shape audit, and mature enough to answer most constitutional questions without promoting speculative vocabulary into knowledge.

## Implementation evidence reviewed

Implementation evidence reviewed in this interrogation:

- `seed_runtime/documentation_structure.py`
  - module boundary text;
  - `BOUNDARY`, `RECURRENCE_BOUNDARY`, and `MEMBERSHIP_BOUNDARY`;
  - document selection and observation implementation;
  - JSON and human formatting surfaces.
- `seed_runtime/structure_observation.py`
  - substrate-independent Structure Observation boundary;
  - adapter handoff through `as_documentation_boundary()`.
- `seed_runtime/diagnostic_inventory.py`
  - `documentation_structure` diagnostic registration;
  - CLI flags, JSON support, record scope, event-ledger, repository-file, diagnostic-fact, and cluster-mutation declarations.
- `seed_runtime/diagnostic_shape_audit.py`
  - implementation spec tying `documentation_structure` to build, format, JSON functions, CLI flags, and repository-file markers.
- `tests/test_documentation_structure.py`
  - structural extraction, output, read-only, filtering, document selection, relation observation, recurrence, drilldown, and membership behavior.
- `tests/test_diagnostic_inventory.py`
  - inventory assertions for `documentation_structure` flags, description, JSON support, record support, record scope, event-ledger boundary, and cluster mutation boundary.
- `tests/test_diagnostic_shape_audit.py`
  - shape-audit coverage proving the surface is checked by diagnostic shape audit.
- App command run for this interrogation:
  - `python scripts/seed_local.py --documentation-structure --summary-only`

## Interrogation matrix

Legend:

- ✓ Answered by implementation
- ? Partially supported
- ○ Not applicable
- ✗ Unsupported / unknown

### Identity

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| What competent worker is this? | ✓ | Documentation Structure Adapter: a read-only Markdown documentation structural observer for allowlisted top-level `docs/*.md` repository files. |
| What bounded responsibility does it own? | ✓ | It owns Markdown documentation structure observation: document counts, line/byte counts, blank/nonblank lines, front matter, H1 presence, trailing newline state, internal/external/broken links, fenced code blocks, sections, selected architectural relation forms, recurrence, drilldown, and exact section-label membership. |
| What does it explicitly refuse to own? | ✓ | It refuses prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, event-ledger writes, and repository mutation. Membership additionally refuses similarity, classification, ontology promotion, recommendation, and prose interpretation. |
| What implementation evidence supports these boundaries? | ✓ | The boundary constants and `observe_documentation_structure()` implementation support the boundary. Diagnostic inventory and shape-audit specs independently register and check the public surface. Tests assert rendered boundary text, read-only behavior, diagnostic inventory registration, and shape-audit coverage. |

### Constitutional Authority

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| Who may invoke this worker? | ✓ | Operators may invoke it through `seed --documentation-structure` and related flags implemented by `scripts/seed_local.py`; internal callers may invoke `observe_documentation_structure()`, `documentation_structure_json()`, and formatter functions. |
| Who may consume its artifacts? | ? | The CLI consumer and tests consume its text/JSON reports. Observation Agreement imports `DocumentationArchitecturalRelationRecord`, showing at least one implementation consumer for relation records. A complete consumer registry is not present. |
| What constitutional authority permits it to participate? | ✓ | The Structure Observation boundary permits read-only structural extraction with evidence preservation, while the Documentation Structure adapter keeps substrate parsing, record schema, traversal, and compatibility surfaces local. |
| What constitutional constraints limit it? | ✓ | It must remain read-only, documentation-structure-local, non-interpretive, non-mutating, and registered/shape-audited as a diagnostic surface. |
| What would be an unlawful expansion of responsibility? | ✓ | Inferring claims, authority, responsibility, grammar, ontology, shape meaning, recommendations, or cluster truth from Markdown presentation would exceed implementation authority. Writing diagnostic findings into the event ledger or mutating repository/cluster state would also exceed its declared boundary. |

### Evidence

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| What evidence can this worker observe? | ✓ | It can observe filesystem evidence from allowlisted top-level `docs/*.md` files: paths, text lines, bytes, Markdown headings, sections, YAML front matter delimiters, links, fenced code fences and languages, trailing newlines, empty sections, and selected exact architectural relation line forms. |
| What evidence can it preserve? | ✓ | It preserves structural summaries, per-document structural records, selected relation records with source/provenance, recurrence/drilldown/membership report data, and boundary fields in text/JSON reports. |
| What evidence can it not observe? | ✓ | It does not parse code contents, infer prose claims, infer authority, infer shape meaning, infer grammar, recover responsibility, stabilize vocabulary, observe semantic similarity, classify membership, or promote ontology. |
| What evidence permits movement? | ✓ | Movement is permitted by observed structural facts: selected documents exist under `docs/*.md`, exact document selection resolves safely, filters match declared structural predicates, recurrence/drilldown/membership are requested through explicit flags, and output bounds are explicit. |
| What evidence causes lawful stop? | ✓ | No selected docs, traversal attempts, non-doc selections, missing selected documents, unsupported flags without the parent surface, no matching filter results, or unsupported conclusions all cause stop or bounded empty output rather than interpretive promotion. |

### Boundaries

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| Where does this worker begin? | ✓ | It begins at a repository root and optional documented CLI/options request, then selects allowlisted top-level Markdown files under `docs/` or a single safely resolved document. |
| Where does it end? | ✓ | It ends at a `DocumentationStructureReport` and text/JSON formatting. It does not convert findings into cluster facts, event-ledger truth, repository edits, or responsibility claims. |
| Which neighboring responsibilities does it deliberately avoid? | ✓ | It avoids generic Structure Observation ownership, repository artifact/code observation, relationship ownership beyond exact documentation relation records, grammar observation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, event-ledger writing, and cluster mutation. |
| Which recurring implementation evidence supports those boundaries? | ✓ | Boundary constants, diagnostic inventory fields, diagnostic shape-audit specs, and tests repeatedly assert read-only, non-recording, non-mutating, repo-file-consuming, JSON-capable, no-event-ledger behavior. |

### Artifact Handoff

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| What artifact leaves this worker? | ✓ | A `DocumentationStructureReport`, text report, JSON payload, recurrence report, drilldown report, membership report, and embedded relation records can leave the worker. |
| What minimum orientation survives? | ✓ | Report type, document path, counts, selected document when applicable, observed structural categories, boundary fields, and option-driven report modes survive. |
| What provenance survives? | ✓ | Paths and source locations for document-derived structures survive; relation records preserve source line evidence. Summary/report output preserves selected document and document-relative evidence. |
| Who may consume the artifact? | ? | CLI users, tests, diagnostic shape/inventory governance, and implementation consumers of relation records may consume it. Broader consumers are not exhaustively declared. |
| What information is intentionally excluded? | ✓ | Prose meaning, claims, authority, ownership, grammar, ontology, recommendations, semantic similarity, code parsing, event-ledger mutation, cluster mutation, and repository mutation are intentionally excluded. |

### Unknown

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| What can remain unknown? | ✓ | Meaning of prose, legitimacy of claims, authority of a statement, semantic relation between documents, ownership/responsibility, grammar, ontology, and whether observed structure should change remain unknown. |
| What unsupported conclusions are refused? | ✓ | The worker refuses to conclude that a heading names an owner, a repeated label is a stable lexicon term, a relation line is architectural truth, a section implies authority, or missing structure implies a required project action. |
| How does the competency stop honestly? | ✓ | It returns bounded structural output, empty bounded output, or explicit selection/flag errors; it does not fill interpretive gaps with assumptions. |

### Locality

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| Why is this competency local? | ✓ | It is local because it observes a specific substrate: repository Markdown documentation under `docs/`. Its parsing, records, traversal, output vocabulary, and CLI compatibility surface are adapter-owned. |
| Why has implementation rejected universal ownership? | ✓ | `StructureObservationBoundary` keeps substrate-independent ownership separate and says substrate adapters keep parsing, record schemas, traversal, and compatibility surfaces. Documentation Structure's own boundary narrows to Markdown/document structure. |
| What would fail if this competency became universal? | ✓ | Markdown-specific assumptions would be wrongly applied to code, repository artifacts, relationship observations, runtime evidence, and cluster truth. Public CLI vocabulary and JSON shapes would overreach beyond their tested substrate. |

### Continuity

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| What public compatibility contract exists? | ✓ | The diagnostic inventory declares the `documentation_structure` CLI flags, JSON support, no record support, `record_scope=none`, event-ledger boundary, repository-file usage, diagnostic-fact behavior, and cluster-mutation boundary. Tests assert those fields. |
| What internal implementation freedom remains? | ✓ | Internal parsing and report construction may evolve if the public flags, JSON/text expectations, boundary constraints, and tests remain satisfied. Structure Observation allows adapter-local parsing and schema ownership. |
| What identity survives implementation evolution? | ✓ | Read-only Markdown documentation structural observation survives: not prose interpretation, not authority/claim/shape inference, not responsibility recovery, not mutation. |

### Self-Observation

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| How can this competency be audited? | ✓ | Through `seed --diagnostic-inventory`, `seed --diagnostic-shape-audit`, documentation-structure tests, and direct CLI execution such as `seed --documentation-structure --summary-only`. |
| How is drift detected today? | ✓ | Diagnostic shape audit compares inventory declarations with static implementation specs and markers. Tests assert inventory fields and shape-audit inclusion. Documentation-structure tests assert output and boundary behavior. |
| What diagnostic evidence already exists? | ✓ | The inventory registration and shape-audit implementation spec exist. The app reports a Documentation Structure boundary and structural counts. |
| What important self-observation remains absent? | ? | No complete consumer registry was found for all artifacts. No explicit self-audit proves every downstream consumer preserves the non-interpretive boundary. No public compatibility version field for the JSON schema was identified in this interrogation. |

### Evolution

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| Why did this competency emerge? | ? | Implementation and prior slices show it emerged as a Markdown substrate adapter under broader Structure Observation pressure, but exact historical causality is partly report-backed rather than solely code-backed. |
| What architectural pressure produced it? | ? | Repeated need to observe documentation structure without interpreting prose appears supported by boundary constants, tests, and diagnostic governance. Full pressure history remains partly characterized in prior documents rather than executable implementation. |
| What future evidence could split it? | ✓ | If recurrence, membership, relation observation, link checking, or code-fence observation gain independent consumers, schemas, or drift audits, they could split into more specific local workers. |
| What future evidence could simplify it? | ✓ | If downstream consumers only require a smaller structural summary, detail expansions or separate report modes could collapse or remain formatting-only concerns. |

## Recurring implementation evidence

Recurring implementation evidence supports the same constitutional boundary from multiple directions:

1. **Boundary constants repeat the refusal.** Documentation Structure declares read-only observation, no prose interpretation, no grammar interpretation, no responsibility recovery, no lexicon stabilization, no claim extraction, no authority inference, no shape inference, no event-ledger writes, and no repository mutation.
2. **Structure Observation keeps ownership split.** The shared owner keeps substrate-independent structural extraction separate from substrate parsing, record schemas, traversal, and compatibility surfaces.
3. **Diagnostic inventory registers the public surface.** The inventory declares flags, JSON support, no record support, `record_scope=none`, repository-file usage, no event-ledger write, and no cluster mutation.
4. **Diagnostic shape audit checks the declaration.** The shape-audit spec names the module, build function, format function, JSON function, flags, and repo-file markers.
5. **Tests preserve the boundary.** Tests assert boundary text in human output, JSON validity, read-only behavior, filter and selection limits, inventory registration, and shape-audit inclusion.
6. **The app reports bounded structural evidence.** The app command used for this interrogation reported structural counts and the boundary without interpreting prose or recommending work.

## Constitutional observations

Documentation Structure is not merely a checklist surface. It answers a narrower oral examination:

- **Who are you?** A Markdown documentation structural observer.
- **What do you own?** Structural facts about allowlisted docs, plus bounded recurrence, drilldown, membership, and exact relation observations.
- **What do you refuse?** Meaning, authority, responsibility, grammar, lexicon, ontology, recommendation, ledger writes, repository mutation, and cluster mutation.
- **What evidence lets you move?** Concrete Markdown/file structural evidence and explicit operator options.
- **What evidence makes you stop?** Unsafe or unsupported selection, absent files, unmatched filters, unsupported flags, and interpretive conclusions.
- **What artifact do you return?** A bounded report with structural data and boundary/provenance.
- **Who may trust it?** Consumers may trust it as structural observation only, not as architectural truth.
- **What must remain unknown?** Meaning, authority, responsibility, grammar, ontology, and required action.

## Unsupported answers

The following answers remain unsupported or only partially supported:

- A complete list of all legitimate consumers of every Documentation Structure artifact.
- A proof that every downstream consumer preserves the non-interpretive boundary.
- A complete implementation-only origin story for why the competency emerged.
- A stable constitutional outcome taxonomy for all future competency interrogations.
- A versioned public JSON compatibility contract beyond tested field behavior and inventory declarations.

## Constitutional oral examination

If Seed were asked to explain Documentation Structure, he could answer truthfully in bounded terms.

| Answer class | Result |
| --- | --- |
| Unknown | Full consumer map; all downstream boundary preservation; complete emergence history; stable future split/simplification path. |
| Unsupported | Any claim that Documentation Structure understands prose, validates authority, recovers responsibility, stabilizes vocabulary, recommends work, mutates repository state, or writes cluster truth. |
| Operator-only | CLI invocation, selected filters, selected document, output bounds, and display mode. |
| Presentation vocabulary | Report headings such as `Documentation Structure`, recurrence/drilldown/membership labels, and count labels are output orientation unless implementation evidence grants stronger authority. |
| Implementation-backed | Read-only Markdown structural observation; allowlisted docs selection; structural counts; section/link/code-fence/front-matter/trailing-newline evidence; exact relation forms; no record support; `record_scope=none`; no event-ledger write; no cluster mutation; diagnostic inventory and shape-audit coverage. |

## Lawful termination

**Characterization sufficient.**

The interrogation recovers a bounded, implementation-backed competency and does not justify implementation recovery. Documentation Structure already has an explicit local boundary, public diagnostic registration, shape-audit coverage, tests, and app-visible output. The smallest truthful constitutional stop is characterization: trust the competency only as read-only Markdown documentation structural observation, and stop before prose meaning, authority, responsibility, grammar, ontology, recommendation, or mutation.

## Remaining questions

- Should a future interrogation examine a downstream consumer to verify preservation of Documentation Structure's non-interpretive boundary?
- Should JSON compatibility be versioned, or are tests and diagnostic inventory sufficient for the current constitutional contract?
- Are recurrence, membership, or architectural relation observations still adapter-local, or has a downstream consumer made one mature enough for a separate interrogation?

## Confidence

**High** for the bounded identity, responsibility, refusals, evidence boundary, locality, continuity, and self-observation currently implemented.

**Medium** for consumer completeness and historical emergence, because those answers are partly supported by imports, tests, and prior characterization documents but not by a complete implementation registry.
