"""Minimal JSON-schema subset validator.

Seed generated tool contracts should stay simple. This validator supports the
subset used by the prototype: object, string, integer, number, boolean, array,
required, properties, additionalProperties, enum, and default-free nesting.
"""

from __future__ import annotations

from typing import Any


class SchemaValidationError(ValueError):
    """Raised when a value does not match a schema."""


def validate_schema_value(schema: dict[str, Any], value: Any, *, path: str = "$") -> Any:
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(value, dict):
            raise SchemaValidationError(f"{path} must be an object")
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise SchemaValidationError(f"{path}.{key} is required")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties", True) is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise SchemaValidationError(f"{path} has unexpected properties: {', '.join(extra)}")
        for key, subschema in properties.items():
            if key in value:
                validate_schema_value(subschema, value[key], path=f"{path}.{key}")
    elif expected == "string":
        if not isinstance(value, str):
            raise SchemaValidationError(f"{path} must be a string")
    elif expected == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise SchemaValidationError(f"{path} must be an integer")
    elif expected == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise SchemaValidationError(f"{path} must be a number")
    elif expected == "boolean":
        if not isinstance(value, bool):
            raise SchemaValidationError(f"{path} must be a boolean")
    elif expected == "array":
        if not isinstance(value, list):
            raise SchemaValidationError(f"{path} must be an array")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                validate_schema_value(item_schema, item, path=f"{path}[{idx}]")
    elif expected is None:
        pass
    else:
        raise SchemaValidationError(f"{path} uses unsupported schema type {expected!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise SchemaValidationError(f"{path} must be one of {schema['enum']!r}")
    return value
