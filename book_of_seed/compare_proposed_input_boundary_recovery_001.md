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

Two of the three positions are recovered. The first is not.

```text
preserved subject  ──?──▶  proposed input  ──▶  Applicable input  ──▶  participation
                     ↑                     ↑                      ↑
                 UNRECOVERED           recovered              recovered
                                    (act-owning              (still requires
                                     responsibility)          the act to occur)
```

Active law establishes who determines Applicability, that the Compare
Responsibility may do so within its own occurrence, and that applicability is
not participation. It establishes **nothing** about how a preserved subject
becomes proposed, and it repeatedly denies the candidate mechanisms.

Per the request, the recovery stops there rather than jumping the gap.

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

**No.** It names a kind constraint on what may be consumed once consumption is
lawful, and a preservation obligation during consumption:

> A bounded comparison may consume multiple independently preserved testimonies
> or findings **only while preserving** each input's attribution, provenance,
> support basis, subject, scope, authority, confidence or uncertainty,
> Unknowns, standing, and forbidden inferences.

```text
supplies      the permitted input kinds                     warranted
supplies      a preservation obligation during consumption  warranted
does not supply   how a subject becomes proposed
does not supply   who proposes it
does not supply   applicability determination (that is 01.Standing.E.1's)
```

The two clauses are complementary and neither covers the gap: `05.Testimony.E`
says *what kind* may be consumed, `01.Standing.E.1` says *who determines
whether this one may be*, and nothing says *how this one came to be offered*.

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

Everything downstream of it is recovered. The act owner may determine
Applicability inside its own occurrence, needs no separate service, and must
not treat determination as occurrence. Nothing upstream is: active law
presupposes proposal in the same sentence that assigns the duty about it, and
denies every mechanism this thread has considered — availability, similarity,
equal content, exclusion, and conditional applicability.

Recorded without a proposed answer, per the request. The prior thread's
assumption that a C-to-E *relation subject* must precede Compare is neither
established nor excluded by this recovery: a relation is one thing that could
support a proposal, and active law does not say it is the only one, nor that
proposal requires one at all.

Report only. No active-law, runtime, test, or projection amendment.
