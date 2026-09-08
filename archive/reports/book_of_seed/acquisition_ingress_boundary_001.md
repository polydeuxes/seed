# The front door cannot present all material, and it did not say so

Findings only. No runtime or Book amendment. **`exit` is deliberately unchanged.**

## What happened

**[measured]** The full-corpus acquisition run recorded:

```text
  source        source lines    events    events/line
  cookbook            37,697   188,487          5.00
  french_hugo         14,399    71,997          5.00
  bash_guide          54,264    14,787          0.27      <-
```

**[measured]** `bash_abs_guide.txt` carries a line whose entire content is
`exit`, at line 2,957. `2,957 x 5 + 2 = 14,787` exactly. Ingestion stopped
there, at **5.4%** of the source, and reported no error.

**[measured]** `_is_console_exit` compares the captured bytes to `b"exit"`
exactly, after stripping one trailing newline. Webster's two `EXIT` lines
survived because the comparison is case-sensitive; the bash guide's lowercase
one did not. That source carries 37 such lines.

**[measured]** Of nineteen corpus sources, one collides. The token is rare and
the failure is total.

## What is not the defect

**`exit` reserving the console boundary is not a defect.** A line whose entire
content is `exit` should stop an interactive console, and
`scripts/seed_local.py` already records why it is examined before ingress
recording: it is a process-boundary escape, not constitutional local stopping.

**[inference]** Nor should the console learn to tell operator control from
material. There is no material-ingress path to distinguish it from — there is
one door, the operator's, and the acquisition campaign is borrowing it.
Teaching the console two modes would manufacture an ingress distinction because
a downstream campaign wants one, which is the shape this project refuses
everywhere else. An escape convention such as `\exit` would be worse: something
would then have to establish that `\exit` represents literal `exit`, and the
material Seed receives would no longer be the material supplied.

**The accurate statement is narrower:**

```text
  the console boundary reserves an exact presentation
  therefore the current front door cannot faithfully present all material
```

That is a property of the temporary acquisition path, not a fault in `exit`.

## What is the defect

**[measured]** Acquisition reported a completed source. It did not report
`presented 2,957 of 54,264` or `stopped at a reserved presentation`. It produced
a plausible partial body and moved on, and the truncation was found only by
comparing events-per-line ratios across sources.

**[inference]** Two claims are separable, and only the second is wrong:

```text
  the console reserves "exit"              current reality
  acquisition silently truncated           defective
```

A runner driving the front door should establish, before presenting a source,
whether that source contains the boundary's reserved presentation — and refuse,
or record the acquisition as incomplete with its exact extent. That repair does
not touch `exit`, the console, or the ingress path.

## The provenance defect beside it

**[measured]** `latin_vulgate.txt` is the Douay-Rheims in English. `#2408`'s
non-English finding is withdrawn there. A downloaded file was named from the
identifier requested rather than from what arrived.

**[measured]** The same failure recurred in the same session: Gutenberg 8083,
requested as the American Standard Version, is *The Allis Family; or, Scenes of
Western Life*. It was caught because every new file's title was read.

```text
  successful download  !=  verified source identity
```

**[inference]** Provenance is not hygiene here. A mislabelled source produced a
published conclusion about English that nothing supported, and it survived four
reports.

## What this does not establish

**That the front door should be replaced now.** Seed's own egress and recovery
would remove this constraint rather than work around it, and that path is
unbuilt and deliberately deferred.

**That the truncation invalidates other sources.** Eighteen of nineteen carry no
bare `exit`. `bash_guide` alone is affected, and its every appearance in
`#2408` onward is a measurement of 5.4% of that source.

**That refusing is the right repair rather than reporting incomplete.** Both are
available and neither is recovered; what is established is that claiming
completion was wrong.
