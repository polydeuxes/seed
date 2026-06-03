"""Read-only observation source for common Ansible inventory file patterns."""

from __future__ import annotations

import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from seed_runtime.ids import new_id
from seed_runtime.observations import Observation, ObservationSourceType


class AnsibleInventoryObservationSource:
    """Import authoritative host identities from a local Ansible inventory file.

    This intentionally supports only common static INI and mapping-based YAML
    inventories. It does not invoke Ansible, expand host patterns, resolve
    aliases, validate connectivity, or perform any network access.
    """

    source_type: ObservationSourceType = "imported"
    confidence = 0.95
    _SUPPORTED_SUFFIXES = {".ini", ".yml", ".yaml"}

    def __init__(self, path: str | Path, *, name: str = "ansible_inventory") -> None:
        self.path = Path(path)
        self.name = name
        if self.path.suffix.lower() not in self._SUPPORTED_SUFFIXES:
            raise ValueError(
                "unsupported Ansible inventory format; expected .ini, .yml, or .yaml"
            )

    def collect(self) -> list[Observation]:
        """Parse the inventory file and emit ordinary identity observations."""

        try:
            text = self.path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Ansible inventory must be UTF-8: {self.path}") from exc

        suffix = self.path.suffix.lower()
        memberships = (
            self._parse_ini(text) if suffix == ".ini" else self._parse_yaml(text)
        )
        observed_at = datetime.now(timezone.utc)
        observations: list[Observation] = []
        for hostname, host_data in memberships.items():
            groups = host_data["groups"]
            ansible_host = host_data.get("ansible_host")
            primary_group = groups[0]
            observations.append(
                self._observation(observed_at, hostname, "hostname", hostname, primary_group)
            )
            if ansible_host is not None:
                for predicate in ("ansible_host", "ip_address", "alias"):
                    observations.append(
                        self._observation(
                            observed_at,
                            hostname,
                            predicate,
                            ansible_host,
                            primary_group,
                        )
                    )
            for group in groups:
                observations.append(
                    self._observation(observed_at, hostname, "group", group, group)
                )
        return observations

    def _observation(
        self,
        observed_at: datetime,
        subject: str,
        predicate: str,
        value: str,
        inventory_group: str,
    ) -> Observation:
        return Observation(
            id=new_id("obs_ansible_inventory"),
            source_type=self.source_type,
            observed_at=observed_at,
            subject=subject,
            predicate=predicate,
            value=value,
            confidence=self.confidence,
            metadata={
                "source_name": "ansible_inventory",
                "inventory_path": str(self.path),
                "inventory_group": inventory_group,
            },
        )

    def _parse_ini(self, text: str) -> dict[str, dict[str, Any]]:
        hosts: dict[str, dict[str, Any]] = {}
        group: str | None = None
        ignored_section = False
        for line_number, raw_line in enumerate(text.splitlines(), start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue
            if stripped.startswith("["):
                if not stripped.endswith("]"):
                    raise ValueError(
                        f"unsupported Ansible INI inventory at line {line_number}: malformed section"
                    )
                section = stripped[1:-1].strip()
                if not section:
                    raise ValueError(
                        f"unsupported Ansible INI inventory at line {line_number}: empty section"
                    )
                ignored_section = section.endswith(":vars") or section.endswith(":children")
                group = section.split(":", 1)[0] if not ignored_section else None
                continue
            if ignored_section:
                continue
            if group is None:
                raise ValueError(
                    f"unsupported Ansible INI inventory at line {line_number}: hosts must be in a group"
                )
            try:
                fields = shlex.split(raw_line, comments=True, posix=True)
            except ValueError as exc:
                raise ValueError(
                    f"unsupported Ansible INI inventory at line {line_number}: {exc}"
                ) from exc
            if not fields:
                continue
            hostname = fields[0]
            if "[" in hostname or "]" in hostname:
                raise ValueError(
                    f"unsupported Ansible INI host pattern at line {line_number}: {hostname}"
                )
            variables = {
                key: value
                for field in fields[1:]
                if "=" in field
                for key, value in [field.split("=", 1)]
            }
            self._record_host(hosts, hostname, group, variables.get("ansible_host"))
        return hosts

    def _parse_yaml(self, text: str) -> dict[str, dict[str, Any]]:
        root = _parse_simple_yaml_mapping(text)
        hosts: dict[str, dict[str, Any]] = {}
        recognized_group = False

        def walk_group(group: str, value: Any) -> None:
            nonlocal recognized_group
            if not isinstance(value, dict):
                raise ValueError(
                    f"unsupported Ansible YAML inventory group {group!r}: expected a mapping"
                )
            if "hosts" in value:
                recognized_group = True
                group_hosts = value["hosts"]
                if not isinstance(group_hosts, dict):
                    raise ValueError(
                        f"unsupported Ansible YAML inventory group {group!r}: hosts must be a mapping"
                    )
                for hostname, variables in group_hosts.items():
                    if variables is None:
                        variables = {}
                    if not isinstance(variables, dict):
                        raise ValueError(
                            f"unsupported Ansible YAML host {hostname!r}: variables must be a mapping"
                        )
                    ansible_host = variables.get("ansible_host")
                    self._record_host(hosts, hostname, group, ansible_host)
            children = value.get("children", {})
            if not isinstance(children, dict):
                raise ValueError(
                    f"unsupported Ansible YAML inventory group {group!r}: children must be a mapping"
                )
            for child_group, child_value in children.items():
                walk_group(child_group, child_value)

        for group, value in root.items():
            walk_group(group, value)
        if root and not recognized_group:
            raise ValueError(
                "unsupported Ansible YAML inventory: expected group mappings containing hosts"
            )
        return hosts

    @staticmethod
    def _record_host(
        hosts: dict[str, dict[str, Any]], hostname: Any, group: Any, ansible_host: Any
    ) -> None:
        hostname_text = str(hostname).strip()
        group_text = str(group).strip()
        entry = hosts.setdefault(hostname_text, {"groups": []})
        if group_text not in entry["groups"]:
            entry["groups"].append(group_text)
        if ansible_host is not None and str(ansible_host).strip():
            entry["ansible_host"] = str(ansible_host).strip()


def _parse_simple_yaml_mapping(text: str) -> dict[str, Any]:
    """Parse the mapping-only YAML subset used by common static inventories."""

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line[: len(raw_line) - len(raw_line.lstrip())]:
            raise ValueError(
                f"unsupported Ansible YAML inventory at line {line_number}: tabs are not supported"
            )
        content = _strip_yaml_comment(raw_line).rstrip()
        if not content.strip() or content.lstrip().startswith("---"):
            continue
        indent = len(content) - len(content.lstrip(" "))
        stripped = content.strip()
        if stripped.startswith("-") or ":" not in stripped:
            raise ValueError(
                f"unsupported Ansible YAML inventory at line {line_number}: only mappings are supported"
            )
        key_text, value_text = stripped.split(":", 1)
        key = _yaml_scalar(key_text.strip())
        if not isinstance(key, str) or not key:
            raise ValueError(
                f"unsupported Ansible YAML inventory at line {line_number}: mapping keys must be names"
            )
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        value_text = value_text.strip()
        if not value_text or value_text == "{}":
            value: Any = {} if not value_text or value_text == "{}" else None
        else:
            value = _yaml_scalar(value_text)
        parent[key] = value
        if isinstance(value, dict):
            stack.append((indent, value))
    return root


def _strip_yaml_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, character in enumerate(line):
        if escaped:
            escaped = False
            continue
        if character == "\\" and quote == '"':
            escaped = True
            continue
        if character in {"'", '"'}:
            quote = None if quote == character else character if quote is None else quote
        elif character == "#" and quote is None and (index == 0 or line[index - 1].isspace()):
            return line[:index]
    return line


def _yaml_scalar(value: str) -> Any:
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        if value[0] == "'":
            return value[1:-1].replace("''", "'")
        return bytes(value[1:-1], "utf-8").decode("unicode_escape")
    return value
