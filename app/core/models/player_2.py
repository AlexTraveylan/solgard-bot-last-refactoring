from dataclasses import dataclass, field

from app.core.entrypoint.json_api import JsonAPI
from app.core.models.api_solgard import ApiSolgard


@dataclass
class Player_2_data:
    user_id: str
    session_id: str
    # use methods for set them
    play_2_content: dict[str, any] = None
    guild_id: str = None
    guild_name: str = None
    guild_members: dict[str, str] = field(default_factory=dict)
    # dependancies
    json_api = JsonAPI()

    def __post_init__(self):
        self.api_solgard = ApiSolgard(self.user_id, self.session_id)
        self._set_play_2_content()
        self._set_guild_infos()

    def _set_play_2_content(self) -> None:
        """get the player_2_content from solgard_api and set it"""

        json_play_2 = self.json_api.json_player_2()
        play_2_response = self.api_solgard.api_endpoint(json_play_2)
        self.play_2_content = play_2_response

    def _set_guild_infos(self):
        """set guild infos, guild_id, guild_name and set a dict for convert member_id to member_name"""

        guild: dict[str, any] = self.play_2_content["eventResult"]["eventResponseData"]["player"]["guild"]
        self.guild_id: str = guild["guildId"]
        self.guild_name: str = guild["name"]

        members: list[dict[str, any]] = guild["members"]
        for member in members:
            member_user_id = member["userId"]
            member_name = member["displayName"]
            self.guild_members[member_user_id] = member_name
