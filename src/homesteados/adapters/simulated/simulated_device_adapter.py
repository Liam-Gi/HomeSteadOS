"""Simulated adapter for testing devices without hardware."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionType, DeviceState
from homesteados.core.results.action_result import ActionResult


class SimulatedDeviceAdapter:
    """Executes actions against in-memory simulated devices."""

    adapter_id = "simulated"

    def execute_action(self, action: Action, device: Device) -> ActionResult:
        """Execute an action against a simulated device."""

        if device.adapter_id != self.adapter_id:
            return ActionResult.fail(
                message=f"Device '{device.id}' is not handled by the simulated adapter.",
                reason=(
                    f"Device adapter_id is '{device.adapter_id}', "
                    f"but this adapter handles '{self.adapter_id}'."
                ),
                action_id=action.id,
            )

        if not device.online:
            return ActionResult.fail(
                message=f"Device '{device.id}' is offline.",
                reason="Simulated adapter cannot execute actions on offline devices.",
                action_id=action.id,
            )

        if action.action_type == ActionType.TURN_ON:
            device.set_state(DeviceState.ON)
            return ActionResult.ok(
                message=f"{device.name} turned on.",
                action_id=action.id,
                data={
                    "device_id": device.id,
                    "state": device.state.value,
                    "adapter_id": self.adapter_id,
                },
            )

        if action.action_type == ActionType.TURN_OFF:
            device.set_state(DeviceState.OFF)
            return ActionResult.ok(
                message=f"{device.name} turned off.",
                action_id=action.id,
                data={
                    "device_id": device.id,
                    "state": device.state.value,
                    "adapter_id": self.adapter_id,
                },
            )

        return ActionResult.fail(
            message=f"Action '{action.action_type.value}' is not supported.",
            reason="Simulated adapter only supports basic turn on and turn off actions.",
            action_id=action.id,
        )