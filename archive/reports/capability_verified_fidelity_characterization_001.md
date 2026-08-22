# `capability_verified` Fidelity Characterization 001

## 1. Scope, authority, and answer in brief

This is one bounded, report-only characterization of the current merged
`main` immediately after PR 2009 (`4020232`). It changes no implementation,
test, fixture, schema, export, interface, event, persistence, projection,
canonical Book chapter, root documentation, `docs/` content, campaign, or prior
report. Current implementation, executable tests, the Event Ledger and State
projection, and the active Book control. Git history and earlier reports are
orientation and counterevidence only.

The exact current finding is:

> `capability_verified` does not identify a verification act. It is a
> caller-attributed, single-cardinality Fact-shaped status assertion about a
> capability-named subject. Generic observation ingestion can mechanically
> turn that assertion into Evidence and a Fact, and generic ledger callers can
> append the Fact directly. No predicate-specific production owner, bounded
> behavioral verifier, constitutional competency admission rule, or current
> reachability check exists. Read-only consumers then present supported values
> as `verified`, `provider_reported`, `unverified`, `stale`, or `unknown` and,
> more strongly, call Fact subjects “admitted capability knowledge.”

Thus the predicate is a **mixed/compressed object**. Per provenance it can be a
faithful attributed verification claim, mechanically promoted provider or user
testimony, an inventory status marker, a developer-compiled fixture, or an
unsupported direct Fact. In the only concrete `web_search` specimen, it is
provider testimony presented as verified, not evidence-backed constitutional
competency standing. There is no active operational prerequisite downstream.

This report does not assume that every stored instance is false. It finds that
the predicate and its consumers do not carry enough dimensions to establish
whether an instance is true in the stronger constitutional sense.

## 2. Controlling distinctions

The following distinctions control every conclusion:

| Distinction | Current implementation result |
|---|---|
| predicate name vs. producer occurrence | A catalog entry and consumer constant exist; neither proves a verifier ran. |
| Fact vs. truth | State projects the supplied Fact; it does not independently adjudicate its value. |
| Fact support vs. constitutional sufficiency | `FactSupport` aggregates current Fact provenance, confidence, sources, and expiry; it has no competency admission test. |
| provider assertion vs. Seed verification | `source_type="provider"` is preserved and can yield either `verified` or `provider_reported`; no provider assertion is executed or checked. |
| passing test vs. runtime standing | Tests manufacture Facts and verify projection behavior. They do not establish live runtime competencies. |
| `ToolSpec` label vs. Capability | Tool labels widen the inventory universe but are explicitly not admitted knowledge or evidence of presence, availability, authorization, or callability. |
| mechanism present vs. transformation reachable | A binary path or compiled function is a mechanism observation; neither is bound to standing or a reachable invocation road. |
| verified once vs. currently reachable | expiry can make a Fact stale, but an unexpired Fact is not rechecked against current mechanism/dependencies. |
| compiled behavior vs. evidence-born competency | Structure and Documentation behavior runs directly from compiled code without this predicate. |
| inventory presentation vs. standing establishment | inventory reads Facts and labels them; it does not perform admission. |

The repository's predicate definition supplies only durable-fact kind, enum
values (`verified`, `provider_reported`, `unverified`), and single cardinality
(`predicate_catalog/core.json:99-110`). It supplies no verification grammar,
method, bounded input/output transformation, applicability, constraint,
authority, mechanism, dependency, refresh rule, or constitutional sufficiency
rule.

## 3. What exact act is claimed?

### 3.1 The narrow claim that is actually representable

A Fact with subject `C`, predicate `capability_verified`, and value `V` claims
only that its attributed source asserted status `V` for the string `C` at the
Fact's observation time. If it came through `ObservationIngestor`, the more
precise occurrence is:

1. a caller supplied an `Observation` with subject, predicate, value,
   `source_type`, time, confidence, metadata/dimensions, and optional expiry;
2. ingestion copied that observation into provenance Evidence; and
3. ingestion mechanically copied subject/predicate/value and evidence identity
   into an observed Fact (`seed_runtime/observations.py:81-228`).

The word `verified` is therefore part of the asserted vocabulary, not evidence
that Seed performed verification. For a direct `fact.observed` append, even the
Observation occurrence is absent.

### 3.2 What the claim does not contain

The Fact does not identify:

* a bounded transformation, input grammar, output grammar, or success oracle;
* invocation arguments, result, expected result, or demonstrated behavior;
* provider/version/environment, target, applicability domain, or scope beyond
  a free-form subject string and optional generic dimensions;
* tool/materialization identity, binding, dependencies, or their current state;
* verifier identity distinct from generic source/actor attribution;
* authority to admit a constitutional Capability or competency;
* authorization, policy approval, selection, invocation, or successful use;
* re-verification cadence. Optional generic expiry can age the assertion, but
  no producer-specific expiry requirement exists.

Accordingly `capability_verified` compresses at least **attributed capability
claim**, **verification-shaped status**, **inventory membership**, and, in
consumer vocabulary, **admitted capability knowledge**. It does not encode
demonstrated bounded behavior, current mechanism reachability, constitutional
Capability standing, competency standing, compiled realization availability,
authorization, or successful invocation.

## 4. Producer audit

### 4.1 Production code: no predicate-specific producer

Repository-wide implementation search finds no production branch that creates
an Observation, Evidence, or Fact with this predicate. The literal appears in
the catalog, consumers, boundary text, and a CLI help/error string, not in a
verifier. Package observation explicitly avoids capability inference, and the
read-only evidence/readiness road explicitly stops before Fact creation
(`seed_runtime/verification_evidence.py:69-103`;
`seed_runtime/capability_promotion_readiness.py:79-166`;
`tests/test_local_packages.py:145-166`).

Therefore there is **no real current runtime producer occurrence** to list. No
production caller owns a verification act, required constitutive evidence,
transformation identity, scope, grammar, mechanism/dependency check, authority,
conflict handling, loss declaration, or recording cadence for this predicate.

### 4.2 Generic CLI/API construction paths

These are active generic construction paths, not predicate-specific producer
occurrences:

| Path | Exact caller and source type | Construction and recording | Verification act/evidence |
|---|---|---|---|
| `seed --observe C capability_verified V` | `parse_observation()` -> `ingest_observations()` -> `ObservationIngestor.ingest_many()`; CLI-selected `discovery`, `provider`, `imported`, or legacy `user` | Constructs Observation; ingestor constructs Evidence and Fact; appends `observation.observed`, `evidence.observed`, `fact.observed` | None. The caller's value is mechanically promoted. |
| `seed --fact C capability_verified V` | `parse_dev_fact()` -> `seed_dev_facts()` -> same ingestion; fixed `user` | Compatibility shorthand records the same three events | None. It is developer/user shorthand. |
| `--observe-json` and generic observation collection | JSON/provider adapter -> normalization -> collection service -> `ObservationIngestor` | Can record the same triple if a caller supplies this canonical predicate | No currently identified adapter emits it on its own. Constructibility is not occurrence. |
| Python `ObservationIngestor` API | Any generic caller with an Observation | Same mechanical Evidence/Fact conversion and ledger append | None imposed by the API. |
| generic `EventLedger.append("fact.observed", ...)` | Any caller | Direct Fact event, possibly with caller-listed `evidence_ids`; no Observation required | None imposed by the ledger. |
| state-patch/generic event ingress | Authorized generic caller supplying a Fact-shaped patch/event | Preserves a supplied Fact-shaped record | No predicate-specific verification. |

The CLI path is visible in `scripts/seed_local.py:512-612,1380-1514,2418-2469`.
The predicate catalog can reject a non-enum value during normalized observation
intake, but enum validation is grammar of the status label, not verification of
the capability (`seed_runtime/predicate_catalog.py:78-115`). Direct generic
Fact-event construction need not pass that normalization boundary.

For all generic paths:

* **scope/applicability:** only caller-provided subject and generic dimensions;
* **currentness/expiry:** caller-provided times and optional expiry; no required
  TTL or refresh;
* **authority:** generic actor/source attribution, not a competency authority;
* **conflicts:** generic State support/conflict semantics only;
* **known loss:** no typed method, transformation, grammar, applicability,
  dependencies, mechanism, result, or verifier authority survives;
* **recording occurrence:** only when a caller actually invokes the path. Code
  availability alone is not evidence that this has happened in a deployment.

### 4.3 Tests and fixtures

Tests are the only concrete constructors found in the current tree:

* `tests/test_capability_inventory.py` builds provider-source Facts and a
  `capability.verification.report` Evidence whose payload is merely the
  capability name. The `web_search` test appends both directly and expects an
  inventory state of `verified` (`tests/test_capability_inventory.py:43-74,94-108`).
* `tests/test_single_capability_state_projection.py` builds provider-source
  `python_runtime` Facts and expects the composed projection to say `verified`
  even with no registered operation and no acquired verification evidence
  (`tests/test_single_capability_state_projection.py:27-67`).
* `tests/test_capability_verification_inspection.py` similarly constructs
  verification Facts to test the join and its boundary language.
* integrity-summary tests manufacture inventory Facts to count presentation
  states; they do not verify competencies.

These are compatibility/projection fixtures. Their asserted facts are not live
producer occurrences and their passing tests establish only consumer behavior.

### 4.4 Campaigns, APIs, catalogs, history, and reports

No current campaign contains the predicate. No capability catalog entry creates
it: catalog recommendations remain advisory and separate from Facts. Public
Python APIs expose generic ingestion and read-only builders, not a dedicated
verification admission API. Historical reports sometimes call the Fact
“admitted” or “verification-produced”; those descriptions are not producers.

## 5. Event Ledger and State consumer road

### 5.1 Event Ledger: assertion preservation

For generic Observation ingestion the ledger preserves three distinct records:
the supplied Observation, mechanically derived Evidence, and mechanically
derived Fact. Evidence preserves attribution and the supplied claim payload;
the Fact links its evidence ID. The ledger does not add a verifier occurrence
or prove the claim (`seed_runtime/observations.py:99-228`). A direct
`fact.observed` append preserves still less.

**Direct answer:** the Event Ledger preserves a **verification-shaped
assertion occurrence**, not necessarily a verification occurrence. It could
preserve evidence of a real verification only if an external caller supplied
adequate evidence, but the predicate contract neither requires nor identifies
that evidence.

### 5.2 StateProjector, current facts, and `FactSupport`

`StateProjector` decodes generic observation/evidence/fact events and rebuilds
generic support, current-fact, expiry, conflict, evidence-relation, and derived
indexes (`seed_runtime/state.py:905-1181`). It has no predicate-specific
verification decoder or competency admission transition.

State adds:

* replayed in-memory objects and identity lookup;
* generic single-cardinality support grouping/selection;
* confidence/source/time aggregation;
* current vs. expired selection and stale-fact visibility;
* generic conflicts and evidence navigation.

It adds no bounded verification, truth adjudication, Capability identity,
competency sufficiency, materialization binding, mechanism reachability,
authorization, selection, or invocation.

### 5.3 Capability inventory: the strengthening point

Inventory is the only predicate-specific semantic consumer. It:

1. adds every matching Fact subject to an `_AdmittedCapabilityState`;
2. unions those subjects with separately sourced `ToolSpec.capabilities` labels;
3. selects active `FactSupport` for the subject/predicate;
4. renames enum values into inventory states (`verified`,
   `provider_reported`, `unverified`, or `unknown`), or calls expired support
   `stale`; and
5. renders facts, Evidence summaries, confidence, source types, timestamps,
   age, expiry, and a reason (`seed_runtime/capability_inventory.py:19-281`).

The preserved parts are provenance, support IDs, evidence summaries, status
value, confidence, and generic freshness. The strengthening is explicit:
matching subjects are called **“admitted capability knowledge”**, and a value
`verified` is presented as **verified capability state**. This is competency-
standing-like vocabulary, but no constitutive competency rule is run. Inventory
therefore presents Fact standing as capability/verification standing; it does
not establish constitutional Capability or competency standing.

Notably, `_observed_verification_capability_subjects()` scans all `state.facts`,
including expired Facts, so an expired Fact keeps the subject in the inventory
and produces `stale`. A negative `unverified` Fact also admits the subject to
the universe while yielding negative status.

### 5.4 Later read-only consumers

| Consumer | Exact input | Rename/strengthening | Operational reliance |
|---|---|---|---|
| capability verification inspection | evidence-derived package candidates plus inventory | calls inventory state `verification_status`; preserves candidate and verification evidence separately | none; explicit no selection/permission/policy/invocation (`seed_runtime/capability_verification.py:90-185`) |
| single-capability state projection | normalized string correlation across catalog, ToolSpecs, candidate/evidence inspections, inventory | exposes inventory state as `verification_status` and support as `verification_support`; calls correlation only | none; explicitly read-only, no authorization or execution (`seed_runtime/single_capability_state_projection.py:19-143`) |
| projection integrity summary | inventory entries | counts `verified_capability_count`, provider-reported, unverified, stale, unknown | integrity presentation only (`seed_runtime/integrity_summary.py:24-117`) |
| capability status CLI | inventory | JSON status presentation | none |
| capability verification CLI | verification inspection | JSON verification presentation | none |
| single-capability-state CLI | composed projection | human/JSON standing presentation | none |
| generic fact/current/why/evidence/ledger CLIs | State/ledger Facts and evidence | generic fact/support vocabulary | inspection only |
| promotion-readiness CLI | candidates plus local PATH evidence | none from this predicate; it is an independent pre-admission road | none; never reads or creates this Fact |

No selection, policy, authorization, execution proposal, tool router, provider
call, successful invocation recorder, or cluster mutation path consumes the
predicate. `capability_verified_not_capability_selection`,
`...not_execution_authority`, `...not_execution_decision`, and
`...not_tool_invocation` are explicit boundary notes
(`seed_runtime/capability_promotion_readiness.py:22-39`).

## 6. Asymmetric specimens

### 6.1 `web_search`: PR 2009's inventory fixture

* **Observed:** nothing about web search behavior. The test directly appends an
  Evidence record and Fact; no search is invoked.
* **Asserted:** provider-source `web_search capability_verified verified`.
* **Verified:** only that inventory projection maps the manufactured Fact and
  evidence ID to state `verified` with the expected age.
* **Projected:** generic Evidence/Fact/FactSupport, then an inventory row named
  `web_search`, state `verified`.
* **Standing resulted:** test-local provider assertion with Fact support,
  strengthened by inventory into verified-capability presentation.
* **Lawful reliance:** that the provider-attributed assertion was preserved and
  remains current under generic expiry semantics. A consumer may not infer a
  bounded web-search competency, reachable provider, grammar, permission,
  successful search, or current callability.

**Finding:** `web_search` is provider testimony presented as verified, not
evidence-backed competency standing.

### 6.2 `ToolSpec` label without a verification Fact

The inventory test registers a ToolSpec labeled `web_search` in otherwise empty
State (`tests/test_capability_inventory.py:79-93`).

* **Observed:** a developer-registered executable operation contract exists in
  projected memory.
* **Asserted:** the ToolSpec declares the label `web_search`.
* **Verified:** no capability behavior.
* **Projected:** inventory includes `web_search` with state `unverified` and no
  supporting Facts.
* **Standing resulted:** operation-contract association and inventory
  membership, not admitted capability knowledge.
* **Lawful reliance:** only that the registered ToolSpec declares the label;
  not that it is available, callable, authorized, adequate, or reachable.

### 6.3 Package/executable evidence that stops before promotion

For `python_runtime`, package facts can derive a candidate and PATH inspection
can observe an executable file. Readiness becomes `supported` when both exist,
yet writes no event and creates no verification Fact
(`tests/test_capability_promotion_readiness.py:117-143`).

* **Observed:** package-derived candidate support and filesystem metadata that
  a named binary exists and is executable.
* **Asserted:** a candidate correlation and `binary_path_observed` support.
* **Verified:** file presence/execute bit only; the binary is not invoked.
* **Projected:** transient candidate, verification-evidence, and readiness
  records; no State Fact.
* **Standing resulted:** promotion readiness `supported`, not capability or
  competency standing.
* **Lawful reliance:** a future admission inquiry has these two support items;
  not that Python performs a bounded transformation or is invocable now.

This specimen proves that repository-named “verification evidence” is not
constitutive evidence for the current predicate because no implemented rule
consumes it into the Fact.

### 6.4 Structure/Documentation compiled behavior without the predicate

Structure Observation is a developer-compiled, read-only boundary for
structural extraction and evidence preservation. It explicitly owns no grammar,
content interpretation, event writes, repository mutation, or cluster mutation
(`seed_runtime/structure_observation.py:1-55`). Documentation Structure executes
its compiled traversal/projection directly.

* **Observed:** bounded structural properties of supplied repository or
  documentation material.
* **Asserted:** typed, surface-specific structural output and boundaries.
* **Verified:** only what each compiled parser/test oracle checks.
* **Projected:** transient read-only probe/view output, not
  `capability_verified` State.
* **Standing resulted:** runnable compiled behavior with tested contracts; no
  constitutional competency standing.
* **Lawful reliance:** the documented direct-call behavior and output boundary,
  subject to inputs/tests; not generic Capability standing.

This disproves both “compiled behavior implies the predicate” and “the
predicate is required to invoke compiled behavior.”

### 6.5 Real runtime producer

None exists. The asymmetric absence is itself material:

* **Observed/asserted/verified/projected:** nothing until an external generic
  caller supplies a claim.
* **Standing resulted:** none.
* **Lawful reliance:** no deployment occurrence can be inferred from code
  constructibility.

## 7. Historical orientation

The reachable Git history first introduces the literal in commit `36fe0d0`
(PR 1908), a 2,173-file repository snapshot. In that same imported neighborhood
it appears as:

* a canonical durable Fact predicate;
* provider-source test Facts and provider-report Evidence;
* a capability inventory over provider/developer labels;
* ToolSpec capability-label correlation;
* read-only verification and promotion/readiness presentation; and
* tests of local/developer CLI and projection behavior.

`git log -S capability_verified` finds no earlier reachable commit and no later
implementation addition of a predicate-specific producer. Later commits only
adjust reports or ToolNeed/inventory ownership language through PR 2009. The
reachable history therefore ties the predicate to **provider capability
catalog/testimony, ToolSpec labels, inventory/readiness presentation, and
developer-compiled fixtures**, not to an implemented behavioral verification
admission. It does not prove the pre-snapshot motivation or a once-live
producer; that earlier provenance is **Unknown**.

Historical reports' stronger “admitted knowledge” formulation is
counterevidence: it demonstrates how the predicate was interpreted, not how its
sufficiency was earned. The active Book warns that a verified Fact is a scoped
claim, not universal truth, and requires method, scope, and time; its generic
statement that capability verification producers append facts does not identify
one in current code
(`book_of_seed/claim_normalization_and_fact_standing_recovery_001.md:33-64,172`).

## 8. Classification by provenance

| Provenance/specimen | Classification | Fidelity judgment |
|---|---|---|
| hypothetical external verifier supplying adequate attributed evidence | **faithful attributed verification claim** only | Possible, not enforced or found as an active producer; remains narrower than constitutional competency. |
| generic provider/user Observation | **mechanically promoted provider testimony**, **mixed/compressed object** | Fact creation is mechanical; adequacy is unconstrained. |
| direct Fact append | **inventory status marker**, **mixed/compressed object** | May lack even an Observation; evidence IDs can be absent or caller-selected. |
| `web_search` test | **compatibility fixture**, **developer-compiled capability declaration**, provider testimony presentation | Tests mapping, not search behavior. |
| inventory and later views | **inventory status marker** | Active presentation consumer, but no operational dependency. |
| current production producer | **Unknown/absent**, not an active operational prerequisite | No predicate-specific producer occurrence exists. |
| whole predicate | **mixed/compressed object** with **consumerless operational residue** | It has active read-only consumers, so not wholly consumerless or a pure historical relic. |

It is not correctly classified as an active operational prerequisite. It is
not wholly a historical relic because current CLI/diagnostic-like presentations
actively consume it. “Developer-compiled capability declaration” applies to
fixtures/neighborhood, not necessarily every externally supplied Fact.

## 9. Deletion topology (characterization only)

This section describes deletion, but does not recommend or perform it.

### 9.1 Exact surfaces that would disappear or change

| Surface | Exact deletion effect | Loss category |
|---|---|---|
| predicate catalog | remove enum definition and single-cardinality canonical predicate | presentation/validation behavior lost; no verified act lost |
| inventory constant/value maps | remove `CAPABILITY_VERIFIED_PREDICATE` and status decoding basis | replacement required only if inventory status is intentionally retained |
| admitted-state producer branch | remove scan of Fact subjects matching predicate | false/unsupported standing removed; Fact-only capability names disappear from inventory |
| State generic facts/support/indexes | no predicate-specific State field exists; existing matching Facts would no longer arise through catalog-normalized intake, while generic historical events remain generically projectable unless separately excluded | generic historical records/queries may remain; predicate-specific selected support ceases to feed inventory |
| inventory universe | becomes ToolSpec labels only under present code; Fact-only entries vanish; all remaining contract-label entries become `unverified` because no matching support can exist | truthful distinction between contract label and asserted verification remains important; verified/provider/stale presentation lost |
| inventory status output | `verified`, `provider_reported`, and `stale` rows sourced by these Facts disappear; `unknown` from unusual direct Fact values disappears; ToolSpec-only `unverified` rows remain | presentation behavior lost |
| verification inspection | candidates formerly joined to inventory Facts become `unverified`; supporting verification Fact/Evidence summaries disappear | presentation behavior lost; no bounded behavior lost |
| single-capability projection | verification status/support/freshness formerly sourced from Facts becomes `unverified` when a ToolSpec inventory row remains, otherwise `unknown`/missing-entry | presentation behavior lost |
| integrity summary | verified/provider-reported/stale/unknown counts attributable to predicate fall to zero; contract-label unverified counts remain | diagnostic count behavior lost |
| CLI `--capability-status` | still structurally runnable if inventory remains, but no Fact-backed statuses/Fact-only names | CLI output changes |
| CLI `--capability-verification` | still runnable; candidates lack Fact-backed verification status/support | CLI output changes |
| CLI `--single-capability-state` | still runnable; loses Fact-backed verification status/support/freshness | CLI output changes |
| generic `--observe`, `--fact`, JSON/API intake | canonical intake of this predicate is rejected/unknown depending on the exact generic boundary; generic arbitrary Fact construction remains unless separately constrained | compatibility behavior lost; no truthful verifier lost |
| capability catalog | no entry or recommendation is deleted; normalized-string/advisory correlation remains | no catalog behavior necessarily lost |
| readiness/evidence | unchanged: package candidates, PATH evidence, and supported/unsupported readiness never depend on the predicate | no replacement warranted for these surfaces |
| downstream selection/auth/invocation | no change | no operational consumer exists |
| tests/fixtures | capability inventory, verification inspection, single-state, integrity, local package negative assertions, and associated CLI expectations mentioning the predicate require deletion or revised expectations | test-only/compatibility behavior lost |
| Book | active references become historically descriptive or inaccurate relative to runtime; user forbids Book editing in this inquiry | reference impact only; no edit here |
| prior reports | remain historical records and leads | no edit and no runtime effect |

No dedicated Event Ledger schema, State field, projection event kind, persistence
table, authorization interface, provider invocation interface, or cluster
mutation would be removed. The event ledger and State are generic; deletion is
principally catalog admission, inventory interpretation, presentation, and
fixtures.

### 9.2 Truthful behavior versus false standing

Potentially truthful information lost is narrow: **an attributed source claimed
a named capability had a status at a time, with generic confidence/evidence IDs
and optional expiry**. That distinction should survive eventual removal only if
real current data or a real producer demonstrates that it is used. It must not
silently retain the stronger name “verified capability.”

False or unwarranted standing removed would be inventory's inference from any
matching Fact to “admitted capability knowledge” and its presentation of a bare
`verified` value as verified capability state without method, bounded behavior,
scope, grammar, applicability, mechanism, dependencies, or authority.

Deletion would expose a pre-existing missing projection: there is no
constitutional competency-standing admission from the repository's candidate
plus executable-path evidence, nor from bounded behavioral occurrences. That
gap exists today; deletion would reveal it rather than create it. The compiled
Structure/Documentation road would remain runnable and still lack competency
standing.

## 10. Required direct answers

1. **Who actively produces it?** No predicate-specific runtime producer. Tests
   directly construct it. Generic CLI/API observation ingestion and generic
   Fact-event append paths can record caller-supplied instances, but
   constructibility is not an observed producer occurrence.
2. **Does any producer perform a bounded verification act?** No.
3. **What constitutive evidence is required?** None predicate-specific. An
   Observation ingestion creates generic Evidence mechanically; a direct Fact
   may merely list evidence IDs or none. The catalog constrains only enum value.
4. **Can generic Observation ingestion create the Fact mechanically?** Yes.
5. **What does the ledger preserve?** A verification-shaped assertion
   occurrence, and, on the Observation path, its attribution—not proof that a
   verification occurred.
6. **What does State add?** Generic replay, support/currentness, confidence,
   expiry, conflict, and evidence indexes; no verification or competency
   sufficiency.
7. **Does inventory strengthen it into competency standing?** It strengthens
   it into “admitted capability knowledge” and verified-capability presentation.
   That resembles standing but is not constitutionally sufficient competency
   standing.
8. **Does an operational consumer require it?** No. All identified consumers
   are read-only inventory, projection, count, or CLI inspection surfaces.
9. **Does it identify a bounded transformation?** No.
10. **Does it preserve grammar, applicability, constraints, authority, and
    reachability?** No. It preserves only a small generic Fact envelope; even
    status grammar is just a three-value enum.
11. **Is `web_search` evidence-backed competency standing?** No. It is a
    provider-attributed fixture assertion presented as verified.
12. **Is it historically tied to compiled/developer declarations?** Yes in the
    reachable first neighborhood: provider fixtures, ToolSpec labels,
    inventory, readiness, and developer-local CLI. Pre-snapshot intent is
    Unknown.
13. **What truthful distinction should survive eventual removal?** Only the
    distinction between “an attributed source asserted a capability status” and
    “Seed demonstrated/admitted a competency,” if current data proves the former
    still matters.
14. **What exact runtime/test surface disappears?** Predicate catalog entry;
    inventory constant, Fact-subject admission scan and Fact-backed states;
    verification/single-capability support and freshness presentation;
    integrity counts; corresponding CLI output; and the predicate-manufacturing
    inventory, verification, projection, integrity, and negative package tests.
    Generic ledger/State machinery, catalogs, candidates, PATH evidence,
    readiness, selection, authorization, and invocation remain.
15. **Would deletion expose missing competency standing?** Yes. Candidate plus
    evidence stops at readiness and no bounded occurrence-to-admission
    projection exists.
16. **Is a replacement warranted now?** No. Current evidence does not establish
    an operational consumer or a sufficient producer contract to replace.
17. **Is implementation excision warranted now?** Exact current evidence
    independently warrants neither preservation as competency standing nor
    immediate excision. One smaller inquiry is required first: inspect actual
    current persisted ledgers/deployments (if any are authoritative and
    available) for instances, their provenance/evidence payloads, and read-only
    consumer use. If none exist, this report's topology leaves only
    presentation and fixture residue; if adequate externally produced instances
    exist, their truthful attributed-claim distinction must be characterized
    before excision. This is an evidence request, not a replacement design.

## 11. Stopping point

The predicate and deletion topology are characterized. This report does not
rename it, add a status predicate, create a competency producer, build a
reachability projection, bind a materialization, change schemas, add
compatibility plumbing, edit the Book, or delete code.
