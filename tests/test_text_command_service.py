"""Tests for text command service behaviour."""

from homesteados.core.domain.enums import ActionTargetType, ActionType, DeviceState
from homesteados.runtime import create_demo_runtime


def test_text_command_parses_room_light_command():
    runtime = create_demo_runtime()

    result = runtime.text_command_service.parse_text(
        "turn on office light",
        requested_by="test",
    )

    assert result.success is True
    assert result.action is not None
    assert result.action.action_type == ActionType.TURN_ON
    assert result.action.target_type == ActionTargetType.ROOM
    assert result.action.target_id == "office"


def test_text_command_executes_light_command():
    runtime = create_demo_runtime()

    result = runtime.text_command_service.execute_text(
        "turn on office light",
        requested_by="test",
    )

    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.ON


def test_text_command_parses_scene_command():
    runtime = create_demo_runtime()

    result = runtime.text_command_service.parse_text(
        "run good night",
        requested_by="test",
    )

    assert result.success is True
    assert result.action is not None
    assert result.action.action_type == ActionType.RUN_SCENE
    assert result.action.target_type == ActionTargetType.SCENE
    assert result.action.target_id == "good-night"


def test_text_command_runs_good_night_scene():
    runtime = create_demo_runtime()

    runtime.text_command_service.execute_text(
        "turn on office light",
        requested_by="test",
    )
    runtime.text_command_service.execute_text(
        "turn on kitchen light",
        requested_by="test",
    )
    runtime.text_command_service.execute_text(
        "turn on bedroom light",
        requested_by="test",
    )

    result = runtime.text_command_service.execute_text(
        "run good night",
        requested_by="test",
    )

    office_light = runtime.device_registry.get_device_by_id("light.office.ceiling")
    kitchen_light = runtime.device_registry.get_device_by_id("light.kitchen.ceiling")
    bedroom_light = runtime.device_registry.get_device_by_id("light.bedroom.lamp")

    assert result.success is True
    assert office_light is not None
    assert kitchen_light is not None
    assert bedroom_light is not None
    assert office_light.state == DeviceState.OFF
    assert kitchen_light.state == DeviceState.OFF
    assert bedroom_light.state == DeviceState.OFF


def test_text_command_sets_system_mode():
    runtime = create_demo_runtime()

    result = runtime.text_command_service.execute_text(
        "set mode away",
        requested_by="test",
    )

    assert result.success is True
    assert runtime.system_state.mode.value == "away"


def test_text_command_unknown_command_fails():
    runtime = create_demo_runtime()

    result = runtime.text_command_service.execute_text(
        "make me a coffee",
        requested_by="test",
    )

    assert result.success is False
    assert "could not understand" in result.message.lower()