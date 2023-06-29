from dataclasses import dataclass
from functools import reduce
from app.adapters.traductor.translation import Translate
from app.core.models.get_guild import SetGuild
from app.core.models.player_2 import Player_2_data, PowerClash
from app.ports.embed_port import EmbedPort
from app.ports.interpolated_port import InterpolatePort


@dataclass
class PowerTeam:
    member_name: str
    team_number: int
    power: int


def reducer(acc: int, curr: PowerClash):
    power = sum([team.power for team in curr.teams])

    return acc + power


class BCModule(EmbedPort):
    def __init__(
        self, play_2: Player_2_data, ennemi_guild_info: SetGuild, trained_interpolate_module: InterpolatePort, translation_module: Translate
    ) -> None:
        if trained_interpolate_module._is_ready:
            raise ValueError("Train first the interpolate model.")
        # given attributes
        self._play_2 = play_2
        self._ennemi_guild_info = ennemi_guild_info
        self._trained_interpolate_module = trained_interpolate_module
        # translations
        self.translations = translation_module.translations["bc_module"]
        # attributes set later
        self._ennemies_powers_list = self._set_ennemies_powers_list()
        self._allies_powers_list = self._set_allies_powers_list()
        self._total_allies_powers, self._total_ennemies_powers = self._set_total_powers()

    def _set_total_powers(self):
        ennemies_powers = self._play_2.ennemies_powersclash
        total_ennemies_power = reduce(reducer, ennemies_powers, 0)

        allies_powers = self._play_2.allies_powersclash
        total_allies_power = reduce(reducer, allies_powers, 0)

        return total_ennemies_power, total_allies_power

    def get_avantage(self) -> tuple[str, str]:
        if self._total_allies_powers is None or self._total_ennemies_powers is None:
            raise ValueError("max powers not set yet.")

        difference_relative = (self._total_allies_powers - self._total_ennemies_powers) / self._total_ennemies_powers

        return self.translations["avantage_title"], f"{difference_relative * 100:.2f}%"

    def description(self) -> str:
        return self.translations["description"]

    def title(self) -> str:
        return self.translations["title"]

    def embed_fields(self) -> list[tuple[str, str]]:
        step_1 = (self.translations["step_1_title"], self.translations["step_1_desc"])
        step_2 = (self.translations["step_2_title"], self.translations["step_2_desc"])
        step_3 = (self.translations["step_3_title"], self.translations["step_3_desc"])

        return [step_1, step_2, step_3]

    def _set_ennemies_powers_list(self):
        ennemiesPowers = self._play_2.ennemies_powersclash
        ennemies_powers_list: list[PowerTeam] = []

        for ennemy in ennemiesPowers:
            try:
                member_name = self._ennemi_guild_info.dict_members_id_name[ennemy.member_id]
            except KeyError:
                member_name = "Unknown_ennemy"

            for index, team in enumerate(ennemy.teams):
                team_number = index + 1
                power = team.power
                ennemies_powers_list.append(PowerTeam(member_name, team_number, power))

        return ennemies_powers_list

    def _set_allies_powers_list(self):
        alliesPowers = self._play_2.allies_powersclash
        allies_powers_list: list[PowerTeam] = []

        for ally in alliesPowers:
            try:
                member_name = self._play_2.guild_members[ally.member_id]
            except KeyError:
                member_name = "Unknown_ally"

            three_first_powers = sorted([team.power for team in ally.teams])
            four_next_powers = self._trained_interpolate_module.predicate(*three_first_powers)
            seven_powers = [*three_first_powers, *four_next_powers]

            for index, power in enumerate(seven_powers):
                team_number = index + 1
                allies_powers_list.append(PowerTeam(member_name, team_number, power))

        return allies_powers_list

    def get_tuple_for_kuhn_munkres(self):
        if self._ennemies_powers_list is None or self._allies_powers_list is None:
            raise ValueError("Ennemies or allies are not set. Set them first.")

        return self._ennemies_powers_list, self._allies_powers_list
