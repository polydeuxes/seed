# Orientation-Guided Recovery Methodology Characterization

## Status

This is a repository characterization, not an implementation proposal.

It asks whether the repository is more faithfully recovered by preserving a current bounded explanation, letting incoming implementation evidence expose only the insufficient region, and repairing that region locally. It does **not** assume that `orientation` is a constitutional participant, runtime competency, planner, or new architectural owner.

Repository authority wins.

## Smallest truthful answer

Yes, with narrow bounds.

The repository repeatedly rewards this discipline:

```text
current bounded explanation
→ incoming implementation evidence
→ exact insufficiency becomes visible
→ still-valid structure is preserved
→ only the insufficient region is repaired or stopped
→ the next question is bounded by the repaired explanation
```

That recurrence is implementation-backed across inquiry orientation, bounded ask dispatch, diagnostic inventory/shape audit, diagnostic recording boundaries, and prior investigation artifacts. It is not proof of a global orientation engine. The supported claim is methodological and local: recovery becomes more faithful when the operator keeps the current explanation under repair instead of discarding it whenever one boundary fails.

The alternative explanation remains partly valid: this is also an operator habit in prose investigations. The repository does not automate the whole loop. What the implementation does show is that its executable surfaces are designed in ways that reward the habit: exact admission, negative authority, typed unknowns, read-only boundaries, shape checks, and compatibility-preserving stops all make broad replacement less truthful than local repair.

## Evidence reviewed

Implementation and tests reviewed:

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_diagnostic_inventory.py`
- repository investigation artifacts, especially:
  - `orientation_insufficiency_transition_characterization.md`
  - `possible_observation_to_lawful_question_competency_interrogation.md`
  - `pressure_audit_smallest_owner_investigation.md`

Checks run:

```bash
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --question-family-explanation "inquiry orientation" --json
pytest -q tests/test_inquiry_orientation.py tests/test_diagnostic_inventory.py
```

The app checks were used to confirm that question-family and inquiry-orientation boundaries are visible through repository surfaces, not merely asserted in prose.

## Recurring reading discipline recovered

### 1. Inquiry orientation preserves the note, then denies excess authority

**Current explanation.** A preserved inquiry note can orient investigation.

**Incoming evidence.** `record_inquiry_note` stores raw operator prose in an isolated JSONL probe store. `build_inquiry_orientation` composes a read-only orientation view from deterministic lexical overlaps.

**Local insufficiency exposed.** The explanation "the note tells the repository what to do" fails. The implementation explicitly treats the note as preserved prose, not as fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, ownership, recommendation, or next move.

**What remains valid.** The raw note remains valid evidence for the orientation probe. Related material remains valid as lexical overlap against existing projected state and source-navigation surfaces.

**Smallest repair.** Repair the explanation from "note authorizes action" to "note can provide read-only orientation with explicit uncertainty and authority boundary."

**Structure that survives unchanged.** The note, its provenance, the related material list, support strings, and uncertainty are preserved. The runtime state is not mutated by recording a note.

**New lawful question made visible.** If a note does not authorize action, the next lawful question becomes: which exact question family or diagnostic surface, if any, can answer the bounded concern?

### 2. Bounded ask admits exact families instead of reinterpreting prose globally

**Current explanation.** A question-like request may be executable.

**Incoming evidence.** `bounded_status_for_question_family` classifies exact question-family strings into `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`. `bounded_work_eligibility_for_question_family` returns a permission result with required parameters and a reason.

**Local insufficiency exposed.** The explanation "question-like language is enough to invoke work" fails. `scripts/seed_local.py` rejects unknown `QuestionFamily` strings, rejects parameters for families that do not accept them, requires exact parameters for parameterized families, rejects diagnostic-only families as inquiry-answer surfaces, and rejects not-dispatchable families.

**What remains valid.** Known question families remain valid. Eligible families can still dispatch to existing CLI surfaces. Diagnostic-only families remain valid diagnostic surfaces even when they are not inquiry-answer surfaces.

**Smallest repair.** Repair from "the question is broadly meaningful" to "the question is lawful only if it is an exact inventory-backed family with compatible bounded status and required arguments."

**Structure that survives unchanged.** The inventory row, bounded status, dispatch surface, required-argument contract, and existing CLI namespace remain the preserved structure.

**New lawful question made visible.** Once a family is rejected, the lawful next question is not a new global theory; it is whether the request maps to an existing family, should stop as unknown, or requires a separate implementation-backed registration/change.

### 3. Dispatch is narrowed to invocation, not answer ownership

**Current explanation.** Once bounded work is selected, the dispatch path might own the full answer.

**Incoming evidence.** `bounded_work_dispatch_request_for_selection` and `execute_bounded_work_dispatch` explicitly say they recover only existing CLI invocation/execution. They deny ownership of question lookup, eligibility, selection, answer composition, rendering, evidence interpretation, and semantic routing.

**Local insufficiency exposed.** The explanation "dispatch owns the investigation" fails.

**What remains valid.** Dispatch remains a lawful local step after selection.

**Smallest repair.** Repair from "dispatch is the owner" to "dispatch is only the already-selected invocation boundary."

**Structure that survives unchanged.** Eligibility and selection remain prior structures; answer composition and surface-local evidence remain later structures.

**New lawful question made visible.** The next question becomes which neighboring owner handles answer composition, evidence interpretation, or rendering, rather than whether dispatch should absorb them.

### 4. Diagnostic inventory and shape audit enforce visibility without promoting diagnostics into cluster truth

**Current explanation.** A diagnostic surface can be added or reasoned about by its visible output.

**Incoming evidence.** The diagnostic shape audit defines auditable fields such as `supports_record`, `supports_json`, `record_scope`, `writes_event_ledger`, `uses_projected_state`, and `mutates_cluster`. The inventory tests require recording diagnostics to declare `record_scope == "diagnostic_run"`, require those entries to write the event ledger, and require all current diagnostics not to mutate the cluster.

**Local insufficiency exposed.** The explanation "diagnostic output is just another fact surface" fails. Recording and mutation boundaries are independently checked.

**What remains valid.** Diagnostics remain valid operational visibility. Recorded diagnostics may write ledger events when scoped as diagnostic runs. Read-only diagnostics remain valid without cluster mutation.

**Smallest repair.** Repair from "diagnostic output can silently become truth" to "diagnostic surfaces must declare and be shape-audited for record scope, ledger writes, projected-state reads, and cluster mutation."

**Structure that survives unchanged.** Existing diagnostic rows, implementation specs, field-level shape audit, and inventory tests remain the preserved structure.

**New lawful question made visible.** When a diagnostic changes, the next lawful question is whether the diagnostic inventory and shape-audit specs still describe the implementation.

### 5. Prior recovery artifacts repeatedly preserve valid structure after insufficiency

Prior artifacts already recover the same local repair behavior:

- `orientation_insufficiency_transition_characterization.md` concludes that a bounded orientation remains usable until incoming implementation-backed evidence exposes a specific explanatory or authority insufficiency; then the prior orientation is preserved as partial/local, the insufficiency is typed, and the next lawful act is bounded.
- `possible_observation_to_lawful_question_competency_interrogation.md` rejects a universal possible-observation-to-question competency and instead preserves family-local ownership: Inquiry Orientation owns note-to-orientation, Question Surface Inventory owns exact public question-family identity, and selected surfaces own evidence and answer behavior.
- `pressure_audit_smallest_owner_investigation.md` preserves the existing `PressureItem` category builders while identifying a smaller repeated pressure-row assembly sequence, but stops because no intermediate type or independent consumer proves the recovery is ready.

These artifacts matter because they do not merely repeat a preferred vocabulary. They demonstrate the same discipline under different subjects: keep the working explanation, identify the precise region that no longer explains the implementation, preserve neighbors, and stop where the implementation does not yet support a smaller owner.

## Preservation behavior

The repository repeatedly preserves:

1. **Raw operator material without promotion.** Inquiry notes remain raw prose and do not become runtime state.
2. **Existing state while adding orientation.** Orientation rendering reads projected state and source navigation but does not create facts, goals, decisions, proposals, or plans.
3. **Known families despite rejected invocations.** A family can remain known while being diagnostic-only or not dispatchable.
4. **Diagnostic visibility without mutation.** Diagnostic surfaces can write diagnostic-run scoped records or remain read-only while preserving `mutates_cluster=false`.
5. **Compressed owners until recovery is earned.** Pressure audit evidence can reveal a possible smaller owner while still preserving the current implementation when no independent owner is proven.

This is the strongest implementation-backed answer to the prompt: faithful recovery comes from preserving what still explains reality.

## Local repair behavior

Local repair appears as a repeated implementation shape:

| Incoming insufficiency | Preserved structure | Smallest repair |
| --- | --- | --- |
| Inquiry note appears action-like | raw note, lexical matches, authority boundary | classify as read-only orientation only |
| Question-like input appears executable | exact inventory families and bounded statuses | require exact family, eligibility, and args |
| Diagnostic-only family appears answerable | diagnostic surface identity | reject as inquiry-answer surface while preserving diagnostic role |
| Dispatch appears to own answer semantics | selected surface invocation | limit dispatch to CLI namespace mutation |
| Diagnostic record appears truth-like | diagnostic run subject and ledger write boundary | require `record_scope=diagnostic_run` and `mutates_cluster=false` |
| Potential smaller pressure owner appears | existing category builders and `PressureItem` contract | preserve as typed pressure until independently consumed |

The recurrence is not that every artifact says "orientation." The recurrence is that insufficient explanations are repaired at the boundary where they fail.

## Negative analysis

Implementation-backed evidence rejects the following moves.

### Replacing entire explanations unnecessarily

The inquiry-orientation implementation does not discard the note when the note lacks command authority. It preserves the note and repairs only its authority status. The bounded ask path does not discard the question-family inventory when one family is not dispatchable. It preserves the family and rejects only the unsupported invocation.

### Promoting broad theories before local repair

Question dispatch is map-backed and exact. Unknown family strings are rejected before semantic interpretation. Diagnostic-only families are stopped before being treated as answer surfaces. This rejects a broad theory that "questions" or "diagnostics" are one universal executable category.

### Discarding valid structure because one boundary failed

When a surface is diagnostic-only, diagnostic identity remains valid. When a note has only lexical overlap, the overlap remains valid support even though it does not prove intent or importance. When pressure audit evidence suggests a smaller row-assembly pattern, existing category builders remain valid because no independent intermediate owner is implemented.

### Answering before local insufficiency is understood

The bounded ask parser validates known family identity, bounded status, and required arguments before dispatch. Inquiry orientation renders uncertainty and authority boundary before any later work is authorized. Diagnostic inventory tests require record scope and mutation status to be declared before diagnostic recording can be treated as lawful visibility.

## Typed unknowns

1. **Global orientation participant:** not recovered. No implementation proves an `Orientation` constitutional participant or runtime owner.
2. **Automated continuous explanation repair:** not recovered. The repository supports local boundaries and stops, but the full repair loop remains operator-mediated.
3. **General semantic question formation:** not recovered. Exact question-family dispatch exists; free-prose semantic conversion does not.
4. **Universal recovery methodology engine:** not recovered. Methodology appears in artifacts and boundary-preserving implementation patterns, not as a scheduler or engine.
5. **When a local repair should become new implementation:** typed unknown. Prior readiness and pressure artifacts require independent implementation pressure, tests, and owner evidence before changing code.
6. **Whether all future investigations should follow this style:** likely useful but not constitutionally mandated by implementation evidence.

## Lawful termination

The investigation should stop at a methodology characterization.

It would be unlawful, on current evidence, to implement an orientation participant, global recovery engine, semantic question generator, or automatic explanation-repair loop. The implementation-backed recovery is smaller: repository surfaces repeatedly reward exactness, preservation, bounded admission, typed unknowns, negative authority, and local stops.

## Remaining questions

- Can a future app surface expose investigation-local explanation repair without turning operator methodology into cluster truth?
- Are there additional families where local insufficiency produces a recurring smaller owner that is independently consumed by code?
- Should pressure/readiness reports define a stricter threshold for when a repeated methodological shape becomes implementation-worthy?
- Can diagnostic or question-family inventories represent more typed unknowns without expanding their authority beyond visibility?

## Confidence

**Medium-high** for the narrow claim: implementation evidence repeatedly rewards preserving current understanding and repairing only the smallest insufficient region.

**Low** for any stronger claim: the repository does not prove a constitutional orientation participant, runtime cognition, autonomous repair loop, or universal methodology engine.

## Final answer to acceptance question

The repository repeatedly rewards preserving current understanding and repairing only the smallest insufficient region.

That is not merely an operator habit, because executable boundaries also enforce it: inquiry orientation preserves prose without promotion, bounded ask rejects unsupported invocations while preserving known families, dispatch refuses answer ownership, and diagnostic inventory/shape tests preserve visibility boundaries.

But the habit is not fully automated by the repository. The lawful characterization is:

```text
Repository implementation rewards orientation-guided local repair,
but does not recover Orientation as a new participant.
```

Preserve continuity. Repair locally. Stop where implementation stops.
