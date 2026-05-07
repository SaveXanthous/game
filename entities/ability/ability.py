from random import randint, choice

import pygame
from pygame.math import Vector2

from entities.animation_component.animation import Animation
from entities.base.base_entity import BaseEntity
from entities.enemy.enemy import Enemy


class Ability(BaseEntity):
    def __init__(self):
        enemies = list(Enemy.get_group())

        if not enemies:
            super().__init__()
            self.kill()
            return

        self.target_enemy = choice(enemies)

        super().__init__()

        arrow = pygame.image.load('data/sprites/arrow.png')

        self.animations = {
            "arrow": Animation(arrow, 100, 100, scale=2, duration=100, loop = True)
        }

        self.current_state = "arrow"
        self.image = self.animations[self.current_state].get_current_frame()

        spawn_x = self.target_enemy.rect.centerx
        spawn_y = self.target_enemy.rect.top - 5

        self.max_distance = 200

        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
        self.flip = False

        self._type = "ability"

        self.hitbox = self.rect

        self.damage = 5

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.start_pos = self.pos
        self.velocity = Vector2(0, 1)
        self.speed = 5
        self.friction = 0

    def set_state(self, new_state):
        pass

    def animate(self):
        pass

    def update(self):
        super().move()
        if self.pos.distance_to(self.start_pos) > self.max_distance:
            self.kill()

        # if self.rect.colliderect(self.target_enemy.rect):
        #     self.target_enemy.hp -= self.damage
        #     super().kill()
