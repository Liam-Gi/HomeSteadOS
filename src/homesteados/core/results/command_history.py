"""Command history result models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class CommandHistoryEntry:
    """Represents a text command preview or execution."""

    command: str
    requested_by: str
    mode: str
    success: bool
    message: str
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=datetime.now)
    action_type: str | None = None
    target_id: str | None = None
    target_type: str | None = None
    risk_level: str | None = None
    requires_confirmation: bool | None = None
    description: str | None = None
    result_data: dict[str, Any] = field(default_factory=dict)