import json
from os import PathLike


def read_json(filePath: PathLike) -> dict[str, any]:
    """Reads and parses a JSON file and returns its contents as a dictionary.

    Parameters
    ----------
    filePath : PathLike
        The path to the JSON file.

    Returns
    -------
    dict[str, any]
        A dictionary containing the parsed JSON data.
    """
    with open(filePath) as file:
        data = json.load(file)
    return data
