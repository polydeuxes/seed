# Seed vocabulary and episode-index local-history recovery 001

## Attribution and standing

This report was produced by the visitor (independent reviewer session), not the
curator. It is offered as attributed evidence and testimony, in the same sense
`seed_vocabulary_and_episode_index_remote_history_correction_001.md` treats
operator statements: repository testimony, not Book authority, and not
automatically promoted to established fact.

It corrects one premise of that report. Its stated blocker was that
`git fetch --unshallow` and GitHub API/connector retrieval both failed with
403/401 in its task environment, so E1's exact adoption chronology, E2's
originating PR, and E3's pre-1611 creation PR were deferred as remote-retrieval
work. The checkout this report was produced from is **not shallow**
(`git rev-parse --is-shallow-repository` returns `false`; 2996 first-parent
commits, back to the actual first commit). No GitHub API or remote fetch was
used or needed here — only `git log`, `git show`, and `git diff` against commit
objects already present locally. The prior report's 403/401 findings were an
artifact of its own execution environment, not of the repository.

## E1 — "handoff" origin

- PR #66, commit `0adffdc`, 2026-06-03, "Introduce non-executable HandoffPlan
  and capability/handoff boundary (no internal execution)." Full diff recovered
  via `git diff 0adffdc^1 0adffdc -- 01-architecture.md`. Before this PR, Seed
  had a "Tool Registry" and an internal executor calling registered tools
  directly. This PR replaced that with `HandoffPlan` and stated Seed "does not
  own an internal execution lifecycle." Exact quoted rationale from the diff:

  > "Preferred execution backends live outside Seed: Ansible/AWX for host
  > automation, Temporal/Prefect for workflows, MCP servers for tool
  > integration, Vault, ssh-agent, sudo, and become-aware automation for
  > secrets and privilege boundaries."

  This is infrastructure-orchestration vocabulary (Ansible, Temporal, MCP,
  Vault) adopted as architecture, not generic "LLM/agentic" language. This is a
  more precise, falsifiable characterization than the general one attributed to
  the operator in the prior report's testimony ledger, and the two should be
  kept distinct rather than treated as identical.

- PR #67, commit `0f7862c`: "Add HandoffPlan generation and --handoff CLI for
  accepted ActionPlans."
- PR #68, commit `1cf39f0`: "Persist handoff plan creation."
- PR #1918, commit `e34240d`: "Excise foreign planning control shell" — the
  quarantine/removal of the planning/handoff control shell.
- PR #1922, commit `d567d3e`: "Add Book standing contamination topology
  report."
- PR #1923, commit `8d397f2`: "Correct handoff compression in active Book."
- PR #1924, commit `904f0bb`: "Correct representation emission book address."
- PR #1925, commit `ea0975f`: "Clean up representation emission residue."

Corrected chain: PRs 66-68 (architecture adoption) -> PR 1918
(quarantine/excision) -> PRs 1922-1925 (constitutional decomposition into
representation formation/emission/responsibility/authority). This matches the
prior report's guessed shape (E1a/E1b/E1c) with exact commits attached instead
of a targeted-but-unretrieved record.

## E2 — claim/Fact origin (still partial; a real, acknowledged gap)

- Claim-related work traces back at least to PR #253, commit `801b489`,
  2026-06-08, "Add documentation claim extraction path," and to several
  earlier untitled direct commits before it in the log ("docs: add claim
  support frontier", "docs: characterize claim support", "docs: add claim
  support design") that carry no PR number.
- Commit `6ea2334`, 2026-06-10, "Align documentation with claim-centric
  ontology" — two days after PR #253, a consolidation, not the origin.
- PR #1887, commit `00b68fe`: "Add claim normalization fact standing recovery
  report" (adds `claim_normalization_and_fact_standing_recovery_001.md`).
- PR #1888, commit `4e60289`: "Amend Book claim normalization fact standing"
  (adds `claim_normalization_and_fact_standing_amendment_001.md`).

This pass stopped at PR #253 and the untitled pre-#253 commits without fully
tracing them. That earlier boundary is a real, acknowledged gap, not a
fabricated absence, and is the one part of the prior report's "recover
remotely" instruction that still applies locally: someone should trace the
pre-#253 commits the rest of the way.

## E3 — constitutional pipeline, now fully chained locally

- PR #1607, commit `eb9806a`: "Implement constitutional pipeline invocation" —
  the pipeline's actual creation, four PRs before bounded-ask was wired to it.
  This was Unknown in both prior reports.
- PR #1611, commit `66e1f3f`, 2026-07-13: "Wire bounded ask to constitutional
  pipeline." Full PR content recovered — the report
  `constitutional_pipeline_integration_wiring_001.md` was added in this same
  commit. It directly confirms the six-field adapter was chosen because it
  "avoided semantic inference" and bounded-ask "already owned admission." The
  prior report quoted this only as "contemporaneous claims pending remote
  verification"; it is now directly verified from the original PR's own added
  report text, not inferred from later summaries.
- PR #1734, commit `7bd2325`: "Delete raw constitutional pipeline question
  origination" — the refusal that made PR #1611's producer stale.
- PRs #2135-2139: already fully covered by existing repository reports
  (`bounded_ask_constitutional_pipeline_ingress_cleanup_001.md`,
  `bounded_constitutional_question_complete_topology_recovery_001.md`,
  `static_constitutional_pipeline_deletion_001.md`).

## What this does not establish

- Why Ansible/Temporal/MCP specifically seemed like the right execution model
  at the time (motive, not recoverable from commits).
- Any discussion that happened outside these commits.
- The exact pre-PR-253 claim-centric origin (untitled early commits not fully
  traced in this pass) — still open.

## Direct answers

1. **Was the prior report's remote-retrieval blocker a repository fact?** No.
   It was that report's own execution environment failing to reach GitHub;
   this checkout's full history was available the whole time.
2. **Does this resolve E1?** Yes, with exact commits for architecture
   adoption, quarantine, and constitutional decomposition.
3. **Does this resolve E2?** Partially. Adoption/amendment reports are pinned
   (PR #1887/#1888); the true origin before PR #253 remains untraced.
4. **Does this resolve E3?** Yes, including the previously-Unknown
   pipeline-creation PR (#1607).
5. **What is the smallest next lawful action?** Trace the pre-PR-253
   claim-centric commits to their actual origin, the same way this report
   traced E1 and E3. No Book, schema, or implementation change is proposed
   here.
