# Surviving operator-ingress material-role Fidelity recovery 001

## Boundary, method, and result

This is one bounded, report-only Fidelity recovery against merged `main` at
`3703914` (PR 2132).  It examines only the surviving operator-ingress role and
projection subject shape.  It changes no implementation, test, Book, Event,
payload, projection, State, CLI, name, or persisted representation.

The exact live road recovered is:

```text
run_persistent_operator_console
  -> capture_stdin_material(input_stream)
  -> CapturedOperatorMaterial
  -> run_operator_ingress_attempt(...)
  -> _capture_representation(..., material_role="initial_ingress")
  -> raw_material_captured Event
  -> examine_text_representation(...)
  -> representation_examined Event
  -> [failure: separately recorded stopping, not adjudicated here]
  -> [success: ingress_occurred Event]
  -> form_operator_ingress_addressable_material(...)
  -> OperatorIngressAddressableMaterial
  -> operator-ingress projection
```

The mixed verdict is **E**:

* Raw boundary bytes, the examination occurrence, and decoded ingress are
  faithful, distinct current subjects/occurrences.  Removing a singleton role
  must not collapse them.
* `material_role="initial_ingress"` is an application-declared singleton.  It
  retains historical explanatory testimony but no current alternative, branch,
  or independently established locality.  It is active but its current
  applicability as a role distinction is unestablished.
* The role-keyed `representation_examinations` map is singleton implementation
  organization in current production.  Exact Event identity and lineage retain
  all evidence that the role presently confirms.
* `raw_initial_material` faithfully points at the raw captured subject, but
  `initial` is not independently warranted by current evidence.  Its complete
  label is therefore **active but current applicability unestablished**, not a
  reason to merge the raw and decoded subjects.
* `preserved_ingress` is independently faithful: it identifies the distinct
  decoded ingress occurrence under projection-revised `preserved` standing.

This recovery does **not** decide interaction closure, stopping authority,
representation-insufficiency treatment, semantic consumption, common grammar,
Demand, BOGE, candidate production, candidate preservation semantics, or
projector-wide Event admission.

## Evidence corpus and recorded searches

### Current implementation and tests inspected

* `seed_runtime/operator_ingress.py` (producer, Events, projection)
* `seed_runtime/operator_ingress_representation.py` (capture and examination
  value subjects)
* `seed_runtime/operator_ingress_addressable_material.py` (lineage consumer and
  addressable artifact)
* `seed_runtime/operator_ingress_interpretation_candidates.py` (adjacent
  artifact-only downstream consumption)
* `seed_runtime/state.py` (State slot and projector dispatch)
* `scripts/seed_local.py` (persistent console and repeated attempt ownership)
* `tests/test_operator_ingress.py`
* `tests/test_operator_ingress_addressable_material.py`
* `tests/test_operator_ingress_interpretation_candidates.py`

The repository-wide live-code searches were recorded as:

```text
rg -n --hidden --glob '!.git/**' --glob '!*.md' \
  'material_role|initial_ingress|raw_initial_material|preserved_ingress|representation_examinations|addressable_operator_material' .

rg -n --hidden --glob '!.git/**' --glob '!*.md' \
  'OperatorIngressAddressableMaterial|operator_ingress_addressable_material' \
  seed_runtime scripts tests

rg -n -i 'operator.ingress|operator_ingress|raw_initial|representation_examin' \
  seed_runtime scripts tests | rg -i 'diagnostic|shape|inventory'
```

The first search found the named coordinates only in
`seed_runtime/operator_ingress.py`, the two exact role checks in
`seed_runtime/operator_ingress_addressable_material.py`, and the three test
files enumerated above.  The second found downstream production use of the
addressable artifact in `operator_ingress_interpretation_candidates.py`, not use
of any role or projection label.  The final search returned no diagnostic,
inventory, or shape-audit ownership of these names.  Markdown was excluded from
the consumer count so prior report testimony could not become a live consumer.

### Active Book authority inspected

The active Book was identified through `book_of_seed/README.md` and the exact
clauses used below were inspected in:

* `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
* `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
* `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
* `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`
* `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
* `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
* `book_of_seed/06-state-and-projection/events-facts-and-state.md`
* `book_of_seed/06-state-and-projection/projection-and-current-state.md`
* `book_of_seed/06-state-and-projection/ownership-discrepancy-and-residue.md`
* `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`
* `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`

The common-grammar prerequisite chapter was inspected only to avoid treating
its surviving constitutional distinctions as authority for the deleted
orchestration shape.  No old report, test, implementation comment, history, or
PR description is used as Book authority.

### Bounded history inspected

The bounded history commands were:

```text
git log --all --oneline -S'<symbol>' -- seed_runtime tests scripts
git show e50b3b0^:seed_runtime/operator_ingress_common_grammar_prerequisite.py
git show --stat --oneline e50b3b0 b085ef9 b2a13ac 4af5fc4 3703914
git show --unified=35 e50b3b0 -- seed_runtime/operator_ingress.py
```

Relevant testimony is commits `8f1718f` (#2035), `c28be17` (#2037), `e50b3b0`
(#2101), `754aae0` (#2111), `b085ef9` (#2127), `b2a13ac` (#2128), `ee30f96`
(#2130), `4af5fc4` (#2131), and `3703914` (#2132).  Immediately before
`e50b3b0`, the common-grammar attempt actively called `_capture_representation`
twice with roles `initial_ingress` and `enum_response`.  The projection
distinguished `raw_initial_material` from `raw_response_material`, and the same
role-keyed map held each capture's representation examination.  Commit
`e50b3b0` deleted the now-unreachable probe/response orchestration tail,
including the `enum_response` producer; `b085ef9` later removed the remaining
historical common-grammar projection surface.  The neutral ingress road retains
only the first capture shape.

Thus historical current-at-the-time role cardinality was **two** within one
common-grammar attempt: initial operator ingress and enum response.  The role
key and raw subject labels then prevented replacement between two materially
different capture/examination pairs.  The deleted response capture, response
examination, and `raw_response_material` consumer are the recovered alternatives.
History explains the current shape; it neither warrants current applicability
nor makes the singleton automatically invalid.

## Recovery A — exact active producers

`capture_stdin_material` reads exactly one framed occurrence and returns a
`CapturedOperatorMaterial`.  It declares no role.  It derives bytes, EOF,
delimiter, boundary, byte origin, encoding testimony, and known loss from the
stream boundary.  `run_persistent_operator_console` repeats that capture and
calls `run_operator_ingress_attempt` once per non-EOF, non-exit capture; the
session can therefore produce first, second, and later bounded attempts.

`run_operator_ingress_attempt` creates a fresh `operator_ingress_attempt` ID and
is the sole current production caller of `_capture_representation`.  At that
call it hard-codes `material_role="initial_ingress"`; no observation,
selection, decoder result, or responsibility chooses the value.
`_capture_representation` merely accepts and copies the parameter into both
Event payloads and interpolates it into the raw Event's dimensional scope.

### Table 1 — producer and consumer inventory

| coordinate or label | producer | producer evidence | consumer | consumer act | current cardinality | constitutional standing |
|---|---|---|---|---|---:|---|
| `material_role` on raw capture | `run_operator_ingress_attempt` -> `_capture_representation` | fixed literal at `operator_ingress.py:237`; copied at `:162-165` | addressable constructor; projector | exact equality; indirectly dictionary key through examination | 1 value per attempt, 1 production value globally | implementation-witnessed only; relation applicability unestablished |
| `material_role` on examination | `_capture_representation` copies same parameter | payload at `operator_ingress.py:198`, with capture lineage at `:199-210` | addressable constructor; projector | exact equality and dictionary key | 1 per current attempt | singleton implementation organization |
| `initial_ingress` | application call site | declared literal, not derived or selected | constructor compares raw and examination against it | compatibility/topology assertion plus redundant lineage confirmation | only current value | historical implementation testimony; current locality Unknown |
| `raw_initial_material` | `project_operator_ingress_events`'s fixed kind-to-slot table | raw Event kind maps unconditionally at `operator_ingress.py:49-50` | no production consumer beyond the view itself | presentation/projection storage; tests inspect | exactly 1 slot and at most 1 active capture per attempt | raw subject distinction faithful; `initial` qualifier unestablished |
| `preserved_ingress` | projector's fixed kind-to-slot table and standing rewrite | ingress kind maps at `:51`; `occurred` is rewritten to `preserved` at `:104-105` | projector uses slot during projection; addressable tests inspect; no downstream production lookup | projection of decoded occurrence under preservation standing | 0 on decode failure, exactly 1 on success | faithful current distinction |
| `representation_examinations` | projector initializes map and writes `map[payload.material_role]` | `operator_ingress.py:77,90-99` | no current production reader; tests index literal key | keyed storage/presentation | 1 entry per valid production attempt | singleton implementation organization |
| `addressable_operator_material` | projector calls `form_operator_ingress_addressable_material` for complete successful ingress payload | `operator_ingress.py:107-128` | interpretation-candidate preservation island consumes the artifact | validates intrinsic artifact and carries it; does not inspect role labels | 0 on failure, exactly 1 on success | faithful addressable decoded-material artifact |

The exact inputs, values, and responsibilities are:

* **Raw capture Event:** input is one `CapturedOperatorMaterial`, plus workspace,
  session, fresh attempt, and declared role.  Identity is a fresh
  `operator_material` ID; content is exact byte hex; standing is `captured`;
  source is the capture boundary; responsibility is
  `competent-raw-material-capture`; authority is occurrence evidence only;
  scope text is workspace/session/role; occurrence says exact boundary bytes are
  durably preserved.  The role is declared by the application, not derived.
* **Examination Event:** input is the same captured value and the result of
  `examine_text_representation`.  Identity is keyed to the capture Event ID;
  content is strict decoder examination; standing is the exact decoder outcome;
  source and scope identify the capture occurrence; responsibility is bounded
  representation-evidence production; authority is decoder-outcome evidence
  only; lineage contains the capture Event ID.  The role is copied without
  examination.
* **Ingress Event:** input is the represented text from the successful
  examination.  Identity is the attempt ID, content is delimiter-trimmed decoded
  text, standing is `occurred`, source is the examination Event, responsibility
  is operator ingress, authority is occurrence-only with meaning Unknown, and
  lineage is the exact raw/examination pair.  It has no `material_role` field.
* **Addressable artifact:** input is the recorded ingress occurrence plus the
  ledger.  Its exact material identity is the ingress Event ID; its provenance
  is raw, examination, ingress in that order; its full source span points to the
  ingress Event; its scope is workspace/session/attempt; its source role is
  “operator-origin material at the preserved ingress boundary.”  It is a new
  decoded-material representation, not the raw bytes renamed.

The producer claims only that the raw and examination Events occupy the
application's `initial_ingress` role.  The current code makes one capture before
any other work in each newly created bounded attempt, so each later console
attempt happens to receive the literal truthfully under **function-local ordinal
position**.  But the role coordinate itself says neither `attempt:<id>` nor
“first capture in this attempt”; the raw scope contains workspace, session, and
role, while attempt locality is carried separately by `attempt_ref`.  Therefore
the exact locality claimed by the word `initial` remains **Unknown**.  It is not
established as process-first, console-session-first, operator-first, or
capture-call-first, and its historical contrast was first material before the
removed enum response.

`raw_initial_material` comes solely from projector interpretation of Event kind;
the raw Event producer emits the role but no projection label.  `preserved_ingress`
also comes solely from projector interpretation, including a standing rewrite.
It contains the decoded ingress subject (attempt identity), not the raw capture
subject (operator-material identity) under a renamed standing.

## Recovery B — exact active consumers

No production consumer compares among more than one role value.  The only
production equality consumer is
`form_operator_ingress_addressable_material`, which requires both referenced
Events to equal `initial_ingress`.  The projector never branches on recognized
role values: it accepts the payload value as a dictionary key.  Tests assert
literal shape and refusal behavior but are witnesses, not authority.

The constructor uses the role primarily as an **application-topology assertion**
and compatibility check.  In the same compound checks it already requires:

* exact referenced raw and examination Event IDs from the ingress payload;
* exact Event kinds;
* the recorded ingress occurrence to equal the supplied occurrence;
* common workspace, session, and attempt;
* exact raw -> examination `capture_event_id`;
* successful decoded examination outcome;
* ingress lineage exactly `[raw_ref, examination_ref]`.

Those coordinates establish the exact current lineage without the role.  The
role is not the foreign-lineage defense: the ID, Event kind, common locality,
capture reference, and ordered lineage provide it.  It is redundant confirmation
that the application-produced pair came through the historically named lane.
The test that changes the raw role to `response` witnesses that this compatibility
check currently refuses; it does not demonstrate a second production role or
constitutional need.

The projector can hold more than one examination entry only if manually
recorded Events for the same attempt supply fabricated distinct role strings.
No active producer can create that case.  A repeated Event with the same role
replaces the entry in the role map even though `event_ids` and
`dimensional_standing[event.id]` preserve both occurrences.  Projector
permissiveness is relevant only as evidence that the map is not a validated role
taxonomy; projector-wide payload admission remains explicitly unresolved.

Neither `raw_initial_material` nor `preserved_ingress` is read by a current
production downstream consumer.  They are current view coordinates and are
asserted by tests.  `preserved_ingress` nevertheless expresses a distinct
constitutional standing faithfully because it projects the separately evidenced
decoded ingress occurrence.  The candidate-testimony preservation island takes
and validates `OperatorIngressAddressableMaterial`; it depends on its exact
material, provenance, scope, and intrinsic invariants, not the Event roles,
`raw_initial_material`, `preserved_ingress`, or the examination-map key.

Consumer classification:

| consumer | coordinate | classification | production behavior witnessed by tests |
|---|---|---|---|
| `project_operator_ingress_events` | `material_role` | uses as dictionary key without validation | examination projection is reachable under the literal; fabricated keys are mechanically admitted |
| `form_operator_ingress_addressable_material` | `material_role` / `initial_ingress` | validates exact equality after exact identity and lineage | altered role is refused even when copied IDs remain valid |
| projection itself | `raw_initial_material`, `preserved_ingress` | fixed presentation/storage slots | raw and ingress Events project into distinct slots; preserved standing is rewritten |
| tests | all named coordinates | validates exact equality/shape; presentation inspection | preserves current implementation shape, cardinality, lineage refusal, and subject separation; supplies no independent warrant |
| interpretation-candidate preservation | addressable artifact only | exact artifact validation/copy; labels ignored | downstream island preserves the artifact without examining role vocabulary |
| diagnostic inventory / shape audit | none | no consumer recovered | no required public diagnostic topology for these names |

## Recovery C — historical origin and bounded disposition

The recovered pre-deletion road had two raw materials in one attempt:

```text
initial ingress capture -> representation examination
presentation
enum response capture -> representation examination
```

`initial_ingress` and `enum_response` were both active values.
`raw_initial_material` contrasted directly with `raw_response_material`.
`representation_examinations[material_role]` prevented the second examination
from replacing the first.  The roles described each material's responsibility
in that interaction more than its identity: each capture and examination already
had an exact Event ID.

The probe/response orchestration, `enum_response` producer, response capture and
examination, and `raw_response_material` projection consumer were deleted.  No
surviving production road creates response or closed-choice material inside an
operator-ingress attempt.  The surviving role is therefore a historical
coordinate with one current declared value.  This is historical implementation
testimony, not Book warrant.  It explains both the word `initial` and the plural
map but does not establish their present applicability; conversely, deletion of
the alternative does not by itself invalidate the current literal.

## Recovery D — current constitutional subjects

### Subject-by-subject dimensional recovery

| subject | identity | content | standing | source or provenance | responsibility | authority or warrant | scope or locality | occurrence or preservation |
|---|---|---|---|---|---|---|---|---|
| `CapturedOperatorMaterial` | no durable ID in the value; later capture Event supplies one | exact bytes plus boundary metadata | captured value awaiting Event recording | stdin/binary/text-adapter boundary and known loss | smallest available boundary observation | value validation only; no interpretation | one `readline` frame; workspace/session absent | in-memory capture occurrence; Event makes it durable |
| `raw_material_captured` Event | fresh `operator_material:<id>` | exact bytes as hex plus capture metadata | `captured` | capture boundary; optional incoming lineage | competent raw-material capture | occurrence evidence only | workspace/session plus role text; attempt in payload | exact boundary bytes durably recorded |
| `RepresentationExamination` | no durable ID in value; Event identity later relates it to capture | mechanism, selection, outcome, represented text or failure | exact decoder outcome | `CapturedOperatorMaterial` | strict bounded decoder invocation | representation evidence, not encoding/meaning verdict | one capture | one in-memory decoder invocation |
| `representation_examined` Event | `representation-examination:<capture Event id>` | strict decoder examination plus outcome fields | decoded, decoder-unavailable, or bytes-rejected | exact capture Event ID and lineage | bounded representation-evidence production | decoder outcome evidence only | captured occurrence | separate decoder examination durably recorded |
| `ingress_occurred` Event | attempt ID | decoded text and ingress framing | `occurred` | raw + examination IDs in exact ordered lineage; direct source is examination | operator-ingress occurrence | occurrence only; meaning Unknown | workspace/session; attempt in payload | separate decoded-ingress occurrence durably recorded |
| `OperatorIngressAddressableMaterial` | stable projection ID; exact material ref is ingress Event ID | exact decoded text and one full source span | addressable, exact-material carriage only | ordered raw/examination/ingress provenance | addressable-material formation | addressability only; no interpretation or competency | exact workspace/session/attempt | immutable projection artifact; no ledger or cluster mutation |
| projected raw material | raw capture subject ID | copied raw Event dimensions | captured | raw capture Event | view formation | projection visibility only | attempt view | current slot evidenced by raw Event |
| projected preserved ingress | ingress subject/attempt ID | copied ingress dimensions | projector changes `occurred` to `preserved` | ingress Event | view formation | projection visibility only | attempt view | separately occurred ingress retained as current preserved standing |

### Table 2 — subject distinction matrix

| row | same or distinct identity | content | standing | provenance | scope | occurrence | what must not be collapsed |
|---|---|---|---|---|---|---|---|
| raw captured material | distinct `operator_material` identity | bytes/hex and boundary metadata | captured | capture boundary | framed capture in workspace/session/attempt context | capture then durable raw Event | bytes != decoded text; capture != examination |
| representation examination | distinct identity derived from capture Event | mechanism and exact outcome | decoder outcome evidence | exact capture ID | one captured occurrence | separate decoder invocation/Event | examination != capture and != decoded ingress |
| decoded ingress occurrence | distinct attempt identity | decoded, delimiter-normalized ingress content | occurred | ordered raw/examination lineage | workspace/session/attempt | separate ingress Event | representation availability != ingress occurrence |
| addressable operator material | new stable projection identity; inner material identifies ingress Event | exact decoded text plus source span | addressable carriage only | raw/examination/ingress | workspace/session/attempt | constructed from recorded ingress | artifact != raw bytes; addressability != interpretation |
| projected raw material | same raw subject represented by view | raw Event dimensions | captured | evidence Event ID | attempt projection | projection, not new capture | label != subject standing |
| projected preserved ingress | same decoded-ingress subject represented under revised projected standing; not raw identity | decoded ingress dimensions | preserved | evidence Event ID and retained lineage elsewhere | attempt projection | projection, not another ingress | preserved ingress != raw capture; preservation != occurrence |

Raw bytes and decoded ingress are distinct current subjects because they have
different identities, contents, responsible occurrences, authority, and
lineage position.  The examination is both an act occurrence and recorded
evidence with its own subject identity and outcome standing.  `ingress_occurred`
establishes a new decoded-ingress occurrence/subject sourced from representation
evidence; it does not revise the raw capture's identity.  The projection then
represents that ingress subject under `preserved` standing.

The Book does not prescribe `material_role`, a material-role taxonomy, any of
the five implementation names, or role-keyed storage.  It does require recovery
of applicable dimensional distinctions and faithful purpose-relative projection;
it permits omission of an inapplicable or redundant implementation coordinate
when retained evidence keeps the consumer-required distinctions.  It does not
itself command deletion or retention of this exact coordinate.  The cleanup
conclusion is a bounded Fidelity comparison between those clauses and current
implementation evidence, not a claim that the Book names a code edit.

### Mandatory Book-authority table

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
|---|---|---|---|
| Constitutional subjects and relations are examined through identity, content, standing, source/provenance, responsibility, authority/warrant, scope/locality, and occurrence/preservation. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.F — Dimensional characterization**: the eight listed macro-dimensional families. | Orientation for this exact subject recovery; local coordinates depend on subject, consumer, purpose, scope, and evidence. | No universal schema, fixed coordinate count, role taxonomy, or required `material_role` field. |
| Raw capture, examination, and decoded ingress may remain distinct when their responsible occurrences and standings differ. | `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`, **Bounded resolution**: an act is a bounded occurrence; evidence about an act is not the act, and outputs do not prove occurrence by identity. | Keeps the separately recorded capture, decoder examination, and ingress occurrences from being collapsed in this road. | Does not prescribe these Event kinds, IDs, payloads, or labels; does not decide stopping semantics. |
| Artifact names and shapes do not establish constitutional standing. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.C — Constructed behavior does not confer standing**: standing suggested by name/output/behavior still requires subject, producer, evidence, scope, authority, occurrence, limits, and boundary. | Governs conclusions about `raw_initial_material`, `preserved_ingress`, and the map shape. | Does not prove the labels wrong or require their deletion merely because they are implementation vocabulary. |
| The Book requires no operator-ingress material-role taxonomy. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.F**, especially “not mandatory fields or one universal artifact schema” and local-coordinate applicability; no operator-ingress role-taxonomy clause was recovered from the active Book. | Establishes that general dimensionality does not prescribe a universal coordinate; for an exact operator-ingress taxonomy the classification is **Unknown: no exact active Book authority recovered**. | Does not prohibit a locally warranted present or future role family and does not turn absence of a clause into a deletion command. |
| Exact addressability and lineage validation may be required locally without requiring `material_role`. | `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`, **Bounded resolution**: an authorized producer validates required identity, provenance, state, and warrant before asserting occurrence/standing. | Supports the constructor's exact local identity/provenance validation and addressable artifact formation. | Does not prescribe the role field, role-keyed storage, `initial_ingress`, or a universal constructor shape. |
| Provenance must retain sources, transformations, loss, and derivation boundaries needed for the claim. | `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`, **05.Evidence.A — Evidence support binding** requires evidence identity, source attribution, source/collection context, bounded subject, supported claim, authority boundary, preservation horizon, uncertainty, and provenance relation; **05.Evidence.B — Provenance representation and applicability** keeps represented lineage, applicability, coherence, verification, causation, and producer occurrence separate. | Supports retention of raw -> examination -> ingress lineage and distinct representation boundary for the addressability claim. | Does not require a role taxonomy or use provenance as authority for a map key. |
| Recording an Event preserves bounded evidence but does not turn it into every downstream standing. | `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`, **Bounded resolution**: recording preserves evidence under source, scope, authority, confidence, and limits; recording is not knowledge extraction or establishment. | Supports distinct capture, examination, and ingress evidence occurrences and their limited authority. | Does not make `material_role` constitutional truth or prescribe Event payload names. |
| Projection must preserve distinctions required by its bounded consumer purpose, but need not duplicate every upstream implementation detail. | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, **06.Projection.B — Purpose-relative lossless projection and package standing**. | Supports retaining raw/examination/decoded distinctions and cardinality evidence needed by the attempt view while allowing redundant role organization to be omitted. | Does not prescribe `raw_initial_material`, `preserved_ingress`, `representation_examinations`, or role-keyed storage; does not identify the view's undeclared consumers universally. |
| A rebuildable projection is not the constitutional source. | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, **06.Projection.C — Rebuildability and prior invocation boundary**: projection snapshots are generally rebuildable from ledger evidence within retained evidence/rules/purpose. | Supports treating current slots and map as rebuildable view organization, with Events as retained evidence. | Does not permit erasing ledger evidence or reconstruct a historical invocation not recorded. |
| Implementation visibility can faithfully witness behavior without becoming Book law or current constitutional standing. | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, **06.Projection.A — Projection and diagnostic visibility boundary**. | Supports classification of projection labels and tests as implementation witnesses only. | Does not treat tests, output shape, diagnostic absence, or projection existence as constitutional authority. |
| Implementation-local organization may carry no independent constitutional standing. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.F**: dimension != implementation key and local coordinates may be applicable, inapplicable, Unknown, conflicting, or unexamined. | Permits classifying the singleton map/key as implementation organization where exact current consumer evidence needs no role distinction. | Does not make all implementation organization dispensable or prohibit future lawful alternatives. |
| `material_role` is not established as identity. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.E — Relations have bounded standing**: relation participants/roles and relation assertion require their own bounded warrant and dimensions. | Supports separating a role/relation assertion from participant identity and requiring evidence for its applicable scope. | Does not establish what `initial_ingress` means; **classification: Unknown; finding: no exact active Book authority recovered for that locality**. |
| The current role's exact locality is Unknown. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.F**, final paragraph: an exact coordinate may remain Unknown when required evidence, authority, provenance, occurrence, applicability, or relation is not warranted/available. | Supports bounded Unknown for whether “initial” is attempt-, session-, process-, operator-, or historical-interaction-local. | Does not infer absence of locality, falsity of the literal, or a universal prohibition from missing evidence. |
| The Book does not prescribe `material_role`, `initial_ingress`, `raw_initial_material`, `preserved_ingress`, or `representation_examinations`. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.B — Constitutional kind labels are not ontology closure**, plus **01.Standing.F**'s “dimension != ... implementation key”; repository search recovered no exact naming clause. | Establishes that labels/forms do not create mandatory grammar; for each exact implementation name, **classification: Unknown; finding: no exact active Book authority recovered**. | Does not prove each name stale, forbid local organization, or erase distinctions faithfully represented through those names. |
| `preserved_ingress` may faithfully project decoded ingress without becoming source truth. | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, **06.Projection.A**, and **06.Projection.B**. | Supports a bounded view faithfully exposing the separately evidenced ingress subject and preservation standing without strengthening it. | Does not prescribe the label or mean ingress occurrence and projection-preservation occurrence are identical. |
| `raw_initial_material` cannot derive standing from its label; raw material distinction is independently supported while `initial` remains unestablished. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.C**, and `book_of_seed/06-state-and-projection/projection-and-current-state.md`, **06.Projection.B**. | Supports preserving raw-vs-decoded content/identity while refusing to infer role locality from projection vocabulary. | Does not require renaming, merge raw with decoded, or establish that “initial” is false. |
| Removing a redundant role coordinate may be faithful only if no material evidence or consumer-required distinction is erased. | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, **06.Projection.B**, sentence allowing compression not to duplicate every upstream implementation detail while forbidding collapse of required distinctions; `book_of_seed/06-state-and-projection/ownership-discrepancy-and-residue.md`, **Bounded resolution**, which requires present producer/consumer/warrant recovery before disposition of residue. | Supports this bounded recommendation after exact producer, consumer, history, and retained-lineage recovery. | The Book does not directly command deletion, promise compatibility, or authorize changes beyond the explicitly recovered singleton set. |
| Future constructibility and historical multiplicity do not establish a current collective/role family. | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, **01.Standing.D — Multiplicity does not establish a collective**. | Prevents both old two-role co-presence and possible future alternatives from being promoted to a currently warranted taxonomy. | Does not deny the historical roles, prohibit future role families, or show the present singleton invalid. |
| Source role is distinct from material role and must not be collapsed by this recovery. | `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, **01.External.B — Addressability without assimilation**: addressability retains source role or Unknown source role, provenance, scope, uncertainty, and authority limits. | Supports the addressable artifact's current operator-origin `source_role` as a provenance/attribution coordinate independent of the Event's application role. | Does not require `material_role`, equate source role with ordinal role, or adjudicate external grammar here. |

No exact Book clause establishes the meaning or locality of `initial_ingress`,
requires a role-keyed examination family, or commands the exact cleanup.  Those
questions remain Unknown at Book-name level; current applicability is assessed
from the bounded implementation witness under the Book's dimensional,
projection, and residue constraints.

## Recovery E — locality of `initial`

| proposed locality | current evidence | verdict |
|---|---|---|
| first material in process | persistent console may start after other operations; role carries no process coordinate | not established |
| first material in console session | every loop iteration receives the same literal | contradicted as a session ordinal |
| first material in one bounded attempt | one fresh attempt is created immediately before the sole capture call; historical attempt once had a later response | function topology witnesses this ordering, but the role itself does not declare attempt locality |
| first material before a response | current road has no response capture | historical only |
| first material on removed common-grammar road | historical two-role implementation directly establishes the contrast | historical implementation testimony only |
| first capture owned by one function | sole call is first and only call | implementation-local truth, not independent constitutional standing |
| implementation-local label | fixed literal, copied and checked, never selected | established current behavior |

Second and third console attempts all carry `initial_ingress`.  They can be
described as first/only capture calls in their respective freshly allocated
attempt functions.  They cannot be described as initial in the process or
console session.  Because the role value does not encode or declare its own
attempt-relative assertion, readers must infer locality from adjacency and
`attempt_ref`; the exact claimed role scope is therefore **Unknown**, not
attempt-local constitutional standing.

## Recovery F — projection shape

One active `run_operator_ingress_attempt` enforces:

* exactly one non-EOF raw captured material;
* exactly one representation examination;
* zero ingress occurrences on decode failure or exactly one on success;
* zero or one addressable artifact accordingly.

The producer cannot create multiple raw materials, examinations, or ingress
occurrences inside the same attempt.  The projection truthfully preserves these
active cardinalities, but the examination map advertises mechanically plural
roles that production cannot supply.  Role-keyed storage formerly protected two
materially distinct examinations.  It now adds no distinction and is not the
place that preserves multiplicity if fabricated same-role Events occur:
`event_ids` and `dimensional_standing` retain those exact Event identities while
the map replaces by key.

A single exact examination coordinate containing the current fields and exact
capture/examination IDs would preserve all current production evidence.  That
does not justify collapsing it into raw capture or decoded ingress.  The raw
slot's subject is faithful; only its `initial` qualifier lacks established
current applicability.  `preserved_ingress` is independently warranted by the
separate decoded occurrence and preservation projection even if the role and raw
qualifier are residue.

### Table 3 — role applicability

| coordinate | historical purpose | current producer | current alternatives | current consumer | current evidence of applicability | classification |
|---|---|---|---|---|---|---|
| `material_role` | distinguish initial ingress from enum response capture/examination | application hard-codes and helper copies | none | map key; two exact constructor checks | confirms a lane already identified by IDs/kinds/lineage | active but current applicability unestablished |
| `initial_ingress` | identify first raw material before probe response | sole attempt call site | none | constructor literal comparison; tests | first/only function-local capture, but no declared role locality | historical implementation testimony / Unknown locality |
| `raw_initial_material` | contrast raw initial bytes with raw response bytes | fixed projector kind mapping | no raw response slot/producer | view and tests only | faithfully contains raw capture; qualifier adds no current distinction | crossing: faithful current subject, unestablished qualifier |
| role-keyed `representation_examinations` | retain both initial and enum-response examinations | projector keys arbitrary payload role | none from production; fabricated manual values admitted | no production reader; tests index one key | one entry on every active road | singleton implementation organization |
| `preserved_ingress` | retain decoded initial ingress separately from response and raw bytes | fixed projector ingress-kind mapping | failure has none; no second ingress | view and tests only | distinct decoded occurrence with evidence and revised preserved standing | faithful current distinction |

`current_standing` presents distinct subjects, not merely successive standings of
one subject: raw uses a fresh material identity, ingress uses attempt identity,
and closure (not adjudicated) uses another identity.  Within the ingress slot,
the projector does revise `occurred` to `preserved` for the same decoded-ingress
subject.  Thus “different slots” and “standing revision” both occur, but at
different boundaries.

## Direct verdicts

1. **Are raw captured material and decoded ingress distinct current subjects?**
   **Yes.** Different identity, content, responsibility, authority, occurrence,
   and exact raw -> examination -> ingress lineage.
2. **Is representation examination distinct from both?** **Yes.** It is a
   separate decoder act occurrence and separately recorded evidence subject.
3. **Is `material_role` currently required to preserve those distinctions?**
   **No.** Event kind, identity, source, capture reference, attempt locality, and
   ordered lineage preserve them.
4. **Is `initial_ingress` currently relative to an established scope?**
   **Unknown.** Attempt-first is visible in function topology but not declared by
   the role; process/session readings are not true for repeated attempts.
5. **Does more than one current production role exist?** **No.** Only the fixed
   literal `initial_ingress`.
6. **Does any current production consumer branch among roles?** **No.** The
   constructor checks one literal; the projector keys without branching.
7. **Does the role prevent a current ambiguity not already prevented by identity
   and lineage?** **No recovered ambiguity.** All current references are exact.
8. **Does the addressable constructor require the role for constitutional
   fidelity?** **No.** It requires exact lineage fidelity; the role check is
   redundant application-topology confirmation, not necessary evidence.
9. **Is `representation_examinations` genuinely plural in current production?**
   **No.** It is a singleton map.  Manual fabrication is permissiveness, not an
   active family.
10. **Is `raw_initial_material` a faithful subject label?** **Mixed.** `raw` and
    `material` faithfully identify the slot's subject; `initial` has no
    independently established current locality.
11. **Is `preserved_ingress` a faithful subject label?** **Yes, boundedly.** It
    projects the decoded ingress subject with preserved standing; it does not
    identify the raw subject.
12. **Would removing `material_role` erase material evidence?** **No**, provided
    exact raw/examination/ingress IDs, kinds, locality, outcomes, and lineage stay.
13. **Would removing role-keyed storage erase material evidence?** **No** for the
    current production cardinality, provided one exact examination coordinate
    retains its present fields and IDs.
14. **Would renaming `raw_initial_material` improve fidelity, or is its current
    meaning established?** Removing the qualifier would improve fidelity to the
    recovered current subject, but that naming change is separable and is not
    the smallest recommended next slice.  The current complete meaning is not
    established.
15. **Does current evidence warrant implementation cleanup?** **Yes**, bounded
    to the redundant singleton role coordinate and its keyed organization; not
    to subject/event collapse or projection-label cleanup.
16. **What is the smallest exact slice?** Remove `material_role` from the
    single-role capture/examination road and replace role-keyed examination
    standing with one exact coordinate, preserving all subject identities,
    Events, lineage, content, outcomes, and raw/decoded separation.
17. **If cleanup were not warranted, what evidence would be missing?** A current
    second producer, a consumer that distinguishes simultaneous materials, or an
    exact local responsibility requiring the role.  None was recovered.
18. **Which questions remain Unknown?** The constitutional locality/meaning of
    `initial`; exact Book standing of every implementation name; whether any
    future lawful multi-material road will need roles; and projector-wide
    admission policy.
19. **What must not be changed together even if one singleton role is removed?**
    Do not merge raw bytes, representation examination, decoded ingress, or the
    addressable artifact; do not remove their Events, identities, provenance,
    outcomes, scopes, or separate occurrence standing; do not couple role
    cleanup to `preserved_ingress`, stopping, semantic, or candidate behavior.
20. **What is the next smallest lawful action?** The one slice below.

## Smallest next action

**Perform one bounded implementation cleanup that removes only the inseparable
singleton-role set: remove `material_role`/`initial_ingress` from the sole raw
capture and representation-examination road and constructor checks, and replace
the role-keyed `representation_examinations` map with one exact examination
coordinate.** Preserve raw capture, representation examination, decoded ingress,
their separate Events and identities, exact lineage, addressable material,
`raw_initial_material`, `preserved_ingress`, and every excluded semantic or
stopping boundary unchanged.  Do not add aliases or dual-read compatibility.

That is exactly one recommended next slice.  Renaming `raw_initial_material` is
not included: its qualifier is unestablished, but label cleanup is separable and
does not warrant expanding the smallest role-coordinate change.
