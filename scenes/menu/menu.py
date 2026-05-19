from scenes.base.base_scene import BaseScene
from scenes.menu.events import MenuEvents
from ui.elements.ui_button import Button
from ui.elements.ui_label import Label
from ui.elements.ui_panel import Panel
from scenes.game.game import Game
from ui.decorator.register_ui_element import ui_elements

import pygame
import os



class Menu(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.panel = Panel('background', 0+900, 0, 0, 0,image_path=os.path.join('data', 'ui', 'panel', 'water.png'), style='tile_screen')

        self.panel = Panel('menu_panel', 0+900,0, 260, 320, image_path=os.path.join('data', 'ui', 'panel', 'RegularPaper.png'))
        menu_panel = self.panel.image

        Label('title_label', 0+900, 70, 400, 120, 'GAME', 72, show_bg=True, bg_image_path=os.path.join('data', 'ui', 'label', 'BigRibbons.png'))

        path_1 = os.path.join('data', 'ui', 'button', 'BigRedButton_Regular.png')
        path_2 = os.path.join('data', 'ui', 'button', 'BigRedButton_Pressed.png')
        Button('play_button', 0+900, -30, 200, 50, path_1, path_2, 'Play', action=self.play_button)

        path_1 = os.path.join('data', 'ui', 'button', 'BigBlueButton_Regular.png')
        path_2 = os.path.join('data', 'ui', 'button', 'BigBlueButton_Pressed.png')
        Button('exit_button', 0+900, -90, 200, 50, path_1, path_2, 'Exit', action=self.exit_button)

        self.events = MenuEvents(game_manager, self)
        game_manager.events_manager.add_events(self.events)

        self.play = False
        self.quit_game = False

        for element_id in ui_elements:
            if element_id == 'background':
                continue
            ui_elements[element_id].move_by_easing(x=+900)

    def play_button(self):
        for id in ui_elements:
            if id == 'background':
                continue
            ui_elements[id].move_by_easing(x = -900)

        self.play = True


    def exit(self):
        self.game_manager.events_manager.remove_events(self.events)
        self.game_manager.ui_manager.kill()
        self.game_manager.scenes_manager.next_scene(Game)

    def exit_button(self):
        for element_id in ui_elements:
            if element_id == 'background':
                continue
            ui_elements[element_id].move_by_easing(x=-900)
        self.quit_game = True


    def update(self):
        if self.play and self.panel.is_finished:
            self.exit()
        elif self.quit_game and self.panel.is_finished:
            pygame.quit()
            import sys
            sys.exit()


        for element in list(ui_elements.values()):
            element.update_easing()


    def draw(self):
        pass

