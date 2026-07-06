"""Service for running HomeSteadOS scenes."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.scene import Scene
from homesteados.core.registry.scene_registry import SceneRegistry
from homesteados.core.results.action_result import ActionResult


class SceneService:
    """Runs saved scenes through the ActionDispatcher."""

    def __init__(
        self,
        scene_registry: SceneRegistry,
        action_executor,
    ) -> None:
        self.scene_registry = scene_registry
        self.action_executor = action_executor

    def list_scenes(self) -> list[Scene]:
        """Return all scenes."""

        return self.scene_registry.list_scenes()

    def run_scene(
        self,
        scene_id: str,
        requested_by: str = "system",
    ) -> ActionResult:
        """Run a scene by ID."""

        scene = self.scene_registry.get_scene_by_id(scene_id)

        if scene is None:
            return ActionResult.fail(
                message=f"Scene '{scene_id}' was not found.",
                reason="No registered scene matched the provided ID.",
            )

        if not scene.enabled:
            return ActionResult.fail(
                message=f"Scene '{scene_id}' is disabled.",
                reason="Disabled scenes cannot be run.",
            )

        results = []

        for action_template in scene.actions:
            action = self._create_action_from_template(
                scene=scene,
                action_template=action_template,
                requested_by=requested_by,
            )

            result = self.action_executor.execute(action)

            results.append(
                {
                    "action_id": result.action_id,
                    "success": result.success,
                    "requires_confirmation": result.requires_confirmation,
                    "message": result.message,
                    "reason": result.reason,
                }
            )

            if result.requires_confirmation:
                return ActionResult.confirmation_required(
                    message=f"Scene '{scene.name}' requires confirmation.",
                    reason=result.reason,
                    action_id=result.action_id,
                    data={
                        "scene_id": scene.id,
                        "scene_name": scene.name,
                        "results": results,
                    },
                )

            if not result.success:
                return ActionResult.fail(
                    message=f"Scene '{scene.name}' failed.",
                    reason=result.reason,
                    action_id=result.action_id,
                    data={
                        "scene_id": scene.id,
                        "scene_name": scene.name,
                        "results": results,
                    },
                )

        return ActionResult.ok(
            message=f"Scene '{scene.name}' completed.",
            data={
                "scene_id": scene.id,
                "scene_name": scene.name,
                "results": results,
            },
        )

    def _create_action_from_template(
        self,
        scene: Scene,
        action_template: Action,
        requested_by: str,
    ) -> Action:
        """Create a fresh Action from a scene action template."""

        return Action(
            action_type=action_template.action_type,
            target_id=action_template.target_id,
            target_type=action_template.target_type,
            parameters=dict(action_template.parameters),
            requested_by=f"scene:{scene.id}:{requested_by}",
            requires_confirmation=action_template.requires_confirmation,
            risk_level=action_template.risk_level,
        )