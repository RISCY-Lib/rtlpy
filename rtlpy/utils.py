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

import re
from typing import Any


def valid_name(name: str) -> bool:
  """Checks the name is valid for use in RTL.
  (i.e. contains only letters, numbers, and underscores)

  Args:
      name (str): The string to check

  Returns:
      bool: True if the name is valid, False otherwise
  """
  pattern = re.compile(r'[^A-z0-9_]')
  return not bool(pattern.search(name))


def name_validator(self: Any, attribute: Any, val: Any) -> None:
  if not valid_name(val):
    raise ValueError(f"Invalid Name Value {val}")


def val2int(val: Any) -> int:
  if not isinstance(val, str):
    return int(val)

  val = val.lower()

  if val[0:2] == "0x":
    return int(val[2:], base=16)
  if val[0] == "x":
    return int(val[1:], base=16)

  if "'h" in val:
    return int(val[val.find("'h")+2:], base=16)
  if "'d" in val:
    return int(val[val.find("'d")+2:], base=10)
  if "'o" in val:
    return int(val[val.find("'o")+2:], base=8)
  if "'b" in val:
    return int(val[val.find("'b")+2:], base=2)

  return int(val)
