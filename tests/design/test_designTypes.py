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
"""Module to test the rtlpy.design module
"""

import pytest
import rtlpy.design as design


@pytest.mark.parametrize("val,expected", [
  ("READ_ONLY".lower(),         design.AccessType.READ_ONLY),
  ("READ_WRITE".lower(),        design.AccessType.READ_WRITE),
  ("READ_CLEARS".lower(),       design.AccessType.READ_CLEARS),
  ("WRITE_READ_CLEARS".lower(), design.AccessType.WRITE_READ_CLEARS),
  ("WRITE_CLEARS".lower(),      design.AccessType.WRITE_CLEARS),
  ("WRITE_ONE_CLEARS".lower(),  design.AccessType.WRITE_ONE_CLEARS),
  ("WRITE_ZERO_CLEARS".lower(), design.AccessType.WRITE_ZERO_CLEARS),
  ("RO",                        design.AccessType.READ_ONLY),
  ("RW",                        design.AccessType.READ_WRITE),
  ("RC",                        design.AccessType.READ_CLEARS),
  ("WRC",                       design.AccessType.WRITE_READ_CLEARS),
  ("WC",                        design.AccessType.WRITE_CLEARS),
  ("W1C",                       design.AccessType.WRITE_ONE_CLEARS),
  ("W0C",                       design.AccessType.WRITE_ZERO_CLEARS),
])
def test_AccessType(val, expected):
  assert design.AccessType.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("OUTPUT", design.PortDirection.OUTPUT),
  ("out", design.PortDirection.OUTPUT),
  ("IN",  design.PortDirection.INPUT),
  ("input",  design.PortDirection.INPUT),
  ("INOUT",  design.PortDirection.INOUT),
  ("inout",  design.PortDirection.INOUT),
])
def test_PortDirection(val, expected):
  assert design.PortDirection.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("WIRE".lower(),        design.SignalType.WIRE),
  ("wire".upper(),        design.SignalType.WIRE),
  ("REG".lower(),         design.SignalType.REG),
  ("reg".upper(),         design.SignalType.REG),
  ("LOGIC".lower(),       design.SignalType.LOGIC),
  ("logic".upper(),       design.SignalType.LOGIC),
  ("REAL".lower(),        design.SignalType.REAL),
  ("real".upper(),        design.SignalType.REAL),
  ("WREAL".lower(),       design.SignalType.WREAL),
  ("wreal".upper(),       design.SignalType.WREAL),
  ("WREAL4".lower(),      design.SignalType.WREAL4),
  ("wreal4state".upper(), design.SignalType.WREAL4),
])
def test_SignalType(val, expected):
  assert design.SignalType.from_string(val) is expected


@pytest.mark.parametrize("val,expected", [
  ("NONE".lower(),    design.ParamType.NONE),
  ("none".upper(),    design.ParamType.NONE),
  ("INTEGER".lower(), design.ParamType.INTEGER),
  ("int".upper(),     design.ParamType.INTEGER),
  ("STRING".lower(),  design.ParamType.STRING),
  ("string".upper(),  design.ParamType.STRING),
])
def test_ParamType(val, expected):
  assert design.ParamType.from_string(val) is expected
