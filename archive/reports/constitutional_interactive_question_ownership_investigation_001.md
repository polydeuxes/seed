# Constitutional Interactive Question Ownership Investigation 001

## Question

A conflict has become visible between attributed operator testimony about Seed's intended interaction and public implementation surfaces such as:

```text
seed ask --question-family ...
seed ask --question-family ... --presentation
```

The investigation asks whether questioning is constitutionally an internal act of Seed while the operator supplies testimony, goals, constraints, corrections, and responses; whether views are internal means for Seed to see and compose bounded understanding; and what standing the public `ask --question-family` surface possesses.

This artifact is one bounded constitutional investigation. It does not implement, deprecate, rename, remove, test, or correct any runtime surface.

## Operator testimony consumed

The prompt-supplied interaction description is treated as attributed operator testimony, not law:

```text
operator supplies testimony, goals, constraints, corrections, and responses
↓
Seed establishes bounded meaning
↓
Seed composes applicable views internally
↓
Seed originates and asks bounded questions internally
↓
the operator responds
```

Preserved testimony distinctions:

```text
operator expression != constitutional question
operator testimony != inquiry origination
question surface != question standing
Question Family exposure != applicability
operator-selected presentation != Seed-composed view
view visibility != view-selection authority
dispatch != inquiry origination
compatibility access != canonical interaction
interactive dialogue != operator control of internal machinery
```

These distinctions are not assumed true. They are cross-examined below against Book and implementation testimony.

## Relevant Book neighborhood

The smallest relevant Book neighborhood begins with existing constitutional investigations and slices around inquiry origination, bounded goals, bounded questions, frontiers, view selection/composition, and bounded ask.

### Inquiry origination boundary

`constitutional_inquiry_origination_boundary_audit_001.md` already recovers a strong separation between external ingress and normal inquiry origination. It says the current operator-ingress path preserves exact operator expression, interpretation, authority/scope binding, and a permitted future handoff, but does not own goal establishment, advancement need diagnosis, inquiry frontier assembly, source selection, inquiry execution, result knowledge, or repository truth creation. It further finds that the current formulation path bypasses goal advancement and inquiry-need establishment, and classifies operator-ingress formulation as compatibility / ingress-formulated bounded question rather than normal inquiry origination.

The same audit recommends a normal road:

```text
external grammar
→ translation / interpretation
→ authority and scope preservation or binding
→ constitutional intent or bounded goal
→ bounded advancement horizon
→ advancement need projections
→ inquiry need establishment
→ selected inquiry need
→ frontier-boundary testimony
→ BoundedInquiryFrontier
→ frontier-question formulation testimony
→ BoundedConstitutionalQuestion
```

This Book neighborhood directly supports the distinction:

```text
operator testimony != inquiry origination
```

It also supports that a question-shaped artifact may exist by compatibility without proving normal Seed-originated inquiry.

### Bounded goal to bounded question bridge

`constitutional_bounded_goal_question_bridge_001.md` preserves that no current implementation-backed universal bounded-goal object or live consumer produces a new bounded constitutional question from bounded-goal state. It distinguishes goal-relative pressure from question-worthy uncertainty, bounded question standing, evidence demand, examination admission, and caller-authored routing.

It also says `caller_supplied_fields` named `selection_key` belong to caller-directed registered-view routing, not evidence demand recovery, question origination, or examination admission from bounded-goal state.

This supports the distinction:

```text
operator expression != constitutional question
operator-selected route != question standing
```

### Bounded inquiry frontier

`bounded_inquiry_frontier_slice_001.md` makes a narrower positive claim: one `BoundedInquiryFrontier` assembler consumes an exact selected inquiry need plus boundary testimony and refuses to invent scope, evidence admission, question formulation, inquiry opening, source selection, authorization, execution, recording, ledger writing, mutation, or known results.

This does not prove a complete interactive dialogue engine. It does prove that the Book has already moved constitutional question origination away from raw operator text and toward Seed-side need/frontier establishment when normal internal inquiry standing is claimed.

### Bounded ask adjacent terrain

`bounded_ask_adjacent_terrain_scout.md` records implementation-adjacent evidence for public bounded ask. It characterizes an exact QuestionFamily lookup, eligibility, surface-argument handling, presentation handoff, selection, dispatch request, dispatch execution, dispatch result handoff, and message clearing chain. The Scout explicitly does not recover another implementation slice, assign ownership, characterize responsibilities, recommend slice order, or design a new surface.

Therefore bounded ask Book evidence is mostly realization testimony and seam visibility, not constitutional authority establishing canonical interaction.

### Constitutional pipeline and view composition neighborhood

Existing Book and implementation-facing artifacts describe a pipeline that consumes an already-established bounded question and then performs deterministic projection, capability projection, exact selection, and composition from registered views. This neighborhood supports that views can be internal read-model means once exact keys and registered sources are already present, but it does not prove that operator-selected keys are the constitutional origin of evidence demand or view applicability.

## Implementation testimony examined

Implementation is treated as realization testimony, not authority.

### Default interactive `seed` ingress

`scripts/seed_local.py` defines a positional `message` for one-shot mode and describes `ask --question-family <exact-question-family>` as bounded question-family presentation dispatch. The parser also defines top-level `--question-family`, `--surface-args`, and `--presentation` flags with `ask`-specific help text.

This proves that public operator-accessible flags exist. It does not prove those flags are constitutionally canonical.

### Public `ask --question-family` dispatch

`apply_bounded_ask_dispatch(...)` maps the exact `ask --question-family` shape to existing inquiry surfaces. It rejects `--surface-args` and `--presentation` unless `--question-family` is present, rejects `--question-family` unless the message is exactly `ask`, performs exact inventory-backed QuestionFamily preparation, computes bounded work eligibility, validates surface args only for eligible families, then either performs a presentation handoff or creates a selection and dispatch request.

Implementation testimony therefore shows a lawful narrow public dispatch adapter shape:

```text
operator-supplied exact QuestionFamily text
→ exact inventory lookup
→ implementation-backed eligibility
→ optional surface-args satisfaction
→ presentation handoff or dispatch request
→ existing surface handling
```

It does not show:

```text
operator-selected family
→ Seed-originated inquiry need
→ constitutional applicability
→ Seed-composed view authority
```

### Question Family exposure

`seed_runtime/question_surface_inventory.py` has static maps for dispatchable Question Families, required surface arguments, diagnostic-only families, and static arg values. Its exact lookup and preparation helpers explicitly refuse to classify free text or own eligibility, selection, dispatch, presentation, rendering, diagnostics, or mutation. Eligibility is derived from executable dispatch maps: `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`.

This implementation testimony supports:

```text
Question Family exposure != applicability
```

The current map can say whether the implementation has a bounded ask dispatch path. It cannot, by itself, establish that a Question Family is constitutionally applicable to the operator's goal or that Seed lawfully selected that family as the next inquiry.

### Public presentation path

The public `--presentation` branch consumes bounded work eligibility and produces a handoff to the existing `question_family_explanation` surface, then stops before dispatch. This is presentation of an existing composed QuestionFamily explanation, not proof that the operator owns view selection, view composition, or question origination.

### Constitutional question and pipeline

`seed_runtime/bounded_constitutional_question.py` preserves explicitly supplied bounded question fields as testimony, with read-only boundaries that reject natural-language classification, fact promotion, authority creation, durable knowledge creation, constitutional view selection, QuestionProjection production, ledger writes, and cluster mutation.

`seed_runtime/constitutional_pipeline.py` says a pipeline request consumes one already-established bounded question and existing formatting inputs. It does not discover, repair, infer capability evidence, or originate questions.

`seed_runtime/constitutional_view_selection.py` projects only exact caller-declared selection keys from a bounded question, then selects registered constitutional views by exact comparison against capability keys. It performs no semantic matching or natural-language inference.

`seed_runtime/constitutional_view_composition.py` composes explicitly requested registered constitutional views read-only and says the request does not select views heuristically, discover evidence, reason at runtime, recover authority, plan, orchestrate, or mutate repository state.

Together, implementation testimony supports this distinction:

```text
operator-selected presentation / selection_key / view request
!= Seed-composed constitutional view applicability
```

Current implementation can perform explicit registered-view routing and composition. It does not prove that this route is the normal internal Seed inquiry act.

### Operator testimony, goals, and constraints

`seed_runtime/operator_expression_interpretation.py` preserves attributed operator expression and explicitly says interpretation does not establish authority, produce a bounded constitutional question, select a question family, diagnostic surface, constitutional view, or renderer, authorize, schedule, emit, or execute. `seed_runtime/operator_authority_scope_binding.py` binds requested scope and authority class, while preserving that authority-bearing expressions are not authority grants. `seed_runtime/bounded_operator_goal_establishment.py` establishes or refuses bounded operator goals from lawful ingress evidence, but says goal established is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied.

This supports the recovered relationship that operator input is admissible as testimony, goal material, constraints, corrections, or response material, but not automatically as Seed-originated inquiry selection.

## Cross-examination

### Authority

Authority is strongest where artifacts explicitly refuse overreach. Operator expression interpretation refuses question-family selection and question production. Bounded goal establishment refuses inquiry opening. Bounded question construction refuses authority creation and view selection. Constitutional pipeline refuses question origination. View selection refuses semantic matching. View composition refuses heuristic view selection and authority recovery.

Positive authority for a full canonical interactive loop remains incomplete. The Book supports a normal internal inquiry road through bounded goal, advancement need, inquiry need, frontier, and future frontier-question formulation, but implementation testimony does not show a complete default interactive engine that executes that full road.

### Evidence

Evidence supports these recovered responsibilities:

| Responsibility | Lawful owner as far as evidence permits |
| --- | --- |
| Operator expression / testimony supply | operator supplies; Seed preserves as attributed testimony |
| Goal and constraint material supply | operator may supply; Seed establishes/refuses bounded goal through lawful ingress evidence |
| Inquiry origination | Seed-owned in the normal constitutional road, only after bounded advancement / inquiry need / frontier establishment; not owned by raw operator text |
| Question formation | Seed-owned for normal internal inquiry, but current direct bounded-question constructors and ask compatibility can preserve supplied/caller-routed question-shaped artifacts without proving normal standing |
| Question Family applicability | Seed/implementation-owned eligibility evidence for public bounded ask dispatch; constitutional applicability to a goal remains unproven unless separate need/frontier evidence establishes it |
| View selection and composition | Seed-owned internally when driven by established question/projection/capability evidence; caller-declared selection keys are explicit routing testimony, not constitutional view-selection authority |
| Bounded question asking | Seed-owned in the intended normal interaction only as far as the Book's need/frontier path supports; full executable dialogue standing remains incomplete |
| Operator response | operator-owned as response/testimony; response does not own internal inquiry machinery |
| Dispatch | implementation-owned adapter over existing surfaces; dispatch does not originate inquiry |

### Responsibility

The public ask surface relocates some operational control to the operator at the CLI boundary: the operator can choose an exact Question Family, provide surface args, and request presentation. That is a real implementation behavior. Fidelity prevents treating this relocation as constitutional ownership unless the Book or stronger implementation-backed law establishes it.

The recovered responsibility is therefore mixed:

- **Normal constitutional relationship:** Seed owns internal inquiry origination, question formation, family applicability, view selection/composition, and bounded question asking; the operator owns supplying testimony/goals/constraints/corrections and responding.
- **Current public `ask --question-family` relationship:** the operator owns invocation of a compatibility/diagnostic/development-facing dispatch adapter; implementation owns exact lookup, eligibility, dispatch mapping, and presentation handoff; this does not establish canonical inquiry origination.

### Standing

`seed` interactive / one-shot standing is **partly established, partly Unknown**:

- Established: operator text is accepted as message testimony / one-shot input; implementation has roads for interpreting attributed operator expressions, binding authority/scope, and establishing bounded goals.
- Unknown: the default interactive `seed` process fully implements the constitutional loop in which Seed internally composes views, originates bounded questions, asks them, and consumes operator responses.

`seed ask --question-family` standing is **mixed compatibility and diagnostic/development projection, not canonical interaction as currently evidenced**:

- Compatibility: it maps exact family names to existing inquiry-answer surfaces and maintains public behavior through dispatch handoffs.
- Diagnostic/development projection: it exposes inventory, definitions, explanations, eligibility, and shape of the question surface machinery.
- Not established as canonical: no reviewed evidence proves that operator-selected families are the lawful normal means by which inquiry originates or views are selected.
- Not merely historical residue: current code and tests intentionally preserve the surface.
- Not pure diagnostic: several families dispatch to existing answer surfaces when eligible.

The most precise classification currently warranted is:

```text
public ask compatibility surface with diagnostic/development visibility; canonical standing Unknown and not established
```

### Handoff

Lawful handoff from operator to Seed is through attributed expression, interpretation, authority/scope binding, and bounded goal establishment. Lawful handoff from Seed inquiry need to question formation is Book-recovered through advancement need and frontier testimony, but not yet executable as a complete default interactive loop. Public `ask --question-family` handoff is a separate exact-family dispatch adapter and should not be confused with the normal Seed-owned inquiry handoff.

### Reliance

It is lawful to rely on `ask --question-family` for what its implementation actually proves: exact inventory-backed family lookup, implementation-backed eligibility, optional surface argument validation, presentation explanation handoff, and dispatch to existing surfaces. It is not lawful to rely on that surface as proof that the operator owns inquiry origination, question formation, family applicability, view selection, or Seed's internal bounded asking.

### External grammar

Operator-supplied words can orient interpretation and bounded goal establishment. Presentation vocabulary and Question Family labels are not automatically knowledge. Exact QuestionFamily text may be admitted into the bounded ask inventory path, but exact label admission is not constitutional applicability.

### Negative authority

The investigation rejects these promotions unless future evidence establishes them:

```text
operator says a question → constitutional question standing
operator selects Question Family → family is applicable to current goal
operator requests --presentation → operator selected Seed's internal view composition
public dispatch works → canonical interaction is operator-controlled dispatch
view is visible → operator owns view selection authority
implementation map exists → constitutional inquiry need exists
```

### Lawful stop

This operation stops at constitutional classification. It does not alter runtime code, tests, CLI flags, diagnostic inventory, shape audit, or public compatibility behavior because implementation correction before constitutional authority would reverse Fidelity.

### Unknown

Preserved Unknowns are listed below rather than resolved by preference.

### Fidelity

Fidelity governs crossing between Book and implementation:

- Operator testimony oriented the investigation but did not become law.
- Implementation behavior testified about realized surfaces but did not become constitutional authority merely because it exists and is tested.
- The Book is treated as honest but imperfect projection; existing audits around inquiry origination and goal-question standing provide stronger constitutional evidence than the mere presence of `ask --question-family`.
- Where Book and implementation diverge, the lawful finding preserves a compatibility/public adapter beside a Seed-owned normal inquiry relationship rather than forcing one to erase the other.

## Recovered interaction relationship

As far as current evidence permits:

```text
operator supplies attributed expression, testimony, goals, constraints, corrections, and later responses
↓
Seed may interpret expression, bind authority/scope, and establish or refuse bounded goals
↓
Seed-owned normal inquiry requires advancement / inquiry need / frontier establishment before internal question formation
↓
Seed-owned view selection and composition are internal read-model means when driven by established question/projection/capability evidence
↓
Seed asks bounded questions only when that internal standing exists
↓
operator responses are further testimony, not control of internal machinery
```

Parallel compatibility road:

```text
operator invokes seed ask --question-family <exact-family> [--surface-args ...] [--presentation]
↓
implementation admits only exact inventory-backed QuestionFamily labels
↓
implementation computes bounded ask eligibility from current dispatch maps
↓
implementation either refuses, presents existing QuestionFamily explanation, or dispatches to an existing answer surface
↓
this proves compatibility dispatch standing, not normal inquiry origination
```

## View ownership

Views are Seed-owned internal read-model means when used by the constitutional pipeline. Current view selection and composition implementations consume exact keys, registered capability projections, and explicitly requested registered views. They are read-only and refuse heuristic selection, authority recovery, runtime reasoning, and mutation.

Public presentation can expose a composed explanation. That visibility does not transfer view-selection authority to the operator.

## Question ownership

Normal question ownership belongs to Seed, not the operator, when the question claims constitutional standing as an internal inquiry act. Operator expression and testimony can supply material that Seed preserves, interprets, binds, and may eventually use to establish inquiry need. Direct bounded-question construction and public ask dispatch can preserve question-shaped/caller-routed artifacts as testimony or compatibility artifacts, but do not prove normal Seed-originated question standing.

## Question Family applicability ownership

Question Family applicability has two layers:

1. **Implementation bounded ask eligibility:** owned by Seed implementation through exact inventory and dispatch maps. This layer can say `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable` for the public ask adapter.
2. **Constitutional applicability to the current goal/inquiry:** owned by Seed's internal inquiry establishment path. Current evidence does not show that public operator selection of a family establishes this layer.

Therefore:

```text
Question Family exposure != constitutional applicability
```

## Standing of interactive `seed`

Interactive / one-shot `seed` is the broader operator ingress surface. Its constitutional standing is to receive operator material and route realized work through current implementation. The fully recovered canonical dialogue loop remains only partly established because the Book supports the Seed-owned normal road, but reviewed implementation does not prove a complete default interactive engine that internally selects inquiry need, composes views, originates a question, asks it, and consumes a response.

Classification:

```text
operator ingress surface with partial constitutional support; full canonical dialogue standing Unknown
```

## Standing of public `seed ask`

Public `seed ask --question-family` is not currently established as canonical interaction. It is also not merely accidental residue because implementation and tests intentionally preserve its exact-family dispatch and presentation behavior.

Classification:

```text
public ask compatibility surface with diagnostic/development visibility; canonical interaction standing Unknown and not established
```

Lawful public standing includes:

- exact QuestionFamily inventory lookup;
- implementation-backed eligibility/refusal;
- surface-argument validation for parameterized families;
- presentation of existing QuestionFamily explanation;
- dispatch to existing inquiry-answer surfaces where eligible.

Unlawful promotion includes:

- operator ownership of inquiry origination;
- operator ownership of question formation;
- operator ownership of constitutional Question Family applicability;
- operator ownership of Seed's internal view selection/composition.

## Fidelity finding

The current repository preserves a constitutional distinction between Seed-owned normal inquiry and operator-supplied ingress/testimony, but implementation exposes a public compatibility dispatch adapter that can look like operator control of internal inquiry machinery.

Fidelity finding:

```text
preserved-with-pressure
```

Meaning:

- The Book already contains enough evidence to reject promotion of public ask dispatch into canonical operator-owned inquiry origination.
- The Book does not yet fully establish the default interactive dialogue loop as an executable canonical process.
- The implementation preserves a public ask compatibility surface whose standing must remain bounded to exact dispatch/presentation behavior until future constitutional work either canonizes, deprecates, or rehomes it.

## Book projection decision

A Book update is warranted because the specific relationship among operator, Seed, interactive dialogue, Question Families, views, presentation, and public ask compatibility was not stated in one bounded constitutional artifact. Existing grammar mostly supports the relationship, so this artifact clarifies and reconciles rather than rewriting constitutional law.

No runtime implementation or test update is warranted in this operation.

## Preserved Unknowns

1. Whether the default interactive `seed` process fully implements the normal constitutional loop from operator testimony through Seed-originated bounded question asking and operator response consumption.
2. Whether `seed ask --question-family` should later be canonized, deprecated, renamed, hidden, or formally classified as diagnostic/compatibility/development-only.
3. Whether any specific Question Family is constitutionally applicable to a particular operator goal without separate goal/need/frontier evidence.
4. Whether public `--presentation` should remain attached to ask compatibility or be separated from internal view-composition visibility.
5. Whether future frontier-question formulation should become the only executable producer for normal internal bounded constitutional questions.
6. Whether additional Book grammar should define interactive response consumption after Seed asks a bounded question.

## Implementation pressure for later work

Later implementation work may be warranted, but is not authorized by this artifact alone:

- inventory and classify public ask surfaces as canonical, compatibility, diagnostic, development, or legacy once constitutional authority is sufficient;
- expose clearer user-facing language that `ask --question-family` is exact dispatch compatibility rather than internal inquiry ownership, if that remains the chosen standing;
- build or connect the normal interactive Seed-owned inquiry road from bounded goal through advancement need, inquiry need, frontier, question formulation, bounded asking, and response consumption;
- audit whether public presentation and view-composition explanation surfaces imply more authority than they own;
- add diagnostic inventory / shape-audit updates only if later work modifies diagnostic, audit, probe, view, CLI flag, or recordable output surfaces.

## Final answer to the direct questions

### Is questioning an internal act of Seed, while the operator supplies testimony and responses?

For normal constitutional inquiry, yes as far as existing Book evidence permits: Seed owns inquiry origination and question formation after need/frontier establishment; the operator supplies testimony, goals, constraints, corrections, and responses. Full executable default interactive standing remains Unknown.

### Are views internal means by which Seed sees and composes bounded understanding?

Yes for registered constitutional view selection/composition when driven by established question/projection/capability evidence. Public visibility or presentation of those views does not grant the operator view-selection authority.

### What standing does operator-selected `ask --question-family` possess?

It has public compatibility dispatch standing with diagnostic/development visibility. It is not established as canonical interaction, not pure diagnostic, not merely historical residue, and not proof of operator-owned inquiry origination.

### Does the current Book sufficiently establish this relationship?

Mostly, but not in one place. Existing inquiry-origination and bounded-goal/question audits establish the core negative authority. This artifact adds the smallest warranted reconciliation: public `ask --question-family` is bounded as compatibility/visibility unless future evidence establishes canonical standing, while Seed-owned normal inquiry remains the constitutional direction where supported and Unknown where not yet executable.
