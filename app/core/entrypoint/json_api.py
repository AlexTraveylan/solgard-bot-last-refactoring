import time
from typing import Any

from app.core.models.version import Versions


class JsonAPI:
    def __init__(self, version: Versions = Versions()) -> None:
        self.version = version

    def json_player_2(self) -> dict[str, Any]:
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
