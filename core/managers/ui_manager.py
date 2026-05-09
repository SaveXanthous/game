import pygame_gui

from game.game_handle import GameHandle
from ui.ui_scaler import UIScaler
from utils.dir_handler import DirHandler
from core.ui.ui_compiler import UICompiler
from utils.json_handler import JSONHandler


class UIManager(GameHandle):
    def __init__(self, game_manager):
        GameHandle.__init__(self, game_manager)

        resolution = game_manager.settings_manager.graphics_settings.resolution
        self._manager = pygame_gui.UIManager(resolution)

        self._ui_elements = {}

        self.ui_compiler = UICompiler(game_manager, self._manager)
        self.ui_scaler = UIScaler(game_manager)
    @property
    def manager(self):
        return self._manager

    @property
    def ui_elements(self):
        return self._ui_elements

    @manager.setter
    def manager(self, value):
        self._manager = value

    @ui_elements.setter
    def ui_elements(self, value):
        self._ui_elements = value

    def kill(self):
        for key_ui_element in self._ui_elements:
            self._ui_elements[key_ui_element].kill()

    def set_ui_json(self, path):
        self._ui_elements = self.ui_compiler.get_ui_json(path)

    def update_ui(self):
        path = JSONHandler.path_join('scenes')
        for dir in DirHandler.get_dirs(path):
            self.ui_scaler.scaled_ui(dir)
        self.kill()
        self.game_manager.scenes_manager.current_scene.init_ui()