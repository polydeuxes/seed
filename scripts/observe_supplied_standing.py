"""Observe each current Standing supplied to a Responsibility that reads it.

This asks one question of Seed's own runtime: when a Responsibility is supplied a
Standing, what exact coordinates does that Standing carry, and does anything
observable distinguish a Standing carried along a live road from one supplied
at a public boundary?

The observer is given no discriminator.  It never reads the `carried` control
flag, and it never reads the name of the validator that ran.  It records the
exact coordinates present in the supplied Standing, the exact occurrence that
Standing names as its boundary, whether that occurrence was appended earlier in
this same observed run, and whether a complete Locality reconstruction happened
inside the call.

The calling function's name is recorded but held aside.  It is written to a
separate section of the artifact so a comparison against it can only be made
after the coordinate populations are frozen.

Set ``SEED_SUPPLIED_STANDING`` to an output path when invoking pytest.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from contextvars import ContextVar
from hashlib import sha256
import inspect
import json
import os
from pathlib import Path
from typing import Any

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
import seed_runtime.operator_current_coordinates as standing_module

OUTPUT_ENVIRONMENT_COORDINATE = "SEED_SUPPLIED_STANDING"

STANDING_PARAMETERS = (
    "locality_standing",
    "responsibility_assignment_standing",
    "applicability_standing",
    "prior_standing",
    "responsibility_standing",
    "operator_locality_standing",
)

_appended: dict[str, int] = {}
_supplied: list[dict[str, Any]] = []
_reconstructions: ContextVar[list | None] = ContextVar(
    "standing_reconstructions", default=None
)
_originals: list[tuple[Any, str, Any]] = []
_depth = {"value": 0}


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode(
            "utf-8"
        )
    ).hexdigest()[:16]


def _supplied_standing(bound: inspect.BoundArguments) -> tuple[str, Any] | None:
    for name in STANDING_PARAMETERS:
        if name in bound.arguments and isinstance(bound.arguments[name], dict):
            return name, bound.arguments[name]
    return None


def _standing_shape(standing: dict[str, Any]) -> dict[str, Any]:
    """Exact observable coordinates of one supplied Standing."""

    through = standing.get("through_event_occurrence_identity")
    identity_valued = sorted(
        key
        for key, value in standing.items()
        if isinstance(value, str) and value in _appended
    )
    populated = sorted(
        key
        for key, value in standing.items()
        if isinstance(value, (dict, list)) and len(value) > 0
    )
    return {
        "coordinate_names": sorted(standing),
        "identity_valued_coordinates": identity_valued,
        "populated_coordinates": populated,
        "through_occurrence_present": isinstance(through, str) and bool(through),
        "through_occurrence_was_appended_in_this_run": through in _appended,
        "through_occurrence_append_position": _appended.get(through),
        "appended_occurrences_before_this_call": len(_appended),
        "through_occurrence_is_latest_append": (
            _appended.get(through) == len(_appended) - 1
            if through in _appended
            else None
        ),
    }


def _wrap_recorder(module: Any, name: str, function: Any) -> None:
    try:
        signature = inspect.signature(function)
    except (TypeError, ValueError):
        return
    if not any(p in signature.parameters for p in STANDING_PARAMETERS):
        return
    _originals.append((module, name, function))

    def wrapped(*arguments, **keywords):
        try:
            bound = signature.bind_partial(*arguments, **keywords)
        except TypeError:
            return function(*arguments, **keywords)
        supplied = _supplied_standing(bound)
        if supplied is None or _depth["value"]:
            return function(*arguments, **keywords)
        parameter_name, standing = supplied
        shape = _standing_shape(standing)
        token = _reconstructions.set([])
        _depth["value"] += 1
        outcome = "yielded"
        try:
            return function(*arguments, **keywords)
        except BaseException as error:
            outcome = type(error).__name__
            raise
        finally:
            _depth["value"] -= 1
            rebuilt = _reconstructions.get() or []
            _reconstructions.reset(token)
            _supplied.append(
                {
                    "standing_parameter": parameter_name,
                    "standing_shape": shape,
                    "reconstructions_inside_call": len(rebuilt),
                    "reconstruction_boundaries": rebuilt[:4],
                    "outcome": outcome,
                    "held_aside_recorder": f"{module.__name__.split('.')[-1]}.{name}",
                }
            )

    setattr(module, name, wrapped)


def _wrap_reconstruction(name: str) -> None:
    original = getattr(standing_module, name)
    _originals.append((standing_module, name, original))

    def wrapped(*arguments, **keywords):
        seen = _reconstructions.get()
        if seen is not None:
            seen.append(
                {
                    "reader": name,
                    "locality_identity": keywords.get("locality_identity"),
                    "through": keywords.get("through_event_occurrence_identity"),
                }
            )
        return original(*arguments, **keywords)

    setattr(standing_module, name, wrapped)


def _wrap_append(cls: type, method_name: str) -> None:
    original = getattr(cls, method_name)
    _originals.append((cls, method_name, original))

    def wrapped(ledger, *arguments, **keywords):
        produced = original(ledger, *arguments, **keywords)
        events = (produced,) if method_name == "append" else produced
        for event in events:
            _appended.setdefault(event.identity, len(_appended))
        return produced

    setattr(cls, method_name, wrapped)


def pytest_configure(config: object) -> None:
    del config
    import importlib
    import pkgutil
    import seed_runtime

    for cls in (EventLedger, SQLiteEventLedger):
        for method_name in ("append", "append_many"):
            _wrap_append(cls, method_name)
    for name in (
        "read_operator_current_coordinates",
        "read_operator_current_coordinates_through",
    ):
        _wrap_reconstruction(name)
    for info in pkgutil.iter_modules(seed_runtime.__path__):
        try:
            module = importlib.import_module(f"seed_runtime.{info.name}")
        except Exception:
            continue
        for name, function in list(vars(module).items()):
            if not callable(function) or not name.startswith(("record_", "_record_")):
                continue
            if getattr(function, "__module__", None) != module.__name__:
                continue
            _wrap_recorder(module, name, function)


def pytest_unconfigure(config: object) -> None:
    del config
    while _originals:
        holder, name, original = _originals.pop()
        setattr(holder, name, original)


def _analyze() -> dict[str, Any]:
    populations: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    for supplied_standing in _supplied:
        shape = supplied_standing["standing_shape"]
        key = (
            shape["through_occurrence_was_appended_in_this_run"],
            shape["through_occurrence_is_latest_append"],
            supplied_standing["reconstructions_inside_call"] > 0,
        )
        populations[key].append(supplied_standing)

    rows = []
    for key, members in sorted(populations.items(), key=lambda item: str(item[0])):
        appended_here, is_latest, reconstructed = key
        recorders = Counter(member["held_aside_recorder"] for member in members)
        rows.append(
            {
                "through_occurrence_was_appended_in_this_run": appended_here,
                "through_occurrence_is_latest_append": is_latest,
                "reconstructed_inside_call": reconstructed,
                "supplied_standing_count": len(members),
                "distinct_coordinate_name_sets": len(
                    {
                        _digest(member["standing_shape"]["coordinate_names"])
                        for member in members
                    }
                ),
                "held_aside_recorders": dict(recorders.most_common(6)),
            }
        )

    coordinate_sets = {
        _digest(supplied_standing["standing_shape"]["coordinate_names"]): supplied_standing[
            "standing_shape"
        ]["coordinate_names"]
        for supplied_standing in _supplied
    }
    return {
        "observer": (
            "each current Standing supplied to a Responsibility; the observer reads no control flag "
            "and no validator name when separating populations"
        ),
        "supplied_standing_count": len(_supplied),
        "appended_occurrence_count": len(_appended),
        "distinct_supplied_coordinate_sets": len(coordinate_sets),
        "populations": rows,
        "supplied_coordinate_sets": coordinate_sets,
    }


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    del session
    output = os.environ.get(OUTPUT_ENVIRONMENT_COORDINATE)
    if not output:
        return
    result = _analyze()
    result["pytest_exit_status"] = exitstatus
    path = Path(output)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        f"\nSUPPLIED STANDING {path} supplied={result['supplied_standing_count']} "
        f"populations={len(result['populations'])}"
    )
