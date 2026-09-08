# Question Family Registration Boundary Audit

## Selected architectural question

How does a recovered architectural family earn the right to become a public, answerable `QuestionFamily`?

Bounded answer: current implementation evidence supports **explicit registration as implementation work inside the static Question Surface Inventory and bounded ask maps**. It does not support an implemented, first-class `Registration` responsibility between `Recovered Family` and `QuestionFamily` today. `QuestionFamily` is the terminal public answerable identity in the implemented inquiry path, and a family exists there only after code explicitly adds a `QuestionSurfaceInventoryRow` and, where dispatchable, bounded ask metadata that points at an existing answering surface.

The audit therefore supports this current chain:

```text
QuestionFamily
  -> QuestionSurfaceInventoryRow
  -> bounded ask eligibility / dispatch map
  -> existing answer surface
```

It does **not** support this as an implemented architecture:

```text
Recovered Family
  -> Registration responsibility
  -> QuestionFamily
```

A future implementation could recover a registration responsibility, but the current repository has not implemented it as a distinct owner. Repository authority wins.

## Implementation evidence

### Question families are static inventory rows plus map-backed eligibility

`seed_runtime/question_surface_inventory.py` describes the module as a static inventory of question families and answering surfaces. The primary data object is `QuestionSurfaceInventoryRow`, whose fields include the family name, example questions, answering surface, CLI flag, answer responsibility, authority boundary, notes, bounded status, dispatch surface, required surface args, formatter metadata, implementation reason, diagnostic relationship fields, and relationship status.

`build_question_surface_inventory()` returns a deterministic, read-only tuple of rows. The row list is literal code data: adding a new family currently means editing this tuple with a `QuestionSurfaceInventoryRow(...)` entry. Row enrichment then derives status and relationship metadata from static maps and diagnostic registries rather than recovering families from responsibility records.

Dispatchability is separately controlled by static maps:

- `BOUNDED_ASK_DISPATCH_SURFACES` maps exact question-family strings to existing implementation surfaces.
- `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` names exact families that need explicit operator-provided arguments.
- `BOUNDED_ASK_DIAGNOSTIC_ONLY_FAMILIES` keeps some inventory rows visible but not dispatchable by bounded ask.
- `bounded_status_for_question_family()` derives status only from those maps and returns `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`.

This means a new public answerable family is caused by static implementation edits, not by automated recovery.

### QuestionFamily definition and composed explanation are downstream wrappers

`QuestionFamilyDefinition` and `ComposedQuestionFamilyExplanation` wrap inventory-derived fields. `build_question_family_definition()` returns `unknown` when no inventory row exists and says no implementation-backed authority boundary exists for that unknown family. For known rows it returns the inventory row's surface, flag, bounded status, answer responsibility, authority boundary, diagnostic relationship, implementation reason, and evidence source.

`build_composed_question_family_explanation()` explicitly composes existing `QuestionFamily` explanation fields for presentation only. Its sections are Definition, Answer responsibility, Boundary, and Diagnostic relationship. It does not create the family, admit it, promote it, or recover it from architecture evidence.

### Bounded ask dispatch consumes exact registered family strings

`apply_bounded_ask_dispatch()` maps `ask --question-family` to an existing exact inquiry surface. The dispatch adapter:

1. requires the literal `ask` command shape when `--question-family` is present;
2. validates the supplied family against `build_question_surface_inventory()`;
3. rejects an unknown family before any dispatch;
4. derives eligibility with `bounded_status_for_question_family()`;
5. rejects diagnostic-only and not-dispatchable families;
6. enforces exact required surface argument counts for parameterized families;
7. maps eligible families through `BOUNDED_ASK_DISPATCH_SURFACES` to existing surfaces; and
8. routes `--presentation` to the composed QuestionFamily explanation rather than to a recovery process.

The dispatch implementation therefore treats `QuestionFamily` as an exact, registered namespace value. It does not inspect recovered families, grammar observations, responsibility records, or free-text question meaning.

### Grammar Observation explicitly refuses promotion into responsibility or family recovery

`ObservationAgreement` emits candidate agreement records from already-observed inputs while refusing grammar ownership, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, event writes, ledger writes, repository mutation, and cluster mutation.

`GrammarObservation` consumes only `ObservationAgreementRecord` values and emits recurring relation-shape observations. Its boundary explicitly sets `owns_responsibility_recovery` and `owns_family_recovery` to `False`. `GrammarObservationRecord` preserves relation shape, supporting agreements, provenance, recurrence evidence, and a non-promotion boundary; it intentionally carries no `question_family`, no answer responsibility, no surface, no dispatch surface, and no inquiry subject.

The tests reinforce the boundary: grammar observation emits only recurring relation shapes and confirms the boundary rejects adjacent ownership and mutation. A test can feed evidence strings such as `Responsibility Recovery != Grammar Observation` and `Family Recovery != Grammar Observation`; the implementation still emits only the generic shape `term != term`, not a recovered responsibility, recovered family, or registered question family.

### Prior boundary audit already found no direct Responsibility Recovery to Inquiry path

`responsibility_to_inquiry_boundary_audit.md` concluded that current Inquiry does not consume recovered responsibilities directly. It found that a recovered responsibility becomes answerable only after being represented as an exact named `QuestionFamily` with an inventory row, bounded eligibility, answer surface, and dispatch mapping where applicable.

That prior audit is important here because this task asks whether one final compatibility boundary exists between family recovery and the public answerable namespace. The implementation evidence still stops at the same place: the current bridge is `QuestionFamily` / `QuestionSurfaceInventory` plus bounded ask dispatch, not an implemented `Registration` owner.

## Supported boundary

Supported current boundary:

```text
Registered QuestionFamily
  -> QuestionSurfaceInventoryRow
  -> bounded ask status
  -> optional dispatch mapping / required args
  -> existing answer surface
```

The boundary is implementation-backed because:

- the namespace is exact string-valued family identity;
- the inventory row owns public answerable-subject metadata;
- the dispatch maps own executable eligibility;
- the dispatch adapter rejects unknown, diagnostic-only, not-dispatchable, and wrongly parameterized families;
- definition and explanation surfaces expose inventory-derived identity, responsibility, boundary, and diagnostic relationship; and
- authority boundaries remain attached to rows rather than inferred from recovered vocabulary.

A recovered family, if one existed outside this namespace, earns public answerability today only by being explicitly encoded into this contract. That encoding is manual implementation work: add or modify the row, decide whether it is dispatchable, map it to an existing surface when appropriate, provide required args if needed, and keep diagnostic visibility aligned if the surface is diagnostic.

## Unsupported boundary

Unsupported as existing implementation:

```text
Recovered Family
  -> Registration
  -> QuestionFamily
```

No inspected code defines a `QuestionFamilyRegistration`, `FamilyRegistration`, `InquirySubjectRegistration`, `RecoveredFamily`, or `FamilyRecovery` implementation that admits recovered families into the question-family namespace. No inspected dispatch path consumes `GrammarObservationRecord`, `ObservationAgreementRecord`, responsibility-family completion evidence, or a recovered-family object. No registry records admission criteria such as evidence sufficiency, surface ownership proof, authority boundary validation, answer responsibility acceptance, or compatibility review as a distinct registration lifecycle.

The strongest current admission rule is implicit and static: an exact string is a known `QuestionFamily` if and only if it appears in `build_question_surface_inventory()`. It is dispatchable if and only if the bounded ask maps say it is dispatchable.

## Counterexamples

### Counterexample: QuestionFamily already owns registration

Partly accepted only in a weak sense. The question-family subsystem owns the currently registered namespace because inventory rows and dispatch maps determine known families and bounded ask eligibility. However, it does not own a separate recovery-to-registration decision. There is no admission workflow, no recovered-family input, no registration result object, and no explicit registration lifecycle. `QuestionFamily` owns the terminal public identity, not the process by which recovered families become public identities.

### Counterexample: Registration is only presentation vocabulary

Rejected as a complete explanation. The word `registration` is not implemented as a named object here, so treating it as architecture would over-promote vocabulary. But the underlying question-family rows and dispatch maps are not merely presentation vocabulary: they determine CLI acceptance, bounded eligibility, dispatch target, required args, diagnostic relationship, and unknown-family rejection. The operational behavior is real; only the proposed architectural label `Registration` is unsupported as a first-class current responsibility.

### Counterexample: Registration is merely static configuration

Mostly accepted for the current implementation. New QuestionFamilies currently exist through static code data and static maps. That does not mean the boundary is unimportant: the static data carries recurring ownership concerns such as answer responsibility, authority boundary, exact dispatch surface, required arguments, diagnostic linkage, and relationship status. But these concerns are compressed into the inventory/dispatch implementation rather than separated as an independent registration responsibility.

### Counterexample: Existing inventories already fulfill every responsibility

Partly accepted for current behavior, rejected for stronger architecture. `QuestionSurfaceInventoryRow` plus bounded ask maps fulfill the current public answerable-subject contract. Diagnostic Inventory and Diagnostic Shape Audit fulfill diagnostic surface visibility and shape checks. Together they cover the implemented answerability path.

They do not fulfill a recovery-admission responsibility because they do not evaluate recovered-family evidence, do not compare recovered families to existing namespace entries, do not decide promotion readiness, and do not preserve a non-promotional candidate state before registration.

### Counterexample: Registration has independent recurring ownership

Weakly suggested but not implemented. Recurring concerns are visible:

- exact namespace identity;
- answering surface ownership;
- authority boundary;
- bounded ask eligibility;
- required parameters;
- diagnostic inventory and shape-audit relationship;
- implementation reason; and
- rejection of unknown or unsupported families.

These could become the owned fields of a future registration responsibility. Current evidence, however, keeps them inside static inventory construction and dispatch validation. Recurrence alone is not enough to claim a first-class responsibility.

## Compatibility implications

1. **QuestionFamily is the current terminal object for answerable subjects.** Public inquiry dispatch is keyed by exact `QuestionFamily` strings backed by inventory rows.

2. **Recovered families are not public inquiry subjects by default.** Even if future audits recover an architectural family, current inquiry will not answer it unless it is explicitly represented in the Question Surface Inventory and bounded ask maps where applicable.

3. **Automatic QuestionFamily creation would violate current non-promotion boundaries if added directly.** Grammar Observation and Observation Agreement explicitly reject responsibility recovery, family recovery, semantic interpretation, architectural truth, and promotion. Creating a QuestionFamily directly from recurring relation shapes or candidate agreements would bypass those boundaries.

4. **A future registration responsibility would need a candidate/admission boundary.** It would need to prove that recovered-family evidence remains non-promotional until an explicit implementation-backed admission decision supplies an answering surface, answer responsibility, authority boundary, compatibility behavior, diagnostics, tests, and dispatch eligibility.

5. **Static registration preserves compatibility today.** Because dispatch maps existing exact families to existing surfaces, adding a family is a compatibility decision made in code rather than a runtime mutation, schema change, event change, grammar change, or ledger update.

## Answers to the requested questions

### 1. What currently causes a new QuestionFamily to exist?

A static implementation edit to `build_question_surface_inventory()` causes a new known `QuestionFamily` to exist. If it should be executable through bounded ask, corresponding static dispatch-map entries must also be added. Without the inventory row, `build_question_family_definition()` reports the family as unknown and `apply_bounded_ask_dispatch()` rejects it.

### 2. Is QuestionFamily recovered? Or explicitly registered?

It is explicitly registered in code as a static inventory row. It is not recovered by current Grammar Observation, Responsibility Recovery, Family Recovery, bounded ask dispatch, or QuestionFamily explanation code.

### 3. Does implementation evidence support `Recovered Family -> Registration -> QuestionFamily` or only `QuestionFamily`?

Only `QuestionFamily` as the terminal public answerable object is implemented. The repository supports static inventory/dispatch registration as implementation work, but not a first-class recovered-family registration responsibility.

### 4. Is registration merely implementation work? Or does implementation already exhibit recurring ownership and boundaries?

Today it is implementation work compressed into static inventory construction and bounded dispatch maps. The code does exhibit recurring ownership concerns: namespace identity, surface ownership, answer responsibility, authority boundary, dispatch eligibility, required args, diagnostic relationship, and unknown-family rejection. Those concerns are evidence for a possible future boundary, not proof that the boundary is already implemented as a responsibility.

### 5. If registration is a responsibility, what would it own?

If recovered later, it would own admission from a non-promotional recovered-family candidate into the public QuestionFamily namespace. Concretely it would own evidence requirements, duplicate/compatibility checks, answer-surface ownership, answer responsibility, authority boundary, dispatch eligibility, required arguments, diagnostic inventory/shape-audit linkage, implementation reason, unknown/rejected candidate status, and tests proving non-promotion before admission.

### 6. If registration is not a responsibility, what implementation evidence rejects it?

The rejection evidence is the absence of a registration object or admission workflow, the static row tuple, map-derived bounded status, exact string dispatch, unknown-family rejection, presentation-only composed explanation, and non-promotion boundaries in Observation Agreement and Grammar Observation. Current records before the QuestionFamily inventory do not carry answerability metadata.

### 7. Would introducing automatic QuestionFamily creation violate current non-promotion boundaries?

Yes, if implemented as direct creation from observation agreement, grammar observation, responsibility labels, or recovered-family vocabulary. It would promote candidate/shape evidence into public inquiry authority without the explicit inventory row, answer responsibility, authority boundary, dispatch compatibility, diagnostic visibility, and tests required by current implementation practice.

## Recommended next implementation step

Do not implement automatic registration and do not implement Family Recovery.

The next smallest implementation-backed step, if future work is requested, should be a characterization test or audit of one concrete proposed QuestionFamily addition against the existing `QuestionSurfaceInventoryRow` contract. The test should prove that the family remains unknown and non-dispatchable until explicitly added to the inventory and dispatch maps. That would preserve the current non-promotion boundary while making the implicit registration gate more observable.

## Confidence

High confidence that current `QuestionFamily` existence is static and explicit, not recovered.

High confidence that bounded ask dispatch consumes exact registered family strings and rejects unknown or unsupported families.

High confidence that Grammar Observation and Observation Agreement reject direct promotion into responsibility or family recovery.

Medium confidence that a future `QuestionFamily Registration` responsibility is architecturally plausible, because recurring ownership fields are visible but compressed.

Low confidence that registration is already a first-class responsibility, because no implementation owner, record shape, lifecycle, or tests currently separate it from static inventory and dispatch work.
