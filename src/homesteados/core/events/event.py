"""Base event model for HomeSteadOS."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from homesteados.core.events.event_types import EventType


@dataclass(frozen=True)
class Event:
    """Represents something that happened inside HomeSteadOS."""

    event_type: EventType
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))