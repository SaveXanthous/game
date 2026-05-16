from random import choice

import pygame
from pygame.math import Vector2

from utils.animation import Animation
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

        arrow_sheet_horizontal = pygame.image.load('data/sprites/arrow.png').convert_alpha()
        arrow_sheet_vertical = pygame.transform.rotate(arrow_sheet_horizontal, -90)

        self.animations = {
            "arrow": Animation(arrow_sheet_vertical, 100, 100, scale=2, duration=100, loop = True)
        }

        self.current_state = "arrow"
        self.image = self.animations[self.current_state].get_current_frame()

        spawn_x = self.target_enemy.hitbox.centerx
        spawn_y = self.target_enemy.hitbox.top - 5

        self.max_distance = 200

        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
        self.flip = False

        self._type = "ability"

        self.hitbox = self.rect.inflate(-70 * 2, -70 * 2)

        self.damage = 5

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.start_pos = self.pos
        self.velocity = Vector2(0, 1)
        self.speed = 7.5
        self.friction = 0

    def deal_damage(self):
        enemy_group = Enemy.get_group()

        hit_list = pygame.sprite.spritecollide(
            self,
            enemy_group,
            False,
            collided=lambda sprite, other: sprite.hitbox.colliderect(other.hitbox)
        )
        for enemy in hit_list:
            if enemy.take_damage(self.damage):
                return


    def set_state(self, new_state):
        pass

    def animate(self):
        pass

    def update(self):
        super().move()
        self.deal_damage()
        if self.pos.distance_to(self.start_pos) > self.max_distance:
            self.kill()
