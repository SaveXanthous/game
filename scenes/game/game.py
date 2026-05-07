from xml.dom.minidom import Entity

import pygame

from entities.ability.ability import Ability
from events.default_events import DefaultEvents
from scenes.base.base_scene import BaseScene
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from entities.base.base_entity import BaseEntity

class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.player = Player()
        Enemy(self.player)
        Enemy(self.player)
        Enemy(self.player)
        Enemy(self.player)
        Enemy(self.player)
        Enemy(self.player)
        Enemy(self.player)
        Enemy(self.player)


        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()
        Ability()

        print(BaseEntity.container)

    def update(self):
        BaseEntity.container.update()

    def draw(self):
        BaseEntity.container.draw(self.screen)

