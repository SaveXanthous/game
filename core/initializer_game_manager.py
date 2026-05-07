from abc import ABC

import pygame
import pygame_gui
from core.managers.events_manager import EventsManager
from core.managers.settings_manager import SettingsManager
from managers.scenes_manager import SceneManager
from scenes.game.game import Game

class Initializer(ABC):
    
    def __init__(self):

        self._init_settings_manager()
        self._init_pygame()
        self._init_pygame_gui()
        self._init_events()
        self._init_scene()


    def _init_scene(self):
        self.scenes_manager = SceneManager(self)

    
    def _init_events(self):
        self.events_manager = EventsManager(self)

    
    def _init_settings_manager(self):
        self.settings_manager = SettingsManager()

    
    def _init_pygame(self):
        pygame.init()
        self.running = True
        self.resolution = self.settings_manager.graphics_settings.resolution
        self.FPS = self.settings_manager.graphics_settings.fps
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.time_delta = 0


    
    def _init_pygame_gui(self):
        self.manager_ui = pygame_gui.UIManager(self.resolution)
        