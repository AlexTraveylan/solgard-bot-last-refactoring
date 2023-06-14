from dataclasses import dataclass, field
from app.adapters.date_time_fonctions import debutJourneeByTimecode, is_on_day
import re
from app.core.entrypoint.json_api import JsonAPI
from app.core.models.api_solgard import ApiSolgard


DEFAULT_COUNT_DICT = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}


@dataclass
class MemberBombAttacks:
    member_id: str
    nb_bomb_used_by_day: dict[int, int] = field(default_factory=lambda: DEFAULT_COUNT_DICT.copy())
    nb_attacks_used_by_day: dict[int, int] = field(default_factory=lambda: DEFAULT_COUNT_DICT.copy())


@dataclass
class BombsAttacks:
    members_bomb_attacks: list[MemberBombAttacks] = field(default_factory=list)

    def find_member_by_member_id(self, user_id: str):
        for member in self.members_bomb_attacks:
            if member.member_id == user_id:
                return member
        raise ValueError("Member not found")


@dataclass
class ClashInfo:
    saison: int
    id_clash: str
    opponent_guild_id: str
    team_id: int


@dataclass
class Player_2_data:
    user_id: str
    session_id: str
    # use methods for set them
    play_2_content: dict[str, any] = field(default_factory=dict)
    guild_id: str = None
    guild_name: str = None
    guild_members: dict[str, str] = field(default_factory=dict)
    bombs_attacks: BombsAttacks = field(default_factory=lambda: BombsAttacks())
    clash_info: ClashInfo = None
    # dependancies
    json_api = JsonAPI()

    def __post_init__(self):
        self.api_solgard = ApiSolgard(self.user_id, self.session_id)
        self._set_play_2_content()
        self._set_guild_infos()
        self._set_bombs_info()
        self._set_clash_info()

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
            self.bombs_attacks.members_bomb_attacks.append(MemberBombAttacks(member_user_id))

    def _set_bombs_info(self):
        """set bombs and attacks for eatch members 4 days in the past"""

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
        """set clash info"""
        events = self.play_2_content["eventResult"]["eventResponseData"]["player"]["guild"]["sharedEvents"]["sharedEvents"]
        event = events[-1]
        saison = int(re.sub("[a-zA-Z]+_", "", event["tournamentId"]))
        id_clash = event["guildChallengeId"]
        opponent_guild_id = event["guildChallenge"]["opponentGuildId"]
        team_id = int(event["guildChallenge"]["teamId"])

        self.clash_info = ClashInfo(saison, id_clash, opponent_guild_id, team_id)
