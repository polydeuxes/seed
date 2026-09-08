# Answer Responsibility Implementation Characterization

## Question

This investigation asks what recurring implementation shapes produce strong
bounded answer responsibility in existing Seed surfaces. It does not propose an
`AnswerInventory`, an answer schema, a metadata registry, runtime registration,
or a new visibility system.

The bounded conclusion is:

> Seed's strongest answer-responsible surfaces are not unified by declarations.
> They are unified by implementation shapes that build a bounded view from
> existing authorities, perform explicit answer-shaping work, preserve what is
> unknown or not inferable, and render an authority boundary. Several families of
> this shape exist: composition, orientation/matching, aggregation/integrity,
> navigation, derivation audit, and selection audit.

## Evidence reviewed

Implementation evidence reviewed:

- `seed_runtime/operational_story.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- Corresponding tests under `tests/` for the above surfaces.

Prior investigation evidence reviewed:

- `answer_responsibility_auditability_investigation.md`
- `bounded_answer_responsibility_investigation.md`
- `docs/answer_composition_self_knowledge_investigation.md`
- `observation_model_implementation_audit.md`

Repository authority wins over the terminology in these investigations. The
implementation patterns below are therefore phrased as implementation shapes,
not as new declarations.

## Recurring implementation shapes

### 1. Bounded view object shape

Strong answer-responsible surfaces usually define a small immutable view object
or summary object whose fields are already the answer boundary. The object is not
just a transport record; it encodes the parts of the bounded answer that the
builder is allowed to produce.

Examples:

- Operational Story uses an immutable `OperationalStory` dataclass with answer
  fields such as focus, pressure, evidence, investigation path, recent changes,
  outcomes, unknowns, consumed surfaces, and boundary metadata.
- Inquiry Orientation uses immutable records for the preserved inquiry note,
  related material, and final orientation view. Its view includes note text,
  related facts, related source navigation, uncertainty, and authority boundary.
- Projection Integrity Summary uses an immutable summary dataclass containing
  aggregate counts and caveats.
- Source Navigation uses immutable row and view dataclasses for one query.
- Reasoning Path Audit and Selection Path Audit use immutable audit dataclasses
  with evidence, conclusions/candidates, unknowns, and boundary data.

This shape is weaker or absent in mechanical-only surfaces. Diagnostic Inventory
also has an immutable entry dataclass, but its fields describe mechanical surface
properties such as CLI flags, JSON support, recording scope, and mutation
boundary. The view object is about surface contract inventory, not a bounded
semantic answer. Projection Shape has immutable stage-shape rows, but those rows
characterize projection stages rather than answer composition.

### 2. Builder-over-existing-authorities shape

Strong answer-responsible surfaces have a builder that consumes already-existing
authorities and composes an answer without creating new cluster truth.

Recurring forms:

- composition from multiple implemented diagnostics and read models;
- lexical or predicate matching over preserved facts;
- aggregation over projected integrity signals;
- derivation from implemented pressure, capability, ownership, story, or state
  evidence;
- selection explanation from an already-ordered candidate source.

Operational Story is the strongest composition example: its builder consumes
pressure audit, capability needs, privilege discovery, correlation audit, impact
audit, and investigation-path evidence, then returns a story with explicit
`consumed_surfaces` and read-only boundary metadata.

Inquiry Orientation is a matching/orientation example: its builder consumes a
preserved inquiry note and projected state/support material, then finds related
material by deterministic token overlap instead of promoting the note into a
fact, goal, or intent.

Projection Integrity Summary is an aggregation example: its builder composes
counts from current state, contradiction input, graph validation, evidence
support, and capability inventory, then returns caveated aggregate integrity
counts.

Source Navigation is a navigation example: its builder consumes projected source
facts only, filters by query, sorts matching definitions/imports, and returns a
bounded navigation view.

Reasoning Path Audit is a derivation-audit example: its builder consumes
ownership discrepancies, capability needs, pressure audit, Operational Story,
projected state, and repository context, then builds evidence rows,
intermediate conclusions, derived conclusions, consumers, and unknowns.

Selection Path Audit is a selection-audit example: its builder consumes pressure
audit and Operational Story, then explains current-focus or primary-pressure
selection, selected candidate, non-selected candidates, evidence, outcome, and
unknowns.

Mechanical-only contrast: Diagnostic Inventory consumes no semantic authorities
for a target answer. It enumerates declared diagnostic surface properties.
Diagnostic Shape Audit consumes inventory entries and implementation specs, then
checks whether mechanical declarations match implementation markers. Projection
Shape consumes no live semantic evidence; it renders a static projection-stage
shape table.

### 3. Answer-shaping logic shape

Strong answer responsibility appears when a builder performs visible shaping work
that narrows the answer target. The shaping logic differs by family, but the
presence of such logic recurs.

Observed shaping forms:

| Family | Recurring shaping logic |
| --- | --- |
| Composition | Choose current focus or primary pressure, map multiple surfaces into story fields, attach support and path hints. |
| Orientation/matching | Normalize tokens, compute overlap, deduplicate related material, cap related source rows. |
| Aggregation/integrity | Count entities, count validation and support states, count capability states, attach default caveats. |
| Navigation | Normalize query, match predicates and symbols/paths, sort rows, limit rendered support summaries. |
| Derivation audit | Match subject/domain, build evidence rows, derive intermediate and capability conclusions, deduplicate consumers. |
| Selection audit | Normalize target, preserve candidate ordering, identify selected/non-selected candidates, explain selection factors. |

Mechanical-only surfaces can contain logic, but it is mechanical comparison or
listing logic rather than bounded answer shaping. Diagnostic Shape Audit compares
expected fields to observed implementation markers and assigns statuses. That is
audit mechanics, not a semantic answer family. Diagnostic Inventory formats
entries. Projection Shape renders stage metadata.

### 4. Unknown, caveat, and negative-authority shape

Strong answer-responsible surfaces usually preserve limits inside the returned
view or formatter. This is not merely prose polish; it prevents missing evidence
from silently becoming an answer.

Recurring elements:

- `unknowns` collections in Operational Story, Reasoning Path Audit, and
  Selection Path Audit;
- `caveats` in Projection Integrity Summary;
- no-match and uncertainty text in Inquiry Orientation and Source Navigation;
- authority-boundary text that refuses promotion, inference, repair, mutation,
  execution, or broader truth claims.

The implementation strength varies. Projection Integrity Summary's caveats are
first-class data on the summary object. Operational Story and the two audit
surfaces carry `unknowns` as structured fields. Inquiry Orientation's authority
boundary and uncertainty are constants on the view. Source Navigation's negative
authority is strong in module and formatter behavior, but less structured than
Operational Story's or Projection Integrity Summary's boundary fields.

Mechanical-only contrast: Diagnostic Inventory and Projection Shape also expose
read-only and mutation boundaries, but those boundaries primarily protect
operation mechanics. They do not preserve semantic non-inference about a bounded
answer target. Diagnostic Shape Audit has an `unknown` status, but that means the
audit cannot classify a mechanical property, not that a semantic answer contains
unknown evidence.

### 5. Formatter boundary-section shape

Strong answer-responsible surfaces typically render named sections that mirror
the answer structure and then close with an explicit boundary.

Recurring rendered sections include:

- selected/focus or target;
- evidence or related material;
- candidates, non-selected candidates, conclusions, or aggregate counts;
- unknowns/caveats/uncertainty;
- authority boundary.

This matters because formatter text alone can create the appearance of answer
responsibility. The stronger pattern is formatter sections backed by structured
builder output. A formatter that only appends authoritative-sounding text without
corresponding builder fields would be a weak counterexample.

Source Navigation is the main caution case: a compact formatter says no facts
matched and names source-fact boundaries. That is legitimate for the narrow
navigation family because the builder also performs predicate-bound matching and
sorting over source facts. It would be insufficient evidence for broad answer
responsibility outside that narrow family.

## Strong patterns by surface

### Operational Story: composition shape

Operational Story is the strongest current answer-responsible family. Its shape
is:

1. collect multiple read-only diagnostic/read-model authorities;
2. select a focus from pressure evidence;
3. map authority outputs into a coherent narrative view;
4. retain unknowns for missing pressure or impact evidence;
5. preserve consumed-surface names and read-only boundary metadata;
6. render the story with sections and an authority boundary.

This is answer responsibility as multi-authority composition. It is not a schema
or registry pattern.

### Inquiry Orientation: orientation/matching shape

Inquiry Orientation is answer-responsible for a narrower question: what existing
projected material is deterministically related to preserved operator prose?
Its shape is:

1. preserve the note as isolated operator prose;
2. tokenize and normalize note terms;
3. match against projected supports and source navigation evidence;
4. keep related material bounded and deduplicated;
5. state uncertainty and refuse semantic promotion.

The answer is strong for related-material orientation, but intentionally does
not claim intent, importance, plan, fact, command, or goal.

### Projection Integrity Summary: aggregation/integrity shape

Projection Integrity Summary is answer-responsible for aggregate integrity
signals. Its shape is:

1. consume existing projected integrity inputs;
2. aggregate counts deterministically;
3. preserve caveats as returned data;
4. refuse truth, health, repair, execution, or mutation authority.

This family shows that strong answer responsibility can be produced by
aggregation rather than narrative composition.

### Source Navigation: navigation shape

Source Navigation is answer-responsible for a narrow source-origin lookup. Its
shape is:

1. consume preserved `defines` and `imports` facts from projected state;
2. normalize the query;
3. match by subject/path/symbol/final segment;
4. sort and render matching rows;
5. explicitly avoid parsing files or inferring behavior/reachability.

It is strong only within that narrow source-fact boundary. It is partial if the
expected answer is broader source understanding.

### Reasoning Path Audit: derivation-audit shape

Reasoning Path Audit is answer-responsible for explaining implemented derivation
paths. Its shape is:

1. consume ownership, capability, pressure, story, state, and repository context;
2. match a requested subject/domain;
3. construct evidence rows;
4. derive intermediate and capability conclusions;
5. attach consumers and story impact;
6. preserve unknowns when the requested path cannot be fully supported.

It demonstrates an answer family where the answer is not the operational fact
itself, but the implemented path by which the repository arrived at that kind of
conclusion.

### Selection Path Audit: selection-audit shape

Selection Path Audit is answer-responsible for explaining implemented selection,
especially current focus and primary pressure. Its shape is:

1. consume pressure ordering and Operational Story focus;
2. normalize the requested target;
3. expose selected candidate;
4. expose candidate set and non-selected candidates;
5. explain selection factors;
6. preserve unknowns for unsupported or empty candidate contexts.

It is partial where the selected object is not one of the supported target
families or where candidate sources are empty.

## Weak patterns and partial responsibility

The weaker answer-responsible cases are not weak because they lack all common
implementation structures. They are weak because the structures are narrower or
less semantic.

### Source Navigation weaker elements

- It has minimal structured uncertainty compared to Operational Story,
  Projection Integrity Summary, Reasoning Path Audit, and Selection Path Audit.
- Its authority boundary is strongest at the module/formatter level and through
  predicate-limited matching, not through a rich boundary object.
- It answers only preserved source-origin lookup. It does not explain ownership,
  behavior, runtime reachability, semantic importance, or architectural meaning.

### Selection Path Audit weaker elements

- It depends on the pressure audit's candidate ordering and Operational Story's
  focus rather than owning selection itself.
- It has strong responsibility for explaining implemented selection paths, but
  not for selecting new work or proving that the selected item is correct.
- Its unsupported-target branch preserves unknowns, which is a strength, but it
  also shows the boundedness of the family.

### Formatter-only risk

Formatter text can make a surface look answer-responsible even when the builder
only lists records. The repository evidence does not support treating formatter
vocabulary alone as an implementation shape. The implementation-backed pattern
requires structured builder output plus boundary-preserving rendering.

## Mechanical-only contrasts

### Diagnostic Inventory

Diagnostic Inventory is strong self-knowledge about operational surfaces. It
tracks whether a diagnostic supports JSON, supports record, reads state, reads
repo files, reads diagnostic facts, writes events, mutates cluster state, and
which CLI flags expose it.

It lacks answer-responsible implementation structures because:

- it does not consume semantic authorities for a bounded operator question;
- it does not perform answer-family shaping such as composition, matching,
  aggregation, selection, navigation, or derivation;
- its boundaries protect diagnostic mechanics rather than preserving semantic
  unknowns or refusing semantic inference;
- its entries are declarations of surface mechanics, not a built answer over
  evidence.

### Diagnostic Shape Audit

Diagnostic Shape Audit audits whether Diagnostic Inventory declarations match
implementation evidence. It is implementation-backed and important, but it is
mechanical-only for answer responsibility.

It lacks answer-responsible implementation structures because:

- its target is consistency between inventory fields and implementation markers;
- its statuses are mechanical audit statuses, not answer caveats;
- its unknowns mean missing mechanical evidence, not unresolved semantic evidence;
- it does not own a bounded semantic answer beyond diagnostic shape consistency.

### Projection Shape

Projection Shape exposes projection-stage structure, authority boundaries, and
read-only/mutation boundaries. It is stronger than a plain formatter because it
has stage rows with consumes, produces, influences, non-influences, and authority
boundaries.

It remains mechanical/structural rather than answer-responsible because:

- its rows are static projection-stage shape descriptions;
- it does not compose a semantic answer from current evidence;
- it does not select, match, aggregate current integrity, derive conclusions, or
  explain a candidate decision;
- its unknown handling is stage-shape vocabulary rather than unresolved evidence
  for a bounded answer.

## Counterexamples and cautions

### Strong surfaces do not share one single implementation family

Operational Story, Projection Integrity Summary, Source Navigation, Inquiry
Orientation, Reasoning Path Audit, and Selection Path Audit do not share one
uniform algorithm. The evidence supports multiple implementation families, not a
single answer-responsibility mechanism.

Supported families:

- composition shape;
- orientation/matching shape;
- aggregation/integrity shape;
- navigation shape;
- derivation-audit shape;
- selection-audit shape.

### Mechanical surfaces can look structurally similar

Diagnostic Inventory and Projection Shape both have dataclasses, formatters,
read-only boundaries, and authority vocabulary. Diagnostic Shape Audit has
builder logic and unknown statuses. These similarities are insufficient.

The missing piece is semantic answer-shaping over existing authorities. A
mechanical surface can be implementation-backed and bounded without owning answer
responsibility.

### Formatter text alone is not enough

A surface may render sections named `Unknowns`, `Boundary`, `Summary`, or
`Answer` without implementing answer responsibility. The supported pattern is the
combination of:

1. bounded structured view;
2. builder over implementation evidence;
3. shaping logic;
4. unknown/caveat/negative-authority preservation;
5. boundary rendering.

The formatter is the visible end of the shape, not the source of responsibility.

## Supported conclusions

1. Strong answer-responsible surfaces share recurring implementation shapes, but
   not a single implementation family.
2. The recurring shapes are visible in code without adding declarations, schemas,
   metadata registries, runtime registration, or a new inventory.
3. The common denominator is not surface type or vocabulary. It is a combination
   of bounded view object, builder-over-authorities, answer-shaping logic,
   unknown/caveat preservation, and explicit authority boundary.
4. Multiple implementation families can produce answer responsibility:
   composition, orientation/matching, aggregation/integrity, navigation,
   derivation audit, and selection audit.
5. Mechanical-only surfaces lack semantic answer-shaping even when they share
   dataclasses, formatters, boundaries, and audit logic.
6. Strong answer responsibility usually emerges from combinations of structures,
   not from one structure alone. Dataclasses alone, formatters alone, unknown
   statuses alone, and read-only boundaries alone are insufficient.
7. The best repository-native implementation model is:

   > answer-responsible surface = bounded read-only view built from existing
   > authorities by explicit shaping logic, with preserved uncertainty and an
   > authority boundary appropriate to its family.

## Unsupported conclusions

The implementation evidence does not support concluding that:

- Seed needs an `AnswerInventory`.
- Seed needs an `AnswerContract` schema.
- Seed needs a metadata registry or runtime registration for answer surfaces.
- All answer-responsible surfaces should use the same fields.
- All answer responsibility should be audited through Diagnostic Inventory.
- Formatter vocabulary alone establishes answer responsibility.
- Source Navigation owns broad source understanding beyond preserved source
  facts.
- Inquiry Orientation understands operator intent.
- Projection Integrity Summary decides truth, correctness, health, repair, or
  execution.
- Selection Path Audit performs selection rather than explaining implemented
  selection evidence.

## Recommended next step

Do not introduce a new answer registry or schema. The repository-native next step
is a small evidence-preserving characterization pass over one additional
implemented surface when needed:

1. identify its bounded view object, if any;
2. identify consumed authorities;
3. identify shaping logic;
4. identify unknown/caveat/negative-authority preservation;
5. identify whether formatter boundary text is backed by builder data;
6. classify it into an existing implementation family or mark it as a new family
   only if implementation evidence requires it.

This keeps the work in implementation characterization rather than architecture
proposal.

## Acceptance answers

### What implementation patterns recur across answer-responsible surfaces?

Bounded immutable view objects, builders over existing authorities,
answer-shaping logic, structured unknown/caveat or no-match preservation,
consumed-surface/evidence composition, and explicit authority-boundary rendering.

### What implementation patterns are absent from mechanical-only surfaces?

Mechanical-only surfaces lack semantic answer-shaping over existing authorities.
They may have dataclasses, formatters, read-only boundaries, and audit statuses,
but they do not compose, select, navigate, aggregate semantic evidence, or derive
bounded answer conclusions for an operator question.

### Do strong answer-responsible surfaces share common shapes?

Yes, at the combination level. They share bounded view + builder + shaping +
uncertainty/boundary preservation. They do not share one uniform algorithm or
field schema.

### Are there multiple answer-responsible implementation families?

Yes. The evidence supports composition, orientation/matching,
aggregation/integrity, navigation, derivation-audit, and selection-audit
families.

### Can answer responsibility be characterized from implementation shape alone?

Yes, conservatively. Implementation shape can characterize existing bounded
answer responsibility without new declarations, as long as the characterization
requires the combination of builder evidence, shaping logic, and boundaries—not
formatter vocabulary alone.

### What repository-native implementation model best explains the evidence?

Answer responsibility is an implementation shape: a read-only bounded view over
existing authorities, produced by explicit answer-shaping logic, preserving
unknowns/caveats/non-inference, and rendering an authority boundary. Surface
purpose and vocabulary may help locate candidates, but implementation evidence
wins.
