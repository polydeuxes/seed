# State-Build Cache Debug Family Completion Audit

## Scope

This audit reviews the implementation-local State-Build Cache Debug evidence-production path. It does not propose or implement another ownership slice, and it treats the current code and tests as repository authority.

Reviewed implementation points:

- `_state_build_cache_debug_evidence_from_args(...)`
- `_StateBuildCacheDebugCacheEvidence`
- `_StateBuildCacheDebugProjectionEvidence`
- `_StateBuildCacheDebugReadModelEvidence`
- `_StateBuildCacheDebugTimingEvidence`
- `_StateBuildCacheDebugEvidenceAssembly`
- `_StateBuildCacheDebugEvidence`
- `_StateBuildCacheDebugReportPayload`
- `StateSummaryCacheDebugReport`
- `format_state_summary_cache_debug_report(...)`

## Recovered implementation boundaries

The implementation now exposes these boundaries as separate implementation-local artifacts or consumers:

1. **Evidence collection != cache evidence**
   - `_state_build_cache_debug_evidence_from_args(...)` still performs the runtime collection work.
   - `_StateBuildCacheDebugCacheEvidence` is the local cache-evidence carrier for state-build visibility and projection diagnostic payload inputs.

2. **Evidence collection != projection evidence**
   - `_StateBuildCacheDebugProjectionEvidence` carries the projection diagnostic payload.
   - The cold path uses `from_diagnostic_selection(...)` to convert selected projection diagnostics into the cache-debug projection evidence shape.
   - The warm summary-cache-hit path constructs skipped projection evidence explicitly, with empty projection timings and counters.

3. **Evidence collection != read-model evidence**
   - `_StateBuildCacheDebugReadModelEvidence` records the read-model source and whether a summary snapshot was published.
   - The warm path marks `summary_source="summary snapshot"` and `summary_snapshot_published=False`.
   - The cold path marks `summary_source="constructed read model"` and records the actual snapshot-publication result.

4. **Evidence collection != timing evidence**
   - `_StateBuildCacheDebugTimingEvidence.from_collected_timings(...)` appends the `total runtime` timing to the collected timing list.
   - Both warm and cold return paths pass timing evidence into assembly instead of appending the final timing inside the assembly artifact.

5. **Evidence streams != evidence assembly**
   - `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)` consumes cache, projection, read-model, and timing evidence streams and creates the assembly shape.

6. **Evidence assembly != evidence artifact**
   - `_StateBuildCacheDebugEvidence.from_assembly(...)` consumes `_StateBuildCacheDebugEvidenceAssembly` and produces the final implementation-local evidence artifact.

7. **Evidence artifact != report payload**
   - `_StateBuildCacheDebugReportPayload.from_evidence(...)` consumes `_StateBuildCacheDebugEvidence` and selects the report payload fields.

8. **Report payload != compatibility report**
   - `StateSummaryCacheDebugReport.from_payload(...)` consumes `_StateBuildCacheDebugReportPayload` and constructs the compatibility report object.

9. **Compatibility report != presentation**
   - `format_state_summary_cache_debug_report(...)` consumes `StateSummaryCacheDebugReport` through report properties and renders the CLI text.

## Recovered producer → artifact → consumer chain

The implementation evidence supports this producer chain:

```text
_state_build_cache_debug_evidence_from_args(...)
  collects runtime evidence and produces stream artifacts

  -> _StateBuildCacheDebugCacheEvidence
  -> _StateBuildCacheDebugProjectionEvidence
  -> _StateBuildCacheDebugReadModelEvidence
  -> _StateBuildCacheDebugTimingEvidence

_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)
  consumes the stream artifacts

  -> _StateBuildCacheDebugEvidenceAssembly

_StateBuildCacheDebugEvidence.from_assembly(...)
  consumes assembly

  -> _StateBuildCacheDebugEvidence

_StateBuildCacheDebugReportPayload.from_evidence(...)
  consumes evidence artifact

  -> _StateBuildCacheDebugReportPayload

StateSummaryCacheDebugReport.from_payload(...)
  consumes report payload

  -> StateSummaryCacheDebugReport

format_state_summary_cache_debug_report(...)
  consumes compatibility report

  -> rendered CLI presentation
```

The public `state_summary_cache_debug_from_args(...)` function also confirms the outer handoff: it builds a `StateSummaryCacheDebugReport` from the evidence returned by `_state_build_cache_debug_evidence_from_args(...)`.

## Counterexample review

### Cache evidence and projection evidence

No remaining producer-chain counterexample was found where cache evidence and projection evidence remain inseparably mixed. Cache evidence still includes the projection diagnostics payload for compatibility with the older `from_cache_evidence(...)` assembly path, but the stream-aware path now also passes `_StateBuildCacheDebugProjectionEvidence` separately into `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`. That is residual compatibility pressure, not evidence that the producer chain lacks a projection-evidence artifact.

### Evidence streams and evidence assembly

No remaining counterexample was found where stream production and assembly are the same artifact. The warm and cold paths both construct stream artifacts and then call `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.

### Evidence assembly and evidence artifact

No remaining counterexample was found where assembly and final evidence artifact remain the same owner. `_StateBuildCacheDebugEvidence.from_assembly(...)` is the explicit handoff.

### Evidence artifact and report payload

No remaining counterexample was found where the final evidence artifact directly becomes the public report. `_StateBuildCacheDebugReportPayload.from_evidence(...)` is the explicit intermediate owner, and `StateSummaryCacheDebugReport.from_payload(...)` consumes that payload.

## Remaining compressed boundaries

The strongest remaining compression is no longer inside the evidence-production owner. It is downstream and consumer-facing:

1. **`StateSummaryCacheDebugReport` compatibility surface**
   - The report still exposes property-based compatibility names for cache eligibility, state cache status, last event ids, projection timings, projection counters, and notes.
   - This is a compatibility/report owner pressure, not evidence-production pressure.

2. **`format_state_summary_cache_debug_report(...)` presentation**
   - The formatter still owns CLI vocabulary, ordering, headings, conditional sections, sorted counter rendering, timing rendering, and projection-subphase rendering.
   - This is presentation pressure.

3. **Broader state-build cache-debug orchestration**
   - `_state_build_cache_debug_evidence_from_args(...)` still opens the projection store and ledger, lists events, performs cache lookups, constructs the projector, performs projection replay/build, derives read models, optionally saves summary snapshots, and closes resources.
   - That pressure belongs to orchestration/runtime collection, not to the now-recovered evidence stream → assembly → artifact → report-payload chain.

## Supported conclusions

### 1. Has the evidence-production path become a completed implementation responsibility chain?

Yes. For the evidence side of State-Build Cache Debug, the implementation now exposes a complete responsibility chain from collection, through four evidence stream artifacts, through assembly, through final evidence, through report payload, and into the compatibility report.

The completion is bounded: it means the evidence-production lifecycle is explicit. It does not mean every downstream consumer, presentation detail, or broader orchestration activity is separately recovered.

### 2. What implementation evidence supports that conclusion?

Implementation support:

- The stream artifact classes exist for cache, projection, read-model, and timing evidence.
- `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)` consumes those stream artifacts.
- `_StateBuildCacheDebugEvidence.from_assembly(...)` consumes assembly.
- `_StateBuildCacheDebugReportPayload.from_evidence(...)` consumes the evidence artifact.
- `StateSummaryCacheDebugReport.from_payload(...)` consumes the report payload.
- `state_summary_cache_debug_from_args(...)` uses the evidence producer as its upstream source and returns the compatibility report.
- `format_state_summary_cache_debug_report(...)` consumes the report object rather than the implementation-local evidence artifacts.

Test support:

- Existing tests prove assembly consumes stream artifacts, timing evidence preserves collected labels and appends total runtime, projection evidence is built from selected diagnostics, evidence consumes assembly, and the report consumes evidence through the payload.

### 3. Does any remaining recurring compression still belong to the evidence-production owner?

No. The recurring evidence-production compression identified in the bounded recovery is now explicitly represented by the stream artifacts and the assembly/report handoffs.

The remaining pressure is either compatibility/presentation pressure or broader orchestration pressure. Continuing to slice the same evidence-production family would likely produce framework extraction rather than implementation-backed ownership recovery.

### 4. Which implementation owner now contains the strongest remaining pressure?

The strongest remaining pressure is the **StateSummaryCacheDebugReport / formatter presentation owner** pair.

Reason:

- The report object preserves public compatibility properties that flatten visibility and projection diagnostic details into consumer-facing names.
- The formatter owns the visible CLI structure and vocabulary.
- These owners are downstream of the evidence-production chain and are the next place where repeated presentation/report-shape pressure can be investigated without confusing it for evidence collection.

A secondary pressure exists in the broader `_state_build_cache_debug_evidence_from_args(...)` orchestration body. However, that pressure is runtime orchestration and resource lifecycle pressure, not evidence-production pressure.

### 5. Should the next work continue State-Build Cache Debug ownership recovery?

No. Stop this State-Build Cache Debug evidence-production family.

The next investigation should begin with a different responsibility owner: **StateSummaryCacheDebugReport / `format_state_summary_cache_debug_report(...)` presentation and compatibility ownership**. If that owner does not show implementation-backed recurring compression, then the next likely owner is broader state-build cache-debug orchestration/resource lifecycle.

## Unsupported conclusions

This audit does not support these conclusions:

- That the CLI output should change.
- That JSON, event, ledger, cache, projection, or read-model schemas should change.
- That `_state_build_cache_debug_evidence_from_args(...)` should be split further as part of this audit.
- That presentation vocabulary such as state-build cache, projection cache, or timing labels should be promoted into broader repository knowledge.
- That downstream diagnostic inventory or shape-audit surfaces changed; this audit adds only a markdown report and no runtime surface.

## Relationship to completed upstream families

The evidence-production chain now aligns with the prior completed upstream recoveries:

- Report payload recovery established `_StateBuildCacheDebugEvidence != _StateBuildCacheDebugReportPayload`.
- Report compatibility recovery established `_StateBuildCacheDebugReportPayload != StateSummaryCacheDebugReport`.
- Assembly recovery established `Evidence Assembly != _StateBuildCacheDebugEvidence`.
- Cache, projection, read-model, and timing stream recoveries established stream-level boundaries before assembly.

Together, those recoveries form a complete implementation-local lifecycle for the evidence side of State-Build Cache Debug.

## Confidence

Confidence: **High**.

Reasons:

- The implementation has explicit classes and classmethod handoffs for every stage in the requested lifecycle.
- Warm and cold evidence paths both converge through `_StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(...)`.
- Tests cover the stream artifacts, assembly handoff, evidence artifact handoff, payload handoff, and compatibility report handoff.
- Remaining pressure can be named in downstream or orchestration owners without requiring another evidence-production slice.

## Recommended next responsibility owner

Recommended next owner: **StateSummaryCacheDebugReport / `format_state_summary_cache_debug_report(...)` presentation and compatibility ownership**.

Recommendation: **stop slicing the State-Build Cache Debug evidence-production family** and begin a new bounded investigation of report/presentation ownership only if implementation evidence shows recurring compression there.
