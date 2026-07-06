"""Tests for automation service behaviour."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.automation_rule import AutomationRule
from homesteados.core.domain.enums import ActionTargetType, ActionType, DeviceState
from homesteados.core.events.event import Event
from homesteados.core.events.event_types import EventType
from homesteados.runtime import create_demo_runtime


def test_automation_rule_matches_event_payload():
    rule = AutomationRule(
        id="test-rule",
        name="Test rule",
        trigger_event_type=EventType.SYSTEM_MODE_CHANGED,
        trigger_payload_matches={
            "new_mode": "night",
        },
        action=Action(
            action_type=ActionType.TURN_OFF,
            target_id="kitchen",
            target_type=ActionTargetType.ROOM,
        ),
    )

    event = Event(
        event_type=EventType.SYSTEM_MODE_CHANGED,
        source="test",
        payload={
            "previous_mode": "home",
            "new_mode": "night",
        },
    )

    assert rule.matches_event(event) is True


def test_automation_rule_does_not_match_wrong_payload():
    rule = AutomationRule(
        id="test-rule",
        name="Test rule",
        trigger_event_type=EventType.SYSTEM_MODE_CHANGED,
        trigger_payload_matches={
            "new_mode": "night",
        },
        action=Action(
            action_type=ActionType.TURN_OFF,
            target_id="kitchen",
            target_type=ActionTargetType.ROOM,
        ),
    )

    event = Event(
        event_type=EventType.SYSTEM_MODE_CHANGED,
        source="test",
        payload={
            "previous_mode": "home",
            "new_mode": "away",
        },
    )

    assert rule.matches_event(event) is False


def test_night_mode_automation_turns_off_kitchen_light():
    runtime = create_demo_runtime()

    runtime.lighting_service.turn_on_light(
        "light.kitchen.ceiling",
        requested_by="test",
    )

    runtime.system_service.set_mode(
        mode="night",
        updated_by="test",
    )

    kitchen_light = runtime.device_registry.get_device_by_id("light.kitchen.ceiling")

    assert kitchen_light is not None
    assert kitchen_light.state == DeviceState.OFF


def test_disabled_automation_rule_does_not_run():
    runtime = create_demo_runtime()

    runtime.lighting_service.turn_on_light(
        "light.kitchen.ceiling",
        requested_by="test",
    )

    runtime.automation_service.disable_rule("night-turn-off-kitchen")

    runtime.system_service.set_mode(
        mode="night",
        updated_by="test",
    )

    kitchen_light = runtime.device_registry.get_device_by_id("light.kitchen.ceiling")

    assert kitchen_light is not None
    assert kitchen_light.state == DeviceState.ON


def test_automation_trigger_publishes_event():
    runtime = create_demo_runtime()

    runtime.lighting_service.turn_on_light(
        "light.kitchen.ceiling",
        requested_by="test",
    )

    runtime.system_service.set_mode(
        mode="night",
        updated_by="test",
    )

    event_types = [
        event.event_type
        for event in runtime.event_bus.list_published_events()
    ]

    assert EventType.AUTOMATION_TRIGGERED in event_types