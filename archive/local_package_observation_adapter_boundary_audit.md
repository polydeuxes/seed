# Local Package Observation Adapter Boundary Audit

## Purpose

This audit preserves the implementation boundary for Local Package Observation v1.

The package vocabulary audit intentionally selected dpkg status as the first package source.

That creates a risk:

```text
dpkg first
        ↓
dpkg becomes the package observation architecture
```

This audit prevents that overfit.

## Central Finding

```text
dpkg is the first package adapter.

It is not the package observation model.
```

Seed's package observation architecture should distinguish:

```text
normalized package evidence
        ≠
dpkg status parsing
```

## Required Boundary

The implementation should preserve three roles.

### Package Observation Vocabulary

Owns normalized package facts such as:

```text
package_installed
package_version
package_architecture
package_manager
```

These predicates should not be dpkg-shaped.

They should remain usable by future adapters.

### dpkg Adapter

Owns only dpkg-specific parsing and filtering.

Examples:

```text
/var/lib/dpkg/status record parsing
Status: install ok installed filtering
Package field extraction
Version field extraction
Architecture field extraction
```

### Local Host Observation Source

Owns orchestration of read-only local collection.

It may call a package observation helper.

It should not become the place where all package-manager parsers accumulate.

## Suggested Module Shape

Prefer a dedicated helper module.

Possible name:

```text
seed_runtime/local_packages.py
```

Possible contents:

```text
PackageRecord
parse_dpkg_status(text) -> list[PackageRecord]
package_records_to_observations(host, records, observed_at, source_type) -> list[Observation]
```

This keeps dpkg parsing testable without invoking the full local-host observer.

The exact names are not authoritative.

The boundary is authoritative.

## What To Avoid

Avoid hardcoding dpkg logic directly into a large local-host collector.

Avoid naming generic package functions as if dpkg is the only package source.

Avoid package predicates such as:

```text
dpkg_status
dpkg_installed
dpkg_version
```

unless a dpkg-specific diagnostic fact is separately justified.

Avoid dimensions that only make sense for dpkg.

Avoid assuming all package managers have:

```text
Status
Architecture
Version
Package
```

Those are dpkg record fields, not universal package concepts.

## Normalization Boundary

A dpkg record should be normalized into a generic package record before becoming observations.

Example normalized record shape:

```text
name: curl
version: 8.5.0-2ubuntu10.6
architecture: amd64
manager: dpkg
installed: true
```

Then observations are emitted from the normalized record.

This prevents observation emission code from depending on dpkg text-field shape.

## Future Adapter Compatibility

Future adapters may include:

```text
rpm / dnf
apk
pacman
snap
flatpak
pip / pipx
npm / pnpm / yarn
cargo
gem
homebrew
nix
```

They should be able to emit the same generic predicates where possible.

Adapter-specific fields should either be omitted, placed in metadata, or introduced through a separate audit.

## Predicate Guidance

Use generic predicates:

```text
package_installed
package_version
package_architecture
package_manager
```

Keep dimensions generic:

```text
package_name
package_manager
```

Optional future dimension:

```text
package_scope
```

Examples of possible scopes:

```text
system
user
language_runtime
container
```

Do not add scope in v1 unless the implementation has explicit evidence for it.

## Test Guidance

Tests should verify both layers separately.

### Parser Tests

Parser tests should prove:

```text
dpkg installed records are parsed
non-installed dpkg records are skipped
malformed records are skipped safely
multi-record fixtures are deterministic
```

### Observation Tests

Observation tests should prove:

```text
normalized records emit generic package predicates
package facts are host-subject facts
dimensions include package_name and package_manager
no services are inferred
no capabilities are inferred
no vulnerability facts are emitted
```

### Boundary Tests

Boundary tests should guard against:

```text
subprocess execution
network calls
package manager CLI calls
repository inspection
service inference
State Summary additions
Package entity creation
```

## Relationship To External Inventory Tools

This boundary also prepares for possible future external inventory tooling.

If a broad inventory tool is added later, it should act as another adapter:

```text
ExternalInventoryAdapter
        ↓
PackageRecord
        ↓
package observations
```

not as the owner of package semantics.

## Non-Goals

This audit does not implement package observation.

It does not require an adapter registry.

It does not require a full provider framework.

It does not require package entities.

It does not require multi-package-manager support in v1.

It does not reject dpkg as the first adapter.

It only prevents dpkg from becoming the package observation architecture by accident.

## Current Conclusion

Local Package Observation v1 should use dpkg because it is a useful first source.

But the implementation should make clear that:

```text
Package observation is generic.
Dpkg parsing is adapter-specific.
LocalHostObservationSource orchestrates collection.
```

This preserves future extension without prematurely building a large adapter framework.
