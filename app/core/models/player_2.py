from dataclasses import dataclass, field
import datetime
from typing import Literal
import pytz

from app.core.entrypoint.json_api import JsonAPI
from app.core.models.api_solgard import ApiSolgard


def debutJourneeByTimecode(timecode: int) -> int:
    paris_tz = pytz.timezone('Europe/Paris')
    dt = datetime.datetime.utcfromtimestamp(timecode / 1000.0)
    dt = pytz.UTC.localize(dt).astimezone(paris_tz)  # Convert to Paris timezone

    day_start = dt.replace(hour=7, minute=0, second=0, microsecond=0)

    if dt.hour < 7:
        day_start = day_start - datetime.timedelta(days=1)

    begin_day_timestamp = int(day_start.timestamp() * 1000)

    return begin_day_timestamp



def is_on_day(nb_day_passed: Literal[0, 1, 2, 3, 4, 5], begin_day: int, actual_timestamp: int) -> bool:
    one_day_timestamp = 24 * 60 * 60 * 1000
    if nb_day_passed == 0:
        return actual_timestamp > begin_day
    else:
        return begin_day - one_day_timestamp * nb_day_passed < actual_timestamp < begin_day - one_day_timestamp * (nb_day_passed - 1)


DEFAULT_COUNT_DICT = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}


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
class Player_2_data:
    user_id: str
    session_id: str
    # use methods for set them
    play_2_content: dict[str, any] = field(default_factory=dict)
    guild_id: str = None
    guild_name: str = None
    guild_members: dict[str, str] = field(default_factory=dict)
    bombs_attacks: BombsAttacks = field(default_factory=lambda: BombsAttacks())  # TODO element 0 shloud be total
    # dependancies
    json_api = JsonAPI()

    def __post_init__(self):
        self.api_solgard = ApiSolgard(self.user_id, self.session_id)
        self._set_play_2_content()
        self._set_guild_infos()
        self._set_bombs_info()

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
        """set bombs and attacks for eatch members 5 days in the past"""

        player = self.play_2_content["eventResult"]["eventResponseData"]["player"]
        actual_timecode: int = player["timestamp"]
        begin_day = debutJourneeByTimecode(actual_timecode)

        guildActivities: list[dict[str, any]] = player["guild"]["guildActivities"]

        for activity in guildActivities:
            member_concerned_id: str = activity["userId"]
            member_concerned: MemberBombAttacks = self.bombs_attacks.find_member_by_member_id(member_concerned_id)
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

            if is_on_day(5, begin_day, activity_timestamp):
                if isBomb:
                    member_concerned.nb_bomb_used_by_day[5] += 1
                else:
                    member_concerned.nb_attacks_used_by_day[5] += 1
