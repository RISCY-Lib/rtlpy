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

from __future__ import annotations

import pytest

from rtlpy import sv


@pytest.mark.parametrize(
    "expr, expected_val",
    [
        ("5", 5),
        ("5'd5", 5),
        ("5'd10", 10),
        ("5'd0", 0),
        ("5'hA", 10),
        ("5'o12", 10),
        ("5'b1010", 10),
    ],
)
def test_expression_to_unsigned_long_int(expr: str, expected_val: int) -> None:
    assert sv.expression_to_unsigned_long_int(expr) == expected_val
