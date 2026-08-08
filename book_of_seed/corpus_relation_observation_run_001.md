# corpus through the operator console: run record 001

Testimony for a future session. `corpus/` is gitignored, so nothing in CI
exercises any of this and no test result records it. This file is the record.

```text
python -m scripts.measure_operator_console_corpus grammar_goold_brown.txt
python -m scripts.measure_operator_console_corpus grammar_goold_brown.txt --profile
```

Run 2026-08-08.

**This document replaces an earlier version that measured the wrong path and
reported "there is no speed problem".** That measurement was of a
developer-compiled probe which writes nothing; see
`developer_compiled_probe_register_001.md`. The correction is §3.

## 1. What is in `corpus/`

Three Project Gutenberg texts, none tracked by git (`.gitignore:7`).

```text
grammar_goold_brown.txt    6.4 MB     108,194 lines
webster_dictionary.txt    29.0 MB     974,256 lines
roget_thesaurus.txt        1.5 MB      26,254 lines
```

Nothing in `seed_runtime/`, `tests/`, `campaigns/`, or `scripts/` referenced
`corpus/` before this run.

## 2. The console is quadratic

Grammar-book lines fed to `run_persistent_operator_console`:

```text
  lines   events      wall   per line   growth
     25      127     0.11s       4.4ms
     50      252     0.31s       6.1ms    x2.79
    100      502     1.14s      11.4ms    x3.71
    200     1002     4.43s      22.2ms    x3.91
    400     2002    18.00s      45.0ms    x4.06
    800     4002    73.82s      92.3ms    x4.10
```

Doubling the input quadruples the cost, and per-line cost doubles at every
doubling. Fitted from the three largest points, `t = 1.13e-4 * n^2`:

```text
roget_thesaurus.txt         26,254 lines    21.6 hours
grammar_goold_brown.txt    108,194 lines    15.3 days
webster_dictionary.txt     974,256 lines     3.4 years
```

## 3. The correction

The first version of this record measured manifest -> structural projection ->
surface features -> relation observation and reported 2.4s for the grammar and
21.7s for the dictionary, concluding "there is no speed problem on this path"
and "the thing that was slow isn't on this road."

Both sentences were true and worthless. That chain writes no events and holds
nothing afterward, so its cost is not Seed's cost. The second sentence was the
diagnosis stated as reassurance: Seed was not on that road.

```text
                        probe chain      operator console
grammar_goold_brown          2.4s            15.3 days
webster_dictionary          21.7s             3.4 years
```

## 4. Where the time goes

Cumulative profile of one 300-line run, 29.4s wall:

```text
run_operator_ingress_attempt        300 calls     26.7s
  StateProjector.project            300 calls     26.2s   98% of the console
    project_from_state                            26.2s
      replay_events                               25.9s
        apply                   225,750 calls     25.5s
          project_operator_ingress_events
                                135,450 calls     23.1s
            dataclasses.asdict  135,450 calls     15.0s   51% of wall
            form_operator_ingress_addressable_material
                                 45,150 calls     12.7s
```

Per line of input, at 300 lines:

```text
state.apply                                    752 calls
project_operator_ingress_events                452 calls
form_operator_ingress_addressable_material     150 calls
dataclasses._asdict_inner                   10,986 calls
```

`run_operator_ingress_attempt` records about five events and then calls
`StateProjector(ledger).project(workspace_id)`, which builds a fresh empty
projection and replays every event recorded so far. Line *n* replays the events
of lines 1..*n*. That is the square.

The dominant cost inside the replay is that **addressable material is re-formed
for every past ingress occurrence on every replay**, and each formation deep
copies dataclasses through `asdict`. Half the wall clock is that copying.

Note that `project()` already delegates to `project_from_state`, the function
documented as supporting "safe incremental projection from a previously
validated snapshot". The incremental door is being used, from an empty
projection and the full event list, every time.

## 5. The open question that gates the fix

Unchanged from `#2367` and still unanswered:

> Does the full `StateProjector` replay perform a validation or refusal side
> effect that a narrow per-attempt projection would bypass?

Until that is answered the call cannot be replaced, because a narrow projection
that silently skipped a refusal would trade a slow console for an unsound one.

Two further targets are visible in §4 independently of that question: re-forming
addressable material for every past occurrence on every replay, and the `asdict`
deep copies it performs.

## 6. `state` in the projection machinery

Checked because the word is retired and the machinery is live.

**`ProjectionStoreCache` does not exist.** Zero occurrences in the repository.
What exists is `ProjectionStore` (Protocol), `InMemoryProjectionStore`,
`SQLiteProjectionStore`, and `StateCacheStatus`.

**`StateCacheStatus` carries no state.** Its six fields -- `cache_hit`,
`projection_version`, `snapshot_last_event_id`, `current_last_event_id`,
`incremental_replay`, `events_applied` -- are all projection, replay, or cache
bookkeeping. Substituting `ProjectionCacheStatus` loses nothing.

`seed_runtime/state.py` is 2,225 lines whose classes are
`_ProjectionInfluenceLineage`, `_ReplayScopeAssessment`, `_ReplaySelection`,
`ProjectionBuildDiagnostics`, `EntityRelationship`. A projection module wearing
a retired name. 1,216 `state*` identifiers remain across `seed_runtime/`.

## 7. What this run does not establish

**That the console is correct.** It is the proper path and it is quadratic.

**That the quadratic is only the projection call.** §4 identifies the replay as
the shape and addressable-material re-formation as the dominant constant. No
fix was attempted and no other call site was audited.

**That the extrapolations hold.** They are a two-parameter fit over six points
spanning 25 to 800 lines, extended three orders of magnitude. The shape is
solid; the years are indicative.

**That the probe chain is worthless.** §3 finds its measurements irrelevant to
Seed's cost, not that the code is wrong. See the register.

**That `state` should be renamed.** §6 establishes the word carries nothing in
`StateCacheStatus`. The 1,216 identifiers were not audited individually.
