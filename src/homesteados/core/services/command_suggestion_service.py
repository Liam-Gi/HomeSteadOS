"""Service for suggesting supported text commands."""

from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.registry.scene_registry import SceneRegistry


class CommandSuggestionService:
    """Suggests valid HomeSteadOS text commands."""

    def __init__(
        self,
        room_registry: RoomRegistry,
        scene_registry: SceneRegistry,
    ) -> None:
        self.room_registry = room_registry
        self.scene_registry = scene_registry

    def suggest_commands(
            self,
            command: str,
            limit: int = 8,
    ) -> list[str]:
        """Return suggested commands for a failed input command."""

        normalised_command = self._normalise(command)
        suggestions: list[str] = []

        suggestions.extend(
            self._suggest_scene_commands(normalised_command)
        )
        suggestions.extend(
            self._suggest_system_mode_commands(normalised_command)
        )
        suggestions.extend(
            self._suggest_room_light_commands(normalised_command)
        )

        return self._dedupe(suggestions)[:limit]

    def list_common_commands(self, limit: int = 10) -> list[str]:
        """Return common supported commands."""

        suggestions: list[str] = []

        suggestions.extend(
            self._suggest_room_light_commands("")
        )
        suggestions.extend(
            self._suggest_scene_commands("")
        )
        suggestions.extend(
            self._suggest_system_mode_commands("")
        )

        return self._dedupe(suggestions)[:limit]

    def _suggest_room_light_commands(self, command: str) -> list[str]:
        """Suggest room light commands."""

        suggestions: list[str] = []

        rooms = self.room_registry.list_rooms()

        for room in rooms:
            room_name = room.name.lower()

            if self._command_mentions(command, room.id, room_name):
                suggestions.append(f"turn on {room_name} light")
                suggestions.append(f"turn off {room_name} light")
                suggestions.append(f"preview turn on {room_name} light")
                suggestions.append(f"preview turn off {room_name} light")

        if suggestions:
            return suggestions

        for room in rooms:
            room_name = room.name.lower()
            suggestions.append(f"turn on {room_name} light")
            suggestions.append(f"turn off {room_name} light")

        return suggestions

    def _suggest_scene_commands(self, command: str) -> list[str]:
        """Suggest scene commands."""

        suggestions: list[str] = []

        scenes = self.scene_registry.list_scenes()

        for scene in scenes:
            scene_name = scene.name.lower()

            if self._command_mentions(command, scene.id, scene_name):
                suggestions.append(f"run {scene_name}")
                suggestions.append(f"run scene {scene.id}")
                suggestions.append(f"preview run {scene_name}")

        if suggestions:
            return suggestions

        for scene in scenes:
            scene_name = scene.name.lower()
            suggestions.append(f"run {scene_name}")

        return suggestions

    def _suggest_system_mode_commands(self, command: str) -> list[str]:
        """Suggest system mode commands."""

        modes = [
            "home",
            "away",
            "night",
            "guest",
            "vacation",
        ]

        suggestions: list[str] = []

        for mode in modes:
            if mode in command:
                suggestions.append(f"set mode {mode}")
                suggestions.append(f"preview set mode {mode}")

        if suggestions:
            return suggestions

        return [
            "set mode home",
            "set mode away",
            "set mode night",
        ]

    def _command_mentions(
        self,
        command: str,
        identifier: str,
        name: str,
    ) -> bool:
        """Return True if command seems related to an identifier or name."""

        if not command:
            return False

        identifier_tokens = self._tokens(identifier)
        name_tokens = self._tokens(name)
        command_tokens = set(self._tokens(command))

        return bool(command_tokens.intersection(identifier_tokens | name_tokens))

    def _tokens(self, value: str) -> set[str]:
        """Tokenise text for basic matching."""

        cleaned = (
            value.lower()
            .replace(".", " ")
            .replace("_", " ")
            .replace("-", " ")
        )

        return {
            token
            for token in cleaned.split()
            if token
        }

    def _dedupe(self, suggestions: list[str]) -> list[str]:
        """Remove duplicate suggestions while preserving order."""

        seen: set[str] = set()
        unique: list[str] = []

        for suggestion in suggestions:
            if suggestion in seen:
                continue

            seen.add(suggestion)
            unique.append(suggestion)

        return unique

    def _normalise(self, command: str) -> str:
        """Normalise user text."""

        return " ".join(command.strip().lower().split())