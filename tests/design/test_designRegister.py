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
"""Module to test the rtlpy.design.Register class
"""


from rtlpy.design import Register


import tests._definitions.design_test_definitions as test_defs


def test_defaultRegister():
  reg = Register(name="test_name")

  assert reg.name == "test_name"
  assert reg.dimension == 1
  assert len(reg.fields) == 0
  assert reg.coverage == "UVM_NO_COVERAGE"


def test_simpleRegisterFromDict():
  reg = Register.from_dict(test_defs.MINIMUM_REGISTER_DEFINITION)

  assert reg.name == test_defs.MINIMUM_REGISTER_DEFINITION["name"]
  assert reg.dimension == 0
  assert len(reg.fields) == 0
  assert reg.coverage == "UVM_NO_COVERAGE"


def test_fullRegisterFromDict():
  reg = Register.from_dict(test_defs.FULL_REGISTER_DEFINITION)

  assert reg.name == test_defs.FULL_REGISTER_DEFINITION["name"]
  assert reg.dimension == 4
  assert len(reg.fields) == 2
  assert reg.coverage == "UVM_FULL_COVERAGE"
