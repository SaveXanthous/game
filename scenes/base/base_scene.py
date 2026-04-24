from abc import abstractmethod, ABC
import pygame


class BaseScene(ABC):
    def __init__(self, game_manager):
        self._game_manager = game_manager
        self._sprites = pygame.sprite.Group()
        self.screen = game_manager.screen

    @property
    def sprites(self):
        return self._sprites

    @sprites.setter
    def sprites(self, value):
        self._sprites = value

    def add_sprites(self, sprites):
        self._sprites.add(sprites)

    def remove_sprite(self, sprite):
        self._sprites.remove(sprite)

    def get_sprite_by_id(self, id):
        for sprite in self._sprites:
            if sprite.id == id:
                return sprite

    @abstractmethod
    def update(self):
        pass

    def next_scene(self, scene):
        self._game_manager.next_scene(scene)

