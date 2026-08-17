"""Event occurrence and durable read boundary."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import math
from typing import Any

from seed_runtime.secrets import (
    is_secret_boundary_key,
)

def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


_SCREENED_EVENT_MATERIAL_TOKEN = object()


class _ScreenedEventMaterial(dict[str, Any]):
    """Runtime-local evidence that durable JSON keys were screened."""

    def __init__(self, material: dict[str, Any], token: object) -> None:
        if token is not _SCREENED_EVENT_MATERIAL_TOKEN:
            raise TypeError("screened Event materials come from the durable decoder")
        super().__init__(material)


def _screen_durable_event_object(value: dict[str, Any]) -> dict[str, Any]:
    for key in value:
        if is_secret_boundary_key(key):
            raise ValueError(
                f"secret field is not allowed in durable event material: {key}"
            )
    return value


def _require_preservable_material(value: Any, path: str = "material") -> None:
    """Refuse material that cannot cross the durable boundary exactly."""

    if type(value) is dict:
        for key, nested in value.items():
            if is_secret_boundary_key(key):
                raise ValueError(
                    f"secret field is not allowed in durable event material: {key}"
                )
            if type(key) is not str:
                raise ValueError(
                    f"{path} carries a {type(key).__name__} key {key!r}; a durable "
                    "store preserves only exact string keys"
                )
            _require_preservable_material(nested, f"{path}[{key!r}]")
        return
    if type(value) is list:
        for index, nested in enumerate(value):
            _require_preservable_material(nested, f"{path}[{index}]")
        return
    if type(value) is tuple:
        raise ValueError(
            f"{path} carries a tuple; a durable store returns it as a list, so "
            "pass a list to preserve it exactly"
        )
    if type(value) is float and not math.isfinite(value):
        raise ValueError(
            f"{path} carries {value!r}, which is not a JSON number; a durable "
            "store could hold it only under a permissive reader"
        )
    if value is None or type(value) in (str, int, float, bool):
        return
    raise ValueError(
        f"{path} carries {type(value).__name__}, which a durable store cannot "
        "preserve exactly"
    )


def _decode_screened_event_material(raw_material: str) -> Any:
    """Decode durable JSON while screening each dictionary as it is built."""

    material = json.loads(raw_material, object_hook=_screen_durable_event_object)
    if isinstance(material, dict):
        return _ScreenedEventMaterial(material, _SCREENED_EVENT_MATERIAL_TOKEN)
    return material


class Event:
    __slots__ = (
        "identity",
        "kind",
        "timestamp",
        "material",
        "exact_material",
        "locality_identity",
        "_fixed",
        "__weakref__",
    )

    def __init__(
        self,
        *,
        identity: str,
        kind: str,
        timestamp: datetime | None = None,
        material: dict[str, Any] | None = None,
        exact_material: bytes | None = None,
        locality_identity: str | None = None,
    ) -> None:
        material = {} if material is None else material
        if type(identity) is not str or not identity:
            raise ValueError("event identity must be a non-empty string")
        if type(kind) is not str or not kind:
            raise ValueError("event kind must be a non-empty string")
        if timestamp is not None and type(timestamp) is not datetime:
            raise ValueError("event timestamp must be a datetime or absent")
        if type(material) is not dict and not isinstance(material, _ScreenedEventMaterial):
            raise ValueError("event material must be an exact dictionary")
        if exact_material is not None and type(exact_material) is not bytes:
            raise ValueError("event exact material must be exact bytes or absent")
        if locality_identity is not None and type(locality_identity) is not str:
            raise ValueError("event locality identity must be a string or absent")
        if not isinstance(material, _ScreenedEventMaterial):
            _require_preservable_material(material, "event.material")
        object.__setattr__(self, "identity", identity)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "timestamp", utc_now() if timestamp is None else timestamp)
        object.__setattr__(
            self,
            "material",
            dict(material) if isinstance(material, _ScreenedEventMaterial) else material,
        )
        object.__setattr__(self, "exact_material", exact_material)
        object.__setattr__(self, "locality_identity", locality_identity)
        object.__setattr__(self, "_fixed", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_fixed", False):
            raise AttributeError("Event coordinates are fixed")
        object.__setattr__(self, name, value)

    def __deepcopy__(self, memo: dict[int, Any]) -> Event:
        repeated = Event(
            identity=self.identity,
            kind=self.kind,
            timestamp=self.timestamp,
            material=deepcopy(self.material, memo),
            exact_material=self.exact_material,
            locality_identity=self.locality_identity,
        )
        memo[id(self)] = repeated
        return repeated

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return all(
            getattr(self, coordinate) == getattr(other, coordinate)
            for coordinate in (
                "identity",
                "kind",
                "timestamp",
                "material",
                "exact_material",
                "locality_identity",
            )
        )

    def __repr__(self) -> str:
        return (
            "Event("
            f"identity={self.identity!r}, kind={self.kind!r}, "
            f"timestamp={self.timestamp!r}, material={self.material!r}, "
            f"exact_material={self.exact_material!r}, "
            f"locality_identity={self.locality_identity!r})"
        )
