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
"""Module to test the rtlpy.types module
"""

import pytest
import rtlpy.types as types


@pytest.mark.parametrize("val,expected", [
  ("READ_ONLY".lower(),         types.AccessType.READ_ONLY),
  ("READ_WRITE".lower(),        types.AccessType.READ_WRITE),
  ("READ_CLEARS".lower(),       types.AccessType.READ_CLEARS),
  ("WRITE_READ_CLEARS".lower(), types.AccessType.WRITE_READ_CLEARS),
  ("WRITE_CLEARS".lower(),      types.AccessType.WRITE_CLEARS),
  ("WRITE_ONE_CLEARS".lower(),  types.AccessType.WRITE_ONE_CLEARS),
  ("WRITE_ZERO_CLEARS".lower(), types.AccessType.WRITE_ZERO_CLEARS),
  ("RO",                        types.AccessType.READ_ONLY),
  ("RW",                        types.AccessType.READ_WRITE),
  ("RC",                        types.AccessType.READ_CLEARS),
  ("WRC",                       types.AccessType.WRITE_READ_CLEARS),
  ("WC",                        types.AccessType.WRITE_CLEARS),
  ("W1C",                       types.AccessType.WRITE_ONE_CLEARS),
  ("W0C",                       types.AccessType.WRITE_ZERO_CLEARS),
])
def test_AccessType(val, expected):
  assert types.AccessType.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("OUTPUT", types.PortDirection.OUTPUT),
  ("out", types.PortDirection.OUTPUT),
  ("IN",  types.PortDirection.INPUT),
  ("input",  types.PortDirection.INPUT),
  ("INOUT",  types.PortDirection.INOUT),
  ("inout",  types.PortDirection.INOUT),
])
def test_PortDirection(val, expected):
  assert types.PortDirection.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("WIRE".lower(),        types.SignalType.WIRE),
  ("wire".upper(),        types.SignalType.WIRE),
  ("REG".lower(),         types.SignalType.REG),
  ("reg".upper(),         types.SignalType.REG),
  ("LOGIC".lower(),       types.SignalType.LOGIC),
  ("logic".upper(),       types.SignalType.LOGIC),
  ("REAL".lower(),        types.SignalType.REAL),
  ("real".upper(),        types.SignalType.REAL),
  ("WREAL".lower(),       types.SignalType.WREAL),
  ("wreal".upper(),       types.SignalType.WREAL),
  ("WREAL4".lower(),      types.SignalType.WREAL4),
  ("wreal4state".upper(), types.SignalType.WREAL4),
])
def test_SignalType(val, expected):
  assert types.SignalType.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("NONE".lower(),    types.ParamType.NONE),
  ("none".upper(),    types.ParamType.NONE),
  ("INTEGER".lower(), types.ParamType.INTEGER),
  ("int".upper(),     types.ParamType.INTEGER),
  ("STRING".lower(),  types.ParamType.STRING),
  ("string".upper(),  types.ParamType.STRING),
])
def test_ParamType(val, expected):
  assert types.ParamType.from_string(val) is expected
