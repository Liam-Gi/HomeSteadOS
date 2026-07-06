"""Tests for the ActionDispatcher."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import (
    ActionTargetType,
    ActionType,
    DeviceState,
    SystemMode,
)
from homesteados.runtime import create_demo_runtime
from homesteados.core.domain.enums import ActionRisk


def test_action_dispatcher_turns_on_device_light():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="test",
    )

    result = runtime.action_dispatcher.execute(action)
    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.ON


def test_action_dispatcher_turns_off_device_light():
    runtime = create_demo_runtime()
    runtime.lighting_service.turn_on_light("light.office.ceiling")

    action = Action(
        action_type=ActionType.TURN_OFF,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="test",
    )

    result = runtime.action_dispatcher.execute(action)
    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.OFF


def test_action_dispatcher_turns_on_room_lights():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="office",
        target_type=ActionTargetType.ROOM,
        requested_by="test",
    )

    result = runtime.action_dispatcher.execute(action)
    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.ON


def test_action_dispatcher_sets_system_mode():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.SET_STATE,
        target_id="system",
        target_type=ActionTargetType.SYSTEM,
        requested_by="test",
        parameters={
            "mode": "night",
        },
    )

    result = runtime.action_dispatcher.execute(action)

    assert result.success is True
    assert runtime.system_service.get_mode() == SystemMode.NIGHT


def test_action_dispatcher_rejects_unsupported_device_action():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.SET_BRIGHTNESS,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="test",
    )

    result = runtime.action_dispatcher.execute(action)

    assert result.success is False
    assert "Unsupported device action" in result.message

def test_action_dispatcher_preserves_high_risk_device_action():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="api",
        risk_level=ActionRisk.HIGH,
    )

    result = runtime.action_dispatcher.execute(action)

    assert result.success is False
    assert result.requires_confirmation is True
    assert result.action_id == action.id


def test_action_dispatcher_preserves_requires_confirmation_flag():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="api",
        requires_confirmation=True,
    )

    result = runtime.action_dispatcher.execute(action)

    assert result.success is False
    assert result.requires_confirmation is True
    assert result.action_id == action.id


def test_action_dispatcher_preserves_ai_request_in_away_mode():
    runtime = create_demo_runtime()
    runtime.system_service.set_mode("away", updated_by="test")

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="ai",
    )

    result = runtime.action_dispatcher.execute(action)

    assert result.success is False
    assert result.requires_confirmation is True
    assert result.action_id == action.id