from random import randint

import pygame

import utils.scaler
from entities.animation_component.animation import Animation
from entities.base.base_entity import BaseEntity
from entities.player.player import Player
from pygame.math import Vector2

from utils import scaler


class Enemy(BaseEntity):
    def __init__(self, player: Player, arena_manager):
        super().__init__()

        walk_sheet = pygame.image.load("data/sprites/enemy_walk.png").convert_alpha()

        self.animations = {
            "walk": Animation(walk_sheet, 100, 100, scale=2, duration=100, loop=True)
        }

        self.current_state = "walk"
        self.image = self.animations[self.current_state].get_current_frame()
        self.rect = self.image.get_rect(midbottom=(randint(0, scaler.Scaler.scaled_x(1280)), randint(0, scaler.Scaler.scaled_x(720))))
        self.flip = False

        self._type = "enemy"
        self.player = player

        self.arena_manager = arena_manager
        self.difficulty = self.arena_manager.difficulty

        self.hp = 10 * self.difficulty
        self.damage = 1

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.speed = 0.25 * self.difficulty

        self.repulsion_strength = 1  # Сила отталкивания
        self.personal_space = 20  # Расстояние, ближе которого врагам тесно

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

    def update(self):
        self.player_direction()
        self.avoid_overlap()

        self.update_difficulty()

        super().move()
        self.animate()
        self.deal_damage()

        if self.hp <= 0:
            self.kill()
