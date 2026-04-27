from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2
from random import randint

from entities.animation_component.animation import Animation


class BaseEntity(ABC, pygame.sprite.Sprite):

    entities = []
    count = 0
    _id_gen = 0

    def __init__(self):
        ABC.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        idle_sheet = pygame.image.load("data/sprites/player_idle.png").convert_alpha()

        self.animations = {
            "idle": Animation(idle_sheet, 100, 100, scale=2, duration=75, loop=True)
        }

        self.current_state = "idle"
        self.image = self.animations[self.current_state].get_current_frame()
        self.rect = self.image.get_rect(midbottom = (randint(0, 1280), randint(0, 720)))

        self.hp = 10
        self.hitbox = self.rect.inflate(-80, -80)

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.velocity = Vector2(0, 0)
        self.speed = 1
        self.friction = 0.15

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


    @abstractmethod
    def update(self):
        pass


    @abstractmethod
    def move(self):
        pass


    @abstractmethod
    def set_state(self, new_state):
        pass


    @abstractmethod
    def animate(self):
        pass


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

    def kill(self, game_manager):
        BaseEntity.remove(self)
        game_manager.remove(self)
        del self