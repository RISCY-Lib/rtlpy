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
"""Module to test the rtlpy.designs module
"""


import pytest
import rtlpy.designs as designs

##########################################################################
# Helper functions
##########################################################################


@pytest.mark.parametrize("rh,lh,expected", [
  ((0, 2), (3, 5), False),
  ((1, 2), (0, 3), True),
  ((0, 2), (1, 3), True),
  ((2, 4), (1, 3), True),
  ((0, 3), (1, 2), True),
])
def test__overlaps(lh, rh, expected):
  """Tests the overlaps helper function"""
  assert designs._overlaps(lh, rh) is expected


@pytest.mark.parametrize("val,expected", [
  ("0xA",    0xA),
  ("0xA",    0xA),
  ("0xBABE", 0xBABE),
  ("243",    243),
  (6969,     6969),
])
def test__val2int(val, expected):
  """Tests the _val2int helper function"""
  assert designs._val2int(val) == expected

##########################################################################
# ENUMS
##########################################################################


@pytest.mark.parametrize("val,expected", [
  ("READ_ONLY".lower(),         designs.AccessType.READ_ONLY),
  ("READ_WRITE".lower(),        designs.AccessType.READ_WRITE),
  ("READ_CLEARS".lower(),       designs.AccessType.READ_CLEARS),
  ("WRITE_READ_CLEARS".lower(), designs.AccessType.WRITE_READ_CLEARS),
  ("WRITE_CLEARS".lower(),      designs.AccessType.WRITE_CLEARS),
  ("WRITE_ONE_CLEARS".lower(),  designs.AccessType.WRITE_ONE_CLEARS),
  ("WRITE_ZERO_CLEARS".lower(), designs.AccessType.WRITE_ZERO_CLEARS),
  ("RO",                        designs.AccessType.READ_ONLY),
  ("RW",                        designs.AccessType.READ_WRITE),
  ("RC",                        designs.AccessType.READ_CLEARS),
  ("WRC",                       designs.AccessType.WRITE_READ_CLEARS),
  ("WC",                        designs.AccessType.WRITE_CLEARS),
  ("W1C",                       designs.AccessType.WRITE_ONE_CLEARS),
  ("W0C",                       designs.AccessType.WRITE_ZERO_CLEARS),
])
def test__conv2access(val, expected):
  assert designs._conv2access(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("OUTPUT", designs.PortDirection.OUTPUT),
  ("output", designs.PortDirection.OUTPUT),
  ("INPUT",  designs.PortDirection.INPUT),
  ("input",  designs.PortDirection.INPUT),
  ("INOUT",  designs.PortDirection.INOUT),
  ("inout",  designs.PortDirection.INOUT),
])
def test__conv2direction(val, expected):
  assert designs._conv2direction(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("WIRE".lower(),        designs.SignalType.WIRE),
  ("wire".upper(),        designs.SignalType.WIRE),
  ("REG".lower(),         designs.SignalType.REG),
  ("reg".upper(),         designs.SignalType.REG),
  ("LOGIC".lower(),       designs.SignalType.LOGIC),
  ("logic".upper(),       designs.SignalType.LOGIC),
  ("REAL".lower(),        designs.SignalType.REAL),
  ("real".upper(),        designs.SignalType.REAL),
  ("WREAL".lower(),       designs.SignalType.WREAL),
  ("wreal".upper(),       designs.SignalType.WREAL),
  ("WREAL4".lower(),      designs.SignalType.WREAL4),
  ("wreal4state".upper(), designs.SignalType.WREAL4),
])
def test__conv2sigtype(val, expected):
  assert designs._conv2sigtype(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("NONE".lower(),    designs.ParamType.NONE),
  ("none".upper(),    designs.ParamType.NONE),
  ("INTEGER".lower(), designs.ParamType.INTEGER),
  ("int".upper(),     designs.ParamType.INTEGER),
  ("STRING".lower(),  designs.ParamType.STRING),
  ("string".upper(),  designs.ParamType.STRING),
])
def test__conv2paramtype(val, expected):
  assert designs._conv2paramtype(val) is expected

##########################################################################
# Memory Classes - Field
##########################################################################


def test_valid_field():
  f = designs.Field(name="test_fld", access="RO", lsb_pos=0)
  assert f.name == "test_fld"
  assert f.access == designs.AccessType.READ_ONLY
  assert f.lsb_pos == 0
  assert f.width == 1
  assert f.reset == 0
  f.lsb_pos = 2
  f.width = 4
  f.reset = "0xA"
  assert f.lsb_pos == 2
  assert f.width == 4
  assert f.reset == 0xA
