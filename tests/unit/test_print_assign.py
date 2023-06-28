import os
import tempfile
import pytest

from app.adapters.kuhn_munkres import AssignClash
from app.adapters.print_assign_clash import PrintAssignClash
from app.adapters.string_assign_clash import AssignClashString


@pytest.fixture
def assign_clash():
    ally_1 = "a", 1, 20000, 2, 25000, 3, 30000
    ally_2 = "b", 1, 21000, 2, 26000, 4, 31000
    ennemy_1 = "c", 1, 22000, 2, 27000, 3, 32000
    ennemy_2 = "d", 1, 23000, 2, 28000, 4, 33000

    target_1 = AssignClash(ally_1[0], ally_1[1], ally_1[2], ennemy_1[0], ennemy_1[1], ennemy_1[2])
    target_2 = AssignClash(ally_2[0], ally_2[1], ally_2[2], ennemy_2[0], ennemy_2[1], ennemy_2[2])
    target_3 = AssignClash(ally_1[0], ally_1[3], ally_1[4], ennemy_2[0], ennemy_2[3], ennemy_2[4])
    target_4 = AssignClash(ally_2[0], ally_2[3], ally_2[4], ennemy_1[0], ennemy_1[3], ennemy_1[4])
    target_5 = AssignClash(ally_1[0], ally_1[5], ally_1[6], ennemy_1[0], ennemy_1[5], ennemy_1[6])
    target_6 = AssignClash(ally_1[0], ally_2[5], ally_2[6], ennemy_2[0], ennemy_2[5], ennemy_2[6])

    return [target_1, target_2, target_3, target_4, target_5, target_6]


def test_generate_table_image(assign_clash):
    with tempfile.TemporaryDirectory() as temp_dir:
        print_module = PrintAssignClash(assign_clash, temp_dir)
        print_module.generate_table_image("test_tab")
        os.path.exists(f"{temp_dir}/test_tab")


def test_assign_clash_string(assign_clash):
    print_module = AssignClashString(assign_clash)

    result_list_tuple = print_module.generate_clash_strings()

    assert len(result_list_tuple) == 2
    assert all([isinstance(result, tuple) for result in result_list_tuple])
