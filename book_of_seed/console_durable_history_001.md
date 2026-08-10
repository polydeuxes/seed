# The console reaches its durable ledger: repair 002

Runtime amended narrowly. No Book amendment.

## What was wrong

**[measured]** `--db` could not reach the console. The console was the
no-argument entry (`if not argv:`), and `--db` made the argument list non-empty,
so `seed --db seed.db` fell through every branch to `parser.print_help()`.

**[measured]** Without a durable ledger the session-id collision `#2412`
repaired could not bite, because the previous lifetime's events were gone before
the next lifetime opened. `#2412` recorded this and its production comment
overstated it, saying reopening "continued the previous exchange's Standing"
where it would only have done so if history survived. That comment is corrected.

**The two halves are only safe together.** Connecting the ledger without
`#2412` would have made the collision live: every reopened console would have
replayed every prior lifetime into its own Standing.

## The read that would have grown forever

Connecting `--db` alone would have introduced a second defect, and this one was
not visible from either half.

**[measured]** `project_operator_session_standing` called
`ledger.list(workspace_id)` — every event in the workspace — and filtered by
session afterwards. The console calls it once at startup.

**[measured]** With a durable ledger, that read grows with total history while
its answer does not. Measured over five console lifetimes of 60 lines each,
projecting Standing for a **freshly allocated** session:

```text
  events in workspace     302     604     906    1208    1510
  startup projection     9.3ms  22.5ms  49.2ms  38.3ms  43.7ms
  presentations found        0       0       0       0       0
```

It read the entire durable history, every time, to find nothing — because a
fresh session has no events by construction.

**[inference]** At corpus scale this is the shape of the problem
`project_corpus_runs_and_projector_state` records as already killed once. A
300-line body records about 900 events, so sixteen bodies would put a
14,000-event read on every console open, growing without bound.

## The repair

`list_session(workspace_id, session_id)` on both ledgers: a comprehension on the
in-memory one, a `WHERE workspace_id = ? AND session_id = ?` on the SQLite one.
`project_operator_session_standing` uses it, because a session projection reads
a session.

```text
  events in workspace     302     604     906    1208    1510
  startup projection    0.33ms  0.36ms  0.37ms  0.42ms  0.46ms
```

Flat instead of growing, and 95× faster at 1,510 events. Nothing was lost: an
earlier session still projects its full Standing when addressed by id, and a
test pins that.

**[inference]** This is the session-scoped query
`project_compare_road_state_2026_08_06` recorded as "the one missing query". It
was written for this repair, not recovered from anything.

## What was deliberately not done

Curator's caution — that sixteen other CLI paths using `SQLiteEventLedger` is
not evidence the console should — **was right, and is not what happened here.**
The reason for connecting it is the operator's: persistent memory is the thing
being built, and a process-local ledger cannot give a later lifetime access to
earlier Standing. Proximity supplied nothing.

Nothing beyond the existing ledger boundary was touched. No session manager, no
projection store, no cache, no new event kind, no change to how events are
recorded or what they carry.

## Tests

`tests/test_console_session_lifetime.py`, nineteen. The monkeypatched
shared-ledger fixture `#2412` needed is **gone** — two real console invocations
against one `--db` path now share history, so the boundary is observable
without manufacturing it. That fixture existed because the CLI could not do
what it was testing, which was the finding rather than the design.

```text
  console options alone select the console        4 cases
  any other argument selects something else       2 cases
  a --db console records into that db
  the bare console writes no durable history
  two lifetimes receive different session ids
  neither uses the constant default
  both share one workspace
  each holds only its own ingress
  a reopened console does not continue prior Standing
  the earlier lifetime remains projectable
  a session read returns only that session
  a fresh session reads none of the history
  the in-memory ledger scopes the same way
  a caller supplying a session id still owns it
  --session remains for the subcommands
```

## What this does not establish

**That co-residence is now available.** Sixteen bodies could now share one
durable workspace as sixteen sessions. `#2410` and `#2411` hold: a session is a
bounded exchange, not a source, and which body each session carried remains
provenance the operator holds.

**That the alias should change.** `seed` still opens an in-memory console.
`seed --db <path>` opens a durable one. Which the alias should be is the
operator's call and nothing here presumes it.

**That `--workspace` is the right second console option.** It was included
because the console already accepted it; no separate reason was established.

**That the startup projection is needed at all.** For a freshly allocated
session it is provably empty. It was left in place because
`run_persistent_operator_console` is also called with existing session ids, and
removing it would have been a change to the console's contract rather than to
its cost.
