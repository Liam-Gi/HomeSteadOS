"""Registry for HomeSteadOS scenes."""

from homesteados.core.domain.scene import Scene


class SceneRegistry:
    """Stores scenes."""

    def __init__(self) -> None:
        self._scenes: dict[str, Scene] = {}

    def register_scene(self, scene: Scene) -> None:
        """Register a scene."""

        if scene.id in self._scenes:
            raise ValueError(f"Scene '{scene.id}' is already registered.")

        self._scenes[scene.id] = scene

    def get_scene_by_id(self, scene_id: str) -> Scene | None:
        """Return a scene by ID."""

        return self._scenes.get(scene_id)

    def list_scenes(self) -> list[Scene]:
        """Return all scenes."""

        return list(self._scenes.values())

    def remove_scene(self, scene_id: str) -> Scene | None:
        """Remove and return a scene."""

        return self._scenes.pop(scene_id, None)

    def clear(self) -> None:
        """Remove all scenes."""

        self._scenes.clear()