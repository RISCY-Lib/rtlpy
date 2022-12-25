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


def test_simpleField():
  f1 = designer.Field("test_field", designer.AccessType.READ_WRITE, 0)

  assert f1.name == "test_field"
  assert f1.access == designer.AccessType.READ_WRITE
  assert f1.lsb_pos == 0
  assert f1.width == 1
  assert f1.reset == 0
  assert not f1.volatile
  assert f1.randomizable


def test_fullField():
  f1 = designer.Field("test_field1", designer.AccessType.READ_ONLY, 4, 10, "10'hF", True, False)

  assert f1.name == "test_field1"
  assert f1.access == designer.AccessType.READ_ONLY
  assert f1.lsb_pos == 4
  assert f1.width == 10
  assert f1.reset == 0xF
  assert f1.volatile
  assert not f1.randomizable


@pytest.mark.parametrize("lh_lsb, lh_width, rh_lsb, rh_width, expected", [
  (0, 10, 1, 1, True),
  (0, 1, 1, 1,  False),
  (2, 3, 5, 5,  False),
  (2, 4, 5, 5,  True),
])
def test_overlappingFields(lh_lsb, lh_width, rh_lsb, rh_width, expected):
  f1 = designer.Field("test_field_left", designer.AccessType.READ_ONLY, lh_lsb, lh_width)
  f2 = designer.Field("test_field_right", designer.AccessType.READ_ONLY, rh_lsb, rh_width)

  if expected:
    assert f1.overlaps(f2)
    assert f2.overlaps(f1)
  else:
    assert not f1.overlaps(f2)
    assert not f2.overlaps(f1)
