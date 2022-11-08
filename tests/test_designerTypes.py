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
import rtlpy.designer as designer


@pytest.mark.parametrize("val,expected", [
  ("READ_ONLY".lower(),         designer.AccessType.READ_ONLY),
  ("READ_WRITE".lower(),        designer.AccessType.READ_WRITE),
  ("READ_CLEARS".lower(),       designer.AccessType.READ_CLEARS),
  ("WRITE_READ_CLEARS".lower(), designer.AccessType.WRITE_READ_CLEARS),
  ("WRITE_CLEARS".lower(),      designer.AccessType.WRITE_CLEARS),
  ("WRITE_ONE_CLEARS".lower(),  designer.AccessType.WRITE_ONE_CLEARS),
  ("WRITE_ZERO_CLEARS".lower(), designer.AccessType.WRITE_ZERO_CLEARS),
  ("RO",                        designer.AccessType.READ_ONLY),
  ("RW",                        designer.AccessType.READ_WRITE),
  ("RC",                        designer.AccessType.READ_CLEARS),
  ("WRC",                       designer.AccessType.WRITE_READ_CLEARS),
  ("WC",                        designer.AccessType.WRITE_CLEARS),
  ("W1C",                       designer.AccessType.WRITE_ONE_CLEARS),
  ("W0C",                       designer.AccessType.WRITE_ZERO_CLEARS),
])
def test_AccessType(val, expected):
  assert designer.AccessType.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("OUTPUT", designer.PortDirection.OUTPUT),
  ("out", designer.PortDirection.OUTPUT),
  ("IN",  designer.PortDirection.INPUT),
  ("input",  designer.PortDirection.INPUT),
  ("INOUT",  designer.PortDirection.INOUT),
  ("inout",  designer.PortDirection.INOUT),
])
def test_PortDirection(val, expected):
  assert designer.PortDirection.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("WIRE".lower(),        designer.SignalType.WIRE),
  ("wire".upper(),        designer.SignalType.WIRE),
  ("REG".lower(),         designer.SignalType.REG),
  ("reg".upper(),         designer.SignalType.REG),
  ("LOGIC".lower(),       designer.SignalType.LOGIC),
  ("logic".upper(),       designer.SignalType.LOGIC),
  ("REAL".lower(),        designer.SignalType.REAL),
  ("real".upper(),        designer.SignalType.REAL),
  ("WREAL".lower(),       designer.SignalType.WREAL),
  ("wreal".upper(),       designer.SignalType.WREAL),
  ("WREAL4".lower(),      designer.SignalType.WREAL4),
  ("wreal4state".upper(), designer.SignalType.WREAL4),
])
def test_SignalType(val, expected):
  assert designer.SignalType.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("NONE".lower(),    designer.ParamType.NONE),
  ("none".upper(),    designer.ParamType.NONE),
  ("INTEGER".lower(), designer.ParamType.INTEGER),
  ("int".upper(),     designer.ParamType.INTEGER),
  ("STRING".lower(),  designer.ParamType.STRING),
  ("string".upper(),  designer.ParamType.STRING),
])
def test_ParamType(val, expected):
  assert designer.ParamType.from_string(val) is expected
