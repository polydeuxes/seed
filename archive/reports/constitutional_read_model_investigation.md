# Constitutional Read-Model Investigation

Repository authority wins.

## Boundary

This is exactly one Constitutional Read-Model Investigation.

It reviews only the Constitutional Governance Investigation, the Constitutional Provenance Investigation, and the Constitutional Observability Investigation, plus existing implementation evidence for repository read models and diagnostic surfaces where needed to answer whether the recovered maps are lawful read models over existing repository evidence.

This investigation does not recover constitutional ownership, recover implementation ownership, redesign implementation, invent runtime engines, invent governance engines, invent provenance engines, invent observability engines, invent execution tracing, or invent new authority.

## Reviewed candidate views

The candidate views reviewed are:

1. Governance view.
2. Fidelity view.
3. Observability coverage view.
4. Provenance coverage view, not provenance reconstruction.
5. Constitutional process view.

The recurring result is that these views do not own repository authority. They can only render, summarize, classify, correlate, or expose existing repository evidence with preserved refusals and Unknowns.

## Existing read-model evidence

Implementation evidence already contains a read-model home separate from authority creation:

- `seed_runtime/read_model_ownership.py` says read models consume already-published projected `State` and that the local boundary does not publish projections, replay events, invalidate caches, render output, persist snapshots, or change read-model semantics.
- `ReadModelConstructionInputs` wraps the visible projected `State` as an identity-preserving handoff into read-model builders and explicitly refuses ownership of projection replay, finalization, publication, cache invalidation, rendering, scheduling, or persistence.
- `build_state_summary()` returns a compact read-only summary from projected state after recovering the read-model construction input boundary.
- `build_fact_index()` is a derived read model built from already-projected `State`; `load_or_build_fact_index()` uses state projection version and last event id as dependency identity for cache lookup/build.

Implementation evidence also contains diagnostic/view surfaces with explicit state and mutation declarations:

- `DiagnosticInventoryEntry` declares whether a surface uses projected state, uses repo files, supports JSON, supports record, has a record scope, emits diagnostic or cluster facts, writes the event ledger, mutates cluster state, and reads diagnostic facts.
- `diagnostic_inventory` is itself a registry-declared JSON-capable, non-recording, non-event-ledger-writing, non-cluster-mutating surface.
- `diagnostic_shape_audit` statically compares diagnostic registry declarations with implementation shape without recording or mutation.
- Tests prove that the diagnostic inventory lists known diagnostics, emits JSON, requires recording diagnostics to declare `record_scope=diagnostic_run` and event-ledger writes, and requires all current diagnostics not to mutate cluster state.
- Tests prove the shape audit emits JSON rows with declared/observed/status fields.

The app was used only to confirm current implementation visibility:

```text
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
```

Observed result: the diagnostic inventory emitted 52 entries; the diagnostic shape audit emitted 468 rows; all observed shape-audit statuses were `consistent`.

## Candidate view answers

### Governance view

1. **Does it own repository authority?** No.
2. **Does it derive entirely from existing repository evidence?** Yes. The reviewed governance investigation classifies relationships among already recovered constitutional artifacts: question grammar, relationship grammar, external grammar, constitutional process, and fidelity. Its own conclusion is connective governance, not ownership hierarchy.
3. **Does it preserve read-only behavior?** Yes, if implemented as a view over repository evidence and diagnostic/read-model outputs. Existing read-model and diagnostic patterns support read-only construction and explicit mutation declarations.
4. **Does it mutate repository state?** No.

Lawful representation: a governance read model may render and summarize connective relations such as constrains, authorizes, preserves, consumes, limits, refuses, supports, relies, projects, selects, reconciles, and emits where existing artifacts support them. It must not recover ownership, hierarchy, runtime governance, execution order, or a new constitutional governor.

### Fidelity view

1. **Does it own repository authority?** No.
2. **Does it derive entirely from existing repository evidence?** Yes. Fidelity is recovered in the reviewed governance investigation as a preservation criterion that consumes authorities recovered elsewhere and tests lawful realization without creating authority.
3. **Does it preserve read-only behavior?** Yes, if implemented as a view that classifies whether evidence preserves already recovered authority, boundaries, refusals, Unknowns, and confidence.
4. **Does it mutate repository state?** No.

Lawful representation: a fidelity read model may render preservation status, summarize boundary preservation, classify known/preserved/Unknown gaps, correlate implementation evidence with recovered authority, and expose why realization remains lawful or insufficient. It must not create constitutional authority, own implementation mechanics, require structural symmetry, invent stages, or promote convenience into authority.

### Observability coverage view

1. **Does it own repository authority?** No.
2. **Does it derive entirely from existing repository evidence?** Yes. The reviewed observability investigation recovers coverage classes: directly emitted public observation, implementation-reconstructable observation, implementation-visible-only observation, constitutionally inferred observation, and preserved Unknown.
3. **Does it preserve read-only behavior?** Yes. Existing diagnostic surfaces already expose visibility, JSON, record, event-ledger, and cluster-mutation boundaries; documentation structure and inquiry artifact examples show read-only classifications with explicit refusal language.
4. **Does it mutate repository state?** No.

Lawful representation: an observability coverage read model may render coverage classes, summarize what is directly emitted, classify reconstructable versus visible-only evidence, correlate public artifacts with implementation files, and expose Unknowns. It must not become Constitutional Observability, invent tracing, emit a provenance ledger, or claim observations that repository evidence does not provide.

### Provenance coverage view, not provenance reconstruction

1. **Does it own repository authority?** No.
2. **Does it derive entirely from existing repository evidence?** Yes, but only as coverage over evidence classes and known absences. The reviewed provenance and observability investigations refuse full stage-by-stage constitutional provenance where repository evidence does not emit it.
3. **Does it preserve read-only behavior?** Yes, if it reports only coverage and refusal boundaries using existing evidence.
4. **Does it mutate repository state?** No.

Lawful representation: a provenance coverage read model may render what provenance-adjacent evidence exists, summarize directly emitted/public evidence, classify reconstruction support, correlate bounded answer surfaces with implementation-visible producers, and expose missing provenance. It must refuse provenance reconstruction, provenance invention, runtime traces, execution logs, explanation engines, stage ledgers, and direct constitutional movement claims unsupported by repository evidence.

### Constitutional process view

1. **Does it own repository authority?** No.
2. **Does it derive entirely from existing repository evidence?** Yes. The reviewed governance investigation treats Constitutional Process as a bounded recurring process pattern across artifacts: Pressure → Lawful Question → Orientation → Recovery → Cross-Examination → Completion Audit → Lawful Stop, while refusing a universal engine, owner, runtime pipeline, topology, or mandatory sequence.
3. **Does it preserve read-only behavior?** Yes, if it renders process evidence and gaps without causing process movement.
4. **Does it mutate repository state?** No.

Lawful representation: a constitutional process read model may render known stage evidence, summarize current stage support, classify missing stages as Unknown or pressure, correlate artifacts across the bounded process pattern, and expose lawful-stop/refusal evidence. It must not recover ownership, execute the process, create workflow state, mutate implementation, mutate repository files, write event-ledger records, or infer stages beyond evidence.

## Existing architecture

1. **Do existing diagnostic/read-model patterns already provide the architectural home for these views?** Yes. The repository already separates projected state/read-model construction from authority creation and already declares diagnostic/view surfaces through registry and shape-audit metadata.
2. **Would these views merely compose existing repository evidence?** Yes. Each candidate view consumes prior investigation artifacts, projected/read-model evidence, diagnostic inventory declarations, shape-audit declarations, and implementation-visible boundaries. None requires new constitutional material.
3. **Do they require new constitutional ownership?** No.
4. **Do they require new runtime authority?** No.

The fit is architectural only in the bounded sense: future implementation would be a registered read-only diagnostic/read-model surface that composes existing evidence. It would not be a constitutional discipline, runtime engine, governance engine, provenance engine, observability engine, or execution tracer.

## Read-only boundaries

Each candidate view may:

- **Render** existing investigation evidence, implementation evidence, diagnostic declarations, shape-audit results, and preserved Unknowns.
- **Summarize** bounded findings already present in reviewed repository artifacts.
- **Classify** evidence into supported, unsupported, Unknown, direct, reconstructable, implementation-visible-only, inferred-boundary, and refusal categories where repository evidence supports those labels.
- **Correlate** prior investigation findings with implementation surfaces, read-model construction boundaries, diagnostic registry declarations, and shape-audit checks.
- **Expose** confidence, boundaries, missing evidence, refusal reasons, and consumption-safe results.

Each candidate view must explicitly refuse:

- ownership recovery;
- constitutional recovery;
- implementation mutation;
- repository mutation;
- event-ledger writes;
- cluster mutation;
- provenance invention;
- explanation beyond repository evidence;
- runtime tracing;
- stage-by-stage provenance reconstruction;
- new constitutional authority;
- new implementation authority;
- promotion of presentation vocabulary into repository knowledge.

If a future surface supports `--record`, the existing diagnostic recording boundary requires `record_scope=diagnostic_run` unless intentionally different, event-ledger writes must be distinguished from cluster mutation, and read-only diagnostics must preserve `mutates_cluster=false`.

## Consumption boundaries

Repository evidence supports these views being consumable by:

- **Operators**, as bounded views explaining what repository evidence currently supports and what remains Unknown.
- **Implementation**, as read-only composition inputs or diagnostic outputs, provided diagnostic inventory and shape-audit contracts are followed.
- **Future bounded answer surfaces**, as evidence summaries or classifications, without changing the constitutional authority of the underlying artifacts.

Consumption does not change authority. A consumer may cite, render, summarize, filter, or correlate the read model, but it may not treat the read model as constitutional ownership, implementation ownership, cluster truth, provenance truth, or repository mutation.

## Preserved Unknowns

The following remain Unknown or explicitly unsupported:

- Whether future repository evidence will recover a distinct constitutional observability discipline.
- Whether future repository evidence will recover a distinct constitutional provenance discipline.
- Whether any future implementation should combine these views into one surface or several separate surfaces.
- Whether a future read-model implementation should use projected state, repository files, or both.
- Whether any future surface should support recording; this investigation does not require recording.
- Whether all prior constitutional artifacts outside the three reviewed investigations would add more candidate view fields.
- Whether consumption by a future answer surface should be direct CLI invocation, internal composition, or another already-authorized pattern.

## Readiness

The reviewed repository evidence supports only this classification:

```text
Ready for constitutional read-model implementation
```

This readiness means the maps are lawful candidate read models over existing repository evidence. It does not authorize implementation in this task and does not create constitutional authority.

## Confidence

High confidence that Governance, Fidelity, Observability Coverage, Provenance Coverage, and Constitutional Process can be lawfully represented as read-only candidate views because reviewed investigations characterize them as bounded maps or coverage classifications rather than owners, and implementation evidence already provides read-model and diagnostic-surface patterns with explicit non-mutation boundaries.

Medium confidence on exact future surface shape because this investigation intentionally does not inspect unrelated implementation or design a concrete CLI/API.

Constitutional read-model investigation complete.
