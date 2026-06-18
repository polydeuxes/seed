# Local Users Observation Vocabulary Audit

## Purpose

This audit scopes a narrow local-host users observation path for Seed.

The motivating operator question is:

```text
What local users and groups exist on this host?
```

The goal is not user management.

The goal is read-only evidence acquisition.

## Current Context

Seed is beginning to add more local-host observation families.

Recent work clarified boundaries for:

```text
State Summary
Impact
Current Facts
Fact Support
local host availability
package inventory dependency posture
```

Users are a reasonable next observation family because they are useful to operators, relatively low-risk to read, and simpler than firewall or policy-routing evidence.

Firewall and IP rules likely require a broader audit because they span multiple implementations and interpretation traps.

Users can start narrower.

## Central Finding

```text
Local user records are identity/configuration evidence.

They are not login activity, reachability, privilege, or account safety evidence by themselves.
```

A local passwd/group observation can support facts about declared accounts and groups.

It must not automatically support conclusions about who is active, who is authorized remotely, who is privileged in practice, or whether the host is secure.

## Initial Evidence Sources

A first users observation should read only stable local configuration files or standard library equivalents.

Recommended initial sources:

```text
/etc/passwd
/etc/group
```

Possible Python equivalents:

```text
pwd module
grp module
```

The implementation should remain read-only.

It should not inspect shadow hashes, mutate users, run commands, or require elevated privileges.

## Supported Evidence From `/etc/passwd`

A passwd entry can support:

```text
user_account exists
user_uid
user_primary_gid
user_gecos / comment if retained
user_home_directory
user_shell
```

Potential dimensions:

```text
username
uid
gid
source_file=/etc/passwd
```

The subject should remain the observed host unless a later entity model for user accounts is explicitly introduced.

A conservative first shape is host-subject facts with dimensions identifying the user.

Example:

```text
subject: example_host
predicate: user_account
value: john
dimensions:
    username: john
    uid: 1000
```

This avoids prematurely turning each user into a graph entity before the relationship model is designed.

## Supported Evidence From `/etc/group`

A group entry can support:

```text
group_account exists
group_gid
group_member
```

Potential dimensions:

```text
groupname
gid
username
source_file=/etc/group
```

A group membership fact should represent declared supplementary group membership from `/etc/group`.

It should not imply active session group state.

## Candidate Predicates

Initial predicates may include:

```text
user_account
group_account
user_uid
user_primary_gid
user_home_directory
user_shell
group_gid
group_member
```

A later pass may add:

```text
user_account_kind
user_login_allowed
user_sudoer_candidate
sudoers_rule
active_login_session
```

but those should not be included in the first observation unless separately audited.

## System Account Classification

It is tempting to classify users as:

```text
system
human
service
```

That classification is useful but should be treated carefully.

Possible evidence includes UID ranges, shell, home directory, and distribution policy.

However, these are heuristics.

A first implementation may either:

```text
avoid classification entirely
```

or emit only a clearly named heuristic predicate such as:

```text
user_account_kind_guess
```

If added, the name should make the uncertainty visible.

Do not silently convert UID ranges into authoritative human/system classification.

## Privilege Boundaries

Group membership can be relevant to privilege, but it is not privilege itself.

Examples:

```text
member of sudo group
member of wheel group
member of docker group
```

These may indicate privilege-relevant configuration.

They do not prove:

```text
sudo access is allowed
sudoers policy permits elevation
user has active credentials
user can log in remotely
account is safe
```

A future privilege audit should separately inspect:

```text
/etc/sudoers
/etc/sudoers.d
polkit rules
ssh authorized keys
PAM configuration
```

Those are out of scope for the first users observation.

## Login / Activity Boundaries

Local passwd/group facts must not imply:

```text
active login session
recent login
SSH access
interactive shell usability
account enabled state
password status
credential validity
```

Those require different evidence sources.

Examples:

```text
utmp/wtmp/loginctl for sessions
sshd configuration for SSH policy
shadow/passwd lock state for password status
PAM configuration for authentication behavior
authorized_keys for SSH key presence
```

These are intentionally excluded from the first pass.

## Surface Placement

### Current Facts

Current Facts should expose the raw user and group evidence.

This is the first and safest surface for new user facts.

### Fact Support

Fact Support should show provenance for user/group facts.

For local users this likely means observation source, source file or module, and observation event.

### Impact

Impact may later summarize user evidence for a host.

Potential examples:

```text
users: 42 observed
human-like users: not classified
privilege-relevant groups: sudo, docker observed
```

Do not add this until the raw facts are stable.

### State Summary

State Summary should not list users.

At most, after facts stabilize, it may include a compact domain presence/count such as:

```text
user facts: observed
```

or leave users entirely to Impact and Current Facts.

State Summary remains repository overview, not host account inventory.

## Recommended First Implementation

Implement a narrow local-host user observation path:

```text
1. Extend LocalHostObservationSource or add a helper it calls.
2. Read local passwd/group data read-only.
3. Emit host-subject user/group facts with dimensions.
4. Register predicates in the canonical predicate catalog.
5. Add tests using fixture data rather than the live test runner's host users.
6. Surface facts first through Current Facts and Fact Support.
```

The implementation should not depend on the test environment's actual `/etc/passwd` content.

Use fixture parsers where possible.

## Fixture Guidance

Tests should include small fixture records such as:

```text
root:x:0:0:root:/root:/bin/bash
john:x:1000:1000:John:/home/john:/bin/bash
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

and groups such as:

```text
sudo:x:27:john
docker:x:999:john
john:x:1000:
```

Tests should verify:

```text
users are observed deterministically
groups are observed deterministically
group membership is represented without privilege inference
no active login facts are emitted
no sudo authorization facts are emitted
no availability facts are emitted
```

## Non-Goals

This audit does not implement user observation.

It does not require parsing `/etc/shadow`.

It does not inspect sudoers.

It does not inspect SSH authorized keys.

It does not infer active logins.

It does not infer account safety.

It does not infer host availability.

It does not mutate users or groups.

It does not require elevated privileges.

It does not require adding user summaries to State Summary.

## Future Work

Likely follow-up audits:

```text
local privilege vocabulary audit
ssh access observation audit
active session observation audit
firewall and policy routing observation audit
```

These should remain separate because they answer different questions.

## Current Conclusion

Users are a good next observation family if kept narrow.

The first implementation should answer:

```text
Which local users and groups are declared on this host?
```

It should not answer:

```text
Who is active?
Who can SSH?
Who can sudo?
Is this account safe?
```

The safest next step is a fixture-tested, read-only local users observation source that emits narrow user/group configuration facts and leaves privilege, activity, and access interpretation for later audits.