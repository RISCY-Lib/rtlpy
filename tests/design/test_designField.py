##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2022, RISCY-Lib Contributors                                    #
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

import logging

from rtlpy.design import Field, AccessType


def test_defaultField():
  fld = Field(name="test_name")

  assert fld.name == "test_name"
  assert fld.size == 1
  assert fld.access is AccessType.READ_ONLY
  assert fld.reset == 0
  assert not fld.volatile
  assert fld.randomizable
  assert not fld.reserved


def test_fullField():
  fld = Field(
    name="fld_name",
    size=8,
    access=AccessType.WRITE_CLEARS,
    reset=10,
    volatile=True,
    randomizable=False,
    reserved=True
  )

  assert fld.name == "fld_name"
  assert fld.size == 8
  assert fld.access is AccessType.WRITE_CLEARS
  assert fld.reset == 10
  assert fld.volatile
  assert not fld.randomizable
  assert fld.reserved


def test_simpleFieldFromDict(minimum_field_definition):
  fld = Field.from_dict(minimum_field_definition)

  assert fld.name == minimum_field_definition['name']
  assert fld.size == 1
  assert fld.access is AccessType.READ_ONLY
  assert not fld.volatile
  assert fld.reset == 0
  assert fld.randomizable
  assert not fld.reserved


def test_fullFieldFromDict(full_field_definition):
  fld = Field.from_dict(full_field_definition)

  assert fld.name == full_field_definition['name']
  assert fld.size == 4
  assert fld.access is AccessType.WRITE_CLEARS
  assert fld.reset == 10
  assert fld.volatile
  assert not fld.randomizable
  assert not fld.reserved


def test_reservedFieldFromDict(reserved_field_definition):
  fld = Field.from_dict(reserved_field_definition)

  assert fld.name == reserved_field_definition['name']
  assert fld.size == 8
  assert fld.access is AccessType.READ_ONLY
  assert fld.reset == 0xFA
  assert not fld.volatile
  assert not fld.randomizable
  assert fld.reserved


@pytest.mark.parametrize("name", [
  ("bad name"),
  ("but_why?")
])
def test_invalidField_BadName(name, caplog, full_field_definition):
  fld = Field.from_dict(full_field_definition)

  fld.name = name

  assert not fld.valid()

  assert caplog.record_tuples == [
    ("rtlpy.design.memory", logging.ERROR, f"Field ({name}) has an invalid name.")
  ]


def test_invalidField_RandomizableAndReserved(caplog, full_field_definition):
  fld = Field.from_dict(full_field_definition)

  fld.randomizable = True
  fld.reserved = True

  assert not fld.valid()

  assert caplog.record_tuples == [
    ("rtlpy.design.memory",
     logging.WARNING,
     f"Field ({fld.name}) cannot be randomizable and reserved.")
  ]


def test_invalidField_ResetSize(caplog, full_field_definition):
  fld = Field.from_dict(full_field_definition)

  fld.reset = 0xFF
  fld.size = 2

  assert not fld.valid()

  assert caplog.record_tuples == [
    ("rtlpy.design.memory",
     logging.ERROR,
     f"Field ({fld.name}) reset value (255) does not fit in field (size: 2).")
  ]
