from abc import ABC
from xml.dom.minidom import Entity

import pygame

from core.managers.events_manager import EventsManager
from core.managers.settings_manager import SettingsManager
from core.managers.ui_manager import UIManager
from managers.scenes_manager import SceneManager
from scenes.menu.menu import Menu

class Initializer(ABC):

    def __init__(self):

        self._init_settings_manager()
        self._init_pygame()
        self._init_ui_manager()
        self._init_events()
        self._init_scene()


    def _init_scene(self):
        self.scenes_manager = SceneManager(self, Menu)


    def _init_events(self):
        self.events_manager = EventsManager(self)


    def _init_settings_manager(self):
        self.settings_manager = SettingsManager()

    def _init_ui_manager(self):
        self.ui_manager = UIManager(self)


    def _init_pygame(self):
        pygame.init()
        self.running = True

        self.resolution = self.settings_manager.graphics_settings.resolution
        self.FPS = self.settings_manager.graphics_settings.fps
        self.difficulty = self.settings_manager.difficulty_settings.difficulty
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.time_delta = 0
