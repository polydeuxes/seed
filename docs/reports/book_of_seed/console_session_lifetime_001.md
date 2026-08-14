# The console lifetime owns its session: repair 001

Runtime amended narrowly. No Book amendment.

## What was wrong

```python
DEFAULT_SESSION = "local"
parser.add_argument("--session", default=DEFAULT_SESSION, ...)
```

The bare console passed that constant straight through, so every console
lifetime addressed the one named session `local`. Opening the console, exiting,
and opening it again produced a second bounded exchange that the projection
could not tell from a continuation of the first.

**A console lifetime is one bounded exchange.** The entry boundary owns it —
the console opens there and exits there — so the session id is now allocated
there.

`--session` is untouched for the subcommands, which address a session that
already exists. A caller passing `session_id` directly to
`run_persistent_operator_console` still owns that choice, and the tests pin
both.

## The consumer curator asked about

> Report any existing consumer that actually requires the default `"local"`
> session to persist across console lifetimes.

**There is none, and the reason matters more than the answer.**

**[measured]** `EventLedger` is "Process-local append-only ledger"
(`seed_runtime/events.py:22`) and holds three in-memory containers. It is not
the SQLite ledger.

**[measured]** The bare console constructs `EventLedger()` and **never consults
`args.db`** (`scripts/seed_local.py:5791`). Every other ledger-opening path in
the CLI reads `SQLiteEventLedger(args.db) if args.db else EventLedger()` —
sixteen of them.

**[inference]** So no consumer *can* require it. Two real console invocations
never share history, because the first one's ledger is discarded when its
process ends. The defect repaired here was latent, not active.

## The finding this repair does not deliver

Curator wrote that fixing the session lifetime "immediately gives us the
mechanism we were prematurely trying to manufacture":

```text
workspace
├── session A → Brown
├── session B → Roget
└── session C → Austen
```

**It does not.** Three console lifetimes today produce three separate in-memory
ledgers that never coexist. Distinct session ids across ledgers that never meet
distinguish nothing.

**[inference]** The two defects are paired and neither is useful alone.
Repairing the session id without the ledger leaves co-residence as far away as
it was. Repairing the ledger without the session id would have made the
collision **live**: a durable console would then have replayed every prior
lifetime's events into each new one's Standing.

This repair is therefore the half that had to come first, and it is only half.
The `--db` omission is recorded here and **not** repaired, because the operator
scoped this to the session lifetime and because a console that writes durable
history is a larger question than a one-line change to how a ledger is opened.

## Tests

`tests/test_console_session_lifetime.py`, eight of them:

```text
  two lifetimes receive different session ids
  neither uses the constant default
  both share one workspace
  each holds only its own ingress
  each forms its own C0
  a reopened console does not continue the prior Standing
  a caller supplying a session id still owns it
  --session remains for the subcommands
```

The shared-ledger fixture substitutes one ledger for the two the CLI would
otherwise build, and says in its own docstring that it is supplying what the
CLI does not. Without that substitution the boundary is unobservable, which is
the finding above stated as a testing difficulty.

## What this does not establish

**That the session boundary is the right one for bounding material.** `#2410`
and `#2411` both found that it is not a source boundary, and this changes
nothing about that. It makes session mean one exchange, which is what session
already claimed to mean.

**That co-residence is now available.** See above. It needs durable history the
console does not write.

**That a session-start event should exist.** None was added. Curator advised
against it and `#2411` recorded that C0's formation and emission are the first
occurrences a lifetime records.
