# Seed Vocabulary and Episode-Index Shape Recovery 001

## 1. Executive finding

**Finding:** the repository contains enough evidence to design and begin both
vocabulary sections without inventing constitutional content, but not enough to
publish an exhaustive vocabulary or a complete episode index. This bounded pass
recovers **5** candidate Book-constitutional distinctions and **2** candidate
engineering practices from **3** correction episodes. It deliberately leaves the
early history and several current term relationships unresolved.

The faithful shape is relational rather than a flat glossary. A constitutional
entry needs an active clause *and* an earned correction episode. A practice entry
needs a repository cost and must expressly disclaim Book authority. Both point to
an episode record; the episode points to existing narrative rather than repeating
it. Book authority is therefore not repository testimony, and indexing an account
is not retelling it.

This is a recovery inventory, not `vocabulary.md`, an episode index, or a genesis
narrative. Counts are exact for the evidence universe declared below, not a claim
that every recurring noun in the repository has been exhaustively adjudicated.

## 2. Method and evidence classes

### Boundary

The checkout is shallow. `git rev-parse --is-shallow-repository` returns `true`;
the reachable first-parent history contains 100 commits, PR 2039 through PR 2138.
The object for commit `b3e4885d033cd12d47476dcd724039c764328c70`
(PR 2038) survives and has three reachable ancestors, but that detached four-commit
fragment is not repository genesis. There is no local `main` ref; the clean
current branch began at `2baf3ab` (`#2138`), the latest merged state supplied by
the checkout. This pass did not manufacture older chronology from filenames.

The bounded evidence universe is:

1. the active leaf chapters under `book_of_seed/01-*` through
   `book_of_seed/08-*`, with focused clause inspection rather than wholesale
   transcription;
2. the three episode accounts named in section 6 and their directly adjacent
   reports;
3. reachable PR 2039–2138 commit testimony, especially PR 2082 and PR 2136–2138;
4. the detached PR 2035–2038 fragment only as weak chronology testimony; and
5. current files and paths only as current implementation or documentary
   testimony, never as constitutional authority.

### Evidence posture

| Evidence class | Use here | Negative authority |
| --- | --- | --- |
| Active Book | Constitutional authority for a precise distinction | Does not prove when or why the repository learned it |
| Current implementation | Current behavior, names, producers, and consumers | Does not establish constitutional standing or historical motive |
| Current report | Repository testimony and possible existing narrative | Is not Book authority |
| PR description/review preserved in a report | Historical testimony | Is not independently available when the shallow graph omits it |
| Reachable commit message | Weak historical testimony and exact adoption marker | Does not prove motive |
| Operator recollection | Future attributed testimony | Not supplied in this pass |

### Qualification and counting rules

An entry was admitted only when a current meaning/practice and a concrete
correction cost were both recoverable. One distinction with several clause
citations counts once. One bounded arc producing several entries counts once. One
arc represented by several reports counts once. A report list is not automatically
a narrative. The **stable-but-uncontested** count is limited to the five explicitly
examined, addressable active clauses in section 4 for which this pass recovered no
correction episode; it is not the count of every paragraph in the Book. This makes
the number reproducible and avoids treating the absence of discovery in a bounded
pass as proof about the entire repository.

## 3. Candidate constitutional vocabulary

### Candidate inventory

| Term or distinction | Active Book authority | Plain-language meaning | Precise requirement | Earlier loose usage | Correction episode | Existing narrative | Remaining uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **external grammar != constitutional grammar** | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, **Bounded resolution**, **01.External.A — Source grammar translation boundary**, and **01.External.B — Addressability without assimilation** | Words and structures Seed encounters can be described without becoming Seed's own law. | External material remains attributed and bounded unless a constitutional translation preserves source, scope, uncertainty, and authority limits. | Planning/tool and “handoff” implementation vocabulary was used as if useful external compression named native constitutional objects or acts. | E1, external-grammar contamination and handoff decomposition | `book_of_seed/agentic_planning_tool_prototype_contamination_recovery_001.md`; `book_of_seed/handoff_compression_constitutional_correction_001.md` | The general warrant for recovering a distinction is explicitly unresolved in the chapter. |
| **representation formation != emission** | `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, **Bounded resolution** and **08.Communication.C — Egress representation preserves result standing without strengthening it** | Preparing something to show is different from actually presenting it toward someone. | Formation and emission need separate responsible occurrences; neither proves delivery, receipt, interpretation, or stronger standing. | “Handoff” compressed formation, emission, transport, receipt, and downstream use into one apparent event. | E1 | `book_of_seed/handoff_compression_constitutional_correction_001.md` | Whether a particular external consumer received or interpreted material remains Unknown without evidence. |
| **responsibility transition != authority transition** | `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, **08.Communication.A — Bounded responsibility transition** and **08.Communication.D — Authority does not move with material** | Taking responsibility for a bounded subject does not automatically grant authority over it. | Each transition has its own subject, source, receiver, scope, evidence, occurrence, and surviving limits; moving or naming material cannot confer authority. | “Handoff,” owner fields, routing targets, and adjacency compressed responsibility and authority movement. | E1 | `book_of_seed/handoff_compression_constitutional_correction_001.md` | Actual acceptance and any authority grant remain case-local and often Unknown. |
| **normalized claim representation != Fact standing** | `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`, **Bounded resolution** and **Important distinctions** (`Fact artifact != Fact standing`); `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.C — Constructed behavior does not confer standing** | Putting a claim into a standard Fact-shaped record does not make it an established fact. | Fact standing requires the applicable supported, scoped, conflict-aware establishment boundary; construction and normalization establish shape only. | Older claim-centric terminology and implementation paths compressed normalization, evidence linking, construction, replay, and establishment into `Fact`. | E2, claim normalization and Fact-standing recovery | `book_of_seed/claim_normalization_and_fact_standing_recovery_001.md` | Exact source-authority thresholds, conflict mechanics, and several current Fact producers remain Unknown. |
| **operator question-shaped material != a Seed-owned bounded internal question** | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **04.Question.B — Inquiry origination requires bounded translation** and **04.Question.E — Normal internal questioning is Seed-owned** | An operator can supply material that prompts inquiry, but that input is not automatically Seed's internal question. | A bounded translation must preserve source material and produce internal question standing; compatibility routing or object construction cannot substitute for that occurrence. | A bounded-ask adapter advertised six raw operator fields as a constitutional-pipeline entrance, while the consumer later refused raw origination; a JSON loader still constructs a question-shaped object directly. | E3, constitutional-pipeline ingress and bounded-question topology | `bounded_ask_constitutional_pipeline_ingress_cleanup_001.md`; no single full-arc narrative | The responsible question-formation implementation and lawful examination entrance remain Unknown. |

### Authority-discipline ledger

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
| --- | --- | --- | --- |
| External vocabulary stays attributed until bounded constitutional translation. | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, **01.External.A** and **01.External.B** | Translation/addressability boundary | That recurrence, usefulness, or implementation adoption makes a term constitutional |
| Formation, emission, and later consumer occurrences are distinct. | `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`, **08.Communication.C** | Bounded egress representation and emission | Delivery, receipt, uptake, or external effect |
| Responsibility and authority do not travel together by implication. | Same path, **08.Communication.A** and **08.Communication.D** | Bounded responsibility and authority transitions | A universal transition artifact or workflow |
| Fact-shaped construction is not Fact standing. | `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`, **Bounded resolution**; `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.C** | Establishment standing versus representation | Exact establishment algorithm or universal corroboration threshold |
| Internal question origination remains Seed-owned. | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`, **04.Question.B** and **04.Question.E** | Operator material to internal inquiry boundary | That the current runtime implements the missing translation |

## 4. Stable-but-uncontested exclusions

These **5** active clauses were directly examined because they neighbor the
question/inquiry candidate. No concrete correction episode was recovered for them
inside this pass, so they are excluded rather than promoted from frequency or
importance:

| Active clause | Current subject | Reason excluded |
| --- | --- | --- |
| `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md`, **04.Frontier.A — Frontier identity is conjunctive, not wording-derived** | Frontier identity | Stable clause; no recovered earning episode in the bounded evidence set |
| Same path, **04.Frontier.B — Positive frontier support requires claim-relative warrant** | Positive frontier support | Same |
| `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`, **04.Examination.A — Bounded relevance before movement** | Relevance before examination movement | Same |
| Same path, **04.Examination.B — Positive lawful inactivity** | Lawful non-movement | Same |
| Same path, **04.Examination.C — Cross-examination without source-local erasure** | Preservation across comparison | Same |

“Stable” here means the active clause exists and was not contradicted in this
focused review. It does not mean timeless, uncontested in all unavailable history,
or automatically eligible for a later vocabulary.

## 5. Candidate engineering-practice vocabulary

No active Book clause inspected establishes either practice as constitutional
grammar. They are repository-working conventions earned by repository costs.

| Convention name | Plain-language meaning | Defect prevented | Originating episode | Adoption point | Existing narrative | Current scope | Constitutional status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **repository-wide producer/consumer search before deletion** | Before deleting a named component, find every place that creates, imports, reconstructs, and uses it instead of assuming it belongs only to the nearby feature. | The proposed constitutional-pipeline-local deletion premise was false: `BoundedConstitutionalQuestion` also served three examination modules, and neighbor imports could be mistaken for independent demand. | E3 | PR 2138, commit `2baf3ab`, records the repository-wide topology recovery; PR 2137, `6640946`, recovered the deletion boundary. | `bounded_constitutional_question_complete_topology_recovery_001.md` | Repository deletion/recovery work where shared artifacts or consumer roads are in question; not a universal constitutional act | **Engineering practice, not Book grammar.** |
| **current active surface outranks stale compatibility/history testimony** | Decide what is currently offered from active code and operator material; keep old reports as history instead of letting them advertise a deleted road. | The bounded-ask inventory still advertised a six-field constitutional-pipeline producer after PR 1734's consumer refused raw fields. | E3 | PR 2136, commit `a895027`; the cleanup report records the operator-guide correction and preservation of old reports as history. | `bounded_ask_constitutional_pipeline_ingress_cleanup_001.md` | Current-surface audits and cleanups; does not authorize rewriting historical reports or decide Book law | **Engineering practice, not Book grammar.** |

Potential habits such as “report-only first,” “recover before implementation,”
“hold out from deletion,” and “do not freeze unexplained behavior in tests” were
not admitted. This pass found examples of those postures, but did not recover a
bounded repository cost and adoption point sufficient to earn separate entries.

## 6. Episode inventory

An episode is counted once even when it yields several terms, practices, clauses,
or reports.

| Episode | Approximate PR range | Governing defect or confusion | Constitutional terms produced | Practices produced | Existing full account | Evidence class | Remaining Unknowns |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **E1 — External compression and “handoff” decomposition** | After PR 1922; exact adopting PR is **Unknown** in this shallow checkout | Useful planning/tool/communication vocabulary was allowed to appear as native grammar, and “handoff” collapsed many independently evidenced transitions. | external grammar != constitutional grammar; representation formation != emission; responsibility transition != authority transition | None admitted | `book_of_seed/handoff_compression_constitutional_correction_001.md` (with contamination context in `book_of_seed/agentic_planning_tool_prototype_contamination_recovery_001.md`) | Current report plus Book-development testimony | Exact adopting PR and particular real-world receipt/transition occurrences |
| **E2 — Claim normalization and Fact-standing recovery** | Exact PR **Unknown** in this shallow checkout | `Fact` carried both a normalized representation shape and stronger established standing; producer paths compressed normalization, construction, evidence linking, replay, and establishment. | normalized claim representation != Fact standing | None admitted | `book_of_seed/claim_normalization_and_fact_standing_recovery_001.md` | Current report and Book reconciliation | Exact source thresholds, conflict-aware mechanics, and lawful status of several Fact producers |
| **E3 — Constitutional-pipeline ingress cleanup and shared-question topology** | PR 2136–2138 (`a895027`..`2baf3ab`) | A stale producer advertised input categorically refused by its consumer; the next deletion premise incorrectly treated a shared question artifact as pipeline-local. | operator question-shaped material != a Seed-owned bounded internal question | repository-wide producer/consumer search before deletion; current active surface outranks stale compatibility/history testimony | `not narrated` as one full arc | Reachable PR history and three current reports | Responsible question formation, lawful examination ingress, and why the original PR 1611 design was chosen |

### Existing-account restraint

E1's report explains the compression, correction, resulting clauses, and limits;
this inventory does not repeat its coordinate-by-coordinate narrative. E2's report
already supplies the lineage, producer/consumer comparison, correction boundary,
and remaining Unknowns; this inventory only identifies the earned distinction.

For E3, dispersed evidence establishes a stale raw-input adapter, its removal in PR
2136, a deletion-boundary recovery in PR 2137, and the shared topology recovery in
PR 2138. It does **not** establish the motive for the original design or supply one
account connecting original defect, investigation, correction, and both resulting
practices. That is the maximum responsible compressed account.

## 7. Narrative coverage

| Episode | Status | Basis |
| --- | --- | --- |
| E1 | **fully narrated** | One report explains the compressed defect, examination, clause correction, resulting distinctions, and Unknowns. |
| E2 | **fully narrated** | One report explains vocabulary lineage, implementation compression, recovery, and resulting standing distinction. |
| E3 | **partially narrated** | Cleanup and topology reports preserve pieces, but no single report explains the whole PR 1611/1734/2136–2138 arc and why both practices were earned. |

There are **0 not-narrated qualifying episodes**. E3 is not upgraded to full merely
because several implementation reports exist. E1 requires operator testimony for
exact pre-shallow adoption chronology; E3 requires it for original design motive.
E2's remaining technical/constitutional Unknowns do not by themselves require
operator memory. Thus **2 episodes require operator testimony**.

## 8. Genesis-gap recovery

### Finding and future scope

The genesis period is **not currently narrated in an artifact recovered by this
pass**. The local graph cannot inspect the first few dozen PRs: its reachable
history begins at PR 2039, and its detached fragment begins at PR 2035. A future
genesis account should be bounded to the repository's creation through the first
stable Book/report discipline, identify then-current names and assumptions, and
stop before later correction arcs already fully narrated. This report does not
write that account.

### Evidence inventory

| Classification | Recoverable material | Responsible conclusion |
| --- | --- | --- |
| **repository-evidenced fact** | Current filenames, `docs/` reconciliations cited by existing reports, archived reports, active Book text, current source, and surviving PR 2035–2138 objects | These can show that names, shapes, and clauses existed in preserved snapshots and that later reports describe changes. |
| **repository-evidenced fact** | `book_of_seed/original_numbered_seed_corpus_archival_001.md` | An archival account exists for a numbered Seed corpus; its existence does not make it a complete repository-genesis narrative. |
| **historical inference** | Earlier implementation was more planning/tool-, truth-, and object-shaped than the current Book | Supported by later correction reports, but the time, sequence, and motive cannot be assigned confidently without original history. |
| **historical inference** | Report-writing and explicit evidence discipline matured after initial implementation | Filename and report-density patterns suggest this, but chronology alone cannot establish the reason. |
| **operator testimony required** | Original meanings of early names; which distinctions were consciously understood; why designs were chosen; which failures were decisive; when “Seed” acquired its present constitutional intent | These are motives and recollections, not recoverable facts from surviving shapes. |
| **Unknown** | Actual first PR range, first stable vocabulary, first contested episode, and whether a complete early account exists outside this checkout | The shallow graph cannot answer. |

### Questions for the operator

1. What repository and PR range counts as genesis, and is full remote history
   available for inspection?
2. Which early terms were intentional constitutional claims rather than temporary
   implementation names?
3. Which concrete failures caused Claim/Fact, planning/tool, question, BOGE, focus,
   and horizon language to change?
4. Which reasons were discussed outside committed PR descriptions and reports?
5. Does an external account already narrate the defect, investigation, correction,
   and resulting distinctions of that period?

## 9. Unresolved distinctions

This pass encountered **9 unresolved contested lexical families**: **BOGE, focus,
advancement horizon, inquiry opening, question formation, applicability,
selection, responsibility, and standing**. “Contested” means repository evidence
warns against collapse or overclaim; it does not mean every local use lacks a
definition.

| Term/family | Current evidence | Classification | What remains Unknown |
| --- | --- | --- | --- |
| BOGE | `book_of_seed/03-goals-and-advancement/construction-and-establishment.md` and current BOGE reports support bounded goal-establishment standing; `bounded_operator_goal_to_advancement_horizon_characterization.md` shows the horizon consumes only limited goal identity/provenance/adverse testimony and no goal semantics sufficient to derive its boundary. | **contested but unresolved** relative to focus/horizon | Whether BOGE, focus, and horizon form a required sequence, and who lawfully produces the horizon boundary |
| focus | `book_of_seed/advancement_need_focus_formation_recovery_001.md` recovers a possible independent producer/consumer boundary but records that production occurrence is not fully recovered. | **contested but unresolved** | Whether focus is required, what exact standing its producer establishes, and its relation to inquiry opening |
| advancement horizon | `bounded_operator_goal_to_advancement_horizon_characterization.md` finds a caller-supplied preserved boundary, not an independently selected or truth-established one. | **contested but unresolved** | Producer authority, applicability, and whether it precedes or follows focus |
| inquiry opening | `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md` separates question formation, inquiry establishment, examination, and answer standing. | **contested but unresolved** | Exact current responsible opening occurrence and its relation to goal/focus/horizon |
| question formation | **04.Question.B/E** reserve internal formation to Seed and reject raw operator origination; E3 finds the runtime entrance incomplete/contaminated. | **contested but unresolved** | Exact producer, admissible input standing, and implemented entrance |
| applicability | Active Book clauses distinguish applicability from admission and consumption; recent operator-ingress reports recover local BOGE applicability ownership. | **contested but unresolved** across families | Whether one common applicability grammar exists and how inquiry/focus uses relate to BOGE-local applicability |
| selection | `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md` gives local constitutional constraints; `book_of_seed/selection_act_classification_recovery_001.md` shows many implementation “selection” neighborhoods are adjacent acts or remain Unknown. | **contested but unresolved** as a repository-wide label | Which families are genuine selection acts and whether focus formation is one |
| responsibility | Active communication and authority clauses define bounded local requirements, while “handoff” previously collapsed transition with authority. | **contested but unresolved** in several roads | Actual holder/acceptance at unevidenced crossings; no universal responsibility transfer is inferred |
| standing | Active Book provides local kind-specific establishment rules and denies that shapes confer standing. | **contested but unresolved** as a universal mechanism | No single universal standing producer or complete taxonomy is established |

The repository therefore establishes non-equivalence and several local boundaries,
not aliases, a settled pipeline, or fully independent systems. The BOGE/focus/
horizon relationship remains **Unknown** beyond the bounded facts above.

## 10. Proposed vocabulary schema

The future `vocabulary.md` should use two separate top-level sections and repeat no
episode narrative.

### A. Book-constitutional vocabulary entry

Required fields: **Term; Plain-language meaning; Precise distinction; Active Book
authority (path, section, clause); Scope supported; What is not inferred;
Correction episode ID; Existing narrative; Related terms; Remaining Unknowns.**

Exactly one real worked example:

> **Term:** representation formation != emission
> **Plain-language meaning:** Preparing something to show is different from
> actually presenting it toward a consumer.
> **Precise distinction:** each occurrence needs its own evidence; neither proves
> delivery or receipt.
> **Active Book authority:**
> `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`,
> **08.Communication.C**.
> **Scope supported:** bounded egress representation and emission.
> **What is not inferred:** delivery, receipt, interpretation, uptake, reliance,
> transition, or external effect.
> **Correction episode:** E1.
> **Existing narrative:**
> `book_of_seed/handoff_compression_constitutional_correction_001.md`.
> **Related terms:** responsibility transition; authority transition.
> **Remaining Unknowns:** actual consumer occurrences in any particular case.

### B. Engineering-practice vocabulary entry

Required fields: **Convention; Plain-language meaning; Failure it prevents;
Originating episode ID; Adoption evidence; Existing narrative; Scope; Explicit
constitutional status; Related practices; Remaining Unknowns.**

Exactly one real worked example:

> **Convention:** repository-wide producer/consumer search before deletion
> **Plain-language meaning:** Find all creators and users before assuming a shared
> component belongs to one nearby feature.
> **Failure it prevents:** deleting `BoundedConstitutionalQuestion` as
> pipeline-local despite three examination consumers.
> **Originating episode:** E3.
> **Adoption evidence:** PR 2137 (`6640946`) and PR 2138 (`2baf3ab`).
> **Existing narrative:**
> `bounded_constitutional_question_complete_topology_recovery_001.md`.
> **Scope:** shared-artifact deletion/recovery work.
> **Constitutional status:** engineering practice, not Book grammar.
> **Related practices:** current active surface outranks stale compatibility/history
> testimony.
> **Remaining Unknowns:** whether an older explicit adoption account exists.

## 11. Proposed episode-index schema

Use chronological episode records with stable IDs. Each record should contain:
**Episode; chronological key; PR/commit range and confidence; original defect;
investigation boundary; constitutional vocabulary produced; engineering practices
produced; active Book clauses implicated; existing reports (one marked primary if
applicable); narrative coverage status; evidence classes; operator testimony
required; remaining Unknowns.** A generated-by-hand reverse table may list term →
episode without repeating definitions.

Exactly one real worked episode:

> **Episode:** E3 — Constitutional-pipeline ingress cleanup and shared-question
> topology
> **Chronological key:** 2136-2138
> **PR/commit range:** PR 2136 `a895027` through PR 2138 `2baf3ab` (exact,
> reachable)
> **Original defect:** a stale raw-input producer was categorically refused by its
> consumer; a subsequent deletion premise treated a shared question artifact as
> pipeline-local.
> **Investigation boundary:** bounded-ask ingress, static pipeline, and complete
> `BoundedConstitutionalQuestion` producer/consumer topology.
> **Constitutional vocabulary produced:** operator question-shaped material != a
> Seed-owned bounded internal question.
> **Engineering practices produced:** repository-wide producer/consumer search
> before deletion; current active surface outranks stale compatibility/history
> testimony.
> **Book clauses implicated:**
> `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`,
> **04.Question.B/E**.
> **Existing reports:** `bounded_ask_constitutional_pipeline_ingress_cleanup_001.md`,
> `constitutional_pipeline_question_origination_deletion_slice_001.md`, and
> `bounded_constitutional_question_complete_topology_recovery_001.md`.
> **Coverage status:** partially narrated.
> **Evidence classes:** reachable PR history, current reports, active Book.
> **Operator testimony required:** why the original PR 1611 entrance was chosen.
> **Remaining Unknowns:** lawful question producer and examination ingress.

## 12. Cross-index shape

The minimum maintainable relations are:

```text
vocabulary entry --authority--> exact active Book clause     (constitutional only)
vocabulary entry --earned-by--> episode ID
vocabulary entry --accounted-by--> primary report or not narrated
episode --produced--> constitutional entry IDs
episode --produced--> practice entry IDs
episode --reported-in--> one or more report paths
episode --occurred-in--> PR/commit range + confidence
episode --leaves--> unresolved question IDs
episode --needs--> attributed operator testimony question IDs
```

The vocabulary owns short definitions and authority pins. The episode index owns
chronology, correction cost, coverage, and testimony requirements. Reports own
narrative. The Book owns constitutional clauses. Human-maintained IDs and relative
links are sufficient; no documentation framework, duplicated prose store, or
uniform alphabetical authority is warranted.

## 13. Required counts

| Measure | Exact count |
| --- | ---: |
| Candidate constitutional terms/distinctions | **5** |
| Stable-but-uncontested active clauses excluded (bounded inspected set) | **5** |
| Candidate engineering-practice terms | **2** |
| Distinct qualifying episodes | **3** |
| Fully narrated episodes | **2** |
| Partially narrated episodes | **1** |
| Not-narrated episodes | **0** |
| Episodes requiring operator testimony | **2** |
| Unresolved contested term families | **9** |

The unit rules are those in section 2: multiple citations do not multiply a term;
multiple terms do not multiply an episode; multiple reports do not multiply an
episode. E1 and E3 need testimony for missing historical reason/chronology. E2 has
substantive Unknowns but no identified memory-only question necessary to index its
recovered account.

## 14. Direct answers

1. **Does the repository contain enough evidence to build the two vocabulary
   sections without inventing constitutional content?** Yes, for a bounded first
   edition using the recovered entries and explicit Unknowns; no, for an
   exhaustive final edition.
2. **How many candidate constitutional terms were recovered?** **5.**
3. **How many stable-but-uncontested Book clauses were excluded?** **5** in the
   explicitly bounded inspected set.
4. **How many candidate engineering-practice terms were recovered?** **2.**
5. **How many distinct episodes were recovered?** **3.**
6. **How many episodes are fully narrated?** **2.**
7. **How many are partially narrated?** **1.**
8. **How many are not narrated?** **0.**
9. **Which episodes require direct operator testimony?** E1 for exact adoption
   chronology hidden by the shallow graph, and E3 for the original ingress design
   reason.
10. **Is the genesis period currently narrated?** No complete genesis narrative
    was recovered.
11. **What can be recovered about genesis from repository evidence alone?**
    Preserved names, files, later reconciliations, archived corpus testimony,
    surviving shapes, and later reports' attributed descriptions of earlier
    assumptions.
12. **What genesis material cannot be responsibly recovered without the
    operator?** Motive, intended meanings, off-repository discussions, which
    failure was decisive, and whether contemporaries already understood a later
    distinction.
13. **Does the proposed schema keep constitutional and practice vocabulary
    structurally separate?** Yes: separate top-level sections, different required
    fields, and no Book-authority field for a practice.
14. **Which current terms remain contested or unresolved?** BOGE, focus,
    advancement horizon, inquiry opening, question formation, applicability,
    selection, responsibility, and standing.
15. **Did the recovery encounter unresolved BOGE/focus/horizon distinctions?**
    Yes.
16. **What does the repository establish about those distinctions?** BOGE can
    represent bounded goal-establishment standing; focus has a partially recovered
    independent producer/consumer topology; the current horizon producer preserves
    a caller-supplied boundary and limited goal lineage rather than deriving that
    boundary from goal semantics. They must not be collapsed.
17. **What remains Unknown?** Their required ordering and cardinality, whether
    focus is necessary, who warrants the horizon boundary, how inquiry opens from
    them, and whether the current implementation realizes a lawful complete road.
18. **What is the smallest next lawful action?** **recover operator testimony
    first.** The schemas and a bounded set of real entries are already recoverable;
    writing either final document now would encode avoidable holes in E1 chronology,
    E3 motive, and genesis scope. One bounded, attributed testimony session can
    answer those history-only questions without changing Book grammar or choosing
    among unresolved BOGE/focus/horizon terms.

## 15. Remaining Unknowns

- Whether full remote history changes any episode boundary or reveals earlier
  adoption accounts.
- Whether the first few dozen PRs contain a complete genesis narrative not present
  in this checkout.
- Whether additional active clauses have recoverable correction episodes and
  therefore qualify in a later bounded inventory.
- Whether apparent practices omitted here have a concrete earning defect and
  adoption point.
- Exact constitutional recovery warrant for external distinctions, which the
  active external-grammar chapter itself marks unresolved.
- Fact-establishment thresholds and conflict mechanics.
- The lawful question-forming producer and examination ingress.
- The BOGE/focus/horizon/inquiry relationship described in section 9.
- Actual receipt, interpretation, uptake, reliance, responsibility acceptance,
  authority grant, and external effect for any particular communication road.

Unknowns are boundaries, not invitations to normalize terms or fill history with
chronological inference.

## 16. Single next lawful action

**Recover operator testimony first.**

The session should be bounded to the questions in section 8 plus E1's adoption
chronology and E3's original ingress-design reason. Testimony must be attributed,
kept separate from repository-evidenced fact, and allowed to answer “Unknown.” It
must not amend the Book, resolve BOGE/focus/horizon by preference, or become the
genesis narrative automatically. After that evidence is preserved, a later change
can decide whether the two final documents are ready.
