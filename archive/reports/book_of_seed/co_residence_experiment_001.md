# Sixteen bodies in one Seed: experiment 011

Runtime amended narrowly. No Book amendment.

## Summary

Sixteen bodies were fed through the real CLI entry, `seed --db <path>`, one
console lifetime each, into one durable workspace. Each was then measured at d1
bounded by its own exchange and compared with `#2408`, where every body had a
Seed to itself.

```text
one workspace, 24032 events, 16 exchanges

  body             events   cand    d1   #2408
  grammar_brown       300    211     7       7   same
  roget               300    206     5       5   same
  grammar_kittr       300    137     2       2   same
  webster             300     87     2       2   same
  algebra             300     95    67      67   same
  boole               300    186    27      27   same
  euclid              300    256   157     157   same
  bash_guide          300    108     2       2   same
  cookbook            300    146    12      12   same
  french_hugo         300    189     2       2   same
  latin_vulgate       300    218    20      20   same
  austen              300    271    20      20   same
  dickens             300    250     6       6   same
  franklin            300    269    23      23   same
  emerson             300    268    78      78   same
  hume                300    146     3       3   same
```

**[measured]** Sixteen of sixteen bodies measure exactly what they measured
alone. **Co-residence without collapse holds**, and holds by measurement rather
than by assumption.

**[inference]** The session filter in `preserved_ingress_occurrences` is a
sufficient boundary for this measurement family. Nothing leaked between
exchanges sharing a workspace, a ledger and a process.

## 1. What the experiment found in `#2413`

**All sixteen lifetimes ran inside one process.** Reopening the real console is
a new process, and `new_id` counts from 1 in each one.

**[measured]** The second real `seed --db` invocation aborted:

```text
ValueError: duplicate presentation reference: operator_presentation_000001
```

**[measured]** `SQLiteEventLedger` already reserves identifier counters on open,
from an allowlist of seven prefixes that predates the operator console. The
console persists four the allowlist does not name — `operator_presentation`,
`operator_ingress_attempt`, `operator_material`, `session` — and session ids
live in their own column, which the payload walk never reads.

**[inference]** Nothing was wrong with those prefixes before. `#2413` connected
the console to a durable ledger, and no console had ever written durable history
until then. The defect was created by the connection, not uncovered in old code.

**Repaired**: the four prefixes are reserved, the session column is read on
open, and a `subprocess` test runs three genuinely separate processes.

```text
  sessions   session_000001   ['material from process 1']
             session_000002   ['material from process 2']
             session_000003   ['material from process 3']
```

**[inference]** Nineteen tests missed this for the same reason the experiment
did: they share a process, where the counters keep climbing and no identifier is
ever reissued. A test that cannot reach the condition cannot fail on it.

## 2. Disclosures

**Which body was supplied during which exchange is the reader's, not Seed's.**
The mapping lives in the experiment script for the reason `corpus/SOURCES.md`
gives for itself. Seed holds sixteen bounded exchanges that differ, per `#2410`
and `#2411`.

**Putting sixteen results in one table is a reader's act.** No cross-source
comparison was built. `#2410` §5 split this: preserving bodies distinctly is
evidence preservation and needed no warranted consumer first; a comparing act is
construction and still does. The table above is mine.

**Opening the durable ledger costs 1.53s at 24,032 events**, because
`_reserve_persisted_payload_ids` walks every stored payload on every open. That
is pre-existing and not introduced by `#2413`, but it grows without bound and
now sits on every durable console open. It is recorded, not repaired.

**The window is `#2408`'s**, 300 lines with `algebra` at a different offset, and
`#2408`'s disclosures carry: the battery is not matched on recurrence, and
`boole` and `euclid` are markup rather than the books they name.

## 3. What this does not establish

**That measurements would stay bounded under any other family.** One family was
run, at one displacement. A form reading across occurrences rather than within
them would pool these bodies immediately, and nothing here prevents that.

**That a session is a source.** `#2410` and `#2411` hold unchanged. Sixteen
distinctly preserved bodies is what this delivers; which book each carried is
provenance held outside Seed.

**That cross-source comparison is now available.** Its owner question is
untouched. `#2410` §3 found that comparing findings across bodies is bounded
testimony comparison under `05.Testimony:27`; that it is not blocked is not the
same as its having been built.

**That the identifier repair is complete.** Four prefixes were added because
four were observed to reach a durable ledger from a console lifetime. Any future
minted identifier that a durable ledger stores has the same requirement, and
nothing enforces it.
