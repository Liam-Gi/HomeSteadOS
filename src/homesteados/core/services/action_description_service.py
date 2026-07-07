"""Service for describing structured HomeSteadOS actions."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.registry.scene_registry import SceneRegistry
from homesteados.core.registry.shortcut_registry import ShortcutRegistry


class ActionDescriptionService:
    """Creates human-readable descriptions for actions."""

    def __init__(
            self,
            device_registry: DeviceRegistry,
            room_registry: RoomRegistry,
            scene_registry: SceneRegistry,
            shortcut_registry: ShortcutRegistry | None = None,
    ) -> None:
        self.device_registry = device_registry
        self.room_registry = room_registry
        self.scene_registry = scene_registry
        self.shortcut_registry = shortcut_registry

    def describe_action(self, action: Action) -> str:
        """Return a human-readable description of an action."""

        if action.target_type == ActionTargetType.DEVICE:
            return self._describe_device_action(action)

        if action.target_type == ActionTargetType.SHORTCUT:
            return self._describe_shortcut_action(action)

        if action.target_type == ActionTargetType.ROOM:
            return self._describe_room_action(action)

        if action.target_type == ActionTargetType.SYSTEM:
            return self._describe_system_action(action)

        if action.target_type == ActionTargetType.SCENE:
            return self._describe_scene_action(action)

        return (
            f"Run action '{action.action_type.value}' "
            f"on target '{action.target_id}'."
        )

    def _describe_device_action(self, action: Action) -> str:
        """Describe a device action."""

        device = self.device_registry.get_device_by_id(action.target_id)
        device_name = device.name if device is not None else action.target_id

        if action.action_type == ActionType.TURN_ON:
            return f"Turn on device '{device_name}'."

        if action.action_type == ActionType.TURN_OFF:
            return f"Turn off device '{device_name}'."

        return (
            f"Run action '{action.action_type.value}' "
            f"on device '{device_name}'."
        )

    def _describe_shortcut_action(self, action: Action) -> str:
        """Describe a shortcut action."""

        shortcut_name = action.target_id

        if self.shortcut_registry is not None:
            shortcut = self.shortcut_registry.get_shortcut_by_id(action.target_id)
            if shortcut is not None:
                shortcut_name = shortcut.name

        if action.action_type == ActionType.RUN_SHORTCUT:
            return f"Run shortcut '{shortcut_name}'."

        return (
            f"Run action '{action.action_type.value}' "
            f"on shortcut '{shortcut_name}'."
        )

    def _describe_room_action(self, action: Action) -> str:
        """Describe a room action."""

        room = self.room_registry.get_room_by_id(action.target_id)
        room_name = room.name if room is not None else action.target_id

        if action.action_type == ActionType.TURN_ON:
            return f"Turn on all supported devices in room '{room_name}'."

        if action.action_type == ActionType.TURN_OFF:
            return f"Turn off all supported devices in room '{room_name}'."

        return (
            f"Run action '{action.action_type.value}' "
            f"in room '{room_name}'."
        )

    def _describe_system_action(self, action: Action) -> str:
        """Describe a system action."""

        if action.action_type == ActionType.SET_STATE:
            mode = action.parameters.get("mode", "unknown")
            return f"Set system mode to '{mode}'."

        return f"Run system action '{action.action_type.value}'."

    def _describe_scene_action(self, action: Action) -> str:
        """Describe a scene action."""

        scene = self.scene_registry.get_scene_by_id(action.target_id)
        scene_name = scene.name if scene is not None else action.target_id

        if action.action_type == ActionType.RUN_SCENE:
            return f"Run scene '{scene_name}'."

        return (
            f"Run action '{action.action_type.value}' "
            f"on scene '{scene_name}'."
        )