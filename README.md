# Seed

Seed is an append-only runtime whose Ledger records exact bounded material and
occurrences. Its readers address exact coordinates current through a selected
occurrence boundary without adding distinctions to those coordinates.

## Orientation

- [Book of Seed](book_of_seed/README.md) — active constitutional grammar,
  with its exact chapter coordinates.
- [Rosetta of Seed](rosetta/README.md) — ordinary-language translations of the
  Book coordinates and explanations of retired vocabulary. Rosetta carries no
  constitutional coordinates.
- [`seed_runtime/`](seed_runtime/) — current implementation witnesses.
- [`tests/`](tests/) — executable behavioral and grammar checks.

The Book states grammar. Runtime behavior and tests provide implementation
testimony. Neither silently substitutes for the other.

## Repository layout

- `book_of_seed/chapters/` — active Book chapters.
- `book_of_seed/witness_grammar.json` — Witness Grammar coordinates checked by
  tests.
- `rosetta/` — translation and vocabulary retirement records.
- `seed_runtime/` — live Python runtime.
- `tests/` — executable checks.
- `archive/reports/` — historical reports; not current grammar.
- `dormant/` — retired witness code and data available for inspection.
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
