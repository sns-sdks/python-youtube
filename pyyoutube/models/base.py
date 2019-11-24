from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class BaseModel(DataClassJsonMixin):
    """ Base model class for instance use. """

    ...
