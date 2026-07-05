"""Event bus for publishing and subscribing to system events."""

from collections.abc import Callable

from homesteados.core.events.event import Event
from homesteados.core.events.event_types import EventType

EventHandler = Callable[[Event], None]


class EventBus:
    """Simple synchronous event bus for HomeSteadOS."""

    def __init__(self) -> None:
        self._subscribers: dict[EventType, list[EventHandler]] = {}
        self._all_subscribers: list[EventHandler] = []
        self._published_events: list[Event] = []

    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """Subscribe a handler to a specific event type."""

        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: EventHandler) -> None:
        """Subscribe a handler to all events."""

        self._all_subscribers.append(handler)

    def publish(self, event: Event) -> None:
        """Publish an event to all matching subscribers."""

        self._published_events.append(event)

        for handler in self._all_subscribers:
            handler(event)

        for handler in self._subscribers.get(event.event_type, []):
            handler(event)

    def list_published_events(self) -> list[Event]:
        """Return all events published during this process."""

        return list(self._published_events)

    def clear(self) -> None:
        """Clear subscribers and stored event history."""

        self._subscribers.clear()
        self._all_subscribers.clear()
        self._published_events.clear()