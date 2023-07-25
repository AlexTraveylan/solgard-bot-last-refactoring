import datetime
from typing import Literal
from app.adapters.date_time_fonctions import display_day_name_n_day_in_the_past
from app.adapters.traductor.translation import Translate
from app.core.models.player_2 import MemberBombAttacks, Player_2_data
from app.ports.embed_port import EmbedPort


class ABModule(EmbedPort):
    """
    The ABModule class, which is a subclass of EmbedPort, is responsible for managing the game play and statistics
    of members playing a game involving bombs and attacks.

    Parameters
    ----------
    play_2 : Player_2_data
        The Player_2_data instance containing the game play data for the second player.
    nb_day : Literal[0, 1, 2, 3, 4]
        The number of days passed since the game started. Must be between 0 and 4 inclusive.
    translation_module : Translate
        The Translate instance used to manage translations for different languages.

    Attributes
    ----------
    members : List[MemberBombAttacks]
        List of MemberBombAttacks instances for each guild member.
    lang : str
        Language used for translations.
    translations : Dict[str, Union[str, Dict[str, str]]]
        A dictionary containing translated text for ABModule.
    nb_day : Literal[0, 1, 2, 3, 4]
        The number of days passed since the game started.
    _members_missing_something : List[MemberBombAttacks]
        List of MemberBombAttacks instances for each member who has remaining bombs or attacks.
    """

    __slots__ = ["play_2", "members", "lang", "translations", "nb_day", "_members_missing_something"]

    def __init__(self, play_2: Player_2_data, nb_day: Literal[0, 1, 2, 3, 4], translation_module: Translate) -> None:
        """
        Initialize an ABModule instance.

        Parameters
        ----------
        play_2 : Player_2_data
            The Player_2_data instance containing the game play data for the second player.
        nb_day : Literal[0, 1, 2, 3, 4]
            The number of days passed since the game started. Must be between 0 and 4 inclusive.
        translation_module : Translate
            The Translate instance used to manage translations for different languages.
        """
        self.play_2 = play_2
        self.members = self.play_2.bombs_attacks.members_bomb_attacks
        self.lang = translation_module.lang
        self.translations = translation_module.translations["ab_module"]
        self.nb_day = nb_day
        self._members_missing_something: list[MemberBombAttacks] = []
        self._members_missing_something = self._set_members_missing_something()

    def _set_members_missing_something(self) -> list[MemberBombAttacks]:
        """
        Filter and return the members who still have remaining bombs or attacks.

        Returns
        -------
        list[MemberBombAttacks]
            List of MemberBombAttacks instances for each member who has remaining bombs or attacks.
        """
        return [member for member in self.members if self._is_member_missing_something(member)]

    @property
    def _is_rest_day(self) -> bool:
        """
        Determines if it's a rest day. A rest day is when all members have used their bombs and attacks.

        Returns
        -------
        bool
            True if it's a rest day, False otherwise.
        """
        return len(self._members_missing_something) == len(self.members)

    def _is_member_missing_something(self, member: MemberBombAttacks) -> bool:
        """
        Checks if a member still has remaining attacks or bombs.

        Parameters
        ----------
        member : MemberBombAttacks
            The MemberBombAttacks instance for the member.

        Returns
        -------
        bool
            True if the member has remaining attacks or bombs, False otherwise.
        """
        is_less_tant_2_attack_used = member.nb_attacks_used_by_day[self.nb_day] < 2
        is_no_bomb_used = member.nb_bomb_used_by_day[self.nb_day] == 0

        return is_less_tant_2_attack_used or is_no_bomb_used

    def _total_atacks_bombs_missing(self) -> tuple[int, int]:
        """
        Calculates and returns the total number of missing attacks and bombs.

        Returns
        -------
        tuple[int, int]
            A tuple where the first element is the total missing attacks and the second element is the total missing bombs.
        """
        total_attacks_missing = sum([(2 - attacks.nb_attacks_used_by_day[self.nb_day]) for attacks in self._members_missing_something])
        total_bombs_missing = sum([(1 - bombs.nb_bomb_used_by_day[self.nb_day]) for bombs in self._members_missing_something])

        return (total_attacks_missing, total_bombs_missing)

    def title(self) -> str:
        """
        Determines the title of the embed based on the number of days passed since the game started.

        Returns
        -------
        str
            The title of the embed.
        """
        display_name_day = display_day_name_n_day_in_the_past(datetime.datetime.utcnow(), self.nb_day, self.lang)
        if self.nb_day == 0:
            title = self.translations["title_today"]
        else:
            title = self.translations["title_past"].format(display_name_day=display_name_day)

        return title

    def description(self) -> str:
        """
        Determines the description of the embed based on the current game state.
        The description varies based on whether it's a rest day, all attacks and bombs are used,
        or there are still remaining attacks and bombs.

        Returns
        -------
        str
            The description of the embed.
        """
        if self._is_rest_day:
            return self.translations["desc_rest_day"]

        total_attacks_missing, total_bombs_missing = self._total_atacks_bombs_missing()

        if total_attacks_missing + total_bombs_missing == 0:
            return self.translations["desc_all_attacks_bombs_used"]

        if self.nb_day > 0:
            return self.translations["desc_total_attacks_bombs_missed"].format(
                total_attacks_missing=total_attacks_missing, total_bombs_missing=total_bombs_missing
            )

        return self.translations["desc_remaining_attacks_bombs_today"].format(
            total_attacks_missing=total_attacks_missing, total_bombs_missing=total_bombs_missing
        )

    def _member_field_data(self, member: MemberBombAttacks) -> tuple[str, str]:
        """
        Generates a tuple containing a member's name and their game play status.

        Parameters
        ----------
        member : MemberBombAttacks
            The MemberBombAttacks instance for the member.

        Returns
        -------
        tuple[str, str]
            A tuple where the first element is the member's name and the second element is their game play status.
        """
        try:
            member_name = self.play_2.guild_members[member.member_id]
        except KeyError:
            member_name = self.translations["member_unknown"]

        member_nb_atck = member.nb_attacks_used_by_day[self.nb_day]
        is_attack_done = member_nb_atck == 2
        if is_attack_done:
            display_atck = ""
        else:
            remaining_attacks = 2 - member_nb_atck
            display_atck = f"{':crossed_swords:' * remaining_attacks}"

        member_nb_bomb = member.nb_bomb_used_by_day[self.nb_day]
        is_bomb_done = member_nb_bomb == 1
        if is_bomb_done:
            display_bomb = ""
        else:
            display_bomb = ":bomb:"

        return (member_name, f"{display_bomb}{display_atck}\n")

    def embed_fields(self) -> list[tuple[str, str]]:
        """
        Generates a list of tuples to be used for adding fields to the embed.
        Each tuple consists of the member's name and their game play status.

        Returns
        -------
        list[tuple[str, str]]
            List of tuples for adding fields to the embed.
        """
        fields_data = []
        if self._is_rest_day:
            return fields_data

        for member in self._members_missing_something:
            field_data = self._member_field_data(member)
            fields_data.append(field_data)

        return fields_data
