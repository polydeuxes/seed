# Predicate and the Relation-Assertion Coordinate

## Investigation boundary and method

**Question.** Does `Predicate` name an irreducible constitutional distinction in
relation grammar, or can every predicate-shaped responsibility be expressed by
the active grammar without it?

- **[active law]** The numbered chapter directories are controlling. This report
  treats every other Book file, runtime shape, test, and commit as testimony at
  the authority level specified by the investigation.
- **[active law]** A class, field, inventory row, recurring name, or stable
  serialization does not establish a kind or its production authority
  (01.Kinds:18-22).
- **[method]** Sections 1-4 were completed independently and written to a
  timestamped scratch record before any attempt to open the prior report. Only
  then was `git show c9ec7e9:book_of_seed/predicate_cat_test_001.md` attempted.
- **[Unknown]** The supplied commit is not present in this checkout, there is no
  configured Git remote, and neither the named report nor an unreachable object
  containing it exists locally. The full prior report therefore could not be
  read. Section 8 reconciles only the prior findings quoted in the investigation
  request; it does not pretend those excerpts are the full report.

## 1. Relation-coordinate inventory

### 1.1 Coordinates recovered from active law

| Coordinate or local concern | What it preserves | Status and authority |
|---|---|---|
| relation claim subject / identity | the relation itself as a bounded claim subject, distinct from participant identity | **[active law]** 01.Kinds:27-28 |
| participants and roles | each related subject and its place in this exact relation | **[active law]** 01.Kinds:28 |
| **relation assertion** | **what relation is being asserted** | **[active law]** 01.Kinds:28 |
| evidence standing | whether and how evidence supports this relation claim | **[active law]** 01.Kinds:28; 05.Evidence:15-19 |
| standing | candidate relation, testimony, evidence-supported relation, established relation, or a bounded responsibly produced Unknown | **[active law]** 01.Kinds:28,69 |
| source, attribution, provenance | where the assertion/material came from and who supplied it; for meaning relations these are explicit local concerns | **[active law]** 01.Kinds:30-32 |
| producer and occurrence | the responsibility and evidenced occurrence that carried, proposed, or warranted the relation | **[active law]** 01.Kinds:28,30-32 |
| consumer and purpose | the local consumer/use boundary where applicable | **[active law]** 01.Kinds:28,30,36-45 |
| scope / locality | the bounded corpus, subjects, place, time, or purpose to which the assertion applies | **[active law]** 01.Kinds:28,30 |
| authority and warrant | authority to make the exact assertion and the claim-appropriate warrant it has | **[active law]** 01.Kinds:28,30-32 |
| conflicts, known loss, limits, Unknowns | what is contested, discarded, bounded, unresolved, or inapplicable | **[active law]** 01.Kinds:28,30 |

- **[active law]** This is an inventory of locally applicable concerns, not a
  universal serialized schema. The eight macro-families—subject/identity,
  assertion/content, standing, source/provenance, responsibility,
  authority/warrant, scope/locality, and occurrence/preservation—are orientation,
  not mandatory fields or a closed coordinate count (01.Kinds:51-67).
- **[active law]** Relations, acts, and constraints are structurally distinct
  from those dimensions. A relation operates with dimension-bearing material; it
  is not an extra dimension merely because a field carries it (01.Kinds:67).

### 1.2 Vacancy test

- **[active law]** There is **no vacancy for “what relation is asserted.”** The
  controlling coordinate is named verbatim: **the relation assertion**
  (01.Kinds:28). In the macro orientation it belongs under assertion/content
  (01.Kinds:54-56), but the local name is more exact.
- **[active law]** The coordinate does not require a canonical Predicate value,
  a catalog entry, interpreted meaning, or established warrant to exist. An
  applicable coordinate may be known, Unknown, conflicting, or unresolved, and
  unsupported local coordinates may remain Unknown or inapplicable
  (01.Kinds:30,65,69).
- **[inference]** A source token such as `causes` or `=` may therefore be the
  exact represented **content** of the relation-assertion coordinate. `Predicate`
  can be an implementation label for that content, but it does not name a second
  coordinate alongside relation assertion.
- **[Unknown]** Active law does not prescribe one universal internal syntax for
  storing the representation inside the relation assertion. That serialization
  question is not a constitutional vacancy.

## 2. Cat-test table

| Reading | Does it name something, and of what kind? | Owner / producing act / Standing | Result |
|---|---|---|---|
| Predicate as developer catalog | A hand-authored list of 76 predicate definitions and five mappings. | `PredicateCatalog.load` reads authored JSON; construction establishes catalog readability and validation, not relation standing. No source evidence or claim-specific warrant accompanies each definition. | **[runtime witness] developer-compiled competency**, not a constitutional distinction. |
| Predicate as canonical vocabulary | A runtime namespace for durable/measurement labels, value types, cardinality, and allowed values. | Developers supply the JSON and mappings. Loading/lookup is the implementation act; no active clause makes that vocabulary law. | **[runtime witness] ordinary implementation term plus developer-compiled competency**; **[active law]** shape/name cannot confer standing (01.Kinds:18-22). |
| Predicate as normalization target | The mapped `canonical_predicate` in a derived Observation. | `PredicateNormalizer.normalize` consumes an Observation plus a catalog rule and produces another Observation with original and canonical labels. Normalization canonicalizes an already interpreted claim; it creates no new subject, proof, or support (05.Fact:10-12). | **[active law] derived representational property** and **[runtime witness] developer-selected target**; not a kind. |
| Predicate as interpreted meaning | A possible interpretation of what source material says of/between participants. | Interpretation must precede normalization (05.Fact:10-12,64-65). A responsible occurrence may warrant a bounded meaning relation, while mere carriage does not (01.Kinds:30-34; 05.Evidence:41-42). | **[active law] constitutional relation form only when it is a warranted meaning relation**; `Predicate` itself is neither identical to meaning nor its warrant. |
| Predicate as relation kind/name | A name or representation such as `depends_on`, `causes`, or `=` offered as the asserted relation. | A source/translator may carry a relation proposal; a responsible relation producer may establish its standing. A label or catalog does neither by identity (01.External:14-19; 01.Kinds:28). | **[inference] ordinary representation that can occupy relation assertion**; not an additional constitutional kind. |
| Predicate as grammatical relation coordinate | A proposed name for the place that answers “what is asserted between/of these participants?” | Active law already assigns this responsibility to relation assertion. Relation production establishes the bounded relation standing, not a Predicate constructor. | **[active law] reducible to the existing relation-assertion coordinate**. `Predicate` adds no irreducible distinction. |

### Elimination test

- **[inference]** Remove the word `Predicate`, its class names, its catalog, and
  its runtime fields: canonical observation lookup, normalization, aggregation,
  and consumers keyed by that field would cease to work in their current form.
  That is implementation loss, not loss of a constitutional distinction.
- **[active law]** No relation-grammar distinction becomes impossible to
  preserve. Participants and roles still preserve who participates; relation
  assertion still preserves what is asserted; identity, meaning, evidence,
  warrant, Standing, scope, producer, occurrence, conflicts, and limits retain
  their separate responsibilities (01.Kinds:28-34).
- **[inference]** Downstream lookup, projection, conflict grouping, or inference
  demand explains why a stable implementation key is useful. It does not prove
  that the key carries a distinction beyond relation assertion.

## 3. Source-population test

### 3.1 Is source-population lawful without semantic knowledge?

- **[active law] Yes, with a boundary qualification.** A responsible occurrence
  may form a bounded representation from exact source material without changing
  the source's Standing; its assertion is limited to what the source exposes
  under the formation purpose, scope, authority, evidence, and provenance
  (06.Representations:12-16,26-30).
- **[active law]** External material may be preserved as attributed source
  grammar or translated into a bounded relation proposal while interpretation,
  meaning-relation warrant, applicability, admission, truth, and native grammar
  remain unestablished (01.External:14-22,33-34).
- **[active law]** Exact material adjacency is insufficient. Merely preserving
  three strings does not establish participant roles or a relation
  (01.Kinds:24-25), and field adjacency does not warrant meaning
  (05.Evidence:38-42).

### 3.2 Lawful weak shape

```text
relation-claim subject: bounded source-relative proposal R
participant/role 1:    exact source-derived Representation
relation assertion:    exact source-derived Representation
participant/role 2:    exact source-derived Representation
source/provenance:      preserved source boundary and extraction/formation lineage
meaning:                unresolved / Unknown if responsibly found Unknown
relation Standing:      carried proposal or attributed testimony only
Warrant:                not established
```

- **[inference]** This is compositional under current relation, external-source,
  representation, Evidence, and Standing law. It requires no new Representation
  kind and no canonical Predicate vocabulary.
- **[active law]** “Meaning = Unknown” must not be fabricated. If no responsible
  finding produced Typed Unknown Standing, the honest result is unresolved or
  absence of an established warrant, not a positive Unknown artifact by identity
  (01.Kinds:28,69; 08.Communication:14).
- **[active law]** `Warrant = not established` does not mean false, negated, or
  unrelated. Candidate relation, testimony, supported standing, and established
  standing remain distinct (01.Kinds:28).

### 3.3 Given source strings

| Material | What can be preserved without developer interpretation? | What remains unestablished? |
|---|---|---|
| `A noun is a word` | **[inference]** exact representations `A noun`, `is`, `a word`, plus attributed source order/segmentation if the responsible source boundary actually supplies it | **[Unknown]** sense of `is`, class-membership semantics, truth, and relation warrant |
| `X causes Y` | **[inference]** exact `X`, `causes`, `Y` representations and a source-relative relation proposal | **[Unknown]** causal meaning and causation; correlation/source assertion is not established causation (05.Evidence:29-30) |
| `2 + 2 = 4` | **[inference]** exact expression tokens/segments and source-relative proposal that `=` relates represented expressions | **[Unknown]** parsing, arithmetic semantics, equality truth, and the role of `+` absent source grammar/evidence |
| `F = ma` | **[inference]** exact represented expressions and `=` token in their source relation position | **[Unknown]** multiplication convention, physical interpretation, lawhood, truth, and warrant |
| `x < y` | **[inference]** exact represented participants and `<` as relation-assertion content if source structure supports that segmentation | **[Unknown]** ordering domain, denotation of variables, truth, and warrant |

## 4. Cross-domain stress test

| Domain | Candidate relation-assertion Representation | Same vacancy? | Limit |
|---|---|---|---|
| ordinary English | `is`, `causes` | **[active law]** no: relation assertion owns the distinction | **[Unknown]** word sense and syntactic role until supported; lexical position is not meaning |
| mathematical notation | `=`, `<`, `∈` | **[inference]** no: exact notation can occupy the same coordinate | **[Unknown]** formal system, operand denotation, semantics, and truth |
| physics notation and prose | `=`, `causes`, domain-specific phrases | **[inference]** no: the coordinate is representation-neutral | **[Unknown]** empirical/theoretical meaning, convention, and warrant |
| programming-language material | equality/comparison/operator syntax or named relations | **[inference]** no when source grammar actually presents a relation | **[active law]** programming grammar remains external grammar; syntax and adjacency do not become Seed law (01.External:9-19) |

- **[inference]** `=`, `<`, `∈`, `is`, and `causes` can occupy the same
  relation-assertion coordinate as exact source-derived Representations. This
  states common placement, not semantic equality, substitutability, shared kind,
  or equivalent warrant.
- **[inference]** The coordinate is not English-specific because active law calls
  for assertion/content rather than a word, lemma, verb, or catalog key.
- **[inference]** In `x + y = z`, `=` is the candidate assertion relating the
  represented expression `x + y` to `z` if source grammar supports that parse.
  `+` is then inside a participant expression and may represent an operation or
  function application. In another grammar it could play another role. Infix
  position alone does not force `+` and `=` into one constitutional kind.

## 5. Runtime and history testimony table

| Machinery | Supplier and evidence | Responsibility actually performed | Effect of a source-populated relation assertion |
|---|---|---|---|
| `predicate_catalog/core.json` | **[runtime witness]** developers supplied 76 definitions and five mappings; the rows contain operational metadata but no per-row source, provenance, producer occurrence, authority, scope, conflicts, known loss, or semantic warrant. | Stable vocabulary, value/cardinality metadata, provider-to-canonical lookup: compiled competency. | **[inference]** unnecessary for merely carrying exact source relation content; still separately useful for authored validation, grouping, projection, and compatibility policy. |
| `PredicateCatalog` / `PredicateDefinition` / `PredicateMapping` | **[runtime witness]** constructors validate literals and mapping targets; JSON loading supplies the values. | Read-only catalog access, mapping specificity, value remapping, cardinality and measurement policy. | **[inference]** not needed to represent the source assertion; remains a distinct implementation policy service. |
| `canonical_predicate` | **[runtime witness]** developer-authored mappings choose the target; metadata records original and canonical labels. | Target label for canonicalized observation representation. | **[inference]** source population removes no need for optional canonical comparison, but it removes any excuse to substitute canonical content for exact source testimony. |
| `PredicateNormalizer` | **[runtime witness]** catalog plus source name selects a mapping; it copies subject/time/confidence/dimensions and emits a derived Observation with a deterministic id. | Representational translation/canonicalization, not evidence examination or semantic warrant production. | **[inference]** unnecessary for source carriage; separate if a consumer lawfully needs developer-attributed normalization. |
| Observation/Fact subject-predicate-value fields | **[runtime witness]** source adapters, users, importers, inference rules, or normalizers supply values. `ObservationIngestor` can copy these fields into Evidence and Fact shapes. | Compact claim representation, indexing, support aggregation, contradiction grouping, explanation lookup, and projection. | **[inference]** a source-populated assertion coordinate could carry raw content, but these consumers still require a declared keying/interpretation policy; that is separate from constitutional relation grammar. |
| `relationship_catalog/core.json` / `RelationshipCatalog` | **[runtime witness]** nine hand-authored relationship definitions map selected predicates to named relationship/kind/object-type rules. | Developer-directed conversion from fact-shaped rows to semantic topology edges. | **[inference]** unnecessary for preserving a source relation proposal; still performs a separate authored projection/classification responsibility. It cannot warrant the projected meaning by identity. |
| `EntityRelationship` | **[runtime witness]** projection supplies `relationship`, one of five `relationship_kind` literals, participants, source Fact id, confidence, and time. | Projected semantic edge optimized for graph consumers. | **[inference]** source relation content can exist without it; the projection adds developer interpretation and a consumer-specific shape. |
| `LegacyEntityRelationship` | **[runtime witness]** directly re-expresses string-valued facts as subject/predicate/object edges with evidence ids. | Compatibility projection that comes closest to treating the predicate field as relation assertion. | **[inference]** witnesses the representational usefulness of the coordinate, not the constitutional name `Predicate` or its warrant. |
| `RelationshipFact` and constants such as `imports` / `defines` | **[runtime witness]** a Python AST adapter or caller-supplied documentation metadata supplies syntactic relationship kinds and evidence text; module comments explicitly limit behavioral/ownership implications. | Source-specific syntactic relation observation. | **[inference]** a general source-populated coordinate could preserve its asserted token/name; parsing and source-specific extraction remain genuinely separate responsibilities. |
| inference rules (`when_predicate` / `then_predicate`) | **[runtime witness]** developers authored antecedents, consequents, confidence, and reasons. | Developer-supplied semantic implication and production of inferred fact-shaped output. | **[inference]** not replaced by source carriage; it is a separate inferential responsibility whose authority and support require their own audit. |
| stale refresh, ranking, audit, and view selectors keyed by predicate | **[runtime witness]** code selects authored behavior based on strings or groups outputs by them. | Consumer policy, indexing, display, or diagnostic classification. | **[inference]** not evidence for a new coordinate. Each consumer may still need stable internal keys after source relation content is preserved separately. |

- **[active law]** The runtime's two large compressions must not be mistaken for
  grammar: a normalized fact-shaped artifact does not confer Fact Standing
  (01.Kinds:9-10), and current Observation intake compresses observation,
  Evidence, claim-field normalization, optional Fact construction, and emission
  without making that sequence universal law (05.Fact:14-18).
- **[inference]** The machinery has been filling at least three different needs:
  (1) a compact slot for assertion content; (2) canonical consumer keys and
  classification policy; and (3) developer-supplied semantic projection. Only
  the first coincides with the constitutional relation-assertion coordinate.

## 6. Chronology

1. **[historical testimony]** Commit `945dfbe` (2026-08-05, “Recover handoff
   decomposition residue (#2271)”) introduces, in one repository-sized recovery
   commit, `observations.py`, `facts.py`, both predicate catalog files, predicate
   normalization, both relationship catalog files, relationship observation,
   and their tests. Each relevant file is absent from that commit's parent.
2. **[historical testimony]** The same commit adds 554 lines of predicate catalog,
   140 lines of catalog implementation, 74 lines of predicate normalization, 68
   lines of relationship catalog, and 71 lines of relationship-catalog code.
   Because these layers arrive together, this checkout supplies no commit-order
   evidence among missing relation distinction, special relation names,
   canonical vocabulary, normalization, and developer meaning.
3. **[historical testimony]** No later commit in the current history modifies the
   eight primary predicate/relationship machinery files inspected here.
4. **[historical testimony]** Later recovery commits address relation grammar and
   meaning warrant—most notably `f5a6050` (relation grammar status) and `6cdc2e2`
   (meaning relation warrant)—but those are recovery work and active law now
   controls their surviving conclusions.

- **[Unknown]** The hypothesized expansion sequence is neither established nor
  contradicted by available file history. The bulk import destroys intra-layer
  chronology.
- **[inference]** The simultaneous shapes are consistent with developers needing
  a place to carry asserted relation content and then adding canonicalization and
  semantic projections. Consistency is not historical proof.
- **[historical testimony]** Structural resemblance to other recovery cases is
  orientation only and supplies no Predicate authority.

## 7. Contradictions, nearby concepts, pressure, and Unknowns

### 7.1 Required non-identities

| Distinction | Finding |
|---|---|
| Predicate != participant | **[active law]** participant identity/role and relation assertion are separate coordinates (01.Kinds:28). |
| Predicate != participant role | **[active law]** role says how a participant participates; relation assertion says what is claimed between/of them (01.Kinds:28). |
| Predicate != relation identity | **[inference]** the relation claim is its own bounded subject; identical assertion content may occur in different claims with different participants, sources, occurrences, or scope (01.Kinds:27-32). |
| Predicate != relation meaning | **[active law]** meaning is a bounded relation form with independent source, attribution, warrant, loss, conflicts, and limits; assertion carriage is not meaning warrant (01.Kinds:30-32). |
| Predicate != Warrant | **[active law]** assertion/content and authority/warrant are separate; a material may carry an assertion without warranting it (01.Kinds:28,32). |
| Predicate != Evidence | **[active law]** Evidence may support a claim but does not become its assertion or truth; exact support binding is separately governed (05.Evidence:15-19). |
| Predicate != Standing | **[active law]** candidate, testimony, supported, established, Unknown, and unresolved standings can apply to the same assertion content (01.Kinds:28,65,69). |
| Predicate != operator/function by notation alone | **[active law]** external syntax, labels, adjacency, and recurrence do not confer structural or semantic meaning (01.External:14-28). |

### 7.2 Pressure around the coordinate

- **[runtime witness]** `Observation` and `Fact` compress assertion content into
  `subject/predicate/value`; the field can appear to own interpretation, source
  testimony, normalized vocabulary, and semantic relation at once.
- **[runtime witness]** `RelationshipCatalog` maps fact predicates into separately
  named relationships and kinds, sometimes changing vocabulary (`group` to
  `member_of`) and sometimes copying it (`runs_on`). That is evidence of
  developer interpretation, not proof that relation naming already lawfully
  owns meaning.
- **[active law]** Relation assertion lawfully owns only what is asserted. It does
  not absorb relation identity, meaning, Evidence, Warrant, Standing, source,
  attribution, participants/roles, or interpretation merely because a compact
  record uses one string (01.Kinds:28-34).
- **[active law]** Comparison can establish exact equality under a declared
  boundary without semantic meaning; identification remains separate, and exact
  token equality is not communicative meaning (08.Communication:20-22).
- **[active law]** Source testimony may carry the asserted content without
  establishing it. Evidence absence does not authorize a stronger negative claim
  (05.Evidence:22-30).
- **[inference]** Removing Predicate while also refusing the existing relation
  assertion would wrongly force relation identity, naming, meaning, comparison,
  participant roles, or Warrant to absorb what is asserted. Active law prevents
  that forced collapse because relation assertion already owns the responsibility.

### 7.3 Contradictions and remaining Unknowns

- **[runtime witness vs active law]** The catalog calls itself “what Seed can
  know” and a PredicateDefinition “one canonical thing Seed can know.” Active law
  denies that authored catalog shape supplies knowledge or kind authority
  (01.Kinds:18-22). The runtime wording is implementation testimony, not law.
- **[runtime witness vs active law]** `Observation` calls itself canonical external
  observation, while the normalizer derives a second canonical Observation from
  an original provider predicate. Which producer supplied semantic interpretation
  remains producer-specific and cannot be settled by the class name.
- **[Unknown]** Whether every current source adapter preserves enough exact source
  material and segmentation to populate a source-derived relation assertion is
  not established. The constitutional permission does not prove runtime Fidelity.
- **[Unknown]** The lawful universal serialization, if any, of relation assertion
  content is not established. Active law expressly rejects a universal mandatory
  field schema.
- **[Unknown]** The full prior report and its evidence path remain unavailable in
  this checkout.

## 8. Reconciliation with the prior report

Because the full artifact could not be retrieved, each item below is reconciled
against the prior findings quoted in the investigation request, not against
unseen text.

| Prior reported finding | Current verification or refinement |
|---|---|
| Active law used predicate in two unconnected senses; identity/distinctness was not established. | **[active law] still holds as a warning.** Current law uses lowercase `predicate` in declared measurement and normalized claim vocabulary (01.External:27-28; 05.Fact:12-18). No clause equates those uses. **[inference] refinement:** the proposed relation dimension is broader than either lexical use and is already named `relation assertion`; it is not a third Predicate kind. |
| Catalog, fields, occurrence counts were not constitutional evidence. | **[active law] verified** by 01.Kinds:18-22 and 01.External:27-28. |
| Catalog was developer-compiled competency. | **[runtime witness] verified:** 76 authored definitions and five mappings lack per-entry constitutional production coordinates. |
| Normalization is a producing act that creates no subject, proof, or support. | **[active law] narrowed:** normalization is a named boundary that canonicalizes an interpreted claim and expressly creates no new subject, proof, or support (05.Fact:10-12). Whether representation formation is always a distinct Act remains Unknown (06.Representations:28); calling all normalization a constitutional Act would overstate current law. |
| External grammar resemblance did not prove borrowing. | **[active law] verified:** external grammar remains attributed and cannot become native grammar through resemblance, recurrence, or convenience (01.External:9-28). |
| Retain/retire remained unresolved. | **[inference] now answered for the constitutional question, not runtime deletion:** Predicate need not be retained as an extra constitutional coordinate because relation assertion already preserves the distinction. This report does not recommend deleting useful implementation machinery. |

- **[inference]** The prior report's two senses and the present hypothesis are not
  identical. “Predicate as measurement classification” and “predicate in
  normalized subject/predicate/value vocabulary” are implementation/normalization
  uses. The hypothesized relation dimension is **broader as a responsibility**—it
  must carry any exact asserted relation content across domains—but active law
  already establishes that responsibility under another name.
- **[Unknown]** Any additional nuance, evidence, or contradiction in the unread
  full report cannot be reconciled here.

## 9. Disposition

### **C. Predicate is reducible to existing relation grammar.**

- **[active law]** The irreducible distinction is real: a relation must preserve
  **what relation is asserted**. Active law already places it in **the relation
  assertion** coordinate (01.Kinds:28), oriented under assertion/content
  (01.Kinds:51-65).
- **[inference]** `Predicate` does not name an additional kind, coordinate, or
  standing. It may be (a) exact source-derived content occupying relation
  assertion, (b) a canonical developer-authored key, (c) a normalization target,
  or (d) shorthand for an interpreted meaning. Those readings must not borrow
  authority from one another.
- **[active law]** Without Predicate, what is asserted remains preservable as an
  exact bounded Representation in relation assertion, while meaning, Warrant,
  Evidence, Standing, identity, source, roles, and limits remain independently
  represented or unresolved.
- **[inference]** No amendment establishing Predicate is warranted. The smallest
  law would be no law at all: renaming the existing coordinate would add
  vocabulary without adding a distinction.

## 10. Smallest next investigation

- **[inference]** If implementation work is later contemplated, the smallest
  investigation is a bounded Fidelity trace of **one** source adapter: source
  bytes/tokens -> source segmentation -> attributed participant Representations ->
  exact relation-assertion Representation -> recorded proposal/testimony. It
  should ask where exactness, provenance, source grammar, and unresolved meaning
  are preserved or lost.
- **[inference]** That investigation should compare the source-derived path with
  any later optional canonicalization and semantic projection, proving that raw
  assertion carriage does not depend on `PredicateCatalog` and that derived
  meaning remains attributed.
- **[active law]** It must not invent a Representation kind, normalize the source
  predicate, define allowable values, infer meaning from notation, or promote the
  proposal to established relation Standing.
- **[Unknown]** Before relying on prior testimony, the missing branch/commit must
  be made locally addressable and the full prior report read.

## What this report does not establish

- **[limitation]** It does not establish `Predicate` as a constitutional kind,
  relation kind registry, canonical vocabulary, or mandatory field.
- **[limitation]** It does not establish that any catalog entry, normalizer,
  relationship mapping, inference rule, Observation, Fact, or edge has semantic
  warrant, Fact Standing, current applicability, or truth.
- **[limitation]** It does not establish meanings or equivalence among `=`, `<`,
  `∈`, `is`, `causes`, `+`, or any source expressions.
- **[limitation]** It does not establish that every infix operator is a relation,
  that every relation is binary, or that participants must be text spans.
- **[limitation]** It does not establish a universal relation serialization or a
  fixed coordinate count.
- **[limitation]** It does not recommend deleting, retaining, or changing runtime
  machinery merely because that machinery is developer-authored.
- **[limitation]** It does not amend runtime or active Book law.
- **[limitation]** It does not claim full reconciliation with an unavailable prior
  report.
