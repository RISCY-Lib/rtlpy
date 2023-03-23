##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2022, Benjamin Davis                                     #
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
"""Module to test the rtlpy.design.Field class
"""

import pytest

from rtlpy.design import Field, AccessType, InvalidMemoryComponent

import tests._definitions.design_test_definitions as test_defs


def test_defaultField():
  fld = Field(name="test_name")

  assert fld.name == "test_name"
  assert fld.size == 1
  assert fld.lsb_pos == 0
  assert fld.access is AccessType.READ_ONLY
  assert not fld.volatile
  assert fld.reset == 0
  assert fld.randomizable
  assert not fld.reserved


def test_fullField():
  fld = Field(
    name="fld_name",
    size=8,
    lsb_pos=1,
    access=AccessType.WRITE_CLEARS,
    volatile=True,
    reset=10,
    randomizable=False,
    reserved=True
  )

  assert fld.name == "fld_name"
  assert fld.size == 8
  assert fld.lsb_pos == 1
  assert fld.access is AccessType.WRITE_CLEARS
  assert fld.volatile
  assert fld.reset == 10
  assert not fld.randomizable
  assert fld.reserved


def test_simpleFieldFromDict():
  fld = Field.from_dict(test_defs.MINIMUM_FIELD_DEFINITION)

  assert fld.name == test_defs.MINIMUM_FIELD_DEFINITION['name']
  assert fld.size == 1
  assert fld.lsb_pos == 0
  assert fld.access is AccessType.READ_ONLY
  assert not fld.volatile
  assert fld.reset == 0
  assert fld.randomizable
  assert not fld.reserved


def test_fullFieldFromDict():
  fld = Field.from_dict(test_defs.FULL_FIELD_DEFINITION)

  assert fld.name == test_defs.FULL_FIELD_DEFINITION['name']
  assert fld.size == 4
  assert fld.lsb_pos == 1
  assert fld.access is AccessType.WRITE_CLEARS
  assert fld.volatile
  assert fld.reset == 10
  assert not fld.randomizable
  assert not fld.reserved


def test_reservedFieldFromDict():
  fld = Field.from_dict(test_defs.RESERVED_FIELD_DEFINITION)

  assert fld.name == test_defs.RESERVED_FIELD_DEFINITION['name']
  assert fld.size == 8
  assert fld.lsb_pos == 0
  assert fld.access is AccessType.READ_ONLY
  assert not fld.volatile
  assert fld.reset == 0xFA
  assert not fld.randomizable
  assert fld.reserved


@pytest.mark.parametrize("name", [
  ("bad name"),
  ("but_why?")
])
def test_invalidField_BadName(name):
  fld = Field.from_dict(test_defs.FULL_FIELD_DEFINITION)

  fld.name = name

  with pytest.raises(InvalidMemoryComponent) as imc:
    fld.validate()

  assert imc.value.errors[0] == "Invalid field name"


def test_invalidField_RandomizableAndReserved():
  fld = Field.from_dict(test_defs.FULL_FIELD_DEFINITION)

  fld.randomizable = True
  fld.reserved = True

  with pytest.raises(InvalidMemoryComponent) as imc:
    fld.validate()

  assert imc.value.errors[0] == "Field cannot be randomizable and reserved"


def test_invalidField_ResetSize():
  fld = Field.from_dict(test_defs.FULL_FIELD_DEFINITION)

  fld.reset = 0xFF
  fld.size = 2

  with pytest.raises(InvalidMemoryComponent) as imc:
    fld.validate()

  assert imc.value.errors[0] == "Reset value does not fit in field"
