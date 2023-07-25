from dataclasses import dataclass, field
import datetime
from typing import Any, Literal
from app.adapters.date_time_fonctions import debutJourneeByTimecode, is_clash_on, is_on_day
import re
from app.core.entrypoint.json_api import JsonAPI
from app.core.models.api_solgard import ApiSolgard


DEFAULT_COUNT_DICT = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}


@dataclass
class MemberBombAttacks:
    """
    Dataclass that encapsulates the information of a guild member's bomb attacks.

    Attributes
    ----------
    member_id: str
        The id of the guild member.
    nb_bomb_used_by_day: dict[int, int]
        The number of bombs used by the guild member each day.
    nb_attacks_used_by_day: dict[int, int]
        The number of attacks used by the guild member each day.
    """

    member_id: str
    nb_bomb_used_by_day: dict[int, int] = field(default_factory=lambda: DEFAULT_COUNT_DICT.copy())
    nb_attacks_used_by_day: dict[int, int] = field(default_factory=lambda: DEFAULT_COUNT_DICT.copy())


@dataclass
class BombsAttacks:
    """
    Dataclass that encapsulates the information of bombs attacks of all members.

    Attributes
    ----------
    members_bomb_attacks: list[MemberBombAttacks]
        List of `MemberBombAttacks` instances.
    """

    members_bomb_attacks: list[MemberBombAttacks] = field(default_factory=list)

    def find_member_by_member_id(self, user_id: str):
        """
        Find and return the `MemberBombAttacks` object for a given user ID.

        Parameters
        ----------
        user_id : str
            The ID of the user.

        Returns
        -------
        MemberBombAttacks
            The `MemberBombAttacks` object of the user.

        Raises
        ------
        ValueError
            If the member was not found.
        """
        for member in self.members_bomb_attacks:
            if member.member_id == user_id:
                return member
        raise ValueError("Member not found")


@dataclass
class ClashInfo:
    """
    Dataclass that encapsulates the information of a guild clash.

    Attributes
    ----------
    saison: int
        The season of the clash.
    id_clash: str
        The id of the clash.
    opponent_guild_id: str
        The id of the opponent guild.
    team_id: int
        The team id of the clash.
    """

    saison: int
    id_clash: str
    opponent_guild_id: str
    team_id: int


@dataclass
class ClashTeam:
    """
    Dataclass that encapsulates the information of a clash team.

    Attributes
    ----------
    power: int
        The power of the clash team.
    scores: tuple[int, int]
        The scores of the clash team.
    is_killed: bool
        Whether the clash team is killed.
    """

    power: int
    scores: tuple[int, int]
    is_killed: bool


@dataclass
class PowerClash:
    """
    Dataclass that encapsulates the information of a power clash.

    Attributes
    ----------
    member_id: str
        The id of the member in the power clash.
    end_bonus: int
        The end bonus of the power clash.
    teams: list[ClashTeam]
        List of `ClashTeam` instances.
    """

    member_id: str
    end_bonus: int
    teams: list[ClashTeam] = field(default_factory=dict)


@dataclass
class Player_2_data:
    """
    Dataclass that encapsulates the information of a Player 2.

    Attributes
    ----------
    user_id: str
        The user id of the player 2.
    session_id: str
        The session id of the player 2.
    play_2_content: dict[str, Any]
        The content of the player 2.
    guild_id: str
        The id of the guild of the player 2.
    guild_name: str
        The name of the guild of the player 2.
    guild_members: dict[str, str]
        Dictionary of guild members of the player 2.
    bombs_attacks: BombsAttacks
        `BombsAttacks` instance of the player 2.
    clash_info: ClashInfo
        `ClashInfo` instance of the player 2.
    clash_event: list[dict[str, Any]]
        List of clash events of the player 2.
    ennemies_powersclash: list[PowerClash]
        List of `PowerClash` instances of the enemies of the player 2.
    allies_powersclash: list[PowerClash]
        List of `PowerClash` instances of the allies of the player 2.
    json_api: JsonAPI
        `JsonAPI` instance for the player 2.
    """

    user_id: str
    session_id: str
    # use methods for set them
    play_2_content: dict[str, any] = field(default_factory=dict)
    guild_id: str = None
    guild_name: str = None
    guild_members: dict[str, str] = field(default_factory=dict)
    bombs_attacks: BombsAttacks = field(default_factory=lambda: BombsAttacks())
    clash_info: ClashInfo = None
    clash_event: list[dict[str, Any]] = field(default_factory=list)
    ennemies_powersclash: list[PowerClash] = field(default_factory=list)
    allies_powersclash: list[PowerClash] = field(default_factory=list)
    # dependancies
    json_api = JsonAPI()

    def __post_init__(self):
        """
        Method that is run after the class is instantiated.
        It initializes various properties based on the player 2's data.
        """
        self.api_solgard = ApiSolgard(self.user_id, self.session_id)
        self._set_play_2_content()
        self._set_guild_infos()
        self._set_bombs_info()
        # clash infos
        now = datetime.datetime.utcnow()
        if is_clash_on(now):
            self._set_clash_info()
            self._set_clash_event()
            self.ennemies_powersclash = self._get_clash_power("ennemy")
            self.allies_powersclash = self._get_clash_power("ally")

    def _set_play_2_content(self) -> None:
        """
        Retrieve the player_2_content from the Solgard API and set the corresponding attribute.
        """

        json_play_2 = self.json_api.json_player_2()
        play_2_response = self.api_solgard.api_endpoint(json_play_2)
        self.play_2_content = play_2_response

    def _set_guild_infos(self):
        """
        Set guild information, including the guild ID, guild name, and a dictionary for converting
        member IDs to member names.
        """

        guild: dict[str, any] = self.play_2_content["eventResult"]["eventResponseData"]["player"]["guild"]
        self.guild_id: str = guild["guildId"]
        self.guild_name: str = guild["name"]

        members: list[dict[str, any]] = guild["members"]
        for member in members:
            member_user_id = member["userId"]
            member_name = member["displayName"]
            self.guild_members[member_user_id] = member_name
            self.bombs_attacks.members_bomb_attacks.append(MemberBombAttacks(member_user_id))

    def _set_bombs_info(self):
        """
        Set bomb and attack counts for each guild member for the past 4 days.
        """

        player = self.play_2_content["eventResult"]["eventResponseData"]["player"]
        actual_timecode: int = player["timestamp"]
        begin_day = debutJourneeByTimecode(actual_timecode)

        guildActivities: list[dict[str, any]] = player["guild"]["guildActivities"]

        for activity in guildActivities:
            member_concerned_id: str = activity["userId"]
            try:
                member_concerned: MemberBombAttacks = self.bombs_attacks.find_member_by_member_id(member_concerned_id)
            except ValueError:
                member_concerned: MemberBombAttacks = MemberBombAttacks(member_id="Unknown")

            activity_timestamp: int = activity["createdOn"]
            isBomb: bool = activity["type"] == "GUILD_BOSS_BOMB"

            if is_on_day(0, begin_day, activity_timestamp):
                if isBomb:
                    member_concerned.nb_bomb_used_by_day[0] += 1
                else:
                    member_concerned.nb_attacks_used_by_day[0] += 1

            if is_on_day(1, begin_day, activity_timestamp):
                if isBomb:
                    member_concerned.nb_bomb_used_by_day[1] += 1
                else:
                    member_concerned.nb_attacks_used_by_day[1] += 1

            if is_on_day(2, begin_day, activity_timestamp):
                if isBomb:
                    member_concerned.nb_bomb_used_by_day[2] += 1
                else:
                    member_concerned.nb_attacks_used_by_day[2] += 1

            if is_on_day(3, begin_day, activity_timestamp):
                if isBomb:
                    member_concerned.nb_bomb_used_by_day[3] += 1
                else:
                    member_concerned.nb_attacks_used_by_day[3] += 1

            if is_on_day(4, begin_day, activity_timestamp):
                if isBomb:
                    member_concerned.nb_bomb_used_by_day[4] += 1
                else:
                    member_concerned.nb_attacks_used_by_day[4] += 1

    def _set_clash_info(self):
        """
        Set the clash information from the player's guild events.
        """
        events = self.play_2_content["eventResult"]["eventResponseData"]["player"]["guild"]["sharedEvents"]["sharedEvents"]
        event = events[-1]
        saison = int(re.sub("[a-zA-Z]+_", "", event["tournamentId"]))
        id_clash = event["guildChallengeId"]
        opponent_guild_id = event["guildChallenge"]["opponentGuildId"]
        team_id = int((event["guildChallenge"]["teamId"])[-1])

        self.clash_info = ClashInfo(saison, id_clash, opponent_guild_id, team_id)

    def _get_team(self, concerned_team: Literal["ally", "ennemy"]) -> str:
        """
        Get the team ("ally" or "enemy") based on the concerned team.

        Parameters
        ----------
        concerned_team : Literal["ally", "ennemy"]
            The team of interest ("ally" or "ennemy").

        Returns
        -------
        str
            The name of the team.
        """
        if concerned_team == "ally":
            return f"team{self.clash_info.team_id}"
        else:
            return f"team{self.clash_info.team_id % 2 + 1}"

    def _set_clash_event(self):
        """
        Set the enemies' powers from the clash events of the player.
        """
        if self.clash_info is None:
            raise ValueError("use _set_clash_info first")

        liveEvents = self.play_2_content["eventResult"]["eventResponseData"]["player"]["hero"]["liveEvents"]["liveEvents"]
        i = 0
        for event in liveEvents:
            try:
                if event["type"] == "GuildChallenge":
                    break
            except:
                pass
            i += 1
        self.clash_event = liveEvents[i]["config"]["liveEventGameModes"]["guildChallenge"]

    def _get_clash_power(self, concerned_team: Literal["ally", "ennemy"]) -> list[PowerClash]:
        """
        Get the clash power for the concerned team ("ally" or "enemy").

        Parameters
        ----------
        concerned_team : Literal["ally", "ennemy"]
            The team of interest ("ally" or "ennemy").

        Returns
        -------
        list[PowerClash]
            A list of `PowerClash` objects representing the clash power of the concerned team.

        Raises
        ------
        ValueError
            If the clash event is not yet set.
        """
        if len(self.clash_event) == 0:
            raise ValueError("use _get_clash_event first")

        bouts = self.clash_event[self._get_team(concerned_team)]["bouts"]

        ennemies_powersclash: list[PowerClash] = []

        for bout in bouts:
            member_id = bout["opponent"]["userId"]
            bonus = bout["boutBonus"]
            encounters = bout["encounters"]

            clash_teams: list[ClashTeam] = []
            for encounter in encounters:
                power = encounter["duelPower"]
                scores = (encounter["duelBonus"], encounter["duelDamageScore"])
                try:
                    encounter["mostDamageEntry"]["userId"]
                    is_killed = True
                except:
                    is_killed = False
                clash_teams.append(ClashTeam(power=power, scores=scores, is_killed=is_killed))

            ennemies_powersclash.append(PowerClash(member_id=member_id, end_bonus=bonus, teams=clash_teams))

        return ennemies_powersclash
