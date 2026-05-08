from abc import ABC, abstractmethod
from core.game_handle import GameHandle


class BaseEvents(ABC):
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

    @game_manager.setter
    def game_manager(self, value):
        self._game_manager = value

    @abstractmethod
    def process(self, event):
        pass