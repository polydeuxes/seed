# Competency Interrogation 007

## Selected competency

**Inquiry Orientation**.

This interrogation selects Inquiry Orientation because repository evidence shows a mature but still constitutionally dangerous boundary: operator prose can be preserved and oriented without becoming fact, intent, command, ownership, recommendation, or next action. This selection is not based on novelty. It is based on implementation evidence in `seed_runtime/inquiry_orientation.py`, CLI exposure in `scripts/seed_local.py`, and preservation tests in `tests/test_inquiry_orientation.py`.

Smallest truthful answer:
Inquiry Orientation can preserve raw operator prose outside the event ledger and render deterministic lexical orientation against projected material; it cannot interpret intent, route work, create truth, authorize action, or recommend a next move.

## Implementation evidence reviewed

Implementation evidence reviewed:

- `seed_runtime/inquiry_orientation.py`
  - module purpose defines a minimized read-only inquiry-note orientation probe;
  - notes are stored outside the event ledger;
  - rendering reads projected state but does not mutate, append events, call providers, execute tools, or create facts, goals, tool needs, decisions, proposals, or plans;
  - `InquiryNoteRecord` preserves note id, raw note, recorded time, source, workspace id, and session id;
  - `AUTHORITY_BOUNDARY` explicitly refuses fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, importance, ownership, intent, concern, recommended action, and next safe move;
  - `_note_tokens()` tokenizes raw prose with minimum token length rather than semantic interpretation;
  - `_fact_matches()` and `_source_navigation_matches()` use deterministic lexical overlap against projected fact support and source-navigation material;
  - `_dedupe_related()` and `_MAX_RELATED_ITEMS` bound result presentation;
  - `_collect_architectural_orientation_evidence()`, `_compose_architectural_orientation_answer()`, and `format_inquiry_orientation()` split evidence collection, answer composition, and rendering.
- `scripts/seed_local.py`
  - `--record-inquiry-note TEXT` appends raw operator prose to the isolated inquiry-note probe store;
  - `--inquiry-orientation [NOTE_ID]` renders a bounded read-only orientation view for a selected or latest note;
  - record-and-render flow records only a note, then builds orientation from projected state and the selected note;
  - missing notes produce explicit failure rather than inferred content.
- `tests/test_inquiry_orientation.py`
  - raw note and minimal provenance are preserved;
  - inquiry notes are not projected into runtime state;
  - output includes required sections, supported matches, uncertainty, and authority boundary;
  - absence of related material is rendered explicitly;
  - orientation helper does not mutate state or create actions;
  - matches do not assert importance or ownership;
  - fact-support and source-navigation matches preserve surface-family labels;
  - surface-family labels do not add authority claims;
  - answer composition is separate from rendering.
- Adjacent repository evidence:
  - `representation_contract_boundary_investigation.md` identifies `InquiryOrientationView` as a boundary contract that refuses promotion from operator prose into repository truth;
  - `null_first_constitutional_transition_audit.md` treats inquiry-note preservation and Inquiry Orientation as the supported path for the smallest operator representation, while rejecting universal external-representation centralization;
  - `seed_competency_roadmap_v2.md` characterizes Inquiry Orientation as preserving operator notes as prose and matching only deterministic lexical overlap.
- App and checks run for this interrogation:
  - `python scripts/seed_local.py --help | rg -n "record-inquiry-note|inquiry-orientation|inquiry-artifacts"`
  - `python -m pytest -q tests/test_inquiry_orientation.py`

Smallest truthful answer:
The implementation supports bounded read-only orientation over preserved operator prose, not semantic interpretation or operational routing.

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
| Core | What worker or implementation surface is being interrogated? | ✓ | `record_inquiry_note()`, `load_inquiry_notes()`, `select_inquiry_note()`, `build_inquiry_orientation()`, `InquiryOrientationView`, `format_inquiry_orientation()`, and the `--record-inquiry-note` / `--inquiry-orientation` CLI path. |
| Core | What competency does that worker exercise? | ✓ | Read-only orientation over preserved operator prose using deterministic lexical overlap against already projected material. |
| Core | What constitutional role does this competency play inside the organism? | ✓ | The smallest supported role is **operator-prose boundary keeper**. This is descriptive only and not stabilized vocabulary. |
| Core | What bounded responsibility does that competency own? | ✓ | It owns preserving a raw inquiry note in an isolated probe store, selecting a note, collecting bounded lexical matches from projected facts and source navigation, composing an orientation answer, and rendering required orientation sections with uncertainty and authority boundary. |
| Core | Does implementation distinguish worker, competency, and responsibility? | ✓ | Yes. The workers are note persistence, orientation building, and formatting functions; the competency is inquiry orientation; the responsibility is bounded orientation without promotion, semantic interpretation, routing, mutation, or execution. |
| Core | What is this competency incapable of doing? | ✓ | It cannot create facts, goals, tool needs, requirements, capabilities, decisions, proposals, plans, authorizations, commands, runtime instructions, ownership assertions, intent claims, recommendations, next safe moves, provider calls, tool executions, or event-ledger truth. |
| Core | What is this competency constitutionally forbidden from doing? | ✓ | It is forbidden from treating operator prose as repository truth, deterministic overlap as semantic interpretation, related material as importance, and an orientation view as work selection, command, or authorization. |
| Core | What does it explicitly refuse to own? | ✓ | Its authority boundary refuses fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, importance, ownership, intent, concern, recommended action, and next safe move. |

Smallest truthful answer:
Inquiry Orientation is a preserved-prose orientation competency, not an intent interpreter.

### Constitutional Authority

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Who may invoke this worker? | ✓ | Operators may invoke it through `seed --record-inquiry-note` and `seed --inquiry-orientation`; tests and internal code may invoke the builder and formatter directly. |
| Core | Who may consume its artifacts? | ? | Operators, tests, CLI text consumers, and repository investigations may consume the output. A complete downstream consumer registry is not implemented. |
| Core | Who may trust this artifact? | ✓ | Consumers may trust it as a bounded read-only orientation view over a preserved note and projected material. |
| Core | What may be trusted? | ✓ | Raw note, note provenance, selected note identity, deterministic related material, surface family, support strings, uncertainty text, and authority boundary may be trusted as orientation output. |
| Core | To what extent may it be trusted? | ✓ | Only as lexical orientation. It is not evidence of operator intent, repository truth, importance, ownership, priority, task readiness, command, authorization, or next safe move. |
| Core | Under what assumptions does that trust remain lawful? | ✓ | Trust remains lawful only if the probe store is the intended note source, the projected state is the intended evidence base, lexical overlap is treated as possible relation rather than meaning, and consumers preserve the negative authority boundary. |
| Core | What constitutional authority permits it to participate? | ✓ | Participation is permitted by explicit operator note recording, isolated note storage, projected-state read access, deterministic matching, and CLI rendering. |
| Core | What constitutional constraints limit it? | ✓ | It is constrained to preserved raw prose, existing projected read models, source-navigation matches, bounded related-material count, uncertainty language, and read-only output. |
| Advanced | What would be an unlawful expansion of responsibility? | ✓ | Inferring intent, selecting a question family, routing work, creating facts from note text, ranking material by importance, asserting ownership, recommending action, creating plans, or mutating the event ledger would exceed authority. |

Smallest truthful answer:
Seed may trust Inquiry Orientation for bounded orientation only; it must not trust it for meaning or action.

### Preconditions

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What must already be true before this competency can answer honestly? | ✓ | A non-empty operator note must be recorded or selected; a projected `State` must exist; any related material must already be visible in projected fact support or source navigation. |
| Core | Which preconditions are organism-level assumptions rather than observed evidence? | ✓ | The legitimacy of the selected workspace, session, store path, and projected state are assumed by invocation. The operator's actual intent is not observed. |
| Core | Which preconditions are not guaranteed by the artifact itself? | ✓ | The artifact does not prove that matches are important, complete, intentional, actionable, owned, current, or semantically correct. |

Smallest truthful answer:
Inquiry Orientation begins after note preservation and projection; it does not establish the meaning of the note.

### Evidence

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What evidence can this worker observe? | ✓ | It observes raw note text and minimal provenance, note tokens, projected fact supports, source-navigation matches, surface-family labels, and support strings. |
| Core | What evidence can it preserve? | ✓ | It preserves the note record, related material rows, material type, label, surface, support, why-related explanation, surface family, uncertainty, and authority boundary. |
| Core | What evidence can it not observe? | ✓ | It cannot observe operator intent, priority, desired next action, ownership, semantic meaning, work readiness, permission, or runtime truth. |
| Core | What evidence permits movement? | ✓ | Non-empty raw note permits note preservation. Deterministic token overlap permits a related-material row. Missing overlap permits explicit no-related-material output. |
| Core | What evidence causes lawful stop? | ✓ | Empty note input raises an error. Missing note selection returns CLI failure. Missing related material produces explicit uncertainty. In all cases the competency stops before fact creation, semantic interpretation, routing, recommendation, authorization, planning, or execution. |

Observed:
The implementation stores notes outside the event ledger and derives related material only through deterministic lexical overlap.

Derived:
Operator communication can become preserved orientation evidence without becoming cluster truth.

Assumed:
The caller understands the output as orientation rather than selection or interpretation.

Smallest truthful answer:
Inquiry Orientation moves from prose to possible relation, never from prose to truth.

### Boundaries

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Where does this worker begin? | ✓ | It begins with a non-empty raw operator note or selected `InquiryNoteRecord` plus projected `State`. |
| Core | Where does it end? | ✓ | It ends at an `InquiryOrientationView` or formatted orientation text. |
| Core | Which neighboring responsibilities does it deliberately avoid? | ✓ | It avoids operator intent interpretation, candidate request derivation, question-family dispatch, source-navigation ownership, fact projection, requirement capture, task planning, action authorization, and execution. |
| Core | How does implementation distinguish note preservation, orientation, source navigation, answer composition, rendering, and authority? | ✓ | Note persistence is a JSONL probe store; orientation collection uses token overlap; source navigation is a separate builder; answer composition is a local dataclass; rendering formats sections; authority is a fixed boundary string. |
| Advanced | Which recurring implementation evidence supports those boundaries? | ✓ | Module docstring, dataclass separation, CLI help text, required output sections, no-projection tests, no-action tests, surface-family tests, and composition/rendering separation tests repeat the same boundary. |

Observed:
The implementation preserves raw note, related material, uncertainty, and boundary as separate fields.

Derived:
The method should not ask whether Seed "understands" the note, because implementation supports only bounded orientation.

Smallest truthful answer:
Inquiry Orientation begins with preserved prose and ends with bounded orientation text.

### Artifact Handoff

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What artifact leaves this worker? | ✓ | An `InquiryOrientationView` or formatted text with inquiry note, potentially related material, support/why-related, uncertainty, and authority boundary. |
| Core | What minimum orientation survives? | ✓ | Raw note, note id, provenance, related material, support strings, why-related explanation, surface family, uncertainty, and negative authority boundary survive. |
| Core | What provenance survives? | ? | Note id, source, recorded time, workspace id, session id, and support strings survive. Full operator identity, terminal invocation context, complete projection provenance, and consumer identity do not survive. |
| Core | Who may consume the artifact? | ? | Operators, tests, investigations, and text/CLI consumers may consume it. Complete consumer governance is absent. |
| Core | What information is intentionally excluded? | ✓ | Intent, importance, ownership, concern, requirement, recommended action, next safe move, authorization, plan, command, runtime instruction, and mutation effect are excluded. |

Smallest truthful answer:
The handoff artifact is an orientation view, not an interpretation record.

### Unknown / Stop

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What can remain unknown? | ✓ | Intent, meaning, priority, ownership, relevance completeness, actionability, authorization, work selection, and whether absent lexical overlap hides a real relation can remain unknown. |
| Core | What unsupported conclusions are refused? | ✓ | Operator prose is not fact. Lexical overlap is not semantic interpretation. Related material is not importance. Surface family is not authority. Orientation is not routing, recommendation, command, or next safe move. |
| Core | How does the competency stop honestly? | ✓ | It renders uncertainty and authority boundary, or fails on missing note, and does not mutate event ledger or projected state. |
| Advanced | Which unanswered questions reveal real gaps? | ? | Complete consumer governance, invocation provenance, note retention policy, multi-note comparison semantics, and downstream enforcement remain real gaps for stronger reliance. |
| Evolutionary | Which unanswered questions are inappropriate for this maturity level? | ○ | Requiring Inquiry Orientation itself to infer intent, rank importance, select work, or authorize execution is inappropriate because implementation explicitly refuses those responsibilities. |

Smallest truthful answer:
Inquiry Orientation can stop while meaning remains unknown.

### Locality

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | Why is this competency local? | ✓ | It is local because it handles one preserved note against already projected material and source navigation; it does not own universal intake, interpretation, routing, or planning. |
| Core | Why has implementation rejected universal ownership? | ✓ | It stores only inquiry notes, uses only lexical overlap, relies on existing projection/source navigation, and repeats authority exclusions rather than centralizing all operator communication. |
| Advanced | What would fail if this competency became universal? | ✓ | Operator prose would risk becoming repository truth, lexical overlap would become interpretation, orientation would become selection, and visibility would become action authority. |

Smallest truthful answer:
Inquiry Orientation is local to bounded note orientation.

### Continuity

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | What public compatibility contract exists? | ✓ | The contract includes `--record-inquiry-note`, `--inquiry-orientation`, note JSONL preservation, required text sections, surface-family rendering, uncertainty text, and authority-boundary language tested by unit tests. |
| Core | What internal implementation freedom remains? | ✓ | Internals may change if they preserve raw-prose isolation, deterministic bounded matching, read-only behavior, required output sections, and negative authority. |
| Core | What identity survives implementation evolution? | ✓ | Preserved-prose orientation survives. Intent interpretation, routing, fact creation, recommendations, and execution remain outside. |
| Advanced | How is compatibility drift detected today? | ✓ | Drift is detected by note preservation tests, projection non-mutation tests, output-section tests, absent-material tests, no-action tests, surface-family tests, and composition/rendering separation tests. |

Smallest truthful answer:
The continuity contract is bounded read-only orientation over raw note text.

### Self-Observation / Drift

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Core | How can this competency be audited? | ✓ | It can be audited through unit tests, CLI help, formatted output inspection, note-store contents, and state-before/state-after comparison. |
| Advanced | How is drift detected today? | ✓ | Drift is detected if tests show notes enter projected state, actions appear, authority boundary weakens, surface-family labels gain authority claims, or answer composition collapses into rendering. |
| Advanced | What diagnostic evidence already exists? | ? | CLI surfaces and tests exist. `--inquiry-artifacts` appears in diagnostic inventory and shape audit, but `--inquiry-orientation` itself is not shown by reviewed evidence as a diagnostic-inventory surface. |
| Advanced | What important self-observation remains absent? | ? | Complete consumer registry, retention policy, invocation provenance, note-store audit visibility, and downstream-use enforcement remain absent. |

Smallest truthful answer:
Inquiry Orientation is test-auditable but not fully governance-auditable.

### Evolution

| Level | Question | Mark | Implementation-supported answer |
| --- | --- | --- | --- |
| Evolutionary | What change would preserve identity? | ✓ | A different match implementation could preserve identity if it remained deterministic, bounded, projected-state-based, read-only, and explicit about uncertainty and negative authority. |
| Evolutionary | What change would alter identity? | ✓ | Adding semantic interpretation, work selection, fact creation, recommendation, authorization, command generation, or execution would alter identity. |
| Evolutionary | What future split may become justified? | ? | Note preservation, orientation evidence collection, answer composition, rendering, and note-store audit visibility are already distinguishable. Future separation may be justified if multiple consumers or retention requirements recur. |

Smallest truthful answer:
Future evolution must preserve the prose-to-orientation boundary.

## Neighbor Boundary Analysis

Which competency is most likely to be mistaken for this competency?

**Operator Intake** is the nearest constitutional neighbor. Operator Intake appears as the broader first-contact discipline: accepting operator-origin communication, preserving opacity, asking clarification when necessary, and stopping when no lawful continuation exists. Inquiry Orientation is a narrower implemented path: preserve a raw inquiry note and render bounded lexical orientation.

What recurring implementation evidence keeps their constitutional boundaries separate?

- Inquiry Orientation has concrete note-recording, note-selection, orientation-building, and formatting functions.
- Operator Intake remains broader architectural behavior in reviewed documents rather than a universal implemented intake gateway.
- Inquiry Orientation stores inquiry notes outside the event ledger, not all operator communications.
- Inquiry Orientation uses deterministic lexical overlap; Operator Intake discussions include candidate attachment, clarification, and explicit stop.
- Inquiry Orientation can render related material; it cannot decide whether clarification is required for every operator communication.
- Tests prove Inquiry Orientation avoids projection, action creation, importance, ownership, and recommendation authority.

If these competencies were accidentally merged,

what constitutional mistake

would the organism begin making?

Seed would risk treating every operator communication as eligible for inquiry-note orientation, or treating orientation output as a general intake decision. The smallest implementation-backed consequence is that raw operator prose could be promoted into inferred intent, route selection, or repository truth without implementation authority.

Smallest truthful answer:
The boundary prevents bounded orientation from becoming universal operator understanding.

## Constitutional methodology investigation

Working hypothesis evaluated using this competency only:

| Statement | Classification | Implementation-backed support |
| --- | --- | --- |
| Contrast recovers boundaries. | Supported | Contrast with Operator Intake and source navigation exposes that Inquiry Orientation owns neither universal intake nor source-navigation truth; it owns bounded orientation over a preserved note. |
| Invariants recover identity. | Supported | Recurring invariants are raw prose preservation, isolated probe storage, projected-state read-only access, deterministic lexical overlap, uncertainty, authority boundary, and no mutation/action. |
| Recurrence earns constitutional legitimacy. | Partially supported | The note/prose/no-authority boundary recurs in code, CLI help, tests, and prior investigations. However, recurrence across all possible operator-intake surfaces remains unproven. |
| Neighbor analysis discovers hallways. | Supported | The neighbor analysis shows a hallway from operator communication to inquiry-note preservation to orientation, while refusing to turn that hallway into universal intake or routing. |
| Interrogation discovers constitutional limits. | Supported | The interrogation exposes limits around intent, ownership, importance, recommendation, routing, projection, and action. |
| Typed unknowns preserve honesty. | Supported | Unknowns about intent, consumer governance, provenance, retention, and downstream enforcement remain named rather than inferred through. |

Smallest truthful answer:
For Inquiry Orientation, the method is more precise when it keeps orientation, intake, source navigation, and action separate.

## Additional constitutional question

What authority

does this competency

appear to possess,

but implementation

does not actually grant?

Inquiry Orientation appears to possess **operator intent interpretation authority** because it receives operator prose and returns related material.

Implementation does not grant that authority. The note is preserved as operator prose, matching is deterministic lexical overlap, uncertainty says related material may be incomplete or incidental, and the authority boundary explicitly denies intent, concern, recommendation, and next safe move.

**Independent recurrence observed.** Across Capability Verification, Capability Inventory, Pressure Audit, and Inquiry Orientation, visible status or related material repeatedly appears to grant stronger authority than implementation permits. In this case, orientation visibility appears to grant intent interpretation; implementation grants only bounded lexical orientation.

Smallest truthful answer:
Inquiry Orientation appears to understand the operator, but only preserves prose and shows possible lexical relations.

## Constitutional observations

Observed:

- Inquiry notes are stored outside the event ledger.
- Empty notes are rejected.
- A selected note or latest note is required for orientation.
- Orientation reads projected state.
- Related material is collected from fact support and source-navigation matches.
- Matching is token-based and deterministic.
- Related material is capped.
- Output always includes uncertainty and authority boundary.
- Tests prove no facts, goals, tool needs, authorizations, execution proposals, pending actions, action plans, handoff plans, or tools are created.

Derived:

- Raw operator prose can be preserved without becoming repository truth.
- Lexical relatedness is weaker than semantic interpretation.
- Orientation is weaker than selection.
- Surface-family labeling can help describe evidence source without adding authority.
- The competency's most important constitutional work is negative: preserving usefulness while refusing interpretation.

Assumed:

- The selected projected state is the intended evidence base.
- The note store path is the intended probe store.
- Consumers will not treat orientation as recommendation or action.

Smallest truthful answer:
Inquiry Orientation is useful because it lets Seed be addressed without pretending to understand.

## Constitutional reliance

Seed may rely on Inquiry Orientation to:

- preserve non-empty raw operator prose with minimal provenance;
- select a preserved inquiry note;
- find bounded deterministic lexical overlaps with projected fact support and source navigation;
- render related material with surface family and support;
- state uncertainty when matches exist or do not exist;
- preserve a strong authority boundary;
- remain read-only with respect to projected runtime state.

Seed must not rely on Inquiry Orientation to:

- infer operator intent;
- infer concern, importance, priority, ownership, or desired action;
- create facts, goals, requirements, tool needs, capabilities, decisions, proposals, plans, commands, or runtime instructions;
- select a question family or route work;
- authorize execution;
- mutate the event ledger or cluster truth;
- prove absence of related work when lexical overlap is absent.

Smallest truthful answer:
Inquiry Orientation may reduce disorientation; it may not decide what the operator meant.

## Methodology audit

Which question prevented the largest architectural overclaim?

**What authority does this competency appear to possess, but implementation does not actually grant?**

It prevented the overclaim that receiving operator prose and showing related material means Seed understands operator intent or can recommend a next safe move.

Which question produced the highest constitutional precision?

**What recurring implementation evidence keeps neighboring boundaries separate?**

The neighbor-boundary question separated Inquiry Orientation from Operator Intake, source navigation, question-family dispatch, and planning.

Which question generated the weakest evidence?

**Who may consume its artifacts?**

Operators, tests, CLI text consumers, and investigations are visible. Complete downstream consumer governance is absent.

Which question may still contain multiple compressed concerns?

**Who may trust this competency?**

It compresses caller identity, consumer identity, output reliability, lawful use, and downstream misuse prevention. The implementation supports output reliability better than it supports consumer governance.

Did implementation collapse previously distinct concepts?

No. Implementation separates note preservation, evidence collection, answer composition, rendering, uncertainty, and authority boundary.

Did implementation split previously compressed concepts?

Yes. The apparent phrase "inquiry orientation" could compress intake, interpretation, routing, source navigation, answer composition, and recommendation. Implementation splits these into narrower steps and refusals.

Did the interrogation discipline change?

**No redesign.**

This interrogation retains the recovered methodology from Competency Interrogation 006 and adds the required audit of the interrogation discipline itself. No new competency question is stabilized.

Smallest truthful answer:
The method again gained precision from negative authority and neighbor contrast, not from new conceptual machinery.

## Interrogation Discipline Audit

This section treats the interrogation itself as a constitutional artifact. Evidence is limited to Competency Interrogations 001-007 and the implementation-backed results they produced.

### Question legitimacy

For every major interrogation section:

| Major section / question group | Why does this question exist? | Recurring constitutional mistake prevented | Unique evidence? | Survival |
| --- | --- | --- | --- | --- |
| Selected competency | To force a repository-evidence reason for choosing the subject. | Choosing by novelty, elegance, or operator curiosity rather than implementation pressure. | Yes; each interrogation explains why this competency was selected now. | Essential |
| Implementation evidence reviewed | To bind claims to files, tests, CLI surfaces, and app behavior. | Philosophizing from vocabulary or documents alone. | Yes; no other section fully enumerates evidence. | Essential |
| Identity | To recover worker, competency, role, responsibility, incapability, and forbidden expansion. | Treating a surface name as a constitutional owner. | Yes; it produces the smallest identity boundary. | Essential |
| Constitutional Authority | To distinguish trust, invocation, consumption, authority, and constraints. | Treating visibility, verification, or orientation as permission. | Yes; especially in Capability Verification, Capability Inventory, Pressure Audit, and Inquiry Orientation. | Essential |
| Preconditions | To name what must already be true before the competency can answer. | Letting the artifact appear self-grounding. | Yes, but partially overlaps with Evidence and Unknown/Stop. | Useful |
| Evidence | To distinguish observable, preservable, absent, movement-permitting, and stop-causing evidence. | Promoting weak evidence into truth or action. | Yes; this question repeatedly finds the lawful movement boundary. | Essential |
| Boundaries | To locate beginning, ending, neighbors, and deliberate avoidance. | Expanding local competency into universal ownership. | Yes; neighbor and boundary evidence repeatedly produces unique distinctions. | Essential |
| Artifact Handoff | To identify what leaves the worker and what survives. | Treating internal local state as crossed-boundary knowledge. | Yes, especially provenance gaps. | Useful |
| Unknown / Stop | To preserve lawful ignorance and termination. | Inferring through missing evidence. | Yes; typed unknowns are not fully recovered elsewhere. | Essential |
| Locality | To prevent universalization. | Turning a local competency into a planner, coordinator, registry, or gateway. | Partially; often overlaps with Boundaries. | Useful |
| Continuity | To identify compatibility and identity across evolution. | Mistaking implementation freedom for constitutional freedom. | Yes for CLI/test-backed surfaces; weaker for document-only neighbors. | Useful |
| Self-Observation / Drift | To ask how the boundary is tested and audited. | Making invisible operational drift. | Yes for diagnostic/CLI/test-backed surfaces. | Useful |
| Evolution | To distinguish identity-preserving change from identity-changing expansion. | Freezing implementation details or permitting unlawful growth. | Partially; often duplicates Identity and Boundaries. | Useful |
| Neighbor Boundary Analysis | To compare the nearest mistaken competency. | Collapsing adjacent competencies with similar appearances. | Yes; it has repeatedly produced high-precision boundaries. | Essential |
| Negative authority | To name apparent authority not granted by implementation. | Treating output appearance as constitutional permission. | Yes; independent recurrence is now observed again. | Essential |
| Constitutional observations | To separate observed, derived, and assumed claims. | Mixing evidence classes. | Yes; it is the main honesty ledger. | Essential |
| Constitutional reliance | To state what Seed may and must not rely on. | Overusing a truthful artifact outside its authority. | Yes; it turns interrogation into lawful use constraints. | Essential |
| Methodology audit | To evaluate the interrogation's own precision. | Preserving questions because they are elegant. | Yes; it identifies weak, compressed, and high-value questions. | Useful |
| Methodology honesty candidates | To preserve recurring observations without stabilizing vocabulary. | Turning repeated phrasing into constitutional law too early. | Yes; unique vocabulary-honesty function. | Useful |
| Constitutional reflection | To reduce loss/expansion claims to smallest truthful capability. | Inflating importance of a competency. | Yes; produces minimal disappearance consequence. | Essential |
| Lawful termination | To stop at implementation boundary. | Continuing into redesign, recommendation, or aspiration. | Yes; explicit stop prevents methodology sprawl. | Essential |
| Remaining questions | To preserve gaps without inventing answers. | Treating unknowns as defects requiring immediate architecture. | Yes; unique gap preservation. | Useful |
| Confidence | To calibrate certainty. | Presenting bounded findings as complete recovery. | Yes; unique confidence calibration. | Essential |

Smallest truthful answer:
Most questions have earned a place, but not all have earned equal permanence.

### Question survival

Essential questions:

- Selected competency.
- Implementation evidence reviewed.
- Identity.
- Constitutional Authority.
- Evidence.
- Boundaries.
- Unknown / Stop.
- Neighbor Boundary Analysis.
- Negative authority.
- Constitutional observations.
- Constitutional reliance.
- Constitutional reflection.
- Lawful termination.
- Confidence.

Useful questions:

- Preconditions.
- Artifact Handoff.
- Locality.
- Continuity.
- Self-Observation / Drift.
- Evolution.
- Methodology audit.
- Methodology honesty candidates.
- Remaining questions.

Redundant questions:

- None have earned removal yet. Some overlap, but the overlap has not always moved together.

Insufficient evidence:

- Whether Evolution should remain a major section for every small competency.
- Whether Locality should remain separate from Boundaries.
- Whether Artifact Handoff and Constitutional reliance should remain separate for non-handoff surfaces.

Smallest truthful answer:
The interrogation has become more precise, but several useful questions have not yet earned permanence.

### Reduction Challenge

If this question disappeared,

what constitutional mistake

would become easier to make?

| Question group | Mistake made easier if removed | Earned permanence? |
| --- | --- | --- |
| Selected competency | Selecting by novelty or attachment rather than repository evidence. | Yes |
| Implementation evidence reviewed | Making unsupported constitutional claims. | Yes |
| Identity | Confusing surface, worker, competency, responsibility, and role. | Yes |
| Constitutional Authority | Treating output as permission or trust without scope. | Yes |
| Preconditions | Treating artifact output as self-grounding. | Not permanent alone; useful. |
| Evidence | Letting evidence source, movement, and stop collapse. | Yes |
| Boundaries | Universalizing a local competency. | Yes |
| Artifact Handoff | Losing what survives across boundaries. | Not permanent alone; useful. |
| Unknown / Stop | Inferring through unknowns. | Yes |
| Locality | Promoting local behavior into universal governance. | Not permanent alone; useful. |
| Continuity | Breaking public contracts or freezing internals. | Not permanent alone; useful. |
| Self-Observation / Drift | Letting invisible drift pass as stable behavior. | Not permanent alone; useful. |
| Evolution | Treating all change as either forbidden or free. | Insufficient permanence evidence. |
| Neighbor Boundary Analysis | Merging adjacent surfaces by similar appearance. | Yes |
| Negative authority | Mistaking apparent authority for granted authority. | Yes |
| Constitutional observations | Mixing observed, derived, and assumed material. | Yes |
| Constitutional reliance | Overusing the artifact after truthful characterization. | Yes |
| Methodology audit | Expanding the method without examining it. | Useful, not proven permanent for every interrogation. |
| Methodology honesty candidates | Stabilizing vocabulary prematurely. | Useful. |
| Constitutional reflection | Inflating disappearance consequences. | Yes |
| Lawful termination | Continuing into redesign or recommendation. | Yes |
| Remaining questions | Hiding gaps or inventing closure. | Useful. |
| Confidence | Overstating certainty. | Yes |

Smallest truthful answer:
Reduction is not yet justified by redundancy, but permanence is not equally earned.

### Question compression

Questions that still appear to ask more than one constitutional concern:

| Current question | Hidden concerns | Evidence supporting future separation |
| --- | --- | --- |
| Who may trust this competency? | Caller identity, consumer identity, trusted fields, trust scope, lawful-use assumptions. | Capability Inventory, Capability Verification, and Inquiry Orientation all had stronger evidence for trusted fields than for complete consumer governance. |
| Who may consume its artifacts? | Existing consumers, allowed consumers, downstream governance, public compatibility. | Repeated weak evidence in Capability Verification, Capability Inventory, and Inquiry Orientation. |
| What constitutional role does this competency play? | Descriptive role, stabilized vocabulary risk, responsibility identity, organism position. | Repeated caution not to stabilize labels such as confidence-boundary keeper or operator-prose boundary keeper. |
| Which unanswered questions reveal real gaps? | Implementation gaps, governance gaps, future maturity, inappropriate demands. | Unknown/Stop sections repeatedly mix missing provenance, consumer registry, policy sufficiency, stale refresh, and authorization linkage. |
| How can this competency be audited? | Unit tests, CLI behavior, diagnostic inventory, shape audit, runtime observability, drift detection. | Pressure Audit and diagnostic surfaces have stronger operational audit requirements than Inquiry Orientation and capability surfaces. |
| What would be an unlawful expansion? | Forbidden behavior, neighbor collapse, identity change, authority misuse. | Negative authority and Boundaries often recover the same but from different angles. |

Do not separate them yet.

Smallest truthful answer:
Compression exists mostly around trust, consumers, role, auditability, and unlawful expansion.

### Question reduction

Identify any pair of questions whose answers have always moved together.

| Pair | Have these earned merger? | Reason |
| --- | --- | --- |
| Locality / Boundaries | Not yet | Locality often repeats boundary evidence, but it uniquely prevents universal ownership claims. |
| Preconditions / Evidence | No | Preconditions expose assumptions before answer; Evidence exposes movement and stop. |
| Artifact Handoff / Constitutional reliance | No | Handoff asks what leaves; reliance asks how Seed may use it. |
| Self-Observation / Continuity | Not yet | Both use tests, but continuity concerns compatibility while self-observation concerns drift detection. |
| Evolution / Identity | Probably | Evolution often restates identity-preserving versus identity-changing boundaries already recovered in Identity and Boundaries. More interrogations are needed before removal. |
| Methodology audit / Interrogation Discipline Audit | Not yet | The new audit is broader and question-level; prior methodology audit is competency-local. |
| Negative authority / Constitutional Authority | No | Authority asks granted trust; negative authority asks apparent but ungranted power. Their answers are related but not identical. |

Smallest truthful answer:
Only Evolution and Identity/Boundaries are plausible future merger candidates, and even that is not yet justified.

### Question gaps

Which constitutional mistakes

still escape

the interrogation?

Only implementation-backed recurrence may justify answers.

Recurring escaped or weakly caught mistakes:

- **Consumer-governance overclaim.** Interrogations repeatedly identify consumers but lack complete consumer registries. This affects Capability Verification, Capability Inventory, and Inquiry Orientation.
- **Invocation provenance weakness.** Artifacts often preserve support evidence but not full operator/invocation/projection context. This recurs in capability and inquiry surfaces.
- **Diagnostic visibility mismatch.** Some CLI-visible read-only surfaces are test-backed but not diagnostic-inventory-backed. The interrogation notices this, but does not by itself decide whether registration is required unless the surface is a diagnostic/audit/probe/view/recordable output under repository rules.
- **Retention and lifecycle policy.** Inquiry notes and similar artifacts raise persistence questions that the current interrogation can name but not resolve.

No new question is justified yet. These are remaining gaps, not methodology additions.

Smallest truthful answer:
The largest recurring escape is downstream consumer governance.

### Methodology legitimacy

Evaluate the current working hypothesis across Competency Interrogations 001-007:

| Hypothesis | Classification | Recurring interrogation evidence |
| --- | --- | --- |
| Contrast discovers boundaries. | Supported | Pressure Audit vs authority, Capability Verification vs permission, Capability Inventory vs verification, and Inquiry Orientation vs Operator Intake all gained precision by contrast. |
| Invariants discover identity. | Supported | Read-only behavior, no runtime, no event mutation, deterministic output, evidence-source separation, and authority boundaries repeatedly recovered competency identity. |
| Recurrence earns legitimacy. | Supported | Questions gained legitimacy when the same mistake recurred across multiple competencies: visibility is not authority, verification is not permission, orientation is not interpretation. |
| Neighbor analysis discovers hallways. | Supported | Neighbor analysis exposed hallways between candidate/inventory/verification, pressure/orientation, and operator intake/inquiry orientation without collapsing them. |
| Interrogation discovers constitutional limits. | Supported | Each interrogation ended with smaller permissible reliance than the public surface initially suggested. |
| Typed unknowns preserve honesty. | Supported | Remaining questions and Unknown/Stop sections repeatedly preserved unknowns instead of filling them with plans or recommendations. |

Smallest truthful answer:
The methodology is supported as a boundary-recovery discipline, not as a source of new authority.

### Has the interrogation discipline become more precise, or merely more elaborate?

More precise, with risk of elaboration.

Implementation-backed precision gained:

- neighbor analysis repeatedly prevents adjacent competency collapse;
- negative authority repeatedly exposes apparent power not granted by implementation;
- observed/derived/assumed separation repeatedly prevents evidence-class mixing;
- reliance sections repeatedly reduce truthful use to a smaller scope;
- typed unknowns repeatedly prevent inference through gaps.

Elaboration risk:

- Evolution, Locality, Artifact Handoff, and some trust/consumer questions overlap.
- Consumer questions often produce weak evidence because implementation lacks complete consumer governance.
- The method may become too long if useful-but-not-essential sections are preserved for elegance rather than recurring mistake prevention.

Smallest truthful answer:
The interrogation has become more precise where it prevents recurring overclaim; it becomes merely elaborate where questions repeat without exposing a distinct mistake.

## Methodology honesty candidates

Recurring observations preserved, not stabilized:

- Visibility is not authority.
- Verification is not permission.
- Inventory is not admission.
- Orientation is not interpretation.
- Lexical overlap is not intent.
- Candidate presence is not readiness.
- Related material is not importance.
- Surface-family labeling is not ownership.
- Read-only output is not mutation.
- CLI availability is not governance completeness.
- Negative authority is a recurring constitutional phenomenon.
- Consumer governance remains weaker than artifact construction in several surfaces.

Inquiry Orientation reinforces these candidates in a concrete form:

- operator prose is not repository truth;
- preserved note is not a command;
- deterministic match is not semantic understanding;
- uncertainty is part of the artifact, not an apology for it.

Smallest truthful answer:
The strongest honesty candidate here is that addressability does not equal understanding.

## Constitutional reflection

If this competency disappeared tomorrow,

what constitutional capability

would the organism lose?

Seed would lose a read-only way to preserve raw operator prose outside cluster truth and render bounded lexical orientation against projected material with explicit uncertainty and authority limits.

Nothing more.

Nothing less.

If this interrogation disappeared tomorrow,

what constitutional capability

would Seed lose?

Seed would lose an implementation-backed discipline for reducing apparent competency authority to lawful reliance, boundary, unknown, and stop conditions.

Nothing more.

Nothing less.

If this competency

were silently expanded,

what constitutional boundary

would most likely be violated first?

The first likely violation would be converting operator prose or lexical overlap into intent, recommendation, route selection, command, or repository truth.

Smallest truthful answer:
Seed would lose bounded prose orientation if the competency disappeared; Seed would lose boundary interrogation if the method disappeared.

## Lawful termination

This interrogation stops at the implemented boundary.

It does not redesign the methodology. It does not stabilize vocabulary. It does not create a registry. It does not recommend planners or coordinators. It does not promote operator prose into knowledge. It does not infer intent from related material. It does not turn surface-family labels into ownership. It does not turn uncertainty into a demand for new architecture. It does not remove questions solely because they look repetitive, and it does not preserve questions solely because they are elegant.

Smallest truthful answer:
The lawful stop is bounded read-only orientation and question-level audit.

## Remaining questions

| Type | Remaining question | Why it remains |
| --- | --- | --- |
| Consumer unknown | Which downstream consumers rely on inquiry orientation output? | Tests and CLI consumers are visible; complete consumer governance is absent. |
| Provenance unknown | What invocation and projection context should accompany every orientation? | The note preserves minimal provenance, but not complete invocation/projection provenance. |
| Retention unknown | How long should inquiry notes remain in the probe store? | Persistence exists, but retention policy is not established by this competency. |
| Boundary-enforcement unknown | How are downstream consumers prevented from treating orientation as intent? | The artifact states the boundary; enforcement outside the artifact is not complete. |
| Methodology unknown | Should Evolution remain a major section for every competency? | It is useful, but repeated overlap with Identity and Boundaries makes permanence unproven. |
| Methodology unknown | Should consumer governance become a sharper question? | Recurring weak evidence exists, but no new question is justified yet. |

Smallest truthful answer:
The remaining unknowns limit overuse; they do not weaken the implemented orientation boundary.

## Confidence

**High confidence** that Inquiry Orientation is implemented as a read-only preserved-prose orientation surface with deterministic lexical matching and explicit authority boundaries.

**High confidence** that it refuses fact creation, projection mutation, action creation, importance, ownership, intent, recommendation, authorization, command, runtime instruction, and next safe move authority.

**Medium confidence** that Operator Intake is the nearest constitutional neighbor, because broader intake is strongly present in architectural evidence but less centralized as a single implementation surface.

**Medium confidence** that the interrogation discipline has become more precise rather than merely elaborate, because negative authority, neighbor contrast, and typed unknowns repeatedly prevent overclaim; some useful sections still risk overlap.

**Medium-low confidence** in complete consumer governance and note lifecycle policy, because reviewed implementation evidence does not provide complete downstream registry or retention semantics.

Smallest truthful answer:
Seed can truthfully explain Inquiry Orientation and can now challenge its interrogation questions without pretending the method is final.
