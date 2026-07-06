"""Service for recording HomeSteadOS audit log entries."""

from homesteados.core.events.event import Event
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType
from homesteados.core.results.audit_log import AuditLogEntry


class AuditLogService:
    """Records important HomeSteadOS events for later inspection."""

    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self._entries: list[AuditLogEntry] = []

    def start(self) -> None:
        """Subscribe to the event bus."""

        self.event_bus.subscribe_all(self.record_event)

    def record_event(self, event: Event) -> None:
        """Record an event as an audit log entry."""

        entry = AuditLogEntry(
            event_id=event.id,
            event_type=event.event_type,
            source=event.source,
            occurred_at=event.occurred_at,
            message=self._message_for_event(event),
            payload=event.payload,
        )

        self._entries.append(entry)

    def list_entries(self) -> list[AuditLogEntry]:
        """Return all audit log entries."""

        return list(self._entries)

    def clear(self) -> None:
        """Clear audit log entries."""

        self._entries.clear()

    def _message_for_event(self, event: Event) -> str:
        """Create a readable audit message for an event."""

        if event.event_type == EventType.ACTION_REQUESTED:
            return (
                f"Action requested: {event.payload.get('action_type')} "
                f"for {event.payload.get('target_id')} "
                f"by {event.payload.get('requested_by')}"
            )

        if event.event_type == EventType.ACTION_COMPLETED:
            return (
                f"Action completed: {event.payload.get('action_type')} "
                f"for {event.payload.get('target_id')}"
            )

        if event.event_type == EventType.ACTION_FAILED:
            return (
                f"Action failed: {event.payload.get('action_type')} "
                f"for {event.payload.get('target_id')}"
            )

        if event.event_type == EventType.ACTION_BLOCKED:
            return (
                f"Action blocked: {event.payload.get('action_type')} "
                f"for {event.payload.get('target_id')}"
            )

        if event.event_type == EventType.DEVICE_STATE_CHANGED:
            return (
                f"Device state changed: {event.payload.get('device_id')} "
                f"from {event.payload.get('previous_state')} "
                f"to {event.payload.get('new_state')}"
            )

        if event.event_type == EventType.SYSTEM_MODE_CHANGED:
            return (
                f"System mode changed from {event.payload.get('previous_mode')} "
                f"to {event.payload.get('new_mode')} "
                f"by {event.payload.get('updated_by')}"
            )

        return f"Event recorded: {event.event_type.value}"