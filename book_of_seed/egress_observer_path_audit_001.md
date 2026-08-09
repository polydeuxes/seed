# The egress and observer path: audit 001

Findings only. No runtime or Book amendment.

## Executive

`#2398` said the shuffled control material "was never received as ingress". That
was the wrong diagnosis, and correcting it is half this report.

The corpus is not operator testimony. It is environment. Nothing should reach
Seed through operator ingress except the operator, or ingress quietly becomes
a second privileged entrance and the front door becomes a developer injection
channel wearing a constitutional name.

**Active law already has the outward path**, and names its stages.

**The runtime has an observer path too** — and it collapses observation into
decoded text at a single line, lossily and without recording the loss. It is
**worse than the ingress path it would replace**: ingress decodes strictly and
records rejection as evidence, while the observer substitutes replacement
characters, discards everything after the first line, and reports none of it.

## 1. Correcting `#2398`

```text
withdrawn   "the shuffled material was never received as ingress"
corrected   the shuffled material was never an observed occurrence with
            preserved provenance through the observer path
```

The distinction matters because the withdrawn wording recovers the wrong
repair. A future reader could take it as *make the experiment material
ingress*, which is exactly the front door this report says the corpus must not
use.

## 2. Active law has the outward path

**[active law]** The stages are named as time coordinates in
`05.Testimony`:

> Requirement time, request-formation time, emission time, delivery time,
> external receipt time, interpretation time, uptake time, reliance time…

That is an act reaching outward and a consequence returning, enumerated.

**[active law]** And the acquisition path is stated directly:

> External material may be acquired and interpreted into Observation testimony,
> but Observation produced is not testimony admitted, not standing revised, and
> not movement opened.

**[active law]** With the definition, and its denial:

> External provider material is not an Observation; an Observation is
> Seed-native testimony formed after acquisition and interpretation, not
> environment truth, not recording, not current standing, and not learning.

**[active law]** And what an Observation must carry, which is exactly what a
control needs:

> Later admission, comparison, establishment, current projection, and
> inquiry-continuation movements must consume the Observation only within
> preserved **source, method, scope, temporal, conflict, authority**, and
> uncertainty…

`method` is the coordinate that would distinguish the same source observed
under two arrangements. Nothing new is required for that.

**[active law]** `Observation` occurs 56 times across five chapters. `egress`
occurs once, and `observer` five times; the outward half is named through the
timing and acquisition clauses rather than through the word.

## 3. The runtime has an observer path

**[runtime witness]** `ObservationSource` is a protocol with `collect() ->
list[Observation]`, and two implementations read the repository:
`RepositorySourceObservationSource` and `SeedRuntimeObservationSource`. Event
kinds `observation.observed`, `evidence.observed`, and `fact.observed` exist.

**[runtime witness]** `Observation.value` is typed `Any`. **The type does not
require text.** The collapse is in the reading, not the carrier.

## 4. Where observation collapses into decoded text

`observation_sources.py`, in `_read_bounded_first_line`:

```python
with path.open("rb") as handle:
    raw = handle.read(max_bytes)
text = raw.decode("utf-8", errors="replace").splitlines()[0].strip()
```

Three losses in one line, none recorded:

```text
errors="replace"   undecodable bytes become U+FFFD -- characters that
                   were not there are put where bytes were
.splitlines()[0]   everything after the first line is discarded
.strip()           leading and trailing whitespace is discarded
```

**Measured, same bytes through both paths:**

```text
bytes: ff fe 20 61 75 64 69 6f ... \n second line \n trailing␣␣

observer path        returns '�� audio-like bytes'
                     U+FFFD fabricated        yes
                     later lines kept         no
                     loss recorded            no

ingress path         outcome                  bytes_rejected
                     text                     None
                     failure recorded         yes
                     exact bytes preserved    fffe20617564696f2d6c696b...
```

**[inference]** The ingress path refuses to invent text and says so. The
observer path invents text and says nothing. So the boundary the corpus should
arrive through currently preserves observed occurrences *less* faithfully than
the one it should not use.

**[inference]** `max_bytes=4096` is a further bound, and a file larger than it
returns nothing at all rather than a bounded observation of its first 4096
bytes.

## 5. What this does not establish

**That the observer path should be changed.** This locates where it collapses.
Whether `_read_bounded_first_line` is doing something else correctly for its
own consumers is not examined, and it may be right for them.

**That the corpus should be observed rather than ingressed.** That is the
operator's correction, recorded here as the topology this audit assumes. The
audit tests the path against it; it does not establish it.

**That an egress act exists.** Nothing found performs one. The timing clauses
name emission and delivery; no runtime act was traced that reaches outward and
records having done so, and `egress` appears once in active law and four times
in one unrelated runtime module.

**That `Observation` is uncontaminated.** `05.Testimony:18` says the repository
compresses Observation intake, Evidence construction, normalization, Fact
construction, and emission into `ObservationIngestor`, and the probe register
records that module as compressed.

**That method would suffice for the control.** §2 shows active law requires an
Observation to preserve `method`. Whether two arrangements of one source are
distinguishable *by* that coordinate is unrecovered.

**That anything was measured about the corpus here.** Nothing was observed,
acquired, or ingested. The two paths were compared on five bytes.
