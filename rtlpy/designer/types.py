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

from __future__ import annotations
from enum import Enum


class AccessType (Enum):
  """Type to represent Memory Access-Types"""

  READ_ONLY = "RO"
  READ_WRITE = "RW"
  READ_CLEARS = "RC"
  READ_SETS = "RS"
  WRITE_READ_CLEARS = "WRC"
  WRITE_READ_SETS = "WRS"
  WRITE_CLEARS = "WC"
  WRITE_SETS = "WS"
  WRITE_SETS_READ_CLEARS = "WSRC"
  WRITE_CLEARS_READ_SETS = "WCRS"
  WRITE_ONE_CLEARS = "W1C"
  WRITE_ONE_SETS = "W1S"
  WRITE_ONE_TOGGLES = "W1T"
  WRITE_ZERO_CLEARS = "W0C"
  WRITE_ZERO_SETS = "W0S"
  WRITE_ZERO_TOGGLES = "W0T"
  WRITE_ONE_SETS_READ_CLEARS = "W1SRC"
  WRITE_ONE_CLEARS_READ_SETS = "W1CRS"
  WRITE_ZERO_SETS_READ_CLEARS = "W0SRC"
  WRITE_ZERO_CLEARS_READ_SETS = "W0CRS"
  WRITE_ONLY = "WO"
  WRITE_ONLY_CLEARS = "WOC"
  WRITE_ONLY_SETS = "WOS"
  WRITE_ONE = "W1"
  WRITE_ONLY_ONE = "WO1"

  @classmethod
  def from_string(cls, label: str) -> AccessType:
    format_label = label.replace(" ", "_").upper()

    for access in cls:
      print(type(access))
      if (format_label == access.name):
        return access
      elif (format_label == access.value):
        return access
    raise KeyError(label)


class PortDirection(Enum):
  """Type to represent Port Direction Types"""

  OUTPUT = "OUT"
  INPUT = "IN"
  INOUT = "INOUT"

  @classmethod
  def from_string(cls, label: str) -> PortDirection:
    format_label = label.replace(" ", "_").upper()
    for access in cls:
      if (format_label == access.name):
        return access
      elif (format_label == access.value):
        return access
    raise KeyError(label)


class SignalType(Enum):
  """Type to represent signal type"""

  WIRE = "WIRE"
  REG = "REG"
  LOGIC = "LOGIC"
  REAL = "REAL"
  WREAL = "WREAL"
  WREAL4 = "WREAL4STATE"

  @classmethod
  def from_string(cls, label: str) -> SignalType:
    format_label = label.replace(" ", "_").upper()
    for access in cls:
      if (format_label == access.name):
        return access
      elif (format_label == access.value):
        return access
    raise KeyError(label)


class ParamType(Enum):
  """Type to represent a parameter type"""

  NONE = "NONE"
  INTEGER = "INT"
  STRING = "STRING"

  @classmethod
  def from_string(cls, label: str) -> ParamType:
    format_label = label.replace(" ", "_").upper()
    for access in cls:
      if (format_label == access.name):
        return access
      elif (format_label == access.value):
        return access
    raise KeyError(label)
