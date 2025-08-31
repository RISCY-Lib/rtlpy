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

from rtlpy.ipxact import common


@pytest.mark.parametrize(
    ("left", "right", "expected_left", "expected_right"),
    [
        ("0", "31", 0, 31),
        ("'h8", "'hF", 8, 15),
        ("8'hFF", "32'h100", 255, 256),
        ("0x0", "0x1F", 0, 31),
    ]
)
def test_range_valid(left: str, right: str, expected_left: str, expected_right: str) -> None:
    range_val = common.Range.from_xml(
        f'''<ipxact:range xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2022">
            <ipxact:left minimum="0">{left}</ipxact:left>
            <ipxact:right>{right}</ipxact:right>
            </ipxact:range>
        '''
    )

    assert range_val.left == expected_left
    assert range_val.right == expected_right
    assert "minimum" in range_val.left_attribs
