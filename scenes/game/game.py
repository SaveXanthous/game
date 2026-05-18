from entities.ability.ability import Ability
from entities.player import player
from events.default_events import DefaultEvents
from scenes.base.base_scene import BaseScene
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from entities.base.base_entity import BaseEntity
from entities.camera.camera import Camera
from entities.world.world import World
from scenes.game.ability_manager import AbilityManager
from scenes.game.arena_manager import ArenaManager
from scenes.game.events import PlayerControlsEvents
from scenes.game.upgrade_menu import UpgradeMenu


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

        self.arena_manager = ArenaManager(self.player)

        self.ability_manager = AbilityManager(self.player)

        self.player_events = PlayerControlsEvents(self.game_manager, self, self.ability_manager)
        self.game_manager.events_manager.add_events(self.player_events)

        self.arena_manager.update_enemy_types("enemy", 2000)

        self.ability_manager.update_ability_types("arrow", 1000)

        self.is_paused = False
        self.player.scene = self

        self.upgrade_menu = UpgradeMenu(self)


    def update(self):
        if not getattr(self, 'is_paused', False):
            self.arena_manager.update()
            BaseEntity.container.update()
            pass


    def draw(self):
        self.world.render(self.game_manager.screen, self.camera.offset.x, self.camera.offset.y)
        self.camera.draw()
        if getattr(self, 'is_paused', False):
            self.upgrade_menu.draw(self.game_manager.screen)
