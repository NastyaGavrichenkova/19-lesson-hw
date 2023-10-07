import json
from pathlib import Path

from tests import API


def load_schema(name):
    path = str(Path(API.__file__).parent.joinpath('json_schemas', f'{name}').absolute())
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
