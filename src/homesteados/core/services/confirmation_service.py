"""Service for confirming or cancelling pending actions."""

from homesteados.core.registry.pending_action_store import PendingActionStore
from homesteados.core.results.action_result import ActionResult


class ConfirmationService:
    """Handles confirmation workflow for pending actions."""

    def __init__(
        self,
        pending_action_store: PendingActionStore,
        action_executor,
    ) -> None:
        self.pending_action_store = pending_action_store
        self.action_executor = action_executor

    def list_pending_actions(self):
        """Return all pending actions."""

        return self.pending_action_store.list_actions()

    def cancel_action(self, action_id: str) -> ActionResult:
        """Cancel a pending action."""

        action = self.pending_action_store.remove(action_id)

        if action is None:
            return ActionResult.fail(
                message=f"Pending action '{action_id}' was not found.",
                reason="No pending action matched the provided action ID.",
            )

        return ActionResult.ok(
            message=f"Pending action '{action_id}' cancelled.",
            action_id=action_id,
            data={
                "action_type": action.action_type.value,
                "target_id": action.target_id,
            },
        )

    def confirm_action(self, action_id: str) -> ActionResult:
        """Confirm and execute a pending action."""

        action = self.pending_action_store.remove(action_id)

        if action is None:
            return ActionResult.fail(
                message=f"Pending action '{action_id}' was not found.",
                reason="No pending action matched the provided action ID.",
            )

        # The action has now been explicitly confirmed.
        action.requires_confirmation = False
        action.confirmed = True

        return self.action_executor.execute(action)