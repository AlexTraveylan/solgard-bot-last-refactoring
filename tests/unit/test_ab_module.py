from app.core.models.ab_module import ABModule


def test_ab_module_set_members_missing_something_on_post_init(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    assert len(ab_module._members_missing_something) == 12


def test_ab_module_set_members_missing_something(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    members_to_test = ab_module._set_members_missing_something()
    assert len(members_to_test) == 12


def test_ab_module_nb_members_is_20(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)

    assert len(ab_module.members) == 20


def test_ab_module_rest_day_false(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    assert ab_module._is_rest_day is False


def test_ab_module_is_missing(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    assert ab_module._is_rest_day is False


def test_ab_module_total_atck_11_total_bombs_12(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    total_attacks_missing, total_bombs_missing = ab_module._total_atacks_bombs_missing()
    assert total_attacks_missing == 11
    assert total_bombs_missing == 12


def test_ab_module_title_0_is_bilan_actuel(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    title = ab_module.title()
    assert "Bilan actuel" == title


def test_ab_module_title_is_recap_mardi(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=1)
    title = ab_module.title()
    assert "Recapitulatif de" in title


def test_ab_module_description_is_11a_12b(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=0)
    description = ab_module.description()
    assert description == "Attaques et bombes restantes du jour.\nIl reste au total :\n- 11 attaques\n- 12 bombes\n"


def test_ab_module_description_is_3a_2b(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=1)
    description = ab_module.description()
    assert description == "Total des attaques et bombes oubliées :\n- 3 attaques\n- 2 bombes"


def test_ab_module_embed_fields(player_2_data):
    ab_module = ABModule(play_2=player_2_data, nb_day=2)
    fields = ab_module.embed_fields()
    assert len(fields) == 2
    assert fields[0] == ("Beloune", ":bomb:\n")
    assert fields[1] == ("Djoulz", ":bomb::crossed_swords::crossed_swords:\n")
