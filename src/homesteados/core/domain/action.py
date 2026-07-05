"""Domain model for requested device or system actions."""

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from homesteados.core.domain.enums import ActionType


@dataclass
class Action:
    """Represents a requested action before execution."""

    action_type: ActionType
    target_id: str
    id: str = field(default_factory=lambda: str(uuid4()))
    parameters: dict[str, Any] = field(default_factory=dict)
    requested_by: str = "system"
    requires_confirmation: bool = False