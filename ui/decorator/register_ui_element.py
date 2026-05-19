ui_elements = {}

def register_ui_element(cls):
    original_new = cls.__new__

    def new_object(cls, *args, **kwargs):
        instance = original_new(cls)
        ui_elements[args[0]] = instance
        return instance

    cls.__new__ = new_object
    return cls