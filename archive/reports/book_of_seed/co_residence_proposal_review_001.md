# Co-residence without collapse: proposal review 001

Findings only. No runtime or Book amendment. This reviews a curator proposal
before it becomes work.

## The proposal

Not sixteen books concatenated into one corpus, but sixteen books preserved
inside one Seed, each bounded as its own source, measurements staying
source-bounded, and Compare then crossing between preserved subjects — so that
Seed might recover which sources behave alike without being told "these are
grammar books".

**The distinction between co-residence and concatenation is real and worth
holding.** `#2408` showed a reader's categories predicting nothing, so not
handing Seed those categories is right. Four things need checking first.

## 1. The `source:` node does not exist

Curator's topology places a source under Standing/Evidence with its findings
beneath it. **Nothing in the runtime carries that coordinate.**

**[measured]** `preserved_ingress_occurrences`
(`seed_runtime/preserved_material_measurement.py:159`) selects on
`workspace_id`, `session_id` and event kind. There is no source term.

**[measured]** An ingress occurrence *has* a `source` dimension, and it holds
something else. `seed_runtime/operator_ingress.py:323` records
`source=ingress_examination_event.id` — the prior event in the occurrence's own
lineage. The slot a reader would reach for is occupied by internal provenance,
not material origin.

**[measured]** Its `scope` is `workspace:{id};session:{id}`. Those are the only
boundaries an occurrence carries.

**[inference]** Sixteen books fed into one Seed today would be one
undifferentiated stream — the concatenation the proposal exists to avoid,
arrived at by accident rather than by choice. In `#2408` the sixteen were kept
apart by sixteen separate ledgers in a script, and their identity lived in a
Python variable name.

**The topology is a construction, not an arrangement.** Curator's diagram is
drawn as though the boxes exist and only need filling.

## 2. Session is not source

The mechanism that does exist is one session per book: `session_id` is threaded
onto every event and `preserved_ingress_occurrences` already filters by it.
That genuinely separates sixteen bodies of material without collapsing them.

**It separates bounded exchanges, not sources.** "This material arrived in this
exchange" and "this material came from Roget" are different accountable
responsibilities. Reading a session label as a source label is the
different-responsibility failure, and it would be invisible afterwards because
the two coincide in every run we would do.

**[inference]** What Seed could hold is sixteen distinctly preserved bodies of
material. That they are sixteen *books*, and which book each is, would remain
provenance the operator holds — the same standing `corpus/SOURCES.md` has, and
it says so in its own first lines: it exists "because nothing else will."

That is not an objection to the proposal. It is what the proposal would
actually deliver, stated so it is not later mistaken for more.

## 3. Which Compare, and whether it is blocked

Curator wrote "Compare across preserved subjects" without saying which. Two are
established distinct:

```text
  bounded testimony comparison            multiple testimonies compared with one another
  candidate equivalence compared with     one proposed relation tested against known grammar
  applicable relation grammar
```

**[measured]** The unresolved owner blocks the **second**.
`shape_b_compare_owner_and_continuation_recovery_001.md:171` records the exact
owner as "responsibly unresolved", and that report's questions are about the
attributed relation proposal and its relation grammar.

**[measured]** Comparing findings from Brown with findings from Roget is the
**first**. `05.Testimony:27` already carried a bounded comparison consuming
preserved findings as Prior Standing, relied on since `#2389`.

**So the proposal is less blocked than a blanket reading suggests — if it is
the first.** Curator should say which, because the two have different owners
and only one of them is gated. Naming "Compare" without the qualifier is how a
blocked act gets moved by association with an unblocked one.

## 4. The inventory question the operator actually asked

*"Are these works like kinds enough to push their comparisons across seed?"*

`01.Kinds:19` speaks to this directly, and it is a **positive** clause rather
than a refusal:

> A kind label, artifact form, characterization category, dataclass name,
> concordance entry, inventory row, or recurring report type may preserve a
> bounded standing distinction for the subject and consumer it names. It does
> not ... supply kind-specific production authority without preserved evidence,
> provenance, scope, confidence limits, Unknowns, and the applicable production
> or establishment boundary.

`corpus/SOURCES.md` is an inventory and its sixteen rows are inventory rows. The
clause does not block them; it lists what they need. Against that list:

```text
  preserved evidence          #2408, source-isolated                    have
  provenance                  SOURCES.md origin + conversion per row     have
  scope                       300-line window, d1, one criterion         have
  confidence limits           #2408 section 4 disclosures                have
  Unknowns                    #2408 section 2                           have
  production or establishment boundary                                   MISSING
```

**[inference]** Five of six are already supplied, largely by accident of having
written the disclosures down. The missing one is the whole question: what act
produces a cross-source finding, who owns it, and what standing it establishes.
That is section 3's question again, arriving from a different direction.

## 5. Where the consumer-first rule falls

**Preserving sixteen sources distinctly is evidence preservation**, and
evidence preservation is where consumer-first manufactures the outcome it
exists to prevent. It does not need a warranted consumer first.

**A cross-source Compare act is construction**, and it does.

**The proposal bundles them into one move.** Split, the first half can proceed
now and the second half waits on section 3. Bundled, the first half's exemption
would carry the second half across, which is the cardboard pattern in its usual
form: a producer built because something downstream was described.

## 6. What this does not establish

**That the proposal is wrong.** Sections 1 and 2 say it must be built and would
deliver less than its diagram shows. Neither is a refusal.

**That `operator_source_recovery.py` is the home.** It exists, it records
`operator.presentation.source_recovered`, and its subject is the source of a
presentation rather than the origin of material. A nearby name is where the
last several owner-fills went wrong, and this does not propose it.

**That one session per book is the right boundary.** It is the boundary that
exists. Nothing here establishes it as the correct one for this subject.

**That `#2408` supports composition either way.** It gave source-isolated
baselines. It said nothing about what happens when sources share a Seed.
