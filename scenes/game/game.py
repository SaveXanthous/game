from entities.ability.ability import Ability
from entities.player import player
from events.default_events import DefaultEvents
from managers.arena_manager import ArenaManager
from scenes.base.base_scene import BaseScene
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from entities.base.base_entity import BaseEntity
from entities.camera.camera import Camera
from entities.world.world import World

class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        world = World()

        self.world = world
        self.world.generate_new_world()

        BaseEntity.world = self.world

        spawn_x = (world.map_size[0] * world.tile_size) // 2
        spawn_y = (world.map_size[1] * world.tile_size) // 2

        self.player = Player()
        self.player.pos = (spawn_x, spawn_y)


        self.camera = Camera()
        self.camera.set_target_camera(self.player)

        # ------------------------------------------------------------------

        self.arena_manager = ArenaManager(self.player, self.game_manager)

        base_interval = 2000
        adjusted_interval = base_interval / self.game_manager.difficulty

        self.arena_manager.update_enemy_types(Enemy.type, adjusted_interval)

        self.arena_manager.update_ability_types(Ability.type, 1000)


    def update(self):
        self.arena_manager.update()
        BaseEntity.container.update()


    def draw(self):
        self.world.render(self.game_manager.screen, self.camera.offset.x, self.camera.offset.y)
        self.camera.draw()
