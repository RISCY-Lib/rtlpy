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
"""Module to test the the ability of RTLPY to build a UVM_RAL from a MemoryMap definition
"""

from rtlpy.design import MemoryMap
import rtlpy.build.uvm_ral as uvm_ral

import tests._definitions.memory_map_definitions as test_defs


def test_TrafficLightFullRAL():
  mem_map = MemoryMap.from_dict(test_defs.TRAFFIC_LIGHT_FULL_DEF)

  ral_str = uvm_ral.memmap_to_ral(mem_map)

  assert ral_str == test_defs.TRAFFIC_LIGHT_RAL_STR
