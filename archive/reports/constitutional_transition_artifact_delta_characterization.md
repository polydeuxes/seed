# Constitutional Transition Artifact Delta Characterization

## Evidence reviewed

This characterization reviews implementation-backed transition families, not transition vocabulary. The main evidence reviewed was:

- `seed_runtime/inquiry_orientation.py` and `tests/test_inquiry_orientation.py` for communication-to-orientation behavior.
- `seed_runtime/capability_candidates.py`, `seed_runtime/verification_evidence.py`, `seed_runtime/capability_verification.py`, `seed_runtime/capability_inventory.py`, `tests/test_verification_evidence.py`, and related capability tests for candidate, acquired support, verification, and admission boundaries.
- `seed_runtime/state.py`, `tests/test_state_projector.py`, `tests/test_fact_support_aggregation.py`, and `tests/test_fact_extraction.py` for event replay, evidence admission, fact projection, inferred facts, fact support, and projection publication.
- `seed_runtime/inquiry_artifacts.py`, `seed_runtime/diagnostic_shape_audit.py`, and `seed_runtime/question_surface_inventory.py` for repository-visible diagnostic/read-only surfaces and visibility boundaries.
- Existing recovered investigations named in the prompt were used only as prompts to re-check implementation evidence; their prose was not treated as authority when implementation evidence was more specific.

## Answer

Recurring constitutional transitions are often clarified by artifact deltas, but they are not best reduced to one generic artifact-delta compression.

The strongest implementation-backed answer is:

> Constitutional transition families are distinguished by which artifact becomes visible, supported, admitted, projected, or authority-bearing, and by which artifacts explicitly do **not** change.

That means artifact deltas clarify recurring distinctions that prose labels obscure. However, some recurring transitions are deliberately non-durable: orientation is the clearest case. It records operator prose in an isolated probe store and renders future lawful possibility by relating that note to already projected material, but it does not create facts, goals, tool needs, decisions, proposals, plans, authorizations, runtime instructions, or cluster truth.

Therefore artifact analysis is useful, but not sufficient as a universal compression. Repository authority supports a family-by-family artifact delta characterization, not a single transition engine and not a redesigned family taxonomy.

## Transition families reviewed

### 1. Communication to orientation

**Implementation evidence.** Inquiry orientation stores a raw inquiry note outside the event ledger, then builds a read-only view from projected state using deterministic lexical overlap. The module's authority boundary says the note is preserved operator prose and not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction. Tests prove that recording a note does not change facts, goals, tool needs, authorizations, proposals, pending actions, plans, handoff plans, or tools.

**Artifact delta.**

- **Before:** projected state, optional event ledger contents, and no selected inquiry-note record for this probe.
- **After:** an `InquiryNoteRecord` exists in an isolated JSONL probe store; an `InquiryOrientationView` may be rendered from the note and already projected state.
- **Unchanged:** event ledger, projected facts, observed facts, inferred facts, goals, tool needs, execution authorizations, execution proposals, pending actions, action plans, handoff plans, tools, and cluster truth.
- **Newly created:** the preserved inquiry-note record; a transient orientation view/output when rendered.
- **Gains authority:** no repository fact or operational artifact gains authority. The note has provenance as preserved operator prose only.
- **Gains evidence:** the note gains minimal provenance (`note_id`, timestamp, source, workspace/session when provided). Related material gains display support from lexical overlap, not semantic proof.
- **Merely gains visibility:** potentially related projected facts or source-navigation matches become visible in the orientation rendering.
- **Disappears:** nothing in state disappears.
- **Defining change:** preservation of operator prose plus read-only orientation visibility; no durable constitutional state changes beyond the isolated note record.

**Orientation-specific conclusion.** Orientation primarily changes future lawful possibility, not repository truth. It creates a bounded surface that lets future work start from preserved communication and visible related material, while preserving a negative authority boundary. Orientation is not evidence acquisition and not admission.

### 2. Bounded inquiry / diagnostic visibility surfaces

**Implementation evidence.** Diagnostic inventory and shape audit register and inspect diagnostic surfaces as declared shapes. Inquiry artifact visibility classifies known inquiry artifacts from implementation payloads and explicitly says some categories are surface outputs or unsupported as generalized artifacts.

**Artifact delta.**

- **Before:** implementation surfaces exist in code, tests, and CLI flags, but may not be visible through a specific inventory/audit rendering.
- **After:** diagnostic or inquiry artifact rows are rendered as read-only visibility over existing implementation declarations.
- **Unchanged:** state projection, facts, evidence, event ledger, and operational authority.
- **Newly created:** transient diagnostic/audit output; no necessarily durable repository artifact unless a `--record` diagnostic explicitly records a diagnostic run.
- **Gains authority:** a surface gains inventory/audit visibility, not domain authority.
- **Gains evidence:** the row gains implementation-reference support when the audit verifies module/function/format/json/CLI shape.
- **Merely gains visibility:** most of this family is visibility.
- **Disappears:** nothing by default.
- **Defining change:** an already existing surface becomes inspectable as a registered diagnostic/read-only artifact shape. Visibility is the delta; knowledge is not automatically changed.

### 3. Evidence acquisition

**Implementation evidence.** Verification evidence acquisition checks only local filesystem PATH metadata for binaries associated with existing capability candidates. It never invokes binaries and never promotes evidence into `capability_verified` facts. Tests prove no executor or policy evaluation is used and the ledger event count remains unchanged for the CLI inspection.

**Artifact delta.**

- **Before:** candidate capability artifacts may exist from package facts; no acquired verification-evidence row for observed executable binary path.
- **After:** a `VerificationEvidenceInspection` may contain `VerificationEvidence` records such as `binary_path_observed` with source `local_path_inspection`.
- **Unchanged:** projected facts, `capability_verified` facts, execution proposals, pending actions, event ledger, policy state, and execution authority.
- **Newly created:** transient evidence-inspection records.
- **Gains authority:** no capability gains verification authority.
- **Gains evidence:** a candidate gains acquired support evidence for inspection only.
- **Merely gains visibility:** local PATH/binary metadata becomes visible.
- **Disappears:** nothing.
- **Defining change:** candidate-adjacent support evidence is acquired and preserved as inspection output without admission, selection, permission, or execution.

### 4. Candidate/support

**Implementation evidence.** Capability candidates are built from projected `package_installed` facts. The candidate module states that a candidate is not capability proof, execution authority, execution decision, policy evaluation, or tool invocation. Candidate records include supporting fact/evidence summaries and boundary notes.

**Artifact delta.**

- **Before:** package facts may exist in projected state.
- **After:** `CapabilityCandidateInspection` exposes `CapabilityCandidate` records derived from selected package fact values.
- **Unchanged:** the underlying package facts, event ledger, verified capability facts, execution decisions, policy state, and tool invocation state.
- **Newly created:** transient candidate records and candidate evidence summaries.
- **Gains authority:** no verified capability authority is gained.
- **Gains evidence:** candidate records carry support from fact IDs, evidence IDs, source type, confidence, and summaries.
- **Merely gains visibility:** possible capability names become visible.
- **Disappears:** nothing.
- **Defining change:** package-derived observed support is re-expressed as a candidate artifact while preserving the negative boundary that candidate is not verified.

### 5. Candidate to verified inspection

**Implementation evidence.** Capability verification inspection joins candidates to existing capability inventory. The implementation states verification status comes only from existing capability inventory backed by projected `capability_verified` facts. Without such a fact, the candidate remains `unverified`, even if package evidence and acquired binary evidence exist.

**Artifact delta.**

- **Before:** candidate records may exist; acquired verification evidence may exist; `capability_verified` facts may or may not exist.
- **After:** `CapabilityVerificationInspection` renders each candidate with a verification status.
- **Unchanged:** candidates remain candidates; acquired evidence remains support; missing `capability_verified` facts remain missing; no execution authority appears.
- **Newly created:** transient verification-inspection rows.
- **Gains authority:** only when an already projected `capability_verified` fact exists does the inspection reflect verified/stale/provider-reported authority from inventory semantics. The inspection itself does not create authority.
- **Gains evidence:** rows may display verification-supporting facts and evidence from the admitted inventory entry.
- **Merely gains visibility:** candidate verification status becomes visible.
- **Disappears:** nothing.
- **Defining change:** the inspected status changes from candidate-only to candidate-with-verification-status, but verification authority is imported from pre-existing projected facts, not generated by inspection.

### 6. Admission

**Implementation evidence.** Capability inventory separates admitted capability state from operation contract metadata and requested capabilities. Admission is represented by projected `capability_verified` facts; inventory presentation consumes admitted state but does not own admission or create promotion facts.

**Artifact delta.**

- **Before:** a capability may be requested, named by a tool contract, or preserved as candidate support, without being admitted as repository capability knowledge.
- **After:** if a `capability_verified` fact exists in projected state, inventory can present the capability as verified, provider-reported, stale, unknown, or unverified according to fact support.
- **Unchanged:** tool contracts remain operation metadata; requests remain needs; candidates remain candidates; inventory remains read-only.
- **Newly created:** no admission artifact is created by inventory. Admission requires an already existing projected fact from event replay.
- **Gains authority:** the capability subject gains admitted repository capability knowledge only through the projected `capability_verified` fact and its support.
- **Gains evidence:** supporting facts/evidence are attached through fact support and evidence graph summaries.
- **Merely gains visibility:** inventory renders the admitted state.
- **Disappears:** no deletion is evidenced in this family.
- **Defining change:** a `capability_verified` fact exists as projected knowledge for the capability subject. Support or presentation alone does not define admission.

### 7. Fact projection

**Implementation evidence.** State projection replays `evidence.observed`, `fact.observed`, and `fact.inferred` events into state. Finalization partitions observed and inferred facts, runs deterministic inference from current observed facts, rebuilds `state.facts`, builds fact supports, relationships, entity type assertions, graph issues, aliases, and conflicts, then publishes the finalized state.

**Artifact delta.**

- **Before:** append-only events exist in the ledger; projection may be absent, stale, or not yet finalized for a consumer.
- **After:** a finalized `State` exists with evidence, facts, observed/inferred partitions, fact supports, relationships, graph issues, aliases, and conflicts rebuilt from the event stream.
- **Unchanged:** source events remain append-only inputs; finalization does not rewrite event history.
- **Newly created:** projected state collections and derived indexes/read models.
- **Gains authority:** projected current facts and fact supports gain consumer-visible authority as the current read model of ledger events.
- **Gains evidence:** fact support aggregates supporting fact IDs, source types, confidence, observation times, expiry, and support kind.
- **Merely gains visibility:** projection-publication handoff makes finalized state visible to consumers without changing compatibility behavior.
- **Disappears:** some historical measurement samples or pruned measurement evidence may disappear from current projected read models due to retention/provenance pruning, but deletion/replacement semantics are limited to projection state, not ledger history.
- **Defining change:** ledger events become consumer-visible projected state and support structures through replay plus finalization. Projection is not the same as fact existence in the event ledger; projection is the current read model over events.

### 8. Implementation recovery

**Implementation evidence.** Source-navigation and repository-observation surfaces recover implementation-backed facts such as imports, definitions, repository state, and source-navigation matches. Orientation consumes source-navigation matches only as related material. Structure observation explicitly says it has no grammar interpretation, responsibility recovery, lexicon stabilization, or ownership promotion.

**Artifact delta.**

- **Before:** implementation artifacts exist as files, AST nodes, definitions, imports, repository status, or projected source facts.
- **After:** read-only recovery surfaces expose bounded structural observations or source-navigation rows.
- **Unchanged:** source files, operational authority, ownership, runtime behavior, and repository knowledge unless facts are separately observed/projected.
- **Newly created:** transient observation/recovery rows, or projected facts when the event pipeline admits them.
- **Gains authority:** bounded structural claims gain authority only to the extent they are backed by observed implementation evidence and admitted/projected facts.
- **Gains evidence:** source path, symbol, predicate, line/path metadata, and evidence IDs may support the recovered artifact.
- **Merely gains visibility:** many recovery surfaces only expose already existing implementation shape.
- **Disappears:** no supported recurring deletion.
- **Defining change:** implementation structure becomes bounded observed support; it does not automatically become responsibility, ownership, or constitutional vocabulary.

### 9. Methodology promotion

**Implementation evidence.** The reviewed code supports many read-only methodology surfaces and recovered investigations, but implementation promotion is not a generic engine. The closest implementation-backed pattern is that a methodology claim gains repository authority only when backed by code, tests, events, diagnostics, or projected facts. Presentation vocabulary alone is explicitly not repository knowledge under the repository instructions.

**Artifact delta.**

- **Before:** prose, labels, investigation conclusions, or recurring patterns may exist.
- **After:** when implementation-backed, a methodology may be preserved in a repository document or diagnostic/read-only surface with specific evidence references.
- **Unchanged:** runtime machinery and state mutation boundaries unless implementation actually changes them.
- **Newly created:** a document or diagnostic visibility artifact, not a transition engine.
- **Gains authority:** only claims directly supported by implementation evidence gain authority.
- **Gains evidence:** citations to files, tests, records, events, or behavior.
- **Merely gains visibility:** unsupported vocabulary remains visibility/presentation only.
- **Disappears:** no supported recurring deletion.
- **Defining change:** prose becomes repository-supported characterization only by attaching implementation evidence and preserving unsupported/unknown boundaries. The transition is not “promotion” in the abstract; it is evidence-backed preservation.

## Artifact delta analysis

### Visibility != Knowledge

This distinction is fundamentally artifact-delta based. Diagnostic rows, inquiry-artifact rows, orientation related material, capability candidate rows, and source-navigation matches can all become visible without creating projected facts or admitted authority. The delta is a visibility artifact, not a knowledge artifact.

### Support != Admission

This distinction is artifact-delta based. Package facts and binary-path observations support candidate or verification inspection rows. Admission requires a projected authoritative fact such as `capability_verified`. Support artifacts can accumulate without changing admitted repository knowledge.

### Candidate != Verified

This distinction is artifact-delta based. A `CapabilityCandidate` exists after package-derived candidate preservation. A verified status depends on capability inventory and projected `capability_verified` facts. Candidate artifacts and verified-capability artifacts have different authority and evidence deltas.

### Orientation != Evidence

This distinction is artifact-delta based but with a non-durable-state caveat. Orientation creates/preserves a note and renders lexical relatedness. It does not create evidence events, facts, claims, goals, needs, decisions, proposals, plans, or commands. Orientation changes future lawful possibility and visibility, not evidentiary truth.

### Projection != Fact

This distinction is artifact-delta based. A fact event can exist in the ledger; projection builds the current consumer-visible read model, partitions observed and inferred facts, applies current-belief selection, aggregates fact supports, and derives indexes. Projection changes visibility and current read-model authority; it is not identical to the underlying fact event.

## Recurrence analysis

Recurring transitions appear to be defined more reliably by artifact deltas than by prose labels, but only if the analysis includes unchanged artifacts and negative boundaries.

The reliable recurring question is not “what movement occurred?” It is:

1. Which artifact existed before?
2. Which artifact exists afterward?
3. Did the event ledger change?
4. Did projected state change?
5. Did a fact, support, candidate, evidence row, view, or diagnostic row appear?
6. Did any artifact gain authority, or only visibility?
7. What did tests prove stayed unchanged?

This explains why the same prose label can hide different transitions. “Promotion” might mean candidate support became visible, a verified fact existed, a document preserved a supported characterization, or nothing durable changed. Artifact deltas separate those cases.

## Negative analysis

Recurring mistakes caused by prose-only transition descriptions include:

- **“Movement.”** This hides whether the movement created an event, a fact, a view, a candidate, a support row, or only a rendered orientation surface.
- **“Promotion.”** This hides the difference between support accumulation and admission. Candidate evidence and binary-path evidence do not promote capability verification; `capability_verified` projected facts are the relevant admitted artifact.
- **“Interpretation.”** This hides local competency boundaries. Orientation uses deterministic lexical overlap; source recovery can expose definitions/imports; neither automatically interprets intent, ownership, responsibility, or next action.
- **“Processing.”** This hides read-only versus mutating behavior. Verification evidence “processing” inspects PATH metadata but does not execute tools, evaluate policy, append events, or mutate state.
- **“Projection.”** This can hide whether the source event exists, whether the current read model includes it, whether a support aggregate won current-belief selection, and whether the visible output is merely a view over projected state.

Artifact deltas expose distinctions hidden by those labels because they force the investigation to identify the artifact with authority and the artifacts deliberately left unchanged.

## Typed unknowns

The following remain typed unknowns because the reviewed implementation does not support a general answer:

- **Artifact deletion:** projection retention and pruning exist for current read-model/evidence visibility, but there is no reviewed generic constitutional deletion transition.
- **Artifact replacement:** current-belief selection and snapshot update patterns exist, but a generic replacement family is not supported.
- **Artifact supersession:** stale/expired support and best-support selection exist, but generic supersession semantics are not recovered.
- **Artifact lineage:** fact support and evidence graph preserve some lineage, but generic constitutional lineage across all families is not implemented.
- **Concurrent artifact deltas:** projection replay can rebuild multiple derived structures together, but the reviewed evidence does not support a general concurrent-transition model.
- **Composite transitions:** candidate/support/admission/projection can compose in practice, but the repository does not support a transition engine or generic composite transition type.

## Smallest truthful answer

The smallest recurring artifact change performed by the organism is:

> creation or rendering of a bounded read-only visibility artifact over already existing repository/state evidence, while preserving explicit non-authority boundaries.

This is smaller than durable knowledge mutation. It recurs in orientation views, diagnostic inventory/audit rows, candidate inspections, verification evidence inspections, capability verification inspections, source-navigation visibility, and inquiry artifact visibility.

If the question is restricted to durable cluster or projected repository truth, then the smallest answer is narrower:

> no durable artifact changes occur for several recurring transition families; durable knowledge changes require event/fact admission and projection, not mere transition recognition.

## Lawful termination

This investigation stops at characterization. It does not redesign transition families, invent a transition engine, recommend implementation, stabilize transition names, or assume that every transition changes durable repository state.

## Remaining questions

1. Which implemented event producers create `capability_verified` facts, and under what authority boundary?
2. Which projection-retention behaviors should be characterized as deletion, pruning, replacement, or current-view selection, if any?
3. Are there implementation-backed composite transitions where multiple artifact deltas are intentionally one constitutional unit?
4. Does any implemented family preserve supersession or lineage as a first-class artifact rather than as incidental support metadata?
5. Are methodology documents ever consumed by runtime/read-only surfaces as evidence, or are they only repository prose artifacts?

## Confidence

Confidence is **high** that artifact deltas clarify the distinctions requested: visibility versus knowledge, support versus admission, candidate versus verified, orientation versus evidence, and projection versus fact.

Confidence is **medium** that artifact deltas distinguish all recurring transition families better than prose labels. The evidence supports this for the reviewed families, but the typed unknowns prevent a universal compression.

Confidence is **high** that orientation primarily changes preserved communication and future lawful possibility, not durable repository truth.

Confidence is **high** that the repository does not support a transition engine or a redesigned family taxonomy from this evidence.
