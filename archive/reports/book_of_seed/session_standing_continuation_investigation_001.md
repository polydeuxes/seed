# session Standing continuation: investigation 001

## 1. Executive

`#2370` removed the whole-workspace rebuild from live ingress. The console is
still quadratic, and the remaining term is now measured: whenever session
Standing is projected, it is rebuilt from the first event of the session.

**The continuation boundary already exists.** The projection records
`as_of_event_id`, `consumed_event_ids`, and `event_count`. It already answers
"I include through Event X".

**The projection is a forward fold, verified rather than assumed.** Across
every prefix of a 27-event session, projections are deterministic and
`consumed_event_ids` is append-only. Nothing at step *k* depends on an event
after *k*.

**Exactly one refusal depends on session history**, and it is guarded by the
one accumulator the returned Standing does not carry.

**That accumulator is empty on every live path today**, so a continuation
seeded from the returned Standing would be correct now and would silently lose
a refusal later. That is the finding this report exists to record.

No runtime change is proposed here.

## 2. What is consumed now

`project_operator_session_standing` takes a ledger and rebuilds from zero:

```text
for event in ledger.list(workspace_id):
    skip if event.session_id != session_id
    skip if kind is not operator.{ingress,presentation,exchange,interaction}.*
    raise if kind not in _SUPPORTED_KINDS
    accumulate
```

No prior Standing is consumed. There is no parameter for one.

Twenty-three accumulators are built by that pass, from `attempts` and
`preserved_ingress_occurrences` through the goal coordinates to `known_loss`,
`unknowns`, and `conflicts`.

## 3. The cost shape

One call, measured against grammar-book material through the console:

```text
lines   events   one call   per event
   50      252      0.5ms      1.94us
  100      502      1.0ms      1.99us
  200     1002      2.0ms      1.95us
  400     2002      4.7ms      2.33us
  800     4002     10.5ms      2.62us
```

Per-call cost is linear in session events. The console calls it about twice per
line, so the session total is the sum of a growing linear cost, which is the
square. Profiling 300 lines after `#2370` put it at **2.47s of 3.10s, about 80%
of the run**, across 601 calls.

## 4. The fold property, tested

For a 27-event session containing ordinary, empty, non-ASCII, and code-shaped
material:

```text
prefix projections deterministic            yes, all 27
consumed_event_ids append-only across k     yes, all 27
as_of_event_id == last consumed id          yes, at every prefix
event_count == filtered prefix length       yes, at every prefix
```

So the projection depends only on its filtered event prefix, in append order.
That is the necessary condition for advancing Standing instead of rebuilding
it, and it holds.

## 5. The one history-dependent refusal

Every other check is per-event: an unsupported kind raises on the event in
hand, and payload agreement checks read only that payload.

One check is not. `register_goal_identity` refuses a duplicate identity
anywhere in the session:

```text
register_goal_identity(identity, coordinate)
    raise if identity already registered under another coordinate
```

Ten call sites register identities from goal applicability, admission,
consumption, and standing payloads.

**This refusal survives a continuation only if the continuation carries
`goal_identities`.** It does not depend on re-reading old events; it depends on
the accumulated set those events produced. Carry the set and the check is
unchanged.

## 6. The seed is incomplete, and the gap is exactly there

Comparing the twenty-three accumulators against the returned keys:

```text
accumulators not present in the returned Standing:
    goal_identities
```

One. The same one §5 identifies.

Nor is it fully reconstructible from what is returned. `goal_applicabilities`
entries preserve `applicability_ref`, `consumer_ref`, and `responsibility_ref`,
but the applicability act's `act_ref` is registered as an identity and does not
appear in the projected entry.

`known_loss`, `unknowns`, and `conflicts` are returned as sorted lists where
the accumulators are sets. That direction is lossless for sets of strings.

## 7. Why this is currently invisible

The live console records five event kinds:

```text
operator.ingress.raw_material_captured
operator.ingress.representation_examined
operator.ingress.ingress_occurred
operator.presentation.formed
operator.presentation.emitted
```

None of them reach `register_goal_identity`. The identities come from
`operator.interaction.goal_*` kinds, which no live path records.

So `goal_identities` is empty in every session the console can currently
produce. A continuation seeded from the returned Standing would be exactly
equivalent to full replay today, and would begin losing the duplicate-identity
refusal on the first session that records a goal occurrence. The loss would be
a missing refusal rather than a wrong value, which is the harder kind to
notice.

## 8. What a continuation would have to establish

Stated as requirements, not as a design:

```text
1  the seed states which occurrence it includes through
       as_of_event_id already does this

2  the continuation consumes exactly the occurrences after that one,
   in append order, and each exactly once
       consumed_event_ids supports checking this after the fact

3  the seed carries every accumulator the fold reads, including the
   ones no returned coordinate exposes
       goal_identities is the known gap

4  the advanced Standing is equal to the full replay it replaces
       testable at every prefix, as in §4
```

Requirement 3 is the one this investigation found. Requirements 1 and 2 are
already met by coordinates the projection records.

## 9. What this does not establish

**That a continuation should be built.** This is a findings pass. Whether
advancing session Standing is the right responsibility, and whose, is not
recovered here.

**That the fold property holds for kinds no live path records.** §4 tested a
session of the five live kinds. Exchange, interaction, and goal occurrences
were not exercised, and §5 identifies a cross-event check that lives precisely
in the untested region.

**That `goal_identities` is the only gap for those untested kinds.** §6
compares accumulators to returned keys, which is a structural check. It does
not prove that carrying `goal_identities` is sufficient.

**That the refusal is the only thing lost.** Only the accumulator set was
compared. No claim is made that every value would agree under continuation for
goal-bearing sessions.

**That session Standing is the last quadratic term.** It is the largest one
measured after `#2370`. Whether another appears once it is gone is unknown, and
`#2370` is the precedent for expecting one.
