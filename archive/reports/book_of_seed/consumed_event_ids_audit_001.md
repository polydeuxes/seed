# `consumed_event_ids`: audit 001

## 1. Executive

`#2373` removed the last consumer of session Standing's append-order event
inventory. This audit asks whether the inventory itself still belongs in the
projected Standing before anything is built on it.

**It has no reader.** After `#2373`, nothing outside the function that builds
it reads `consumed_event_ids` — not the runtime, not the rendered View, not the
Presentation path. Two assertions in one test module are the only references.

**The projector does not read it either.** Inside
`project_operator_session_standing` the list is initialised, appended to, and
returned. It is never consulted. It is write-only.

**The one claim made for it in the code is wrong.** A comment states emission
order is recoverable from `presentations` and `consumed_event_ids`. Emission
order is recoverable from `presentations` alone.

**`as_of_event_id` and `event_count` already do the work.** At every step of a
session they identify the consumed prefix exactly, and the applicable suffix
after the boundary is exactly what a continuation would consume.

So the answer to Q3 is **projector bookkeeping**, and the minimal continuation
seed does not include it.

No runtime change is proposed here.

## 2. Q1 — every reader after `#2373`

```text
seed_runtime/operator_session_standing.py:145    its own initialisation
seed_runtime/operator_session_standing.py:170    its own append
seed_runtime/operator_session_standing.py:1321   its own return
seed_runtime/operator_session_standing.py:1327   a comment about it

tests/test_presentation_records_no_history_inventory.py:172-173
```

Zero non-test readers.

Checked for indirect consumption as well. Nothing iterates the Standing mapping
generically. `operator_presentation.py:176` takes
`session_standing["as_of_event_id"]` as its provenance source, and
`operator_ingress_view.py:76` renders "as of event …" from the same coordinate.
Both use the boundary; neither touches the list.

## 3. Q2 — the one claim, and whether it holds

`operator_session_standing.py:1327`:

> Emission order is recoverable from `presentations` and `consumed_event_ids`;
> naming one of them current would assert present relevance that no occurrence
> establishes.

Tested over a four-interaction session. The emitted occurrences taken from
`presentations` alone are already in ledger order, and identical to the order
derived by filtering `consumed_event_ids`.

```text
emission order from presentations alone, in ledger order    yes
identical to the order derived from consumed_event_ids      yes
```

Each `presentations` entry carries `formed_event_id` and `emitted_event_id`,
and the mapping preserves insertion order. The list adds nothing to the claim
its own comment cites it for.

The rest of that comment stands and is untouched: no Presentation is named
current, and nothing here proposes naming one.

## 4. Q3 — what it is

```text
constitutional Standing?
    no. Nothing consumes it, and no clause names it. A coordinate
    that no responsibility reads establishes nothing for anyone.

View or provenance inventory?
    no. 06.Representations:18 permits a View to be an inventory or
    provenance index "when its contract asserts only source
    visibility, identity, location, or faithful transformation".
    This is not exposed as a View and no contract asserts it.
    05.Evidence:19 separately refuses copied identifiers the
    standing of verified provenance.

projector bookkeeping?
    yes. Built by the fold, never read by it, returned because it
    was in scope.
```

The write-only shape is the decisive part. A value the producing act never
consults is not participating in the projection; it is a by-product of it.

## 5. Q4 — continuation without the list

Across every prefix of a session containing ordinary, empty, and non-ASCII
material:

```text
event_count equals the applicable events seen so far          yes
as_of_event_id equals the last applicable event seen          yes
the applicable suffix after as_of is exactly what remains     yes
```

So a continuation can locate its new occurrences from the boundary alone. It
does not need the prefix enumerated to know where the prefix ended.

`event_count` is a useful second coordinate here: it is a fixed-size check that
a continuation consumed the expected number of occurrences, which is the
exactly-once property `#2371 §8` asked for, without an identifier per event.

## 6. Q6 — the minimal continuation seed for the active road

```text
required
    the projected Standing's accumulator coordinates
    as_of_event_id          where to resume
    event_count             how many were consumed, for checking

not required
    consumed_event_ids      no reader, not read by the fold,
                            and its stated purpose is served by
                            `presentations`

out of scope
    goal_identities         dormant; #2371 established the five
                            live kinds never reach it
```

The seed is the returned Standing minus one coordinate, plus the ledger to
supply occurrences after the boundary.

## 7. What this does not establish

**That `consumed_event_ids` should be removed.** This is a findings pass. It is
a returned coordinate with a test asserting it, and removal is a runtime change
with its own scope.

**That it never had a purpose.** It had a consumer until `#2373` removed it.
This audit describes what is true now, not whether it was always redundant.

**That the seed in §6 is sufficient.** §5 establishes that the boundary locates
the new occurrences. It does not prove that every accumulator advances
correctly from the returned Standing, which is the experiment `#2371 §8`
requirement 4 still calls for.

**That the fold property holds for goal-bearing sessions.** `#2371` and `#2372`
both recorded this limit and it is unchanged. Every session measured here
contains only the five live kinds.

**That `event_count` is sufficient for exactly-once.** §5 shows it counts what
was consumed. Whether a count can establish that no applicable occurrence was
skipped and none consumed twice, against an append-only ledger, is not
recovered here.
