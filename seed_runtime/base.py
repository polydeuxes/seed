"""Shared Pydantic base model for Seed runtime domain objects."""

from __future__ import annotations

from importlib.util import find_spec

if find_spec("pydantic") is not None:
    from pydantic import BaseModel, ConfigDict
else:
    from seed_runtime._pydantic_compat import BaseModel, ConfigDict


class SeedModel(BaseModel):
    """Base model with immutable, assignment-friendly domain semantics."""

    model_config = ConfigDict(frozen=True)
