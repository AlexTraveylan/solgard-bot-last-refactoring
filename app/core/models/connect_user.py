from dataclasses import dataclass
import time
from app.core.entrypoint.connect import CONNECT_JSON
from app.core.models.api_solgard import ApiSolgard
from app.core.models.version import Versions


@dataclass
class ConnectUser:
    user_id: str = None
    session_id: str = None
    display_name: str = None
    version = Versions
    _connect_json = CONNECT_JSON

    def _set_connexion_json(self):
        """set the connexion with updated data, you have to do it before anything"""
        self._connect_json["builtInMultiConfigVersion"] = self.version.builtInMultiConfigVersion
        self._connect_json["installId"] = self.version.installId
        self._connect_json["universeVersion"] = self.version.universeVersion
        self._connect_json["playerEvent"]["createdOn"] = str(int(time.time() * 1000))
        self._connect_json["playerEvent"]["gameConfigVersion"] = self.version.gameConfigVersion
        self._connect_json["playerEvent"]["multiConfigVersion"] = self.version.multiConfigVersion

    def _set_user_id(self):
        """set the user_id, you have to do it before anything"""
        self.user_id = self._connect_json["playerEvent"]["playerEventData"]["userId"]

    def connect(self):
        """request the game api for get and set session_id, needed for all futurs requests"""
        self._set_user_id()
        self._set_connexion_json()
        api = ApiSolgard(self.user_id)
        new_session_id = api.connect_and_set_session_id(connect_json=self._connect_json)
        self.session_id = new_session_id

    def get_user_id_session_id(self):
        """util who return tupple for using in ApiSolgard class"""
        if self.user_id is None or self.session_id is None:
            raise ValueError("You have to connect first")

        return self.user_id, self.session_id
