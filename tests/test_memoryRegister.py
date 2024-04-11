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
# Check Register Validation
####################################################################################################
@pytest.mark.parametrize("name", [
  ("bad name"),
  ("but_why?")
])
def test_invalidRegister_BadName(name, caplog,):
  reg = memory.Register(name=name)

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, f"Invalid Register Name '{name}'")
  ]


def test_invalidRegister_BadDim(caplog):
  reg = memory.Register(name="reg", dimension=0)

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, "Invalid Register (reg) Dimension 0")
  ]


def test_invalidRegister_BadOffset(caplog):
  reg = memory.Register(name="reg", address_offset=-1)

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, "Invalid Register (reg) Offset -1")
  ]

def test_invalidRegister_BadSize(caplog):
  reg = memory.Register(name="reg", size=0)

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, "Invalid Register (reg) Size 0")
  ]


def test_invalidRegister_FieldOverlap(caplog):
  reg = memory.Register(name="reg", size=32, fields=[
    memory.Field(name="fld1", width=9, offset=0),
    memory.Field(name="fld2", width=8, offset=8)
  ])

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, "Field fld1 overlaps with Field fld2 in Register reg")
  ]

def test_invalidRegister_FieldOutOfBounds(caplog):
  reg = memory.Register(name="reg", fields=[
    memory.Field(name="fld1", width=8, offset=0),
    memory.Field(name="fld2", width=8, offset=8)
  ])

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.WARNING, "Field fld1 is out of bounds in Register reg"),
    ("rtlpy.memory.registers", logging.WARNING, "Field fld2 is out of bounds in Register reg")
  ]

def test_invalidRegister_BadField(caplog):
  reg = memory.Register(name="reg", size=16, fields=[
    memory.Field(name="fld1", width=-1, offset=0),
    memory.Field(name="what?", width=0, offset=8)
  ])

  assert not reg.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", logging.ERROR, "Invalid Field (fld1) Width -1"),
    ("rtlpy.memory.registers", logging.WARNING, "Field (fld1) Reset Value 0 does not fit in -1 bits"),
    ("rtlpy.memory.registers", logging.ERROR, "Invalid Field Name 'what?'"),
    ("rtlpy.memory.registers", logging.ERROR, "Invalid Field (what?) Width 0")
  ]

def test_validRegister(caplog):
  reg = memory.Register(name="reg", size=16, fields=[
    memory.Field(name="fld1", width=8, offset=0),
    memory.Field(name="fld2", width=8, offset=8)
  ])

  assert reg.validate()

  assert caplog.record_tuples == []