from scenes.game.game import Game
from core.game_handle import GameHandle

class SceneManager(GameHandle):
    def __init__(self,game_manager):
        GameHandle.__init__(self, game_manager)
        self._current_scene = Game(game_manager)

    @property
    def current_scene(self):
        return self._current_scene
    @current_scene.setter
    def current_scene(self, scene):
        self._current_scene = scene

    def draw(self):
        self._current_scene.draw()

    def update(self):
        self._current_scene.update()

    def next_scene(self, scene):
        self._current_scene = scene