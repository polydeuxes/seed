# Executive Summary

Recent architecture audit sequences converged on the same preservation finding:
Seed usually did not need a new subsystem. The audited behavior already existed,
ownership already existed, and composition often existed. The durable gap was
usually vocabulary, status, discoverability, or handoff clarity.

This document preserves those findings as long-lived repository guidance so
future work can start from settled architecture instead of rediscovering the same
questions. It is documentation-only. It does not create a new audit chain, new
vocabulary, new reconciliation, new inventory, new summary, new navigation
system, or implementation plan.

Current frontier: **Knowledge Acquisition expansion** through bounded read-only
observation slices. The best immediate candidates remain **Users Observation v1**
and **Groups Observation v1**, followed by Packages and Systemd when their
boundaries are kept equally narrow.

# Architectural Findings Worth Preserving

The following findings should remain visible in roadmap, status, handoff, and
architecture guidance:

| Finding | Preservation guidance |
| --- | --- |
| Behavior already exists before implementation assumptions. | Before proposing new code, inspect existing surfaces for the behavior. Recent Response, Selection Rationale, Response Caveat, Projection Integrity, Context Composition, and Explainability work found distributed behavior before missing implementation. |
| Ownership before implementation. | Identify the existing owner of each semantic concern before introducing a new owner. Integrity signals, confidence, contradictions, evidence, state, context, explanations, capability metadata, and response envelopes already have owners. |
| Composition before new subsystems. | Prefer cross-links, handoff notes, status tables, or documentation maps over engines, universal formatters, or centralized layers when existing surfaces already carry the semantics. |
| Audit before inventing. | When a concern is ambiguous, characterize existing behavior and boundaries before adding objects, routes, adapters, read models, schemas, or execution paths. |
| Implementation not justified is a valid outcome. | A completed audit may conclude that no implementation should happen. That outcome should be recorded as architecture knowledge, not treated as incomplete work. |
| Negative findings are architectural findings. | Rejections such as “no engine,” “no summary,” “no Runtime integration,” and “no ToolExecutor integration” prevent architecture drift and should stay discoverable. |
| Vocabulary can be enough. | Several audit chains only needed stable terms to describe existing behavior. Vocabulary should not be mistaken for a mandate to implement a new owner. |
| Runtime is not the default integration point. | Runtime owns routing and response envelopes; it is not the universal home for selection, integrity, caveats, explanations, or response composition semantics. |
| ToolExecutor is not the default integration point. | ToolExecutor owns registered-operation execution; it is not a verification, truth-selection, caveat, response, or rationale engine. |
| Acquisition creates; Integrity characterizes; Selection selects; Response communicates. | Preserve this lifecycle framing when adding future documentation or observation slices. |

# Completed Audit Sequences

Completed and paused audit sequences should be recorded as settled status, not as
open implementation backlog.

| Audit sequence | Preserved status | Final handoff |
| --- | --- | --- |
| Explainability | Resolved enough for now. | Explanation behavior and ownership exist through existing explanation, evidence, confidence, conflict, and projection surfaces. No `ExplainabilityEngine` is justified. |
| Context Composition | Resolved enough for now. | Context composition vocabulary and reconciliation established distributed context selection, relevance, priority, and budget concepts. No `ContextEngine` is justified. |
| Knowledge Integrity | Resolved enough for now. | Integrity is a read-only projected-knowledge concern over support, conflict, staleness, confidence, graph issues, verification limits, and source limitations. |
| Projection Integrity Summary | Characterized and implemented where justified. | Summary work is read-only visibility over existing projected integrity signals, not a repair or truth engine. |
| Projection Integrity Navigation / Drilldown | Characterized and implemented where justified. | Navigation should remain linked to existing integrity structures and should not create a parallel truth system. |
| Selection Rationale | Complete. | Characterization, vocabulary, reconciliation, and summary characterization established distributed rationale. Selection Rationale Summary implementation is not currently justified. |
| Response | Complete enough for current architecture. | Response is a distributed operator-facing communication concern. No `ResponseEngine`, universal formatter, Runtime rewrite, or ToolExecutor integration is justified. |
| Response Caveats | Complete enough for now; paused. | Caveat vocabulary exists and caveat signals already live in source surfaces. Additional caveat-specific audit chains are not currently justified. |
| Backlog and Status Reconciliation | Complete for Selection Rationale handoff. | Selection Rationale should remain completed-audit / documentation-maintenance work, not generic implementation backlog. |
| Architectural Status and Next Frontier | Complete for current frontier choice. | The next frontier is Knowledge Acquisition expansion, not recursive architecture decomposition. |

Future status documents should prefer compact labels such as:

```text
Completed audit / vocabulary established / implementation not justified / paused pending new evidence.
```

# Negative Findings Worth Preserving

These negative findings should remain visible because they block repeated
rediscovery and protect accepted ownership boundaries:

- **Selection Rationale Summary implementation is not justified.** Existing
  rationale surfaces answer current concrete questions well enough; a first-class
  summary would require new classification, inventory, history, or read-model
  semantics without demonstrated operator need.
- **Selection Rationale Inventory, Navigation, and Drilldown are not justified as
  new runtime artifacts.** Documentation cross-links are acceptable; new read
  models, routes, schemas, adapters, or engines are not currently warranted.
- **Response implementation is not justified.** Response behavior already exists
  across response envelopes, CLI output, context/state views, explanations,
  integrity surfaces, capability surfaces, evidence, contradictions, confidence,
  and issue outputs.
- **Response Caveat implementation is not justified.** Caveat signals already
  exist in source surfaces; a universal caveat layer would duplicate source
  semantics and risk a parallel limitation system.
- **Repeated engine rejection is settled architectural memory.** The audit
  program repeatedly rejected `ReasoningEngine`, `IntegrityEngine`,
  `ExplainabilityEngine`, `SelectionEngine`, `ResponseEngine`, `ContextEngine`,
  planners, workflow engines, universal formatters, universal caveat layers,
  parallel truth systems, parallel response systems, and parallel caveat systems.
- **Runtime and ToolExecutor integration are not default fixes.** Neither owner
  should absorb selection, caveat, response, integrity, or explanation semantics
  merely because a future document wants a central place to look.
- **Parallel truth systems must be avoided.** Documentation, rationale, caveats,
  summaries, and responses must not introduce hidden trust scores, automatic
  contradiction repair, projection mutation, or independent fact stores.

Recommended destinations for these findings:

- architecture/frontier documents for high-level handoff;
- roadmap and backlog documents for future-work filtering;
- audit sequence status tables for completed-chain visibility;
- handoff notes whenever future sessions resume acquisition work.

# Current Frontier

The current frontier is **Knowledge Acquisition expansion**.

Roadmap and status documents should align around narrow read-only observation
slices rather than additional recursive architecture decomposition. The highest
value candidates remain:

1. **Users Observation v1** — local identity/configuration facts from bounded
   local sources such as `/etc/passwd`; avoid NSS/network lookup, authentication
   claims, user health, or account-management authority.
2. **Groups Observation v1** — local group/configuration facts from bounded local
   sources such as `/etc/group`; avoid network-backed lookup and authorization
   claims beyond observed membership/configuration.
3. **Packages Observation v1** — readable local package databases only; do not
   call package managers or infer supportability/health.
4. **Systemd Observation v1** — read-only unit inventory/state boundaries only;
   no `systemctl` actions, management authority, or service-health claims.

Further recursive decomposition of Response Caveats, Selection Rationale,
Response subcategories, or generalized “reasoning” should pause unless new
evidence identifies a concrete operator question not answered by existing
surfaces.

# Acquisition Readiness

Documentation now sufficiently supports beginning **Users Observation v1** and
**Groups Observation v1** without additional architecture work.

Readiness basis:

- the acquisition/selection distinction is established as
  `Observation -> Evidence -> Fact -> Projection` versus selected consumption of
  projected knowledge;
- the knowledge acquisition status board already lists Users and Groups as
  planned Local Observation v1 items;
- the capability extension methodology already requires the narrowest fact,
  least-privileged source of truth, read-only observation, and separation of
  observation, inference, verification, and execution;
- the frontier document already recommends Users and Groups as the strongest
  immediate candidates;
- completed audit sequences have preserved the relevant non-goals: no new
  engines, no Runtime changes, no ToolExecutor changes, no projection mutation,
  no event appends outside a future observation implementation, and no parallel
  truth systems.

Additional architecture work is not required before starting those slices. A
future implementation task should still define each observation's precise fact
scope, evidence source, projection behavior, privacy boundaries, and tests before
code changes begin.

# Recommended Documentation Updates

Recommended low-risk documentation maintenance:

1. Cross-link this preservation document from the architectural frontier document
   so future sessions can find the settled findings quickly.
2. Update the reasoning roadmap to state that Response and Response Caveat audit
   sequences are now complete enough for current architecture and paused unless
   new evidence appears.
3. Update backlog/status language that still calls Response the least-audited
   top-level concern. That was true before Response characterization,
   vocabulary, reconciliation, and caveat vocabulary work; it is no longer the
   best frontier framing.
4. Keep Knowledge Acquisition status as the active frontier and keep Users and
   Groups at the top of the planned Local Observation v1 path.
5. Preserve negative findings in status tables rather than converting them into
   implementation backlog items.
6. Avoid creating a separate audit index unless documentation discoverability
   materially degrades; compact status tables in existing documents are enough
   for now.

# Conclusion

The recent audit program produced durable architectural knowledge: Seed's next
step is not another engine, planner, universal layer, or recursive audit chain.
The repository should preserve the completed audit findings, keep negative
findings visible, and move the frontier to bounded Knowledge Acquisition
expansion.

Users Observation v1 and Groups Observation v1 are ready to begin as future
implementation tasks without more architecture work, provided they stay narrow,
read-only, evidence-backed, and separate from inference, verification,
management, execution, response composition, and truth arbitration.
