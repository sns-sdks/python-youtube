import json


class BaseModel(object):
    """ Base model class  for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

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
            data[key] = getattr(self, key, None)
        return data

    def as_json_string(self):
        """ Create a json string representation of the object. To convert all model properties. """
        return json.dumps(self.as_dict(), sort_keys=True)
