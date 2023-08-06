import os
from matplotlib import pyplot as plt
from app.adapters.kuhn_munkres import AssignClash


class PrintAssignClash:
    """
    A class to create a table image of assigned clashes.

    ...

    Attributes
    ----------
    assign_clash : list[AssignClash]
        A list of assigned clashes.

    Methods
    -------
    generate_table_image(output_file_path: str)
        Generate a table image from the assigned clashes and save it to the specified file path.
    """

    def __init__(self, assign_clash: list[AssignClash]) -> None:
        """
        Construct all the necessary attributes for the PrintAssignClash object.

        Parameters
        ----------
        assign_clash : list[AssignClash]
            A list of assigned clashes.
        """

        self.assign_clash = assign_clash

    def generate_table_image(self, output_file_path: str):
        """
        Generate a table image from the assigned clashes and save it to the specified file path.

        The table contains information about the enemy, and the allies they are matched with in each duel.
        Each cell contains the name of the ally, their team number, and the difference in power between
        the ally and the enemy.

        Parameters
        ----------
        output_file_path : str
            The path (excluding file extension) where the output image will be saved.
        """

        # Initialize the table headers
        headers = ["Enemy name", "duel 1", "duel 2", "duel 3"]
        table_data = [headers]

        # Organize the data by duel and by enemy
        for enemy_name in set(clash.ennemy_name for clash in self.assign_clash):
            row_data = [enemy_name]

            # Create a list of all teams for a given enemy
            teams = [
                f"{clash.ally_name} T{clash.ally_team_number} ({clash.ally_power - clash.ennemy_power})"
                for clash in self.assign_clash
                if clash.ennemy_name == enemy_name
            ]

            row_data.extend(teams)
            table_data.append(row_data)

        # Create an image from the table
        fig, ax = plt.subplots(figsize=(12, 14))
        ax.axis("tight")
        ax.axis("off")
        the_table = ax.table(cellText=table_data, cellLoc="center", loc="center", bbox=[0, 0, 1, 1])

        plt.savefig(f"{output_file_path}.png")
