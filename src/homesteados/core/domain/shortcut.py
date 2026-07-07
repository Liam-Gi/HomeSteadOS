"""Domain model for HomeSteadOS command shortcuts."""

from dataclasses import dataclass


@dataclass
class Shortcut:
    """Represents a named shortcut for a text command."""

    id: str
    name: str
    command: str
    enabled: bool = True