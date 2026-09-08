# Handoff — visitor session, 2026-08-10

Written for the model taking over. The operator is `poly`; a separate **curator**
session reviews this work and relays through the operator; **codex** implements
corpus changes. This session is **the visitor**: independent adversarial reviewer
of curator's reasoning and of committed output, with standing warrant to write
and commit reports and implementation directly.

## Read these first

**`/home/user/.claude/projects/-home-user-seed/memory/`** — 46 files, indexed by
`MEMORY.md`. That index is loaded into context automatically each session; the
individual files are not, so read the ones the index points you to. They are the
accumulated corrections, most of them recording a mistake this session made and
was caught on. `feedback_*` are the sharpest.

The ones that would have prevented the most damage:

```text
feedback_developer_probe_is_not_the_evidence_probe   generic != evidence-born
feedback_corrections_do_not_propagate                fix the body, leave the heading
feedback_naming_does_not_supply_the_owner            6 instances, all withdrawn
feedback_absence_is_not_an_argument_against_building recovery standards != construction
feedback_empty_result_is_not_absent_occurrence       and its 2026-08-09 second instance
```

Write memory **often** — the operator asked for that explicitly. Conservatism is
for content, not frequency.

## The two Seeds

### Test Seed — complete, reported in `book_of_seed/test_seed_report_001.md`

```text
store       /dev/shm/seed-scratch/real_c.db     4.95 GB, 898,787 events
subject     16 source windows of 300 lines each, one bounded exchange per window
A = B       identical finding sets alone and co-resident, every displacement
C           720,881 comparison occurrences, every one bounded relation Unknown
D           83,351 distinctions counted over those comparisons
```

Two known unfaithfulnesses, recorded not hidden: `bash_guide` is 5.4% of its
source (console escape, fixed after this store was built) and `latin_vulgate` is
the English Douay-Rheims, which withdrew `#2408`'s non-English finding.

**Running right now:** `scratchpad/D2.py` re-runs D against this store with the
`#2441` memory fix. At last check 21.8 GB / 12 min, output to
`scratchpad/D2.txt`. Compare against the pre-fix shape: 34 GB, 26 min, no result.
If it still climbs past ~30 GB, kill it — the per-exchange fix reduced the peak
but may not have reduced it enough, and `list_session_kind` is the next lever.

### Acquisition Seed — **not started**, ready to launch

```text
runner      scratchpad/acq2.py       27 sources, ingest only
target      /dev/shm/seed-scratch/acq_seed.db
expect      ~7.5M events, ~8 GB, ~1 hour at the measured ~2,000 events/s
```

Everything it needs is in place: `process_boundary_escape=False` so no source
truncates, per-source completeness checked and printed as `INCOMPLETE` if a
source falls short, a manifest with sha256/lines/words/session per source, and
the Book of Seed as source 27 at revision `6aac38e` recorded as *"testimony;
holds Authority in its own subject and none over Seed's projection"*.

Launch: `nohup timeout 20000 .venv/bin/python -u scratchpad/acq2.py > scratchpad/acq2.txt 2>&1 &`

**Do not measure or compare on it yet.** Ingest is linear in line count;
findings and comparisons are not, and the prospective cardinality at full source
extent is unknown. The operator's plan is ingest, then inspect cardinality
before producing anything.

## Where the work actually stands

The constitutional seam, which is the real subject:

```text
measurement  ->  Compare  ->  ????  ->  relation  ->  warranted Standing
```

Every cross-exchange comparison returns `Unknown` **by design**, and that refusal
is the result rather than a limitation. `01.Standing.D` refuses relation standing
to co-presence. What is genuinely open is what responsibly converts comparison
Evidence into a relation — and **do not assume it is Compare**. Curator's
correction: making Compare smarter because Compare is where the gap was noticed
is `naming does not supply the owner` in a new costume.

One coordinate remains Unknown in the measurement family: the **production
Responsibility**. `#2423` recovered `production owner: none found` for declared
measurement. The **Producer** is separate and is recovered — `producer: this
Seed`, verified by the recorded producing occurrence. Do not let owner swallow
Producer again; that compression cost four documents.

## Open branches, all rebased onto `b6cf0d4`

```text
per-exchange-materialization   the memory fix, just pushed, unreviewed
book-lexical-gate              RED BY DESIGN, 290 violations, needs an operator decision
verb-survey
stopping-surface-witness
ingress-declared-boundary-audit
predicate-cat-test
external-material-relation-observation
```

The `codex/*` and `agent/*` branches are not this session's and are hundreds of
commits behind; leave them.

## Working rules the operator enforces

**Rebase before every handoff and after every pull.** This session was told
three times. `git fetch --prune` too — without it, merged-and-deleted branches
read as open and you will report a stale list.

**Verify what arrived, not what you requested.** Two sources this session were
confidently wrong: a "Latin Vulgate" that is English, and an "American Standard
Version" that is *The Allis Family*. Read every downloaded file's own title.
A successful download is not a verified identity, and one mislabelled source
produced a published conclusion that survived four reports.

**Measure both arms under the same conditions.** Two benchmark errors this
session came from comparing against a baseline taken under different disk load.

**Commit before reporting done.** Twice this session I described work the
operator could not see because it sat uncommitted.

**The most frequent defect:** a claim written next to code that contradicts it —
a report disclaiming an arity the code had, a schema check validating something
adjacent to its own invariant, prose keeping a scope the grouping dropped, a
console announcing an escape it was not enforcing. Four instances. Compare the
claim to the code, not the claim to your intention.

## Vocabulary

The Book has banned families enforced by `tests/test_book_lexical_contamination.py`
— `execut*`, `suffi*`, `state`, `learn*`, `translat*`, `operation*`, `method*`
and more. They leak into casual conversation first and reports second. `artifact`
is not banned but was found to name no distinction of its own, so it is worse to
use loosely than an ordinary word; that is recorded in the gate's considered list.

Never write `relation`, `agreement`, `corroboration` or `independent` about
measured co-presence. Bodies here are *independently preserved*, which is not
independent sources.
