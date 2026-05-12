from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2
from random import randint

from entities.animation_component.animation import Animation


class BaseEntity(ABC, pygame.sprite.Sprite):

    container = pygame.sprite.Group()
    _id_gen = 0

    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)
        cls.group = pygame.sprite.Group()


    def __init__(self):
        ABC.__init__(self)
        pygame.sprite.Sprite.__init__(self, type(self).group, BaseEntity.container)

        idle_sheet = pygame.image.load("data/sprites/player_idle.png").convert_alpha()

        self.animations = {
            "idle": Animation(idle_sheet, 100, 100, scale=2, duration=75, loop=True)
        }

        self.current_state = "idle"
        self.image = self.animations[self.current_state].get_current_frame()
        self.rect = self.image.get_rect(midbottom = (randint(0, 1280), randint(0, 720)))

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.velocity = Vector2(0, 0)
        self.speed = 1
        self.friction = 0.15

        self._type = "none"

        self.hitbox = self.rect.inflate(-80 * 2, -80 * 2)
        self.hp = 1
        self.damage = 0
        self.last_hit_time = 0
        self.invincibility_duration = 500

        self.id = BaseEntity.generate_new_id()


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
    def set_state(self, new_state):
        pass


    @abstractmethod
    def animate(self):
        pass


    @classmethod
    def get_group(cls):
        return cls.group

    @classmethod
    def get_count(cls):
        return len(cls.group)

    @classmethod
    def generate_new_id(cls):
        cls._id_gen += 1
        return cls._id_gen


    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > self.invincibility_duration:
            self.hp -= amount
            self.last_hit_time = now
            return True
        return False

    def move(self):
        self.velocity *= (1 - self.friction)

        if self.velocity.length() < 0.1: self.velocity = Vector2(0, 0)

        self.pos += self.velocity * self.speed  # нужно потом добавить time_delta

        self.rect.center = self.pos

        self.hitbox.center = self.rect.center

    def kill(self):
        super().kill()