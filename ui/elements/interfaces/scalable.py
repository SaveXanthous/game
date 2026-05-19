class Scalable:
    width_ratio = 1.0
    height_ratio = 1.0
    font_ratio = 1.0

    @classmethod
    def set_scale(cls, current_w, current_h):
        cls.width_ratio = current_w / 1280
        cls.height_ratio = current_h / 720
        cls.font_ratio = min(cls.width_ratio, cls.height_ratio)

    
    def scaled_width(self, value):
        value = int(value * self.width_ratio)
        return value

    
    def scaled_x(self, value):
        value = int(value * self.width_ratio)
        return value

    
    def scaled_height(self, value):
        value = int(value * self.height_ratio)
        return value

    
    def scaled_y(self, value):
        value = int(value * self.height_ratio)
        return value

    
    def scaled_size_front(self, value):
        value = int(value)
        value = int(value * self.font_ratio)
        return str(value)