# Book of Seed

The Book of Seed preserves the durable constitutional grammar needed to interpret Seed. It names bounded concepts, keeps important non-equivalences visible, and offers a few representative repository anchors.

It is not a roadmap, API reference, generated topology, complete inventory, or substitute for repository inspection. Existing implementation and tests are Evidence of current practice; they do not carry constitutional Authority by identity. Historical audits and roadmaps are records outside active law.

## Resolution model

- A **Chapter** concerns one bounded concept, Responsibility, distinction, constraint, or relation.
- `[UNRESOLVED]` marks a question for which the current repository does not safely support a constitutional resolution.
- Representative anchors are illustrative. Seed must inspect the repository for current responsible occurrences, exact Acts, fields, topology, discrepancies, and residue.

The [concordance](concordance.md) is a navigation aid, not an ontology.

[`grammar.json`](grammar.json) carries machine-readable clause coordinates used
by tests. Tests validate that grammar rather than freezing explanatory prose.
The Markdown chapters explain and orient the same clauses.

## Responsibility

1. Responsibility is the Book's representation and traversal root for reading each exact responsibility and the branches it instantiates.
2. The headings beneath it expose coordinates and relations; they do not change Responsibility assignments.
3. Every instantiated responsibility must expose the branches required by that responsibility.
4. A conditional branch remains uninstantiated until a responsible occurrence supplies its coordinate.
5. An instantiated coordinate whose value has not been resolved remains unresolved unless a responsible occurrence carries Unknown Standing for it.
6. Recurrence, headings, adjacency, implementation shape, or plausible completion supply neither a branch value nor its identity.

### Required identifying branches

#### Responsible boundary

Identifies who bears and answers for the exact responsibility. It is distinct from the subject addressed, the responsible occurrence, the exact Act, and any separately assigned Standing boundary.

#### Subject or material addressed

Identifies what the Responsibility concerns, evaluates, forms, preserves, or stops. Responsible-boundary identity does not supply subject identity.

#### Exact responsible act

Identifies the exact constitutional act assigned to the responsibility. Responsibility identity does not by itself establish that the act occurred.

#### Authority

Identifies the exact Authority under which the responsible boundary may bear and perform the exact act.

```text
Authority
!= separate Authorization standing
!= responsible-boundary identity
!= locality
!= admission
!= Authority carried by an input
```

The Authority coordinate may be positively established, conflicting, responsibly Unknown, or unresolved. Absence of a separate Authorization standing does not answer the Authority coordinate.

#### Evidence

Identifies the Evidence supporting the exact Responsibility, Act, occurrence, result, Standing, or relation asserted. Evidence does not establish Authority, a support relation, occurrence, or Standing by identity.

#### Scope and locality

Preserve the bounded extent and place within which the Responsibility, exact Act, subject, and result apply. They do not establish Authority.

### Conditional input branches

These branches are required where material participates in the exact Responsibility's Act.

#### Input source

Identifies where the exact input material came from. Source does not establish provenance by itself.

#### Provenance

Identifies the source, preservation, and occurrence history required by the exact use. Source and provenance remain distinct.

### Conditional support-relation branches

Where a Responsibility uses a substantive Assertion as support, the exact relation “these Evidence, Authority, Scope, provenance, and limits support this Assertion” is another Assertion. Its participants, responsible Act, occurrence, Evidence, Authority, Scope, conflicts, limits, Unknowns, and Standing remain independently recoverable. Nearby coordinates, reference presence, or adjacency do not supply that relation.

Support-relation Standing does not establish the supported Assertion's Standing, Applicability, Admission, or a later input-to-result support relation. Each requires its own responsible occurrence.

### Act-occurrence and non-occurrence branches

These branches apply where the exact act occurs, including a failed act occurrence; or where a separate responsible occurrence establishes that the proposed act did not occur.

#### Act occurrence

Identifies the responsible occurrence at which the exact act happens. A failed act may still be an act occurrence. No act occurrence exists merely because a later responsibility finds that the proposed act did not occur.

```text
act
!= act occurrence
```

#### Absence-of-act-occurrence finding

Identifies the separately responsible occurrence and result that establish that the proposed exact Act did not occur. The finding is not the absent Act's occurrence. It may itself be a lawful result under its own Responsibility, Evidence, Authority, Scope, and established support relations.

```text
absence-of-act-occurrence finding
!= act occurrence

absence finding
!= lawful Stop by identity

absence finding
!= failure by identity
```

#### Occurrence or non-occurrence evidence

Identifies the evidence supporting the exact act-occurrence Assertion, failed-act-occurrence Assertion, or absence-of-act-occurrence finding. An absence-of-act-occurrence finding must not fabricate the absent act's result.

### Result branches

These branches apply where the exact Act occurrence establishes or preserves a result. Publicly callable code, direct instantiation, constructability, and a returned shape do not establish the Act, its Authority, its occurrence, or its relation to the result.

#### Occurrence-result Evidence

Identifies the Evidence that the exact Act occurrence established or preserved the exact result. Result existence and equal shape do not establish that relation.

```text
same-shaped result
!= same Act occurrence-to-result relation

Act occurrence
!= Standing occurrence
```

#### Result

Identifies the exact result established or preserved by the Act occurrence.

```text
result
!= result standing
```

### Standing branches

These branches apply where Standing is established for a result, relation, Assertion, or other bounded subject.

#### Standing responsible boundary

Identifies the responsible boundary that establishes the Standing. It may be the result's Act boundary or a separately assigned Responsibility; identity must be established.

#### Standing occurrence

Identifies the exact occurrence that establishes the standing.

```text
Act occurrence
!= Standing occurrence
```

#### Standing-occurrence evidence

Identifies the Evidence supporting the Standing occurrence. Representation existence, a representation Act, recording, or visibility does not establish Standing by identity.

#### Standing

Identifies the exact standing established for the exact result, relation, assertion, input-to-act relation, or other bounded subject.

Where the subject is a result, this is result standing.

Where the subject is not a result, the standing retains the exact identity of its own subject and must not be renamed result standing.

```text
result
!= established standing by identity

subject existence
!= standing established

Standing occurrence
!= Act occurrence by identity
```

### Conditional preservation, standing, and neighboring branches

These branches are exposed only where the exact responsibility instantiates them. Some may precede the act, govern it, preserve its occurrence, or belong to a later exact Act. Each retains its exact constitutional grammar.

#### Preservation record

Identifies any separately retained representation or record preserving an Act, Standing occurrence, support relation, result, or other occurrence. A preservation record does not prove the preserved occurrence by identity.

#### Separate Authorization standing

Identifies any separately established Authorization input by the exact downstream act. It remains distinct from the responsibility's general Authority coordinate.

#### Applicability and admission standing

Identifies any act-local applicability or admission standing required before material may participate in the downstream act. Applicability, admission, participation, and input support remain distinct.

#### Constraint

Constraint is an independently bounded constitutional subject that may govern the exact proposed act, material, or responsibility. It is not reclassified as a relation merely because it governs another responsibility. A Constraint governing an Act does not assign that Constraint to the Act's Responsibility.

```text
Constraint
!= relation by identity
```

#### Lawful Stopping

Where a stopping occurrence carries a lawful Stop result, preserve separately the responsible boundary, stopping Act, stopping occurrence, and bounded Stop result. Identity among those coordinates must not be inferred. It is not reclassified as a relation merely because it connects a reason-bearing responsibility to the exact Act addressed by the Stop. Absence of movement, unresolved material, negative Standing, or a preventing condition does not supply a Stop by identity.

```text
absence of movement
!= Stop

unresolved material
!= Stop

negative standing
!= Stop

preventing condition
!= Stop

Stopping
!= relation by identity
```

The Responsibility hierarchy is the Book's representation and traversal structure. It does not create a new constitutional kind, change Responsibility assignments, require one universal populated shape, or replace the exact grammar of the chapters.

```text
structural branch present != branch value established
coordinate unresolved != coordinate Unknown
same responsible boundary != same act, responsible occurrence, Standing boundary, or exact Act
same occurrence != same Assertion
```

## Maintenance rule

> Maintain the constitutional grammar.  
> Let Seed inspect the current implementation and emit only bounded results supported by that inspection's Evidence.

Change the Book when constitutional grammar, a durable distinction, or the status of an unresolved constitutional question changes. Do not update it merely because a function moves, a field is added, a pipeline is rewired, or a new diagnostic projects the same grammar.

## Chapters

- [Source coordinates and grammar](chapters/01-source-coordinates-and-grammar.md)
- [Constitutional Standing](chapters/02-constitutional-standing.md)
- [Acts and occurrences](chapters/03-acts-and-occurrences.md)
- [Constraints and preconditions](chapters/04-constraints-and-preconditions.md)
- [Selection and Selection Acts](chapters/05-selection-and-selection-acts.md)
- [Movement coordinates](chapters/06-movement-coordinates.md)
- [Result boundaries and movement](chapters/07-result-boundaries-and-movement.md)
- [Selection and Authorization](chapters/08-selection-and-authorization.md)
- [Assertion source coordinates and Standing](chapters/09-assertion-source-coordinates-and-standing.md)
- [Evidence and provenance](chapters/10-evidence-provenance-and-explanation.md)
- [Recording and preserved Assertions](chapters/11-recording-and-preserved-assertions.md)
- [Events and Standing](chapters/12-events-and-standing.md)
- [Authority Scope](chapters/13-authority-scope.md)
- [Representation, emission, and locality](chapters/14-representation-emission-and-locality.md)
- [Stopping and completion](chapters/15-stopping-and-completion.md)
