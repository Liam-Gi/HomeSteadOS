"""Tests for the simulated device adapter."""

from homesteados.adapters.simulated.simulated_device_adapter import (
    SimulatedDeviceAdapter,
)
from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionType, DeviceState, DeviceType


def create_light() -> Device:
    return Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        adapter_id="simulated",
        state=DeviceState.OFF,
    )


def test_simulated_adapter_turns_device_on():
    adapter = SimulatedDeviceAdapter()
    device = create_light()
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is True
    assert device.state == DeviceState.ON
    assert result.data["adapter_id"] == "simulated"


def test_simulated_adapter_turns_device_off():
    adapter = SimulatedDeviceAdapter()
    device = create_light()
    device.set_state(DeviceState.ON)
    action = Action(
        action_type=ActionType.TURN_OFF,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is True
    assert device.state == DeviceState.OFF


def test_simulated_adapter_rejects_offline_device():
    adapter = SimulatedDeviceAdapter()
    device = create_light()
    device.mark_offline()
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is False
    assert "offline" in result.message


def test_simulated_adapter_rejects_wrong_adapter_id():
    adapter = SimulatedDeviceAdapter()
    device = create_light()
    device.adapter_id = "home_assistant"
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id=device.id,
    )

    result = adapter.execute_action(action, device)

    assert result.success is False
    assert "not handled" in result.message