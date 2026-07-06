"""Service for generating behaviour insights from command history."""

from collections import Counter

from homesteados.core.results.behaviour_insight import BehaviourInsight
from homesteados.core.services.command_history_service import CommandHistoryService


class BehaviourInsightService:
    """Generates simple deterministic insights from command history."""

    def __init__(
        self,
        command_history_service: CommandHistoryService,
        repeated_command_threshold: int = 3,
    ) -> None:
        self.command_history_service = command_history_service
        self.repeated_command_threshold = repeated_command_threshold

    def generate_insights(self) -> list[BehaviourInsight]:
        """Generate behaviour insights."""

        insights: list[BehaviourInsight] = []

        insights.extend(self._repeated_command_insights())

        return insights

    def _repeated_command_insights(self) -> list[BehaviourInsight]:
        """Generate insights for repeated successful command executions."""

        entries = [
            entry
            for entry in self.command_history_service.list_entries()
            if entry.mode == "execute" and entry.success
        ]

        command_counts = Counter(entry.command for entry in entries)

        insights: list[BehaviourInsight] = []

        for command, count in command_counts.items():
            if count < self.repeated_command_threshold:
                continue

            insights.append(
                BehaviourInsight(
                    title="Repeated command detected",
                    message=(
                        f"You have run '{command}' {count} times. "
                        "This may be a good candidate for a scene, automation, "
                        "or shortcut."
                    ),
                    insight_type="repeated_command",
                    data={
                        "command": command,
                        "count": count,
                        "suggested_next_steps": [
                            "Create a scene",
                            "Create an automation",
                            "Create a shortcut",
                        ],
                    },
                )
            )

        return insights