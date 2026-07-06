"""Store for actions awaiting confirmation."""

from homesteados.core.domain.action import Action


class PendingActionStore:
    """Stores actions that require user confirmation before execution."""

    def __init__(self) -> None:
        self._pending_actions: dict[str, Action] = {}

    def add(self, action: Action) -> None:
        """Store a pending action."""

        self._pending_actions[action.id] = action

    def get(self, action_id: str) -> Action | None:
        """Return a pending action by ID."""

        return self._pending_actions.get(action_id)

    def remove(self, action_id: str) -> Action | None:
        """Remove and return a pending action."""

        return self._pending_actions.pop(action_id, None)

    def list_actions(self) -> list[Action]:
        """Return all pending actions."""

        return list(self._pending_actions.values())

    def clear(self) -> None:
        """Remove all pending actions."""

        self._pending_actions.clear()