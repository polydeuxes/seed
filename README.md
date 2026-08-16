# Seed

Seed is an append-only runtime for preserving bounded material, Assertions,
Evidence, occurrences, and Standing without strengthening what the recorded
coordinates establish.

## Orientation

- [Book of Seed](book_of_seed/README.md) — active constitutional grammar,
  organized as chapters along the Responsibility spine.
- [Rosetta of Seed](rosetta/README.md) — ordinary-language translations of the
  same spine and explanations of retired vocabulary. Rosetta carries no
  constitutional Authority.
- [`seed_runtime/`](seed_runtime/) — current implementation witnesses.
- [`tests/`](tests/) — executable behavioral and grammar checks.

The Book states grammar. Runtime behavior and tests provide implementation
Evidence. Neither silently substitutes for the other.

## Repository layout

- `book_of_seed/chapters/` — active Book chapters.
- `book_of_seed/grammar.json` — machine-readable grammar coordinates checked by
  tests.
- `rosetta/` — translation and vocabulary retirement records.
- `seed_runtime/` — live Python runtime.
- `tests/` — executable checks.
- `archive/reports/` — historical reports retained as records, not current
  architectural Authority.
- `dormant/` — retired implementation and data retained for inspection.
- `scripts/` — repository maintenance commands.

## Run checks

Seed requires Python 3.11 or newer and Pydantic 2.

```bash
python -m pytest -q
```

After installation, the command entrypoint is:

```bash
seed --help
```
