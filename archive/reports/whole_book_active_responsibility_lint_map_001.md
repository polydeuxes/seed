# Whole-Book active responsibility-lint map 001

## 1. Executive map

This Phase 2, PR 1 report is a bounded map, not a clause-level audit. A candidate means only **candidate for bounded review**. It does not mean that wording is defective, a subject is unsupported, an act lacks an owner, or a clause should be amended.

- Active Book Markdown files inspected: **34**.
- Raw search hits across the six required candidate-generation expressions, limited to those 34 files: **954**. A hit is one matching file/line returned by one expression, so a line returned by two expressions contributes two raw hits.
- Unique search-hit lines after exact file-and-line deduplication: **577**.
- Deduplicated material candidate lines after direct-context review: **478**.
- Files with at least one material candidate: **26**.
- Files with no material candidate: **8**.
- Complete file coverage: **yes**.

Candidate-family totals overlap because one candidate line can belong to several families:

| Candidate family | Candidate lines |
| --- | ---: |
| 1. Passive constitutional act | 25 |
| 2. Result-like subject | 415 |
| 3. Standing or status assertion | 175 |
| 4. Relation assertion | 90 |
| 5. Producer or responsibility candidate | 319 |
| 6. Consumer or demand candidate | 171 |
| 7. Repository-current testimony candidate | 5 |
| 8. Repeated normative formula candidate | 60 |
| 9. Alternative-route candidate | 27 |
| 10. Vocabulary-hook candidate | 116 |

| Active Book directory/chapter family | Files | Candidate lines | Lines/file |
| --- | ---: | ---: | ---: |
| Book root | 3 | 8 | 2.7 |
| `01-grammar-and-standing` | 5 | 86 | 17.2 |
| `02-acts-and-constraints` | 4 | 45 | 11.3 |
| `03-goals-and-advancement` | 6 | 143 | 23.8 |
| `04-inquiry-and-examination` | 3 | 26 | 8.7 |
| `05-evidence-and-knowledge` | 4 | 78 | 19.5 |
| `06-state-and-projection` | 4 | 28 | 7.0 |
| `08-authority-communication-and-stopping` | 5 | 64 | 12.8 |

## 2. Method

### Authority and scope

The authority order used here is:

```text
current active Book:
constitutional authority

reachable production:
current implementation occurrence evidence

tests:
canonical-text and implementation testimony

historical reports:
attributed recovery testimony

Git history:
provenance testimony

names, recurrence, adjacency, and stylistic plausibility:
not authority by identity
```

The active-law inventory is the 31 Markdown files in the numbered Book directories plus the root `README.md`, `concordance.md`, and `unresolved.md`. Root files named as audits, recoveries, surveys, passes, amendments, corrections, and other numbered reports were distinguished by their report character and excluded. No Markdown outside `book_of_seed/` was included. This new report was not counted. Historical reports were not substantively inspected, and no Git-history provenance tracing was performed.

### Enumeration and searches

The inventory began with:

```bash
find book_of_seed -type f -name '*.md' | sort
```

The six required `git grep -n -E` searches were run for: the listed passive forms; result/standing vocabulary; consumer/demand vocabulary; repository-current phrases; vocabulary hooks; and potentially load-bearing alternatives. For the reported raw count, the same expressions were restricted to the active-law inventory so historical-report matches did not inflate an active-Book measure.

Every hit's surrounding paragraph or section was read. Lines were keyed by exact active file and one-based line number. Repeated hits from one search or across searches were collapsed to one candidate line. Every applicable family was then attached to that line, so family totals are intentionally non-additive. Navigation-only headings, concordance rows, directory README links, ordinary passive English, incidental lexical uses, and ordinary conjunctions were excluded.

The review lens was responsibility **R**, act **A**, subject **S**, purpose **P**, inputs or prior standing **I**, warrant and authority **W**, locality **L**, bounded result **O**, consumer **C**, and preserved limits/conflicts/loss/provenance/negative authority/Unknowns. A sentence was not expected to restate every coordinate.

Explicit interpretation limits:

```text
candidate count != defect count
recurrence != authority
passive voice != absent responsibility
term occurrence != constitutional subject
```

This is a text map. It does not establish runtime reachability, implementation demand, provenance, lawful ownership, or a constitutional disposition. Counts depend on the stated searches and direct-review threshold; a later bounded audit may narrow or expand a family without invalidating this coverage map.

## 3. Active Book file map

Priority is workload/risk triage only, not a constitutional disposition. Family numbers refer to the ten families above.

| Active Book file | Book directory | Principal constitutional subject matter | Candidate lines | Candidate families present | Highest-density family | Direct-review priority | Notes |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `book_of_seed/README.md` | Book root | Book status, use, and navigation | 4 | 2, 4, 5, 7, 8, 10 | result-like subject | low | Repository-current framing warrants bounded separation from law. |
| `book_of_seed/concordance.md` | Book root | Navigation aliases and cross-references | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/unresolved.md` | Book root | Explicitly unresolved questions | 4 | 2, 3, 4, 5, 6 | result-like subject | low | Questions are mapped, not answered. |
| `book_of_seed/01-grammar-and-standing/README.md` | `01-grammar-and-standing` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` | `01-grammar-and-standing` | Kinds, artifacts, relations, applicability, Unknowns | 35 | 1–10 | result-like subject | high | Dense cross-family standing and applicability formulas. |
| `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md` | `01-grammar-and-standing` | Construction and production authority | 12 | 2, 3, 5, 6, 7, 9, 10 | result-like subject | medium | Includes repository-current producer illustration. |
| `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md` | `01-grammar-and-standing` | Translation, external grammar, Fidelity | 11 | 1–10 except 7 | result-like subject | medium | Translation and cross-seam alternatives merit bounded review. |
| `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md` | `01-grammar-and-standing` | Views, roads, uptake, representation | 28 | 1–10 except 7 | result-like subject | high | Dense producer/consumer and standing boundaries. |
| `book_of_seed/02-acts-and-constraints/README.md` | `02-acts-and-constraints` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md` | `02-acts-and-constraints` | Acts, occurrence, act artifacts | 12 | 1, 2, 3, 5, 6, 8, 10 | result-like subject | medium | Act/result separation is the main later-review seam. |
| `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md` | `02-acts-and-constraints` | Constraints, policy, preconditions | 12 | 1–8, 10 | result-like subject | medium | Admission/refusal and responsible evaluation recur. |
| `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md` | `02-acts-and-constraints` | Selection artifacts and acts | 21 | 2–6, 10 | producer/responsibility | high | Selection producers, standing, and downstream use cluster. |
| `book_of_seed/03-goals-and-advancement/README.md` | `03-goals-and-advancement` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/03-goals-and-advancement/construction-and-establishment.md` | `03-goals-and-advancement` | Goal construction and establishment | 24 | 2–6, 8, 10 | result-like subject | high | Establishment and resulting standing are dense. |
| `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md` | `03-goals-and-advancement` | Demand and movement opening | 22 | 2–10 except 7 | result-like subject | high | Demand/consumer and alternative-route candidates co-occur. |
| `book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md` | `03-goals-and-advancement` | Operator ingress and common grammar | 78 | 1–6, 8, 10 | result-like subject | high | Highest absolute candidate workload; split its follow-up by section. |
| `book_of_seed/03-goals-and-advancement/orientation-and-movement.md` | `03-goals-and-advancement` | Orientation and movement | 8 | 2, 3, 5, 6, 8, 9, 10 | result-like subject | medium | Alternatives and movement results need bounded review. |
| `book_of_seed/03-goals-and-advancement/selection-and-authorization.md` | `03-goals-and-advancement` | Consideration selection and authorization | 11 | 2–6, 10 | producer/responsibility | medium | Selection/authorization ownership is the principal seam. |
| `book_of_seed/04-inquiry-and-examination/README.md` | `04-inquiry-and-examination` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md` | `04-inquiry-and-examination` | Inquiry boundaries and frontiers | 8 | 2–6, 9, 10 | result-like subject | medium | Frontier alternatives and findings merit a small audit. |
| `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md` | `04-inquiry-and-examination` | Questions and inquiry | 18 | 2–9 except 7 | result-like subject | medium | Question standing and evidence demand recur. |
| `book_of_seed/05-evidence-and-knowledge/README.md` | `05-evidence-and-knowledge` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md` | `05-evidence-and-knowledge` | Evidence, provenance, explanation | 17 | 2–6, 8, 10 | result-like subject | medium | Support relations and consumer reliance dominate. |
| `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md` | `05-evidence-and-knowledge` | Recording and knowledge extraction | 17 | 1–3, 5, 6, 8–10 | result-like subject | medium | Production/recording boundaries and routes recur. |
| `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md` | `05-evidence-and-knowledge` | Testimony, Claim, Fact standing | 44 | 1–10 | result-like subject | high | All families occur; repository-current compression is explicit. |
| `book_of_seed/06-state-and-projection/README.md` | `06-state-and-projection` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/06-state-and-projection/events-facts-and-state.md` | `06-state-and-projection` | Events, facts, state | 14 | 2–10 except 7 | result-like subject | medium | Projection, support, and state assertions intersect. |
| `book_of_seed/06-state-and-projection/ownership-discrepancy-and-residue.md` | `06-state-and-projection` | Ownership discrepancy and residue | 2 | 2, 3, 4, 5, 8 | repeated formula | low | Small, bounded formula review. |
| `book_of_seed/06-state-and-projection/projection-and-current-state.md` | `06-state-and-projection` | Projection and current state | 12 | 2–8, 10 | result-like subject | medium | Repository-current FactView wording is explicit. |
| `book_of_seed/08-authority-communication-and-stopping/README.md` | `08-authority-communication-and-stopping` | District navigation | 0 | — | — | none | no material candidate under this mapping pass |
| `book_of_seed/08-authority-communication-and-stopping/authority-scope.md` | `08-authority-communication-and-stopping` | Authority and scope | 8 | 2–6, 8, 10 | result-like subject | medium | Authority relations and limits are compact. |
| `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md` | `08-authority-communication-and-stopping` | Refusal and non-performance | 4 | 2, 3, 4, 5, 8 | producer/responsibility | low | Small refusal-owner seam. |
| `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md` | `08-authority-communication-and-stopping` | Representation, emission, consumers | 47 | 1–10 except 7 | result-like subject | high | Second-highest workload; consumer boundaries are dense. |
| `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md` | `08-authority-communication-and-stopping` | Stop and completion | 5 | 2, 3, 5, 6, 8 | result-like subject | low | Compact stopping/result review. |

## 4. Candidate-family distribution

### 1. Passive constitutional act

- **Definition:** a constitutional act or reliance is expressed in a passive shape whose responsible occurrence may merit direct examination.
- **Total / files:** **25 lines / 12 files**.
- **Highest-density files:** `constitutional-kinds-and-artifact-standing.md`, `lenses-views-and-roads.md`, and `testimony-and-established-fact.md`.
- **Representative excerpts:** “applicability is determined”; “A Fidelity finding is produced”; “may be consumed”; “is established”; “may be relied upon.”
- **False positives excluded:** passive descriptions of document layout, historical action, and non-constitutional English.
- **Bounded follow-up:** examine Books I–II first for whether nearby owner/occurrence clauses already bound each passive expression.

### 2. Result-like subject

- **Definition:** load-bearing finding, testimony, standing, result, determination, classification, establishment, applicability, admission, authorization, selection, warrant, refusal, or stop subjects.
- **Total / files:** **415 lines / 26 files**.
- **Highest-density files:** `operator-ingress-common-grammar-prerequisite.md`, `representation-emission-and-consumer-boundaries.md`, `testimony-and-established-fact.md`.
- **Representative excerpts:** “Fact standing”; “exact applicability result”; “selection standing”; “lawful stop”; “bounded finding.”
- **False positives excluded:** concordance vocabulary, headings, navigation lists, and incidental ordinary-language results.
- **Bounded follow-up:** divide review by chapter subject; do not attempt a cross-Book clause ledger first.

### 3. Standing or status assertion

- **Definition:** a clause states or implies that a subject has bounded standing or status.
- **Total / files:** **175 lines / 25 files**.
- **Highest-density files:** `operator-ingress-common-grammar-prerequisite.md`, `testimony-and-established-fact.md`, `constitutional-kinds-and-artifact-standing.md`.
- **Representative excerpts:** “constitutional Fact standing”; “Question standing”; “selection standing”; “current standing”; “applicability standing.”
- **False positives excluded:** the Book I navigation title and concordance cross-references.
- **Bounded follow-up:** Books I–II responsibility-and-standing report, then evidence-specific standing in Book V.

### 4. Relation assertion

- **Definition:** wording asserts identification, representation, expression, dependence, participation, applicability, support, authorization, constraint, or evidentiary relation.
- **Total / files:** **90 lines / 22 files**.
- **Highest-density files:** `constitutional-kinds-and-artifact-standing.md`, `operator-ingress-common-grammar-prerequisite.md`, `representation-emission-and-consumer-boundaries.md`.
- **Representative excerpts:** “X identifies, represents, or expresses Y”; “evidence supports”; “applies to”; “participates in”; “authorizes movement.”
- **False positives excluded:** hyperlinks, chapter relationships in navigation, and grammatical conjunction without a constitutional relation claim.
- **Bounded follow-up:** review Book I relation law before the Book V and VIII relation uses.

### 5. Producer or responsibility candidate

- **Definition:** a clause appears to produce, revise, establish, preserve, recover, compare, classify, admit, select, authorize, refuse, stop, record, or project constitutionally.
- **Total / files:** **319 lines / 25 files**.
- **Highest-density files:** `operator-ingress-common-grammar-prerequisite.md`, `representation-emission-and-consumer-boundaries.md`, `testimony-and-established-fact.md`.
- **Representative excerpts:** “responsible occurrence warrants”; “may establish”; “records testimony”; “selects”; “must refuse.”
- **False positives excluded:** report provenance, document maintenance instructions, and mere noun labels without an act.
- **Bounded follow-up:** audit responsible acts by Book district, preserving local purpose and occurrence rather than inferring ownership from verbs.

### 6. Consumer or demand candidate

- **Definition:** a clause names or implies a consumer, reliance, downstream/local use, demand, required result, or admission before use.
- **Total / files:** **171 lines / 23 files**.
- **Highest-density files:** `representation-emission-and-consumer-boundaries.md`, `operator-ingress-common-grammar-prerequisite.md`, `lenses-views-and-roads.md`.
- **Representative excerpts:** “later consumer”; “consumer-local occurrence”; “downstream purpose”; “may rely”; “Demand.”
- **False positives excluded:** ordinary “required” prose with no result/use boundary and README requirements for readers.
- **Bounded follow-up:** Books III–IV demand report followed by the Book VIII representation/consumer report.

### 7. Repository-current testimony candidate

- **Definition:** prose may describe current repository or implementation shape rather than durable constitutional law.
- **Total / files:** **5 lines / 4 files**.
- **Highest-density files:** one line each in the root `README.md`, `constructors-and-production-authority.md`, `testimony-and-established-fact.md`, and `projection-and-current-state.md` (the README has two distinct search phrases on one line pair).
- **Representative excerpts:** “current repository”; “current implementation”; “often a Python function or method”; “named `FactView`.”
- **False positives excluded:** constitutional “current standing,” “current condition,” and temporal applicability.
- **Bounded follow-up:** one small repository-current testimony report across these four files.

### 8. Repeated normative formula candidate

- **Definition:** materially recurring exact or close formula, recorded without deciding canonical ownership or useful local restatement.
- **Total / files:** **60 lines / 22 files**.
- **Highest-density files:** `operator-ingress-common-grammar-prerequisite.md`, `constitutional-kinds-and-artifact-standing.md`, `testimony-and-established-fact.md`.
- **Representative excerpts:** “does not by itself establish”; “must preserve”; “does not automatically”; “must not”; “is not by identity.”
- **False positives excluded:** repeated headings, concordance cells, Markdown structure, and isolated non-normative phrases.
- **Bounded follow-up:** defer synthesis until chapter-family reports establish local context.

### 9. Alternative-route candidate

- **Definition:** an alternative appears capable of creating another warrant, authority, producer, evidence basis, or constitutional road.
- **Total / files:** **27 lines / 14 files**.
- **Highest-density files:** `constitutional-kinds-and-artifact-standing.md`, `external-and-constitutional-grammar.md`, `demands-and-opened-movement.md`.
- **Representative excerpts:** “authority or evidence”; “determine or consume applicability standing”; “separate bounded warrant”; “another responsible occurrence.”
- **False positives excluded:** ordinary lists joined by “or,” alternative outcomes within one already-bounded result, and prose choices that create no route.
- **Bounded follow-up:** combine active alternatives with vocabulary hooks in the smallest first report.

### 10. Vocabulary-hook candidate

- **Definition:** descriptive compounds or condition/result vocabulary resemble constitutional kinds, relations, results, or responsibilities enough to invite later identity promotion.
- **Total / files:** **116 lines / 22 files**.
- **Highest-density files:** `operator-ingress-common-grammar-prerequisite.md`, `constitutional-kinds-and-artifact-standing.md`, `representation-emission-and-consumer-boundaries.md`.
- **Representative excerpts:** “readiness”; “conditional input applicability”; “automatic correction authority”; “shared purpose”; “input-set sufficiency.”
- **False positives excluded:** generic adjectives lacking constitutional load, the deleted `constitutive` wording, and vocabulary examples with no occurrence in the active inventory. Direct verification confirmed that the phantom terms did not contribute candidate lines or file-family assignments, so the **116 lines / 22 files** accounting is unchanged.
- **Bounded follow-up:** inventory hooks and alternative routes together, limited to current active text and without promotion-by-name.

## 5. Chapter-family distribution

| Directory / chapter family | Files | Candidate lines | Dominant families | Suggested bounded audit order | One report or split? |
| --- | ---: | ---: | --- | --- | --- |
| Book root | 3 | 8 | result-like, repository-current | Review only after chapter law | One short appendix to a synthesis |
| `01-grammar-and-standing` | 5 | 86 | result-like, producer, standing | First with Book II | One report with Book II, but section Book I internally |
| `02-acts-and-constraints` | 4 | 45 | result-like, producer, standing | First with Book I | One combined Books I–II report |
| `03-goals-and-advancement` | 6 | 143 | result-like, producer, consumer/demand | Next, before movement consumers | Split operator-ingress from the other five chapters within one PR or into two if clause inventory grows |
| `04-inquiry-and-examination` | 3 | 26 | result-like, producer, standing | After Book III | One report with Book III only if operator ingress is separately bounded |
| `05-evidence-and-knowledge` | 4 | 78 | result-like, producer, standing/consumer | After Books I–IV | One report, sectioning Fact/testimony separately |
| `06-state-and-projection` | 4 | 28 | result-like, producer, repeated formula | With Book V after its standing vocabulary is reviewed | One combined Books V–VI report |
| `08-authority-communication-and-stopping` | 5 | 64 | result-like, producer, consumer | After earlier standing and demand work | One report, with representation/emission as its own section |

`03-goals-and-advancement` has the highest density at **23.8 candidate lines per active file** as well as the highest absolute count. Density is review workload, not defect density.

## 6. Repeated-formula map

Only high-frequency formula families are mapped; no duplicate-propagation disposition is made.

| Formula family | Number of files | Locations | Exact or paraphrased | Apparent canonical owner found? | Follow-up needed |
| --- | ---: | --- | --- | --- | --- |
| report-local formula family: “does not by itself establish” / “does not automatically establish” | 19 | Books I–VIII, densest in `constitutional-kinds-and-artifact-standing.md` and operator-ingress | Both | unclear | Compare local negated inferences after district audits. |
| report-local formula family: “must preserve” plus bounded coordinates/limits | 15 | Books I, III, V, VI, VIII | Paraphrased | unclear | Determine whether local coordinate lists are restatement or distinct law. |
| report-local formula family: name/shape/adjacency/recurrence is not authority or standing | 12 | Books I, II, V, VI, VIII | Paraphrased | yes | Treat Book I as apparent orientation only; verify each local use. |
| report-local formula family: production/performance is distinct from result standing | 11 | Books I–III, V, VI, VIII | Paraphrased | unclear | Review producer/result boundaries by district. |
| report-local formula family: Unknown/conflict must remain preserved rather than strengthened | 10 | Books I, III–VI, VIII | Paraphrased | unclear | Compare evidence and consumer boundaries after Book V audit. |

An apparent owner marked “yes” is not a completed constitutional disposition.

## 7. Repository-current wording map

| File and section | Short excerpt | Why it may be repository-relative | Possible lawful constitutional reading | Follow-up priority |
| --- | --- | --- | --- | --- |
| `book_of_seed/README.md` — Status | “Existing implementation and tests are evidence of current practice” | Explicitly describes present evidence | A durable authority-boundary instruction | low |
| `book_of_seed/README.md` — Book structure | “current repository does not safely support” | Unresolved status can change with repository evidence | A conservative rule for maintaining unresolved questions | low |
| `01-grammar-and-standing/constructors-and-production-authority.md` — Constitutional rule | “In the current repository this boundary is often a Python function or method” | Names current language/realization shape | A non-exclusive illustration of producer realization | medium |
| `05-evidence-and-knowledge/testimony-and-established-fact.md` — Observation-to-Fact boundary | “The current repository compresses ... in `ObservationIngestor`” | Names current class and compression | Attributed implementation testimony expressly limited from universal law | high |
| `06-state-and-projection/projection-and-current-state.md` — Constitutional rule | “The current implementation named `FactView` exposes ...” | Names current implementation surface and prior PR | A bounded contrast between inventory testimony and constitutional View standing | high |

Every row in this table was reverified against the exact current-main active Book inventory during the vocabulary-hook correction.

## 8. Alternative-route map

This is the bounded set of recurring route shapes, not every line containing “or.”

| File and section | Short excerpt | Alternative subjects or routes | Existing definition found in active Book? | Follow-up priority |
| --- | --- | --- | --- | --- |
| `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` — Applicability | “may determine applicability ... or may validate and consume applicability standing” | Act-local determination vs separately assigned occurrence | yes | high |
| Same — Alternative proposed inputs | “determine or consume applicability standing” | Direct producer vs consuming prior standing | yes | high |
| `01-grammar-and-standing/external-and-constitutional-grammar.md` — Translation | “until a separate bounded warrant is established” | Attributed source grammar vs separately warranted Seed claim | yes | medium |
| `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md` — Consumer uptake | accept, narrow, refuse, or locally strengthen | Multiple consumer-local acts | yes | high |

Four prior report-local paraphrase rows—constraint evaluation/refusal/non-performance, current Demand evidence versus a later establishing occurrence, current versus another inquiry examiner, and direct establishment versus consumption in recording—were deleted because direct reading did not support the stated route in the stated active file. Those narrative rows were not source candidate-line assignments, and this targeted verification found no associated false candidate line or file-family assignment requiring downstream recounting.

Every row in this table was reverified against the exact current-main active Book inventory during the vocabulary-hook correction.

No Git-history provenance analysis was used.

## 9. Vocabulary-hook map

### Vocabulary-hook verification correction

PR 2193's vocabulary-hook map included two phrases that direct current-main verification did not find anywhere in the active 34-file Book inventory:

- `selection testimony`
- `trigger` / `triggered`

Those rows were prompt-, history-, or analyst-context residue, not active-current Book evidence. This correction reverified every vocabulary-hook row against the exact active inventory. Terms absent from current active text were deleted rather than preserved as active candidates. The same verification also found no active occurrence supporting the report-local `activation condition` family, so that row was deleted rather than replaced with a synonym. These were report defects, not constitutional defects or deleted Book law; the repository evidence does not identify which bounded alternative produced the residue.

| Exact active phrase or report-local family | Exact active locations | Current grammatical use | Verification status | Why later promotion may be plausible | Established owner found? | Follow-up priority |
| ------------------------------------------ | ---------------------- | ----------------------- | ------------------- | ------------------------------------ | ------------------------ | ------------------ |
| Exact active phrase: `readiness` | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` — Alternative proposed inputs; `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md` — Readiness decomposition correction 001; `book_of_seed/03-goals-and-advancement/selection-and-authorization.md` — Authorization; `book_of_seed/06-state-and-projection/projection-and-current-state.md` — Constitutional rule; `book_of_seed/08-authority-communication-and-stopping/authority-scope.md` — sufficiency/admission and authorization boundaries | A denied inferred standing, decomposed condition, or explicitly bounded evidence contribution | confirmed by direct current-main search | The result-like noun could be mistaken for a kind or scalar permission. | unclear | high |
| Exact active phrase: `conditional input applicability` | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` — Alternative proposed inputs | Qualified applicability condition in a negative non-establishment rule | confirmed by direct current-main search | The compact phrase could be promoted as a producer or result identity. | yes | medium |
| Exact active phrase: `automatic correction authority` | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md` — Fidelity | An authority inference that a Fidelity finding explicitly must not become | confirmed by direct current-main search | The adjective-noun compound resembles an authority kind despite its negative use. | no | low |
| Exact active phrase: `shared purpose` | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` — Multiplicity, collections, and higher-order standing | One stronger collective assertion that co-presence does not establish | corrected after direct current-main search | The collective phrase could encourage promotion by recurrence, although `shared state` has no active occurrence. | unclear | medium |
| report-local analytical family; exact active phrases include `input-set sufficiency`, `resource sufficiency`, `sufficiency and lawful stopping conditions`, `evidence sufficiency`, and `a sufficiency ... finding`; the active adjective is `sufficient` | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` — Alternative proposed inputs; `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md` — Non-examples and Readiness decomposition correction 001; `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md` — Selection artifacts; `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md` — Frontier identity and testimony support; `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md` — opening question; `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md` — Preservation; `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md` — Fact standing, operational baselines, and Remembering; `book_of_seed/08-authority-communication-and-stopping/authority-scope.md` — sufficiency/admission boundary; `book_of_seed/concordance.md` — baseline transition, stopping, and Remembering entries | Several distinct threshold, evidence, input-set, resource, stopping, and support uses, grouped here only for later review | report-local analytical family grounded in listed exact phrases | Result-like noun uses could be mistaken for independently produced standing; the grouping itself is not an active constitutional subject. | unclear | high |

The final active “constitutive warrant” wording was removed by commit `451b99f` before this inventory and is outside the current candidate set. Neither `constitutive warrant` nor `constitutive convention` remains in the 34-file active Book inventory, and neither is listed as an active hook. The required broad `git grep` over all of `book_of_seed/` returned two `constitutive warrant` matches, both in excluded historical reports (`atx_heading_evidence_born_competency_road_recovery_001.md:563` and `constrained_movement_sensing_gap_capability_learning_correction_001.md:66`); it returned no `constitutive convention` match.

## 10. Proposed bounded follow-up reports

| Priority | Proposed report | Exact Book scope | Candidate families examined | Why this scope is recoverable |
| ---: | --- | --- | --- | --- |
| 1 | Active vocabulary-hook and alternative-route audit | The active locations listed in sections 8–9 only | 9, 10 | Smallest cross-cutting set; current text only; no provenance work. |
| 2 | Books I–II responsibility and standing audit | `01-grammar-and-standing/*.md`; `02-acts-and-constraints/*.md` | 1–5, 8 | Establishes grammar before downstream districts; 131 mapped lines. |
| 3 | Books III–IV goals, demand, ingress, and inquiry audit | `03-goals-and-advancement/*.md`; `04-inquiry-and-examination/*.md`, with operator-ingress as a separate section | 1–6, 9 | Bounded chapter families; isolates the 78-line high-density chapter. |
| 4 | Books V–VI evidence, knowledge, state, and projection audit | `05-evidence-and-knowledge/*.md`; `06-state-and-projection/*.md` | 1–7, 9 | Evidence standing can be examined before projection consumption; 106 mapped lines. |
| 5 | Book VIII authority, representation, communication, and stopping audit | `08-authority-communication-and-stopping/*.md` | 1–6, 9 | One exact district; representation/emission can remain a distinct section. |
| 6 | Cross-Book repeated-formula synthesis | Only formulas retained by reports 2–5 plus the active root files | 8 | Defers recurrence judgment until local context exists and avoids a whole-Book clause ledger. |

No proposed report recommends wording or another all-file clause-level disposition.

## 11. Direct answers

1. **Was every active Book Markdown file inspected?** Yes—all 34.
2. **How many active files contain at least one material candidate?** 26.
3. **Which candidate family is most frequent?** Result-like subject, with 415 deduplicated candidate lines.
4. **Which Book directory has the highest candidate density?** `03-goals-and-advancement`, at 23.8 candidate lines per file.
5. **Which files have the highest direct-review priority?** `constitutional-kinds-and-artifact-standing.md`; `lenses-views-and-roads.md`; `selection-artifacts-and-selection-acts.md`; `construction-and-establishment.md`; `demands-and-opened-movement.md`; `operator-ingress-common-grammar-prerequisite.md`; `testimony-and-established-fact.md`; and `representation-emission-and-consumer-boundaries.md`.
6. **Are passive forms automatically defects?** No.
7. **Does recurrence establish authority?** No.
8. **Does the current active Book still contain `constitutive warrant` or `constitutive convention`?** No. The required broad grep returned two historical-report matches, but neither belongs to the active 34-file inventory; it returned no `constitutive convention` match.
9. **Did this mapping PR determine any clause to be unsupported?** No.
10. **Does this mapping warrant a whole-Book amendment?** No.
11. **What is the smallest recoverable next report?** **Active vocabulary-hook and alternative-route audit**, limited to the active locations in sections 8–9.
12. **Does this mapping establish runtime implementation demand?** No.

## 12. Final map disposition

```text
complete active-file coverage:
yes

candidate map complete for this method:
yes

constitutional defect dispositions:
none in this report

Book amendments warranted by this report alone:
none

runtime implementation warrant:
none

next bounded report:
Active vocabulary-hook and alternative-route audit
```

### Vocabulary-hook correction disposition

```text
vocabulary-hook rows reverified:
8

confirmed rows:
3

corrected rows:
2

deleted phantom rows:
3 — selection testimony; trigger / triggered; activation condition family

repository-current rows reverified:
5

alternative-route rows reverified:
8

constitutional defect dispositions added:
none

Book amendments warranted by this correction:
none

runtime implementation warrant:
none
```
