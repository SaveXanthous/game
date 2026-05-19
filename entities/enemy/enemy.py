from random import randint, uniform

import pygame

from entities.experience_coin.experience_coin import ExperienceCoin
from utils.animation import Animation
from entities.base.base_entity import BaseEntity
from entities.player.player import Player
from pygame.math import Vector2

from utils import scaler

class Enemy(BaseEntity):
    def __init__(self, player: Player, arena_manager):
        self._type = "enemy"
        self.player = player
        self.arena_manager = arena_manager
        self.difficulty = self.arena_manager.difficulty

        super().__init__()

    def _setup_animations(self):
        walk_sheet = pygame.image.load("data/sprites/enemy_walk.png").convert_alpha()

        self.animations = {
            "walk": Animation(walk_sheet, 100, 100, scale=2, duration=100, loop=True)
        }

        self.current_state = "walk"
        self.image = self.animations[self.current_state].get_current_frame()
        self.flip = False

        min_radius = 700
        max_radius = 1200
        spawn_pos = Vector2(self.player.pos.x, self.player.pos.y)

        safe_margin = 80

        for i in range(50):
            angle = uniform(0, 360)
            distance = randint(min_radius, max_radius)
            offset = Vector2(distance, 0).rotate(angle)
            target_pos = self.player.pos + offset

            points_to_check = [
                (target_pos.x, target_pos.y),
                (target_pos.x - safe_margin, target_pos.y - safe_margin),
                (target_pos.x + safe_margin, target_pos.y - safe_margin),
                (target_pos.x - safe_margin, target_pos.y + safe_margin),
                (target_pos.x + safe_margin, target_pos.y + safe_margin)
            ]

            is_safe = True
            for px, py in points_to_check:
                if self.world.get_tile_at(px, py) == 0:
                    is_safe = False
                    break

            if is_safe:
                spawn_pos = target_pos
                break

        self.rect = self.image.get_rect(center=(spawn_pos.x, spawn_pos.y))

    def _setup_stats(self):
        super()._setup_stats()
        self.hp = 10 * self.difficulty
        self.damage = 1

    def _setup_physics(self):
        super()._setup_physics()
        self.pos = Vector2(self.rect.centerx, self.rect.centery)
        self.speed = 0.25 * self.difficulty
        self.repulsion_strength = 1
        self.personal_space = 20

    def update_difficulty(self):
        new_difficulty = self.arena_manager.difficulty
        if new_difficulty > self.difficulty:
            self.difficulty = new_difficulty
            self.speed *= self.difficulty

    def deal_damage(self):
        if self.hitbox.colliderect(self.player.hitbox):
            if self.player.take_damage(self.damage):
                return

    def set_state(self, new_state):
        if self.current_state != new_state:
            self.current_state = new_state
            self.animations[self.current_state].reset()

    def animate(self):
        if self.velocity.x > 0:
            self.set_state("walk")
            self.flip = False
        elif self.velocity.x < 0:
            self.set_state("walk")
            self.flip = True

        current_animation = self.animations[self.current_state]
        current_animation.update()
        raw_image = current_animation.get_current_frame()
        self.image = pygame.transform.flip(raw_image, self.flip, False)

    def player_direction(self):
        acceleration = (self.player.pos - self.pos).normalize()

        self.velocity += acceleration

    def avoid_overlap(self):
        repulsion = Vector2(0, 0)
        for other in Enemy.get_group():
            if other is not self:
                diff = self.pos - other.pos
                distance = diff.length()

                if 0 < distance < self.personal_space:
                    repulsion += diff.normalize() * (self.personal_space / distance)

        self.velocity += repulsion * self.repulsion_strength

    def kill_low_hp(self):
        self.player.score += 50

        drop_chance = 60

        if randint(1, 100) <= drop_chance:
            ExperienceCoin(self.pos, self.player)

        self.kill()

    def update(self):
        self.player_direction()
        self.avoid_overlap()

        self.update_difficulty()

        super().move()
        self.animate()
        self.deal_damage()

        if self.hp <= 0:
            self.kill_low_hp()
