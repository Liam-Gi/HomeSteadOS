"""Service for recording text command history."""

from homesteados.core.domain.action import Action
from homesteados.core.results.action_result import ActionResult
from homesteados.core.results.command_history import CommandHistoryEntry


class CommandHistoryService:
    """Stores text command preview and execution history in memory."""

    def __init__(self) -> None:
        self._entries: list[CommandHistoryEntry] = []

    def record_preview(
        self,
        command: str,
        requested_by: str,
        success: bool,
        message: str,
        action: Action | None = None,
        description: str | None = None,
    ) -> CommandHistoryEntry:
        """Record a command preview."""

        entry = CommandHistoryEntry(
            command=command,
            requested_by=requested_by,
            mode="preview",
            success=success,
            message=message,
            description=description,
            action_type=action.action_type.value if action is not None else None,
            target_id=action.target_id if action is not None else None,
            target_type=action.target_type.value if action is not None else None,
            risk_level=action.risk_level.value if action is not None else None,
            requires_confirmation=(
                action.requires_confirmation if action is not None else None
            ),
        )

        self._entries.append(entry)
        return entry

    def record_execution(
        self,
        command: str,
        requested_by: str,
        result: ActionResult,
        action: Action | None = None,
        description: str | None = None,
    ) -> CommandHistoryEntry:
        """Record a command execution."""

        entry = CommandHistoryEntry(
            command=command,
            requested_by=requested_by,
            mode="execute",
            success=result.success,
            message=result.message,
            description=description,
            action_type=action.action_type.value if action is not None else None,
            target_id=action.target_id if action is not None else None,
            target_type=action.target_type.value if action is not None else None,
            risk_level=action.risk_level.value if action is not None else None,
            requires_confirmation=result.requires_confirmation,
            result_data=result.data,
        )

        self._entries.append(entry)
        return entry

    def list_entries(self) -> list[CommandHistoryEntry]:
        """Return all command history entries."""

        return list(self._entries)

    def clear(self) -> None:
        """Clear command history."""

        self._entries.clear()