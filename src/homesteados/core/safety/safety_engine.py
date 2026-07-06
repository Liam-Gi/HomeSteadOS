"""Safety engine for reviewing proposed actions before execution."""

from dataclasses import dataclass

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionRisk, SystemMode
from homesteados.core.domain.system_state import SystemState


@dataclass(frozen=True)
class SafetyDecision:
    """Represents the outcome of a safety review."""

    allowed: bool
    requires_confirmation: bool = False
    reason: str | None = None


class SafetyEngine:
    """Reviews actions before execution.

    The Safety Engine is the boundary between requested actions and execution.
    Future AI, API, voice, and automation requests must pass through this layer.
    """

    def __init__(self, system_state: SystemState | None = None) -> None:
        self.system_state = system_state

    def review_action(self, action: Action) -> SafetyDecision:
        """Review an action and decide whether it may proceed."""

        if action.requires_confirmation:
            return SafetyDecision(
                allowed=False,
                requires_confirmation=True,
                reason="This action requires confirmation before execution.",
            )

        if action.risk_level == ActionRisk.CRITICAL:
            return SafetyDecision(
                allowed=False,
                requires_confirmation=False,
                reason="Critical-risk actions are blocked by default.",
            )

        if action.risk_level == ActionRisk.HIGH:
            return SafetyDecision(
                allowed=False,
                requires_confirmation=True,
                reason="High-risk actions require confirmation before execution.",
            )

        if self._requires_ai_confirmation_in_current_mode(action):
            return SafetyDecision(
                allowed=False,
                requires_confirmation=True,
                reason=(
                    "AI-requested actions require confirmation while the system "
                    "is in Away or Vacation mode."
                ),
            )

        return SafetyDecision(
            allowed=True,
            reason="Action passed safety review.",
        )

    def _requires_ai_confirmation_in_current_mode(self, action: Action) -> bool:
        """Return True if AI actions need confirmation in the current mode."""

        if self.system_state is None:
            return False

        if action.requested_by != "ai":
            return False

        return self.system_state.mode in {
            SystemMode.AWAY,
            SystemMode.VACATION,
        }