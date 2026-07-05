"""Domain model for device capabilities."""

from dataclasses import dataclass
from typing import Any

from homesteados.core.domain.enums import CapabilityType


@dataclass(frozen=True)
class Capability:
    """Represents something a device can do or report."""

    capability_type: CapabilityType
    name: str
    metadata: dict[str, Any] | None = None