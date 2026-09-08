# Program Review Evaluation Readiness Investigation

## Scope

This is a bounded implementation investigation into whether Seed now contains enough recovered architecture to support a bounded **Program Review Evaluation** inquiry: reviewing an unfamiliar software system before proposing implementation changes.

It is not an implementation of program review, autonomous debugging, repository import, code modification, planning, automation, ownership recovery, or inquiry redesign. Repository authority wins. This report recovers implementation evidence only and treats vocabulary as evidence only where tied to completed implementation-backed investigations, code surfaces, tests, diagnostics, compatibility handoffs, or explicit authority boundaries.

## Implementation evidence reviewed

Primary evidence reviewed:

- `responsibility_recovery_evaluation_readiness_investigation.md`
- `slice_evaluation_readiness_investigation.md`
- `responsibility_authority_frontier_reconciliation.md`
- `docs/architectural_recovery_methodology_characterization.md`
- `docs/answer_composition_family_completion_audit.md`
- `responsibility_family_completion_inquiry_audit.md`
- `implementation_responsibility_family_stack_audit.md`
- Operational Responsibility slices 001-006
- Read-Model Ownership slices 001-005 and `read_model_ownership_family_completion_audit.md`
- Projection Influence Lineage slices 001-004 and `projection_influence_lineage_family_completion_audit.md`
- Inquiry Lineage slices and vocabulary audit
- Inquiry implementation evidence around `seed_runtime/question_surface_inventory.py`, `seed_runtime/inquiry_orientation.py`, bounded ask/dispatch investigations, and inquiry subject/identity/anchor investigations referenced by the frontier reconciliation

The review looked for recurring implementation evidence involving intended responsibility, fulfilled responsibility, observed implementation evidence, authority boundaries, visibility sufficiency, compatibility expectations, explicit boundary artifacts, bounded recommendations, and counterexamples where recommendations or fixes proceed without implementation evidence.

## Central finding

Seed contains enough recovered architecture to **support a bounded Program Review Evaluation inquiry in principle**, but only as a read-only, evidence-first evaluation pattern for a human-scoped unfamiliar system. The repository does not currently support an implemented program-review command, repository importer, autonomous debugger, automatic code modifier, planner, or semantic architecture interpreter.

The implementation-backed shape is close to the proposed chain, but the repository-supported version needs stricter bounds:

```text
human-scoped program purpose or observed operator claim
↓
expected responsibilities stated as candidate responsibilities, not presumed truth
↓
observed implementation evidence
↓
responsibility / authority / visibility / compatibility comparison
↓
classified mismatch, insufficient evidence, or bounded recommendation
```

The evidence does **not** support assuming that Seed can infer a program's true intent from an arbitrary codebase. It does support asking what the program **appears intended to do** when the purpose is grounded in observable implementation, public surfaces, tests, documentation with appropriate authority limits, or operator-provided scope.

## Transferable recovered methodology

### 1. Implementation evidence before architectural preference

Transferable and strongly implementation-backed.

The Architectural Recovery Methodology Characterization found that completed recoveries start from concrete implementation compression rather than desired taxonomy. Examples include operational execution, execution visibility, observation-derived capability, projection influence lineage, and read-model ownership. The same report identifies implementation authority first as an invariant: executable code, tests, event behavior, payload shape, and existing call order govern recovery.

For Program Review Evaluation, this transfers as:

```text
Do not begin with a preferred architecture.
Begin with observed implementation behavior and surfaces.
```

This directly supports evaluating an unfamiliar system's observed implementation before recommending changes. It does not support changing that system.

### 2. One bounded responsibility at a time

Transferable and strongly implementation-backed.

Completed responsibility recoveries repeatedly selected one compressed boundary at a time: execution recording versus post-execution knowledge extraction, state-build visibility versus projection-cache diagnostics, capability inventory versus executable operation contract metadata, projection lineage/replay/publication steps, and read-model construction/cache/publication steps.

For Program Review Evaluation, this transfers as:

```text
Evaluate one candidate responsibility mismatch at a time.
Do not turn review into broad redesign.
```

This is especially relevant for unfamiliar systems because repository evidence warns against broad abstraction from repeated vocabulary or surface similarity.

### 3. Fulfilled responsibility and upstream work

Transferable with bounds.

Responsibility / Authority Frontier Reconciliation found a recurring pattern where downstream work becomes eligible only after consuming explicit upstream evidence, identity, validation, assessment, construction result, durable record, payload, request, result, or compatibility handoff. Responsibility Recovery Evaluation Readiness and Slice Evaluation Readiness both use fulfilled upstream work as an evaluation criterion.

For Program Review Evaluation, this transfers as:

```text
Ask what work is already fulfilled by the unfamiliar program before proposing a new owner or fix.
```

This supports review questions such as whether a behavior is absent, already fulfilled elsewhere, duplicated, or compressed into an unsuitable boundary.

### 4. Concrete boundary-crossing artifacts

Transferable and strongly implementation-backed.

The recovered methodology repeatedly looks for artifacts crossing boundaries: completed events, payloads, request/result records, diagnostic rows, inventory rows, compatibility objects, cache lookup results, construction results, identity values, selected notes, queries, targets, domains, support records, and source facts.

For Program Review Evaluation, this transfers as:

```text
A review claim is stronger when it identifies the artifact that crosses between responsibilities.
```

Without such an artifact, the review should remain at insufficient evidence or require further observation rather than recommend implementation changes.

### 5. Authority boundaries

Transferable and strongly implementation-backed.

Across Inquiry Orientation, Question Surface Inventory, Source Navigation, Observation-Derived Capability, and the frontier reconciliation, Seed repeatedly separates evidence authority, operator prose, facts, recommendations, commands, mutation authority, semantic interpretation, ownership, and runtime truth. Inquiry Orientation is especially important because it explicitly does **not** promote notes into facts, goals, ownership, recommendations, commands, or next-safe-move authority.

For Program Review Evaluation, this transfers as:

```text
Treat docs, tests, code paths, runtime observations, operator statements, and recommendations as different authority sources.
Do not let one source silently become truth for another.
```

This directly supports classifying mismatches as authority mismatch rather than behavior mismatch when the issue is unsupported claim strength or wrong source authority.

### 6. Visibility sufficiency

Transferable with caution.

Execution Visibility and diagnostic-family work show that visibility is a distinct responsibility: status, timing, cache visibility, diagnostics, state-build visibility, projection-cache diagnostics, inventory registration, shape audit behavior, and record/ledger mutation boundaries can be owned separately from behavior. The repository instructions also require new diagnostic surfaces to be inventoried and shape-audited.

For Program Review Evaluation, this transfers as:

```text
A program may have correct behavior but insufficient visibility to evaluate or operate it safely.
```

However, visibility evidence is weaker than fulfilled-responsibility evidence for some families because visibility payloads can be sidecar diagnostic surfaces rather than prerequisites for downstream ownership.

### 7. Compatibility preservation

Transferable as an expectation, not a universal law.

Completed recoveries preserved event kinds, ordering, causation, correlation, result shapes, CLI/JSON shapes, diagnostic inventory behavior, shape-audit behavior, cache semantics, report accessors, answer surfaces, and rendering. Both readiness investigations treat compatibility preservation as part of evaluating proposed work.

For Program Review Evaluation, this transfers as:

```text
Before recommending changes, identify the compatibility surfaces that should remain stable.
```

The limit is important: Seed has not demonstrated compatibility-break evaluation. A program review should not claim that a compatibility break is justified from current recovered methodology alone.

### 8. Bounded recommendation and refusal conditions

Transferable and strongly implementation-backed.

Responsibility Recovery Evaluation Readiness and Slice Evaluation Readiness both support recommendations such as proceed, stop, or insufficient implementation evidence. Family completion audits preserve supported conclusions, unsupported conclusions, counterexamples, confidence, and natural stopping points. The Answer Composition family supports answer/reason/support/boundary/limitations composition before compatibility handoff.

For Program Review Evaluation, this transfers as:

```text
A review may recommend proceed, stop, classify mismatch, or state insufficient evidence.
The recommendation must carry support, boundary, and limitations.
```

This supports evidence-backed recommendations, not automatic fixes.

## Repository-specific assumptions

Several recovered concepts remain repository-specific or only partially transferable:

1. **Seed's exact responsibility families.** Operational Responsibility, Read-Model Ownership, Projection Influence Lineage, Answer Composition, Inquiry Lineage, Execution Visibility, and Observation-Derived Capability are implementation-backed in Seed. An unfamiliar program may not have these families or may express them differently.
2. **Question-family dispatch and inquiry identities.** `question_family`, `subject`, `target`, `domain`, `query`, note identity, and focus are Seed-local identities with different validation, routing, and authority boundaries. They do not become a universal program-review ontology.
3. **Diagnostic inventory and shape audit.** These are strong Seed operational visibility contracts. They transfer as a visibility principle, not as required infrastructure in another system unless that system has equivalent diagnostic surfaces.
4. **Compatibility surfaces.** Seed's event ledger, CLI/JSON outputs, cache snapshots, read-model payloads, and answer objects are repository-specific. The transferable question is "what compatibility surface exists here?" not "does it match Seed's surface?"
5. **Exact handoff mechanisms.** Seed uses events, dataclasses, request/result objects, private payloads, report accessors, diagnostic rows, inventory rows, source facts, and cache records. The recovered method supports looking for a concrete handoff, but not demanding one particular mechanism.
6. **Recovered completion criteria.** Family completion in Seed means no more same-family implementation-backed compression is visible. In an unfamiliar system, completion may be unassessable without more implementation evidence.

## Evaluation shape assessment

The proposed shape was:

```text
Program Purpose
↓
Expected responsibilities
↓
Observed implementation
↓
Recovered mismatches
↓
Evidence-backed recommendation
```

Implementation evidence supports a bounded version, not the unqualified version.

### Program Purpose

Partially supported.

Seed can preserve and compare purpose-like material when it is bounded by authority: operator prose stays operator prose; source navigation is source-fact matching, not runtime truth; question surfaces use exact provided identities and do not infer missing subject identity. Program Review Evaluation can therefore use purpose as a scoped input or observed claim, but current evidence does not support autonomous recovery of true program intent.

Supported phrasing:

```text
What does this program appear intended to do, according to bounded evidence?
```

Unsupported phrasing:

```text
What is this program truly intended to do, inferred automatically from code?
```

### Expected responsibilities

Supported when framed as candidate responsibilities.

Responsibility and slice readiness investigations support evaluating a human-framed candidate boundary against implementation compression, fulfilled upstream work, existing owners, crossing artifacts, excluded authority, compatibility, sufficiency, counterexamples, and stopping criteria. They do not support automatic generation of all expected responsibilities for an unfamiliar system.

### Observed implementation

Strongly supported.

The recovered methodology starts from implementation evidence and repeatedly rejects vocabulary, diagrams, output similarity, and boundary prose when not tied to executable behavior, tests, diagnostics, events, payloads, cache behavior, or compatibility-preserving handoffs. This is directly transferable to unfamiliar-system review.

### Recovered mismatches

Supported for bounded classifications.

Implementation evidence supports distinguishing at least these mismatch categories:

- **Behavior mismatch:** expected responsibility is not fulfilled by observed behavior, or fulfilled behavior differs from bounded evidence.
- **Visibility gap:** behavior may exist, but diagnostic/status/projection/reporting evidence is insufficient for evaluation or operation.
- **Authority mismatch:** a surface, note, document, projection, recommendation, or read-only output is treated as stronger authority than it owns.
- **Collapsed responsibility:** multiple responsibilities are behaviorally present but compressed into one owner or handoff point.
- **Insufficient implementation evidence:** observed evidence does not justify the claim, recommendation, or classification.

The collapsed-responsibility classification is supported only when concrete implementation compression is visible. Repeated conceptual overlap is not enough.

### Evidence-backed recommendation

Supported as bounded answer composition.

Answer Composition and both readiness investigations support recommendations with answer, reason, support, boundary, limitations, confidence, and refusal conditions. The supported recommendation is evaluative: proceed to bounded investigation, stop, classify mismatch, or insufficient evidence. It is not a command to modify code.

## Counterexamples and limits

The review found multiple implementation-backed reasons to avoid overclaiming Program Review Evaluation readiness:

- There is no implemented Program Review Evaluation surface, command, registry row, importer, or automated evaluator.
- `seed ask` style dispatch is exact-family dispatch, not natural-language program review or arbitrary repository routing.
- Inquiry Orientation performs deterministic lexical related-material matching and explicitly avoids semantic interpretation, intent recovery, ownership, recommendations, commands, or next-safe-move authority.
- Responsibility Recovery Evaluation and Slice Evaluation both require human-scoped candidates; neither supports autonomous candidate discovery from arbitrary prose.
- Family-local handoff mechanisms differ, so there is no universal review abstraction.
- Completed recoveries preserved compatibility; the repository has not demonstrated compatibility-break review.
- Evidence sufficiency and confidence are argued in human-written investigations and audits, not computed by implementation.
- Visibility surfaces can prove operational observability but do not always prove responsibility prerequisites.
- Seed's known families are not automatically the responsibility taxonomy of another software system.
- Documentation or presentation vocabulary is not automatically repository knowledge, and by extension not automatically program intent.

No reviewed completed recovery showed a valid recommendation that ignored implementation evidence, authority boundaries, compatibility preservation, or stopping criteria. That absence should not be overread as universal proof; it only shows that within the completed Seed recovery corpus, those constraints recur.

## Answers to the requested questions

### 1. Does the repository now contain enough recovered architecture to evaluate an unfamiliar software system before proposing implementation changes?

**Yes, boundedly.**

Seed contains enough recovered architecture to support a read-only Program Review Evaluation pattern when the unfamiliar system is reviewed through bounded evidence: scoped purpose claims, observable implementation, tests, public surfaces, documentation with calibrated authority, concrete handoffs, visibility surfaces, compatibility expectations, and explicit refusal conditions.

Seed does **not** contain enough evidence for autonomous unfamiliar-codebase understanding, implementation planning, debugging, code modification, repository import, automatic responsibility discovery, or automatic intent inference.

### 2. Which recurring implementation-backed concepts transfer directly?

The concepts that transfer most directly are:

- implementation evidence before architectural preference;
- one bounded responsibility at a time;
- fulfilled upstream work and downstream eligibility;
- concrete boundary-crossing artifacts;
- authority boundaries and negative ownership;
- visibility as distinct from behavior;
- compatibility surface preservation;
- evidence sufficiency and counterexample review;
- stop/proceed/insufficient-evidence recommendations;
- answer composition with support, boundary, limitations, and confidence.

### 3. Which concepts remain repository-specific?

Repository-specific concepts include Seed's exact responsibility-family names, question-family dispatch model, `subject`/`target`/`domain`/`query`/note/focus identity distinctions, diagnostic inventory and shape-audit machinery, event-ledger and cluster-mutation boundaries, read-model cache shapes, projection influence lineage details, and current answer compatibility objects.

These can guide review questions, but they should not be imposed as a universal architecture on an unfamiliar system.

### 4. Does implementation evidence support evaluating implementation against intended responsibilities?

**Yes, but only when intended responsibilities are bounded by evidence.**

The evidence supports evaluating observed implementation against human-scoped candidate responsibilities, public behavior claims, tests, documented contracts with calibrated authority, or explicit operator-provided purpose. It does not support inferring complete intended responsibilities automatically from arbitrary code or presentation vocabulary.

The safer supported question is:

```text
Given this bounded purpose evidence, what responsibilities appear necessary, what implementation evidence fulfills them, and where is evidence missing or mismatched?
```

### 5. Would recovered responsibility methodology naturally detect collapsed responsibilities during review?

**Yes, when collapse is implementation-visible; no, when collapse is only conceptual.**

The recovered methodology naturally looks for implementation compression and one-boundary recovery. That would detect collapsed responsibilities during review when multiple responsibilities are concretely compressed in one function, payload, report shape, event branch, cache path, builder, or compatibility object.

Implementation evidence does not support concluding that Seed can detect all collapsed responsibilities in an unfamiliar system. Detection still depends on human scoping, accessible implementation evidence, and a visible crossing or compression point. If the review cannot identify concrete compression, the correct conclusion is insufficient implementation evidence rather than collapsed responsibility.

## Supported conclusions

- Seed has enough recovered architecture to begin a bounded, read-only Program Review Evaluation inquiry as an investigation pattern.
- The strongest transferable method is implementation-first, one-boundary-at-a-time, authority-calibrated, compatibility-aware, and willing to stop.
- Program purpose can be evaluated only as bounded evidence or scoped operator/documented claim, not as automatically inferred truth.
- Expected responsibilities can be evaluated as candidate responsibilities, not automatically generated complete responsibility maps.
- Observed implementation, boundary-crossing artifacts, authority limits, visibility gaps, compatibility expectations, and evidence sufficiency are implementation-backed review dimensions.
- Collapsed responsibilities are review-detectable when implementation compression is concrete.
- Evidence-backed recommendations are supported as bounded answer composition, not as automatic code changes.

## Unsupported conclusions

- Seed already implements Program Review Evaluation.
- Seed can import or understand arbitrary repositories autonomously.
- Seed can infer true program intent automatically.
- Seed can generate a complete responsibility map for an unfamiliar system without human scoping.
- Seed can plan or modify unfamiliar code from this methodology.
- Seed can evaluate compatibility-breaking recommendations from current recovery evidence.
- Seed's responsibility-family taxonomy is universal.
- Visibility, authority, behavior, and responsibility mismatch can always be separated automatically.
- Conceptual similarity alone proves collapsed responsibility.

## Confidence

**High** confidence that Seed has recurring implementation-backed concepts useful for bounded program review: implementation evidence, responsibility boundaries, authority, visibility, compatibility, handoffs, sufficiency, counterexamples, and bounded recommendations.

**High** confidence that the review must remain read-only and human-scoped because the readiness investigations and inquiry surfaces explicitly reject semantic inference, planning, automation, and automatic ownership recovery.

**Medium** confidence that these concepts transfer cleanly to unfamiliar systems, because the method is evidence-first and boundary-oriented, but another system may lack equivalent tests, diagnostics, handoffs, or explicit authority surfaces.

**Low** confidence that Seed can evaluate an unfamiliar system without operator-provided scope, accessible implementation evidence, or documented/public behavior claims.

## Recommended next action

Begin only a bounded **Program Review Evaluation inquiry investigation** after this readiness report is accepted.

That next investigation should remain read-only and should define:

1. admissible inputs, such as a human-scoped program purpose claim, repository path, public behavior contract, test suite, or bounded subsystem;
2. evidence sources and their authority levels;
3. candidate responsibility framing rules;
4. mismatch categories and refusal conditions;
5. output shape with answer, reason, support, boundary, limitations, confidence, and recommendation;
6. explicit non-goals: no debugging, no code modification, no planning, no repository import automation, no compatibility-break approval, no ownership recovery.

Do not implement a program-review surface yet. If future work adds a CLI, diagnostic, audit, probe, view, or recordable output, it must follow the repository operational visibility contract: diagnostic inventory registration, shape-audit implementation specs, tests proving `seed --diagnostic-inventory`, tests proving `seed --diagnostic-shape-audit`, and record/ledger mutation boundary proofs where applicable.

## Acceptance answer

Before changing an unfamiliar program, Seed now knows enough to evaluate, in a bounded and evidence-first way, what the program appears intended to do, what candidate responsibilities appear necessary, what implementation evidence fulfills them, and whether pressure suggests a collapsed responsibility, visibility gap, authority mismatch, behavior mismatch, or insufficient implementation evidence.

The answer is not unconditional. Missing architecture before stronger claims includes:

- an implemented Program Review Evaluation surface;
- repository-native import or evidence-ingestion boundaries;
- tests for review outputs and refusal conditions;
- implementation evidence for automatic purpose or responsibility inference;
- implementation evidence for compatibility-break evaluation;
- demonstrated review of a novel unfamiliar system using only bounded evidence;
- a stable way to compute sufficiency and confidence rather than manually arguing them in reports.

Until those exist, Program Review Evaluation is supported as a bounded investigation pattern, not an automated capability.
