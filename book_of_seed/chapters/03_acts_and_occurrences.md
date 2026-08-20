# Acts and Occurrences

### 02.Acts.A — Exact Act and occurrence

One exact Responsibility bounds one exact Act. The Responsibility carries its
responsible boundary, subject, Authority, Scope, Locality, limits, and required
relations.

An Act occurrence is the occurrence of that Act under the Responsibility. An
Act, invocation, proposed Act, material availability, or result
establishes no Act occurrence.

Participation carries one subject, one Act-local role, and one Act occurrence:

```
subject --Participation(role)--> Act occurrence
```

Carriage carries content and one Act occurrence:

```
content --Carriage--> Act occurrence
```

Yield is the exact relation from one Act occurrence to its exact result:

```
Act occurrence --Yield--> result
```

The Yield relation requires its first subject, second subject, relation occurrence, Authority,
Scope, Locality, limits, and Unknown. Multiplicity of an occurrence and result
establishes no Yield.

A result preserves coordinates established by its Act occurrence. It
establishes no later Standing.

## References

- [Standing](01_constitutional_standing.md)
- [Authority and Scope](02_authority_scope.md)
