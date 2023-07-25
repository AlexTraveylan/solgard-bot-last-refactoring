from dataclasses import dataclass


@dataclass
class Versions:
    """
    A dataclass representing different versions of the game.

    Attributes
    ----------
    builtInMultiConfigVersion : str
        The built-in multi configuration version.
    installId : str
        The installation ID of the game.
    gameConfigVersion : str
        The game configuration version.
    multiConfigVersion : str
        The multi configuration version.
    universeVersion : str
        The universe version of the game.
    """

    builtInMultiConfigVersion = "54fd9362992aa47894ee93f719be78b1"
    installId = "63da37e2-940e-4fc1-b379-d072078c4e22"
    gameConfigVersion = "FC79E8B283D49540120556BE823BDC35"
    multiConfigVersion = "54fd9362992aa47894ee93f719be78b1"
    universeVersion = "52AB1265BA18205FFD9D57B2274317D8"
