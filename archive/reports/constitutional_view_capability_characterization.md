# Constitutional View Capability Characterization

This is exactly one implementation architecture investigation. It determines whether `ConstitutionalViewCapability` is an implementation-local ownership boundary or a deterministic projection derived from existing constitutional read-model evidence.

It does not implement Capability, redesign Selection, redesign Composition, redesign registration, invent semantic reasoning, invent runtime derivation, invent constitutional authority, or recover another ownership boundary.

Repository authority wins.

## Implementation evidence reviewed

Review was limited to the requested evidence set:

- Constitutional Process View: `seed_runtime/constitutional_process_view.py`;
- Constitutional Governance View: `seed_runtime/constitutional_governance_view.py`;
- Constitutional Fidelity View: `seed_runtime/constitutional_fidelity_view.py`;
- `ConstitutionalReadModelContract` and `ReadModelViewRegistration`: `seed_runtime/read_model_ownership.py`;
- Constitutional View Capability Slice 001: `constitutional_view_capability_slice_001.md`.

Expansion was not required beyond these files. Existing CLI behavior, JSON output, human rendering, compatibility answers, diagnostic inventory, diagnostic shape audit, Constitutional View Selection recovery, and Constitutional View Composition remain preserved.

## Existing implementation evidence

### ConstitutionalReadModelContract

`ConstitutionalReadModelContract` records recurring implementation obligations shared by constitutional read-model views: stable name, CLI flag, builder, renderer, JSON renderer, diagnostic inventory name, diagnostic shape-audit name, read-only status, JSON support, record support, record scope, event-ledger behavior, and cluster-mutation behavior.

Its implementation-local authority is explicitly negative beyond that metadata: it does not construct views, render output, dispatch CLI requests, register diagnostics, create constitutional authority, create implementation authority, or define future constitutional view contents.

The registered constitutional contracts are exactly:

- `constitutional_process`;
- `constitutional_governance`;
- `constitutional_fidelity`.

Each registered contract preserves `read_only=True`, `supports_json=True`, `supports_record=False`, `record_scope="none"`, `writes_event_ledger=False`, and `mutates_cluster=False`.

### ReadModelViewRegistration

`ReadModelViewRegistration` records only the consumable registration shape for an already existing read-model view: name, CLI flag, builder, renderer, and read-only status.

Its docstring refuses construction, rendering, CLI dispatch, argument parsing, projection publication, ledger writes, cluster mutation, and constitutional-content declaration. The registration therefore does not own constitutional capability semantics.

### Constitutional Process View

The Constitutional Process View is a frozen, read-only view over existing constitutional process evidence. It contains:

- a stable view name;
- `compatibility_answer="No."`;
- an evidence composition tuple;
- deterministic stage records with stage name, status, support level, evidence, and summary;
- preserved Unknowns;
- remaining candidate views;
- read-only, non-ledger-writing, non-cluster-mutating boundary flags.

The view already expresses what it contributes toward: bounded process stages from Pressure through Lawful Stop, each tied to implementation-visible evidence and summary text. It also expresses what remains Unknown. A capability description for this view would be regenerated from those existing fields rather than independently authored.

### Constitutional Governance View

The Constitutional Governance View is a frozen, read-only view over existing constitutional governance evidence. It contains:

- a stable view name;
- `compatibility_answer="No."`;
- an evidence composition tuple;
- deterministic relationship records with relationship name, status, support level, evidence, and summary;
- preserved Unknowns;
- explicit refusals;
- remaining candidate views;
- read-only, non-ledger-writing, non-cluster-mutating boundary flags.

The view already expresses what it contributes toward: known governance relationships and refusals, each grounded in existing evidence. A capability description for this view would expose those already-owned relationships and refusals in another representation.

### Constitutional Fidelity View

The Constitutional Fidelity View is a frozen, read-only view over completed Constitutional Fidelity evidence. It contains:

- a stable view name;
- `compatibility_answer="No."`;
- an evidence composition tuple;
- deterministic classification records;
- recurring discipline text;
- preserved Unknowns;
- explicit refusals;
- read-only boundaries;
- remaining candidate views;
- read-only, non-ledger-writing, non-cluster-mutating boundary flags.

The view already expresses what it contributes toward: classifications and recurring fidelity discipline, plus explicit refusals and Unknowns. A capability description for this view would be derived from those already-owned fields.

### Constitutional View Capability Slice 001

The earlier capability recovery correctly identified implementation pressure: `ConstitutionalViewSelection` needs deterministic repository evidence for what each registered constitutional view may contribute toward.

However, the slice also states that existing immutable read-only view artifacts expose bounded content, Unknowns, refusals, and compatibility answers, while existing contracts expose registered identities and operational metadata. That same evidence supports a narrower conclusion than independent ownership: capability can be a deterministic projection over an already registered constitutional read model and its already-owned view artifact.

The slice did not implement Capability and did not prove an independent mutation owner. It identified a missing representation between registered views and Selection. Repository evidence now determines that the missing representation is projection, not ownership.

## Derivability analysis

### Constitutional Process View

1. **Can its constitutional capability be deterministically regenerated from existing repository evidence?** Yes. The view's registered identity comes from `ConstitutionalReadModelContract`, while its contribution surface comes from the view name, process stages, stage evidence, stage summaries, Unknowns, and read-only flags in the existing Process View artifact.
2. **Would an independently maintained capability artifact duplicate constitutional knowledge?** Yes. Re-authoring process scope, supported stages, out-of-scope implications, or Unknowns in a separate capability artifact would duplicate the Process View's existing constitutional evidence and summaries.
3. **Would capability become stale if the underlying constitutional view evolved?** Yes. If stages, evidence, summaries, Unknowns, or remaining candidate views changed, a separately maintained capability artifact would need synchronized edits or would misdescribe the Process View.

### Constitutional Governance View

1. **Can its constitutional capability be deterministically regenerated from existing repository evidence?** Yes. The view's registered identity comes from `ConstitutionalReadModelContract`, while its contribution surface comes from the Governance View name, governance relationships, relationship evidence, relationship summaries, Unknowns, explicit refusals, and read-only flags.
2. **Would an independently maintained capability artifact duplicate constitutional knowledge?** Yes. Re-authoring governance relationships, supported governance uses, refusals, or Unknowns in a separate capability artifact would duplicate already-owned Governance View knowledge.
3. **Would capability become stale if the underlying constitutional view evolved?** Yes. If governance relationships, summaries, evidence, Unknowns, or refusals changed, an independently maintained capability artifact would need to change in lockstep or become stale.

### Constitutional Fidelity View

1. **Can its constitutional capability be deterministically regenerated from existing repository evidence?** Yes. The view's registered identity comes from `ConstitutionalReadModelContract`, while its contribution surface comes from the Fidelity View name, classifications, recurring discipline, evidence, Unknowns, explicit refusals, read-only boundaries, and remaining candidate views.
2. **Would an independently maintained capability artifact duplicate constitutional knowledge?** Yes. Re-authoring fidelity classifications, lawful-realization scope, refusals, or Unknowns in a separate capability artifact would duplicate the Fidelity View's existing constitutional knowledge.
3. **Would capability become stale if the underlying constitutional view evolved?** Yes. If classifications, discipline text, evidence, Unknowns, refusals, or read-only boundaries changed, an independently maintained capability artifact would need synchronized maintenance or would misrepresent the Fidelity View.

## Duplication analysis

Repository evidence already divides responsibility:

- contracts own stable registered implementation metadata;
- registrations own consumable read-model registration metadata;
- each constitutional view owns its own read-only constitutional artifact;
- Selection is recovered as the later relevance decision;
- Composition consumes selected registered names after selection.

An independently maintained capability artifact would repeat content that the views already own: process stages, governance relationships, fidelity classifications, explicit refusals, Unknowns, read-only boundaries, and compatibility answers. That repetition would introduce a second authored location for constitutional contribution scope.

The repository has repeatedly preserved distinctions where a representation can expose owned evidence without becoming its owner. The reviewed evidence follows that pattern: capability is a representation of the registered view's existing contribution surface, not an independent constitutional or implementation authority.

## Ownership analysis

### 1. Does capability own independent implementation authority?

No.

The reviewed files prove existing owners for every implementation responsibility capability would need to describe:

- registered identity and operational metadata are owned by `ConstitutionalReadModelContract` and `ReadModelViewRegistration`;
- process contribution evidence is owned by Constitutional Process View;
- governance contribution evidence is owned by Constitutional Governance View;
- fidelity contribution evidence is owned by Constitutional Fidelity View;
- relevance decision ownership belongs to recovered `ConstitutionalViewSelection`;
- post-selection composition belongs to Constitutional View Composition.

No reviewed evidence requires Capability to mutate, author, adjudicate, select, compose, recover, or declare new authority.

### 2. Or does capability merely expose already-owned constitutional evidence in another representation?

Capability merely exposes already-owned constitutional evidence in another representation.

For each view, the capability surface is derivable from stable registration identity plus the view's own deterministic fields: names, contribution records, evidence, summaries, Unknowns, refusals, compatibility answer, and read-only operational boundaries.

### 3. Does repository evidence require independent mutation ownership?

No.

The views are frozen read-only artifacts. The contracts and registrations are deterministic metadata. The capability pressure arises because Selection needs deterministic access to contribution evidence, not because a new component must independently mutate or author constitutional knowledge.

## Projection analysis

Repository evidence supports:

```text
Constitutional View

↓

Capability Projection

↓

Selection
```

It does not support:

```text
Constitutional View

↓

Capability Owner

↓

Selection
```

The reason is implementation-local and evidence-bound:

1. The constitutional views already contain contribution records, supporting evidence, Unknowns, refusals, compatibility answers, and non-mutating boundaries.
2. The read-model contract and registration already provide stable registered identity and operational entry-point metadata.
3. The earlier Capability slice identified the need for deterministic selection input, but did not prove independent authorship, independent mutation, independent constitutional authority, or independent implementation authority.
4. A capability layer can expose the view's already-owned evidence in selection-friendly form without becoming the owner of that evidence.
5. If capability were independently authored, it would duplicate view knowledge and become stale whenever the underlying view evolved.

Therefore Capability belongs between Constitutional View and Selection only as a deterministic projection.

## Preserved Unknowns

The following Unknowns remain preserved and are not resolved by this characterization:

- Whether every constitutional inquiry starts only as Pressure remains Unknown.
- Whether every Recovery requires a separate Cross-Examination artifact remains Unknown.
- Whether every Cross-Examination requires a separate Completion Audit remains Unknown.
- Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains Unknown.
- Whether a single named constitutional process owner exists remains Unknown.
- Whether future constitutional work may recover additional governance relationships remains Unknown.
- Whether Constitutional Governance should ever become a runtime governance mechanism remains Unknown.
- Whether the implementation should expose governance comparison or conflict-resolution views remains Unknown.
- Whether Constitutional Fidelity should ever become an implementation-backed public surface remains Unknown.
- Whether future work should implement a projection mechanism for capability remains Unknown.
- Whether future Selection implementation should consume a materialized projection artifact, an in-memory derived structure, or another deterministic representation remains Unknown.

## Compatibility

Expected compatibility answer:

```text
No.
```

Compatibility is preserved because this characterization changes only this investigation document and does not modify:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Capability recovery;
- Constitutional View Selection recovery;
- Constitutional View Composition;
- CLI behavior;
- JSON output;
- human rendering;
- diagnostic inventory;
- diagnostic shape audit;
- compatibility behavior.

No diagnostic, audit, probe, view, operational CLI flag, or recordable output is added or modified. No runtime behavior changes. No JSON shape changes. No human rendering changes. No diagnostic registry or diagnostic shape-audit implementation change is required.

## Confidence

High confidence.

The reviewed implementation evidence consistently shows Capability as derivable from existing registered read-model identity plus each constitutional view's already-owned contribution evidence. The evidence does not require independent mutation ownership, independent authorship, or a second constitutional knowledge location. The stale-duplication risk is direct for all three implemented constitutional views.

## Classification

Capability is a deterministic projection.

Constitutional View Capability characterization complete.
