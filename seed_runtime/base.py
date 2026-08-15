"""Shared Pydantic base model for Seed runtime domain objects."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class SeedModel(BaseModel):
    """Base model with immutable, assignment-friendly domain semantics."""

    model_config = ConfigDict(frozen=True)
