import pygame
import pygame_gui

from event_manager import EventManager

class GameManager:

    isInit = False

    @classmethod
    def init(cls):
        cls.isInit = True

        cls.__init_pygame()
        cls.__init_pygame_gui()
        cls.__init_events()

    @classmethod
    def __init_events(cls):
        EventManager.init(GameManager = cls)

    @classmethod
    def __init_pygame(cls):
        pygame.init()

        cls.running = True

        cls.WIDTH, cls.HEIGHT = 1280, 720
        cls.screen = pygame.display.set_mode((cls.WIDTH, cls.HEIGHT))
        cls.clock = pygame.time.Clock()

    @classmethod
    def __init_pygame_gui(cls):
        cls.manager = pygame_gui.UIManager((cls.WIDTH, cls.HEIGHT))

    @classmethod
    def start(cls):
        if not cls.isInit:
            cls.init()

        while cls.running:
            time_delta = cls.clock.tick(60) / 1000.0

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

            for handler_event in EventManager.get_events(system_event):
                handler_event.process(system_event)

    @classmethod
    def get_ui_manager(cls):
        return cls.manager

