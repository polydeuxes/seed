# Operator-ingress disconnected common-grammar island fidelity recovery 001

## Scope, method, and result

This is one bounded, report-only recovery against merged `main` at `c64fdec` (PR
2099).  I searched the full repository for the module's definitions, imports,
calls, Event-kind strings, state fields, projector dispatch, CLI wiring, tests,
SQLite fixtures, documentation, exports, and Book references.  In particular I
did **not** treat construction, a test call, lexical adjacency, an unused import,
an Event handler, or Book recognition as production reachability.

The result is asymmetric.  The executable console still calls
`run_operator_ingress_common_grammar_probe_attempt`, but for decoded non-EOF
material line 1767 returns the projected three-Event view.  Everything beginning
with `_examine_potential_goal_standing` at line 1769 is a lexically present,
unreachable orchestration tail.  No non-test caller independently calls any
tail helper.  The common projector can nevertheless consume old or externally
extended downstream Events, and SQLite can reload them, but no repository
fixture, version/migration policy, or explicit compatibility promise specific
to these kinds was found.  Therefore producer/orchestration reachability and
generic replay capability must be decided separately.

## Evidence rules and recovered boundaries

* **Non-test entrance** means a call reachable from current executable code,
  excluding tests, reports, Book prose, and dead statements.  The only entrance
  found is `scripts/seed_local.py:5801`, from the persistent console.
* **Current producer** means code that can append the Event on such a path.
  `_record` statements below line 1767 are historical/unreachable producers,
  not current producers.
* **Consumer** is split into projection/replay, later semantic uptake, and test
  assertion.  `StateProjector.apply` dispatches every matching kind to
  `project_operator_ingress_common_grammar_events`; that fact does not make the
  Event producible.
* **Durable replay** is technically available: `SQLiteEventLedger` persists
  arbitrary Events and reconstructs them, and `StateProjector` projects the
  returned list.  The two `tmp_path` tests prove this for synthetic standing and
  binding histories.  They do not establish a shipped database or a declared
  long-term schema compatibility policy.
* **API standing** is based on exports and documentation, not capitalization.
  Closed-choice and BOGE artifacts are exported by `seed_runtime.__init__`.
  Nothing from `operator_ingress_common_grammar_prerequisite` is exported there.
  The latter's public-looking names are internal unless stronger evidence is
  found; underscore helpers are module-private and directly imported by tests.

## Required topology A — current active road

```text
scripts.seed_local.main (bare `seed`, persistent console)
→ run_persistent_operator_console
→ capture_stdin_material
→ run_operator_ingress_common_grammar_probe_attempt
→ _capture_representation(material_role="initial_ingress")
   → operator.ingress.common_grammar.raw_material_captured
   → strict examine_text_representation
   → operator.ingress.common_grammar.representation_examined
→ operator.ingress.common_grammar.ingress_occurred (decoded non-EOF)
→ StateProjector.project
→ StateProjector.apply
→ project_operator_ingress_common_grammar_events
→ return state.operator_ingress_common_grammar_attempts[attempt]  # line 1767
→ continuing outer console operation
```

The adjacent active failure/EOF branches also remain production: failed initial
decoding records `stopping_occurred`; initial EOF records
`initial_eof_occurred` then `stopping_occurred`.  They do not enter the island.

## Required topology B — lexically present unreachable tail

`..then..>` below denotes source chronology only, never constitutional uptake:

```text
_examine_potential_goal_standing
..then..> _examine_presentation_eligibility
..then..> common_grammar_choice_set
..then..> render_probe + probe_produced
..then..> common_grammar_representation_lineages + alternatives_represented
..then..> render_probe + stdout + presentation_occurred
..then..> _capture_representation(material_role="enum_response")
..then..> response EOF/representation-failure stopping branches
..then..> response_captured + OperatorSelectionTokenCapture
..then..> validate_capture_for_probe
..then..> bind_closed_choice_selection
..then..> binding_completed or unsupported_finding
..then..> alternative_selected (bound only)
..then..> _recover_represented_source
..then..> source_recovered or source_recovery_refused
..then..> _warrant_source_meaning_relation
..then..> (potential-goal source only)
            _examine_meaning_relation_for_bounded_operator_goal_establishment
            → examine_meaning_relation_applicability
            → applicability_examined/refused
..then..> projection, result rendering, and return
```

Notably this tail does not call either BOGE establishment function.  Its last
semantic step is consumer-local *applicability examination*, which currently
finds admission absent/Unknown; it does not admit or establish a goal.  Local
stopping appears in the response EOF and response representation-failure
branches.  Recovering a `local-stop` source merely renders that a bounded stop
was **not** established.

## Required topology C — current non-test call graph

```text
run_persistent_operator_console
→ run_operator_ingress_common_grammar_probe_attempt
   → active: _capture_representation, _record, StateProjector.project
   → downstream tail: blocked by unconditional return at line 1767

StateProjector.apply
→ project_operator_ingress_common_grammar_events  # independent replay dispatcher
```

For calls into downstream **producer/semantic helpers**: **no current non-test
call path found**.  Static full-repository call search found no other non-test
calls to `_examine_potential_goal_standing`, `_examine_presentation_eligibility`,
`application_presentation_purpose`, `common_grammar_choice_set`, `render_probe`,
`common_grammar_representation_lineages`, `validate_capture_for_probe`,
`_recover_represented_source`, `_warrant_source_meaning_relation`, or
`_examine_meaning_relation_for_bounded_operator_goal_establishment`.

The general `bind_closed_choice_selection` and
`examine_meaning_relation_applicability` implementations likewise have no
reachable non-test caller today: their only non-definition production call
sites are inside this unreachable tail/helper chain.  BOGE is broader in design
and package exports, and `bounded_advancement_horizon` consumes the BOGE
artifact type, but repository code has no non-test call to either establishment
producer.  “Broader” therefore means a distinct module/interface and downstream
artifact responsibility, not presently demonstrated executable reachability.

## Required topology D — Event producers and consumers

```text
CURRENT PRODUCTION PRODUCERS
  _capture_representation → raw_material_captured, representation_examined
  run_operator_ingress_common_grammar_probe_attempt
    → ingress_occurred | initial_eof_occurred | stopping_occurred

UNREACHABLE HISTORICAL PRODUCERS
  tail/helper chain → potential_goal_standing_examined,
  presentation_eligibility_examined, probe_produced,
  alternatives_represented, presentation_occurred,
  response raw_material_captured/representation_examined,
  response_captured, response_eof_occurred, binding_completed,
  unsupported_finding, alternative_selected, source_recovered,
  source_recovery_refused, meaning_relation_warranted,
  meaning_relation_refused,
  bounded_operator_goal_establishment_applicability_examined,
  bounded_operator_goal_establishment_applicability_refused,
  response-branch stopping_occurred

TEST-ONLY PRODUCERS
  tests construct/append fixtures for every downstream stage needed by the
  direct helper contracts; the SQLite tests manufacture standing and binding
  histories in temporary databases.

PROJECTION / REPLAY CONSUMERS
  SQLiteEventLedger.list → StateProjector.project/apply
    → project_operator_ingress_common_grammar_events
    → State.operator_ingress_common_grammar_attempts

SEMANTIC CONSUMERS (all unreachable in production)
  presentation eligibility consumes exact standing occurrence
  capture validation consumes presentation + response capture
  source recovery consumes representation + presentation + binding + selection
  meaning warrant consumes source recovery + testimony + convention
  BOGE applicability helper consumes exact meaning-warrant occurrence

CLI / API / DIAGNOSTIC CONSUMERS
  no fixed-probe CLI flag, API, or diagnostic consumer found;
  bare console exposes only the settled ingress boundary
```

## Inventory matrix

“Tests” below means direct construction/call unless stated otherwise.  “Generic
replay” means the common projector accepts a supplied historical Event, not that
a compatibility obligation was established.

| Symbol / Event / artifact | Current non-test producer | Current non-test consumer | Reachability | Replay dependency | Test-only standing | Constitutional classification | Present disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CapturedOperatorMaterial`; `_capture_representation(initial_ingress)` | persistent console / active attempt | representation examiner, active Event recording | actively reachable | active raw/examination Events project | active boundary tests | direct witness of representation examination; application ingress material | preserve now |
| `raw_material_captured`, `representation_examined`, `ingress_occurred` | active attempt | common projector/current console return | actively reachable | current and historical projection | active ingress boundary | direct witness of capture/examination/occurrence | preserve now |
| `initial_eof_occurred`, initial-failure/EOF `stopping_occurred` | active attempt branches | common projector and returned view | conditionally reachable | current and historical projection | active EOF/failure boundary | direct witness of ingress occurrence/local stopping | preserve now |
| `ApplicationSourceRoleTestimony`; `APPLICATION_POTENTIAL_GOAL_ROLE_TESTIMONY` | only module initialization; tail would consume | `_examine_potential_goal_standing` only | lexically present but unreachable after the PR 2097 return | serialized only in downstream standing Event | direct helper fixtures | application-local representation material / conditional implementation witness | candidate for bounded deletion |
| `ApplicationPotentialGoalStandingConvention`; singleton | only module initialization; tail would consume | `_examine_potential_goal_standing` only | lexically present but unreachable after the PR 2097 return | serialized only in downstream standing Event | direct helper fixtures | conditional implementation witness for a possible responsibility | candidate for bounded deletion |
| `_examine_potential_goal_standing`; `potential_goal_standing_examined` | no current producer | projector; unreachable eligibility helper | not called anywhere in non-test code | generic replay; SQLite synthetic test | independent helper contract + synthetic durable replay | conditional implementation witness | requires separate recovery |
| `ApplicationPresentationPurposeDeclaration`; `application_presentation_purpose` | tail only | eligibility examiner only | not called anywhere reachable in non-test code | serialized only in eligibility Event | direct helper fixtures | application-local representation material | candidate for bounded deletion |
| `ApplicationPresentationEligibilityConvention`; singleton | module initialization/tail only | eligibility examiner only | lexically present but unreachable after the PR 2097 return | serialized only in eligibility Event | direct helper fixtures | conditional implementation witness | candidate for bounded deletion |
| `_examine_presentation_eligibility`; `presentation_eligibility_examined` | no current producer | projector only after tail; no later tail query | not called anywhere in non-test code | generic replay | independent helper contract | conditional implementation witness for presentation eligibility | requires separate recovery |
| `CHOICE_SET_REF`, `PROMPT`, `OPTIONS`; `common_grammar_choice_set`; `render_probe` | tail only | tail representation/presentation/binding | not called anywhere reachable in non-test code | payload identities only | tests manufacture sole runtime uses | application-local representation material | candidate for bounded deletion |
| `probe_produced` | no current producer | projector; tail lineage | lexically present but unreachable after the PR 2097 return | generic replay | fixture/assertion only | historical scaffold / presentation occurrence support | candidate for bounded deletion |
| `AlternativeSourceRepresentation`; `common_grammar_representation_lineages`; fingerprint helpers; `alternatives_represented` | no current producer | projector; unreachable source recovery | not called anywhere in non-test code | generic replay | direct artifact distinction contract | mixed object: representation, exact-set participation, source testimony | mixed — split before disposition |
| `presentation_occurred` | no current producer | projector; unreachable capture validation and source recovery | lexically present but unreachable after the PR 2097 return | generic replay | fixture/assertion only | conditional presentation witness | requires separate recovery |
| response `_capture_representation`; `response_captured`; `response_eof_occurred` | no current producer | projector; unreachable capture validation | lexically present but unreachable after the PR 2097 return | generic replay | fixtures/direct validation | conditional capture/representation witness | requires separate recovery |
| `validate_capture_for_probe` | none | none outside tests; would call general binder | not called anywhere in non-test code | reads supplied ledger history, including SQLite | independent helper contract; tests manufacture prerequisites | application-local validation material | candidate for bounded deletion |
| `ClosedChoiceOption`, `PresentedClosedChoiceSet`, `OperatorSelectionTokenCapture`, `ClosedChoiceSelectionBinding`, `bind_closed_choice_selection`, serializer/fingerprint | no current non-test call/producer found | no current non-test semantic consumer; package export | not called anywhere in non-test code | binding testimony can be replayed as Event payload | separate module contract tests and island tests | direct witness of general exact-set binding; internal documented-by-code exported interface | preserve now |
| `binding_completed`, `unsupported_finding` | no current producer | projector; unreachable source recovery | lexically present but unreachable after the PR 2097 return | generic replay; SQLite synthetic consumed-capture test | fixture/assertion only | application Event wrapper around general binding | requires separate recovery |
| `alternative_selected` | no current producer | projector; unreachable source recovery | lexically present but unreachable after the PR 2097 return | generic replay | fixture/assertion only | conditional selection witness | requires separate recovery |
| `RecoveredRepresentedSource`; `_recover_represented_source`; `source_recovered`, `source_recovery_refused` | no current producer | projector; unreachable meaning warrant | not called anywhere in non-test code | generic replay | independent helper contract | mixed source-lineage recovery and application source assertion | mixed — split before disposition |
| `SOURCE_PROPOSITIONS`, `ALTERNATIVE_SOURCES`, `RENDERING_KNOWN_LOSS` | module constants only | island representation/recovery/testimony | no use outside island/tests | values may appear in old payloads | tests manufacture sole executable use | application-local source/representation material | candidate for bounded deletion |
| `ApplicationSourceMeaningTestimony`, `ApplicationSourceMeaningConvention`, `SOURCE_MEANING_TESTIMONIES`, `SOURCE_MEANING_CONVENTIONS` | module initialization only | unreachable warrant helper | not called anywhere reachable in non-test code | serialized in meaning Event | direct helper fixtures | application-local testimony plus conditional convention witness | mixed — split before disposition |
| `_warrant_source_meaning_relation`; `meaning_relation_warranted`, `meaning_relation_refused` | no current producer | projector; unreachable applicability helper | not called anywhere in non-test code | generic replay | independent helper contract | conditional implementation witness for meaning warrant | requires separate recovery |
| `_examine_meaning_relation_for_bounded_operator_goal_establishment`; applicability Events | no current producer | projector only | not called anywhere in non-test code | generic replay | independent helper contract | conditional implementation witness for consumer-local applicability | requires separate recovery |
| `examine_meaning_relation_applicability`, `MeaningRelationApplicabilityExamination` | no reachable non-test caller | island wrapper only; package-internal public-looking helper | not called anywhere in non-test code | none independently | direct helper contract via island | direct/conditional witness of BOGE consumer applicability, broader module | preserve now |
| `establish_bounded_operator_goal_from_closed_choice` | no current caller; always refuses | none | not called anywhere in non-test code | no Event handler | negative direct test | historical/negative boundary witness; broader exported BOGE API | preserve now |
| `establish_bounded_operator_goal_from_admitted_interpretation`; `BoundedOperatorGoalEstablishment`; serializer | no current producer call found | `bounded_advancement_horizon` consumes constructed BOGE artifacts; package export | not called anywhere in non-test code | artifact, not this Event family | separate BOGE tests | direct witness of independently applicable admitted-interpretation BOGE | preserve now |
| `stopping_occurred` as a whole | active initial branches; response variants unreachable | projector | mixed: active and unreachable variants | generic replay | active plus disconnected fixtures | mixed ingress/response local stopping | mixed — split before disposition |
| `project_operator_ingress_common_grammar_events`; state field and dispatch | arbitrary current/historical matching Event supplied to projector | `StateProjector.apply`, replayed current view, tests | actively reachable as projector | is the replay/projection mechanism | active projection and synthetic historical replay | representation/projection material, not semantic uptake | requires separate recovery |

## Event-by-Event production and consumption ledger

| Event kind | Production standing | Projection consumer | Later semantic consumer |
| --- | --- | --- | --- |
| `raw_material_captured` | current non-test producer (initial); response variant unreachable; tests | projector | initial examiner active; response validation unreachable |
| `representation_examined` | current non-test producer (initial); response variant unreachable; tests | projector | active ingress branch; response parsing unreachable |
| `ingress_occurred` | current non-test producer | projector | none after the unconditional return |
| `initial_eof_occurred` | conditional current producer | projector | active local-stop branch |
| `stopping_occurred` | conditional current producer for initial failure/EOF; response producers unreachable | projector | none |
| `potential_goal_standing_examined` | unreachable historical producer; test fixture producer | projector | unreachable eligibility helper |
| `presentation_eligibility_examined` | unreachable historical producer; test fixture producer | projector | none; tail does not retain its return |
| `probe_produced` | unreachable historical producer; test fixture producer | projector | unreachable presentation lineage |
| `alternatives_represented` | unreachable historical producer; test fixture producer | projector | unreachable source recovery |
| `presentation_occurred` | unreachable historical producer; test fixture producer | projector | unreachable validation/source recovery |
| `response_captured` | unreachable historical producer; test fixture producer | projector | unreachable validation/binding |
| `response_eof_occurred` | unreachable historical producer; test fixture producer | projector | unreachable response stop |
| `binding_completed` | unreachable historical producer; test fixture producer | projector | unreachable source recovery |
| `unsupported_finding` | unreachable historical producer; test fixture producer | projector | none after rendering branch |
| `alternative_selected` | unreachable historical producer; test fixture producer | projector | unreachable source recovery |
| `source_recovered` | unreachable historical producer; test fixture producer | projector | unreachable meaning warrant |
| `source_recovery_refused` | unreachable historical producer; test fixture producer | projector | unreachable refusal-shaped meaning examination |
| `meaning_relation_warranted` | unreachable historical producer; test fixture producer | projector | unreachable BOGE applicability examination |
| `meaning_relation_refused` | unreachable historical producer; test fixture producer | projector | none |
| `bounded_operator_goal_establishment_applicability_examined` | unreachable historical producer; test fixture producer | projector | none; no admission or BOGE follows |
| `bounded_operator_goal_establishment_applicability_refused` | unreachable historical producer; test fixture producer | projector | none |

Thus every downstream kind has a handler but no current producer.  Several have
unreachable later semantic consumers, while `presentation_eligibility_examined`,
the final applicability family, refusals, unsupported findings, and closing
occurrences have only representation/projection consumers after they are made.

## Durable replay standing

Evidence found:

1. `EventLedger` describes append-only runtime history; `SQLiteEventLedger`
   stores kind and JSON payload without a per-kind schema table and reloads all
   rows through the same public API.
2. `StateProjector.apply` currently dispatches every
   `operator.ingress.common_grammar.*` Event to the handler.  Consequently a
   user-provided current `--db` ledger containing a structurally valid historical
   downstream Event can be replayed today.
3. `test_sqlite_reconstructed_standing_is_consumed_and_survives_replay` and
   `test_consumed_capture_refusal_and_durable_replay` create temporary SQLite
   databases and prove exact helper/replay behavior.

Evidence **not** found: an actual repository `.db`/`.sqlite` fixture; a downstream
Event schema version; a migration; a retention or backwards-compatibility policy;
a documented public promise naming these Event kinds; or a CLI/API assertion that
historical downstream common-grammar Events must remain readable.  The generic
SQLite behavior is current functionality, but the repository does not establish
whether it is a compatibility obligation.  The honest classification is:
technical replay exists; documented durable replay obligation **Unknown / none
found**.  A replay decision is required before deleting the Event handlers or
state shape, but not before deleting only unreachable producer statements whose
removal leaves replay intact.

## External interface standing

* The fixed probe has no parser option, diagnostic inventory entry, HTTP/API
  surface, or dedicated CLI.  Bare `seed` enters a persistent console and calls
  the named attempt, but decoded non-EOF input returns before the fixed probe is
  built or displayed.  `test_parser_has_no_alternate_operator_ingress_controller`
  confirms there is no alternate controller.
* `operator_ingress_common_grammar_prerequisite` symbols are absent from
  `seed_runtime.__all__`.  The script imports only the run function.  Public-looking
  helper names are therefore internal, not a documented supported API; underscore
  helpers are module-private with test imports.
* Closed-choice types/functions and BOGE types/functions are explicitly imported
  and listed in `seed_runtime.__all__`.  That is external package-export evidence,
  although no stability/version promise was found.  They must not be swept away
  with the application island without separate interface recovery.

## Constitutional responsibility standing

The Book recognizes distinctions around translation, candidate formation,
closed-choice presentation, selection binding, source recovery, meaning warrant,
applicability, admission, BOGE, and stopping.  It also expressly leaves the exact
upstream common-grammar act and responsible owner Unknown.  Therefore:

* general closed-choice binding and admitted-interpretation BOGE are the strongest
  independent implementation witnesses;
* standing, eligibility, meaning, and applicability examiners are conditional
  witnesses for possible responsibilities, not proof that this first-contact
  application road is applicable;
* fixed choices, source declarations, role testimony, labels, renderings, and
  source maps are application-authored representation material;
* representation rows and recovered-source objects are mixed: they preserve
  constitutional distinctions but bake in application identities/propositions;
* the common projector is representation/replay machinery, not constitutional
  semantic uptake;
* no translation, candidate-formation producer, consumer-local admission, or
  positive BOGE establishment occurs in the tail.

No Book correction is warranted by this recovery.  The Book's recognition of a
possible responsibility does not require this exact island, and no contradiction
requiring correction was established.

## Test standing

### Active production witnesses

* `test_initial_eof_records_eof_and_separate_stop_without_probe`;
  `test_decoded_non_eof_ingress_returns_after_preservation_and_projection`;
  `test_console_recurs_after_each_quiescent_non_eof_attempt`;
  bare-console/capture/provenance/representation tests through
  `test_representation_evidence_produces_no_broader_standing` witness the settled
  ingress boundary, outer-console recurrence, exact bytes, strict decoding, and
  the absence of downstream claims.
* Source-text tests asserting the absence of PESC/source-relative claims are
  active-topology guards, not downstream execution witnesses.

### Disconnected helper witnesses

* Standing and eligibility tests at lines 128–599 directly call private helpers.
  They witness independent bounded contracts, plus one synthetic SQLite replay;
  they do not witness the current console road.
* Tests from `test_direct_representation_and_source_recovery_preserve_exact_distinctions`
  through the meaning/source-recovery refusal matrices directly manufacture
  choice sets, Events, and application artifacts.  They witness helper contracts
  and artifact distinctions only.
* The applicability tests directly call the private wrapper and witness only the
  exact meaning-warrant consumer boundary.
* Capture-validation tests manufacture presentation/capture Events; the durable
  test manufactures the only historical binding use in a temporary database.
* `test_direct_closed_choice_binding_is_not_positive_boge_admission` witnesses a
  negative general boundary, not production topology.

Several production helpers now appear executable only because tests construct
their prerequisite artifacts and call them: all tail examiners, representation
and recovery helpers, choice-set/render helpers, and probe-specific capture
validation.  This is not a reason by itself either to retain or delete them.
The tests do **not** encode obsolete production topology when they accurately say
“direct”; any older assertions expecting the downstream road to execute were
replaced by PRs 2098–2099.  Their standing is independent helper contract,
application-local artifact distinction, or synthetic historical replay.

## Deletion analysis

### Candidate 1 — the unreachable orchestration tail

* **Remove:** statements from `_examine_potential_goal_standing` at line 1769
  through the final tail return at line 2185, leaving the settled return.
* **Current non-test behavior:** none; no instruction is executable.
* **Replay behavior:** none if the projector/state field remain.
* **Tests:** active boundary tests remain; source-inspection assertions may be
  simplified.  Direct helper-contract tests need not be removed merely because
  orchestration is removed.
* **New dead material:** most island constants, declarations, serializers, and
  helpers become clearer deletion candidates; general closed-choice/BOGE modules
  do not.
* **Possible lost distinction:** only a historical lexical example tying the
  responsibility sequence together, not an active constitutional occurrence.
* **Safety:** **presently safe and smallest** given the exact unconditional return
  and absence of any jump/dynamic entry into function interiors.

### Candidate 2 — application-authored fixed source/representation family

* **Remove:** `CHOICE_SET_REF`, prompt/options, source proposition/maps,
  rendering loss, fixed role/purpose/meaning declarations and singleton
  conventions, choice-set/render/representation helpers and local serializers.
* **Current non-test behavior:** none after Candidate 1; today none beyond import
  construction.
* **Replay behavior:** existing payloads remain projectable if handler logic does
  not import these constants; direct semantic re-examination of old Events would
  no longer be available.
* **Tests:** application-local construction, exact-ref/fingerprint, testimony,
  eligibility, meaning and representation tests would be removed or rewritten.
* **New dead material:** recovery/warrant/validation wrappers and imports from the
  general binding module.
* **Possible lost distinction:** tests currently preserve valuable separations
  among application testimony, constitutive convention, presentation eligibility,
  representation, source recovery, and meaning warrant.
* **Safety:** not yet sufficiently specified as one deletion.  It is mixed and
  should be decomposed/recovered after tail deletion rather than deleted en bloc.

### Candidate 3 — probe-specific binding/selection/recovery helper family

* **Remove:** `validate_capture_for_probe`, application Event wrappers for binding,
  selection and recovery, `RecoveredRepresentedSource`, and recovery helper.
* **Current non-test behavior:** none.
* **Replay behavior:** unchanged if handlers remain; ability to re-run semantic
  validation against historical ledgers disappears.
* **Tests:** direct capture validation, consumed-capture SQLite, and source-recovery
  matrices removed/rewritten.
* **New dead material:** local binding serializers, representation fingerprint,
  source maps, and several imported closed-choice types.
* **Possible lost distinction:** general exact-set binding must stay separate from
  application validation and represented-source recovery.
* **Safety:** requires separate recovery.  Do not delete the exported general
  `closed_choice_selection_binding` module as part of this boundary.

### Candidate 4 — downstream Event family plus projector/state support

* **Remove:** downstream kind branches, projected subjects/payload copying, and
  perhaps the whole attempt view if active kinds are migrated elsewhere.
* **Current non-test behavior:** active projection must be retained or split;
  removing the whole handler would break the settled road.
* **Replay behavior:** historical downstream Events cease to project and may raise
  on missing expected payload/subject mappings depending on the exact split.
* **Tests:** all synthetic historical projection/SQLite tests must be decided, not
  casually removed.
* **New dead material:** state field/dispatch only if active kinds receive another
  projection owner.
* **Possible lost distinction:** historical projection visibility, but no current
  semantic consumer uptake.
* **Safety:** premature until a deliberate replay-compatibility decision and a
  split between active and downstream kinds.

### Candidate 5 — general closed-choice and BOGE modules

* **Remove:** exported general artifacts and serializers, including the admitted
  interpretation BOGE road.
* **Current non-test behavior:** direct calls were not found, but BOGE artifacts
  participate in the separate bounded-advancement-horizon family and both modules
  are package exports.
* **Replay behavior:** not principally this Event family.
* **Tests/imports:** multiple independent modules and tests change.
* **Possible lost distinction:** independently applicable binding, admission,
  goal-establishment, and advancement boundaries.
* **Safety:** clearly premature and outside a coherent island deletion.

## Direct answers

1. **Disconnecting line/branch:** the unconditional decoded-non-EOF `return
   state.operator_ingress_common_grammar_attempts[attempt]` at
   `operator_ingress_common_grammar_prerequisite.py:1767`, after projection and
   after the EOF branch.
2. **Anything below reachable from this function?** No.  Python has no label/jump
   entry and the return dominates every following statement.
3. **Other non-test caller?** No other caller of the orchestration or downstream
   helpers was found.  Projector dispatch is an independent representation path,
   not a helper-producer call.
4. **Helpers with no non-test callers:** every downstream helper named in topology
   C, including the standing, eligibility, construction/render, representation,
   validation, recovery, meaning, and applicability wrappers.
5. **Independent non-test callers:** none for downstream helpers.  The projector
   has independent `StateProjector.apply` dispatch; that is a replay consumer.
6. **Downstream kinds with a non-test producer:** none.  Only the settled active
   kinds, plus conditional initial EOF/stopping, have current producers.
7. **Only test-fixture producers:** all 16 strictly downstream kinds listed in the
   Event ledger table (while lexical historical `_record` sites remain).
8. **Handlers but no producer:** every strictly downstream kind.
9. **Later semantic consumers:** standing, presentation, response capture,
   binding, selection, representation, recovery, and warranted meaning have the
   unreachable consumers shown in topology D.
10. **Only representation/projection consumers:** eligibility result, unsupported
    and refusal terminal findings, final applicability results, and closing Events;
    `probe_produced` additionally supplies unreachable lineage.
11. **Supported CLI/API exposes fixed probe?** No.  Bare console exposes ingress,
    but the fixed choice probe is unreachable; no option/API/diagnostic exists.
12. **Documented public API requires helpers?** None found for island helpers.
    General closed-choice/BOGE names are package exports and require separate care.
13. **Durable contract requires handlers?** No explicit contract found; technical
    generic SQLite replay exists.  Compatibility obligation remains Unknown.
14. **Current database/fixture requiring readability?** No repository database
    fixture found.  Only temporary test databases establish technical replay.
15. **Source constants outside island?** No production use outside this module;
    tests import/construct against them and Book prose discusses concepts, not refs.
16. **Closed-choice broader?** Yes as a separately exported general exact-set
    artifact/serializer with its own tests; no independent reachable caller found.
17. **BOGE broader?** Yes: admitted-interpretation establishment, exported artifact,
    and advancement-horizon consumption are separate; current producer call absent.
18. **Meaning/applicability specificity?** Meaning testimony/warrant wrappers are
    specific to this source road.  `examine_meaning_relation_applicability` belongs
    to broader BOGE but currently is called only by this island wrapper.
19. **Mixed objects:** `AlternativeSourceRepresentation`,
    `RecoveredRepresentedSource`, meaning testimony/convention family,
    `stopping_occurred`, common projected attempt view, and application wrappers
    around general binding/applicability.
20. **Tests witnessing active production:** initial EOF, decoded non-EOF return,
    console recurrence/exit/capture, raw bytes, decoding and no-broader-standing
    tests identified above.
21. **Disconnected-only tests:** standing/eligibility, representation/recovery,
    meaning/warrant/applicability and capture-validation clusters.
22. **Tests manufacture only use?** Yes, for every downstream helper; SQLite tests
    manufacture the only durable downstream histories visible in-repository.
23. **Smallest safe deletion:** the unreachable orchestration statements only,
    lines 1769–2185, preserving helpers, Events and projection pending recovery.
24. **Premature deletion:** the whole mixed island, projector/Event family,
    general closed-choice module, or broader BOGE implementation.
25. **Replay decision required?** Before deleting handlers/state compatibility,
    yes.  Before deleting only unreachable orchestration, no replay changes occur.
26. **Book correction required?** No evidence requires one.
27. **Production deletion sufficiently specified?** Yes only for the unreachable
    orchestration-tail candidate; not for the entire island.
28. **Next smallest honest inch:** a separate deletion PR removing only the dead
    tail, with active-boundary tests, followed by a bounded replay-policy recovery
    and then decomposition of application-local artifacts from general witnesses.

## Final disposition

```text
active downstream production road:
    none; the active road ends at projected ingress occurrence and quiescent return

independent non-test downstream callers:
    none; only the common Event projector has an independent replay call path

downstream Event production:
    no current non-test producer; unreachable lexical producers and test fixtures only

projection/replay consumers:
    StateProjector → project_operator_ingress_common_grammar_events → attempt view;
    SQLiteEventLedger can reload structurally valid historical Events

documented replay obligation:
    none found; technical generic replay exists, compatibility obligation Unknown

test-only helper standing:
    bounded direct contracts, application-artifact distinctions, and synthetic replay;
    not production reachability or applicability

smallest safe deletion candidate:
    unreachable orchestration statements at lines 1769–2185 only

premature deletion boundary:
    mixed helper/Event/projector island, exported general closed-choice, or broader BOGE

Book change now:
    none

production change now:
    none in this report-only PR

next honest inch:
    separately delete only the unreachable tail, then recover replay policy before
    splitting application-local artifacts from conditional/general witnesses
```
