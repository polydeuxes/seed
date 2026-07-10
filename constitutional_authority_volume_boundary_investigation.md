# Constitutional Authority / Volume Boundary Investigation

Repository authority wins.

## Status and bounded question

This is exactly one bounded constitutional investigation focused only on:

```text
Authority != Volume
```

Bounded question:

```text
Across recurring repository evidence, what constitutional boundary, if any, separates authority / competent boundary / warrant / lawful reliance from volume / source count / popularity / repetition / consensus / visibility / amplification, and under what conditions, if any, can volume lawfully contribute to evidence without becoming authority?
```

This investigation does not implement anything, add a diagnostic surface, create an authority engine, create a volume engine, create a consensus engine, create source scoring, create popularity scoring, create artifact scoring, create a checklist engine, create a truth engine, perform world research, evaluate Flock cameras, perform legal research, implement the Eye, or promote `volume`, `consensus`, or `popularity` into ontology.

## App-visible evidence used

App-visible surfaces were used as bounded repository evidence, not as an oracle:

- `python -m scripts.seed_local --help`
- `python -m scripts.seed_local --diagnostic-inventory --json > /tmp/diag_inventory.json`
- `python -m scripts.seed_local --diagnostic-shape-audit --json > /tmp/shape_audit.json`
- `python -m scripts.seed_local --knowledge-reachability-audit --knowledge-reachability-audit-subject authority --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr_authority.json`
- `python -m scripts.seed_local --knowledge-reachability-audit --knowledge-reachability-audit-subject volume --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr_volume.json`
- `python -m scripts.seed_local --reasoning-path ownership discrepancy --json > /tmp/reasoning.json`
- `python -m scripts.seed_local --selection-path current_focus --json > /tmp/selection.json`

The app output contributed these bounded observations:

- The CLI exposes authority-, warrant-, evidence-, reachability-, reasoning-, selection-, source-navigation-, fact-support-, diagnostic-inventory-, and diagnostic-shape-audit-related surfaces.
- Diagnostic inventory returned 52 registered diagnostics and includes mechanical boundary fields such as `record_scope`, `writes_event_ledger`, and `mutates_cluster`.
- Diagnostic shape audit returned 468 rows comparing declared and observed diagnostic shape fields.
- Knowledge reachability for both `authority` and `volume` treated the one-off queried term as an `unknown` candidate in the empty default state used by the command. That is not proof that the repository lacks those concepts; it is only app-visible evidence that the queried terms were not projected as current knowledge in that run.
- Reasoning path for `ownership discrepancy` returned a read-only reasoning boundary and preserved `unknown` because no derivation evidence was currently available.
- Selection path for `current_focus` returned a read-only selection boundary, ranked candidates by explicit evidence fields, and preserved boundary fields saying it does not record facts, write the event ledger, or mutate the cluster.

The attempted commands `python -m scripts.seed_local --source-navigation authority --limit 20` and `python -m scripts.seed_local --source-navigation volume --limit 20` failed because `--limit` is owned by `--documentation-structure`, not `--source-navigation`. That failure is not used as substantive evidence except to preserve the command-shape boundary.

## Reviewed repository evidence

Reviewed repository evidence included:

- `AGENTS.md`
- `constitutional_boundary_confusion_competency_audit.md`
- `constitutional_boundary_confusion_competency_audit_review.md`
- `constitutional_repetition_proof_boundary_investigation.md`
- `constitutional_narrative_history_boundary_investigation.md`
- `constitutional_warrant_characterization.md`
- `constitutional_promotion_authority_characterization.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/operator_understanding_surface_observation.md`
- representative search results around state summary volume, source counts, measurement volume, documentation recurrence, knowledge reachability, source navigation, reasoning path, selection path, fact support, diagnostic inventory, diagnostic shape audit, responsibility evaluation, Unknown preservation, and lawful stop.

## 1. What repository evidence already means by authority

Repository evidence already treats authority as **bounded permission or competence to rely, move, record, execute, mutate, promote, or interpret within a specific local family**. It is not generic confidence, popularity, display prominence, source count, or repeated presence.

The strongest recurring authority pattern is:

```text
Evidence may authorize movement only through the local constitutional boundary competent for that movement.
```

`constitutional_promotion_authority_characterization.md` states that promotion is permitted only when family-local repository evidence satisfies that family's boundary, ownership, and stop conditions. It also says no universal promoter has been earned. This makes authority local, evidence-gated, and stop-conditioned rather than volume-gated.

`constitutional_warrant_characterization.md` adds that lawful reliance depends on evidence binding, provenance, support, role, authority limit, negative authority, Unknown preservation, confidence, and non-promotion. Warrant is therefore not merely the existence of many references; it is the preserved entitlement and limit under which a claim can be used.

Operationally, diagnostic inventory and diagnostic shape audit preserve authority boundaries mechanically. Their app-visible fields include read/write/mutation/record-scope declarations. A diagnostic can be visible, registered, and frequently used while still lacking cluster-mutation authority. The selection and reasoning path app outputs likewise expose read-only boundaries.

## 2. What repository evidence already means by volume, source count, popularity, consensus, amplification, or high visibility

Repository evidence does **not** show a general constitutional ontology for public-world volume, popularity, consensus, amplification, or high visibility.

What it does show is local count-like or visibility-like evidence:

- fact counts;
- durable fact counts;
- current measurement sample counts;
- observation source counts;
- warning counts;
- graph issue counts;
- source counters;
- candidate counts;
- diagnostic row counts;
- documentation recurrence;
- repeated wording;
- high-volume operational output;
- measurement volume;
- high-visibility projection or summary surfaces.

Those counts describe amount, shape, recurrence, or visibility. They do not by themselves establish authority. Existing state-summary and operator-understanding work explicitly warns that fact counts, observation counts, and entity counts can describe system volume while saying little about what Seed learned. State-summary top-entity work similarly rejects fact or measurement volume as operator relevance.

The prior boundary-confusion audit found authority boundaries strongly supported but `volume` as a named repository category unsupported. That remains true: `volume` is currently a local descriptor of count, recurrence, or visibility, not a general constitutional source of authority.

## 3. When volume is merely repeated or highly visible assertion

Volume is merely repeated or highly visible assertion when the repository can show only:

- many copies of the same claim;
- repeated wording without source independence;
- high count without provenance;
- repeated institutional publication without a competent authority path;
- consensus language without preserved support rules;
- high visibility in a projection, summary, diagnostic, or document set;
- repeated app output without implementation-backed evidence;
- source count without source identity, source role, source time, method, vantage point, or claim form;
- recurring presentation vocabulary without knowledge-reachability or implementation evidence.

In that condition, the lawful statement is weak:

```text
The assertion recurs / is visible / appears in many places.
```

The lawful statement is not:

```text
The assertion is authoritative / proved / warranted / lawfully relied upon as a stronger claim.
```

This follows the strengthened `Repetition != Proof` investigation: high count or high volume without an authority path, local admissibility rule, or claim-strength match is not proof. It also follows the `Narrative != History` investigation: a coherent or repeated rendering is not historical evidence unless it carries temporal provenance and lawful support.

## 4. When volume can lawfully contribute to evidence

Volume can lawfully contribute to evidence only as **bounded evidence about a bounded claim form**, not as authority itself.

Lawful contribution requires at least one local admissibility rule such as:

1. **Count claim rule**: the claim is itself about count, frequency, recurrence, or distribution. Example: a diagnostic emitted 468 shape-audit rows in one run. The count can support a count claim, not a truth or authority claim.
2. **Independent corroboration rule**: multiple observations come from independent sources, methods, times, or evidence paths and agree on the relevant normalized dimensions required by the claim.
3. **Operational pressure rule**: high warning or observation volume can create pressure to inspect, prioritize, or reduce noise, while not establishing truth or authority.
4. **Coverage rule**: multiple files, tests, or surfaces can show recurrence of a repository pattern when the claim is limited to recurrence or implementation visibility.
5. **Confidence calibration rule**: independent support may increase confidence for the same scoped claim, but only when provenance, independence, freshness, and claim-strength matching are preserved.

Even then, the volume remains evidence. It does not become the competent authority. The competent authority remains the local boundary that decides what the count can mean.

## 5. What distinguishes source count from source authority

Source count asks:

```text
How many sources, observations, rows, files, mentions, or surfaces exist?
```

Source authority asks:

```text
Does this source have the competent role, provenance, scope, method, and authority boundary to support this claim at this strength?
```

A high source count can be duplicated from one source, copied through many documents, stale, out of scope, institutionally amplified, or scoped to weaker claims. A single competent source with preserved provenance may support a bounded claim better than many non-independent sources. Conversely, many independent competent sources may corroborate a claim, but they do so by satisfying independence and support rules, not because the raw count itself is authority.

## 6. What distinguishes popularity or consensus from warrant

Popularity or consensus describes social or institutional uptake. Warrant describes lawful reliance under preserved evidence, provenance, authority boundary, negative authority, Unknowns, and claim-strength limits.

Popularity can be evidence for a popularity claim:

```text
Many sources say X / X is widely visible / X is a consensus label in this corpus.
```

It is not warrant for a stronger claim unless the repository also preserves why that popularity is admissible for that stronger claim. Consensus without provenance, source independence, claim-form preservation, and competent authority remains consensus-as-visibility, not warrant.

## 7. What distinguishes institutional amplification from competent authority

Institutional amplification means an institution repeats, republishes, syndicates, standardizes, or makes a claim prominent. Competent authority means the institution or surface has the lawful role for the specific movement or claim.

The boundary is role and competence, not volume. A diagnostic inventory entry has authority to declare and expose diagnostic shape fields because repository implementation and tests make that its role. Its visibility does not grant it authority to mutate cluster truth unless its `mutates_cluster` boundary says so. Likewise, an external institution repeating a claim many times would not become competent authority unless repository evidence preserves its authority path and admissibility for the claim.

## 8. What distinguishes high visibility from admissible evidence

High visibility is that something is easy to see, prominent, repeated, summarized, projected, or operationally noisy. Admissible evidence is evidence that the relevant local boundary can lawfully use for the claim.

Repository evidence repeatedly separates visibility from authority:

- projections and summaries are read views, not truth engines;
- diagnostics expose shape and state but generally preserve read-only or diagnostic-run scope;
- app output is bounded evidence, not an oracle;
- presentation vocabulary is not automatically repository knowledge;
- knowledge reachability is needed before promoting presentation vocabulary into preserved or projected knowledge.

High visibility can prompt investigation. It cannot substitute for provenance, support path, authority, or claim-strength match.

## 9. Role of provenance, source independence, claim form, authority boundary, confidence, and claim-strength matching

These are the controlling conditions that prevent volume from becoming authority:

| Condition | Constitutional work |
| --- | --- |
| Provenance | Preserves who/what reported, generated, observed, or rendered the material; without it, source count may be copy count. |
| Source independence | Distinguishes corroboration from duplication, copying, syndication, or shared upstream dependency. |
| Claim form | Keeps count claims, recurrence claims, support claims, current-truth claims, historical claims, authority claims, and implementation claims separate. |
| Authority boundary | Identifies the local competent boundary that can interpret evidence and what the surface explicitly cannot do. |
| Confidence | Calibrates strength of reliance without becoming certainty or authority. |
| Claim-strength matching | Prevents weak support from being used for stronger conclusions; some claims require specific evidence kinds, not merely more evidence volume. |

The decisive pattern is not `more sources => more authority`; it is:

```text
more admissible, independent, provenance-preserved support may increase evidentiary weight for a claim whose form permits that support, under a competent boundary, with confidence and Unknowns preserved.
```

## 10. Unknown preservation when volume lacks provenance, independence, or authority evidence

When volume lacks provenance, source independence, authority evidence, claim form, or support path, the following must remain Unknown:

- whether repeated sources are independent;
- whether many mentions derive from one upstream assertion;
- whether institutional repetition reflects competence or mere amplification;
- whether consensus is evidentiary consensus, social consensus, presentation convention, or copied language;
- whether high visibility reflects importance, measurement frequency, projection mechanics, source shape, or operator relevance;
- whether the sources are competent for the claim;
- whether the claim is about recurrence, fact, history, current condition, authority, recommendation, or implementation behavior;
- whether confidence should rise;
- whether lawful reliance is permitted at all;
- whether `volume`, `consensus`, or `popularity` should become stable repository vocabulary.

The lawful output is to preserve these as Unknowns, not to fill them with volume.

## 11. Lawful stop condition

The lawful stop condition is:

```text
Stop when many instances, repeated sources, consensus language, popularity, institutional amplification, or high visibility are offered as authority without a preserved authority path, source role, provenance, source independence, support path, claim-form match, and local admissibility rule.
```

At that stop, the investigation may say:

- the material is repeated;
- the material is highly visible;
- the material appears in many sources;
- a count or recurrence claim may be supported;
- additional bounded inquiry may be warranted.

It must not say:

- volume is authority;
- popularity is warrant;
- institutional repetition is competent authority;
- source count proves the claim;
- high visibility is admissible evidence for every claim;
- app output is truth;
- a volume/consensus/popularity engine is required.

## 12. Does this investigation strengthen the previous partial boundary?

Yes, at constitutional-analysis level.

The previous review found `Authority != Volume` strongly preserved for authority boundary and non-promotion, but only partially preserved for `volume` because volume remained local and unsupported as a general category. This investigation strengthens that partial by distinguishing:

- authority;
- competent boundary;
- warrant;
- lawful reliance;
- source count;
- repetition;
- popularity;
- consensus;
- institutional amplification;
- high visibility;
- corroboration;
- evidentiary weight.

It strengthens the boundary without promoting `volume` into ontology and without implementing anything.

## 13. Does repository evidence support implementation work yet?

No.

No concrete repository failure was found that requires implementation work. The repository already has diagnostic inventory, shape audit, knowledge reachability, source navigation, fact support, reasoning path, selection path, responsibility-style audits, Unknown preservation, and lawful-stop vocabulary sufficient for this bounded investigation.

The unsupported implementation conclusions remain:

- no authority engine;
- no volume engine;
- no consensus engine;
- no popularity scoring;
- no source scoring;
- no artifact scoring;
- no truth engine;
- no checklist engine;
- no ontology promotion for `volume`, `consensus`, or `popularity`.

## Supported conclusions

1. Authority is local, evidence-gated, boundary-bound competence for lawful reliance, movement, recording, execution, mutation, interpretation, or promotion.
2. Volume is currently local count, recurrence, visibility, source-count, warning-count, fact-count, observation-count, or measurement-count evidence, not a general constitutional authority category.
3. Source count is not source authority.
4. Popularity and consensus are not warrant unless repository evidence preserves a local admissibility rule and support path.
5. Institutional amplification is not competent authority unless the institution or surface has the competent role for the claim.
6. High visibility is not admissible evidence by itself.
7. Volume can contribute to evidence for count, recurrence, coverage, pressure, or corroboration claims when provenance, independence, claim form, authority boundary, confidence, and claim-strength matching are preserved.
8. Unknowns must remain where provenance, independence, authority, claim form, or support path is missing.
9. The previous partial `Authority != Volume` boundary is strengthened at constitutional-analysis level.
10. No implementation work is supported by this investigation.

## Unsupported conclusions

1. That volume is authority.
2. That source count proves a claim.
3. That popularity is warrant.
4. That consensus is constitutional authority.
5. That institutional repetition is competent authority.
6. That high visibility is admissible evidence for all claims.
7. That app output is an oracle.
8. That `volume`, `consensus`, or `popularity` should be promoted into repository ontology.
9. That a source-scoring, popularity-scoring, authority-scoring, consensus-scoring, artifact-scoring, checklist, proof, or truth engine is warranted.

## Implementation recommendation

No implementation work is recommended.

Repository evidence supports a constitutional boundary clarification only: volume may contribute to evidence under provenance, independence, claim-form, authority-boundary, confidence, and claim-strength controls, but volume must not become authority.
