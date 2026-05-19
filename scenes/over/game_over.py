import os
import pygame
from scenes.base.base_scene import BaseScene
from scenes.over.events import GameOverEvents
from utils.json_handler import JSONHandler

from ui.elements.ui_button import Button
from ui.elements.ui_label import Label
from ui.elements.ui_panel import Panel
from ui.decorator.register_ui_element import ui_elements

class GameOver(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.score = getattr(self.game_manager, 'last_score', 0)
        self.scores_filepath = os.path.join("data", "scores", "scores.json")

        self.best_score = self.load_best_score()

        self.is_new_record = self.score > self.best_score


        if self.is_new_record:
            JSONHandler.update(self.scores_filepath, self.score, "best_score")

        self.background = Panel('background', 0-900, 0, 0, 0, image_path=os.path.join('data', 'ui', 'panel', 'water.png'),
                                style='tile_screen')

        self.panel = Panel('game_over_panel', 0-900, 20, 320, 380,
                           image_path=os.path.join('data', 'ui', 'panel', 'SpecialPaper.png'))

        Label('title_label', 0-900, 140, 500, 120, 'GAME OVER', 54, show_bg=True,
              bg_image_path=os.path.join('data', 'ui', 'label', 'BigRibbons.png'), bg_color_index=1)

        if self.is_new_record:
            Label('record_label', 0-900, 50, 250, 50, f"NEW RECORD: {self.score}", 32, font_color=(255, 215, 0))
        else:
            Label('score_label', 0-900, 60, 250, 40, f"Score: {self.score}", 28, font_name='arial')
            Label('best_score_label', 0-900, 20, 250, 40, f"Best Score: {self.best_score}", 24, font_color=(160, 160, 160),font_name='arial')

        path_red_1 = os.path.join('data', 'ui', 'button', 'BigBlueButton_Regular.png')
        path_red_2 = os.path.join('data', 'ui', 'button', 'BigBlueButton_Pressed.png')
        Button('menu_button', 0-900, -50, 200, 50, path_red_1, path_red_2, 'Main Menu', action=self.press_menu_button)

        path_blue_1 = os.path.join('data', 'ui', 'button', 'BigRedButton_Regular.png')
        path_blue_2 = os.path.join('data', 'ui', 'button', 'BigRedButton_Pressed.png')
        Button('exit_button', 0-900, -110, 200, 50, path_blue_1, path_blue_2, 'Exit', action=self.press_exit_button)

        self.events = GameOverEvents(game_manager, self)
        game_manager.events_manager.add_events(self.events)

        self.go_to_menu = False
        self.quit_game = False

        for element_id in ui_elements:
            if element_id == 'background':
                continue
            ui_elements[element_id].move_by_easing(x=-900)

    def load_best_score(self):
        data = JSONHandler.read(self.scores_filepath)

        if not data:
            base_structure = {"best_score": 0}
            JSONHandler.write(self.scores_filepath, base_structure)
            return 0

        return data.get("best_score", 0)

    def press_menu_button(self):
        for element_id in ui_elements:
            if element_id == 'background':
                continue
            ui_elements[element_id].move_by_easing(x=900)
        self.go_to_menu = True

    def press_exit_button(self):
        for element_id in ui_elements:
            if element_id == 'background':
                continue
            ui_elements[element_id].move_by_easing(x=900)
        self.quit_game = True

    def clean_up_and_switch(self):
        self.game_manager.events_manager.remove_events(self.events)
        self.game_manager.ui_manager.kill()

        if self.go_to_menu:
            from scenes.menu.menu import Menu
            self.game_manager.scenes_manager.next_scene(Menu)
        elif self.quit_game:
            pygame.quit()
            import sys
            sys.exit()

    def update(self):
        if (self.go_to_menu or self.quit_game) and self.panel.is_finished:
            self.clean_up_and_switch()

        for element in list(ui_elements.values()):
            element.update_easing()

    def draw(self):
        pass