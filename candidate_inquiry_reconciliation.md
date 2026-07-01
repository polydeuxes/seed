# Candidate Inquiry Reconciliation

## Executive answer

The previous implementation report remains correct: current implementation evidence is still insufficient to recognize a first-class **Candidate Interpretation** owner for raw input tokens such as `.`.

Subsequent architectural recovery does, however, support a narrower and better-fitting constitutional characterization:

```text
ambiguous observation
  -> multiple candidate bounded inquiries may be framed by the operator or by an existing exact surface
  -> each inquiry gathers or composes evidence inside its own authority boundary
  -> unsupported inquiries stop safely
  -> only evidence-bearing inquiries continue toward justified knowledge
```

This is not an implementation claim that Seed currently tokenizes `.` and automatically spawns runtime inquiry records. It is a repository-evidence claim about the constitutional mechanism Seed repeatedly prefers when uncertainty must be reduced: bounded, evidence-bearing inquiry with explicit eligibility and safe stop, rather than direct semantic interpretation or an interpretation engine.

The strongest answer to the acceptance question is therefore:

```text
Seed does not currently reduce ambiguity in a bare token by selecting one
candidate interpretation.

Repository evidence more strongly supports reducing ambiguity through bounded
questions that acquire or compose evidence, stop when unsupported, and only
continue when constitutionally eligible.
```

## Previous implementation conclusion

`input_interpretation_candidate_characterization.md` remains implementation-correct. It found that a bare `.` travels through the CLI as a positional message, while repository treatment of `.` happens only when an explicit surface such as `--observe-repository .` is selected. It also found no reviewed model or record type that preserves a raw token plus multiple candidate interpretations.

That report should not be invalidated. Its negative conclusion is a boundary condition for this reconciliation:

- no first-class Candidate Interpretation implementation owner is recovered;
- no automatic `.` repository detection is recovered;
- no tokenizer-to-interpretation pipeline is recovered;
- no new implementation, planner, classifier, intent engine, or interpretation engine is recommended.

The refinement is only that the phenomenon motivating the rejected owner may have been misnamed. The repository can reject “candidate interpretation” as an implementation owner while still supporting “candidate inquiry” as the constitutional way uncertainty is handled after a bounded question has been framed.

## Architectural reconciliation

The original motivating diagram was:

```text
Observed Token
  -> Candidate Interpretations
  -> Evidence
  -> Selected Interpretation
```

Repository evidence supports replacing it with a weaker, bounded inquiry diagram:

```text
Ambiguous observation or pressure
  -> candidate bounded inquiries
  -> eligibility / authority check
  -> evidence-bearing inquiry or safe stop
  -> answer, recovery, or remaining inquiry
```

The difference matters.

A **candidate interpretation** says the token already sits inside a semantic competition for meaning. That implies a preserved interpretation space and a selection result. The implementation report did not find that.

A **candidate inquiry** says the observation can legitimately raise several bounded questions, each with its own evidence requirements and stop condition. For `.` those questions might be:

- Is this punctuation?
- Is this a filesystem path?
- Is this a repository reference?
- Is this the current working directory?
- Is this malformed input?
- Is this an operator shorthand?

Current implementation does not automatically ask all of these. But repository recovery repeatedly treats unresolved uncertainty as a matter of bounded questions, exact surfaces, eligibility, evidence acquisition/composition, and safe non-promotion.

## Repository evidence reviewed

### Raw input and repository observation

The previous report provides the primary negative implementation evidence. Bare `.` is a positional message, not a repository path. `--observe-repository .` is different because the explicit repository-observation surface authorizes path treatment and then `GitRepositoryObservationProvider` resolves the path and checks whether it is a git work tree.

The repository observation implementation also demonstrates safe stop. If git is unavailable or the path is not a git work tree, the observer returns an unavailable `RepositoryObservation` with `repository_status_available=False` and a reason, while preserving `writes_event_ledger=False` and `mutates_cluster=False`.

### Runtime Question characterization

`runtime_question_recovery_characterization.md` says mature recovery usually terminates as a runtime-owned question or answer surface, not as a new durable runtime object that stores every recovered concept. It also states that new durable runtime artifacts are justified only when implementation needs state, provenance, registry identity, dispatch identity, catalog data, or a recording boundary.

This supports candidate inquiry over candidate interpretation because the recovered constitutional movement is toward answerable bounded surfaces, not toward a durable interpretation object for every ambiguous concept.

### Inquiry Eligibility

`inquiry_eligibility_characterization.md` recognizes a distributed competency that determines whether a candidate inquiry, boundary, vocabulary, family, or implementation direction has been constitutionally earned by repository evidence. It explicitly distinguishes eligibility from Methodological Selection: eligibility determines whether candidates have earned consideration at all, while selection explains ordering among eligible or implemented candidates.

That is direct support for treating ambiguous observations as possible inquiries subject to eligibility and safe rejection rather than as meanings subject to immediate selection.

### Question Family and bounded ask

`seed_runtime/question_surface_inventory.py` implements exact Question Family dispatch maps, bounded status derivation, eligibility results, selection results, and dispatch requests. The code classifies exact families as `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`. It permits bounded work only for eligible statuses and refuses diagnostic-only or unmapped families.

`scripts/seed_local.py` enforces the same boundary at the CLI: `ask` requires `--question-family <exact-question-family>`, unknown families are rejected, parameterized families require exact `--surface-args`, diagnostic-only families are rejected as inquiry-answer surfaces, and non-dispatchable families are rejected.

This is a strong implementation pattern for bounded inquiry, exact eligibility, and safe non-dispatch. It is not semantic interpretation of free text.

### Methodological Selection

`operator_methodological_selection_characterization.md` finds that the operator currently performs decisive pre-inquiry selection: reviewing unresolved pressure, identifying evidence-bearing artifacts, bounding the next question, choosing a Question Family or subject manually, and invoking implementation that begins only after that choice is supplied.

This supports candidate inquiries as constitutional objects of operator and repository methodology, while rejecting a hidden implementation-owned selector.

### Observation Transition

`observation_transition_recovery_characterization.md` identifies the authority-bearing movement as bounded observation or implementation-backed inquiry producing preserved evidence, followed by bounded interpretation, recovery, answer, or stop. It rejects discussion alone as sufficient to recover architecture.

This directly answers how ambiguity is reduced: not by conversational preference and not by direct interpretation, but by evidence-bearing inquiry or explicit insufficiency.

### Inquiry Orientation and null/orientation discussions

`seed_runtime/inquiry_orientation.py` preserves inquiry notes as operator prose outside the event ledger, finds related material by deterministic lexical overlap, and explicitly refuses to treat the note as a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, runtime instruction, semantic interpretation, ownership assertion, intent, recommendation, or next safe move.

Orientation evidence therefore supports the same boundary: preserve the ambiguous or motivating material, show bounded related material, state uncertainty, and refuse semantic promotion without evidence.

### Repository Artifact versus Runtime Artifact

The runtime-question characterization and repository-artifact discussions support a recurring distinction: documentation artifacts can preserve constitutional claims, negative findings, methodology, and candidate direction without making those concepts runtime artifacts. That distinction matters here. Candidate inquiries are supported as a constitutional/recovery pattern; they are not thereby promoted into a new runtime artifact.

### Answer Composition

Answer Composition evidence supports bounded answers with answer material, reasons, support, boundaries, unknowns, and limitations. That aligns with inquiry: a bounded question composes an answer from evidence under limits. It does not require a prior selected interpretation object.

## Comparison: interpretation versus inquiry

### Model A: Candidate Interpretation

```text
Observation
  -> Candidate Interpretation
  -> Selected Meaning
```

Repository support is weak for Model A at the motivating boundary.

Supported pieces:

- Some later surfaces use the word `interpretation` for bounded, evidence-backed views.
- Facts and projections can represent validated or projected interpretations of evidence.
- Some provider adapters perform provider-local interpretation after an explicit provider surface is already chosen.

Unsupported pieces:

- No reviewed implementation stores raw `.` plus multiple candidate meanings.
- Bare `.` is not promoted to path/repository/current-working-directory by interpretation.
- Runtime validates one proposed decision rather than preserving a candidate-meaning set.
- Question Family dispatch is exact and non-semantic.

Model A overstates the repository evidence when applied to the motivating phenomenon.

### Model B: Candidate Inquiry

```text
Observation
  -> Candidate Inquiries
  -> Evidence-bearing Inquiry
  -> Independent Safe Stops
  -> Remaining Inquiry
```

Repository support is stronger for Model B, with one limitation: the multiple inquiries are constitutionally legitimate, but not automatically generated from `.` by current implementation.

Supported pieces:

- Exact Question Families are bounded inquiry identities.
- Eligibility can permit, parameterize, reject as diagnostic-only, or reject as not dispatchable.
- Repository observation can safely return unavailable rather than overclaim.
- Inquiry Orientation preserves operator prose and bounded lexical related material without semantic interpretation.
- Observation Transition says recovery moves through evidence-bearing inquiry or stop.
- Methodological Selection says the operator frames and chooses the next bounded inquiry before implementation dispatch.
- Inquiry Eligibility says insufficient evidence is a completed negative result, not a failure to interpret.

Model B better fits the constitutional pattern as long as it is stated carefully:

```text
Candidate inquiries are a supported recovery/methodology pattern.
They are not currently an automatic runtime token-expansion artifact.
```

## Counterexamples reviewed

### Counterexample: direct interpretation exists in provider-local code

Provider adapters and later read views sometimes perform bounded interpretation after an explicit surface, provider, or domain has already been selected. This is real evidence that Seed has interpretation in some bounded contexts.

It is not evidence for Model A at the raw-token boundary. Provider-local interpretation begins after the operator or implementation has already chosen a provider/surface and acquired evidence.

### Counterexample: facts and projections are interpretations

Seed can normalize observations into facts and project read models. That is a form of evidence-backed interpretation.

It is not direct ambiguity resolution without inquiry. The constitutional sequence still depends on observation, evidence, provenance, projection, support, contradiction handling, and authority boundaries.

### Counterexample: Selection Path selects among candidates

Selection Path can explain selected results, candidate sets, non-selected candidates, and unknowns for supplied targets.

It does not prove raw input candidate interpretation. The selection target is supplied, unknown targets stop explicitly, and selection-path ownership remains local to its implemented surface.

### Counterexample: Question Family exactness could be inconsistent with multiple candidate inquiries

The exactness of Question Family dispatch limits automatic candidate generation, but it does not contradict candidate inquiries. It shows that inquiries must be bounded, explicitly identified, eligible, and dispatchable before implementation execution. Multiple candidate inquiries can exist at the methodological/recovery level; each must independently earn eligibility before dispatch.

### Counterexample: direct semantic routing from `ask` could exist

The bounded ask implementation is the opposite: it requires an exact Question Family and rejects unknown, diagnostic-only, or non-dispatchable families. No semantic routing counterexample was found in the reviewed evidence.

## Recovery questions answered

### 1. Does the previous implementation report remain correct?

Yes. The repository still lacks sufficient implementation evidence for a first-class Candidate Interpretation owner at the raw-token boundary.

### 2. Is the motivating phenomenon better explained by candidate inquiries than candidate interpretations?

Yes, at the constitutional/recovery level. The repository repeatedly prefers bounded questions, eligibility, evidence-bearing inquiry, answer composition, authority boundaries, and safe stops over raw semantic interpretation.

### 3. Can one observation constitutionally generate multiple bounded inquiries?

Yes, with careful wording. One ambiguous observation can legitimately motivate several bounded questions, but current implementation does not automatically spawn them as runtime records. The operator or an exact implemented surface frames the inquiries; each inquiry then needs its own eligibility and authority boundary.

### 4. Can those inquiries independently reach safe stop?

Yes. Safe stop is supported by question-family non-permission, parameter requirements, diagnostic-only rejection, repository observation unavailability, unknown selection targets, unsupported reference-selection domains, inquiry-orientation uncertainty, and insufficient-evidence conclusions.

### 5. How is ambiguity actually reduced?

Ambiguity is reduced by evidence-bearing inquiry, not by direct semantic selection. A bounded inquiry identifies required evidence, acquires or composes existing evidence, reports support and limits, and either produces a justified answer/recovery or stops with insufficiency.

### 6. Does this better align with Runtime Questions and Inquiry Eligibility?

Yes. Runtime Question recovery says recovered concepts usually terminate as answerable question or answer surfaces rather than durable runtime objects. Inquiry Eligibility says candidates must be constitutionally earned before consideration and can stop with insufficient evidence. Candidate inquiry aligns with both; Candidate Interpretation does not.

### 7. Is there sufficient repository evidence to recognize this as a recurring architectural pattern?

Yes, as a recurring architectural/recovery pattern, not as a new implementation subsystem. The evidence is sufficient for this formulation:

```text
When ambiguity or pressure appears, Seed constitutionally prefers bounded,
evidence-bearing inquiries with eligibility and safe stop over unbounded semantic
interpretation.
```

The evidence is insufficient for this stronger formulation:

```text
Seed currently implements an automatic Candidate Inquiry owner that expands raw
ambiguous tokens into multiple runtime inquiry records.
```

## Supported conclusions

1. The previous rejection of Candidate Interpretation remains correct.
2. The repository more strongly supports candidate bounded inquiries than candidate interpretations for the motivating phenomenon.
3. One observation can constitutionally motivate multiple bounded inquiries.
4. Those inquiries can independently stop when eligibility, evidence, authority, or implementation support is insufficient.
5. Ambiguity is reduced through evidence-bearing inquiry, not immediate selected meaning.
6. The pattern aligns with Runtime Questions, Inquiry Eligibility, Methodological Selection, Observation Transition, Inquiry Orientation, and Answer Composition.
7. Candidate Inquiry is a constitutional/recovery pattern, not a currently implemented automatic runtime artifact.

## Unsupported conclusions

The reviewed evidence does not support concluding that Seed currently has:

- a Candidate Interpretation implementation owner;
- a Candidate Inquiry implementation owner for automatic raw-token expansion;
- automatic interpretation of bare `.` as repository, path, current directory, punctuation, shorthand, or malformed input;
- semantic routing from arbitrary operator prose into Question Families;
- a hidden planner, intent engine, LLM classifier, heuristic selector, interpretation engine, or autonomous inquiry generator that should be added;
- authority to promote presentation vocabulary into repository knowledge without implementation evidence.

## Confidence

**High** confidence that the previous implementation conclusion remains correct.

**Medium-high** confidence that candidate inquiry is the better constitutional characterization of the motivating phenomenon. The evidence is broad and recurring across exact Question Family dispatch, Inquiry Eligibility, Methodological Selection, Observation Transition, Inquiry Orientation, repository observation safe stop, and Answer Composition.

**Medium** confidence on the “multiple inquiries from one observation” formulation because it is strongest as a constitutional/methodological pattern and weaker as direct implementation evidence. The repository supports multiple bounded questions as legitimate, but current implementation does not automatically generate them from an ambiguous token.
