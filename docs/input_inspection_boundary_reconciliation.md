# Input Inspection Boundary Reconciliation

## Purpose

This reconciliation investigates whether source observation inspection and
language candidate inspection are manifestations of one shared architectural
boundary or separate phenomena that merely exhibit a similar shape.

It is an investigation, not a proposal. It does not implement runtime behavior,
define schemas, create command aliases, add governance, modify ontology, or
claim a shared abstraction merely because similar diagrams recur.

Repository authority wins over this document. Existing source-observation,
repository-observation, language, routing, promotion, authority, and capability
reconciliations remain authoritative for their own scopes.

## Central Question

```text
Are source observation inspection
and language candidate inspection

manifestations of a shared architectural boundary?

or

are they separate architectural phenomena
that merely exhibit similar structure?
```

The answer is mixed: repository evidence supports a shared **preservation
pattern** around pre-promotion candidate spaces, but it does not yet justify a
single shared architectural boundary with identical authority, inputs, outputs,
or downstream transitions.

## Evidence Reviewed

This investigation reviewed repository evidence from both families and nearby
boundary work, including:

- `docs/repository_observation_source_design.md`
- `docs/repository_observation_implementation_inventory_audit.md`
- `docs/repository_observation_characterization.md`
- `docs/repository_observation_seed_characterization.md`
- `docs/repository_observation_language_boundary.md`
- `docs/repository_artifact_ontology_reconciliation.md`
- `docs/source_definitions_and_entrypoint_observation_reconciliation.md`
- `docs/repository_observation_validation_audit.md`
- `docs/documentation_lineage_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/learning_as_lens_observation.md`
- `docs/observation_surface_and_blind_spot_audit.md`
- `docs/input_inspection_reconciliation.md`
- `docs/input_act_vocabulary.md`
- `docs/input_envelope_vocabulary.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/natural_language_request_routing_audit.md`
- `docs/natural_language_execution_path_inventory_audit.md`
- `docs/interpretation_candidate_preservation_audit.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/candidate_request_and_routing_boundary_reconciliation.md`
- `docs/candidate_meaning_and_ambiguity_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`

Implementation surfaces were reviewed where useful, including tests for input
inspection, candidate requests, repository observation, relationship
observation, observation sources, event batching, and projection/state views.
Those surfaces were used as evidence of current repository shape, not as a basis
for proposing runtime changes.

## Repository Shapes Under Comparison

Family A, source/repository observation, repeatedly uses a shape like:

```text
repository source text
    ↓
inspection / parsing / observation
    ↓
relationship candidates or observations
    ↓
fact or relationship promotion, when justified
    ↓
projection / explanation / response
```

Family B, language candidate preservation, repeatedly uses a shape like:

```text
operator language
    ↓
communicative-act observation / input inspection
    ↓
interpretation and candidate request preservation
    ↓
routing
    ↓
clarification, promotion, capability selection, decision, command, refusal, or execution boundary
```

The recurring generic shape is real:

```text
raw input
    ↓
inspection
    ↓
candidate space
    ↓
promotion/routing
```

The reconciliation question is whether that generic shape is architecture or
only family resemblance.

## Part 1: Inspection

### What is being inspected in source observation?

Source observation inspects repository-local artifacts and source text. The
source input may be a Python file, documentation file, catalog, generated
architecture artifact, test file, or other repository-local artifact selected as
read-only evidence. The inspection target is not the operator's desired action;
it is what repository evidence says about artifacts, definitions, imports,
relationships, declarations, lineage, and other source-local structures.

What survives inspection:

- source artifact identity;
- source location and line/range evidence where available;
- observed definitions, imports, declarations, or relationship-like structures;
- evidence about documentation lineage or discovery path when the document itself
  preserves it;
- source authority caveats, such as documentation declaration not proving runtime
  behavior and tests not proving passing status unless tests are actually run.

What is discarded or intentionally not promoted:

- behavior claims not supported by the inspected source structure;
- ownership claims inferred only from imports or references;
- runtime availability or operator command existence inferred only from an
  adapter primitive;
- freshness, verification, or enforcement claims not established by the inspected
  artifact.

What remains unresolved:

- whether a repository-wide acquisition workflow exists for every primitive;
- which source relationships beyond imports and definitions should be observed;
- how much lineage survives when documentation compresses discovery paths into
  final findings;
- where source observation should stop before becoming architecture enforcement
  or repository management.

### What is being inspected in language candidate work?

Language candidate work inspects operator communicative acts: raw user messages,
input envelopes, phrasing, intent signals, ambiguity, target candidates, and
possible request meanings. The input is a communication event, not an external
world fact and not a command by default.

What survives inspection:

- raw text or input event;
- input-act classification or communicative-act observation;
- possible meanings, request candidates, target candidates, and route candidates;
- ambiguity state and confidence distinctions;
- notes that inspection is preservation-only and does not select capabilities,
  make execution decisions, or execute tools.

What is discarded or compressed in current implementation surfaces:

- many possible meanings after a single `Decision` is selected;
- the full interpretation space behind a selected route or response;

What remains unresolved:

- how much candidate interpretation should be preserved durably;
- when clarification should be preferred over routing;
- where natural language becomes an accepted request, decision, command, or
  claim;
- how to avoid treating language authority as environmental truth authority.

## Part 2: Candidate Space

Both families create candidate spaces, but the contents and costs differ.

### Source-family candidate spaces

Source-family candidate spaces include:

- relationship candidates, such as imports, definitions, containment,
  entrypoints, calls, registrations, reads, writes, or emits;
- possible observations derived from source text;
- possible promotions into facts or relationships;
- possible documentation lineage links;
- possible source-supported claims about artifacts, declarations, and structure.

The candidate space is evidence-facing. Its primary danger is overclaiming what
the source proves. For example, import can support dependency knowledge, but not
ownership; definition can support ownership-of-symbol evidence, but not
invocation; entrypoint can support reachability evidence, but not capability or
execution authority.

### Language-family candidate spaces

Language-family candidate spaces include:

- candidate requests;
- possible meanings;
- possible targets;
- possible routes;
- possible questions, goals, constraints, claims, recommendations, tasks,
  commands, or refusals;
- possible capability selections only after routing and authority checks.

The candidate space is interaction-facing. Its primary danger is premature
collapse from language to nearest capability or execution. Language may produce
strong candidates, but candidate request does not equal command, route does not
equal capability selection, and capability selection does not equal execution.

### Candidate-space similarity

The strongest similarity is preservation of alternatives before acceptance:

```text
candidate status must remain visible until a boundary-specific authority can
justify selection, promotion, clarification, or rejection.
```

Both families improve when candidates are not silently collapsed into certainty.
Both families treat ambiguity as information and premature certainty as risk.
Both families distinguish the inspected source from downstream accepted
structures.

### Candidate-space difference

The strongest difference is the target of candidate acceptance:

- source candidates tend toward evidence-backed fact or relationship promotion;
- language candidates tend toward routing, clarification, response, decision,
  command, refusal, or possible claim creation.

That difference matters because fact promotion and request routing use different
authority questions.

## Part 3: Promotion And Routing

### What happens after source inspection?

After source inspection, repository evidence may remain an observation, become
evidence for a claim, support fact promotion, support relationship promotion, or
be projected into read models and explanations. Promotion is narrow and bounded:
the promoted fact or relationship must say no more than the evidence supports.

Possible outcomes include:

- no promotion, only preserved observation;
- fact promotion when evidence, support, and confidence justify it;
- relationship promotion when the relationship type is supported without
  identity overclaim;
- projection into state, impact, graph, or explanation surfaces;
- documentation navigation or lineage preservation when the inspected artifact is
  itself documentation.

Source inspection should not become repository repair, test execution,
architecture enforcement, or runtime behavior merely because a source artifact
was inspected.

### What happens after language inspection?

After language inspection, possible outcomes include:

- answer;
- clarification question;
- candidate request preservation;
- route preservation;
- capability-gap recording;
- capability selection;
- execution decision;
- command;
- refusal;
- no-op or deferred handling.

Language inspection should not collapse into execution. Even a high-confidence
candidate such as `show state summary` must still pass through the relevant
routing, capability, policy, decision, and execution authority boundaries if the
path performs work.

### Routing versus promotion

Routing and promotion overlap as transitions out of candidate space, but they
are not the same transition.

Routing asks:

```text
Which boundary should consider this candidate?
```

Promotion asks:

```text
What structured object is accepted or created under what support and authority?
```

Source-family work often emphasizes promotion into facts and relationships.
Language-family work often emphasizes routing before promotion, clarification,
capability selection, or execution decision. This is one of the strongest
reasons not to declare a single shared boundary.

## Part 4: Authority

### Source observation authority

Source observation requires source authority. Repository-local evidence can
support claims about the artifact observed, but its authority is scoped.
Documentation can declare architecture without proving runtime behavior. A test
file can evidence test existence without proving the test currently passes. A
source parser can observe imports without proving ownership or invocation.

Observation becomes fact only when evidence, support, scope, and claim strength
justify the promotion. Relationship promotion similarly requires that the
relationship not overclaim identity, ownership, behavior, reachability, or
capability.

### Language routing authority

Language routing requires communicative-act and operator-interface authority.
Language can evidence that an operator said something, requested something,
presupposed something, or may mean something. It does not by itself prove an
environmental fact, authorize execution, create a goal, select a capability, or
perform work.

Interpretation becomes action only after crossing additional boundaries:

```text
candidate meaning
  -> route
  -> capability selection or response boundary
  -> decision / command when applicable
  -> execution
  -> action only if reality is mutated
```

### Authority finding

The authority structures are analogous but not identical. Both families use
bounded source authority and resist premature promotion. But the source family
asks whether repository evidence can support knowledge; the language family asks
how an operator communication should be interpreted, routed, and possibly acted
upon without treating interpretation as authorization.

## Required Findings

### Strongest similarities

- Both families preserve raw input before downstream selection.
- Both distinguish inspection from acceptance.
- Both produce candidate spaces that must not be silently collapsed.
- Both treat ambiguity as information rather than automatic failure.
- Both require authority checks before candidates become facts, routes,
  commands, executions, or actions.
- Both warn that projection or route visibility is not the same as authority.

### Strongest distinctions

- Source observation inspects artifacts; language candidate work inspects
  communicative acts.
- Source candidates primarily seek evidence-backed knowledge promotion; language
  candidates primarily seek interaction routing and possible request handling.
- Source promotion asks what is true or supported about repository artifacts;
  language routing asks what boundary should handle an operator's possible
  meaning.
- Source evidence authority is artifact/source scoped; language authority is
  speaker/input scoped and does not imply environmental truth or execution
  permission.
- Source observation can be read-only knowledge acquisition; language routing may
  approach execution, command, refusal, or clarification boundaries.

### Strongest overlaps

- Candidate preservation before certainty.
- Boundary-specific downstream acceptance.
- Source attribution and caveat preservation.
- Avoidance of invisible interpretation.
- Rejection of direct collapse from input to action or fact.

### Strongest divergences

- Fact promotion and request routing are different downstream moves.
- Relationship candidates and candidate requests have different acceptance
  criteria.
- Repository artifact authority and operator authority answer different
  questions.
- Source inspection can often remain entirely in knowledge acquisition, while
  language inspection often touches operator interaction and execution gates.
- Evidence preservation and meaning preservation are related preservation
  pressures, but they preserve different losses.

### Strongest preservation pressures

- Preserve raw source text or raw operator text enough to audit interpretation.
- Preserve candidate status until promotion, routing, or rejection is justified.
- Preserve ambiguity instead of hiding it behind selected results.
- Preserve authority caveats so downstream surfaces do not overstate what was
  inspected.
- Preserve lineage where final findings compress the path by which a candidate
  became visible.

### Strongest authority differences

- Source observation authority is about evidence support for claims.
- Language authority is about communicative acts, requests, and operator-facing
  routing.
- Source observation can support facts without creating commands.
- Language interpretation can create request candidates without proving facts or
  authorizing execution.
- Promotion to fact and promotion to command have different costs and different
  required authority.

### Strongest candidate-space similarities

- Multiple candidates can exist legitimately.
- Candidate visibility is safer than premature certainty.
- Candidates are not failures.
- Candidates need route- or promotion-specific handling.
- Candidate loss is an architectural risk because later explanations cannot show
  why a selected result won.

### Strongest candidate-space differences

- Relationship candidates ask what relation source evidence may support.
- Candidate requests ask what the operator may be asking for.
- Possible observations remain tied to evidence acquisition.
- Possible meanings remain tied to interpretation of communication.
- Possible promotions in source work tend toward claims; possible promotions in
  language work may become questions, goals, recommendations, decisions,
  commands, claims, or refusals depending on boundary.

### Strongest promotion differences

- Source promotion is claim/relationship acceptance under evidence authority.
- Language promotion may create structured interaction objects, but routing often
  precedes promotion.
- Routing is not promotion; it only selects the boundary that should consider a
  candidate.
- Execution is not promotion; it is a later realization of a command through a
  concrete provider/tool/adapter path.

## Required Tensions

### Inspection vs observation

Inspection is the act of examining input. Observation is the preserved record or
source-derived evidence. Source work often uses observation as the durable
knowledge-acquisition unit. Language work may inspect input while preserving less
of the interpretation space unless candidate preservation is explicit.

### Inspection vs interpretation

Inspection can identify structures; interpretation attaches possible meaning.
Source parsing may interpret syntax as imports or definitions, but it should not
interpret those as ownership or behavior without support. Language
interpretation may identify possible requests, but it should not treat them as
commands.

### Candidate vs promotion

Candidate means possible. Promotion means accepted into a stronger structured
role under authority. Both families are harmed when candidate status disappears.

### Candidate vs routing

A candidate can be routed, but the route is not the candidate itself. Routing
says where the candidate should be considered, not that the candidate is true,
selected, executable, or sufficient.

### Routing vs promotion

Routing directs attention to a boundary. Promotion creates or accepts a
structured object. Language work relies heavily on this distinction; source work
uses it less centrally but still needs it when observations move toward fact or
relationship acceptance.

### Knowledge acquisition vs operator interaction

Source observation is primarily knowledge acquisition. Language inspection is
operator interaction and may become knowledge acquisition only when the language
is treated as evidence for a communication, claim, correction, or request.

### Fact promotion vs request routing

Fact promotion asks whether evidence supports a claim. Request routing asks
which interface or capability boundary should consider a possible operator
meaning. They may share candidate-preservation pressure, but they are not the
same architectural transition.

### Ambiguity preservation vs observation preservation

Observation preservation keeps evidence available. Ambiguity preservation keeps
multiple interpretations visible. Evidence can be preserved while ambiguity is
lost if only the selected interpretation remains.

### Meaning preservation vs evidence preservation

Meaning preservation protects the interpretation space around an input. Evidence
preservation protects the source material and support chain. A future reader may
need both to understand why a candidate was accepted, rejected, routed, or left
unresolved.

## Final Conclusion

Repository evidence does not support declaring source observation inspection and
language candidate inspection to be simply the same architectural boundary.
Their inputs, authority questions, downstream transitions, and failure modes are
too different.

Repository evidence also does not support treating them as unrelated. They share
a strong architectural preservation pattern:

```text
preserve raw input,
inspect without overclaiming,
make candidate space visible,
and cross only boundary-specific promotion, routing, decision, or execution
thresholds.
```

The most defensible conclusion is therefore:

```text
A shared pre-acceptance preservation pattern exists.
A single shared architectural boundary is not yet justified.
```

Future work should cite this reconciliation as a boundary caution: similarity of
shape is evidence for a recurring preservation pressure, not authority to merge
source observation, language interpretation, candidate routing, fact promotion,
and execution decision into one abstraction.

## Unresolved Questions

- Whether Seed should ever name a cross-cutting pre-acceptance preservation
  concern, or whether scoped documents are sufficient.
- How much candidate space should be durably preserved in implementation without
  creating unbounded candidate growth.
- How repository acquisition workflows should preserve relationship candidates
  that do not promote.
- How language routing should preserve rejected or clarified alternatives after a
  selected response.
- Whether documentation lineage and discovery-path preservation require a
  separate preservation surface or remain observation-only findings.
- How future projections should expose candidate history without implying
  authority or acceptance.
