# Operator Clarification vs Competency Gap Assessment Audit

## Executive answer

**Short answer:** the repository only partially distinguishes **Operator Clarification** from **Competency Gap Assessment**.

Current runtime behavior clearly supports **operator clarification as an immediate inquiry outcome**: a model decision may be `ask_question`, validation requires a `question`, the runtime records `response.question`, and then returns a `RuntimeResponse(kind="question")`. There is no implemented continuation in that route that evaluates why the external answer was needed.

The repository also supports a broader **responsibility-evaluation / competency-evaluation discipline** that can ask whether evidence was sufficient, contradicted, incomplete, invisible, or unsupported. That discipline can produce bounded conclusions and stop. However, current implementation evidence does **not** show a stable runtime boundary specifically named or invoked as "competency gap assessment after operator clarification."

Therefore, **Model A is more strongly supported for runtime operator clarification**:

```text
Operator clarification
↓
Inquiry complete / response.question emitted
↓
Stop
```

**Model B is supported only as an audit/investigation posture, not as an implemented recurring runtime transition**:

```text
Operator clarification
↓
Inquiry complete
↓
Competency assessment
↓
Explicit stop or future pressure
```

The audit can recognize a candidate distinction:

```text
Question answered
!=
Why couldn't I answer?
```

but repository evidence is insufficient to claim it as a stable implemented boundary for every operator clarification.

## Implementation evidence reviewed

### Runtime operator input and clarification behavior

The runtime records every incoming user message as `input.user_message`, projects state, composes decision input, asks the decision producer for exactly one structured decision, validates it, and routes it. This establishes operator interaction as event-backed runtime input, not as a separate reflective loop.

Relevant implementation evidence:

- `Runtime.__seed_arch__` lists routed response events including `response.question`, alongside `response.answer` and `response.refusal`.
- `DecisionKind` includes `ask_question` as one decision kind among runtime outcomes.
- `DecisionValidator.validate(...)` requires `ask_question` decisions to contain a concrete `question`.
- `Runtime._route(...)` handles `ask_question` by appending `response.question` and returning `RuntimeResponse(kind="question", message=...)`.
- Tests assert `ask_question` routes to a `question` response.

This supports **operator clarification as a terminal runtime response for that turn**. It does not show a second runtime pass that evaluates why clarification was required.

### Bounded question and answer surfaces

The app's bounded question inventory exposes exact question-family routing and authority boundaries. Running:

```bash
python scripts/seed_local.py ask --question-families --json
```

showed current question families such as `operational pressure`, `current operational explanation`, `derivation explanation`, `selection explanation`, `knowledge reachability`, `surface inventory`, `surface shape validation`, `source definition/import lookup`, and `inquiry orientation`.

These rows demonstrate that Seed distinguishes bounded operator-facing answers by exact surface and authority boundary. Representative inventory output says:

- `derivation explanation` answers with an evidence-backed derivation path and is read-only.
- `selection explanation` answers with candidates, factors, alternatives, and outcome and is read-only.
- `inquiry orientation` is a read-only orientation view over an inquiry note and projected state, with no routing or execution.

This supports a repository pattern of **bounded answers**, but not an automatic post-clarification competency assessment.

### Diagnostic inventory and shape audit

Running:

```bash
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
```

confirmed that current diagnostic surfaces are inventory-backed and shape-audited. The repository's operational visibility contract also requires new diagnostic/audit/probe/view surfaces to be registered and shape-audited.

Because no new implementation surface was added here, no diagnostic registry updates were required. More importantly for this audit, the absence of a registered operator-clarification competency-assessment surface is evidence against claiming a stable implemented boundary.

### Competency roadmap and responsibility evaluation discipline

The competency roadmap supports a conservative chain:

```text
Target Orientation
→ Evidence Visibility
→ Surface/Question Routing
→ Authority Interpretation
→ Bounded Responsibility Understanding
→ Responsibility Evaluation
→ Bounded Answer Explanation
→ Repository-Neutral Review Readiness
```

The roadmap explicitly separates:

- preserving an operator-supplied target/question from inferring operator intent;
- routing exact question families from semantic free-form routing;
- authority interpretation from mutation or promotion;
- responsibility evaluation from planning or autonomous review;
- bounded answer explanation from creating new truth.

The most relevant row is **Responsibility Evaluation**, whose bounded question is whether a claimed bounded responsibility is supported, contradicted, incomplete, or insufficiently visible. It consumes observed implementation evidence, counterexamples, authority boundaries, missing visibility, proceed/stop conditions, and confidence. Its stop criteria include semantic reasoning, hidden intent, unsupported tooling, and treating missing evidence as failure.

This is strong evidence for **competency-style assessment as investigation discipline**. It is not strong evidence for an implemented runtime transition after every operator clarification.

### Roadmap, pressure, investigation, and completion audit behavior

`roadmap_responsibility_characterization.md` distinguishes several relevant artifact families:

- **Investigation** answers a bounded question using evidence and can produce findings, supported/unsupported conclusions, next pressure, or stop.
- **Implementation Audit** checks current behavior, shape, or conformance and can produce pass/fail findings, visibility gaps, and conformance evidence.
- **Gap Analysis** identifies missing evidence, missing behavior, or missing representation and can produce named gaps and non-gaps.
- **Completion Audit** determines whether a family is complete, stopped, or reassigned.
- **Pressure** preserves friction or unresolved force but is signal authority, not automatic truth or priority.
- **Inquiry** bounds and conducts evidence-seeking work and retires when answered, reframed, or escalated.

This supports the idea that a second bounded activity may occur after an inquiry, but only if evidence warrants it. It also supports **no gap** as a legitimate result because gap analysis can produce non-gaps, completion audits can stop, and pressure retires when explained, resolved, decomposed, or unsupported.

## Current implementation behavior

### What happens when Seed asks a question

Current runtime behavior is:

```text
input.user_message
↓
model.decision.proposed(kind="ask_question")
↓
DecisionValidator validates question field
↓
response.question event appended
↓
RuntimeResponse(kind="question") returned
↓
runtime route ends
```

No inspected code path appends a follow-up event such as:

```text
competency_gap.assessed
inquiry_competency.reviewed
operator_clarification.evaluated
future_pressure.created
```

No test asserts that an operator clarification response causes pressure generation, roadmap generation, competency reflection, or a completion audit.

### What happens when a tool/capability gap is detected

The runtime does have a separate `request_tool` route. A `request_tool` decision creates a `ToolNeed`, projects it into open state, and returns a tool-need response. This is explicit gap recording, but it is not tied to `ask_question`. It is a different decision kind with different outputs.

This is an important counterexample to overgeneralization: the repository already has a way to represent some missing capability, and it does so through `request_tool`, not by treating every operator clarification as missing architecture.

### What bounded inquiry and audit artifacts can do

The document corpus supports follow-up audits and investigations. Those artifacts can ask why a question was not answerable internally, compare evidence, find unsupported conclusions, identify missing visibility, or explicitly stop. But that is a **human/investigation workflow**, not an automatic runtime continuation.

## Boundary analysis

### Operator Clarification

Repository-supported shape:

- Input: current user message, projected state, decision input, model decision.
- Decision: `ask_question`.
- Validation: question text must be present.
- Output: `response.question` event and `RuntimeResponse(kind="question")`.
- Authority: asks operator for missing immediate information; does not mutate cluster; does not by itself create a tool need, roadmap item, pressure item, or architectural finding.

Supported conclusion: **Operator Clarification is an immediate interaction boundary.**

Unsupported conclusion: **Operator Clarification owns competency assessment.** No inspected runtime code or registry row supports that.

### Competency Gap Assessment

Repository-supported shape, at the audit/investigation level:

- Input: claimed responsibility or expected boundary, implementation evidence, counterexamples, visibility gaps, authority constraints, proceed/stop criteria, confidence.
- Output: supported/unsupported/insufficient findings, named gaps or non-gaps, boundary notes, possible pressure, or explicit stop.
- Authority: evidence characterization; not planning, learning, self-improvement, autonomous architecture evolution, or automatic work selection.

Supported conclusion: **Competency-style assessment exists as responsibility evaluation / gap-analysis / implementation-audit discipline.**

Unsupported conclusion: **A stable implemented post-operator-clarification competency-assessment boundary exists.** Current evidence does not show this as a runtime route, diagnostic surface, event, schema, or test-backed transition.

### Immediate Inquiry Completion vs Inquiry Competency Reflection

The repository does distinguish the *ideas* through existing artifact families:

- inquiry can retire when answered, reframed, or escalated;
- investigation and implementation audit can inspect why a boundary failed or remained unsupported;
- gap analysis can identify gaps and non-gaps;
- pressure can retire when explained or unsupported.

But the repository does not prove that this distinction is a stable, recurring implementation boundary specifically following operator clarification.

## Comparative analysis

### Model A

```text
Operator clarification
↓
Inquiry complete
↓
Stop
```

**Stronger implementation support.** Runtime code routes `ask_question` directly to `response.question` and returns. Tests cover the route as a question response. No automatic subsequent activity appears in that path.

### Model B

```text
Operator clarification
↓
Inquiry complete
↓
Competency assessment
↓
Explicit stop
or
Future pressure
```

**Supported as a possible audit/investigation workflow, not as current runtime behavior.** Responsibility evaluation, implementation audits, gap analysis, completion audits, and pressure characterization provide the vocabulary and discipline for the second activity. But no inspected implementation binds that activity to every or any operator clarification response.

### Determination

Model A is the current runtime model. Model B is a repository-supported investigative posture that may be manually applied when evidence warrants it. Current evidence is insufficient to promote Model B into a stable implemented boundary.

## Counterexamples searched

### Counterexample: operator clarification always creates future work

Not supported. The runtime `ask_question` route emits `response.question` and returns a question response. It does not create a tool need, roadmap row, pressure record, action plan, or state patch.

### Counterexample: operator clarification never being examined after completion

Too strong. The repository contains investigation, implementation-audit, gap-analysis, completion-audit, roadmap, and pressure artifacts that can examine completed inquiries and missing evidence. This means post-completion examination is repository-supported as a documentation/audit activity. It is just not automatic or specific to operator clarification.

### Counterexample: competency reflection already owned by another recurring responsibility

Partially supported. The strongest existing owner is **Responsibility Evaluation** as a competency/investigation discipline. Related ownership also appears in **Gap Analysis**, **Implementation Audit**, **Completion Audit**, and **Pressure** artifact families. However, none of these currently owns a specific post-clarification runtime transition.

### Counterexample: every operator clarification implies missing architecture

Rejected. `ask_question` is a valid decision kind independent from `request_tool`. Capability gaps are represented separately through `request_tool` and `ToolNeed`; pressure and roadmap artifacts are not automatic truth or priority. Therefore operator clarification can be appropriate external authority rather than evidence of missing architecture.

## Supported conclusions

1. **The repository distinguishes operator clarification from capability/tool gap recording.** `ask_question` and `request_tool` are separate decision kinds with separate validation and routing outcomes.

2. **The runtime treats operator clarification as a terminal response for the current turn.** The `ask_question` branch appends `response.question` and returns `RuntimeResponse(kind="question")`.

3. **The repository supports bounded evaluation of why evidence was insufficient.** Responsibility Evaluation, Gap Analysis, Implementation Audit, Completion Audit, and Pressure artifacts can inspect support, contradiction, missing visibility, non-gaps, and stopping.

4. **Competency assessment can legitimately stop without future work.** Roadmap characterization allows gap analysis to produce non-gaps, completion audits to stop, and pressure to retire when explained/resolved/unsupported. The competency roadmap also forbids treating missing visibility as failure.

5. **Not every operator clarification implies missing architecture.** Clarification may reflect appropriate operator authority, exact target orientation, or an unavailable external fact rather than repository deficiency.

6. **Current evidence supports a candidate conceptual boundary, not a stable implemented boundary.** The second activity exists as audit discipline, not as a registered runtime/diagnostic surface tied to `response.question`.

## Unsupported conclusions

1. **Unsupported:** every operator clarification should create architectural pressure.

2. **Unsupported:** the runtime currently performs competency gap assessment after asking a question.

3. **Unsupported:** operator responses are automatically converted into repository facts, goals, requirements, ownership, or future work.

4. **Unsupported:** a learning engine, planner, self-improvement subsystem, continuous optimization loop, or automatic architecture-evolution mechanism exists or is warranted.

5. **Unsupported:** "Operator Clarification != Competency Gap Assessment" is fully implemented as a stable recurring boundary. It is partially recoverable as a distinction between runtime clarification and audit/evaluation discipline, but implementation evidence is insufficient for a stronger claim.

## Direct answers to the recovery questions

### 1. Does the repository distinguish Operator Clarification != Competency Gap Assessment?

**Partially.** Runtime code distinguishes operator clarification from tool/capability gap recording, and investigation discipline distinguishes bounded answer completion from evaluation/gap analysis. But there is no stable implemented boundary named or invoked as competency assessment after operator clarification.

### 2. Does inquiry naturally terminate after operator clarification?

**For the runtime turn, yes.** The `ask_question` branch records `response.question` and returns a question response. No automatic continuation was found.

### 3. Does repository evidence support a second bounded reflection activity?

**Yes as audit/investigation discipline; no as automatic runtime behavior.** Responsibility Evaluation, Implementation Audit, Gap Analysis, Completion Audit, and Pressure artifacts support second-order examination when evidence warrants it.

### 4. What recurring evidence triggers competency assessment?

Supported triggers are not "operator clarification" by itself. Recurring triggers include:

- claimed responsibility needing support/contradiction/incomplete/insufficient classification;
- missing visibility or unsupported evidence;
- boundary-crossing pressure after completion;
- counterexamples;
- compatibility or authority-boundary questions;
- explicit implementation audit questions.

### 5. Can competency assessment legitimately conclude `No gap`?

**Yes.** Gap Analysis can produce non-gaps; Completion Audit can stop; Pressure can retire when explained, resolved, decomposed, or unsupported; Responsibility Evaluation forbids treating missing visibility as failure.

### 6. Does every operator clarification imply missing architecture?

**No.** Operator clarification is a valid runtime outcome. Missing capability has a separate `request_tool` / `ToolNeed` path. Operator authority can be appropriate without architectural deficiency.

### 7. Is there sufficient implementation evidence to recognize this as a stable boundary?

**Insufficient implementation evidence.** The repository supports the conceptual distinction and the audit discipline, but not a stable implemented post-clarification boundary.

## Confidence

**Medium-high for current runtime behavior.** The `ask_question` code path and tests are direct implementation evidence.

**Medium for audit/investigation discipline.** The roadmap and artifact-family characterizations consistently support bounded evaluation, non-gaps, pressure retirement, and explicit stopping.

**Low for claiming a stable post-clarification competency-assessment boundary.** No event type, CLI surface, diagnostic inventory row, shape-audit spec, schema, or test establishes that boundary.

