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
"""Module to test the rtlpy.design.Register class
"""

from rtlpy.design import Register


def test_defaultRegister():
  reg = Register(name="test_name")

  assert reg.name == "test_name"
  assert reg.dimension == 1
  assert len(reg.fields) == 0
  assert reg.coverage == "UVM_NO_COVERAGE"
  assert not reg.randomizable()


def test_simpleRegisterFromDict(minimum_register_definition):
  reg = Register.from_dict(minimum_register_definition)

  assert reg.name == minimum_register_definition["name"]
  assert reg.dimension == 1
  assert len(reg.fields) == 0
  assert reg.coverage == "UVM_NO_COVERAGE"
  assert not reg.randomizable()


def test_fullRegisterFromDict(full_register_definition):
  reg = Register.from_dict(full_register_definition)

  assert reg.name == full_register_definition["name"]
  assert reg.dimension == 4
  assert len(reg.fields) == 2
  assert reg.coverage == "UVM_FULL_COVERAGE"
  assert reg.randomizable()
