import pygame

from entities.ability.ability import Ability
from entities.enemy.enemy import Enemy
from utils.timer import Timer


class AbilityManager:

    def __init__(self, player):

        self.player = player

        self.ability_types = dict()
        self.max_abilities = 3

    def update_ability_types(self, new_type, duration):
        if not self.ability_types.__len__() >= self.max_abilities:
            self.ability_types.update({new_type: Timer(duration)})


    def use_abilities(self, ability_type):
        timer = self.ability_types[ability_type]
        if timer.check():
            if ability_type == Ability.type:
                Ability()



    def update(self):
        pass

