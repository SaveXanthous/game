from abc import ABC, abstractmethod
from game.game_handle import GameHandle


class BaseEvents(ABC,GameHandle):
    def __init__(self, game_manager, scene = None):
        GameHandle.__init__(self, game_manager)
        self._scene = scene

    @property
    def game_manager(self):
        return self._game_manager

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        self._scene = scene

    @abstractmethod
    def process(self, event):
        pass