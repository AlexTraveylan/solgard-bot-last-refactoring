from dataclasses import dataclass
import pytest
from app.adapters.jsonreader import read_json
from app.core.models.connect_user import ConnectUser
from app.core.models.version import Versions


class FakeVersions(Versions):
    builtInMultiConfigVersion = "aze"
    installId = "qsd"
    gameConfigVersion = "wxc"
    multiConfigVersion = "iop"
    universeVersion = "klm"


@dataclass
class FakeConnectUser(ConnectUser):
    def __post_init__(self):
        super().__post_init__()
        self.version = FakeVersions

    def _decrypt_connect_json(self):
        FAKE_CONNECT_JSON = read_json("tests/data/connect.json")
        self._connect_json = FAKE_CONNECT_JSON


def test_set_connexion_json():
    connexion = FakeConnectUser("no_config", "no_key")
    connexion._set_connexion_json()
    assert connexion._connect_json["builtInMultiConfigVersion"] == "aze"
    assert connexion._connect_json["installId"] == "qsd"
    assert connexion._connect_json["universeVersion"] == "klm"
    assert connexion._connect_json["playerEvent"]["gameConfigVersion"] == "wxc"
    assert connexion._connect_json["playerEvent"]["multiConfigVersion"] == "iop"
    assert connexion._connect_json["playerEvent"]["playerEventData"]["clientSecret"] == "fake"
    assert connexion._connect_json["playerEvent"]["playerEventType"] == "CONNECT"


def test_set_user_id():
    connexion = FakeConnectUser("no_config", "no_key")

    assert connexion.user_id == "fakeUser"


def test_get_user_id_session_id_raise_without_nothing():
    connexion = FakeConnectUser("no_config", "no_key")

    with pytest.raises(ValueError) as exc_info:
        connexion.get_user_id_session_id()

    assert str(exc_info.value) == "You have to connect first"
