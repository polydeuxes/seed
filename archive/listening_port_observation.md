# Listening Port Observation v1

Listening Port Observation v1 is Tier 3 host topology knowledge. It enriches Seed's local knowledge model through the existing Observation → Evidence → Fact → Projection path only.

This slice answers: what TCP and UDP endpoints are bound locally according to local kernel socket-table evidence?

It is not service management, process management, endpoint monitoring, health monitoring, reachability testing, availability verification, orchestration, provider integration, network probing, shell execution, subprocess execution, sudo use, or LLM-generated host fact creation.

## Evidence sources

Listening Port Observation v1 uses bounded read-only local procfs evidence:

- `/proc/net/tcp`
- `/proc/net/tcp6`
- `/proc/net/udp`
- `/proc/net/udp6`

TCP rows are projected only when the local kernel state is `0A` (`LISTEN`). UDP rows are treated as locally bound UDP endpoints when they expose a non-zero local port. Seed does not open sockets, attempt connections, call DNS, invoke `ss`, `netstat`, `lsof`, `fuser`, shell commands, subprocesses, sudo, provider APIs, network probes, or Prometheus.

`/proc/net/unix` remains out of v1 so the representation stays narrow around TCP/UDP bound endpoints.

## Representation chosen

Listener facts are host-scoped. A bound endpoint is represented with dimensions:

- `protocol`: `tcp` or `udp`
- `address`: parsed local IPv4 or IPv6 address
- `port`: parsed local port as a string dimension; `listening_port` stores the parsed integer port fact
- `address_family`: `ipv4` or `ipv6`

The compact endpoint value is:

- IPv4: `tcp 0.0.0.0:22`
- IPv6: `tcp [::1]:8080`
- UDP: `udp 0.0.0.0:53`

This representation is intentionally about machine shape: protocol/address/port topology visible from local kernel state. It does not model process ownership, service ownership, application identity, reachability, availability, or health.

## Facts

| Predicate | Question | Evidence | Fact | Non-inferences |
| --- | --- | --- | --- | --- |
| `listening_endpoint` | What protocol/address/port endpoints are bound locally? | `/proc/net/tcp`, `/proc/net/tcp6`, `/proc/net/udp`, `/proc/net/udp6` | A compact endpoint string such as `tcp 0.0.0.0:22`. | `listening_endpoint` != reachable, externally accessible, healthy, responding, monitored, managed, owned by a service, owned by a process, or owned by an application. |
| `listening_protocol` | What local listener protocol is exposed by kernel state? | Same procfs socket tables. | `tcp` or `udp` for an observed local listener. | `listening_protocol` != protocol success, active traffic, service availability, or application ownership. |
| `listening_address` | What local addresses are bound by listeners? | Same procfs socket tables. | The local bound address parsed from kernel state. | `listening_address` != connectivity, routability, external accessibility, DNS validity, or reachability. |
| `listening_port` | What TCP/UDP ports are bound locally? | Same procfs socket tables. | The local bound port parsed as an integer. | `listening_port` != reachable, healthy, responding, managed, externally accessible, or owned by a process/service/application. |

## Bounded-read behavior

Listening port observation uses the existing bounded local read helper:

- procfs socket tables are read with a maximum byte bound;
- regular files larger than the configured bound are skipped;
- pseudo-files or streams that fill the full bound are treated as possibly truncated and skipped;
- malformed/truncated socket-table rows cause that source table to be skipped;
- oversized or possibly truncated inputs are not partially projected.

## Impact and current facts

`--current-facts` exposes every emitted listener fact, including `listening_endpoint`, `listening_protocol`, `listening_address`, and `listening_port`.

`--impact HOST` includes a compact `listening endpoints` section, for example:

```text
listening endpoints:
- tcp 0.0.0.0:22
- tcp 127.0.0.1:9090
- udp 0.0.0.0:53
- availability/reachability/health/ownership: not inferred from listener facts
```

The impact section is a concise summary only. It does not overload aliases, availability, identity, local network configuration, mounts, or storage topology.

## Non-inference boundaries

Listening port facts must not imply:

- availability;
- reachability;
- external accessibility;
- endpoint health;
- application health;
- service health;
- process ownership;
- service ownership;
- application ownership;
- responsiveness;
- active traffic;
- monitoring status;
- management authority.

Examples:

- `listening_port` != reachable;
- `listening_port` != externally accessible;
- `listening_endpoint` != healthy;
- TCP listener != responding;
- UDP listener != active traffic;
- bound address != connectivity;
- observed listener != managed service;
- observed listener != process ownership.
