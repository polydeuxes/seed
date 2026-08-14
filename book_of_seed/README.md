# Book of Seed

The Book of Seed preserves the durable constitutional grammar needed to interpret Seed. It names bounded concepts, keeps important non-equivalences visible, offers a few representative repository anchors, and records questions that remain constitutionally unsettled.

It is not a roadmap, API reference, generated topology, complete inventory, or substitute for repository inspection. Existing implementation and tests are Evidence of current practice, not automatic constitutional Authority. Historical audits and roadmaps are attributed records only.

## Resolution model

- A **Book** is a major constitutional district, family, or kind.
- A **Chapter** concerns one bounded concept, responsibility, distinction, constraint, relationship, or unresolved constitutional question.
- `[UNRESOLVED]` marks a question for which the current repository does not safely support a constitutional resolution.
- Representative anchors are illustrative. Seed must inspect the repository to recover current responsible occurrences, exact Acts, fields, topology, discrepancies, and residue.

The first pass deliberately favors concise distinctions over comprehensive prose. The [concordance](concordance.md) is a navigation aid, not an ontology. Cross-cutting questions without a stable chapter home live in [unresolved.md](unresolved.md).

[`grammar.json`](grammar.json) carries machine-readable clause coordinates used
by tests. Tests validate that grammar rather than freezing explanatory prose.
The Markdown Books explain and orient the same clauses.

Book numbers are stable citation addresses only. They do not prescribe reading order, dependency order, constitutional sequence, or implementation movement.

Book VII is intentionally absent. Its former implementation topic collection was excised after its surviving constitutional distinctions were relocated to their owning Books; the bounded disposition is recorded in [Book VII Implementation Topic Collection Excision 001](book_vii_operational_topic_collection_excision_001.md).

## Responsibility

1. Responsibility is the Book's presentation and traversal root for reading each exact responsibility and the branches it instantiates.
2. The headings beneath it expose coordinates and relations; they do not reassign constitutional ownership.
3. Every instantiated responsibility must expose the branches required by that responsibility.
4. A conditional branch remains uninstantiated where that responsibility does not establish the coordinate.
5. An instantiated coordinate whose value has not been resolved remains unresolved unless a responsible occurrence positively establishes Unknown.
6. Recurrence, headings, adjacency, implementation shape, or plausible completion do not establish a branch value or identity.

### Required identifying branches

#### Owner / responsible boundary

Identifies who bears and answers for the exact responsibility. It is distinct from the subject addressed, the responsible occurrence, the exact Act, and any separately assigned establishment boundary.

#### Subject or material addressed

Identifies what the responsibility concerns, consumes, evaluates, forms, preserves, establishes, or stops. Owner identity does not establish subject identity.

#### Exact responsible act

Identifies the exact constitutional act assigned to the responsibility. Responsibility identity does not by itself establish that the act occurred.

#### Authority

Identifies the exact Authority under which the responsible boundary may bear and perform the exact act.

```text
Authority
!= separate Authorization standing
!= owner identity
!= locality
!= admission
!= Authority carried by an input
```

The Authority coordinate may be positively established, conflicting, responsibly Unknown, or unresolved. Absence of a separate Authorization standing does not answer the Authority coordinate.

#### Evidence

Identifies the Evidence supporting the exact Responsibility, Act, occurrence, result, Standing, or relation claimed. Evidence does not establish Authority, a support relation, occurrence, or Standing by identity.

#### Scope and locality

Preserve the bounded extent and place within which the Responsibility, exact Act, subject, and result apply. They do not establish Authority.

### Conditional input branches

These branches are required where the exact responsibility consumes input material.

#### Input source

Identifies where the exact consumed material came from. Source does not establish provenance by itself.

#### Provenance

Identifies the attributed source, preservation, and occurrence history required by the exact use. Source and provenance remain distinct.

### Conditional support-relation branches

Where a Responsibility relies upon or establishes a substantive Assertion, the exact relation “these Evidence, Authority, Scope, provenance, and limits support this Assertion” is another Assertion. Its participants, responsible Act, occurrence, Evidence, Authority, Scope, conflicts, limits, Unknowns, and Standing remain independently recoverable. Nearby coordinates, reference presence, or adjacency do not establish that relation.

Support-relation Standing does not establish the supported Assertion's Standing, Applicability, Admission, or later reliance. Each requires its own responsible occurrence.

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
!= lawful Stop automatically

absence finding
!= failure automatically
```

#### Occurrence or non-occurrence evidence

Identifies the evidence supporting the exact act-occurrence claim, failed-act-occurrence claim, or absence-of-act-occurrence finding. An absence-of-act-occurrence finding must not fabricate the absent act's result.

### Result branches

These branches apply where the exact Act occurrence establishes or preserves a result. Publicly callable code, direct instantiation, constructability, and a returned shape do not establish the Act, its Authority, its occurrence, or its relation to the result.

#### Occurrence-result Evidence

Identifies the Evidence that the exact Act occurrence established or preserved the exact result. Result existence and equal shape do not establish that relation.

```text
same-shaped result
!= same Act occurrence-to-result relation

Act occurrence
!= Standing-establishment occurrence
```

#### Result

Identifies the exact result established or preserved by the Act occurrence.

```text
result
!= result standing
```

### Standing-establishment branches

These branches apply where standing is claimed for a result, relation, assertion, or other bounded subject.

#### Standing-establishment boundary

Identifies the responsible boundary that establishes the claimed Standing. It may be the result's Act boundary or a separately assigned Responsibility; identity must be established.

#### Standing-establishment occurrence

Identifies the exact occurrence that establishes the standing.

```text
Act occurrence
!= standing-establishment occurrence
```

#### Standing-occurrence evidence

Identifies the evidence warranting the standing-establishment occurrence. Artifact existence, construction, recording, projection, or visibility does not establish standing by identity.

#### Established standing

Identifies the exact standing established for the exact result, relation, assertion, input-to-act relation, or other bounded subject.

Where the subject is a result, this is result standing.

Where the subject is not a result, the standing retains the exact identity of its own subject and must not be renamed result standing.

```text
result
!= established standing automatically

subject existence
!= standing established

standing-establishment occurrence
!= Act occurrence automatically
```

### Conditional preservation, standing, and neighboring branches

These branches are exposed only where the exact responsibility instantiates them. Some may precede the act, govern it, preserve its occurrence, or belong to a later exact Act. They remain governed by their independently owned constitutional grammar.

#### Preservation record

Identifies any separately retained representation or record preserving an Act, Standing establishment, support relation, result, or other occurrence. A preservation record does not prove the preserved occurrence by identity.

#### Separate Authorization standing

Identifies any separately established Authorization consumed by the exact downstream act. It remains distinct from the responsibility's general Authority coordinate.

#### Applicability and admission standing

Identifies any act-local applicability or admission standing required before material may participate in the downstream act. Applicability, admission, consumption, and reliance remain distinct.

#### Constraint

Constraint is an independently owned constitutional subject that may govern the exact proposed act, material, or responsibility. It is not reclassified as a relation merely because it governs another responsibility. Responsibility does not own the Constraint merely because the Constraint governs its act.

```text
Constraint
!= relation by identity
```

#### Lawful Stopping

Where the exact responsibility establishes lawful Stopping, preserve separately the responsible owner, stopping act, stopping occurrence, and bounded Stop result. Identity among those coordinates must not be inferred. It is not reclassified as a relation merely because it connects a reason-forming responsibility to the exact act for which Stopping is established. Absence of movement, unresolved material, a negative standing, or a preventing condition does not establish a Stop by identity.

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

The Responsibility hierarchy is a Book-root presentation and traversal structure. It does not create a new constitutional kind, reassign ownership among existing constitutional subjects, require one universal populated shape, or replace the exact grammar of the numbered Books.

```text
structural branch present != branch value established
coordinate unresolved != coordinate Unknown
same owner != same act, responsible occurrence, establishment boundary, or exact Act
same occurrence != same claim
```

## Maintenance rule

> Maintain the constitutional grammar.  
> Let Seed recover and project the current implementation.

Change the Book when constitutional grammar, a durable distinction, or the status of an unresolved constitutional question changes. Do not update it merely because a function moves, a field is added, a pipeline is rewired, or a new diagnostic projects the same grammar.

## Books

1. [Grammar and Standing](01-grammar-and-standing/)
2. [Acts and Constraints](02-acts-and-constraints/)
3. [Movement and Selection](03-goals-and-advancement/)
4. [Inquiry](04-inquiry/)
5. [Evidence and Provenance](05-evidence-and-knowledge/)
6. [Standing and Locality](06-standing-and-projection/)
7. **Intentionally absent** — see [Book VII Implementation Topic Collection Excision 001](book_vii_operational_topic_collection_excision_001.md).
8. [Authority, Emission, and Stopping](08-authority-communication-and-stopping/)
