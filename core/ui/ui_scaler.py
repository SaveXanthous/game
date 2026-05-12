from game.game_handle import GameHandle
from utils.scaler import Scaler
from utils.json_handler import JSONHandler

class UIScaler(GameHandle):
    def __init__(self, game_manager):
        super().__init__(game_manager)

    def scaled_ui(self, name_scene):
        self.scaled_ui_style(name_scene, 'style_ui.json')
        self.scaled_ui_elements(name_scene, 'ui.json')

    def scaled_ui_elements(self, name_scene, name_file):
        try:
            source_path, target_path = self.__get_source_and_target_paths(name_scene, name_file)
            self.__merge_files(source_path, target_path)
            self.__scaled_ui_elements(source_path, target_path)
        except ValueError as e:
            print(e)

    def scaled_ui_style(self, name_scene, name_file):
        source_path, target_path = self.__get_source_and_target_paths(name_scene, name_file)
        self.__merge_files(source_path, target_path)
        self.__scaled_ui_style(source_path, target_path)

    
    def __get_source_and_target_paths(self, name_scene, name_file):
        source_path = JSONHandler.path_join('scenes', name_scene, 'default_ui', name_file)
        target_path = JSONHandler.path_join('scenes', name_scene, name_file)
        return source_path, target_path

    
    def __merge_files(self, source_path, target_path):
        JSONHandler.merge_files(source_path, target_path)

    
    def __scaled_ui_style(self, source_path, target_path):
        data = JSONHandler.read(source_path)
        for key_element in data:
            size = data[key_element]['font']['size']
            size = Scaler.scaled_size_front(size)
            JSONHandler.update(target_path, size, key_element, 'font', 'size')

    
    def __scaled_ui_elements(self, source_path, target_path):
        data = JSONHandler.read(source_path)

        if data == {}:
            raise ValueError(f"{UIScaler.__module__}: {source_path} is empty")

        for key_element, element in enumerate(data['elements']):
            rect = element['rect']

            rx = rect['x']
            ry = rect['y']
            rw = rect['w']
            rh = rect['h']

            rx = Scaler.scaled_x(rx)
            ry = Scaler.scaled_y(ry)
            rw = Scaler.scaled_width(rw) if rw != -1 else self.game_manager.screen.get_size()[0]
            rh = Scaler.scaled_height(rh)

            rect = {'x': rx, 'y': ry, 'w': rw, 'h': rh}

            JSONHandler.update(target_path, rect, 'elements', key_element, 'rect')