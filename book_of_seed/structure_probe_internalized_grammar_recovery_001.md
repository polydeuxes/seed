# Structure Probe Internalized-Grammar Recovery 001

## 1. Scope and negative authority

This is one bounded, Book-first, report-only recovery against merged `main` at
`da953d4` (PR 1976). It examines the active Book, current implementation, and
focused tests. Earlier Structure Probe reports, unknown-grammar audits, and PRs
840, 841, 1625, 1633, 1975, and 1976 are locator testimony only. They neither
establish the claims below nor supply missing competency warrant.

This report does **not** declare the probe faithful or contaminated, change any
implementation, promote report vocabulary into Constitutional Grammar, infer
that literal semantic zero is possible, recommend a repair, or continue into
Prometheus, the Evidence Graph, confidence, goals, Questions, Answers,
execution, or presentation. `runtime-active` below means exercised by the
current implementation; it does not mean constitutionally established.

The governing distinctions recovered here are:

* **constitutional bootstrap candidate** — a capacity arguably required to
  preserve and boundedly examine attributed material without deciding its
  substrate meaning; it produces only examination-addressability or exact
  measurement testimony, never Fact, norm, authority, ontology, or semantic
  identity;
* **declared measurement convention** — an identified projection/comparison
  rule whose scope and losses can remain visible; declaration makes the
  operation inspectable, not universally applicable or neutral;
* **learned external grammar** — source-, substrate-, or domain-relative
  competency whose meaning, applicability, selection, and authority must be
  established from evidence; a compiled realization is not that standing; and
* **semantic strengthening** — a crossing from attributed material or
  measurement into meaning, ontology, norm, authority, completeness, defect,
  or other standing not warranted by that input.

## 2. Active Book clauses

The controlling Book witnesses say:

1. External grammar may be attributed and compared without becoming
   Constitutional Grammar. Addressability must preserve source role,
   provenance, grammar boundary, scope, uncertainty, and authority limits;
   lexical recurrence and repository convenience confer no native standing.
   A Fidelity finding requires a bounded constitutional comparison and must
   preserve witness, evidence, authority, loss, conflict, Unknowns, and stop.
2. A lens exposes supplied material under a declared method without changing
   source standing. Availability, applicability, admission, and consumption are
   distinct. A lens output is not evidence sufficiency and cannot manufacture
   dimensions absent from its inputs.
3. Read-only/non-mutating behavior proves side-effect limits, not absence of a
   constitutional occurrence. Artifact construction does not by itself prove a
   warranted act occurred.
4. Orientation or association is not movement; movement requires a separately
   warranted transition. Repetition and association are not causal or semantic
   establishment.
5. Testimony is attributed material, not Fact. Evidence, provenance,
   applicability, coherence, verification, producer occurrence, independent
   corroboration, and truth are separate standings. Multiple projections or
   occurrences from one source are not independent evidence.
6. Explanation exposes bases and conflicts but does not create upstream truth.
   Missing provenance remains Unknown; a bounded absence finding is not global
   absence.
7. Recording preserves an attributed assertion or already-established standing;
   it does not establish that standing. Diagnostic material stays local to its
   examination unless separately established.
8. A projection is a recoverable view shaped by declared scope and rules, not a
   constitutional source or current standing. Purpose-relative fidelity requires
   the consumer-relevant method, limits, loss, Unknowns, conflict, and refusal
   distinctions to remain recoverable.

These clauses warrant preservation, attribution, bounded exact comparison, and
honest refusal. They do not enumerate Python strings, lines, Markdown, regexes,
or thresholds as native primitives.

## 3. Central finding

The probe is **mixed**. Its strongest faithful core is the external-material
road: supplied text is rebound to a manifest artifact by a declared encoding
and SHA-256 check, then projected under named line/coordinate and surface-feature
conventions while preserving order, coordinates, exact line text, identities,
Unknown strings, and negative authority. That is a useful positive reference
for evidence-born competency because the transformation and its limits are
substantially visible.

It is not semantic zero. Encoding, Python's character model, `splitlines`,
whitespace blankness, and contiguous nonblank regions are compiled conventions.
The selected length features are frozen without feature-candidacy evidence.
The documentation road then compiles a partial Markdown/front-matter/link grammar,
an English architectural-relation grammar, a documentation ontology, and
consumer-local thresholds without recoverable constitutive competency evidence.

The **first exact strengthening** on the general road is
`content.strip() == "" -> ExternalMaterialProjectedLine.is_blank`: an exact
line slice is reclassified through Python whitespace grammar. It is honestly
bounded as mechanical and does not yet claim a paragraph. The first unmarked
ontology-strengthening on the documentation road is regex-matched `#` syntax
`-> DocumentationHeadingRecord`, followed immediately by headings `-> sections`
and first H1 `-> title_heading`. The first explicit normative classification is
`front_matter_present + heading_present -> structure_status="complete"`.

## 4. Exact current implementation topology

| Path | Exact current symbols and role | Occurrence |
|---|---|---|
| `seed_runtime/external_material_testimony_binding.py` | `ExternalMaterialManifest`, source/artifact/annotation records, requests, `validate_external_material_testimony_bindings()`; reference/span compatibility only | runtime-active, CLI-triggered, test-active |
| `seed_runtime/external_material_structural_projection.py` | `ExternalMaterialStructuralProjectionRequest`, `project_external_material_structure()`, `ExternalMaterialStructuralProjection`, `ExternalMaterialProjectedLine`, `ExternalMaterialProjectedNonblankRegion`; encoding/hash/count checks and line/region projection | runtime-active, CLI-triggered, projection-active, test-active |
| `seed_runtime/external_material_surface_feature_projection.py` | `ExternalMaterialSurfaceFeatureProjection`, `project_external_material_surface_features()`, `ExternalMaterialLineSurfaceFeature`, `ExternalMaterialRegionSurfaceFeature`; selected counts/sequences | runtime-active, CLI-triggered, projection-active, test-active |
| `seed_runtime/structure_observation.py` | `StructureObservationBoundary`, `STRUCTURE_OBSERVATION_BOUNDARY`, text and owner; shared negative-authority metadata | runtime-active, compatibility-tested |
| `seed_runtime/documentation_structure.py` | `observe_documentation_structure()`, `observe_markdown_document()`, records/reports, `_heading_outline()`, `_section_inventory()`, `_front_matter()`, `_code_block_observations()`, `_link_observations()`, `_architectural_relation_observations()`, `_build_recurrence_report()`, `_common_section_rows()`, `_structural_outlier_rows()` | runtime-active, CLI-triggered, test-active |

Class/function names demonstrate implementation organization, not constitutional
ownership. The external projection and documentation observer are adjacent
roads, not one demonstrated constitutional competency pipeline.

## 5. Layered Structure Probe topology

### Layer A — material binding

Supplied manifest records attribute source and artifact identities, locations,
reported metadata, counts, hashes, and Unknown strings. Binding validates exact
identifier membership, parent-source relation, expected hash, coordinate bounds,
and optional annotation span equality. Structural projection additionally
encodes supplied `exact_text` using the requested encoding, SHA-256 hashes the
bytes, and checks stored line/character counts.

Established: **representation compatibility** between this supplied Python
string, named encoding, resulting bytes/hash, and manifest artifact record;
identifier and span referential integrity. Still attributed or Unknown: source
authority, source truth, whether the manifest accurately describes an external
artifact, whether the hash is a universal artifact identity, decoding provenance,
encoding applicability, character model applicability, testimony support,
annotation correctness, and independence.

### Layer B — mechanical structural projection

`exact_text.splitlines(keepends=True)` creates ordered physical-line slices;
zero-based half-open Python-string offsets and one-based line numbers locate
them. Terminator detection recognizes `\r\n`, final `\n`, or `\r` for content
removal, while `splitlines` may recognize a broader set of Unicode boundaries.
`content.strip() == ""` declares blankness; maximal adjacent nonblank lines form
regions. Exact line slices, order, coordinates, case, punctuation, whitespace,
and newline distinctions are preserved.

This establishes recurrence-addressable representation units **under those
conventions only**. It does not establish lines as semantic units, whitespace as
semantically empty, regions as paragraphs/sections, textual applicability, or
cross-encoding identity.

### Layer C — surface-feature projection

For every selected line: raw Python-character count, content-character count,
terminator-character count, blank flag, terminator flag, line number/id. For
every selected region: line count, ordered raw/content length sequences, totals,
region/line ids. Raw text is deliberately erased from this artifact but remains
reopenable from the upstream projection. Feature convention and upstream
structural identity are emitted.

The code contains no corpus evidence, selection record, consumer purpose, or
candidate comparison establishing why length, blankness, and terminators matter.
Thus measurement formation is declared; feature candidacy is **compressed**.

### Layer D — documentation grammar and recurrence

Top-level `docs/*.md` paths are decoded as UTF-8 and parsed by compiled regexes
and procedures into front matter, headings, title, sections/hierarchy/emptiness,
fences/languages, links/classes/brokenness, and architectural relations. Exact
values are counted, bucketed, labeled rare/common, compared for missing common
sections, and combined into outlier signals, issue score, and structure status.
This layer changes source scope (a repository corpus), source grammar (partial
Markdown/YAML/path/English), authority (hard-coded policy), and standing
(semantic-looking and normative labels).

## 6. Constitutional bootstrap-primitive candidates

| Candidate | Constitutional work / output standing | Avoided import and authority limit | Removal loss / classification |
|---|---|---|---|
| Preserve attributed material | permits reopening and comparison; attributed material only | avoids interpreting content; source/scope/authority remain attached | without it fidelity cannot be checked; **constitutional bootstrap candidate**, Book-evidenced in principle |
| Bind to scoped identity plus digest testimony | detects replacement within a declared byte/encoding procedure; compatibility standing | avoids truth/authority; digest algorithm and byte realization are conventions | without it same supplied artifact cannot be reliably reopened; binding is candidate, SHA-256/hash universality is not |
| Preserve order and coordinates | permits exact source-local addressability | avoids semantic sequence; coordinate system declared | without it arrangement and testimony spans are lost; order preservation is candidate, coordinate model convention |
| Exact representation comparison | establishes same selected representation value under E | avoids semantic identity if refusal retained | without it exact recurrence cannot be computed; comparison capacity candidate, selected E convention |
| Count supplied occurrences | establishes cardinality in bounded S | avoids significance/commonness | without it no exact distribution; arithmetic capacity candidate, occurrence unit and scope conventions |
| Group under declared E | establishes equivalence classes under E | avoids universal identity only if E remains visible | without it recurrence classes vanish; grouping capacity candidate, every E a convention/grammar |
| Preserve/report Unknown or inability | prevents silent invention and supports refusal | avoids default applicability/meaning | without it absence becomes resolution; Book-evidenced bootstrap candidate |
| Stable ids | navigation/reopening convenience | does not itself establish artifact identity or standing | removable without measurement truth if coordinates remain; **declared measurement convention**, not kernel |

Smallest kernel: preserve attributed material and its limits; maintain scoped
identity, order, and addressability; perform declared exact representation
comparison/grouping/counting; and preserve Unknown/refusal. It produces only
bounded examination and measurement testimony. Encoding choice, strings,
characters, lines, regions, hashes, feature sets, and thresholds are not kernel
by identity. Native availability and determinism do not make them neutral.

## 7. Declared measurement-convention inventory

| Convention | Input -> operation -> output | Identity, loss, alternatives, applicability/selection | Current standing |
|---|---|---|---|
| Encoding | Python string -> `encode(request.encoding)` -> bytes for SHA-256 | requested name only; no version/purpose; loss is original decode history; many encodings | declared but applicability silently supplied; errors explicit |
| Character model | exact text -> `len()`/offsets -> Python code-point-like string positions | stated as “exact Python string”; not byte/grapheme coordinates | declared measurement convention |
| Line splitting | string -> `splitlines(keepends=True)`; empty -> zero lines | `external_material_structural_projection_v1`; no synthetic final line; alternatives include bytes/newline-only/stream rules | unusually explicit; applicability Unknown |
| Terminators | suffix tests -> has terminator and 0/1/2 count | asymmetry with `splitlines` for other Unicode separators is not declared | partially evidenced, mixed |
| Blankness | terminator-stripped content -> `strip()==""` | Python whitespace set hidden; alternatives space-only/byte-specific | compiled convention, incompletely declared |
| Region | maximal consecutive nonblank projected lines -> region | explicitly denies paragraph/section; alternative segmentation retained only conceptually | declared measurement convention |
| Coordinates | one-based lines; zero-based half-open Python-string character offsets including terminators | clearly emitted; alternative byte/grapheme/one-based models | declared measurement convention |
| Line lengths | `len(line.text)` and terminator-subtracted count | v1 notes; text omitted downstream; byte/grapheme widths unavailable | declared measurement convention |
| Region lengths | ordered line-length tuples and sums | preserves selected ordering; erases characters/patterns | declared measurement convention |
| Stable ids | SHA-256 of convention + scoped ids + coordinates, truncated | deterministic navigation, collision possibility/universal identity not claimed | declared convention |

Typed Unknowns are accepted as free strings and forwarded at projection/line/
region level, but no producer, type, resolution condition, or consumer-purpose
contract is enforced. Declaration makes these crossings more faithful for a
consumer needing exactly these measurements; it does not establish universal
applicability or erase the hidden whitespace/terminator asymmetry.

## 8. Learned external-grammar inventory

| Assumption | Classification | Recoverability / occurrence |
|---|---|---|
| “text”, Python string, UTF-8 | compiled substrate grammar / convention | UTF-8 hard-coded on documentation road; no competency identity/evidence; runtime-active |
| top-level `docs/*.md` | documentation policy + compatibility rule | selection explicit in code/CLI, authority/evidence absent; runtime-active |
| ATX `#{1,6}` headings/levels | compiled partial Markdown grammar | compatibility-tested; version/applicability/evidence absent |
| H1 as title | domain/document ontology | compiled realization; unearned external grammar |
| heading stack as section hierarchy | compiled Markdown/document grammar | alternatives/loss absent; runtime-active |
| `---` plus colon keys as front matter | partial YAML/front-matter grammar | not a complete parser; competency/applicability absent |
| backtick/tilde fences and info token | partial Markdown grammar | recognizes 0–3 spaces, matching char/length; language lowercased; version absent |
| inline/reference links | partial Markdown grammar | regex subset; normalization/path grammar compiled; version absent |
| relative/internal/broken target | path/URI compatibility grammar + documentation policy | repository existence test only; anchors, case, URI semantics incomplete |
| empty/duplicate/skipped sections | mixed syntax-derived measurement and documentation policy | “empty”, “duplicate”, “skipped” add ontology/policy labels |
| capitalized L + token + capitalized R | compiled English grammar + domain ontology | unearned; runtime-active and test-active |
| `owns`, `produces`, `consumes`, `preserves`, `bounds`, `derives`, `selects`, `explains`, `observes`, `does not own`, `hands off to`, `!=` | architectural vocabulary/semantic candidates | exact token list compiled without constitutive evidence |
| common/rare/outlier/complete/broken | policy and normative/presentation vocabulary | thresholds or predicates compiled; no constitutional standing |

File extension, regex match, or recurrence demonstrates compatibility with test
examples, not Markdown applicability, meaning, or learned competency standing.

## 9. Feature-candidacy analysis

A feature becomes eligible only because code selected it. There is no candidate
formation record, constitutive corpus, comparison of alternatives, purpose-local
selection, selection authority, applicability finding, conflict, or Fidelity
finding. The surface road selects length/blank/terminator/order features; the
documentation road selects heading text/depth, front-matter keys, fence language,
link class, and heading skeleton. This is implementation availability mistaken
for a closed feature horizon if consumers read it as “structure”.

All recurrence must be stated as:

> recurrence **R** under projection **P** using equivalence relation **E**
> within scope **S** for consumer purpose **C**.

Here P and E can mostly be reconstructed from code; S is top-level selected
`docs/*.md` after filters; C is only generically “structural visibility” and is
not constitutively recorded. Accordingly the probe cannot observe *any possible*
recurrence. It observes only recurrence expressible by its selected P/E. It does
not currently expose punctuation arrangements, indentation changes, balanced
delimiters, token positions, fixed-width columns, byte patterns, character-class
sequences, case-insensitive forms (except lowercased fence language), approximate
skeletons, semantic paraphrases, or cross-substrate structures. That is a scope
limit, not a demand that it support them.

## 10. Segmentation-grammar analysis

Line segmentation internalizes Python `splitlines`, a textual model, and its
boundary set. Blank segmentation internalizes Python whitespace. Region
segmentation internalizes blank lines as separators and maximal adjacency as a
unit rule. The emitted notes faithfully deny semantic boundaries, paragraphs,
sections, headings, rules, examples, and exercises. Nevertheless `line` and
`region` are formed objects, not discoveries from literal zero.

The exact honest standing is: “under convention v1, these ordered Python-string
slices and these maximal runs satisfy the declared predicates.” It does not
establish semantic unit boundaries, alternative segmentation irrelevance,
Markdown paragraphs, prose blocks, or grammar.

## 11. Equality and recurrence-identity analysis

| Family | P / E / S / C | Equality standing |
|---|---|---|
| line/region length arrangement | selected raw/content count sequences / tuple integer equality / one supplied projection / surface visibility | measurement equality; candidate structural equivalence only |
| section label | ATX capture `.strip()` / exact string equality / selected docs and all headings / recurrence, drilldown, membership | lexical equality, not meaning |
| front-matter key | delimiter/colon extraction / exact string equality / selected docs / recurrence | lexical equality under partial grammar |
| fence language | first normalized info token, lowercase / exact normalized string / selected docs/fences / recurrence | normalized lexical equality; original case erased |
| heading depth | ATX marker count / integer equality / selected headings / recurrence | numeric measurement equality |
| link target class | link regex + URI/path predicates / Boolean category membership / selected docs/links / totals | candidate classification equivalence |
| skeleton | `H1` discards title; other levels retain exact text; `|` serialization / exact signature equality / selected docs / skeleton visibility | mixed measurement/lexical equality, not document grammar identity |
| common-section membership | set of exact section labels per doc / exact label equality / selected docs / missing comparison | lexical membership only |

Same string is not same meaning; different string is not different structure;
same count is not same pattern; same skeleton is not same grammar; repeated rows
are not independent evidence. Exact recurrence establishes only membership in a
declared representation-equivalence class, not structural or semantic identity.

## 12. Recurrence/count standing analysis

The chain is:

1. compiled parser emits an occurrence;
2. `Counter` groups exact projected values;
3. arithmetic produces counts;
4. fixed buckets (`1`, `2`, `3-4`, `5-9`, `10-24`, `25-99`, `100+`) summarize
   distinct-entry count distributions;
5. filters and thresholds rename subsets rare/common;
6. per-document exact-label sets support missing comparisons; and
7. unrelated policy signals are aggregated into outlier rows.

Steps 2–4 are faithful measurements only relative to parser P, equality E, and
corpus S. Counts do not establish recurrence meaning, significance,
representativeness, independence, grammar, or authority. Corpus filtering and
size changes can change every later label without changing a document.

## 13. Commonness and rarity analysis

Itemized default minimums are section labels 2 and all other families 1;
`--min-count` overrides all. Rare defaults to inclusive counts 1–2;
`--min-count` supplies its lower bound and `--max-count` its upper bound.
“Common section” means exact section label present in at least **25 documents**,
not 25 occurrences or a proportion. The threshold remains 25 when corpus size
changes; for fewer than 25 documents nothing can be common, while at 25 a label
must be universal.

These are consumer-local hard-coded policies/filters. Tests establish
compatibility, not authority. Frequency is not significance; rare is not
anomalous; common is not required; and missing a common exact label is not an
incomplete document.

## 14. Outlier and issue-policy analysis

An outlier row exists if any compiled signal fires: missing front matter;
missing trailing newline; one or more “empty sections”; section count >=10;
code-fence count >=5; link count >=10; max heading depth >=5; or at least one
section-label occurrence whose corpus count <=2. It is sorted by number of
signal **types**, not magnitude or statistical distance.

The separate issue score used for `--top` sums: status not complete (1), missing
trailing newline (1), empty-section count, broken-local-doc-link count, and
unclosed-fence count. “High” thresholds do not contribute to issue score.
Thresholds have implementation authority only; no Book/corpus evidence or
versioned policy identity was recovered. “Outlier”, “issue”, and “offender”
formatting are normative classifications, not measurements. Corpus change can
alter rare-label signals; fixed magnitude thresholds ignore corpus size.

## 15. Documentation-ontology analysis

| Crossing | Structural evidence | Imported grammar / strengthening / alternatives |
|---|---|---|
| `#` token sequence -> heading | regex match and capture | partial ATX Markdown grammar; setext/HTML absent |
| marker count -> hierarchy | 1–6 count | Markdown convention plus stack ontology; heading sequence need not express semantic parentage |
| first H1 -> title | first level-1 match | documentation convention/domain ontology; multiple/no title alternatives |
| heading interval -> section | next heading of <= level closes interval | invented document-shaped subject under compiled rule |
| stack -> parent/child | nearest prior shallower heading | structural convention with semantic-looking hierarchy |
| no nonheading nonblank line -> empty section | selected line predicates, code-content exclusion | policy meaning of content/emptiness; child headings ignored |
| `---` delimiters -> front matter | exact first/closing lines | partial front-matter grammar; thematic break/YAML alternatives |
| colon line -> key | split first colon, ignore blank/comment | partial YAML-like grammar, no YAML parse |
| fence info token -> language | first whitespace token lowercased | convention/semantic candidate, not verified programming language |
| link-shaped text -> target/link | regex capture | partial Markdown link grammar |
| local target absent -> broken | path resolution + `exists()` | repository/path policy; unresolved anchors/content/case semantics |

Loss and alternatives are not emitted by documentation records. Applicability,
Markdown version, parser subset, and Typed Unknowns are absent. Therefore the
records are useful compiled projections but not recoverable learned competency.

## 16. Markdown competency analysis

The realization supports a bounded subset: UTF-8 decoded top-level Markdown
files; ATX headings only; fenced blocks with backtick/tilde runs and matching
close; a delimiter/colon front-matter approximation; inline non-image and
reference-definition links; and repository-relative path classification. It
does not identify a Markdown specification/version or preserve constitutive
examples, applicability criteria, refusal rules, alternatives, conflicts, or
Fidelity findings.

Markdown applicability is inferred operationally from `docs/*.md` or a required
`.md` selection path. Extension and location are selection policy, not evidence
that contents instantiate Markdown or that this subset is applicable. The
competency is **compiled realization**, **compatibility-tested**, and **unearned
external grammar** at this boundary; absent constitutive evidence does not prove
it unlawful or prove that evidence never existed globally.

## 17. Architectural-relation mini-observer analysis

Outside recognized code-content lines, the observer skips blank and selected
leading markup lines, then matches capitalized left/right strings with characters
`[A-Za-z0-9_. /-]` around one exact token: `does not own`, `hands off to`,
`owns`, `produces`, `consumes`, `preserves`, `bounds`, `derives`, `selects`,
`explains`, `observes`, or `!=`. Optional final punctuation is removed by the
match. The record stores captures, source path, line, and stripped source line.

Separate standings:

1. **evidenced pattern occurrence:** this line matched compiled regex P with
   captures L/R and token T;
2. **candidate grammatical roles:** P assigns L as left/subject-like and R as
   right/object-like; unearned English grammar;
3. **candidate token interpretation:** T resembles a relation/negation/operator;
   unearned lexicon/domain grammar;
4. **candidate architectural assertion:** the line may be read as asserting
   L T R; semantic candidate only;
5. **attribution:** the repository artifact contains the matching line at the
   coordinate; with proper source binding this can support attributed text, not
   automatically author intent;
6. **truth/standing:** entirely unestablished.

The safest output claim is exactly: “outside the observer's selected code-line
exclusions, source line N matched compiled pattern P with captures L, T, R.”
`DocumentationArchitecturalRelationRecord` overstates that safe claim through
its type/field vocabulary. It does not establish that the document asserted the
architectural relation in the intended sense, and never establishes the relation
is true. The observer has internalized English word order, capitalization as
term boundary, a narrow noun-phrase alphabet, subject/relation/object roles,
negation only for ownership, and architectural meanings for ownership, handoff,
production, consumption, preservation, bounding, derivation, selection,
explanation, observation, and inequality.

## 18. Boundary-declaration Fidelity analysis

| Declaration | Finding |
|---|---|
| read-only; no event/repository/cluster mutation | **evidenced** and compatibility-tested for examined paths; faithful side-effect boundary |
| preserves evidence | partially evidenced: external line road preserves exact slices and coordinates; surface road intentionally omits raw text; documentation records retain selected evidence only |
| no prose interpretation / no claim extraction / no authority inference | substantially faithful as to truth and authority: no Fact or authority promotion; incomplete because relation roles and document labels interpret lexical forms |
| no grammar interpretation / owns no grammar / no substrate parsing | contradicted as a behavioral description of documentation adapter: regexes implement Markdown/path/front-matter/English grammar; possibly accurate only as owner-allocation metadata for shared `StructureObservationBoundary` |
| no shape inference | incomplete/contradicted: heading hierarchy, sections, skeletons, relations, and outliers are inferred shapes/classes |
| no ontology promotion | no cluster/Book promotion occurs, but output types promote matches into local `section`, `title`, `architectural relation`, `complete`, `broken`, and `outlier` vocabulary; therefore partial constraint, not full description |
| exact membership; no classification | exact matching is faithful, but category parsing and “section label” depend on prior classification; membership stage adds no similarity |
| not Evidence/Fact/capability evidence | faithful negative standing for external projections; no persistence/promotion found |

Negative authority is valuable and prevents stronger reliance, but a declaration
is not a Fidelity finding and cannot negate operations the code performs.

## 19. Compiled realization versus recoverable competency matrix

| Competency/convention | Identity/version | Evidence, applicability, selection, authority | Rules/loss/alternatives/Unknowns | Finding |
|---|---|---|---|---|
| testimony reference binding | artifact type/status, no competency version | manifest/request supply; reference consumer clear; source authority refused | exact rules visible, alternatives/typed resolution sparse | partially evidenced convention |
| line/region projection | `external_material_structural_projection_v1` | input scope and selection explicit; applicability/authority not established | rules/coordinates/negative loss good; alternatives and typed Unknowns incomplete | strongest recoverable declared convention |
| surface features | `external_material_surface_feature_projection_v1` | upstream identity explicit; feature candidacy/purpose absent | selected rules/loss substantially visible; alternatives absent | declared convention, selection compressed |
| Markdown parser | module/function names only | constitutive evidence, version, applicability, authority absent | rules reconstructable from code; loss/alternatives/Unknowns absent | compiled realization, compatibility-tested, unearned external grammar |
| recurrence grouping | report fields, no convention id | scope reconstructable; purpose/authority incomplete | E reconstructable; independence/loss/alternatives absent | mixed measurement and compressed competency |
| thresholds/status/outlier | signal strings only | no evidence or authority | rules visible in code; rationale/version/conditions absent | policy/normative classification |
| relation matcher | regex constants, no competency id/version | no constitutive English evidence/applicability/selection authority | patterns visible; loss/conflicts/Unknowns/refusal absent | unearned external grammar |
| Fidelity examination | no responsible comparison in probe | absent | absent | implementation ability to test is not established Capability |

No compiled grammar examined here has recoverable constitutive learned-competency
evidence. The two versioned external projections have recoverable realization
rules and negative authority, making them declared conventions, not learned
grammar. Evidence unrecovered here is not proof that it never existed.

## 20. Typed Unknown matrix

| Unknown | Producer / consumer / resolution condition | Current representation |
|---|---|---|
| material encoding and decode history | supplier -> binding/projection; resolve by provenance plus byte/decode competency | encoding asserted; applicability silently resolved; decode history absent |
| character model | projection convention -> coordinate consumer; resolve by purpose | Python string stated; alternatives absent |
| line-boundary applicability | projection -> structure consumer; resolve by substrate evidence | absent/silently resolved |
| semantic unit/region boundaries | later grammar consumer; resolve by learned grammar | explicitly refused in notes, not typed |
| feature relevance/candidacy | recurrence consumer; resolve by purpose/evidence/selection | absent and frozen |
| alternative segmentation/E | comparison consumer; resolve by declared examination | absent except negative prose |
| Markdown applicability/version | documentation observer consumer; resolve by attributed grammar competency | inferred from path; absent |
| heading/title/section/front-matter/fence/link meaning | documentation consumer; resolve by grammar evidence | silently resolved into record types |
| language-token meaning | code-fence consumer; resolve by grammar/domain evidence | lowercased token emitted as `language` |
| relation token and L/R boundaries | relation consumer; resolve by English/domain competency | silently resolved by regex |
| threshold applicability/authority | report consumer; resolve by consumer-local policy warrant | absent; constants execute |
| corpus representativeness | recurrence consumer; resolve by scoped corpus-selection evidence | absent |
| occurrence independence | evidence consumer; resolve by provenance/source analysis | absent; counts can duplicate one source |
| source truth/authority | any semantic consumer; separate evidence/establishment | explicitly refused by binding notes |

Free-form `unknowns` tuples are explicit carriage slots on external artifacts,
but most named Unknowns above are not produced. Documentation records expose no
Unknown slots. Thus Unknown preservation is strongest at Layer A/B and weakest
at Layer D.

## 21. Capability matrix

| Capability | Ability / availability / execution | Applicability, selection, authority, verification / current standing |
|---|---|---|
| material binding | implemented, CLI/test active | scoped compatibility; no constitutional Capability artifact recovered |
| exact-text preservation | implemented in structural lines | selected by request; fidelity substantially test-evidenced |
| coordinate projection | implemented | applicability Unknown; declared convention |
| line/region segmentation | implemented/executed | rules selected; substrate applicability unverified |
| surface measurement | implemented/executed | exact under Python model; feature relevance unverified |
| feature selection | hard-coded/executed | selection act compressed; authority/purpose absent |
| exact recurrence counting/distributions | implemented/CLI-triggered | valid under P/E/S; purpose/independence limits absent |
| threshold comparison/outlier classification | implemented | policy authority and applicability absent; normative output only |
| Markdown parsing/document projection | implemented/test-active | compatibility shown; competency standing absent |
| English relation matching | implemented/test-active | pattern compatibility only; learned grammar absent |
| candidate grammar formation | not performed by these roads | absent |
| Fidelity examination | tests compare expected behavior; no bounded constitutional Fidelity producer | Capability standing absent |

Availability, applicability, selection, authority, execution, result, and
verification must remain distinct. Tests establish deterministic compatibility
and side-effect behavior, not constitutional Capability standing.

## 22. Gap matrix

| Consumer-local Gap | Present standing vs required standing | Consequence |
|---|---|---|
| convention applicability unexamined | exact declared line measurements vs consumer needing substrate-fit structure | measurements cannot generalize beyond v1 |
| frozen feature candidacy | selected lengths vs consumer seeking evidence-born recurrence | invisible recurrence families cannot become candidates |
| recurrence identity hidden in report | counts/labels expose values but no P/E/S/C identity/version | consumer may read count as general recurrence |
| Markdown competency unrecoverable | compiled matches vs consumer needing attributed learned grammar | document constructs have no recoverable applicability/authority |
| document ontology unattributed | regex-derived records vs consumer needing source-relative meanings | `title`/`section` appear native |
| common/rare/outlier authority absent | exact counts plus constants vs consumer needing warranted comparison | policy words can appear factual/normative |
| relation output semantically typed | lexical match vs consumer needing architectural assertion | match is strengthened into relation-shaped record |
| negative declarations incomplete | “no grammar/shape inference” vs executed parsing/inference | boundary metadata obscures the crossing |
| compiled vs learned grammar indistinguishable | implementation rule vs competency standing | later grammar recovery could inherit answers as evidence |

The declared coordinate/length convention is not itself a Gap for a consumer
requiring exactly that bounded measurement. The Gap appears only when a consumer
requires stronger applicability or meaning.

## 23. Demand matrix

| Active consumer requirement | Present standing + bounded incompatibility | Demand classification |
|---|---|---|
| recurrence report needs interpretable recurrence families | parser-relative counts, but P/E/S/C not emitted as contract | consumer-local constitutional Demand for bounded recurrence reliance; no persisted Demand artifact |
| missing-common-section report needs “common” and absence comparison | exact label presence plus threshold 25; no requirement authority | runtime implementation pressure; stronger normative Demand unmet |
| outlier/issue/top needs comparison policy | measurements plus hard-coded signals | consumer-local policy Demand is compressed, not constitutional defect standing |
| structure status needs completeness criterion | two Booleans plus hard-coded labels | active runtime Demand for policy label; no Book authority for completeness standing |
| architectural relation output needs attributed semantic assertion | regex match only | semantic Demand unmet; record can safely support pattern testimony only |
| later grammar recovery needs constitutive evidence | compiled realization/test examples only | applicable future consumer Demand; currently no execution of recovery |

Formula: applicable requirement + present standing + bounded comparison +
incompatibility + consumer-local consequence yields Demand. None of the rows is
a persisted `Demand` artifact, and runtime report construction is not proof of a
constitutional Demand occurrence.

## 24. Fidelity crossing matrix

| Crossing | Preserved / erased / normalized | Invented or strengthened; scope/authority/source change | Finding |
|---|---|---|---|
| bytes -> decoded text | documentation bytes counted; decoded UTF-8 text | decode provenance/invalid-byte alternatives erased | mixed; applicability Unknown |
| text -> physical lines | order and text slices preserved externally; terminators omitted in documentation `splitlines()` | “physical line” under Python convention | faithful within declared external v1; documentation rule hidden |
| lines -> blank/nonblank | content preserved externally | Python whitespace predicate adds classification | declared/mechanical but first structural strengthening |
| lines -> nonblank regions | line ids/order preserved | maximal run object invented; semantics refused | faithful bounded convention |
| lines/regions -> surface features | ids/order/counts retained; raw text erased downstream | selected feature horizon | faithful measurement, candidacy Unknown |
| features -> recurrence identities | selected tuples/values | equivalence class chosen | E-dependent, not general structure |
| recurrence identities -> counts | identities/cardinality preserved | no semantic change by arithmetic | faithful bounded measurement; independence Unknown |
| counts -> common/rare | count retained | fixed policy labels, authority change | normative strengthening |
| document text -> Markdown constructs | selected coordinates/text/captures retained | partial external grammar applied; alternatives erased | unearned external grammar |
| headings -> hierarchy/sections | levels/order retained | parentage/section objects invented | ontology strengthening |
| document measurements -> `structure_status` | front-matter/H1 Booleans recoverable | “complete/missing” policy standing | strongest explicit normative strengthening |
| measurements -> outlier signals | raw counts often retained | high/rare/outlier significance invented | normative classification |
| relation-shaped line -> relation record | line/path/captures/token preserved | grammatical roles and architectural relation type strengthened | semantic candidate emitted as semantic-looking record |

No examined crossing changes cluster state or source truth. The relevant
failures are representation/authority strengthening, not mutation.

## 25. Object-bias and vocabulary-bias audit

| Name | Actual bounded status |
|---|---|
| `StructureObservationBoundary` | implementation/compatibility metadata; not a constitutional owner or Fidelity finding |
| `ExternalMaterialStructuralProjection` | declared projection artifact; “structural” is presentation vocabulary |
| `ExternalMaterialProjectedLine` | convention-defined slice/measurement, not semantic line universally |
| `ExternalMaterialProjectedNonblankRegion` | convention-defined maximal run, explicitly not paragraph/section |
| `ExternalMaterialSurfaceFeatureProjection` | selected measurement representation, not complete feature space |
| `DocumentationStructureRecord` | mixed compiled external grammar, measurements, ontology, and policy |
| `DocumentationSectionRecord` | external/document grammar object and semantic candidate, no constitutional standing |
| `DocumentationStructureRecurrenceReport` | P/E/S-relative counts plus policy labels |
| `DocumentationArchitecturalRelationRecord` | pattern-match testimony wrapped in semantic-looking object vocabulary |
| line / region / surface feature | measurement-convention/presentation terms |
| structure / recurrence | candidate structural equivalence and bounded count vocabulary, not native ontology |
| common / rare / outlier | policy/normative classifications |
| section / title | compiled documentation ontology |
| complete / broken | consumer-local policy labels, not global quality or truth |
| architectural relation | semantic candidate; safest standing is regex match occurrence |

Object shape and field names bias consumers toward stable entities and meanings.
They do not create constitutional subjects or standing.

## 26. Strongest faithful surfaces

1. Manifest/request/hash rebinding accurately refuses source authority, truth,
   annotation correctness, and claim support.
2. External v1 projection preserves exact line slices, order, coordinates,
   hash-linked identity, convention descriptions, Unknown carriage, and explicit
   semantic refusals.
3. Surface v1 retains upstream identity and ordered exact measurements, states
   raw-text omission, normalization refusal, and the nonsemantic status of
   recurrence.
4. Exact `Counter` arithmetic is faithful when read only as P/E/S-relative
   cardinality.
5. Read-only, no-ledger, and no-cluster-mutation declarations accurately bound
   operational effect.

## 27. Strongest contradictions

1. “No grammar interpretation/no substrate parsing” coexists with compiled
   Markdown, front-matter, path, and English parsers.
2. “No shape inference” coexists with heading hierarchy, sections, skeletons,
   missing-common structure, and outliers.
3. “No interpretation occurs” is too broad for `strip` blankness and
   terminator/feature selection, though semantic refusals remain faithful.
4. `DocumentationArchitecturalRelationRecord` grants semantic-looking object
   form to a lexical pattern occurrence.
5. `structure_status="complete"`, issue score, “offenders”, common/rare, and
   outliers impose policy while the boundary sounds purely observational.

## 28. Strongest Unknowns

The strongest unresolved dimensions are: whether Python-string/line/whitespace
conventions apply to the source and consumer; why selected features matter;
what alternative P/E would expose; Markdown identity/version/applicability and
constitutive evidence; front-matter dialect; title/section meaning; relation
term boundaries and token meaning; threshold authority; corpus
representativeness; repeated-occurrence independence; and whether any compiled
grammar was once learned elsewhere. The current probe mostly erases or silently
resolves these on the documentation road.

## 29. Smallest positive reference competency

The smallest positive reference is not “structure observation” generally. It is:

> Given attributed exact text, a manifest artifact hash, an explicitly selected
> encoding, and external structural projection convention v1, validate the
> representation binding; preserve exact ordered slices and coordinates; emit
> blankness and maximal-nonblank-run measurements under the named rules; carry
> Unknowns and negative authority; and refuse semantic unit, grammar, Fact,
> Evidence, correspondence, or responsibility standing.

Its evidence is the recoverable implementation rule plus focused compatibility
tests and boundary output. It is a **declared measurement competency**, not yet
a learned cross-substrate grammar. Its first compressed crossing is applicability
of Python textual segmentation/whitespace to the supplied material.

## 30. Smallest next honest recovery

Stopping without recommendation: the smallest next honest recovery subject is
the first exact compressed crossing already present—how encoding/Python-string
material receives applicability for `splitlines` and Python-whitespace blankness,
and how that convention is selected for a stated consumer purpose. No English
observer, candidate grammar, redesign, schema, threshold, parser, or deletion is
specified here.

## Direct answers

1. **Smallest constitutional kernel:** attributed preservation; scoped identity,
   order, and addressability; declared exact comparison/group/count; and
   Unknown/refusal. It produces examination/measurement standing only.
2. **Primitives that are conventions:** encoding, Python string/character
   coordinates, line splitting, terminator handling, whitespace blankness,
   nonblank runs, lengths, and stable ids.
3. **Standing before projection:** supplied, source-attributed manifest/artifact
   testimony plus representation/hash/count compatibility—not truth, authority,
   or universal artifact identity.
4. **Line projection establishes:** exact ordered convention-defined string
   slices, coordinates, counts, terminator predicate, and stable scoped ids.
5. **Blank/region projection establishes:** predicate satisfaction and maximal
   adjacency under Python whitespace and v1 rules.
6. **It does not establish:** paragraphs, sections, semantic units, grammar,
   meaning, correspondence, responsibility, Evidence, or Fact.
7. **Selected surface features:** raw/content/terminator character counts,
   blank/terminator flags, line order/ids; region line count, ordered length
   sequences, totals, and ids.
8. **Evidence for relevance:** none recovered; code/tests establish selection and
   compatibility only.
9. **Any recurrence?** No universal “any”; only selected P/E recurrence.
10. **Actual families:** exact section labels, front-matter keys, heading depths,
    normalized fence languages, link classes, heading skeleton signatures, and
    selected line/region length arrangements (the last are measurable but not
    corpus-counted by the documentation recurrence report).
11. **P/E for each:** stated in section 11; every one is representation-,
    lexical-, numeric-, tuple-, or Boolean-class equality within selected scope.
12. **Exact recurrence -> structural equivalence?** No; only equality under E.
13. **Common:** exact section label present in >=25 selected documents.
14. **Rare:** exact projected entry count within inclusive defaults 1–2 or
    supplied bounds.
15. **Outlier:** at least one hard-coded signal listed in section 14.
16. **Threshold authority:** implementation-local constants/options only; no
    constitutional or constitutive evidence recovered.
17. **Structurally complete:** compiled front matter and first H1 both present.
18. **Its kind:** consumer-local documentation policy/normative classification,
    not mere measurement or constitutional standing.
19. **Compiled Markdown grammar:** the bounded subset in section 16.
20. **Applicability:** inferred operationally from top-level path/`.md`, not
    established.
21. **Compiled English grammar:** capitalized L, exact relation token, capitalized
    R, narrow characters/order/punctuation, limited negation and architectural
    lexicon.
22. **Safest relation claim:** source line N matched P with captures L/T/R.
23. **Does record establish document asserted relation?** No; at most attributed
    matching text plus candidate assertion.
24. **Does it establish truth?** No.
25. **Faithful negative declarations:** read-only/no writes/no mutation; no Fact,
    authority, responsibility, or cluster-truth promotion; semantic refusal on
    external v1 road.
26. **Contradicted/incomplete:** no grammar parsing, no shape inference, no
    interpretation, and no ontology promotion as broad behavioral descriptions.
27. **Recoverable constitutive competencies:** none for learned Markdown/English;
    binding and external v1 rules are recoverable declared conventions with
    tests, not learned competency evidence.
28. **Declared conventions without learned evidence:** the inventory in section
    7, especially line/coordinate/length projection.
29. **Unearned external grammar:** UTF-8/path-selected Markdown/front matter,
    document ontology, link/path semantics, English relation patterns, and
    architectural vocabulary.
30. **Silent strengthening:** blank/region labels (bounded), Markdown constructs,
    title/section/hierarchy/emptiness, language/link/brokenness, skeleton
    structure, common/rare/missing/outlier/issue/complete, and relation records.
31. **Strongest positive reference:** versioned external material structural and
    surface measurement with exact binding, preservation, and negative authority.
32. **First missing/compressed crossing:** evidence and authority selecting the
    Python textual segmentation/whitespace convention as applicable for this
    material, scope, and consumer purpose.
