# Frontier Pressure Admission Outward Scout 005

## Scope

This scout moved outward from the exhausted `seed_runtime/pressure_audit.py` pocket after District Scout 004. It is read-only with respect to implementation and tests.

No implementation files were changed. No test files were changed. No slice report was created. No PR metadata was created. This scout report is the only intended repository change.

## Commands used

```bash
pwd && find .. -name AGENTS.md -print && git status --short
cat AGENTS.md && rg -n "District Scout|Scout 004|Slice 062|frontier_pressure|pressure" -S . --glob '!*.pyc' --glob '!__pycache__/*'
rg -n "Slice 062|Scout 004|District Scout 004|frontier_pressure_admission_outward|frontier_pressure_admission_slice_062" -S --glob '*.md'
sed -n '1,240p' frontier_pressure_admission_district_scout_004.md && sed -n '1,130p' frontier_pressure_admission_slice_062.md
find seed_runtime tests -maxdepth 2 -type f | sort | sed -n '1,220p'
python scripts/seed_local.py --pressure-audit --json | python -m json.tool | head -160
python scripts/seed_local.py --reasoning-path-audit --json | python -m json.tool | head -220
sed -n '1,420p' seed_runtime/pressure_audit.py && sed -n '1,260p' seed_runtime/consumer_dependency_audit.py && sed -n '1,240p' seed_runtime/operational_story.py
sed -n '240,520p' seed_runtime/operational_story.py && sed -n '1,360p' seed_runtime/reasoning_path_audit.py && sed -n '1,260p' seed_runtime/investigation_path_audit.py
rg -n "operational_story|reasoning_path|investigation_path|consumer_audit" frontier_pressure_admission_slice_*.md frontier_pressure_admission_district_scout_*.md
nl -ba seed_runtime/operational_story.py | sed -n '80,360p'; nl -ba seed_runtime/reasoning_path_audit.py | sed -n '70,240p'; nl -ba seed_runtime/investigation_path_audit.py | sed -n '20,130p'; nl -ba seed_runtime/consumer_dependency_audit.py | sed -n '45,190p'
git status --short
git add frontier_pressure_admission_outward_scout_005.md && git commit -m "Add Frontier Pressure Admission outward scout 005"
git rev-parse HEAD
```

The attempted `--reasoning-path-audit` command failed because the app exposes `--reasoning-path DOMAIN SUBJECT`, not `--reasoning-path-audit`. This did not modify repository files.

## Current app evidence

The current `seed --pressure-audit --json` output still reports only the two consumer-predicate pressure categories:

- `Orphaned Predicates`, score `26`, recommended command `seed --consumer-audit`.
- `Fragile Predicates`, score `13`, recommended command `seed --consumer-audit`.

That app evidence points outward from pressure-audit into consumer evidence, operational story consumers, investigation-path declarations, and reasoning-path composition. It does not by itself authorize more local pressure-audit slicing.

## Stopped and exhausted neighborhoods respected

- **Slice 035:** `selection_path_audit` neighborhood remains exhausted. This scout did not inspect it for new targets and recommends no selection-path work.
- **Slice 051:** immediate diagnostic-shape pressure candidate-construction pocket remains exhausted. This scout recommends no diagnostic-shape candidate shell, reason, command, label, evidence, score, or local construction extraction.
- **District Scout 004:** immediate post-Slice-062 `pressure_audit` neighborhood remains exhausted. This scout did not continue mining pressure-audit candidate producers and treats local candidate shells, category labels, reason text, command text, and presentation formatting as rejected unless a new implementation-backed producer/consumer boundary appears outside that pocket.

## Recently consumed boundaries treated as unavailable

The following boundaries remain consumed and unavailable:

- capability pressure score production;
- capability pressure positive-finding refusal;
- orphaned-predicate pressure score production;
- orphaned-predicate positive-finding refusal;
- fragile-predicate pressure score production;
- fragile-predicate positive-finding refusal;
- ownership-pressure positive-finding refusal;
- ownership-discrepancy conflicted-row selection;
- orphaned-predicate item-set selection;
- fragile-predicate item-set selection.

The scout also rejects pressure-audit candidate-shell literals, category labels, reason text, command text, and presentation formatting as local re-slice material.

## Inspected outward neighborhoods

### 1. Operational-story pressure consumer neighborhood

Rank: **B. Possible but needs caution**

`build_operational_story(...)` is a real outward consumer of pressure-audit results. It builds pressure, capability, privilege, correlation, impact, selects `primary = pressure_audit.pressures[0] if pressure_audit.pressures else None`, then builds an investigation path from `_domain_for(primary)`. It then passes `primary`, source families, investigation surfaces, and `has_pressures` into `_compose_operational_story_payloads(...)`.

Current implementation already separates answer, reasoning, supporting-evidence, boundary, and limitations payloads. Inside `_compose_operational_story_payloads(...)`, the reasoning payload still constructs the investigation-path records inline from `investigation_surfaces`, while the answer payload constructs focus/pressure/capabilities/constraints/correlation/impact/recent/outcome records in the same composition function.

Potential boundary observed: **operational-story investigation-path payload preparation** from implemented `InvestigationPathStep` records into public story path dictionaries.

Classification: **Sequential**, confidence **Medium**.

Why not a re-slice: This is outside `pressure_audit.py`, outside `selection_path_audit`, and outside diagnostic-shape candidate construction. It is not score, refusal, evidence, item-set selection, or pressure candidate construction.

Why not merely a name: The implementation already has a dedicated `_OperationalStoryReasoningPayload` dataclass and a public `OperationalStory.investigation_path` field, and the payload is consumed separately when building the final story object.

Why not immediately safe: The broader `_compose_operational_story_payloads(...)` function already advertises separation of answer/reason/support/boundary/limitations. A slice would need to prove it is not just extracting an existing list comprehension from an already separated reasoning payload. It should be reassessed only if the next campaign deliberately moves into the operational-story district.

Would it still be valid without the others? **Yes**, as a possible single operational-story slice, but only after reassessment in that district.

### 2. Reasoning-path derivation composition neighborhood

Rank: **B. Possible but needs caution**

`build_reasoning_path_audit(...)` is another outward consumer. It builds ownership rows, capability needs, pressure audit, privilege discovery, and operational story, then fills five public lists: evidence, intermediate conclusions, derived conclusions, consumers, and story impact. It later packages those lists into `_DerivedConclusionPayload`, `_DerivationSupportingEvidencePayload`, and `_DerivationLineagePayload` before calling `_reasoning_path_from_payloads(...)`.

Potential boundary observed: **reasoning-path pressure consumer row production**, where pressure audit items matching subject/domain become consumer records with `surface`, `reason`, `category`, and `score`.

Classification: **Sequential**, confidence **Medium-Low**.

Why not a re-slice: This is not local pressure-audit production. It is a downstream derivation-path consumer that reads already-produced pressure items and emits reasoning-path consumer records.

Why not merely a name: There is a public `ReasoningPathAudit.consumers` field and an existing lineage payload, so the pressure-consumer record is not only a label in prose.

Why not immediately safe: The loop is one of several similar loops that append consumer/story/evidence records. Extracting only the pressure loop could be a small compatibility-preserving slice, but it may also be a piecemeal list-append extraction unless tests prove the pressure consumer record is a distinct ownership boundary. It is likely valid only after an explicit reasoning-path district scout.

Would it still be valid without the others? **Yes**, independent of operational-story and consumer-audit work, but not safe enough from this pressure-admission scout to command now.

### 3. Investigation-path declaration and inventory-validation neighborhood

Rank: **C. Already separated / likely re-slice**

`seed_runtime/investigation_path_audit.py` contains implementation-backed path declarations. `build_investigation_path_audit(...)` normalizes a domain, intersects declared surface names with registered diagnostic inventory names, assigns order, and returns known domains. This is an outward neighborhood because operational story consumes it through `_domain_for(primary)`.

No safe candidate found. The local responsibilities are already compact and directly named: declarations live in `_INVESTIGATION_PATHS`, known-domain projection is a helper, and `build_investigation_path_audit(...)` owns normalization, inventory filtering, and step construction. Pulling out consumer-domain path declarations, pressure-domain path declarations, or step tuple construction would be declaration formatting or re-slicing inventory validation.

Classification: **Invalid**, confidence **High**.

Would it still be valid without the others? **No**. It lacks a still-compressed single ownership boundary.

### 4. Consumer dependency audit item-source and filter neighborhood

Rank: **B. Possible but needs caution**

The app pressure output recommends `seed --consumer-audit`, so the next outward source neighborhood is `seed_runtime/consumer_dependency_audit.py`. `build_consumer_audit(...)` reads source files once, optionally builds observation-predicate items when `diagnostic_filter is None`, optionally builds diagnostic items when `predicate_filter is None`, sorts the combined items, and attaches metadata. `_audit_item(...)` separately owns lookup-term construction and source consumer matching.

Potential boundary observed: **consumer-audit observation-predicate item production under predicate filters**. It consumes `build_observation_inventory(repo_root, predicate_filter=predicate_filter)` and emits `ConsumerAuditItem` rows of kind `observation_predicate` before diagnostic rows are considered.

Classification: **Sequential**, confidence **Medium**.

Why not a re-slice: It is upstream of pressure-audit and distinct from Slice 037 source fan-out. Slice 037 recovered the handoff from pressure-audit to one `ConsumerAudit`; this possible target would live inside the consumer-audit surface itself and would own one category of audited items.

Why not merely a name: The implementation produces concrete `ConsumerAuditItem` records with a public `kind`, and pressure-audit consumes observation-predicate items specifically when generating orphaned/fragile pressure.

Why not immediately safe: This may belong to a **different district**: consumer dependency audit, not Frontier Pressure Admission. It also risks expanding the campaign from admission pressure into consumer-audit internals. A separate district handoff should validate whether consumer-audit item-family production has not already been recovered elsewhere.

Would it still be valid without the others? **Yes**, as a possible consumer-audit district slice; **not** as a direct next Frontier Pressure Admission slice without handoff.

### 5. Consumer-audit presentation neighborhood

Rank: **D. Cosmetic only**

`format_consumer_audit(...)` prints summary counts, per-item identity, consumers, counts, orphan status, and highlight. This is adjacent because pressure-audit recommends the consumer-audit CLI, but the implementation evidence is presentation only. Extracting summary lines, item sections, consumer lines, or highlight display would be formatting cleanup rather than Frontier Pressure Admission recovery.

Classification: **Invalid**, confidence **High**.

Would it still be valid without the others? **No**. It is cosmetic presentation material and not a compressed implementation-local ownership boundary for pressure admission.

## Candidate boundaries found

How many recoverable candidates currently exist?

**0 immediate Frontier Pressure Admission candidates.**

The scout found **three possible outward district candidates**, but all require reassessment in their own neighborhoods before implementation. They do not justify an efficiency batch or protection batch under the current Frontier Pressure Admission command.

| Rank | Candidate | Classification | Confidence | Still valid without others? | Why it is not a re-slice | Why it is not merely a name | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B | Operational-story investigation-path payload preparation | Sequential | Medium | Yes, if reassessed in operational-story district | Outside pressure-audit, selection-path, diagnostic-shape, and consumed score/refusal/item-selection work | Existing reasoning payload and public `investigation_path` field provide a concrete artifact/consumer | Do not batch now; reassess as operational-story district slice |
| B | Reasoning-path pressure consumer record production | Sequential | Medium-Low | Yes, if reassessed in reasoning-path district | Downstream consumer of pressure items, not pressure-item production | Public `consumers` field and lineage payload consume concrete records | Do not batch now; reassess as reasoning-path district slice |
| B | Consumer-audit observation-predicate item production | Sequential | Medium | Yes, if reassessed in consumer-audit district | Upstream source surface, distinct from Slice 037 pressure-audit fan-out | Produces concrete `ConsumerAuditItem(kind="observation_predicate")` rows consumed by pressure-audit | Different-district handoff; not current campaign batch |
| C | Investigation-path declaration splitting | Invalid | High | No | Would split already declared path table / inventory validation | Mostly declaration formatting and tuple construction | Reject |
| D | Consumer-audit presentation sections | Invalid | High | No | Presentation only; no admission owner | Line formatting only | Reject |

## Candidate independence classification

- **Operational-story investigation-path payload preparation**: **Sequential**, confidence **Medium**. It is independent from the other two possible candidates, but only after an operational-story scout proves this is not just extracting a list comprehension from an already separated reasoning payload. It is not a re-slice because it does not touch the pressure-audit pocket or prior consumed pressure boundaries. It is not merely a name because the payload feeds the public story `investigation_path` field.
- **Reasoning-path pressure consumer record production**: **Sequential**, confidence **Medium-Low**. It is independent from operational-story payload preparation and consumer-audit item production, but it should be reassessed in the reasoning-path district. It is not a re-slice because it consumes pressure output rather than producing/admitting it. It is not merely a name because it emits concrete public consumer records.
- **Consumer-audit observation-predicate item production**: **Sequential**, confidence **Medium**. It is independent from the downstream story/reasoning candidates, but it changes district ownership from Frontier Pressure Admission to consumer dependency audit. It is not a re-slice of Slice 037 because Slice 037 only recovered pressure-audit's single consumer-audit source handoff/fan-out. It is not merely a name because it produces concrete item rows with a public kind and downstream pressure consumers.

Fewer than three implementation-backed **current-campaign** candidates are supported. There are zero immediate recoverable Frontier Pressure Admission candidates. The three possible outward candidates are handoff candidates, not a safe batch queue.

## Rejected candidates and why

- **More pressure-audit local helpers**: rejected by District Scout 004 and this scout. Remaining local material is candidate shell assembly, reason/command/category text, already separated source orchestration, or presentation formatting.
- **Selection-path audit work**: rejected by Slice 035 stop marker.
- **Diagnostic-shape pressure candidate construction**: rejected by Slice 051 stop marker.
- **Orphaned/fragile item selection, score, refusal, and evidence**: rejected as recently consumed or already separated.
- **Investigation-path table splitting**: rejected as already separated declaration data and validation flow.
- **Consumer-audit formatting**: rejected as cosmetic presentation.

## Batch Efficiency Gate

Current queue classification: **Move to a different district / stop for Frontier Pressure Admission**.

- Recoverable candidates currently existing in the Frontier Pressure Admission pressure-audit district: **0**.
- Efficiency batch: **No**. Three immediate safe Frontier Pressure Admission candidates do not exist.
- Protection batch: **No**. Two immediate safe Frontier Pressure Admission candidates do not exist.
- Single-slice target: **No**. One immediate safe Frontier Pressure Admission candidate does not exist.
- Stop/move-out: **Yes** for the broader Frontier Pressure Admission district.
- Different-district handoff: **Yes**. If work continues, open a new scout in one of the outward districts: operational story, reasoning path, or consumer dependency audit.

Because the outward queue contains only sequential handoff candidates, running a batch now is not worth it for speed or process protection. A batch would blur district ownership and create re-slicing risk. Recommended batch size: **0**.

## Recommended next command

Recommended next command: **different-district handoff**, not a Frontier Pressure Admission slice.

Suggested wording:

```text
Perform a read-only district scout in the consumer dependency audit district, starting from `seed --consumer-audit` as the current pressure-audit recommended command. Do not modify implementation or tests. Determine whether consumer-audit observation-predicate item production, diagnostic item production, or source-consumer matching contains a recoverable implementation-local ownership boundary distinct from prior Frontier Pressure Admission Slice 037.
```

Alternative handoff if the operator wants to follow downstream consumers instead of source evidence:

```text
Perform a read-only district scout in the operational-story/reasoning-path district, starting from pressure-audit consumption. Determine whether operational-story investigation-path payload preparation or reasoning-path pressure consumer record production is a real ownership boundary rather than presentation/list-comprehension extraction.
```

## Risk of re-slicing prior work

Risk is **high** if the next command remains in `seed_runtime/pressure_audit.py` or names pressure-audit candidate shells. The remaining local pressure-audit material is already classified as exhausted, consumed, cosmetic, or source orchestration.

Risk is **medium** if the next command moves into operational-story or reasoning-path code without a district scout, because those modules already contain payload helpers and public surfaces; a slice could accidentally extract an already-separated payload fragment.

Risk is **lower but still present** for a consumer dependency audit district scout, because the current live app evidence recommends `seed --consumer-audit` and pressure-audit consumes observation-predicate item rows. That is the clearest outward implementation-backed handoff, but it is a different district and should be treated as such.

## Final scout statement

No implementation files were changed. No test files were changed. No slice report was created. No PR metadata was created. This scout report is the only repository file intentionally added.

Scout report commit hash: `7413ac03c7d9c85e9636f00bf553fa38a259ce57`.
