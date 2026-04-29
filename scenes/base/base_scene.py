from abc import abstractmethod, ABC
import pygame


class BaseScene(ABC):
    def __init__(self, game_manager):
        self._game_manager = game_manager
        self.screen = game_manager.screen

    @abstractmethod
    def update(self):
        pass

    def next_scene(self, scene):
        self._game_manager.next_scene(scene)

