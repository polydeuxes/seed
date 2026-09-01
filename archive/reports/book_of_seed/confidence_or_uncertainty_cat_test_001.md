# `confidence or uncertainty` in 05.Testimony.E: cat test 001

Findings only. No Book or runtime amendment. Nothing was added to any finding.

## Disposition

**The universal requirement is unsupported.** `confidence` and `uncertainty`
are not one coordinate and do not fail the same way.

```text
  confidence    names something real and provider-side.
                No Seed act produces it. No owner in Seed. It is
                attributed external grammar, and active law says so twice.

  uncertainty   names something real and inquiry-local.
                Chapter 04 is where it lives. Every other clause that
                mentions it does so permissively or about an inquiry,
                never as a coordinate every finding must carry.
```

The pairing `confidence or uncertainty` appears in active law **only** inside
coordinate lists. It was authored for cross-examination of witness testimony and
relocated verbatim.

## 1. Cat test — `confidence`

**Does it name something?** Yes.

```text
  01.External:15   "Provider vocabulary, external representations, and source
                    confidence labels enter Seed reasoning only as attributed
                    source grammar."
  01.External:44   "provider confidence != repository authority"
```

**What kind?** A label an external source attaches to its own material. Active
law admits it as attributed external grammar and separates it from repository
authority by explicit non-equivalence.

**Does it own a Responsibility, or is it carried?** Carried. Its owner is the
**provider**, and the provider is outside Seed.

**What Act produces confidence-as-confidence, and what Standing does that
establish?** **Nothing in active law.**

```text
  clauses establishing, producing, assigning, determining, forming or
  setting a confidence                                          0
```

`08.Authority:25` permits Seed to *analyze* "confidence limits". Analyzing a
source's confidence is not producing one, and that clause's own next sentence
refuses to let the competence become jurisdiction.

`01.Uptake:17` mentions confidence only to deny movement: evidence becoming
available "does not by itself change any consumer assertion, standing,
confidence, reliance, or current result."

**[inference]** Confidence is a coordinate of *someone else's* testimony.
Requiring Seed's own exact count to carry one requires Seed to hold a coordinate
active law locates in external sources. This is the `learning` shape: real word,
real occurrences, no owner, no producing act, no established standing.

## 2. Cat test — `uncertainty`, which passes differently

**Does it name something?** Yes, and it has a home.

```text
  04.README:3            the Book "concerns bounded questions, inquiry
                         frontiers, uncertainty, and findings"
  04.Question:7          a question is "connected to an established goal or
                         uncertainty"
  04.Question:10         Seed may consume "repository uncertainty"
  04.Frontiers:15        a frontier preserves "the exact inquiry demand or
                         uncertainty it concerns"
```

**What kind?** An inquiry-local subject — what an inquiry is *about*.

**Owner?** The bounded question or inquiry frontier that concerns it.

**Producing act and standing?** `04.Question:18` and `:56` are explicit that an
uncertainty statement creates attributed testimony or inquiry pressure only, and
**"uncertainty statement != inquiry origination"**.

**[measured]** Where an artifact may carry uncertainty, active law is
permissive, not mandatory. `01.Kinds:10`: an artifact's "shape **can** preserve
identity, provenance, result, uncertainty, and boundaries".

**[inference]** Uncertainty is real and belongs to inquiry. It is not
established as a coordinate every preserved finding must possess.

## 3. The clause that governs declared measurement asks for three things

`01.External:28` is where a declared measurement's obligations live:

> A recurrence assertion must disclose the representation or projection
> measured, the rule by which equivalence or sameness was determined, and the
> bounded scope within which occurrences were counted.

**Three disclosures. Neither confidence nor uncertainty is among them**, and the
measurement findings carry all three as required fields.

**The same clause then refuses this exact move:**

> A consumer's purpose separately governs lawful reliance, acceptable
> aggregation, and acceptable representational loss; **purpose is not therefore
> a required coordinate of every exact count.**

**[inference]** That is the present question already answered in the general
case. A downstream consumer governing something does not make its coordinate
required of every exact count. `05.Testimony.E` is a consumer of findings
demanding a coordinate of every input, which is the structure `01.External:28`
declines for purpose.

## 4. Its own chapter does not agree with it

```text
  05.Testimony:24   consumption preserves   attribution, source-relative
                    limits, conflicts, uncertainty                    4 items
  05.Testimony:27   consumption preserves   attribution, provenance, support
                    basis, subject, scope, authority, confidence or
                    uncertainty, Unknowns, standing, forbidden
                    inferences                                       10 items
```

**[measured]** `:24` governs consuming "a recorded claim, diagnostic finding, or
evidence record ... as attributed testimony or premise-relative input for an
exact declared act" — which is nearer to what the measurement findings do than
`:27` is. It requires no confidence, and says `uncertainty` alone.

**[inference]** The ten-item list is an outlier inside its own chapter, and the
outlier is the one that arrived from elsewhere.

## 5. Where the list came from

**[measured]** One commit ever wrote `confidence or uncertainty` into
`testimony-and-established-fact.md`: `6135f18`, **"Relocate examination clauses
and excise contaminated chapter (#2146)"**.

**[measured]** Its source was `04.Examination.C — Cross-examination without
source-local erasure`, in the chapter that commit excised as contaminated:

> **Cross-examination** may compare independently preserved testimony or
> findings only while preserving each input's attribution, provenance, support
> basis, subject, scope, authority, confidence or uncertainty, Unknowns,
> standing, and forbidden inferences.

**[measured]** The relocation report's stated reason for this coordinate, in
full:

> | confidence or uncertainty | "confidence or uncertainty" | Preserved | **Both
> poles retain the source wording.** |

**[inference]** The relocation is not at fault. It declared semantic
preservation and performed it exactly. But that reason is the only justification
the coordinate has ever received in this position: it was carried, never
warranted.

**[inference]** The frame explains the coordinate. Cross-examination compares
**witnesses**, and a witness's statement has a confidence its source asserts.
`01.External:15` already says where such a label goes — attributed external
grammar. A measurement Seed performed on material Seed preserved is not a
witness statement, and the coordinate does not transfer with the verb.

## 6. The hard case, as asked

```text
  finding    pair ('because', 'therefore') measured at displacement 4
  rule       byte-for-byte equality; no normalization
  scope      one bounded exchange
```

**[inference]** There is no probability here to record. The pair either occupied
that position in preserved material or did not, under a disclosed rule, inside a
disclosed scope. `confidence = 1.0` would be manufactured; `uncertainty = none`
would be manufactured more quietly.

**[measured]** The limits that are real are already carried, and none of them is
confidence:

```text
  which material           dimensions.identity, representation_measured
  under what rule          equivalence_rule
  within what bound        counting_scope, scope_locality
  standing on what         premise_event_id, premise_chain()
  what is not known        payload.unknowns
  what may not be inferred payload.boundary_notes
  what standing it has     dimensions.standing = "measured"
```

## 7. The narrow correction, identified and not written

**[inference]** `05.Testimony.E` should require preservation of the coordinates
an input **carries**, rather than asserting that every preserved testimony or
finding possesses all ten. The clause's protective purpose — that comparison
must not erase what an input holds — survives that reading intact, and `:29`
already carries the rest of its force.

The wording is not proposed here. `#2408`'s lesson applies to Book text as much
as to sources: the correction should be made by whoever owns the clause, and
this report's job was to establish that the requirement is unwarranted, not to
draft its replacement.

## 8. What this does not establish

**That confidence has no place in Seed.** It has one: attributed external
grammar, provider-owned. Nothing here removes it from `01.External`.

**That the measurement finding is complete.** It carries the three disclosures
`01.External:28` requires. Whether other coordinates are missing was not asked.

**That `05.Testimony.E` is otherwise defective.** Nine of ten coordinates are
carried by the findings without difficulty, and the clause's permission to
produce bounded relation standing inside the comparison boundary is untouched.

**That layer C is now unblocked.** This establishes that one blocker is
unwarranted. Whether the clause is corrected, and by whom, is not this report's
to decide, and no comparison was built.
