from random import choice

import pygame
from pygame.math import Vector2

from utils.animation import Animation
from entities.base.base_entity import BaseEntity
from entities.enemy.enemy import Enemy
from utils.timer import Timer


class Ability(BaseEntity):
    def __init__(self, player, ability_manager, index=0):
        super().__init__()

        self._type = "ability"
        self.damage = 5 * (1 + (0.25 * ability_manager.acquired_upgrades.get("arrow_dmg", 0)))
        self.speed = 10 * (1 + (0.25 * ability_manager.acquired_upgrades.get("arrow_spd", 0)))
        self.friction = 0
        self.lifetime_timer = Timer(1000)
        self.flip = False

        self.target_enemy = self._get_closest_enemy(player)

        if not self.target_enemy:
            self.kill()
            return

        self.index = index
        self.velocity = self._calculate_velocity(player)

        self._setup_animation()

        self.pos = Vector2(player.rect.centerx, player.rect.centery)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.hitbox = self.rect.inflate(-70 * 2, -70 * 2)

    def _get_closest_enemy(self, player):
        enemies = list(Enemy.get_group())
        if not enemies:
            return None

        closest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            dist = player.pos.distance_to(enemy.pos)
            if dist < min_distance:
                min_distance = dist
                closest_enemy = enemy

        return closest_enemy

    def _calculate_velocity(self, player):
        direction = self.target_enemy.pos - player.pos
        if direction.length() > 0:
            direction = direction.normalize()

            if self.index % 2 != 0:
                spread_angle = 15 * ((self.index + 1) // 2)
            else:
                spread_angle = -15 * (self.index // 2)

            direction = direction.rotate(spread_angle)
            return direction
        return Vector2(0, 1)

    def _setup_animation(self):
        arrow_sheet = pygame.image.load('data/sprites/arrow.png').convert_alpha()
        angle = -self.velocity.as_polar()[1]

        arrow_anim = Animation(arrow_sheet, 100, 100, scale=2, duration=100, loop=True)

        for i in range(len(arrow_anim.frames)):
            arrow_anim.frames[i] = pygame.transform.rotate(arrow_anim.frames[i], angle)

        self.animations = {
            "arrow": arrow_anim
        }
        self.current_state = "arrow"
        self.image = self.animations[self.current_state].get_current_frame()

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

    def can_move_to(self, new_center):
        return True

    def update(self):
        super().move()
        self.deal_damage()
        if self.lifetime_timer.check():
            self.kill()
