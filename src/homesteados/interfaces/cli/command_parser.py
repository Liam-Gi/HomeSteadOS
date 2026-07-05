"""Temporary command parser for early CLI testing."""

from homesteados.core.domain.device import Device
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService


class CommandParser:
    """Parses simple CLI commands and routes them through core services."""

    def __init__(
        self,
        device_registry: DeviceRegistry,
        lighting_service: LightingService,
    ) -> None:
        self.device_registry = device_registry
        self.lighting_service = lighting_service

    def handle(self, command: str) -> str:
        """Handle a user command and return a response message."""

        normalised_command = command.strip().lower()

        if not normalised_command:
            return "Please enter a command."

        if normalised_command in {"help", "?"}:
            return self._help_text()

        if normalised_command in {"devices", "list devices"}:
            return self._list_devices()

        if normalised_command in {"status", "device status", "system status"}:
            return self._device_status()

        if normalised_command.startswith("turn on "):
            device_query = normalised_command.replace("turn on ", "", 1)
            return self._handle_light_action(device_query, turn_on=True)

        if normalised_command.startswith("turn off "):
            device_query = normalised_command.replace("turn off ", "", 1)
            return self._handle_light_action(device_query, turn_on=False)

        return (
            "Command not recognised. Type 'help' to see available commands."
        )

    def _handle_light_action(self, device_query: str, turn_on: bool) -> str:
        """Find a matching light and request the lighting service action."""

        matches = self._find_matching_devices(device_query)

        if not matches:
            return f"No device found matching '{device_query}'."

        if len(matches) > 1:
            options = "\n".join(
                f"- {device.id} ({device.name})"
                for device in matches
            )
            return f"Multiple devices matched '{device_query}':\n{options}"

        device = matches[0]

        if turn_on:
            result = self.lighting_service.turn_on_light(
                device.id,
                requested_by="cli",
            )
        else:
            result = self.lighting_service.turn_off_light(
                device.id,
                requested_by="cli",
            )

        if result.success:
            return result.message

        return f"Failed: {result.message}"

    def _find_matching_devices(self, device_query: str) -> list[Device]:
        """Find devices by ID, name, or simple token matching."""

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

            searchable_text = searchable_text.replace(".", " ").replace("_", " ")

            if all(token in searchable_text for token in query_tokens):
                matches.append(device)

        return matches

    def _list_devices(self) -> str:
        """Return a list of registered devices."""

        devices = self.device_registry.list_devices()

        if not devices:
            return "No devices are currently registered."

        lines = ["Registered devices:"]

        for device in devices:
            lines.append(f"- {device.id} ({device.name})")

        return "\n".join(lines)

    def _device_status(self) -> str:
        """Return current device state information."""

        devices = self.device_registry.list_devices()

        if not devices:
            return "No devices are currently registered."

        lines = ["Device status:"]

        for device in devices:
            lines.append(
                f"- {device.id}: {device.state.value}, "
                f"online={device.online}"
            )

        return "\n".join(lines)

    def _help_text(self) -> str:
        """Return help text for CLI users."""

        return "\n".join(
            [
                "Available commands:",
                "- help",
                "- devices",
                "- status",
                "- turn on office light",
                "- turn off office light",
                "- turn on kitchen light",
                "- turn off bedroom lamp",
                "- exit",
            ]
        )