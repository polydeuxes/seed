# Orientation-attempt observable Evidence recovery 001

## Scope

This report resolves one question:

```text
What exact repository-visible Evidence must distinguish

  Seed attempted to relate new free-form material
  to its available grammar and could not establish
  a stronger relation

from

  Seed never attempted?
```

It amends no active Book law, runtime, or tests. `bounded grammar orientation` is used only as report-level shorthand and no orientation Responsibility is created.

Prior cause is not reinvestigated: PR 2276's implementation prompt prohibited Compare, so the omission of the middle road was instructed rather than a defect of that implementation.

### Correction record

The first version of this report contained four errors, recorded rather than silently replaced:

```text
1. it omitted Seed's available grammar from the consumed materials,
   and so recovered comparison across operator utterances instead of
   the candidate-versus-grammar road recovered in PRs 2267-2270

2. it claimed E1 necessarily has an empty candidate set because every
   01.External.E finding is relational; several are not

3. it declined to create an orientation Responsibility and then proposed
   an `orientation-attempt` runtime event named after the same
   report-level shorthand, with no established owner or act

4. it preserved `candidate-production occurrence != candidate` and then
   collapsed it, treating zero candidates as no production occurrence
```

The materials, the E1 claim, the proposed event, and the implementation slice did not survive that round.

A second correction then replaced the evidentiary core itself:

```text
5. it claimed the ledger is the only repository-visible Evidence surface,
   and inferred that without a recorded occurrence "attempted" and
   "never attempted" are indistinguishable

   constitutional_event_projection_persistence_boundary_001.md establishes
   that a result may remain transient when bounded to immediate live use,
   recomputable from preserved inputs, or not needed for cross-tick
   recognition. Candidate production and Compare at first contact meet all
   three. The distinction must hold inside the live road, not in durable
   history.
```

A third correction then narrowed two claims made while making the second:

```text
6. it claimed candidate formation and Compare satisfy every condition for
   remaining transient, including full recomputability from preserved
   inputs

   the criterion is disjunctive, so only one condition is needed; and
   recomputability is not established, since exact recomputation would
   also require the grammar, method, scope, and as-of boundary at that
   occurrence, and Seed's available grammar is expected to change

7. it treated a focused test as repository-visible Evidence that the road
   occurred

   a test evidences that the implementation contains and consumes the
   road; it is not Evidence of any particular runtime occurrence
```

A fourth correction then fixed two boundaries introduced by the third:

```text
8. it treated a live intermediate artifact as occurrence-local Evidence

   result existence is not Evidence of its producing occurrence. Active
   law preserves this as `act != artifact describing an act`, and in the
   Fact-artifact and Fidelity-artifact clauses. The call boundary, exact
   inputs, returned result, and preserved lineage together may evidence
   the occurrence; the artifact alone cannot.

9. it said losing the intermediates destroys no unique historical
   Evidence because the operator material is durably recorded

   that reasoning depends on the recomputability the same round withdrew.
   The transient result may be unique and later irreproducible. Its loss
   is lawful because no later Consumer depends on it, not because the
   ingress preserves it.
```

What survives all four rounds is narrower and stated below: the current rendering is a constant and therefore cannot reflect any act, whether transient or recorded.

## Recovered owner and Consumer-purpose

**Unresolved, not absent.** The general recovery leaves ownership local to each instantiated comparison, so an unresolved general owner does not establish that this instance cannot supply one.

`candidate_versus_grammar_comparison_recovery_001.md` records, for the exact shape at issue here:

```text
Candidate producer                        Unresolved
Owner of candidate-versus-grammar question Unresolved
Authority                                  Unresolved for the general shape
Act occurrence                             Unresolved until an exact responsible
                                           occurrence performs Compare
```

The BOGE recovery independently found that *"candidate-production ownership remains unresolved in attributed testimony."*

Implementation adds nothing. `seed_runtime/candidate_external_grammar.py` preserves **caller-supplied** candidates — its own boundary notes state *"Candidate grammars are caller-supplied structural hypotheses"* and *"Supporting and contradicting testimony relationships are preserved, not evaluated"* — produces none, and contains no reference to operator ingress. `run_operator_ingress_attempt(...)` owns the ingress road and stops at projection.

Consumer-purpose is available: the console owns *"process-local repetition around bounded operator interactions"*, holds an open output stream, and already responds on decoder failure. That establishes an available candidate Consumer boundary. It does not supply the missing owner.

## Exact materials

The first version omitted the material the question is actually about.

```text
Seed's available constitutional grammar
  — the relation grammars presently recoverable to Seed, against which
    a candidate equivalence could be tested

the exact presentation
  — addressable material exact_text, provenance, scope, known_loss,
    unknowns, authority_warrant ("occurrence-only; meaning Unknown")

the exact interaction
  — attempt event ids, ordering, session and workspace scope

prior preserved operator-origin material
  — available for cross-utterance findings, but not the primary material
```

Omitting the first item is what turned the inquiry into comparison across operator utterances. The recovered road is candidate-versus-grammar, not testimony-versus-testimony, and those were established as non-identical instantiated Responsibilities.

## What the road requires, and what is named

There is no established Act named orientation. Exactly one Act on this road is recovered:

```text
Compare    "Compare the candidate equivalence with the applicable
           relation grammar" — recovered as Shape B, explicitly
           non-identical to testimony-versus-testimony comparison
```

Compare tests an **already-produced** candidate. The Act that forms the candidate is not recovered.

`candidate production` is not that Act. The candidate-versus-grammar recovery treats production as Responsibility topology concerning producer, production occurrence, and result, and states directly that production is not the exact Act's name. `01.External.F` governs what a candidate must preserve — producer, source-role, formation-occurrence, scope, authority, provenance — not who forms it.

```text
production                != exact responsible Act
candidate production      != candidate-forming Act by identity
```

Any occurrence, transient or recorded, must be an occurrence *of an exact Act under an exact Responsibility*. Naming one after report-level shorthand, or after a topology branch, testifies to nothing.

## Candidate production at E1

The first version claimed E1 necessarily produces no candidates because every permitted finding is relational. That is wrong. `01.External.E` permits findings *"within its measurement boundary"*, and a single material can be that boundary — count, intra-material recurrence, prefix occurrence, and declared predicates all operate on one material without a prior utterance.

More importantly, measurement findings are not the candidate-versus-grammar road at all. Whether a candidate equivalence can be formed for `Hello` against Seed's available grammar is not answered by counting bytes.

The corrected position:

```text
E1 candidate set: not established as empty, and not established as non-empty

E2 is the first point at which cross-utterance findings become available,
which is not the same as the first point a candidate becomes possible
```

## Empty candidate set as a production result

The first version treated zero candidates as no production occurrence, collapsing a distinction it had just preserved. The corrected reading:

```text
the exact candidate-forming Act occurred
→ production occurrence
→ bounded result: empty candidate set
```

is distinct from:

```text
no candidate-forming Act occurred
```

This removes the reason the first version invented a separate event: a production occurrence carrying an empty result already distinguishes attempted from not-attempted, with no new act.

Two things remain unresolved and are not settled by this correction: what the exact candidate-forming Act is, and who performs it. The phrase `candidate-production Act`, used in the second version of this report, is withdrawn — it named a topology branch as though it were the Act.

## Observable Evidence

The first two versions demanded durable history. That was the wrong requirement.

`constitutional_event_projection_persistence_boundary_001.md` establishes the boundary:

> An occurrence must enter durable history when later reconstruction, provenance, audit, authorization state, execution history, evidence observation, fact observation/inference, pending action state, or other cross-tick recognition depends on the occurrence as unique historical evidence.

> A result **may remain transient** when it is bounded to immediate live use, does not need cross-tick recognition, is fully recomputable from preserved inputs, or is intentionally only renderer/operator progress visibility.

That criterion is **disjunctive**. A result need satisfy only one of its conditions, not all of them.

Candidate formation and Compare at first contact satisfy the first two:

```text
bounded to immediate live use     the result is consumed by the response
                                  being formed in the active interaction

no cross-tick recognition needed  no later projected recognition presently
                                  depends on preserving the intermediate
```

That is sufficient on its own.

It is **not** sufficient to say the intermediates may be lost because the operator material is durably recorded. That reasoning depends on recomputability, which is withdrawn below. The exact transient result may be unique and later irreproducible, since Seed's grammar and method may change.

The lawful position is narrower:

```text
the exact transient result may be permanently lost

that loss is lawful after immediate consumption, where no later
reconstruction, provenance, accountability, or cross-tick recognition
depends upon that result surviving
```

```text
durable preservation unnecessary
!= exact result non-unique

transient result discarded after consumption
!= result reconstructible
```

**Recomputability is not claimed.** An earlier version asserted these results are fully recomputable from the preserved ingress and Seed's available grammar. That is not established, and exact recomputation would additionally require preserving:

```text
the exact grammar available at that occurrence
the exact candidate-forming method and its identity or version
the exact scope and as-of boundary
any other transient inputs consumed
```

Seed's available grammar is expected to change, so a later recomputation from the same ingress may not reproduce the same result. Recomputability is therefore instance-local and unresolved. It is also unnecessary, because the first two disjuncts already hold.

So:

```text
candidate formed        != Event required
Compare occurred        != Event required
no relation warranted   != Event required
```

The distinction must hold **inside the live road**, not in the ledger. The correct test is therefore not whether history differs, but:

```text
does the result reaching the response Consumer
vary with what actually occurred?
```

The current implementation fails that test, and this is what survives from both prior versions. `"Communicative meaning: unresolved (Unknown)."` is an unconditional literal in `operator_ingress_view.py`, and `UNKNOWNS` is a module-level constant tuple in `operator_ingress_addressable_material.py`. Neither can vary. The response would be byte-identical whether Seed formed candidates and compared them or did nothing at all — not because the acts went unrecorded, but because nothing downstream consumes their result.

Both constants remain correct as honest declarations of the preservation boundary's own limits. They are wrong only where a produced result should have taken their place.

Four kinds of Evidence are distinct here. Earlier versions conflated the first with the third, then the second with the third:

```text
focused tests           Evidence that the implementation contains and
                        connects the live road — not Evidence that any
                        particular runtime occurrence happened

live result artifact    the exact material consumed by the immediate
                        Consumer — its existence alone evidences nothing
                        about the Act that produced it

live occurrence         Evidence supporting that the exact Act and its
Evidence                production occurrence happened — the call
                        boundary, exact inputs, returned result, and
                        preserved lineage together, not the artifact alone

Event Ledger            durable historical Evidence — unnecessary unless
                        the occurrence must survive as history
```

The second and third must not be collapsed. Active law preserves this in three places: `act != artifact describing an act`; *"A Fact artifact does not prove its own Fact standing"*; and *"A Fidelity-shaped artifact does not prove that this bounded comparison responsibility occurred."* A candidate or comparison result existing is not Evidence that candidate formation or Compare occurred.

A test supplying different material and asserting a correspondingly different response establishes that the road exists and is consumed. It says nothing about any specific occurrence, and substitutes for none of the other three.

Durable recording becomes warranted later, at the first occurrence whose loss would destroy the only support for something established — a warranted relation, with its subject, supporting coordinates, candidate provenance, comparison result, Warrant, scope, and Standing. In the worked examples that plausibly falls partway through E3, not at E1.

## Bounded result and Standing

| Case | Result | Standing |
|---|---|---|
| candidate-production occurs, empty result | production occurred; no candidate formed | occurrence-only; unresolved coordinates preserved unchanged |
| candidate produced, no applicable relation grammar | candidate preserved with its `01.External.F` production dimensions | candidate standing only; absence of applicable grammar is not Unknown by identity |
| Compare occurs, no relation warranted | bounded comparison result | bounded relation standing inside the comparison boundary; not falsehood |
| Compare occurs, bounded relation warranted | bounded comparison result for the exact coordinate | bounded relation standing only; not truth, meaning, reliance, or Authority |

No case establishes communicative meaning, operator intent, goal, Demand, or Authority carried by the material.

## Finding/response Consumer

No existing relation consumes these results. Once such an occurrence were admitted into the attempt projection, the existing View would be positioned to render it, since the View already consumes the projection.

Positioning is not performance. A View exposing a produced result is not response formation:

```text
View can expose a bounded result
!= response formation completed
!= composition
!= presentation
```

A richer diagnostic View must not drift back into being treated as Seed's completed response.

Whether these results are `findings` in the Book's sense is not settled here. `01.External.D` reserves *Fidelity finding* for a bounded comparison of constitutional grammar, a bounded expectation, and an implementation witness — a different subject.

## E1 / E2 / E3 trace

**E1 — `Hello`.** One preserved material. Whether a candidate equivalence can be formed against Seed's available grammar is unresolved, because no owner exists to attempt it. Intra-material measurement findings are available but are not the candidate-versus-grammar road. The observable difference between tried and not-tried remains unevidenced, and cannot be evidenced until the act has an owner.

**E2 — `Learn English`.** First point at which cross-utterance findings become available: exact equality (false), difference, recurrence across E1 and E2, ordering. This does not establish that E2 expresses a goal, Demand, or instruction — `01.External.E` states such findings *"do not establish structural, grammatical, or semantic meaning."*

**E3 — corpus.** Substantially more material within and across events. More candidates become producible in principle and Compare may become applicable for exact coordinates. Semantic establishment still requires a separate responsible occurrence under `01.External.A`, which translation and recurrence explicitly do not supply.

## Earliest missing implementation boundary

The insertion point identified in the first version is confirmed and unchanged. In `seed_runtime/operator_ingress.py`, between:

```python
_record(ledger, "operator.ingress.ingress_occurred", ...)
```

and:

```python
state = StateProjector(ledger).project(workspace_id)
```

Admission is governed by a closed whitelist in `project_operator_ingress_events(...)`; four `operator.ingress.*` kinds are admitted and anything else raises `ValueError`. `stopping_occurred → interaction_closure` is the existing pattern for a subject-bearing kind.

This locates *where* an occurrence would be recorded. It does not establish *what* may be recorded there.

## Smallest implementation slice

No slice is proposed here, and no new Event kind is warranted at first contact.

The remaining blocker is narrower than the second version stated. It is not that a recorded occurrence needs an owner — no recording is required. It is that the exact Act forming a candidate equivalence from ingress material and Seed's available grammar is itself unrecovered:

```text
production
!= exact responsible Act

candidate production
!= candidate-forming Act by identity
```

The candidate-versus-grammar recovery names Compare as the Act that tests an already-produced candidate. It leaves the Act that forms the candidate unresolved, and treats production as Responsibility topology concerning producer, production occurrence, and result. The second version of this report withdrew one invented Act and then substituted `candidate-production Act`; that substitution is withdrawn here.

Ownership is likewise unresolved rather than absent. The general recovery leaves it local to each instantiated comparison, so its being unresolved in general does not establish that this instance cannot supply one. This instance already supplies substantial local coordinates:

```text
subject              exact free-form ingress material
Consumer-purpose     form a bounded response during the active interaction
Consumer boundary    available operator through the console
scope                exact workspace, session, attempt, interaction
comparison material  exact presentation plus Seed's available grammar
```

The prerequisite recovery is therefore:

```text
what exact Act forms candidate equivalences from operator-ingress
material and Seed's available grammar

what exact local Responsibility owns that Act during the active
free-form interaction, and whether the coordinates above instantiate
an already-owned one
```

Once that is answered, the shape available is a **live transient road** requiring no ledger addition:

```text
ingress projection
→ candidate formation
→ Compare where candidates exist and are applicable
→ bounded result
→ response formation
→ composition, presentation, rendering, emission
```

with durable recording deferred to the first occurrence establishing something whose later reconstruction depends on it.

## Files likely changed

None yet. When the prerequisite is answered, the change is expected to be live-road wiring plus tests rather than a new event kind or projection coordinate.

## Vocabulary or architecture explicitly rejected

```text
orientation Responsibility        not created
orientation-attempt event kind    withdrawn; it was the same shorthand
                                  re-entering as an ownerless runtime occurrence
trigger / invocation              rejected; killed PRs 2176 and 2180 here
prerequisite-invocation           rejected
presentation-permission producer  rejected
diagnostic Consumer family        rejected
generic semantic interpreter      rejected
universal interaction pipeline    rejected
general compare-everything act    rejected; both active Compare clauses are
                                  subject-bounded
finding as a name for these       not adopted; would need separate recovery
```

`capture` and `examine` appear only as quoted implementation identifiers.
