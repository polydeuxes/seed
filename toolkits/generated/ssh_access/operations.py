"""Safe SSH access planning operations.

These operations intentionally avoid shell execution and network SSH access. They
return deterministic read-only or plan-only results so Seed can reason about the
`ssh_access` capability without mutating hosts.
"""

from __future__ import annotations

from seed_runtime.execution import ToolContext


def verify_ssh_access(ctx: ToolContext, host: str) -> dict[str, object]:
    """Return a non-network SSH verification stub for a host.

    The tool does not open sockets, run commands, or inspect the host. It records
    that no live check was attempted yet, which is safe evidence for planning.
    """

    return {
        "ok": True,
        "host": host,
        "access_status": "not_checked",
        "method": "stub_no_network",
        "summary": f"SSH access for {host} was not checked because network SSH is not enabled in this prototype.",
    }


def plan_ssh_install(ctx: ToolContext, host: str) -> dict[str, object]:
    """Return non-mutating implementation steps for a future SSH install flow."""

    steps = [
        "Confirm the host identity and operating system through an approved inventory or verification source.",
        "Check whether an SSH server package is already installed using a future read-only verification tool.",
        "Prepare platform-specific installation commands for human review without executing them.",
        "Require explicit L3 approval before any future package installation or service changes.",
        "After approval in a hardened implementation, install the SSH server and verify service status.",
    ]
    return {
        "ok": True,
        "host": host,
        "plan_only": True,
        "mutation_allowed": False,
        "steps": steps,
        "summary": f"Prepared a non-mutating SSH installation plan for {host}.",
    }
