# Book Constitutional Contamination-Pressure Inventory 001

## Scope and governing question

This report asks which active Book claims, grammatical constructions, examples, or local names may repeatedly pressure a reader or implementer toward unwarranted objects, actors, transitions, standings, orderings, scopes, or constitutional kinds. It does not assume contamination. The primary corpus was `book_of_seed/README.md`, `concordance.md`, `unresolved.md`, and every Markdown file in the active numbered chapter directories `01` through `06` and `08`. Root-level investigation reports under `book_of_seed/` were excluded from the primary finding set.

The examination proceeded in the required order: semantic reading of the active corpus; recovery of pressure families from claims; a second-pass, case-insensitive vocabulary search; bounded provenance recovery; and only then inspection of current implementation witnesses. Prior reports were not used to generate active findings.

## 1. Recovery discipline

The following inequalities govern every finding:

```text
lexical match != contamination
awkward wording != false constitutional claim
implementation similarity != causal origin
PR changed file != PR changed quoted wording
file added with wording = repository introduction evidence
repository introduction != conceptual origin
precursor wording != current exact wording
later expansion != original pressure source
local example != universal law
historical residue != active standing automatically
quoted evidence != adopted constitutional vocabulary
```

This inventory keeps two questions independent. **Claim standing** asks whether the complete claim, including its qualifications and cross-chapter narrowing, is faithful, creates contamination pressure, or remains Unknown. **Wording standing** asks whether the exact wording is active grammar, stale residue, a historical or local example, or Unknown. A faithful claim does not rehabilitate stale vocabulary, and a stale expression does not by itself make a constitutionally careful claim contaminated.

Suspect wording may be quoted without being canonized. Quotation must preserve the evidence under examination. Editorial cleanup inside a quotation destroys Fidelity. Accordingly, exact Book language appears below even where the quoted term has no adopted constitutional standing.

The second pass returned 226 matching lines for the supplied recall vocabulary and morphological variants. Most were explicit inequalities, counterexamples, scope limits, headings, index aliases, implementation identifiers, or ordinary descriptions. They were reviewed but omitted unless they contributed materially to a family below. In particular, ordinary uses of `act`, confidence preserved as a bounded dimension, exact identity matching, policy/precondition boundaries, and explicit denials of automatic transition were not treated as findings by lexical shape alone.

## 2. Recovered pressure-family topology

These are possible distortions, not one mandatory order:

```text
attributed record or representation
→ wording assigns its producer's verb to the representation
→ responsible occurrence becomes less visible
→ representation appears to own assertion, exposure, or movement
```

```text
distinct local standings
→ transition wording compresses responsible acts
→ availability appears to entail candidacy, request binding, or establishment
```

```text
local operator-ingress witness
→ exclusive or prerequisite language sounds general
→ a witness-local noun appears to define all goal establishment
```

```text
claim-relative evidence and consumer purpose
→ abstract sufficiency noun replaces the exact condition
→ threshold judgment appears portable between consumers
```

```text
preserved material → projection → consumer-local use
```

The last line is not compulsory: compression can make adjacency look ordered even though the active Book repeatedly says that availability, applicability, admission, consumption, Uptake, reliance, and standing change remain distinct and are not universally ordered.

## 3. Active Book findings

### A and J — Artifact agency; producer/consumer and act/artifact collapse

#### BCP-01

- **Finding id:** BCP-01
- **Pressure family:** artifact agency; act/artifact collapse
- **Book location:** `book_of_seed/06-state-and-projection/events-facts-and-state.md:10`
- **Bounded quotation:** “Events are immutable records that assert occurrences or other claims;”; “Facts carry supported normalized claims when their producer established bounded Fact standing,”; “A projection replays bounded recorded material under declared rules”.
- **Claim subject / verb / result:** Events **assert**, Facts **carry**, and a projection **replays** material, which may make record and representation nouns appear to own responsible production and projection acts.
- **Responsible producer:** a Fact producer is named later in the sentence; the Event assertion producer and projection occurrence are not named locally.
- **Responsible consumer:** named conditionally as “the responsible consumer” for current-standing use.
- **Distinction endangered:** recording occurrence / Event artifact; Fact-establishment act / Fact-shaped material; projection occurrence / projected representation.
- **Nearby narrowing:** the same sentence says recording does not make every asserted occurrence true, Fact-shaped material may lack Fact standing, projected material is not standing by identity, and consumer limits must be preserved.
- **Cross-chapter narrowing or contradiction:** `02-acts-and-constraints/acts-and-act-artifacts.md:10` says an artifact reports or preserves an assertion and construction does not prove the act; `06-state-and-projection/projection-and-current-state.md:10` makes projection and standing distinct.
- **Historical introduction:** Fragment-level evidence is recovered. PR #1742 added the cited file at commit `8406e6a` with the pressure-bearing precursor “facts carry supported claims”; this is repository-introduction evidence for the Fact “carry” pressure. The current Event noun using “assert” and projection noun using “replays” are later wording evolutions, but their exact changing commits are Unknown. Pre-Book conceptual or textual origin is Unknown.
- **Implementation correlation:** **direct lexical repetition** in `seed_runtime/models.py` (`Event`, `Fact`) and **structural similarity** in `seed_runtime/state.py` projection APIs. This does not establish direction or causation.
- **Claim standing:** candidate contamination pressure.
- **Wording standing:** active grammar.
- **Reasoning:** extensive local narrowing makes the constitutional content careful, but repeated inanimate subjects retain a compact agency grammar that could be copied without those qualifications.

#### BCP-02 / BCP-10

- **Finding ids:** BCP-02 and BCP-10. The identifiers are retained for cross-reference; they describe distinct pressures in the same bounded sentence and are consolidated here rather than assigning contradictory standings to duplicated evidence.
- **Pressure families:** artifact agency; automatic transition grammar; producer/consumer collapse; transfer-shorthand residue
- **Book location:** `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md:10`
- **Bounded quotation:** “Applicable examination methods become candidates; a bounded selection and handoff can bind a probe request. Probe output remains testimony or evidence until the relevant establishment boundary acts.”
- **Claim subject / verb / result:** methods **become** candidates; selection plus compressed transfer wording **binds** a request; a boundary **acts**.
- **Responsible producer:** Unknown for applicability and candidate formation; a bounded selection is named but its owner is not.
- **Responsible consumer:** “the relevant establishment boundary” is named only for later output standing; the request consumer is Unknown.
- **Distinction endangered:** applicability / candidate establishment; selection act / transfer / request formation; output artifact / later establishment.
- **Nearby narrowing:** output remains testimony or evidence; lines 12 and 26 separate applicability, selection, request, execution, and Fact establishment.
- **Cross-chapter narrowing or contradiction:** `01-grammar-and-standing/lenses-views-and-roads.md:14,20` requires consumer-local applicability and denies automatic crossings; `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md:12` denies the compressed transfer term Seed-native standing.
- **Historical introduction:** Repository introduction of the exact quoted sentence is recovered at commit `8406e6a` / PR #1742: that PR added the cited file containing the sentence. Pre-Book conceptual or textual origin is Unknown. Later active amendments added stronger consumer and communication distinctions without amending this line.
- **Implementation correlation:** **structural similarity** in probe-request and examination surfaces under `seed_runtime/`; no current implementation correlation proves that this sentence governs them.
- **Claim standing:** candidate contamination pressure.
- **Wording standing:** stale residue.
- **Reasoning:** three responsible boundaries are compressed into one sentence, and two are represented by nouns whose actors and consumers are absent. The automatic candidacy and request-binding claim supplies the candidate pressure; the later communication chapter expressly denies Seed-native standing to the retained transfer shorthand.

### B — Automatic transition grammar

BCP-02 is the active candidate in this family: “become candidates” can sound automatic. Most other matches are faithful denials. In particular, `01-grammar-and-standing/lenses-views-and-roads.md:14,20`, `03-goals-and-advancement/demands-and-opened-movement.md:11,41-43`, and `06-state-and-projection/events-facts-and-state.md:16,51` explicitly preserve responsible acts and local standings.

#### BCP-03

- **Finding id:** BCP-03
- **Pressure family:** automatic transition grammar; globalization of local standing
- **Book location:** `book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md:29-36`
- **Bounded quotation:** “sufficient common grammar established for the preserved ingress”; “original ingress re-enters interpretation, warrant, applicability, and admission”; “operator-origin BOGE may then be established”.
- **Claim subject / verb / result:** common grammar is **established**; preserved ingress **re-enters** interpretation; BOGE **may** be established.
- **Responsible producer:** a common-grammar establishment producer is not identified in the display.
- **Responsible consumer:** interpretation and BOGE consumers are not identified in the display.
- **Distinction endangered:** acquisition result / consumer-relative applicability / establishment; preserved ingress / interpretation occurrence; prerequisite availability / later admission.
- **Nearby narrowing:** lines 36, 50, and 54 call the branches guarded, require separately warranted selection and authority, and say common grammar does not retroactively interpret or admit ingress.
- **Cross-chapter narrowing or contradiction:** `01-grammar-and-standing/lenses-views-and-roads.md:20` denies a universal order and requires a responsible consumer-local revision occurrence.
- **Historical introduction:** commit `2c2c59e` / PR #2026 added the cited file with the quoted display. Commit `fe4b06c` / PR #2027 changed the bounded-resolution sentence to narrow BOGE establishment to the preserved ingress and deny a universal first event; it did not change the quoted display. Commit `af7758b` / PR #2028 later changed other display branches while preserving the quoted steps.
- **Implementation correlation:** **possible pressure relation** to operator-ingress acquisition-treatment diagnostics and console boundaries; whether any implementation consumer establishes the displayed standing remains Unknown.
- **Claim standing:** faithful within context.
- **Wording standing:** stale residue.
- **Reasoning:** the display alone compresses transitions, but the immediately surrounding prose explicitly restores optionality, distinct acts, authority, re-entry, applicability, and admission.

### C — Universal ordered-process pressure

#### BCP-04

- **Finding id:** BCP-04
- **Pressure family:** universal ordered-process pressure
- **Book location:** `book_of_seed/06-state-and-projection/events-facts-and-state.md:10`
- **Bounded quotation:** “These boundaries must remain visible even when one pipeline connects them.” The exact quoted `pipeline` is generic Book wording, not the exact named implementation subject `constitutional pipeline`; preserving it as evidence does not adopt it as constitutional vocabulary.
- **Claim subject / verb / result:** a singular implementation connection **connects** recording, Fact standing, projection, and current-standing boundaries.
- **Responsible producer / consumer:** the sentence names neither the connecting producer nor its scope; a bounded consumer is named earlier for standing.
- **Distinction endangered:** independent optional relations / one general ordered connection.
- **Nearby narrowing:** the full paragraph carefully denies identity between every adjacent standing.
- **Cross-chapter narrowing or contradiction:** `01-grammar-and-standing/lenses-views-and-roads.md:20,55` denies universal order and treats the exact `constitutional pipeline` implementation call order as local; `book_of_seed/README.md:16` denies order from Book numbering.
- **Historical introduction:** Fragment-level evidence is recovered. PR #1742 added the cited file at commit `8406e6a` with the pressure-bearing sentence “Their boundaries must remain visible even when one pipeline connects them.” This establishes repository introduction of the generic `pipeline` term and relation, not of the current exact sentence beginning “These boundaries”. The current exact-sentence amendment is a later wording evolution whose changing commit is Unknown. Pre-Book conceptual or textual origin is Unknown.
- **Implementation correlation:** **direct lexical repetition** exists only for the exact named `constitutional pipeline` implementation and its tests; **structural similarity** exists in ledger replay and projection. Neither proves a single general constitutional connection.
- **Claim standing:** candidate contamination pressure.
- **Wording standing:** active grammar.
- **Reasoning:** singular generic wording can reassemble carefully separated coordinates into a normal road, despite the paragraph's own non-equivalences.

### D — Scalar or threshold grammar

#### BCP-05

- **Finding id:** BCP-05
- **Pressure family:** scalar or threshold grammar; stopping/completion collapse
- **Book location:** `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md:7-10`
- **Bounded quotation:** “Which sufficiency, exhaustion, impossibility, refusal, or operator conditions warrant stopping, and which warrant completion?”; “including sufficiency projections, bounded horizons, policy blocks, and explicit goal status”; “Their complete constitutional ordering and the sufficient warrant for completion remain unclear.”
- **Claim subject / verb / result:** abstract sufficiency conditions **warrant** stopping or completion; projections appear among non-movement conditions.
- **Responsible producer:** Unknown.
- **Responsible consumer:** Unknown.
- **Distinction endangered:** claim- and consumer-relative warrant / scalar sufficiency; projected condition / responsible stopping or completion establishment.
- **Nearby narrowing:** the ordering and completion warrant are explicitly `[UNRESOLVED]`; lines 13-15 and 30-34 distinguish stop, completion, remaining Demand, failure, and global impossibility.
- **Cross-chapter narrowing or contradiction:** `01-grammar-and-standing/lenses-views-and-roads.md:12` says road sufficiency is local; `04-inquiry-and-examination/inquiry-frontiers.md:18` requires warrant sufficient for an exact claim, boundary, and reliance purpose.
- **Historical introduction:** Repository introduction of the exact quoted wording is recovered at commit `8406e6a` / PR #1742: that PR added the cited file containing the question, the sufficiency-projections clause, and the unresolved completion-warrant sentence. Pre-Book conceptual or textual origin is Unknown.
- **Implementation correlation:** **structural similarity** with sufficiency-named projections and bounded horizon surfaces; no causal relation is established.
- **Claim standing:** candidate contamination pressure.
- **Wording standing:** stale residue.
- **Reasoning:** this is deliberately unresolved, but abstract nouns and an unnamed consumer can still license a portable threshold reading.

#### BCP-06

- **Finding id:** BCP-06
- **Pressure family:** scalar grammar
- **Book location:** `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md:12`
- **Bounded quotation:** evidence and limits “are sufficient for that consumer boundary”; “Road sufficiency is local”.
- **Claim subject / verb / result:** preserved evidence and limits **are sufficient**, enabling bounded consumer use.
- **Responsible producer:** upstream producer, locally bounded.
- **Responsible consumer:** explicitly “that consumer boundary”.
- **Distinction endangered:** none after local qualification; a detached excerpt could lose the condition.
- **Nearby narrowing:** purpose, warrant, identity, authority, confidence, Unknowns, producer warrant, artifact preservation, and consumer validation are explicit.
- **Cross-chapter narrowing or contradiction:** consistent with the exact-claim formulation in `04-inquiry-and-examination/inquiry-frontiers.md:18`.
- **Historical introduction:** Fragment-level evidence is recovered. “Road sufficiency is local” is present by commit `f9b2516` / PR #1746, the earliest verified occurrence in a commit that changed the cited file. The exact introduction commit for the later clause “the preserved evidence, warrant, identity, scope, authority, confidence, and Unknown limits are sufficient for that consumer boundary” is Unknown: the examined uptake amendments do not supply a recovered patch establishing its addition. PR #1983 changed the cited file while preserving that clause and added separate uptake narrowing; PR #1984 changed another sentence only. Pre-Book conceptual or textual origin is Unknown.
- **Implementation correlation:** no current implementation correlation found beyond ordinary sufficiency vocabulary.
- **Claim standing:** faithful within context.
- **Wording standing:** stale residue.
- **Reasoning:** the retired scalar form remains, but here it names an exact consumer-relative condition rather than an abstract score.

The search also reviewed `threshold`, `score`, `confidence`, `probability`, `strongest`, `best`, `rank`, `enough`, and `adequate`. Confidence is ordinarily a preserved bounded dimension; rank is a permitted projection method, not authority; “enough” at the ingress witness is bounded to examination of preserved ingress. No independent active candidate was recovered from the other terms.

### E — Globalization of local standing

#### BCP-07

- **Finding id:** BCP-07
- **Pressure family:** globalization of local standing
- **Book location:** `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md:49`
- **Bounded quotation:** “repeated bounded failure to establish sufficient common grammar for an operator interaction may expose pressure to establish a common-grammar relation.”
- **Claim subject / verb / result:** repeated failure **may expose** pressure for a common-grammar relation.
- **Responsible producer:** failure-measurement producer Unknown.
- **Responsible consumer:** consumer of recurrence and establisher of the relation Unknown.
- **Distinction endangered:** interaction-local obstruction evidence / a generalized common-grammar relation; recurrence / Demand pressure.
- **Nearby narrowing:** the interaction is singular and bounded; recurrence is measurement, not meaning, selection, authority, or execution.
- **Cross-chapter narrowing or contradiction:** `03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md:44,50` denies automatic Demand establishment and global bootstrap.
- **Historical introduction:** commit `b5dc93c` / PR #1999 introduced this recoverable wording under the earlier filename; later rename/amendment preserved it.
- **Implementation correlation:** **direct lexical repetition** in operator-ingress common-grammar surfaces; **possible pressure relation** only. The implementation witness is similarly local.
- **Claim standing:** candidate contamination pressure.
- **Wording standing:** stale residue.
- **Reasoning:** “a common-grammar relation” leaves consumer, material, act, and purpose implicit and can sound like a shared global object when detached from the bounded example.

### F — Witness-local naming promoted into constitutional kind

#### BCP-08

- **Finding id:** BCP-08
- **Pressure family:** witness-local naming promoted into constitutional kind; closed taxonomy pressure
- **Book location:** `book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md:9`
- **Bounded quotation:** “BOGE is Seed's only goal-establishment apparatus”.
- **Claim subject / verb / result:** BOGE **is** the exclusive apparatus for goal establishment.
- **Responsible producer / consumer:** operator origin is named; the establishing boundary is represented by the BOGE noun, and its consumer is not named.
- **Distinction endangered:** current operator-origin witness / general constitutional kind; one apparatus / all lawful goal-establishment realizations.
- **Nearby narrowing:** the paragraph denies self-goals, instrumental goals, another goal, and a universal first event.
- **Cross-chapter narrowing or contradiction:** `03-goals-and-advancement/construction-and-establishment.md:4-16` defines the constitutional boundary without making BOGE a universal implementation object; `README.md:5,12` says implementation anchors are illustrative testimony.
- **Historical introduction:** commit `2c2c59e` / PR #2026 added the cited file with the exclusive BOGE wording. Commit `fe4b06c` / PR #2027 changed the remainder of that sentence to narrow ingress scope and deny a universal first event; it did not introduce the quoted exclusivity. Any pre-Book origin is Unknown.
- **Implementation correlation:** **direct lexical repetition** in bounded operator-goal establishment production and CLI witnesses.
- **Claim standing:** candidate contamination pressure.
- **Wording standing:** active grammar.
- **Reasoning:** the operator-origin exclusion may be constitutionally intended, but “only ... apparatus” can promote the first named implementation-shaped witness into the sole general object. Intended realization breadth remains Unknown.

CLI names, developer-compiled observers, current runtime response, and diagnostic names were inspected where the active Book mentions them. Most are expressly marked representative anchors, implementation testimony, compatibility surfaces, or current implementation inventories and therefore are **historical or local example**, not independent findings.

### G — Closed taxonomy pressure

#### BCP-09

- **Finding id:** BCP-09
- **Pressure family:** closed taxonomy pressure
- **Book location:** `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md:53-65`
- **Bounded quotation:** “This counterexample demonstrates only that the four canonical families are not a universal taxonomy.”
- **Claim subject / verb / result:** the example **demonstrates** that four local families are non-exhaustive.
- **Responsible producer / consumer:** the example author demonstrates; no operational consumer is asserted.
- **Distinction endangered:** none in context; the numeral can look closed only if the denial is dropped.
- **Nearby narrowing:** calls the topology illustrative, permits zero or more local crossings, and creates no fifth family.
- **Cross-chapter narrowing or contradiction:** `book_of_seed/README.md:5,12` denies complete-inventory standing and marks anchors illustrative.
- **Historical introduction:** commit `b5dc93c` / PR #1999 changed the cited file and added the bounded four-family counterexample. Commit `21820e4` / PR #2019 changed the qualifier to the current exact “four canonical families” wording. No earlier occurrence was recovered; any pre-Book origin is Unknown.
- **Implementation correlation:** no current implementation correlation found that makes the four families exhaustive.
- **Claim standing:** faithful within context.
- **Wording standing:** active grammar.
- **Reasoning:** the active claim opens rather than closes the taxonomy.

### H — Agent, decision, action, execution, and transfer-shorthand residue

BCP-10 is consolidated with BCP-02 above. Its transfer-shorthand evidence, pressure family, stale wording standing, implementation correlation, and cross-chapter narrowing are preserved there.

Other `decision`, `action`, and `execution` matches describe bounded responsible judgments, external realization, forbidden inferences, compatibility aliases, or explicit non-equivalences. Ordinary constitutional `act` was not included. No active agent/controller/manager/lifecycle/workflow ownership candidate survived semantic review.

### I — Stopping and completion collapse

BCP-05 carries the only retained candidate pressure in this family. The controlling active distinctions are unusually explicit: `08-authority-communication-and-stopping/stopping-and-completion.md:13-15,30-34` says stopping is not completion or failure, local exhaustion is not global impossibility, and no selection does not erase Demand. `08-authority-communication-and-stopping/refusal-and-non-performance.md:10-15` also separates refusal, policy blocks, failed preconditions, clarification, abandonment, and execution failure. These are **faithful within context**.

## 4. Cross-chapter narrowing map

| Risky shorthand | Narrowing chapter | Relationship |
|---|---|---|
| Event/Fact/projection nouns use act-like verbs (`06...events-facts-and-state.md:10`) | `02...acts-and-act-artifacts.md:10`; `06...projection-and-current-state.md:10` | claim remains candidate pressure despite narrowing |
| methods “become” candidates and compressed transfer binds a request (`04...examination-methods-and-probes.md:10`) | `01...lenses-views-and-roads.md:14,20`; `08...representation-emission-and-consumer-boundaries.md:12` | automatic grammar remains candidate; transfer noun is stale residue |
| displayed common-grammar road (`03...operator-ingress...md:29-36`) | same file `:36,42-54`; `01...lenses-views-and-roads.md:20` | claim is faithful only when read with local and cross-chapter narrowing |
| singular generic implementation connection (`06...events-facts-and-state.md:10`) | `01...lenses-views-and-roads.md:20,55` | claim remains candidate pressure despite narrowing |
| sufficiency projections and completion warrant (`08...stopping-and-completion.md:7-10`) | same file `:13-15,30-34`; `04...inquiry-frontiers.md:18` | pressure remains; intended exact condition is Unknown |
| common-grammar relation (`03...demands-and-opened-movement.md:49`) | `03...operator-ingress...md:44,50,54` | relationship remains candidate pressure; global standing is denied elsewhere |
| “only” BOGE apparatus (`03...operator-ingress...md:9`) | `03...construction-and-establishment.md:4-16`; Book `README.md:5,12` | intended exclusivity remains Unknown |
| transfer shorthand (`04...examination-methods-and-probes.md:10`) | `08...representation-emission-and-consumer-boundaries.md:12` | stale residue |

## 5. Historical provenance map

The map keeps changed-file evidence separate from quoted-wording evidence. A file added with wording supplies repository-introduction evidence for that wording, not its pre-Book conceptual origin. A later change that preserves wording is preservation only, and a pressure-bearing precursor does not establish introduction of a later exact sentence. The local investigation incorrectly encountered commit `012be5d` as a shallow or merge-adjacent history boundary. PR #1949 did not modify the cited Book files and supplies no provenance evidence for their wording.

| Finding id | Quoted fragment or pressure-bearing precursor | Cited Book file | Repository introduction or earliest verified changing commit | Associated PR | Later wording changes or narrowing | Current exact wording introduction | Pre-Book origin |
|---|---|---|---|---|---|---|---|
| BCP-01 | “facts carry supported claims” precursor | `book_of_seed/06-state-and-projection/events-facts-and-state.md` | `8406e6a`; repository introduction recovered because the file was added with the fragment | PR #1742 | Current Event “assert” and projection “replays” forms are later expansions | Fact “carry” pressure-bearing precursor recovered; later exact Event and projection wording introduction Unknown | Unknown |
| BCP-01 | Event noun using “assert”; projection noun using “replays” | `book_of_seed/06-state-and-projection/events-facts-and-state.md` | later changing commits not recovered | — | The PR #1742 skeleton instead used “records of occurrences or assertions” and “state is a replayed ... projection” | current exact wording introduction Unknown | Unknown |
| BCP-02 / BCP-10 | exact quoted examination sentence | `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md` | `8406e6a`; repository introduction recovered because the file was added with the exact sentence | PR #1742 | later consumer and communication grammar narrows the relation in other files | recovered at `8406e6a` | Unknown |
| BCP-03 | quoted common-grammar display | `book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md` | `2c2c59e`; file and exact display introduction recovered | PR #2026 | `fe4b06c` / PR #2027 narrowed the bounded-resolution sentence, not the display; `af7758b` / PR #2028 changed other display branches while preserving the quoted steps | recovered at `2c2c59e` | Unknown |
| BCP-04 | “Their boundaries must remain visible even when one pipeline connects them.” | `book_of_seed/06-state-and-projection/events-facts-and-state.md` | `8406e6a`; pressure-bearing precursor and generic `pipeline` relation introduced with the file | PR #1742 | later grammatical expansion changed “Their” to current “These” | current exact wording introduction Unknown | Unknown |
| BCP-05 | quoted stopping/completion sufficiency wording | `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md` | `8406e6a`; repository introduction recovered because the file was added with the exact wording | PR #1742 | later stopping corrections changed the file but preserved the quoted wording; later preservation only | recovered at `8406e6a` | Unknown |
| BCP-06 | “Road sufficiency is local” | `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md` | `f9b2516`; earliest verified occurrence in a commit that changed the cited file | PR #1746 | later uptake amendments preserved the phrase | not claimed beyond earliest verified changed-file occurrence | Unknown |
| BCP-06 | “the preserved evidence, warrant, identity, scope, authority, confidence, and Unknown limits are sufficient for that consumer boundary” | `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md` | exact adding patch not recovered | — | `e34d26b` / PR #1983 preserved the clause while adding separate uptake narrowing; `3f9b054` / PR #1984 changed another sentence only | current exact wording introduction Unknown | Unknown |
| BCP-07 | quoted bounded common-grammar-relation counterexample | `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md` | `b5dc93c`; exact wording introduction recovered under the earlier filename | PR #1999 | Demand rename and later amendments preserved it; rename/preservation only | recovered at `b5dc93c` | Unknown |
| BCP-08 | “BOGE is Seed's only goal-establishment apparatus” | `book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md` | `2c2c59e`; file and exact wording introduction recovered | PR #2026 | `fe4b06c` / PR #2027 changed the rest of the sentence and narrowed scope; quoted exclusivity preserved | recovered at `2c2c59e` | Unknown |
| BCP-09 | non-universal four-family counterexample and current “four canonical families” qualifier | `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md` | `b5dc93c` introduced the counterexample; `21820e4` introduced the current exact qualifier | PR #1999; PR #2019 | later Demand rename/amendments preserved the non-universal qualification; rename/preservation only | recovered at `21820e4` | Unknown |

These associations establish repository introduction, changed-file occurrence, narrowing, or preservation only as stated. They establish neither authorship nor causal influence.

## 6. Current implementation correlations

Implementation inspection followed, rather than generated, the Book findings.

- **BCP-01:** `Event`, `Fact`, State projection, `FactSupport`, and `FactView` names are compatible with object-as-actor readings. Classification: **direct lexical repetition** plus **structural similarity**. Production also contains provenance and read-only boundaries that contradict stronger standing by identity.
- **BCP-02/BCP-10:** probe request, selection, and examination surfaces preserve similar adjacency. Classification: **structural similarity**; exact responsible consumer and any pressure relation are Unknown.
- **BCP-03/BCP-07/BCP-08:** operator-ingress common-grammar and acquisition-treatment surfaces repeat the witness-local nouns. Classification: **direct lexical repetition** and **possible pressure relation**. Their locality also supplies contradicting evidence against global scope.
- **BCP-04:** the exact `constitutional pipeline` implementation is a bounded diagnostic composition surface, while ledger projection is a different road. Classification: **contradicting implementation evidence** against one general ordered process, alongside local structural similarity.
- **BCP-05:** sufficiency and horizon-named projections are compatible with scalar stopping grammar. Classification: **possible pressure relation**; no evidence shows that projection alone performs completion.
- **BCP-06/BCP-09:** **no current implementation correlation found** material to the bounded pressure question.

No correlation establishes a causal relation between Book wording and implementation behavior.

## 7. Highest-pressure active claims

This is a short non-numeric set, not a ranking or prescription:

- **The examination sentence (BCP-02/BCP-10):** claim standing is **candidate contamination pressure**; wording standing is **stale residue**. It compresses several responsible coordinates, retains non-native transfer shorthand, and resembles current probe-request composition.
- **The singular generic connection (BCP-04):** claim standing is **candidate contamination pressure**; wording standing is **active grammar**. It sits inside otherwise careful State grammar but can restore an unwarranted general ordering. The generic quoted `pipeline` is not the named implementation subject by identity.
- **The abstract stopping/completion sufficiency grammar (BCP-05):** claim standing is **candidate contamination pressure**; wording standing is **stale residue**. The claim is unresolved, leaves producer and consumer unnamed, and is compatible with current projection nouns.
- **The exclusive BOGE apparatus claim (BCP-08):** claim standing is **candidate contamination pressure**; wording standing is **active grammar**. It is categorical and directly repeats a current operator-ingress witness even though its intended constitutional-versus-realization scope remains Unknown.
- **The common-grammar relation (BCP-07):** claim standing is **candidate contamination pressure**; wording standing is **stale residue**. It can hide consumer, material, act, and purpose coordinates and appear global when removed from its bounded interaction example.

## 8. Remaining Unknowns

- Historical origin before the first recoverable Book commits for most findings.
- Whether BOGE exclusivity names constitutional origin only or also requires one realization apparatus.
- The producers and consumers for applicability, candidacy, common-grammar establishment, recurrence pressure, request binding, stopping, and completion in the cited shorthand.
- The exact consumer-relative condition intended by “sufficiency projections” and “sufficient warrant for completion”.
- Whether the generic connection wording in State is deliberately ordinary implementation description or intended topology.
- Whether the examination transfer noun was deliberately retained as an external/local term after the communication correction.
- Whether implementation similarities preserved Book grammar, supplied testimony for it, or arose independently.
- Whether apparent cross-chapter contradictions are deliberate local distinctions. Where repository evidence does not resolve these questions, standing remains Unknown.

## 9. Required conclusion

### Recovered active claim pressures

BCP-01, BCP-02/BCP-10, BCP-04, BCP-05, BCP-07, and BCP-08 remain candidate contamination pressures. The faithful contextual claims in BCP-03, BCP-06, and BCP-09 remain recovered rather than being discarded merely because two contain stale wording.

### Recovered stale wording

The retired `sufficient`, `insufficient`, and `sufficiency` forms remain outside current constitutional vocabulary. BCP-03 and BCP-06 therefore pair a faithful contextual claim with stale wording; BCP-05 and BCP-07 pair candidate pressure with stale wording. BCP-02/BCP-10 also preserves stale transfer shorthand. Exact quotation of these forms is evidence preservation, not rehabilitation.

### Verified historical provenance

PR #1742 introduced the Book skeleton and supplies repository-introduction evidence for the exact examination sentence, the stopping/completion sufficiency wording, and the generic State `pipeline` precursor. Later commits supplied expanded or revised forms whose exact introduction is reported separately where recovered. PR #1999 introduced the Demand counterexamples, PR #2019 supplied BCP-09's current exact qualifier, and PR #2026 introduced the operator-ingress chapter and relevant wording; PR #2027 narrowed surrounding wording, while PR #2028 changed other branches and preserved the quoted steps. PR #1949 did not modify the cited Book files and supplies no provenance evidence for these findings.

### Historical provenance remaining Unknown

Pre-Book conceptual or textual origin remains Unknown for every finding. Current exact wording introduction remains Unknown for the later BCP-01 Event “assert” and projection “replays” fragments, the BCP-04 “These boundaries” amendment, and the BCP-06 consumer-boundary clause. Those Unknowns do not erase the recovered PR #1742 repository introductions or pressure-bearing precursors, nor the earliest verified changed-file occurrence for the separate BCP-06 road-sufficiency fragment.

### Amendment posture

This report proposes no Book amendment, replacement wording,
implementation change, bridge, or cleanup sequence.
