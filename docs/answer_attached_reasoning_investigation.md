# Answer-attached reasoning investigation

## Question

This investigation asks whether Seed is converging toward answer-attached
reasoning: when Seed produces a statement, the explanation chain should travel
with the answer rather than requiring a separate retrieval task.

The investigation is conceptual and implementation-backed. It does not propose
new commands, flags, audits, workflow engines, runtime autonomy, or user
interfaces.

## Surfaces reviewed

The review focused on repository surfaces that already expose conclusions,
selection, derivation, or operational interpretation:

| Surface | Reviewed implementation evidence | Primary answer shape |
| --- | --- | --- |
| `reference_selection` | `ReferenceSelection` returns `selected_reference`, `selection_rationale`, alternatives, boundaries, and limitations. | Selected reference plus attached rationale and authority boundary. |
| `selection_path_audit` | `SelectionPathAudit` returns selected item, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and boundary. | Selection answer plus attached selection path. |
| `reasoning_path_audit` | `ReasoningPathAudit` returns evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and boundary. | Derivation answer plus attached chain and downstream consumers. |
| `capability_relationship` | `CapabilityRelationship` returns capability, access, benefit, pressure, attainability, expectation, reasoning, and limitations. | Capability relationship answer plus attached reasoning and limits. |
| `projection_shape` | `ProjectionShapeStage` returns each stage's consumes, produces, influences, non-influences, authority boundary, and confidence. | Projection stage answer plus attached influence map. |
| `observation_permission` | `ObservationPermissionDomain` returns domain, class, permission state, authority evidence, reasoning, limitations, reusable permission, and future invocation status. | Permission answer plus attached authority evidence and reasoning. |
| `operational_story` | `OperationalStory` returns focus, pressure, support, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and boundary. | Operational answer plus attached evidence and investigation path. |

## Answer-producing surfaces

Several surfaces already produce direct answers rather than only raw diagnostic
rows.

- `reference_selection` answers which reference is selected for a domain. Its
  data model makes the selected reference inseparable from rationale,
  alternatives, boundary, and limitations.
- `selection_path_audit` answers what was selected for a target. It also includes
  the candidate set, factors, non-selected candidates, evidence, and outcome.
- `capability_relationship` answers how a capability relates to access,
  operational benefit, pressure, attainability, and expectation.
- `observation_permission` answers whether an observation domain has reusable
  permission, requires operator expression, is denied, or is unknown.
- `operational_story` answers the current operational focus and pressure while
  carrying supporting evidence, capability needs, constraints, correlation gaps,
  impacts, changes, outcomes, and investigation path.

These are not merely storage or enumeration surfaces. They produce operator-
readable statements such as selected reference, current focus, permission state,
capability benefit, and projection influence.

## Reasoning-producing surfaces

Some reviewed surfaces are explicitly reasoning-chain surfaces.

- `reasoning_path_audit` is the clearest chain surface. It starts from a domain
  and subject, then returns observed evidence, intermediate conclusions, derived
  conclusions, consumers, story impact, and unknowns.
- `selection_path_audit` is selection reasoning. It does not only report the
  selected item; it reports candidates, rank, score, evidence, selection factors,
  non-selection reasons, and outcome.
- `projection_shape` is influence reasoning. It reports what each projection
  stage consumes, produces, influences, and explicitly does not influence.
- `reference_selection` is reference reasoning. It reports why a reference was
  selected and why alternatives are only candidates.

These surfaces show that Seed already has chain preservation for several classes
of question: why selected, what produced this, what does this influence, and what
is downstream of this conclusion.

## Attached-reasoning examples

### Reference selection

`reference_selection` succeeds as answer-attached reasoning because the answer is
not only `selected_reference`. The same object also carries selection rationale,
alternative references, authority boundary, and limitations. In the history case,
the rationale states that impact comparison uses latest comparable snapshot pairs
and that the historical brief is built from impact and snapshot-policy outputs.
The authority boundary prevents the selected reference from becoming an accepted
baseline or expectation-bearing reference.

This is an answer with attached explanation. The operator does not need to run a
second command to learn why the reference was chosen or what the selection does
not authorize.

### Selection path audit

`selection_path_audit` attaches the explanation to the selection result. Its
result includes the selected candidate, all candidates, selection factors,
non-selected candidates, evidence, outcome, and unknowns. The implementation
also preserves non-selection reasons such as lower pressure score or tie-breaking
by category name.

This directly answers `Why was this selected?` without making selection and
rationale separate retrieval tasks.

### Reasoning path audit

`reasoning_path_audit` makes a fragmented operational chain visible in one
result. It pulls from ownership discrepancies, capability needs, pressure,
privilege discovery, and operational story, then separates observed evidence,
intermediate conclusions, derived conclusions, consumers, and story impact.

This is still an audit surface, but its successful behavior is not that it is
another flag. Its successful behavior is that evidence, derived claims, and
consumers travel together.

### Capability relationship

`capability_relationship` attaches reasoning to capability relationship answers.
It reports the capability, current access, operational benefit, pressure,
attainability, and expectation together with explicit reasoning and known
limitations. The reasoning is especially important because the surface prevents
capability pressure from becoming acquisition guidance or deployment intent.

This answers `Why does this capability matter?` while preserving the boundary
that Seed has not observed operator intent or acquisition authority.

### Projection shape

`projection_shape` attaches influence information directly to projection stages.
Each stage reports what it consumes, produces, influences, does not influence,
and what authority boundary applies. This is a compact example of conclusion plus
support plus influence: a stage exists, its inputs and outputs are visible, and
its downstream influence is stated.

This answers `What produced this?` and `What does this influence?` better than a
surface that only lists stage names.

### Observation permission

`observation_permission` attaches authority evidence and reasoning to permission
state. It distinguishes recognized observation domains, reusable approval,
manual operator invocation, future autonomous invocation, and implementation
limitations.

This answers `Why can't this be observed?` or `Why is this not reusable
permission?` without collapsing a manual invocation into durable approval.

### Operational story

`operational_story` is answer-attached at the story level. The current focus and
primary pressure are returned with supporting evidence, missing capabilities,
access constraints, correlation gaps, impact, changes, outcomes, and an
investigation path. It acts as a composition over existing visibility surfaces
rather than a new authority layer.

This supports the pattern that an operational answer is stronger when its
explanation travels with it.

## Fragmented-reasoning examples

The repository also shows why answer-attached reasoning is needed.

- Ownership discrepancy to capability need to capability relationship to
  observation domain to operational story can require manual reconstruction when
  viewed through individual surfaces. `reasoning_path_audit` helps only when the
  operator already knows to ask for the path and supplies a useful subject.
- Reference evidence, selection rationale, and selected reference are attached
  in `reference_selection`, but similar selection behavior in other areas may
  still require moving between raw evidence, policy, and downstream story
  surfaces.
- Projection stages already attach consumes/produces/influences, but an operator
  asking about a specific projected conclusion may still need to map from the
  conclusion back to the stage chain manually unless an existing explanation
  surface covers that conclusion.
- Operational story bundles focus and support, but deeper derivation may still
  require `reasoning_path_audit` for the chain from upstream evidence to story
  impact.

The fragmented cases do not prove that Seed needs more surfaces. They prove that
answers degrade when their reason, support, and influence are distributed across
separate retrieval tasks.

## Supported conclusions

1. **Reasoning attachment is already a recurring repository pattern.** The
   reviewed surfaces repeatedly pair conclusions with rationale, support,
   limitations, boundaries, and influence.
2. **The successful surfaces behave more like `answer -> attached explanation`
   than `answer -> go run another command`.** `reference_selection`,
   `selection_path_audit`, `capability_relationship`, `projection_shape`,
   `observation_permission`, and `operational_story` all put explanatory context
   in the same result as the answer.
3. **Reasoning attachment is not the same as adding more audit families.** The
   important pattern is not proliferation of flags. It is preserving explanation
   where Seed makes or exposes a statement.
4. **Answer-attached reasoning protects authority boundaries.** Attached
   reasoning commonly includes limitations and read-only/no-mutation boundaries,
   preventing pressure, permission, references, or projection effects from being
   over-interpreted.
5. **Some reasoning should remain separately inspectable.** Chain-focused
   surfaces such as `reasoning_path_audit` remain useful for deep derivation, but
   they are strongest when they bundle evidence, intermediate conclusions,
   derived conclusions, consumers, and impact rather than requiring operators to
   reconstruct those pieces manually.

## Unsupported conclusions

The reviewed evidence does not support these stronger claims:

- Seed should introduce a new answer-attached-reasoning interface.
- Seed should add new command flags, audits, summaries, workflow engines, or UI
  concepts.
- Every answer must include every possible reasoning path.
- Reasoning chains should become cluster truth or be recorded directly on hosts,
  services, filesystems, or runtime entities.
- Presentation terms alone should become repository knowledge without
  implementation evidence.

## Open questions

- What is the smallest useful attached explanation for ordinary answers: source,
  support count, rationale, limitation, influence, or all of these?
- When does attached reasoning become too verbose for the answer surface and need
  a separate deep inspection path?
- Which answer types already have enough attached reasoning through fact support,
  confidence, contradictions, and context views, and which answer types still
  force manual reconstruction?
- Should attached reasoning prefer stable identifiers and support references over
  prose when the answer can be consumed by later tools?
- How should Seed distinguish explanation attached for operator comprehension
  from explanation preserved as durable evidence?

## Investigation answer

The repository is increasingly showing that explanation belongs with the answer
itself when Seed makes an implementation-backed statement. The strongest
existing surfaces do not merely expose additional data; they attach the reason,
support, influence, limitations, and authority boundary to the result they
produce.

Separate retrieval remains useful for deep derivation and focused audits, but it
should not be the default burden placed on the operator for ordinary `why`,
`what produced this`, `why selected`, `why missing`, or `what does this
influence` questions. The supported pattern is therefore:

```text
answer
    +
attached explanation sufficient to understand authority, support, and limits
```

not:

```text
answer
    ->
operator manually reconstructs the reasoning chain elsewhere
```
