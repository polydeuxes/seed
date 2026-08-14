# Responsibility spine

Translation testimony. **No entry here carries constitutional Authority**, and
nothing here is citable as law — see [README](README.md). Where this file names
a clause, the clause is the authority and this is the gloss.

Rosetta has no independent constitutional topology. It follows the Book's
Responsibility spine and supplies ordinary-English glosses for the coordinates
and relations encountered there.

```text
Responsibility
    ├── responsible boundary
    ├── subject or material
    ├── exact Act
    ├── Authority / Evidence
    ├── purpose / Scope / locality
    ├── inputs
    │   ├── source / provenance
    │   ├── Applicability
    │   └── Admission, where required
    ├── Act occurrence
    ├── production
    │   └── result / Assertion
    ├── Standing
    └── movement / neighboring responsibilities
```

The Book defines that spine. Runtime occurrences instantiate it. Rosetta keeps
the same orientation while translating the dense parts into ordinary English.

Examination and Presentation are directional views across this spine, not
structural roots:

```text
world  ── Examination gloss ──>  Responsibility spine
world  <─ Presentation gloss ──  Responsibility spine
```

The directions are not mirror images. Presentation maps to bounded formation
and separately evidenced emission. Examination compresses several inward
responsibilities and has no single Book clause. Emission is not a third view;
it is an exact outward occurrence distinct from formation.

The following shorthands hang from exact parts of the spine rather than naming
additional branches.

### Implementation witnesses

These anchors show current concrete instantiations; they do not define the
grammar:

```text
Responsibility / Act / occurrence
    seed_runtime/byte_measurement.py::record_byte_count_layer
    seed_runtime/byte_measurement.py::record_adjacent_byte_pair_count_layer

production relation / Evidence
    seed_runtime/production_evidence.py::_record_production_evidence

Assertion / occurrence-bound recovery
    seed_runtime/byte_measurement.py::RecordedByteAssertion
    seed_runtime/byte_measurement.py::assertions_of_recorded_byte_measurement

locality movement
    seed_runtime/byte_measurement.py::_move_byte_assertion_to_locality

Applicability
    seed_runtime/byte_measurement.py::get_recorded_pair_input_applicability

Provenance path validation
    seed_runtime/operator_ingress_addressable_material.py::form_operator_ingress_addressable_material
```

## Producer

`Producer` is ordinary shorthand for the side from which a result comes. In
Seed grammar it expands to an exact Responsibility, Act, Act occurrence,
production relation, result Assertion, Evidence, Authority, provenance, and
locality. It names no additional participant or constitutional coordinate.

## Consumer

`Consumer` is ordinary shorthand for the side at which material may
participate in another Act. In Seed grammar it expands to the exact locality,
Responsibility, Act, purpose, Applicability, warranted participation or
input-to-result support, and Act occurrence. It names no additional participant or
constitutional coordinate.

## Uptake

`Uptake` is ordinary shorthand for available material later participating in
another bounded Act. In Seed grammar it expands to locality movement or
availability, Applicability, Admission where required, exact purpose,
warranted participation or input-to-result support, and the Act occurrence. It names no
relation family or additional occurrence.

## Handoff

`Handoff` is ordinary shorthand for movement between localities or for a
separately established change in Responsibility or Authority. Movement does
not imply that one participant gave material to another. The exact movement,
Responsibility assignment, or Authority transition must be named instead.

## Consumption

`Consumption` is ordinary shorthand for material participating as input in an
exact Act. Material is not depleted or transferred by that participation.
Availability, Applicability, Admission where required, the input occurrence,
and the exact Act occurrence carry the distinctions; the shorthand adds no
stage or coordinate.

## Reliance

`Reliance` is ordinary shorthand for saying that an exact input supports an
exact result. In Seed grammar that is a relation Assertion with its own
participants, Evidence, Authority, Scope, occurrence, limits, Unknowns, and
Standing. Input participation does not establish that support relation.

## Claim

`Claim` is ordinary shorthand for the content of an Assertion viewed apart
from the exact representation carrying it. Seed grammar keeps the Assertion as
the subject. Equal content across two Assertions requires an established
relation; the shorthand creates no shared proposition object.

## Fact

`Fact` is ordinary shorthand for an Assertion described through established,
bounded Standing. It is not a species above Assertion and does not add an
identity, Responsibility, Act, occurrence, Evidence, Authority, Scope, or
Standing coordinate. Stronger Standing does not turn an Assertion into another
constitutional kind.

## Artifact

`Artifact` is ordinary shorthand for a representation, record, Assertion, or
result preserved by an exact occurrence. The exact kind must be named because
each carries different identity, Evidence, Authority, Scope, and Standing.
Artifact adds no container subject or constitutional coordinate.

## Lineage

`Lineage` is ordinary shorthand for an addressable representation of where
material came through. In Seed grammar it belongs beneath Provenance and may be
represented by ordered source, occurrence, production, or preservation
references. The representation helps an exact Act validate claimed provenance;
it establishes no separate subject, Responsibility, Act, Standing, causation,
production occurrence, or Applicability.

## Purpose

`Purpose` is ordinary shorthand for why an exact Responsibility/Act has its
particular subject, result boundary, Scope, locality, Authority, and
Constraints. It adds no coordinate when those remain unchanged.

## Meaning

`Meaning` is ordinary shorthand for an exact warranted relation such as X
representing or identifying Y. The relation carries its own participants,
Assertion, Evidence, Authority, Scope, locality, occurrence, limits, and
Standing; the shorthand adds no relation kind.

## Capability, Gap, Goal, and Demand

`Capability` glosses exact Responsibility/Act/Authority/Constraint and Evidence
about what may occur. `Gap` glosses a bounded Compare or distinction between
current Standing and an exact reference condition. `Goal` glosses
locality-bound material or Standing concerning a desired result. `Demand`
glosses that an exact Responsibility/Act/result boundary remains unmet. None
adds an object, occurrence, or Standing by name.

## Testimony

`Testimony` is ordinary shorthand for asserted content carried with source
coordinates. Seed grammar preserves the source identity or role, material
origin, source occurrence where evidenced, provenance, Evidence, Scope,
Authority limits, locality, conflicts, Unknowns, and surviving limits. Those
coordinates do not establish that the named source asserted the content.

## Attribution

`Attribution` is ordinary shorthand for a claimed or warranted relation between
an Assertion and source coordinates. A source label or mechanically observed
material origin does not establish that relation. The relation is another
Assertion with its own Evidence, Warrant, occurrence, and Standing.

## Artifact

`Artifact` is ordinary shorthand for a durably represented result, Assertion,
record, or other material. Its exact kind, occurrence, Evidence, Standing, and
preservation boundary must be named instead.

## Constructor

`Constructor` is ordinary implementation shorthand for code that can form a
representation or result. Invocation may participate in an exact production
Act, but public reachability, direct instantiation, constructability, or the
returned shape establishes none of Responsibility, Authority, Act occurrence,
production occurrence, production Evidence, or Standing.

## Warrant

`Warrant` is ordinary shorthand for why Seed is entitled to carry particular
Standing. Seed grammar represents the exact relation Assertion connecting
Evidence, Authority, Scope, provenance, and limits to the supported Assertion,
together with that relation's responsible Act, occurrence, and Standing. The
shorthand adds no subject or coordinate.

## Projection and View

`Projection` and `View` are ordinary lenses over bounded formation toward
emission. In runtime they may also name mechanical replay, selection, caching,
or formatting. Seed grammar names the source material, formation
Responsibility/Act/occurrence, exact result boundary, preserved loss and
limits, representation, emission occurrence, and later Applicability. Neither
lens adds a constitutional subject.

---

## Presentation

```text
role            outward view across the Responsibility spine
book standing   none as a responsibility. `presentation` appears in active law
                as rendering vocabulary, as closed-choice machinery, and as an
                ordinary verb
maps to         06.Representations (forming) · 08.Emission (sending)
```

### What a person means by it

What Seed shows you. You typed something, Seed answered, and the answer you are
looking at is the Presentation.

### What Seed is actually doing

Two established things, in order, owned separately.

```text
a responsible occurrence forms a bounded representation
    from exact source material, for a declared purpose
        ↓
that representation carries only the Standing warranted by
    its source, responsible formation, purpose, Scope, Evidence,
    provenance, Authority limits, conflicts, limits, and
    responsibly established Unknowns
        ↓
emission occurs, separately, as its own occurrence
```

The middle line is the whole of what people mean when they say Seed should be
honest. It is not a disposition or an intention. It is a bound on what the thing
you are looking at is permitted to carry.

This is why a fluent answer can be a failure and an awkward one can be correct.
If Seed has met a word twice and says something that would only be warranted by
meeting it ten thousand times, the Presentation carries standing its formation
does not supply — regardless of how well it reads.

### What it must not become

`presentation` is a crowded word in the repository, and most of what it names
is not this.

```text
not closed-choice machinery       presented alternatives are bounded test and
                                  interaction representations, not this view
not session Standing              a current implementation projects Standing
                                  "for a session"; that is not what a person
                                  sees, and no clause warrants it
not Emission                      forming and sending are separate occurrences
not receipt                       that you saw it is not part of Seed's act
not a UI                          rendering is a surface over the formation
                                  payload, and a rendered label is expressly
                                  not the represented meaning
```

### Where the mapping is Unknown

`06.Representations` closes with: *"Whether forming a representation names an
Act distinct from the exact Act that forms it remains **Unknown** unless
separately established."*

So the Book declines to say that forming-outward is its own Act. This view is a
human word for a direction, and does not settle that question.

---

## Examination

```text
role            inward view across the Responsibility spine
book standing   none. `examination` was retired from active law 2026-08-03 and
                stands at zero occurrences; see retired-vocabulary.md
maps to         no single clause. several bounded responsibilities
```

### What a person means by it

Seed encountering something from outside and coming to hold it — a book, a line
you typed, a file, a program's output. The word covers the whole inward trip
from *there is something out there* to *Seed has something it can work with*.

### What Seed is actually doing

Not one thing, and this is the honest part of the entry.

```text
material arrives and is preserved as an occurrence, attributed to
    its origin — operator, this Seed, or system
        ↓
external material may become addressable as source-attributed material
    without becoming constitutional grammar          (01.External.B)
        ↓
a declared measurement may produce bounded findings — equality, count,
    recurrence, prefix occurrence, a declared predicate, adjacency —
    disclosing what was measured, the rule of sameness, and the bounded
    scope                                            (01.External:28)
        ↓
none of that establishes meaning                     (01.External.E)
```

Four separate boundaries, no single act joining them. A person saying
"Seed examined the book" is compressing all of it, which is what ordinary
English is for and what the Book cannot afford.

### Why this word is not in the Book

It was, and it was removed. The chapter now called Inquiry was
`inquiry-and-examination` until the noun came out on 2026-08-03, because it had
compressed several responsibilities — comparison, applicability determination,
and relation establishment among them — into one word that sounded like an act.

That is precisely the property that makes it a useful view here and a bad clause
there. As a view it says *this direction, all of it*. As law it would claim
there is one act where there are several.

The verb survives in active law, with applicability as the thing doing the
examining. The noun does not.

### What it must not become

```text
not an Act                    nothing performs an Examination
not a stage                   the responsibilities beneath it have no
                              required order
not meaning-making            measurement and recurrence establish no
                              meaning, which is a titled clause
not admission                 material arriving is not material admitted
not a return path to law      the noun is retired; Rosetta does not restore its
                              constitutional Standing
```

### Where the mapping is Unknown

Whether the inward direction has a single responsibility at all. The outward
direction has one clause that names the whole of it; the inward direction has
four boundaries and no clause joining them.

That may be a gap, or it may be the true shape — one mouth and many senses is
an ordinary way for an organism to be built. Nothing recovered so far decides
it, and this entry does not either.

---

## On using these words

They are for talking to people, including ourselves at speed. They carry no
standing, they name no act, and an argument that turns on one of them has not
yet reached the grammar.

The test that keeps them honest: **if a sentence about Seed would change
meaning when the Rosetta word is replaced by the clauses beneath it, the sentence
was resting on the English.**
