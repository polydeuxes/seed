# Compare occurrence implementation form recovery 001

## Scope

This report records what form an implementation of candidate-versus-relation-grammar Compare may take, given that its owner remains unresolved. It authorizes no build. It amends no active Book law, runtime, or tests.

Two construction proposals were withdrawn in reaching it, and both are recorded rather than dropped.

### Correction record

A later round corrected four claims in the first version:

```text
1. it recovered `boundary invocation != Act occurrence` and then wrote
   "each invocation is an instantiated occurrence or is not one",
   contradicting the clause it had just cited. Restoring the word
   `invocation` for precision made the contradiction explicit rather
   than creating it

2. it stated that ownership "is recorded as local to each instantiated
   comparison" for candidate-versus-relation-grammar Compare. That is
   recovered for bounded testimony comparison only; the
   candidate-comparison owner remains unresolved. This is the same
   transfer corrected in PR 2287, recurring after the labels that made
   it visible were retired

3. it located the distinction between object fields and function
   arguments, which is a Python idiom rather than a constitutional
   boundary. An atomically constructed complete record is not dormant,
   and arguments can be accumulated before a call. The distinction is
   partial-or-dormant representation versus complete occurrence-local
   material

4. it claimed tests showing the path proceed demonstrate "the occurrence
   proceeding". They demonstrate the implementation path proceeding
```

Two further defects were caught in the same round by this report's own
first checks, both introduced by its author:

```text
5. it used `road`, which this same author excised from active law in
   PRs 2249-2266, in its own scope sentence

6. it presented a `forbidden` / `permitted` table. `permitted` grants a
   constitutional standing the report disclaims two sentences earlier
   ("the Book does not govern code shape"). Recorded now as what does
   and does not violate the recovered distinction
```

The retired report labels `Shape A` and `Shape B` are not used. The two comparisons are named directly:

```text
bounded testimony comparison
  — multiple independently preserved testimonies or findings
    compared with one another

candidate equivalence compared with applicable relation grammar
  — one proposed relation tested against grammar Seed already has
```

This report concerns the second.

## Withdrawn proposal 1 — a structure with required fields

This report's author proposed building an empty boundary carrying required coordinates, which would refuse to Compare while any remained unresolved, on the ground that refusal makes the gap behaviorally testable rather than documentary.

The objection that defeats it is ontological, not stylistic. No persistent candidate-versus-relation-grammar Responsibility is recovered for such a structure to represent. `candidate_versus_grammar_comparison_recovery_001.md` records its owner as **Unresolved** — *"not automatically the candidate producer, operator, presentation source, later consumer, or PESC report"* — and its Authority, act occurrence, producer, production occurrence, and result Consumer likewise Unresolved. Its purpose is recorded as local to the instantiated candidate rather than universally established.

The separate finding that an owner *is* local to each instantiated comparison belongs to **bounded testimony comparison**, and is not available here.

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

The withdrawal of proposal 1 does not require abandoning testable refusal. But an earlier version located the distinction in the wrong place — between object **fields** and function **arguments** — which is a Python idiom, not a constitutional boundary. An immutable record constructed atomically from complete material represents no dormant Responsibility; function arguments can equally be accumulated, cached, or defaulted before a call. Neither code form is required or forbidden.

The distinction is semantic:

```text
partial or dormant Responsibility representation
!= complete occurrence-local material
```

What must not exist is a representation standing in for a Responsibility before every constituting coordinate is warranted. What does not violate the distinction is complete occurrence-local material, in whatever form. This report grants nothing; it records which forms the recovered grammar already rules out:

```text
violates the distinction    a partial instance
                            a missing-coordinate sentinel
                            a default owner
                            any object treated as an existing
                            Responsibility before its constituting
                            coordinates are warranted

does not violate it         complete occurrence-local material, whether
                            carried as arguments to one call or as an
                            atomically constructed immutable record
```

This is an implementation-form finding derived from recovered constitutional grammar. It is not itself recovered law, and the Book does not govern code shape.

**And the implementation boundary is not the occurrence.** `02.Acts` states it directly, in the context of exactly this question — *"Current Python functions and methods witness such boundaries; they are not the constitutional definition of act occurrence"*:

```text
boundary invocation != assertion-bearing branch
                    != result construction
                    != external effect
```

So a call carrying complete attributed material may run, produce an implementation result, and witness a boundary. It does not thereby establish a constitutional Compare occurrence. That still requires its own Evidence — exact inputs, exact owner and Authority, the call boundary, the observed Act, the produced result, and preserved lineage.

Refusal therefore remains demonstrable, but what a test demonstrates is narrower than an earlier version claimed:

```text
tests can establish     all required material supplied
                        → the implementation path proceeds

                        owner omitted
                        → the path refuses

tests cannot establish  a constitutional Compare occurrence happened
```

## Constraints that survive

**Refusal must be structural.** No default, optional coordinate, or sentinel may satisfy the boundary:

```text
owner=None
owner="unknown"
owner="operator-ingress"
owner=DEFAULT_OWNER
```

If any of these lets the implementation path proceed, the gap closes by convention rather than by warrant, which is the laundering the withdrawal was meant to prevent.

```text
missing required coordinate  → no candidate Compare occurrence can be warranted
complete material supplied   → the implementation boundary proceeds
implementation proceeds      != constitutional occurrence established
```

`unresolved` must also not become a runtime value. Per the root it belongs to an *instantiated* coordinate whose value has not been resolved. Before an exact Responsibility is instantiated there may be no coordinate present to call unresolved at all, and `unresolved` supplied as an argument would be a missing-coordinate sentinel by another name.

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

That is precisely the register this section needs, so the word is used here rather than avoided — but only in that register:

```text
invocation may witness an implementation boundary

invocation != Act
           != Act occurrence
           != result production
```

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

- No pre-instantiated or partially populated candidate-versus-relation-grammar Compare Responsibility is recovered, so there is nothing for a container to represent before its constituting Evidence.
- The exact owner of any candidate-versus-relation-grammar Compare occurrence remains **unresolved**. Occurrence-local ownership is recovered for *bounded testimony comparison* only and must not be transferred here.
- A recognizer act relocates the unresolved owner rather than closing it, and is the sixth such relocation in this thread.
- The constitutional constraint is `partial or dormant Responsibility representation != complete occurrence-local material`. It is semantic, not a choice between arguments and fields; either code form can satisfy or violate it.
- A call carrying complete material witnesses an implementation boundary. It does not thereby establish a constitutional Compare occurrence, which requires its own Evidence.
- Structural refusal, the unresolved/Unknown distinction, and act-derived naming remain required.

## Unsupported findings

- That an implementation is presently authorized.
- That a test fixture supplying coordinates establishes any warranted Compare.
- That the form recorded here is recovered law rather than a form derived from recovered grammar.
- That a passing refusal test establishes a constitutional Compare occurrence, or that a call is one.
- That occurrence-local ownership recovered for bounded testimony comparison applies to candidate-versus-relation-grammar Compare.
- That the owner is absent — it remains unresolved.

## Unresolved coordinates

- The exact owner of candidate-versus-relation-grammar Compare, and whether an exact occurrence's Evidence instantiates one.
- The exact Authority, Warrant, occurrence Evidence, result Producer, production occurrence, Standing-establishment boundary, and later Consumer for that Compare.
- What consumes a bounded result, and what it produces that makes another such Compare applicable.

## Disposition

```text
container form                    withdrawn
recognizer act                    withdrawn
fields-versus-arguments framing   withdrawn

partial or dormant Responsibility representation
!= complete occurrence-local material
                                  consistent with recovered grammar

invocation != Act
           != Act occurrence
           != result production   recovered

structural refusal                required
unresolved/Unknown distinction    required
unresolved as a runtime value     forbidden
act-derived naming                required

candidate-comparison owner        unresolved
implementation                    not authorized; owner unresolved
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
