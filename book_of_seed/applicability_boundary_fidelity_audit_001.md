# The dormant Applicability boundary: fidelity audit 001

## 1. Executive

Audit of `determine_goal_applicability()` against active law. No runtime
change is proposed, and none should follow from this report alone.

**The headline is not the enum.** It is that the boundary's gating input no
longer exists outside the test suite, so the boundary is unreachable in the
live runtime — and the result it would produce if reached is one of the
misclassified ones.

```text
Applicability results active law permits   applicable, inapplicable,
                                           Unknown, conflicting
Applicability results the code produces    applicable, inapplicable

of its 8 non-applicable bases:
  4  sound as inapplicable
  3  misclassified — two are Unknown, one is conflicting
  1  conflates Unknown with inapplicable inside a single basis
```

**The gating input is a test fixture.** `determine_goal_applicability` requires
a `consumer_treatment` relation carrying `attribution == "developer-supplied"`.
`alternative_sources` is passed by **no non-test caller**; the only place a
populated `consumer_treatment` is constructed anywhere in the repository is
`tests/closed_choice_fixture.py:39`. In the live runtime the parameter defaults
to `()`, so no presented alternative is formed at all — which means the
function is not merely limited to one branch, it is **never reached**.

Were it reached with live-shaped input carrying no treatment, it returns the
misclassified branch. Verified by execution:

```text
determine_goal_applicability(relation, recovery, None, scope=...)
  → ('inapplicable', 'no-consumer-treatment-relation')
```

Absence of a relation is not a finding of inapplicability. It is Unknown.

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

## 3. Basis-by-basis

```text
basis                                 code   should be        sound?
────────────────────────────────────────────────────────────────────
role-not-potential-goal               inapp  inapplicable     yes
treatment-disagreement                inapp  inapplicable     yes
scope-mismatch                        inapp  inapplicable     yes
treatment-kind-mismatch               inapp  inapplicable     yes
no-consumer-treatment-relation        inapp  Unknown          no
authority-coordinates-not-established inapp  Unknown          no
treatment-conflicted                  inapp  conflicting      no
consumer-authority-not-established    inapp  SPLIT — see 3.1  no
```

**The four sound ones share a shape.** Each is a positive mismatch between two
things that both exist: a role that is not the expected role, a treatment that
concerns a different alternative, a scope that disagrees, a treatment kind that
is not the expected kind. A responsible determination was made and the answer
was no. That is what `inapplicable` means.

**The three misclassified ones share the opposite shape.** In each, something
required was missing or unresolved, and the code converts that into a positive
negative finding:

```text
no-consumer-treatment-relation          treatment is None
authority-coordinates-not-established   separation standings are not
                                        "established"
treatment-conflicted                    treatment carries conflicts
```

The first two are `unresolved != absent`. The third has its own standing in the
clause — `conflicting` — and is instead reported as a determination that the
material does not apply.

### 3.1 The basis that conflates two standings

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
also catches the second. One basis cannot carry both, and widening the return
enum would not separate them; the condition itself has to split.

## 4. Why widening the enum is not the repair

Recorded because it is the obvious next move and it is wrong.

Each of the eight bases is a determination about **which standing this exact
ground warrants**, and that determination belongs to the boundary, not to a
type signature. `01.Standing.E.1` places input applicability with the exact act
owner. Adding `"conflicting"` and `"unknown"` to the return type would let the
code express the right answers without establishing that any particular
mapping is the right one.

Three of the four claims in §3 are also not equally firm. `treatment-conflicted`
→ `conflicting` follows almost directly from the clause. The two Unknown
reclassifications follow from `unresolved != absent`, which is well established
in this campaign but has not been shown to govern *this* boundary by any clause
cited here. That is a gap in this audit, not a settled result.

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

It did not test whether the four sound bases are *complete* — whether there are
grounds for inapplicability the function fails to check at all.

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
