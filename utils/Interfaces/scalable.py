from math import sqrt

class Scalable:
    scaled_width_coefficient = 1.0
    scaled_height_coefficient = 1.0

    @classmethod
    def set_scale(cls, current_w, current_h):
        cls.scaled_width_coefficient = current_w / 1280
        cls.scaled_height_coefficient = current_h / 720
        cls.scaled_size_front_coefficient = min(cls.scaled_width_coefficient, cls.scaled_height_coefficient)

    def scaled_width(self, value):
        value = int(value * self.scaled_width_coefficient)
        return value

    def scaled_x(self, value):
        value = int(value * self.scaled_width_coefficient)
        return value

    def scaled_height(self, value):
        value = int(value * self.scaled_height_coefficient)
        return value

    def scaled_y(self, value):
        value = int(value * self.scaled_height_coefficient)
        return value

    def scaled_size_front(self, value):
        value = int(value)
        value = int(value * self.scaled_size_front_coefficient)
        return str(value)