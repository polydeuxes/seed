# Candidate-versus-relation-grammar bounded orientation 001

## 1. Executive disposition

The phrase

```text
candidate-versus-relation-grammar Compare
```

does not currently name an exact constitutional shape recovered within the
inspected repository boundary. It compresses several adjacent but non-identical
subjects: caller-supplied candidate testimony, the active dimensions of a
bounded relation Claim or Standing, source-attributed relation proposals,
bounded testimony comparison, closed-choice response-coordinate Compare, and
Fidelity comparison. Current higher-authority evidence does not compose those
subjects into one candidate-versus-relation-grammar Responsibility.

The executive disposition is therefore:

```text
exact phrase: not recovered within the inspected repository boundary
constitutional shape required to own the proposed Compare: Unknown
adjacent constitutional shapes: partially recovered and non-composable
```

The controlling proof is not lexical. Active law does not use `relation
grammar` or `relation-grammar`. It governs relation Claims and relation Standing
through applicable constitutional dimensions, and it independently governs
external grammar, candidate attribution, bounded testimony comparison,
closed-choice response-coordinate comparison, and Fidelity production. Runtime
contains no exact named relation-grammar holder within the inspected boundary.
The runtime carrier named `CandidateExternalGrammarSet` preserves caller input;
its name and construction do not establish constitutional grammar Standing,
Applicability, Admission, comparison participation, or a comparison occurrence.

Because the proposed Compare Responsibility remains Unknown, no responsible
Compare Act and no occurrence of that proposed Act are recovered. Ordinary
value checks, structural validation, projector reconstruction, and other
comparison families do not fill that constitutional gap.

## 2. Authority order and excluded testimony

This orientation applied the required order:

1. current active internal Book grammar;
2. current runtime structures and tests;
3. repository history and established Responsibilities before the excluded
   chain;
4. reports only as attributed testimony.

The active internal Book boundary was identified through
`book_of_seed/README.md`, which says the Book preserves constitutional grammar,
implementation and tests are evidence of current practice rather than automatic
Authority, historical reports are locators and testimony, and `[UNRESOLVED]`
marks questions without safe constitutional resolution.

### Excluded reverted history

The inspected history begins at current `HEAD`, commit `28d75fb`, whose parent
sequence shows PRs 2311--2314 followed by their reversion in PR 2315. The
following reverted commits and every conclusion, correction, and vocabulary
choice introduced by them were deliberately excluded:

```text
1f1b2b8  PR 2311
e9ee481  PR 2312
f4ea119  PR 2313
05e9f8f  PR 2314
```

Their removed report path remains visible in history only as a visibility fact.
The removed contents were not read as evidence, were not used as candidate
testimony, and were not used to interpret runtime. Current state after reversion
is the investigation baseline.

### History boundary inspected

History inspection covered current `HEAD` through the pre-chain implementation
and report lineage visible from PRs 2310 back through PR 2236, with focused
inspection of current files whose earlier commits concern candidate comparison,
response-coordinate comparison, operator meaning relations, Prometheus
translation, and Fidelity. A historical commit title or report does not
establish a coordinate; it served only as a locator unless current higher
Authority independently corroborated the substantive claim.

## 3. Independently verified repository facts

### 3.1 Active-law vocabulary and relation clauses

An exact case-insensitive search of active numbered Book chapters found no use
of `relation grammar` or `relation-grammar`. That bounded search establishes
only that no exact phrase was found in those active-law files.

Active law instead says:

- A relation is its own bounded Claim subject. A relation Claim or Standing
  preserves each applicable constitutional dimension, or explicit Unknown or
  unresolved standing: participants and roles, relation assertion, Evidence
  standing, Scope, Producer, Consumer and purpose, Authority, occurrence,
  conflicts, and limits
  (`01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`,
  `01.Standing.E`).
- Candidate relation, relation testimony, and evidence-supported or established
  relation Standing remain distinct (`01.Standing.E`).
- Meaning is one bounded relation form. Meaning assertion carriage, relation
  Warrant, consumer-local Applicability, Admission, and later establishment are
  distinct (`01.Standing.E` and `08.Communication`).
- Source translation may form an attributed, Seed-addressable relation proposal
  while preserving source boundary, context, Scope, uncertainty, Authority
  limits, provenance, known loss, and conflicts. Translation does not establish
  Applicability, Admission, comparison, interpretation, meaning-relation
  Warrant, truth, or adopted law (`01.External.A`).
- External material may propose meaning; carriage is not a Seed-native
  meaning-relation Warrant (`01.External.G`).
- A bounded testimony comparison may consume multiple independently preserved
  testimonies or findings and may produce bounded relation Standing while
  preserving every input's source-local limits (`05.Testimony.E`).
- A closed-choice response comparison consumes captured response material and
  an exact Presentation's response coordinates. It establishes exact match or
  no exact coordinate match; Comparison and Identification remain distinct
  (`08.Communication`, paragraphs 20--22).
- Fidelity production compares constitutional grammar, a bounded expectation,
  and an implementation witness under a declared seam or Scope and may produce
  qualitative standing within that Scope (`01.External.D`).

Active law describes these materials as constitutional **dimensions**,
**constraints** where independently applicable, **Warrant**, **Applicability**,
**Admission**, source or constitutional **grammar**, and bounded
**representations** according to the exact clause. It does not rename the
relation dimensions collectively as one grammar representation. It also does
not establish one per-relation-kind Compare family.

### 3.2 Current runtime inventory

Searches by exact names and by relation-shaped fields found:

- `CandidateExternalGrammarInputCandidate`, `CandidateExternalGrammarInput`,
  `CandidateExternalGrammarSet`, and
  `assemble_candidate_external_grammar_set(...)` in
  `seed_runtime/candidate_external_grammar.py`;
- recorded operator meaning-relation events and their session projection in
  `seed_runtime/operator_source_recovery.py` and
  `seed_runtime/operator_session_standing.py`;
- the closed-choice response comparison in
  `seed_runtime/operator_response_comparison.py`;
- ordinary diagnostic snapshot comparison and ordinary Python comparison
  syntax inspection in unrelated runtime modules;
- Prometheus acquisition, decoded samples, provider-local observation shapes,
  and Observation formation in `seed_runtime/observation_sources.py`.

No exact named symbol for `RelationGrammarRepresentation`, a relation-grammar
holder, or an applicable-grammar projection was found within current
`seed_runtime` and `tests`. Search by relation shape found no runtime structure
that independently carries all of participants and roles, relation assertion,
Evidence standing, Warrant, Scope, Producer, Consumer and purpose, Authority,
occurrence, conflicts, known loss, Unknowns, and limits **as a proposed compared
grammar representation**. Differently named partial structures are treated
separately below.

No current runtime path from `CandidateExternalGrammarSet` to
`operator_response_comparison`, the operator meaning-relation path, Prometheus,
or Fidelity was found. Its runtime consumers within the inspected boundary are
its JSON formatter, human formatter, a CLI branch, diagnostic shape-audit
metadata, and tests.

### 3.3 Exact `CandidateExternalGrammarSet` facts

`CandidateExternalGrammarSet` is a frozen runtime dataclass containing:

```text
representation_scope
candidates
set_unknowns
boundary_notes
read_only=true
writes_event_ledger=false
mutates_cluster=false
```

Each supplied candidate contains a caller-provided identifier, structural
Claim text, optional Claim Scope, provenance strings, supporting-testimony
strings, contradicting-testimony strings, unresolved alternatives, and explicit
Unknown strings. The module's fixed notes say candidate grammars are
caller-supplied structural hypotheses; testimony relations are preserved rather
than evaluated; no candidate is selected, verified, promoted, or treated as
semantic truth; and the artifact establishes neither translator readiness nor
capability.

`assemble_candidate_external_grammar_set(...)` checks nonempty and unique
candidate identifiers, then copies the supplied Scope, candidates, and set
Unknowns into the frozen carrier with fixed boundary notes. That implementation
establishes the function as the constructor of this runtime carrier. The
repository does not thereby establish it as the constitutional Producer of the
candidate Claims, their provenance, their testimony relations, a grammar, or a
comparison input. Recorded identity is not participant role; constructor
activity is not the source formation occurrence asserted by caller testimony.

The representation carries only caller-attributed structural testimony and the
module's negative boundary assertions. Its provenance fields are opaque strings
supplied by the caller; the constructor does not establish their Evidence
standing. It creates no event-ledger record and no Seed-native Fact, relation,
grammar, Applicability, Admission, or comparison Standing. The representation's
independently evidenced standing is a read-only, non-cluster-mutating runtime
carrier of validated input shape, renderable through the CLI and formatters.

Tests prove exact copying, rendering, duplicate refusal, zero-candidate
rendering, and the fixed no-selection/no-verification boundary. They do not use
the carrier as a compared representation. No recorded occurrence determines
its Applicability to the proposed Compare, admits it, or performs that Compare.

### 3.4 Meaning-relation path

The meaning-relation path performs distinct operations:

1. validate the recorded Presentation, comparison, identification, capture, and
   ingress chain;
2. recover represented-source identity from the identified alternative and
   recorded Presentation lineage;
3. consume attributed developer-supplied meaning testimony and record a bounded
   meaning-relation result;
4. reconstruct and structurally check those recorded coordinates in the session
   projector.

This path relies on a prior closed-choice response-coordinate comparison. It
does not compare a candidate with a relation grammar. Its equality and
consistency checks are producer-invariant validation and projector
reconstruction. The source module expressly separates represented-source
identity from source meaning and says the meaning relation derives nothing from
response text, recurrence, or lexical similarity. Current tests exercise event
formation, exact lineage, refusal of forged coordinates, deterministic
projection, and the bounded meaning relation. Those tests do not supply a
relation-grammar representation.

### 3.5 Collection and projection questions

Current runtime does project a dictionary of meaning relations and a latest
meaning relation within one operator session. It also exposes an empty
`recorded_relation_standings` list in the operator-ingress view projection. These
are adjacent relation-shaped projections, not a general collection of
established relation Standings and not an applicable-grammar projection. Their
event-local subject and projection invariants do not establish generic
relation-grammar Standing.

No Consumer-local comparison basis for the proposed family was recovered. The
closed-choice response-coordinate set is a Consumer-local basis for its own
exact response comparison only and must not be transferred by analogy.

## 4. Attributed-claim disposition table

No external-Book passage was needed. The following report claims were used only
as attributed testimony and were dispositioned against current higher
Authority. The excluded PR 2311--2314 chain is intentionally omitted from
candidate testimony.

| Claim | Source | Exact wording or bounded paraphrase | Current repository corroboration | Current internal-grammar corroboration | Contradiction | Unresolved coordinates | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PESC asks which applicable relation grammar can examine a bounded candidate equivalence. | `book_of_seed/grammar_bounded_orientation_observation_001.md` | The report repeatedly describes an “applicable relation grammar” examining a candidate and says none may presently be recovered. | No runtime representation or occurrence independently supplies that grammar or comparison. | Active law supplies relation dimensions and several exact comparison boundaries, but does not use the phrase or assign this Responsibility. | Treating the prose label as active grammar would conflict with the Book's artifact-standing and lexical-presentation limits. | Owner, Authority, inputs, Applicability, Admission, occurrence, result, Standing, Consumer. | attributed candidate only |
| Candidate-versus-grammar has an exact Compare Act rendering. | `book_of_seed/candidate_versus_grammar_comparison_recovery_001.md` | The report calls “Compare the candidate equivalence with the applicable relation grammar” the exact responsible act while leaving its owner unresolved. | No proposed-family runtime occurrence was found. | The Responsibility root requires an exact owning Responsibility; active law does not assign one here. | Under the controlling proof discipline, unresolved owner means the proposed Act and occurrence are not recovered. | Exact Responsibility and every dependent occurrence/result coordinate. | contradicted |
| The proposed family is distinct from testimony comparison. | `book_of_seed/candidate_versus_grammar_comparison_recovery_001.md` | It distinguishes multiple testimonies/findings from one candidate-equivalence proposal. | Runtime response comparison and candidate carrier have different exact subjects and no connecting path. | `05.Testimony.E` is expressly limited to multiple preserved testimonies/findings; active relation and candidate clauses do not compose the proposed family. | None for the bounded non-identity; it does not positively establish the proposed family. | Proposed family's own Responsibility and coordinates. | corroborated |
| The proposed owner remained unresolved in pre-chain orientation reports. | `book_of_seed/shape_b_compare_owner_and_continuation_recovery_001.md` and `book_of_seed/compare_occurrence_implementation_form_recovery_001.md` | Both reports say the candidate-versus-relation-grammar owner was unresolved and no construction followed. | No current owner symbol, runtime path, or occurrence was found. | Active Responsibility grammar requires the owner and forbids inference from adjacency; no active clause assigns it. | None. “Unresolved” remains report testimony; the constitutional coordinate is reported here as Unknown because the exact required shape cannot be recovered. | Authority, Evidence, Applicability, Admission, result, Standing, Consumer. | corroborated |
| Prometheus has provider-local Translation-shaped implementation boundaries. | `book_of_seed/prometheus_translation_ownership_recovery_001.md` | Bounded paraphrase: decoded sample and provider-local observation shape separate provider JSON from Observation formation. | `PrometheusDecodedSample`, `PrometheusObservationShape`, mapping functions, and tests independently witness those separations. | `01.External.A` and `05.Testimony` distinguish provider material, translated/addressable material, acquisition and interpretation, and Observation testimony. | The implementation names do not prove every constitutional coordinate or a relation to the proposed Compare. | Exact per-path Authority, Evidence standing, Consumer, production occurrence, and any Fidelity result. | partially corroborated |
| Fidelity is bounded constitutional grammar versus expectation versus implementation witness. | `book_of_seed/fidelity_production_ownership_correction_001.md` | Bounded paraphrase: Book I owns general Fidelity production through bounded constitutional comparison. | Runtime-wide Fidelity occurrence was not needed or found for this proposed family. | `01.External.D` directly establishes the subject, required preservation, bounded qualitative results, Scope, and negative Authority. | No contradiction at the general active-law boundary. It does not supply candidate-versus-grammar inputs. | Particular seam, witnesses, occurrence, result, and Consumer for any instantiated Fidelity case. | corroborated |

Repeated report language was not counted as independent corroboration.

## 5. Decompression of the proposed phrase

The words in the compressed phrase do not correspond one-to-one with recovered
constitutional coordinates.

| Coordinate investigated | Finding | Exact bounded basis |
| --- | --- | --- |
| relation Claim subject | recovered | `01.Standing.E` establishes a relation as its own bounded Claim subject. |
| representation carrying a relation assertion | partially recovered | Candidate entries may carry structural Claim text; operator Presentation material carries attributed meaning assertions. Neither is the proposed grammar representation. |
| relation Standing | recovered | `01.Standing.E` defines bounded relation Standing; `05.Testimony.E` may produce bounded relation Standing; exact instances retain local standing. |
| grammar applicable to a relation Claim | not recovered | No exact active clause, runtime representation, or determination occurrence connects a grammar to a relation Claim under this phrase. |
| constraints governing a relation Claim | partially recovered | Active constraint and relation law may govern exact Claims; no proposed-family constraint package is represented. |
| dimensions applicable to a relation Claim | recovered | Participants/roles, assertion, Evidence standing, Scope, Producer, Consumer/purpose, Authority, occurrence, conflicts, and limits are active relation dimensions. |
| represented comparison basis | adjacent but non-identical | Response coordinates and Fidelity bounded expectations are represented bases for their own families only. |
| collection of relation Standings | adjacent but non-identical | Session meaning-relation dictionaries are event-local projections; no general established relation-Standing collection was recovered. |
| PESC testimony | represented only in report testimony | The orientation report supplies the PESC label and “applicable relation grammar” prose; active law does not adopt the compound. |
| Authority for forming any proposed grammar | Unknown | No exact responsible formation boundary was recovered. |
| Evidence warranting inclusion in any proposed grammar | Unknown | No inclusion Responsibility or grammar subject was recovered. |
| Producer | Unknown | Constructor of a caller-input carrier is not constitutional Producer of proposed grammar. |
| production Act | not recovered | Owning Responsibility remains Unknown. |
| production occurrence | not recovered | No exact responsible occurrence independently forms the proposed grammar. |
| produced representation | not recovered | No admitted compared grammar representation was found. |
| Consumer | Unknown | CLI/formatter consumers of the candidate carrier are not the proposed grammar Consumer. |
| Consumer purpose | Unknown | No proposed comparison Consumer was recovered; report-purpose prose cannot supply identity and purpose. |
| Applicability | not recovered | No occurrence determines either side applicable to this proposed Compare. |
| Admission | not recovered | No occurrence admits either side to this proposed Compare. |
| Compare Responsibility | Unknown | No active clause assigns the exact owner and complete responsibility. |
| Compare Act | not recovered | An Act cannot be recovered without its exact owning Responsibility. |
| comparison occurrence | not recovered | No event, call path, or test evidences the proposed occurrence. |
| comparison result | not recovered | Candidate outcome prose and adjacent result kinds cannot be imported. |
| Standing established from comparison | not recovered | No occurrence or standing-establishment boundary was recovered. |

The recovered relation dimensions are constitutional law about relation Claims
and Standing. They are not a represented grammar, and the list does not admit a
candidate to comparison.

## 6. Existing and proposed Compare-family matrix

Cells are populated only from independent evidence for the exact family.

| Coordinate | Operator response representation vs Presentation coordinate | Proposed candidate-versus-relation-grammar family | Testimony vs testimony | Constitutional grammar vs bounded expectation vs implementation witness |
| --- | --- | --- | --- | --- |
| exact Responsibility | bounded response comparison under `08.Communication` | Unknown | bounded testimony comparison under `05.Testimony.E` | Fidelity production under `01.External.D` |
| Producer | runtime comparison function produces recorded result; constitutional local producer is the responsible response-comparison boundary | Unknown | local bounded comparison boundary; no universal named producer | bounded Fidelity comparison boundary |
| Consumer | Identification consumes the response comparison finding where binding is applicable | Unknown | Unknown for a particular result | downstream cross-seam consumers may preserve an already-produced finding's limits; particular Consumer Unknown |
| proposed compared subjects or representations | captured ingress content and exact recorded response-coordinate set of one Presentation | candidate side not admitted; proposed grammar representation not recovered | multiple independently preserved testimonies or findings | constitutional grammar, bounded expectation, implementation witness |
| Applicability | exact exchange lineage and recorded Presentation preconditions; binding Applicability belongs to later Identification | not recovered | local to the instantiated comparison; no universal determination specified | declared seam or Scope bounds the comparison |
| Admission | comparison precondition checks are evidenced; no separately named Admission occurrence is established | not recovered | Unknown for a particular instantiation | Unknown for a particular instantiation |
| Authority | bounded to one exchange and exact coordinate equality; no intent, meaning, selection, authorization, or treatment | Unknown | comparison must preserve each input's Authority; exact comparison Authority local | constitutional grammar and declared bounded expectation within seam/Scope; no global certification or correction Authority |
| Evidence | Presentation formation/emission, capture, ingress, and exact reference lineage | Unknown | each input's preserved support basis plus exact local occurrence Evidence | constitutional subject, expectation, witness, Evidence/provenance, invariants, conflicts, Unknowns |
| Scope | exact workspace, session, Presentation, and response attempt | Unknown | bounded comparison and each input's Scope | declared examined seam or Scope |
| Compare Act | exact equality of captured representation to response coordinates | not recovered | bounded comparison of preserved testimonies/findings | bounded constitutional comparison |
| occurrence | recorded as `operator.exchange.comparison_occurred`; tests independently exercise it | not recovered | no particular occurrence claimed by the active general clause | no particular Prometheus or repository-wide occurrence claimed here |
| result | `match:<coordinate>` or `no-coordinate-match` | not recovered | bounded relation Standing such as agreement, disagreement, contradiction, conflict, refinement, unmet requirements, or responsibly established Unknown | faithful within Scope, unfaithful boundary crossing, crossing or mixed, or Unknown |
| Standing | exact bounded match/no-coordinate-match Standing, with stronger meanings withheld | not recovered | bounded relation Standing inside comparison boundary | qualitative Fidelity Standing inside Scope |
| no-match meaning | no exact Presentation response coordinate matched; intent, meaning, selection, and treatment remain Unknown | not recovered | no generic no-match result established | not a named general result; exact qualitative findings govern |

### Family relations

The independently established relations are:

```text
shared word Compare:
operator response, bounded testimony comparison, and Fidelity use comparison
language in active law

shared dimensional discipline:
each exact responsible family preserves its own subject, Authority, Evidence,
Scope, occurrence, limits, and Unknowns where applicable
```

The following are not established:

```text
shared Responsibility
shared compared-representation shape
shared result kind
shared Warrant
candidate-versus-relation-grammar family membership
```

Response-coordinate Compare is not testimony comparison by identity. Testimony
comparison is not the proposed candidate-versus-grammar family by identity.
Fidelity does not establish a generic relation-grammar representation.

## 7. Candidate-side Standing

| Candidate-side question | Finding |
| --- | --- |
| caller-supplied candidate representation | recovered: the caller supplies `CandidateExternalGrammarInput`, and the constructor preserves it in a frozen carrier after structural checks |
| preserved structural testimony | recovered: structural Claim, Scope, provenance strings, testimony references, alternatives, and Unknown strings are copied without semantic evaluation |
| an attributed Claim set | partially recovered: active law makes candidate production attributed and the runtime labels these caller hypotheses; the collection shape does not warrant each Claim or establish a constitutional collective Standing |
| applicable to an exact Compare | not recovered |
| admitted to an exact Compare | not recovered |
| an established grammar | not recovered |
| a Seed-native relation Standing | not recovered |

Accordingly, this report refers to `CandidateExternalGrammarSet` only as a
caller-supplied candidate representation or read-only carrier of preserved
structural testimony. Candidate representation availability does not establish
Applicability. Applicability would not establish Admission. Admission would not
establish that a comparison occurred.

The constructor is the runtime producer of the carrier instance in ordinary
implementation terms. Constitutional Producer identity for the represented
Claims remains Unknown because the caller's source role, formation occurrence,
provenance standing, Authority, and Warrant are neither validated nor supplied
by copying. The carrier has no event identity, no Evidence-standing result, and
no Seed-native Standing beyond what its exact read-only preservation boundary
witnesses.

## 8. Proposed grammar-side Standing

No proposed compared relation-grammar representation was recovered within the
inspected repository boundary.

Independent partial shapes remain separate:

| Partial shape | What it preserves | Why it is not the proposed grammar side |
| --- | --- | --- |
| active relation dimensions | participants/roles, assertion, Evidence standing, Scope, Producer, Consumer/purpose, Authority, occurrence, conflicts, limits | constitutional requirements are not a produced representation or admitted comparison basis |
| source-attributed relation proposal | external source, translated assertion/relation proposal, Scope, provenance limits, conflicts and loss | proposal is not established relation Standing and translation withholds comparison, Applicability, and Admission |
| operator meaning-relation event | exact local participants, proposition, attributed basis, lineage, Authority limits, occurrence, conflicts/loss/Unknowns | one established local relation is not a grammar for comparing arbitrary candidates |
| projected meaning-relation dictionary | replay reconstruction of exact session events | projection is not a generic collection Standing or grammar representation |
| `CandidateExternalGrammarSet` | caller hypotheses and testimony strings | candidate carrier is not the proposed grammar side and no semantic verification occurs |
| Book clauses and dimension lists | constitutional law and required distinctions | law text or a list is not an admitted compared representation |
| response-coordinate set | exact tokens within one Presentation | basis belongs solely to response equality comparison |
| Fidelity bounded expectation | exact expectation within an examined seam or Scope | expectation belongs to Fidelity and does not supply relation grammar |
| Prometheus decoded sample and observation shape | provider-local decoded and interpreted observation material | provider translation shapes neither assert relation grammar nor participate in this Compare |

No responsible composition occurrence combines these shapes. Their adjacency,
capitalization, recurring fields, or relation-shaped vocabulary cannot form the
missing representation.

The following proposed-grammar coordinates therefore remain:

```text
identity: not recovered
participants and roles: not recovered for this subject
relation assertion: not recovered for this subject
Evidence standing: Unknown
Warrant: Unknown
Scope: Unknown
Producer: Unknown
Consumer and purpose: Unknown
Authority: Unknown
production occurrence: not recovered
conflicts and known loss: Unknown
Applicability: not recovered
Admission: not recovered
Standing: not recovered
```

## 9. Validation/reconstruction/Compare distinctions

### Validation

`assemble_candidate_external_grammar_set(...)` validates required strings and
candidate-id uniqueness. The response comparison function validates that
formation, emission, capture, and ingress records belong to the exact exchange.
The operator session projector validates event kinds, references, and carried
coordinate agreement. These checks enforce producer or projector invariants.
They do not compare a candidate representation against relation grammar.

### Reconstruction

The session projector reconstructs recorded response comparisons,
identifications, represented-source recoveries, and meaning relations from the
ledger, rejecting forged or inconsistent records. Reconstruction recovers what
recorded events assert under projector rules. It does not establish the upstream
occurrence merely by reconstructing it, and it does not create a new proposed
comparison.

### Relation establishment

The meaning-relation path records a bounded relation that an exact represented
source expresses an exact attributed proposition. It consumes attributed
developer testimony after exact represented-source recovery. Its result is
bounded meaning-relation Standing with stronger operator intent, selection,
goal, and treatment claims withheld. Relation establishment is not validation,
reconstruction, or the proposed Compare.

### Compare

The response path performs an exact Compare because active law and runtime
independently recover its Responsibility, subjects, Authority boundary,
Evidence chain, occurrence, and result. `05.Testimony.E` and `01.External.D`
establish other bounded comparison Responsibilities with different subjects.
No corresponding recovery was made for the proposed family.

Thus:

```text
ordinary value agreement check != constitutional Compare by identity
structural refusal != Compare by identity
projector reconstruction != Compare by identity
meaning-relation Warrant != comparison result
```

## 10. No-match boundary

Current active grammar establishes a no-match result only for the exact
closed-choice response-coordinate family: captured response representation did
not equal any exact coordinate of that Presentation. It does not establish
operator intent, nonparticipation, negative meaning, selection, requested
treatment, or an opposing relation.

For the proposed family, no right-side representation, Applicability,
Admission, Compare Responsibility, occurrence, or result was recovered.
Therefore this report does not claim a no-match finding. It preserves:

```text
candidate does not match admitted grammar
!= candidate is false
!= candidate is unrelated

candidate lacks Warrant
!= candidate's negation is warranted

grammar not recovered
!= grammar positively recorded as absent

no applicable grammar recovered
!= no-match

right-side representation not recovered
!= comparison occurred

comparison occurrence not recovered
!= no comparison could ever be warranted
```

Active `05.Evidence.C` independently limits missing or unmatched findings to the
bounded corpus, surface, query or Claim form, temporal boundary, Authority, and
limitations that produced them. A stronger negative requires separate Authority
and Evidence.

## 11. Prometheus/Fidelity disposition

### Prometheus

Current runtime independently witnesses a read-only Prometheus Observation
source, allowlisted queries, provider JSON validation, decoded vector samples,
provider-local observation shapes, and Observation formation. Tests prove the
separation of provider sample from Observation, provider-local interpretation,
timestamp preservation, malformed-sample refusal, and selected suppression
boundaries.

Active law supplies adjacent Responsibilities: source grammar translation
preserves attribution and limits; Sensing produces bounded testimony through a
declared acquisition and interpretation boundary; external provider material is
not an Observation; Observation formation does not establish Fact, current,
verification, comparison, Applicability, Admission, or Learning Standing.

For Prometheus specifically:

| Coordinate | Disposition |
| --- | --- |
| exact constitutional Responsibility | partially recovered: provider acquisition/interpretation into Observation testimony is supported; exact full Prometheus-local ownership topology remains report testimony where active law does not assign it |
| compared subjects or representations | not recovered; this path decodes and maps provider samples rather than performing the proposed Compare |
| Producer of each represented stage | implementation functions/classes are recovered; constitutional producer coordinates are partially recovered at the general Sensing/translation boundary, not completely for every local stage |
| Consumer requiring a comparison result | not recovered |
| declared seam or Scope | provider endpoint, allowlisted query, decoded sample, and provider-local mapping boundaries are implementation evidence; no proposed comparison Scope is established |
| Authority and Evidence | read-only/allowlisted implementation boundary and provider testimony are evidenced; exact claim-relative constitutional Authority and Evidence standing remain local and incomplete |
| occurrence | collection and mapping paths are exercised by tests; no candidate-versus-grammar or instantiated Fidelity occurrence is inferred |
| result kind | provider-local shapes and Observation testimony, not a comparison result |
| relation to proposed family | not recovered |
| proposed grammar representation supplied | not recovered |

Prometheus is therefore an adjacent translation/Sensing implementation witness,
not a preferred route for the proposed family.

### Fidelity

`01.External.D` establishes the exact general Fidelity production
Responsibility: bounded constitutional comparison of constitutional grammar, a
bounded expectation, and an implementation witness within a declared seam or
Scope. It preserves Evidence and provenance, Authority, invariants, observed
erasure/invention/mutation/relocation, conflicts, Unknowns, and a lawful stopping
point. Its bounded qualitative result may be faithful within Scope, an
unfaithful boundary crossing, crossing or mixed, or Unknown. A Fidelity-shaped
artifact does not prove occurrence; the finding confers neither global
certification nor correction Authority.

For the proposed family:

| Coordinate | Disposition |
| --- | --- |
| exact Fidelity Responsibility | recovered at the general active-law boundary |
| exact subjects | constitutional grammar, bounded expectation, implementation witness |
| Producers | exact local producers of the three inputs remain instance-specific; the bounded Fidelity comparison produces its finding |
| Consumer | cross-seam consumers must preserve supplied limits, but a particular instantiated Consumer is Unknown |
| seam or Scope | required and declared per occurrence |
| Authority and Evidence | required and bounded as stated by `01.External.D` |
| implemented occurrence | not claimed for this orientation |
| result kind | recovered qualitative Fidelity Standing within Scope |
| relation to proposed family | no shared Responsibility, input shape, result kind, Warrant, or grammar representation recovered |
| proposed grammar representation supplied | not recovered |

Fidelity is a distinct existing constitutional family. Shared comparison
language does not authorize importing its constitutional grammar input as the
missing right-side representation of another family.

## 12. Exact established relations

The following relations are independently established within the inspected
boundary:

1. A bounded relation Claim or Standing is governed by its applicable
   dimensions; candidate relation, relation testimony, and established relation
   Standing are distinct.
2. External translation may preserve an attributed relation proposal without
   establishing Seed-native relation Warrant, Applicability, Admission,
   comparison, truth, or law.
3. `CandidateExternalGrammarSet` construction preserves caller-supplied
   structural testimony under a read-only, ledger-free, non-cluster-mutating
   boundary and performs only structural checks.
4. The closed-choice response family compares exact captured representation
   with exact Presentation response coordinates and records bounded match or
   no-coordinate-match Standing.
5. Identification consumes the response comparison finding and a locally
   applicable token-to-alternative binding; it remains distinct from Compare.
6. Represented-source recovery and attributed meaning-relation establishment
   are distinct from response Compare and from projector reconstruction.
7. Bounded testimony comparison and Fidelity comparison are independently
   established comparison Responsibilities with their own exact subjects.
8. Prometheus decoding and provider-local observation shaping witness
   translation/Sensing-adjacent boundaries, not the proposed Compare.
9. All recovered comparison families share only the word `Compare` and general
   Responsibility discipline where active law says so; no shared constitutional
   family follows.

No established relation connects `CandidateExternalGrammarSet` to an applicable
or admitted relation grammar, comparison occurrence, result, or Seed-native
relation Standing.

## 13. Exact Unknowns

For `candidate-versus-relation-grammar Compare`, the exact Unknowns are:

```text
whether the compressed phrase corresponds to any differently named exact
constitutional Responsibility

the exact owning Responsibility
the exact proposed candidate subject and its constitutional production Standing
the identity and Standing of any proposed grammar representation
the Authority for forming that representation
the Evidence and Warrant governing its contents
the Producer and production occurrence
the exact Consumer and Consumer purpose
the Applicability determination and its occurrence
the Admission requirement, boundary, and occurrence
the exact compared representations
the comparison method or relation
the Compare occurrence
the result kind
the result Producer and production occurrence
the Standing-establishment boundary and occurrence
the established result Standing
the no-match meaning, if any
any later Consumer Uptake
```

These are not positive declarations that the coordinates are constitutionally
instantiated with an Unknown value. They identify what this bounded orientation
could not recover. No failed search establishes global nonexistence, and no
report's `[UNRESOLVED]` wording supplies a Responsibility or construction gate.

### Visibility record

Files inspected included:

- active Book root and relevant active chapters under
  `book_of_seed/01-grammar-and-standing`,
  `book_of_seed/02-acts-and-constraints`,
  `book_of_seed/05-evidence-and-knowledge`, and
  `book_of_seed/08-authority-communication-and-stopping`;
- `seed_runtime/candidate_external_grammar.py` and its tests and CLI call sites;
- operator Presentation, response comparison, source recovery, session
  Standing, interaction goal, and their tests;
- Prometheus observation-source structures and focused tests;
- diagnostic inventory/shape-audit references to the candidate carrier;
- current attributed reports listed in section 4;
- Git history described in section 2, while excluding the reverted chain.

Searches and checks performed included exact and case-insensitive phrase
searches; symbol, call-site, event-kind, relation-shape, Applicability, Admission,
Compare, Prometheus, and Fidelity searches; focused source and test inspection;
history title/path inspection; expected-diff inspection; and a whole-report
coherence scan.

Visibility limits:

- the repository and history reachable from the current checkout are the
  inspected boundary;
- symbol searches do not rule out differently named partial shapes;
- passing tests evidence current behavior, not constitutional Authority by
  themselves;
- no external-Book source was required;
- the deliberately excluded reverted PR 2311--2314 artifacts remain visible in
  Git history only and did not contribute evidence or interpretation.

## 14. Construction authorization

No construction is authorized by this report.

**D. Required constitutional shape remains Unknown.**
