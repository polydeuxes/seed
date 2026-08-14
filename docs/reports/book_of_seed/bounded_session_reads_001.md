# Bounding what is read, not only what is answered: repair 003

Runtime amended narrowly. No Book amendment.

## What was wrong

`#2414` found two reads that answered a bounded question by reading everything.
Both returned correct results, which is why neither was visible until a
workspace held sixteen co-resident bodies.

**The acquisition read.** `preserved_ingress_occurrences` called
`ledger.list(workspace_id)` and filtered by session in Python, although
`list_session` existed one layer down.

**The session query.** The only index on `events` was the automatic one on `id`,
so selecting by `workspace_id` and `session_id` scanned every row.

## The repair

```python
    return [
        event
        for event in ledger.list_session(workspace_id, session_id)
        if event.kind == INGRESS_OCCURRED_KIND
    ]
```

```sql
CREATE INDEX IF NOT EXISTS idx_events_workspace_session
ON events(workspace_id, session_id)
```

Measured on `#2415`'s 24,032-event workspace of sixteen bodies:

```text
                                        before      after
  query plan                         SCAN events   SEARCH USING
                                                   idx_events_workspace_session
  SQL, one session                       17.3 ms        3.3 ms
  preserved_ingress_occurrences         796.9 ms       38.9 ms      20x
```

**[measured]** Identical occurrences and identical payloads, by id and by
content, for every session in the tests and for the measured body above.

**[inference]** The path is now bounded in both senses. The consumer asks for
one session, SQLite seeks that session, and only that session's events are
deserialized. Before, only the last of those three was true.

## Why this was invisible

**[inference]** Both defects produced correct answers, and `#2413`'s
`list_session` produced a 95× improvement that made the remaining scan look like
success. A read that returns the right rows after examining all of them is
indistinguishable from a bounded read at every point except cost, and cost only
became legible when sixteen bodies shared a ledger.

The general shape, which `#2414` named and this is the second instance of:

```text
  answer extent    one session
  read extent      the whole workspace
```

## Tests

`tests/test_bounded_session_reads.py`, eleven.

The identical-results tests matter as much as the query-plan test. A bounded
read that changes what it returns has not been made cheaper; it has been broken.
The former whole-workspace read is kept in the test file as the comparison, so
the two are checked against each other rather than against an expectation.

```text
  occurrences identical in memory            3 sessions
  occurrences identical durably              3 sessions
  each body still gets only its own material
  an unrecorded session reads empty
  the session read seeks rather than scans
  the index covers the boundary sessions are selected by
  the index is created on a ledger written before this change
```

## What this does not establish

**That the open-time reads are addressed.** They are not, and identifier
reservation remains the largest of them at 2.39s per open on this workspace.
`#2414` §2 records it and curator scoped it out of this repair deliberately: it
would introduce durable counter ownership, which needs its own investigation of
crash and transaction semantics.

**That every read is now bounded.** Two were repaired because `#2414` traced one
console lifetime and found two. Subcommands, diagnostics and audit surfaces were
never traced, and `#2414` §5 says so.

**That indexing is free.** An index is maintained on every insert. Nothing here
measured the write cost, and the workspaces in play are read far more than
written.

**That the in-memory ledger gained anything.** `list_session` there is a
comprehension over the workspace list, so its read extent is unchanged. Only the
deserialization and the durable seek improved, and only the durable ledger has
either.
