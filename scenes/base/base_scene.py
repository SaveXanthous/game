from abc import abstractmethod, ABC

from game.game_handle import GameHandle

from utils.json_handler import JSONHandler


class BaseScene(ABC, GameHandle):

    def __init__(self, game_manager):
        ABC.__init__(self)
        GameHandle.__init__(self, game_manager)

        self.screen = self.game_manager.screen
        self.name =  type(self).__module__.split('.')[-1]
        self.ui_elements = {}

        self.init_ui()

    def init_ui(self):
        get_path_json = lambda file : JSONHandler.path_join("scenes",  self.name, file)


        self.ui_elements = self.game_manager.ui_manager.ui_elements

    @abstractmethod
    def update(self):
        pass

    def next_scene(self, scene):
        self.game_manager.scenes_manager.next_scene(scene)