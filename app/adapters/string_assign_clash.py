from app.adapters.kuhn_munkres import AssignClash


class AssignClashString:
    def __init__(self, assign_clash: list[AssignClash]) -> None:
        self.assign_clash = assign_clash

    def generate_clash_strings(self) -> list[tuple[str, str]]:
        clash_strings = []

        for ennemy_name in set(clash.ennemy_name for clash in self.assign_clash):
            clashes_for_ennemy = [
                f"{clash.ally_name} T{clash.ally_team_number} ( {'+' if (clash.ally_power - clash.ennemy_power) > 0 else '' } {clash.ally_power - clash.ennemy_power} )"
                for clash in self.assign_clash
                if clash.ennemy_name == ennemy_name
            ]

            clash_string = f"{ennemy_name}", "\n".join(f"duel {i+1} : {clash}" for i, clash in enumerate(clashes_for_ennemy))
            clash_strings.append(clash_string)

        return clash_strings
