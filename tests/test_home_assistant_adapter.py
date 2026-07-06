"""Tests for the Home Assistant adapter."""

import requests

from homesteados.adapters.home_assistant.home_assistant_adapter import (
    HomeAssistantAdapter,
)
from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionType, DeviceType


class FakeResponse:
    """Fake HTTP response for adapter tests."""

    def __init__(self, should_raise: bool = False) -> None:
        self.should_raise = should_raise

    def raise_for_status(self) -> None:
        """Raise an HTTP error if configured to do so."""

        if self.should_raise:
            raise requests.RequestException("Home Assistant error")


class FakeHttpClient:
    """Fake HTTP client for adapter tests."""

    def __init__(self, should_raise: bool = False) -> None:
        self.should_raise = should_raise
        self.calls: list[dict] = []

    def post(self, url: str, headers: dict, json: dict, timeout: int) -> FakeResponse:
        """Record fake POST calls."""

        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "json": json,
                "timeout": timeout,
            }
        )

        return FakeResponse(should_raise=self.should_raise)


def create_home_assistant_light() -> Device:
    return Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        adapter_id="home_assistant",
        attributes={
            "home_assistant_entity_id": "light.office_ceiling",
        },
    )


def test_home_assistant_adapter_sends_turn_on_service_call():
    fake_client = FakeHttpClient()
    adapter = HomeAssistantAdapter(
        base_url="http://homeassistant.local:8123",
        access_token="test-token",
        http_client=fake_client,
    )
    device = create_home_assistant_light()
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is True
    assert len(fake_client.calls) == 1
    assert fake_client.calls[0]["url"] == (
        "http://homeassistant.local:8123/api/services/homeassistant/turn_on"
    )
    assert fake_client.calls[0]["json"] == {
        "entity_id": "light.office_ceiling",
    }
    assert fake_client.calls[0]["headers"]["Authorization"] == "Bearer test-token"


def test_home_assistant_adapter_sends_turn_off_service_call():
    fake_client = FakeHttpClient()
    adapter = HomeAssistantAdapter(
        base_url="http://homeassistant.local:8123",
        access_token="test-token",
        http_client=fake_client,
    )
    device = create_home_assistant_light()
    action = Action(
        action_type=ActionType.TURN_OFF,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is True
    assert fake_client.calls[0]["url"].endswith("/api/services/homeassistant/turn_off")


def test_home_assistant_adapter_rejects_wrong_adapter_id():
    fake_client = FakeHttpClient()
    adapter = HomeAssistantAdapter(
        base_url="http://homeassistant.local:8123",
        access_token="test-token",
        http_client=fake_client,
    )
    device = create_home_assistant_light()
    device.adapter_id = "simulated"

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is False
    assert "not handled" in result.message
    assert fake_client.calls == []


def test_home_assistant_adapter_requires_entity_id():
    fake_client = FakeHttpClient()
    adapter = HomeAssistantAdapter(
        base_url="http://homeassistant.local:8123",
        access_token="test-token",
        http_client=fake_client,
    )
    device = create_home_assistant_light()
    device.attributes = {}

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is False
    assert "missing a Home Assistant entity ID" in result.message
    assert fake_client.calls == []


def test_home_assistant_adapter_handles_http_failure():
    fake_client = FakeHttpClient(should_raise=True)
    adapter = HomeAssistantAdapter(
        base_url="http://homeassistant.local:8123",
        access_token="test-token",
        http_client=fake_client,
    )
    device = create_home_assistant_light()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is False
    assert "service call failed" in result.message