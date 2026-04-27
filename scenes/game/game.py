import pygame

from events.default_events import DefaultEvents
from scenes.base.base_scene import BaseScene
from entities.player.player import Player
from entities.enemy.enemy import Enemy

class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.player = Player()

        self.add_sprites(self.player)
        for i in range(1):
            self.add_sprites(Enemy(self.player))

    def update(self):
        self.sprites.update()

    def draw(self):
        self.sprites.draw(self.screen)

