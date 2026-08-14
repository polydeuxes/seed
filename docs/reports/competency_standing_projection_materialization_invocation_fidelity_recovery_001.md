# Competency Standing, Projection, Materialization, and Invocation Fidelity Recovery 001

## 1. Scope, authority, and stopping discipline

This is one bounded, report-only recovery against current merged `main` after
PR 2008 (`0cb5671`). It changes no implementation, test, fixture, schema,
export, interface, event, persistence, projection, canonical Book chapter,
documentation tree, campaign, or prior report. Reports were used only to locate
witnesses. Current implementation, tests, active Book, Event Ledger, and State
contracts control every adjudication below.

The governing question is whether evidence-born and compiled competencies are
origins of standing, materializations of standing, or provenance-relative
combinations, and what current producer-to-invocation road exists. The bounded
answer is **specimen-relative, with no implemented general relationship**.
Seed has (1) an evidence-to-projected-`capability_verified` standing road whose
admission producer is not implemented, (2) independently developer-compiled
behaviors that do not acquire competency standing from compilation or tests,
and (3) evidence-oriented candidate/readiness roads that deliberately stop
before standing. It does **not** currently join those roads to materialization
derivation, choice, authorization, invocation, result recording, or revision.

The first unsupported crossing in the proposed universal topology is:

> **constitutive evidence and occurrences -> competency-standing admission**

Evidence can be preserved, projected, and inspected, but the only current
standing marker is a `capability_verified` Fact and no production owner creates
one from candidate plus verification evidence. The readiness inspector says so
explicitly and remains read-only (`seed_runtime/capability_promotion_readiness.py:1-5,85-93,141-166`).
This report stops the proposed through-road there. Later crossings are tested
independently as existing islands; none is inferred to repair the first gap.

## 2. Controlling distinctions and terms

For this report:

* **evidence available** means an attributed `Evidence`, `Observation`, Fact
  provenance link, caller-supplied external-material record, test result, or
  inspectable occurrence exists. It is not standing.
* **competency standing** means current projected repository knowledge under the
  only implemented admission marker found: a subject-bearing
  `capability_verified` Fact and its `FactSupport`. Candidate, readiness,
  `ToolSpec`, catalog entry, code, and passing tests are not substitutes.
* **materialization** means the executable or inspectable form actually usable
  to perform a bounded transformation. It is not the abstract transformation,
  the mechanism alone, or standing.
* **compiled** means behavior embodied in developer-authored Python/regex/AST or
  an external executable. It says nothing by itself about competency standing.
* **invocation** means a consumer calls an implementation under a concrete input
  grammar. Construction, availability, selection, authorization, successful
  execution, and verified result remain distinct.

The implementation enforces the central separation. `ToolSpec` capability
labels widen inventory presentation but are expressly not evidence of presence,
availability, verification, authorization, or callability
(`seed_runtime/capability_inventory.py:41-49,174-200`). Verification facts,
not operation contracts, admit capability subjects
(`seed_runtime/capability_inventory.py:160-171,203-215`).

## 3. Current preservation and projection road

### 3.1 What the ledger can preserve

`ObservationIngestor.ingest_many()` turns each supplied observation into three
ordered event kinds: `observation.observed`, `evidence.observed`, and, unless
suppressed, `fact.observed`/`fact.inferred`. Each remains a separate event even
when persistence is batched (`seed_runtime/observations.py:81-97,99-171`). The
Evidence payload retains observation identity, source type, subject, predicate,
value, metadata, dimensions, expiry, confidence, and observation time; the Fact
links back by evidence id (`seed_runtime/observations.py:174-228`). The generic
ledger preserves arbitrary event payloads in append order; SQLite persists the
same event envelope (`seed_runtime/events.py:20-93,100-176`).

Therefore competency-relevant ledger preservation exists only when a producer
actually records relevant observations/evidence/facts. The ledger does not have
a dedicated competency occurrence, materialization, selection, invocation,
result, or revision event. In particular, current Structure/Documentation probe
outputs and both inspected campaigns declare no ledger write; their transient
results are not competency evidence in the ledger merely because code can
produce them.

### 3.2 What State projects

`StateProjector.project()` creates State, lists all workspace events, applies
them, and finalizes derived indexes (`seed_runtime/state.py:905-990`). Its event
decoder projects observation, evidence, Fact, goal, entity, and approval
payloads; it has no competency/materialization/invocation event decoder
(`seed_runtime/state.py:1130-1181`). Finalization rebuilds Fact support, evidence
relations, conflicts, expiry-sensitive current facts, and other indexes from the
event-derived objects (`seed_runtime/state.py:1000-1120`). Incremental projection
may start from a validated snapshot, but event history remains authority and the
compatible selection still performs full replay/finalization
(`seed_runtime/state.py:932-949`).

Active competency knowledge is the read-only capability inventory over current
State. Its universe combines two deliberately separated inputs:

1. admitted capability subjects named by projected `capability_verified` facts;
2. operation-contract labels from registered `ToolSpec`s, shown as metadata and
   normally `unverified` when no standing Fact exists.

The inventory derives `verified`, `provider_reported`, `unverified`, `stale`, or
`unknown` from current `FactSupport`; expiry changes a standing view to `stale`
without deleting ledger history (`seed_runtime/capability_inventory.py:111-139,218-280`).
Supporting Facts and Evidence are reopened through `build_fact_evidence_view`,
so evidence-backed inventory entries expose fact ids, evidence ids/type/summary,
confidence, observation times, source types, expiry, and age
(`seed_runtime/capability_inventory.py:250-280,326-359`). Reopenability is
bounded by what the original producer put into Evidence and Fact: there is no
automatic grammar version, applicability, conflict rationale, materialization
identity, invocation trace, or known-loss field specialized for competency.

### 3.3 What changes with new evidence

New recorded evidence becomes projected Evidence, but it does not revise
standing by identity. New `capability_verified` Facts can change current support,
conflicts, currentness, or inventory state on subsequent projection. Generic
Observation ingestion mechanically promotes an observation's predicate/value
to a Fact, but it does not adjudicate whether a competency observation is
constitutionally sufficient (`seed_runtime/observations.py:202-228`). No current
responsible competency admission/revision consumer was found. Readiness,
verification inspection, inventory, and candidate inspection all disclaim that
authority.

## 4. Asymmetric specimen recovery

### 4.1 Specimen 1 — current compiled Structure Probe

**Bounded subject/transformation.** “Structure Probe” is not one stable class.
The smallest current compiled structural witnesses are: (a) the
substrate-independent `StructureObservationBoundary`, which declares read-only
structural extraction/evidence preservation and disclaims grammar/substrate
parsing (`seed_runtime/structure_observation.py:1-58`); and (b) external-material
binding/structural/surface projection functions that validate caller-supplied
identity/hash/text and produce exact lines, regions, and bounded measurements.
The bounded competency candidate is **reopenably bind exact attributed material
and project declared structural measurements**, not “understand structure.”

**Standing.** No `capability_verified` subject is emitted or hard-coded for this
transformation. The boundary constant is a developer claim; tests demonstrate
compatibility behavior; caller manifests supply provenance. These are useful
evidence and compiled behavior, not current competency standing. Standing is
therefore **demonstrated compiled behavior; competency standing absent**.
Producer: developers plus callers for input claims. Scope: supplied artifact and
declared projection contract. Currentness: source revision under Git, with no
runtime competency version/invalidation record. Conflicts/applicability are
validated only where the request schemas express them. Unknown: who could admit
this behavior as standing. Known loss: boundary metadata has no constitutive
evidence ids or verification history.

**Preservation/projection.** The probe returns caller-visible records and is
read-only; it does not write the Event Ledger or State. Knowledge is recomputed
when the projection function is invoked from supplied material, not rebuilt as
competency State. A caller can reopen exact material/hash within the returned
road, but cannot reopen competency standing because none exists. New material
changes a new invocation's output; no standing revision consumer follows.

**Materialization.** Developer-authored Python dataclasses, validators, hashing,
UTF-8/text splitting, and projection functions are the inspectable realization.
They are independently compiled from source, not derived from established
standing. Dependencies include Python and the request/manifest grammar. Version
is repository commit/module source, not a materialization record. Invalidators
are source/contract/dependency change, incompatible hash/encoding/input, or
failed tests; no current invalidation owner records these as competency state.
Several functions cooperate in this bounded capacity, and the common structural
boundary participates in multiple substrate adapters. That proves composition
and reuse, not a first-class one-to-many materialization relation or selector.

**Invocation.** Direct function/CLI consumers supply manifest/request/text and
receive projection records. Authority is caller authority constrained by
read-only validation; the code selects no alternate materialization. Result
observations are returned, not automatically recorded, and cannot revise
standing without an absent admission/revision occurrence.

**Disposition.** **Mixed scaffolding**: bootstrap measurement instruments plus
developer-compiled candidate materializations and destination witnesses. The
boundary is not constitutional ownership merely because consumers import it.

### 4.2 Specimen 2 — current compiled Documentation Probe

**Bounded subject/transformation.** For the decisive asymmetric slice, the
subject is repository Markdown bytes and the transformation is: decode UTF-8,
split lines, suppress code-fence content, recognize the compiled ATX-like regex,
emit heading records, then derive title/section/depth/recurrence observations.
`observe_markdown_document()` visibly performs this composition
(`seed_runtime/documentation_structure.py:594-646`); `_ATX_HEADING_RE` and
`_heading_outline()` embody the one-to-six-`#` grammar and strip result text
(`seed_runtime/documentation_structure.py:1475-1500`).

**Standing.** No capability subject or `capability_verified` Fact exists for
“recognize ATX headings” or “observe documentation structure.” Producer of
behavior is developer source; tests demonstrate fixtures; the regex embeds a
grammar claim. Classification: **developer-compiled, compatibility-tested
behavior with no competency standing**. It is not compiled-only standing,
because compilation is not an admission path. Provenance of individual output
is file path/line, but output records omit grammar authority/version,
constitutive evidence, applicability decision, conflicts, and Typed Unknowns.
Known loss includes `.strip()` normalization and downstream strengthening of
the first H1 into title and heading records into section hierarchy.

**Preservation/projection.** The report is computed from repository files on
each invocation and not written to ledger/State. Historical document bytes are
not preserved by this probe. The result can be reopened to the current file and
line, not to constitutive evidence that warranted the regex. New documents or
code alter future output; nobody revises competency standing.

**Materialization.** The Python module plus compiled regex and downstream
functions are the exact realization. It is independently developer-compiled,
not generated from a learned rule, `capability_verified` standing, or external
evidence. Its input grammar is a repository root/options and UTF-8 `.md` files;
its output contract is documentation structure records/report. Python, regex
semantics, filesystem, and repository source are dependencies. No alternative
realization list or selection exists. The same module realizes many bounded
transformations (metrics, headings, links, fences, recurrence), so one
realization can participate in several competency candidates.

**Invocation.** The operational consumer is the diagnostic CLI/direct Python
caller requiring read-only documentation structure. CLI/options select filters
and output detail, not a competency materialization. Invocation has read-only
authority and explicitly no ledger/repository mutation. Results can be tested or
read by humans but are not recorded as observations/facts and cannot revise
standing automatically.

**Disposition.** **Mixed scaffolding**, predominantly a
developer-compiled destination witness. It demonstrates a useful downstream
shape and invocation, not the provenance road by which its embedded grammar was
earned.

### 4.3 Specimen 3 — evidence-oriented Graded Lessons external-material campaign

**Bounded subject/transformation.** The subject is the hash-bound four-line
Lesson 6 excerpt. The campaign binds supplied source/artifact/annotations,
projects exact structure/surface features, and renders caller-supplied candidate
grammar records. The campaign itself records that the author—not Seed—identified
headings, rules, examples, exercises, contrasts, support, and contradiction
(`campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py:194-212`).

**Standing.** The campaign establishes **attributed evidence and candidate
claims only**. It expressly labels provenance as campaign-local and source
authority unverified, carries correctness Unknowns, and distinguishes selected
artifact hash from parent-book hash
(`campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py:214-231`).
No `capability_verified` Fact, responsible admission act, applicable rule
selection, or current competency subject results. Standing: historical campaign
evidence/candidates; competency standing absent. Conflicts and alternatives can
be carried in candidate forms, but interpretation remains author-supplied and
general applicability Unknown.

**Preservation/projection.** Campaign records preserve source identity,
selection, annotations, supervision trace, testimony bindings, structural and
surface projections, and rendered candidates in a returned dictionary. They do
not write Event Ledger or State. Reopenability exists to the fixture/hash/line
bindings, not via current capability inventory. A rerun recomputes these
artifacts; new evidence has no admission/revision consumer.

**Materialization.** The evidence road uses developer-authored campaign Python,
fixture text, external-material validators/projections, and candidate rendering.
These are mechanisms/materializations for acquisition and inspection, not a
materialization derived from grammar competency standing. Version is Git source
plus `EXPECTED_SHA256`; dependencies and scope are campaign-local. Invalidation
follows hash/source/schema/code changes or violated bindings. There is no
checkpointed learned competency and no selector.

**Invocation.** Tests or direct campaign callers invoke `campaign_record()` and
related functions. Authority is bounded, supervised, read-only campaign
authority. Results are returned and test-observed, not ledger-recorded. They
cannot revise standing.

### 4.4 Specimen 4 — operational competency involving Bash

**Bounded subject/transformation.** The most faithful current Bash specimen is
not a Bash executor. It is the candidate **execute an external command grammar
through Bash/shell**. Current production searches find no Seed-owned shell/tool
execution owner; observation sources repeatedly disclaim shell/subprocess
execution. `ToolSpec` can describe an implementation and schemas, but operation
contract metadata is not standing or callability
(`seed_runtime/models.py:84-101`; `seed_runtime/capability_inventory.py:188-200`).

**Standing.** `/bin/bash` existence, a declared user shell, executable PATH
metadata, developer use of shell in tests, or this agent's terminal access is
not a projected Bash competency. No `capability_verified` Bash subject was
found. Classification: **operational mechanism externally available; Seed
competency standing absent**. Producer/provenance/applicability/version for a
general Bash competency are Unknown. Tests do not promote it.

**Preservation/projection.** User-shell observations can be ingested as ordinary
facts, but they state a user's declared shell, not execution competency.
Executable-file inspection similarly stops at verification evidence and never
runs the binary or promotes it (`seed_runtime/verification_evidence.py:69-117`).
No Bash materialization projection exists.

**Materialization.** A host Bash binary is an externally supplied mechanism and
possible realization. Exact binary version, grammar/dialect, dependencies,
authority, verification history, and invalidation are not represented in
competency State. It could participate in many transformations; any one
transformation could potentially use Bash or a direct API. Those cardinalities
are mechanically possible, but no current first-class mapping or selector
represents them.

**Invocation.** There is no current Seed runtime consumer that selects,
authorizes, invokes, observes, and records Bash results. Manual operator/agent
terminal execution is outside the recovered Seed road. Thus available mechanism
!= selected realization != authorized Seed invocation != verified result.

### 4.5 Specimen 5 — ordinary evidence-backed projected `web_search` capability

**Bounded subject/transformation.** The exact standing specimen demonstrated by
current tests is subject `web_search`, predicate `capability_verified`, value
`verified`: the bounded claimed transformation is public-web search as named by
the subject. The evidence fixture is a provider report and the projected Fact
links it. The test proves inventory state, fact id, evidence id, and age
(`tests/test_capability_inventory.py:39-81`).

**Standing.** Within that projected test ledger, standing exists and is current,
evidence-backed, provider-provenanced, and scoped to workspace `ws`. It is not a
claim that the repository's live/default ledger currently contains that Fact.
The producer in the specimen directly appends evidence and Fact events; no
implemented adjudicator establishes constitutional sufficiency. Applicability,
provider report semantics, conflicts, and transformation bounds beyond the
string are not expressed. Expiry can make it stale; multiple Fact supports can
conflict. Known loss is the compression of competency semantics to
subject/predicate/value plus generic provenance.

**Preservation/projection.** Event Ledger preserves the evidence report and
verification Fact separately; State projects both and FactSupport; inventory
reopens them. Projection is performed at read time, not at each web-search
invocation. New evidence alone does not alter standing; a new relevant Fact
does. There is still no responsible production admission/revision owner.

**Materialization.** `capability_catalog/web_search.yml` lists Tavily and Brave
recommendations, but catalog recommendations require explicit integration and
registration and are metadata, not selected/available implementations. No
materialization is derived from the standing Fact. Version, dependencies,
verification history, invalidation, and standing-to-realization relation remain
unrepresented.

**Invocation.** No current runtime consumer connects this standing to provider
choice, policy/approval, operation grammar, invocation, result observation, or
ledger return. The specimen's exact road stops after inventory presentation.

## 5. Crossing-by-crossing falsification

| Candidate crossing | Current result | Controlling witness |
|---|---|---|
| constitutive evidence/occurrences -> ledger | **Conditional, implemented generically** | Observation ingestion records observation/evidence/Fact only when invoked; probes/campaigns do not invoke it. |
| ledger evidence -> competency standing | **Unsupported: first missing crossing** | Only `capability_verified` Fact marks admission; readiness explicitly creates none. |
| ledger -> current standing projection | **Implemented if standing Fact already exists** | State replay + FactSupport + capability inventory. |
| projection -> reopen evidence | **Implemented, bounded/lossy** | Inventory follows supporting Fact ids into evidence summaries; only producer-preserved dimensions survive. |
| standing -> available materializations | **Unsupported** | No standing-to-artifact/ToolSpec/provider relation. |
| evidence-replayed vs compiled materialization | **Not represented as alternatives** | Evidence roads recompute views; compiled probes exist independently. |
| materializations -> constraint-relative selection | **Unsupported** | No materialization set, lawful selector, or resource policy. |
| selection -> authorization | **Unsupported** | Capability verification expressly is not execution authority. |
| authorization -> invocation | **Absent in recovered runtime** | No Seed-owned general tool/Bash execution corridor. |
| invocation -> result observation -> ledger | **Generic recording is available, no joined invocation producer** | Caller may construct Observation; no execution result router. |
| new evidence -> standing revision | **Unsupported as competency responsibility** | Generic Facts may alter projection; no competency adjudicator owns revision. |

The candidate topology is therefore false as a current end-to-end road. The
exact road that already exists is:

```text
caller-supplied Observation
-> ObservationIngestor
-> observation/evidence/(optional) Fact events
-> Event Ledger
-> StateProjector replay/finalization
-> Evidence + Fact + FactSupport
-> capability inventory when predicate == capability_verified
-> read-only standing presentation with evidence links
```

Separately:

```text
caller files/text/manifest
-> independently developer-compiled probe/campaign function
-> transient result
-> human/test consumer
```

and:

```text
package_installed Fact + evidence
-> evidence-derived capability candidate
-> PATH executable-file observation
-> promotion-readiness inspection
-> STOP (no capability_verified Fact)
```

The candidate builder explicitly says observed package evidence is candidate
support, not proof/permission/selection/execution
(`seed_runtime/capability_candidates.py:81-115`).

## 6. Evidence-born versus compiled adjudication

| Candidate classification | Adjudication |
|---|---|
| **A. Two independent competency origins** | **Not generally established.** Evidence-backed `capability_verified` standing is one current standing form. Compilation is not a second standing origin. A developer could directly append a claimed Fact, but compilation would still not be its warrant. |
| **B. One competency standing with two materialization strategies** | **Not implemented.** Plausible cardinality, absent representation and selector. No specimen links one standing subject to replayed and compiled forms. |
| **C. Compiled materialization admitted from external evidence** | **Absent.** Campaign evidence never admits probe code; no derivation/admission record binds external evidence to a compiled artifact. |
| **D. Evidence-born standing later compiled/checkpointed** | **Absent.** No compilation/checkpoint event, artifact contract, authority, provenance, verification, or invalidation road exists. |
| **E. Developer-compiled behavior with no competency standing** | **Current and demonstrated.** Structure and Documentation probes, campaign helpers, and most local observers fit. |
| **F. No general relationship currently established** | **Current universal finding.** Evidence-backed standing and compiled behavior coexist as independent islands. Relationships are specimen-relative and must be proven, never inferred from labels. |

Thus “evidence-born versus compiled” is specimen-relative only at the level of
evidence/behavior provenance. It is **not currently two lawful origins of
competency standing**, and it is **not currently two registered
materializations of one standing**.

## 7. Resource comparison and constrained-hardware scenario

Current grammar can measure some bounded operations independently:

* ledger/storage footprint from database/file sizes;
* State projection rebuild timing and counters through optional non-authoritative
  `ProjectionBuildDiagnostics` (`seed_runtime/state.py:149-218`);
* campaign request count, byte count, and elapsed behavior;
* external timing/RSS/CPU/load/latency measurements around a concrete invocation;
* dependency footprint and hashes from attributed inspection;
* reopenability, represented loss, currentness, and invalidation cost only when a
  producer declares a bounded comparison convention and retains source evidence.

These can be **measurements** or **candidate-selection evidence**. They are not
thresholds, sufficiency, authority, or optimization policy. Current grammar has
no compilation-time/materialization identity schema, active-RAM contract,
candidate set joined to standing, or selector that can consume them.

For the bounded scenario—constrained hardware, several required competencies,
and evidence-replayed plus compiled candidates—lawful selection would first
require all of the following, none inferred as an implementation recommendation:

1. a responsible producer establishing each exact competency standing;
2. attributed materialization producers binding candidates to that standing,
   with version, grammar, dependencies, applicability, verification, loss, and
   invalidation evidence;
3. a consumer that actually requires the bounded transformation under stated
   hardware constraints;
4. authority to admit the candidates and to use declared resource measurements
   for that consumer purpose;
5. a lawful selection occurrence preserving considered candidates, measurements,
   conflicts, Unknowns, reason, and non-selection;
6. separate invocation authorization and result verification.

Until those antecedents exist, resource measurements may inform inquiry but
cannot lawfully select or authorize a materialization. Resource efficiency is
not constitutional sufficiency.

## 8. Compilation, checkpointing, invalidation, and cardinality

No current competency contract grants compilation or checkpoint authority.
Developer repository authority can produce code; operator authority can run a
bounded command; neither makes the resulting artifact an admitted competency
materialization. A lawful compilation/checkpoint would require an established
standing subject, a responsible producer occurrence, explicit authority/scope,
a derivation record linking constitutive evidence and standing to artifact
identity/version, declared representational loss, verification, and a consumer.

No competency-aware invalidation owner exists. For today's compiled behaviors,
ordinary engineering invalidators include source revision, dependency/runtime
change, input grammar/version change, violated fixture/hash, failing verification,
changed applicability, expired standing evidence, or conflicting evidence. The
repository does not project those as a materialization's validity state.

Conceptually, one competency may have several realizations and one realization
may support several competencies. Current code already supplies weak structural
counterevidence to a one-to-one assumption: many helper functions cooperate in
one probe transformation, while `documentation_structure.py` supports many
bounded outputs. But Seed has no first-class competency-to-realization relation,
so neither cardinality has current standing and nobody selects among them.

## 9. Structure and Documentation probe scaffold disposition

Both probes are **mixed scaffolding**:

* bootstrap measurement instruments where they expose exact read-only
  observations and negative-authority boundaries;
* developer-compiled candidate materializations where Python embodies a bounded
  transformation;
* destination witnesses where downstream consumers demonstrate useful shapes;
* not permanent constitutional owners, because imports/tests/current consumers
  do not establish that standing.

Eventual deletion is warranted only by exact replacement evidence, not by the
label “evidence-born” and not by compatibility preservation alone. For each
currently required bounded transformation, the replacement evidence must show:

1. the same or intentionally changed consumer requirement and authority;
2. established, current, applicable competency standing reopenable to
   constitutive evidence, including conflicts/Unknowns and known loss;
3. an attributed replacement materialization derived from or lawfully admitted
   against that standing, with exact version/grammar/dependencies/scope;
4. verification against positive, negative, ambiguous, boundary, and
   consumer-relevant specimens, including comparison with current probe output;
5. explicit disposition of every current consumer and output distinction;
6. valid invocation/authorization/result-observation behavior under the required
   constraints;
7. invalidation/currentness handling and evidence that no unique constitutional
   measurement or refusal boundary is lost;
8. evidence that removal, rather than coexistence, is selected by the responsible
   owner for the bounded consumer purpose.

For Documentation Probe specifically, replacement must warrant fence locality,
one-to-six marker bounds, delimiter treatment, text normalization, line
coordinates, H1-to-title strengthening, section hierarchy, skipped levels,
duplicates, recurrence, links, code blocks, and all negative-authority behavior—or
explicitly show which are no longer required. For Structure Probe, it must
preserve or intentionally supersede hash/encoding/text/coordinate binding,
declared measurement conventions, reopenability, refusal, and caller-supplied
provenance. Evidence-born replacements merely existing is insufficient.

## 10. Required direct answers

1. **What competency evidence is actually preserved in the Event Ledger today?**
   Generic recorded observations, Evidence payloads, and Facts can preserve
   competency-relevant testimony and `capability_verified` support. There is no
   dedicated competency/materialization/invocation event, and current probes and
   campaigns do not automatically record their output.
2. **What current projection represents active competency knowledge?** The
   capability inventory derived from projected `capability_verified` Facts and
   FactSupport. `ToolSpec` labels appear as separate unverified operation metadata.
3. **Can projected competency standing be reopened to constitutive evidence?**
   Yes, when Facts carry evidence ids: inventory follows FactSupport to Facts and
   Evidence summaries. Only preserved dimensions reopen; constitutional
   sufficiency and omitted applicability/loss do not reappear.
4. **Is competency knowledge recomputed on every invocation?** No general
   competency invocation exists. State/FactSupport/inventory is recomputed on
   projection/read construction; compiled probes recompute their own result per
   call independently of competency State.
5. **Does any current compiled artifact derive from established competency
   standing?** No such derivation link or producer was found.
6. **Does compiled behavior currently gain standing anywhere merely from
   existence or tests?** No. Operation contracts remain metadata; tests are
   demonstration/counterevidence, not admission.
7. **Are evidence-born and compiled two origins, two materializations, or
   specimen-relative?** Specimen-relative evidence/behavior provenance with no
   general current relationship. Compilation is not a standing origin; two
   strategies for one standing are not implemented.
8. **Can one competency have several realizations?** Mechanically possible, not
   currently represented or established.
9. **Can one realization support several competencies?** Mechanically visible in
   multi-purpose modules/mechanisms, not currently represented as standing.
10. **Who selects among materializations?** Nobody in the current competency
    road. CLI option selection and catalog recommendation ranking are not that act.
11. **Can resource measurements lawfully affect selection?** Only as attributed
    candidate-selection evidence after standing, candidate binding, consumer
    requirement, authority, constraints, and a responsible selector exist. They
    cannot do so today.
12. **What authority permits compilation or checkpointing?** No competency-aware
    authority is implemented. Developer build authority is not competency
    admission; lawful checkpointing authority is Unknown.
13. **What invalidates a compiled materialization?** No projected rule owns it.
    Source/dependency/grammar/applicability changes, expired/conflicting evidence,
    violated hashes, and failed verification are candidate invalidation evidence.
14. **How does new invocation evidence return to the ledger?** It does not via a
    joined current road. A caller can separately construct and ingest an
    Observation, producing observation/evidence/Fact events.
15. **Who may revise current competency standing?** No responsible competency
    revision owner was found. A producer able to append `capability_verified`
    Facts can mechanically alter projection, but mechanical write access is not
    recovered constitutional authority.
16. **What exact current road already exists?** Observation -> ingestion ->
    observation/evidence/Fact events -> ledger -> State replay/finalization ->
    FactSupport/evidence graph -> inventory, conditional on an already-produced
    `capability_verified` Fact. Compiled probes form a separate direct-call road.
17. **What is the first missing crossing?** Evidence/candidate/readiness ->
    responsible `capability_verified` standing admission.
18. **What responsibility owns that crossing, or is ownership Unknown?** Unknown.
    Inventory disclaims admission; readiness disclaims promotion; generic
    Observation ingestion lacks sufficiency adjudication.
19. **What standing do Structure and Documentation probes actually possess?**
    Current developer-compiled, test-demonstrated, directly invocable behaviors
    and mixed scaffolding; no recovered competency standing.
20. **What exact replacement evidence would warrant deleting them?** The
    eight-part consumer/standing/provenance/materialization/verification/
    invocation/invalidation/removal-selection packet in section 9, applied to
    every bounded distinction each probe currently supplies.

## 11. Final adjudication and stop

The strongest warranted conclusion is **E + F** today: developer-compiled
behavior without competency standing exists, and no general evidence-born to
compiled relationship is established. The evidence-backed projected-standing
island also exists when callers have already recorded a `capability_verified`
Fact, but its admission producer is missing. A, B, C, and D are not current
general roads.

Accordingly the proposed topology stops at its first unsupported crossing:

```text
constitutive evidence and occurrences
-> Event Ledger preservation                         [conditional, generic]
-> responsible competency-standing admission         [UNSUPPORTED — STOP]
```

No compiler, cache, registry, optimizer, selector, recompilation, evidence
router, promotion gate, sufficiency stage, representation recovery, or handoff
plumbing follows from this report. No implementation recommendation is made;
the current active road independently warrants only the bounded inventory and
evidence-reopenability characterization above.
