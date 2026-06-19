# CLI Debug Command Consistency

Cache-debug commands are standalone read-only views.

A cache-debug flag owns dispatch for the view it instruments. Operators do not
need to supply the non-debug view flag for top-level cache/timing inspection.
For views that also support filtered legacy query arguments, the debug flag may
still be combined with the base view flag and its arguments to instrument that
filtered invocation.

Current cache-debug entrypoints following this rule:

- `--state-summary-cache-debug` renders state-summary cache eligibility, cache
  status, and timings without `--state-summary`.
- `--current-facts-cache-debug` renders the current-facts view with cache status
  and timings without requiring `--current-facts`.

This rule keeps cache-debug surfaces from mixing standalone-command and
modifier-only invocation models.

Audit notes:

- `--integrity-summary` is a standalone integrity inspection surface, but this
  slice found no separate `--integrity-summary-cache-debug` command.
- No other `*-cache-debug` commands are currently present in the CLI.
