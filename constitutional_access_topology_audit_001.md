# Constitutional Access Topology Audit 001

Repository authority wins. This is exactly one bounded Constitutional Access Topology Audit. It does not implement access architecture, does not create an access registry, does not recover tools, and does not assume one owner for every access domain.

## Bounded audit question

Across repository, filesystem, service, network, internet, privileged-local, external-identity, and peer-Seed boundaries, what is the constitutional unit of access, and which current artifacts compress access observation, authority, reachability, identity, credentials, scope, effects, and authorization?

## Reviewed evidence

Primary implementation evidence reviewed:

- `seed_runtime/operator_authority_scope_binding.py` for interpreted operator request, activity class, scope binding, required authority, effect constraints, and future bounded-question handoff.
- `seed_runtime/observation_permission.py` for observation classes and manual/reusable permission visibility.
- `seed_runtime/repository_observation.py` for explicit repository observation of an arbitrary git-backed path without event-ledger writes or cluster mutation.
- `seed_runtime/privilege_discovery.py` for privilege guidance, limiting reasons, Docker/root/systemd/listener boundaries, and visibility-only behavior.
- `seed_runtime/candidate_operational_realization.py` for candidate mechanism, grammar, behavior, dependency, authority, and standing dimensions.
- `seed_runtime/capability_reachability_projection.py` for exact bounded transformation reachability and blocker classes.
- `seed_runtime/operational_realization_selection.py` for selection policy and its refusal to authorize or execute.
- `seed_runtime/operational_realization_warrant.py` for bounded reliance on one selected realization and its refusal to authorize, schedule, emit, or execute.
- `seed_runtime/external_material_testimony_binding.py` and `seed_runtime/external_site_rule_testimony.py` for external testimony integrity and site-rule testimony boundaries.

Primary characterization/audit/slice evidence reviewed:

- `authority_ingress_egress_topology_audit_001.md`.
- `operator_authority_scope_binding_slice_001.md`.
- `input_interpretation_candidate_characterization.md`.
- `capability_demand_realization_reachability_topology_audit_001.md`.
- `capability_reachability_projection_slice_001.md`.
- `operational_realization_topology_audit_001.md`.
- `operational_realization_warrant_slice_001.md`.
- `docs/filesystem_measurement_identity_boundary_audit.md`.
- `docs/local_network_observation_audit.md`.
- `docs/listening_port_observation.md`.
- `docs/reachable_observation_third_slice_investigation.md`.
- `IMPLEMENTATION.md`.

## Current access-related owners and artifacts

| Current owner/artifact | What it owns | What it does not own |
| --- | --- | --- |
| `OperatorAuthorityScopeBindingProjection` | One interpreted operator request bound to ingress authority and scope. It preserves operator identity, workspace/session, requested activity class, requested/resolved/permitted/excluded scope, required authority class, operator effect constraints, and binding state. | It explicitly does not establish mechanism availability, capability reachability, selection, warrant, or execution. |
| `ObservationPermissionReport` | Visibility of observation domains and classes: local passive, network passive, network active, local privileged, external, and unknown. It distinguishes observed reusable approval from manual invocation. | It does not enforce permission, store approvals, or create runtime autonomy. |
| `RepositoryObservation` | Read-only git work-tree observation for an explicit path: head, branch, remote presence, and porcelain status counts. | It does not establish repository role, canonicality, reliance authority, or authority to inspect every repository. |
| `PrivilegeDiscoveryAudit` | Visibility-only explanation of capability access level, implementation evidence, guidance status, and limiting reason. | It does not use sudo, escalate privilege, write the event ledger, or mutate the cluster. |
| `CandidateOperationalRealizationSet` | Candidate realization dimensions: mechanism availability, grammar, behavior, representation, method, dependency, authority, and standing. | It does not project overall reachability, rank, select, or authorize. |
| `CapabilityReachabilityProjection` | Demand-level reachability for one exact bounded transformation, including dependency, authority, representation, method, grammar, behavior, and mechanism blockers. | It does not select, authorize, schedule, execute, or prove possession of a mechanism. |
| `OperationalRealizationSelection` | Selection of zero or one supported realization under policy. | It does not warrant, authorize, schedule, execute, translate, or construct an invocation. |
| `OperationalRealizationWarrant` | Bounded reliance warrant for one selected realization in current State. | It does not authorize, schedule, emit, or execute. |
| External testimony artifacts | Source/artifact/span integrity and attributed site-rule testimony preservation. | They do not determine truth, permission, prohibition, applicability, precedence, Seed authorization, or external movement. |

## Independently inspected proving cases

### 1. Repository

- **Who is the access subject?** The current Seed runtime/operator session acting through an explicit repository-observation surface or through repository-local evidence review.
- **What activity is requested?** Enumerate/read repository state or rely on repository evidence for constitutional analysis.
- **Exact target.** An exact path supplied to repository observation, a current workspace, another repository path, generated artifacts, mirrors/forks, or a canonical/reference role claim.
- **Exact scope.** Path-specific git work tree when `--observe-repository PATH` is supplied; document-specific scope when reading files; no global repository universe.
- **Boundary/path.** CLI argument to repository observation; filesystem path resolution; git command read-only status path; repository evidence citation path.
- **Authority required.** Repository observation/read authority for the path; separate reliance authority for treating repository evidence as constitutional authority; separate role evidence for canonical/reference/mirror/fork/generated status.
- **State that must be observed.** Whether path is a git work tree; head/branch/status/remote presence; artifact contents; role evidence if repository-role claims are made.
- **Identity/credential required.** Local filesystem identity sufficient for local read; remote credentials only if a remote fetch/clone is requested, which is a different activity.
- **Permitted effects.** Read-only inspection; no event-ledger write and no cluster mutation for current repository observation artifact.
- **Prohibited effects.** Mutating repository state, fetching from a remote, rewriting generated artifacts, or treating role labels as automatic reliance authority.
- **Reachability established by.** Path existence/readability, git executable availability, git work-tree test, and file contents for document review.
- **Reachability blocked by.** Missing path, unreadable path, unavailable git executable, non-work-tree path, absent role evidence, or remote unavailable/unauthorized.
- **Unknown.** Whether additional repositories, mirrors, forks, or canonical/reference roles exist unless observed.
- **Later authorization still required.** Remote network request, authenticated clone/fetch, writing files, deleting files, executing repo code, or relying on non-current repository as canonical.
- **Access != ?** Repository role, canonicality, generated-artifact status, or reliance authority.
- **Authority != ?** Path readability, git availability, or repository status output.
- **Reachability != ?** Permission to rely, mutate, fetch, execute, or publish.

### 2. Filesystem

- **Who is the access subject?** Seed runtime/operator session or an implemented observation source.
- **What activity is requested?** Enumerate, read, write, delete, or execute; these are constitutionally distinct.
- **Exact target.** Exact path, file, directory, descendant tree, procfs/sysfs file, mount table, socket table, generated artifact, or executable path.
- **Exact scope.** Exact path and descendants only where authorized; not “filesystem access” globally.
- **Boundary/path.** Local OS filesystem boundary; path traversal; bounded read helper; pseudo-file and size/truncation constraints.
- **Authority required.** Activity-specific path authority. Read-only local passive authority for procfs/socket-table reads differs from write/delete/execute authority and from root visibility.
- **State that must be observed.** Path existence, file type, size/truncation status, permissions, regular/pseudo-file handling, and whether target is in requested scope.
- **Identity/credential required.** Local process user identity; root/sudo/container-daemon identity only for protected files or privileged views.
- **Permitted effects.** Read bounded files when in scope; write only if a file-modification task explicitly authorizes it.
- **Prohibited effects.** Silent global traversal, delete, execute, privilege escalation, raw device access, kernel mutation, or treating endpoint-owned measurements as host-owned facts.
- **Reachability established by.** Local path and OS permissions plus implementation-backed bounded readers.
- **Reachability blocked by.** Missing path, permission denied, protected file, oversize/truncated pseudo-file, absent implementation guidance, or prohibited activity.
- **Unknown.** Whether a protected path would be readable under another identity unless that identity and credential are observed and authorized.
- **Later authorization still required.** Write/delete/execute, descendant expansion beyond bounded scope, sudo/root, container-runtime socket, or remote filesystem access.
- **Access != ?** A single filesystem boolean.
- **Authority != ?** File existence, path syntax, or local mechanism availability.
- **Reachability != ?** Authorization to mutate or promote measurements across identity boundaries.

### 3. Services

- **Who is the access subject?** Seed observation source/operator session; possibly external service-management provider if later selected.
- **What activity is requested?** Observe status, query an interface, authenticate, change configuration, restart, or administer.
- **Exact target.** Local listener endpoint, systemd unit, service API endpoint, container, process, or provider-specific service object.
- **Exact scope.** Endpoint inventory, service-manager unit inventory, process attribution, container ownership, service ownership, or administrative movement; these scopes are not interchangeable.
- **Boundary/path.** Local socket tables; systemd inventory; service API; container runtime socket; service-management provider.
- **Authority required.** Local passive for listener endpoint shape; systemd inventory where available; Docker group/root for container inventory; authenticated/admin authority for service changes.
- **State that must be observed.** Bound protocol/address/port, unit state/substate, process/container attribution, service API grammar, credentials, and effect constraints.
- **Identity/credential required.** None for bounded listener endpoint shape; local OS/systemd visibility for unit inventory; service credentials for authenticated query/admin; Docker/root identity for container ownership.
- **Permitted effects.** Read-only observation where bounded; no restart/config mutation unless separately authorized.
- **Prohibited effects.** Treating endpoint reachability as service understanding, treating listener facts as ownership, or treating service status observation as administration authority.
- **Reachability established by.** Implementation-backed local reads and available non-root inventory for bounded questions.
- **Reachability blocked by.** Missing process attribution, Docker/root unavailable, unknown service API grammar, absent credential, or policy forbidding effectful movement.
- **Unknown.** Owner, health, responsiveness, desired state, dependency causality, and external accessibility unless observed through appropriate boundaries.
- **Later authorization still required.** Authentication, configuration change, restart, remote API call, or service-admin operation.
- **Access != ?** Listening port existence.
- **Authority != ?** Endpoint reachability or unit visibility.
- **Reachability != ?** Service comprehension or change authorization.

### 4. Network and Internet

- **Who is the access subject?** Seed runtime/operator session or external observation provider.
- **What activity is requested?** Consume existing observation, emit observational request, perform active discovery/probing, authenticate to a remote, or effect remote movement.
- **Exact target.** Local network config, DNS resolver config, neighbor table, endpoint, site URL, provider API, git remote, HTTP resource, or remote service.
- **Exact scope.** Local passive host config; network passive capture; network-active probe; external provider/site request; authenticated remote interaction; remote mutation.
- **Boundary/path.** Local kernel/config files; socket emission; DNS/HTTP/Git/protocol request; external identity/provider boundary.
- **Authority required.** Local passive authority for reading local config; explicit network-active/external authority for emitting requests; provider/site-specific authorization for authenticated/effectful movement.
- **State that must be observed.** Existing observations, local config, request target, protocol grammar, environmental network reachability, site rules/testimony, credential/identity availability, effect constraints.
- **Identity/credential required.** None for local passive config; possibly network identity/IP for emitted requests; provider credentials for authenticated interaction.
- **Permitted effects.** Consume existing observations; read local config; only emit requests within bounded authorization.
- **Prohibited effects.** Calling HTTP GET, DNS, Git fetch, ping, ARP, scan, provider API, or similar “passive” merely because intended purpose is observation; remote mutation without exact authorization.
- **Reachability established by.** Implemented request mechanism, dependency availability, target address/grammar, network path success, credential availability if required, and policy authorization.
- **Reachability blocked by.** Missing operator authority, scope, DNS/network path, mechanism, dependency, protocol grammar, credential, provider identity, policy authorization, or effect constraints.
- **Unknown.** Remote truth, site policy precedence, whether external request is admissible, and whether remote side effects occur.
- **Later authorization still required.** Each exact external request, active probe, authenticated interaction, and effectful remote movement.
- **Access != ?** Internet-enabled boolean.
- **Authority != ?** Network route, DNS resolution, HTTP library, or site testimony.
- **Reachability != ?** Constitutional passivity, remote authorization, admissibility, or truth.

### 5. Privileged local activity

- **Who is the access subject?** Operator/Seed session, local process user, root/sudo identity, Docker group identity, or container-runtime identity.
- **What activity is requested?** Observe protected state, read Docker socket, inspect containers, read NFS exports, administer system, access kernel interfaces, or raw devices.
- **Exact target.** Protected file, `/var/run/docker.sock`, container inventory, container port mapping, systemd, NFS export config, kernel interface, raw block device.
- **Exact scope.** One protected inventory or one exact privileged movement, not general root.
- **Boundary/path.** OS privilege boundary; sudo/become boundary; Docker socket/root-equivalent boundary; kernel/raw-device boundary.
- **Authority required.** Exact privileged authority matching activity, scope, target, and effects. Operator may request privileged activity is not the same as privileged identity reachable.
- **State that must be observed.** Current capability need, implementation evidence, guidance status, access level, credential/identity availability, and policy/effect constraints.
- **Identity/credential required.** Root, sudo, Docker group, container-runtime credential, or other protected identity as applicable.
- **Permitted effects.** Visibility-only explanation in current privilege discovery; non-root observations where sufficient.
- **Prohibited effects.** Sudo, privilege escalation, cluster mutation, raw-device movement, system administration, Docker mutation, or credential capture absent separate authorization.
- **Reachability established by.** Observed identity/credential and mechanism plus dependency and policy authorization for the exact privileged movement.
- **Reachability blocked by.** Access level root/docker_group_or_root, missing implementation evidence, missing guidance, absent credential, absent mechanism, or explicit effect prohibition.
- **Unknown.** Whether privilege would be available in another environment or via another operator identity.
- **Later authorization still required.** Exact privileged read/admin movement and any execution after reachability.
- **Access != ?** Root toggle.
- **Authority != ?** Sudo binary, Docker socket path, or operator desire.
- **Reachability != ?** Authorization to perform exact privileged movement.

### 6. External identity and credentials

- **Who is the access subject?** Operator, Seed session, provider account, external service identity, credential-bearing process, or peer identity.
- **What activity is requested?** Observe credential reference, bind identity, use credential, authenticate, query, submit, mutate, or attest.
- **Exact target.** Provider account, API endpoint, SSH host, git remote, site, token scope, credential store, identity assertion, or external testimony source.
- **Exact scope.** Credential observation, identity binding, credential availability, operator permission to use identity, and exact request authorization are separate.
- **Boundary/path.** Secrets boundary; external provider identity boundary; policy authorization boundary; disclosure boundary.
- **Authority required.** Identity-use authority and exact activity/scope authorization; credential presence alone is not authority.
- **State that must be observed.** Identity binding evidence, credential availability, credential scope, disclosure constraints, policy authorization, request target, effect constraints.
- **Identity/credential required.** The specific provider/local/external identity and non-disclosed credential material appropriate to the request.
- **Permitted effects.** Preserve credential/identity Unknowns and non-disclosure; use only if exact bounded authorization exists.
- **Prohibited effects.** Storing raw tokens/passwords/private keys in events, models, CLI args, handoff plans, action plans, or database; using credential observation as authorization.
- **Reachability established by.** Bound identity plus available credential plus mechanism/dependency plus policy authorization for exact request.
- **Reachability blocked by.** Credential absent, identity unbound, credential scope insufficient, disclosure constraint, missing mechanism, or missing policy authorization.
- **Unknown.** Credential existence and scope when not safely observable; external identity authority; provider-side policy.
- **Later authorization still required.** Every exact authenticated/effectful request.
- **Access != ?** Credential possession.
- **Authority != ?** Identity string or credential presence.
- **Reachability != ?** Permission to use identity or disclose secret.

### 7. Peer Seeds

- **Who is the access subject?** This Seed session, a peer Seed, or an operator mediating communication.
- **What activity is requested?** Discover peer, bind peer identity, understand protocol grammar, send message, receive testimony, admit claim, or coordinate movement.
- **Exact target.** Peer endpoint, peer identity, protocol grammar, message, testimony reference, claim, or external State.
- **Exact scope.** Reachability, identity, grammar, attribution, testimony admissibility, and claim establishment are separate.
- **Boundary/path.** Network/external-identity boundary; peer protocol boundary; testimony/evidence admission boundary; State boundary.
- **Authority required.** Exact communication authority, identity-use authority where credentials are involved, and separate admissibility authority for testimony.
- **State that must be observed.** Peer endpoint reachability, peer identity binding, protocol grammar, message attribution, provenance, testimony integrity, and admissibility conditions.
- **Identity/credential required.** Peer identity credential if authenticated; otherwise peer identity remains Unknown or weakly attributed.
- **Permitted effects.** Preserve attributed testimony and Unknowns; treat peer material as external testimony unless admitted by local rules.
- **Prohibited effects.** Treating another Seed as trusted internal State, treating peer reachability as claim truth, or treating grammar understanding as authorization.
- **Reachability established by.** Network path, protocol grammar, identity binding, credential availability, and policy authorization.
- **Reachability blocked by.** No peer endpoint, no grammar, identity unbound, message unattributed, testimony inadmissible, or policy/effect constraint.
- **Unknown.** Peer trust, peer State truth, identity authenticity, testimony admissibility, and claim support absent local validation.
- **Later authorization still required.** Communication, claim admission, reliance, and any effectful coordination.
- **Access != ?** Peer trust.
- **Authority != ?** Peer availability.
- **Reachability != ?** Testimony admissibility or claim establishment.

## Comparison findings

### Recurring constitutional access dimensions

The recurring dimensions are:

1. subject;
2. requested activity;
3. exact target;
4. exact scope;
5. boundary/path;
6. required authority class;
7. State to be observed;
8. identity/credential requirement;
9. permitted effects;
10. prohibited effects;
11. environmental reachability basis;
12. environmental reachability blockers;
13. mechanism/dependency/grammar availability;
14. policy/realization-specific authorization;
15. Unknown/conflict preservation;
16. later authorization still required.

### Recurring access subjects

The subjects recur as operator/session/workspace, local Seed runtime/process user, external provider identity, privileged local identity, service identity, and peer Seed. None is a universal “Seed has access” subject.

### Recurring activities

Read/observe, enumerate, write, delete, execute, query, authenticate, administer, probe, request external material, communicate with peer, rely, warrant, authorize, and execute recur as distinct activities.

### Recurring target and scope boundaries

Exact path, descendant path, repository path, git work tree, endpoint, host, service, process, container, site URL, provider API, credential scope, peer identity, and bounded transformation recur as targets/scopes. Repository role and filesystem path are not the same kind of scope. Endpoint identity and host identity remain separate in measurement ownership.

### Authority-class findings

Current artifacts already contain authority classes, but they are domain-local and compressed:

- `OperatorAuthorityScopeBindingProjection` maps interpreted movement into classes such as constitutional read, network-active observation, local passive observation, local privileged observation, external effectful movement, and presentation request.
- `ObservationPermissionReport` uses local passive, network passive, network active, local privileged, external, and unknown.
- `PrivilegeDiscoveryAudit` uses access levels such as available, local_passive, partial_non_root, docker_group_or_root, root, partial_passive, and unknown.
- Candidate realization/reachability artifacts use authority standing as reachable/unavailable/unknown/conflict, which is narrower than constitutional authorization.

The evidence supports authority as one dimension of access, not the unit of access.

### Target and scope findings

Access operates on exact target/scope relationships, not broad domains. “Filesystem,” “internet,” “repository,” “service,” and “root” are too coarse. A lawful access statement must name the activity and exact scope: for example, read local procfs TCP/UDP socket tables for listener endpoint inventory is different from inspect container ownership through Docker socket and different from restart a service.

### Identity and credential findings

Identity and credentials are independent dimensions. Operator identity is not unlimited authority. Credential observed, identity bound, credential available, operator may use identity, and exact request authorized are not interchangeable. External material/source identities establish testimony attribution and integrity boundaries, not truth or authorization.

### Environmental reachability findings

Reachability is environmental and dimensional. Mechanism available, dependency available, target reachable, grammar understood, identity credential available, and authority reachable can all fail independently. Capability reachability is about one exact bounded transformation; it is not mechanism possession, not selection, not warrant, and not authorization.

### Effect-constraint findings

Effects recur as read-only, writes-event-ledger, mutates-cluster, remote request emission, authentication, configuration change, restart/administer, repository mutation, file write/delete/execute, privilege escalation, and external movement. Current read-only diagnostic/observation artifacts repeatedly preserve `writes_event_ledger=false` and `mutates_cluster=false`. Operator-stated effect constraints remain requirements, not proof that a realization satisfies them.

### Repository-role distinction

Repository access has three separable questions:

1. may read or observe this repository/path;
2. what role does this repository/artifact have: current workspace, generated artifact, mirror, fork, canonical/reference, or additional repository;
3. may rely on that repository/artifact as constitutional authority.

Current repository observation proves only path-specific git-state observation. It does not prove canonicality, reference role, reliance, or permission to fetch/write/execute.

### Peer-Seed distinction

A peer Seed is external testimony unless local evidence admits specific claims. Peer reachable, peer identity bound, protocol grammar understood, message attributed, testimony admissible, and claim established are separate. Another Seed is not trusted internal State merely because it is reachable or because it speaks a recognizable grammar.

## Access versus adjacent responsibilities

- **Access versus capability reachability:** Access contributes authority/scope/identity/effect dimensions; capability reachability decides whether one exact bounded transformation is reachable under mechanism, dependency, authority, grammar, behavior, representation, and method evidence.
- **Access versus operational realization:** A realization candidate names mechanism/grammar/behavior/dependency/authority standings for a demand. It is not itself authorization and does not prove general access.
- **Access versus warrant:** Warrant supports reliance on one selected realization. It still refuses authorization, scheduling, emission, and execution.
- **Access versus authorization:** Authorization is realization/request-specific policy permission to move. Authority classes and reachable candidates are not enough.
- **Access versus execution:** Execution is an effectful movement outside these read-only audit/projection artifacts. Existing core evidence delegates actual execution, secrets, retries, scheduling, credential prompts, and host automation to external providers rather than making Seed own a universal execution lifecycle.

## Minimum-missing-authority explanation

Seed should explain a blocked inquiry by naming the missing boundary, not by asking for a tool. The explanation shape should distinguish at least:

- operator authority;
- scope permission;
- identity binding;
- credential availability;
- environmental reachability;
- mechanism availability;
- dependency availability;
- grammar;
- effect constraint;
- policy authorization.

Seed must not request additional authority when authority would not resolve the actual blocker. Examples:

- If Docker socket read is unavailable because credential/identity is unavailable, the missing boundary is privileged identity/credential reachability, not generic authority.
- If a HTTP request cannot be emitted because network-active/external activity is not authorized, the missing boundary is operator authority/scope/effect authorization.
- If a service API cannot be queried because grammar is unknown, requesting broader authority is unlawful noise.
- If repository role is Unknown, asking for internet or filesystem authority does not resolve canonicality.

Smallest lawful request shape for one bounded missing-authority case:

```text
For this bounded inquiry only, may Seed perform one read-only local privileged observation of Docker container inventory through the Docker socket at the exact local socket path required for container ownership attribution, with no container mutation, no service restart, no event-ledger write unless separately requested, no cluster mutation, no credential disclosure, and no reuse of this permission beyond this inquiry?
```

This request names subject, activity, target, scope, boundary, authority class, identity/credential dependency, permitted effects, prohibited effects, and non-reuse. It does not ask for a Docker tool or a root toggle.

## Strongest supporting evidence

- Operator authority/scope binding already separates requested activity, requested scope, resolved/permitted/excluded scope, required authority class, operator constraints, additional authority, and future bounded-question handoff.
- Observation permission already separates observation class from permission state and denies that manual invocation creates reusable permission.
- Privilege discovery already distinguishes access level, implementation evidence, guidance status, and limiting reason.
- Candidate realization/reachability/selection/warrant artifacts already split mechanism, grammar, behavior, dependency, authority, selection, warrant, and refusal to authorize/execute.
- Local listener, local network, and filesystem measurement audits preserve non-inference boundaries: local listener != reachability/ownership; local network config != network health; endpoint visibility != host ownership.
- External testimony artifacts preserve source/span/testimony integrity and explicitly refuse truth, authority, permission, precedence, and authorization.

## Strongest counterevidence

- Several artifacts still use compressed labels such as authority standing, current access, observation class, access level, capability, external, local privileged, and reachable. These labels are useful locally but can look like one access taxonomy if read outside their owning artifacts.
- `PrivilegeDiscoveryCapability.access_level` can sound like access itself even though its formatter and limiting reason show it is visibility guidance.
- `CapabilityReachabilityProjection.authority_reachability` can sound like authorization even though boundary notes explicitly separate authority reachability from selection/authorization/execution.
- Observation permission domains classify external/provider query and active network probe, but do not themselves encode exact request target, identity, credential, grammar, policy authorization, or effect constraints.
- Repository observation can read arbitrary git-backed paths if reachable locally, but that does not include an explicit artifact for repository role/canonicality/reliance.

## Exact current compressions

1. **Observation permission compression:** domain and observation class compress target, scope, identity, credential, environmental reachability, and effect constraints.
2. **Privilege discovery compression:** capability/access level compresses target, privileged identity, credential, mechanism, dependency, and exact authorization.
3. **Capability reachability compression:** authority standing compresses ingress authority, policy authorization, identity/credential, and environmental authorization into reachable/unavailable/unknown/conflict at candidate level.
4. **Candidate realization compression:** mechanism availability, dependency evidence, authority evidence, and grammar can coexist but do not carry full subject/activity/target/scope/effect relationship.
5. **Repository observation compression:** path observation compresses workspace/current/additional/mirror/fork/generated/canonical/reference roles unless separate evidence is inspected.
6. **Filesystem compression:** “path readable” can be mistaken for enumerate/write/delete/execute authority if activity is not named.
7. **Service compression:** endpoint/listener/unit visibility can be mistaken for process ownership, service understanding, authenticated query, or administration authority.
8. **Network/internet compression:** external request mechanisms can be mistaken for passive observation; HTTP GET/DNS/Git fetch have emitted-request and remote-policy dimensions.
9. **Credential compression:** credential observed/available can be mistaken for identity-use authority or exact request authorization.
10. **Peer compression:** peer reachability/protocol compatibility can be mistaken for internal State trust, testimony admissibility, or claim establishment.

## First missing ownership boundary

The first missing ownership boundary is not an implementation registry. It is a constitutional characterization boundary for a single requested access relationship:

```text
subject + activity + target + exact scope + boundary/path + required authority + observed State + identity/credential + permitted effects + prohibited effects + reachability basis + blockers + later authorization
```

Current owners each hold slices of this relationship, but no current artifact owns the full constitutional relationship as a bounded access characterization. That does not yet warrant one implementation slice.

## Whether one implementation slice is warranted

No implementation slice is warranted by this audit. Repository evidence supports several independent access responsibilities already existing: operator ingress authority/scope binding, observation permission visibility, privilege discovery visibility, repository observation, capability reachability, realization selection, warrant, and external testimony preservation. The next move should remain a bounded question, not an access registry, global permission table, authority manager, credential store, network catalog, or root/internet boolean.

## Exact next bounded question

```text
For one blocked inquiry, which existing artifact should explain the missing boundary when the blocker is not operator authority but one of scope permission, identity binding, credential availability, environmental reachability, mechanism availability, dependency availability, grammar, effect constraint, or policy authorization?
```

## Preserved Unknowns

- Whether additional repositories, mirrors, forks, generated artifacts, or canonical/reference repositories exist beyond reviewed local evidence.
- Whether peer-Seed communication has any implemented local owner beyond external testimony/admissibility-adjacent boundaries.
- Whether external identity binding and credential availability have a first-class current artifact outside legacy/provider handoff boundaries.
- Whether policy authorization after warrant has a current implementation-backed owner or remains deliberately outside core execution.
- Whether a future characterization should split “access relationship” into multiple owners rather than one projection.
- Whether any environment-specific credential, Docker, sudo, network, or service endpoint is actually reachable in a particular run.

## Confidence

Medium-high for the constitutional unit and topology: multiple implementation artifacts independently refuse to equate authority, reachability, realization, warrant, authorization, and execution. Medium for external identity/peer specifics because current reviewed evidence is stronger for testimony and provider boundaries than for peer-Seed protocol implementation.

## Final answer

Across current repository evidence, the constitutional unit of access is not a target, permission, mechanism, boundary, path, or authority class by itself. The constitutional unit of access is an exact bounded relationship:

```text
subject requests activity on target within exact scope
across a boundary/path,
under a required authority class,
with observed State,
identity/credential conditions,
permitted and prohibited effects,
environmental reachability basis and blockers,
and later realization-specific authorization still explicit.
```

Access is therefore the relationship among subject, activity, target, scope, authority, State, identity/credential, boundary/path, reachability, and effects for one bounded inquiry.

Constitutional access topology audit complete.
