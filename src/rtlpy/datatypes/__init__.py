####################################################################################################
# rtlpy is a open-source utility library for RTL developers                                        #
# Copyright (C) 2025, RISCY-Lib Contributors                                                       #
#                                                                                                  #
# This program is free software: you can redistribute it and/or modify                             #
# it under the terms of the GNU General Public License as published by                             #
# the Free Software Foundation, either version 3 of the License, or                                #
# (at your option) any later version.                                                              #
#                                                                                                  #
# This program is distributed in the hope that it will be useful,                                  #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                                   #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                    #
# GNU General Public License for more details.                                                     #
#                                                                                                  #
# You should have received a copy of the GNU General Public License                                #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.                           #
####################################################################################################
"""A collection of data types and data-type converters for RTL design."""

from __future__ import annotations
from typing import Any

import re


def convert_to_unsigned_long_int(value: Any) -> int:
    if isinstance(value, int):
        if value < 0:
            raise ValueError("Value must be non-negative")
        return value
    if not isinstance(value, str):
        raise ValueError("Value must be a string or integer")

    if match := re.match(r"^\d*'[uU]?[hH]([0-9a-fA-F_]+)$", value):
        return int(match.group(1), 16)
    elif match := re.match(r"^\d*'[uU]?[dD]([0-9]+)$", value):
        return int(match.group(1), 10)
    elif match := re.match(r"^\d*'[uU]?[oO]([0-7]+)$", value):
        return int(match.group(1), 8)
    elif match := re.match(r"^\d*'[uU]?[bB]([01]+)$", value):
        return int(match.group(1), 2)
    elif match := re.match(r"^0?x([0-9a-fA-F_]+)$", value):
        return int(match.group(1), 16)
    else:
        return int(value, 10)
