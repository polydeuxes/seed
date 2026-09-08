# Presentation's copied Evidence inventory: investigation 001

## 1. Executive

Every Presentation formation copies session Standing's entire append-order
event inventory into its own recorded payload:

```text
standing_evidence_ids = list(session_standing["consumed_event_ids"])
```

alongside `session_standing_as_of_event_id`, which already names the exact
occurrence the Standing was consumed through.

**The copy is exactly derivable from the boundary recorded beside it.** Across
67 formations in three sessions, the stored list equals the filtered session
prefix through `session_standing_as_of_event_id` every time.

**It is durable, not transient.** The list is written into the
`operator.presentation.formed` payload, so the cost is stored bytes.

**Its growth is quadratic**, converging on x4 per doubling. Extrapolated to the
grammar book that is 29 billion stored identifiers, about 323 GB of duplicated
event identifiers.

**No clause requires it**, and two clauses say copied lineage establishes
nothing.

No runtime or Book change is proposed here.

## 2. What is copied, and where it lands

`form_operator_presentation` copies at line 133 and records at 192, returning
the same list at 213. Both the recorded payload and the returned projection
carry it, next to `session_standing_as_of_event_id` in both places.

`project_operator_session_standing:194` reads it back out of the payload into
the projected `presentations` entry, so each Standing projection re-exposes
every formation's copy.

Outside those two modules, the only readers are tests.

## 3. Growth

Total identifiers stored across all formations, measured through the console:

```text
lines   events   formations   stored ids   ids/formation   growth
   25      127           26        1,625            62.5
   50      252           51        6,375           125.0    x3.92
  100      502          101       25,250           250.0    x3.96
  200     1002          201      100,500           500.0    x3.98
  400     2002          401      401,000          1000.0    x3.99
```

Identifiers per formation double as the line count doubles, and the total
converges on x4. Fitting `2.5 * n^2`:

```text
grammar_goold_brown.txt    108,194 lines     29,338,016,225 ids    ~323 GB
webster_dictionary.txt     974,256 lines  2,378,869,226,050 ids     ~26 TB
```

At roughly 11 bytes per identifier, before any storage overhead.

## 4. The copy is derivable from the boundary beside it

`#2371` established that session Standing is a forward fold over its filtered
event prefix in append order. If that holds, `consumed_event_ids` is precisely
the filtered prefix through `as_of_event_id`, and the copy carries nothing the
boundary does not already fix.

Tested directly, comparing each formation's stored list against the prefix
derived from its own recorded `session_standing_as_of_event_id`:

```text
mixed material (ordinary, empty, non-ASCII, code-shaped)   5/5
empty session                                              1/1
60 grammar-book lines                                     61/61
```

Sixty-seven of sixty-seven, exactly equal. Including the first formation of a
session, where Standing is empty, `as_of_event_id` is absent, and the stored
list is correctly empty.

## 5. What active law says

**No clause requires it.** No sentence in the numbered chapters states what a
Presentation or emission must preserve as consumed Evidence. That is a bounded
absence across those chapters, not a prohibition.

**Two clauses say the copy establishes nothing.** `05.Evidence:19`:

> A consumer may rely on represented lineage where that is the bounded
> requirement, but must not treat a string, foreign key, **copied causation
> identifier**, or internally coherent lineage as verified provenance…

`05.Testimony:18`:

> coherence checks and **copied lineage fields do not turn testimony into
> established fact** or prove the testifying producer occurred.

So a longer list of copied identifiers is not stronger evidence than a shorter
one. Duplication is not corroboration.

**An inventory is a permitted View shape, not a required emission coordinate.**
`06.Representations:18`: "A View may be only a navigation artifact, inventory, or
provenance index when its contract asserts only source visibility, identity,
location, or faithful transformation."

## 6. The six questions

```text
1  what claim requires every prior session event id?
     none found in the numbered chapters

2  does the as-of boundary already bound the consumed Standing?
     yes, and §4 shows the copy is exactly derivable from it

3  Evidence of formation, provenance of Standing, or expanded lineage?
     expanded lineage — it is a restatement of what the boundary fixes,
     and 05.Evidence:19 denies copied identifiers provenance standing

4  does copying strengthen or duplicate?
     duplicate; 05.Testimony:18 states copies establish nothing

5  growth shape?
     quadratic, converging on x4 (§3)

6  smallest lawful replacement?
     the as-of boundary already recorded beside it, since it is
     already sufficient to derive the list
```

## 7. The same shape as `#2370`

```text
#2370   a bounded Representation was reached by rebuilding the
        whole workspace, once per attempt

here    a bounded Presentation records the whole session history,
        once per formation, beside the boundary that already
        determines it
```

Both are a bounded thing carrying the universe to establish something local.

## 8. What this does not establish

**That the copy should be removed.** This is a findings pass. Removal is a
runtime change with a test surface, and `test_preserved_material_later_referenceable`
and `test_operator_session_standing` both read the field.

**That derivability makes it lawful to drop.** §4 shows the list is
reconstructible from a recorded boundary. Whether reconstructibility satisfies
whatever the field was added to satisfy is not recovered, because §5 found no
clause stating what that was.

**That the fold property holds for goal-bearing sessions.** `#2371` recorded
the same limit. §4's derivation depends on it, and all three sessions tested
contain only the five live kinds.

**That the extrapolated storage is reachable.** The 323 GB figure assumes the
current console runs to corpus scale, which the remaining quadratic already
prevents.

**That this is the last such duplication.** Only Presentation formation was
examined.
