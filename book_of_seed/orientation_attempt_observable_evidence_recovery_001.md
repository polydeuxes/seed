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

It amends no active Book law, runtime, or tests. `bounded grammar orientation` is used only as report-level shorthand; it is not active constitutional vocabulary and no orientation Responsibility is created here.

Prior cause is not reinvestigated: PR 2276's implementation prompt prohibited Compare, so the omission of the middle road was instructed, not a defect of that implementation.

## Recovered owner and Consumer-purpose

No existing Consumer Responsibility owns the attempt to relate new free-form material to Seed's available grammar. Two candidates were inspected and both fail:

- `seed_runtime/candidate_external_grammar.py` preserves **caller-supplied** candidate grammars. Its own boundary notes state *"Candidate grammars are caller-supplied structural hypotheses"* and *"Supporting and contradicting testimony relationships are preserved, not evaluated."* It produces no candidates and contains no reference to operator ingress.
- `run_operator_ingress_attempt(...)` owns the ingress road and stops at projection.

Two dispositions are defensible and the choice is not made here:

1. **Extension of an owned road.** The implementation already records `responsibility="operator-ingress"` in its event dimensions. An orientation-attempt occurrence recorded inside that same bounded attempt extends an already-owned road with one further act rather than creating a new owner.
2. **Unresolved.** No active clause assigns the attempt to relate ingress material to available grammar. Recording that as unresolved is honest and blocks nothing, because the observable-Evidence answer below does not depend on settling it.

Consumer-purpose is supplied by the active free-form interaction: the console owns *"process-local repetition around bounded operator interactions"*, holds an open output stream, and already responds on decoder failure. That establishes an available candidate Consumer boundary, not operator receipt.

## Exact materials

Available to the attempt from the successful projection:

```text
addressable material exact_text
provenance
scope (workspace;session;role)
known_loss
unknowns
attempt event_ids and dimensional_standing
authority_warrant ("occurrence-only; meaning Unknown")
```

Available across attempts in the same workspace and session:

```text
previously preserved operator-origin material
prior attempt occurrence identities and ordering
```

## Orientation-attempt occurrence

The attempt itself must be a recorded occurrence. It is the only thing that can carry the distinction the question asks for.

Following the existing naming and admission pattern, this is one new ledger event kind recorded through the existing `_record(...)`, carrying at minimum:

```text
identity and lineage to operator.ingress.ingress_occurred
exact materials considered
declared method or bounding applied
candidate set produced, explicitly including the empty case
result
authority: occurrence-only
```

## Candidate-production occurrence

Candidate production is separate from the candidate and from the attempt. `01.External.F` requires that a candidate preserve *"each applicable producer, source-role, formation-occurrence, scope, authority, and provenance dimension where known"* and that *"where a dimension is unresolved, its Unknown or unresolved standing must remain explicit."*

Where the attempt produces zero candidates, no candidate-production occurrence exists. The attempt occurrence still does.

## Empty-candidate disposition

At first contact the lawful candidate set is **empty**, and this is the correct answer rather than a gap.

`01.External.E` permits bounded findings of *"exact equality, count, recurrence, prefix occurrence, the result of a declared predicate, or adjacency within its measurement boundary."* Every one of those is relational: it requires material to measure against. At E1 there is one preserved material and no prior operator-origin material in the interaction, so no permitted finding is applicable.

Therefore:

```text
empty candidate set after a recorded orientation attempt
!= no orientation attempt occurred
```

The first is an occurrence with a bounded negative result. The second is the absence of any occurrence. Only the recorded event distinguishes them.

## Compare occurrence

Compare is not created here. Active law establishes responsible comparison acts in two places, both bounded to specific subjects:

- `03-goals-and-advancement/construction-and-establishment.md` — *"A responsible comparison act may compare that material with C's exact response coordinates and establish an exact coordinate match or nonmatch"*, with *"Comparison and identification are distinct acts."*
- `05.Testimony.E` — bounded comparison of *"multiple independently preserved testimonies or findings"*, producing bounded relation standing inside the comparison boundary.

Neither is a general act for comparing arbitrary material. Where candidates exist and are applicable, the exact Compare Act must be recovered for that instance; this report does not extend either clause.

Where the candidate set is empty, no Compare occurrence exists, and none should be recorded.

## PESC bounding

PESC is report-level shorthand, not active law. Used only as a bounding checklist, it constrains what a candidate-production or Compare occurrence may claim:

```text
Presentation      which exact material is present
Equivalence       which candidate relation is proposed
Scope             within which occurrence and boundaries
Consumer-purpose  for which exact Consumer use
```

Its function here is negative: a candidate that cannot state all four is not bounded, and an occurrence that omits them cannot show what it tested.

## Observable Evidence

This is the direct answer to the question.

The ledger is the only repository-visible Evidence surface for these acts. Without a recorded occurrence, "attempted and found nothing applicable" and "never attempted" produce byte-identical repository state, byte-identical projections, and byte-identical renderings. No amount of prose in the View can distinguish them, because prose in the View is not Evidence of anything having occurred.

The distinguishing Evidence is therefore:

```text
a recorded orientation-attempt occurrence, admitted into the
attempt projection, carrying:

  the occurrence identity and its lineage to the ingress occurrence
  the exact materials considered
  the declared method or bounding applied
  the candidate set produced, with the empty case explicit
  the bounded result
```

A useful test of any proposed implementation: **would the recorded ledger differ if Seed had not attempted?** If not, the attempt is not evidenced.

The current implementation fails that test. `"Communicative meaning: unresolved (Unknown)."` is an unconditional literal in `operator_ingress_view.py`, and `UNKNOWNS` is a module-level constant tuple in `operator_ingress_addressable_material.py`. Both render identically regardless of what occurred, so neither is Evidence of an attempt. They are honest declarations of the preservation boundary's limits and remain correct in that role.

## Bounded result and Standing

| Case | Result | Standing |
|---|---|---|
| empty candidate set | orientation attempted; no candidate produced; no relation applicable | occurrence-only; unresolved coordinates preserved unchanged |
| candidate produced, Compare inapplicable | candidate preserved with its `01.External.F` production dimensions; applicability negative | candidate standing only; no comparison result exists |
| Compare occurred, no relation matched | bounded comparison result: nonmatch | bounded relation standing inside the comparison boundary; not falsehood, not Unknown by identity |
| Compare occurred, bounded relation matched | bounded comparison result: match for the exact coordinate | bounded relation standing only; not truth, reliance, meaning, or Authority |

In no case does any result establish communicative meaning, operator intent, goal, Demand, or Authority carried by the material.

## Finding/response Consumer

No existing relation consumes these results today. The projection is consumed by `StateProjector`, and the View consumes the projection — so once an orientation occurrence is admitted into the attempt projection, the existing View is already positioned to render it.

Whether the result becomes a `finding` in the Book's sense is not settled here. `01.External.D` reserves *Fidelity finding* for a bounded comparison of constitutional grammar, a bounded expectation, and an implementation witness — a different subject. Naming these results `findings` would need its own recovery and is not required for the slice below.

## E1 / E2 / E3 trace

**E1 — `Hello`.** One preserved material, no prior operator-origin material in the interaction. No permitted measurement finding is applicable. Candidate set empty. Observable difference:

```text
today:      ingress preserved; three events; no orientation occurrence
after slice: ingress preserved; four events; orientation occurrence
             recording empty candidate set and no applicable relation
```

The ledger differs. That is the whole distinction.

**E2 — `Learn English`.** First point at which any candidate becomes possible, because it is the first time two operator-origin materials exist in one interaction. Permitted findings become applicable: exact equality (false), difference, recurrence of byte sequences across E1 and E2, ordering. Candidates may be produced. No English meaning, goal, or Demand may be inferred from the text — `01.External.E` states these findings *"do not establish structural, grammatical, or semantic meaning."*

**E3 — corpus.** Substantially more material, both across events and internally. More candidates become producible and Compare may become applicable for exact coordinates. Still no semantic establishment: a warranted meaning relation requires a separate responsible occurrence under `01.External.A`, which translation and recurrence explicitly do not supply.

## Earliest missing implementation boundary

Confirmed as proposed. In `seed_runtime/operator_ingress.py`, between:

```python
_record(ledger, "operator.ingress.ingress_occurred", ...)
```

and:

```python
state = StateProjector(ledger).project(workspace_id)
return state.operator_ingress_attempts[attempt]
```

Admission is governed by a closed whitelist in `project_operator_ingress_events(...)`:

```python
subject_by_kind = {
    "operator.ingress.raw_material_captured": "raw_initial_material",
    "operator.ingress.ingress_occurred":      "preserved_ingress",
    "operator.ingress.stopping_occurred":     "interaction_closure",
}
supported_kinds = {*subject_by_kind, "operator.ingress.representation_examined"}
if event.kind not in supported_kinds:
    raise ValueError(f"unsupported operator-ingress event: {event.kind}")
```

Any new kind must be admitted here or projection raises. `stopping_occurred → interaction_closure` is the existing pattern for a subject-bearing kind.

## Smallest implementation slice

```text
1. record one orientation-attempt occurrence after the ingress
   occurrence and before projection, carrying materials considered,
   declared bounding, candidate set (empty at E1), and result
2. admit that kind in project_operator_ingress_events
3. add one current_standing coordinate if the occurrence is
   subject-bearing, following the stopping_occurred pattern
4. render the occurrence in the existing View
5. focused tests proving the ledger differs between attempted and
   not-attempted, and that an empty candidate set is explicit
```

No Compare is implemented in this slice, because at E1 the candidate set is empty and no Compare occurrence exists to record. Compare enters at E2 at the earliest, and requires its own recovery of the exact comparison act.

## Files likely changed

```text
seed_runtime/operator_ingress.py
seed_runtime/operator_ingress_view.py
tests/test_operator_ingress.py
tests/test_operator_ingress_view.py
```

## Vocabulary or architecture explicitly rejected

```text
orientation Responsibility          not created; owner left as stated above
trigger / invocation                rejected; killed PRs 2176 and 2180 at this position
prerequisite-invocation             rejected
presentation-permission producer    rejected
diagnostic Consumer family          rejected
generic semantic interpreter        rejected
universal interaction pipeline      rejected
general compare-everything act      rejected; both active Compare clauses are subject-bounded
finding as a name for these results not adopted; would need separate recovery
```

`capture` and `examine` appear here only as quoted implementation identifiers.
