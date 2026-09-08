# Bounding material by common provenance: proposal review 002

Findings only. No runtime or Book amendment.

## The adjustment, and what it gets right

Curator replaced "source A" with "descended from event A", so that Seed holds
only `A != B` and the operator keeps `A ↔ Brown` as external provenance.

**That is the right axis to move on**, and it answers `#2410` §2 as stated: a
recorded event is not a developer-written label, and independence is a weaker
claim than identity. `#2408` gave good reason to keep a reader's names out.

**The code change is also genuinely small, and for a reason worth recording.**

**[measured]** The measurement forms never cross an occurrence boundary. Each
reads `_positions(event.payload["decoded_text"])` and steps within that one
occurrence. Two bodies of material pool only at the *selection* step, in
`preserved_ingress_occurrences`, which returns the whole session stream.

**[inference]** So bounding selection by an ancestor really would keep bodies
apart. Curator's "very small missing distinction" is small in the code.

**The difficulty is not the selection. It is that there is no ancestor.**

## 1. No such event exists today

**[measured]** There is no session-start, session-opened, or body-begun event
kind anywhere in `seed_runtime/` or `scripts/`.

**[measured]** The first occurrences a console session records are the C0
presentation's formation and emission (`scripts/seed_local.py:5696`). Every
ingress in that session follows them.

**[measured]** Each line's lineage points at its own capture and examination
events (`seed_runtime/operator_ingress.py:336`). Lines of the same body share
no ancestor with each other.

**[inference]** The only real occurrence that all of a body's ingress
descends from is C0 — and "descended from this session's C0" is coextensive
with "in this session". The reframing is more honest in expression and lands on
the same boundary `#2410` §2 objected to. It does not escape that objection; it
restates it in event terms.

That is not a reason to reject it. It is a reason not to count it as answered.

## 2. "One book as one material event" is worse, not better

Curator wrote that preserving an entire book as one material event would make
this basically done. **It would remove the one genuinely source-supplied
boundary Seed currently has.**

**[measured]** `capture_stdin_material`
(`seed_runtime/operator_ingress_representation.py:113`) is documented as "Read
one framed occurrence" and performs `readline()`. The line boundary is an
**observed transport framing**, not a developer's choice of segment.

**[measured]** `source_supplied_segmentation_experiment_001.md` established that
what makes a boundary trustworthy here is that the source supplies it and no
developer chose it. The line boundary meets that test as it stands.

**[inference]** Feeding a book as one material event means feeding it with its
newlines removed, which is a developer choosing to discard observed framing.
The resulting single occurrence would also let d1 measure across every sentence
and paragraph boundary in the book, which is a different measurement from every
result in `#2396`–`#2409`, not the same one at a larger scale.

## 3. Where a real ancestor would actually come from

An occurrence with a genuinely observable bounded extent, upstream of the
lines, is a **file or byte-stream read**: the boundary is the file, and Seed
would be observing it rather than asserting it.

**[measured]** That is the ingest path the operator deferred — *"we can build
the pipeline to ingest bytes"*, then *"i didn't mean build it now. too many
unknowns."*

**[inference]** So curator's E is not imaginary and not near. It is the
deferred ingest occurrence. Until that exists, E is either C0 — which is the
session — or authored.

**An authored E would be `05.Evidence:19` exactly.** Minting an event and
stamping every subsequent occurrence as its descendant makes the identifier
present in the payload without making the descent observed. A copied causation
identifier is not verified provenance, and stamped descent is the same defect
with an extra hop.

## 4. What this does not establish

**That the proposal should not proceed.** Sections 1 and 3 say what it would
cost and what it currently rests on. Selection by ancestor is sound machinery
whose ancestor is missing.

**That C0 is unsuitable.** It is a real recorded occurrence with a producing
act. The objection is only that descent from it carries exactly the session's
extent, so nothing is gained that `session_id` did not already give.

**That the deferred ingest path should now be built.** The operator's reason —
too many Unknowns — is not addressed here, and this adds a use for it rather
than an argument that its Unknowns are resolved.

**That bounded testimony comparison across bodies is blocked.** `#2410` §3
found it carried by `05.Testimony:27`. What is unresolved is the bounding of
the bodies, not the comparing of their findings.
