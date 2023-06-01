import io
from app.core.models.player_2 import MemberBombAttacks, Player_2_data


class BModule:
    def __init__(self, play_2: Player_2_data) -> None:
        self.play_2 = play_2
        self.members = self.play_2.bombs_attacks.members_bomb_attacks
        self._members_missing_bomb = self._set_members_missing_bomb()

    def _set_members_missing_bomb(self) -> list[MemberBombAttacks]:
        """filter only the members with remining bombs or attacks"""
        return [member for member in self.members if self._is_member_missing_bomb(member)]

    @property
    def _is_rest_day(self) -> bool:
        """determine if it's rest day or not"""
        return len(self._members_missing_bomb) == len(self.members)

    def _is_member_missing_bomb(self, member: MemberBombAttacks) -> bool:
        """test is member still have bomb"""
        is_no_bomb_used = member.nb_bomb_used_by_day[0] == 0

        return is_no_bomb_used

    def title(self) -> str:
        """define title of embed"""
        return "Bombes restantes aujourd'hui."

    def description(self) -> str:
        """define description of embed"""
        total_bombs_missing = len(self._members_missing_bomb)
        if self._is_rest_day:
            return "Jour de repos"
        if total_bombs_missing == 0:
            return "Toutes les bombes ont été utilisées.\n"
        description_io = io.StringIO()
        description_io.write(f"Il reste {total_bombs_missing} bombes non utilisées.\n")
        for member in self._members_missing_bomb:
            member_name = self.play_2.guild_members[member.member_id]
            description_io.write(f":bomb:  {member_name}\n")

        return description_io.getvalue()
