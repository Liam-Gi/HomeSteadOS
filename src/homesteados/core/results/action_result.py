"""Result object returned after action requests."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ActionResult:
    """Represents the result of an attempted HomeSteadOS action."""

    success: bool
    message: str
    action_id: str | None = None
    requires_confirmation: bool = False
    reason: str | None = None
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(
        cls,
        message: str,
        action_id: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> "ActionResult":
        """Create a successful action result."""

        return cls(
            success=True,
            message=message,
            action_id=action_id,
            data=data or {},
        )

    @classmethod
    def fail(
        cls,
        message: str,
        reason: str | None = None,
        action_id: str | None = None,
    ) -> "ActionResult":
        """Create a failed action result."""

        return cls(
            success=False,
            message=message,
            reason=reason,
            action_id=action_id,
        )

    @classmethod
    def confirmation_required(
        cls,
        message: str,
        reason: str | None = None,
        action_id: str | None = None,
    ) -> "ActionResult":
        """Create an action result that requires user confirmation."""

        return cls(
            success=False,
            message=message,
            reason=reason,
            action_id=action_id,
            requires_confirmation=True,
        )