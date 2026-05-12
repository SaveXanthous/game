from scenes.base.base_scene import BaseScene
from scenes.menu.events import MenuEvents


class Menu(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        game_manager.events_manager.add_events(MenuEvents(game_manager, self))

    def update(self):
        pass

    def draw(self):
        pass

