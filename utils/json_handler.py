import json
import os

class JSONHandler:
    @staticmethod
    def read(file_path):
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при чтении {file_path}: {e}")
            return {}

    @staticmethod
    def write(file_path, data, indent=4):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except IOError as e:
            print(f"Ошибка при записи в {file_path}: {e}")
            return False

    @staticmethod
    def update(file_path, key, value):
        data = JSONHandler.read(file_path)
        data[key] = value
        return JSONHandler.write(file_path, data)

    @staticmethod
    def get_by_key(file_path, key):
        data = JSONHandler.read(file_path)
        return data[key]

    @staticmethod
    def path_join(*paths):
        return os.path.join(*paths)