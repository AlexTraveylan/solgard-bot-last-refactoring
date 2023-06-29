import datetime
from typing import Literal
from app.adapters.date_time_fonctions import display_day_name_n_day_in_the_past
from app.adapters.traductor.translation import Translate
from app.core.models.player_2 import MemberBombAttacks, Player_2_data
from app.ports.embed_port import EmbedPort


class ABModule(EmbedPort):
    def __init__(self, play_2: Player_2_data, nb_day: Literal[0, 1, 2, 3, 4], translation_module: Translate) -> None:
        self.play_2 = play_2
        self.members = self.play_2.bombs_attacks.members_bomb_attacks
        self.lang = translation_module.lang
        self.translations = translation_module.translations["ab_module"]
        self.nb_day = nb_day
        self._members_missing_something: list[MemberBombAttacks] = []
        self._members_missing_something = self._set_members_missing_something()

    def _set_members_missing_something(self) -> list[MemberBombAttacks]:
        """filter only the members with remining bombs or attacks"""
        return [member for member in self.members if self._is_member_missing_something(member)]

    @property
    def _is_rest_day(self) -> bool:
        """determine if it's rest day or not"""
        return len(self._members_missing_something) == len(self.members)

    def _is_member_missing_something(self, member: MemberBombAttacks) -> bool:
        """test is member still have attacks or bombs"""
        is_less_tant_2_attack_used = member.nb_attacks_used_by_day[self.nb_day] < 2
        is_no_bomb_used = member.nb_bomb_used_by_day[self.nb_day] == 0

        return is_less_tant_2_attack_used or is_no_bomb_used

    def _total_atacks_bombs_missing(self) -> tuple[int, int]:
        """calculate and return total missing attacks and bombs as tuple"""
        total_attacks_missing = sum([(2 - attacks.nb_attacks_used_by_day[self.nb_day]) for attacks in self._members_missing_something])
        total_bombs_missing = sum([(1 - bombs.nb_bomb_used_by_day[self.nb_day]) for bombs in self._members_missing_something])

        return (total_attacks_missing, total_bombs_missing)

    def title(self) -> str:
        """define title of embed"""
        display_name_day = display_day_name_n_day_in_the_past(datetime.datetime.utcnow(), self.nb_day, self.lang)
        if self.nb_day == 0:
            title = self.translations["title_today"]
        else:
            title = self.translations["title_past"].format(display_name_day=display_name_day)

        return title

    def description(self) -> str:
        """define description of embed"""
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
        """return tuple name=member_name and value=bomb_atcks for embed.add_field()"""
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
        """return value, name list tuple for embed.add_field()"""
        fields_data = []
        if self._is_rest_day:
            return fields_data

        for member in self._members_missing_something:
            field_data = self._member_field_data(member)
            fields_data.append(field_data)

        return fields_data
