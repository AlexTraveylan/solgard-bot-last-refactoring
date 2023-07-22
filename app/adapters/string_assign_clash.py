from app.adapters.kuhn_munkres import AssignClash


class AssignClashString:
    def __init__(self, assign_clash: list[AssignClash]) -> None:
        self.assign_clash = assign_clash

    def generate_clash_strings(self) -> list[tuple[str, str]]:
        clash_strings: list[tuple[str, str]] = []

        for ennemy_name in set(clash.ennemy_name for clash in self.assign_clash):
            clashes_for_ennemy = [
                f"{clash.ally_name} T{clash.ally_team_number} ( {'+' if (clash.ally_power - clash.ennemy_power) > 0 else '-' } {abs(clash.ally_power - clash.ennemy_power)} )"
                for clash in self.assign_clash
                if clash.ennemy_name == ennemy_name
            ]

            clash_string = f"{ennemy_name}", "\n".join(f"duel {i+1} : {clash}" for i, clash in enumerate(clashes_for_ennemy))
            clash_strings.append(clash_string)

        return clash_strings

    def generate_allies_side_clash_strings(self) -> list[tuple[str, str]]:
        clash_strings: list[tuple[str, str]] = []

        for ally_name in set(clash.ally_name for clash in self.assign_clash):
            clashes_for_ally = [
                (
                    clash,
                    f"{clash.ennemy_name} T{clash.ennemy_team_number} ( {'+' if (clash.ennemy_power - clash.ally_power) > 0 else '-' } {abs(clash.ennemy_power - clash.ally_power)} )",
                )
                for clash in self.assign_clash
                if clash.ally_name == ally_name
            ]

            clash_string = f"{ally_name}", "\n".join(f"duel {ally.ally_team_number} : {clash}" for ally, clash in clashes_for_ally)

            clash_strings.append(clash_string)

        return clash_strings
