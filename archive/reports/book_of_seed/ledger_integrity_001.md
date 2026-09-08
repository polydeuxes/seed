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
  pre-digest schema  REFUSED at open, rows or not; no ALTER path exists
  nullable digest    REFUSED at open, however many rows carry one
  durable occurrence VERIFIED or CORRUPTED, never UNVERIFIABLE
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

**`test_a_pre_digest_store_is_refused_rather_than_migrated`** pins the
migration stance. A digest computed today proves what bytes exist today; it
cannot prove they are the bytes originally recorded, so no back-fill is
performed — and Seed does not preserve a durable history nobody needs.

This took two passes. The first classified undigested rows as `UNVERIFIABLE`
and consumed them, on backward-compatibility grounds the operator does not
hold — leaving a **supported path on which a durable occurrence carried no
integrity**, which could later have been cited as evidence that durable
references need none. The second refused populated pre-digest stores but
migrated empty ones by `ALTER`, which meant **a new database was created by
running a compatibility migration over the shape being rejected**. The table is
now born with `content_hash TEXT NOT NULL` and there is no `ALTER` path at all.

The invariant that buys:

```text
  if the ledger opens, the store was born with the current integrity schema
```

**And the check has to prove that, not something near it.** A third pass was
needed: the open validated that `content_hash` exists and that no row is
currently `NULL`, which a store created by the withdrawn `ALTER` path could
satisfy while remaining nullable. Holding no undigested occurrence today is not
being unable to hold one tomorrow, so the column's `NOT NULL` declaration is
what is checked. **Prose claiming a property the runtime does not enforce is
the defect `#2421` removed from Compare's arity, appearing again in the same
session.**

The row-level check became unreachable once the column check was right — a
`NOT NULL` column cannot hold a null digest, and a nullable column is refused
before rows are counted — so it was removed rather than left as a guard that
guards nothing.

rather than "either born current, or an empty old schema we upgraded". A
durable occurrence is `VERIFIED` or `CORRUPTED`; `UNVERIFIABLE` survives only
for the in-memory ledger and for an identifier nothing stored.

**`test_an_unverifiable_input_is_recorded_rather_than_refused`** pins that
Compare refuses only `CORRUPTED`. `UNVERIFIABLE` travels into the comparison
payload on the input that carried it. That case is now the in-memory ledger
alone, which holds objects rather than stored bytes; demanding a durable
guarantee of a storage shape that has none would be the shape `#2419` removed
from `05.Testimony.E`.

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

**That existing databases keep working.** They do not. Any SQLite ledger
written before this — including `.seed-local.sqlite` and the corpus experiment
stores — is refused at open, whether or not it holds rows. That is the intended
consequence of not carrying a history nobody needs, and it is a cost, not a
side effect.

**That `VERIFIED` means durable.** It means the stored occurrence still matches
its recorded digest. A ledger on tmpfs verifies identically and does not survive
a reboot, so integrity and persistence are separate properties that this
arrangement supplies separately.

**That a trigger is the right mechanism.** It is *a* mechanism that refuses the
mutation the API never performs. Content addressing, an integrity root, or a
different store would each make different claims, and none was compared.

## Identifier counters, kept rather than reconstructed

`#2414` recorded the largest remaining whole-history read and curator scoped it
out at the time. The rerun's scale reopened it.

**[measured]** Reconstructing the highest issued suffix per prefix by walking
every stored payload, on every open:

```text
    5,000 events   1.87s
   20,000 events   7.42s
   50,000 events  18.55s
  100,000 events  36.92s
  ~965,000 events ~356s extrapolated, every open
```

**[measured]** Kept in an `id_reservations` table written by the same
transaction as the occurrence that carried the identifier:

```text
    5,000 events   0.006s
   20,000 events   0.015s
   50,000 events   0.038s
  100,000 events   0.075s
```

**[inference]** The table is not an occurrence. It records no claim, supports no
standing, and only ever rises; it is ledger mechanics, and the `events` mutation
refusal deliberately does not cover it. A test pins that rewriting it does not
make any occurrence `CORRUPTED`.

**[measured]** The property the reservation exists for is unchanged: three
separate OS processes against one durable store still receive distinct sessions
and every occurrence verifies. `#2415` established that without reservation the
second process reissues identifiers and aborts.
