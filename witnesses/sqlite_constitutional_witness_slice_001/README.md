# SQLite Constitutional Witness Slice 001

This district is an isolated side-by-side realization witness. It is not a
production replacement, not a Python compatibility layer, and not a canonical
database requirement.

Run all verification cases from a clean disposable database:

```sh
./witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh
```

The SQL owns the witness semantics: recorded assertion boundaries, bounded
competency declarations, relevance/unknown/evidence/authority outcomes, and the
forbidden inference that relevance is not execution authorization or truth
establishment. The shell harness only recreates the database and asks SQLite to
run deterministic assertions.
