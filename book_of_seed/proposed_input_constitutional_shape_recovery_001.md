# Proposed-input constitutional shape recovery 001

## Scope

This report recovers what, if anything, `proposed input` names in active
constitutional grammar, and what makes a preserved subject one.

It amends no active law, runtime, test, projection, or prior report, and
constructs nothing. The Applicability side settled by
`compare_proposed_input_boundary_recovery_001.md` is reopened only as far as
bounding Proposal requires. Verified at `67e5014`.

## 1. Executive answer

**`proposed input` is a local role term, not a recovered constitutional
coordinate.** It has no producing Act, no owning Responsibility, no Standing,
and no coordinates of its own anywhere in active law. It appears in exactly one
clause, which introduced it in order to name the thing whose Applicability that
clause assigns.

```text
Test                                          Result
a distinct constitutional coordinate          no
a result produced by another Responsibility   no — none is named
a local role assigned within an exact Act     closest supported reading
a descriptive word for an existing shape      partly — see §4
an unresolved compression                     not established either way
```

The governing question — *what makes a preserved subject a proposed input* —
therefore has no recovered answer, and the reason is sharper than "the Book is
silent." The Book uses the term only where it needs a name for an input under
consideration by an act, and says what does **not** produce that status without
ever saying what does.

## 2. Where the term lives

```text
"proposed input"      5 occurrences, all in 01.Standing.E.1
                      (constitutional-kinds-and-artifact-standing.md:37,43,45,47,49)
                      0 occurrences in any other chapter

"proposal"            2 occurrences
                      02.Acts:18   proposal != occurrence
                      01.External:15  provider vocabulary context

"candidate formation" 1 occurrence
                      03.Demands:33
```

No chapter other than `01.Standing.E.1` uses `proposed input`. No clause
anywhere defines proposal, assigns it, or names a proposal act, occurrence,
producer, or result.

### 2.1 How it entered

```text
#2171  015b584  Assign default ownership of input applicability
                introduced 01.Standing.E.1
#2172  e9430cc  Distinguish input exclusion from act nonperformance
#2178  2988ed2  Tie applicability and act performance to responsible occurrences
#2179  6864f4d  Make input requirements act-local
```

Four PRs, all amending the same clause, all titled for **applicability** or
**inputs to acts**, none carrying a recovery report. The term arrived as
vocabulary the applicability clause required, and every subsequent PR sharpened
the applicability side without ever addressing proposal.

This is provenance, not disqualification. It does establish that no separate
recovery of proposal underlies the term.

## 3. Question by question

### Q1 — is `proposed input` a constitutional result or Standing?

**No.** Nothing in active law produces it, establishes it, or attributes
standing to it.

Contrast a term active law does treat as a kind. `01.External.F` says of
candidates:

> A candidate must preserve each applicable producer, source-role,
> formation-occurrence, scope, authority, and provenance dimension where known.

A candidate has a producer, a source-role, and a formation occurrence, and
where those are unresolved their Unknown standing must remain explicit. Nothing
comparable is said of a proposed input anywhere.

```text
Q1  not a constitutional result or Standing        recovered negative
```

### Q2 — what Act or occurrence produces the proposal?

**None is named.** `01.Standing.E.1` presupposes proposal in every sentence
that uses the term and defines it in none.

What it does say is what proposal is *not* produced by:

```text
:45   availability
:45   similarity
:45   equal proposition text or content
:45   exclusion of another input
:49   conditional input applicability
```

`:49` is the most direct: conditional input applicability *"does not by itself
establish producer demand, candidate-formation demand, **a proposed input**, a
producer, a responsible occurrence, Demand, translation, Question formation,
production authority, or implementation authority."*

That sentence places `a proposed input` in a list of things that are not
established by something else — which presupposes that a proposed input is the
sort of thing that could be established, while naming nothing that establishes
it.

```text
Q2  producing Act or occurrence                    Unknown
```

### Q3 — what Responsibility owns proposal?

**None is assigned.** `01.Standing.E.1` assigns the *applicability* duty by
name, in the same sentences, to the act-owning responsibility. It assigns
proposal to nobody.

As recorded in the prior report, that silence is not the silence of a clause
which never discusses ownership; it discusses ownership immediately adjacent
and does not extend it.

```text
Q3  owning Responsibility                          Unknown
```

### Q4 — generic across Acts, or local to the exact Act?

**Local, on the only evidence available.** Every use of the term is bound to an
exact act:

```text
:37  "applicability is determined for every proposed input before that input
      participates in ... the exact act"
:45  "the act-owning responsibility must determine or consume applicability
      standing for that exact input-to-act relation"
:45  "Required coordinates are local to the exact act and proposed use; no
      coordinate is universally required merely because a subject is proposed
      as an input."
```

The last sentence is decisive against a generic proposal relation carrying
universal coordinates. Whether a generic *proposal act* could exist is not
addressed; what is established is that being proposed carries no universal
requirements.

```text
Q4  local to the exact act and proposed use        warranted
    a generic proposal relation                    not established
```

### Q5 — what coordinates does proposal carry?

**None of its own.** Every coordinate `01.Standing.E.1` names belongs to the
*applicability determination*, not to the proposal:

```text
determined for      the act's exact subject and content, purpose, scope and
                    locality, authority, participants and roles, consumer
                    context, preserved limits

preserving          consumer identity, source and provenance, standing and
                    warrant, currentness and occurrence identity, known loss,
                    conflicts, Unknowns, negative authority
```

And `:45` states positively that no coordinate attaches by virtue of being
proposed.

```text
Q5  proposal's own coordinates                     none recovered
```

### Q6 — can proposal occur within the same occurrence that determines Applicability?

**Not established, and the clause's grant does not reach it.** `:38` and `:47`
permit one bounded occurrence to *determine applicability*, *exclude*
inapplicable, conflicting, or Unknown inputs, and *perform the act*. Proposal is
not among the permitted acts of that occurrence — it is presupposed as already
having happened to the inputs it receives.

Reading the grant as covering proposal would extend an enumerated permission by
analogy, which `:47`'s own *"same occurrence is not same claim"* discourages.

```text
Q6  same-occurrence proposal                       Unknown, not granted
```

### Q7 — is proposal distinct from the neighbouring terms?

| Against | Distinct? | Basis |
| --- | --- | --- |
| candidate formation | **yes** — a candidate has a producer, source-role, and formation occurrence (`01.External.F`); a proposed input has none named. `03.Demands:33` also treats candidate formation as a thing Demand content may constrain without producing | recovered |
| Demand | **yes** — `:49` lists Demand and a proposed input as separate things not established by conditional applicability | recovered |
| selection | **not established** — active law nowhere relates proposal to selection; neither identity nor distinction is stated | Unknown |
| Admission | **yes** — `:38` "upstream applicability is not downstream admission"; Admission is downstream of applicability, which is downstream of proposal | recovered |
| Applicability | **yes** — proposal precedes the determination in every sentence; a determination is *about* a proposed input | recovered |
| participation | **yes** — `:47` "applicability success is not act occurrence, one input applicable is not act occurrence" | recovered |

## 4. What the term actually does in the clause

Reading the five occurrences together, `proposed input` functions as a **role
name for a subject under consideration by an exact act**, used to state duties
that attach to the act owner:

```text
:37  every proposed input must have applicability determined before it
     participates                             → duty on the act owner
:43  exclusion of one proposed input does not establish whether the act
     occurs                                   → limit on inference
:45  an alternative proposed input does not participate by virtue of
     availability, similarity, equal content, or exclusion of another
                                              → limits on participation
:47  an occurrence may exclude inapplicable, conflicting, or Unknown inputs
                                              → permission for the occurrence
:49  conditional applicability does not establish a proposed input
                                              → limit on what creates the role
```

Every sentence uses the term to bound something *else* — the act owner's duty,
an inference, a participation claim, an occurrence's permissions. None gives the
role a producer, an occurrence, a result, or a standing.

That is the shape of a **role assigned within an exact act**, not of an
independent constitutional kind. The role is real in the sense that duties
attach to it; it is not recovered as a thing that is produced.

**Where the reading stops.** It does not follow that proposal is *merely*
descriptive. `:49` treats a proposed input as something that could be
established, and `01.Standing.E.1` conditions a real duty on the role obtaining.
Whether something must occur for a subject to hold the role — and if so what —
is exactly what is unrecovered. This report does not resolve it, and does not
claim the term dissolves.

## 5. Arrows, independently classified

| Arrow | Class |
| --- | --- |
| preserved subject → proposed input | **Unknown** — no clause supplies it |
| candidate → proposed input | **Unknown** — candidate has its own recovered kind grammar; no clause relates the two |
| Demand → proposed input | **denied in one direction** — `:49` says conditional applicability establishes neither Demand nor a proposed input; no clause relates them positively |
| available Standing → proposed input | **denied** — availability at `:45` |
| relation Standing → proposed input | **Unknown** — never addressed |
| projection → proposed input | **Unknown** — never addressed |
| caller reference → proposed input | **Unknown** — active law does not discuss callers; a caller reference is an implementation notion with no constitutional standing |
| proposed input → Applicability determination | **warranted** — owned by the exact act's responsibility |

## 6. Smallest edge between preserved subject and Applicability determination

```text
preserved subject
        │
        │   whether anything must occur for this subject to hold the
        │   role of proposed input to an exact Act — and if so, what
        │   Act, occurrence, or Responsibility does it
        ▼
   proposed input                    role recovered; production Unknown
        │
        ▼
Applicability determination          owner, form, and four results recovered
```

The edge is unrecovered, and the recovery narrows what kind of thing is
missing. It is not a missing *coordinate* of a known kind: `proposed input` has
no coordinates. It is not a missing *owner* of a known act: no proposal act is
named. What is missing is whether the role is conferred by an occurrence at all,
or obtains from the act owner's own consideration of a subject — and active law
supports neither reading.

No roadmap beyond that edge is offered.

Report only. No active-law, runtime, test, projection, or prior-report
amendment.
