# `the relation assertion`: investigation 001

Findings only. No runtime or Book amendment.

## Executive

**Active law names the coordinate and establishes almost nothing else about
it.** `relation assertion` occurs exactly twice, both times inside a list of
dimensions a relation claim must preserve or mark Unknown. No clause defines
its content, names what may occupy it, or says what act places content there.

**Occupancy alone establishes nothing, and law says so directly.**
`01.Standing.D` refuses relation standing to co-presence. Three preserved
representations sitting in three slots are three preserved representations.

**Six distinct acts stand between source material and established relation
standing, and law names all six.** None absorbs the others.

**The gap between `#2379` and `#2380` is one join, and it is exact.**
`01.External:15` licenses forming a **relation proposal**. `01.Kinds:28`
requires a **relation claim or standing** to preserve the relation assertion.
**No clause relates those two terms.** Each occurs once, in a different
chapter.

**Both prior reports were right about different halves.** `#2379` established
that forming the material is licensed. `#2380` established that occupying the
coordinate with it is not. The disagreement dissolves at the join above.

## 1. What active law establishes

**[active law]** `01.Kinds:28` lists it among the dimensions a relation claim or
standing must preserve "**or its explicit Unknown or unresolved standing**":
participants and roles, **the relation assertion**, evidence standing, scope,
producer, consumer and purpose, authority, occurrence, conflicts, limits.

**[active law]** `01.Kinds:30` repeats it for the meaning-relation form.

**[active law]** Those two occurrences are the whole of it. `assertion` alone
is nowhere defined.

**[active law]** `01.Kinds:28` gives the ladder the coordinate sits inside:
"Candidate relation, relation testimony, and evidence-supported or established
relation standing remain distinct."

**[active law]** And the identity rule: "Later evidence may revise relation
standing **without mutating participant identity**."

**[Unknown]** What the coordinate holds. What form its content takes. Whether
its content is revisable, and under what.

## 2. What may lawfully occupy it

**[active law] No clause states what may occupy any relation coordinate.**
A search for a clause constraining what participants, roles, or the relation
assertion may be returns nothing.

**[active law]** What is licensed is the *material*, not the occupancy:

```text
06.Representations:12  "Seed may form a bounded representation from exact
                        source material for a declared purpose."
06.Representations:14  it carries only the Standing warranted by its source,
                        formation, purpose, Scope, Evidence, provenance,
                        Authority limits, conflicts, limits, Unknowns
01.External:15         a bounded translation may form "an attributed,
                        Seed-addressable translated representation, term,
                        assertion, claim proposal, or relation proposal"
01.Kinds:32            "Material may carry or propose the assertion that X
                        identifies, represents, or expresses Y without
                        warranting that meaning relation."
```

**[inference]** So a representation formed from `"is"` exists lawfully, is
attributed, and carries no meaning. Whether it may be *the content of* a
relation claim's relation-assertion coordinate is §6.

**Stress tests.** For each, the material may be preserved and represented; the
coordinate's occupancy is the same open question in all five:

```text
"A noun is a word"    A noun  | is     | a word
"X causes Y"          X       | causes | Y
"2 + 2 = 4"           2 + 2   | =      | 4
"F = ma"              F       | =      | ma
"x < y"               x       | <      | y
```

**[active law]** Nothing in that arrangement establishes the arrangement.
`01.Standing.D`: "Co-presence or multiplicity does not by itself establish
membership, collection standing, **relation**, topology, ordering, selection,
priority, focus, shared purpose, or higher-order identity."

The middle column is not the relation assertion because it sits in the middle.
Position, adjacency, and ordinary English are not warrant, and this report
draws no semantics from them.

## 3. The acts, kept apart

**[active law]** Six, each separately named:

```text
preserving source material    external material remains attributed source
                              grammar; 01.External:15
forming a Representation      06.Representations:12, for a declared purpose
forming a relation proposal   01.External:15, one item in the list a bounded
                              translation may form
carrying attributed testimony 01.Kinds:32, material may carry or propose an
                              assertion without warranting it
Compare                       consumes an applicable baseline or authorized
                              comparison boundary and a measurement within a
                              declared purpose and scope
establishing relation         01.Kinds:32, "A responsible occurrence warrants
Standing                      only the bounded relation supported by
                              claim-appropriate authority, evidence, scope,
                              provenance, conflicts, loss, and preserved
                              Unknowns"
```

**[active law]** None absorbs another. `01.External:15` keeps them apart from
the consumer side too: "Applicability is not admission, admission is not
consumption, and consumption is not a comparison or interpretation finding."

**[Unknown] Which of them places content into the coordinate.** Formation
produces a representation. Translation produces a proposal. A responsible
occurrence warrants a relation. No clause says which one populates a dimension,
or whether populating is an act at all rather than a property of the claim.

## 4. Standing from occupancy alone

**[active law] None.**

```text
rung                        established by occupancy?
exact source carriage       no -- carriage is the material's own standing
                            (01.External:15), unchanged by where it sits
candidate relation          no -- 01.Standing.D refuses relation standing to
                            co-presence; a candidate needs its own subject
attributed testimony        no -- 01.Kinds:32, attribution "does not by itself
                            establish what the subject means"
evidence-supported relation no -- 01.Kinds:28 keeps this rung distinct
established relation        no -- 01.Kinds:32 requires a responsible occurrence
                            and claim-appropriate support
```

**[active law]** `01.Kinds:32` also bounds what the warrant does reach: it
"establishes neither Y's truth nor its applicability, admission, goal standing,
act occurrence, or completion."

**[inference]** Carriage does not become warrant at any rung. The ladder is
climbed by occurrences, not by filling slots.

## 5. Implementation testimony

**[runtime witness]** The runtime carried a `relation_assertion` payload
coordinate for one day. Introduced 2026-07-29 in `#2074`, deleted 2026-07-30 in
`#2107` as "disconnected operator ingress probe scaffold".

What it held:

```python
relation_assertion: str = "expresses"
attribution: str = "Seed application developer declaration"
```

**[runtime witness]** The only occupancy of this coordinate the repository has
ever contained was a developer-declared constant, and the adjacent field says
so in plain words. That is testimony about who was supplying the content, not
about what may.

**[runtime witness]** `predicate_catalog/core.json` — 76 authored rows, five
fields, no source, evidence, provenance, or production boundary.
`relationship_catalog/core.json` — 9 rows carrying `derived_from_predicates`,
a second authored layer on the first.

**[historical testimony]** Both catalogues predate every piece of relation
grammar in active law by about seven weeks (`#2380 §6`). They are not evidence
of a grammatical vacancy; they are evidence of what was built before the
grammar existed.

**[inference]** All three shapes answer the same question — *what is asserted
between these participants* — and all three answer it by developer declaration.
That is consistent testimony about the coordinate being real and unowned. It
establishes neither.

## 6. Reconciling `#2379` and `#2380`

**The exact clause boundary:**

```text
LICENSED
01.External:15   a bounded translation may form a relation proposal
06.Representations:12  Seed may form a bounded representation from exact
                       source material for a declared purpose
01.Kinds:32      material may carry or propose an assertion without warrant

REQUIRED
01.Kinds:28      a relation CLAIM or STANDING must preserve the relation
                 assertion, or its explicit Unknown

MISSING
                 no clause relates "relation proposal" to "relation claim",
                 "candidate relation", or "relation standing"
```

**[active law]** `relation proposal` occurs once, at `01.External:15`.
`candidate relation` occurs once, at `01.Kinds:28`. **No clause connects
them.**

So the hinge is precise:

- **If a relation proposal is a relation claim**, then `01.Kinds:28` governs it,
  its dimensions must be preserved or marked Unknown, and forming one from
  external material necessarily populates the relation assertion. Occupancy is
  licensed. **`#2379` is warranted.**
- **If it is something weaker**, it has no stated dimensions at all, and nothing
  says a representation may occupy a relation claim's coordinate. **`#2380` is
  warranted.**

**Verdict on the disagreement.** Both reports were right about different halves,
and neither established the join. `#2379`'s §3.1 is correct as active law —
forming the material is licensed — and it labelled its assembled shape
`[inference]`, which was honest. `#2380` was correct that no clause licenses
occupancy, and overstated by implying `#2379` had claimed otherwise as law.

**[inference]** The disagreement was never about the clauses. It was about
whether "may form a relation proposal" entails "may populate a relation claim".
That entailment is exactly what is unrecovered.

## 7. Answers

```text
what may occupy relation assertion
    Unrecovered. No clause constrains the content of any relation
    coordinate. An exact source-derived Representation is lawfully
    formable (06.Representations:12) and lawfully carries no meaning
    (01.Kinds:32), so nothing disqualifies it -- but nothing licenses it
    either, pending §6's join.

who or what puts it there
    Unrecovered. Six acts are separately named (§3); none is stated to
    populate a dimension. The only runtime occupancy was a developer
    declaration that labelled itself one.

what Standing occupancy establishes
    Nothing, at any rung. 01.Standing.D refuses relation standing to
    co-presence; 01.Kinds:32 requires a responsible occurrence for
    warrant. This is the one question active law answers cleanly.

what remains Unknown
    the coordinate's content and form; whether populating is an act;
    whether a relation proposal is a relation claim; whether the
    coordinate's content is revisable given that participant identity
    is not
```

## 8. The smallest bridge

**One join, and it is a relation between two existing terms rather than a new
one:**

```text
whether a relation proposal is a relation claim at the candidate rung,
and therefore whether 01.Kinds:28's dimensions apply to it
```

That single relation would make `#2379`'s assembled shape lawful without any
new coordinate, without naming Predicate, and without constraining what may
occupy the relation assertion — which would remain Unknown and free for source
material to fill.

**[inference]** It is the smallest thing that would open the grammar-source
road. It is not proposed here.

## What this does not establish

**That a representation may occupy the coordinate.** §6 is the finding: the
entailment is unrecovered in both directions.

**That the six acts are the complete set.** §3 lists those active law names.

**That the middle term of the stress tests is a relation assertion.** §2
refuses that inference explicitly.

**That the catalogues were filling this coordinate.** §5 records that all three
shapes answer the same question by developer declaration. Intent is not
recoverable from artifacts.

**That `#2379` or `#2380` was wrong.** §6 finds both correct about different
halves.

**Independence.** `#2380` was written by this session. §6's reading of it is
self-review; §6's reading of `#2379` is not.
