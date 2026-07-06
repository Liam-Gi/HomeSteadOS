"""Service for event-driven HomeSteadOS automations."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.automation_rule import AutomationRule
from homesteados.core.events.event import Event
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType
from homesteados.core.registry.automation_rule_registry import AutomationRuleRegistry
from homesteados.core.results.action_result import ActionResult


class AutomationService:
    """Runs automation rules when matching events are published."""

    def __init__(
        self,
        automation_rule_registry: AutomationRuleRegistry,
        event_bus: EventBus,
        action_executor,
    ) -> None:
        self.automation_rule_registry = automation_rule_registry
        self.event_bus = event_bus
        self.action_executor = action_executor
        self._running_rule_ids: set[str] = set()

    def start(self) -> None:
        """Subscribe automation handling to the event bus."""

        self.event_bus.subscribe_all(self.handle_event)

    def register_rule(self, rule: AutomationRule) -> None:
        """Register an automation rule."""

        self.automation_rule_registry.register_rule(rule)

    def list_rules(self) -> list[AutomationRule]:
        """Return all automation rules."""

        return self.automation_rule_registry.list_rules()

    def enable_rule(self, rule_id: str) -> ActionResult:
        """Enable an automation rule."""

        enabled = self.automation_rule_registry.enable_rule(rule_id)

        if not enabled:
            return ActionResult.fail(
                message=f"Automation rule '{rule_id}' was not found.",
                reason="No automation rule matched the provided ID.",
            )

        return ActionResult.ok(
            message=f"Automation rule '{rule_id}' enabled.",
            data={"rule_id": rule_id},
        )

    def disable_rule(self, rule_id: str) -> ActionResult:
        """Disable an automation rule."""

        disabled = self.automation_rule_registry.disable_rule(rule_id)

        if not disabled:
            return ActionResult.fail(
                message=f"Automation rule '{rule_id}' was not found.",
                reason="No automation rule matched the provided ID.",
            )

        return ActionResult.ok(
            message=f"Automation rule '{rule_id}' disabled.",
            data={"rule_id": rule_id},
        )

    def handle_event(self, event: Event) -> None:
        """Run matching automation rules for an event."""

        for rule in self.automation_rule_registry.list_rules():
            if not rule.matches_event(event):
                continue

            if rule.id in self._running_rule_ids:
                continue

            self._execute_rule(rule, event)

    def _execute_rule(
        self,
        rule: AutomationRule,
        source_event: Event,
    ) -> None:
        """Execute a matching automation rule."""

        self._running_rule_ids.add(rule.id)

        try:
            action = self._create_action_from_rule(rule)
            result = self.action_executor.execute(action)

            if result.success:
                self._publish_automation_event(
                    event_type=EventType.AUTOMATION_TRIGGERED,
                    rule=rule,
                    source_event=source_event,
                    result=result,
                )
            else:
                self._publish_automation_event(
                    event_type=EventType.AUTOMATION_FAILED,
                    rule=rule,
                    source_event=source_event,
                    result=result,
                )

        finally:
            self._running_rule_ids.remove(rule.id)

    def _create_action_from_rule(self, rule: AutomationRule) -> Action:
        """Create a fresh Action instance from a rule action template."""

        return Action(
            action_type=rule.action.action_type,
            target_id=rule.action.target_id,
            target_type=rule.action.target_type,
            parameters=dict(rule.action.parameters),
            requested_by=f"automation:{rule.id}",
            requires_confirmation=rule.action.requires_confirmation,
            risk_level=rule.action.risk_level,
        )

    def _publish_automation_event(
        self,
        event_type: EventType,
        rule: AutomationRule,
        source_event: Event,
        result: ActionResult,
    ) -> None:
        """Publish an automation result event."""

        event = Event(
            event_type=event_type,
            source="AutomationService",
            payload={
                "rule_id": rule.id,
                "rule_name": rule.name,
                "source_event_id": source_event.id,
                "source_event_type": source_event.event_type.value,
                "result_success": result.success,
                "result_message": result.message,
                "result_reason": result.reason,
            },
        )

        self.event_bus.publish(event)