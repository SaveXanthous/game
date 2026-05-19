from game.game_handle import GameHandle
from ui.decorator.register_ui_element import ui_elements

class UIManager(GameHandle):
    def __init__(self, game_manager):
        GameHandle.__init__(self, game_manager)

    @property
    def ui_elements(self):
        return ui_elements

    def kill(self):
        ui_elements.clear()

    def draw(self):
        for id in ui_elements:
            ui_elements[id].draw(self.game_manager.screen)
