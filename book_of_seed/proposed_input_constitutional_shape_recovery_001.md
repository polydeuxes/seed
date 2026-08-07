# Proposed-input constitutional shape recovery 001

## Scope

This report recovers what, if anything, `proposed input` names in active
constitutional grammar, and what makes a preserved subject one.

It amends no active law, runtime, test, projection, or prior report, and
constructs nothing. The Applicability side settled by
`compare_proposed_input_boundary_recovery_001.md` is reopened only as far as
bounding Proposal requires. Verified at `67e5014`.

## 1. Executive answer

**`proposed input` is antecedent vocabulary used by the Applicability grammar.
What it names constitutionally is not recovered.** It appears in exactly one
clause, which introduced it in order to refer to the thing whose Applicability
that clause assigns.

Four readings remain open, and this report picks none:

```text
A  an independently established constitutional relation or role
B  a local role internal to an Act-owning Responsibility
C  the descriptive condition "an input this exact Act is considering
   for Applicability", with no independent thing at all
D  unresolved vocabulary compressing some missing Responsibility
```

**C would dissolve the missing edge entirely**, since nothing would need to
occur for a subject to be considered — the act owner's consideration would be
the whole content. **D would make the edge a compression to be decompressed.**
A and B would make it a thing with an origin to find. The clause does not
distinguish them.

What is recovered, stated in the form the corpus requires:

```text
no producing Act or occurrence is recovered
no owning Responsibility is recovered
no independent proposed-input result or Standing is recovered
no coordinates belonging to the term are recovered
```

Each of those is `not recovered`, not `absent`. `:49` itself lists *"a proposed
input"* among things conditional applicability does not establish, which treats
it as the sort of thing that could be established — so a categorical negative is
not available.

The governing question — *what makes a preserved subject a proposed input* —
has no recovered answer, and under reading C it may be a question with no
subject. The Book uses the term only where it needs to refer to an input an act
is considering, and says what does **not** confer that status without ever
saying what does.

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

**Not recovered as one.** Nothing located in active law produces it,
establishes it, or attributes standing to it. That is the absence of a
recovery, not a recovered absence: `:49`'s wording treats a proposed input as
something that could be established, so this report does not conclude that no
such result or Standing exists.

Contrast a term active law does treat as a kind. `01.External.F` says of
candidates:

> A candidate must preserve each applicable producer, source-role,
> formation-occurrence, scope, authority, and provenance dimension where known.

A candidate has a producer, a source-role, and a formation occurrence, and
where those are unresolved their Unknown standing must remain explicit. Nothing
comparable is said of a proposed input anywhere.

```text
Q1  no independent proposed-input result or Standing is recovered
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

**None is assigned in any clause located here.** `01.Standing.E.1` assigns the
*applicability* duty by name, in the same sentences, to the act-owning responsibility. It assigns
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

**None are recovered.** Every coordinate `01.Standing.E.1` names belongs to the
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

Reading the five occurrences together, `proposed input` is the phrase the clause
uses to refer to a subject an exact act is considering, in the course of stating
duties that attach to the act owner:

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

What that pattern shows is that the term is **used to refer** rather than
defined — every sentence needs a phrase for "the input this act is considering",
and supplies one. It does not show what the phrase names.

An earlier version of this report read the pattern as establishing a **role
assigned within an exact act**. That is withdrawn. Duties attaching to a phrase
does not establish that the phrase names a role: under reading C the duty
attaches to the act owner's consideration of a subject, with no role conferred
on the subject at all, and the clause reads identically either way.

**Where the reading stops, in both directions.** It does not follow that
proposal is merely descriptive — `:49` treats a proposed input as something that
could be established, and a real duty is conditioned on the phrase applying. Nor
does it follow that a role exists to be conferred. Both remain open, and this
report resolves neither. It neither claims the term dissolves nor preserves it
as a constitutional noun.

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
        │   what is "proposed" doing here at all?
        │
        ▼
   proposed input                    antecedent vocabulary;
        │                            what it names is not recovered
        ▼
Applicability determination          owner, form, and four results recovered
```

The smallest unresolved question is not *what confers the role*, because that
phrasing already answers one of the four readings. It is:

```text
does "proposed" name anything constitutional at all,
and if so which of A, B, C, or D?
```

The recovery narrows what would count as an answer. It is not a missing
*coordinate* of a known kind — none is recovered for the term. It is not a
missing *owner* of a named act — no proposal act is recovered. Under reading C
there is nothing missing at all, and the edge in the diagram above would not
exist. Active law distinguishes none of these, and this report does not.

No roadmap beyond that question is offered.

## 7. Correction record

Two claims in the previous version were corrected. The provenance finding, the
occurrence counts, the distinctness table, and the Q2/Q4/Q6 dispositions are
unchanged.

```text
1. it concluded that `proposed input` is "a local role term", and framed
   the closing question as what confers the role. That decides reading B
   over C and D without warrant. Duties attaching to a phrase does not
   establish that the phrase names a role -- under C the duty attaches to
   the act owner's consideration and the clause reads identically. The
   four readings are now recorded as open and the closing question is
   "what is proposed doing here at all".

2. its executive stated "it has no producing Act, no owning
   Responsibility, no Standing, and no coordinates of its own", while the
   detailed dispositions in the same report recorded those as Unknown.
   `not recovered` is not `absent`, and :49's own wording -- listing "a
   proposed input" among things conditional applicability does not
   establish -- treats it as something that could be established, which
   makes a categorical negative unavailable. All four are now stated as
   not recovered, and Q1's "recovered negative" is withdrawn.
```

The second defect is this author's most repeated one and its third
occurrence in a single session: the body recorded Unknown, the summary
recorded absence. It recurred here in a report whose subject is the
difference between what a clause says and what a reader supplies.

Report only. No active-law, runtime, test, projection, or prior-report
amendment.
