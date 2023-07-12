import json
from os import PathLike


def read_json(filePath: PathLike) -> dict[str, any]:
    with open(filePath) as file:
        data = json.load(file)
    return data
