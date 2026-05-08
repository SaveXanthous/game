import pygame
import pygame_gui
from pip._internal import resolution

from core.game_handle import GameHandle
from utils.json_handler import JSONHandler

class UIManager(GameHandle):
    def __init__(self, game_manager):
        GameHandle.__init__(self, game_manager)

        resolution = game_manager.settings_manager.graphics_settings.resolution

        self._manager = pygame_gui.UIManager(resolution)
        self.ui_elements = {}

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, value):
        self._manager = value

    def kill(self):
        for key_ui_element in self.ui_elements:
            self.ui_elements[key_ui_element].kill()

    def load_ui_from_json(self, file_path):
        data = JSONHandler.read(file_path)

        width = self.game_manager.settings_manager.graphics_settings.width
        self.ui_elements = {}

        for item in data['elements']:
            rect = self._get_ui_rect(item, width)
            ui_element = None

            if item['type'] == "UILabel":
                ui_element = self._add_ui_label(item, rect)
            elif item['type'] == "UIButton":
                ui_element = self._add_ui_button(item, rect)

            if ui_element is not None:
                self.ui_elements[item['id']] = ui_element
                print(item['id'])

        return self.ui_elements

    def _get_ui_rect(self, item,width):
        rect_dictanory= item['rect']

        rx = rect_dictanory["x"]
        ry = rect_dictanory["y"]
        rh = rect_dictanory["h"]
        rw = rect_dictanory["w"]

        rw = width if rw == -1 else rw

        rect = pygame.Rect((rx, ry), (rw, rh))
        return rect

    def _add_ui_label(self, item, rect):
        return pygame_gui.elements.UILabel(
            relative_rect=rect,
            text=item['text'],
            manager=self._manager,
            anchors=item['anchors']
        )

    def _add_ui_button(self, item, rect):
        return pygame_gui.elements.UIButton(
            relative_rect=rect,
            text=item['text'],
            manager=self._manager,
            anchors=item['anchors']
        )