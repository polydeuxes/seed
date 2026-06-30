# Null to Repository Orientation Experiment

## Initial null state

The experiment began with an empty local Seed database at `/tmp/seed-null-orientation.sqlite` and no projected observations or facts. The only experimental observation recorded into Seed was the literal text:

```text
.
```

The note was recorded with:

```bash
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --record-inquiry-note '.'
```

Seed returned:

```text
recorded inquiry note: inq_000001
```

Implementation boundary: this uses the inquiry-note probe, which stores operator prose outside the event ledger and treats it as preserved evidence for the probe only, not as a fact, requirement, plan, or command.

## Complete observation and inquiry sequence

### Step 0 — Null

- **Observed:** no observations and no facts existed in the fresh database.
- **Question created:** can an otherwise empty projected state orient around the unknown note `.`?
- **Evidence gathered:** `--current-observations` returned `(none)` and `--current-facts` returned `(none)` after the note was recorded.
- **Conclusion justified:** the inquiry note did not silently become projected cluster or repository knowledge.
- **Next inquiry enabled:** render the bounded orientation view for the preserved note.

### Step 1 — First observation from `.`

Command:

```bash
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --inquiry-orientation
```

- **Observed:** Seed rendered the inquiry note exactly as `.`.
- **Question created:** does `.` deterministically overlap with any already projected read-model material?
- **Evidence gathered:** Seed reported no deterministic related material in projected read models and no supportable lexical overlap.
- **Conclusion justified:** the first observation is not a repository structure fact. It is only the preserved unknown note `.` plus the absence of deterministic matches in the currently projected read models.
- **Next inquiry enabled:** inspect whether the implementation has a repository-visible concept of inquiry artifacts or unknowns before selecting any richer observer.

Rendered evidence:

```text
Inquiry note:
  .

Potentially related material:
  No deterministic related material found in projected read models.

Support / why related:
  No supportable lexical overlap was found.

Uncertainty:
  No deterministic related material was found in already projected read models; this absence does not prove the note is unrelated to existing work.

Authority boundary:
  This orientation is read-only. The inquiry note is preserved operator prose, not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction. Matches are deterministic lexical overlaps only and do not assert importance, do not assert ownership, intent, concern, recommended action, or next safe move.
```

### Step 2 — Validate that the note did not mutate projected knowledge

Commands:

```bash
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --current-observations
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --current-facts
```

- **Observed:** Seed reported no current observations and no current facts.
- **Question created:** if the note creates no projected facts, what kind of supported movement is still possible?
- **Evidence gathered:** the read models remained empty.
- **Conclusion justified:** the transition from `.` to orientation did not create repository claims, topology, ontology, plans, or commands.
- **Next inquiry enabled:** ask a read-only implementation surface what inquiry artifacts are actually repository-visible.

### Step 3 — First richer observation need

Command:

```bash
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --inquiry-artifacts
```

- **Observed:** Seed exposed inquiry-artifact visibility as read-only, with explicit boundaries: no recording, no event-ledger writes, no cluster mutation, no inquiry graph creation, no pressure transformation inference, and no workflow or planning behavior.
- **Question created:** which inquiry artifacts are implementation-visible, and which are only document-visible or partial?
- **Evidence gathered:** `unknown` and `boundary` were `repository_visible`; `gap`, `pressure`, and `finding` were only `partially_visible`; supported and unsupported conclusions and open questions were `document_visible`.
- **Conclusion justified:** Seed independently reaches a need for richer observation at the point where the orientation output has no deterministic match and the implementation must distinguish unknowns and boundaries before making any next claim.
- **Next inquiry enabled:** determine whether a structure observer is justified by implementation evidence or merely by the operator's experimental expectation.

### Step 4 — Structure observer selection check

- **Observed:** no command in the experiment selected `--observe-repository-source` or any other repository/source/documentation observer.
- **Question created:** did Seed naturally invent or select a structure observer from `.`?
- **Evidence gathered:** the implemented orientation surface only performs deterministic lexical overlap against already projected fact supports and source-navigation matches. With no projected state and a one-character note that yields no token of the minimum supported length, it produced no related material and no recommendation for a next observer.
- **Conclusion justified:** Seed did **not** naturally invent or select a structure observer in this bounded run. Selecting one would have injected an implementation family not justified by the observed sequence.
- **Next inquiry enabled:** preserve unsupported transitions explicitly rather than continuing into repository traversal.

## Direct answers

1. **What is the first observation made from `.`?**

   The first observation is the preserved inquiry note whose raw text is exactly `.`. The first rendered orientation output repeats that note and reports no deterministic related material.

2. **What bounded unknown does that observation create?**

   It creates the bounded unknown: whether the note `.` has deterministic lexical overlap with already projected read-model material. The implementation explicitly limits this to projected fact supports and source-navigation matches, not semantic interpretation.

3. **What is the first justified inquiry?**

   The first justified inquiry is: does this preserved note have deterministic related material in existing projected read models? This is justified because the orientation implementation is defined as a read-only orientation view over a preserved inquiry note.

4. **What observation naturally follows?**

   The natural following observation is absence: no deterministic related material and no supportable lexical overlap were found.

5. **At what point does Seed independently discover the need for richer observation?**

   Seed reaches the need for richer observation immediately after the orientation view reports no related material and the projected observations/facts remain empty. The need is not a selected repository traversal; it is a supported limitation: current read models have no material from which to justify a next repository claim.

6. **Does Seed naturally invent or select a structure observer?**

   No. The implementation exposes a repository-source observer as a CLI surface, but the `.` orientation sequence did not select it, recommend it, or justify it. Invoking it would be operator selection, not Seed's natural discovery from `.`.

7. **Does the resulting inquiry sequence remain implementation-backed?**

   Yes, up to the stopping point. The sequence is backed by implemented inquiry-note preservation, read-only orientation rendering, projected observation/fact checks, and inquiry-artifact visibility. It stops before repository traversal because no implementation-backed transition selected such traversal.

## Transitions from unknown to supported knowledge

| Transition | Supported knowledge | Evidence |
| --- | --- | --- |
| Null → `.` | A raw inquiry note can be preserved without becoming a fact or command. | `--record-inquiry-note '.'` returned `inq_000001`; implementation describes inquiry notes as outside the event ledger and not facts/plans/commands. |
| `.` → orientation | Orientation asks only for deterministic overlap with already projected read models. | `--inquiry-orientation` rendered the note and reported no deterministic related material. |
| Orientation → absence | No current projected material supports a repository claim from `.`. | `--current-observations` and `--current-facts` returned `(none)`. |
| Absence → richer-observation need | More evidence would be required before repository claims can be justified. | inquiry-artifacts reports boundaries and partial/document-only visibility for inquiry artifacts. |
| Richer-observation need → stop | Structure traversal is not justified by the observed sequence alone. | no selected/recommended structure observer appeared in the outputs. |

## Unsupported transitions

The following transitions were intentionally not taken:

- Treating `.` as a repository root fact.
- Listing repository layout as experimental evidence.
- Running a repository source observer merely because one exists.
- Promoting presentation vocabulary into repository knowledge.
- Inferring operator intent, curiosity, plan, workflow, or architecture from `.`.
- Treating absence of matches as proof that no related repository material exists.

## First independently discovered observer need

The first independently discovered observer need is not a named structure observer. It is the narrower need for **additional evidence beyond the empty projected read models**. The implementation-supported form of that need is:

```text
No deterministic related material was found in already projected read models; this absence does not prove the note is unrelated to existing work.
```

That statement justifies stopping or obtaining more evidence, but it does not by itself justify which observer should be used next.

## First independently justified curiosity

The first independently justified curiosity is:

```text
Does the preserved note `.` have deterministic related material in already projected read models?
```

This curiosity is justified by the orientation implementation and by the note's preserved status. It is not a repository-map curiosity and does not assume architecture, observers, providers, diagnostics, ontology, or commands.

## Confidence

- **High confidence** that the experiment stayed inside the implemented inquiry-note/orientation boundary.
- **High confidence** that `.` did not create projected observations or facts in the fresh database.
- **High confidence** that no structure observer was naturally selected in the captured sequence.
- **Medium confidence** in the broader conclusion that Seed cannot currently move from `.` to repository structure without an operator-selected observer, because this experiment exercised the existing bounded inquiry surfaces rather than adding a new autonomous curiosity mechanism.

## Commands run

```bash
rm -f /tmp/seed-null-orientation.sqlite
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --record-inquiry-note '.'
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --inquiry-orientation
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --current-observations
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --current-facts
python -m scripts.seed_local --db /tmp/seed-null-orientation.sqlite --inquiry-artifacts
```
