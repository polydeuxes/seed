# One transaction, occurrences and their reservations together

Runtime amended narrowly. No Book amendment.

## The defect

`#2428` stated its invariant plainly: an identifier reservation is written **in
the same transaction as the occurrence that carried the identifier**. `append`
does that. `append_many` did not.

```text
  transaction 1     insert event 1 .. event N          COMMIT
  transaction 2     persist reservations 1 .. N        COMMIT
```

**[inference]** A failure between the two commits leaves durable occurrences
carrying identifiers whose counters are stale on reopen — the collision `#2428`
exists to prevent, and `#2415` measured as the second process aborting on
`duplicate presentation reference`. `evt` is partly shielded because open
recovers the maximum event id separately; the payload and session prefixes,
which are why `id_reservations` was introduced, are not.

**[measured]** `#2428` was written and reviewed without this being noticed,
including by its author. It surfaced only when batching became the answer to a
different question.

## The repair

```text
  BEGIN
      for each event:  insert occurrence
                       persist the reservations it carries
  COMMIT
```

A test traces the connection and requires exactly one `COMMIT` for a batch,
with the reservations present afterwards. A second reopens a batched store with
the process counters cleared and requires the next identifier not to reissue a
batched one.

## Why it mattered now

**[measured]** Batching is the whole speed story. At full SQLite durability,
one transaction per batch:

```text
        1 event/txn    9.943 ms/event    1.0x
       10 events/txn   1.183 ms/event    8.4x
      100 events/txn   0.225 ms/event   44.2x
     1000 events/txn   0.143 ms/event   69.7x
```

**[inference]** The 44x attributed to tmpfs was never RAM against disk. It was
one durability barrier per occurrence. Batching at **full durability** is faster
than tmpfs (0.218) and faster than `synchronous=OFF` (0.250) were measured to
be, so the durability question does not need answering — it dissolves.

**[measured]** The ledger's own contract already permitted this: `append_many`
documents that event granularity remains unchanged while the underlying
persistence transaction may be batched. What changes is the physical commit
boundary and nothing else.

```text
  event identity, order, digest, Evidence     unchanged
  identifier reservation                      now atomic with its occurrence
  physical durability barrier                 amortised across the batch
```

## What this does not establish

**That 1,000 is the right batch.** It is the largest measured. 100 already
reaches 44x. The trade is throughput against how much uncommitted work a failure
discards — and that is the **current batch only**, never already-committed
history.

**That the console should batch.** Its natural boundary is one interaction, not
one event, but whether five events can be deferred to interaction completion
depends on whether later steps in the same interaction consume earlier recorded
occurrences. Unexamined, and untouched here.

**That any caller now batches.** This repairs the path so that batching is safe.
No call site was changed.

**That tmpfs or relaxed durability have a remaining speed argument.** They do
not, on this evidence. Capacity is a separate question and unaffected.
