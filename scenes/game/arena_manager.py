import pygame

from entities.ability.ability import Ability
from entities.enemy.enemy import Enemy
from utils.timer import Timer


class ArenaManager:

    def __init__(self, player):
        self.difficulty = 1.0
        self.difficulty_timer = Timer(15000)

        self.player = player

        self.enemy_types = dict()

    def update_enemy_types(self, new_type, duration):
        self.enemy_types.update({new_type: Timer(duration * (2 - self.difficulty))})
        if new_type == "enemy":
            Enemy(self.player, self)

    def spawn_enemies(self):
        for enemy_class, timer in self.enemy_types.items():
            if timer.check():
                if enemy_class == "enemy":
                    Enemy(self.player, self)

    def update_difficulty(self):
        if self.difficulty_timer.check():
            self.difficulty += 0.05

            for timer in self.enemy_types.values():
                timer.set_duration(timer.duration * (2 - self.difficulty))

    def update(self):
        if not self.difficulty == 1.90:
            self.update_difficulty()

        self.spawn_enemies()
