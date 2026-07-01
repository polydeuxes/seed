# Null First Constitutional Transition Audit

## Executive answer

The first implementation-backed constitutional transition after Null is not full semantic observation, attachment, interpretation, or inquiry. The strongest recurring implementation evidence supports this narrower transition:

```text
Null
↓
A bounded external representation is preserved or inspected by an existing local input/intake responsibility
↓
Observation may be created only if a provider/source contract can construct a valid Observation
```

For the smallest operator representation `.` specifically, current implementation begins by preserving an inquiry note outside the event ledger. That preservation truthfully acknowledges that operator prose exists, but it does not create an `Observation`, `Evidence`, `Fact`, repository attachment, or inquiry graph. The first bounded responsibility eligible to participate for this operator-prose path is Inquiry Orientation: it may render a read-only orientation view over the preserved note and already projected state, while explicitly refusing fact, claim, goal, tool, plan, command, authorization, semantic-interpretation, ownership, and recommendation authority.

The repository does distinguish external representation from `Observation`, but not through a universal `ExternalRepresentation` type. The distinction is distributed across existing responsibilities such as `InputInspector`/`InputArtifact`, inquiry-note preservation, provider parsers, JSON observation import validation, and observation source adapters. Therefore Model B is better supported than Model A if Model B is phrased as a distributed, bounded intake/preservation condition rather than a new central artifact or gateway.

## Implementation evidence reviewed

Representative implementation and prior repository investigations reviewed:

- `seed_runtime/input_inspector.py`: raw file input inspection, `InputArtifact`, deterministic text-format detection, input-act classification.
- `seed_runtime/inquiry_orientation.py`: inquiry-note preservation, orientation rendering, lexical related-material matching, authority boundary.
- `scripts/seed_local.py`: CLI wiring for `--record-inquiry-note` and `--inquiry-orientation`.
- `seed_runtime/runtime.py`: runtime user messages recorded as `input.user_message` before decision composition.
- `seed_runtime/context.py`: `DecisionInputComposer` carries current input into a model packet without converting it into an observation.
- `seed_runtime/observations.py`: canonical `Observation` shape and `ObservationIngestor` conversion into observation/evidence/fact events.
- `seed_runtime/observation_sources.py`: `ObservationSource` protocol and repository-source observation adapter.
- `seed_runtime/ansible_inventory_source.py`: provider-specific file intake, parser selection, and observation creation after accepted inventory parsing.
- `external_representation_repository_attachment_audit.md`: recent evidence that attachment-like work is distributed rather than centralized.
- `external_artifact_intake_vs_provider_language_translation_investigation.md`: evidence for raw artifact intake before provider language translation in some paths.
- `null_to_repository_orientation_experiment.md`: recent `.` experiment showing inquiry note preservation, no current observations/facts, and justified stopping.

## Current implementation behavior

### Operator-prose path

`record_inquiry_note(...)` appends one non-empty raw note into an isolated JSONL probe store. The module-level boundary says inquiry notes are outside the event ledger and that rendering does not mutate state, append events, call providers, execute tools, or create facts, goals, tool needs, decisions, proposals, or plans.

For `.` this means the implementation-backed first truth is:

```text
A raw inquiry note with text `.` was preserved for the inquiry-orientation probe.
```

It is not:

```text
An observation exists.
```

`build_inquiry_orientation(...)` then constructs a read-only view from the preserved note and projected state. Its evidence collection tokenizes note text and searches projected fact supports and source-navigation matches. The authority boundary states the note is preserved operator prose and is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction. It further states matches are deterministic lexical overlaps only and do not assert importance, ownership, intent, concern, recommended action, or next safe move.

The recent `.` experiment confirms this path in a fresh database: recording `.` produced an inquiry note id, `--inquiry-orientation` rendered the note and no deterministic related material, and `--current-observations` / `--current-facts` remained empty.

### Runtime CLI input path

`Runtime.handle_user_message(...)` records user text as an `input.user_message` event and only then projects state and composes a decision input. `DecisionInputComposer.compose(...)` places the input event payload in the `CURRENT_INPUT` section of a `DecisionInputPacket`. That route makes user input visible to decision production, but it still does not create an `Observation`.

This is an important counterexample to observation-first claims: runtime input can exist as an input event/current-input packet before any canonical observation exists.

### File-backed external representation path

`InputInspector.inspect_file(...)` reads file bytes, hashes the full file, samples a bounded prefix, detects empty/binary/unknown text conditions, records warnings, and returns an `InputArtifact` with path, size, sha256, extension, declared purpose, detected format, confidence, and warnings. The class describes this as audit metadata and bounded content classification for an input file. It does not execute content or resolve embedded references.

This is direct evidence for an implementation-visible external-representation artifact prior to observation in file-backed paths. It is not universal, but it is real.

### Provider translation and observation creation

`AnsibleInventoryObservationSource.collect()` first calls `InputInspector.inspect_file(...)`, stores the resulting `InputArtifact`, chooses INI/YAML parsing from detected format with extension fallback, rejects unsupported formats, parses the provider grammar, and only then constructs `Observation` objects. Observation metadata preserves input path, sha256, detected format, and warnings.

`Observation` itself is a canonical external observation with required `source_type`, `observed_at`, `subject`, `predicate`, `value`, confidence, metadata, dimensions, and optional expiry. Its constructor rejects secret fields and bounds confidence. `ObservationIngestor` then converts an observation into an `observation.observed` event, an `evidence.observed` event, and optionally a fact event. This confirms observation is a meaningful constitutional transition, but not necessarily the first transition for every input path.

## Earliest constitutional transition

### General answer

The earliest implementation-backed constitutional transition after Null is:

```text
Null
↓
Bounded external representation is present to an existing local responsibility
```

That transition is supported only where implementation has a concrete local responsibility that can preserve or inspect the representation without overclaiming. Examples:

- Inquiry-note preservation can say raw operator prose exists for the orientation probe.
- Runtime can say an `input.user_message` event exists.
- File intake can say an `InputArtifact` exists for file bytes.
- Provider adapters can say source-specific bytes/text/rows were accepted enough to attempt provider translation.

### Specific answer for `.`

For the minimal probe `.` in the recent null experiment, the earliest transition is:

```text
Null
↓
Preserved inquiry note exists: raw_note = "."
```

The first lawful participant is Inquiry Orientation, but only after the note is preserved. Its participation is limited to read-only orientation over the note and already projected state. It can also truthfully report no deterministic related material and no supportable lexical overlap.

Observation is not the first transition in this path because no canonical `Observation` object or observation event is created by recording the note or rendering orientation.

## Boundary analysis

### Can the repository truthfully acknowledge an external representation before observation exists?

Yes, in implemented paths. It can acknowledge a preserved inquiry note, runtime input event, or file `InputArtifact` without creating an `Observation`. These acknowledgments are narrower than observation and must not be promoted into repository truth.

### Does implementation distinguish `External Representation Exists` from `Observation`?

Yes, but in a distributed way:

```text
InquiryNoteRecord != Observation
input.user_message event != Observation
InputArtifact != Observation
provider-local decoded/parsed records != Observation
Observation != Evidence != Fact
```

The distinction is implementation-backed by separate dataclasses/events/conversion steps and by the absence of observation/fact mutation in the `.` experiment.

### Is there a repository-visible artifact representing only "repository-visible external representation" prior to observation?

There is no universal artifact with that exact name or scope. There are several local artifacts or records that can play that role inside their bounded contexts:

- `InquiryNoteRecord` for inquiry-orientation probe prose.
- `input.user_message` event for runtime user input.
- `InputArtifact` for file-backed input inspection.

Because these are local and responsibility-specific, the stable boundary is recoverable as a pattern, not as a new global object.

### Does any existing bounded responsibility become eligible before observation exists?

Yes, depending on input path:

- Inquiry Orientation becomes eligible after an inquiry note exists.
- Decision input composition becomes eligible after an `input.user_message` event exists.
- Provider-specific translation becomes eligible after source-specific intake/inspection accepts enough shape to parse.
- File-backed provider parsing becomes eligible after `InputArtifact` exists.

For the `.` probe, the answer is specifically Inquiry Orientation.

## Comparative analysis

### Model A

```text
Null
↓
Observation
↓
Inquiry
```

Model A is too strong for current implementation. It fits canonical observation-source ingestion after an `Observation` object exists, but it fails the operator-prose and file-intake evidence. The `.` path preserves an inquiry note and renders orientation while current observations/facts remain empty. Runtime user input is recorded as `input.user_message`, not as an `Observation`. File intake returns `InputArtifact` before Ansible constructs observations.

### Model B

```text
Null
↓
External Representation Exists
↓
Existing bounded responsibility may now participate
↓
Observation
↓
Inquiry
```

Model B is more strongly supported if narrowed:

```text
Null
↓
Bounded external representation exists for a specific implemented responsibility
↓
That responsibility may inspect, preserve, route, or stop within its authority
↓
Observation is created only when a source/provider contract emits a valid Observation
```

The phrase `External Representation Exists` must not imply a universal repository object, central gateway, semantic admission, or automatic attachment. It is a distributed condition evidenced by specific local records.

## Counterexamples

### External representation immediately becoming observation

Some observation providers construct observations during collection, but reviewed examples still include local validation/extraction first. `AnsibleInventoryObservationSource` uses `InputArtifact` and parser acceptance before observations. `RepositorySourceObservationSource` reads allowlisted Python source files, extracts import/definition relationship facts, and then constructs observations. JSON observation import may appear closest to immediate promotion, but prior investigation found it still requires a top-level object, an `observations` array, entry objects, required fields, valid metadata/datetime/id/confidence, and `Observation` validation.

Thus no strong counterexample was found where an arbitrary external representation immediately becomes an observation with no implemented boundary.

### Repository-visible existence already owned by another recurring responsibility

Yes. This is the strongest counterexample to naming Observation as the first universal transition and also to inventing a new global external-representation subsystem. Existence-before-observation is already owned locally by recurring responsibilities:

- inquiry-note preservation;
- runtime input event recording;
- file input inspection;
- provider-local intake/translation;
- source-specific observation adapters.

### Observation as first constitutional transition with no earlier implementation evidence

Observation is the first transition only for paths where the externally supplied material is already inside an observation-source contract that emits `Observation` records and no earlier local artifact is exposed or relevant. It is not the first transition for `.` and not the first transition for file-backed Ansible intake.

## Supported conclusions

1. The first implementation-backed transition after Null is a bounded external representation becoming present to an existing local responsibility, not interpretation or universal observation.
2. For `.` specifically, the first transition is preserved inquiry note existence; no observation, evidence, or fact is created.
3. The repository can truthfully acknowledge external representation before observation exists, but only through local records such as `InquiryNoteRecord`, `input.user_message`, or `InputArtifact`.
4. Implementation distinguishes external representation from observation through separate local shapes and conversion boundaries.
5. Inquiry Orientation is the first bounded responsibility eligible to participate in the `.` probe, and its participation is read-only and lexical/absence-oriented.
6. Observation remains the first lawful participant only for paths that start inside an observation-source contract and have no implementation-visible prior intake/preservation record.
7. A stable boundary is recoverable as a recurring distributed pattern, not as a centralized artifact or subsystem.

## Unsupported conclusions

- Unsupported: Observation is always the first constitutional transition after Null.
- Unsupported: Attachment is always the first constitutional transition after Null.
- Unsupported: Interpretation is needed before Seed can acknowledge anything.
- Unsupported: There is a universal `ExternalRepresentation` object, admission gateway, null manager, or attachment engine.
- Unsupported: The period `.` means anything semantically.
- Unsupported: Inquiry Orientation may infer operator intent, command, goal, next action, or repository ownership from `.`.
- Unsupported: Preserving an inquiry note, input event, or `InputArtifact` mutates cluster truth.

## Confidence

High confidence for the `.` path: preserved inquiry note is earlier than observation, and Inquiry Orientation is the first eligible bounded participant.

High confidence that `Observation` is distinct from `Evidence` and `Fact`, and that observation creation is a meaningful later transition.

Medium-high confidence that the broader boundary is stable and recurring, because multiple local implementations support existence/intake before observation, but no universal external-representation artifact exists.

Medium confidence on repository-wide generalization: some providers may expose only observation-level records to downstream callers, so the safer claim is distributed bounded external-representation presence, not a single mandatory stage.

## Final answer

When Seed encounters the smallest possible external representation `.` in the current implementation, the very first truthful thing it is constitutionally permitted to acknowledge is:

```text
A raw inquiry note containing "." exists in the inquiry-orientation probe store.
```

The first existing bounded responsibility allowed to participate is:

```text
Inquiry Orientation
```

It may only render a read-only orientation against already projected state and may truthfully stop with no deterministic related material. It may not create observation truth, semantic interpretation, attachment, command, goal, plan, or repository knowledge from the period.

Therefore the implementation more strongly supports narrowed Model B than Model A:

```text
Null
↓
Bounded external representation exists for a specific implemented responsibility
↓
That responsibility may participate within its local authority and may stop unknown
↓
Observation exists only if a source/provider contract emits a valid Observation
```
