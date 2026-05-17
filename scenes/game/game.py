from entities.ability.ability import Ability
from scenes.game.ability_manager import AbilityManager
from scenes.game.arena_manager import ArenaManager
from scenes.base.base_scene import BaseScene
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from entities.base.base_entity import BaseEntity
from entities.camera.camera import Camera

class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.player = Player()

        self.arena_manager = ArenaManager(self.player)
        self.ability_manager = AbilityManager(self.player)

        self.arena_manager.update_enemy_types(Enemy.type, 2000)

        self.ability_manager.update_ability_types(Ability.type, 1000)

        self.camera = Camera()
        self.camera.set_target_camera(self.player)

    def update(self):
        self.arena_manager.update()
        self.ability_manager.update()

        BaseEntity.container.update()


    def draw(self):
        self.camera.draw(BaseEntity.container)

