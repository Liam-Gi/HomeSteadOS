"""Temporary command parser for early CLI testing."""

from homesteados.core.services.room_service import RoomService
from homesteados.core.events.event_bus import EventBus
from homesteados.core.domain.device import Device
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService
from homesteados.core.domain.enums import SystemMode
from homesteados.core.services.system_service import SystemService
from homesteados.core.services.diagnostics_service import DiagnosticsService
from homesteados.core.services.audit_log_service import AuditLogService
from homesteados.core.services.confirmation_service import ConfirmationService
from homesteados.core.services.automation_service import AutomationService
from homesteados.core.services.scene_service import SceneService
from homesteados.core.services.text_command_service import TextCommandService
from homesteados.core.services.action_description_service import ActionDescriptionService


class CommandParser:
    """Parses simple CLI commands and routes them through core services."""

    def __init__(
            self,
            device_registry: DeviceRegistry,
            lighting_service: LightingService,
            room_service: RoomService | None = None,
            system_service: SystemService | None = None,
            diagnostics_service: DiagnosticsService | None = None,
            action_description_service: ActionDescriptionService | None = None,
            scene_service: SceneService | None = None,
            audit_log_service: AuditLogService | None = None,
            confirmation_service: ConfirmationService | None = None,
            automation_service: AutomationService | None = None,
            text_command_service: TextCommandService | None = None,
            event_bus: EventBus | None = None,
    ) -> None:
        self.device_registry = device_registry
        self.lighting_service = lighting_service
        self.automation_service = automation_service
        self.room_service = room_service
        self.system_service = system_service
        self.action_description_service = action_description_service
        self.text_command_service = text_command_service
        self.scene_service = scene_service
        self.diagnostics_service = diagnostics_service
        self.audit_log_service = audit_log_service
        self.confirmation_service = confirmation_service
        self.event_bus = event_bus

    def handle(self, command: str) -> str:
        """Handle a user command and return a response message."""

        normalised_command = command.strip().lower()

        if not normalised_command:
            return "Please enter a command."

        if self._looks_like_action_command(normalised_command):
            return self._handle_text_command(command)

        if normalised_command.startswith("preview "):
            command_to_preview = command.strip()[len("preview "):].strip()
            return self._preview_text_command(command_to_preview)

        if normalised_command in {"audit", "audit log"}:
            return self._audit_log()

        if normalised_command in {"health", "diagnostics"}:
            return self._system_health()

        if normalised_command in {"mode", "system mode"}:
            return self._system_mode()

        if normalised_command == "scenes":
            return self._scenes()

        if normalised_command.startswith("run scene "):
            scene_id = normalised_command.replace("run scene ", "", 1).strip()
            return self._run_scene(scene_id)

        if normalised_command in {"pending", "pending actions"}:
            return self._pending_actions()

        if normalised_command in {"automations", "automation rules"}:
            return self._automation_rules()

        if normalised_command.startswith("enable automation "):
            rule_id = normalised_command.replace("enable automation ", "", 1).strip()
            return self._enable_automation(rule_id)

        if normalised_command.startswith("disable automation "):
            rule_id = normalised_command.replace("disable automation ", "", 1).strip()
            return self._disable_automation(rule_id)

        if normalised_command.startswith("confirm "):
            action_id = normalised_command.replace("confirm ", "", 1).strip()
            return self._confirm_action(action_id)

        if normalised_command.startswith("cancel "):
            action_id = normalised_command.replace("cancel ", "", 1).strip()
            return self._cancel_action(action_id)

        if normalised_command.startswith("set mode "):
            mode = normalised_command.replace("set mode ", "", 1).strip()
            return self._set_system_mode(mode)

        if normalised_command in {"help", "?"}:
            return self._help_text()

        if normalised_command in {"events", "event log"}:
            return self._event_log()

        if normalised_command in {"devices", "list devices"}:
            return self._list_devices()

        if normalised_command in {"status", "device status", "system status"}:
            return self._device_status()

        if normalised_command in {"rooms", "list rooms"}:
            return self._list_rooms()

        if normalised_command.startswith("room status "):
            room_id = normalised_command.replace("room status ", "", 1).strip()
            return self._room_status(room_id)

        if normalised_command.startswith("turn on room "):
            room_id = normalised_command.replace("turn on room ", "", 1).strip()
            return self._handle_room_light_action(room_id, turn_on=True)

        if normalised_command.startswith("turn off room "):
            room_id = normalised_command.replace("turn off room ", "", 1).strip()
            return self._handle_room_light_action(room_id, turn_on=False)

        if normalised_command.startswith("turn on "):
            device_query = normalised_command.replace("turn on ", "", 1)
            return self._handle_light_action(device_query, turn_on=True)

        if normalised_command.startswith("turn off "):
            device_query = normalised_command.replace("turn off ", "", 1)
            return self._handle_light_action(device_query, turn_on=False)

        return (
            "Command not recognised. Type 'help' to see available commands."
        )

    def _event_log(self) -> str:
        """Return published event history."""

        if self.event_bus is None:
            return "Event logging is not enabled."

        events = self.event_bus.list_published_events()

        if not events:
            return "No events have been published yet."

        lines = ["Event log:"]

        for event in events:
            lines.append(
                f"- {event.event_type.value} from {event.source}"
            )

        return "\n".join(lines)

    def _pending_actions(self) -> str:
        """Return pending actions."""

        if self.confirmation_service is None:
            return "Confirmation service is not enabled."

        actions = self.confirmation_service.list_pending_actions()

        if not actions:
            return "No actions are pending confirmation."

        lines = ["Pending actions:"]

        for action in actions:
            lines.append(
                f"- {action.id} | {action.action_type.value} | "
                f"{action.target_type.value}:{action.target_id} | "
                f"requested_by={action.requested_by} | "
                f"risk={action.risk_level.value}"
            )

        return "\n".join(lines)

    def _preview_text_command(self, command: str) -> str:
        """Preview a text command without executing it."""

        if self.text_command_service is None:
            return "Text command service is not enabled."

        if self.action_description_service is None:
            return "Action description service is not enabled."

        parse_result = self.text_command_service.parse_text(
            command=command,
            requested_by="cli",
        )

        if not parse_result.success or parse_result.action is None:
            return f"Failed: {parse_result.message}"

        action = parse_result.action
        description = self.action_description_service.describe_action(action)

        return "\n".join(
            [
                "Preview:",
                f"- {description}",
                f"- action_type={action.action_type.value}",
                f"- target_type={action.target_type.value}",
                f"- target_id={action.target_id}",
                f"- requested_by={action.requested_by}",
                f"- risk={action.risk_level.value}",
                f"- requires_confirmation={action.requires_confirmation}",
            ]
        )

    def _looks_like_action_command(self, command: str) -> bool:
        """Return True if a command should be handled by TextCommandService."""

        return command.startswith(
            (
                "turn on ",
                "turn off ",
                "set mode ",
                "run scene ",
                "run ",
            )
        )

    def _handle_text_command(self, command: str) -> str:
        """Handle a command through TextCommandService."""

        if self.text_command_service is None:
            return "Text command service is not enabled."

        result = self.text_command_service.execute_text(
            command=command,
            requested_by="cli",
        )

        if result.success:
            return result.message

        if result.requires_confirmation:
            return f"Confirmation required: {result.message}"

        return f"Failed: {result.message}"

    def _automation_rules(self) -> str:
        """Return automation rules."""

        if self.automation_service is None:
            return "Automation service is not enabled."

        rules = self.automation_service.list_rules()

        if not rules:
            return "No automation rules are registered."

        lines = ["Automation rules:"]

        for rule in rules:
            status = "enabled" if rule.enabled else "disabled"
            lines.append(
                f"- {rule.id} | {rule.name} | {status} | "
                f"on {rule.trigger_event_type.value} -> "
                f"{rule.action.action_type.value} {rule.action.target_type.value}:{rule.action.target_id}"
            )

        return "\n".join(lines)

    def _enable_automation(self, rule_id: str) -> str:
        """Enable an automation rule."""

        if self.automation_service is None:
            return "Automation service is not enabled."

        result = self.automation_service.enable_rule(rule_id)

        if result.success:
            return result.message

        return f"Failed: {result.message}"

    def _disable_automation(self, rule_id: str) -> str:
        """Disable an automation rule."""

        if self.automation_service is None:
            return "Automation service is not enabled."

        result = self.automation_service.disable_rule(rule_id)

        if result.success:
            return result.message

        return f"Failed: {result.message}"

    def _scenes(self) -> str:
        """Return scenes."""

        if self.scene_service is None:
            return "Scene service is not enabled."

        scenes = self.scene_service.list_scenes()

        if not scenes:
            return "No scenes are registered."

        lines = ["Scenes:"]

        for scene in scenes:
            status = "enabled" if scene.enabled else "disabled"
            lines.append(
                f"- {scene.id} | {scene.name} | {status} | "
                f"{len(scene.actions)} action(s)"
            )

        return "\n".join(lines)

    def _run_scene(self, scene_id: str) -> str:
        """Run a scene."""

        if self.scene_service is None:
            return "Scene service is not enabled."

        result = self.scene_service.run_scene(
            scene_id=scene_id,
            requested_by="cli",
        )

        if result.success:
            return result.message

        if result.requires_confirmation:
            return f"Confirmation required: {result.message}"

        return f"Failed: {result.message}"

    def _confirm_action(self, action_id: str) -> str:
        """Confirm a pending action."""

        if self.confirmation_service is None:
            return "Confirmation service is not enabled."

        result = self.confirmation_service.confirm_action(action_id)

        if result.success:
            return result.message

        if result.requires_confirmation:
            return f"Confirmation still required: {result.message}"

        return f"Failed: {result.message}"

    def _cancel_action(self, action_id: str) -> str:
        """Cancel a pending action."""

        if self.confirmation_service is None:
            return "Confirmation service is not enabled."

        result = self.confirmation_service.cancel_action(action_id)

        if result.success:
            return result.message

        return f"Failed: {result.message}"

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
                "- rooms",
                "- room status office",
                "- turn on room office",
                "- turn off room office",
                "- mode",
                "- set mode home",
                "- set mode away",
                "- set mode night",
                "- run good night",
                "- run scene good-night",
                "- preview <command>",
                "- health",
                "- diagnostics",
                "- audit",
                "- audit log",
                "- scenes",
                "- run scene <scene_id>",
                "- pending",
                "- confirm <action_id>",
                "- cancel <action_id>",
                "- automations",
                "- enable automation <rule_id>",
                "- disable automation <rule_id>",
                "- events",
                "- exit",
            ]
        )

    def _list_rooms(self) -> str:
        """Return a list of known rooms."""

        if self.room_service is None:
            return "Room service is not enabled."

        rooms = self.room_service.room_registry.list_rooms()

        if not rooms:
            return "No rooms are currently registered."

        lines = ["Registered rooms:"]

        for room in rooms:
            lines.append(f"- {room.id} ({room.name})")

        return "\n".join(lines)

    def _room_status(self, room_id: str) -> str:
        """Return devices in a room."""

        if self.room_service is None:
            return "Room service is not enabled."

        room = self.room_service.room_registry.get_room_by_id(room_id)

        if room is None:
            return f"Room '{room_id}' was not found."

        devices = self.room_service.list_devices_in_room(room_id)

        if not devices:
            return f"No devices are registered in {room.name}."

        lines = [f"{room.name} devices:"]

        for device in devices:
            lines.append(
                f"- {device.id}: {device.state.value}, online={device.online}"
            )

        return "\n".join(lines)

    def _system_mode(self) -> str:
        """Return the current system mode."""

        if self.system_service is None:
            return "System service is not enabled."

        return f"System mode: {self.system_service.get_mode().value}"

    def _set_system_mode(self, mode: str) -> str:
        """Set the current system mode."""

        if self.system_service is None:
            return "System service is not enabled."

        result = self.system_service.set_mode(
            mode=mode,
            updated_by="cli",
        )

        if result.success:
            return result.message

        return f"Failed: {result.message}"

    def _handle_room_light_action(self, room_id: str, turn_on: bool) -> str:
        """Turn all lights in a room on or off."""

        if self.room_service is None:
            return "Room service is not enabled."

        if turn_on:
            result = self.room_service.turn_on_room_lights(
                room_id=room_id,
                requested_by="cli",
            )
        else:
            result = self.room_service.turn_off_room_lights(
                room_id=room_id,
                requested_by="cli",
            )

        if result.success:
            return result.message

        return f"Failed: {result.message}"

    def _system_health(self) -> str:
        """Return system health information."""

        if self.diagnostics_service is None:
            return "Diagnostics service is not enabled."

        report = self.diagnostics_service.get_health_report()

        lines = [
            f"System health: {report.status.value}",
            f"Mode: {report.summary['mode']}",
            f"Devices: {report.summary['device_count']}",
            f"Rooms: {report.summary['room_count']}",
            f"Adapters: {report.summary['adapter_count']}",
            f"Events: {report.summary['event_count']}",
            "Checks:",
        ]

        for check in report.checks:
            lines.append(
                f"- {check.name}: {check.status.value} - {check.message}"
            )

        return "\n".join(lines)

    def _audit_log(self) -> str:
        """Return audit log entries."""

        if self.audit_log_service is None:
            return "Audit log service is not enabled."

        entries = self.audit_log_service.list_entries()

        if not entries:
            return "No audit log entries have been recorded yet."

        lines = ["Audit log:"]

        for entry in entries:
            lines.append(
                f"- {entry.occurred_at.isoformat()} | "
                f"{entry.event_type.value} | "
                f"{entry.message}"
            )

        return "\n".join(lines)