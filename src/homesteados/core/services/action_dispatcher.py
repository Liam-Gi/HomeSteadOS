"""Central dispatcher for structured HomeSteadOS actions."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.core.results.action_result import ActionResult
from homesteados.core.services.lighting_service import LightingService
from homesteados.core.services.room_service import RoomService
from homesteados.core.services.system_service import SystemService


class ActionDispatcher:
    """Routes structured actions to the correct HomeSteadOS service."""

    def __init__(
        self,
        lighting_service: LightingService,
        room_service: RoomService,
        system_service: SystemService,
    ) -> None:
        self.lighting_service = lighting_service
        self.room_service = room_service
        self.system_service = system_service

    def execute(self, action: Action) -> ActionResult:
        """Execute an action through the appropriate service."""

        if action.target_type == ActionTargetType.DEVICE:
            return self._execute_device_action(action)

        if action.target_type == ActionTargetType.ROOM:
            return self._execute_room_action(action)

        if action.target_type == ActionTargetType.SYSTEM:
            return self._execute_system_action(action)

        return ActionResult.fail(
            message=f"Unsupported target type '{action.target_type.value}'.",
            reason="The ActionDispatcher does not recognise this target type.",
            action_id=action.id,
        )

    def _execute_device_action(self, action: Action) -> ActionResult:
        """Execute a device-targeted action."""

        if action.action_type in {ActionType.TURN_ON, ActionType.TURN_OFF}:
            return self.lighting_service.execute_action(action)

        return ActionResult.fail(
            message=f"Unsupported device action '{action.action_type.value}'.",
            reason="Only turn_on and turn_off device actions are currently supported.",
            action_id=action.id,
        )

    def _execute_room_action(self, action: Action) -> ActionResult:
        """Execute a room-targeted action."""

        if action.action_type == ActionType.TURN_ON:
            return self.room_service.turn_on_room_lights(
                room_id=action.target_id,
                requested_by=action.requested_by,
            )

        if action.action_type == ActionType.TURN_OFF:
            return self.room_service.turn_off_room_lights(
                room_id=action.target_id,
                requested_by=action.requested_by,
            )

        return ActionResult.fail(
            message=f"Unsupported room action '{action.action_type.value}'.",
            reason="Only turn_on and turn_off room actions are currently supported.",
            action_id=action.id,
        )

    def _execute_system_action(self, action: Action) -> ActionResult:
        """Execute a system-targeted action."""

        if action.action_type == ActionType.SET_STATE:
            mode = action.parameters.get("mode")

            if mode is None:
                return ActionResult.fail(
                    message="System mode action requires a 'mode' parameter.",
                    reason="No mode was provided in the action parameters.",
                    action_id=action.id,
                )

            return self.system_service.set_mode(
                mode=mode,
                updated_by=action.requested_by,
            )

        return ActionResult.fail(
            message=f"Unsupported system action '{action.action_type.value}'.",
            reason="Only set_state system actions are currently supported.",
            action_id=action.id,
        )