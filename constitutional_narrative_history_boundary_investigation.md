# Constitutional Narrative / History Boundary Investigation

## Boundary

This document performs exactly one bounded constitutional investigation:

```text
Narrative != History
```

It does not implement anything, add a diagnostic surface, create a narrative engine, create a history engine, create a chronology engine, create artifact scoring, create a truth engine, perform world research, perform legal research, evaluate Flock cameras, implement the Eye, or promote `narrative` or `history` into ontology.

Repository authority wins.

## Bounded question

Across recurring repository evidence, what constitutional boundary, if any, separates:

```text
narrative / explanation / story / rendering
```

from:

```text
history / event evidence / temporal provenance / historical claim
```

and under what conditions, if any, can narrative lawfully render history without becoming history?

## App-visible evidence used

The app was used only as a bounded visibility surface. Its output is evidence of app-visible surface behavior and registry declarations, not an oracle about truth.

Reviewed commands:

```text
python scripts/seed_local.py --help
python scripts/seed_local.py --history-brief
python scripts/seed_local.py --diagnostic-inventory
python scripts/seed_local.py --diagnostic-shape-audit
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-subject narrative --knowledge-reachability-audit-all --knowledge-reachability-audit-limit 10
```

App-visible findings:

- `--help` exposes repository surfaces relevant to the boundary: `--history-brief`, `--reasoning-path`, `--selection-path`, `--source-navigation`, `--fact-support`, `--evidence`, `--current-facts`, `--diagnostic-inventory`, `--diagnostic-shape-audit`, and knowledge-reachability audit surfaces.
- `--history-brief` reported a clean repository context, unknown historical confidence, insufficient comparison history, and a boundary that correlation may be visible while causation is not proven by the brief.
- `--diagnostic-inventory` showed diagnostic rows with explicit columns for state use, repo-file use, JSON support, record support, record scope, fact emission, and cluster mutation. This supports treating visible output as bounded declared surface behavior rather than history by itself.
- `--diagnostic-shape-audit` showed registry declarations compared to static implementation shape, including `record_scope`, `writes_event_ledger`, `uses_projected_state`, and `mutates_cluster`. This supports the boundary between a diagnostic record, an event-ledger write, projected state use, and cluster mutation.
- Knowledge reachability for `narrative` reported candidate kind `unknown`, not preserved, not projected, not in read model, not in inquiry orientation, not rendered, and first loss `not_preserved`. This supports refusing to treat `narrative` as already promoted repository knowledge or ontology.

## Reviewed repository evidence

This investigation reviewed recurring repository evidence around constitutional history, constitutional reality, observation, event ledger, event evidence, temporal provenance, current lawful condition, projection, explanation, natural-language interpretation, constitutional translation, artifact bounded lawful reliance, lawful acceptance, bounded lawful reliance, warrant, claim form, source navigation, fact support, reasoning path, selection path, diagnostic inventory, diagnostic shape audit, Unknown preservation, lawful stop, and boundary-confusion review artifacts.

Key reviewed artifacts include:

- `README.md`
- `docs/architecture.md`
- `docs/logic_model.md`
- `seed_runtime/events.py`
- `time_neighborhood_characterization.md`
- `constitutional_biography_origin_investigation.md`
- `constitutional_boundary_confusion_competency_audit_review.md`
- `constitutional_repetition_proof_boundary_investigation.md`
- `constitutional_lawful_acceptance_characterization.md`
- `constitutional_warrant_characterization.md`
- `artifact_bounded_lawful_reliance_characterization.md`
- `plato_cave_constitutional_translation_characterization.md`

## 1. What repository evidence already means by history

Repository evidence supports several distinct uses of history. They are related but not interchangeable.

### Append-only Seed event history

The strongest implementation-backed meaning is EventLedger history. `docs/architecture.md` states that `EventLedger` is the authoritative historical event record, append-only, and records what happened within Seed without becoming a truth oracle about the world. `seed_runtime/events.py` implements `EventLedger` as the owner of append-only runtime event history read by projection and owner services. `docs/logic_model.md` places `EventLedger` in the State layer as append-only history from which `StateProjector` and `ProjectionStore` derive current projected state.

This means repository history is not merely a sequence told in prose. It is a preserved event record with append order, event identity, kind, workspace, payload, actor/session/correlation fields where modeled, and projection consequences where consumed.

### Constitutional history

Constitutional history is the preserved Seed-local past for a scope. `constitutional_biography_origin_investigation.md` states that Seed preserved constitutional history begins only when a competent local responsibility records a lawful append-only event, while external world-side history may pre-exist Seed-local participation without becoming Seed-owned history. The same investigation says append-only history is projection/audit authority, not objective reality, complete memory, verification, or truth.

### Historical account or self-history visibility

The repository also recognizes later accounts over preserved history. A bounded read, inspection, orientation, replay, or explanation may access preserved history and produce a self-history account, but the account is not the history itself. It is downstream visibility or interpretation over preserved material.

### History brief

The app's `--history-brief` is an operational visibility surface. In this run it preserved insufficient comparison history and refused causation. The brief is therefore an account over available comparison/snapshot evidence, not a general history oracle.

## 2. What repository evidence already means by narrative, explanation, story, or rendering

`narrative` is not currently preserved as a stable repository concept. App-visible knowledge reachability for `narrative` showed `unknown` candidate kind and first loss `not_preserved`. That is important: this investigation cannot promote `narrative` into ontology merely because the user asks about it.

The repository does support narrower adjacent responsibilities:

- **Presentation/rendering.** `README.md` says Presentation owns rendering. Rendering is a display responsibility, not authority.
- **Explanation.** `docs/architecture.md` places explanation downstream of projected knowledge and context selection, and describes the Evidence Graph as a read-only explanation layer derived from projected State. Explanation can expose why a fact exists and which projected evidence supports it, but it does not append events, mutate hosts, resolve contradictions, or become a second state store.
- **Natural-language interpretation.** `README.md` says natural language may be treated as observation of communicative acts and may support claims about what a speaker requested, asserted, forbade, or prioritized, while remaining weak or irrelevant as direct support for environmental truth. Interpreters may derive candidate meaning from language, but they are not architectural authority.
- **Constitutional translation.** Prior translation evidence treats translation/promotion/projection/explanation as repository-owned movements that must preserve boundaries rather than bypass finite observation.

`story` and `rendering` therefore have no independent authority as history. At most, a story-like or narrative-like rendering can be a presentation format over evidence, claims, chronology, or history when its support path and authority boundaries are preserved.

## 3. When narrative is merely presentation or interpretation over evidence

Narrative is merely presentation or interpretation when it organizes, summarizes, selects, or explains already bounded evidence without adding lawful event evidence, temporal provenance, support, or authority.

A narrative remains presentation/interpretation when:

1. It is produced by a renderer, explanation surface, audit report, investigation, or natural-language account.
2. It cites or points to underlying event records, observations, facts, source-navigation results, support paths, or prior artifacts.
3. It preserves claim form: what is event evidence, what is projection, what is current lawful condition, what is inference, what is unsupported, and what remains Unknown.
4. It does not assert that its coherence is proof of occurrence.
5. It does not treat order in prose as temporal provenance.
6. It does not overwrite append-only history, mutate projected state, or silently convert diagnostic output into cluster truth.

A coherent story can be useful and lawful as an explanation. It becomes unlawful when the account's coherence is used as the authority for historical occurrence.

## 4. When narrative can lawfully render historical evidence

Narrative can lawfully render historical evidence only as a bounded presentation over historical evidence. It may render history without becoming history when all of the following conditions hold:

1. **Evidence anchor.** The narrative identifies the preserved event evidence, observation evidence, fact support, source path, prior artifact, or diagnostic output it is rendering.
2. **Temporal boundary.** It distinguishes preservation/event-ledger time, observation time, source-sample time, occurrence-time claims, knowledge/justification time, and chronology prose where relevant.
3. **Claim-form boundary.** It marks whether the statement is an event-record claim, current-state projection claim, historical claim, temporal claim, interpretation, explanation, or unsupported conclusion.
4. **Authority boundary.** It remains within the authority of the underlying source. Event existence can support that an event was recorded; it does not prove external-world truth of every payload assertion.
5. **Support path.** It exposes enough support path for a reader or downstream surface to know why the historical claim is warranted.
6. **Unknown preservation.** Missing occurrence time, missing provenance, missing independence, missing event evidence, missing authority, or missing support remains Unknown.
7. **Non-mutation.** The narrative does not write cluster truth, rewrite history, or treat diagnostic recording as operational mutation.

Under those conditions, narrative can be a lawful rendering of history. It is not itself the event ledger, the event evidence, the temporal provenance, or the historical claim's warrant.

## 5. What distinguishes event evidence from a story about events

Event evidence is repository-preserved material with a competent local recording boundary. In the implementation-backed case, it is an EventLedger event stored append-only with modeled identity and payload. A story about events is an account that selects and orders statements about events.

The distinction is:

| Boundary | Event evidence | Story about events |
| --- | --- | --- |
| Constitutional status | Preserved local record or evidence artifact | Presentation, interpretation, explanation, or account |
| Authority | Supports claims within source/event authority | Has only the authority of its sources and claim form |
| Time | Has preservation context and possibly modeled temporal fields | May contain chronology prose that is not provenance |
| Projection relation | Can feed projection where implementation consumes events | May explain projection but does not feed projection by being coherent |
| Unknowns | Preserves missing provenance/support as gaps | Must not fill gaps narratively |
| Failure mode | Event existence overclaimed as world truth | Narrative coherence overclaimed as history |

A story may cite event evidence. It does not become event evidence unless it is itself lawfully recorded as an event or artifact, and even then the event proves the recording of the story, not the external truth of the story's contents.

## 6. What distinguishes temporal provenance from chronology prose

`time_neighborhood_characterization.md` strongly separates time neighborhoods. Occurrence/external-reality time, observation/collection time, source sample/source-asserted time, knowledge/justification time, preservation/event-ledger time, temporal claim/revision time, diagnostic elapsed time, progress timing, and cache visibility time are not interchangeable.

Temporal provenance is preserved timing support: who or what supplied the timestamp, what clock or source it came from, what it measures, when Seed observed or preserved it, and what claim it can support.

Chronology prose is ordered language: first, next, later, before, after, finally. It may express an interpretation of sequence, but it is not temporal provenance unless tied to preserved timing support and claim authority.

Therefore:

- Append order is not external occurrence time.
- Event timestamp is preservation context, not automatic occurrence authority.
- Observation time is not source sample time.
- Source sample time may support an occurrence claim but does not become the occurrence itself.
- Diagnostic elapsed timing measures Seed diagnostic work, not the time of external events.
- Chronology prose may render a temporal claim, but cannot create one.

## 7. What distinguishes historical claim from narrative coherence

A historical claim is a bounded claim about something that happened, was recorded, was observed, changed, became justified, or became preserved. It requires claim-form-matched support.

Narrative coherence is the internal fit of an account. It may make an explanation easier to follow. It may reveal a hypothesis. It may organize evidence. It does not itself provide event evidence, source provenance, source independence, temporal provenance, currentness, contradiction handling, or authority.

A historical claim may be warranted when:

- it is supported by event evidence, observation evidence, source-navigation results, fact support, prior bounded artifacts, or other competent repository evidence;
- its source authority matches the claim form;
- temporal provenance or temporal Unknowns are preserved;
- contradictions and stale support are considered where relevant;
- confidence remains support-relative.

A coherent story lacking those conditions remains an interpretation, candidate explanation, or Unknown-bearing account.

## 8. Role of observation, event ledger, support path, claim form, authority, confidence, and Unknown preservation

### Observation

Observation is the intake layer for what Seed has seen or been told before deciding what it proves. Natural language can be observed as a communicative act, but the truth of its represented content requires separate support.

### Event ledger

The event ledger preserves append-only Seed runtime history. It can support claims that Seed recorded an event. It does not prove external-world truth and does not turn payload narrative into objective history.

### Support path

Support path is what keeps a historical account inspectable. Fact support, reasoning path, selection path, and source navigation are surfaces for showing why a claim or selection is available. Missing support path prevents promotion from narrative to warranted historical claim.

### Claim form

Claim form determines needed support. A claim that an event was recorded differs from a claim that an external event occurred; a claim that a speaker asserted something differs from a claim that the asserted thing is true; a chronology claim differs from a temporal-provenance claim.

### Authority

Authority constrains claims. Presentation, explanation, rendering, and app visibility have display or visibility authority, not truth authority. Event evidence has event-record authority; observations have source/provenance authority; prior investigations have bounded constitutional-characterization authority.

### Confidence

Confidence is support-relative, not certainty. `docs/architecture.md` describes Confidence Aggregation as estimating support strength without becoming truth or resolving contradictions. A narrative may have high readability while low historical confidence.

### Unknown preservation

Unknown is the lawful result when evidence, authority, provenance, temporal support, or support path is missing. Unknown preservation prevents a story from filling evidentiary gaps with fluent prose.

## 9. Unknowns that must remain when narrative lacks event evidence, temporal provenance, or support path

When narrative lacks event evidence, temporal provenance, or support path, these Unknowns must remain:

- whether the described event occurred;
- whether Seed recorded any event corresponding to the narrative;
- whether the narrative accurately represents preserved event history;
- whether the order in the narrative matches append order, observation order, occurrence order, or a source's asserted order;
- whether timestamps are occurrence time, observation time, source sample time, knowledge time, preservation time, diagnostic timing, or prose chronology;
- whether source statements are independent, copied, stale, contradictory, or authoritative;
- whether a historical claim is supported, weakly supported, contradicted, or unsupported;
- whether any current-state projection follows from the claimed history;
- whether the narrative has authority beyond presentation or interpretation;
- whether confidence stronger than low/unknown is warranted.

Unknown preservation is not failure. It is the repository-lawful alternative to narrative overclaiming.

## 10. Lawful stop condition preventing narrative from becoming history

The lawful stop condition is:

> Stop when coherent story, explanation, chronology prose, public motivation, narrative-like rendering, or natural-language interpretation is offered as historical fact without preserved event evidence, temporal provenance or explicit temporal Unknown, support path, source authority, claim-form boundary, and confidence limit.

At that point the repository may report a narrative, interpretation, candidate explanation, chronology prose, or unsupported historical claim. It must not report history, event evidence, temporal provenance, proof, truth, current state, ontology, or implementation requirement.

## 11. Does this investigation strengthen the previous partial boundary?

Yes. The prior boundary-confusion review found `Narrative != History` partially preserved because history/current-state/projection boundaries were supported, while `narrative` as a separate competency was less developed.

This investigation strengthens the boundary by separating:

- narrative / explanation / story / rendering as presentation or interpretation;
- chronology prose as ordered language rather than temporal provenance;
- event evidence as preserved local record or support artifact;
- temporal provenance as timestamp/source/clock/meaning support rather than prose sequence;
- historical claim as claim-form-matched support rather than narrative coherence;
- constitutional history as Seed-local preserved append-only history or bounded constitutional past, not objective world history;
- lawful rendering as bounded account over evidence, not history by identity.

The strengthening is constitutional clarification only. It does not stabilize `narrative` as implementation vocabulary or require a narrative/history engine.

## 12. Does repository evidence support implementation work yet?

No. No concrete repository failure was found. Existing surfaces and artifacts already preserve the relevant boundaries at manual constitutional-review level:

- app-visible diagnostic surfaces distinguish record scope, event-ledger writes, projected-state use, and cluster mutation;
- history brief refuses causation when comparison history is insufficient;
- knowledge reachability refuses to treat `narrative` as preserved knowledge;
- repository architecture separates observation, evidence, claims, projection, explanation, rendering, event history, and confidence;
- prior investigations preserve Unknowns and lawful stop.

Repository evidence supports this bounded investigation as documentation. It does not support implementing a new diagnostic, ontology, engine, checklist, artifact scoring system, chronology system, or truth adjudicator.

## Supported conclusions

1. History in the strongest repository sense is Seed-local preserved append-only event history and downstream bounded accounts over it, not coherent prose.
2. Constitutional history begins only at a competent Seed-local preservation or event-recording boundary for its scope; external world history does not become Seed history merely by existing or being narrated.
3. Explanation and rendering are downstream visibility/presentation responsibilities.
4. Natural-language interpretation may support claims about communicative acts but is weak or irrelevant as direct support for environmental truth unless other evidence supports that truth.
5. Narrative can lawfully render history only when it preserves evidence anchors, temporal boundaries, claim form, authority, support path, Unknowns, and non-mutation.
6. Event evidence differs from a story because event evidence is preserved under a competent local boundary; a story is an account over claimed or preserved events.
7. Temporal provenance differs from chronology prose because provenance preserves timestamp source, clock/meaning, observation/preservation context, and support relation; prose sequence does not.
8. Historical claim differs from narrative coherence because the former requires claim-form-matched support and authority while the latter is an account-quality property.
9. Missing event evidence, temporal provenance, support path, or authority must remain Unknown.
10. The previous partial `Narrative != History` boundary is strengthened at constitutional-analysis level.

## Unsupported conclusions

1. `Narrative` is not proven as preserved repository ontology.
2. `History` is not a world-truth oracle.
3. A coherent story is not historical evidence by coherence.
4. Chronology prose is not temporal provenance by sequence words.
5. A recorded event does not prove external truth of every payload assertion.
6. App output is not an oracle.
7. Diagnostic recording is not cluster mutation unless a competent implementation boundary says so.
8. Current repository evidence does not support a narrative engine, history engine, chronology engine, truth engine, artifact scoring system, checklist engine, or new diagnostic surface.

## Implementation recommendation

No implementation work is recommended.

The appropriate result is constitutional clarification: preserve the lawful stop where narrative, explanation, story, rendering, or chronology prose lacks event evidence, temporal provenance, support path, authority, or claim-form-matched warrant.
