"""Service for lighting-related operations."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionType, DeviceType
from homesteados.core.ports.device_adapter import DeviceAdapter
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.results.action_result import ActionResult
from homesteados.core.safety.safety_engine import SafetyEngine


class LightingService:
    """Provides controlled lighting operations."""

    def __init__(
        self,
        device_registry: DeviceRegistry,
        device_adapter: DeviceAdapter,
        safety_engine: SafetyEngine | None = None,
    ) -> None:
        self.device_registry = device_registry
        self.device_adapter = device_adapter
        self.safety_engine = safety_engine or SafetyEngine()

    def turn_on_light(
        self,
        device_id: str,
        requested_by: str = "system",
    ) -> ActionResult:
        """Turn on a light by device ID."""

        return self._request_light_action(
            device_id=device_id,
            action_type=ActionType.TURN_ON,
            requested_by=requested_by,
        )

    def turn_off_light(
        self,
        device_id: str,
        requested_by: str = "system",
    ) -> ActionResult:
        """Turn off a light by device ID."""

        return self._request_light_action(
            device_id=device_id,
            action_type=ActionType.TURN_OFF,
            requested_by=requested_by,
        )

    def _request_light_action(
        self,
        device_id: str,
        action_type: ActionType,
        requested_by: str,
    ) -> ActionResult:
        """Validate, review, and execute a lighting action."""

        device = self.device_registry.get_device_by_id(device_id)

        if device is None:
            return ActionResult.fail(
                message=f"Device '{device_id}' was not found.",
                reason="No registered device matched the provided device ID.",
            )

        if not self._is_light(device):
            return ActionResult.fail(
                message=f"Device '{device_id}' is not a light.",
                reason="LightingService can only control devices of type light.",
            )

        action = Action(
            action_type=action_type,
            target_id=device_id,
            requested_by=requested_by,
        )

        safety_result = self.safety_engine.review_action(action)

        if safety_result.requires_confirmation:
            return ActionResult.confirmation_required(
                message="Action requires confirmation.",
                reason=safety_result.reason,
                action_id=action.id,
            )

        if not safety_result.allowed:
            return ActionResult.fail(
                message="Action was blocked by the Safety Engine.",
                reason=safety_result.reason,
                action_id=action.id,
            )

        return self.device_adapter.execute_action(action, device)

    def _is_light(self, device: Device) -> bool:
        """Return True if the device is a light."""

        return device.device_type == DeviceType.LIGHT

        return device.device_type == DeviceType.LIGHT