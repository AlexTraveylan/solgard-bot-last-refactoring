import io
from app.adapters.traductor.translation import Translate
from app.core.models.player_2 import MemberBombAttacks, Player_2_data
from app.ports.embed_port import EmbedPort


class BModule(EmbedPort):
    """
    BModule is an implementation of the abstract EmbedPort base class.
    It generates embed data for members with remaining bombs in a game.

    Attributes
    ----------
    play_2 : Player_2_data
        The Player_2_data instance containing the game play data for the second player.
    members : list[MemberBombAttacks]
        List of MemberBombAttacks instances representing each member's bombs attacks status.
    _members_missing_bomb : list[MemberBombAttacks]
        List of MemberBombAttacks instances for each member who has remaining bombs.
    translations : dict
        The translations dictionary for "b_module" from the provided translation module.

    """

    __slots__ = ["play_2", "members", "_members_missing_bomb", "translations"]

    def __init__(self, play_2: Player_2_data, translation_module: Translate) -> None:
        """
        Initialize a BModule instance.

        Parameters
        ----------
        play_2 : Player_2_data
            The Player_2_data instance containing the game play data for the second player.
        translation_module : Translate
            The Translate instance used to manage translations for different languages.
        """
        self.play_2 = play_2
        self.members = self.play_2.bombs_attacks.members_bomb_attacks
        self._members_missing_bomb = self._set_members_missing_bomb()
        self.translations = translation_module.translations["b_module"]

    def _set_members_missing_bomb(self) -> list[MemberBombAttacks]:
        """
        Filter out the members who still have remaining bombs.

        Returns
        -------
        list[MemberBombAttacks]
            List of MemberBombAttacks instances for each member who has remaining bombs.
        """
        return [member for member in self.members if self._is_member_missing_bomb(member)]

    @property
    def _is_rest_day(self) -> bool:
        """
        Determines if it's a rest day. A rest day is when all members have used their bombs and attacks.

        Returns
        -------
        bool
            True if it's a rest day, False otherwise.
        """
        return len(self._members_missing_bomb) == len(self.members)

    def _is_member_missing_bomb(self, member: MemberBombAttacks) -> bool:
        """
        Checks if a member still has remaining bombs.

        Parameters
        ----------
        member : MemberBombAttacks
            The MemberBombAttacks instance for the member.

        Returns
        -------
        bool
            True if the member has remaining bombs, False otherwise.
        """
        is_no_bomb_used = member.nb_bomb_used_by_day[0] == 0

        return is_no_bomb_used

    def title(self) -> str:
        """
        Defines the title of the embed based on the translations provided.

        Returns
        -------
        str
            The title of the embed.
        """
        return self.translations["title"]

    def description(self) -> str:
        """
        Defines the description of the embed. The description contains information about remaining bombs and the names
        of the members who haven't used their bombs.

        Returns
        -------
        str
            The description of the embed.
        """
        total_bombs_missing = len(self._members_missing_bomb)
        if self._is_rest_day:
            return self.translations["desc_rest_day"]
        if total_bombs_missing == 0:
            return self.translations["desc_all_bombs_used"]
        description_io = io.StringIO()
        description_io.write(self.translations["desc_remaining_bombs"].format(total_bombs_missing=total_bombs_missing))
        for member in self._members_missing_bomb:
            try:
                member_name = self.play_2.guild_members[member.member_id]
            except KeyError:
                member_name = self.translations["member_unknown"]
            description_io.write(f":bomb:  {member_name}\n")

        return description_io.getvalue()
