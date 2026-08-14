# Constitutional / Physiological / Behavioral Architecture

## Architectural motivation

Recent architectural reasoning suggests that the organism becomes cleaner when three explanatory layers remain distinct:

```text
Constitution
↓
Physiology
↓
Behavior
```

The constitution should establish lawful facts and boundary conditions. It should not command visible actions. If it says `Become curious`, it has already crossed from law into behavior. A cleaner constitution would instead establish a lawful condition such as:

```text
Authenticated operator communication exists.
```

From that fact, the organism's physiology may naturally become receptive, question-forming, evidence-seeking, attachment-aware, and willing to stop when lawful continuation is not available. Observable behavior then appears as the consequence of those physiological tendencies rather than as constitutionally scripted output.

The design question is therefore not how the current implementation behaves. The question is whether the organism is more coherent when lawful fact, natural response, and visible act are separated.

This characterization concludes that the separation is architecturally useful, provided each layer has strict boundaries:

- the constitution establishes what is lawfully true or lawfully possible;
- physiology determines how the organism is naturally disposed to respond to those lawful conditions;
- behavior is the observable result of physiology meeting a concrete situation.

The organism should feel grown rather than programmed: facts establish a world, physiology adapts to that world, and behavior becomes the visible trace of that adaptation.

## Proposed separation

### Constitution

The constitution is the layer of lawful givens. It establishes facts, permissions, prohibitions, identities, boundaries, and invariants that hold before any particular response is chosen.

It answers questions such as:

- What entities or relations lawfully exist?
- What conditions are recognized as valid?
- What must remain invariant across situations?
- What boundaries cannot be violated?
- What facts constrain any subsequent response?

It should not answer:

- What should the organism visibly do next?
- Which question should be asked?
- Whether to continue this particular inquiry?
- What clarification text should be produced?
- Which candidate should be selected?

A constitutional statement should be phrased as a lawful fact, not as an instruction to act.

Clean constitutional examples:

```text
Authenticated operator communication exists.
An observation may be opaque at intake.
Evidence may be insufficient for commitment.
A distinction exists between established fact and candidate interpretation.
Diagnostic-only findings do not silently become organism truth.
A lawful stop condition may exist.
```

Constitutional anti-examples:

```text
Ask the operator.
Continue inquiry.
Become curious.
Preserve this exact intake.
Generate candidate attachments.
Stop now.
```

Those anti-examples may be lawful behaviors or physiological consequences, but they are not constitutional facts.

### Physiology

Physiology is the organism's natural response structure. It is not a list of visible commands. It is the layer that converts lawful conditions into tendencies, pressures, capacities, and regulatory mechanisms.

It answers questions such as:

- Given a lawful fact, what kind of response becomes natural?
- Given uncertainty, how does the organism regulate commitment?
- Given opaque intake, how does the organism remain receptive without premature reduction?
- Given possible relevance, how does the organism form candidate questions or attachments?
- Given insufficient evidence, how does the organism withhold, discard, clarify, or stop?

Physiology is where curiosity can live. Curiosity need not be constitutionally commanded if the constitution establishes a lawful condition such as authenticated communication or admissible observation. Once an authenticated operator communication exists, the organism can naturally orient toward understanding it. That orientation is physiological: a tendency to preserve, attend, compare, form candidates, gate by evidence, and remain clarification-ready.

Physiological examples:

```text
receptivity to authenticated communication
opaque-intake preservation pressure
candidate-question formation
candidate-attachment formation
evidence gating
uncertainty regulation
clarification readiness
commitment inhibition under insufficient evidence
honest stopping pressure
```

Physiological anti-examples:

```text
The constitution says to ask.
The behavior must be: "Can you clarify?"
Always continue inquiry after an operator message.
Never stop while candidate questions remain.
```

Those anti-examples either push behavior upward into physiology or push physiology upward into constitution.

### Behavior

Behavior is the visible consequence of physiological response under constitutional constraint. It is what an observer can see, receive, or record.

It answers questions such as:

- What did the organism visibly do?
- What did it ask?
- What did it preserve?
- What did it discard?
- What did it produce?
- Did it stop, continue, clarify, or commit?

Behavioral examples:

```text
Ask operator.
Continue inquiry.
Stop.
Discard candidate.
Produce clarification.
Preserve opaque intake in an output record.
State that evidence is insufficient.
Decline to promote a candidate into fact.
```

Behavior is not arbitrary. It remains constrained by constitution and generated through physiology. But behavior should not be prescribed directly by the constitution. It should be selected because the organism's physiology makes that action natural under the lawful facts of the moment.

## Responsibilities of each layer

| Layer | Exclusive responsibility | Must not cross into |
| --- | --- | --- |
| Constitution | Establish lawful facts, identities, permissions, prohibitions, invariants, and boundary conditions | Physiological tendencies or visible actions |
| Physiology | Convert lawful conditions into natural response tendencies, capacities, pressures, and regulatory mechanisms | Constitutional authority or literal output scripts |
| Behavior | Express visible actions that result from physiology operating under constitutional constraint | Law-making or durable physiological design |

## What must never cross between layers

### Constitution must never prescribe behavior

The constitution may establish that authenticated operator communication exists. It may establish that opaque observations are admissible. It may establish that unsupported claims cannot become established facts. But it should not say `Ask operator`, `Continue`, or `Stop` as direct commands.

If the constitution prescribes behavior, growth becomes programming. The organism no longer responds naturally to lawful conditions; it executes rules.

### Physiology must never create law

Physiology may form candidate questions, inhibit commitment, or create clarification pressure. It must not decide that a candidate is constitutionally true merely because the organism is inclined toward it.

For example, curiosity may produce a candidate interpretation, but it cannot make that interpretation a lawful fact. Evidence gating exists precisely to prevent physiological pressure from becoming constitutional authority.

### Behavior must never become proof of constitution

A visible action does not prove that the constitution contains a matching rule. If the organism asks a clarification question, that does not mean the constitution says `Ask clarification questions`. It may only mean that lawful uncertainty triggered clarification readiness through physiology.

This protects the architecture from backfilling constitutional rules from observed behavior.

### Presentation vocabulary must never become knowledge by repetition

Visible labels or explanatory phrases may help behavior communicate, but they do not automatically become constitutional facts. If a word appears in presentation, the architecture should not promote it into preserved knowledge merely because it is convenient or repeated.

## Operator communication example

Consider the smallest possible interaction:

```text
Operator
↓
.
```

The period is not analyzed. The architectural question is what changes across layers.

### Constitutional change

The clean constitutional fact is minimal:

```text
Authenticated operator communication exists.
```

Potentially, the constitution may also recognize generic boundary facts if already lawful in the architecture:

```text
The communication may be opaque.
The communication may be insufficient for factual commitment.
The communication is distinguishable from an interpretation of the communication.
```

The constitution does not say:

```text
Ask what the operator means.
Infer intent from the period.
Continue probing.
Stop immediately.
```

### Physiological reaction

From authenticated operator communication, several physiological responses may naturally emerge:

- intake preservation pressure, because the communication is lawful and may be opaque;
- curiosity, because authenticated communication creates an orientation toward understanding;
- candidate-question formation, because opacity creates possible clarification paths;
- evidence gating, because the organism should not commit to unsupported meaning;
- candidate-attachment formation, if the communication may connect to existing lawful context;
- clarification readiness, because lawful communication plus insufficient evidence creates a natural readiness to ask;
- honest stopping pressure, if no lawful next step can be selected without fabricating meaning.

None of these needs to be a constitutional command. They are physiological consequences of the lawful fact that communication exists and the lawful boundary that unsupported interpretation should not become fact.

### Behavioral emergence

Possible behaviors include:

```text
Ask operator.
Continue inquiry.
Stop.
Discard candidate.
Produce clarification.
Preserve opaque intake.
State insufficient evidence.
```

Which behavior appears depends on physiological resolution. If curiosity plus clarification readiness outweighs stopping pressure, the organism may ask a question. If evidence gating blocks all candidate interpretations and no useful clarification can be formed, the organism may stop honestly. If a candidate question is formed but fails evidence or relevance gating, the organism may discard it.

The key point is that behavior is emergent. The constitution establishes communication and lawful boundaries; physiology creates response pressures; behavior is the visible outcome.

## Future sensory observation example

Consider a future sensory observation:

```text
Sensor
↓
unclassified signal
```

### Constitutional facts

A clean constitution might establish:

```text
A sensory observation exists.
The observation is not yet classified.
The observation is distinguishable from any interpretation of it.
Classification requires sufficient lawful support.
```

It should not say:

```text
Classify the signal.
Ask for more data.
Attach the signal to the nearest known object.
Ignore the signal.
```

### Physiological response

The organism may naturally develop:

- preservation pressure for the raw observation;
- comparison pressure against lawful prior facts;
- candidate-classification formation;
- candidate-attachment formation;
- novelty sensitivity;
- evidence gating;
- uncertainty regulation;
- readiness to request more observation;
- stopping pressure when classification would exceed support.

### Behavioral emergence

Visible behavior may include:

```text
Record the observation as opaque.
Generate candidate classifications.
Reject unsupported classifications.
Request additional observation.
State that classification is unavailable.
Stop without classifying.
Commit to a classification only when support is sufficient.
```

Again, no constitutional command to classify is required. The organism naturally orients toward lawful observations because its physiology is receptive, comparative, and evidence-gated.

## Answers to the design questions

### 1. What information belongs exclusively to the constitution?

Only lawful facts and boundary conditions belong exclusively to the constitution:

- recognized entities and relations;
- valid identities;
- lawful communication or observation conditions;
- distinctions between fact, candidate, interpretation, and behavior;
- permissions and prohibitions;
- invariants;
- admissibility conditions;
- commitment boundaries;
- stop conditions as lawful conditions, not commands.

The constitution should say what is lawfully true or possible, not what to visibly do.

### 2. What capabilities belong exclusively to physiology?

Capabilities that transform lawful conditions into natural response tendencies belong to physiology:

- curiosity;
- attention;
- preservation pressure;
- candidate formation;
- candidate attachment;
- evidence gating;
- uncertainty regulation;
- clarification readiness;
- comparison;
- inhibition of unsupported commitment;
- stopping pressure.

These are not visible outputs by themselves. They are capacities and tendencies that make visible outputs possible.

### 3. What observable actions belong exclusively to behavior?

Visible acts belong to behavior:

- asking;
- answering;
- continuing;
- stopping;
- clarifying;
- discarding;
- preserving in a visible record;
- stating insufficiency;
- committing;
- declining to commit.

Behavior is where the organism becomes observable, but not where law is made.

### 4. Can curiosity exist as a physiological property rather than a constitutional rule?

Yes. Curiosity is cleaner as physiology. The constitution need only establish that authenticated communication or lawful observation exists. A living organism naturally orients toward lawful signals. Curiosity is that orientation expressed as a response tendency: preserve the signal, consider possible meaning, form candidate questions, seek support, and remain willing not to know.

If curiosity becomes constitutional, the constitution starts commanding temperament. If curiosity remains physiological, it can vary in intensity by circumstance while still respecting lawful boundaries.

### 5. Should candidate-question formation be physiological rather than constitutional?

Yes. Candidate-question formation is a physiological capability. The constitution may establish that uncertainty exists, that communication is authenticated, and that unsupported interpretation cannot become fact. From those facts, physiology can generate candidate questions.

The constitution should not contain the questions. It should not even require that a question always be asked. A candidate question may form and then be discarded if it fails evidence, relevance, scope, or stopping gates.

### 6. Should stopping be constitutional, physiological, behavioral, or some combination?

Stopping spans all three layers, but differently in each:

- constitution establishes lawful stop conditions;
- physiology generates stopping pressure when continuation would violate those conditions;
- behavior visibly stops.

For example, the constitution may establish that unsupported interpretation cannot be promoted. Physiology detects that all continuation paths require unsupported promotion and generates stopping pressure. Behavior then stops or says that no lawful continuation is available.

The constitution should not say `Stop now` as behavior. It should establish the condition under which stopping becomes lawful or necessary.

### 7. Does separating these three layers simplify future organism growth?

Yes. Separation simplifies growth because new lawful facts can be added without scripting every behavior, and new physiological capacities can produce richer behavior without changing constitutional authority.

For example, if future architecture adds lawful sensory observation, the organism need not receive a list of sensor behaviors. Receptive, preserving, comparative, evidence-gated physiology can naturally produce appropriate behaviors for the new condition.

This also reduces conceptual collisions. Constitutional work can focus on law. Physiological work can focus on natural response. Behavioral work can focus on visible expression.

### 8. Does this separation reduce the need for explicit behavioral programming?

Yes, if physiology is strong enough. Instead of programming `if opaque input, ask clarification`, the architecture can establish lawful opaque intake and support physiology that preserves, forms candidates, gates evidence, and becomes clarification-ready. Asking then emerges when it is the natural visible consequence, not because it was directly commanded.

The reduction is not the elimination of behavior. Behavior still exists. But behavior becomes generated rather than enumerated.

## Advantages

### Cleaner constitutional authority

The constitution remains small, lawful, and non-procedural. It does not accumulate behavioral instructions disguised as principles.

### More natural growth

New facts can create new response patterns through physiology. The organism can grow by deepening its response structure rather than by adding scripts for every possible surface.

### Better uncertainty handling

Because evidence gating and commitment inhibition live in physiology, the organism can remain active without pretending to know. It can generate candidates while preventing candidates from becoming facts too early.

### Reduced behavioral brittleness

If behavior is scripted directly, small contextual changes require new scripts. If behavior emerges physiologically, the same response capacities can adapt across operator communication, sensory observations, diagnostic findings, and future lawful inputs.

### Better protection against accidental knowledge promotion

The separation prevents visible output, candidate language, or presentation vocabulary from automatically becoming constitutional truth.

### Honest stopping

Stopping becomes a natural result of lawful boundaries rather than a failure to continue. The organism can stop because its physiology recognizes that continuation would exceed constitutional support.

## Possible weaknesses

### Physiology may become vague

If physiology is described only metaphorically, it may become a dumping ground for anything that is neither constitutional nor behavioral. The architecture should keep physiological properties precise: candidate formation, evidence gating, preservation pressure, uncertainty regulation, and stopping pressure are clearer than general words such as `instinct` or `desire`.

### Emergence can hide responsibility

If every behavior is described as emergent, it may become difficult to explain why a particular action occurred. The architecture should preserve traceability: lawful fact, physiological response, visible behavior.

### Over-separation may slow decisions

Some actions may appear simple enough to script. The architecture should resist premature scripting but also avoid making every behavior require elaborate explanation. The goal is clean causality, not unnecessary indirection.

### Constitutional minimalism can become under-specification

A constitution that establishes too little may leave physiology without lawful grounding. For example, `Authenticated operator communication exists` may be enough to orient curiosity, but additional lawful distinctions may be needed to prevent unsupported interpretation from becoming fact.

### Behavior may be mistaken for physiology

Repeated behaviors can look like capacities. For example, frequent clarification questions may tempt the architecture to define `asking clarification` as physiology. The cleaner physiological property is clarification readiness; the question itself remains behavior.

## Open questions

1. What is the minimal constitutional set required for physiology to produce honest curiosity without producing unsupported interpretation?
2. How should physiological pressures be prioritized when curiosity, evidence gating, clarification readiness, and stopping pressure conflict?
3. How can the organism explain emergent behavior without converting that explanation into a behavioral rule?
4. When a behavior appears repeatedly, what prevents it from being promoted accidentally into constitution?
5. Can physiological properties be composed without becoming hidden subsystems?
6. What distinguishes a lawful stop condition from a physiological stopping pressure in edge cases?
7. How much constitutional structure is needed for future sensory observations before physiology can respond cleanly?
8. Can this model support multiple simultaneous lawful inputs without scripting behavior for each combination?

## Architectural conclusion

Separating constitution, physiology, and behavior produces a cleaner organism than treating them as one.

The constitution should establish lawful facts only. Physiology should naturally respond to those facts through preservation, curiosity, candidate formation, evidence gating, clarification readiness, and stopping pressure. Behavior should be the visible consequence: asking, continuing, stopping, discarding, preserving, clarifying, or declining to commit.

The central acceptance question can therefore be answered:

```text
If the constitution establishes only lawful facts,
what physiology naturally emerges,
and what behaviors naturally emerge from that physiology,
without the constitution ever prescribing behavior?
```

When authenticated operator communication exists, physiology naturally becomes receptive, curious, preserving, candidate-forming, evidence-gated, clarification-ready, and willing to stop. From that physiology, behavior may ask, continue, clarify, discard, preserve, or stop.

The constitution does not need to command behavior. It establishes the lawful world in which physiology can live. Behavior is the organism's visible life within that world.
