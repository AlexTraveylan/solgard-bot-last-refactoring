import time
from typing import Any

from app.core.models.version import Versions


class JsonAPI:
    """
    A class for creating JSON payloads for player events in a game.

    Attributes
    ----------
    version : Versions
        An instance of the Versions class storing various version details.

    Methods
    -------
    json_player_2() -> dict[str, Any]:
        Returns a JSON payload for a GET_PLAYER_2 event.

    json_get_guild(guildId: str) -> dict[str, Any]:
        Returns a JSON payload for a VIEW_GUILD_2 event.
    """

    def __init__(self, version: Versions = Versions()) -> None:
        """
        Constructs the necessary attributes for the JsonAPI object.

        Parameters
        ----------
        version : Versions, optional
            An instance of the Versions class storing various version details (default is Versions()).
        """
        self.version = version

    def json_player_2(self) -> dict[str, Any]:
        """
        Constructs a JSON payload for a GET_PLAYER_2 event.

        Returns
        -------
        dict
            A JSON payload with the required parameters for a GET_PLAYER_2 event.
        """
        return {
            "builtInMultiConfigVersion": self.version.builtInMultiConfigVersion,
            "installId": self.version.installId,
            "playerEvent": {
                "createdOn": str(int(time.time() * 1000)),
                "gameConfigVersion": self.version.gameConfigVersion,
                "multiConfigVersion": self.version.multiConfigVersion,
                "playerEventData": {},
                "playerEventType": "GET_PLAYER_2",
                "universeVersion": self.version.universeVersion,
            },
        }

    # def json_clash_message(message: str, guild: Guild):
    #     return {
    #             "builtInMultiConfigVersion": Versions.builtInMultiConfigVersion,
    #             "installId": Versions.installId,
    #             "playerEvent": {
    #                 "createdOn": str(int(time.time()*1000)),
    #                 "gameConfigVersion": Versions.gameConfigVersion,
    #                 "multiConfigVersion": Versions.multiConfigVersion,
    #                 "playerEventData": {
    #                     "guildId": guild.id,
    #                     "message": message
    #                 },
    #                 "playerEventType": "SEND_GUILD_CHALLENGE_CHAT_MESSAGE",
    #                 "universeVersion": Versions.universeVersion
    #             }
    #         }

    # def json_guild_message(message: str, guild: Guild):
    #     return {
    #         "builtInMultiConfigVersion": Versions.builtInMultiConfigVersion,
    #         "installId": Versions.installId,
    #         "playerEvent": {
    #             "createdOn": str(int(time.time() * 1000)),
    #             "gameConfigVersion": Versions.gameConfigVersion,
    #             "multiConfigVersion": Versions.multiConfigVersion,
    #             "playerEventData": {"guildId": guild.id, "message": message},
    #             "playerEventType": "SEND_GUILD_CHAT_MESSAGE_2",
    #             "universeVersion": Versions.universeVersion,
    #         },
    #     }

    def json_get_guild(guildId: str) -> dict[str, Any]:
        """
        Constructs a JSON payload for a VIEW_GUILD_2 event.

        Parameters
        ----------
        guildId : str
            The ID of the guild to view.

        Returns
        -------
        dict
            A JSON payload with the required parameters for a VIEW_GUILD_2 event.
        """
        return {
            "builtInMultiConfigVersion": Versions.builtInMultiConfigVersion,
            "installId": Versions.installId,
            "playerEvent": {
                "createdOn": str(int(time.time() * 1000)),
                "gameConfigVersion": Versions.gameConfigVersion,
                "multiConfigVersion": Versions.multiConfigVersion,
                "playerEventData": {"guildId": guildId},
                "playerEventType": "VIEW_GUILD_2",
                "universeVersion": Versions.universeVersion,
            },
        }
