from xml.dom.minidom import Entity

import pygame

from entities.ability.ability import Ability
from events.default_events import DefaultEvents
from managers.arena_manager import ArenaManager
from scenes.base_scene import BaseScene
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from entities.base.base_entity import BaseEntity

class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.player = Player()

        self.arena_manager = ArenaManager(self.player)

        self.arena_manager.update_enemy_types(Enemy.type, 2000)

        self.arena_manager.update_ability_types(Ability.type, 1000)

    def update(self):
        self.arena_manager.update()

        BaseEntity.container.update()

        print(BaseEntity.container)

    def draw(self):
        BaseEntity.container.draw(self.screen)

