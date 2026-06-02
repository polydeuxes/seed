# ssh_access

`ssh_access` is a safe generated-style toolkit for reasoning about SSH access
without changing or contacting hosts.

## Current tools

- `verify_ssh_access(host)` returns a deterministic read-only/stub result. It
  does not run commands, open sockets, or attempt a network SSH connection.
- `plan_ssh_install(host)` returns an ordered, non-mutating plan. It is intended
  to help Seed explain what would be needed before any future install workflow.

## Explicit non-goals for this session

- No real SSH network access.
- No shell execution.
- No package installation.
- No service management.
- No `install_ssh_server` implementation.

A future `install_ssh_server` tool, if added, must be L3 approval-gated or
disabled/model-hidden until sandboxing, policy, and review workflows are strong
enough for host mutation.
