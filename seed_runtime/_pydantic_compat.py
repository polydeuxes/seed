"""Tiny local fallback for environments without Pydantic installed.

The project declares Pydantic as a dependency. This compatibility layer exists only
so the repository's dependency-light tests can run in restricted sandboxes where
packages cannot be fetched.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class _FieldInfo:
    def __init__(self, default: Any = ..., default_factory: Any = None) -> None:
        self.default = default
        self.default_factory = default_factory

    def make_default(self) -> Any:
        if self.default_factory is not None:
            return self.default_factory()
        if self.default is ...:
            raise TypeError("missing required field")
        return deepcopy(self.default)


def Field(default: Any = ..., *, default_factory: Any = None) -> _FieldInfo:
    return _FieldInfo(default=default, default_factory=default_factory)


class ConfigDict(dict):
    pass


class BaseModel:
    model_config: ConfigDict = ConfigDict()

    def __init__(self, **data: Any) -> None:
        fields = getattr(type(self), "__annotations__", {})
        for name in fields:
            if name in data:
                value = data.pop(name)
            else:
                default = _lookup_default(type(self), name)
                if isinstance(default, _FieldInfo):
                    value = default.make_default()
                elif default is _MISSING:
                    raise TypeError(f"missing required field: {name}")
                else:
                    value = deepcopy(default)
            object.__setattr__(self, name, value)
        for name, value in data.items():
            object.__setattr__(self, name, value)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(type(self), "model_config", {}).get("frozen"):
            raise TypeError(f"{type(self).__name__} is frozen")
        object.__setattr__(self, name, value)

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({fields})"

    def model_dump(self, *, mode: str | None = None) -> dict[str, Any]:
        return deepcopy(self.__dict__)

    def model_copy(
        self, *, deep: bool = False, update: dict[str, Any] | None = None
    ) -> Any:
        data = deepcopy(self.__dict__) if deep else dict(self.__dict__)
        if update:
            data.update(update)
        return type(self)(**data)


_MISSING = object()


def _lookup_default(cls: type, name: str) -> Any:
    for base in cls.__mro__:
        if name in base.__dict__:
            return base.__dict__[name]
    return _MISSING
