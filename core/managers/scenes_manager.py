from core.game_handle import GameHandle

class SceneManager(GameHandle):
    def __init__(self, game_manager, scene):
        GameHandle.__init__(self, game_manager)
        self.current_scene = scene

    @property
    def current_scene(self):
        return self._current_scene
    @current_scene.setter
    def current_scene(self, scene):
        self._current_scene = scene(self.game_manager)

    def draw(self):
        self._current_scene.draw()

    def update(self):
        self._current_scene.update()

    def next_scene(self, scene):
        self._current_scene = scene(self.game_manager)