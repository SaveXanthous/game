import pygame
import pygame_gui

from core.events.base_events import BaseEvents
from scenes.game.game import Game

class MenuEvents(BaseEvents):
    def process(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.scene.ui_elements['play_button']:
                self.game_manager.ui_manager.update_ui()
            if event.ui_element == self.scene.ui_elements['settings_button']:
                self.game_manager.events_manager.remove_events(self)
                self.game_manager.ui_manager.kill()
                self.scene.next_scene(Game)

        self.game_manager.ui_manager.manager.process_events(event)