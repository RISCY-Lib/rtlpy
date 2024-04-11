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

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from rtlpy.memory.registers import Register

import logging

from dataclasses import dataclass
import dataclasses
from abc import ABC, abstractmethod

from rtlpy.memory.remapping import RemapState, RegisterValueRemapCondition
from rtlpy._version_cfg import _dc_kwargs
import rtlpy.utils as utils

##########################################################################
# Logging
##########################################################################
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


##########################################################################
# Class Definitions
##########################################################################
@dataclass(**_dc_kwargs)
class MemoryMap:
  name: str = ""
  """The name of the memory map"""
  is_present: bool = True
  """Whether the memory map is present in the design"""
  mmap: list[MemSpace] = dataclasses.field(default_factory=list)
  """The memory map definition"""
  remap: MemoryRemap | None = None
  """The memory remap definition"""
  address_unit_bits: int = 8
  """The number of bits in each address unit"""

  def validate(self, recurse: bool = True) -> bool:
    """Validate the memory map. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = True

    if not utils.valid_name(self.name):
      _log.error(f"Invalid MemoryMap Name '{self.name}'")
      ret_val = False

    if self.address_unit_bits <= 0:
      _log.error(f"Invalid MemoryMap ({self.name}) AddressUnitBits {self.address_unit_bits}")
      ret_val = False

    if recurse:
      for element in self.mmap:
        if not element.validate():
          ret_val = False

      if self.remap is not None:
        if not self.remap.validate():
          ret_val = False

    return ret_val

  def to_ral(self, predictor_type: str = "uvm_reg_predictor#(uvm_sequence_item)") -> str:
    """Convert the provided MemoryMap and all sub-components to UVM registers and blocks.

    Args:
        predictor_type (str): The UVM predictor to use when creating a paged address block

    Returns:
        str: The string version of the generated RAL
    """
    ral_str = ""

    if self.is_present:
      for element in self.mmap:
        if isinstance(element, AddressBlock):
          ral_str += element.to_ral() + "\n\n"
        else:
          raise TypeError(
            f"MemoryMap.to_ral cannot handle a memory element of type: {type(element)}"
          )

      if self.remap is not None:
        ral_str += self.remap.to_ral() + "\n\n"

      ral_str += utils._render_uvm(
        "uvm_reg_block_top.jinja",
        block=self,
        predictor_type=predictor_type
      )

    return ral_str


@dataclass(**_dc_kwargs)
class MemSpace(ABC):
  name: str = ""
  """The name of the memory space"""
  is_present: bool = True
  """Whether the memory space is present in the design"""
  base_address: int = 0
  """The starting address of the memory space"""

  @abstractmethod
  def validate(self, recurse: bool = True, address_unit_bits: int = 8) -> bool:
    """Validate the memory space. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.
        address_unit_bits (int, optional): The number of bits in each address unit. Defaults to 8.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = True

    class_name = type(self).__name__

    if not utils.valid_name(self.name):
      _log.error(f"Invalid {class_name} Name '{self.name}'")
      ret_val = False

    if self.base_address < 0:
      _log.error(f"Invalid {class_name} ({self.name}) Base Address {self.base_address}")
      ret_val = False

    return ret_val


@dataclass(**_dc_kwargs)
class AddressBlock(MemSpace):
  block_size: int = 32
  """The bit width of the address block"""
  registers: list[Register] = dataclasses.field(default_factory=list)
  """The memory element associated with the address block"""

  def validate(self, recurse: bool = True, address_unit_bits: int = 8) -> bool:
    """Validate the memory map. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = super().validate(recurse, address_unit_bits)

    if self.block_size < 0:
      _log.error(f"Invalid AddressBlock Size {self.block_size}")
      ret_val = False

    if recurse:
      for element in self.registers:
        if not element.validate():
          ret_val = False

    if self.block_size <= 0:
      _log.error(f"Invalid AddressBlock ({self.name}) Block Size {self.block_size}")
      ret_val = False

    if self.block_size % address_unit_bits != 0:
      _log.error(f"AddressBlock '{self.name}' Size {self.block_size}" +
                 f" is not a multiple of AddressUnitBits {address_unit_bits}")
      ret_val = False

    for idx, r1 in enumerate(self.registers):
      for r2 in self.registers[idx + 1:]:
        if r1.overlaps(r2, address_unit=address_unit_bits):
          _log.error(f"AddressBlock {self.name} has overlapping registers {r1.name} and {r2.name}")
          ret_val = False

    return ret_val

  def to_ral(self) -> str:
    """Convert the provided AddressBlock and all sub-components to UVM registers and blocks.

    Returns:
        str: The string version of the generated RAL
    """
    ral_str = ""

    if not self.is_present:
      return ral_str

    for reg in self.registers:
      ral_str += reg.to_ral() + "\n\n"

    ral_str += utils._render_uvm(
      "uvm_reg_block.jinja",
      block=self
    )

    return ral_str


@dataclass(**_dc_kwargs)
class Bank(MemSpace):
  pass


@dataclass(**_dc_kwargs)
class SubspaceMap(MemSpace):
  pass


@dataclass(**_dc_kwargs)
class MemoryRemap:

  name: str = ""
  """The name of the memory remap"""
  state: RemapState = dataclasses.field(default_factory=RemapState)
  """The state that must be true for the remap to be active"""
  mmap: list[MemSpace] = dataclasses.field(default_factory=list)
  """The memory maps to be added when the remap is active"""

  def validate(self, recurse: bool = True) -> bool:
    """Validate the memory map. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = True

    if not utils.valid_name(self.name):
      _log.error(f"Invalid MemoryRemap Name '{self.name}'")
      ret_val = False

    if recurse:
      if not self.state.validate():
        ret_val = False

      for element in self.mmap:
        if not element.validate():
          ret_val = False

    return ret_val

  def to_ral(self) -> str:
    """Convert the provided MemoryRemap and all sub-components to UVM registers and blocks.

    Returns:
        str: The string version of the generated RAL
    """
    ral_str = ""

    for cond in self.state.conditions:
      if isinstance(cond, RegisterValueRemapCondition):
        ral_str += cond.to_ral() + "\n\n"

    for element in self.mmap:
      if isinstance(element, AddressBlock):
        ral_str += element.to_ral() + "\n\n"
      else:
        raise TypeError(
          f"MemoryRemap.to_ral cannot handle a memory element of type: {type(element)}"
        )

    return ral_str
