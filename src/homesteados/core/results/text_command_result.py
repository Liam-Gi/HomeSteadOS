"""Result model for text command parsing."""

from dataclasses import dataclass, field

from homesteados.core.domain.action import Action


@dataclass(frozen=True)
class TextCommandParseResult:
    """Represents the result of parsing a text command."""

    success: bool
    message: str
    action: Action | None = None
    suggestions: list[str] = field(default_factory=list)

    @classmethod
    def ok(
        cls,
        action: Action,
        message: str = "Text command parsed.",
    ) -> "TextCommandParseResult":
        """Create a successful parse result."""

        return cls(
            success=True,
            message=message,
            action=action,
        )

    @classmethod
    def fail(
            cls,
            message: str,
            suggestions: list[str] | None = None,
    ) -> "TextCommandParseResult":
        """Create a failed parse result."""

        return cls(
            success=False,
            message=message,
            action=None,
            suggestions=suggestions or [],
        )