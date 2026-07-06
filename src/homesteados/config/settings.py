"""Application settings for HomeSteadOS."""

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DEMO_CONFIG_PATH = PROJECT_ROOT / "configs" / "demo_home.json"


@dataclass(frozen=True)
class AppSettings:
    """Application settings for HomeSteadOS."""

    environment: str
    log_level: str
    demo_config_path: Path


def get_settings() -> AppSettings:
    """Load application settings from environment variables."""

    demo_config_path = os.getenv("HOMESTEADOS_DEMO_CONFIG")

    return AppSettings(
        environment=os.getenv("HOMESTEADOS_ENV", "development"),
        log_level=os.getenv("HOMESTEADOS_LOG_LEVEL", "INFO").upper(),
        demo_config_path=(
            Path(demo_config_path)
            if demo_config_path
            else DEFAULT_DEMO_CONFIG_PATH
        ),
    )