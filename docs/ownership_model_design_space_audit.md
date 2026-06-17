---
status: audit
scope: ownership model design-space investigation
created: 2026-06-17
---

# Ownership Model Design Space Audit

## Status

Investigation only. No implementation changes were made to ownership,
relationships, projections, lenses, views, alias handling, identity projection,
Prometheus normalization, availability handling, storage projection, entity
typing, inference rules, or predicate catalogs.

Short answer: repository authority does **not** show that Seed is simply missing
one concept named `ownership`. It shows several currently conflated questions:

```text
where was this observed?
what subject is the measurement stored on?
what entity, if any, does the measurement describe?
what entity owns, hosts, provides, or is responsible for a resource/service/capability?
what should a future lens present as useful operator interpretation?
```

The current repository has a strong `measurement subject` model, preserved
endpoint/non-endpoint identity boundaries, and bounded read projections. It does
not have a general modeled concept equivalent to `measurement owner`, `described
entity`, `observation target`, `measurement_target`, `resource_target`, or
`ownership transfer`.

## Audit question

```text
What ownership models are possible without violating existing repository boundaries?
```

This is not a recommendation for how ownership should work. The first-order
question is whether `ownership` is even the correct abstraction.

## Documents reconciled

Required investigation inputs:

- `docs/filesystem_measurement_identity_boundary_audit.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/lens_implementation_frontier_observation.md`

Related recent audit/reconciliation evidence was also considered where it
intersected this question, especially storage topology ambiguity and repository
observation/self-model boundary documents.

## Prior findings reconciled

The required documents are mutually consistent with the implementation evidence:

1. **Endpoint visibility is not host ownership.** Prometheus `instance` subjects
   such as `192.168.254.115:9100` remain endpoint-shaped measurement subjects.
2. **Measurement subject is not entity identity.** A fact subject can be a scrape
   endpoint without collapsing into the stable host identity.
3. **Alias is not ownership transfer.** Alias-like evidence is constrained, and
   endpoint/non-endpoint identity collapse is explicitly rejected.
4. **`prometheus_instance` is not identity collapse.** It preserves a source
   relation from stable nodename metadata to an endpoint, but it is intentionally
   excluded from alias predicates and suppressed as a Prometheus-derived topology
   relationship.
5. **Endpoint/non-endpoint boundaries are intentionally preserved.** Current
   facts, inference, State Summary availability scopes, and relationship
   projection all preserve this boundary.
6. **Lens/view language is not a license to mutate State.** Existing views are
   deterministic read-only projections over already-projected State; lens
   language remains mostly architectural vocabulary for bounded interpretation.

No inspected evidence contradicts the established findings.

## Repository evidence inspected

### State and facts

`Fact` stores `subject_id`, `predicate`, `value`, dimensions, evidence,
provenance, confidence, timing, and inference metadata. It has no separate
`owner`, `described_entity`, `observation_target`, or `measurement_target` field.
`FactSupport` likewise groups by subject, predicate, value/dimensions, support,
confidence, and timing; measurement support selects the latest current sample
rather than aggregating ownership claims.

`State` holds projected facts, observations, relationships, aliases, entity type
assertions, graph issues, fact support, conflicts, evidence, plans, tools, and
other projected structures. There is no State-level ownership index for
measurements or observations.

### Alias handling and identity projection

Alias projection is intentionally narrow. Alias predicates are `alias`,
`ip_address`, `hostname`, and non-Prometheus `*_instance` predicates.
`prometheus_instance` is explicitly excluded. The alias resolver rejects any edge
that would equate an endpoint-shaped subject with a non-endpoint-shaped subject.

Current-fact lookup can use alias resolution, but endpoint-scoped predicates
force exact subject lookup. The endpoint-scoped set is `availability_status`,
`health_status`, and `endpoint_role`.

Entity type projection separately classifies host-like subjects from host
predicates and endpoint-like subjects from `host:port` shape. This supports
visibility and classification; it does not transfer ownership.

### Prometheus normalization

Prometheus collection is read-only and allowlisted to `up`, `node_uname_info`,
`node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`. All emitted
samples use the Prometheus `instance` label as the observation subject. Only
`node_uname_info` is treated as authoritative for stable host identity metadata;
other metrics remain endpoint-scoped and do not participate in endpoint alias
normalization.

Predicate normalization preserves the original observation subject and
dimensions while deriving canonical predicates. Thus `filesystem_avail_bytes`
becomes `filesystem_free_bytes` on the same endpoint subject, not on a host
owner.

### Availability and health handling

`up` normalizes to canonical `availability_status`. `availability_status` and
`health_status` are measurement predicates. Inference from availability to health
preserves the selected subject; endpoint availability infers endpoint health,
not host health. State Summary separately counts endpoint scrape availability,
host availability, and service availability.

### Storage projection

`storage_state_projection(state)` is an explicit read projection. It scans
current measurement facts, selects `filesystem_free_bytes` and
`filesystem_total_bytes`, groups by canonical fact subject plus mountpoint and
filesystem dimensions, and emits complete rows only when both free and total are
present. Its row field is named `host`, but under current alias boundaries that
value may be an endpoint-shaped subject. The projection preserves filesystem
measurements; it does not prove physical storage ownership.

### Relationship projection

The relationship catalog has topology/dependency/grouping relationships such as
`alias_of`, `monitored_by`, `provides`, and `runs_on`. `prometheus_instance` can
normally derive `monitored_by`, and `endpoint_role` can normally derive
`provides`, but Prometheus-sourced `prometheus_instance -> monitored_by` and
Prometheus-sourced `endpoint_role -> provides` are suppressed. This is direct
evidence that repository authority avoids promoting scrape visibility into
service/capability ownership.

### Repository observations

Repository observation tests assert that repository extraction emits artifact
facts without architecture inference. Related documentation warns that imports,
definitions, calls, references, and documentation claims are support signals, not
ownership, behavior, or architectural responsibility unless an explicit rule
supports that conclusion. This mirrors the runtime measurement boundary:
visibility/support is not ownership.

## Ownership-related concepts discovered

The repository already has several concepts adjacent to ownership, but they are
not one concept:

| Concept | Current status | Boundary |
|---|---|---|
| Fact subject / observation subject | Implemented | The storage/query location of an observed or projected fact. |
| Measurement subject | Implemented through subject + measurement predicate semantics | Latest sample is per subject/predicate/dimensions. |
| Evidence/provenance source | Implemented | Explains where support came from, not who owns the thing described. |
| Alias / identity component | Implemented and constrained | Identity equivalence only inside allowed boundaries; not ownership transfer. |
| Entity type | Implemented | Classification, not ownership. |
| Relationship edge | Implemented for cataloged relationships | Topology/dependency/hosting/grouping, with Prometheus promotions suppressed where unsafe. |
| Lens/read projection | Partially implemented as deterministic read-only surfaces | Interpretation/selection over State; no new authority. |
| Measurement owner | Not found | Would be a new concept if introduced. |
| Described entity / observation target / measurement target | Not found as general State fields | Candidate vocabulary may be more accurate than ownership for endpoint-observed facts. |
| Resource owner/service owner/capability owner | Not general; only specific relations such as `runs_on`/`provides` exist | Semantics differ by domain and should not be collapsed prematurely. |

## Candidate models

### Model A: No new concept

```text
measurement subject is sufficient
```

**How it fits current repository authority**

This is the current implemented model. Facts and observations have one subject.
Measurement support chooses current samples by subject, predicate, and
dimensions. Prometheus metrics remain on endpoint subjects. Inference preserves
subject. Storage projection groups by canonical fact subject. Availability
surfaces separate endpoint, host, and service scopes without inventing an owner.

**Strengths**

- Lowest implementation and semantic risk.
- Preserves all established endpoint/non-endpoint boundaries.
- Keeps repository evidence honest: it says exactly what was observed and where
  it is stored.
- Works cleanly for endpoint scrape availability and direct host facts.
- Avoids making Prometheus labels, aliases, or path text into ownership claims.

**Limitations**

- Human operators often read endpoint-observed filesystem metrics as host
  resource facts; this model cannot answer that interpretation directly.
- Future Node Detail, Storage, or HomeOps surfaces may need caveats or may show
  endpoint visibility rather than host-owned resources.
- Service and capability ownership questions remain separate relationship or
  lens questions.
- The storage projection row name `host` can overstate semantics when the row is
  actually endpoint-shaped.

**Affected surfaces**

Current-facts lookup, storage projection, availability summary, health
inference, relationship projection, and future lenses can continue operating on
visibility plus provenance.

### Model B: Ownership Relationship

```text
measurement subject -> ownership relationship -> entity
```

**How it could fit without violating boundaries**

A relationship model could be compatible only if ownership edges are explicit,
evidence-bearing, source-scoped, and not derived from alias collapse. For
example, endpoint-observed filesystem measurements could remain on the endpoint
subject while a separate relationship says what entity owns, hosts, exports,
serves, or is responsible for the measured resource.

**Compatibility constraints**

- Must not make `prometheus_instance` an alias predicate.
- Must not allow endpoint/non-endpoint identity collapse.
- Must not make current-facts lookup cross endpoint boundaries silently.
- Must distinguish storage ownership, service hosting, service responsibility,
  capability provision, and observation provenance.
- Must avoid deriving ownership from Prometheus `endpoint_role`, filesystem path
  text, imports, definitions, or references alone.

**Strengths**

- Can represent real ownership or responsibility when evidence supports it.
- Keeps measurement facts on observed subjects while enabling separate topology
  or responsibility interpretation.
- Could support future lenses that need host/service/resource ownership claims.

**Limitations and risks**

- `ownership` is too broad: filesystem ownership, service ownership, tool
  ownership, and capability ownership do not obviously mean the same thing.
- Relationship projection already suppresses Prometheus promotions that look
  ownership-like, showing high risk of overprojection.
- If generalized prematurely, this model could become an unsupported authority
  layer.

**Best repository-consistent reading**

Possible, but only as an explicit future design family. Repository evidence does
not support introducing one generic ownership edge as the next assumption.

### Model C: Observation Target

```text
measurement subject
observation target
```

**How it fits repository language**

This model separates the stored measurement subject from the entity/resource the
observation is about, without claiming legal/physical/operational ownership. It
matches the repository's repeated distinction between where a fact was observed
and what it might describe.

**Strengths**

- More neutral than ownership.
- Better fit for Prometheus and filesystem examples: `192.168.254.115:9100`
  observed a filesystem metric; a future target concept could say the target is
  a host, mount, filesystem series, service, endpoint, repository artifact, or
  claim, depending on evidence.
- Preserves measurement subject and endpoint boundaries.
- Can support lens interpretation without transferring identity.

**Limitations and risks**

- Still not currently implemented as a general State concept.
- Needs precise vocabulary: observation target, measurement target, resource
  target, and described entity may not be interchangeable.
- A target relation could be mistaken for ownership unless caveated.

**Best repository-consistent reading**

This appears more aligned with current evidence than generic ownership for many
measurement cases, but the repository does not yet prove the exact name or
shape.

### Model D: Described Entity

```text
where observed
what described
```

**How it fits repository language**

This model explicitly distinguishes the observation/measurement carrier from the
entity described by the fact. It is close to the phrasing in prior audits:
“where observed vs what entity the measurement describes.”

**Strengths**

- Captures the filesystem tension directly.
- Avoids implying responsibility, control, or ownership.
- Could apply beyond metrics to repository observations: a source artifact may
  mention or describe a component without owning it.
- Supports caveated read projections where a lens says “this endpoint-observed
  sample appears to describe host X” without moving facts.

**Limitations and risks**

- “Describes” can be too broad for operational decisions. A metric, import,
  documentation sentence, and endpoint role can all describe something at
  different strengths.
- May need support strength, source scope, and predicate-specific rules to avoid
  overclaiming.
- Does not by itself answer ownership, hosting, responsibility, or action
  authority.

**Best repository-consistent reading**

Promising as a vocabulary for investigation because it matches existing boundary
language better than ownership. It should not be treated as an implementation
recommendation yet.

### Model E: Lens-only Interpretation

```text
ownership does not exist in State
future lenses perform interpretation
```

**How it fits current repository authority**

Existing views are deterministic read-only projections over State, and lens
language is currently exploratory. A future Storage Lens, Availability Lens,
Node Detail View, or HomeOps surface could interpret endpoint visibility plus
provenance without changing State or inventing State ownership.

**Strengths**

- Preserves State as observed/projected evidence rather than interpreted
  operator truth.
- Allows multiple bounded interpretations over the same facts.
- Avoids premature ontology changes.
- Can expose caveats such as “endpoint-observed,” “host-owned not asserted,” or
  “shared-storage candidate from observable fields only.”

**Limitations and risks**

- If lenses use ownership language without State support, they may create UI
  authority by presentation.
- Repeated ad hoc interpretations can diverge across surfaces.
- Some future actions or recommendations may require explicit State-backed
  semantics rather than a lens-only caveat.

**Best repository-consistent reading**

Safe for investigation and early read surfaces, provided lenses remain explicit
about visibility/provenance and avoid ownership claims.

## Model comparison

| Model | Boundary preservation | Fits current code | Fits filesystem metrics | Fits availability/health | Fits services/capabilities | Architectural risk |
|---|---:|---:|---:|---:|---:|---:|
| A. No new concept | High | High | Partial: endpoint facts only | High | Partial: relationships only where supported | Lowest |
| B. Ownership relationship | Medium if explicit; low if inferred | Low today | Risky unless scoped by evidence | Risky for endpoint scrape status | Potentially useful but domain-specific | Highest if generic |
| C. Observation target | High if non-owning | Not implemented | Strong conceptual fit | Medium: target may equal endpoint | Medium: needs predicate-specific rules | Medium |
| D. Described entity | High if caveated | Not implemented | Strong conceptual fit | Medium | Medium: “describes” may be too broad | Medium |
| E. Lens-only interpretation | High if caveated | Medium: views exist; formal lenses do not | Useful for read surfaces | Useful for scoped availability views | Useful but risks presentation authority | Low-to-medium |

## Example analysis

### Filesystem measurements

Example:

```text
192.168.254.115:9100 filesystem_free_bytes
```

Current repository authority says this is an endpoint-subject measurement with
filesystem dimensions such as mountpoint, device, and filesystem type. It does
not say the endpoint is the host identity, the physical disk owner, the storage
owner, or the node that should receive host-owned resource facts.

- Model A: accurate but limited; the measurement remains endpoint-scoped.
- Model B: possible only with explicit future storage/topology ownership
  evidence; unsafe if inferred from endpoint, alias, or path.
- Model C: plausible; endpoint is observation subject, filesystem/host/resource
  could become a target only with evidence.
- Model D: plausible; endpoint-observed measurement may describe a filesystem
  visible through that endpoint, but not necessarily ownership.
- Model E: a lens can present endpoint-visible storage with caveats and shared
  storage candidates without State ownership.

### Availability

`up` and `availability_status` are best handled as scoped measurements. For
Prometheus, `up` describes scrape-target availability, not necessarily host or
service availability. State Summary already separates endpoint scrape
availability from host and service availability.

- Ownership adds little here.
- Observation target/described entity can be useful only if a surface needs to
  say what availability is about.
- Visibility plus provenance is sufficient for many availability surfaces.

### Health

`health_status` can be observed directly or inferred from `availability_status`.
Inference preserves subject, and endpoint availability infers endpoint health.
There is no evidence that health should transfer to a host owner through aliases
or Prometheus instance facts.

- Model A preserves current behavior.
- Model B is risky because “owner health” is not the same as “observed endpoint
  health.”
- Models C/D may help distinguish observed subject from described entity if
  future sources provide stronger evidence.

### Services

Services already have relationship vocabulary such as `runs_on` and may have
availability facts on service subjects. Prometheus `endpoint_role` is
intentionally not promoted to `provides` when Prometheus-sourced.

- Service ownership is not the same as measurement ownership.
- A service may run on a host, provide a capability, be monitored by a system, or
  have endpoint visibility; these are different relations.
- Generic ownership would conflate hosting, responsibility, provision,
  monitoring, and availability.

### Capabilities and tools

The relationship catalog can project `provides` to capability for supported
non-Prometheus facts. Capability inventory and verification concepts describe
status and support; they do not imply that any endpoint label owns the
capability. Tool ownership in repository/self-model contexts is also narrower:
source structure, registrations, and tests may support existence or behavior,
but not broad architectural ownership without explicit rules.

- Capability ownership and filesystem ownership do not mean the same thing.
- `provides` is a more precise relation than generic ownership where evidence
  supports it.

### Repository observations

Imports, definitions, calls, and references are visibility/support facts. They
can support existence, structure, or narrow behavior claims under explicit rules,
but they do not prove architecture ownership by themselves. This is analogous to
Prometheus: visibility of a metric or label does not prove ownership of the
underlying host/service/resource.

## Ownership vs target analysis

### Is ownership actually one concept?

No. Repository evidence points to multiple concepts currently being conflated:

- **measurement subject**: where the fact lives in projected State;
- **observation source/provenance**: where evidence came from;
- **endpoint visibility**: what a scrape target or local observation could see;
- **identity aliasing**: when two names are treated as the same entity;
- **hosting/topology**: where services run or how entities depend on each other;
- **capability provision**: what an entity provides;
- **physical/resource ownership**: stronger storage/control/responsibility
  semantics not generally modeled;
- **described entity/target**: what an observation is about, without ownership;
- **lens interpretation**: what an operator surface chooses to present.

### Would filesystem ownership, service ownership, and capability ownership mean the same thing?

No. Filesystem ownership might mean physical disk control, mount visibility,
local filesystem responsibility, exported/shared storage, backup authority, or
capacity attribution. Service ownership might mean `runs_on`, operator
responsibility, service endpoint identity, or availability subject. Capability
ownership might mean `provides`, registration, verification responsibility, or
implementation location. A single generic ownership relation would erase these
differences.

### Is Seed missing ownership, or a more general target concept?

The stronger evidence is that Seed is missing a general way to represent
`where observed` versus `what described/targeted`, if future surfaces require
that distinction. `ownership` is only one possible stronger interpretation of a
target relation and should not be assumed for endpoint-observed measurements.

## Boundary preservation analysis

A repository-consistent ownership/target design space must preserve these
boundaries:

1. **Subject preservation.** Prometheus and other observations should not move
   measurements from observed subjects to host subjects by default.
2. **Alias boundary.** Endpoint/non-endpoint aliases must not collapse identity
   unless repository authority changes explicitly.
3. **Predicate scope.** Endpoint-scoped predicates must remain exact-subject
   unless a separate read surface explicitly and caveatedly interprets them.
4. **Relationship caution.** Prometheus labels and instances must not silently
   become `provides`, `monitored_by`, ownership, or service topology.
5. **Storage ambiguity.** Mount visibility and filesystem measurements must not
   imply physical storage ownership.
6. **Repository observation boundary.** Imports, definitions, calls, and
   references must not become architectural ownership claims without explicit
   support rules.
7. **Lens authority boundary.** Lenses may select and interpret projected facts,
   but should not create hidden State authority or unsupported ownership truth.

## Architectural risks

1. **Semantic collapse risk.** Treating ownership as one concept would collapse
   resource visibility, host identity, service hosting, capability provision,
   physical control, and responsibility.
2. **Alias misuse risk.** Expanding alias behavior would directly contradict the
   preserved endpoint/non-endpoint boundary.
3. **Prometheus overprojection risk.** `endpoint_role` and `prometheus_instance`
   look tempting as topology signals, but repository code suppresses their
   Prometheus-derived relationship promotions.
4. **UI authority risk.** A lens or summary can imply ownership by labels such as
   `host` or by grouping endpoint metrics under node detail, even if State does
   not assert ownership.
5. **Action authority risk.** Ownership-like language can influence repair,
   backup, capacity, or recommendation decisions; unsupported ownership would be
   higher risk than unsupported visibility.
6. **Repository self-model overclaim risk.** Source observations can support
   existence and narrow structural claims, but not broad ownership unless rules
   define the support pattern.

## Answers to required questions

### 1. Is ownership actually one concept?

No. The evidence separates measurement subject, observation provenance,
visibility, identity, topology, capability provision, physical/resource control,
responsibility, target/description, and lens interpretation.

### 2. Would filesystem ownership, service ownership, and capability ownership mean the same thing?

No. They have different evidence requirements and different safe predicates or
relationships. `runs_on`, `provides`, mount visibility, and physical ownership
are distinct claims.

### 3. Can endpoint visibility alone support useful future lenses?

Yes, for bounded read-only lenses that clearly say they are showing endpoint
visibility plus provenance. Endpoint visibility alone can support scrape
availability, endpoint-observed filesystem detail, shared-storage candidates
from observable fields, and investigation prompts. It cannot support
host-owned resources, service ownership, physical storage ownership, or action
authority without additional evidence.

### 4. Would HomeOps, Node Detail, Availability, and Storage surfaces require ownership semantics?

Not necessarily.

- **Availability** can operate on visibility plus provenance using existing
  endpoint/host/service scopes.
- **Storage** can initially operate as endpoint-visible filesystem measurement
  detail with ambiguity grouping and caveats.
- **Node Detail** can show direct host facts plus related endpoint visibility,
  if it does not relabel visibility as host ownership.
- **HomeOps** could operate as a high-level lens over visibility/provenance, but
  any repair, backup, or capacity recommendation would likely require stronger
  explicit semantics than visibility alone.

### 5. Which candidate model best preserves existing repository boundaries?

Model A preserves boundaries most completely because it is the current model.
Model E also preserves boundaries if lens output is caveated and does not create
new authority. Models C and D can preserve boundaries if kept non-owning and
explicit. Model B preserves boundaries only if ownership relationships are
strictly explicit and domain-specific; a generic ownership relationship is the
most boundary-sensitive option.

### 6. Which candidate model introduces the least architectural risk?

Model A introduces the least risk. Model E is low risk for investigation and
read-only presentation if caveats are strong. Models C/D are moderate-risk
candidate vocabulary for the next investigation. Model B is highest-risk unless
split into narrower, evidence-specific relationships.

## Recommended next investigation

Do not implement ownership. Recommended next investigation:

```text
Target / description vocabulary audit
```

Questions for that audit:

1. Is the missing abstraction best named `observation_target`,
   `measurement_target`, `described_entity`, `applies_to`, or something else?
2. Are there separate target families for measurements, repository artifacts,
   services, capabilities, and resources?
3. What evidence is sufficient to say an endpoint-observed measurement describes
   a host, filesystem, mount, service, or capability without asserting
   ownership?
4. Which future surfaces can operate on endpoint visibility plus provenance, and
   which require stronger explicit target/ownership semantics before they can be
   safe?
5. What wording should lenses use to avoid implying ownership where State only
   preserves visibility?

## Non-conclusions

- This audit does not conclude that Seed should implement ownership.
- This audit does not conclude that Seed should implement observation targets,
  described entities, applies-to relations, lenses, or views.
- This audit does not choose a winning model.
- This audit does not conclude that filesystem measurements should move from
  endpoints to hosts.
- This audit does not conclude that aliases should bridge endpoint and host
  identity.
- This audit does not conclude that `prometheus_instance` should become an alias
  or ownership relation.
- This audit does not conclude that Storage, Availability, Node Detail, or
  HomeOps surfaces require ownership semantics.
- This audit does not conclude that endpoint-owned Prometheus measurements are
  wrong; it concludes that ownership is not currently modeled and may not be the
  right first abstraction.
