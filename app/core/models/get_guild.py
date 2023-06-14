from dataclasses import dataclass, field
from typing import Any
from app.core.entrypoint.json_api import JsonAPI
from app.core.models.api_solgard import ApiSolgard


@dataclass
class Member:
    member_id: str
    member_name: str
    is_clash_on: bool


@dataclass
class SetGuild:
    # init fields
    user_id: str
    session_id: str
    guild_id: str
    # fields to set
    infos_guild: dict[str, Any] = field(default_factory=dict)
    guild_name: str = None
    members: list[Member] = field(default_factory=list)
    dict_members_id_name: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self._set_infos_guild()
        self._read_for_set_infos_guild()
        self._set_dict_members_id_name()

    def _set_infos_guild(self):
        """call api endpoint for ask guild infos"""
        json_guild = JsonAPI.json_get_guild(self.guild_id)
        self.infos_guild = ApiSolgard.api_endpoint(json_guild)

    def _read_for_set_infos_guild(self):
        """extract infos from recupered json"""
        self.guild_name = self.infos_guild["eventResult"]["eventResponseData"]["guild"]["name"]

        get_members = self.infos_guild["eventResult"]["eventResponseData"]["guild"]["members"]

        for member in get_members:
            try:
                isClashOn = member["guildChallengeOptIn"]
            except KeyError:
                isClashOn = False
            self.members.append(Member(member["userId"], member["displayName"], isClashOn))

    def _set_dict_members_id_name(self):
        """make a dict for translate member_id to member_name"""
        for member in self.members:
            self.dict_members_id_name[member.member_id] = member.member_name
