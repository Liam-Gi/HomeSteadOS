"""Domain model for HomeSteadOS scenes."""

from dataclasses import dataclass, field

from homesteados.core.domain.action import Action


@dataclass
class Scene:
    """Represents a saved group of actions."""

    id: str
    name: str
    actions: list[Action] = field(default_factory=list)
    enabled: bool = True