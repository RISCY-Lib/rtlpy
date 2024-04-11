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
"""Module for testing basic memory functionality
"""

import rtlpy.memory as memory

import logging
import pytest

####################################################################################################
# Field Utility Functions
####################################################################################################
def test_FieldOverlap():
  fld1 = memory.Field(name="fld1", width=8, offset=0)
  fld2 = memory.Field(name="fld2", width=8, offset=8)

  assert fld1.overlaps(fld2) == False
  assert fld2.overlaps(fld1) == False
  fld2.offset = 4
  assert fld1.overlaps(fld2) == True
  assert fld2.overlaps(fld1) == True
  fld1.offset = 5
  assert fld1.overlaps(fld2) == True
  assert fld2.overlaps(fld1) == True

####################################################################################################
# Check Field Validation
####################################################################################################
@pytest.mark.parametrize("name", [
  ("bad name"),
  ("but_why?")
])
def test_invalidField_BadName(name, caplog):
  fld = memory.Field(name=name)

  assert not fld.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, f"Invalid Field Name '{name}'")
  ]


def test_invalidField_ResetSize(caplog):
  fld = memory.Field(reset=0xFF, width=2)

  assert not fld.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers",
     logging.WARNING,
     "Field () Reset Value 255 does not fit in 2 bits")
  ]

def test_invalidField_Offset(caplog):
  fld = memory.Field(offset=-1)

  assert not fld.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers",
     logging.ERROR,
     "Invalid Field () Offset -1")
  ]

def test_invalidField_Width(caplog):
  fld = memory.Field(width=0)

  assert not fld.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers",
     logging.ERROR,
     "Invalid Field () Width 0")
  ]

