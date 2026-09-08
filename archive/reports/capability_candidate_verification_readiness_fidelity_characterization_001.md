# Capability candidate → verification evidence → promotion readiness Fidelity characterization 001

## 1. Boundary, authority, and answer

This is one bounded, report-only characterization of current commit `22f9609`
(`Excise capability verified district (#2011)`). It changes no implementation,
test, fixture, schema, export, interface, event, persistence, projection, Book,
root documentation, `docs/`, campaign, or prior report. Current implementation,
focused tests, active Book, Event Ledger, and projected State control. The parent
diff is used only to identify deletion topology; historical reports are leads and
counterevidence, not authority.

**Answer to the governing question.** `verification_evidence` makes exactly one
positive claim: for a package-derived candidate whose identifier is in a fixed
five-entry candidate-to-binary table, the first named path found by ordered PATH
inspection was, at inspection time, both `Path.is_file()` and `os.access(...,
X_OK)`. It does not verify the candidate, the binary, invocation, a
transformation, a result, or competency. `capability_promotion_readiness` then
joins the already-required package support to those PATH records by candidate
string and labels the row `supported` iff both lists are nonempty. It performs no
promotion and has no remaining promotion consumer.

The truthful core is a transient **candidate-correlated executable-file
availability measurement**. The names `verification_evidence`, `supported`,
`promotion`, and `readiness` compress or overstate that core. Neither artifact is
an evidence-born competency foundation: neither identifies or compares a bounded
transformation, preserves its grammar, establishes applicability, checks
dependencies, carries authority, records an occurrence, runs a mechanism, or
compares a result. The readiness object is the surviving tail of the deleted
capability-verification/promotion model, while VerificationEvidence is a mixed
object: useful executable-file observation entangled with that legacy
destination vocabulary and package-gated candidate association.

Deletion is not lossless: it would remove truthful visibility that a candidate's
configured binary name currently resolves to an executable file and would remove
that correlation from the single-capability projection. Preservation under the
present names is not warranted either. The smallest exact next action is a
separate implementation pass to **delete `CapabilityPromotionReadiness` and its
CLI/public export/tests, and narrow/rename `VerificationEvidence` to a plainly
named, occurrence-bearing candidate↔executable-file observation view while
retaining its single-capability visibility**. That pass must not add invocation,
verification, competency standing, selection, authorization, or promotion.

## 2. Current road, crossing by crossing

### 2.1 Package Observation/Evidence/Fact → `CapabilityCandidate`

| Question | Current answer |
|---|---|
| subject and bounded transformation | Current projected Facts with predicate `package_installed` are matched by lower-cased package value against a fixed table; e.g. `python3` or `python` → `python_runtime`. Subject identity is copied only into `CapabilityCandidateEvidence.subject_id`; candidate identity is a table value, not a globally established capability. |
| producer occurrence | A caller runs `build_capability_candidates`. The returned artifact has no builder occurrence id/time. The input Fact can preserve `fact_id` and `observed_at` internally, but candidate evidence omits `observed_at`. |
| exact input evidence | Any projected `Fact(predicate="package_installed")`; no requirement that referenced Evidence exists. If it does, evidence summaries are copied from `build_fact_evidence_view`. The fact index changes lookup mechanics, not output. |
| projection/comparison | Exact normalized package-name membership in `_PACKAGE_CAPABILITY_CANDIDATES`; optional filter aliases normalize user text. No package state, architecture, version, provenance quality, conflict, expiry, current support, or installation verification comparison. |
| output standing | Candidate preservation with confidence label `supported_by_observed_package`; expressly not capability proof. |
| source/provenance | Fact id, predicate, subject, value, source type, confidence, evidence ids and lossy summaries survive. Evidence payload, evidence source identity fields beyond summary, Fact observation time, event identity, and projection horizon do not. |
| scope/applicability | Host-like fact subject is preserved in support but not made the candidate subject or checked against PATH locality. Package-to-candidate applicability is hard-coded and unversioned. |
| grammar/mechanism/dependencies | Package names and candidate labels are compiled lookup vocabulary. No operation, input/output representation, command grammar, environment, dependency, or transformation is represented. |
| constraints/authority/currentness/conflicts | Boundary notes deny selection/policy/execution. No authority check, expiry/current-support check, conflict treatment, explicit Unknown, negative evidence, or known-loss field. |
| refusal | Unknown package values, non-`package_installed` facts, and filter mismatches silently yield no candidate. Absence is not encoded as a finding. |
| exact consumer | VerificationEvidence's candidate universe; PromotionReadiness; candidate CLI/tests; single-capability composition; otherwise callers of the public API. |

The first crossing already proves `package installed != executable present` and
`candidate != operational realization`.

### 2.2 `CapabilityCandidate` → executable-PATH inspection → `VerificationEvidence`

| Question | Current answer |
|---|---|
| subject and bounded transformation | For each package-derived candidate, map its candidate string through `_CAPABILITY_BINARY_CANDIDATES`, scan PATH directories in order, and emit one record for the first matching name that is a file and X_OK. The represented subject is the candidate string; the actual measured subject is a path entry. |
| producer occurrence | `build_verification_evidence` performs synchronous local filesystem metadata checks. No occurrence id, inspected-at time, host/workspace, PATH snapshot, caller purpose, or producer version is preserved. |
| exact input evidence | A `CapabilityCandidateInspection` (supplied or rebuilt), a supplied PATH string or process `PATH`, the fixed name table, and live filesystem metadata. Package evidence gates all output but is not copied into each VerificationEvidence. |
| projection/comparison | Candidate-string lookup plus ordered `is_file && X_OK`; the first success for each allowed binary name is retained. It neither uses `shutil.which` nor checks what the file contains. `OSError` is swallowed into absence. |
| output standing | `evidence_type="binary_path_observed"`, `observation_source="local_path_inspection"`, absolute/relative path string, rationale, and denial notes. Lawful standing is only “this path passed these two metadata predicates during this unrecorded inspection.” |
| source/provenance | Candidate label, observation-source label, path value, binary-name note, and metadata-only note survive. Package support, PATH entry ordinal, symlink resolution, stat identity, device/inode/hash, ownership, interpreter/loader, environment, error observations, time, host, workspace, and code/table version do not. |
| scope/applicability | Scope is implicitly the builder process filesystem and PATH. There is no binding between package Fact subject (`localhost` or otherwise) and the filesystem inspected. Consumer-local applicability is absent. |
| grammar | Only a binary filename token is preserved. No argv, stdin, environment, protocol, accepted input representation, produced output representation, exit/result grammar, or claimed transformation. |
| mechanism/dependencies | X_OK file presence is measured. Shebang/interpreter, dynamic loader, libraries, services, sockets, credentials, configuration, architecture, sandbox, working directory, and runtime dependencies are not. |
| constraints/authority/currentness/conflicts | Denials state no permission/approval/policy/execution. No affirmative authority or constraint fields. Currentness is ephemeral at check time and unrecoverable afterward. Multiple PATH hits and alternate binary names may produce multiple records, but no ambiguity/conflict relation is formed. |
| refusal | No candidate means no scan/output. Missing/non-file/non-X_OK or any caught `OSError` silently gives no record. Empty PATH segments become `.`. Absence is not a negative finding and errors are lost. |
| exact consumer | PromotionReadiness joins records by candidate; single-capability projection displays them by normalized string; dedicated CLI/tests display/reinforce them. No invoker or selector consumes them. |

Thus `executable present` here means “file and X_OK under this process check,”
not invocable. Invocable mechanism would still not prove a bounded
transformation reachable.

### 2.3 `VerificationEvidence` → `CapabilityPromotionReadiness`

| Question | Current answer |
|---|---|
| subject and bounded transformation | For every package-derived candidate, group PATH records by equal candidate string, copy package support and PATH support into an implementation-local `_CapabilityVerificationPayload`, and classify it. |
| producer occurrence | `build_capability_promotion_readiness_inspection`; no occurrence id/time and no retained identity for the intermediate payload. |
| exact input evidence | Candidate support is necessarily nonempty for every candidate built by the public road; verification support is zero or more PATH metadata records. |
| exact predicate | `bool(candidate_support) and bool(verification_support)` → `supported`; otherwise `unsupported`. In normal construction only the second term varies. |
| projection/comparison | Co-presence and candidate-string equality only. It does not compare package subject to inspected host, package contents to path, binary provenance to package, behavior to a claim, or positive to negative/ambiguous results. |
| output standing | A read-only presentation conclusion that both inspected lists are nonempty. Boundary notes explicitly deny promotion, competency standing, selection, authority, decision, policy and invocation. |
| source/provenance | Copies candidate support and VerificationEvidence, preserving their partial provenance and all their losses. Adds no comparison evidence or provenance. |
| scope/applicability/grammar | No new scope or applicability. No invocation or transformation grammar. Candidate-string association is the whole relation grammar. |
| mechanism/dependencies/constraints/authority | None evaluated beyond upstream file/X_OK. Denials are boundaries, not positive constraint or authority evidence. |
| currentness/conflicts/Unknowns | No occurrence identity/time, expiry, refresh boundary, conflict model, Unknown list, ambiguity state, or known-loss field. `unsupported` conflates missing executable observation, errors, unmapped candidates, stale/mismatched locality, and unexamined conditions. |
| refusal | It never refuses a package candidate row. Missing PATH support becomes conclusion-shaped `unsupported`; there is no Unknown. |
| exact consumer | Dedicated CLI and tests, plus public API callers. No current projection, selector, Demand, movement, invoker, verification producer, fact producer, event writer, or competency consumer uses readiness. |

The internal name `_CapabilityVerificationPayload` and docstring “before
promotion admission checks” name stages that no longer exist. They are direct
topological evidence of legacy destination vocabulary, not evidence that a
verification or promotion act survives.

## 3. Naming cross-examination

| Active name | Implied act | Exact implemented act | Classification |
|---|---|---|---|
| `verification_evidence` | evidence that bears on, or results from, verification of some explicit claim | package-gated file/X_OK PATH observation with no proposition, behavioral comparison, or verifier | **broader than implementation** and **legacy destination vocabulary** |
| `capability_promotion_readiness` | assessed sufficiency/applicability for a real downstream promotion | nonempty package-support list AND nonempty PATH-record list; no downstream promotion survives | **actively misleading** and **legacy destination vocabulary** |
| `supported` | an identified claim has sufficient support within a stated scope | the two lists are nonempty | **mixed/compressed**; conclusion-shaped and broader than the predicate |
| `unsupported` | counterevidence or a completed insufficiency decision | no PATH record was emitted for a package candidate, including silence and swallowed errors | **actively misleading** |
| `promotion` | a later act changes/adopts standing | no act, producer, consumer, artifact, event, fact, or interface remains | **legacy destination vocabulary** |
| `readiness` | evaluated prerequisites make a subject ready for a named next act | file correlation only; applicability, grammar, dependencies, authority and next act absent | **actively misleading** |

Boundary notes reduce the risk of over-reliance but do not make the positive
names faithful. “Promotion readiness, but not promotion” still asserts readiness;
“verification evidence, but not verification” still implies a defined
verification proposition. Neither implication is implemented.

## 4. Asymmetric specimens

### 4.1 `python_runtime`: package evidence plus executable PATH entry

* **Observed:** projected `package_installed=python3` (or `python`) and, in the
  live inspection, the first `python3` and/or `python` path which is a file and
  X_OK.
* **Candidate:** `python_runtime`, carrying the package Fact's partial support.
* **Projected relation:** compiled package-name→candidate and
  candidate→binary-name mappings, then string-correlated co-presence. No proof
  that the observed path came from the package or belongs to the Fact subject.
* **Meaning of supported:** at least one package-support item and at least one
  matching PATH metadata record are present.
* **Lawful reliance:** a consumer may display that local correlation as a
  transient inspection result. It may not rely on Python starting, accepting
  Python grammar, executing code, producing a result, being applicable,
  selected, authorized, successful, verified, or competent.

### 4.2 Package-derived candidate with no executable observation

For `package_installed=openssh-client` with an empty directory PATH:

* **Observed:** package Fact only; absence of emitted PATH evidence is not a
  preserved negative observation.
* **Candidate:** `ssh_client`.
* **Projected relation:** package→candidate exists; candidate↔mechanism
  association has no positive instance.
* **Meaning of unsupported:** only that no VerificationEvidence record was
  emitted. It cannot distinguish missing file, non-X_OK file, mapping absence,
  filesystem error, subject/locality mismatch, or later change.
* **Lawful reliance:** candidate support exists; executable availability,
  invocability, operational realization and competency remain Unknown. A
  consumer may not infer capability absence or failure.

### 4.3 Executable observation without package evidence

Place an X_OK `git` stub on PATH with no `package_installed=git` Fact:

* **Observed by the environment:** the file is constructible and would satisfy
  `_find_binary` if called for `git`.
* **Observed by this road:** nothing. Candidate gating prevents the scan for
  `git_client`; there is no executable-only artifact.
* **Candidate:** none.
* **Projected relation / supported:** none; no readiness row exists.
* **Lawful reliance:** no conclusion about file presence or capability. This
  asymmetry proves VerificationEvidence is not a general executable observation
  inventory and that candidate↔mechanism association is fused to package
  candidacy.

### 4.4 Mechanism exists but claimed transformation is undemonstrated

The tests deliberately create X_OK text files containing only `stub` and name
them `ssh` or `git`:

* **Observed:** file and X_OK only.
* **Candidate:** package-derived `ssh_client` or `git_client`.
* **Projected relation:** filename convention associates the candidate with the
  stub. No file content, loader, invocation, or behavior is checked.
* **Meaning of supported:** still both lists nonempty—even if the operating
  system could not execute the stub.
* **Lawful reliance:** mechanism-file availability under the metadata predicate;
  no SSH connection, Git operation, input/output transformation, success, or
  verified result.

### 4.5 Structure / Documentation compiled behavior counterevidence

`StructureObservationBoundary` declares structural extraction and evidence
preservation while denying grammar ownership. `documentation_structure` has
actual compiled regex/parsing behavior that transforms Markdown text into
heading, section, link, code-block and relation records, with source paths and
line coordinates. Tests exercise those transformations. Yet active Book law
correctly says compiled behavior and compatibility evidence do not confer the
standing suggested by names.

* **Observed:** document bytes/text and concrete source-relative structures.
* **Candidate:** no package-derived CapabilityCandidate is formed.
* **Projected relation:** actual input→output compiled transformations recur,
  unlike the package/PATH road, but their constitutional competency standing is
  still not established merely by execution/tests.
* **Meaning of supported:** not applicable; package/PATH `supported` cannot
  recognize this stronger implementation evidence at all.
* **Lawful reliance:** consumers can rely on the bounded compiled projection and
  its declared limits, not infer learned/evidence-born competency. This is
  decisive counterevidence to treating package plus file presence as competency
  sufficiency.

## 5. Dimensional contamination audit

| Dimension | CapabilityCandidate | VerificationEvidence | PromotionReadiness |
|---|---|---|---|
| identity | candidate string plus support Fact ids/subjects | candidate string and path value; no observation id | candidate string; no relation/readiness occurrence id |
| evidence / provenance | partial Fact and Evidence summaries; payload/time lost | filesystem predicate asserted; no stat/path snapshot/package provenance | copies both partial lists; no comparison provenance |
| scope / locality | support subject preserved but not bound to candidate scope | process-local PATH/filesystem implicit, host/workspace absent | silently joins potentially different localities |
| applicability | compiled package map only | compiled candidate/binary map only | nonempty co-presence substitutes for applicability |
| grammar | package and candidate tokens | binary filename only | none beyond string equality/status vocabulary |
| constraints | denial notes; package constraints absent | X_OK and is-file predicate; operational constraints absent | no prerequisites beyond list truthiness |
| authority | source type copied; no use authority | explicitly no permission/approval | explicitly no selection/policy/authority; none evaluated |
| currentness / occurrence | Fact `observed_at` omitted; builder occurrence absent | live check with no timestamp/id/horizon | builder occurrence/time absent; no expiry |
| consumer purpose | generic inspection | “support later verification inspection,” whose producer is deleted | future promotion, whose act/consumer is deleted |
| conflicts / Unknowns / known loss | none structured; silence only | errors/alternatives/absence lost; none structured | binary `supported/unsupported` erases ambiguity |

`supported` therefore compresses absent locality binding, applicability,
transformation identity, grammar, dependencies, constraints, authority,
currentness, occurrence, conflict treatment, and consumer sufficiency into a
single conclusion-shaped status. It is not an eight-dimensional standing and
cannot lawfully serve as competency readiness.

## 6. Consumer audit and removal topology

| Candidate consumer | Active consumption | What disappears if both surfaces are removed | Classification |
|---|---|---|---|
| single-capability projection | consumes VerificationEvidence only; filters by normalized candidate string and displays count/records | truthful candidate-correlated executable-file visibility and an explicit Unknown when owner artifact is absent | truthful evidence visibility + candidate correlation; no readiness reliance |
| CLI | `--verification-evidence` emits JSON; `--capability-promotion-readiness` emits JSON; both inspect current projected state/PATH | two measurement/presentation commands | evidence measurement for first; presentation-only/future-stage status for second |
| diagnostic inventory | neither surface is registered | nothing | no ownership/visibility evidence; operational visibility gap in current state, not permanent ownership |
| diagnostic shape audit | neither has an implementation spec | nothing | neither surface is checked |
| candidate examination work | no imports, fields, or runtime references | nothing | unrelated examination scaffolding |
| examination frontier | no imports, fields, or runtime references | nothing | unrelated examination scaffolding |
| focused tests | direct tests preserve file/X_OK observation, status vocabulary, JSON shape, read-only behavior, public export, and readiness fact-index cache behavior | compatibility reinforcement disappears | truthful measurement tests plus test-only legacy reinforcement |
| public runtime API | both builders/types exported | callable presentation APIs disappear | reachability, not proof of operational reliance |
| operational selector/invocation road | none found | nothing | **no operational reliance** |
| Event Ledger / State / facts/projections | inputs are read; no output is recorded or projected into State | no cluster truth or recorded occurrence disappears | read-only; no mutation |

There is one real non-test consumer of VerificationEvidence: the
single-capability projection. There is no non-presentation consumer of
PromotionReadiness. Imports, exports, CLI presentation and tests demonstrate
reachability, not permanent ownership. The absence from diagnostic inventory and
shape audit also means the two operational CLI flags are currently invisible to
the repository's operational visibility contract; this report does not alter
those registries because the requested pass is report-only.

## 7. Artifact classifications

| Artifact | Supported classifications | Refused classifications |
|---|---|---|
| `CapabilityCandidate` | evidence-preserving observation view (partial); read-only examination scaffolding; mixed object | operational realization, competency evidence/readiness, promotion machinery |
| `VerificationEvidence` | mechanism-availability measurement; bounded relation projection; candidate operational-realization evidence only in the narrow sense of a candidate-associated executable-file observation; read-only examination scaffolding; mixed object; legacy capability-verification tail | verification, competency standing/readiness, invocation/result evidence |
| `_CapabilityVerificationPayload` | read-only join scaffolding; legacy capability-verification tail; consumerless outside its local classifier | verification payload in the constitutional/behavioral sense |
| `CapabilityPromotionReadiness` | bounded co-presence projection; promotion machinery vocabulary; read-only examination scaffolding; legacy capability-verification tail; mixed object | competency evidence/readiness, actual promotion |
| `supported` / `unsupported` | presentation-only binary status over list co-presence | verified/unverified behavior, applicability, sufficiency, operational availability |

PromotionReadiness is not wholly consumerless because CLI/tests/public callers
can display it, but its claimed destination is consumerless. VerificationEvidence
is not merely residue because the single-capability projection consumes its
truthful core.

## 8. Decomposition test

| Independently truthful material | Already recurs? | Current location / loss |
|---|---|---|
| package-derived capability candidate | **yes** | independently represented by `CapabilityCandidate` with partial Fact provenance |
| executable-file observation | **partly** | represented only after candidate gating; lacks occurrence/locality/stat identity and cannot represent executable-only specimen |
| candidate ↔ mechanism association | **yes, compressed** | compiled tables plus equal candidate string; relation has no identity, provenance, applicability, time, conflict, or standing |
| candidate operational-realization evidence | **partly** | file/X_OK is mechanism-availability evidence, not realized transformation evidence |
| consumer-local applicability | **absent** | no consumer, purpose, subject/locality, requirement, grammar, constraint, or authority comparison |
| competency standing | **absent** | explicitly denied; no establishment producer or artifact |

The road is compressing three separable truths—package-derived candidate,
executable-file observation, and their compiled association—into
“verification support” and then “promotion readiness.” The first already has an
owner. The second is real but under-specified. The relation recurs in two mapping
tables and readiness grouping but has no independent standing. Consumer-local
applicability and competency standing do not recur and must not be invented by a
rename.

## 9. Required distinctions resolved

* Package installed **does not equal** executable present: specimen 4.2.
* Executable present **does not equal** executable invocable: X_OK stubs pass.
* Invocable mechanism **does not equal** bounded transformation reachable: no
  invocation or transformation contract exists.
* Candidate **does not equal** operational realization: only compiled name
  association is projected.
* Verification evidence **does not equal** verification: no proposition/result
  comparison occurs.
* Evidence sufficient for this inspection **does not equal** competency
  sufficiency: the inspection requires only two nonempty lists.
* `supported` **does not equal** promoted, established, selected, authorized,
  invoked, successful, or verified result: all are absent or expressly denied.
* Readiness **does not equal** Demand or movement opened: neither is produced or
  consumed.
* The STOP boundary is real: no future stage follows automatically, and after
  PR 2011 the named future promotion stage does not exist.

## 10. Direct answers

1. **What exact observation produces VerificationEvidence?** For an already
   package-derived candidate with a fixed binary-name mapping, ordered PATH scan
   finds the first entry for a name where `Path.is_file()` and
   `os.access(path, os.X_OK)` are true.
2. **What is verified?** Nothing. A filesystem metadata predicate is observed;
   no explicit claim or result is verified.
3. **Does any executable run?** No.
4. **What exact predicate makes readiness supported?**
   `bool(candidate_support) and bool(verification_support)`.
5. **Does supported identify a bounded transformation?** No.
6. **Does it preserve invocation grammar?** No; only binary filename tokens.
7. **Does it evaluate dependencies beyond file presence?** Only the X_OK access
   bit/check. It evaluates no loader, interpreter, library, service,
   configuration, credential, protocol, or runtime dependency.
8. **Does it evaluate applicability, constraints or authority?** No. It carries
   denial notes but performs none of those evaluations.
9. **Does it preserve currentness and occurrence identity?** No. The check is
   live during construction but stores neither time, horizon, host/workspace nor
   occurrence id.
10. **Does it compare positive, negative or ambiguous behavior?** No behavior is
    observed. It records positive metadata hits only; silence, OSError and all
    ambiguity collapse to no record and eventually `unsupported`.
11. **Is promotion still a real downstream act?** No active producer, artifact,
    fact/event, selector, consumer, or CLI performs it after PR 2011.
12. **Does any operational consumer rely on readiness?** None found. CLI, public
    API and tests expose it; they do not operationally rely on it.
13. **What truthful information would be lost by deletion?** Candidate-correlated
    visibility of a configured binary name resolving to a file that passes X_OK,
    its path/name, partial package support in the readiness display, and the
    single-capability projection's evidence count/records.
14. **What false standing would be removed?** The implications that file
    correlation is verification evidence, that nonempty lists support a claim,
    and that a candidate is ready for a real promotion stage; also the false
    negative flavor of `unsupported`.
15. **Is either artifact a foundation for the evidence-born competency probe?**
    No. VerificationEvidence is at most possible raw mechanism-availability
    testimony after narrowing. PromotionReadiness supplies no competency
    dimension or establishment act.
16. **Is either merely a renamed continuation of `capability_verified`?**
    PromotionReadiness is a surviving pre-admission tail and retains explicit
    verification/promotion vocabulary, so **yes in topology, no in standing**: it
    neither reads nor recreates the deleted predicate. VerificationEvidence
    predates the final act and has a truthful measurement core, so it is **mixed,
    not merely renamed continuation**, though its name/purpose remain legacy.
17. **Is narrowing, renaming, decomposition or excision warranted?** Evidence
    independently warrants excision of PromotionReadiness and narrowing/renaming
    of VerificationEvidence. Minimal decomposition should preserve candidate,
    executable-file observation, and association as distinct standings. No
    evidence warrants competency/applicability additions.
18. **What is the smallest exact next action?** In one separately authorized
    implementation slice: remove PromotionReadiness module/CLI/export/tests;
    rename and narrow VerificationEvidence and its CLI/single-capability field to
    candidate-associated executable-file observation; add occurrence/locality
    and explicit unknown/loss only where current producer evidence can truthfully
    supply them; register/audit the surviving diagnostic surface. Do not invoke
    binaries or create verification, competency, selection, authority,
    promotion, Demand, or movement.

## 11. Deletion/decomposition topology and stop

```text
projected package_installed Fact
  -> package-derived CapabilityCandidate                  [preserve]
  -> fixed candidate/binary-name convention              [expose as association]
  -> local file + X_OK observation                        [narrow/rename; preserve]
  -> "verification evidence"                             [remove overstated name]
  -> nonempty(candidate support) AND nonempty(path hit)
  -> "supported promotion readiness"                     [excise]
  -X-> capability verification / capability_verified     [deleted in PR 2011]
  -X-> promotion / competency / selection / invocation   [no current road]
```

Characterization stops here. This report does not create competency standing,
replace verification, invoke binaries, build a behavior harness, bind an
operational realization, select or authorize execution, add promotion, add
aliases, or edit the Book.

## 12. Evidence inspected and checks

Primary current implementation: `seed_runtime/capability_candidates.py`,
`seed_runtime/verification_evidence.py`,
`seed_runtime/capability_promotion_readiness.py`,
`seed_runtime/single_capability_state_projection.py`,
`seed_runtime/structure_observation.py`,
`seed_runtime/documentation_structure.py`, `seed_runtime/__init__.py`, and
`scripts/seed_local.py`. Consumer/visibility evidence:
`seed_runtime/diagnostic_inventory.py`,
`seed_runtime/diagnostic_shape_audit.py`,
`seed_runtime/candidate_examination_work.py`, and
`seed_runtime/examination_frontier.py`. Focused tests:
`tests/test_capability_candidates.py`, `tests/test_verification_evidence.py`,
`tests/test_capability_promotion_readiness.py`, and
`tests/test_single_capability_state_projection.py`. Constitutional controls:
active Book chapters on artifact standing, examination, and testimony/fact
standing. Deletion topology: commit `22f9609` diff only.

