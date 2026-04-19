import pygame
import pygame_gui
from core.managers.event_manager import EventManager
from core.managers.settings_manager import SettingsManager

class GameManager:

    isInit = False

    @classmethod
    def init(cls):
        cls.isInit = True

        cls.__init_settings_manager()
        cls.__init_pygame()
        cls.__init_pygame_gui()
        cls.__init_events()

    @classmethod
    def __init_events(cls):
        cls.event_manager = EventManager(cls)

    @classmethod
    def __init_settings_manager(cls):
        cls.settings_manager = SettingsManager()

    @classmethod
    def __init_pygame(cls):
        pygame.init()
        cls.running = True
        cls.__init_screen()

    @classmethod
    def __init_screen(cls):
        cls.resolution = cls.settings_manager.graphics_settings.resolution
        cls.FPS = cls.settings_manager.graphics_settings.fps
        cls.screen = pygame.display.set_mode(cls.resolution)
        cls.clock = pygame.time.Clock()


    @classmethod
    def __init_pygame_gui(cls):
        cls.manager = pygame_gui.UIManager(cls.resolution)

    @classmethod
    def start(cls):
        if not cls.isInit:
            cls.init()

        while cls.running:
            time_delta = cls.clock.tick(cls.FPS) / 1000.0

            cls.process_events()

            cls.manager.update(time_delta)

            cls.screen.fill((20, 20, 30))
            cls.manager.draw_ui(cls.screen)

            pygame.display.update()

        pygame.quit()

    @classmethod
    def stop(cls):
        cls.running = False

    @classmethod
    def process_events(cls):
        for system_event in pygame.event.get():
            cls.manager.process_events(system_event)

            for handler_event in cls.event_manager.events:
                handler_event.process(system_event)

    @classmethod
    def get_ui_manager(cls):
        return cls.manager

