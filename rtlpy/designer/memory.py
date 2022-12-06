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
from attr import define, field, validators

import rtlpy.utils as utils
from rtlpy.designer.types import AccessType


class OverlappingMemoryException (Exception):
  pass


@define
class Field:
  """Class to represent a field in a memory map
  """

  name: str = field(validator=utils.name_validator)
  """The name of the Field"""

  access: AccessType = field(validator=validators.instance_of(AccessType))
  """The access type of the field"""

  lsb_pos: int = field(validator=validators.instance_of(int))
  """The offset of the Field's LSB in the register"""

  width: int = field(validator=validators.instance_of(int), default=1)
  """The width of the Field in bits"""

  reset: int = field(validator=validators.instance_of(int), converter=utils.val2int, default=0)
  """The value of the field upon reset"""

  volatile: bool = field(validator=validators.instance_of(bool), default=False)
  """Whether the field is volatile (aka will change without user input)"""

  randomizable: bool = field(validator=validators.instance_of(bool), default=True)
  """Whether the field is randomizable in sim"""

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


class Register:
  """Class to represent a Register in a memory map
  """

  name: str = field(validator=utils.name_validator)
  """The name of the Register"""

  width: int = field(validator=validators.instance_of(int))
  """The width of the register in bits"""

  _fields: list[Field] = field(factory=list, init=False)
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


class MemoryMap:
  pass
