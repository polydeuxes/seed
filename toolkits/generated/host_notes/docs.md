# host_notes

`host_notes` is the first harmless generated-style toolkit. It proves the
generate/register/context loop with tools that only mutate Seed's own event
ledger:

- `add_host_note(host, note)` records a note as `host_note.added`.
- `list_host_notes(host)` returns notes from the workspace ledger.

The toolkit deliberately does not contact, mutate, or authenticate to any host.
