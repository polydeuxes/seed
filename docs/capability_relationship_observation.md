# Capability Relationship Observation

Observation

Recent operational-story investigation exposed a distinction between capability pressure and capability acquisition.

Current capability surfaces can answer:

- what capability is missing;
- what evidence is blocked;
- what operational benefit the capability would provide.

However, this does not answer whether the capability is expected, attainable, appropriate, or intentionally unavailable in the current deployment.

Examples

A deployment may intentionally operate with:

- Prometheus-only visibility;
- read-only inventory visibility;
- no SSH access;
- no root access;
- no Docker socket access.

In such environments:

- listener_process_inventory
- container_inventory
- container_port_mapping

may remain unavailable by design.

This is materially different from:

- not yet acquired;
- temporarily unavailable;
- unknown.

Working question

Can Seed distinguish:

- unknown;
- unavailable;
- intentionally unavailable;
- not yet acquired;
- impossible within the current deployment boundary?

Potential significance

Current operational pressure surfaces may implicitly treat missing capability as acquisition pressure.

The repository may instead require a way to reason about the relationship between:

- deployment shape;
- visibility boundaries;
- capability expectations;
- capability attainability.

Observation

The operator may remain the authority for declaring environmental boundaries.

However, Seed may still benefit from repository-visible reasoning that distinguishes:

```text
I would benefit from capability X.
```

from:

```text
Capability X is expected and attainable.
```

and:

```text
Capability X is intentionally unavailable in this environment.
```

This observation does not propose implementation work. It records a possible gap between capability pressure visibility and capability-environment reasoning.
