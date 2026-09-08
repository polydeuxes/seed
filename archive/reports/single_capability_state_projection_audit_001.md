# Single-Capability State Projection Audit 001

## 1. Bounded question

What existing read-only artifacts are sufficient to distinguish, for one capability name, its requested, catalog-known, provider-recommended, operation-registered, candidate-supported, verification-evidence, verified, stale, and Unknown states without introducing capability dependencies, realization selection, promotion, or execution?

This audit is topology-only. It does not implement a projection, add dependency edges, select a provider or operation, verify any capability, authorize execution, execute tools, or modify runtime/catalog/registry behavior.

## 2. Selected capability and selection evidence

Selected capability: `web_search`.

Candidates considered:

- `web_search`: checked-in catalog entry with provider recommendations; inventory tests demonstrate registered-operation universe contribution, verified state through `capability_verified`, evidence support, and stale state through expired fact semantics.
- `weather_lookup`: checked-in catalog entry with provider recommendations and request examples; tests demonstrate provider-reported inventory state, but not stale state for that name and not candidate or verification-evidence acquisition.
- `service_management`: strong request/catalog/provider recommendation coverage and policy/action-plan surfaces, but weaker direct `capability_verified`/stale evidence in the focused capability inventory neighborhood.
- `ssh_client`, `python_runtime`, `git_client`, `http_client`, `docker_client`: strong candidate and verification-evidence coverage, but no checked-in catalog entry or provider recommendation under the same capability string.

`web_search` provides the strongest implementation evidence across the requested surface list because the same capability string appears in catalog metadata/provider recommendations, registered `ToolSpec` inventory tests, capability inventory, `capability_verified` fact support, evidence summaries, and stale expiration behavior. Expected surfaces absent for `web_search`: capability candidate inspection and verification-evidence acquisition, because those implementations currently derive candidates only from observed package facts mapped to `ssh_client`, `python_runtime`, `docker_client`, `git_client`, and `http_client`.

## 3. Methodology

Read-only repository inspection was used. I ran focused `rg` probes for capability classes/surfaces and for `web_search`, then inspected implementation bodies and focused tests in the capability catalog, registry, tool needs, candidate, verification-evidence, verification-inspection, inventory, state projection, and CLI formatting neighborhoods. I did not run mutating Seed CLI surfaces, emit events outside test inspection, alter an event ledger, or execute operational tools.

## 4. Inspected neighborhoods

- `capability_catalog/web_search.yml`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/registry.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/capabilities.py`
- `seed_runtime/state.py`
- `scripts/seed_local.py`
- `tests/test_capability_catalog.py`
- `tests/test_capability_inventory.py`
- focused search output for related tests

## 5. Terminology

- Requested: a `ToolNeed.capability` names demand only.
- Catalog-known: `CapabilityCatalog` metadata exists for a normalized key.
- Provider recommendation: catalog/advisory provider, backend, operation, or handoff metadata.
- Registered operation label: `ToolSpec.capabilities` or fallback tool name contributes operation-contract metadata only.
- Capability candidate: package-derived possible capability, explicitly not proof.
- Verification evidence: observed local support, such as executable path, explicitly not verification.
- Verified: current supported `capability_verified` fact interpreted by inventory semantics.
- Stale: expired verification fact support interpreted by existing fact freshness semantics.
- Unknown: no stronger state supported; must not be rewritten as false or unavailable.

## 6. Artifact inventory

| Surface | `web_search` present? | Evidence | Claim |
| --- | --- | --- | --- |
| ToolNeed/request | Indirectly supported; no focused `web_search` ToolNeed fixture found | `ToolNeedService.create_from_decision` slugifies requested capability; inventory universe includes all `ToolNeed.capability` values | Demand only when present |
| CapabilityCatalog | Yes | `capability_catalog/web_search.yml` | Known catalog metadata |
| Provider recommendation | Yes | `tavily`, `brave_search` in catalog entry | Advisory recommendation only |
| ToolSpec capabilities/registry | Yes in tests via fallback tool name and inventory state | `_tool("web_search")` registers a `ToolSpec` with no explicit capabilities; inventory uses `tool.capabilities or [tool.name]` | Registered operation association only |
| Capability candidate | No | candidate package map excludes `web_search` | Absence preserved as no candidate evidence, not false capability |
| Verification evidence acquisition | No | binary candidate map excludes `web_search` | No local binary-path evidence derivable by this owner |
| Capability inventory | Yes | inventory tests assert `web_search` unverified/verified/stale states | Presentation of verification status from existing state |
| `capability_verified` support | Yes | tests create `Fact(subject_id="web_search", predicate="capability_verified")` | Verification authority when current; stale when expired |

## 7. Producer/artifact/consumer table

| Occurrence | Producer | Artifact | Consumer | Triggering evidence | Exact claim | Claim explicitly refused | Provenance | Freshness | Scope | Authority | Read-only/mutating | Event-ledger behavior | Absence preserved | Unknown preserved | LLM-free |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Catalog metadata | Checked-in YAML loader | `CapabilityCatalogEntry(capability="web_search")` | `CapabilityCatalog.get/recommend_for`, runtime/tool-need resolution | `capability_catalog/web_search.yml` | `web_search` is a known catalog key with summary | Does not execute, register, verify, or authorize | Repository file | Static until file changes | Catalog | Metadata owner | Read-only load | None | Missing entry returns `None`/`[]` | Unknown catalog key remains no entry | Yes |
| Provider recommendations | Checked-in YAML loader | `CapabilityRecommendation` records for `tavily`, `brave_search` | Catalog recommendation consumers and handoff payloads | Recommendation list in catalog file | Providers/backends may be suggested | Not provider selection, not credential proof, not verification | Repository file | Static until file changes | Catalog/handoff metadata | Advisory metadata | Read-only | None | Empty list if none | No recommendation does not mean impossible | Yes |
| ToolNeed request | `ToolNeedService.create_from_decision` or projected events | `ToolNeed.capability` | state projection, inventory universe, tool-need resolution | request_tool decision payload | Demand/request exists | Not verification, not registration, not execution | Event payload | Current while need in projected state | Workspace | Request owner | Creation mutates ledger; inspection is read-only | `tool_need.created` on creation | No need means no demand artifact | Unknown demand is preserved by absence | Yes after event exists |
| Registered operation association | `tool.registered` event / manifest loader | `ToolSpec` with `name`/`capabilities` | `ToolRegistry.list_tools_for_capability`, inventory universe | ToolSpec labels; tests use `_tool("web_search")` | Operation contract claims association | Not availability, verification, authorization, or execution | Manifest or event | Current projected registered state | Registry/workspace | Registry/operation contract | Registration mutates ledger; listing is read-only | `tool.registered` when registered | No matching tool means no registered operation | Unknown stays no operation association | Yes |
| Candidate inspection | `build_capability_candidates` | `CapabilityCandidateInspection` | verification evidence, verification inspection, CLI | package_installed facts mapped by package table | Package fact supports possible candidate | Not capability proof, permission, selection, policy, or execution | Projected package facts | Current fact projection | State inspection | Candidate-preservation owner | Read-only | None | No mapped package => no candidate | Unknown preserved by no candidate | Yes |
| Verification evidence | `build_verification_evidence` | `VerificationEvidenceInspection` | verification inspection, promotion readiness | candidate plus PATH executable metadata | Observed binary path may support checking | Not verification, selection, permission, policy, execution | Local PATH metadata | Moment of inspection only | Local process environment | Evidence-acquisition owner | Read-only filesystem metadata | None | No binary => no evidence | Unknown preserved by no evidence | Yes |
| Capability inventory | `build_capability_inventory` | `CapabilityInventoryEntry` | CLI formatting, integrity summary, verification inspection | union of registered labels, requests, and verification fact subjects | Verification state presentation | Does not own admission, execute, schedule, route, or create facts | Projected State | Uses fact expiry semantics and `now` | Projected state | Inventory presentation | Read-only | None | Missing `capability_verified` => `unverified` reason, not absence-as-false outside inventory universe | Unknown fact values map to `unknown` | Yes |
| Verification fact support | Observation/fact projection | `Fact`/`FactSupport` with predicate `capability_verified` | inventory and verification inspection | `fact.observed` carrying subject `web_search` | Verification support according to predicate/value/freshness | Not selection, authorization, execution, or tool invocation | Evidence IDs and fact source | `expires_at`/expired fact semantics | Projected facts | Fact owner | Fact append mutates ledger; consumption read-only | `fact.observed` when created | No fact means no verification support | Unknown value maps to inventory `unknown` | Yes after fact exists |

## 8. Capability-state topology

Implementation-backed topology for `web_search`:

```text
request_tool decision payload / tool_need.created event
→ ToolNeed.capability == "web_search"
→ capability inventory requested-capability universe

capability_catalog/web_search.yml
→ CapabilityCatalogEntry("web_search")
→ CapabilityRecommendation(provider="tavily")
→ CapabilityRecommendation(provider="brave_search")

ToolSpec name/capabilities in registered tool state
→ _registered_operation_contract_capabilities
→ capability inventory universe / ToolRegistry capability lookup

fact.observed: Fact(subject_id="web_search", predicate="capability_verified")
→ State FactSupport
→ build_capability_inventory
→ CapabilityInventoryEntry(state="verified" or "stale" or "unknown" by value/freshness)
```

Disconnected branches that are only correlated by text for this capability:

```text
package_installed facts
→ build_capability_candidates
(no web_search mapping)

CapabilityCandidateInspection
→ build_verification_evidence PATH binary inspection
(no web_search binary mapping)
```

No edge is warranted from catalog/provider recommendation to verification, from registry to verification, from binary reachability to verification, or from request to execution.

## 9. Identity and correlation analysis

`web_search` can be correlated by normalized capability string in some surfaces, but not by one repository-wide capability identity object.

- Catalog keys are normalized with `slugify` during `CapabilityCatalog` load/get.
- ToolNeed capabilities are slugified in `ToolNeedService.create_from_decision`.
- ToolSpec manifest capabilities are normalized by `normalize_capabilities`; inventory also uses `tool.capabilities or [tool.name]`, so a fallback tool-name label can enter the capability universe without passing through an explicit capability field in that test helper.
- Candidate filters lower/replace hyphens and use an alias map; their candidate universe is a local package mapping and does not include `web_search`.
- Verification evidence uses local candidate strings from the candidate inspection and a separate binary-name map.
- Verification facts use `Fact.subject_id` text. Inventory matches `capability` to `FactSupport` by subject/predicate.

Correlation options:

| Identifier | Available for `web_search`? | Audit result |
| --- | --- | --- |
| Normalized capability name | Yes | Main join mechanism, but local meanings differ |
| Subject identity | Yes for `capability_verified` facts only | Not shared by catalog/registry/request as a typed identity |
| Event ID | Yes for created/registered/fact events individually | Not a cross-surface capability identity |
| Fact ID | Yes for verification support | Verification-local only |
| Evidence ID | Yes for verification fact evidence | Verification-local only |
| Provider ID | Yes for recommendations (`tavily`, `brave_search`) | Recommendation-local only |
| Operation name | Yes for registered operations | Registry-local only |
| Catalog key | Yes | Catalog-local normalized key |
| Other stable identifier | No repository-wide one found | Matching strings with local meanings |

Answer: the repository does not have one stable capability identity across these surfaces; it has matching normalized strings with local meanings and local owners. That is sufficient for a careful read-only composition if the projection preserves provenance and refuses promotion.

## 10. Requested-state evidence

`ToolNeedService.create_from_decision` reads `decision.tool_need`, slugifies `name` and `capability`, and appends `tool_need.created` if no open need already matches the name or capability. This proves request/demand only. `build_capability_inventory` includes requested capabilities by collecting `need.capability` from projected `state.tool_needs`.

For `web_search`, no focused fixture was found that creates a `ToolNeed(capability="web_search")`; therefore the audit treats requested state as structurally supported but not currently instantiated in focused evidence for this selected capability.

## 11. Catalog-state evidence

`capability_catalog/web_search.yml` declares `capability: web_search` with a summary for public web search. `CapabilityCatalog.load` loads checked-in `*.yml` entries and stores them under `slugify(entry.capability)`. `CapabilityCatalog.get` returns the entry by slugified capability, and `recommend_for` returns recommendations only when the requested capability matches an entry.

Claim: catalog-known metadata exists. Refused claim: catalog metadata does not prove registered operation, provider availability, verification, authorization, or execution.

## 12. Provider-recommendation evidence

The `web_search` catalog entry recommends:

- provider `tavily`, kind `hosted_api`, backend type `mcp`, operation `web.search`, risk `L2`, with notes that API credentials and explicit tool registration are required.
- provider `brave_search`, kind `hosted_api`, backend type `mcp`, operation `web.search`, risk `L2`, with notes that API credentials and explicit tool registration are required.

These recommendations are advisory catalog metadata. They are not provider selection, credential proof, operation selection, verification, or execution authority.

## 13. Registration evidence

Focused inventory tests append a `tool.registered` event containing `_tool("web_search")`. The helper creates a `ToolSpec` named `web_search` with empty `capabilities` by default. Inventory derives registered operation contract capability labels using `tool.capabilities or [tool.name]`, which means this registration widens the inventory universe to include `web_search` even without explicit `ToolSpec.capabilities` content.

This proves only operation-contract association. The implementation explicitly states registered operation contract capabilities are not observed evidence that the capability is present, available, verified, authorized, or callable.

## 14. Candidate evidence

No `web_search` candidate evidence exists in current candidate inspection. `_PACKAGE_CAPABILITY_CANDIDATES` maps observed packages only to `ssh_client`, `python_runtime`, `docker_client`, `git_client`, and `http_client`. Therefore candidate-supported state for `web_search` is Unknown/absent, not false capability, not unavailable capability, and not a negative verification result.

## 15. Verification evidence

No verification-evidence acquisition exists for `web_search` through `build_verification_evidence`. `_CAPABILITY_BINARY_CANDIDATES` maps only `ssh_client`, `python_runtime`, `docker_client`, `git_client`, and `http_client` to binary names. Since the candidate universe excludes `web_search`, the PATH binary inspector cannot honestly populate `verification_evidence` for this capability.

Separate from acquired local binary evidence, capability inventory tests create provider-report evidence records linked to `capability_verified` facts for `web_search`. Those evidence summaries support the verification fact; they are not the same owner as verification-evidence acquisition.

## 16. Verified/stale/Unknown evidence

`build_capability_inventory` derives verification state from `capability_verified` `FactSupport` only. For `web_search`, tests demonstrate:

- `unverified`: registered tool present but no `capability_verified` fact.
- `verified`: `Fact(subject_id="web_search", predicate="capability_verified", value="verified")` with evidence ID `evd_web_search`.
- `stale`: the same verification fact pattern with expired `expires_at` uses existing expired fact semantics and yields state `stale`.
- `unknown`: implementation maps unrecognized `capability_verified` values to `unknown`, although the focused `web_search` tests do not instantiate an unknown-valued fact.

Freshness/staleness is established by `Fact.expires_at`, `is_fact_expired`, `State.get_fact_supports(... include_expired=...)`, and inventory's `_support_is_expired` path.

## 17. Authority distinctions

- Request authority owns demand, not capability truth.
- Catalog authority owns metadata/recommendations, not provider selection or verification.
- Registry authority owns operation-contract labels, not capability availability.
- Candidate authority owns evidence-derived possibilities, not proof.
- Verification-evidence authority owns observed local support, not verification.
- Fact/inventory authority interprets `capability_verified` support and freshness, not execution permission.
- Policy/execution authority is adjacent and not part of the capability state audited here.

## 18. Projection-field feasibility table

| Field | Classification | Reason |
| --- | --- | --- |
| `capability_name` | Directly available | Normalized string exists as catalog key, request capability, registered label, and fact subject |
| `requested` | Derivable without authority creation | State contains `ToolNeed.capability`; for selected capability no focused fixture currently requests it |
| `catalog_known` | Directly available | `CapabilityCatalog.get("web_search")` |
| `provider_recommendations` | Directly available | Catalog recommendation records |
| `registered_operations` | Derivable without authority creation | Registry/state ToolSpec labels and fallback name labels |
| `candidate_evidence` | Directly available as empty/absent | Candidate inspection can be filtered; no `web_search` mapping |
| `verification_evidence` | Directly available as empty/absent for acquisition; derivable separately for fact evidence summaries | Must keep binary-path acquisition separate from fact support evidence |
| `verification_status` | Directly available when in inventory universe | Inventory returns unverified/verified/stale/provider_reported/unknown |
| `verification_support` | Directly available when facts exist | Inventory exposes supporting fact IDs/evidence summaries/support summary |
| `freshness` | Directly available for fact support | `observed_at`, `latest_observed_at`, `expires_at`, `expired`, `age_seconds` |
| `unknowns` | Derivable without authority creation | Absences and unknown fact values can be preserved with provenance |
| `boundary_notes` | Directly available/derivable | Existing modules expose notes and docstrings; projection would need to carry them without creating authority |

Fields that cannot currently be populated honestly for `web_search`: package-derived `candidate_evidence`, PATH-derived `verification_evidence`, a single cross-surface capability identity ID, selected provider, selected operation, authorization status, execution status, credential availability, and runtime reachability.

## 19. Strongest counterevidence

Strongest evidence that an existing artifact intentionally spans several states is `build_capability_inventory`: its universe is the union of registered tools, ToolNeeds, and verification fact subjects, and it emits a single `CapabilityInventoryEntry` state. However, the implementation explicitly separates admitted capability state from executable operation contract state and requested capabilities, and it derives verification state only from `capability_verified` facts and fact freshness. Thus it is a presentation/inventory surface, not a complete projection of requested/catalog/provider/candidate/verification-evidence states.

Strongest evidence against a stable identity is that each owner normalizes or interprets strings locally: catalog uses slugified keys, registry normalizes manifest capabilities but inventory may fall back to tool names, candidate inspection has its own alias map and package-derived candidate namespace, verification evidence has a separate binary map, and `capability_verified` facts use subject IDs. A composed projection could misrepresent local meanings if it pretended these were one typed identity rather than same-string correlations.

No evidence found that registration is intended as capability proof; comments say the opposite. No evidence found that provider recommendation is realization selection; catalog notes require credentials and explicit registration. No evidence found that binary reachability is intended as verification; verification-evidence notes say it is not. No evidence found that `capability_verified` facts are unnecessary; inventory and verification inspection rely on them.

## 20. Preserved Unknowns

- No `web_search` ToolNeed fixture found: requested state is not asserted for the selected capability.
- No `web_search` candidate package mapping: candidate-supported state remains absent/Unknown.
- No `web_search` PATH binary mapping: verification-evidence acquisition remains absent/Unknown.
- No single identity object: cross-surface identity remains matching-string correlation.
- No provider credentials, endpoint availability, authorization, or execution result is represented by catalog recommendation.
- No registered operation proof of runtime availability is inferred from `ToolSpec` registration.

## 21. Supported conclusions

1. `web_search` is catalog-known.
2. `web_search` has provider recommendations for `tavily` and `brave_search`.
3. Registered operation labels can widen the visible capability universe without verification.
4. `web_search` can be represented as unverified, verified, and stale in capability inventory depending on `capability_verified` fact support and freshness.
5. Candidate evidence and verification-evidence acquisition remain non-authoritative and, for `web_search`, absent.
6. A future read-only projection could compose existing artifacts if it reports provenance, owner, freshness, and boundary notes and refuses promotion.

## 22. Unsupported conclusions

- `web_search` is executable.
- `web_search` is authorized.
- `tavily` or `brave_search` is selected.
- Any credentials or integration exist.
- Registration proves capability availability.
- Catalog recommendation proves provider reachability.
- Candidate absence proves capability unavailability.
- Binary/path absence proves capability false.
- One stable capability identity exists beyond matching normalized strings.

## 23. Classification

B. Existing artifacts can be composed into a truthful read-only single-capability projection without new capability authority.

## 24. Implementation-warrant decision

One bounded implementation slice is warranted.

## 25. Exact next bounded boundary

- Producer: read-only composer over `State`, `CapabilityCatalog`, `ToolRegistry`/registered `ToolSpec` state, capability candidate inspection, verification-evidence inspection, and capability inventory.
- Proposed read-only artifact: single-capability state projection for one supplied normalized capability string.
- Consumer: diagnostic/operator inspection only.
- Exact fields supported by current evidence: `capability_name`, `requested`, `catalog_known`, `provider_recommendations`, `registered_operations`, `candidate_evidence`, `verification_evidence`, `verification_status`, `verification_support`, `freshness`, `unknowns`, `boundary_notes`.
- Fields explicitly excluded: dependencies, provider selection, operation selection, capability verification/promotion, authorization, execution, credential availability, endpoint reachability, binary invocation, cluster mutation.
- Exact bounded question: for one capability string, show which existing read-only surfaces mention or derive the string, what each surface claims, what it refuses, and which states remain Unknown.

## 26. Files changed

- Added `single_capability_state_projection_audit_001.md` only.

## 27. Probes/tests executed

Read-only probes/checks executed during the audit:

```bash
pwd && find .. -name AGENTS.md -print && git status --short
cat AGENTS.md && git status --short
rg -n "ToolNeed|CapabilityCatalog|capability_verified|CapabilityInventory|CapabilityCandidate|VerificationEvidence|ToolSpec" seed_runtime scripts tests
find capability_catalog -maxdepth 2 -type f -print -exec sed -n '1,160p' {} \;
sed -n '100,150p' seed_runtime/registry.py; sed -n '880,930p' scripts/seed_local.py; sed -n '1,260p' seed_runtime/capability_candidates.py; sed -n '1,220p' seed_runtime/verification_evidence.py; sed -n '1,310p' seed_runtime/capability_inventory.py
sed -n '310,380p' seed_runtime/capability_inventory.py; sed -n '1,220p' seed_runtime/capability_verification.py; sed -n '1,230p' seed_runtime/capability_catalog.py; sed -n '1,220p' seed_runtime/tool_needs.py
rg -n "docker_client|python_runtime|git_client|http_client|ssh_client|weather_lookup|docker_inspection|service_management|web_search" seed_runtime scripts tests capability_catalog -g '*.py' -g '*.yml' -g '*.md'
rg -n "web_search" seed_runtime scripts tests . -g '*.md'
rg -n "web_search" seed_runtime scripts tests capability_catalog -g '*.py' -g '*.yml' -g '*.md'
sed -n '1,190p' tests/test_capability_inventory.py; sed -n '1,90p' tests/test_capability_catalog.py; sed -n '1,80p' seed_runtime/capabilities.py
```

The required selected-capability search was also run in its literal `-g '*.md'` form; it returned no hits because current `web_search` evidence is in YAML/Python, not Markdown. The expanded focused search included Python/YAML/Markdown and found the selected capability evidence listed above.

## 28. Confidence statement

Confidence: moderate-high. The audit inspected the focused implementation neighborhoods that own request, catalog, provider recommendation, registry labels, candidate preservation, verification-evidence acquisition, capability inventory, and verification fact interpretation. The main uncertainty is not about current behavior but about representativeness: `web_search` best covers catalog/provider/registry/inventory/verified/stale surfaces, while candidate and binary verification-evidence surfaces are better represented by other capability strings that lack catalog/provider coverage. This supports composition with explicit Unknown preservation, not a claim of one unified capability identity.

## Required questions answered

1. Selected capability: `web_search`.
2. It was selected because it spans catalog, provider recommendation, registered operation inventory, `capability_verified` fact support, evidence summaries, verified state, and stale state better than the other considered names.
3. It is structurally requestable through `ToolNeed.capability`; no focused `web_search` ToolNeed fixture was found.
4. It is catalog-known in `capability_catalog/web_search.yml`.
5. Recommended providers/backends: `tavily` and `brave_search`, both `hosted_api`/`mcp` recommendations for operation `web.search`.
6. Registered operations claiming it: focused tests register a `ToolSpec` named `web_search`; explicit `ToolSpec.capabilities` entries for `web_search` were not found.
7. Candidate evidence: none for `web_search`; package-derived candidate mappings do not include it.
8. Verification evidence: no PATH/binary acquisition evidence; inventory tests attach provider-report evidence to a `capability_verified` fact.
9. It is currently verified only when a current `capability_verified` fact for subject `web_search` exists in projected state.
10. Verification is established by `capability_verified` `FactSupport` interpreted by capability inventory.
11. It can become stale.
12. Freshness/staleness is established by fact expiry (`expires_at`, expired support, `is_fact_expired`, stale inventory path).
13. Catalog, registry, candidate, and verification surfaces are joined only by matching normalized text/local strings, not one stable identity object.
14. Yes, registration widens the visible capability universe without proving capability.
15. Yes, candidate evidence remains explicitly non-authoritative.
16. Yes, verification evidence remains explicitly non-authoritative until supported by a verification fact.
17. Yes, a capability can be requested while unverified.
18. Yes, it can be registered while unverified.
19. Yes, verification facts can name a capability subject without a registered operation.
20. Yes, it can be stale while still registered.
21. Yes, provider recommendations can exist without verification.
22. Capability inventory intentionally presents several inputs in one inventory universe, but preserves ownership distinctions and derives verification only from facts.
23. No current focused consumer was found treating catalog, candidate, registration, or binary evidence as verification; strongest risk is any reader overinterpreting inventory universe membership.
24. Yes, one read-only projection could expose supported distinctions without creating new authority.
25. It would compose existing artifacts; it would not require a new underlying capability owner if it remains read-only and provenance-preserving.
26. Unsupported fields: single stable capability identity ID, selected provider, selected operation, candidate evidence for `web_search`, binary verification evidence for `web_search`, credential availability, authorization, execution, and runtime reachability.
27. Smallest implementation boundary: one diagnostic/operator read-only composer for one supplied capability string with explicit owner/provenance/Unknown boundaries.

B. Existing artifacts can be composed into a truthful read-only single-capability projection without new capability authority.

One bounded implementation slice is warranted.
