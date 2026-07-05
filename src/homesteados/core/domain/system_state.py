"""Domain model for HomeSteadOS system state."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from homesteados.core.domain.enums import SystemMode


@dataclass
class SystemState:
    """Represents high-level HomeSteadOS state."""

    mode: SystemMode = SystemMode.HOME
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_by: str = "system"

    def set_mode(self, mode: SystemMode, updated_by: str = "system") -> None:
        """Update the current system mode."""

        self.mode = mode
        self.updated_at = datetime.now(UTC)
        self.updated_by = updated_by