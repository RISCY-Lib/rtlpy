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


from rtlpy.design import Field, AccessType

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import design_test_definitions as test_defs  # noqa: E402


def test_defaultField():
  fld = Field(name="test_name")

  assert fld.name == "test_name"
  assert fld.size == 1
  assert fld.lsb_pos == 0
  assert fld.access is AccessType.READ_ONLY
  assert not fld.volatile
  assert fld.reset == 0
  assert fld.randomizable


def test_fullField():
  fld = Field(
    name="fld_name",
    size=8,
    lsb_pos=1,
    access=AccessType.WRITE_CLEARS,
    volatile=True,
    reset=10,
    randomizable=False
  )

  assert fld.name == "fld_name"
  assert fld.size == 8
  assert fld.lsb_pos == 1
  assert fld.access is AccessType.WRITE_CLEARS
  assert fld.volatile
  assert fld.reset == 10
  assert not fld.randomizable


def test_simpleFieldFromDict():
  fld = Field.from_dict(test_defs.MINIMUM_FIELD_DEFINITION)

  assert fld.name == test_defs.MINIMUM_FIELD_DEFINITION['name']
  assert fld.size == 1
  assert fld.lsb_pos == 0
  assert fld.access is AccessType.READ_ONLY
  assert not fld.volatile
  assert fld.reset == 0
  assert fld.randomizable


def test_fullFieldFromDict():
  fld = Field.from_dict(test_defs.FULL_FIELD_DEFINITION)

  assert fld.name == test_defs.FULL_FIELD_DEFINITION['name']
  assert fld.size == 2
  assert fld.lsb_pos == 1
  assert fld.access is AccessType.WRITE_CLEARS
  assert fld.volatile
  assert fld.reset == 10
  assert not fld.randomizable
