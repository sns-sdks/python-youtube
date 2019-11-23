import json


class BaseModel:
    """ Base model class for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

    def initial(self, kwargs):
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        """ convert the data from api to model's properties. """
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c.__json = data
        return c

    def as_dict(self):
        """ Create a dictionary representation of the object. To convert all model properties. """
        data = {}
        for (key, value) in self.param_defaults.items():
            key_attr = getattr(self, key, None)
            # Notice:
            # Now have different handler to sub items
            if isinstance(key_attr, (list, tuple, set)):
                data[key] = list()
                for sub_obj in key_attr:
                    if getattr(sub_obj, 'as_dict', None):
                        data[key].append(sub_obj.as_dict())
                    else:
                        data[key].append(sub_obj)
            elif getattr(key_attr, 'as_dict', None):
                data[key] = key_attr.as_dict()
            elif key_attr is not None:
                data[key] = getattr(self, key, None)
        return data

    def as_json_string(self):
        """ Create a json string representation of the object. To convert all model properties. """
        return json.dumps(self.as_dict(), sort_keys=True)

    @classmethod
    def _get_class_name(cls):
        """ Get the current class's defined name """
        return cls.__name__

    def __repr__(self):
        """ Provide a simple repr method for model class """
        key = next(iter(self.param_defaults.keys()))
        return f"{self._get_class_name()}({key.upper()}={getattr(self, key, None)})"
