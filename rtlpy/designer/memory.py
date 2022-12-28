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

from __future__ import annotations

from typing import Iterator

from attr import validators
import attr

import rtlpy.utils as utils
from rtlpy.designer.types import AccessType


class OverlappingMemoryException (Exception):
  pass


class RegisterWidthException (Exception):
  pass


@attr.s
class Field:
  """Class to represent a field in a memory map
  """

  name: str = attr.ib(validator=utils.name_validator)
  """The name of the Field"""

  access: AccessType = attr.ib(validator=validators.instance_of(AccessType))
  """The access type of the field"""

  lsb_pos: int = attr.ib(validator=validators.instance_of(int))
  """The offset of the Field's LSB in the register"""

  width: int = attr.ib(validator=validators.instance_of(int), default=1)
  """The width of the Field in bits"""

  reset: int = attr.ib(validator=validators.instance_of(int), converter=utils.val2int, default=0)
  """The value of the field upon reset"""

  volatile: bool = attr.ib(validator=validators.instance_of(bool), default=False)
  """Whether the field is volatile (aka will change without user input)"""

  randomizable: bool = attr.ib(validator=validators.instance_of(bool), default=True)
  """Whether the field is randomizable in sim"""

  comment: str | None = attr.ib(default=None)

  def overlaps(self, fld: Field) -> bool:
    """Checks if this field overlaps bit positions with the provided field

    Args:
        fld (Field): The field to check for overlap with

    Returns:
        bool: True if they overlap, otherwise false
    """
    if not isinstance(fld, Field):
      raise ValueError(f"{type(self)}.overlaps expectes Field. Got {type(fld)}")

    return (self.lsb_pos <= fld.lsb_pos + fld.width - 1) and \
      (fld.lsb_pos <= self.lsb_pos + self.width - 1)


@attr.s
class Register:
  """Class to represent a Register in a memory map
  """

  name: str = attr.ib(validator=utils.name_validator)
  """The name of the Register"""

  width: int = attr.ib(validator=validators.instance_of(int))
  """The width of the register in bits"""

  _fields: list[Field] = attr.ib(factory=list, init=False)
  """List of fields in the register"""

  def addField(self, fld: Field) -> None:
    """Adds a field to the

    Args:
        fld (Field): The field to add
    """
    # Check if the provided field overlaps with any existing fields
    for idx, f in enumerate(self._fields):
      if fld.overlaps(f):
        raise OverlappingMemoryException(f"Cannot add field {fld.name} to register {self.name}:" +
                                         f" overlaps with {f.name}")

      if fld.lsb_pos < f.lsb_pos:
        self._fields.insert(idx, fld)

    if f.lsb_pos >= self.width:
      raise IndexError(f"Cannot add field {fld.name} to register {self.name}: " +
                       "register not wide enough")

    self._fields.append(fld)

  def addFields(self, flds: list[Field]) -> None:
    """Adds all of the fields

    Args:
        flds (list[Field]): All the fields to add
    """
    for f in flds:
      self.addField(f)

  def __len__(self) -> int:
    """The number of fields in the register

    Returns:
        int: The number of fields
    """
    return len(self._fields)

  def getFields(self) -> list[Field]:
    """Returns a list of the fields

    Returns:
        list[Field]: The list of fields in the register
    """
    return self._fields

  def getField(self, idx: int) -> Field:
    """Returns the field in the specified index

    Args:
        idx (int): The index of the field to get

    Returns:
        Field: The field at the given index
    """
    return self._fields[idx]

  def __iter__(self) -> Iterator[Field]:
    for fld in self._fields:
      yield fld


@attr.s
class AddressBlock:
  """Class to represent an AddressBlock in a memory map
  """

  name: str = attr.ib(validator=utils.name_validator)
  """The name of the AddressBlock"""

  width: int = attr.ib(validator=validators.instance_of(int))
  """The width of the registers of the block in bytes"""

  _regs: dict[int, Register] = attr.ib(factory=list, init=False)
  """List of registers in the AddressBlock"""

  def addReg(self, reg: Register, addr: int) -> None:
    """Adds the provided register at the provided register

    Args:
        reg (Register): The register to add to the AddressBlock
    """
    if (reg.width != self.width * 8):
      raise RegisterWidthException(f"Cannot add register {reg.name} to AddressBlock {self.name}:" +
                                   f" The register width ({reg.width} bits) it not compatible")

    for a, r in self._regs.items():
      if (addr <= a + self.width - 1) and (a <= addr + self.width - 1):
        raise OverlappingMemoryException(f"Cannot add field {reg.name} to register {self.name}:" +
                                         f" overlaps with {r.name}")

    self._regs[addr] = reg


class MemoryMap:
  pass
