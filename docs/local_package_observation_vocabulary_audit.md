# Local Package Observation Vocabulary Audit

## Purpose

This audit scopes a narrow local-host package observation path for Seed.

The motivating operator question is:

```text
Which packages are installed on this host?
```

The goal is read-only package inventory evidence.

The goal is not dependency solving, vulnerability scanning, service inference, package management, or host mutation.

## Current Context

Seed has started adding local-host observation families.

Recent work added narrow users/groups observation and exposed the importance of dimensioned fact rendering.

A prior dependency audit concluded that broad external package inventory tooling should not become a core dependency before Seed defines its own package evidence model.

This audit defines that first package evidence model narrowly.

## Central Finding

```text
Installed package evidence
        ≠
service status
        ≠
running process
        ≠
capability availability
        ≠
security posture
```

A package observation can prove that a package manager reports a package record.

It cannot by itself prove that software is running, reachable, healthy, safe, configured, or usable.

## Initial Evidence Source

For the first implementation, use a single common Linux package database source.

Recommended first source:

```text
dpkg status database
```

Likely path:

```text
/var/lib/dpkg/status
```

This keeps the implementation deterministic, read-only, and fixture-testable.

Do not shell out to package manager commands in v1.

Do not depend on apt, dpkg CLI availability, network access, repositories, or lock files.

The implementation should parse fixture text in tests rather than depending on the test runner's installed packages.

## Supported Evidence From dpkg Status

A dpkg package record can support facts such as:

```text
package_installed
package_version
package_architecture
package_manager
package_status
```

Potential optional fields, if present and useful:

```text
package_source_name
package_description_summary
package_section
package_priority
```

For v1, keep the required set small.

The first pass should prefer:

```text
package_installed
package_version
package_architecture
package_manager
```

`package_status` may be useful if it is needed to distinguish installed from non-installed records, but the observation should only emit installed-package facts for records that are clearly installed.

## What "Installed" Means In v1

For dpkg status records, treat a package as installed only when the status field indicates:

```text
Status: install ok installed
```

Do not emit `package_installed` for records that are:

```text
not-installed
config-files only
half-installed
unpacked but not configured
unknown malformed states
```

If future work needs non-installed dpkg states, add a separate audit.

## Recommended Fact Shape

Use host-subject facts with dimensions.

Do not introduce Package entities in v1.

Example:

```text
subject: node115
predicate: package_installed
value: curl
dimensions:
    package_name: curl
    package_manager: dpkg
```

Version example:

```text
subject: node115
predicate: package_version
value: 8.5.0-2ubuntu10.6
dimensions:
    package_name: curl
    package_manager: dpkg
```

Architecture example:

```text
subject: node115
predicate: package_architecture
value: amd64
dimensions:
    package_name: curl
    package_manager: dpkg
```

This mirrors the users/groups choice:

```text
host-subject facts first
entity modeling later only if justified
```

## Candidate Predicates

Initial predicates:

```text
package_installed
package_version
package_architecture
package_manager
```

Optional only if needed:

```text
package_status
package_section
package_priority
package_description_summary
```

Do not include dependency predicates in v1.

Do not include vulnerability predicates in v1.

Do not include service predicates in v1.

## Dimensions

Use dimensions to preserve package identity and source context.

Recommended dimensions:

```text
package_name
package_manager
```

Optional dimensions:

```text
architecture
```

if needed to distinguish multi-arch package records.

Dimension keys should be deterministic and lowercase snake_case.

## Boundary With Services

Do not infer services from packages.

Examples:

```text
package_installed=nginx
        ≠
nginx service exists
        ≠
nginx service is enabled
        ≠
nginx is running
        ≠
port 80 is listening
```

Service observation should be handled separately through systemd or process/socket evidence.

## Boundary With Capabilities

Do not infer capability availability from packages.

Examples:

```text
package_installed=ansible
        ≠
ansible capability is verified

package_installed=openssh-server
        ≠
SSH is reachable

package_installed=docker
        ≠
Docker daemon is running
```

Capability verification remains separate.

## Boundary With Security

Do not infer vulnerability, patch status, or safety from package records.

A version can later be used as evidence for security analysis, but package observation alone should not assert:

```text
vulnerable
patched
safe
unsupported
end_of_life
```

Those require separate security knowledge sources and audits.

## Boundary With External Inventory Tools

This audit does not reject broad inventory tools permanently.

It preserves the prior dependency boundary:

```text
external package inventory tool
        = candidate optional observation adapter
```

not:

```text
core Seed dependency
```

Once Seed's package vocabulary is stable, external adapters can map their output into the same package facts.

## Surface Placement

### Current Facts

Current Facts should expose package facts first.

This is the safest surface for initial package evidence.

### Fact Support

Fact Support should expose provenance and dimensions for package facts.

### Impact

Impact may later summarize packages for a host, but not in v1 unless output pain proves it is needed.

### State Summary

State Summary should not list packages.

A future compact domain count may be considered after package observations exist across multiple hosts, but v1 should not expand State Summary.

## Recommended First Implementation

Implement local package observation v1 as:

```text
1. Add a small dpkg status parser with fixture tests.
2. Wire parser into the existing LocalHostObservationSource read-only collection path.
3. Emit host-subject package facts with dimensions.
4. Register required predicates in the canonical predicate catalog.
5. Add characterization tests proving installed records emit facts and non-installed/malformed records are skipped.
6. Verify no subprocess, network, package-manager command, lock, repository, service, capability, or vulnerability inference occurs.
```

## Fixture Guidance

Tests should use small dpkg status fixture records.

Installed example:

```text
Package: curl
Status: install ok installed
Architecture: amd64
Version: 8.5.0-2ubuntu10.6
Description: command line tool for transferring data with URL syntax
```

Skipped example:

```text
Package: oldpkg
Status: deinstall ok config-files
Architecture: amd64
Version: 1.0
```

Malformed records should be skipped or ignored safely.

## Non-Goals

This audit does not implement package observation.

It does not require parsing every package manager.

It does not add external inventory tool dependencies.

It does not shell out to package manager commands.

It does not inspect repositories.

It does not inspect apt sources.

It does not infer services.

It does not infer running processes.

It does not infer open ports.

It does not infer capabilities.

It does not infer vulnerabilities or patch status.

It does not introduce Package entities.

It does not add State Summary sections.

## Current Conclusion

Package observation is a good next local-host acquisition family if kept narrow.

The first implementation should answer:

```text
Which installed packages does the local dpkg status database declare?
```

It should not answer:

```text
What services are running?
What capabilities are available?
What ports are open?
Is the host secure?
```

The safest next step is a fixture-tested, read-only dpkg status observation source that emits narrow host-subject package facts and leaves service, capability, vulnerability, and package-entity interpretation for later audits.