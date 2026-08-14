# Competency Interrogation 003

## Methodological refinements applied

This interrogation applies the existing Competency Interrogation discipline with the refinements requested for Competency Interrogation 003.

The refinements are treated as hypotheses only. They are reduced wherever implementation does not independently support them.

Repository authority wins.

This interrogation therefore separates worker, competency, and bounded responsibility; splits constitutional trust into what, extent, and assumptions; recovers competency preconditions; preserves unanswered questions in existing categories; adds constitutional reliance statements; and ends with a lawful stop rather than a project-management conclusion.

## Selected competency

**Documentation Structure Observation**.

This interrogation selects Documentation Structure Observation because it is implementation-backed as a diagnostic surface, has diagnostic inventory registration, has diagnostic shape-audit coverage, and has explicit refusal boundaries. It is more operationally visible than the Repository Artifact Observation Adapter interrogated in Competency Interrogation 002.

The selected competency is not a universal documentation interpreter. It is the read-only Markdown documentation structure observer implemented in `seed_runtime/documentation_structure.py`, registered as the `documentation_structure` diagnostic surface.

## Implementation evidence reviewed

Implementation evidence reviewed in this interrogation:

- `seed_runtime/documentation_structure.py`
  - module-level purpose: read-only structural observation for repository Markdown documentation;
  - `BOUNDARY_TEXT`, `RECURRENCE_BOUNDARY_TEXT`, and `MEMBERSHIP_BOUNDARY_TEXT` refusal language;
  - `observe_documentation_structure()` selection of top-level `docs/*.md` files or one resolved document;
  - `DocumentationStructureOptions` and subordinate option records;
  - `DocumentationStructureReport` construction;
  - `documentation_structure_json()`;
  - `format_documentation_structure()` and specialized recurrence, drilldown, and membership formatters.
- `seed_runtime/diagnostic_inventory.py`
  - `documentation_structure` inventory entry;
  - CLI flags;
  - `uses_repo_files=True`;
  - `supports_json=True`;
  - `supports_record=False`;
  - `record_scope="none"`;
  - `writes_event_ledger=False`;
  - `mutates_cluster=False`;
  - diagnostic description preserving non-interpretive boundaries.
- `seed_runtime/diagnostic_shape_audit.py`
  - `documentation_structure` implementation spec;
  - build, format, and JSON function names;
  - CLI flag coverage;
  - repository-file evidence markers;
  - mutation markers checked by the diagnostic shape audit.
- `tests/test_diagnostic_inventory.py`
  - tests proving `documentation_structure` appears in diagnostic inventory;
  - tests proving recording, event-ledger, and mutation boundaries.
- `tests/test_diagnostic_shape_audit.py`
  - tests proving `documentation_structure` is checked by diagnostic shape audit.
- App command run for this interrogation:
  - `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Interrogation matrix

Legend:

- ✓ Answered by implementation
- ? Partially supported / unanswered but meaningful
- ○ Not applicable at current maturity
- ✗ Unsupported / unknown

Question level legend:

- **Core** — needed for truthful bounded use of the competency now.
- **Advanced** — useful for mature public or multi-consumer governance, but not always required for this surface.
- **Evolutionary** — future split, simplification, or maturation question; absence is not automatically a failure.

### Identity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What worker or implementation surface is being interrogated? | ✓ | The `documentation_structure` diagnostic surface is being interrogated: `observe_documentation_structure()`, `documentation_structure_json()`, `format_documentation_structure()`, and the CLI flags registered for Documentation Structure. |
| Core | What competency does that worker exercise? | ✓ | It exercises read-only structural observation of repository Markdown documentation. |
| Core | What bounded responsibility does that competency own? | ✓ | It owns mechanical observation and rendering of top-level repository documentation structure: document metrics, front matter presence, heading outline metadata, section inventory boundaries, structural Markdown link targets, fenced code block structure, explicit architectural relation forms, corpus-level structural recurrence, exact section-label drilldown, exact section-label membership, and skeleton signatures. |
| Core | Does implementation distinguish worker, competency, and responsibility? | ✓ | Yes. The worker is the diagnostic surface and functions; the competency is Markdown documentation structure observation; the bounded responsibility is mechanical structural reporting over selected repository docs. |
| Core | If they collapse, where does implementation collapse them? | ○ | They do not collapse for the core surface. Implementation distinguishes function surface, inventory registration, shape-audit spec, options, report, formatting, and refusal boundaries. |
| Core | What does it explicitly refuse to own? | ✓ | It refuses prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, ontology promotion, event-ledger writes, repository mutation, and cluster mutation. |

### Constitutional Authority

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Who may invoke this worker? | ✓ | Operators may invoke it through the registered `seed` diagnostic flags, and internal code/tests may invoke the build/format/JSON functions directly. |
| Core | Who may consume its artifacts? | ? | CLI users, JSON consumers, tests, and diagnostic shape-audit/inventory-related consumers may consume its output. A complete consumer registry for every downstream reader is not implemented. |
| Core | Who may trust this artifact? | ✓ | Operators and internal diagnostic consumers may trust it when they need a read-only structural observation of selected repository Markdown documentation. |
| Core | What may be trusted? | ✓ | They may trust mechanical structural facts emitted from repository Markdown files selected by the surface: counts, headings, front matter presence, link target structure, fenced code block structure, explicit relation forms, recurrence summaries, exact section-label drilldown, exact section-label membership, and skeleton signatures. |
| Core | To what extent may it be trusted? | ✓ | It may be trusted as diagnostic structural evidence only. It is not claim truth, prose meaning, architectural authority, responsibility ownership, lexicon knowledge, shape authority, cluster truth, or mutation evidence. |
| Core | Under what assumptions does that trust remain lawful? | ✓ | Trust remains lawful only if the repository root and selected docs are the intended inputs, the invocation is bounded to the diagnostic surface, structural Markdown observation is the question being asked, and consumers preserve the surface's non-interpretive, read-only, non-recording, non-mutating boundary. |
| Core | What constitutional authority permits it to participate? | ✓ | Diagnostic inventory registers it as a diagnostic surface that uses repository files, supports JSON, does not support record, has `record_scope=none`, does not write the event ledger, and does not mutate the cluster. Diagnostic shape audit also names its implementation functions and checks its shape. |
| Core | What constitutional constraints limit it? | ✓ | It is limited to read-only structural documentation observation and must not become prose interpretation, claim extraction, authority inference, ontology promotion, event-ledger writing, repository mutation, cluster mutation, or a source of architectural truth. |
| Advanced | What would be an unlawful expansion of responsibility? | ✓ | Treating headings or links as verified claims, treating relation wording as recovered authority, writing diagnostic results as cluster facts, using this surface to rank work, mutating files, executing code, or promoting documentation vocabulary into preserved knowledge would exceed its authority. |

### Preconditions

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What must already be true before this competency can answer honestly? | ✓ | A repository root must be supplied; the operator or caller must have selected Documentation Structure; the invocation must be bounded to one document or top-level `docs/*.md` discovery; the selected files must be readable as bytes/text by the implementation; and the question must be answerable as structural Markdown observation rather than prose interpretation. |
| Core | Which preconditions are organism-level assumptions rather than observed evidence? | ✓ | Operator selection of this competency, the intended repository root, the bounded invocation purpose, and the consumer's agreement to use structural evidence structurally are assumptions of lawful use. They are not observations emitted by the competency. |
| Core | Which preconditions are not guaranteed by the artifact itself? | ✓ | The artifact does not by itself prove that the operator selected the best diagnostic, that the repository root was semantically correct, that the docs are complete, that documentation is truthful, or that downstream consumers will preserve the boundary. |

### Evidence

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What evidence can this worker observe? | ✓ | It can observe selected Markdown documentation files under the repository root, document bytes/text, line counts, blank/nonblank lines, front matter delimiters, headings, section labels, Markdown links, fenced code block boundaries, explicit architectural relation forms, and recurrence/skeleton patterns derived from observed structure. |
| Core | What evidence can it preserve? | ✓ | It preserves report data and rendered/JSON output for document summaries, per-document metrics, structural details when requested, recurrence rows, drilldown rows, membership rows, boundary metadata, and skeleton signature metrics. |
| Core | What evidence can it not observe? | ✓ | It cannot observe prose truth, implementation behavior, runtime reachability, operator intent, actual architectural ownership, responsibility recovery, lexicon stabilization, grammar meaning, cluster truth, or whether another diagnostic should act. |
| Core | What evidence permits movement? | ✓ | Movement from files to report is permitted by direct structural evidence in selected Markdown files and by the options selected for filtering, detail expansion, recurrence, drilldown, membership, and output bounds. |
| Core | What evidence causes lawful stop? | ✓ | The competency stops at structural output. It does not continue from an observed heading, relation phrase, link, or code fence into semantic interpretation, authority inference, responsibility ownership, claim extraction, event writing, or mutation. |

### Boundaries

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Where does this worker begin? | ✓ | It begins with a repository root, selected Documentation Structure options, and optionally a single document selector. |
| Core | Where does it end? | ✓ | It ends at a `DocumentationStructureReport`, JSON representation, or formatted diagnostic output. |
| Core | Which neighboring responsibilities does it deliberately avoid? | ✓ | It avoids claim extraction, prose interpretation, grammar interpretation, authority inference, responsibility recovery, lexicon stabilization, shape inference, ontology promotion, source-code parsing, event-ledger writing, repository mutation, and cluster mutation. |
| Advanced | Which recurring implementation evidence supports those boundaries? | ✓ | The module boundary text, recurrence and membership boundary text, diagnostic inventory entry, shape-audit implementation spec, and diagnostic inventory tests all repeat the same non-interpretive and non-mutating boundary. |

### Artifact Handoff

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What artifact leaves this worker? | ✓ | A `DocumentationStructureReport`, formatted text, or JSON-compatible structure leaves the worker. |
| Core | What minimum orientation survives? | ✓ | Diagnostic name, selected document if any, summary counts, per-document structural observations, option-shaped expansions, and explicit boundary metadata survive. |
| Core | What provenance survives? | ? | Repository-relative document paths and structural positions survive in the report where implemented. Full parser/version provenance, invocation timestamp, operator identity, and exhaustive downstream-consumer provenance do not survive. |
| Core | Who may consume the artifact? | ? | Operators, tests, diagnostic inventory/shape-audit consumers, and internal callers may consume it. A complete consumer registry is not implemented. |
| Core | What information is intentionally excluded? | ✓ | Prose meaning, claim truth, source-code interpretation, runtime behavior, ownership authority, responsibility assignment, lexicon stabilization, cluster facts, event-ledger records, and mutation effects are excluded. |

### Unknown / Stop

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What can remain unknown? | ✓ | Whether documentation statements are true, whether headings correspond to implementation authority, whether relation phrases are architecturally valid, whether links are semantically useful, whether docs are complete, whether consumers should act, and whether future diagnostics should split from this one can remain unknown. |
| Core | What unsupported conclusions are refused? | ✓ | A heading does not prove an implemented responsibility. A link does not prove dependency authority. A relation phrase does not prove ownership. A repeated section label does not prove ontology. A code fence does not prove runnable behavior. Structural recurrence does not prove architectural truth. |
| Core | How does the competency stop honestly? | ✓ | It reports structure and boundary metadata, then stops before interpretation, claim extraction, authority inference, event writing, mutation, or cluster truth. |
| Advanced | Which unanswered questions reveal real gaps? | ? | Complete consumer mapping, richer invocation provenance, and stronger downstream boundary enforcement are real gaps if this surface becomes a source for more automated consumers. |
| Evolutionary | Which unanswered questions are inappropriate for this maturity level? | ○ | Requiring semantic claim validation, runtime proof, responsibility ownership, or planner authority from this diagnostic would be inappropriate because those belong to different competencies. |

### Locality

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Why is this competency local? | ✓ | It is local because it observes Markdown documentation structure from repository files and emits diagnostic structural reports. |
| Core | Why has implementation rejected universal ownership? | ✓ | The boundary texts and inventory description reject interpretation, claim extraction, authority inference, shape inference, ontology promotion, event writing, and mutation. |
| Advanced | What would fail if this competency became universal? | ✓ | It would wrongly treat Markdown structure as authority over code behavior, architecture, runtime state, claim truth, responsibility ownership, lexicon knowledge, or future work selection. |

### Continuity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What public compatibility contract exists? | ✓ | The public contract includes registered CLI flags, JSON support, the build function, format function, JSON function, diagnostic inventory entry, and diagnostic shape-audit spec. |
| Core | What internal implementation freedom remains? | ✓ | Internals may change if they preserve the registered diagnostic surface, JSON/format/build behavior expected by tests, non-recording status, event-ledger boundary, mutation boundary, and structural/non-interpretive limits. |
| Core | What identity survives implementation evolution? | ✓ | Read-only structural observation of selected repository Markdown documentation survives. Prose interpretation, claim truth, architecture, responsibility recovery, event writing, and mutation remain outside identity. |
| Advanced | How is compatibility drift detected today? | ✓ | Diagnostic inventory tests and diagnostic shape-audit tests detect drift in registration, CLI flags, functions, JSON support, record boundary, event-ledger boundary, mutation boundary, and implementation markers. |

### Self-Observation / Drift

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | How can this competency be audited? | ✓ | It can be audited through `seed --diagnostic-inventory`, `seed --diagnostic-shape-audit`, direct tests, and direct invocation of its build/format/JSON functions. |
| Advanced | How is drift detected today? | ✓ | Drift is detected through the diagnostic inventory registry, diagnostic shape-audit implementation spec, and tests that prove the surface appears in inventory and is checked by shape audit. |
| Advanced | What diagnostic evidence already exists? | ✓ | Inventory registration, CLI flags, JSON support, `supports_record=False`, `record_scope=none`, `writes_event_ledger=False`, `mutates_cluster=False`, shape-audit function names, repository-file markers, and mutation markers exist. |
| Advanced | What important self-observation remains absent? | ? | Complete downstream-consumer registry, invocation-time provenance, and proof that every consumer preserves the non-interpretive boundary remain absent. |

### Evolution

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Evolutionary | Why did this competency emerge? | ? | Current implementation shows a mature diagnostic surface for structural documentation observation, but code alone does not fully prove historical causality. |
| Evolutionary | What architectural pressure produced it? | ? | Implementation suggests pressure to make document structure visible without interpreting prose or promoting authority, but historical pressure is only partially supported by implementation evidence. |
| Evolutionary | What future evidence could split it? | ✓ | Independently governed consumers or tests for recurrence, membership, drilldown, architectural relation forms, skeleton signatures, or link/code-fence structure could justify smaller competencies. |
| Evolutionary | What future evidence could simplify it? | ✓ | If consumers stop depending on recurrence, membership, drilldown, or skeleton signatures, those concerns could remain internal details or be removed without changing the core documentation-structure competency. |

## Recurring implementation evidence

Recurring evidence supports the same bounded conclusion:

1. **The module declares a read-only structural purpose.** Documentation Structure observes Markdown documentation structure and repeatedly refuses prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, event-ledger writes, repository mutation, and cluster mutation.
2. **The diagnostic inventory makes the operational surface visible.** The `documentation_structure` entry exposes CLI flags, repository-file use, JSON support, no recording support, `record_scope=none`, no event-ledger writes, and no cluster mutation.
3. **The diagnostic shape-audit spec checks implementation shape.** The spec names the module path, build function, format function, JSON function, CLI flags, repository-file markers, and mutation markers.
4. **The build function is bounded by selected repository docs.** It reads top-level `docs/*.md` files or one resolved document, applies options, and returns a report rather than mutating repository or cluster state.
5. **The formatter and JSON paths are handoff surfaces, not authority promotion.** They render or serialize structural report data without converting it into claim truth or ownership.
6. **The tests preserve visibility and drift boundaries.** Diagnostic inventory and shape-audit tests prove the operational surface is registered and checked.

## Constitutional observations

Documentation Structure Observation can answer a bounded constitutional oral examination:

- **What worker or implementation surface is being interrogated?** The `documentation_structure` diagnostic surface and its build/format/JSON functions.
- **What competency does that worker exercise?** Read-only structural observation of repository Markdown documentation.
- **What bounded responsibility does that competency own?** Mechanical document-structure reporting for selected top-level repository docs and option-selected structural views.
- **Who may trust this artifact?** Operators and internal diagnostic consumers may trust it for structural diagnostic orientation.
- **What may be trusted?** Mechanical structural observations over selected Markdown documentation.
- **To what extent may it be trusted?** Only as read-only diagnostic structure evidence, not as semantic truth, authority, ownership, or mutation evidence.
- **Under what assumptions does that trust remain lawful?** The repository root and document selection are intended, the invocation is bounded to Documentation Structure, and consumers preserve the non-interpretive and non-mutating boundary.
- **What must already be true before this competency can answer honestly?** A bounded repository/document invocation must exist, the selected documentation files must be available to the diagnostic, and the question must be structural rather than semantic.
- **What can Seed trust it for?** Seed can trust it for repository-document structure visibility.
- **What must Seed refuse to infer from it?** Seed must refuse claim truth, implementation behavior, architectural authority, responsibility ownership, lexicon stabilization, planner priority, event-ledger truth, repository mutation, and cluster mutation.
- **Which gaps are real?** Complete consumer mapping, invocation provenance, and downstream boundary enforcement remain real gaps for automated or delegated consumption.
- **Which unknowns are maturity-inappropriate demands?** Semantic validation, runtime proof, responsibility ownership, and planning authority are inappropriate demands for this diagnostic surface.

## Unsupported answers

The following answers remain unsupported or only partially supported:

- A complete list of all legitimate downstream consumers of Documentation Structure output.
- Proof that every downstream consumer preserves the non-interpretive boundary.
- Invocation timestamp, operator identity, and full environment provenance in every artifact.
- Proof that documentation prose is true.
- Proof that headings, relation phrases, links, or recurring skeletons correspond to implemented architecture.
- Proof that a structural observation should change work selection.
- Full implementation-only history of why the diagnostic emerged.

### Unanswered question classification

| Unanswered / partial question | Classification | Why |
| --- | --- | --- |
| Complete consumer map | consumer gap | The diagnostic has visible consumers and tests, but no exhaustive consumer registry was found. |
| Downstream boundary preservation | handoff gap | The artifact declares and carries boundaries, but implementation does not prove every consumer preserves them. |
| Invocation timestamp/operator/environment provenance | handoff gap | The diagnostic preserves document/report orientation, not full invocation provenance. |
| Whether documentation prose is true | authority gap | The competency explicitly refuses prose interpretation and claim extraction. |
| Whether headings or relation phrases prove implementation authority | authority gap | The diagnostic observes structure and explicit forms, not actual ownership or authority. |
| Whether structural recurrence should drive work selection | frontier | No work-selection authority is implemented for this surface. |
| Whether historical emergence is fully known from code | implementation gap | Current code proves present boundary better than historical causality. |
| Whether repeated structure vocabulary is repository knowledge | presentation-only | Structural labels and rendered signatures orient output; they do not promote vocabulary into preserved knowledge. |

## Constitutional oral examination

If Seed were asked to explain Documentation Structure Observation, he could answer truthfully only in bounded terms.

| Answer class | Result |
| --- | --- |
| Unknown | Complete consumer map; full downstream boundary preservation; invocation timestamp/operator/environment provenance; full historical emergence; whether future consumers need split competencies. |
| Unsupported | Any claim that the diagnostic proves prose truth, implementation behavior, architectural authority, responsibility ownership, lexicon knowledge, planner priority, event-ledger truth, repository mutation, or cluster mutation. |
| Operator-only | Repository root selection, document selection, and choice to invoke Documentation Structure are lawful-use preconditions, not structural facts observed by the diagnostic. |
| Presentation vocabulary | Headings, section labels, relation-form labels, recurrence labels, and skeleton signatures are structural output orientation, not constitutional knowledge or authority. |
| Implementation-backed | Read-only Markdown documentation structure observation; top-level docs discovery or selected document observation; structural metrics and option-selected detail reports; inventory registration; shape-audit coverage; JSON support; no recording; `record_scope=none`; no event-ledger writes; no cluster mutation. |

## Constitutional reliance

Seed may rely on this competency to:

- observe selected repository Markdown documentation as structure;
- render or serialize structural documentation diagnostics;
- expose Documentation Structure through diagnostic inventory;
- be checked by diagnostic shape audit;
- preserve a read-only, non-recording, non-event-writing, non-cluster-mutating operational boundary.

Seed must not rely on this competency to:

- decide whether documentation claims are true;
- infer implementation behavior from prose, headings, links, code fences, relation forms, recurrence, membership, drilldown, or skeleton signatures;
- recover responsibility ownership;
- infer architectural authority;
- stabilize lexicon or ontology;
- select or prioritize work;
- write event-ledger facts;
- mutate repository or cluster state.

## Lawful termination

**Operationally visible structural competency characterized; semantic and consumer handoff gaps preserved.**

This is the smallest truthful stopping condition supported by implementation. Documentation Structure Observation is mature as an operational diagnostic surface because it is registered in diagnostic inventory, checked by diagnostic shape audit, supports JSON, and preserves explicit non-recording, non-event-writing, and non-mutating boundaries. It is not mature as prose truth, architectural authority, responsibility recovery, lexicon stabilization, planner authority, or universal documentation knowledge.

The lawful stop is therefore not to generalize Documentation Structure into semantic documentation understanding. The lawful stop is to rely on it only for structural documentation visibility and preserve unanswered consumer/handoff/authority gaps as evidence.

## Remaining questions

- Which downstream consumers consume Documentation Structure output, and do all preserve the structural/non-interpretive boundary?
- Would invocation provenance improve handoff without implying semantic authority?
- Are recurrence, membership, drilldown, architectural relation forms, or skeleton signatures becoming independent competencies, or are they still option-shaped views inside Documentation Structure?
- Should any future consumer require a separate evidence interpretation step before using structural documentation observations in architectural inquiry?
- Does repeated use of Competency Interrogation continue to recover constitutional trust boundaries rather than merely document competencies?

## Methodology observation, non-normative

This interrogation again suggests that Competency Interrogation may be recovering trust boundaries: what can be trusted, to what extent, and under what assumptions. This remains only an observation from repeated use. It is not stabilized vocabulary, not constitutional doctrine, and not repository knowledge. If the pattern continues recurring across future interrogations, it should be preserved through a separate honesty or methodology investigation rather than silently promoted here.

## Confidence

**High** for bounded identity, operational diagnostic visibility, inventory registration, shape-audit coverage, read-only structure observation, JSON support, no recording, `record_scope=none`, no event-ledger writes, no cluster mutation, and explicit refusal boundaries.

**Medium** for downstream consumer and handoff conclusions, because the surface is visible and tested but no exhaustive consumer registry or invocation-provenance artifact was found.

**Low** for historical emergence and future split/simplification paths, because those answers depend on future consumer pressure and repository history beyond the current implementation boundary.
