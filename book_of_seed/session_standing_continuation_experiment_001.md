# session Standing continuation: experiment 001

## 1. Executive

The question `#2371` opened and `#2374` narrowed:

```text
prior Standing + occurrences after its as_of_event_id
    ==
replay from zero through the same boundary
```

**Yes, exactly, at every prefix tested.** 1,077 prefix pairs across seven
sessions, then 302 consecutive resumes over a 302-event grammar-book session.
No coordinate disagreed.

**No accumulator failed to seed from the returned Standing.** For the five live
kinds, every coordinate the fold reads is a coordinate the projection returns.

**`event_count` contributes nothing beyond checking.** It is assigned,
incremented, and returned, and never read by any decision.

**This report corrects `#2371`.** That report stated exactly one refusal
depends on session history. There are many. The correction does not change the
result, but it changes why the result holds.

No runtime change is proposed here.

## 2. Method

The runtime was not amended. The projector's source was read, its accumulator
initialisers replaced with values from a prior projected Standing, and its
event loop restricted to occurrences strictly after that Standing's
`as_of_event_id`. Every refusal and every per-event branch is the unmodified
body.

For each session and each pair of prefixes `j <= k`:

```text
prior  = replay(events[0:j])
target = replay(events[0:k])
got    = advance(events[0:k], prior=prior)   seeded, skipping through as_of
compare got with target across every returned coordinate
```

## 3. Result

```text
session         prefix pairs   exact
ordinary                 171     171
empty lines              276     276
non-ASCII                 91      91
code-shaped               91      91
mixed                    406     406
single                    36      36
bare exit                  6       6
                       -----   -----
                       1,077   1,077

grammar-book, 302 events: 302/302 consecutive resumes exact
```

Accumulators that cannot be advanced from returned Standing: **none**.

## 4. The correction to `#2371`

`#2371 §5` stated:

> Every other check is per-event… One check is not.

That is wrong. `project_operator_session_standing` contains **53 refusal
sites**, and many are cross-event: duplicate reference checks for
presentations, comparisons, identifications, applicabilities, admissions,
consumptions and goal standings; agreement checks against recorded testimony;
and this one, which a first attempt at this experiment hit immediately:

```text
if presentation_ref not in presentations:
    raise ValueError("presentation emission without recorded formation: …")
```

**Why the result still holds.** Those checks read *accumulators*, not the
ledger. Every accumulator they read — `presentations`, `comparisons`,
`identifications`, and the rest — is returned in the Standing, so seeding
restores them and the refusals fire exactly as before. `goal_identities`
remains the sole accumulator not returned, and `#2374` established the five
live kinds never reach it.

So `#2371`'s conclusion was right for a reason it did not state: not that there
is one history-dependent refusal, but that all but one read state the
projection already carries.

**A method this invalidates.** An earlier attempt compared
`advance(replay(a), replay(b))` against `replay(a+b)` — projecting the suffix
in isolation and merging. That is unsound here, because a suffix beginning with
an emission does not project alone. Seeding the accumulators, which is what
`#2375`'s task specified, is the correct form and is what §2 does.

## 5. `event_count`

```text
145    event_count = 0
167    event_count += 1
1315   "event_count": event_count
```

Assigned, incremented, returned. Never read.

It is therefore a check on a continuation rather than an input to one: a
fixed-size count that a resumed projection consumed the number of occurrences
expected. That is useful and it is not Standing. Nothing here supports making
it constitutional.

## 6. What this does not establish

**That a continuation should be implemented.** This is an experiment. Whether
advancing session Standing is a responsibility, and whose, is not recovered.

**That the seeded body is a design.** §2 built it by rewriting initialisers to
run the experiment. It proposes no API and no boundary.

**That equality of returned coordinates is equality of Standing.** The
comparison is over the projection's returned mapping. Whether two equal
mappings are the same Standing is a constitutional question this does not
reach.

**Anything about goal-bearing sessions.** All seven sessions contain only the
five live kinds. `goal_identities` is unseeded in §2, so a session recording
`operator.interaction.goal_*` would not be covered, and §4's reasoning about
returned accumulators does not extend to it.

**That resumption is safe against a mutated ledger.** Every session was
append-only and unmodified between projections. A prior Standing whose ledger
changed beneath it was not tested.

**That `event_count` proves exactly-once.** §5 shows it counts. Whether a count
can establish that no applicable occurrence was skipped or consumed twice is
unrecovered, as `#2374` also recorded.
