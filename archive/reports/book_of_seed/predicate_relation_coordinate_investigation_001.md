# Predicate as a relation coordinate: investigation 001

Findings only. No runtime or Book amendment.

**Independence limit, stated first.** §8 reconciles against
`predicate_cat_test_001.md`, which this session wrote. That section is
self-review, not an independent check, and should be weighed accordingly. §1-§7
were completed before rereading it.

## 1. The relation-coordinate inventory

**Active law.** `01.Kinds:28`:

> A relation is its own bounded claim subject. A relation claim or standing
> must preserve each applicable constitutional dimension, or its explicit
> Unknown or unresolved standing, including **participants and roles, the
> relation assertion, evidence standing, scope, producer, consumer and purpose,
> authority, occurrence, conflicts, and limits**.

`01.Kinds:30` gives the meaning-relation form: participants and roles, the
relation assertion, source and attribution, producer and occurrence, evidence,
scope, consumer and purpose, provenance, authority, known loss, conflicts,
limits, Unknowns.

```text
coordinate              distinction it carries
participants and roles  who or what stands in the relation, and as what
the relation assertion  named; content undefined -- see below
evidence standing       what supports the claim, at what strength
scope                   where the claim holds
producer                whose occurrence produced it
consumer and purpose    for whom, toward what
authority               under what warrant
occurrence              that a responsible act happened
conflicts / limits      what disagrees, what bounds it
```

**The vacancy question.** Given participants and every other coordinate, where
is *what relation is being asserted* represented?

**A coordinate already occupies that position by name: `the relation
assertion`.** It is not vacant.

**But its content is undefined.** `relation assertion` occurs exactly twice in
active law, both times inside these two lists. No clause states what it holds,
what may occupy it, what produces it, or what standing its occupancy
establishes. `assertion` alone is nowhere defined either.

So the finding is not a vacancy. It is a **named coordinate with no recovered
content** — which is a different defect and admits different repairs.

## 2. Cat test

```text
reading                        verdict
Predicate as developer         developer-compiled competency. 76 authored rows
  catalog                      in predicate_catalog/core.json, five fields
                               each, no source, evidence, provenance, scope,
                               or production boundary. 01.Kinds:19 denies an
                               inventory row production authority without
                               exactly those.
Predicate as canonical         same artifact, same verdict. "Canonical" is
  vocabulary                   asserted by the file, not established.
Predicate as normalization     ordinary implementation term. 05.Testimony:12
  target                       names normalization as the act that
                               canonicalises into subject/predicate/value, and
                               denies in the same sentence that it creates a
                               subject, proves the claim, or supplies support.
Predicate as interpreted       not Predicate. 01.Kinds:30 makes meaning its own
  meaning                      bounded relation form with its own coordinates;
                               01.Kinds:32 denies that carrying an assertion
                               warrants the meaning relation.
Predicate as relation          Unknown. No clause names a relation kind
  kind or name                 coordinate. 01.Kinds:19 denies that a kind label
                               closes the ontology or supplies authority.
Predicate as a grammatical     Unknown, and displaced. The position exists and
  relation coordinate          is already named `the relation assertion`; no
                               clause relates `predicate` to it.
```

**The decisive negative.** No sentence in active law contains both a relation
form and `predicate`. Relation grammar and claim-triple grammar are two
vocabularies the Book never connects.

**Elimination test.** If `predicate` is removed entirely, what becomes
impossible to preserve?

Within *relation* grammar: nothing. `the relation assertion` holds the
position, undefined either way. Within *claim* grammar: the middle term of
`subject, predicate, value` at `05.Testimony:12`, which no other coordinate
names. So the word is load-bearing where it lives, and absent from where the
hypothesis places it.

## 3. Source-populated occupancy

**Permitted, so far as active law reaches.**

`01.Kinds:28` requires each dimension "**or its explicit Unknown or unresolved
standing**". Participants, roles, and the relation assertion are inside that
disjunction. Nothing requires an interpreted occupant.

`01.External:15` states what a bounded translation may form: "an attributed,
Seed-addressable translated representation, term, assertion, **claim proposal,
or relation proposal**." A relation proposal from external material is
explicitly available, and `01.External:34` keeps it from becoming warrant.

`01.Kinds:28` closes with "Later evidence may revise relation standing
**without mutating participant identity**." An exact source-derived
representation is a *better* participant identity than an interpreted subject,
because bytes do not shift when interpretation improves; interpretation attaches
separately as `01.Kinds:30`'s meaning relation.

So for `"A noun is a word"`, this is expressible without amendment:

```text
participant            exact representation "A noun"
relation assertion     exact representation "is"
participant            exact representation "a word"
roles                  Unknown
meanings               Unknown
standing               candidate relation only
```

**What is not established** is that occupying the coordinate *with a
representation* is lawful, because the coordinate's content is undefined (§1).
Nothing forbids it; nothing licenses it. **Zero clauses in active law contain
both a relation form and a representation form.**

## 4. Cross-domain stress

The same position is unfilled in each domain, and the position is the same one:

```text
"A noun is a word"     A noun    | is    | a word
"X causes Y"           X         | causes| Y
"2 + 2 = 4"            2 + 2     | =     | 4
"F = ma"               F         | =     | ma
"x < y"                x         | <     | y
```

`=`, `<`, `is`, `causes` can each occupy one coordinate as exact source-derived
representations without shared meaning.

**Occupancy is not equivalence, and this report does not claim it.** `05.Evidence:30`
lists similarity and co-occurrence among the things that establish no relation.
That `=` and `is` sit in one slot establishes nothing about whether they are the
same kind of thing.

**The `+`/`=` distinction is real and is not settled here.** In `x + y = z`,
`=` occupies the position between two terms; `+` composes one of those terms.
Reading both as the same coordinate would require warrant no clause supplies.
Recorded as a limit, not resolved.

## 5. Runtime and history testimony

```text
artifact                     who supplied      evidence   responsibility
predicate_catalog/core.json  developers        none       name the things Seed
  76 rows, 5 fields                                       can know
RelationshipCatalog          developers        none       "how entities connect
  9 rows, derived_from_                                   to each other"
  predicates
predicate normalizers        developers        none       map provider terms to
  canonical_predicate                                     canonical ones
relation_assertion           implementers      n/a        deleted 2026-07-30
  payload coordinate                                      as "disconnected
                                                          probe scaffold"
```

`RelationshipDefinition` carries `derived_from_predicates: list[str]` — a second
authored vocabulary layered on the first. Two compiled layers, neither with a
production boundary.

**Not a deletion recommendation.** Each was filling something. What that
something is cannot be recovered from the artifacts themselves, which is the
finding.

## 6. Chronology

```text
2026-06-03  predicate catalog normalization added to the runtime
2026-06-04  relationship catalog added, deriving from predicates
2026-07-21  subject/predicate/value enters active law
2026-07-25  relation coordinates, and `the relation assertion`, enter law
2026-07-29  relation_assertion appears as a runtime payload coordinate
2026-07-30  deleted as "disconnected operator ingress probe scaffold"
```

**The expansion hypothesis is refuted for the runtime.** The authored
catalogues predate every piece of relation grammar by about seven weeks, and
predate the claim triple in law by six. They cannot have grown to fill a
vacancy in a grammar that did not yet exist.

They may still have been filling a vacancy in the *developers' understanding*.
That is not recoverable from chronology and is not claimed.

**One inversion worth recording.** The runtime carried `relation_assertion` for
a single day. The coordinate active law names survived one commit; the
vocabulary active law never connects to relations survived and grew.

## 7. Distinctions

```text
Predicate != participant       the position is between or of them
Predicate != participant role  role qualifies a participant, not the assertion
Predicate != relation identity 01.Kinds:28 revises standing without mutating
                               participant identity; identity is not content
Predicate != relation meaning  01.Kinds:30 makes meaning its own relation form
Predicate != Warrant           01.Kinds:32: carriage is not warrant
Predicate != Evidence          evidence standing is a separate coordinate
Predicate != Standing          standing is what an act establishes about it
Predicate != operator          unsettled; see §4
```

All hold, and none of them establishes that Predicate names anything, since
`the relation assertion` satisfies every one of these distinctions too.

## 8. Reconciliation with `predicate_cat_test_001.md`

**Self-review; see the note at the head of this report.**

**Still holds, re-verified.** Two senses of `predicate` in active law, unrelated
by any clause. The catalogue is not constitutional evidence. Normalization is a
named act whose clause denies it establishes anything. Resemblance to an
external corpus does not establish borrowing.

**Left Unknown there, still Unknown.** Whether the two senses are one thing.
Whether Predicate should be retained or retired.

**Answerable now, and it could not have been.** That report never examined
relation grammar. It compared `predicate` against *measurement*. The present
question — whether Predicate names the missing relation coordinate — is
answered by `01.Kinds:28` naming `the relation assertion`, which that report
never cites.

**Narrowed.** That report treated `predicate` as possibly two senses. There are
two senses *and* a third position it does not occupy. The proposed dimension is
**distinct from both** of its senses: not the claim triple's middle slot, which
lives in claim grammar and is connected to nothing relational, and not the
declared-measurement test at `01.External:28`.

## 9. Disposition

**C, with a qualification that matters.**

*Predicate is reducible to existing relation grammar* — `what relation is
asserted` is already preserved, by name, at `01.Kinds:28` and `:30`, as **the
relation assertion**. There is no vacancy for a ninth coordinate to fill.

The qualification: that coordinate's **content is entirely unrecovered**. Named
twice, defined never. So the honest disposition is C over the *position* and
**B over the content** — a real distinction, named in law, whose constitutional
kind and permitted occupants active law does not establish.

Nothing here supports introducing `Predicate` as a coordinate. Doing so would
add a second name for a position law already names, which is the
naming-does-not-supply-the-owner pattern.

## 10. Smallest next investigation

Not about Predicate.

```text
What may occupy `the relation assertion`, and what act puts it there?
```

That is the actual unrecovered thing, it is one clause wide, and §3 shows the
answer probably permits an exact source-derived representation. If it does, the
grammar-source road is open without any new coordinate.

## What this does not establish

**That the two senses of `predicate` are unrelated.** §2 records that no clause
relates them, which is absence of a relating clause.

**That `the relation assertion` means what its name suggests.** §1 is the
finding: it is named and undefined. Reading its content off its name is the
error this report is otherwise warning against.

**That a representation may lawfully occupy it.** §3 establishes that nothing
forbids it and that the Unknown disjunction admits it. No clause licenses it.

**That the catalogues should be removed.** §5 declines that.

**That developers did not face a real gap.** §6 refutes the chronology only.

**That `+` and `=` are different constitutional kinds.** §4 records the
question as open.

**Independence.** §8 is self-review.
