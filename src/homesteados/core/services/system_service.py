"""Service for system-level operations."""

from homesteados.core.domain.enums import SystemMode
from homesteados.core.domain.system_state import SystemState
from homesteados.core.events.event import Event
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType
from homesteados.core.results.action_result import ActionResult


class SystemService:
    """Provides system-level HomeSteadOS operations."""

    def __init__(
        self,
        system_state: SystemState,
        event_bus: EventBus | None = None,
    ) -> None:
        self.system_state = system_state
        self.event_bus = event_bus

    def get_mode(self) -> SystemMode:
        """Return the current system mode."""

        return self.system_state.mode

    def set_mode(
        self,
        mode: SystemMode | str,
        updated_by: str = "system",
    ) -> ActionResult:
        """Set the current system mode."""

        try:
            parsed_mode = (
                mode if isinstance(mode, SystemMode) else SystemMode(mode)
            )
        except ValueError:
            return ActionResult.fail(
                message=f"Unsupported system mode '{mode}'.",
                reason="The requested system mode is not recognised.",
            )

        previous_mode = self.system_state.mode

        if previous_mode == parsed_mode:
            return ActionResult.ok(
                message=f"System mode is already {parsed_mode.value}.",
                data={
                    "mode": self.system_state.mode.value,
                    "updated_by": self.system_state.updated_by,
                },
            )

        self.system_state.set_mode(parsed_mode, updated_by=updated_by)

        self._publish_mode_changed(
            previous_mode=previous_mode,
            new_mode=parsed_mode,
            updated_by=updated_by,
        )

        return ActionResult.ok(
            message=f"System mode changed to {parsed_mode.value}.",
            data={
                "previous_mode": previous_mode.value,
                "mode": parsed_mode.value,
                "updated_by": updated_by,
            },
        )

    def _publish_mode_changed(
        self,
        previous_mode: SystemMode,
        new_mode: SystemMode,
        updated_by: str,
    ) -> None:
        """Publish a system mode changed event."""

        if self.event_bus is None:
            return

        event = Event(
            event_type=EventType.SYSTEM_MODE_CHANGED,
            source="SystemService",
            payload={
                "previous_mode": previous_mode.value,
                "new_mode": new_mode.value,
                "updated_by": updated_by,
            },
        )

        self.event_bus.publish(event)