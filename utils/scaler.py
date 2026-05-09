class Scaler:
    width_ratio = 1.0
    height_ratio = 1.0
    font_ratio = 1.0

    @classmethod
    def set_scale(cls, current_w, current_h):
        cls.width_ratio = current_w / 1280
        cls.height_ratio = current_h / 720
        cls.font_ratio = min(cls.width_ratio, cls.height_ratio)

    @classmethod
    def scaled_width(cls, value):
        value = int(value * cls.width_ratio)
        return value

    @classmethod
    def scaled_x(cls, value):
        value = int(value * cls.width_ratio)
        return value

    @classmethod
    def scaled_height(cls, value):
        value = int(value * cls.height_ratio)
        return value

    @classmethod
    def scaled_y(cls, value):
        value = int(value * cls.height_ratio)
        return value

    @classmethod
    def scaled_size_front(cls, value):
        value = int(value)
        value = int(value * cls.font_ratio)
        return str(value)