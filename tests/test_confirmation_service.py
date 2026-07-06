"""Tests for confirmation service behaviour."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionRisk, ActionTargetType, ActionType, DeviceState
from homesteados.runtime import create_demo_runtime


def test_high_risk_action_is_stored_as_pending():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="test",
        risk_level=ActionRisk.HIGH,
    )

    result = runtime.action_dispatcher.execute(action)

    assert result.requires_confirmation is True

    pending_action = runtime.pending_action_store.get(action.id)

    assert pending_action == action


def test_confirm_pending_action_executes_it():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="test",
        risk_level=ActionRisk.HIGH,
    )

    runtime.action_dispatcher.execute(action)

    result = runtime.confirmation_service.confirm_action(action.id)

    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.ON
    assert runtime.pending_action_store.get(action.id) is None


def test_cancel_pending_action_removes_it():
    runtime = create_demo_runtime()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        target_type=ActionTargetType.DEVICE,
        requested_by="test",
        risk_level=ActionRisk.HIGH,
    )

    runtime.action_dispatcher.execute(action)

    result = runtime.confirmation_service.cancel_action(action.id)

    assert result.success is True
    assert runtime.pending_action_store.get(action.id) is None


def test_confirm_unknown_action_fails():
    runtime = create_demo_runtime()

    result = runtime.confirmation_service.confirm_action("missing")

    assert result.success is False
    assert "not found" in result.message