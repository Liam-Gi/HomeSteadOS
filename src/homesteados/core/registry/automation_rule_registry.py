"""Registry for HomeSteadOS automation rules."""

from homesteados.core.domain.automation_rule import AutomationRule


class AutomationRuleRegistry:
    """Stores automation rules."""

    def __init__(self) -> None:
        self._rules: dict[str, AutomationRule] = {}

    def register_rule(self, rule: AutomationRule) -> None:
        """Register an automation rule."""

        if rule.id in self._rules:
            raise ValueError(f"Automation rule '{rule.id}' is already registered.")

        self._rules[rule.id] = rule

    def get_rule_by_id(self, rule_id: str) -> AutomationRule | None:
        """Return an automation rule by ID."""

        return self._rules.get(rule_id)

    def list_rules(self) -> list[AutomationRule]:
        """Return all automation rules."""

        return list(self._rules.values())

    def remove_rule(self, rule_id: str) -> AutomationRule | None:
        """Remove and return an automation rule."""

        return self._rules.pop(rule_id, None)

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule."""

        rule = self.get_rule_by_id(rule_id)

        if rule is None:
            return False

        rule.enabled = True
        return True

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule."""

        rule = self.get_rule_by_id(rule_id)

        if rule is None:
            return False

        rule.enabled = False
        return True

    def clear(self) -> None:
        """Remove all automation rules."""

        self._rules.clear()