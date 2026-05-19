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
from scenes.over.game_over import GameOver
from ui.elements.ui_progress_bar import ProgressBar


class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)


        map_size = (70, 70)
        tile_size = 64
        world = World(map_size=map_size,tile_size=tile_size)

        self.world = world
        self.world.generate_new_world()

        BaseEntity.world = self.world

        spawn_x = (world.map_size[0] * world.tile_size) // 2
        spawn_y = (world.map_size[1] * world.tile_size) // 2

        self.player = Player()
        self.player.pos = (spawn_x, spawn_y)


        self.camera = Camera()
        min_rad = min(map_size[0], map_size[1]) * tile_size
        max_rad = max(map_size[0], map_size[1]) * tile_size
        self.camera.spawn_cinematic(self.player, min_rad ,max_rad)

        self.is_freeze = False

        self.my_bar = ProgressBar(
        "hp_bar",
            x=+200, y=-300,
            w=400, h=50,
            base_image_path="data/ui/bar/BigBar_Base.png",
            fill_image_path="data/ui/bar/BigBar_Fill.png",
            text="",
            progress=1.0,
            offset_x = 11, offset_y = 0,
            offset_w = 11, offset_h = 0
        )

        self.value = 1.0


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

        self.arena_manager.update()
        BaseEntity.container.update()


    def update(self):
        if not getattr(self, 'is_paused', False) and self.camera.is_cinematic_finished:
            self.arena_manager.update()
            BaseEntity.container.update()
            pass

        if self.player.hp <= 0:
            self.game_manager.last_score = self.player.score

            self.game_manager.events_manager.remove_events(self.player_events)
            self.next_scene(GameOver)


    def draw(self):
        self.world.render(self.game_manager.screen, self.camera.offset.x, self.camera.offset.y)
        self.camera.draw()
        if getattr(self, 'is_paused', False):
            self.upgrade_menu.draw(self.game_manager.screen)
