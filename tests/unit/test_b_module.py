import pytest
from app.adapters.traductor.translation import Translate
from app.core.models.b_module import BModule


@pytest.fixture(scope="module")
def translation_module():
    translation_module = Translate("fr")

    return translation_module


def test_b_module_set_members_missing_bomb_after_init(player_2_data, translation_module):
    b_module = BModule(play_2=player_2_data, translation_module=translation_module)
    assert len(b_module._members_missing_bomb) == 12


def test_b_module_is_rest_day_is_false(player_2_data, translation_module):
    b_module = BModule(play_2=player_2_data, translation_module=translation_module)
    assert b_module._is_rest_day is False


def test_b_module_title(player_2_data, translation_module):
    b_module = BModule(play_2=player_2_data, translation_module=translation_module)
    assert b_module.title() == "Bombes restantes aujourd'hui."


def test_b_module_description(player_2_data, translation_module):
    b_module = BModule(play_2=player_2_data, translation_module=translation_module)
    assert b_module.description().count(":bomb:") == 12
