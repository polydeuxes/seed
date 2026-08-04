# Operational Vocabulary and Recording Decompilation 001

## 1. Scope and authority

This is one bounded, report-only recovery from the current merged repository (`HEAD` at commit `1e10d8e`, including PR 2238). It changes no active Book chapter, runtime file, test, or concordance entry. Authority order: active numbered Book chapters control; the Book VII excision record (`book_vii_operational_topic_collection_excision_001.md`) is itself an active correction record and is treated as authoritative for what it already settled; implementation and tests are testimony only; prior reports (including `consideration_vocabulary_residue_audit_001.md` and its correction) are attributed testimony.

Governing question, as set by curator: **which exact responsibilities preserve an act, testimony, result, or standing as retrievable material, and which current operational terms disappear when those responsibilities are expressed through Act, production, preservation, standing, and consumer Uptake?**

All four named files were read in full: `02-acts-and-constraints/acts-and-act-artifacts.md`, `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`, `05-evidence-and-knowledge/testimony-and-established-fact.md`, `06-state-and-projection/events-facts-and-state.md`. A direct case-insensitive whole-word search for `operations?` and `operational` was run across all four. `events-facts-and-state.md` contains **zero** occurrences of either — it is relevant to the Recording question but carries none of the disputed vocabulary itself.

## 2. Method: grammar-mapping before decomposition-testing

Per the operator's stated technique, this recovery leads with a different first move than the five-coordinate decomposition test used in prior audits (`examine_uptake_and_production_residue_audit_001.md`, `consideration_vocabulary_residue_audit_001.md`): for every occurrence of `operation`/`operational`, the first question is **which already-established word is this reaching for**, not whether the word independently qualifies. The five-coordinate test (owner, subject, act, result, consumer) is applied only where grammar-mapping does not resolve the occurrence.

## 3. Governing prior finding: the Book VII excision already closed this territory once

`book_vii_operational_topic_collection_excision_001.md` is not background reading here — it is controlling. Its central rule (`:9`): "External operational terms... are ordinarily subjects of testimony, propositions under examination, externally attributed occurrences, bounded findings, or Unknown. They are not automatically Seed-native constitutional kinds, stages, or districts." Its disposition for the specific word `execution` (`:31-33`, and Final Direct Answer 4): "The former execution chapter did not leave a distinct constitutional kind named execution after separating Seed-owned act occurrence, request-shaped representation, emission, invocation occurrence, external mechanism performance, result testimony, and recording... No distinct execution family survived." And directly: "Seed-owned performance is a general act occurrence" (`:37`).

This matters because PR 2238 (reviewed and provisionally endorsed by this session before this recovery) replaced `execution`/`execution record`/`execution status` with `operation occurrence`/`operation-occurrence record`/`operation status`. That endorsement was wrong on exactly this point: it verified the *sentence* still made sense and nothing was lost in translation, but never asked whether the *replacement word* was itself grounded. It wasn't checked against the Book VII excision's own governing rule, which already states the general principle broadly enough to cover any external-operational-sounding term, not only the specific word `execution`.

## 4. Grammar-mapping table: every occurrence

| Occurrence | Location | What word is it reaching for | Basis |
|---|---|---|---|
| "for operational acts, by the execution or recording boundary" | `acts-and-act-artifacts.md:10` | **act** (no separate species exists); the real distinction being gestured at is "acts whose occurrence is evidenced via a recording boundary specifically" | Book VII excision `:37`: "Seed-owned performance is a general act occurrence." No active clause anywhere defines a distinct `operational act` kind. |
| "An operational measurement is bounded testimony about the observed behavior of a particular operation instance..." | `testimony-and-established-fact.md:32-33` (05.Testimony.B) | **act occurrence** — every listed example ("a projection, cache lookup, query, rendering, observation collection, read-model construction, fact-index construction, diagnostic comparison, external realization, or other bounded operation") is itself an act; "operation instance" = "one particular act occurrence" | The chapter's own list is exhaustively acts; "or other bounded operation" is the umbrella catch-all with no independent content beyond the list |
| "Operation-instance measurement... scoped operation instance" | `testimony-and-established-fact.md:35-36` (05.Testimony.C) | **act occurrence**, same mapping | Parallel construction to 05.Testimony.B |
| "An operational baseline is retained, scoped, evidence-supported understanding of ordinary operational behavior" | `testimony-and-established-fact.md:38-39` (05.Testimony.D) | **act-occurrence behavior** — the defining sentence is circular (defines "operational baseline" using "operational behavior") in exactly the shape found for `consideration selection` | Same circularity pattern as the corrected consideration audit; grammar-mapping resolves it by substituting the already-established `act occurrence` for both sides |
| "the operation and conditions covered" (comparison/tolerance boundary) | `testimony-and-established-fact.md:39` | **which act** is covered — an identifying dimension, not a distinct kind | Consistent with 05.Testimony.B's own list of measurement dimensions including bare "operation" as an identity dimension |
| "it is not automatically an operation failure" | `testimony-and-established-fact.md:39` | **act failure** — already-established vocabulary one chapter over | `acts-and-act-artifacts.md`'s own Important Distinction: "failed act != no occurrence automatically" |
| "Operational measurement production, operational understanding establishment, diagnostic rendering, and recording/preservation are separate responsibilities" | `recording-and-knowledge-extraction.md:10` | **umbrella compression**, not a single reaching-for-one-word case: this sentence bundles three already-separately-named responsibilities (05.Testimony.B's measurement production, 05.Testimony.D's baseline/deviation/transition establishment, and diagnostic rendering) under two adjective-modified labels | Matches [[feedback_umbrella_verb_detection]] exactly: the pieces already have homes; the umbrella adds nothing except the appearance of one more kind |
| "Seed must preserve... its materially sufficient understanding of operational reality" | `recording-and-knowledge-extraction.md:23` (05.Recording.C) | **act-occurrence behavior**, same mapping as the baseline definition | Consistent with 05.Testimony.D |
| "Recording operational testimony and standing" (boundary title) | `recording-and-knowledge-extraction.md:25` (05.Recording.D title) | **umbrella compression** over the same three already-named things: measurement testimony (05.Testimony.B), runtime/resource observation testimony (05.Testimony.C), and baseline/deviation/transition standing (05.Testimony.D) | The boundary's own body text confirms this — it separately lists "already produced measurement testimony," "already produced runtime/resource observation testimony," and "already established baseline standing, deviation standing, or transition standing" as the three things being preserved |
| "operational measurement", "operational baseline" throughout the Important Distinctions lists (both files) | multiple | **act-occurrence measurement**, **act-occurrence baseline** | Same substitution applied consistently; no distinctions are lost by the substitution since each `!=` pairing already names the *other* side of the distinction independently |
| "ExecutionStatus cadence != operation timing testimony"; "execution status != operational measurement" | `recording-and-knowledge-extraction.md:57-58` | `ExecutionStatus` is a real, cited implementation anchor (representative-repository-anchor style), correctly left as a literal class-name citation, not constitutional prose; "operation timing testimony" and "operational measurement" both reduce to **act-occurrence measurement** by the same mapping | Consistent with the already-established distinction that implementation names are testimony, not authority (`constitutional-kinds-and-artifact-standing.md:19`) |

No occurrence of `operation`/`operational` in either file survives as an independent constitutional kind once grammar-mapped. Every occurrence either (a) reaches directly for the already-established `act` or `act occurrence`, or (b) is an umbrella compression over responsibilities that are already separately named and defined within the same two chapters.

## 5. Consequence for PR 2238

PR 2238's replacements (`execution` → `operation occurrence`; `execution record` → `operation-occurrence record`; `execution status` → `operation status`) substituted one ungrounded word for another. Grammar-mapping resolves all three cleanly onto already-established vocabulary:

```text
operation occurrence          -> act occurrence
operation-occurrence record   -> act-occurrence record (or: recorded act occurrence, per 05.Recording.A's "record exists")
operation status               -> act-occurrence testimony / measurement (context-dependent, per 05.Testimony.B/C)
```

This is not a new finding requiring its own audit — it falls directly out of the same mapping applied to every other occurrence in this report, and PR 2238's own test-suite breakage (found and reported earlier in this session, not yet corrected) means the string these tests assert on needs to change again regardless. Both defects should be fixed in the same pass: correct the vocabulary and bring the two test files back into sync.

## 6. Recording decomposition

### 6.1 What is genuinely established

`recording-and-knowledge-extraction.md`'s core question — "Which bounded responsibility may take up recorded material, and what standing, if any, may it establish?" — is answered, in bounded form, by 05.Recording.A: "A recording boundary may create retrievable assertion-bearing material within its declared preservation horizon. The produced standing is that a record exists and preserves an attributed assertion." This is a real act (create retrievable material), a real bounded result (a record exists; it preserves an attributed assertion — two distinct claims, not one), and a real scope (the declared preservation horizon). `events-facts-and-state.md:10` independently corroborates this with a sharper, artifact-tied version: "A responsible recording occurrence may preserve, as an Event, attributed testimony that an occurrence or other claim was asserted; Event preservation does not establish the asserted occurrence as true." That sentence supplies an act (preserve as an Event), a material (attributed testimony that a claim was asserted), and an explicit denial (preservation does not establish truth) — genuinely more complete than anything in Book V's own chapter for this exact question.

Recording preservation grammar is real. It is not a bare recurring word the way `movement consideration` was.

### 6.2 What is not established: one exact Recording responsibility

Every reference to the acting party is generic and conditional: "a recording boundary," "the recorder," "a responsible recording occurrence." None of these is ever instantiated with a concrete owner, Authority, Warrant, or occurrence-evidence requirement the way, for example, `authority-scope.md:44`'s Authorization boundary correction names eleven required coordinates for an actual instance. Under the Responsibility root (`README.md`), a conditional occurrence coordinate being *describable* is not the same as an *exact* road being established for any particular recording act. No amendment is warranted to manufacture one; the finding is simply that Recording, read as a responsibility rather than as a description of what recording preservation *can* do, remains generic.

### 6.3 Recording is not silently compressed — it is correctly separated in name but incompletely owned in practice

The chapter's own bounded resolution already states the needed separation directly: "Operational measurement production, operational understanding establishment, diagnostic rendering, and recording/preservation are separate responsibilities" (after grammar-mapping: measurement production, baseline/deviation/transition establishment, diagnostic rendering, and recording/preservation are separate). 05.Recording.C independently states "Preservation decision != standing-establishment decision." Extraction is explicitly named as "a separate constitutional responsibility with its own evidence, reconciliation, and standing limits."

So the chapter does not speak as though Recording were one settled thing swallowing production, establishment, comparison, and extraction — it explicitly denies that, repeatedly, in its own prose. What it does *not* do is complete the coordinates for the adjacent decisions it correctly names as separate:

- **the preservation decision** (05.Recording.C: "Seed must preserve sufficient evidence or compressed standing... when discarding would erase material evidence") — named, never assigned an owner or Authority;
- **diagnostic-scoped admission** (05.Recording.B) — described as a bounded effect ("bounded availability to the diagnostic consumer"), never assigned an owner;
- **extraction** — named as separate and stopped there; this chapter supplies no further decomposition of it.

The defect is not compression-into-one-responsibility. It is: correct naming of several separate responsibilities, followed by completing the coordinates for only one of them (the bare create/preserve act itself), leaving the rest as unowned, free-floating adjacent concerns.

## 7. Answer to the governing question

**Which exact responsibilities preserve an act, testimony, result, or standing as retrievable material?**

Exactly one is fully coordinate-complete as a bounded act: the recording/preservation act itself (05.Recording.A; corroborated by `events-facts-and-state.md:10`'s Event-preservation sentence) — create a retrievable representation of already-produced, attributed material within a declared preservation horizon. Three further responsibilities are named and given real content but sit in a different chapter and were never described as "recording" in the first place: measurement production (05.Testimony.B, once grammar-mapped: act-occurrence measurement), runtime/resource observation production (05.Testimony.C), and baseline/deviation/transition establishment (05.Testimony.D). Extraction is named but not decomposed here. The preservation decision and diagnostic-scoped admission are named but not assigned an owner anywhere in the active Book.

**Which current operational terms disappear when those responsibilities are expressed through Act, production, preservation, standing, and consumer Uptake?**

All of them, per §4's table. `operational measurement` → act-occurrence measurement (production, per 05.Testimony.B, already correctly named "measurement-production responsibility"). `operational baseline` → act-occurrence baseline (establishment, per 05.Testimony.D, already correctly named "baseline establishment"). `operational act` → act (no residue; Book VII excision already closed this). `operational testimony and standing` / `operational understanding establishment` → umbrella labels that disappear entirely once the three things they bundle (measurement testimony, runtime/resource observation testimony, baseline/deviation/transition standing) are named directly, exactly as they already are named directly elsewhere in the same two chapters. No new noun is required anywhere in this decomposition; every occurrence maps onto vocabulary the active Book already has.

## 8. Failure audit

1. **New word treated as needing independent proof rather than mapped to existing grammar first:** the error this report exists to correct, in my own prior review of PR 2238 — noted and not repeated here.
2. **Umbrella label mistaken for a fourth responsibility:** rejected for `operational testimony and standing` and `operational understanding establishment`; both decompose losslessly into the three already-separately-named responsibilities.
3. **Compression mistaken for silence:** rejected; the Recording chapter already explicitly separates production, establishment, diagnostic rendering, recording, and extraction in its own prose. The defect is incomplete ownership of the correctly-separated pieces, not an unacknowledged bundling.
4. **Circular definition accepted at face value:** rejected for `operational baseline`, whose own defining sentence uses "operational behavior" to define "operational," exactly the shape already found and corrected for `consideration selection`.
5. **Implementation class name treated as prose vocabulary:** rejected; `ExecutionStatus` remains a legitimate literal citation and is not touched by this recovery.
6. **PR 2238's replacement vocabulary treated as already resolved:** rejected; it is not, and is folded into the disposition below rather than left as a dangling loose end from an earlier review.

## 9. Required conclusion

```text
operational act:
unsupported specialization; maps to act; no residue after Book VII excision

operation / operational (bare, modifying measurement/baseline/behavior/failure):
unsupported as an independent kind; maps directly to act / act occurrence in every occurrence checked

operational testimony and standing / operational understanding establishment:
umbrella compression over measurement production (05.Testimony.B), runtime/resource
observation production (05.Testimony.C), and baseline/deviation/transition
establishment (05.Testimony.D); disappears once those three are named directly

Recording preservation grammar:
established (05.Recording.A; corroborated by events-facts-and-state.md:10)

one universal/exact Recording responsibility:
not established; owner, Authority, Warrant, and occurrence-evidence are never
instantiated for a concrete recording act

Recording compression finding:
not silent bundling -- the chapter already separates production, establishment,
diagnostic rendering, recording, and extraction in its own prose; the gap is
incomplete ownership of the preservation decision and diagnostic-scoped
admission, both of which are named but never assigned an owner

PR 2238 replacement vocabulary (operation occurrence / operation-occurrence
record / operation status):
unsupported; same defect class as the vocabulary it replaced; needs correction
in the same pass that fixes its broken test assertions

smallest next active-Book step:
a bounded amendment to acts-and-act-artifacts.md, recording-and-knowledge-extraction.md,
and testimony-and-established-fact.md that (1) removes "operational" wherever it
modifies measurement/baseline/behavior/failure and substitutes act / act occurrence,
(2) removes the two umbrella phrases and lists the three already-named responsibilities
directly, (3) corrects PR 2238's three replacement terms to the same act-occurrence
vocabulary, and (4) does not attempt to assign owners to the preservation decision or
diagnostic-scoped admission in the same pass -- that recovery is separate and not yet done
```

This report does not draft that amendment. It does not decompose extraction, the preservation decision, or diagnostic-scoped admission beyond noting they are named and unowned — that is a further, separate recovery, not this one.
