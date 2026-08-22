# Local Network Impact Boundary Audit

## Purpose

This audit follows the local CLI responsibility boundary audit.

The question is whether local network impact formatting in `scripts/seed_local.py` contains responsibility leaks similar to the mount-impact issue.

## Trigger

The mount impact work showed that implementation agents naturally place nearby classification policy into the CLI unless ownership boundaries are explicit.

After merging the corrected mount change, the next likely risk area is:

```text
local network configuration
```

inside `--impact` output.

## Central Question

```text
Does scripts/seed_local.py merely render network impact output,
or does it own local-host network classification policy?
```

## Current Observed Shape

`format_entity_impact(...)` collects local network fact families including:

```text
network_interface
interface_role
interface_operstate
interface_mac_address
interface_mtu
ip_address
address_assignment_method
default_gateway
dns_resolver
dns_resolver_stub
dns_resolver_upstream
```

It then delegates to `_format_local_network_impact(...)`.

The local network impact path currently performs several responsibilities:

```text
Groups facts by predicate
Collects interfaces from values and dimensions
Infers display role from default gateway facts and interface role facts
Falls back to interface-name heuristics
Collapses container/virtual/vpn interfaces
Orders visible interfaces by role priority
Groups IP addresses into ipv4, ipv6_global, and ipv6_link_local
Formats DNS resolver lines
Adds non-inference guardrail lines
```

## Findings

## 1. Some Network Logic Is Pure Rendering

The following responsibilities are acceptable CLI formatting:

```text
Printing primary/default-route interface labels
Indenting IPv4/IPv6 address lists
Printing DNS resolver lines
Printing the non-inference guardrail line
```

These are presentation concerns.

## 2. Some Network Logic Is Classification Policy

The following responsibilities are not merely rendering:

```text
Choosing interface display role priority
Classifying names beginning with tailscale or wg as vpn
Classifying docker, br-, and veth interfaces as container
Classifying virbr as virtual
Collapsing container/virtual/vpn interfaces
Classifying IPv6 link-local versus global address groups
```

These define local-host network interpretation policy.

They are analogous to the mount filesystem taxonomy and collapse policy that was moved out of the CLI.

## 3. The Current State Is Not An Emergency

Unlike the mount issue, the network output is already relatively readable.

The concern is not immediate operator pain.

The concern is architectural drift:

```text
The CLI owns policy because it was the closest place to put it.
```

This is the same failure mode documented in implementation prompt alignment.

## Boundary Recommendation

A better boundary would be:

```text
seed_runtime/local_host_networks.py
    owns local-host network classification and grouping policy

scripts/seed_local.py
    owns terminal rendering of the classified/grouped network impact output
```

Candidate runtime-owned helpers:

```text
classify_interface_role(...)
interface_display_priority(...)
should_collapse_interface(...)
classify_interface_address_group(...)
group_interface_addresses(...)
```

The CLI may still own:

```text
Text labels
Indentation
Line ordering for terminal output
Guardrail wording
```

## Tests To Require If Refactored

Runtime-level tests should prove:

```text
default-route interfaces classify as primary
lo classifies as loopback
wg/tailscale interfaces classify as vpn
docker/br-/veth interfaces classify as container
virbr interfaces classify as virtual
container/virtual/vpn interfaces are collapsible
IPv4 addresses group as ipv4
IPv6 link-local addresses group as ipv6_link_local
Other IPv6 addresses group as ipv6_global
Display priority is deterministic
```

CLI-level tests should remain focused on:

```text
Rendered --impact network output
Collapsed interface count line
DNS output formatting
Non-inference guardrail line
```

## Non-Goals

Do not change local network observation acquisition.

Do not change stored facts.

Do not change `--current-facts`.

Do not infer reachability, availability, health, ownership, or service identity from local network facts.

Do not remove the existing collapsed-interface behavior unless a separate operator-output audit justifies it.

## Implementation Timing

This does not need to be fixed immediately unless network impact code is being touched.

However, the next network-impact change should include the boundary move.

The rule should be:

```text
Do not add more local-host network classification policy to scripts/seed_local.py.
```

If new policy is needed, create the runtime helper first.

## Current Conclusion

The local network impact path contains a mild version of the same boundary issue discovered in mount impact rendering.

The CLI currently owns network classification and collapse policy that would better live in a runtime-owned local-host network helper module.

This is not urgent because the operator output is acceptable.

It is important because it identifies the next place the CLI could become a second domain system.
