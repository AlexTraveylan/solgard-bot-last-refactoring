from dataclasses import dataclass
from functools import reduce
from app.adapters.traductor.translation import Translate
from app.core.models.get_guild import SetGuild
from app.core.models.player_2 import Player_2_data, PowerClash
from app.ports.embed_port import EmbedPort
from app.ports.interpolated_port import InterpolatePort


@dataclass
class PowerTeam:
    """
    Class to store information about a team's power in a clash.

    Attributes
    ----------
    member_name : str
        The name of the member.
    team_number : int
        The number of the team.
    power : int
        The power of the team.
    """

    member_name: str
    team_number: int
    power: int


def reducer(acc: int, curr: PowerClash):
    """
    Function to compute the total power across all clashes.

    Parameters
    ----------
    acc : int
        The accumulator that stores the running total.
    curr : PowerClash
        The current clash.

    Returns
    -------
    int
        The updated total power across all clashes.
    """
    power = sum([team.power for team in curr.teams])

    return acc + power


class BCModule(EmbedPort):
    """
    The BCModule class is used for calculating and maintaining information about
    the powers of the allies and enemies in a clash.

    Attributes
    ----------
    _play_2 : Player_2_data
        The player's game data.
    _ennemi_guild_info : SetGuild
        Information about the enemy's guild.
    _trained_interpolate_module : InterpolatePort
        The trained model for interpolation.
    translations : dict
        The dictionary of translations.
    _ennemies_powers_list : list
        The list of enemy powers.
    _allies_powers_list : list
        The list of ally powers.
    _total_allies_powers : int
        The total power of the allies.
    _total_ennemies_powers : int
        The total power of the enemies.
    """

    def __init__(
        self, play_2: Player_2_data, ennemi_guild_info: SetGuild, trained_interpolate_module: InterpolatePort, translation_module: Translate
    ) -> None:
        """_summary_

        Parameters
        ----------
        play_2 : Player_2_data
            The player's game data.
        ennemi_guild_info : SetGuild
            Information about the enemy's guild.
        trained_interpolate_module : InterpolatePort
            The trained model for interpolation.
        translation_module : Translate
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        if not trained_interpolate_module._is_ready:
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

    def _set_total_powers(self) -> tuple[int, int]:
        """
        Sets the total power of the allies and enemies.

        Returns
        -------
        tuple[int, int]
            total for powers for respectives teams
        """
        ennemies_powers = self._play_2.ennemies_powersclash
        total_ennemies_power = reduce(reducer, ennemies_powers, 0)

        allies_powers = self._play_2.allies_powersclash
        total_allies_power = reduce(reducer, allies_powers, 0)

        return total_ennemies_power, total_allies_power

    def get_avantage(self) -> tuple[str, str]:
        """
        Computes and returns the advantage or disadvantage of the player's team.

        Returns
        -------
        tuple[str, str]
            A tuple containing the title and the percentage of advantage or disadvantage.
        """
        if self._total_allies_powers is None or self._total_ennemies_powers is None:
            raise ValueError("max powers not set yet.")

        difference_relative = (self._total_allies_powers - self._total_ennemies_powers) / self._total_allies_powers
        sign = f"{self.translations['avantage']} " if difference_relative > 0 else f"{self.translations['disavantage']} "

        return self.translations["avantage_title"], f"{sign} {abs(difference_relative) * 100:.2f}%"

    def description(self) -> str:
        """
        Returns the embed description.

        Returns
        -------
        str
            The description.
        """
        return self.translations["description"]

    def title(self) -> str:
        """
        Returns the embed title.

        Returns
        -------
        str
            The title.
        """
        return self.translations["title"]

    def _set_ennemies_powers_list(self) -> list[PowerTeam]:
        """
        Sets and returns the list of enemy powers.

        Returns
        -------
        list[PowerTeam]
            The list of enemy powers.
        """
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

    def _set_allies_powers_list(self) -> list[PowerTeam]:
        """
        Sets and returns the list of ally powers.

        Returns
        -------
        list[PowerTeam]
            The list of ally powers.
        """
        alliesPowers = self._play_2.allies_powersclash
        allies_powers_list: list[PowerTeam] = []

        for ally in alliesPowers:
            try:
                member_name = self._play_2.guild_members[ally.member_id]
            except KeyError:
                member_name = "Unknown_ally"

            three_first_powers = sorted([team.power for team in ally.teams], reverse=True)
            four_next_powers = self._trained_interpolate_module.predicate(*three_first_powers)
            seven_powers = [*three_first_powers, *four_next_powers]

            for index, power in enumerate(seven_powers):
                team_number = index + 1
                allies_powers_list.append(PowerTeam(member_name, team_number, power))

        return allies_powers_list

    def get_tuple_for_kuhn_munkres(self) -> tuple[list[PowerTeam], list[PowerTeam]]:
        """
        Returns the list of ally and enemy powers for the Kuhn-Munkres algorithm.

        Returns
        -------
        tuple[list[PowerTeam], list[PowerTeam]]
            The list of ally powers and the list of enemy powers.
        """
        if self._ennemies_powers_list is None or self._allies_powers_list is None:
            raise ValueError("Ennemies or allies are not set. Set them first.")

        return self._ennemies_powers_list, self._allies_powers_list
