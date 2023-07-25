from dataclasses import dataclass
from typing import Literal
from scipy.optimize import linear_sum_assignment
import numpy as np

from app.core.models.bc_module import PowerTeam


@dataclass
class AssignClash:
    """
    A dataclass that stores the result of a clash assignment.

    Parameters
    ----------
    ally_name : str
        The name of the ally.
    ally_team_number : int
        The team number of the ally.
    ally_power : int
        The power of the ally.
    ennemy_name : str
        The name of the enemy.
    ennemy_team_number : int
        The team number of the enemy.
    ennemy_power : int
        The power of the enemy.
    """

    ally_name: str
    ally_team_number: int
    ally_power: int
    ennemy_name: str
    ennemy_team_number: int
    ennemy_power: int


class KuhnMunkres:
    """
    A class to solve the assignment problem using the Hungarian (Kuhn-Munkres) algorithm.

    Parameters
    ----------
    ennemies_team : list[PowerTeam]
        The list of enemies team members.
    allies_team : list[PowerTeam]
        The list of allies team members.

    Attributes
    ----------
    ennemies_team : list[PowerTeam]
        The list of enemies team members.
    allies_team : list[PowerTeam]
        The list of allies team members.
    _allies_name : list[str]
        The list of allies names.
    _allies_powers : np.ndarray
        The array of allies powers.
    _ennemies_name : list[str]
        The list of enemies names.
    _ennemies_powers : np.ndarray
        The array of enemies powers.
    _cost_matrix : np.ndarray
        The cost matrix for the assignment problem.
    """

    __slots__ = ["ennemies_team", "allies_team", "_allies_name", "_allies_powers", "_ennemies_name", "_ennemies_powers", "_cost_matrix"]

    def __init__(self, ennemies_team: list[PowerTeam], allies_team: list[PowerTeam]) -> None:
        # initialised attributes
        self.ennemies_team = ennemies_team
        self.allies_team = allies_team
        # attributes to set
        self._allies_name, self._allies_powers = self._split_name_powers("ally")
        self._ennemies_name, self._ennemies_powers = self._split_name_powers("ennemy")
        self._cost_matrix = self._create_cost_matrix()

    def _split_name_powers(self, team: Literal["ally", "ennemy"]) -> tuple[tuple[str, int], np.ndarray]:
        """
        Split names and powers from the team members.

        Parameters
        ----------
        team : Literal["ally", "ennemy"]
            The team to split.

        Returns
        -------
        names : tuple[str, int]
            The names and team numbers of the team members.
        powers : np.ndarray
            The powers of the team members.
        """
        member_list = self.allies_team if team == "ally" else self.ennemies_team

        names: tuple[str, int] = [(member.member_name, member.team_number) for member in member_list]
        powers: np.ndarray = np.array([member.power for member in member_list])

        return names, powers

    def _create_cost_matrix(self) -> np.ndarray:
        """
        Create the cost matrix for the assignment problem.

        Returns
        -------
        cost_matrix : np.ndarray
            The cost matrix.
        """
        cost_matrix = np.zeros((len(self._ennemies_powers), len(self._allies_powers)))

        for i, ally_power in enumerate(self._ennemies_powers):
            for j, ennemy_power in enumerate(self._allies_powers):
                cost_matrix[i][j] = abs(ennemy_power - ally_power)

        return cost_matrix

    def get_results(self) -> list[AssignClash]:
        """
        Get the result of the assignment problem.

        Returns
        -------
        result_assign_list : list[AssignClash]
            The list of assignments.
        """
        enemies_index, allies_index = linear_sum_assignment(self._cost_matrix)

        result_assign_list: list[AssignClash] = []

        for ally_index, enemy_index in zip(allies_index, enemies_index):
            result_assign_list.append(
                AssignClash(
                    ally_name=self._allies_name[ally_index][0],
                    ally_team_number=self._allies_name[ally_index][1],
                    ally_power=self._allies_powers[ally_index],
                    ennemy_name=self._ennemies_name[enemy_index][0],
                    ennemy_team_number=self._ennemies_name[enemy_index][1],
                    ennemy_power=self._ennemies_powers[enemy_index],
                )
            )

        return result_assign_list
