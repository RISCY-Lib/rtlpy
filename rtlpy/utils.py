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
