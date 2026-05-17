from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2
from random import randint

from entities.animation_component.animation import Animation
from entities.world.world import World


class BaseEntity(ABC, pygame.sprite.Sprite):

    container = pygame.sprite.Group()
    _world = None
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

        self.pos = Vector2(self.rect.centerx, self.rect.centery)
        self.velocity = Vector2(0, 0)
        self.speed = 1
        self.friction = 0.15

        self._type = "none"

        self.hitbox = self.rect.inflate(-80 * 2, -80 * 2)
        self.hitbox.bottom = self.rect.bottom
        self.hp = 1
        self.damage = 0
        self.last_hit_time = 0
        self.invincibility_duration = 500

        self.id = BaseEntity.generate_new_id()


    @property
    def world(cls):
        return cls._world

    @world.setter
    def world(cls, value):
        cls._world = value


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

    def can_move_to(self, new_center):
        temp_rect = self.hitbox.copy()
        temp_rect.center = (new_center.x, new_center.y)

        corners = [
            temp_rect.topleft,
            temp_rect.topright,
            temp_rect.bottomleft,
            temp_rect.bottomright
        ]

        for corner in corners:
            if self.world.get_tile_at(corner[0], corner[1]) == 0:
                return False
        return True




    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > self.invincibility_duration:
            self.hp -= amount
            self.last_hit_time = now
            return True
        return False

    def move(self):
        self.velocity *= (1 - self.friction)
        if self.velocity.length() < 0.1:
            self.velocity = Vector2(0, 0)

        target_pos = self.pos + self.velocity * self.speed

        next_center_x = Vector2(target_pos.x, self.pos.y)
        if self.can_move_to(next_center_x):
            self.pos.x = target_pos.x

        next_center_y = Vector2(self.pos.x, target_pos.y)
        if self.can_move_to(next_center_y):
            self.pos.y = target_pos.y

        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.hitbox.center = self.rect.center

    def kill(self):
        super().kill()