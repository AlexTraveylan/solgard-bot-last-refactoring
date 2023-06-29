from dataclasses import dataclass
from functools import reduce
from typing import Any
from app.adapters.traductor.translation import Translate
from app.core.models.get_guild import SetGuild

from app.core.models.player_2 import Player_2_data
from app.ports.embed_port import EmbedPort


@dataclass
class ClashStatut:
    user_name: str
    num_attempts: int
    accumulated_score: int
    fortification: int
    is_spectator: bool = False


class InfoClashModule(EmbedPort):
    def __init__(self, team_number: int, play_2: Player_2_data, ennemi_guild_info: SetGuild, translation_module: Translate) -> None:
        # attrib init
        self.team_number = team_number
        self.play_2 = play_2
        self.ennemi_guild_info = ennemi_guild_info
        self.translations = translation_module.translations["info_clash_module"]
        # attrib calculate
        self.total_dict = {**self.play_2.guild_members, **self.ennemi_guild_info.dict_members_id_name}
        self.team = self._define_team()
        self.live_event_index = self._recup_live_events_index()
        self.clash_data = self._recup_clash_data()
        self.clash_members_statuts = self._define_clash_members_statuts()

    def title(self) -> str:
        return self.translations["title"]

    def description(self) -> str:
        filtered_members_statuts = [member for member in self.clash_members_statuts if not member.is_spectator]
        remining_atck = reduce(lambda acc, curr: acc + 7 - curr.num_attempts, filtered_members_statuts, 0)
        accumulate_score = reduce(lambda acc, curr: acc + curr.accumulated_score, self.clash_members_statuts, 0)

        return f"{self.translations['desc_total_remaining_attacks'].format(remining_atck=remining_atck)}\n{self.translations['desc_cumulative_score'].format(accumulate_score=accumulate_score)}\n"

    def embed_fields(self) -> list[tuple[str, str]]:
        filter_clash_members_statuts = [member for member in self.clash_members_statuts if not member.is_spectator]
        sorted_clash_members_statuts = sorted(filter_clash_members_statuts, key=lambda member: (member.num_attempts, member.accumulated_score))
        embed_data = []
        for member_statut in sorted_clash_members_statuts:
            member_name = member_statut.user_name
            if member_statut.num_attempts != 7:
                value = f"{':crossed_swords:' * (7 - member_statut.num_attempts)}\n"
                value += f"{self.translations['desc_current_score'].format(current_score=member_statut.accumulated_score)}\n"
            else:
                value = f"{self.translations['desc_final_score'].format(final_score=member_statut.accumulated_score)}\n"
            embed_data.append((member_name, value))

        return embed_data

    def _define_team(self) -> str:
        if self.team_number == 0:
            return f"team{self.play_2.clash_info.team_id}"
        else:
            return f"team{self.play_2.clash_info.team_id % 2 + 1}"

    def _recup_live_events_index(self) -> int:
        live_events = self.play_2.play_2_content["eventResult"]["eventResponseData"]["player"]["hero"]["liveEvents"]["liveEvents"]
        i = 0
        for event in live_events:
            try:
                if event["type"] == "GuildChallenge":
                    break
            except:
                pass
            i += 1

        return i

    def _recup_clash_data(self) -> list[dict[str, Any]]:
        live_events = self.play_2.play_2_content["eventResult"]["eventResponseData"]["player"]["hero"]["liveEvents"]["liveEvents"]
        guild = live_events[self.live_event_index]["config"]["liveEventGameModes"]["guildChallenge"][self.team]

        return guild["teamMembers"]

    def _define_clash_members_statuts(self) -> list[ClashStatut]:
        clash_members_statuts: list[ClashStatut] = []
        for data in self.clash_data:
            user_name = self.total_dict[data["userId"]]
            try:
                num_attempts = data["numAttempts"]
            except KeyError:
                num_attempts = 0
            try:
                accumulated_score = data["accumulatedScore"]
            except KeyError:
                accumulated_score = 0
            try:
                fortification = data["fortification"]
            except KeyError:
                fortification = 0
            try:
                is_spectator = data["spectator"]
            except KeyError:
                is_spectator = False
            clash_members_statuts.append(ClashStatut(user_name, num_attempts, accumulated_score, fortification, is_spectator))

        return clash_members_statuts
