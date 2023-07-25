import os
from matplotlib import pyplot as plt
import pandas as pd
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
        # Initialize a dictionary to organize the data
        data = {"Enemy name": [], "duel 1": [], "duel 2": [], "duel 3": []}

        # Organize the data by duel and by enemy
        for enemy_name in set(clash.ennemy_name for clash in self.assign_clash):
            # Create a list of all teams for a given enemy
            teams = [
                f"{clash.ally_name} T{clash.ally_team_number} ({clash.ally_power - clash.ennemy_power})"
                for clash in self.assign_clash
                if clash.ennemy_name == enemy_name
            ]

            # Add the teams to the correct column in the data
            data["Enemy name"].append(enemy_name)
            for i, team in enumerate(teams):
                data[f"duel {i+1}"].append(team)

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Create an image from the table
        fig, ax = plt.subplots(figsize=(12, 14))
        ax.axis("tight")
        ax.axis("off")
        the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center", bbox=[0, 0, 1, 1])

        plt.savefig(f"{output_file_path}.png")


if __name__ == "__main__":
    ally_1 = "ally_1", 1, 20000, 2, 25000, 3, 30000
    ally_2 = "ally_2", 1, 21000, 2, 26000, 4, 31000
    ennemy_1 = "Soaer", 1, 22000, 2, 27000, 3, 32000
    ennemy_2 = "机器学习在您过去3年", 1, 23000, 2, 28000, 4, 33000

    target_1 = AssignClash(ally_1[0], ally_1[1], ally_1[2], ennemy_1[0], ennemy_1[1], ennemy_1[2])
    target_2 = AssignClash(ally_2[0], ally_2[1], ally_2[2], ennemy_2[0], ennemy_2[1], ennemy_2[2])
    target_3 = AssignClash(ally_1[0], ally_1[3], ally_1[4], ennemy_2[0], ennemy_2[3], ennemy_2[4])
    target_4 = AssignClash(ally_2[0], ally_2[3], ally_2[4], ennemy_1[0], ennemy_1[3], ennemy_1[4])
    target_5 = AssignClash(ally_1[0], ally_1[5], ally_1[6], ennemy_1[0], ennemy_1[5], ennemy_1[6])
    target_6 = AssignClash(ally_1[0], ally_2[5], ally_2[6], ennemy_2[0], ennemy_2[5], ennemy_2[6])

    assign_clash = [target_1, target_2, target_3, target_4, target_5, target_6]

    file_to_send = "app/adapters/tableau.png"
    file_path, ext = os.path.splitext(file_to_send)
    print_module = PrintAssignClash(assign_clash)
    print_module.generate_table_image(file_path)
