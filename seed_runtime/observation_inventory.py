"""Implementation-backed inventory for observation-producing surfaces."""

from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ObservationProviderInventory:
    name: str
    class_name: str
    module: str
    path: str
    source_type: str | None
    observation_count: int
    predicates: tuple[str, ...]

    @property
    def predicate_count(self) -> int:
        return len(self.predicates)


@dataclass(frozen=True)
class ObservationPredicateInventory:
    predicate: str
    providers: tuple[str, ...]

    @property
    def provider_count(self) -> int:
        return len(self.providers)


@dataclass(frozen=True)
class ObservationFamilyInventory:
    family: str
    predicates: tuple[str, ...]
    providers: tuple[str, ...]

    @property
    def predicate_count(self) -> int:
        return len(self.predicates)

    @property
    def provider_count(self) -> int:
        return len(self.providers)


@dataclass(frozen=True)
class ObservationInventory:
    providers: tuple[ObservationProviderInventory, ...]
    predicates: tuple[ObservationPredicateInventory, ...]
    families: tuple[ObservationFamilyInventory, ...]
    metadata: dict[str, str] = field(default_factory=dict)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "providers": [
                {**asdict(provider), "predicates": list(provider.predicates), "predicate_count": provider.predicate_count}
                for provider in self.providers
            ],
            "predicates": [
                {"predicate": predicate.predicate, "provider_count": predicate.provider_count, "providers": list(predicate.providers)}
                for predicate in self.predicates
            ],
            "families": [
                {"family": family.family, "predicate_count": family.predicate_count, "provider_count": family.provider_count, "predicates": list(family.predicates), "providers": list(family.providers)}
                for family in self.families
            ],
            "summary": {
                "provider_count": len(self.providers),
                "predicate_count": len(self.predicates),
                "family_count": len(self.families),
            },
            "metadata": dict(self.metadata),
        }


def build_observation_inventory(
    root: str | Path | None = None,
    *,
    provider_filter: str | None = None,
    predicate_filter: str | None = None,
) -> ObservationInventory:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    runtime_root = repo_root / "seed_runtime"
    providers: list[ObservationProviderInventory] = []
    if runtime_root.exists():
        for path in sorted(runtime_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            providers.extend(_providers_from_file(path, repo_root))
    if provider_filter:
        providers = [p for p in providers if provider_filter in {p.name, p.class_name}]
    if predicate_filter:
        providers = [
            ObservationProviderInventory(
                name=p.name,
                class_name=p.class_name,
                module=p.module,
                path=p.path,
                source_type=p.source_type,
                observation_count=p.observation_count,
                predicates=tuple(q for q in p.predicates if q == predicate_filter),
            )
            for p in providers
            if predicate_filter in p.predicates
        ]
    predicate_to_providers: dict[str, set[str]] = defaultdict(set)
    for provider in providers:
        for predicate in provider.predicates:
            predicate_to_providers[predicate].add(provider.name)
    predicates = tuple(
        ObservationPredicateInventory(predicate, tuple(sorted(names)))
        for predicate, names in sorted(predicate_to_providers.items())
    )
    families = _families(predicates)
    metadata = {
        "providers_discovered_from": "Python classes implementing collect() and named like observation providers under seed_runtime/",
        "predicates_discovered_from": "AST string literals passed to Observation(predicate=...) or provider _observation(..., predicate, ...) calls",
        "families_discovered_from": "predicate name prefixes before the first underscore",
    }
    return ObservationInventory(tuple(sorted(providers, key=lambda p: p.name)), predicates, families, metadata)


def _providers_from_file(path: Path, repo_root: Path) -> list[ObservationProviderInventory]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    module = path.relative_to(repo_root).with_suffix("").as_posix().replace("/", ".")
    module_predicates = _module_predicate_constants(tree)
    providers = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or not _is_provider_class(node):
            continue
        predicates = set(_predicate_literals(node))
        if node.name == "LocalHostObservationSource":
            predicates.update(module_predicates.get("_LISTENER_QUESTIONS", set()))
        predicates = sorted(predicates)
        providers.append(
            ObservationProviderInventory(
                name=_class_string_attr(node, "name") or _default_provider_name(node.name),
                class_name=node.name,
                module=module,
                path=path.relative_to(repo_root).as_posix(),
                source_type=_class_string_attr(node, "source_type"),
                observation_count=len(predicates),
                predicates=tuple(predicates),
            )
        )
    return providers


def _is_provider_class(node: ast.ClassDef) -> bool:
    if node.name == "ObservationSource" or any(_call_name(base) == "Protocol" for base in node.bases):
        return False
    has_collect = any(isinstance(item, ast.FunctionDef) and item.name == "collect" for item in node.body)
    return has_collect and (node.name.endswith("ObservationSource") or _class_string_attr(node, "source_type") is not None)


def _module_predicate_constants(tree: ast.Module) -> dict[str, set[str]]:
    constants: dict[str, set[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        if not names or not isinstance(node.value, ast.Dict):
            continue
        keys = {
            key.value
            for key in node.value.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        }
        for name in names:
            if name.endswith("_QUESTIONS"):
                constants[name] = keys
    return constants


def _predicate_literals(node: ast.ClassDef) -> set[str]:
    predicates: set[str] = set()
    for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
        func_name = _call_name(call.func)
        if func_name == "Observation":
            for kw in call.keywords:
                if kw.arg == "predicate" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    predicates.add(kw.value.value)
        if func_name and func_name.endswith("_observation") and len(call.args) >= 3:
            arg = call.args[2]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                predicates.add(arg.value)
    return predicates


def _call_name(func: ast.AST) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _class_string_attr(node: ast.ClassDef, name: str) -> str | None:
    for item in node.body:
        if isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name) and target.id == name and isinstance(item.value, ast.Constant) and isinstance(item.value.value, str):
                    return item.value.value
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name) and item.target.id == name and isinstance(item.value, ast.Constant) and isinstance(item.value.value, str):
            return item.value.value
    return None


def _default_provider_name(class_name: str) -> str:
    suffix = "ObservationSource"
    stem = class_name[: -len(suffix)] if class_name.endswith(suffix) else class_name
    out = []
    for i, char in enumerate(stem):
        if i and char.isupper() and (not stem[i - 1].isupper()):
            out.append("_")
        out.append(char.lower())
    return "".join(out)


def _families(predicates: tuple[ObservationPredicateInventory, ...]) -> tuple[ObservationFamilyInventory, ...]:
    grouped: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"predicates": set(), "providers": set()})
    for predicate in predicates:
        family = predicate.predicate.split("_", 1)[0]
        grouped[family]["predicates"].add(predicate.predicate)
        grouped[family]["providers"].update(predicate.providers)
    return tuple(
        ObservationFamilyInventory(name, tuple(sorted(values["predicates"])), tuple(sorted(values["providers"])))
        for name, values in sorted(grouped.items())
    )


def format_observation_inventory(inventory: ObservationInventory) -> str:
    lines = [
        "Observation Inventory",
        "",
        f"Providers: {len(inventory.providers)}",
        f"Predicates: {len(inventory.predicates)}",
        f"Families: {len(inventory.families)}",
        "",
        f"providers discovered from: {inventory.metadata['providers_discovered_from']}",
        f"predicates discovered from: {inventory.metadata['predicates_discovered_from']}",
        f"families discovered from: {inventory.metadata['families_discovered_from']}",
        "",
        "Providers",
        "Provider | Observation Count | Predicate Count | Example Predicates",
    ]
    for provider in inventory.providers:
        lines.append(f"{provider.name} | {provider.observation_count} | {provider.predicate_count} | {', '.join(provider.predicates[:5])}")
    lines.extend(["", "Predicates", "Predicate | Provider Count | Provider Examples"])
    for predicate in inventory.predicates:
        lines.append(f"{predicate.predicate} | {predicate.provider_count} | {', '.join(predicate.providers[:5])}")
    lines.extend(["", "Families", "Family | Predicate Count | Provider Count"])
    for family in inventory.families:
        lines.append(f"{family.family} | {family.predicate_count} | {family.provider_count}")
    return "\n".join(lines)
