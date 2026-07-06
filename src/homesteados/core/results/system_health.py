"""System health result models."""

from dataclasses import dataclass, field
from typing import Any

from homesteados.core.domain.enums import HealthStatus


@dataclass(frozen=True)
class HealthCheck:
    """Represents a single system health check."""

    name: str
    status: HealthStatus
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SystemHealthReport:
    """Represents the full HomeSteadOS health report."""

    status: HealthStatus
    checks: list[HealthCheck]
    summary: dict[str, Any] = field(default_factory=dict)