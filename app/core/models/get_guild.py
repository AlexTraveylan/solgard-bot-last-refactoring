from dataclasses import dataclass, field
from typing import Any
from app.core.entrypoint.json_api import JsonAPI
from app.core.models.api_solgard import ApiSolgard


@dataclass
class Member:
    """
    A class used to represent and manipulate a guild member.

    Attributes
    ----------
    member_id : str
        The unique identifier of the member.
    member_name : str
        The name of the member.
    is_clash_on : bool
        A flag indicating whether the clash is on for the member.
    """

    member_id: str
    member_name: str
    is_clash_on: bool


@dataclass
class SetGuild:
    """
    A class used to represent and manipulate a guild.
    Use it for get information of an ennemy guild for clash.

    Attributes
    ----------
    user_id : str
        The user ID.
    session_id : str
        The session ID.
    guild_id : str
        The guild ID.
    infos_guild : dict
        Information about the guild.
    guild_name : str
        The name of the guild.
    members : list
        The members of the guild.
    dict_members_id_name : dict
        A dictionary mapping member IDs to member names.
    """

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
        """Initialize additional attributes of the instance after it has been created."""

        self._set_infos_guild()
        self._read_for_set_infos_guild()
        self._set_dict_members_id_name()

    def _set_infos_guild(self):
        """
        Retrieve guild information from the API endpoint.
        """

        json_guild = JsonAPI.json_get_guild(self.guild_id)
        api = ApiSolgard(user_id=self.user_id, session_id=self.session_id)
        self.infos_guild = api.api_endpoint(json_guild)

    def _read_for_set_infos_guild(self):
        """
        Extract information from the obtained JSON response.
        """

        self.guild_name = self.infos_guild["eventResult"]["eventResponseData"]["guild"]["name"]

        get_members = self.infos_guild["eventResult"]["eventResponseData"]["guild"]["members"]

        for member in get_members:
            try:
                isClashOn = member["guildChallengeOptIn"]
            except KeyError:
                isClashOn = False
            self.members.append(Member(member["userId"], member["displayName"], isClashOn))

    def _set_dict_members_id_name(self):
        """
        Generate a dictionary for mapping member IDs to member names.
        """

        for member in self.members:
            self.dict_members_id_name[member.member_id] = member.member_name
