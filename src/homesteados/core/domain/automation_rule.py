"""Domain model for HomeSteadOS automation rules."""

from dataclasses import dataclass, field
from typing import Any

from homesteados.core.domain.action import Action
from homesteados.core.events.event import Event
from homesteados.core.events.event_types import EventType


@dataclass
class AutomationRule:
    """Represents an event-driven automation rule."""

    id: str
    name: str
    trigger_event_type: EventType
    action: Action
    trigger_payload_matches: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    def matches_event(self, event: Event) -> bool:
        """Return True if this rule should run for the event."""

        if not self.enabled:
            return False

        if event.event_type != self.trigger_event_type:
            return False

        for key, expected_value in self.trigger_payload_matches.items():
            if event.payload.get(key) != expected_value:
                return False

        return True