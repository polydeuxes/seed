# The dormant Applicability boundary: fidelity audit 001

## 1. Executive

Audit of `determine_goal_applicability()` against active law. No runtime
change is proposed, and none should follow from this report alone.

**The headline is not the enum.** It is that the boundary's gating input no
longer exists outside the test suite, so the boundary is unreachable in the
live runtime — and the result it would produce if reached rests on a
coordinate whose constitutional role is unrecovered.

**Two independent fidelity problems, and the second is the larger one.**

```text
1  The result vocabulary cannot express all four applicability standings
   active law permits. Whatever the right answers are, the code can say
   only two things.

2  Most of the determination grammar depends on `consumer_treatment`,
   whose constitutional role is unrecovered and whose only producer is
   test-only developer testimony. For those branches the basis→standing
   mapping is not recoverable at all — and some of them may not belong.
```

An earlier draft of this report gave a full basis-by-basis verdict — "four
sound, three misclassified, one split." **That table is withdrawn for every
branch that depends on `consumer_treatment`.** §3 explains why, and §3.1 gives
what survives.

**The gating input is a test fixture.** `determine_goal_applicability` requires
a `consumer_treatment` relation carrying `attribution == "developer-supplied"`.
`alternative_sources` is passed by **no non-test caller**; the only place a
populated `consumer_treatment` is constructed anywhere in the repository is
`tests/closed_choice_fixture.py:39`. In the live runtime the parameter defaults
to `()`, so no presented alternative is formed at all — which means the
function is not merely limited to one branch, it is **never reached**.

Were it reached with live-shaped input carrying no treatment, it returns —
verified by execution:

```text
determine_goal_applicability(relation, recovery, None, scope=...)
  → ('inapplicable', 'no-consumer-treatment-relation')
```

That is a positive finding of inapplicability resting on the absence of a
coordinate whose constitutional role in this determination is unrecovered. It
asserts a determination that was not made. Whether the right answer there is
`Unknown`, or whether the branch should exist at all, is exactly what §3 says
cannot be settled yet.

So the boundary is not merely dormant. Its only lawful input was determined to
be developer-supplied contamination and excised to a fixture, leaving a careful
validator with nothing valid to validate.

## 2. The standard

`01.Lenses:14`:

> Available upstream material may be evaluated by a consumer-local applicability
> boundary and remain **applicable, inapplicable, Unknown, or conflicting**;
> applicable material does not thereby become admitted. A separate
> consumer-local admission boundary may consume applicability and admission
> evidence to produce **admitted, unadmitted, Unknown, or conflicting** admission
> standing.

Four standings at each of two boundaries. The distinction that matters
throughout this audit is the one the campaign has been recovering all along:

```text
a responsible finding that X does not apply     inapplicable
a coordinate required to decide was not
  established                                   Unknown
material bearing an unresolved conflict         conflicting
```

## 3. Why most bases cannot be classified yet

The cat rule, one level deeper than §5 applies it. Before recovering **which
standing** a basis warrants, establish that the coordinate it inspects has a
constitutional role in this determination at all.

`consumer_treatment` does not have a recovered one. It is absent from active
law as a compound, it is required by the code to be `developer-supplied`, and
its only producer is a test fixture. So:

```text
consumer_treatment is absent
  does NOT establish   Applicability = Unknown
  may instead mean     this coordinate has no constitutional role here
```

And a conflict inside an unrecovered developer-supplied object yields no
constitutional conclusion about Applicability — not `conflicting`, not
`inapplicable`, nothing. The branch may simply not belong.

Splitting the eight bases by what they inspect:

```text
DEPENDENT on consumer_treatment — no standing recoverable yet
  no-consumer-treatment-relation      treatment is None
  treatment-disagreement              treatment fields vs relation fields
  treatment-kind-mismatch             treatment["treatment_kind"]
  treatment-conflicted                treatment["conflicts"]
  consumer-authority-not-established  treatment["consumer_authority"]

INDEPENDENT of consumer_treatment
  role-not-potential-goal             recovery alternative role
  authority-coordinates-not-established   relation["authority_separation"]

MIXED — see 3.2
  scope-mismatch
```

Five of eight are unrecoverable until `consumer_treatment` itself survives a
recovery. That is a stronger result than a mapping table, because it opens the
possibility that some of these bases **should not exist**.

### 3.1 What survives, and how firmly

**`role-not-potential-goal` — inapplicable, and this holds.** It inspects the
presented alternative's role, not the treatment. `potential-goal` is real
active-law vocabulary (15 occurrences). A material whose role is not the role
this consumer takes is a positive mismatch between two things that both exist:
a determination was made and the answer was no. That is what `inapplicable`
means.

**`authority-coordinates-not-established` — not yet auditable.** It reads
`relation["authority_separation"]`, so it does not depend on the treatment. The
draft's reclassification to `Unknown` is plausible under `unresolved != absent`
— but that requires first establishing that those exact Authority coordinates
are **required for this exact Applicability act**, and active law deliberately
makes local coordinates depend on the exact act and proposed use rather than a
universal checklist. Downgraded from a finding to a candidate.

**The result-vocabulary problem survives all of this.** Whatever the right
mapping turns out to be, `01.Lenses:14` permits four standings and the function
can return two. That claim needs no premise about `consumer_treatment`.

### 3.2 A second conflation, in `scope-mismatch`

```python
if treatment["scope"] != scope or relation["representation_scope"] != scope:
    return "inapplicable", "scope-mismatch"
```

Two conjuncts returning one basis. The first inspects the developer-supplied
treatment; the second inspects the meaning relation's own scope and is
independent of it. A caller cannot tell which fired.

The second conjunct may genuinely warrant inapplicability — a relation whose
representation scope disagrees with the consumer's scope is a real mismatch
between two established things. The first cannot be borrowed until the
treatment relation survives. Structurally this is the same defect as §3.3: one
basis carrying two constitutionally different situations.

### 3.3 The basis that conflates two standings

`consumer-authority-not-established` is returned by a single condition covering
two constitutionally different situations:

```python
authority = treatment.get("consumer_authority")
if authority is None or (
    authority.get("standing") != "bounded"
    or authority.get("supports") != [...]
    or authority.get("scope") != {...}
):
    return "inapplicable", "consumer-authority-not-established"
```

```text
authority is None                        no authority coordinate exists
                                         → Unknown

authority exists but standing, supports,  a present authority that does not
or scope disagree                         match → inapplicable, or
                                          conflicting if the disagreement
                                          is a conflict
```

Its name asserts the first reading — "not established" — while its condition
also catches the second. (This basis is treatment-dependent per §3, so the
split is recorded as a structural observation rather than as a mapping.) One basis cannot carry both, and widening the return
enum would not separate them; the condition itself has to split.

## 4. Why widening the enum is not the repair

Recorded because it is the obvious next move and it is wrong, and §3 makes it
more clearly wrong.

Each basis is a determination about **which standing this exact ground
warrants**, and that determination belongs to the boundary, not to a type
signature. `01.Standing.E.1` places input applicability with the exact act
owner. Adding `"conflicting"` and `"unknown"` to the return type would let the
code express right answers without establishing that any mapping is right.

And for five of the eight bases there is no mapping to make yet, because the
coordinate they inspect has no recovered constitutional role. Widening the enum
there would preserve branches that may not belong, in better vocabulary.

The question this boundary actually poses is not how to repair the function. It
is:

```text
What does an exact Responsibility need established
before it may lawfully perform its Act?
```

`determine_goal_applicability` encodes one answer to that question. This audit
establishes that the answer is partly developer-supplied and no longer has a
live producer. Recovering the real answer is the work; repairing the encoding
of the old one is not.

## 5. The chain's vocabulary

Cat-tested, since the chain predates the campaign and a careful encoding is not
a warranted one.

```text
potential-goal        15 occurrences in active law      real
treatment             18 occurrences in active law      real
consumer purpose       6 occurrences in active law      real
consumer treatment     0                                not in active law
goal admission         0                                not as a compound
goal consumption       0                                not as a compound
```

`treatment` is genuine and used in active law in the sense the code intends —
`local-stop treatment`, `presentation-navigation treatment`, `clarification
treatment`, `conflict treatment`, `freshness/expiry treatment`. A treatment is
how something is to be handled.

`goal admission` and `goal consumption` are absent as compounds, but this is
not a finding against them: `01.Lenses:14` establishes admission and
consumption as general consumer-side boundaries, and applying them to a goal is
ordinary composition rather than a new kind.

`consumer_treatment` is the one to watch. The compound is absent from active
law, and more importantly the code requires its `attribution` to be
`"developer-supplied"`. Whether a developer-supplied relation may gate a
constitutional Applicability determination is exactly the question the excision
arc answered elsewhere in this runtime — and the answer given there was to
remove such inputs, which is why this one now lives in a fixture.

## 6. What this audit did not do

It did not follow the chain past Applicability. Admission, consumption, and
goal standing are unexamined. `01.Lenses:14` gives admission four standings and
the implementation was observed to produce `admitted` only, but no basis-level
audit was performed, and that observation should not be cited as a finding.

It did not test whether the checks are *complete* — whether there are grounds
for inapplicability the function fails to check at all.

It did not recover `consumer_treatment`. §3 establishes that its constitutional
role is unrecovered and that five bases depend on it. It does not establish
that the coordinate is illegitimate, only that nothing here warrants using it
to determine Applicability. That recovery is the next piece of work and it
governs whether those five branches survive in any vocabulary.

It did not determine whether `role != "potential-goal"` is the right gate, only
that returning `inapplicable` for it is a coherent use of the standing.

It proposes no code change. The determination of which standing each basis
warrants is owned by that boundary, and this report is evidence for that
determination rather than a substitute for it.

## 7. Method note

The finding that mattered came from asking who *calls* the code, not from
reading it. `determine_goal_applicability` is careful, well-named, and
thoroughly tested; none of that indicates that its gating input still exists.
The fixture-only dependency is invisible from inside the module and invisible
from the test suite, which supplies the missing input on every run.

```text
tests pass                    the fixture provides consumer_treatment
live runtime                  alternative_sources = (), no alternative is
                              formed, the boundary is never reached
```

A test suite that supplies an excised input is not evidence that the input
exists. It is the reason the excision left no visible failure.
