"""Registry for HomeSteadOS command shortcuts."""

from homesteados.core.domain.shortcut import Shortcut


class ShortcutRegistry:
    """Stores command shortcuts."""

    def __init__(self) -> None:
        self._shortcuts: dict[str, Shortcut] = {}

    def register_shortcut(self, shortcut: Shortcut) -> None:
        """Register a shortcut."""

        if shortcut.id in self._shortcuts:
            raise ValueError(f"Shortcut '{shortcut.id}' is already registered.")

        self._shortcuts[shortcut.id] = shortcut

    def get_shortcut_by_id(self, shortcut_id: str) -> Shortcut | None:
        """Return a shortcut by ID."""

        return self._shortcuts.get(shortcut_id)

    def list_shortcuts(self) -> list[Shortcut]:
        """Return all shortcuts."""

        return list(self._shortcuts.values())

    def remove_shortcut(self, shortcut_id: str) -> Shortcut | None:
        """Remove and return a shortcut."""

        return self._shortcuts.pop(shortcut_id, None)

    def clear(self) -> None:
        """Remove all shortcuts."""

        self._shortcuts.clear()