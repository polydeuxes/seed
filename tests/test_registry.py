import pytest

from seed_runtime.registry import ManifestError, ToolRegistry, toolkit_from_manifest


def _manifest(*tools):
    return {
        "id": "tk_test",
        "name": "test toolkit",
        "summary": "Test toolkit.",
        "tools": list(tools) or [_tool("echo")],
    }


def _tool(name="echo", **overrides):
    data = {
        "name": name,
        "summary": f"Run {name}.",
        "input_schema": {},
        "output_schema": {},
        "policy_action": f"{name}.run",
        "implementation": f"tests.fixtures:{name}",
        "risk_class": "L1",
        "visibility": "model_visible",
    }
    data.update(overrides)
    return data


def test_loads_echo_manifest():
    registry = ToolRegistry()
    toolkit = registry.load_manifest("toolkits/core/echo/toolkit.yaml")

    assert toolkit.name == "echo"
    assert registry.require("echo").policy_action == "echo.run"


def test_existing_manifest_without_capabilities_loads_empty_capabilities():
    toolkit = toolkit_from_manifest(_manifest(_tool("echo")))

    assert toolkit.tools[0].capabilities == []


def test_manifest_capabilities_load_into_tool_spec():
    toolkit = toolkit_from_manifest(
        _manifest(_tool("verify_ssh_access", capabilities=["ssh_access", "endpoint_identity"]))
    )

    assert toolkit.tools[0].capabilities == ["ssh_access", "endpoint_identity"]


def test_manifest_capability_names_normalize_consistently():
    toolkit = toolkit_from_manifest(
        _manifest(_tool("verify_ssh_access", capabilities=[" SSH Access ", "Endpoint-Identity"]))
    )

    assert toolkit.tools[0].capabilities == ["ssh_access", "endpoint_identity"]


@pytest.mark.parametrize(
    "capabilities",
    [
        "ssh_access",
        [123],
        ["   "],
    ],
)
def test_rejects_invalid_manifest_capabilities(capabilities):
    manifest = _manifest(_tool("bad", capabilities=capabilities))

    with pytest.raises(ManifestError):
        toolkit_from_manifest(manifest)


def test_list_tools_for_capability_returns_matching_registered_tool_specs():
    registry = ToolRegistry()
    registry.register_toolkit(
        toolkit_from_manifest(
            _manifest(
                _tool("verify_ssh_access", capabilities=["ssh_access"]),
                _tool("record_host_note", capabilities=["host_notes"]),
                _tool("ssh_identity", capabilities=["ssh_access", "endpoint_identity"]),
            )
        )
    )

    assert [tool.name for tool in registry.list_tools_for_capability("SSH Access")] == [
        "ssh_identity",
        "verify_ssh_access",
    ]


def test_list_tools_for_capability_visible_only_uses_existing_visibility_and_status_semantics():
    registry = ToolRegistry()
    registry.register_toolkit(
        toolkit_from_manifest(
            _manifest(
                _tool("visible_tool", capabilities=["ssh_access"]),
                _tool("hidden_tool", capabilities=["ssh_access"], visibility="internal"),
                _tool("unregistered_tool", capabilities=["ssh_access"], status="generated"),
            )
        )
    )

    assert [tool.name for tool in registry.list_tools_for_capability("ssh_access")] == [
        "hidden_tool",
        "unregistered_tool",
        "visible_tool",
    ]
    assert [tool.name for tool in registry.list_tools_for_capability("ssh_access", visible_only=True)] == [
        "visible_tool"
    ]


def test_rejects_invalid_manifest():
    with pytest.raises(ManifestError):
        toolkit_from_manifest({"id": "bad"})
