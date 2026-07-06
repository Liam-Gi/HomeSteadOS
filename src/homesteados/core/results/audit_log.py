"""Audit log result models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from homesteados.core.events.event_types import EventType


@dataclass(frozen=True)
class AuditLogEntry:
    """Represents a single audit log entry."""

    event_id: str
    event_type: EventType
    source: str
    occurred_at: datetime
    message: str
    payload: dict[str, Any] = field(default_factory=dict)