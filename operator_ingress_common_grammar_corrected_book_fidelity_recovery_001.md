# Operator-Ingress Common-Grammar Corrected-Book Fidelity Recovery 001

## Scope and governing question

This is one report-only recovery of the production witness reached by invoking bare `seed` (the no-argument path in `scripts/seed_local.py`) against the active Book corrected through PR 2054. It asks:

> What exact production road currently exists from bare `seed` operator ingress through common-grammar treatment selection and return to the persistent console, which responsible consumer owns each occurrence, and where is that road faithful, unfaithful, disconnected, or Unknown relative to the corrected Book?

The implementation scope is `scripts/seed_local.py::run_persistent_operator_console`, `seed_runtime/operator_ingress_common_grammar_prerequisite.py`, `seed_runtime/operator_ingress_representation.py`, `seed_runtime/closed_choice_selection_binding.py`, `seed_runtime/events.py`, `seed_runtime/state.py`, `seed_runtime/bounded_operator_goal_establishment.py`, the direct external-grammar surface discovered in `seed_runtime/candidate_external_grammar.py`, and `tests/test_operator_ingress_bootstrap.py`. The comparison authority is the nine active chapters named in the request.

This report treats occurrence, artifact, preservation, projection, and consumer uptake separately. It assigns responsibility to functions or calling boundaries, not to a probe, Event, projection, ledger, choice set, treatment, boundary, or view by identity. “Production” below means the actual no-argument CLI path unless a programmatic-only branch is expressly identified. An Event's responsibility string is recorded testimony, not independent proof that the named constitutional competency exists.

## Corrected Book expectation

The corrected Book expectation is a guarded prerequisite topology, not a compulsory workflow:

1. **Preserved operator material.** One exact operator-ingress occurrence, its material and provenance remain recoverable. Capture occurrence is not the captured artifact; preservation does not prove a later consumer can reopen it.
2. **Exact consumer and attempted act.** An exact bounded-operator-goal-establishment (BOGE) consumer attempts to examine that exact material for its declared consumer-local act. BOGE names a constitutional boundary, not necessarily a Python object named BOGE.
3. **Common-grammar constraint.** Evidence shows that consumer cannot presently examine that material under an applicable common grammar. Representation examination or decoded text does not establish interpretation or that constraint.
4. **Available treatment-choice representation.** A responsible producer may form and a responsible presenter may present a bounded affirmative/negative communication-probe representation. Production is not presentation, presentation is not receipt, and the enum is not an interpretation menu.
5. **Response alternatives.** An exact affirmative member can select only bounded common-grammar-acquisition treatment; an exact negative member can select only local-stop treatment; nonmembership can establish only unsupported binding while meaning, intent, and requested treatment remain Unknown.
6. **Responsible selection.** Binding finding is not selection. A separate responsible occurrence selects the treatment. Selection supplies neither interpretation nor authority.
7. **Possible later acquisition.** Affirmative selection may be followed by separately examined applicability, movement selection, authority, and a responsible acquisition occurrence. None is entailed by selection and none is mandatory in this bounded witness.
8. **Possible later Demand examination.** Separately evidenced retry recurrence may become input to a responsible Demand examination; recurrence is not examination, establishment, or movement. Retry count may be zero.
9. **Possible later stopping.** Negative selection may be followed by a separate competent stopping occurrence. Selection and function return do not establish it. Local stopping is not process termination or completion.
10. **Possible later examination of the same preserved ingress.** Newly available material may support a responsible re-examination of the identical preserved ingress. Resource availability is not interpretation, ledger preservation is not re-examination, and projection visibility is not uptake.

Thus the locally expected continuous core is preservation → evidenced exact-consumer common-grammar constraint → probe formation → presentation → response occurrence/capture → exact-set finding → responsible treatment selection. The acquisition, Demand, stopping, re-examination, and BOGE establishment relations are possible later, separately owned occurrences, not automatically required implementation scope.

## Current production inventory

| Occurrence or material | Responsible production boundary | Input | Output/standing and provenance | Scope / authority | Direct and possible consumers |
|---|---|---|---|---|---|
| Console recurrence | `run_persistent_operator_console` | no-argument CLI, stdin/stdout, process-local ledger | banner and a `while True` capture cycle | workspace/session; recurrence only | outer EOF/`exit` inspector, or bounded attempt |
| Initial capture occurrence | `capture_stdin_material`, called only by the console for ordinary production ingress | one `sys.stdin` frame | `CapturedOperatorMaterial` with exact boundary bytes, EOF, delimiter testimony, boundary, byte origin, encoding testimony, and known loss | one frame; occurrence evidence only | outer inspector, then the attempt with the same object |
| Initial raw preservation | `_capture_representation` in the attempt | the already-captured object | `operator.bootstrap.raw_material_captured`; exact bytes as hex and supplied capture testimony | attempt/workspace/session/role; `mutates_cluster=false` | representation examiner; projector on replay |
| Representation examination | `examine_text_representation`, recorded by `_capture_representation` | exact captured bytes plus encoding testimony or UTF-8 fallback | strict decoder result: `decoded`, `decoder_unavailable`, or `bytes_rejected` | capture occurrence; decoder evidence only | attempt branching; projector |
| Ingress occurrence recording | attempt | decoded text or EOF plus raw/examination lineage | `operator.bootstrap.ingress_occurred` or programmatic `initial_eof_occurred`; meaning expressly Unknown | workspace/session; occurrence only | identity/lineage source for the probe on non-EOF; projector; no prerequisite material consumer evidenced |
| Probe representation | `bootstrap_choice_set` and `render_probe`, orchestrated by attempt | presentation identity derived from ingress Event | exact two-option representation plus `operator.bootstrap.probe_produced` | one attempt; exact local token invitation only | stdout presenter; later validator |
| Presentation occurrence | attempt's `output_stream.write/flush`, then `_record` | rendered representation | bytes/text sent toward real-shell stdout and `operator.bootstrap.presentation_occurred` | one attempt; no acquisition/stopping authority | human is candidate recipient; actual receipt/interpretation Unknown; response capture follows in control flow |
| Response raw capture and examination | `_capture_representation` | the same input stream, now read once by the attempt | separate `CapturedOperatorMaterial`, raw Event, decoder evidence | enum-response role in same attempt | EOF/failure branch or response occurrence producer |
| Response occurrence | attempt | decoded framed response | `response_eof_occurred`, or `response_captured` with exact token text and probe identity | exact choice set; meaning and intent Unknown before binding | validator/binder for non-EOF; projector |
| Exact-set binding | `validate_capture_for_probe` then `bind_closed_choice_selection` | current recorded presentation, fingerprint, current unconsumed response capture | bound or unsupported `ClosedChoiceSelectionBinding`; corresponding Event | exact presented set; read-only, no goal/acquisition/authority | treatment selector only if bound; projector |
| Treatment selection | attempt | bound option reference and binding Event | `operator.bootstrap.treatment_selected`, `selected_treatment` of `common-grammar-acquisition` or `local-stop` | one attempt; selection only | stdout result and projector; no constitutional downstream consumer |
| Unsupported finding | attempt | non-bound exact-set binding | `operator.bootstrap.unsupported_finding` plus three semantic Unknowns | one attempt / exact set | stdout result and projector only |
| Stopping occurrences | attempt, only on representation failure or EOF branches | examination failure or EOF occurrence | `operator.bootstrap.stopping_occurred`, `closed=true`, interaction closure | one attempt; claims competent local stop only | stdout and projector |
| Projection | `StateProjector.apply` dispatching to `project_bootstrap_events` | all `operator.bootstrap.*` Events | `state.operator_ingress_bootstraps[attempt]` visibility | workspace replay; no cluster mutation | returned to caller then ignored by console; tests inspect it |
| Initial-ingress constitutional consumption before probe | none on bare-console road | decoded ingress Event | probe identity and lineage reference exist, but no examination, assertion adoption, material use, or constitutional uptake | not established | no exact prerequisite consumer evidenced |
| Later constitutional consumption | none on bare-console road | projected/raw preserved ingress or selected treatment | no acquisition, Demand, re-examination, authority, stopping-after-negative, or BOGE result | not established | none evidenced |

The in-memory bare CLI ledger records Events for the duration of the process. The implementation also supports durable replay when a `SQLiteEventLedger` is supplied programmatically, but bare `seed` constructs `EventLedger`; therefore cross-process durability is absent on the exact default road.

## Actual producer-to-consumer topology

```text
bare `seed` / no argv
  scripts.seed_local.main
    -> process-local EventLedger
    -> run_persistent_operator_console
         emits one console banner
         |
         +== outer persistent-console recurrence ============================+
         | capture_stdin_material(input_stream)                              |
         |   -> one CapturedOperatorMaterial                                 |
         |                                                                  |
         | outer inspection:                                                 |
         |   EOF -------------------------------> return from console/process|
         |   exact encoded `exit` ----------------> return from console/process|
         |   ordinary frame                                                  |
         |      -> pass SAME capture object (no recapture)                   |
         |      -> run_operator_ingress_common_grammar_probe_attempt         |
         |          +-- bounded one-attempt function ---------------------+  |
         |          | record raw initial bytes                           |  |
         |          | -> strict representation examination              |  |
         |          |    failure -> record local stopping -> stdout -> return
         |          | -> record decoded ingress (meaning Unknown)        |  |
         |          | -> form two-choice probe -> record probe produced  |  |
         |          | -> stdout -> record presentation                   |  |
         |          | -> capture a SEPARATE response frame               |  |
         |          | -> strict representation examination              |  |
         |          |    EOF/failure -> record local stopping -> return  |  |
         |          | -> record response capture                         |  |
         |          | -> validate identity/currentness and bind exact set|  |
         |          |    unsupported -> record finding -> stdout -> return
         |          |    bound -> record binding                         |  |
         |          |          -> record treatment selection             |  |
         |          |          -> accurate bounded stdout -> return      |  |
         |          +----------------------------------------------------+  |
         |                                                                  |
         | every `_record`: EventLedger.append (durable only with supplied   |
         | SQLite ledger; default is process-local)                          |
         | every return projection: StateProjector replays Events            |
         | returned attempt view: ignored by persistent console              |
         |                                                                  |
         +-- next loop iteration captures a FRESH ingress occurrence --------+

Downstream constitutional consumption:
  selected treatment ----X----> acquisition / authority / Demand
  preserved ingress -----X----> same-ingress re-examination / BOGE
  local-stop selection ---X----> competent stopping

Separate implementation islands:
  caller-supplied CandidateExternalGrammarSet CLI (no identity/lineage/invocation link)
  BOGE from admitted interpretation (different artifact road)
  closed-choice BOGE adapter (always refuses; tests only, not invoked by console)
```

Control flow proves that the projector consumes recorded Events. It does not prove that a human received the probe, that a later constitutional consumer used projected material, or that console recurrence continues the previous attempt.

## Initial-ingress capture and preservation

The persistent console is the sole production owner of **initial** stdin capture on the bare road. It calls `capture_stdin_material` once before inspection and passes that exact frozen `CapturedOperatorMaterial` object to the bounded attempt. The attempt records it; it neither reads initial ingress again nor impersonates replay. Response capture is separately owned inside the attempt.

For real `sys.stdin`, capture uses `stdin.buffer.readline`: the observed bytes are exact at that boundary, with `direct_boundary_observation` origin. The only declared loss is transport bytes before that byte-stream boundary. Delimiter testimony is `0d0a` for CRLF, `0a` for LF, otherwise `None`; delimiter bytes remain in `exact_bytes`. `encoding_testimony` is the stream's encoding, not a source-relative encoding verdict. Strict decoding uses that testimony, or an implementation UTF-8 fallback if none exists. A programmatic text-only stream is compatibility-adapted by re-encoding and honestly declares the original bytes and prior decoder unavailable.

The capture boundary is framed `readline`, not the transport before stdin. EOF is exact empty bytes. The outer console owns production initial EOF and returns without handing it to the attempt, recording an Event, or producing local-stopping testimony. The direct attempt's initial-EOF Event/stop branch exists but is unreachable from the bare console because the outer owner intercepts EOF. Exact outer `exit` handling removes a terminal LF then CR from bytes and compares against exactly `"exit"` encoded under stream testimony or UTF-8; lookup failure means “not exit.” It does not record the `exit` frame. This inspection is a process-console command boundary, not interpretation of ordinary ingress.

After any response branch reached from a non-failing initial representation, original ingress is preserved in raw hex and decoded occurrence Events with capture/examination lineage. Initial representation failure preserves raw hex and examination evidence but never creates `ingress_occurred`; this is honest because no decoded ingress occurrence is claimed. In a supplied SQLite ledger these Events can be replayed after reopen. In bare `seed`, they are visible only while the in-memory ledger lives and disappear with the process.

The four required findings are therefore separate:

- **Preserved and visible:** yes, within the live ledger/projection on every bounded-attempt return; persistently reopenable only when a persistent ledger is supplied.
- **Consumer available:** no exact prerequisite consumer is evidenced before probe production. Projection replay is available, and probe production is identity- and lineage-linked to the ingress Event, but linkage is not material consumption.
- **Consumer applicable:** Unknown; no applicability examination is recorded.
- **Actually consumed:** no constitutional ingress examination or material-use occurrence is evidenced before probe production. The initial occurrence supplies probe identity and lineage, but that does not establish reading its material, adopting its assertion, examining its meaning, using its standing, or constitutional uptake. It is not later consumed for interpretation, acquisition, Demand, BOGE, or re-examination.

## Bounded-attempt responsibility

“One attempt” is a **faithful bounded responsibility for the treatment-choice interaction**, and a local implementation decomposition, but it is **not by itself a faithful complete ingress-prerequisite examination**. Its evidenced constitutional completion is, depending on branch, one treatment selection, one unsupported exact-set finding, or one separately recorded local stop for EOF/representation failure. It is not a hidden multi-retry conversation: it captures one initial frame already owned by the console and at most one response frame, then returns.

The important discontinuity occurs before probe production. The attempt records decoded initial text with “meaning Unknown,” but no exact BOGE consumer attempts examination, no consumer-local common-grammar requirement is represented, and no responsible finding establishes inability to examine under applicable common grammar. Nevertheless every decodable non-EOF ordinary frame unconditionally causes the treatment probe. That crossing is unfaithful to the corrected guarded prerequisite if the implementation claims the whole prerequisite road: decoded text and unknown meaning are being used as substitutes for the exact-consumer constraint finding. The later probe/presentation/binding/selection acts can still be faithful local support inside their exact narrower scope.

A return completes Python control flow only. Affirmative, negative, and unsupported returns do not record interaction closure. The persistent console then recurs and captures a fresh frame. The return is neither competent stopping nor re-examination, and the next attempt does not retain the old attempt identity, capture identity, selected treatment, or ingress lineage.

## Affirmative branch

For exact token `1`, the binder produces a bound finding and the attempt records `operator.bootstrap.treatment_selected` with `selected_treatment="common-grammar-acquisition"`, binding lineage, `standing="selected"`, and authority “selection only; acquisition not authorized or begun.” State exposes that selection. Stdout says: “Common-grammar acquisition treatment selected; acquisition was not authorized or begun.” The attempt returns; the console ignores the returned view and captures a new frame as a new attempt.

Classification by coordinate:

- **Treatment-selection witness:** faithful within exact implementation scope. Binding and responsible selection are separate Events and the claim is selection-only.
- **Continuation ownership:** console-local recurrence is evidenced; constitutional continuation of the selected treatment is not.
- **Preserved-ingress continuity:** the old Events remain in the ledger/projection, but no lineage leaves the old attempt for a later act.
- **Later-consumer availability:** no acquisition, applicability, authority, Demand, re-examination, or BOGE consumer accepts this selected treatment or preserved ingress. Projection visibility is not availability of a competent consumer.
- **Default-console observable behavior:** it accurately disclaims acquisition, then silently returns to the general console loop. The next frame is unrelated fresh ingress by implementation identity.

Accordingly, the bounded selection endpoint itself is faithful. The default console does not falsely label the next frame continuation, retry, or re-examination, so zero later acquisition is not automatically unfaithful. It is nevertheless a **disconnected witness** beyond selection: the only default continuation is reset-like fresh ingress, and no consumer owns the affirmative result or same preserved ingress. Whether a product requirement intended constitutional continuation is Unknown; the implementation makes none.

## Negative branch

For exact token `2`, the same binding and selection road records `selected_treatment="local-stop"`. It does **not** record `operator.bootstrap.stopping_occurred`, set `closed`, or create `interaction_closure`. No competent stopping consumer acts. The attempt writes: “Local-stop treatment selected; bounded stop was not established.” It returns, the console continues, and a new initial frame is captured under a new attempt.

These are distinct standings:

- local-stop treatment selection: established;
- function return: occurred;
- interaction completion as a broad lifecycle claim: not recorded and Unknown;
- bounded stop: expressly not established;
- console termination: did not occur;
- process termination: did not occur unless later outer EOF/`exit` occurs.

The stdout is faithful to the evidence. Negative selection is therefore faithful in its exact selection-only scope and disconnected from stopping, not an unfaithful attempt to establish stopping. The Book makes a later competent stop possible, but the implementation does not claim it is mandatory or performed.

## Unsupported branch

For any token outside the exact set—including empty and whitespace variants—the binder records `operator.bootstrap.unsupported_finding`. Exact-set nonmembership is known. The Event/projection retains “response meaning Unknown,” “operator intent Unknown,” and “requested treatment Unknown.” No refusal, treatment selection, stopping, retry requirement, or Demand is recorded.

The attempt says “Unsupported response: exact token 1 or 2 required.” Here “required” describes membership needed by this exact binder, not a constitutional requirement to retry. It returns. The projection marks both presentation and response `consumed`, but those standings have different support: the binder used the exact response capture, while response occurrence does not prove external receipt, interpretation, use, reliance upon, or constitutional consumption of the presentation. The presentation and original ingress remain reconstructable from the live process-local Event history. They are durably reconstructable across process boundaries only when a persistent ledger is supplied. No active retry consumer re-presents or reopens either artifact. The console captures the next frame as a new attempt, not as a retry: new attempt identity, new initial-capture role, no prior presentation reference, and no lineage to the prior unsupported finding.

Zero retries is Book-permitted, so their absence is not unfaithful. The console makes no explicit retry or recurrence claim, so fresh capture does not falsely establish either. No recurrence evidence is formed even if multiple unsupported attempts occur; mere adjacency or similar text would not suffice. This branch is faithful for unsupported/Unknown binding and disconnected after return.

## EOF and representation-failure stopping

Four potential branches must be separated:

1. **Initial EOF on bare production:** `run_persistent_operator_console` detects the `CapturedOperatorMaterial.eof` and returns. It produces no bootstrap Event and no `stopping_occurred`. This is outer console/process control, not the attempt's competent local stopping.
2. **Direct/programmatic initial EOF:** if the attempt is called directly with an EOF capture, it records raw capture, `operator.bootstrap.initial_eof_occurred`, then a distinct `operator.bootstrap.stopping_occurred` sourced from that occurrence, with `closed=true`, `response_kind="initial_eof"`, attempt scope, and authority limited to closing this interaction.
3. **Response EOF:** the attempt records response raw capture, `response_eof_occurred`, then a distinct stopping Event with `closed=true` and attempt-local authority. It does not create a normal response capture or binding.
4. **Initial or response representation failure:** `_capture_representation` first records raw bytes and the exact decoder outcome. The attempt then records a separate stopping Event sourced from that examination, closes only the attempt, writes the exact implementation message `representation insufficiency` or `response representation insufficiency`, and returns. Those messages are stale retired-scalar residue that compresses the distinct `decoder_unavailable` and `bytes_rejected` outcomes; the upstream examination evidence preserves the distinction. Initial failure occurs before an ingress occurrence; response failure occurs after presentation but before response occurrence/binding.

For the three attempt-owned categories, producer, source, scope, lineage, closed standing, and negative authority are explicit. They are faithful implementation witnesses of separately recorded **local** stopping occurrences within the attempt's declared competency. Whether the self-description `competent-local-stopping` is constitutionally warranted beyond the implementation's deliberately tiny interaction boundary remains Unknown because the Book leaves the exact stopping warrant unresolved. They do not close the persistent console, which recurs after failure/response EOF. That is not contradictory because local stop differs from process termination.

The asymmetry with negative selection is intentional and accurately exposed: selecting local-stop records no stop, whereas EOF or representation failure creates a separate stop. Function returns exist in all cases and add no stopping standing.

## Projection and current visibility

`StateProjector.apply` sends every `operator.bootstrap.*` Event to `project_bootstrap_events`. Per attempt, the projection preserves Event ids; an eight-dimensional snapshot per occurrence; lineage; raw-initial/raw-response material; representation-examination details; current subject slots; accumulated known loss, Unknowns, and conflicts; and selected scalar conveniences such as `selected_treatment`, `closed`, and `response_kind`.

| Projected subject | Source Events | What becomes visible | Known loss / Unknown / conflict treatment | Consumer standing |
|---|---|---|---|---|
| `preserved_ingress` | ingress or initial-EOF occurrence | decoded occurrence dimensions forcibly shown as `preserved`, raw lineage elsewhere | capture known loss accumulated; meaning remains limited by Event authority | visibility, not constitutional preservation consumer by identity |
| `produced_probe` | probe-produced Event | rendered content, identity, fingerprint lineage | no receipt/interpretation | formed representation only |
| `presentation` | presentation Event | stdout occurrence; later changed in the projection to `consumed` when response appears | external receipt, interpretation, use, reliance, and meaning remain Unknown | **unfaithful projected-standing crossing**: response capture does not warrant presentation consumption |
| `response` | response-captured or response-EOF Event | response occurrence; normal response changed to `consumed` at binding | unsupported branch accumulates semantic Unknowns at binding | faithful local material-use support only for the exact validator/binder relation |
| `binding_finding` | completed or unsupported Event | exact-set bound/unsupported result | unsupported semantic Unknowns retained | binding, not treatment selection |
| `treatment_selection` | treatment-selected Event | selected option and scalar | acquisition, authority, stopping not projected as performed | selection only |
| `interaction_closure` | stopping Event | closed local attempt and evidence | stopping competency beyond local claim Unknown | local stopping testimony |

The projection mutates its own nested current snapshots by setting presentation and response to `consumed`, but the two crossings are not equivalent. The exact-set validator reads and validates the current recorded response capture, so response consumption has faithful local material-use support within that exact binder scope. A response occurrence does not prove that an external operator received, interpreted, used, relied upon, or constitutionally consumed the presentation; that projected presentation standing is an **unfaithful projected-standing crossing**, while external receipt and interpretation remain Unknown. Retaining each original occurrence in `dimensional_standing` prevents erasure but does not warrant the stronger projected standing. `current_standing` is a dictionary name, not constitutional current standing by identity, and asserts no as-of/freshness or downstream applicability contract.

`interaction_closure` is absent on affirmative, negative, and unsupported returns. This is **meaningful and benign** in the narrow projection: no stopping Event exists, and the implementation does not fabricate one from return. It is not proof the interaction remains constitutionally open, because no lifecycle consumer uses the slot. The broader closure standing is therefore Unknown. On recorded stop branches it reflects the stopping Event.

No bare-console caller consumes the returned projection. Tests and programmatic callers can inspect/replay it; that is not production constitutional uptake.

## Downstream consumer recovery

Searches for every named Event kind, `CapturedOperatorMaterial`, both treatment literals, `selected_treatment`, and `operator_ingress_bootstraps` found no production downstream consumer beyond the projector and the within-attempt validator/selector. Imports, similarly named external-grammar code, and test-only reconstruction do not establish consumption.

| Candidate relation | Identity linkage | Lineage / scope / standing / authority | Invocation and material use | Classification |
|---|---|---|---|---|
| Common-grammar acquisition | no consumer references treatment literal outside producer/tests | none | none | absent within current scope; consumer absent |
| Candidate external-grammar admission | separate CLI accepts caller JSON | no attempt, selection, ingress, presentation, or binding refs; no authority link | independently invoked only by its CLI flag | disconnected implementation island |
| Demand examination/establishment | no bootstrap Event or projection consumer | no recurrence, exact ingress/consumer constraint, or Demand lineage | none | absent within current scope |
| Same-ingress re-examination | no consumer reopens raw Event/projection for examination | preserved visibility only; applicability/authority Unknown | none | projection-only visibility, then absent consumer |
| Operator-origin BOGE from this ingress | closed-choice adapter accepts a reconstructed binding type but always refuses; admitted-interpretation BOGE consumes another road | no production bridge from bootstrap Event/binding object; exact ingress absent; console never invokes it | test reconstructs only to prove refusal | disconnected implementation island |
| Competent stopping after negative selection | no consumer | selection expressly lacks stopping authority | none | absent within current scope |
| EOF/failure local stopping | attempt itself records separate act | direct failure/EOF lineage, attempt scope, limited authority | invoked on those branches | directly connected locally; constitutional competency beyond declared boundary Unknown |

The BOGE closed-choice function is especially important: accepting the Python binding type does not make it a consumer of the preserved ingress road. Production never passes the in-memory binding to it; the binding is not retained as an object in the Event; and the function categorically refuses because no goal-specific semantic admission exists. The admitted-interpretation BOGE path consumes `DownstreamInterpretationAdmission`, not bootstrap ingress or treatment selection.

## Implementation vocabulary standing

| Term | Classification | Recovery |
|---|---|---|
| `bootstrap` / `operator-common-grammar-bootstrap` | stale lexical pressure only | Historical implementation namespace suggests universal start, while the corrected Book denies universal bootstrap; behavior remains local to bare console and does not create a global constitutional primitive. |
| `one-attempt` / `probe_attempt` | faithful implementation-local identifier | Accurately bounds one initial object, one presentation, at most one response, and return; it is not constitutional stopping. |
| `probe` | faithful implementation-local identifier with mild ambiguity | Behavior is the Book's communication-probe representation. It is not an examination execution or interpretation menu. |
| `probe-production` | faithful implementation-local identifier | Separate from recorded presentation and response. |
| `treatment_selected` / `treatment-selection` | faithful implementation-local identifier | Separate from binding and explicit negative authority. |
| `interaction_closure` | compatibility identifier | Projection slot maps only recorded stopping Events; absence on ordinary returns avoids reifying return, but “closure” could be overread without Event evidence. |
| `representation insufficiency` / `response representation insufficiency` | stale lexical pressure with bounded behavioral consequence | Exact quoted implementation strings compress distinct decoder outcomes in later Event content, `response_kind`, and stdout. Exact `decoder_unavailable`, `bytes_rejected`, and `decoded` evidence remains distinguishable upstream; the shorthand is not adopted constitutional grammar. |
| `common-grammar-acquisition` | compatibility identifier | Correct as a treatment option; behavior and stdout refuse acquisition applicability, authority, and performance. |
| `local-stop` | compatibility identifier | Correct as a selected treatment; output explicitly says stop not established. |
| `operator-ingress` responsibility string | misleading responsibility assignment | The attempt is the actual Event producer and records an occurrence attributed to operator ingress; the string can look like an agent/consumer. Behavior limits it to occurrence-only meaning Unknown, reducing but not eliminating pressure. |
| `competent-local-stopping` | behaviorally consequential pressure / Unknown warrant | It affirmatively claims competency for EOF/decoder-failure stopping. Scope and separate occurrence are good, but constitutional competency is not independently examined. |
| `seed_runtime.operator_ingress_bootstrap:v1` provenance | stale constitutional residue | The provenance string names an older/non-current module form and bootstrap vocabulary; it does not alter the actual fingerprinted two-option behavior. |

The retired scalar vocabulary encountered in implementation is quoted here only as evidence and is not promoted to corrected constitutional grammar.

## Test testimony

`tests/test_operator_ingress_bootstrap.py` is compatibility testimony after production recovery, not constitutional warrant.

- **Capture provenance and ownership proved:** real-buffer exact bytes, LF/CRLF delimiter testimony, encoding testimony, direct byte origin, text-adapter loss, same capture object passed unchanged, response ownership inside attempt, and no alternate parser controller.
- **Single-capture continuity proved:** monkeypatch testimony proves the outer capture is passed without recapture; Event/projection reconstruction is proved in the live process, while cross-process replay requires a supplied persistent ledger. It does not prove a later constitutional consumer reopens the preserved ingress.
- **Exact-set binding proved:** exact options select; near matches are unsupported; presentation identity, set reference, fingerprint, current capture, and single consumption are guarded.
- **Selection-only standing proved:** both treatments record selection without acquisition, Demand, interpretation, cluster mutation, or stopping; stdout preserves negative authority.
- **Local-stop non-establishment proved:** token `2` lacks stop Event/closed standing and the persistent console starts another interaction.
- **Unsupported Unknowns proved:** response meaning, operator intent, and requested treatment remain Unknown; no selection or stop occurs.
- **EOF/failure stopping proved:** direct initial EOF, response EOF, and both representation failure kinds record separate local stops with expected lineage and decoder distinctions.
- **Console recurrence proved:** multiple attempts occur after local-stop and unsupported responses; outer exact `exit` is excluded from bootstrap Events.
- **Same-ingress later continuity not proved:** tests prove preservation and replay, not downstream reopening or re-examination.
- **Consumer availability not proved:** the BOGE test reconstructs an immutable binding and proves the adapter refuses it. That is evidence of disconnection, not production uptake.
- **Common-grammar constraint left unexamined:** no test demonstrates an exact BOGE consumer attempted to examine the ingress and found common grammar unavailable before probe production.
- **Initial-ingress consumption not proved:** tests prove the identity-derived presentation reference and probe lineage, not prerequisite examination, material use, assertion adoption, or constitutional uptake.
- **Projected standings have unequal support:** tests prove the exact validator uses the current response capture, but response occurrence proves neither presentation receipt nor interpretation; preserving the original presentation snapshot does not warrant projecting it as consumed.
- **Retired decoder wording is only implementation residue:** tests preserve exact decoder outcomes upstream while also testifying that later Event/output surfaces compress failure branches under the quoted stale scalar strings.
- **Durability is conditional:** bare-console tests exercise live in-memory history; durable cross-process reconstruction is available only through tests or callers supplying a persistent ledger.
- **Stopping competency assumed locally:** tests verify the recorded `competent-local-stopping` label and attempt closure but do not independently warrant constitutional competency.

Passing tests therefore preserve the implemented boundaries, including intentional non-establishment, while leaving the largest prerequisite and downstream consumer boundaries unproved.

## Fidelity classification table

| Major boundary | Classification | Basis |
|---|---|---|
| Persistent-console capture ownership | faithful within exact implementation scope | sole real initial capture; same object passed; response capture delegated explicitly |
| Outer EOF / `exit` ownership | faithful local support but not constitutional act | exact console termination inspection; ordinary ingress is not interpreted; no false stopping Event |
| Bounded attempt responsibility | faithful local support but not constitutional act | bounded treatment interaction, not full prerequisite/goal lifecycle |
| Common-grammar constraint before probe | unfaithful boundary crossing | no exact consumer examination/finding; all decodable ordinary ingress triggers probe |
| Initial ingress before probe | identity/lineage linked but not constitutionally consumed | `presentation_ref` derives from ingress identity and probe lineage contains the ingress Event id; no prerequisite examination or material-use occurrence |
| Probe production | faithful local support but not constitutional act | exact two-treatment representation with negative authority; missing prerequisite warrant upstream |
| Probe presentation | faithful within exact implementation scope | real stdout emission separately recorded; receipt/interpretation not claimed |
| Response capture | faithful within exact implementation scope | separate framed bytes/examination and occurrence lineage |
| Presentation projected as `consumed` | unfaithful projected-standing crossing | response occurrence does not evidence external receipt, interpretation, use, reliance, or constitutional consumption |
| Response projected as `consumed` | faithful local support within exact binder scope | exact-set validator reads and validates the current recorded response capture; no broader interpretation is established |
| Exact-set binding | faithful within exact implementation scope | identity, fingerprint, currentness, one-use, exact membership; no interpretation/authority |
| Affirmative treatment selection | faithful within exact implementation scope | separate selection Event; no acquisition applicability/movement/authority/performance claim |
| Negative treatment selection | faithful within exact implementation scope | separate selection; explicitly no stop |
| Unsupported finding | faithful within exact implementation scope | nonmembership only; meaning/intent/request Unknown; no refusal |
| EOF stopping | faithful local support but not constitutional act | separate scoped attempt stop; initial production EOF actually remains outer-only |
| Representation-failure stopping | faithful local support but not constitutional act | separate scoped stop with source lineage; ultimate competency warrant Unknown |
| Attempt return | faithful local support but not constitutional act | bounded decomposition only; no stop/closure inference |
| Console continuation | faithful local support but not constitutional act | owns process recurrence but not prior-attempt constitutional continuation |
| Fresh next-frame capture | disconnected witness | new identity with no prior lineage; not falsely called retry/re-examination |
| Preserved-ingress later availability | projection-only visibility / disconnected witness | material visible/replayable, but no competent consumer can reopen it on production road |
| Selected-treatment downstream consumption | disconnected witness | projector/stdout only; returned view ignored |
| Demand relation | Unknown as constitutional applicability; absent within current scope | no recurrence producer, examination, establishment, or movement; not required automatically |
| Acquisition relation | Unknown as constitutional applicability; absent within current scope | no consumer, authority, or movement; omission not automatically defective |
| Re-examination relation | disconnected witness | same ingress preserved, no responsible re-examiner or lineage |
| BOGE relation | disconnected witness | production does not invoke BOGE; closed-choice path refuses; admitted path is independent |
| State projection | mixed witness containing an unfaithful projected-standing crossing | Event visibility, lineage, loss preservation, and exact binder-local response consumption are faithful local support; presentation is nevertheless projected as `consumed` without evidence of external receipt, interpretation, use, or reliance |
| `representation insufficiency` wording | stale lexical pressure with bounded behavioral consequence | later Event/output shorthand compresses distinct decoder failures, while exact decoder outcomes remain distinguishable upstream |
| Bare-road durable replay | absent; live process-local reconstruction only | bare `seed` uses `EventLedger`; cross-process replay requires a supplied persistent ledger such as `SQLiteEventLedger` |
| `bootstrap` lexical family | stale lexical pressure only | corrected Book rejects universal bootstrap, but behavior does not enact one |

## Strongest continuous faithful road

Without skipping a consumer, the longest evidenced continuous faithful **implementation-local** road is:

```text
persistent console captures one ordinary stdin frame at stdin.buffer.readline
-> passes the same CapturedOperatorMaterial to the bounded attempt
-> attempt records exact raw bytes and capture provenance
-> examine_text_representation performs and records one strict decoder examination
-> attempt records decoded ingress occurrence with meaning Unknown
-> identity and lineage link are available
-> [constitutional prerequisite discontinuity:
    no exact BOGE-consumer examination,
    no common-grammar-constraint finding,
    no constitutional material consumption]
```

A second strong continuous local road begins after that gap but cannot erase it:

```text
attempt forms exact two-treatment representation
-> emits it to stdout and records presentation
-> captures/examines one response frame
-> records response occurrence
-> validator consumes the exact current presentation/capture evidence
-> binder produces bound or unsupported finding
-> on bound finding, attempt records separate treatment selection
-> projector consumes Events and stdout reports only the bounded result
-> function returns
```

The first road is the longest faithful road from bare ingress without skipping the missing consumer. The second is a faithful treatment-interaction subroad, not proof that the corrected prerequisite condition warranted its invocation. Neither road continues through acquisition, Demand, stopping-after-negative, same-ingress re-examination, or BOGE.

## Largest missing or unfaithful consumer-local crossings

1. **Unfaithful crossing already performed — common-grammar prerequisite trigger.** Probe production follows decoded ordinary ingress without a responsible exact-BOGE-consumer examination or a finding that applicable common grammar is unavailable. This is required by the claimed corrected prerequisite behavior, not supplied by “meaning Unknown.”
2. **Unfaithful projected presentation consumption.** The projector uses response occurrence as proof that the presentation is `consumed`, although emission and response capture establish neither external receipt nor interpretation. Original-snapshot retention prevents erasure but cannot warrant this stronger standing.
3. **Consumer absent — selected treatment.** Both selections end at Event/projection/stdout; no acquisition or competent stopping consumer accepts them. The production console also provides no bridge to BOGE. These later relations are outside the bounded selection witness unless stronger behavior is claimed, so absence alone is not a defect.
4. **Consumer absent — same preserved ingress.** Events/projector retain the material, but no later re-examination consumer reopens it and no lineage connects a later act; the disconnected BOGE islands do not supply that consumer. Possible later relation, not mandatory witness scope.
5. **Standing or authority Unknown — attempt-local stopping competency.** EOF/failure stopping is separately and narrowly recorded, yet the evidence and authority required to warrant that exact attempt-local stopping responsibility are not established. The negative branch correctly avoids crossing this boundary.

## Remaining Unknowns

- Whether an external operator actually receives, interprets, or understands stdout; only emission toward the shell is evidenced.
- Whether the corrected prerequisite was intended to govern every bare-console frame or only a not-yet-implemented applicability boundary; current production provides no discriminator.
- Whether the evidence and authority required to warrant that exact attempt-local EOF/representation-failure stopping responsibility exist beyond its recorded self-description.
- Whether absence of `interaction_closure` means a constitutionally open interaction; it certainly means no projected stopping Event, but no lifecycle consumer adjudicates more.
- Whether future acquisition, Demand, authority, stopping, re-examination, or BOGE consumers should exist. The Book permits these later relations and does not make them compulsory here.
- Whether bare-console Event preservation was intended to survive process exit. The exact road uses an in-memory ledger; persistent replay is only programmatically available.
- Whether the next fresh frame is intended by product semantics as unrelated work. Implementation identity makes it unrelated and does not call it retry; intent beyond that is Unknown.
- The exact Demand family, applicability, materiality, and establishment standing; no recurrence evidence or Demand examination exists.
- Common-grammar acquisition applicability, candidate movement, authority, and possible acquired resources; treatment selection settles none.
- Any later interpretation, admission, or operator-origin BOGE meaning for the original ingress.

## Required conclusion

The current bare production road is not one uniformly faithful or unfaithful lifecycle. Its strongest continuous road faithfully owns one real stdin capture, preserves exact boundary bytes and loss testimony, performs a bounded decoder examination without calling decoding interpretation, records ingress meaning as Unknown, and establishes identity and lineage linkage into probe production. That linkage is not constitutional consumption. It then crosses the largest corrected-Book gap: no exact BOGE consumer attempts the declared act, no responsible common-grammar-constraint finding exists, and no constitutional material-use occurrence is evidenced before the probe is unconditionally produced.

After that gap, the treatment-choice interaction is carefully faithful in its exact local scope. Probe formation is separate from stdout presentation; response capture is separate from meaning; the binder's use of the exact response supports only response consumption in that material-use relation; exact-set binding is separate from treatment selection; affirmative selection does not acquire or authorize; negative selection does not stop; unsupported nonmembership preserves semantic Unknowns; and EOF/decoder-failure branches alone record separate attempt-local stopping occurrences. Function return never impersonates stopping. Separately, projecting presentation standing as `consumed` after response capture is unfaithful because response occurrence does not prove external receipt or interpretation.

The persistent console owns recurrence, not constitutional continuation. After every affirmative, negative, or unsupported return it ignores the projected result and captures a new frame under a new attempt with no identity or lineage to the old ingress. That next frame is not represented as a retry, recurrence, or re-examination, so the Book-permitted absence of those later acts is not automatically unfaithful. The result is instead disconnected after selection: preservation and projection visibility exist, but no responsible production consumer uses the selected treatment or reopens the same ingress for acquisition, Demand examination, competent stopping after negative selection, re-examination, or BOGE.

Accordingly: **capture, preservation, representation evidence, presentation occurrence, response occurrence, exact binder-local response use, selection-only claims, unsupported Unknowns, and return/stopping distinctions are faithful within their exact local scopes; identity and lineage do not establish constitutional ingress consumption; the prerequisite invocation crosses an unevidenced consumer-local constraint and is unfaithful as a corrected-Book prerequisite witness; projected presentation consumption is a separate unfaithful crossing; retired scalar decoder wording remains stale residue rather than constitutional grammar; bare-road reconstruction is live and process-local rather than durable; and all alleged downstream constitutional continuation is disconnected or Unknown rather than established.**
