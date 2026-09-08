# Input Interpretation Candidate Characterization

## Executive answer

Seed does **not** currently demonstrate a stable, recurring architectural boundary that sits between raw operator input and observation for the specific responsibility of producing multiple candidate interpretations of an observed token without selecting one.

The first implementation-visible responsibility after raw operator input depends on the entry surface:

1. In the CLI, `argparse` first classifies argv into explicit flags and the positional `message` list.
2. In one-shot runtime handling, the runtime first records the supplied text as an `input.user_message` event, then composes a decision input packet, asks the decision producer for exactly one structured decision, validates that decision, and routes it.
3. In repository observation, the CLI only calls repository observation when `--observe-repository PATH` is explicitly supplied; that path is resolved and checked as a git work tree by the repository observer.

For the motivating input `.` alone, the CLI treats it as a positional message, not as a repository path. Nothing in the reviewed implementation turns bare `.` into repository observation. The only observed `.`-to-repository path is explicit operator selection of a repository-observation surface such as `--observe-repository .`, where the flag, not the token alone, authorizes path/repository treatment.

Therefore:

```text
Insufficient implementation evidence.
```

to recognize a stable architectural boundary named candidate input interpretation. The repository has adjacent disciplines--exact question-family eligibility, bounded work selection, candidate discovery inside knowledge reachability, selection-path candidate explanation, repository observation safe unavailability, and raw inquiry-note preservation--but those do not collectively prove a recurring input-token interpretation stage.

## Implementation evidence reviewed

### CLI input surface

The CLI parser has a positional `message` argument with `nargs="*"`; absent a flag, tokens are collected as message words. The same parser has explicit bounded-ask flags (`--question-family`, `--surface-args`, `--presentation`) that are not inferred from free text.

The main CLI flow later joins `args.message` into `message`. If no earlier flag-driven surface handled the request and `message` exists, the app runs the message through the local runtime path. If observation flags exist without a message, observation ingestion runs. This shows a flag/message split, not a candidate interpretation set.

### Runtime input path

`Runtime.handle_user_message(...)` appends an `input.user_message` event containing the raw text, projects current state, composes a decision input packet, asks `decision_producer.decide(...)` for a decision, appends `model.decision.proposed`, validates the decision, and routes it only if validation and intent validation pass.

`DecisionValidator.validate(...)` validates a single `Decision.kind` branch (`answer`, `ask_question`, `request_tool`, `call_tool`, `propose_state_patch`, or `refuse`). It does not validate a list of candidate interpretations of the operator token.

### Repository observation path

`observe_repository(repository_path)` delegates to `GitRepositoryObservationProvider.observe(...)`. The provider resolves the supplied path, checks for a git executable, checks `git rev-parse --is-inside-work-tree`, and returns unavailable repository observation records when git is unavailable or the path is not a git work tree. Successful observation reads head, branch, remote, and porcelain status without writing the event ledger or mutating the cluster.

The CLI calls `observe_repository(args.observe_repository)` only under the `if args.observe_repository:` branch. That means repository observation is selected by an explicit CLI surface and explicit argument value, not by bare token promotion.

### Question family and bounded ask path

Question-family dispatch is exact-map based. `bounded_status_for_question_family(...)` classifies an exact `question_family` string as `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`. `bounded_work_eligibility_for_question_family(...)` returns permission and reason but does not select a dispatch surface. `bounded_work_selection_for_question_family(...)` requires permitted eligibility and then selects an implementation surface from `BOUNDED_ASK_DISPATCH_SURFACES`.

Tests explicitly prove eligibility is separate from surface selection and dispatch, and that diagnostic-only or not-dispatchable families do not become selected work.

### Adjacent recovery reports and investigations

Existing recovery documents repeatedly support exactness, boundedness, and stopping, but not a general input-token interpretation boundary:

- `runtime_question_recovery_characterization.md` says dispatch and CLI contracts become implementation artifacts when deterministic acceptance, rejection, or routing is required, and warns against planner-style expansion.
- `inquiry_navigation_selection_justification_recovery_investigation.md` says bounded selection checks same question family, rejects non-permitted eligibility, uses exact-map lookup, and does not preserve competing eligible candidates.
- `current_inquiry_actionability_reconciliation.md` says question-surface inventory maps question families to answering surfaces but does not route questions, infer arguments, or classify intent.
- `seed_competency_roadmap_v2.md` characterizes current readiness as strong for explicit identities and exact question families, but not ready for autonomous orientation over unfamiliar repositories.

## Current input interpretation path

### Bare `.` through CLI

Current observed path for:

```bash
python scripts/seed_local.py .
```

is:

```text
argv token "."
  -> argparse positional message list
  -> " ".join(args.message).strip() == "."
  -> LocalSeedApp.run(".")
  -> Runtime.handle_user_message(..., text=".")
  -> input.user_message event
  -> decision input composition
  -> one model/decision-producer decision
  -> validation
  -> route selected decision or invalid decision response
```

This path preserves the raw text as input, but it does not enumerate these possible interpretations:

```text
prose punctuation
current working directory
filesystem path
repository root
malformed input
operator shorthand
```

### Explicit `.` as repository path

Current observed path for:

```bash
python scripts/seed_local.py --observe-repository .
```

is:

```text
--observe-repository flag
  -> args.observe_repository == "."
  -> observe_repository(".")
  -> Path(".").expanduser().resolve()
  -> git work-tree check
  -> repository observation or unavailable repository observation
```

Here `.` becomes a filesystem/repository candidate because the operator supplied the repository-observation flag. The token alone does not authorize that promotion.

## Candidate interpretation characterization

The repository naturally supports this narrower discipline:

```text
explicit operator surface or exact family
  -> eligibility/status check
  -> selection only if permitted
  -> dispatch or safe non-selection
```

Evidence is strongest in question-family dispatch. Eligibility and selection are separate records, and non-permitted eligibility cannot be selected. However, that discipline starts after the operator has already supplied an exact question family or CLI flag. It does not start from an untyped raw token such as `.`.

For raw operator text, the runtime preserves text and delegates to a single structured decision producer. The implementation validates and routes one proposed decision, not a candidate set. Retry prompts repair invalid parse/validation/intent failures; they do not record or compare multiple candidate interpretations of the original token.

Therefore the candidate flow in the prompt is only partially supported by analogy:

```text
Observed token
  -> Candidate interpretations
  -> Evidence evaluation
  -> Safe stop or eligible interpretation
  -> Bounded observation
```

Current implementation evidence supports only these pieces:

- observed raw text is recorded;
- exact bounded asks can have eligibility before selection;
- selected surfaces can perform bounded read-only observation;
- non-eligible exact families and unavailable repository paths can stop safely.

It does **not** support the full interpreted-token stage.

## Safe-stop characterization

Safe stop is recurring, but not specifically as candidate input interpretation.

Supported safe-stop patterns include:

1. **Repository observation unavailability.** A non-git path or unavailable git binary returns a `RepositoryObservation` with `repository_status_available=False` and a reason instead of throwing or mutating.
2. **Question-family non-permission.** Diagnostic-only and not-dispatchable families return `permitted=False`; selection raises rather than silently dispatching.
3. **Runtime validation failure.** Invalid parsed decisions, invalid intent, or unsupported decision kinds lead to invalid-decision responses after bounded retries rather than arbitrary routing.
4. **Read-only diagnostics.** Many audit and diagnostic surfaces explicitly preserve no event-ledger writes and no cluster mutation.

These prove a repository-wide tendency toward bounded stopping, but not a stable responsibility that evaluates all interpretations of `.` and safely terminates the unsupported ones.

## Counterexamples

### Bare raw input does not become candidate interpretations

The CLI positional `message` behavior is a counterexample to a candidate interpretation boundary. A bare `.` is simply a message token. The implementation does not first ask whether it might be a path, repository root, punctuation, malformed input, or shorthand.

### Runtime routes a single decision

The runtime asks for exactly one model decision per attempt and validates that decision. This is a counterexample to multiple candidate interpretations coexisting at the raw-input boundary. Multiple retries may occur, but they repair invalid output rather than preserve alternative interpretations.

### Repository observation requires explicit surface selection

The repository observation path consumes `args.observe_repository`. That is a counterexample to automatic repository detection from raw text. `.` is resolved as a path only after the operator selects repository observation.

### Question-family maps are exact, not inferential

Question-family bounded ask supports eligibility and safe non-selection, but only for exact family strings. Existing documents explicitly say this inventory does not route questions, infer arguments, or classify intent. This is a counterexample to treating question-family machinery as an input interpretation owner.

### Existing candidates belong to other responsibilities

Candidate discovery and candidate explanation exist in other bounded contexts, such as knowledge reachability and selection-path audits. Those candidates are read-model or selection candidates after an inquiry surface is already chosen. They are not raw operator-token interpretations.

## Supported conclusions

1. **The first implementation-visible responsibility after raw operator input is surface-dependent.** CLI argv first goes through argparse classification; runtime one-shot text first becomes an `input.user_message` event and then a single decision input.
2. **The repository distinguishes raw input text from selected decisions.** Raw text is recorded separately from `model.decision.proposed`, and decisions undergo validation before routing.
3. **The repository does not demonstrate `Observed Token != Candidate Interpretation` as a stable first-class boundary.** No reviewed model or record type preserves raw token plus multiple candidate interpretations.
4. **Multiple candidate interpretations do not safely coexist at the raw-input boundary.** Multiple candidates coexist elsewhere, but not as interpretations of a raw operator token.
5. **Safe stop is recurring across repository observation, question-family eligibility, diagnostics, and runtime validation.** This is a general safety behavior, not proof of candidate input interpretation.
6. **The evidence authorizing `.` to continue as repository is explicit surface selection plus git evidence.** `--observe-repository .` authorizes path treatment; git work-tree checks authorize repository-status availability. Bare `.` does not.
7. **There is insufficient implementation evidence to recognize a stable architectural boundary for candidate input interpretation.** The repository has adjacent boundedness and safe-stop mechanisms, but not this boundary.

## Unsupported conclusions

The reviewed implementation does not support concluding that Seed currently has:

- a general input interpretation subsystem;
- a candidate-interpretation record model;
- multiple coexisting raw-token interpretations;
- automatic `.` repository detection;
- a constitutional rule that current working directory is the first observation;
- an intent engine, parser, classifier, planner, or LLM interpretation layer that should be added;
- evidence that `.` as punctuation, filesystem path, repository root, malformed input, and shorthand are all generated and evaluated before observation.

## Confidence

**Medium-high** for the negative conclusion: the main CLI, runtime, repository observation, question-family dispatch, and relevant tests/docs all point away from a stable candidate input interpretation boundary.

**Medium** for completeness: the repository is large and contains many historical investigations. The reviewed evidence is broad enough to answer the bounded question, but a future hidden or experimental surface could contain a more direct input-interpretation artifact. The current implementation-visible behavior, however, does not show it.
