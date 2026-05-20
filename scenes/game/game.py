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
from ui.elements.ui_label import Label


class Game(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)


        self.map_size = (70, 70)
        self.tile_size = 64
        world = World(map_size=self.map_size,tile_size=self.tile_size)

        self.world = world
        self.world.generate_new_world()

        BaseEntity.world = self.world

        spawn_grid_x, spawn_grid_y = world.spawn_point
        spawn_x = spawn_grid_x * world.tile_size + (world.tile_size // 2)
        spawn_y = spawn_grid_y * world.tile_size + (world.tile_size // 2)

        self.player = Player()
        self.player.pos = (spawn_x, spawn_y)


        self.camera = Camera()
        min_rad = min(self.map_size) * self.tile_size
        max_rad = max(self.map_size) * self.tile_size
        self.camera.spawn_cinematic(self.player, min_rad ,max_rad)

        self.is_freeze = False

        self.hp_bar = ProgressBar(
        "hp_bar",
            x=+200, y=-300-150,
            w=400, h=50,
            base_image_path="data/ui/bar/BigBar_Base.png",
            fill_image_path="data/ui/bar/BigBar_Fill.png",
            text="",
            progress=1.0,
            offset_x = 11, offset_y = 0,
            offset_w = 0, offset_h = 0
        )

        self.hp_bar.move_by_easing(y=-150)

        self.xp_bar = ProgressBar(
            "xp_bar",
            x=+150, y=-275-150,
            w=300, h=50,
            base_image_path="data/ui/bar/SmallBar_Base.png",
            fill_image_path="data/ui/bar/SmallBar_Fill.png",
            text="",
            progress=1.0,
            offset_x=11, offset_y=0,
            offset_w=0, offset_h=0
        )

        self.xp_bar.move_by_easing(y=-150)

        self.label_score = Label('label_score', 0, 320+150, 700, 80, 'Score: 0', 48, show_bg=True,
              bg_image_path='data/ui/label/BigRibbons.png')

        self.label_score.move_by_easing(y=150)

        self.is_stop = False

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

        self.is_hide_ui = False


    def update(self):

        if self.is_hide_ui and self.label_score.is_finished:
            self.is_hide_ui = False
            min_rad = min(self.map_size) * self.tile_size
            max_rad = max(self.map_size) * self.tile_size
            self.camera.spawn_cinematic(min_radius=min_rad, max_radius=max_rad, mode='ease_in')

        if self.is_stop and self.label_score.is_finished and self.camera.is_cinematic_finished:
            for entity in BaseEntity.container:
                entity.kill()
            self.game_manager.last_score = self.player.score
            self.game_manager.events_manager.remove_events(self.player_events)
            self.next_scene(GameOver)


        if not getattr(self, 'is_paused', False) and self.camera.is_cinematic_finished:
            self.arena_manager.update()
            BaseEntity.container.update()
            pass

        if self.camera.is_cinematic_finished:
            for element in [self.label_score, self.hp_bar, self.xp_bar]:
                element.update_easing()

        if self.player.hp <= 0 and not self.is_stop:
            self.stop()


        self.label_score.set_text(f'Score: {self.player.score}')
        self.hp_bar.set_progress(self.player.hp/ self.player.max_hp)
        self.xp_bar.set_progress(self.player.xp / self.player.max_xp)


    def draw(self):
        self.world.render(self.game_manager.screen, self.camera.offset.x, self.camera.offset.y)
        self.camera.draw()
        self.upgrade_menu.draw(self.game_manager.screen)

    def hide_ui(self):
        self.is_hide_ui = True
        for element in [self.hp_bar, self.xp_bar]:
            element.move_by_easing(y=150)

        self.label_score.move_by_easing(y=-150)

    def stop(self):
        self.hide_ui()
        self.is_stop = True