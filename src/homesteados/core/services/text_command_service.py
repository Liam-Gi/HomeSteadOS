"""Service for parsing text commands into structured HomeSteadOS actions."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.registry.scene_registry import SceneRegistry
from homesteados.core.results.action_result import ActionResult
from homesteados.core.results.text_command_result import TextCommandParseResult
from homesteados.core.services.command_suggestion_service import CommandSuggestionService


class TextCommandService:
    """Parses simple text commands and executes them as structured Actions."""

    def __init__(
            self,
            device_registry: DeviceRegistry,
            room_registry: RoomRegistry,
            scene_registry: SceneRegistry,
            action_executor,
            command_suggestion_service: CommandSuggestionService | None = None,
    ) -> None:
        self.device_registry = device_registry
        self.room_registry = room_registry
        self.scene_registry = scene_registry
        self.action_executor = action_executor
        self.command_suggestion_service = command_suggestion_service

    def parse_text(
        self,
        command: str,
        requested_by: str = "text",
    ) -> TextCommandParseResult:
        """Parse a text command into an Action."""

        normalised_command = self._normalise(command)

        if not normalised_command:
            return self._fail_with_suggestions(
                message="Please enter a command.",
                command=command,
            )

        if normalised_command.startswith("set mode "):
            mode = normalised_command.replace("set mode ", "", 1).strip()
            return self._parse_set_mode(mode, requested_by=requested_by)

        if normalised_command.startswith("run scene "):
            scene_query = normalised_command.replace("run scene ", "", 1).strip()
            return self._parse_run_scene(scene_query, requested_by=requested_by)

        if normalised_command.startswith("run "):
            scene_query = normalised_command.replace("run ", "", 1).strip()
            return self._parse_run_scene(scene_query, requested_by=requested_by)

        if normalised_command.startswith("turn on "):
            target_query = normalised_command.replace("turn on ", "", 1).strip()
            return self._parse_power_action(
                target_query=target_query,
                action_type=ActionType.TURN_ON,
                requested_by=requested_by,
            )

        if normalised_command.startswith("turn off "):
            target_query = normalised_command.replace("turn off ", "", 1).strip()
            return self._parse_power_action(
                target_query=target_query,
                action_type=ActionType.TURN_OFF,
                requested_by=requested_by,
            )

        return self._fail_with_suggestions(
            message=f"Could not understand text command '{command}'.",
            command=command,
        )

    def execute_text(
        self,
        command: str,
        requested_by: str = "text",
    ) -> ActionResult:
        """Parse and execute a text command."""

        parse_result = self.parse_text(
            command=command,
            requested_by=requested_by,
        )

        if not parse_result.success or parse_result.action is None:
            return ActionResult.fail(
                message=parse_result.message,
                reason="Text command could not be parsed into a structured action.",
            )

        return self.action_executor.execute(parse_result.action)

    def _parse_set_mode(
        self,
        mode: str,
        requested_by: str,
    ) -> TextCommandParseResult:
        """Parse a system mode command."""

        if not mode:
            return self._fail_with_suggestions(
                message="No system mode was provided.",
                command="set mode",
            )

        action = Action(
            action_type=ActionType.SET_STATE,
            target_id="system",
            target_type=ActionTargetType.SYSTEM,
            requested_by=requested_by,
            parameters={
                "mode": mode,
            },
        )

        return TextCommandParseResult.ok(action)

    def _parse_run_scene(
        self,
        scene_query: str,
        requested_by: str,
    ) -> TextCommandParseResult:
        """Parse a scene command."""

        scene = self._find_scene(scene_query)

        if scene is None:
            return self._fail_with_suggestions(
                message=f"No scene found matching '{scene_query}'.",
                command=scene_query,
            )

        action = Action(
            action_type=ActionType.RUN_SCENE,
            target_id=scene.id,
            target_type=ActionTargetType.SCENE,
            requested_by=requested_by,
        )

        return TextCommandParseResult.ok(action)

    def _fail_with_suggestions(
            self,
            message: str,
            command: str,
    ) -> TextCommandParseResult:
        """Create a failed parse result with command suggestions."""

        suggestions: list[str] = []

        if self.command_suggestion_service is not None:
            suggestions = self.command_suggestion_service.suggest_commands(command)

        return TextCommandParseResult.fail(
            message=message,
            suggestions=suggestions,
        )

    def _parse_power_action(
        self,
        target_query: str,
        action_type: ActionType,
        requested_by: str,
    ) -> TextCommandParseResult:
        """Parse a light power command."""

        room_query = self._strip_light_terms(target_query)
        room = self._find_room(room_query)

        if room is not None:
            action = Action(
                action_type=action_type,
                target_id=room.id,
                target_type=ActionTargetType.ROOM,
                requested_by=requested_by,
            )

            return TextCommandParseResult.ok(action)

        matches = self._find_matching_devices(target_query)

        if not matches:
            return self._fail_with_suggestions(
                message=f"No room or device found matching '{target_query}'.",
                command=target_query,
            )

        if len(matches) > 1:
            options = ", ".join(device.id for device in matches)

            return self._fail_with_suggestions(
                message=f"Multiple devices matched '{target_query}': {options}.",
                command=target_query,
            )

        device = matches[0]

        action = Action(
            action_type=action_type,
            target_id=device.id,
            target_type=ActionTargetType.DEVICE,
            requested_by=requested_by,
        )

        return TextCommandParseResult.ok(action)

    def _find_room(self, query: str):
        """Find a room by ID or name."""

        normalised_query = query.strip().lower()

        if not normalised_query:
            return None

        room = self.room_registry.get_room_by_id(normalised_query)

        if room is not None:
            return room

        room = self.room_registry.find_room_by_name(normalised_query)

        if room is not None:
            return room

        slug_query = normalised_query.replace(" ", "-")

        return self.room_registry.get_room_by_id(slug_query)

    def _find_scene(self, query: str):
        """Find a scene by ID or name."""

        normalised_query = query.strip().lower()

        if not normalised_query:
            return None

        scene = self.scene_registry.get_scene_by_id(normalised_query)

        if scene is not None:
            return scene

        slug_query = normalised_query.replace(" ", "-")

        scene = self.scene_registry.get_scene_by_id(slug_query)

        if scene is not None:
            return scene

        for candidate in self.scene_registry.list_scenes():
            if candidate.name.lower() == normalised_query:
                return candidate

        return None

    def _find_matching_devices(self, device_query: str) -> list[Device]:
        """Find devices by ID, name, or token matching."""

        query = device_query.strip().lower()

        device_by_id = self.device_registry.get_device_by_id(query)

        if device_by_id is not None:
            return [device_by_id]

        device_by_name = self.device_registry.find_device_by_name(query)

        if device_by_name is not None:
            return [device_by_name]

        query_tokens = (
            query.replace(".", " ")
            .replace("_", " ")
            .replace("-", " ")
            .split()
        )

        matches: list[Device] = []

        for device in self.device_registry.list_devices():
            searchable_text = (
                f"{device.id} "
                f"{device.name} "
                f"{device.room_id} "
                f"{device.device_type.value}"
            ).lower()

            searchable_text = (
                searchable_text.replace(".", " ")
                .replace("_", " ")
                .replace("-", " ")
            )

            if all(token in searchable_text for token in query_tokens):
                matches.append(device)

        return matches

    def _strip_light_terms(self, query: str) -> str:
        """Remove common light words from a query."""

        ignored_words = {
            "the",
            "room",
            "light",
            "lights",
            "lamp",
            "lamps",
        }

        words = [
            word
            for word in query.split()
            if word not in ignored_words
        ]

        return " ".join(words).strip()

    def _normalise(self, command: str) -> str:
        """Normalise user text."""

        return " ".join(command.strip().lower().split())