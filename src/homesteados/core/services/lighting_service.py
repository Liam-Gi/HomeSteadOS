"""Service for lighting-related operations."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionType, DeviceType
from homesteados.core.events.event import Event
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.results.action_result import ActionResult
from homesteados.core.safety.safety_engine import SafetyEngine


class LightingService:
    """Provides controlled lighting operations."""

    def __init__(
        self,
        device_registry: DeviceRegistry,
        adapter_registry: AdapterRegistry,
        safety_engine: SafetyEngine | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self.device_registry = device_registry
        self.adapter_registry = adapter_registry
        self.safety_engine = safety_engine or SafetyEngine()
        self.event_bus = event_bus

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

        self._publish_event(
            event_type=EventType.ACTION_REQUESTED,
            source="LightingService",
            payload={
                "action_id": action.id,
                "action_type": action.action_type.value,
                "target_id": action.target_id,
                "requested_by": action.requested_by,
            },
        )

        safety_result = self.safety_engine.review_action(action)

        if safety_result.requires_confirmation:
            self._publish_action_blocked(action, safety_result.reason)

            return ActionResult.confirmation_required(
                message="Action requires confirmation.",
                reason=safety_result.reason,
                action_id=action.id,
            )

        if not safety_result.allowed:
            self._publish_action_blocked(action, safety_result.reason)

            return ActionResult.fail(
                message="Action was blocked by the Safety Engine.",
                reason=safety_result.reason,
                action_id=action.id,
            )

        adapter = self.adapter_registry.get_adapter(device.adapter_id)

        if adapter is None:
            result = ActionResult.fail(
                message=f"No adapter registered for '{device.adapter_id}'.",
                reason=(
                    f"Device '{device.id}' requires adapter '{device.adapter_id}', "
                    "but no matching adapter is registered."
                ),
                action_id=action.id,
            )

            self._publish_action_failed(action, result.reason)
            return result

        previous_state = device.state
        result = adapter.execute_action(action, device)

        if result.success:
            self._publish_event(
                event_type=EventType.ACTION_COMPLETED,
                source="LightingService",
                payload={
                    "action_id": action.id,
                    "action_type": action.action_type.value,
                    "target_id": action.target_id,
                    "requested_by": action.requested_by,
                },
            )

            if device.state != previous_state:
                self._publish_event(
                    event_type=EventType.DEVICE_STATE_CHANGED,
                    source="LightingService",
                    payload={
                        "device_id": device.id,
                        "device_name": device.name,
                        "previous_state": previous_state.value,
                        "new_state": device.state.value,
                        "adapter_id": device.adapter_id,
                    },
                )

            return result

        self._publish_action_failed(action, result.reason)
        return result

    def _is_light(self, device: Device) -> bool:
        """Return True if the device is a light."""

        return device.device_type == DeviceType.LIGHT

    def _publish_action_blocked(
        self,
        action: Action,
        reason: str | None,
    ) -> None:
        """Publish an action blocked event."""

        self._publish_event(
            event_type=EventType.ACTION_BLOCKED,
            source="LightingService",
            payload={
                "action_id": action.id,
                "action_type": action.action_type.value,
                "target_id": action.target_id,
                "reason": reason,
            },
        )

    def _publish_action_failed(
        self,
        action: Action,
        reason: str | None,
    ) -> None:
        """Publish an action failed event."""

        self._publish_event(
            event_type=EventType.ACTION_FAILED,
            source="LightingService",
            payload={
                "action_id": action.id,
                "action_type": action.action_type.value,
                "target_id": action.target_id,
                "reason": reason,
            },
        )

    def _publish_event(
        self,
        event_type: EventType,
        source: str,
        payload: dict,
    ) -> None:
        """Publish an event if an event bus is configured."""

        if self.event_bus is None:
            return

        event = Event(
            event_type=event_type,
            source=source,
            payload=payload,
        )

        self.event_bus.publish(event)