import pygame
import pygame_gui
from core.managers.event_manager import EventManager
from core.managers.settings_manager import SettingsManager

class InitializerGameManager:
    
    def __init__(self,game_manager):
        self._game_manager = game_manager

        self._init_settings_manager()
        self._init_pygame()
        self._init_pygame_gui()
        self._init_events()

    
    def _init_events(self):
        self._game_manager.event_manager = EventManager(self._game_manager)

    
    def _init_settings_manager(self):
        self._game_manager.settings_manager = SettingsManager()

    
    def _init_pygame(self):
        pygame.init()
        self._game_manager.running = True

        self._game_manager.resolution = self._game_manager.settings_manager.graphics_settings.resolution
        self._game_manager.FPS = self._game_manager.settings_manager.graphics_settings.fps
        self._game_manager.screen = pygame.display.set_mode(self._game_manager.resolution)
        self._game_manager.clock = pygame.time.Clock()


    
    def _init_pygame_gui(self):
        self._game_manager.manager = pygame_gui.UIManager(self._game_manager.resolution)
        