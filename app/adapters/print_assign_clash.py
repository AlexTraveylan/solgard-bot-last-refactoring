from matplotlib import pyplot as plt
import pandas as pd
from app.adapters.kuhn_munkres import AssignClash


class PrintAssignClash:
    def __init__(self, assign_clash: list[AssignClash], output_directory_path: str) -> None:
        self.assign_clash = assign_clash
        self.output_directory_path = output_directory_path

    def generate_table_image(self, file_name: str):
        # Initialiser un dictionnaire pour organiser les données
        data = {"duel 1": [], "duel 2": [], "duel 3": []}

        # Organiser les données par duel et par ennemi
        for ennemy_name in set(clash.ennemy_name for clash in self.assign_clash):
            # Créer une liste de toutes les équipes pour un ennemi donné
            teams = [
                f"{clash.ally_name} T{clash.ally_team_number} ({clash.ally_power - clash.ennemy_power})"
                for clash in self.assign_clash
                if clash.ennemy_name == ennemy_name
            ]

            # Ajouter les équipes à la bonne colonne dans les données
            for i, team in enumerate(teams):
                data[f"duel {i+1}"].append(team)

        # Créer un DataFrame à partir des données
        df = pd.DataFrame(data, index=list(set(f"{' '*5}{clash.ennemy_name}{' '*5}" for clash in self.assign_clash)))

        # Crée une image à partir du tableau
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis("tight")
        ax.axis("off")
        the_table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc="center", loc="center", bbox=[0, 0, 1, 1])

        plt.savefig(f"{self.output_directory_path}/{file_name}.png")


if __name__ == "__main__":
    ally_1 = "Alex", 1, 20000, 2, 25000, 3, 30000
    ally_2 = "Miaou", 1, 21000, 2, 26000, 4, 31000
    ennemy_1 = "Soaer", 1, 22000, 2, 27000, 3, 32000
    ennemy_2 = "Mickel", 1, 23000, 2, 28000, 4, 33000

    target_1 = AssignClash(ally_1[0], ally_1[1], ally_1[2], ennemy_1[0], ennemy_1[1], ennemy_1[2])
    target_2 = AssignClash(ally_2[0], ally_2[1], ally_2[2], ennemy_2[0], ennemy_2[1], ennemy_2[2])
    target_3 = AssignClash(ally_1[0], ally_1[3], ally_1[4], ennemy_2[0], ennemy_2[3], ennemy_2[4])
    target_4 = AssignClash(ally_2[0], ally_2[3], ally_2[4], ennemy_1[0], ennemy_1[3], ennemy_1[4])
    target_5 = AssignClash(ally_1[0], ally_1[5], ally_1[6], ennemy_1[0], ennemy_1[5], ennemy_1[6])
    target_6 = AssignClash(ally_1[0], ally_2[5], ally_2[6], ennemy_2[0], ennemy_2[5], ennemy_2[6])

    assign_clash = [target_1, target_2, target_3, target_4, target_5, target_6]

    print_module = PrintAssignClash(assign_clash, "app/adapters")
    print_module.generate_table_image("tableau")
