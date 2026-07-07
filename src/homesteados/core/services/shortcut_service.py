"""Service for running HomeSteadOS command shortcuts."""

from homesteados.core.domain.shortcut import Shortcut
from homesteados.core.registry.shortcut_registry import ShortcutRegistry
from homesteados.core.results.action_result import ActionResult


class ShortcutService:
    """Runs saved shortcuts through the TextCommandService."""

    def __init__(
        self,
        shortcut_registry: ShortcutRegistry,
        text_command_service,
    ) -> None:
        self.shortcut_registry = shortcut_registry
        self.text_command_service = text_command_service
        self._running_shortcut_ids: set[str] = set()

    def list_shortcuts(self) -> list[Shortcut]:
        """Return all shortcuts."""

        return self.shortcut_registry.list_shortcuts()

    def run_shortcut(
        self,
        shortcut_id: str,
        requested_by: str = "system",
    ) -> ActionResult:
        """Run a shortcut by ID."""

        shortcut = self.shortcut_registry.get_shortcut_by_id(shortcut_id)

        if shortcut is None:
            return ActionResult.fail(
                message=f"Shortcut '{shortcut_id}' was not found.",
                reason="No registered shortcut matched the provided ID.",
            )

        if not shortcut.enabled:
            return ActionResult.fail(
                message=f"Shortcut '{shortcut_id}' is disabled.",
                reason="Disabled shortcuts cannot be run.",
            )

        if shortcut.id in self._running_shortcut_ids:
            return ActionResult.fail(
                message=f"Shortcut '{shortcut_id}' is already running.",
                reason="Shortcut execution loop detected.",
            )

        self._running_shortcut_ids.add(shortcut.id)

        try:
            result = self.text_command_service.execute_text(
                command=shortcut.command,
                requested_by=f"shortcut:{shortcut.id}:{requested_by}",
            )

            result.data["shortcut_id"] = shortcut.id
            result.data["shortcut_name"] = shortcut.name
            result.data["shortcut_command"] = shortcut.command

            return result

        finally:
            self._running_shortcut_ids.remove(shortcut.id)