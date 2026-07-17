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


## Naming and enumeration boundary

The fixture competency `competency:evidence-boundary-local-observation` names
only the represented responsibility subject `evidence_boundary` and authority
zone `local_observation`. It intentionally does not name the Eye, does not bind
the competency to an inquiry, and does not assert organism-level observation.

The `competency_change_examination` view uses a complete SQL enumeration of
bounded competency rows against recorded change rows so verification can inspect
every deterministic pair. That enumeration is not a broadcast, notification,
subscription, polling cycle, or claim that every competency received, observed,
or awakened to every recorded change.
