"""Tests for the HomeSteadOS HTTP API."""

from fastapi.testclient import TestClient

from homesteados.interfaces.api.app import create_app
from homesteados.runtime import create_demo_runtime


def create_test_client() -> TestClient:
    app = create_app(create_demo_runtime())
    return TestClient(app)


def test_api_returns_system_status():
    client = create_test_client()

    response = client.get("/system/status")

    assert response.status_code == 200
    assert response.json()["status"] == "running"
    assert response.json()["device_count"] == 3


def test_api_lists_devices():
    client = create_test_client()

    response = client.get("/devices")

    assert response.status_code == 200

    devices = response.json()
    device_ids = [device["id"] for device in devices]

    assert "light.office.ceiling" in device_ids


def test_api_returns_single_device():
    client = create_test_client()

    response = client.get("/devices/light.office.ceiling")

    assert response.status_code == 200
    assert response.json()["name"] == "Office Ceiling Light"


def test_api_can_turn_on_light():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "requested_by": "api",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "on"


def test_api_can_return_events_after_action():
    client = create_test_client()

    client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "requested_by": "api",
            "parameters": {},
        },
    )

    response = client.get("/events")

    assert response.status_code == 200

    event_types = [event["event_type"] for event in response.json()]

    assert "action_requested" in event_types
    assert "action_completed" in event_types
    assert "device_state_changed" in event_types


def test_api_rejects_unknown_action_type():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "dance",
            "target_id": "light.office.ceiling",
            "requested_by": "api",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Invalid action request" in response.json()["message"]

def test_api_lists_rooms():
    client = create_test_client()

    response = client.get("/rooms")

    assert response.status_code == 200

    room_ids = [
        room["id"]
        for room in response.json()
    ]

    assert "office" in room_ids
    assert "kitchen" in room_ids
    assert "bedroom" in room_ids


def test_api_returns_single_room():
    client = create_test_client()

    response = client.get("/rooms/office")

    assert response.status_code == 200
    assert response.json()["name"] == "Office"


def test_api_returns_system_mode():
    client = create_test_client()

    response = client.get("/system/mode")

    assert response.status_code == 200
    assert response.json()["mode"] == "home"


def test_api_can_set_system_mode():
    client = create_test_client()

    response = client.post(
        "/system/mode",
        json={
            "mode": "away",
            "updated_by": "test",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    mode_response = client.get("/system/mode")

    assert mode_response.json()["mode"] == "away"


def test_api_rejects_unknown_system_mode():
    client = create_test_client()

    response = client.post(
        "/system/mode",
        json={
            "mode": "invalid_mode",
            "updated_by": "test",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False

def test_api_lists_devices_in_room():
    client = create_test_client()

    response = client.get("/rooms/office/devices")

    assert response.status_code == 200

    device_ids = [
        device["id"]
        for device in response.json()
    ]

    assert "light.office.ceiling" in device_ids

def test_api_can_turn_on_room_lights():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "office",
            "target_type": "room",
            "requested_by": "api",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "on"


def test_api_can_set_system_mode_through_action_dispatcher():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "set_state",
            "target_id": "system",
            "target_type": "system",
            "requested_by": "api",
            "parameters": {
                "mode": "night",
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    mode_response = client.get("/system/mode")

    assert mode_response.json()["mode"] == "night"


def test_api_rejects_invalid_action_request():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "not_real",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Invalid action request" in response.json()["message"]

def test_api_returns_system_health():
    client = create_test_client()

    response = client.get("/system/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    check_names = [
        check["name"]
        for check in response.json()["checks"]
    ]

    assert "adapters" in check_names
    assert "devices" in check_names
    assert "rooms" in check_names

def test_api_high_risk_device_action_requires_confirmation():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "risk_level": "high",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["requires_confirmation"] is True


def test_api_stores_high_risk_action_as_pending():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "risk_level": "high",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["requires_confirmation"] is True

    pending_response = client.get("/actions/pending")

    assert pending_response.status_code == 200
    assert len(pending_response.json()) == 1


def test_api_can_confirm_pending_action():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "risk_level": "high",
            "parameters": {},
        },
    )

    action_id = response.json()["action_id"]

    confirm_response = client.post(f"/actions/{action_id}/confirm")

    assert confirm_response.status_code == 200
    assert confirm_response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "on"


def test_api_can_cancel_pending_action():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "risk_level": "high",
            "parameters": {},
        },
    )

    action_id = response.json()["action_id"]

    cancel_response = client.post(f"/actions/{action_id}/cancel")

    assert cancel_response.status_code == 200
    assert cancel_response.json()["success"] is True

    pending_response = client.get("/actions/pending")

    assert pending_response.json() == []

def test_api_lists_automation_rules():
    client = create_test_client()

    response = client.get("/automations")

    assert response.status_code == 200

    rule_ids = [
        rule["id"]
        for rule in response.json()
    ]

    assert "night-turn-off-kitchen" in rule_ids


def test_api_can_disable_automation_rule():
    client = create_test_client()

    response = client.post("/automations/night-turn-off-kitchen/disable")

    assert response.status_code == 200
    assert response.json()["success"] is True

    rules_response = client.get("/automations")
    rule = rules_response.json()[0]

    assert rule["id"] == "night-turn-off-kitchen"
    assert rule["enabled"] is False


def test_api_night_mode_triggers_automation():
    client = create_test_client()

    client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.kitchen.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "parameters": {},
        },
    )

    client.post(
        "/system/mode",
        json={
            "mode": "night",
            "updated_by": "test",
        },
    )

    device_response = client.get("/devices/light.kitchen.ceiling")

    assert device_response.status_code == 200
    assert device_response.json()["state"] == "off"

def test_api_ai_action_requires_confirmation_in_away_mode():
    client = create_test_client()

    client.post(
        "/system/mode",
        json={
            "mode": "away",
            "updated_by": "test",
        },
    )

    response = client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "ai",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["requires_confirmation"] is True

def test_api_lists_scenes():
    client = create_test_client()

    response = client.get("/scenes")

    assert response.status_code == 200

    scene_ids = [
        scene["id"]
        for scene in response.json()
    ]

    assert "good-night" in scene_ids


def test_api_can_run_good_night_scene():
    client = create_test_client()

    client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "parameters": {},
        },
    )

    response = client.post("/scenes/good-night/run")

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "off"

def test_api_can_run_scene_through_action_endpoint():
    client = create_test_client()

    client.post(
        "/actions",
        json={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "target_type": "device",
            "requested_by": "api",
            "parameters": {},
        },
    )

    response = client.post(
        "/actions",
        json={
            "action_type": "run_scene",
            "target_id": "good-night",
            "target_type": "scene",
            "requested_by": "api",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "off"

def test_api_can_execute_text_command():
    client = create_test_client()

    response = client.post(
        "/commands/text",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "on"


def test_api_can_run_scene_from_text_command():
    client = create_test_client()

    client.post(
        "/commands/text",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )

    response = client.post(
        "/commands/text",
        json={
            "command": "run good night",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "off"

def test_api_can_preview_text_command():
    client = create_test_client()

    response = client.post(
        "/commands/text/preview",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["action_type"] == "turn_on"
    assert response.json()["target_type"] == "room"
    assert response.json()["target_id"] == "office"
    assert "Office" in response.json()["description"]


def test_api_preview_does_not_execute_command():
    client = create_test_client()

    response = client.post(
        "/commands/text/preview",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "off"


def test_api_preview_unknown_command_fails():
    client = create_test_client()

    response = client.post(
        "/commands/text/preview",
        json={
            "command": "make me a coffee",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False

def test_api_records_text_command_execution_history():
    client = create_test_client()

    client.post(
        "/commands/text",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )

    response = client.get("/commands/history")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["command"] == "turn on office light"
    assert response.json()[0]["mode"] == "execute"
    assert response.json()[0]["success"] is True


def test_api_records_text_command_preview_history():
    client = create_test_client()

    client.post(
        "/commands/text/preview",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )

    response = client.get("/commands/history")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["command"] == "turn on office light"
    assert response.json()[0]["mode"] == "preview"
    assert response.json()[0]["success"] is True

def test_api_text_command_failure_returns_suggestions():
    client = create_test_client()

    response = client.post(
        "/commands/text",
        json={
            "command": "make office bright",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "suggestions" in response.json()["data"]
    assert "turn on office light" in response.json()["data"]["suggestions"]


def test_api_preview_failure_returns_suggestions():
    client = create_test_client()

    response = client.post(
        "/commands/text/preview",
        json={
            "command": "make office bright",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "turn on office light" in response.json()["suggestions"]

def test_api_returns_no_insights_without_history():
    client = create_test_client()

    response = client.get("/insights")

    assert response.status_code == 200
    assert response.json() == []


def test_api_returns_repeated_command_insight():
    client = create_test_client()

    for _ in range(3):
        client.post(
            "/commands/text",
            json={
                "command": "turn on office light",
                "requested_by": "api",
            },
        )

    response = client.get("/insights")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["insight_type"] == "repeated_command"
    assert response.json()[0]["data"]["command"] == "turn on office light"

def test_api_lists_shortcuts():
    client = create_test_client()

    response = client.get("/shortcuts")

    assert response.status_code == 200

    shortcut_ids = [
        shortcut["id"]
        for shortcut in response.json()
    ]

    assert "bedtime" in shortcut_ids
    assert "office-on" in shortcut_ids


def test_api_can_run_shortcut():
    client = create_test_client()

    response = client.post("/shortcuts/office-on/run")

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "on"

def test_api_can_run_shortcut_through_action_endpoint():
    client = create_test_client()

    response = client.post(
        "/actions",
        json={
            "action_type": "run_shortcut",
            "target_id": "office-on",
            "target_type": "shortcut",
            "requested_by": "api",
            "parameters": {},
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    device_response = client.get("/devices/light.office.ceiling")

    assert device_response.json()["state"] == "on"


def test_api_can_preview_shortcut_text_command():
    client = create_test_client()

    response = client.post(
        "/commands/text/preview",
        json={
            "command": "run shortcut office-on",
            "requested_by": "api",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["action_type"] == "run_shortcut"
    assert response.json()["target_type"] == "shortcut"
    assert response.json()["target_id"] == "office-on"

def test_api_night_mode_runs_shortcut_automation():
    client = create_test_client()

    client.post(
        "/commands/text",
        json={
            "command": "turn on office light",
            "requested_by": "api",
        },
    )
    client.post(
        "/commands/text",
        json={
            "command": "turn on kitchen light",
            "requested_by": "api",
        },
    )
    client.post(
        "/commands/text",
        json={
            "command": "turn on bedroom light",
            "requested_by": "api",
        },
    )

    response = client.post(
        "/system/mode",
        json={
            "mode": "night",
            "updated_by": "api",
        },
    )

    assert response.status_code == 200

    office_response = client.get("/devices/light.office.ceiling")
    kitchen_response = client.get("/devices/light.kitchen.ceiling")
    bedroom_response = client.get("/devices/light.bedroom.lamp")

    assert office_response.json()["state"] == "off"
    assert kitchen_response.json()["state"] == "off"
    assert bedroom_response.json()["state"] == "off"