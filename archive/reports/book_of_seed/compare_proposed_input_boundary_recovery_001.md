# Compare proposed-input boundary recovery 001

## Scope

This report recovers the exact input boundary immediately upstream of a Compare
Act: what makes an independently preserved subject a *proposed input*, and what
Responsibility determines that proposed input's Applicability before it
participates.

It does not reopen #2331. It amends no active law, runtime, test, or
projection, constructs nothing, and proposes no machinery. Verified at
`ebe4ace`.

## 1. Executive answer

```text
preserved subject
        │
        ?                          UNRECOVERED
        ▼
  proposed input
        │
        ▼
Applicability determination        owner, form, and possible results recovered
        │
        ├── applicable
        ├── inapplicable
        ├── conflicting
        └── Unknown
        │
        ?                          separate claims, not established here
        ▼
   Act occurrence
   actual participation or reliance
```

What is recovered: **who** ordinarily determines Applicability, that the
Compare Responsibility may determine it within its own bounded occurrence, the
**form** that determination takes, and the four **results** it may reach.

What is not: how a preserved subject becomes proposed, and who owns that
proposal.

What is expressly not implied by an applicable result: that the Act occurs,
that the input is consumed, or that it is relied upon. Those are separate
claims that active law holds apart, and this report establishes none of them.

Per the request, the recovery stops at the proposal gap rather than jumping it.

## 2. Q1 — how a preserved subject becomes a proposed input

**Unrecovered.** Active law addresses proposal only negatively.

`01.Standing.E.1:45`:

> An alternative proposed input does not participate by virtue of
> availability, similarity, equal proposition text or content, or exclusion of
> another input.

`01.Standing.E.1:49`:

> Conditional input applicability does not by itself establish producer demand,
> candidate-formation demand, **a proposed input**, a producer, a responsible
> occurrence, Demand, translation, Question formation, production authority, or
> implementation authority.

So the following are explicitly denied as proposal mechanisms:

```text
availability                    denied  :45
similarity                      denied  :45
equal proposition text/content  denied  :45
exclusion of another input      denied  :45
conditional applicability       denied  :49
```

And the request's own exclusion list is confirmed rather than assumed:
recency, projection, caller choice, and presence in Standing are named nowhere
as proposal mechanisms, and `availability` — the closest of them to a general
term — is denied by name.

The clause presupposes proposal throughout (*"every proposed input"*, *"a
subject is proposed as an input"*) without defining it or assigning it. That
presupposition is the gap.

```text
Q1 disposition   Unknown
```

## 3. Q2 — who owns the proposal

**Unrecovered.** No clause located in this trace assigns proposal to any
Responsibility, Producer, or occurrence.

Note that `01.Standing.E.1` assigns the *applicability determination* to the
act owner explicitly and by name. Its silence on proposal is therefore not the
silence of a clause that never addresses ownership — it addresses ownership in
the adjacent sentence and does not extend it here.

```text
Q2 disposition   Unknown
```

## 4. Q3 — who determines Applicability to the exact Compare Act

**Recovered, warranted.** `01.Standing.E.1:37`:

> Unless the Book explicitly assigns otherwise, the responsibility assigned to
> perform an exact constitutional act is responsible for ensuring that
> applicability is determined for every proposed input before that input
> participates in, is consumed by, or is relied upon in the exact act.

And `:45`:

> Before the exact act relies upon a proposed input, the act-owning
> responsibility must determine or consume applicability standing for that
> exact input-to-act relation.

The determination's possible results are named at `:47` — the occurrence may
*"exclude **inapplicable**, **conflicting**, or **Unknown** inputs"* — so the
determination is four-valued, not a gate that either passes or is absent:

```text
applicable      the exact input may participate in this exact act under
                this bounded determination
inapplicable    excluded
conflicting     excluded
Unknown         excluded
```

An applicable result is a bounded determination about an input-to-act relation.
It is not the act, not consumption, and not reliance.

```text
default owner        the responsibility performing the exact act      warranted
override             an explicit Book assignment displaces it         warranted
delegation           to an explicitly assigned responsible occurrence
                     for that exact downstream act                    warranted
not permitted        a universal applicability service                warranted
non-transferable     applicability for one act is not applicability
                     for another; upstream applicability is not
                     downstream admission                             warranted
```

## 5. Q4 — what that determination requires

**Recovered as a form, deliberately not as a list.** `:37` names the coordinates
Applicability is determined *for*:

> that act's exact subject and content, purpose, scope and locality, authority,
> participants and roles, consumer context, and preserved limits

and what the determination preserves:

> consumer identity, source and provenance, standing and warrant, currentness
> and occurrence identity, known loss, conflicts, **Unknowns**, and negative
> authority. Purpose is a required local coordinate, not an additional
> universal dimension.

`:45` then bounds the requirement itself:

> validate or consume whatever standing, warrant, admission, authority, scope,
> provenance, or other relation that exact proposed use requires. Required
> coordinates are local to the exact act and proposed use; **no coordinate is
> universally required merely because a subject is proposed as an input.**

That last sentence is load-bearing and cuts against a natural implementation
instinct: there is no enumerable precondition set that a Compare could check
once and for all. The requirement is local to the exact act and the exact
proposed use.

`:45` also records what stays Unknown:

> whether one input may occupy another's exact role remains **Unknown** unless
> a responsible occurrence separately establishes that relation for the exact
> act, purpose, and scope.

```text
Q4 disposition   warranted as a form; the coordinate set is local by
                 construction and not universally enumerable
```

## 6. Q5 — may the Compare Responsibility determine Applicability itself?

**Recovered, and this is the clearest answer in the trace: yes.**

`01.Standing.E.1:38`:

> The owner may determine applicability within the same bounded occurrence, or
> may validate and consume applicability standing established by an explicitly
> assigned responsible occurrence for that exact downstream act.

`01.Standing.E.1:47`:

> One bounded responsible occurrence may determine applicability for proposed
> inputs, exclude **inapplicable**, **conflicting**, or **Unknown** inputs,
> perform the exact act or establish no act occurrence within the act-owning
> responsibility's assigned boundaries, and, where independently warranted,
> establish the bounded standing of its output.

**No separate universal Applicability owner is required and none should be
constructed.** The same bounded occurrence may determine, exclude, and act.

`:47` then holds those apart as claims even when one occurrence performs them:

> These remain independently recoverable claims, each retaining its own
> subject, responsible act, purpose, evidence basis, result, consumer, scope,
> authority, provenance, **Unknowns**, conflicts, negative authority, and
> failure or absence-of-occurrence reason. Same occurrence is not same claim,
> same function is not same responsibility, **applicability success is not act
> occurrence, one input applicable is not act occurrence** [...] The occurrence
> must not fabricate participation, reliance, act-occurrence, or output-standing
> claims.

So the request's distinction `Applicable input != participation in Compare` is
active law, stated twice.

```text
Q5 disposition   warranted — same-occurrence determination is permitted
                 explicitly; the claims stay distinct regardless
```

## 7. Q6 — does `05.Testimony.E` supply input-formation grammar?

**No.** It positively names Compare input kinds and imposes a preservation
condition on their consumption:

> A bounded comparison may consume multiple independently preserved testimonies
> or findings **only while preserving** each input's attribution, provenance,
> support basis, subject, scope, authority, confidence or uncertainty,
> Unknowns, standing, and forbidden inferences.

```text
supplies      testimony and finding as positively named Compare
              input kinds                                   warranted
supplies      a preservation obligation during consumption  warranted

does not supply   that only testimony or finding may ever be a Compare
                  input — the wording names kinds positively and states
                  no closure                                Unknown
does not supply   how a subject becomes proposed
does not supply   who proposes it
does not supply   applicability determination (that is 01.Standing.E.1's)
```

Exhaustiveness is left **Unknown**. `only while preserving` in that sentence
conditions the manner of consumption, not the membership of the input kinds,
and no other clause located here establishes closure.

The two clauses are complementary and neither covers the gap:
`05.Testimony.E` names kinds that may be consumed, `01.Standing.E.1` says who
determines whether an exact proposed input may be, and nothing says how this
one came to be offered.

## 8. Q7 — does the answer differ for testimony versus finding inputs?

**Not established.** `05.Testimony.E` names *"testimonies or findings"* as one
permitted-input phrase and distinguishes them nowhere. Active law contains no
definition of `finding` as a constitutional kind; the only occurrences located
are two non-equivalences about *diagnostic* findings (`06.Projection:35`,
`05.Testimony:77`), neither of which concerns comparison inputs.

`01.Standing.E.1` is kind-agnostic throughout: it speaks of *proposed inputs*
without distinguishing what kind of subject is proposed.

```text
Q7 disposition   Unknown — no differentiating grammar located; the absence
                 of a `finding` definition is itself unresolved and is not
                 asserted here to mean the kinds are equivalent
```

## 9. Edge classification

| Edge | Class |
| --- | --- |
| preserved subject → proposed input | **Unknown** — presupposed, undefined, unassigned |
| availability / similarity / equal content / exclusion of another → proposed input | **denied by active law** (`:45`) |
| conditional applicability → proposed input | **denied by active law** (`:49`) |
| recency / projection / caller choice / presence in Standing → proposed input | **Unknown** — named nowhere; `availability` is the nearest denied term |
| proposed input → Applicability determination | **warranted** — owned by the act-owning responsibility (`:37`, `:45`) |
| that ownership displaced by explicit Book assignment | **warranted** (`:37`) |
| delegation to an explicitly assigned responsible occurrence | **warranted, local-only** — for that exact downstream act (`:38`) |
| a universal applicability service | **denied by active law** (`:38`) |
| Compare Responsibility determining Applicability in its own occurrence | **warranted** (`:38`, `:47`) |
| applicability determination → act occurrence | **denied** — "applicability success is not act occurrence" (`:47`) |
| exclusion of an input → act does not occur | **denied** (`:43`) |
| act occurrence without an excluded input → that input was applicable | **denied** (`:43`) |
| `05.Testimony.E` as input-formation grammar | **implementation assumption if relied upon** — it constrains kind, not formation |
| testimony and finding treated alike for Applicability | **Unknown** |

## 10. Smallest unresolved coordinate

```text
what makes an independently preserved subject a proposed input
to an exact Compare Act — and what Responsibility, if any, owns
that proposal
```

What is recovered downstream of it is narrower than *everything*: the
ownership, form, and possible results of the Applicability determination. The
act owner may determine Applicability inside its own occurrence, needs no
separate service, and must not treat determination as occurrence. **Act
occurrence and actual participation remain separate claims**, established by
neither the determination nor this report.

Nothing upstream is recovered: active law presupposes proposal in the same
sentence that assigns the duty about it, and denies every mechanism this thread
has considered — availability, similarity, equal content, exclusion, and
conditional applicability.

Recorded without a proposed answer, per the request. The prior thread's
assumption that a C-to-E *relation subject* must precede Compare is neither
established nor excluded by this recovery: a relation is one thing that could
support a proposal, and active law does not say it is the only one, nor that
proposal requires one at all.

## 11. Correction record

Four claims in the first version were corrected. The main finding — that the
proposal boundary is unrecovered — is unchanged, as are the Q1, Q2, Q3, Q4,
Q5, and Q7 recoveries.

```text
1. the executive topology drew

     proposed input -> Applicable input

   which collapses a four-valued determination into its success case.
   01.Standing.E.1:47 names inapplicable, conflicting, and Unknown
   alongside applicable. Replaced with proposed input -> Applicability
   determination -> bounded result.

2. it drew

     Applicable input -> participation

   and labelled participation recovered, while section 9's own table
   listed that arrow as denied and section 6 quoted the clause denying
   it. Active law holds that applicability success is not act occurrence
   and that one input applicable is not act occurrence. Withdrawn: an
   applicable result means the exact input may participate under that
   bounded determination, nothing more.

3. it called testimony and finding "the permitted input kinds", which
   implies closure. 05.Testimony.E names them positively and states no
   exhaustiveness; `only while preserving` conditions the manner of
   consumption, not the membership of the kinds. Exhaustiveness is now
   Unknown.

4. section 10 said "everything downstream of it is recovered". Narrowed
   to the ownership, form, and possible results of the Applicability
   determination, with Act occurrence and actual participation recorded
   as separate claims.
```

The second is the one worth naming: the report established
`Applicability success != Act occurrence` in its body and then drew the
arrow that denial forbids, in its own summary diagram. Frames outrunning
the findings they summarise is this author's most repeated defect, and it
recurred here inside a report about not overclaiming.

Report only. No active-law, runtime, test, or projection amendment.
