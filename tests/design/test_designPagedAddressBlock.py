##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2023, RISCY-Lib Contributors                                    #
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
"""Module to test the rtlpy.design.PagedAddressBlock class
"""

from rtlpy.design import PagedAddressBlock


def test_defaultPagedAddressBlock():
  blk = PagedAddressBlock(name="test_name", addr_size=32, data_size=32)

  assert blk.name == "test_name"
  assert blk.addr_size == 32
  assert blk.data_size == 32
  assert blk.base_address == 0
  assert blk.dimension == 1
  assert blk.endianness == "little"
  assert blk.coverage == "UVM_NO_COVERAGE"
  assert len(blk.registers) == 0
  assert len(blk.sub_blocks) == 0


def test_singleSubBlockPagedAddressBlockFromDict(traffic_light_full_def):
  blk = PagedAddressBlock.from_dict(traffic_light_full_def)

  assert blk.name == traffic_light_full_def["name"]
  assert blk.addr_size == 6
  assert blk.data_size == 8
  assert blk.base_address == 0
  assert blk.dimension == 1
  assert blk.endianness == "little"
  assert blk.coverage == traffic_light_full_def["coverage"]
  assert len(blk.registers) == 0
  assert len(blk.sub_blocks) == 1


def test_multipleRegisterPagedAddressBlockFromDict(traffic_light_full_def):
  blk = PagedAddressBlock.from_dict(traffic_light_full_def)

  blk = blk.sub_blocks[0]

  assert blk.name == "setup"
  assert blk.addr_size == 6
  assert blk.data_size == 8
  assert blk.base_address == 16
  assert blk.dimension == 1
  assert blk.endianness == "little"
  assert blk.coverage == traffic_light_full_def["coverage"]
  assert len(blk.registers) == 3
  assert len(blk.sub_blocks) == 0
