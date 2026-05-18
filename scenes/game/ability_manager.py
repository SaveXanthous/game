from shlex import join

import pygame

from entities.ability.ability import Ability
from entities.enemy.enemy import Enemy
from utils.timer import Timer


class AbilityManager:

    def __init__(self, player):

        self.player = player

        self.ability_types = dict()
        self.max_abilities = 3

        self.acquired_upgrades = dict()

    def update_ability_types(self, new_type, duration):
        if not self.ability_types.__len__() >= self.max_abilities:
            self.ability_types.update({new_type: Timer(duration), "start_duration": duration})


    def use_abilities(self, ability_type):
        timer = self.ability_types.get(ability_type)
        amount = 1 + self.acquired_upgrades.get(ability_type + "_amt", 0)
        if timer and timer.check():
            if ability_type == "arrow":
                for i in range(amount):
                    Ability(self.player, self, index=i)


    def apply_upgrade(self, upgrade):
        upg_id = upgrade["id"]
        a_type = upgrade["ability_type"]
        u_type = upgrade["upgrade_type"]

        if upg_id not in self.acquired_upgrades:
            self.acquired_upgrades.update({upg_id: 0})
        self.acquired_upgrades[upg_id] = self.acquired_upgrades.get(upg_id, 0) + 1

        if u_type == "recharge":
            duration = self.ability_types["start_duration"]
            self.ability_types[a_type] = Timer(duration - (100 * self.acquired_upgrades.get(upg_id, 0)))
