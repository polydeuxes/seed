---
status: audit
scope: visibility, target, ownership, and operational concern reconciliation
created: 2026-06-17
---

# Visibility / Target / Ownership / Concern Reconciliation

## Status

Investigation only. No implementation changes were made to ownership, targets,
lenses, views, topology alerts, HomeOps surfaces, alias handling, current-facts
lookup, storage projection, availability projection, relationship projection, or
filesystem measurement handling.

Short answer: repository authority is currently closest to **visibility** and
**measurement/observation subject**, not to ownership. The inspected evidence
shows that Seed already preserves several boundaries:

```text
measurement subject
    !=
entity identity

alias
    !=
ownership transfer

endpoint visibility
    !=
host ownership
```

This audit finds that the operational example requires at least four separable
questions:

```text
what is visible?
what is the observation about or indexed by?
who owns or controls it, if anyone is known?
why should the operator care?
```

The repository does not currently have to answer the ownership question to
explain the operational concern. Visibility plus an expected topology or
expected observation pattern can be sufficient to explain why a filesystem
visibility loss matters.

## Audit question

Does the repository currently conflate:

```text
visibility

target / described entity

ownership

operational concern
```

and should these be treated as distinct concepts before introducing a new
ownership model?

## Prior findings reconciled

This audit treats the following documents as investigation inputs and does not
rediscover their established findings unless implementation evidence contradicts
them:

- `docs/filesystem_measurement_identity_boundary_audit.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/ownership_model_design_space_audit.md`
- `docs/lens_view_reconciliation.md`

The documents are mutually consistent with the inspected implementation:

1. Prometheus filesystem samples are attached to the Prometheus `instance`
   subject rather than silently re-owned to a stable host.
2. `prometheus_instance` preserves source-specific identity knowledge, but it is
   not an alias predicate and does not move endpoint facts to the host.
3. Alias resolution rejects endpoint/non-endpoint identity collapse.
4. Current facts and storage projections operate from the fact subject plus
   dimensions; they do not use a general `owner`, `target`, `described_entity`,
   or `measurement_owner` field.
5. Lens/view language is currently an architectural vocabulary over read-only
   projections, not a license to create new State authority or operational
   products.

No inspected repository evidence contradicts these findings.

## Repository evidence inspected

Implementation and tests inspected for this reconciliation included:

- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/observation_sources.py`
- `tests/test_observation_sources.py`
- `tests/test_predicate_normalizers.py`
- `tests/test_observation_normalizers.py`
- `tests/test_inference_catalog.py`
- `tests/test_seed_local_script.py`

Documentation inspected or reconciled included:

- `docs/filesystem_measurement_identity_boundary_audit.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/ownership_model_design_space_audit.md`
- `docs/lens_view_reconciliation.md`
- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/storage_measurement_current_fact_regression_audit.md`
- `docs/availability_vocabulary_audit.md`
- related lens/view, State Summary, and current implementation audits found by
  repository search where they intersected storage topology, current facts,
  availability, and read projections.

## Operational example analysis

Scenario:

```text
host115 exports storage
host116 observes storage
host116 loses visibility
ingestion becomes uneven
operator should be informed
```

Under current repository authority, this scenario cannot be reduced to
ownership.

### What the current repository can express directly

Current storage projection can express that a filesystem measurement row is
visible on a subject, grouped by canonical fact subject, mountpoint, and the
filesystem dimensions. It can also express multi-endpoint mount visibility and
shared-storage candidates derived only from observed filesystem fields. The
projection explicitly warns that these candidates are not facts, ownership
assertions, storage identities, relationships, or topology authority.

Therefore, the repository can represent parts of the scenario as:

```text
host116-or-endpoint subject had filesystem visibility for mount M
host116-or-endpoint subject no longer has current complete visibility for mount M
other endpoint(s) may still have visibility for M
this produces storage topology ambiguity or changed visibility pressure
```

### What the current repository does not express directly

The repository does not currently express:

```text
host115 owns the storage
host116 is an intended consumer of host115-owned storage
host116 must always mount that storage
loss of that mount is an alertable topology violation
uneven ingestion is causally caused by the storage visibility loss
```

Those may be true operationally in the real environment, but repository
authority does not currently encode them as ownership, target, expected topology,
or alert semantics.

### Concepts required to explain the scenario

The scenario requires these concepts to stay separate:

| Question | Concept | Why it is needed |
|---|---|---|
| Was the mount or endpoint seen before and is it seen now? | Visibility | The loss is about current observation changing. |
| Which subject carries the measurement? | Measurement subject / target index | Current projections and queries need an index such as endpoint or host subject. |
| What resource is the observation about? | Described entity / target candidate | A filesystem, mountpoint, device, service, or capability may be the thing described. Current repository authority only partially models this through predicate and dimensions. |
| Who controls or is responsible for it? | Ownership | This may be relevant later, but current evidence does not require it to detect visibility loss. |
| Why should an operator care? | Operational concern | Ingestion unevenness, missing mount visibility, and topology expectation changes matter even if owner is unknown. |

## Visibility analysis

Visibility asks:

```text
What can currently be seen?
```

Repository evidence strongly supports visibility as an existing concept family:

- Storage topology projection emits `visible_endpoint_count` and
  `visible_endpoints` for cluster mount groups and shared-storage candidates.
- Shared-storage candidates are derived only from matching observable filesystem
  measurement fields.
- Storage topology ambiguities are assembled from projected filesystem
  measurements, mount visibility groups, and shared-storage candidates, while
  explicitly avoiding ownership or topology truth.
- Availability summary separates endpoint scrape availability, host
  availability, and service availability so endpoint visibility is not reported
  as host or service availability.
- Endpoint-scoped predicates force exact lookup for `availability_status`,
  `health_status`, and `endpoint_role`, preserving endpoint visibility as its
  own scope.

### Required question 1: Can visibility exist without ownership?

Yes.

Repository examples:

1. `shared_storage_candidates` are derived from visible filesystem measurement
   fields and visible endpoints, while explicitly not being ownership
   assertions.
2. `cluster_mount_groups` answer where a mountpath is visible across endpoints;
   a code comment states the grouping must not be interpreted as shared storage
   identity or ownership.
3. Prometheus `up` becomes endpoint-scoped availability visibility, but tests
   and current-facts boundaries preserve that this does not make the host
   available or owned by the endpoint.
4. Local observation sources can record filesystem, network, users, and package
   visibility without inferring host availability.

Conclusion: visibility is already useful and intentionally narrower than
ownership.

## Target / described-entity analysis

Target or described entity asks:

```text
What is the observation about?
```

Current repository authority has a strong **subject** field, a strong predicate
and dimensions model, and weak/general absent target semantics.

For filesystem measurements, the current implemented target-like structure is:

```text
subject_id = endpoint or host-shaped measurement subject
predicate = filesystem_free_bytes / filesystem_total_bytes
dimensions = mountpoint, device, fstype, and related labels
```

This can describe a filesystem measurement row without deciding who owns that
filesystem. However, the repository does not provide a general field such as:

```text
observed_entity
described_entity
measurement_target
resource_target
owner_subject
```

The storage projection row field is named `host`, but prior audits already note
that under endpoint/host alias boundaries it may contain an endpoint-shaped
subject. That is a projection naming limitation, not ownership authority.

### Target versus ownership

For the operational example, the described entity could be:

- the mountpoint visible on host116;
- the filesystem mounted at that path;
- the backing device or export;
- the host116 ingestion capability that depends on the mount;
- the host115 export capability.

Current repository authority can only support some of these as observed
predicate/dimension shapes. It does not establish that the described entity and
owner are identical.

## Ownership analysis

Ownership asks:

```text
Who owns, controls, hosts, provides, or is responsible for something?
```

Repository evidence does not show that ownership is the single missing concept.
It shows that ownership-like questions are intentionally constrained:

- `Fact` and `FactSupport` carry subject and support information, not a separate
  owner.
- Alias predicates are limited, and `prometheus_instance` is excluded from alias
  predicates.
- Alias resolution rejects endpoint/non-endpoint identity collapse.
- Relationship projection suppresses Prometheus-derived `endpoint_role ->
  provides` and `prometheus_instance -> monitored_by` relationships where those
  would promote scrape visibility into broader topology claims.
- Existing relationship catalog semantics such as `runs_on`, `provides`, and
  `monitored_by` are specific relationships, not a universal ownership model.

Ownership may eventually be needed for some operator questions, such as
responsibility, remediation routing, or durable service topology. But the
example in this audit does not require ownership to explain that losing mount
visibility on host116 can matter.

## Operational-concern analysis

Operational concern asks:

```text
Why should an operator care?
```

Repository evidence already has concern-like but non-authoritative pressure
surfaces:

- `storage_topology_ambiguities` record reasons, candidate interpretations,
  observable evidence, and materiality, while explicitly avoiding facts,
  ownership, topology truth, issues, or operator clarification requests.
- Availability surfaces can identify down endpoints without making claims about
  host ownership.
- State Summary has scoped availability counts so endpoint scrape concerns are
  visible without being misrepresented as host or service availability.
- Current-facts and storage measurement regression audits frame some symptoms as
  visibility/query-shape issues rather than disappearance of facts.

### Required question 2: Can operational concern exist without ownership?

Yes.

Repository examples:

1. A down Prometheus endpoint is operationally relevant even when it is only
   endpoint scrape availability and not host availability.
2. A storage topology ambiguity can be material because a mountpath is visible
   on multiple endpoints or matches shared-storage candidate evidence, even
   though the projection refuses ownership assertions.
3. A missing or incomplete current filesystem measurement pair matters to a
   storage projection even if the storage owner is unknown.
4. Local observation deliberately avoids inferring availability, but the absence
   of availability is itself an operationally relevant unknown.

### Required question 3: Can filesystem visibility loss be important even if ownership is unknown?

Yes.

For the example, host116 losing visibility to a mount can matter because:

- ingestion behavior becomes uneven;
- an expected observed mount disappeared;
- a previously visible filesystem is no longer represented by complete current
  free/total measurement pairs;
- the topology pattern seen by storage projection changed;
- other endpoints may still see the mount, creating an asymmetry.

None of those statements requires knowing whether host115 owns the storage.
Ownership may help explain responsibility or remediation later, but it is not a
precondition for noticing the operational concern.

## Concept comparison

| Concept | Current repository strength | Existing evidence | Boundary risk if conflated |
|---|---:|---|---|
| Visibility | Strong | Visible endpoints, endpoint availability, observed filesystem fields, scoped summary counts | Conflating with ownership would turn observations into responsibility claims. |
| Target / described entity | Partial | Subject, predicate, dimensions, mountpoint/device/fstype | Conflating with ownership would make “about filesystem X” mean “owned by host Y.” |
| Ownership | Weak/general absent | Specific relationships exist; general measurement owner does not | Premature ownership would bypass alias and endpoint boundaries. |
| Operational concern | Emerging/projection-only | Ambiguity materiality, scoped availability, storage projection completeness | Conflating with ownership would require owner knowledge before warning about real symptoms. |

### Required question 6: Are ownership and operational concern separate concepts?

Yes. Repository evidence treats concern-like pressure as derivable from observed
visibility patterns and scoped measurements, while ownership is absent or
suppressed unless a specific relationship is justified. A mount disappearing
from host116 can be an operational concern even if the repository cannot say
whether host115 owns the storage.

### Required question 7: Which concept appears closest to current repository authority?

The closest concept is **visibility**, followed by **measurement subject** as the
implemented indexing mechanism. Target/described-entity is partially present via
predicate and dimensions. Ownership is the least supported as a general concept.
Operational concern exists only as bounded projection pressure, not as a formal
alert or HomeOps surface.

## Boundary preservation analysis

The repository currently preserves these boundaries:

```text
endpoint visibility
    !=
host ownership

measurement subject
    !=
described entity

alias evidence
    !=
ownership transfer

storage candidate
    !=
storage identity

ambiguity materiality
    !=
alert or topology truth

lens/view vocabulary
    !=
implemented product surface
```

The operational example stresses these boundaries because it is tempting to say:

```text
host115 owns storage; therefore host116 should mount it; therefore alert
```

But repository authority can currently support a narrower and safer chain:

```text
host116 or host116 endpoint had filesystem visibility
visibility disappeared or became incomplete
ingestion became uneven or topology pattern changed
operator concern exists
ownership remains unknown
```

This narrower chain explains the observed operational reality without violating
existing repository boundaries.

## Candidate future surfaces

This section names possible future surfaces only to preserve boundaries for later
investigation. It is not an implementation recommendation.

### Future Storage Lens

Required question 4:

A future Storage Lens, under current repository authority, would primarily answer:

```text
what storage/filesystem visibility exists?
where are filesystem measurements visible?
what mount/device/fstype patterns are ambiguous?
```

It would not primarily answer:

```text
who owns the storage?
```

unless a later architecture introduces explicit ownership or target authority.

### Future HomeOps View

Required question 5:

A future HomeOps View would not require ownership semantics to raise some useful
alerts or operator notices. Visibility plus topology expectation can be
sufficient for useful concerns such as:

- an expected mount disappeared from host116;
- an endpoint that previously supplied measurements is down;
- a filesystem measurement pair became incomplete;
- multi-endpoint mount visibility changed;
- ingestion behavior became uneven while storage visibility changed.

Ownership semantics may improve routing, explanation, accountability, or
remediation, but the repository evidence does not show that ownership is a
precondition for all useful operator concern.

## Recommended next investigation

Required question 8:

The next architectural gap appears to be **expectation / topology expectation / concern semantics**, not ownership alone.

The missing distinction is:

```text
observed visibility
    vs
expected visibility
    vs
operator-significant deviation
```

A follow-up investigation should determine what repository authority already
supports for expected topology, expected mounts, expected scrape targets,
expected ingestion paths, and expected visibility continuity. That investigation
should still avoid implementation and should decide whether expectation can be
modeled without ownership, or whether some domains need explicit ownership later.

## Non-conclusions

- This audit does not recommend implementing ownership.
- This audit does not recommend implementing targets.
- This audit does not recommend implementing lenses.
- This audit does not recommend implementing views.
- This audit does not recommend implementing topology alerts.
- This audit does not recommend implementing HomeOps surfaces.
- This audit does not choose a final ontology.
- This audit does not conclude that host115 owns the storage in the example.
- This audit does not conclude that host116 has an encoded expected mount today.
- This audit does not conclude that current-facts lookup should cross endpoint
  and host boundaries.
- This audit does not conclude that aliases should transfer ownership.
- This audit does not conclude that storage candidates are storage identities.

## Major findings

1. The repository is closer to a visibility model than an ownership model.
2. Operational concern can be present without ownership.
3. Filesystem visibility loss can matter even when the storage owner is unknown.
4. Target/described-entity remains only partially modeled through subject,
   predicate, and dimensions.
5. Ownership is not currently the next obvious architecture primitive; expected
   visibility and concern semantics appear to be the next gap.

## Required questions answered

1. **Can visibility exist without ownership?** Yes; storage visibility groups,
   shared-storage candidates, and endpoint availability are repository examples.
2. **Can operational concern exist without ownership?** Yes; down endpoints,
   storage topology ambiguities, incomplete filesystem measurement pairs, and
   unknown availability can matter without owner knowledge.
3. **Can a filesystem visibility loss be important even if ownership is
   unknown?** Yes; host116 losing mount visibility can affect ingestion and
   topology expectations without proving host115 ownership.
4. **Would a future Storage Lens primarily answer what is visible or who owns
   it?** Current authority points to what is visible.
5. **Would a future HomeOps View require ownership semantics to raise useful
   alerts?** No; visibility plus topology expectation can be sufficient for some
   useful alerts or notices.
6. **Are ownership and operational concern separate concepts?** Yes.
7. **Which concept appears closest to current repository authority?**
   Visibility, followed by measurement subject; target is partial and ownership
   is weakest.
8. **Which concept appears to be the next architectural gap?** Expected
   visibility / topology expectation / operational concern semantics.
