from seed_runtime.events import EventLedger, SQLiteEventLedger


def test_append_records_reality_in_order():
    ledger = EventLedger()

    ledger.append("user.message")
    ledger.append("goal.created")

    assert len(ledger.list()) == 2
    assert ledger.list()[0].kind == "user.message"
    assert ledger.list()[1].kind == "goal.created"


def test_get_returns_appended_event_by_id():
    ledger = EventLedger()

    event = ledger.append("user.message")

    assert ledger.get(event.id) == event


def test_sqlite_execution_authorization_events_persist_secret_free_metadata(tmp_path):
    db_path = tmp_path / "events.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    try:
        event = ledger.append(
            "execution_authorization.granted",
            "ws",
            {
                "execution_authorization": {
                    "id": "auth_1",
                    "execution_proposal_id": "eprop_1",
                    "action_plan_id": "plan_1",
                    "tool_name": "restart_container",
                    "arguments_fingerprint": "abc123",
                    "granted_by": "operator@example.com",
                    "expires_at": "2026-06-03T00:05:00+00:00",
                    "interactive_prompt": True,
                    "ssh_agent": "SSH_AUTH_SOCK",
                    "sudo_timestamp": "host-sudo-cache",
                    "external_vault_token_ref": "vault://seed/jit/1",
                    "secret_seen_by_seed": False,
                }
            },
        )
        assert ledger.get(event.id) is not None
        assert [stored.kind for stored in ledger.list_events("ws")] == [
            "execution_authorization.granted"
        ]
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(str(db_path))
    try:
        events = reopened.list_events("ws")
        assert [stored.kind for stored in events] == [
            "execution_authorization.granted"
        ]
        payload = events[0].payload["execution_authorization"]
        assert payload["id"] == "auth_1"
        assert payload["execution_proposal_id"] == "eprop_1"
        assert "password" not in payload
        assert "passphrase" not in payload
        assert "token" not in payload
        assert "private_key" not in payload
    finally:
        reopened.close()


def test_event_ledger_rejects_secret_fields_in_payloads():
    ledger = EventLedger()

    for field in ("password", "passphrase", "token", "private_key"):
        try:
            ledger.append("tool.call_requested", "ws", {field: "not-accepted"})
        except ValueError as exc:
            assert "secret field" in str(exc)
        else:
            raise AssertionError(f"{field} must be rejected")


def test_execution_authorization_event_rejects_non_grant_metadata():
    ledger = EventLedger()

    try:
        ledger.append(
            "execution_authorization.granted",
            "ws",
            {
                "execution_authorization": {
                    "id": "auth_1",
                    "execution_proposal_id": "eprop_1",
                    "action_plan_id": "plan_1",
                    "tool_name": "restart_container",
                    "arguments_fingerprint": "sha256:abc123",
                    "granted_by": "operator@example.com",
                    "expires_at": "2026-06-03T00:05:00+00:00",
                    "credential_grant_id": "legacy-grant",
                    "secret_seen_by_seed": False,
                }
            },
        )
    except ValueError as exc:
        assert "only store secret-free grant metadata" in str(exc)
    else:
        raise AssertionError("execution authorization must reject legacy metadata")
