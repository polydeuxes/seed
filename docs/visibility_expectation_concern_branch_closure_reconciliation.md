---
status: reconciliation
scope: visibility / expectation / concern branch closure
created: 2026-06-18
---

# Visibility / Expectation / Concern Branch Closure Reconciliation

## Status

Investigation only. This document does not implement storage behavior, baseline
storage, expectations, concern recording, operator surfaces, HomeOps, SeedOps,
Topology surfaces, lenses, schemas, projections, runtime behavior, policy
behavior, tests, or ontology.

Repository authority wins over this reconciliation. The purpose of this document
is branch-closure reconciliation: determine whether the investigation branch has
answered the original operator pain, what was learned, and what remains outside
this branch.

Closure assessment:

```text
The branch answered the original operator pain at the conceptual level.
It did not implement any surface or policy.
It did not discover a genuinely new independent architectural primitive.
It reconciled existing repository patterns into a coherent explanation and
identified the remaining gaps as separate authority questions.
```

## Original operator pressure

The branch did not originate from an abstract baseline, expectation, ownership,
or concern question. It originated from operational pressure:

```text
Storage surfaces appeared empty.
Filesystem measurements existed.
Identity boundaries prevented expected visibility.
Node116 mount-loss examples exposed operational concerns.
The operator wanted Seed to eventually help identify meaningful topology changes.
```

The initial pain was therefore not "where should HomeOps render this" and not
"which new ontology should be added." The pain was that Seed had evidence that
looked operationally meaningful, but the evidence did not appear where the
operator expected and did not yet support a safe statement that a topology change
was meaningful.

The earliest storage symptom was explained by the endpoint/host identity and
measurement-subject boundary: Prometheus filesystem measurements are attached to
scrape endpoint subjects, while host identities such as `node115` or `node116`
are not silently collapsed with endpoint-shaped subjects for query ownership.
Alias-like knowledge such as a Prometheus instance relation preserves identity
knowledge, but it does not transfer endpoint-owned measurements to the host.

The node116 example then widened the pressure: even if ownership is unknown, a
node that historically saw a mount and now no longer sees it may still matter to
an operator. That forced the branch to distinguish descriptive visibility,
continuity, comparison reference, expectation, and concern without converting
history into a hidden `should`.

## Investigation progression

The branch progressed from concrete visibility failure to authority boundaries:

```text
Why does storage appear empty when filesystem measurements exist?
    ->
Are endpoint subjects and host identities intentionally distinct?
    ->
Does alias knowledge transfer measurement ownership?
    ->
Is the missing concept ownership, target/description, visibility, or concern?
    ->
Can visibility loss matter even when ownership is unknown?
    ->
Can history create expectation?
    ->
Is a baseline continuity evidence, a selected comparison reference, or a should?
    ->
What authority can select a comparison reference?
    ->
What authority would be required to say a mount should continue to be visible?
    ->
Can the branch explain observation-to-operator-significant concern without
    implementing a surface or adding new authority classes?
```

The progression stayed anchored in the original operator pain. Later audit
questions were not the origin; they were successive attempts to preserve the
repository's boundaries while explaining why a visibility change can be
important.

## Major findings

1. **Endpoint visibility is not host ownership.** Filesystem measurements from
   Prometheus live on endpoint-shaped measurement subjects unless another source
   records the fact directly on a host subject. Endpoint/host alias collapse is
   intentionally blocked, and `prometheus_instance`-like knowledge does not move
   facts.

2. **Measurement subject and stable entity identity are distinct.** The current
   effective measurement owner is the fact subject after permitted
   canonicalization. The repository does not currently have a general separate
   measurement-owner, observed-entity, or ownership-transfer model for
   endpoint-derived measurements.

3. **Visibility can be useful without ownership.** Repository evidence supports
   visibility as a descriptive/read-projection concept. A future read-only view
   can show endpoint-visible filesystem or availability evidence with caveats,
   but that does not create host ownership, physical ownership, action authority,
   or remediation authority.

4. **Operational concern can arise without ownership.** A filesystem visibility
   loss can matter to an operator even when the repository cannot prove who owns
   the storage. Concern is not the same thing as ownership, expectation, alerting,
   or remediation.

5. **History does not by itself create expectation.** Observation history and
   continuity can support a candidate comparison reference. They do not authorize
   the claim that a condition should continue.

6. **Accepted baseline is a selected comparison reference, not a new source of
   truth.** The accepted-baseline vocabulary is useful only as the selected
   reference state/effect inside a scoped investigation or decision context. It
   does not independently create ownership, expectation, alerting, policy,
   execution, or remediation authority.

7. **Expectation requires separate should-bearing authority.** To say
   `node116 should see mount M`, repository authority would require an authorized
   expectation, requirement, policy, goal-derived rule, or approved baseline
   promotion mechanism. Current observation history alone is insufficient.

8. **The branch mostly reconciled existing patterns.** The concepts that carried
   the resolution were already present or already emerging in repository
   authority: observation, visibility, continuity, decision/selection,
   investigation scope, current work orientation, handoff preservation, and
   policy/goal/requirement boundaries.

## Authority boundaries clarified

The branch clarified these boundaries:

| Boundary | Clarification |
| --- | --- |
| Evidence boundary | Observations say what was seen, with provenance. They do not say what is owned, required, or wrong. |
| Identity boundary | Endpoint-shaped scrape subjects and stable host identities are not silently collapsed. |
| Measurement boundary | A measurement's subject is the current query/projection owner unless explicit repository authority says otherwise. |
| Visibility boundary | Visibility reports what is or was visible; it does not imply ownership. |
| Interpretation boundary | Continuity and candidate baseline interpret evidence as a possible comparison reference; they do not create a should. |
| Selection authority boundary | An accepted baseline requires authorized selection of a comparison reference within a scope. |
| Should-bearing boundary | Expectation requires distinct normative authority; history and accepted baseline are not enough by themselves. |
| Operator-significance boundary | Concern can identify that a difference matters to an operator without becoming alerting, remediation, or execution authority. |
| View/lens boundary | Views can scope interpretation and presentation, but they do not create State truth, policy, expectation, or execution authority. |
| Handoff boundary | Handoff preserves selected context and authority trail; it does not invent the authority it transfers. |

## Concepts reconciled

The branch reconciled the following repository-supported concepts:

- **identity**: endpoint identity, host identity, alias-like knowledge, and the
  endpoint/non-endpoint collapse boundary;
- **measurement subject**: the subject on which current measurement support is
  recorded and queried;
- **visibility**: descriptive current or historical observed presence/absence;
- **ownership**: not one generic concept, and not implied by visibility;
- **target / described entity**: partially modeled through subject, predicate,
  dimensions, and source-specific metadata, but not generalized as an ownership
  transfer;
- **continuity**: interpretation over evidence about what persisted or recurred;
- **candidate baseline**: an evidence-supported possible comparison reference;
- **accepted baseline**: a scoped selected comparison reference, derivative of
  authorized selection;
- **expectation**: a should-bearing claim requiring separate authority;
- **concern**: operator-significant interpretation that can exist before
  expectation, alerting, or remediation;
- **decision / investigation context / current work position / handoff context**:
  existing authority and continuation patterns that explain selection, scope,
  orientation, and preservation without adding an independent baseline authority
  class.

## Remaining gaps

The remaining gaps are real, but they do not justify keeping this branch open as
an investigation of the original pain.

### Architectural gaps

- The repository does not yet have a general implemented continuity query model
  over long-term observation history. The branch can describe continuity, but it
  did not implement a persistence/query layer for it.
- The repository does not yet decide whether concern should remain architectural
  vocabulary or become a first-class recorded concept.
- The repository does not yet choose whether baselines should be represented in
  code, documents, decisions, handoff context, views, or some other existing
  pattern.
- The repository does not yet generalize target/description beyond current
  subject, predicate, dimension, metadata, and source-specific patterns.

### Policy questions

- Which authorities may declare or promote an operational topology expectation
  remains a policy/authority question.
- Which authorities may accept comparison references for different scopes
  remains a policy/decision question.
- When a concern should become an alert, recommendation, requirement, or action
  remains outside this branch.

### Implementation questions

- How Storage Lens, Node Detail, Availability Lens, or other
  topology surfaces should render endpoint-visible facts is an implementation and
  view-design question, provided they preserve the reconciled boundaries.
- How to compute or store continuity evidence is an implementation question.
- How to expose selected comparison references or expectations, if later
  authorized, is an implementation question.
- How to causally relate ingestion unevenness to mount visibility loss is an
  implementation/evidence question unless a separate architecture investigation
  makes causality part of its scope.

## Node116 example revisited

The original node116 example can now be explained coherently using repository-authoritative terminology:

```text
Observation:
    Seed has evidence that node116, or an endpoint associated with node116,
    reported filesystem visibility for mount M at earlier times.

Current visibility:
    Later evidence no longer shows that same node116-scoped visibility for
    mount M.

Continuity:
    The earlier repeated or durable visibility can be interpreted as historical
    continuity.

Candidate baseline:
    That historical visibility can be framed as a possible comparison reference
    for the investigation.

Accepted baseline:
    A decision or other recognized authority may select that historical
    visibility as the comparison reference for a scoped investigation.

Expectation:
    The repository still cannot say `node116 should see M` unless separate
    should-bearing authority declares or derives that expectation.

Concern:
    The difference between historical visibility and current visibility can be
    operator-significant even before ownership or expectation is proven.
```

This explanation does not assert that node116 owns mount M. It does not assert
that mount M exists now. It does not assert that missing M is a policy violation.
It does not authorize remediation. It explains why the operator's concern is
legitimate as a visibility/continuity/comparison-reference concern while
preserving the repository's authority boundaries.

## Branch closure assessment

The branch has reached conceptual closure for the original operator pressure.

It answered:

```text
Why did visible filesystem evidence fail to appear as expected?
```

By identifying the endpoint/host identity boundary and measurement-subject
ownership model.

It answered:

```text
Can a mount visibility loss matter if ownership is unknown?
```

Yes. Visibility loss can be operator-significant without ownership.

It answered:

```text
Can Seed safely move from observation toward meaningful topology-change concern?
```

Yes, conceptually, through the boundary-preserving progression:

```text
Observation
    -> Visibility
    -> Continuity
    -> Candidate Baseline
    -> Accepted Baseline, if selected by authority
    -> Concern
```

But the complete progression to `Expectation` requires an additional
should-bearing authority boundary:

```text
Accepted Baseline
    ? should-bearing authority
    -> Expectation
```

Therefore the repository possesses a coherent explanation from observation to
operator-significant concern. It does not yet possess authority to convert every
such concern into expectation, alerting, or remediation.

## Reopen criteria

Reopening this branch would be justified only if new repository evidence
contradicts or reopens one of the reconciled boundaries, for example:

- endpoint-owned measurements begin appearing as host-owned facts without an
  explicit authority boundary;
- a new or existing repository concept claims that history alone creates
  `should continue`;
- a view, lens, policy, or decision path collapses accepted baseline into
  expectation without separate should-bearing authority;
- concern is treated as alerting, remediation, or execution authority without an
  intervening authority decision;
- new evidence shows that the node116 example cannot be explained by the
  observation/visibility/continuity/comparison-reference/concern progression.

Reopening would also be justified if the repository deliberately chooses to make
one of the remaining gaps part of architecture rather than implementation or
policy, such as recording concern as a first-class repository concept. That
would be a new scoped architecture question, not continuation of the original
storage-empty investigation.

## Future work that should not reopen this branch

The following work should not reopen this branch if it preserves the reconciled
boundaries:

- Storage Lens work that shows endpoint-visible filesystem measurements with
  provenance and caveats;
- Node Detail work that distinguishes direct host facts from related endpoint
  visibility;
- Availability Lens work that preserves endpoint, host, and service scope;
- topology surfaces that show observed visibility or selected comparison
  references without relabeling them as ownership or expectation;
- Storage Lens, Node Detail, HomeOps, or Availability Lens implementation work
  that uses the branch findings rather than revisiting them;
- policy work that explicitly defines who may declare expectations;
- continuity-query implementation work;
- handoff/current-work work that preserves selected comparison references and
  authority trails.

Such work may need its own scoped design or implementation decisions, but it
should consume this branch's findings rather than reopen the investigation.

## Conclusion

The answer to the closure question is:

```text
Yes: the investigation branch answered the original operator pain at the
conceptual architecture level.
```

What was learned:

```text
Storage appeared empty because endpoint-owned measurements, host identity,
alias-like knowledge, and bounded summaries have different authorities.
The node116 mount-loss pressure is best explained as visibility loss over time,
not as implicit ownership.
Historical continuity can support a candidate comparison reference.
Authorized selection can make that reference an accepted baseline for a scope.
Concern can arise from deviation from such a reference without first asserting
that the condition should continue.
Expectation, alerting, and remediation require additional authority.
```

The unresolved architectural question is not the original branch question. The
remaining architecture question, if pursued later, is whether Seed should record
continuity, selected comparison references, expectations, or concerns as
first-class repository structures, and under which existing authority patterns.
That question should be opened separately only when repository authority requires
it.
