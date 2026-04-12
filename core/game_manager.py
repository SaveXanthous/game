import pygame
import pygame_gui

class GameManager:

    isInit = False

    @classmethod
    def init(cls):
        cls.isInit = True

        pygame.init()

        cls.running = True

        cls.WIDTH, cls.HEIGHT = 1280, 720
        cls.screen = pygame.display.set_mode((cls.WIDTH, cls.HEIGHT))
        cls.clock = pygame.time.Clock()

        cls.initPygameGUI()

    @classmethod
    def initPygameGUI(cls):
        cls.manager = pygame_gui.UIManager((cls.WIDTH, cls.HEIGHT))

    @classmethod
    def start(cls):
        if not cls.isInit:
            cls.init()

        while cls.running:
            time_delta = cls.clock.tick(60) / 1000.0

            cls.events()

            cls.manager.update(time_delta)

            cls.screen.fill((20, 20, 30))
            cls.manager.draw_ui(cls.screen)

            pygame.display.update()

        pygame.quit()

    @classmethod
    def stop(cls):
        cls.running = False

    @classmethod
    def events(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.stop()

            cls.manager.process_events(event)

