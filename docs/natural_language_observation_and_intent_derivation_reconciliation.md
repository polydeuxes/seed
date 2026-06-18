# Natural Language Observation And Intent Derivation Reconciliation

## Purpose

This document performs a documentation-only reconciliation of natural language,
language observations, interpretation, intent derivation, question derivation,
goal derivation, constraint derivation, command derivation, and claim extraction.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify projections, observations,
evidence handling, claims, recommendations, decisions, capabilities, execution
paths, authority boundaries, attribution boundaries, or tests.

It does not introduce new runtime semantics.

## Central Question

Seed increasingly separates claims, questions, goals, recommendations,
decisions, commands, attribution, explainability, and handoff alignment. The
remaining boundary question is:

```text
How does prose enter the architecture?
```

Operator language can be concise, ambiguous, imperative, speculative,
prohibitive, or goal-shaped:

```text
Check why nginx is down.
I think example_host is unhealthy.
Investigate storage usage.
Do not restart anything.
We should prioritize reliability over speed.
```

Humans naturally derive intent, questions, goals, constraints, entities,
relationships, priorities, and possible commands from such language. Seed should
be able to represent those derivations without treating language understanding
as truth, authority, verification, execution, or goal ownership.

## Central Finding

Natural language is an observation source. Interpretation transforms language
observations into inspectable candidate structures, especially language-derived
claims, intent hypotheses, question candidates, goal hypotheses, constraint
candidates, entity references, relationship hypotheses, priorities, and
command-like requests.

The resulting boundary is:

```text
language observation
  -> interpretation
  -> extracted or derived candidates
  -> support, clarification, corroboration, verification, recommendation, decision, or command boundaries
```

This is a conceptual decomposition, not a new runtime pipeline.

Interpretation may produce claims, but interpretation is not verification.
Language-derived claims may be supported by the language that produced them, but
that support is support for the claim that the speaker said, implied, requested,
or appeared to believe something. It is not, by itself, support that the external
world matches the statement. For example, `I think example_host is unhealthy` can
support a claim that the operator stated a concern about example_host health. It does
not verify example_host health.

The safest architecture treats language understanding as decomposable,
inspectable, and caveated:

```text
raw utterance
  -> explicit text spans
  -> source and attribution context
  -> interpretation method and confidence
  -> derived candidates
  -> unresolved ambiguity
  -> required support or clarification
```

LLMs may be one implementation technique for interpretation, but they are not
the center of the architecture. Rule-based parsers, forms, workflow labels,
command grammars, deterministic classifiers, transcript processors, human review,
and model-assisted extractors can all produce language interpretations if their
outputs preserve support, scope, attribution, and uncertainty.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/input_source_authority_reconciliation.md`
- `docs/input_act_vocabulary.md`
- `docs/input_inspection_reconciliation.md`
- `docs/claim_support_characterization.md`
- `docs/claim_support_design.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/explainability_contract_characterization.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/recommendation_selection_boundary.md`
- `docs/agency_and_attribution_reconciliation.md`
- `docs/handoff_template_and_continuation_protocol_reconciliation.md`

## Boundary Summary

| Concept | Definition | Primary output | Must not become |
| --- | --- | --- | --- |
| Language observation | Preserved natural-language input with source, time, scope, and attribution context. | Evidence that language was received. | Claim truth, authority, command execution, policy. |
| Interpretation | An explicit derivation from language observations into candidate meaning structures. | Extracted/derived candidates plus caveats. | Observation, verification, hidden truth, authority. |
| Claim extraction | Identification of claim-shaped assertions, beliefs, reports, or assumptions in language. | Language-derived claims. | Verification or corroboration. |
| Intent derivation | Identification of what the speaker appears to be trying to do. | Intent hypothesis or declared intent record. | Recommendation, decision, command, authority. |
| Question derivation | Conversion of concern or prose into answerable inquiries over Seed knowledge. | Question candidates. | Claim, recommendation, assumption. |
| Goal derivation | Identification of desired outcomes expressed or implied by language. | Declared goal or inferred goal hypothesis. | Goal ownership, policy, authority, decision. |
| Constraint derivation | Identification of restrictions on acceptable means, timing, scope, or providers. | Constraint candidate. | Policy source, authorization, command. |
| Command derivation | Identification of command-like language or requested bounded operations. | Command candidate or command-intent candidate. | Actual command record, decision, action. |

## 1. Language Observations

A language observation is a preserved natural-language artifact received by Seed
or an adjacent interface, together with its source, time, channel, attribution,
scope, and confidence metadata when available.

Examples include:

```text
operator typed: Check why nginx is down.
operator typed: Do not restart anything.
voice transcript: investigate storage usage
uploaded incident note: example_host looked unhealthy at 02:10Z
chat handoff: reliability matters more than speed for this task
```

Operator language is therefore an observation source. It observes that language
was provided in a particular context. It does not directly observe the external
condition described by the language.

### How language differs from other observation families

Language observations differ from telemetry, inventory, repository, and event
observations by the kind of reality they directly report:

| Observation family | Directly observes | Typical support boundary |
| --- | --- | --- |
| Language observation | A speaker, document, transcript, or interface supplied words. | Supports claims about stated beliefs, requests, concerns, constraints, or instructions. |
| Telemetry observation | Measured runtime signals such as availability, latency, counters, or utilization. | Supports operational state claims. |
| Inventory observation | Discovered entities, packages, hosts, ports, users, or resources. | Supports existence, configuration, and topology claims. |
| Repository observation | Files, code, documentation, history, or static structure. | Supports implementation, documentation, and ownership claims. |
| Event observation | A recorded occurrence in an event stream or ledger. | Supports temporal, causation, and state-transition claims. |

The distinction is not that language is weaker. The distinction is that language
observes a communicative act. It may be highly authoritative about what the
speaker requested or forbade, while remaining weak or irrelevant as direct
support for what is true in the environment.

## 2. Interpretation

Interpretation is the explicit derivation of candidate meaning from one or more
language observations.

Interpretation may identify:

- explicit assertions;
- presuppositions;
- implied concerns;
- candidate entities;
- candidate relationships;
- question candidates;
- intent hypotheses;
- goal hypotheses;
- constraints;
- priorities;
- command-like requests;
- ambiguity and missing information.

Interpretation is not the original observation. The raw utterance `Check why
nginx is down` is a language observation. The candidate interpretation
`operator wants an investigation into nginx unavailability` is derived from it.

Interpretation is also not evidence in the same sense as the raw language. The
raw language is evidence that the utterance occurred. The interpretation is a
claim-producing derivation over that evidence. It should carry support back to
text spans, source metadata, method, confidence, and unresolved ambiguity.

Interpretation is not assessment by default. Assessment interprets preserved
knowledge under a scoped evaluative frame such as risk, condition, sufficiency,
or impact. Language interpretation may produce an assessment candidate such as
`the operator appears to regard reliability as higher priority than speed`, but
that candidate still requires attribution and caveats.

## 3. Claim Extraction

Claim extraction identifies claim-shaped content in language. A language-derived
claim is a claim whose immediate support includes language observations and the
interpretation that extracted the claim.

Examples:

| Language | Possible extracted claim | Safer framing |
| --- | --- | --- |
| `nginx is down` | `nginx is down` | Speaker asserted nginx is down; operational verification remains separate. |
| `I think example_host is unhealthy` | `example_host is unhealthy` | Speaker expressed belief or concern that example_host is unhealthy. |
| `storage utilization is high` | `storage utilization high` | Speaker asserted or reported high storage utilization. |
| `the deployment probably caused this` | `deployment caused incident` | Speaker hypothesized causation; causality remains unverified. |

Language-derived claims differ from observed, verified, and corroborated claims:

| Claim status | Meaning |
| --- | --- |
| Language-derived claim | Extracted from language and supported by language observation plus interpretation. |
| Observed claim | Supported by non-language observations or facts produced from observation paths. |
| Verified claim | Checked by an appropriate verification path under known scope and freshness. |
| Corroborated claim | Supported by multiple independent or complementary sources. |

A single claim may have multiple support relationships. For example,
`example_host unhealthy` may begin as language-derived, later receive telemetry
support, and eventually become corroborated. Those transitions should remain
visible rather than overwriting the original language-derived origin.

## 4. Intent Derivation

Intent derivation identifies what the speaker appears to be trying to do through
the utterance.

Examples:

```text
Check why nginx is down.        -> investigate / explain
Compare these two incidents.    -> compare
Can we repair this safely?      -> evaluate remediation
Restart nginx.                  -> request command-like execution
```

Intent derivation differs from recommendation, decision, command, and execution:

- An intent hypothesis says what the operator appears to want to accomplish.
- A recommendation suggests a possible response.
- A decision selects, rejects, defers, or escalates an option.
- A command requests bounded execution through an execution path.
- An action is the attempted or actual mutation.

Intent derivation is not authority. `Restart nginx` may reveal an execution
intent, but it does not prove that the speaker is authorized, that policy allows
the restart, that a decision record exists, or that a command has been issued.

Intent should preserve attribution:

```text
who or what supplied the language
whether the intent was declared or inferred
which text span supports the derivation
what ambiguity remains
whether clarification is required before material use
```

## 5. Question Derivation

Question derivation converts language into answerable inquiries over Seed
knowledge, support, provenance, interpretation, option space, or gaps.

Examples:

| Language | Possible derived question |
| --- | --- |
| `Check why nginx is down.` | Why is nginx unavailable, if it is unavailable? |
| `I think example_host is unhealthy.` | What evidence supports or conflicts with example_host being unhealthy? |
| `Investigate storage usage.` | Which storage resources have notable utilization, change, or risk? |
| `Do not restart anything.` | What read-only diagnostic paths are available? |

Questions emerge from language because prose often contains concern before it
contains a precise query. The question form is safer than silently assuming the
truth of the prose. `Why is nginx down?` can preserve the presupposition as a
candidate claim while asking a safer question: `Is nginx down, and if so, what
supports the explanation?`

Questions remain distinct from intent. The same question can serve different
intents, and the same intent can generate multiple questions. Questions ask what
knowledge is needed; intent explains why the operator is engaging Seed.

## 6. Goal Derivation

Goal derivation identifies desired outcomes expressed or implied by language.

Examples:

```text
keep service available
reduce risk
improve reliability
minimize downtime
prioritize reliability over speed
```

Goals may be declared directly:

```text
We should prioritize reliability over speed.
```

or inferred from task language:

```text
Check why nginx is down.
```

which may imply a possible goal such as `restore or preserve service
availability`. Inferred goals remain hypotheses unless the operator, workflow,
or governance context explicitly owns them. Seed may reason about inferred goals,
but it should not silently convert them into operator-owned objectives.

When an inferred goal materially affects recommendations, decisions, command
selection, prioritization, or refusal, Seed should either expose the assumption
or ask a clarification question. Goal derivation is especially dangerous when a
common operational default hides a different operator priority, such as cost,
safety, compliance, forensics, or avoiding downtime.

## 7. Constraint Derivation

Constraint derivation identifies restrictions on acceptable means, timing,
scope, providers, resources, risk, or side effects.

Examples:

```text
do not restart services
avoid downtime
use local providers only
read-only investigation
no network calls
only inspect example_host
wait for approval before changing anything
```

Constraints differ from goals, policy, authority, and commands:

| Concept | Difference from constraint |
| --- | --- |
| Goal | Desired outcome; a constraint limits acceptable ways to pursue outcomes. |
| Policy | Governance rule from an authoritative policy source; a derived constraint may reflect operator instruction but is not the whole policy system. |
| Authority | Permission for a transition; a constraint can forbid or require approval without proving who has authority. |
| Command | Execution request; a constraint bounds or prohibits commands but is not itself execution. |

`Do not restart anything` may be a strong operator-stated constraint for the
current interaction. It still should not be treated as a complete policy model,
identity proof, or authority system. Conversely, a policy may prohibit restarts
even if the operator language omits that constraint.

## 8. Command Derivation

Command derivation identifies language that resembles or requests a bounded
operation.

Examples:

```text
restart nginx
collect logs
inspect filesystem
run diagnostics
open the incident document
```

Command-like language differs from intent, recommendation, decision, and actual
command records:

| Concept | Meaning |
| --- | --- |
| Command-like language | Words that appear to request an operation. |
| Intent | The apparent purpose behind the utterance. |
| Recommendation | Advice that an operation could be considered. |
| Decision | Authorized selection, deferral, rejection, or escalation of an option. |
| Command record | Bounded execution request recognized by the command/execution architecture. |
| Action | The attempted or completed effect. |

`Restart nginx` can be interpreted as command-like language. It should not be
reported as a command record unless the architecture has actually produced such
a record through the required decision, validation, policy, authority, and
capability boundaries. It should not be reported as an action unless execution
actually occurred.

## 9. Evidence And Support For Language-Derived Claims

Language-derived claims should be supportable and inspectable. Their immediate
support should preserve:

- raw text or transcript reference;
- exact or approximate text span;
- source and attribution context;
- time and interaction scope;
- channel or document origin when known;
- interpretation method;
- confidence or ambiguity markers;
- distinction between explicit, implied, inferred, and ambiguous content.

### Explicit language

Explicit language is directly present in the utterance:

```text
Do not restart anything.
```

It can strongly support a claim that the speaker prohibited restarts in the
current context, subject to attribution and authority boundaries.

### Implied language

Implied language follows from ordinary linguistic structure but is not stated as
a standalone assertion:

```text
Check why nginx is down.
```

This implies concern about nginx and presupposes possible unavailability. The
presupposition should be marked as presupposed or assumed, not verified.

### Inferred language

Inferred language depends on context, domain knowledge, workflow state, or
interpretive judgment:

```text
Investigate storage usage.
```

This may imply a goal of reducing storage risk, but that goal remains a
hypothesis unless confirmed or made explicit by workflow context.

### Ambiguous language

Ambiguous language admits multiple reasonable interpretations:

```text
Use local providers only.
```

This might mean local LLM providers, local cloud region, local filesystem, local
team, or local network. Ambiguity should produce a caveat or question rather
than a hidden assumption when material.

## 10. What Should Not Be Collapsed Together

The following distinctions should remain visible:

| Distinction | Why it matters |
| --- | --- |
| Language observation != claim | Receiving words is not the same as preserving the world-state assertion contained in them. |
| Claim extraction != verification | Extracting `nginx is down` from prose does not verify nginx availability. |
| Intent derivation != goal ownership | Inferring `investigate` does not prove the operator owns every implied goal. |
| Goal derivation != authority | A desired outcome does not authorize decisions, commands, or side effects. |
| Constraint derivation != policy | Operator-stated constraints may matter, but policy has separate governance authority. |
| Question derivation != recommendation | Asking what to know does not advise what to do. |
| Recommendation != command | Advice is not an execution request. |
| Interpretation != truth | Plausible meaning is not environmental fact. |
| Language understanding != knowledge | Understanding prose produces candidate structures that still require support, provenance, and boundaries. |
| Command-like language != command record | An uttered imperative is not the same as a validated execution request. |
| Command record != action | Requesting execution is not the same as executing or observing effects. |

These distinctions matter because natural language compresses many architectural
layers into one sentence. Seed's architecture is safer when it decompresses the
sentence into inspectable pieces rather than allowing fluent prose to bypass
support, attribution, authority, policy, recommendation, decision, command, or
action boundaries.

## Required Findings

This audit supports the following findings:

1. Natural language is an observation source.
2. Language observations observe communicative acts, not external world truth by themselves.
3. Interpretation produces derived candidates, including claims.
4. Language-derived claims remain supportable and inspectable.
5. Interpretation is not verification.
6. Intent derivation is not authority.
7. Goal derivation may remain hypothetical.
8. Constraint derivation is distinct from policy.
9. Questions are safer than assumptions when language contains presupposition, ambiguity, or material inference.
10. Interpretation should remain explainable.
11. Language understanding should remain decomposable.
12. LLMs are not required to be the center of language interpretation.

## Support Requirements

Any future representation of language-derived meaning should preserve enough
support to answer:

1. What language was observed?
2. Who or what supplied it, to the extent known?
3. Through what channel, document, workflow, session, or handoff did it arrive?
4. What exact text span supports the derivation?
5. Was the content explicit, implied, inferred, or ambiguous?
6. What interpretation method produced the candidate?
7. What confidence, caveat, or ambiguity applies?
8. What claim, intent, question, goal, constraint, or command-like candidate was produced?
9. What non-language support exists, if any?
10. What boundary must be crossed before assessment, recommendation, decision, command, or action?

## Non-Goals

This reconciliation does not require or recommend immediate implementation of:

- new language observation schemas;
- new interpretation schemas;
- new claim extraction records;
- new intent, question, goal, constraint, or command-derivation records;
- new LLM integrations;
- new parsers or classifiers;
- new projection behavior;
- new evidence handling;
- new attribution behavior;
- new authority behavior;
- new policy behavior;
- new recommendation, decision, command, or action behavior;
- new runtime routes;
- new tests.

It also does not define a natural-language parser, dialogue manager, prompt
protocol, semantic grammar, ontology expansion, authorization system, policy
language, planning engine, remediation engine, or autonomous agent loop.

## Implementation Implications

The findings imply documentation-level guardrails for future work:

1. Preserve raw language separately from derived meaning.
2. Preserve attribution and source context separately from authority.
3. Mark whether derived content is explicit, implied, inferred, or ambiguous.
4. Treat language-derived claims as claims requiring support, not as verified facts.
5. Prefer derived questions over hidden assumptions when presuppositions are material.
6. Preserve declared goals separately from inferred goal hypotheses.
7. Preserve operator-stated constraints without treating them as the entire policy model.
8. Preserve command-like language separately from actual command records.
9. Require the established recommendation, decision, command, capability, and action boundaries before mutation.
10. Make interpretation explainable through text spans, method, confidence, caveats, and unresolved ambiguity.

These implications are not implementation instructions for this change. They are
architectural constraints for preserving conceptual boundaries if future designs
introduce explicit language-observation or interpretation representations.

## Architectural Invariants

This reconciliation supports the following invariants:

1. Language is an observation source.
2. Language observations preserve communicative acts.
3. Language observations do not make external-world claims true by themselves.
4. Interpretation produces claims and other derived candidates.
5. Interpretation is not verification.
6. Interpretation is not authority.
7. Language-derived claims require support.
8. Support for a language-derived claim should be inspectable.
9. Explicit, implied, inferred, and ambiguous language should remain distinguishable.
10. Questions bridge intent and knowledge.
11. Questions remain distinct from intent.
12. Questions are safer than assumptions when language is ambiguous or presuppositional.
13. Goals remain operator-owned.
14. Inferred goals remain hypotheses unless confirmed or otherwise owned.
15. Goal derivation does not create authority.
16. Constraint derivation is distinct from policy.
17. Intent derivation is distinct from recommendation, decision, command, and execution.
18. Command-like language is distinct from command records.
19. Recommendations are advisory and do not become commands.
20. Decisions select; commands request; actions mutate.
21. Language understanding should remain decomposable.
22. LLM interpretation is optional implementation machinery, not architectural authority.

## Conclusion

Prose enters Seed as observation: words supplied by an operator, document,
transcript, handoff, automation, or interface. Interpretation may derive claims,
intents, questions, goals, constraints, priorities, relationships, and
command-like candidates from that observation, but each derived object must
preserve support and boundary context.

The architectural task is not to make language authoritative. It is to make
language-derived meaning inspectable enough that Seed can ask safer questions,
preserve claims honestly, explain assumptions, respect constraints, and avoid
turning fluent prose into unverified truth or unauthorized action.
