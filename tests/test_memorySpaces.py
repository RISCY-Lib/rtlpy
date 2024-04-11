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
"""Module for testing memory spaces"""

import rtlpy.memory as memory


def test_InvalidMemoryMap_BadName(caplog):
  mem = memory.MemoryMap(name="bad name")

  assert not mem.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid MemoryMap Name 'bad name'")
  ]


def test_InvalidMemoryMap_BadAddressUnitBits(caplog):
  mem = memory.MemoryMap(name="mem", address_unit_bits=0)

  assert not mem.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid MemoryMap (mem) AddressUnitBits 0")
  ]


def test_InvalidMemoryMap_ChildMemSpace(caplog):
  mem = memory.MemoryMap(name="mem")
  mem.mmap.append(
    memory.AddressBlock(name="mem map")
  )

  assert not mem.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid AddressBlock Name 'mem map'")
  ]


def test_InvalidAddressBlock_BadName(caplog):
  block = memory.AddressBlock(name="bad name")

  assert not block.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid AddressBlock Name 'bad name'")
  ]


def test_InvalidAddressBlock_BadBaseAddress(caplog):
  block = memory.AddressBlock(name="block", base_address=-1)

  assert not block.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid AddressBlock (block) Base Address -1")
  ]


def test_InvalidAddressBlock_BadBlockSize(caplog):
  block = memory.AddressBlock(name="block", block_size=0)

  assert not block.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid AddressBlock (block) Block Size 0")
  ]


def test_InvalidAddressBlock_BadBlockSize2(caplog):
  block = memory.AddressBlock(name="block", block_size=7)

  assert not block.validate(address_unit_bits=8)

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "AddressBlock 'block' Size 7 is not a multiple of AddressUnitBits 8")
  ]


def test_InvalidAddressBlock_ChildRegister(caplog):
  block = memory.AddressBlock(name="block")
  block.registers.append(
    memory.Register(name="reg?")
  )

  assert not block.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.registers", 40, "Invalid Register Name 'reg?'")
  ]


def test_InvalidMemoryRemap_BadName(caplog):
  remap = memory.MemoryRemap(name="bad name")

  assert not remap.validate()

  assert caplog.record_tuples == [
    ("rtlpy.memory.spaces", 40, "Invalid MemoryRemap Name 'bad name'")
  ]
