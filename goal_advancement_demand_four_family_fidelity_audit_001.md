# Four-family goal-advancement Demand Fidelity audit 001

## 1. Boundary, method, and governing answer

This is one bounded, report-only audit at commit `be1d14c`, after PR 2017. It
changes no Book, root documentation, `docs/`, prior report, runtime code, test,
API, diagnostic, event, persistence, or cluster state. Symbol searches count an
export as an export and a test fixture as a test occurrence, never as a
production occurrence.

**Governing answer:** none of the four local projections has a production
producer. All requirement and standing records are caller-authored testimony;
all concrete constructors and projector calls are in tests. The projectors are
real, externally callable, read-only classifiers and the shared assemblers are
real, externally callable consumers, but no runtime orchestration calls them.
Thus the four roads are **test-supported architectural scaffolding with no
production producer or occurring consumer**, not active implementation
witnesses. Inquiry alone has a longer implemented downstream compatibility
road (reference -> consideration selection -> bounded inquiry frontier), and
all four can feed sufficiency, but those too have no non-test caller. This is
an implementation asymmetry, not production activity.

The canonical Book warrants the four Demand *families* as local vocabulary; it
does not warrant these particular caller-declaration projectors. Canonical
legitimacy and implementation occurrence are separate findings.

## 2. Exact topology and producer/consumer matrix

Legend: **P** production-active; **E** externally callable only; **T**
test-active only; **V** presentation-only; **C0** consumerless; **A** absent.

| Family | Source occurrence | Requirement testimony | Standing/blocker testimony | Demand projection | Demand set branch | Downstream consumer | Constrained action / STOP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clarification | A; no observer/deriver | T constructor; there is no separate requirement side | T `OperatorMeaningUncertaintyTestimony` combines uncertainty and standing | E + T | E + T optional `clarification=` storage | E generic reference/sufficiency only; no family-specific caller | A action; STOP before clarification request |
| inquiry | A; repository/world observations do not produce this testimony | T constructor; no separate requirement side | T `RepositoryWorldUncertaintyTestimony` combines uncertainty and standing | E + T | E + T optional `inquiry=` storage | E reference, consideration selection, sufficiency, and inquiry-frontier compatibility; only tests instantiate the chain | E compatibility classification only; A inquiry opening; STOP |
| authority | A | T `AuthorityRequirementTestimony` | T `AuthorityStandingTestimony` | E + T | E optional `authority=` branch; branch tested only as absent/excluded | E generic reference/sufficiency; no concrete authority-chain caller | A request/grant/authorization; STOP |
| operational realization | A | T `OperationalRealizationRequirementTestimony` | T `OperationalRealizationStandingTestimony` | E + T | E optional `operational_realization=` branch; no supplied specimen in set test | E generic reference/sufficiency; no realization consumer | A selection/warrant/realization; STOP |

Exact common path:

```text
no production source occurrence
  -> caller declares testimony (tests are the only concrete callers)
  -> projector validates identity/membership and applies a compiled table
  -> family-local Demand bucket
  -> optional GoalAdvancementDemandSet family record
  -> reference projection and/or sufficiency projection (callable, not called)
  -> [inquiry only] consideration selection -> frontier compatibility (tests only)
  -> STOP: no clarification, inquiry opening, authority act, realization, or movement
```

### Non-test callers and consumers

There are **zero non-test calls** to any of the four family projectors or to
`assemble_goal_advancement_demand_set`. There are also zero non-test calls to
the sufficiency projector. Production modules import the types only to define
callable consumers.

| Consumer implementation | Exact conclusion used | Decision constrained | Ordering / sufficiency | Standing distinctions | Performs work? |
| --- | --- | --- | --- | --- | --- |
| `GoalAdvancementDemandSet` assembler | none; stores the supplied projection object and disposition | identity refusal only when opt-in flag is true | neither | distinguishes supplied/absent/excluded and identity conflict, but does not inspect family buckets | No; merely stores optional records |
| Demand-reference projector | every native bucket and native standing | `selectable=True` only for bucket and standing both `established` | no ordering or sufficiency | preserves established, unsupported, unknown, conflicting, family-specific outside/unclassified-here, and unclassified | Presents references; no movement |
| Sufficiency projector | established -> insufficient; conflict -> conflicting; unknown or absent -> unknown | bounded sufficiency label | evaluates sufficiency, never family priority | consumes established/conflicting/unknown and absence/exclusion; ignores unsupported, `unclassified_here`, and `unclassified` except indirectly through coverage | Classification only |
| Consideration selector | reference `selectable` and exact identity evidence | chooses one established Demand for consideration | no family ordering; caller evidence names the reference | rejects nonselectable states collectively; does not independently interpret their semantics | Selection for consideration only |
| Bounded inquiry frontier | selected reference must be family `inquiry` | local clause-coherence state | no Demand ordering/sufficiency | selected/non-selected plus its separate clause standings | Compatibility only; it explicitly does not formulate/open inquiry |

Only inquiry can cross from a selected Demand reference into the frontier
assembler. This is not a real runtime producer/consumer contrast: both ends
remain fixture-driven. There is therefore **no family with a real runtime
producer to compare against a fixture-only family**; that requested contrast
itself exposes the common missing ingress.

## 3. File ownership and exact LOC

LOC is physical `wc -l` at the audited commit. “Owned” means the file defines
the family surface, not that a production responsibility occurs there.

| Family | Direct production owner | LOC | Focused test owner | LOC | Shared owners attributable to all four |
| --- | --- | ---: | --- | ---: | --- |
| clarification | `seed_runtime/clarification_demand_projection.py` | 196 | `tests/test_clarification_demand_projection.py` | 17 | demand set 266; reference set 196; sufficiency 202; exports in `__init__.py` |
| inquiry | `seed_runtime/inquiry_demand_projection.py` | 196 | `tests/test_inquiry_demand_projection.py` | 17 | same shared 664 LOC, plus consideration selector 270, frontier testimony 185, frontier 265 |
| authority | `seed_runtime/authority_demand_projection.py` | 180 | `tests/test_authority_demand_projection.py` | 19 | same shared 664 LOC |
| operational realization | `seed_runtime/operational_realization_demand_projection.py` | 262 | `tests/test_operational_realization_demand_projection.py` | 17 | same shared 664 LOC |

Shared tests inspected: demand-set 29 LOC, reference-set 11 LOC,
consideration-selection 11 LOC, inquiry-frontier testimony 16 LOC, and bounded
inquiry-frontier 12 LOC. The package export file is shared infrastructure and
was not assigned fractionally. PR 2017 added only a 357-LOC prior report; it
changed no runtime or test surface under this audit.

## 4. Field-level provenance, defaults, use, and loss

### Common identity, applicability, ownership, evidence, and Unknown fields

| Field/dimension | Producer status | Projector use | Preservation/loss |
| --- | --- | --- | --- |
| testimony identity | caller-declared; duplicate uniqueness never enforced | payload identity and/or item lineage | copied; duplicate refs can corrupt first-match `used` tracking in paired families |
| `source_ref` | caller-declared opaque pointer | unused | dropped in every projection item |
| goal and horizon IDs | copied from caller's goal/horizon in fixtures | exact identity gate | projection carries goal/horizon; item drops them |
| `evidence_ref` | caller-declared opaque pointer | **membership only** in horizon evidence refs | copied; membership is presented beside Demand but support is never resolved |
| component/subject/transformation/class/scope refs | caller-declared opaque identities | nonempty gates and paired join keys | selected identities copied; semantics never inspected |
| `owning_stage` | caller-declared; no owner registry or authority check | nonempty gate and paired equality | copied, but authority to testify is absent |
| family/type | positively defaulted | exact family gate | dropped as an explicit provenance fact |
| boundedness | positively defaulted `True` | truth gate | dropped; no indication it was defaulted |
| applicability | positively defaulted where represented | only positive value passes | output copies positive paired value; nonpositive values collapse to coarse unclassified |
| materiality | positively defaulted where represented | only positive value passes | same collapse; no derivation or default provenance |
| notes | caller-declared | unused | dropped everywhere |
| explicit Unknown/conflict | caller-declared enum | table input or first failing structural gate | bucket survives only when it reaches table; applicability/materiality Unknown/conflict becomes `unclassified` |

Opaque evidence-reference membership is indeed presented as evidentiary
support: the horizon inventory and item references are emitted, yet the code
checks no contents, relation, source authority, freshness (except preserving
inquiry labels), or support strength. It proves address membership, not that
evidence supports the testimony or Demand.

### Family-specific comparison

| Family | Semantic fields and provenance | Positive defaults | Used to conclude | Dropped or compressed |
| --- | --- | --- | --- | --- |
| clarification | caller declares uncertainty family, standing, owning stage, bounded component, stage ownership, materiality, mixedness | family, stage ownership, boundedness, materiality | valid item copies caller's standing directly; horizon exclusion overrides it | source, family, ownership flag, bounded/material flags, mixed flag, notes; no separate requirement standing |
| inquiry | same plus repository/world subject, evidence freshness and availability | family, stage ownership, boundedness, materiality, freshness=`current`, availability=`available` | valid item copies standing directly; exclusion overrides it | source, family, ownership/bounded/material/mixed flags, notes; freshness/availability preserved but do not affect Demand |
| authority requirement | requirement, authority class, scope, owner, applicability, materiality are caller declarations | family, boundedness, applicable, material | requirement is one side of `_conclude` | source, family, boundedness, notes, selected-source context |
| authority standing | authority standing and optional selected authority source are caller declarations | family, boundedness, applicable, material | `required + unavailable => established`; `required + available => unsupported` | `selected_authority_source_ref` is unused/dropped; no authority producer/currentness |
| realization requirement | required transformation and requirement standing are caller declarations | family, boundedness, applicable, material | requirement is one table side | source, family, boundedness, notes |
| realization standing | availability, coverage, blocker ownership and all optional candidate/reachability/selection/warrant/applicability/dependency/behavior refs are caller declarations | family, boundedness, applicable, material | complete unavailable owned by realization establishes; other-family blocker is unclassified-here | every optional support ref, source, notes, and testimony kind are unused/dropped |

No field is observed or evidence-derived by these roads. IDs are copied;
bucket outcomes and stable IDs are compiled; semantic standings are
caller-declared; positive family/boundedness/applicability/materiality (and
inquiry evidence quality) are defaulted.

## 5. Eight-dimensional Fidelity comparison

| Dimension | Clarification | Inquiry | Authority | Operational realization |
| --- | --- | --- | --- | --- |
| 1 subject/identity | component only; partial | component + subject; partial | component + authority class + scope; partial | component + transformation + scope; partial |
| 2 source occurrence | absent | absent | both producers absent | both producers absent |
| 3 evidence/provenance | opaque membership; source dropped | same; caller-default freshness retained | two opaque refs; sources dropped | two opaque refs; all support refs dropped |
| 4 applicability/materiality | caller/default booleans | caller/default booleans | caller/default enums on both sides | caller/default enums on both sides |
| 5 coverage/sufficiency | no coverage dimension | evidence availability is not coverage | no coverage/currentness | caller declares horizon coverage; no covered set |
| 6 ownership/authority | free stage + default ownership bool | same | paired free stage, not testimonial authority | paired stage + caller-owned blocker family |
| 7 conflict/Unknown | explicit label only; structural states coarse | same; evidence quality does not constrain Demand | explicit labels; contradictory matches not compared | explicit labels; contradictory matches not compared; other family gets `unclassified_here` |
| 8 consumer/constrained act | generic classification only | longest compatibility chain, still no inquiry act | generic classification only | generic classification only |

All four have partial identity/classification fidelity and poor occurrence,
evidentiary, authority, currentness, and conflict fidelity. Inquiry's richer
downstream shape is the only retention asymmetry, but it is not an occurring
producer or constitutional inquiry-opening witness.

## 6. Asymmetric cross-examination

1. **Runtime producer versus fixtures:** no positive specimen exists. Every
   family is fixture-only at ingress. Inquiry has more runtime *definitions*,
   not a runtime occurrence.
2. **Missing testimony:** clarification/inquiry with no testimony yield empty
   projections. Authority/realization requirement without standing becomes
   unclassified; standing without requirement becomes unclassified. None
   establishes Demand or a STOP act.
3. **Caller-declared positive standing without producer:** clarification or
   inquiry `standing="established"` is copied straight to established after
   gates. Authority `available` produces unsupported Demand, while realization
   `available` does the same, with no supporting availability producer.
4. **Positive defaults:** all families default their family, boundedness, and
   materiality/applicability gates positively. Inquiry additionally defaults
   evidence fresh/current and available, although these labels do not alter its
   Demand conclusion.
5. **Contradictory matching testimony:** clarification/inquiry preserve two
   contradictory caller records in separate buckets without computing a
   conflict. Authority/realization choose `matches[0]`; the second match becomes
   an unmatched unclassified item rather than conflicting the first Demand.
6. **Blocker owned by another family:** realization unavailable with authority,
   clarification, inquiry, or generic ownership becomes `unclassified_here`.
   No handoff is produced and sufficiency does not explicitly consume that
   state.
7. **Established with no consumer:** all four can emit established; generic
   reference/sufficiency code can read it, but no occurring downstream caller
   exists. Inquiry's potential chain still ends before opening inquiry.
8. **Absent record versus explicit unsupported:** assembler absence becomes an
   `absent` record and sufficiency Unknown; supplied unsupported has no
   established/unknown/conflict reason and can contribute to sufficiency only
   if separate coverage is complete. They are distinct, but neither is an act.
9. **Canonical but absent operationally:** the Book lawfully names all four;
   implementation has no operational producers for any. Book warrant cannot
   manufacture those crossings.

## 7. Family-wide contamination finding

The repeated pattern is exact:

* caller authors the relevant semantic side (and both sides for authority and
  realization);
* projector gates caller fields and applies a compiled truth table;
* output calls that classification Demand;
* assembler stores optional family records;
* no occurring runtime consumer acts on them.

This is **compiled demand simulation / orphaned scaffolding**, with a limited
lawful kernel: it can truthfully project *explicit boundary testimony* if an
external responsible caller exists. The repository, however, supplies neither
that producer nor a reliance authority, and drops the provenance needed to
distinguish lawful testimony from arbitrary declaration. Therefore it is not
an active implementation witness. Calling the whole road lawful boundary
testimony projection would overstate the evidence; calling it merely
incomplete would understate its current consumerlessness.

First-match behavior, duplicate identities, contradictory records, positive
defaults, dropped sources/support refs, and coarse `unclassified` handling are
family-wide fidelity hazards. This audit does not repair them.

## 8. Deletion and preservation topology

### Deletion topology for consumerless scaffold

If maintainers choose cleanup, delete leaf-to-root, in one separately tested
change:

1. clarification module and focused test;
2. authority module and focused test;
3. operational-realization module and focused test;
4. inquiry frontier/selection chain only after confirming no external API
   contract, then inquiry projection and focused tests;
5. remove each family's reference buckets, lineage/standing branches,
   sufficiency branches, demand-set union/optional parameter/family inventory,
   JSON shape assertions, package imports and `__all__` exports;
6. when no family remains, remove the shared demand set, reference set,
   coverage/sufficiency scaffold and their tests.

Do not delete the canonical Demand families from the Book merely because these
implementations are dormant. Do not alias or migrate them to a generic engine.

### Preservation topology for truthful active material

There is no demonstrated production-active family material to preserve. The
smallest potentially truthful material is the distinction between native
standings, explicit Unknown/conflict, absent versus excluded family, exact
goal/horizon identity, read-only behavior, and inquiry's refusal to equate a
selected Demand with an opened inquiry. Preserve those semantics only if an
external caller contract or imminent producer is evidenced before deletion.
Exports and tests alone are insufficient preservation warrants.

## 9. Cleanup judgment and STOP conditions

**Implementation cleanup is warranted for consideration, not execution in
this audit.** The evidence favors deleting orphaned scaffolding rather than
inventing four producers merely to complete symmetry. Inquiry deserves an
individual retention review because it alone has a downstream compatibility
consumer; that is not enough by itself to retain it. No other family has a
retention asymmetry beyond richer testimony shape.

STOP this audit now and preserve Unknown/refusal when:

* no production producer occurrence and responsible owner are evidenced;
* evidence-reference membership is offered as proof of semantic support;
* testimony is missing, duplicated, contradictory, stale, inapplicable, or
  materially Unknown;
* applicability/materiality/coverage/ownership is only a positive default or
  unsupported caller declaration;
* a second matching testimony would be discarded by first-match behavior;
* a blocker belongs to another family and no responsible handoff exists;
* a family record is absent: do not read absence as unsupported or satisfied;
* Demand is established: STOP before clarification, inquiry opening, authority
  request/grant, realization selection, authorization, execution, recording,
  event writing, persistence, or mutation;
* cleanup would require a replacement, alias, migration, generic Demand
  engine, new producer, selector, CLI, diagnostic, event, or mutation;
* external usage evidence appears; reassess before deletion.

## 10. Exact files inspected and report LOC

Files inspected directly:

* `AGENTS.md`
* `book_of_seed/03-goals-and-advancement/README.md`
* `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md`
* `book_of_seed/03-goals-and-advancement/selection-and-authorization.md`
* `seed_runtime/__init__.py`
* `seed_runtime/bounded_advancement_horizon.py`
* `seed_runtime/clarification_demand_projection.py`
* `seed_runtime/inquiry_demand_projection.py`
* `seed_runtime/authority_demand_projection.py`
* `seed_runtime/operational_realization_demand_projection.py`
* `seed_runtime/goal_advancement_demand_set.py`
* `seed_runtime/goal_advancement_demand_reference_set.py`
* `seed_runtime/goal_advancement_demand_consideration_selection.py`
* `seed_runtime/goal_advancement_demand_family_coverage_set.py`
* `seed_runtime/goal_advancement_sufficiency_projection.py`
* `seed_runtime/inquiry_frontier_boundary_testimony.py`
* `seed_runtime/bounded_inquiry_frontier.py`
* `tests/test_clarification_demand_projection.py`
* `tests/test_inquiry_demand_projection.py`
* `tests/test_authority_demand_projection.py`
* `tests/test_operational_realization_demand_projection.py`
* `tests/test_goal_advancement_demand_set.py`
* `tests/test_goal_advancement_demand_reference_set.py`
* `tests/test_goal_advancement_demand_consideration_selection.py`
* `tests/test_inquiry_frontier_boundary_testimony.py`
* `tests/test_bounded_inquiry_frontier.py`
* `operational_realization_availability_testimony_fidelity_recovery_001.md`
  (prior report, navigation/counterevidence only)

Repository-wide `rg` symbol searches over production and tests established the
callers, constructors, exports, and consumers. `git log`, `git show`, and
physical LOC counts established the post-PR-2017 boundary and ownership. Only
this report is added. **Report LOC added: 304** (`wc -l`).
