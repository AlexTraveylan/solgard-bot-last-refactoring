from app.core.entrypoint.json_api import JsonAPI
from app.core.models.version import Versions
import pytest


class FakeVersions(Versions):
    builtInMultiConfigVersion = "aze"
    installId = "qsd"
    gameConfigVersion = "wxc"
    multiConfigVersion = "iop"
    universeVersion = "klm"


@pytest.fixture
def version():
    version = FakeVersions()
    return version


def test_json_player_2(version):
    json_api = JsonAPI(version)
    json_player_2 = json_api.json_player_2()

    assert json_player_2["builtInMultiConfigVersion"] == "aze"
    assert json_player_2["installId"] == "qsd"
    assert json_player_2["playerEvent"]["gameConfigVersion"] == "wxc"
    assert json_player_2["playerEvent"]["multiConfigVersion"] == "iop"
    assert json_player_2["playerEvent"]["universeVersion"] == "klm"
    assert json_player_2["playerEvent"]["playerEventType"] == "GET_PLAYER_2"
