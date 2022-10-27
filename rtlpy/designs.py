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
"""The module which contains the classes necessary to represent a skeleton
RTL design.
"""

from __future__ import annotations
from typing import Any, Iterator, Union, Tuple
from attr import define, field, validators
from enum import Enum

##########################################################################
# Helper functions
##########################################################################


def _val2int(val: Union[str, int]) -> int:
  if (isinstance(val, int)):
    return val

  if (not isinstance(val, str)):
    raise TypeError("Function _val2int takes one argument that must be type: str or int")

  if (val.startswith("0x")):
    return int(val, base=16)
  elif (val.startswith("x")):
    return int("0"+val, base=16)
  else:
    return int(val)


def _overlaps(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
  """Determines if the two ranges overlap

  Args:
      range1 (Tuple[int, int]): The first range
      range2 (Tuple[int, int]): The second range

  Returns:
      bool: True if the ranges overlap, otherwise false
  """
  if (range1[0] < range2[0] and range1[1] > range2[0]):  # Overlaps low point of range
    return True
  if (range1[0] < range2[1] and range1[1] > range2[1]):  # Overlaps high point of range
    return True
  if (range1[0] > range2[0] and range1[1] < range2[1]):  # Inside case
    return True

  return False


##########################################################################
# ENUMS
##########################################################################


class AccessType (Enum):
  READ_ONLY = "RO"
  READ_WRITE = "RW"
  READ_CLEARS = "RC"
  WRITE_READ_CLEARS = "WRC"
  WRITE_CLEARS = "WC"
  WRITE_ONE_CLEARS = "W1C"
  WRITE_ZERO_CLEARS = "W0C"


def _conv2access(val: Union[str, AccessType]) -> AccessType:
  if (isinstance(val, AccessType)):
    return val
  if (isinstance(val, str)):
    try:
      return AccessType[val.upper()]
    except KeyError:
      try:
        return AccessType(val.upper())
      except KeyError:
        pass
    raise ValueError(f"Invalid AccessType String \"{val}\"")
  raise ValueError("Function _conv2access takes a single argument of type str or AccessType")


class PortDirection(Enum):
  OUTPUT = "output"
  INPUT = "input"
  INOUT = "inout"


def _conv2direction(val: Union[str, PortDirection]) -> PortDirection:
  if (isinstance(val, PortDirection)):
    return val
  if (isinstance(val, str)):
    return PortDirection[val.upper()]
  raise ValueError("Function _conv2direction takes a single argument of type" +
                   " str or PortDirection")


class SignalType(Enum):
  WIRE = "wire"
  REG = "reg"
  LOGIC = "logic"
  REAL = "real"
  WREAL = "wreal"
  WREAL4 = "wreal4state"


def _conv2sigtype(val: Union[str, SignalType]) -> SignalType:
  if (isinstance(val, SignalType)):
    return val
  if (isinstance(val, str)):
    try:
      return SignalType[val.upper()]
    except KeyError:
      try:
        return SignalType(val.lower())
      except KeyError:
        pass
    raise ValueError(f"Invalid SignalType String \"{val}\"")
  raise ValueError("Function _conv2sigtype takes a single argument of type str or SignalType")


class ParamType(Enum):
  NONE = "none"
  INTEGER = "int"
  STRING = "string"


def _conv2paramtype(val: Union[str, ParamType]) -> ParamType:
  if (isinstance(val, ParamType)):
    return val
  if (isinstance(val, str)):
    try:
      return ParamType[val.upper()]
    except KeyError:
      try:
        return ParamType(val.lower())
      except KeyError:
        pass
    raise ValueError(f"Invalid ParamType String \"{val}\"")
  raise ValueError("Function _conv2sigtype takes a single argument of type str or ParamType")


##########################################################################
# Memory Classes
##########################################################################


@define
class Field:
  """Class to represent a field of a Register
  """

  name: str = field(validator=validators.instance_of(str))
  """The name of the field"""

  access: AccessType = field(validator=validators.instance_of(AccessType),
                             converter=_conv2access)
  """The access type of the field"""

  lsb_pos: int = field(validator=validators.instance_of(int))
  """The Least-Significant bit location of the field in the register"""

  width: int = field(validator=validators.instance_of(int), default=1)
  """The width of the field in bits"""

  volatile: bool = field(validator=validators.instance_of(bool), default=False)
  """The volatile field flag (i.e. the underlying data can change without bus interaction)"""

  reset: int = field(validator=validators.instance_of((int, str)), default=0, converter=_val2int)
  """The reset value of the field"""

  def get_msb_pos(self) -> int:
    """
    Returns:
        int: The position of the msb (zero indexed)
    """
    return self.lsb_pos + self.width - 1

  def overlaps(self, fld: Field) -> bool:
    return _overlaps((self.lsb_pos, self.get_msb_pos()), (fld.lsb_pos, fld.get_msb_pos()))


@define
class Register:
  """Class to represent a Register from a register bank
  """
  name: str = field(validator=validators.instance_of(str))
  offset: int = field(validator=validators.instance_of(int))
  _flds: list[Field] = field(init=False, factory=list)

  def add(self, fld: Field) -> None:
    """Adds a field to the register at the provided fields specified lsb_pos

    Args:
        fld (Field): The field to add to the register

    Raises:
        ValueError: If the field's size overlaps an existing field
        ValueError: If the field shares a name with an existing field
    """
    new_idx = -1
    for idx, val in enumerate(self._flds):
      if fld.overlaps(val):
        raise ValueError(f"Can't add field named {fld.name} to register named {self.name}." +
                         f" Overlaps with existing field (named {val.name}).")
      if fld.name == self.name:
        raise ValueError(f"Cant add field named {fld.name} to register named {self.name}." +
                         " A field of that name already exists.")

      if (val.get_msb_pos() > fld.lsb_pos):
        new_idx = idx + 1

    self._flds.insert(new_idx, fld)

  def append(self, fld: Field) -> int:
    """Adds a field to the end of the existing register

    Args:
        fld (Field): The field to add to the end of the register

    Raises:
        ValueError: If the field shares a name with an existing field

    Returns:
        int: The new lsb_pos of the field
    """
    if sum([(1 if fld.name == f.name else 0) for f in self._flds]) > 0:
      raise ValueError(f"Cant add field named {fld.name} to register named {self.name}." +
                       " A field of that name already exists.")

    if (len(self._flds) == 0):
      fld.lsb_pos = 0
    else:
      fld.lsb_pos = self._flds[-1].get_msb_pos() + 1
    self._flds.append(fld)
    return fld.lsb_pos

  def overlaps(self, reg: Register, reg_size: int) -> bool:
    """Determines if this register's bytes overlap with the provided register's bytes

    Args:
        reg (Register): The register to check against
        reg_size (int): The maximum size of the register in bytes

    Returns:
        bool: True they overlap, False otherwise
    """
    return _overlaps((self.offset, self.offset + reg_size), (reg.offset, reg.offset + reg_size))

  def get(self, i: int) -> Field:
    return self._flds[i]

  def size(self) -> int:
    """The size of the register in bits

    Returns:
        int: The size of the register
    """
    if (len(self._flds) == 0):
      return 0
    return self._flds[-1].get_msb_pos()

  def __len__(self) -> int:
    return len(self._flds)

  def __iter__(self) -> Iterator[Field]:
    return self._flds.__iter__()


@define
class AddressBlock:
  """Class to represent an address block from a memory map
  """

  name: str = field(validator=validators.instance_of(str))
  """Name of the Address Block"""
  reg_size: int = field(validator=validators.instance_of(int))
  """Size of the registers in the address block (in Bytes)"""
  _regs: list[Register] = field(init=False, factory=list)
  """List of register in the address block"""

  def add(self, reg: Register) -> None:
    """Adds a register to the address block at the provided register's specified offset

    Args:
        reg (Register): The register to add to the address block

    Raises:
        ValueError: If the register's size overlaps an existing register
        ValueError: If the register shares a name with an existing register
    """
    new_idx = -1
    if reg.size() > self.reg_size * 8:
      raise ValueError(f"Can't add register named {reg.name} to address block named {self.name}." +
                       "The register is larger than the address block reg size " +
                       f"({self.reg_size} bytes)")

    for idx, val in enumerate(self._regs):
      if reg.overlaps(val, self.reg_size):
        raise ValueError(f"Can't add register named {reg.name} to address block named " +
                         f"{self.name}. Overlaps with existing register (named {val.name}).")
      if reg.name == self.name:
        raise ValueError(f"Cant add register named {reg.name} to address block named {self.name}." +
                         " A register of that name already exists.")

      if (val.offset + val.size() > reg.offset):
        new_idx = idx + 1

    self._regs.insert(new_idx, reg)

  def append(self, reg: Register) -> int:
    """Adds a register to the end of the existing address block

    Args:
        reg (Register): The register to add to the end of the address block

    Raises:
        ValueError: If the register shares a name with an existing register

    Returns:
        int: The new offset of the register
    """
    if (reg.name in [r.name for r in self._regs]):
      raise ValueError(f"Cant add register named {reg.name} to address block named {self.name}." +
                       " A register of that name already exists.")
    if reg.size() > self.reg_size * 8:
      raise ValueError(f"Can't add register named {reg.name} to address block named {self.name}." +
                       "The register is larger than the address block reg size " +
                       f"({self.reg_size} bytes)")

    if (len(self._regs) == 0):
      reg.offset = 0
    else:
      reg.offset = self._regs[-1].offset + 1
    self._regs.append(reg)
    return reg.offset

  def get(self, i: int) -> Register:
    return self._regs[i]

  def __len__(self) -> int:
    return len(self._regs)

  def __iter__(self) -> Iterator[Register]:
    return self._regs.__iter__()


@define
class MemoryMap:
  """Class to represent an RTL memory map
  """
  name: str = field(validator=validators.instance_of(str))
  """Name of the Memory Map"""
  _blocks: list[AddressBlock] = field(init=False, factory=list)
  """List of the blocks in the MemoryMap"""

  def add(self, block: AddressBlock) -> None:

    if (block.name in [b.name for b in self._blocks]):
      raise ValueError(f"Can't add AddressBlock named {block.name} to the MemoryMap named" +
                       f" {self.name}. An AddressBlock of that name already exists.")

    self._blocks.append(block)

  def get(self, i: Union[str, int]) -> AddressBlock:
    """Gets the corresponding addressblock by name or index

    Args:
        i (Union[str, int]): The name (str) or index (int) used to get the address block

    Returns:
        AddressBlock: The addressblock with the specified name or index
    """
    if (isinstance(i, int)):
      return self._blocks[i]

    for b in self._blocks:
      if b.name == i:
        return b

    raise ValueError(f"Can't find AddressBlock with name: {i}, in MemoryMap ({self.name})")

  def __len__(self) -> int:
    return len(self._blocks)

  def __iter__(self) -> Iterator[AddressBlock]:
    return self._blocks.__iter__()


##########################################################################
# Design Classes
##########################################################################

@define
class Port:
  """Class to represent the port in an RTL Module
  """
  name: str = field(validator=validators.instance_of(str))
  """The name of the port"""
  dir: PortDirection = field(validator=validators.instance_of(PortDirection),
                             converter=_conv2direction)
  """The direction of the port"""
  width: int = field(validator=validators.instance_of(int), default=1)
  """The width of the port"""
  type: SignalType = field(validator=validators.instance_of(SignalType),
                           converter=_conv2sigtype, default=SignalType.LOGIC)
  """The signal type of the port"""


@define
class Parameter:
  """Class to represent a parameter in an RTL Module
  """
  name: str = field(validator=validators.instance_of(str))
  """The name of the parameter"""
  type: ParamType = field(validator=validators.instance_of(ParamType), default=ParamType.NONE)
  """The type of the parameter"""
  default: Any = field(default=None)
  """The default of the parameter"""


class _ConnectionGraph:
  """Class which
  """


@define
class Module:
  """Class to represent the top-level definition of an RTL module
  """
  name: str = field(validator=validators.instance_of(str))
  """The module name"""
  _ports: list[Port] = field(init=False, factory=list)
  _params: list[Port] = field(init=False, factory=list)
  _subModule: list[Module]
