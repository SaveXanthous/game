from random import choice

import pygame
from pygame.math import Vector2

from utils.animation import Animation
from entities.base.base_entity import BaseEntity
from entities.enemy.enemy import Enemy
from utils.timer import Timer


class Ability(BaseEntity):
    def __init__(self, player):
        enemies = list(Enemy.get_group())

        if not enemies:
            super().__init__()
            self.kill()
            return

        closest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            dist = player.pos.distance_to(enemy.pos)
            if dist < min_distance:
                min_distance = dist
                closest_enemy = enemy

        self.target_enemy = closest_enemy

        super().__init__()

        direction = self.target_enemy.pos - player.pos

        if direction.length() > 0:
            self.velocity = direction.normalize()
        else:
            self.velocity = Vector2(0, 1)

        arrow_sheet_horizontal = pygame.image.load('data/sprites/arrow.png').convert_alpha()

        angle = -self.velocity.as_polar()[1]

        arrow_anim = Animation(arrow_sheet_horizontal, 100, 100, scale=2, duration=100, loop=True)

        for i in range(len(arrow_anim.frames)):
            arrow_anim.frames[i] = pygame.transform.rotate(arrow_anim.frames[i], angle)

        self.animations = {
            "arrow": arrow_anim
        }

        self.current_state = "arrow"
        self.image = self.animations[self.current_state].get_current_frame()

        spawn_x = player.hitbox.centerx
        spawn_y = player.hitbox.centery

        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.flip = False

        self._type = "ability"

        self.hitbox = self.rect.inflate(-70 * 2, -70 * 2)

        self.damage = 5

        self.pos = Vector2(self.rect.centerx, self.rect.centery)
        self.speed = 10
        self.friction = 0

        self.lifetime_timer = Timer(1000)

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
        if self.lifetime_timer.check():
            self.kill()
