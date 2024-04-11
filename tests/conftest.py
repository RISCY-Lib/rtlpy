##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2024, RISCY-Lib Contributors                             #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

import pytest
import json

from rtlpy.memory import Field, Register

@pytest.fixture(scope="module")
def simple_field():
    return Field(name="simple_field")


@pytest.fixture(scope="module")
def full_field_definition():
    return {
        "name": "abacadabra",
        "size": 4,
        "access": "WC",
        "volatile": True,
        "reset": 10,
        "randomizable": False,
    }


@pytest.fixture(scope="module")
def reserved_field_definition():
    return {
        "name": "part_id",
        "size": 8,
        "access": "RO",
        "reset": 0xFA,
        "randomizable": False,
        "reserved": True
    }


@pytest.fixture(scope="module")
def minimum_register_definition():
    return {
        "name": "test_reg"
    }


@pytest.fixture(scope="module")
def full_register_definition(minimum_field_definition, full_field_definition):
    return {
        "name": "full_reg",
        "coverage": "UVM_FULL_COVERAGE",
        "dimension": 4,
        "fields": [
            minimum_field_definition,
            full_field_definition
        ]
    }


@pytest.fixture(scope="module")
def traffic_light_full_def():
    with open("tests/data/traffic_light.json", "r") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def traffic_light_ral():
    with open("tests/data/traffic_light.svh", "r") as f:
        return f.read()


@pytest.fixture(scope="module")
def paged_block_ral():
    with open("tests/data/paged_block_ral.svh", "r") as f:
        return f.read()
