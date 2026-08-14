# Durable storage physiology: survey 001

Findings only. No runtime or Book amendment. **No database is proposed**, and
the evidence below does not distinguish one.

## Summary

Traced against a real durable console lifetime and the 24,032-event workspace
`#2415` recorded, **the live durable console path** shows **six statement
shapes**. Three run once at open, three run per interaction.

**Correction.** This first said "Seed's entire durable access surface". Only one
console lifetime was traced, and §5 already recorded that subcommands,
diagnostics and audit surfaces were not. The warranted claim is about the
console path, and the broader one was never measured.

```text
  AT OPEN                                                     extent    cost
  SELECT MAX(...) FROM events WHERE id LIKE 'evt%'            global     low
  SELECT payload FROM events ORDER BY rowid                   global    2.2s
  SELECT DISTINCT session_id FROM events                      global     low

  PER INTERACTION
  INSERT INTO events (...)                             one occurrence    low
  SELECT * FROM events WHERE id = ?                    one occurrence  0.1ms
  SELECT * FROM events WHERE workspace_id=? AND session_id=?   one session
```

**The per-interaction path is already what Standing implies.** Append one
occurrence, read one occurrence by exact id, read one bounded session once at
the start. There is no rebuild after any event.

## 1. The operator's recollection, verified

> *"It was integrated with State and did global rebuild after every new event
> instead of our proper Standing."*

**[measured]** True of the projection store, and **not true of the event
ledger**, and neither is on the console path. Profiling one durable console
lifetime, exactly ten repository modules execute:

```text
  seed_runtime/events.py                          5672 calls
  seed_runtime/secrets.py                         1338
  seed_runtime/operator_ingress_addressable_material.py  133
  seed_runtime/ids.py                               47
  seed_runtime/models.py                            42
  seed_runtime/operator_ingress.py                  38
  seed_runtime/operator_ingress_representation.py   23
  scripts/seed_local.py                             21
  seed_runtime/operator_session_standing.py         15
  seed_runtime/operator_presentation.py             15

  projection_store.py   state.py   state_patches.py   fact_index.py
      not executed    not executed    not executed    not executed
```

**[measured]** Appending does no global work. `_insert_without_commit` issues
one INSERT; `_advance_event_counter` is local; `_reserve_payload_ids` walks the
**one** payload being written.

**[inference]** Curator's separation is correct and stronger than stated: this
is not a question of snipping `State` out of the ledger, because the console
path never reaches it. Nothing needs disentangling on the live path.

## 2. Where a read exceeds its answer

Three reads, and all three are at open or on acquisition rather than per
interaction.

### Identifier reservation — the clearest specimen

**Question asked:** what identifier suffixes have already been allocated?
**Answer size:** eleven integers.
**Read extent:** every payload of every event, deserialized and walked.

```text
  SQL fetch                      44 ms
  whole open                   2200 ms
  -> 98% of it is Python, not the database
```

**[measured]** This is not a storage-engine cost. It is a Python scan over
deserialized payloads, and the database part of it is 2%.

**[measured]** **`#2415` made it 51% worse.** Reserving four more prefixes means
four more comparisons per string per payload:

```text
   7 prefixes (before #2415)    1.58 s
  11 prefixes (after  #2415)    2.39 s
```

The repair was necessary — without it the second console process aborts — and
its cost is real and compounding. Recorded against my own work, not inherited.

### The bounded session read is not bounded in what it scans

**[measured]** The only index on `events` is the automatic one on `id`.
`WHERE workspace_id = ? AND session_id = ?` is a **SCAN**: 17.3ms reading 24,032
rows to return 1,502.

**[inference]** `list_session` bounded what is *returned* and what is
*deserialized*, which is where `#2413`'s 95× came from. It did not bound what is
*read*. The distinction was invisible while the win was large.

**Repaired in `#2416`**, which indexes the boundary sessions are selected by.

### The acquisition path still reads the whole workspace

**[measured]** `preserved_ingress_occurrences` calls `ledger.list(workspace_id)`
and filters by session in Python, although `list_session` now exists:

```text
  ledger.list(workspace) + python filter   757.8 ms   300 occurrences
  ledger.list_session()  + python filter    46.4 ms   300 occurrences
  identical results
```

**[inference]** 16× for the same answer, and the factor is the number of
co-resident bodies. This is exactly the shape `#2413` repaired one layer up,
surviving one layer down.

**Repaired in `#2416`.** This survey did not repair it, being a survey.

## 3. The question the evidence cannot settle

Curator listed the questions that look graph-shaped:

```text
  what Evidence produced this finding?
  what occurrence descended from this occurrence?
  which findings consume this Evidence?
```

**[measured]** **None of them is asked anywhere in the live path.**

- No `WITH RECURSIVE` exists in the repository.
- The only relationship traversal is `state.py:_traverse_relationships`, in the
  machinery §1 shows is not executed.
- Edges *are* recorded — `lineage`, `causation_id`, `correlation_id`,
  `consumed_event_ids`, `premise_event_id`, `raw_material_event_id` — and
  nothing reads them as a graph.
- One-hop edge following does exist: `SELECT * FROM events WHERE id = ?`, ten
  times per lifetime at 0.1ms, resolving a recorded id to its event.

**[inference]** The relational-versus-DAG question is still a shrug, and now the
reason is known rather than felt: **one side of the comparison has no live
reads.** Choosing a store for traversal today would be choosing for a workload
that does not exist, which is compiling future competence into the store — the
thing curator asked to avoid.

**[Unknown]** Whether multi-hop traversal becomes a real read shape. `#2411`'s
descent-bounding and `#2410`'s cross-source comparison would both produce one,
and both are unbuilt and unowned.

## 4. What the observed shapes require

Stated as properties, from the six statements only.

```text
  established by the live path
    append one occurrence durably, ordered            INSERT
    fetch one occurrence by exact id                  0.1ms, indexed
    fetch one session's occurrences, in order         indexed by #2416
    survive process exit                              the point of --db
    tell one bounded exchange from another            #2415, 16/16

  established as a defect of the current arrangement
    answer a small question without a whole-history read
    bound what is read, not only what is returned

  NOT established by anything measured
    multi-hop traversal
    relation queries between preserved subjects
    any read whose answer is a subgraph
```

**[inference]** Everything in the first two groups is served by an ordered
append-only table with appropriate indexes. Nothing measured argues for or
against a graph store, because nothing measured traverses.

## 5. What this does not establish

**That SQLite is the right substrate.** It is the current one, it serves the
observed shapes, and its measured costs are Python-side rather than engine-side.
That is not a comparison against alternatives, and none was run.

**That the three excess reads are hard to fix.** Two look small. This is a
survey and proposes no repair; "looks small" has been wrong before in this
session.

**That the live path is the whole path.** One console lifetime with `--db` was
traced. Subcommands, diagnostics and the audit surfaces were not, and several
do touch `State` and the projection store. Whether any of those is live is a
separate question this does not answer.

**That recorded edges are unused because they are unnecessary.** They are
recorded by acts that had reason to record them. Nothing consuming them yet is
a fact about consumers, not about the edges — `#2409` and
`feedback_absence_is_not_an_argument_against_building` both apply.
