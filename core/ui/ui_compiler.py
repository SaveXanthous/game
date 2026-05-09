import pygame
import pygame_gui

from game.game_handle import GameHandle
from utils.json_handler import JSONHandler


class UICompiler(GameHandle):
    def __init__(self, game_manager,manager):
        GameHandle.__init__(self, game_manager)
        self._manager = manager

    def get_ui_json(self, path):
        data = JSONHandler.read(path)

        width = self.game_manager.settings_manager.graphics_settings.width
        ui_elements = {}

        for item in data['elements']:
            rect = self.__get_ui_rect(item, width)
            ui_element = None

            if item['type'] == "UILabel":
                ui_element = self.__add_ui_label(item, rect)
            elif item['type'] == "UIButton":
                ui_element = self.__add_ui_button(item, rect)

            if ui_element is not None:
                ui_elements[item['id']] = ui_element

        return ui_elements


    
    def __get_ui_rect(self, item,width):
        rect_dictionary= item['rect']

        rx = rect_dictionary["x"]
        ry = rect_dictionary["y"]
        rh = rect_dictionary["h"]
        rw = rect_dictionary["w"]

        rw = width if rw == -1 else rw

        rect = pygame.Rect((rx, ry), (rw, rh))
        return rect


    
    def __add_ui_label(self, item, rect):
        return pygame_gui.elements.UILabel(
            relative_rect=rect,
            text=item['text'],
            manager=self._manager,
            anchors=item['anchors']
        )


    
    def __add_ui_button(self, item, rect):
        return pygame_gui.elements.UIButton(
            relative_rect=rect,
            text=item['text'],
            manager=self._manager,
            anchors=item['anchors']
        )