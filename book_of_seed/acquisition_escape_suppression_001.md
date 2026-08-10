# A driven console that does not install the operator's escape

Runtime amended narrowly. No Book amendment. **`exit` is unchanged.**

## The circle this breaks

```text
  Seed needs Bash evidence
      -> the Bash guide contains a line whose entire content is `exit`
      -> the console's process-boundary escape consumes it as control
      -> Seed cannot acquire enough Bash
      -> Seed cannot use Bash through an egress it does not have yet
```

**[measured]** `#2435` measured the cost: 2,957 of 54,264 lines, 5.4%, with no
error reported.

## What was added

One default argument on `run_persistent_operator_console`:

```python
process_boundary_escape: bool = True
```

At `False`, the escape is not examined and **EOF terminates**.

```text
  source lines            54,264
  ingress occurrences     54,264
  bare 'exit' preserved   37 of 37
  now presented           100.0%   (was 5.4%)
```

## What it is not

**Not a second ingress mode.** There is one door, the operator's, and the
acquisition campaign is borrowing it. Seed is never told that `exit` is
sometimes control and sometimes material; nothing in the ingress path
distinguishes them, and manufacturing that distinction because a downstream
campaign wants one is the shape this project refuses elsewhere.

**Not a rename.** Making the token `quit` moves the collision to the next corpus
that contains `quit`, and changes the operator interface for no constitutional
reason.

**Not an escape convention.** `\exit` would require something to establish that
`\exit` represents literal `exit`, and the material Seed receives would stop
being the material supplied.

**Not a rewritten source.** Capitalising the guide's `exit` to `Exit` would plant
a false representation and hope a later Seed repairs it. A test pins that
`exit`, `Exit`, `EXIT` and ` exit` are each preserved exactly as supplied.

**[inference]** What is suppressed is a convenience of the surrounding developer
console. A non-interactive driver declines to install it, and termination comes
from EOF — outside the material stream, where no corpus line can collide with
it. That is why EOF rather than a different token: every byte before it is
material, by construction rather than by choice of word.

## What is unchanged

**[measured]** The default is the interactive behaviour, and three tests pin it:
the operator console still exits on the token, the default parameter is the
escape, and the CLI exposes no flag for suppression. The accommodation is
reachable by a driver, not by a person at a prompt.

## What this does not establish

**That the accommodation should persist.** It is bootstrap scaffolding with a
known removal condition: when Seed's own egress makes acquisition stop passing
through operator escape syntax, this argument has no caller and should go.

**That `exit` reserving the boundary was ever wrong.** `#2435` recorded that it
is not. A line whose entire content is `exit` should stop an interactive
console.

**That the driven path is now faithful in general.** One collision was measured
and removed. Whether the front door reserves anything else was not surveyed.

**That the Bash guide's earlier appearances are repaired.** Every measurement of
`bash_guide` from `#2408` onward read 5.4% of that source, and those reports
stand as measurements of what was presented.
