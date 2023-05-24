import pytest
from app.core.models.connect_user import ConnectUser
from app.core.models.version import Versions
from tests.data.connect import FAKE_CONNECT_JSON


class FakeVersions(Versions):
    builtInMultiConfigVersion = "aze"
    installId = "qsd"
    gameConfigVersion = "wxc"
    multiConfigVersion = "iop"
    universeVersion = "klm"


class FakeConnectUser(ConnectUser):
    def __init__(self):
        super().__init__()
        self._connect_json = FAKE_CONNECT_JSON
        self.version = FakeVersions


def test_set_connexion_json():
    connexion = FakeConnectUser()
    connexion._set_connexion_json()
    assert connexion._connect_json["builtInMultiConfigVersion"] == "aze"
    assert connexion._connect_json["installId"] == "qsd"
    assert connexion._connect_json["universeVersion"] == "klm"
    assert connexion._connect_json["playerEvent"]["gameConfigVersion"] == "wxc"
    assert connexion._connect_json["playerEvent"]["multiConfigVersion"] == "iop"
    assert connexion._connect_json["playerEvent"]["playerEventData"]["clientSecret"] == "fake"
    assert connexion._connect_json["playerEvent"]["playerEventType"] == "CONNECT"


def test_set_user_id():
    connexion = FakeConnectUser()
    connexion._set_user_id()

    assert connexion.user_id == "fakeUser"


def test_get_user_id_session_id_raise_without_nothing():
    connexion = FakeConnectUser()

    with pytest.raises(ValueError) as exc_info:
        connexion.get_user_id_session_id()

    assert str(exc_info.value) == "You have to connect first"


def test_get_user_id_session_id_raise_with_only_user_id():
    connexion = FakeConnectUser()
    connexion._set_user_id()

    with pytest.raises(ValueError) as exc_info:
        connexion.get_user_id_session_id()

    assert str(exc_info.value) == "You have to connect first"
