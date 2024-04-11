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
  from rtlpy.memory.spaces import AddressBlock


import logging

from dataclasses import dataclass
import dataclasses

import enum

from rtlpy.types import AccessType
from rtlpy._version_cfg import _dc_kwargs
from rtlpy import utils

##########################################################################
# Logging
##########################################################################
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


##########################################################################
# Class Definitions
##########################################################################
@dataclass(**_dc_kwargs)
class Register:
  name: str = ""
  """The name of the register"""
  is_present: bool = True
  """Whether the register is present in the design"""
  dimension: int = 1
  """The number of instances of the register"""
  address_offset: int = 0
  """The starting address of the register"""
  size: int = 1
  """The bit width of the register"""
  volatile: bool = False
  """Whether the value of register is volatile"""
  access: AccessType = AccessType.READ_WRITE
  """Access Policy of the Register"""
  fields: list[Field] = dataclasses.field(default_factory=list)
  """The memory element associated with the register"""

  def validate(self, recurse: bool = True, parent: AddressBlock | None = None) -> bool:
    """Validate the register. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = True

    if not utils.valid_name(self.name):
      _log.error(f"Invalid Register Name '{self.name}'")
      ret_val = False

    if self.dimension < 1:
      _log.error(f"Invalid Register ({self.name}) Dimension {self.dimension}")
      ret_val = False

    if self.address_offset < 0:
      _log.error(f"Invalid Register ({self.name}) Offset {self.address_offset}")
      ret_val = False

    if self.size < 1:
      _log.error(f"Invalid Register ({self.name}) Size {self.size}")
      ret_val = False

    for field in self.fields:
      if field.offset + field.width - 1 > self.size:
        _log.warning(f"Field {field.name} is out of bounds in Register {self.name}")
        ret_val = False

      if recurse and not field.validate():
        ret_val = False

    for idx, f1 in enumerate(self.fields):
      for f2 in self.fields[idx+1:]:
        if f1.overlaps(f2):
          _log.error(f"Field {f1.name} overlaps with Field {f2.name} in Register {self.name}")
          ret_val = False

    return ret_val

  def overlaps(self, other: Register, address_unit: int = 8) -> bool:
    """Check if the register overlaps with another register

    Args:
        other (Register): The other register to check for overlap

    Returns:
        bool: True if the registers overlap, False otherwise
    """
    if (self.address_offset == other.address_offset):
      return True
    elif self.address_offset < other.address_offset:
      return self.address_offset + (self.size/address_unit) > other.address_offset
    else:
      return other.address_offset + (other.size/address_unit) > self.address_offset


@dataclass(**_dc_kwargs)
class Field:
  name: str = ""
  """The name of the field"""
  is_present: bool = True
  """Whether the field is present in the design"""
  offset: int = 0
  """The offset of the field in the register"""
  reset: int = 0
  """The reset value of the field"""
  width: int = 1
  """Size of the field in bits"""
  volatile: bool = False
  """Whether the value of field is volatile"""
  access: AccessType = AccessType.READ_ONLY
  """Access Policy of the Field"""
  enum_vals: type[enum.Enum] | None = None

  def validate(self) -> bool:
    """Validate the field. Errors and warnings are logged.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = True

    if not utils.valid_name(self.name):
      _log.error(f"Invalid Field Name '{self.name}'")
      ret_val = False

    if self.width < 1:
      _log.error(f"Invalid Field ({self.name}) Width {self.width}")
      ret_val = False

    if self.offset < 0:
      _log.error(f"Invalid Field ({self.name}) Offset {self.offset}")
      ret_val = False

    if self.reset.bit_length() > self.width:
      _log.warning(f"Field ({self.name}) Reset Value {self.reset} does not fit in {self.width} bits")
      ret_val = False

    return ret_val

  def overlaps(self, other: Field) -> bool:
    """Check if the register overlaps with another register

    Args:
        other (Register): The other register to check for overlap

    Returns:
        bool: True if the registers overlap, False otherwise
    """
    if (self.offset == other.offset):
      return True
    elif self.offset < other.offset:
      return self.offset + (self.width) > other.offset
    else:
      return other.offset + (other.width) > self.offset
