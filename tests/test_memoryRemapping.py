##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2024, RISCY-Lib Contributors                             #
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
"""Module for testing memory remapping functionality"""

import rtlpy.memory as memory


def test_InvalidRemapState_BadName(caplog):
  remap = memory.RemapState(name="bad name")

  assert not remap.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.remapping", 40, "Invalid RemapState Name 'bad name'")
  ]


def test_InvalidRemapState_BadCondition(caplog):
  remap = memory.RemapState(name="remap")
  remap.conditions.append(
    memory.RegisterValueRemapCondition(
      register=None,
      value=0
    )
  )

  assert not remap.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.remapping", 40, "Invalid Register Value Remap Condition (None)")
  ]
