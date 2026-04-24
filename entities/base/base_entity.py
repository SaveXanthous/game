from abc import ABC, abstractmethod
from itertools import count
import pygame
from pygame.math import Vector2
from random import randint


class BaseEntity(ABC, pygame.sprite.Sprite):

    entities = []
    count = 0
    _id_gen = 0

    def __init__(self):
        ABC.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("data/sprites/enemy.png")
        self.rect = self.image.get_rect(midbottom = (randint(0, 1280), randint(0, 720)))
        self.pos = Vector2(self.rect.x, self.rect.y)

        self._type = "none"

        self.id = BaseEntity.generate_new_id()
        BaseEntity.add(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Vector2(value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    # ---------------------------------------------------------------------------------------------

    @abstractmethod
    def update(self):
        pass

    # ---------------------------------------------------------------------------------------------

    @classmethod
    def add(cls, value):
        cls.entities.append(value)
        cls.count += 1

    @classmethod
    def remove(cls, value):
        cls.entities.remove(value)
        cls.count -= 1

    @classmethod
    def get_entities(cls):
        return cls.entities

    @classmethod
    def get_count(cls):
        return len(cls.count)

    @classmethod
    def generate_new_id(cls):
        cls._id_gen += 1
        return cls._id_gen

    # ---------------------------------------------------------------------------------------------

    def kill(self, game_manager):
        BaseEntity.remove(self)
        game_manager.remove(self)
        del self