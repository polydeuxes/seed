# Eye–Competency Composition and Locality Characterization 009

## Repository state examined

Before changing files, the surveyed checkout reported:

- `git rev-parse HEAD`: `29962b7f79da19a058e143b35438d28a26d6d214`.
- `git status --short`: no output.

PR 1751 is present as `29962b7 (HEAD -> work) Add SQLite constitutional witness slice 001 (#1751)`. The required orientation, Book, and witness artifacts were present:

- `book_of_seed/sqlite_constitutional_witness_slice_001.md`.
- `eye_roadmap_orientation.md`.
- `town_clock_competency_orientation.md`.
- `witnesses/sqlite_constitutional_witness_slice_001/schema.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/fixtures.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/verify.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/README.md`.

The existing witness verification was run before changing files:

```sh
./witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh
```

Result: posture cases, record-not-truth case, no-universal-activity case, and forbidden-inference boundary passed.

## Eye evidence examined

`eye_roadmap_orientation.md` calls itself an orientation artifact, not implementation, constitutional law, or architectural authority. Its strongest claim is orientation: the Eye appears to be the constitutional core of the organism, ordered around observing reality, preserving reality honestly, recovering lawful understanding, and determining where future observation effort should be spent.

`town_clock_competency_orientation.md` preserves a behind-the-frontier metaphor. It says the Eye roadmap remains the frontier orientation, while the town-clock artifact is downstream orientation only. It explicitly does not recover the Eye implementation, introduce runtime behavior, or define dispatch, subscription, polling, scheduler, queue, worker loop, or notification mechanisms.

The Book chapters inspected provide constitutional support for examination, recording, evidence/provenance, event/fact/state separation, authority boundaries, and refusal/non-performance. They do not define the Eye as a Book constitutional identity, runtime owner, competency registry, projection, or composed artifact.

## Competency evidence examined

The strongest supported competency evidence is bounded and local, not organism-universal:

- `04.Examination.A` permits recorded material to be treated as relevant only when explicit record material supports local responsibility, subject binding, evidence or provenance requirements, and authority boundary. It forbids selection, execution, mutation, truth establishment, or required action.
- `04.Examination.B` makes lawful inactivity a positive result for irrelevant, unsupported, insufficiently bound, or outside-authority material.
- `08` authority material prevents internal models, selections, records, and handoffs from creating or enlarging authority.
- The SQLite witness declares rows for fixture examination and does not claim its table is the constitutional definition of bounded competency.

## Eye identity matrix

| Candidate Eye identity | Constitutional subject | Owned responsibility | Inputs | Acts or constraints | Outputs | Standing produced | Consumers | Implementation witness | Orientation-only evidence | Counterevidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seed itself as observer | Not established as a Book subject in this pass. | No single owned Eye responsibility recovered. | Reality, recorded material, current lawful condition are orientation vocabulary here. | Observation and honest preservation are orientation aims. | Lawful understanding and future observation effort are orientation aims. | No independent standing beyond existing recording, evidence, projection, and examination clauses. | Auxiliary capabilities may consume observation. | None specific to an Eye identity. | Eye roadmap organism-core language. | Roadmap disclaims law and implementation. |
| Organism-level faculty | Plausible orientation subject. | Constitutional observation as a faculty is suggested but not declared. | Observation, evidence, warrant, reliance, unknowns. | Must remain evidence-driven and repository-controlled. | Awareness, lawful understanding. | Orientation only. | Forecasting and other auxiliary capabilities are described as consumers. | None as a faculty object. | Eye roadmap says neighboring participants strengthen observation. | No owned boundary, stop condition, or authority table for a faculty. |
| Constitutional frontier | Best supported bounded characterization. | Frontier around observation and honest preservation. | Repository evidence and recorded constitutional change. | Repository authority wins; orientation may be refined or rejected. | Better questions and future observation direction. | Orientation standing, not runtime standing. | Town-clock orientation sits behind it. | No runtime implementation required. | Town-clock relationship section explicitly says Eye frontier remains primary. | Frontier is not a Book kind or executable owner. |
| Composed projection | Not recovered. | None recovered. | Multiple neighboring participants exist. | Composition not proven by adjacency. | No projection output recovered. | None. | None. | Some orientation lists participants. | Projection/state Book chapters do not identify Eye as a projection. |
| Family of responsibilities | Not recovered as constitutional identity. | Several responsibilities participate near observation. | Evidence, warrant, reliance, current lawful condition. | May participate without composing the Eye. | No family standing recovered. | None. | None. | Roadmap lists neighboring participants. | No family declaration, membership relation, or consumer. |
| Single bounded competency | Contradicted. | No single competency declaration for Eye. | No Eye-owned evidence/provenance/authority row. | No Eye stop condition or bounded acts recovered. | None. | None. | Current witness has a competency row formerly named with Eye but without Eye semantics. | None beyond metaphor. | Schema has no `eye` field or relation; Book lacks Eye competency law. |
| Orientation metaphor only | Strongly supported as minimum. | Orientation around constitutional observation. | Repository evidence. | Must not become law without evidence. | Investigation direction. | Orientation-only standing. | Future investigations. | Orientation documents. | The word Eye appears in orientation files, not implementation. | The roadmap's organism-core language suggests a stronger future possibility, but not enough for law. |

## Bounded competency characterization

Smallest supported meaning: a bounded competency is a declared examination responsibility whose possible movement is limited by explicit responsibility family, responsibility subject, authority boundary, evidence/provenance requirements, and lawful inactivity or stop conditions. Its identity permits examination of relevance only inside those boundaries. It does not create universal observation, notification, action, dispatch, truth establishment, or authority.

Current `bounded_competencies` column classification:

| Column | Classification | Reason |
| --- | --- | --- |
| `competency_id` | Required by this witness only | A row needs identity for SQL verification, but the Book has not recovered general competency identity grammar. |
| `responsibility_family` | Constitutionally required for this witness's bounded relevance claim | Relevance requires local responsibility support. |
| `responsibility_subject` | Constitutionally required for this witness's bounded relevance claim | Subject binding is part of `04.Examination.A`. |
| `authority_zone` | Constitutionally required for this witness's bounded relevance claim | Authority boundaries limit movement. |
| `requires_provenance` | Constitutionally required for this witness's evidence boundary | Provenance is needed where the declared responsibility requires it. |
| `requires_evidence` | Constitutionally required for this witness's evidence boundary | Evidence support is needed where the declared responsibility requires it. |
| `stop_condition` | Descriptive label with constitutional direction | Lawful inactivity and stopping are supported, but this string is witness-local wording. |
| `book_clause_id` | Required by this witness only | It preserves traceability from fixture rows to recovered clauses. |

## Locality dimensions supported

| Dimension | What establishes locality | Preserved by | Consumer/check | Assertion limited | Travels? | Current SQL witness represents it? |
| --- | --- | --- | --- | --- | --- | --- |
| Responsibility locality | Matching `responsibility_family` and `responsibility_subject`. | `bounded_competencies` row and `competency_change_examination` CASE. | SQL verification expected postures. | Relevance and further examination. | Only as explicit represented fields. | Yes. |
| Subject locality | `responsibility_subject` compared with `observable_subject`. | Same row/view relation. | Irrelevance cases. | A competency cannot treat unrelated subjects as locally relevant. | Only if copied into another artifact. | Yes. |
| Authority locality | `authority_zone` equality before permission. | `authority_zone` fields and authority-blocked posture. | Authority-blocked verification. | Relevance cannot become permission outside authority. | No automatic transfer. | Yes. |
| Evidence/provenance locality | `requires_evidence`, `requires_provenance`, and explicit refs. | Fixture fields and insufficient-evidence posture. | Insufficient evidence verification. | Missing support blocks movement. | Evidence/provenance refs may travel only as represented refs, not as truth. | Yes. |

## Locality dimensions contradicted or unsupported

| Dimension | Result | Reason |
| --- | --- | --- |
| Inquiry locality | Unsupported and contradicted as a reading of the current witness. | No `inquiry_ref`, `question_ref`, `frontier_ref`, `examination_ref`, `orientation_ref`, or `session_ref` participates in the witness result. |
| Observation-context locality | Unresolved. | `local_observation` names an authority zone, not a source context, host context, or evidence horizon relation. |
| Organism locality | Unsupported in SQL. | The fixture does not distinguish Seed-internal, process-local, external provider, or operator-local evidence. |
| Host/process locality | Unsupported. | No host, process, runtime, source context, or session field exists. |

## Inquiry-locality result

Neither `competency:eye-evidence-local` nor `authority_zone = local_observation` can lawfully be interpreted as evidence local to the current inquiry. The witness has no represented inquiry, question, frontier, examination, orientation, or session binding. Therefore the current fixture is not inquiry-local.

## Seed-locality result

The fixture can be interpreted only as local to one represented authority zone and one represented responsibility/subject boundary. It cannot be interpreted as local to Seed's internal state, the current Seed process, one observation source, one organism identity, or one inquiry without additional represented relations.

## Identifier-token analysis

The original identifier was `competency:eye-evidence-local`.

| Token | Represented semantic owner | Schema field or relation | Book support | Orientation support | Implementation effect | Rename behavior effect | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `competency` | Fixture row in `bounded_competencies`. | `competency_id` primary key. | Bounded examination clauses support responsibility, not general identity grammar. | Town-clock citizen metaphor. | Joins expected rows in verification. | Requires updating fixture references only. | Witness identity label. |
| `eye` | None in schema. | None. | None recovered. | Eye roadmap/frontier orientation. | None except string identity. | No constitutional outcome changes. | Unsupported semantic claim in the fixture name. |
| `evidence` | Responsibility subject and evidence requirement. | `responsibility_subject = evidence_boundary`; `requires_evidence = 1`. | Evidence/provenance and recording clauses. | Neighboring Eye participant. | Affects relevance and insufficient-evidence posture. | Preserved by descriptive replacement name. | Supported, when bounded to evidence boundary. |
| `local` | Authority-zone value only. | `authority_zone = local_observation`. | Authority boundary support. | Local citizen metaphor. | Affects authority-blocked posture. | Preserved as local observation authority. | Supported only as authority locality. |

## Universal-observation / CROSS JOIN result

The `CROSS JOIN` in `competency_change_examination` computes every competency/change pair for deterministic witness analysis. It does not mean every competency receives every change, observes every change, examines every change at runtime, is awakened by the record, or has been notified. A query pair exists only as a calculated row; calculated relevance is not dispatched relevance checking.

The README was corrected to state this enumeration boundary explicitly.

## Eye–town-clock–competency topology

The supported topology is closest to: the Eye is an orientation placed above several independent observation and examination responsibilities. The town-clock paper positions recorded constitutional change behind the Eye frontier. Bounded competencies may examine local relevance of recorded change and may preserve lawful inactivity or bounded permission for further examination. The evidence does not support a single pipeline where the Eye owns all observation, nor a composition where competencies collectively constitute the Eye.

## Current fixture meaning

After correction, the fixture `competency:evidence-boundary-local-observation` means:

- one fixture competency row;
- responsibility family `constitutional_change`;
- responsibility subject `evidence_boundary`;
- authority zone `local_observation`;
- required provenance and evidence;
- inactivity when irrelevant, unknown, unsupported, or authority-blocked;
- Book traceability to bounded relevance.

It does not mean Eye ownership, inquiry locality, organism-local standing, source-local standing, subscription membership, dispatch readiness, runtime observation, or universal notification.

## Current fixture naming verdict

`competency:eye-evidence-local` overstated the implemented relation because `eye` had no schema owner, Book owner, or implementation effect, and `local` was only an authority-zone value. The smallest bounded correction was to rename it to `competency:evidence-boundary-local-observation`, preserving the represented evidence-boundary subject and local-observation authority without adding schema fields.

## SQLite witness corrections made

- Renamed the fixture identity from `competency:eye-evidence-local` to `competency:evidence-boundary-local-observation` in fixtures and verification references.
- Clarified the README naming boundary: the fixture does not name the Eye, bind to an inquiry, or assert organism-level observation.
- Clarified the README enumeration boundary: complete SQL enumeration is not broadcast, notification, subscription, polling, receipt, observation, or awakening.

No schema fields, dispatch, subscription, runtime behavior, or Eye runtime were added.

## Book clause recovered, if any

No new Book clause is recovered in this pass. The candidate bounded competency declaration remains plausible, but current evidence is still best handled by the existing `04.Examination.A`, `04.Examination.B`, recording, evidence/provenance, authority, and refusal clauses. The Eye itself is not promoted into Book law.

## Orientation vocabulary retained as orientation only

Eye, frontier, town clock, citizen, and organism-level observation are retained as orientation vocabulary. They do not become constitutional kinds, runtime owners, registries, dispatchers, or proof that competencies compose the Eye.

## Constitutional vocabulary recovered

This pass recovers only bounded relevance, positive lawful inactivity, recorded assertion standing, evidence/provenance requirements, authority boundary, and record/fact/state separation as directly usable constitutional vocabulary for the witness.

## Claims contradicted

- The Eye is one bounded competency: contradicted by absence of Eye competency declaration, owned evidence, authority, acts, outputs, and stop conditions.
- The current SQL fixture is inquiry-local: contradicted by absence of inquiry/session/frontier binding fields.
- `CROSS JOIN` implies broadcast or universal observation: contradicted by witness boundary and README correction.
- `local_observation` means Seed-local, process-local, inquiry-local, source-local, and authority-local simultaneously: contradicted by represented fields.

## Claims remaining unresolved

- Whether the Eye will later become a constitutional subject, faculty, projection, composition, or implementation boundary.
- Whether a general bounded competency declaration should become Book law.
- Whether observation-context locality or organism locality should receive represented grammar.
- Whether future implementation will add relevance checking, without implying dispatch or universal activity.

## Files changed

- `book_of_seed/eye_competency_composition_locality_characterization_009.md`.
- `witnesses/sqlite_constitutional_witness_slice_001/README.md`.
- `witnesses/sqlite_constitutional_witness_slice_001/fixtures.sql`.
- `witnesses/sqlite_constitutional_witness_slice_001/verify.sql`.

## Verification command and result

Command:

```sh
./witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh
```

Result: posture cases, record-not-truth case, no-universal-activity case, forbidden-inference boundary, and full SQLite constitutional witness slice 001 verification passed.

## Bounded resolution

the Eye is an organism-level frontier or orientation within which bounded competencies participate
