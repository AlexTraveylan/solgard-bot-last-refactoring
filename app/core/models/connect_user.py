from dataclasses import dataclass
import json
import os
import time

from dotenv import load_dotenv
from app.adapters.jsonreader import read_json
from app.core.models.api_solgard import connect_and_set_session_id
from app.core.models.version import Versions
from cryptography.fernet import Fernet


@dataclass
class ConnectUser:
    config_encrypted: str
    key: str
    user_id: str = None
    session_id: str = None
    display_name: str = None
    version = Versions
    # _connect_json = read_json("app/core/entrypoint/connect.json")

    def __post_init__(self):
        """auto set user_id"""
        self._decrypt_connect_json()
        self.user_id = self._connect_json["playerEvent"]["playerEventData"]["userId"]

    def _decrypt_connect_json(self):
        cipher_text = self.config_encrypted
        cipher_suite = Fernet(self.key)
        plain_text = cipher_suite.decrypt(cipher_text)
        self._connect_json = json.loads(plain_text.decode())

    def _set_connexion_json(self):
        """set the connexion with updated data, you have to do it before anything"""
        self._connect_json["builtInMultiConfigVersion"] = self.version.builtInMultiConfigVersion
        self._connect_json["installId"] = self.version.installId
        self._connect_json["universeVersion"] = self.version.universeVersion
        self._connect_json["playerEvent"]["createdOn"] = str(int(time.time() * 1000))
        self._connect_json["playerEvent"]["gameConfigVersion"] = self.version.gameConfigVersion
        self._connect_json["playerEvent"]["multiConfigVersion"] = self.version.multiConfigVersion

    def connect_and_get_new_session_id(self):
        """needed for all futurs requests"""
        self._set_connexion_json()
        new_session_id = connect_and_set_session_id(user_id=self.user_id, connect_json=self._connect_json)
        self.session_id = new_session_id

    def get_user_id_session_id(self):
        """util who return tupple for using in ApiSolgard class"""
        if self.user_id is None or self.session_id is None:
            raise ValueError("You have to connect first")

        return (self.user_id, self.session_id)
