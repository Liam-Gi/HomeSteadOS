"""Safety engine for reviewing proposed actions before execution."""

from dataclasses import dataclass

from homesteados.core.domain.action import Action


@dataclass(frozen=True)
class SafetyDecision:
    """Represents the outcome of a safety review."""

    allowed: bool
    requires_confirmation: bool = False
    reason: str | None = None


class SafetyEngine:
    """Reviews actions before execution.

    This is intentionally simple for now.
    Future versions will add policies for locks, cameras, alarms,
    security modes, user permissions, and AI-generated actions.
    """

    def review_action(self, action: Action) -> SafetyDecision:
        """Review an action and decide whether it may proceed."""

        if action.requires_confirmation:
            return SafetyDecision(
                allowed=False,
                requires_confirmation=True,
                reason="This action requires confirmation before execution.",
            )

        return SafetyDecision(
            allowed=True,
            reason="Action passed basic safety review.",
        )