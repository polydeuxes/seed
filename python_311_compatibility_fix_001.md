# Python 3.11 Compatibility Fix 001

## Detected compatibility defect

The constitutional pipeline public import path failed under Python 3.11 with an import-time syntax error in `seed_runtime/constitutional_pipeline.py`.

## Repository Python baseline before the change

The repository already declared Python 3.11 or newer in `pyproject.toml`:

```toml
requires-python = ">=3.11"
```

`README.md` also stated that the project should be installed in an environment with Python 3.11 or newer.

No conflicting repository declaration requiring a version newer than Python 3.11 was found.

## Final declared baseline

```text
Python >= 3.11
```

## Exact syntax defect

Python 3.11 rejected this nested f-string expression:

```python
f"Available capability keys: {'; '.join(f'{name}=[{', '.join(keys) or 'none'}]' for name, keys in explanation.available_capability_keys) or 'none'}"
```

The incompatible sub-expression was:

```python
f'{name}=[{', '.join(keys) or 'none'}]'
```

Python 3.11 reported:

```text
SyntaxError: f-string: f-string: expecting '}'
```

## Files audited

Minimum requested files audited:

- `seed_runtime/bounded_constitutional_question.py`
- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_pipeline.py`
- `seed_runtime/constitutional_pipeline_diagnostic.py`
- `scripts/seed_local.py`

Additional files changed by recent constitutional pipeline implementation commits inspected:

- `constitutional_pipeline_integration_wiring_001.md`
- `constitutional_pipeline_operational_documentation_001.md`
- `constitutional_pipeline_operations.md`
- `constitutional_pipeline_provenance_explanation_implementation_001.md`
- `constitutional_pipeline_real_inquiry_campaign_001.md`
- `constitutional_pipeline_self_consumption_demonstration_001.md`
- `docs/README.md`
- `seed_runtime/question_surface_inventory.py`
- `tests/test_constitutional_pipeline_integration_wiring.py`
- `tests/test_constitutional_pipeline_provenance_explanation.py`

## Additional incompatibilities found

No additional Python 3.12-only syntax or standard-library usage was found in the audited constitutional pipeline implementation files.

Specifically, the audit did not find incompatible use of:

- Python 3.12 `type` statement aliases;
- unsupported `typing.override` imports;
- `itertools.batched`;
- Python 3.12-only `pathlib` APIs in the audited files;
- other syntax rejected by Python 3.11 compilation across `seed_runtime` and `scripts`.

## Fixes applied

- Replaced the Python 3.12-style nested f-string with Python 3.11-compatible string composition while preserving rendered output.
- Added an import regression test covering the constitutional pipeline modules.

## Packaging metadata changes

No packaging metadata change was required because `pyproject.toml` already declared:

```toml
requires-python = ">=3.11"
```

No second packaging configuration was introduced.

## CI changes

Added a minimal GitHub Actions compatibility workflow that runs under Python 3.11 and the current primary runtime target:

- `python -m compileall -q seed_runtime scripts`
- `pytest -q`

## Documentation changes

Updated `README.md` to state that compatibility must be validated against the minimum supported interpreter, Python 3.11.

## Python interpreters used for validation

- Default `python`: Python 3.14.4
- Default `python3`: Python 3.14.4
- Direct Python 3.11 validation: Python 3.11.15 via `PYENV_VERSION=3.11.15 python`

The plain `python3.11` shim was present but not selected by pyenv in the shell. Direct Python 3.11 validation was performed with the exact installed interpreter version through pyenv.

## Compile commands

Passed:

```bash
PYENV_VERSION=3.11.15 python -m compileall -q seed_runtime scripts
python -m compileall -q seed_runtime scripts
```

## Tests executed

Passed:

```bash
PYENV_VERSION=3.11.15 pytest -q tests/test_bounded_constitutional_question.py tests/test_constitutional_question_projection.py tests/test_constitutional_capability_projection.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py tests/test_constitutional_pipeline.py tests/test_constitutional_pipeline_public_surface.py tests/test_constitutional_pipeline_diagnostic.py tests/test_constitutional_pipeline_provenance_explanation.py tests/test_constitutional_pipeline_integration_wiring.py
```

Passed:

```bash
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Full-suite result under the default Python 3.14.4 interpreter:

```bash
pytest -q
```

Result: failed with 8 pre-existing/unrelated failures in architecture generator stability, consumer dependency audit filtering, observation inventory filtering, and observation utilization filtering. The constitutional pipeline focused suite passed.

## Command-level verification

Passed under Python 3.11.15:

```bash
PYENV_VERSION=3.11.15 python scripts/seed_local.py --help
PYENV_VERSION=3.11.15 python scripts/seed_local.py --constitutional-pipeline --operator-inquiry "Compatibility verification; testimony only." --inquiry-provenance "operator:python-311-compatibility" --bounded-question "Is the constitutional pipeline importable?" --constitutional-intent "compatibility verification" --scope-status bounded --selection-key process --json
```

Passed under default Python 3.14.4:

```bash
python scripts/seed_local.py --help
python scripts/seed_local.py --constitutional-pipeline --operator-inquiry "Compatibility verification; testimony only." --inquiry-provenance "operator:python-311-compatibility" --bounded-question "Is the constitutional pipeline importable?" --constitutional-intent "compatibility verification" --scope-status bounded --selection-key process --json
```

## Files changed

- `.github/workflows/python-compatibility.yml`
- `README.md`
- `seed_runtime/constitutional_pipeline.py`
- `tests/test_constitutional_pipeline_public_surface.py`
- `python_311_compatibility_fix_001.md`

## LOC delta

+247 / -1

## Commit hash

To be finalized after commit creation; the final task response records the exact commit hash.

## Explicit answers

```text
Is Python 3.11 a supported runtime?

Yes.
```

```text
Was upgrading the operator runtime required?

No.
```

```text
Did this task change constitutional pipeline behavior?

No.
```

```text
Was the public pipeline import verified under Python 3.11?

Yes, with Python 3.11.15 via `PYENV_VERSION=3.11.15 python -m compileall -q seed_runtime scripts`, the focused constitutional pipeline pytest suite, and command-level `scripts/seed_local.py --constitutional-pipeline ... --json` verification.
```
