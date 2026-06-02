import pytest

from seed_runtime.registry import ManifestError, ToolRegistry, toolkit_from_manifest


def test_loads_echo_manifest():
    registry = ToolRegistry()
    toolkit = registry.load_manifest("toolkits/core/echo/toolkit.yaml")

    assert toolkit.name == "echo"
    assert registry.require("echo").policy_action == "echo.run"


def test_rejects_invalid_manifest():
    with pytest.raises(ManifestError):
        toolkit_from_manifest({"id": "bad"})
