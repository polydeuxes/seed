# Compare occurrence implementation form recovery 001

## Scope

This report records what form an implementation of candidate-versus-relation-grammar Compare may take, given that its owner remains unresolved. It authorizes no build. It amends no active Book law, runtime, or tests.

Two construction proposals were withdrawn in reaching it, and both are recorded rather than dropped.

The retired report labels `Shape A` and `Shape B` are not used. The two comparisons are named directly:

```text
bounded testimony comparison
  — multiple independently preserved testimonies or findings
    compared with one another

candidate equivalence compared with applicable relation grammar
  — one proposed relation tested against grammar Seed already has
```

The road under construction concerns the second.

## Withdrawn proposal 1 — a structure with required fields

This report's author proposed building an empty boundary carrying required coordinates, which would refuse to Compare while any remained unresolved, on the ground that refusal makes the gap behaviorally testable rather than documentary.

The objection that defeats it is ontological, not stylistic. There is no persistent Responsibility for such a structure to represent. `candidate_versus_grammar_comparison_recovery_001.md` records for bounded testimony comparison:

> The exact owner **is local to the instantiated comparison** and is not named universally.

and leaves the candidate-versus-grammar owner Unresolved. Purpose, comparison basis, comparison Authority, and Consumer are likewise recorded as local to each instance rather than universally established.

So the coordinates are not values poured into a waiting container. They are what constitutes the Responsibility. An object holding empty slots asserts that a Responsibility exists prior to the Evidence that would instantiate it.

```text
Responsibility with unfilled coordinates
!= Responsibility awaiting values

no exact Evidence
→ no instantiated Responsibility to represent
```

## Withdrawn proposal 2 — a Compare recognizer

The replacement proposal was to build the capability to observe available material, determine whether an exact Compare Responsibility is evidenced, and perform the occurrence where it is.

That determination is itself an act. It requires its own owner, Authority, Evidence, purpose, and occurrence, none of which is recovered. The proposal relocates the unresolved owner one level up rather than closing it.

This is the recurring failure of the surrounding thread. Each time an owner could not be found, a new act was named to stand where it was missing:

```text
orientation-attempt event
candidate-production Act
Project as the candidate-forming Act
constitutive lens
R requires resolution of U
Compare recognizer
```

Every one was withdrawn. The pattern is not that any particular name was poor. It is that naming an act does not supply the owner whose absence prompted the naming.

## The implementable distinction

The withdrawal of proposal 1 does not require abandoning testable refusal. The distinction is between required **fields** and required **arguments**, and it is implementable:

```text
container form     an object exists with owner, Authority, and Evidence
                   slots, initially unfilled, awaiting later values.
                   A Responsibility persists between invocations.

occurrence form    no object persists. An invocation either carries every
                   exact coordinate or does not happen. Each invocation is
                   an instantiated occurrence or is not one.
```

The second asserts nothing between invocations. It has no dormant Responsibility, no owner slot awaiting discovery, and no partial instance. It also keeps refusal demonstrable: a test supplying complete coordinates shows the occurrence proceeding, and a test withholding any one shows it not occurring.

This is an implementation-form finding derived from recovered constitutional grammar. It is not itself recovered law, and the Book does not govern code shape. It is recorded as the form consistent with what the grammar establishes.

## Constraints that survive

**Refusal must be structural.** No default, optional coordinate, or sentinel may satisfy the boundary:

```text
owner=None
owner="unknown"
owner="operator-ingress"
owner=DEFAULT_OWNER
```

If any of these permits an occurrence, the gap closes by convention rather than by warrant, which is the laundering the withdrawal was meant to prevent.

**`unresolved` and `Unknown` must remain distinguishable.** The Responsibility root:

> An instantiated coordinate whose value has not been resolved **remains unresolved** unless a responsible occurrence positively establishes Unknown.

So unresolved is the default and requires nothing; Unknown is a positive value supplyable only where a responsible occurrence has established it for that exact coordinate. An implementation that accepts `Unknown` as a convenient stand-in for unfilled erases the distinction.

**A recorded false positive: `invocation` is not banned.** An earlier draft of this report removed the word, believing it forbidden because it appears on several prompt do-not-introduce lists and was retracted at one position by PR 2181. That was wrong, and the removal replaced a word appearing in a clause title with a vaguer one — inside a report arguing for naming precision.

`invocation` is established in active law:

```text
06.Projection.C — Rebuildability and prior invocation boundary   (clause title)
02.Acts:13   boundary invocation != assertion-bearing branch
             != result construction != external effect
06.Projection:38-39   rebuildable projection != prior invocation reconstruction
                      reconstructable current condition
                      != irrecoverable historical invocation
01.Uptake anchor  seed_runtime/constitutional_pipeline.py::invoke_constitutional_pipeline
```

PR 2181's finding was that PRs 2176 and 2180 *"incorrectly treated `trigger`, `invocation`, ... **as if they named recovered constitutional acts**"* — the defect was treating the word as recovered at that position, not the word's standing.

What `invocation` names across those uses is consistent: **a code-level call or run, offered as implementation testimony, proving nothing constitutional.** `02.Acts` states its context directly — *"Current Python functions and methods witness such boundaries; they are not the constitutional definition of act occurrence"* — and separates boundary invocation from external effect. `06.Projection.C` uses it for a prior projection run, citing elapsed duration and cache condition at that historical invocation.

That is precisely the register this section needs, so the word is used here rather than avoided.

Two lessons carried forward: a prompt's banned list is scoped to that report and is not a claim about Book standing; and over-banning is its own failure mode, producing vaguer language in the name of discipline.

**Naming must come from the Act and its exact subjects**, not from working shorthand. `cup`, `faucet`, `Shape A`, and `Shape B` were conversational handles and are retired. A name such as `compare_candidate_with_relation_grammar` is descriptive; `ShapeBCompare` or `CompareCup` would install a metaphor as repository architecture.

## What this does not authorize

No build follows from this report.

The owner of candidate-versus-relation-grammar Compare remains unresolved, so no call carrying every required coordinate can presently be formed outside a test fixture. This report constrains the form such an implementation must take **when** the owner is recovered. It does not supply the owner, and it does not make the occurrence presently instantiable.

```text
implementation form constrained
!= implementation authorized

test fixture may supply coordinates
!= coordinates responsibly supplied in operation
```

A test that supplies an artificial owner demonstrates the refusal boundary. It does not establish that any real Compare is warranted, and the existence of such a fixture creates pressure to supply the same value in operation. That pressure is the specific risk this report's structural-refusal constraint exists to resist.

## Supported findings

- No persistent candidate-versus-relation-grammar Compare Responsibility exists to be represented by a container; ownership is recorded as local to each instantiated comparison.
- A recognizer act relocates the unresolved owner rather than closing it, and is the sixth such relocation in this thread.
- Required arguments without a persisting object satisfy both the absence of a prior Responsibility and the requirement that refusal be demonstrable.
- Structural refusal, the unresolved/Unknown distinction, and act-derived naming remain required.

## Unsupported findings

- That an implementation is presently authorized.
- That a test fixture supplying coordinates establishes any warranted Compare.
- That the occurrence form is recovered law rather than a form derived from recovered grammar.
- That the owner is absent — it remains unresolved.

## Unresolved coordinates

- The exact owner of candidate-versus-relation-grammar Compare, and whether an exact occurrence's Evidence instantiates one.
- The exact Authority, Warrant, occurrence Evidence, result Producer, production occurrence, Standing-establishment boundary, and later Consumer for that Compare.
- What consumes a bounded result, and what it produces that makes another such Compare applicable.

## Disposition

```text
container form                 withdrawn
recognizer act                 withdrawn
occurrence form                consistent with recovered grammar
structural refusal             required
unresolved/Unknown distinction required
act-derived naming             required
implementation                 not authorized; owner unresolved
```

## Vocabulary explicitly retired

```text
Shape A
Shape B
cup
faucet
Compare recognizer
CompareCup
ShapeBCompare
```

These may remain in prior reports as acknowledged shorthand. They are not constitutional terms and must not become implementation names.

**Not retired, and not banned:** `invocation`. It is established active-law vocabulary for a code-level call or run offered as implementation testimony. See the false positive recorded above.
