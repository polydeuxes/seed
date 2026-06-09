# Package Inventory Dependency Boundary Audit

## Purpose

This audit reviews whether Seed should depend on an external package-inventory tool or first implement a small native package observation path.

The motivating example was an external tool described as a pain-reduction inventory utility that lists installed packages across many package managers.

The question is:

```text
Should Seed shortcut package observation by depending on a broad external inventory tool,
or should Seed first define and implement its own minimal package observation shape?
```

## Current Dependency Context

Seed currently treats a small set of infrastructure tools as the meaningful orchestration/observation dependencies:

```text
SSH
Prometheus
Ansible
```

These are broad infrastructure surfaces.

They help Seed observe and orchestrate across hosts.

A package inventory collector is different.

It is not an orchestration substrate.

It is an observation adapter candidate.

## Central Finding

```text
Dependency
        ≠
Observation source
```

A useful external tool should not automatically become a core dependency.

It may instead become an optional observation source once Seed knows what package evidence it wants.

## External Inventory Tool Assessment

A broad package inventory tool may eventually be useful because it could normalize collection across many package managers.

Examples include system, language, and user-level package managers such as:

```text
apt
dpkg
rpm
dnf
apk
pacman
pip
pipx
npm
cargo
gem
flatpak
snap
homebrew
nix
```

However, using a broad external collector too early risks importing someone else's assumptions before Seed has defined its own facts, dimensions, and authority boundaries.

The problem is not whether the external tool is useful.

The problem is whether Seed is ready to depend on it.

## Handwritten First Rationale

Seed should first implement the smallest native package observation path.

A minimal first implementation might inspect one or two common local package backends such as:

```text
dpkg / apt
```

and emit narrow facts such as:

```text
package_name
package_version
package_manager
package_architecture
package_scope
package_install_state
```

The exact vocabulary should be audited before implementation.

The point of a handwritten first pass is to let Seed define:

```text
What counts as package evidence?
What entity owns the package fact?
Which dimensions are required?
Which package managers are in scope?
What is excluded?
How should package facts appear in State Summary, Impact, and Current Facts?
```

This keeps Seed's semantic authority inside Seed.

## Boundary With Filesystem Taxonomy Work

Recent filesystem work showed that small handwritten classification can be acceptable when the scope is narrow and the boundary is clear.

Package inventory may follow the same pattern initially.

However, package ecosystems are broader than filesystem types.

That means handwritten coverage should start deliberately small.

The goal is not to handwrite every package manager immediately.

The goal is to establish Seed's package evidence model.

## When An External Tool Becomes Justified

An external inventory adapter becomes more justified if repeated operator pain shows that handwritten collectors are insufficient.

Signals include:

```text
multiple package managers are repeatedly needed
manual collector expansion becomes noisy
package manager detection becomes the dominant problem
Seed's package vocabulary is already stable
raw external output can be mapped cleanly into Seed facts
```

At that point, the external tool should be integrated as:

```text
InventoryObservationSource
```

or similar.

It should remain an optional adapter unless future evidence justifies promoting it.

## Dependency Classification

Recommended classification today:

```text
SSH
    core orchestration / observation transport

Prometheus
    optional provider observation source

Ansible
    optional inventory / orchestration source

External package inventory tool
    candidate optional package observation adapter
```

This preserves the difference between infrastructure dependencies and domain-specific evidence collectors.

## Risks Of Adding The Dependency Too Early

Adding a broad package inventory dependency immediately may cause:

```text
outsourced vocabulary
unclear package fact ownership
unclear package scope
large dependency surface
harder tests
adapter behavior treated as Seed semantics
overcollection before read surfaces know how to summarize it
```

These risks are especially relevant because Seed is close to adding more local-host data.

Observation expansion should not outrun semantic clarity.

## Recommended Next Step

Do not add the external package inventory tool as a core dependency yet.

Instead:

```text
1. Audit package inventory vocabulary.
2. Define minimal package facts and dimensions.
3. Implement a narrow local package observation source for one common backend.
4. Surface package facts through Current Facts first.
5. Add Impact or State Summary summaries only after evidence shape is stable.
6. Reconsider an optional external adapter after repeated operator pain.
```

## Non-Goals

This audit does not reject the external tool permanently.

It does not require hand-coding every package manager.

It does not define final package vocabulary.

It does not add package observation.

It does not change current dependency policy.

It does not require package data in State Summary or Impact yet.

## Current Conclusion

Seed should not promote a broad package inventory helper into a core dependency before defining its own package evidence model.

The safer path is:

```text
minimal native package observation
        ↓
stable package vocabulary
        ↓
operator feedback
        ↓
optional external adapter if justified
```

This keeps package inventory aligned with Seed's broader pattern:

```text
observe narrowly
preserve boundaries
define semantics before expanding coverage
```
