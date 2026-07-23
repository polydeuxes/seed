# Step-Wise Inquiry Frontier Transition Audit 001

## Scope

This audit determines what the repository currently owns when an inquiry is communicated step by step and an operator intervenes before the current chain is complete.

It is an audit only. It does not implement a frontier transition engine, workflow graph, conversation binding layer, question-state model, branch manager, planner, router, schema, diagnostic surface, CLI flag, recordable output, event-ledger behavior, or cluster mutation.

The tested guardrails for this audit are:

```text
interrupted != completed
closed by new evidence != abandoned
constrained != answered
expanded != replaced
new branch != rewritten history
communication turn != inquiry step
```

Conversation-reference binding remains separate from any frontier transition. This audit asks what current implementation evidence already supports, not what a conversation system might infer.

## Evidence reviewed

Implementation and repository evidence reviewed:

- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_inquiry_artifacts.py`
- `tests/test_question_surface_inventory.py`
- `question_to_inquiry_transition_characterization.md`
- `question_bounded_work_invocation_investigation.md`
- `constitutional_transition_family_characterization.md`
- `inquiry_lineage_slice_001.md`
- `inquiry_lineage_slice_004.md`
- `bounded_inquiry_recovery_characterization.md`
- `inquiry_completion_evaluation_audit.md`
- `docs/archive/original_book_of_seed/12-open-questions.md`

Commands used during the audit:

```bash
rg --files -g 'AGENTS.md' -g '!vendor' -g '!node_modules'
rg --files | rg 'inquiry|question|frontier|conversation|continuation|knowledge|reachability|audit' | head -200
rg -n "inquiry|frontier|question|continue|constrain|expand|fork|supersede|close|diagnostic" -S .
sed -n '1,220p' inquiry_lineage_slice_001.md
sed -n '1,220p' inquiry_lineage_slice_004.md
sed -n '1,220p' question_to_inquiry_transition_characterization.md
sed -n '1,220p' bounded_inquiry_recovery_characterization.md
sed -n '1,220p' tests/test_inquiry_artifacts.py
sed -n '1,260p' seed_runtime/inquiry_artifacts.py
sed -n '1,260p' seed_runtime/inquiry_orientation.py
sed -n '1,520p' seed_runtime/question_surface_inventory.py
sed -n '1,240p' question_bounded_work_invocation_investigation.md
sed -n '1,200p' constitutional_transition_family_characterization.md
```

## Executive determination

The repository does **not** currently have one implementation owner for an active inquiry frontier.

The strongest existing owner-like responsibilities are narrower and distributed:

1. **Preserved operator inquiry material** is owned by the inquiry-note/orientation probe. It can preserve raw operator prose and orient it through deterministic lexical overlap, while explicitly refusing fact, claim, goal, requirement, command, plan, ownership, intent, recommendation, or next-safe-move authority.
2. **Known bounded question identity and executable bounded work** are owned by the question surface inventory and bounded-ask compatibility path. They require exact registered `QuestionFamily` lookup, eligibility, required-argument validation, selection of an existing surface, and dispatch into that surface.
3. **Inquiry artifact visibility** is owned by the inquiry-artifacts visibility surface only as read-only classification. It reports that open questions are document-visible, not implemented workflow or planning items.
4. **Outcome/lineage preservation** is an established implementation pattern across several surfaces, but it is not an active frontier-transition owner.

Therefore, the current lawful frontier after a mid-inquiry intervention can be described only as a **repository-evidence-preserving characterization**, not as an executable transition state machine.

## What existing implementation already supports

### 1. Preserving the inquiry before intervention

Existing implementation supports preservation of raw operator material as an `InquiryNoteRecord` with `note_id`, `raw_note`, `recorded_at`, `source`, optional `workspace_id`, and optional `session_id`.

That support is intentionally weak: the note is preserved as operator prose for orientation, not promoted into a fact, claim, goal, requirement, command, decision, proposal, plan, authorization, or runtime instruction.

Supported conclusion:

```text
previous inquiry material can be preserved as raw note/prose evidence for orientation
```

Unsupported conclusion:

```text
previous inquiry material is automatically a frontier node, step object, branch, obligation, or completed/abandoned inquiry
```

### 2. Preserving the active step

The repository does not currently expose an implemented active-step object for an ongoing inquiry chain.

Bounded ask can identify a selected `QuestionFamily`, dispatch surface, selected surface value, dispatch request, and dispatch result. That is an invocation path for one bounded work surface, not a step-wise active inquiry frontier.

Inquiry orientation can preserve and orient a note. It does not identify the note as the current step in a larger chain.

Supported conclusion:

```text
selected bounded work invocation can be represented for exact registered QuestionFamily execution
```

Unsupported conclusion:

```text
Seed currently stores a durable active inquiry step that can be continued, constrained, expanded, forked, superseded, or closed
```

### 3. Completed, active, and pending questions

Current evidence supports these distinctions only partially:

- Completed or evidence-bearing results appear as surface-local answers, reports, diagnostics, or explicit stops.
- Active executable work exists only during selected bounded surface invocation, not as durable general inquiry state.
- Open questions are visible in documents and reported by inquiry-artifacts visibility as `document_visible`, with a limitation that they are not workflow or planning items.
- Pending questions are not implemented as a general queue, frontier set, or state machine.

Supported conclusion:

```text
completed/evidence-bearing result != open document-visible question != selected bounded invocation
```

Unsupported conclusion:

```text
completed, active, pending, retained, constrained, opened, and closed questions are currently managed by one frontier owner
```

### 4. Operator's new material

The operator's new material can be preserved as raw inquiry note prose or supplied as exact bounded-ask inputs. The implementation does not semantically classify free text into `continue`, `constrain`, `expand`, `fork`, `supersede`, or `close` transition commands.

For bounded ask, free text is not routed. The repository requires exact registered question-family identity for bounded work invocation. For inquiry orientation, lexical overlap is deterministic and explicitly non-semantic.

Supported conclusion:

```text
operator material can be preserved or used as exact registered QuestionFamily input
```

Unsupported conclusion:

```text
operator intervention text is currently interpreted as a frontier transition command
```

### 5. Questions closed, retained, constrained, or opened

The repository supports the underlying safety distinctions as audit/report conclusions, but not as an implemented transition algebra:

- A question can reach an evidence-bearing result or explicit stop inside a selected surface.
- Unsupported material can remain unsupported without becoming truth.
- Open questions can be preserved in documents.
- Exact bounded work can be admitted or refused.
- Outcome and lineage can remain separate.

However, no implementation currently records a question as `closed`, `retained`, `constrained`, or `opened` in response to operator intervention.

Supported conclusion:

```text
closed by evidence, retained as open document material, and refused as not dispatchable are distinguishable outcomes in repository evidence
```

Unsupported conclusion:

```text
the repository currently applies closed/retained/constrained/opened transition labels to an active inquiry frontier
```

### 6. The resulting lawful inquiry frontier

The repository can lawfully describe the resulting frontier only by composing existing evidence:

```text
preserved prior material
+ current selected bounded work or orientation result, if any
+ operator's new preserved material or exact QuestionFamily input
+ surface-local evidence/result/stop boundaries
+ unchanged lineage frame
```

It cannot lawfully assert a new executable frontier state without implementation.

## Whether the repository already has an inquiry-frontier owner

No.

The closest candidates are intentionally insufficient:

| Candidate | What it owns | Why it is not the active inquiry-frontier owner |
| --- | --- | --- |
| `inquiry_orientation` | Preserved notes and read-only lexical orientation | It denies semantic routing, next-safe-move authority, planning, command, and truth promotion. |
| `question_surface_inventory` / bounded ask | Exact `QuestionFamily` registration, eligibility, required args, selected surface, dispatch request | It invokes one existing surface; it does not manage interrupted chain state or future frontier. |
| `inquiry_artifacts` | Read-only visibility classification of artifacts such as open questions | It explicitly refuses workflow/planning and inquiry movement inference. |
| Surface-local answer composition | Evidence collection, answer composition, rendering for specific surfaces | It does not own cross-surface step-wise frontier transition. |
| Inquiry lineage reports | Outcome/lineage boundary evidence | They are documentation and implementation-pattern audits, not a runtime owner. |

The repository therefore supports a distributed boundary map, not a single frontier owner.

## Lawful transition states supported by evidence

The terms below are not current implementation states. They are lawful audit descriptions backed by existing implementation evidence.

### Continue

Lawful only as continuing the same exact bounded question or same preserved inquiry note orientation if the operator's new material does not change the question boundary.

Current implementation support:

- bounded ask can invoke the same exact registered `QuestionFamily` again;
- inquiry orientation can select a preserved note and build a read-only view.

Unsupported:

- automatic continuation of a multi-turn inquiry chain;
- treating a communication turn as an inquiry step.

### Constrain

Lawful only as new operator material that narrows the question boundary while leaving prior lineage unchanged.

Current implementation support:

- exact required surface args can parameterize certain bounded question families;
- orientation can preserve the constraining material as prose.

Unsupported:

- considering the constrained question answered merely because it was constrained;
- rewriting prior inquiry history.

### Expand

Lawful only as opening additional related material or an additional bounded question while retaining the previous question and lineage.

Current implementation support:

- question inventory contains multiple registered families;
- inquiry orientation can expose deterministic related material;
- documents can preserve open questions.

Unsupported:

- replacing the previous inquiry merely because scope expanded;
- inferring semantic relatedness from presentation labels alone.

### Fork

Lawful only as a new branch-like characterization in documentation or as a separate exact bounded work invocation while previous lineage remains unchanged.

Current implementation support:

- bounded ask can invoke a different registered `QuestionFamily`;
- outcome/lineage patterns preserve alternatives and non-selected material in several surfaces.

Unsupported:

- implemented branch object;
- rewriting history of the interrupted inquiry.

### Supersede

Lawful only as a new operator material or new evidence making a prior question no longer the current selected focus while preserving the prior question as lineage.

Current implementation support:

- selection-path and reference-selection patterns preserve selected and non-selected material;
- bounded ask can select a different exact family for invocation.

Unsupported:

- deleting, abandoning, or completing the prior inquiry by implication;
- promoting supersession into truth without evidence.

### Close

Lawful only when the selected surface produces an evidence-bearing result, explicit stop, or insufficiency conclusion.

Current implementation support:

- diagnostic/audit and answer surfaces can produce conclusions, negative findings, or explicit limitations;
- transition-family evidence distinguishes inquiry from evidence-bearing result or explicit stop.

Unsupported:

- treating interruption as completion;
- treating closed by new evidence as abandoned.

## Historical inquiry lineage remains unchanged

Historical lineage remains unchanged because the existing repository patterns preserve prior material as separate from current outcome:

```text
outcome != lineage frame
selected result != selection lineage
reference choice != comparison lineage
```

A lawful frontier transition must therefore append or compose new material beside the preserved lineage frame. It must not overwrite the previous question, selected/non-selected alternatives, supports, limitations, authority boundaries, unknowns, or open questions.

Applied to the guardrails:

- `interrupted != completed`: interruption is only new material or orientation pressure unless a surface produces an evidence-bearing close.
- `closed by new evidence != abandoned`: closure requires evidence or explicit stop; abandonment is not currently implemented as an inquiry state.
- `constrained != answered`: constraints can narrow surface args or prose boundary; they do not supply evidence by themselves.
- `expanded != replaced`: expansion can add another question or related material without erasing the previous one.
- `new branch != rewritten history`: a different bounded work invocation is additional lineage, not mutation of prior lineage.
- `communication turn != inquiry step`: the implementation has notes, exact question-family dispatch, and surface-local results, but no general turn-to-step binding.

## Conversation-reference binding is separate

The repository currently lacks an implementation that binds conversation references such as "this", "that", "continue", or "the current question" to an inquiry object. Existing inquiry orientation deliberately avoids semantic interpretation and intent inference.

Therefore, a future frontier transition implementation would need two separate boundaries:

```text
conversation reference binding
    identifies what operator prose points at

frontier transition
    decides what happens to preserved questions and lineage after the target is known
```

This audit finds evidence for the separation, not an existing implementation of either general capability.

## Is one implementation slice warranted?

Yes, but only one narrow slice is warranted, and it should not implement the whole transition algebra.

The warranted slice is a read-only characterization/visibility slice that makes the current absence explicit and testable without creating a planner or state machine.

Smallest lawful candidate:

```text
Expose or test a read-only inquiry-frontier transition inventory over existing evidence that reports:
- no active frontier owner exists;
- inquiry_orientation preserves raw operator material but does not infer movement;
- bounded ask owns exact QuestionFamily eligibility/dispatch, not step-wise frontier state;
- inquiry_artifacts reports open questions as document-visible and non-workflow;
- outcome/lineage preservation prevents history rewriting.
```

However, because this job explicitly says not to implement anything, the slice remains only a recommendation.

An implementation slice would be unwarranted if it attempted any of the following first:

- adding `continue/constrain/expand/fork/supersede/close` as executable commands;
- creating durable active frontier state;
- inferring conversation references;
- converting open document questions into workflow items;
- rewriting bounded ask as a general question router.

## Exact next bounded question

```text
What is the smallest read-only implementation surface that can prove, from existing inquiry_orientation, inquiry_artifacts, bounded ask, and lineage evidence, that Seed has no active inquiry-frontier owner while preserving the distinction between operator material, exact QuestionFamily invocation, open document questions, and historical lineage?
```

## Final conclusion

Current repository authority supports preservation, exact bounded invocation, read-only orientation, open-question visibility, and lineage preservation. It does not support a general active inquiry-frontier owner or executable mid-inquiry transition algebra.

Step-wise inquiry frontier transition audit complete.
