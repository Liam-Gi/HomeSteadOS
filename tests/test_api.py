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
    assert "Unsupported action type" in response.json()["message"]

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