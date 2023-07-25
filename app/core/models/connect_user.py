from dataclasses import dataclass
import json
import time

from dotenv import load_dotenv
from app.adapters.jsonreader import read_json
from app.core.models.api_solgard import connect_and_set_session_id
from app.core.models.version import Versions
from cryptography.fernet import Fernet


@dataclass
class ConnectUser:
    """
    A dataclass that handles user connection and session management.

    Attributes
    ----------
    config_encrypted : str
        The encrypted user configuration.
    key : str
        The key used to decrypt the user configuration.
    user_id : str, optional
        The user's unique identifier.
    session_id : str, optional
        The session's unique identifier.
    display_name : str, optional
        The display name of the user.
    version : Versions
        The version information of the game.
    """

    config_encrypted: str
    key: str
    user_id: str = None
    session_id: str = None
    display_name: str = None
    version = Versions

    def __post_init__(self):
        """
        Automatically set the `user_id` attribute after the instance is initialized.
        """
        self._decrypt_connect_json()
        self.user_id = self._connect_json["playerEvent"]["playerEventData"]["userId"]

    def _decrypt_connect_json(self):
        """
        Decrypts the connect JSON file using the key.
        The decrypted JSON is then stored in the `_connect_json` attribute.
        """
        cipher_text = self.config_encrypted
        cipher_suite = Fernet(self.key)
        plain_text = cipher_suite.decrypt(cipher_text)
        self._connect_json = json.loads(plain_text.decode())

    def _set_connexion_json(self):
        """
        Updates the `_connect_json` attribute with the current version and timestamp information.
        This method should be called before establishing any new connections.
        """
        self._connect_json["builtInMultiConfigVersion"] = self.version.builtInMultiConfigVersion
        self._connect_json["installId"] = self.version.installId
        self._connect_json["universeVersion"] = self.version.universeVersion
        self._connect_json["playerEvent"]["createdOn"] = str(int(time.time() * 1000))
        self._connect_json["playerEvent"]["gameConfigVersion"] = self.version.gameConfigVersion
        self._connect_json["playerEvent"]["multiConfigVersion"] = self.version.multiConfigVersion

    def connect_and_get_new_session_id(self):
        """
        Establishes a new connection and updates the `session_id` attribute.
        This method should be called before making any future requests.
        """
        self._set_connexion_json()
        new_session_id = connect_and_set_session_id(user_id=self.user_id, connect_json=self._connect_json)
        self.session_id = new_session_id

    def get_user_id_session_id(self) -> tuple[str, str]:
        """
        Returns a tuple of user_id and session_id.

        Returns
        -------
        tuple
            A tuple of the form (user_id, session_id).

        Raises
        ------
        ValueError
            If the user_id or session_id attribute is not set (i.e., is None), this method raises a ValueError.
        """
        if self.user_id is None or self.session_id is None:
            raise ValueError("You have to connect first")

        return (self.user_id, self.session_id)
