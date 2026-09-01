# Competency Interrogation 006

## Selected competency

**Capability Inventory**.

This interrogation selects Capability Inventory because it sits immediately beside Capability Verification with a similar public appearance: both expose capability status. Their constitutional responsibilities differ. Capability Inventory presents the current capability verification inventory derived from projected state; Capability Verification inspects capability candidates against that inventory and explicitly refuses to turn verification into permission.

Repository authority wins. The selected competency is the read-only inventory implemented in `seed_runtime/capability_inventory.py`, surfaced through `seed --capability-status`, and protected by `tests/test_capability_inventory.py`.

Smallest truthful answer:
Capability Inventory can present a deterministic read-only inventory of capability verification states from projected State; it cannot admit capabilities, verify the world, select operations, or authorize execution.

## Implementation evidence reviewed

Implementation evidence reviewed:

- `seed_runtime/capability_inventory.py`
  - module purpose says capability verification is represented as projected facts and evidence;
  - module boundary says it does not execute tools, call providers, append events, schedule work, or route through Runtime behavior;
  - `_AdmittedCapabilityState` separates already-projected `capability_verified` facts from inventory presentation;
  - `_ExecutableOperationContractState` separates registered operation-contract metadata from admitted repository capability knowledge;
  - `_CapabilityInventorySources` unions admitted capabilities, executable operation contracts, and requested capabilities without collapsing ownership;
  - `build_capability_inventory()` returns deterministic entries from State only;
  - missing verification facts produce `unverified`;
  - expired verification facts produce `stale` using existing fact expiry semantics;
  - provider-reported values produce `provider_reported`;
  - support and evidence summaries preserve supporting fact and evidence provenance.
- `scripts/seed_local.py`
  - `--capability-status` is a CLI surface;
  - `format_capability_inventory()` emits deterministic JSON;
  - CLI dispatch calls `build_capability_inventory(projected_state_from_args(args))` and returns without runtime execution.
- `tests/test_capability_inventory.py`
  - inventory is read-only;
  - inventory uses no ToolExecutor or Runtime;
  - verified state derives from facts and evidence;
  - unverified state derives from missing facts;
  - stale state uses existing expired fact semantics only;
  - provider-reported state derives from fact value;
  - source helpers keep operation-contract metadata separate from admitted knowledge;
  - ordering is deterministic;
  - CLI output is read-only JSON and avoids runtime.
- Adjacent evidence from `seed_runtime/capability_verification.py` and `tests/test_capability_verification_inspection.py`
  - verification inspection consumes inventory entries but owns candidate-to-status inspection rather than inventory construction;
  - verification inspection refuses selection, permission, policy, invocation, execution, proposals, pending actions, and plans.
- App and checks run for this interrogation:
  - `python scripts/seed_local.py --help | rg -n "capability-status|capability-verification|capability-candidates|promotion-readiness"`
  - `python -m pytest -q tests/test_capability_inventory.py tests/test_capability_verification_inspection.py`

Smallest truthful answer:
The implementation supports a read-only, JSON-visible inventory of capability verification belief, not capability authority.

## Interrogation matrix

Legend:

- ✓ Answered by implementation
- ? Partially supported / unanswered but meaningful
- ○ Not applicable at current maturity
- ✗ Unsupported / unknown

### Identity

| Question | Mark | Implementation-supported answer |
| --- | --- | --- |
| What worker or implementation surface is being interrogated? | ✓ | `build_capability_inventory()`, `CapabilityInventoryEntry`, support/evidence summary dataclasses, source-separation helpers, `format_capability_inventory()`, and the `--capability-status` CLI path. |
| What competency does that worker exercise? | ✓ | Read-only presentation of capability verification inventory from projected State. |
| What constitutional role does this competency play? | ✓ | The smallest supported role is **capability-status presenter**. This vocabulary is descriptive only and not stabilized. |
| What bounded responsibility does it own? | ✓ | It owns collecting the implemented capability universe, deriving each entry's verification state from projected `capability_verified` support, preserving support/evidence summaries, and rendering deterministic output. |
| Does implementation distinguish worker, competency, and responsibility? | ✓ | Yes. The worker is the inventory builder/CLI formatter; the competency is capability inventory presentation; the responsibility is State-derived status presentation without admission, verification acquisition, selection, or execution. |
| What is it incapable of doing? | ✓ | It cannot create facts, verify tools, acquire evidence, evaluate promotion readiness, choose a provider, select an operation, authorize permission, call Runtime, use ToolExecutor, append events, or mutate cluster truth. |
| What is it constitutionally forbidden from doing? | ✓ | It is forbidden from treating registered operation-contract metadata as admitted repository capability knowledge, treating `verified` as execution permission, or turning inventory presentation into action. |

Smallest truthful answer:
Capability Inventory is a status-presentation competency, not a capability-governance competency.

### Preconditions

Observed:
A projected `State` must exist. The predicate catalog must admit `capability_verified`; otherwise inventory returns no entries. Capability names may enter the inventory universe from registered tool contracts, tool needs, or verification fact subjects. Verification state requires projected FactSupport.

Derived:
The competency depends on projection and fact-support semantics already implemented elsewhere. Its own constitutional work begins after projection.

Assumed:
The caller intends the selected projected State to be the evidence base. Downstream consumers will preserve the distinction between inventory status and permission.

Smallest truthful answer:
Capability Inventory can answer honestly only after State projection; it does not establish the truth of the world it presents.

### Evidence and movement

Observed:
The inventory observes registered ToolSpec capability labels, unresolved ToolNeed capabilities, `capability_verified` fact subjects, active and expired FactSupport, supporting facts, and supporting evidence summaries.

Derived:
The inventory derives `verified`, `provider_reported`, `unverified`, `stale`, and `unknown` states from fact values, missing support, and expiry. It derives age from support time and invocation time.

Assumed:
The meaning of each `capability_verified` fact and its sufficiency were earned before inventory presentation.

Movement permitted by implementation:

- registered operation-contract metadata or requested need can add a capability name to the presented universe;
- active support can move an entry into `verified`, `provider_reported`, `unverified`, or `unknown` depending on fact value;
- expired support can move an entry into `stale`;
- missing support keeps an entry at `unverified`.

Movement refused by implementation:

- inventory cannot move metadata into admitted knowledge;
- inventory cannot move evidence into a new fact;
- inventory cannot move `verified` into permission;
- inventory cannot move status into execution.

Smallest truthful answer:
Capability Inventory moves only from projected inputs to displayed status.

### Constitutional authority

Who may trust this competency?
Operators using `seed --capability-status`, internal callers, tests, and read-only summary consumers may trust the inventory.

What may be trusted?
They may trust the deterministic inventory entries as a presentation of projected capability verification state: capability name, state, supporting fact ids, supporting evidence summaries, support summary, observation times, age, and reason.

To what extent?
Only as read-only State-derived status. It is not proof of live availability, safe use, sufficient verification, provider preference, readiness for promotion, policy approval, operator authorization, or execution authority.

Under what assumptions?
Trust remains lawful only if projected State is the intended basis, `capability_verified` is the accepted predicate for verification belief, FactSupport and expiry semantics are valid for this projection, and consumers refuse to infer action from inventory status.

Capability vs constitutional authority:

- Capability: present a status inventory.
- Constitutional authority: read projected State and format derived entries.
- Not granted: authority to admit, verify, promote, select, permit, invoke, execute, record, or mutate.

Technical possibility vs constitutional permission:

- Technical possibility: the builder can see tool names, capability labels, facts, evidence ids, and support summaries.
- Constitutional permission: it may only present those as inventory status; it may not convert them into operational decisions.

Smallest truthful answer:
Seed may trust Capability Inventory for projected status presentation only.

## Neighbor Boundary Analysis

Which competency is most likely to be mistaken for this competency?

**Capability Verification** is the nearest constitutional neighbor. Both expose capability-related verification status, both are CLI-visible, both produce JSON-compatible structures, and both are read-only.

What recurring implementation evidence keeps their constitutional boundaries separate?

- Capability Inventory constructs entries from the implemented universe of admitted verification fact subjects, executable operation-contract metadata, and requested capabilities.
- Capability Verification starts from capability candidates and joins them to inventory entries.
- Capability Inventory's source helpers separate admitted knowledge from operation-contract metadata.
- Capability Verification's inspection artifact preserves candidate support separately from verification support and acquired local evidence.
- Capability Inventory returns inventory entries; Capability Verification returns candidate verification rows with boundary notes and rationale.
- Tests for both surfaces independently prove read-only behavior and no runtime/tool execution.
- Capability Verification tests additionally prove verified status does not create selection, permission, execution proposals, pending actions, or action plans.

If these competencies were accidentally merged,

what constitutional mistake

would the organism begin making?

Seed would risk treating candidate inspection as inventory admission, or treating inventory status as candidate verification authority. The smallest implementation-backed behavioral consequence is that candidate presence or operation-contract metadata could be presented as stronger capability knowledge than projected `capability_verified` support actually grants.

Smallest truthful answer:
The boundary prevents candidate or contract visibility from becoming admitted capability truth.

## Constitutional methodology investigation

Working hypothesis evaluated using this competency only:

| Statement | Classification | Implementation-backed support |
| --- | --- | --- |
| Contrast recovers boundaries. | Supported | Contrast with Capability Verification exposes that inventory owns status presentation while verification owns candidate-to-status inspection. Contrast inside inventory also separates admitted verification subjects from operation-contract metadata. |
| Invariants recover identity. | Supported | Recurring invariants are State-only input, deterministic entries, FactSupport-derived state, JSON presentation, read-only behavior, no Runtime, no ToolExecutor, and no event append. These invariants recover identity as status inventory. |
| Recurrence earns constitutional legitimacy. | Partially Supported | The read-only/no-runtime/no-execution boundary recurs in module docstrings, helper names, CLI dispatch, and tests. However, this single interrogation cannot prove universal legitimacy for the methodology statement beyond this competency. |
| Interrogation builds confidence that recovered architecture has been honestly characterized. | Partially Supported | The questions prevented overclaim by separating inventory, verification, admission, selection, and execution. The implementation evidence increases confidence, but confidence remains bounded by missing complete consumer governance and provenance. |

Smallest truthful answer:
For Capability Inventory, contrast and invariants are well supported; recurrence and interrogation are supported only within the reviewed implementation, not as stabilized methodology.

## Additional constitutional question

What authority

does this competency

appear to possess,

but implementation

does not actually grant?

Capability Inventory appears to possess **capability admission authority** because it lists capabilities and labels some as `verified`.

Implementation does not grant that authority. Admission is represented by already-projected `capability_verified` facts. Registered operation-contract capability labels only widen the presentation universe and are explicitly not admitted repository capability knowledge. Inventory consumes these inputs but does not create promotion facts, evaluate readiness, or decide execution authority.

Smallest truthful answer:
Capability Inventory appears to admit capabilities, but only presents already-projected or requested capability status.

## Constitutional observations

Observed:

- Inventory is built from State only.
- Inventory returns an empty list if `capability_verified` is absent from the predicate catalog.
- The capability universe combines registered operation-contract labels, requested capabilities, and verification fact subjects.
- Those sources are represented by separate helper dataclasses.
- Verification states are derived from FactSupport values, expiry, or missing support.
- CLI output is deterministic JSON.
- Tests prove read-only behavior and avoidance of Runtime and ToolExecutor.

Derived:

- Capability Inventory is presentation, not verification acquisition.
- Operation-contract metadata is visibility, not admitted knowledge.
- `verified` is confidence status, not permission.
- `stale` is expiry interpretation, not automatic refresh instruction.
- `provider_reported` is a state value, not provider preference.

Assumed:

- The projected State is the lawful evidence base.
- Predicate catalog semantics are trusted by the caller.
- Consumers will not promote status into action authority.

Smallest truthful answer:
The competency is constitutionally narrow because every visible capability remains tied to source type and support state.

## Constitutional reliance

Seed may rely on Capability Inventory to:

- list the implemented capability universe currently visible to inventory;
- report verification state from projected support;
- preserve support and evidence summaries;
- distinguish missing support from active, expired, provider-reported, or unknown support;
- provide deterministic JSON for operator or test inspection.

Seed must not rely on Capability Inventory to:

- admit capabilities into repository truth;
- discover candidates;
- acquire verification evidence;
- decide promotion readiness;
- select providers or operations;
- evaluate policy;
- authorize execution;
- invoke tools;
- create plans or pending actions;
- mutate the event ledger or cluster.

Smallest truthful answer:
Inventory may orient inspection; it may not govern action.

## Methodology audit

Which question prevented the largest architectural overclaim?

**What authority does this competency appear to possess, but implementation does not actually grant?**

It prevented the overclaim that listing a capability, especially as `verified`, means the inventory admitted the capability or authorized its use.

Which question produced the highest constitutional precision?

**What recurring implementation evidence keeps their constitutional boundaries separate?**

The neighbor-boundary question forced the separation between inventory presentation and candidate verification inspection, and also exposed the internal separation between operation-contract metadata and admitted verification fact subjects.

Which question generated the weakest evidence?

**Who may consume its artifacts?**

Operators, tests, CLI callers, and integrity summary code are visible, but a complete consumer registry is not implemented.

Which question may still contain multiple compressed concerns?

**Who may trust this competency?**

It compresses invocation authority, consumer identity, output trust, and downstream use constraints. This interrogation separated those concerns, but implementation does not provide a complete governance map.

Did implementation collapse previously distinct concepts?

No. The implementation preserves separations between operation-contract metadata, requested needs, admitted verification subjects, support, evidence, and inventory presentation.

Did implementation split previously compressed concepts?

Yes. The public phrase `capability-status` could compress capability existence, verification, readiness, and permission. Implementation splits it into presentation universe, FactSupport-derived state, source provenance, and refused authority.

Did the interrogation discipline change?

**Minor refinement.**

The new neighbor-boundary question usefully sharpened contrast without redesigning the discipline. The additional negative-authority question also exposed apparent admission authority. No major methodological redesign is supported.

Smallest truthful answer:
The method gained a small boundary tool; it did not earn new architecture.

## Methodology honesty candidates

Recurring observations preserved, not stabilized:

- Visibility repeatedly separates from authority.
- Recommendations repeatedly reduce to inspection rather than command.
- Verification repeatedly produces confidence rather than permission.
- Contrast repeatedly exposes boundaries.
- Invariants repeatedly expose identity.
- Recurrence repeatedly earns constitutional legitimacy only within implementation-backed repetition.
- Interrogation repeatedly increases confidence without creating authority.
- Negative authority appears to be a recurring constitutional phenomenon.

Capability Inventory reinforces these candidates in a smaller form:

- Inventory visibility is not admission authority.
- Operation-contract capability labels are not verified capability knowledge.
- Status presentation is not policy permission.
- Stale status is not refresh command.

Smallest truthful answer:
The strongest preserved candidate here is that visibility is not authority.

## Constitutional reflection

If this competency disappeared tomorrow,

what constitutional capability

would the organism lose?

Seed would lose a deterministic read-only way to present capability verification status from projected State while preserving source/support distinctions.

Nothing more.

Nothing less.

If this competency

were silently expanded,

what constitutional boundary

would most likely be violated first?

The first likely violation would be converting inventory presentation into capability admission or permission. Implementation evidence points to that boundary because admitted verification subjects and executable operation-contract metadata are explicitly separated, and tests prove inventory avoids runtime, tool execution, and event mutation.

Smallest truthful answer:
Seed would lose status inventory if removed; if expanded, it would most likely violate admission or permission boundaries.

## Lawful termination

This interrogation stops at the implemented boundary.

It does not redesign the discipline. It does not stabilize methodology vocabulary. It does not recommend a universal registry, planner, or coordinator. It does not infer authority from visibility. It does not infer permission from verification state. It does not infer priority from measurement. It does not infer action from inventory output.

Smallest truthful answer:
The lawful stop is read-only capability-status presentation.

## Remaining questions

| Type | Remaining question | Why it remains |
| --- | --- | --- |
| Consumer unknown | Which downstream consumers rely on capability inventory in all execution paths? | CLI, tests, verification, and integrity summary are visible, but complete consumer governance is absent. |
| Provenance unknown | Which operator, invocation, and projection context should accompany every inventory output? | The entry preserves support/evidence provenance, not full invocation provenance. |
| Sufficiency unknown | What support is sufficient for future promotion, policy, or operation use? | Inventory presents support; readiness and policy are outside this competency. |
| Freshness unknown | When should stale entries trigger refresh work? | Inventory reports stale state; it does not command refresh. |
| Authority unknown | Who may admit a capability or authorize execution after seeing inventory status? | Admission and execution authority are explicitly outside this surface. |

Smallest truthful answer:
The remaining unknowns do not weaken the inventory boundary; they prevent overuse of the inventory artifact.

## Confidence

**High confidence** that Capability Inventory is implemented as read-only, deterministic capability-status presentation from projected State.

**High confidence** that it refuses Runtime, ToolExecutor, event append, cluster mutation, operation selection, and execution authority.

**Medium confidence** that Capability Verification is the nearest constitutional neighbor, because implementation evidence strongly supports the adjacency but there may be other capability-adjacent surfaces with narrower public similarity.

**Medium-low confidence** in complete consumer mapping and future governance, because the repository evidence reviewed does not provide a complete consumer registry.

Smallest truthful answer:
Seed can truthfully explain Capability Inventory and distinguish it from Capability Verification without inventing authority.
