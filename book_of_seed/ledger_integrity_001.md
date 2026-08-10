# Mutation refused by default, corruption made detectable

Runtime amended narrowly. No Book amendment.

## What this claims, and what it does not

```text
  claimed      mutation is refused by default
  claimed      undetected corruption becomes detectable
  NOT claimed  history cannot change
  NOT claimed  the ledger is immutable
```

**[measured]** Before this, a plain `UPDATE` on the events table rewrote a
recorded payload and the ledger read the changed value back. Append-only was a
convention of `events.py` — no `UPDATE` or `DELETE` in the module — and nothing
protected the file.

**[measured]** Active law never requires append-only. It appears once, in
`06.Standing:16`, inside a permissive list — "Append-only records, established
facts, projected material, current lawful condition, context views, and
candidate convergence **may support** a bounded current constitutional
standing" — beside members that are not append-only. Nothing requires physical
inscription rather than recoverability.

**[inference]** So this establishes a storage property Seed chose, not one the
Book demanded. That distinction matters because the reason for wanting it is
downstream: references to preserved inputs are only equivalent to carriage while
the referenced occurrence is immutable and reachable, and the first half was
believed rather than held.

## The arrangement

```text
  new occurrence     whole persisted row -> SHA-256 -> content_hash
  SQLite             BEFORE UPDATE and BEFORE DELETE refuse
  consuming act      Compare verifies its two inputs, refuses CORRUPTED
  legacy row         UNVERIFIABLE, never back-filled
  in-memory ledger   UNVERIFIABLE — objects, not stored bytes
```

**[measured]** The digest covers all nine persisted fields, so moving an
occurrence between sessions is detected. That is not incidental: `session_id` is
the boundary keeping sixteen bounded exchanges apart, and a payload-only digest
would have left it unprotected.

**[measured]** The digest is free. Interleaved arms under identical disk load,
800 appends each:

```text
  without digest    18.56 ms
  with digest       18.40 ms
  difference        -0.16 ms   (noise)
```

An earlier reading of this report's author compared 18.08 ms against a 12.10 ms
figure measured on a quieter disk and would have shown a 49% regression. Two
arms measured together show none. **A benchmark against a baseline taken under
different conditions is not a measurement of the change.**

## Where verification happens

On the consuming act, not on reads.

**[inference]** `#2416` made ordinary reads bounded and cheap. Recomputing a
digest inside `get` or `list_session` would charge every reader for an
obligation only a consuming act carries. `compare_preserved_findings` claims to
preserve what it consumes, so it verifies what it consumes; a diagnostic listing
events claims nothing and verifies nothing.

**[measured]** A full verification pass over 86,907 findings costs 1.27 s, so
this is a placement decision rather than a cost one.

## Three limits, written as tests

They are tests rather than prose so they cannot be quietly forgotten.

**`test_rewriting_the_row_and_its_digest_together_is_not_detected`** asserts
`VERIFIED` on tampered content. `DROP TRIGGER` succeeds, and anyone who can
issue it can also recompute the digest. Detecting that needs an integrity root
outside the mutable database, which this does not have and does not claim.

**`test_history_written_before_the_digest_is_unverifiable_not_verified`**
pins the migration stance. A digest computed today proves what bytes exist
today; it cannot prove they are the bytes originally recorded. Back-filling
would manufacture exactly the guarantee this exists to stop assuming.

**`test_an_unverifiable_input_is_recorded_rather_than_refused`** pins that
Compare refuses only `CORRUPTED`. `UNVERIFIABLE` travels into the comparison
payload on the input that carried it. In-memory ledgers and pre-digest history
are both lawfully unverifiable, and refusing them would demand a guarantee
nothing ever offered — the same shape `#2419` removed from `05.Testimony.E`.

## What this does not establish

**That references may now replace carriage.** Nothing here touches
consumed-input preservation, and no pointer was introduced. Whether
`05.Testimony.E`'s obligation is satisfied by verified recoverability rather
than copied carriage is unrecovered, and this deliberately runs first so that
question is not answered backwards from a storage optimisation.

**That the 48% copied input state is waste.** While the store was unprotected,
that copy was the only thing making a comparison independent of a mutable row.
It may remain warranted after this; that is the separate question.

**That the repeated constitutional text is warranted.** Roughly 23% of each
comparison is byte-identical boilerplate — boundary notes, owner wording, fixed
dimension strings. Nothing in active law requires inscription, and that question
is untouched here and needs no doctrinal answer about inputs.

**That a trigger is the right mechanism.** It is *a* mechanism that refuses the
mutation the API never performs. Content addressing, an integrity root, or a
different store would each make different claims, and none was compared.
