"""Safe, content-based inspection for file-backed runtime inputs."""

from __future__ import annotations

import hashlib
import re
from importlib.util import find_spec
from pathlib import Path
from typing import Literal

from seed_runtime.base import SeedModel

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

DetectedInputFormat = Literal["json", "yaml", "ini", "unknown"]

_SAMPLE_LIMIT_BYTES = 64 * 1024
_READ_CHUNK_BYTES = 64 * 1024
_INI_SECTION = re.compile(r"^\[[^\[\]\r\n]+\]\s*$")
_YAML_MAPPING_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*\s*:\s*(?:#.*)?$")
_YAML_INVENTORY_KEYS = {"all", "children", "hosts", "vars"}
_EXTENSION_FORMATS = {
    ".ini": "ini",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
}


class InputArtifact(SeedModel):
    """Audit metadata and a bounded content-classification result for an input file."""

    path: str
    size_bytes: int
    sha256: str
    extension: str
    declared_purpose: str | None = None
    detected_format: DetectedInputFormat
    confidence: float
    warnings: list[str] = Field(default_factory=list)


class InputInspector:
    """Inspect file bytes without executing content or resolving embedded references."""

    @staticmethod
    def inspect_file(
        path: str | Path, declared_purpose: str | None = None
    ) -> InputArtifact:
        """Hash a file and classify a bounded prefix using content, not its extension."""

        input_path = Path(path)
        digest = hashlib.sha256()
        sample = bytearray()
        size_bytes = 0
        contains_null = False

        with input_path.open("rb") as input_file:
            while chunk := input_file.read(_READ_CHUNK_BYTES):
                digest.update(chunk)
                size_bytes += len(chunk)
                contains_null = contains_null or b"\x00" in chunk
                remaining = _SAMPLE_LIMIT_BYTES - len(sample)
                if remaining > 0:
                    sample.extend(chunk[:remaining])

        extension = input_path.suffix.lower()
        warnings: list[str] = []
        detected_format: DetectedInputFormat = "unknown"
        confidence = 0.0

        if size_bytes == 0:
            warnings.append("empty_file")
        elif contains_null:
            warnings.append("binary_or_null_bytes")
        else:
            detected_format, confidence = _detect_text_format(
                bytes(sample).decode("utf-8", errors="replace")
            )
            if detected_format == "unknown":
                warnings.append("unknown_format")

        expected_format = _EXTENSION_FORMATS.get(extension, extension.removeprefix("."))
        if (
            detected_format != "unknown"
            and expected_format
            and expected_format != detected_format
        ):
            warnings.append(f"extension_mismatch:{extension}!={detected_format}")

        return InputArtifact(
            path=str(input_path),
            size_bytes=size_bytes,
            sha256=digest.hexdigest(),
            extension=extension,
            declared_purpose=declared_purpose,
            detected_format=detected_format,
            confidence=confidence,
            warnings=warnings,
        )


def _detect_text_format(text: str) -> tuple[DetectedInputFormat, float]:
    first_non_whitespace = text.lstrip()[:1]
    if first_non_whitespace == "{":
        return "json", 0.95

    meaningful_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith(("#", ";"))
    ]
    if not meaningful_lines:
        return "unknown", 0.0

    first_line = meaningful_lines[0]
    if _INI_SECTION.fullmatch(first_line):
        return "ini", 0.95
    if first_non_whitespace == "[":
        return "json", 0.95

    yaml_lines = [line for line in meaningful_lines if line not in {"---", "..."}]
    if yaml_lines and _YAML_MAPPING_KEY.fullmatch(yaml_lines[0]):
        return "yaml", 0.85
    if any(_is_yaml_inventory_key(line) for line in yaml_lines):
        return "yaml", 0.85

    return "unknown", 0.0


def _is_yaml_inventory_key(line: str) -> bool:
    if not _YAML_MAPPING_KEY.fullmatch(line):
        return False
    key = line.split(":", 1)[0].strip()
    return key in _YAML_INVENTORY_KEYS
