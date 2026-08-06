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

The evidentiary core survives. The materials, the E1 claim, the proposed event, and the implementation slice do not.

## Recovered owner and Consumer-purpose

**Unresolved, and this is the blocking finding.**

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

## The established acts

There is no established act named orientation. The acts the road requires are:

```text
candidate production      01.External.F — a candidate must preserve each
                          applicable producer, source-role, formation-
                          occurrence, scope, authority, and provenance
                          dimension where known

Compare                   "Compare the candidate equivalence with the
                          applicable relation grammar", recovered as
                          Shape B and explicitly non-identical to
                          testimony-versus-testimony comparison
```

Any ledger occurrence must testify to one of these under an exact Responsibility. An event named after report-level shorthand testifies to nothing.

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

The corrected reading, replacing the collapse in the first version:

```text
candidate-production Act occurred
→ bounded result: empty candidate set
```

is distinct from:

```text
no candidate-production Act occurred
```

This matters because it removes the reason the first version invented a separate event. If a candidate-production occurrence can carry an empty result, the tried-versus-not-tried distinction is evidenced by an act that already has Book grammar, with no new act invented.

What remains unresolved is who performs it.

## Observable Evidence

This part of the first version survives.

The ledger is the only repository-visible Evidence surface for these acts. Without a recorded occurrence, "attempted and established nothing stronger" and "never attempted" produce byte-identical repository state, projections, and renderings.

The test for any proposed implementation:

```text
would the recorded ledger differ if Seed had not attempted?
```

The current implementation fails it. `"Communicative meaning: unresolved (Unknown)."` is an unconditional literal in `operator_ingress_view.py`, and `UNKNOWNS` is a module-level constant tuple in `operator_ingress_addressable_material.py`. Both render identically regardless of what occurred, so neither evidences an attempt. Both remain correct as honest declarations of the preservation boundary's own limits.

The distinguishing Evidence would be a recorded occurrence of an established act carrying its exact materials, declared bounding, produced result including the empty case, and lineage. What blocks recording it is not the event schema. It is that no Responsibility owns the act.

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

**None is warranted yet.**

The blocker is not schema, naming, or projection. It is that no Responsibility owns candidate production for operator-ingress material, and none owns the candidate-versus-grammar Compare. Both are recorded as unresolved in the active recovery. An occurrence must evidence an exact Act under an exact Responsibility; recording one before the owner exists produces an ownerless event, which is what the first version of this report proposed and what this correction withdraws.

The prerequisite is a recovery answering:

```text
which Responsibility, if any, produces a candidate equivalence for
operator-ingress material, under what Authority and purpose

whether that Responsibility already exists compressed inside an
owned road, or is genuinely absent
```

Until then the correct state is the current one: material preserved, Standing projected, no claim that an attempt occurred.

## Files likely changed

None. No implementation slice is warranted at this disposition.

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
