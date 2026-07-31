# Operator-Ingress Interpretation-Candidate Supplier, Applicability, and Consumer Fidelity Recovery 001

## 0. Status, scope, method, and answer in brief

This is one bounded, report-only Fidelity recovery after PR 2120. It changes no
Book text, implementation, tests, Events, projection, CLI, runtime wiring,
schema, identifier, or earlier report. The Book is constitutional testimony;
current code, tests, imports, call sites, and history are implementation
testimony. Earlier PR claims are not treated as authority.

The governing answer is **negative/Unknown**. The Book permits attributed
candidate testimony from a Seed producer, the operator, an external source, or
another producer whose identity may remain Unknown, but it does not assign one
universal producer. Current production identifies no non-test supplier,
producer of proposed meaning, preservation caller, applicability examiner, or
candidate-set consumer. `SuppliedInterpretationCandidateTestimony` is therefore
an implementation-local explicit-caller shape, not a recovered constitutional
supplier contract.

The preservation function is an explicit, constructible boundary utility. If
called, it faithfully copies caller testimony, derives narrow field-absence
findings, validates carrier invariants, and returns a deterministic read-only
artifact. It is not on the active ingress road, records no occurrence, and is
not consumed by contextual warrant production, selection, projection, replay,
BOGE, Demand, or diagnostics. The earliest missing relation is not a generator:
it is evidence of an exact responsible consumer and purpose whose requirements
make preservation applicable. Until that relation is recovered, production
work is not sufficiently specified.

### Evidence examined

Implementation inspection covered the required four modules; focused tests;
all repository references to the four named carrier/functions; carrier users;
state projection dispatch; JSON reconstruction; serializers; constructors; and
non-test imports/calls. The search found candidate-boundary symbols only in
`seed_runtime/operator_ingress_interpretation_candidates.py` and its focused
test, except for the imported addressable-material and shared carrier types.

Book inspection was bounded to:

* `01-grammar-and-standing/external-and-constitutional-grammar.md`, especially
  `01.External.A--G`;
* `constitutional-kinds-and-artifact-standing.md`, especially
  `01.Standing.A--F`;
* `constructors-and-production-authority.md`;
* `lenses-views-and-roads.md`, especially consumer-local uptake;
* `05-evidence-and-knowledge/testimony-and-established-fact.md` and
  `recording-and-knowledge-extraction.md`;
* `02-acts-and-constraints/acts-and-act-artifacts.md`; and
* the operator-ingress common-grammar prerequisite only where it distinguishes
  candidate formation, warrant, selection, applicability, admission, and BOGE.

Historical reports were used only to locate questions and contradictions. In
particular, a historical statement about an operator/caller candidate does not
override current `01.External.F`, which deliberately leaves source roles open.

## 1. Governing constitutional recovery

The Book warrants these limited conclusions:

1. External material can become addressable without becoming constitutional
   grammar or truth. Attribution, source role or Unknown, provenance or Unknown,
   scope, uncertainty, and authority limits must survive lawful consumption.
2. A candidate preserves applicable producer, source-role,
   formation-occurrence, scope, authority, and provenance coordinates where
   known, and explicit Unknowns where not known. Seed-produced, operator-supplied
   testimony, and external-source testimony are examples, not an exhaustive
   taxonomy.
3. Candidate carriage, transport, comparison, or re-presentation does not
   produce the candidate and cannot fill in a missing formation occurrence.
4. Material may carry a proposed meaning without warranting the meaning
   relation. Attribution says who supplied an assertion, not what the source
   means and not whether that meaning is warranted.
5. Artifact construction, serialization, stable identity, reachability, and
   type compatibility do not confer named standing or prove a producer
   occurrence. A responsible live return can give an observer local occurrence
   evidence, but that evidence is not durable unless represented or recorded.
6. Applicability is consumer- and purpose-local. Availability does not establish
   applicability; applicability does not establish admission; admission does not
   establish consumption. The Book supplies no generic applicability stage.
7. An Unknown finding with constitutional standing requires a responsible,
   bounded production occurrence. Mere field absence can support a narrow
   implementation finding, but neither absence nor an unchecked reference
   authenticates external history.

The Book-warranted postures answer **who may supply** only conditionally: any
source that can lawfully provide attributed testimony with the coordinates
required by the exact later use. It does not name the operator, developer,
decoder, observer, adapter, local competency, other Seed, model, or caller as
the owner for this implementation boundary.

## 2. Recovery A — current executable and constructible roads

### 2.1 Road inventory

| Producer or constructor | Exact caller | Exact input | Exact act | Exact output | Occurrence recorded? | Immediate consumer | Later consumer | Current standing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `_capture_representation` / active common-grammar ingress producer | ordinary operator-ingress runtime | external bytes and selected decoder mechanism | capture bytes, examine representation, record decoded ingress | durable raw, examination, and ingress Events | yes, ledger | state projector | addressable-material former during projection | **active producer**, implementation-witnessed |
| `form_operator_ingress_addressable_material` | `project_operator_ingress_common_grammar_events`, on a complete decoded `ingress_occurred`, with ledger | exact recorded ingress Event plus its recorded raw/examination lineage | verify occurrence and lineage; construct exact material and one full span | `OperatorIngressAddressableMaterial` | no new Event; source occurrences already recorded | projector stores JSON in the attempt view | projection/replay readers of that view; no candidate producer | active runtime constructor and projection formation; not interpretation |
| `OperatorIngressAddressableMaterial.from_json_dict` | state/replay reconstruction through projected data and direct callers | JSON-safe addressable-material fields | reconstruct nested `SourceSpan` and `ExactOperatorMaterial`, then validate | equivalent addressable-material instance | no | caller-held result | no candidate call edge | JSON reconstruction capability; not a new material occurrence |
| `OperatorIngressAddressableMaterial(...)` | its producer, JSON constructor, and tests | exact typed fields | validate intrinsic v1 carrier invariants | instance | no | caller | as above | direct construction; standing limited by provenance |
| `SuppliedInterpretationCandidateTestimony(...)` | tests only | caller-assembled `InterpretationCandidate`, attributed supplier text, provenance, optional formation ref, scope/loss/Unknown/conflict/limits | validate local shape | supplier-input instance | no | test or hypothetical preservation caller | preservation helper if explicitly invoked | **test-only** current witness; constructible only outside tests |
| `preserve_operator_ingress_interpretation_candidates` | tests only; no current non-test call | addressable material, exact tuple of supplied testimonies, supplied set Unknowns/conflicts | validate, copy attribution, derive narrow absence findings, construct identity-bearing set | `OperatorIngressInterpretationCandidateSet` | no ledger/state/cluster write | test/caller-held result | absent | constructible explicit boundary utility; not active production road |
| `AttributedInterpretationCandidateTestimony(...)` inside preservation | preservation helper; JSON reconstruction; tests attempting forgery | supplied fields plus repository-derived `preservation_unknowns` | construct and validate preserved testimony | attributed testimony instance | no | candidate-set constructor or caller | absent | nested carrier construction; no proof of preservation occurrence |
| `OperatorIngressInterpretationCandidateSet(...)` | preservation helper; `from_json_dict`; adversarial tests | addressable material, attributed testimonies, owned declarations, deterministic id and flags | enforce intrinsic v1 invariants | candidate-set instance | no | caller | absent | direct construction; constructible only in non-test repository |
| `OperatorIngressInterpretationCandidateSet.from_json_dict` | tests only in current repository | serialized candidate set | reconstruct nested types and revalidate all intrinsic invariants | equivalent set instance | no | test/caller | absent | JSON reconstruction, not projection reconstruction and not preservation occurrence |
| contextual warrant-set producer | its independent callers/tests, never candidate-set code | `ExactOperatorMaterial` and a separate tuple of bare `InterpretationCandidate`, plus corrections/evidence | produce candidate-local warrant standings | `ContextualInterpretationWarrantSet` | no | contextual selection may consume independently produced sets | later selection paths | separate constructible responsibility; **not a consumer** of candidate set or attributed testimony |

There is no non-test import, call, serializer registration, projector, state field,
CLI path, diagnostic, export, ledger kind, or runtime wiring for the candidate
set. Module import occurs only within the candidate module itself and tests.
Tests exercise behavior but are not producers, consumers, or runtime fixtures.

### 2.2 Required topology 1 — current active ingress road

```text
external bytes
  -> raw-material capture occurrence (ledger Event)
  -> representation examination occurrence (ledger Event)
  -> decoded ingress occurrence (ledger Event; meaning Unknown)
  -> state projector calls addressable-material former
  -> OperatorIngressAddressableMaterial serialized into projected attempt view
  -> quiescent return / the active road stops here

  -X-> no candidate testimony supply
  -X-> no candidate preservation call
  -X-> no interpretation candidate, warrant, selection, or BOGE uptake
```

### 2.3 Required topology 2 — current candidate-preservation road

```text
actual producer of proposed meaning: absent / Unknown
actual non-test supplier:            absent
actual non-test caller:              absent

hypothetical explicit caller
  -> caller constructs SuppliedInterpretationCandidateTestimony
       supplied: candidate fields, supplier attribution/provenance,
                 optional unchecked formation ref, scope/loss/Unknown/conflicts/limits
  -> preserve_operator_ingress_interpretation_candidates(...)
       repository derives only:
         missing formation ref -> FORMATION_UNKNOWN
         no span refs           -> SOURCE_RELATION_UNKNOWN
         empty proposition      -> PROPOSITION_UNKNOWN
         empty testimony tuple  -> NO_CANDIDATES_UNKNOWN
       repository fixes boundary notes and preservation authority limits
  -> AttributedInterpretationCandidateTestimony tuple
  -> OperatorIngressInterpretationCandidateSet
  -> returned to caller

preservation occurrence standing: observer-held only if a real caller observes
                                  the live responsible return; currently absent;
                                  never durably recorded by this artifact
actual consumer:                   absent
```

## 3. Recovery B — candidate supplier responsibility

### 3.1 Supplier and producer matrix

| Candidate source posture | Supplies what? | Produces proposed meaning? | Formation occurrence available? | Authority | Current implementation witness | Standing |
| --- | --- | ---: | ---: | --- | --- | --- |
| operator | attributed candidate testimony, if actually expressed and bounded | possibly, for the operator's proposed assertion; not Seed-native warrant | only if separately evidenced; ordinary ingress is not enough | source-relative testimony only | no candidate-supply edge | Book-warranted posture; current producer **Unknown/absent** |
| external grammar source | source-attributed candidate or rule testimony | possibly, as external meaning assertion | only from preserved source occurrence evidence | bounded external grammar, never repository law by carriage | no adapter/source edge | Book-warranted posture; current witness absent |
| translator | bounded translated claim with source, scope, uncertainty and limits | may produce a translation assertion, not necessarily the upstream candidate | only if translator occurrence is evidenced | translation-local | no translator call | plausible Book composition; ownership Unknown |
| decoder | decoded representation | no: decoding establishes representation availability, not semantic candidate | decoder examination Event exists, candidate formation does not | representation outcome only | active decoder explicitly stops short | constitutionally insufficient supplier for candidate testimony |
| observer | attributed observation/testimony about what it observed | only if separately competent and responsible to propose meaning | requires observation/formation evidence | observation-local | no observer candidate edge | plausible but unassigned; Unknown |
| application declaration | caller/developer declaration of proposed meaning | possibly, as application-source meaning testimony | only if declaration occurrence is preserved | declaration-local; not constitutional ownership | no non-test declaration | plausible external testimony; current absent |
| local competency | Seed-produced candidate with method/evidence | yes, if a responsible candidate producer exists | required and may be local or preserved | candidate-production authority only | no such producer/call | Book permits; current absent/Unknown |
| another Seed | external/source-relative candidate testimony, unless independently warranted otherwise | possibly | only if source Seed occurrence is evidenced | source-relative; no authority transfer | no transport edge | plausible external posture; current absent |
| model or LLM | provider/model output as external testimony | possibly as source assertion, not automatically Seed candidate | only with separate occurrence/provenance | provider-bounded, no constitutional authority by identity | no model boundary | investigative possibility only; neither required nor recommended |
| human developer | developer-supplied candidate/meaning testimony | possibly as attributed developer assertion | only if declaration/formation occurrence is evidenced | bounded developer testimony | Book closed-choice example, but no edge here | plausible, not assigned to this carrier |
| explicit caller | exact fields accepted by `SuppliedInterpretationCandidateTestimony` | **Unknown**; assembling fields does not show who formed meaning | optional unchecked string or absent | whatever limits caller supplies; shape does not authenticate them | tests only | implementation-local input role, not constitutional supplier contract |
| Unknown producer | testimony with unresolved producer dimension | Unknown | Unknown must remain explicit | no invented authority | `attributed_supplier` forbids empty text but cannot express authenticated producer standing | Book-warranted negative posture; current representation is only caller assertion |

The candidate object supplies an identity, label, zero or more span references,
and possibly-empty proposed meaning. The testimony supplies asserted supplier
identity, provenance, optional formation reference, declared scope, known loss,
supplier Unknowns, conflicts, and supplier authority limits. None is verified
against an event, registry, source object, material origin, or formation method.

The exact assertion preserved is: **the named caller-attributed supplier supplies
this candidate-shaped proposed-meaning testimony with these declared
coordinates**. It is not: the supplier identity is verified; candidate formation
occurred; the material means the proposition; the source span caused or supports
the meaning; or the proposition is warranted.

Thus:

```text
supplier of testimony
!= producer of proposed meaning
!= repository preserver
!= contextual warrant examiner
!= selector
```

The same real actor could hold several roles, but the artifact neither proves
that identity nor joins the occurrences. `formation_occurrence_ref` is an
unchecked attributed reference, not evidence loaded or validated by this
boundary. Source attribution is likewise not formation-occurrence evidence.

## 4. Recovery C — applicability of preservation

### 4.1 Tested conditions

| Proposed condition | What it establishes | Does it make preservation applicable? |
| --- | --- | --- |
| supplier actually supplied testimony | candidate testimony is available, if the supply occurrence is evidenced | necessary for preserving nonempty testimony, but not sufficient without a responsible preservation purpose/consumer or independently warranted remembering decision |
| current consumer requests testimony | a consumer-local need may exist | potentially sufficient only with exact input/standing requirements and lawful supplier evidence; no such current consumer exists |
| interpretation responsibility applicable | an interpretation consumer has local applicability | may motivate candidate use, but does not automatically require this preservation artifact |
| material semantically unresolved | meaning remains Unknown | does not imply candidates exist or that preservation is required |
| material addressable | exact material and one coordinate are available | insufficient; availability != testimony != applicability |
| candidate objects available | carrier values exist | insufficient without attribution, standing, purpose, and boundary responsibility |
| caller invokes constructor | code executed | implementation precondition/occurrence evidence at most; not constitutional applicability evidence |
| application elects to preserve | an application policy assertion | potentially relevant, but no policy, owner, occurrence, or consumer is present |
| replay consumer requires reconstruction | durable preservation requirement | could make recording/schema work applicable, but no such consumer or current projection exists |

The current helper accepts no applicability finding, consumer, purpose,
preservation horizon, or decision evidence. It validates material and supplied
shape, then preserves whenever invoked, including an empty tuple. Therefore it
**does not examine or consume applicability**. Invocation is implementation
crossing and may evidence that somebody called it; invocation alone is not an
answer to why that act was responsible.

No separate universal applicability examiner is constitutionally required for
this bounded act. A responsible explicit caller could own a local remembering or
transport purpose and call a preservation helper without materializing an
applicability artifact. What is missing here is evidence that any such caller,
purpose, or consumer exists—not a mandate to create an examiner.

## 5. Recovery D — exact candidate source relation

The addressable-material v1 invariant creates exactly one `SourceSpan` whose
`source_ref` is the decoded ingress Event, offsets are `0..len(exact_text)`, and
text equals the entire decoded material. Candidate validation accepts zero or
more references and proves only that every supplied reference identity belongs
to that one-span universe. Foreign references are refused.

For a nonempty candidate reference, the implementation establishes:

```text
candidate testimony carries a reference to the identity of a SourceSpan
belonging to the exact OperatorIngressAddressableMaterial
```

It does **not** establish:

* that the proposed meaning is about that span;
* that the candidate was formed from it;
* that the span evidentially supports the meaning;
* that the proposed meaning semantically covers all material;
* that it concerns only part of the material; or
* a warranted meaning relation.

Because the only admissible v1 span happens to cover all material, the carrier
reference is a reference to the full-material coordinate. This is not semantic
coverage. An externally supplied reference can be preserved faithfully at that
coarse coordinate; the coordinate is insufficient evidence of formation and is
not by itself sufficient for later contextual warrant examination. The warrant
producer can mechanically resolve matching span refs, but it independently
requires candidates and evidence and does not consume this set.

The full span is both an addressable-material intrinsic v1 invariant and the
only presently available coordinate. The Book requires bounded addressability
and relation dimensions where applicable, not one universal full-material
candidate grammar. Whether it is sufficient for a particular candidate kind or
consumer is **Unknown**. No active consumer requires localized spans, so no
subdivision API is warranted now.

### Required topology 4 — source relation

```text
decoded OperatorIngressAddressableMaterial
  -> one canonical full-material SourceSpan
       identity/offset/text relation: implementation-witnessed

InterpretationCandidate
  -> source_span_refs contains that span identity (or none)
       membership/reference relation: implementation-witnessed
  -> proposed_meaning
       meaning about span/material: Unknown, only supplier-attributed text
  -> formation_occurrence_ref
       unchecked supplied reference or absent; occurrence truth: Unknown

preservation helper live return
  -> possible observer-held preservation occurrence if actually called
       current occurrence: absent; durable occurrence: absent

contextual warrant
  -> separate producer with separate bare inputs/evidence
       edge from candidate set: absent
```

## 6. Recovery E — formation and preservation occurrences

| Statement | What current repository can truthfully establish |
| --- | --- |
| candidate formation occurred | not established by this boundary |
| supplier claims formation occurred | only weakly suggested when caller supplies a non-null reference; the artifact does not name the reference semantics beyond its field name or validate it |
| formation occurrence reference absent | exact field fact, intrinsic and deterministically inspectable |
| preservation derives formation Unknown | implementation derives `FORMATION_UNKNOWN` from that absence; honest shorthand for “formation occurrence is not represented here,” not proof no occurrence happened |
| candidate set was constructed | an in-memory result proves construction to a live observer; a JSON object proves only represented fields until reconstruction/validation |
| preservation act occurred | a live call observed returning can provide local observer-held occurrence evidence; no current non-test call exists |
| preservation artifact exists | possible transiently in tests/hypothetical callers; no durable current artifact found |
| preservation act durably recorded | false: flags prohibit ledger/state/cluster mutation and no occurrence ref is carried |
| artifact reconstructed from JSON | focused tests establish capability and equivalence; reconstruction is a new mechanical construction, not original preservation occurrence |

`AttributedInterpretationCandidateTestimony` construction proves only nested
carrier construction and invariant satisfaction. Candidate-set construction
proves only set construction. Neither authenticates a responsibility-bearing
preservation occurrence, because direct and JSON constructors can create the
same shape without the helper. The deterministic id seals content, not time,
caller, authority, or occurrence.

No observer currently holds a non-test preservation return; no Event, projection,
or artifact coordinate preserves such standing. Replay or a later consumer that
requires original preservation standing would need a recoverable responsible
producer/caller, occurrence identity or other sufficient occurrence evidence,
scope/purpose, inputs and provenance, authority/limits, result binding, and
conflicts/Unknowns. A consumer that needs only content-coherent attributed
testimony might accept reconstructed fields under its own local checks, but that
would not prove the original preservation act or candidate formation.

## 7. Recovery F — repository-owned preservation findings

| Coordinate | Classification | Exact subject/evidence/scope | Authority and risk |
| --- | --- | --- | --- |
| `preservation_unknowns` tuple shape/order | intrinsic invariant + implementation convention | one attributed testimony; three current fields | repository may enforce its own deterministic summary; no external truth authority |
| `FORMATION_UNKNOWN` | deterministic consequence + repository-derived finding; not yet constitutional Typed Unknown occurrence | `formation_occurrence_ref is None` in this testimony | truthful only as “no formation occurrence reference is preserved”; risks self-authentication if read as responsibly examined real-world formation Unknown |
| `SOURCE_RELATION_UNKNOWN` | deterministic consequence + repository-derived finding | empty `source_span_refs` | truthful as absent represented reference; does not establish no source relation exists |
| `PROPOSITION_UNKNOWN` | deterministic consequence + repository-derived finding | empty `proposed_meaning` | truthful as unavailable proposition in carrier; does not establish supplier had no proposition |
| `preservation_set_unknowns` tuple shape/content | intrinsic invariant + deterministic set-level convention | supplied tuple empty/nonempty | repository-owned summary, not external absence finding |
| `NO_CANDIDATES_UNKNOWN` | deterministic consequence + repository-derived finding | zero testimonies supplied to this call | truthful as “none presently supplied to this invocation”; cannot establish no candidates exist elsewhere |
| `preservation_authority_limits` | intrinsic invariant + negative authority declaration | repository's own preservation act and returned carrier | responsibly states what helper does not establish; safe if not mistaken for proof helper occurred |
| `boundary_notes` | intrinsic invariant + negative authority/implementation convention, mixed | repository's intended v1 semantics | first two notes accurately limit preservation; “external or caller-supplied” is broader than evidenced current producer and must remain a boundary declaration, not supplier proof |
| `supplied_unknowns`, `supplied_set_unknowns` | attributed testimony | caller fields | repository checks shape only and must not own their truth |
| `known_loss`, `conflicts`, `supplied_authority_limits` | attributed testimony | caller fields | not repository findings; duplication/order deliberately preserved |
| unique candidate refs | intrinsic set invariant | candidate fields in returned set | deterministic identity coherence only |
| referenced span belongs to material | intrinsic membership invariant | candidate refs and material's span identities | proves reference membership, not semantic/source/formation relation |
| stable `candidate_set_id` | intrinsic content-identity invariant | all identity payload fields | detects forged/stale content; no occurrence seal |
| read-only/non-mutating flags | intrinsic side-effect declaration | artifact/helper contract | negative operational authority, not evidence of constitutional inactivity or occurrence |

The implications under special test are therefore:

```text
formation_occurrence_ref is None
  -> no formation occurrence reference is represented in this testimony
  -> repository emits its bounded implementation finding FORMATION_UNKNOWN
  -X-> candidate formation did not occur
  -X-> a constitutional Unknown examiner occurrence has been durably preserved

zero supplied candidates
  -> no candidate testimony was supplied to this exact invocation
  -> repository emits NO_CANDIDATES_UNKNOWN
  -X-> no candidate exists
  -X-> no source could supply one later or elsewhere
```

The repository is the producer of these deterministic preservation summaries,
using only artifact/call fields. It has authority to describe its own evidence
boundary. Their honest subject must stay field availability within this
preservation set. They risk becoming unsupported, self-authenticating assertions
when labels are read as external examination results, formation history, or
global absence. The artifact has no producer/occurrence coordinates for a
standing-bearing Unknown finding beyond content and convention.

## 8. Recovery G — active and possible consumers

### 8.1 Consumer matrix

| Candidate consumer | Exact required input | Current call edge | Applicability evidence | Required occurrence standing | Result |
| --- | --- | --- | --- | --- | --- |
| contextual interpretation warrant production | bare `ExactOperatorMaterial`, tuple of bare `InterpretationCandidate`, corrections, retrospective/clarification evidence, maps, optional binding ref | none from candidate set | none | its own producer invocation; it neither requires nor validates candidate formation occurrence | compatible nested carriers only; **not uptake** |
| contextual interpretation selection | `ContextualInterpretationWarrantSet` plus explicit candidate-bound selection evidence | none | warrant-set-local evidence | warrant and selection producer returns | no candidate-set input |
| interpretation applicability | an exact warranted meaning relation and consumer/purpose on the Book road | none | absent | consumer-local applicability occurrence if required | no current candidate-set consumer |
| bounded question formation | family-specific goal/frontier inputs | none | absent | local question producer | no import or coordinate use |
| BOGE | admitted warranted relation/proposition on applicable roads, not unresolved raw material | none | separate BOGE-local evidence required | admission/establishment standing | explicitly not current consumer |
| Demand | established applicable insufficiency/requirement under Demand grammar | none | absent | Demand establishment occurrence | not a candidate carrier consumer |
| projection | ingress Event and ledger for addressable material only | none | active only for addressable material | source Events already durable | candidate set not projected |
| diagnostic rendering | registered diagnostic inputs | none | absent | diagnostic-local | no CLI/import/registry entry |
| serialization/replay | JSON supplied directly to classmethod in tests | tests only | none | content coherence only unless original occurrence separately preserved | capability, not active replay consumer |
| external export | an explicit export surface/contract | none | absent | purpose-local emission/transport evidence | absent |

The contextual warrant producer accepts structurally related nested types, but
it does not accept `OperatorIngressInterpretationCandidateSet`, attributed
testimony, preservation findings, supplier identity, formation reference, or
preservation limits. Passing extracted candidate/material fields would be a new
caller-owned adaptation and would discard coordinates unless separately
warranted. No current code performs it.

The artifact is simultaneously:

* a **constructible capability** (implementation-witnessed);
* an **explicit boundary utility** (it cleanly separates supplier and
  repository-owned fields when called);
* a **future-compatible carrier** only in the weak sense that a future consumer
  could examine it—no compatibility or need is established; and
* a **disconnected scaffold** in current topology because it has no producer
  call edge, durable occurrence, or consumer.

It is **not yet an independently warranted preservation artifact** for current
operator ingress. The Book warrants the possibility and discipline of preserving
attributed candidate testimony, but no current applicable preservation purpose,
supplier occurrence, horizon, or consumer makes production of this exact set a
responsibility. “Capability” and “scaffold” are not mutually exclusive here.

## 9. Recovery H — carrier ownership

`SourceSpan`, `ExactOperatorMaterial`, and `InterpretationCandidate` are defined
in `contextual_interpretation_warrant_set.py`. Addressable material imports the
first two; candidate preservation imports the third; contextual selection also
imports `ExactOperatorMaterial`. The warrant producer itself consumes all three.

This establishes implementation reuse and historical/module placement. It does
not establish constitutional ownership. The carriers are useful across earlier
addressability/preservation and later warrant responsibilities, but the Book
does not independently name these dataclasses as universal shared constitutional
subjects. Their current standing is best classified as **implementation-local
types reused by multiple responsibilities; constitutional ownership Unknown**.

There is a backward import dependency on a downstream-named module and some
warrant vocabulary can be inferred from location. Yet no cycle, runtime defect,
standing mutation, schema confusion, failed validation, or consumer crossing was
found. The ingress modules use only the carrier shapes/error, and do not invoke
warrant production. Thus placement is historically awkward but presently
harmless. Module location alone neither grants contextual-warrant ownership nor
warrants a move.

### Ownership matrix

| Coordinate | Supplier-owned | Material-owner-owned | Preservation-owner-owned | Consumer-owned | Current enforcement | Current standing |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| exact decoded material/provenance | no | yes | no | no | recorded ingress lineage and addressable invariants | active, implementation-witnessed addressability |
| canonical full span identity/offset/text | no | yes | no | no | exact single-span invariant | material-owner v1 coordinate, not universal candidate grammar |
| candidate id/label/proposed meaning | attributed input | no | copy only | no | type/string and uniqueness checks | caller-attributed, producer Unknown |
| candidate span references | attributed input | owns available span universe, not assertion | validates membership | later consumer owns sufficiency judgment | foreign refs refused | reference membership only |
| attributed supplier/provenance | supplier/caller assertion | no | copy/shape validation | must decide reliance | nonempty strings/tuples only | attributed testimony; unauthenticated |
| formation occurrence | candidate producer | no | preserves reference/derives absence finding | decides required standing | optional string only | occurrence Unknown |
| declared scope/loss/supplied Unknowns/conflicts/limits | attributed supplier | no | lossless copy | decides applicability/admission | exact tuple shapes | attributed testimony only |
| preservation Unknowns | no | no | yes | decides whether sufficient | exact deterministic derivation | repository-derived field-absence findings |
| set-level supplied Unknowns/conflicts | supplier/caller | no | copy | decides reliance | exact tuple | attributed input |
| no-testimony finding | no | no | yes | decides significance | empty tuple equivalence | invocation-local repository finding |
| boundary notes/authority limits | no | no | yes | preserves if consumed | fixed exact tuples | negative authority and convention |
| applicability | no universal owner | no | no | yes, for exact use; or caller-local preservation decision | absent | Unknown |
| warranty/selection/BOGE standing | no | no | expressly denied | respective later producers/consumers | no edge | absent from this artifact |
| preservation occurrence | no | no | helper/live observer if called | may require durable proof | not represented or recorded | absent currently |

## 10. Required topology 3 — possible lawful road

Only Book-warranted relations are shown; unassigned owners remain Unknown.

```text
exact addressable external/operator-origin material
  + attributed candidate testimony
      producer/source role: known or explicit Unknown
      proposed meaning: source assertion, not warranted relation
      formation occurrence: evidenced or explicit Unknown
      provenance/scope/authority/loss/conflicts/Unknowns
  + an exact responsible preservation purpose or consumer requirement
      owner/applicability: Unknown in the current repository
  -> responsible bounded preservation occurrence (if applicable)
      faithfully retains attribution and limits
      does not generate, warrant, rank, select, admit, or act
  -> reachable preserved testimony
  -> optional later consumer-local applicability/admission/use
      only under that consumer's exact standing and purpose requirements
  -> possible separate candidate-local warrant examination

No arrow above requires one universal artifact, Event, adapter, generator,
registry, projector, module, or order.
```

## 11. Fidelity result

### Faithful within its constructible seam

The helper preserves supplied coordinates without claiming to generate meaning;
separates supplied and repository-derived Unknowns; fixes negative authority;
refuses foreign span identities and duplicate candidate refs; keeps zero, one,
and many candidates distinct from selection; validates deterministic identity;
and remains read-only/non-mutating. It also remains disconnected from warrant
production. These are faithful implementation witnesses within the called seam.

### Crossings and Unknowns

1. **Supplier standing is compressed.** `attributed_supplier` is mandatory text,
   but no source kind, responsible producer occurrence, authentication, or
   constitutional supplier contract is established.
2. **Formation standing is compressed.** A non-null ref is unchecked; a null ref
   yields a label whose safe meaning is only absent represented occurrence
   evidence.
3. **Source relation is weaker than its name can suggest.** Membership in the
   material's span universe is proven; semantic aboutness, derivation, support,
   and coverage are not.
4. **Preservation standing is absent.** Direct construction and JSON
   reconstruction are observationally indistinguishable from helper output by
   fields; no durable occurrence coordinate exists.
5. **Applicability and consumption are absent.** Exact construction validates
   shape, not responsibility. No active consumer requires these fields.

These are not all constitutional conflicts requiring repair. They are bounded
Unknowns or implementation crossings that become defects only if a responsible
consumer requires stronger standing than the carrier provides. The current
absence of a consumer prevents an honest production design.

## 12. Direct answers

1. **Is candidate preservation part of the current active ingress road?** No.
   Active production stops after addressable-material projection.
2. **What current non-test caller invokes it?** None.
3. **What current non-test producer supplies `SuppliedInterpretationCandidateTestimony`?**
   None.
4. **Is that supplier constitutionally identified?** No. The input type names a
   caller assertion; no supplier contract or occurrence is recovered.
5. **Who produces the proposed meaning?** Unknown. The caller supplies its text,
   but field assembly does not identify the responsible meaning producer.
6. **Is candidate formation distinct from testimony supply?** Yes. A supplier may
   report a candidate formed by itself or another producer; carriage is not
   formation.
7. **What evidence establishes candidate formation occurrence?** None here. A
   supplied non-null string is an unchecked attributed reference, not validated
   occurrence evidence.
8. **What does `formation_occurrence_ref=None` establish?** Only that this
   testimony preserves no formation-occurrence reference; not that formation did
   not occur.
9. **Who responsibly produces `FORMATION_UNKNOWN`?** Mechanically, the
   preservation helper/repository derives it. Constitutionally, no separately
   evidenced Unknown-examination occurrence is preserved.
10. **Is that Unknown derivable solely from current fields?** Yes, as the bounded
    field-absence finding; no, if read as a real-world formation-history finding.
11. **What makes candidate preservation applicable?** An exact responsible
    preservation/remembering purpose or consumer requirement applied to actually
    supplied testimony with sufficient standing. None is current; applicability
    is Unknown.
12. **Does the implementation examine applicability?** No.
13. **Is invocation itself sufficient applicability evidence?** No.
14. **Is addressable material sufficient to require candidate preservation?** No.
15. **Does zero candidate testimony establish that no candidates exist?** No; it
    establishes only none supplied to that invocation.
16. **Does one candidate establish uniqueness of interpretation?** No.
17. **What exact relation does a candidate source-span reference establish?** The
    supplied candidate carries an identity reference to a span belonging to the
    exact addressable material.
18. **Does the canonical full span establish that the candidate concerns the
    complete material?** No. The referenced coordinate covers the material; the
    candidate's semantic coverage remains Unknown.
19. **Does it establish that the proposed meaning was formed from that material?**
    No.
20. **Is a localized source relation required now?** No active consumer proves
    that requirement; future sufficiency is Unknown.
21. **What active consumer requires the candidate set?** None.
22. **Does contextual warrant production currently consume it?** No; it accepts
    separate bare material/candidates/evidence.
23. **Does projection currently preserve it?** No.
24. **Is there a preserved occurrence of candidate-set formation?** No.
25. **Is artifact construction enough to establish such an occurrence?** No.
    A live observer may know construction returned, but the artifact does not
    durably carry responsible occurrence standing.
26. **What replay or later-consumer standing would be required?** Whatever the
    exact consumer declares: at minimum content identity/provenance and limits;
    if relying on formation or preservation occurrence, independently recoverable
    responsible producer, occurrence binding, scope/purpose, authority, inputs,
    conflicts, and Unknowns.
27. **Which repository-owned findings are intrinsic invariants?** Exact tuple/type
    shapes, fixed convention/type/notes/limits, read-only flags, unique refs,
    span-membership validation, deterministic identity, and exact equivalence of
    derived findings to their triggering fields.
28. **Which are responsible preservation findings?** At implementation scope,
    absent represented formation ref, absent represented source refs, empty
    represented proposition, and zero testimony supplied to this call, plus the
    helper's own negative authority. They do not have durable occurrence standing.
29. **Which risk becoming self-authenticating assertions?** All four uppercase
    Unknown labels if interpreted beyond field availability; a supplied
    `formation_occurrence_ref`; supplier identity/provenance; semantic source
    relation; and boundary-note source claims if treated as verified facts.
30. **Are `ExactOperatorMaterial`, `SourceSpan`, and `InterpretationCandidate`
    independently owned shared carriers?** Not constitutionally established.
    They are implementation-local reused types; ownership remains Unknown.
31. **Does their current module placement create a concrete defect?** No concrete
    standing, cycle, dependency, or runtime defect was found.
32. **Is the candidate-set artifact an independently warranted capability or a
    disconnected scaffold?** It is a constructible explicit boundary capability
    and a disconnected scaffold. Independent current production warrant is
    Unknown/absent.
33. **What is the earliest missing relation?** A current, responsible consumer or
    preservation-purpose owner establishing why attributed testimony for this
    exact material must be retained and what standing it requires.
34. **What is the smallest next responsibility?** Recover that one owner-to-use
    relation: exact consumer/purpose, applicability condition, required testimony
    and source/occurrence standing, preservation horizon, and lawful stopping
    point.
35. **Is production work sufficiently specified?** No.
36. **Should the next step preserve, repair, delete, relocate, wire, or perform
    another bounded recovery?** Perform another bounded recovery of the earliest
    missing consumer/purpose relation. Do not choose an implementation shape in
    advance. Preserve, repair, delete, relocate, or wire only if that recovery
    supplies exact responsibility and necessity.

## 13. Final recommendation — one honest next inch

Perform one bounded, evidence-first recovery asking whether any current
responsibility actually needs attributed interpretation-candidate testimony for
one exact addressable operator-ingress material. Name that exact consumer and
purpose if found; recover its minimum accepted testimony, provenance,
source-relation, formation/preservation occurrence, authority, Unknown/conflict,
and temporal/preservation-horizon requirements; and otherwise record a negative
result. This recommendation chooses no generator, supplier class, adapter,
applicability engine, Event, registry, span API, module move, projection, or
warrant wiring. That is the smallest honest next inch because applicability and
consumer necessity precede any responsible decision to preserve, repair,
delete, relocate, or wire the constructible carrier.
