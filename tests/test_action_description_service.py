"""Tests for action description service behaviour."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.runtime import create_demo_runtime


def test_describes_room_turn_on_action():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="office",
        target_type=ActionTargetType.ROOM,
        requested_by="test",
    )

    description = runtime.action_description_service.describe_action(action)

    assert "Turn on" in description
    assert "Office" in description


def test_describes_scene_action():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.RUN_SCENE,
        target_id="good-night",
        target_type=ActionTargetType.SCENE,
        requested_by="test",
    )

    description = runtime.action_description_service.describe_action(action)

    assert "Run scene" in description
    assert "Good Night" in description


def test_describes_system_mode_action():
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

    description = runtime.action_description_service.describe_action(action)

    assert "Set system mode" in description
    assert "night" in description