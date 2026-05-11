import pygame

from entities.ability.ability import Ability
from entities.enemy.enemy import Enemy
from utils.timer import Timer


class ArenaManager:

    def __init__(self, player):
        self.player = player
        self.enemy_types = []
        self.enemy_timers = []
        self.ability_types = []
        self.ability_timers = []

    def update_enemy_types(self, new_type, duration):
        self.enemy_types.append(new_type)
        self.enemy_timers.append(Timer(duration))

    def update_ability_types(self, new_type, duration):
        self.ability_types.append(new_type)
        self.ability_timers.append(Timer(duration))

    def update(self):
        for i in range(0, self.enemy_types.__len__()):
            if self.enemy_timers[i].check():
                if self.enemy_types[i] == Enemy.type:
                    Enemy(self.player)

        for i in range(0, self.ability_types.__len__()):
            if self.ability_timers[i].check():
                if self.ability_types[i] == Ability.type:
                    Ability()