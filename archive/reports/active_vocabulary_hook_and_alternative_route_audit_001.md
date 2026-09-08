# Active Vocabulary Hook and Alternative Route Audit 001

## 1. Executive disposition

This report-only Phase 2 recovery consumes the corrected whole-Book map from PRs 2193 and 2194. It examines exactly five verified vocabulary-hook rows, decomposes the report-local sufficiency grouping into **18 materially distinct active uses**, and examines exactly four verified alternative-route rows. Route 4 is shown as four treatment subrows so that its listed treatments do not disappear into one conclusion.

The 30 classified audit units are distributed as follows: **A: 16; B: 12; C: 0; D: 0; E: 1; F: 1; G: 0**. Twenty-eight units are recommended to be retained, one phrase is recommended for a bounded clarification, one unnecessary vocabulary hook is recommended for deletion, and none requires narrower recovery before an amendment. These counts treat the sufficiency analytical grouping as one E unit, each of its 18 exact uses as its own unit, Routes 1–3 as one unit each, and Route 4's four treatments as four units.

The audit warrants two optional, independent Book amendment slices: clarify the claim-appropriate responsibility behind `separate bounded warrant`, and delete `automatic correction authority` from a negative enumeration whose surrounding exact prohibitions already carry the boundary. Neither is an emergency correctness repair. **No runtime implementation is warranted.**

## 2. Method and consumed evidence

### Authority and evidence order

The order used was:

1. current active Book text as constitutional authority;
2. reachable production as current implementation occurrence evidence;
3. tests as canonical-text and implementation testimony;
4. `whole_book_active_responsibility_lint_map_001.md` as corrected candidate-map testimony;
5. historical reports as attributed recovery testimony;
6. Git history as provenance testimony; and
7. names, recurrence, examples, analyst groupings, and stylistic plausibility as no authority by identity.

Implementation was not needed to resolve these textual boundaries and was not allowed to create Book law. No implementation claim in this report depends on a runtime name.

### Active material inspected

The audit read the corrected map's sections 8 and 9 and inspected the complete relevant paragraphs in:

- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`;
- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`;
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`;
- `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md`;
- `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md`;
- `book_of_seed/03-goals-and-advancement/selection-and-authorization.md`;
- `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md`;
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`;
- `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`;
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`;
- `book_of_seed/06-state-and-projection/projection-and-current-state.md`;
- `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`;
- `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md`; and
- `book_of_seed/concordance.md`.

The direct active inventory is reproducible with:

```bash
rg -ni --glob '*.md' '\b(readiness|conditional input applicability|automatic correction authority|shared purpose|sufficien(t|cy|cies)|locally strengthen|separate bounded warrant|determine applicability|determine or consume applicability standing)\b' \
  book_of_seed/01-grammar-and-standing \
  book_of_seed/02-acts-and-constraints \
  book_of_seed/03-goals-and-advancement \
  book_of_seed/04-inquiry-and-examination \
  book_of_seed/05-evidence-and-knowledge \
  book_of_seed/06-state-and-projection \
  book_of_seed/08-authority-communication-and-stopping \
  book_of_seed/concordance.md
rg -n '^## (8|9)\.|readiness|conditional input applicability|automatic correction authority|shared purpose|sufficien|separate bounded warrant|locally strengthen' \
  whole_book_active_responsibility_lint_map_001.md
```

Search results were not classified in isolation. Each match was read with its heading, full paragraph, neighboring negative distinctions, responsible subject, and referenced consumer boundary. Exact uses sharing a word stem were separated whenever their subject, claim, act, examiner, or consumer differed. A category was assigned only after asking whether the phrase itself performed constitutional work and whether its coordinates were supplied locally or by the controlling active grammar.

Limited Git history was used only for the sole F disposition:

```bash
git log --follow --format='%h %ad %s' --date=short -- \
  book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md
git blame -L 15,15 -- \
  book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md
git grep -n -i 'separate bounded warrant' 9fa3503 -- '*.md'
git grep -n -i 'Unknown or unavailable provenance' 9fa3503 -- '*.md'
```

The audit excludes every map row outside corrected sections 8 and 9, removed phantom rows, inactive or merely historical candidates, and all amendment drafting or implementation work. It does not modify the consumed map or any active Book file. The “sufficiency family” is only a report-local search and decomposition device: a common stem cannot turn claim support, resources, stopping conditions, preservation thresholds, and negative authority comparisons into one constitutional subject.

## 3. Vocabulary disposition ledger

| Exact phrase | Exact location | Current grammatical role | Responsibility or owner | Assertion or result | Consumer and purpose | Category A–G | Promotion risk | Disposition |
| ------------ | -------------- | ------------------------ | ----------------------- | ------------------- | -------------------- | ------------ | -------------- | ----------- |
| `readiness` | `01/.../constitutional-kinds-and-artifact-standing.md:45`; `02/.../constraints-policy-and-preconditions.md:45,47`; `03/.../selection-and-authorization.md:41`; `06/.../projection-and-current-state.md:15`; `08/.../authority-scope.md:19,42` | A denied unassigned standing, denied complete/scalar compression, and bounded possible evidence contribution; not one positive result | Exact local condition examiner and later consumer; authorization remains owned by its authority boundary | Local findings carry only their exact conditions; none establishes complete permission or authority | Each exact act/authorization/state consumer, to preserve local coordinates and Unknowns | B | Medium: noun recurrence looks result-like, but every operative use narrows or denies inference | retain as ordinary negative wording |
| `conditional input applicability` | `01/.../constitutional-kinds-and-artifact-standing.md:49` | Qualified ordinary applicability in a non-establishment rule | Exact act owner or explicitly assigned applicability-producing occurrence, when such an input relation actually exists | Applicability, even if conditional, does not establish current production demand or its listed prerequisites | Exact downstream act owner deciding lawful reliance | B | Medium: compact wording can look like a persistent family | retain as ordinary negative wording |
| `automatic correction authority` | `01/.../external-and-constitutional-grammar.md:25` | One forbidden inference in the negative authority of a Fidelity finding | No producer is assigned because the phrase names what the finding must not become | Fidelity does not authorize correction | Fidelity consumer preserving comparison limits | B | Medium: an authority-shaped noun is reusable despite being negated; “mutation authority” and the exact Fidelity boundary already carry the useful prohibition | delete unnecessary vocabulary hook |
| `shared purpose` | `01/.../constitutional-kinds-and-artifact-standing.md:25` | Stronger collective relation expressly not inferred from co-presence | A bounded relation-establishment occurrence, only if later positively claimed; none is created here | Co-presence does not establish a shared-purpose relation | Any consumer tempted to infer collective identity or relation | B | Low: the forbidden inference is precise and immediately requires a bounded subject and warrant | retain as ordinary negative wording |
| report-local sufficiency analytical family | Corrected map section 9; exact uses decomposed below | Audit grouping only, not active grammar | This report only | No collective result | Analyst navigation only | E | High if the grouping were promoted by stem identity | retain |

`readiness` does not have one disposition per spelling occurrence: the alternative-input paragraph denies an unassigned result, the constraints chapter expressly denies scalar compression, projection denies an implementation-readiness inference, and authority chapters deny authority by identity. None positively establishes a general standing. The exact local conditions—not the compression word—have their ordinary producers and consumers.

## 4. Sufficiency-use decomposition

The following 18 rows are materially distinct by subject or constitutional purpose. Concordance rows are retained as navigation wording, not counted as additional laws.

| Exact phrase | Subject relative to which sufficiency is judged | Examiner or producer | Evidence/input | Result | Consumer | Free-floating standing created? | Category | Disposition |
| ------------ | ----------------------------------------------- | -------------------- | -------------- | ------ | -------- | ------------------------------- | -------- | ----------- |
| `input-set sufficiency` | Proposed inputs for one exact downstream act | No owner is assigned; the clause denies creation | Availability or proposed-input status | No set-level standing | Exact act owner | No; expressly denied | B | retain as ordinary negative wording |
| `sufficient execution authority` | Authority to execute after schema validation | No producer; this is a non-example | Passing schema validation | No execution authority | Would-be act performer | No; expressly denied | B | retain as ordinary negative wording |
| `resource sufficiency` | Resources for the exact contemplated act and conditions | Examiner of the exact resource condition; identity is local and otherwise Unknown | Resource evidence in the examined scope and time | One condition finding, not permission | Exact act/condition consumer | No | B | retain |
| `may be sufficient with selected registered names plus unsupported-key uncertainty` | Representation selection artifact preservation for its intended consumer | Responsible representation selector | Selected registered names and explicit unsupported-key uncertainty | Enough preservation for that selector-specific representation assertion | Intended representation consumer | No; expressly selector-specific | B | retain |
| `sufficiency and lawful stopping conditions` | Identity coordinates of one bounded inquiry frontier | Responsible frontier-establishment boundary | Exact inquiry demand/uncertainty, scope, conditions, Unknowns and limits | Bounded frontier identity | Inquiry/movement consumer | No | A | retain |
| `warrant sufficient for the exact claim, inquiry demand, frontier boundary, and reliance purpose` | Positive testimony support for four exact claim-relative dimensions | Responsible consuming examiner | Preserved testimony, provenance, currentness, conflicts and claim-local warrant | Positive support only for the exact bounded claim | Frontier consumer | No; universality is expressly rejected | A | retain |
| `evidence and provenance are sufficient to explain why Seed holds a claim` | Explanation of one held claim at one time | Responsible explanation/examination boundary; exact identity is question-local | Claim-appropriate evidence and provenance | A bounded explanation answer or Unknown | Explanation requester/consumer | No | B | retain |
| `dimensions were absent or insufficient for answer recovery` | Recovery of required provenance dimensions from one examined corpus/surface | Bounded inquiry/explanation examiner | Identified material and required dimensions | Bounded negative evidentiary finding | Later inquiry consumer | No | B | retain |
| `preserve sufficient evidence or compressed standing to retain its materially sufficient understanding` | Preservation of operational understanding | Responsible preservation decision, distinct from establishment | Evidence or already established compressed standing, materiality and rebuildability | Recoverable materially bounded understanding | Later recovery/explanation consumer | No | A | retain |
| `preserve sufficient measurement and comparison context` | Challenge to prior operational understanding | Responsible preservation boundary | Measurement, applicable comparison context and material-deviation standing | Preserved challenge, not establishment by recording | Later comparison/recovery consumer | No | A | retain |
| `source or producer authority sufficient for the claim strength` | Fact standing for one proposition and strength | Fact establishment or later consumption boundary | Claim-appropriate support, source authority, scope and conflicts | Bounded Fact standing | Exact Fact consumer | No | A | retain |
| `consumes sufficient measurement testimony` | Establishment of one operational baseline under declared conditions | Baseline-establishment occurrence | Measurements, authorized observations, method, scope, conflicts and uncertainty | Bounded operational baseline | Later comparison consumer | No | A | retain |
| `sufficiently fresh` | Present freshness of latest selected support | Projection and consumer-local judgment | Observed support time plus applicable freshness/expiry rule | At most current-support eligibility; the clause denies freshness by latestness alone | Present-facing Fact consumer | No | B | retain as ordinary negative wording |
| `preservation of sufficient testimony or standing for later lawful recovery` / `preserve sufficient testimony or standing` | Recoverability across time | Remembering/preservation responsibility | Testimony or already established standing adequate for later recovery | Remembering, not current projection or later reliance | Later recovery, revision, explanation, or movement consumer | No | A | retain |
| `sufficiently established standing` | Later adaptive reliance for an exact Demand or Gap | Prior standing-establishment boundary; later consumer owns reliance | Revised gap, capability, or learned standing with provenance and warrant | Consumer-local constrained reliance | Inquiry, selection, or movement consumer | No | A | retain |
| `A sufficiency ... finding may let a supported subject participate` | Participation in the next bounded constitutional posture | Finding's evidence owner; exact finding kind remains local | Evidence, owner, purpose, authority, confidence, limits and Unknowns | Bounded participation only, not truth or reusable permission | Next-posture consumer | No | A | retain |
| `evidence sufficiency` | Concordance navigation for baseline transition | No new producer in the concordance; controlling baseline text supplies establishment | Claim-appropriate transition evidence | Index term pointing to transition support | Concordance reader | No | B | retain |
| `exhaustion, sufficiency, completion` | Concordance navigation for stopping | No new producer in the concordance; stopping chapter preserves the responsible consumer/occurrence question | Exact evidenced stopping conditions remain unresolved in controlling text | Index neighbor, not one stopping standing | Concordance reader | No | B | retain |

No active clause in scope recreates an independently sufficient input set, unowned set-level sufficiency, universal readiness, or universal evidence-sufficiency standing. The one set-level phrase expressly denies that result. The generic-looking finding in `authority-scope.md` is bounded by its supported subject, evidence, owner, purpose, authority, negative authority, confidence, and Unknowns; it does not grant a reusable kind by itself.

The required distinctions therefore hold: sufficiency for one exact act is not a self-sufficient set; evidence for claim C is not universal evidence standing; resources do not confer authority; one coordinate does not establish complete readiness; and a finding is not performance.

## 5. Alternative-route ledger

| Route | Exact clause | Route A | Route B | Producer(s) | Result(s) | Consumer(s) | Both routes established? | Category | Disposition |
| ----- | ------------ | ------- | ------- | ----------- | --------- | ----------- | ------------------------ | -------- | ----------- |
| 1 | `may determine applicability within the same bounded occurrence, or may validate and consume applicability standing established by an explicitly assigned responsible occurrence` | Exact act owner determines exact input-to-act applicability in its own occurrence | Explicitly assigned occurrence establishes it; act owner validates and consumes it | Act owner; or assigned applicability producer followed by act owner | Same exact relation standing, not two constitutional kinds | Exact downstream act owner | Yes. Assignment, exact relation, validation, consumption, and prohibition on a universal service are explicit. `validate and consume` states two recoverable consumer responsibilities that may share the owner occurrence; it does not establish mandatory separate occurrences. | A | retain |
| 2 | `must determine or consume applicability standing ... and validate or consume whatever standing, warrant, admission, authority, scope, provenance, or other relation ... requires` | Act owner determines the exact proposed-input applicability and validates other required coordinates | Act owner consumes already established applicability and consumes or validates other independently required coordinates | Exact act owner plus only those upstream producers established for locally required coordinates | Proposed input is lawfully usable only within exact local relations; no universal coordinate bundle | Exact act owner | Yes, as Route 1 restated and applied to proposed alternatives. The additional list is not a new applicability road. | A | retain |
| 3 | `Unknown or unavailable provenance limits reliance until a separate bounded warrant is established` | Preserve limited reliance/Unknown provenance | Reliance may proceed under some later bounded warrant | Current consumer preserves the limit; later producer is not assigned | Limited reliance; later claim-appropriate reliance not specified | Consumer of translated/external material | No. The first side is established; the second lacks the exact claim/relation and responsible establishment occurrence. | F | clarify through bounded amendment |
| 4a — accept | `consumer ... may accept ... material only through its own evidence and authority boundary` | Accept the producer's one bounded assertion for the declared local purpose | Not applicable | Responsible downstream consumer | Consumer-local adoption/reliance for that bounded assertion | Same downstream consumer and its later dependents | Yes as one result of the established consumer-local uptake responsibility | A | retain |
| 4b — narrow | Same clause | Narrow the material/assertion for local use while preserving source limits | Not applicable | Responsible downstream consumer | Narrower consumer-local assertion or use; upstream artifact and standing unchanged | Same downstream consumer | Yes | A | retain |
| 4c — refuse | Same clause | Decline consumer-local uptake or reliance without disproving the source | Not applicable | Responsible downstream consumer | Bounded refusal/Unknown preservation | Same downstream consumer | Yes | A | retain |
| 4d — locally strengthen | Same clause | Establish a stronger consumer-local assertion only from the consumer's own evidence and authority | Not applicable | Responsible downstream consumer | New stronger local assertion bounded to exact subject, purpose, evidence, scope, authority and preserved upstream limits | Same consumer and only its declared downstream boundary | Yes. The chapter's general uptake rule supplies the missing-looking constraint: any resulting standing is produced by the consumer-local occurrence and remains locally bounded. | A | retain |

Routes 1 and 2 are one constitutional alternative at different levels of application, not two independent laws and not support multiplied by repetition. Route 2 additionally reminds the proposed-input consumer to handle every other relation its *exact use* actually requires. It does not broaden Route 1 into an all-coordinate service.

Route 4 is not four constitutional kinds. It is four ordinary bounded treatments/result forms available within one already-assigned consumer-local responsibility. Accepting one assertion does not accept all producer assertions; narrowing does not mutate the source; refusal does not disprove it; and local strengthening cannot inflate upstream standing because any stronger result must be newly supported by the consumer's own evidence and authority and remains consumer-local.

## 6. Responsibility-coordinate findings

Only Route 3 is F; there are no G dispositions.

```text
responsibility: a later claim-appropriate warrant-establishment responsibility
act: establish the warrant that would permit a stated reliance despite Unknown or unavailable provenance
subject: the exact external or translated claim/relation to be relied upon
purpose: the exact proposed reliance
inputs: attributed material, known provenance and explicit provenance Unknowns, translation boundary, evidence, uncertainty, and authority limits
warrant/authority: claim-appropriate evidence and bounded authority; exact required basis remains unresolved
scope/locality: the exact external source, translated claim, consumer, purpose, and reliance boundary
result: bounded permission for the exact reliance, not provenance recovery or grammar adoption
consumer: the responsibility proposing to rely on the external or translated material
missing or unresolved coordinate: the clause does not identify the exact claim/relation being warranted or assign the responsible establishment occurrence
```

The appropriate repair must refer to a claim-appropriate responsible warrant without minting a named warrant family. It must preserve Unknown provenance rather than imply that a different warrant supplies the missing provenance.

### Bounded provenance review for Route 3

`git blame` places the complete clause at commit `9fa3503` on 2026-07-29, when `external-and-constitutional-grammar.md` entered the active Book in PR 2096, “Recover first post-representation ingress consumer.” The commit did include recovery testimony, and `constitutional_grammar_recoverability_survey_001.md` said sufficient promotion warrant remained unresolved while Unknown or unavailable provenance limited reliance. Exact-phrase search at that commit finds `separate bounded warrant` only in the new active clause, not in a report-local shorthand that later propagated. The file has no later modifying commit in `git log --follow`. Thus the route was introduced alongside recovery, inherited an explicitly unresolved warrant boundary, and did not gain apparent support through later repetition. This provenance explains the compression but does not authorize it.

## 7. Duplicate and propagation findings

1. **Routes 1 and 2:** one rule restated locally. Route 1 defines the owner/assigned-producer alternatives. Route 2 applies them to alternative proposed inputs and separately requires validation or consumption only for other relations the exact use requires. Their repetition is readability, not independent support.
2. **Sufficiency recurrence:** the repeated stem belongs to independent local subjects: proposed inputs, execution authority, resources, representation preservation, frontier identity, claim support, explanation recovery, operational preservation, Fact establishment, baseline establishment, currentness, Remembering, adaptive reliance, and next-posture participation. The only report-level abstraction is analytical.
3. **Readiness recurrence:** no single owner produces a general readiness result. One constraints paragraph explicitly denies scalar compression; the remaining uses deny an unassigned result, complete coverage, source truth, authority, or authorization by identity. Exact local condition producers remain controlling.
4. **Apparent authority:** no audited hook became authoritative through recurrence. Route 2 derives authority from its immediate act-owner grammar, not from restating Route 1. Route 3 did not recur at all. Concordance recurrence is navigation, not law creation.

## 8. Negative-language findings

- **`readiness`: retain.** It gains precision by naming the tempting compression that the Book forbids. Its uses consistently connect the word to negative identity or bounded-evidence rules. Deleting every occurrence would make it harder to reject implementation, constraint, or authorization compression, while the current text already prevents promotion.
- **`shared purpose`: retain.** This is the exact stronger collective inference likely to be drawn from co-presence. The sentence immediately requires its own bounded subject and warrant. The precision of the guardrail outweighs the small promotion risk.
- **`automatic correction authority`: delete in a bounded amendment.** Negative mention does not establish the authority, but this compound adds less precision than the neighboring prohibitions. A Fidelity finding's lack of mutation, implementation, external-effect, and authority transfer is already expressed by the paragraph and chapter. The phrase is therefore harmless current grammar but an avoidable reusable noun.
- **`conditional input applicability`: retain.** The adjective limits an applicability relation and the sentence's entire work is to deny that persistent/local applicability becomes current production demand. It does not name a result family.
- **Negative sufficiency uses: retain.** `input-set sufficiency` and `sufficient execution authority` precisely deny two dangerous identity inferences; nearby text supplies their scope and prevents promotion.

Negative enumeration is therefore neither automatically safe nor automatically disposable. The deciding question is whether naming the forbidden inference materially improves the boundary and whether immediate grammar prevents identity promotion.

## 9. Amendment recommendations

Two independent bounded amendments are warranted; they should not be combined merely to reduce PR count.

| Priority | Exact Book files | Finding consumed | Intended correction | What must remain unchanged |
| -------- | ---------------- | ---------------- | ------------------- | -------------------------- |
| 1 | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md` | Route 3 F: later warrant route lacks exact warranted relation and assigned responsible occurrence | Replace only the compressed escape clause with claim-appropriate responsible-warrant wording tied to the exact proposed reliance; preserve provenance Unknown | Attribution, translation scope, reliance limitation, uncertainty, authority limits, and the rule that another warrant does not manufacture provenance or adopt external grammar |
| 2 | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md` | Negative hook B: `automatic correction authority` is redundant and authority-shaped | Remove only this item from the Fidelity negative list after confirming the surrounding boundary still expressly denies correction/mutation authority | Fidelity producer, comparison inputs, qualitative results, all other negative authority, consumer preservation boundary, and no runtime change |

No amendment is recommended for `readiness`, `conditional input applicability`, `shared purpose`, any exact sufficiency use, Routes 1–2, or Route 4. No whole-Book rewrite or central sufficiency/readiness subject is warranted.

## 10. Direct answers

1. **Is `readiness` an established constitutional standing?** No. In this scope it is denied compression, denied inference, or a label for a bounded possible finding/evidence contribution—not an independently established standing.
2. **Does the Book safely decompose readiness into exact local conditions?** Yes. The constraints text lists distinct local coordinates, requires condition testimony to retain producer/examiner boundaries, and preserves unevidenced coordinates as Unknown; other chapters deny authority and state inferences.
3. **Does `conditional input applicability` name a distinct constitutional result?** No. It qualifies an input-to-act applicability relation while denying that the relation creates production demand.
4. **Does `automatic correction authority` perform necessary negative-boundary work?** No. It is harmlessly negative today, but the exact Fidelity and mutation/authority boundaries make this compound unnecessary.
5. **Does `shared purpose` require a responsible relation-establishment occurrence when positively claimed?** Yes. Co-presence cannot establish it; a positive claim requires its own bounded subject, warrant, evidence, scope, result, and responsible occurrence.
6. **Does the active Book contain free-floating sufficiency standing?** No.
7. **Does any active sufficiency clause recreate independently sufficient input-set grammar?** No. The only exact set-level use expressly denies an unassigned result.
8. **Are Routes 1 and 2 constitutionally distinct?** No. Route 2 is Route 1 applied locally to proposed alternatives, with reminders about independently required exact relations.
9. **Is the separately established applicability route sufficiently assigned?** Yes. It requires an explicitly assigned responsible occurrence for the exact downstream act, followed by validation and consumption by the act owner; no universal service is created. The identity of a concrete assigned producer remains occurrence-local until an exact Book assignment exists.
10. **Does `separate bounded warrant` create an undefined warrant family?** It does not establish a named family, but it does open an insufficiently assigned alternative because the exact warranted claim/relation and producer are absent. Clarification is warranted.
11. **Are accept, narrow, refuse, and locally strengthen distinct acts or bounded consumer treatments?** They are bounded treatment/result descriptions within one consumer-local uptake responsibility, not four sibling constitutional kinds. Their claims remain independently recoverable.
12. **Is `locally strengthen` sufficiently constrained against unsupported standing inflation?** Yes. The controlling paragraph requires the consumer's own evidence and authority; the chapter requires any resulting assertion to be produced in and bounded to that consumer-local occurrence. Upstream standing is unchanged.
13. **Which phrases should be deleted?** Only `automatic correction authority`, as an optional bounded removal from the negative enumeration.
14. **Which phrases should be clarified?** Only `separate bounded warrant`, to identify a claim-appropriate responsible warrant for the exact proposed reliance without creating a family or repairing missing provenance by assertion.
15. **Which phrases should remain unchanged?** `readiness`; `conditional input applicability`; `shared purpose`; all exact sufficiency uses; both applicability-route clauses; and `accept`, `narrow`, `refuse`, and `locally strengthen`.
16. **What remains Unknown?** Concrete producers and consumers until an occurrence is instantiated; whether Route 1 validation and consumption share one act realization; the exact evidence and authority adequate for reliance despite provenance Unknown; whether deletion priority outweighs the precision preferences of a later amendment owner; and concrete local thresholds for every comparative sufficiency judgment.
17. **Does this audit warrant runtime implementation?** No.
18. **What is the smallest next Book amendment, if any?** Clarify only the final reliance clause of `01-grammar-and-standing/external-and-constitutional-grammar.md:15` so the later warrant is claim-appropriate, responsibly established, local to the exact reliance, and incapable of supplying missing provenance.

## 11. Preserved Unknowns

This audit intentionally preserves rather than fills:

- the exact producer of a concrete local condition, applicability relation, relation claim, sufficiency judgment, or later reliance warrant unless the Book assigns it;
- the exact consumer until a declared act and purpose instantiate the boundary;
- whether validation and consumption are separate acts in every realization or two recoverable responsibilities sharing one bounded occurrence;
- occurrence sharing beyond the explicit permission that one bounded occurrence may preserve independently recoverable claims;
- concrete evidence and authority adequate for reliance when provenance is Unknown;
- scope and result identities of future positive `shared purpose` claims;
- provenance not supplied by the active clause or attributed source;
- whether local recurrence serves readability or propagation outside the specific duplicate findings above;
- whether a later amendment owner judges the negative correction phrase necessary after reviewing the complete Fidelity guardrail;
- the relative amendment priority after this report; and
- every missing coordinate that current active text itself marks Unknown.

Unknown does not authorize a new producer, consumer, act, standing, service, or family.

## 12. Final disposition

```text
retain unchanged:
[conditional input applicability; shared purpose; all 18 exact sufficiency uses;
 Routes 1 and 2; accept; narrow; refuse; locally strengthen]

retain as ordinary negative wording:
[readiness]

clarify through bounded amendment:
[separate bounded warrant]

delete unnecessary vocabulary hooks:
[automatic correction authority]

recover before amendment:
[]

leave Unknown:
[]

Book amendment warrant:
[external-and-constitutional-grammar.md: claim-appropriate reliance warrant slice;
 external-and-constitutional-grammar.md: optional Fidelity negative-list deletion slice]

runtime implementation warrant:
none
```

The corrected PR 2193/2194 map supplied candidate testimony only. Removed phantom rows were not reintroduced, exact phrases were kept separate from analytical families, and no term acquired constitutional authority merely by being useful to this audit.
